"""Mention → concept: (1) E-number, (2) exact alias, (3) fuzzy alias; otherwise unknown.
Vector search (Qdrant) is step (4) in the decision record and is added in the next iteration."""
import csv
import difflib
import re
import pathlib
from dataclasses import dataclass

from .text import e_code, normalize

DATA = pathlib.Path(__file__).resolve().parents[2] / "data"
FUZZY_CUTOFF = 0.88  # similarity ratio for accepting a fuzzy alias; tuned on the matching test set


@dataclass
class Match:
    concept_id: str = ""
    method: str = "unknown"        # e_code | exact | plural | fuzzy | function_label | noise | unknown
    score: float = 0.0
    alias: str = ""


class Dictionary:
    def __init__(self, data_dir=DATA):
        self.concepts = {}
        for r in csv.DictReader(open(data_dir / "sozluk" / "kavram.csv", encoding="utf-8")):
            r["parents"] = [p for p in r["ust_kavramlar"].split("|") if p]
            self.concepts[r["kavram_id"]] = r
        self.index = {}       # normalised alias → concept ids (Turkish aliases first)
        rows = list(csv.DictReader(open(data_dir / "sozluk" / "esanlamli.csv", encoding="utf-8")))
        team = data_dir / "sozluk" / "ekip_esanlamli.csv"     # team-reviewed Turkish aliases (step 3 of K8)
        if team.exists():
            rows += list(csv.DictReader(open(team, encoding="utf-8")))
        for r in sorted(rows, key=lambda r: r["dil"] != "tr"):
            self.index.setdefault(normalize(r["metin"]), []).append(r["kavram_id"])
        self.keys_tr = [normalize(r["metin"]) for r in rows if r["dil"] == "tr"]
        self.keys_all = list(self.index)

    def ancestors(self, concept_id):
        seen, stack = [], list(self.concepts.get(concept_id, {}).get("parents", []))
        while stack:
            p = stack.pop()
            if p in self.concepts and p not in seen:
                seen.append(p)
                stack.extend(self.concepts[p]["parents"])
        return seen

    def name(self, concept_id):
        c = self.concepts.get(concept_id, {})
        return c.get("ad_tr") or c.get("ad_en") or concept_id

    def match(self, norm: str) -> Match:
        if re.fullmatch(r"[\d\s.,/()\[\]-]*[a-zçğıöşü]?", norm):
            return Match(method="noise")          # "6", "12", "b" — split leftovers, not ingredients
        code = e_code(norm)
        if code and code in self.concepts:
            return Match(code, "e_code", 1.0, norm)
        if norm in self.index:
            return Match(self.index[norm][0], "exact", 1.0, norm)
        stem = re.sub(r"(ler|lar)(i|ı)?$", "", norm)   # Turkish plural: "aroma vericiler" → "aroma verici"
        if stem != norm and stem in self.index:
            return Match(self.index[stem][0], "plural", 1.0, stem)
        for keys in (self.keys_tr, self.keys_all):
            close = difflib.get_close_matches(norm, keys, n=1, cutoff=FUZZY_CUTOFF)
            if close:
                ratio = difflib.SequenceMatcher(None, norm, close[0]).ratio()
                return Match(self.index[close[0]][0], "fuzzy", round(ratio, 3), close[0])
        return Match()
