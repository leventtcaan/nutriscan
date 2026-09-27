"""Sentetik 'Akilli Takas' MILP benchmark'i (OR-Tools 9.15, CP-SAT + SCIP + GLOP LP gevsetmesi).
Amac: tipik boyutlarda cozum suresi ve LP gevsetmesi bosluğu hakkinda kaba fikir. Gercek veri DEGIL.
"""
import time, random, statistics, sys
from ortools.linear_solver import pywraplp


def gen(nL, nJ, M=3, seed=0):
    rnd = random.Random(seed)
    lines = []
    for l in range(nL):
        E0 = rnd.uniform(300, 3000)            # kcal (satir toplami)
        base = dict(E=E0,
                    sug=E0 * rnd.uniform(0.0, 0.35) / 4,     # g serbest seker
                    na=E0 * rnd.uniform(0.2, 2.5),            # mg sodyum
                    sfa=E0 * rnd.uniform(0.0, 0.2) / 9,       # g doymus yag
                    fib=E0 * rnd.uniform(0.0, 0.02),          # g lif
                    c=rnd.uniform(20, 250), nps=rnd.randint(-5, 25))
        cons = [m for m in range(M) if rnd.random() < 0.7] or [0]
        cands = [dict(base, d=0.0, allergen=False)]
        for j in range(nJ):
            f = lambda v, s: max(0.0, v * rnd.uniform(1 - s, 1 + s))
            cand = dict(E=f(base['E'], 0.15), sug=f(base['sug'], 0.8), na=f(base['na'], 0.6),
                        sfa=f(base['sfa'], 0.6), fib=f(base['fib'], 0.8), c=f(base['c'], 0.35),
                        nps=base['nps'] + rnd.randint(-10, 6))
            cand['d'] = rnd.uniform(0.1, 1.0)              # sapma/benzemezlik cezasi
            cand['allergen'] = (0 in cons) and rnd.random() < 0.2   # uye 0 = alerjik
            cands.append(cand)
        lines.append(dict(cands=cands, cons=cons))
    return lines

def build(solver_name, lines, k, beta, lam=0.3, relax=False, M=3):
    s = pywraplp.Solver.CreateSolver(solver_name)
    x = {}
    for l, L in enumerate(lines):
        for j, c in enumerate(L['cands']):
            if c['allergen']:
                continue
            x[l, j] = s.NumVar(0, 1, '') if relax else s.BoolVar('')
        s.Add(sum(x[l, j] for j in range(len(L['cands'])) if (l, j) in x) == 1)
    C0 = sum(L['cands'][0]['c'] for L in lines); B = C0 * (1 + beta)
    E0 = sum(L['cands'][0]['E'] for L in lines)
    tot = lambda key: sum(lines[l]['cands'][j][key] * v for (l, j), v in x.items())
    # saglam butce: kabul edilen alt kume ne olursa olsun B asilmasin
    if beta >= 0:
        budget = s.Add(C0 + sum(max(0.0, lines[l]['cands'][j]['c'] - lines[l]['cands'][0]['c']) * v
                                for (l, j), v in x.items()) <= B)
    else:  # tasarruf hedefi: nominal (tum takaslar kabul) butce
        budget = s.Add(tot('c') <= B)
    s.Add(sum(v for (l, j), v in x.items() if j > 0) <= k)
    s.Add(tot('E') >= 0.95 * E0); s.Add(tot('E') <= 1.05 * E0)
    # hedef programlama: yogunluk hedeflerinden asim (dev>=0)
    dev = {}
    dev['sug'] = s.NumVar(0, s.infinity(), ''); s.Add(4 * tot('sug') - 0.10 * tot('E') <= dev['sug'])
    dev['na'] = s.NumVar(0, s.infinity(), '');  s.Add(tot('na') - 1.0 * tot('E') <= dev['na'])   # 2000mg/2000kcal
    dev['sfa'] = s.NumVar(0, s.infinity(), ''); s.Add(9 * tot('sfa') - 0.10 * tot('E') <= dev['sfa'])
    dev['fib'] = s.NumVar(0, s.infinity(), ''); s.Add(0.0125 * tot('E') - tot('fib') <= dev['fib'])
    # uye bazli (uye 0 cocuk: seker yogunlugu <= %5 hedefi), tuketim payi = 1/|S_l|
    dm = s.NumVar(0, s.infinity(), '')
    s.Add(sum((4 * lines[l]['cands'][j]['sug'] - 0.05 * lines[l]['cands'][j]['E']) / len(lines[l]['cons']) * v
              for (l, j), v in x.items() if 0 in lines[l]['cons']) <= dm)
    Esc = E0 / 1000.0
    obj = (sum(-(lines[l]['cands'][j]['nps'] - lines[l]['cands'][0]['nps']) * lines[l]['cands'][j]['E'] / E0 * 100 * v
               for (l, j), v in x.items())
           - (dev['sug'] + dev['na'] / 10 + dev['sfa'] + 10 * dev['fib'] + dm) / Esc
           - lam * 10 * sum(lines[l]['cands'][j]['d'] * v for (l, j), v in x.items()))
    s.Maximize(obj)
    return s, x, budget

def run(solver_name, lines, k, beta, relax=False, tl=60):
    s, x, budget = build(solver_name, lines, k, beta, relax=relax)
    s.SetTimeLimit(tl * 1000)
    t = time.perf_counter(); st = s.Solve(); dt = time.perf_counter() - t
    val = s.Objective().Value() if st in (s.OPTIMAL, s.FEASIBLE) else None
    dual = budget.dual_value() if relax and st == s.OPTIMAL else None
    return dt, st == s.OPTIMAL, val, dual

if __name__ == '__main__':
    configs = [(30, 10), (60, 20), (120, 40), (300, 40)]
    reps = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    print('nL nJ k beta | nvar | CP-SAT med/max s (opt%) | SCIP med/max s (opt%) | LP-gap med %')
    for nL, nJ in configs:
        for k in (5,):
            for beta in (0.0,):
                tc, ts, gaps, oc, os_ = [], [], [], 0, 0
                for r in range(reps):
                    L = gen(nL, nJ, seed=1000 * nL + r)
                    d1, o1, v1, _ = run('CP_SAT', L, k, beta); tc.append(d1); oc += o1
                    d2, o2, v2, _ = run('SCIP', L, k, beta); ts.append(d2); os_ += o2
                    d3, o3, v3, du = run('GLOP', L, k, beta, relax=True)
                    if v2 is not None and v3 is not None and abs(v3) > 1e-9:
                        gaps.append(100 * (v3 - v2) / abs(v3))
                nvar = nL * (nJ + 1)
                print(f'{nL:3d} {nJ:3d} {k:2d} {beta:.2f} | {nvar:5d} | '
                      f'{statistics.median(tc):.3f}/{max(tc):.3f} ({100*oc/reps:.0f}%) | '
                      f'{statistics.median(ts):.3f}/{max(ts):.3f} ({100*os_/reps:.0f}%) | '
                      f'{statistics.median(gaps) if gaps else float("nan"):.2f}')
