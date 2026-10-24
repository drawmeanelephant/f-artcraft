#!/usr/bin/env python3
"""Futon — field plate V1R00. Three-quarter view from front-right-above: the
frame that folds flat into a bed or up into a sofa, shown mid-life as a sofa —
slab pine arms, a tri-fold cotton mattress bent at the hinge (seat flat, back
leaning), welt cords and tufted buttons, and a denim pillow against the arm.
Cotton-and-pine plate, first-apartment mood. 1000x1000.
Modelled in inches (x right, y up, +z back); face-culled prisms, yaw+pitch.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Futon — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#241606"
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
S, OX, OY = 11.0, 500.0, 695.0
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
PINE_D, PINE_L = "#7A5626", "#E0B972"    # honey pine
COT_D, COT_L = "#8A7A58", "#EAE0C8"      # cotton ticking
DEN_D, DEN_L = "#3E5E7A", "#7A9EB8"      # denim pillow


def prism(name, corners, dark=PINE_D, light=PINE_L, lo=0.06, hi=0.94, ink=1.8):
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


def quad3(name, pts3, dark, light, lo=0.2, hi=0.9, ink=1.8, flip=False):
    """Single flat quad in 3D; gradient keyed to its projected bbox."""
    q = [P(*p) for p in pts3]
    y0, y1 = min(p[1] for p in q), max(p[1] for p in q)
    if flip:
        g = lin((0, y1), (0, y0), (0, shade(dark, light, hi)), (1, shade(dark, light, lo)))
    else:
        g = lin((0, y0), (0, y1), (0, shade(dark, light, min(1, hi + 0.1))),
                                 (1, shade(dark, light, lo)))
    d.path(poly(q), name, fill=g, stroke=INK, strokeWidth=ink, join="round")


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
        fill=lin((0, 0), (0, 1000), (0, "#16100D"), (1, "#060403")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#A8804C", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#684A2A"), (0.6, "#3C2712"), (1, "#130B04")),
        stroke="#100A04", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#EFCB96", strokeWidth=3, opacity=24)
d.shape("ellipse", "Window light", x=185, y=125, width=540, height=500,
        fill=rad((0, "#F2CC86", 17), (0.55, "#B8864A", 6), (1, "#6E4A28", 0)),
        stroke=NONE)
for i, (x, y, w) in enumerate([(210, 232, 6), (780, 250, 7), (172, 624, 6), (826, 594, 7),
                               (432, 106, 6), (634, 104, 7), (168, 426, 6), (838, 428, 6)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#CBA063", opacity=30, stroke=NONE)

FY = 708
hx = math.sqrt(PR ** 2 - (FY - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{FY} L{PCX + hx:.1f},{FY} A420,420 0 0 1 {PCX - hx:.1f},{FY} Z",
       "Floor", fill=lin((0, FY), (0, 880), (0, "#4A3622", 42), (1, "#120A05", 78)),
       stroke=NONE)
d.path(f"M{PCX - hx + 6:.1f},{FY} L{PCX + hx - 6:.1f},{FY}", "Floor edge light",
       fill=NONE, stroke="#E8CC92", strokeWidth=2, opacity=20)

# grounding shadow under the frame
sh = [P(x, 0, z) for x in (-22, 22) for z in (-10, 11.5)]
sx0, sx1 = min(p[0] for p in sh) - 32, max(p[0] for p in sh) + 32
sy0, sy1 = min(p[1] for p in sh) - 18, max(p[1] for p in sh) + 24
d.shape("ellipse", "Frame shadow", x=round(sx0), y=round(sy0),
        width=round(sx1 - sx0), height=round(sy1 - sy0),
        fill=rad((0, "#060302", 62), (0.6, "#060302", 24), (1, "#060302", 0)),
        stroke=NONE)

# --- arms: slab panels, trapezoid profile (y,z) --------------------------------------------
ARMX = (19.0, 22.0)                            # arm slab spans x 19..22
PROF = [(0, -9.5), (0, 11.5), (24, 10.5), (15, -3), (14, -9.5)]


def arm(side):
    x0, x1 = (-22, -19) if side < 0 else (19, 22)
    # front cap: narrow face at z = -9.5, visible on both arms
    quad3(f"{side:+d} arm front", [(x0, 0, -9.5), (x1, 0, -9.5),
                                   (x1, 14, -9.5), (x0, 14, -9.5)],
          PINE_D, PINE_L, lo=0.15, hi=0.85, ink=1.8)
    # top strip: along the sloped profile edge, both segments
    quad3(f"{side:+d} arm top rear", [(x0, 24, 10.5), (x1, 24, 10.5),
                                      (x1, 15, -3), (x0, 15, -3)],
          PINE_D, PINE_L, lo=0.35, hi=1.05, ink=1.6)
    quad3(f"{side:+d} arm top front", [(x0, 15, -3), (x1, 15, -3),
                                       (x1, 14, -9.5), (x0, 14, -9.5)],
          PINE_D, PINE_L, lo=0.3, hi=1.0, ink=1.6)
    if side > 0:
        # right arm shows its outside face
        pts = [(x1, y, z) for y, z in PROF]
        quad3("Right arm face", pts, PINE_D, PINE_L, lo=0.12, hi=0.8, ink=2.0, flip=True)
        # grain hint down the panel
        seg3("Arm grain 1", [(x1 + 0.05, 3, 8.5), (x1 + 0.05, 12, 4.5)], "#5E3E18", 1.8, 45)
        seg3("Arm grain 2", [(x1 + 0.05, 2, -4), (x1 + 0.05, 10, -7.5)], "#5E3E18", 1.6, 40)


arm(-1)
arm(+1)

# stretcher bar under the seat, between the arms
prism("Stretcher", box(-19, 4.5, -8.2, 19, 6.8, -6.4),
      dark="#5E3E18", light="#B08A4C", lo=0.08, hi=0.85, ink=1.6)

# --- mattress: seat flat, back leaning -----------------------------------------------------
prism("Seat cushion", box(-19, 9.0, -10.5, 19, 13.6, 5.2),
      dark=COT_D, light=COT_L, lo=0.25, hi=1.0, ink=2.0)
# tri-fold seam across the front face: the folded-over layer
seg3("Fold seam", [(-18.6, 11.4, -10.6), (18.6, 11.4, -10.6)], "#7A6A48", 2.6, 65)
foldq = [P(-18.6, 9.2, -10.58), P(18.6, 9.2, -10.58),
         P(18.6, 11.35, -10.58), P(-18.6, 11.35, -10.58)]
fy0, fy1 = min(p[1] for p in foldq), max(p[1] for p in foldq)
d.path(poly(foldq), "Fold flap",
       fill=lin((0, fy0), (0, fy1), (0, "#9A8A64"), (1, "#8A7A58")), stroke=NONE)

# back cushion: a slab leaning up-back from the hinge line
BY0, BZ0 = 13.2, 4.6                        # hinge point in the yz plane
BLEN, BTH = 18.5, 4.2                       # slab length and thickness
ANG = math.radians(70)                       # lean from horizontal
UY, UZ = math.sin(ANG), math.cos(ANG)        # along-slab direction (up-back)
NY, NZ = math.cos(ANG) * 1.0, -math.sin(ANG)  # slab normal toward the viewer
NY, NZ = UZ, -UY                             # = (cos70, -sin70): +y,-z — front side
E0 = (BY0, BZ0)
E1 = (BY0 + UY * BLEN, BZ0 + UZ * BLEN)
F0 = (BY0 + NY * BTH, BZ0 + NZ * BTH)        # front-bottom edge of the face
F1 = (BY0 + UY * BLEN + NY * BTH, BZ0 + UZ * BLEN + NZ * BTH)

# front face (big, toward viewer), top edge strip, right end cap
quad3("Back cushion face",
      [(-19, F0[0], F0[1]), (19, F0[0], F0[1]),
       (19, F1[0], F1[1]), (-19, F1[0], F1[1])],
      COT_D, COT_L, lo=0.35, hi=1.05, ink=2.0)
quad3("Back cushion crown",
      [(-19, F1[0], F1[1]), (19, F1[0], F1[1]),
       (19, E1[0], E1[1]), (-19, E1[0], E1[1])],
      COT_D, COT_L, lo=0.5, hi=1.1, ink=1.8)
quad3("Back cushion end",
      [(19, E0[0], E0[1]), (19, F0[0], F0[1]),
       (19, F1[0], F1[1]), (19, E1[0], E1[1])],
      "#6E6044", COT_D, lo=0.2, hi=0.9, ink=1.8)

# hinge shadow where seat meets back
seg3("Hinge shadow", [(-18.5, 13.9, 4.9), (18.5, 13.9, 4.9)], "#4A3E28", 4.5, 60)

# welt cords: piping along the cushion edges
seg3("Seat welt", [(-18.7, 13.7, -10.3), (18.7, 13.7, -10.3)], "#F4EAD4", 2.6, 55)
seg3("Back welt", [(-18.7, F1[0] + 0.1, F1[1] + 0.05), (18.7, F1[0] + 0.1, F1[1] + 0.05)],
     "#F4EAD4", 2.4, 55)
seg3("Back welt side", [(19.05, F0[0], F0[1]), (19.05, F1[0], F1[1])], "#F4EAD4", 2.2, 45)

# tufted buttons: dimple dots in a loose grid
def tuft(name, pt3):
    x, y = P(*pt3)
    d.shape("ellipse", name, x=round(x - 3.6), y=round(y - 2.8), width=7.2, height=5.6,
            fill=rad((0, "#5E5038", 0.75), (1, "#5E5038", 0.1)), stroke=NONE)
    d.shape("ellipse", name + " hi", x=round(x - 4.4), y=round(y - 3.9), width=2.6,
            height=2.0, fill="#F4EAD4", opacity=50, stroke=NONE)


for i, (tx, tz) in enumerate([(-13, -6), (-4.5, -5.4), (4.5, -5.4), (13, -6),
                              (-9, -0.6), (0, 0), (9, -0.6)]):
    tuft(f"Seat tuft {i+1}", (tx, 13.75, tz))
for i, ty in enumerate((19, 23.5, 28)):
    zf = BZ0 + (ty - BY0 - NY * BTH) * UZ / UY + NZ * BTH
    for j, tx in enumerate((-13, -4.5, 4.5, 13)):
        tuft(f"Back tuft {i*4+j+1}", (tx, ty, zf))

# --- denim pillow against the left end of the back cushion ---------------------------------
pcx, pcy = P(-13.6, 18.2, 0.9)
d.shape("ellipse", "Pillow shadow", x=round(pcx - 26), y=round(pcy + 18),
        width=52, height=11,
        fill=rad((0, "#0A0503", 0.5), (1, "#0A0503", 0)), stroke=NONE)
# puffy rotated square: corners + bulged edge midpoints
pd = math.radians(-16)
pc_, ps_ = math.cos(pd), math.sin(pd)
pw, ph = 30, 26
corners = [(-pw, -ph), (pw, -ph), (pw, ph), (-pw, ph)]
bulge = 0.16
pp = []
for k in range(4):
    ax_, ay_ = corners[k]
    bx_, by_ = corners[(k + 1) % 4]
    ca = (pcx + ax_ * pc_ - ay_ * ps_, pcy + ax_ * ps_ + ay_ * pc_)
    mx_, my_ = (ax_ + bx_) / 2, (ay_ + by_) / 2
    mb = (pcx + mx_ * (1 + bulge) * pc_ - my_ * (1 + bulge) * ps_,
          pcy + mx_ * (1 + bulge) * ps_ + my_ * (1 + bulge) * pc_)
    pp.append((ca, mb))
dpath = f"M{pp[0][0][0]:.1f},{pp[0][0][1]:.1f} "
for k in range(4):
    nxt = pp[(k + 1) % 4][0]
    dpath += f"Q{pp[k][1][0]:.1f},{pp[k][1][1]:.1f} {nxt[0]:.1f},{nxt[1]:.1f} "
d.path(dpath + "Z", "Pillow",
       fill=lin((pcx - 25, pcy - 25), (pcx + 25, pcy + 28),
                (0, DEN_L), (0.55, "#5E82A0"), (1, DEN_D)),
       stroke="#2A4256", strokeWidth=2.2, join="round")
d.shape("ellipse", "Pillow dimple", x=round(pcx - 4), y=round(pcy - 2.5), width=8,
        height=6, fill=rad((0, "#2A4256", 0.7), (1, "#2A4256", 0)), stroke=NONE)
for k, (dx, dy) in enumerate([(-14, -9), (13, -11), (15, 8), (-13, 11)]):
    d.path(f"M{pcx:.1f},{pcy:.1f} L{pcx + dx:.1f},{pcy + dy:.1f}",
           f"Pillow crease {k+1}", fill=NONE, stroke="#2A4256", strokeWidth=1.8,
           opacity=45, cap="round")

# --- extent check ---------------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("futon extent: farthest point %.0f from centre (rim %d)" % (far, PR))
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


caption("FUTON", "PINE · COTTON · DENIM")
d.finish("futon-V1R00")
