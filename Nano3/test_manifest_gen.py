"""Regression tests for VBL manifest metadata and byte verification."""

import contextlib
import importlib.util
import io
import json
import os
import tempfile
import unittest
from unittest import mock

SCRIPT_PATH = os.path.join(os.path.dirname(__file__), "scripts", "manifest_gen.py")
SPEC = importlib.util.spec_from_file_location("vbl_manifest_gen_under_test", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("could not load scripts/manifest_gen.py for regression tests")
manifest_gen = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(manifest_gen)


class ManifestGeneratorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = self.temp.name
        os.makedirs(os.path.join(self.root, "scripts"))
        self.manifest_path = os.path.join(self.root, "LICENSE-MANIFEST.json")
        self.metadata_path = os.path.join(self.root, "scripts", "release_metadata.json")
        self.metadata = {
            "license": "VBL — Verification Before Assertion License",
            "version": "0.1210 × 10⁴",
            "date": "2026-10-28",
            "law": "VBL §0a; SHA-256",
            "note": "release metadata stays explicit",
        }
        self.write_metadata()
        for path, body in {
            "LICENSE.md": b"license bytes\n",
            "REGISTER-NEIMENOVANIH.jsonl": b'{"id":"NE-0001"}\n',
            "REGISTER-PADCEV.jsonl": b'{"id":"PAD-0001"}\n',
        }.items():
            with open(os.path.join(self.root, path), "wb") as f:
                f.write(body)

        self.patches = [
            mock.patch.object(manifest_gen, "ROOT", self.root),
            mock.patch.object(manifest_gen, "MANIFEST", self.manifest_path),
            mock.patch.object(manifest_gen, "RELEASE_METADATA", self.metadata_path),
        ]
        for patcher in self.patches:
            patcher.start()
        self.addCleanup(self.stop_patches)

    def stop_patches(self):
        for patcher in reversed(self.patches):
            patcher.stop()
        self.temp.cleanup()

    def write_metadata(self, value=None):
        if value is None:
            value = self.metadata
        with open(self.metadata_path, "w", encoding="utf-8") as f:
            json.dump(value, f, ensure_ascii=False, indent=2)
            f.write("\n")

    def write_manifest(self, value=None):
        if value is None:
            value = manifest_gen.generate()
        with open(self.manifest_path, "w", encoding="utf-8") as f:
            json.dump(value, f, ensure_ascii=False, indent=2)
            f.write("\n")

    def run_check(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = manifest_gen.check()
        return code, output.getvalue()

    def test_current_manifest_passes(self):
        self.write_manifest()
        code, output = self.run_check()
        self.assertEqual(code, 0)
        self.assertIn("MANIFEST-DRŽI", output)

    def test_version_mismatch_fails_even_when_file_hashes_match(self):
        manifest = manifest_gen.generate()
        manifest["version"] = "0.1100 × 10⁴"
        self.write_manifest(manifest)
        code, output = self.run_check()
        self.assertEqual(code, 1)
        self.assertIn("MANIFEST-METAPODATKI-ODMIK", output)
        self.assertIn("version", output)

    def test_date_mismatch_fails(self):
        manifest = manifest_gen.generate()
        manifest["date"] = "1900-01-01"
        self.write_manifest(manifest)
        code, output = self.run_check()
        self.assertEqual(code, 1)
        self.assertIn("date", output)

    def test_law_mismatch_fails(self):
        manifest = manifest_gen.generate()
        manifest["law"] = "different rule"
        self.write_manifest(manifest)
        code, output = self.run_check()
        self.assertEqual(code, 1)
        self.assertIn("law", output)

    def test_unexpected_manifest_metadata_fails(self):
        manifest = manifest_gen.generate()
        manifest["unreviewed_field"] = "unexpected"
        self.write_manifest(manifest)
        code, output = self.run_check()
        self.assertEqual(code, 1)
        self.assertIn("unreviewed_field", output)

    def test_changed_body_bytes_fail(self):
        self.write_manifest()
        with open(os.path.join(self.root, "LICENSE.md"), "ab") as f:
            f.write(b"changed\n")
        code, output = self.run_check()
        self.assertEqual(code, 1)
        self.assertIn("MANIFEST-TELESA-ODMIK", output)

    def test_missing_covered_file_fails_closed(self):
        self.write_manifest()
        os.remove(os.path.join(self.root, "REGISTER-PADCEV.jsonl"))
        code, output = self.run_check()
        self.assertEqual(code, 1)
        self.assertIn("MANIFEST-NEPREVERLJIV", output)

    def test_missing_release_metadata_field_fails(self):
        self.metadata.pop("version")
        self.write_metadata()
        self.write_manifest({})
        code, output = self.run_check()
        self.assertEqual(code, 1)
        self.assertIn("version", output)

    def test_release_metadata_cannot_supply_items(self):
        metadata = dict(self.metadata)
        metadata["items"] = []
        self.write_metadata(metadata)
        self.write_manifest({})
        code, output = self.run_check()
        self.assertEqual(code, 1)
        self.assertIn("polja 'items'", output)

    def test_release_metadata_must_be_json_object(self):
        self.write_metadata(["not", "an", "object"])
        self.write_manifest({})
        code, output = self.run_check()
        self.assertEqual(code, 1)
        self.assertIn("mora vsebovati JSON-objekt", output)

    def test_missing_release_metadata_file_fails_cleanly(self):
        self.write_manifest()
        os.remove(self.metadata_path)
        code, output = self.run_check()
        self.assertEqual(code, 1)
        self.assertIn("MANIFEST-NEPREVERLJIV", output)

    def test_changed_release_note_makes_existing_manifest_stale(self):
        self.write_manifest()
        metadata = dict(self.metadata)
        metadata["note"] = "edited after manifest generation"
        self.write_metadata(metadata)
        code, output = self.run_check()
        self.assertEqual(code, 1)
        self.assertIn("note", output)

    def test_malformed_manifest_fails_cleanly(self):
        with open(self.manifest_path, "w", encoding="utf-8") as f:
            f.write("{not-json")
        code, output = self.run_check()
        self.assertEqual(code, 1)
        self.assertIn("MANIFEST-NEPREVERLJIV", output)

    def test_missing_manifest_fails(self):
        code, output = self.run_check()
        self.assertEqual(code, 1)
        self.assertIn("LICENSE-MANIFEST.json manjka", output)


if __name__ == "__main__":
    unittest.main(verbosity=2)
