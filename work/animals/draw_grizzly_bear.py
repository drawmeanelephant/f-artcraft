#!/usr/bin/env python3
"""Grizzly bear — field-guide plate V1R00. Standing hip-deep in a glacial river
at the salmon run: the shoulder hump like a landslide, head lowered to the
water, a sockeye hanging in the air off its nose. Pale alder trunks on the far
bank, drizzle, rapids boiling round the legs. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Grizzly Bear — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420          # plate disc centre + radius
INK = "#180C04"

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def on_disc(x, y, pad=0):
    return math.hypot(x - CX, y - CY) <= R - pad

BG_GRAD = lin(0, 0, 0, 1000, (0, "#0C1614"), (1, "#030807"))
PLATE_GRAD = rad((0, "#C2CFC6"), (0.55, "#8AA39A"), (1, "#4C665C"))
WATER_GRAD = lin(0, 700, 0, 880, (0, "#5E8A84"), (1, "#223E38"))
FUR = lin(0, 380, 0, 730, (0, "#6B4A2E"), (0.5, "#463018"), (1, "#241206"))
FUR_DARK = "#241206"
MUZZLE_G = rad((0, "#8A6A44"), (1, "#543A20"))
FISH = lin(240, 540, 330, 610, (0, "#C8785E"), (0.5, "#A84C3A"), (1, "#6E2A20"))

# --- backdrop + river plate -----------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880, fill="#8AA39A", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#37504A", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E2EAE2", strokeWidth=3, opacity=40)
# drizzle — fine slant lines, temper like weather
for i, (x, y, ln) in enumerate([(240,180,34),(330,150,28),(430,120,30),(560,140,26),(660,180,32),
                                (760,240,26),(830,330,24),(200,300,26),(300,240,30),(700,320,26),
                                (840,420,22),(180,440,22),(520,180,24)]):
    assert on_disc(x, y, 20) and on_disc(x + 7, y + ln, 20), (x, y)
    d.path(f"M{x},{y} L{x+7},{y+ln}", f"Rain {i+1}",
           fill=NONE, stroke="#E4EEE8", strokeWidth=2, opacity=14, cap="round")

# --- the river: crest at y700, bottom closes on the disc arc --------------------
wy = 700
wdx = math.sqrt(R * R - (wy - CY) ** 2)
d.path(f"M{CX-wdx:.1f},{wy} C290,690 420,700 540,694 C650,689 720,698 {CX+wdx:.1f},{wy} "
       f"A{R},{R} 0 0 1 {CX-wdx:.1f},{wy} Z", "River", fill=WATER_GRAD, stroke=NONE)
d.path(f"M{CX-wdx+8:.1f},{wy-2} C290,688 420,696 540,690 C650,685 720,694 {CX+wdx-8:.1f},{wy-2}",
       "River light", fill=NONE, stroke="#C4DCD4", strokeWidth=4, opacity=40, cap="round")
# current streaks on the water
for i, (dd) in enumerate(["M180,748 C280,742 380,742 460,748",
                          "M560,756 C640,750 720,750 780,756",
                          "M240,796 C340,790 440,790 520,796",
                          "M580,808 C660,802 730,802 790,808",
                          "M300,840 C400,834 500,834 580,840"]):
    d.path(dd, f"Current {i+1}", fill=NONE, stroke="#8FB8B0", strokeWidth=5, opacity=30, cap="round")
# wet boulders breaking the surface
d.path("M214,714 C214,698 226,686 244,684 C262,682 278,692 280,708 "
       "C282,722 272,732 254,734 C234,736 216,728 214,714 Z",
       "Boulder L", fill=rad((0, "#5A5E52"), (1, "#2E322A")), stroke=INK, strokeWidth=3)
d.path("M762,730 C762,716 774,706 790,706 C806,706 816,716 816,730 "
       "C816,742 806,750 790,750 C774,750 764,742 762,730 Z",
       "Boulder R", fill=rad((0, "#4E564C"), (1, "#262C24")), stroke=INK, strokeWidth=3)
# foam collars round the boulders
for i, (x, y, w) in enumerate([(247,736,76),(791,752,62)]):
    d.path(f"M{x-w/2},{y} C{x-w/4},{y-8} {x+w/4},{y-8} {x+w/2},{y}",
           f"Foam {i+1}", fill=NONE, stroke="#E8F2EE", strokeWidth=5, opacity=55, cap="round")

# far bank: a dark scrub-and-treeline band above the water so the alders grow
# from land, not out of the river
d.path("M150,704 C170,680 190,660 216,652 C240,644 266,650 286,662 "
       "C310,640 340,628 372,630 C404,632 430,644 450,660 "
       "C480,646 516,640 552,644 C590,648 620,660 642,674 "
       "C676,660 716,656 750,664 C786,672 816,688 838,704 L838,708 L150,708 Z",
       "Far bank", fill="#3E5248", opacity=75, stroke=NONE)
# two conifer spires rising over the bank
d.path("M340,640 L356,548 L372,640 Z", "Spire L", fill="#2E4038", opacity=70, stroke=NONE)
d.path("M318,640 L330,576 L342,640 Z", "Spire L2", fill="#2E4038", opacity=55, stroke=NONE)
d.path("M752,660 L766,556 L782,660 Z", "Spire R", fill="#2E4038", opacity=70, stroke=NONE)

# --- alders on the far bank: pale trunks, small leaf clusters -------------------
def alder(x, base, top, lean, w, label):
    d.path(f"M{x},{base} C{x+lean*0.4},{base-70} {x+lean*0.7},{top+60} {x+lean},{top}",
           label, fill=NONE, stroke="#B6BAAC", strokeWidth=w, cap="round")
    d.path(f"M{x+1},{base} C{x+lean*0.4+1},{base-70} {x+lean*0.7+1},{top+60} {x+lean+1},{top}",
           f"{label} shade", fill=NONE, stroke="#6E7466", strokeWidth=w*0.4, opacity=60, cap="round")

alder(238, 706, 480, -14, 9, "Alder L1")
alder(272, 710, 520, 8, 7, "Alder L2")
alder(790, 702, 470, 16, 9, "Alder R1")
alder(822, 706, 530, -6, 6, "Alder R2")
# leaf dabs clustered at the tops
for i, (x, y, w) in enumerate([(212,478,26),(236,452,32),(254,488,22),(272,516,24),(288,540,20),
                               (216,512,18),(796,466,30),(820,490,24),(800,516,20),(836,522,18),
                               (776,494,20)]):
    assert on_disc(x, y, 16), (x, y)
    d.shape("ellipse", f"Alder leaf {i+1}", x=x, y=y, width=w, height=w*0.62,
            fill="#4E6A40", opacity=85, stroke=NONE)

# --- the leaping sockeye: hung in the air off the bear's nose -------------------
d.path("M238,556 C256,544 280,540 298,546 C312,551 322,562 326,574 "
       "L340,566 L336,584 L350,580 L344,596 "
       "C330,604 312,608 294,604 C274,600 256,590 244,576 "
       "C238,568 236,562 238,556 Z",
       "Sockeye", fill=FISH, stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Fish eye", x=246, y=556, width=7, height=7, fill="#140A06", stroke=NONE)
d.path("M256,550 C258,558 258,566 254,572", "Gill", fill=NONE,
       stroke="#5E2018", strokeWidth=3, cap="round")
d.path("M282,560 C292,556 302,556 310,560", "Back line", fill=NONE,
       stroke="#5E2018", strokeWidth=2.5, opacity=60, cap="round")
# droplets flung off the leap
for i, (x, y, w) in enumerate([(300,540,5),(318,614,6),(286,620,4),(332,556,4)]):
    assert on_disc(x, y, 14), (x, y)
    d.shape("ellipse", f"Drop {i+1}", x=x, y=y, width=w, height=w*1.3,
            fill="#E4F0EC", opacity=70, stroke=NONE)

# --- grizzly: full body profile, nose left, standing in the river ---------------
# ears first — small round ears, bases buried in the crown
d.path("M442,446 C442,432 452,422 466,422 C480,422 490,432 490,446 "
       "C490,458 480,466 466,466 C452,466 442,458 442,446 Z",
       "Ear near", fill=FUR, stroke=INK, strokeWidth=4)
d.path("M476,436 C476,424 484,416 496,416 C508,416 516,424 516,436 "
       "C516,446 508,454 496,454 C484,454 476,446 476,436 Z",
       "Ear far", fill=FUR_DARK, stroke=INK, strokeWidth=3.5)

# one silhouette: nose → long muzzle → dished face → crown → neck → THE HUMP →
# back → rump → legs cut by the waterline → chest → throat → jaw → close
SILH = ("M296,548 C306,530 322,516 344,508 C358,502 370,494 378,482 "
        "C386,468 396,458 408,452 C420,446 434,444 448,446 "
        "C468,436 490,428 512,420 C540,402 574,394 608,400 "
        "C646,408 678,426 702,452 C724,476 738,506 744,538 "
        "C748,574 744,612 734,646 C730,670 726,694 724,716 L710,716 "
        "C704,694 702,674 700,654 L658,668 "
        "C618,676 574,676 538,670 L490,662 "
        "C486,682 484,700 484,718 L452,718 "
        "C446,698 444,676 446,656 C430,640 412,620 398,602 "
        "C380,592 364,582 350,574 C330,566 312,558 296,548 Z")
d.path(SILH, "Grizzly", fill=FUR, stroke=INK, strokeWidth=6)

# open jaw hint: the mouth line + a shadowed gape, head lowered to the water
d.path("M302,556 C316,564 332,570 348,574 C362,578 376,582 388,586",
       "Mouth", fill=NONE, stroke=INK, strokeWidth=4.5, cap="round")
d.path("M304,558 C314,566 326,572 338,576 C328,578 316,576 310,568 Z",
       "Mouth gape", fill="#0E0602", opacity=85, stroke=NONE)
# nose leather
d.path("M282,544 C280,534 286,526 296,524 C306,522 315,528 316,538 "
       "C317,548 310,556 300,556 C290,556 284,552 282,544 Z",
       "Nose", fill=rad((0, "#3E3028"), (1, "#120905")), stroke=INK, strokeWidth=3)
# dished-face shading + paler muzzle
d.path("M298,546 C310,530 328,518 350,512 C364,508 376,500 384,490 "
       "C376,508 362,522 346,532 C330,540 312,546 298,548 Z",
       "Muzzle", fill=MUZZLE_G, opacity=70, stroke=NONE)
# neck ruff — fur break between the head and the landslide
for i, dd in enumerate(["M438,470 C452,486 462,508 466,532",
                        "M456,462 C472,478 484,502 490,528",
                        "M428,478 C438,494 446,514 450,536"]):
    d.path(dd, f"Ruff {i+1}", fill=NONE, stroke="#2A180A", strokeWidth=5, opacity=50, cap="round")

# the eye: small, deep-set, weather-dark
d.path("M368,508 C378,498 396,496 408,504 C398,516 380,518 368,508 Z",
       "Eye", fill=rad((0, "#8A622E"), (0.6, "#543418"), (1, "#2A180A")),
       stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Pupil", x=386, y=502, width=8, height=10, fill="#0E0A04", stroke=NONE)
d.shape("ellipse", "Glint", x=388, y=504, width=4, height=4, fill="#FFFFFF", opacity=85, stroke=NONE)
d.path("M364,504 C376,492 398,490 412,500", "Brow",
       fill=NONE, stroke=INK, strokeWidth=5, cap="round")

# hump shading: dark under the crest, grizzled tips catching light on top
d.path("M516,424 C546,408 578,402 608,408 C646,416 676,436 698,464 "
       "C676,444 646,432 610,430 C576,428 544,432 520,442 Z",
       "Hump shade", fill=FUR_DARK, opacity=60, stroke=NONE)
for i, dd in enumerate(["M470,428 C500,414 536,406 570,404",
                        "M490,446 C524,434 562,428 596,428",
                        "M520,420 C548,410 578,406 606,408"]):
    d.path(dd, f"Grizzle {i+1}", fill=NONE, stroke="#C8AE8A", strokeWidth=4, opacity=35, cap="round")
# fur texture down the flank and legs
for i, dd in enumerate(["M560,470 C576,510 586,556 588,604",
                        "M620,480 C636,522 644,570 644,616",
                        "M680,510 C692,548 696,590 692,630",
                        "M452,660 C456,680 456,700 452,716",
                        "M712,648 C716,670 716,694 712,714"]):
    d.path(dd, f"Flank fur {i+1}", fill=NONE, stroke="#180C04", strokeWidth=4, opacity=40, cap="round")
# belly shag
d.path("M490,658 C540,668 600,672 654,664 C608,680 544,682 500,674 Z",
       "Belly shag", fill=FUR_DARK, opacity=50, stroke=NONE)

# rapids boiling round the legs — foam arcs over the waterline
for i, (x, y, w) in enumerate([(430,724,110),(470,730,150),(560,726,180),(700,720,150)]):
    d.path(f"M{x-w/2},{y} C{x-w/4},{y-8} {x+w/4},{y-8} {x+w/2},{y}",
           f"Rapid {i+1}", fill=NONE, stroke="#E8F2EE", strokeWidth=5, opacity=50, cap="round")
d.path("M420,718 C490,730 590,732 700,722", "Leg shadow",
       fill=NONE, stroke="#14201C", strokeWidth=10, opacity=40, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#0A1412", strokeWidth=6)

# --- name ----------------------------------------------------------------------
d.text("GRIZZLY BEAR", "Name", x=500, y=962, size=54, font="Virelai Sans",
       color="#DEE8E0", justify="center")

d.finish("grizzly-bear-V1R00")
