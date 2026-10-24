#!/usr/bin/env python3
"""Cedar chest — field plate V1R00. Three-quarter view from the front right:
a blanket chest with its lid open past vertical, pale aromatic cedar inside,
a stack of folded trousseau linens in the cavity and one quilt draped over
the front lip. Warm umber plate, trousseau mood. 1000x1000.
Modelled in inches (x right, y up, +z back) and projected with a fixed
yaw + pitch; the carcass is five thin slabs so face-culling opens the
cavity; the lid is a prism rotated about its hinge line.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Cedar Chest — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#26140C"   # warm dark, not black
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
    """Catmull-Rom through pts as cubic Beziers."""
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
YAW, PITCH = math.radians(28), math.radians(22)
S, OX, OY = 12.0, 500.0, 655.0
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
EXT_D, EXT_L = "#3E1E12", "#A86844"      # aged cedar exterior
EXT_HI = "#D89E70"
INT_D, INT_L = "#A07048", "#EAC694"      # pale aromatic interior
LIN_D, LIN_L = "#B8A488", "#F4EAD2"      # ivory linen
ROS_D, ROS_L = "#7E4A44", "#C88E84"      # dusty rose quilt


def prism(name, corners, dark=EXT_D, light=EXT_L, lo=0.06, hi=0.94, ink=1.8):
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


def quad3(name, pts3, fill, stroke=NONE, sw=1.6, opacity=None):
    """One flat quad from 3D points, no culling — caller orders it."""
    kw = {"fill": fill}
    if stroke != NONE:
        kw.update(stroke=stroke, strokeWidth=sw, join="round")
    else:
        kw["stroke"] = NONE
    if opacity is not None:
        kw["opacity"] = opacity
    d.path(poly([P(*p) for p in pts3]), name, **kw)


def rot_hinge(p, a):
    """Rotate point p about the lid hinge axis (x axis through y=HY, z=HZ)."""
    x, y, z = p
    dy, dz = y - HINGE[0], z - HINGE[1]
    ca, sa = math.cos(a), math.sin(a)
    return (x, HINGE[0] + dy * ca - dz * sa, HINGE[1] + dy * sa + dz * ca)


# --- backdrop + plate ---------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#1C1410"), (1, "#0A0605")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#9A7A52", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#6E5638"), (0.6, "#463524"), (1, "#1E160E")),
        stroke="#120B07", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8D2A0", strokeWidth=3, opacity=22)
d.shape("ellipse", "Lamplight", x=200, y=120, width=580, height=580,
        fill=rad((0, "#F0BE7A", 18), (0.55, "#A87840", 6), (1, "#6E4A28", 0)),
        stroke=NONE)

FY = 612
hx = math.sqrt(PR ** 2 - (FY - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{FY} L{PCX + hx:.1f},{FY} A420,420 0 0 1 {PCX - hx:.1f},{FY} Z",
       "Floor", fill=lin((0, FY), (0, 880), (0, "#584632", 42), (1, "#160D08", 78)),
       stroke=NONE)
d.path(f"M{PCX - hx + 6:.1f},{FY} L{PCX + hx - 6:.1f},{FY}", "Floor edge light",
       fill=NONE, stroke="#E8D0A0", strokeWidth=2, opacity=20)

# grounding shadow under the chest
sh = [P(x, 0, z) for x in (-19.5, 19.5) for z in (-10, 10)]
sx0, sx1 = min(p[0] for p in sh) - 40, max(p[0] for p in sh) + 40
sy0, sy1 = min(p[1] for p in sh) - 24, max(p[1] for p in sh) + 30
d.shape("ellipse", "Chest shadow", x=round(sx0), y=round(sy0),
        width=round(sx1 - sx0), height=round(sy1 - sy0),
        fill=rad((0, "#050302", 68), (0.6, "#050302", 28), (1, "#050302", 0)),
        stroke=NONE)

# --- chest geometry (inches; x right, y up, +z back) ----------------------------------
X0, X1 = -19.0, 19.0
Z0, Z1 = -9.5, 9.5
WY0, WY1 = 4.0, 18.0              # walls span this y range
T = 1.3                           # wall thickness
HINGE = (WY1, Z1)                 # lid hinge: y, z
LID_T = 2.2
LID_A = math.radians(105)         # open past vertical

# --- open lid (farthest structure) -----------------------------------------------------
lid = [rot_hinge(p, LID_A) for p in box(X0, WY1, Z0, X1, WY1 + LID_T, Z1)]
prism("Lid", lid, dark="#8A5E3E", light="#E8C89A", lo=0.35, hi=1.0, ink=2.0)
# panel inlay on the lid's interior face (closed-lid bottom = corners 0,1,5,4 rotated)
inner = [lid[i] for i in (0, 1, 5, 4)]
cx = [sum(p[i] for p in inner) / 4 for i in range(3)]
inset = [(cx[0] + (p[0] - cx[0]) * 0.86, cx[1] + (p[1] - cx[1]) * 0.86,
          cx[2] + (p[2] - cx[2]) * 0.86) for p in inner]
ys = [P(*p)[1] for p in inset]
quad3("Lid inner panel", inset,
      lin((0, min(ys)), (0, max(ys)), (0, "#F6E2BC"), (1, "#D8AE7E")),
      stroke="#8A5A38", sw=1.8)
# brass stay hinge hints at both lid ends, small blocks on the back edge
for nm, hx0 in (("L", X0 + 2.2), ("R", X1 - 4.2)):
    hpts = [rot_hinge(p, LID_A) for p in box(hx0, WY1 - 0.4, Z1 - 0.9, hx0 + 2.0, WY1 + 0.9, Z1 + 0.2)]
    prism(f"Hinge {nm}", hpts, dark="#6E4E1E", light="#D9B25E", lo=0.2, hi=1.0, ink=1.4)

# --- carcass: five slabs so the cavity is real -----------------------------------------
# bottom floor slab first (its top face is the cavity floor, pale)
prism("Cavity floor", box(X0, WY0, Z0, X1, WY0 + 1.6, Z1),
      dark=INT_D, light=INT_L, lo=0.30, hi=1.0)
# back wall — pale interior face toward the viewer
prism("Back wall", box(X0, WY0, Z1 - T, X1, WY1, Z1),
      dark=INT_D, light=INT_L, lo=0.40, hi=1.05)
# left wall — pale interior face (+x normal) toward the viewer
prism("Left wall", box(X0, WY0, Z0, X0 + T, WY1, Z1),
      dark="#96684A", light="#DCB486", lo=0.30, hi=0.95)
# right wall — exterior palette (its interior is culled from this view)
prism("Right wall", box(X1 - T, WY0, Z0, X1, WY1, Z1), lo=0.05, hi=0.9)

# --- trousseau linens inside the cavity -------------------------------------------------
prism("Folded sheet", box(X0 + 3.4, WY0 + 1.6, Z0 + 2.6, X1 - 3.0, WY0 + 7.0, Z1 - 2.8),
      dark=LIN_D, light=LIN_L, lo=0.30, hi=1.05, ink=1.6)
prism("Folded quilt", box(X0 + 4.4, WY0 + 7.0, Z0 + 3.4, X1 - 4.2, WY0 + 11.6, Z1 - 3.6),
      dark=ROS_D, light=ROS_L, lo=0.12, hi=0.95, ink=1.6)
# fold shadows on the linen stack's visible top faces
for i, yy in enumerate((WY0 + 6.9, WY0 + 11.5)):
    a = P(X0 + 5.0, yy, Z0 + 2.4)
    b = P(X1 - 4.6, yy - 0.3, Z0 + 3.2)
    d.path(f"M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}", f"Linen fold {i+1}",
           fill=NONE, stroke="#7A5C40", strokeWidth=1.8, opacity=40, cap="round")
# top folded blanket, left half of the cavity, cresting just over the front rim
prism("Top blanket", box(X0 + 3.0, WY0 + 11.6, Z0 + 2.2, -1.0, WY0 + 15.4, Z1 - 4.0),
      dark="#8E6A52", light="#E8D4AC", lo=0.25, hi=1.0, ink=1.8)
# its front fold line where the crest rolls over
fa, fb = P(X0 + 4.0, WY0 + 15.2, Z0 + 2.0), P(-1.6, WY0 + 15.2, Z0 + 3.4)
d.path(f"M{fa[0]:.1f},{fa[1]:.1f} L{fb[0]:.1f},{fb[1]:.1f}", "Blanket crest fold",
       fill=NONE, stroke="#7A5C40", strokeWidth=2.0, opacity=45, cap="round")

# --- front slab + base rail ----------------------------------------------------------------
prism("Front wall", box(X0, WY0, Z0, X1, WY1, Z0 + T), lo=0.10, hi=1.0, ink=2.0)
# recessed panels on the front face
for i, (px0, px1) in enumerate(((X0 + 3.2, -3.2), (3.2, X1 - 3.2))):
    pnl = [(px0, WY0 + 2.4, Z0 - 0.08), (px1, WY0 + 2.4, Z0 - 0.08),
           (px1, WY1 - 2.4, Z0 - 0.08), (px0, WY1 - 2.4, Z0 - 0.08)]
    ysp = [P(*p)[1] for p in pnl]
    quad3(f"Front panel {i+1}", pnl,
          lin((0, min(ysp)), (0, max(ysp)), (0, "#8A5230"), (1, "#5E3018")),
          stroke="#2E1409", sw=1.8)
    # inner bevel light along the panel top
    a = P(px0 + 0.7, WY1 - 3.0, Z0 - 0.1)
    b = P(px1 - 0.7, WY1 - 3.0, Z0 - 0.1)
    d.path(f"M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}", f"Panel bevel {i+1}",
           fill=NONE, stroke="#DCA878", strokeWidth=1.8, opacity=45, cap="round")

# base rail, slightly proud and darker, grounds the chest
prism("Base rail", box(X0 - 0.5, 0, Z0 - 0.5, X1 + 0.5, WY0 + 0.4, Z1 + 0.5),
      dark="#28120A", light="#6E3C22", lo=0.06, hi=0.85, ink=2.0)

# brass lock escutcheon at the front rim centre
ex, ey = P(0, WY1 - 1.8, Z0 - 0.15)
d.path(f"M{ex:.1f},{ey - 10:.1f} L{ex + 7:.1f},{ey:.1f} L{ex:.1f},{ey + 10:.1f} L{ex - 7:.1f},{ey:.1f} Z",
       "Escutcheon", fill=lin((ex - 7, ey), (ex + 7, ey), (0, "#F2DA94"), (1, "#9A7028")),
       stroke="#4A340E", strokeWidth=1.6)
d.shape("ellipse", "Keyhole", x=round(ex - 2.4), y=round(ey - 1), width=5, height=7,
        fill="#1E0E04", stroke=NONE)

# --- quilt draped over the front lip, right of the escutcheon -------------------------------
# hangs from inside the cavity over the front rim and down the front face
over = P(11.0, WY1 + 0.4, Z0 - 1.0)
hang = [(6.2, WY1 - 1.8, Z0 - 0.6), (7.0, WY1 + 0.9, Z0 - 0.4),
        (14.6, WY1 + 0.7, Z0 - 0.6), (15.8, WY1 - 1.4, Z0 - 0.5),
        (16.4, WY1 - 4.6, Z0 - 0.9), (15.9, WY1 - 7.6, Z0 - 1.0),
        (13.0, WY1 - 8.1, Z0 - 1.0), (8.8, WY1 - 8.0, Z0 - 1.0),
        (6.4, WY1 - 6.4, Z0 - 0.8)]
hang2 = [P(*p) for p in hang]
d.path(smooth(hang2, k=0.9), "Draped quilt", stroke=INK, strokeWidth=1.8, join="round",
       fill=lin((over[0], over[1] - 30), (over[0] + 20, over[1] + 90),
                (0, "#E8D8B8"), (0.5, "#C4A87E"), (1, "#96755A")))
for i, fx in enumerate(((8.6, 8.2), (11.4, 11.6), (14.4, 14.9))):
    a = P(fx[0], WY1 + 0.3, Z0 - 0.75)
    b = P(fx[1], WY1 - 6.6, Z0 - 1.05)
    d.path(f"M{a[0]:.1f},{a[1]:.1f} Q{(a[0] + b[0]) / 2 - 4:.1f},{(a[1] + b[1]) / 2:.1f} {b[0]:.1f},{b[1]:.1f}",
           f"Drape fold {i+1}", fill=NONE, stroke="#8E6E4E", strokeWidth=1.8, opacity=50, cap="round")

# warm sheen where lamplight grazes the lid and the front top edge
gx, gy = P(-4, WY1 + 2.0, Z1 - 1)
d.shape("ellipse", "Lid sheen", x=round(gx - 90), y=round(gy - 30), width=180, height=60,
        fill=rad((0, EXT_HI, 20), (1, EXT_HI, 0)), stroke=NONE)
fe0, fe1 = P(X0 + 2, WY1 - 0.3, Z0 - 0.2), P(X1 - 2, WY1 - 0.3, Z0 - 0.2)
d.path(f"M{fe0[0]:.1f},{fe0[1]:.1f} L{fe1[0]:.1f},{fe1[1]:.1f}", "Front rim light",
       fill=NONE, stroke="#E8C090", strokeWidth=2.5, opacity=40, cap="round")

# --- extent check ---------------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("chest extent: farthest point %.0f from centre (rim %d)" % (far, PR))
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
               color="#F4E4CE", justify="center")
    m = d.text(mats, "Materials", x=500, y=970, size=22, font="Virelai Sans",
               color="#C9A582", justify="center")
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


caption("CEDAR CHEST", "CEDAR · BRASS · LINEN")
d.finish("cedar-chest-V1R00")
