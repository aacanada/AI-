"""Copy/resize the photos the scenes use and cut brochure crops. Run from project root:
    python3 -I tools/prep_assets.py
Source: ../../plans/sga-longform/assets (photos + brochure). Output: assets/photos, assets/brochure.
"""
import os
from collections import deque

from PIL import Image

SRC = os.path.join("..", "..", "plans", "sga-longform", "assets")
PH = os.path.join("assets", "photos")
BR = os.path.join("assets", "brochure")
os.makedirs(PH, exist_ok=True)
os.makedirs(BR, exist_ok=True)

PHOTOS = """campus-01-class-whiteboard campus-02-class-desks campus-04-lounge-pingpong campus-06-counselling
campus-07-lobby-flags campus-13-lobby campus-18-hallway grad-01-2025-stage grad-02-gowns grad-04-2025-group
life-01-island-cntower life-04-group-hall life-07-island-banner life-08-soccer life-09-picnic life-18-island-banner-wide
res-01-kitchen res-02-house town-03-northyork-aerial town-04-mall town-05-foodcourt town-07-earl-haig
town-08-cardinal-carter town-09-tdsb town-11-subway town-12-nyc-station town-13-northyork-centre town-14-library
town-15-fitness town-16-pool town-18-building-5ph town-20-artcentre""".split()


def find(name):
    for ext in (".jpg", ".png"):
        p = os.path.join(SRC, "photos", name + ext)
        if os.path.exists(p):
            return p
    raise FileNotFoundError(name)


for n in PHOTOS:
    im = Image.open(find(n)).convert("RGB")
    if im.width > 1920:
        im = im.resize((1920, round(im.height * 1920 / im.width)), Image.LANCZOS)
    im.save(os.path.join(PH, n + ".jpg"), quality=84, optimize=True)

# logos keep alpha
crest = Image.open(os.path.join(SRC, "photos", "logo-crest.png")).convert("RGBA")
crest.thumbnail((800, 900), Image.LANCZOS)
crest.save(os.path.join(PH, "logo-crest.png"), optimize=True)
tc = Image.open(os.path.join(SRC, "photos", "town-10-tcdsb-logo.png")).convert("RGB")
tc.thumbnail((600, 600), Image.LANCZOS)
tc.save(os.path.join(PH, "town-10-tcdsb-logo.jpg"), quality=88)


def crop(page, box, out, w=None):
    im = Image.open(os.path.join(SRC, "brochure", page + ".jpg")).convert("RGB").crop(box)
    if w and im.width > w:
        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    im.save(os.path.join(BR, out + ".jpg"), quality=86, optimize=True)


def key_white(page, box, out, thr=236):
    """Cut a mascot off a white page: flood-fill near-white from the crop edges to transparent."""
    im = Image.open(os.path.join(SRC, "brochure", page + ".jpg")).convert("RGBA").crop(box)
    px = im.load()
    W, H = im.size
    seen = bytearray(W * H)
    dq = deque([(x, y) for x in range(W) for y in (0, H - 1)] + [(x, y) for y in range(H) for x in (0, W - 1)])
    while dq:
        x, y = dq.popleft()
        if not (0 <= x < W and 0 <= y < H) or seen[y * W + x]:
            continue
        seen[y * W + x] = 1
        r, g, b, _ = px[x, y]
        if min(r, g, b) < thr:
            continue
        px[x, y] = (r, g, b, 0)
        dq.extend(((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))
    im.save(os.path.join(BR, out + ".png"), optimize=True)


crop("br-01-cover", (0, 0, 2400, 1350), "cover", 1920)
crop("br-01-cover", (360, 340, 800, 820), "cover-crest")
# residences: house-photo parts of each card (text overlay avoided)
crop("br-15-residences", (600, 492, 816, 832), "res-h1")
crop("br-15-residences", (850, 492, 1110, 832), "res-h2")
crop("br-15-residences", (2060, 488, 2290, 832), "res-h3")
crop("br-15-residences", (114, 870, 384, 1216), "res-h4")
crop("br-15-residences", (848, 870, 1110, 1216), "res-h5")
crop("br-18-meals", (112, 452, 1620, 1094), "meals-grid")
crop("br-19-morning-snack", (1270, 580, 2240, 820), "snack-items")
crop("br-07-oly-question", (1640, 520, 2260, 1300), "oly-question-card")
# mascots on white background (br-19 owls row)
key_white("br-19-morning-snack", (1262, 940, 1532, 1222), "oly-1")
key_white("br-19-morning-snack", (1540, 940, 1802, 1222), "oly-2")
key_white("br-19-morning-snack", (1812, 940, 2080, 1222), "oly-3")
key_white("br-19-morning-snack", (2084, 940, 2350, 1222), "oly-4")
print("photos", len(PHOTOS) + 3, "brochure crops done")
