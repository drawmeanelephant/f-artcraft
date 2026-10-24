#!/usr/bin/env python3
"""Blinko Chompframe — mascot portrait V1R00.
Half-topiary, half-vending mascot with a glitching LED faceplate; cardboard
arm eternally clutching a foil-wrapped cupcake. 1000x1000. Gradients +
translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Blinko Chompframe — Mascot Portrait", 1000, 1000)

INK = "#2A1E18"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#161210"}, {"offset": 1, "color": "#080605"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#5E4A38"}, {"offset": 0.7, "color": "#3E3024"},
    {"offset": 1, "color": "#211A12"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#33261C"}, {"offset": 1, "color": "#17100A"}]}}
TOPIARY = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#5E8A48"}, {"offset": 0.7, "color": "#3E5E30"},
    {"offset": 1, "color": "#24421C"}]}}
VENDING = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#C05C42"}, {"offset": 1, "color": "#7E3226"}]}}
LED_SCR = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1E2A30"}, {"offset": 1, "color": "#0C1418"}]}}
CARDBOARD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#C99F65"}, {"offset": 1, "color": "#8E6836"}]}}
FOIL = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#DDE2EA"}, {"offset": 0.5, "color": "#A8AEBC"},
    {"offset": 1, "color": "#78809A"}]}}
FROST = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F4B4C8"}, {"offset": 1, "color": "#C4748E"}]}}
POT = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#8A5E3E"}, {"offset": 1, "color": "#5A3A24"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#8A6E4E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8D4B8", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(193,233,8),(801,230,7),(157,524,9),(837,544,8),
                               (247,766,7),(753,749,9),(133,393,6),(864,391,7),
                               (391,113,7),(613,110,8),(333,823,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#4E3E2C", opacity=45, stroke=NONE)

# --- floor: bottom segment closed on the disc's own arc -----------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#140E08",
       strokeWidth=4, opacity=70)

# --- dropped wrappers + an expired fortune card ------------------------------------
d.path("M300,690 L360,682 L372,700 L305,700 Z", "Empty wrapper",
       fill="#8A94A4", stroke=INK, strokeWidth=3, join="round", opacity=85)
d.path("M310,690 L322,686 M335,688 L348,684", "Wrapper creases", fill=NONE,
       stroke="#5A6472", strokeWidth=2, opacity=70)
d.path("M640,660 L716,648 L724,686 L648,698 Z", "Fortune card",
       fill="#E8DCBE", stroke=INK, strokeWidth=4, join="round")
d.text("FORTUNE VOID", "Card text", x=655, y=676, size=9,
       font="Virelai Sans", color="#8A3A30", justify="left")

# --- the mascot body: split down the middle -----------------------------------------
d.shape("ellipse", "Chomp shadow", x=330, y=672, width=300, height=32,
        fill="#0C0806", opacity=50, stroke=NONE)
# pedestal pot under the topiary half, block foot under the vending half
d.path("M345,660 L475,660 L465,700 L355,700 Z", "Pot", fill=POT,
       stroke=INK, strokeWidth=5, join="round")
d.shape("rectangle", "Vend foot", x=505, y=672, width=120, height=28,
        fill="#3A2418", stroke=INK, strokeWidth=4, radius=5)
# LEFT HALF: topiary dome
d.path("M480,640 L480,430 C480,355 430,310 385,310 C335,310 300,355 300,430 "
       "L300,640 Z",
       "Topiary half", fill=TOPIARY, stroke=INK, strokeWidth=6)
# leaf bumps along the dome crown
for i, (cx, cy, w) in enumerate([(310,395,34),(330,340,40),(375,308,38),
                                 (430,315,40),(468,350,34),(292,470,30),
                                 (292,545,32),(292,610,30)]):
    d.shape("ellipse", f"Leaf bump {i+1}", x=cx, y=cy, width=w, height=w,
            fill=TOPIARY, stroke=INK, strokeWidth=4)
# leaf flecks
for i, (x, y) in enumerate([(345,430),(400,390),(360,510),(425,470),(370,580),(440,540)]):
    d.path(f"M{x},{y} C{x+8},{y-6} {x+16},{y-6} {x+20},{y+2}",
           f"Leaf {i+1}", fill=NONE, stroke="#7AA85E", strokeWidth=4,
           cap="round", opacity=70)
# shear mark
d.path("M335,445 L365,438", "Shear mark", fill=NONE, stroke="#1E3418",
       strokeWidth=4, cap="round", opacity=60)

# RIGHT HALF: vending machine
d.path("M480,640 L480,300 L660,300 C672,300 680,310 680,322 L680,640 Z",
       "Vending half", fill=VENDING, stroke=INK, strokeWidth=6)
# the seam where topiary meets vending
d.path("M480,310 L480,640", "Split seam", fill=NONE, stroke=INK,
       strokeWidth=5)
# LED faceplate
d.shape("rectangle", "LED plate", x=500, y=330, width=150, height=140,
        fill=LED_SCR, stroke=INK, strokeWidth=5, radius=8)
# scanlines
for i in range(5):
    d.path(f"M505,{352+i*26} L645,{352+i*26}", f"Scan {i+1}", fill=NONE,
           stroke="#3E5A62", strokeWidth=2, opacity=50)
# glitch bars
d.shape("rectangle", "Glitch bar", x=505, y=368, width=90, height=10,
        fill="#5FD8C8", opacity=45, stroke=NONE)
d.shape("rectangle", "Glitch bar 2", x=560, y=432, width=85, height=8,
        fill="#E88AA4", opacity=40, stroke=NONE)
# eyes: one round pixel-glow, one blocky glitch square
d.shape("ellipse", "Eye round", x=525, y=385, width=22, height=24,
        fill="#7EE8D4", stroke=NONE)
d.shape("rectangle", "Eye block", x=590, y=383, width=22, height=22,
        fill="#7EE8D4", stroke=NONE, radius=3)
d.shape("rectangle", "Eye block tear", x=618, y=390, width=14, height=8,
        fill="#7EE8D4", opacity=60, stroke=NONE)
# zigzag waveform mouth
d.path("M535,440 L548,428 L561,442 L574,430 L587,442 L600,431",
       "Wave mouth", fill=NONE, stroke="#7EE8D4", strokeWidth=4,
       cap="round", join="round")
# coin slot + return
d.shape("rectangle", "Coin slot", x=600, y=500, width=50, height=18,
        fill="#161C20", stroke=INK, strokeWidth=3, radius=8)
d.text("25¢", "Coin price", x=608, y=514, size=11, font="Virelai Sans",
       color="#E8C25E", justify="left")
d.shape("ellipse", "Coin return", x=640, y=548, width=22, height=22,
        fill="#161C20", stroke=INK, strokeWidth=3)
# dispensing slot with a snack silhouette hanging half-out
d.shape("rectangle", "Dispense slot", x=500, y=560, width=150, height=48,
        fill="#161C20", stroke=INK, strokeWidth=4, radius=6)
d.path("M540,560 L575,560 L572,600 L544,600 Z", "Half-dispensed snack",
       fill="#E8A85E", stroke=INK, strokeWidth=3, join="round")
# side label strip
d.shape("rectangle", "Label strip", x=655, y=330, width=14, height=140,
        fill="#E8D4B8", opacity=80, stroke=INK, strokeWidth=3)

# --- cardboard arm + the eternal cupcake --------------------------------------------
d.path("M675,470 C715,450 745,455 762,478 C770,490 770,505 762,514",
       "Cardboard arm", fill=NONE, stroke=CARDBOARD, strokeWidth=20,
       cap="round")
# corrugation ticks on the arm
for i, (x, y) in enumerate([(695,458),(720,455),(745,464)]):
    d.path(f"M{x},{y} L{x+6},{y+14}", f"Flute {i+1}", fill=NONE,
           stroke="#8E6836", strokeWidth=3, opacity=70)
# gripper claws on the cupcake cup
d.path("M748,505 C745,518 752,528 762,530", "Claw L", fill=NONE,
       stroke="#8E6836", strokeWidth=7, cap="round")
d.path("M782,500 C788,512 784,524 776,530", "Claw R", fill=NONE,
       stroke="#8E6836", strokeWidth=7, cap="round")
# cupcake: foil cup + frosting swirl
d.path("M745,520 L795,520 L785,570 L755,570 Z", "Foil cup", fill=FOIL,
       stroke=INK, strokeWidth=4, join="round")
for i in range(3):
    x = 755 + i*11
    d.path(f"M{x},523 L{x+3},567", f"Foil ridge {i+1}", fill=NONE,
           stroke="#7A8296", strokeWidth=2, opacity=70)
d.path("M742,522 C738,500 752,488 768,488 C784,488 800,500 797,520 "
       "C792,512 780,508 770,510 C758,512 748,515 742,522 Z",
       "Frosting", fill=FROST, stroke=INK, strokeWidth=4, join="round")
d.shape("ellipse", "Sprinkle 1", x=760, y=498, width=7, height=4,
        fill="#7EE8D4", stroke=NONE)
d.shape("ellipse", "Sprinkle 2", x=776, y=502, width=7, height=4,
        fill="#E8C25E", stroke=NONE)

# --- captions ------------------------------------------------------------------
d.text("BLINKO CHOMPFRAME", "Name", x=500, y=930, size=54, font="Virelai Sans",
       color="#E8D4B8", justify="center")
r = d.text("FORECASTER OF SNACK SATISFACTION", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#B89A72", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("937.blinko-chompframe-V1R00")
