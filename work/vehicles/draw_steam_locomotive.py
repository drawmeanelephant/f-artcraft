#!/usr/bin/env python3
"""Steam locomotive — field plate V1R00. Side profile of a 4-6-2 Pacific with
its tender, moving right along a chord of the disc: boiler, chimney and domes
along the top, three spoked drivers with the rods caught mid-stroke, and a
translucent steam plume trailing back across the upper plate into a dusk sun.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420; rail head on the chord y=640."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Steam Locomotive — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
GY = 640                      # rail head
S = 0.715                     # locomotive drawn in local units, ground at y=0
OX = 140.7
INK = "#2A1A16"

def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

def lin(stops, angle=None):
    g = {"kind": "linear", "stops": [dict(offset=s[0], color=s[1], **({"opacity": s[2]} if len(s) > 2 else {}))
                                     for s in stops]}
    if angle is not None:
        g["angle"] = angle
    return {"gradient": g}

def rad(stops):
    return {"gradient": {"kind": "radial", "stops": [
        dict(offset=s[0], color=s[1], **({"opacity": s[2]} if len(s) > 2 else {})) for s in stops]}}

def X(x): return OX + S * x
def Y(y): return GY + S * y

def pth(cmds):
    out = []
    for c in cmds:
        op, v = c[0], c[1:]
        if op == "Z":
            out.append("Z"); continue
        pts = " ".join(f"{X(v[i]):.1f},{Y(v[i+1]):.1f}" for i in range(0, len(v), 2))
        out.append(f"{op}{pts}")
    return " ".join(out)

def poly(name, pts, **kw):
    return d.path(pth([("M",) + pts[0]] + [("L",) + q for q in pts[1:]] + [("Z",)]), name, **kw)

def rect(name, x0, y0, x1, y1, **kw):
    return d.shape("rectangle", name, x=round(X(min(x0, x1)), 1), y=round(Y(min(y0, y1)), 1),
                   width=round(S * abs(x1 - x0), 1), height=round(S * abs(y1 - y0), 1), **kw)

def ell(name, cx, cy, rx, ry, **kw):
    return d.shape("ellipse", name, x=round(X(cx - rx), 1), y=round(Y(cy - ry), 1),
                   width=round(2 * rx * S, 1), height=round(2 * ry * S, 1), **kw)

def line(name, x0, y0, x1, y1, w, color, **kw):
    return d.path(pth([("M", x0, y0), ("L", x1, y1)]), name, fill=NONE, stroke=color,
                  strokeWidth=w, cap="round", **kw)

GREEN = lin([(0, "#5E8A5A"), (0.22, "#3F6E46"), (0.7, "#24452C"), (1, "#15291A")], 90)
GREEN_DK = lin([(0, "#335A3A"), (1, "#122216")], 90)
SMOKE_BOX = lin([(0, "#4A3C38"), (0.35, "#2E2422"), (1, "#16100F")], 90)
BRASS = lin([(0, "#FFF0B8"), (0.4, "#E0B45A"), (1, "#8A6224")], 90)
BRASS_R = rad([(0, "#FFF2C0"), (0.6, "#D8A84E"), (1, "#7A5420")])
CRIMSON = rad([(0, "#C8503A"), (0.7, "#962E22"), (1, "#5E1812")])
CRIMSON_L = lin([(0, "#C24A34"), (1, "#6A1C14")], 90)
STEEL = lin([(0, "#E4DED8"), (0.45, "#A49A94"), (1, "#5A504C")], 90)
TIRE = rad([(0, "#6A5A54"), (0.85, "#3E322E"), (1, "#221A18")])
COAL = lin([(0, "#3E3634"), (1, "#141010")], 90)
GLASS = rad([(0, "#FFD27A", 0.85), (1, "#E07A34", 0.55)])

# --- backdrop + plate -------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin([(0, "#22161A"), (1, "#0B0708")], 90), stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880, fill="#F2B870", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad([(0, "#FBE0A6"), (0.45, "#F0B677"), (0.8, "#D47E52"), (1, "#8E3E36")]),
        stroke="#4A2220", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#FFE6BC", strokeWidth=3, opacity=45)

# dusk sun, low and behind the plume
d.shape("ellipse", "Sun glow", x=200, y=210, width=260, height=260,
        fill=rad([(0, "#FFF4D0", 0.55), (1, "#FFD08A", 0)]), stroke=NONE)
d.shape("ellipse", "Sun", x=270, y=280, width=120, height=120,
        fill=rad([(0, "#FFFBEA"), (0.7, "#FFE6A8"), (1, "#F8C278")]), stroke=NONE, opacity=85)

# distant hills on the horizon chord
hc = math.sqrt(PR**2 - (GY - PCY)**2)
HL, HR = PCX - hc, PCX + hc
hills = (f"M{HL:.1f},{GY} C200,606 262,574 330,588 C400,602 452,556 540,566 "
         f"C622,576 700,596 762,584 C822,574 858,606 {HR:.1f},{GY} Z")
for x, y in [(200, 606), (262, 574), (858, 606), (822, 574)]:
    assert on_disc(x, y, 10)
d.path(hills, "Far hills", fill=lin([(0, "#B0605A", 0.55), (1, "#7E3C3E", 0.75)], 90), stroke=NONE)
d.path(f"M{HL:.1f},{GY} C230,622 300,604 380,612 C470,622 560,600 650,610 "
       f"C740,620 820,612 {HR:.1f},{GY} Z", "Near hills",
       fill=lin([(0, "#7A3A3A", 0.6), (1, "#4E2428", 0.85)], 90), stroke=NONE)

# --- ground: meadow, then the ballast embankment, both closing on the disc arc ---------
def chord(y):
    h = math.sqrt(PR**2 - (y - PCY)**2)
    return PCX - h, PCX + h
by, ey = GY + 6, GY + 40
bl, br = chord(by)
el, er = chord(ey)
d.path(f"M{bl:.1f},{by} L{br:.1f},{by} A420,420 0 0 1 {bl:.1f},{by} Z", "Meadow",
       fill=lin([(0, "#9A5E3E"), (0.35, "#6E4030"), (1, "#2E1A1A")], 90), stroke=NONE)
for i, (y, op) in enumerate([(700, 22), (742, 16), (790, 11)]):
    l, r_ = chord(y)
    d.path(f"M{l + 40:.1f},{y} Q500,{y - 8} {r_ - 40:.1f},{y} Q500,{y + 6} {l + 40:.1f},{y} Z",
           f"Field light {i+1}", fill=lin([(0, "#FFD8A0", 0), (0.5, "#FFD8A0", 1), (1, "#FFD8A0", 0)]),
           stroke=NONE, opacity=op)
for i, (x, y) in enumerate([(190, 712), (262, 760), (338, 708), (420, 784), (560, 770), (640, 716),
                            (720, 774), (800, 712), (470, 728), (340, 816), (660, 820), (500, 846)]):
    assert on_disc(x, y, 16), (x, y)
    d.path(f"M{x-7},{y} Q{x-5},{y-9} {x-9},{y-16} M{x},{y} Q{x+1},{y-12} {x-1},{y-20} M{x+7},{y} Q{x+6},{y-9} {x+10},{y-15}",
           f"Grass tuft {i+1}", fill=NONE, stroke="#C88A5A", strokeWidth=3, opacity=45, cap="round")
d.path(f"M{bl:.1f},{by} L{br:.1f},{by} A420,420 0 0 1 {er:.1f},{ey} L{el:.1f},{ey} "
       f"A420,420 0 0 1 {bl:.1f},{by} Z", "Ballast",
       fill=lin([(0, "#8A6656"), (0.5, "#5E4238"), (1, "#3A2824")], 90), stroke=NONE)
d.path(f"M{bl + 30:.1f},{GY + 10} L{br - 30:.1f},{GY + 10} L{br - 60:.1f},{GY + 22} L{bl + 60:.1f},{GY + 22} Z",
       "Train shadow", fill=lin([(0, "#1A0E0E", 0), (0.15, "#1A0E0E", 1), (0.85, "#1A0E0E", 1),
                                 (1, "#1A0E0E", 0)]), stroke=NONE, opacity=35)
for i, x in enumerate(range(146, 845, 33)):
    x0, x1 = x, x + 22
    assert on_disc(x0, GY + 20, 4) and on_disc(x1, GY + 20, 4), x
    d.shape("rectangle", f"Sleeper {i+1}", x=x0, y=GY + 5, width=22, height=12,
            fill=lin([(0, "#5A3E30"), (1, "#2E1E18")], 90), stroke=NONE, opacity=80)
for i, (x, y, w) in enumerate([(200, 666, 6), (300, 672, 5), (420, 662, 7), (520, 676, 5), (640, 664, 6),
                               (740, 670, 5), (360, 674, 6), (600, 668, 5), (480, 670, 6), (250, 676, 4),
                               (690, 676, 5), (800, 664, 4)]):
    assert on_disc(x, y, 12)
    d.shape("ellipse", f"Ballast stone {i+1}", x=x, y=y, width=w, height=w * 0.7,
            fill="#C89A80", opacity=30, stroke=NONE)
rx0, rx1 = 128, 872
assert on_disc(rx0, GY + 7, 2) and on_disc(rx1, GY + 7, 2)
d.shape("rectangle", "Rail", x=rx0, y=GY, width=rx1 - rx0, height=7,
        fill=lin([(0, "#F2E6DA"), (0.4, "#A8968C"), (1, "#4A3A34")], 90), stroke=NONE)

# --- steam plume (behind the locomotive) ------------------------------------------------
CHX, CHY = X(842), Y(-342)
puffs = [(CHX + 4, CHY - 14, 30, 22, 80), (CHX - 8, CHY - 46, 42, 32, 78), (CHX - 38, CHY - 86, 58, 42, 74),
         (CHX - 84, CHY - 126, 72, 50, 70), (CHX - 146, CHY - 160, 84, 56, 66), (CHX - 214, CHY - 186, 94, 60, 60),
         (CHX - 292, CHY - 202, 98, 60, 54), (CHX - 372, CHY - 206, 92, 56, 46), (CHX - 432, CHY - 196, 78, 48, 38),
         (CHX - 490, CHY - 164, 56, 36, 30)]
for i, (cx, cy, rx, ry, op) in enumerate(puffs):
    for k in range(24):
        a = k / 24 * 2 * math.pi
        assert on_disc(cx + rx * math.cos(a), cy + ry * math.sin(a), 12), (i, cx, cy)
    d.shape("ellipse", f"Steam {i+1} shadow", x=round(cx - rx + rx * 0.18, 1), y=round(cy - ry + ry * 0.3, 1),
            width=round(2 * rx, 1), height=round(2 * ry, 1),
            fill=rad([(0, "#9A8A88", 0.5), (1, "#7A6460", 0)]), stroke=NONE, opacity=op)
    d.shape("ellipse", f"Steam {i+1}", x=round(cx - rx, 1), y=round(cy - ry, 1), width=round(2 * rx, 1),
            height=round(2 * ry, 1),
            fill=rad([(0, "#FFFFFF", 0.95), (0.6, "#F4ECE6", 0.75), (1, "#E2D2CC", 0.1)]),
            stroke=NONE, opacity=op)
    d.shape("ellipse", f"Steam {i+1} light", x=round(cx - rx * 0.7, 1), y=round(cy - ry * 0.8, 1),
            width=round(rx * 0.9, 1), height=round(ry * 0.7, 1), fill="#FFFFFF", opacity=round(op * 0.35),
            stroke=NONE)

# --- wheels ------------------------------------------------------------------------------
CRANK = math.radians(40)       # crank pins down-and-forward: rods mid-stroke

def wheel(name, cx, cy, R, spokes, crank=None, cw=False):
    ax, ay, r = X(cx), Y(cy), R * S
    d.shape("ellipse", f"{name} tyre", x=round(ax - r, 1), y=round(ay - r, 1), width=round(2 * r, 1),
            height=round(2 * r, 1), fill=TIRE, stroke=INK, strokeWidth=2.5)
    ri = r * 0.84
    d.shape("ellipse", f"{name} well", x=round(ax - ri, 1), y=round(ay - ri, 1), width=round(2 * ri, 1),
            height=round(2 * ri, 1), fill=rad([(0, "#3A1E1A", 0.85), (1, "#1E1010", 0.7)]), stroke=NONE)
    sw = max(3.2, r * 0.075)
    for k in range(spokes):
        a = k / spokes * 2 * math.pi + 0.1
        d.path(f"M{ax + r*0.2*math.cos(a):.1f},{ay + r*0.2*math.sin(a):.1f} "
               f"L{ax + ri*math.cos(a):.1f},{ay + ri*math.sin(a):.1f}",
               f"{name} spoke {k+1}", fill=NONE, stroke="#A83826", strokeWidth=sw, cap="round")
    if cw and crank is not None:
        phi = crank + math.pi
        outer = [(ax + ri * math.cos(phi + t), ay + ri * math.sin(phi + t))
                 for t in [math.radians(v) for v in range(-55, 56, 10)]]
        inner = [(ax + ri * 0.55 * math.cos(phi + t), ay + ri * 0.55 * math.sin(phi + t))
                 for t in [math.radians(v) for v in range(45, -46, -15)]]
        pts = outer + inner
        d.path("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z", f"{name} counterweight",
               fill=CRIMSON, stroke="#4A1410", strokeWidth=1.5, opacity=95)
    d.shape("ellipse", f"{name} rim", x=round(ax - ri, 1), y=round(ay - ri, 1), width=round(2 * ri, 1),
            height=round(2 * ri, 1), fill=NONE, stroke=CRIMSON_L, strokeWidth=max(3.5, r * 0.09))
    hb = r * 0.26
    d.shape("ellipse", f"{name} hub", x=round(ax - hb, 1), y=round(ay - hb, 1), width=round(2 * hb, 1),
            height=round(2 * hb, 1), fill=CRIMSON, stroke="#4A1410", strokeWidth=1.5)
    hc_ = r * 0.1
    d.shape("ellipse", f"{name} axle cap", x=round(ax - hc_, 1), y=round(ay - hc_, 1), width=round(2 * hc_, 1),
            height=round(2 * hc_, 1), fill=BRASS_R, stroke=NONE)
    d.path(f"M{ax - r*0.92:.1f},{ay - r*0.12:.1f} A{r*0.93:.1f},{r*0.93:.1f} 0 0 1 {ax - r*0.12:.1f},{ay - r*0.92:.1f}",
           f"{name} tyre glint", fill=NONE, stroke="#FFFFFF", strokeWidth=2.5, opacity=30, cap="round")

# frames visible between the wheels
rect("Main frames", 330, -150, 900, -78, fill=lin([(0, "#2C2220"), (1, "#140E0D")], 90), stroke=NONE)
rect("Tender frame", 8, -76, 200, -50, fill=lin([(0, "#2C2220"), (1, "#140E0D")], 90), stroke=NONE)

for i, x in enumerate([40, 105, 170]):
    rect(f"Tender axlebox {i+1}", x - 9, -56, x + 9, -38, fill=SMOKE_BOX, stroke=NONE)
    wheel(f"Tender wheel {i+1}", x, -30, 30, 10)
wheel("Trailing wheel", 270, -40, 40, 12)
for i, x in enumerate([850, 925]):
    wheel(f"Pony wheel {i+1}", x, -34, 34, 10)
DRIVERS = [400, 562, 724]
for i, x in enumerate(DRIVERS):
    wheel(f"Driver {i+1}", x, -75, 75, 16, crank=CRANK, cw=True)

# --- cylinder, motion, rods ----------------------------------------------------------------
CYL_Y = -97
rect("Cylinder", 825, -126, 948, -68, fill=lin([(0, "#5E8A5A"), (0.4, "#335A3A"), (1, "#14261A")], 90),
     stroke=INK, strokeWidth=2.5, radius=6)
for x in (836, 937):
    rect("Cylinder band", x - 3, -126, x + 3, -68, fill=BRASS, stroke=NONE)
rect("Steam chest", 832, -150, 942, -126, fill=GREEN_DK, stroke=INK, strokeWidth=2)
line("Guide bar top", 735, -109, 826, -109, 3.5, STEEL)
line("Guide bar bottom", 735, -85, 826, -85, 3.5, STEEL)

pins = [(x + 30 * math.cos(CRANK), -75 + 30 * math.sin(CRANK)) for x in DRIVERS]
mp = pins[1]
CHX_L = mp[0] + math.sqrt(230**2 - (CYL_Y - mp[1])**2)
line("Piston rod", CHX_L, CYL_Y, 828, CYL_Y, 4, STEEL)
rect("Crosshead", CHX_L - 13, CYL_Y - 11, CHX_L + 13, CYL_Y + 11, fill=STEEL, stroke=INK, strokeWidth=1.5)

def rod(name, a, b, w0, w1, fill):
    ux, uy = b[0] - a[0], b[1] - a[1]
    ln = math.hypot(ux, uy); nx, ny = -uy / ln, ux / ln
    pts = [(a[0] + nx * w0 / 2, a[1] + ny * w0 / 2), (b[0] + nx * w1 / 2, b[1] + ny * w1 / 2),
           (b[0] - nx * w1 / 2, b[1] - ny * w1 / 2), (a[0] - nx * w0 / 2, a[1] - ny * w0 / 2)]
    poly(name, pts, fill=fill, stroke=INK, strokeWidth=1.5)

# Walschaerts hint: eccentric rod, expansion link, radius rod
ecc = (mp[0] - 14, mp[1] - 20)
line("Eccentric rod", ecc[0], ecc[1], 690, -128, 4, STEEL)
d.path(pth([("M", 684, -146), ("Q", 694, -128, 684, -110)]), "Expansion link", fill=NONE,
       stroke=lin([(0, "#D8D0C8"), (1, "#6A5E58")], 90), strokeWidth=6, cap="round")
line("Radius rod", 690, -132, CHX_L - 6, -122, 4, STEEL)
line("Combination lever", CHX_L - 6, -122, CHX_L - 6, CYL_Y + 10, 4, STEEL)

rod("Coupling rod", (pins[0][0] - 8, pins[0][1]), (pins[2][0] + 8, pins[2][1]), 11, 11, STEEL)
rod("Main rod", (CHX_L, CYL_Y), mp, 12, 17, lin([(0, "#F0EAE4"), (0.5, "#B4AAA4"), (1, "#5E5450")], 90))
for i, (px, py) in enumerate(pins):
    ell(f"Crank pin {i+1}", px, py, 8, 8, fill=BRASS_R, stroke=INK, strokeWidth=1.5)

# --- tender ---------------------------------------------------------------------------------
d.path(pth([("M", 5, -70), ("L", 5, -238), ("Q", 5, -255, 22, -255), ("L", 205, -255), ("L", 205, -70), ("Z",)]),
       "Tender tank", fill=GREEN, stroke=INK, strokeWidth=3)
d.path(pth([("M", 26, -255), ("Q", 50, -280, 92, -276), ("Q", 140, -288, 196, -262), ("L", 196, -255), ("Z",)]),
       "Coal heap", fill=COAL, stroke=INK, strokeWidth=2)
for i, (x, y, r) in enumerate([(60, -268, 6), (96, -275, 7), (130, -276, 6), (166, -268, 5), (80, -262, 4)]):
    ell(f"Coal glint {i+1}", x, y, r, r * 0.6, fill="#8A8080", opacity=40, stroke=NONE)
d.shape("rectangle", "Tender lining", x=round(X(22), 1), y=round(Y(-238), 1), width=round(S * 166, 1),
        height=round(S * 150, 1), radius=8, fill=NONE, stroke="#E8C070", strokeWidth=3, opacity=75)
rect("Tender top sheen", 10, -250, 200, -236, fill="#FFFFFF", opacity=14, stroke=NONE)
rect("Tender lower shade", 6, -100, 204, -71, fill="#0A1A0E", opacity=30, stroke=NONE)
rect("Tender valance", 5, -76, 205, -66, fill=CRIMSON_L, stroke=INK, strokeWidth=1.5)
rect("Drawbar", 200, -66, 226, -56, fill=SMOKE_BOX, stroke=NONE)

# --- boiler, firebox, smokebox --------------------------------------------------------------------
rect("Boiler", 440, -275, 812, -160, fill=GREEN, stroke=INK, strokeWidth=3)
d.path(pth([("M", 345, -160), ("L", 345, -286), ("L", 420, -286), ("Q", 444, -286, 446, -262),
            ("L", 446, -160), ("Z",)]), "Firebox", fill=GREEN, stroke=INK, strokeWidth=3)
rect("Boiler top sheen", 350, -268, 808, -258, fill="#FFFFFF", opacity=22, stroke=NONE)
line("Boiler top glint", 360, -264, 790, -264, 3, "#FFFFFF", opacity=45)
rect("Boiler belly shade", 346, -188, 810, -161, fill="#08140A", opacity=35, stroke=NONE)
for i, x in enumerate([446, 560, 680, 800]):
    rect(f"Boiler band {i+1}", x - 4, -275, x + 4, -160, fill=BRASS, stroke=NONE, opacity=92)
# domes
d.path(pth([("M", 588, -275), ("C", 590, -310, 652, -310, 654, -275), ("Z",)]), "Steam dome",
       fill=BRASS, stroke=INK, strokeWidth=2.5)
d.path(pth([("M", 600, -296), ("Q", 614, -304, 628, -302)]), "Steam dome glint", fill=NONE,
       stroke="#FFFFFF", strokeWidth=3, opacity=60, cap="round")
d.path(pth([("M", 486, -275), ("C", 488, -302, 536, -302, 538, -275), ("Z",)]), "Sand dome",
       fill=GREEN, stroke=INK, strokeWidth=2.5)
rect("Safety valve", 392, -306, 406, -286, fill=BRASS, stroke=INK, strokeWidth=1.5)
rect("Safety valve cap", 388, -312, 410, -305, fill=BRASS, stroke=INK, strokeWidth=1.5)
line("Whistle", 362, -286, 362, -318, 4, BRASS)
ell("Whistle bell", 362, -320, 6, 9, fill=BRASS_R, stroke=INK, strokeWidth=1.2)
# a wisp off the safety valve
for i, (x, y, r, op) in enumerate([(398, -330, 12, 55), (388, -356, 17, 42), (370, -384, 22, 30)]):
    ell(f"Valve wisp {i+1}", x, y, r, r * 0.75, fill=rad([(0, "#FFFFFF", 0.9), (1, "#F2E6E0", 0)]),
        stroke=NONE, opacity=op)
# smokebox + chimney
rect("Smokebox", 806, -284, 886, -152, fill=SMOKE_BOX, stroke=INK, strokeWidth=3)
rect("Smokebox front ring", 880, -282, 894, -154, fill=lin([(0, "#5A4C48"), (1, "#1A1212")], 90),
     stroke=INK, strokeWidth=2, radius=4)
for i, y in enumerate(range(-272, -160, 14)):
    ell(f"Smokebox rivet {i+1}", 813, y, 2.6, 2.6, fill="#8A7C78", opacity=55, stroke=NONE)
rect("Smokebox sheen", 808, -278, 884, -268, fill="#FFFFFF", opacity=12, stroke=NONE)
d.path(pth([("M", 822, -284), ("L", 826, -330), ("L", 818, -336), ("L", 866, -336), ("L", 858, -330),
            ("L", 862, -284), ("Z",)]), "Chimney", fill=lin([(0, "#3A3230"), (0.5, "#2A2220"), (1, "#120C0C")]),
       stroke=INK, strokeWidth=2.5)
rect("Chimney lip sheen", 820, -336, 864, -331, fill="#FFFFFF", opacity=22, stroke=NONE)
line("Chimney glint", 832, -326, 834, -290, 3, "#FFFFFF", opacity=30)
# headlamp
rect("Headlamp", 868, -306, 892, -284, fill=SMOKE_BOX, stroke=INK, strokeWidth=1.5, radius=3)
ell("Headlamp lens", 888, -295, 6, 8, fill=rad([(0, "#FFFBE0"), (1, "#FFC860", 0.7)]), stroke=NONE)
ell("Headlamp glow", 892, -295, 18, 16, fill=rad([(0, "#FFF2C0", 0.6), (1, "#FFD890", 0)]), stroke=NONE)

# running board, valance, buffer beam, pilot
rect("Running board", 345, -162, 910, -152, fill=lin([(0, "#4A3E3A"), (1, "#1C1414")], 90), stroke=NONE)
line("Running board edge", 345, -151, 910, -151, 3, "#E0B45A", opacity=80)
rect("Valance", 345, -150, 910, -140, fill=CRIMSON_L, stroke=NONE)
rect("Buffer beam", 948, -152, 972, -112, fill=CRIMSON_L, stroke=INK, strokeWidth=2)
for i, y in enumerate([-142, -122]):
    rect(f"Buffer stock {i+1}", 972, y - 5, 984, y + 5, fill=SMOKE_BOX, stroke=NONE)
    ell(f"Buffer head {i+1}", 986, y, 4, 9, fill=STEEL, stroke=INK, strokeWidth=1.2)
poly("Pilot", [(952, -112), (978, -112), (1004, -8), (962, -8)],
     fill=lin([(0, "#3A302E"), (1, "#141010")], 90), stroke=INK, strokeWidth=2)
for i, t in enumerate([0.25, 0.5, 0.75]):
    line(f"Pilot bar {i+1}", 952 + 10 * t, -112 + 104 * t, 978 + 26 * t, -112 + 104 * t, 3, STEEL, opacity=70)

# --- cab ---------------------------------------------------------------------------------------
d.path(pth([("M", 220, -112), ("L", 220, -300), ("L", 346, -300), ("L", 346, -112), ("Q", 300, -96, 220, -112), ("Z",)]),
       "Cab side", fill=GREEN, stroke=INK, strokeWidth=3)
d.path(pth([("M", 208, -298), ("Q", 280, -326, 356, -298), ("L", 356, -292), ("L", 208, -292), ("Z",)]),
       "Cab roof", fill=SMOKE_BOX, stroke=INK, strokeWidth=2.5)
d.shape("rectangle", "Cab window", x=round(X(246), 1), y=round(Y(-276), 1), width=round(S * 78, 1),
        height=round(S * 62, 1), radius=8, fill=GLASS, stroke=BRASS, strokeWidth=3.5)
line("Cab window bar", 285, -276, 285, -214, 3, BRASS)
line("Cab window reflection", 254, -232, 274, -268, 3, "#FFFFFF", opacity=45)
d.shape("rectangle", "Cab lining", x=round(X(232), 1), y=round(Y(-196), 1), width=round(S * 102, 1),
        height=round(S * 72, 1), radius=6, fill=NONE, stroke="#E8C070", strokeWidth=3, opacity=75)
line("Cab handrail rear", 226, -122, 226, -272, 3.5, BRASS)
line("Cab handrail front", 340, -122, 340, -272, 3.5, BRASS)
rect("Cab top sheen", 222, -294, 344, -284, fill="#FFFFFF", opacity=14, stroke=NONE)
d.shape("ellipse", "Firebox glow", x=round(X(250), 1), y=round(Y(-236), 1), width=round(S * 70, 1),
        height=round(S * 34, 1), fill=rad([(0, "#FFE8A0", 0.7), (1, "#FF9A40", 0)]), stroke=NONE)

# --- name ----------------------------------------------------------------------------------------
d.text("STEAM LOCOMOTIVE", "Name", x=500, y=940, size=50, font="Virelai Sans", color="#F6E2C4", justify="center")
LINE2, SZ2, TRK = "1935 · 4-6-2 · COAL-FIRED STEAM", 22, 200
r = d.text(LINE2, "Second line", x=500, y=975, size=SZ2, font="Virelai Sans", color="#D49C74", justify="center")
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
# whole locomotive inside the disc
for (lx, ly) in [(5, -255), (5, -30), (1004, -8), (986, -151), (842, -336), (208, -298), (356, -298)]:
    assert on_disc(X(lx), Y(ly), 8), (lx, ly, X(lx), Y(ly))

d.finish("steam-locomotive-V1R00")
