#!/usr/bin/env python3
"""Davenport desk — field plate V1R00. Three-quarter view from front-right-above:
a compact upright ship captain's desk in walnut — sloped leather writing
surface, piano-top superstructure with crown moulding and gallery finials, a
right-side column of four drawers with one pulled out on a secret parchment,
a panelled knee door, bun feet and a small brass cabin lamp. Deep navy plate,
ship's-cabin mood. 1000x1000.
Modelled in inches (x right, y up, +z back); face-culled prisms, yaw+pitch.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Davenport Desk — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#1A0E06"
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
YAW, PITCH = math.radians(30), math.radians(22)
S, OX, OY = 11.0, 505.0, 672.0
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


WALNUT_D, WALNUT_L = "#3A1E0E", "#A06A3C"
WALNUT_XD, WALNUT_XL = "#5E3A1E", "#C89058"
BRASS_D, BRASS_L = "#6E4E1E", "#E8C470"
LEATHER_D, LEATHER_L = "#14261C", "#3E5E48"


def prism(name, corners, dark=WALNUT_D, light=WALNUT_L, lo=0.06, hi=0.94, ink=1.8):
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
    kw = {"fill": fill}
    if stroke != NONE:
        kw.update(stroke=stroke, strokeWidth=sw, join="round")
    else:
        kw["stroke"] = NONE
    if opacity is not None:
        kw["opacity"] = opacity
    d.path(poly([P(*p) for p in pts3]), name, **kw)


def dot3(name, x, y, z, rx, ry=None, **kw):
    sx, sy = P(x, y, z)
    rx2 = rx
    ry2 = rx if ry is None else ry
    kw.setdefault("stroke", INK)
    kw.setdefault("strokeWidth", 1.2)
    return d.shape("ellipse", name, x=round(sx - rx2, 1), y=round(sy - ry2, 1),
                   width=round(2 * rx2, 1), height=round(2 * ry2, 1), **kw)


# --- backdrop + plate: ship's cabin ------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#0E171C"), (1, "#04090C")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#5A7A86", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#3C4E5A"), (0.6, "#23303A"), (1, "#0D151B")),
        stroke="#080E12", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C8DAE2", strokeWidth=3, opacity=24)
d.shape("ellipse", "Lantern light", x=190, y=120, width=560, height=540,
        fill=rad((0, "#F0BE7A", 17), (0.55, "#A87E44", 6), (1, "#5E3E20", 0)),
        stroke=NONE)
for i, (x, y, w) in enumerate([(210, 235, 6), (778, 250, 7), (172, 618, 6), (826, 592, 7),
                               (428, 106, 6), (640, 108, 7), (166, 424, 6), (840, 418, 6)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#8AA2AE", opacity=28, stroke=NONE)

FY = 712
hx = math.sqrt(PR ** 2 - (FY - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{FY} L{PCX + hx:.1f},{FY} A420,420 0 0 1 {PCX - hx:.1f},{FY} Z",
       "Floor", fill=lin((0, FY), (0, 880), (0, "#2A3840", 40), (1, "#0A1114", 78)),
       stroke=NONE)
d.path(f"M{PCX - hx + 6:.1f},{FY} L{PCX + hx - 6:.1f},{FY}", "Floor edge light",
       fill=NONE, stroke="#C8D8DE", strokeWidth=2, opacity=18)

# grounding shadow
sh = [P(x, 0, z) for x in (-12, 12) for z in (-11, 11)]
sx0, sx1 = min(p[0] for p in sh) - 44, max(p[0] for p in sh) + 44
sy0, sy1 = min(p[1] for p in sh) - 18, max(p[1] for p in sh) + 24
d.shape("ellipse", "Desk shadow", x=round(sx0), y=round(sy0),
        width=round(sx1 - sx0), height=round(sy1 - sy0),
        fill=rad((0, "#030608", 66), (0.6, "#030608", 26), (1, "#030608", 0)),
        stroke=NONE)

# --- geometry (inches): a compact upright captain's desk ---------------------------
X0, X1 = -11.0, 11.0
Z0, Z1 = -10.0, 10.0
BODY0, BODY1 = 2.0, 28.0          # carcass
DRX0, DRX1 = 4.0, X1              # right drawer column inside the body
SLOPE_F, SLOPE_B = 27.5, 31.5     # writing slope front/back heights
PY0, PY1, PZ0, PZ1 = 30.0, 40.5, 2.0, 10.0   # piano-top superstructure

# bun feet
for i, (fx, fz) in enumerate([(-9, -8), (9, -8), (-9, 8), (9, 8)]):
    dot3(f"Bun foot {i+1}", fx, 1.2, fz, 5.5, 4.2,
         fill=rad((0, WALNUT_XL), (1, WALNUT_XD)))

# carcass
prism("Carcass", box(X0, BODY0, Z0, X1, BODY1, Z1), lo=0.08, hi=0.92, ink=2.2)

# knee door: recessed panelled door on the front face, left of the drawer column
door = [(-9, 4.5, Z0 - 0.08), (3, 4.5, Z0 - 0.08), (3, 25.5, Z0 - 0.08), (-9, 25.5, Z0 - 0.08)]
ys = [P(*p)[1] for p in door]
quad3("Knee door", door,
      lin((0, min(ys)), (0, max(ys)), (0, "#6E4020"), (1, "#341A0A")),
      stroke=INK, sw=2.0)
inset = [(-7.5, 6.5, Z0 - 0.12), (1.5, 6.5, Z0 - 0.12), (1.5, 23.5, Z0 - 0.12), (-7.5, 23.5, Z0 - 0.12)]
ys = [P(*p)[1] for p in inset]
quad3("Knee door panel", inset,
      lin((0, min(ys)), (0, max(ys)), (0, "#7E4A28"), (1, "#4A2812")),
      stroke="#241005", sw=1.6)
dot3("Knee door knob", 1.8, 15, Z0 - 0.2, 3, 3,
     fill=rad((0, BRASS_L), (1, BRASS_D)))

# --- right drawer column on the +x face --------------------------------------------
DRAWERS = [(3.5, 8.5), (9.5, 14.5), (15.5, 20.5), (21.5, 26.5)]
for i, (dy0, dy1) in enumerate(DRAWERS):
    face = [(X1 + 0.06, dy0, -8.5), (X1 + 0.06, dy0, 8.5),
            (X1 + 0.06, dy1, 8.5), (X1 + 0.06, dy1, -8.5)]
    ys = [P(*p)[1] for p in face]
    quad3(f"Drawer {i+1}", face,
          lin((0, min(ys)), (0, max(ys)), (0, "#7A4A26"), (1, "#462410")),
          stroke=INK, sw=1.8)
    dot3(f"Drawer {i+1} knob", X1 + 0.25, (dy0 + dy1) / 2, 0, 3.4, 3.4,
         fill=rad((0, BRASS_L), (1, BRASS_D)))

# the drawer of secrets: bottom drawer pulled out 3.2in toward +x, dark cavity behind
sec_y0, sec_y1 = DRAWERS[0]
pull = box(X1, sec_y0 + 0.4, -7.5, X1 + 3.4, sec_y1 - 0.4, 8.0)
prism("Secret drawer", pull, dark="#4A2814", light="#8E5C30", lo=0.18, hi=0.95, ink=1.8)
# cavity shadow on the face where the drawer left
cav = [(X1 + 0.05, sec_y0, -7.2), (X1 + 0.05, sec_y0, 7.6),
       (X1 + 0.05, sec_y1, 7.6), (X1 + 0.05, sec_y1, -7.2)]
quad3("Drawer cavity", cav, "#120702", stroke=NONE)
# a rolled parchment peeking out of the pulled drawer
par = [(X1 + 1.0, sec_y1 - 0.5, -4.5), (X1 + 3.1, sec_y1 - 0.5, -4.5),
       (X1 + 3.1, sec_y1 + 1.6, -4.5), (X1 + 1.0, sec_y1 + 1.6, -4.5)]
ys = [P(*p)[1] for p in par]
quad3("Secret parchment", par,
      lin((0, min(ys)), (0, max(ys)), (0, "#F2E4C0"), (1, "#C4AE84")),
      stroke="#6E5630", sw=1.4)
dot3("Parchment seal", X1 + 2.1, sec_y1 + 0.5, -4.6, 2.6, 2.6,
     fill="#8E2E24", stroke="#3A0E0A")

# --- sloped writing surface: a thin prism tilted about the back ----------------------
slab = [(-11, SLOPE_F - 1.2, Z0), (11, SLOPE_F - 1.2, Z0),
        (11, SLOPE_F, Z0), (-11, SLOPE_F, Z0),
        (-11, SLOPE_B - 1.2, PZ0), (11, SLOPE_B - 1.2, PZ0),
        (11, SLOPE_B, PZ0), (-11, SLOPE_B, PZ0)]
prism("Writing slope", slab, dark=WALNUT_XD, light=WALNUT_XL, lo=0.2, hi=1.02, ink=2.2)
# leather inset on the slope
def on_slope(x, z, dy=0.0):
    """Point resting on the inclined top of the slope."""
    t = (z - Z0) / (PZ0 - Z0)
    return (x, SLOPE_F + (SLOPE_B - SLOPE_F) * t + dy, z)

leath = [on_slope(-9.4, Z0 + 1.2), on_slope(9.4, Z0 + 1.2),
         on_slope(9.4, PZ0 - 0.8), on_slope(-9.4, PZ0 - 0.8)]
ys = [P(*p)[1] for p in leath]
quad3("Leather writing field", leath,
      lin((0, min(ys)), (0, max(ys)), (0, LEATHER_L), (1, LEATHER_D)),
      stroke="#0C1810", sw=1.8)
gilt = [on_slope(-8.4, Z0 + 2.2, 0.02), on_slope(8.4, Z0 + 2.2, 0.02),
        on_slope(8.4, PZ0 - 1.8, 0.02), on_slope(-8.4, PZ0 - 1.8, 0.02)]
quad3("Leather gilt border", gilt, NONE, stroke="#C89A4E", sw=1.6, opacity=70)
# a letter lying on the leather + brass inkwell
pap = [on_slope(-6, -7.4, 0.06), on_slope(1.5, -7.4, 0.06),
       on_slope(1.5, -1.8, 0.06), on_slope(-6, -1.8, 0.06)]
ys = [P(*p)[1] for p in pap]
quad3("Letter", pap,
      lin((0, min(ys)), (0, max(ys)), (0, "#F4ECDA"), (1, "#D8CBAE")),
      stroke="#8A7A5E", sw=1.3)
dot3("Inkwell", 4.6, 0, -4.5, 4.6, 3.8,
     fill=rad((0, "#F6E2AC"), (0.6, "#C89A4E"), (1, "#5E3E14")))
# inkwell sits on the slope — reproject correctly
dot3("Inkwell top", *on_slope(4.6, -4.5, 0.4), 3.0, 2.4,
     fill="#241305", stroke="#C89A4E", strokeWidth=1.2)

# --- piano-top superstructure at the back --------------------------------------------
prism("Piano-top body", box(X0, PY0, PZ0, X1, PY1, PZ1), lo=0.10, hi=0.98, ink=2.2)
# crown moulding
prism("Crown moulding", box(X0 - 0.6, PY1, PZ0 - 0.6, X1 + 0.6, PY1 + 1.3, PZ1 + 0.6),
      dark=WALNUT_XD, light=WALNUT_XL, lo=0.25, hi=1.05, ink=2.0)
# lid seam + brass hinges: the piano-top lid lift line
seg = "M%.1f,%.1f L%.1f,%.1f"
a, b = P(X0 + 0.6, PY1 - 1.4, PZ0 - 0.05), P(X1 - 0.6, PY1 - 1.4, PZ0 - 0.05)
d.path(seg % (a + b), "Lid seam", fill=NONE, stroke="#120702", strokeWidth=2.2, opacity=75)
for i, hx_ in enumerate((-8, 8)):
    hg = [(hx_ - 1.2, PY1 - 0.9, PZ0 - 0.08), (hx_ + 1.2, PY1 - 0.9, PZ0 - 0.08),
          (hx_ + 1.2, PY1 + 0.3, PZ0 - 0.08), (hx_ - 1.2, PY1 + 0.3, PZ0 - 0.08)]
    ys = [P(*p)[1] for p in hg]
    quad3(f"Hinge {i+1}", hg,
          lin((0, min(ys)), (0, max(ys)), (0, BRASS_L), (1, BRASS_D)),
          stroke="#3A2408", sw=1.2)
# gallery finials on the crown corners
for i, (fx, fz) in enumerate([(X0 - 0.2, PZ0 - 0.2), (X1 + 0.2, PZ0 - 0.2), (X0 - 0.2, PZ1 + 0.2)]):
    prism(f"Finial {i+1}", box(fx - 0.45, PY1 + 1.3, fz - 0.45, fx + 0.45, PY1 + 3.2, fz + 0.45),
          dark=WALNUT_XD, light=WALNUT_XL, lo=0.3, hi=1.0, ink=1.2)
    dot3(f"Finial {i+1} ball", fx, PY1 + 3.6, fz, 2.2, 2.2,
         fill=rad((0, WALNUT_XL), (1, WALNUT_XD)))
# pigeonhole rail on the superstructure front face
rail = [(X0 + 1.0, PY0 + 0.6, PZ0 - 0.06), (X1 - 1.0, PY0 + 0.6, PZ0 - 0.06),
        (X1 - 1.0, PY0 + 2.6, PZ0 - 0.06), (X0 + 1.0, PY0 + 2.6, PZ0 - 0.06)]
ys = [P(*p)[1] for p in rail]
quad3("Pigeonhole rail", rail,
      lin((0, min(ys)), (0, max(ys)), (0, "#4A2812"), (1, "#2A1408")),
      stroke=INK, sw=1.5)
for i in range(3):
    seg3_x = X0 + 1.0 + (X1 - 1.0 - X0) * (i + 1) / 4
    a, b = P(seg3_x, PY0 + 0.6, PZ0 - 0.08), P(seg3_x, PY0 + 2.6, PZ0 - 0.08)
    d.path(f"M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}", f"Pigeon divider {i+1}",
           fill=NONE, stroke="#241005", strokeWidth=1.4, opacity=70)

# --- brass cabin lamp on the crown, left side ----------------------------------------
lcx, lcy = P(-8.0, PY1 + 1.4, 5.0)
d.shape("ellipse", "Lamp glow", x=round(lcx - 46), y=round(lcy - 60), width=92, height=92,
        fill=rad((0, "#F0BE7A", 30), (0.6, "#C08A48", 10), (1, "#C08A48", 0)), stroke=NONE)
d.shape("ellipse", "Lamp base", x=round(lcx - 10), y=round(lcy - 4), width=20, height=8,
        fill=rad((0, BRASS_L), (1, BRASS_D)), stroke=INK, strokeWidth=1.4)
d.path(f"M{lcx - 7:.1f},{lcy - 2:.1f} L{lcx - 5:.1f},{lcy - 26:.1f} "
       f"C{lcx - 5:.1f},{lcy - 30:.1f} {lcx + 5:.1f},{lcy - 30:.1f} {lcx + 5:.1f},{lcy - 26:.1f} "
       f"L{lcx + 7:.1f},{lcy - 2:.1f} Z",
       "Lamp chimney", fill=lin((lcx - 7, lcy - 30), (lcx + 7, lcy - 2),
       (0, "#F6E2AC", 0.55), (0.5, "#F0BE7A", 0.75), (1, "#8A6428", 0.6)),
       stroke="#D9AE5E", strokeWidth=1.6, join="round")
d.shape("ellipse", "Lamp flame", x=round(lcx - 3), y=round(lcy - 22), width=6, height=11,
        fill=rad((0, "#FFF2C8"), (0.6, "#F0BE5A"), (1, "#C87828")), stroke=NONE)

# --- extent check ---------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("davenport extent: farthest point %.0f from centre (rim %d)" % (far, PR))
assert far < PR - 24, far


# --- caption ---------------------------------------------------------------------------
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
               color="#EEEAE0", justify="center")
    m = d.text(mats, "Materials", x=500, y=970, size=22, font="Virelai Sans",
               color="#A8C2CC", justify="center")
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


caption("DAVENPORT DESK", "WALNUT · LEATHER · BRASS")
d.finish("davenport-desk-V1R00")
