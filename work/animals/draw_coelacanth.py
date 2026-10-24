#!/usr/bin/env python3
"""Coelacanth — field plate V1R00. Full body in profile drifting right:
the lobed-finned relic, extinct for sixty-six million years until it
wasn't. Midnight blue body scattered with cream flecks, fleshy stalked
paired fins, a spiny first dorsal and the trident tail. Abyss teal plate
with light shafts, marine snow and a rock ledge closing on the disc arc.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Coelacanth — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#0A141E"   # abyss navy, not black


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


def arc_closed(contour):
    """contour runs left disc point -> right disc point over the top; close it
    clockwise along the disc's own arc through the bottom."""
    for x, y in (contour[0], contour[-1]):
        assert abs(math.hypot(x - PCX, y - PCY) - PR) < 1.5, (x, y)
    (lx, ly) = contour[0]
    return smooth(contour, closed=False) + f" A420,420 0 0 1 {lx:.1f},{ly:.1f} Z"


BG_GRAD = lin("#0A141E", "#02060C", [0, 0], [0, 1000])
PLATE_GRAD = rad("#316273", "#1B3D4C", "#081A22")
BODY_GRAD = lin("#48709A", "#162B48", [500, 380], [500, 580])
FIN_GRAD = lin("#3E648E", "#152A44", [500, 480], [500, 680])
FAR_FIN_GRAD = lin("#25466A", "#0E1F34", [500, 480], [500, 680])

# --- backdrop + plate -----------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876, fill="#5A9AA8", opacity=6, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#0C242E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#8FC2C8", strokeWidth=3, opacity=45)
# light shafts slanting down from the surface, tips well inside the rim
for i, (x0, w0, x1, w1, yend) in enumerate([(300, 40, 380, 90, 430), (520, 50, 560, 110, 460),
                                           (700, 36, 640, 80, 400)]):
    y0 = PCY - math.sqrt(PR ** 2 - (x0 - PCX) ** 2) + 14
    assert on_disc(x1, yend, 10), i
    d.path(f"M{x0},{y0:.0f} L{x0 + w0},{y0:.0f} L{x1 + w1},{yend} L{x1 - w1},{yend} Z",
           f"Light shaft {i+1}", fill="#BFE6EC", opacity=7, stroke=NONE)
# marine snow drifting through the plate
for i, (x, y, w) in enumerate([(190, 250, 5), (770, 200, 6), (150, 420, 5), (845, 380, 6),
                               (230, 600, 4), (800, 590, 5), (300, 130, 5), (600, 120, 4),
                               (430, 170, 4), (170, 330, 4), (860, 480, 5), (260, 720, 5),
                               (750, 700, 4), (420, 810, 4), (580, 800, 5), (490, 90, 4)]):
    assert on_disc(x + w / 2, y + w / 2, 4), i
    d.shape("ellipse", f"Marine snow {i+1}", x=x, y=y, width=w, height=w,
            fill="#D8ECE8", opacity=40, stroke=NONE)

# --- rock ledge across the bottom, closing on the disc arc ------------------------
y0 = 800
LEDGE = [(disc_x(y0, -1), y0), (205, 778), (300, 762), (390, 776), (470, 760),
         (560, 774), (660, 762), (745, 780), (disc_x(790, 1), 790)]
d.path(arc_closed(LEDGE), "Rock ledge", fill=lin("#12202C", "#060E16", (500, 760), (500, 880)),
       stroke=NONE)
# ledge cracks + a dim sponge or two rooted on it
for lbl, dd in [("Ledge crack 1", "M300,790 L330,830 L322,860"),
                ("Ledge crack 2", "M560,788 L545,828 L560,858"),
                ("Ledge crack 3", "M700,792 L716,824")]:
    d.path(dd, lbl, fill=NONE, stroke="#2C4252", strokeWidth=4, opacity=50, cap="round")
for i, (x, y, h) in enumerate([(352, 776, 26), (628, 768, 22)]):
    d.path(f"M{x},{y} C{x - 10},{y - h * 0.7} {x - 6},{y - h} {x},{y - h - 8} "
           f"C{x + 6},{y - h} {x + 10},{y - h * 0.7} {x},{y} Z",
           f"Sponge {i+1}", fill="#3A5468", opacity=55, stroke=NONE)

