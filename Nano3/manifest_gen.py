#!/usr/bin/env python3
"""Generate and verify LICENSE-MANIFEST from release metadata and covered bytes.

The release metadata in scripts/release_metadata.json is the explicit input for
license identity and release metadata. The manifest is a generated record of
that metadata plus measured file sizes and SHA-256 digests.
"""

import hashlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, "LICENSE-MANIFEST.json")
RELEASE_METADATA = os.path.join(ROOT, "scripts", "release_metadata.json")
COVERED = ["LICENSE.md", "REGISTER-NEIMENOVANIH.jsonl", "REGISTER-PADCEV.jsonl"]
REQUIRED_METADATA = {"license", "version", "date", "law"}


def entry(rel_path):
    with open(os.path.join(ROOT, rel_path), "rb") as f:
        data = f.read()
    return {"path": rel_path, "size": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def load_release_metadata():
    """Read and validate the explicit release-metadata source of truth."""
    with open(RELEASE_METADATA, encoding="utf-8") as f:
        metadata = json.load(f)

    if not isinstance(metadata, dict):
        raise ValueError("scripts/release_metadata.json mora vsebovati JSON-objekt")

    missing = sorted(REQUIRED_METADATA - metadata.keys())
    if missing:
        raise ValueError("manjkajo obvezna polja: " + ", ".join(missing))

    invalid = sorted(
        key for key in REQUIRED_METADATA
        if not isinstance(metadata.get(key), str) or not metadata[key].strip()
    )
    if invalid:
        raise ValueError("obvezna polja morajo biti neprazni nizi: " + ", ".join(invalid))

    if "items" in metadata:
        raise ValueError("release metadata ne sme vsebovati polja 'items'; ta polja izmeri generator")

    return metadata


def generate():
    """Return the full manifest, using metadata input and measured file bytes."""
    result = load_release_metadata()
    # Every declared covered file is mandatory; absence must never shrink the manifest.
    result["items"] = [entry(path) for path in COVERED]
    return result


def _display(value):
    rendered = json.dumps(value, ensure_ascii=False, sort_keys=True)
    return rendered if len(rendered) <= 120 else rendered[:117] + "..."


def check():
    """Fail on metadata drift, body drift, malformed input, or missing records."""
    if not os.path.exists(MANIFEST):
        print("MANIFEST-ODMIK: LICENSE-MANIFEST.json manjka (VBL §0a — identifikacija brez prijave)")
        return 1

    try:
        with open(MANIFEST, encoding="utf-8") as f:
            current = json.load(f)
        fresh = generate()
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        print("MANIFEST-NEPREVERLJIV:", str(exc))
        return 1

    if not isinstance(current, dict):
        print("MANIFEST-NEPREVERLJIV: LICENSE-MANIFEST.json mora vsebovati JSON-objekt")
        return 1

    current_metadata = {key: value for key, value in current.items() if key != "items"}
    fresh_metadata = {key: value for key, value in fresh.items() if key != "items"}
    metadata_drift = current_metadata != fresh_metadata
    body_drift = current.get("items") != fresh["items"]

    if metadata_drift:
        print("MANIFEST-METAPODATKI-ODMIK: manifest se ne ujema z scripts/release_metadata.json")
        for key in sorted(current_metadata.keys() | fresh_metadata.keys()):
            old = current_metadata.get(key, "<manjka>")
            new = fresh_metadata.get(key, "<manjka>")
            if old != new:
                print("  ", key, "manifest:", _display(old), "vir:", _display(new))

    if body_drift:
        print("MANIFEST-TELESA-ODMIK: merjena telesa se ne ujemajo s prijavljenimi vnosi (VBL §0a/§12)")
        current_items = current.get("items")
        if isinstance(current_items, list):
            for old in current_items:
                if not isinstance(old, dict):
                    continue
                for new in fresh["items"]:
                    if old.get("path") == new.get("path") and old != new:
                        print(
                            "  ", old.get("path"),
                            "manifest:", str(old.get("sha256"))[:12],
                            "telesi:", str(new.get("sha256"))[:12],
                        )

    if metadata_drift or body_drift:
        return 1

    print(
        "MANIFEST-DRŽI:",
        fresh["version"],
        "|",
        ", ".join(item["path"] for item in fresh["items"]),
    )
    return 0


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(check())

    try:
        print(json.dumps(generate(), ensure_ascii=False, indent=2))
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        print("MANIFEST-GENERIRANJE-NEUSPEŠNO:", str(exc), file=sys.stderr)
        sys.exit(1)
