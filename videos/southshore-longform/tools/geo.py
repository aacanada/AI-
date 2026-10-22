"""Schematic map of Montreal and the South Shore (Rive-Sud) for the long-form.

The sandbox cannot reach OpenStreetMap servers and the generalized OSM water layer on npm is too coarse at this
scale, so the brief's fallback applies: a hand-drawn schematic built from real coordinates (island shore, river,
south shore, REM stations and school pins from the brief, OSM Nominatim 2026-10-22). Shapes are simplified on
purpose: "island / river / south shore" must read at a glance, exact coastline is not the goal.

Map units: equirectangular around 45.5N, 1 km = U map units. map_xy(lat, lon) -> (x, y) in the map SVG.
"""
import math

LON0, LAT0 = -74.05, 45.75          # map top-left
LON1, LAT1 = -73.15, 45.20          # map bottom-right
U = 30.0                            # map units per km
KX = 111.32 * math.cos(math.radians(45.5))
KY = 111.13
W = round((LON1 - LON0) * KX * U)
H = round((LAT0 - LAT1) * KY * U)


def map_xy(lat, lon):
    return ((lon - LON0) * KX * U, (LAT0 - lat) * KY * U)


def _path(pts, close=True):
    xy = [map_xy(la, lo) for la, lo in pts]
    d = "M" + " L".join(f"{x:.0f},{y:.0f}" for x, y in xy)
    return d + (" Z" if close else "")


def _smooth(pts, close=True):
    """Catmull-Rom through the points -> cubic Bezier path (softer, map-like shores)."""
    xy = [map_xy(la, lo) for la, lo in pts]
    n = len(xy)
    if close:
        get = lambda i: xy[i % n]
        rng = range(n)
    else:
        get = lambda i: xy[min(max(i, 0), n - 1)]
        rng = range(n - 1)
    d = f"M{xy[0][0]:.0f},{xy[0][1]:.0f}"
    for i in rng:
        p0, p1, p2, p3 = get(i - 1), get(i), get(i + 1), get(i + 2)
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f" C{c1[0]:.0f},{c1[1]:.0f} {c2[0]:.0f},{c2[1]:.0f} {p2[0]:.0f},{p2[1]:.0f}"
    return d + (" Z" if close else "")


# ---- shorelines (lat, lon) ------------------------------------------------------------------------------------
# Montreal island, clockwise from the west tip (Sainte-Anne-de-Bellevue)
ISLAND = [
    (45.405, -73.955), (45.430, -73.930), (45.458, -73.885), (45.488, -73.832), (45.512, -73.775),
    (45.533, -73.722), (45.558, -73.672), (45.583, -73.622), (45.613, -73.572), (45.652, -73.532),
    (45.690, -73.492), (45.702, -73.474), (45.694, -73.478), (45.660, -73.497), (45.622, -73.510),
    (45.586, -73.521), (45.552, -73.535), (45.525, -73.543), (45.503, -73.549), (45.487, -73.560),
    (45.470, -73.575), (45.456, -73.583), (45.443, -73.612), (45.432, -73.665), (45.430, -73.720),
    (45.425, -73.772), (45.415, -73.830), (45.405, -73.885),
]
# Île des Sœurs (Nuns' Island)
NUNS = [(45.476, -73.552), (45.472, -73.538), (45.463, -73.529), (45.455, -73.536), (45.458, -73.551), (45.468, -73.556)]
# Laval (north of Rivière des Prairies): we only need the river band, drawn as a stroke along the north shore
NORTH_RIVER = [(45.395, -73.985), (45.440, -73.935), (45.470, -73.890), (45.500, -73.836), (45.524, -73.779),
               (45.545, -73.725), (45.570, -73.675), (45.595, -73.625), (45.625, -73.576), (45.663, -73.537),
               (45.700, -73.500), (45.722, -73.475), (45.75, -73.455)]
# South shore of the St. Lawrence, from the north-east (Varennes) back to the south-west (Châteauguay)
SOUTH = [
    (45.760, -73.405), (45.700, -73.428), (45.660, -73.440), (45.622, -73.452), (45.592, -73.463),
    (45.562, -73.487), (45.537, -73.509), (45.518, -73.521), (45.501, -73.526), (45.486, -73.521),
    (45.470, -73.509), (45.452, -73.497), (45.432, -73.494), (45.414, -73.505), (45.403, -73.540),
    (45.396, -73.600), (45.383, -73.670), (45.362, -73.745), (45.345, -73.830), (45.333, -73.930), (45.330, -74.060),
]
# Lac des Deux Montagnes / Lac Saint-Louis edge west of the island (closes the water polygon)
WEST = [(45.330, -74.060), (45.560, -74.060), (45.470, -73.995), (45.430, -73.965)]
RICHELIEU = [(45.200, -73.275), (45.262, -73.262), (45.315, -73.252), (45.372, -73.262), (45.430, -73.282),
             (45.470, -73.268), (45.520, -73.225), (45.560, -73.200)]

# ---- REM South Shore branch (brief, OSM Nominatim) -------------------------------------------------------------
REM_STATIONS = [
    ("brossard", "브로사드", 45.4374, -73.4325),
    ("quartier", "뒤 카르티에", 45.4467, -73.4333),
    ("panama", "파나마", 45.4650, -73.4704),
    ("ids", "일데쇠르", 45.4703, -73.5389),
    ("gare", "중앙역", 45.5000, -73.5666),
]
REM_LINE = [(45.4374, -73.4325), (45.4467, -73.4333), (45.4560, -73.4500), (45.4650, -73.4704),
            (45.4668, -73.5000), (45.4690, -73.5250), (45.4703, -73.5389), (45.4790, -73.5530),
            (45.4900, -73.5610), (45.5000, -73.5666)]
