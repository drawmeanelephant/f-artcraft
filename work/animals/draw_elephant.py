#!/usr/bin/env python3
"""Elephant — field-guide plate V1R00. Front-on portrait: ears spread like
sails, tusks set low and wide, trunk hanging center and curling at the tip.
Warm dust-grey mass on an amber savanna dusk, low sun behind the left ear,
dry-grass band closing on the disc arc. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Elephant — Field Plate", 1000, 1000)

INK = "#2E2118"
BG_GRAD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000], "stops": [
    {"offset": 0, "color": "#1C1410"}, {"offset": 1, "color": "#0A0605"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#EFC084"}, {"offset": 0.62, "color": "#D09A5C"},
    {"offset": 1, "color": "#96633A"}]}}
SKIN_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#B5AA9C"}, {"offset": 0.6, "color": "#8D8172"},
    {"offset": 1, "color": "#655A4D"}]}}
EAR_INNER = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#C4A795"}, {"offset": 1, "color": "#96786A"}]}}
TUSK_GRAD = {"gradient": {"kind": "linear", "start": [0, 560], "end": [0, 740], "stops": [
    {"offset": 0, "color": "#F2E6CC"}, {"offset": 1, "color": "#C0A276"}]}}
GRASS_GRAD = {"gradient": {"kind": "linear", "start": [0, 720], "end": [0, 880], "stops": [
    {"offset": 0, "color": "#D8A85C"}, {"offset": 1, "color": "#96682F"}]}}

PCX, PCY, PR = 500, 460, 420

def on_disc(x, y, pad):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

# --- backdrop + amber dusk plate ---------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#D09A5C", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#6E4626", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F4DCA8", strokeWidth=3, opacity=50)

# low sun sinking behind the left ear + its haze
d.shape("ellipse", "Sun haze", x=170, y=150, width=230, height=230,
        fill="#FFD98F", opacity=16, stroke=NONE)
d.shape("ellipse", "Sun", x=200, y=180, width=170, height=170,
        fill="#FFD98F", opacity=60, stroke=NONE)

# dusk dust motes drifting in the plate
for i, (x, y, w) in enumerate([(200,300,7),(770,250,6),(170,470,8),(825,430,7),(240,690,6),
                               (750,700,8),(150,380,5),(855,560,6),(400,110,6),(605,105,7),
                               (310,160,5),(700,175,6),(335,800,6),(665,810,5),(505,95,5)]):
    assert on_disc(x + w/2, y + w/2, 6), (x, y)
    d.shape("ellipse", f"Dust mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#F4DCA8", opacity=35, stroke=NONE)
# distant birds, high right
for i, dd in enumerate(["M680,220 Q690,212 700,220 Q710,212 720,220",
                        "M735,255 Q744,248 753,255 Q762,248 771,255",
                        "M640,255 Q649,248 658,255 Q667,248 676,255"]):
    d.path(dd, f"Bird {i+1}", fill=NONE, stroke="#5A3B22",
           strokeWidth=4, opacity=55, cap="round")

# --- dry-grass ground band, closing on the disc's own arc --------------------------
d.path("M194,748 C380,730 620,730 806,748 A420,420 0 0 1 194,748 Z",
       "Grass band", fill=GRASS_GRAD, stroke="#7A5228", strokeWidth=4)
d.path("M240,762 C380,752 620,752 760,764", "Band shade", fill=NONE,
       stroke="#8A5F30", strokeWidth=5, opacity=45, cap="round")
for i, dd in enumerate(["M250,760 Q258,730 268,712", "M300,768 Q306,742 318,726",
                        "M700,766 Q694,738 682,720", "M745,758 Q738,732 726,716",
                        "M360,772 Q364,748 374,734", "M640,772 Q636,748 626,732"]):
    d.path(dd, f"Grass blade {i+1}", fill=NONE, stroke="#B08040",
           strokeWidth=5, opacity=60, cap="round")

# --- ears: spread like sails -------------------------------------------------------
d.path("M412,335 C345,295 245,255 190,290 C145,318 138,405 158,470 "
       "C182,550 280,602 352,596 C375,540 388,465 396,415 "
       "C401,380 406,352 412,335 Z",
       "Ear L", fill=SKIN_GRAD, stroke=INK, strokeWidth=7)
d.path("M588,335 C655,295 755,255 810,290 C855,318 862,405 842,470 "
       "C818,550 720,602 648,596 C625,540 612,465 604,415 "
       "C599,380 594,352 588,335 Z",
       "Ear R", fill=SKIN_GRAD, stroke=INK, strokeWidth=7)
# inner-ear shading + fold ridges
d.path("M390,355 C330,320 250,290 208,318 C175,342 172,410 190,462 "
       "C212,530 290,572 344,566 C362,516 374,450 382,405 Z",
       "Ear L inner", fill=EAR_INNER, opacity=55, stroke=NONE)
d.path("M610,355 C670,320 750,290 792,318 C825,342 828,410 810,462 "
       "C788,530 710,572 656,566 C638,516 626,450 618,405 Z",
       "Ear R inner", fill=EAR_INNER, opacity=55, stroke=NONE)
for lbl, dd in [("Ear L fold", "M380,380 C320,355 255,340 215,360"),
                ("Ear R fold", "M620,380 C680,355 745,340 785,360"),
                ("Ear L fold 2", "M368,470 C315,465 255,470 215,495"),
                ("Ear R fold 2", "M632,470 C685,465 745,470 785,495")]:
    d.path(dd, lbl, fill=NONE, stroke="#5F5346", strokeWidth=5, opacity=45, cap="round")

# --- head dome ----------------------------------------------------------------------
d.path("M500,292 C588,292 662,345 680,432 C694,505 678,580 640,632 "
       "C602,676 548,694 500,694 C452,694 398,676 360,632 "
       "C322,580 306,505 320,432 C338,345 412,292 500,292 Z",
       "Head", fill=SKIN_GRAD, stroke=INK, strokeWidth=7)
# crown highlight + jowl shading
d.shape("ellipse", "Crown light", x=400, y=300, width=200, height=80,
        fill="#FFFFFF", opacity=13, stroke=NONE)
d.path("M352,560 C370,620 430,660 500,662 C570,660 630,620 648,560 "
       "C640,640 575,690 500,692 C425,690 360,640 352,560 Z",
       "Jowl shade", fill="#4E443A", opacity=28, stroke=NONE)
# forehead crease + temple lines
for i, dd in enumerate(["M400,352 C460,338 540,338 600,352",
                        "M415,395 C465,384 535,384 585,395",
                        "M352,470 C368,478 382,480 396,478",
                        "M648,470 C632,478 618,480 604,478"]):
    d.path(dd, f"Crease {i+1}", fill=NONE, stroke="#5F5346",
           strokeWidth=5, opacity=40, cap="round")

# --- tusks: set low and wide ---------------------------------------------------------
d.path("M450,575 C405,600 372,650 354,714 L368,726 "
       "C392,674 428,640 468,622 C472,602 466,582 450,575 Z",
       "Tusk L", fill=TUSK_GRAD, stroke=INK, strokeWidth=6)
d.path("M550,575 C595,600 628,650 646,714 L632,726 "
       "C608,674 572,640 532,622 C528,602 534,582 550,575 Z",
       "Tusk R", fill=TUSK_GRAD, stroke=INK, strokeWidth=6)

# --- trunk: hanging center, tip curling left -----------------------------------------
d.path("M462,478 C452,580 444,680 452,758 "
       "C458,800 482,822 510,814 "
       "C536,808 546,782 530,764 "
       "C522,754 508,756 502,768 "
       "C516,752 522,722 518,682 "
       "C513,602 520,522 540,480 "
       "C520,464 480,464 462,478 Z",
       "Trunk", fill=SKIN_GRAD, stroke=INK, strokeWidth=7)
# trunk ridge wrinkles
for i, dd in enumerate(["M458,545 C485,556 515,556 538,545",
                        "M452,610 C482,622 512,622 534,610",
                        "M450,675 C478,687 508,687 528,675",
                        "M455,735 C478,746 500,746 516,736"]):
    d.path(dd, f"Trunk ridge {i+1}", fill=NONE, stroke="#5F5346",
           strokeWidth=6, opacity=50, cap="round")
# trunk tip shading on the curl
d.shape("ellipse", "Trunk tip shade", x=472, y=748, width=60, height=58,
        fill="#4E443A", opacity=30, stroke=NONE)

# --- eyes: deep-set under the brow ----------------------------------------------------
d.shape("ellipse", "Brow L", x=380, y=455, width=80, height=42,
        fill="#6E6154", opacity=55, stroke=NONE)
d.shape("ellipse", "Brow R", x=540, y=455, width=80, height=42,
        fill="#6E6154", opacity=55, stroke=NONE)
d.shape("ellipse", "Eye L", x=398, y=478, width=34, height=40, fill="#241A12", stroke=NONE)
d.shape("ellipse", "Eye R", x=568, y=478, width=34, height=40, fill="#241A12", stroke=NONE)
d.shape("ellipse", "Glint L", x=406, y=486, width=9, height=9, fill="#FFFFFF", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=576, y=486, width=9, height=9, fill="#FFFFFF", opacity=90, stroke=NONE)
d.path("M388,470 C404,462 428,462 444,470", "Brow line L", fill=NONE,
       stroke=INK, strokeWidth=6, cap="round")
d.path("M556,470 C572,462 596,462 612,470", "Brow line R", fill=NONE,
       stroke=INK, strokeWidth=6, cap="round")

# --- name -----------------------------------------------------------------------------
d.text("ELEPHANT", "Name", x=500, y=962, size=60, font="Virelai Sans",
       color="#F0D8AE", justify="center")

d.finish("elephant-V1R00")
