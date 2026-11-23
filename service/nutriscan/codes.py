"""Turkish values in data files ↔ English codes in the API (docs/tasarim/04-veri-modeli.md §3.1).

The only place where this translation happens. An unknown value raises KeyError instead of being guessed.
"""
from .types import Outcome

_RULE_TYPES = {"varlik": "presence", "icerebilir": "may_contain", "beyan": "claim", "miktar": "amount",
               "eksik_veri": "missing_data", "varsayilan": "default"}
_SOURCE_KINDS = {"mevzuat": "regulation", "klinik_kilavuz": "clinical_guideline", "efsa_gorusu": "efsa_opinion",
                 "ekip_karari": "team_decision"}


def outcome_to_api(label: str) -> str:
    return Outcome(label).name


def rule_type_to_api(value: str) -> str:
    return _RULE_TYPES[value]


def source_kind_to_api(value: str) -> str:
    return _SOURCE_KINDS[value]
