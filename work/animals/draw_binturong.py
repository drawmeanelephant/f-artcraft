#!/usr/bin/env python3
"""Binturong — field-guide plate V1R00. Full body in profile facing left,
walking a diagonal branch: coarse black fur, grizzled grey mask, tufted ears,
one musk-yellow eye, long whiskers; the prehensile tail wraps twice around
the wood behind the body and the tip hangs in a hook. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Binturong — Field Plate", 1000, 1000)

INK = "#1E1712"
BG_GRAD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000], "stops": [
    {"offset": 0, "color": "#152A20"}, {"offset": 1, "color": "#050C09"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#EAE5CB"}, {"offset": 0.7, "color": "#BFBD9E"},
    {"offset": 1, "color": "#7E8262"}]}}
FUR_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#554839"}, {"offset": 0.6, "color": "#2C241C"},
    {"offset": 1, "color": "#14100C"}]}}
MASK_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#C6BCA4"}, {"offset": 1, "color": "#8A8069"}]}}
BRANCH_GRAD = {"gradient": {"kind": "linear", "start": [0, 620], "end": [0, 700], "stops": [
    {"offset": 0, "color": "#8A6F4E"}, {"offset": 1, "color": "#4A3624"}]}}
TAIL_GRAD = {"gradient": {"kind": "linear", "start": [0, 560], "end": [0, 760], "stops": [
    {"offset": 0, "color": "#453A2E"}, {"offset": 1, "color": "#1A1410"}]}}
LEG_GRAD = {"gradient": {"kind": "linear", "start": [0, 600], "end": [0, 710], "stops": [
    {"offset": 0, "color": "#3A2F26"}, {"offset": 1, "color": "#181210"}]}}

PCX, PCY, PR = 500, 460, 420

def on_disc(x, y, pad):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

# --- backdrop + plate ---------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#BFBD9E", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#5C6648", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F2F0DE", strokeWidth=3, opacity=55)
# soft leaf shadows high in the plate
for i, (x, y, w, h) in enumerate([(160,140,220,120),(700,120,200,110),(590,170,160,90)]):
    d.shape("ellipse", f"Leaf shade {i+1}", x=x, y=y, width=w, height=h,
            fill="#6E7A52", opacity=16, stroke=NONE)
for i, (x, y, w) in enumerate([(210,300,8),(770,270,7),(160,470,7),(830,430,8),(250,180,6),(700,190,7),
                               (400,130,7),(600,125,8),(150,560,6),(860,540,6),(330,220,5),(680,240,5)]):
    assert on_disc(x + w / 2, y + w / 2, 8), (x, y)
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#6E765E", opacity=40, stroke=NONE)

# --- tail, far side: root + the under/behind connector between the two wraps ---------
# (drawn before the branch so the branch band hides the middles)
d.path("M700,566 C722,580 726,600 706,630", "Tail root", fill=NONE,
       stroke="#241C15", strokeWidth=30, cap="round")
d.path("M742,712 C760,754 804,754 814,716 C822,684 808,644 794,616",
       "Tail far wrap", fill=NONE, stroke="#1E1712", strokeWidth=28, cap="round")

# --- the branch: both ends close on the disc's own arc --------------------------------
d.path("M121,640 C370,624 630,624 879,640 A420,420 0 0 1 848,695 "
       "C630,682 370,682 152,695 A420,420 0 0 1 121,640 Z",
       "Branch", fill=BRANCH_GRAD, stroke=INK, strokeWidth=5)
for i, dd in enumerate(["M170,652 C300,644 420,646 520,652",
                        "M580,650 C680,646 780,644 850,650",
                        "M210,676 C330,670 450,672 540,676",
                        "M620,672 C700,668 780,668 830,672"]):
    d.path(dd, f"Bark groove {i+1}", fill=NONE, stroke="#2A1E14",
           strokeWidth=3, opacity=45, cap="round")
d.path("M140,638 C370,622 630,622 860,638", "Branch top light", fill=NONE,
       stroke="#B7A184", strokeWidth=4, opacity=45, cap="round")
# moss + a sprig on the branch's right end
d.shape("ellipse", "Moss 1", x=250, y=634, width=70, height=18, fill="#7E8C54", opacity=45, stroke=NONE)
d.shape("ellipse", "Moss 2", x=700, y=632, width=56, height=16, fill="#7E8C54", opacity=40, stroke=NONE)
for i, dd in enumerate(["M838,632 C840,610 832,596 818,588", "M846,634 C852,616 864,606 878,604"]):
    d.path(dd, f"Sprig stem {i+1}", fill=NONE, stroke="#4E5C38", strokeWidth=3, cap="round")
d.shape("ellipse", "Sprig leaf 1", x=804, y=580, width=26, height=14, fill="#8FA060", stroke="#3E4A2C", strokeWidth=2)
d.shape("ellipse", "Sprig leaf 2", x=866, y=596, width=24, height=13, fill="#8FA060", stroke="#3E4A2C", strokeWidth=2)

# --- body mass: arched back, low head, walking left -----------------------------------
BODY = ("M296,560 "
        "C292,534 306,508 332,486 "        # snout bridge to forehead
        "C355,468 390,455 430,450 "        # crown
        "C500,436 590,430 648,442 "        # arched back, rump highest
        "C692,450 718,484 724,525 "        # rump rounding
        "C728,565 716,600 690,616 "        # rump rear down
        "C640,632 540,634 460,624 "        # belly
        "C420,618 395,604 384,586 "        # chest
        "C360,600 330,600 314,586 "        # jaw underside
        "C302,576 296,570 296,560 Z")      # chin to nose
d.path(BODY, "Body", fill=FUR_GRAD, stroke=INK, strokeWidth=7)
# guard-hair spikes along the back
for i in range(24):
    x = 340 + i * 15.5
    y = 500 - 62 * math.sin((x - 340) / 360 * math.pi * 0.8 + 0.5)
    d.path(f"M{x:.0f},{y+14:.0f} L{x+4:.0f},{y-6:.0f}", f"Back spike {i+1}",
           fill=NONE, stroke="#241C15", strokeWidth=5, cap="round")
# flank texture strokes
for i, dd in enumerate(["M460,500 C520,494 580,496 640,508",
                        "M450,540 C520,534 600,536 668,552",
                        "M470,580 C540,576 610,578 660,590"]):
    d.path(dd, f"Flank fur {i+1}", fill=NONE, stroke="#4E4234",
           strokeWidth=4, opacity=40, cap="round")
d.shape("ellipse", "Rump shade", x=620, y=520, width=110, height=90,
        fill="#0E0A07", opacity=25, stroke=NONE)
d.shape("ellipse", "Shoulder light", x=430, y=452, width=140, height=44,
        fill="#8A7862", opacity=18, stroke=NONE)
# neck crease separating head from shoulders
d.path("M438,470 C452,505 452,550 436,586", "Neck crease", fill=NONE,
       stroke="#0E0A07", strokeWidth=10, opacity=30, cap="round")

# --- legs gripping the branch (in front of it) ----------------------------------------
for label, xx in (("Foreleg", 392), ("Hind leg", 618)):
    d.path(f"M{xx},598 C{xx+8},640 {xx+8},672 {xx+2},700 L{xx-34},700 "
           f"C{xx-38},668 {xx-36},634 {xx-32},600 Z",
           label, fill=LEG_GRAD, stroke=INK, strokeWidth=4)
    d.shape("ellipse", f"{label} paw", x=xx-40, y=686, width=52, height=28,
            fill="#2A211A", stroke=INK, strokeWidth=4)
    for j in range(3):
        d.path(f"M{xx-26+j*14},692 L{xx-28+j*14},706", f"{label} toe {j+1}",
               fill=NONE, stroke="#14100C", strokeWidth=3, cap="round")

# --- tail, near side: two bands crossing the face, then the hanging hook ---------------
d.path("M702,620 C716,652 730,682 742,712", "Tail wrap 1", fill=NONE,
       stroke=TAIL_GRAD, strokeWidth=32, cap="round")
d.path("M794,616 C810,648 824,676 834,706", "Tail wrap 2", fill=NONE,
       stroke=TAIL_GRAD, strokeWidth=28, cap="round")
d.path("M834,706 C842,738 824,760 792,762 C766,763 754,748 762,732",
       "Tail tip", fill=NONE, stroke="#241C15", strokeWidth=20, cap="round")
d.path("M792,762 C766,763 754,748 762,732", "Tail hook", fill=NONE,
       stroke="#3A2F24", strokeWidth=10, cap="round")
# tail sheen along each wrap
d.path("M708,630 C720,658 732,682 740,704", "Wrap sheen 1", fill=NONE,
       stroke="#6E5E4C", strokeWidth=6, opacity=45, cap="round")
d.path("M800,626 C812,652 822,676 830,698", "Wrap sheen 2", fill=NONE,
       stroke="#6E5E4C", strokeWidth=5, opacity=45, cap="round")

# --- ears with long tufts ---------------------------------------------------------------
d.path("M442,462 C438,440 446,420 464,412 C476,422 476,444 468,460 Z",
       "Ear far", fill="#241C15", stroke=INK, strokeWidth=4)
d.path("M382,462 C374,436 380,414 402,406 C418,414 420,438 410,460 Z",
       "Ear near", fill="#3A2F26", stroke=INK, strokeWidth=4)
for i, dd in enumerate(["M390,424 l-10,-24", "M400,420 l-2,-28", "M410,424 l9,-22",
                        "M452,428 l-4,-20", "M462,426 l5,-20"]):
    d.path(dd, f"Ear tuft {i+1}", fill=NONE, stroke="#1E1712",
           strokeWidth=4, cap="round")

# --- grizzled mask + face ---------------------------------------------------------------
# grizzle sits as a cap on the crown and upper cheek; muzzle and jaw stay dark
d.path("M320,506 C326,476 356,456 396,450 C428,447 450,460 455,484 "
       "C457,502 448,518 430,526 C400,534 362,530 342,520 C330,514 320,512 320,506 Z",
       "Mask", fill=MASK_GRAD, opacity=58, stroke=NONE)
# dark muzzle over the mask's front edge
d.path("M296,548 C296,528 308,510 328,502 C336,516 334,540 324,556 "
       "C312,560 300,556 296,548 Z",
       "Muzzle", fill="#241C15", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Nostril", x=298, y=536, width=12, height=9,
        fill="#0C0906", stroke=NONE)
d.path("M300,564 C308,570 318,572 328,570", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
# the one musk-yellow eye
d.shape("ellipse", "Eye socket", x=352, y=494, width=38, height=36,
        fill="#4E4234", opacity=55, stroke=NONE)
d.shape("ellipse", "Iris", x=358, y=500, width=24, height=24, fill="#E3AC40",
        stroke=INK, strokeWidth=3)
d.shape("ellipse", "Pupil", x=365, y=504, width=12, height=15, fill="#120D08",
        stroke=NONE)
d.shape("ellipse", "Glint", x=363, y=503, width=6, height=6, fill="#FFFFFF",
        opacity=85, stroke=NONE)
d.path("M352,494 C364,486 384,486 396,494", "Brow line", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
# grizzle speckles on the mask
for i, (x, y) in enumerate([(330,480),(350,470),(380,462),(410,468),(335,510),(430,490),(400,540),(355,545)]):
    d.shape("ellipse", f"Grizzle {i+1}", x=x, y=y, width=6, height=5,
            fill="#EFE8D4", opacity=45, stroke=NONE)

# --- long whiskers fanning forward -------------------------------------------------------
for i, dd in enumerate(["M306,548 C270,530 240,522 212,522",
                        "M304,556 C268,548 236,548 208,556",
                        "M306,564 C272,566 242,574 216,590",
                        "M310,570 C280,580 254,594 236,614"]):
    d.path(dd, f"Whisker {i+1}", fill=NONE, stroke="#DAD2C0",
           strokeWidth=3, opacity=70, cap="round")

# --- name -----------------------------------------------------------------------------
d.text("BINTURONG", "Name", x=500, y=962, size=60, font="Virelai Sans",
       color="#E4E0C8", justify="center")

print("extent check done")
d.finish("binturong-V1R00")
