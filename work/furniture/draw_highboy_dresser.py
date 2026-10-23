#!/usr/bin/env python3
"""Highboy dresser — field plate V1R00. Near-side three-quarter view of a
cherry chest-on-stand: stepped-in upper case under a flat cornice, a lower
case with a scalloped apron and drop finials, a fan-inlaid centre drawer and
four cabriole legs on pad feet. Cherry on a green plate. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Highboy Dresser — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#3A1A12"   # warm umber, not black

def on_disc(x, y, pad):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

def disc_x(y, side):
    return PCX + side * math.sqrt(PR**2 - (y - PCY)**2)

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
        {"offset": 0, "color": color, "opacity": o}, {"offset": 1, "color": color, "opacity": 0}]}}

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
DX, DY = 54, 26                     # side face recedes up and to the right
L0, L1 = 292, 652                   # lower case front
U0, U1 = 314, 630                   # upper case front, stepped in
M0, M1 = 284, 660                   # waist moulding
C0, C1 = 294, 650                   # cornice
Y_CT, Y_CB = 150, 182               # cornice top / bottom
Y_UB = 462                          # upper case bottom
Y_MB = 476                          # waist moulding bottom
Y_LB = 640                          # lower case bottom (corners)
Y_FT = 790                          # floor under the front feet

for x, y in [(C1 + DX, Y_CT - DY), (C0 - 4, Y_CT), (L0 - 14, Y_FT), (L1 + DX + 16, Y_FT - DY)]:
    assert on_disc(x, y, 18), (x, y)

CH_FRONT = lin("#D07A54", "#8C3824", [L0, 160], [L1, 700])
CH_SIDE = lin("#7E3220", "#4E1C12", [L1, 200], [L1 + DX, 700])
CH_DRAWER = lin("#CC7350", "#963E28", [0, 0], [1, 1])
CH_TOP = lin("#E49A70", "#B05C3C")
BRASS = rad("#FFF0B0", "#E2B656", "#A4741E")
BRASS_LINE = "#7A5214"

# --- backdrop + plate ------------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin("#14261C", "#060D09", [0, 0], [0, 1000]), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876, fill="#7FB08A", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad("#9CC4A0", "#6E9E78", "#3E6A4C"), stroke=NONE)
# window light falling from the upper left
WIN = [(190, 250), (380, 92), (560, 92), (400, 836), (232, 718)]
for x, y in WIN:
    assert on_disc(x, y, 8), (x, y)
d.path(poly(WIN), "Window light",
       fill=lin("#F6F2D8", "#F6F2D8", [200, 80], [420, 760], 0.16, 0), stroke=NONE)
d.shape("ellipse", "Plate glow", x=210, y=100, width=420, height=420, fill=glow("#E8F4DA", 0.30), stroke=NONE)
# wainscot line and floor, both closed on the disc arc
WY = 700
d.path(f"M{disc_x(WY,-1):.1f},{WY} L{disc_x(WY,1):.1f},{WY}", "Wainscot rail",
       fill=NONE, stroke="#D8ECD6", strokeWidth=4, opacity=22, cap="round")
FY = 748
d.path(f"M{disc_x(FY,-1):.1f},{FY} L{disc_x(FY,1):.1f},{FY} A420,420 0 0 1 {disc_x(FY,-1):.1f},{FY} Z",
       "Floor", fill=lin("#4E7A58", "#24442E", [0, FY], [0, 880]), stroke=NONE, opacity=85)
for i, y in enumerate([778, 812, 846]):
    d.path(f"M{disc_x(y,-1)+10:.1f},{y} L{disc_x(y,1)-10:.1f},{y}", f"Floorboard seam {i+1}",
           fill=NONE, stroke="#1A3322", strokeWidth=3, opacity=35, cap="round")
d.path(f"M{disc_x(FY,-1):.1f},{FY} L{disc_x(FY,1):.1f},{FY}", "Floor edge light",
       fill=NONE, stroke="#CFE8CC", strokeWidth=3, opacity=30, cap="round")
# soft contact shadow hugging the disc
d.shape("ellipse", "Shadow", x=262, y=748, width=476, height=70, fill=glow("#0C1E12", 0.75), stroke=NONE)
d.shape("ellipse", "Shadow core", x=300, y=766, width=420, height=34, fill=glow("#08140C", 0.6), stroke=NONE)

# --- cabriole legs -------------------------------------------------------------------------
def leg(name, cx, y0, y1, sgn, front=True):
    """sgn = direction the knee juts out (+1 right, -1 left)."""
    h = y1 - y0
    P = lambda dx, t: (cx + sgn * dx, y0 + h * t)
    outer = [P(16, 0), P(30, 0.12), P(30, 0.24), P(18, 0.45), P(6, 0.72), P(5, 0.84), P(16, 0.93), P(22, 0.98)]
    inner = [P(-16, 0.98), P(-12, 0.93), P(-7, 0.84), P(-8, 0.72), P(-12, 0.45), P(-16, 0.24), P(-17, 0.10), P(-16, 0)]
    pts = outer + inner
    g = lin("#D88460", "#7A2C1A", [cx - 30, y0], [cx + 30, y1]) if front else lin("#8A3A26", "#4A1A10")
    d.path(smooth(pts), name, fill=g, stroke=INK, strokeWidth=4)
    # knee highlight and the ankle shadow
    d.path(smooth([P(10, 0.06), P(22, 0.16), P(18, 0.34), P(6, 0.56)], closed=False), f"{name} sheen",
           fill=NONE, stroke="#FFD2B0", strokeWidth=5, opacity=45 if front else 20, cap="round")
    d.path(smooth([P(-10, 0.5), P(-4, 0.74), P(-3, 0.86)], closed=False), f"{name} shade",
           fill=NONE, stroke="#2A0E08", strokeWidth=5, opacity=35, cap="round")
    # pad foot
    fx, fy = cx + sgn * 3, y1 - 6
    d.shape("ellipse", f"{name} pad", x=fx - 26, y=fy - 8, width=52, height=16,
            fill=lin("#C4704C", "#6E2616"), stroke=INK, strokeWidth=4)
    d.shape("ellipse", f"{name} pad sheen", x=fx - 16, y=fy - 6, width=22, height=6, fill="#FFD8B8", opacity=35, stroke=NONE)

# rear-right leg first, it stands behind the side apron
leg("Leg rear right", L1 + DX - 14, Y_LB - DY - 4, Y_FT - DY, 1, front=False)

# --- lower case ------------------------------------------------------------------------------
# side face with its own scalloped apron
d.path(poly([(L1, Y_MB), (L1 + DX, Y_MB - DY), (L1 + DX, Y_LB - DY), (L1, Y_LB)]), "Lower case side",
       fill=CH_SIDE, stroke=INK, strokeWidth=4)
d.path(f"M{L1+6},{Y_LB-3} C{L1+18},{Y_LB+8} {L1+34},{Y_LB-2} {L1+DX-6},{Y_LB-DY+6} L{L1+DX-6},{Y_LB-DY-2} L{L1+6},{Y_LB-6} Z",
       "Side apron scallop", fill="#5A2014", stroke=INK, strokeWidth=3, opacity=90)
for i, t in enumerate([0.3, 0.62]):
    y = Y_MB + (Y_LB - Y_MB) * t
    d.path(f"M{L1+6},{y:.1f} L{L1+DX-6},{y-DY:.1f}", f"Lower side panel line {i+1}",
           fill=NONE, stroke="#2A0E08", strokeWidth=3, opacity=30)
# front face with a scalloped apron edge
AP = Y_LB - 32
apron = (f"M{L0},{Y_MB} L{L1},{Y_MB} L{L1},{Y_LB} "
         f"C{L1-24},{Y_LB} {L1-30},{AP+6} {L1-56},{AP+6} "
         f"C{L1-76},{AP+6} {L1-80},{AP+22} {L1-104},{AP+22} "
         f"C{(L0+L1)/2+30},{AP+22} {(L0+L1)/2+24},{AP+40} {(L0+L1)/2},{AP+40} "
         f"C{(L0+L1)/2-24},{AP+40} {(L0+L1)/2-30},{AP+22} {L0+104},{AP+22} "
         f"C{L0+80},{AP+22} {L0+76},{AP+6} {L0+56},{AP+6} "
         f"C{L0+30},{AP+6} {L0+24},{Y_LB} {L0},{Y_LB} Z")
d.path(apron, "Lower case front", fill=CH_FRONT, stroke=INK, strokeWidth=5)
d.path(f"M{L0+8},{Y_LB-4} C{L0+26},{AP+12} {L0+40},{AP+10} {L0+56},{AP+10}", "Apron edge light",
       fill=NONE, stroke="#FFC8A0", strokeWidth=3, opacity=40, cap="round")
# drop finials under the apron
for i, x in enumerate([L0 + 104, L1 - 104]):
    y = AP + 22
    d.path(smooth([(x - 7, y), (x - 9, y + 8), (x - 4, y + 16), (x - 8, y + 24), (x, y + 34),
                   (x + 8, y + 24), (x + 4, y + 16), (x + 9, y + 8), (x + 7, y)]),
           f"Drop finial {i+1}", fill=lin("#D88460", "#7A2C1A"), stroke=INK, strokeWidth=3)

def drawer(name, x0, y0, x1, y1, pulls=2, key=True):
    d.shape("rectangle", f"{name} recess", x=x0 - 3, y=y0 - 3, width=x1 - x0 + 6, height=y1 - y0 + 6,
            fill="#3A140C", opacity=55, stroke=NONE)
    d.shape("rectangle", name, x=x0, y=y0, width=x1 - x0, height=y1 - y0,
            fill=lin("#D27C56", "#923A24", [x0, y0], [x1, y1]), stroke=INK, strokeWidth=3)
    # thumbnail moulding: lit top-left edge, shaded bottom-right edge
    d.path(f"M{x0+3},{y1-3} L{x0+3},{y0+3} L{x1-3},{y0+3}", f"{name} lip light",
           fill=NONE, stroke="#FFCCA4", strokeWidth=3, opacity=45, cap="round")
    d.path(f"M{x0+3},{y1-3} L{x1-3},{y1-3} L{x1-3},{y0+3}", f"{name} lip shade",
           fill=NONE, stroke="#2A0C06", strokeWidth=3, opacity=35, cap="round")
    # figure in the cherry: soft long waves
    h = y1 - y0
    for j in range(2 if h < 60 else 3):
        y = y0 + h * (0.3 + 0.28 * j)
        amp = 3 + j
        d.path(f"M{x0+8},{y:.1f} C{x0+(x1-x0)*0.3:.1f},{y-amp:.1f} {x0+(x1-x0)*0.6:.1f},{y+amp:.1f} {x1-8},{y-1:.1f}",
               f"{name} grain {j+1}", fill=NONE, stroke="#6A2414", strokeWidth=2.5, opacity=22, cap="round")
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
        d.path(f"M{kx},{cy-4} L{kx},{cy+4}", f"{name} keyhole", fill=NONE, stroke="#2A1608",
               strokeWidth=3, cap="round")

def batwing(name, cx, cy):
    d.path(f"M{cx-20},{cy} C{cx-16},{cy-11} {cx-7},{cy-9} {cx},{cy-5} C{cx+7},{cy-9} {cx+16},{cy-11} {cx+20},{cy} "
           f"C{cx+16},{cy+11} {cx+7},{cy+9} {cx},{cy+5} C{cx-7},{cy+9} {cx-16},{cy+11} {cx-20},{cy} Z",
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
               f"{name} ray {i+1}", fill=lin("#FCEFC8", "#E2C48A") if light else lin("#E0B070", "#B07A3C"),
               stroke=NONE, opacity=95)
    d.path(f"M{cx-r},{cy} A{r},{r} 0 0 1 {cx+r},{cy}", f"{name} band", fill=NONE,
           stroke="#F6E2B0", strokeWidth=4, opacity=90)
    d.path(f"M{cx-r-5},{cy} A{r+5},{r+5} 0 0 1 {cx+r+5},{cy}", f"{name} stringing", fill=NONE,
           stroke="#3A1A0C", strokeWidth=3, opacity=60)
    d.shape("ellipse", f"{name} hub", x=cx - 7, y=cy - 7, width=14, height=14, fill=rad("#FFF6DA", "#C89A58"),
            stroke=NONE)

G = 6
y = Y_MB + G
drawer("Lower long drawer", L0 + G + 6, y, L1 - G - 6, y + 44)
y += 44 + G
wsmall = 92
drawer("Lower drawer left", L0 + G + 6, y, L0 + G + 6 + wsmall, y + 72, pulls=1)
drawer("Lower drawer right", L1 - G - 6 - wsmall, y, L1 - G - 6, y + 72, pulls=1)
cx0, cx1 = L0 + G + 6 + wsmall + G, L1 - G - 6 - wsmall - G
drawer("Lower fan drawer", cx0, y, cx1, y + 72, pulls="knobs", key=False)
fan("Fan inlay", (cx0 + cx1) / 2, y + 64, 40)
# shade under the waist moulding
d.shape("rectangle", "Waist shadow", x=L0, y=Y_MB, width=L1 - L0, height=14,
        fill=lin("#2A0C06", "#2A0C06", [0, Y_MB], [0, Y_MB + 14], 0.5, 0), stroke=NONE)

# front cabriole legs
leg("Leg front left", L0 + 18, Y_LB - 4, Y_FT, -1)
leg("Leg front right", L1 - 6, Y_LB - 4, Y_FT, 1)
# knee brackets tie the legs into the apron
for i, (x, s) in enumerate([(L0 + 34, 1), (L1 - 22, -1)]):
    d.path(f"M{x},{Y_LB-2} C{x+s*10},{Y_LB} {x+s*14},{Y_LB+4} {x+s*16},{Y_LB-2} Z",
           f"Knee bracket {i+1}", fill="#B05A3A", stroke=INK, strokeWidth=3)

# --- waist moulding ----------------------------------------------------------------------------
d.path(poly([(M1, Y_UB), (M1 + DX, Y_UB - DY), (M1 + DX, Y_MB - DY), (M1, Y_MB)]), "Waist moulding side",
       fill=lin("#8A3A26", "#5A2014"), stroke=INK, strokeWidth=3)
d.path(poly([(M0, Y_UB), (M1, Y_UB), (M1 + DX, Y_UB - DY), (M0 + DX, Y_UB - DY)]), "Waist moulding top",
       fill=CH_TOP, stroke=INK, strokeWidth=3)
d.shape("rectangle", "Waist moulding", x=M0, y=Y_UB, width=M1 - M0, height=Y_MB - Y_UB,
        fill=lin("#E08A62", "#9A4228", [0, Y_UB], [0, Y_MB]), stroke=INK, strokeWidth=4)
d.path(f"M{M0+4},{Y_UB+4} L{M1-4},{Y_UB+4}", "Waist moulding bead", fill=NONE, stroke="#FFD4B0",
       strokeWidth=3, opacity=55, cap="round")

# --- upper case ---------------------------------------------------------------------------------
d.path(poly([(U1, Y_CB), (U1 + DX, Y_CB - DY), (U1 + DX, Y_UB - DY), (U1, Y_UB)]), "Upper case side",
       fill=CH_SIDE, stroke=INK, strokeWidth=4)
for i, t in enumerate([0.25, 0.5, 0.75]):
    yy = Y_CB + (Y_UB - Y_CB) * t
    d.path(f"M{U1+6},{yy:.1f} L{U1+DX-6},{yy-DY:.1f}", f"Upper side panel line {i+1}",
           fill=NONE, stroke="#2A0E08", strokeWidth=3, opacity=25)
d.shape("rectangle", "Upper case front", x=U0, y=Y_CB, width=U1 - U0, height=Y_UB - Y_CB,
        fill=CH_FRONT, stroke=INK, strokeWidth=5)
# fluted quarter columns at the front corners
for i, x in enumerate([U0 + 4, U1 - 16]):
    d.shape("rectangle", f"Quarter column {i+1}", x=x, y=Y_CB + 6, width=12, height=Y_UB - Y_CB - 12,
            fill=lin("#E0906A", "#8A3622"), stroke=INK, strokeWidth=3)
    d.path(f"M{x+6},{Y_CB+14} L{x+6},{Y_UB-14}", f"Quarter column {i+1} flute", fill=NONE,
           stroke="#4A1A0E", strokeWidth=3, opacity=45, cap="round")
IX0, IX1 = U0 + 22, U1 - 22
avail = (Y_UB - Y_CB) - 5 * G
rows = [50, 58, 68, 76]
rows = [r * avail / sum(rows) for r in rows]
y = Y_CB + G
half = (IX1 - IX0 - G) / 2
drawer("Upper small drawer left", IX0, y, IX0 + half, y + rows[0], pulls=1)
drawer("Upper small drawer right", IX1 - half, y, IX1, y + rows[0], pulls=1)
y += rows[0] + G
for j, h in enumerate(rows[1:]):
    drawer(f"Upper long drawer {j+1}", IX0, y, IX1, y + h)
    y += h + G

# --- cornice ------------------------------------------------------------------------------------
d.path(poly([(C1, Y_CT), (C1 + DX, Y_CT - DY), (C1 + DX, Y_CB - DY), (C1, Y_CB)]), "Cornice side",
       fill=lin("#8A3A26", "#5A2014"), stroke=INK, strokeWidth=3)
d.path(poly([(C0, Y_CT), (C1, Y_CT), (C1 + DX, Y_CT - DY), (C0 + DX, Y_CT - DY)]), "Cornice top",
       fill=CH_TOP, stroke=INK, strokeWidth=3)
cornice = (f"M{C0},{Y_CT} L{C1},{Y_CT} L{C1},{Y_CT+10} C{C1-6},{Y_CT+12} {C1-10},{Y_CT+20} {U1+6},{Y_CB} "
           f"L{U0-6},{Y_CB} C{C0+10},{Y_CT+20} {C0+6},{Y_CT+12} {C0},{Y_CT+10} Z")
d.path(cornice, "Cornice", fill=lin("#E8986E", "#9A4228", [0, Y_CT], [0, Y_CB]), stroke=INK, strokeWidth=4)
d.path(f"M{C0+4},{Y_CT+5} L{C1-4},{Y_CT+5}", "Cornice fillet", fill=NONE, stroke="#FFDAB8",
       strokeWidth=3, opacity=60, cap="round")
d.path(f"M{U0-2},{Y_CB-6} L{U1+2},{Y_CB-6}", "Cornice cove line", fill=NONE, stroke="#4A1A0E",
       strokeWidth=3, opacity=40, cap="round")
d.shape("rectangle", "Cornice shadow", x=U0, y=Y_CB, width=U1 - U0, height=18,
        fill=lin("#2A0C06", "#2A0C06", [0, Y_CB], [0, Y_CB + 18], 0.5, 0), stroke=NONE)

# --- light on the cherry ---------------------------------------------------------------------------
d.path(poly([(U0 + 30, Y_CB + 4), (U0 + 96, Y_CB + 4), (L0 + 70, Y_LB - 30), (L0 + 20, Y_LB - 30)]),
       "Front sheen", fill=lin("#FFE6CC", "#FFE6CC", [U0, Y_CB], [L0 + 60, Y_LB], 0.22, 0.02), stroke=NONE)
d.path(f"M{U1+3},{Y_CB+2} L{U1+3},{Y_UB-2}", "Upper corner rim light", fill=NONE, stroke="#FFC09A",
       strokeWidth=3, opacity=40, cap="round")
d.path(f"M{L1+3},{Y_MB+2} L{L1+3},{Y_LB-4}", "Lower corner rim light", fill=NONE, stroke="#FFC09A",
       strokeWidth=3, opacity=40, cap="round")

# plate rim drawn last so everything inside closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840, fill=NONE, stroke="#16301E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E2F2DC", strokeWidth=3, opacity=30)

# --- name + second line -----------------------------------------------------------------------------
d.text("HIGHBOY DRESSER", "Name", x=500, y=940, size=58, font="Virelai Sans", color="#E2F0DC", justify="center")
LINE2, SZ2, TRK = "CHERRY · WHITE PINE · BRASS", 22, 200
r = d.text(LINE2, "Second line", x=500, y=975, size=SZ2, font="Virelai Sans", color="#A8CCAE", justify="center")
d.cmd("text.setStyle", "Second line tracking", id=r["id"], tracking=TRK)
def find(o, oid):
    if isinstance(o, dict):
        if o.get("id") == oid and "bounds" in o: return o
        o = list(o.values())
    if isinstance(o, list):
        for v in o:
            hit = find(v, oid)
            if hit: return hit
b2 = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("second line bounds", {k: round(v) for k, v in b2.items()})
assert b2["width"] <= 760 and b2["x"] >= 100 and b2["y"] + b2["height"] <= 990, b2

d.finish("highboy-dresser-V1R00")
