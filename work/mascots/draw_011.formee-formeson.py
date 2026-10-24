#!/usr/bin/env python3
"""Formee Formeson — mascot portrait V1R00.
Identity Duplication Officer stamping a credential form; two identical
user records hang on file behind. Detached procedural confidence.
1000x1000. Gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Formee Formeson — Mascot Portrait", 1000, 1000)

INK = "#33262A"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1B2622"}, {"offset": 1, "color": "#0A100E"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#7E7A5E"}, {"offset": 0.7, "color": "#4E4A38"},
    {"offset": 1, "color": "#2A281E"}]}}
UNIFORM = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3A4660"}, {"offset": 1, "color": "#1E2738"}]}}
UNIFORM_DK = "#161D2C"
FACE = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#EFE2C6"}, {"offset": 1, "color": "#CDB78F"}]}}
CARD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#EADFB9"}, {"offset": 1, "color": "#C9BC90"}]}}
DESK = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6E5638"}, {"offset": 1, "color": "#46331E"}]}}
STAMP_RED = "#A8372C"
BRASS = "#C9A45C"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#6E6A50", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8D2B2", strokeWidth=3, opacity=45)
for i, (x, y, w) in enumerate([(193,232,8),(800,234,7),(158,522,9),(835,542,8),
                               (245,768,7),(755,746,9),(132,392,6),(862,394,7),
                               (390,110,7),(614,112,8),(332,824,6),(666,818,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#3E3A2C", opacity=45, stroke=NONE)

# faint carbon-copy offset frames: the whole wall is a duplicate of itself
for i, off in enumerate([14, 8]):
    d.shape("rectangle", f"Carbon frame {i+1}", x=196+off, y=150+off,
            width=608, height=470, fill=NONE, stroke="#8A8462",
            strokeWidth=3, opacity=18)

# --- two identical user records on file ---------------------------------------
def record(cx, label):
    # manila card, portrait silhouette, three form lines — identical by design
    d.path(rot_rect_path(cx, 265, 150, 196, 0), f"{label} card",
           fill=CARD, stroke=INK, strokeWidth=5)
    d.path(rot_rect_path(cx, 265, 150, 196, 0), f"{label} carbon",
           fill="#8A8262", stroke=NONE, opacity=18)
    # pin dot
    d.shape("ellipse", f"{label} pin", x=cx-5, y=176, width=10, height=10,
            fill=STAMP_RED, stroke=INK, strokeWidth=2)
    # header line + photo box
    d.shape("rectangle", f"{label} header", x=cx-58, y=196, width=116,
            height=12, fill="#9A8F6C", opacity=70, stroke=NONE)
    d.shape("rectangle", f"{label} photo", x=cx-58, y=216, width=52,
            height=62, fill="#B9AC84", stroke=INK, strokeWidth=3)
    # silhouette inside the photo box: same head, same shoulders
    d.path(f"M{cx-32},252 C{cx-48},252 {cx-52},262 {cx-52},278 "
           f"L{cx-6},278 L{cx-6},262 C{cx-6},262 {cx-16},252 {cx-32},252 Z",
           f"{label} photo shoulders", fill="#5A5140", stroke=NONE)
    d.shape("ellipse", f"{label} photo head", x=cx-44, y=224, width=24,
            height=26, fill="#5A5140", stroke=NONE)
    # three identical form lines
    for j, y in enumerate([222, 240, 258]):
        d.shape("rectangle", f"{label} line {j+1}", x=cx+4, y=y,
                width=54 if j < 2 else 38, height=7, fill="#7A7050",
                opacity=80, stroke=NONE)
    # stamp box at the foot of the card — already stamped
    d.shape("rectangle", f"{label} stampbox", x=cx-58, y=292, width=116,
            height=52, fill=NONE, stroke="#9A8F6C", strokeWidth=3)
    d.shape("ellipse", f"{label} stampmark", x=cx-38, y=300, width=76,
            height=36, fill=NONE, stroke=STAMP_RED, strokeWidth=4,
            opacity=75)

record(300, "Record L")
record(700, "Record R")

# --- desk ----------------------------------------------------------------------
# counter across the lower disc; bottom corners stay inside the rim
d.shape("ellipse", "Ground shadow", x=220, y=720, width=560, height=80,
        fill="#141810", opacity=70, stroke=NONE)
d.path("M170,690 L830,690 L752,784 L248,784 Z", "Desk front",
       fill=DESK, stroke=INK, strokeWidth=6, join="round")
d.path("M170,690 L830,690 L824,712 L176,712 Z", "Desk edge",
       fill="#86683F", stroke=INK, strokeWidth=4)
# wood grain strokes on the counter front
for i, y in enumerate([728, 752, 772]):
    d.path(f"M240,{y} C380,{y+8} 620,{y-8} 740,{y}", f"Grain {i+1}",
           fill=NONE, stroke="#3A2C18", strokeWidth=3, opacity=45)

# --- formee: the officer -------------------------------------------------------
# torso in uniform, behind the desk
d.path("M500,440 C576,440 632,492 640,570 C646,636 640,676 634,690 "
       "L366,690 C360,676 354,636 360,570 C368,492 424,440 500,440 Z",
       "Torso", fill=UNIFORM, stroke=INK, strokeWidth=7)
# placket + brass buttons
d.path("M500,452 L500,690", "Placket", fill=NONE, stroke=UNIFORM_DK,
       strokeWidth=6)
for i, y in enumerate([486, 542, 598, 654]):
    d.shape("ellipse", f"Button {i+1}", x=493, y=y, width=14, height=14,
            fill=BRASS, stroke=INK, strokeWidth=3)
# collar tabs
d.path("M454,452 L500,492 L546,452", "Collar", fill=NONE, stroke=INK,
       strokeWidth=6, join="round")
d.path("M456,452 L478,470 L462,486 Z", "Collar tab L", fill=BRASS,
       stroke=INK, strokeWidth=3)
d.path("M544,452 L522,470 L538,486 Z", "Collar tab R", fill=BRASS,
       stroke=INK, strokeWidth=3)
# name tag, blank — the record predates the user
d.shape("rectangle", "Name tag", x=548, y=520, width=58, height=18,
        fill="#E8DFC0", stroke=INK, strokeWidth=3)
d.shape("rectangle", "Name tag line", x=556, y=527, width=42, height=5,
        fill="#9A8F6C", opacity=80, stroke=NONE)

# head: detached procedural confidence
d.shape("ellipse", "Head", x=420, y=300, width=160, height=150,
        fill=FACE, stroke=INK, strokeWidth=7)
# peaked service cap
d.path("M424,332 C424,272 576,272 576,332 L560,332 C560,302 440,302 440,332 Z",
       "Cap crown", fill=UNIFORM, stroke=INK, strokeWidth=6, join="round")
d.path("M416,332 C452,318 548,318 584,332 C584,344 560,350 500,350 "
       "C440,350 416,344 416,332 Z", "Cap brim", fill=UNIFORM_DK,
       stroke=INK, strokeWidth=5, join="round")
d.shape("ellipse", "Cap badge", x=486, y=292, width=28, height=22,
        fill=BRASS, stroke=INK, strokeWidth=3)
# half-lidded eyes, flat mouth — nothing about this is personal
d.shape("ellipse", "Eye L", x=450, y=362, width=26, height=22, fill="#FBF4E2",
        stroke=INK, strokeWidth=4)
d.shape("ellipse", "Eye R", x=524, y=362, width=26, height=22, fill="#FBF4E2",
        stroke=INK, strokeWidth=4)
d.path("M450,366 L476,366 M524,366 L550,366", "Lids", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.shape("ellipse", "Pupil L", x=459, y=370, width=9, height=10, fill=INK,
        stroke=NONE)
d.shape("ellipse", "Pupil R", x=533, y=370, width=9, height=10, fill=INK,
        stroke=NONE)
d.path("M446,348 C456,342 468,342 476,346", "Brow L", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.path("M524,346 C532,342 544,342 554,348", "Brow R", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.path("M470,420 L530,420", "Flat mouth", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")

# the credential form on the desk, in front of the uniform
d.path(rot_rect_path(555, 668, 205, 112, -3), "Form sheet",
       fill="#F0E7CC", stroke=INK, strokeWidth=4)
for j, y in enumerate([632, 650, 668]):
    d.shape("rectangle", f"Form line {j+1}", x=485, y=y,
            width=100 if j < 2 else 70, height=6, fill="#9A8F6C",
            opacity=75, stroke=NONE)
# ghost imprint: the stamp has already hit once, offset — it duplicates itself
d.path(rot_rect_path(545, 650, 140, 58, -8), "Ghost imprint", fill=NONE,
       stroke=STAMP_RED, strokeWidth=4, opacity=22)
d.text("DUPLICATE", "Ghost text", x=545, y=664, size=22,
       font="Virelai Sans", color="#C27A6C", justify="center")
# fresh DUPLICATE imprint over the lines, tilted like a real stamp hit
d.path(rot_rect_path(528, 668, 140, 58, -8), "Imprint box", fill=NONE,
       stroke=STAMP_RED, strokeWidth=5, opacity=85)
d.text("DUPLICATE", "Imprint text", x=528, y=682, size=24,
       font="Virelai Sans", color=STAMP_RED, justify="center")

# right arm driving the stamp down onto the form
d.path("M612,556 C646,566 660,584 662,600", "Arm R", fill=NONE,
       stroke=UNIFORM, strokeWidth=30, cap="round")
# stamp: brass collar, wooden handle, red rubber face on the sheet
d.path("M652,568 L676,568 L670,612 L658,612 Z", "Stamp stem",
       fill=BRASS, stroke=INK, strokeWidth=4, join="round")
d.shape("ellipse", "Stamp knob", x=644, y=536, width=30, height=32,
        fill=DESK, stroke=INK, strokeWidth=4)
d.path("M646,612 L694,612 L702,644 L638,644 Z", "Stamp base",
       fill=STAMP_RED, stroke=INK, strokeWidth=5, join="round")
# impact ticks around the fresh strike
d.path("M630,600 L614,588 M706,594 L720,580 M668,590 L668,574",
       "Stamp impact", fill=NONE, stroke=STAMP_RED, strokeWidth=4,
       cap="round", opacity=80)

# left hand resting on a stack of identical blank forms
d.path("M390,560 C360,580 350,606 354,632", "Arm L", fill=NONE,
       stroke=UNIFORM, strokeWidth=30, cap="round")
for i, (dx, dy) in enumerate([(-6, -8), (0, -4), (6, 0)]):
    d.path(rot_rect_path(336+dx, 640+dy, 120, 84, -3), f"Blank form {i+1}",
           fill="#EAE1C4", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Hand L", x=346, y=622, width=32, height=26, fill=FACE,
        stroke=INK, strokeWidth=5)
d.shape("ellipse", "Hand R", x=640, y=576, width=32, height=26, fill=FACE,
        stroke=INK, strokeWidth=5)

# --- captions -------------------------------------------------------------------
d.text("FORMEE FORMESON", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#E4DCC0", justify="center")
r = d.text("IDENTITY DUPLICATION OFFICER", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#A8A684", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("011.formee-formeson-V1R00")
