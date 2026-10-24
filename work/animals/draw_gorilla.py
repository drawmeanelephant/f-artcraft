#!/usr/bin/env python3
"""Gorilla — field-guide plate V1R00. Face-forward silverback portrait: the
sagittal-crest dome, a heavy brow shelf shading small calm eyes, the broad
flat nose and a wide stern mouth, massive shoulders with the silver saddle
catching light. Forest-mist plate, leaf-dark mood — mist bands, leaf
silhouettes inside the rim, a moss floor closing on the disc's own arc.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os, math, re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Gorilla — Field Plate", 1000, 1000)

INK = "#14100C"                    # warm dark ink, never pure black
CX, CY, R = 500, 460, 420          # plate disc centre + radius

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

BG_GRAD = lin(0, 0, 0, 1000, (0, "#101E14"), (1, "#050A06"))
PLATE_GRAD = rad((0, "#8FA88A"), (0.55, "#5F7A62"), (1, "#2E4434"))
FUR_GRAD = rad((0, "#3A3028"), (0.6, "#261E17"), (1, "#15100B"))
FUR_SIDE = lin(0, 300, 0, 860, (0, "#2C241D"), (1, "#120D09"))
SKIN_GRAD = rad((0, "#574A3E"), (0.6, "#3E332B"), (1, "#241C16"))
MUZZLE_GRAD = rad((0, "#5C4E42"), (0.7, "#453A30"), (1, "#2A211A"))
SILVER_GRAD = lin(0, 560, 0, 720, (0, "#C6CDD2"), (0.5, "#98A1A8"), (1, "#6A727A"))
FLOOR_GRAD = lin(0, 748, 0, 880, (0, "#3E5238"), (1, "#1E2E20"))
LEAF_GRAD = lin(0, 200, 0, 700, (0, "#233A28"), (1, "#101E14"))

def rim_x(y, r=R, side=-1):
    return CX + side * math.sqrt(r * r - (y - CY) ** 2)

def on_disc(x, y, pad=0, r=R):
    return math.hypot(x - CX, y - CY) <= r - pad

def mirror(dd):
    out, toks, ex = [], re.findall(r"[A-Za-z]|-?\d*\.?\d+", dd), True
    for t in toks:
        if t.isalpha():
            out.append(t); ex = True
        elif ex:
            out.append(f"{1000 - float(t):g},"); ex = False
        else:
            out[-1] += f"{float(t):g}"; ex = True
    return " ".join(out)

def pair(dd, label, **kw):
    d.path(dd, f"{label} L", **kw)
    d.path(mirror(dd), f"{label} R", **kw)

# --- backdrop + plate -------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
for i, (x, y, w) in enumerate([(150,130,4),(850,160,5),(60,420,4),(940,430,4),(120,840,4),(880,830,5),(55,640,3),(945,640,3)]):
    d.shape("ellipse", f"Backdrop fleck {i+1}", x=x, y=y, width=w, height=w, fill="#B8CCB4", opacity=25, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#1E3024", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8E6D4", strokeWidth=3, opacity=40)
# canopy gloom at the top of the disc
d.path(f"M{rim_x(150, side=-1):.1f},150 C340,120 660,120 {rim_x(150, side=1):.1f},150 "
       f"C780,220 220,220 {rim_x(150, side=-1):.1f},150 Z",
       "Canopy gloom", fill="#14241A", opacity=35, stroke=NONE)

# mist bands drifting through the plate (all ends well inside the rim)
for i, (x, y, w, h, o) in enumerate([(190,286,300,44,20),(520,240,260,36,16),
                                     (150,430,330,52,18),(560,470,300,46,16),
                                     (240,600,280,40,14),(620,640,220,36,13)]):
    d.shape("ellipse", f"Mist {i+1}", x=x, y=y, width=w, height=h, fill="#E4EEE2", opacity=o, stroke=NONE)
for i, (x, y, w) in enumerate([(220,340,90),(430,310,60),(690,350,80),(300,520,70),(620,540,90)]):
    d.path(f"M{x},{y} C{x + w*0.3},{y - 6} {x + w*0.7},{y - 6} {x + w},{y}",
           f"Mist wisp {i+1}", fill=NONE, stroke="#E4EEE2", strokeWidth=5, opacity=20, cap="round")

# leaf silhouettes leaning in from the rim (every point inside the disc)
def leaf(label, base, tip, width, op):
    bx, by = base; tx, ty = tip
    mx, my = (bx + tx) / 2, (by + ty) / 2
    nx, ny = -(ty - by), tx - bx
    ln = math.hypot(nx, ny) or 1
    nx, ny = nx / ln * width, ny / ln * width
    for p in [(mx + nx, my + ny), (mx - nx, my - ny), (tx, ty)]:
        assert on_disc(p[0], p[1], 30), (label, p)
    d.path(f"M{bx},{by} Q{mx + nx:.0f},{my + ny:.0f} {tx},{ty} "
           f"Q{mx - nx:.0f},{my - ny:.0f} {bx},{by} Z",
           label, fill=LEAF_GRAD, opacity=op, stroke=NONE)
    d.path(f"M{bx},{by} L{tx},{ty}", f"{label} vein", fill=NONE,
           stroke="#060B07", strokeWidth=2.5, opacity=op * 0.5, cap="round")

leaf("Leaf L1", (150, 480), (258, 372), 46, 70)
leaf("Leaf L2", (140, 560), (268, 520), 38, 60)
leaf("Leaf L3", (176, 360), (238, 268), 36, 55)
leaf("Leaf R1", (850, 470), (742, 366), 46, 70)
leaf("Leaf R2", (862, 552), (734, 512), 38, 60)
leaf("Leaf R3", (826, 350), (762, 262), 36, 55)

# moss floor: top edge sways, bottom closes on the disc's own arc
fy = 748
fl, fr = rim_x(fy, side=-1), rim_x(fy, side=1)
d.path(f"M{fl:.1f},{fy} C330,736 430,754 500,748 C580,742 680,740 {fr:.1f},{fy} "
       f"A{R},{R} 0 0 1 {fl:.1f},{fy} Z", "Moss floor", fill=FLOOR_GRAD, stroke=NONE)
for i, (x, y, w, h) in enumerate([(210,782,60,12),(430,806,80,14),(640,790,64,12),(320,830,56,10),(560,846,70,11),(740,820,46,9)]):
    d.shape("ellipse", f"Moss mound {i+1}", x=x, y=y, width=w, height=h, fill="#4E6A44", opacity=45, stroke=NONE)
for i, (x, y, w) in enumerate([(260,772,7),(380,786,6),(520,778,8),(660,774,7),(470,812,6),(720,796,6),(330,812,5),(600,800,6)]):
    d.shape("ellipse", f"Leaf litter {i+1}", x=x, y=y, width=w, height=w*0.6, fill="#6E8A5A", opacity=40, stroke=NONE)

# --- shoulders: the silverback mass, closing on the disc's own arc ----------------------
sy = 692
sl, sr = rim_x(sy, side=-1), rim_x(sy, side=1)
d.path(f"M{sl:.1f},{sy} C240,700 292,636 372,596 C410,576 590,576 628,596 "
       f"C708,636 760,700 {sr:.1f},{sy} A{R},{R} 0 0 1 {sl:.1f},{sy} Z",
       "Shoulders", fill=FUR_SIDE, stroke=NONE)
# shoulder-top contour strokes
pair(f"M{sl + 14:.1f},{sy - 4} C252,684 300,628 374,592", "Shoulder edge",
     fill=NONE, stroke=INK, strokeWidth=6, cap="round")
d.path(f"M{sl + 16:.1f},{sy - 10} C258,676 306,624 376,590", "Shoulder light L",
     fill=NONE, stroke="#98A1A8", strokeWidth=5, opacity=40, cap="round")
d.path("M624,590 C694,624 742,676 828,684", "Shoulder light R",
       fill=NONE, stroke="#98A1A8", strokeWidth=5, opacity=40, cap="round")
# the silver saddle: a sheen washing over the shoulder tops either side of the head
pair("M252,716 C268,656 316,610 380,590 C356,630 336,680 330,736 "
     "C300,736 272,728 252,716 Z",
     "Silver flank", fill=SILVER_GRAD, opacity=38, stroke=NONE)
for i, (x, y) in enumerate([(300,640),(322,622),(348,608),(652,608),(678,624),(700,644)]):
    d.path(f"M{x},{y} C{x + 5},{y + 14} {x + 7},{y + 30} {x + 4},{y + 48}",
           f"Silver strand {i+1}", fill=NONE, stroke="#DDE4E8", strokeWidth=3, opacity=35, cap="round")
# chest shadow + fur parting
d.path("M430,700 C450,740 458,780 460,830 M570,700 C550,740 542,780 540,830",
       "Chest parting", fill=NONE, stroke="#0C0806", strokeWidth=10, opacity=35, cap="round")
d.shape("ellipse", "Chest shade", x=418, y=690, width=164, height=140, fill="#0A0705", opacity=30, stroke=NONE)

# --- knuckles resting on the moss ------------------------------------------------------
pair("M306,772 C290,740 308,712 346,708 C384,704 412,724 414,756 "
     "C416,788 394,808 358,808 C326,808 310,796 306,772 Z",
     "Fist", fill=FUR_GRAD, stroke=INK, strokeWidth=5)
for j, x in enumerate([328, 352, 376]):
    pair(f"M{x},726 C{x - 4},744 {x - 4},762 {x + 2},778", f"Knuckle {j+1}",
         fill=NONE, stroke="#0E0A07", strokeWidth=4, opacity=60, cap="round")
pair("M322,720 C338,712 360,710 380,716", "Fist light", fill=NONE,
     stroke="#8A939B", strokeWidth=4, opacity=30, cap="round")

# --- ears (small, tucked against the dome) ---------------------------------------------
pair("M338,396 C312,382 290,398 294,428 C298,456 320,472 344,468 "
     "C354,444 352,416 338,396 Z",
     "Ear", fill=FUR_GRAD, stroke=INK, strokeWidth=5)
pair("M330,414 C316,412 308,424 312,440 C316,452 328,458 338,454",
     "Ear inner", fill=NONE, stroke="#4A3E34", strokeWidth=5, opacity=60, cap="round")

# --- head: crested dome, wide cheeks, heavy jaw -----------------------------------------
HEAD = ("M500,214 C540,216 576,230 606,256 C646,290 668,336 668,390 "
        "C688,414 690,458 676,494 C690,540 672,592 632,620 "
        "C598,644 550,656 500,656 C450,656 402,644 368,620 "
        "C328,592 310,540 324,494 C310,458 312,414 332,390 "
        "C332,336 354,290 394,256 C424,230 460,216 500,214 Z")
d.path(HEAD, "Head", fill=FUR_GRAD, stroke=INK, strokeWidth=7)
# sagittal dome sheen: a soft wash high on the crest, no band edge
d.shape("ellipse", "Dome sheen", x=400, y=240, width=200, height=96,
        fill="#9AA5AC", opacity=10, stroke=NONE)
for i, (x, y) in enumerate([(430,270),(452,254),(478,244),(548,246),(572,258)]):
    d.path(f"M{x},{y} C{x + 4},{y + 14} {x + 5},{y + 30} {x + 3},{y + 46}",
           f"Crown fur {i+1}", fill=NONE, stroke="#100B08", strokeWidth=3, opacity=40, cap="round")
# cheek ruff edges
pair("M348,470 C330,500 334,540 356,566", "Cheek edge", fill=NONE,
     stroke=INK, strokeWidth=5, opacity=70, cap="round")

# --- bare face mask ---------------------------------------------------------------------
d.path("M500,352 C548,352 588,376 606,416 C620,450 620,500 606,538 "
       "C590,584 550,614 500,616 C450,614 410,584 394,538 "
       "C380,500 380,450 394,416 C412,376 452,352 500,352 Z",
       "Face mask", fill=SKIN_GRAD, stroke=NONE)
# mask rim shadow where fur meets skin
pair("M398,412 C386,450 386,502 398,540", "Mask edge", fill=NONE,
     stroke="#16100B", strokeWidth=6, opacity=45, cap="round")
# temple hollows
pair("M406,400 C394,424 392,452 398,478", "Temple shade", fill=NONE,
     stroke="#191109", strokeWidth=10, opacity=30, cap="round")

# --- brow shelf over deep-set eyes ------------------------------------------------------
d.path("M402,428 C436,402 564,402 598,428 C604,442 596,452 578,454 "
       "C540,458 460,458 422,454 C404,452 396,442 402,428 Z",
       "Brow shelf", fill="#1A130E", opacity=88, stroke=NONE)
d.path("M408,424 C440,404 560,404 592,424", "Brow light", fill=NONE,
       stroke="#8A939B", strokeWidth=4, opacity=20, cap="round")
# under-brow shadow pooling over the eyes
d.shape("ellipse", "Eye shade", x=410, y=436, width=180, height=44, fill="#0E0A07", opacity=45, stroke=NONE)
# the still stare: small calm eyes under the shelf
pair("M428,462 C438,450 460,448 472,458 C466,472 442,476 428,462 Z",
     "Eye", fill="#241812", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Iris L", x=444, y=456, width=12, height=12, fill="#3E2415", stroke=NONE)
d.shape("ellipse", "Iris R", x=544, y=456, width=12, height=12, fill="#3E2415", stroke=NONE)
d.shape("ellipse", "Glint L", x=447, y=458, width=4, height=4, fill="#E8E2D4", opacity=80, stroke=NONE)
d.shape("ellipse", "Glint R", x=547, y=458, width=4, height=4, fill="#E8E2D4", opacity=80, stroke=NONE)
pair("M424,460 C436,446 462,444 476,456", "Upper lid", fill=NONE,
     stroke="#0C0805", strokeWidth=6, cap="round")
pair("M430,478 C444,486 462,486 472,478", "Lower lid crease", fill=NONE,
     stroke="#1C1410", strokeWidth=3, opacity=60, cap="round")

# --- broad flat nose --------------------------------------------------------------------
d.path("M500,468 C526,468 546,486 552,510 C558,534 544,556 500,558 "
       "C456,556 442,534 448,510 C454,486 474,468 500,468 Z",
       "Nose pad", fill=MUZZLE_GRAD, stroke=NONE)
d.path("M500,470 C522,470 540,486 546,508", "Nose bridge light", fill=NONE,
       stroke="#8E7C68", strokeWidth=4, opacity=35, cap="round")
# the big heart-shaped nostril pair
pair("M462,510 C458,494 474,486 488,492 C498,498 500,514 494,528 "
     "C486,542 468,540 464,526 C462,520 462,516 462,510 Z",
     "Nostril", fill="#0F0A07", stroke=INK, strokeWidth=3)
pair("M470,504 C476,498 486,498 490,506", "Nostril sheen", fill=NONE,
     stroke="#6A5A48", strokeWidth=3, opacity=50, cap="round")
d.path("M496,540 C498,552 498,562 496,572 M504,540 C502,552 502,562 504,572",
       "Philtrum", fill=NONE, stroke="#1A120D", strokeWidth=4, opacity=70, cap="round")

# --- wide stern mouth + heavy chin -------------------------------------------------------
d.path("M442,580 C470,592 530,592 558,580", "Mouth shadow", fill=NONE,
     stroke="#120C08", strokeWidth=9, opacity=50, cap="round")
d.path("M446,576 C474,588 526,588 554,576", "Mouth", fill=NONE,
     stroke="#0F0A07", strokeWidth=5, cap="round")
pair("M444,576 C434,578 426,584 422,592", "Mouth corner", fill=NONE,
     stroke="#0F0A07", strokeWidth=4, cap="round")
d.shape("ellipse", "Chin pad", x=460, y=600, width=80, height=30, fill="#564840", opacity=25, stroke=NONE)
d.path("M468,608 C486,616 514,616 532,608", "Chin crease", fill=NONE,
     stroke="#1A120D", strokeWidth=4, opacity=60, cap="round")

# --- name --------------------------------------------------------------------------------
d.text("GORILLA", "Name", x=500, y=962, size=60, font="Virelai Sans",
       color="#D8E4D2", justify="center")

d.finish("gorilla-V1R00")
