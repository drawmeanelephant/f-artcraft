#!/usr/bin/env python3
"""Potoo — field-guide plate V1R00. Head/bust on a broken branch: giant yellow
eyes, a frog-mouth gape running cheek to cheek, mottled grey-bark plumage.
Deadpan, played completely straight. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Potoo — Field Plate", 1000, 1000)
rng = random.Random(15)   # fixed seed: the mottling is the same every run

INK = "#2B2620"   # warm bark-brown, not black
BG_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#1E241B"}, {"offset": 1, "color": "#090C08"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E6E8DA"}, {"offset": 0.7, "color": "#BCC2AB"},
    {"offset": 1, "color": "#878F76"}]}}
PLUME_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#ABA393"}, {"offset": 0.65, "color": "#837A6B"},
    {"offset": 1, "color": "#5A5246"}]}}
WING_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6E6557"}, {"offset": 1, "color": "#4A4238"}]}}
WING_GRAD_R = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4A4238"}, {"offset": 1, "color": "#6E6557"}]}}
LID_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#8C8373"}, {"offset": 1, "color": "#6A6153"}]}}
IRIS_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#FFF09A"}, {"offset": 0.55, "color": "#F7C523"},
    {"offset": 1, "color": "#B9800B"}]}}
BEAK_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#4E463C"}, {"offset": 1, "color": "#1E1A15"}]}}
BARK_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#7A6B58"}, {"offset": 1, "color": "#3E3428"}]}}
TAIL_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#6A6153"}, {"offset": 1, "color": "#423B32"}]}}

# --- backdrop + fireflies + plate ------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
for i, (x, y, w, o) in enumerate([(60,120,8,45),(140,60,5,35),(48,420,6,40),(70,760,7,40),
                                  (930,90,7,45),(880,170,5,35),(950,470,6,40),(925,780,7,40)]):
    d.shape("ellipse", f"Firefly halo {i+1}", x=x-w, y=y-w, width=w*3, height=w*3,
            fill="#F7D24A", opacity=10, stroke=NONE)
    d.shape("ellipse", f"Firefly {i+1}", x=x, y=y, width=w, height=w,
            fill="#F7D24A", opacity=o, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#5E6650", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F0F2E6", strokeWidth=3, opacity=55)
d.shape("ellipse", "Lichen blot 1", x=170, y=170, width=220, height=130, fill="#9AA388", opacity=24, stroke=NONE)
d.shape("ellipse", "Lichen blot 2", x=640, y=190, width=190, height=110, fill="#9AA388", opacity=20, stroke=NONE)
d.shape("ellipse", "Lichen blot 3", x=150, y=520, width=150, height=100, fill="#9AA388", opacity=18, stroke=NONE)
d.shape("ellipse", "Lichen blot 4", x=700, y=520, width=150, height=100, fill="#9AA388", opacity=18, stroke=NONE)
for i, (x, y, w) in enumerate([(250,320,8),(760,260,7),(180,450,7),(820,430,8),(400,120,7),
                               (600,115,8),(220,640,6),(780,640,6),(320,200,5),(690,330,5)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w, fill="#6E765E", opacity=40, stroke=NONE)

# --- tail hanging below the branch: closes on the disc's own arc ---------------------
d.path("M546,780 C556,820 566,850 571,874 A420,420 0 0 1 429,874 "
       "C434,850 444,820 454,780 Z", "Tail", fill=TAIL_GRAD, stroke=INK, strokeWidth=5)
for i, dd in enumerate(["M480,792 L474,866", "M500,792 L500,872", "M520,792 L526,866"]):
    d.path(dd, f"Tail bar {i+1}", fill=NONE, stroke="#2E2820", strokeWidth=3, opacity=40, cap="round")
for i, y in enumerate([812, 838, 860]):
    d.path(f"M{446 - i*4},{y} C480,{y+6} 520,{y+6} {554 + i*4},{y}", f"Tail band {i+1}",
           fill=NONE, stroke="#B1A897", strokeWidth=4, opacity=35, cap="round")

# --- body + head: one upright stump-shaped silhouette ---------------------------------
d.path("M500,336 C590,336 694,318 714,404 C728,462 708,520 676,566 "
       "C694,626 702,694 680,756 L320,756 C298,694 306,626 324,566 "
       "C292,520 272,462 286,404 C306,318 410,336 500,336 Z",
       "Body", fill=PLUME_GRAD, stroke=INK, strokeWidth=7)
# long bark-streaks down the breast: stump camouflage, not an owl's pale belly
for i, x in enumerate([420, 452, 486, 516, 548, 580]):
    d.path(f"M{x},582 C{x-4},630 {x+4},680 {x-2},736", f"Bark streak {i+1}",
           fill=NONE, stroke="#C9C1B0", strokeWidth=5, opacity=28, cap="round")
# crown rim light
d.path("M470,340 C500,338 520,338 540,338", "Crown rim", fill=NONE,
       stroke="#E2DACA", strokeWidth=6, opacity=30, cap="round")

# folded wings along the flanks
d.path("M334,560 C312,620 302,690 322,756 C356,740 380,676 388,600 C376,580 356,566 334,560 Z",
       "Wing L", fill=WING_GRAD, stroke=INK, strokeWidth=5)
d.path("M666,560 C688,620 698,690 678,756 C644,740 620,676 612,600 C624,580 644,566 666,560 Z",
       "Wing R", fill=WING_GRAD_R, stroke=INK, strokeWidth=5)
for i, (x0, sgn) in enumerate([(342, 1), (658, -1)]):
    for j in range(4):
        y = 600 + j * 36
        d.path(f"M{x0 + sgn*(4 + j*3)},{y} C{x0 + sgn*18},{y+10} {x0 + sgn*30},{y+14} {x0 + sgn*40},{y+12}",
               f"Wing bar {i*4 + j + 1}", fill=NONE, stroke="#BDB3A0", strokeWidth=3, opacity=40, cap="round")

# bark mottling: seeded blotches and streaks, translucent so the gradient reads through
def inside_body(x, y):
    if y < 350 or y > 740:
        return False
    half = 190 if y < 560 else 160
    return abs(x - 500) < half
n = 0
while n < 70:
    x, y = rng.uniform(310, 690), rng.uniform(340, 740)
    if not inside_body(x, y) or (y < 470 and abs(abs(x - 500) - 88) < 90) or (460 < y < 520):
        continue
    w = rng.uniform(5, 16); h = w * rng.uniform(0.5, 1.0)
    col = rng.choice(["#3E362D", "#3E362D", "#CFC6B4", "#5A5044"])
    d.shape("ellipse", f"Mottle {n+1}", x=round(x, 1), y=round(y, 1), width=round(w, 1), height=round(h, 1),
            fill=col, opacity=rng.randint(28, 50), stroke=NONE)
    n += 1
for i in range(14):
    x = 410 + i * 14 + rng.uniform(-4, 4); y = rng.uniform(590, 680)
    d.path(f"M{x:.0f},{y:.0f} l{rng.uniform(-3,3):.0f},{rng.uniform(22,40):.0f}", f"Breast streak {i+1}",
           fill=NONE, stroke="#3E362D", strokeWidth=3, opacity=40, cap="round")

# --- eyes: enormous, yellow, flat-lidded stare ------------------------------------------
for side, cx in (("L", 412), ("R", 588)):
    cy, r = 384, 70
    # feathered socket bulges above the flat crown, frog-style
    d.shape("ellipse", f"Socket {side}", x=cx-r-14, y=cy-r-14, width=2*r+28, height=2*r+28,
            fill=PLUME_GRAD, stroke=INK, strokeWidth=6)
    d.shape("ellipse", f"Socket shade {side}", x=cx-r-6, y=cy-r-4, width=2*r+12, height=2*r+12,
            fill="#3E362D", opacity=35, stroke=NONE)
    d.shape("ellipse", f"Iris {side}", x=cx-r, y=cy-r, width=2*r, height=2*r,
            fill=IRIS_GRAD, stroke=INK, strokeWidth=6)
    d.shape("ellipse", f"Pupil {side}", x=cx-15, y=cy-10, width=30, height=30, fill="#120F0B", stroke=NONE)
    d.shape("ellipse", f"Glint {side}", x=cx-30, y=cy-26, width=16, height=14, fill="#FFFFFF", opacity=85, stroke=NONE)
    d.shape("ellipse", f"Glint2 {side}", x=cx+14, y=cy+22, width=7, height=6, fill="#FFFBE0", opacity=55, stroke=NONE)
    # the lid: a flat chord across the top of the eye, which carries the deadpan
    k = (r*r - 30*30) ** 0.5
    d.path(f"M{cx-k:.1f},{cy-30} A{r},{r} 0 0 1 {cx+k:.1f},{cy-30} Z", f"Lid {side}",
           fill=LID_GRAD, stroke=INK, strokeWidth=5)
    d.path(f"M{cx-k+4:.1f},{cy-30} L{cx+k-4:.1f},{cy-30}", f"Lid edge {side}",
           fill=NONE, stroke=INK, strokeWidth=6, cap="round")
    d.path(f"M{cx-k+10:.1f},{cy-23} L{cx+k-10:.1f},{cy-23}", f"Lid shadow {side}",
           fill=NONE, stroke="#7A520A", strokeWidth=5, opacity=35, cap="round")
# brow bristles over each lid
for i, (x, y, dx) in enumerate([(372,312,-6),(394,304,-3),(416,301,0),(438,304,3),
                                (562,304,-3),(584,301,0),(606,304,3),(628,312,6)]):
    d.path(f"M{x},{y} l{dx},-14", f"Brow bristle {i+1}", fill=NONE, stroke="#4A4238", strokeWidth=3, opacity=60, cap="round")

# --- the frog-mouth: a gape from cheek to cheek, and a tiny hooked beak -------------------
# the broad lower mandible: a faint jaw outline makes the mouth read as enormous
d.path("M302,494 C336,584 664,584 698,494 C640,516 360,516 302,494 Z", "Jaw",
       fill="#CFC6B4", opacity=24, stroke=NONE)
d.path("M312,506 C352,578 648,578 688,506", "Jaw line", fill=NONE,
       stroke=INK, strokeWidth=4, opacity=35, cap="round")
d.path("M300,488 C390,504 610,504 700,488", "Gape", fill=NONE, stroke=INK, strokeWidth=8, cap="round")
d.path("M314,498 C394,512 606,512 686,498", "Gape lip", fill=NONE,
       stroke="#E9B59A", strokeWidth=3, opacity=50, cap="round")
d.path("M300,488 C292,492 286,500 284,510", "Gape corner L", fill=NONE, stroke=INK, strokeWidth=5, opacity=65, cap="round")
d.path("M700,488 C708,492 714,500 716,510", "Gape corner R", fill=NONE, stroke=INK, strokeWidth=5, opacity=65, cap="round")
d.path("M487,486 C491,474 509,474 513,486 L506,514 C503,522 497,522 494,514 Z",
       "Beak", fill=BEAK_GRAD, stroke=INK, strokeWidth=3)
d.path("M495,482 C498,478 502,478 505,482", "Beak sheen", fill=NONE, stroke="#A89E8C", strokeWidth=2, opacity=60, cap="round")
for i, dd in enumerate(["M304,480 C286,468 270,464 256,466", "M306,488 C288,482 272,482 260,488",
                        "M696,480 C714,468 730,464 744,466", "M694,488 C712,482 728,482 740,488"]):
    d.path(dd, f"Rictal bristle {i+1}", fill=NONE, stroke="#4A4238", strokeWidth=2, opacity=55, cap="round")

# --- the broken branch: both ends close on the disc's own arc ------------------------------
d.path("M187,740 C400,728 600,728 813,740 A420,420 0 0 1 760,790 "
       "C600,782 400,782 240,790 A420,420 0 0 1 187,740 Z",
       "Branch", fill=BARK_GRAD, stroke=INK, strokeWidth=5)
for i, dd in enumerate(["M220,752 C300,748 360,750 420,756", "M560,756 C640,750 720,748 790,752",
                        "M260,772 C330,768 380,770 430,774", "M600,774 C660,770 720,768 770,772"]):
    d.path(dd, f"Bark groove {i+1}", fill=NONE, stroke="#2A221A", strokeWidth=3, opacity=45, cap="round")
d.path("M200,738 C400,726 600,726 800,738", "Branch top light", fill=NONE,
       stroke="#B9AA92", strokeWidth=4, opacity=45, cap="round")
d.shape("ellipse", "Lichen L", x=244, y=738, width=60, height=18, fill="#A9B88A", opacity=45, stroke=NONE)
d.shape("ellipse", "Lichen R", x=700, y=742, width=48, height=14, fill="#A9B88A", opacity=40, stroke=NONE)
# toes gripping over the branch
for i, x in enumerate([446, 462, 478, 522, 538, 554]):
    d.shape("ellipse", f"Toe {i+1}", x=x-7, y=728, width=14, height=18, fill="#6A6153", stroke=INK, strokeWidth=3)

# --- name -------------------------------------------------------------------------------
d.text("POTOO", "Name", x=500, y=962, size=60, font="Virelai Sans",
       color="#DCE0CF", justify="center")

d.finish("potoo-V1R00")
