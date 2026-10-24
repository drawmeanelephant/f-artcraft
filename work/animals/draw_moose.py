#!/usr/bin/env python3
"""Moose — field-guide plate V1R00. Bull head-and-shoulders in profile, belly-deep
in the bog at muggy dusk: palmate antlers like a carried forest, the bell swinging
under the throat, blackflies orbiting the poll. Dark peat water closes on the disc
arc; sedges and cattails at the rim. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Moose — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420          # plate disc centre + radius
INK = "#160C06"

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def on_disc(x, y, pad=0):
    return math.hypot(x - CX, y - CY) <= R - pad

BG_GRAD = lin(0, 0, 0, 1000, (0, "#0C120C"), (1, "#030503"))
PLATE_GRAD = rad((0, "#C4CDAE"), (0.55, "#8D9C7B"), (1, "#4C5B42"))
WATER_GRAD = lin(0, 715, 0, 880, (0, "#46543E"), (1, "#1B2519"))
COAT = lin(0, 300, 0, 720, (0, "#5A422C"), (0.5, "#3C2A1A"), (1, "#241508"))
DARKFUR = lin(0, 320, 0, 720, (0, "#3A2A1A"), (1, "#1A0E06"))
ANTLER = lin(0, 160, 0, 380, (0, "#D8CBA6"), (1, "#9A8A64"))
ANTLER_FAR = lin(0, 190, 0, 380, (0, "#A79877"), (1, "#6E5F45"))
MUZZLE = rad((0, "#8A7A66"), (1, "#554838"))

# --- backdrop + bog plate ------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880, fill="#8D9C7B", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#37432E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E2E8D2", strokeWidth=3, opacity=40)
# muggy low sun — a dull ember through the bog haze, behind the antlers' reach
d.shape("ellipse", "Bog sun", x=170, y=470, width=150, height=150,
        fill=rad((0, "#E8C08A"), (0.7, "#C89458"), (1, "#9A6838")), opacity=55, stroke=NONE)
d.shape("ellipse", "Sun haze", x=130, y=430, width=230, height=230,
        fill="#E8C08A", opacity=12, stroke=NONE)
# haze bands drifting across the waterline
for i, (y, op) in enumerate([(640, 14), (680, 11)]):
    d.path(f"M150,{y} C300,{y-14} 480,{y+10} 650,{y-6} C740,{y-12} 830,{y-6} 880,{y}",
           f"Haze {i+1}", fill=NONE, stroke="#D8DEC8", strokeWidth=16, opacity=op, cap="round")

# blackflies orbiting the head — the mood, literally
for i, (x, y, w) in enumerate([(300,300,4),(348,268,3),(420,242,4),(268,352,3),(322,330,3),
                               (386,296,3),(448,300,4),(256,404,3),(360,352,3),(418,338,3)]):
    assert on_disc(x, y, 14), (x, y)
    d.shape("ellipse", f"Fly {i+1}", x=x, y=y, width=w, height=w, fill="#14100A", opacity=75, stroke=NONE)
for i, (x, y) in enumerate([(310,296),(428,246),(278,356)]):
    d.path(f"M{x},{y} C{x+5},{y-5} {x+10},{y-5} {x+13},{y}",
           f"Fly wing {i+1}", fill=NONE, stroke="#E8ECD8", strokeWidth=1.5, opacity=50, cap="round")

# --- peat water: soughing top edge, bottom closes on the disc arc --------------
wy = 720
wdx = math.sqrt(R * R - (wy - CY) ** 2)
d.path(f"M{CX-wdx:.1f},{wy} C300,706 420,718 540,712 C650,707 730,716 {CX+wdx:.1f},{wy} "
       f"A{R},{R} 0 0 1 {CX-wdx:.1f},{wy} Z", "Water", fill=WATER_GRAD, stroke=NONE)
d.path(f"M{CX-wdx+8:.1f},{wy-2} C300,704 420,714 540,708 C650,703 730,712 {CX+wdx-8:.1f},{wy-2}",
       "Water light", fill=NONE, stroke="#C8D2B4", strokeWidth=4, opacity=40, cap="round")
# sun's smeared reflection on the water
d.path("M200,742 C240,738 280,738 316,742 C280,748 240,748 200,742 Z",
       "Sun path", fill="#E8C08A", opacity=20, stroke=NONE)
d.path("M214,764 C246,761 278,761 306,764 C278,768 246,768 214,764 Z",
       "Sun path 2", fill="#E8C08A", opacity=14, stroke=NONE)
# lily pads
for i, (x, y, w) in enumerate([(268,782,46),(330,806,34),(240,758,26),(700,780,40),(740,756,28)]):
    assert on_disc(x + w/2, y + w/4, 20), (x, y)
    d.shape("ellipse", f"Pad {i+1}", x=x, y=y, width=w, height=w*0.42,
            fill="#2E3E28", opacity=85, stroke="#1A2414", strokeWidth=2)
d.path("M278,782 L304,786 M270,790 L296,788", "Pad cut", fill=NONE,
       stroke=WATER_GRAD, strokeWidth=4, cap="round")
# drowned snag poking out of the water, right of centre
d.path("M756,742 C762,716 770,696 782,682 C786,700 782,722 774,742 Z",
       "Snag", fill="#241A0E", opacity=80, stroke=NONE)

# --- sedges + cattails at the rim ----------------------------------------------
def sedge(x, base, top, lean, w, label, op=80):
    d.path(f"M{x},{base} C{x+lean*0.4},{base-40} {x+lean*0.8},{top+30} {x+lean},{top}",
           label, fill=NONE, stroke="#2C3A24", strokeWidth=w, opacity=op, cap="round")

for i, (x, top, lean, w) in enumerate([(206,586,-24,4),(226,560,-12,4.5),(250,604,-30,3.5),
                                       (268,570,-6,4),(288,598,8,3)]):
    sedge(x, 736, top, lean, w, f"Sedge L {i+1}")
# cattail heads on two of them
d.path("M210,592 C206,566 208,544 214,528 C222,544 224,566 220,592 Z",
       "Cattail L1", fill="#4A3016", stroke=INK, strokeWidth=2.5)
d.path("M214,530 L214,518", "Cattail L1 stem", fill=NONE, stroke="#2C3A24", strokeWidth=2, cap="round")
d.path("M258,574 C254,550 256,530 262,516 C270,530 272,550 268,574 Z",
       "Cattail L2", fill="#4A3016", stroke=INK, strokeWidth=2.5)
d.path("M262,518 L262,506", "Cattail L2 stem", fill=NONE, stroke="#2C3A24", strokeWidth=2, cap="round")
for i, (x, top, lean, w) in enumerate([(806,580,18,4),(824,556,10,4.5),(842,596,22,3.5)]):
    sedge(x, 734, top, lean, w, f"Sedge R {i+1}")
d.path("M832,560 C828,536 830,516 836,502 C844,516 846,536 842,560 Z",
       "Cattail R1", fill="#4A3016", stroke=INK, strokeWidth=2.5)
d.path("M836,504 L836,492", "Cattail R1 stem", fill=NONE, stroke="#2C3A24", strokeWidth=2, cap="round")

# --- moose: bull head + shoulders, nose left -----------------------------------
# antlers first: beams bury in the poll so the palms grow out of the skull.
# palmate blade = wider than tall, tines round the whole outer rim, beam thick
# far antler — darker blade peeking above and behind
d.path("M480,376 C506,350 534,324 568,298 C580,288 590,278 598,266 "
       "L590,246 L612,256 L618,228 L638,246 L646,220 L662,242 "
       "L682,216 L690,244 L712,232 L710,262 "
       "C726,276 730,294 720,310 C704,330 672,342 636,346 "
       "C598,352 546,360 510,366 C496,368 486,372 480,376 Z",
       "Antler far", fill=ANTLER_FAR, stroke=INK, strokeWidth=4)
# ear: big blade flopping sideways under the antler base
d.path("M452,362 C424,352 396,352 376,364 C392,380 422,386 450,378 Z",
       "Ear", fill=DARKFUR, stroke=INK, strokeWidth=4)
# near antler — the carried forest
d.path("M448,370 C476,344 504,318 536,292 C548,282 558,272 566,260 "
       "L556,240 L576,250 L580,224 L600,240 L606,212 L624,234 "
       "L636,206 L650,232 L668,202 L678,230 L700,196 L706,226 "
       "L724,214 L722,244 L734,262 L718,282 "
       "C700,298 676,308 650,316 C610,326 560,338 522,344 "
       "C496,350 470,360 448,370 Z",
       "Antler near", fill=ANTLER, stroke=INK, strokeWidth=4.5)
# palm shading — darker scoop along the lower palm
d.path("M540,332 C576,330 620,322 652,310 C676,300 692,286 700,270 "
       "C690,296 668,314 638,322 C604,330 566,332 540,332 Z",
       "Palm shade", fill="#6E5F45", opacity=60, stroke=NONE)

# one silhouette: muzzle front → dished face → poll → hump → back → waterline →
# chest → smooth throat → under-muzzle
SILH = ("M292,472 C300,452 318,436 344,426 C366,418 388,414 406,412 "
        "C418,404 428,392 438,382 C456,368 478,362 500,364 "
        "C528,348 560,342 590,346 C634,352 676,384 706,432 "
        "C730,470 744,524 748,578 C752,626 750,676 742,716 "
        "C700,724 640,726 580,722 C530,719 486,716 456,712 "
        "C448,682 448,646 456,616 C442,596 430,576 424,556 "
        "C406,540 384,530 366,520 C342,512 320,504 304,494 "
        "C294,486 288,478 292,472 Z")
d.path(SILH, "Moose", fill=COAT, stroke=INK, strokeWidth=6)

# the bell: thin flap swinging under the throat
d.path("M420,560 C414,592 414,624 424,650 C428,660 436,662 442,654 "
       "C438,624 438,594 444,568 C436,560 426,556 420,560 Z",
       "Bell", fill=DARKFUR, stroke=INK, strokeWidth=4)

# muzzle: the big grey overhanging nose — paler, squared, drooping
d.path("M292,472 C300,452 318,436 344,426 C364,418 384,414 402,412 "
       "C396,428 384,442 368,452 C380,458 388,468 390,480 "
       "C392,494 384,506 368,512 C346,518 320,510 304,496 "
       "C294,486 288,478 292,472 Z",
       "Muzzle", fill=MUZZLE, opacity=85, stroke=NONE)
# nostril: the long moose comma
d.path("M312,468 C318,456 330,448 342,448 C336,460 326,468 316,470 Z",
       "Nostril", fill="#0E0804", stroke=NONE)
# mouth line under the overhang
d.path("M300,494 C320,502 344,506 366,506", "Mouth",
       fill=NONE, stroke=INK, strokeWidth=4, cap="round")

# the eye: small, deep-set, amber under the overhang of brow
d.path("M392,432 C402,422 420,420 432,428 C424,442 404,444 392,432 Z",
       "Eye", fill=rad((0, "#C89440"), (0.6, "#8A5E1C"), (1, "#4A300C")),
       stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Pupil", x=410, y=425, width=9, height=12, fill="#0E0A04", stroke=NONE)
d.shape("ellipse", "Glint", x=412, y=428, width=4, height=4, fill="#FFFFFF", opacity=90, stroke=NONE)
d.path("M388,428 C400,416 422,414 436,424", "Brow",
       fill=NONE, stroke=INK, strokeWidth=5, cap="round")
d.path("M392,444 C404,450 420,449 430,442", "Under eye",
       fill=NONE, stroke="#8A7A66", strokeWidth=2.5, opacity=50, cap="round")

# hump shading + coat texture down the neck and shoulder
d.path("M500,370 C540,354 580,350 614,360 C660,374 696,412 716,462 "
       "C700,420 668,392 626,382 C580,372 536,374 500,388 Z",
       "Hump light", fill="#6B4E32", opacity=55, stroke=NONE)
for i, dd in enumerate(["M520,420 C540,460 552,510 554,562",
                        "M560,430 C584,472 596,524 596,576",
                        "M620,452 C644,494 656,546 654,600",
                        "M480,440 C494,480 502,524 502,568"]):
    d.path(dd, f"Coat fur {i+1}", fill=NONE, stroke="#241508", strokeWidth=4, opacity=40, cap="round")
# dew-wet sheen on the shoulder
d.path("M560,380 C610,376 658,392 692,424", "Shoulder sheen",
       fill=NONE, stroke="#9A8A64", strokeWidth=5, opacity=30, cap="round")

# ripples where the chest and shoulder break the surface
for i, (x, y, w) in enumerate([(430,718,120),(470,724,170),(560,722,230),(680,720,180)]):
    d.path(f"M{x-w/2},{y} C{x-w/4},{y-6} {x+w/4},{y-6} {x+w/2},{y}",
           f"Ripple {i+1}", fill=NONE, stroke="#C8D2B4", strokeWidth=3, opacity=35, cap="round")
# dark water contact shadow under the chest
d.path("M440,714 C500,724 600,726 700,718", "Water shadow",
       fill=NONE, stroke="#0E140C", strokeWidth=10, opacity=40, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#0A120A", strokeWidth=6)

# --- name ----------------------------------------------------------------------
d.text("MOOSE", "Name", x=500, y=962, size=58, font="Virelai Sans",
       color="#DCE4CC", justify="center")

d.finish("moose-V1R00")
