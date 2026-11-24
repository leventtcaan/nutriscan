"""Regression tests for wrong outcomes found in the audit (docs/tasarim/00-denetim-raporu.md §A).

Each test states the correct outcome and fails on today's code. They are marked expectedFailure so CI stays
green until #9 fixes the rule engine; a fixed test then reports "unexpected success" and its marker is removed.
Invariants: docs/tasarim/06-kural-motoru.md §2 (D2, D4, D7, D9).
"""
import unittest

from nutriscan.pipeline import analyze

CONDITIONS = ["colyak", "diyabet", "kronik_bobrek", "hipertansiyon", "laktoz_intoleransi", "fenilketonuri", "sulfit_hassasiyeti"]
NO_NUTRITION = {"sekerler_g_100": None, "tuz_g_100": None}


def outcome(text, condition, nutrition=NO_NUTRITION):
    """Run the whole pipeline with all seven conditions and return the outcome label for one of them."""
    return analyze(text, nutrition, liquid=False, conditions=CONDITIONS).results[condition]["sonuc"]


class AuditRegressionTest(unittest.TestCase):
    @unittest.expectedFailure
    def test_a1_no_recognised_ingredient_is_unverified(self):
        # D2: with zero recognised ingredients no condition may be "Engel bulunmadı".
        for text in ["", "İçindekiler: 12, 6"]:
            for condition in ["laktoz_intoleransi", "sulfit_hassasiyeti"]:
                with self.subTest(text=text, condition=condition):
                    self.assertEqual(outcome(text, condition), "Doğrulanamadı")

    @unittest.expectedFailure
    def test_a2_may_contain_milk_is_caution_for_lactose(self):
        # D4: a "may contain" mention matching a presence target blocks "Engel bulunmadı" even without a may-contain row.
        self.assertEqual(outcome("İçindekiler: şeker. Eser miktarda süt içerebilir.", "laktoz_intoleransi"), "Dikkat")

    @unittest.expectedFailure
    def test_a7_sodium_just_above_low_limit_is_caution(self):
        # D7: salt 0.301 g → sodium 0.1204 g > 0.12 g; the comparison uses the raw value, not a rounded one.
        nutrition = {"sekerler_g_100": None, "tuz_g_100": 0.301}
        self.assertEqual(outcome("İçindekiler: tuz, su.", "hipertansiyon", nutrition), "Dikkat")

    @unittest.expectedFailure
    def test_a11_exemption_applies_to_sub_ingredients(self):
        # D9: "buğday" inside an exempt wheat glucose syrup does not fire CEL-01; no gluten-free claim → CEL-04.
        self.assertEqual(outcome("İçindekiler: glikoz şurubu (buğday), şeker.", "colyak"), "Dikkat")


if __name__ == "__main__":
    unittest.main()
