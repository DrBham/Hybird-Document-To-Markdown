"""Download and verify the small, attributed Phase E2 evaluation corpus."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from urllib.request import urlopen


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("datasets/manifests/e2-paddleocr-smoke.json"),
    )
    parser.add_argument("--output", type=Path, default=Path(".e2-corpus"))
    arguments = parser.parse_args()
    manifest = json.loads(arguments.manifest.read_text(encoding="utf-8"))
    arguments.output.mkdir(parents=True, exist_ok=True)

    for sample in manifest["samples"]:
        target = arguments.output / sample["filename"]
        if not target.is_file() or _sha256(target) != sample["sha256"]:
            with urlopen(sample["url"], timeout=60) as response:
                target.write_bytes(response.read())
        actual = _sha256(target)
        if actual != sample["sha256"]:
            target.unlink(missing_ok=True)
            raise ValueError(
                f"checksum mismatch for {sample['id']}: {actual}"
            )
        print(f"verified {sample['id']}: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
