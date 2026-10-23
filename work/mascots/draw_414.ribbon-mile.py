#!/usr/bin/env python3
"""Ribbon Mile — mascot portrait V1R00.
Cartographer beside a wall map whose route runs off the map, across the wall,
and into the hallway arch. 1000x1000. Gradients + translucency, never flat."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Ribbon Mile — Mascot Portrait", 1000, 1000)

INK = "#2E2A28"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#111814"}, {"offset": 1, "color": "#060A08"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#93A894"}, {"offset": 0.7, "color": "#637E6C"},
    {"offset": 1, "color": "#38493E"}]}}
BODY = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F2D8B0"}, {"offset": 0.72, "color": "#D4AE7E"},
    {"offset": 1, "color": "#A87E52"}]}}
PARCH = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F0E4C4"}, {"offset": 1, "color": "#D4C394"}]}}
FRAME = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6E4E34"}, {"offset": 1, "color": "#46301E"}]}}
ROUTE = "#C4442E"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#6E8674", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#DEE8DA", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(205,230,8),(790,238,7),(170,536,9),(822,556,8),
                               (255,750,7),(745,744,9),(145,398,6),(852,406,7),
                               (398,116,7),(602,114,8),(340,812,6),(660,810,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#4C6354", opacity=45, stroke=NONE)

# --- floor (closes on the plate's own arc) -------------------------------------
d.path("M208,740 L792,740 A420,420 0 0 1 208,740 Z", "Floor",
       fill="#3E5248", stroke=NONE)
d.path("M208,740 L792,740", "Skirting", fill=NONE, stroke="#2E3E36",
       strokeWidth=6, opacity=80)
for i, (x1, x0) in enumerate([(300,420),(430,470),(570,530),(700,580)]):
    d.path(f"M{x1},812 L{x0},742", f"Floorboard {i+1}", fill=NONE,
           stroke="#31443A", strokeWidth=3, opacity=60)

# --- hallway arch on the right wall --------------------------------------------
d.path("M700,750 L700,440 C700,368 720,330 745,330 C770,330 782,368 782,440 "
       "L782,750 Z", "Hallway arch", fill="#101A12", stroke=INK, strokeWidth=6)
d.path("M712,750 L712,452 C712,392 728,356 745,356 C762,356 770,392 770,452 "
       "L770,750 Z", "Hallway inner", fill="#1B2A1E", stroke=NONE)
# corridor hint inside: receding doorframes
d.path("M722,750 L722,468 C722,418 733,388 745,388 C757,388 764,418 764,468 L764,750",
       "Hall frame 1", fill=NONE, stroke="#2E4434", strokeWidth=4, opacity=80)
d.path("M732,750 L732,486 C732,448 738,428 745,428 C752,428 756,448 756,486 L756,750",
       "Hall frame 2", fill=NONE, stroke="#243829", strokeWidth=3, opacity=70)
# faint warm light deep inside
d.shape("ellipse", "Hall glow", x=733, y=540, width=26, height=110,
        fill="#E8CE8E", opacity=12, stroke=NONE)

# --- the wall map --------------------------------------------------------------
d.shape("rectangle", "Map frame", x=262, y=272, width=330, height=268,
        fill=FRAME, stroke=INK, strokeWidth=6, radius=6)
d.shape("rectangle", "Map paper", x=278, y=288, width=298, height=236,
        fill=PARCH, stroke=NONE)
# coastlines
d.path("M300,340 C330,320 360,332 385,318 C410,306 440,320 452,344 "
       "C430,356 415,378 420,404 C390,398 366,410 340,398 C318,388 302,366 300,340 Z",
       "Coastline", fill="#C9B88C", opacity=55, stroke="#8A7A54",
       strokeWidth=3)
d.path("M480,440 C510,428 545,438 560,462 C545,482 505,484 486,466 "
       "C476,456 472,446 480,440 Z",
       "Coastline 2", fill="#C9B88C", opacity=55, stroke="#8A7A54",
       strokeWidth=3)
# grid lines
for i, x in enumerate(range(310, 570, 52)):
    d.path(f"M{x},292 L{x},520", f"Grid V{i+1}", fill=NONE, stroke="#BBA87E",
           strokeWidth=1.5, opacity=60)
for i, y in enumerate(range(316, 520, 46)):
    d.path(f"M282,{y} L572,{y}", f"Grid H{i+1}", fill=NONE, stroke="#BBA87E",
           strokeWidth=1.5, opacity=60)
# route on the map: dashed ribbon with pins, heading for the right edge
d.path("M310,480 C360,470 370,420 415,415 C460,410 480,445 520,430 "
       "C548,420 560,420 574,422", "Route on map", fill=NONE, stroke=ROUTE,
       strokeWidth=7, cap="round", dash=[12, 9])
d.shape("ellipse", "Pin start", x=302, y=472, width=16, height=16,
        fill=ROUTE, stroke=INK, strokeWidth=3)
d.path("M404,406 L412,406 L408,418 Z", "Pin mid flag", fill=ROUTE, stroke=INK,
       strokeWidth=2)
d.path("M408,384 L408,406", "Pin mid pole", fill=NONE, stroke=INK, strokeWidth=3)
d.shape("ellipse", "Pin exit", x=568, y=414, width=14, height=14,
        fill=ROUTE, stroke=INK, strokeWidth=3)
# the route leaves the map, crosses the wall, enters the hallway
d.path("M582,422 C620,418 648,426 676,440 C694,449 706,458 714,468",
       "Route off-wall", fill=NONE, stroke=ROUTE,
       strokeWidth=7, cap="round", dash=[12, 9])
# inside the hallway the dashes shrink into the dark
d.path("M714,468 C722,480 732,494 742,510", "Route deep", fill=NONE,
       stroke=ROUTE, strokeWidth=4, cap="round", dash=[6, 7], opacity=75)

# --- the cartographer ----------------------------------------------------------
d.shape("ellipse", "Shadow", x=430, y=730, width=190, height=34,
        fill="#2E3E36", opacity=55, stroke=NONE)
d.path("M525,470 C600,470 646,530 648,610 C650,685 610,742 525,742 "
       "C440,742 400,685 402,610 C404,530 450,470 525,470 Z",
       "Body", fill=BODY, stroke=INK, strokeWidth=7)
d.shape("ellipse", "Body highlight", x=455, y=485, width=110, height=44,
        fill="#FFFFFF", opacity=22, stroke=NONE)
# cartographer's cap with compass star
d.path("M455,472 C460,430 495,408 535,412 C570,416 592,442 592,472 Z",
       "Cap", fill="#7A4A38", stroke=INK, strokeWidth=6, join="round")
d.shape("star", "Cap star", cx=522, cy=438, radius1=13, radius2=5, points=4,
        fill="#E8CE8E", stroke=INK, strokeWidth=3)
# rolled chart under the left arm
d.path("M420,620 C408,650 410,680 424,700", "Chart tube", fill=NONE,
       stroke=PARCH, strokeWidth=26, cap="round")

d.shape("ellipse", "Chart rim", x=402, y=692, width=36, height=20,
        fill="#D4C394", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Chart hole", x=413, y=698, width=14, height=8,
        fill="#8A7A54", stroke=INK, strokeWidth=2)
# face: surveying, one eye toward the route, pleased
d.shape("ellipse", "Eye L", x=465, y=530, width=26, height=30, fill="#FBF6E8",
        stroke=INK, strokeWidth=5)
d.shape("ellipse", "Eye R", x=555, y=530, width=26, height=30, fill="#FBF6E8",
        stroke=INK, strokeWidth=5)
d.shape("ellipse", "Pupil L", x=474, y=538, width=11, height=13, fill=INK, stroke=NONE)
d.shape("ellipse", "Pupil R", x=564, y=538, width=11, height=13, fill=INK, stroke=NONE)
d.path("M460,510 L492,504", "Brow L", fill=NONE, stroke=INK, strokeWidth=5, cap="round")
d.path("M556,504 L588,510", "Brow R", fill=NONE, stroke=INK, strokeWidth=5, cap="round")
d.path("M492,586 C512,600 540,600 558,586", "Smile", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
d.shape("ellipse", "Blush L", x=444, y=560, width=24, height=14, fill="#DE9B72",
        opacity=55, stroke=NONE)
d.shape("ellipse", "Blush R", x=582, y=560, width=24, height=14, fill="#DE9B72",
        opacity=55, stroke=NONE)
# right arm up, tracing the route toward the hallway
d.path("M640,560 C665,540 685,510 695,478", "Arm R", fill=NONE, stroke=BODY,
       strokeWidth=22, cap="round")
d.shape("ellipse", "Hand R", x=684, y=456, width=28, height=30, fill=BODY,
        stroke=INK, strokeWidth=5)
# pencil in the tracing hand
d.path("M700,462 L722,432", "Pencil", fill=NONE, stroke="#D8A24A",
       strokeWidth=7, cap="round")
d.path("M722,432 L726,425", "Pencil tip", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
# left arm hugging the chart
d.path("M420,610 C400,630 398,655 410,672", "Arm L", fill=NONE, stroke=BODY,
       strokeWidth=22, cap="round")
# little boots
d.shape("ellipse", "Boot L", x=460, y=728, width=48, height=28, fill="#5E4630",
        stroke=INK, strokeWidth=5)
d.shape("ellipse", "Boot R", x=548, y=728, width=48, height=28, fill="#5E4630",
        stroke=INK, strokeWidth=5)

# --- captions ------------------------------------------------------------------
d.text("RIBBON MILE", "Name", x=500, y=930, size=56, font="Virelai Sans",
       color="#DEE8DA", justify="center")
r = d.text("CARTOGRAPHER OF EXITS", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#9DB89E", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("414.ribbon-mile-V1R00")
