#!/usr/bin/env python3
"""Settle bench — furniture field plate V1R00. Near-side view with a slight
three-quarter from the front right: a high-backed oak settle — a paneled wall
of a back leaning a few degrees off vertical, solid plank seat over a box
base, winged ends curving down to arm height. Warm tavern-corner light, low
from the right. 1000x1000. Modelled in 3D (inches), projected with a fixed
yaw + pitch.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Settle Bench — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#221105"   # warm dark umber, not black
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


def smooth(pts, closed=False, move=True):
    """Catmull-Rom through pts as cubic Beziers."""
    n = len(pts)

    def g(i):
        return pts[i % n] if closed else pts[max(0, min(n - 1, i))]
    s = ("M%.1f,%.1f" if move else "L%.1f,%.1f") % pts[0]
    for i in (range(n) if closed else range(n - 1)):
        p0, p1, p2, p3 = g(i - 1), g(i), g(i + 1), g(i + 2)
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        s += " C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (c1 + c2 + p2)
    return s + (" Z" if closed else "")


# --- projection -------------------------------------------------------------
YAW, PITCH = math.radians(24), math.radians(14)
S, OX, OY = 12.4, 506.0, 744.0


def P(x, y, z):
    c, s = math.cos(YAW), math.sin(YAW)
    xr, zr = x * c + z * s, -x * s + z * c
    p = (OX + S * xr, OY - S * (y * math.cos(PITCH) + zr * math.sin(PITCH)))
    EXTENT.append(p)
    return p


def quad(name, pts3, fill, ink=3, join="miter"):
    """A crisp planar face: 3D corners projected, drawn as a straight polygon —
    joinery reads by its edges, not by softening."""
    c2 = [P(*p) for p in pts3]
    path = "M%.1f,%.1f" % c2[0] + "".join(" L%.1f,%.1f" % p for p in c2[1:]) + " Z"
    d.path(path, name, fill=fill, stroke=INK, strokeWidth=ink, join=join)


# --- palette -------------------------------------------------------------------
OAK = lin((0, 180), (0, 780), (0, "#A9763E"), (0.5, "#7A5024"), (1, "#442608"))
OAK_DK = lin((0, 180), (0, 780), (0, "#6E4820"), (1, "#2A1606"))
OAK_HI = "#E8BC78"
OAK_PANEL = lin((0, 300), (0, 640), (0, "#8A5C2C"), (0.55, "#6A441E"), (1, "#3C2008"))
OAK_SIDE = lin((0, 180), (0, 780), (0, "#5E3C1C"), (1, "#241204"))

# --- backdrop + plate -----------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#160F08"), (1, "#060403")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#64482C", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#4A3620"), (0.6, "#302112"), (1, "#170E06")),
        stroke="#0D0703", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E2B878", strokeWidth=3, opacity=26)
# hearth glow low on the right — the tavern corner's fire
d.shape("ellipse", "Hearth glow", x=520, y=430, width=520, height=420,
        fill=rad((0, "#F09A48", 34), (0.5, "#B8581E", 12), (1, "#7A3010", 0)), stroke=NONE)
d.shape("ellipse", "Lamp fill", x=120, y=110, width=480, height=460,
        fill=rad((0, "#E8B878", 14), (1, "#E8B878", 0)), stroke=NONE)

# floor: a band that closes on the disc's own arc
FY = 712
hx = math.sqrt(PR ** 2 - (FY - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{FY} L{PCX + hx:.1f},{FY} A420,420 0 0 1 {PCX - hx:.1f},{FY} Z",
       "Floor", fill=lin((0, FY), (0, 880), (0, "#503C26", 34), (1, "#140C05", 74)), stroke=NONE)
for i, y in enumerate([748, 792, 842]):
    hw = math.sqrt(PR ** 2 - (y - PCY) ** 2) - 10
    d.path(f"M{PCX - hw:.1f},{y} L{PCX + hw:.1f},{y}", f"Floorboard seam {i+1}",
           fill=NONE, stroke="#221304", strokeWidth=2, opacity=45)
d.path(f"M{PCX - hx + 6:.1f},{FY} L{PCX + hx - 6:.1f},{FY}", "Floor edge light",
       fill=NONE, stroke="#E0BE8A", strokeWidth=2, opacity=20)

# --- geometry (inches) --------------------------------------------------------------
# the settle: wide high-backed box bench
W = 19.5            # half width of the back wall / seat
BACK_Z = 5.6        # back wall front face
BACK_Y0, BACK_Y1 = 16.0, 44.0
BACK_RAKE = 0.06    # lean back per inch of height
WING_X = 20.5       # wing outer face
WING_T = 1.8
SEAT_Y0, SEAT_Y1 = 16.0, 18.6
SEAT_ZF = -10.0
BASE_Y0, BASE_Y1 = 1.6, 16.0
BASE_ZF = -8.8

# soft shadow under the bench
d.shape("ellipse", "Bench shadow", x=210, y=740, width=590, height=92,
        fill=rad((0, "#050301", 70), (0.6, "#050301", 34), (1, "#050301", 0)), stroke=NONE)


def bk_z(y):
    return BACK_Z + (y - 16) * BACK_RAKE


# --- far wing (left): inner face peeking over the seat --------------------------------
quad("Wing far inner",
     [(-WING_X + WING_T, BASE_Y1, SEAT_ZF + 1.5), (-WING_X + WING_T, BASE_Y1, BACK_Z + 0.5),
      (-WING_X + WING_T, 36.5, BACK_Z + 0.8), (-WING_X + WING_T, 33.5, SEAT_ZF + 1.8)],
     OAK_DK, ink=3)

# --- back wall ---------------------------------------------------------------------------
# rake: the wall leans back as it rises
wall = [(-W, BACK_Y0, bk_z(BACK_Y0)), (W, BACK_Y0, bk_z(BACK_Y0)),
        (W, BACK_Y1, bk_z(BACK_Y1)), (-W, BACK_Y1, bk_z(BACK_Y1))]
quad("Back wall", wall, OAK, ink=4)
# top rail: a slightly wider cap band
quad("Back top rail", [(-W - 0.5, 39.8, bk_z(39.8)), (W + 0.5, 39.8, bk_z(39.8)),
                       (W + 0.5, BACK_Y1 + 0.6, bk_z(BACK_Y1) + 0.5),
                       (-W - 0.5, BACK_Y1 + 0.6, bk_z(BACK_Y1) + 0.5)],
     lin((0, 170), (0, 260), (0, "#B9854A"), (1, "#5A3614")), ink=3.5)
# top rail top face (the cap's edge catches light)
quad("Top rail face", [(-W - 0.5, BACK_Y1 + 0.6, bk_z(BACK_Y1) + 0.5),
                       (W + 0.5, BACK_Y1 + 0.6, bk_z(BACK_Y1) + 0.5),
                       (W + 0.5, BACK_Y1 + 0.2, bk_z(BACK_Y1) + 1.6),
                       (-W - 0.5, BACK_Y1 + 0.2, bk_z(BACK_Y1) + 1.6)],
     OAK_HI, ink=2.5)
# three fielded panels between stiles
for i, (x0, x1) in enumerate([(-W + 2.2, -7.0), (-7.0, 7.0), (7.0, W - 2.2)]):
    py0, py1 = 20.5, 36.5
    pz0, pz1 = bk_z(py0) - 0.22, bk_z(py1) - 0.22
    quad(f"Panel {i+1}", [(x0, py0, pz0), (x1, py0, pz0), (x1, py1, pz1), (x0, py1, pz1)],
         OAK_PANEL, ink=3)
    # inner bevel light top-left, shade bottom-right
    bev = [P(x0 + 0.9, py0 + 1.2, pz0 - 0.12), P(x1 - 0.9, py0 + 1.2, pz0 - 0.12)]
    d.path("M%.1f,%.1f L%.1f,%.1f" % (bev[0] + bev[1]), f"Panel {i+1} bevel top",
           fill=NONE, stroke=OAK_HI, strokeWidth=2.2, opacity=45, cap="round")
    bev = [P(x0 + 0.9, py1 - 1.2, pz1 - 0.12), P(x1 - 0.9, py1 - 1.2, pz1 - 0.12)]
    d.path("M%.1f,%.1f L%.1f,%.1f" % (bev[0] + bev[1]), f"Panel {i+1} bevel low",
           fill=NONE, stroke="#1E0E04", strokeWidth=2.2, opacity=50, cap="round")
# stile lines between panels
for x in (-8.5, 8.5):
    a = P(x, BACK_Y0 + 1.5, bk_z(BACK_Y0 + 1.5) - 0.1)
    b = P(x, 39.6, bk_z(39.6) - 0.1)
    d.path("M%.1f,%.1f L%.1f,%.1f" % (a + b), f"Stile {x}", fill=NONE,
           stroke="#2E1808", strokeWidth=3, opacity=55)
# hearth-side rim light up the wall's right edge
er = [P(W - 0.3, y, bk_z(y) - 0.05) for y in (20, 28, 36, 43.5)]
d.path(smooth(er), "Wall rim light", fill=NONE, stroke="#F0A04E", strokeWidth=3,
       opacity=40, cap="round")

# --- near wing (right): outer face, front edge, inner face -------------------------------
# outer first
quad("Wing near outer",
     [(WING_X, 0.8, SEAT_ZF - 0.4), (WING_X, 0.8, BACK_Z + 1.2),
      (WING_X, 38.5, BACK_Z + 1.4), (WING_X, 34.0, SEAT_ZF - 0.2)],
     OAK_SIDE, ink=3.5)
# inner face
quad("Wing near inner",
     [(WING_X - WING_T, BASE_Y1 - 1.2, SEAT_ZF + 0.4), (WING_X - WING_T, BASE_Y1 - 1.2, BACK_Z + 0.4),
      (WING_X - WING_T, 37.6, BACK_Z + 0.8), (WING_X - WING_T, 33.2, SEAT_ZF + 0.6)],
     lin((560, 260), (860, 640), (0, "#8A5C2C"), (0.55, "#6A441E"), (1, "#381E08")),
     ink=3.5)
# wing cap: the top edge face
quad("Wing near cap",
     [(WING_X, 38.5, BACK_Z + 1.4), (WING_X, 34.0, SEAT_ZF - 0.2),
      (WING_X - WING_T, 33.2, SEAT_ZF + 0.6), (WING_X - WING_T, 37.6, BACK_Z + 0.8)],
     lin((800, 300), (1060, 420), (0, "#C08C50"), (1, "#6E441E")), ink=3)
# wing front edge face
quad("Wing near front",
     [(WING_X, 0.8, SEAT_ZF - 0.4), (WING_X, 34.0, SEAT_ZF - 0.2),
      (WING_X - WING_T, 33.2, SEAT_ZF + 0.6), (WING_X - WING_T, 0.8, SEAT_ZF - 0.2)],
     lin((0, 300), (0, 780), (0, "#9A6A34"), (0.55, "#6E441E"), (1, "#301806")),
     ink=3.5)
# hearth light up the wing's front edge
we = [P(WING_X - 0.15, y, SEAT_ZF - 0.28) for y in (4, 14, 24, 33)]
d.path(smooth(we), "Wing edge light", fill=NONE, stroke="#F0A04E", strokeWidth=3,
       opacity=45, cap="round")

# --- seat plank ----------------------------------------------------------------------------
quad("Seat top", [(-WING_X + WING_T + 0.3, SEAT_Y1, SEAT_ZF), (WING_X - WING_T + 0.2, SEAT_Y1, SEAT_ZF),
                  (WING_X - WING_T + 0.2, SEAT_Y1, BACK_Z), (-WING_X + WING_T + 0.3, SEAT_Y1, BACK_Z)],
     lin((0, 560), (0, 660), (0, "#B98A52"), (0.5, "#8A5C2C"), (1, "#4E2E10")), ink=3.5)
# front edge face
quad("Seat front", [(-WING_X + WING_T + 0.3, SEAT_Y1, SEAT_ZF), (WING_X - WING_T + 0.2, SEAT_Y1, SEAT_ZF),
                    (WING_X - WING_T + 0.2, SEAT_Y0, SEAT_ZF - 0.15), (-WING_X + WING_T + 0.3, SEAT_Y0, SEAT_ZF - 0.15)],
     lin((0, 620), (0, 700), (0, "#8A5C2C"), (1, "#38200A")), ink=3)
# seat top edge light
se = [P(x, SEAT_Y1 + 0.1, SEAT_ZF + 0.15) for x in (-17, -7, 3, 13, 18.2)]
d.path(smooth(se), "Seat edge light", fill=NONE, stroke=OAK_HI, strokeWidth=2.6,
       opacity=50, cap="round")
# board seams in the plank top
for zz in (-6.0, -1.5, 3.0):
    bs = [P(-17.6, SEAT_Y1 + 0.02, zz), P(18.4, SEAT_Y1 + 0.02, zz)]
    d.path("M%.1f,%.1f L%.1f,%.1f" % (bs[0] + bs[1]), f"Seat seam {zz}", fill=NONE,
           stroke="#3C220C", strokeWidth=1.8, opacity=45)

# --- box base ------------------------------------------------------------------------------
# front face with two fielded panels
quad("Base front", [(-WING_X + WING_T + 0.2, BASE_Y1, BASE_ZF), (WING_X - WING_T + 0.2, BASE_Y1, BASE_ZF),
                    (WING_X - WING_T + 0.2, BASE_Y0, BASE_ZF), (-WING_X + WING_T + 0.2, BASE_Y0, BASE_ZF)],
     OAK, ink=3.5)
for i, (x0, x1) in enumerate([(-16.4, -1.6), (-1.6, 16.2)]):
    quad(f"Base panel {i+1}", [(x0, 4.6, BASE_ZF - 0.2), (x1, 4.6, BASE_ZF - 0.2),
                               (x1, 13.2, BASE_ZF - 0.2), (x0, 13.2, BASE_ZF - 0.2)],
         OAK_PANEL, ink=2.8)
# base side (right)
quad("Base side", [(WING_X - WING_T + 0.2, BASE_Y1, BASE_ZF), (WING_X - 0.4, BASE_Y1, BACK_Z),
                   (WING_X - 0.4, BASE_Y0, BACK_Z), (WING_X - WING_T + 0.2, BASE_Y0, BASE_ZF)],
     OAK_SIDE, ink=3)
# plinth foot: a slightly darker toe band
quad("Plinth", [(-WING_X + WING_T - 0.2, BASE_Y0 + 2.2, BASE_ZF - 0.1), (WING_X - WING_T + 0.4, BASE_Y0 + 2.2, BASE_ZF - 0.1),
                (WING_X - WING_T + 0.4, 0.6, BASE_ZF - 0.4), (-WING_X + WING_T - 0.2, 0.6, BASE_ZF - 0.4)],
     lin((0, 720), (0, 790), (0, "#4E3016"), (1, "#201004")), ink=3)

# --- extent check ----------------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("bench extent: farthest point %.0f from centre (rim %d)" % (far, PR))
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
    n = d.text(name, "Name", x=500, y=940, size=56, font="Virelai Sans",
               color="#F2DCB4", justify="center")
    m = d.text(mats, "Materials", x=500, y=972, size=22, font="Virelai Sans",
               color="#C29A6C", justify="center")
    d.cmd("text.setStyle", "Name tracking", ids=[n["id"]], tracking=60)
    d.cmd("text.setStyle", "Materials tracking", ids=[m["id"]], tracking=260)
    doc = d.m.call("doc_inspect", {})
    for oid, label in ((n["id"], "name"), (m["id"], "materials")):
        b = find(doc, oid)
        nearest = (min(max(PCX, b["x"]), b["x"] + b["width"]),
                   min(max(PCY, b["y"]), b["y"] + b["height"]))
        clear = math.hypot(nearest[0] - PCX, nearest[1] - PCY) - (PR + 3)
        print("%s: %.0fx%.0f at y %.0f, clears rim by %.1f" % (label, b["width"], b["height"], b["y"], clear))
        assert clear > 0 and b["x"] >= 10 and b["x"] + b["width"] <= 990, label
        if label == "materials":
            assert b["width"] <= 760, b["width"]


caption("SETTLE BENCH", "OAK")
d.finish("settle-bench-V1R00")
