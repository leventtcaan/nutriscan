"""Checks for the first draft of the rule data (issue #12)."""
import csv
import math
import unittest
from pathlib import Path

from nutriscan.codes import outcome_to_api, rule_type_to_api, source_kind_to_api


DATA = Path(__file__).resolve().parents[1] / "data"


def read_rows(path):
    with (DATA / path).open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


class RuleDataTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rules = read_rows("kurallar/kurallar.csv")
        cls.conditions = read_rows("kurallar/durumlar.csv")

    def test_rule_inventory_and_status(self):
        self.assertEqual(len(self.rules), 17)
        self.assertEqual(len({row["kural_id"] for row in self.rules}), 17)
        for row in self.rules:
            with self.subTest(rule=row["kural_id"]):
                self.assertEqual(row["durum_satir"], "taslak")
                self.assertEqual(row["surum"], "1")
                self.assertTrue(row["yazan"])
                self.assertTrue(row["kaynak_id"])
                rule_type_to_api(row["kural_turu"])
                source_kind_to_api(row["kaynak_turu"])
                if row["kural_turu"] == "miktar":
                    self.assertEqual(row["sonuc"], "")
                else:
                    outcome_to_api(row["sonuc"])
                    self.assertEqual(row["bantlar"], "")

    def test_conditions_and_concepts(self):
        condition_ids = {row["durum_id"] for row in self.conditions}
        self.assertEqual(len(self.conditions), 7)
        self.assertEqual(len(condition_ids), 7)
        self.assertEqual(condition_ids, {row["durum"] for row in self.rules})
        concepts = {row["kavram_id"] for row in read_rows("sozluk/kavram.csv")}
        for row in self.rules:
            with self.subTest(rule=row["kural_id"]):
                if row["kural_turu"] in {"varlik", "icerebilir"}:
                    self.assertLessEqual(set(row["hedef"].split("|")), concepts)
                if row["muaf"]:
                    self.assertLessEqual(set(row["muaf"].split("|")), concepts)

    def test_amount_bands(self):
        for row in self.rules:
            if row["kural_turu"] != "miktar":
                continue
            with self.subTest(rule=row["kural_id"]):
                bases = []
                for group in row["bantlar"].split(";"):
                    basis, steps = group.split(":", 1)
                    bases.append(basis)
                    thresholds = []
                    for step in steps.split("|"):
                        limit, label = step.split("=", 1)
                        outcome_to_api(label)
                        thresholds.append(limit)
                    self.assertEqual(thresholds[-1], ">")
                    bounds = [float(value) for value in thresholds[:-1]]
                    self.assertTrue(bounds)
                    self.assertTrue(all(math.isfinite(value) for value in bounds))
                    self.assertEqual(bounds, sorted(set(bounds)))
                self.assertIn(sorted(bases), [["her_ikisi"], ["kati", "sivi"]])

    def test_dependencies_point_to_first_pass_in_same_condition(self):
        by_id = {row["kural_id"]: row for row in self.rules}
        for row in self.rules:
            if not row["bagimlilik"]:
                continue
            with self.subTest(rule=row["kural_id"]):
                for rule_id in row["bagimlilik"].split("|"):
                    dependency = by_id[rule_id]
                    self.assertEqual(dependency["durum"], row["durum"])
                    self.assertEqual(dependency["bagimlilik"], "")
                    self.assertNotEqual(dependency["kural_turu"], "varsayilan")

    def test_derived_sodium_field(self):
        self.assertEqual(read_rows("kurallar/turetilen_alanlar.csv"), [{
            "alan": "sodyum_g_100", "kaynak_alan": "tuz_g_100",
            "bolen": "2.5", "kaynak_id": "eu-1169-2011",
        }])
