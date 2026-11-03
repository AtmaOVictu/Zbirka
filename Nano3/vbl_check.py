#!/usr/bin/env python3
"""vbl_check.py - mechanical checks for a VBL license text (stdlib only).

Usage:  python3 vbl_check.py LICENSE.md [--manifest MANIFEST.txt] [--xref] [--json]

A PASS covers ONLY the named check. It does not establish authorship, legal validity,
publication history, or that the text is right. Anyone can run this on the same bytes
and compare: that is the point.
"""
import sys, re, json, hashlib, os

SUP = "⁰¹²³⁴⁵⁶⁷⁸⁹"
EXP = "[" + SUP + "]+"
sup2int = lambda s: int(s.translate(str.maketrans(SUP, "0123456789")))


def main(argv):
    if not argv or argv[0].startswith("-"):
        print(__doc__); return 2
    path = argv[0]
    manifest = argv[argv.index("--manifest") + 1] if "--manifest" in argv else None
    want_xref, want_json = "--xref" in argv, "--json" in argv
    res = []  # (status, check, detail)
    add = lambda s, c, d: res.append((s, c, d))

    raw = open(path, "rb").read()
    sha = hashlib.sha256(raw).hexdigest()
    try:
        t = raw.decode("utf-8")
    except UnicodeDecodeError as e:
        add("FAIL", "encoding", "not valid UTF-8: %s" % e)
        return report(res, path, sha, len(raw), None, want_json)
    bad = t.count("\ufffd")
    add("PASS" if bad == 0 else "FAIL", "encoding", "UTF-8 ok; U+FFFD count %d; marked letters C/S/Z/D: %s" %
        (bad, [t.count(c) for c in "ČŠŽĐ"]))

    # sections and cross-references
    heads = list(re.finditer(r"^## §(0(?:\.\d+)?a?)(?: × 10(%s))?" % EXP, t, re.M))
    secs, order = {}, []
    for i, m in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(t)
        nl = t.index("\n", m.start())
        secs[m.group(1)] = dict(exp=m.group(2), body=t[nl:end])
        order.append(m.group(1))
    ref_re = re.compile(r"§(0(?:\.\d+)?a?)(?: × 10(%s))?" % EXP)
    cites = {s: {} for s in secs}
    dangling, mism, total = {}, [], 0
    for s in secs:
        for m in ref_re.finditer(secs[s]["body"]):
            total += 1
            tgt, e = m.group(1), m.group(2)
            if tgt not in secs:
                dangling[tgt] = dangling.get(tgt, 0) + 1; continue
            cites[s][tgt] = cites[s].get(tgt, 0) + 1
            if e and secs[tgt]["exp"] and e != secs[tgt]["exp"]:
                mism.append((s, tgt, e, secs[tgt]["exp"]))
    # references from the preamble (before the first heading)
    pre = t[:heads[0].start()] if heads else t
    for m in ref_re.finditer(pre):
        total += 1
        if m.group(1) not in secs:
            dangling[m.group(1)] = dangling.get(m.group(1), 0) + 1
    add("PASS" if not dangling else "FAIL", "refs resolve",
        "%d section refs, %d sections; dangling: %s" % (total, len(secs), dangling or "none"))
    add("PASS" if not mism else "FAIL", "exponent labels", "mismatches: %s" % (mism or "none"))

    # KORENINA references 1..6
    kor = [int(n) for g in re.findall(r"KORENINA((?: 0\.\d × 10¹(?: ·)?)+)", t)
           for n in re.findall(r"0\.(\d) × 10¹", g)]
    badk = sorted({n for n in kor if not 1 <= n <= 6})
    add("PASS" if not badk else "FAIL", "KORENINA refs", "%d refs; out of range: %s" % (len(kor), badk or "none"))

    # label collision between KORENINA items and a clause's own numbered items
    coll = []
    for s in secs:
        n = len(re.findall(r"^0\.[1-9] × 10¹\. ", secs[s]["body"], re.M))
        if n:
            coll.append((s, n))
    add("WARN" if coll else "PASS", "label collision",
        "clause items numbered like KORENINA (0.N × 10¹.): %s" % (coll or "none"))

    # algorithm name
    mangled, plain = t.count("SHA-0.256"), t.count("SHA-256")
    add("PASS" if mangled == 0 and plain > 0 else "FAIL", "algorithm name",
        "'SHA-0.256 x 10^3' x%d, 'SHA-256' x%d" % (mangled, plain))

    # machine record
    m = re.search(r"```json\n(.*?)\n```", t, re.S)
    if not m:
        add("NOT_RUN", "machine record", "no json block found")
    else:
        try:
            j = json.loads(m.group(1))
            d = str(j.get("date", ""))
            iso = bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}(T[\d:.]+(Z|[+-]\d\d:\d\d))?", d))
            add("PASS" if iso else "FAIL", "machine date", "date=%r ISO 8601: %s" % (d, iso))
            pd = str((j.get("predecessor") or {}).get("date", ""))
            has_commit = bool(j.get("commit") or (j.get("predecessor") or {}).get("commit"))
            same = pd == d and d != ""
            add("WARN" if same and not has_commit else "PASS", "version order",
                "predecessor date == current date: %s; commit id recorded: %s" % (same, has_commit))
        except Exception as e:
            add("FAIL", "machine record", "json does not parse: %s" % e)

    # number spelling (author's rule: quantities fragmented; names/identifiers literal)
    frag = len(re.findall(r"\d\.\d+ × 10%s" % EXP, t))
    words = re.findall(r"\b(?:thirty|twenty|forty|sixty|ninety)\b", t)
    add("WARN" if words else "PASS", "number spelling",
        "%d fragmented numbers; plain number words: %s" % (frag, words or "none"))

    # definitions
    evil = len(re.findall(r"\bEvil is\b", t))
    car_u = len(re.findall(r"\bcarrier\b", t, re.I))
    car_d = bool(re.search(r"^\s*carrier\s+—", t, re.M | re.I))
    add("WARN" if evil > 1 else "PASS", "one definition of 'evil'", "%d definitions found" % evil)
    add("WARN" if car_u and not car_d else "PASS", "'carrier' defined", "%d uses; definition line present: %s" % (car_u, car_d))

    # lineage
    a, b = t.find("LINEAGE"), t.find("A name that is not in this list")
    if a < 0 or b < 0:
        add("NOT_RUN", "lineage", "no LINEAGE block")
    else:
        lin = t[a:b]
        vs = []
        for v in re.findall(r"(?:AVL/VBL|AVL|VBL) (?:v)?(0\.\d+ × 10%s)" % EXP, lin):
            if v not in vs: vs.append(v)
        same_day = len(re.findall(r"October 0\.26 × 10², 0\.2026", lin))
        add("INFO", "lineage", "%d entries; %d dated 26 Oct; never on main: %d" %
            (len(vs), same_day, lin.count("nikoli na ⟨main⟩")))

    # manifest
    if manifest:
        want = None
        base = os.path.basename(path).replace("_", ".").lower()
        for line in open(manifest, encoding="utf-8"):
            if line.startswith("#") or "|" not in line: continue
            name, size, h = [x.strip() for x in line.split("|")[:3]]
            if name.replace("_", ".").lower() == base:
                want = (int(size), h.lower())
        if want is None:
            add("UNVERIFIED", "manifest", "no entry for this file name")
        else:
            ok = want == (len(raw), sha)
            add("PASS" if ok else "FAIL", "manifest", "size %d/%d, sha256 match: %s" % (want[0], len(raw), want[1] == sha))
    else:
        add("NOT_RUN", "manifest", "no --manifest given")

    add("NOT_RUN", "not checked", "authorship, publication history, legal effect, commit chain, whether text is right")
    return report(res, path, sha, len(raw), (secs, order, cites) if want_xref else None, want_json)


def report(res, path, sha, n, xr, as_json):
    if as_json:
        print(json.dumps({"file": path, "bytes": n, "sha256": sha,
                          "results": [dict(status=s, check=c, detail=d) for s, c, d in res]},
                         ensure_ascii=False, indent=2))
    else:
        print("file: %s  bytes: %d  sha256: %s" % (path, n, sha))
        for s, c, d in res:
            print("%-10s %-24s %s" % (s, c, d))
    if xr:
        secs, order, cites = xr
        cited = {s: set() for s in secs}
        for s in cites:
            for tg in cites[s]:
                if tg != s: cited[tg].add(s)
        print("\nxref map (section | cites -> | <- cited by)")
        for s in order:
            print("§%-5s | %s | %s" % (s, ",".join(sorted(cites[s], key=str)) or "-", ",".join(sorted(cited[s], key=str)) or "-"))
        print("never cited by another section:", [s for s in order if not cited[s]])
    return 1 if any(s == "FAIL" for s, _, _ in res) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
