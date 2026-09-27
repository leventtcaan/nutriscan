"""Sentetik 'Birlesik Menu + Sepet + Market' (MSM) MILP benchmark'i.
OR-Tools 9.15: SCIP ve CP-SAT (MPSolver arayuzu), GLOP ile LP gevsetmesi.

Amac: v4 MENU adiminin, paket tamsayiligi + kiler/israf + <=2 market secimiyle BIRLESIK
kurulan halinin hangi olcekte exact cozuculer icin zorlastigini KABA olcmek; ayrica
"once menu, sonra sepet" (sirali) yaklasimina gore birlesik modelin kazancini gormek.
GERCEK VERI DEGIL. Tum sayilar sentetik uretecten gelir.

Kullanim: python3 05-ek-menu_bench.py [zaman_limiti_s] [olcek ...]
          python3 05-ek-menu_bench.py --parca [zaman_limiti_s] [olcek ...]   (birlesik vs sirali, TL bilesenleri)
Sonuclar (2026-09-24, Apple M1): 05-ek-menu_bench_sonuc.txt, 05-ek-menu_bench_parca.txt
"""
import random, time, math, sys, statistics
from ortools.linear_solver import pywraplp

ALLERGENS = ['gluten', 'findik', 'sut', 'yumurta', 'susam']
ALG_P = [0.08, 0.03, 0.12, 0.05, 0.03]      # malzeme basina alerjen olasiligi
HANE_YASAK = {'gluten', 'findik'}            # 4 kisilik hane: cocukta findik, bir uyede colyak
MEMBERS = 4
PACKS = [200, 250, 400, 500, 1000, 2000]


