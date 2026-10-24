#!/usr/bin/env python3
"""Panther chameleon — field-guide plate V1R00. A mood ring the size of a
forearm: Madagascar plate, tangle mood. Profile on a gnarled branch —
casque helmet, turret eye, leaf-tall body banded teal and coral, the tail
curled into its signature spiral. Lianas and leaf shadows tangle the
plate. Forest floor closes on the disc's own arc. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Panther Chameleon — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420          # plate disc centre + radius
INK = "#1A2210"                    # warm dark ink, never pure black

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

def on_disc(x, y, pad=0, r=R):
    return math.hypot(x - CX, y - CY) <= r - pad

BG_GRAD = lin(0, 0, 0, 1000, (0, "#0E140C"), (1, "#050703"))
PLATE_GRAD = rad((0, "#C9D8A6"), (0.5, "#8AA268"), (1, "#465434"))
FLOOR_GRAD = lin(0, 720, 0, 880, (0, "#5E5630"), (0.6, "#37301C"), (1, "#191408"))
SKIN_GRAD = lin(430, 420, 590, 640, (0, "#5FBE9C"), (0.55, "#35805F"), (1, "#1E5240"))
CASQUE_GRAD = lin(660, 370, 730, 500, (0, "#6ECBA8"), (1, "#2E7355"))
STRIPE = "#F2EAD0"                 # the cream lateral band
BAND = "#C85A44"                   # coral bars — the mood ring reading
BRANCH = "#524026"

# --- backdrop + Madagascar plate --------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=64, y=24, width=872, height=872,
        fill="#8AA268", opacity=12, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#303C22", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E4EECC", strokeWidth=3, opacity=40)

# canopy light from upper left
d.shape("ellipse", "Canopy light", x=180, y=120, width=300, height=230,
        fill=rad((0, "#EDF4D0", 40), (1, "#EDF4D0", 0)), stroke=NONE)

# --- the tangle: lianas crossing, leaf shadows at the edges -------------------------
for i, dd in enumerate([
        "M140,140 C220,260 240,400 210,540 C200,590 208,640 230,680",
        "M760,110 C720,230 730,360 780,470 C800,514 806,560 796,600",
        "M400,80 C420,180 410,280 380,370"]):
    d.path(dd, f"Liana {i+1}", fill=NONE, stroke="#2C3C22",
           strokeWidth=6, opacity=55, cap="round")
# leaf silhouettes — pointed drops hung on the lianas
for i, (x, y, w, h, s) in enumerate([(196, 300, 34, 60, -0.3), (236, 470, 30, 54, 0.25),
                                     (768, 260, 36, 64, 0.3), (800, 480, 30, 56, -0.2),
                                     (396, 300, 30, 52, 0.15), (150, 420, 26, 46, -0.4),
                                     (830, 380, 28, 50, 0.35)]):
    tipx, tipy = x + w * s, y + h
    d.path(f"M{x},{y - h/2} C{x - w/2},{y + h*0.1} {tipx - 4},{tipy - 10} {tipx},{tipy} "
           f"C{tipx + 4},{tipy - 10} {x + w/2},{y + h*0.1} {x},{y - h/2} Z",
           f"Leaf {i+1}", fill="#3A4E2C", opacity=60, stroke=NONE)
# a spider-orchid hanging in the tangle — white star, small
d.path("M300,540 L306,552 L319,550 L310,560 L314,573 L300,566 L286,573 "
       "L290,560 L281,550 L294,552 Z", "Orchid", fill="#E8E4CC",
       opacity=70, stroke=NONE)

# --- forest floor, mostly shadow, closing on the disc's own arc --------------------
fy = 724
fl, fr = rim_x(fy, side=-1), rim_x(fy, side=1)
d.path(f"M{fl:.1f},{fy} C300,708 420,730 530,724 C640,718 730,716 {fr:.1f},{fy} "
       f"A{R},{R} 0 0 1 {fl:.1f},{fy} Z", "Forest floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{fl+8:.0f},{fy} C300,708 420,730 530,724 C640,718 730,716 {fr-8:.0f},{fy}",
       "Floor crest", fill=NONE, stroke="#9AA468", strokeWidth=5, opacity=35, cap="round")
for i, (x, y, w) in enumerate([(260, 764, 160), (640, 780, 200), (460, 800, 140)]):
    d.shape("ellipse", f"Leaf litter {i+1}", x=x - w/2, y=y, width=w, height=12,
            fill="#4A4226", opacity=40, stroke=NONE)

# --- the branch: gnarled diagonal the chameleon rides --------------------------------
d.path("M158,730 C290,706 420,676 540,654 C660,632 760,612 838,600",
       "Branch", fill=NONE, stroke=BRANCH, strokeWidth=17, cap="round")
d.path("M158,730 C290,706 420,676 540,654 C660,632 760,612 838,600",
       "Branch top light", fill=NONE, stroke="#8A7048", strokeWidth=5,
       opacity=55, cap="round")
d.path("M392,682 C376,668 368,650 372,634 M620,640 C636,624 640,606 634,592",
       "Branch twigs", fill=NONE, stroke=BRANCH, strokeWidth=7, cap="round")
d.shape("ellipse", "Branch knot", x=534, y=650, width=22, height=16,
        fill="#3A2C18", opacity=80, stroke=NONE)
# branch shadow pooled below
d.shape("ellipse", "Branch shadow", x=330, y=708, width=340, height=16,
        fill="#14180C", opacity=40, stroke=NONE)

# --- the chameleon --------------------------------------------------------------------
# tail: the prehensile spiral, curled tight at the rear
d.path("M416,540 C372,556 340,590 336,626 C332,664 360,694 398,692 "
       "C426,690 442,668 438,646 C434,628 416,618 398,624 "
       "C386,630 382,644 390,654",
       "Tail spiral", fill=NONE, stroke="#35805F", strokeWidth=16, cap="round")
d.path("M390,654 C394,660 402,660 406,654", "Tail tip", fill=NONE,
       stroke="#2A6A50", strokeWidth=9, cap="round")
# faint banding on the tail coil
for i, (x, y) in enumerate([(352, 600), (344, 640), (374, 676)]):
    d.path(f"M{x},{y} L{x+16},{y+10}", f"Tail band {i+1}", fill=NONE,
           stroke=BAND, strokeWidth=5, opacity=40, cap="round")

# far legs — dimmer, gripping the far side of the branch
d.path("M586,570 C600,594 606,622 604,648 C608,658 620,658 624,650 "
       "C626,622 620,592 606,566 C600,558 590,560 586,570 Z",
       "Front leg far", fill="#1E5240", stroke=INK, strokeWidth=4)
d.path("M470,584 C462,608 460,634 464,656 C460,664 470,670 478,664 "
       "C482,640 484,612 488,588 C486,578 474,576 470,584 Z",
       "Rear leg far", fill="#1E5240", stroke=INK, strokeWidth=4)

# body — leaf-tall, laterally compressed, deepest at mid-flank
d.path("M424,520 C428,486 448,458 482,444 C520,428 566,428 602,446 "
       "C634,462 650,494 650,528 C650,566 632,600 600,618 "
       "C562,638 508,640 470,624 C438,610 420,580 418,548 "
       "C417,538 419,528 424,520 Z",
       "Body", fill=SKIN_GRAD, stroke=INK, strokeWidth=6)
# dorsal crest: serrated ridge of teeth along the back
for i, (x, y) in enumerate([(452, 452), (480, 440), (508, 434), (536, 432), (564, 436)]):
    d.path(f"M{x},{y} L{x+7},{y-13} L{x+14},{y} Z",
           f"Spine {i+1}", fill="#2A6A50", stroke=INK, strokeWidth=2.5)
# the cream lateral stripe — the mood ring's neutral reading
d.path("M428,560 C470,540 560,536 632,552 C600,568 500,574 442,570 "
       "C432,568 428,564 428,560 Z", "Lateral stripe",
       fill=STRIPE, opacity=90, stroke=NONE)
# coral bars crossing the flank — the current mood
for i, (x, o) in enumerate([(466, 80), (512, 75), (558, 70), (600, 62)]):
    d.path(f"M{x},446 C{x-8},494 {x-10},540 {x-4},600",
           f"Mood bar {i+1}", fill=NONE, stroke=BAND,
           strokeWidth=13, opacity=o, cap="round")
# belly shadow where the body meets the legs
d.path("M452,600 C500,622 566,622 610,600 C580,622 500,630 462,614 "
       "C452,610 450,606 452,600 Z", "Belly shade", fill="#1E4634",
       opacity=50, stroke=NONE)

# near legs — thin bent limbs ending in clamp feet on the branch
d.path("M596,576 C610,598 618,624 616,650 C622,660 636,658 640,648 "
       "C640,620 632,592 616,570 C608,562 594,566 596,576 Z",
       "Front leg near", fill=SKIN_GRAD, stroke=INK, strokeWidth=5)
d.path("M612,646 C606,656 606,666 616,670 C626,672 636,666 638,656 "
       "C634,648 622,644 612,646 Z", "Front foot", fill="#2A6A50",
       stroke=INK, strokeWidth=4)
d.path("M440,560 C428,586 424,616 428,644 C424,654 434,662 444,656 "
       "C448,630 452,602 460,578 C458,566 446,554 440,560 Z",
       "Rear leg near", fill=SKIN_GRAD, stroke=INK, strokeWidth=5)
d.path("M424,648 C416,656 416,666 426,670 C436,672 446,666 448,656 "
       "C444,648 432,644 424,648 Z", "Rear foot", fill="#2A6A50",
       stroke=INK, strokeWidth=4)

# head + casque: the helmet rising off the back of the skull
d.path("M612,470 C622,438 644,406 678,390 C700,380 724,382 738,398 "
       "C750,412 754,432 750,452 C766,462 778,478 782,496 "
       "C784,510 776,520 762,522 C740,524 716,516 700,502 "
       "C680,504 656,500 640,490 C624,482 612,478 612,470 Z",
       "Head+casque", fill=CASQUE_GRAD, stroke=INK, strokeWidth=5)
# casque comb — serrated edge on the helmet peak
for i, (x, y) in enumerate([(668, 394), (692, 384), (716, 386)]):
    d.path(f"M{x},{y} L{x+8},{y-11} L{x+16},{y} Z",
           f"Casque tooth {i+1}", fill="#2A6A50", stroke=INK, strokeWidth=2.5)
# casque shading — the hollow behind the helmet
d.path("M640,440 C660,418 690,404 716,402 C694,418 672,438 660,462 "
       "C652,458 644,450 640,440 Z", "Casque shade",
       fill="#1E5240", opacity=45, stroke=NONE)
# pointed snout + mouth line back to the jaw
d.path("M742,468 C760,474 774,486 780,498 C776,506 764,508 752,504 "
       "C744,494 740,480 742,468 Z", "Snout", fill="#35805F",
       stroke=INK, strokeWidth=4)
d.path("M716,500 C736,508 758,510 774,504", "Mouth", fill=NONE,
       stroke="#14351F", strokeWidth=4, opacity=80, cap="round")
# the turret eye — a cone that reads its own weather
d.shape("ellipse", "Eye turret", x=698, y=440, width=42, height=40,
        fill=rad((0, "#7AD4B0"), (0.7, "#469678"), (1, "#2A6A50")),
        stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Eye", x=712, y=452, width=16, height=15,
        fill="#14180C", stroke=NONE)
d.shape("ellipse", "Eye glint", x=716, y=455, width=4, height=4,
        fill="#FFF6DC", opacity=85, stroke=NONE)
# nose
d.shape("ellipse", "Nostril", x=764, y=486, width=7, height=5,
        fill="#14351F", opacity=80, stroke=NONE)
# throat fan — pale wedge under the jaw
d.path("M668,492 C686,510 710,522 734,526 C716,530 690,524 672,508 "
       "C664,502 662,496 668,492 Z", "Throat fan", fill=STRIPE,
       opacity=70, stroke=NONE)

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#222E18", strokeWidth=6)

# --- name ---------------------------------------------------------------------------
d.text("PANTHER CHAMELEON", "Name", x=500, y=962, size=54, font="Virelai Sans",
       color="#DCE8C2", justify="center")

d.finish("panther-chameleon-V1R00")
