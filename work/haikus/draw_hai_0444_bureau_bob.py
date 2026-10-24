#!/usr/bin/env python3
"""HAI-0444 Bureau Bob — haiku plate V1R00. The case number exists, the case
itself does not: Bob holds a real ticket tied to a dashed ghost folder, appeal
portal reports success while the mainframe finds nothing. Statute vs shoe on
a level scale, chatbot clown in a bubble. Warm dark ink, 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("HAI-0444 Bureau Bob — Haiku Plate", 1000, 1000)

INK = "#2A1A12"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1A100A"}, {"offset": 1, "color": "#0A0503"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#5C3F28"}, {"offset": 0.7, "color": "#37220F"},
    {"offset": 1, "color": "#1C0F07"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#33210F"}, {"offset": 1, "color": "#1A0E06"}]}}
BEZEL = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#51453A"}, {"offset": 1, "color": "#2E2620"}]}}
PORTAL_SCR = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#17402A"}, {"offset": 1, "color": "#0A2317"}]}}
CRT_SCR = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1C1916"}, {"offset": 1, "color": "#0E0B09"}]}}
CABINET = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4A4038"}, {"offset": 1, "color": "#262019"}]}}
SUIT = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#5E5470"}, {"offset": 0.75, "color": "#453C56"},
    {"offset": 1, "color": "#2C2438"}]}}
FOLDER = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#EBD3A0"}, {"offset": 1, "color": "#C6A870"}]}}
BONE = "#F0DEB8"
DIM = "#C9A87E"
GREEN = "#8FD49A"
RED = "#B05048"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#8A6A44", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8D4AE", strokeWidth=3, opacity=45)
for i, (x, y, w) in enumerate([(192, 232, 8), (800, 226, 7), (158, 528, 9),
                               (836, 542, 8), (248, 762, 7), (750, 750, 9),
                               (132, 392, 6), (864, 388, 7), (392, 112, 7),
                               (612, 110, 8), (330, 820, 6), (668, 818, 7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#6E4E30", opacity=45, stroke=NONE)

# --- floor: bottom segment closed on the disc's own arc -----------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#120A05",
       strokeWidth=4, opacity=70)

# --- ghost COBOL high on the plate --------------------------------------------
d.text("PERFORM UNTIL NO-RECORD-FOUND", "Cobol 1", x=500, y=140, size=13,
       font="Virelai Sans", color="#7A6248", justify="center")
d.text("IF SUCCESS THEN MOVE ZEROES TO CASE", "Cobol 2", x=500, y=163,
       size=12, font="Virelai Sans", color="#6A543C", justify="center")

# --- appeal portal (left): reports success -------------------------------------
d.shape("ellipse", "Portal glow", x=180, y=200, width=270, height=220,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#8FD49A", "opacity": 0.14},
            {"offset": 1, "color": "#8FD49A", "opacity": 0}]}},
        stroke=NONE)
d.shape("rectangle", "Portal bezel", x=190, y=215, width=240, height=185,
        fill=BEZEL, stroke=INK, strokeWidth=5, radius=10)
d.shape("rectangle", "Portal screen", x=204, y=229, width=212, height=140,
        fill=PORTAL_SCR, stroke="#0A1A12", strokeWidth=3, radius=6)
d.shape("ellipse", "Check badge", x=219, y=248, width=44, height=44,
        fill=GREEN, stroke=INK, strokeWidth=4)
d.path("M229,270 L239,280 L254,259", "Check mark", fill=NONE,
       stroke="#0A2317", strokeWidth=5, cap="round", join="round")
d.text("UPLOAD", "Portal line 1", x=275, y=266, size=15,
       font="Virelai Sans", color="#A9E8B4", justify="left")
d.text("SUCCEEDED", "Portal line 2", x=275, y=288, size=15,
       font="Virelai Sans", color="#7FC78C", justify="left")
for i, w in enumerate([176, 140, 160]):
    d.shape("rectangle", f"Portal row {i+1}", x=216, y=312 + i * 16,
            width=w, height=7, fill="#3E7A52", opacity=55, stroke=NONE,
            radius=3)
d.shape("rectangle", "Portal stand", x=288, y=400, width=38, height=55,
        fill=BEZEL, stroke=INK, strokeWidth=4)
d.path("M265,455 L350,455 L360,470 L255,470 Z", "Portal foot",
       fill=BEZEL, stroke=INK, strokeWidth=4)

# --- mainframe cabinet (right): finds nothing -----------------------------------
d.shape("rectangle", "Mainframe", x=585, y=195, width=230, height=280,
        fill=CABINET, stroke=INK, strokeWidth=6, radius=12)
# twin tape reels
for i, cx in enumerate([645, 745]):
    d.shape("ellipse", f"Reel {i+1}", x=cx - 38, y=212, width=76, height=76,
            fill="#2A2320", stroke=INK, strokeWidth=4)
    d.shape("ellipse", f"Reel hub {i+1}", x=cx - 9, y=241, width=18,
            height=18, fill="#8A7A62", stroke=INK, strokeWidth=3)
    for j in range(3):
        a = j * 2.094 + (0.5 if i else 0)
        import math
        x2 = cx + 30 * math.cos(a)
        y2 = 250 + 30 * math.sin(a)
        d.path(f"M{cx},250 L{x2:.0f},{y2:.0f}", f"Reel {i+1} spoke {j+1}",
               fill=NONE, stroke="#6A5C48", strokeWidth=5, cap="round",
               opacity=80)
# lamp column
for i, c in enumerate([GREEN, "#E8C85E", RED, "#3E5A44", GREEN]):
    d.shape("ellipse", f"Lamp {i+1}", x=797, y=222 + i * 22, width=9,
            height=9, fill=c, stroke=NONE,
            opacity=90 if i < 3 else 40)
# dead CRT set into the cabinet
d.shape("rectangle", "CRT bezel", x=605, y=318, width=190, height=120,
        fill=BEZEL, stroke=INK, strokeWidth=4, radius=8)
d.shape("rectangle", "CRT screen", x=616, y=329, width=168, height=98,
        fill=CRT_SCR, stroke="#060504", strokeWidth=3, radius=5)
d.shape("ellipse", "CRT spinner", x=631, y=362, width=24, height=24,
        fill=NONE, stroke="#6A5A44", strokeWidth=4)
d.path("M631,374 L631,383", "Spinner tick", fill=NONE, stroke="#6A5A44",
       strokeWidth=4, cap="round")
d.text("NO RECORD", "CRT line 1", x=666, y=365, size=14,
       font="Virelai Sans", color="#A89678", justify="left")
d.text("FOUND", "CRT line 2", x=666, y=386, size=14,
       font="Virelai Sans", color="#8A785E", justify="left")
d.text("0 RESULTS", "CRT line 3", x=631, y=414, size=11,
       font="Source Sans 3", color="#6A5A44", justify="left")
# vents + kick plate
for i in range(3):
    d.shape("rectangle", f"Vent {i+1}", x=605, y=446 + i * 11, width=150,
            height=5, fill="#171210", opacity=75, stroke=NONE, radius=2)

# --- statute vs shoe: a level scale (lower left) ---------------------------------
d.shape("ellipse", "Scale shadow", x=190, y=698, width=120, height=16,
        fill="#0A0604", opacity=40, stroke=NONE)
d.path("M250,560 L250,700", "Scale post", fill=NONE, stroke="#B08D5E",
       strokeWidth=6, cap="round")
d.path("M218,700 L282,700 L274,688 L226,688 Z", "Scale base",
       fill="#8A6A44", stroke=INK, strokeWidth=4)
d.path("M196,566 L304,566", "Scale beam", fill=NONE, stroke="#B08D5E",
       strokeWidth=6, cap="round")
d.shape("ellipse", "Beam pivot", x=243, y=559, width=14, height=14,
        fill="#D8B57E", stroke=INK, strokeWidth=3)
for side, px in [("L", 196), ("R", 304)]:
    d.path(f"M{px},566 L{px-14},610 M{px},566 L{px+14},610",
           f"Pan wires {side}", fill=NONE, stroke="#B08D5E",
           strokeWidth=2.5, cap="round")
    d.path(f"M{px-22},610 Q{px},626 {px+22},610", f"Pan {side}",
           fill=NONE, stroke="#B08D5E", strokeWidth=4, cap="round")
# the statute: a little law book on the left pan
d.shape("rectangle", "Statute book", x=178, y=588, width=38, height=22,
        fill="#6E3A34", stroke=INK, strokeWidth=3, radius=2)
d.path("M182,594 L212,594 M182,600 L212,600", "Book bands", fill=NONE,
       stroke="#D8B57E", strokeWidth=2, opacity=80)
# the shoe: a plain shoe on the right pan — equal weight
d.path("M286,612 L286,595 C293,591 298,594 302,600 L311,604 "
       "C318,606 324,608 324,612 Z",
       "Shoe", fill="#4A3626", stroke=INK, strokeWidth=3, join="round")
d.path("M288,612 L288,617 L298,617 L298,612", "Shoe heel",
       fill="#3A2A1A", stroke=INK, strokeWidth=2.5)

# --- chatbot clown (lower right): a bubble that helps no one --------------------
d.shape("rectangle", "Chat bubble", x=688, y=540, width=140, height=110,
        fill="#241B14", opacity=80, stroke="#8A6A44", strokeWidth=4,
        radius=18)
d.path("M706,650 L696,676 L726,652", "Bubble tail", fill="#241B14",
       stroke="#8A6A44", strokeWidth=4, join="round")
d.shape("ellipse", "Clown face", x=716, y=556, width=56, height=56,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#F0E2C8"},
            {"offset": 1, "color": "#C9A882"}]}},
        stroke=INK, strokeWidth=4)
d.shape("ellipse", "Clown eye L", x=730, y=576, width=7, height=9,
        fill="#2A1A12", stroke=NONE)
d.shape("ellipse", "Clown eye R", x=752, y=576, width=7, height=9,
        fill="#2A1A12", stroke=NONE)
d.shape("ellipse", "Clown nose", x=738, y=586, width=13, height=13,
        fill=RED, stroke=INK, strokeWidth=2.5)
d.path("M726,596 Q744,612 762,596", "Clown grin", fill=NONE, stroke=INK,
       strokeWidth=4, cap="round")
# tiny party hat, tipped
d.path("M732,556 L748,532 L762,558 Z", "Party hat", fill="#8A3A44",
       stroke=INK, strokeWidth=3, join="round")
d.shape("ellipse", "Hat bobble", x=743, y=527, width=9, height=9,
        fill="#E8D4AE", stroke=INK, strokeWidth=2)
# painted-on grin cheeks + tiny ruff
d.shape("ellipse", "Cheek L", x=724, y=590, width=7, height=5,
        fill=RED, opacity=45, stroke=NONE)
d.shape("ellipse", "Cheek R", x=758, y=590, width=7, height=5,
        fill=RED, opacity=45, stroke=NONE)
for i, cx in enumerate([726, 744, 762]):
    d.shape("ellipse", f"Ruff {i+1}", x=cx - 8, y=610, width=16, height=10,
            fill="#E8D4AE", stroke=INK, strokeWidth=2)
d.text("…", "Typing dots", x=776, y=632, size=22, font="Virelai Sans",
       color="#8A6A44", justify="left")
d.shape("ellipse", "Online dot", x=812, y=552, width=10, height=10,
        fill=GREEN, stroke=INK, strokeWidth=2)

# --- Bob: folder-headed clerk, deadpan ------------------------------------------
d.shape("ellipse", "Bob shadow", x=390, y=722, width=230, height=26,
        fill="#0A0604", opacity=45, stroke=NONE)
d.path("M500,548 C575,548 620,600 620,662 C620,706 575,726 500,726 "
       "C425,726 380,706 380,662 C380,600 425,548 500,548 Z",
       "Bob body", fill=SUIT, stroke=INK, strokeWidth=6)
d.path("M465,570 L500,624 L535,570", "Shirt V", fill=NONE, stroke="#D8CBE0",
       strokeWidth=8, cap="round", join="round")
d.path("M493,620 L507,620 L505,688 L500,698 L495,688 Z", "Tie",
       fill="#8A3A44", stroke=INK, strokeWidth=3, join="round")
d.path("M385,622 C360,632 352,658 362,680", "Arm L", fill=NONE,
       stroke="#453C56", strokeWidth=18, cap="round")
d.path("M615,622 C640,632 650,650 640,668", "Arm R", fill=NONE,
       stroke="#453C56", strokeWidth=18, cap="round")
d.shape("ellipse", "Hand R", x=626, y=654, width=26, height=24,
        fill="#B4A0C4", stroke=INK, strokeWidth=4)
# head: manila folder with tab
d.path("M425,414 L425,540 L575,540 L575,430 L545,430 L538,414 Z",
       "Folder head", fill=FOLDER, stroke=INK, strokeWidth=6, join="round")
d.path("M425,458 L575,458", "Folder crease", fill=NONE, stroke="#B0935E",
       strokeWidth=3, opacity=60)
# face: glasses, flat eyes, flat mouth
d.shape("ellipse", "Lens L", x=448, y=476, width=42, height=42,
        fill="#F5EDD8", opacity=35, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Lens R", x=512, y=476, width=42, height=42,
        fill="#F5EDD8", opacity=35, stroke=INK, strokeWidth=4)
d.path("M490,497 L512,497", "Bridge", fill=NONE, stroke=INK, strokeWidth=4)
d.path("M448,490 C455,498 465,498 472,490", "Eye L", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
d.path("M530,490 C537,498 547,498 554,490", "Eye R", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
d.path("M480,524 L522,524", "Flat mouth", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
d.path("M520,506 L562,498 L566,520 L524,528 Z", "Red stamp", fill=RED,
       opacity=75, stroke=NONE)
d.shape("ellipse", "Hand L", x=338, y=664, width=26, height=24,
        fill="#B4A0C4", stroke=INK, strokeWidth=4)

# --- the case that is not: ghost folder in front of Bob --------------------------
# dashed outline folder dissolving upward — drawn over him, the case is a void
GHOST = "M300,652 L300,785 L462,785 L462,668 L366,668 L356,652 Z"
d.path(GHOST, "Ghost folder", fill="#E8D4AE", opacity=9, stroke="#E8D4AE",
       strokeWidth=4, dash=[10, 8])
d.path("M312,706 L450,706 M312,738 L450,738", "Ghost lines", fill=NONE,
       stroke="#E8D4AE", strokeWidth=2.5, dash=[6, 6], opacity=32)
for i, (x, y, s, o) in enumerate([(312, 622, 13, 48), (348, 604, 10, 40),
                                  (386, 614, 12, 44), (426, 596, 9, 34),
                                  (448, 622, 8, 30), (330, 580, 7, 24),
                                  (406, 574, 8, 22), (366, 590, 6, 28)]):
    d.shape("rectangle", f"Dissolve {i+1}", x=x, y=y, width=s, height=s,
            fill="#E8D4AE", opacity=o, stroke=NONE)
# the real part: Bob's ticket, dangling from his hand over the ghost
d.path("M376,624 C374,644 366,658 357,668", "Tag string", fill=NONE,
       stroke="#C9A87E", strokeWidth=3, cap="round", opacity=85)
d.shape("rectangle", "Case tag", x=298, y=606, width=86, height=40,
        fill=FOLDER, stroke=INK, strokeWidth=4, radius=6)
d.shape("ellipse", "Tag hole", x=372, y=620, width=8, height=8,
        fill="#3A2A18", stroke=NONE)
d.text("CASE", "Tag word", x=308, y=626, size=12, font="Virelai Sans",
       color="#5A4526", justify="left")
d.text("0444", "Tag number", x=308, y=641, size=13, font="Source Sans 3",
       color="#3A2A18", justify="left")

# --- key haiku line, lettered on the floor band ---------------------------------
k = d.text("the case itself does not.", "Key line", x=500, y=812, size=23,
           font="Virelai Sans", color="#D8BE92", justify="center")
if k and k.get("id"):
    d.cmd("text.setStyle", "key tracking", ids=[k["id"]], tracking=260)

# --- captions --------------------------------------------------------------------
d.text("BUREAU BOB", "Name", x=500, y=930, size=58, font="Virelai Sans",
       color=BONE, justify="center")
r = d.text("RIGHTS IN STATUTE NOT SOFTWARE", "Role", x=500, y=968, size=20,
           font="Virelai Sans", color="#A98E66", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("hai-0444-bureau-bob-V1R00")