# --- lobed fins: a fleshy stalk widening into a scalloped ray fan -------------------
def lobed_fin(base, tip, w0, wt, label, grad, far=False):
    """Closed paddle: narrow muscular stalk flaring to a scalloped blade.
    base/tip are points; w0 stalk half-width, wt fan half-width."""
    bx, by = base
    ux, uy = tip[0] - bx, tip[1] - by
    ln = math.hypot(ux, uy) or 1
    ux, uy = ux / ln, uy / ln
    nx, ny = -uy, ux
    # distal fan edge: five points across, outer pair recessed => scalloped rim
    edge = [(-1.0, -0.10), (-0.45, 0.06), (0.0, -0.06), (0.45, 0.06), (1.0, -0.10)]
    fan = [(tip[0] + nx * wt * s + ux * wt * 0.5 * v,
            tip[1] + ny * wt * s + uy * wt * 0.5 * v) for s, v in edge]
    mid = (bx + ux * ln * 0.55, by + uy * ln * 0.55)
    wm = (w0 + wt) * 0.55
    pts = [(bx - nx * w0, by - ny * w0),
           (mid[0] - nx * wm, mid[1] - ny * wm),
           fan[0], fan[1], fan[2], fan[3], fan[4],
           (mid[0] + nx * wm, mid[1] + ny * wm),
           (bx + nx * w0, by + ny * w0)]
    for p in pts:
        assert on_disc(*p, 4), (label, p)
    d.path(smooth(pts), label, fill=grad, stroke=INK,
           strokeWidth=4 if not far else 3, opacity=55 if far else 100)
    # ray strokes fanning from mid-stalk to the blade edge
    if not far:
        for j, (fx, fy) in enumerate(fan[1:4]):
            d.path(f"M{mid[0]:.0f},{mid[1]:.0f} L{fx:.0f},{fy:.0f}",
                   f"{label} ray {j+1}", fill=NONE, stroke="#7FA6C2",
                   strokeWidth=3, opacity=45, cap="round")


# far pectoral + far pelvic, ghosted slivers behind the body
lobed_fin((662, 505), (700, 615), 9, 26, "Far pectoral", FAR_FIN_GRAD, far=True)
lobed_fin((468, 545), (440, 640), 8, 24, "Far pelvic", FAR_FIN_GRAD, far=True)

# --- tail: the trident — fleshy upper and lower lobes plus the central tuft ---------
d.path(smooth([(280, 440), (252, 410), (220, 368), (198, 330), (186, 312),
               (208, 354), (229, 398), (244, 436), (250, 452),
               (216, 452), (168, 464), (216, 478), (250, 484),
               (246, 500), (226, 542), (202, 580), (188, 598),
               (214, 552), (230, 518), (252, 496), (280, 484)]),
       "Tail fin", fill=FIN_GRAD, stroke=INK, strokeWidth=5)
for lbl, dd in [("Tail ray 1", "M258,446 C230,422 208,390 198,352"),
                ("Tail ray 2", "M254,492 C230,518 212,548 202,582"),
                ("Tail ray 3", "M252,468 C228,467 208,466 190,465")]:
    d.path(dd, lbl, fill=NONE, stroke="#7FA6C2", strokeWidth=4, opacity=45, cap="round")

# --- body ---------------------------------------------------------------------------
BODY = smooth([(760, 466), (726, 430), (664, 402), (580, 388), (470, 390),
               (370, 402), (300, 424), (272, 446), (264, 470), (272, 496),
               (310, 522), (390, 546), (490, 556), (580, 552), (664, 532),
               (720, 506), (752, 486)])
d.path(BODY, "Body", fill=BODY_GRAD, stroke=INK, strokeWidth=6)
# belly sheen + dorsal depth
d.path("M310,516 C390,540 480,550 560,546 C620,542 680,524 716,502 "
       "C680,530 600,556 500,554 C410,552 340,538 310,516 Z",
       "Belly sheen", fill="#7EA4BC", opacity=35, stroke=NONE)
