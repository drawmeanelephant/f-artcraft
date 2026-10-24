#!/usr/bin/env python3
"""Bunk bed — field plate V1R00. Three-quarter view down the bed's length:
a pine bunkhouse bunk, two mattresses stacked like a promise, camp blankets
folded at each foot, a ladder hanging on the near side. Olive dusk plate,
summer-camp mood. 1000x1000.
Modelled in inches (x right, y up, +z back) and projected with a fixed
yaw + pitch; everything is 8-corner prisms, drawn far to near.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Bunk Bed — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#221408"   # warm dark, not black
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


def smooth(pts, closed=True, k=1.0):
    n = len(pts)
    s = "M%.1f,%.1f" % pts[0]
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        p0 = pts[(i - 1) % n] if (closed or i > 0) else pts[0]
        p1, p2 = pts[i], pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (closed or i + 2 < n) else pts[-1]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6 * k, p1[1] + (p2[1] - p0[1]) / 6 * k)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6 * k, p2[1] - (p3[1] - p1[1]) / 6 * k)
        s += " C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (c1 + c2 + p2)
    return s + (" Z" if closed else "")


# --- projection ------------------------------------------------------------------
YAW, PITCH = math.radians(28), math.radians(20)
S, OX, OY = 8.5, 518.0, 680.0
CY, SY = math.cos(YAW), math.sin(YAW)
CP, SP = math.cos(PITCH), math.sin(PITCH)


def P(x, y, z):
    xr, zr = x * CY + z * SY, -x * SY + z * CY
    p = (OX + S * xr, OY - S * (y * CP + zr * SP))
    EXTENT.append(p)
    return p


def depth(x, y, z):
    return -x * SY * CP - y * SP + z * CY * CP


def box(x0, y0, z0, x1, y1, z1):
    return [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
            (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]


FACES = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4),
         (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
TO_VIEWER = (SY * CP, SP, -CY * CP)
LIGHT = (-0.45, 0.80, -0.42)
_l = math.sqrt(sum(c * c for c in LIGHT))
LIGHT = tuple(c / _l for c in LIGHT)


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def normal(c, f):
    u = sub(c[f[1]], c[f[0]])
    v = sub(c[f[3]], c[f[0]])
    n = (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2],
         u[0] * v[1] - u[1] * v[0])
    l = math.sqrt(sum(k * k for k in n))
    return tuple(k / l for k in n)


def shade(hex1, hex2, b):
    a = [int(hex1[i:i + 2], 16) for i in (1, 3, 5)]
    c = [int(hex2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02X%02X%02X" % tuple(round(a[i] + (c[i] - a[i]) * b) for i in range(3))


PIN_D, PIN_L = "#5E3C1C", "#C89858"      # honey pine ramp
PIN_HI = "#E8C088"


def prism(name, corners, dark=PIN_D, light=PIN_L, lo=0.06, hi=0.94, ink=1.8):
    faces = []
    for f in FACES:
        n = normal(corners, f)
        if n[0] * TO_VIEWER[0] + n[1] * TO_VIEWER[1] + n[2] * TO_VIEWER[2] <= 0.02:
            continue
        lam = max(0.0, sum(n[i] * LIGHT[i] for i in range(3)))
        dep = sum(depth(*corners[i]) for i in f) / len(f)
        pts = [P(*corners[i]) for i in f]
        faces.append((dep, pts, lam))
    for dep, pts, lam in sorted(faces, key=lambda t: -t[0]):
        b = lo + (hi - lo) * lam ** 0.8
        y0, y1 = min(p[1] for p in pts), max(p[1] for p in pts)
        g = lin((0, y0), (0, y1), (0, shade(dark, light, min(1, b + 0.12))),
                                 (1, shade(dark, light, b)))
        d.path(poly(pts), name, fill=g, stroke=INK, strokeWidth=ink, join="round")
    return faces


# --- backdrop + plate ---------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#18160E"), (1, "#080604")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#9C8E58", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#5A5238"), (0.6, "#38321F"), (1, "#181207")),
        stroke="#100B05", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8D8A0", strokeWidth=3, opacity=20)
# low summer sun, behind the foot posts
d.shape("ellipse", "Sunset glow", x=380, y=110, width=560, height=520,
        fill=rad((0, "#F0B460", 20), (0.55, "#A8783C", 8), (1, "#5E4020", 0)),
        stroke=NONE)

FY = 622
hx = math.sqrt(PR ** 2 - (FY - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{FY} L{PCX + hx:.1f},{FY} A420,420 0 0 1 {PCX - hx:.1f},{FY} Z",
       "Floor", fill=lin((0, FY), (0, 880), (0, "#4A4230", 45), (1, "#14100A", 80)),
       stroke=NONE)
d.path(f"M{PCX - hx + 6:.1f},{FY} L{PCX + hx - 6:.1f},{FY}", "Floor edge light",
       fill=NONE, stroke="#E8D0A0", strokeWidth=2, opacity=18)

# grounding shadow under the bunks
sh = [P(x, 0, z) for x in (-24.6, 24.6) for z in (-9.8, 9.8)]
sx0, sx1 = min(p[0] for p in sh) - 50, max(p[0] for p in sh) + 50
sy0, sy1 = min(p[1] for p in sh) - 20, max(p[1] for p in sh) + 28
d.shape("ellipse", "Bed shadow", x=round(sx0), y=round(sy0),
        width=round(sx1 - sx0), height=round(sy1 - sy0),
        fill=rad((0, "#050302", 70), (0.6, "#050302", 30), (1, "#050302", 0)),
        stroke=NONE)

# --- bunk geometry (inches; length along x, head at -x) -------------------------------
PX, PZ = 23.5, 8.7                    # post centres
PW = 1.1                              # post half-width
TOP_Y = 57.0                          # post tops
LOW, UP = 14.5, 39.5                  # mattress base heights
MAT_T = 4.5                           # mattress thickness


def post(name, cx, cz, dim=False):
    dk, lt = ("#3E2810", "#8A6034") if dim else (PIN_D, PIN_L)
    prism(name, box(cx - PW, 0, cz - PW, cx + PW, TOP_Y, cz + PW),
          dark=dk, light=lt, lo=0.05, hi=0.95, ink=1.7)
    # ball cap
    bx, by = P(cx, TOP_Y + 0.9, cz)
    d.shape("ellipse", f"{name} cap", x=round(bx - 9), y=round(by - 8), width=18, height=16,
            fill=rad((0, shade(lt, "#FFFFFF", 0.15)), (0.65, lt), (1, dk)),
            stroke=INK, strokeWidth=1.5)


def end_frame(ex, dim):
    """End frame in the y-z plane at x=ex: rails at both levels + top, slats."""
    dk, lt = ("#3E2810", "#8A6034") if dim else (PIN_D, PIN_L)
    for i, (ry0, ry1) in enumerate([(10.0, 14.0), (35.0, 39.0), (52.5, 56.5)]):
        prism(f"End rail {ex:+g} {i}", box(ex - 1.1, ry0, -PZ - 0.9, ex + 1.1, ry1, PZ + 0.9),
              dark=dk, light=lt, lo=0.08, hi=0.9, ink=1.6)
    for i, sz in enumerate((-5.8, 0.0, 5.8)):
        prism(f"End slat {ex:+g} {i}", box(ex - 0.6, 14.0, sz - 0.6, ex + 0.6, 35.0, sz + 0.6),
              dark=dk, light=lt, lo=0.08, hi=0.9, ink=1.4)


# far side first: back posts, then the two end frames, then far side rails
post("Post head far", -PX, PZ, dim=True)
post("Post foot far", PX, PZ, dim=True)
end_frame(-PX, dim=True)
end_frame(PX, dim=True)
for i, (ry0, ry1) in enumerate([(LOW - 3.5, LOW), (UP - 3.5, UP)]):
    prism(f"Far side rail {i}", box(-PX, ry0, PZ - 1.2, PX, ry1, PZ + 0.6),
          dark="#3E2810", light="#8A6034", lo=0.06, hi=0.85, ink=1.5)

# mattresses + camp bedding, lower then upper
BLANK = [("#3E4632", "#8A9068"), ("#4E3028", "#A86A50")]   # olive, rust


def bunk(i, y0):
    prism(f"Mattress {i}", box(-22.4, y0, -8.2, 22.4, y0 + MAT_T, 8.2),
          dark="#8A8494", light="#F0EBDD", lo=0.32, hi=1.02, ink=1.6)
    pa, pb = P(-22.0, y0 + MAT_T - 0.1, -8.1), P(22.0, y0 + MAT_T - 0.1, -8.1)
    d.path(f"M{pa[0]:.1f},{pa[1]:.1f} L{pb[0]:.1f},{pb[1]:.1f}", f"Mattress {i} piping",
           fill=NONE, stroke="#A89CA8", strokeWidth=1.6, opacity=55, cap="round")
    # camp blanket folded across the foot half
    bd, bl = BLANK[i]
    prism(f"Blanket {i}", box(4.0, y0 + MAT_T, -8.4, 22.6, y0 + MAT_T + 1.4, 8.4),
          dark=bd, light=bl, lo=0.15, hi=0.95, ink=1.6)
    a, b = P(4.2, y0 + MAT_T + 0.7, -8.5), P(4.2, y0 + MAT_T + 0.7, 8.5)
    d.path(f"M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}", f"Blanket {i} fold",
           fill=NONE, stroke="#241A10", strokeWidth=2.0, opacity=45, cap="round")
    # pillow at the head
    c = P(-19.0, y0 + MAT_T + 1.8, -1.5)
    pts = [(c[0] - 34, c[1] + 20), (c[0] - 40, c[1] + 6), (c[0] - 14, c[1] - 20),
           (c[0] + 24, c[1] - 32), (c[0] + 42, c[1] - 20), (c[0] + 18, c[1] + 8),
           (c[0] - 10, c[1] + 24)]
    d.path(smooth(pts), f"Pillow {i}", stroke="#5E5470", strokeWidth=2.2,
           fill=rad((0, "#F6F0E4"), (0.7, "#E0DCE8"), (1, "#B4AEC2")))
    d.path(smooth([(c[0] - 24, c[1] + 6), (c[0] - 2, c[1] - 12), (c[0] + 24, c[1] - 22)],
                  closed=False), f"Pillow {i} crease",
           fill=NONE, stroke="#8C84A4", strokeWidth=2.0, opacity=40, cap="round")


bunk(0, LOW)
bunk(1, UP)

# near side rails at both levels, then the top-bunk guard rail and its slats
for i, (ry0, ry1) in enumerate([(LOW - 3.5, LOW), (UP - 3.5, UP)]):
    prism(f"Near side rail {i}", box(-PX - 0.4, ry0, -PZ - 1.4, PX + 0.4, ry1, -PZ + 0.2),
          lo=0.08, hi=0.95, ink=1.9)
    ra, rb = P(-PX, ry1 - 0.35, -PZ - 1.5), P(PX, ry1 - 0.35, -PZ - 1.5)
    d.path(f"M{ra[0]:.1f},{ra[1]:.1f} L{rb[0]:.1f},{rb[1]:.1f}", f"Rail {i} bead light",
           fill=NONE, stroke=PIN_HI, strokeWidth=1.8, opacity=40, cap="round")
prism("Guard rail", box(-PX - 0.4, 47.5, -PZ - 1.4, PX + 0.4, 50.5, -PZ + 0.2),
      lo=0.08, hi=0.95, ink=1.9)
for i, sx in enumerate((-15.0, -1.0, 13.0)):
    prism(f"Guard slat {i}", box(sx - 0.7, UP, -PZ - 1.2, sx + 0.7, 47.5, -PZ - 0.2),
          lo=0.08, hi=0.9, ink=1.5)
ga, gb = P(-PX, 50.2, -PZ - 1.5), P(PX, 50.2, -PZ - 1.5)
d.path(f"M{ga[0]:.1f},{ga[1]:.1f} L{gb[0]:.1f},{gb[1]:.1f}", "Guard bead light",
       fill=NONE, stroke=PIN_HI, strokeWidth=1.8, opacity=45, cap="round")

# ladder hooked on the near side at the foot end
LZ_ = -PZ - 2.0
for i, lx in enumerate((19.0, 24.6)):
    prism(f"Ladder stile {i}", box(lx - 0.7, 0.0, LZ_ - 0.6, lx + 0.7, 52.0, LZ_ + 0.6),
          lo=0.08, hi=0.95, ink=1.6)
for i, ly in enumerate((8.0, 15.5, 23.0, 30.5, 38.0, 45.5)):
    prism(f"Rung {i}", box(19.0, ly - 0.55, LZ_ - 0.5, 24.6, ly + 0.55, LZ_ + 0.5),
          dark="#4E3014", light="#B08048", lo=0.10, hi=0.95, ink=1.4)

# near posts last, over the rail ends
post("Post head near", -PX, -PZ)
post("Post foot near", PX, -PZ)

# sunset sheen on the upper near rail and foot post cap
sa, sb = P(-8, UP - 0.6, -PZ - 1.5), P(20, UP - 0.6, -PZ - 1.5)
d.path(f"M{sa[0]:.1f},{sa[1]:.1f} L{sb[0]:.1f},{sb[1]:.1f}", "Sunset rim light",
       fill=NONE, stroke="#F0C888", strokeWidth=2.5, opacity=35, cap="round")

# --- extent check ---------------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("bunk extent: farthest point %.0f from centre (rim %d)" % (far, PR))
assert far < PR - 22, far


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
               color="#F2E8CC", justify="center")
    m = d.text(mats, "Materials", x=500, y=970, size=22, font="Virelai Sans",
               color="#C4AE82", justify="center")
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


caption("BUNK BED", "PINE · COTTON · WOOL")
d.finish("bunk-bed-V1R00")
