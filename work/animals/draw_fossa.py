#!/usr/bin/env python3
"""Fossa — field-guide plate V1R00. Lithe full-body profile facing left, padding
along a dry-forest branch; the absurdly long tail drapes off the branch and
curls round the lower plate as the frame. Russet fur, warm ochre plate. Branch
ends close on the disc's own arc so they never leak past the rim.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Fossa — Field Plate", 1000, 1000)

INK = "#3A2418"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#33261A"}, {"offset": 1, "color": "#120C08"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F3E8CE"}, {"offset": 0.7, "color": "#DCC69E"},
    {"offset": 1, "color": "#A88C60"}]}}
FUR_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#D08850"}, {"offset": 0.7, "color": "#A85C30"},
    {"offset": 1, "color": "#743C1E"}]}}
HEAD_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#D89462"}, {"offset": 0.72, "color": "#B06838"},
    {"offset": 1, "color": "#7A4222"}]}}
TAIL_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#B8693A"}, {"offset": 1, "color": "#7E4222"}]}}
LEG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#A85C30"}, {"offset": 1, "color": "#6A361A"}]}}
FAR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7E4426"}, {"offset": 1, "color": "#55301A"}]}}
BARK_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7A5E42"}, {"offset": 1, "color": "#43301F"}]}}
LEAF_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#8E9A62"}, {"offset": 1, "color": "#56623A"}]}}

CX, CY, R = 500, 460, 420

def rim_x(y):
    dx = math.sqrt(R*R - (y - CY)**2)
    return CX - dx, CX + dx

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#7A6440", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#FBF3E0", strokeWidth=3, opacity=55)
d.shape("ellipse", "Patina 1", x=160, y=200, width=240, height=140, fill="#B9A27A", opacity=22, stroke=NONE)
d.shape("ellipse", "Patina 2", x=420, y=660, width=260, height=120, fill="#B9A27A", opacity=18, stroke=NONE)
for i, (x, y, w) in enumerate([(200,300,8),(170,540,9),(140,420,6),(400,125,7),(600,118,8),
                               (250,740,7),(330,820,6),(860,420,7),(700,800,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w, fill="#8E7650", opacity=40, stroke=NONE)

# --- hanging foliage, upper right (well inside the disc) ------------------------
for i, (x, y, ang, L) in enumerate([(640,110,30,90),(700,140,55,80),(760,190,75,84),
                                    (600,130,10,70),(820,250,95,70),(730,250,60,60)]):
    a = math.radians(ang + 60)
    tx, ty = x + math.cos(a)*L, y + math.sin(a)*L
    nx, ny = -math.sin(a)*L*0.28, math.cos(a)*L*0.28
    mx, my = (x + tx)/2, (y + ty)/2
    d.path(f"M{x:.0f},{y:.0f} Q{mx+nx:.0f},{my+ny:.0f} {tx:.0f},{ty:.0f} "
           f"Q{mx-nx:.0f},{my-ny:.0f} {x:.0f},{y:.0f} Z",
           f"Leaf {i+1}", fill=LEAF_GRAD, stroke=INK, strokeWidth=3, opacity=55)
    d.path(f"M{x:.0f},{y:.0f} L{tx:.0f},{ty:.0f}", f"Leaf {i+1} vein",
           fill=NONE, stroke="#3E4A26", strokeWidth=2, opacity=45, cap="round")
d.path("M600,130 C660,100 740,130 820,250", "Twig", fill=NONE,
       stroke="#5A4430", strokeWidth=6, opacity=60, cap="round")

# --- branch: both ends close on the disc's own arc ------------------------------
Y_L, Y_R, TH = 646, 606, 40
lxa, _ = rim_x(Y_L); lxb, _ = rim_x(Y_L + TH)
_, rxa = rim_x(Y_R); _, rxb = rim_x(Y_R + TH)
def branch_top(x):
    return Y_L + (Y_R - Y_L) * (x - lxa) / (rxa - lxa)
d.path(f"M{lxa:.1f},{Y_L} L{rxa:.1f},{Y_R} A420,420 0 0 1 {rxb:.1f},{Y_R+TH} "
       f"L{lxb:.1f},{Y_L+TH} A420,420 0 0 1 {lxa:.1f},{Y_L} Z",
       "Branch", fill=BARK_GRAD, stroke=NONE)
d.path(f"M{lxa:.1f},{Y_L} L{rxa:.1f},{Y_R}", "Branch top edge", fill=NONE, stroke=INK, strokeWidth=5)
d.path(f"M{lxb:.1f},{Y_L+TH} L{rxb:.1f},{Y_R+TH}", "Branch under edge", fill=NONE, stroke=INK, strokeWidth=5)
d.path(f"M{lxa+20:.1f},{Y_L+8} L{rxa-20:.1f},{Y_R+8}", "Branch light", fill=NONE,
       stroke="#C8AE86", strokeWidth=5, opacity=35, cap="round")
for i, x in enumerate([180, 300, 470, 560, 700, 820]):
    y = branch_top(x)
    d.path(f"M{x},{y+16:.0f} C{x+18},{y+20:.0f} {x+30},{y+24:.0f} {x+46},{y+24:.0f}",
           f"Bark grain {i+1}", fill=NONE, stroke="#2E2014", strokeWidth=3, opacity=45, cap="round")
# a knot and a small side stub
d.shape("ellipse", "Knot", x=500, y=branch_top(520)+12, width=30, height=16, fill="#3A2818", opacity=60, stroke=NONE)

# --- tail: tapered ribbon along a Catmull-Rom spine -----------------------------
def catmull(pts, samples_per=10):
    out = []
    P = [pts[0]] + pts + [pts[-1]]
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i-1], P[i], P[i+1], P[i+2]
        for s in range(samples_per):
            t = s / samples_per
            t2, t3 = t*t, t*t*t
            x = 0.5*((2*p1[0]) + (-p0[0]+p2[0])*t + (2*p0[0]-5*p1[0]+4*p2[0]-p3[0])*t2 + (-p0[0]+3*p1[0]-3*p2[0]+p3[0])*t3)
            y = 0.5*((2*p1[1]) + (-p0[1]+p2[1])*t + (2*p0[1]-5*p1[1]+4*p2[1]-p3[1])*t2 + (-p0[1]+3*p1[1]-3*p2[1]+p3[1])*t3)
            out.append((x, y))
    out.append(pts[-1])
    return out

spine = catmull([(640,500),(712,520),(754,580),(766,668),(730,748),(640,800),
                 (520,814),(420,796),(366,756),(368,718),(406,708)])
N = len(spine)
L, Rr, mid = [], [], []
for i, (x, y) in enumerate(spine):
    a = spine[max(i-1, 0)]; b = spine[min(i+1, N-1)]
    dx, dy = b[0]-a[0], b[1]-a[1]
    ln = math.hypot(dx, dy) or 1
    nx, ny = -dy/ln, dx/ln
    t = i / (N - 1)
    w = (48 - 34*t) / 2 if t < 0.94 else (48 - 34*0.94) / 2 * (1 - (t - 0.94)/0.06*0.7)
    mid.append((x, y, nx, ny, w))
    L.append((x + nx*w, y + ny*w)); Rr.append((x - nx*w, y - ny*w))
td = "M%.1f,%.1f " % L[0] + " ".join("L%.1f,%.1f" % p for p in L[1:])
td += " " + " ".join("L%.1f,%.1f" % p for p in reversed(Rr)) + " Z"
d.path(td, "Tail", fill=TAIL_GRAD, stroke=INK, strokeWidth=6)
def offset_line(frac, i0, i1):
    pts = [(m[0] + m[2]*m[4]*frac, m[1] + m[3]*m[4]*frac) for m in mid[i0:i1]]
    return "M%.1f,%.1f " % pts[0] + " ".join("L%.1f,%.1f" % p for p in pts[1:])
d.path(offset_line(-0.45, 2, N-6), "Tail sheen", fill=NONE, stroke="#F0C496", strokeWidth=6, opacity=32, cap="round")
d.path(offset_line(0.55, 2, N-4), "Tail shade", fill=NONE, stroke="#4A2412", strokeWidth=8, opacity=28, cap="round")
for j in range(9):
    x, y, nx, ny, w = mid[8 + j*10]
    d.path(f"M{x - nx*w*0.6:.1f},{y - ny*w*0.6:.1f} Q{x + nx*w*0.1 + ny*6:.1f},{y + ny*w*0.1 - nx*6:.1f} {x + nx*w*0.5:.1f},{y + ny*w*0.5:.1f}",
           f"Tail fur {j+1}", fill=NONE, stroke="#5E301A", strokeWidth=3, opacity=35, cap="round")

# --- legs: tapered, drawn before the body so their tops tuck under it ------------
def foreleg(label, sx, px, ws, wp, fill, paw_fill):
    sy, py = 500, branch_top(px) - 6
    d.path(f"M{sx-ws/2},{sy} C{sx-ws/2+2},{sy+50} {px-wp/2-6},{py-36:.1f} {px-wp/2},{py-4:.1f} "
           f"Q{px},{py+4:.1f} {px+wp/2},{py-4:.1f} C{px+wp/2+2},{py-30:.1f} {sx+ws/2-2},{sy+40} {sx+ws/2},{sy} Z",
           label, fill=fill, stroke=INK, strokeWidth=5)
    d.shape("ellipse", f"{label} paw", x=px-(wp+18)/2-5, y=py-12, width=wp+18, height=16,
            fill=paw_fill, stroke=INK, strokeWidth=4)
    return px - 5, py

def hindleg(label, hx, px, fill, paw_fill):
    py = branch_top(px) - 6
    d.path(f"M{hx-30},500 L{hx+30},500 C{hx+46},528 {hx+44},556 {hx+32},570 "
           f"C{hx+24},578 {px+14},{py-14:.1f} {px+12},{py-4:.1f} Q{px},{py+4:.1f} {px-12},{py-4:.1f} "
           f"C{px-14},{py-24:.1f} {hx-12},544 {hx-30},500 Z",
           label, fill=fill, stroke=INK, strokeWidth=5)
    d.shape("ellipse", f"{label} paw", x=px-22, y=py-12, width=40, height=16,
            fill=paw_fill, stroke=INK, strokeWidth=4)
    return px - 2, py

foreleg("Far foreleg", 414, 420, 34, 18, FAR_GRAD, "#5A321C")
hindleg("Far hindleg", 656, 660, FAR_GRAD, "#5A321C")
paws = [foreleg("Near foreleg", 384, 368, 46, 22, LEG_GRAD, "#6A3A1E"),
        hindleg("Near hindleg", 628, 614, LEG_GRAD, "#6A3A1E")]

# --- body: long, low, lithe ------------------------------------------------------
d.path("M318,446 C370,424 444,438 520,436 C590,434 646,438 676,470 "
       "C702,500 696,540 664,556 C624,574 540,564 460,560 "
       "C400,558 352,534 332,504 C318,484 310,462 318,446 Z",
       "Body", fill=FUR_GRAD, stroke=INK, strokeWidth=7)
d.path("M360,444 C440,434 560,430 650,452", "Back sheen", fill=NONE,
       stroke="#F2C89C", strokeWidth=12, opacity=26, cap="round")
d.path("M380,536 C460,556 580,560 650,548", "Belly light", fill=NONE,
       stroke="#E8C49A", strokeWidth=14, opacity=26, cap="round")
d.path("M400,520 C480,540 580,544 660,530", "Flank shade", fill=NONE,
       stroke="#5A2E16", strokeWidth=10, opacity=20, cap="round")
for i, dd in enumerate(["M470,460 C490,470 500,484 504,498", "M540,458 C560,468 570,482 574,496",
                        "M430,470 C448,480 456,494 460,508"]):
    d.path(dd, f"Body fur {i+1}", fill=NONE, stroke="#6E3A1C", strokeWidth=4, opacity=38, cap="round")
# haunch + shoulder masses
d.path("M584,486 C612,462 668,466 686,500 C700,528 682,556 652,560 "
       "C622,562 596,540 584,512 Z", "Haunch", fill=FUR_GRAD, stroke=NONE, opacity=85)
d.path("M588,504 C598,478 636,464 670,476", "Haunch line", fill=NONE,
       stroke=INK, strokeWidth=4, opacity=45, cap="round")
d.path("M398,462 C378,480 372,508 380,540", "Shoulder line", fill=NONE,
       stroke=INK, strokeWidth=4, opacity=40, cap="round")
for (px, py) in paws:
    for k in (-8, 0, 8):
        d.path(f"M{px+k:.0f},{py-9:.0f} L{px+k:.0f},{py-3:.0f}", "Toe", fill=NONE,
               stroke=INK, strokeWidth=2, opacity=55, cap="round")

# --- head: small, blunt, puma-like ---------------------------------------------------
d.path("M280,406 C270,382 280,366 298,366 C312,368 316,384 310,402 Z",
       "Far ear", fill=FAR_GRAD, stroke=INK, strokeWidth=4)
d.path("M306,408 C298,380 312,362 334,364 C356,368 362,392 350,414 Z",
       "Ear", fill=HEAD_GRAD, stroke=INK, strokeWidth=5)
d.path("M314,404 C310,384 320,374 334,376 C348,379 350,394 344,408 Z",
       "Inner ear", fill="#4A2614", opacity=55, stroke=NONE)
d.path("M220,446 C228,414 262,396 300,396 C340,396 370,420 372,454 "
       "C374,488 350,512 316,518 C290,522 266,514 250,504 "
       "C232,502 214,496 206,484 C200,472 206,456 220,446 Z",
       "Head", fill=HEAD_GRAD, stroke=INK, strokeWidth=7)
d.shape("ellipse", "Brow light", x=262, y=402, width=84, height=34, fill="#FFFFFF", opacity=13, stroke=NONE)
d.path("M214,488 C240,504 272,512 304,510", "Muzzle light", fill=NONE,
       stroke="#F2D2B0", strokeWidth=14, opacity=30, cap="round")
d.path("M306,506 C334,502 356,484 364,460", "Cheek shade", fill=NONE,
       stroke="#5A2E16", strokeWidth=10, opacity=25, cap="round")
d.shape("ellipse", "Muzzle tip shade", x=200, y=450, width=46, height=40, fill="#5A2E16", opacity=22, stroke=NONE)
# big amber eye, cat-slit pupil
d.shape("ellipse", "Eye ring", x=262, y=428, width=42, height=36, fill="#F0D6B0", opacity=35, stroke=NONE)
d.shape("ellipse", "Iris", x=268, y=432, width=30, height=28, fill="#B07A2A", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Pupil", x=278, y=434, width=10, height=24, fill="#1E120A", stroke=NONE)
d.shape("ellipse", "Glint", x=280, y=437, width=6, height=6, fill="#FFFFFF", opacity=90, stroke=NONE)
d.path("M264,432 C274,422 294,422 302,432", "Upper lid", fill=NONE, stroke=INK, strokeWidth=4, cap="round")
d.path("M270,460 C262,470 252,476 240,480", "Tear line", fill=NONE, stroke="#4A2412", strokeWidth=4, opacity=45, cap="round")
# nose, mouth, whiskers
d.path("M200,462 C206,454 220,454 224,462 C224,472 212,478 204,474 C198,470 198,466 200,462 Z",
       "Nose", fill="#241410", stroke=NONE)
d.path("M210,486 C222,496 238,500 254,496", "Mouth", fill=NONE, stroke=INK, strokeWidth=4, cap="round")
for i, dd in enumerate(["M232,478 C212,472 192,472 174,476", "M234,484 C214,486 196,492 180,502"]):
    d.path(dd, f"Whisker {i+1}", fill=NONE, stroke="#FBF0DC", strokeWidth=2, opacity=60, cap="round")
# --- name ----------------------------------------------------------------------
d.text("FOSSA", "Name", x=500, y=962, size=60, font="Virelai Sans",
       color="#EADCC0", justify="center")

d.finish("fossa-V1R00")
