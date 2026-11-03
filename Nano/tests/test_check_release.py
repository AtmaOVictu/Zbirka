"""Regression and adversarial tests for the VBL release gate."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "check_release.py"
PREPARER = ROOT / "prepare_release.py"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def valid_source(version: str = "10.0.0") -> str:
    record = {"version": "10.0.0", "date": "2026-10-26",
              "predecessor": {"version": "10.0.0-rc1", "date": "2026-10-25"}}
    return "\n".join([
        "VBL — VERIFICATION BEFORE ASSERTION LICENSE", f"Version {version} · October 26, 2026",
        "## Machine record", "```json", json.dumps(record), "```", "",
    ])


def release_fixture(root: Path) -> None:
    headings = [
        "## §0 What this door covers", "## §1 Grant", "## §2 The ledger condition",
        "## §3 The extraction clause", "## §4 The angel clause",
        "## §5 No perfection claimed", "## §6 The closed layers stay closed",
        "## §7 All else reserved", "## §8 Superiority and the record",
        "## §9 The ethics condition", "## §10 The change clause", "## §11 Severability",
        "## §12 The marked letters", "## §13 Regeneration",
    ]
    machine_record = {"version": "2.6", "date": "2026-10-23",
                      "predecessor": {"version": "2.5", "date": "2026-10-22"}}
    license_text = "\n".join([
        "VBL — VERIFICATION BEFORE ASSERTION LICENSE", "Version 2.6 · October 23, 2026",
        *headings, "## Machine record", "```json", json.dumps(machine_record), "```", "",
    ])
    license_bytes = license_text.encode("utf-8")
    (root / "LICENSE.md").write_bytes(license_bytes)
    template_data = (ROOT / "RELEASE-REVIEW-TEMPLATE.json").read_bytes()
    (root / "RELEASE-REVIEW-TEMPLATE.json").write_bytes(template_data)
    registers = {
        "REGISTER-NEIMENOVANIH.jsonl": '{"record_type":"register","entries_recorded":0}\n',
        "REGISTER-PADCEV.jsonl": '{"record_type":"register","entries_recorded":0}\n',
    }
    entries = [
        {"path": "LICENSE.md", "size": len(license_bytes), "sha256": sha256(license_bytes)},
        {"path": "RELEASE-REVIEW-TEMPLATE.json", "size": len(template_data), "sha256": sha256(template_data)},
    ]
    for name, contents in registers.items():
        data = contents.encode("utf-8")
        (root / name).write_bytes(data)
        entries.append({"path": name, "size": len(data), "sha256": sha256(data)})
    manifest = {
        "schema_version": "1.0.0", "release_status": "CANDIDATE_NOT_RELEASED",
        "version": "2.6", "date": "2026-10-23", "predecessor": "2.5",
        "source_commit": None, "files": entries,
    }
    manifest_bytes = (json.dumps(manifest, indent=2) + "\n").encode("utf-8")
    (root / "release-manifest.json").write_bytes(manifest_bytes)
    review = {
        "schema_version": "1.0.0", "reviewer_id": "reviewer-1", "executor_id": "executor-1",
        "decision": "APPROVED", "reviewed_at": "2026-10-26T10:00:00Z",
        "scope": "Structural checks and exact artifact digest.",
        "conflict_statement": "No financial or authorship conflict declared.",
        "findings": [], "manifest_sha256": sha256(manifest_bytes),
        "license_sha256": sha256(license_bytes), "evidence_uri": "https://reviews.test/vbl/1",
        "signature": None,
    }
    (root / "independent-review.json").write_text(json.dumps(review, indent=2) + "\n", encoding="utf-8")


class ReleaseGateTests(unittest.TestCase):
    def run_checker(self, root: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run([sys.executable, str(CHECKER), str(root)], check=False,
                              capture_output=True, text=True, encoding="utf-8")

    def run_preparer(self, source: Path, destination: Path, *options: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run([sys.executable, str(PREPARER), str(source), str(destination),
                               "--executor-id", "executor-test", *options], check=False,
                              capture_output=True, text=True, encoding="utf-8")

    def test_complete_fixture_passes_local_gate(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            release_fixture(root)
            result = self.run_checker(root)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("VBL-PRE-REVIEW", result.stdout)
            self.assertIn("VBL-PRE-VERSION", result.stdout)
            self.assertIn("local checks cannot authenticate identities", result.stdout)

    def test_missing_review_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            release_fixture(root)
            (root / "independent-review.json").unlink()
            result = self.run_checker(root)
            self.assertEqual(result.returncode, 2)
            self.assertIn("VBL-PRE-REVIEW", result.stdout)

    def test_self_review_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            release_fixture(root)
            path = root / "independent-review.json"
            review = json.loads(path.read_text(encoding="utf-8"))
            review["reviewer_id"] = review["executor_id"]
            path.write_text(json.dumps(review), encoding="utf-8")
            result = self.run_checker(root)
            self.assertEqual(result.returncode, 2)
            self.assertIn("reviewer_id must differ", result.stdout)

    def test_case_insensitive_self_review_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            release_fixture(root)
            path = root / "independent-review.json"
            review = json.loads(path.read_text(encoding="utf-8"))
            review["reviewer_id"] = review["executor_id"].upper()
            path.write_text(json.dumps(review), encoding="utf-8")
            result = self.run_checker(root)
            self.assertEqual(result.returncode, 2)
            self.assertIn("case-insensitive", result.stdout)

    def test_review_bound_to_stale_license_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            release_fixture(root)
            with (root / "LICENSE.md").open("ab") as stream:
                stream.write(b"changed\n")
            result = self.run_checker(root)
            self.assertEqual(result.returncode, 2)
            self.assertIn("review must bind current manifest and license SHA-256", result.stdout)
            self.assertIn("size/hash mismatch", result.stdout)

    def test_manifest_parent_traversal_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            release_fixture(root)
            path = root / "release-manifest.json"
            manifest = json.loads(path.read_text(encoding="utf-8"))
            manifest["files"][0]["path"] = "../LICENSE.md"
            path.write_text(json.dumps(manifest), encoding="utf-8")
            result = self.run_checker(root)
            self.assertEqual(result.returncode, 2)
            self.assertIn("unsafe or missing path", result.stdout)

    def test_manifest_duplicate_paths_fail(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            release_fixture(root)
            path = root / "release-manifest.json"
            manifest = json.loads(path.read_text(encoding="utf-8"))
            manifest["files"].append(dict(manifest["files"][0]))
            path.write_text(json.dumps(manifest), encoding="utf-8")
            result = self.run_checker(root)
            self.assertEqual(result.returncode, 2)
            self.assertIn("duplicate manifest path", result.stdout)

    def test_missing_manifest_list_is_reported_not_raised(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            release_fixture(root)
            path = root / "release-manifest.json"
            manifest = json.loads(path.read_text(encoding="utf-8"))
            del manifest["files"]
            path.write_text(json.dumps(manifest), encoding="utf-8")
            result = self.run_checker(root)
            self.assertEqual(result.returncode, 2)
            self.assertIn("manifest invalid", result.stdout)

    def test_manifest_windows_path_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            release_fixture(root)
            path = root / "release-manifest.json"
            manifest = json.loads(path.read_text(encoding="utf-8"))
            manifest["files"][0]["path"] = "C:\\outside\\LICENSE.md"
            path.write_text(json.dumps(manifest), encoding="utf-8")
            result = self.run_checker(root)
            self.assertEqual(result.returncode, 2)
            self.assertIn("unsafe or missing path", result.stdout)

    def test_symlink_escape_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            outside = root.parent / f"{root.name}-outside.txt"
            outside.write_text("outside", encoding="utf-8")
            release_fixture(root)
            link = root / "escape.txt"
            try:
                link.symlink_to(outside)
            except (OSError, NotImplementedError):
                outside.unlink(missing_ok=True)
                self.skipTest("symlink creation is unavailable")
            path = root / "release-manifest.json"
            manifest = json.loads(path.read_text(encoding="utf-8"))
            manifest["files"].append({"path": "escape.txt", "size": 6, "sha256": sha256(b"outside")})
            path.write_text(json.dumps(manifest), encoding="utf-8")
            result = self.run_checker(root)
            outside.unlink(missing_ok=True)
            self.assertEqual(result.returncode, 2)
            self.assertIn("unsafe or missing path", result.stdout)

    def test_duplicate_record_ids_across_registers_fail(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            release_fixture(root)
            first = {"record_type":"contributor", "schema_version":"1.0.0", "record_id":"R-1",
                     "status":"ACTIVE", "created_at":"2026-10-26T00:00:00Z", "identity_status":"UNKNOWN",
                     "attribution":"Source contributor", "evidence":[]}
            second = {"record_type":"fall", "schema_version":"1.0.0", "record_id":"R-1",
                      "status":"OPEN", "created_at":"2026-10-26T00:00:00Z", "artifact":"test",
                      "claim_or_expectation":"expected pass", "observation":"observed failure",
                      "impact":"LOW", "evidence":[]}
            (root / "REGISTER-NEIMENOVANIH.jsonl").write_text(
                '{"record_type":"register","entries_recorded":1}\n' + json.dumps(first) + "\n", encoding="utf-8")
            (root / "REGISTER-PADCEV.jsonl").write_text(
                '{"record_type":"register","entries_recorded":1}\n' + json.dumps(second) + "\n", encoding="utf-8")
            result = self.run_checker(root)
            self.assertEqual(result.returncode, 2)
            self.assertIn("duplicate record_id", result.stdout)

    def test_register_missing_required_fields_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            release_fixture(root)
            (root / "REGISTER-PADCEV.jsonl").write_text(
                '{"record_type":"fall","record_id":"F-1"}\n', encoding="utf-8")
            result = self.run_checker(root)
            self.assertEqual(result.returncode, 2)
            self.assertIn("schema_version", result.stdout)

    def test_header_count_mismatch_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            release_fixture(root)
            (root / "REGISTER-NEIMENOVANIH.jsonl").write_text(
                '{"record_type":"register","entries_recorded":7}\n', encoding="utf-8")
            result = self.run_checker(root)
            self.assertEqual(result.returncode, 2)
            self.assertIn("header declares 7 entries; found 0 live rows", result.stdout)

    def test_missing_header_in_empty_register_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            release_fixture(root)
            (root / "REGISTER-PADCEV.jsonl").write_text("", encoding="utf-8")
            result = self.run_checker(root)
            self.assertEqual(result.returncode, 2)
            self.assertIn("header is required even when the register contains zero", result.stdout)

    def test_register_header_must_be_first_and_unique(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            release_fixture(root)
            row = {"record_type":"contributor", "schema_version":"1.0.0", "record_id":"R-2",
                   "status":"ACTIVE", "created_at":"2026-10-26T00:00:00Z", "identity_status":"UNKNOWN",
                   "attribution":"Source contributor", "evidence":[]}
            header = '{"record_type":"register","entries_recorded":1}'
            (root / "REGISTER-NEIMENOVANIH.jsonl").write_text(
                json.dumps(row) + "\n" + header + "\n" + header + "\n", encoding="utf-8")
            result = self.run_checker(root)
            self.assertEqual(result.returncode, 2)
            self.assertIn("expected exactly one register header; found 2", result.stdout)

    def test_correction_must_reference_prior_record(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            release_fixture(root)
            original = {"record_type":"fall", "schema_version":"1.0.0", "record_id":"F-10",
                        "status":"OPEN", "created_at":"2026-10-26T00:00:00Z", "artifact":"test",
                        "claim_or_expectation":"expected pass", "observation":"observed failure",
                        "impact":"LOW", "evidence":[]}
            correction = {"record_type":"fall", "schema_version":"1.0.0", "record_id":"F-11",
                          "status":"CORRECTED", "created_at":"2026-10-26T00:01:00Z", "artifact":"test",
                          "claim_or_expectation":"correct prior entry", "observation":"corrected", "impact":"LOW",
                          "evidence":[], "corrects_record_id":"F-MISSING", "correction_reason":"source correction"}
            rows = ['{"record_type":"register","entries_recorded":2}', json.dumps(original), json.dumps(correction)]
            (root / "REGISTER-PADCEV.jsonl").write_text("\n".join(rows) + "\n", encoding="utf-8")
            result = self.run_checker(root)
            self.assertEqual(result.returncode, 2)
            self.assertIn("missing or self-referential target", result.stdout)

    def test_invalid_timestamp_in_evidence_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            release_fixture(root)
            row = {"record_type":"fall", "schema_version":"1.0.0", "record_id":"F-3",
                   "status":"OPEN", "created_at":"2026-10-26T00:00:00Z", "artifact":"test",
                   "claim_or_expectation":"expected pass", "observation":"observed failure",
                   "impact":"LOW", "evidence":[{"source":"test", "sha256":"a" * 64,
                   "observed_at":"not-a-date"}]}
            (root / "REGISTER-PADCEV.jsonl").write_text(
                '{"record_type":"register","entries_recorded":1}\n' + json.dumps(row) + "\n", encoding="utf-8")
            result = self.run_checker(root)
            self.assertEqual(result.returncode, 2)
            self.assertIn("not-a-date", result.stdout)

    def test_template_cannot_enter_live_register(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            release_fixture(root)
            (root / "REGISTER-PADCEV.jsonl").write_text(
                '{"record_type":"fall","record_id":"TEMPLATE-F-0","status":"TEMPLATE"}\n', encoding="utf-8")
            result = self.run_checker(root)
            self.assertEqual(result.returncode, 2)
            self.assertIn("template/example rows are not allowed", result.stdout)

    def test_approved_review_with_findings_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            release_fixture(root)
            path = root / "independent-review.json"
            review = json.loads(path.read_text(encoding="utf-8"))
            review["findings"] = ["Unresolved source mismatch"]
            path.write_text(json.dumps(review), encoding="utf-8")
            result = self.run_checker(root)
            self.assertEqual(result.returncode, 2)
            self.assertIn("APPROVED review must have no unresolved findings", result.stdout)

    def test_pending_reviewer_placeholder_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            release_fixture(root)
            path = root / "independent-review.json"
            review = json.loads(path.read_text(encoding="utf-8"))
            review["reviewer_id"] = "PENDING_REVIEWER"
            path.write_text(json.dumps(review), encoding="utf-8")
            result = self.run_checker(root)
            self.assertEqual(result.returncode, 2)
            self.assertIn("pending placeholder fields", result.stdout)

    def test_replacement_character_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            release_fixture(root)
            with (root / "LICENSE.md").open("ab") as stream:
                stream.write("\ufffd\n".encode("utf-8"))
            result = self.run_checker(root)
            self.assertEqual(result.returncode, 2)
            self.assertIn("replacement-character", result.stdout)

    def test_manifest_version_mismatch_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            release_fixture(root)
            path = root / "release-manifest.json"
            manifest = json.loads(path.read_text(encoding="utf-8"))
            manifest["version"] = "10.0.0"
            path.write_text(json.dumps(manifest), encoding="utf-8")
            result = self.run_checker(root)
            self.assertEqual(result.returncode, 2)
            self.assertIn("VBL-PRE-VERSION", result.stdout)

    def test_prepare_rejects_version_machine_record_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "pasted.txt"
            destination = root / "candidate"
            source.write_text(valid_source(version="10.0.0").replace("10.0.0", "2.6", 1), encoding="utf-8")
            prepared = self.run_preparer(source, destination)
            self.assertNotEqual(prepared.returncode, 0)
            self.assertIn("disagrees with machine version", prepared.stderr)
            self.assertFalse(destination.exists())

    def test_prepare_rejects_scrape_chrome(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "scraped.md"
            destination = root / "candidate"
            source.write_text(valid_source() + "\nSymbols\nFilter symbols\n", encoding="utf-8")
            prepared = self.run_preparer(source, destination)
            self.assertNotEqual(prepared.returncode, 0)
            self.assertIn("web/page-scrape contamination", prepared.stderr)
            self.assertFalse(destination.exists())

    def test_prepare_rejects_conflicting_version_argument(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.md"
            destination = root / "candidate"
            source.write_text(valid_source(), encoding="utf-8")
            prepared = self.run_preparer(source, destination, "--version", "2.6")
            self.assertNotEqual(prepared.returncode, 0)
            self.assertIn("does not match source version", prepared.stderr)
            self.assertFalse(destination.exists())

    def test_prepare_stages_source_metadata_and_blocks_review(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.md"
            staged = root / "candidate"
            source.write_text(valid_source(), encoding="utf-8")
            prepared = self.run_preparer(source, staged)
            self.assertEqual(prepared.returncode, 0, prepared.stdout + prepared.stderr)
            manifest = json.loads((staged / "release-manifest.json").read_text(encoding="utf-8"))
            self.assertEqual((manifest["version"], manifest["date"], manifest["predecessor"]),
                             ("10.0.0", "2026-10-26", "10.0.0-rc1"))
            result = self.run_checker(staged)
            self.assertEqual(result.returncode, 2)
            self.assertIn("decision must be APPROVED", result.stdout)

    def test_prepare_refuses_nonempty_destination_without_overwriting(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.md"
            destination = root / "candidate"
            source.write_text(valid_source(), encoding="utf-8")
            destination.mkdir()
            marker = destination / "keep.txt"
            marker.write_text("untouched", encoding="utf-8")
            prepared = self.run_preparer(source, destination)
            self.assertNotEqual(prepared.returncode, 0)
            self.assertEqual(marker.read_text(encoding="utf-8"), "untouched")


if __name__ == "__main__":
    unittest.main()
