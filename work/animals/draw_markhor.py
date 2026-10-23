#!/usr/bin/env python3
"""Markhor — field-guide plate V1R00. Head/bust portrait, profile facing left:
tall corkscrew horns (tapered ribbon paths + spiral ridge strokes), long chin
beard, shaggy neck ruff. Slate-grey/tan palette, mountain mood.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Markhor — Field Plate", 1000, 1000)

INK = "#423B33"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2C3944"}, {"offset": 1, "color": "#0F161D"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#EEE9DA"}, {"offset": 0.7, "color": "#CDC7B2"},
    {"offset": 1, "color": "#948E76"}]}}
FUR_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#C2B7A0"}, {"offset": 0.72, "color": "#9A8D74"},
    {"offset": 1, "color": "#6E6350"}]}}
RUFF_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#8F8468"}, {"offset": 1, "color": "#655A45"}]}}
BEARD_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6E6250"}, {"offset": 1, "color": "#4E4436"}]}}
EAR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#8F8468"}, {"offset": 1, "color": "#6E6250"}]}}
HORN_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#DCCFAC"}, {"offset": 1, "color": "#9C8F6E"}]}}
HORN_FAR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#9A8E72"}, {"offset": 1, "color": "#6E6450"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#6E6852", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F4F0E2", strokeWidth=3, opacity=55)
# plate patina
d.shape("ellipse", "Patina 1", x=160, y=190, width=250, height=150, fill="#A39C86", opacity=22, stroke=NONE)
d.shape("ellipse", "Patina 2", x=600, y=640, width=260, height=150, fill="#A39C86", opacity=20, stroke=NONE)
# faint mountain silhouettes low inside the plate (all vertices inside the disc)
d.path("M300,790 L380,700 L440,750 L520,660 L600,745 L660,705 L700,790 Z",
       "Mountains", fill="#8E8878", opacity=18, stroke=NONE)
for i, (x, y, w) in enumerate([(200,300,8),(770,250,7),(170,560,9),(820,560,8),(250,760,7),(740,750,9),
                               (140,420,6),(860,400,7),(400,125,7),(600,120,8),(330,820,6),(670,820,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w, fill="#7F7A66", opacity=40, stroke=NONE)

# --- corkscrew horns ----------------------------------------------------------
def cubic(p0, p1, p2, p3, t):
    u = 1 - t
    x = u**3*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t**3*p3[0]
    y = u**3*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t**3*p3[1]
    dx = 3*u*u*(p1[0]-p0[0]) + 6*u*t*(p2[0]-p1[0]) + 3*t*t*(p3[0]-p2[0])
    dy = 3*u*u*(p1[1]-p0[1]) + 6*u*t*(p2[1]-p1[1]) + 3*t*t*(p3[1]-p2[1])
    return (x, y), (dx, dy)

def horn(spine, w0, w1, label, fill, twists=2.5, amp=0.30, n_ridges=6, samples=28):
    """Tapered ribbon along a cubic spine; edges bulge alternately (corkscrew
    silhouette), then rotated chord strokes add the spiral ridges."""
    left, right, mid = [], [], []
    for i in range(samples + 1):
        t = i / samples
        (x, y), (dx, dy) = cubic(*spine, t)
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy/ln, dx/ln
        w = (w0 + (w1 - w0)*t) / 2
        ph = math.sin(t*math.pi*2*twists)
        mid.append((x, y, nx, ny, w))
        left.append((x + nx*w*(1 + amp*ph), y + ny*w*(1 + amp*ph)))
        right.append((x - nx*w*(1 - amp*ph), y - ny*w*(1 - amp*ph)))
    dd = "M%.1f,%.1f " % left[0] + " ".join("L%.1f,%.1f" % p for p in left[1:])
    dd += " " + " ".join("L%.1f,%.1f" % p for p in reversed(right)) + " Z"
    d.path(dd, label, fill=fill, stroke=INK, strokeWidth=5)
    # spiral ridges: chords rotated alternately across the horn
    for j in range(n_ridges):
        t = 0.10 + 0.80*j/(n_ridges - 1)
        x, y, nx, ny, w = mid[round(t*samples)]
        ang = math.radians(26 if j % 2 == 0 else -26)
        rx, ry = nx*math.cos(ang) - ny*math.sin(ang), nx*math.sin(ang) + ny*math.cos(ang)
        e = w * 1.12
        d.path("M%.1f,%.1f L%.1f,%.1f" % (x - rx*e, y - ry*e, x + rx*e, y + ry*e),
               f"{label} ridge {j+1}", fill=NONE, stroke="#5A4E3C",
               strokeWidth=5, cap="round")
    # soft sheen along the lit edge
    e0, e1, e2 = mid[2], mid[samples//2], mid[samples - 3]
    d.path("M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" % (
        e0[0] + e0[2]*e0[4]*0.8, e0[1] + e0[3]*e0[4]*0.8,
        e1[0] + e1[2]*e1[4]*0.8, e1[1] + e1[3]*e1[4]*0.8,
        e2[0] + e2[2]*e2[4]*0.8, e2[1] + e2[3]*e2[4]*0.8),
        f"{label} sheen", fill=NONE, stroke="#F2EAD2", strokeWidth=7,
        opacity=30, cap="round")

# far horn (behind, darker, slightly right)
horn([(505, 420), (548, 352), (566, 282), (584, 172)], 34, 7,
     "Horn far", HORN_FAR_GRAD, n_ridges=6)
# near horn — tall corkscrew
horn([(458, 425), (492, 340), (486, 262), (524, 158)], 44, 8,
     "Horn near", HORN_GRAD, n_ridges=7)

# --- ear (behind head) --------------------------------------------------------
d.path("M552,432 C590,410 628,420 636,452 C618,478 578,482 552,462 Z",
       "Ear", fill=EAR_GRAD, stroke=INK, strokeWidth=5)
d.path("M568,442 C590,432 610,438 614,455 C600,468 580,468 568,458 Z",
       "Inner ear", fill="#5C5142", stroke=NONE)

# --- shaggy neck ruff (behind head) --------------------------------------------
d.path("M505,610 C575,625 655,690 688,782 L668,772 L680,822 L648,800 "
       "L652,842 L618,815 L612,852 L570,820 L556,858 L520,828 "
       "C478,848 436,838 428,792 C420,738 445,645 505,610 Z",
       "Neck ruff", fill=RUFF_GRAD, stroke=INK, strokeWidth=6)
for lbl, dd in [("Ruff fur 1", "M560,680 C600,700 630,730 648,770"),
                ("Ruff fur 2", "M540,740 C570,760 592,785 604,815"),
                ("Ruff fur 3", "M500,780 C520,800 532,820 538,842"),
                ("Ruff fur 4", "M620,700 C645,720 662,745 672,772")]:
    d.path(dd, lbl, fill=NONE, stroke="#4E4436", strokeWidth=6, opacity=40, cap="round")

# --- head (profile facing left) --------------------------------------------------
d.path("M305,562 C296,545 306,512 330,478 C358,440 405,405 468,388 "
       "C512,377 552,398 570,442 C600,510 608,588 612,652 "
       "C616,706 592,740 550,738 C498,736 436,714 390,672 "
       "C364,649 344,624 330,600 C314,590 302,578 305,562 Z",
       "Head", fill=FUR_GRAD, stroke=INK, strokeWidth=8)
# forehead tuft between the horn bases
d.path("M452,396 L444,374 L460,390 L458,366 L474,386 L480,368", "Forehead tuft",
       fill=NONE, stroke=INK, strokeWidth=5, cap="round")
# pale blaze along the face bridge + forehead highlight
d.path("M462,400 C418,442 362,494 330,548", "Face blaze", fill=NONE,
       stroke="#DCD4C0", strokeWidth=24, opacity=22, cap="round")
d.shape("ellipse", "Forehead light", x=430, y=390, width=120, height=60,
        fill="#FFFFFF", opacity=12, stroke=NONE)
# jaw / throat shadow where head meets the ruff
d.path("M392,672 C442,714 512,732 556,730", "Jaw shadow", fill=NONE,
       stroke="#5C5142", strokeWidth=12, opacity=35, cap="round")
# lighter muzzle + dark nose tip
d.shape("ellipse", "Muzzle light", x=300, y=555, width=110, height=85,
        fill="#DDD5C2", opacity=40, stroke=NONE)
d.shape("ellipse", "Nose tip shade", x=298, y=545, width=42, height=45,
        fill="#5C5142", opacity=35, stroke=NONE)
# eye: amber iris, dark pupil, lid line, pale eye-ring
d.shape("ellipse", "Eye ring", x=415, y=498, width=56, height=58,
        fill="#DCD4C0", opacity=30, stroke=NONE)
d.shape("ellipse", "Iris", x=424, y=508, width=32, height=38, fill="#7A5A34", stroke=NONE)
d.shape("ellipse", "Pupil", x=431, y=514, width=18, height=26, fill="#221B14", stroke=NONE)
d.shape("ellipse", "Glint", x=435, y=518, width=6, height=6, fill="#FFFFFF", opacity=85, stroke=NONE)
d.path("M422,502 C436,492 458,492 472,502", "Upper lid", fill=NONE,
       stroke=INK, strokeWidth=6, cap="round")
# nostril + mouth
d.shape("ellipse", "Nostril", x=312, y=558, width=20, height=13, fill="#2E2620", stroke=NONE)
d.path("M320,596 C334,606 352,611 368,608", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=6, cap="round")
# short fur texture strokes on the cheek
for lbl, dd in [("Cheek fur 1", "M470,560 C500,575 525,590 545,610"),
                ("Cheek fur 2", "M460,600 C490,612 515,628 532,648"),
                ("Cheek fur 3", "M480,540 C505,552 528,568 545,585")]:
    d.path(dd, lbl, fill=NONE, stroke="#6E6350", strokeWidth=5, opacity=45, cap="round")

# --- long chin beard --------------------------------------------------------------
d.path("M388,668 C352,700 346,762 334,822 C366,848 416,834 432,786 "
       "C444,744 432,694 412,672 Z",
       "Beard", fill=BEARD_GRAD, stroke=INK, strokeWidth=6)
for lbl, dd, col, w in [
        ("Beard strand 1", "M386,676 C362,715 355,775 342,818", "#4E4436", 8),
        ("Beard strand 2", "M396,680 C380,732 380,795 366,842", "#5C5142", 9),
        ("Beard strand 3", "M406,682 C396,742 398,800 388,846", "#4E4436", 8),
        ("Beard strand 4", "M416,680 C414,740 420,795 412,838", "#7E7259", 7),
        ("Beard strand 5", "M424,678 C430,735 432,790 428,830", "#4E4436", 7),
        ("Beard light", "M400,686 C390,740 392,795 382,834", "#9A8D74", 4)]:
    d.path(dd, lbl, fill=NONE, stroke=col, strokeWidth=w, cap="round")

# --- name ----------------------------------------------------------------------
d.text("MARKHOR", "Name", x=500, y=962, size=60, font="Virelai Sans",
       color="#E0DACA", justify="center")

d.finish("markhor-V1R00")