CHAMPLAIN = [(45.4690, -73.5250), (45.4668, -73.5000), (45.4655, -73.4900)]  # Samuel De Champlain Bridge span
OTHER_BRIDGES = [  # Jacques-Cartier, Victoria (thin, context only)
    [(45.5225, -73.5440), (45.5240, -73.5215)],
    [(45.4930, -73.5500), (45.4985, -73.5260)],
]

# ---- places (label anchors) --------------------------------------------------------------------------------------
CITIES = [  # key, Korean label, lat, lon  (order = narration order in S02)
    ("brossard", "브로사드", 45.452, -73.468),
    ("stlambert", "생랑베르", 45.503, -73.507),
    ("longueuil", "롱게일", 45.535, -73.482),
    ("greenfield", "그린필드파크", 45.486, -73.471),
    ("sthubert", "생위베르", 45.500, -73.405),
    ("boucherville", "부셔빌", 45.598, -73.438),
    ("stbruno", "생브루노", 45.530, -73.345),
]
DOWNTOWN = (45.503, -73.568)
SJSR = ("생장쉬르리슐리외", 45.3151, -73.2725)

HIGH = [  # key, label, lat, lon, video
    ("heritage", "헤리티지", 45.4913, -73.3914, "heritage"),
    ("centennial", "센테니얼", 45.4917, -73.4465, "centennial"),
    ("sli", "생랑베르 인터내셔널", 45.5102, -73.5045, "sli"),
    ("stjohns", "세인트 존스", 45.3151, -73.2725, "stjohns"),
]
ELEM = [
    ("goodshepherd", "굿셰퍼드", 45.4729, -73.4539),
    ("napper", "해롤드 내퍼", 45.4637, -73.4454),
    ("stlambertel", "생랑베르 초등", 45.5023, -73.5099),
    ("gpi", "그린필드파크 인터내셔널", 45.4825, -73.4714),
    ("cpi", "코틀랜드파크 인터내셔널", 45.5326, -73.3568),
    ("boucherville", "부셔빌 초등", 45.6205, -73.4463),
]

WATER = "#CFDCE3"      # brief: only the river may be a pale grey-blue
WATER_LINE = "#B7C9D3"
LAND = "#FFF8F2"
ISLAND_FILL = "#F6E6E1"
SOUTH_FILL = "#FFE9E4"


def water_path():
    """St. Lawrence between the south shore and the island's south shore (+ Lac Saint-Louis), and the lakes west of
    the island. ISLAND runs west tip -> north shore -> east tip (index 11) -> south shore back west."""
    island_south_we = [ISLAND[0]] + ISLAND[12:][::-1] + [ISLAND[11]]
    river = SOUTH + [(45.395, -74.060)] + island_south_we + [(45.760, -73.445)]
    lakes = [(45.395, -74.060), (45.560, -74.060), (45.470, -73.985), (45.432, -73.952), (45.405, -73.955)]
    return _smooth(river) + " " + _smooth(lakes)


def svg_map(cls="mapsvg", south_hi=False, with_island_tint=True):
    """Base map SVG (no labels). The scene adds labels/pins as HTML on top, positioned with map_xy."""
    island = _smooth(ISLAND)
    south_band = _smooth(SOUTH + [(45.20, -74.06), (45.20, -73.10), (45.76, -73.10)])
    parts = [
        f'<rect x="0" y="0" width="{W}" height="{H}" fill="{LAND}"/>',
        f'<path class="southband" d="{south_band}" fill="{SOUTH_FILL if south_hi else LAND}"/>',
        f'<path class="island" d="{island}" fill="{ISLAND_FILL if with_island_tint else LAND}"/>',
        f'<path class="water" d="{water_path()}" fill="{WATER}" fill-rule="evenodd" stroke="{WATER_LINE}" stroke-width="6"/>',
        f'<path class="nriver" d="{_smooth(NORTH_RIVER, False)}" fill="none" stroke="{WATER}" stroke-width="34" stroke-linecap="round"/>',
        f'<path class="richelieu" d="{_smooth(RICHELIEU, False)}" fill="none" stroke="{WATER}" stroke-width="26" stroke-linecap="round"/>',
        f'<path class="nuns" d="{_smooth(NUNS)}" fill="{ISLAND_FILL}" stroke="{WATER_LINE}" stroke-width="4"/>',
    ]
    for b in OTHER_BRIDGES:
        parts.append(f'<path class="obridge" d="{_path(b, False)}" stroke="#D9C4BF" stroke-width="10" stroke-linecap="round" fill="none"/>')
    return f'<svg class="{cls}" viewBox="0 0 {W} {H}" width="{W}" height="{H}">{"".join(parts)}</svg>'


def rem_path_d():
    return _path(REM_LINE, False)


def champlain_d():
    return _path(CHAMPLAIN, False)


def rem_length_units():
    xy = [map_xy(*p) for p in REM_LINE]
    return sum(math.dist(a, b) for a, b in zip(xy, xy[1:]))


def view(lat, lon, km_wide, frame_w=1920, frame_h=1080, cx=960, cy=470):
    """Camera: CSS transform that puts (lat, lon) at frame point (cx, cy) with `km_wide` km across the frame."""
    s = frame_w / (km_wide * U)
    x, y = map_xy(lat, lon)
    return dict(scale=round(s, 5), x=round(cx - x * s, 1), y=round(cy - y * s, 1))


def screen(lat, lon, v):
    x, y = map_xy(lat, lon)
    return (x * v["scale"] + v["x"], y * v["scale"] + v["y"])


if __name__ == "__main__":
    print(W, H, round(rem_length_units() / U, 1), "km drawn REM")
