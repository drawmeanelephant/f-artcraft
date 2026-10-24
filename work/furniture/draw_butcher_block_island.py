#!/usr/bin/env python3
"""Butcher block island — field plate V1R00. Three-quarter view from the
front right: a massive end-grain maple slab — the kitchen's anvil — its
top a checkerboard of maple blocks, on four thick legs with a low slatted
shelf. Prep props: a cleaver stuck in the top, a halved onion, a sprig of
rosemary, a linen towel draped over the near edge. Maple plate on a cool
slate field, prep mood. 1000x1000. Modelled in inches (x right, y up,
+z back), projected with a fixed yaw + pitch; carcass parts are 8-corner
prisms culled by view normal and shaded by lamp light.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Butcher Block Island — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#1E1810"   # warm dark, not black
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
S, OX, OY = 10.9, 502.0, 726.0
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


def prism(name, corners, ramp=("#7A4E24", "#D9AE72"), lo=0.06, hi=0.94, sw=1.8):
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
        fill=lin((0, 0), (0, 1000), (0, "#131A18"), (1, "#060908")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#A8B8A0", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#39443C"), (0.55, "#212A22"), (1, "#0D120C")),
        stroke="#0C0F0A", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C8D8C2", strokeWidth=3, opacity=22)

# cool morning light from a high window, faint
d.shape("ellipse", "Window glow", x=280, y=150, width=440, height=320,
        fill=rad((0, "#D8E4DA", 0.13), (0.55, "#8AA092", 0.05), (1, "#8AA092", 0)),
        stroke=NONE)

# --- floor: dark boards closing on the disc arc ---------------------------------------
FYB = 752
hw = math.sqrt(PR ** 2 - (FYB - PCY) ** 2)
d.path(f"M{PCX - hw:.1f},{FYB} L{PCX + hw:.1f},{FYB} A420,420 0 0 0 {PCX - hw:.1f},{FYB} Z",
       "Floor", fill=lin((0, FYB), (0, 880), (0, "#323A32", 0.5), (0.5, "#1C221C", 0.7),
                         (1, "#0B0E09", 0.9)), stroke=NONE)
for i, yb in enumerate([784, 816, 848]):
    h = math.sqrt(PR ** 2 - (yb - PCY) ** 2) - 4
    d.path(f"M{PCX - h:.1f},{yb} L{PCX + h:.1f},{yb}", f"Board seam {i+1}",
           fill=NONE, stroke="#4A5A4C", strokeWidth=2, opacity=24)

# --- grounding shadow under the block ---------------------------------------------------
fx0, fy0 = P(-16, 0, -10)
fx1, fy1 = P(16, 0, 10)
sx0, sx1 = min(fx0, fx1) - 28, max(fx0, fx1) + 28
sy0, sy1 = min(fy0, fy1) - 15, max(fy0, fy1) + 19
d.shape("ellipse", "Block shadow", x=round(sx0), y=round(sy0),
        width=round(sx1 - sx0), height=round(sy1 - sy0),
        fill=rad((0, "#030403", 0.7), (0.6, "#030403", 0.3), (1, "#030403", 0)),
        stroke=NONE)

# --- block geometry (inches) ---------------------------------------------------------------
MAPLE = ("#7A4E24", "#D9AE72")
MAPLE_HI = ("#8A5E2E", "#E8C48A")
MAPLE_DK = ("#5E3C1A", "#B8884E")

# slatted shelf first (behind the near legs)
for i, zs in enumerate((-6.4, -3.2, 0.0, 3.2, 6.4)):
    prism(f"Shelf slat {i+1}", box(-13.6, 8.0, zs - 1.1, 13.6, 9.0, zs + 1.1),
          ramp=MAPLE_DK, lo=0.05, hi=0.8, sw=1.4)
# bearer bars under the slat ends
prism("Shelf bearer L", box(-14.6, 7.2, -8.6, -12.6, 8.2, 8.6), ramp=MAPLE_DK, lo=0.04, hi=0.7)
prism("Shelf bearer R", box(12.6, 7.2, -8.6, 14.6, 8.2, 8.6), ramp=MAPLE_DK, lo=0.04, hi=0.7)

# legs: thick squares with a slight taper
def leg(sx, sz, tag):
    lx, lz = sx * 13.8, sz * 7.8
    corners = [(lx - 1.45, 0, lz - 1.45), (lx + 1.45, 0, lz - 1.45),
               (lx + 1.45, 0, lz + 1.45), (lx - 1.45, 0, lz + 1.45),
               (lx - 1.75, 25.5, lz - 1.75), (lx + 1.75, 25.5, lz - 1.75),
               (lx + 1.75, 25.5, lz + 1.75), (lx - 1.75, 25.5, lz + 1.75)]
    prism(f"Leg {tag}", corners, ramp=MAPLE, lo=0.04, hi=0.88)


leg(-1, 1, "far L")
leg(1, 1, "far R")
leg(-1, -1, "near L")
leg(1, -1, "near R")

# shallow apron rails between the legs
prism("Apron far", box(-13.0, 22.5, 6.6, 13.0, 26.0, 9.4), ramp=MAPLE, lo=0.03, hi=0.7)
prism("Apron L", box(-15.4, 22.5, -7.0, -13.0, 26.0, 7.0), ramp=MAPLE, lo=0.03, hi=0.7)
prism("Apron R", box(13.0, 22.5, -7.0, 15.4, 26.0, 7.0), ramp=MAPLE, lo=0.03, hi=0.7)
prism("Apron near", box(-13.0, 22.5, -9.4, 13.0, 26.0, -6.6), ramp=MAPLE, lo=0.03, hi=0.7)

# the great slab: five inches of end-grain maple
prism("Block slab", box(-17, 26, -11, 17, 31, 11), ramp=MAPLE_HI, lo=0.14, hi=1.0, sw=2.2)

# end-grain checkerboard on the top face: blocks of alternating maple
X0, X1, Z0, Z1 = -16.4, 16.4, -10.4, 10.4
NC, NR = 9, 6
CELLS = ["#EBD2A4", "#DDBB84", "#CFA96C", "#C69E62"]
for r in range(NR):
    for c in range(NC):
        x0 = X0 + (X1 - X0) * c / NC
        x1 = X0 + (X1 - X0) * (c + 1) / NC
        z0 = Z0 + (Z1 - Z0) * r / NR
        z1 = Z0 + (Z1 - Z0) * (r + 1) / NR
        tone = CELLS[(r + c) % 2 + ((r * 7 + c * 3) % 2) * 2]
        pts = [P(x0, 31.02, z0), P(x1, 31.02, z0), P(x1, 31.02, z1), P(x0, 31.02, z1)]
        y0_, y1_ = min(p[1] for p in pts), max(p[1] for p in pts)
        d.path(poly(pts), f"Cell {r}-{c}", fill=lin((0, y0_), (0, y1_),
               (0, shade(tone, "#FFFFFF", 0.12), None), (1, shade(tone, "#000000", 0.10), None)),
               stroke="#8A5E2E", strokeWidth=0.55, opacity=92)

# knife scars: a few pale nicks across the grain
for i, (x0, z0, x1, z1) in enumerate([(-9, -4, -3, -3.4), (2, 5, 8, 5.8), (-13, 2, -8, 2.6)]):
    a, b = P(x0, 31.05, z0), P(x1, 31.05, z1)
    d.path(f"M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}", f"Scar {i+1}",
           fill=NONE, stroke="#F4E4BC", strokeWidth=1.6, opacity=28, cap="round")

# --- the cleaver, struck into the block -------------------------------------------------------
# blade plane in x/y at z=1.6, leaning ~7 degrees
CBX, CBZ, TILT = 9.5, 1.8, math.radians(7)
ct, st_ = math.cos(TILT), math.sin(TILT)


def blade_pt(u, v):
    """u across the blade, v up from the bite; rotated about the bite point."""
    x = CBX + u * ct - v * st_
    y = 30.4 + u * st_ + v * ct
    return P(x, y, CBZ)


# shadow of the blade cast on the top
sh = [P(CBX - 4.6, 31.06, CBZ + 0.6), P(CBX + 4.2, 31.06, CBZ + 1.0),
      P(CBX + 5.4, 31.06, CBZ + 3.4), P(CBX - 3.4, 31.06, CBZ + 3.0)]
d.path(poly(sh), "Cleaver shadow", fill="#0A1208", opacity=30, stroke=NONE)

bw, bh = 3.4, 4.3
blade = [blade_pt(-bw, 0), blade_pt(bw, 0), blade_pt(bw, bh), blade_pt(-bw, bh)]
by0, by1 = min(p[1] for p in blade), max(p[1] for p in blade)
d.path(poly(blade), "Cleaver blade",
       fill=lin((blade[0][0], by0), (blade[2][0], by1),
                (0, "#E8ECE8", None), (0.55, "#9AA8A4", None), (1, "#5E6E68", None)),
       stroke=INK, strokeWidth=1.8, join="round")
# the bevel line near the cutting edge and a dark spine
e0, e1 = blade_pt(-bw + 0.5, 0.8), blade_pt(bw - 0.3, 0.5)
d.path(f"M{e0[0]:.1f},{e0[1]:.1f} L{e1[0]:.1f},{e1[1]:.1f}", "Cleaver bevel",
       fill=NONE, stroke="#F4F8F4", strokeWidth=2.0, opacity=50)
s0, s1 = blade_pt(-bw + 0.2, bh - 0.4), blade_pt(bw - 0.2, bh - 0.6)
d.path(f"M{s0[0]:.1f},{s0[1]:.1f} L{s1[0]:.1f},{s1[1]:.1f}", "Cleaver spine",
       fill=NONE, stroke="#4A5450", strokeWidth=2.6, opacity=70)
# the hole in the blade's far corner
hl = blade_pt(bw - 0.8, bh - 0.9)
d.shape("ellipse", "Cleaver hole", x=round(hl[0] - 3.0, 1), y=round(hl[1] - 3.0, 1),
        width=6.0, height=6.0, fill="#1A140E", stroke="#8A9894", strokeWidth=1.0)
# handle rising from the blade top
h0, h1 = blade_pt(-0.7, bh - 0.2), blade_pt(0.9, bh + 3.4)
h2, h3 = blade_pt(-1.6, bh + 3.2), blade_pt(-2.4, bh - 0.1)
d.path(poly([h0, h1, h2, h3]), "Cleaver handle",
       fill=lin(h0, h1, (0, "#8A5E30", None), (1, "#4A2E14", None)),
       stroke=INK, strokeWidth=1.6, join="round")
rv = blade_pt(-0.9, bh + 1.6)
d.shape("ellipse", "Handle rivet", x=round(rv[0] - 2.0, 1), y=round(rv[1] - 2.0, 1),
        width=4.0, height=4.0, fill="#D8DCD4", stroke=INK, strokeWidth=0.8)

# --- halved onion + rosemary ----------------------------------------------------------------
# cut face up: concentric rings
onx, onz = -7.0, -3.0
flat_ellipse(onx + 0.4, 31.06, onz + 0.4, 2.5, "Onion shadow",
             fill=rad((0, "#0A1208", 0.4), (1, "#0A1208", 0)), stroke=NONE)
for i, (rr, cc) in enumerate([(2.4, "#7E3A48"), (2.05, "#F0E4D0"), (1.55, "#D8BFB8"),
                              (1.05, "#F0E4D0"), (0.5, "#C9A8A0")]):
    flat_ellipse(onx, 31.07 + i * 0.01, onz, rr, f"Onion ring {i}", fill=cc,
                 stroke="#8A4A55", strokeWidth=0.9)
# dome-side half beside it
dcx, dcz = -2.6, -4.6
flat_ellipse(dcx + 0.4, 31.06, dcz + 0.4, 2.1, "Dome shadow",
             fill=rad((0, "#0A1208", 0.4), (1, "#0A1208", 0)), stroke=NONE)
dce = P(dcx, 31.8, dcz)
d.shape("ellipse", "Onion dome", x=round(dce[0] - 24, 1), y=round(dce[1] - 15, 1),
        width=48, height=30,
        fill=rad((0, "#F4EADA", None), (0.6, "#D8BEB0", None), (1, "#8A4A55", None)),
        stroke=INK, strokeWidth=1.2)
for i in (-1, 0, 1):
    d.path(f"M{dce[0] - 16:.1f},{dce[1] + 12:.1f} Q{dce[0] + i * 9:.1f},{dce[1] - 10:.1f} "
           f"{dce[0] + 16:.1f},{dce[1] + 10:.1f}", f"Onion layer {i}",
           fill=NONE, stroke="#A85E68", strokeWidth=1.1, opacity=45)

# a sprig of rosemary near the cleaver
rb0 = P(3.5, 31.1, -5.5)
rb1 = P(9.0, 31.1, -4.0)
d.path(f"M{rb0[0]:.1f},{rb0[1]:.1f} L{rb1[0]:.1f},{rb1[1]:.1f}", "Rosemary stem",
       fill=NONE, stroke="#3E5E3A", strokeWidth=2.4, cap="round")
ux, uy = rb1[0] - rb0[0], rb1[1] - rb0[1]
ul = math.hypot(ux, uy)
ux, uy = ux / ul, uy / ul
nx_, ny_ = -uy, ux
for i in range(1, 9):
    t = i / 9.0
    bx_, by_ = rb0[0] + ux * ul * t, rb0[1] + uy * ul * t
    for sgn in (-1, 1):
        lx_, ly_ = bx_ + (ux * 0.35 + nx_ * sgn) * 7, by_ + (uy * 0.35 + ny_ * sgn) * 7
        EXTENT.append((lx_, ly_))
        d.path(f"M{bx_:.1f},{by_:.1f} L{lx_:.1f},{ly_:.1f}", f"Needle {i}{sgn}",
               fill=NONE, stroke="#5E8A54", strokeWidth=1.7, cap="round")

# --- linen towel over the near-left edge ------------------------------------------------------
t0 = [P(-15.5, 31.06, -10.9), P(-9.5, 31.06, -10.9), P(-9.5, 31.06, -7.6), P(-15.5, 31.06, -7.6)]
d.path(poly(t0), "Towel flat", fill=lin((0, min(p[1] for p in t0)), (0, max(p[1] for p in t0)),
       (0, "#F0EADC", None), (1, "#C8BFA8", None)), stroke="#9A8E72", strokeWidth=1.0)
fl = [P(-15.5, 31.0, -11.15), P(-9.5, 31.0, -11.15), P(-9.8, 23.2, -11.5), P(-15.8, 23.6, -11.5)]
d.path(poly(fl), "Towel flap", fill=lin((0, min(p[1] for p in fl)), (0, max(p[1] for p in fl)),
       (0, "#E4DCC8", None), (1, "#A89E84", None)), stroke="#8A7E64", strokeWidth=1.2, join="round")
# the stripe woven near the towel's edge, on flat and flap
s_ = [P(-14.4, 31.07, -10.92), P(-10.6, 31.07, -10.92)]
d.path(f"M{s_[0][0]:.1f},{s_[0][1]:.1f} L{s_[1][0]:.1f},{s_[1][1]:.1f}", "Towel stripe flat",
       fill=NONE, stroke="#A04038", strokeWidth=2.0, opacity=75)
s_ = [P(-14.5, 28.0, -11.3), P(-10.7, 28.0, -11.3)]
d.path(f"M{s_[0][0]:.1f},{s_[0][1]:.1f} L{s_[1][0]:.1f},{s_[1][1]:.1f}", "Towel stripe flap",
       fill=NONE, stroke="#A04038", strokeWidth=2.0, opacity=75)

# warm rim light along the near top edge
ra, rb = P(-16.6, 31.1, -11), P(16.6, 31.1, -11)
d.path(f"M{ra[0]:.1f},{ra[1]:.1f} L{rb[0]:.1f},{rb[1]:.1f}", "Top rim light",
       fill=NONE, stroke="#FFE0A8", strokeWidth=2.4, opacity=35, cap="round")

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


def caption(name, mats, nsize=56, ntrack=60):
    n = d.text(name, "Name", x=500, y=934, size=nsize, font="Virelai Sans",
               color="#F0E6CE", justify="center")
    m = d.text(mats, "Materials", x=500, y=970, size=22, font="Virelai Sans",
               color="#C4B091", justify="center")
    d.cmd("text.setStyle", "Name tracking", ids=[n["id"]], tracking=ntrack)
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


caption("BUTCHER BLOCK ISLAND", "MAPLE · END GRAIN · STEEL", nsize=46, ntrack=50)
d.finish("butcher-block-island-V1R00")
