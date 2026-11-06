"""Small, reproducible metrics for iterative local OCR evaluation."""

from __future__ import annotations

import unicodedata
from dataclasses import dataclass


def normalize_ocr_text(value: str) -> str:
    """Normalize Unicode and whitespace without hiding recognition mistakes."""

    normalized = unicodedata.normalize("NFKC", value)
    return " ".join(normalized.split()).casefold()


def edit_distance(reference: str, prediction: str) -> int:
    """Return Levenshtein distance using linear memory."""

    previous = list(range(len(prediction) + 1))
    for row, reference_character in enumerate(reference, start=1):
        current = [row]
        for column, prediction_character in enumerate(prediction, start=1):
            current.append(
                min(
                    current[-1] + 1,
                    previous[column] + 1,
                    previous[column - 1]
                    + (reference_character != prediction_character),
                )
            )
        previous = current
    return previous[-1]


def character_error_rate(reference: str, prediction: str) -> float:
    """Measure normalized OCR edits per reference character."""

    expected = normalize_ocr_text(reference)
    actual = normalize_ocr_text(prediction)
    if not expected:
        return 0.0 if not actual else 1.0
    return edit_distance(expected, actual) / len(expected)


@dataclass(frozen=True, slots=True)
class OCREvaluation:
    sample_count: int
    exact_matches: int
    total_reference_characters: int
    total_edits: int

    @property
    def exact_match_rate(self) -> float:
        return self.exact_matches / self.sample_count if self.sample_count else 0.0

    @property
    def character_error_rate(self) -> float:
        if not self.total_reference_characters:
            return 0.0 if not self.total_edits else 1.0
        return self.total_edits / self.total_reference_characters


def evaluate_ocr_samples(samples: list[tuple[str, str]]) -> OCREvaluation:
    """Aggregate corpus-level OCR metrics without averaging tiny samples equally."""

    matches = 0
    characters = 0
    edits = 0
    for reference, prediction in samples:
        expected = normalize_ocr_text(reference)
        actual = normalize_ocr_text(prediction)
        matches += expected == actual
        characters += len(expected)
        edits += edit_distance(expected, actual)
    return OCREvaluation(len(samples), matches, characters, edits)
