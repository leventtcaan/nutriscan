"""Checks for the first draft of the rule data (issue #12)."""
import csv
import math
import unittest
from pathlib import Path

from nutriscan.codes import outcome_to_api, rule_type_to_api, source_kind_to_api


DATA = Path(__file__).resolve().parents[1] / "data"
RULE_FIELDS = (
    "kural_id", "durum", "kural_turu", "hedef", "muaf", "bantlar", "bagimlilik",
    "sonuc", "aciklama_tr", "kaynak_id", "kaynak_bolum", "kaynak_turu", "surum",
    "durum_satir", "yazan", "kontrol_eden_1", "kontrol_eden_2", "kontrol_tarihi", "not",
)
SOURCE_IDS = {
    "eu-1169-2011", "eu-1924-2006", "eu-828-2014", "tgk-etiketleme-2017",
    "tgk-beslenme-beyan-2017", "ada-2026", "kdigo-2024", "who-sodyum-2012",
    "efsa-laktoz-2010", "ekip-karari",
}
DEPENDENCIES = {
    "CEL-03": "CEL-01",
    "CEL-04": "CEL-01|CEL-02",
    "PKU-02": "PKU-01",
    "SUL-02": "SUL-01",
    "LAK-02": "LAK-01",
}


def read_rows(path):
    with (DATA / path).open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


class RuleDataTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rules = read_rows("kurallar/kurallar.csv")
        cls.conditions = read_rows("kurallar/durumlar.csv")
        cls.old_rules = {
            row["kural_id"]: row
            for row in read_rows("kurallar/kurallar_v0.csv")
        }

    def test_rule_inventory_and_status(self):
        self.assertEqual(tuple(self.rules[0]), RULE_FIELDS)
        self.assertEqual(len(self.rules), 17)
        self.assertEqual(len({row["kural_id"] for row in self.rules}), 17)
        self.assertEqual(
            {row["kural_turu"] for row in self.rules},
            {"varlik", "icerebilir", "beyan", "miktar", "eksik_veri", "varsayilan"},
        )
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

    def test_legacy_rule_details_are_retained(self):
        migrated_rules = {row["kural_id"]: row for row in self.rules}
        self.assertEqual(set(migrated_rules), set(self.old_rules))
        for rule_id, old in self.old_rules.items():
            with self.subTest(rule=rule_id):
                note = migrated_rules[rule_id]["not"]
                self.assertIn(old["kaynak"], note)
                self.assertIn(old["dogrulama"], note)
                if old["parametre"]:
                    self.assertIn(old["parametre"], note)

    def test_conditions_and_concepts(self):
        self.assertEqual(
            tuple(self.conditions[0]),
            ("durum_id", "ad_tr", "mesh_id", "kapsam_notu_tr", "gereken_besin"),
        )
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
                self.assertIn(row["kaynak_id"], SOURCE_IDS)

    def test_legacy_rule_fields_are_migrated(self):
        migrated_rules = {row["kural_id"]: row for row in self.rules}
        for rule_id, old in self.old_rules.items():
            new = migrated_rules[rule_id]
            with self.subTest(rule=rule_id):
                self.assertEqual(new["durum"], old["durum"])
                self.assertEqual(new["kural_turu"], old["kural_turu"])
                self.assertEqual(new["hedef"], old["hedef"])
                self.assertEqual(new["aciklama_tr"], old["aciklama"])
                expected_result = "" if old["kural_turu"] == "miktar" else old["sonuc"]
                self.assertEqual(new["sonuc"], expected_result)
                parameter = old["parametre"]
                if parameter.startswith("muaf="):
                    self.assertEqual(new["muaf"], parameter.removeprefix("muaf="))
                elif old["kural_turu"] == "miktar":
                    self.assertEqual(new["bantlar"], parameter)

                if parameter.startswith("yalniz_"):
                    self.assertEqual(new["bagimlilik"], DEPENDENCIES[rule_id])

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
