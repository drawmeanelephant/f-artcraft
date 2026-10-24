#!/usr/bin/env python3
"""rc-status.sh — The Pulse-Taker. Necropolis plate V1R00.
A physician of the old school with a stethoscope pressed to the crypt floor,
listening — environment, health, pulse — while a nurse writes the structured
status report in triplicate. The necropolis is alive; here is the paperwork
to prove it. 1000x1000. Gradients + translucent shading."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("RC-Status — Necropolis Plate", 1000, 1000)

INK = "#14201E"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#0C1616"}, {"offset": 1, "color": "#050A0A"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#3A5050"}, {"offset": 0.7, "color": "#1C2828"},
    {"offset": 1, "color": "#0C1212"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#28362F"}, {"offset": 1, "color": "#0E1412"}]}}
COAT = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#39404E"}, {"offset": 1, "color": "#181C26"}]}}
COAT_DK = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2A303C"}, {"offset": 1, "color": "#12141C"}]}}
UNIFORM = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#BCCBC2"}, {"offset": 1, "color": "#7C8E84"}]}}
APRON = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E4ECE4"}, {"offset": 1, "color": "#A8B8AC"}]}}
CAP = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F0F4EE"}, {"offset": 1, "color": "#C4CFC4"}]}}
SKIN = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#C9A87E"}, {"offset": 1, "color": "#8E6B48"}]}}
BAG = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5A4230"}, {"offset": 1, "color": "#2A1C10"}]}}
BRASS = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E0BC6A"}, {"offset": 1, "color": "#96742E"}]}}
PARCH = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#EAE2CC"}, {"offset": 1, "color": "#BDB08C"}]}}
BOARD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6E5C42"}, {"offset": 1, "color": "#3A2C1C"}]}}
PULSE = "#7AE0A8"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#54706E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#BCD0CC", strokeWidth=3, opacity=45)
for i, (x, y, w) in enumerate([(193,233,8),(801,230,7),(157,524,9),(837,544,8),
                               (247,766,7),(753,749,9),(133,393,6),(864,391,7),
                               (391,113,7),(613,110,8),(333,823,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#48605E", opacity=35, stroke=NONE)

# --- crypt wall: seam, damp streaks, a small vent grate --------------------------
d.path("M150,330 C350,322 650,322 850,330", "Wall seam", fill=NONE,
       stroke="#081010", strokeWidth=4, opacity=40)
for i, (x, ln) in enumerate([(300,60),(470,84),(640,54),(770,70)]):
    d.path(f"M{x},{332} C{x+3},{332+ln*0.5} {x-2},{332+ln*0.8} {x+1},{332+ln}",
           f"Damp streak {i+1}", fill=NONE, stroke="#0A1616", strokeWidth=5,
           opacity=35, cap="round")
# little arched vent grate, high right — the environment on record
d.path("M742,258 L742,222 C742,200 760,188 782,188 C804,188 822,200 822,222 "
       "L822,258 Z", "Vent", fill="#08100F", stroke="#2E4240", strokeWidth=4,
       join="round")
for i, vx in enumerate([756, 770, 784, 798, 810]):
    d.path(f"M{vx},206 L{vx},250", f"Vent bar {i+1}", fill=NONE,
           stroke="#2E4240", strokeWidth=3, opacity=80)

# --- the physician's bag, set down behind him ------------------------------------
d.path("M236,664 L236,626 C236,606 252,596 274,596 C296,596 312,606 312,626 "
       "L312,664 Z", "Bag body", fill=BAG, stroke=INK, strokeWidth=4,
       join="round")
d.path("M254,598 C254,584 294,584 294,598", "Bag handle", fill=NONE,
       stroke="#3A2A1C", strokeWidth=5, cap="round")
d.shape("rectangle", "Bag clasp", x=267, y=620, width=14, height=12,
        fill=BRASS, stroke=INK, strokeWidth=2, radius=2)
d.path("M240,642 L308,642", "Bag seam", fill=NONE, stroke="#1E140C",
       strokeWidth=3, opacity=60)

# --- floor ----------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#060C0A",
       strokeWidth=4, opacity=70)
d.shape("ellipse", "Physician shadow", x=330, y=688, width=240, height=16,
        fill="#030806", opacity=55, stroke=NONE)
d.shape("ellipse", "Nurse shadow", x=662, y=688, width=160, height=14,
        fill="#030806", opacity=55, stroke=NONE)
# a crack in the slab the chest piece listens over
d.path("M520,700 L548,720 L534,742 L560,770", "Floor crack", fill=NONE,
       stroke="#060C0A", strokeWidth=3, opacity=70)

# --- the pulse: rings on the floor + a heartbeat trace running right ---------------
for i, (rx, ry, op) in enumerate([(46, 12, 65), (80, 20, 40), (116, 28, 20)]):
    d.path(f"M{560-rx},{694} C{560-rx},{694-ry*2} {560+rx},{694-ry*2} "
           f"{560+rx},{694}", f"Pulse ring {i+1}", fill=NONE,
           stroke=PULSE, strokeWidth=3, opacity=op)
# heartbeat trace: glow underlay + the trace itself
d.path("M600,690 L660,690 L672,668 L684,706 L696,690 L744,690 L754,676 "
       "L764,700 L776,690 L836,690", "Pulse trace glow", fill=NONE,
       stroke=PULSE, strokeWidth=9, opacity=14, cap="round", join="round")
d.path("M600,690 L660,690 L672,668 L684,706 L696,690 L744,690 L754,676 "
       "L764,700 L776,690 L836,690", "Pulse trace", fill=NONE,
       stroke=PULSE, strokeWidth=3, opacity=65, cap="round", join="round")

# --- the physician, kneeling, ear to the ground via the chest piece ---------------
# rear shin folded flat on the slab, boot toe poking out behind
d.path("M278,680 L312,680 L312,694 L276,694 Z", "Rear boot", fill="#10100E",
       stroke=INK, strokeWidth=3, join="round")
d.path("M294,694 C292,674 308,662 332,660 L412,658 C428,658 436,672 434,694 Z",
       "Rear shin", fill=COAT_DK, stroke=INK, strokeWidth=4, join="round")
# coat skirt pooling over the folded leg
d.path("M336,694 C330,656 336,620 356,592 L398,596 C390,628 388,662 390,694 Z",
       "Coat skirt", fill=COAT_DK, stroke=INK, strokeWidth=3, join="round")
# torso: back high and rounded, chest pitched forward toward the floor
d.path("M348,694 C342,628 354,556 386,502 C402,476 428,462 454,464 "
       "C480,466 494,484 498,512 C504,558 510,626 514,694 L438,694 "
       "C436,662 426,646 404,644 C384,642 370,658 366,694 Z",
       "Coat", fill=COAT, stroke=INK, strokeWidth=5, join="round")
# a fold down the back
d.path("M370,560 C376,610 374,656 368,688", "Coat fold", fill=NONE,
       stroke="#10141C", strokeWidth=3, opacity=55)
# the raised front knee the arm is laid over
d.path("M436,694 C430,654 438,616 462,600 C486,584 518,592 532,618 "
       "C544,640 548,668 548,694 Z", "Front knee", fill=COAT, stroke=INK,
       strokeWidth=4, join="round")
# head, tipped down toward the chest piece
d.shape("ellipse", "Head", x=428, y=424, width=46, height=48,
        fill=SKIN, stroke=INK, strokeWidth=4)
# hair + sideburn shadow
d.path("M430,442 C426,420 442,404 462,406 C478,408 486,422 484,438 "
       "C472,428 448,426 438,436 Z", "Hair", fill="#3A3230", stroke=INK,
       strokeWidth=3, join="round")
d.shape("ellipse", "Eye", x=458, y=452, width=6, height=6,
        fill="#241812", stroke=NONE)
# the old-school forehead mirror: brow band + reflector disc
d.path("M428,428 C440,420 462,418 478,424", "Mirror band", fill=NONE,
       stroke="#26201C", strokeWidth=5, cap="round")
d.shape("ellipse", "Mirror", x=462, y=408, width=20, height=20,
        fill=BRASS, stroke=INK, strokeWidth=3)
d.shape("ellipse", "Mirror hole", x=469, y=415, width=6, height=6,
        fill="#241812", stroke=NONE)
# arm reaching down over the knee, chest piece pressed to the slab
d.path("M448,512 C482,542 522,606 552,662", "Sleeve", fill=NONE,
       stroke="#2E3442", strokeWidth=13, cap="round")
d.shape("ellipse", "Hand", x=542, y=658, width=20, height=16,
        fill=SKIN, stroke=INK, strokeWidth=3)
# stethoscope: earpieces at the ear, tube down the arm to the chest piece
d.path("M444,468 C452,500 470,540 505,586 C525,612 545,646 556,672",
       "Scope tube", fill=NONE, stroke="#0E1A18", strokeWidth=5, cap="round")
d.shape("ellipse", "Chest piece", x=548, y=668, width=20, height=12,
        fill=BRASS, stroke=INK, strokeWidth=3)
d.shape("ellipse", "Chest piece rim", x=552, y=672, width=12, height=6,
        fill="#F0D894", opacity=70, stroke=NONE)

# --- the nurse, writing the report in triplicate ----------------------------------
# shoes
d.path("M692,686 L718,686 L718,696 L692,696 Z", "Shoe L", fill="#141A16",
       stroke=INK, strokeWidth=3, join="round")
d.path("M742,686 L768,686 L768,696 L742,696 Z", "Shoe R", fill="#141A16",
       stroke=INK, strokeWidth=3, join="round")
# uniform dress
d.path("M684,692 L694,540 C697,494 708,462 730,456 C752,462 764,494 768,540 "
       "L778,692 Z", "Dress", fill=UNIFORM, stroke=INK, strokeWidth=5,
       join="round")
# apron front
d.path("M708,548 L756,548 L762,690 L702,690 Z", "Apron", fill=APRON,
       opacity=75, stroke="#5E6E64", strokeWidth=2, join="round")
# collar + cuff hints
d.path("M716,470 L730,486 L744,470", "Collar", fill=NONE, stroke="#E4ECE4",
       strokeWidth=4, join="round")
# head + nurse cap
d.shape("ellipse", "Nurse head", x=712, y=396, width=38, height=42,
        fill=SKIN, stroke=INK, strokeWidth=4)
d.path("M712,412 C710,394 722,382 734,382 C748,382 756,394 754,412 "
       "C746,402 722,402 712,412 Z", "Nurse hair", fill="#4A3A30", stroke=INK,
       strokeWidth=3, join="round")
d.path("M716,392 C718,376 750,376 752,392 L752,400 C744,392 724,392 716,400 Z",
       "Nurse cap", fill=CAP, stroke=INK, strokeWidth=3, join="round")
d.shape("ellipse", "Nurse eye", x=718, y=418, width=5, height=5,
        fill="#241812", stroke=NONE)
# the board with its triplicate, held up in front — smaller than her torso,
# so her shoulders and the writing hand still read
d.path("M630,478 L710,464 L730,560 L650,574 Z", "Board", fill=BOARD,
       stroke=INK, strokeWidth=4, join="round")
d.path("M634,474 L702,462 L706,471 L638,483 Z", "Board clip", fill=BRASS,
       stroke=INK, strokeWidth=2, join="round")
for i, (ox, oy) in enumerate([(9, 5), (4, 2)]):
    d.path(f"M{634+ox},{482+oy} L{704+ox},{470+oy} L{722+ox},{552+oy} "
           f"L{652+ox},{564+oy} Z", f"Copy {3-i}", fill=PARCH, stroke=INK,
           strokeWidth=2, opacity=95, join="round")
d.path("M632,482 L702,470 L720,552 L650,564 Z", "Top copy", fill=PARCH,
       stroke=INK, strokeWidth=2, join="round")
# the structured report: headed rows, boxes ticked
d.path("M646,492 L688,486", "Report head", fill=NONE, stroke="#6A5B40",
       strokeWidth=4, opacity=85)
for i, ty in enumerate([504, 516, 528, 540, 550]):
    d.path(f"M{644},{ty} L{706},{ty-11}", f"Report line {i+1}", fill=NONE,
           stroke="#8A7A58", strokeWidth=2, opacity=80)
for i, (bx, by) in enumerate([(710, 498), (715, 516), (720, 534)]):
    d.shape("rectangle", f"Tick box {i+1}", x=bx, y=by, width=8, height=8,
            fill=NONE, stroke="#6A5B40", strokeWidth=2)
d.path("M711,500 L713,503 L717,496", "Tick 1", fill=NONE, stroke="#3E5E44",
       strokeWidth=2, cap="round")
# left hand gripping the board's lower corner — the arm is lost behind it,
# which is what holding a board looks like
d.shape("ellipse", "Hand L", x=642, y=556, width=16, height=14,
        fill=SKIN, stroke=INK, strokeWidth=3)
# right arm in from the shoulder, writing on the top copy
d.path("M754,494 C742,512 726,526 706,538", "Arm R", fill=NONE,
       stroke="#9AAEA2", strokeWidth=11, cap="round")
d.shape("ellipse", "Hand R", x=694, y=530, width=16, height=14,
        fill=SKIN, stroke=INK, strokeWidth=3)
# pencil mid-stroke
d.path("M700,534 L710,550", "Pencil", fill=NONE, stroke="#C8964A",
       strokeWidth=4, cap="round")
d.path("M708,548 L714,555", "Pencil tip", fill=NONE, stroke="#3A2C1C",
       strokeWidth=3, cap="round")

# --- captions ------------------------------------------------------------------
d.text("RC-STATUS", "Name", x=500, y=930, size=58, font="Virelai Sans",
       color="#D8E4E0", justify="center")
r = d.text("PULSE OF THE GROUND", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#94ACA4", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("rk-status-V1R00")
