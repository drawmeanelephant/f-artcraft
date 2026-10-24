#!/usr/bin/env python3
"""Credenza — field plate V1R00. A low mid-century walnut sideboard: slab
carcass on tapered dowel legs, two sliding doors — the left one slid open
to show the bottle shelf it kept from its tasting-table days. Seen from
front-right, above. Walnut plate, mid-century mood. 1000x1000.
Modelled in inches (x right, y up, +z back) and projected with a fixed
yaw + pitch; the carcass is slabs so face-culling opens the cavity; the
open door is a thin prism slid sideways along its track.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Credenza — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#241108"   # warm dark, not black
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
    return {"gradient": {"kind": "linear", "start": [round(a[0], 1), round(b[0], 1)],
                         "end": [round(b[0], 1), round(b[1], 1)], "stops": stops(*pairs)}}


def rad(*pairs):
    return {"gradient": {"kind": "radial", "stops": stops(*pairs)}}


def poly(pts):
    return "M%.1f,%.1f " % pts[0] + " ".join("L%.1f,%.1f" % p for p in pts[1:]) + " Z"


# --- projection ------------------------------------------------------------------
YAW, PITCH = math.radians(26), math.radians(20)
S, OX, OY = 11.5, 500.0, 640.0
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
EXT_D, EXT_L = "#30160C", "#96613C"      # walnut exterior
DOOR_D, DOOR_L = "#3A1C0E", "#A8703F"    # door faces, a touch lighter
INT_D, INT_L = "#7E5434", "#C49A66"      # oiled interior
LEG_D, LEG_L = "#2A120A", "#7E4E2E"      # turned legs
BRASS_D, BRASS_L = "#8A6224", "#F6DE96"


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


def rbox(pivot, axis, a, c):
    """Rotate box corners `c` about `axis` ('x','y','z') through `pivot` by `a`."""
    ca, sa = math.cos(a), math.sin(a)
    i = {"x": 0, "y": 1, "z": 2}[axis]
    j, k = (i + 1) % 3, (i + 2) % 3
    out = []
    for p in c:
        q = list(p)
        dj, dk = p[j] - pivot[j], p[k] - pivot[k]
        q[j] = pivot[j] + dj * ca - dk * sa
        q[k] = pivot[k] + dj * sa + dk * ca
        out.append(tuple(q))
    return out


# --- backdrop + plate ---------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#16120E"), (1, "#080604")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#8A6A48", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#5E4A30"), (0.6, "#3E2E1C"), (1, "#191109")),
        stroke="#100A05", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E2CBA0", strokeWidth=3, opacity=22)
d.shape("ellipse", "Room light", x=190, y=110, width=600, height=560,
        fill=rad((0, "#F0BE7A", 16), (0.55, "#A87840", 6), (1, "#6E4A28", 0)),
        stroke=NONE)

FY = 640
hx = math.sqrt(PR ** 2 - (FY - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{FY} L{PCX + hx:.1f},{FY} A420,420 0 0 1 {PCX - hx:.1f},{FY} Z",
       "Floor", fill=lin((0, FY), (0, 880), (0, "#4E3E28", 40), (1, "#140C06", 78)),
       stroke=NONE)
d.path(f"M{PCX - hx + 6:.1f},{FY} L{PCX + hx - 6:.1f},{FY}", "Floor edge light",
       fill=NONE, stroke="#E8D0A0", strokeWidth=2, opacity=20)

# grounding shadow under the carcass
sh = [P(x, 0, z) for x in (-26, 26) for z in (-8, 8)]
sx0, sx1 = min(p[0] for p in sh) - 46, max(p[0] for p in sh) + 46
sy0, sy1 = min(p[1] for p in sh) - 22, max(p[1] for p in sh) + 30
d.shape("ellipse", "Credenza shadow", x=round(sx0), y=round(sy0),
        width=round(sx1 - sx0), height=round(sy1 - sy0),
        fill=rad((0, "#050302", 66), (0.6, "#050302", 26), (1, "#050302", 0)),
        stroke=NONE)

# --- geometry (inches; x right, y up, +z back) ----------------------------------------
X0, X1 = -26.0, 26.0
Z0, Z1 = -8.0, 8.0
LEG_H = 7.0                        # floor to carcass bottom
BY0, BY1 = LEG_H, LEG_H + 15.5     # carcass walls
T = 1.2                            # wall thickness
IX0, IX1 = X0 + T, X1 - T          # interior span between the side walls
MID = 0.0                          # centre divider between the two bays
SLIDE = 11.0                       # right door slid right, overhanging the end
DT = 1.0                           # door thickness
DY0, DY1 = BY0 + 0.6, BY1 - 0.18
MOUTH0, MOUTH1 = MID + 0.7, MID + SLIDE   # revealed mouth of the right bay

# --- legs: tapered dowels splayed a touch, dark walnut + brass ferrules --------------
for i, (lx, lz) in enumerate(((X0 + 2.2, Z0 + 1.6), (X1 - 2.2, Z0 + 1.6),
                              (X0 + 2.2, Z1 - 1.6), (X1 - 2.2, Z1 - 1.6))):
    sx = -1.4 if lx < 0 else 1.4
    sz = -1.0 if lz < 0 else 1.0
    # tapered leg in box() corner order: smaller foot ring kicked out by the splay
    legc = [(lx + sx - 0.8, 0, lz + sz - 0.8), (lx + sx + 0.8, 0, lz + sz - 0.8),
            (lx + 1.05, LEG_H, lz - 1.05), (lx - 1.05, LEG_H, lz - 1.05),
            (lx + sx - 0.8, 0, lz + sz + 0.8), (lx + sx + 0.8, 0, lz + sz + 0.8),
            (lx + 1.05, LEG_H, lz + 1.05), (lx - 1.05, LEG_H, lz + 1.05)]
    prism(f"Leg {i+1}", legc, dark=LEG_D, light=LEG_L, lo=0.10, hi=0.95, ink=1.6)
    fer = box(lx + sx * 0.85 - 0.95, 0.0, lz + sz * 0.85 - 0.95,
              lx + sx * 0.85 + 0.95, 1.4, lz + sz * 0.85 + 0.95)
    prism(f"Ferrule {i+1}", fer, dark=BRASS_D, light=BRASS_L, lo=0.15, hi=1.0, ink=1.3)

# --- open right bay: slabs so face-culling reveals the cavity --------------------------
# interior is drawn BEFORE the carcass shell: the nearer shell faces then occlude the
# interior everywhere except the mouth (painter's order)
# divider at MID: its +x face lights the cavity for this front-right view
prism("Divider", box(MID - 0.6, BY0, Z0 + T, MID + 0.6, BY1, Z1 - T),
      dark=INT_D, light=INT_L, lo=0.35, hi=1.05)
# interior slabs span the full carcass: the left bay interior peeks through the
# reveal over the closed door and must read as warm wood, not a void
prism("Cavity floor", box(IX0, BY0, Z0 + T, IX1, BY0 + 1.4, Z1 - T),
      dark=INT_D, light=INT_L, lo=0.30, hi=1.0)
prism("Cavity back", box(IX0, BY0, Z1 - T, IX1, BY1, Z1),
      dark=INT_D, light=INT_L, lo=0.40, hi=1.05)
# mid shelf inside the revealed mouth
prism("Cavity shelf", box(MID + 0.6, BY0 + 6.6, Z0 + T, MOUTH1, BY0 + 7.8, Z1 - T),
      dark="#6E4526", light="#C09060", lo=0.30, hi=1.0, ink=1.5)

# --- shelf contents: decanter + bottles, the tasting-table leftovers -------------------
def bottle(nm, bx, base, r, h, neck_r, neck_h, dark, light):
    prism(nm + " body", box(bx - r, base, -r * 0.7, bx + r, base + h, r * 0.7),
          dark=dark, light=light, lo=0.15, hi=1.0, ink=1.4)
    prism(nm + " neck", box(bx - neck_r, base + h, -neck_r, bx + neck_r,
                            base + h + neck_h, neck_r),
          dark=dark, light=light, lo=0.15, hi=1.0, ink=1.2)

SH = BY0 + 7.8                     # shelf top
bottle("Decanter", MID + 4.4, SH, 2.4, 3.2, 0.95, 2.4, "#5E2A18", "#D88E50")
bottle("Bottle tall", MID + 8.9, SH, 1.4, 4.4, 0.7, 2.8, "#28351C", "#8EA858")
# decanter stopper
sx, sy = P(MID + 4.4, SH + 3.2 + 2.4 + 0.7, 0)
d.shape("ellipse", "Decanter stopper", x=round(sx - 6), y=round(sy - 6), width=12, height=12,
        fill=rad((0, "#F2D9A0"), (1, "#9A7028")), stroke="#4A340E", strokeWidth=1.4)
# two tumblers on the cavity floor
for i, tx in enumerate((MID + 3.6, MID + 8.0)):
    prism(f"Tumbler {i+1}", box(tx - 1.1, BY0 + 1.4, Z0 + 2.4, tx + 1.1, BY0 + 3.7, Z0 + 4.6),
          dark="#9A7848", light="#F4D9A8", lo=0.30, hi=1.0, ink=1.3)

# --- carcass shell: drawn after the interior so its nearer faces occlude ---------------
prism("Top slab", box(X0, BY1, Z0, X1, BY1 + 1.4, Z1),
      dark="#3A1E10", light="#AA6E42", lo=0.10, hi=1.0, ink=2.0)
prism("Right side", box(X1 - T, BY0, Z0, X1, BY1, Z1), lo=0.05, hi=0.9)
prism("Left side", box(X0, BY0, Z0, X0 + T, BY1, Z1), lo=0.05, hi=0.9)
prism("Base rail", box(X0 + 1.4, BY0 - 1.0, Z0 + 0.6, X1 - 1.4, BY0, Z1 - 0.6),
      dark="#28120A", light="#6E3C22", lo=0.06, hi=0.85, ink=1.8)
# the top slab's left end face is back-facing and culled; cap it dark so the
# lining doesn't read as a hole at the carcass's left silhouette
_e0, _e1 = P(X0, BY1 + 1.4, Z1), P(X0, BY1, Z0)
quad3("Top slab end cap", [(X0, BY1, Z0), (X0, BY1, Z1),
                           (X0, BY1 + 1.4, Z1), (X0, BY1 + 1.4, Z0)],
      lin((0, min(_e0[1], _e1[1])), (0, max(_e0[1], _e1[1])), (0, "#5E3418"), (1, "#2A1208")),
      stroke=INK, sw=1.6)

# --- sliding doors ----------------------------------------------------------------------
# left door closed on the back track, covering the left bay
prism("Closed door", box(IX0, DY0, Z0 - 0.55, MID - 0.2, DY1, Z0 - 0.55 + DT),
      dark=DOOR_D, light=DOOR_L, lo=0.10, hi=1.0, ink=1.9)
# right door on the front track, slid right past the carcass end
OD0, OD1 = MID + 0.2 + SLIDE, IX1 + SLIDE
prism("Open door", box(OD0, DY0, Z0 - 1.3, OD1, DY1, Z0 - 1.3 + DT),
      dark=DOOR_D, light=DOOR_L, lo=0.12, hi=1.05, ink=1.9)

# door details: pull slots + grain hints
for nm, dx0, dx1, dz in (("Closed", IX0, MID - 0.2, Z0 - 0.6),
                         ("Open", OD0, OD1, Z0 - 1.35)):
    px = dx1 - 7.5 if nm == "Closed" else dx0 + 4.0   # pulls near the meeting edges
    a = P(px, DY0 + (DY1 - DY0) * 0.5, dz)
    b = P(px + 3.5, DY0 + (DY1 - DY0) * 0.5, dz)
    d.path(f"M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}", f"{nm} pull",
           fill=NONE, stroke="#1E0C04", strokeWidth=4.5, cap="round")
    for j, gy in enumerate((DY0 + 3.5, DY0 + 8.0)):
        g0 = P(dx0 + 2.5, gy, dz)
        g1 = P(dx1 - 2.5, gy + 0.4, dz)
        d.path(f"M{g0[0]:.1f},{g0[1]:.1f} L{g1[0]:.1f},{g1[1]:.1f}", f"{nm} grain {j+1}",
               fill=NONE, stroke="#5E3018", strokeWidth=1.8, opacity=45, cap="round")

# track shadow under the door line
t0, t1 = P(X0 + 1, DY0 - 0.4, Z0 - 0.2), P(X1 - 1, DY0 - 0.4, Z0 - 0.2)
d.path(f"M{t0[0]:.1f},{t0[1]:.1f} L{t1[0]:.1f},{t1[1]:.1f}", "Track shadow",
       fill=NONE, stroke="#1A0C05", strokeWidth=3, opacity=55, cap="round")

# warm sheen where room light grazes the top slab and the open door edge
gx, gy = P(8, BY1 + 1.4, -2)
d.shape("ellipse", "Top sheen", x=round(gx - 110), y=round(gy - 26), width=220, height=52,
        fill=rad((0, "#D89E70", 22), (1, "#D89E70", 0)), stroke=NONE)

# --- extent check ---------------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("credenza extent: farthest point %.0f from centre (rim %d)" % (far, PR))
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
               color="#F2E2C8", justify="center")
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


caption("CREDENZA", "WALNUT · BRASS")
d.finish("credenza-V1R00")
