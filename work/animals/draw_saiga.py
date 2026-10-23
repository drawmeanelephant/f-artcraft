#!/usr/bin/env python3
"""Saiga — field-guide plate V1R00. Front head portrait: the swollen, drooping
trunk-nose does the comedy, flanked by wide-set worried eyes, outward ears and
waxy translucent lyre horns. Tan/cream steppe palette; the steppe band and the
bust both close on the disc's own arc so nothing leaks past the rim.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Saiga — Field Plate", 1000, 1000)

INK = "#3E3022"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2A3240"}, {"offset": 1, "color": "#0F131A"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F6EEDA"}, {"offset": 0.7, "color": "#E2D0AA"},
    {"offset": 1, "color": "#B0976A"}]}}
FUR_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#DDBC8A"}, {"offset": 0.7, "color": "#BE9663"},
    {"offset": 1, "color": "#8A673F"}]}}
NOSE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#EED3A8"}, {"offset": 0.65, "color": "#CDA672"},
    {"offset": 1, "color": "#97724A"}]}}
NECK_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#C49C68"}, {"offset": 1, "color": "#8E6B44"}]}}
EAR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#C8A06A"}, {"offset": 1, "color": "#94704A"}]}}
HORN_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F6E6B4"}, {"offset": 1, "color": "#C49C58"}]}}
STEPPE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#CDB98C"}, {"offset": 1, "color": "#9C875C"}]}}
SUN_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#FFF4D8"}, {"offset": 1, "color": "#F2D9A0"}]}}

CX, CY, R = 500, 460, 420

def rim_x(y):
    dx = math.sqrt(R*R - (y - CY)**2)
    return CX - dx, CX + dx

def mirror(pts):
    return [(1000 - x, y) for x, y in pts]

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#7E6A48", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#FFF8E8", strokeWidth=3, opacity=55)
d.shape("ellipse", "Low sun", x=640, y=150, width=150, height=150, fill=SUN_GRAD, opacity=55, stroke=NONE)
d.shape("ellipse", "Patina 1", x=160, y=200, width=230, height=130, fill="#C2AC80", opacity=22, stroke=NONE)
for i, (x, y, w) in enumerate([(200,300,8),(170,540,9),(140,420,6),(400,125,7),(600,118,8),
                               (860,420,7),(820,560,8),(780,250,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w, fill="#9A8460", opacity=40, stroke=NONE)

# --- steppe band: wavy horizon closed on the disc's own arc -----------------------
HZ = 712
lx, rx = rim_x(HZ)
n = 10
hz_d = f"M{lx:.1f},{HZ} " + " ".join(
    f"Q{(lx + (rx-lx)*(k-0.5)/n):.1f},{HZ + (-7 if k % 2 else 5)} {(lx + (rx-lx)*k/n):.1f},{HZ}"
    for k in range(1, n + 1))
d.path(hz_d + f" A420,420 0 0 1 {lx:.1f},{HZ} Z", "Steppe", fill=STEPPE_GRAD, stroke=NONE, opacity=80)
d.path(hz_d, "Horizon line", fill=NONE, stroke="#8A7650", strokeWidth=3, opacity=50)
for side in (0, 1):
    for i, (x, h, lean) in enumerate([(190,34,-6),(206,46,4),(222,30,10),(250,40,-4),(272,28,6)]):
        bx = x if side == 0 else 1000 - x
        lean = lean if side == 0 else -lean
        d.path(f"M{bx},{HZ+14} Q{bx+lean/2},{HZ+14-h/2} {bx+lean},{HZ+14-h}",
               f"Grass {side}-{i+1}", fill=NONE, stroke="#7E6C46", strokeWidth=4, opacity=60, cap="round")
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840, fill=NONE, stroke="#7E6A48", strokeWidth=6)

# --- bust: closes on the disc's own arc ----------------------------------------------
BY = 830
blx, brx = rim_x(BY)
d.path(f"M{blx:.1f},{BY} C330,760 378,700 404,590 L596,590 C622,700 670,760 {brx:.1f},{BY} "
       f"A420,420 0 0 1 {blx:.1f},{BY} Z", "Neck", fill=NECK_GRAD, stroke=INK, strokeWidth=7)
# throat fringe: a closed patch whose bottom runs along the disc's own arc
fy = 872
flx, frx = 500 - math.sqrt(R*R - (fy - CY)**2), 500 + math.sqrt(R*R - (fy - CY)**2)
d.path(f"M536,692 C548,730 556,770 566,800 L556,812 C562,836 {frx-4:.1f},{fy-14} {frx:.1f},{fy} "
       f"A420,420 0 0 1 {flx:.1f},{fy} C{flx+4:.1f},{fy-14} 438,836 444,812 L434,800 "
       f"C444,770 452,730 464,692 Z", "Throat fringe", fill="#F3E6CC", opacity=38, stroke=NONE)
d.path("M484,704 C480,760 478,800 482,850", "Throat fringe light", fill=NONE,
       stroke="#FBF2DE", strokeWidth=22, opacity=28, cap="round")
for i, (x0, x1) in enumerate([(440,430),(470,466),(530,534),(560,570),(410,396),(590,604)]):
    d.path(f"M{x0},716 Q{(x0+x1)/2 + (x0-500)*0.05:.0f},770 {x1},826", f"Fringe strand {i+1}",
           fill=NONE, stroke="#8A6A44", strokeWidth=4, opacity=35, cap="round")
d.path("M404,600 C394,680 360,750 320,808", "Neck shade L", fill=NONE,
       stroke="#5E4428", strokeWidth=14, opacity=22, cap="round")
d.path("M596,600 C606,680 640,750 680,808", "Neck shade R", fill=NONE,
       stroke="#5E4428", strokeWidth=14, opacity=22, cap="round")

# --- waxy lyre horns (behind head) ---------------------------------------------------
def cubic(p0, p1, p2, p3, t):
    u = 1 - t
    x = u**3*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t**3*p3[0]
    y = u**3*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t**3*p3[1]
    dx = 3*u*u*(p1[0]-p0[0]) + 6*u*t*(p2[0]-p1[0]) + 3*t*t*(p3[0]-p2[0])
    dy = 3*u*u*(p1[1]-p0[1]) + 6*u*t*(p2[1]-p1[1]) + 3*t*t*(p3[1]-p2[1])
    return (x, y), (dx, dy)

def horn(spine, label, w0=34, w1=8, samples=26, rings=9):
    left, right, mid = [], [], []
    for i in range(samples + 1):
        t = i / samples
        (x, y), (dx, dy) = cubic(*spine, t)
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy/ln, dx/ln
        w = (w0 + (w1 - w0)*t**0.9) / 2
        mid.append((x, y, nx, ny, w))
        left.append((x + nx*w, y + ny*w)); right.append((x - nx*w, y - ny*w))
    dd = "M%.1f,%.1f " % left[0] + " ".join("L%.1f,%.1f" % p for p in left[1:])
    dd += " " + " ".join("L%.1f,%.1f" % p for p in reversed(right)) + " Z"
    d.path(dd, label, fill=HORN_GRAD, stroke=INK, strokeWidth=5, opacity=90)
    for j in range(rings):
        x, y, nx, ny, w = mid[round((0.06 + 0.62*j/(rings - 1))*samples)]
        d.path("M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" % (x - nx*w*0.95, y - ny*w*0.95, x + 0, y + 5,
                                                   x + nx*w*0.95, y + ny*w*0.95),
               f"{label} ring {j+1}", fill=NONE, stroke="#8E6C38", strokeWidth=4, opacity=60, cap="round")
    pts = [(m[0] + m[2]*m[4]*0.45, m[1] + m[3]*m[4]*0.45) for m in mid[1:samples-2]]
    d.path("M%.1f,%.1f " % pts[0] + " ".join("L%.1f,%.1f" % p for p in pts[1:]),
           f"{label} wax sheen", fill=NONE, stroke="#FFFBEA", strokeWidth=5, opacity=45, cap="round")

L_SPINE = [(470, 326), (436, 252), (428, 184), (456, 122)]
horn(L_SPINE, "Horn L")
horn(mirror(L_SPINE), "Horn R")

# --- ears, pointing outward -------------------------------------------------------
for side, sx in (("L", 1), ("R", -1)):
    def X(x): return x if sx == 1 else 1000 - x
    d.path(f"M{X(382)},{338} C{X(340)},{312} {X(300)},{306} {X(282)},{322} "
           f"C{X(292)},{352} {X(336)},{372} {X(386)},{372} Z",
           f"Ear {side}", fill=EAR_GRAD, stroke=INK, strokeWidth=5)
    d.path(f"M{X(370)},{344} C{X(340)},{328} {X(312)},{324} {X(298)},{330} "
           f"C{X(310)},{350} {X(338)},{360} {X(372)},{362} Z",
           f"Inner ear {side}", fill="#E8C8A4", opacity=55, stroke=NONE)

# --- head -------------------------------------------------------------------------
d.path("M500,288 C560,288 612,312 632,352 C652,394 642,444 620,474 "
       "C600,502 590,540 588,584 C584,644 556,700 500,702 "
       "C444,700 416,644 412,584 C410,540 400,502 380,474 "
       "C358,444 348,394 368,352 C388,312 440,288 500,288 Z",
       "Head", fill=FUR_GRAD, stroke=INK, strokeWidth=8)
d.shape("ellipse", "Forehead light", x=440, y=300, width=120, height=70, fill="#FFFFFF", opacity=14, stroke=NONE)
d.path("M396,476 C412,504 422,540 426,588", "Cheek shade L", fill=NONE, stroke="#6E5032", strokeWidth=14, opacity=24, cap="round")
d.path("M604,476 C588,504 578,540 574,588", "Cheek shade R", fill=NONE, stroke="#6E5032", strokeWidth=14, opacity=24, cap="round")
# forelock tuft between the horn bases
d.path("M470,300 L480,276 L488,298 L500,270 L512,298 L520,276 L530,300", "Forelock",
       fill=NONE, stroke=INK, strokeWidth=5, cap="round")
# chin + mouth peeking under the nose
d.shape("ellipse", "Chin light", x=460, y=664, width=80, height=32, fill="#F6E8CC", opacity=40, stroke=NONE)
d.path("M472,676 Q500,688 528,676", "Mouth", fill=NONE, stroke=INK, strokeWidth=5, cap="round")

# --- eyes: wide-set, a little worried ------------------------------------------------
for side, cx in (("L", 418), ("R", 582)):
    sgn = -1 if side == "L" else 1
    d.shape("ellipse", f"Eye ring {side}", x=cx-30, y=386, width=60, height=52, fill="#F6E8CC", opacity=45, stroke=NONE)
    d.shape("ellipse", f"Eye {side}", x=cx-19, y=394, width=38, height=36, fill="#3A2614", stroke=INK, strokeWidth=3)
    d.shape("ellipse", f"Iris glow {side}", x=cx-12, y=406, width=24, height=20, fill="#7A5228", opacity=55, stroke=NONE)
    d.shape("ellipse", f"Glint {side}", x=cx-9 + sgn*2, y=400, width=8, height=8, fill="#FFFFFF", opacity=90, stroke=NONE)
    # brow tilted up toward the middle = worried
    d.path(f"M{cx + sgn*26},{388} C{cx + sgn*10},{376} {cx - sgn*10},{372} {cx - sgn*24},{378}",
           f"Brow {side}", fill=NONE, stroke=INK, strokeWidth=5, cap="round")
    d.path(f"M{cx - sgn*18},{436} C{cx - sgn*26},{452} {cx - sgn*30},{468} {cx - sgn*30},{486}",
           f"Tear streak {side}", fill=NONE, stroke="#6E5032", strokeWidth=5, opacity=30, cap="round")

# --- THE NOSE -------------------------------------------------------------------------
d.path("M500,436 C540,436 562,466 572,506 C592,536 612,578 606,618 "
       "C600,654 560,672 500,672 C440,672 400,654 394,618 "
       "C388,578 408,536 428,506 C438,466 460,436 500,436 Z",
       "Nose", fill=NOSE_GRAD, stroke=INK, strokeWidth=7)
d.path("M412,612 C430,650 470,664 500,664 C530,664 570,650 588,612 "
       "C570,640 530,652 500,652 C470,652 430,640 412,612 Z",
       "Nose underside shade", fill="#7A5634", opacity=30, stroke=NONE)
d.shape("ellipse", "Nose bulb shine", x=456, y=520, width=88, height=48, fill="#FFFFFF", opacity=22, stroke=NONE)
d.shape("ellipse", "Nose bulb shine core", x=476, y=530, width=34, height=16, fill="#FFFFFF", opacity=35, stroke=NONE)
for i, (y, hw) in enumerate([(468, 30), (486, 38), (504, 48)]):
    d.path(f"M{500-hw},{y+4} Q500,{y-8} {500+hw},{y+4}", f"Nose wrinkle {i+1}",
           fill=NONE, stroke="#7A5634", strokeWidth=4, opacity=55, cap="round")
# big round nostrils, flared down and out
d.path("M440,606 C446,590 474,588 484,604 C490,618 474,630 456,628 C442,626 436,616 440,606 Z",
       "Nostril L", fill="#2A1C12", stroke=NONE)
d.path("M560,606 C554,590 526,588 516,604 C510,618 526,630 544,628 C558,626 564,616 560,606 Z",
       "Nostril R", fill="#2A1C12", stroke=NONE)
d.path("M444,600 C452,592 468,592 476,598", "Nostril rim L", fill=NONE, stroke="#F2DCB6", strokeWidth=3, opacity=50, cap="round")
d.path("M556,600 C548,592 532,592 524,598", "Nostril rim R", fill=NONE, stroke="#F2DCB6", strokeWidth=3, opacity=50, cap="round")
d.path("M500,598 L500,630", "Septum", fill=NONE, stroke="#7A5634", strokeWidth=4, opacity=50, cap="round")

# --- name ----------------------------------------------------------------------
d.text("SAIGA", "Name", x=500, y=962, size=60, font="Virelai Sans",
       color="#EFE4CC", justify="center")

d.finish("saiga-V1R00")
