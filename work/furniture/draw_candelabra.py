#!/usr/bin/env python3
"""Candelabra — field plate V1R00. A five-arm sterling branch, straight on
with a whisper of asymmetry so the silver doesn't read machined: domed foot,
baluster stem, four scrolled arms carrying stubby beeswax candles burned
low, wax run down the stem and frozen mid-drip. The five flames are the only
light on the plate — a power-cut mood, warm bloom inside cold silver dark.
1000x1000. Turned-ware construction: lathe profiles + ribbon arms.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Candelabra — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#1A1210"   # warm dark, not black
AX = 500          # stem axis
EXTENT = []


def stops(*pairs):
    out = []
    for p in pairs:
        s = {"offset": p[0], "color": p[1]}
        if len(p) > 2:
            s["opacity"] = p[2]
        out.append(s)
    return out


def lin(a, b, *pairs):
    return {"gradient": {"kind": "linear", "start": [round(a[0], 1), round(a[1], 1)],
                         "end": [round(b[0], 1), round(b[1], 1)], "stops": stops(*pairs)}}


def rad(*pairs):
    return {"gradient": {"kind": "radial", "stops": stops(*pairs)}}


def poly(pts):
    return "M%.1f,%.1f " % pts[0] + " ".join("L%.1f,%.1f" % p for p in pts[1:]) + " Z"


def smooth(pts, closed=True, move=True):
    n = len(pts)

    def g(i):
        return pts[i % n] if closed else pts[max(0, min(n - 1, i))]
    s = ("M%.1f,%.1f" if move else "L%.1f,%.1f") % pts[0]
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        p0, p1, p2, p3 = g(i - 1), g(i), g(i + 1), g(i + 2)
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        s += " C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (c1 + c2 + p2)
    return s + (" Z" if closed else "")


def lathe(profile, ax=AX):
    """Right-half profile [(x,y)...] bottom->top -> closed symmetric silhouette."""
    left = [(2 * ax - x, y) for x, y in reversed(profile)]
    for p in profile + left:
        EXTENT.append(p)
    return smooth(profile + left)


def cubic(p0, p1, p2, p3, n=24):
    return [tuple((1 - t) ** 3 * p0[k] + 3 * (1 - t) ** 2 * t * p1[k] +
                  3 * (1 - t) * t * t * p2[k] + t ** 3 * p3[k] for k in (0, 1))
            for t in [i / n for i in range(n + 1)]]


def ribbon(name, spine, w0, w1, fill, ink=1.8, bulge=0.0):
    """Tapered filled ribbon along a spine polyline (half-width w0->w1)."""
    n = len(spine)
    left, right = [], []
    for i, p in enumerate(spine):
        q0 = spine[max(0, i - 1)]
        q1 = spine[min(n - 1, i + 1)]
        tx, ty = q1[0] - q0[0], q1[1] - q0[1]
        L = math.hypot(tx, ty) or 1
        nx, ny = -ty / L, tx / L
        w = (w0 + (w1 - w0) * i / (n - 1)) * (1 + bulge * math.sin(math.pi * i / (n - 1)))
        left.append((p[0] + nx * w, p[1] + ny * w))
        right.append((p[0] - nx * w, p[1] - ny * w))
    for p in left + right:
        EXTENT.append(p)
    d.path(smooth(left, closed=False) + " " + smooth(right[::-1], closed=False, move=False) + " Z",
           name, fill=fill, stroke=INK, strokeWidth=ink, join="round")
    return left, right


# --- backdrop + plate ---------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#10151C"), (1, "#05070A")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#5A6C80", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#4C545E"), (0.6, "#30363E"), (1, "#10141A")),
        stroke="#0A0D12", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C6D0DA", strokeWidth=3, opacity=24)

# the candles are the light: one wide warm bloom centred on the flame row
d.shape("ellipse", "Candle bloom", x=200, y=120, width=600, height=520,
        fill=rad((0, "#E8963C", 24), (0.45, "#A8621E", 8), (1, "#A8621E", 0)),
        stroke=NONE)

FY = 742
hx = math.sqrt(PR ** 2 - (FY - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{FY} L{PCX + hx:.1f},{FY} A420,420 0 0 1 {PCX - hx:.1f},{FY} Z",
       "Floor", fill=lin((0, FY), (0, 880), (0, "#3E4650", 40), (1, "#0C1014", 76)),
       stroke=NONE)
d.path(f"M{PCX - hx + 6:.1f},{FY} L{PCX + hx - 6:.1f},{FY}", "Floor edge light",
       fill=NONE, stroke="#D4DEE8", strokeWidth=2, opacity=16)
# warm pool the flames throw on the dark table
d.shape("ellipse", "Floor light pool", x=300, y=716, width=400, height=52,
        fill=rad((0, "#D89034", 20), (1, "#D89034", 0)), stroke=NONE)
d.shape("ellipse", "Candelabra shadow", x=400, y=714, width=200, height=26,
        fill=rad((0, "#030405", 75), (0.65, "#030405", 32), (1, "#030405", 0)),
        stroke=NONE)

# --- sterling palette ---------------------------------------------------------------
def silver(y0, y1):
    return lin((0, y0), (0, y1),
               (0, "#232A30"), (0.30, "#6E7880"), (0.46, "#C8D2DA"),
               (0.56, "#E8EEF2"), (0.72, "#78828A"), (1, "#1E242A"))


def silver_x(x0, x1):
    return lin((x0, 0), (x1, 0),
               (0, "#2A3238"), (0.35, "#96A2AA"), (0.5, "#DDE5EA"),
               (0.68, "#828C94"), (1, "#242B31"))


WAX_D, WAX_L = "#B9A88A", "#F6EDD8"

# --- foot + stem: one turned-silver silhouette -----------------------------------------
stem_profile = [(402, 710), (406, 702), (416, 696), (432, 688), (450, 680),
                (464, 672), (474, 662), (476, 650), (470, 640), (461, 628),
                (457, 614), (453, 598), (451, 582), (455, 570), (462, 560),
                (468, 552), (472, 542), (468, 534), (460, 528), (455, 518),
                (453, 506), (456, 492), (462, 480), (468, 472), (470, 462),
                (468, 452), (461, 446), (458, 438), (460, 428)]
d.path(lathe(stem_profile), "Foot and stem", fill=silver(428, 708),
       stroke=INK, strokeWidth=2.2, join="round")
# foot rim light + turning grooves on the knops
d.shape("ellipse", "Foot rim", x=402, y=701, width=196, height=15,
        fill=NONE, stroke="#DDE5EA", strokeWidth=2.2, opacity=42)
for i, (y, rx) in enumerate([(557, 15), (476, 14), (438, 13)]):
    d.shape("ellipse", f"Knop groove {i+1}", x=AX - rx, y=y - 2, width=2 * rx,
            height=5, fill=NONE, stroke="#14181C", strokeWidth=1.6, opacity=55)
# stem sheen, left edge catching flame light
d.path("M452,690 C443,650 440,600 445,556 C448,530 452,508 458,488", "Stem sheen",
       fill=NONE, stroke="#F2E4C8", strokeWidth=5, opacity=34, cap="round")
# warm flame-light reflected up the right of the stem
d.path("M548,690 C557,650 560,600 555,556 C552,530 548,510 542,492", "Stem warm",
       fill=NONE, stroke="#C8883C", strokeWidth=4, opacity=30, cap="round")

# --- wax run down the stem: drips that froze mid-slide ------------------------------------
for i, (x, y0, y1, w) in enumerate([(486, 452, 560, 4.5), (512, 440, 518, 3.6),
                                    (494, 460, 502, 3.0)]):
    drip = [(x - w, y0), (x + w, y0), (x + w * 0.8, y1 - 14),
            (x + w * 0.4, y1), (x - w * 0.4, y1), (x - w * 0.8, y1 - 14)]
    d.path(smooth(drip), f"Stem wax drip {i+1}",
           fill=lin((0, y0), (0, y1), (0, "#EFE4CC", 92), (1, "#C4B294", 88)),
           stroke="#9A8A6E", strokeWidth=1.2, opacity=90)

# branch collar: the knop all four arms grow out of
collar = [(476, 462), (480, 452), (490, 444), (500, 441), (510, 444),
          (520, 452), (524, 462)]
for p in collar + [(2 * AX - x, y) for x, y in collar[::-1][1:-1]]:
    EXTENT.append(p)
d.path(smooth(collar + [(2 * AX - x, y) for x, y in collar[::-1][1:-1]]),
       "Branch collar", fill=silver(438, 464), stroke=INK, strokeWidth=2.0, join="round")
d.shape("ellipse", "Collar ring", x=484, y=449, width=32, height=7, fill=NONE,
        stroke="#14181C", strokeWidth=1.5, opacity=55)

# --- arms: mirrored scrolls out of the shoulder -------------------------------------------
# spine from stem shoulder -> dip -> up to cup base; per-side bezier control pts
ARMS = [("Outer L", (497, 448), (370, 470), (300, 430), (296, 402)),
        ("Outer R", (503, 448), (632, 472), (700, 428), (704, 400)),
        ("Inner L", (498, 452), (430, 468), (388, 436), (392, 404)),
        ("Inner R", (502, 452), (572, 470), (612, 434), (608, 402))]
# paint far pair first (inner arms attach slightly behind)
for nm, p0, p1, p2, p3 in ARMS:
    spine = cubic(p0, p1, p2, p3)
    ribbon(nm + " arm", spine, 7.5, 5.5, silver_x(p0[0], p3[0]), ink=2.0, bulge=0.25)
    # root scroll: a little C-curl tucked under the shoulder joint
    sx, sy = p0[0] + (4 if p3[0] > AX else -4), p0[1] + 4
    d.path(f"M{sx},{sy} q{(p3[0] - AX) * 0.10:.0f},10 {(p3[0] - AX) * 0.05:.0f},16 "
           f"q{(AX - p3[0]) * 0.03:.0f},4 -4,-2", f"{nm} root scroll",
           fill=NONE, stroke="#96A2AA", strokeWidth=2.6, opacity=70, cap="round")

# --- cups, candles, flames ---------------------------------------------------------------
def cup(cx, base_y, r):
    """Bobeche + socket: flared drip pan under a short candle socket."""
    prof = [(cx + r, base_y), (cx + r - 2, base_y - 6), (cx + r * 0.45, base_y - 10),
            (cx + r * 0.38, base_y - 14), (cx + r * 0.34, base_y - 26)]
    lp = [(x, y) for x, y in prof]
    left = [(2 * cx - x, y) for x, y in reversed(lp)]
    for p in lp + left:
        EXTENT.append(p)
    d.path(smooth(lp + left), f"Cup {cx}", fill=silver(base_y - 26, base_y),
           stroke=INK, strokeWidth=1.8, join="round")
    d.shape("ellipse", f"Cup rim {cx}", x=round(cx - r), y=round(base_y - 4),
            width=round(2 * r), height=round(r * 0.4), fill=NONE,
            stroke="#DDE5EA", strokeWidth=1.8, opacity=45)
    # socket top ellipse (dark hole the candle sits in)
    d.shape("ellipse", f"Socket {cx}", x=round(cx - r * 0.34), y=round(base_y - 28),
            width=round(r * 0.68), height=round(r * 0.22),
            fill="#14181C", opacity=80, stroke=NONE)


def candle(cx, top_y, base_y, w, drip_seed):
    """Ivory taper with a lumpy melted top and drips down the front."""
    n = 24
    right = [(cx + w * (0.92 + 0.08 * t) + 0.7 * math.sin(t * 9 + drip_seed),
              base_y - 2 - (base_y - 2 - top_y) * t) for t in [i / n for i in range(n + 1)]]
    top = [(cx + w - 2 * w * i / n,
            top_y - 1.8 * math.sin(i / n * math.pi * 3 + drip_seed)) for i in range(1, n)]
    left = [(cx - w * (0.92 + 0.08 * t) - 0.7 * math.sin(t * 9 + drip_seed),
             base_y - 2 - (base_y - 2 - top_y) * t) for t in [1 - i / n for i in range(1, n + 1)]]
    outline = right + top + left
    for p in outline:
        EXTENT.append(p)
    d.path(smooth(outline), f"Candle {cx}",
           fill=lin((0, top_y), (0, base_y), (0, WAX_L), (0.5, "#E2D4B6"),
                    (1, WAX_D)), stroke="#8A7A60", strokeWidth=1.6, join="round")
    # melted pool on top
    d.shape("ellipse", f"Wax pool {cx}", x=round(cx - w * 0.7), y=round(top_y - 3),
            width=round(w * 1.4), height=7, fill="#FBF4E0", opacity=85,
            stroke="#BBA98A", strokeWidth=1.2)
    # drips: rivulets down the front face
    for j, (dx, ln) in enumerate([(-0.45, 30), (0.35, 42)]):
        x = cx + dx * w
        dd = [(x - 1.6, top_y + 2), (x + 1.8, top_y + 3),
              (x + 1.4, top_y + ln), (x, top_y + ln + 4), (x - 1.2, top_y + ln)]
        d.path(smooth(dd), f"Drip {cx} {j+1}", fill="#EFE4CC", opacity=80,
               stroke="#B8A886", strokeWidth=1.0)
    # wick
    d.path(f"M{cx - 1.2},{top_y - 1} L{cx - 1.0},{top_y - 9} L{cx + 1.4},{top_y - 9} "
           f"L{cx + 1.2},{top_y - 1} Z", f"Wick {cx}", fill="#241812",
           stroke=NONE)


def flame(scale, cx, cy, lean=0.0):
    p = [(cx + lean * 56 * scale, cy - 56 * scale),
         (cx + 11 * scale + lean * 28 * scale, cy - 30 * scale),
         (cx + 14 * scale, cy - 12 * scale), (cx + 8 * scale, cy),
         (cx, cy + 4 * scale), (cx - 8 * scale, cy),
         (cx - 14 * scale, cy - 12 * scale), (cx - 11 * scale + lean * 20 * scale, cy - 30 * scale)]
    for q in p:
        EXTENT.append(q)
    return smooth(p)


# candle geometry: (cx, cup_y, candle_top, cup_r) — centre tallest, outers lowest
CANDS = [(296, 402, 322, 26), (392, 404, 302, 24), (500, 396, 240, 26),
         (608, 402, 306, 24), (704, 400, 326, 26)]
for cx, cy, top, r in CANDS:
    cup(cx, cy, r)
    candle(cx, top, cy - 22, r * 0.42, cx * 0.13)

# wax pooled on the two lowest cups
for cx, cy, w in ((296, 398, 30), (704, 396, 30)):
    d.shape("ellipse", f"Pool on cup {cx}", x=cx - w // 2, y=cy - 8, width=w, height=9,
            fill="#EFE4CC", opacity=70, stroke="#B8A886", strokeWidth=1.2)
# one runaway drip off the outer-left cup lip
d.path("M282,398 q-3,10 -1,20 q2,6 5,2 q2,-8 -1,-22 Z", "Cup drip L",
       fill="#EFE4CC", opacity=80, stroke="#B8A886", strokeWidth=1.0)

# flames last so they sit on top of wax
FLAME_Y = {296: 316, 392: 296, 500: 234, 608: 300, 704: 320}
for cx, fy in FLAME_Y.items():
    sc = 0.62 if cx != 500 else 0.72
    d.path(flame(sc, cx + 1, fy, lean=0.06), f"Flame outer {cx}", fill="#E8862A",
           opacity=70, stroke=NONE)
for cx, fy in FLAME_Y.items():
    sc = 0.62 if cx != 500 else 0.72
    d.path(flame(sc * 0.6, cx + 1, fy + 3, lean=0.06), f"Flame mid {cx}",
           fill="#F5B84A", opacity=85, stroke=NONE)
    d.shape("ellipse", f"Flame core {cx}", x=round(cx - 4), y=round(fy - 24 * sc),
            width=9, height=round(22 * sc), fill=rad((0, "#FDF6DC", 95), (1, "#FBD88A", 0)),
            stroke=NONE)
    d.shape("ellipse", f"Flame blue {cx}", x=round(cx - 6), y=round(fy - 2),
            width=12, height=6, fill="#5A7AC8", opacity=40, stroke=NONE)
# soft halo ring over each flame + one big shared glow
for cx, fy in FLAME_Y.items():
    d.shape("ellipse", f"Halo {cx}", x=round(cx - 26), y=round(fy - 42), width=52,
            height=56, fill=rad((0, "#FBD88A", 22), (1, "#FBD88A", 0)), stroke=NONE)
d.shape("ellipse", "Flame bloom", x=330, y=180, width=340, height=220,
        fill=rad((0, "#FBD88A", 18), (0.6, "#E89A3C", 6), (1, "#E89A3C", 0)),
        stroke=NONE)

# --- extent check ---------------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("candelabra extent: farthest point %.0f from centre (rim %d)" % (far, PR))
assert far < PR - 26, far


# --- caption ----------------------------------------------------------------------------------
def find(node, oid):
    if isinstance(node, dict):
        if node.get("id") == oid and "bounds" in node:
            return node["bounds"]
        for v in node.values():
            r = find(v, oid)
            if r:
                return r
    elif isinstance(node, list):
        for v in node:
            r = find(v, oid)
            if r:
                return r
    return None


def caption(name, mats):
    n = d.text(name, "Name", x=500, y=934, size=56, font="Virelai Sans",
               color="#EAEEF2", justify="center")
    m = d.text(mats, "Materials", x=500, y=970, size=22, font="Virelai Sans",
               color="#A8B4BE", justify="center")
    d.cmd("text.setStyle", "Name tracking", ids=[n["id"]], tracking=60)
    d.cmd("text.setStyle", "Materials tracking", ids=[m["id"]], tracking=260)
    doc = d.m.call("doc_inspect", {})
    for oid, label in ((n["id"], "name"), (m["id"], "materials")):
        b = find(doc, oid)
        nearest = (min(max(PCX, b["x"]), b["x"] + b["width"]),
                   min(max(PCY, b["y"]), b["y"] + b["height"]))
        clear = math.hypot(nearest[0] - PCX, nearest[1] - PCY) - (PR + 3)
        print("%s: %.0fx%.0f at y %.0f, clears rim by %.1f" %
              (label, b["width"], b["height"], b["y"], clear))
        assert clear > 0 and b["x"] >= 10 and b["x"] + b["width"] <= 990, label
        if label == "materials":
            assert b["width"] <= 760, b["width"]


caption("CANDELABRA", "STERLING · BEESWAX · COTTON WICK")
d.finish("candelabra-V1R00")
