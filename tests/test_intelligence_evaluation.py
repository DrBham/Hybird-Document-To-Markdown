import pytest

from document_converter.intelligence.evaluation import (
    character_error_rate,
    edit_distance,
    evaluate_ocr_samples,
    normalize_ocr_text,
)


def test_normalization_handles_unicode_case_and_whitespace():
    assert normalize_ocr_text("  ROUTER\nＡ  ") == "router a"


def test_edit_distance_matches_known_example():
    assert edit_distance("kitten", "sitting") == 3


def test_character_error_rate_uses_normalized_reference_length():
    assert character_error_rate("router", "routex") == pytest.approx(1 / 6)


def test_corpus_evaluation_weights_by_character_count():
    result = evaluate_ocr_samples(
        [("Router A", "Router A"), ("Switch", "Switxh")]
    )

    assert result.sample_count == 2
    assert result.exact_matches == 1
    assert result.exact_match_rate == 0.5
    assert result.character_error_rate == pytest.approx(1 / 14)
