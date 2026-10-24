#!/usr/bin/env python3
"""Yeti — field-guide plate V1R00. Whiteout plate: an empty den under a rock
brow at the left horizon, a line of sunken tracks crossing the snow floor,
and the owner himself a low-contrast pale figure walking away right into
the blowing veils — home by habit, never there to ask. Himalayan plate,
whiteout mood. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Yeti — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420
INK = "#22303A"                    # cold dark ink, never pure black
SLATE = "#5E7684"

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

BG_GRAD = lin(0, 0, 0, 1000, (0, "#0A0E12"), (1, "#04070A"))
PLATE_GRAD = rad((0, "#E4EBEC"), (0.6, "#BCCDD3"), (1, "#7E96A0"))
SNOW_GRAD = lin(0, 716, 0, 880, (0, "#F2F5F4"), (0.6, "#D2DEE1"), (1, "#9DB2BA"))
FUR = lin(560, 280, 640, 720, (0, "#F2F4F1"), (0.5, "#D4DEE0"), (1, "#A8BCC2"))
TRACK = "#3E5260"

# --- backdrop + whiteout plate -----------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=64, y=24, width=872, height=872,
        fill="#BCCDD3", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#54686F", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F4F8F8", strokeWidth=3, opacity=45)

# the whiteout itself: broad veils stacking the upper sky
for i, (x, y, w, h, o) in enumerate([
        (140, 150, 700, 200, 20), (200, 320, 640, 170, 16),
        (120, 480, 720, 150, 14), (300, 90, 500, 160, 14)]):
    d.shape("ellipse", f"Whiteout {i+1}", x=x, y=y, width=w, height=h,
            fill="#FFFFFF", opacity=o, stroke=NONE)
# pale sun trying and failing
d.shape("ellipse", "Weak sun", x=640, y=150, width=140, height=130,
        fill=rad((0, "#FAFBF4", 45), (1, "#FAFBF4", 0)), stroke=NONE)

# far seracs — ice teeth nearly lost in the weather, right horizon
d.path("M726,712 L758,590 L792,712 Z", "Serac 1", fill="#AFC2C9",
       opacity=28, stroke=NONE)
d.path("M788,712 L820,620 L854,712 Z", "Serac 2", fill="#AFC2C9",
       opacity=20, stroke=NONE)
d.path("M676,712 L698,636 L722,712 Z", "Serac 3", fill="#AFC2C9",
       opacity=18, stroke=NONE)

# spindrift — wind-driven snow streaks, all raking one way
for i, (x1, y1, x2, y2) in enumerate([
        (820, 180, 690, 300), (760, 300, 620, 420), (700, 430, 580, 530),
        (400, 160, 280, 270), (320, 330, 190, 430), (860, 420, 740, 520)]):
    d.path(f"M{x1},{y1} L{x2},{y2}", f"Spindrift {i+1}", fill=NONE,
           stroke="#FFFFFF", strokeWidth=4, opacity=18, cap="round")
# falling snow
for i, (x, y, w, o) in enumerate([
        (240, 200, 5, 45), (400, 140, 4, 40), (560, 180, 5, 50),
        (720, 240, 4, 40), (820, 320, 5, 45), (180, 340, 4, 35),
        (340, 400, 5, 45), (520, 360, 4, 40), (660, 440, 5, 45),
        (790, 500, 4, 35), (260, 520, 4, 40), (450, 500, 5, 45),
        (600, 560, 4, 40), (360, 250, 3, 35), (540, 300, 4, 40)]):
    d.shape("ellipse", f"Snow {i+1}", x=x, y=y, width=w, height=w,
            fill="#FFFFFF", opacity=o, stroke=NONE)

# --- snow floor, closing on the disc's own arc ----------------------------------------
fy = 716
fl, fr = rim_x(fy, side=-1), rim_x(fy, side=1)
d.path(f"M{fl:.1f},{fy} C300,704 420,722 540,714 C660,706 770,710 {fr:.1f},{fy} "
       f"A{R},{R} 0 0 1 {fl:.1f},{fy} Z", "Snow floor", fill=SNOW_GRAD, stroke=NONE)
d.path(f"M{fl+6:.0f},{fy} C300,704 420,722 540,714 C660,706 770,710 {fr-6:.0f},{fy}",
       "Floor crest", fill=NONE, stroke="#FFFFFF", strokeWidth=6, opacity=55, cap="round")
# drift lines — wind-carved sastrugi on the floor
for i, dd in enumerate(["M240,760 C380,750 560,750 700,760",
                        "M300,800 C420,792 580,792 690,800",
                        "M380,838 C460,832 540,832 620,838"]):
    d.path(dd, f"Sastrugi {i+1}", fill=NONE, stroke="#AFC2C9",
           strokeWidth=4, opacity=50, cap="round")

# --- the empty den: nobody home --------------------------------------------------------
d.path("M164,{0} L164,668 C166,634 186,614 214,610 C240,608 258,622 262,650 "
       "L262,{0} Z".format(fy), "Den rock", fill="#6A7683", opacity=90, stroke=NONE)
d.path("M188,{0} L188,676 C188,656 200,646 216,646 C232,646 242,658 242,678 "
       "L242,{0} Z".format(fy), "Den mouth", fill="#232E38", stroke=NONE)
# snow cap on the brow
d.path("M164,668 C166,634 186,614 214,610 C240,608 258,622 262,650 "
       "C244,640 224,634 204,638 C186,642 172,654 164,668 Z",
       "Den snowcap", fill="#EDF2F2", opacity=85, stroke=NONE)

# --- the track line: sunken prints leaving the den, freshest nearest the figure ---------
def footprint(cx, cy, ang, scale, label, op):
    """Foreshortened print pressed into snow: dark sole + toe row."""
    t = math.radians(ang); c, s = math.cos(t), math.sin(t)
    def rot(px, py):
        return (cx + px*c - py*s, cy + px*s + py*c)
    w, h = 54*scale, 22*scale
    x0, y0 = rot(0, 0)
    d.shape("ellipse", f"{label} sole", x=x0 - w/2, y=y0 - h/2,
            width=w, height=h, fill=TRACK, opacity=op, stroke=NONE)
    for k in range(4):
        tx, ty = rot((k - 1.5) * w*0.24, -h*0.9)
        tr = 4.5*scale * (1 - k*0.14)
        d.shape("ellipse", f"{label} toe {k+1}", x=tx - tr, y=ty - tr*0.7,
                width=tr*2, height=tr*1.4, fill=TRACK, opacity=op-4, stroke=NONE)
    # bright lip where the foot pushed snow up on the far side
    lx, ly = rot(0, h*0.75)
    d.path(f"M{lx - w*0.4:.0f},{ly:.0f} C{lx - w*0.1:.0f},{ly + 4:.0f} "
           f"{lx + w*0.1:.0f},{ly + 4:.0f} {lx + w*0.4:.0f},{ly:.0f}",
           f"{label} lip", fill=NONE, stroke="#FFFFFF", strokeWidth=3,
           opacity=45, cap="round")

footprint(278, 704, -4, 0.80, "Print 1", 32)
footprint(360, 707, -6, 0.84, "Print 2", 40)
footprint(444, 710, -8, 0.88, "Print 3", 48)
footprint(524, 713, -10, 0.92, "Print 4", 56)

# contact shadow under the walker — faint, it barely presses the snow
d.shape("ellipse", "Contact shadow", x=560, y=706, width=180, height=14,
        fill="#3E5260", opacity=25, stroke=NONE)

# === the owner, barely home ==============================================================
# a breath of wind-blown ghost ahead of the body — weather wearing his shape
d.path("M600,300 C572,308 552,336 546,376 C538,430 548,490 568,546 "
       "C580,582 588,616 586,648 C608,662 644,656 666,630 "
       "C690,596 700,540 696,484 C692,428 682,378 664,338 "
       "C652,310 628,292 600,300 Z",
       "Whiteout echo", fill="#FFFFFF", opacity=14, stroke=NONE)

# rear leg trailing back-left, toe leaving the snow
d.path("M566,560 C540,588 518,622 506,658 C498,682 500,704 514,712 "
       "C528,720 544,710 550,694 C558,666 566,632 580,602 "
       "C588,582 584,564 566,560 Z",
       "Rear leg", fill="#B9C7CC", stroke=SLATE, strokeWidth=4)
d.path("M496,700 C480,704 466,714 462,728 C472,740 496,742 512,734 "
       "C520,726 518,712 508,704 C504,700 500,700 496,700 Z",
       "Rear foot", fill="#A8B8BF", stroke=SLATE, strokeWidth=4)

# torso: the big hunched mass, shoulders ahead of hips, facing right
d.path("M584,300 C554,308 534,338 528,380 C520,436 532,500 554,554 "
       "C566,590 574,624 572,652 C596,668 632,660 654,634 "
       "C678,600 688,544 684,486 C680,430 668,380 650,340 "
       "C638,314 614,294 584,300 Z",
       "Torso", fill=FUR, stroke=SLATE, strokeWidth=5)
# chest plane catching what little light there is
d.path("M640,380 C656,420 664,478 660,534 C672,500 676,444 668,398 "
       "C660,376 648,372 640,380 Z", "Chest light",
       fill="#FAFBF8", opacity=45, stroke=NONE)
# cold shade down the back
d.path("M548,380 C540,440 548,506 570,556", "Back shade", fill=NONE,
       stroke="#8CA0AA", strokeWidth=14, opacity=30, cap="round")
# fur fringe — ragged edges against the white
for i, (x1, y1, x2, y2) in enumerate([
        (530, 400, 520, 412), (526, 444, 516, 456), (532, 490, 520, 502),
        (542, 536, 530, 548), (556, 582, 544, 594), (684, 420, 694, 432),
        (688, 470, 698, 482), (686, 520, 696, 532)]):
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    d.path(f"M{x1},{y1} Q{mx + 4},{my} {x2},{y2}", f"Fur fringe {i+1}",
           fill=NONE, stroke="#8CA0AA", strokeWidth=4, opacity=55, cap="round")

# the long arm hanging ahead down the chest, knuckles low
d.path("M650,360 C676,384 692,426 696,474 C700,522 694,566 678,598 "
       "C668,616 646,616 638,598 C630,578 634,540 638,508 "
       "C642,466 640,418 630,386 C624,366 634,352 650,360 Z",
       "Arm", fill=lin(640, 360, 690, 610, (0, "#D4DEE0"), (1, "#9DB2BA")),
       stroke=SLATE, strokeWidth=5)
d.path("M640,596 C632,612 636,630 652,636 C668,642 684,632 684,616 "
       "C684,604 674,594 662,592 C652,590 646,590 640,596 Z",
       "Hand", fill="#9DB2BA", stroke=SLATE, strokeWidth=4)
for i in range(3):
    d.path(f"M{648 + i*10},632 q3,8 0,14", f"Finger {i+1}", fill=NONE,
           stroke=SLATE, strokeWidth=3.5, opacity=65, cap="round")

# head: dome sunk into the shoulders, face pushed out right
d.path("M578,288 C554,290 536,310 530,338 C524,368 530,398 548,416 "
       "C566,432 592,436 614,426 C636,416 650,394 652,368 "
       "C654,342 650,316 640,296 C632,276 618,264 602,264 "
       "C592,264 584,272 578,288 Z",
       "Head", fill=lin(540, 270, 640, 430, (0, "#EDF1EE"), (1, "#B4C4CA")),
       stroke=SLATE, strokeWidth=5)
# face plane turned into the weather
d.path("M604,336 C620,344 632,358 634,376 C636,394 630,410 618,418 "
       "C604,410 596,392 594,370 C592,356 596,342 604,336 Z",
       "Face", fill="#B8C4C8", opacity=85, stroke=NONE)
d.path("M606,358 C616,350 628,348 636,354", "Brow", fill=NONE,
       stroke=SLATE, strokeWidth=5, cap="round")
d.shape("ellipse", "Eye", x=614, y=364, width=11, height=12,
        fill="#22303A", stroke=NONE)
d.shape("ellipse", "Eye glint", x=616, y=366, width=3.5, height=3.5,
        fill="#FFFFFF", opacity=75, stroke=NONE)
# flat muzzle + breath cloud
d.path("M620,390 C630,396 634,406 630,416 C624,424 612,424 606,416 "
       "C602,408 604,396 612,392 C614,390 618,390 620,390 Z",
       "Muzzle", fill="#A8BCC4", stroke=SLATE, strokeWidth=3.5)
d.shape("ellipse", "Breath", x=648, y=396, width=44, height=26,
        fill="#FFFFFF", opacity=30, stroke=NONE)
# nape fur down the back of the skull
for i, dd in enumerate(["M570,306 C558,322 552,342 552,360",
                        "M596,300 C592,320 592,342 596,362"]):
    d.path(dd, f"Nape fur {i+1}", fill=NONE, stroke="#9DB2BA",
           strokeWidth=5, opacity=55, cap="round")

# shoulder shag bridging head to torso — no collar seam
for i, dd in enumerate([
        "M556,410 C560,432 570,452 584,466",
        "M584,424 C590,444 600,460 614,472",
        "M612,416 C622,434 632,448 644,458"]):
    d.path(dd, f"Shoulder shag {i+1}", fill=NONE, stroke="#C6D2D6",
           strokeWidth=8, opacity=60, cap="round")

# front leg planted mid-stride
d.path("M578,568 C566,608 560,654 562,694 C563,716 572,730 588,734 "
       "C604,738 618,726 618,706 C618,674 616,636 610,600 "
       "C604,574 594,560 578,568 Z",
       "Front leg", fill=FUR, stroke=SLATE, strokeWidth=5)
d.path("M562,706 C548,716 540,732 548,744 C562,754 590,756 610,750 "
       "C620,744 620,730 610,722 C596,712 578,706 562,706 Z",
       "Front foot", fill="#9DB2BA", stroke=SLATE, strokeWidth=4)
for i in range(4):
    d.path(f"M{552 + i*14},748 q6,5 14,3", f"Toe {i+1}", fill=NONE,
           stroke="#6E8390", strokeWidth=3.5, opacity=60, cap="round")
# belly fringe between the legs
for i, (x, y) in enumerate([(584, 636), (606, 652), (630, 646), (652, 626)]):
    d.path(f"M{x},{y} q-5,16 -13,26", f"Belly fringe {i+1}", fill=NONE,
           stroke="#8CA0AA", strokeWidth=4.5, opacity=50, cap="round")

# the whiteout taking him: veils drawn OVER the figure
d.shape("ellipse", "Veil shoulders", x=470, y=290, width=320, height=150,
        fill="#FFFFFF", opacity=20, stroke=NONE)
d.shape("ellipse", "Veil legs", x=470, y=560, width=330, height=130,
        fill="#FFFFFF", opacity=16, stroke=NONE)
d.shape("ellipse", "Veil head", x=560, y=250, width=200, height=110,
        fill="#FFFFFF", opacity=14, stroke=NONE)

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#3E545E", strokeWidth=6)

# --- name ---------------------------------------------------------------------------------
d.text("YETI", "Name", x=500, y=962, size=60, font="Virelai Sans",
       color="#E8F0F0", justify="center")

d.finish("yeti-V1R00")
