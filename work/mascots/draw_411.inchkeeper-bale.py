#!/usr/bin/env python3
"""Inchkeeper Bale — mascot portrait V1R00.
Gatekeeper at a gate, balance scale and measuring tape beside, three ledger
volumes of denied entries stacked nearby.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Inchkeeper Bale — Mascot Portrait", 1000, 1000)

INK = "#2E2A38"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#161A28"}, {"offset": 1, "color": "#07080F"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#8B9AC0"}, {"offset": 0.7, "color": "#5D6B93"},
    {"offset": 1, "color": "#333B58"}]}}
GATE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6B7690"}, {"offset": 1, "color": "#424A62"}]}}
BODY = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F0CD94"}, {"offset": 0.72, "color": "#D2A468"},
    {"offset": 1, "color": "#A87944"}]}}
BRASS = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E4C36A"}, {"offset": 1, "color": "#9A7430"}]}}
LEDGER = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#8A4A44"}, {"offset": 1, "color": "#5C2E2C"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#7C8CB2", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#DCE4F4", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(200,225,8),(795,238,7),(168,538,9),(822,558,8),
                               (252,752,7),(742,742,9),(142,398,6),(855,408,7),
                               (398,116,7),(602,114,8),(338,812,6),(660,810,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#4A5578", opacity=45, stroke=NONE)

# --- the gate (behind the mascot) ---------------------------------------------
d.shape("rectangle", "Gate dark", x=352, y=330, width=296, height=390,
        fill="#171D2C", stroke=NONE)
for i, x in enumerate([386, 432, 478, 524, 570, 616]):
    d.shape("rectangle", f"Bar {i+1}", x=x, y=336, width=13, height=384,
            fill=GATE, stroke=INK, strokeWidth=3, radius=4)
# posts + lintel
d.shape("rectangle", "Post L", x=340, y=320, width=30, height=410,
        fill=GATE, stroke=INK, strokeWidth=5, radius=6)
d.shape("rectangle", "Post R", x=630, y=320, width=30, height=410,
        fill=GATE, stroke=INK, strokeWidth=5, radius=6)
d.path("M335,330 C335,265 415,235 500,235 C585,235 665,265 665,330 "
       "L640,330 C640,285 575,262 500,262 C425,262 360,285 360,330 Z",
       "Gate arch", fill=GATE, stroke=INK, strokeWidth=5, join="round")
# post finials
d.shape("ellipse", "Finial L", x=342, y=296, width=26, height=26, fill=BRASS,
        stroke=INK, strokeWidth=4)
d.shape("ellipse", "Finial R", x=632, y=296, width=26, height=26, fill=BRASS,
        stroke=INK, strokeWidth=4)
# ground shadow under the scene
d.shape("ellipse", "Ground shadow", x=210, y=716, width=580, height=54,
        fill="#22283E", opacity=55, stroke=NONE)

# --- balance scale on its plinth, left ----------------------------------------
d.shape("rectangle", "Scale plinth", x=232, y=700, width=120, height=22,
        fill=GATE, stroke=INK, strokeWidth=4, radius=4)
d.path("M292,700 L292,560", "Scale column", fill=NONE, stroke=BRASS,
       strokeWidth=10, cap="round")
# beam tilted: denied (left) pan hangs lower
d.path("M236,590 L348,545", "Scale beam", fill=NONE, stroke=BRASS,
       strokeWidth=8, cap="round")
d.shape("ellipse", "Beam pivot", x=283, y=558, width=18, height=18,
        fill=BRASS, stroke=INK, strokeWidth=4)
# pan chains + pans
d.path("M240,590 L222,640 M240,590 L258,640", "Chains L", fill=NONE,
       stroke=INK, strokeWidth=3)
d.path("M348,545 L336,600 M348,545 L360,600", "Chains R", fill=NONE,
       stroke=INK, strokeWidth=3)
d.path("M210,640 C216,662 264,662 270,640 C258,648 222,648 210,640 Z",
       "Pan L", fill=BRASS, stroke=INK, strokeWidth=4)
d.path("M326,600 C332,622 364,622 370,600 C360,608 336,608 326,600 Z",
       "Pan R", fill=BRASS, stroke=INK, strokeWidth=4)
# a denied slip lying on the low pan
d.path("M224,634 L252,628 L256,640 L228,646 Z", "Denied slip",
       fill="#E8DCC2", stroke=INK, strokeWidth=2)

# --- three ledger volumes of denied entries, right ----------------------------
for i, (y, w) in enumerate([(748,150),(712,138),(678,124)]):
    x0 = 660 - w/2
    d.shape("rectangle", f"Ledger {i+1}", x=x0, y=y, width=w, height=34,
            fill=LEDGER, stroke=INK, strokeWidth=5, radius=5)
    d.shape("rectangle", f"Ledger pages {i+1}", x=x0+8, y=y+7, width=w-16,
            height=8, fill="#E8DCC2", stroke=NONE, opacity=85)
d.text("DENIED", "Denied stamp", x=660, y=772, size=16, font="Virelai Sans",
       color="#D4584A", justify="center")
# the stamp frame on the bottom ledger's face
d.shape("rectangle", "Denied frame", x=612, y=754, width=96, height=24,
        fill=NONE, stroke="#D4584A", strokeWidth=3, opacity=85, radius=4)

# --- mascot: the inchkeeper ----------------------------------------------------
d.path("M500,452 C562,452 606,500 610,580 C613,660 585,742 500,742 "
       "C415,742 387,660 390,580 C394,500 438,452 500,452 Z",
       "Body", fill=BODY, stroke=INK, strokeWidth=7)
d.shape("ellipse", "Body highlight", x=428, y=470, width=110, height=46,
        fill="#FFFFFF", opacity=22, stroke=NONE)
# keeper's flat cap
d.path("M430,452 C440,410 480,392 516,398 C548,404 566,428 566,452 Z",
       "Cap", fill="#4A5578", stroke=INK, strokeWidth=6, join="round")
d.shape("ellipse", "Cap badge", x=486, y=414, width=20, height=20,
        fill=BRASS, stroke=INK, strokeWidth=3)
# ruler sash across the chest
d.path("M432,560 L578,610 L566,646 L420,596 Z", "Sash", fill="#E8DCC2",
       stroke=INK, strokeWidth=5, join="round")
for i in range(9):
    t = i / 8
    x1 = 432 + (578-432)*t + 4
    y1 = 560 + (610-560)*t + 6
    x2 = 432 + (566-420)*t + 4
    y2 = 560 + (646-560)*t + 6
    mx, my = x1 + (x2-x1)*0.45, y1 + (y2-y1)*0.45
    ln = 7 if i % 2 else 11
    d.path(f"M{x1:.0f},{y1:.0f} L{x1 + (x2-x1)*ln/22:.0f},{y1 + (y2-y1)*ln/22:.0f}",
           f"Sash tick {i+1}", fill=NONE, stroke=INK, strokeWidth=3)
# face: level stare, flat mouth — nothing gets past
d.shape("ellipse", "Eye L", x=448, y=500, width=26, height=30, fill="#FBF6E8",
        stroke=INK, strokeWidth=5)
d.shape("ellipse", "Eye R", x=526, y=500, width=26, height=30, fill="#FBF6E8",
        stroke=INK, strokeWidth=5)
d.shape("ellipse", "Pupil L", x=456, y=508, width=11, height=13, fill=INK, stroke=NONE)
d.shape("ellipse", "Pupil R", x=534, y=508, width=11, height=13, fill=INK, stroke=NONE)
d.path("M444,484 L486,480", "Brow L", fill=NONE, stroke=INK, strokeWidth=5, cap="round")
d.path("M514,480 L556,484", "Brow R", fill=NONE, stroke=INK, strokeWidth=5, cap="round")
d.path("M472,566 L530,566", "Flat mouth", fill=NONE, stroke=INK,
       strokeWidth=6, cap="round")
# arms: left palm up in "halt", right holds the tape roll
d.path("M408,600 C385,608 362,610 342,608", "Arm L", fill=NONE, stroke=BODY,
       strokeWidth=22, cap="round")
d.shape("ellipse", "Palm halt", x=306, y=590, width=30, height=36, fill=BODY,
        stroke=INK, strokeWidth=5)
for i, x in enumerate([312, 321, 330]):
    d.path(f"M{x},592 L{x-2},576", f"Halt finger {i+1}",
           fill=NONE, stroke=INK, strokeWidth=3, cap="round")
d.path("M592,590 C620,600 636,618 644,638", "Arm R", fill=NONE, stroke=BODY,
       strokeWidth=22, cap="round")
# measuring tape: roll in right hand, tape drooping to a curled end
d.shape("ellipse", "Tape roll", x=630, y=628, width=52, height=52, fill="#E8C85E",
        stroke=INK, strokeWidth=6)
d.shape("ellipse", "Roll hub", x=648, y=646, width=16, height=16, fill="#8A7434",
        stroke=INK, strokeWidth=3)
d.path("M642,676 C620,700 624,726 648,734 C668,740 684,730 680,714",
       "Tape tail", fill=NONE, stroke="#E8C85E", strokeWidth=12, cap="round")
d.path("M642,676 C620,700 624,726 648,734", "Tape edge", fill=NONE,
       stroke=INK, strokeWidth=3, cap="round", opacity=70)

# --- captions ------------------------------------------------------------------
d.text("INCHKEEPER BALE", "Name", x=500, y=930, size=56, font="Virelai Sans",
       color="#DCE4F4", justify="center")
r = d.text("GATEKEEPER OF SMALL DENIALS", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#9AA8CC", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("411.inchkeeper-bale-V1R00")
