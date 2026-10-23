#!/usr/bin/env python3
"""City taxi — field plate V2R00, a rendition of V1R00.

V1 was midnight: profile cab against a lit skyline. This take is the other end
of the shift — 5:40 a.m., an empty boulevard, mist burning off, the cab alone
at the curb with the sky in its glass and a long shadow running left. Pale
rose light, cold chrome, one warm streetlamp still on.
1000x1000. House style: gradients + translucent shading, never flat fills.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("City Taxi — Field Plate V2", 1000, 1000)

CX, CY, R = 500, 460, 420
INK = "#2A1A1E"


def rim_y(x):
    return CY + math.sqrt(max(R * R - (x - CX) ** 2, 0))


BG_GRAD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000], "stops": [
    {"offset": 0, "color": "#0B0709"}, {"offset": 1, "color": "#050203"}]}}
SKY_GRAD = {"gradient": {"kind": "linear", "start": [0, 60], "end": [0, 760], "stops": [
    {"offset": 0, "color": "#7E6A85"}, {"offset": 0.3, "color": "#C08C92"},
    {"offset": 0.58, "color": "#E8AE96"}, {"offset": 0.78, "color": "#F6CFB0"},
    {"offset": 1, "color": "#E2AE8E"}]}}
ROAD_GRAD = {"gradient": {"kind": "linear", "start": [0, 660], "end": [0, 890], "stops": [
    {"offset": 0, "color": "#6E5A5E"}, {"offset": 0.3, "color": "#4A3A40"},
    {"offset": 1, "color": "#241A20"}]}}
BODY_GRAD = {"gradient": {"kind": "linear", "start": [0, 500], "end": [0, 660], "stops": [
    {"offset": 0, "color": "#F6CE8A"}, {"offset": 0.28, "color": "#E2A94E"},
    {"offset": 0.72, "color": "#C08334"}, {"offset": 1, "color": "#7E5220"}]}}
BODY_SHADE = {"gradient": {"kind": "linear", "start": [0, 560], "end": [0, 680], "stops": [
    {"offset": 0, "color": "#8A5A24", "opacity": 0.0},
    {"offset": 1, "color": "#6A4218", "opacity": 0.55}]}}
GLASS_GRAD = {"gradient": {"kind": "linear", "start": [0, 505], "end": [0, 575], "stops": [
    {"offset": 0, "color": "#F8DCC8", "opacity": 0.85},
    {"offset": 0.55, "color": "#D8A6A0", "opacity": 0.7},
    {"offset": 1, "color": "#7A5A66", "opacity": 0.8}]}}
CHROME = {"gradient": {"kind": "linear", "start": [0, 590], "end": [0, 616], "stops": [
    {"offset": 0, "color": "#FFF6E2"}, {"offset": 0.4, "color": "#D9C8B4"},
    {"offset": 1, "color": "#8A7A70"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill="#2A1C22", stroke="#2A171C", strokeWidth=6)
d.shape("ellipse", "Sky", x=80, y=40, width=840, height=840, fill=SKY_GRAD, stroke=NONE)
d.shape("ellipse", "Inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#FFE2C4", strokeWidth=3, opacity=14)

# low sun behind the mist, just above the roofline
d.shape("ellipse", "Sun haze", x=270, y=330, width=520, height=380,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#FFF0D2", "opacity": 0.8},
            {"offset": 0.5, "color": "#FFD2A4", "opacity": 0.35},
            {"offset": 1, "color": "#FFC89A", "opacity": 0}]}}, stroke=NONE, opacity=75)

# --- distant blocks in the mist ------------------------------------------------
BLOCKS = [(160, 392, 84, 288), (250, 344, 70, 336), (330, 412, 78, 268),
          (404, 366, 66, 314), (470, 408, 88, 272), (556, 380, 74, 300),
          (628, 348, 96, 330), (718, 398, 82, 276), (790, 356, 62, 318)]
for i, (x, y, w, h) in enumerate(BLOCKS):
    d.shape("rectangle", f"Block {i+1}", x=x, y=y, width=w, height=h,
            fill={"gradient": {"kind": "linear", "start": [0, y], "end": [0, 720], "stops": [
                {"offset": 0, "color": "#5E4050"}, {"offset": 1, "color": "#B98A84"}]}},
            opacity=(15 if i in (0, 8) else 30), stroke=NONE)
    # a grid of dark windows, a couple lit
    for r in range(3):
        for c in range(2):
            wx = x + 14 + c * (w - 28) / 2
            wy = y + 22 + r * 54
            lit = (i + r + c) % 5 == 0
            d.shape("rectangle", f"Window {i+1}-{r}-{c}", x=wx, y=wy,
                    width=(w - 34) / 2, height=26,
                    fill="#FFE0B0" if lit else "#4E3440",
                    opacity=40 if lit else 26, stroke=NONE)

# mist banks across the skyline
for i, (x, y, w, h, op) in enumerate([(80, 496, 420, 116, 50), (380, 480, 460, 126, 44),
                                      (200, 556, 560, 106, 34), (600, 446, 260, 146, 30),
                                      (60, 618, 380, 80, 22), (560, 610, 420, 84, 20)]):
    d.shape("ellipse", f"Mist {i+1}", x=x, y=y, width=w, height=h,
            fill={"gradient": {"kind": "radial", "stops": [
                {"offset": 0, "color": "#FFE6D0", "opacity": 0.55},
                {"offset": 1, "color": "#FFE6D0", "opacity": 0}]}}, stroke=NONE, opacity=op)

# a streetlamp still burning on the far sidewalk
d.path("M818,690 L818,430 Q818,404 842,402", "Lamp post", fill=NONE, stroke="#4A343C",
       strokeWidth=5, cap="round", opacity=80)
d.shape("ellipse", "Lamp glow", x=790, y=360, width=110, height=110,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#FFD9A0", "opacity": 0.7},
            {"offset": 1, "color": "#FFD9A0", "opacity": 0}]}}, stroke=NONE, opacity=65)
d.shape("ellipse", "Lamp bulb", x=838, y=392, width=16, height=12, fill="#FFF0CE", stroke=NONE)

# --- road ------------------------------------------------------------------------
GY = 690
d.path(f"M149,{GY} C300,{GY - 4} 520,{GY + 2} 700,{GY - 2} C760,{GY - 4} 810,{GY - 2} 851,{GY} "
       f"A420,420 0 0 1 149,{GY} Z", "Road", fill=ROAD_GRAD, stroke=NONE, opacity=95)
d.path(f"M156,{GY} C320,{GY - 4} 520,{GY + 2} 700,{GY - 2} C760,{GY - 4} 810,{GY - 2} 845,{GY}",
       "Curb", fill=NONE, stroke="#B08A80", strokeWidth=3, opacity=45, cap="round")
# wet reflections: horizontal smears under the skyline
for i, (y, w, op) in enumerate([(714, 560, 16), (736, 480, 13), (764, 380, 10), (800, 300, 8)]):
    d.shape("ellipse", f"Reflection {i+1}", x=500 - w / 2, y=y, width=w, height=14,
            fill="#F2C8AC", opacity=op, stroke=NONE)
# lane line, broken, running out of frame
for i, x in enumerate((300, 420, 540, 660)):
    d.shape("rectangle", f"Lane dash {i+1}", x=x, y=806, width=68, height=6,
            fill="#E8D2B4", opacity=14, stroke=NONE)

# --- the cab ---------------------------------------------------------------------
# long shadow running left across the wet road
d.path("M204,700 C168,706 140,712 120,720 C170,726 230,724 300,716 "
       "C360,710 440,700 520,696 L520,710 C400,714 300,720 204,720 Z",
       "Cab shadow", fill="#2A1C22", opacity=32, stroke=NONE)
d.shape("ellipse", "Contact shadow", x=196, y=682, width=612, height=40,
        fill="#1A1014", opacity=45, stroke=NONE)

BODY = ("M206,646 L202,612 C200,594 208,582 224,576 L258,568 "
        "C280,562 296,552 312,536 L352,510 C362,502 380,498 470,497 "
        "C560,496 580,500 590,508 L628,552 C640,562 660,566 700,568 "
        "L772,572 C788,574 798,580 800,592 L802,614 C804,630 798,640 786,644 "
        "L700,650 C690,650 682,644 676,636 L672,628 "
        "C664,610 648,600 628,600 L360,600 C340,600 324,610 316,628 "
        "L312,638 C306,646 298,650 288,650 L222,648 C212,648 208,647 206,646 Z")

d.path(BODY, "Body", fill=BODY_GRAD, stroke=INK, strokeWidth=5)
d.path(BODY, "Body shade", fill=BODY_SHADE, stroke=NONE, opacity=90)

# roof and hood catching the dawn sky
d.path("M312,536 L352,510 C362,502 380,498 470,497 L560,497", "Roof light",
       fill=NONE, stroke="#FFE8C0", strokeWidth=7, opacity=55, cap="round")
d.path("M628,552 C640,562 660,566 700,568 L772,572", "Hood light",
       fill=NONE, stroke="#FFE8C0", strokeWidth=6, opacity=45, cap="round")
d.path("M214,584 L250,574 C272,568 288,558 302,544", "Rear light",
       fill=NONE, stroke="#FFE0B4", strokeWidth=4, opacity=35, cap="round")

# glazing: rear screen, door glass, windshield; the sky shows through
d.path("M318,540 C336,522 352,514 372,511 L432,509 L432,560 L318,560 Z",
       "Rear glass", fill=GLASS_GRAD, stroke=INK, strokeWidth=4, opacity=88)
d.path("M442,509 L556,507 L592,556 L442,558 Z", "Front glass", fill=GLASS_GRAD,
       stroke=INK, strokeWidth=4, opacity=88)
d.path("M296,572 L432,566 L432,600 L300,600 Z", "Rear door glass", fill=GLASS_GRAD,
       stroke=INK, strokeWidth=4, opacity=80)
d.path("M442,566 L560,564 L590,596 L442,600 Z", "Front door glass", fill=GLASS_GRAD,
       stroke=INK, strokeWidth=4, opacity=80)
# sky reflection streaks across the glass
for i, (x0, y0, x1, y1, w) in enumerate([(332, 552, 386, 514, 6), (452, 552, 512, 512, 7),
                                         (560, 560, 582, 540, 4)]):
    d.path(f"M{x0},{y0} L{x1},{y1}", f"Glass glint {i+1}", fill=NONE, stroke="#FFF6E6",
           strokeWidth=w, opacity=42, cap="round")
# door frames and pillars
for i, (x0, y0, x1, y1) in enumerate([(436, 506, 436, 600), (596, 552, 604, 600),
                                      (462, 560, 462, 600), (536, 560, 536, 600)]):
    d.path(f"M{x0},{y0} L{x1},{y1}", f"Pillar {i+1}", fill=NONE, stroke=INK,
           strokeWidth=5, opacity=70, cap="round")

# chrome: beltline, bumpers, window sills
d.path("M208,600 L300,600 L300,606 L208,606 Z", "Rear bumper", fill=CHROME, stroke=INK, strokeWidth=3)
d.path("M788,606 L806,606 L806,620 L788,620 Z", "Front bumper", fill=CHROME, stroke=INK, strokeWidth=3)
d.path("M300,572 L700,566", "Belt trim", fill=NONE, stroke=CHROME, strokeWidth=5, opacity=80, cap="round")
d.path("M206,612 L300,610", "Belt trim rear", fill=NONE, stroke=CHROME, strokeWidth=4, opacity=60, cap="round")

# headlight, taillight, grille
d.shape("ellipse", "Headlight", x=780, y=580, width=26, height=20, fill="#FFF4D8", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Headlight glow", x=766, y=570, width=58, height=42,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#FFE9C0", "opacity": 0.5},
            {"offset": 1, "color": "#FFE9C0", "opacity": 0}]}}, stroke=NONE, opacity=55)
d.shape("rectangle", "Grille", x=796, y=586, width=10, height=22, fill="#5A4A44",
        stroke=INK, strokeWidth=2)
d.shape("rectangle", "Taillight", x=200, y=600, width=12, height=16, fill="#B84A3A",
        stroke=INK, strokeWidth=2)

# roof sign, lit
d.shape("rectangle", "Sign box", x=406, y=472, width=96, height=26, fill="#F6DCA8",
        stroke=INK, strokeWidth=3)
d.text("TAXI", "Sign text", x=454, y=482, size=17, font="Virelai Sans", color="#4A2A16",
       justify="center")
d.shape("ellipse", "Sign glow", x=376, y=452, width=156, height=70,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#FFD9A0", "opacity": 0.45},
            {"offset": 1, "color": "#FFD9A0", "opacity": 0}]}}, stroke=NONE, opacity=55)

# checker band along the doors — the one thing that says "cab"
for i in range(11):
    x = 312 + i * 30
    d.shape("rectangle", f"Checker light {i+1}", x=x, y=616, width=15, height=15,
            fill="#F2E2C4", opacity=85, stroke=NONE)
    d.shape("rectangle", f"Checker dark {i+1}", x=x + 15, y=616, width=15, height=15,
            fill="#2E2024", opacity=85, stroke=NONE)
d.shape("rectangle", "Checker edge", x=312, y=612, width=330, height=2,
        fill="#2E2024", opacity=60, stroke=NONE)
d.shape("rectangle", "Checker edge low", x=312, y=631, width=330, height=2,
        fill="#2E2024", opacity=60, stroke=NONE)

# door handle, mirror, vent
d.shape("rectangle", "Door handle", x=470, y=584, width=28, height=6, fill="#E8D6BC",
        stroke=INK, strokeWidth=2, opacity=90)
d.shape("rectangle", "Door handle 2", x=560, y=582, width=26, height=6, fill="#E8D6BC",
        stroke=INK, strokeWidth=2, opacity=90)
d.path("M622,556 L648,548 L652,560 L626,566 Z", "Mirror", fill="#B07C3C", stroke=INK, strokeWidth=3)
d.path("M206,626 L300,624", "Rocker trim", fill=NONE, stroke=INK, strokeWidth=3, opacity=55, cap="round")

# --- wheels ----------------------------------------------------------------------
def wheel(cx, cy, r, label):
    d.shape("ellipse", f"{label} tyre", x=cx - r, y=cy - r, width=2 * r, height=2 * r,
            fill={"gradient": {"kind": "radial", "stops": [
                {"offset": 0, "color": "#3A3034"}, {"offset": 0.72, "color": "#221A1E"},
                {"offset": 1, "color": "#120C10"}]}}, stroke=INK, strokeWidth=3)
    d.shape("ellipse", f"{label} hub", x=cx - r * 0.56, y=cy - r * 0.56,
            width=r * 1.12, height=r * 1.12, fill=CHROME, stroke="#6A5A50", strokeWidth=3)
    d.shape("ellipse", f"{label} hub inner", x=cx - r * 0.28, y=cy - r * 0.28,
            width=r * 0.56, height=r * 0.56, fill="#9A8A80", stroke="#5A4A44", strokeWidth=2)
    for k in range(5):
        a = math.radians(-90 + k * 72)
        d.path(f"M{cx},{cy} L{cx + math.cos(a) * r * 0.5:.1f},{cy + math.sin(a) * r * 0.5:.1f}",
               f"{label} spoke {k+1}", fill=NONE, stroke="#EDE2D0", strokeWidth=3.4, opacity=80)


wheel(318, 664, 46, "Rear")
wheel(716, 664, 46, "Front")
# wheel arches, drawn as dark crescents over the body edge
for i, (cx, cy, r) in enumerate(((318, 664, 54), (716, 664, 54))):
    d.path(f"M{cx - r},660 A{r},{r} 0 0 1 {cx + r},660", f"Arch {i+1}", fill=NONE,
           stroke=INK, strokeWidth=5, opacity=80)

# --- plate rim -------------------------------------------------------------------
# nothing may show outside the disc: repaint the backdrop over the ring,
# then the rim gets drawn back on top of it
d.shape("ellipse", "Backdrop mask", x=-200, y=-240, width=1400, height=1400,
        fill=NONE, stroke=BG_GRAD, strokeWidth=560)

d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#2A171C", strokeWidth=6)
d.shape("ellipse", "Rim light", x=94, y=54, width=812, height=812,
        fill=NONE, stroke="#FFE2C4", strokeWidth=2.2, opacity=18)

d.text("CITY TAXI", "Name", x=500, y=944, size=54, font="Virelai Sans",
       color="#FFEBD2", justify="center")
d.text("1979  ·  V8  ·  AUTOMATIC", "Spec", x=500, y=976, size=21, font="Virelai Sans",
       color="#E0B48E", justify="center")

d.finish("city-taxi-V2R00")
