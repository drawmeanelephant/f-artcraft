#!/usr/bin/env python3
"""Thylacine — field-guide plate V1R00. The striped wolf that was never a
wolf; last frame 1936: Tasmanian plate, sepia mood. Profile facing right,
head low, stiff tapering tail trailing the topline, dark bars barring the
rump — behind it, two enclosure posts and a sagging wire. Dusty ground
closes on the disc's own arc. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Thylacine — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420          # plate disc centre + radius
INK = "#2E1E12"                    # warm dark ink, never pure black
random.seed(36)                    # 1936, if you like

def lin(x0, y0, x1, y1, *stops):
    ss = []
    for s in stops:
        st = {"offset": s[0], "color": s[1]}
        if len(s) > 2: st["opacity"] = s[2]
        ss.append(st)
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": ss}}

def rad(*stops):
    ss = []
    for s in stops:
        st = {"offset": s[0], "color": s[1]}
        if len(s) > 2: st["opacity"] = s[2]
        ss.append(st)
    return {"gradient": {"kind": "radial", "stops": ss}}

def rim_x(y, r=R, side=-1):
    return CX + side * math.sqrt(r * r - (y - CY) ** 2)

BG_GRAD = lin(0, 0, 0, 1000, (0, "#181008"), (1, "#080502"))
PLATE_GRAD = rad((0, "#E4D6BC"), (0.5, "#B59872"), (1, "#543C24"))
COAT_GRAD = lin(620, 430, 420, 720, (0, "#C8A876"), (0.5, "#A68458"), (1, "#6E4E30"))
GROUND_GRAD = lin(0, 736, 0, 890, (0, "#9A8060"), (0.55, "#6A5034"), (1, "#3A2818"))
STRIPE = "#3A2414"

# --- backdrop + sepia photograph plate ------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=64, y=24, width=872, height=872,
        fill="#B59872", opacity=12, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#3A2814", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F0E4CC", strokeWidth=3, opacity=40)

# aged print: photo vignette corners, grain flecks, two scratches
d.shape("ellipse", "Vignette", x=120, y=80, width=760, height=760,
        fill=rad((0.62, "#2A1808", 0), (0.88, "#2A1808", 22), (1, "#1E1004", 55)),
        stroke=NONE)
for i in range(60):
    x, y = random.uniform(120, 880), random.uniform(90, 840)
    if math.hypot(x - CX, y - CY) < 405:
        w = random.uniform(1.5, 4)
        d.shape("ellipse", f"Grain {i+1}", x=x, y=y, width=w, height=w,
                fill=random.choice(["#F4E8CC", "#3A2814"]),
                opacity=random.choice([12, 18, 25]), stroke=NONE)
d.path("M238,140 C234,340 240,560 236,700", "Scratch 1", fill=NONE,
       stroke="#F4E8CC", strokeWidth=2, opacity=10)
d.path("M762,110 C766,320 758,540 764,690", "Scratch 2", fill=NONE,
       stroke="#F4E8CC", strokeWidth=2, opacity=8)

# the enclosure — two posts and a sagging wire behind the animal
for i, x in enumerate((196, 828)):
    d.path(f"M{x-4},430 L{x+4},430 L{x+5},{606} L{x-5},{606} Z",
           f"Post {i+1}", fill="#2E1E12", opacity=45, stroke=NONE)
d.path("M196,486 C360,516 660,518 828,492", "Wire", fill=NONE,
       stroke="#2E1E12", strokeWidth=3, opacity=35, cap="round")
d.path("M196,520 C360,550 660,552 828,526", "Wire low", fill=NONE,
       stroke="#2E1E12", strokeWidth=2.5, opacity=28, cap="round")

# --- dusty ground closing on the disc's own arc ----------------------------------------
fy = 738
fl, fr = rim_x(fy, side=-1), rim_x(fy, side=1)
d.path(f"M{fl:.1f},{fy} C300,726 420,746 560,740 C680,736 760,732 {fr:.1f},{fy} "
       f"A{R},{R} 0 0 1 {fl:.1f},{fy} Z", "Ground", fill=GROUND_GRAD, stroke=NONE)
d.path(f"M{fl+8:.0f},{fy} C300,726 420,746 560,740 C680,736 760,732 {fr-8:.0f},{fy}",
       "Ground crest", fill=NONE, stroke="#D8C4A0", strokeWidth=4, opacity=30, cap="round")
# worn scuffs and two tussock blades
for i, (x, y, w) in enumerate([(300, 780, 120), (560, 800, 160), (720, 768, 110)]):
    d.shape("ellipse", f"Scuff {i+1}", x=x - w/2, y=y, width=w, height=9,
            fill="#2E1E12", opacity=25, stroke=NONE)
for i, (x0, b) in enumerate([(180, -14), (806, 12), (830, -8)]):
    d.path(f"M{x0},{fy-6} Q{x0+b},{fy-40} {x0+b*1.6},{fy-58}",
           f"Tussock {i+1}", fill=NONE, stroke="#6A5034",
           strokeWidth=4, opacity=55, cap="round")

# contact shadow
d.shape("ellipse", "Shadow", x=330, y=726, width=430, height=20,
        fill="#1E1004", opacity=40, stroke=NONE)

# --- the animal ----------------------------------------------------------------------
def limb(label, pts, widths, fill, **kw):
    n = len(pts)
    L, Rr = [], []
    for i in range(n):
        ax, ay = pts[max(i - 1, 0)]
        bx, by = pts[min(i + 1, n - 1)]
        dx, dy = bx - ax, by - ay
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy / ln, dx / ln
        w = widths[i] / 2
        L.append((pts[i][0] + nx * w, pts[i][1] + ny * w))
        Rr.append((pts[i][0] - nx * w, pts[i][1] - ny * w))
    dd = "M%.1f,%.1f " % L[0]
    for i in range(1, n):
        mx, my = (L[i - 1][0] + L[i][0]) / 2, (L[i - 1][1] + L[i][1]) / 2
        dd += ("Q%.1f,%.1f %.1f,%.1f " % (L[i-1][0], L[i-1][1], mx, my)) if i > 1 else ("L%.1f,%.1f " % (mx, my))
    dd += "L%.1f,%.1f L%.1f,%.1f " % (L[-1] + Rr[-1])
    for i in range(n - 2, -1, -1):
        dd += "L%.1f,%.1f " % Rr[i]
    d.path(dd + "Z", label, fill=fill, **kw)

def paw(label, cx, cy, fill):
    d.path(f"M{cx+22},{cy} C{cx+24},{cy-14} {cx+8},{cy-20} {cx-10},{cy-19} "
           f"C{cx-28},{cy-18} {cx-34},{cy-8} {cx-32},{cy} Z",
           label, fill=fill, stroke=INK, strokeWidth=3)

# the stiff tail first — a straight taper trailing the topline, never wolf-loose
d.path("M392,462 C344,486 296,526 254,570 C244,580 236,590 230,600 "
       "C238,602 248,598 256,590 C300,546 348,508 396,486 Z",
       "Tail", fill=COAT_GRAD, stroke=INK, strokeWidth=4.5)
d.path("M258,566 C290,532 330,502 368,482", "Tail top light", fill=NONE,
       stroke="#E4D6BC", strokeWidth=3, opacity=40, cap="round")

# far legs — slimmer, darker, a half-pace back
limb("Foreleg far", [(636, 560), (640, 620), (646, 686), (648, 730)],
     [46, 38, 30, 26], "#6E4E30", stroke=INK, strokeWidth=3)
paw("Forepaw far", 646, 736, "#54381E")
limb("Hindleg far", [(452, 552), (462, 610), (460, 676), (462, 730)],
     [52, 42, 32, 26], "#6E4E30", stroke=INK, strokeWidth=3)
paw("Hindpaw far", 460, 736, "#54381E")

# torso — deep chest, tucked waist, level back into the tail root
d.path("M688,538 C682,560 676,580 666,594 "                            # chest front
       "C652,610 624,620 590,624 "                                     # brisket
       "C540,630 480,628 438,616 "                                     # tucked waist
       "C408,608 388,590 380,568 "                                     # abdomen up
       "C372,548 370,526 374,506 "                                     # flank front
       "C370,486 378,470 398,462 "                                     # rump top
       "C450,446 540,444 600,448 "                                     # level back
       "C640,450 666,456 682,468 "                                     # withers to neck
       "C692,488 694,512 688,538 Z",
       "Body", fill=COAT_GRAD, stroke=INK, strokeWidth=6)
# shading — chest light, belly shade, hip hollow
d.shape("ellipse", "Chest light", x=590, y=470, width=110, height=100,
        fill="#E4CFA8", opacity=20, stroke=NONE)
d.path("M404,600 C470,616 560,618 640,600 C600,624 490,628 432,612 "
       "C416,608 406,606 404,600 Z", "Belly shade", fill="#54381E",
       opacity=40, stroke=NONE)

# the bars that name it — dark stripes barring the rump, shortest forward
for i in range(13):
    x = 402 + i * 13.5
    top = 452 + (600 - x) * 0.022
    h = max(38, 74 - i * 3)
    lean = -6 + i * 0.4
    d.path(f"M{x:.0f},{top:.0f} L{x+10:.0f},{top+2:.0f} "
           f"L{x+4+lean:.0f},{top+h:.0f} L{x-5+lean:.0f},{top+h-2:.0f} Z",
           f"Stripe {i+1}", fill=STRIPE, opacity=78, stroke=NONE)
# two stragglers onto the tail root
for i, (x, y, h) in enumerate([(378, 468, 44), (392, 462, 48)]):
    d.path(f"M{x},{y} L{x+9},{y+1} L{x+2},{y+h} L{x-6},{y+h-2} Z",
           f"Tail bar {i+1}", fill=STRIPE, opacity=70, stroke=NONE)

# near legs — slim, the hind with a real hock bend
limb("Foreleg near", [(600, 548), (598, 600), (600, 660), (606, 700), (610, 734)],
     [54, 46, 36, 30, 26], COAT_GRAD, stroke=INK, strokeWidth=4)
paw("Forepaw near", 612, 740, "#8A6842")
limb("Hindleg near", [(424, 540), (410, 580), (424, 636), (420, 690), (410, 732)],
     [66, 54, 40, 32, 26], COAT_GRAD, stroke=INK, strokeWidth=4)
paw("Hindpaw near", 406, 738, "#8A6842")
# thigh mass over the hip
d.path("M392,478 C430,462 468,480 474,516 C478,548 464,574 442,586 "
       "C418,566 398,524 392,478 Z", "Thigh", fill=COAT_GRAD, stroke=NONE)
d.path("M442,586 C464,574 478,548 474,516", "Thigh edge", fill=NONE,
       stroke=INK, strokeWidth=4, opacity=45, cap="round")

# head — long narrow wedge, low off the shoulder, big rounded ears
d.path("M806,528 C810,540 806,550 796,556 "                            # nose front
       "C780,566 758,572 736,572 "                                     # chin
       "C714,572 700,566 692,554 "                                     # jaw underside
       "C686,540 688,518 696,502 "                                     # throat rising
       "C704,478 716,462 734,456 "                                     # poll
       "C752,452 772,458 786,472 "                                     # forehead
       "C796,484 804,500 806,512 "                                     # bridge
       "C810,518 810,524 806,528 Z",
       "Head", fill=COAT_GRAD, stroke=INK, strokeWidth=5.5)
# neck mass closing over the head-torso seam
d.path("M662,452 C700,446 720,470 722,506 C724,540 712,568 692,582 "
       "C668,570 656,540 656,504 C656,482 658,464 662,452 Z",
       "Neck mass", fill=COAT_GRAD, stroke=NONE)
# ears — large rounded triangles, the marsupial tell
d.path("M706,452 C700,424 706,398 726,388 C742,390 750,410 748,432 "
       "C744,450 726,458 706,452 Z", "Ear near", fill="#8A6842",
       stroke=INK, strokeWidth=4)
d.path("M714,444 C712,426 716,408 728,400", "Ear inner", fill=NONE,
       stroke="#3A2414", strokeWidth=3.5, opacity=60, cap="round")
d.path("M742,446 C744,424 752,406 766,402 C774,410 776,426 770,442 "
       "C760,450 750,450 742,446 Z", "Ear far", fill="#6E4E30",
       stroke=INK, strokeWidth=3.5)
# face — dark nose, straight mouth, level eye
d.path("M800,518 C808,522 812,530 808,538 C800,544 788,542 784,534 "
       "C782,524 790,516 800,518 Z", "Nose", fill="#1E1004", stroke=NONE)
d.path("M782,548 C762,556 740,558 720,554", "Mouth", fill=NONE,
       stroke="#1E1004", strokeWidth=3.5, opacity=80, cap="round")
d.path("M738,494 C748,488 760,488 768,494 C760,502 748,502 738,494 Z",
       "Eye", fill="#1E1004", stroke=NONE)
d.shape("ellipse", "Eye glint", x=750, y=491, width=4.5, height=4.5,
        fill="#F4E8CC", opacity=85, stroke=NONE)
# the pale brow spot thylacines carry
d.shape("ellipse", "Brow spot", x=742, y=470, width=20, height=9,
        fill="#E4D6BC", opacity=30, stroke=NONE)

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#140C04", strokeWidth=6)

# --- name ---------------------------------------------------------------------------
d.text("THYLACINE", "Name", x=500, y=962, size=58, font="Virelai Sans",
       color="#E4D6BC", justify="center")

d.finish("thylacine-V1R00")
