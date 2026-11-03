#!/usr/bin/env python3
"""Apply the reviewed, append-only attribution correction bundle to a local clone.

This script never changes the upstream repository or pushes a branch. It only
writes into the --repo-root directory supplied by the operator. Default mode
is dry-run; use --apply for local writes.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import tempfile

BASE_REGISTER_SHA256 = "b1ddc4ce9b85481eb2efc39899da2f705db752b06ea0578702ebb529bc807c63"
BASE_REGISTER_GIT_BLOB = "5b2e26d27c88802c077201cd4050c3d7f90a37f1"
BASE_REGISTER_SIZE = 2784
BASE_MANIFEST_REGISTER_SHA256 = BASE_REGISTER_SHA256
BASE_MANIFEST_REGISTER_SIZE = BASE_REGISTER_SIZE
BASE_MANIFEST_SIZE = 1458
BASE_MANIFEST_GIT_BLOB = "206e789f5eaede4718a458c1656819fe85813091"
BASE_LICENSE_SHA256 = "cea269e49d8a7dbe2b802deb4d4a91eed02435c580310178da275eb03ad99844"
BASE_LICENSE_SIZE = 80596
BASE_PADCEV_SHA256 = "f389543a40a54458a7e822112276fcbbf6b2d079c08af3582a52dc734511ab33"
BASE_PADCEV_SIZE = 36170
BASE_VERSION = "0.1210 × 10⁴"
TARGET_DATE = "2026-10-30"

OLD_EN = "- Training data from a **national citizen-science campaign** (povejmo.si) toward a 40-billion-word corpus, with the National and University Library, Dnevnik, and the Slovenian Press Agency — framed as digital sovereignty for a two-million-speaker language. ⊢"
NEW_EN = "- **[Povejmo.si](https://citizenscience.si/aktivnosti-katalog-projektov/zbiranje-besedil-za-slovenski-veliki-jezikovni-model-povejmo-si/)** was a national collection activity under [PoVeJMo](https://www.fri.uni-lj.si/sl/projekti/1818), gathering written and spoken Slovene texts for a Slovene large language model. The activity page gives 40 billion words as the estimated volume of text needed — not as a campaign opposing a corpus. It says submitters must hold copyright in the texts they send. The source does not establish blanket volunteer status, individual payment status, or one licence for every submission. ⊢"
OLD_SL = "- Učni podatki iz **nacionalne kampanje občanske znanosti** (povejmo.si) proti 40-milijardnemu besednemu korpusu, z NUK, Dnevnikom in STA — predstavljeno kot digitalna suverenost za jezik z dvema milijonoma govorcev. ⊢"
NEW_SL = "- **[Povejmo.si](https://citizenscience.si/aktivnosti-katalog-projektov/zbiranje-besedil-za-slovenski-veliki-jezikovni-model-povejmo-si/)** je bila nacionalna zbiralna akcija pisnih in govorjenih besedil v slovenščini v okviru [PoVeJMo](https://www.fri.uni-lj.si/sl/projekti/1818). Uradni opis navaja oceno 40 milijard besed kot potrebni obseg besedil za model — ne kot korpus, proti kateremu bi bila akcija usmerjena. Za oddana besedila so morali imeti sodelujoči avtorske pravice. Vir ne dokazuje, da so bili vsi oddajatelji neplačani prostovoljci ali da je za vse prispevke veljala ena skupna licenca. ⊢"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def build_changes(repo_root: Path, bundle_dir: Path) -> dict[str, bytes | dict]:
    base = (bundle_dir / "BASE-REGISTER-NEIMENOVANIH.jsonl").read_bytes()
    proposed = (bundle_dir / "REGISTER-NEIMENOVANIH.jsonl").read_bytes()
    require(len(base) == BASE_REGISTER_SIZE, "Bundle base register byte count mismatch")
    require(sha256(base) == BASE_REGISTER_SHA256, "Bundle base register SHA-256 mismatch")
    require(git_blob_sha(base) == BASE_REGISTER_GIT_BLOB, "Bundle base register Git blob mismatch")
    require(proposed.startswith(base), "Proposed register is not append-only: original bytes are not an exact prefix")

    current_register = (repo_root / "REGISTER-NEIMENOVANIH.jsonl").read_bytes()
    require(current_register == base, "Repository register does not match the measured base snapshot; stop and rebase manually")

    parsed = [json.loads(line) for line in proposed.decode("utf-8").splitlines() if line.strip()]
    base_parsed = [json.loads(line) for line in base.decode("utf-8").splitlines() if line.strip()]
    require(len(base_parsed) == 7 and len(parsed) == 14, "Unexpected register row counts")
    ids = [r["⊙"] for r in parsed]
    require(len(ids) == len(set(ids)), "Duplicate register IDs")
    require(ids[:7] == [f"NE-{i:04d}" for i in range(1, 8)], "Original register IDs/order changed")
    require(ids[7:] == [f"NE-{i:04d}" for i in range(8, 15)], "Correction IDs/order mismatch")
    require(all(r.get("placano", "").startswith("NEZNANO") for r in parsed[7:]), "A new record lacks explicit UNKNOWN payment status")

    manifest_path = repo_root / "LICENSE-MANIFEST.json"
    manifest_bytes = manifest_path.read_bytes()
    require(len(manifest_bytes) == BASE_MANIFEST_SIZE, "Baseline manifest byte count changed")
    require(git_blob_sha(manifest_bytes) == BASE_MANIFEST_GIT_BLOB, "Baseline manifest blob differs from the measured main snapshot")
    manifest = json.loads(manifest_bytes.decode("utf-8"))
    require(manifest.get("version") == BASE_VERSION, "Manifest version is no longer the expected 0.1210 line")
    items = {item["path"]: item for item in manifest.get("items", [])}
    require(items.get("LICENSE.md", {}).get("size") == BASE_LICENSE_SIZE, "LICENSE.md manifest size changed")
    require(items.get("LICENSE.md", {}).get("sha256") == BASE_LICENSE_SHA256, "LICENSE.md manifest digest changed")
    license_bytes = (repo_root / "LICENSE.md").read_bytes()
    require(len(license_bytes) == BASE_LICENSE_SIZE, "LICENSE.md actual byte count differs from the measured base")
    require(sha256(license_bytes) == BASE_LICENSE_SHA256, "LICENSE.md actual bytes differ from the measured base")
    require(items.get("REGISTER-NEIMENOVANIH.jsonl", {}).get("size") == BASE_MANIFEST_REGISTER_SIZE, "Manifest register byte count is not the expected base")
    require(items.get("REGISTER-NEIMENOVANIH.jsonl", {}).get("sha256") == BASE_MANIFEST_REGISTER_SHA256, "Manifest register digest is not the expected base")
    require(items.get("REGISTER-PADCEV.jsonl", {}).get("size") == BASE_PADCEV_SIZE, "Register of falls manifest size differs from measured base")
    require(items.get("REGISTER-PADCEV.jsonl", {}).get("sha256") == BASE_PADCEV_SHA256, "Register of falls differs from measured base; refusing to touch it")
    padcev_bytes = (repo_root / "REGISTER-PADCEV.jsonl").read_bytes()
    require(len(padcev_bytes) == BASE_PADCEV_SIZE, "Register of falls actual byte count differs from the measured base")
    require(sha256(padcev_bytes) == BASE_PADCEV_SHA256, "Register of falls actual bytes differ from the measured base")

    old_en = (repo_root / "README.md").read_text(encoding="utf-8")
    old_sl = (repo_root / "README-SL.md").read_text(encoding="utf-8")
    require(old_en.count(OLD_EN) == 1, "English README correction anchor missing or not unique")
    require(old_sl.count(OLD_SL) == 1, "Slovenian README correction anchor missing or not unique")

    new_en = old_en.replace(OLD_EN, NEW_EN, 1)
    new_sl = old_sl.replace(OLD_SL, NEW_SL, 1)
    new_manifest = dict(manifest)
    new_manifest["date"] = TARGET_DATE
    new_items = []
    for item in manifest["items"]:
        item = dict(item)
        if item["path"] == "REGISTER-NEIMENOVANIH.jsonl":
            item["size"] = len(proposed)
            item["sha256"] = sha256(proposed)
        new_items.append(item)
    new_manifest["items"] = new_items
    new_manifest_bytes = (json.dumps(new_manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    return {
        "REGISTER-NEIMENOVANIH.jsonl": proposed,
        "LICENSE-MANIFEST.json": new_manifest_bytes,
        "README.md": new_en.encode("utf-8"),
        "README-SL.md": new_sl.encode("utf-8"),
        "manifest": new_manifest,
    }


def apply(repo_root: Path, bundle_dir: Path, write: bool = False) -> dict:
    changes = build_changes(repo_root, bundle_dir)
    report = {
        "mode": "APPLY" if write else "DRY_RUN",
        "writes": [],
        "register_bytes": len(changes["REGISTER-NEIMENOVANIH.jsonl"]),
        "register_sha256": sha256(changes["REGISTER-NEIMENOVANIH.jsonl"]),
        "manifest_sha256": sha256(changes["LICENSE-MANIFEST.json"]),
        "manifest_register_item": next(x for x in changes["manifest"]["items"] if x["path"] == "REGISTER-NEIMENOVANIH.jsonl"),
        "unchanged": ["LICENSE.md", "REGISTER-PADCEV.jsonl", "preverba.py", "vba.py", "test_vba.py", ".github/workflows/vrata-prica.yml"],
        "original_rows_preserved": 7,
        "appended_rows": 7,
        "legal_review": "NOT_PERFORMED",
        "independent_review": "NOT_PERFORMED",
        "release": "NOT_RELEASED — this script only changes the local working tree",
    }
    if not write:
        return report
    # Stage every file and preserve exact originals before the first replace.
    # If any replace fails, restore all targets already replaced in this run.
    staged: list[tuple[Path, Path]] = []
    originals: dict[Path, bytes] = {}
    replaced: list[Path] = []
    try:
        for rel, content in changes.items():
            if rel == "manifest":
                continue
            target = repo_root / rel
            originals[target] = target.read_bytes()
            fd, temp_name = tempfile.mkstemp(prefix=target.name + ".", suffix=".tmp", dir=str(target.parent))
            with os.fdopen(fd, "wb") as f:
                f.write(content)
                f.flush()
                os.fsync(f.fileno())
            staged.append((Path(temp_name), target))
        for temp_path, target in staged:
            os.replace(temp_path, target)
            replaced.append(target)
            report["writes"].append(str(target.relative_to(repo_root)))
    except Exception:
        for target in reversed(replaced):
            fd, restore_name = tempfile.mkstemp(prefix=target.name + ".rollback.", suffix=".tmp", dir=str(target.parent))
            try:
                with os.fdopen(fd, "wb") as f:
                    f.write(originals[target])
                    f.flush()
                    os.fsync(f.fileno())
                os.replace(restore_name, target)
            finally:
                if os.path.exists(restore_name):
                    os.unlink(restore_name)
        raise
    finally:
        for temp_path, _ in staged:
            if temp_path.exists():
                temp_path.unlink()
    return report


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo-root", type=Path, required=True, help="Path to a local clone of AtmaOVictu/verification-before-assertion")
    p.add_argument("--bundle-dir", type=Path, default=Path(__file__).resolve().parent)
    p.add_argument("--apply", action="store_true", help="Write changes locally; default is dry-run")
    args = p.parse_args()
    result = apply(args.repo_root.resolve(), args.bundle_dir.resolve(), args.apply)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
