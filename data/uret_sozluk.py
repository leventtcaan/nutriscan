"""Sözlük v0 üreticisi: Open Food Facts taksonomilerinden kavram ve eşanlamlı tabloları.

Kaynaklar (ODbL, atıf gerekir — data/kaynaklar.md):
  taxonomies/food/ingredients.txt  → gıda kavramları + Türkçe/İngilizce adlar + üst kavram (IS_A) bağları
  taxonomies/additives.txt         → E-kodlu katkı maddeleri + Türkçe/İngilizce adlar
  taxonomies/additives_classes.txt → katkı sınıfları (renklendirici, emülgatör…): madde değil, işlev adı

Çalıştır:
  python3 data/uret_sozluk.py <indirilen_dosyalarin_klasoru> <off_commit>
Çıktı:
  data/sozluk/kavram.csv       kavram_id, tur, ad_tr, ad_en, e_kodu, wikidata, ust_kavramlar, kaynak
  data/sozluk/esanlamli.csv    kavram_id, metin, dil, iliski, kaynak
"""
import csv, pathlib, re, sys

KOK = pathlib.Path(__file__).resolve().parent
DILLER = ("tr", "en")  # eşanlamlı tablosuna alınan diller


def kimlik(metin):
    """'en: Cereal flour' → 'en:cereal-flour' (üst kavram ve kavram kimliği aynı biçimde yazılsın)."""
    dil, _, ad = metin.partition(":")
    return dil.strip().lower() + ":" + re.sub(r"\s+", "-", ad.strip().lower())


def parse(path):
    """OFF taksonomi biçimi: boş satırla ayrılmış bloklar; '<' üst kavram, 'xx:' adlar, 'ozellik:xx:' özellikler."""
    bloklar = []
    for blok in re.split(r"\n\s*\n", path.read_text(encoding="utf-8")):
        k = {"ust": [], "ad": {}, "oz": {}}
        for satir in blok.splitlines():
            satir = satir.strip()
            if not satir or satir.startswith("#"):
                continue
            if satir.startswith("<"):
                k["ust"].append(kimlik(satir[1:].strip()))
                continue
            m = re.match(r"^([a-z]{2}(?:_[a-z]{2})?):\s*(.*)$", satir)
            if m:
                k["ad"][m.group(1)] = [x.strip() for x in m.group(2).split(",") if x.strip()]
                continue
            m = re.match(r"^([a-z0-9_]+):([a-z]{2}):\s*(.*)$", satir)
            if m:
                k["oz"][m.group(1)] = m.group(3).strip()
        if "en" in k["ad"]:
            k["id"] = kimlik("en:" + k["ad"]["en"][0])
            bloklar.append(k)
    return bloklar


def main(klasor, commit):
    klasor = pathlib.Path(klasor)
    kaynak_ing = f"OFF ingredients.txt @{commit[:8]}"
    kaynak_add = f"OFF additives.txt @{commit[:8]}"
    kavramlar, esler = [], []

    seen = set()
    for k in parse(klasor / "additives.txt"):
        e = k["oz"].get("e_number")
        if not e:
            continue
        kid = "E" + e.upper()
        if kid in seen:          # sub-variants (E322(i), E322(ii)…) share the group code: keep one concept, add names
            for dil in DILLER:
                for metin in k["ad"].get(dil, []):
                    esler.append([kid, metin, dil, "IS_A", kaynak_add])
            continue
        seen.add(kid)
        ad_tr = next((x for x in k["ad"].get("tr", []) if not re.fullmatch(r"E\s?\d+\w*(\([ivx]+\))?", x, re.I)), "")
        ad_en = next((x for x in k["ad"]["en"] if not re.fullmatch(r"E\s?\d+\w*(\([ivx]+\))?", x, re.I)), "")
        kavramlar.append([kid, "katki_maddesi", ad_tr, ad_en, kid, k["oz"].get("wikidata", ""), "", kaynak_add])
        for dil in DILLER:
            for metin in k["ad"].get(dil, []):
                esler.append([kid, metin, dil, "SAME_AS", kaynak_add])

    kaynak_cls = f"OFF additives_classes.txt @{commit[:8]}"
    for k in parse(klasor / "additives_classes.txt"):
        ad_tr = (k["ad"].get("tr") or [""])[0]
        kavramlar.append([k["id"], "katki_sinifi", ad_tr, k["ad"]["en"][0], "", k["oz"].get("wikidata", ""),
                          "|".join(k["ust"]), kaynak_cls])
        for dil in DILLER:
            for metin in k["ad"].get(dil, []):
                esler.append([k["id"], metin, dil, "SAME_AS", kaynak_cls])

    for k in parse(klasor / "ingredients.txt"):
        ad_tr = (k["ad"].get("tr") or [""])[0]
        kavramlar.append([k["id"], "gida_kavrami", ad_tr, k["ad"]["en"][0], "", k["oz"].get("wikidata", ""),
                          "|".join(k["ust"]), kaynak_ing])
        for dil in DILLER:
            for metin in k["ad"].get(dil, []):
                esler.append([k["id"], metin, dil, "SAME_AS", kaynak_ing])

    out = KOK / "sozluk"
    with open(out / "kavram.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["kavram_id", "tur", "ad_tr", "ad_en", "e_kodu", "wikidata", "ust_kavramlar", "kaynak"])
        w.writerows(kavramlar)
    with open(out / "esanlamli.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["kavram_id", "metin", "dil", "iliski", "kaynak"])
        w.writerows(esler)

    sinif = [r for r in kavramlar if r[1] == "katki_sinifi"]
    print(f"katkı sınıfı: {len(sinif)} (Türkçe adlı {sum(1 for r in sinif if r[2])})")
    katki = [r for r in kavramlar if r[1] == "katki_maddesi"]
    gida = [r for r in kavramlar if r[1] == "gida_kavrami"]
    print(f"kavram: {len(kavramlar)} (katkı {len(katki)}, Türkçe adlı {sum(1 for r in katki if r[2])}; "
          f"gıda {len(gida)}, Türkçe adlı {sum(1 for r in gida if r[2])})")
    print(f"eşanlamlı: {len(esler)} (tr {sum(1 for r in esler if r[2] == 'tr')}, en {sum(1 for r in esler if r[2] == 'en')})")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
