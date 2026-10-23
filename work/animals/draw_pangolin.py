#!/usr/bin/env python3
"""Pangolin — field-guide plate V1R00. Full-body side profile, walking pose,
overlapping scale shingles, long curved tail. Warm bronze/ochre palette.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Pangolin — Field Plate", 1000, 1000)

INK = "#3B2210"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2B1B0E"}, {"offset": 1, "color": "#100804"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#EBDCB2"}, {"offset": 0.7, "color": "#CDAB6E"},
    {"offset": 1, "color": "#94703E"}]}}
FUR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#8E6B41"}, {"offset": 1, "color": "#5B3C20"}]}}
BODY_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#9C7847"}, {"offset": 0.75, "color": "#7A5830"},
    {"offset": 1, "color": "#54371B"}]}}
TAIL_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#B98A49"}, {"offset": 1, "color": "#6B421D"}]}}
SCALE_A = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E0AD61"}, {"offset": 1, "color": "#96632A"}]}}
SCALE_B = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#C98F49"}, {"offset": 1, "color": "#7C5222"}]}}
SCALE_C = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#EFCB87"}, {"offset": 1, "color": "#AB7738"}]}}

# --- backdrop + plate ----------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#6E4F28", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F0E3BD", strokeWidth=3, opacity=55)
# plate patina: soft blotches + speckles
d.shape("ellipse", "Patina 1", x=170, y=170, width=240, height=150, fill="#A8814C", opacity=22, stroke=NONE)
d.shape("ellipse", "Patina 2", x=620, y=650, width=250, height=140, fill="#A8814C", opacity=20, stroke=NONE)
for i, (x, y, w) in enumerate([(210,300,8),(770,240,7),(180,560,9),(800,570,8),(250,770,7),(730,750,9),
                               (140,430,6),(860,410,7),(410,120,7),(600,110,8),(340,830,6),(670,830,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w, fill="#8A6231", opacity=40, stroke=NONE)
# ground shadow under the animal (kept inside the plate edge)
d.shape("ellipse", "Ground shadow", x=265, y=694, width=550, height=54, fill="#1A0F06", opacity=45, stroke=NONE)

# --- scale helper: domed shingle, tip at bottom; deg<0 swings tip toward tail -----
def scale_path(cx, cy, w, h, deg=0):
    t = math.radians(deg); c, s = math.cos(t), math.sin(t)
    def R(px, py):
        dx, dy = px - cx, py - cy
        return (cx + dx * c - dy * s, cy + dx * s + dy * c)
    f = lambda p: f"{p[0]:.0f},{p[1]:.0f}"
    TL, cTL, AP = (cx - w/2, cy - h*0.18), (cx - w/2, cy - h/2), (cx, cy - h/2)
    cTR, TR = (cx + w/2, cy - h/2), (cx + w/2, cy - h*0.18)
    cR, BT, cL = (cx + w*0.30, cy + h/2), (cx, cy + h/2), (cx - w*0.30, cy + h/2)
    pts = [R(*p) for p in (TL, cTL, AP, cTR, TR, cR, BT, cL)]
    return (f"M{f(pts[0])} Q{f(pts[1])} {f(pts[2])} Q{f(pts[3])} {f(pts[4])} "
            f"Q{f(pts[5])} {f(pts[6])} Q{f(pts[7])} {f(pts[0])} Z")

# --- tail first (body base will overlap its root) --------------------------------
d.path("M648,468 C752,494 815,576 820,664 C823,706 806,726 775,718 "
       "C724,704 672,678 646,646 C628,624 632,556 648,468 Z",
       "Tail", fill=TAIL_GRAD, stroke=INK, strokeWidth=7)
# tail scale shingles along the exposed tail (body is drawn over the root)
for i, (x, y, w, h, dg) in enumerate([
        (735, 530, 58, 50, -25), (785, 575, 56, 48, -40), (810, 632, 50, 44, -55),
        (800, 688, 46, 40, -65),
        (725, 600, 56, 50, -20), (770, 645, 52, 46, -35), (778, 700, 44, 38, -52)]):
    d.path(scale_path(x, y, w, h, dg), f"Tail scale {i+1}",
           fill=SCALE_B if i % 2 else SCALE_A, stroke=INK, strokeWidth=3)
# tail underside shading
d.path("M656,630 C706,678 742,700 780,708", "Tail underside shade",
       fill=NONE, stroke="#54371B", strokeWidth=14, opacity=35, cap="round")

# --- legs (drawn before the body so belly overlaps the tops) ----------------------
# far-side legs darker
d.path("M428,586 C414,624 408,662 412,694 C415,714 436,716 444,700 C454,668 458,626 460,592 Z",
       "Front leg far", fill="#54371B", stroke=INK, strokeWidth=6)
d.path("M664,580 C676,616 682,656 680,690 C679,710 658,714 650,698 C640,668 638,624 640,588 Z",
       "Hind leg far", fill="#54371B", stroke=INK, strokeWidth=6)
# near-side legs, walking: front reaches forward, hind planted
d.path("M372,576 C356,606 342,646 336,682 C332,706 350,718 366,704 C382,676 394,630 400,590 Z",
       "Front leg", fill=FUR_GRAD, stroke=INK, strokeWidth=7)
d.path("M586,586 C600,618 606,656 604,690 C602,714 578,718 568,700 C556,672 552,626 556,590 Z",
       "Hind leg", fill=FUR_GRAD, stroke=INK, strokeWidth=7)
# claws: pale keratin strokes on each foot
for i, (x, y, x2, y2) in enumerate([(340,700,320,712),(352,706,334,720),(366,708,352,722),
                                    (570,704,552,714),(582,708,566,720),(596,708,584,720),
                                    (416,698,400,708),(654,696,640,706)]):
    d.path(f"M{x},{y} L{x2},{y2}", f"Claw {i+1}", fill=NONE,
           stroke="#EAD9B8", strokeWidth=5, cap="round")

# --- body dome -------------------------------------------------------------------
d.path("M332,604 C328,470 412,346 536,338 C652,330 730,414 742,520 "
       "C748,586 726,644 678,664 C570,700 428,694 356,662 C338,650 332,628 332,604 Z",
       "Body", fill=BODY_GRAD, stroke=INK, strokeWidth=7)
# belly fur: warm lighter crescent under the scales
d.path("M368,650 C450,684 580,688 668,656 C610,678 470,682 368,650 Z",
       "Belly shade", fill="#A8845A", opacity=55, stroke=NONE)

# --- scale shingles: staggered rows over the dome, bottom row first ----------------
# (y, scale_w, scale_h, x_start, x_end) — ranges hand-clamped inside the body edge
rows = [(640, 60, 54, 400, 640),
        (598, 62, 56, 390, 690),
        (556, 64, 58, 372, 700),
        (514, 64, 58, 360, 698),
        (472, 62, 56, 372, 690),
        (430, 60, 54, 376, 676),
        (395, 52, 46, 430, 620)]
n = 0
for ri, (y, w, h, x0, x1) in enumerate(rows):
    x = x0 + (ri % 2) * 27
    while x <= x1:
        n += 1
        grad = SCALE_C if ri >= 5 else (SCALE_A if (ri + n) % 2 == 0 else SCALE_B)
        d.path(scale_path(x, y, w, h), f"Scale {n}", fill=grad, stroke=INK, strokeWidth=3)
        x += 54
# soft top-light along the back crest
d.path("M352,556 C366,440 448,356 545,346 C636,338 706,404 734,492",
       "Back ridge light", fill=NONE, stroke="#F0D9A0", strokeWidth=7, opacity=22, cap="round")

# --- head: small, pointed snout, attached at the shoulder -------------------------
d.path("M362,462 C322,452 284,472 264,512 C248,544 242,576 252,598 "
       "C264,622 296,626 322,614 C344,640 372,652 398,642 "
       "C424,630 434,584 424,544 C416,508 392,474 362,462 Z",
       "Head", fill=FUR_GRAD, stroke=INK, strokeWidth=7)
# crown scales (small)
for i, (x, y) in enumerate([(305, 490), (328, 472), (288, 508)]):
    d.path(scale_path(x, y, 30, 26), f"Head scale {i+1}", fill=SCALE_B, stroke=INK, strokeWidth=3)
# ear, eye, nostril, jaw line
d.shape("ellipse", "Ear", x=352, y=478, width=30, height=24, fill="#7A5830", stroke=INK, strokeWidth=5)
d.shape("ellipse", "Eye", x=292, y=536, width=24, height=24, fill="#1E1208", stroke=NONE)
d.shape("ellipse", "Eye glint", x=297, y=541, width=7, height=7, fill="#FFFFFF", opacity=85, stroke=NONE)
d.shape("ellipse", "Nostril", x=250, y=582, width=10, height=8, fill="#241407", stroke=NONE)
d.path("M258,600 C280,614 308,614 330,602", "Jaw line", fill=NONE, stroke=INK, strokeWidth=5, cap="round")
# throat shading
d.path("M330,614 C352,632 380,640 402,634", "Throat shade", fill=NONE,
       stroke="#54371B", strokeWidth=10, opacity=35, cap="round")

# --- name ---------------------------------------------------------------------------
d.text("PANGOLIN", "Name", x=500, y=962, size=60, font="Virelai Sans",
       color="#E3CD9C", justify="center")

d.finish("pangolin-V1R00")
