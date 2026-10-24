#!/usr/bin/env python3
"""Console table — field plate V1R00. Three-quarter view from front-right-above:
a narrow wall-side table doing one thing well — pale veined marble slab on a
gilded neoclassical base: fluted square legs, brass sabots, a carved apron with
a shell medallion, and a low under-tier shelf. A gilt calling-card bowl on the
marble sells the entry-hall mood. Gilded plate. 1000x1000.
Modelled in inches (x right, y up, +z back); face-culled prisms, yaw+pitch.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Console Table — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#241405"   # warm umber, never black
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


# --- projection ------------------------------------------------------------------
YAW, PITCH = math.radians(28), math.radians(22)
S, OX, OY = 12.0, 500.0, 670.0
CY, SY = math.cos(YAW), math.sin(YAW)
CP, SP = math.cos(PITCH), math.sin(PITCH)


def P(x, y, z):
    xr, zr = x * CY + z * SY, -x * SY + z * CY
    p = (OX + S * xr, OY - S * (y * CP + zr * SP))
    EXTENT.append(p)
    return p


def depth(x, y, z):
    """View-space distance; smaller = nearer the viewer (front-right-above)."""
    return -x * SY * CP - y * SP + z * CY * CP


def box(x0, y0, z0, x1, y1, z1):
    """8 corners of an axis-aligned box, near quad (-z) first, CCW from below-left."""
    return [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
            (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]


FACES = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4),
         (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
TO_VIEWER = (SY * CP, SP, -CY * CP)          # normals facing this draw
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
    """Mix two hex colors at brightness b in [0,1]."""
    a = [int(hex1[i:i + 2], 16) for i in (1, 3, 5)]
    c = [int(hex2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02X%02X%02X" % tuple(round(a[i] + (c[i] - a[i]) * b) for i in range(3))


# palettes: (dark, light) ramps per material
GILT_D, GILT_L = "#4E3012", "#D8AC54"    # gilded wood
GILT_HI = "#F2D68C"
MARBLE_D, MARBLE_L = "#9A968C", "#F0ECE2"
BRASS_D, BRASS_L = "#6E4E1E", "#E2BC66"


def prism(name, corners, dark=GILT_D, light=GILT_L, lo=0.06, hi=0.94, ink=1.8):
    """Draw the viewer-facing faces of an 8-corner prism, far to near."""
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


def seg3(name, pts3, stroke, sw, opacity=None, dash=None):
    """Polyline through 3D points, no culling."""
    kw = {"fill": NONE, "stroke": stroke, "strokeWidth": sw, "cap": "round"}
    if opacity is not None:
        kw["opacity"] = opacity
    if dash is not None:
        kw["dash"] = dash
    q = [P(*p) for p in pts3]
    d.path("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in q), name, **kw)


# --- backdrop + plate ---------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#1A120C"), (1, "#0A0604")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#B89050", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#8E7040"), (0.6, "#5A4226"), (1, "#211608")),
        stroke="#140D06", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#EED49A", strokeWidth=3, opacity=24)
d.shape("ellipse", "Entry lamplight", x=180, y=110, width=600, height=560,
        fill=rad((0, "#F2C87E", 20), (0.55, "#B8864A", 7), (1, "#6E4A28", 0)),
        stroke=NONE)
for i, (x, y, w) in enumerate([(208, 228, 6), (780, 252, 7), (170, 622, 6), (828, 596, 7),
                               (430, 104, 6), (636, 106, 7), (168, 420, 6), (842, 430, 6)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#C8A060", opacity=30, stroke=NONE)

FY = 706
hx = math.sqrt(PR ** 2 - (FY - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{FY} L{PCX + hx:.1f},{FY} A420,420 0 0 1 {PCX - hx:.1f},{FY} Z",
       "Floor", fill=lin((0, FY), (0, 880), (0, "#4E3E26", 40), (1, "#140C06", 76)),
       stroke=NONE)
d.path(f"M{PCX - hx + 6:.1f},{FY} L{PCX + hx - 6:.1f},{FY}", "Floor edge light",
       fill=NONE, stroke="#E8CC92", strokeWidth=2, opacity=20)

# grounding shadow under the table
sh = [P(x, 0, z) for x in (-21, 21) for z in (-7, 7)]
sx0, sx1 = min(p[0] for p in sh) - 36, max(p[0] for p in sh) + 36
sy0, sy1 = min(p[1] for p in sh) - 20, max(p[1] for p in sh) + 26
d.shape("ellipse", "Table shadow", x=round(sx0), y=round(sy0),
        width=round(sx1 - sx0), height=round(sy1 - sy0),
        fill=rad((0, "#060402", 66), (0.6, "#060402", 26), (1, "#060402", 0)),
        stroke=NONE)

# --- geometry (inches) ---------------------------------------------------------------
LW, LD = 2.0, 2.0                     # leg section
LX, LZ = 19.0, 5.0                    # leg centres
AY0, AY1 = 29.5, 33.0                 # apron band
TY0, TY1 = 33.0, 34.3                 # marble slab
TX0, TX1, TZ0, TZ1 = -22.8, 22.8, -8.2, 8.2
SY0, SY1 = 5.0, 6.4                   # under-tier shelf


def leg(nm, cx, cz):
    """Sabot foot, fluted square leg, capital collar."""
    prism(f"{nm} sabot", box(cx - 1.3, 0, cz - 1.3, cx + 1.3, 1.9, cz + 1.3),
          dark=BRASS_D, light=BRASS_L, lo=0.15, hi=1.0, ink=1.6)
    prism(f"{nm} leg", box(cx - LW / 2, 1.9, cz - LD / 2,
                           cx + LW / 2, AY0, cz + LD / 2), lo=0.10, hi=1.0)
    prism(f"{nm} capital", box(cx - 1.25, AY0 - 1.9, cz - 1.25,
                               cx + 1.25, AY0, cz + 1.25), lo=0.12, hi=1.0, ink=1.6)


# back pair first (farthest), then shelf, then front pair
leg("Back left", -LX, LZ)
leg("Back right", LX, LZ)
prism("Under-tier", box(-LX - 0.4, SY0, -LZ - 0.4, LX + 0.4, SY1, LZ + 0.4),
      dark="#3E260E", light="#A87E3E", lo=0.08, hi=0.92, ink=1.6)
seg3("Shelf lip light", [(-LX - 0.3, SY1, -LZ - 0.46), (LX + 0.3, SY1, -LZ - 0.46)],
     "#D8AC60", 2.0, 45)
leg("Front left", -LX, -LZ)
leg("Front right", LX, -LZ)

# fluting: paired channels down each visible leg face, gilt light/dark pairs
for nm, cx, cz, fx, fz in [("FL", -LX, -LZ, -1, -1), ("FR", LX, -LZ, 1, -1)]:
    for k in (-0.45, 0.45):
        seg3(f"{nm} flute {k:+.2f}", [(cx + k, 4.2, cz - LD / 2 - 0.06),
                                     (cx + k, AY0 - 3.4, cz - LD / 2 - 0.06)],
             "#2E1C0A", 1.8, 55)
for k in (-0.45, 0.45):
    seg3(f"FR side flute {k:+.2f}", [(LX + LW / 2 + 0.06, 4.2, -LZ + k),
                                    (LX + LW / 2 + 0.06, AY0 - 3.4, -LZ + k)],
         "#2E1C0A", 1.8, 45)

# --- apron: rails between the legs ---------------------------------------------------
prism("Apron back", box(-21, AY0, LZ - 0.6, 21, AY1, LZ + 1.4), lo=0.05, hi=0.85, ink=1.6)
prism("Apron right", box(LX - 0.6, AY0, -LZ, LX + 2.0, AY1, LZ),
      dark="#3E260E", light="#B8863E", lo=0.08, hi=0.95, ink=1.8)
prism("Apron front", box(-21, AY0, -LZ - 1.9, 21, AY1, -LZ + 0.9), lo=0.15, hi=1.05, ink=2.0)

# shell medallion centred on the front apron, screen-space
mcx, mcy = P(0, (AY0 + AY1) / 2 - 0.4, -LZ - 1.95)
bx, by = mcx, mcy + 9                     # shell base
arc_pts = []
for tdeg in (18, 48, 78, 108, 138, 168):
    t = math.radians(tdeg)
    arc_pts.append((mcx + 15 * math.cos(t), mcy - 15 * math.sin(t) * 0.8))
d.path(f"M{mcx - 15:.1f},{mcy:.1f} A15,12 0 0 1 {mcx + 15:.1f},{mcy:.1f}",
       "Shell fan arc", fill=NONE, stroke=GILT_HI, strokeWidth=2.2, cap="round", opacity=85)
for i, (px, py) in enumerate(arc_pts):
    d.path(f"M{bx:.1f},{by:.1f} L{px:.1f},{py:.1f}", f"Shell spoke {i+1}",
           fill=NONE, stroke=GILT_HI, strokeWidth=1.8, cap="round", opacity=80)
d.shape("ellipse", "Shell bead", x=round(bx - 2.6), y=round(by - 1.5), width=5.2, height=4.4,
        fill=rad((0, GILT_HI), (1, BRASS_D)), stroke=INK, strokeWidth=1.0)

# --- marble slab ----------------------------------------------------------------------
prism("Marble top", box(TX0, TY0, TZ0, TX1, TY1, TZ1),
      dark=MARBLE_D, light=MARBLE_L, lo=0.35, hi=1.05, ink=2.0)
# veins: thin grey strokes wandering across the top face
seg3("Vein 1", [(-20, TY1 + 0.05, -4.5), (-12, TY1 + 0.05, -5.4),
                (-4, TY1 + 0.05, -4.0), (3, TY1 + 0.05, -5.0)],
     "#5E5A52", 1.7, 55)
seg3("Vein 2", [(6, TY1 + 0.05, 2.5), (12, TY1 + 0.05, 1.4),
                (18, TY1 + 0.05, 2.6), (21, TY1 + 0.05, 1.2)],
     "#6E6A62", 1.6, 50)
seg3("Vein 3", [(-8, TY1 + 0.05, 4.4), (-1, TY1 + 0.05, 5.2),
                (7, TY1 + 0.05, 4.6)], "#8A867C", 1.5, 45)
seg3("Vein 4", [(-17, TY1 + 0.05, 1.8), (-11, TY1 + 0.05, 3.0),
                (-4, TY1 + 0.05, 2.2), (1, TY1 + 0.05, 3.4)],
     "#7A766C", 1.4, 42)
# polish line along the slab's lit front edge
seg3("Top edge light", [(TX0 + 1, TY1 + 0.1, TZ0 + 0.4),
                        (TX1 - 1, TY1 + 0.1, TZ0 + 0.4)], "#FAF6EA", 2.4, 60)

# --- calling-card bowl on the marble, left of centre ----------------------------------
bcx, bcy = P(-8.5, TY1 + 0.2, -0.5)
br = 26
d.shape("ellipse", "Bowl shadow", x=round(bcx - br * 1.05), y=round(bcy - 4),
        width=round(br * 2.1), height=10,
        fill=rad((0, "#100A04", 50), (1, "#100A04", 0)), stroke=NONE)
d.path(f"M{bcx - br:.1f},{bcy - 2:.1f} "
       f"C{bcx - br * 0.9:.1f},{bcy + br * 0.52:.1f} {bcx - br * 0.4:.1f},{bcy + br * 0.62:.1f} {bcx:.1f},{bcy + br * 0.62:.1f} "
       f"C{bcx + br * 0.4:.1f},{bcy + br * 0.62:.1f} {bcx + br * 0.9:.1f},{bcy + br * 0.52:.1f} {bcx + br:.1f},{bcy - 2:.1f} Z",
       "Card bowl", fill=lin((bcx - br, bcy), (bcx + br, bcy),
                             (0, "#8A6428"), (0.45, "#E8C87E"), (1, "#6E4C1C")),
       stroke=INK, strokeWidth=2.0, join="round")
d.shape("ellipse", "Bowl rim", x=round(bcx - br), y=round(bcy - 8.5),
        width=round(br * 2), height=13,
        fill=rad((0, "#3E2A10"), (0.7, "#5E4218"), (1, "#8A6428")),
        stroke=INK, strokeWidth=1.8)
# one cream card leaning in the bowl
card = [(bcx - 6, bcy - 26), (bcx + 15, bcy - 21), (bcx + 12, bcy - 5), (bcx - 9, bcy - 10)]
d.path(poly(card), "Calling card", fill=lin((bcx - 6, bcy - 26), (bcx + 12, bcy - 5),
       (0, "#F6EFDC"), (1, "#DCCFAE")), stroke="#8A7A5E", strokeWidth=1.4, join="round")
d.path(f"M{bcx - 4:.1f},{bcy - 20:.1f} L{bcx + 11:.1f},{bcy - 16.5:.1f}",
       "Card rule", fill=NONE, stroke="#B8A888", strokeWidth=1.4, opacity=70, cap="round")
d.path(f"M{bcx - br + 5:.1f},{bcy + 2:.1f} C{bcx - br * 0.5:.1f},{bcy + br * 0.5:.1f} "
       f"{bcx + br * 0.3:.1f},{bcy + br * 0.52:.1f} {bcx + br - 8:.1f},{bcy + 3:.1f}",
       "Bowl sheen", fill=NONE, stroke="#F6E2AC", strokeWidth=2.2, opacity=55, cap="round")

# --- extent check ---------------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("console extent: farthest point %.0f from centre (rim %d)" % (far, PR))
assert far < PR - 24, far


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
               color="#F4E6C8", justify="center")
    m = d.text(mats, "Materials", x=500, y=970, size=22, font="Virelai Sans",
               color="#D2B078", justify="center")
    d.cmd("text.setStyle", "Name tracking", ids=[n["id"]], tracking=60)
    d.cmd("text.setStyle", "Materials tracking", ids=[m["id"]], tracking=240)
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


caption("CONSOLE TABLE", "GILTWOOD · MARBLE · BRASS")
d.finish("console-table-V1R00")
