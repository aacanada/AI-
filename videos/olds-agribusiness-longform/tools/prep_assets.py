"""Copy the photos the scenes use (webp -> jpg, max 1920 px wide). Run from project root:
    python3 -I tools/prep_assets.py
Source: ../../plans/olds-agribusiness-longform/assets/photos (Olds College official site, see SOURCES.md).
Output: assets/photos/<name>.jpg
"""
import os

from PIL import Image

SRC = os.path.join("..", "..", "plans", "olds-agribusiness-longform", "assets", "photos")
PH = os.path.join("assets", "photos")
os.makedirs(PH, exist_ok=True)

PHOTOS = """prog-08-agriculture-card prog-02-agribusiness-card prog-09-ag-sales campus-03-aerial-water-tower
hist-02-osa hist-03-1914-livestock-class campus-07-lsc sf-03-drone-flying sf-06-precision-ag sf-04-sensor
sf-15-crop-research prog-04-wsat-classroom sf-18-agexpert-farm-mgmt campus-04-students-walking
prog-10-pasture-to-plate prog-06-wsat-ag-students sf-07-smartag sf-11-canola sf-09-cattle campus-05-central-gardens
prog-01-student-with-crops sf-02-banner campus-02-aerial-full""".split()

for n in PHOTOS:
    src = next(os.path.join(SRC, n + e) for e in (".jpg", ".webp", ".png") if os.path.exists(os.path.join(SRC, n + e)))
    im = Image.open(src).convert("RGB")
    if im.width > 1920:
        im = im.resize((1920, round(im.height * 1920 / im.width)), Image.LANCZOS)
    im.save(os.path.join(PH, n + ".jpg"), quality=86, optimize=True)
print(f"{len(PHOTOS)} photos -> {PH}")
