#!/usr/bin/env python3
"""Anglerfish — field plate V1R00. A lantern in the dark, a mouth around the
lantern: globular black seadevil in left profile, gape wide under the glowing
esca, needle fangs along both jaws, illicium arcing off the forehead. Abyss
plate, lure mood — the esca is the only light in the water. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Anglerfish — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#060D14"


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


BG_GRAD = lin("#050A12", "#010204", [0, 0], [0, 1000])
PLATE_GRAD = rad("#17323E", "#0A1A24", "#030A10")
BODY_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#31434F"}, {"offset": 0.65, "color": "#1A2830"},
    {"offset": 1, "color": "#0D161C"}]}}
MOUTH_GRAD = rad("#2E1622", "#140A12", "#070309")
FIN_GRAD = lin("#22323E", "#0C161E", [600, 380], [640, 560])
SILT_GRAD = lin("#0E2028", "#050C12", [500, 740], [500, 880])
LURE = "#DFFCE8"

# --- backdrop + abyss plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=56, y=16, width=888, height=888, fill="#1E5A64", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#071922", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#3A6E78", strokeWidth=3, opacity=40)

# marine snow + sparse bioluminescent pinpricks
for i, (x, y, w) in enumerate([(210, 280, 5), (780, 230, 6), (160, 450, 5), (850, 400, 6),
                               (250, 630, 4), (810, 620, 5), (320, 150, 5), (620, 140, 4),
                               (450, 190, 4), (180, 350, 4), (860, 510, 5), (730, 730, 4),
                               (560, 120, 4), (380, 790, 4)]):
    assert on_disc(x + w / 2, y + w / 2, 4), i
    d.shape("ellipse", f"Snow {i+1}", x=x, y=y, width=w, height=w,
            fill="#9AD4DC", opacity=38, stroke=NONE)
for i, (x, y) in enumerate([(305, 215), (730, 270), (220, 590), (770, 660), (555, 130)]):
    d.shape("ellipse", f"Glow speck {i+1}", x=x, y=y, width=5, height=5,
            fill="#7EF0C8", opacity=55, stroke=NONE)

# --- abyssal silt, closing on the disc arc -------------------------------------------
y0 = 770
SILT = [(disc_x(y0, -1), y0), (310, 760), (430, 772), (560, 762), (680, 774),
        (disc_x(y0, 1), y0)]
d.path(arc_closed(SILT), "Silt band", fill=SILT_GRAD, stroke="#081C24", strokeWidth=3)

# --- lure glow: concentric veils around the esca (drawn early, under the fish) -------
for i, (r, op) in enumerate([(150, 6), (100, 10), (58, 15), (34, 22)]):
    d.shape("ellipse", f"Lure halo {i+1}", x=292 - r, y=262 - r, width=2 * r, height=2 * r,
            fill="#9FE8C4", opacity=op, stroke=NONE)

# --- tail: small rounded fan at the peduncle ------------------------------------------
d.path(smooth([(742, 442), (788, 428), (822, 444), (836, 474), (824, 500),
               (792, 508), (756, 494), (738, 470)]),
       "Tail fin", fill=FIN_GRAD, stroke=INK, strokeWidth=4)
for i, dd in enumerate(["M762,460 C782,452 800,450 818,456",
                        "M760,478 C780,476 800,478 818,486"]):
    d.path(dd, f"Tail ray {i+1}", fill=NONE, stroke="#4A6E7C", strokeWidth=3,
           opacity=45, cap="round")

# --- dorsal + anal soft fins: low ridges on the rear ------------------------------------
d.path(smooth([(600, 356), (646, 336), (690, 340), (716, 368), (692, 380), (644, 376)]),
       "Dorsal soft", fill=FIN_GRAD, stroke=INK, strokeWidth=4, opacity=90)
d.path(smooth([(612, 572), (660, 558), (700, 540), (716, 556), (700, 580), (656, 594)]),
       "Anal soft", fill=FIN_GRAD, stroke=INK, strokeWidth=4, opacity=90)

# --- body + gaping head: one silhouette -------------------------------------------------
# clockwise from snout tip: into the gape, around the lower jaw, belly, back, forehead
BODY = smooth([
    (296, 396),                       # snout tip (upper lip)
    (330, 442), (372, 484), (418, 524), (450, 548),   # mouth floor to hinge
    (398, 552), (336, 540), (278, 514),               # inside lower jaw to jaw tip
    (292, 552), (352, 582),                            # chin underside
    (470, 612), (590, 602), (690, 545), (748, 480),   # belly to peduncle
    (726, 428), (646, 378), (540, 342), (452, 322),   # back to crown
    (382, 340), (330, 366),                            # forehead down to snout
])
d.path(BODY, "Body", fill=BODY_GRAD, stroke=INK, strokeWidth=6)
# mouth interior: the gullet, dark wine
d.path("M300,404 C330,448 372,494 424,532 C390,544 336,538 288,514 "
       "C284,472 288,432 300,404 Z", "Gullet", fill=MOUTH_GRAD, stroke=NONE)
# lure light spilling onto the lip edges + throat
d.path("M300,400 C334,444 376,492 428,530", "Lip rim light", fill=NONE,
       stroke="#8FE0BC", strokeWidth=5, opacity=35, cap="round")
d.path("M296,514 C330,532 372,542 416,540", "Throat glow", fill=NONE,
       stroke="#7AD4AE", strokeWidth=4, opacity=25, cap="round")
# back rim: faint ambient from above
d.path("M420,330 C500,326 590,344 660,382", "Back rim", fill=NONE,
       stroke="#4A7E8C", strokeWidth=4, opacity=30, cap="round")
# lure light caught on the snout crown and forehead
d.path("M306,392 C334,362 374,344 414,336", "Forehead rim light", fill=NONE,
       stroke="#8FE0BC", strokeWidth=5, opacity=28, cap="round")

# --- fangs: pointed paths along the lip edges (no stroke -- thin would vanish) --------
def fang(bx, by, tip_x, tip_y, w, label, op=88):
    """Triangle tooth: base at (bx,by) width w across, tip at (tip_x,tip_y)."""
    ux, uy = tip_x - bx, tip_y - by
    ln = math.hypot(ux, uy) or 1
    nx, ny = -uy / ln * w / 2, ux / ln * w / 2
    d.path(f"M{bx - nx:.1f},{by - ny:.1f} L{tip_x:.1f},{tip_y:.1f} "
           f"L{bx + nx:.1f},{by + ny:.1f} Z", label,
           fill="#DCE6DA", opacity=op, stroke=NONE)


# upper jaw edge: snout -> gullet, teeth point down-inward
UPPER_LIP = [(302, 404, 16, 10), (322, 428, 20, 10), (344, 452, 24, 10),
             (366, 476, 20, 9), (388, 498, 17, 8), (410, 518, 13, 7)]
for i, (bx, by, L, w) in enumerate(UPPER_LIP):
    fang(bx, by, bx - 4 + 10 * (i / len(UPPER_LIP)), by + L, w, f"Upper fang {i+1}")
# two long sabers at the snout corner
fang(300, 402, 292, 438, 12, "Upper saber 1")
fang(314, 420, 310, 452, 10, "Upper saber 2")
# lower jaw edge: jaw tip -> hinge, teeth point up-inward
LOWER_LIP = [(284, 516, 26, 10), (312, 526, 22, 9), (344, 534, 20, 9),
             (376, 540, 16, 8), (410, 544, 12, 7)]
for i, (bx, by, L, w) in enumerate(LOWER_LIP):
    fang(bx, by, bx + 6 - 12 * (i / len(LOWER_LIP)), by - L, w, f"Lower fang {i+1}", op=80)
fang(282, 514, 272, 478, 11, "Lower saber")

# --- face detail ------------------------------------------------------------------------
# tiny dim eye high on the head, lure-light glint
d.shape("ellipse", "Eye", x=396, y=394, width=18, height=18, fill="#0A141C",
        stroke="#3A5E68", strokeWidth=3)
d.shape("ellipse", "Eye glint", x=400, y=397, width=5, height=5, fill="#BFF0D8", opacity=70, stroke=NONE)
# nostril pit + skin pores on the snout
d.shape("ellipse", "Nostril", x=316, y=384, width=8, height=10, fill="#0A141C", opacity=80, stroke=NONE)
for i, (x, y) in enumerate([(348, 372), (368, 386), (386, 360), (352, 402), (404, 424)]):
    d.shape("ellipse", f"Pore {i+1}", x=x, y=y, width=4, height=4, fill="#0A141C", opacity=70, stroke=NONE)
# skin flaps (cirri) trailing off the chin
for i, dd in enumerate(["M310,556 C300,576 296,592 300,606",
                        "M338,570 C332,588 332,602 340,614"]):
    d.path(dd, f"Cirrus {i+1}", fill=NONE, stroke="#1A2830", strokeWidth=5, cap="round")
# pectoral fin: small fan low on the flank
d.path(smooth([(500, 520), (540, 528), (566, 556), (556, 584), (524, 578), (500, 552)]),
       "Pectoral", fill=FIN_GRAD, stroke=INK, strokeWidth=4, opacity=85)

# --- illicium: the rod, then the esca (the lantern) ---------------------------------------
d.path("M382,344 C360,306 330,276 300,266", "Illicium", fill=NONE,
       stroke="#2E4E5A", strokeWidth=5, cap="round")
# esca: bright core + two filaments curling off the bulb
d.shape("ellipse", "Esca", x=280, y=250, width=24, height=24, fill=LURE,
        stroke="#8FE0BC", strokeWidth=3)
d.path("M288,254 C280,244 274,238 264,236", "Esca filament 1", fill=NONE,
       stroke="#BFF0D8", strokeWidth=4, opacity=80, cap="round")
d.path("M296,272 C302,280 310,284 320,284", "Esca filament 2", fill=NONE,
       stroke="#BFF0D8", strokeWidth=4, opacity=60, cap="round")
# hot center + tight halo over everything
d.shape("ellipse", "Esca core", x=286, y=256, width=12, height=12, fill="#FFFFFF", opacity=95, stroke=NONE)
d.shape("ellipse", "Esca bloom", x=276, y=246, width=32, height=32, fill="#C8F4D8", opacity=25, stroke=NONE)

# --- name -------------------------------------------------------------------------------
d.text("ANGLERFISH", "Name", x=500, y=962, size=58, font="Virelai Sans",
       color="#A8CCD4", justify="center")

d.finish("anglerfish-V1R00")
