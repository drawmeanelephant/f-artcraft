#!/usr/bin/env python3
"""Twiggy Snipsnark — mascot portrait V1R00. Layout Interrogator.
A smug little parser daemon with twig horns, snips in hand, correcting a
rogue indent on a floating template partial — one line sits left of its
block, a dashed ghost marks where it belongs, and Twiggy's pointer stick
is already there. {% %} lint drifts across the plate like gnats.
Plum-indigo plate on a purgatory-dark backdrop. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Code glyphs in Source Sans 3. Plate = circle (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Twiggy Snipsnark — Mascot Portrait", 1000, 1000)

INK = "#2A2030"   # warm dark ink, never black
BG_GRAD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000], "stops": [
    {"offset": 0, "color": "#161225"}, {"offset": 1, "color": "#070611"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#6E6398"}, {"offset": 0.62, "color": "#4A4272"},
    {"offset": 1, "color": "#221D3E"}]}}
SKIN_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#B8A8D8"}, {"offset": 0.7, "color": "#8E7CB8"},
    {"offset": 1, "color": "#5E5088"}]}}
SHEET_GRAD = {"gradient": {"kind": "linear", "start": [0, 250], "end": [0, 620], "stops": [
    {"offset": 0, "color": "#F2EAD6"}, {"offset": 0.7, "color": "#E0D3B2"},
    {"offset": 1, "color": "#C4B48C"}]}}
DOG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#FBF4E2"}, {"offset": 1, "color": "#D8C9A4"}]}}
TWIG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#8A6A4E"}, {"offset": 1, "color": "#5A4230"}]}}
LINT = "#C8BEF0"
RED = "#D96A5A"

PCX, PCY, PR = 500, 460, 420

def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#5A5088", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#16112A", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#CFC6EC", strokeWidth=3, opacity=28)
# patina + flecks
d.shape("ellipse", "Patina 1", x=190, y=300, width=250, height=160,
        fill="#8278AC", opacity=16, stroke=NONE)
d.shape("ellipse", "Patina 2", x=580, y=590, width=260, height=150,
        fill="#332C55", opacity=32, stroke=NONE)
for i, (x, y, w) in enumerate([(215,340,5),(795,335,6),(180,540,5),(838,565,5),
                               (255,755,5),(730,760,6),(160,450,5),(852,645,5),
                               (430,135,5),(600,140,6),(335,170,4),(705,200,5),
                               (250,655,4),(660,715,5)]):
    assert on_disc(x, y, 12), (x, y)
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#DCD4F4", opacity=28, stroke=NONE)
# drifting template lint — faint {% %} glyphs
def faint_text(t, label, opacity, **kw):
    r = d.text(t, label, **kw)
    if r and r.get("id"):
        d.cmd("object.setProps", f"{label} opacity", id=r["id"],
              opacity=opacity)

for i, (t, x, y, s) in enumerate([("{%", 200, 240, 26), ("%}", 770, 210, 24),
                                  ("{{", 165, 650, 22), ("}}", 800, 720, 26),
                                  ("{%", 620, 130, 20)]):
    assert on_disc(x, y, 20), (x, y)
    faint_text(t, f"Lint {i+1}", 25, x=x, y=y, size=s,
               font="Source Sans 3", color=LINT, justify="center")
# ghost arcs on the dark backdrop
d.path("M935,165 A100,100 0 0 0 855,70", "Ghost arc TR",
       fill=NONE, stroke="#6E6098", strokeWidth=14, opacity=10, cap="round")
d.path("M75,775 A115,115 0 0 0 180,880", "Ghost arc BL",
       fill=NONE, stroke="#6E6098", strokeWidth=10, opacity=8, cap="round")

# --- the malformed template partial ------------------------------------------
d.shape("ellipse", "Sheet shadow", x=400, y=610, width=360, height=40,
        fill="#0A0816", opacity=42, stroke=NONE)
# sheet body with dog-eared top-right corner
d.path("M410,240 L680,240 L730,290 L730,600 C730,614 718,620 704,620 "
       "L430,620 C416,620 410,614 410,600 Z",
       "Sheet body", fill=SHEET_GRAD, stroke=INK, strokeWidth=5)
d.path("M680,240 L730,290 L682,290 C678,276 678,256 680,240 Z",
       "Dog ear", fill=DOG_GRAD, stroke=INK, strokeWidth=3.5)
d.path("M700,300 L700,600 C700,606 695,610 688,610 L690,300 Z",
       "Sheet shade R", fill="#A8946C", opacity=35, stroke=NONE)
d.path("M418,252 L722,252", "Sheet top light",
       fill=NONE, stroke="#FFF9E8", strokeWidth=3, opacity=55, cap="round")

# template header lines — {% block %} frame, all correctly indented
CODE = "#5A4E3E"
d.text("{% block body %}", "Block open", x=436, y=286, size=17,
       font="Source Sans 3", color=CODE)
d.text("{% endif %}", "Block close", x=436, y=594, size=17,
       font="Source Sans 3", color=CODE)
# properly indented code rows (aligned at x=480)
for j, (yy, w) in enumerate([(320, 150), (352, 190), (416, 165), (448, 120),
                             (512, 180), (544, 140)]):
    d.path(f"M480,{yy} L{480 + w},{yy}", f"Code line {j+1}",
           fill=NONE, stroke="#8A7A5C", strokeWidth=9, opacity=55,
           cap="round")
    # indent guide ticks
    d.path(f"M452,{yy} L456,{yy}", f"Guide {j+1}",
           fill=NONE, stroke="#6A5A42", strokeWidth=3, opacity=40)
# THE offending line: sits flush-left at 436 where it belongs at 480
d.path("M436,384 L596,384", "Bad indent line",
       fill=NONE, stroke=RED, strokeWidth=9, opacity=85, cap="round")
# dashed ghost where it belongs
d.shape("rectangle", "Ghost slot", x=476, y=374, width=124, height=18,
        radius=9, fill=NONE, stroke=RED, strokeWidth=2, dash=[5, 5],
        opacity=70)
# correction arrow: bad → good
d.path("M444,398 C452,416 468,420 484,414 M484,414 L472,412 M484,414 L478,404",
       "Correction arrow", fill=NONE, stroke=RED, strokeWidth=3,
       opacity=80, cap="round")
# red pen marks: a small circle-slash over the bad whitespace
d.path("M424,378 C416,388 418,398 428,402 C438,404 446,396 444,386",
       "Pen circle", fill=NONE, stroke=RED, strokeWidth=2.5,
       opacity=70, cap="round")

# --- Twiggy himself -------------------------------------------------------------
# cast shadow
d.shape("ellipse", "Body shadow", x=170, y=758, width=280, height=42,
        fill="#0A0816", opacity=45, stroke=NONE)
# little feet
d.path("M262,742 C252,762 260,776 284,776 C304,776 310,766 306,752 Z",
       "Foot L", fill=SKIN_GRAD, stroke=INK, strokeWidth=3.5)
d.path("M340,742 C350,762 342,776 318,776 C298,776 292,766 296,752 Z",
       "Foot R", fill=SKIN_GRAD, stroke=INK, strokeWidth=3.5)
# pear-shaped body — smug belly
d.path("M300,460 C232,480 196,560 204,648 C210,720 250,756 300,756 "
       "C350,756 390,720 396,648 C404,560 368,480 300,460 Z",
       "Body", fill=SKIN_GRAD, stroke=INK, strokeWidth=5)
# belly shading + rim light
d.path("M372,540 C384,600 380,680 352,724 C368,680 368,600 356,548 Z",
       "Belly shade", fill="#463A6A", opacity=40, stroke=NONE)
d.path("M222,540 C214,600 218,670 240,716", "Rim light",
       fill=NONE, stroke="#DCD2F4", strokeWidth=4, opacity=45, cap="round")

# twig horns — gnarled little branches off the head
for side, sx in (("L", -1), ("R", 1)):
    bx = 300 + sx * 52
    d.path(f"M{bx},470 C{bx + sx*10},430 {bx + sx*26},410 {bx + sx*22},378 "
           f"M{bx + sx*14},424 C{bx + sx*30},418 {bx + sx*38},404 {bx + sx*46},400",
           f"Twig horn {side}", fill=NONE, stroke="#5A4230",
           strokeWidth=6, cap="round")
    d.path(f"M{bx + sx*22},378 L{bx + sx*34},362",
           f"Twig tip {side}", fill=NONE, stroke="#5A4230",
           strokeWidth=4, cap="round")
    # one spring leaf per horn
    lx = bx + sx * 46
    d.path(f"M{lx},400 C{lx + sx*16},388 {lx + sx*22},396 {lx + sx*18},408 "
           f"C{lx + sx*8},412 {lx},408 {lx},400 Z",
           f"Leaf {side}", fill=TWIG_GRAD, stroke=INK, strokeWidth=2)

# face: half-lidded smug eyes, flat condescending mouth
d.path("M242,548 C256,540 276,540 288,548 C276,556 256,556 242,548 Z",
       "Eye L", fill="#F4EEFC", stroke=INK, strokeWidth=3.5)
d.path("M312,548 C326,540 346,540 358,548 C346,556 326,556 312,548 Z",
       "Eye R", fill="#F4EEFC", stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Pupil L", x=258, y=543, width=10, height=10,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Pupil R", x=336, y=543, width=10, height=10,
        fill=INK, stroke=NONE)
# lids — the smugness
d.path("M240,544 C258,534 280,534 290,544", "Lid L",
       fill=NONE, stroke=INK, strokeWidth=4, cap="round")
d.path("M310,544 C328,534 350,534 360,544", "Lid R",
       fill=NONE, stroke=INK, strokeWidth=4, cap="round")
# raised brow + flat mouth
d.path("M238,522 C258,512 282,512 294,520", "Brow L",
       fill=NONE, stroke=INK, strokeWidth=3.5, cap="round")
d.path("M272,600 L328,600 C330,596 330,594 328,592", "Mouth",
       fill=NONE, stroke=INK, strokeWidth=4, cap="round")

# left arm akimbo, holding the snips low
d.path("M214,600 C188,622 180,652 190,676 C202,684 216,678 218,664 "
       "C210,644 214,624 226,610 Z",
       "Arm L", fill=SKIN_GRAD, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Hand L", x=182, y=660, width=30, height=26,
        fill="#8E7CB8", stroke=INK, strokeWidth=3)
# tiny snips in the left hand — two blades ajar
d.path("M196,668 L224,646 M196,668 L230,664", "Snips blades",
       fill=NONE, stroke="#3A3644", strokeWidth=4, cap="round")
d.shape("ellipse", "Snips ring 1", x=188, y=664, width=12, height=12,
        fill=NONE, stroke="#3A3644", strokeWidth=3)
d.shape("ellipse", "Snips ring 2", x=198, y=672, width=12, height=12,
        fill=NONE, stroke="#3A3644", strokeWidth=3)

# right arm extended, pointer stick touching the bad line's ghost slot
d.path("M386,560 C420,548 452,540 478,534 C492,536 494,550 484,556 "
       "C456,564 426,574 398,586 Z",
       "Arm R", fill=SKIN_GRAD, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Hand R", x=474, y=526, width=28, height=28,
        fill="#8E7CB8", stroke=INK, strokeWidth=3)
d.path("M492,540 L530,408", "Pointer stick",
       fill=NONE, stroke="#5A4230", strokeWidth=5, cap="round")
d.shape("ellipse", "Pointer tip", x=524, y=400, width=12, height=12,
        fill=RED, stroke=INK, strokeWidth=2)

# stray commented-out mutter, faint beside him
faint_text("{# clear cache #}", "Mutter", 45, x=250, y=830, size=19,
           font="Source Sans 3", color=LINT, justify="center")

# --- name + role ----------------------------------------------------------------------
d.text("TWIGGY SNIPSNARK", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#E4DEF4", justify="center")
r = d.text("LAYOUT INTERROGATOR", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#AEA2D8", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("048.twiggy-snipsnark-V1R00")
