"""Where data lives and which thresholds apply. Nothing else in the package hardcodes a path or a threshold."""
import os
import pathlib
import tomllib
from dataclasses import dataclass

_REPO_DATA = pathlib.Path(__file__).resolve().parents[2] / "data"
_DEFAULT_RULES_FILE = "kurallar_v0.csv"


@dataclass(frozen=True)
class Thresholds:
    fuzzy_cutoff: float


def data_dir() -> pathlib.Path:
    """Knowledge-base folder; NUTRISCAN_DATA_DIR overrides the repository's data/ folder."""
    return pathlib.Path(os.environ.get("NUTRISCAN_DATA_DIR", _REPO_DATA))


def thresholds_path() -> pathlib.Path:
    return data_dir() / "config" / "esikler.toml"


def thresholds() -> Thresholds:
    with open(thresholds_path(), "rb") as f:
        values = tomllib.load(f)
    return Thresholds(fuzzy_cutoff=float(values["fuzzy_cutoff"]))


def rules_path() -> pathlib.Path:
    """Rule table file; NUTRISCAN_RULES_FILE overrides the file name inside data/kurallar/."""
    return data_dir() / "kurallar" / os.environ.get("NUTRISCAN_RULES_FILE", _DEFAULT_RULES_FILE)
