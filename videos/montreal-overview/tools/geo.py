"""Build SVG path data for the map scenes from Natural Earth (public domain).

Inputs (downloaded from github.com/nvkelso/natural-earth-vector):
  ne_50m_admin_1_states_provinces.geojson  -> Canada provinces
  ne_10m_admin_1_states_provinces.geojson  -> Island of Montreal / Laval (Quebec parts)
Run:  python3 -I tools/geo.py <dir-with-geojson>
Writes assets/geo/geo.json
"""
import json, math, os, sys

SRC = sys.argv[1]
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Lambert conformal conic (Statistics Canada parameters)
R = 6378137.0
phi1, phi2, phi0, lam0 = map(math.radians, (49.0, 77.0, 63.390675, -91.866667))
n = math.log(math.cos(phi1) / math.cos(phi2)) / math.log(math.tan(math.pi / 4 + phi2 / 2) / math.tan(math.pi / 4 + phi1 / 2))
F = math.cos(phi1) * math.tan(math.pi / 4 + phi1 / 2) ** n / n
rho0 = R * F / math.tan(math.pi / 4 + phi0 / 2) ** n


def lcc(lon, lat):
    phi, lam = math.radians(lat), math.radians(lon)
    rho = R * F / math.tan(math.pi / 4 + phi / 2) ** n
    return rho * math.sin(n * (lam - lam0)), rho0 - rho * math.cos(n * (lam - lam0))


def dp(pts, eps):
    if len(pts) < 3:
        return pts
    a, b = pts[0], pts[-1]
    dx, dy = b[0] - a[0], b[1] - a[1]
    L = math.hypot(dx, dy) or 1e-9
    idx, dmax = 0, 0
    for i in range(1, len(pts) - 1):
        d = abs(dy * pts[i][0] - dx * pts[i][1] + b[0] * a[1] - b[1] * a[0]) / L
        if d > dmax:
            idx, dmax = i, d
    if dmax > eps:
        return dp(pts[: idx + 1], eps)[:-1] + dp(pts[idx:], eps)
    return [a, b]


def fit(rings, W, H, pad):
    xs = [p[0] for r in rings for p in r]
    ys = [p[1] for r in rings for p in r]
    s = min((W - 2 * pad) / (max(xs) - min(xs)), (H - 2 * pad) / (max(ys) - min(ys)))
    ox = pad + ((W - 2 * pad) - (max(xs) - min(xs)) * s) / 2 - min(xs) * s
    oy = pad + ((H - 2 * pad) - (max(ys) - min(ys)) * s) / 2 + max(ys) * s
    return lambda x, y: (round(ox + x * s, 1), round(oy - y * s, 1))


def path(ring):
    return "M" + "L".join(f"{x},{y}" for x, y in ring) + "Z"


# ---------- Canada ----------
d50 = json.load(open(os.path.join(SRC, "ne_50m_admin_1_states_provinces.geojson")))
prov = {}
for f in d50["features"]:
    p = f["properties"]
    if p["admin"] != "Canada":
        continue
    g = f["geometry"]
    polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
    rings = []
    for poly in polys:
        ring = [lcc(*c) for c in poly[0]]
        rings.append(ring)
    prov[p["postal"]] = rings
allr = [r for rs in prov.values() for r in rs]
T = fit(allr, 1100, 860, 20)
EPS = 9000  # metres
canada = {}
for k, rings in prov.items():
    parts = []
    for r in rings:
        h = len(r) // 2
        s = dp(r[: h + 1], EPS)[:-1] + dp(r[h:], EPS)
        if len(s) < 4:
            continue
        xs = [q[0] for q in s]; ys = [q[1] for q in s]
        if (max(xs) - min(xs)) < 25000 and (max(ys) - min(ys)) < 25000:
            continue
        parts.append(path([T(*q) for q in s]))
    canada[k] = "".join(parts)
cities = {
    "montreal": (-73.5673, 45.5017), "vancouver": (-123.1207, 49.2827), "toronto": (-79.3832, 43.6532),
    "halifax": (-63.5752, 44.6488), "calgary": (-114.0719, 51.0447), "victoria": (-123.3656, 48.4284),
}
city_xy = {k: T(*lcc(*v)) for k, v in cities.items()}

# ---------- Island of Montreal (+ Laval) ----------
d10 = json.load(open(os.path.join(SRC, "ne_10m_admin_1_states_provinces.geojson")))
isl, laval = None, None
for f in d10["features"]:
    p = f["properties"]
    if p["admin"] == "Canada" and p["name"] in ("Québec", "Quebec"):
        for poly in f["geometry"]["coordinates"]:
            r = poly[0]
            xs = [c[0] for c in r]; ys = [c[1] for c in r]
            if -74.0 < min(xs) < -73.9 and max(xs) > -73.5 and min(ys) < 45.45 and max(ys) > 45.7:
                isl = r
            if -73.9 < min(xs) < -73.85 and max(ys) > 45.69 and min(ys) > 45.54:
                laval = r
assert isl and laval
k = math.cos(math.radians(45.55))
proj = lambda lon, lat: (lon * k, lat)
T2 = fit([[proj(*c) for c in isl]], 1000, 760, 40)
island = path([T2(*proj(*c)) for c in isl])
lav = path([T2(*proj(*c)) for c in laval])
downtown = T2(*proj(-73.5673, 45.5017))
out = {"canada": canada, "cities": city_xy, "island": island, "laval": lav, "downtown": downtown,
       "note": "Natural Earth admin-1 (public domain). Canada: 50m, LCC. Montreal island & Laval: 10m."}
os.makedirs(os.path.join(ROOT, "assets/geo"), exist_ok=True)
json.dump(out, open(os.path.join(ROOT, "assets/geo/geo.json"), "w"))
print({k: len(v) for k, v in canada.items()}, city_xy, downtown, len(island))
