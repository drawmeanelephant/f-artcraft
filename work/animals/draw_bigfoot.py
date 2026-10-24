#!/usr/bin/env python3
"""Bigfoot — field-guide plate V1R00. Pine-forest plate, footprint mood: the
figure caught mid-stride between the trunks, shaggy umber mass hunched
forward, one long arm swinging, a trail of pressed prints in the needle
floor behind it — seen everywhere, photographed nowhere, so the edges sit
in mist. Moon glow through the pines. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math, re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Bigfoot — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420          # plate disc centre + radius
INK = "#180E08"                    # warm dark ink, never pure black

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rim_x(y, r=R, side=-1):
    return CX + side * math.sqrt(r * r - (y - CY) ** 2)

def on_disc(x, y, pad=0, r=R):
    return math.hypot(x - CX, y - CY) <= r - pad

def pine(x, base_y, w, h, label, color, op):
    """Conifer silhouette: stacked scalloped tiers on a trunk."""
    d.path(f"M{x - 5},{base_y} L{x - 5},{base_y - h*0.28} "
           f"L{x + 5},{base_y - h*0.28} L{x + 5},{base_y} Z",
           f"{label} trunk", fill=color, opacity=op, stroke=NONE)
    for k in range(4):
        ty = base_y - h*0.22 - k*h*0.20
        tw = w * (1 - k*0.22)
        d.path(f"M{x - tw},{ty + h*0.16} Q{x - tw*0.5},{ty - h*0.06} {x},{ty - h*0.14} "
               f"Q{x + tw*0.5},{ty - h*0.06} {x + tw},{ty + h*0.16} "
               f"Q{x},{ty + h*0.08} {x - tw},{ty + h*0.16} Z",
               f"{label} tier {k+1}", fill=color, opacity=op, stroke=NONE)

BG_GRAD = lin(0, 0, 0, 1000, (0, "#0B120C"), (1, "#040704"))
PLATE_GRAD = rad((0, "#6E8470"), (0.5, "#3C5244"), (1, "#14221A"))
FLOOR_GRAD = lin(0, 700, 0, 880, (0, "#46584A"), (0.6, "#2A3A30"), (1, "#141E18"))
FUR = lin(430, 280, 520, 700, (0, "#6B4526"), (0.55, "#4A2E18"), (1, "#2A180C"))
FUR_DARK = "#2A180C"

# --- backdrop + forest plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=64, y=24, width=872, height=872,
        fill="#3C5244", opacity=12, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#0E1C14", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C4D4BC", strokeWidth=3, opacity=35)

# moon + glow, high left behind the pines
d.shape("ellipse", "Moon glow", x=240, y=140, width=300, height=280,
        fill="#D8E4C8", opacity=16, stroke=NONE)
d.shape("ellipse", "Moon", x=330, y=190, width=110, height=110,
        fill=rad((0, "#F0F2DC"), (1, "#C4CCA8")), opacity=90, stroke=NONE)
d.shape("ellipse", "Moon shade", x=352, y=206, width=60, height=60,
        fill="#A8B490", opacity=35, stroke=NONE)

# far treeline — soft, low opacity
for i, (x, w, h) in enumerate([(180, 46, 210), (260, 40, 190), (350, 44, 200),
                               (620, 42, 195), (710, 46, 215), (800, 40, 185)]):
    pine(x, 700, w, h, f"Far pine {i+1}", "#223428", 55)
# mist band across the far treeline
for i, (x, y, w, h, o) in enumerate([(160, 560, 700, 60, 18), (200, 620, 620, 48, 14)]):
    d.shape("ellipse", f"Mist {i+1}", x=x, y=y, width=w, height=h,
            fill="#C4D4BC", opacity=o, stroke=NONE)
# near pines framing the figure — darker, at the sides
for i, (x, w, h) in enumerate([(168, 60, 330), (830, 64, 350), (240, 52, 300), (762, 54, 310)]):
    pine(x, 760, w, h, f"Near pine {i+1}", "#16241A", 85)

# --- needle floor closing on the disc's own arc --------------------------------------
fy = 730
fl, fr = rim_x(fy, side=-1), rim_x(fy, side=1)
d.path(f"M{fl:.1f},{fy} C300,714 400,738 500,728 C600,718 700,724 {fr:.1f},{fy} "
       f"A{R},{R} 0 0 1 {fl:.1f},{fy} Z", "Needle floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{fl+8:.0f},{fy} C300,714 400,738 500,728 C600,718 700,724 {fr-8:.0f},{fy}",
       "Floor crest", fill=NONE, stroke="#7C9078", strokeWidth=5, opacity=45, cap="round")
# fallen needles — short strokes scattered on the floor
for i, (x, y, a) in enumerate([(250, 760, -20), (310, 780, 15), (390, 762, -30),
                               (470, 786, 10), (560, 770, -15), (640, 792, 25),
                               (720, 768, -25), (350, 812, 20), (520, 820, -10),
                               (660, 830, 15), (430, 842, -20)]):
    dx, dy = math.cos(math.radians(a)) * 14, math.sin(math.radians(a)) * 14
    d.path(f"M{x - dx:.0f},{y - dy:.0f} L{x + dx:.0f},{y + dy:.0f}",
           f"Needle {i+1}", fill=NONE, stroke="#5A7060", strokeWidth=3,
           opacity=50, cap="round")

# --- the footprint trail: flat prints pressed into the needle floor -------------------
def footprint(cx, cy, ang, scale, label, op):
    """Foreshortened print lying on the floor plane: wide flat sole, toe row."""
    t = math.radians(ang); c, s = math.cos(t), math.sin(t)
    def rot(px, py):
        return (cx + px*c - py*s, cy + px*s + py*c)
    w, h = 58*scale, 24*scale
    x0, y0 = rot(0, 0)
    d.shape("ellipse", f"{label} sole", x=x0 - w/2, y=y0 - h/2,
            width=w, height=h, fill="#120A06", opacity=op, stroke=NONE)
    hx, hy = rot(0, h*0.5)
    d.shape("ellipse", f"{label} heel", x=hx - w*0.34, y=hy - h*0.3,
            width=w*0.68, height=h*0.6, fill="#120A06", opacity=op-8, stroke=NONE)
    for k in range(4):
        tx, ty = rot((k - 1.5) * w*0.24, -h*0.72)
        tr = 5*scale * (1 - k*0.14)
        d.shape("ellipse", f"{label} toe {k+1}", x=tx - tr, y=ty - tr*0.7,
                width=tr*2, height=tr*1.4, fill="#120A06",
                opacity=op-4, stroke=NONE)

# alternating prints trailing behind the walker, older ones fainter
footprint(612, 776, -10, 0.95, "Print 1", 58)
footprint(700, 762, -16, 0.84, "Print 2", 48)
footprint(772, 744, -20, 0.72, "Print 3", 40)

# --- the figure, hunched mid-stride facing left ----------------------------------------
# soft mist-echo of the body — the photographed-nowhere blur
d.path("M420,290 C384,296 358,326 350,368 C340,424 352,484 374,538 "
       "C388,574 396,612 394,646 C416,662 452,658 474,634 "
       "C500,602 510,544 506,486 C502,428 494,368 478,322 "
       "C466,292 444,282 420,290 Z",
       "Mist echo", fill="#8CA088", opacity=12, stroke=NONE)

# rear leg trailing back and down, toe just leaving the floor
d.path("M492,520 C534,540 574,570 600,608 C618,636 626,664 620,688 "
       "C614,706 594,710 580,698 C562,682 552,650 538,622 "
       "C524,592 506,558 492,520 Z",
       "Rear leg", fill=FUR_DARK, stroke=INK, strokeWidth=5)
d.path("M606,676 C628,674 652,682 662,696 C654,712 630,716 612,708 "
       "C602,702 600,688 606,676 Z", "Rear foot", fill=FUR_DARK,
       stroke=INK, strokeWidth=4)

# torso: the big shaggy mass leaning into the walk — shoulders ahead of hips
d.path("M414,288 C374,296 346,332 338,380 C328,440 342,502 366,554 "
       "C382,590 390,622 388,652 C414,668 452,662 476,636 "
       "C502,602 512,542 508,482 C504,422 494,362 476,320 "
       "C462,292 438,280 414,288 Z",
       "Torso", fill=FUR, stroke=INK, strokeWidth=7)
# belly shading and moonlit back sheen
d.path("M364,372 C354,432 366,502 392,552", "Belly shade", fill=NONE,
       stroke="#241408", strokeWidth=18, opacity=30, cap="round")
d.path("M448,300 C472,340 488,400 494,460", "Back sheen", fill=NONE,
       stroke="#9C8058", strokeWidth=9, opacity=28, cap="round")
# fur fringe along the silhouette edges
for i, (x1, y1, x2, y2) in enumerate([
        (346, 390, 336, 402), (340, 432, 330, 444), (344, 478, 332, 490),
        (354, 524, 342, 536), (368, 570, 356, 582), (382, 616, 370, 628),
        (492, 390, 502, 402), (500, 436, 510, 448), (504, 484, 514, 496),
        (502, 536, 512, 548)]):
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    d.path(f"M{x1},{y1} Q{mx - 4},{my} {x2},{y2}", f"Fur fringe {i+1}",
           fill=NONE, stroke=INK, strokeWidth=4, opacity=60, cap="round")

# the long arm swinging ahead of the body, hanging past the hip
d.path("M380,352 C350,378 332,420 328,468 C324,516 332,560 350,594 "
       "C360,614 384,616 394,598 C404,578 400,540 396,508 "
       "C392,464 394,414 408,380 C414,360 398,344 380,352 Z",
       "Arm", fill=lin(328, 352, 400, 610, (0, "#5A3A20"), (1, "#2E1A0C")),
       stroke=INK, strokeWidth=6)
# long hand, knuckles brushing low
d.path("M348,592 C342,610 346,628 364,634 C380,640 394,630 394,614 "
       "C394,602 384,592 372,590 C362,588 354,588 348,592 Z",
       "Hand", fill="#2E1A0C", stroke=INK, strokeWidth=4)
for i in range(3):
    d.path(f"M{358 + i*10},630 q2,8 -1,14", f"Finger {i+1}", fill=NONE,
           stroke=INK, strokeWidth=3.5, opacity=70, cap="round")

# head sunk into the shoulders, face pushed forward — the no-neck silhouette,
# skull sweeping up to the sagittal peak at the back-top in one outline
d.path("M402,284 C372,286 348,306 338,336 C328,368 332,400 350,422 "
       "C366,442 394,448 418,438 C442,428 458,402 460,370 "
       "C462,342 460,316 452,296 C446,272 434,258 416,256 "
       "C404,254 396,258 390,266 C382,272 374,282 402,284 Z",
       "Head", fill=lin(350, 256, 390, 442, (0, "#6B4526"), (1, "#3A2210")),
       stroke=INK, strokeWidth=6)
# crest fur strokes following the peak down the nape
d.path("M398,272 C408,260 424,256 438,262 M392,284 C402,276 416,272 430,276",
       "Peak fur", fill=NONE, stroke="#4A2E18", strokeWidth=5,
       opacity=60, cap="round")
# face plane in profile — darker, projecting forward-left
d.path("M356,344 C340,352 330,368 330,386 C330,404 340,418 356,424 "
       "C368,412 372,390 370,368 C368,356 363,348 356,344 Z",
       "Face", fill="#3A2210", stroke=INK, strokeWidth=4)
# heavy brow over a deep-set eye
d.path("M336,360 C348,352 362,350 372,356", "Brow", fill=NONE,
       stroke=INK, strokeWidth=6, cap="round")
d.shape("ellipse", "Eye", x=342, y=366, width=12, height=14,
        fill="#0E0805", stroke=NONE)
d.shape("ellipse", "Eye glint", x=344, y=368, width=4, height=4,
        fill="#D8E4C8", opacity=70, stroke=NONE)
# flat muzzle in profile
d.path("M332,390 C324,396 320,406 324,416 C330,424 342,426 350,420 "
       "C354,410 352,398 344,392 C340,388 336,388 332,390 Z",
       "Muzzle", fill="#2E1A0C", stroke=INK, strokeWidth=3.5)
# nape fur strokes down the back of the head
for i, dd in enumerate(["M384,302 C370,316 362,336 360,356",
                        "M412,306 C404,326 400,346 402,366",
                        "M438,318 C436,340 438,360 444,378"]):
    d.path(dd, f"Nape fur {i+1}", fill=NONE, stroke="#2A180C",
           strokeWidth=6, opacity=55, cap="round")

# front leg planted mid-stride, knee soft
d.path("M430,560 C418,602 410,650 412,694 C413,718 422,734 438,738 "
       "C456,742 470,730 470,710 C470,676 468,634 462,598 "
       "C456,572 444,556 430,560 Z",
       "Front leg", fill=FUR, stroke=INK, strokeWidth=6)
# flat bare foot planted ahead on the floor
d.path("M408,710 C394,720 386,736 394,748 C408,758 436,760 456,754 "
       "C466,748 466,734 456,726 C442,716 424,710 408,710 Z",
       "Front foot", fill="#2E1A0C", stroke=INK, strokeWidth=5)
for i in range(4):
    d.path(f"M{398 + i*13},752 q6,5 14,3", f"Toe {i+1}", fill=NONE,
           stroke="#0E0805", strokeWidth=4, opacity=70, cap="round")
# shaggy belly fringe hanging between the legs
for i, (x, y) in enumerate([(410, 632), (432, 650), (456, 644), (480, 624)]):
    d.path(f"M{x},{y} q-4,16 -12,26", f"Belly fringe {i+1}", fill=NONE,
           stroke=INK, strokeWidth=5, opacity=55, cap="round")

# low mist drifting across the figure's feet — the never-quite-seen haze
d.shape("ellipse", "Ground mist", x=280, y=700, width=440, height=54,
        fill="#C4D4BC", opacity=12, stroke=NONE)

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#0A140E", strokeWidth=6)

# --- name ---------------------------------------------------------------------------
d.text("BIGFOOT", "Name", x=500, y=962, size=58, font="Virelai Sans",
       color="#D4E0CC", justify="center")

d.finish("bigfoot-V1R00")
