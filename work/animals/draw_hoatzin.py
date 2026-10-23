#!/usr/bin/env python3
"""Hoatzin — field-guide plate V1R00. Full body, perched profile facing left:
spiky rufous mohawk crest with dark tips, red eye in bare blue facial skin,
buff breast, chestnut flanks and wing, long dark tail with a buff tip hanging
behind a mossy branch. Humid riverside canopy: hanging vines, broad leaves,
a slow brown river closing on the disc's own arc.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Hoatzin — Field Plate", 1000, 1000)

INK = "#2A1A12"
CX, CY, R = 500, 460, 420
BG_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#1C2A18"}, {"offset": 1, "color": "#0A1008"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F6EECA"}, {"offset": 0.6, "color": "#CFCB92"},
    {"offset": 1, "color": "#7C8C56"}]}}
RIVER_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#9A8A5E"}, {"offset": 1, "color": "#5E5A3A"}]}}
LEAF_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6E9A50"}, {"offset": 1, "color": "#3E6A38"}]}}
BRANCH_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#8C6440"}, {"offset": 0.5, "color": "#6A4A2E"},
    {"offset": 1, "color": "#3E2A1A"}]}}
TAIL_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5A3A24"}, {"offset": 1, "color": "#2E1E14"}]}}
BODY_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#C86E3A"}, {"offset": 0.65, "color": "#A4522A"},
    {"offset": 1, "color": "#6E3418"}]}}
BREAST_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#FAE6BC"}, {"offset": 0.7, "color": "#EACB90"},
    {"offset": 1, "color": "#C8A066"}]}}
WING_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6A4A30"}, {"offset": 1, "color": "#3E2A1C"}]}}
PRIMARY_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#C2582A"}, {"offset": 1, "color": "#86361A"}]}}
HEAD_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#D8A870"}, {"offset": 0.7, "color": "#B07C48"},
    {"offset": 1, "color": "#7E5230"}]}}
CREST_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#2A1A10"}, {"offset": 0.35, "color": "#B8622E"},
    {"offset": 1, "color": "#E8A060"}]}}
SKIN_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#8ED8F2"}, {"offset": 1, "color": "#2E86C0"}]}}
IRIS_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#FF6A50"}, {"offset": 0.7, "color": "#D41E1E"},
    {"offset": 1, "color": "#7A0A0A"}]}}
BILL_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#7A7064"}, {"offset": 1, "color": "#3E3830"}]}}

def rim_x(y, r=R, side=-1):
    return CX + side*math.sqrt(r*r - (y - CY)**2)

def rim_y(x, r=R):
    return CY - math.sqrt(r*r - (x - CX)**2)

def inside(x, y, r=386):
    dx, dy = x - CX, y - CY
    k = math.hypot(dx, dy)
    return (x, y) if k <= r else (CX + dx*r/k, CY + dy*r/k)

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#5A6A3A", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#FBF6E0", strokeWidth=3, opacity=55)
# humid haze
for i, (x, y, w, h, o) in enumerate([(180,200,280,120,16),(560,300,260,110,14),(260,440,480,120,10)]):
    d.shape("ellipse", f"Humid haze {i+1}", x=x, y=y, width=w, height=h, fill="#FFFBE6", opacity=o, stroke=NONE)

# hanging vines: tops start on the disc's arc, tips end inside
for i, (x, length, sway, op) in enumerate([(250, 260, 18, 45), (300, 180, -12, 35), (700, 300, -20, 45),
                                           (760, 200, 14, 35), (650, 140, 10, 30)]):
    y0 = rim_y(x) + 4
    d.path(f"M{x},{y0:.0f} C{x + sway},{y0 + length*0.35:.0f} {x - sway},{y0 + length*0.7:.0f} {x + sway*0.5:.0f},{y0 + length:.0f}",
           f"Vine {i+1}", fill=NONE, stroke="#4E6A34", strokeWidth=4, opacity=op, cap="round")
    for j in range(3):
        t = 0.3 + j*0.25
        vx, vy = x + sway*(0.6 - t), y0 + length*t
        s = 1 if j % 2 else -1
        d.path(f"M{vx:.0f},{vy:.0f} Q{vx + s*16:.0f},{vy - 4:.0f} {vx + s*24:.0f},{vy + 10:.0f} "
               f"Q{vx + s*10:.0f},{vy + 10:.0f} {vx:.0f},{vy:.0f} Z",
               f"Vine {i+1} leaf {j+1}", fill=LEAF_GRAD, opacity=op, stroke=NONE)

# broad leaves at the sides, all points kept inside the inner ring
def leaf(label, base, tip, width, op):
    bx, by = base; tx, ty = tip
    mx, my = (bx + tx)/2, (by + ty)/2
    nx, ny = -(ty - by), tx - bx
    ln = math.hypot(nx, ny) or 1
    nx, ny = nx/ln*width, ny/ln*width
    p1 = inside(mx + nx, my + ny); p2 = inside(mx - nx, my - ny); t = inside(tx, ty)
    d.path(f"M{bx},{by} Q{p1[0]:.0f},{p1[1]:.0f} {t[0]:.0f},{t[1]:.0f} Q{p2[0]:.0f},{p2[1]:.0f} {bx},{by} Z",
           label, fill=LEAF_GRAD, opacity=op, stroke=NONE)
    d.path(f"M{bx},{by} L{t[0]:.0f},{t[1]:.0f}", f"{label} vein", fill=NONE,
           stroke="#2E4A26", strokeWidth=2, opacity=op*0.6, cap="round")

leaf("Leaf L1", (170, 470), (250, 360), 44, 50)
leaf("Leaf L2", (160, 520), (270, 500), 34, 40)
leaf("Leaf R1", (840, 420), (760, 330), 44, 50)
leaf("Leaf R2", (850, 470), (740, 460), 34, 40)

# --- river: closes on the disc's own arc ----------------------------------------------
ry = 760
rl, rr = rim_x(ry, side=-1), rim_x(ry, side=1)
d.path(f"M{rl:.1f},{ry} C380,750 620,750 {rr:.1f},{ry} A420,420 0 0 1 {rl:.1f},{ry} Z",
       "River", fill=RIVER_GRAD, opacity=88, stroke=NONE)
for i, (x, y, w) in enumerate([(300,786,90),(470,800,120),(640,790,80),(380,830,70),(560,840,90)]):
    d.path(f"M{x},{y} C{x + w*0.3:.0f},{y - 4} {x + w*0.7:.0f},{y - 4} {x + w},{y}",
           f"River glint {i+1}", fill=NONE, stroke="#F2E6C0", strokeWidth=3, opacity=40, cap="round")
# hoatzin reflection, faint
d.shape("ellipse", "Reflection", x=400, y=780, width=200, height=40, fill="#4A3020", opacity=18, stroke=NONE)

# --- tail: long, broad, hangs behind the branch ----------------------------------------
d.path("M548,466 C612,506 680,590 726,690 C736,714 718,736 694,730 "
       "C672,724 654,714 642,702 C612,640 572,580 520,520 Z",
       "Tail", fill=TAIL_GRAD, stroke=INK, strokeWidth=5)
d.path("M648,694 C664,706 680,716 696,720 C714,724 728,712 724,694 "
       "C716,676 706,662 696,650 C690,676 672,690 648,694 Z",
       "Tail buff tip", fill="#E8C890", opacity=85, stroke=NONE)
for i, dd in enumerate(["M560,500 C610,550 652,610 680,680", "M548,512 C592,560 630,620 660,690",
                        "M572,488 C628,536 670,600 702,670"]):
    d.path(dd, f"Tail feather line {i+1}", fill=NONE, stroke="#1E140C", strokeWidth=3, opacity=40, cap="round")
d.path("M576,486 C630,530 672,594 706,664", "Tail sheen", fill=NONE,
       stroke="#B08A60", strokeWidth=4, opacity=30, cap="round")

# --- branch: crosses the disc, both ends close on the disc's own arc --------------------
y_tl, y_bl, y_tr, y_br = 606, 648, 556, 598
xl_t, xl_b = rim_x(y_tl, 418, -1), rim_x(y_bl, 418, -1)
xr_t, xr_b = rim_x(y_tr, 418, 1), rim_x(y_br, 418, 1)
d.path(f"M{xl_t:.1f},{y_tl} C300,596 640,560 {xr_t:.1f},{y_tr} "
       f"A418,418 0 0 1 {xr_b:.1f},{y_br} C640,604 300,640 {xl_b:.1f},{y_bl} "
       f"A418,418 0 0 1 {xl_t:.1f},{y_tl} Z",
       "Branch", fill=BRANCH_GRAD, stroke=NONE)
d.path(f"M{xl_t + 6:.1f},{y_tl - 1} C300,596 640,560 {xr_t - 6:.1f},{y_tr - 1}", "Branch top edge",
       fill=NONE, stroke=INK, strokeWidth=4, opacity=80, cap="round")
d.path(f"M{xl_b + 6:.1f},{y_bl - 1} C300,640 640,604 {xr_b - 6:.1f},{y_br - 1}", "Branch bottom edge",
       fill=NONE, stroke=INK, strokeWidth=4, opacity=80, cap="round")
d.path("M140,612 C320,600 620,568 880,562", "Branch light", fill=NONE,
       stroke="#D8B488", strokeWidth=5, opacity=35, cap="round")
for i, (x, y, w) in enumerate([(200,624,40),(330,612,50),(560,594,44),(700,584,36),(800,578,30)]):
    d.path(f"M{x},{y} C{x + w*0.3:.0f},{y + 6} {x + w*0.7:.0f},{y + 6} {x + w},{y + 2}",
           f"Bark ridge {i+1}", fill=NONE, stroke="#2E1E12", strokeWidth=3, opacity=40, cap="round")
for i, (x, y, w, h) in enumerate([(240,600,70,16),(600,572,60,14),(760,566,50,12)]):
    d.shape("ellipse", f"Moss {i+1}", x=x, y=y, width=w, height=h, fill="#7EA048", opacity=55, stroke=NONE)
# re-stroke the rim so the branch ends sit cleanly under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#5A6A3A", strokeWidth=6)

# --- body + neck ---------------------------------------------------------------------
d.path("M302,312 C306,350 328,384 356,408 C350,452 380,520 440,566 "
       "C482,594 540,590 586,560 C616,540 626,500 602,470 "
       "C562,420 482,380 420,350 C392,334 378,310 374,286 Z",
       "Body", fill=BODY_GRAD, stroke=INK, strokeWidth=6)
# buff throat + breast
d.path("M302,312 C306,350 328,384 356,408 C350,452 380,520 440,566 "
       "C472,540 456,470 424,420 C392,380 366,344 356,300 Z",
       "Breast", fill=BREAST_GRAD, opacity=92, stroke=NONE)
for i, (x, y) in enumerate([(326,340),(340,370),(360,400),(372,440),(390,480),(412,516)]):
    d.path(f"M{x},{y} C{x + 4},{y + 8} {x + 10},{y + 12} {x + 16},{y + 14}", f"Breast streak {i+1}",
           fill=NONE, stroke="#B88A54", strokeWidth=3, opacity=45, cap="round")
d.path("M460,560 C510,576 560,566 590,540", "Belly shade", fill=NONE,
       stroke="#5A2810", strokeWidth=10, opacity=25, cap="round")
# nape streaks: buff shaft lines on the dark back of the neck
for i, (x, y) in enumerate([(380,300),(392,322),(410,340)]):
    d.path(f"M{x},{y} C{x + 8},{y + 6} {x + 16},{y + 10} {x + 26},{y + 12}", f"Nape streak {i+1}",
           fill=NONE, stroke="#F2D8A8", strokeWidth=3, opacity=55, cap="round")

# --- folded wing ------------------------------------------------------------------------
d.path("M398,390 C462,370 540,398 592,448 C622,478 642,518 652,552 "
       "C612,550 562,532 520,510 C460,478 418,440 398,390 Z",
       "Wing", fill=WING_GRAD, stroke=INK, strokeWidth=5)
d.path("M560,468 C598,492 630,522 652,552 C612,550 572,532 540,514 Z",
       "Wing primaries", fill=PRIMARY_GRAD, stroke=NONE)
for i, dd in enumerate(["M560,486 C590,506 616,528 636,550", "M548,500 C576,516 600,534 616,550"]):
    d.path(dd, f"Primary edge {i+1}", fill=NONE, stroke="#5A2410", strokeWidth=3, opacity=50, cap="round")
# covert scallops with buff fringes
for row, (pts) in enumerate([[(430,402),(462,398),(494,404),(526,416)],
                             [(444,430),(476,428),(508,436),(540,450)],
                             [(468,460),(500,462),(532,472)]]):
    for j, (x, y) in enumerate(pts):
        d.path(f"M{x-14},{y} C{x-8},{y+12} {x+8},{y+12} {x+14},{y}", f"Covert r{row+1} {j+1}",
               fill=NONE, stroke="#F0D2A0", strokeWidth=3, opacity=70, cap="round")
d.path("M420,388 C470,378 530,396 576,432", "Wing sheen", fill=NONE,
       stroke="#C8A078", strokeWidth=5, opacity=30, cap="round")

# --- legs + feet gripping the branch -------------------------------------------------------
for side, (x0, xf) in (("far", (500, 498)), ("near", (468, 462))):
    yb = 606 - (xf - 108) * 50 / 800 - 4
    d.path(f"M{x0},{560} C{x0 - 2},{572} {xf + 2},{yb - 10:.0f} {xf},{yb:.0f}",
           f"Leg {side}", fill=NONE, stroke="#5A4E44" if side == "near" else "#3E342C",
           strokeWidth=9, cap="round")
    for k, (dx, dy) in enumerate([(-18, 10), (-6, 14), (10, 12)]):
        d.path(f"M{xf},{yb:.0f} Q{xf + dx*0.6:.0f},{yb - 2:.0f} {xf + dx},{yb + dy:.0f}",
               f"Toe {side} {k+1}", fill=NONE, stroke="#4A4038", strokeWidth=5, cap="round")

# --- crest: wild mohawk of rufous spikes with dark tips (behind the head) ----------------------
CROWN = (332, 252)
for k, (tx, ty, w) in enumerate([(286,176,17),(304,156,18),(326,144,19),(350,142,19),
                                 (374,150,18),(394,166,17),(410,190,15),(418,216,13)]):
    bx = CROWN[0] - 26 + k*9
    by = CROWN[1] + abs(k - 3.5)*2
    mx, my = (bx + tx)/2, (by + ty)/2
    nx, ny = -(ty - by), tx - bx
    ln = math.hypot(nx, ny) or 1
    nx, ny = nx/ln*w*0.6, ny/ln*w*0.6
    bend = 6 if k > 3 else -4
    d.path(f"M{bx - w/2:.0f},{by:.0f} Q{mx + nx + bend:.0f},{my + ny:.0f} {tx},{ty} "
           f"Q{mx - nx + bend:.0f},{my - ny:.0f} {bx + w/2:.0f},{by:.0f} Z",
           f"Crest spike {k+1}", fill=CREST_GRAD, stroke=INK, strokeWidth=2.5)

# --- head -----------------------------------------------------------------------------------
d.path("M332,244 C364,244 382,264 380,290 C378,314 358,328 332,328 "
       "C306,328 288,312 288,288 C288,264 302,244 332,244 Z",
       "Head", fill=HEAD_GRAD, stroke=INK, strokeWidth=5)
d.path("M308,256 C324,248 344,248 360,256", "Crown light", fill=NONE,
       stroke="#F6DCB0", strokeWidth=5, opacity=40, cap="round")
# bare blue facial skin around the red eye
# a tight ring of skin around the eye with a short tail sweeping back, so the red iris dominates
d.path("M310,284 C312,270 326,264 340,268 C350,271 356,278 364,282 "
       "C356,284 352,288 350,294 C346,306 324,310 314,300 C310,296 309,290 310,284 Z",
       "Facial skin", fill=SKIN_GRAD, stroke="#1E5E8E", strokeWidth=2)
d.shape("ellipse", "Iris", x=317, y=273, width=28, height=28, fill=IRIS_GRAD, stroke=INK, strokeWidth=2.5)
d.shape("ellipse", "Pupil", x=326, y=282, width=10, height=10, fill="#140604", stroke=NONE)
d.shape("ellipse", "Eye glint", x=322, y=278, width=6, height=6, fill="#FFFFFF", opacity=90, stroke=NONE)
for k, (x0, y0, x1, y1) in enumerate([(318,274,312,266),(326,270,324,262),(336,270,338,262),(344,274,350,268)]):
    d.path(f"M{x0},{y0} L{x1},{y1}", f"Lash {k+1}", fill=NONE, stroke="#1A0E08", strokeWidth=2.5, cap="round")
d.path("M352,304 C362,312 372,316 380,316", "Cheek shade", fill=NONE,
       stroke="#5E3A20", strokeWidth=6, opacity=30, cap="round")
# short, stubby bill
d.path("M296,282 C280,282 266,290 260,302 C262,306 266,306 270,304 "
       "C278,302 288,300 298,300 Z", "Upper bill", fill=BILL_GRAD, stroke=INK, strokeWidth=3)
d.path("M296,302 C284,304 274,306 268,308 C276,314 288,314 298,310 Z",
       "Lower bill", fill=BILL_GRAD, stroke=INK, strokeWidth=2.5)
d.path("M292,286 C282,287 272,292 266,298", "Bill sheen", fill=NONE,
       stroke="#D8CEC0", strokeWidth=2, opacity=50, cap="round")

# --- name -----------------------------------------------------------------------------------
# set in three runs: Virelai Sans spaces Z far too loosely, so Z and IN are placed by hand
NAME_X, Z_X, IN_X = 537.5, 532, 573.5
for txt, x, j in (("HOAT", NAME_X, "right"), ("Z", Z_X, "left"), ("IN", IN_X, "left")):
    d.text(txt, f"Name {txt}", x=x, y=962, size=60, font="Virelai Sans",
           color="#F2E8CC", justify=j)

d.finish("hoatzin-V1R00")
