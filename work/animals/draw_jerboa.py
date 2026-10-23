#!/usr/bin/env python3
"""Jerboa — field-guide plate V1R00. Full body, standing tall on a moonlit dune,
facing left: huge ears and eyes, tiny tucked forepaws, oversized hind legs on
long flat feet, and a long tail curling up into its black-and-white banner tuft.
Sand palette rhymes with fennec-fox-V1R00 (same night backdrop + dune plate).
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Jerboa — Field Plate", 1000, 1000)

INK = "#4A3423"
CX, CY = 500, 460          # plate disc centre (r=420)
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#232A45"}, {"offset": 1, "color": "#12152A"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F2E0BC"}, {"offset": 0.7, "color": "#E2C794"},
    {"offset": 1, "color": "#C9A266"}]}}
FUR_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F6E4C2"}, {"offset": 0.7, "color": "#E0BC88"},
    {"offset": 1, "color": "#C0955C"}]}}
FUR_FAR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#C9A06A"}, {"offset": 1, "color": "#A47D4C"}]}}
LEG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F4E6CC"}, {"offset": 1, "color": "#D8B783"}]}}
EAR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#EFD7AE"}, {"offset": 1, "color": "#CFA874"}]}}
EAR_FAR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#D2AE7C"}, {"offset": 1, "color": "#B08858"}]}}
TAIL_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#D9B57F"}, {"offset": 1, "color": "#C49C66"}]}}
TUFT_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4A3A30"}, {"offset": 1, "color": "#1E1714"}]}}

def disc_x(y, side, r=420):
    return CX + side*math.sqrt(r*r - (y - CY)**2)

# Head+ears and body are laid out at a comfortable size, then scaled into place
# so the small round body rides high on the long hind legs.
import re
def _tf(s_, ax, ay, tx, ty):
    def f(dd):
        return re.sub(r"(-?\d+\.?\d*),(-?\d+\.?\d*)",
                      lambda m: "%.1f,%.1f" % (ax + s_*(float(m.group(1)) - ax) + tx,
                                               ay + s_*(float(m.group(2)) - ay) + ty), dd)
    def box(x, y, w, h):
        return dict(x=round(ax + s_*(x - ax) + tx, 1), y=round(ay + s_*(y - ay) + ty, 1),
                    width=round(w*s_, 1), height=round(h*s_, 1))
    return f, box
H, HB = _tf(0.92, 450, 110, 0, 0)
B, BB = _tf(0.82, 450, 380, 0, -20)

# --- backdrop + plate ----------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
for i, (x, y, w) in enumerate([(130,130,7),(870,140,6),(925,330,8),(70,330,5),(170,880,6),
                               (840,890,7),(940,620,5),(60,600,6)]):
    d.path(f"M{x},{y-w} L{x+w},{y} L{x},{y+w} L{x-w},{y} Z", f"Star {i+1}",
           fill="#FFFFFF", opacity=30, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#A9834E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F6ECD6", strokeWidth=3, opacity=60)
# crescent moon, upper left of the plate
d.path("M276,186 A48,48 0 0 0 276,282 A60,60 0 0 1 276,186 Z", "Moon",
       fill="#FFF6DE", opacity=80, stroke=NONE)
d.path("M254,204 A30,30 0 0 0 254,264", "Moon shade", fill=NONE,
       stroke="#E2C794", strokeWidth=5, opacity=40, cap="round")
for i, (x, y, w) in enumerate([(210,330,8),(760,230,7),(160,520,9),(850,470,8),(330,150,7),(640,110,8)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w, fill="#A9834E", opacity=35, stroke=NONE)
# dunes — lower edges ride the plate's own arc so nothing leaks past the rim
y0 = 672
d.path(f"M{disc_x(y0,-1):.1f},{y0} C280,640 400,668 520,652 C640,636 760,656 {disc_x(y0,1):.1f},{y0} "
       f"A420,420 0 0 1 {disc_x(y0,-1):.1f},{y0} Z", "Dune far", fill="#D9B87E", opacity=45, stroke=NONE)
y1 = 748
d.path(f"M{disc_x(y1,-1):.1f},{y1} C280,726 420,736 560,736 C680,736 780,724 {disc_x(y1,1):.1f},{y1} "
       f"A420,420 0 0 1 {disc_x(y1,-1):.1f},{y1} Z", "Dune near", fill="#C9A266", opacity=50, stroke=NONE)
for i, (x, y) in enumerate([(300,790),(380,815),(620,812),(700,790),(480,835)]):
    d.path(f"M{x},{y} q14,-6 28,0", f"Sand ripple {i+1}", fill=NONE,
           stroke="#A9834E", strokeWidth=4, opacity=35, cap="round")
d.shape("ellipse", "Ground shadow", x=418, y=726, width=290, height=24, fill="#8A6A40", opacity=28, stroke=NONE)

# --- long tail curling up into the banner tuft ------------------------------------
def cubic(p0, p1, p2, p3, t):
    u = 1 - t
    x = u**3*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t**3*p3[0]
    y = u**3*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t**3*p3[1]
    dx = 3*u*u*(p1[0]-p0[0]) + 6*u*t*(p2[0]-p1[0]) + 3*t*t*(p3[0]-p2[0])
    dy = 3*u*u*(p1[1]-p0[1]) + 6*u*t*(p2[1]-p1[1]) + 3*t*t*(p3[1]-p2[1])
    return (x, y), (dx, dy)

spine = [(584, 572), (680, 752), (808, 744), (832, 548)]
left, right = [], []
N = 30
for i in range(N + 1):
    t = i / N
    (x, y), (dx, dy) = cubic(*spine, t)
    ln = math.hypot(dx, dy) or 1
    nx, ny = -dy/ln, dx/ln
    w = (16 - 9*t) / 2
    left.append((x + nx*w, y + ny*w)); right.append((x - nx*w, y - ny*w))
dd = "M%.1f,%.1f " % left[0] + " ".join("L%.1f,%.1f" % p for p in left[1:])
dd += " " + " ".join("L%.1f,%.1f" % p for p in reversed(right)) + " Z"
d.path(dd, "Tail", fill=TAIL_GRAD, stroke=INK, strokeWidth=4)
# light stripe along the tail's upper edge
pts = [cubic(*spine, t/10)[0] for t in range(1, 10)]
d.path("M%.1f,%.1f " % pts[0] + " ".join("L%.1f,%.1f" % (x, y - 2) for x, y in pts[1:]),
       "Tail sheen", fill=NONE, stroke="#FFF2D8", strokeWidth=3, opacity=45, cap="round")

# tuft: dark banner then the white tip, along the end tangent
(ex, ey), (tx, ty) = cubic(*spine, 1.0)
ln = math.hypot(tx, ty); ux, uy = tx/ln, ty/ln; nx, ny = -uy, ux
(sx, sy), _ = cubic(*spine, 0.84)
tip = (ex + ux*78, ey + uy*78)
mid = (ex + ux*20, ey + uy*20)
W = 24
d.path(f"M{sx:.1f},{sy:.1f} C{mid[0] + nx*W:.1f},{mid[1] + ny*W:.1f} {tip[0] + nx*W*0.8:.1f},{tip[1] + ny*W*0.8:.1f} "
       f"{tip[0]:.1f},{tip[1]:.1f} C{tip[0] - nx*W*0.8:.1f},{tip[1] - ny*W*0.8:.1f} "
       f"{mid[0] - nx*W:.1f},{mid[1] - ny*W:.1f} {sx:.1f},{sy:.1f} Z",
       "Tail tuft", fill=TUFT_GRAD, stroke=INK, strokeWidth=4)
w0 = (ex + ux*38, ey + uy*38)
d.path(f"M{w0[0] + nx*16:.1f},{w0[1] + ny*16:.1f} C{tip[0] + nx*16:.1f},{tip[1] + ny*16 + 6:.1f} "
       f"{tip[0] + nx*6:.1f},{tip[1] + ny*6:.1f} {tip[0]:.1f},{tip[1]:.1f} "
       f"C{tip[0] - nx*6:.1f},{tip[1] - ny*6:.1f} {tip[0] - nx*16:.1f},{tip[1] - ny*16 + 6:.1f} "
       f"{w0[0] - nx*16:.1f},{w0[1] - ny*16:.1f} "
       f"Q{w0[0] + ux*8:.1f},{w0[1] + uy*8:.1f} {w0[0] + nx*16:.1f},{w0[1] + ny*16:.1f} Z",
       "Tuft tip", fill="#FBF6EC", stroke=NONE, opacity=95)
for k, off in enumerate([-8, 0, 8]):
    a0 = (ex + ux*10 + nx*off, ey + uy*10 + ny*off)
    d.path(f"M{a0[0]:.1f},{a0[1]:.1f} L{a0[0] + ux*30 + nx*off*0.4:.1f},{a0[1] + uy*30 + ny*off*0.4:.1f}",
           f"Tuft hair {k+1}", fill=NONE, stroke="#7A6656", strokeWidth=3, opacity=50, cap="round")

# --- far hind leg + far ear (behind the body) ---------------------------------------
def hind_leg(dx, dy, fill, label):
    def p(x, y): return f"{x+dx},{y+dy}"
    d.path(f"M{p(556,574)} L{p(602,580)} C{p(628,630)} {p(650,690)} {p(656,716)} "
           f"C{p(660,730)} {p(648,738)} {p(628,738)} L{p(470,738)} "
           f"C{p(452,738)} {p(446,728)} {p(456,720)} L{p(614,714)} C{p(598,668)} {p(578,622)} {p(556,574)} Z",
           label, fill=fill, stroke=INK, strokeWidth=5)
    d.path(f"M{p(590,600)} C{p(610,640)} {p(626,680)} {p(636,708)}", f"{label} shin light",
           fill=NONE, stroke="#FFF2D8", strokeWidth=4, opacity=35, cap="round")
    for k in range(3):
        x, y = 452 + dx, 724 + k*5 + dy
        d.path(f"M{x+10},{y} L{x-4},{y+1}", f"{label} toe fur {k+1}", fill=NONE,
               stroke="#B08858", strokeWidth=3, opacity=70, cap="round")

hind_leg(-44, -6, FUR_FAR_GRAD, "Hind leg far")
d.path(H("M454,300 C452,232 492,150 550,126 C578,140 568,222 522,302 Z"),
       "Ear far", fill=EAR_FAR_GRAD, stroke=INK, strokeWidth=5)
d.path(H("M470,290 C474,240 502,180 540,156 C552,176 540,236 512,292 Z"),
       "Inner ear far", fill="#D8A48E", stroke=NONE, opacity=80)

# --- body --------------------------------------------------------------------------
d.path(B("M450,380 C530,372 604,430 612,520 C620,600 580,652 520,656 "
         "C456,660 412,616 408,552 C404,482 410,392 450,380 Z"),
       "Body", fill=FUR_GRAD, stroke=INK, strokeWidth=6)
d.path(B("M424,470 C412,530 420,600 470,640 C440,600 432,540 444,476 Z"),
       "Belly", fill="#FFF8EC", opacity=55, stroke=NONE)
d.path(B("M480,392 C540,392 590,440 600,500"), "Back light", fill=NONE,
       stroke="#FFF2D8", strokeWidth=10, opacity=35, cap="round")

# --- near haunch + hind leg ---------------------------------------------------------
hind_leg(0, 0, LEG_GRAD, "Hind leg near")
d.path(B("M520,540 C560,520 620,540 630,590 C640,640 600,668 560,664 "
         "C520,660 500,620 505,585 C508,565 512,550 520,540 Z"),
       "Haunch", fill=FUR_GRAD, stroke=INK, strokeWidth=5)
d.path(B("M530,560 C560,546 600,556 614,584"), "Haunch light", fill=NONE,
       stroke="#FFF2D8", strokeWidth=7, opacity=40, cap="round")
d.path(B("M520,630 C540,656 580,664 610,652"), "Haunch shade", fill=NONE,
       stroke="#9C7448", strokeWidth=9, opacity=30, cap="round")

# --- tiny forepaws held up at the chest -----------------------------------------------
for i, (a, b, c) in enumerate([((446,436),(428,446),(412,462)), ((458,446),(444,460),(432,474))]):
    dd = f"M{a[0]},{a[1]} Q{b[0]},{b[1]} {c[0]},{c[1]}"
    d.path(dd, f"Forepaw ink {i+1}", fill=NONE, stroke=INK, strokeWidth=13, cap="round")
    d.path(dd, f"Forepaw {i+1}", fill=NONE, stroke="#F4E2C2", strokeWidth=7, cap="round")
    d.shape("ellipse", f"Paw {i+1}", x=c[0]-8, y=c[1]-5, width=14, height=11,
            fill="#F0C8B4", stroke=INK, strokeWidth=3)

# --- near ear --------------------------------------------------------------------------
d.path(H("M408,300 C394,230 406,150 450,116 C486,122 494,210 472,298 Z"),
       "Ear near", fill=EAR_GRAD, stroke=INK, strokeWidth=6)
d.path(H("M422,288 C414,232 424,170 450,140 C468,160 470,226 458,286 Z"),
       "Inner ear near", fill="#E9BCA4", stroke=NONE)
d.path(H("M440,160 C446,200 448,240 446,280"), "Ear vein", fill=NONE,
       stroke="#C98E80", strokeWidth=3, opacity=45, cap="round")
d.path(H("M404,250 C400,200 410,150 444,122"), "Ear rim light", fill=NONE,
       stroke="#FFF6E4", strokeWidth=4, opacity=50, cap="round")

# --- head ------------------------------------------------------------------------------
d.path(H("M350,360 C352,320 380,282 430,276 C482,270 512,310 512,350 "
         "C512,396 480,424 440,428 C400,432 372,414 356,394 C344,382 342,370 350,360 Z"),
       "Head", fill=FUR_GRAD, stroke=INK, strokeWidth=6)
d.shape("ellipse", "Head highlight", **HB(404, 284, 90, 34), fill="#FFFFFF", opacity=18, stroke=NONE)
d.path(H("M360,392 C380,416 420,428 456,420 C430,410 400,402 372,384 Z"),
       "Cheek white", fill="#FFF8EC", opacity=60, stroke=NONE)
d.path(H("M470,412 C490,400 504,380 508,356"), "Head shade", fill=NONE,
       stroke="#9C7448", strokeWidth=8, opacity=28, cap="round")

# --- face: oversized eye -----------------------------------------------------------------
d.shape("ellipse", "Eye ring", **HB(370, 304, 62, 66), fill="#FFF4DE", opacity=45, stroke=NONE)
d.shape("ellipse", "Eye", **HB(378, 312, 46, 50), fill="#241812", stroke=NONE)
d.shape("ellipse", "Eye depth", **HB(386, 336, 30, 20), fill="#5A3A28", opacity=45, stroke=NONE)
d.shape("ellipse", "Glint", **HB(388, 320, 13, 13), fill="#FFFFFF", opacity=92, stroke=NONE)
d.shape("ellipse", "Glint small", **HB(410, 344, 6, 6), fill="#FFFFFF", opacity=70, stroke=NONE)
d.path(H("M346,358 C348,350 358,348 362,356 C362,366 350,370 346,364 Z"),
       "Nose", fill="#C98478", stroke=INK, strokeWidth=2)
d.path(H("M354,380 C360,388 372,390 380,386"), "Mouth", fill=NONE, stroke=INK, strokeWidth=4, cap="round")
for lbl, dd in [("W1", "M364,366 C320,352 280,344 236,346"), ("W2", "M364,372 C316,372 272,380 232,394"),
                ("W3", "M366,378 C330,392 296,410 262,432"), ("W4", "M366,362 C334,340 304,322 276,304")]:
    d.path(H(dd), f"Whisker {lbl}", fill=NONE, stroke=INK, strokeWidth=2.5, opacity=60, cap="round")

# --- name -------------------------------------------------------------------------------
d.text("JERBOA", "Name", x=500, y=962, size=60, font="Virelai Sans",
       color="#EAD9B8", justify="center")

d.finish("jerboa-V1R00")
