"""Characterization test: the refactored package must reproduce the prototype's outputs exactly.

tests/golden/prototype_v0.json was produced by the pre-refactor code (issue #7). It also freezes known
wrong outcomes (docs/tasarim/00-denetim-raporu.md §A); fixing them (#8, #9) updates this file on purpose.
"""
import json
import pathlib
import unittest

from nutriscan.pipeline import analyze

GOLDEN = pathlib.Path(__file__).resolve().parent / "golden" / "prototype_v0.json"
CONDITIONS = ["colyak", "diyabet", "kronik_bobrek", "hipertansiyon", "laktoz_intoleransi", "fenilketonuri", "sulfit_hassasiyeti"]


def num(v):
    v = (v or "").strip().replace(",", ".")
    return float(v) if v else None


class CharacterizationTest(unittest.TestCase):
    def test_outputs_match_golden_record(self):
        golden = json.loads(GOLDEN.read_text(encoding="utf-8"))
        self.assertEqual(len(golden), 63)
        for case in golden:
            lab = case["label"]
            result = analyze(lab["icindekiler"],
                             {"sekerler_g_100": num(lab["sekerler_g_100"]), "tuz_g_100": num(lab["tuz_g_100"])},
                             liquid=lab["sivi"] == "evet", conditions=CONDITIONS)
            mentions = [[m.raw, m.norm, m.kind, x.concept_id, x.method, x.score] for m, x in result.matched + result.may_matched]
            with self.subTest(source=case["source"]):
                self.assertEqual(mentions, case["mentions"])
                self.assertEqual(result.results, case["results"])


if __name__ == "__main__":
    unittest.main()
