#!/usr/bin/env python3
"""Read-only structural audit for the captured VBL register snapshots.

No network access, writes to the source repositories, or source mutation occurs.
Run: python verify_vbl_registers.py
The script expects the snapshots/ directory beside this file.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
SNAP = ROOT / "registry-snapshots"
results: list[dict[str, Any]] = []


def add(check: str, status: str, detail: str, **extra: Any) -> None:
    results.append({"check": check, "status": status, "detail": detail, **extra})


def read(path: Path) -> bytes:
    return path.read_bytes()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_jsonl(path: Path) -> list[dict[str, Any]]:
    out = []
    for number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not raw_line.strip():
            continue
        try:
            value = json.loads(raw_line)
        except json.JSONDecodeError as exc:
            add(f"jsonl:{path.relative_to(ROOT)}:{number}", "FAIL", f"Invalid JSON: {exc}")
            continue
        if not isinstance(value, dict):
            add(f"jsonl:{path.relative_to(ROOT)}:{number}", "FAIL", "JSONL row is not an object")
            continue
        out.append(value)
    return out


def audit_todo_app() -> None:
    base = SNAP / "todo-app"
    manifest_path = base / "LICENSE-MANIFEST"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        add("todo-app:LICENSE-MANIFEST:read", "FAIL", f"Manifest could not be read as UTF-8 JSON: {exc}")
        manifest = {}
    all_match = True
    entries = manifest.get("files", []) if isinstance(manifest, dict) else []
    if not isinstance(entries, list) or not entries:
        add("todo-app:LICENSE-MANIFEST:shape", "FAIL", "Manifest 'files' must be a non-empty array.")
        # Still inspect register structure below, but do not claim manifest success.
        entries = []
        all_match = False
    base_resolved = base.resolve()
    for entry in entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
            all_match = False
            add("manifest:entry-shape", "FAIL", "Manifest entry must be an object with a string path.")
            continue
        rel = Path(entry["path"])
        candidate = (base / rel).resolve()
        # Treat the captured manifest as untrusted input: never follow absolute or parent-traversal paths.
        if rel.is_absolute() or ".." in rel.parts or (candidate != base_resolved and base_resolved not in candidate.parents):
            all_match = False
            add(f"manifest:{entry['path']}", "FAIL", "Manifest path escapes the captured snapshot root.")
            continue
        if not candidate.is_file():
            all_match = False
            add(f"manifest:{entry['path']}", "FAIL", "Manifest-listed file absent from captured snapshot")
            continue
        content = read(candidate)
        digest = sha256(content)
        size = len(content)
        ok = digest == entry.get("sha256") and size == entry.get("size")
        all_match &= ok
        add(
            f"manifest:{entry['path']}", "PASS" if ok else "FAIL",
            "Captured bytes match manifest" if ok else "Size or SHA-256 mismatch",
            bytes=size, sha256=digest, expected_bytes=entry.get("size"), expected_sha256=entry.get("sha256"),
        )
    if all_match and entries:
        add("todo-app:LICENSE-MANIFEST", "PASS", f"All {len(entries)} manifest entries match captured byte sizes and SHA-256 values.")

    true_record_ids: list[tuple[str, str]] = []
    for rel in ("REGISTER-NEIMENOVANIH.jsonl", "REGISTER-PADCEV.jsonl"):
        records = parse_jsonl(base / rel)
        headers = [r for r in records if r.get("record_type") == "register"]
        actual = [r for r in records if r.get("record_type") != "register" and r.get("status") != "TEMPLATE"]
        declared = headers[0].get("entries_recorded") if len(headers) == 1 else None
        ok = len(headers) == 1 and declared == len(actual)
        add(
            f"todo-app:{rel}:count", "PASS" if ok else "FAIL",
            f"Header declares {declared!r}; structurally present non-template entries: {len(actual)}.",
            header_records=len(headers), actual_entries=len(actual),
        )
        for row in actual:
            rid = row.get("record_id")
            if isinstance(rid, str) and rid:
                true_record_ids.append((rel, rid))

    permission_text = (base / "canon" / "DOVOLJENJA.md").read_text(encoding="utf-8")
    # Count actual grants only when a dated entry heading is present; the generic format example is excluded.
    actual_permission_entries = [line for line in permission_text.splitlines()
                                 if line.startswith("### Permission — ") and "YYYY-MM-DD" not in line]
    add("todo-app:permissions", "PASS" if not actual_permission_entries else "REVIEW",
        f"Recorded permission entries in captured file: {len(actual_permission_entries)}; text says no permissions are recorded yet.",
        actual_permission_entries=len(actual_permission_entries))

    seen: dict[str, str] = {}
    duplicates = []
    for path, rid in true_record_ids:
        if rid in seen:
            duplicates.append((rid, seen[rid], path))
        else:
            seen[rid] = path
    add("todo-app:record-id-uniqueness", "PASS" if not duplicates else "FAIL",
        f"Checked actual entries only; {len(true_record_ids)} actual entry IDs, {len(duplicates)} duplicates.",
        duplicate_ids=duplicates)


def audit_cookbook() -> None:
    base = SNAP / "cookbook"
    true_ids: list[tuple[str, str]] = []
    for rel in ("REGISTER-NEIMENOVANIH.jsonl", "REGISTER-PADCEV.jsonl"):
        rows = parse_jsonl(base / rel)
        placeholders = [r for r in rows if r.get("status") == "TEMPLATE" or str(r.get("record_id", "")).startswith("TEMPLATE-")]
        actual = [r for r in rows if r not in placeholders]
        add(f"cookbook:{rel}:template", "WARN" if placeholders else "PASS",
            f"Rows: {len(rows)}; template rows: {len(placeholders)}; actual evidence rows: {len(actual)}. Template rows are not evidence.",
            rows=len(rows), templates=len(placeholders), actual_entries=len(actual))
        for row in actual:
            rid = row.get("record_id")
            if isinstance(rid, str) and rid:
                true_ids.append((rel, rid))

    sums = (base / "SHA256SUMS.txt").read_text(encoding="utf-8").splitlines()
    digest_lines = [line for line in sums if line.strip() and not line.lstrip().startswith("(")]
    unverified = [line for line in digest_lines if line.startswith("UNVERIFIED")]
    valid_digest_lines = [line for line in digest_lines if not line.startswith("UNVERIFIED")]
    all_nine_marked = len(unverified) == 9 and len(valid_digest_lines) == 0
    add("cookbook:SHA256SUMS", "BLOCKED" if all_nine_marked else "REVIEW",
        f"Digest entries: {len(digest_lines)}; literal UNVERIFIED placeholders: {len(unverified)}; actual digest entries: {len(valid_digest_lines)}.",
        unverified_placeholders=len(unverified), actual_digest_entries=len(valid_digest_lines))

    seen: dict[str, str] = {}
    duplicates = []
    for path, rid in true_ids:
        if rid in seen:
            duplicates.append((rid, seen[rid], path))
        else:
            seen[rid] = path
    add("cookbook:record-id-uniqueness", "PASS" if not duplicates else "FAIL",
        f"Checked actual evidence rows only; {len(true_ids)} actual entry IDs, {len(duplicates)} duplicates.",
        duplicate_ids=duplicates)


def main() -> int:
    results.clear()
    audit_todo_app()
    audit_cookbook()
    report = {
        "audit": "VBL registry read-only audit",
        "audit_date": "2026-10-25",
        "scope": "Captured GitHub file snapshots only; no remote changes, application tests, or ZPV execution.",
        "summary": {
            status: sum(1 for item in results if item["status"] == status)
            for status in ("PASS", "WARN", "BLOCKED", "REVIEW", "FAIL")
        },
        "results": results,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    (ROOT / "registry-audit-result.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    # Do not return success while a required verification is blocked.
    if any(item["status"] == "FAIL" for item in results):
        return 1
    if any(item["status"] == "BLOCKED" for item in results):
        return 2
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
