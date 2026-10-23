#!/usr/bin/env python3
"""Dugong — field-guide plate V1R00. Full body in grazing profile, facing left
and nosing down into the seagrass: weathered-boulder bulk, downturned bristled
muzzle, small paddle flipper, fluked whale-like tail raised behind. Muted
seagrass greens and slate blue, soft volumetric shading. Bed + rays close on
the disc's own arc. 1000x1000. Gradients + translucent shading, never flat."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Dugong — Field Plate", 1000, 1000)

INK = "#232B30"
CX, CY, R = 500, 460, 420
BG_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#122630"}, {"offset": 1, "color": "#04090C"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#D8E2D4"}, {"offset": 0.65, "color": "#93AF9E"},
    {"offset": 1, "color": "#54706A"}]}}
BED_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#A4B48E"}, {"offset": 1, "color": "#6E7E5E"}]}}
BODY_GRAD = {"gradient": {"kind": "linear", "angle": 115, "stops": [
    {"offset": 0, "color": "#8E97A0"}, {"offset": 0.55, "color": "#6A747E"},
    {"offset": 1, "color": "#49535E"}]}}
FLUKE_GRAD = {"gradient": {"kind": "linear", "angle": 60, "stops": [
    {"offset": 0, "color": "#7C8791"}, {"offset": 1, "color": "#454F5A"}]}}
FLIPPER_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#78828C"}, {"offset": 1, "color": "#4A545E"}]}}
MUZZLE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#9AA2A8"}, {"offset": 0.7, "color": "#767F88"},
    {"offset": 1, "color": "#525B64"}]}}
RAY_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#FFFFFF", "opacity": 0.30}, {"offset": 1, "color": "#FFFFFF", "opacity": 0}]}}
BLADE_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#88A878"}, {"offset": 1, "color": "#4E6E4A"}]}}
SCAR_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#B9C0C4"}, {"offset": 1, "color": "#899198"}]}}

def rim_y(x):
    return CY - math.sqrt(R*R - (x - CX)**2)

def chord_x(y, r=R):
    h = math.sqrt(r*r - (y - CY)**2)
    return CX - h, CX + h

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#4E6E66", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#EAF2E6", strokeWidth=3, opacity=55)
d.shape("ellipse", "Patina 1", x=170, y=170, width=230, height=130, fill="#B9CBB8", opacity=24, stroke=NONE)
d.shape("ellipse", "Patina 2", x=600, y=560, width=240, height=120, fill="#6E8A7C", opacity=20, stroke=NONE)
for i, (x, y, w, h) in enumerate([(340,112,110,16),(480,98,86,12),(570,120,100,14),(410,146,64,10)]):
    d.shape("ellipse", f"Caustic {i+1}", x=x, y=y, width=w, height=h,
            fill="#FFFFFF", opacity=20, stroke=NONE)
# light rays: tops ride the disc arc, bottoms tuck under the seagrass bed
for i, (x0, x1, b0, b1, o) in enumerate([(300, 352, 340, 452, 55), (440, 492, 470, 590, 65),
                                         (566, 604, 620, 700, 50), (662, 692, 700, 758, 38)]):
    d.path(f"M{x0},{rim_y(x0):.1f} A420,420 0 0 1 {x1},{rim_y(x1):.1f} L{b1},764 L{b0},764 Z",
           f"Light ray {i+1}", fill=RAY_GRAD, opacity=o, stroke=NONE)
for i, (x, y, w) in enumerate([(190,320,6),(790,250,6),(160,520,7),(840,450,6),
                               (260,220,5),(720,190,6),(140,420,5),(860,560,5)]):
    d.shape("ellipse", f"Drift fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#FFFFFF", opacity=35, stroke=NONE)

# --- seagrass bed: closes on the disc's own arc ---------------------------------
gl, gr = chord_x(756)
d.path(f"M{gl:.1f},756 C360,740 640,740 {gr:.1f},756 A420,420 0 0 1 {gl:.1f},756 Z",
       "Seagrass bed", fill=BED_GRAD, stroke=NONE)
d.path(f"M{gl+20:.1f},755 C370,742 630,742 {gr-20:.1f},755", "Bed light", fill=NONE,
       stroke="#EEF2D8", strokeWidth=4, opacity=40, cap="round")
for i, (x, y, w) in enumerate([(300,790,22),(450,780,18),(600,794,20),(380,822,14),(540,828,16),(680,808,12)]):
    d.shape("ellipse", f"Sand ripple {i+1}", x=x, y=y, width=w*2, height=w/3,
            fill="#5E6E50", opacity=30, stroke=NONE)
def blade(label, x, h, lean, w=10, op=80):
    top = (x + lean, 752 - h)
    c1 = (x - lean*0.4, 752 - h*0.45)
    d.path(f"M{x - w/2:.0f},754 Q{c1[0] - w/2:.0f},{c1[1]:.0f} {top[0]:.0f},{top[1]:.0f} "
           f"Q{c1[0] + w/2:.0f},{c1[1]:.0f} {x + w/2:.0f},754 Z",
           label, fill=BLADE_GRAD, opacity=op, stroke=NONE)
# blades at the grazed patch in front of the muzzle bend toward it
for i, (x, h, lean) in enumerate([(216,86,-34),(238,116,-42),(262,96,-30),
                                  (700,90,-18),(722,140,20),(744,118,-26),(768,84,12)]):
    blade(f"Seagrass {i+1}", x, h, lean)
for i, (x, h, lean) in enumerate([(400,44,-10),(430,58,12),(560,50,-8),(590,40,10)]):
    blade(f"Seagrass low {i+1}", x, h, lean, w=8, op=60)
# re-stroke the rim over the bed
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#4E6E66", strokeWidth=6)
d.shape("ellipse", "Plate inner ring over bed", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#EAF2E6", strokeWidth=3, opacity=35)
d.shape("ellipse", "Dugong shadow", x=270, y=740, width=460, height=26,
        fill="#3E4A3C", opacity=26, stroke=NONE)

# --- tail flukes: two lobes with a central notch, behind the stock ---------------
d.path("M736,432 C790,398 852,368 898,360 C904,386 868,422 816,444 "
       "C788,456 758,456 738,446 Z",
       "Fluke upper", fill=FLUKE_GRAD, stroke=INK, strokeWidth=6)
d.path("M738,472 C796,482 852,500 888,524 C880,548 830,548 786,532 "
       "C762,522 746,502 738,486 Z",
       "Fluke lower", fill=FLUKE_GRAD, stroke=INK, strokeWidth=6)
for i, dd in enumerate(["M780,428 C820,408 856,392 884,384",
                        "M786,492 C822,500 852,512 872,524"]):
    d.path(dd, f"Fluke crease {i+1}", fill=NONE, stroke="#3E4750",
           strokeWidth=4, opacity=45, cap="round")
d.path("M800,404 C832,388 862,376 886,372", "Fluke sheen", fill=NONE,
       stroke="#C6CDD2", strokeWidth=5, opacity=40, cap="round")

# --- far flipper peeking below the belly ------------------------------------------
d.path("M420,640 C412,668 400,694 380,710 C376,692 390,664 404,642 Z",
       "Flipper far", fill="#3E4750", opacity=70, stroke=NONE)

# --- body: weathered boulder, head low to the grass --------------------------------
d.path("M252,676 C270,644 300,610 344,580 C420,530 540,472 656,442 "
       "C700,430 728,430 746,440 L748,478 "
       "C700,512 620,586 530,646 C470,684 400,708 340,712 "
       "C300,714 266,700 252,676 Z",
       "Body", fill=BODY_GRAD, stroke=INK, strokeWidth=7)
# soft volumetric shading: belly glow + top shade along the spine line
d.path("M340,690 C420,700 520,660 610,586", "Belly glow", fill=NONE,
       stroke="#C9D2D4", strokeWidth=22, opacity=22, cap="round")
d.path("M360,568 C440,522 560,474 660,450", "Back shade", fill=NONE,
       stroke="#3A4248", strokeWidth=20, opacity=20, cap="round")
d.path("M400,540 C480,500 570,466 650,448", "Back sheen", fill=NONE,
       stroke="#DDE4E6", strokeWidth=8, opacity=30, cap="round")
# weathered hide: mottled patches + old scars + hide creases
for i, (x, y, w, h) in enumerate([(450,520,90,26),(560,482,80,24),(640,462,60,20),(380,560,60,20)]):
    d.shape("ellipse", f"Hide patch {i+1}", x=x, y=y, width=w, height=h,
            fill="#5A636C", opacity=22, stroke=NONE)
for i, (x, y, w, h) in enumerate([(500,560,40,12),(580,540,34,10),(420,600,36,10),(660,500,30,10)]):
    d.shape("ellipse", f"Scar {i+1}", x=x, y=y, width=w, height=h,
            fill=SCAR_GRAD, opacity=35, stroke=NONE)
for i, dd in enumerate(["M330,600 C326,630 330,660 344,686", "M356,590 C350,624 354,656 368,684",
                        "M680,470 C676,494 678,518 686,540", "M704,462 C700,482 702,504 710,522"]):
    d.path(dd, f"Hide crease {i+1}", fill=NONE, stroke="#454E56",
           strokeWidth=4, opacity=35, cap="round")
for i, (x, y) in enumerate([(440,560),(500,530),(560,510),(620,480),(480,600),(600,570),(400,640)]):
    d.shape("ellipse", f"Hide pore {i+1}", x=x, y=y, width=5, height=5,
            fill="#454E56", opacity=35, stroke=NONE)

# --- near flipper: small paddle at the chest, no nails ----------------------------
d.path("M420,620 C430,650 428,686 410,712 C398,730 372,734 362,720 "
       "C354,706 368,688 380,668 C392,648 402,628 406,614 Z",
       "Flipper near", fill=FLIPPER_GRAD, stroke=NONE)
d.path("M420,620 C430,650 428,686 410,712 C398,730 372,734 362,720 "
       "C354,706 368,688 380,668 C392,648 402,628 406,614",
       "Flipper outline", fill=NONE, stroke=INK, strokeWidth=5, cap="round")
d.path("M404,628 C408,656 402,682 390,704", "Flipper sheen", fill=NONE,
       stroke="#C2CACE", strokeWidth=4, opacity=35, cap="round")

# --- downturned bristled muzzle, bilobed, grazing the grass -----------------------
d.path("M344,590 C306,586 268,598 248,626 C230,652 228,682 246,700 "
       "C264,716 296,718 322,706 C346,694 358,668 356,640 "
       "C354,620 350,604 344,590 Z",
       "Muzzle pad", fill=MUZZLE_GRAD, stroke=NONE)
d.path("M344,590 C306,586 268,598 248,626 C230,652 228,682 246,700 "
       "C264,716 296,718 322,706", "Muzzle outline", fill=NONE,
       stroke=INK, strokeWidth=7, cap="round")
d.path("M322,706 C346,694 358,668 356,640 C354,620 350,604 346,594",
       "Muzzle crease", fill=NONE, stroke="#454E56", strokeWidth=4, opacity=40, cap="round")
# the two lip lobes + mouth slit, angled down toward the grass
d.path("M246,690 C262,704 286,708 306,700", "Lip cleft", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
d.path("M258,716 C272,726 296,728 314,720", "Lower lip", fill=NONE,
       stroke=INK, strokeWidth=4, opacity=70, cap="round")
# nostrils on top of the snout
d.path("M262,610 C268,604 278,604 282,610", "Nostril front", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.path("M290,600 C296,594 306,594 310,600", "Nostril back", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
# heavy bristles hanging off the pad into the grass
for i, (x, y, dx, dy) in enumerate([(252,650,-26,16),(258,670,-28,20),(268,688,-24,24),
                                    (288,698,-16,26),(306,700,-8,28),(240,636,-22,8),
                                    (320,690,4,28),(332,664,10,22)]):
    d.path(f"M{x},{y} L{x+dx},{y+dy}", f"Bristle {i+1}", fill=NONE,
           stroke="#D8DCD6", strokeWidth=2.5, opacity=75, cap="round")
# whisker pores
for i, (x, y) in enumerate([(262,644),(276,638),(290,644),(270,662),(286,658),(300,664),
                            (312,678),(326,652),(252,672),(296,684)]):
    d.shape("ellipse", f"Pore {i+1}", x=x-2, y=y-2, width=4, height=4,
            fill="#3A4148", opacity=70, stroke=NONE)
# small placid eye + brow crease
d.shape("ellipse", "Eye socket", x=368, y=574, width=32, height=22,
        fill="#454E56", opacity=30, stroke=NONE)
d.shape("ellipse", "Eye", x=378, y=579, width=13, height=12, fill="#14181C", stroke=NONE)
d.shape("ellipse", "Eye glint", x=381, y=581, width=5, height=4,
        fill="#FFFFFF", opacity=85, stroke=NONE)
d.path("M370,574 C380,566 394,566 404,574", "Eye crease", fill=NONE,
       stroke="#454E56", strokeWidth=3, opacity=60, cap="round")

# --- a few dislodged grass flecks + bubbles by the muzzle --------------------------
for i, (x, y, w, h) in enumerate([(210,712,16,5),(232,722,13,4),(196,700,12,4)]):
    d.shape("ellipse", f"Grass fleck {i+1}", x=x, y=y, width=w, height=h,
            fill="#7E9A6E", opacity=60, stroke=NONE)
for i, (x, y, w) in enumerate([(228,584,10),(216,548,7),(232,516,11)]):
    d.shape("ellipse", f"Bubble {i+1}", x=x, y=y, width=w, height=w,
            fill="#FFFFFF", opacity=22, stroke="#FFFFFF", strokeWidth=1.5)

# --- name ---------------------------------------------------------------------------
d.text("DUGONG", "Name", x=500, y=962, size=60, font="Virelai Sans",
       color="#DCE8DC", justify="center")

d.finish("dugong-V1R00")
