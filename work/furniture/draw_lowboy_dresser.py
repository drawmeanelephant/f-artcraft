#!/usr/bin/env python3
"""Lowboy dresser — field plate V1R00. Near-side three-quarter view of a
Queen Anne dressing table: overhanging thumbnail top, a long shallow drawer
over three smalls (the centre one fan-carved) over a long deep drawer, a
cyma-scalloped apron with a pendant drop, and four cabriole legs on pad
feet. A brass candlestick burns on the top — cherry plate, colonial mood.
1000x1000. Drawn in screen space like its taller cousin the highboy: flat
front elevation plus a (DX,-DY) recede for the right side and the top.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Lowboy Dresser — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#2E140C"   # warm umber, not black


def on_disc(x, y, pad):
    return math.hypot(x - PCX, y - PCY) <= PR - pad


def disc_x(y, side):
    return PCX + side * math.sqrt(PR ** 2 - (y - PCY) ** 2)


def lin(c0, c1, start=None, end=None, o0=None, o1=None):
    s0 = {"offset": 0, "color": c0}; s1 = {"offset": 1, "color": c1}
    if o0 is not None: s0["opacity"] = o0
    if o1 is not None: s1["opacity"] = o1
    g = {"kind": "linear", "stops": [s0, s1]}
    if start: g["start"], g["end"] = start, end
    return {"gradient": g}


def rad(*stops):
    n = len(stops) - 1
    return {"gradient": {"kind": "radial", "stops": [
        {"offset": round(i / n, 3), "color": c} for i, c in enumerate(stops)]}}


def glow(color, o):
    return {"gradient": {"kind": "radial", "stops": [
        {"offset": 0, "color": color, "opacity": o},
        {"offset": 1, "color": color, "opacity": 0}]}}


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


def poly(pts):
    return "M" + " L".join("%.1f,%.1f" % p for p in pts) + " Z"


# --- geometry -------------------------------------------------------------------------
DX, DY = 48, 22                     # side face recedes up and to the right
L0, L1 = 302, 658                   # case front
T0, T1 = 292, 668                   # top overhang
Y_TF, Y_TB = 296, 320               # top front band top / bottom
Y_LB = 592                          # apron bottom at the leg shoulders
Y_FT = 778                          # floor under the front feet
MID = (L0 + L1) / 2

for x, y in [(T1 + DX, Y_TF - DY), (T0 - 4, Y_TF), (L0 - 16, Y_FT + 8), (L1 + DX + 14, Y_FT - DY)]:
    assert on_disc(x, y, 16), (x, y)

CH_FRONT = lin("#C47450", "#7E3220", [L0, 300], [L1, 700])
CH_SIDE = lin("#6E2C1C", "#421610", [L1, 300], [L1 + DX, 700])
CH_TOP = lin("#DE9268", "#A85232")
BRASS = rad("#FFF0B0", "#E2B656", "#A4741E")
BRASS_LINE = "#7A5214"

# --- backdrop + plate ------------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin("#1C1208", "#080503", [0, 0], [0, 1000]), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#C09A5E", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad("#6E5434", "#45311A", "#1C1106"), stroke="#120B05", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8CE9E", strokeWidth=3, opacity=24)
# candle-warm wash on the upper left + wall detail
d.shape("ellipse", "Plate glow", x=230, y=110, width=380, height=380,
        fill=glow("#FFD8A0", 0.22), stroke=NONE)
WY = 700
d.path(f"M{disc_x(WY,-1):.1f},{WY} L{disc_x(WY,1):.1f},{WY}", "Wainscot rail",
       fill=NONE, stroke="#D8BC8E", strokeWidth=4, opacity=20, cap="round")
FY = 736
d.path(f"M{disc_x(FY,-1):.1f},{FY} L{disc_x(FY,1):.1f},{FY} A420,420 0 0 1 {disc_x(FY,-1):.1f},{FY} Z",
       "Floor", fill=lin("#4A3418", "#1E1206", [0, FY], [0, 880]), stroke=NONE, opacity=85)
for i, y in enumerate([766, 800, 834]):
    d.path(f"M{disc_x(y,-1)+10:.1f},{y} L{disc_x(y,1)-10:.1f},{y}", f"Floorboard seam {i+1}",
           fill=NONE, stroke="#2E1C0A", strokeWidth=3, opacity=35, cap="round")
d.path(f"M{disc_x(FY,-1):.1f},{FY} L{disc_x(FY,1):.1f},{FY}", "Floor edge light",
       fill=NONE, stroke="#E8C88E", strokeWidth=3, opacity=26, cap="round")
# soft contact shadow hugging the disc
d.shape("ellipse", "Shadow", x=282, y=744, width=456, height=66,
        fill=glow("#0E0602", 0.75), stroke=NONE)
d.shape("ellipse", "Shadow core", x=320, y=762, width=400, height=32,
        fill=glow("#0A0401", 0.6), stroke=NONE)

# --- cabriole legs ---------------------------------------------------------------------
def leg(name, cx, y0, y1, sgn, front=True):
    """sgn = direction the knee juts out (+1 right, -1 left)."""
    h = y1 - y0
    PP = lambda dx, t: (cx + sgn * dx, y0 + h * t)
    outer = [PP(16, 0), PP(30, 0.12), PP(30, 0.24), PP(18, 0.45), PP(6, 0.72),
             PP(5, 0.84), PP(16, 0.93), PP(22, 0.98)]
    inner = [PP(-16, 0.98), PP(-12, 0.93), PP(-7, 0.84), PP(-8, 0.72),
             PP(-12, 0.45), PP(-16, 0.24), PP(-17, 0.10), PP(-16, 0)]
    pts = outer + inner
    g = (lin("#C87A52", "#6E2A18", [cx - 30, y0], [cx + 30, y1]) if front
         else lin("#6E2A18", "#3A120A"))
    d.path(smooth(pts), name, fill=g, stroke=INK, strokeWidth=4)
    d.path(smooth([PP(10, 0.06), PP(22, 0.16), PP(18, 0.34), PP(6, 0.56)], closed=False),
           f"{name} sheen", fill=NONE, stroke="#FFCFA8", strokeWidth=5,
           opacity=45 if front else 20, cap="round")
    d.path(smooth([PP(-10, 0.5), PP(-4, 0.74), PP(-3, 0.86)], closed=False),
           f"{name} shade", fill=NONE, stroke="#1E0A05", strokeWidth=5,
           opacity=35, cap="round")
    fx, fy = cx + sgn * 3, y1 - 6
    d.shape("ellipse", f"{name} pad", x=fx - 26, y=fy - 8, width=52, height=16,
            fill=lin("#B86844", "#5A2012"), stroke=INK, strokeWidth=4)
    d.shape("ellipse", f"{name} pad sheen", x=fx - 16, y=fy - 6, width=22, height=6,
            fill="#FFD8B8", opacity=35, stroke=NONE)


# rear-right leg first, standing behind the side apron
leg("Leg rear right", L1 + DX - 14, Y_LB - DY - 4, Y_FT - DY, 1, front=False)

# --- case: right side face -----------------------------------------------------------------
d.path(poly([(L1, Y_TB), (L1 + DX, Y_TB - DY), (L1 + DX, Y_LB - DY), (L1, Y_LB)]),
       "Case side", fill=CH_SIDE, stroke=INK, strokeWidth=4)
d.path(f"M{L1+6},{Y_LB-2} C{L1+18},{Y_LB+6} {L1+32},{Y_LB-4} {L1+DX-6},{Y_LB-DY+6} "
       f"L{L1+DX-6},{Y_LB-DY-2} L{L1+6},{Y_LB-8} Z",
       "Side apron scallop", fill="#4A1A0E", stroke=INK, strokeWidth=3, opacity=90)
for i, t in enumerate([0.35, 0.68]):
    y = Y_TB + 30 + (Y_LB - Y_TB - 60) * t
    d.path(f"M{L1+6},{y:.1f} L{L1+DX-6},{y-DY:.1f}", f"Side panel line {i+1}",
           fill=NONE, stroke="#1E0A05", strokeWidth=3, opacity=30)

# --- case front with the cyma apron -----------------------------------------------------------
AP = Y_LB - 16
apron = (f"M{L0},{Y_TB} L{L1},{Y_TB} L{L1},{Y_LB} "
         f"C{L1-20},{Y_LB} {L1-28},{AP-4} {L1-52},{AP-4} "
         f"C{L1-72},{AP-4} {L1-78},{AP+12} {L1-98},{AP+12} "
         f"C{MID+28},{AP+12} {MID+18},{AP+26} {MID},{AP+26} "
         f"C{MID-18},{AP+26} {MID-28},{AP+12} {L0+98},{AP+12} "
         f"C{L0+78},{AP+12} {L0+72},{AP-4} {L0+52},{AP-4} "
         f"C{L0+28},{AP-4} {L0+20},{Y_LB} {L0},{Y_LB} Z")
d.path(apron, "Case front", fill=CH_FRONT, stroke=INK, strokeWidth=5)
d.path(f"M{L0+10},{Y_LB-4} C{L0+30},{AP+2} {L0+44},{AP+2} {L0+58},{AP}", "Apron edge light",
       fill=NONE, stroke="#FFC8A0", strokeWidth=3, opacity=38, cap="round")
# pendant drop hanging from the apron's centre dip
dy_ = AP + 26
d.path(smooth([(MID - 8, dy_), (MID - 10, dy_ + 8), (MID - 5, dy_ + 15), (MID - 9, dy_ + 22),
               (MID, dy_ + 30), (MID + 9, dy_ + 22), (MID + 5, dy_ + 15),
               (MID + 10, dy_ + 8), (MID + 8, dy_)]),
       "Apron drop", fill=lin("#C87A52", "#6E2A18"), stroke=INK, strokeWidth=3)
d.shape("ellipse", "Drop sheen", x=MID - 4, y=dy_ + 6, width=6, height=12,
        fill="#FFCFA8", opacity=35, stroke=NONE)

# --- drawers -----------------------------------------------------------------------------------
def batwing(name, cx, cy):
    d.path(f"M{cx-20},{cy} C{cx-16},{cy-11} {cx-7},{cy-9} {cx},{cy-5} "
           f"C{cx+7},{cy-9} {cx+16},{cy-11} {cx+20},{cy} "
           f"C{cx+16},{cy+11} {cx+7},{cy+9} {cx},{cy+5} "
           f"C{cx-7},{cy+9} {cx-16},{cy+11} {cx-20},{cy} Z",
           f"{name} plate", fill=BRASS, stroke=BRASS_LINE, strokeWidth=2)
    d.path(f"M{cx-12},{cy-1} Q{cx},{cy+15} {cx+12},{cy-1}", f"{name} bail",
           fill=NONE, stroke=lin("#FFE6A0", "#9A6A1C"), strokeWidth=3.5, cap="round")
    for s in (-1, 1):
        d.shape("ellipse", f"{name} post {s}", x=cx + s * 12 - 3, y=cy - 4, width=6, height=6,
                fill="#FFF2C0", stroke=BRASS_LINE, strokeWidth=1.5)


def fan(name, cx, cy, r):
    n = 9
    for i in range(n):
        a0 = math.pi + math.pi * i / n
        a1 = math.pi + math.pi * (i + 1) / n
        p0 = (cx + r * math.cos(a0), cy + r * math.sin(a0))
        p1 = (cx + r * math.cos(a1), cy + r * math.sin(a1))
        light = i % 2 == 0
        d.path(f"M{cx},{cy} L{p0[0]:.1f},{p0[1]:.1f} A{r},{r} 0 0 1 {p1[0]:.1f},{p1[1]:.1f} Z",
               f"{name} ray {i+1}", fill=lin("#FCEFC8", "#E2C48A") if light
               else lin("#E0B070", "#B07A3C"), stroke=NONE, opacity=95)
    d.path(f"M{cx-r},{cy} A{r},{r} 0 0 1 {cx+r},{cy}", f"{name} band", fill=NONE,
           stroke="#F6E2B0", strokeWidth=4, opacity=90)
    d.path(f"M{cx-r-5},{cy} A{r+5},{r+5} 0 0 1 {cx+r+5},{cy}", f"{name} stringing",
           fill=NONE, stroke="#3A1A0C", strokeWidth=3, opacity=60)
    d.shape("ellipse", f"{name} hub", x=cx - 7, y=cy - 7, width=14, height=14,
            fill=rad("#FFF6DA", "#C89A58"), stroke=NONE)


def drawer(name, x0, y0, x1, y1, pulls=2, key=True):
    d.shape("rectangle", f"{name} recess", x=x0 - 3, y=y0 - 3, width=x1 - x0 + 6,
            height=y1 - y0 + 6, fill="#2E1008", opacity=55, stroke=NONE)
    d.shape("rectangle", name, x=x0, y=y0, width=x1 - x0, height=y1 - y0,
            fill=lin("#C87854", "#86341F", [x0, y0], [x1, y1]), stroke=INK, strokeWidth=3)
    d.path(f"M{x0+3},{y1-3} L{x0+3},{y0+3} L{x1-3},{y0+3}", f"{name} lip light",
           fill=NONE, stroke="#FFCCA4", strokeWidth=3, opacity=45, cap="round")
    d.path(f"M{x0+3},{y1-3} L{x1-3},{y1-3} L{x1-3},{y0+3}", f"{name} lip shade",
           fill=NONE, stroke="#200A04", strokeWidth=3, opacity=35, cap="round")
    h = y1 - y0
    for j in range(2 if h < 60 else 3):
        y = y0 + h * (0.3 + 0.28 * j)
        amp = 3 + j
        d.path(f"M{x0+8},{y:.1f} C{x0+(x1-x0)*0.3:.1f},{y-amp:.1f} "
               f"{x0+(x1-x0)*0.6:.1f},{y+amp:.1f} {x1-8},{y-1:.1f}",
               f"{name} grain {j+1}", fill=NONE, stroke="#5A2010", strokeWidth=2.5,
               opacity=22, cap="round")
    cy = (y0 + y1) / 2
    if pulls == "knobs":
        for k, f in enumerate([0.12, 0.88]):
            kx = x0 + (x1 - x0) * f
            d.shape("ellipse", f"{name} knob {k+1}", x=kx - 7, y=cy - 7, width=14, height=14,
                    fill=BRASS, stroke=BRASS_LINE, strokeWidth=2)
        return
    xs = [x0 + (x1 - x0) * f for f in ([0.5] if pulls == 1 else [0.22, 0.78])]
    for k, cx in enumerate(xs):
        batwing(f"{name} pull {k+1}", cx, cy)
    if key and pulls == 2:
        kx = (x0 + x1) / 2
        d.shape("ellipse", f"{name} escutcheon", x=kx - 7, y=cy - 10, width=14, height=20,
                fill=BRASS, stroke=BRASS_LINE, strokeWidth=2)
        d.path(f"M{kx},{cy-4} L{kx},{cy+4}", f"{name} keyhole", fill=NONE,
               stroke="#241204", strokeWidth=3, cap="round")


G = 6
X0, X1 = L0 + 12, L1 - 12
y = Y_TB + 8
drawer("Top long drawer", X0, y, X1, y + 40)
y += 40 + G
wsmall = 100
drawer("Small drawer left", X0, y, X0 + wsmall, y + 52, pulls=1)
drawer("Small drawer right", X1 - wsmall, y, X1, y + 52, pulls=1)
cx0, cx1 = X0 + wsmall + G, X1 - wsmall - G
drawer("Fan drawer", cx0, y, cx1, y + 52, pulls="knobs", key=False)
fan("Fan inlay", (cx0 + cx1) / 2, y + 46, 30)
y += 52 + G
drawer("Deep drawer", X0, y, X1, y + 74)
# a cockbead moulding strip under the drawer bank finishes the apron rail
mb = y + 82
d.shape("rectangle", "Bead shadow", x=X0 - 2, y=mb, width=X1 - X0 + 4, height=10,
        fill="#2E1008", opacity=50, stroke=NONE)
d.shape("rectangle", "Bead moulding", x=X0, y=mb + 1, width=X1 - X0, height=6,
        fill=lin("#C87854", "#6E2A18", [0, mb], [0, mb + 6]), stroke=INK, strokeWidth=1.5)
d.path(f"M{X0+2},{mb+2} L{X1-2},{mb+2}", "Bead light",
       fill=NONE, stroke="#FFC8A0", strokeWidth=1.6, opacity=45, cap="round")
# shade under the top overhang
d.shape("rectangle", "Top shadow", x=L0, y=Y_TB, width=L1 - L0, height=12,
        fill=lin("#1E0A05", "#1E0A05", [0, Y_TB], [0, Y_TB + 12], 0.5, 0), stroke=NONE)

# --- front cabriole legs -----------------------------------------------------------------------
leg("Leg front left", L0 + 18, Y_LB - 6, Y_FT, -1)
leg("Leg front right", L1 - 18, Y_LB - 6, Y_FT, 1)
# knee brackets tie the legs into the apron
for i, (x, s) in enumerate([(L0 + 34, 1), (L1 - 34, -1)]):
    d.path(f"M{x},{Y_LB-4} C{x+s*10},{Y_LB-2} {x+s*14},{Y_LB+2} {x+s*16},{Y_LB-4} Z",
           f"Knee bracket {i+1}", fill="#9A4A2E", stroke=INK, strokeWidth=3)

# --- top slab ----------------------------------------------------------------------------------
d.path(poly([(T0, Y_TF), (T1, Y_TF), (T1 + DX, Y_TF - DY), (T0 + DX, Y_TF - DY)]),
       "Top surface", fill=CH_TOP, stroke=INK, strokeWidth=4, join="round")
d.path(poly([(T0, Y_TF), (T1, Y_TF), (T1, Y_TB), (T0, Y_TB)]),
       "Top front edge", fill=lin("#B06038", "#6E2A18", [0, Y_TF], [0, Y_TB]),
       stroke=INK, strokeWidth=3)
d.path(poly([(T1, Y_TF), (T1 + DX, Y_TF - DY), (T1 + DX, Y_TB - DY), (T1, Y_TB)]),
       "Top right edge", fill=lin("#8A4026", "#4A1A0E", [0, Y_TF - DY], [0, Y_TB - DY]),
       stroke=INK, strokeWidth=3)
# thumbnail moulding: a raised bead along the front band
d.path(f"M{T0+6},{Y_TF+10} L{T1-6},{Y_TF+10}", "Top bead light",
       fill=NONE, stroke="#FFC8A0", strokeWidth=3, opacity=50, cap="round")
d.path(f"M{T0+6},{Y_TB-5} L{T1-6},{Y_TB-5}", "Top bead shade",
       fill=NONE, stroke="#1E0A05", strokeWidth=3, opacity=45, cap="round")
# top-surface sheen and back edge
d.path(f"M{T0+10},{Y_TF-DY*0.35:.0f} L{T1-20},{Y_TF-DY*0.35:.0f}", "Top sheen",
       fill=NONE, stroke="#FFDCB0", strokeWidth=8, opacity=20, cap="round")

# --- candlestick on the top --------------------------------------------------------------------
CX_, CY_ = 366, 282                 # drip-pan centre on the top surface
d.shape("ellipse", "Candle pool", x=CX_ - 70, y=CY_ - 20, width=150, height=34,
        fill=glow("#FFC87A", 0.28), stroke=NONE)
d.shape("ellipse", "Drip pan", x=CX_ - 22, y=CY_ - 8, width=44, height=16,
        fill=BRASS, stroke=BRASS_LINE, strokeWidth=2.5)
d.path(smooth([(CX_ - 8, CY_ - 4), (CX_ - 5, CY_ - 14), (CX_ - 9, CY_ - 24),
               (CX_ - 4, CY_ - 32), (CX_ - 6, CY_ - 38), (CX_ + 6, CY_ - 38),
               (CX_ + 4, CY_ - 32), (CX_ + 9, CY_ - 24), (CX_ + 5, CY_ - 14),
               (CX_ + 8, CY_ - 4)]),
       "Candle stem", fill=lin("#E8C878", "#8A5E1E", [CX_ - 9, 0], [CX_ + 9, 0]),
       stroke=INK, strokeWidth=2)
d.path(f"M{CX_-5},{CY_-38} C{CX_-5.5},{CY_-58} {CX_-5},{CY_-74} {CX_-4},{CY_-82} "
       f"L{CX_+4},{CY_-82} C{CX_+5},{CY_-74} {CX_+5.5},{CY_-58} {CX_+5},{CY_-38} Z",
       "Candle", fill=lin("#F4EAD2", "#C8B892", [CX_ - 5, 0], [CX_ + 5, 0]),
       stroke=INK, strokeWidth=2)
d.path(f"M{CX_},{CY_-82} L{CX_},{CY_-88}", "Wick", fill=NONE, stroke="#241204",
       strokeWidth=2.4, cap="round")
# flame: warm teardrop + halo
d.shape("ellipse", "Flame glow", x=CX_ - 52, y=CY_ - 152, width=104, height=110,
        fill=glow("#FFC87A", 0.4), stroke=NONE)
d.path(f"M{CX_},{CY_-128} C{CX_+9},{CY_-112} {CX_+8},{CY_-100} {CX_},{CY_-92} "
       f"C{CX_-8},{CY_-100} {CX_-9},{CY_-112} {CX_},{CY_-128} Z",
       "Flame", fill=rad("#FFF8DC", "#FFC860", "#E88820"), stroke=NONE)
d.shape("ellipse", "Flame core", x=CX_ - 3.5, y=CY_ - 108, width=7, height=12,
        fill="#FFFCE8", opacity=90, stroke=NONE)

# --- extent check ------------------------------------------------------------------------------
for x, y in [(CX_, CY_ - 152), (T0, Y_TB), (MID, dy_ + 34), (T1 + DX, Y_TB - DY)]:
    assert on_disc(x, y, 14), (x, y)


# --- caption -------------------------------------------------------------------------------------
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
               color="#F0E0C2", justify="center")
    m = d.text(mats, "Materials", x=500, y=970, size=22, font="Virelai Sans",
               color="#C9AC85", justify="center")
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


caption("LOWBOY DRESSER", "CHERRY · BRASS")
d.finish("lowboy-dresser-V1R00")
