#!/usr/bin/env python3
"""Komodo dragon — field-guide plate V1R00. A dragon in everything but
breath: monsoon-forest plate, carrion-wind mood. Long low profile walking
right, belly half-dragging, bowed legs, forked tongue tasting the air, the
tail curling back around a stripped ribcage it already finished. Mist
between the trunks, wet leaf-litter floor closing on the disc's own arc.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Komodo Dragon — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420          # plate disc centre + radius
INK = "#1E1A0E"                    # warm dark ink, never pure black

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

BG_GRAD = lin(0, 0, 0, 1000, (0, "#0C140E"), (1, "#040705"))
PLATE_GRAD = rad((0, "#BEC9A2"), (0.5, "#7A8A5E"), (1, "#3E4A2C"))
FLOOR_GRAD = lin(0, 700, 0, 880, (0, "#6E6038"), (0.6, "#403420"), (1, "#1E160A"))
HIDE_GRAD = lin(420, 460, 560, 620, (0, "#8A7C52"), (0.55, "#655838"), (1, "#3E351E"))
BELLY = "#9A8E62"
TRUNK = "#232E1C"

# --- backdrop + monsoon-forest plate ----------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=64, y=24, width=872, height=872,
        fill="#7A8A5E", opacity=12, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#2C3620", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E4EAD0", strokeWidth=3, opacity=40)

# forest trunks dissolving upward into the canopy gloom
for i, (x, w, o) in enumerate([(196, 26, 55), (300, 16, 42), (742, 30, 58), (824, 18, 45)]):
    d.path(f"M{x},120 C{x-4},300 {x-2},520 {x},700 L{x+w},700 "
           f"C{x+w+2},520 {x+w+4},300 {x+w},120 Z",
           f"Trunk {i+1}", fill=TRUNK, opacity=o, stroke=NONE)
# a liana hanging between trunks
d.path("M300,140 C330,240 326,340 300,420 C292,446 296,470 310,486",
       "Liana", fill=NONE, stroke="#2A3822", strokeWidth=5, opacity=55, cap="round")
# mist bands between the trunks
for i, (x, y, w, o) in enumerate([(150, 330, 320, 16), (430, 380, 340, 14),
                                  (200, 460, 300, 18), (560, 300, 260, 15)]):
    d.path(f"M{x},{y} C{x + w*0.3},{y - 10} {x + w*0.6},{y + 10} {x + w},{y}",
           f"Mist {i+1}", fill=NONE, stroke="#DDE6CC",
           strokeWidth=7, opacity=o, cap="round")

# --- wet leaf-litter floor closing on the disc's own arc ---------------------------
fy = 698
fl, fr = rim_x(fy, side=-1), rim_x(fy, side=1)
d.path(f"M{fl:.1f},{fy} C310,684 420,706 530,700 C640,694 720,694 {fr:.1f},{fy} "
       f"A{R},{R} 0 0 1 {fl:.1f},{fy} Z", "Litter floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{fl+8:.0f},{fy} C310,684 420,706 530,700 C640,694 720,694 {fr-8:.0f},{fy}",
       "Floor crest", fill=NONE, stroke="#A8B080", strokeWidth=5, opacity=40, cap="round")
# wet sheen pools on the litter
for i, (x, y, w) in enumerate([(240, 760, 150), (560, 786, 190), (700, 740, 120)]):
    d.shape("ellipse", f"Sheen {i+1}", x=x - w/2, y=y, width=w, height=14,
            fill="#BEC9A2", opacity=18, stroke=NONE)
# fallen leaves
for i, (x, y, s) in enumerate([(230, 730, 1), (330, 752, -1), (660, 746, 1),
                               (760, 724, -1), (450, 758, 1), (170, 742, -1)]):
    d.path(f"M{x},{y} C{x+8*s},{y-10} {x+18*s},{y-10} {x+24*s},{y} "
           f"C{x+16*s},{y+6} {x+8*s},{y+6} {x},{y} Z",
           f"Leaf {i+1}", fill="#4A3E1E", opacity=55, stroke=NONE)

# the stripped ribcage the tail curls past — carrion-wind made visible
cx0, cy0 = 246, 676
d.path(f"M{cx0-40},{cy0+16} C{cx0-10},{cy0+4} {cx0+30},{cy0+2} {cx0+62},{cy0+10}",
       "Carcass spine", fill=NONE, stroke="#DCD4BC", strokeWidth=5, opacity=65, cap="round")
for k in range(4):
    x = cx0 - 24 + k * 26
    d.path(f"M{x},{cy0+8} C{x-6},{cy0-16} {x-2},{cy0-32} {x+10},{cy0-38}",
           f"Rib {k+1}", fill=NONE, stroke="#DCD4BC", strokeWidth=4.5,
           opacity=60, cap="round")
# a fern frond wilting beside the carcass
for j, sgn in enumerate((-1, 1)):
    for k in range(4):
        x0, y0 = 168 + sgn * k * 14, 706 - k * 4
        d.path(f"M{x0},{y0} Q{x0 + sgn*16},{y0-14} {x0 + sgn*30},{y0-16}",
               f"Fern {j*4+k+1}", fill=NONE, stroke="#5E6E3E",
               strokeWidth=3.5, opacity=60, cap="round")

# contact shadow — long and low under the whole animal
d.shape("ellipse", "Contact shadow", x=330, y=672, width=430, height=20,
        fill="#14180C", opacity=45, stroke=NONE)

# --- the dragon ---------------------------------------------------------------------
# tail: thick at the hip, tapering to a curl along the floor past the bones
d.path("M392,522 C330,548 278,588 248,634 C228,664 210,684 192,690 "
       "C178,694 174,682 186,676 C212,662 238,632 264,596 "
       "C294,556 340,524 388,506 C398,506 400,516 392,522 Z",
       "Tail", fill=lin(392, 506, 192, 690, (0, "#6E613C"), (0.7, "#54482A"), (1, "#3A301A")),
       stroke=INK, strokeWidth=5)
# tail banding — juvenile marks faded to ghosts on the adult
for i, (x, y, w) in enumerate([(286, 600, 26), (320, 570, 30), (252, 634, 20)]):
    d.path(f"M{x},{y} C{x+6},{y+12} {x+8},{y+24} {x+6},{y+34}",
           f"Tail band {i+1}", fill=NONE, stroke="#8A7C52",
           strokeWidth=w/2, opacity=30, cap="round")

# far legs — bowed, darker, a half-pace behind
d.path("M672,540 C694,556 708,584 712,612 C714,634 710,652 700,660 "
       "C692,664 680,662 678,654 C682,632 680,606 672,584 "
       "C666,566 662,550 672,540 Z",
       "Front leg far", fill="#3A3018", stroke=INK, strokeWidth=4)
d.path("M400,548 C382,562 370,588 368,614 C368,636 374,654 384,662 "
       "C394,666 404,662 406,654 C402,632 404,606 412,584 "
       "C418,566 420,552 400,548 Z",
       "Rear leg far", fill="#3A3018", stroke=INK, strokeWidth=4)

# body: the long heavy hull, belly low, neck thick into the rectangular head
d.path("M386,514 C430,486 510,472 576,480 C622,486 652,470 692,482 "
       "C722,490 748,508 762,528 C772,542 768,554 754,558 "
       "C738,562 720,558 706,550 C698,566 684,580 664,588 "
       "C566,616 458,614 402,590 C374,578 360,556 360,536 "
       "C360,526 370,518 386,514 Z",
       "Body", fill=HIDE_GRAD, stroke=INK, strokeWidth=6)
# belly line — lighter fold of skin where the hull meets the ground
d.path("M402,560 C460,588 570,594 660,574 C620,600 500,610 424,592 "
       "C404,586 398,572 402,560 Z", "Belly fold", fill=BELLY,
       opacity=55, stroke=NONE)
# loose neck folds — skin too big for the frame
for i, (x, dy) in enumerate([(640, 0), (656, 8), (622, -6)]):
    d.path(f"M{x},{496 + dy} C{x+8},{536 + dy} {x+2},{564 + dy} {x-10},{588 + dy}",
           f"Neck fold {i+1}", fill=NONE, stroke="#3E351E",
           strokeWidth=5, opacity=55, cap="round")
# pebbly hide — mud-flecks and scale pits over the flank
for i, (x, y, w, o) in enumerate([
        (420, 516, 12, 40), (452, 500, 10, 35), (486, 512, 14, 42), (520, 496, 10, 35),
        (552, 510, 12, 40), (584, 500, 10, 35), (612, 514, 12, 40), (470, 536, 9, 30),
        (510, 540, 11, 32), (550, 534, 9, 30), (590, 542, 11, 32), (436, 548, 8, 28),
        (632, 500, 10, 38), (668, 492, 9, 35), (696, 502, 8, 32)]):
    d.shape("ellipse", f"Hide fleck {i+1}", x=x, y=y, width=w, height=w*0.7,
            fill="#3E351E", opacity=o, stroke=NONE)
# paler scale bosses catching the canopy light along the spine
for i, (x, y) in enumerate([(430, 496), (478, 488), (526, 484), (574, 486), (620, 488)]):
    d.shape("ellipse", f"Back boss {i+1}", x=x, y=y, width=14, height=7,
            fill="#A89E74", opacity=45, stroke=NONE)

# near legs — bowed out, claws raking forward
d.path("M640,548 C668,562 686,590 692,616 C694,640 688,660 676,670 "
       "C666,676 652,672 648,664 C654,644 654,620 646,598 "
       "C640,578 634,560 640,548 Z",
       "Front leg near", fill=HIDE_GRAD, stroke=INK, strokeWidth=5)
d.path("M652,656 C638,662 630,674 638,682 C652,688 674,686 686,676 "
       "C688,668 676,656 664,654 Z", "Front foot", fill="#4A3E20",
       stroke=INK, strokeWidth=4)
for k, (x, dx) in enumerate([(644, -18), (658, -10), (672, -2)]):
    d.path(f"M{x},678 Q{x + dx*0.5},{686 + 0} {x + dx},{688}",
           f"Front claw {k+1}", fill=NONE, stroke="#D8D0B4",
           strokeWidth=4, opacity=85, cap="round")
d.path("M416,556 C392,570 376,598 372,624 C370,646 378,664 392,672 "
       "C402,676 414,672 416,664 C410,642 410,618 418,596 "
       "C424,578 430,564 416,556 Z",
       "Rear leg near", fill=HIDE_GRAD, stroke=INK, strokeWidth=5)
d.path("M384,660 C372,666 366,676 374,682 C386,688 406,686 416,678 "
       "C418,670 408,660 396,658 Z", "Rear foot", fill="#4A3E20",
       stroke=INK, strokeWidth=4)
for k, (x, dx) in enumerate([(378, -14), (392, -8), (404, -2)]):
    d.path(f"M{x},678 Q{x + dx*0.5},{686} {x + dx},{688}",
           f"Rear claw {k+1}", fill=NONE, stroke="#D8D0B4",
           strokeWidth=3.5, opacity=80, cap="round")

# head — rectangular skull, brow ridge over a dark bead eye
d.path("M664,478 C690,470 726,478 748,494 C764,506 774,522 772,536 "
       "C770,548 758,554 744,552 C724,550 704,540 690,528 "
       "C676,516 666,496 664,478 Z",
       "Head", fill=HIDE_GRAD, stroke=INK, strokeWidth=5)
# brow ridge and jowl folds
d.path("M676,486 C696,480 716,482 732,492", "Brow ridge", fill=NONE,
       stroke="#3E351E", strokeWidth=6, opacity=60, cap="round")
d.path("M700,540 C716,548 736,552 752,550", "Jowl", fill=NONE,
       stroke="#3E351E", strokeWidth=4, opacity=55, cap="round")
# eye — dark bead under the ridge
d.shape("ellipse", "Eye", x=700, y=498, width=14, height=12,
        fill="#14100A", stroke=NONE)
d.shape("ellipse", "Eye glint", x=704, y=500, width=3.5, height=3.5,
        fill="#FFF6DC", opacity=80, stroke=NONE)
# nostril at the snout tip
d.shape("ellipse", "Nostril", x=752, y=522, width=9, height=6,
        fill="#14100A", opacity=80, stroke=NONE)
# the long gape line — mouth nearly ear to snout
d.path("M688,522 C712,534 738,542 762,544", "Gape", fill=NONE,
       stroke="#1A1408", strokeWidth=4, opacity=85, cap="round")
# the forked tongue out tasting carrion-wind
d.path("M766,546 C782,552 796,556 808,560", "Tongue", fill=NONE,
       stroke="#D8C44A", strokeWidth=4.5, cap="round")
d.path("M808,560 L820,554 M808,560 L822,564", "Tongue fork", fill=NONE,
       stroke="#D8C44A", strokeWidth=3.5, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#1A2010", strokeWidth=6)

# --- name ---------------------------------------------------------------------------
d.text("KOMODO DRAGON", "Name", x=500, y=962, size=58, font="Virelai Sans",
       color="#DCE4C4", justify="center")

d.finish("komodo-dragon-V1R00")
