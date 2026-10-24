#!/usr/bin/env python3
"""Strutter Crashley — mascot portrait V1R00. Framework Nostalgist:
a proud, quietly buckling legacy framework in a faded corporate-blue
blazer, action-mapping sash, brittle lapel pins, cracked monocle, and
an XML config fan folded as a pocket square. Broken but proud.
Warm archive-stone plate on a sepia-night backdrop. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Digits (2009) in Source Sans 3. Plate = circle (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Strutter Crashley — Mascot Plate", 1000, 1000)

INK = "#2A2016"   # warm dark ink, never black
BG_GRAD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000], "stops": [
    {"offset": 0, "color": "#16110C"}, {"offset": 1, "color": "#0A0705"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#6E665C"}, {"offset": 0.62, "color": "#453F36"},
    {"offset": 1, "color": "#1E1A15"}]}}
BLAZER_GRAD = {"gradient": {"kind": "linear", "start": [0, 420], "end": [0, 770], "stops": [
    {"offset": 0, "color": "#5E7FAE"}, {"offset": 0.55, "color": "#41598A"},
    {"offset": 1, "color": "#2A3A5E"}]}}
SASH_GRAD = {"gradient": {"kind": "linear", "start": [560, 430], "end": [430, 700], "stops": [
    {"offset": 0, "color": "#8AA2C4"}, {"offset": 1, "color": "#5E76A0"}]}}
SKIN_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E6CCA8"}, {"offset": 0.75, "color": "#C9A888"},
    {"offset": 1, "color": "#A8846A"}]}}
SHIRT_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E8E2D0"}, {"offset": 1, "color": "#C4BCA4"}]}}
GOLD = "#C8A85A"
FAN_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F0E8CE"}, {"offset": 1, "color": "#C9B992"}]}}

PCX, PCY, PR = 500, 460, 420

def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#8A7E6A", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#14100C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D4C8AE", strokeWidth=3, opacity=26)
# archive patina + flecks
d.shape("ellipse", "Patina 1", x=195, y=335, width=235, height=150,
        fill="#57504A", opacity=22, stroke=NONE)
d.shape("ellipse", "Patina 2", x=615, y=575, width=235, height=140,
        fill="#2E2823", opacity=32, stroke=NONE)
for i, (x, y, w) in enumerate([(218,348,5),(792,342,6),(182,548,5),(850,568,5),
                               (262,762,5),(732,768,6),(160,452,5),(852,632,5),
                               (432,128,5),(598,140,6),(340,162,4),(702,202,5),
                               (252,652,4),(658,722,5)]):
    assert on_disc(x, y, 12), (x, y)
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#E0D4BC", opacity=30, stroke=NONE)
# ghost arcs on the dark backdrop
d.path("M930,158 A105,105 0 0 0 848,64", "Ghost arc TR",
       fill=NONE, stroke="#7A6A4E", strokeWidth=14, opacity=10, cap="round")
d.path("M78,778 A118,118 0 0 0 186,880", "Ghost arc BL",
       fill=NONE, stroke="#7A6A4E", strokeWidth=10, opacity=8, cap="round")

# --- faded corporate ghosts on the plate -----------------------------------------
# giant angle brackets, retired but still framing things
d.text("<", "Ghost angle L", x=235, y=330, size=120, font="Source Sans 3",
       color="#8A8272", justify="center")
d.text(">", "Ghost angle R", x=765, y=345, size=120, font="Source Sans 3",
       color="#8A8272", justify="center")
# the arrow: rises confidently, droops at the end — the mapping failed
d.path("M255,640 C360,560 430,470 480,400", "Chart arrow rise",
       fill=NONE, stroke=GOLD, strokeWidth=5, opacity=22, cap="round",
       dash=[10, 8])
d.path("M480,400 C540,430 590,470 630,530", "Chart arrow sag",
       fill=NONE, stroke=GOLD, strokeWidth=5, opacity=18, cap="round",
       dash=[10, 8])
d.path("M630,530 L614,508 M630,530 L652,518", "Arrow head",
       fill=NONE, stroke=GOLD, strokeWidth=5, opacity=18, cap="round")
# a hairline crack through the plate, lower right — the collapse, decorative
d.path("M760,700 L736,724 L752,744 L720,772 L734,796", "Plate crack",
       fill=NONE, stroke="#0E0B08", strokeWidth=3, opacity=55, cap="round")
for x, y in [(760, 700), (734, 796)]:
    assert on_disc(x, y, 4), (x, y)

# --- the man himself -------------------------------------------------------------
# left arm (viewer's left) hanging dignified
d.path("M392,480 C360,540 350,620 356,690 C366,704 384,704 394,692 "
       "C390,622 398,556 414,500 Z",
       "Arm L", fill=BLAZER_GRAD, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Hand L", x=350, y=688, width=30, height=26,
        fill=SKIN_GRAD, stroke=INK, strokeWidth=3)
# torso: blazer bell
d.path("M500,432 C560,432 606,470 624,540 C638,600 646,680 640,748 "
       "C590,774 410,774 362,748 C356,680 364,600 378,540 "
       "C396,470 440,432 500,432 Z",
       "Blazer", fill=BLAZER_GRAD, stroke=INK, strokeWidth=5)
# blazer shade + worn sheen on the shoulder
d.path("M580,470 C612,530 632,640 628,740 C608,752 584,760 560,764 "
       "C588,690 594,560 580,470 Z",
       "Blazer shade", fill="#16224A", opacity=42, stroke=NONE)
d.path("M400,470 C390,500 384,540 382,580 C396,550 406,510 420,484 Z",
       "Shoulder wear", fill="#8AA2C4", opacity=30, stroke=NONE)
# shirt V + a tie that gave up
d.path("M470,440 L530,440 L500,540 Z", "Shirt V",
       fill=SHIRT_GRAD, stroke=INK, strokeWidth=3)
d.path("M500,452 L512,470 L500,528 L488,470 Z", "Tie",
       fill="#6E4A3A", stroke=INK, strokeWidth=2.5)
# lapels
d.path("M468,440 C440,470 424,510 420,556 C444,540 462,512 472,478 Z",
       "Lapel L", fill="#33477A", stroke=INK, strokeWidth=3.5)
d.path("M532,440 C560,470 576,510 580,556 C556,540 538,512 528,478 Z",
       "Lapel R", fill="#33477A", stroke=INK, strokeWidth=3.5)
# buttons: one hangs by a thread
d.shape("ellipse", "Button 1", x=497, y=600, width=12, height=12,
        fill=GOLD, stroke=INK, strokeWidth=2)
d.path("M503,640 L505,652", "Button thread",
       fill=NONE, stroke="#8A8272", strokeWidth=1.5, opacity=80)
d.shape("ellipse", "Button 2", x=498, y=652, width=11, height=11,
        fill=GOLD, stroke=INK, strokeWidth=2, opacity=85)

# the crack across his shoulder — he buckles from heritage
d.path("M398,505 L420,522 L408,540 L432,556 L422,574", "Shoulder crack",
       fill=NONE, stroke="#14100C", strokeWidth=3.5, opacity=70,
       cap="round")

# --- the action-mapping sash: right shoulder to left hip ----------------------------
d.path("M548,436 L596,464 L452,742 L408,716 Z", "Sash",
       fill=SASH_GRAD, stroke=INK, strokeWidth=3.5)
d.path("M556,444 L588,464 M596,464 L452,742 M548,436 L408,716 "
       "M452,742 L416,722",
       "Sash edge gold", fill=NONE, stroke=GOLD, strokeWidth=2, opacity=60)
# frayed sash hem
d.path("M408,716 L452,742 L444,754 L428,742 L420,752 L412,730 Z",
       "Sash fray", fill="#5E76A0", stroke=INK, strokeWidth=2.5)
# sash lettering, rotated to march with the band
r = d.text("ACTION MAPPING", "Sash text", x=502, y=592, size=19,
           font="Source Sans 3", color="#2E3E5E", justify="center")
if r and r.get("id"):
    d.cmd("object.rotate", "sash text tilt", ids=[r["id"]], angle=-64,
          origin=[502, 590])

# --- brittle lapel pins, viewer-left lapel ------------------------------------------
# star pin, intact but dim
d.path("M442,486 L447,496 L458,497 L449,504 L452,515 L442,509 L432,515 "
       "L435,504 L426,497 L437,496 Z",
       "Star pin", fill=GOLD, stroke=INK, strokeWidth=2)
# round pin, cracked straight through
d.path("M442,534 A13,13 0 1 1 441,534 Z", "Pin disc",
       fill="#8A96AC", stroke=INK, strokeWidth=2.5)
d.path("M434,524 L446,532 L438,540 L450,546", "Pin crack",
       fill=NONE, stroke="#14100C", strokeWidth=2.5, cap="round")
# little '2009' service pin — digits need Source Sans 3
d.shape("rectangle", "Service pin", x=424, y=556, width=42, height=18,
        radius=3, fill="#B8A86E", stroke=INK, strokeWidth=2)
d.path("M424,556 L432,556 L430,564 L424,562 Z", "Pin chip",
       fill="#1E1A15", stroke=NONE)
d.text("2009", "Service pin text", x=447, y=570, size=12,
       font="Source Sans 3", color="#3A3222", justify="center")

# --- the pocket square: an XML config fan -------------------------------------------
# jacket pocket
d.path("M556,620 L628,612 L626,646 L558,652 Z", "Pocket",
       fill="#33477A", stroke=INK, strokeWidth=3)
# three folded config leaves fanning out of the pocket
d.path("M566,616 L588,566 L600,614 Z", "Fan leaf 1",
       fill=FAN_GRAD, stroke=INK, strokeWidth=2.5)
d.path("M588,614 L616,556 L622,608 Z", "Fan leaf 2",
       fill=FAN_GRAD, stroke=INK, strokeWidth=2.5)
d.path("M604,612 L636,568 L636,610 Z", "Fan leaf 3",
       fill=FAN_GRAD, stroke=INK, strokeWidth=2.5)
# tiny config scribbles on the leaves
d.path("M580,600 L590,584 M596,600 L608,582 M612,606 L624,592",
       "Fan scribbles", fill=NONE, stroke="#8A7A56", strokeWidth=2,
       opacity=60, cap="round")
d.text("</>", "Fan glyph", x=600, y=604, size=11, font="Source Sans 3",
       color="#6A5A3C", justify="center")

# --- right arm akimbo: hand on hip, elbow out ----------------------------------------
d.path("M620,530 C668,540 700,580 706,632 C712,668 700,700 676,716 "
       "C664,710 658,696 664,684 C678,668 682,644 676,620 "
       "C668,588 648,566 620,556 Z",
       "Arm R akimbo", fill=BLAZER_GRAD, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Hand R", x=656, y=676, width=32, height=28,
        fill=SKIN_GRAD, stroke=INK, strokeWidth=3)

# --- the head: chin up, heritage intact ----------------------------------------------
d.path("M500,278 C548,278 580,312 580,362 C580,412 546,446 500,446 "
       "C454,446 420,412 420,362 C420,312 452,278 500,278 Z",
       "Head", fill=SKIN_GRAD, stroke=INK, strokeWidth=4.5)
# comb-over: three proud streaks
d.path("M430,330 C450,300 480,288 512,290 M438,318 C460,296 492,286 522,292",
       "Comb-over", fill=NONE, stroke="#5E4A34", strokeWidth=4,
       cap="round", opacity=85)
# raised chin shade + cheek light
d.path("M448,404 C470,424 530,424 552,404 C544,432 524,444 500,444 "
       "C476,444 456,432 448,404 Z",
       "Chin shade", fill="#9A7A5C", opacity=35, stroke=NONE)
d.shape("ellipse", "Cheek light", x=440, y=330, width=52, height=40,
        fill="#F0DCBC", opacity=35, stroke=NONE)
# smug closed eyes, mid-speech about separation of concerns
d.path("M444,352 C454,344 468,344 478,352", "Eye L",
       fill=NONE, stroke=INK, strokeWidth=4, cap="round")
d.path("M522,352 C532,344 546,344 556,352", "Eye R",
       fill=NONE, stroke=INK, strokeWidth=4, cap="round")
# one eyebrow still making a point
d.path("M436,334 C448,326 464,326 476,332", "Brow L",
       fill=NONE, stroke=INK, strokeWidth=3.5, cap="round")
d.path("M524,330 C538,322 554,322 566,330", "Brow R",
       fill=NONE, stroke=INK, strokeWidth=3.5, cap="round")
# the dignified nose + small knowing smile
d.path("M498,360 C496,372 494,380 490,388 C496,392 504,392 510,388",
       "Nose", fill=NONE, stroke=INK, strokeWidth=3, cap="round")
d.path("M472,408 C486,418 514,418 528,406", "Smile",
       fill=NONE, stroke=INK, strokeWidth=3.5, cap="round")

# --- the cracked monocle, on its chain -----------------------------------------------
d.shape("ellipse", "Monocle rim", x=516, y=338, width=52, height=52,
        fill=NONE, stroke=GOLD, strokeWidth=4)
d.shape("ellipse", "Monocle glass", x=520, y=342, width=44, height=44,
        fill="#C4D4E0", opacity=18, stroke=NONE)
d.path("M526,346 L542,360 L534,372", "Monocle crack",
       fill=NONE, stroke="#3A3630", strokeWidth=2.5, cap="round")
# chain: three drooping links to the lapel
d.path("M566,378 C576,410 576,446 566,476", "Monocle chain",
       fill=NONE, stroke=GOLD, strokeWidth=2.5, dash=[4, 4],
       cap="round")

# --- name + role ----------------------------------------------------------------------
d.text("STRUTTER CRASHLEY", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#EBE2CC", justify="center")
r = d.text("FRAMEWORK NOSTALGIST", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#B8AA88", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("045.strutter-crashley-V1R00")
