#!/usr/bin/env python3
"""Scaffold videos/<slug>/ from the AA Canada shorts template.

Copies the HyperFrames project config, the blue-professional frame.md, the caption
skin, Pretendard fonts and a local GSAP (the render sandbox cannot reach jsDelivr).

  python3 new_project.py <slug> [--title "영상 제목"]
"""
import argparse, datetime, json, os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "..", "template")
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
PIN = "hyperframes@0.8.114"

ap = argparse.ArgumentParser()
ap.add_argument("slug")
ap.add_argument("--title", default="")
a = ap.parse_args()

dst = os.path.join(REPO, "videos", a.slug)
if os.path.exists(dst) and os.listdir(dst):
    sys.exit(f"✗ {dst} already exists and is not empty")
shutil.copytree(TEMPLATE, dst, dirs_exist_ok=True)
for d in ("compositions/frames", "assets/voice", "renders", "scripts"):
    os.makedirs(os.path.join(dst, d), exist_ok=True)
json.dump({"id": a.slug, "name": a.title or a.slug,
           "createdAt": datetime.datetime.now(datetime.timezone.utc).isoformat()},
          open(os.path.join(dst, "meta.json"), "w"), ensure_ascii=False, indent=2)
json.dump({"name": a.slug, "private": True, "type": "module", "scripts": {
    "dev": f"npx --yes {PIN} preview", "check": f"npx --yes {PIN} check",
    "render": f"npx --yes {PIN} render", "publish": f"npx --yes {PIN} publish"}},
    open(os.path.join(dst, "package.json"), "w"), indent=2)
print(f"✓ scaffolded {os.path.relpath(dst, REPO)}")
