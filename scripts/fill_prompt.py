#!/usr/bin/env python3
"""Fill the ad-copy prompt template. Usage: fill_prompt.py <template> <niche> <brief.txt>
Prints the filled prompt. Exits 1 if the template (e.g. after a Lyra pass) dropped a required constraint."""
import sys

tpl, niche, brief_path = sys.argv[1], sys.argv[2], sys.argv[3]
text = open(tpl).read()
required = [
    "[NICHE]", "[AVATAR_BRIEF]",
    "$50K to $250K from the bank at 0% interest",
    "DM me SCALE to learn how",
    "Proof I can claim: NONE",
    "UNKNOWN",
    "10 words or fewer",
    "two beats",
    "first 3 words",
    "reframe",
    "personal guarantees or collateral",
    "No timeline",
    "valid JSON",
    "NEITHER body contains a CTA",
]
missing = [r for r in required if r.lower() not in text.lower()]
if missing:
    sys.stderr.write("GUARD FAIL, template dropped: " + "; ".join(missing) + "\n")
    sys.exit(1)
sys.stdout.write(text.replace("[NICHE]", niche).replace("[AVATAR_BRIEF]", open(brief_path).read().strip()))
