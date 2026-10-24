#!/usr/bin/env python3
"""Vanity table — field plate V1R00. Three-quarter view from the front
right: a low painted table with slim tapered legs and one drawer, an oval
mirror swung between two finial posts at the back edge, bulbs glowing
around the frame, and a mirrored tray crowded with small bottles. Painted
plate, boudoir mood — a deep plum field with warm bulb light.
1000x1000. Modelled in inches (x right, y up, +z back), projected with a
fixed yaw + pitch; carcass parts are 8-corner prisms culled by view normal
and shaded by lamp light.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Vanity Table — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#241418"   # warm dark, not black
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
YAW, PITCH = math.radians(30), math.radians(24)
S, OX, OY = 10.4, 502.0, 730.0
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


def prism(name, corners, ramp=("#3E4A44", "#9EB0A2"), lo=0.06, hi=0.94, sw=1.8):
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


def cylinder(name, cx, y0, y1, cz, r, ramp, sw=1.4, top_kw=None):
    """Vertical cylinder: projected side wall + top ellipse."""
    eb = P(cx, y0, cz)
    et = P(cx, y1, cz)
    rx, ry = S * r, S * r * SP
    side = (f"M{eb[0] - rx:.1f},{eb[1]:.1f} L{et[0] - rx:.1f},{et[1]:.1f} "
            f"A{rx:.1f},{ry:.1f} 0 0 1 {et[0] + rx:.1f},{et[1]:.1f} "
            f"L{eb[0] + rx:.1f},{eb[1]:.1f} "
            f"A{rx:.1f},{ry:.1f} 0 0 0 {eb[0] - rx:.1f},{eb[1]:.1f} Z")
    d.path(side, name, fill=lin((0, et[1]), (0, eb[1]),
           (0, ramp[1], None), (1, ramp[0], None)), stroke=INK,
           strokeWidth=sw, join="round")
    kw = {"fill": rad((0, shade(ramp[1], "#FFFFFF", 0.25), None),
                      (1, ramp[1], None)), "stroke": INK, "strokeWidth": sw}
    if top_kw:
        kw.update(top_kw)
    flat_ellipse(cx, y1, cz, r, name + " top", **kw)


def upright_oval(name, cx, cy, cz, rx, ry, n=26, **kw):
    """Vertical oval in the x/y plane at depth cz, projected truly."""
    pts = [P(cx + rx * math.cos(2 * math.pi * i / n),
             cy + ry * math.sin(2 * math.pi * i / n), cz)
           for i in range(n)]
    d.path(poly(pts), name, join="round", **kw)
    return pts


# --- backdrop + plate ---------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#1B1016"), (1, "#090507")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#D8A8B8", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#4A3038"), (0.55, "#2C1B22"), (1, "#130A0E")),
        stroke="#100A0C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8C8D0", strokeWidth=3, opacity=22)

# warm bulb glow pooled behind the mirror zone
d.shape("ellipse", "Boudoir glow", x=310, y=180, width=400, height=300,
        fill=rad((0, "#FFC890", 0.15), (0.55, "#B87A5A", 0.06), (1, "#B87A5A", 0)),
        stroke=NONE)

# --- floor: dark boards closing on the disc arc ---------------------------------------
FYB = 752
hw = math.sqrt(PR ** 2 - (FYB - PCY) ** 2)
d.path(f"M{PCX - hw:.1f},{FYB} L{PCX + hw:.1f},{FYB} A420,420 0 0 0 {PCX - hw:.1f},{FYB} Z",
       "Floor", fill=lin((0, FYB), (0, 880), (0, "#3A2A30", 0.5), (0.5, "#221419", 0.7),
                         (1, "#0D0709", 0.9)), stroke=NONE)
for i, yb in enumerate([784, 816, 848]):
    h = math.sqrt(PR ** 2 - (yb - PCY) ** 2) - 4
    d.path(f"M{PCX - h:.1f},{yb} L{PCX + h:.1f},{yb}", f"Board seam {i+1}",
           fill=NONE, stroke="#5E4450", strokeWidth=2, opacity=24)

# --- grounding shadow under the table ---------------------------------------------------
fx0, fy0 = P(-19, 0, -8)
fx1, fy1 = P(19, 0, 8)
sx0, sx1 = min(fx0, fx1) - 26, max(fx0, fx1) + 26
sy0, sy1 = min(fy0, fy1) - 14, max(fy0, fy1) + 18
d.shape("ellipse", "Table shadow", x=round(sx0), y=round(sy0),
        width=round(sx1 - sx0), height=round(sy1 - sy0),
        fill=rad((0, "#040203", 0.7), (0.6, "#040203", 0.3), (1, "#040203", 0)),
        stroke=NONE)

# --- table geometry (inches) ---------------------------------------------------------------
PAINT = ("#43544C", "#A4BCAC")          # celadon-grey paint
PAINT_HI = ("#4E6055", "#BCD0BE")
GILT = ("#4A3414", "#C89A52")

# slim tapered legs, far pair first
def leg(sx, sz, tag):
    lx, lz = sx * 17.2, sz * 5.8
    corners = [(lx - 0.75, 0, lz - 0.75), (lx + 0.75, 0, lz - 0.75),
               (lx + 0.75, 0, lz + 0.75), (lx - 0.75, 0, lz + 0.75),
               (lx - 1.05, 18.5, lz - 1.05), (lx + 1.05, 18.5, lz - 1.05),
               (lx + 1.05, 18.5, lz + 1.05), (lx - 1.05, 18.5, lz + 1.05)]
    prism(f"Leg {tag}", corners, ramp=PAINT, lo=0.05, hi=0.9, sw=1.4)
    # little gilt foot cap
    prism(f"Foot {tag}", box(lx - 0.88, 0, lz - 0.88, lx + 0.88, 1.1, lz + 0.88),
          ramp=GILT, lo=0.1, hi=0.9, sw=1.1)


leg(-1, 1, "far L")
leg(1, 1, "far R")
leg(-1, -1, "near L")
leg(1, -1, "near R")

# apron: shallow skirt, drawer front proud on the near face
prism("Apron far", box(-16.5, 17.8, 4.6, 16.5, 21.4, 6.6), ramp=PAINT, lo=0.03, hi=0.7)
prism("Apron L", box(-18.0, 17.8, -5.0, -16.4, 21.4, 5.4), ramp=PAINT, lo=0.03, hi=0.7)
prism("Apron R", box(16.4, 17.8, -5.0, 18.0, 21.4, 5.4), ramp=PAINT, lo=0.03, hi=0.7)
prism("Apron near", box(-16.5, 17.8, -6.6, 16.5, 21.4, -4.6), ramp=PAINT, lo=0.03, hi=0.7)
prism("Drawer", box(-6.0, 18.3, -7.15, 6.0, 20.9, -6.55), ramp=PAINT_HI, lo=0.15, hi=0.95, sw=1.4)
kn = P(0, 19.6, -7.2)
d.shape("ellipse", "Drawer knob", x=round(kn[0] - 2.6, 1), y=round(kn[1] - 2.6, 1),
        width=5.2, height=5.2,
        fill=rad((0, "#E8C87A", None), (1, "#6A4A1A", None)),
        stroke=INK, strokeWidth=0.9)

# a thin gilt edge moulding under the top slab — drawn first so only its
# proud ring survives past the slab's faces
prism("Edge moulding", box(-19.75, 20.9, -8.25, 19.75, 21.6, 8.25), ramp=GILT, lo=0.1, hi=0.85, sw=1.2)
prism("Top slab", box(-19.5, 21.4, -8.0, 19.5, 23.4, 8.0), ramp=PAINT_HI, lo=0.12, hi=1.0, sw=2.0)

# worn top highlight: a soft sheen across the paint
ta, tb = P(-18.5, 23.45, -7.2), P(18.5, 23.45, 6.8)
d.path(f"M{ta[0]:.1f},{ta[1]:.1f} L{tb[0]:.1f},{tb[1]:.1f}", "Top sheen",
       fill=NONE, stroke="#EAF4E8", strokeWidth=10, opacity=12, cap="round")

# --- mirror: posts, frame, glass, bulbs ---------------------------------------------------
POSTX, POSTZ = 10.2, 6.9
for sx, tag in ((-1, "L"), (1, "R")):
    lx = sx * POSTX
    corners = [(lx - 0.55, 23.4, POSTZ - 0.55), (lx + 0.55, 23.4, POSTZ - 0.55),
               (lx + 0.55, 23.4, POSTZ + 0.55), (lx - 0.55, 23.4, POSTZ + 0.55),
               (lx - 0.42, 42.6, POSTZ - 0.42), (lx + 0.42, 42.6, POSTZ - 0.42),
               (lx + 0.42, 42.6, POSTZ + 0.42), (lx - 0.42, 42.6, POSTZ + 0.42)]
    prism(f"Post {tag}", corners, ramp=GILT, lo=0.15, hi=1.0, sw=1.3)
    ft = P(lx, 43.6, POSTZ)
    d.shape("ellipse", f"Finial {tag}", x=round(ft[0] - 4.6, 1), y=round(ft[1] - 4.6, 1),
            width=9.2, height=9.2,
            fill=rad((0, "#F0D08A", None), (0.6, "#B08A44", None), (1, "#5A3E16", None)),
            stroke=INK, strokeWidth=1.0)

# low stretcher bar between the posts under the glass
prism("Mirror stretcher", box(-9.6, 25.6, 6.5, 9.6, 27.0, 7.4),
      ramp=GILT, lo=0.1, hi=0.85, sw=1.2)

MCX, MCY, MCZ = 0.0, 36.4, 7.0
MRX, MRY = 8.6, 9.8
# gilt frame ring, then the glass
upright_oval("Mirror frame", MCX, MCY, MCZ, MRX + 0.55, MRY + 0.55,
             fill=lin((MCX - MRX, MCY - MRY), (MCX + MRX, MCY + MRY),
                      (0, "#E8C87A", None), (0.5, "#9A7434", None), (1, "#4A3414", None)),
             stroke=INK, strokeWidth=1.6)
upright_oval("Mirror glass", MCX, MCY, MCZ, MRX, MRY,
             fill=lin((MCX - MRX * 0.6, MCY - MRY), (MCX + MRX * 0.5, MCY + MRY),
                      (0, "#E4EEE9", None), (0.45, "#A9BCB4", None), (1, "#4E5E5C", None)),
             stroke="#2E2018", strokeWidth=1.0)
# sheen band across the glass (quad kept inside the oval)
sh_pts = [P(MCX - MRX * 0.62, MCY - MRY * 0.62, MCZ - 0.05),
          P(MCX - MRX * 0.10, MCY - MRY * 0.95, MCZ - 0.05),
          P(MCX + MRX * 0.30, MCY + MRY * 0.88, MCZ - 0.05),
          P(MCX - MRX * 0.28, MCY + MRY * 0.94, MCZ - 0.05)]
d.path(poly(sh_pts), "Mirror sheen", fill="#FFFFFF", opacity=16, stroke=NONE)
# pivot knobs where the glass meets the posts
for sx, tag in ((-1, "L"), (1, "R")):
    pv = P(sx * (MRX + 0.15), MCY, MCZ - 0.1)
    d.shape("ellipse", f"Pivot {tag}", x=round(pv[0] - 3.2, 1), y=round(pv[1] - 3.2, 1),
            width=6.4, height=6.4,
            fill=rad((0, "#F0D08A", None), (1, "#5A3E16", None)),
            stroke=INK, strokeWidth=1.0)

# vanity bulbs around the frame: glow first, then the lamps
BULBS = []
for i in range(10):
    t = 2 * math.pi * i / 10 + math.pi / 10
    BULBS.append(P(MCX + (MRX + 1.15) * math.cos(t), MCY + (MRY + 1.15) * math.sin(t), MCZ - 0.3))
for i, (bx_, by_) in enumerate(BULBS):
    d.shape("ellipse", f"Bulb glow {i+1}", x=round(bx_ - 11, 1), y=round(by_ - 11, 1),
            width=22, height=22,
            fill=rad((0, "#FFD898", 0.5), (0.6, "#D89850", 0.15), (1, "#D89850", 0)),
            stroke=NONE)
for i, (bx_, by_) in enumerate(BULBS):
    d.shape("ellipse", f"Bulb {i+1}", x=round(bx_ - 3.4, 1), y=round(by_ - 3.4, 1),
            width=6.8, height=6.8,
            fill=rad((0, "#FFF2D0", None), (0.7, "#F0C070", None), (1, "#A07028", None)),
            stroke=INK, strokeWidth=0.8)

# --- the tray and its small bottles ---------------------------------------------------------
TOP = 23.45
# mirrored tray under the right-hand cluster
flat_ellipse(10.5, TOP + 0.03, 0.8, 5.6, "Tray",
             fill=lin((P(5, TOP, -4)), (P(16, TOP, 5)),
                      (0, "#C8D4D2", 0.55), (0.6, "#7E8E8C", 0.45), (1, "#3E4A48", 0.5)),
             stroke="#C89A52", strokeWidth=1.6)

# bottle shadows
for bx_, bz_, br_ in ((-12.5, 1.5, 1.3), (-8.8, -3.0, 1.6), (10.8, 0.2, 1.5),
                      (15.0, 3.8, 2.1), (6.8, -3.8, 1.0), (13.2, -2.6, 0.9)):
    flat_ellipse(bx_ + 0.4, TOP + 0.04, bz_ + 0.4, br_ + 0.3, f"Bottle shadow {bx_}",
                 fill=rad((0, "#0A0507", 0.4), (1, "#0A0507", 0)), stroke=NONE)

# tall scent cylinder, pale rose
cylinder("Scent bottle", -12.5, TOP, TOP + 4.6, 1.5, 1.0, ("#6E3A42", "#D89AA4"))
sc = P(-12.5, TOP + 5.1, 1.5)
d.shape("ellipse", "Scent stopper", x=round(sc[0] - 3.6, 1), y=round(sc[1] - 3.6, 1),
        width=7.2, height=7.2,
        fill=rad((0, "#F4DCE0", None), (1, "#8A5258", None)), stroke=INK, strokeWidth=0.9)

# round flacon, violet
cylinder("Flacon", -8.8, TOP, TOP + 2.9, -3.0, 1.45, ("#3A2E52", "#9A88C8"))
fc = P(-8.8, TOP + 3.5, -3.0)
d.shape("ellipse", "Flacon stopper", x=round(fc[0] - 2.8, 1), y=round(fc[1] - 2.8, 1),
        width=5.6, height=5.6,
        fill=rad((0, "#E8D8F0", None), (1, "#5A4878", None)), stroke=INK, strokeWidth=0.9)

# square amber flacon (faceted prism reads cut-glass)
prism("Amber flacon", box(10.0, TOP, -0.6, 11.7, TOP + 3.4, 1.1),
      ramp=("#6E3A0E", "#E0A050"), lo=0.2, hi=1.0, sw=1.2)
prism("Amber stopper", box(10.45, TOP + 3.4, -0.15, 11.25, TOP + 4.5, 0.65),
      ramp=("#8A5A18", "#F0C070"), lo=0.3, hi=1.0, sw=1.0)

# squat ivory powder box
cylinder("Powder box", 15.0, TOP, TOP + 1.35, 3.8, 2.05, ("#6E6252", "#D8CCB4"))
# and a small green vial + slim clear bottle on the tray
cylinder("Green vial", 6.8, TOP, TOP + 3.1, -3.8, 0.8, ("#2E4A38", "#8AB89A"))
cylinder("Clear bottle", 13.2, TOP, TOP + 3.8, -2.6, 0.75, ("#5E6A68", "#C8D4D0"))
cb = P(13.2, TOP + 4.15, -2.6)
d.shape("ellipse", "Clear stopper", x=round(cb[0] - 2.2, 1), y=round(cb[1] - 2.2, 1),
        width=4.4, height=4.4,
        fill=rad((0, "#FFFFFF", None), (1, "#8A9896", None)), stroke=INK, strokeWidth=0.8)

# a hand mirror laid flat at the near-left corner of the top
hmc = P(-14.5, TOP + 0.12, -4.2)
d.shape("ellipse", "Hand mirror face", x=round(hmc[0] - 16, 1), y=round(hmc[1] - 11, 1),
        width=32, height=22,
        fill=rad((0, "#D8E4E0", None), (0.7, "#8E9E9A", None), (1, "#4E5E5A", None)),
        stroke="#C89A52", strokeWidth=1.6)
hd = P(-17.4, TOP + 0.1, -6.4)
d.path(f"M{hmc[0] - 12:.1f},{hmc[1] + 8:.1f} L{hd[0] - 6:.1f},{hd[1] + 12:.1f}",
       "Hand mirror handle", fill=NONE, stroke="#C89A52", strokeWidth=4.2, cap="round")

# warm rim light along the near top edge
ra, rb = P(-19.2, 23.5, -8.2), P(19.2, 23.5, -8.2)
d.path(f"M{ra[0]:.1f},{ra[1]:.1f} L{rb[0]:.1f},{rb[1]:.1f}", "Top rim light",
       fill=NONE, stroke="#FFCEA0", strokeWidth=2.2, opacity=35, cap="round")

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


caption("VANITY TABLE", "PAINTED BEECH · MIRROR GLASS · BRASS")
d.finish("vanity-table-V1R00")
