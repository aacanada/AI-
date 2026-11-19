#!/usr/bin/env python3
"""Count SFX in every 60s window (step 1s) — brief: 4~8 per minute."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
tl = json.load(open(os.path.join(ROOT, "build", "timeline.json"), encoding="utf-8"))
ts = sorted(e["t"] for e in tl["sfx"])
lo, hi, bad = 99, 0, []
for s in range(0, int(tl["total"] - 60) + 1):
    n = sum(1 for t in ts if s <= t < s + 60)
    lo, hi = min(lo, n), max(hi, n)
    if n < 4 or n > 8: bad.append((s, n))
print("count", len(ts), "min/max per 60s", lo, hi, "violations", bad[:40])
