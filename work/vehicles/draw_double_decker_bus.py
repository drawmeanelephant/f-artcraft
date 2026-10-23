#!/usr/bin/env python3
"""Double-decker bus — field plate V1R00. Near-profile three-quarter of a
half-century city double-decker moving right: tomato-red body with a cream
band between the decks, both decks' windows translucent so the staircase
reads as it climbs from the open rear platform past the first windows, a
sliver of the front face (grille, lamps, blank destination blind) turned to
the viewer. Sage plate with a soft city skyline. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420; road surface on y=668."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Double-Decker Bus — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
GY = 668
INK = "#2E1A18"
DOWN = -90                    # linear gradient angle: first stop at the top

def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

def chord(y):
    h = math.sqrt(PR**2 - (y - PCY)**2)
    return PCX - h, PCX + h

def _stops(stops):
    return [dict(offset=s[0], color=s[1], **({"opacity": s[2]} if len(s) > 2 else {})) for s in stops]

def lin(stops, angle=None):
    g = {"kind": "linear", "stops": _stops(stops)}
    if angle is not None:
        g["angle"] = angle
    return {"gradient": g}

def rad(stops):
    return {"gradient": {"kind": "radial", "stops": _stops(stops)}}

def rect(name, x, y, w, h, **kw):
    return d.shape("rectangle", name, x=round(x, 1), y=round(y, 1), width=round(w, 1), height=round(h, 1), **kw)

def ell(name, cx, cy, rx, ry, **kw):
    return d.shape("ellipse", name, x=round(cx - rx, 1), y=round(cy - ry, 1),
                   width=round(2 * rx, 1), height=round(2 * ry, 1), **kw)

def line(name, x0, y0, x1, y1, w, color, **kw):
    return d.path(f"M{x0:.1f},{y0:.1f} L{x1:.1f},{y1:.1f}", name, fill=NONE, stroke=color,
                  strokeWidth=w, cap="round", **kw)

def poly(name, pts, **kw):
    return d.path("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z", name, **kw)

RED = lin([(0, "#E8604A"), (0.4, "#C83A2C"), (1, "#7A1A16")], DOWN)
RED_FACE = lin([(0, "#C44A38"), (0.5, "#A02C22"), (1, "#5E1412")], DOWN)
CREAM = lin([(0, "#FFF6DE"), (0.55, "#F0DEB4"), (1, "#C8AE84")], DOWN)
CHROME = lin([(0, "#FFFFFF"), (0.35, "#C8CCD0"), (0.6, "#7A8088"), (1, "#E0E4E8")], DOWN)
DARK = lin([(0, "#3E3436"), (1, "#141012")], DOWN)
INTERIOR = lin([(0, "#7A5040"), (0.6, "#5A3428"), (1, "#3A2018")], DOWN)
GLASS = lin([(0, "#E8F4F2", 0.55), (0.45, "#B8D8D4", 0.28), (1, "#8AB0AC", 0.38)], DOWN)
WOOD = lin([(0, "#D8A060"), (1, "#8A5428")], DOWN)

# --- backdrop + plate ------------------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin([(0, "#16201E"), (1, "#070B0A")], DOWN), stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880, fill="#9CC8BC", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=lin([(0, "#6E9C94"), (0.45, "#A8CABE"), (0.75, "#E4DEC4"), (1, "#C8B898")], DOWN),
        stroke="#1E3430", strokeWidth=6)
d.shape("ellipse", "Plate vignette", x=80, y=40, width=840, height=840,
        fill=rad([(0, "#000000", 0), (0.78, "#000000", 0), (1, "#10201C", 0.45)]), stroke=NONE)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F2F6EC", strokeWidth=3, opacity=45)
ell("Sun haze", 690, 210, 130, 130, fill=rad([(0, "#FFF8E4", 0.75), (1, "#FFF8E4", 0)]), stroke=NONE)
for i, (cx, cy, rx, ry, op) in enumerate([(340, 180, 100, 28, 40), (420, 156, 80, 24, 34), (640, 300, 120, 24, 30),
                                          (210, 290, 70, 18, 26), (780, 360, 70, 16, 24)]):
    for k in range(16):
        a = k / 16 * 2 * math.pi
        assert on_disc(cx + rx * math.cos(a), cy + ry * math.sin(a), 10), i
    ell(f"Cloud {i+1}", cx, cy, rx, ry, fill=rad([(0, "#FFFFFF", 0.95), (1, "#FFFFFF", 0)]), stroke=NONE, opacity=op)

# --- skyline: a clock tower, a dome, terraces ------------------------------------------------------
L0, R0 = chord(GY)
sky = [(L0, GY), (150, 600), (150, 540), (200, 540), (200, 520), (236, 500), (272, 520), (272, 470), (300, 470),
       (300, 330), (308, 316), (316, 300), (324, 316), (332, 330), (332, 470), (380, 470), (380, 510), (430, 510),
       (430, 486), (470, 486), (470, 440)]
dome = [(470 + 60 * (1 - math.cos(t)), 440 - 60 * math.sin(t)) for t in [k / 12 * math.pi for k in range(13)]]
sky += dome + [(590, 486), (640, 486), (640, 452), (690, 452), (690, 500), (740, 500), (740, 470), (790, 470),
               (790, 530), (848, 530), (848, 590), (R0, GY)]
for x, y in sky[1:-1]:
    assert on_disc(x, y, 8), (x, y)
d.path("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in sky) + " Z", "Skyline",
       fill=lin([(0, "#7E9E98", 0.55), (1, "#5E7C78", 0.7)], DOWN), stroke=NONE)
ell("Clock face", 316, 352, 9, 9, fill=rad([(0, "#FFF6DC", 0.9), (1, "#E8D8B0", 0.6)]), stroke=NONE)
line("Clock hand", 316, 352, 316, 346, 1.6, "#5E7C78")
ell("Dome lantern", 530, 374, 6, 10, fill="#7E9E98", opacity=60, stroke=NONE)

# --- road, closing on the disc arc ------------------------------------------------------------------
rl, rr = chord(GY)
d.path(f"M{rl:.1f},{GY} L{rr:.1f},{GY} A420,420 0 0 1 {rl:.1f},{GY} Z", "Road",
       fill=lin([(0, "#6A6460"), (0.3, "#4A4442"), (1, "#221E1E")], DOWN), stroke=NONE)
ky = GY + 2
line("Kerb light", rl + 6, ky, rr - 6, ky, 3, "#D8D0C0", opacity=40)
for i, x in enumerate(range(206, 780, 70)):
    assert on_disc(x, 724, 10) and on_disc(x + 38, 730, 10)
    rect(f"Lane dash {i+1}", x, 722, 38, 6, fill=lin([(0, "#FFF4D8"), (1, "#D8C8A0")], DOWN), opacity=55,
         stroke=NONE)
for i, (y, op) in enumerate([(760, 14), (800, 10)]):
    l, r_ = chord(y)
    d.path(f"M{l + 40:.1f},{y} Q500,{y - 6} {r_ - 40:.1f},{y} Q500,{y + 5} {l + 40:.1f},{y} Z",
           f"Road sheen {i+1}", fill=lin([(0, "#E8F0EC", 0), (0.5, "#E8F0EC", 1), (1, "#E8F0EC", 0)]),
           stroke=NONE, opacity=op)
d.path(f"M200,{GY + 20} L780,{GY + 20} L760,{GY + 96} L220,{GY + 96} Z", "Bus reflection",
       fill=lin([(0, "#C83A2C", 0.4), (1, "#C83A2C", 0)], DOWN), stroke=NONE, opacity=45)
d.path(f"M168,{GY + 2} L806,{GY + 2} L780,{GY + 18} L196,{GY + 18} Z", "Bus shadow",
       fill=lin([(0, "#100A0A", 0), (0.12, "#100A0A", 1), (0.88, "#100A0A", 1), (1, "#100A0A", 0)]),
       stroke=NONE, opacity=40)

# --- bus geometry ------------------------------------------------------------------------------------
BX0, BX1 = 182, 746           # side panel
FX = 792                      # far edge of the front face
TOP = 344
UW0, UW1 = 380, 436           # upper windows
LW0, LW1 = 484, 552           # lower windows
SKIRT = 640
WR = 42
WHEELS = [300, 662]

# interior first: everything behind the glass
rect("Interior upper", BX0, UW0 - 4, BX1 - BX0, UW1 - UW0 + 8, fill=INTERIOR, stroke=NONE)
rect("Interior lower", BX0, LW0 - 4, BX1 - BX0, SKIRT - LW0 - 8, fill=INTERIOR, stroke=NONE)
rect("Platform back wall light", BX0 + 2, LW0, 66, 140, fill=rad([(0, "#FFD8A0", 0.5), (1, "#FFD8A0", 0)]),
     stroke=NONE)
# seats through the windows
for i in range(6):
    x = 262 + i * 80
    d.path(f"M{x + 10},{UW1 + 4} L{x + 10},{UW1 - 22} Q{x + 30},{UW1 - 30} {x + 48},{UW1 - 22} L{x + 48},{UW1 + 4} Z",
           f"Upper seat {i+1}", fill=lin([(0, "#B04A3A"), (1, "#6A2420")], DOWN), opacity=70, stroke=NONE)
for i in range(5):
    x = 336 + i * 78
    d.path(f"M{x + 8},{LW1 + 4} L{x + 8},{LW1 - 24} Q{x + 28},{LW1 - 32} {x + 46},{LW1 - 24} L{x + 46},{LW1 + 4} Z",
           f"Lower seat {i+1}", fill=lin([(0, "#B04A3A"), (1, "#6A2420")], DOWN), opacity=70, stroke=NONE)
# staircase: climbs forward from the platform floor to the upper deck
SX0, SY0, SX1, SY1, N = 194, 626, 304, UW0 + 16, 14
rise, run = (SY0 - SY1) / N, (SX1 - SX0) / N
pts = [(SX0, SY0)]
for k in range(N):
    x, y = SX0 + k * run, SY0 - k * rise
    pts += [(x, y - rise), (x + run, y - rise)]
pts += [(SX1, SY0)]
poly("Staircase", pts, fill=WOOD, stroke="#4A2A14", strokeWidth=2, opacity=88)
for k in range(N):
    x, y = SX0 + k * run, SY0 - (k + 1) * rise
    line(f"Stair nosing {k+1}", x, y, x + run, y, 3, "#F0C890", opacity=80)
d.path(f"M{SX0 + 2},{SY0 - 44} L{SX1 - 4},{SY1 - 30} Q{SX1 + 14},{SY1 - 34} {SX1 + 22},{SY1 - 14}",
       "Stair handrail", fill=NONE, stroke=CHROME, strokeWidth=4, cap="round")
for k in (1, 4, 7, 10, 13):
    x, y = SX0 + k * run + run / 2, SY0 - (k + 1) * rise
    line(f"Baluster {k}", x, y, x, y - 40, 3, CHROME, opacity=85)
# a passenger's shadow climbing, seen through the upper glass
ell("Climber head", SX0 + 10 * run + 8, SY0 - 11 * rise - 46, 7, 8, fill="#3A2018", opacity=45, stroke=NONE)
d.path(f"M{SX0 + 10 * run - 4},{SY0 - 11 * rise} L{SX0 + 10 * run},{SY0 - 11 * rise - 36} "
       f"Q{SX0 + 10 * run + 8},{SY0 - 11 * rise - 42} {SX0 + 10 * run + 16},{SY0 - 11 * rise - 36} "
       f"L{SX0 + 10 * run + 18},{SY0 - 11 * rise} Z", "Climber body", fill="#3A2018", opacity=40, stroke=NONE)

# --- body pieces around the windows --------------------------------------------------------------------
d.path(f"M{BX0},{UW0} L{BX0},{TOP + 26} Q{BX0},{TOP} {BX0 + 28},{TOP} L{BX1 - 10},{TOP} Q{BX1},{TOP} {BX1},{TOP + 10} "
       f"L{BX1},{UW0} Z", "Roof dome", fill=RED, stroke=INK, strokeWidth=3)
line("Roof sheen", BX0 + 30, TOP + 9, BX1 - 16, TOP + 9, 4, "#FFFFFF", opacity=30)
rect("Rain strip", BX0 + 6, UW0 - 10, BX1 - BX0 - 6, 4, fill=CHROME, stroke=NONE, opacity=70)
# upper pillars
up_x = [BX0 + 4, 252] + [252 + 80 * k for k in range(1, 7)]
for i, x in enumerate([BX0] + [252 + 80 * k - 10 for k in range(0, 7)]):
    w = 10 if i else 8
    rect(f"Upper pillar {i+1}", x, UW0, w, UW1 - UW0, fill=RED, stroke=NONE)
rect("Upper pillar front", BX1 - 6, UW0, 6, UW1 - UW0, fill=RED, stroke=NONE)
rect("Between-deck red", BX0, UW1, BX1 - BX0, 10, fill=RED, stroke=NONE)
rect("Cream band", BX0, UW1 + 10, BX1 - BX0, 26, fill=CREAM, stroke=INK, strokeWidth=1.5)
line("Cream band sheen", BX0 + 4, UW1 + 15, BX1 - 4, UW1 + 15, 2.5, "#FFFFFF", opacity=55)
rect("Lower header", BX0 + 70, UW1 + 36, BX1 - BX0 - 70, LW0 - UW1 - 36, fill=RED, stroke=NONE)
# route box: blank, lit
rect("Side route box", 400, UW1 + 38, 96, 10, fill=lin([(0, "#FFF8E0", 0.95), (1, "#E8D8A8", 0.8)], DOWN),
     stroke=INK, strokeWidth=1.5, radius=2)
# lower pillars and cab
for i, x in enumerate([326 + 78 * k for k in range(0, 5)]):
    rect(f"Lower pillar {i+1}", x, LW0, 10, LW1 - LW0, fill=RED, stroke=NONE)
rect("Platform bulkhead", 248, LW0 - 6, 12, SKIRT - LW0 + 6, fill=RED, stroke=NONE)
rect("Saloon front bulkhead", 716, LW0, 30, LW1 - LW0, fill=RED, stroke=NONE)
rect("Lower panel", 248, LW1, BX1 - 248, SKIRT - LW1, fill=RED, stroke=INK, strokeWidth=2)
rect("Rear corner post", BX0, LW0 - 6, 6, SKIRT - LW0 + 6, fill=RED, stroke=NONE)
rect("Platform skirt", BX0, SKIRT - 14, 66, 14, fill=RED, stroke=NONE)
line("Body outline rear", BX0, TOP + 26, BX0, SKIRT, 3, INK)
line("Body outline front", BX1, TOP + 10, BX1, SKIRT, 3, INK)
d.shape("rectangle", "Lower panel lining", x=262, y=LW1 + 14, width=BX1 - 278, height=36, radius=6,
        fill=NONE, stroke="#F4D8A0", strokeWidth=2.5, opacity=55)
line("Lower panel sheen", 270, LW1 + 8, BX1 - 14, LW1 + 8, 3, "#FFFFFF", opacity=22)
rect("Lower panel shade", 248, SKIRT - 22, BX1 - 248, 22, fill="#2A0606", opacity=28, stroke=NONE)
rect("Skirt chrome", BX0, SKIRT - 3, BX1 - BX0, 5, fill=CHROME, stroke=NONE)

# open rear platform: floor, step, grab pole
rect("Platform floor", BX0 - 6, SKIRT - 16, 72, 8, fill=lin([(0, "#8A7A70"), (1, "#3A302C")], DOWN), stroke=INK,
     strokeWidth=1.5)
rect("Platform step", BX0 - 10, SKIRT + 4, 66, 7, fill=CHROME, stroke=INK, strokeWidth=1.5)
line("Grab pole", 218, LW0 - 4, 218, SKIRT - 16, 5.5, CHROME)
line("Grab pole glint", 216.5, LW0 + 6, 216.5, SKIRT - 30, 1.6, "#FFFFFF", opacity=80)
ell("Tail lamp", BX0 + 4, 600, 4, 7, fill=rad([(0, "#FFB0A0"), (1, "#C02A20")]), stroke=INK, strokeWidth=1.2)

# glazing over everything behind it
rect("Rear upper glass", BX0 + 8, UW0, 62, UW1 - UW0, fill=GLASS, stroke="#5A1A14", strokeWidth=2, radius=6)
for i in range(6):
    rect(f"Upper glass {i+1}", 262 + 80 * i, UW0, 70, UW1 - UW0, fill=GLASS, stroke="#5A1A14", strokeWidth=2, radius=6)
    line(f"Upper glass {i+1} glint", 268 + 80 * i, UW1 - 14, 290 + 80 * i, UW0 + 6, 3, "#FFFFFF", opacity=40)
for i in range(5):
    x = 260 + 78 * i if i == 0 else 336 + 78 * (i - 1)
for i, x in enumerate([260] + [336 + 78 * k for k in range(4)] + [648]):
    w = 66 if i < 5 else 68
    rect(f"Lower glass {i+1}", x, LW0, w, LW1 - LW0, fill=GLASS, stroke="#5A1A14", strokeWidth=2, radius=6)
    line(f"Lower glass {i+1} glint", x + 6, LW1 - 12, x + 26, LW0 + 6, 3, "#FFFFFF", opacity=38)
rect("Cab door glass", 724, LW0 + 4, 18, LW1 - LW0 - 8, fill=GLASS, stroke="#5A1A14", strokeWidth=1.5, radius=3)

# --- front face, turned toward the viewer ---------------------------------------------------------------
def fy(y, t):
    """y on the front face at fraction t across it (receding top edge)."""
    return y + t * (8 if y < 500 else 2)
poly("Front face", [(BX1, TOP + 10), (FX - 6, fy(TOP + 10, 1) + 4), (FX, fy(TOP + 22, 1)), (FX, SKIRT + 2),
                    (BX1, SKIRT)], fill=RED_FACE, stroke=INK, strokeWidth=3)
poly("Destination box", [(BX1 + 6, TOP + 18), (FX - 6, fy(TOP + 18, 1) + 2), (FX - 6, fy(UW0 - 4, 1)),
                         (BX1 + 6, UW0 - 4)], fill=DARK, stroke=INK, strokeWidth=1.5)
poly("Destination blind", [(BX1 + 9, TOP + 22), (FX - 9, fy(TOP + 22, 1) + 2), (FX - 9, fy(UW0 - 8, 1)),
                           (BX1 + 9, UW0 - 8)], fill=lin([(0, "#FFF8E0", 0.95), (1, "#E8D8A8", 0.85)], DOWN),
     stroke=NONE)
poly("Front upper window", [(BX1 + 6, UW0 + 2), (FX - 6, fy(UW0 + 2, 1)), (FX - 6, fy(UW1 - 2, 1)),
                            (BX1 + 6, UW1 - 2)], fill=INTERIOR, stroke=NONE)
poly("Front upper glass", [(BX1 + 6, UW0 + 2), (FX - 6, fy(UW0 + 2, 1)), (FX - 6, fy(UW1 - 2, 1)),
                           (BX1 + 6, UW1 - 2)], fill=GLASS, stroke="#5A1A14", strokeWidth=2)
poly("Front cream band", [(BX1, UW1 + 10), (FX, fy(UW1 + 10, 1)), (FX, fy(UW1 + 36, 1)), (BX1, UW1 + 36)],
     fill=CREAM, stroke=INK, strokeWidth=1.5)
poly("Windscreen interior", [(BX1 + 6, LW0), (FX - 6, fy(LW0, 1)), (FX - 6, fy(LW1, 1)), (BX1 + 6, LW1)],
     fill=INTERIOR, stroke=NONE)
poly("Windscreen", [(BX1 + 6, LW0), (FX - 6, fy(LW0, 1)), (FX - 6, fy(LW1, 1)), (BX1 + 6, LW1)],
     fill=GLASS, stroke="#5A1A14", strokeWidth=2)
line("Windscreen glint", BX1 + 12, LW1 - 10, BX1 + 30, LW0 + 8, 3, "#FFFFFF", opacity=45)
# radiator grille + lamps
poly("Grille", [(BX1 + 10, 566), (FX - 10, 567), (FX - 10, 626), (BX1 + 10, 626)],
     fill=lin([(0, "#E8ECEE"), (0.5, "#8A9096"), (1, "#3A3E42")], DOWN), stroke=INK, strokeWidth=2)
for k in range(1, 6):
    x = BX1 + 10 + k * (FX - BX1 - 20) / 6
    line(f"Grille bar {k}", x, 569, x, 623, 3, "#2A2E32", opacity=70)
ell("Headlamp", BX1 + 4, 600, 9, 11, fill=rad([(0, "#FFFFF0"), (0.6, "#F4E8B8"), (1, "#A89A70")]),
    stroke=CHROME, strokeWidth=3)
ell("Headlamp far", FX - 2, 600, 5, 10, fill=rad([(0, "#FFFFF0"), (1, "#A89A70")]), stroke=CHROME, strokeWidth=2)
rect("Bumper", BX1 - 4, SKIRT - 4, FX - BX1 + 8, 9, fill=CHROME, stroke=INK, strokeWidth=1.5, radius=3)
line("Front face shade", FX - 3, TOP + 30, FX - 3, SKIRT - 4, 4, "#2A0606", opacity=30)
# wipers
line("Wiper", BX1 + 14, LW1 - 4, BX1 + 30, LW0 + 22, 3, "#2A2224", opacity=80)

# --- wheels -------------------------------------------------------------------------------------------------
for i, x in enumerate(WHEELS):
    cy = GY - WR
    d.path(f"M{x - WR - 8},{SKIRT} A{WR + 8},{WR + 8} 0 0 1 {x + WR + 8},{SKIRT} Z", f"Wheel arch {i+1}",
           fill=lin([(0, "#1A1010"), (1, "#3A2826")], DOWN), stroke=INK, strokeWidth=2)
    ell(f"Tyre {i+1}", x, cy, WR, WR, fill=rad([(0, "#5A5254"), (0.75, "#2E2828"), (1, "#141010")]),
        stroke=INK, strokeWidth=2.5)
    ell(f"Wheel disc {i+1}", x, cy, WR * 0.62, WR * 0.62, fill=rad([(0, "#E4D8C0"), (0.7, "#B0A088"), (1, "#5E5444")]),
        stroke="#2A2224", strokeWidth=2)
    for k in range(8):
        a = k / 8 * 2 * math.pi
        ell(f"Wheel {i+1} nut {k+1}", x + WR * 0.4 * math.cos(a), cy + WR * 0.4 * math.sin(a), 2.6, 2.6,
            fill="#4A4038", opacity=80, stroke=NONE)
    ell(f"Hub {i+1}", x, cy, WR * 0.22, WR * 0.22, fill=rad([(0, "#FFFFFF"), (0.5, "#C8CCD0"), (1, "#6A7078")]),
        stroke=INK, strokeWidth=1.5)
    d.path(f"M{x - WR*0.9:.1f},{cy - 8:.1f} A{WR*0.92:.1f},{WR*0.92:.1f} 0 0 1 {x - 8:.1f},{cy - WR*0.9:.1f}",
           f"Tyre {i+1} glint", fill=NONE, stroke="#FFFFFF", strokeWidth=2.5, opacity=28, cap="round")

for x, y in [(BX0 - 10, SKIRT + 11), (BX0, TOP + 10), (BX0 + 28, TOP), (FX, fy(TOP + 22, 1)), (FX + 4, SKIRT + 4),
             (BX1 + 10, TOP)]:
    assert on_disc(x, y, 10), (x, y)

# --- name -------------------------------------------------------------------------------------------------
d.text("DOUBLE-DECKER BUS", "Name", x=500, y=940, size=48, font="Virelai Sans", color="#F4ECD8", justify="center")
LINE2, SZ2, TRK = "1956 · 9.6-LITRE DIESEL", 22, 200
r = d.text(LINE2, "Second line", x=500, y=975, size=SZ2, font="Virelai Sans", color="#B8CCC0", justify="center")
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

d.finish("double-decker-bus-V1R00")
