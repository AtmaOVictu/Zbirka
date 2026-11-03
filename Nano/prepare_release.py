#!/usr/bin/env python3
"""Stage an explicitly selected VBL license file as an unreleased candidate.

This utility never selects drafts automatically and never marks a candidate as
released or reviewed. Supply the source file and version metadata deliberately.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path

UI_CONTAMINATION = (
    "Find definitions and references for functions and other symbols in this file by clicking a symbol below",
    "Filter symbols",
    "Symbols\n",
)


def source_metadata(text: str) -> tuple[str, str, str | None]:
    """Extract and require one consistent human/machine version record."""
    headings = re.findall(r"(?m)^Version\s+([^\s·—]+)", text)
    if len(headings) != 1:
        raise ValueError(f"expected exactly one 'Version X' header; found {len(headings)}")
    marker = "## Machine record"
    if text.count(marker) != 1:
        raise ValueError(f"expected exactly one machine-record section; found {text.count(marker)}")
    section = text.split(marker, 1)[1]
    blocks = re.findall(r"```json\s*(\{.*?\})\s*```", section, re.DOTALL)
    if len(blocks) != 1:
        raise ValueError(f"expected exactly one JSON machine record; found {len(blocks)}")
    try:
        record = json.loads(blocks[0])
    except json.JSONDecodeError as exc:
        raise ValueError(f"machine record JSON is invalid: {exc}") from exc
    if not isinstance(record, dict) or not isinstance(record.get("version"), str):
        raise ValueError("machine record must be an object with a string version")
    machine_version = record["version"]
    if headings[0] != machine_version:
        raise ValueError(f"human version {headings[0]!r} disagrees with machine version {machine_version!r}")
    machine_date = record.get("date")
    predecessor = record.get("predecessor")
    predecessor_version = predecessor.get("version") if isinstance(predecessor, dict) else None
    return machine_version, machine_date, predecessor_version


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("license_source", type=Path, help="explicitly selected license candidate")
    parser.add_argument("release_dir", type=Path, help="candidate output directory")
    parser.add_argument("--version", help="must match the source license's human and machine version")
    parser.add_argument("--date", help="must match the source machine-record date; omit to derive it")
    parser.add_argument("--predecessor", help="must match the source machine-record predecessor")
    parser.add_argument("--source-commit", help="optional verified source commit SHA")
    parser.add_argument("--executor-id", required=True, help="stable reviewer/executor identity label")
    args = parser.parse_args()

    source = args.license_source.resolve()
    destination = args.release_dir.resolve()
    if not source.is_file():
        parser.error(f"license source does not exist: {source}")
    if not args.executor_id.strip():
        parser.error("executor identity must be non-empty")
    if args.source_commit and not re.fullmatch(r"[0-9a-fA-F]{40,64}", args.source_commit):
        parser.error("--source-commit must be a full 40–64 digit hexadecimal commit SHA")
    if destination.exists() and (not destination.is_dir() or any(destination.iterdir())):
        parser.error(f"destination is not an empty directory; refusing to overwrite candidate or user files: {destination}")
    if destination == source or destination in source.parents:
        parser.error("release directory cannot equal or contain the license source path")
    if args.date:
        try:
            from datetime import date
            date.fromisoformat(args.date)
        except ValueError:
            parser.error("--date must be an ISO calendar date, YYYY-MM-DD")

    data = source.read_bytes()
    try:
        text = data.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        parser.error(f"license source must be strict UTF-8: {exc}")
    if "VBL — VERIFICATION BEFORE ASSERTION LICENSE" not in text:
        parser.error("license source does not contain the VBL title; refusing to stage unrelated text")
    if "\ufffd" in text:
        parser.error("license source contains U+FFFD replacement characters")
    contamination = [item for item in UI_CONTAMINATION if item in text]
    if contamination or re.search(r"(?m)^\s*\d+\s+(minutes?|hours?|days?)\s+ago\s*$", text):
        parser.error("license source contains web/page-scrape contamination")
    try:
        source_version, source_date, source_predecessor = source_metadata(text)
    except ValueError as exc:
        parser.error(str(exc))
    if args.version and args.version != source_version:
        parser.error(f"requested version {args.version!r} does not match source version {source_version!r}")
    if args.date and args.date != source_date:
        parser.error(f"requested date {args.date!r} does not match source machine-record date {source_date!r}")
    if args.predecessor and args.predecessor != source_predecessor:
        parser.error(f"requested predecessor {args.predecessor!r} does not match source machine-record predecessor {source_predecessor!r}")
    args.version = source_version
    args.date = args.date or source_date
    args.predecessor = args.predecessor or source_predecessor

    destination.mkdir(parents=True, exist_ok=True)
    license_path = destination / "LICENSE.md"
    shutil.copyfile(source, license_path)
    (destination / "REGISTER-NEIMENOVANIH.jsonl").write_text(
        json.dumps({"record_type": "register", "entries_recorded": 0}, ensure_ascii=False) + chr(10),
        encoding="utf-8",
    )
    (destination / "REGISTER-PADCEV.jsonl").write_text(
        json.dumps({"record_type": "register", "entries_recorded": 0}, ensure_ascii=False) + chr(10),
        encoding="utf-8",
    )

    template_path = Path(__file__).resolve().parent / "RELEASE-REVIEW-TEMPLATE.json"
    if not template_path.is_file():
        parser.error(f"review template is missing: {template_path}")
    shutil.copyfile(template_path, destination / "RELEASE-REVIEW-TEMPLATE.json")

    payloads = []
    for path in (license_path, destination / "REGISTER-NEIMENOVANIH.jsonl",
                 destination / "REGISTER-PADCEV.jsonl", destination / "RELEASE-REVIEW-TEMPLATE.json"):
        payload = path.read_bytes()
        payloads.append({"path": path.name, "size": len(payload), "sha256": sha256(payload)})
    manifest = {
        "schema_version": "1.0.0",
        "release_status": "CANDIDATE_NOT_RELEASED",
        "version": args.version,
        "date": args.date,
        "predecessor": args.predecessor,
        "source_commit": args.source_commit,
        "files": payloads,
    }
    manifest_bytes = (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    manifest_path = destination / "release-manifest.json"
    manifest_path.write_bytes(manifest_bytes)
    review = {
        "schema_version": "1.0.0",
        "reviewer_id": "PENDING_INDEPENDENT_REVIEWER",
        "executor_id": args.executor_id,
        "decision": "NOT_PERFORMED",
        "reviewed_at": None,
        "scope": "Pending: independent source, schema, integrity, and release-readiness review.",
        "conflict_statement": "Pending: reviewer must disclose conflicts and independence basis.",
        "findings": [],
        "manifest_sha256": sha256(manifest_bytes),
        "license_sha256": sha256(data),
        "evidence_uri": "PENDING_EXTERNAL_REVIEW_EVIDENCE",
        "signature": None,
    }
    (destination / "independent-review.json").write_text(
        json.dumps(review, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Staged candidate directory: {destination}")
    print(f"Candidate version: {args.version}; status: CANDIDATE_NOT_RELEASED")
    print(f"License SHA-256: {sha256(data)}")
    print("Independent review: NOT_PERFORMED; release preflight must remain blocked.")
    print("Run: python check_release.py <candidate-directory>")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
