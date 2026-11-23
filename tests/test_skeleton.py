"""Package skeleton (issue #7): importable package, thresholds from a config file, one place for outcome codes."""
import os
import pathlib
import tempfile
import unittest
from unittest import mock

from nutriscan import codes, config
from nutriscan.matching.lexical import Dictionary
from nutriscan.types import Outcome


class ConfigTest(unittest.TestCase):
    def test_fuzzy_cutoff_comes_from_thresholds_file(self):
        self.assertEqual(config.thresholds().fuzzy_cutoff, 0.88)
        self.assertEqual(config.thresholds_path().name, "esikler.toml")

    def test_data_dir_can_be_overridden_by_environment(self):
        with tempfile.TemporaryDirectory() as tmp:
            (pathlib.Path(tmp) / "config").mkdir()
            (pathlib.Path(tmp) / "config" / "esikler.toml").write_text("fuzzy_cutoff = 0.5\n", encoding="utf-8")
            with mock.patch.dict(os.environ, {"NUTRISCAN_DATA_DIR": tmp}):
                self.assertEqual(config.data_dir(), pathlib.Path(tmp))
                self.assertEqual(config.thresholds().fuzzy_cutoff, 0.5)

    def test_dictionary_uses_configured_cutoff(self):
        self.assertEqual(Dictionary().fuzzy_cutoff, config.thresholds().fuzzy_cutoff)
        self.assertEqual(Dictionary(fuzzy_cutoff=0.95).fuzzy_cutoff, 0.95)


class OutcomeTest(unittest.TestCase):
    def test_four_outcomes_with_turkish_labels(self):
        self.assertEqual([o.value for o in Outcome], ["Engel bulunmadı", "Doğrulanamadı", "Dikkat", "Uygun değil"])

    def test_severity_order(self):
        order = sorted(Outcome, key=lambda o: o.severity)
        self.assertEqual(order, [Outcome.NO_ISSUE_FOUND, Outcome.UNVERIFIED, Outcome.CAUTION, Outcome.NOT_SUITABLE])

    def test_rule_file_label_maps_to_api_code(self):
        self.assertIs(Outcome("Uygun değil"), Outcome.NOT_SUITABLE)
        self.assertEqual(codes.outcome_to_api("Dikkat"), "CAUTION")
        self.assertEqual(codes.rule_type_to_api("icerebilir"), "may_contain")
        self.assertEqual(codes.source_kind_to_api("ekip_karari"), "team_decision")

    def test_unknown_code_is_an_error_not_a_guess(self):
        with self.assertRaises(KeyError):
            codes.rule_type_to_api("bilinmeyen")


if __name__ == "__main__":
    unittest.main()
