#!/usr/bin/env python3
"""Quoll — field plate V1R00. Head/bust portrait, face-on: the stuffed-toy
face of a spotted marsupial — big rounded ears, bright dark eyes, a pointed
muzzle with a pink-brown nose — over dusk-brown fur scattered with rust
spots. Warm tan plate on a dusk-indigo backdrop. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Quoll — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#3A2420"   # deep umber, not black


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
    (lx, ly), (rx, ry) = contour[0], contour[-1]
    for x, y in (contour[0], contour[-1]):
        assert abs(math.hypot(x - PCX, y - PCY) - PR) < 1.5, (x, y)
    return smooth(contour, closed=False) + f" A420,420 0 0 1 {lx:.1f},{ly:.1f} Z"


BG_GRAD = lin("#241A28", "#0A060E", [0, 0], [0, 1000])
PLATE_GRAD = rad("#E8CEA4", "#C29A68", "#7A5436")
FUR_GRAD = rad("#C08A5E", "#94603C", "#5A3624")
EAR_GRAD = lin("#A8764C", "#6E452C", [500, 190], [500, 400])
BUST_GRAD = lin("#A87A50", "#5E3A26", [500, 660], [500, 880])

# --- backdrop + plate -----------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876, fill="#E8CEA4", opacity=6, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#4E3320", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F4E4C4", strokeWidth=3, opacity=50)
# plate patina: soft blotches + speckles, all inside the rim
d.shape("ellipse", "Patina 1", x=175, y=195, width=240, height=150, fill="#9A7248", opacity=20, stroke=NONE)
d.shape("ellipse", "Patina 2", x=590, y=620, width=265, height=155, fill="#9A7248", opacity=18, stroke=NONE)
for i, (x, y, w) in enumerate([(210, 300, 8), (760, 250, 7), (180, 560, 9), (810, 560, 8), (260, 745, 7),
                               (730, 745, 9), (140, 420, 6), (860, 410, 7), (410, 130, 7), (590, 120, 8),
                               (370, 810, 6), (640, 815, 7)]):
    assert on_disc(x + w / 2, y + w / 2, 4), i
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w, fill="#7C5A38", opacity=38, stroke=NONE)

# --- bust / shoulders, closing on the disc arc -------------------------------------
y0 = 766
SH = [(disc_x(y0, -1), y0), (168, 740), (225, 706), (305, 682), (400, 672), (500, 676)]
SH = SH + [(2 * PCX - x, y) for x, y in reversed(SH[:-1])]
d.path(arc_closed(SH), "Shoulders", fill=BUST_GRAD, stroke=INK, strokeWidth=6)
# chest light + under-head shadow
d.shape("ellipse", "Chest light", x=415, y=760, width=170, height=95, fill="#DDB98A", opacity=35, stroke=NONE)
d.shape("ellipse", "Under-head shadow", x=360, y=668, width=280, height=64, fill="#452A1A", opacity=32, stroke=NONE)
# the felon's spots: rust over the dusk-brown chest, a few cream ones mixed in
SPOTS_RUST = [(300, 752, 26, 20), (380, 718, 20, 16), (468, 742, 24, 18), (560, 716, 22, 16),
              (648, 748, 26, 20), (712, 782, 20, 16), (268, 786, 22, 17), (352, 792, 18, 14),
              (455, 806, 26, 19), (548, 788, 20, 15), (640, 812, 23, 17), (722, 794, 18, 14),
              (318, 820, 20, 14), (420, 852, 24, 16), (560, 848, 22, 15), (672, 826, 20, 14)]
SPOTS_CREAM = [(340, 758, 15, 12), (520, 730, 14, 11), (610, 770, 15, 12), (300, 806, 14, 11),
               (490, 830, 15, 11), (600, 836, 14, 10), (730, 752, 13, 10)]
for i, (x, y, w, h) in enumerate(SPOTS_RUST):
    assert on_disc(x, y, 6), i
    d.shape("ellipse", f"Rust spot {i+1}", x=x - w / 2, y=y - h / 2, width=w, height=h,
            fill="#C4703C", opacity=75, stroke=NONE)
for i, (x, y, w, h) in enumerate(SPOTS_CREAM):
    assert on_disc(x, y, 6), i
    d.shape("ellipse", f"Cream spot {i+1}", x=x - w / 2, y=y - h / 2, width=w, height=h,
            fill="#EAD8B8", opacity=70, stroke=NONE)

# --- ears: big, rounded, thin-edged ------------------------------------------------
d.path(smooth([(352, 208), (418, 226), (444, 296), (428, 368), (372, 398),
               (316, 372), (296, 300), (312, 238)]), "Ear L",
       fill=EAR_GRAD, stroke=INK, strokeWidth=7)
d.path(smooth([(648, 208), (582, 226), (556, 296), (572, 368), (628, 398),
               (684, 372), (704, 300), (688, 238)]), "Ear R",
       fill=EAR_GRAD, stroke=INK, strokeWidth=7)
d.path(smooth([(356, 252), (398, 268), (414, 314), (402, 360), (366, 376),
               (334, 354), (322, 308), (334, 270)]), "Inner ear L",
       fill="#5E3524", opacity=85, stroke=NONE)
d.path(smooth([(644, 252), (602, 268), (586, 314), (598, 360), (634, 376),
               (666, 354), (678, 308), (666, 270)]), "Inner ear R",
       fill="#5E3524", opacity=85, stroke=NONE)
d.path("M316,268 C324,240 342,222 366,214", "Ear rim light L", fill=NONE,
       stroke="#EBCFA2", strokeWidth=6, opacity=55, cap="round")
d.path("M684,268 C676,240 658,222 634,214", "Ear rim light R", fill=NONE,
       stroke="#EBCFA2", strokeWidth=6, opacity=55, cap="round")

# --- head: broad cheeks tapering to the pointed marsupial muzzle --------------------
d.path(smooth([(500, 306), (612, 318), (694, 396), (716, 500), (688, 596),
               (620, 668), (548, 706), (500, 718), (452, 706), (380, 668),
               (312, 596), (284, 500), (306, 396), (388, 318)]),
       "Head", fill=FUR_GRAD, stroke=INK, strokeWidth=8)
# cheek fur flicks on the silhouette
d.path("M288,528 L268,538 L290,550 L272,562 L294,572", "Fur flick L",
       fill=NONE, stroke=INK, strokeWidth=6, cap="round")
d.path("M712,528 L732,538 L710,550 L728,562 L706,572", "Fur flick R",
       fill=NONE, stroke=INK, strokeWidth=6, cap="round")
# top highlight + shading
d.shape("ellipse", "Head highlight", x=385, y=330, width=230, height=80, fill="#FFFFFF", opacity=13, stroke=NONE)
d.shape("ellipse", "Cheek shade L", x=300, y=560, width=70, height=50, fill="#6E4228", opacity=30, stroke=NONE)
d.shape("ellipse", "Cheek shade R", x=630, y=560, width=70, height=50, fill="#6E4228", opacity=30, stroke=NONE)
# pale muzzle blaze running to the nose
d.path(smooth([(500, 470), (560, 500), (584, 566), (560, 648), (500, 688),
               (440, 648), (416, 566), (440, 500)]),
       "Muzzle blaze", fill="#E4C8A2", opacity=55, stroke=NONE)
# forehead fur strokes
for lbl, dd in [("Forehead fur 1", "M464,352 C470,338 480,328 492,322"),
                ("Forehead fur 2", "M510,322 C522,328 532,338 538,352"),
                ("Forehead fur 3", "M488,336 C496,328 508,328 516,336")]:
    d.path(dd, lbl, fill=NONE, stroke="#6E4228", strokeWidth=5, opacity=45, cap="round")

# --- face ---------------------------------------------------------------------------
# eyes: dark, round, a little manic
d.shape("ellipse", "Eye L", x=384, y=468, width=50, height=56, fill="#241410", stroke=NONE)
d.shape("ellipse", "Eye R", x=566, y=468, width=50, height=56, fill="#241410", stroke=NONE)
d.shape("ellipse", "Glint L", x=397, y=479, width=11, height=11, fill="#FFFFFF", opacity=92, stroke=NONE)
d.shape("ellipse", "Glint R", x=579, y=479, width=11, height=11, fill="#FFFFFF", opacity=92, stroke=NONE)
d.shape("ellipse", "Glint L2", x=414, y=500, width=5, height=5, fill="#FFFFFF", opacity=60, stroke=NONE)
d.shape("ellipse", "Glint R2", x=596, y=500, width=5, height=5, fill="#FFFFFF", opacity=60, stroke=NONE)
# brow light arcs
d.path("M378,452 C398,438 426,436 448,446", "Brow light L", fill=NONE,
       stroke="#EBCFA2", strokeWidth=6, opacity=55, cap="round")
d.path("M552,446 C574,436 602,438 622,452", "Brow light R", fill=NONE,
       stroke="#EBCFA2", strokeWidth=6, opacity=55, cap="round")
# nose: pink-brown, pointed, moist
d.path("M468,618 C468,600 484,590 500,590 C516,590 532,600 532,618 "
       "C532,634 518,646 500,646 C482,646 468,634 468,618 Z",
       "Nose", fill="#8A4A3E", stroke=INK, strokeWidth=4)
d.path("M478,606 C486,598 498,596 508,600", "Nose glint", fill=NONE,
       stroke="#FFFFFF", strokeWidth=4, opacity=45, cap="round")
d.path("M500,646 L500,666", "Philtrum", fill=NONE, stroke=INK, strokeWidth=5, opacity=70, cap="round")
# small mouth: the felon's smirk
d.path("M440,662 C462,684 482,692 500,692 C518,692 538,684 560,662",
       "Mouth", fill=NONE, stroke=INK, strokeWidth=7, cap="round")
# whisker dots + whiskers
for i, (x, y) in enumerate([(440, 628), (452, 644), (436, 610)]):
    d.shape("ellipse", f"Whisker dot L{i+1}", x=x, y=y, width=5, height=5, fill=INK, opacity=50, stroke=NONE)
for i, (x, y) in enumerate([(560, 628), (548, 644), (564, 610)]):
    d.shape("ellipse", f"Whisker dot R{i+1}", x=x, y=y, width=5, height=5, fill=INK, opacity=50, stroke=NONE)
for lbl, dd in [("Whisker L1", "M448,616 L388,600"), ("Whisker L2", "M450,636 L392,640"),
                ("Whisker L3", "M446,600 L398,574"), ("Whisker R1", "M552,616 L612,600"),
                ("Whisker R2", "M550,636 L608,640"), ("Whisker R3", "M554,600 L602,574")]:
    d.path(dd, lbl, fill=NONE, stroke=INK, strokeWidth=4, opacity=45, cap="round")

# --- name ----------------------------------------------------------------------------
d.text("QUOLL", "Name", x=500, y=962, size=60, font="Virelai Sans",
       color="#F0DCB8", justify="center")

d.finish("quoll-V1R00")
