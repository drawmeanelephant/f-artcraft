#!/usr/bin/env python3
"""Cargo bike — field plate V1R00. Profile, moving right: a long-john box
bike with the wooden cargo box slung low between the rider and the small
front wheel, a child-seat hoop over the box, chain drive and mudguards.
Brick-red plate. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Cargo Bike — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420
INK = "#2A1716"

def lin(angle, *stops):
    return {"gradient": {"kind": "linear", "angle": angle, "stops": [
        {"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial", "stops": [
        {"offset": o, "color": c} for o, c in stops]}}

def chord_x(y, r=R):
    dx = math.sqrt(max(r * r - (y - CY) ** 2, 0))
    return CX - dx, CX + dx

def arc_band(y, label, **kw):
    xl, xr = chord_x(y)
    d.path(f"M{xl:.1f},{y} L{xr:.1f},{y} A420,420 0 0 1 {xl:.1f},{y} Z", label, **kw)

def seg(a, b):
    return f"M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}"

FRAME = lin(-90, (0, "#4FA49A"), (0.5, "#1F6E66"), (1, "#0F403B"))
CHROME = lin(-90, (0, "#FFFFFF"), (0.45, "#A9B0B8"), (1, "#E4E8EC"))

def tube(name, a, b, w=11):
    d.path(seg(a, b), f"{name} ink", fill=NONE, stroke=INK, strokeWidth=w + 5, cap="round")
    d.path(seg(a, b), name, fill=NONE, stroke=FRAME, strokeWidth=w, cap="round")
    d.path(seg((a[0], a[1] - w * 0.2), (b[0], b[1] - w * 0.2)), f"{name} sheen", fill=NONE,
           stroke="#BFEDE6", strokeWidth=3, opacity=40, cap="round")

def wheel(name, cx, cy, r, spokes):
    d.shape("ellipse", f"{name} tyre", x=cx - r, y=cy - r, width=2 * r, height=2 * r,
            fill=NONE, stroke=lin(-90, (0, "#4A3C3A"), (1, "#1C1414")), strokeWidth=12)
    d.shape("ellipse", f"{name} tyre wall", x=cx - r + 3, y=cy - r + 3, width=2 * r - 6,
            height=2 * r - 6, fill=NONE, stroke="#8A7A70", strokeWidth=3, opacity=50)
    ri = r - 9
    d.shape("ellipse", f"{name} rim", x=cx - ri, y=cy - ri, width=2 * ri, height=2 * ri,
            fill=rad((0, "#F6E8DE"), (1, "#D9B8A6")), opacity=18, stroke=CHROME, strokeWidth=5)
    for k in range(spokes):
        a = math.radians(k * 360 / spokes + 7)
        hx, hy = cx + 7 * math.cos(a + 0.5), cy + 7 * math.sin(a + 0.5)
        ex, ey = cx + (ri - 2) * math.cos(a), cy + (ri - 2) * math.sin(a)
        d.path(seg((hx, hy), (ex, ey)), f"{name} spoke {k+1}", fill=NONE,
               stroke="#C9CFD5", strokeWidth=3, opacity=85, cap="round")
    d.shape("ellipse", f"{name} hub", x=cx - 12, y=cy - 12, width=24, height=24,
            fill=rad((0, "#FFFFFF"), (0.6, "#A9B0B8"), (1, "#5C636B")), stroke=INK, strokeWidth=3)

def mudguard(name, cx, cy, r, a0, a1):
    p0 = (cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0)))
    p1 = (cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1)))
    large = 1 if (a1 - a0) % 360 > 180 else 0
    dd = f"M{p0[0]:.1f},{p0[1]:.1f} A{r},{r} 0 {large} 1 {p1[0]:.1f},{p1[1]:.1f}"
    d.path(dd, f"{name} ink", fill=NONE, stroke=INK, strokeWidth=12, cap="round")
    d.path(dd, name, fill=NONE, stroke=lin(-90, (0, "#3E3432"), (1, "#151010")),
           strokeWidth=8, cap="round")
    d.path(dd, f"{name} sheen", fill=NONE, stroke="#FFFFFF", strokeWidth=3, opacity=30,
           cap="round")

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin(-90, (0, "#2E1A17"), (1, "#120A09")), stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#E39A80"), (0.65, "#B9553D"), (1, "#7F3021")),
        stroke="#5E2418", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F6C9B6", strokeWidth=3, opacity=45)
# faint brick coursing in the plate, kept well inside the ring
for row in range(6):
    y = 180 + row * 44
    xl, xr = chord_x(y, 360)
    d.path(f"M{xl:.0f},{y} L{xr:.0f},{y}", f"Brick course {row+1}", fill=NONE,
           stroke="#8E3A28", strokeWidth=3, opacity=18)
    off = 0 if row % 2 else 40
    x = 200 + off
    k = 0
    while x < 820:
        if xl + 10 < x < xr - 10:
            k += 1
            d.path(f"M{x},{y} L{x},{y+44}", f"Brick joint {row+1}.{k}", fill=NONE,
                   stroke="#8E3A28", strokeWidth=3, opacity=14)
        x += 80

GROUND = 690
arc_band(GROUND, "Street", fill=lin(-90, (0, "#6E3426"), (1, "#3E1A12")), stroke=NONE)
d.path(f"M{chord_x(GROUND)[0]:.0f},{GROUND} L{chord_x(GROUND)[1]:.0f},{GROUND}",
       "Kerb light", fill=NONE, stroke="#F2B8A2", strokeWidth=4, opacity=50)
for i, y in enumerate([724, 762, 804]):
    xl, xr = chord_x(y, 396)
    d.path(f"M{xl:.0f},{y} L{xr:.0f},{y}", f"Paving line {i+1}", fill=NONE,
           stroke="#2A100A", strokeWidth=3, opacity=35)
d.shape("ellipse", "Bike shadow", x=170, y=GROUND - 10, width=660, height=22,
        fill=rad((0, "#2A100A"), (1, "#6E3426")), opacity=55, stroke=NONE)

# --- geometry -------------------------------------------------------------------
RW = (262, 595); RR = 95       # rear wheel
FW = (744, 625); FR = 65       # small front wheel under the load
BB = (350, 612)                # bottom bracket
SEAT = (318, 446)
HT_TOP, HT_BOT = (430, 446), (446, 560)   # rider's steerer
FHT_TOP, FHT_BOT = (708, 506), (720, 566) # front head tube

# wheels and guards
mudguard("Rear mudguard", *RW, RR + 12, 185, 330)
wheel("Rear wheel", *RW, RR, 18)
mudguard("Front mudguard", *FW, FR + 12, 200, 340)
wheel("Front wheel", *FW, FR, 14)

# steering link rod under the box
d.path("M450,566 L466,656 L708,656 L722,600", "Steering rod", fill=NONE, stroke=CHROME,
       strokeWidth=4, cap="round")

# rear triangle + rack
tube("Chainstay", RW, BB, 9)
tube("Seat stay", RW, (322, 470), 8)
tube("Seat tube", BB, (320, 460), 12)
d.path(seg((182, 498), (312, 498)), "Rear rack", fill=NONE, stroke=CHROME, strokeWidth=6,
       cap="round")
d.path(seg((196, 498), (250, 590)), "Rack strut", fill=NONE, stroke=CHROME, strokeWidth=4,
       cap="round")

# main frame: top tube, steerer, long low beam to the front head tube
tube("Top tube", (322, 472), (436, 474), 11)
tube("Down tube", HT_BOT, (476, 640), 12)
tube("Beam to bracket", BB, (476, 640), 11)
tube("Cargo beam", (476, 640), (690, 640), 13)
tube("Front riser", (690, 640), FHT_BOT, 12)
tube("Rider head tube", HT_TOP, HT_BOT, 13)
tube("Front head tube", FHT_TOP, FHT_BOT, 13)
tube("Front fork", FHT_BOT, FW, 9)

# chain drive
d.shape("ellipse", "Chainring", x=BB[0] - 24, y=BB[1] - 24, width=48, height=48,
        fill=rad((0, "#E4E8EC"), (1, "#5C636B")), stroke=INK, strokeWidth=3)
d.path(f"M{BB[0]},{BB[1]-24} L{RW[0]},{RW[1]-11}", "Chain top", fill=NONE,
       stroke="#4A4442", strokeWidth=5, cap="round")
d.path(f"M{BB[0]},{BB[1]+24} L{RW[0]},{RW[1]+11}", "Chain bottom", fill=NONE,
       stroke="#4A4442", strokeWidth=5, cap="round")
for side, (a, b) in enumerate([((BB[0], BB[1] - 24), (RW[0], RW[1] - 11)),
                               ((BB[0], BB[1] + 24), (RW[0], RW[1] + 11))]):
    for k in range(1, 10):
        t = k / 10
        x, y = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
        d.shape("ellipse", f"Chain link {side+1}.{k}", x=x - 2, y=y - 2, width=4, height=4,
                fill="#C9CFD5", opacity=70, stroke=NONE)
d.shape("ellipse", "Rear cog", x=RW[0] - 13, y=RW[1] - 13, width=26, height=26,
        fill=rad((0, "#E4E8EC"), (1, "#5C636B")), stroke=INK, strokeWidth=3)
d.path("M298,560 C318,552 380,560 384,590 C388,624 372,640 350,642 L300,612 Z",
       "Chainguard", fill=lin(-90, (0, "#3E3432"), (1, "#151010")), opacity=70,
       stroke=INK, strokeWidth=3)
# crank + pedal
d.path(seg(BB, (378, 660)), "Crank arm", fill=NONE, stroke=CHROME, strokeWidth=8, cap="round")
d.path(seg((364, 664), (394, 664)), "Pedal", fill=NONE, stroke=INK, strokeWidth=9, cap="round")

# saddle + post
d.path(seg((320, 460), SEAT), "Seat post", fill=NONE, stroke=CHROME, strokeWidth=7, cap="round")
d.path("M282,440 C296,428 340,428 354,436 C352,446 318,452 286,450 Z", "Saddle",
       fill=lin(-90, (0, "#8A5A3C"), (1, "#3E2416")), stroke=INK, strokeWidth=4)
d.path("M292,436 C310,430 330,430 344,434", "Saddle sheen", fill=NONE, stroke="#F2C8A8",
       strokeWidth=3, opacity=50, cap="round")

# handlebars
d.path(seg(HT_TOP, (424, 416)), "Stem", fill=NONE, stroke=CHROME, strokeWidth=8, cap="round")
d.path("M424,416 C412,404 392,400 376,404", "Handlebar", fill=NONE, stroke=INK,
       strokeWidth=12, cap="round")
d.path("M424,416 C412,404 392,400 376,404", "Handlebar chrome", fill=NONE, stroke=CHROME,
       strokeWidth=7, cap="round")
d.path(seg((390, 402), (366, 406)), "Grip", fill=NONE, stroke="#5A3A2A", strokeWidth=12,
       cap="round")
d.shape("ellipse", "Bell", x=414, y=402, width=14, height=12,
        fill=rad((0, "#FFFFFF"), (1, "#A9B0B8")), stroke=INK, strokeWidth=2)

# --- wooden cargo box -------------------------------------------------------------
WOOD = lin(-90, (0, "#E8B878"), (0.5, "#C48A4A"), (1, "#8A5A2C"))
box = "M474,500 L700,488 L692,634 L480,634 Z"
d.path(box, "Cargo box", fill=WOOD, stroke=INK, strokeWidth=6)
for i, (y0, y1) in enumerate([(536, 528), (572, 566), (606, 602)]):
    d.path(f"M478,{y0} L697,{y1}", f"Box plank seam {i+1}", fill=NONE, stroke="#6A3E1C",
           strokeWidth=3, opacity=60)
    d.path(f"M478,{y0+3} L697,{y1+3}", f"Box plank light {i+1}", fill=NONE, stroke="#FBE2B8",
           strokeWidth=3, opacity=35)
for i, (x, y, w) in enumerate([(530, 548, 40), (610, 512, 30), (560, 584, 50), (640, 616, 34)]):
    d.path(f"M{x},{y} C{x+w*0.3},{y-4} {x+w*0.7},{y+4} {x+w},{y}", f"Wood grain {i+1}",
           fill=NONE, stroke="#8A5A2C", strokeWidth=3, opacity=35, cap="round")
d.path("M474,500 L700,488", "Box top rail", fill=NONE, stroke=lin(-90, (0, "#F4D6A4"),
       (1, "#9A6A3A")), strokeWidth=10, cap="round")
d.path("M480,634 L692,634 L700,488 C690,560 640,624 480,628 Z", "Box shade",
       fill="#4A2A10", opacity=22, stroke=NONE)
# corner brackets
for i, (x, y) in enumerate([(482, 506), (686, 494), (486, 618), (680, 618)]):
    d.shape("rectangle", f"Box bracket {i+1}", x=x - 6, y=y - 6, width=14, height=14,
            fill=CHROME, stroke=INK, strokeWidth=2)
# child seat back + cushion peeking above the rail
d.path("M510,500 L514,460 C516,452 560,450 566,458 L566,497 Z", "Child seat back",
       fill=lin(-90, (0, "#5FA8C8"), (1, "#2A6A88")), stroke=INK, strokeWidth=4)
d.path("M522,468 C534,462 548,462 558,466", "Seat back sheen", fill=NONE, stroke="#D8F0FA",
       strokeWidth=3, opacity=55, cap="round")
d.path(seg((540, 470), (540, 496)), "Seat belt", fill=NONE, stroke="#F2D27A", strokeWidth=4,
       opacity=85, cap="round")
# child-seat hoop
hoop = "M494,502 C494,392 690,384 690,492"
d.path(hoop, "Seat hoop ink", fill=NONE, stroke=INK, strokeWidth=12, cap="round")
d.path(hoop, "Seat hoop", fill=NONE, stroke=CHROME, strokeWidth=7, cap="round")
d.path("M510,452 C530,412 600,404 650,420", "Hoop glint", fill=NONE, stroke="#FFFFFF",
       strokeWidth=3, opacity=80, cap="round")
# front lamp on the box
d.path("M700,512 L722,506 L724,526 L702,528 Z", "Lamp", fill=lin(-90, (0, "#FFF4C8"),
       (1, "#C8A040")), stroke=INK, strokeWidth=3)
d.path("M726,508 L760,500 L760,534 L726,526 Z", "Lamp beam", fill="#FFF4C8", opacity=25,
       stroke=NONE)

# --- caption --------------------------------------------------------------------
d.text("CARGO BIKE", "Name", x=500, y=940, size=56, font="Virelai Sans",
       color="#F4D8CC", justify="center")
o = d.text("2012 · PEDAL · 8-SPEED HUB GEAR", "Spec", x=500, y=975, size=22,
           font="Virelai Sans", color="#C99484", justify="center")
if o and "id" in o:
    d.cmd("text.setStyle", "Spec tracking", ids=[o["id"]], tracking=300)

d.finish("cargo-bike-V1R00")
