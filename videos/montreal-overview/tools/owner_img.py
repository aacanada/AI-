"""Prepare the director's images (plans/montreal-overview/assets/owner/) for motion.

The finished frame always shows each picture exactly as supplied: label/legend pieces are cut out
of the original and laid back on top at the same pixel position, so they can pop in one by one.
Under them, the base copy has those pieces removed (inpainted map / white legend box).
Run: python3 -I tools/owner_img.py   -> assets/img/owner/*, assets/img/owner/rects.json
"""
import json, os, shutil
import cv2
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "..", "..", "plans", "montreal-overview", "assets", "owner")
OUT = os.path.join(ROOT, "assets", "img", "owner")
os.makedirs(OUT, exist_ok=True)
for f in ("region-map-abcd.png", "city-population.png", "statcan-rent-2026q2.jpg", "pcap2023-math.png"):
    shutil.copy(os.path.join(SRC, f), os.path.join(OUT, f))

# rent infographic: city labels (name + price box), x0,y0,x1,y1 in source pixels
RENT = {"van": (36, 770, 208, 870), "tor": (820, 975, 972, 1074), "hal": (834, 688, 988, 790), "ott": (476, 860, 724, 979),
        "cal": (292, 962, 444, 1064), "edm": (282, 732, 448, 834), "mtl": (572, 710, 724, 812)}
im = cv2.imread(os.path.join(SRC, "statcan-rent-2026q2.jpg"))
hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
ink = ((hsv[..., 2] < 150) | (hsv[..., 1] > 90)).astype(np.uint8)
ink[:640] = 0; ink[1110:] = 0  # map area only (keeps the title and footer untouched)
n, lab = cv2.connectedComponents(cv2.dilate(ink, np.ones((5, 5), np.uint8)), connectivity=8)
union = np.zeros(im.shape[:2], np.uint8)
for k, (x0, y0, x1, y1) in RENT.items():
    m = np.zeros(im.shape[:2], np.uint8)
    m[y0:y1, x0:x1] = 1
    for c in np.unique(lab[y0 - 4:y1 + 4, x0 - 4:x1 + 4]):
        if c:
            m[lab == c] = 1
    m = cv2.dilate(m, np.ones((5, 5), np.uint8))
    union |= m
    rgba = cv2.cvtColor(im, cv2.COLOR_BGR2BGRA)
    rgba[..., 3] = m * 255
    ys, xs = np.nonzero(m)
    X0, Y0, X1, Y1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
    cv2.imwrite(os.path.join(OUT, f"rent-{k}.png"), rgba[Y0:Y1, X0:X1])
    RENT[k] = (int(X0), int(Y0), int(X1), int(Y1))
cv2.imwrite(os.path.join(OUT, "rent-base.jpg"), cv2.inpaint(im, union * 255, 9, cv2.INPAINT_TELEA), [cv2.IMWRITE_JPEG_QUALITY, 95])

# region map: legend lines (white box) -> base has white box, lines are sprites
REG = {"l1": (26, 28, 456, 72), "l2": (26, 72, 456, 115), "l3": (26, 115, 456, 158), "l4": (26, 158, 456, 202)}
rm = cv2.imread(os.path.join(SRC, "region-map-abcd.png"))
base = rm.copy()
for k, (x0, y0, x1, y1) in REG.items():
    cv2.imwrite(os.path.join(OUT, f"region-{k}.png"), rm[y0:y1, x0:x1])
    base[y0:y1, x0:x1] = (255, 255, 255)
cv2.imwrite(os.path.join(OUT, "region-base.png"), base)
json.dump({"rent": RENT, "region": REG}, open(os.path.join(OUT, "rects.json"), "w"))
print("ok")
