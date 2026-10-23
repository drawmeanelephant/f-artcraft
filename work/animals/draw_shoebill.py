#!/usr/bin/env python3
"""Shoebill — field-guide plate V1R00. Bust portrait, dead front-on: the
massive clog-shaped bill hanging toward the viewer, pale yellow unblinking
eyes under a heavy brow, slate-grey plumage, papyrus marsh behind.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Shoebill — Field Plate", 1000, 1000)

INK = "#1E252B"
CX, CY, R = 500, 460, 420          # plate disc
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1B242A"}, {"offset": 1, "color": "#080C0F"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E6ECE6"}, {"offset": 0.7, "color": "#BFCCC6"},
    {"offset": 1, "color": "#86999A"}]}}
PLUME_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#A3AEB7"}, {"offset": 0.65, "color": "#76828D"},
    {"offset": 1, "color": "#4E5862"}]}}
BODY_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7C8893"}, {"offset": 1, "color": "#47515B"}]}}
BILL_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E2D8BE"}, {"offset": 0.6, "color": "#B5A88A"},
    {"offset": 1, "color": "#7D7059"}]}}
IRIS_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#FFF8C8"}, {"offset": 0.6, "color": "#F1DE7A"},
    {"offset": 1, "color": "#C9A93E"}]}}
PAPYRUS_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#93A79A"}, {"offset": 1, "color": "#6A7E72"}]}}

def chord_x(y, r):
    h = math.sqrt(r*r - (y - CY)**2)
    return CX - h, CX + h

def inside(x, y, r=388):
    dx, dy = x - CX, y - CY
    k = math.hypot(dx, dy)
    return (x, y) if k <= r else (CX + dx*r/k, CY + dy*r/k)

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#5D7073", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F2F6F2", strokeWidth=3, opacity=55)
# layered low-opacity mist so the band has a soft edge
for i, (x, y, w, h) in enumerate([(160,560,680,90),(200,550,600,110),(250,540,500,130)]):
    d.shape("ellipse", f"Mist band {i+1}", x=x, y=y, width=w, height=h, fill="#FFFFFF", opacity=8, stroke=NONE)
for i, (x, y, w) in enumerate([(190,300,8),(780,260,7),(160,540,9),(830,540,8),(140,420,6),
                               (860,400,7),(380,110,7),(610,105,8),(260,190,6),(730,180,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w, fill="#6C8082", opacity=40, stroke=NONE)

# papyrus: stems + radiating umbels, every point pulled inside the inner ring
def papyrus(base, top, spread, n, label, op):
    bx, by = base; tx, ty = top
    d.path(f"M{bx},{by} Q{(bx+tx)/2 + 10:.0f},{(by+ty)/2:.0f} {tx},{ty}", f"{label} stem",
           fill=NONE, stroke="#6A7E72", strokeWidth=6, opacity=op, cap="round")
    for k in range(n):
        a = math.radians(-90 - spread/2 + spread*k/(n - 1))
        ex, ey = inside(tx + 74*math.cos(a), ty + 74*math.sin(a))
        mx, my = tx + 40*math.cos(a + 0.12), ty + 40*math.sin(a + 0.12) - 6
        d.path(f"M{tx},{ty} Q{mx:.0f},{my:.0f} {ex:.0f},{ey:.0f}", f"{label} ray {k+1}",
               fill=NONE, stroke=PAPYRUS_GRAD, strokeWidth=4, opacity=op, cap="round")

papyrus((250, 720), (232, 360), 150, 9, "Papyrus L1", 70)
papyrus((300, 700), (318, 250), 140, 9, "Papyrus L2", 45)
papyrus((750, 720), (770, 350), 150, 9, "Papyrus R1", 70)
papyrus((700, 700), (684, 240), 140, 9, "Papyrus R2", 45)

# --- body: neck + shoulders, closed on the disc's own arc --------------------------
by = 790
bl, br = chord_x(by, 417)
d.path(f"M{bl:.1f},{by} C{bl+6:.0f},700 300,622 382,566 C398,526 408,484 418,440 L582,440 "
       f"C592,484 602,526 618,566 C700,622 {br-6:.0f},700 {br:.1f},{by} A417,417 0 0 1 {bl:.1f},{by} Z",
       "Body", fill=BODY_GRAD, stroke=INK, strokeWidth=7)
# wing-covert scallops on the shoulders
for row, (y0, xs) in enumerate([(650, [300, 350, 650, 700]), (700, [280, 330, 380, 620, 670, 720]),
                                 (750, [300, 350, 400, 600, 650, 700])]):
    for j, x in enumerate(xs):
        d.path(f"M{x-26},{y0} C{x-18},{y0+24} {x+18},{y0+24} {x+26},{y0}",
               f"Covert r{row+1} {j+1}", fill=NONE, stroke="#38414A", strokeWidth=5,
               opacity=50, cap="round")
        d.path(f"M{x-18},{y0-4} C{x-10},{y0+8} {x+10},{y0+8} {x+18},{y0-4}",
               f"Covert light r{row+1} {j+1}", fill=NONE, stroke="#B9C3CB", strokeWidth=3,
               opacity=30, cap="round")
d.path("M300,640 C330,606 360,584 390,570", "Shoulder sheen L", fill=NONE,
       stroke="#C3CDD5", strokeWidth=8, opacity=30, cap="round")
d.path("M700,640 C670,606 640,584 610,570", "Shoulder sheen R", fill=NONE,
       stroke="#C3CDD5", strokeWidth=8, opacity=30, cap="round")
# neck feather streaks
for i, x in enumerate([430, 452, 548, 570]):
    d.path(f"M{x},470 C{x + (x-500)*0.1:.0f},520 {x + (x-500)*0.25:.0f},560 {x + (x-500)*0.4:.0f},600",
           f"Neck streak {i+1}", fill=NONE, stroke="#4E5862", strokeWidth=4, opacity=40, cap="round")

# --- nape crest (behind the head) ---------------------------------------------------
d.path("M462,232 L470,186 L488,222 L500,170 L514,220 L534,184 L540,234 Z",
       "Crest", fill=PLUME_GRAD, stroke=INK, strokeWidth=5)

# --- head ----------------------------------------------------------------------
d.path("M500,214 C590,214 652,262 656,334 C660,400 620,452 560,472 "
       "L440,472 C380,452 340,400 344,334 C348,262 410,214 500,214 Z",
       "Head", fill=PLUME_GRAD, stroke=INK, strokeWidth=8)
d.path("M420,236 C460,220 540,220 580,236", "Crown sheen", fill=NONE,
       stroke="#DCE3E8", strokeWidth=9, opacity=35, cap="round")
d.path("M356,380 C366,420 392,448 428,464", "Cheek shade L", fill=NONE,
       stroke="#3E4750", strokeWidth=10, opacity=30, cap="round")
d.path("M644,380 C634,420 608,448 572,464", "Cheek shade R", fill=NONE,
       stroke="#3E4750", strokeWidth=10, opacity=30, cap="round")
for i, (x, y) in enumerate([(380,280),(410,262),(590,262),(620,280),(370,410),(630,410)]):
    d.path(f"M{x-10},{y} C{x-6},{y+8} {x+6},{y+8} {x+10},{y}", f"Head feather {i+1}",
           fill=NONE, stroke="#56616B", strokeWidth=3, opacity=45, cap="round")

# --- eyes: pale, round, unblinking ---------------------------------------------------
for side, cx in (("L", 408), ("R", 592)):
    cy = 334
    d.shape("ellipse", f"Eye socket {side}", x=cx - 32, y=cy - 30, width=64, height=60,
            fill="#3E4750", opacity=35, stroke=NONE)
    d.shape("ellipse", f"Eye {side}", x=cx - 24, y=cy - 24, width=48, height=48,
            fill=IRIS_GRAD, stroke=INK, strokeWidth=5)
    d.shape("ellipse", f"Pupil {side}", x=cx - 7, y=cy - 7, width=14, height=14,
            fill="#0A0D10", stroke=NONE)
    d.shape("ellipse", f"Glint {side}", x=cx - 12, y=cy - 13, width=7, height=7,
            fill="#FFFFFF", opacity=90, stroke=NONE)
    # heavy, dead-level brow ridge: no expression, just the stare
    s = -1 if side == "L" else 1
    d.path(f"M{cx - s*30},{cy - 22} C{cx - s*10},{cy - 34} {cx + s*14},{cy - 32} {cx + s*34},{cy - 20}",
           f"Brow {side}", fill=NONE, stroke=INK, strokeWidth=8, cap="round")
    d.path(f"M{cx - s*26},{cy - 30} C{cx - s*8},{cy - 40} {cx + s*12},{cy - 38} {cx + s*30},{cy - 28}",
           f"Brow light {side}", fill=NONE, stroke="#C3CDD5", strokeWidth=4, opacity=40, cap="round")

# --- the bill: a clog hanging toward the viewer ------------------------------------
d.shape("ellipse", "Bill shadow", x=410, y=470, width=180, height=220, fill="#1E252B", opacity=22, stroke=NONE)
d.path("M455,310 C475,300 525,300 545,310 C585,340 606,420 600,500 "
       "C596,560 568,612 530,636 C520,650 512,662 500,668 "
       "C488,662 480,650 470,636 C432,612 404,560 400,500 "
       "C394,420 415,340 455,310 Z",
       "Bill", fill=BILL_GRAD, stroke=INK, strokeWidth=7)
# gape lines: the lower mandible edge showing at the sides
d.path("M406,520 C414,578 446,618 484,644", "Gape L", fill=NONE,
       stroke="#5B503F", strokeWidth=5, opacity=80, cap="round")
d.path("M594,520 C586,578 554,618 516,644", "Gape R", fill=NONE,
       stroke="#5B503F", strokeWidth=5, opacity=80, cap="round")
# side shading + top light
d.path("M416,400 C406,450 408,500 420,550", "Bill shade L", fill=NONE,
       stroke="#6E624D", strokeWidth=14, opacity=30, cap="round")
d.path("M584,400 C594,450 592,500 580,550", "Bill shade R", fill=NONE,
       stroke="#6E624D", strokeWidth=14, opacity=30, cap="round")
d.path("M470,322 C490,314 510,314 530,322", "Bill top light", fill=NONE,
       stroke="#FFF8E6", strokeWidth=6, opacity=45, cap="round")
# culmen ridge with a lit flank
d.path("M500,316 C505,400 505,520 500,640", "Culmen", fill=NONE,
       stroke="#6E624D", strokeWidth=5, opacity=75, cap="round")
d.path("M512,330 C518,410 518,520 512,620", "Culmen light", fill=NONE,
       stroke="#FFF8E6", strokeWidth=5, opacity=35, cap="round")
# mottled blotches
for i, (x, y, w, h) in enumerate([(440,420,22,16),(552,452,26,18),(456,520,18,14),
                                  (536,560,20,15),(470,470,12,10),(528,392,14,11)]):
    d.shape("ellipse", f"Bill blotch {i+1}", x=x, y=y, width=w, height=h,
            fill="#7A6C55", opacity=30, stroke=NONE)
# hooked nail at the tip
d.path("M484,642 C492,654 508,654 516,642 C514,662 507,674 500,680 "
       "C493,674 486,662 484,642 Z",
       "Bill hook", fill="#5E5342", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Nostril L", x=478, y=344, width=6, height=16, fill="#3E3528", opacity=70, stroke=NONE)
d.shape("ellipse", "Nostril R", x=516, y=344, width=6, height=16, fill="#3E3528", opacity=70, stroke=NONE)

# --- name ----------------------------------------------------------------------
d.text("SHOEBILL", "Name", x=500, y=962, size=58, font="Virelai Sans",
       color="#DCE6E4", justify="center")

d.finish("shoebill-V1R00")
