#!/usr/bin/env python3
"""Assemble, validate, snapshot and render an AA Canada short (after frames are built).

Runs the faceless-explainer post-build pipeline plus the house fixes:
sync durations → captions (moved to the TOP band) → assemble index → transitions →
local GSAP (jsDelivr is blocked in the render sandbox) → caption track kind →
background clip durations → lint + check → [snapshots] → [render].

  python3 finish.py --project videos/<slug> [--snapshot] [--render]
"""
import argparse, glob, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
FX = os.path.abspath(os.path.join(HERE, "..", "..", "faceless-explainer", "scripts"))
CAPTION_TOP, CAPTION_H = 170, 190

ap = argparse.ArgumentParser()
ap.add_argument("--project", required=True)
ap.add_argument("--snapshot", action="store_true", help="contact sheet at each frame's landed state")
ap.add_argument("--render", action="store_true")
a = ap.parse_args()
P = os.path.abspath(a.project)


def run(cmd, check=True, quiet=False):
    r = subprocess.run(cmd, cwd=P, capture_output=True, text=True)
    out = (r.stdout + r.stderr).strip()
    if not quiet and out:
        print("\n".join(out.splitlines()[-6:]))
    if check and r.returncode != 0:
        print(out)
        sys.exit(f"✗ failed: {' '.join(cmd)}")
    return out


def sub(path, pat, rep, count=0):
    s = open(path).read()
    s2 = re.sub(pat, rep, s, count=count, flags=re.M)
    open(path, "w").write(s2)
    return s != s2


sb, am = "./STORYBOARD.md", "./audio_meta.json"
run(["node", f"{FX}/audio.mjs", "sync-durations", "--audio-meta", am, "--storyboard", sb])
run(["node", f"{FX}/captions.mjs", "build", "--storyboard", sb, "--audio-meta", am, "--hyperframes", ".", "--out", "./caption_groups.json"])
cap = os.path.join(P, "compositions/captions.html")
sub(cap, r"--cap-band-top: \d+px;", f"--cap-band-top: {CAPTION_TOP}px;")
sub(cap, r"--cap-band-height: \d+px;", f"--cap-band-height: {CAPTION_H}px;")
run(["node", f"{FX}/assemble-index.mjs", "--storyboard", sb, "--hyperframes", "."])
run(["node", f"{FX}/transitions.mjs", "inject", "--storyboard", sb, "--hyperframes", "."])
run(["node", f"{FX}/transitions.mjs", "verify", "--storyboard", sb, "--index", "./index.html"])

idx = os.path.join(P, "index.html")
for f in (idx, cap):
    sub(f, r'<script src="https://cdn\.jsdelivr\.net/npm/gsap@[^"]+/dist/gsap\.min\.js"[^>]*></script>',
        '<script src="assets/vendor/gsap.min.js"></script>')
if 'data-track-kind="captions"' not in open(idx).read():
    sub(idx, r'^(\s*)id="el-captions"$', r'\1id="el-captions"\n\1data-track-kind="captions"', count=1)

# The full-bleed background clip must last as long as the (transition-padded) frame root.
for p in sorted(glob.glob(os.path.join(P, "compositions/frames/*.html"))):
    s = open(p).read()
    m = re.search(r'data-composition-id="[^"]+" data-start="0" data-duration="([\d.]+)"', s)
    if m:
        s = re.sub(r'(<div id="[^"]*bg" class="[^"]*clip" data-start="0" data-duration=")[\d.]+(")', rf"\g<1>{m.group(1)}\2", s)
        open(p, "w").write(s)

lint = run(["npx", "hyperframes", "lint"], check=False, quiet=True)
print("lint:", lint.splitlines()[-1] if lint else "?")
if re.search(r"[1-9]\d* error", lint):
    print(lint)
    sys.exit("✗ lint errors")
chk = run(["npx", "hyperframes", "check"], check=False, quiet=True)
print("check:", next((l.strip() for l in chk.splitlines() if "Check " in l), "?"))
if "Check passed" not in chk:
    print("\n".join(l for l in chk.splitlines() if "✗" in l or "error" in l.lower()))
    sys.exit("✗ check failed — fix the named frame element and rerun")

if a.snapshot:
    # landed state of each frame: just before its end (skipping the transition tail)
    meta = json.load(open(os.path.join(P, "audio_meta.json")))
    t, times = 0.0, []
    for v in sorted(meta["voices"], key=lambda v: v["frame"]):
        times.append(round(t + v["duration_s"] - 0.3, 2))
        t += v["duration_s"]
    run(["rm", "-rf", "snapshots"])
    run(["npx", "hyperframes", "snapshot", "--at", ",".join(map(str, times))], quiet=True)
    print("✓ snapshots/contact-sheet.jpg")

if a.render:
    out = run(["npx", "hyperframes", "render", "--skill=faceless-explainer", "--quality", "high",
               "--output", "renders/video.mp4"], quiet=True)
    print("\n".join(l.strip() for l in out.splitlines() if " MB · " in l))
    print("✓ renders/video.mp4")
