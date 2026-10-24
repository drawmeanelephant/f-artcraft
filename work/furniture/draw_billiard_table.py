#!/usr/bin/env python3
"""Billiard table — field plate V1R00. Three-quarter view from the front
right under a hanging three-shade lamp: a slate-bed table in walnut with
green baize, six pocket openings, ivory diamond sights, a rack of balls,
a resting cue and a blue chalk cube on the near rail. Baize plate,
chalk-dust mood. 1000x1000. Modelled in inches (x right, y up, +z back),
projected with a fixed yaw + pitch; carcass parts are 8-corner prisms
culled by view normal and shaded by lamp light.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Billiard Table — Field Plate", 1000, 1000)

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
YAW, PITCH = math.radians(30), math.radians(27)
S, OX, OY = 5.95, 502.0, 734.0
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


def prism(name, corners, ramp=("#241408", "#7A4E26"), lo=0.06, hi=0.94, sw=1.8):
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
        fill=lin((0, 0), (0, 1000), (0, "#10161A"), (1, "#060809")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#9A8C60", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#55503A"), (0.55, "#38341F"), (1, "#191508")),
        stroke="#12100A", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8C8A0", strokeWidth=3, opacity=24)

# --- hanging lamp: cone first, then the fixture -------------------------------------
d.path("M420,222 L580,222 L690,690 L310,690 Z", "Lamp cone",
       fill=lin((500, 222), (500, 690), (0, "#FFCE8A", 0.16), (0.6, "#FFB464", 0.05),
                (1, "#FFB464", 0)), stroke=NONE)
d.shape("ellipse", "Lamp bloom", x=290, y=240, width=420, height=300,
        fill=rad((0, "#FFBE70", 0.14), (0.6, "#C88A44", 0.05), (1, "#C88A44", 0)),
        stroke=NONE)
# suspension rod fading into the dark above the disc's inner ring
d.path("M497.5,196 L502.5,196 L502.5,110 L497.5,110 Z", "Lamp rod",
       fill=lin((0, 196), (0, 110), (0, "#8A6A3A", 0.8), (1, "#8A6A3A", 0)),
       stroke=NONE)
d.path("M412,200 L588,200 L588,206 L412,206 Z", "Lamp bar",
       fill=lin((412, 0), (588, 0), (0, "#5A4020", None), (0.5, "#B08A4C", None),
                (1, "#4A3418", None)), stroke=INK, strokeWidth=1.6)
for i, sx in enumerate((438, 500, 562)):
    # conical metal shade: dark bronze outside, hot underside
    d.path(f"M{sx - 9},{206} L{sx + 9},{206} L{sx + 27},{240} L{sx - 27},{240} Z",
           f"Shade {i+1}", fill=lin((sx, 206), (sx, 240),
           (0, "#3A5A40", None), (0.7, "#22402A", None), (1, "#14251A", None)),
           stroke=INK, strokeWidth=1.6, join="round")
    d.shape("ellipse", f"Shade mouth {i+1}", x=sx - 27, y=236, width=54, height=12,
            fill=rad((0, "#FFE2A8", None), (0.55, "#D89A4A", None), (1, "#7A4A1E", None)),
            stroke=NONE)

# --- floor: dark boards closing on the disc arc ---------------------------------------
FYB = 752
hw = math.sqrt(PR ** 2 - (FYB - PCY) ** 2)
d.path(f"M{PCX - hw:.1f},{FYB} L{PCX + hw:.1f},{FYB} A420,420 0 0 0 {PCX - hw:.1f},{FYB} Z",
       "Floor", fill=lin((0, FYB), (0, 880), (0, "#3C3423", 0.5), (0.5, "#251C0E", 0.7),
                         (1, "#100B05", 0.9)), stroke=NONE)
for i, yb in enumerate([784, 816, 848]):
    h = math.sqrt(PR ** 2 - (yb - PCY) ** 2) - 4
    d.path(f"M{PCX - h:.1f},{yb} L{PCX + h:.1f},{yb}", f"Board seam {i+1}",
           fill=NONE, stroke="#5A4526", strokeWidth=2, opacity=26)

# --- grounding shadow under the table ---------------------------------------------------
fx0, fy0 = P(-40, 0, -18)
fx1, fy1 = P(40, 0, 18)
sx0, sx1 = min(fx0, fx1) - 30, max(fx0, fx1) + 30
sy0, sy1 = min(fy0, fy1) - 16, max(fy0, fy1) + 20
d.shape("ellipse", "Table shadow", x=round(sx0), y=round(sy0),
        width=round(sx1 - sx0), height=round(sy1 - sy0),
        fill=rad((0, "#040302", 0.7), (0.6, "#040302", 0.3), (1, "#040302", 0)),
        stroke=NONE)

# --- table geometry (inches) ---------------------------------------------------------------
# legs: 4 tapered squares, far ones first
WALNUT = ("#1E1008", "#6E4525")
WALNUT_HI = ("#2A1810", "#8A5E35")
LEATHER = ("#120A06", "#3A2314")
for sx, sz, tag in ((-1, 1, "far L"), (1, 1, "far R"), (-1, -1, "near L"), (1, -1, "near R")):
    lx, lz = sx * 36, sz * 15
    # tapered leg: 5.6in at the apron down to 4.2in at the floor
    corners = [(lx - 2.1, 0, lz - 2.1), (lx + 2.1, 0, lz - 2.1),
               (lx + 2.1, 0, lz + 2.1), (lx - 2.1, 0, lz + 2.1),
               (lx - 2.8, 21.5, lz - 2.8), (lx + 2.8, 21.5, lz - 2.8),
               (lx + 2.8, 21.5, lz + 2.8), (lx - 2.8, 21.5, lz + 2.8)]
    prism(f"Leg {tag}", corners, ramp=WALNUT, lo=0.04, hi=0.85)
    # collar block at the top of the leg
    prism(f"Leg collar {tag}", box(lx - 3.2, 21.5, lz - 3.2, lx + 3.2, 24.5, lz + 3.2),
          ramp=WALNUT_HI, lo=0.05, hi=0.9)
    # foot pad
    prism(f"Foot {tag}", box(lx - 2.5, 0, lz - 2.5, lx + 2.5, 2.0, lz + 2.5),
          ramp=WALNUT, lo=0.03, hi=0.7)

# leather drop-pocket baskets hanging below the four corners
for sx, sz, tag in ((-1, 1, "far L"), (1, 1, "far R"), (-1, -1, "near L"), (1, -1, "near R")):
    bx, bz = sx * 41, sz * 19.6
    prism(f"Basket {tag}", box(bx - 4.8, 14.5, bz - 4.4, bx + 4.8, 27.5, bz + 4.4),
          ramp=LEATHER, lo=0.05, hi=0.8)

# aprons: the deep skirt under the rails
prism("Apron near", box(-41, 22.5, -22, 41, 30.2, -16.8), ramp=WALNUT, lo=0.03, hi=0.7)
prism("Apron far", box(-41, 22.5, 16.8, 41, 30.2, 22), ramp=WALNUT, lo=0.03, hi=0.7)
prism("Apron L", box(-45.2, 22.5, -16.8, -38.6, 30.2, 16.8), ramp=WALNUT, lo=0.03, hi=0.7)
prism("Apron R", box(38.6, 22.5, -16.8, 45.2, 30.2, 16.8), ramp=WALNUT, lo=0.03, hi=0.7)
# a recessed panel line on the near apron for cabinetry read
pa, pb = P(-36, 26.5, -19.9), P(36, 26.5, -19.9)
d.path(f"M{pa[0]:.1f},{pa[1]:.1f} L{pb[0]:.1f},{pb[1]:.1f}", "Apron panel line",
       fill=NONE, stroke="#0E0703", strokeWidth=2.2, opacity=55)

# rails: four slabs of walnut forming the frame, tops at y=32.5
prism("Rail near", box(-46, 30, -24, 46, 32.5, -16), ramp=WALNUT_HI, lo=0.1, hi=1.0)
prism("Rail far", box(-46, 30, 16, 46, 32.5, 24), ramp=WALNUT_HI, lo=0.1, hi=1.0)
prism("Rail L", box(-46, 30, -16, -38, 32.5, 16), ramp=WALNUT_HI, lo=0.1, hi=1.0)
prism("Rail R", box(38, 30, -16, 46, 32.5, 16), ramp=WALNUT_HI, lo=0.1, hi=1.0)

# baize bed: the playing surface, inset from the rails
bed = [P(-38.5, 30.3, -15.5), P(38.5, 30.3, -15.5), P(38.5, 30.3, 15.5), P(-38.5, 30.3, 15.5)]
by0, by1 = min(p[1] for p in bed), max(p[1] for p in bed)
d.path(poly(bed), "Baize bed", fill=lin((0, by0), (0, by1),
       (0, "#3E7A46", None), (0.55, "#2E5E36", None), (1, "#1E4226", None)),
       stroke="#0E2412", strokeWidth=2.4, join="round")
# lamp pool on the cloth
d.shape("ellipse", "Light on cloth", x=round(P(-6, 30.3, -2)[0] - 150),
        y=round(P(-6, 30.3, -2)[1] - 60), width=300, height=120,
        fill=rad((0, "#7AB06A", 0.30), (0.6, "#5A9455", 0.12), (1, "#5A9455", 0)),
        stroke=NONE)

# cushions: baize-covered bands sloping from the rail inner edge down to the bed
CUSH = ("#1E4226", "#4E8A55")
for tag, quad in (
        ("near", [(-38, 32.1, -16), (38, 32.1, -16), (36.5, 30.5, -13.4), (-36.5, 30.5, -13.4)]),
        ("far", [(-38, 32.1, 16), (38, 32.1, 16), (36.5, 30.5, 13.4), (-36.5, 30.5, 13.4)]),
        ("L", [(-38, 32.1, -16), (-38, 32.1, 16), (-35.4, 30.5, 14), (-35.4, 30.5, -14)]),
        ("R", [(38, 32.1, -16), (38, 32.1, 16), (35.4, 30.5, 14), (35.4, 30.5, -14)])):
    pts = [P(*p) for p in quad]
    cy0, cy1 = min(p[1] for p in pts), max(p[1] for p in pts)
    d.path(poly(pts), f"Cushion {tag}", fill=lin((0, cy0), (0, cy1),
           (0, CUSH[1], None), (1, CUSH[0], None)), stroke="#0E2412",
           strokeWidth=2.0, join="round")
    # nose line where the cushion meets the bed
    na, nb = P(*quad[2]), P(*quad[3])
    d.path(f"M{na[0]:.1f},{na[1]:.1f} L{nb[0]:.1f},{nb[1]:.1f}", f"Cushion nose {tag}",
           fill=NONE, stroke="#A8D898", strokeWidth=1.8, opacity=35)

# ivory diamond sights on the rail tops
for cx_, cz_ in ((-31, -20), (-17, -20), (17, -20), (31, -20),
                 (-31, 20), (-17, 20), (17, 20), (31, 20),
                 (-42, -7), (-42, 7), (42, -7), (42, 7)):
    a, b_, c_, e_ = (P(cx_, 32.6, cz_ - 1.6), P(cx_ + 1.6, 32.6, cz_),
                     P(cx_, 32.6, cz_ + 1.6), P(cx_ - 1.6, 32.6, cz_))
    d.path(poly([a, b_, c_, e_]), f"Sight {cx_} {cz_}", fill="#E8DCC2",
           stroke="#8A7A5A", strokeWidth=0.8, opacity=90)

# six pocket openings: dark mouth on the rail plane + a deeper throat
POCKETS = [(-39.5, -17.5), (39.5, -17.5), (-39.5, 17.5), (39.5, 17.5),
           (0, -17.8), (0, 17.8)]
for i, (px_, pz_) in enumerate(POCKETS):
    flat_ellipse(px_, 30.9, pz_, 4.6, f"Pocket mouth {i+1}",
                 fill=rad((0, "#050302", None), (0.8, "#0A0604", None),
                          (1, "#1E1208", None)), stroke="#3A2812", strokeWidth=1.4)
    flat_ellipse(px_, 30.7, pz_, 2.6, f"Pocket throat {i+1}", fill="#030201",
                 stroke=NONE)

# --- props on the bed -------------------------------------------------------------------
# cue stick lying across the near-left of the bed, butt toward the viewer
ca, cb = P(-34, 30.9, 9), P(4, 30.9, -7)
cdx, cdy = cb[0] - ca[0], cb[1] - ca[1]
cl = math.hypot(cdx, cdy)
ux, uy = cdx / cl, cdy / cl
nx_, ny_ = -uy, ux
cue = [(ca[0] + nx_ * 4.4, ca[1] + ny_ * 4.4), (ca[0] - nx_ * 4.4, ca[1] - ny_ * 4.4),
       (cb[0] - nx_ * 2.0, cb[1] - ny_ * 2.0), (cb[0] + nx_ * 2.0, cb[1] + ny_ * 2.0)]
# its soft shadow on the cloth first
sh = [(p[0] + 7, p[1] + 4) for p in cue]
d.path(poly(sh), "Cue shadow", fill="#0A1E0E", opacity=30, stroke=NONE)
d.path(poly(cue), "Cue", fill=lin(ca, cb, (0, "#5A3A1C", None), (0.45, "#8A5E30", None),
       (0.8, "#C89A5C", None), (1, "#E0C48E", None)), stroke=INK, strokeWidth=1.6,
       join="round")
d.path(f"M{cb[0] - ux * 8 - nx_ * 1.9:.1f},{cb[1] - uy * 8 - ny_ * 1.9:.1f} "
       f"L{cb[0] - nx_ * 2.0:.1f},{cb[1] - ny_ * 2.0:.1f} "
       f"L{cb[0] + nx_ * 2.0:.1f},{cb[1] + ny_ * 2.0:.1f} "
       f"L{cb[0] - ux * 8 + nx_ * 1.9:.1f},{cb[1] - uy * 8 + ny_ * 1.9:.1f} Z",
       "Cue tip", fill="#E8E4D8", stroke=INK, strokeWidth=1.0)

# balls: contact shadow first, then sphere + specular
BALLS = [(-15, 3, "#EDE6D4", "#8A8474", "cue"), (15, -3, "#16130F", "#000000", "eight"),
         (11, -1, "#8E2A22", "#3A0E08", "red"), (19, -5, "#22407A", "#0C1830", "blue")]
for bx_, bz_, c1, c2, tag in BALLS:
    flat_ellipse(bx_ + 0.5, 30.32, bz_ + 0.4, 1.5, f"Ball shadow {tag}",
                 fill=rad((0, "#04140A", 0.55), (1, "#04140A", 0)), stroke=NONE)
for bx_, bz_, c1, c2, tag in BALLS:
    ex, ey = P(bx_, 31.45, bz_)
    r = S * 1.15
    d.shape("ellipse", f"Ball {tag}", x=round(ex - r, 1), y=round(ey - r, 1),
            width=round(r * 2, 1), height=round(r * 2, 1),
            fill=rad((0, shade(c1, "#FFFFFF", 0.35)), (0.55, c1, None), (1, c2, None)),
            stroke="#0A0603", strokeWidth=1.2)
    d.shape("ellipse", f"Ball spec {tag}", x=round(ex - r * 0.45, 1), y=round(ey - r * 0.6, 1),
            width=round(r * 0.5, 1), height=round(r * 0.35, 1), fill="#FFFFFF", opacity=55,
            stroke=NONE)
    if tag == "eight":
        d.shape("ellipse", "Eight spot", x=round(ex - r * 0.42, 1), y=round(ey - r * 0.34, 1),
                width=round(r * 0.84, 1), height=round(r * 0.68, 1), fill="#EDE6D4",
                stroke=NONE)
        d.text("8", "Eight digit", x=round(ex, 1), y=round(ey + r * 0.24, 1),
               size=round(r * 0.62), font="Source Sans 3", color="#16130F",
               justify="center")

# blue chalk cube on the near rail
chalk = box(7.6, 32.5, -21.6, 9.0, 33.9, -20.2)
prism("Chalk", chalk, ramp=("#1E3A66", "#5A8AC8"), lo=0.15, hi=1.0, sw=1.2)

# chalk dust motes hanging in the lamp beam
for i, (mx_, my_, mr_, mo_) in enumerate([
        (430, 300, 2.0, 30), (470, 350, 1.6, 24), (540, 320, 2.4, 30), (590, 370, 1.7, 22),
        (455, 420, 2.2, 26), (525, 450, 1.5, 20), (575, 480, 2.0, 24), (480, 520, 1.8, 20),
        (415, 470, 1.4, 18), (610, 430, 1.9, 22), (500, 380, 1.3, 18), (560, 540, 1.6, 18)]):
    EXTENT.append((mx_, my_))
    d.shape("ellipse", f"Mote {i+1}", x=mx_, y=my_, width=mr_ * 2, height=mr_ * 2,
            fill="#FFE8C0", opacity=mo_, stroke=NONE)

# warm rim light along the near rail's top edge
ra, rb = P(-44, 32.55, -22.5), P(44, 32.55, -22.5)
d.path(f"M{ra[0]:.1f},{ra[1]:.1f} L{rb[0]:.1f},{rb[1]:.1f}", "Rail rim light",
       fill=NONE, stroke="#FFCE8A", strokeWidth=2.4, opacity=40, cap="round")

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


caption("BILLIARD TABLE", "WALNUT · SLATE · BAIZE · LEATHER")
d.finish("billiard-table-V1R00")
