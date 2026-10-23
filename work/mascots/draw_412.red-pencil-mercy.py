#!/usr/bin/env python3
"""Red Pencil Mercy — mascot portrait V1R00.
Mascot correcting a contract with a red pencil, margins crowded with red marks.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Red Pencil Mercy — Mascot Portrait", 1000, 1000)

INK = "#3A2A30"
RED = "#C03028"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#221016"}, {"offset": 1, "color": "#0D0509"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#C98F8F"}, {"offset": 0.7, "color": "#9A5E64"},
    {"offset": 1, "color": "#61363C"}]}}
BODY = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E2DCEE"}, {"offset": 0.72, "color": "#B4AACB"},
    {"offset": 1, "color": "#857A9E"}]}}
PAPER = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F4ECDA"}, {"offset": 1, "color": "#DCCFAC"}]}}
PENCIL = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#DE4A40"}, {"offset": 1, "color": "#8E221E"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#A0686C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F0D8D4", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(205,228,8),(792,235,7),(168,535,9),(824,555,8),
                               (252,752,7),(745,745,9),(145,395,6),(852,408,7),
                               (396,118,7),(604,112,8),(338,812,6),(662,810,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#7E4A50", opacity=45, stroke=NONE)

# --- mascot leaning in from the top -------------------------------------------
# small mercy halo
d.shape("ellipse", "Halo", x=448, y=252, width=104, height=30,
        fill=NONE, stroke="#E8C85E", strokeWidth=7, opacity=85)
d.shape("ellipse", "Halo glow", x=430, y=240, width=140, height=54,
        fill="#E8C85E", opacity=12, stroke=NONE)
# body — shoulders hidden behind the contract
d.path("M500,330 C580,330 632,390 636,470 C639,540 600,580 500,580 "
       "C400,580 361,540 364,470 C368,390 420,330 500,330 Z",
       "Body", fill=BODY, stroke=INK, strokeWidth=7)
d.shape("ellipse", "Body highlight", x=430, y=345, width=110, height=44,
        fill="#FFFFFF", opacity=22, stroke=NONE)
# face: kind, half-lowered lids, gentle smile
d.path("M440,430 C448,438 462,438 470,430", "Eye L soft", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
d.path("M530,430 C538,438 552,438 560,430", "Eye R soft", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
d.path("M430,408 C444,400 462,398 476,402", "Lid L", fill=NONE, stroke=INK,
       strokeWidth=4, cap="round")
d.path("M524,402 C538,398 556,400 570,408", "Lid R", fill=NONE, stroke=INK,
       strokeWidth=4, cap="round")
d.path("M472,478 C490,492 512,492 528,478", "Gentle smile", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
d.shape("ellipse", "Blush L", x=420, y=452, width=28, height=16, fill="#E89B8A",
        opacity=50, stroke=NONE)
d.shape("ellipse", "Blush R", x=552, y=452, width=28, height=16, fill="#E89B8A",
        opacity=50, stroke=NONE)
# left arm braced on the contract's top edge
d.path("M388,520 C365,545 355,565 352,585", "Arm L", fill=NONE, stroke=BODY,
       strokeWidth=24, cap="round")
d.shape("ellipse", "Hand L", x=336, y=578, width=32, height=26, fill=BODY,
        stroke=INK, strokeWidth=5)
# right arm reaching the pencil down onto the page
d.path("M612,520 C628,548 630,568 622,590", "Arm R", fill=NONE, stroke=BODY,
       strokeWidth=24, cap="round")

# --- the contract --------------------------------------------------------------
d.shape("rectangle", "Contract", x=295, y=560, width=410, height=215,
        fill=PAPER, stroke=INK, strokeWidth=6, radius=6)
d.shape("rectangle", "Contract head band", x=315, y=578, width=130, height=16,
        fill="#B8A888", stroke=NONE, opacity=80)
d.text("CONTRACT", "Contract head", x=380, y=591, size=12, font="Virelai Sans",
       color="#8A7A5C", justify="center")
# body text lines
for i, y in enumerate(range(614, 750, 19)):
    w = 340 if i % 4 != 3 else 250
    d.shape("rectangle", f"Line {i+1}", x=330, y=y, width=w, height=7,
            fill="#A89878", stroke=NONE, opacity=75, radius=3)
# --- red marks crowding the margins -------------------------------------------
# strikethroughs
for i, (x, y, w) in enumerate([(332,622,150),(334,678,120),(335,716,180)]):
    d.path(f"M{x},{y+4} L{x+w},{y+4}", f"Strike {i+1}", fill=NONE, stroke=RED,
           strokeWidth=4, cap="round", opacity=85)
# insertion carets between lines
for i, (x, y) in enumerate([(500,641),(560,698),(452,660)]):
    d.path(f"M{x},{y} L{x+7},{y-9} L{x+14},{y}", f"Caret {i+1}", fill=NONE,
           stroke=RED, strokeWidth=3.5, cap="round", join="round", opacity=85)
# circled clause on line 5
d.shape("ellipse", "Circled clause", x=420, y=686, width=120, height=22,
        fill=NONE, stroke=RED, strokeWidth=3.5, opacity=85)
# margin scribbles — crowded left and right margins
for i, (x, y) in enumerate([(308,612),(306,652),(310,694),(306,736),
                            (688,616),(690,658),(686,700),(690,740)]):
    d.path(f"M{x},{y} c3,-6 9,-6 12,0 c-3,6 -9,6 -12,0", f"Margin mark {i+1}",
           fill=NONE, stroke=RED, strokeWidth=3, opacity=70)
# one merciful star of approval
d.shape("star", "Mercy star", cx=672, cy=566, radius1=14, radius2=5, points=5,
        fill="#DE6A5E", stroke=RED, strokeWidth=2, opacity=90)

# --- the red pencil, gripped by the right hand ---------------------------------
# pencil body diagonal, tip at page
d.path("M472,652 L588,556 L618,576 L500,672 Z", "Pencil body", fill=PENCIL,
       stroke=INK, strokeWidth=5, join="round")
# wood + graphite tip
d.path("M472,652 L500,672 L488,686 L462,664 Z", "Pencil wood",
       fill="#E8C89A", stroke=INK, strokeWidth=4, join="round")
d.path("M462,664 L488,686 L470,694 Z", "Pencil tip", fill=INK, stroke=NONE)
# eraser + ferrule
d.path("M588,556 L618,576 L636,556 L606,536 Z", "Ferrule", fill="#C8B892",
       stroke=INK, strokeWidth=4, join="round")
d.path("M606,536 L636,556 L648,542 L620,522 Z", "Eraser", fill="#E89B8A",
       stroke=INK, strokeWidth=4, join="round")
# hand over the grip
d.shape("ellipse", "Hand R", x=584, y=568, width=34, height=30, fill=BODY,
        stroke=INK, strokeWidth=5)
# fresh red line just drawn
d.path("M472,700 L540,704", "Fresh mark", fill=NONE, stroke=RED, strokeWidth=5,
       cap="round")

# --- captions ------------------------------------------------------------------
d.text("RED PENCIL MERCY", "Name", x=500, y=930, size=56, font="Virelai Sans",
       color="#F0D8D4", justify="center")
r = d.text("MERCY IN THE MARGINS", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#C99090", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("412.red-pencil-mercy-V1R00")
