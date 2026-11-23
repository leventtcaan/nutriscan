"""Rule table → outcome per condition. The decision comes only from data/kurallar/*.csv (decision record K5)."""
import csv
import pathlib

DATA = pathlib.Path(__file__).resolve().parents[2] / "data"
SEVERITY = {"Engel bulunmadı": 0, "Doğrulanamadı": 1, "Dikkat": 2, "Uygun değil": 3}
SALT_TO_SODIUM = 2.5  # Reg. (EU) 1169/2011 Annex I: salt = sodium × 2.5


def load_rules(path=DATA / "kurallar" / "kurallar_v0.csv"):
    return list(csv.DictReader(open(path, encoding="utf-8")))


def _hits(dictionary, matched, targets, exempt):
    found = []
    for mention, match in matched:
        if not match.concept_id:
            continue
        lineage = [match.concept_id] + dictionary.ancestors(match.concept_id)
        if exempt & set(lineage):
            continue
        if targets & set(lineage):
            found.append(mention.raw)
    return found


def _band(value, spec, liquid):
    """spec: 'kati:0.5=X|5=Y|>=Z;sivi:...' or 'her_ikisi:...' → outcome."""
    parts = dict(p.split(":", 1) for p in spec.split(";"))
    bands = parts.get("her_ikisi") or parts.get("sivi" if liquid else "kati")
    for step in bands.split("|"):
        limit, outcome = step.split("=")
        if limit == ">" or value <= float(limit):
            return outcome, (None if limit == ">" else float(limit))
    return None, None


def evaluate(dictionary, matched, may_matched, full_text, nutrition, liquid, conditions, rules):
    """matched / may_matched: [(Mention, Match)]; nutrition: {'sekerler_g_100': float|None, 'tuz_g_100': ...}."""
    nutrition = dict(nutrition)
    if nutrition.get("sodyum_g_100") is None and nutrition.get("tuz_g_100") is not None:
        nutrition["sodyum_g_100"] = round(nutrition["tuz_g_100"] / SALT_TO_SODIUM, 3)
    unknown = [m.raw for m, x in matched if x.method == "unknown"]
    results = {}
    for cond in conditions:
        fired = []
        for r in (r for r in rules if r["durum"] == cond):
            only_if = r["parametre"].startswith("yalniz_")
            if only_if and any(f["kural_id"].replace("-", "") in r["parametre"] for f in fired):
                continue
            kind, targets = r["kural_turu"], set(filter(None, r["hedef"].split("|")))
            exempt = set()
            if r["parametre"].startswith("muaf="):
                exempt = set(r["parametre"][5:].split("|"))
            hit = None
            if kind == "varlik":
                found = _hits(dictionary, matched, targets, exempt)
                hit = found and f"bulunan: {', '.join(found)}"
            elif kind == "icerebilir":
                found = _hits(dictionary, may_matched, targets, exempt)
                hit = found and f"içerebilir: {', '.join(found)}"
            elif kind == "beyan":
                hit = r["hedef"] in full_text and f"beyan: {r['hedef']}"
            elif kind == "varsayilan":
                hit = "varsayılan"
            elif kind == "miktar":
                value = nutrition.get(r["hedef"])
                if value is not None:
                    outcome, limit = _band(value, r["parametre"], liquid)
                    unit = "ml" if liquid else "g"
                    detail = f"{r['hedef'].split('_')[0]} {value} g / 100 {unit}"
                    fired.append({"kural_id": r["kural_id"], "sonuc": outcome,
                                  "neden": detail + (f" (≤ {limit})" if limit else " (sınırın üstünde)"),
                                  "kaynak": r["kaynak"], "dogrulama": r["dogrulama"]})
                continue
            elif kind == "eksik_veri":
                if nutrition.get(r["hedef"]) is None:
                    fired.append({"kural_id": r["kural_id"], "sonuc": r["sonuc"],
                                  "neden": "besin tablosu gerekli → kullanıcıdan istenir", "kaynak": r["kaynak"],
                                  "dogrulama": r["dogrulama"]})
                continue
            if hit:
                fired.append({"kural_id": r["kural_id"], "sonuc": r["sonuc"], "neden": f"{r['aciklama']} ({hit})",
                              "kaynak": r["kaynak"], "dogrulama": r["dogrulama"]})
        outcome = max((f["sonuc"] for f in fired), key=SEVERITY.get, default="Doğrulanamadı")
        # Uncertainty only raises risk: an unrecognised ingredient blocks "no issue found" for presence rules.
        if outcome == "Engel bulunmadı" and unknown and any(r["kural_turu"] == "varlik" for r in rules if r["durum"] == cond):
            outcome = "Doğrulanamadı"
            fired.append({"kural_id": "-", "sonuc": outcome, "neden": f"tanınmayan içerik: {', '.join(unknown)}",
                          "kaynak": "Karar belgesi ilke 3", "dogrulama": ""})
        results[cond] = {"sonuc": outcome, "kurallar": fired}
    return results
