#!/usr/bin/env python3
"""Orangutan — field-guide plate V1R00. Frontal portrait of a flanged male:
rust-red shaggy mane haloing the wide dark cheek pads, deep-set eyes under a
heavy brow — the old man of the forest in durian season. Lianas and canopy
leaves droop from the top, a ripe durian hangs at left, a split fruit rests
on a leaf-litter floor that closes on the disc arc. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Orangutan — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420          # plate disc centre + radius
INK = "#160C04"

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def on_disc(x, y, pad=0):
    return math.hypot(x - CX, y - CY) <= R - pad

BG_GRAD = lin(0, 0, 0, 1000, (0, "#0E160C"), (1, "#030502"))
PLATE_GRAD = rad((0, "#D6D8A8"), (0.55, "#93A468"), (1, "#46562E"))
FLOOR_GRAD = lin(0, 764, 0, 880, (0, "#42492A"), (1, "#181C0C"))
FUR = lin(0, 220, 0, 860, (0, "#C86428"), (0.5, "#96400F"), (1, "#5E2406"))
FUR_DK = "#6E2E0A"
FUR_LT = "#E08A44"
PAD = rad((0, "#4A3424"), (1, "#241812"))        # cheek flange skin
FACE_SKIN = rad((0, "#7A563C"), (0.7, "#5E3E2A"), (1, "#402A1A"))
LEAF = "#3C5228"
LEAF_DK = "#2C3E1E"
DURIAN = lin(0, 0, 0, 1000, (0, "#8A9440"), (1, "#56601E"))

# --- backdrop + canopy plate ---------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880, fill="#93A468", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#36441F", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E2E4BC", strokeWidth=3, opacity=40)
# canopy light shafts
d.path("M640,110 L520,430", "Shaft 1", fill=NONE, stroke="#EAE6B4",
       strokeWidth=70, opacity=9, cap="round")
d.path("M760,180 L660,420", "Shaft 2", fill=NONE, stroke="#EAE6B4",
       strokeWidth=45, opacity=7, cap="round")

# --- lianas + canopy leaves drooping from the top -------------------------------
d.path("M300,98 C296,130 310,170 296,240 C288,282 292,318 304,350",
       "Liana L", fill=NONE, stroke="#2E4420", strokeWidth=8, cap="round")
d.path("M690,94 C700,130 686,160 696,220 C702,262 696,300 684,330",
       "Liana R", fill=NONE, stroke="#2E4420", strokeWidth=8, cap="round")

def droopleaf(x, y, s, ang, label, fill=LEAF):
    """Lobed canopy leaf hanging from (x,y), scale s, lean ang (rad)."""
    t = ang
    ux, uy = math.sin(t), math.cos(t)          # leaf axis points down
    L = 90 * s
    tx, ty = x + ux * L, y + uy * L
    wx, wy = uy, -ux
    w = L * 0.30
    p = (f"M{x},{y} "
         f"C{x + ux*L*0.3 + wx*w},{y + uy*L*0.3 + wy*w} "
         f"{x + ux*L*0.7 + wx*w*0.9},{y + uy*L*0.7 + wy*w*0.9} {tx},{ty} "
         f"C{x + ux*L*0.7 - wx*w*0.9},{y + uy*L*0.7 - wy*w*0.9} "
         f"{x + ux*L*0.3 - wx*w},{y + uy*L*0.3 - wy*w} {x},{y} Z")
    d.path(p, label, fill=fill, stroke=INK, strokeWidth=3)
    d.path(f"M{x},{y} L{tx:.0f},{ty:.0f}", f"{label} rib",
           fill=NONE, stroke="#5E7840", strokeWidth=2.5, opacity=60, cap="round")

droopleaf(296, 180, 1.0, -0.9, "Leaf L1")
droopleaf(302, 250, 0.85, 0.8, "Leaf L2", LEAF_DK)
droopleaf(694, 160, 0.95, 0.95, "Leaf R1")
droopleaf(690, 235, 0.8, -0.85, "Leaf R2", LEAF_DK)
droopleaf(500, 60, 1.1, -0.55, "Leaf T1")
droopleaf(560, 54, 0.9, 0.7, "Leaf T2", LEAF_DK)

# --- a ripe durian hanging at left ----------------------------------------------
d.path("M236,150 C234,185 236,215 238,240", "Durian stem",
       fill=NONE, stroke="#3A2E14", strokeWidth=5, cap="round")
d.path("M196,240 C188,280 194,318 214,338 C234,358 264,356 280,334 "
       "C294,314 296,278 284,254 C270,230 240,224 220,232 "
       "C208,236 200,238 196,240 Z",
       "Durian", fill=DURIAN, stroke=INK, strokeWidth=4)
# spikes: short pointed strokes ringing the fruit
for i, (x, y, dx, dy) in enumerate([(200,258,-14,-8),(196,286,-16,0),(206,316,-12,10),
                                    (228,340,-4,15),(256,344,4,14),(278,326,12,10),
                                    (288,296,15,2),(282,264,13,-8),(260,240,6,-13),(228,238,-6,-13)]):
    d.path(f"M{x},{y} L{x+dx},{y+dy}", f"Spike {i+1}",
           fill=NONE, stroke="#464E14", strokeWidth=5, cap="round")
d.shape("ellipse", "Durian light", x=222, y=258, width=24, height=34,
        fill="#C8CC78", opacity=40, stroke=NONE)

# --- leaf-litter floor: crest ~y764, bottom closes on the disc arc --------------
fy = 764
fdx = math.sqrt(R * R - (fy - CY) ** 2)
d.path(f"M{CX-fdx:.1f},{fy} C300,750 430,760 560,754 C650,750 730,758 {CX+fdx:.1f},{fy} "
       f"A{R},{R} 0 0 1 {CX-fdx:.1f},{fy} Z", "Floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{CX-fdx+8:.1f},{fy-2} C300,748 430,756 560,750 C650,746 730,754 {CX+fdx-8:.1f},{fy-2}",
       "Floor light", fill=NONE, stroke="#DCE0B0", strokeWidth=4, opacity=30, cap="round")
# fallen leaves on the litter
for i, (x, y, w, c) in enumerate([(280,792,34,"#5A6634"),(350,812,26,"#4A5628"),(700,800,28,"#5A6634")]):
    d.shape("ellipse", f"Litter leaf {i+1}", x=x, y=y, width=w, height=w*0.4,
            fill=c, opacity=70, stroke=NONE)

# --- the mane: shaggy rust halo around the face, closes on the arc --------------
my = 800
mdx = math.sqrt(R * R - (my - CY) ** 2)
mxl, mxr = CX - mdx, CX + mdx
MANE = (f"M318,330 C330,280 380,240 450,228 C520,216 600,232 656,272 "
        f"C700,304 726,350 728,404 C760,440 778,490 776,548 "
        f"C774,620 742,690 690,736 C740,752 {mxr-4:.0f},778 {mxr:.0f},{my} "
        f"A{R},{R} 0 0 1 {mxl:.0f},{my} "
        f"C{mxl+4:.0f},778 260,752 310,736 C258,690 226,620 224,548 "
        f"C222,490 240,440 272,404 C274,376 292,348 318,330 Z")
d.path(MANE, "Mane", fill=FUR, stroke=INK, strokeWidth=6)
# mane edge fur: jagged strokes combing outward
for i, (x, y, dx, dy) in enumerate([
        (262,430,-26,-4),(252,470,-28,2),(248,514,-28,8),(254,560,-24,12),
        (266,610,-20,16),(286,656,-14,20),(738,430,26,-4),(748,470,28,2),
        (752,514,28,8),(746,560,24,12),(734,610,20,16),(714,656,14,20),
        (340,300,-18,-14),(390,268,-12,-18),(610,268,12,-18),(660,300,18,-14)]):
    d.path(f"M{x},{y} L{x+dx},{y+dy}", f"Mane edge {i+1}",
           fill=NONE, stroke=FUR_DK, strokeWidth=7, opacity=75, cap="round")
# long hair strokes inside the mane
for i, dd in enumerate([
        "M300,420 C292,470 292,530 304,580", "M284,460 C276,520 280,580 296,630",
        "M330,380 C320,440 322,500 336,556", "M700,420 C708,470 708,530 696,580",
        "M716,460 C724,520 720,580 704,630", "M670,380 C680,440 678,500 664,556",
        "M420,266 C400,300 388,340 386,384", "M580,266 C600,300 612,340 614,384"]):
    d.path(dd, f"Mane hair {i+1}", fill=NONE, stroke=FUR_DK,
           strokeWidth=5, opacity=50, cap="round")
# mane highlight on the crown
d.path("M360,300 C400,262 470,244 540,250 C600,256 650,280 678,318 "
       "C640,292 590,274 534,270 C478,266 412,278 360,300 Z",
       "Mane light", fill=FUR_LT, opacity=55, stroke=NONE)

# --- face: dark cheek flanges + central skin ------------------------------------
# flange pads — wide dark discs each side of the muzzle
d.path("M352,430 C330,470 322,520 330,570 C338,622 368,660 410,676 "
       "C436,684 458,678 468,658 C474,640 470,614 458,592 "
       "C442,562 434,528 436,494 C438,462 430,440 410,428 "
       "C390,418 366,418 352,430 Z",
       "Flange L", fill=PAD, stroke=NONE)
d.path("M648,430 C670,470 678,520 670,570 C662,622 632,660 590,676 "
       "C564,684 542,678 532,658 C526,640 530,614 542,592 "
       "C558,562 566,528 564,494 C562,462 570,440 590,428 "
       "C610,418 634,418 648,430 Z",
       "Flange R", fill=PAD, stroke=NONE)
# flange sheen
d.path("M350,470 C342,510 346,556 360,596 C344,560 338,514 344,474 Z",
       "Flange sheen L", fill="#6A4E34", opacity=45, stroke=NONE)
d.path("M650,470 C658,510 654,556 640,596 C656,560 662,514 656,474 Z",
       "Flange sheen R", fill="#6A4E34", opacity=45, stroke=NONE)
# central face: brow → eyes → broad flat nose → projecting muzzle
d.path("M420,340 C440,318 470,306 500,306 C530,306 560,318 580,340 "
       "C600,364 612,398 610,434 C626,456 634,486 632,518 "
       "C630,562 612,602 578,626 C556,642 526,650 500,650 "
       "C474,650 444,642 422,626 C388,602 370,562 368,518 "
       "C366,486 374,456 390,434 C388,398 400,364 420,340 Z",
       "Face", fill=FACE_SKIN, stroke=NONE)
# heavy brow bar
d.path("M420,400 C444,384 474,376 500,376 C526,376 556,384 580,400 "
       "C560,394 530,390 500,390 C470,390 440,394 420,400 Z",
       "Brow", fill="#2A1A10", opacity=80, stroke=NONE)
d.path("M430,384 C452,372 478,366 500,366 C522,366 548,372 570,384",
       "Brow ridge", fill=NONE, stroke=INK, strokeWidth=6, cap="round")
# deep-set eyes, quiet and close under the brow
d.path("M442,428 C452,416 470,414 482,422 C476,436 456,440 442,428 Z",
       "Eye L", fill=rad((0, "#3A2410"), (1, "#120A04")),
       stroke=INK, strokeWidth=3)
d.path("M518,422 C530,414 548,416 558,428 C544,440 524,436 518,422 Z",
       "Eye R", fill=rad((0, "#3A2410"), (1, "#120A04")),
       stroke=INK, strokeWidth=3)
d.shape("ellipse", "Glint L", x=458, y=422, width=5, height=5,
        fill="#FFFFFF", opacity=80, stroke=NONE)
d.shape("ellipse", "Glint R", x=536, y=422, width=5, height=5,
        fill="#FFFFFF", opacity=80, stroke=NONE)
# lids — heavy, the old man's look
d.path("M438,424 C450,410 472,408 486,418 M514,418 C528,408 550,410 562,424",
       "Lids", fill=NONE, stroke=INK, strokeWidth=4.5, cap="round")
# broad flat nose, nostrils flaring outward-down
d.path("M462,470 C474,458 490,452 500,454 C510,452 526,458 538,470 "
       "C548,484 550,502 542,516 C532,530 514,536 500,536 "
       "C486,536 468,530 458,516 C450,502 452,484 462,470 Z",
       "Nose bridge", fill="#4A3020", opacity=85, stroke=NONE)
d.path("M458,510 C448,518 438,532 440,546 C444,558 458,562 468,556 "
       "C476,548 476,534 468,524 C464,518 460,514 458,510 Z",
       "Nostril L", fill="#1C1008", stroke=NONE)
d.path("M542,510 C552,518 562,532 560,546 C556,558 542,562 532,556 "
       "C524,548 524,534 532,524 C536,518 540,514 542,510 Z",
       "Nostril R", fill="#1C1008", stroke=NONE)
# nostril crease
d.path("M470,522 C478,514 490,510 500,510 C510,510 522,514 530,522",
       "Septum", fill=NONE, stroke="#241608", strokeWidth=3.5, cap="round")
# projecting muzzle + the long thoughtful mouth
d.path("M430,556 C450,546 478,544 500,548 C522,544 550,546 570,556 "
       "C584,570 586,594 576,612 C560,634 530,644 500,644 "
       "C470,644 440,634 424,612 C414,594 416,570 430,556 Z",
       "Muzzle", fill="#6E4C34", opacity=90, stroke=NONE)
d.path("M434,586 C460,598 480,602 500,602 C520,602 540,598 566,586",
       "Mouth", fill=NONE, stroke=INK, strokeWidth=5, cap="round")
d.path("M446,600 C470,610 530,610 554,600", "Lower lip",
       fill=NONE, stroke="#8A5E40", strokeWidth=4, opacity=70, cap="round")
# chin pad
d.shape("ellipse", "Chin", x=470, y=622, width=60, height=24,
        fill="#5E3E28", opacity=60, stroke=NONE)
# throat beard wisps under the chin
for i, (x0, x1) in enumerate([(452,446),(486,482),(514,518),(548,554)]):
    d.path(f"M{x0},648 C{x0-4},670 {x1-6},692 {x1-10},712",
           f"Beard {i+1}", fill=NONE, stroke=FUR_DK,
           strokeWidth=5, opacity=65, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#0C1206", strokeWidth=6)

# --- name ----------------------------------------------------------------------
d.text("ORANGUTAN", "Name", x=500, y=962, size=60, font="Virelai Sans",
       color="#DDE2B8", justify="center")

d.finish("orangutan-V1R00")