def gen(nR, nI, nS, days, mpd, seed):
    rnd = random.Random(seed)
    ings = []
    for i in range(nI):
        per = rnd.random() < 0.5
        loose = per and rnd.random() < 0.5                      # manav: 100 g adimla
        packs = [100] if loose else sorted(rnd.sample(PACKS, rnd.choice([1, 2, 3])))
        ings.append(dict(per=per, shelf=(rnd.randint(3, 10) if per else 180), packs=packs,
                         ppk=rnd.uniform(30, 600),                # TL/kg
                         alg={a for a, p in zip(ALLERGENS, ALG_P) if rnd.random() < p}))
    w = [1 / (i + 1) ** 0.8 for i in range(nI)]                  # Zipf: sogan, salca, yag ortak
    recipes = []
    for r in range(nR):
        ch = set()
        k = rnd.randint(4, 10)
        while len(ch) < k:
            ch.add(rnd.choices(range(nI), w)[0])
        recipes.append(dict(use={i: rnd.randint(5, 150) for i in ch},     # g/porsiyon
                            time=rnd.choice([15, 20, 30, 40, 45, 60, 90]), cat=rnd.randrange(12),
                            pref=rnd.randint(0, 10), recent=rnd.random() < 0.1,
                            na=rnd.randint(300, 2500), prot=rnd.randint(10, 45),
                            alg=set().union(*[ings[i]['alg'] for i in ch])))
    stores = [dict(mult={i: rnd.uniform(0.85, 1.2) for i in range(nI)},
                   avail={i: rnd.random() < 0.9 for i in range(nI)},
                   travel=rnd.randint(0, 60)) for _ in range(nS)]
    pantry = {i: dict(amt=rnd.randint(100, 800), exp=rnd.randint(1, days))
              for i in rnd.sample(range(nI), max(1, nI // 10))}
    return dict(ings=ings, recipes=recipes, stores=stores, pantry=pantry, days=days, mpd=mpd)


def price(ing, g, mult):
    disc = 1 - 0.08 * math.log2(g / min(ing['packs'])) if g > 100 else 1.0   # buyuk paket ucuz
    return int(round(ing['ppk'] * g / 1000 * mult * disc * 100))           # kurus


def build(inst, solver, relax=False, fixed_menu=None, stage1=False):
    I, R, S, P = inst['ings'], inst['recipes'], inst['stores'], inst['pantry']
    days, mpd = inst['days'], inst['mpd']
    T = days * mpd
    s = pywraplp.Solver.CreateSolver(solver)
    V = (lambda lb, ub: s.NumVar(lb, ub, '')) if relax else (lambda lb, ub: s.IntVar(lb, ub, ''))
    B = (lambda: s.NumVar(0, 1, '')) if relax else (lambda: s.BoolVar(''))
    weekday = lambda t: (t // mpd) % 7 < 5
    ok = [r for r, rc in enumerate(R) if not (rc['alg'] & HANE_YASAK)]   # C2 yapisal eleme
    y = {}
    for t in range(T):
        for r in ok:
            if weekday(t) and R[r]['time'] > 60:
                continue
            if fixed_menu is not None and fixed_menu.get(t) != r:
                continue
            y[r, t] = B()
    for t in range(T):
        s.Add(sum(y[r, tt] for (r, tt) in y if tt == t) == 1)
    for r in ok:
        s.Add(sum(y[rr, t] for (rr, t) in y if rr == r) <= 1)           # tarif tekrari yok
    for c in range(12):                                                 # ayni kategori 2 gunde 1
        for d in range(days - 1):
            ts = [t for t in range(T) if d <= t // mpd <= d + 1]
            s.Add(sum(y[r, t] for (r, t) in y if t in ts and R[r]['cat'] == c) <= 1)
    s.Add(sum(R[r]['time'] * v for (r, t), v in y.items() if weekday(t)) <= 40 * sum(weekday(t) for t in range(T)))
    sl_na, sl_pr = s.NumVar(0, s.infinity(), ''), s.NumVar(0, s.infinity(), '')
    s.Add(sum(R[r]['na'] * v for (r, t), v in y.items()) <= 1400 * T + sl_na)
    s.Add(sum(R[r]['prot'] * v for (r, t), v in y.items()) >= 25 * T - sl_pr)

    need = {i: [] for i in range(len(I))}
    for (r, t), v in y.items():
        for i, g in R[r]['use'].items():
            need[i].append((MEMBERS * g, t // mpd, v))
    cost_terms, waste_terms, pantry_terms = [], [], []
    z = [B() for _ in S]
    s.Add(sum(z) <= 2)
    s.Add(sum(z) >= 1)
    for i, lst in need.items():
        if not lst and i not in P:
            continue
        maxneed = sum(g for g, _, _ in lst)
        q = sum(g * v for g, _, v in lst)
        u = 0
        if i in P:                                                     # kileri once kullan
            u = V(0, P[i]['amt'])
            s.Add(u <= sum(g * v for g, d, v in lst if d < P[i]['exp']))
            pantry_terms.append(-u * (I[i]['ppk'] / 10))                 # kilerden kullanilan = alinmayan
            if I[i]['per'] or P[i]['exp'] <= days:
                waste_terms.append((P[i]['amt'] - u) * (I[i]['ppk'] / 10))   # kurus/g * g
                pantry_terms.append((P[i]['amt'] - u) * (I[i]['ppk'] / 10))
        if not lst:
            continue
        buy = []
        for si, st in enumerate(S):
            if not st['avail'][i]:
                continue
            for g in I[i]['packs']:
                n = V(0, math.ceil(maxneed / g) + 1)
                s.Add(n <= (math.ceil(maxneed / g) + 1) * z[si])
                buy.append(g * n)
                cost_terms.append(price(I[i], g, st['mult'][i]) * n)
        if not buy:                                                    # hicbir markette yok
            s.Add(q <= u)
            continue
        s.Add(sum(buy) + u >= q)
        if I[i]['shelf'] <= days:                                      # artan bozulur = israf
            waste_terms.append((sum(buy) + u - q) * (I[i]['ppk'] / 10))
    travel = sum(100 * st['travel'] * z[si] for si, st in enumerate(S))
    pref = sum((1500 * R[r]['pref'] - 5000 * R[r]['recent']) * v for (r, t), v in y.items())
    if stage1:
        # sirali taban cizgisi, 1. asama: kiler-farkinda ama paket/market/alim-artigi yok;
        # malzeme ortalama gram fiyatiyla dogrusal (bugunku tipik "once menu, sonra liste" akisi)
        lin = sum(MEMBERS * g * I[i]['ppk'] / 10 * v for (r, t), v in y.items() for i, g in R[r]['use'].items())
        s.Minimize(lin + sum(pantry_terms) - pref + 200 * sl_na + 2000 * sl_pr)
    else:
        s.Minimize(sum(cost_terms) + sum(waste_terms) + travel - pref + 200 * sl_na + 2000 * sl_pr)
    parts = dict(alim=sum(cost_terms), israf=sum(waste_terms), yol=travel, tercih=pref)
    return s, y, parts


def solve(inst, solver, tl, **kw):
    s, y, parts = build(inst, solver, **kw)
    s.SetTimeLimit(int(tl * 1000))
    if solver == 'CP_SAT':
        s.SetSolverSpecificParametersAsString('num_workers:8')
    t0 = time.time()
    st = s.Solve()
    dt = time.time() - t0
    if st not in (pywraplp.Solver.OPTIMAL, pywraplp.Solver.FEASIBLE):
        return dict(status=st, time=dt, obj=None, bound=None, nvar=s.NumVariables(), menu=None)
    menu = {t: r for (r, t), v in y.items() if v.solution_value() > 0.5}
    bound = s.Objective().BestBound() if solver != 'GLOP' else s.Objective().Value()
    pv = {}
    for k, e in parts.items():
        try:
            pv[k] = e.solution_value() / 100          # TL (tercih: TL esdegeri)
        except AttributeError:
            pv[k] = float(e) / 100
    return dict(status=st, time=dt, obj=s.Objective().Value(), bound=bound,
                nvar=s.NumVariables(), ncon=s.NumConstraints(), menu=menu, parts=pv)


SCALES = {
    # ad: (tarif, malzeme, market, gun, ogun/gun)
    'S0': (50, 60, 2, 5, 1),
    'S1': (100, 120, 4, 7, 1),
    'S2': (200, 200, 8, 7, 1),
    'S3': (200, 200, 8, 7, 2),
    'S4': (400, 300, 10, 7, 2),
    'S5': (400, 300, 10, 14, 2),
}

def parca(names, tl, seeds=(0, 1, 2)):
    """Birlesik vs sirali: amac bilesenleri (TL). Birlesik = CP-SAT cozumu."""
    for nm in names:
        nR, nI, nS, days, mpd = SCALES[nm]
        for sd in seeds:
            inst = gen(nR, nI, nS, days, mpd, sd)
            b = solve(inst, 'CP_SAT', tl)
            s1 = solve(inst, 'SCIP', tl, stage1=True)
            q = solve(inst, 'SCIP', tl, fixed_menu=s1['menu'])
            f = lambda d: ' '.join(f"{k}={v:.0f}" for k, v in d['parts'].items())
            print(f"{nm} seed{sd} BIRLESIK {f(b)} | SIRALI {f(q)}", flush=True)


if __name__ == '__main__':
    if '--parca' in sys.argv:
        a = [x for x in sys.argv[1:] if x != '--parca']
        parca(a[1:] or ['S1'], float(a[0]) if a else 30)
        sys.exit()
    tl = float(sys.argv[1]) if len(sys.argv) > 1 else 60
    names = sys.argv[2:] or list(SCALES)
    seeds = [0, 1, 2]
    for nm in names:
        nR, nI, nS, days, mpd = SCALES[nm]
        rows = []
        for sd in seeds:
            inst = gen(nR, nI, nS, days, mpd, sd)
            lp = solve(inst, 'GLOP', tl, relax=True)
            sc = solve(inst, 'SCIP', tl)
            cp = solve(inst, 'CP_SAT', tl)
            s1 = solve(inst, 'SCIP', tl, stage1=True)                  # sirali: once menu
            seq = solve(inst, 'SCIP', tl, fixed_menu=s1['menu']) if s1['menu'] else dict(obj=None)
            best = min(o for o in (sc['obj'], cp['obj']) if o is not None)
            bnd = max(b for b in (sc['bound'], cp['bound']) if b is not None)
            rows.append((sd, sc, cp, lp, seq, best, bnd))
            gap = lambda o: (o - bnd) / abs(o) * 100 if o is not None else float('nan')
            print(f"{nm} seed{sd} nvar={sc['nvar']} ncon={sc.get('ncon')} | "
                  f"SCIP {sc['time']:.1f}s gap%={gap(sc['obj']):.2f} | CP-SAT {cp['time']:.1f}s gap%={gap(cp['obj']):.2f} | "
                  f"LP={lp['obj']:.0f} LPgap%={(best - lp['obj']) / abs(best) * 100:.1f} | "
                  f"sirali={seq['obj'] or float('nan'):.0f} (2.asama {seq.get('time', float('nan')):.1f}s) birlesik={best:.0f} sirali_fark%="
                  f"{((seq['obj'] - best) / abs(best) * 100) if seq['obj'] is not None else float('nan'):.1f}",
                  flush=True)
