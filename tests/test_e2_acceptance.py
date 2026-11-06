import json
from pathlib import Path

from document_converter.intelligence.model_manager import ModelState
from scripts.validate_e2_acceptance import evaluate_evidence


POLICY_PATH = Path("datasets/manifests/e2-acceptance-policy.json")


def _evidence():
    policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
    benchmark = {
        "character_error_rate": 0.02,
        "elapsed_seconds_warm_average": 2.5,
        "rss_delta_mib": 250.0,
    }
    corpus = {"sample_count": 5, "scored_substring_recall": 1.0}
    gui = {
        "model_option_enabled": True,
        "conversion_succeeded": True,
        "local_analysis_rendered": True,
    }
    return policy, benchmark, corpus, gui


def test_e2_acceptance_policy_passes_complete_evidence():
    policy, benchmark, corpus, gui = _evidence()

    checks = evaluate_evidence(
        policy,
        benchmark,
        corpus,
        gui,
        model_state=ModelState.READY,
        model_version=policy["required_model_version"],
        model_pack_mib=19.1,
    )

    assert checks
    assert all(check.passed for check in checks)


def test_e2_acceptance_policy_reports_quality_failure():
    policy, benchmark, corpus, gui = _evidence()
    benchmark["character_error_rate"] = 0.20

    checks = evaluate_evidence(
        policy,
        benchmark,
        corpus,
        gui,
        model_state=ModelState.READY,
        model_version=policy["required_model_version"],
        model_pack_mib=19.1,
    )

    failed = [check.name for check in checks if not check.passed]
    assert failed == ["synthetic CER"]
