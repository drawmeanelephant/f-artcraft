#!/usr/bin/env python3
"""Htmlie Structura — mascot portrait V1R00.
Guardian of document structure: angle-bracket armor, blueprint scroll
tucked under one arm, chalkboard of nesting diagrams behind. Stern,
unwavering. 1000x1000. Gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Htmlie Structura — Mascot Portrait", 1000, 1000)

INK = "#22242E"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#12202E"}, {"offset": 1, "color": "#070D14"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4A6A80"}, {"offset": 0.7, "color": "#2A4254"},
    {"offset": 1, "color": "#141F2C"}]}}
ARMOR = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#93A2B6"}, {"offset": 1, "color": "#4C5A70"}]}}
ARMOR_DK = "#36435A"
FACE = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F0E2C6"}, {"offset": 1, "color": "#D2B98F"}]}}
BOARD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#23423A"}, {"offset": 1, "color": "#122620"}]}}
CHALK = "#DCE8DA"
FRAME_W = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7A5C3A"}, {"offset": 1, "color": "#4E3A20"}]}}
SCROLL = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2E5078"}, {"offset": 1, "color": "#1C3550"}]}}
CYAN = "#7FC8E4"
BRASS = "#C9A45C"

def bracket(cx, cy, s, direction, label, color=CHALK, w=5, op=None):
    # an angle bracket drawn as two strokes — < or >
    sg = -1 if direction == "left" else 1
    kw = {"fill": NONE, "stroke": color, "strokeWidth": w,
          "cap": "round", "join": "round"}
    if op is not None:
        kw["opacity"] = op
    d.path(f"M{cx + sg*s},{cy - s} L{cx - sg*s},{cy} L{cx + sg*s},{cy + s}",
           label, **kw)

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#54708A", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C4D8E8", strokeWidth=3, opacity=45)
for i, (x, y, w) in enumerate([(193,232,8),(800,234,7),(158,522,9),(835,542,8),
                               (245,768,7),(755,746,9),(132,392,6),(862,394,7),
                               (390,110,7),(614,112,8),(332,824,6),(666,818,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#1C2C3C", opacity=50, stroke=NONE)

# faint blueprint grid ghosts behind everything
for i, x in enumerate(range(220, 800, 80)):
    d.path(f"M{x},150 L{x},640", f"Grid v {i+1}", fill=NONE,
           stroke="#5E7C96", strokeWidth=2, opacity=10)
for i, y in enumerate(range(160, 660, 80)):
    d.path(f"M200,{y} L800,{y}", f"Grid h {i+1}", fill=NONE,
           stroke="#5E7C96", strokeWidth=2, opacity=10)

# --- chalkboard of nesting diagrams -------------------------------------------
d.path(rot_rect_path(500, 268, 560, 250, 0), "Board frame",
       fill=FRAME_W, stroke=INK, strokeWidth=6)
d.path(rot_rect_path(500, 268, 530, 220, 0), "Board", fill=BOARD,
       stroke=INK, strokeWidth=4)
# chalk nesting diagram: bracket row, indented child rows, one struck out
rows = [(270, 186, 0), (300, 216, 1), (300, 246, 1), (330, 276, 2), (300, 306, 1)]
for i, (bx, by, depth) in enumerate(rows):
    bracket(bx, by, 11, "left", f"Nest open {i+1}", w=4, op=90)
    bracket(bx + 96 + depth * 30, by, 11, "right",
            f"Nest close {i+1}", w=4, op=90)
    d.shape("rectangle", f"Nest tag {i+1}", x=bx + 18, y=by - 5,
            width=60 + depth * 30, height=10, fill=CHALK, opacity=60,
            stroke=NONE)
# the invalid row, corrected in red chalk
d.shape("rectangle", "Bad tag", x=288, y=330, width=52, height=10,
        fill="#E4A89A", opacity=80, stroke=NONE)
d.path("M276,322 L352,344 M352,322 L276,344", "Bad X", fill=NONE,
       stroke="#E08A78", strokeWidth=4, cap="round", opacity=90)
# chalk tray with a nub of chalk
d.shape("rectangle", "Chalk tray", x=380, y=384, width=240, height=10,
        fill=FRAME_W, stroke=INK, strokeWidth=3)
d.shape("rectangle", "Chalk nub", x=560, y=376, width=26, height=8,
        fill=CHALK, stroke=NONE)

# --- ground -------------------------------------------------------------------
d.shape("ellipse", "Ground", x=240, y=700, width=520, height=84,
        fill="#0C1218", opacity=75, stroke=NONE)

# --- htmlie: the guardian --------------------------------------------------------
# torso: breastplate
d.path("M500,445 C575,445 628,495 636,565 C642,625 638,672 632,730 "
       "L368,730 C362,672 358,625 364,565 C372,495 425,445 500,445 Z",
       "Breastplate", fill=ARMOR, stroke=INK, strokeWidth=7)
# center ridge + rivets
d.path("M500,460 L500,720", "Ridge", fill=NONE, stroke=ARMOR_DK,
       strokeWidth=5, opacity=80)
for i, (x, y) in enumerate([(430,520),(570,520),(420,620),(580,620),(470,690),(530,690)]):
    d.shape("ellipse", f"Rivet {i+1}", x=x-4, y=y-4, width=8, height=8,
            fill=BRASS, stroke=INK, strokeWidth=2)
# fauld: two overlapping plate bands at the waist
d.path("M378,700 L622,700 L626,722 L374,722 Z", "Fauld band",
       fill=ARMOR_DK, stroke=INK, strokeWidth=4, join="round", opacity=90)
# chest emblem: <> in brass
bracket(462, 590, 16, "left", "Emblem <", color=BRASS, w=6)
bracket(538, 590, 16, "right", "Emblem >", color=BRASS, w=6)
d.shape("rectangle", "Emblem tag", x=490, y=582, width=20, height=16,
        fill=BRASS, stroke=INK, strokeWidth=3)

# pauldrons: giant angle brackets, < left and > right
d.path("M436,486 L362,522 L436,558", "Pauldron L", fill=NONE,
       stroke=ARMOR, strokeWidth=34, cap="round", join="round")
d.path("M564,486 L638,522 L564,558", "Pauldron R", fill=NONE,
       stroke=ARMOR, strokeWidth=34, cap="round", join="round")
# ink edge on the bracket pauldrons
d.path("M446,478 L358,522 L446,566 M554,478 L642,522 L554,566",
       "Pauldron edges", fill=NONE, stroke=INK, strokeWidth=5,
       cap="round", join="round", opacity=85)

# head: stern guardian
d.shape("ellipse", "Head", x=422, y=305, width=156, height=148,
        fill=FACE, stroke=INK, strokeWidth=7)
# helm: circlet band + cheek guards + <> crest
d.path("M424,330 C424,292 576,292 576,330 L576,344 L424,344 Z",
       "Helm crown", fill=ARMOR, stroke=INK, strokeWidth=6, join="round")
d.path("M424,344 C460,356 540,356 576,344", "Helm band line", fill=NONE,
       stroke=ARMOR_DK, strokeWidth=4, opacity=80)
d.shape("ellipse", "Helm stud", x=494, y=306, width=12, height=10,
        fill=BRASS, stroke=INK, strokeWidth=3)
bracket(474, 316, 9, "left", "Crest <", color=BRASS, w=4)
bracket(526, 316, 9, "right", "Crest >", color=BRASS, w=4)
# cheek guards
d.path("M424,344 L436,344 L436,410 C430,396 424,372 424,344 Z",
       "Cheek L", fill=ARMOR, stroke=INK, strokeWidth=4)
d.path("M576,344 L564,344 L564,410 C570,396 576,372 576,344 Z",
       "Cheek R", fill=ARMOR, stroke=INK, strokeWidth=4)
# unwavering eyes, level brows, set mouth
d.shape("ellipse", "Eye L", x=452, y=366, width=26, height=26, fill="#FBF4E2",
        stroke=INK, strokeWidth=4)
d.shape("ellipse", "Eye R", x=522, y=366, width=26, height=26, fill="#FBF4E2",
        stroke=INK, strokeWidth=4)
d.shape("ellipse", "Pupil L", x=461, y=374, width=9, height=10, fill=INK,
        stroke=NONE)
d.shape("ellipse", "Pupil R", x=530, y=374, width=9, height=10, fill=INK,
        stroke=NONE)
d.path("M448,350 L480,350", "Brow L", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
d.path("M520,350 L552,350", "Brow R", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
d.path("M472,424 C486,420 514,420 528,424", "Set mouth", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")

# --- blueprint scroll under the left arm ----------------------------------------
# roll tucked against the ribs, flap unrolling toward the viewer
d.path("M316,560 L316,700", "Scroll roll", fill=NONE, stroke=FRAME_W,
       strokeWidth=30, cap="round")
d.shape("ellipse", "Scroll cap top", x=301, y=546, width=30, height=16,
        fill=BRASS, stroke=INK, strokeWidth=4)
d.path("M330,600 C360,640 400,662 444,670 L420,730 C366,716 330,672 316,640 Z",
       "Scroll flap", fill=SCROLL, stroke=INK, strokeWidth=5, join="round")
# blueprint content on the flap: nested rectangles + a bracket diagram
d.path("M344,620 L356,660 L390,668 L378,628 Z", "Blueprint box 1",
       fill=NONE, stroke=CYAN, strokeWidth=3, opacity=90)
d.path("M352,632 L360,654 L378,658 L370,636 Z", "Blueprint box 2",
       fill=NONE, stroke=CYAN, strokeWidth=2, opacity=70)
d.path("M398,672 L428,680 M402,664 L424,646", "Blueprint marks",
       fill=NONE, stroke=CYAN, strokeWidth=3, opacity=70)
# arm L cradling the roll
d.path("M398,540 C362,566 342,600 336,632", "Arm L", fill=NONE,
       stroke=ARMOR, strokeWidth=30, cap="round")
d.shape("ellipse", "Hand L", x=318, y=622, width=32, height=26, fill=FACE,
        stroke=INK, strokeWidth=5)

# right gauntlet raised: halt — no structure, no meaning
d.path("M604,540 C640,520 664,494 676,460", "Arm R", fill=NONE,
       stroke=ARMOR, strokeWidth=30, cap="round")
d.shape("ellipse", "Gauntlet palm", x=664, y=400, width=52, height=60,
        fill=ARMOR, stroke=INK, strokeWidth=6)
for i, x in enumerate([668, 682, 696, 710]):
    d.shape("rectangle", f"Finger {i+1}", x=x, y=388, width=11, height=24,
            fill=ARMOR, stroke=INK, strokeWidth=3)
d.shape("ellipse", "Thumb", x=656, y=428, width=18, height=22, fill=ARMOR,
        stroke=INK, strokeWidth=4)

# --- captions -------------------------------------------------------------------
d.text("HTMLIE STRUCTURA", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#DCE8F0", justify="center")
r = d.text("GUARDIAN OF DOCUMENT STRUCTURE", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#8FB8CC", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("014.htmlie-structura-V1R00")
