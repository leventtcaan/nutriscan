"""Behaviour tests for the matcher and rule table.  Run: python3 -m unittest discover -s tests -v"""
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "service"))
from nutriscan.matcher import Dictionary                      # noqa: E402
from nutriscan.rules import evaluate, load_rules              # noqa: E402
from nutriscan.text import e_code, normalize, split_label     # noqa: E402
from run_labels import match_all                              # noqa: E402

D, RULES = Dictionary(), load_rules()


def run(label, sugars=None, salt=None, liquid=False):
    mentions, may, full = split_label(label)
    return evaluate(D, match_all(D, mentions), match_all(D, may), full,
                    {"sekerler_g_100": sugars, "tuz_g_100": salt}, liquid, ["colyak", "diyabet", "kronik_bobrek"], RULES)


class TextTests(unittest.TestCase):
    def test_turkish_lowercase_and_percent(self):
        self.assertEqual(normalize("BUĞDAY UNU (%45)"), "buğday unu")
        self.assertEqual(normalize("İÇİNDEKİLER"), "içindekiler")

    def test_e_code_variants(self):
        for raw in ("E102", "e 102", "E-102"):
            self.assertEqual(e_code(normalize(raw)), "E102")
        self.assertEqual(e_code("e150d"), "E150D")
        self.assertIsNone(e_code("şeker"))

    def test_claim_is_not_an_ingredient(self):
        mentions, _, full = split_label("İçindekiler: mısır unu, tuz. Glutensiz.")
        self.assertEqual([m.norm for m in mentions], ["mısır unu", "tuz"])
        self.assertIn("glutensiz", full)

    def test_may_contain_is_separated(self):
        mentions, may, _ = split_label("İçindekiler: şeker. Eser miktarda süt ve fındık içerebilir.")
        self.assertEqual([m.norm for m in may], ["süt", "fındık"])


class RuleTests(unittest.TestCase):
    def test_wheat_flour_is_gluten_through_is_a_chain(self):
        self.assertEqual(run("İçindekiler: buğday unu, şeker.")["colyak"]["sonuc"], "Uygun değil")

    def test_glucose_syrup_alone_is_not_gluten(self):   # Reg. (EU) 1169/2011 Annex II exemption
        self.assertNotEqual(run("İçindekiler: glikoz şurubu, şeker.")["colyak"]["sonuc"], "Uygun değil")

    def test_unknown_ingredient_blocks_no_issue_found(self):
        r = run("İçindekiler: tuz, xyzabc bileşeni. Glutensiz.")
        self.assertEqual(r["colyak"]["sonuc"], "Doğrulanamadı")

    def test_sugar_bands_solid_and_liquid(self):
        self.assertEqual(run("İçindekiler: şeker.", sugars=48)["diyabet"]["sonuc"], "Dikkat")
        self.assertEqual(run("İçindekiler: şeker.", sugars=4)["diyabet"]["sonuc"], "Engel bulunmadı")
        self.assertEqual(run("İçindekiler: su, şeker.", sugars=4, liquid=True)["diyabet"]["sonuc"], "Dikkat")

    def test_missing_nutrition_is_not_verified(self):
        self.assertEqual(run("İçindekiler: şeker.")["diyabet"]["sonuc"], "Doğrulanamadı")

    def test_salt_is_converted_to_sodium(self):   # salt = sodium × 2.5 → 0.25 g salt = 0.1 g sodium ≤ 0.12
        self.assertEqual(run("İçindekiler: tuz.", salt=0.25)["kronik_bobrek"]["sonuc"], "Engel bulunmadı")
        self.assertEqual(run("İçindekiler: tuz.", salt=1.4)["kronik_bobrek"]["sonuc"], "Dikkat")


if __name__ == "__main__":
    unittest.main()
