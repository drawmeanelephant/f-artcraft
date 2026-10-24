#!/usr/bin/env python3
"""Hammerhead shark — field plate V1R00. The head that widened until it was a
tool: oblique profile cruising left over a sand flat, cephalofoil drawn in
foreshortened plan so the bar reads, scalloped leading edge with a shallow
central notch (great hammerhead), near eye at the ventral tip, far eye dim at
the dorsal tip. Blue plate, scanning mood — pale sense-arcs sweep from the
head down to the sand. 1000x1000. House style: gradients + translucent
shading, never flat fills. Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Hammerhead Shark — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#132637"


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


def ell_path(cx, cy, rx, ry, deg, n=16):
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


BG_GRAD = lin("#061626", "#02070E", [0, 0], [0, 1000])
PLATE_GRAD = rad("#3E7CA0", "#235878", "#0D2F4A")
BODY_GRAD = {"gradient": {"kind": "linear", "start": [500, 360], "end": [500, 580], "stops": [
    {"offset": 0, "color": "#33516B"}, {"offset": 0.6, "color": "#52788E"},
    {"offset": 1, "color": "#A9BEC5"}]}}
FIN_GRAD = lin("#33536C", "#1E384E", [500, 300], [500, 560])
CEPH_GRAD = rad("#64889E", "#41637A", "#2A485E")
SAND_GRAD = lin("#B29468", "#6B5535", [500, 760], [500, 880])

# --- backdrop + blue plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=58, y=18, width=884, height=884, fill="#4E94B8", opacity=7, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#0A2C46", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#9CC4D8", strokeWidth=3, opacity=40)
# light shafts slanting down from the surface
for i, (x0, w0, x1, w1, yend) in enumerate([(330, 42, 400, 95, 440), (560, 48, 590, 105, 470),
                                           (740, 34, 690, 78, 420)]):
    y0 = PCY - math.sqrt(PR ** 2 - (x0 - PCX) ** 2) + 14
    assert on_disc(x1, yend, 10), i
    d.path(f"M{x0},{y0:.0f} L{x0 + w0},{y0:.0f} L{x1 + w1},{yend} L{x1 - w1},{yend} Z",
           f"Light shaft {i+1}", fill="#D4EEF6", opacity=8, stroke=NONE)
# marine snow
for i, (x, y, w) in enumerate([(205, 260, 5), (780, 215, 6), (160, 430, 5), (848, 390, 6),
                               (240, 610, 4), (800, 600, 5), (310, 140, 5), (610, 130, 4),
                               (440, 180, 4), (180, 340, 4), (855, 490, 5), (270, 720, 4),
                               (700, 170, 5), (500, 100, 4)]):
    assert on_disc(x + w / 2, y + w / 2, 4), i
    d.shape("ellipse", f"Snow {i+1}", x=x, y=y, width=w, height=w,
            fill="#D8ECEE", opacity=40, stroke=NONE)

# --- sand flat across the bottom, closing on the disc arc ---------------------------
y0 = 772
SAND = [(disc_x(y0, -1), y0), (300, 758), (390, 774), (470, 762),
        (560, 776), (650, 760), (735, 770), (disc_x(y0, 1), y0)]
d.path(arc_closed(SAND), "Sand flat", fill=SAND_GRAD, stroke=NONE)
# ripple strokes + a faint buried shape in the sand (what it is scanning for)
for lbl, dd in [("Ripple 1", "M300,800 C350,792 420,792 470,800"),
                ("Ripple 2", "M520,812 C580,804 660,804 710,812"),
                ("Ripple 3", "M380,826 C440,818 520,818 570,826")]:
    d.path(dd, lbl, fill=NONE, stroke="#7A6242", strokeWidth=4, opacity=45, cap="round")
d.path("M520,802 C560,790 620,790 655,802 C620,812 560,812 520,802 Z",
       "Buried shape", fill="#54402A", opacity=30, stroke=NONE)

# --- sense arcs sweeping from the head down toward the sand --------------------------
for i, dd in enumerate(["M258,520 C222,600 236,690 312,748",
                        "M292,548 C270,612 284,678 344,722"]):
    d.path(dd, f"Sense arc {i+1}", fill=NONE, stroke="#9FD8E8", strokeWidth=4,
           opacity=10 + i * 3, cap="round")

# --- tail fin: heterocercal, big upper lobe, subterminal notch -----------------------
d.path(smooth([(728, 438), (768, 390), (800, 336), (824, 282), (836, 254),
               (816, 298), (788, 356), (760, 414), (756, 448),
               (768, 472), (790, 508), (762, 506), (738, 480)]),
       "Tail fin", fill=FIN_GRAD, stroke=INK, strokeWidth=5)
d.path("M770,380 C790,340 810,300 826,262", "Tail upper ray", fill=NONE,
       stroke="#7FA6C2", strokeWidth=4, opacity=40, cap="round")

# --- second dorsal, far pectoral (dim), pelvic, anal ----------------------------------
d.path("M650,398 C658,378 670,362 686,352 C692,372 702,388 714,402 "
       "C694,398 672,396 650,398 Z", "Dorsal 2", fill=FIN_GRAD, stroke=INK,
       strokeWidth=4, opacity=90)
d.path("M560,548 C576,572 592,590 608,598 C586,596 560,578 548,556 Z",
       "Far pectoral", fill=FIN_GRAD, stroke=NONE, opacity=45)
d.path("M610,538 C622,562 636,578 650,586 C632,584 612,566 602,546 Z",
       "Pelvic fin", fill=FIN_GRAD, stroke=INK, strokeWidth=3, opacity=85)
d.path("M688,490 C696,508 706,522 718,528 C703,528 690,513 684,498 Z",
       "Anal fin", fill=FIN_GRAD, stroke=INK, strokeWidth=3, opacity=85)

# --- first dorsal: tall, pointed, slightly falcate -------------------------------------
d.path("M498,376 C534,338 566,300 592,268 C600,302 624,348 650,394 "
       "C602,382 546,374 498,376 Z", "Dorsal 1", fill=FIN_GRAD, stroke=INK, strokeWidth=5)
d.path("M560,340 C570,318 580,296 590,278", "Dorsal ray", fill=NONE,
       stroke="#7FA6C2", strokeWidth=3, opacity=40, cap="round")

# --- body ------------------------------------------------------------------------------
BODY = smooth([(298, 462), (368, 508), (455, 540), (540, 556), (630, 548),
               (700, 505), (742, 468), (752, 450), (744, 420), (690, 402),
               (620, 385), (560, 376), (505, 372), (455, 382), (400, 400), (344, 416)])
d.path(BODY, "Body", fill=BODY_GRAD, stroke=INK, strokeWidth=6)
# belly countershade + dorsal depth
d.path("M395,505 C450,545 540,560 620,545 C675,535 715,505 740,475 "
       "C700,520 620,555 530,552 C465,550 415,532 395,505 Z",
       "Belly light", fill="#C4D4D8", opacity=30, stroke=NONE)
d.path("M380,428 C440,392 540,370 630,386 C570,382 480,396 420,428 "
       "C400,438 388,436 380,428 Z", "Back depth", fill="#16283C", opacity=30, stroke=NONE)
# lateral line + gill slits
d.path("M370,470 C470,486 600,486 712,458", "Lateral line", fill=NONE,
       stroke="#1A3048", strokeWidth=3, opacity=50, cap="round")
for i in range(5):
    x = 386 + i * 9
    d.path(f"M{x},{438 + i * 2} C{x - 4},{458} {x - 2},{476} {x + 2},{492}",
           f"Gill slit {i+1}", fill=NONE, stroke=INK, strokeWidth=4, opacity=45, cap="round")

# --- near pectoral fin --------------------------------------------------------------------
d.path("M436,494 C462,542 502,600 544,648 C502,642 446,598 412,540 "
       "C408,520 420,503 436,494 Z", "Pectoral", fill=FIN_GRAD, stroke=INK, strokeWidth=5)
d.path("M446,530 C470,568 500,606 528,634", "Pectoral ray", fill=NONE,
       stroke="#7FA6C2", strokeWidth=3, opacity=40, cap="round")

# --- cephalofoil: the tool itself ---------------------------------------------------------
# shallow crescent swung forward across the head front: near tip low-left toward
# the viewer, far tip wrapping back over the neck. Leading edge = upper rim.
def qbez(p0, p1, p2, t):
    u = 1 - t
    return (u * u * p0[0] + 2 * u * t * p1[0] + t * t * p2[0],
            u * u * p0[1] + 2 * u * t * p1[1] + t * t * p2[1])


def qtan(p0, p1, p2, t):
    return (2 * (1 - t) * (p1[0] - p0[0]) + 2 * t * (p2[0] - p1[0]),
            2 * (1 - t) * (p1[1] - p0[1]) + 2 * t * (p2[1] - p1[1]))


P0, P1, P2 = (235, 478), (295, 395), (425, 450)
HALF = 24
front, rear = [], []
for i in range(19):
    t = i / 18
    px, py = qbez(P0, P1, P2, t)
    gx, gy = qtan(P0, P1, P2, t)
    ln = math.hypot(gx, gy) or 1
    nx, ny = -gy / ln, gx / ln
    if ny > 0:                     # upper rim = leading edge faces up-left
        nx, ny = -nx, -ny
    s_ = 2 * t - 1                 # -1 near tip .. +1 far tip
    notch = 12 * math.exp(-(s_ / 0.15) ** 2) - 5 * math.exp(-((abs(s_) - 0.58) / 0.18) ** 2)
    front.append((px + nx * (HALF + notch), py + ny * (HALF + notch)))
    rear.append((px - nx * HALF, py - ny * HALF))
d.path(smooth(front + rear[::-1]), "Cephalofoil", fill=CEPH_GRAD, stroke=INK, strokeWidth=6)
# soft light pooling on the bar's upper face + shade along the leading rim
d.path(ell_path(322, 412, 55, 20, -10), "Bar light", fill="#9CC0D0", opacity=16, stroke=NONE)
d.path("M238,462 C252,436 284,414 322,404", "Front rim shade", fill=NONE,
       stroke="#1E384E", strokeWidth=8, opacity=45, cap="round")
# nares: short slits on the leading edge near each tip
d.path("M246,468 L236,458", "Naris near", fill=NONE, stroke=INK, strokeWidth=4, opacity=60, cap="round")
d.path("M408,436 L416,426", "Naris far", fill=NONE, stroke=INK, strokeWidth=4, opacity=45, cap="round")
# ampullae pores peppering the leading edge
for i, (x, y) in enumerate([(262, 450), (284, 432), (308, 418), (332, 410), (356, 410), (384, 416)]):
    d.shape("ellipse", f"Pore {i+1}", x=x, y=y, width=4, height=4, fill="#14293E", opacity=70, stroke=NONE)
# eyes at the bar tips
d.path(ell_path(228, 466, 12, 15, -55), "Eye near", fill="#0E1E2C", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Eye glint", x=224, y=460, width=6, height=6, fill="#FFFFFF", opacity=85, stroke=NONE)
d.path(ell_path(418, 438, 8, 10, -10), "Eye far", fill="#0E1E2C", stroke=NONE, opacity=70)
# underside mouth: the wide frown behind the bar
d.path("M305,478 C330,492 358,490 378,474", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=5, opacity=70, cap="round")

# --- name -------------------------------------------------------------------------------
d.text("HAMMERHEAD SHARK", "Name", x=500, y=962, size=56, font="Virelai Sans",
       color="#C4DCE4", justify="center")

d.finish("hammerhead-shark-V1R00")
