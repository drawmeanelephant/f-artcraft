#!/usr/bin/env python3
"""Numbat — field-guide plate V1R00. Full-body profile facing left: russet
forequarters darkening to a grey-brown rump crossed by white bands (the
signature), black eye stripe with its pale underline, small round ears, and a
bottle-brush tail raised behind. Pale wandoo-woodland desert palette with a
hollow log; the ground band closes on the disc's own arc.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Numbat — Field Plate", 1000, 1000)
rng = random.Random(22)   # fixed seed: tail hairs and litter are the same every run

INK = "#3A2418"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#33292A"}, {"offset": 1, "color": "#120E0E"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#FDF7EA"}, {"offset": 0.6, "color": "#EEDDBE"},
    {"offset": 1, "color": "#BC9E78"}]}}
GROUND_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E2C69C"}, {"offset": 1, "color": "#B08A62"}]}}
LOG_GRAD = {"gradient": {"kind": "linear", "start": [0, 640], "end": [0, 716], "stops": [
    {"offset": 0, "color": "#D8CCBA"}, {"offset": 0.5, "color": "#B4A48E"},
    {"offset": 1, "color": "#7E6E5C"}]}}
COAT_GRAD = {"gradient": {"kind": "linear", "start": [260, 0], "end": [700, 0], "stops": [
    {"offset": 0, "color": "#D27A48"}, {"offset": 0.45, "color": "#BC6236"},
    {"offset": 0.75, "color": "#7A4C3A"}, {"offset": 1, "color": "#4E3830"}]}}
BELLY_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F4E2C8"}, {"offset": 1, "color": "#D8BC98"}]}}
LEG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#B05A34"}, {"offset": 1, "color": "#6E3A22"}]}}
HIND_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6A4434"}, {"offset": 1, "color": "#3E2A22"}]}}
LEG_FAR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6E3A22"}, {"offset": 1, "color": "#3A2014"}]}}
TAIL_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#8A6250"}, {"offset": 0.7, "color": "#6A4A3E"},
    {"offset": 1, "color": "#4A3630"}]}}
EAR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#C8703E"}, {"offset": 1, "color": "#8A4626"}]}}

GROUND_Y = 720
CX, CY, R = 500, 460, 420
def disc_x(y):
    return math.sqrt(R*R - (y - CY)**2)

def cubic(p0, p1, p2, p3, t):
    u = 1 - t
    return (u**3*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t**3*p3[0],
            u**3*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t**3*p3[1])

# --- backdrop + plate ---------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#8A7052", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#FFFBF2", strokeWidth=3, opacity=60)
d.shape("ellipse", "Warm haze", x=180, y=160, width=300, height=130, fill="#FFF0D8", opacity=30, stroke=NONE)
d.shape("ellipse", "Patina", x=560, y=190, width=240, height=120, fill="#D8C2A0", opacity=24, stroke=NONE)
for i, (x, y, w) in enumerate([(200,300,7),(780,250,6),(170,440,8),(400,120,6),(620,110,7),
                               (300,170,5),(700,180,6),(860,400,5),(140,520,5),(520,96,5)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w, fill="#A88A66", opacity=35, stroke=NONE)

# faint wandoo trunks (pale-barked eucalypts) standing on the ground line, inside the disc
for i, (x, lean, top, w) in enumerate([(232, -14, 310, 22), (760, 18, 300, 20)]):
    d.path(f"M{x},{GROUND_Y} C{x + lean*0.2},{(GROUND_Y + top)/2 + 40} {x + lean*0.8},{(GROUND_Y + top)/2 - 40} {x + lean},{top}",
           f"Wandoo trunk {i+1}", fill=NONE, stroke="#C8B498", strokeWidth=w, opacity=40, cap="round")
for i, (x, y, w, h) in enumerate([(160, 270, 140, 80), (240, 300, 120, 60), (700, 240, 150, 80), (770, 290, 100, 56)]):
    d.shape("ellipse", f"Wandoo crown {i+1}", x=x, y=y, width=w, height=h, fill="#A8AE8A", opacity=24, stroke=NONE)

# ground band: top edge across, bottom closes on the disc arc
xl, xr = CX - disc_x(GROUND_Y), CX + disc_x(GROUND_Y)
d.path(f"M{xl:.1f},{GROUND_Y} C{xl + 160:.1f},{GROUND_Y - 8} {xr - 160:.1f},{GROUND_Y - 8} {xr:.1f},{GROUND_Y} "
       f"A{R},{R} 0 0 1 {xl:.1f},{GROUND_Y} Z", "Ground", fill=GROUND_GRAD, opacity=92, stroke=NONE)
d.path(f"M{xl + 20:.1f},{GROUND_Y + 2} C{xl + 180:.1f},{GROUND_Y - 5} {xr - 180:.1f},{GROUND_Y - 5} {xr - 20:.1f},{GROUND_Y + 2}",
       "Ground rim light", fill=NONE, stroke="#FFF4E0", strokeWidth=3, opacity=50, cap="round")
# leaf litter + pebbles, all well inside the ground band
for i in range(14):
    x = rng.uniform(250, 750)
    y = rng.uniform(740, 820)
    if math.hypot(x - CX, y - CY) > R - 40:
        continue
    a = math.radians(rng.uniform(-40, 40))
    L = rng.uniform(16, 26)
    dx, dy = math.cos(a)*L, math.sin(a)*L
    d.path(f"M{x:.1f},{y:.1f} Q{x + dx/2 - dy*0.3:.1f},{y + dy/2 + dx*0.3:.1f} {x + dx:.1f},{y + dy:.1f} "
           f"Q{x + dx/2 + dy*0.3:.1f},{y + dy/2 - dx*0.3:.1f} {x:.1f},{y:.1f} Z",
           f"Leaf {i+1}", fill="#9A8A5A" if i % 2 else "#B07A4A", opacity=55, stroke=NONE)
for i, (x, y, w, h) in enumerate([(300,770,14,7),(560,800,12,6),(640,760,16,8),(420,830,10,5),(700,800,12,6)]):
    d.shape("ellipse", f"Pebble {i+1}", x=x, y=y, width=w, height=h, fill="#8E7050", opacity=40, stroke=NONE)
# termites trickling out from under the log
for i, (x, y) in enumerate([(612, 738), (596, 746), (578, 742), (560, 752), (544, 748)]):
    d.shape("ellipse", f"Termite {i+1}", x=x, y=y, width=8, height=4, fill="#F4E6CC", opacity=80, stroke="#7A5A3A", strokeWidth=1)

# --- hollow log behind the tail -------------------------------------------------------
d.path("M600,648 L790,640 C808,640 818,660 818,680 C818,700 808,716 790,716 L600,718 "
       "C584,718 576,700 576,684 C576,664 584,648 600,648 Z",
       "Log", fill=LOG_GRAD, stroke="#5E4E3E", strokeWidth=4)
d.shape("ellipse", "Log end", x=766, y=640, width=52, height=76, fill="#B4A48E", stroke="#5E4E3E", strokeWidth=4)
d.shape("ellipse", "Log hollow", x=776, y=652, width=34, height=54, fill="#2E241C", opacity=85, stroke=NONE)
for i, dd in enumerate(["M610,664 C660,660 710,658 760,656", "M606,694 C660,692 720,690 770,690"]):
    d.path(dd, f"Log grain {i+1}", fill=NONE, stroke="#7E6E5C", strokeWidth=3, opacity=50, cap="round")
d.path("M604,656 C660,652 720,650 774,648", "Log light", fill=NONE, stroke="#F4EEE2", strokeWidth=4, opacity=50, cap="round")
d.shape("ellipse", "Numbat shadow", x=250, y=710, width=470, height=24, fill="#5A4030", opacity=30, stroke=NONE)

# --- bottle-brush tail, raised behind the rump -------------------------------------------
T0, T1, T2, T3 = (676, 590), (740, 560), (770, 470), (742, 368)
spine = [cubic(T0, T1, T2, T3, k/24) for k in range(25)]
lt, rt = [], []
for k, (x, y) in enumerate(spine):
    ax, ay = spine[max(k - 1, 0)]; bx, by = spine[min(k + 1, 24)]
    tx, ty = bx - ax, by - ay
    ln = math.hypot(tx, ty) or 1
    nx, ny = -ty/ln, tx/ln
    w = 30 + 26*math.sin(math.pi*min(1, k/24*1.15))
    lt.append((x + nx*w, y + ny*w)); rt.append((x - nx*w, y - ny*w))
dd = "M%.1f,%.1f " % lt[0] + " ".join("L%.1f,%.1f" % p for p in lt[1:])
dd += " " + " ".join("L%.1f,%.1f" % p for p in reversed(rt)) + " Z"
d.path(dd, "Tail mass", fill=TAIL_GRAD, opacity=92, stroke=NONE)
# fluffed hairs fanning out from the spine toward the tip
HAIR_COLS = ["#5A4038", "#8A6454", "#C8A890", "#B06A44", "#F2E6D4"]
for k in range(2, 25):
    x, y = spine[k]
    ax, ay = spine[k - 1]
    tx, ty = x - ax, y - ay
    ln = math.hypot(tx, ty) or 1
    tx, ty = tx/ln, ty/ln
    nx, ny = -ty, tx
    w = 30 + 26*math.sin(math.pi*min(1, k/24*1.15))
    for side in (1, -1):
        for j in range(3):
            L = w * rng.uniform(0.9, 1.35)
            fwd = rng.uniform(0.25, 0.7)
            ex = x + (nx*side + tx*fwd) * L
            ey = y + (ny*side + ty*fwd) * L
            mx, my = x + nx*side*L*0.5, y + ny*side*L*0.5
            col = HAIR_COLS[(k + j + (side > 0)) % len(HAIR_COLS)]
            d.path(f"M{x:.1f},{y:.1f} Q{mx:.1f},{my:.1f} {ex:.1f},{ey:.1f}", f"Tail hair {k}.{side}.{j}",
                   fill=NONE, stroke=col, strokeWidth=rng.choice([3, 4, 5]), opacity=70, cap="round")
d.path("M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (T0 + T1 + T2 + T3), "Tail core shade",
       fill=NONE, stroke="#3E2A22", strokeWidth=10, opacity=30, cap="round")

# --- far legs, behind the body -----------------------------------------------------------
d.path("M392,650 C386,676 384,700 382,716 L408,718 C410,700 414,676 420,654 Z",
       "Leg far front", fill=LEG_FAR_GRAD, stroke=INK, strokeWidth=3)
d.path("M600,640 C612,670 618,696 616,716 L642,716 C644,694 638,668 628,640 Z",
       "Leg far hind", fill=LEG_FAR_GRAD, stroke=INK, strokeWidth=3)

# --- body: one silhouette, snout to rump --------------------------------------------------
BODY = [((214, 606), (236, 590), (268, 572), (300, 560)),
        ((300, 560), (322, 532), (356, 514), (392, 520)),
        ((392, 520), (430, 512), (470, 508), (520, 510)),
        ((520, 510), (600, 508), (660, 520), (690, 548)),
        ((690, 548), (716, 574), (716, 632), (690, 662)),
        ((690, 662), (650, 692), (560, 694), (480, 690)),
        ((480, 690), (420, 688), (380, 678), (350, 662)),
        ((350, 662), (322, 650), (300, 640), (276, 632)),
        ((276, 632), (250, 624), (226, 620), (214, 606))]
body_d = "M214,606 " + " ".join("C%d,%d %d,%d %d,%d" % (s[1] + s[2] + s[3]) for s in BODY) + " Z"
d.path(body_d, "Body", fill=COAT_GRAD, stroke=NONE)
pts = [cubic(*s, k/40) for s in BODY for k in range(41)]
def top_y(x):
    return min(p[1] for p in pts if abs(p[0] - x) < 4 and p[1] < 620)
def bot_y(x):
    return max(p[1] for p in pts if abs(p[0] - x) < 4 and p[1] > 600)

# pale belly + throat
d.path("M300,640 C340,660 400,682 480,686 C540,690 600,688 650,676 "
       "C600,672 520,668 460,664 C400,658 350,650 300,640 Z",
       "Belly pale", fill=BELLY_GRAD, opacity=70, stroke=NONE)
d.path("M232,618 C254,626 278,632 300,640 C276,630 254,624 232,618 Z",
       "Throat pale", fill="#F4E2C8", opacity=60, stroke=NONE)
# the signature: white bands across the rump, slanted, tapering toward the belly
for i, x in enumerate([514, 548, 582, 614, 644, 672]):
    t0 = top_y(x) + 2
    b = bot_y(x)
    depth = 0.62 - 0.04*i
    yb = t0 + (b - t0)*depth
    w = 15 - i*0.8
    sl = 10
    d.path(f"M{x - w/2:.1f},{t0:.1f} L{x + w/2:.1f},{t0:.1f} "
           f"Q{x + w/2 + sl*0.4:.1f},{(t0 + yb)/2:.1f} {x + sl:.1f},{yb:.1f} "
           f"Q{x - w/2 + sl*0.4:.1f},{(t0 + yb)/2:.1f} {x - w/2:.1f},{t0:.1f} Z",
           f"Rump band {i+1}", fill="#FBF4E8", opacity=88, stroke=NONE)
# back light, haunch + shoulder modelling
d.path("M400,528 C460,516 540,512 620,520", "Back light", fill=NONE,
       stroke="#FFE2C4", strokeWidth=10, opacity=28, cap="round")
d.shape("ellipse", "Haunch shade", x=600, y=574, width=100, height=96, fill="#2E201A", opacity=18, stroke=NONE)
d.shape("ellipse", "Shoulder light", x=360, y=560, width=90, height=70, fill="#FFD2A8", opacity=20, stroke=NONE)
for i, (x, y) in enumerate([(430,560),(460,590),(410,610),(480,624),(500,560)]):
    d.path(f"M{x},{y} Q{x + 10},{y + 4} {x + 18},{y + 12}", f"Coat fur {i+1}", fill=NONE,
           stroke="#8A3E1C", strokeWidth=4, opacity=30, cap="round")
# outline on top hides any band edges at the rim
d.path(body_d, "Body outline", fill=NONE, stroke=INK, strokeWidth=6)

# --- near legs ----------------------------------------------------------------------------
d.path("M336,616 C374,606 398,636 392,666 C388,688 384,704 380,716 "
       "C388,720 392,726 386,730 L346,730 C348,708 348,690 344,672 "
       "C328,658 322,630 336,616 Z", "Leg near front", fill=LEG_GRAD, stroke=INK, strokeWidth=4)
d.path("M590,600 C640,600 670,632 664,670 C660,690 660,706 668,716 "
       "C676,718 682,724 676,728 L634,728 C632,706 626,686 612,668 Z",
       "Leg near hind", fill=HIND_GRAD, stroke=INK, strokeWidth=4)
for i, (x, y) in enumerate([(348,728),(356,729),(364,730),(636,727),(644,729),(652,729)]):
    d.path(f"M{x},{y} L{x - 7},{y + 3}", f"Claw {i+1}", fill=NONE, stroke="#2A1A12", strokeWidth=3, cap="round")
d.path("M614,612 C640,616 656,636 656,660", "Haunch light", fill=NONE,
       stroke="#C8A890", strokeWidth=5, opacity=35, cap="round")
d.path("M370,640 C376,664 372,692 366,712", "Front leg light", fill=NONE,
       stroke="#F2B080", strokeWidth=4, opacity=35, cap="round")

# --- head details: ear, eye stripe, eye, nose ---------------------------------------------
d.path("M362,526 C356,498 372,480 394,486 C406,504 402,522 390,532 Z",
       "Ear", fill=EAR_GRAD, stroke=INK, strokeWidth=4)
d.path("M370,522 C368,504 378,494 390,498 C396,510 394,520 386,526 Z",
       "Inner ear", fill="#E8B898", opacity=70, stroke=NONE)
d.path("M234,600 C262,588 292,576 318,566 C340,558 358,548 372,534", "Eye stripe pale",
       fill=NONE, stroke="#FBF4E8", strokeWidth=22, opacity=70, cap="round")
d.path("M232,594 C262,582 292,570 318,560 C340,552 356,542 370,528", "Eye stripe",
       fill=NONE, stroke="#1E1410", strokeWidth=13, opacity=88, cap="round")
d.shape("ellipse", "Eye", x=308, y=550, width=18, height=15, fill="#0E0806", stroke="#F6E8D4", strokeWidth=2)
d.shape("ellipse", "Eye glint", x=312, y=553, width=5, height=5, fill="#FFFFFF", opacity=90, stroke=NONE)
d.path("M210,600 C206,606 210,614 220,614 C224,608 222,602 210,600 Z", "Nose", fill="#1A100C", stroke=NONE)
d.path("M222,616 C234,622 248,624 262,624", "Mouth", fill=NONE, stroke=INK, strokeWidth=3, opacity=70, cap="round")
for i, (x, y, l) in enumerate([(236, 608, 30), (240, 612, 26)]):
    d.path(f"M{x},{y} Q{x - l*0.5},{y + 2} {x - l},{y + 8}", f"Whisker {i+1}", fill=NONE,
           stroke="#3A2418", strokeWidth=2, opacity=55, cap="round")

# --- name -------------------------------------------------------------------------------------
d.text("NUMBAT", "Name", x=500, y=962, size=60, font="Virelai Sans",
       color="#F2E4CC", justify="center")

d.finish("numbat-V1R00")
