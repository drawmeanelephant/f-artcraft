#!/usr/bin/env python3
"""Atlantic sailfish — field plate V1R00. The fastest fish, wearing a sail:
left profile driving at a sardine baitball, dorsal sail fully erect with
its dark spot scatter, long round bill, lunate forked tail, filament pelvic
fins trailing. Blue-water plate, baitball mood. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Atlantic Sailfish — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#0F2438"


def on_disc(x, y, pad):
    return math.hypot(x - PCX, y - PCY) <= PR - pad


def disc_x(y, side):
    return PCX + side * math.sqrt(PR ** 2 - (y - PCY) ** 2)


def lin(c0, c1, start=None, end=None):
    g = {"kind": "linear", "stops": [{"offset": 0, "color": c0}, {"offset": 1, "color": c1}]}
    if start: g["start"], g["end"] = [round(v, 1) for v in start], [round(v, 1) for v in end]
    return {"gradient": g}


def rad(*stops):
    n = len(stops) - 1
    return {"gradient": {"kind": "radial", "stops": [
        {"offset": round(i / n, 3), "color": c} for i, c in enumerate(stops)]}}


def smooth(pts, closed=True, k=1.0):
    n = len(pts)
    s = "M%.1f,%.1f" % pts[0]
    for i in (range(n) if closed else range(n - 1)):
        p0 = pts[(i - 1) % n] if (closed or i > 0) else pts[0]
        p1, p2 = pts[i], pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (closed or i + 2 < n) else pts[-1]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6 * k, p1[1] + (p2[1] - p0[1]) / 6 * k)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6 * k, p2[1] - (p3[1] - p1[1]) / 6 * k)
        s += " C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (c1 + c2 + p2)
    return s + (" Z" if closed else "")


def ell_path(cx, cy, rx, ry, deg, n=14):
    """Rotated ellipse as a closed smooth path (shapes can't rotate)."""
    t = math.radians(deg)
    c, s = math.cos(t), math.sin(t)
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        ex, ey = rx * math.cos(a), ry * math.sin(a)
        pts.append((cx + ex * c - ey * s, cy + ex * s + ey * c))
    return smooth(pts)


def arc_closed(contour):
    """contour runs left disc point -> right disc point over the top; close it
    clockwise along the disc's own arc through the bottom."""
    for x, y in (contour[0], contour[-1]):
        assert abs(math.hypot(x - PCX, y - PCY) - PR) < 1.5, (x, y)
    (lx, ly) = contour[0]
    return smooth(contour, closed=False) + f" A420,420 0 0 1 {lx:.1f},{ly:.1f} Z"


BG_GRAD = lin("#071C30", "#020910", [0, 0], [0, 1000])
PLATE_GRAD = rad("#2E6C9C", "#1A4668", "#0B2740")
BODY_GRAD = {"gradient": {"kind": "linear", "start": [500, 380], "end": [500, 590], "stops": [
    {"offset": 0, "color": "#1C3C60"}, {"offset": 0.45, "color": "#3A6A90"},
    {"offset": 0.8, "color": "#84A8B8"}, {"offset": 1, "color": "#BCCDD2"}]}}
SAIL_GRAD = {"gradient": {"kind": "linear", "start": [500, 180], "end": [500, 400], "stops": [
    {"offset": 0, "color": "#2A64A0"}, {"offset": 0.6, "color": "#17406C"},
    {"offset": 1, "color": "#0E2C4E"}]}}
FIN_GRAD = lin("#2A5478", "#122C48", [600, 380], [640, 560])
WATER_GRAD = lin("#12324A", "#071C2E", [500, 780], [500, 880])
SARDINE = "#C9D9DE"

# --- backdrop + blue-water plate ------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=56, y=16, width=888, height=888, fill="#4E9CC8", opacity=7, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#0A2C48", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#8CC0DC", strokeWidth=3, opacity=40)
# light shafts down from the surface
for i, (x0, w0, x1, w1, yend) in enumerate([(350, 40, 420, 92, 450), (580, 46, 620, 108, 480),
                                           (750, 34, 700, 76, 430)]):
    y0 = PCY - math.sqrt(PR ** 2 - (x0 - PCX) ** 2) + 14
    assert on_disc(x1, yend, 10), i
    d.path(f"M{x0},{y0:.0f} L{x0 + w0},{y0:.0f} L{x1 + w1},{yend} L{x1 - w1},{yend} Z",
           f"Light shaft {i+1}", fill="#CFEAF6", opacity=8, stroke=NONE)
# marine snow
for i, (x, y, w) in enumerate([(200, 260, 5), (790, 220, 6), (155, 430, 5), (852, 390, 6),
                               (250, 640, 4), (810, 610, 5), (315, 140, 5), (620, 128, 4),
                               (445, 175, 4), (175, 350, 4), (858, 500, 5), (280, 720, 4),
                               (705, 165, 5), (500, 95, 4)]):
    assert on_disc(x + w / 2, y + w / 2, 4), i
    d.shape("ellipse", f"Snow {i+1}", x=x, y=y, width=w, height=w,
            fill="#D8ECEE", opacity=38, stroke=NONE)

# --- deep water band across the bottom, closing on the disc arc -------------------------
y0 = 790
WATER = [(disc_x(y0, -1), y0), (300, 778), (420, 792), (560, 780), (690, 792),
         (disc_x(y0, 1), y0)]
d.path(arc_closed(WATER), "Deep band", fill=WATER_GRAD, stroke=NONE)

# --- the baitball: a swirl of sardines upper-left, drifting strays ----------------------
d.shape("ellipse", "Baitball shimmer", x=215, y=205, width=180, height=150,
        fill="#BFE0EA", opacity=10, stroke=NONE)
BAIT = [(250, 250, -25, 90), (290, 235, -15, 85), (330, 245, -35, 80),
        (270, 285, -10, 90), (310, 275, -20, 75), (350, 290, -30, 85),
        (240, 305, -15, 70), (295, 315, -25, 80), (340, 320, -15, 75),
        (265, 335, -35, 65), (315, 345, -20, 70), (230, 270, -20, 60),
        (340, 248, -40, 70), (352, 288, -25, 65), (255, 220, -10, 60),
        (346, 340, -30, 55), (215, 330, -15, 60), (335, 362, -20, 50)]
for i, (x, y, ang, op) in enumerate(BAIT):
    d.path(ell_path(x, y, 11, 4.5, ang), f"Sardine {i+1}", fill=SARDINE,
           opacity=op, stroke=NONE)
# fleeing strays, wider scatter toward the bill
for i, (x, y, ang) in enumerate([(195, 245, -45), (180, 300, -35), (205, 370, -50), (395, 168, -15)]):
    d.path(ell_path(x, y, 12, 5, ang), f"Stray {i+1}", fill=SARDINE, opacity=75, stroke=NONE)

# --- lunate tail: long pointed lobes, deep central fork ----------------------------------
d.path(smooth([(742, 442), (795, 408), (840, 372), (868, 352),
               (852, 396), (830, 440), (812, 468),
               (830, 500), (852, 540), (866, 566),
               (838, 546), (798, 512), (748, 486)]),
       "Tail fin", fill=FIN_GRAD, stroke=INK, strokeWidth=5)
for i, dd in enumerate(["M770,448 C800,420 830,392 856,366",
                        "M770,478 C800,498 830,524 854,548"]):
    d.path(dd, f"Tail ray {i+1}", fill=NONE, stroke="#7FA6C2", strokeWidth=3,
           opacity=40, cap="round")

# --- the sail: fully erect, quarter-disc fan on the back ----------------------------------
SAIL = smooth([(362, 394), (368, 302), (398, 236), (458, 196), (536, 180),
               (610, 198), (658, 252), (686, 326), (700, 394)])
d.path(SAIL + " Z", "Sail", fill=SAIL_GRAD, stroke=INK, strokeWidth=5)
# anterior rays poking past the leading edge
d.path("M368,330 L356,306", "Sail spike 1", fill=NONE, stroke=INK, strokeWidth=4, cap="round")
d.path("M382,272 L372,246", "Sail spike 2", fill=NONE, stroke=INK, strokeWidth=4, cap="round")
# membrane rays fanning up from the base
for i, (bx, tx, ty) in enumerate([(390, 400, 260), (440, 462, 218), (495, 522, 196),
                                  (550, 580, 204), (605, 632, 240), (655, 672, 300)]):
    d.path(f"M{bx},392 L{tx},{ty}", f"Sail ray {i+1}", fill=NONE,
           stroke="#0C2A48", strokeWidth=4, opacity=55, cap="round")
# the spot scatter: dark cobalt freckles on the membrane
SPOTS = [(420, 300, 7, 9), (460, 260, 6, 8), (505, 235, 7, 8), (550, 232, 6, 8),
         (595, 250, 7, 9), (630, 285, 6, 8), (655, 330, 6, 7), (440, 340, 6, 8),
         (490, 290, 6, 8), (540, 285, 7, 8), (585, 315, 6, 8), (510, 340, 6, 7),
         (615, 350, 5, 7), (460, 365, 5, 7), (560, 360, 6, 7), (400, 345, 5, 7)]
for i, (x, y, w, h) in enumerate(SPOTS):
    d.shape("ellipse", f"Sail spot {i+1}", x=x - w / 2, y=y - h / 2, width=w, height=h,
            fill="#081F3A", opacity=65, stroke=NONE)

# --- body ---------------------------------------------------------------------------------
BODY = smooth([(296, 462), (322, 424), (352, 398), (420, 386), (510, 386),
               (610, 392), (690, 404), (740, 430), (752, 452), (742, 472),
               (700, 496), (620, 528), (540, 556), (460, 566), (390, 552),
               (338, 524), (308, 492)])
d.path(BODY, "Body", fill=BODY_GRAD, stroke=INK, strokeWidth=6)
# the bill: long round rostrum
d.path("M300,462 C260,462 215,466 172,472 C215,472 258,474 300,478 "
       "C292,472 292,468 300,462 Z", "Bill", fill="#2A4A68", stroke=INK, strokeWidth=3)
# flank sheen + back depth
d.path("M330,520 C400,548 500,562 590,540 C540,568 430,570 360,540 "
       "C340,532 330,526 330,520 Z", "Belly light", fill="#D2E0E4", opacity=28, stroke=NONE)
d.path("M350,400 C440,382 560,384 660,398 C570,392 450,392 370,410 "
       "C355,412 348,406 350,400 Z", "Back depth", fill="#0C2038", opacity=30, stroke=NONE)
# lateral line + faint cobalt bars (the hunting flash)
d.path("M320,478 C430,472 580,474 720,462", "Lateral line", fill=NONE,
       stroke="#16304C", strokeWidth=3, opacity=55, cap="round")
for i, x in enumerate([380, 420, 460, 500, 540, 580, 620, 660]):
    y1 = 415 + 14 * math.sin((x - 380) / 300 * math.pi)
    d.path(f"M{x},{y1 + 20} C{x - 4},{y1 + 55} {x - 2},{y1 + 90} {x + 4},{y1 + 118}",
           f"Flank bar {i+1}", fill=NONE, stroke="#2A5E92", strokeWidth=9,
           opacity=28, cap="round")

# --- fins -----------------------------------------------------------------------------------
# pelvic filaments: the long streamers under the mid-body
d.path("M470,556 C462,596 456,632 460,664", "Pelvic 1", fill=NONE,
       stroke=FIN_GRAD, strokeWidth=5, cap="round")
d.path("M490,560 C484,598 480,630 486,658", "Pelvic 2", fill=NONE,
       stroke=FIN_GRAD, strokeWidth=4, cap="round")
# pectoral fin folded on the flank
d.path(smooth([(470, 500), (516, 524), (556, 560), (566, 588), (544, 596),
               (508, 566), (476, 532)]),
       "Pectoral", fill=FIN_GRAD, stroke=INK, strokeWidth=4, opacity=90)
# second dorsal + anal: small matched fins at the peduncle
d.path("M672,398 C682,382 696,372 712,368 C708,384 702,396 694,406 Z",
       "Dorsal 2", fill=FIN_GRAD, stroke=INK, strokeWidth=3, opacity=90)
d.path("M664,506 C676,516 690,522 706,524 C698,510 688,500 676,496 Z",
       "Anal fin", fill=FIN_GRAD, stroke=INK, strokeWidth=3, opacity=85)

# --- head detail -----------------------------------------------------------------------------
# gill cover arc
d.path("M356,428 C342,452 340,486 352,514", "Gill cover", fill=NONE,
       stroke=INK, strokeWidth=4, opacity=55, cap="round")
# eye: dark, gold-rimmed
d.shape("ellipse", "Eye", x=326, y=448, width=24, height=24, fill="#0A1824",
        stroke="#C8A64E", strokeWidth=3)
d.shape("ellipse", "Eye glint", x=333, y=453, width=6, height=6, fill="#FFFFFF", opacity=85, stroke=NONE)
# nostril pit at the bill base
d.shape("ellipse", "Nostril", x=302, y=452, width=6, height=5, fill="#0A1824", opacity=70, stroke=NONE)

# --- name ------------------------------------------------------------------------------------
d.text("ATLANTIC SAILFISH", "Name", x=500, y=962, size=54, font="Virelai Sans",
       color="#C4DCE8", justify="center")

d.finish("atlantic-sailfish-V1R00")
