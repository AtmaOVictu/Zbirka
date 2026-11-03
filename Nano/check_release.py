#!/usr/bin/env python3
"""Fail-closed VBL candidate preflight and independent review gate.

Validates a release directory's source files, version metadata, register JSONL
records, JSON schemas, integrity manifest, and independent-review attestation.
A local PASS is not legal review, provenance authentication, publication, or proof
that a reviewer is independent; those require external human evidence.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError:  # make the missing optional validator an explicit preflight failure
    Draft202012Validator = None  # type: ignore[assignment,misc]
    FormatChecker = None  # type: ignore[assignment,misc]

SCHEMA_DIR = Path(__file__).resolve().parent / "schema"
REQUIRED_FILES = (
    "LICENSE.md",
    "REGISTER-NEIMENOVANIH.jsonl",
    "REGISTER-PADCEV.jsonl",
    "release-manifest.json",
    "independent-review.json",
    "RELEASE-REVIEW-TEMPLATE.json",
)
REGISTER_SCHEMAS = {
    "REGISTER-NEIMENOVANIH.jsonl": "register-neimenovani.schema.json",
    "REGISTER-PADCEV.jsonl": "register-padcev.schema.json",
}
UI_CONTAMINATION = (
    "Find definitions and references for functions and other symbols in this file by clicking a symbol below",
    "Filter symbols",
    "Symbols\n",
)
SECTION_HEADINGS = tuple(
    f"## §{number} {heading}"
    for number, heading in (
        (0, "What this door covers"), (1, "Grant"), (2, "The ledger condition"),
        (3, "The extraction clause"), (4, "The angel clause"),
        (5, "No perfection claimed"), (6, "The closed layers stay closed"),
        (7, "All else reserved"), (8, "Superiority and the record"),
        (9, "The ethics condition"), (10, "The change clause"),
        (11, "Severability"), (12, "The marked letters"), (13, "Regeneration"),
    )
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_relative_file(root: Path, relative: Any) -> Path | None:
    """Resolve a manifest path without permitting traversal or symlink escapes."""
    if not isinstance(relative, str) or not relative or "\\" in relative:
        return None
    rel = PurePosixPath(relative)
    if rel.is_absolute() or any(part in ("", ".", "..") for part in rel.parts):
        return None
    candidate = root.joinpath(*rel.parts)
    try:
        candidate.resolve(strict=True).relative_to(root.resolve(strict=True))
    except (OSError, ValueError):
        return None
    return candidate if candidate.is_file() else None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("release_dir", type=Path, help="candidate release directory")
    args = parser.parse_args()
    root: Path = args.release_dir.resolve()
    results: list[tuple[str, bool, str]] = []

    def record(test_id: str, ok: bool, detail: str) -> None:
        results.append((test_id, ok, detail))
        print(f"{'PASS' if ok else 'FAIL'} {test_id}: {detail}")

    if not root.is_dir():
        print(f"FAIL VBL-PRE-000: release directory does not exist: {root}")
        return 2

    missing = [name for name in REQUIRED_FILES if not (root / name).is_file()]
    record("VBL-PRE-001", not missing,
           "release inputs present" if not missing else "missing: " + ", ".join(missing))

    license_path = root / "LICENSE.md"
    text = ""
    raw = b""
    if not license_path.is_file():
        record("VBL-PRE-002", False, "candidate LICENSE.md is absent")
    else:
        try:
            raw = license_path.read_bytes()
            text = raw.decode("utf-8", errors="strict")
            record("VBL-PRE-002", True,
                   f"candidate decodes as UTF-8; sha256={sha256_bytes(raw)}")
        except UnicodeDecodeError as exc:
            record("VBL-PRE-002", False, f"candidate is not valid UTF-8: {exc}")

    if text:
        title_count = text.count("VBL — VERIFICATION BEFORE ASSERTION LICENSE")
        record("VBL-PRE-003", title_count == 1,
               f"canonical title count={title_count}; expected 1")
        debris = [needle for needle in UI_CONTAMINATION if needle in text]
        relative_history = bool(re.search(r"(?m)^\s*\d+\s+(minutes?|hours?|days?)\s+ago\s*$", text))
        record("VBL-PRE-004", not debris and not relative_history,
               "no known page-scrape debris" if not debris and not relative_history else
               "page/UI capture debris detected: " + ", ".join(repr(d) for d in debris) +
               ("; relative timestamps detected" if relative_history else ""))
        missing_sections = [heading for heading in SECTION_HEADINGS if heading not in text]
        record("VBL-PRE-005", not missing_sections,
               "all §0–§13 headings present" if not missing_sections else
               "missing headings: " + "; ".join(missing_sections))
        replacement_count = raw.count(b"\xef\xbf\xbd")
        record("VBL-PRE-006", replacement_count == 0,
               "no UTF-8 replacement-character byte sequence" if replacement_count == 0 else
               f"found {replacement_count} replacement-character sequence(s)")
    else:
        for test_id, detail in (
            ("VBL-PRE-003", "cannot inspect title without readable source"),
            ("VBL-PRE-004", "cannot inspect source capture without readable source"),
            ("VBL-PRE-005", "cannot inspect section headings without readable source"),
            ("VBL-PRE-006", "cannot inspect bytes without readable source"),
        ):
            record(test_id, False, detail)

    schemas: dict[str, dict[str, Any]] = {}
    schemas_valid = Draft202012Validator is not None
    if not schemas_valid:
        record("VBL-PRE-007", False, "install requirements-dev.txt; jsonschema validator unavailable")
    else:
        for filename in (*REGISTER_SCHEMAS.values(), "release-manifest.schema.json", "independent-review.schema.json"):
            path = SCHEMA_DIR / filename
            try:
                schema = json.loads(path.read_text(encoding="utf-8"))
                Draft202012Validator.check_schema(schema)
                schemas[filename] = schema
            except Exception as exc:
                schemas_valid = False
                record(f"VBL-PRE-007-{filename}", False, f"schema cannot be loaded/validated: {exc}")
        if schemas_valid:
            record("VBL-PRE-007", True, f"{len(schemas)} JSON schemas are valid Draft 2020-12 schemas")

    all_ids: dict[str, str] = {}
    correction_links: list[tuple[str, str, str]] = []
    for filename, schema_name in REGISTER_SCHEMAS.items():
        path = root / filename
        if not path.is_file():
            record(f"VBL-PRE-JSONL-{filename}", False, "register is absent")
            continue
        try:
            content = path.read_bytes().decode("utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            record(f"VBL-PRE-JSONL-{filename}", False, f"not valid UTF-8: {exc}")
            continue
        schema = schemas.get(schema_name)
        errors: list[str] = []
        live_count = 0
        headers: list[tuple[int, dict[str, Any]]] = []
        first_record_line: int | None = None
        for line_no, line in enumerate(content.splitlines(), start=1):
            if not line.strip():
                continue
            try:
                value = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"line {line_no}: invalid JSON: {exc.msg}")
                continue
            if not isinstance(value, dict):
                errors.append(f"line {line_no}: row must be a JSON object")
                continue
            if first_record_line is None:
                first_record_line = line_no
            if schema is not None:
                validator = Draft202012Validator(schema, format_checker=FormatChecker())
                row_errors = sorted(validator.iter_errors(value), key=lambda err: list(err.absolute_path))
                errors.extend(f"line {line_no}: {err.message}" for err in row_errors[:4])
            if value.get("record_type") == "register":
                headers.append((line_no, value))
                continue
            if value.get("status") == "TEMPLATE" or str(value.get("record_id", "")).startswith("TEMPLATE-"):
                errors.append(f"line {line_no}: template/example rows are not allowed in a live register")
                continue
            record_id = value.get("record_id")
            if isinstance(record_id, str) and record_id:
                if record_id in all_ids:
                    errors.append(f"line {line_no}: duplicate record_id {record_id!r} across live registers")
                else:
                    all_ids[record_id] = filename
            corrected_id = value.get("corrects_record_id")
            if corrected_id is not None:
                correction_links.append((filename, record_id if isinstance(record_id, str) else "", corrected_id))
            live_count += 1
        if not headers and live_count == 0 and not errors:
            errors.append("register header is required even when the register contains zero live entries")
        elif len(headers) != 1:
            errors.append(f"expected exactly one register header; found {len(headers)}")
        elif headers[0][0] != first_record_line:
            errors.append(f"register header must be the first non-empty record (line {headers[0][0]})")
        else:
            declared_count = headers[0][1].get("entries_recorded")
            if declared_count != live_count:
                errors.append(f"header declares {declared_count!r} entries; found {live_count} live rows")
        record(f"VBL-PRE-JSONL-{filename}", not errors,
               f"one first-line header declares {live_count} schema-valid live rows" if not errors else "; ".join(errors[:8]))

    correction_errors = [
        f"{filename}: correction {record_id!r} has missing or self-referential target {target!r}"
        for filename, record_id, target in correction_links
        if not target or target == record_id or target not in all_ids
    ]
    record("VBL-PRE-CORRECTIONS", not correction_errors,
           "all corrections preserve and reference an existing different record" if not correction_errors else
           "; ".join(correction_errors[:8]))

    manifest_path = root / "release-manifest.json"
    manifest: dict[str, Any] = {}
    if not manifest_path.is_file():
        record("VBL-PRE-MANIFEST", False, "release-manifest.json is absent")
    else:
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest_schema = schemas.get("release-manifest.schema.json")
            schema_errors = [] if manifest_schema is None else sorted(
                Draft202012Validator(manifest_schema, format_checker=FormatChecker()).iter_errors(manifest),
                key=lambda err: list(err.absolute_path),
            )
            if not isinstance(manifest, dict):
                raise ValueError("manifest root must be an object")
            elif schema_errors:
                raise ValueError("; ".join(err.message for err in schema_errors[:5]))
            if manifest.get("release_status") != "CANDIDATE_NOT_RELEASED":
                raise ValueError("release_status must remain CANDIDATE_NOT_RELEASED; publication is an explicit human action")
            entries = manifest.get("files")
            entry_errors: list[str] = []
            seen_paths: set[str] = set()
            expected_files = {"LICENSE.md", "RELEASE-REVIEW-TEMPLATE.json", *REGISTER_SCHEMAS.keys()}
            if not isinstance(entries, list):
                raise ValueError("manifest files must be an array")
            for entry in entries:
                if not isinstance(entry, dict):
                    entry_errors.append("manifest file entries must be objects")
                    continue
                rel = entry.get("path")
                if not isinstance(rel, str):
                    entry_errors.append(f"unsafe or missing path {rel!r}")
                    continue
                if rel in seen_paths:
                    entry_errors.append(f"duplicate manifest path {rel!r}")
                    continue
                seen_paths.add(rel)
                if "\\" in rel:
                    entry_errors.append(f"unsafe or missing path {rel!r}")
                    continue
                candidate = safe_relative_file(root, rel)
                if candidate is None:
                    entry_errors.append(f"unsafe or missing path {rel!r}")
                    continue
                data = candidate.read_bytes()
                if len(data) != entry.get("size") or sha256_bytes(data) != entry.get("sha256"):
                    entry_errors.append(f"size/hash mismatch for {rel!r}")
            absent_entries = expected_files - seen_paths
            if absent_entries:
                entry_errors.append("manifest omits required payloads: " + ", ".join(sorted(absent_entries)))
            record("VBL-PRE-MANIFEST", not entry_errors,
                   f"{len(entries)} payload files match size and SHA-256" if not entry_errors else
                   "; ".join(entry_errors[:8]))
        except (OSError, UnicodeError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
            record("VBL-PRE-MANIFEST", False, f"manifest invalid: {exc}")

    if isinstance(manifest, dict) and text:
        declared_version = manifest.get("version")
        heading_versions = re.findall(r"(?m)^Version\s+([^\s·—]+)", text)
        marker_count = text.count("## Machine record")
        machine_records: list[dict[str, Any]] = []
        if marker_count == 1:
            section = text.split("## Machine record", 1)[1]
            blocks = re.findall(r"```json\s*(\{.*?\})\s*```", section, re.DOTALL)
            for block in blocks:
                try:
                    value = json.loads(block)
                    if isinstance(value, dict):
                        machine_records.append(value)
                except json.JSONDecodeError:
                    pass
        machine_record = machine_records[0] if len(machine_records) == 1 else {}
        predecessor = machine_record.get("predecessor")
        machine_predecessor = predecessor.get("version") if isinstance(predecessor, dict) else None
        metadata_ok = (
            isinstance(declared_version, str) and
            heading_versions == [declared_version] and
            marker_count == 1 and len(machine_records) == 1 and
            machine_record.get("version") == declared_version and
            machine_record.get("date") == manifest.get("date") and
            machine_predecessor == manifest.get("predecessor")
        )
        record("VBL-PRE-VERSION", metadata_ok,
               f"version, date, and predecessor {declared_version!r} agree across header, machine record, and manifest"
               if metadata_ok else
               "manifest version/date/predecessor must exactly match one human header and one machine record")
    else:
        record("VBL-PRE-VERSION", False, "cannot compare manifest version with unreadable license/manifest")

    review_path = root / "independent-review.json"
    if not review_path.is_file():
        record("VBL-PRE-REVIEW", False, "independent-review.json is absent")
    else:
        try:
            review = json.loads(review_path.read_text(encoding="utf-8"))
            review_schema = schemas.get("independent-review.schema.json")
            schema_errors = [] if review_schema is None else sorted(
                Draft202012Validator(review_schema, format_checker=FormatChecker()).iter_errors(review),
                key=lambda err: list(err.absolute_path),
            )
            if not isinstance(review, dict):
                raise ValueError("review attestation root must be an object")
            elif schema_errors:
                raise ValueError("; ".join(err.message for err in schema_errors[:5]))
            manifest_digest = sha256_bytes(manifest_path.read_bytes()) if manifest_path.is_file() else ""
            license_digest = sha256_bytes(raw) if raw else ""
            reviewer_id = review.get("reviewer_id", "")
            executor_id = review.get("executor_id", "")
            independent = (isinstance(reviewer_id, str) and isinstance(executor_id, str) and
                           reviewer_id.strip().casefold() != executor_id.strip().casefold())
            accepted = review.get("decision") == "APPROVED"
            no_pending_placeholders = all(
                isinstance(review.get(field), str) and
                not review[field].strip().upper().startswith("PENDING")
                for field in ("reviewer_id", "scope", "conflict_statement", "evidence_uri")
            )
            findings_clear = not review.get("findings")
            refs_match = (
                review.get("manifest_sha256") == manifest_digest and
                review.get("license_sha256") == license_digest and
                isinstance(manifest, dict) and
                manifest.get("release_status") == "CANDIDATE_NOT_RELEASED"
            )
            ok = independent and accepted and refs_match and no_pending_placeholders and findings_clear
            reasons = []
            if not independent:
                reasons.append("reviewer_id must differ from executor_id (case-insensitive)")
            if not accepted:
                reasons.append("decision must be APPROVED")
            if not no_pending_placeholders:
                reasons.append("review attestation contains pending placeholder fields")
            if not findings_clear:
                reasons.append("APPROVED review must have no unresolved findings")
            if not refs_match:
                reasons.append("review must bind current manifest and license SHA-256")
            record("VBL-PRE-REVIEW", ok,
                   "review identity differs and attestation binds current bytes" if ok else "; ".join(reasons))
        except (OSError, UnicodeError, json.JSONDecodeError, TypeError, ValueError) as exc:
            record("VBL-PRE-REVIEW", False, f"review attestation invalid: {exc}")

    failed = sum(not ok for _, ok, _ in results)
    passed = len(results) - failed
    print(f"\nSUMMARY: {passed} passed, {failed} failed, {len(results)} total")
    print("LIMIT: local checks cannot authenticate identities, prove reviewer independence, validate rights, or constitute publication.")
    return 0 if failed == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
