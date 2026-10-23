#!/usr/bin/env python3
"""Babirusa — field-guide plate V1R00. Head in three-quarter facing left:
four tusks — the upper canines erupt through the top of the snout and curl
back toward the forehead, the lower pair rise from the jaw — wrinkly grey
hide, a long digging snout ending in a disc. Dark ochre plate, a mud band
that closes on the disc's own arc. 1000x1000. House style: gradients +
translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Babirusa — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420


def disc_x(y, side):
    return CX + side * math.sqrt(R * R - (y - CY) ** 2)


def rim_y(x):
    return CY + math.sqrt(R * R - (x - CX) ** 2)


INK = "#2A2220"
BG_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#261A0E"}, {"offset": 1, "color": "#0B0704"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#D4A452"}, {"offset": 0.6, "color": "#A87430"},
    {"offset": 1, "color": "#64421A"}]}}
MUD_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#86602E"}, {"offset": 1, "color": "#5A3E1C"}]}}
HIDE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#B2A8A0"}, {"offset": 0.65, "color": "#8A807A"},
    {"offset": 1, "color": "#5C5450"}]}}
SNOUT_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#A0948C"}, {"offset": 1, "color": "#6E6460"}]}}
DISC_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#C8A8A0"}, {"offset": 0.7, "color": "#9A7E78"},
    {"offset": 1, "color": "#6A5450"}]}}
EAR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#9A908A"}, {"offset": 1, "color": "#5E5652"}]}}
TUSK_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#FFF8E6"}, {"offset": 0.6, "color": "#EADCB8"},
    {"offset": 1, "color": "#C2AE84"}]}}
TUSK_FAR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#D8CCAE"}, {"offset": 1, "color": "#A08E6A"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#4E3412", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F4DCA8", strokeWidth=3, opacity=45)
d.shape("ellipse", "Patina 1", x=170, y=180, width=240, height=140, fill="#E8C47E", opacity=11, stroke=NONE)
d.shape("ellipse", "Patina 2", x=640, y=200, width=200, height=120, fill="#8A5E24", opacity=20, stroke=NONE)
for i, (x, y, w) in enumerate([(200, 300, 8), (770, 250, 7), (160, 520, 9), (840, 480, 8), (400, 120, 7),
                               (600, 112, 8), (140, 420, 6), (860, 380, 7), (300, 170, 6), (700, 150, 6)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w, fill="#5E3E16", opacity=40, stroke=NONE)
# Sulawesi forest: faint fronds at the plate's sides (all inside the disc)
for i, (bx, by, tx, ty, side) in enumerate([(150, 600, 230, 380, 1), (180, 660, 300, 500, 1),
                                            (850, 590, 770, 380, -1), (820, 660, 720, 520, -1)]):
    d.path(f"M{bx},{by} Q{(bx + tx) / 2 + 30 * side},{(by + ty) / 2} {tx},{ty}",
           f"Frond {i+1} rib", fill=NONE, stroke="#6E4C1E", strokeWidth=4, opacity=35, cap="round")
    for j in range(7):
        t = 0.15 + 0.12 * j
        u = 1 - t
        mx, my = (bx + tx) / 2 + 30 * side, (by + ty) / 2
        x = u * u * bx + 2 * u * t * mx + t * t * tx
        y = u * u * by + 2 * u * t * my + t * t * ty
        L = 46 - j * 4
        for s in (1, -1):
            d.path(f"M{x:.1f},{y:.1f} Q{x + s * L * 0.6:.1f},{y - L * 0.1:.1f} {x + s * L:.1f},{y - L * 0.45:.1f}",
                   f"Frond {i+1} leaf {j+1}{'ab'[s < 0]}", fill=NONE, stroke="#6E4C1E", strokeWidth=5,
                   opacity=24, cap="round")
# mud wallow: wavy top, bottom closes on the disc arc
MY = 748
ml, mr = disc_x(MY, -1), disc_x(MY, 1)
d.path(f"M{ml:.1f},{MY} C300,730 400,760 500,744 C600,728 700,756 {mr:.1f},{MY} "
       f"A420,420 0 0 1 {ml:.1f},{MY} Z", "Mud", fill=MUD_GRAD, opacity=92, stroke=NONE)
d.path(f"M{ml + 20:.1f},{MY + 2} C300,734 400,764 500,748 C600,732 700,760 {mr - 20:.1f},{MY + 2}",
       "Mud sheen", fill=NONE, stroke="#E8C47E", strokeWidth=3, opacity=30, cap="round")
for i, (x, y, w, h) in enumerate([(250, 770, 56, 10), (300, 800, 44, 9), (690, 790, 60, 10)]):
    d.shape("ellipse", f"Puddle glint {i+1}", x=x, y=y, width=w, height=h, fill="#F4DCA8", opacity=18, stroke=NONE)

# --- far ear --------------------------------------------------------------------
d.path("M598,330 C596,290 606,258 626,236 C642,264 644,302 634,336 Z",
       "Ear far", fill=EAR_GRAD, stroke=INK, strokeWidth=4)


def cubic(p0, p1, p2, p3, t):
    u = 1 - t
    x = u**3*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t**3*p3[0]
    y = u**3*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t**3*p3[1]
    dx = 3*u*u*(p1[0]-p0[0]) + 6*u*t*(p2[0]-p1[0]) + 3*t*t*(p3[0]-p2[0])
    dy = 3*u*u*(p1[1]-p0[1]) + 6*u*t*(p2[1]-p1[1]) + 3*t*t*(p3[1]-p2[1])
    return (x, y), (dx, dy)


def tusk(spine, w0, w1, label, fill, n=36):
    left, right, mid = [], [], []
    for i in range(n + 1):
        t = i / n
        (x, y), (dx, dy) = cubic(*spine, t)
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy/ln, dx/ln
        w = (w0 + (w1 - w0) * t ** 0.8) / 2
        mid.append((x, y, nx, ny, w))
        left.append((x + nx*w, y + ny*w))
        right.append((x - nx*w, y - ny*w))
    tx, ty, nx, ny, _ = mid[-1]
    (_, _), (dx, dy) = cubic(*spine, 1)
    ln = math.hypot(dx, dy) or 1
    dd = "M%.1f,%.1f " % left[0] + " ".join("L%.1f,%.1f" % p for p in left[1:])
    dd += " Q%.1f,%.1f %.1f,%.1f" % (tx + dx/ln*5, ty + dy/ln*5, right[-1][0], right[-1][1])
    dd += " " + " ".join("L%.1f,%.1f" % p for p in reversed(right[:-1])) + " Z"
    d.path(dd, label, fill=fill, stroke=INK, strokeWidth=4)
    # growth lines near the root + a lit edge
    for j, t in enumerate([0.06, 0.12, 0.18]):
        x, y, nx, ny, w = mid[round(t * n)]
        d.path("M%.1f,%.1f L%.1f,%.1f" % (x - nx*w*0.8, y - ny*w*0.8, x + nx*w*0.8, y + ny*w*0.8),
               f"{label} growth {j+1}", fill=NONE, stroke="#9C8A64", strokeWidth=3, opacity=55, cap="round")
    a, b, c = mid[4], mid[n // 2], mid[n - 5]
    k = 0.45
    d.path("M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" % (
        a[0] + a[2]*a[4]*k, a[1] + a[3]*a[4]*k, b[0] + b[2]*b[4]*k, b[1] + b[3]*b[4]*k,
        c[0] + c[2]*c[4]*k, c[1] + c[3]*c[4]*k),
        f"{label} sheen", fill=NONE, stroke="#FFFFFF", strokeWidth=3, opacity=50, cap="round")


# far lower tusk: rises from the far jaw and shows only above the snout ridge
tusk([(334, 590), (312, 500), (318, 440), (356, 414)], 20, 6, "Tusk lower far", TUSK_FAR_GRAD)

# --- head, snout and neck in one silhouette, closing on the disc arc -------------------
NRX = 836
NRY = rim_y(NRX)
NLX = 330
NLY = rim_y(NLX)
HEAD = (f"M300,534 C344,500 404,450 444,416 C470,392 500,356 548,330 "
        f"C600,304 680,312 724,352 C774,400 812,520 {NRX},{NRY:.1f} "
        f"A420,420 0 0 1 {NLX},{NLY:.1f} "
        "C360,780 420,734 480,706 C440,700 400,690 370,684 "
        "C340,678 316,664 306,646 C294,610 292,566 300,534 Z")
d.path(HEAD, "Head", fill=HIDE_GRAD, stroke=INK, strokeWidth=7)
# shading: nape shadow, cheek light, throat shade, snout ridge light, jaw shade
d.path("M736,380 C776,450 804,560 822,680", "Nape shade", fill=NONE,
       stroke="#3E3634", strokeWidth=28, opacity=22, cap="round")
d.shape("ellipse", "Cheek light", x=500, y=480, width=120, height=80, fill="#E2DAD2", opacity=9, stroke=NONE)
d.path("M490,716 C560,704 640,716 700,750", "Throat shade", fill=NONE,
       stroke="#3E3634", strokeWidth=22, opacity=24, cap="round")
d.path("M316,530 C370,494 420,452 452,418", "Snout ridge light", fill=NONE,
       stroke="#E8E0D8", strokeWidth=9, opacity=22, cap="round")
d.path("M330,672 C380,690 440,700 480,700", "Jaw shade", fill=NONE,
       stroke="#3E3634", strokeWidth=14, opacity=28, cap="round")
d.shape("ellipse", "Brow light", x=560, y=330, width=120, height=44, fill="#FFFFFF", opacity=12, stroke=NONE)


def wrinkle(a, b, label, w=4):
    d.path(a, label + " shadow", fill=NONE, stroke="#3A3230", strokeWidth=w, opacity=42, cap="round")
    d.path(b, label + " light", fill=NONE, stroke="#E8E0D8", strokeWidth=3, opacity=28, cap="round")


# neck folds: heavy creases
for i, (a, b) in enumerate([("M520,730 C580,712 660,726 720,770", "M522,722 C582,704 662,718 722,762"),
                            ("M480,786 C550,764 650,776 740,826", "M482,778 C552,756 652,768 742,818"),
                            ("M600,650 C650,642 700,654 744,684", "M602,642 C652,634 702,646 746,676"),
                            ("M650,570 C690,566 730,580 762,610", "M652,562 C692,558 732,572 764,602")]):
    wrinkle(a, b, f"Neck fold {i+1}", 5)
# face wrinkles: brow, under the eye, cheek
for i, (a, b) in enumerate([("M600,400 C628,412 648,436 656,466", "M606,394 C634,406 654,430 662,460"),
                            ("M640,368 C668,380 688,406 694,434", "M646,362 C674,374 694,400 700,428"),
                            ("M470,520 C510,540 556,548 596,542", "M470,512 C510,532 556,540 596,534"),
                            ("M480,580 C530,606 590,612 640,604", "M480,572 C530,598 590,604 640,596"),
                            ("M500,640 C550,662 610,666 660,656", "M500,632 C550,654 610,658 660,648")]):
    wrinkle(a, b, f"Face wrinkle {i+1}")
# short creases across the snout top only (a digging snout, not a muzzle)
for i, (a, b) in enumerate([("M346,514 C356,526 362,540 364,556", "M352,510 C362,522 368,536 370,552"),
                            ("M382,486 C394,500 400,516 402,532", "M388,482 C400,496 406,512 408,528")]):
    wrinkle(a, b, f"Snout crease {i+1}", 3)
d.path("M314,652 C360,664 420,668 470,662", "Mouth", fill=NONE, stroke=INK, strokeWidth=5, cap="round")
# sparse bristles along the back of the neck
for i in range(10):
    t = i / 9
    x = 724 + 100 * t
    y = 352 + 320 * t ** 1.3
    d.path(f"M{x:.1f},{y:.1f} L{x + 13:.1f},{y - 7:.1f}", f"Bristle {i+1}", fill=NONE,
           stroke="#3E3634", strokeWidth=3, opacity=55, cap="round")

# --- ear (near) -----------------------------------------------------------------------
d.path("M652,336 C660,294 684,262 714,248 C722,284 708,322 684,348 Z",
       "Ear near", fill=EAR_GRAD, stroke=INK, strokeWidth=5)
d.path("M664,332 C672,300 688,276 708,264 C710,292 700,318 682,336 Z",
       "Ear near inner", fill="#C49E94", opacity=55, stroke=NONE)

# --- snout disc (tilted ellipse seen three-quarter) --------------------------------------
pts = []
for k in range(72):
    a = 2 * math.pi * k / 72
    ex, ey = 24 * math.cos(a), 58 * math.sin(a)
    t = math.radians(-12)
    pts.append((300 + ex * math.cos(t) - ey * math.sin(t), 590 + ex * math.sin(t) + ey * math.cos(t)))
d.path("M%.1f,%.1f " % pts[0] + " ".join("L%.1f,%.1f" % p for p in pts[1:]) + " Z",
       "Snout disc", fill=DISC_GRAD, stroke=INK, strokeWidth=5)
d.path("M290,566 C284,574 284,586 290,592 C296,588 298,574 290,566 Z", "Nostril upper",
       fill="#2A1E1C", stroke=NONE)
d.path("M296,602 C290,610 290,622 296,628 C302,624 304,610 296,602 Z", "Nostril lower",
       fill="#2A1E1C", stroke=NONE)
d.shape("ellipse", "Disc glint", x=300, y=550, width=10, height=16, fill="#FFFFFF", opacity=30, stroke=NONE)

# --- eyes ---------------------------------------------------------------------------------
d.path("M470,404 C478,394 490,392 496,398 C490,408 478,412 470,404 Z", "Eye far",
       fill="#1A1210", opacity=85, stroke=NONE)
d.shape("ellipse", "Eye socket", x=530, y=420, width=58, height=42, fill="#4E4644", opacity=35, stroke=NONE)
d.shape("ellipse", "Eye", x=543, y=431, width=26, height=20, fill="#2A1A12", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Iris", x=549, y=434, width=13, height=13, fill="#6A4A2A", stroke=NONE)
d.shape("ellipse", "Eye glint", x=551, y=435, width=5, height=5, fill="#FFFFFF", opacity=85, stroke=NONE)
d.path("M537,433 C547,421 565,421 575,433", "Upper lid", fill=NONE, stroke=INK, strokeWidth=4, cap="round")
d.path("M539,458 C551,466 567,464 577,454", "Lid fold", fill=NONE, stroke="#3A3230", strokeWidth=3,
       opacity=50, cap="round")


# --- tusks ---------------------------------------------------------------------------------
def collar(cx, cy, label):
    d.shape("ellipse", label, x=cx - 17, y=cy - 7, width=34, height=14, fill="#5E5450",
            opacity=70, stroke=INK, strokeWidth=3)


# near lower tusk: out of the mouth corner, sweeping up beside the snout toward the eye
tusk([(426, 668), (388, 618), (404, 548), (468, 520)], 24, 6, "Tusk lower near", TUSK_GRAD)
# upper pair: punched up through the snout skin, curling right back to the forehead
collar(446, 418, "Tusk collar far")
tusk([(446, 418), (420, 300), (540, 220), (590, 296)], 22, 6, "Tusk upper far", TUSK_FAR_GRAD)
collar(398, 456, "Tusk collar near")
tusk([(398, 456), (348, 320), (470, 214), (532, 312)], 28, 7, "Tusk upper near", TUSK_GRAD)
# --- rim redrawn over the neck so the edge stays crisp ---------------------------------
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#4E3412", strokeWidth=6)

# --- name -----------------------------------------------------------------------------------
d.text("BABIRUSA", "Name", x=500, y=960, size=58, font="Virelai Sans",
       color="#F0D8A8", justify="center")

d.finish("babirusa-V1R00")
