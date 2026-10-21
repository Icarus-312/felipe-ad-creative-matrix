#!/usr/bin/env python3
"""Deterministic checks on the writer's output. Usage: check.py <niche.json> [brief.txt]. Exit 1 on any FAIL."""
import json, re, sys

d = json.load(open(sys.argv[1]))
brief = open(sys.argv[2]).read() if len(sys.argv) > 2 else ""
hooks, bodies = d["hooks"], d["bodies"]
fails = []

def f(msg): fails.append(msg)

if len(hooks) != 10: f(f"need 10 hooks, got {len(hooks)}")
if len(bodies) != 2: f(f"need 2 bodies, got {len(bodies)}")

words = lambda s: len(s.split())
allowed_nums = set(re.findall(r"\d[\d,.]*", brief)) | {"50", "250", "0", "50,000", "250,000"}
niche_words = set(re.findall(r"[a-z]+", d.get("niche", "").lower()))
banned = [r"guarantee", r"approved", r"everyone", r"collateral", r"\bmonths?\b", r"\byears?\b", r"\bdays?\b",
          r"no credit check", r"—"]
proof = [r"\bowners (are|do|have)\b", r"\boperators (are|do|have)\b", r"\bclients?\b", r"\bmost (owner|people|operators|land)",
         r"\bmy (team|clients)\b"]

for i, h in enumerate(hooks, 1):
    if words(h) > 10: f(f"hook {i}: {words(h)} words (max 10): {h}")
    if "?" in h: f(f"hook {i}: question: {h}")
    if len(re.split(r"[.!]\s+", h.strip().rstrip(".!"))) != 2 and ", " not in h:
        f(f"hook {i}: not two beats: {h}")

firsts = [" ".join(h.lower().split()[:3]) for h in hooks]
dups = {x for x in firsts if firsts.count(x) > 1}
if dups: f(f"hooks share first 3 words: {sorted(dups)}")

labeled = [i for i, h in enumerate(hooks, 1)
           if re.match(r"^[A-Z][\w' -]*? (owners|operators|contractors|business owners)\b", h)]
if len(labeled) > 3: f(f"{len(labeled)} hooks open with an avatar label (max 3): hooks {labeled}")

for label, items, lo, hi in (("hook", hooks, 0, 10), ("body", bodies, 60, 80)):
    for i, t in enumerate(items, 1):
        for n in re.findall(r"\d[\d,.]*", t):
            n = n.rstrip(".,")
            if n and n not in allowed_nums: f(f"{label} {i}: number '{n}' not in brief or offer")
        for pat in banned:
            if re.search(pat, t, re.I): f(f"{label} {i}: banned pattern /{pat}/: {t[:70]}")
        for pat in proof:
            if re.search(pat, t, re.I): f(f"{label} {i}: possible invented proof /{pat}/: {t[:70]}")
        if label == "body" and not lo <= words(t) <= hi: f(f"body {i}: {words(t)} words (want {lo}-{hi})")

print("\n".join(f"FAIL {m}" for m in fails) or "PASS all deterministic checks")
print(f"hooks word counts: {[words(h) for h in hooks]}  bodies: {[words(b) for b in bodies]}")
sys.exit(1 if fails else 0)
