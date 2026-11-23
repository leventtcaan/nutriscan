"""One label through the steps in order: split (C3) → match (C4) → evaluate (C6).

The API (#17) and the evaluation scripts call this same function, so what we measure is what we ship (NFR-8).
"""
from dataclasses import dataclass

from .matching import Dictionary, Match
from .rules import evaluate, load_rules
from .text import Mention, flatten, split_label


@dataclass
class AnalysisResult:
    matched: list          # [(Mention, Match)] for ingredient mentions, sub-ingredients included
    may_matched: list      # [(Mention, Match)] for "may contain" mentions
    results: dict          # condition id → {"sonuc": ..., "kurallar": [...]}


def match_all(dictionary: Dictionary, mentions: list[Mention]) -> list[tuple[Mention, Match]]:
    out = []
    for m in flatten(mentions):
        x = dictionary.match(m.norm)
        if x.method == "unknown" and m.children and all(dictionary.match(c.norm).method == "e_code" for c in m.children):
            x = Match(method="function_label")      # "renklendirici (E102)": the head is a function name
        out.append((m, x))
    return out


def analyze(ingredients_text: str, nutrition: dict, liquid: bool, conditions: list[str],
            dictionary: Dictionary | None = None, rules: list | None = None) -> AnalysisResult:
    dictionary = dictionary or Dictionary()
    rules = rules if rules is not None else load_rules()
    mentions, may, full = split_label(ingredients_text)
    matched, may_matched = match_all(dictionary, mentions), match_all(dictionary, may)
    results = evaluate(dictionary, matched, may_matched, full, nutrition, liquid, conditions, rules)
    return AnalysisResult(matched, may_matched, results)
