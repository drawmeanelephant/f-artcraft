#!/usr/bin/env python3
"""Takin — field-guide plate V1R00. Budorcas: a cattle-goat committee wearing
one shaggy body — massive arched Roman nose, gnu-like horns sweeping out
then up off the poll, guard hair falling in a ragged skirt over spindly
dark legs, head lowered mid-snort. Amber coat on a mossy ledge, mountain
mist drifting through the plate. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Takin — Field Plate", 1000, 1000)
rng = random.Random(17)

INK = "#2E2013"   # deep umber, not black
BG_GRAD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000], "stops": [
    {"offset": 0, "color": "#0D1712"}, {"offset": 1, "color": "#030705"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#CBDCCA"}, {"offset": 0.62, "color": "#8FA894"},
    {"offset": 1, "color": "#546A58"}]}}
MOSS_GRAD = {"gradient": {"kind": "linear", "start": [0, 750], "end": [0, 880], "stops": [
    {"offset": 0, "color": "#8A9668"}, {"offset": 1, "color": "#3E4A30"}]}}
FUR_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#D9A85C"}, {"offset": 0.58, "color": "#A8763A"},
    {"offset": 1, "color": "#6E4820"}]}}
SADDLE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#EAC98E"}, {"offset": 1, "color": "#BE9252"}]}}
HORN_GRAD = {"gradient": {"kind": "linear", "start": [0, 400], "end": [0, 560], "stops": [
    {"offset": 0, "color": "#8A7350"}, {"offset": 1, "color": "#40301C"}]}}
BOSS_GRAD = {"gradient": {"kind": "linear", "start": [0, 395], "end": [0, 455], "stops": [
    {"offset": 0, "color": "#C9AE7E"}, {"offset": 1, "color": "#8E744C"}]}}
MUZZLE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#B08A58"}, {"offset": 1, "color": "#6E4E2C"}]}}
LEG_GRAD = {"gradient": {"kind": "linear", "start": [0, 700], "end": [0, 780], "stops": [
    {"offset": 0, "color": "#4A3624"}, {"offset": 1, "color": "#241A10"}]}}
ROCK_GRAD = {"gradient": {"kind": "linear", "start": [0, 720], "end": [0, 800], "stops": [
    {"offset": 0, "color": "#8E9478"}, {"offset": 1, "color": "#4C5238"}]}}

PCX, PCY, PR = 500, 460, 420

def on_disc(x, y, pad):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

# --- backdrop + plate --------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#92AC90", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#3E5646", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#EAF2E4", strokeWidth=3, opacity=50)
# mountain mist: broad soft bands drifting across the upper plate
for i, dd in enumerate(["M150,205 C350,178 560,188 790,215",
                        "M110,315 C320,290 580,296 830,325",
                        "M170,420 C380,398 620,404 800,428"]):
    d.path(dd, f"Mist band {i+1}", fill=NONE, stroke="#F0F6EC",
           strokeWidth=34, opacity=9, cap="round")
for i, dd in enumerate(["M180,250 C360,228 560,236 730,258",
                        "M220,368 C400,348 600,352 770,372"]):
    d.path(dd, f"Mist line {i+1}", fill=NONE, stroke="#F0F6EC",
           strokeWidth=6, opacity=24, cap="round")
# drifting motes behind the animal
for i, (x, y, w) in enumerate([(210,300,7),(770,250,6),(165,470,8),(830,430,7),(255,150,6),
                               (720,150,7),(400,120,6),(600,115,7),(145,580,6),(855,560,6),
                               (330,200,5),(680,220,5)]):
    assert on_disc(x + w / 2, y + w / 2, 8), (x, y)
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#F4F9F0", opacity=50, stroke=NONE)

# --- mossy ledge: top edge wavy, closing on the disc's own arc ------------------------
d.path("M219,772 C360,754 640,754 781,772 A420,420 0 0 1 219,772 Z",
       "Moss ledge", fill=MOSS_GRAD, stroke="#5A6A44", strokeWidth=4)
d.path("M250,780 C390,766 610,766 750,780", "Ledge shade", fill=NONE,
       stroke="#5E6E48", strokeWidth=5, opacity=40, cap="round")
# moss tufts + lichen dots on the ledge
for i, (x, y, w) in enumerate([(260,780,10),(330,788,8),(430,784,9),(540,780,8),(650,786,9),
                               (720,782,8),(480,792,7),(600,794,7)]):
    d.shape("ellipse", f"Moss tuft {i+1}", x=x, y=y, width=w, height=round(w*0.55),
            fill="#A4B276", opacity=55, stroke=NONE)
# two mossy boulders anchoring the ledge ends
for i, (x, y, w, h) in enumerate([(238,724,64,48),(700,742,56,42)]):
    assert on_disc(x + w / 2, y + h / 2, 16), (x, y)
    d.shape("ellipse", f"Boulder {i+1}", x=x, y=y, width=w, height=h,
            fill=ROCK_GRAD, stroke="#3E442E", strokeWidth=3)
for i, (x, y, w) in enumerate([(252,736,9),(278,748,7),(712,752,8),(732,762,6)]):
    d.shape("ellipse", f"Lichen {i+1}", x=x, y=y, width=w, height=w,
            fill="#C4D08E", opacity=60, stroke=NONE)

# --- spindly legs under the skirt (roots hidden by the hem) ----------------------------
for i, (x0, w0, x1) in enumerate([(424, 26, 420), (505, 24, 508), (636, 26, 644), (686, 22, 692)]):
    d.path(f"M{x0-w0//2},700 L{x0+w0//2},700 L{x1+w0//4},768 L{x1-w0//4},768 Z",
           f"Leg {i+1}", fill=LEG_GRAD, stroke=INK, strokeWidth=4)
    d.shape("ellipse", f"Hoof {i+1}", x=x1-13, y=762, width=26, height=14,
            fill="#1A120A", stroke=INK, strokeWidth=3)
# leg joint hint
for i, x in enumerate([422, 508, 642]):
    d.path(f"M{x-8},738 L{x+8},738", f"Leg joint {i+1}", fill=NONE,
           stroke="#17100A", strokeWidth=4, opacity=50, cap="round")

# --- body mass with ragged guard-hair hem ---------------------------------------------
BODY = ("M322,560 "
        "C314,518 326,476 352,450 "        # face front rising to the poll
        "C384,422 438,406 502,402 "        # crown into the shoulder hump
        "C566,390 646,402 688,444 "        # hump top
        "C720,480 730,538 724,592 "        # rump rounding down
        "C720,646 710,686 696,712 "        # rear hem edge
        "L680,704 L672,722 L656,702 L644,726 L628,706 L616,730 "
        "L598,710 L586,732 L568,712 L554,734 L536,714 L522,734 "
        "L506,714 L492,736 L474,716 L462,734 L446,716 L434,730 "
        "L420,714 L408,726 L396,710 "      # ragged hair hem
        "C382,698 376,678 380,656 "        # chest front
        "C362,638 348,608 344,584 "        # jaw underside
        "C332,576 324,568 322,560 Z")      # chin back up to the nose
d.path(BODY, "Body", fill=FUR_GRAD, stroke=INK, strokeWidth=7)

# pale golden saddle across the mid-back
d.path("M462,418 C530,396 620,404 668,444 C646,470 560,478 500,462 "
       "C476,452 462,436 462,418 Z",
       "Saddle", fill=SADDLE_GRAD, opacity=50, stroke=NONE)
# frost of pale guard hair along the top line
for i, dd in enumerate(["M452,406 C510,390 600,392 660,414",
                        "M420,416 C455,402 510,396 555,400"]):
    d.path(dd, f"Back light {i+1}", fill=NONE, stroke="#F0DCA8",
           strokeWidth=7, opacity=35, cap="round")

# long guard-hair strands falling from mid-body to the hem
for i in range(26):
    x = 400 + i * 11.5 + rng.uniform(-3, 3)
    y0 = rng.uniform(510, 570)
    y1 = rng.uniform(680, 730)
    col = rng.choice(["#3A2812", "#3A2812", "#8A6434", "#C89A58"])
    d.path(f"M{x:.0f},{y0:.0f} C{x+rng.uniform(-6,6):.0f},{(y0+y1)/2:.0f} "
           f"{x+rng.uniform(-8,8):.0f},{y1-30:.0f} {x+rng.uniform(-6,6):.0f},{y1:.0f}",
           f"Hair strand {i+1}", fill=NONE, stroke=col,
           strokeWidth=3, opacity=rng.randint(30, 50), cap="round")
# flank shadow + chest light
d.shape("ellipse", "Flank shade", x=560, y=520, width=160, height=180,
        fill="#201408", opacity=22, stroke=NONE)
d.shape("ellipse", "Chest light", x=380, y=470, width=110, height=120,
        fill="#D9B070", opacity=20, stroke=NONE)

# --- horns: gnu-style — out from the poll, droop, then kick up -------------------------
# low boss ridge across the poll where the horns meet
d.path("M360,428 C384,406 452,396 498,406 C508,412 510,424 504,434 "
       "C455,420 398,426 370,446 C362,441 358,435 360,428 Z",
       "Horn boss", fill=BOSS_GRAD, stroke=INK, strokeWidth=4)
d.path("M372,420 C406,404 462,398 494,408", "Boss light", fill=NONE,
       stroke="#F0DCA8", strokeWidth=4, opacity=45, cap="round")
# far horn: hooks up and out right of the poll
d.path("M488,412 C520,412 548,426 560,450 C569,468 565,486 552,492 "
       "C558,476 554,458 541,443 C528,428 509,419 488,415 Z",
       "Horn far", fill="#6E5638", stroke=INK, strokeWidth=4)
d.path("M552,484 C558,468 555,450 545,436", "Horn far tip", fill=NONE,
       stroke="#C9B285", strokeWidth=4, opacity=50, cap="round")

# --- ear tucked below the boss -----------------------------------------------------------
d.path("M506,448 C526,442 542,450 546,464 C534,476 514,473 506,462 Z",
       "Ear", fill="#5A4026", stroke=INK, strokeWidth=3)

# --- face: the great arched nose, one continuous bulbous profile ---------------------------
d.path("M330,468 C348,450 384,444 408,460 C432,478 442,512 432,542 "
       "C420,570 380,582 346,568 C318,556 298,530 300,502 "
       "C302,486 314,476 330,468 Z",
       "Muzzle", fill=MUZZLE_GRAD, stroke=INK, strokeWidth=5)
# shading that sells the convex Roman bridge
d.shape("ellipse", "Bridge shade", x=302, y=478, width=50, height=70,
        fill="#7A5830", opacity=35, stroke=NONE)
d.shape("ellipse", "Bridge light", x=326, y=462, width=44, height=26,
        fill="#D2AC72", opacity=45, stroke=NONE)
d.shape("ellipse", "Nostril near", x=310, y=538, width=24, height=16,
        fill="#1A1208", stroke=NONE)
d.shape("ellipse", "Nostril far", x=360, y=532, width=18, height=12,
        fill="#1A1208", opacity=80, stroke=NONE)
d.path("M322,566 C344,578 376,578 398,564", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
d.shape("ellipse", "Muzzle light", x=356, y=476, width=52, height=22,
        fill="#D2AC72", opacity=45, stroke=NONE)
# eye under the horn overhang
d.shape("ellipse", "Eye socket", x=402, y=452, width=42, height=40,
        fill="#2A1C0E", opacity=60, stroke=NONE)
d.shape("ellipse", "Eye", x=410, y=459, width=24, height=23, fill="#120C06",
        stroke=NONE)
d.shape("ellipse", "Eye glint", x=415, y=464, width=7, height=7,
        fill="#FFFFFF", opacity=80, stroke=NONE)
# near horn, nearest the viewer: a heavy crescent crossing the face plane,
# sweeping left-down off the poll with the tip kicking back up
d.path("M390,436 C350,446 318,470 304,502 C294,524 296,548 310,560 "
       "C318,567 332,564 338,553 C328,543 326,521 337,498 "
       "C350,472 372,451 394,444 Z",
       "Horn near", fill=HORN_GRAD, stroke=INK, strokeWidth=5)
d.path("M310,548 C300,528 303,505 317,484", "Horn near tip", fill=NONE,
       stroke="#D8C49A", strokeWidth=5, opacity=60, cap="round")
# horn ridges on the descending arm
for i, dd in enumerate(["M352,454 C345,464 340,474 337,484",
                        "M336,474 C330,484 325,494 323,504",
                        "M324,496 C318,506 315,517 314,527"]):
    d.path(dd, f"Horn ridge {i+1}", fill=NONE, stroke="#2A1E10",
           strokeWidth=3, opacity=45, cap="round")
# shaggy forelock spilling over the boss
for i, dd in enumerate(["M396,430 C392,450 394,468 402,484",
                        "M428,424 C426,446 430,464 438,478",
                        "M460,420 C460,440 466,458 474,470"]):
    d.path(dd, f"Forelock {i+1}", fill=NONE, stroke="#4A3418",
           strokeWidth=6, opacity=55, cap="round")
# chin beard wisps
for i, dd in enumerate(["M352,576 C350,590 352,602 358,612",
                        "M370,578 C370,592 374,604 380,612",
                        "M336,570 C332,582 332,594 338,604"]):
    d.path(dd, f"Beard wisp {i+1}", fill=NONE, stroke="#5A4024",
           strokeWidth=4, opacity=55, cap="round")

# --- snorted breath, warm against the cold mist ------------------------------------------
d.shape("ellipse", "Snort 1", x=268, y=548, width=64, height=40,
        fill="#F4EFE0", opacity=24, stroke=NONE)
d.shape("ellipse", "Snort 2", x=236, y=572, width=82, height=48,
        fill="#F4EFE0", opacity=16, stroke=NONE)
d.shape("ellipse", "Snort 3", x=202, y=600, width=100, height=54,
        fill="#EEF4E6", opacity=10, stroke=NONE)

# --- low mist drifting in front of the chest and legs -------------------------------------
d.path("M160,700 C330,684 540,690 700,708", "Front mist", fill=NONE,
       stroke="#F0F6EC", strokeWidth=26, opacity=10, cap="round")
d.path("M200,742 C360,728 560,734 720,748", "Front mist low", fill=NONE,
       stroke="#F0F6EC", strokeWidth=18, opacity=8, cap="round")

# --- name ---------------------------------------------------------------------------------
d.text("TAKIN", "Name", x=500, y=962, size=60, font="Virelai Sans",
       color="#E6D9BC", justify="center")

d.finish("takin-V1R00")
