"""Label text → mentions: normalise Turkish text, split the ingredient list, separate 'may contain' statements."""
import re
from dataclasses import dataclass, field

_TR_LOWER = str.maketrans({"I": "ı", "İ": "i"})
_PERCENT = re.compile(r"%\s*\d+(?:[.,]\d+)?|\d+(?:[.,]\d+)?\s*%")
_E_CODE = re.compile(r"^e\s*-?\s*(\d{3,4})\s*([a-z])?(?:\s*\(?([ivx]+)\)?)?$")
_CLAIM = re.compile(r"^(glutensiz|laktozsuz|şeker ilavesiz|ilave şeker içermez|katkısız|koruyucu içermez)( ürün(dür)?)?$")
_MAY_CONTAIN = re.compile(r"(?:eser\s+miktarda\s+)?(.+?)\s+(?:içerebilir|bulunabilir)")


def normalize(text: str) -> str:
    """Turkish-aware lower case; drop percentages, quotes and edge punctuation; collapse spaces."""
    s = text.translate(_TR_LOWER).lower()
    s = _PERCENT.sub(" ", s)
    s = re.sub(r"[(\[]\s*[)\]]", " ", s)          # parentheses left empty after removing a percentage
    s = re.sub(r"[\"'“”‘’*•·]", " ", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip(" .;:-")


def e_code(norm: str):
    """'e 102', 'e-102', 'e450(i)' → 'E102', 'E450'; None if not an E-number."""
    m = _E_CODE.match(norm)
    if not m:
        return None
    return "E" + m.group(1) + (m.group(2) or "").upper()


@dataclass
class Mention:
    raw: str
    norm: str
    kind: str = "ingredient"          # ingredient | may_contain
    parent: str = ""                  # head text when the mention sits inside parentheses
    children: list = field(default_factory=list)


def _split_top(s: str):
    """Split on commas/semicolons that are not inside parentheses."""
    items, depth, cur = [], 0, ""
    for ch in s:
        if ch in "([":
            depth += 1
        elif ch in ")]":
            depth = max(0, depth - 1)
        if ch in ",;" and depth == 0:
            items.append(cur)
            cur = ""
        else:
            cur += ch
    items.append(cur)
    return [i.strip() for i in items if i.strip()]


def _mentions_from_list(text: str, kind: str, parent: str = ""):
    out = []
    for item in _split_top(text):
        m = re.match(r"^(.*?)\s*[(\[](.*)[)\]]\s*$", item)
        head, inner = (m.group(1), m.group(2)) if m else (item, "")
        if not head.strip() and inner:          # "(E102)" alone
            head, inner = inner, ""
        mention = Mention(raw=head.strip(), norm=normalize(head), kind=kind, parent=parent)
        if inner:
            mention.children = _mentions_from_list(inner, kind, parent=mention.norm)
        if mention.norm:
            out.append(mention)
    return out


def split_label(text: str):
    """Return (mentions, may_contain_mentions, full_normalised_text)."""
    body = re.sub(r"^\s*(içindekiler|i̇çindekiler|bileşenler)\s*:\s*", "", text.strip(), flags=re.I)
    main_parts, may = [], []
    for sentence in re.split(r"(?<=[.!])\s+", body):
        low = normalize(sentence)
        if _CLAIM.match(low):
            continue                       # a claim ("Glutensiz.") is not an ingredient; rules read it from full text
        if "içerebilir" in low or "bulunabilir" in low:
            mm = _MAY_CONTAIN.search(low)
            if mm:
                listed = re.sub(r"\s+ve\s+|\s+veya\s+", ",", mm.group(1))
                may.extend(_mentions_from_list(listed, "may_contain"))
        else:
            main_parts.append(sentence.rstrip("."))
    mentions = _mentions_from_list(", ".join(main_parts), "ingredient")
    return mentions, may, normalize(text)


def flatten(mentions):
    for m in mentions:
        yield m
        yield from flatten(m.children)
