"""Run the matcher and rule table on label texts and write a readable report.

    python3 service/run_labels.py                       # tests/eslesme/etiketler.csv → tests/eslesme/rapor.md
    python3 service/run_labels.py <labels.csv> <out.md>
Columns of the labels file: urun, kategori, sivi (evet/hayir), icindekiler, sekerler_g_100, tuz_g_100, ornek_mi
"""
import collections
import csv
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from nutriscan.matcher import Dictionary, Match           # noqa: E402
from nutriscan.rules import evaluate, load_rules          # noqa: E402
from nutriscan.text import flatten, split_label           # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[1]
CONDITIONS = {"colyak": "Çölyak", "diyabet": "Diyabet", "kronik_bobrek": "Kronik böbrek hastalığı"}


def num(v):
    v = (v or "").strip().replace(",", ".")
    return float(v) if v else None


def match_all(d, mentions):
    out = []
    for m in flatten(mentions):
        x = d.match(m.norm)
        if x.method == "unknown" and m.children and all(d.match(c.norm).method == "e_code" for c in m.children):
            x = Match(method="function_label")      # "renklendirici (E102)": the head is a function name
        out.append((m, x))
    return out


def main(src, dst):
    d, rules = Dictionary(), load_rules()
    labels = list(csv.DictReader(open(src, encoding="utf-8")))
    stats, unknown_terms, lines = collections.Counter(), collections.Counter(), []
    for lab in labels:
        mentions, may, full = split_label(lab["icindekiler"])
        matched, may_matched = match_all(d, mentions), match_all(d, may)
        for m, x in matched:
            stats[x.method] += 1
            if x.method == "unknown":
                unknown_terms[m.norm] += 1
        nutrition = {"sekerler_g_100": num(lab.get("sekerler_g_100")), "tuz_g_100": num(lab.get("tuz_g_100"))}
        res = evaluate(d, matched, may_matched, full, nutrition, lab.get("sivi") == "evet", list(CONDITIONS), rules)
        tag = " *(örnek etiket)*" if lab.get("ornek_mi") == "evet" else ""
        lines += [f"## {lab['urun']}{tag}", "", f"> {lab['icindekiler']}", ""]
        lines += ["| Etiketteki ifade | Eşleşen kavram | Yöntem |", "|---|---|---|"]
        for m, x in matched + may_matched:
            name = d.name(x.concept_id) if x.concept_id else "—"
            where = " *(içerebilir)*" if m.kind == "may_contain" else ""
            lines.append(f"| {m.raw}{where} | {name} `{x.concept_id}` | {x.method}{f' ({x.score})' if x.method == 'fuzzy' else ''} |")
        lines += ["", "| Durum | Sonuç | Neden | Kaynak |", "|---|---|---|---|"]
        for c, label in CONDITIONS.items():
            r = res[c]
            why = "; ".join(f"{f['kural_id']}: {f['neden']}" for f in r["kurallar"]) or "kural tetiklenmedi"
            src_ = "; ".join(sorted({f["kaynak"] for f in r["kurallar"]}))
            lines.append(f"| {label} | **{r['sonuc']}** | {why} | {src_} |")
        lines.append("")
    total = sum(stats.values())
    head = [f"# Eşleme ve kural raporu — {len(labels)} etiket", "",
            f"Toplam ifade: **{total}** · E-kodu: {stats['e_code']} · birebir: {stats['exact']} · çoğul: {stats['plural']} · gürültü: {stats['noise']} · "
            f"bulanık: {stats['fuzzy']} · fonksiyon adı: {stats['function_label']} · **tanınmayan: {stats['unknown']}**"
            + (f" (%{100 * stats['unknown'] / total:.0f})" if total else ""), ""]
    if unknown_terms:
        head += ["**Tanınmayan ifadeler (Türkçeleştirme listesi):** "
                 + ", ".join(f"{t} ×{n}" if n > 1 else t for t, n in unknown_terms.most_common()), ""]
    pathlib.Path(dst).write_text("\n".join(head + lines) + "\n", encoding="utf-8")
    print("\n".join(head))


if __name__ == "__main__":
    a = sys.argv[1:]
    main(a[0] if a else ROOT / "tests/eslesme/etiketler.csv", a[1] if len(a) > 1 else ROOT / "tests/eslesme/rapor.md")
