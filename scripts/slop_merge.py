#!/usr/bin/env python3
"""Merge no-ai-slop edits without breaking the hard rules.
Usage: slop_merge.py <pre.json> <edited.json> <brief.txt> > merged.json
Swaps edits in one item at a time and keeps each only if check.py still passes. Report goes to stderr."""
import json, os, subprocess, sys, tempfile

pre, post, brief = sys.argv[1:4]
CHECK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "check.py")
a, b = json.load(open(pre)), json.load(open(post))


def ok(d):
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as t:
        json.dump(d, t)
    r = subprocess.run([sys.executable, CHECK, t.name, brief], capture_output=True)
    os.unlink(t.name)
    return r.returncode == 0


if not ok(a):
    sys.exit("pre-slop file already fails check.py, fix that first")

out = json.loads(json.dumps(a))
for k, lab in (("hooks", "hook"), ("bodies", "body")):
    for i, (x, y) in enumerate(zip(a[k], b[k])):
        if x == y:
            continue
        out[k][i] = y
        if ok(out):
            print(f"KEEP   {lab} {i + 1}", file=sys.stderr)
        else:
            out[k][i] = x
            print(f"REVERT {lab} {i + 1} (breaks check.py)", file=sys.stderr)
json.dump(out, sys.stdout, indent=1)
