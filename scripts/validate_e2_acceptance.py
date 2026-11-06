"""Validate reproducible evidence against the Phase E2 acceptance policy."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from document_converter.intelligence.model_manager import (
    LocalModelManager,
    ModelState,
)


DEFAULT_POLICY = Path("datasets/manifests/e2-acceptance-policy.json")


@dataclass(frozen=True, slots=True)
class AcceptanceCheck:
    name: str
    passed: bool
    actual: Any
    expected: Any


def _load_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def evaluate_evidence(
    policy: dict[str, Any],
    benchmark: dict[str, Any],
    corpus: dict[str, Any],
    gui: dict[str, Any],
    *,
    model_state: ModelState,
    model_version: str,
    model_pack_mib: float,
) -> list[AcceptanceCheck]:
    """Return every E2 check without hiding individual failures."""

    thresholds = policy["thresholds"]
    required_gui = policy["required_gui_evidence"]
    checks = [
        AcceptanceCheck(
            "model integrity",
            model_state == ModelState.READY,
            model_state.value,
            ModelState.READY.value,
        ),
        AcceptanceCheck(
            "model version",
            model_version == policy["required_model_version"],
            model_version,
            policy["required_model_version"],
        ),
        AcceptanceCheck(
            "model-pack size",
            model_pack_mib <= thresholds["maximum_model_pack_mib"],
            round(model_pack_mib, 2),
            f"<= {thresholds['maximum_model_pack_mib']} MiB",
        ),
        AcceptanceCheck(
            "synthetic CER",
            benchmark["character_error_rate"]
            <= thresholds["maximum_synthetic_character_error_rate"],
            benchmark["character_error_rate"],
            f"<= {thresholds['maximum_synthetic_character_error_rate']}",
        ),
        AcceptanceCheck(
            "warm inference",
            benchmark["elapsed_seconds_warm_average"]
            <= thresholds["maximum_warm_inference_seconds"],
            benchmark["elapsed_seconds_warm_average"],
            f"<= {thresholds['maximum_warm_inference_seconds']} s",
        ),
        AcceptanceCheck(
            "memory increase",
            benchmark["rss_delta_mib"]
            <= thresholds["maximum_rss_delta_mib"],
            benchmark["rss_delta_mib"],
            f"<= {thresholds['maximum_rss_delta_mib']} MiB",
        ),
        AcceptanceCheck(
            "official fixture count",
            corpus["sample_count"]
            >= thresholds["minimum_official_fixture_count"],
            corpus["sample_count"],
            f">= {thresholds['minimum_official_fixture_count']}",
        ),
        AcceptanceCheck(
            "official snippet recall",
            corpus["scored_substring_recall"]
            >= thresholds["minimum_official_snippet_recall"],
            corpus["scored_substring_recall"],
            f">= {thresholds['minimum_official_snippet_recall']}",
        ),
    ]
    checks.extend(
        AcceptanceCheck(
            f"GUI {name.replace('_', ' ')}",
            gui.get(name) is expected,
            gui.get(name),
            expected,
        )
        for name, expected in required_gui.items()
    )
    checks.append(
        AcceptanceCheck(
            "license review",
            policy["license_review"]["status"] == "reviewed-for-e2-baseline",
            policy["license_review"]["status"],
            "reviewed-for-e2-baseline",
        )
    )
    return checks


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--policy", type=Path, default=DEFAULT_POLICY)
    parser.add_argument(
        "--benchmark",
        type=Path,
        default=Path(".e2-results/network-benchmark.json"),
    )
    parser.add_argument(
        "--corpus",
        type=Path,
        default=Path(".e2-results/corpus-baseline.json"),
    )
    parser.add_argument(
        "--gui",
        type=Path,
        default=Path(".e2-results/gui-acceptance.json"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(".e2-results/e2-acceptance.json"),
    )
    arguments = parser.parse_args()

    policy = _load_object(arguments.policy)
    benchmark = _load_object(arguments.benchmark)
    corpus = _load_object(arguments.corpus)
    gui = _load_object(arguments.gui)
    manager = LocalModelManager()
    inspection = manager.inspect(policy["model_id"])
    model_directory = manager.model_directory(policy["model_id"])
    size = sum(
        path.stat().st_size
        for path in model_directory.rglob("*")
        if path.is_file()
    )
    checks = evaluate_evidence(
        policy,
        benchmark,
        corpus,
        gui,
        model_state=inspection.state,
        model_version=inspection.version,
        model_pack_mib=size / (1024 * 1024),
    )
    passed = all(check.passed for check in checks)
    report = {
        "checkpoint": policy["checkpoint"],
        "passed": passed,
        "checks": [
            {
                "name": check.name,
                "passed": check.passed,
                "actual": check.actual,
                "expected": check.expected,
            }
            for check in checks
        ],
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    for check in checks:
        marker = "PASS" if check.passed else "FAIL"
        print(f"[{marker}] {check.name}: {check.actual} ({check.expected})")
    print(f"E2 acceptance: {'PASSED' if passed else 'FAILED'}")
    print(arguments.output.resolve())
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
