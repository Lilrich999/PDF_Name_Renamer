"""
name_detector.py
------------------
Finds a person's name inside raw OCR text.

Strategy (in order of preference):
1. Labeled fields -- look for lines like "Surname: ADJEI" and
   "Other Names: KWAME MENSAH", which is how most Ghanaian
   bio-data / ID forms are laid out.
2. Generic heuristic fallback -- if no labels are found, look for
   the first line that looks like a plausible, cleanly-capitalized
   name (2-4 words, each starting with a capital letter followed
   by lowercase letters, no digits, no stray single-letter
   fragments). This is intentionally strict: OCR garbage from
   handwriting or noisy scans often accidentally looks like a
   short word sequence, so a loose check would confidently assign
   wrong names instead of admitting it couldn't find one.

Returns None if nothing usable was found, so the caller can fall
back to random_names.generate_random_name() rather than guessing.
"""

import re
from typing import Optional
import config

_NAME_WORD = r"[A-Za-z][A-Za-z'\-]*"

# Used only by the generic (unlabeled) fallback -- requires proper
# Title Case (e.g. "Kwame", not "KWAME" or "kwame" or "og") so
# random OCR noise from handwriting is much less likely to pass.
_TITLE_CASE_WORD = r"[A-Z][a-z'\-]+"

MIN_WORD_LENGTH = 2


def detect_name(ocr_text: str) -> Optional[str]:
    if not ocr_text or not ocr_text.strip():
        return None

    labeled = _detect_from_labels(ocr_text)
    if labeled:
        return labeled

    return _detect_generic(ocr_text)


def _detect_from_labels(text: str) -> Optional[str]:
    surname = _find_labeled_value(text, config.SURNAME_LABELS)
    other_names = _find_labeled_value(text, config.OTHER_NAMES_LABELS)

    if surname and other_names:
        return _clean_name(f"{surname} {other_names}")
    if surname:
        return _clean_name(surname)
    if other_names:
        return _clean_name(other_names)
    return None


def _find_labeled_value(text: str, labels) -> Optional[str]:
    for label in labels:
        # Matches "Surname: ADJEI", "Surname - Adjei", "SURNAME  Adjei"
        pattern = rf"{re.escape(label)}\s*[:\-]?\s*({_NAME_WORD}(?:\s+{_NAME_WORD}){{0,3}})"
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            value = match.group(1).strip()
            if _looks_like_name(value):
                return value
    return None


def _detect_generic(text: str) -> Optional[str]:
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue

        words = line.split()
        if 1 < len(words) <= config.MAX_NAME_WORDS and _looks_like_title_case_name(line):
            return line

    return None


def _looks_like_name(candidate: str) -> bool:
    """General name-shape check: used for labeled fields (which may be ALL CAPS)."""
    if not candidate:
        return False

    words = candidate.split()
    if not (1 <= len(words) <= config.MAX_NAME_WORDS):
        return False

    for word in words:
        if len(word) < MIN_WORD_LENGTH:
            return False
        if any(char.isdigit() for char in word):
            return False
        if not re.fullmatch(_NAME_WORD, word):
            return False

    return True


def _looks_like_title_case_name(candidate: str) -> bool:
    """
    Stricter check used ONLY for the unlabeled generic fallback.
    Every word must be proper Title Case (e.g. 'Kwame') and at
    least MIN_WORD_LENGTH characters -- this filters out things
    like 'A te og a' or 'Jnm Eee Oe M' that are really OCR noise
    from handwriting, not an actual name.
    """
    if not candidate:
        return False

    words = candidate.split()
    if not (1 <= len(words) <= config.MAX_NAME_WORDS):
        return False

    for word in words:
        if len(word) < MIN_WORD_LENGTH:
            return False
        if any(char.isdigit() for char in word):
            return False
        if not re.fullmatch(_TITLE_CASE_WORD, word):
            return False

    return True


def _clean_name(raw_name: str) -> str:
    """Title-case and collapse whitespace, e.g. 'ADJEI  KWAME' -> 'Adjei Kwame'."""
    words = raw_name.split()
    return " ".join(word.capitalize() for word in words)