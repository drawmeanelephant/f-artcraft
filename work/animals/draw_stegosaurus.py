#!/usr/bin/env python3
"""Stegosaurus — field plate V1R00. Full profile facing left, grazing low:
the arched back carrying two staggered rows of coral kite plates, tail swept
up-right ending in four thagomizer spikes — spikes at the end of the
argument. Fern-meadow floor closing on the disc's own arc, cycad fronds
drooping from above. Jurassic plate, fern-meadow mood. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Stegosaurus — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420
INK = "#1E1408"                    # warm dark ink, never pure black

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

def cubic(p0, p1, p2, p3, t):
    u = 1 - t
    return (u**3*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t**3*p3[0],
            u**3*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t**3*p3[1])

def ribbon(p0, p1, p2, p3, w0, w1, label, n=22, **kw):
    L, Rr = [], []
    for k in range(n + 1):
        t = k / n
        x, y = cubic(p0, p1, p2, p3, t)
        x0, y0 = cubic(p0, p1, p2, p3, max(0, t - 0.01))
        x1, y1 = cubic(p0, p1, p2, p3, min(1, t + 0.01))
        dx, dy = x1 - x0, y1 - y0
        ln = math.hypot(dx, dy) or 1
        w = (w0 + (w1 - w0) * t) / 2
        L.append((x - dy/ln * w, y + dx/ln * w))
        Rr.append((x + dy/ln * w, y - dx/ln * w))
    s = "M%.1f,%.1f " % L[0] + " ".join("L%.1f,%.1f" % p for p in L[1:])
    s += " " + " ".join("L%.1f,%.1f" % p for p in reversed(Rr)) + " Z"
    return d.path(s, label, **kw)

BG_GRAD    = lin(0, 0, 0, 1000, (0, "#141808"), (1, "#060802"))
PLATE_GRAD = rad((0, "#E2DCAC"), (0.55, "#93995E"), (1, "#48532C"))
FLOOR_GRAD = lin(0, 700, 0, 880, (0, "#5C6434"), (0.5, "#3A4220"), (1, "#181C0A"))
HIDE_GRAD  = lin(0, 380, 0, 720, (0, "#9AA06A"), (0.55, "#6E7444"), (1, "#454C26"))
HIDE_DARK  = "#3A401E"
PLT_GRAD   = rad((0, "#E08A5C"), (0.6, "#C05A30"), (1, "#8C3A1A"))
SPIKE_GRAD = lin(0, 300, 0, 460, (0, "#F0E4C0"), (1, "#C4A878"))
FERN       = "#4A6030"
FERN_DK    = "#364A22"

# --- backdrop + fern-meadow plate -----------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#93995E", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#3A4422", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F0ECCC", strokeWidth=3, opacity=45)
# warm Jurassic haze + drifting spores
d.shape("ellipse", "Sun haze", x=540, y=130, width=320, height=170,
        fill="#F4E8B8", opacity=15, stroke=NONE)
for i, (x, y, w) in enumerate([(240,300,5),(770,260,6),(180,470,5),(840,440,5),
                               (420,120,6),(600,105,5),(300,160,4),(720,170,5),
                               (160,600,4),(850,560,4),(500,88,4)]):
    d.shape("ellipse", f"Spore {i+1}", x=x, y=y, width=w, height=w,
            fill="#E4DCAC", opacity=38, stroke=NONE)

# --- cycad fronds drooping from the top -----------------------------------------------
def frond(x, y, tx, ty, label):
    d.path(f"M{x},{y} C{x+(tx-x)*0.3},{y+40} {tx-(tx-x)*0.1},{ty-60} {tx},{ty}",
           label, fill=NONE, stroke=FERN_DK, strokeWidth=5, cap="round")
    # leaflet ticks along the stalk
    n = 7
    for j in range(1, n):
        t = j / n
        px = x + (tx - x) * t
        py = y + (ty - y) * t + math.sin(t * math.pi) * 24
        lx = (tx - x) / n
        d.path(f"M{px:.0f},{py:.0f} l{lx*0.9:.0f},{-14} M{px:.0f},{py:.0f} l{lx*0.9:.0f},{16}",
               f"{label} leaf {j}", fill=NONE, stroke=FERN,
               strokeWidth=3.5, opacity=80, cap="round")

frond(210, 92, 330, 240, "Frond L")
frond(790, 88, 660, 250, "Frond R")

# --- meadow floor, closing on the disc's own arc ---------------------------------------
fy = 716
fl, fr = rim_x(fy, side=-1), rim_x(fy, side=1)
d.path(f"M{fl:.1f},{fy} C300,704 430,720 560,712 C680,704 780,710 {fr:.1f},{fy} "
       f"A{R},{R} 0 0 1 {fl:.1f},{fy} Z", "Meadow floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{fl+8:.0f},{fy-3} C300,701 430,717 560,709 C680,701 780,707 {fr-8:.0f},{fy-3}",
       "Floor light", fill=NONE, stroke="#E4E0B4", strokeWidth=5, opacity=30, cap="round")
# low ridge of far tree line
d.path("M200,690 C330,678 470,684 610,680 C720,676 800,682 830,690",
       "Far ridge", fill=NONE, stroke="#2E3818", strokeWidth=7, opacity=45, cap="round")

# ferns along the floor edges
def ground_fern(x, top, lean, label):
    d.path(f"M{x},{fy-2} C{x+lean},{fy-34} {x+lean},{top+24} {x+lean*2},{top}",
           label, fill=NONE, stroke=FERN_DK, strokeWidth=4.5, cap="round")
    for j in range(3):
        py = fy - 20 - j * 22
        px = x + lean * (1 + j * 0.5)
        d.path(f"M{px:.0f},{py:.0f} l{-14},{-8} M{px:.0f},{py:.0f} l{14},{-8}",
               f"{label} frondlet {j+1}", fill=NONE, stroke=FERN,
               strokeWidth=3, opacity=75, cap="round")

for i, (x, top, lean) in enumerate([(196, 606, -5), (226, 648, 4), (786, 622, 5),
                                    (816, 590, -4), (254, 668, 2)]):
    ground_fern(x, top, lean, f"Fern {i+1}")

# contact shadow under the animal
d.shape("ellipse", "Contact shadow", x=340, y=700, width=430, height=22,
        fill="#14180A", opacity=45, stroke=NONE)

# === the animal =======================================================================
# --- tail swept up-right, then four thagomizer spikes (tips stay inside the rim) --------
ribbon((720, 446), (785, 420), (830, 392), (848, 366), 52, 7,
       "Tail", fill=lin(720, 440, 848, 366, (0, "#6E7444"), (0.7, "#565E30"), (1, "#3E4422")),
       stroke=INK, strokeWidth=5)
# thagomizer: two pairs angled off the tail tip
for i, (bx, by, tx, ty, w) in enumerate([(838,360, 884,300, 9), (848,370, 896,338, 9),
                                        (852,382, 906,382, 8), (844,388, 892,430, 8)]):
    d.path(f"M{bx-w},{by+2} L{tx},{ty} L{bx+w},{by-4} Z",
           f"Thagomizer {i+1}", fill=SPIKE_GRAD, stroke=INK, strokeWidth=4)

# --- far legs: half a pace back, darker -------------------------------------------------
d.path("M500,540 C494,578 492,616 498,650 C502,676 500,694 496,706 "
       "C500,714 514,716 522,710 C526,702 526,692 524,684 "
       "C522,658 524,632 530,606 C536,578 536,556 530,542 "
       "C518,534 508,534 500,540 Z",
       "Front leg far", fill=HIDE_DARK, stroke=INK, strokeWidth=4)
d.path("M676,548 C666,584 664,622 672,656 C676,682 674,700 670,712 "
       "C676,720 694,722 702,714 C706,706 706,696 702,688 "
       "C700,660 702,632 710,606 C718,578 718,556 708,542 "
       "C696,534 684,538 676,548 Z",
       "Rear leg far", fill=HIDE_DARK, stroke=INK, strokeWidth=4)

# --- torso: the great arch, highest over the hips ----------------------------------------
d.path("M330,560 C360,506 420,462 500,442 C560,428 630,424 690,438 "
       "C736,450 762,478 770,512 C776,548 764,580 734,600 "
       "C684,630 560,634 480,618 C420,606 370,586 342,570 "
       "C332,566 328,564 330,560 Z",
       "Torso", fill=HIDE_GRAD, stroke=INK, strokeWidth=6)
# belly light + flank creases + pebble scales
d.path("M420,580 C480,606 620,612 700,592 C650,622 500,628 440,602 "
       "C428,596 420,588 420,580 Z", "Belly light",
       fill="#B8BC84", opacity=38, stroke=NONE)
d.path("M470,470 C458,506 458,548 472,580", "Shoulder crease", fill=NONE,
       stroke="#1E1408", strokeWidth=5, opacity=35, cap="round")
d.path("M690,470 C704,502 706,542 694,572", "Hip crease", fill=NONE,
       stroke="#1E1408", strokeWidth=5, opacity=35, cap="round")
for i, (x, y, w) in enumerate([(500,480,16),(570,468,14),(640,478,15),(450,510,12),
                               (540,520,13),(610,510,12),(680,500,11),(480,552,10),
                               (560,548,12),(640,540,10)]):
    d.shape("ellipse", f"Scale {i+1}", x=x, y=y, width=w, height=w*0.55,
            fill="#3E4422", opacity=30, stroke=NONE)

# --- neck reaching forward-down to the small grazing head ---------------------------------
ribbon((430,530), (382,552), (336,578), (302,608), 58, 30,
       "Neck", fill=HIDE_GRAD, stroke=NONE)
d.path("M300,584 C272,586 250,604 246,628 C242,648 252,664 270,670 "
       "C290,676 314,668 328,650 C340,634 342,612 334,596 "
       "C324,584 312,580 300,584 Z",
       "Head", fill=lin(300, 580, 340, 670, (0, "#8A9058"), (0.6, "#6E7444"), (1, "#4A5028")),
       stroke=INK, strokeWidth=5)
# beak cropping the fern + jaw + nostril + eye
d.path("M252,640 C240,648 234,660 238,670 C243,678 256,680 264,672 "
       "C270,663 270,650 264,642 C260,636 256,636 252,640 Z",
       "Beak", fill="#C8B888", stroke=INK, strokeWidth=4)
d.path("M250,652 C268,664 296,662 316,648", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=3.5, opacity=75, cap="round")
d.shape("ellipse", "Nostril", x=256, y=628, width=10, height=7,
        fill="#1E1408", opacity=75, stroke=NONE)
d.shape("ellipse", "Eye socket", x=296, y=606, width=26, height=20,
        fill="#1E1408", opacity=35, stroke=NONE)
d.shape("ellipse", "Eye", x=302, y=609, width=13, height=12,
        fill="#120C04", stroke=NONE)
d.shape("ellipse", "Eye glint", x=305, y=611, width=4, height=4,
        fill="#F4E8C0", opacity=85, stroke=NONE)

# --- near legs: front short, rear massive -----------------------------------------------
d.path("M428,540 C422,578 420,618 426,652 C430,678 428,696 424,708 "
       "C428,718 444,722 454,714 C458,706 458,696 456,688 "
       "C454,660 456,634 462,608 C468,578 468,556 460,542 "
       "C448,534 436,534 428,540 Z",
       "Front leg near", fill=HIDE_GRAD, stroke=INK, strokeWidth=5)
d.path("M424,698 C422,706 424,716 432,720 L460,720 C466,716 466,706 460,700 "
       "C448,704 434,704 424,698 Z", "Front foot", fill="#4A5028",
       stroke=INK, strokeWidth=4)
for i, xx in enumerate([434, 446, 456]):
    d.path(f"M{xx},702 L{xx-1},718", f"Front toe {i+1}", fill=NONE,
           stroke=INK, strokeWidth=3, opacity=60, cap="round")
d.path("M636,548 C626,586 624,626 632,660 C636,686 634,704 630,716 "
       "C636,724 656,726 664,718 C668,710 668,700 664,692 "
       "C662,662 664,634 672,606 C680,578 680,554 670,540 "
       "C658,532 644,536 636,548 Z",
       "Rear leg near", fill=HIDE_GRAD, stroke=INK, strokeWidth=5)
d.path("M630,702 C628,710 630,720 638,724 L668,724 C674,720 674,710 668,704 "
       "C656,708 640,708 630,702 Z", "Rear foot", fill="#4A5028",
       stroke=INK, strokeWidth=4)
for i, xx in enumerate([640, 652, 662]):
    d.path(f"M{xx},706 L{xx-1},722", f"Rear toe {i+1}", fill=NONE,
           stroke=INK, strokeWidth=3, opacity=60, cap="round")

# --- the plates: two staggered rows of coral kites along the spine ----------------------
def kite(x, y, w, h, lean, label):
    """Rounded kite plate: base sits on the spine at (x,y), tip leans by lean."""
    tx, ty = x + lean, y - h
    d.path(f"M{x-w/2},{y} C{x-w/2},{y-h*0.45} {x-w*0.28+lean*0.6},{ty+h*0.28} {tx},{ty} "
           f"C{x+w*0.28+lean*0.6},{ty+h*0.28} {x+w/2},{y-h*0.45} {x+w/2},{y} Z",
           label, fill=PLT_GRAD, stroke=INK, strokeWidth=4.5)
    d.path(f"M{x},{y-6} C{x+lean*0.4},{y-h*0.45} {tx},{ty+10} {tx},{ty+10}",
           f"{label} ridge", fill=NONE, stroke="#8C3A1A",
           strokeWidth=3, opacity=50, cap="round")

# alternating heights — tallest pair over the hips
for i, (x, y, w, h, lean) in enumerate([
        (368,494, 40, 56, -6), (424,462, 52, 78, -8), (486,444, 56, 96, -6),
        (552,434, 58, 104, -2), (620,432, 58, 108, 4), (686,438, 56, 98, 10),
        (744,452, 50, 82, 14), (788,444, 42, 62, 18)]):
    kite(x, y, w, h, lean, f"Plate {i+1}")
# plate-top glints — sun off the keratin
for i, (x, y) in enumerate([(418,398),(480,362),(548,344),(618,338),(684,354),(742,384)]):
    d.shape("ellipse", f"Plate glint {i+1}", x=x, y=y, width=14, height=8,
            fill="#F4C494", opacity=40, stroke=NONE)

# a spore or two settled on the plates
for i, (x, y, w) in enumerate([(560,420,5),(650,430,4)]):
    d.shape("ellipse", f"Settled spore {i+1}", x=x, y=y, width=w, height=w,
            fill="#E4DCAC", opacity=45, stroke=NONE)

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#2C3418", strokeWidth=6)

# --- name ------------------------------------------------------------------------------
d.text("STEGOSAURUS", "Name", x=500, y=962, size=56, font="Virelai Sans",
       color="#ECE4B8", justify="center")

d.finish("stegosaurus-V1R00")
