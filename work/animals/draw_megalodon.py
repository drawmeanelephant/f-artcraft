#!/usr/bin/env python3
"""Megalodon — field-guide plate V1R00. Abyss plate: the plate itself is the
deep water — a gradient that darkens toward the bottom, marine snow drifting,
faint god rays dying into the murk. The shark rises through it in profile,
countershaded, mouth open on rows of broad triangular teeth. Below, on a
sliver of sea floor, one fossil tooth the size of a hand for scale. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Megalodon — Field Plate", 1000, 1000)
rng = random.Random(3)

INK = "#0E1A20"

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

BG_GRAD = lin(0, 0, 0, 1000, (0, "#04090E"), (1, "#010304"))
# abyss: dim teal light at the top dying to pressure-dark at the bottom
PLATE_GRAD = {"gradient": {"kind": "linear", "start": [500, 40], "end": [500, 880],
    "stops": [{"offset": 0, "color": "#3E5E70"}, {"offset": 0.45, "color": "#1E3442"},
              {"offset": 1, "color": "#0A141C"}]}}
BODY_GRAD = lin(300, 280, 400, 620, (0, "#7A96A4"), (0.5, "#3C5564"), (1, "#1A2832"))
BELLY = "#C6D6DC"
MOUTH = "#200A0E"
IVORY = lin(0, 380, 0, 480, (0, "#F2EFE2"), (1, "#B8B49E"))
TOOTH_GRAD = lin(0, 660, 0, 800, (0, "#D8D2C0"), (1, "#8E887A"))
SED_GRAD = lin(0, 740, 0, 880, (0, "#2E3E44"), (1, "#101A1E"))

PCX, PCY, PR = 500, 460, 420

def on_disc(x, y, pad):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

def tooth_path(x, y, w, h, label, **kw):
    return d.path(f"M{x},{y} L{x+w*0.55},{y+h} L{x+w},{y} Z", label, **kw)

# --- backdrop + abyssal plate -----------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#3E5E70", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#29434F", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#8FB2BE", strokeWidth=3, opacity=30)

# god rays dying into the murk — tops seated just inside the disc's own curve
def disc_top(x):
    return PCY - math.sqrt(max(0.0, PR * PR - (x - PCX) ** 2))
for i, (x0, w, op) in enumerate([(300, 60, 7), (470, 90, 9), (640, 55, 6)]):
    y0 = disc_top(x0) + 14
    y1 = disc_top(x0 + w) + 14
    d.path(f"M{x0},{y0:.0f} L{x0+w},{y1:.0f} L{x0+w+60},560 L{x0+40},560 Z",
           f"God ray {i+1}", fill="#BFE0EA", opacity=op, stroke=NONE)

# marine snow: pale motes through the water column
for i in range(42):
    x = rng.uniform(140, 860)
    y = rng.uniform(90, 840)
    if not on_disc(x, y, 30):
        continue
    w = rng.uniform(2.5, 6)
    d.shape("ellipse", f"Snow {i+1}", x=x, y=y, width=w, height=w,
            fill="#C8E2EA", opacity=rng.randint(18, 55), stroke=NONE)

# --- sea floor sliver, closing on the disc's own arc ---------------------------------------
d.path("M240,762 C400,748 600,748 760,762 A420,420 0 0 1 240,762 Z",
       "Sea floor", fill=SED_GRAD, stroke="#1E3238", strokeWidth=4)
assert on_disc(240, 762, 4) and on_disc(760, 762, 4)

# --- the fossil tooth: hand-sized, for scale -----------------------------------------------
d.path("M300,768 C292,730 296,696 316,672 C322,664 330,664 336,672 "
       "C356,696 360,730 352,768 C344,776 332,780 326,780 "
       "C320,780 308,776 300,768 Z",
       "Fossil tooth", fill=TOOTH_GRAD, stroke=INK, strokeWidth=4)
# root lobes at the base
d.path("M294,764 C288,774 288,784 296,790 C310,798 342,798 356,790 "
       "C364,784 364,774 358,764 C352,772 342,776 326,776 "
       "C310,776 300,772 294,764 Z",
       "Tooth root", fill="#6E6858", stroke=INK, strokeWidth=3)
# serration ticks along both cutting edges
for i, t in enumerate([0.2, 0.38, 0.56, 0.74, 0.9]):
    y = 760 - t * 84
    xl = 296 + t * 18 + 4
    xr = 356 - t * 18 - 4
    d.path(f"M{xl:.0f},{y:.0f} l-5,-3", f"Serr L{i+1}", fill=NONE,
           stroke="#5E584A", strokeWidth=2, cap="round")
    d.path(f"M{xr:.0f},{y:.0f} l5,-3", f"Serr R{i+1}", fill=NONE,
           stroke="#5E584A", strokeWidth=2, cap="round")
# enamel light
d.path("M312,742 C310,714 314,692 326,676", "Tooth light", fill=NONE,
       stroke="#F4F0E0", strokeWidth=3, opacity=55, cap="round")

# === the shark ==============================================================================
# --- tail fin: the forked scythe at the far right ---------------------------------------------
d.path("M688,420 C722,370 762,332 806,300 C800,342 796,380 794,412 "
       "C798,452 800,492 790,530 C766,500 734,478 700,464 "
       "C692,450 688,434 688,420 Z",
       "Tail fin", fill=BODY_GRAD, stroke=INK, strokeWidth=6)

# --- body: the great torpedo, mouth open -------------------------------------------------------
d.path("M196,356 "
       "C240,320 320,296 420,296 "        # snout top over the head to the back
       "C520,296 620,330 676,384 "        # back sweeping to the peduncle
       "C700,410 706,442 700,470 "        # peduncle narrowing
       "C672,500 620,528 560,544 "        # rear underside
       "C480,564 390,560 330,536 "        # belly forward
       "C300,524 280,508 270,490 "        # throat to the jaw corner
       "C240,470 212,430 200,392 "        # chin back up the open gape edge
       "C196,378 194,366 196,356 Z",      # back to the snout tip
       "Body", fill=BODY_GRAD, stroke=INK, strokeWidth=6)

# countershade: pale belly wedge
d.path("M300,520 C360,542 470,550 560,536 C610,528 660,506 690,482 "
       "C660,516 590,544 510,554 C440,562 360,552 316,532 "
       "C306,528 300,524 300,520 Z",
       "Belly", fill=BELLY, opacity=55, stroke=NONE)
# the waterline between dark flank and pale belly
d.path("M268,500 C330,530 440,548 550,538 C610,530 660,508 692,486",
       "Countershade line", fill=NONE, stroke="#8FA8B4",
       strokeWidth=4, opacity=35, cap="round")
# dorsal rim light — the only light here comes from above
d.path("M210,352 C260,318 340,298 430,298 C520,298 610,326 668,376",
       "Rim light", fill=NONE, stroke="#C4E4EC", strokeWidth=5,
       opacity=55, cap="round")
# flank shading + faint lateral line
d.shape("ellipse", "Flank shade", x=430, y=390, width=270, height=100,
        fill="#081118", opacity=20, stroke=NONE)
d.path("M260,430 C360,452 520,460 660,452", "Lateral line", fill=NONE,
       stroke="#8FA8B4", strokeWidth=3, opacity=30, cap="round")

# --- dorsal fin: the sail on the back ---------------------------------------------------------
d.path("M430,300 C452,262 486,238 522,234 C528,264 526,296 516,326 "
       "C490,318 460,308 430,300 Z",
       "Dorsal fin", fill=BODY_GRAD, stroke=INK, strokeWidth=5)
d.path("M440,296 C458,268 484,248 510,240", "Dorsal light", fill=NONE,
       stroke="#C4E4EC", strokeWidth=3, opacity=45, cap="round")

# --- second dorsal + anal fin dots by the tail --------------------------------------------------
d.path("M640,348 C654,334 668,328 678,330 C676,344 668,356 656,362 Z",
       "Second dorsal", fill="#3C5564", stroke=INK, strokeWidth=3)
d.path("M600,516 C614,524 624,534 626,544 C612,542 600,534 592,524 Z",
       "Anal fin", fill="#3C5564", stroke=INK, strokeWidth=3)

# --- pectoral fin: the down-swept wing ---------------------------------------------------------
d.path("M356,492 C346,540 322,584 288,612 C278,620 268,616 268,604 "
       "C274,562 296,522 330,496 C340,488 352,486 356,492 Z",
       "Pectoral fin", fill=lin(330, 490, 290, 615, (0, "#4A6472"), (1, "#24343E")),
       stroke=INK, strokeWidth=5)
d.path("M340,510 C326,548 306,580 284,602", "Fin crease", fill=NONE,
       stroke="#16232C", strokeWidth=3, opacity=50, cap="round")

# --- gill slits --------------------------------------------------------------------------------
for i, x in enumerate([296, 310, 324]):
    d.path(f"M{x},{440} C{x-4},{452} {x-4},{464} {x},{476}",
           f"Gill {i+1}", fill=NONE, stroke="#0E1C24",
           strokeWidth=4, opacity=70, cap="round")

# --- head: open jaws, rows of teeth --------------------------------------------------------------
# mouth interior — the dark wedge of the gape
d.path("M198,362 C210,390 232,420 262,442 C276,452 292,456 304,452 "
       "C298,442 292,432 288,420 C262,404 232,384 210,362 "
       "C205,358 200,358 198,362 Z",
       "Mouth", fill=MOUTH, stroke=NONE)
# lower jaw edge accent
d.path("M268,488 C240,470 214,434 202,398", "Jaw edge", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
# tooth rows: broad triangles on both jaws
for i, (x, y, w, h) in enumerate([(216,376,13,15),(234,392,12,14),(252,406,12,14),
                                  (270,420,11,13),(286,432,10,12)]):
    tooth_path(x, y, w, h, f"Tooth U{i+1}", fill=IVORY, stroke=INK, strokeWidth=1.5)
for i, (x, y, w, h) in enumerate([(224,442,11,13),(242,456,11,13),(260,466,10,12),
                                  (278,474,9,11)]):
    tooth_path(x, y, w, -h, f"Tooth L{i+1}", fill=IVORY, stroke=INK, strokeWidth=1.5)
# nostril + eye: small, hard, alive
d.shape("ellipse", "Nostril", x=214, y=368, width=10, height=7,
        fill="#0A1418", opacity=80, stroke=NONE)
d.shape("ellipse", "Eye", x=268, y=372, width=18, height=17,
        fill="#060C10", stroke=INK, strokeWidth=2)
d.shape("ellipse", "Eye glint", x=272, y=375, width=5, height=5,
        fill="#D8F0F6", opacity=80, stroke=NONE)
# brow shadow over the eye
d.path("M258,364 C270,358 286,360 296,368", "Brow shadow", fill=NONE,
       stroke="#0E1C24", strokeWidth=4, opacity=60, cap="round")

# plate rim on top so everything inside closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840, fill=NONE,
        stroke="#06121A", strokeWidth=6)

# --- name ----------------------------------------------------------------------------------------
d.text("MEGALODON", "Name", x=500, y=962, size=58, font="Virelai Sans",
       color="#BCD6DE", justify="center")

d.finish("megalodon-V1R00")
