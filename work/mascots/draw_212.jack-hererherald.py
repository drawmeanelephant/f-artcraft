#!/usr/bin/env python3
"""Jack Hererherald — mascot portrait V1R00.
Herald mascot mid-proclamation: gold trumpet up-left with pennant and
sound arcs, scroll in hand, shelves of patient record filings behind in
the archive hall. 1000x1000. House style: gradients + translucent shading."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Jack Hererherald — Mascot Portrait", 1000, 1000)

INK = "#263026"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#0C1610"}, {"offset": 1, "color": "#050A07"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4E7A58"}, {"offset": 0.7, "color": "#2E5240"},
    {"offset": 1, "color": "#1A3226"}]}}
FLOOR = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2E4A38"}, {"offset": 1, "color": "#16241C"}]}}
SHELF = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3E3222"}, {"offset": 1, "color": "#241C12"}]}}
BOX = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#C9B98E"}, {"offset": 1, "color": "#96865C"}]}}
PAPER = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F0EBDC"}, {"offset": 1, "color": "#CFC7AC"}]}}
GOLD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E8C568"}, {"offset": 1, "color": "#A8792E"}]}}
TABARD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#8A4638"}, {"offset": 1, "color": "#5A2E26"}]}}
BODY = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#EEDCBE"}, {"offset": 0.7, "color": "#D2B088"},
    {"offset": 1, "color": "#A87E58"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#6E9A7E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8ECDC", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(190,235,8),(800,230,7),(160,520,9),(830,540,8),
                               (240,760,7),(760,740,9),(130,390,6),(865,390,7),
                               (390,110,7),(610,110,8),(330,820,6),(665,815,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#3E5E48", opacity=45, stroke=NONE)

# --- floor ----------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR, stroke=NONE)
d.shape("ellipse", "Jack shadow", x=420, y=676, width=180, height=30,
        fill="#050C08", opacity=55, stroke=NONE)

# --- archive shelves with record boxes -------------------------------------------
for side, sx in [("L", 125), ("R", 770)]:
    d.shape("rectangle", f"Shelf frame {side}", x=sx, y=300, width=105, height=280,
            fill=SHELF, stroke=INK, strokeWidth=5, radius=4)
    for i, sy in enumerate([310, 400, 490]):
        d.path(f"M{sx+6},{sy+76} L{sx+99},{sy+76}", f"Shelf board {side}{i}",
               fill=NONE, stroke="#1A140C", strokeWidth=5)
        for j in range(2):
            bx = sx + 12 + j*45
            d.shape("rectangle", f"Rec box {side}{i}{j}", x=bx, y=sy+18, width=38, height=56,
                    fill=BOX, stroke=INK, strokeWidth=3, radius=2)
            d.shape("rectangle", f"Box label {side}{i}{j}", x=bx+6, y=sy+34, width=26, height=14,
                    fill=PAPER, stroke="#6E5C3C", strokeWidth=1)
            d.path(f"M{bx+9},{sy+40} L{bx+29},{sy+40} M{bx+9},{sy+44} L{bx+24},{sy+44}",
                   f"Box label lines {side}{i}{j}", fill=NONE, stroke="#8A7A54",
                   strokeWidth=1, opacity=80)
d.text("RX", "Shelf tag L", x=177, y=296, size=14, font="Virelai Sans",
       color="#C9B98E", justify="center")
d.text("REC", "Shelf tag R", x=822, y=296, size=14, font="Virelai Sans",
       color="#C9B98E", justify="center")

# --- misfiled box on the floor (the known failure) --------------------------------
d.path(rot_rect_path(275, 640, 96, 60, -4), "Pamphlet box",
       fill=BOX, stroke=INK, strokeWidth=4)
d.shape("rectangle", "Pamphlet label", x=240, y=622, width=74, height=22,
        fill=PAPER, stroke="#6E5C3C", strokeWidth=1)
d.text("PAMPHLETS?", "Pamphlet label text", x=277, y=637, size=9,
       font="Virelai Sans", color="#5A4A2C", justify="center")
# loose folders spilled beside it
d.path(rot_rect_path(330, 668, 60, 10, 12), "Folder spill 1",
       fill=PAPER, stroke=INK, strokeWidth=3)
d.path(rot_rect_path(345, 656, 54, 9, -8), "Folder spill 2",
       fill=PAPER, stroke=INK, strokeWidth=3)

# --- sound arcs sweeping up-left from the bell ------------------------------------
for i, pth in enumerate(["M318,318 Q278,332 288,372",
                         "M272,272 Q218,292 232,342",
                         "M228,228 Q162,252 178,312"]):
    d.path(pth, f"Sound arc {i+1}", fill=NONE, stroke="#E8C568",
           strokeWidth=5, cap="round", opacity=55)

# --- the mascot ------------------------------------------------------------------
# legs + shoes
d.path("M478,652 L474,686", "Leg L", fill=NONE, stroke="#A87E58",
       strokeWidth=13, cap="round")
d.path("M532,652 L536,686", "Leg R", fill=NONE, stroke="#9A724E",
       strokeWidth=13, cap="round")
d.shape("ellipse", "Shoe L", x=458, y=680, width=32, height=15, fill=INK, stroke=NONE)
d.shape("ellipse", "Shoe R", x=524, y=680, width=32, height=15, fill=INK, stroke=NONE)
# body blob
d.path("M505,455 C570,455 604,505 600,562 C596,625 562,660 505,660 "
       "C448,660 414,625 410,562 C406,505 440,455 505,455 Z",
       "Jack body", fill=BODY, stroke=INK, strokeWidth=6)
# herald tabard over the lower body
d.path("M452,548 C462,602 480,638 505,656 C530,638 548,602 558,548 "
       "C538,562 472,562 452,548 Z",
       "Tabard", fill=TABARD, stroke=INK, strokeWidth=4, join="round")
d.path("M452,548 L505,580 L558,548", "Tabard trim", fill=NONE,
       stroke="#E8C568", strokeWidth=4, join="round", opacity=85)
# leaf emblem on the tabard
d.shape("ellipse", "Leaf emblem", x=494, y=596, width=22, height=30,
        fill="#7FAE68", stroke=INK, strokeWidth=2)
d.path("M505,600 L505,622", "Leaf vein", fill=NONE, stroke="#3E5E38",
       strokeWidth=3, cap="round")
# herald cap with leaf-feather
d.path("M458,462 L458,442 C458,426 478,418 505,418 C532,418 552,426 552,442 L552,462 Z",
       "Herald cap", fill=TABARD, stroke=INK, strokeWidth=5, join="round")
d.path("M544,432 C560,414 576,408 590,414", "Cap feather", fill=NONE,
       stroke="#7FAE68", strokeWidth=8, cap="round")
# face: mid-blast, cheeks puffed
d.shape("ellipse", "Eye L", x=486, y=492, width=14, height=18, fill=INK, stroke=NONE)
d.shape("ellipse", "Eye R", x=534, y=490, width=14, height=18, fill=INK, stroke=NONE)
d.shape("ellipse", "Glint L", x=490, y=496, width=4, height=4, fill="#FFFFFF", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=538, y=494, width=4, height=4, fill="#FFFFFF", opacity=90, stroke=NONE)
d.path("M482,476 L498,474", "Brow L", fill=NONE, stroke=INK, strokeWidth=4, cap="round")
d.path("M532,472 L550,476", "Brow R", fill=NONE, stroke=INK, strokeWidth=4, cap="round")
d.shape("ellipse", "Puffed cheek L", x=470, y=516, width=28, height=20,
        fill="#D8947A", opacity=55, stroke=NONE)
d.shape("ellipse", "Puffed cheek R", x=530, y=514, width=30, height=22,
        fill="#D8947A", opacity=55, stroke=NONE)
# trumpet held to the mouth, angled up-left
d.path("M490,520 L400,432", "Trumpet tube", fill=NONE,
       stroke="#C9A03E", strokeWidth=14, cap="round")
d.path("M484,512 L404,438", "Tube highlight", fill=NONE,
       stroke="#E8C568", strokeWidth=4, cap="round", opacity=75)
d.path("M400,432 L372,352 L338,400 Z", "Trumpet bell",
       fill=GOLD, stroke=INK, strokeWidth=4, join="round")
d.path("M372,352 L338,400", "Bell rim", fill=NONE, stroke="#F0D9A0",
       strokeWidth=6, cap="round")
# pennant hanging below the tube
d.path("M428,458 L428,504 L466,480 Z", "Pennant",
       fill=TABARD, stroke=INK, strokeWidth=3, join="round")
d.path("M428,458 L466,480", "Pennant hoist", fill=NONE, stroke=INK, strokeWidth=2)
d.shape("ellipse", "Mouthpiece", x=484, y=512, width=16, height=14,
        fill=GOLD, stroke=INK, strokeWidth=3)
# arm raised gripping the trumpet
d.path("M455,560 C425,545 408,510 412,478", "Arm trumpet", fill=NONE,
       stroke="#D2B088", strokeWidth=12, cap="round")
d.shape("ellipse", "Grip hand", x=404, y=464, width=18, height=15,
        fill="#EEDCBE", stroke=INK, strokeWidth=3)
# scroll proclamation in the other hand
d.path("M555,560 C585,552 606,540 620,524", "Arm scroll", fill=NONE,
       stroke="#C9A87E", strokeWidth=12, cap="round")
d.shape("ellipse", "Scroll hand", x=614, y=512, width=18, height=15,
        fill="#EEDCBE", stroke=INK, strokeWidth=3)
d.shape("rectangle", "Scroll", x=606, y=468, width=64, height=48,
        fill=PAPER, stroke=INK, strokeWidth=4, radius=3)
d.shape("ellipse", "Scroll roll top", x=604, y=462, width=68, height=12,
        fill=PAPER, stroke=INK, strokeWidth=3)
d.shape("ellipse", "Scroll roll bot", x=604, y=512, width=68, height=12,
        fill=PAPER, stroke=INK, strokeWidth=3)
for i, y in enumerate([482, 492, 502]):
    d.path(f"M616,{y} L660,{y}", f"Scroll line {i+1}", fill=NONE,
           stroke="#8A7A54", strokeWidth=2, opacity=55)

# --- captions ---------------------------------------------------------------------------
d.text("JACK HERERHERALD", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#D8ECDC", justify="center")
r = d.text("PROTOCOL HERALD", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#9AC2A4", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("212.jack-hererherald-V1R00")
