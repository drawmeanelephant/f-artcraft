#!/usr/bin/env python3
"""Bananuity Clause — mascot portrait V1R00.
A Winter Banana mascot in a sugar-dripping parka, standing under frosted
boughs in the night grove. Chaotic yet saccharine.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Bananuity Clause — Mascot Portrait", 1000, 1000)

INK = "#2E2634"
BG_GRAD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000], "stops": [
    {"offset": 0, "color": "#0C1424"}, {"offset": 1, "color": "#05080F"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4E6488"}, {"offset": 0.7, "color": "#31445F"},
    {"offset": 1, "color": "#1A2438"}]}}
SNOW_GRAD = {"gradient": {"kind": "linear", "start": [0, 690], "end": [0, 880], "stops": [
    {"offset": 0, "color": "#D9E4F2"}, {"offset": 1, "color": "#93A8C4"}]}}
FACE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#FBEA9C"}, {"offset": 0.7, "color": "#EFCF6A"},
    {"offset": 1, "color": "#C9A23E"}]}}
PARKA_GRAD = {"gradient": {"kind": "linear", "start": [0, 400], "end": [0, 700], "stops": [
    {"offset": 0, "color": "#4E8A96"}, {"offset": 1, "color": "#274E5C"}]}}
FUR = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F4EDDA"}, {"offset": 1, "color": "#C4B48E"}]}}
GLAZE = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 60], "stops": [
    {"offset": 0, "color": "#FFFFFF"}, {"offset": 1, "color": "#EADFB8"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#5E789E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C9D8EE", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(190,240,8),(800,232,7),(160,520,9),(832,545,8),
                               (246,764,7),(754,748,9),(134,392,6),(862,392,7),
                               (392,114,7),(612,112,8),(334,822,6),(664,820,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#3C5070", opacity=45, stroke=NONE)

# --- distant grove silhouettes --------------------------------------------------
def pine(cx, base, w, h, label):
    y1, y2 = base - h, base
    d.path(f"M{cx},{y1} L{cx+w*0.34},{y1+h*0.42} L{cx+w*0.16},{y1+h*0.42} "
           f"L{cx+w*0.5},{y2} L{cx-w*0.5},{y2} L{cx-w*0.16},{y1+h*0.42} "
           f"L{cx-w*0.34},{y1+h*0.42} Z", label, fill="#22344E",
           opacity=70, stroke=NONE)
pine(215, 690, 76, 150, "Grove tree 1")
pine(300, 690, 60, 115, "Grove tree 2")
pine(700, 690, 64, 125, "Grove tree 3")
pine(785, 690, 82, 160, "Grove tree 4")

# --- snow floor, closed on the disc's own arc -----------------------------------
d.path("M152,690 L848,690 A420,420 0 0 1 152,690 Z", "Snow floor",
       fill=SNOW_GRAD, stroke=NONE)
d.path("M152,690 L848,690", "Snow line", fill=NONE, stroke="#7E94B4",
       strokeWidth=4, opacity=60)
# snow drifts
d.shape("ellipse", "Drift L", x=210, y=700, width=200, height=34,
        fill="#E8F0FA", opacity=55, stroke=NONE)
d.shape("ellipse", "Drift R", x=600, y=715, width=220, height=38,
        fill="#E8F0FA", opacity=50, stroke=NONE)

# --- frosted boughs overhead -----------------------------------------------------
# left bough arcs in from the upper-left rim zone
d.path("M214,262 C300,190 380,165 452,158", "Bough L", fill=NONE,
       stroke="#3A2E22", strokeWidth=13, cap="round")
d.path("M214,252 C300,180 382,155 452,148", "Bough L snow", fill=NONE,
       stroke="#E9F0F8", strokeWidth=7, cap="round", opacity=90)
# right bough arcs in from the upper-right
d.path("M786,262 C700,190 620,165 548,158", "Bough R", fill=NONE,
       stroke="#3A2E22", strokeWidth=13, cap="round")
d.path("M786,252 C700,180 618,155 548,148", "Bough R snow", fill=NONE,
       stroke="#E9F0F8", strokeWidth=7, cap="round", opacity=90)
# twig forks
d.path("M300,208 C320,190 336,168 340,150", "Twig L", fill=NONE,
       stroke="#3A2E22", strokeWidth=7, cap="round")
d.path("M700,208 C680,190 664,168 660,150", "Twig R", fill=NONE,
       stroke="#3A2E22", strokeWidth=7, cap="round")
# hanging icicles + snow clumps
for i, (x, y, h) in enumerate([(268,238,30),(348,190,24),(652,190,24),(732,238,30)]):
    d.path(f"M{x},{y} L{x+5},{y+h} L{x+10},{y} Z", f"Icicle {i+1}",
           fill="#CFE2F2", opacity=80, stroke=NONE)
for i, (x, y, w) in enumerate([(240,232,30),(360,168,26),(614,168,26),(730,232,30)]):
    d.shape("ellipse", f"Snow clump {i+1}", x=x, y=y, width=w, height=w*0.45,
            fill="#F0F6FC", opacity=85, stroke=NONE)

# --- falling snow ----------------------------------------------------------------
for i, (x, y, w, o) in enumerate([(250,330,9,70),(330,290,7,55),(430,250,8,60),
                                  (580,255,7,55),(700,300,8,65),(760,360,9,60),
                                  (200,430,7,50),(810,440,7,50),(300,380,6,45),
                                  (640,380,6,45)]):
    d.shape("ellipse", f"Snowflake {i+1}", x=x, y=y, width=w, height=w,
            fill="#EAF2FA", opacity=o, stroke=NONE)

# --- Bananuity: sugar-dripping parka ---------------------------------------------
d.shape("ellipse", "Clause shadow", x=365, y=668, width=270, height=32,
        fill="#101C2C", opacity=50, stroke=NONE)
# parka body: a rounded coat, wider at the hem
d.path("M500,420 C585,420 640,480 648,570 C652,630 640,672 626,690 "
        "L374,690 C360,672 348,630 352,570 C360,480 415,420 500,420 Z",
       "Parka", fill=PARKA_GRAD, stroke=INK, strokeWidth=6, join="round")
# coat shading + zipper
d.path("M376,540 C400,520 430,512 458,514 L452,690 L388,690 C370,640 366,580 376,540 Z",
       "Coat shade", fill="#1E3C48", opacity=45, stroke=NONE)
d.path("M500,500 L500,688", "Zipper", fill=NONE, stroke="#16303A",
       strokeWidth=6)
for i in range(7):
    d.path(f"M492,{512+i*25} L508,{512+i*25}", f"Zip tooth {i+1}", fill=NONE,
           stroke="#9FC4CC", strokeWidth=3, opacity=70)
# pockets
d.path("M396,600 L452,600 L448,644 L392,644 Z", "Pocket L", fill="#224450",
       stroke=INK, strokeWidth=4, join="round")
d.path("M548,600 L604,600 L608,644 L552,644 Z", "Pocket R", fill="#224450",
       stroke=INK, strokeWidth=4, join="round")

# hood ring with fur trim around the face
d.path("M500,330 C575,330 630,385 630,448 C630,505 575,540 500,540 "
        "C425,540 370,505 370,448 C370,385 425,330 500,330 Z",
       "Hood", fill=PARKA_GRAD, stroke=INK, strokeWidth=6)
# sugar cap poured over the hood dome, slipping off the left side
d.path("M398,372 C410,336 480,318 545,330 C540,342 548,352 536,350 "
        "C522,346 518,366 504,358 C492,351 480,372 466,362 C454,353 442,374 "
        "428,364 C416,356 406,386 396,380 C394,378 394,375 398,372 Z",
       "Hood glaze", fill=GLAZE, stroke=INK, strokeWidth=4, join="round", opacity=95)
d.path("M398,382 C404,410 398,430 388,436 C382,422 386,398 398,382 Z",
       "Hood drip L", fill=GLAZE, stroke=INK, strokeWidth=3)
d.path("M540,352 C548,368 548,388 538,396 C532,384 532,364 540,352 Z",
       "Hood drip R", fill=GLAZE, stroke=INK, strokeWidth=3)
# fur trim: scalloped ring of small puffs
for i, (x, y, w) in enumerate([(404,420,26),(414,384,28),(436,352,28),(468,334,28),
                               (504,332,28),(538,342,28),(566,366,28),(584,398,28),
                               (590,432,26)]):
    d.shape("ellipse", f"Fur puff {i+1}", x=x-w/2, y=y-w/2, width=w, height=w,
            fill=FUR, stroke=INK, strokeWidth=3)

# face: the Winter Banana, chaotic yet saccharine
d.shape("ellipse", "Face", x=430, y=372, width=140, height=140,
        fill=FACE_GRAD, stroke=INK, strokeWidth=5)
d.shape("ellipse", "Face hi", x=450, y=390, width=52, height=24,
        fill="#FFFFFF", opacity=30, stroke=NONE)
# mismatched eyes: left wide, right a dizzy squint, brows askew
d.shape("ellipse", "Eye L", x=458, y=418, width=26, height=32,
        fill="#FDF8E2", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Pupil L", x=466, y=430, width=10, height=12,
        fill=INK, stroke=NONE)
d.path("M508,430 C514,422 528,420 536,426 C540,430 536,438 528,438 "
       "C522,438 520,432 524,428", "Eye R spiral", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.path("M450,404 C458,394 474,392 484,398", "Brow L", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.path("M512,398 C524,388 542,392 548,402", "Brow R", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
# big open saccharine grin
d.path("M462,470 C480,492 522,492 540,468 C528,500 474,500 462,470 Z",
       "Grin", fill="#7A3A3E", stroke=INK, strokeWidth=4, join="round")
d.path("M478,486 C492,494 512,494 524,486", "Tongue", fill=NONE,
       stroke="#D98A8E", strokeWidth=6, cap="round")
# blush
d.shape("ellipse", "Blush L", x=442, y=456, width=24, height=13,
        fill="#E89A6E", opacity=55, stroke=NONE)
d.shape("ellipse", "Blush R", x=536, y=452, width=24, height=13,
        fill="#E89A6E", opacity=55, stroke=NONE)

# --- sugar glaze: pooling at the hem ---------------------------------------------
# glaze blob sliding off the left shoulder
d.path("M352,540 C368,512 408,505 430,518 C424,530 428,548 416,546 "
        "C406,544 402,560 392,552 C384,546 372,560 362,552 C356,548 352,546 352,540 Z",
       "Shoulder glaze", fill=GLAZE, stroke=INK, strokeWidth=4, join="round", opacity=95)
d.path("M366,556 C372,576 368,594 360,600 C354,588 356,568 366,556 Z",
       "Shoulder drip", fill=GLAZE, stroke=INK, strokeWidth=3)
# glaze pooling along the hem, wavy top edge
d.path("M362,690 L362,664 C392,644 420,668 452,654 C484,640 516,668 548,654 "
        "C580,642 612,664 638,654 L638,690 Z",
       "Hem glaze", fill=GLAZE, stroke=INK, strokeWidth=4, join="round", opacity=95)
# two drips spilling over the hem onto the snow
d.path("M420,690 C424,704 420,716 412,720 C406,710 410,696 420,690 Z",
       "Hem drip 1", fill=GLAZE, stroke=INK, strokeWidth=3)
d.path("M580,690 C586,702 582,714 574,718 C568,708 570,696 580,690 Z",
       "Hem drip 2", fill=GLAZE, stroke=INK, strokeWidth=3)
# stray sugar sparkles
for i, (x, y) in enumerate([(420,560),(570,560),(500,640)]):
    d.path(f"M{x},{y-9} L{x+3},{y-3} L{x+9},{y} L{x+3},{y+3} L{x},{y+9} "
           f"L{x-3},{y+3} L{x-9},{y} L{x-3},{y-3} Z", f"Sparkle {i+1}",
           fill="#FFF6DC", opacity=80, stroke=NONE)
# dropped glaze splash on the snow
d.shape("ellipse", "Snow splash", x=430, y=700, width=80, height=16,
        fill="#F2ECD8", opacity=70, stroke=NONE)

# --- captions -------------------------------------------------------------------
d.text("BANANUITY CLAUSE", "Name", x=500, y=930, size=56, font="Virelai Sans",
       color="#C9D8EE", justify="center")
r = d.text("SWEET DISRUPTOR", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#8CA4C6", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("220.bananuity-clause-V1R00")
