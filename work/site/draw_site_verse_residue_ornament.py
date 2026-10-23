#!/usr/bin/env python3
"""Verse-residue panel ornament — site equity plate V1R00. A divider set of
three production ornaments, each labelled in Virelai Sans:
  I   tentacle-scroll — tapering arms that end in inward spiral curls
  II  mascots medley — candle / diamond / scroll (U+E006 + U+E004)
  III pure geometry — twin rules and diamonds in Virelai spirit
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Verse Residue Ornament — Site Equity", 1000, 1000)

INK = "#3A2418"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2A1C10"}, {"offset": 1, "color": "#100904"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F4E8CC"}, {"offset": 0.7, "color": "#D9BE92"},
    {"offset": 1, "color": "#A9845A"}]}}
GOLD_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F4CE72"}, {"offset": 0.6, "color": "#D9A03C"},
    {"offset": 1, "color": "#9C6218"}]}}
ARM_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7A5428"}, {"offset": 1, "color": "#4A3018"}]}}
CORE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#5E3A20"}, {"offset": 1, "color": "#2A1608"}]}}

PCX, PCY, PR = 500, 460, 420
def on_disc(x, y, pad):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

def diamond(cx, cy, r):
    return f"M{cx},{cy-r} L{cx+r},{cy} L{cx},{cy+r} L{cx-r},{cy} Z"

def quad(p0, p1, p2, t):
    u = 1 - t
    return (u*u*p0[0] + 2*u*t*p1[0] + t*t*p2[0],
            u*u*p0[1] + 2*u*t*p1[1] + t*t*p2[1],
            2*u*(p1[0]-p0[0]) + 2*t*(p2[0]-p1[0]),
            2*u*(p1[1]-p0[1]) + 2*t*(p2[1]-p1[1]))

def taper(root, ctrl, tip, w0, w1, n=16):
    """Filled strip along a quadratic, w0 at root -> w1 at tip."""
    L, Rr = [], []
    for k in range(n + 1):
        x, y, dx, dy = quad(root, ctrl, tip, k / n)
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy/ln, dx/ln
        w = (w0 + (w1 - w0) * k / n) / 2
        L.append((x + nx*w, y + ny*w)); Rr.append((x - nx*w, y - ny*w))
    s = "M%.1f,%.1f " % L[0] + " ".join("L%.1f,%.1f" % p for p in L[1:])
    return s + " " + " ".join("L%.1f,%.1f" % p for p in reversed(Rr)) + " Z"

def curl(tip, direction, r0, turns=1.45, n=34):
    """Stroked spiral polyline continuing `direction` (unit vec) from tip,
    rolling under the arm tip."""
    # centre sits perpendicular to travel, on the underside (downward) side
    nx, ny = -direction[1], direction[0]
    if ny < 0:
        nx, ny = -nx, -ny
    cx, cy = tip[0] + nx*r0, tip[1] + ny*r0
    th0 = math.atan2(tip[1]-cy, tip[0]-cx)
    # wind so motion at start follows `direction`: th increases if tangent
    # (d/dth = (-sin,cos)) aligns with direction
    sgn = 1 if (-math.sin(th0)*direction[0] + math.cos(th0)*direction[1]) > 0 else -1
    pts = []
    for k in range(n + 1):
        th = th0 + sgn * turns * 2 * math.pi * k / n
        r = r0 * (1 - 0.82 * k / n)
        pts.append((cx + r*math.cos(th), cy + r*math.sin(th)))
    return ("M%.1f,%.1f " % pts[0]) + " ".join("L%.1f,%.1f" % p for p in pts[1:]), pts[-1]

# --- backdrop + plate -------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#D9BE92", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#2E1C0E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F8F0DC", strokeWidth=3, opacity=40)
d.shape("ellipse", "Patina 1", x=190, y=640, width=240, height=130, fill="#B08C5E", opacity=16, stroke=NONE)
d.shape("ellipse", "Patina 2", x=600, y=150, width=220, height=120, fill="#B08C5E", opacity=15, stroke=NONE)
for i, (x, y, w) in enumerate([(200,330,7),(790,290,6),(170,540,8),(830,520,7),(250,730,6),
                               (740,720,8),(145,430,6),(855,410,7),(420,120,7),(600,130,6),
                               (300,170,5),(700,180,6),(330,810,5),(660,800,6),(500,105,5)]):
    assert on_disc(x, y, 12), (x, y)
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#8A6844", opacity=35, stroke=NONE)

def band_label(txt, y):
    d.text(txt, f"Label {txt}", x=500, y=y, size=15, font="Virelai Sans",
           color="#5E3A20", justify="center")

# === I · TENTACLE-SCROLL =====================================================
Y1 = 285
# centre diamond + beads
d.path(diamond(500, Y1, 15), "T1 centre", fill=GOLD_GRAD, stroke=INK, strokeWidth=4, join="round")
for sx in (1, -1):
    root = (500 + sx*24, Y1 + 3)
    ctrl = (500 + sx*130, Y1 + 26)
    tip  = (500 + sx*196, Y1 - 8)
    # tapered arm
    d.path(taper(root, ctrl, tip, 11, 4.5), f"T1 arm {'R' if sx>0 else 'L'}",
           fill=ARM_GRAD, stroke=NONE)
    # sucker dots on the underside of the arm
    for j, t in enumerate([0.45, 0.62, 0.78]):
        x, y, dx, dy = quad(root, ctrl, tip, t)
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy/ln, dx/ln
        if ny < 0:
            nx, ny = -nx, -ny
        w = (11 + (4.5-11)*t) / 2
        r = 3.4 - j * 0.7
        d.shape("ellipse", f"T1 sucker {sx}_{j}", x=x + nx*(w+2) - r,
                y=y + ny*(w+2) - r, width=2*r, height=2*r,
                fill="#4A3018", opacity=70, stroke=NONE)
    # spiral curl continuing the tip tangent, inward
    _,_,dx,dy = quad(root, ctrl, tip, 1.0)
    ln = math.hypot(dx, dy) or 1
    dirv = (dx/ln, dy/ln)
    cd, end = curl(tip, dirv, 22)
    d.path(cd, f"T1 curl {'R' if sx>0 else 'L'}", fill=NONE, stroke="#4A3018",
           strokeWidth=4.5, cap="round")
    assert on_disc(end[0], end[1], 30), end
    d.shape("ellipse", f"T1 curl eye {sx}", x=end[0]-3, y=end[1]-3, width=6, height=6,
            fill="#B8905E", stroke=NONE)
band_label("TENTACLE-SCROLL", Y1 + 58)

# === II · MASCOTS MEDLEY =====================================================
Y2 = 480
CANDLE, SCROLL = "\ue006", "\ue004"
# flanking hairlines with end dots
for sx in (1, -1):
    d.path(f"M{500+sx*230},{Y2} L{500+sx*130},{Y2}", f"T2 rule {sx}",
           fill=NONE, stroke="#8A6844", strokeWidth=2.5, opacity=70, cap="round")
    d.shape("ellipse", f"T2 dot {sx}", x=500+sx*240-3, y=Y2-3, width=6, height=6,
            fill="#8A6844", opacity=80, stroke=NONE)
# candle - diamond - scroll, evenly centred
d.text(CANDLE, "Medley candle", x=420, y=Y2+22, size=54, font="Virelai Mascots",
       color=INK, justify="center")
d.path(diamond(500, Y2, 15), "Medley diamond", fill=GOLD_GRAD, stroke=INK,
       strokeWidth=4, join="round")
d.text(SCROLL, "Medley scroll", x=585, y=Y2+22, size=54, font="Virelai Mascots",
       color=INK, justify="center")
band_label("MASCOTS MEDLEY", Y2 + 58)

# === III · PURE GEOMETRY =====================================================
Y3 = 668
# twin rules each side, end diamonds, centre diamond stack
for sx in (1, -1):
    d.path(f"M{500+sx*210},{Y3-5} L{500+sx*52},{Y3-5}", f"T3 ruleA {sx}",
           fill=NONE, stroke=INK, strokeWidth=3, cap="round")
    d.path(f"M{500+sx*210},{Y3+5} L{500+sx*52},{Y3+5}", f"T3 ruleB {sx}",
           fill=NONE, stroke=INK, strokeWidth=3, cap="round")
    d.path(diamond(500+sx*228, Y3, 8), f"T3 end {sx}", fill=INK, stroke=NONE)
    d.path(diamond(500+sx*36, Y3, 8), f"T3 inner {sx}", fill=GOLD_GRAD,
           stroke=INK, strokeWidth=2.5, join="round")
d.path(diamond(500, Y3, 17), "T3 centre", fill=CORE_GRAD, stroke="#F0C96A",
       strokeWidth=3, join="round")
band_label("PURE GEOMETRY", Y3 + 58)

# --- name + role ------------------------------------------------------------------
d.text("RESIDUE ORNAMENT", "Name", x=500, y=930, size=58, font="Virelai Sans",
       color="#F0E2C4", justify="center")
d.text(" ".join("RELATED RESIDUE"), "Role", x=500, y=968, size=23, font="Virelai Sans",
       color="#C6A472", justify="center")

d.finish("site-verse-residue-ornament-V1R00")