d.path("M300,428 C380,402 480,392 570,394 C640,396 700,418 730,444 "
       "C690,422 620,404 540,404 C450,404 360,414 300,428 Z",
       "Back depth", fill="#12283E", opacity=35, stroke=NONE)
# lateral line
d.path("M296,470 C400,462 560,462 700,476", "Lateral line", fill=NONE,
       stroke="#0E2236", strokeWidth=3, opacity=50, cap="round")
# the cream flecks — speckled scales out of the deep
FLECKS = [(330, 440, 8, 6), (360, 478, 6, 5), (395, 425, 7, 5), (420, 462, 9, 6),
          (445, 505, 7, 5), (470, 432, 6, 5), (495, 470, 8, 6), (515, 516, 6, 5),
          (540, 428, 7, 5), (560, 475, 9, 6), (585, 518, 7, 5), (605, 440, 6, 5),
          (625, 486, 8, 6), (645, 452, 6, 4), (665, 500, 7, 5), (685, 465, 6, 5),
          (375, 515, 6, 5), (705, 490, 5, 4), (440, 535, 6, 4), (300, 460, 5, 4),
          (520, 545, 5, 4), (585, 415, 5, 4)]
for i, (x, y, w, h) in enumerate(FLECKS):
    d.shape("ellipse", f"Fleck {i+1}", x=x - w / 2, y=y - h / 2, width=w, height=h,
            fill="#E4DCC2", opacity=60, stroke=NONE)

# --- first dorsal: the spiny fan on the front of the back -----------------------------
d.path("M560,398 C575,360 610,336 650,330 C635,362 618,384 596,398 Z",
       "Dorsal 1 membrane", fill=FIN_GRAD, stroke=INK, strokeWidth=4, opacity=95)
for j in range(6):
    t = j / 5
    bx, by = 565 + 30 * t, 396
    tx = 585 + 62 * t - 20 * math.sin(math.pi * t)
    ty = 340 + 8 * math.sin(math.pi * t) + 4 * t
    d.path(f"M{bx:.0f},{by} L{tx:.0f},{ty:.0f}", f"Dorsal spine {j+1}",
           fill=NONE, stroke="#0E2236", strokeWidth=4, opacity=70, cap="round")

# --- second dorsal + anal: lobed fins, stalked ----------------------------------------
lobed_fin((432, 398), (398, 322), 9, 22, "Dorsal 2", FIN_GRAD)
lobed_fin((330, 518), (274, 614), 9, 28, "Anal fin", FIN_GRAD)
# near paired fins over the body edge
lobed_fin((648, 512), (596, 628), 11, 34, "Pectoral", FIN_GRAD)
lobed_fin((505, 548), (452, 654), 10, 30, "Pelvic", FIN_GRAD)

# --- head detail ----------------------------------------------------------------------
# gill cover arc
d.path("M662,428 C646,456 644,492 660,522", "Gill cover", fill=NONE,
       stroke=INK, strokeWidth=5, opacity=60, cap="round")
# eye: large, low-set, ancient
d.shape("ellipse", "Eye", x=688, y=440, width=34, height=34, fill="#0A141E", stroke="#7FA6C2", strokeWidth=3)
d.shape("ellipse", "Eye glint", x=697, y=447, width=8, height=8, fill="#FFFFFF", opacity=85, stroke=NONE)
# downturned mouth: the sixty-six-million-year frown
d.path("M722,498 C734,502 748,500 758,492", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
# rostral pores on the snout
for i, (x, y) in enumerate([(742, 462), (752, 472), (736, 478)]):
    d.shape("ellipse", f"Pore {i+1}", x=x, y=y, width=4, height=4, fill="#0E2236", opacity=70, stroke=NONE)
# snout sheen
d.path("M716,436 C732,444 744,456 752,470", "Snout sheen", fill=NONE,
       stroke="#9EC2D4", strokeWidth=4, opacity=40, cap="round")

# --- name -----------------------------------------------------------------------------
d.text("COELACANTH", "Name", x=500, y=962, size=56, font="Virelai Sans",
       color="#BCD8DA", justify="center")

d.finish("coelacanth-V1R00")
