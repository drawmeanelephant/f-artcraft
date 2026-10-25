#!/usr/bin/env python3
"""Obon — Festival Seal V1R00.

Toro nagashi: paper chochin lanterns set afloat on night water to guide the
ancestors home. One hero lantern low-centre, two smaller distant lights,
concentric ripples and a smeared amber reflection. Deep indigo field, warm
glow, a thin crescent moon. 1000x1000.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from orient.plate import (Plate, PCX, PCY, PR, NONE, INK, GOLD, GOLD_HI, PAPER,
                          LATIN, CJK, lin, rad, gold_lin, smooth, blend)
from festival_kit import (seal_disc, glow, dust, ring_dots, caption)

SLUG = "obon-V1R00"
SS3 = "Source Sans 3"

IND_HI = "#2A3A6E"
IND_LO = "#080D22"
WATER = "#17264E"
WATER_LO = "#0A1028"
RIPPLE = "#7A9AD0"
AMBER_HI = "#FFE4A8"
AMBER = "#F2A85C"
AMBER_LO = "#B85A2E"
WOOD = "#2E1E14"
MOON = "#F4ECD8"

p = Plate("Obon — Festival Seal", 1000, 1000)
d = p.d


def inside(x, y, pad=0, label=""):
    if math.hypot(x - PCX, y - PCY) > PR - pad:
        raise AssertionError(f"outside disc: {label} ({x:.0f},{y:.0f})")
    return (x, y)


# --- field ------------------------------------------------------------------
p.backdrop(top="#101832", bottom="#04060F", glow=("#2A3A6E", 14))
dust(d, n=44, r=404, colors=("#F6E3B8", "#9AB0E0"), seed=19,
     smin=0.8, smax=2.2, opmin=8, opmax=24, label="Backdrop dust")
seal_disc(p, IND_HI, IND_LO, rim="#C8A860", rim2="#2E3050")

# sky/water split: water is the disc's lower cap (arc clipped to the rim)
d.path("M87.7,540 A420,420 1 0 1 912.3,540 Z", "Water",
       fill=lin((0, 540), (0, 880), (0, WATER), (1, WATER_LO)), stroke=NONE)
# soft indigo mist at the horizon
glow(d, 500, 545, 400, "#4A5E9E", a=16, label="Horizon mist", squash=0.12)

# stars (upper half only, inside disc)
import random
rnd = random.Random(11)
for i in range(40):
    x = rnd.uniform(180, 820)
    y = rnd.uniform(110, 480)
    if math.hypot(x - PCX, y - PCY) > PR - 30:
        continue
    s = rnd.uniform(0.8, 2.6)
    d.shape("ellipse", f"Star {i+1}", x=x - s / 2, y=y - s / 2, width=s,
            height=s, fill="#DCE6F8", opacity=rnd.randint(18, 55),
            stroke=NONE)

# crescent moon, upper left
MX, MY, MR = 316, 240, 56
inside(MX - MR - 4, MY, 10, "moon")
d.shape("ellipse", "Moon glow", x=MX - MR * 1.7, y=MY - MR * 1.7,
        width=MR * 3.4, height=MR * 3.4,
        fill=rad((0, MOON, 22), (0.6, MOON, 6), (1, MOON, 0)), stroke=NONE)
d.shape("ellipse", "Moon", x=MX - MR, y=MY - MR, width=2 * MR, height=2 * MR,
        fill=rad((0, "#FFF8E4"), (0.7, MOON), (1, "#CDBE98")),
        stroke="#E8DCC0", strokeWidth=1.6)
# shadow disc takes a bite -> crescent
d.shape("ellipse", "Moon shadow", x=MX - MR + 20, y=MY - MR - 6,
        width=2 * MR, height=2 * MR, fill=IND_HI, stroke=NONE, opacity=94)

# faint ring guides + rim dots
for rr, op in ((176, 10), (268, 8), (346, 7)):
    d.shape("ellipse", f"Field ring {rr}", x=PCX - rr, y=PCY - rr,
            width=2 * rr, height=2 * rr, fill=NONE, stroke="#8AA0D8",
            strokeWidth=1.3, opacity=op)
ring_dots(d, r=398, n=56, size=2.4, color="#C8B078", opacity=30)

# --- water: horizon tick + wide still bands ----------------------------------
d.shape("line", "Horizon", x1=150, y1=540, x2=850, y2=540,
        stroke="#3E5490", strokeWidth=2.0, opacity=40, cap="round")
for i, (x, y, w) in enumerate([(300, 585, 130), (560, 612, 170),
                               (730, 572, 110), (280, 660, 120),
                               (640, 700, 190), (400, 756, 160),
                               (700, 792, 40), (310, 780, 70)]):
    d.path(f"M{x - w:.1f},{y:.1f} Q{x:.1f},{y - 6:.1f} {x + w:.1f},{y:.1f}",
           f"Swell {i+1}", fill=NONE, stroke="#3A4E88", strokeWidth=2.0,
           opacity=26, cap="round")


def ripple(cx, cy, n=4, r0=46, gap=26, squash=0.30, col=RIPPLE, op=40,
           label="Ripple"):
    for k in range(n):
        rr = r0 + gap * k
        d.shape("ellipse", f"{label} {k+1}", x=cx - rr, y=cy - rr * squash,
                width=rr * 2, height=rr * 2 * squash, fill=NONE,
                stroke=col, strokeWidth=1.8,
                opacity=max(8, op - k * 9))


def reflection(cx, y0, h, w, col=AMBER, label="Reflection"):
    """Smeared vertical light on water: jittered dashes fading downward."""
    nseg = 7
    for i in range(nseg):
        t = i / (nseg - 1)
        yy = y0 + t * h
        seg = 14 + 26 * (1 - t)
        dx = math.sin(i * 2.3) * w * 0.35 * (0.4 + t)
        d.path(f"M{cx + dx - seg/2:.1f},{yy:.1f} Q{cx + dx:.1f},{yy - 2:.1f} "
               f"{cx + dx + seg/2:.1f},{yy:.1f}", f"{label} {i+1}",
               fill=NONE, stroke=col, strokeWidth=5.5 - t * 3.2,
               opacity=int(30 * (1 - t) + 8), cap="round")


def chochin(cx, cy, w, h, label, bright=1.0):
    """Floating paper lantern: ribbed warm body on a dark wooden base."""
    a, b = w / 2, h / 2
    # halo on the water + around the paper
    glow(d, cx, cy, w * 1.35, AMBER, a=int(30 * bright), label=f"{label} halo")
    # ribbed paper body — near-straight sides, domed top, flat base
    d.path(f"M{cx - a:.1f},{cy + b * 0.48:.1f} "
           f"C{cx - a * 1.02:.1f},{cy + b * 0.08:.1f} "
           f"{cx - a * 0.94:.1f},{cy - b * 0.52:.1f} "
           f"{cx - a * 0.64:.1f},{cy - b * 0.84:.1f} "
           f"C{cx - a * 0.4:.1f},{cy - b * 1.0:.1f} "
           f"{cx + a * 0.4:.1f},{cy - b * 1.0:.1f} "
           f"{cx + a * 0.64:.1f},{cy - b * 0.84:.1f} "
           f"C{cx + a * 0.94:.1f},{cy - b * 0.52:.1f} "
           f"{cx + a * 1.02:.1f},{cy + b * 0.08:.1f} "
           f"{cx + a:.1f},{cy + b * 0.48:.1f} Z", label,
           fill=lin((cx, cy - b), (cx, cy + b * 0.6),
                    (0, "#FFE9BC"), (0.42, AMBER_HI), (0.78, AMBER),
                    (1, AMBER_LO)),
           stroke=INK, strokeWidth=3.2)
    # bamboo ribs: horizontal arcs sagging with the paper curve
    for k, rt in enumerate((-0.72, -0.44, -0.16, 0.14, 0.42)):
        yy = cy + rt * b * 0.9
        half = a * math.sqrt(max(0.05, 1 - (rt * 0.92) ** 2))
        d.path(f"M{cx - half:.1f},{yy:.1f} Q{cx:.1f},{yy + 5:.1f} "
               f"{cx + half:.1f},{yy:.1f}", f"{label} rib {k+1}",
               fill=NONE, stroke="#8A4A24", strokeWidth=1.5, opacity=45,
               cap="round")
    # vertical seams at the sides
    for k in (-0.55, 0.55):
        x = cx + k * a
        d.path(f"M{x:.1f},{cy - b * 0.82:.1f} Q{x + k * 6:.1f},{cy:.1f} "
               f"{x:.1f},{cy + b * 0.5:.1f}", f"{label} seam {k}",
               fill=NONE, stroke="#9A5A2E", strokeWidth=1.3, opacity=34,
               cap="round")
    # paper sheen
    d.shape("ellipse", f"{label} sheen", x=cx - a * 0.62, y=cy - b * 0.72,
            width=a * 0.5, height=b * 0.9,
            fill=rad((0, "#FFFBE8", 34), (1, "#FFFBE8", 0)), stroke=NONE)
    # dark wooden top ring + finial
    d.shape("ellipse", f"{label} cap", x=cx - a * 0.42, y=cy - b - 8,
            width=a * 0.84, height=16,
            fill=lin((0, cy - b - 8), (0, cy - b + 8), (0, "#5E4630"),
                     (1, WOOD)), stroke=INK, strokeWidth=1.8)
    # wooden float base the lantern rests on, overlapping the paper's edge
    d.shape("ellipse", f"{label} base", x=cx - a * 0.72, y=cy + b * 0.44,
            width=a * 1.44, height=17,
            fill=lin((0, cy + b * 0.44), (0, cy + b * 0.78),
                     (0, "#5E4630"), (1, "#1E1208")),
            stroke=INK, strokeWidth=2.0)
    d.shape("ellipse", f"{label} foot", x=cx - a * 0.4, y=cy + b * 0.53,
            width=a * 0.8, height=11, fill="#241812", stroke=NONE)


# --- hero lantern + water play ------------------------------------------------
HX_, HY_, HW, HH = 500, 470, 176, 208
inside(HX_ - HW / 2, HY_, 16, "lantern L")
inside(HX_ + HW / 2, HY_, 16, "lantern R")
inside(HX_, HY_ - HH / 2, 16, "lantern T")

# ripples + reflection first so the lantern sits on top of the water line
reflection(HX_, 596, 150, 60, label="Hero reflection")
ripple(HX_, 586, n=5, r0=96, gap=34, squash=0.26, op=44, label="Hero ripple")
# faint wide swell rings around the hero
ripple(HX_, 590, n=3, r0=200, gap=52, squash=0.20, col="#5A7AB8", op=20,
       label="Wide ripple")

# distant lanterns, dimmer, sitting near the horizon
chochin(264, 548, 74, 92, "Lantern L", bright=0.55)
ripple(264, 606, n=3, r0=42, gap=20, squash=0.28, op=30, label="Ripple L")
reflection(264, 612, 62, 22, label="Reflection L")
chochin(742, 570, 60, 76, "Lantern R", bright=0.5)
ripple(742, 616, n=3, r0=36, gap=17, squash=0.28, op=26, label="Ripple R")
reflection(742, 622, 52, 18, label="Reflection R")
# one far lantern near the horizon, base almost touching it
chochin(640, 512, 34, 44, "Lantern far", bright=0.4)
reflection(640, 542, 24, 10, label="Reflection far")

chochin(HX_, HY_, HW, HH, "Hero lantern")
# hero is half-sunk: its waterline is the base ellipse; ripple lips at sides
for sgn in (-1, 1):
    d.path(f"M{HX_ + sgn * HW * 0.52:.1f},{HY_ + HH * 0.40:.1f} "
           f"Q{HX_ + sgn * (HW * 0.52 + 20):.1f},{HY_ + HH * 0.36:.1f} "
           f"{HX_ + sgn * (HW * 0.52 + 42):.1f},{HY_ + HH * 0.42:.1f}",
           f"Hero waterline {sgn}", fill=NONE, stroke="#9AB6E8",
           strokeWidth=2.2, opacity=42, cap="round")

# drifting fireflies / stray sparks above the water
for i, (x, y, s) in enumerate([(220, 430, 2.6), (352, 372, 2.0),
                               (664, 340, 2.4), (762, 452, 2.8),
                               (600, 396, 1.8), (436, 336, 2.2)]):
    glow(d, x, y, 10, "#FFD98A", a=36, label=f"Spark glow {i+1}")
    d.shape("ellipse", f"Spark {i+1}", x=x - s, y=y - s, width=s * 2,
            height=s * 2, fill="#FFF2C4", opacity=80, stroke=NONE)

# --- seal chop + caption ------------------------------------------------------
CHX, CHY, CHW, CHH = 878, 96, 56, 116
d.shape("rectangle", "Chop shadow", x=CHX + 3, y=CHY + 4, width=CHW,
        height=CHH, radius=4, fill="#000000", opacity=30, stroke=NONE)
p.chop("盆", x=CHX, y=CHY, w=CHW, h=CHH, size=30)

caption(p, "OBON", "お盆 · AUG 13–16 · LANTERNS ON THE WATER",
        name_color="#EDE6D4", sub_color="#B8AC88",
        name_size=54, tracking_name=140, sub_size=20, tracking_sub=60,
        sub_font=CJK)
p.finish(SLUG)
