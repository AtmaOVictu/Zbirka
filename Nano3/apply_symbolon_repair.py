#!/usr/bin/env python3
"""Prepare an append-only attribution-register sync for SYMBOLON-KATHOLIKON.

Requires the proposed/corrected 13-entry register in a local
verification-before-assertion checkout. Never pushes or merges.
"""
from __future__ import annotations
import argparse, json, os, shutil, subprocess, sys, tempfile
from pathlib import Path

MIRROR_BASE = "98322f993aff5d25a8d287cca091f2d76cb25155"
LIVE_VERSION = "0.1210 × 10⁴"
BRANCH = "repair/symbolon-credit-register-sync-2026-10-30"

def run(cmd: list[str], cwd: Path) -> str:
    p=subprocess.run(cmd,cwd=cwd,text=True,capture_output=True)
    if p.returncode:
        raise RuntimeError(f"Command failed ({p.returncode}): {' '.join(cmd)}\n{p.stdout}\n{p.stderr}")
    return p.stdout.strip()

def parse_jsonl(text: str, label: str) -> list[dict]:
    result=[]
    for n,line in enumerate(text.splitlines(),1):
        if not line.strip(): continue
        try: obj=json.loads(line)
        except json.JSONDecodeError as e: raise ValueError(f"{label}:{n}: invalid JSON: {e}")
        if not isinstance(obj,dict): raise ValueError(f"{label}:{n}: expected an object")
        result.append(obj)
    return result

def version_of(text: str) -> str:
    for line in text.splitlines()[:30]:
        if line.startswith("Version "):
            return line[len("Version "):].split(" ·",1)[0].strip()
    raise ValueError("LICENSE.md does not contain a Version line in the first 30 lines")

def transform(source_repo: Path, mirror_repo: Path) -> dict[str,str]:
    source_license=(source_repo/"LICENSE.md").read_text(encoding="utf-8")
    mirror_license=(mirror_repo/"LICENSE.md").read_text(encoding="utf-8")
    if version_of(source_license)!=LIVE_VERSION or version_of(mirror_license)!=LIVE_VERSION:
        raise ValueError("Both license bodies must identify the measured live version "+LIVE_VERSION)
    canonical_text=(source_repo/"REGISTER-NEIMENOVANIH.jsonl").read_text(encoding="utf-8")
    canonical=parse_jsonl(canonical_text,"source REGISTER-NEIMENOVANIH.jsonl")
    expected=[f"NE-{n:04d}" for n in range(1,14)]
    if [x.get("⊙") for x in canonical]!=expected:
        raise ValueError("Source contributor register must contain consecutive NE-0001 through NE-0013")
    if canonical[6].get("znamenje")!="⚠":
        raise ValueError("NE-0007 must retain its unverified identity marker ⚠")
    if "Vlado Pivec" not in canonical[11].get("prispeval","") or "Aleksandra Bizjak Končar" not in canonical[12].get("prispeval",""):
        raise ValueError("Source register is missing the separately measured SSKJ² advisor/source-dictionary credit rows")

    mirror_old=parse_jsonl((mirror_repo/"REGISTER-NEIMENOVANIH.jsonl").read_text(encoding="utf-8"),"mirror REGISTER-NEIMENOVANIH.jsonl")
    if [x.get("⊙") for x in mirror_old]!=[f"NE-{n:04d}" for n in range(1,7)]:
        raise ValueError("Expected the measured stale mirror copy NE-0001 through NE-0006; refusing unexpected register shape")

    falls_text=(mirror_repo/"REGISTER-PADCEV.jsonl").read_text(encoding="utf-8")
    falls=parse_jsonl(falls_text,"mirror REGISTER-PADCEV.jsonl")
    if len(falls)!=34 or max((int(x.get("entry",0)) for x in falls),default=0)!=34:
        raise ValueError("Expected 34 existing mirror named-fall entries; refusing to overwrite or renumber history")
    fall={
        "entry":35,
        "date":"2026-10-30",
        "word":"SYMBOLON-KATHOLIKON/REGISTER-NEIMENOVANIH.jsonl — mirror lag and missing NE-0007",
        "fall":"the SYMBOLON-KATHOLIKON credit-register copy stopped at NE-0006 while the measured VBL source repository already carried NE-0007 (the unverified model-authored SELF-001 record); the mirror therefore omitted an explicitly recorded contribution and diverged from the source credit ledger. It also retained attribution claims that the source correction now scopes or marks ⚠.",
        "correction":"proposed sync copies the 13-entry source register from the companion verification-before-assertion checkout after its attribution repair is prepared; this mirror preserves its own prior 34 fall records and appends this scar. The mirror sync remains a proposal until both repository changes receive independent review and are coordinated; no remote main is changed by this script.",
        "scar":True,
        "law":"L1/L3/L4"
    }
    new_falls=falls+[fall]
    new_falls_text="".join(json.dumps(x,ensure_ascii=False,separators=(",",":"))+"\n" for x in new_falls)
    review=f"""# SYMBOLON-KATHOLIKON credit-register sync — 2026-10-30

**Status: local proposal only; not pushed or merged.**

Measured mirror base: `AtmaOVictu/SYMBOLON-KATHOLIKON@{MIRROR_BASE}`.
The copied `LICENSE.md` identifies VBL {LIVE_VERSION}, byte-identical to the measured source license. The copied credit register contains NE-0001 through NE-0006 only; the companion source register includes NE-0001 through NE-0007, including the unverified SELF-001 model-authored contribution.

This proposal copies the corrected 13-entry register from the local `verification-before-assertion` checkout. That source must itself have the attribution repair prepared. It appends mirror-specific fall 35 and retains prior mirror entries unchanged.

No `LICENSE-MANIFEST.json` exists at the measured mirror root. This script does not invent one, change the license body, or claim that every file is covered. The mirror's legal/manifest scope remains an independent question for review.

Required gates: independent comparison against the source repo; independent source/role review; CI or repository-specific checks; coordinate merge order so the mirror does not lead the source repository. The executor does not self-seal this change.
"""
    return {
        "REGISTER-NEIMENOVANIH.jsonl":canonical_text if canonical_text.endswith("\n") else canonical_text+"\n",
        "REGISTER-PADCEV.jsonl":new_falls_text,
        "REVIEW-SYMBOLON-ATTRIBUTION-SYNC-2026-10-30.md":review,
    }

