#!/usr/bin/env python3
"""Pudu — field-guide plate V1R00. Full-body profile facing right, head
carried low to browse: the world's smallest deer, dense and round like a
mossy stone — stubby legs, dark fawn coat, vestigial antler nubs, soft rim
light along the back. Forest-floor greens and deep umber; toadstools and
ferns by the arc-closing ground band. 1000x1000. House style: gradients +
translucent shading, never flat."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Pudu — Field Plate", 1000, 1000)

INK = "#2A2418"
CX, CY, R = 500, 460, 420          # plate disc centre + radius

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

BG_GRAD = lin(0, 0, 0, 1000, (0, "#161C12"), (1, "#070905"))
PLATE_GRAD = rad((0, "#EFE9C9"), (0.62, "#C2BE8E"), (1, "#7B8252"))
COAT_GRAD = rad((0, "#8A5A38"), (0.62, "#6E4526"), (1, "#452A16"))
NECK_GRAD = lin(620, 560, 780, 660, (0, "#7A4E2E"), (1, "#5C3A20"))
FAR_GRAD = lin(0, 690, 0, 800, (0, "#503218"), (1, "#36220F"))
EAR_GRAD = lin(690, 580, 720, 520, (0, "#6E4526"), (1, "#8A5A38"))
EAR_FAR_GRAD = lin(650, 580, 680, 525, (0, "#503218"), (1, "#684226"))
INNER_EAR_GRAD = lin(695, 575, 715, 530, (0, "#B08866"), (1, "#D9BC9C"))
EYE_GRAD = rad((0, "#3A281C"), (1, "#120A05"))
RIM = "#F2E4C4"
MOSS = "#6E7C4A"

# --- backdrop + mossy plate -----------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#4E5A38", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F4F0DA", strokeWidth=3, opacity=50)
d.shape("ellipse", "Patina 1", x=580, y=150, width=230, height=120, fill="#D5D2A8", opacity=22, stroke=NONE)
d.shape("ellipse", "Patina 2", x=180, y=420, width=190, height=110, fill="#D5D2A8", opacity=18, stroke=NONE)
for i, (x, y, w) in enumerate([(770,310,7),(830,470,8),(210,320,6),(160,510,8),(250,720,7),(750,690,8),
                               (855,560,6),(400,108,7),(610,120,6),(330,800,6),(690,240,5),(150,400,6)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#7C7C50", opacity=38, stroke=NONE)

# faint canopy light + soft bokeh, all inside the disc
for i, (x, y, w) in enumerate([(300,220,26),(420,180,18),(620,230,22),(520,150,14),(240,330,16)]):
    d.shape("ellipse", f"Canopy light {i+1}", x=x, y=y, width=w, height=w,
            fill="#F0ECCE", opacity=16, stroke=NONE)
d.shape("ellipse", "Dapple", x=230, y=390, width=150, height=70, fill="#E8E4C2", opacity=14, stroke=NONE)

# --- forest-floor band, closing on the disc's own arc -----------------------------
gy = 792
gdx = math.sqrt(R*R - (gy - CY)**2)
d.path(f"M{CX-gdx:.1f},{gy} C320,780 400,790 500,784 C590,779 680,786 {CX+gdx:.1f},{gy} "
       f"A{R},{R} 0 0 1 {CX-gdx:.1f},{gy} Z",
       "Forest floor", fill=lin(0, 780, 0, 880, (0, "#7A7C4E"), (1, "#49522F")), opacity=85, stroke=NONE)
d.path("M280,802 C380,792 480,798 580,792 C660,788 720,794 740,798", "Floor moss",
       fill=NONE, stroke="#A8AC74", strokeWidth=8, opacity=30, cap="round")

# hoof shadow + ferns + toadstools (all inside the disc)
d.shape("ellipse", "Hoof shadow", x=350, y=794, width=310, height=22,
        fill="#26301A", opacity=35, stroke=NONE)
for j, (x, y, dx) in enumerate([(296,778,-12),(312,782,-4),(286,786,-20)]):
    d.path(f"M{x},{y} Q{x+dx},{y-28} {x+dx*2},{y-40}", f"Fern blade {j+1}",
           fill=NONE, stroke=MOSS, strokeWidth=3, opacity=50, cap="round")
# little toadstools by the browsing nose
for i, (x, y, s) in enumerate([(738,772,1.0),(758,778,0.7)]):
    d.path(f"M{x-3*s:.0f},{y} C{x-4*s:.0f},{y-10*s:.0f} {x-2*s:.0f},{y-14*s:.0f} {x:.0f},{y-14*s:.0f} "
           f"C{x+2*s:.0f},{y-14*s:.0f} {x+4*s:.0f},{y-10*s:.0f} {x+3*s:.0f},{y} Z",
           f"Stem {i+1}", fill="#E4DCC0", stroke=NONE)
    d.path(f"M{x-9*s:.0f},{y-13*s:.0f} C{x-8*s:.0f},{y-24*s:.0f} {x+8*s:.0f},{y-24*s:.0f} {x+9*s:.0f},{y-13*s:.0f} Z",
           f"Cap {i+1}", fill="#A4572E", stroke="#7A3A1E", strokeWidth=2)

# --- far legs (behind the body): stubby little columns ------------------------------
d.path("M598,694 C601,730 600,762 597,792 L587,792 C589,758 587,726 584,696 Z",
       "Front leg far", fill=FAR_GRAD, stroke=NONE)
d.path("M452,700 C466,722 472,750 468,792 L458,792 C460,756 456,728 444,706 Z",
       "Hind leg far", fill=FAR_GRAD, stroke=NONE)
for i, (x0, x1) in enumerate([(586,600),(457,471)]):
    d.path(f"M{x0},790 L{x1},790 C{x1+2},798 {x1-1},802 {x1-5},802 C{x0+2},802 {x0-2},796 {x0},790 Z",
           f"Hoof far {i+1}", fill="#201409", stroke=NONE)

# --- neck: short and thick, sunk deep over the shoulder -------------------------------
d.path("M596,556 C640,552 682,572 714,606 C728,622 734,640 730,656 "
       "C698,662 660,652 632,634 C610,618 598,588 596,556 Z",
       "Neck", fill=NECK_GRAD, stroke=INK, strokeWidth=5)
d.path("M614,566 C650,566 684,586 706,614", "Nape light", fill=NONE,
       stroke=RIM, strokeWidth=6, opacity=30, cap="round")
d.path("M650,632 C676,644 702,650 724,650", "Throat shade", fill=NONE,
       stroke="#36220F", strokeWidth=7, opacity=30, cap="round")

# --- body: a dense mossy stone ---------------------------------------------------------
d.path("M368,606 C384,556 448,530 526,534 C596,538 650,562 662,606 "
       "C672,646 652,678 612,690 C554,706 462,702 412,682 "
       "C378,668 356,636 368,606 Z",
       "Body", fill=COAT_GRAD, stroke=INK, strokeWidth=6)
# the brief's soft rim light along the back
d.path("M382,594 C404,554 462,534 528,538 C586,542 634,564 654,600", "Back rim light",
       fill=NONE, stroke=RIM, strokeWidth=7, opacity=48, cap="round")
d.path("M540,668 C580,676 618,670 644,650", "Flank shade", fill=NONE,
       stroke="#36220F", strokeWidth=16, opacity=24, cap="round")
d.path("M400,650 C440,670 500,678 560,672 C510,690 440,686 406,666 Z",
       "Belly pale", fill="#C9A87C", opacity=40, stroke=NONE)
d.path("M630,570 C648,588 656,612 650,636", "Shoulder shade", fill=NONE,
       stroke="#36220F", strokeWidth=12, opacity=20, cap="round")
# grizzled coat ticks
for j, (x, y, a) in enumerate([(450,560,-18),(500,550,-12),(550,556,-8),(470,610,6),(520,618,10),(430,600,4)]):
    t = math.radians(a)
    d.path(f"M{x},{y} L{x+15*math.cos(t):.0f},{y+15*math.sin(t):.0f}", f"Coat tick {j+1}",
           fill=NONE, stroke="#4A2E18", strokeWidth=3, opacity=40, cap="round")
# tiny tail nub at the rump
d.path("M372,602 C358,606 352,620 358,634 C367,630 372,616 372,602 Z",
       "Tail", fill="#452A16", stroke=INK, strokeWidth=3)

# --- near legs: stubby, tapering only slightly -------------------------------------------
d.path("M588,698 C592,730 591,762 588,794 L576,794 C578,760 577,728 574,700 Z",
       "Front leg near", fill=NECK_GRAD, stroke=NONE)
d.path("M586,708 C588,738 587,766 585,790", "Front leg light", fill=NONE,
       stroke=RIM, strokeWidth=3, opacity=35, cap="round")
d.path("M424,704 C442,722 450,746 446,772 C444,784 441,790 439,797 L428,797 "
       "C430,784 432,770 430,756 C428,734 418,716 406,708 Z",
       "Hind leg near", fill=NECK_GRAD, stroke=NONE)
d.path("M428,716 C440,732 446,750 442,770", "Hock shade", fill=NONE,
       stroke="#36220F", strokeWidth=5, opacity=30, cap="round")
for i, (x0, x1) in enumerate([(575,590),(427,441)]):
    d.path(f"M{x0},792 L{x1},792 C{x1+2},800 {x1-1},804 {x1-5},804 C{x0+2},804 {x0-2},798 {x0},792 Z",
           f"Hoof near {i+1}", fill="#201409", stroke=NONE)

# --- far ear + far antler nub (behind the head) ---------------------------------------------
d.shape("ellipse", "Ear far", x=672, y=542, width=36, height=48, fill=EAR_FAR_GRAD,
        stroke=INK, strokeWidth=4)
d.path("M696,540 L690,520 L704,536 Z", "Antler far", fill="#36220F", stroke=NONE)

# --- head: small, rounded, reaching down to browse -------------------------------------------
HEAD = ("M700,552 C726,552 750,566 764,588 C776,606 786,622 794,636 "
        "C802,648 800,660 790,664 C776,668 758,664 744,654 "
        "C726,642 710,624 702,604 C696,588 694,568 700,552 Z")
d.path(HEAD, "Head", fill=COAT_GRAD, stroke=INK, strokeWidth=6)
d.path("M710,560 C734,560 754,574 766,594", "Forehead light", fill=NONE,
       stroke=RIM, strokeWidth=6, opacity=35, cap="round")
d.path("M736,646 C752,656 770,660 786,658", "Jaw shade", fill=NONE,
       stroke="#36220F", strokeWidth=6, opacity=30, cap="round")
# nose pad + mouth + pale chin
d.path("M788,636 C798,642 802,652 796,660 C788,658 784,648 786,640 Z",
       "Nose pad", fill="#241610", stroke=NONE)
d.shape("ellipse", "Nostril", x=790, y=646, width=6, height=5, fill="#0E0804", stroke=NONE)
d.path("M784,664 C772,668 758,666 748,660", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.path("M760,658 C770,662 780,662 788,658 C782,666 768,666 760,658 Z",
       "Chin pale", fill="#C9A87C", opacity=50, stroke=NONE)
# small dark eye
d.shape("ellipse", "Eye ring", x=726, y=588, width=30, height=28, fill="#A87E52", opacity=70, stroke=NONE)
d.shape("ellipse", "Eye", x=731, y=592, width=20, height=19, fill=EYE_GRAD, stroke=INK, strokeWidth=3)
d.shape("ellipse", "Eye glint", x=736, y=596, width=6, height=6, fill="#FFFFFF", opacity=90, stroke=NONE)
d.path("M726,592 C734,584 746,584 754,590", "Upper lid", fill=NONE,
       stroke=INK, strokeWidth=3, cap="round")

# --- near ear: small rounded oval -----------------------------------------------------------
d.shape("ellipse", "Ear near", x=692, y=524, width=42, height=56, fill=EAR_GRAD,
        stroke=INK, strokeWidth=4)
d.shape("ellipse", "Inner ear", x=700, y=538, width=26, height=36, fill=INNER_EAR_GRAD,
        opacity=85, stroke=NONE)
d.path("M700,536 C706,530 716,528 724,532", "Ear rim light", fill=NONE,
       stroke=RIM, strokeWidth=3, opacity=45, cap="round")
# vestigial antler nub peeking beside the ear
d.path("M694,534 L688,514 L702,530 Z", "Antler near", fill="#452A16",
       stroke=INK, strokeWidth=2)

# --- rim redrawn so the plate edge stays crisp -----------------------------------------------
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#4E5A38", strokeWidth=6)

# --- name ------------------------------------------------------------------------------------
d.text("PUDU", "Name", x=500, y=962, size=60, font="Virelai Sans",
       color="#E8E4C4", justify="center")

d.finish("pudu-V1R00")
