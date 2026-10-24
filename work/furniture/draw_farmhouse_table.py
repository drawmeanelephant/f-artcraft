#!/usr/bin/env python3
"""Farmhouse table — field plate V1R00. Three-quarter view from the front
right: a scrubbed-pine plank top on thick square legs, an H-stretcher low
between them, pegged joints and a pale worn surface. Harvest props on the
top: a squat pumpkin, a stoneware crock fanned with wheat stalks, two loose
stalks lying flat. Pine plate, harvest mood — a warm amber field.
1000x1000. Modelled in inches (x right, y up, +z back), projected with a
fixed yaw + pitch; carcass parts are 8-corner prisms culled by view normal
and shaded by lamp light.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Farmhouse Table — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#241610"   # warm dark, not black
EXTENT = []


def stops(*pairs):
    out = []
    for p in pairs:
        s = {"offset": p[0], "color": p[1]}
        if len(p) > 2 and p[2] is not None:
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
YAW, PITCH = math.radians(30), math.radians(26)
S, OX, OY = 9.1, 502.0, 724.0
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
    return [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
            (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]


FACES = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4),
         (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
TO_VIEWER = (SY * CP, SP, -CY * CP)          # normals facing this draw
LIGHT = (-0.35, 0.86, -0.30)                  # lamp overhead, slightly left/front
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


def prism(name, corners, ramp=("#5E3A16", "#C8924E"), lo=0.06, hi=0.94, sw=1.8):
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
        g = lin((0, y0), (0, y1), (0, shade(ramp[0], ramp[1], min(1, b + 0.12))),
                                 (1, shade(ramp[0], ramp[1], b)))
        d.path(poly(pts), name, fill=g, stroke=INK, strokeWidth=sw, join="round")


def flat_ellipse(cx, y, cz, r, label, **kw):
    """Ellipse lying on the horizontal plane y: a circle of model radius r."""
    ex, ey = P(cx, y, cz)
    rx, ry = S * r, S * r * SP
    d.shape("ellipse", label, x=round(ex - rx, 1), y=round(ey - ry, 1),
            width=round(rx * 2, 1), height=round(ry * 2, 1), **kw)


# --- backdrop + plate ---------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#1A120A"), (1, "#080503")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#C89A50", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#5E4622"), (0.55, "#382812"), (1, "#170E05")),
        stroke="#120D06", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E0C48E", strokeWidth=3, opacity=24)

# late-afternoon glow high on the disc: the harvest light
d.shape("ellipse", "Field glow", x=270, y=130, width=460, height=330,
        fill=rad((0, "#FFC878", 0.16), (0.55, "#C88A3C", 0.06), (1, "#C88A3C", 0)),
        stroke=NONE)

# a drying sheaf hung in the empty upper disc: cord fading out toward the rim
d.path("M646,104 L649,104 L648.2,212 L646.8,212 Z", "Sheaf cord",
       fill=lin((0, 104), (0, 212), (0, "#8A6A3A", 0), (0.5, "#8A6A3A", 0.55),
                (1, "#8A6A3A", 0.8)), stroke=NONE)
d.shape("ellipse", "Sheaf knot", x=640, y=208, width=15, height=10,
        fill="#7A5622", stroke=INK, strokeWidth=1.2)
# the hung bunch: stems up to the knot, heads drooping below
for i, (dx_, spread) in enumerate(((-26, -34), (-14, -18), (0, 0), (14, 18), (26, 34))):
    bx_, by_ = 647.5 + dx_ * 0.3, 236.0
    tipx, tipy = 647.5 + spread, 236 + abs(spread) * 0.35 + 46
    EXTENT.append((tipx, tipy))
    d.path(f"M647.5,214 Q{bx_:.1f},{by_:.1f} {tipx:.1f},{tipy:.1f}",
           f"Sheaf stem {i+1}", fill=NONE, stroke="#B8923E", strokeWidth=2.8, cap="round")
    ang = math.atan2(tipy - by_, tipx - bx_)
    hx_, hy_ = tipx + math.cos(ang) * 11, tipy + math.sin(ang) * 11
    EXTENT.append((hx_, hy_))
    d.path(f"M{tipx:.1f},{tipy:.1f} L{hx_:.1f},{hy_:.1f}", f"Sheaf head {i+1}",
           fill=NONE, stroke="#CBA84E", strokeWidth=5.0, cap="round")
    for j, sgn in enumerate((-1, 1)):
        ax_, ay_ = hx_ + math.cos(ang + sgn * 0.6) * 7, hy_ + math.sin(ang + sgn * 0.6) * 7
        EXTENT.append((ax_, ay_))
        d.path(f"M{hx_:.1f},{hy_:.1f} L{ax_:.1f},{ay_:.1f}", f"Sheaf awn {i+1}{j}",
               fill=NONE, stroke="#CBA84E", strokeWidth=1.6, cap="round", opacity=70)

# --- floor: dark boards closing on the disc arc ---------------------------------------
FYB = 752
hw = math.sqrt(PR ** 2 - (FYB - PCY) ** 2)
d.path(f"M{PCX - hw:.1f},{FYB} L{PCX + hw:.1f},{FYB} A420,420 0 0 0 {PCX - hw:.1f},{FYB} Z",
       "Floor", fill=lin((0, FYB), (0, 880), (0, "#3E3018", 0.5), (0.5, "#241A0C", 0.7),
                         (1, "#0F0904", 0.9)), stroke=NONE)
for i, yb in enumerate([784, 816, 848]):
    h = math.sqrt(PR ** 2 - (yb - PCY) ** 2) - 4
    d.path(f"M{PCX - h:.1f},{yb} L{PCX + h:.1f},{yb}", f"Board seam {i+1}",
           fill=NONE, stroke="#5A421E", strokeWidth=2, opacity=26)

# --- grounding shadow under the table ---------------------------------------------------
fx0, fy0 = P(-26, 0, -11)
fx1, fy1 = P(26, 0, 11)
sx0, sx1 = min(fx0, fx1) - 30, max(fx0, fx1) + 30
sy0, sy1 = min(fy0, fy1) - 16, max(fy0, fy1) + 20
d.shape("ellipse", "Table shadow", x=round(sx0), y=round(sy0),
        width=round(sx1 - sx0), height=round(sy1 - sy0),
        fill=rad((0, "#040302", 0.7), (0.6, "#040302", 0.3), (1, "#040302", 0)),
        stroke=NONE)

# --- table geometry (inches) ---------------------------------------------------------------
PINE = ("#5E3A16", "#C8924E")
PINE_HI = ("#6E4820", "#D8A860")
SCRUB = ("#7A5426", "#E4C084")          # bleached, scrubbed top
DARK_OAK = ("#3A2410", "#7A5228")

def leg(sx, sz, tag):
    lx, lz = sx * 21.5, sz * 7.5
    corners = [(lx - 2.3, 0, lz - 2.3), (lx + 2.3, 0, lz - 2.3),
               (lx + 2.3, 0, lz + 2.3), (lx - 2.3, 0, lz + 2.3),
               (lx - 2.9, 24, lz - 2.9), (lx + 2.9, 24, lz - 2.9),
               (lx + 2.9, 24, lz + 2.9), (lx - 2.9, 24, lz + 2.9)]
    prism(f"Leg {tag}", corners, ramp=PINE, lo=0.04, hi=0.88)
    # peg hole on the outer face, low
    px_, py_ = P(lx + sx * 2.9, 20.5, lz)
    EXTENT.append((px_, py_))
    d.shape("ellipse", f"Leg peg {tag}", x=round(px_ - 2.4, 1), y=round(py_ - 2.4, 1),
            width=4.8, height=4.8, fill="#2A1808", stroke=NONE)


# far legs, then the H-stretcher (it stands behind the near pair), then near legs
leg(-1, 1, "far L")
leg(1, 1, "far R")
prism("Stretcher end L", box(-23.8, 4.5, -9.8, -19.2, 8.0, 9.8), ramp=PINE, lo=0.03, hi=0.7)
prism("Stretcher end R", box(19.2, 4.5, -9.8, 23.8, 8.0, 9.8), ramp=PINE, lo=0.03, hi=0.7)
prism("Stretcher long", box(-20.5, 5.2, -1.6, 20.5, 8.6, 1.6), ramp=PINE_HI, lo=0.05, hi=0.8)
leg(-1, -1, "near L")
leg(1, -1, "near R")

# apron: the skirt under the top, inset from the edges
prism("Apron far", box(-21.5, 21.0, 5.6, 21.5, 27.0, 9.6), ramp=PINE, lo=0.03, hi=0.72)
prism("Apron L", box(-24.4, 21.0, -7.5, -19.6, 27.0, 7.5), ramp=PINE, lo=0.03, hi=0.72)
prism("Apron R", box(19.6, 21.0, -7.5, 24.4, 27.0, 7.5), ramp=PINE, lo=0.03, hi=0.72)
prism("Apron near", box(-21.5, 21.0, -9.6, 21.5, 27.0, -5.6), ramp=PINE, lo=0.03, hi=0.72)

# top slab: 3in thick, proud of the apron on all sides
prism("Top slab", box(-27, 27, -12, 27, 30, 12), ramp=SCRUB, lo=0.12, hi=1.0, sw=2.2)

# plank seams on the scrubbed top: three boards, gaps running lengthwise
for i, zs in enumerate((-6.0, 0.0, 6.0)):
    a, b = P(-26.2, 30.05, zs), P(26.2, 30.05, zs)
    d.path(f"M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}", f"Plank seam {i+1}",
           fill=NONE, stroke="#4A2C10", strokeWidth=2.0, opacity=55)

# scrub marks: faint pale strokes dragged along the boards
for i, (zs, x0, x1) in enumerate([(-9, -20, -4), (-2.5, 2, 22), (3.2, -24, -10),
                                  (8.8, 6, 18), (-4.6, 8, 24)]):
    a, b = P(x0, 30.06, zs), P(x1, 30.06, zs + 0.5)
    d.path(f"M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}", f"Scrub {i+1}",
           fill=NONE, stroke="#F4DCA8", strokeWidth=1.8, opacity=22, cap="round")

# a couple of knots in the pine
for i, (kx, kz) in enumerate(((-14, -3.2), (10, 7.6))):
    flat_ellipse(kx, 30.06, kz, 0.85, f"Knot {i+1}", fill="#4A2C10",
                 stroke="#6E481E", strokeWidth=1.0, opacity=80)

# oak pegs over each leg on the top face
for i, (px_, pz_) in enumerate(((-21.5, -7.5), (21.5, -7.5), (-21.5, 7.5), (21.5, 7.5))):
    flat_ellipse(px_, 30.07, pz_, 0.62, f"Top peg {i+1}", fill="#2A1808",
                 stroke="#0E0703", strokeWidth=0.8)

# --- props on the top ----------------------------------------------------------------------
TOP = 30.0

# pumpkin at the near-right end: ribbed squat sphere + stem
pkx, pkz = 15.5, -3.5
flat_ellipse(pkx + 0.7, TOP + 0.02, pkz + 0.6, 4.6, "Pumpkin shadow",
             fill=rad((0, "#0A0603", 0.5), (1, "#0A0603", 0)), stroke=NONE)
pkc = P(pkx, TOP + 3.6, pkz)
pkrx, pkry = S * 5.2, S * 3.9
d.shape("ellipse", "Pumpkin body", x=round(pkc[0] - pkrx, 1), y=round(pkc[1] - pkry, 1),
        width=round(pkrx * 2, 1), height=round(pkry * 2, 1),
        fill=rad((0, "#E89A48", None), (0.55, "#C06A1E", None), (1, "#6E320C", None)),
        stroke=INK, strokeWidth=1.6)
# ribs: arcs pulled from crown to base
for i, rx in enumerate((0.30, 0.58, 0.84)):
    for sgn, tag in ((-1, "L"), (1, "R")):
        x0 = pkc[0] + sgn * pkrx * 0.12
        x1 = pkc[0] + sgn * pkrx * rx
        d.path(f"M{x0:.1f},{pkc[1] - pkry * 0.86:.1f} "
               f"Q{x1 + sgn * pkrx * 0.10:.1f},{pkc[1]:.1f} "
               f"{pkc[0] + sgn * pkrx * 0.16:.1f},{pkc[1] + pkry * 0.80:.1f}",
               f"Pumpkin rib {i}{tag}", fill=NONE, stroke="#7E3A0E",
               strokeWidth=1.6, opacity=45)
# stem
d.path(f"M{pkc[0] - 3:.1f},{pkc[1] - pkry * 0.92:.1f} "
       f"L{pkc[0] + 1:.1f},{pkc[1] - pkry - 10:.1f} "
       f"L{pkc[0] + 7:.1f},{pkc[1] - pkry - 8:.1f} "
       f"L{pkc[0] + 4:.1f},{pkc[1] - pkry * 0.88:.1f} Z",
       "Pumpkin stem", fill=lin((pkc[0], pkc[1] - pkry - 10), (pkc[0], pkc[1] - pkry * 0.8),
       (0, "#8A7A3A", None), (1, "#4A3E18", None)), stroke=INK, strokeWidth=1.2, join="round")

# stoneware crock at the far-left end holding a fan of wheat: slight taper
ckx, ckz = -15.0, 4.5
flat_ellipse(ckx + 0.5, TOP + 0.02, ckz + 0.5, 3.6, "Crock shadow",
             fill=rad((0, "#0A0603", 0.45), (1, "#0A0603", 0)), stroke=NONE)
crock = [(ckx - 3.2, TOP, ckz - 3.2), (ckx + 3.2, TOP, ckz - 3.2),
         (ckx + 3.2, TOP, ckz + 3.2), (ckx - 3.2, TOP, ckz + 3.2),
         (ckx - 2.6, TOP + 6.4, ckz - 2.6), (ckx + 2.6, TOP + 6.4, ckz - 2.6),
         (ckx + 2.6, TOP + 6.4, ckz + 2.6), (ckx - 2.6, TOP + 6.4, ckz + 2.6)]
prism("Crock body", crock, ramp=("#4E3520", "#B08A5C"), lo=0.15, hi=0.95, sw=1.6)
flat_ellipse(ckx, TOP + 6.4, ckz, 2.6, "Crock mouth",
             fill=rad((0, "#14100A", None), (0.8, "#241C12", None), (1, "#4E3520", None)),
             stroke="#2A2018", strokeWidth=1.2)
# glaze band around the belly
gl0, gl1 = P(ckx - 3.0, TOP + 2.2, ckz - 3.0), P(ckx + 3.0, TOP + 2.2, ckz - 3.0)
d.path(f"M{gl0[0]:.1f},{gl0[1]:.1f} L{gl1[0]:.1f},{gl1[1]:.1f}", "Crock glaze line",
       fill=NONE, stroke="#3A2A18", strokeWidth=2.0, opacity=50)

# wheat stalks fanning from the crock mouth
WHEAT_S = "#C8A44A"
WHEAT_H = "#DDBB66"
mouth = P(ckx, TOP + 6.6, ckz)
for i, (dx_, dy_, lean) in enumerate([(-30, -95, -14), (-16, -108, -6), (0, -114, 0),
                                      (16, -106, 7), (30, -92, 15)]):
    tip = (mouth[0] + dx_ + lean * 0.4, mouth[1] + dy_)
    mid = (mouth[0] + dx_ * 0.4, mouth[1] + dy_ * 0.6)
    EXTENT.append(tip)
    d.path(f"M{mouth[0]:.1f},{mouth[1]:.1f} Q{mid[0]:.1f},{mid[1]:.1f} {tip[0]:.1f},{tip[1]:.1f}",
           f"Wheat stem {i+1}", fill=NONE, stroke=WHEAT_S, strokeWidth=2.6, cap="round")
    # grain head: a slim ear with whisker awns along it
    ang = math.atan2(tip[1] - mid[1], tip[0] - mid[0])
    hx_, hy_ = tip[0] + math.cos(ang) * 14, tip[1] + math.sin(ang) * 14
    EXTENT.append((hx_, hy_))
    d.path(f"M{tip[0]:.1f},{tip[1]:.1f} L{hx_:.1f},{hy_:.1f}", f"Wheat head {i+1}",
           fill=NONE, stroke=WHEAT_H, strokeWidth=4.4, cap="round")
    for j, t in enumerate((0.35, 0.6, 0.85)):
        wx = tip[0] + math.cos(ang) * 14 * t
        wy = tip[1] + math.sin(ang) * 14 * t
        for sgn in (-1, 1):
            ax_, ay_ = wx + math.cos(ang + sgn * 0.85) * 6, wy + math.sin(ang + sgn * 0.85) * 6
            EXTENT.append((ax_, ay_))
            d.path(f"M{wx:.1f},{wy:.1f} L{ax_:.1f},{ay_:.1f}", f"Wheat awn {i+1}{j}{sgn}",
                   fill=NONE, stroke=WHEAT_H, strokeWidth=1.5, cap="round", opacity=65)

# two loose stalks lying flat on the top between the props
for i, ((x0, z0), (x1, z1)) in enumerate([((-6, -7.5), (7, -9.0)), ((-3, -6.0), (9.5, -4.2))]):
    a, b = P(x0, TOP + 0.15, z0), P(x1, TOP + 0.15, z1)
    d.path(f"M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}", f"Loose stem {i+1}",
           fill=NONE, stroke=WHEAT_S, strokeWidth=2.6, cap="round")
    ux, uy = (b[0] - a[0]), (b[1] - a[1])
    ul = math.hypot(ux, uy)
    ux, uy = ux / ul, uy / ul
    hx_, hy_ = b[0] + ux * 11, b[1] + uy * 11
    EXTENT.append((hx_, hy_))
    d.path(f"M{b[0]:.1f},{b[1]:.1f} L{hx_:.1f},{hy_:.1f}", f"Loose head {i+1}",
           fill=NONE, stroke=WHEAT_H, strokeWidth=4.6, cap="round")
    for sgn in (-1, 1):
        ax_, ay_ = hx_ + math.cos(math.atan2(uy, ux) + sgn * 0.8) * 5.5, \
                   hy_ + math.sin(math.atan2(uy, ux) + sgn * 0.8) * 5.5
        EXTENT.append((ax_, ay_))
        d.path(f"M{hx_:.1f},{hy_:.1f} L{ax_:.1f},{ay_:.1f}", f"Loose awn {i+1}{sgn}",
               fill=NONE, stroke=WHEAT_H, strokeWidth=1.4, cap="round", opacity=60)

# warm rim light along the near top edge
ra, rb = P(-26.5, 30.1, -12), P(26.5, 30.1, -12)
d.path(f"M{ra[0]:.1f},{ra[1]:.1f} L{rb[0]:.1f},{rb[1]:.1f}", "Top rim light",
       fill=NONE, stroke="#FFCE8A", strokeWidth=2.4, opacity=38, cap="round")

# --- extent check ---------------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("table extent: farthest point %.0f from centre (rim %d)" % (far, PR))
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
               color="#F0E6CE", justify="center")
    m = d.text(mats, "Materials", x=500, y=970, size=22, font="Virelai Sans",
               color="#C4B091", justify="center")
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


caption("FARMHOUSE TABLE", "PINE · OAK PEGS · BEESWAX")
d.finish("farmhouse-table-V1R00")
