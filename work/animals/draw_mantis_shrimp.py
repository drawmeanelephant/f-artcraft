#!/usr/bin/env python3
"""Mantis shrimp — field-guide plate V1R00. Side view: emerald/teal segmented
body, folded red-orange raptorial club, banded stalked eyes, tail fan.
Jewel tones + iridescent accents via layered translucent strokes. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Mantis Shrimp — Field Plate", 1000, 1000)

INK = "#332E33"   # warm dark plum, not black
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#0D2433"}, {"offset": 1, "color": "#04101A"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#DCEFE8"}, {"offset": 0.7, "color": "#A5D5C8"},
    {"offset": 1, "color": "#6FA89B"}]}}
CARAPACE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4BDDBB"}, {"offset": 0.6, "color": "#1FA98B"},
    {"offset": 1, "color": "#0D7263"}]}}
SEG_GRAD_A = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3AD0B4"}, {"offset": 1, "color": "#127A66"}]}}
SEG_GRAD_B = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#35BCC8"}, {"offset": 1, "color": "#0E7280"}]}}
CLAW_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#FFB36A"}, {"offset": 0.55, "color": "#E8562E"},
    {"offset": 1, "color": "#A82E14"}]}}
EYE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#9FF0D2"}, {"offset": 0.65, "color": "#2FA87E"},
    {"offset": 1, "color": "#0E5E4E"}]}}
TAIL_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#46D8BC"}, {"offset": 0.6, "color": "#1B9E82"},
    {"offset": 1, "color": "#0B6858"}]}}

# --- backdrop + plate ----------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#4F8A80", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E2F4EC", strokeWidth=3, opacity=60)
# plate patina + reef specks
d.shape("ellipse", "Patina 1", x=170, y=190, width=230, height=140,
        fill="#8FBFB2", opacity=24, stroke=NONE)
d.shape("ellipse", "Patina 2", x=600, y=650, width=260, height=150,
        fill="#8FBFB2", opacity=22, stroke=NONE)
for i, (x, y, w) in enumerate([(200,310,8),(760,250,7),(170,560,9),(800,560,8),
                               (250,760,7),(730,745,9),(135,420,6),(855,410,7),
                               (400,125,7),(590,115,8),(335,825,6),(660,825,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#5F9386", opacity=40, stroke=NONE)
# rising bubbles, left side
for i, (x, y, w) in enumerate([(185,620,18),(162,545,12),(190,465,22),(165,385,14),(188,305,10)]):
    d.shape("ellipse", f"Bubble {i+1}", x=x, y=y, width=w, height=w,
            fill="#FFFFFF", opacity=16, stroke=NONE)

# --- drop shadow under the animal ----------------------------------------------
d.shape("ellipse", "Shrimp shadow", x=280, y=660, width=480, height=42,
        fill="#28504A", opacity=25, stroke=NONE)

# --- tail fan (drawn first so the last body segment overlaps its base) ---------
# upper uropod
d.path("M715,468 C758,436 802,418 830,428 C836,453 800,485 748,498 "
       "C730,502 714,488 715,468 Z",
       "Uropod upper", fill=TAIL_GRAD, stroke=INK, strokeWidth=5)
# lower uropod
d.path("M718,548 C758,578 802,598 828,600 C832,624 796,638 750,618 "
       "C726,606 714,576 718,548 Z",
       "Uropod lower", fill=TAIL_GRAD, stroke=INK, strokeWidth=5)
# telson: the broad middle blade
d.path("M720,472 C768,466 814,492 828,532 C834,562 814,592 776,596 "
       "C746,599 720,582 716,552 C713,526 712,498 720,472 Z",
       "Telson", fill=TAIL_GRAD, stroke=INK, strokeWidth=6)
# peacock eyespots on the telson
d.shape("ellipse", "Telson spot 1", x=758, y=512, width=28, height=24,
        fill="#1B3A8C", stroke="#9FE8FF", strokeWidth=4)
d.shape("ellipse", "Telson spot 2", x=790, y=545, width=22, height=19,
        fill="#1B3A8C", stroke="#9FE8FF", strokeWidth=3)
# gold rim dots on the fan edge
for i, (x, y) in enumerate([(818,455),(830,505),(830,560),(816,610)]):
    d.shape("ellipse", f"Fan dot {i+1}", x=x, y=y, width=9, height=9,
            fill="#FFD45E", opacity=80, stroke=NONE)
# red edges on the uropods
d.path("M720,470 C760,442 800,426 826,432", "Uropod edge up",
       fill=NONE, stroke="#E8562E", strokeWidth=4, opacity=60, cap="round")
d.path("M726,570 C764,596 800,612 824,612", "Uropod edge low",
       fill=NONE, stroke="#E8562E", strokeWidth=4, opacity=60, cap="round")

# --- abdomen segments (rear to front so each anterior plate overlaps) ----------
def seg(name, x0, x1, t0, t1, h, grad):
    mid = (x0 + x1) / 2
    d.path(f"M{x0},{t0} Q{mid},{min(t0,t1)-18} {x1},{t1} "
           f"L{x1},{t1+h} Q{mid},{max(t0,t1)+h+6} {x0},{t0+h} Z",
           name, fill=grad, stroke=INK, strokeWidth=5)
    # iridescent sheen along the top edge
    d.path(f"M{x0+8},{t0+9} Q{mid},{min(t0,t1)-9} {x1-8},{t1+9}",
           f"{name} sheen", fill=NONE, stroke="#9FF0E2",
           strokeWidth=5, opacity=45, cap="round")
    # translucent shadow band along the belly edge
    d.path(f"M{x0+12},{t0+h-12} Q{mid},{max(t0,t1)+h-4} {x1-12},{t1+h-10}",
           f"{name} belly shade", fill=NONE, stroke="#0A4A40",
           strokeWidth=9, opacity=30, cap="round")

seg("Seg 5", 658, 738, 460, 485, 72, SEG_GRAD_B)
seg("Seg 4", 592, 676, 440, 463, 78, SEG_GRAD_A)
seg("Seg 3", 528, 612, 424, 443, 82, SEG_GRAD_B)
seg("Seg 2", 462, 548, 410, 427, 85, SEG_GRAD_A)
seg("Seg 1", 398, 484, 402, 412, 86, SEG_GRAD_B)

# gold lateral dots on each segment
for i, (x, y) in enumerate([(430,455),(505,472),(575,490),(640,505),(700,522)]):
    d.shape("ellipse", f"Flank dot {i+1}", x=x, y=y, width=10, height=8,
            fill="#FFD45E", opacity=75, stroke=NONE)
# magenta iridescent ticks on segment seams
for i, (x, y) in enumerate([(480,428),(545,442),(610,458),(672,478)]):
    d.path(f"M{x},{y} Q{x+10},{y+22} {x+6},{y+44}", f"Seam glow {i+1}",
           fill=NONE, stroke="#FF7FD4", strokeWidth=3, opacity=35, cap="round")

# --- pleopods (soft swimmerets under the abdomen) -------------------------------
for i, (x, y) in enumerate([(545,512),(615,528),(675,540)]):
    d.path(f"M{x},{y} C{x-8},{y+22} {x-18},{y+38} {x-34},{y+48} "
           f"C{x-16},{y+48} {x+2},{y+34} {x+10},{y+10} Z",
           f"Pleopod {i+1}", fill="#3EC8B0", stroke=INK,
           strokeWidth=3, opacity=70)

# --- walking legs under the cephalothorax ---------------------------------------
for i, (x, y) in enumerate([(440,498),(470,505),(500,512)]):
    d.path(f"M{x},{y} L{x-16},{y+38} L{x-30},{y+54}", f"Walk leg ink {i+1}",
           fill=NONE, stroke=INK, strokeWidth=7, cap="round")
    d.path(f"M{x},{y} L{x-16},{y+38} L{x-30},{y+54}", f"Walk leg {i+1}",
           fill=NONE, stroke="#0C5B4F", strokeWidth=4, cap="round")

# --- carapace -------------------------------------------------------------------
d.path("M248,478 C244,430 276,398 332,392 C390,386 436,404 452,446 "
       "C464,484 456,530 426,556 C392,580 322,580 286,552 "
       "C260,532 248,508 248,478 Z",
       "Carapace", fill=CARAPACE_GRAD, stroke=INK, strokeWidth=6)
# ridge highlight + belly shade
d.path("M280,432 C332,406 402,408 436,448", "Carapace sheen",
       fill=NONE, stroke="#9FF0E2", strokeWidth=6, opacity=40, cap="round")
d.path("M280,540 C330,562 392,562 424,540", "Carapace shade",
       fill=NONE, stroke="#0A4A40", strokeWidth=8, opacity=30, cap="round")
# rostrum: pointed plate on the head front
d.path("M330,398 C302,384 274,376 252,378 C272,392 300,401 334,404 Z",
       "Rostrum", fill=SEG_GRAD_A, stroke=INK, strokeWidth=4)
# iridescent flecks on the shell
for i, (x, y, c) in enumerate([(300,455,"#FF7FD4"),(370,420,"#FFD45E"),(410,470,"#FF7FD4")]):
    d.shape("ellipse", f"Shell fleck {i+1}", x=x, y=y, width=9, height=9,
            fill=c, opacity=60, stroke=NONE)

# --- raptorial claws (the folded punching clubs) --------------------------------
# far-side claw, darker, peeking behind
d.path("M392,542 C368,550 350,572 348,596 C346,618 358,634 378,634 "
       "C400,632 412,612 412,586 C412,564 404,546 392,542 Z",
       "Claw far", fill="#A8361C", stroke=INK, strokeWidth=5, opacity=95)
# near propus: the thick folded forearm
d.path("M368,530 C330,530 295,548 276,578 C262,600 264,628 288,642 "
       "C315,656 352,646 370,618 C384,596 386,556 368,530 Z",
       "Club propus", fill=CLAW_GRAD, stroke=INK, strokeWidth=6)
# dactyl: the swollen hammer folded into the propus
d.path("M292,596 C284,578 292,556 314,546 C338,536 362,544 368,564 "
       "C372,580 362,598 344,604 C324,610 300,608 292,596 Z",
       "Club dactyl", fill=CLAW_GRAD, stroke=INK, strokeWidth=5)
# pointed heel at the fold
d.path("M292,596 C276,594 262,600 252,612 C266,616 282,612 292,602 Z",
       "Club heel", fill="#C23E1E", stroke=INK, strokeWidth=4)
# teeth along the dactyl edge
for i, (x, y) in enumerate([(306,544),(322,540),(338,540)]):
    d.path(f"M{x},{y} L{x+5},{y-11} L{x+11},{y-1} Z",
           f"Club tooth {i+1}", fill=INK, stroke=NONE)
# club sheen
d.path("M292,576 C308,560 338,552 358,560", "Club sheen",
       fill=NONE, stroke="#FFCF9E", strokeWidth=5, opacity=55, cap="round")

# --- stalked eyes (banded stalks, compound eyes) --------------------------------
# far stalk + eye (left, slightly smaller)
d.path("M290,414 C282,378 272,346 262,322 L284,312 C296,342 306,378 314,412 Z",
       "Stalk far", fill="#D85E3A", stroke=INK, strokeWidth=4)
d.path("M270,352 Q282,344 296,350", "Stalk far band g",
       fill=NONE, stroke="#3FA85E", strokeWidth=5, cap="round")
d.shape("ellipse", "Eye far", x=238, y=270, width=64, height=48,
        fill=EYE_GRAD, stroke=INK, strokeWidth=5)
d.path("M240,294 Q270,287 300,293", "Eye far band",
       fill=NONE, stroke="#0E3A33", strokeWidth=6, cap="round")
d.shape("ellipse", "Eye far glint", x=252, y=278, width=10, height=10,
        fill="#FFFFFF", opacity=80, stroke=NONE)

# near stalk + eye (right, larger)
d.path("M352,404 C358,358 368,326 380,300 L404,306 C396,338 392,372 392,404 Z",
       "Stalk near", fill="#D85E3A", stroke=INK, strokeWidth=5)
d.path("M366,362 Q384,352 398,358", "Stalk near band g",
       fill=NONE, stroke="#3FA85E", strokeWidth=6, cap="round")
d.path("M372,338 Q388,330 402,336", "Stalk near band r",
       fill=NONE, stroke="#8FE0FF", strokeWidth=5, cap="round")
d.shape("ellipse", "Eye near", x=368, y=258, width=78, height=56,
        fill=EYE_GRAD, stroke=INK, strokeWidth=5)
d.path("M370,286 Q407,278 444,285", "Eye near band",
       fill=NONE, stroke="#0E3A33", strokeWidth=7, cap="round")
d.shape("ellipse", "Eye near glint", x=382, y=266, width=12, height=12,
        fill="#FFFFFF", opacity=85, stroke=NONE)
# magenta glint accent on the near eye
d.shape("ellipse", "Eye magenta accent", x=420, y=290, width=14, height=10,
        fill="#FF7FD4", opacity=45, stroke=NONE)

# --- antennae sweeping forward ---------------------------------------------------
d.path("M258,450 C205,428 148,410 92,412", "Antenna 1",
       fill=NONE, stroke="#D85E3A", strokeWidth=5, cap="round")
d.path("M256,468 C200,460 144,466 96,486", "Antenna 2",
       fill=NONE, stroke="#E8A04A", strokeWidth=4, cap="round")
d.path("M256,486 C214,492 174,506 144,526", "Antenna 3",
       fill=NONE, stroke="#D85E3A", strokeWidth=4, cap="round")

# --- name -------------------------------------------------------------------------
d.text("MANTIS SHRIMP", "Name", x=500, y=958, size=52, font="Virelai Sans",
       color="#D2ECE4", justify="center")

d.finish("mantis-shrimp-V1R00")
