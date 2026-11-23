"""Shared domain vocabulary. Contract file: changes are announced to the team first (PLAN.md, rule 4)."""
from enum import Enum


class Outcome(str, Enum):
    """The four outcomes (AGENTS.md red line 2). Values are the exact labels used in the rule table."""

    NO_ISSUE_FOUND = "Engel bulunmadı"
    UNVERIFIED = "Doğrulanamadı"
    CAUTION = "Dikkat"
    NOT_SUITABLE = "Uygun değil"

    @property
    def severity(self) -> int:
        return _SEVERITY[self]


_SEVERITY = {Outcome.NO_ISSUE_FOUND: 0, Outcome.UNVERIFIED: 1, Outcome.CAUTION: 2, Outcome.NOT_SUITABLE: 3}

# Severity by rule-table label, for code that still compares plain strings.
SEVERITY_BY_LABEL = {o.value: o.severity for o in Outcome}
