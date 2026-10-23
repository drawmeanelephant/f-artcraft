#!/usr/bin/env python3
"""Keyholder Null — mascot portrait V1R00. HTTP 423, "Locked".
Custodian beside a latched door, the presented key unaccepted. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Keyholder Null — Mascot Portrait", 1000, 1000)

INK = "#33281F"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1E241F"}, {"offset": 1, "color": "#0C100C"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E7E1D0"}, {"offset": 0.7, "color": "#B8AE95"},
    {"offset": 1, "color": "#7C7359"}]}}
DOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#9A6B3C"}, {"offset": 0.6, "color": "#7A4E2A"},
    {"offset": 1, "color": "#58351C"}]}}
COAT_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#46586C"}, {"offset": 0.7, "color": "#32404F"},
    {"offset": 1, "color": "#222C38"}]}}
BRASS_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#EFCB6E"}, {"offset": 1, "color": "#A87F2E"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#6B6249", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F0EAD8", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(210,220,7),(780,210,6),(240,715,7),(755,705,7),(170,450,6),
                               (835,455,6),(350,150,6),(650,145,7),(300,795,6),(700,790,6)]):
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#6B6249", opacity=40, stroke=NONE)

# --- the latched door -------------------------------------------------------------
d.shape("ellipse", "Door shadow", x=560, y=740, width=240, height=26,
        fill="#3A3222", opacity=40, stroke=NONE)
d.shape("rectangle", "Door frame", x=576, y=288, width=208, height=452,
        radius=10, fill="#4A3A28", stroke=INK, strokeWidth=6)
d.shape("rectangle", "Door", x=596, y=308, width=168, height=432,
        radius=6, fill=DOOR_GRAD, stroke=INK, strokeWidth=4)
# planks
for i, x in enumerate([638, 680, 722]):
    d.path(f"M{x},312 L{x},736", f"Plank {i+1}", fill=NONE,
           stroke="#4E3018", strokeWidth=3, opacity=70)
# wood knots
d.shape("ellipse", "Knot 1", x=610, y=360, width=12, height=18, fill="#58351C", opacity=60, stroke=NONE)
d.shape("ellipse", "Knot 2", x=732, y=590, width=10, height=16, fill="#58351C", opacity=60, stroke=NONE)
# heavy latch bar across the door
d.shape("rectangle", "Latch bar", x=560, y=470, width=240, height=34,
        radius=8, fill="#3E3A34", stroke=INK, strokeWidth=5)
d.shape("rectangle", "Latch bracket L", x=568, y=458, width=26, height=58,
        radius=5, fill="#2E2A26", stroke=INK, strokeWidth=4)
d.shape("rectangle", "Latch bracket R", x=766, y=458, width=26, height=58,
        radius=5, fill="#2E2A26", stroke=INK, strokeWidth=4)
# keyhole escutcheon on the bar
d.shape("ellipse", "Escutcheon", x=594, y=462, width=52, height=52,
        fill=BRASS_GRAD, stroke=INK, strokeWidth=4)
d.path("M614,482 C614,476 626,476 626,482 C626,486 624,488 622,489 L624,502 L616,502 L618,489 C616,488 614,486 614,482 Z",
       "Keyhole", fill="#1E1A14", stroke=NONE)
# rejection: cold glow + denial marks between offered key and keyhole
d.shape("ellipse", "Keyhole glare", x=584, y=452, width=72, height=72,
        fill="#D94A3A", opacity=22, stroke=NONE)
d.path("M580,470 L566,458 M580,500 L564,506 M586,486 L570,486", "Denial ticks",
       fill=NONE, stroke="#D94A3A", strokeWidth=5, cap="round", opacity=85)

# --- the custodian ------------------------------------------------------------------
d.shape("ellipse", "Figure shadow", x=280, y=748, width=270, height=28,
        fill="#3A3222", opacity=40, stroke=NONE)
# coat body
d.path("M330,744 C324,660 330,560 356,500 C380,446 424,424 460,430 "
       "C502,438 530,490 536,560 C542,640 540,700 538,744 Z",
       "Coat", fill=COAT_GRAD, stroke=INK, strokeWidth=7, join="round")
d.path("M368,720 C366,640 376,555 402,495", "Coat fold",
       fill=NONE, stroke="#1A222C", strokeWidth=8, opacity=45, cap="round")
# belt + keyring of spare keys
d.path("M336,636 L534,626", "Belt", fill=NONE, stroke="#241E16", strokeWidth=14)
d.shape("ellipse", "Belt buckle", x=420, y=622, width=30, height=22,
        fill=BRASS_GRAD, stroke=INK, strokeWidth=3)
d.shape("ellipse", "Keyring", x=462, y=630, width=22, height=22,
        fill=NONE, stroke="#C9B98A", strokeWidth=4)
for i, (x1, y1, x2, y2) in enumerate([(466,650,458,688),(474,651,478,692),(482,650,494,686)]):
    d.path(f"M{x1},{y1} L{x2},{y2} M{x2-5},{y2-2} L{x2+3},{y2+3}",
           f"Ring key {i+1}", fill=NONE, stroke="#C9B98A", strokeWidth=4, cap="round")
# head + custodian cap
d.shape("ellipse", "Head", x=398, y=356, width=128, height=118,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#F2DFC8"}, {"offset": 1, "color": "#D4B394"}]}},
        stroke=INK, strokeWidth=6)
d.path("M390,386 C396,340 430,316 466,318 C500,320 524,344 528,384 "
       "C500,370 420,370 390,386 Z", "Cap", fill="#2E3844", stroke=INK, strokeWidth=5, join="round")
d.path("M384,388 C420,374 508,374 534,390", "Cap brim",
       fill=NONE, stroke=INK, strokeWidth=6, cap="round")
# face: resigned, looking at the door
d.shape("ellipse", "Eye L", x=434, y=408, width=20, height=24, fill="#33222A", stroke=NONE)
d.shape("ellipse", "Eye R", x=486, y=408, width=20, height=24, fill="#33222A", stroke=NONE)
d.shape("ellipse", "Glint L", x=439, y=413, width=6, height=6, fill="#FFFFFF", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=491, y=413, width=6, height=6, fill="#FFFFFF", opacity=90, stroke=NONE)
d.path("M428,394 C436,389 446,388 452,392", "Brow L",
       fill=NONE, stroke=INK, strokeWidth=4, cap="round", opacity=75)
d.path("M482,392 C490,387 500,386 506,390", "Brow R",
       fill=NONE, stroke=INK, strokeWidth=4, cap="round", opacity=75)
d.path("M450,452 C460,458 476,458 484,452", "Mouth",
       fill=NONE, stroke=INK, strokeWidth=5, cap="round")
# arm extended, offering the key
d.path("M512,500 C544,496 566,492 584,488", "Arm",
       fill=NONE, stroke="#32404F", strokeWidth=26, cap="round")
d.path("M512,500 C544,496 566,492 584,488", "Arm seam",
       fill=NONE, stroke=INK, strokeWidth=4, cap="round", opacity=60)
# the big iron key, held short of the keyhole
d.shape("ellipse", "Key bow", x=548, y=470, width=26, height=30,
        fill=NONE, stroke="#C9B98A", strokeWidth=6)
d.path("M560,486 L592,484", "Key shaft", fill=NONE, stroke="#C9B98A", strokeWidth=7, cap="round")
d.path("M586,484 L586,496 M578,484 L578,494", "Key teeth",
       fill=NONE, stroke="#C9B98A", strokeWidth=5, cap="round")
# hand
d.shape("ellipse", "Hand", x=536, y=478, width=30, height=26,
        fill="#E8CBA8", stroke=INK, strokeWidth=4)

# --- name + role ---------------------------------------------------------------------
d.text("KEYHOLDER NULL", "Name", x=500, y=930, size=58, font="Virelai Sans",
       color="#EDE7D6", justify="center")
d.text(" ".join("LOCKED"), "Role", x=500, y=968, size=23, font="Virelai Sans",
       color="#B3A888", justify="center")

d.finish("423.keyholder-null-V1R00")
