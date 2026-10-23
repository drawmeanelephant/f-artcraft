#!/usr/bin/env python3
"""Aye-aye — field-guide plate V1R00. Head/bust portrait on a moonlit disc:
huge amber eyes, leathery ears, wiry fur, long thin middle finger raised
beside the face. Nocturnal palette. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Aye-aye — Field Plate", 1000, 1000)

INK = "#1D1410"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1B1428"}, {"offset": 1, "color": "#08060E"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E4E8F2"}, {"offset": 0.7, "color": "#B4BCCF"},
    {"offset": 1, "color": "#7E87A0"}]}}
HEAD_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4A382B"}, {"offset": 0.7, "color": "#2C1F17"},
    {"offset": 1, "color": "#1A120C"}]}}
BUST_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#33261C"}, {"offset": 1, "color": "#140D08"}]}}
EAR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3D2C20"}, {"offset": 1, "color": "#201510"}]}}
IRIS_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#FBD06A"}, {"offset": 0.6, "color": "#E89A2E"},
    {"offset": 1, "color": "#8A4E10"}]}}
HAND_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3A2A1E"}, {"offset": 1, "color": "#211710"}]}}

# --- backdrop + stars + plate ----------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
for i, (x, y, w, o) in enumerate([(55,90,7,60),(130,40,5,45),(60,300,6,50),(45,650,5,40),
                                  (920,60,7,55),(870,120,5,40),(955,320,6,50),(940,700,5,45),
                                  (70,860,6,45),(935,860,5,40)]):
    d.shape("ellipse", f"Star {i+1}", x=x, y=y, width=w, height=w, fill="#C9CEDE", opacity=o, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#4E5570", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E9EDF5", strokeWidth=3, opacity=50)
# moon craters / mare blotches
d.shape("ellipse", "Crater 1", x=200, y=180, width=180, height=120, fill="#98A0B5", opacity=18, stroke=NONE)
d.shape("ellipse", "Crater 2", x=640, y=600, width=220, height=130, fill="#98A0B5", opacity=15, stroke=NONE)
d.shape("ellipse", "Crater 3", x=560, y=200, width=120, height=80, fill="#98A0B5", opacity=14, stroke=NONE)
d.shape("ellipse", "Crater 4", x=160, y=560, width=140, height=90, fill="#98A0B5", opacity=16, stroke=NONE)
for i, (x, y, w) in enumerate([(250,320,9),(740,180,7),(180,430,8),(800,520,9),(300,760,7),
                               (680,760,8),(130,500,6),(830,380,7),(430,110,8),(590,130,7)]):
    d.shape("ellipse", f"Moon fleck {i+1}", x=x, y=y, width=w, height=w, fill="#7E87A0", opacity=40, stroke=NONE)

# --- bust: shoulder mound, bottom edge curved to sit inside the disc ---------------
d.path("M312,822 C312,756 352,700 408,680 C462,662 538,662 592,680 "
       "C648,700 688,756 688,822 C630,856 560,868 500,868 "
       "C440,868 370,856 312,822 Z",
       "Shoulders", fill=BUST_GRAD, stroke=INK, strokeWidth=7)
# chest shading + a little wiry chest fur
d.shape("ellipse", "Chest shade", x=390, y=730, width=220, height=110, fill="#0F0A06", opacity=35, stroke=NONE)

# --- ears behind the head: big leathery pointed lobes -------------------------------
d.path("M412,440 C355,395 285,315 250,238 C238,210 250,182 280,194 "
       "C345,222 405,305 438,398 C447,424 438,444 412,440 Z",
       "Ear L", fill=EAR_GRAD, stroke=INK, strokeWidth=7)
d.path("M588,440 C645,395 715,315 750,238 C762,210 750,182 720,194 "
       "C655,222 595,305 562,398 C553,424 562,444 588,440 Z",
       "Ear R", fill=EAR_GRAD, stroke=INK, strokeWidth=7)
# inner membranes
d.path("M400,415 C360,380 310,320 285,255 C278,236 288,222 305,232 "
       "C352,260 395,325 418,392 C424,408 415,420 400,415 Z",
       "Inner ear L", fill="#8A6350", opacity=60, stroke=NONE)
d.path("M600,415 C640,380 690,320 715,255 C722,236 712,222 695,232 "
       "C648,260 605,325 582,392 C576,408 585,420 600,415 Z",
       "Inner ear R", fill="#8A6350", opacity=60, stroke=NONE)

# --- head ---------------------------------------------------------------------------
d.path("M500,340 C615,340 695,425 700,530 C705,635 640,720 548,738 "
       "C528,746 472,746 452,738 C360,720 295,635 300,530 "
       "C305,425 385,340 500,340 Z",
       "Head", fill=HEAD_GRAD, stroke=INK, strokeWidth=8)
# moonlit rim along the crown and left cheek
d.path("M368,412 C408,356 466,334 545,340", "Crown rim light", fill=NONE,
       stroke="#B98A4A", strokeWidth=7, opacity=22, cap="round")
d.path("M306,500 C300,560 312,624 340,672", "Cheek rim light", fill=NONE,
       stroke="#B98A4A", strokeWidth=6, opacity=18, cap="round")
# wiry crown tufts + stray hairs
for i, dd in enumerate(["M455,352 C448,332 444,314 448,296", "M492,344 L488,302",
                        "M540,350 C548,330 552,312 550,296", "M430,360 C420,344 412,332 412,318",
                        "M575,368 C586,352 592,338 592,324"]):
    d.path(dd, f"Crown tuft {i+1}", fill=NONE, stroke="#6B5340", strokeWidth=5, opacity=70, cap="round")

# --- eyes: the signature huge amber gaze ---------------------------------------------
# brow shadows above the eyes deepen the stare
d.shape("ellipse", "Brow shade L", x=350, y=430, width=130, height=42, fill="#0F0A06", opacity=35, stroke=NONE)
d.shape("ellipse", "Brow shade R", x=520, y=430, width=130, height=42, fill="#0F0A06", opacity=35, stroke=NONE)
# amber glow halo
d.shape("ellipse", "Eye glow L", x=335, y=460, width=170, height=170, fill="#F2B03D", opacity=16, stroke=NONE)
d.shape("ellipse", "Eye glow R", x=495, y=460, width=170, height=170, fill="#F2B03D", opacity=16, stroke=NONE)
# iris / pupil / glints
d.shape("ellipse", "Iris L", x=360, y=485, width=120, height=120, fill=IRIS_GRAD, stroke=INK, strokeWidth=5)
d.shape("ellipse", "Iris R", x=520, y=485, width=120, height=120, fill=IRIS_GRAD, stroke=INK, strokeWidth=5)
d.shape("ellipse", "Pupil L", x=390, y=515, width=60, height=60, fill="#140C08", stroke=NONE)
d.shape("ellipse", "Pupil R", x=550, y=515, width=60, height=60, fill="#140C08", stroke=NONE)
d.shape("ellipse", "Glint L", x=398, y=500, width=16, height=16, fill="#FFFFFF", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint L2", x=428, y=556, width=8, height=8, fill="#FFD98A", opacity=55, stroke=NONE)
d.shape("ellipse", "Glint R", x=558, y=500, width=16, height=16, fill="#FFFFFF", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R2", x=588, y=556, width=8, height=8, fill="#FFD98A", opacity=55, stroke=NONE)
# --- muzzle / nose / mouth -------------------------------------------------------------
d.shape("ellipse", "Muzzle", x=425, y=600, width=150, height=115, fill="#6B5240", opacity=55, stroke=NONE)
# under-eye crease lines
d.path("M380,618 C400,630 438,630 460,618", "Under-eye L", fill=NONE, stroke=INK, strokeWidth=4, opacity=45, cap="round")
d.path("M540,618 C562,630 600,630 620,618", "Under-eye R", fill=NONE, stroke=INK, strokeWidth=4, opacity=45, cap="round")
d.path("M482,642 C482,626 518,626 518,642 C518,660 508,670 500,670 "
       "C492,670 482,660 482,642 Z", "Nose", fill="#150D08", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Nostril L", x=487, y=648, width=10, height=8, fill="#000000", opacity=60, stroke=NONE)
d.shape("ellipse", "Nostril R", x=503, y=648, width=10, height=8, fill="#000000", opacity=60, stroke=NONE)
d.path("M500,670 L500,690", "Philtrum", fill=NONE, stroke=INK, strokeWidth=4, cap="round")
d.path("M470,700 C485,712 515,712 530,700", "Mouth", fill=NONE, stroke=INK, strokeWidth=6, cap="round")
# sparse whiskers
for i, dd in enumerate(["M470,660 C430,650 400,650 375,658", "M475,676 C435,672 405,678 385,688",
                        "M530,660 C570,650 600,650 625,658", "M525,676 C565,672 595,678 615,688"]):
    d.path(dd, f"Whisker {i+1}", fill=NONE, stroke="#8A705A", strokeWidth=3, opacity=50, cap="round")
# wiry cheek + beard strokes
for i, dd in enumerate(["M310,560 C296,576 287,592 282,606", "M318,612 C304,630 298,646 298,662",
                        "M342,692 C332,712 330,728 332,742", "M690,560 C704,576 713,592 718,606",
                        "M682,612 C696,630 702,646 702,662", "M658,692 C668,712 670,728 668,742",
                        "M462,742 C456,762 457,778 463,790", "M500,746 C498,764 500,780 505,792",
                        "M538,742 C544,762 543,778 537,790"]):
    d.path(dd, f"Fur stroke {i+1}", fill=NONE, stroke="#6B5340", strokeWidth=5, opacity=65, cap="round")

# --- raised hand: the famously long thin middle finger, silhouetted on the moon --------
d.shape("ellipse", "Palm", x=700, y=744, width=62, height=50, fill=HAND_GRAD, stroke=INK, strokeWidth=5)
# middle finger: long, thin, faintly S-curved, tip beside the cheek
d.path("M722,746 C716,700 711,650 710,608 C709,594 715,584 724,586 "
       "C732,588 733,600 732,614 C735,660 740,704 745,742 "
       "C747,754 726,760 722,746 Z",
       "Middle finger", fill=HAND_GRAD, stroke="#6B4E35", strokeWidth=3)
d.shape("ellipse", "Finger knuckle", x=703, y=634, width=16, height=12, fill="#3A2A1E", stroke=NONE)
# curled index and pinky
d.path("M704,762 C692,754 685,742 686,730 C687,722 697,720 701,728 "
       "C703,738 707,746 713,754 C718,762 711,770 704,762 Z",
       "Index curl", fill=HAND_GRAD, stroke=INK, strokeWidth=4)
d.path("M752,770 C762,762 767,752 767,740 C767,732 757,728 753,736 "
       "C751,746 747,754 741,760 C736,766 743,774 752,770 Z",
       "Pinky curl", fill=HAND_GRAD, stroke=INK, strokeWidth=4)
# bony rim light down the finger
d.path("M717,732 C713,694 709,652 709,612", "Finger rim", fill=NONE,
       stroke="#B98A4A", strokeWidth=3, opacity=40, cap="round")

# --- name -----------------------------------------------------------------------------
d.text("AYE-AYE", "Name", x=500, y=962, size=60, font="Virelai Sans",
       color="#C9CEDE", justify="center")

d.finish("aye-aye-V1R00")
