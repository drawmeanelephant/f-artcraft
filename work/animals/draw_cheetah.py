#!/usr/bin/env python3
"""Cheetah — field-guide plate V1R00. Grassland plate, heat-waver mood: the
cat at full rotary-gallop extension, all four feet off the ground, spine
pulled flat, tail streaming for ballast, solid black spots on hot tawny
coat, dust kicking up behind the hind feet and heat shimmer bending the
horizon. Dry grass floor closes on the disc's own arc. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math, re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Cheetah — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420          # plate disc centre + radius
INK = "#241408"                    # warm dark ink, never pure black
SPOT = "#241408"

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

BG_GRAD = lin(0, 0, 0, 1000, (0, "#14100A"), (1, "#070503"))
PLATE_GRAD = rad((0, "#E8CE8E"), (0.5, "#B89454"), (1, "#6E5228"))
COAT_GRAD = lin(400, 380, 560, 560, (0, "#E4AC4E"), (0.55, "#C0802C"), (1, "#7A4C16"))
BELLY_GRAD = lin(0, 480, 0, 620, (0, "#D8A44E"), (1, "#9A6820"))
PALE = "#F0E0BC"
GROUND_GRAD = lin(0, 700, 0, 880, (0, "#A8823E"), (0.6, "#6E5024"), (1, "#38260F"))

# --- backdrop + grassland plate ----------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=64, y=24, width=872, height=872,
        fill="#B89454", opacity=12, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#4A3416", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F4E6BC", strokeWidth=3, opacity=40)

# low hot sun and heat shimmer above the horizon line
d.shape("ellipse", "Sun glow", x=520, y=240, width=320, height=240,
        fill="#F8ECC0", opacity=22, stroke=NONE)
d.shape("ellipse", "Sun", x=610, y=290, width=120, height=120,
        fill=rad((0, "#FCEFBE"), (1, "#E0B868")), opacity=95, stroke=NONE)
for i, (x, y, w, o) in enumerate([(180, 350, 260, 18), (480, 330, 300, 16),
                                (240, 430, 320, 14), (580, 420, 260, 15),
                                (350, 500, 300, 12)]):
    d.path(f"M{x},{y} C{x + w*0.3},{y - 12} {x + w*0.6},{y + 12} {x + w},{y}",
           f"Heat shimmer {i+1}", fill=NONE, stroke="#F8ECC0",
           strokeWidth=4, opacity=o, cap="round")

# far horizon scrub — flat dark tufts
for i, (x, y, w) in enumerate([(200, 560, 60), (320, 575, 80), (640, 565, 70),
                               (760, 575, 55), (460, 580, 90)]):
    d.shape("ellipse", f"Scrub {i+1}", x=x - w/2, y=y - 9, width=w, height=18,
            fill="#5E4820", opacity=50, stroke=NONE)

# --- dry grass floor closing on the disc's own arc -------------------------------------
gy = 726
gl, gr = rim_x(gy, side=-1), rim_x(gy, side=1)
d.path(f"M{gl:.1f},{gy} C300,708 400,734 500,724 C600,714 700,720 {gr:.1f},{gy} "
       f"A{R},{R} 0 0 1 {gl:.1f},{gy} Z", "Grass floor", fill=GROUND_GRAD, stroke=NONE)
d.path(f"M{gl+8:.0f},{gy} C300,708 400,734 500,724 C600,714 700,720 {gr-8:.0f},{gy}",
       "Floor crest", fill=NONE, stroke="#D8BC78", strokeWidth=5, opacity=45, cap="round")
# dry grass blades
for i, (x, y, s) in enumerate([(230, 740, 1), (300, 752, -1), (370, 742, 1),
                               (560, 748, -1), (640, 736, 1), (720, 748, -1),
                               (780, 736, 1), (430, 758, -1), (510, 750, 1)]):
    for j, (dx, dy) in enumerate([(-7, -24), (0, -32), (7, -22)]):
        d.path(f"M{x},{y} Q{x + dx*0.5},{y + dy*0.6} {x + dx + s*j*3},{y + dy}",
               f"Grass {i+1}.{j+1}", fill=NONE, stroke="#C0A058",
               strokeWidth=3.5, opacity=60, cap="round")

# dust kicked up behind the hind feet — the only witness to the hundred
for i, (x, y, w, o) in enumerate([(240, 640, 60, 30), (290, 668, 80, 36),
                                  (200, 680, 46, 26), (340, 690, 66, 30),
                                  (270, 706, 90, 24), (170, 656, 34, 20)]):
    d.shape("ellipse", f"Dust {i+1}", x=x - w/2, y=y - w/4, width=w, height=w/2,
            fill="#D8BC78", opacity=o, stroke=NONE)
# speed streaks behind the body — long low translucent lines
for i, (y, x0, x1, o) in enumerate([(430, 180, 330, 22), (480, 150, 310, 26),
                                    (530, 190, 320, 20), (400, 230, 350, 14)]):
    d.path(f"M{x0},{y} L{x1},{y}", f"Speed line {i+1}", fill=NONE,
           stroke="#F0DCA8", strokeWidth=5, opacity=o, cap="round")

# --- the cat, full extension, facing right ----------------------------------------------
# tail streaming back for ballast — thick base tapering to the dark tip
d.path("M330,470 C280,456 240,452 208,462 C194,468 192,482 204,488 "
       "C236,502 282,506 330,510 C344,506 344,476 330,470 Z",
       "Tail", fill=lin(200, 460, 330, 510, (0, "#5E3A12"), (0.6, "#9A6820"), (1, "#C0802C")),
       stroke=INK, strokeWidth=5)
d.path("M208,462 C194,468 192,482 204,488 C216,494 230,494 238,488 "
       "C234,476 224,466 208,462 Z", "Tail tip", fill="#2E1A0A",
       stroke=INK, strokeWidth=3.5)

# rear leg kicked back — the driving leg at full reach
d.path("M398,512 C360,528 322,554 298,586 C282,608 274,632 280,652 "
       "C288,668 310,668 322,652 C340,630 356,600 376,576 "
       "C392,556 404,534 398,512 Z",
       "Rear leg far", fill="#8A5A1E", stroke=INK, strokeWidth=5)
d.path("M282,642 C268,652 262,670 272,680 C286,688 306,684 314,672 "
       "C316,660 306,648 292,642 Z", "Rear foot far", fill="#6E4414",
       stroke=INK, strokeWidth=4)
# rear leg near — folded deeper under the hip, paw higher
d.path("M430,530 C400,556 376,590 366,622 C360,644 366,660 382,662 "
       "C398,662 408,644 414,622 C422,592 432,560 444,538 "
       "C444,530 436,526 430,530 Z",
       "Rear leg near", fill=BELLY_GRAD, stroke=INK, strokeWidth=5)
d.path("M368,650 C358,662 358,678 370,684 C384,690 400,682 404,668 "
       "C402,656 390,648 378,648 Z", "Rear foot near", fill="#9A6820",
       stroke=INK, strokeWidth=4)

# body: the long flat gallop line, belly tucked high
d.path("M340,466 C380,430 470,410 560,420 C630,428 690,452 716,486 "
       "C730,506 726,528 704,540 C660,562 580,568 500,560 "
       "C430,554 372,534 348,508 C334,494 330,478 340,466 Z",
       "Body", fill=COAT_GRAD, stroke=INK, strokeWidth=7)
# belly tuck + rib shading
d.path("M420,540 C470,556 560,560 630,548 C600,572 520,584 460,570 "
       "C436,564 424,552 420,540 Z", "Belly tuck", fill="#8A5A1E",
       opacity=55, stroke=NONE)
d.shape("ellipse", "Back sheen", x=430, y=418, width=220, height=40,
        fill="#F4CE7C", opacity=30, stroke=NONE)
# the gallop arch — spine crease
d.path("M400,446 C470,428 570,428 650,450", "Spine crease", fill=NONE,
       stroke="#7A4C16", strokeWidth=6, opacity=55, cap="round")

# solid round spots — cheetah, not rosettes
for i, (x, y, rr) in enumerate([
        (400, 452, 7), (440, 442, 6), (480, 436, 7), (520, 434, 6),
        (560, 436, 7), (600, 442, 6), (640, 452, 7), (672, 468, 6),
        (384, 478, 6), (424, 472, 7), (464, 466, 6), (504, 462, 7),
        (544, 462, 6), (584, 466, 7), (624, 474, 6), (660, 490, 6),
        (400, 506, 6), (444, 500, 7), (486, 496, 6), (528, 496, 7),
        (570, 500, 6), (612, 506, 6), (650, 516, 6), (420, 528, 5),
        (470, 524, 6), (520, 526, 5), (578, 528, 6), (350, 486, 5)]):
    d.shape("ellipse", f"Spot {i+1}", x=x - rr, y=y - rr*0.85,
            width=rr*2, height=rr*1.7, fill=SPOT, opacity=88, stroke=NONE)
# spotted legs
for i, (x, y) in enumerate([(312, 590), (330, 612), (352, 576), (392, 570),
                            (408, 596), (672, 560), (690, 586), (706, 550),
                            (718, 584)]):
    d.shape("ellipse", f"Leg spot {i+1}", x=x - 5, y=y - 4,
            width=10, height=8, fill=SPOT, opacity=80, stroke=NONE)

# front legs reaching forward — the catch paws at full stretch
d.path("M640,520 C680,540 716,570 738,600 C752,620 754,642 742,654 "
       "C728,662 710,654 700,636 C684,608 664,578 640,556 "
       "C630,540 630,526 640,520 Z",
       "Front leg near", fill=BELLY_GRAD, stroke=INK, strokeWidth=5)
d.path("M736,640 C752,646 760,662 752,672 C738,678 720,672 714,660 "
       "C714,648 724,640 736,640 Z", "Front paw near", fill="#9A6820",
       stroke=INK, strokeWidth=4)
d.path("M668,512 C700,526 728,550 744,576 C754,594 754,612 744,620 "
       "C730,626 716,616 708,600 C696,576 680,552 662,536 "
       "C654,522 658,512 668,512 Z",
       "Front leg far", fill="#8A5A1E", stroke=INK, strokeWidth=4.5)

# neck and head, low and level — eyes on the line
d.path("M640,430 C668,404 706,390 740,394 C770,398 792,418 800,444 "
       "C806,468 798,492 776,504 C750,518 712,518 686,504 "
       "C660,490 644,462 640,430 Z",
       "Neck+head", fill=COAT_GRAD, stroke=INK, strokeWidth=6)
# small ear folded back flat along the skull — speed posture
d.path("M686,412 C672,398 674,378 690,370 C706,362 728,368 736,384 "
       "C742,398 730,410 714,414 C704,418 692,418 686,412 Z",
       "Ear", fill="#8A5A1E", stroke=INK, strokeWidth=4)
d.path("M694,402 C690,394 694,384 704,382 C714,380 722,386 722,396 "
       "C714,400 704,404 694,402 Z", "Inner ear", fill="#3A2210",
       opacity=80, stroke=NONE)
# face: pale muzzle wedge, dark nose
d.path("M762,446 C786,442 800,456 800,476 C800,494 786,508 766,508 "
       "C748,508 736,496 736,478 C736,462 746,450 762,446 Z",
       "Muzzle", fill=PALE, opacity=92, stroke=NONE)
d.path("M788,462 C798,462 804,470 802,480 C800,490 790,494 782,490 "
       "C774,486 774,474 780,468 C782,464 785,462 788,462 Z",
       "Nose", fill="#3A1E12", stroke=INK, strokeWidth=3)
d.path("M782,494 C772,500 760,500 752,494", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=3.5, cap="round")
# the tear mark — black line from eye corner down past the muzzle
d.path("M742,452 C736,470 734,490 738,510", "Tear mark", fill=NONE,
       stroke=SPOT, strokeWidth=7, cap="round")
# eye — amber, hard ahead
d.path("M726,438 C738,428 756,428 766,438 C762,452 748,458 736,454 "
       "C730,450 726,444 726,438 Z", "Eye",
       fill=rad((0, "#E8C45C"), (0.7, "#B08828"), (1, "#6E5414")),
       stroke=INK, strokeWidth=4)
d.shape("ellipse", "Pupil", x=742, y=435, width=11, height=13,
        fill="#140C06", stroke=NONE)
d.shape("ellipse", "Eye glint", x=745, y=437, width=4, height=4,
        fill="#FFF4D8", opacity=85, stroke=NONE)
# jaw spots + crown flecks
for i, (x, y) in enumerate([(710, 420), (730, 412), (756, 414), (700, 444),
                            (716, 462), (676, 436), (690, 460)]):
    d.shape("ellipse", f"Head spot {i+1}", x=x - 4.5, y=y - 3.5,
            width=9, height=7, fill=SPOT, opacity=80, stroke=NONE)

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#241708", strokeWidth=6)

# --- name ---------------------------------------------------------------------------
d.text("CHEETAH", "Name", x=500, y=962, size=58, font="Virelai Sans",
       color="#F4E6BC", justify="center")

d.finish("cheetah-V1R00")