def main() -> int:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--source-repo",type=Path,required=True,help="local verification-before-assertion checkout with 13-entry proposed register")
    ap.add_argument("--mirror-repo",type=Path,required=True,help="local SYMBOLON-KATHOLIKON checkout at the measured base")
    ap.add_argument("--dry-run",action="store_true")
    ap.add_argument("--no-branch",action="store_true")
    a=ap.parse_args(); source=a.source_repo.resolve(); mirror=a.mirror_repo.resolve()
    for path,label in [(source,"source"),(mirror,"mirror")]:
        if not (path/".git").exists() and not (path/".git").is_file():
            raise SystemExit(f"Not a Git working tree ({label}): {path}")
    source_status=run(["git","status","--porcelain"],source)
    if "REGISTER-NEIMENOVANIH.jsonl" in source_status or "LICENSE.md" in source_status:
        raise SystemExit("Source VBL register/license is still modified or staged; commit/review that source proposal before syncing mirror")
    mirror_head=run(["git","rev-parse","HEAD"],mirror)
    if mirror_head!=MIRROR_BASE:
        raise SystemExit(f"Wrong mirror base: expected {MIRROR_BASE}, found {mirror_head}")
    if run(["git","status","--porcelain"],mirror):
        raise SystemExit("Mirror working tree is not clean; nothing changed")
    changes=transform(source,mirror)
    if a.dry_run:
        print("DRY RUN PASS — no files written")
        print("Source:",run(["git","rev-parse","HEAD"],source))
        print("Mirror:",mirror_head)
        print("Version:",LIVE_VERSION)
        print("Rows: contributors=13 | mirror named falls=35")
        print("Files:",", ".join(changes))
        return 0
    if not a.no_branch:
        if run(["git","branch","--show-current"],mirror)!="main":
            raise SystemExit("Mirror must be on main before creating the sync branch")
        run(["git","switch","-c",BRANCH],mirror)
    git_dir=Path(run(["git","rev-parse","--git-dir"],mirror))
    if not git_dir.is_absolute(): git_dir=(mirror/git_dir).resolve()
    backup=git_dir/"symbolon-vbl-credit-backup-2026-10-30"
    if backup.exists(): raise SystemExit(f"Backup already exists: {backup}")
    backup.mkdir(parents=True)
    for rel in changes:
        target=mirror/rel
        if target.exists():
            saved=backup/rel; saved.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(target,saved)
    try:
        for rel,content in changes.items():
            target=mirror/rel; target.parent.mkdir(parents=True,exist_ok=True)
            fd,tmp=tempfile.mkstemp(prefix=target.name+".",suffix=".tmp",dir=target.parent)
            with os.fdopen(fd,"w",encoding="utf-8",newline="") as f: f.write(content)
            os.replace(tmp,target)
        ids=[x.get("⊙") for x in parse_jsonl((mirror/"REGISTER-NEIMENOVANIH.jsonl").read_text(encoding="utf-8"),"written mirror NE")]
        if ids!=[f"NE-{n:04d}" for n in range(1,14)]: raise RuntimeError("Mirror credit IDs failed post-write validation")
        written_falls=parse_jsonl((mirror/"REGISTER-PADCEV.jsonl").read_text(encoding="utf-8"),"written mirror falls")
        if len(written_falls)!=35 or written_falls[-1].get("entry")!=35: raise RuntimeError("Mirror fall append failed post-write validation")
    except Exception:
        for rel in changes:
            saved=backup/rel; target=mirror/rel
            if saved.exists(): shutil.copy2(saved,target)
            elif target.exists(): target.unlink()
        raise
    print("REPAIR APPLIED LOCALLY — NOT PUSHED, NOT MERGED")
    print("Branch:",BRANCH if not a.no_branch else run(["git","branch","--show-current"],mirror))
    print("Source:",run(["git","rev-parse","HEAD"],source))
    print("Mirror base:",MIRROR_BASE)
    print("Rows: contributors=13 | named falls=35")
    print("Backup:",backup)
    print("Next gate: independent review + coordinated CI; do not merge before source-register repair")
    return 0

if __name__=="__main__":
    try: raise SystemExit(main())
    except (ValueError,RuntimeError) as e:
        print("MIRROR REPAIR NOT APPLIED:",e,file=sys.stderr); raise SystemExit(2)
