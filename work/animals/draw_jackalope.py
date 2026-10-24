#!/usr/bin/env python3
"""Jackalope — field-guide plate V1R00. A sitting jackrabbit in profile
facing left, tall ears, and between them the little branching antlers no
rabbit should have. Above the horizon a faint upside-down twin floats in
the heat — the superior mirage every tall tale deserves. Sagebrush plate,
mirage mood. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Jackalope — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420
INK = "#241A0C"                    # warm dark ink, never pure black
BONE = "#D8C4A0"

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    ss = []
    for s in stops:
        st = {"offset": s[0], "color": s[1]}
        if len(s) > 2: st["opacity"] = s[2]
        ss.append(st)
    return {"gradient": {"kind": "radial", "stops": ss}}

def rim_x(y, r=R, side=-1):
    return CX + side * math.sqrt(r * r - (y - CY) ** 2)

def antler(dd, label, o=95):
    """Antler stroke: dark edge under, bone over — two passes."""
    d.path(dd, f"{label} edge", fill=NONE, stroke=INK, strokeWidth=8,
           opacity=o, cap="round")
    d.path(dd, label, fill=NONE, stroke=BONE, strokeWidth=5.5,
           opacity=o, cap="round")

BG_GRAD = lin(0, 0, 0, 1000, (0, "#1A130C"), (1, "#090604"))
PLATE_GRAD = rad((0, "#DAD7AC"), (0.6, "#A3A06E"), (1, "#5E5A38"))
EARTH_GRAD = lin(0, 720, 0, 880, (0, "#C9B98E"), (0.55, "#7E6A48"), (1, "#3E321F"))
FUR_GRAD = rad((0, "#B8A88E"), (0.55, "#8E7C62"), (1, "#584734"))
FUR_DARK = "#5E4E38"
SAGE = "#5E6A4E"

# --- backdrop + sagebrush plate ----------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#A3A06E", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#4A4630", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#EAE6CC", strokeWidth=3, opacity=45)

# pale sun-disc high in the heat
d.shape("ellipse", "Sun glow", x=620, y=150, width=200, height=180,
        fill=rad((0, "#F4EDD0", 35), (1, "#F4EDD0", 0)), stroke=NONE)
d.shape("ellipse", "Sun", x=662, y=186, width=120, height=110,
        fill="#F4EDD0", opacity=30, stroke=NONE)

# heat shimmer bands wriggling across the sky
for i, dd in enumerate([
        "M180,300 C260,290 300,310 380,300 C460,290 540,308 620,300 C680,294 740,302 810,296",
        "M220,390 C300,382 360,398 440,390 C520,382 600,398 680,390",
        "M160,500 C240,492 320,506 400,498 C480,490 560,504 640,496 C700,492 760,498 830,494"]):
    d.path(dd, f"Shimmer {i+1}", fill=NONE, stroke="#E8E0BC",
           strokeWidth=5, opacity=15, cap="round")

# the mirage twin: a faint upside-down jackalope floating over the horizon
d.path("M258,272 C292,260 328,264 344,288 C352,306 348,328 332,342 "
       "C316,354 294,358 274,352 C254,344 242,328 242,308 "
       "C242,290 248,276 258,272 Z",
       "Mirage body", fill="#D8CBB0", opacity=12, stroke=NONE)
# its ears and antlers point down
d.path("M272,354 C268,378 270,400 278,416 C284,422 292,420 294,412 "
       "C290,394 288,374 288,356 Z", "Mirage ear 1",
       fill="#D8CBB0", opacity=12, stroke=NONE)
d.path("M298,356 C298,380 304,400 314,414 C320,418 326,414 326,406 "
       "C320,390 314,372 312,354 Z", "Mirage ear 2",
       fill="#D8CBB0", opacity=12, stroke=NONE)
d.path("M304,358 C310,378 320,392 334,400 M312,368 C320,382 330,392 342,396",
       "Mirage antler", fill=NONE, stroke="#D8CBB0", strokeWidth=4,
       opacity=12, cap="round")
# shimmer slicing through the ghost
d.path("M234,316 C272,310 310,320 350,314", "Mirage shimmer 1", fill=NONE,
       stroke="#E8E0BC", strokeWidth=5, opacity=20, cap="round")
d.path("M246,346 C280,340 314,350 348,344", "Mirage shimmer 2", fill=NONE,
       stroke="#E8E0BC", strokeWidth=4, opacity=16, cap="round")

# low mesa silhouette on the left horizon
d.path("M150,712 L178,662 L262,662 L286,692 L340,692 L356,712 Z",
       "Mesa", fill="#8A7A58", opacity=38, stroke=NONE)
# drifting dust
for i, (x, y, w) in enumerate([(640,300,5),(760,220,4),(420,240,4),(840,360,5),
                               (560,160,4),(180,420,4),(700,440,5)]):
    d.shape("ellipse", f"Dust {i+1}", x=x, y=y, width=w, height=w,
            fill="#EDE4C4", opacity=35, stroke=NONE)

# --- cracked dry floor, closing on the disc's own arc ---------------------------------
fy = 722
fl, fr = rim_x(fy, side=-1), rim_x(fy, side=1)
d.path(f"M{fl:.1f},{fy} C320,710 440,726 560,718 C680,710 770,714 {fr:.1f},{fy} "
       f"A{R},{R} 0 0 1 {fl:.1f},{fy} Z", "Floor", fill=EARTH_GRAD, stroke=NONE)
d.path(f"M{fl+6:.0f},{fy} C320,710 440,726 560,718 C680,710 770,714 {fr-6:.0f},{fy}",
       "Floor crest", fill=NONE, stroke="#D8CBA0", strokeWidth=5, opacity=40, cap="round")
# the false water: a cool pale band hovering just on the crest — the mirage's promise
d.path("M250,706 C400,696 600,696 760,706 C600,714 400,714 250,706 Z",
       "False water", fill="#C8D6D4", opacity=28, stroke=NONE)
d.path("M300,702 C420,696 580,696 706,702", "Water sheen", fill=NONE,
       stroke="#E4EDE8", strokeWidth=3.5, opacity=30, cap="round")
# earth cracks
for i, dd in enumerate(["M300,780 L360,794 L420,786", "M560,792 L640,780 L710,790",
                        "M400,838 L470,828 L540,840", "M220,806 L270,796"]):
    d.path(dd, f"Crack {i+1}", fill=NONE, stroke="#5E4A30",
           strokeWidth=3.5, opacity=45, cap="round")

# sagebrush clumps: twiggy strokes + leaf dots, floor edges
def sage(x, y, s, label):
    for j, (dx, dy) in enumerate([(-22, -34), (-10, -44), (2, -40), (14, -36),
                                  (-4, -28), (10, -26), (-16, -24)]):
        d.path(f"M{x},{y} Q{x + dx*0.5},{y + dy*0.6} {x + dx*s},{y + dy}",
               f"{label} twig {j+1}", fill=NONE, stroke=SAGE,
               strokeWidth=4, opacity=75, cap="round")
    for j, (dx, dy, w) in enumerate([(-20, -38, 8), (-8, -48, 9), (4, -44, 8),
                                     (16, -40, 8), (-2, -32, 7), (12, -30, 7)]):
        d.shape("ellipse", f"{label} leaf {j+1}", x=x + dx*s - w/2, y=y + dy - w/2,
                width=w, height=w, fill="#7A885E", opacity=70, stroke=NONE)

sage(206, 712, 1, "Sage L")
sage(800, 706, -1, "Sage R")
sage(700, 722, 1, "Sage back")

# contact shadow under the sitter
d.shape("ellipse", "Contact shadow", x=360, y=704, width=270, height=16,
        fill="#14100A", opacity=40, stroke=NONE)

# === the animal ======================================================================
# --- far ear behind everything --------------------------------------------------------
d.path("M424,368 C420,322 424,274 438,238 C448,214 464,206 476,216 "
       "C486,226 486,250 478,276 C468,312 452,348 442,370 Z",
       "Ear far", fill="#7A6850", stroke=INK, strokeWidth=4)

# --- body: the sitting pear -------------------------------------------------------------
d.path("M400,470 C370,500 350,550 348,610 C346,660 360,696 390,712 "
       "C420,724 500,726 550,714 C586,704 604,682 600,650 "
       "C594,610 570,568 538,532 C508,498 466,472 430,464 "
       "C418,462 408,464 400,470 Z",
       "Body", fill=FUR_GRAD, stroke=INK, strokeWidth=6)
# haunch light + belly
d.path("M420,560 C440,610 480,660 540,692 C500,700 440,694 410,660 "
       "C390,634 388,596 420,560 Z", "Haunch light",
       fill="#C9BBA0", opacity=35, stroke=NONE)
d.path("M372,540 C380,600 404,660 444,700 C410,692 380,664 366,624 "
       "C356,592 358,562 372,540 Z", "Chest light",
       fill="#D8CBB0", opacity=22, stroke=NONE)
# rump puff
d.shape("ellipse", "Tail puff", x=592, y=606, width=30, height=34,
        fill="#E8E0CC", opacity=80, stroke=INK, strokeWidth=3)
# the long hind foot planted ahead
d.path("M392,696 C440,702 500,706 542,702 C558,700 566,706 560,714 "
       "C550,722 502,726 458,724 C424,722 396,714 392,696 Z",
       "Hind foot", fill=FUR_GRAD, stroke=INK, strokeWidth=5)
d.path("M540,704 L562,712 M528,710 L548,718", "Foot toes", fill=NONE,
       stroke=INK, strokeWidth=3.5, opacity=60, cap="round")
# slim forelegs down the chest
d.path("M396,556 C390,598 388,648 392,692 L410,692 C408,648 410,602 418,564 "
       "C412,554 402,552 396,556 Z", "Foreleg near",
       fill="#9A8A70", stroke=INK, strokeWidth=4)
d.path("M414,570 C412,608 412,650 416,686 L428,686 C426,648 428,608 432,578 "
       "C426,570 420,568 414,570 Z", "Foreleg far",
       fill="#6E5C44", stroke=INK, strokeWidth=3.5)

# --- head -------------------------------------------------------------------------------
d.path("M396,372 C366,378 344,398 334,424 C328,442 330,458 342,466 "
       "C356,474 376,472 392,462 C412,450 428,428 434,404 "
       "C438,388 434,376 422,370 C414,366 404,368 396,372 Z",
       "Head", fill=lin(430, 380, 335, 465, (0, "#B8A88E"), (0.6, "#8E7C62"), (1, "#6A5840")),
       stroke=INK, strokeWidth=5)
# cheek light + jaw
d.shape("ellipse", "Cheek light", x=350, y=430, width=46, height=30,
        fill="#D8CBB0", opacity=35, stroke=NONE)
# nose: the cleft tip
d.path("M334,426 C328,434 328,444 334,450 C342,452 350,448 352,440 "
       "C352,432 344,426 334,426 Z", "Nose", fill="#4A3826",
       stroke=INK, strokeWidth=3)
d.path("M342,450 C346,458 354,462 364,460", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=3.5, opacity=70, cap="round")
# whiskers — >=3pt or they vanish at plate scale
for i, (x2, y2) in enumerate([(294, 428), (296, 444), (300, 458)]):
    d.path(f"M336,{436 + i*4} C320,{438 + i*4} {x2+8},{y2-4} {x2},{y2}",
           f"Whisker {i+1}", fill=NONE, stroke="#E8E0CC",
           strokeWidth=3, opacity=70, cap="round")
# eye: dark, calm, a little too knowing
d.shape("ellipse", "Eye socket", x=368, y=408, width=30, height=24,
        fill="#241A0C", opacity=35, stroke=NONE)
d.shape("ellipse", "Eye", x=376, y=412, width=16, height=15,
        fill="#140C06", stroke=NONE)
d.shape("ellipse", "Eye glint", x=380, y=415, width=5, height=5,
        fill="#FFEDC8", opacity=85, stroke=NONE)
d.path("M368,406 C380,398 398,398 410,406", "Brow", fill=NONE,
       stroke=INK, strokeWidth=4, opacity=60, cap="round")

# --- near ear: tall, tipped --------------------------------------------------------------
d.path("M398,372 C388,320 386,266 396,224 C402,198 418,186 434,194 "
       "C448,202 452,226 446,254 C438,294 422,336 412,370 Z",
       "Ear near", fill=FUR_GRAD, stroke=INK, strokeWidth=5)
d.path("M406,352 C398,310 398,266 406,232 C412,212 424,204 434,212 "
       "C442,220 442,242 436,266 C428,300 418,330 412,352 Z",
       "Inner ear", fill="#C9A88E", opacity=75, stroke=NONE)
d.path("M398,238 C402,214 412,198 428,192", "Ear rim light", fill=NONE,
       stroke="#E8E0CC", strokeWidth=4, opacity=50, cap="round")
# the dark ear tip
d.path("M394,236 C398,208 410,190 430,186 C424,210 412,228 394,236 Z",
       "Ear tip", fill=FUR_DARK, opacity=85, stroke=NONE)

# --- the antlers: the tall tale made keratin ------------------------------------------------
# far antler, darker and smaller
for dd, w in [("M418,360 C410,330 402,304 392,284", 7),
              ("M408,322 C396,312 384,304 372,300", 5.5),
              ("M398,296 C390,286 384,274 382,262", 5.5)]:
    d.path(dd, "Antler far", fill=NONE, stroke="#8A6E48",
           strokeWidth=w, opacity=85, cap="round")
# near antler: beam curving up-forward with three tines
antler("M392,368 C378,336 360,306 342,282 C334,270 328,258 326,244",
       "Antler near beam")
antler("M376,330 C362,318 348,310 332,304", "Antler near tine 1")
antler("M358,298 C348,286 342,274 340,260", "Antler near tine 2")
antler("M346,272 C340,260 338,248 340,236", "Antler near tine 3")

# a scatter of fur ticks on the flank
for i, (x, y, l) in enumerate([(470, 560, 12), (510, 590, 10), (490, 630, 11),
                               (540, 650, 10), (450, 590, 9)]):
    d.path(f"M{x},{y} l{l},{l//3}", f"Fur tick {i+1}", fill=NONE,
           stroke="#584734", strokeWidth=3.5, opacity=45, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#3E3A26", strokeWidth=6)

# --- name ---------------------------------------------------------------------------------
d.text("JACKALOPE", "Name", x=500, y=962, size=60, font="Virelai Sans",
       color="#E8E4CC", justify="center")

d.finish("jackalope-V1R00")
