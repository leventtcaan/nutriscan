"""Rule table → outcome per condition (C6). The decision comes only from the rule table (K5)."""
from .engine import evaluate, load_rules

__all__ = ["evaluate", "load_rules"]
