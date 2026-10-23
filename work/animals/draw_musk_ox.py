#!/usr/bin/env python3
"""Musk ox — field-guide plate V1R00. Full body, front-quarter view in weather:
the pale horn boss bands the brow and drops into hooks at the cheeks, the
long skirt of guard hair falls in vertical strands to meet the snowdrift.
Ice-blue plate, blowing snow, warm breath fog at the muzzle. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Musk Ox — Field Plate", 1000, 1000)
rng = random.Random(41)

INK = "#241A10"
BG_GRAD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000], "stops": [
    {"offset": 0, "color": "#0E1B26"}, {"offset": 1, "color": "#04090F"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#DCEAF2"}, {"offset": 0.7, "color": "#A6C2D2"},
    {"offset": 1, "color": "#66869C"}]}}
FUR_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#5A4630"}, {"offset": 0.6, "color": "#38291B"},
    {"offset": 1, "color": "#1D140C"}]}}
SADDLE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#D8CBA8"}, {"offset": 1, "color": "#B0A180"}]}}
BOSS_GRAD = {"gradient": {"kind": "linear", "start": [0, 380], "end": [0, 470], "stops": [
    {"offset": 0, "color": "#EFE4C4"}, {"offset": 1, "color": "#AE9C74"}]}}
HORN_GRAD = {"gradient": {"kind": "linear", "start": [0, 420], "end": [0, 580], "stops": [
    {"offset": 0, "color": "#DCCFA8"}, {"offset": 1, "color": "#8F7E5C"}]}}
SNOW_GRAD = {"gradient": {"kind": "linear", "start": [0, 700], "end": [0, 880], "stops": [
    {"offset": 0, "color": "#F4F9FC"}, {"offset": 1, "color": "#B8CFDE"}]}}
MUZZLE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#6E5A44"}, {"offset": 1, "color": "#3A2D20"}]}}

PCX, PCY, PR = 500, 460, 420

def on_disc(x, y, pad):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

# --- backdrop + plate --------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#A6C2D2", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#466A7E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F0F7FA", strokeWidth=3, opacity=55)
# blowing snow: long wind streaks high in the plate
for i, dd in enumerate(["M170,240 C330,215 520,215 700,240",
                        "M240,315 C400,292 580,292 740,318",
                        "M150,380 C300,360 480,360 640,385"]):
    d.path(dd, f"Wind streak {i+1}", fill=NONE, stroke="#EAF4FA",
           strokeWidth=5, opacity=22, cap="round")
# distant flakes behind the animal
for i, (x, y, w) in enumerate([(200,300,7),(770,250,6),(160,470,8),(830,430,7),(250,150,6),(720,150,7),
                               (400,120,6),(600,115,7),(140,580,6),(860,560,6),(330,200,5),(680,220,5)]):
    assert on_disc(x + w / 2, y + w / 2, 8), (x, y)
    d.shape("ellipse", f"Back flake {i+1}", x=x, y=y, width=w, height=w,
            fill="#F4FAFD", opacity=55, stroke=NONE)

# --- snowdrift: top edge, closing on the disc's own arc ------------------------------
d.path("M194,748 C380,730 620,730 806,748 A420,420 0 0 1 194,748 Z",
       "Snowdrift", fill=SNOW_GRAD, stroke="#8FACC0", strokeWidth=4)
d.path("M240,760 C380,750 620,750 760,762", "Drift shade", fill=NONE,
       stroke="#9FBDD0", strokeWidth=5, opacity=40, cap="round")

# --- body mass with ragged guard-hair hem -------------------------------------------
BODY = ("M325,545 "
        "C318,505 330,462 358,438 "        # face front rising to the poll
        "C390,412 440,398 500,395 "        # crown into the shoulder hump
        "C560,382 640,392 682,432 "        # hump top
        "C715,465 726,520 720,575 "        # rump rounding down
        "C716,630 706,672 692,700 "        # rear hem edge
        "L676,692 L668,712 L652,694 L640,718 L624,698 L612,722 "
        "L594,702 L582,726 L564,706 L550,730 L532,710 L518,732 "
        "L500,712 L486,734 L468,714 L454,736 L438,716 L426,732 "
        "L412,716 L400,728 L390,712 "      # ragged hair hem
        "C378,700 372,680 376,660 "        # chest front
        "C358,640 345,610 342,585 "        # jaw underside
        "C330,575 324,562 325,545 Z")      # chin back to the nose
d.path(BODY, "Body", fill=FUR_GRAD, stroke=INK, strokeWidth=7)

# pale saddle patch on the mid-back + snow dusting on the hump
d.path("M480,420 C540,402 620,410 664,448 C640,472 560,478 505,462 "
       "C486,452 476,436 480,420 Z",
       "Saddle", fill=SADDLE_GRAD, opacity=55, stroke=NONE)
for i, dd in enumerate(["M470,398 C520,384 600,386 656,408",
                        "M430,410 C460,398 505,392 545,396"]):
    d.path(dd, f"Back snow {i+1}", fill=NONE, stroke="#F4FAFD",
           strokeWidth=7, opacity=35, cap="round")

# long guard-hair strands falling from mid-body to the hem
for i in range(26):
    x = 400 + i * 11.5 + rng.uniform(-3, 3)
    y0 = rng.uniform(500, 560)
    y1 = rng.uniform(660, 725)
    col = rng.choice(["#171008", "#171008", "#6E5A40", "#4A3826"])
    d.path(f"M{x:.0f},{y0:.0f} C{x+rng.uniform(-6,6):.0f},{(y0+y1)/2:.0f} "
           f"{x+rng.uniform(-8,8):.0f},{y1-30:.0f} {x+rng.uniform(-6,6):.0f},{y1:.0f}",
           f"Hair strand {i+1}", fill=NONE, stroke=col,
           strokeWidth=3, opacity=rng.randint(30, 50), cap="round")
# flank shadow + chest light
d.shape("ellipse", "Flank shade", x=560, y=520, width=160, height=180,
        fill="#120B06", opacity=22, stroke=NONE)
d.shape("ellipse", "Chest light", x=380, y=470, width=110, height=120,
        fill="#8A7250", opacity=18, stroke=NONE)

# --- horn boss across the brow -------------------------------------------------------
d.path("M354,440 C378,410 470,396 545,410 C558,416 562,430 556,444 "
       "C495,428 408,434 368,460 C357,454 352,448 354,440 Z",
       "Horn boss", fill=BOSS_GRAD, stroke=INK, strokeWidth=5)
d.path("M366,432 C405,412 485,404 542,416", "Boss light", fill=NONE,
       stroke="#FBF4DE", strokeWidth=4, opacity=50, cap="round")
# boss knurl: small notches along its upper edge
for i, dd in enumerate(["M400,418 l6,10", "M438,412 l5,11", "M476,410 l4,12",
                        "M512,412 l3,11", "M540,418 l2,10"]):
    d.path(dd, f"Boss knurl {i+1}", fill=NONE, stroke="#8A7652",
           strokeWidth=3, opacity=45, cap="round")

# --- horns: drop beside the cheeks, then hook upward ---------------------------------
# near horn (viewer's left): down the face, tip kicks up beside the muzzle
d.path("M360,450 C336,470 320,504 320,534 C320,558 334,574 352,568 "
       "C344,548 342,524 346,500 C350,478 360,460 374,450 Z",
       "Horn near", fill=HORN_GRAD, stroke=INK, strokeWidth=5)
d.path("M326,544 C322,524 328,502 340,484", "Horn near tip", fill=NONE,
       stroke="#F2E8CC", strokeWidth=4, opacity=55, cap="round")
# far horn (behind the poll, smaller): peeks out right of the head
d.path("M530,424 C556,438 570,466 568,494 C566,514 554,526 540,520 "
       "C550,502 552,478 546,456 C542,440 534,430 530,424 Z",
       "Horn far", fill="#9C8A64", stroke=INK, strokeWidth=5)
d.path("M560,506 C564,488 560,466 550,450", "Horn far tip", fill=NONE,
       stroke="#E8DDBB", strokeWidth=4, opacity=45, cap="round")

# --- ear peeking below the boss's far end --------------------------------------------
d.path("M548,442 C568,436 586,444 590,460 C578,472 556,470 548,458 Z",
       "Ear", fill="#3A2D1E", stroke=INK, strokeWidth=3)

# --- face: broad muzzle, nostrils, watchful eye --------------------------------------
d.path("M330,505 C345,480 385,468 415,478 C435,492 438,520 425,545 "
       "C405,565 365,568 342,552 C328,538 325,522 330,505 Z",
       "Muzzle", fill=MUZZLE_GRAD, stroke=INK, strokeWidth=5)
d.shape("ellipse", "Nostril near", x=336, y=518, width=22, height=14,
        fill="#14100A", stroke=NONE)
d.shape("ellipse", "Nostril far", x=392, y=514, width=18, height=12,
        fill="#14100A", opacity=80, stroke=NONE)
d.path("M340,552 C360,562 395,562 418,550", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
d.shape("ellipse", "Muzzle light", x=352, y=488, width=60, height=26,
        fill="#9A8264", opacity=35, stroke=NONE)
# eye under the boss overhang
d.shape("ellipse", "Eye socket", x=418, y=448, width=40, height=38,
        fill="#241A10", opacity=60, stroke=NONE)
d.shape("ellipse", "Eye", x=426, y=455, width=22, height=21, fill="#0E0906",
        stroke=NONE)
d.shape("ellipse", "Eye glint", x=431, y=460, width=6, height=6,
        fill="#FFFFFF", opacity=80, stroke=NONE)
# shaggy forelock spilling over the boss
for i, dd in enumerate(["M390,430 C386,450 388,468 396,484",
                        "M420,424 C418,446 422,464 430,478",
                        "M452,420 C452,440 458,458 466,470"]):
    d.path(dd, f"Forelock {i+1}", fill=NONE, stroke="#241A10",
           strokeWidth=6, opacity=55, cap="round")

# --- breath fog drifting off the nostrils --------------------------------------------
d.shape("ellipse", "Breath 1", x=286, y=520, width=70, height=44,
        fill="#F0F7FB", opacity=22, stroke=NONE)
d.shape("ellipse", "Breath 2", x=250, y=545, width=90, height=52,
        fill="#F0F7FB", opacity=15, stroke=NONE)
d.shape("ellipse", "Breath 3", x=215, y=575, width=110, height=58,
        fill="#EAF4FA", opacity=10, stroke=NONE)

# --- foreground flakes (in front of the animal, sparse) -------------------------------
for i, (x, y, w) in enumerate([(300,250,8),(660,300,7),(250,650,7),(750,620,8),(480,330,6),
                               (180,680,6),(820,330,7),(560,140,6),(370,780,5),(640,780,6)]):
    assert on_disc(x + w / 2, y + w / 2, 6), (x, y)
    d.shape("ellipse", f"Front flake {i+1}", x=x, y=y, width=w, height=w,
            fill="#FFFFFF", opacity=70, stroke=NONE)

# --- name ----------------------------------------------------------------------------
d.text("MUSK OX", "Name", x=500, y=962, size=60, font="Virelai Sans",
       color="#E2EEF5", justify="center")

d.finish("musk-ox-V1R00")
