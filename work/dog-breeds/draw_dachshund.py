#!/usr/bin/env python3
"""Dachshund — milestone card V1R00. The unmistakable long-low silhouette
in profile: deep keel chest, short legs, long drop ears, smooth red coat,
head carried high like it doesn't know it's funny. Tail a level saber off
the topline. Forest-floor browns: leaf litter on a floor that closes on
the disc's own arc. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Dachshund — Milestone Card", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#241812"                    # warm dark ink, never pure black


def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}


def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}


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


def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad


def rim_x(y, side=-1):
    return PCX + side * math.sqrt(PR * PR - (y - PCY) ** 2)


def find(o, oid):
    if isinstance(o, dict):
        if o.get("id") == oid and "bounds" in o: return o
        o = list(o.values())
    if isinstance(o, list):
        for v in o:
            hit = find(v, oid)
            if hit: return hit


BG_GRAD = lin(0, 0, 0, 1000, (0, "#191410"), (1, "#090604"))
PLATE_GRAD = rad((0, "#C2A878"), (0.55, "#8A6F4B"), (1, "#4C3B26"))
COAT_GRAD = lin(300, 480, 700, 800, (0, "#B26034"), (0.5, "#874322"), (1, "#4E2413"))
DIM_GRAD = lin(300, 480, 700, 800, (0, "#7E4122"), (1, "#381A0E"))
FLOOR_GRAD = lin(0, 750, 0, 880, (0, "#6B5A3C"), (0.55, "#4A3D26"), (1, "#26200F"))

# --- backdrop + forest plate ---------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#3E3220", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E4D9B4", strokeWidth=3, opacity=38)

# low amber light pooling upper-left, sun through canopy
d.shape("ellipse", "Light pool", x=250, y=150, width=400, height=230,
        fill="#F0DCA4", opacity=14, stroke=NONE)
# drifting mist lenses
for i, (x, y, w) in enumerate([(330, 320, 90), (570, 240, 70), (710, 360, 80),
                               (250, 470, 60), (750, 490, 64), (460, 190, 55)]):
    assert on_disc(x, y, 20), i
    d.shape("ellipse", f"Mist {i+1}", x=x - w / 2, y=y - w / 5, width=w, height=w * 0.4,
            fill="#EAE2BC", opacity=11, stroke=NONE)

# --- leaf-litter floor, closing on the disc arc --------------------------------
fy = 795
fl, fr = rim_x(fy, -1), rim_x(fy, 1)
d.path(f"M{fl:.1f},{fy} C300,782 400,806 500,795 C600,784 700,790 {fr:.1f},{fy} "
       f"A{PR},{PR} 0 0 1 {fl:.1f},{fy} Z", "Floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{fl + 8:.0f},{fy} C300,782 400,806 500,795 C600,784 700,790 {fr - 8:.0f},{fy}",
       "Floor crest", fill=NONE, stroke="#A08C58", strokeWidth=5, opacity=42, cap="round")
# fallen leaves — little pointed ovals lying along the crest
for i, (x, y, w, rot, c) in enumerate([(320, 812, 26, -20, "#8C5A2E"), (415, 834, 22, 15, "#A06A34"),
                                       (540, 840, 26, -10, "#7C4E28"), (640, 828, 22, 25, "#96622F"),
                                       (690, 806, 20, -30, "#8C5A2E")]):
    assert on_disc(x, y, 14), i
    d.path(f"M{x},{y} C{x + w * 0.4},{y - w * 0.55} {x + w},{y - w * 0.2} {x + w * 1.1},{y} "
           f"C{x + w},{y + w * 0.3} {x + w * 0.4},{y + w * 0.4} {x},{y} Z",
           f"Leaf {i+1}", fill=c, opacity=60, stroke=NONE)
    d.path(f"M{x + 3},{y} L{x + w * 1.0},{y}", f"Leaf vein {i+1}", fill=NONE,
           stroke="#4A3018", strokeWidth=3, opacity=50, cap="round")
# one small mushroom at the right, forest-floor signature
d.path("M712,786 C712,776 716,770 722,770 C728,770 732,776 732,786 Z",
       "Mushroom stem", fill="#D8C8A4", opacity=70, stroke=NONE)
d.path("M700,772 C704,758 740,758 744,772 C732,778 712,778 700,772 Z",
       "Mushroom cap", fill="#9A5A30", opacity=75, stroke=NONE)

# soft shadow under the long body
d.shape("ellipse", "Dog shadow", x=290, y=762, width=440, height=30,
        fill="#140F06", opacity=32, stroke=NONE)

# --- the dachshund, proud profile facing left -----------------------------------
# tail — level saber carried off the topline, tapering, tip just lifting
d.path(smooth([(676, 622), (712, 606), (742, 586), (762, 562), (768, 540),
               (758, 532), (742, 548), (718, 576), (692, 600), (672, 610)]),
       "Tail", fill=lin(680, 620, 765, 535, (0, "#7E4122"), (0.7, "#4E2413"), (1, "#6E3A20")),
       stroke=INK, strokeWidth=5)
d.path("M712,600 C736,580 754,556 760,540", "Tail sheen", fill=NONE,
       stroke="#C07B4A", strokeWidth=4, opacity=45, cap="round")

# hind legs — short, one hard bend at the hock, feet on the floor
d.path(smooth([(596, 660), (606, 700), (610, 740), (600, 764), (576, 776),
               (560, 790), (566, 800), (594, 798), (620, 780), (632, 750),
               (630, 710), (620, 678)]),
       "Hind leg far", fill=DIM_GRAD, stroke=INK, strokeWidth=4.5)
d.path(smooth([(636, 656), (652, 698), (656, 738), (646, 762), (622, 774),
               (604, 788), (610, 800), (640, 798), (668, 780), (680, 748),
               (676, 706), (662, 674)]),
       "Hind leg near", fill=COAT_GRAD, stroke=INK, strokeWidth=5)
# hind paw pair — compact, pointing forward
d.path("M596,782 C584,788 578,796 584,802 C596,806 616,804 626,796 "
       "C626,786 610,780 596,782 Z", "Hind paw near", fill=COAT_GRAD,
       stroke=INK, strokeWidth=4)

# body — the long low barrel: level topline, deep keel, slight tuck-up
d.path(smooth([(356, 588), (330, 620), (322, 664), (336, 706), (372, 730),
               (440, 740), (540, 736), (620, 722), (668, 700), (690, 662),
               (686, 626), (648, 610), (560, 600), (460, 594), (390, 588)]),
       "Body", fill=COAT_GRAD, stroke=INK, strokeWidth=6)
# topline sheen — one long band of light down the back
d.path("M380,592 C460,584 560,588 650,606 C560,596 460,592 380,600 Z",
       "Back sheen", fill="#D8955C", opacity=35, stroke=NONE)
# belly shading under the barrel
d.path("M380,724 C460,736 560,734 640,712 C570,740 450,744 386,734 Z",
       "Belly shade", fill="#3A1C0E", opacity=45, stroke=NONE)

# front legs — short straight columns, deep chest behind them
d.path(smooth([(368, 680), (360, 716), (352, 748), (340, 768), (330, 782),
               (336, 794), (362, 794), (380, 780), (392, 748), (398, 712)]),
       "Front leg far", fill=DIM_GRAD, stroke=INK, strokeWidth=4.5)
d.path(smooth([(398, 676), (392, 714), (386, 748), (376, 770), (366, 784),
               (372, 798), (400, 796), (418, 780), (428, 746), (432, 710)]),
       "Front leg near", fill=COAT_GRAD, stroke=INK, strokeWidth=5)
# front paw pair
d.path("M364,780 C350,786 344,794 350,802 C364,806 386,804 396,794 "
       "C396,784 380,778 364,780 Z", "Front paw near", fill=COAT_GRAD,
       stroke=INK, strokeWidth=4)

# neck — arched wedge rising off the withers into the proud head
d.path(smooth([(368, 590), (348, 556), (336, 522), (332, 496), (344, 478),
               (368, 474), (392, 490), (406, 522), (414, 556), (410, 590)]),
       "Neck", fill=COAT_GRAD, stroke=INK, strokeWidth=5)
# chest bib shading at the throat junction
d.path("M344,560 C352,596 366,626 390,650", "Throat shade", fill=NONE,
       stroke="#3A1C0E", strokeWidth=4, opacity=40, cap="round")

# head — long muzzle, slight convex profile, nose carried high
d.path(smooth([(330, 462), (306, 458), (282, 462), (258, 472), (242, 486),
               (238, 500), (248, 512), (266, 518), (288, 522), (310, 528),
               (332, 540), (352, 552), (368, 562), (384, 560), (394, 540),
               (394, 512), (388, 488), (372, 472), (352, 462)]),
       "Head", fill=COAT_GRAD, stroke=INK, strokeWidth=5)
# muzzle sheen along the nasal bridge
d.path("M252,486 C278,470 312,462 344,462", "Bridge sheen", fill=NONE,
       stroke="#D8955C", strokeWidth=4, opacity=40, cap="round")
# nose — black, at the lifted muzzle tip
d.path("M236,488 C228,494 228,506 238,510 C248,512 256,506 256,496 "
       "C254,486 244,482 236,488 Z", "Nose", fill="#140D09",
       stroke=INK, strokeWidth=3)
d.path("M234,494 C238,489 246,488 250,491", "Nose sheen", fill=NONE,
       stroke="#8A705A", strokeWidth=2.5, opacity=75, cap="round")
# level mouth line under the muzzle
d.path("M252,514 C272,522 296,528 318,530", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=3.5, opacity=80, cap="round")

# drop ear — long folded ear hanging off the high skull, covering the cheek
d.path(smooth([(352, 470), (372, 478), (388, 498), (396, 528), (396, 560),
               (388, 590), (372, 610), (354, 612), (342, 596), (338, 562),
               (340, 524), (344, 494)]),
       "Ear", fill=DIM_GRAD, stroke=INK, strokeWidth=5)
d.path("M352,496 C360,530 360,566 352,596", "Ear fold", fill=NONE,
       stroke="#2E1408", strokeWidth=4, opacity=50, cap="round")

# eye — calm dark almond, looking ahead not at us
d.path("M296,486 C304,478 318,478 324,486 C322,497 308,501 300,496 "
       "C295,492 294,490 296,486 Z", "Eye",
       fill=rad((0, "#6E4A24"), (0.7, "#422A12"), (1, "#1E1208")),
       stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Pupil", x=303, y=484, width=9, height=10, fill="#0E0806", stroke=NONE)
d.shape("ellipse", "Glint", x=305, y=485, width=4.5, height=4.5, fill="#FFF4D8", opacity=90, stroke=NONE)
d.path("M290,474 C304,468 320,468 330,474", "Brow", fill=NONE,
       stroke="#3A1C0E", strokeWidth=4, opacity=55, cap="round")
# tan point over the eye — the little eyebrow dot of the red type
d.shape("ellipse", "Eyebrow point", x=298, y=470, width=18, height=10,
        fill="#C98A54", opacity=65, stroke=NONE)

# smooth-coat sheen — a few short ticks on shoulder and hip
for i, dd in enumerate(["M416,606 C424,596 434,590 446,588",
                        "M474,600 C484,592 496,588 508,588",
                        "M610,618 C622,612 634,610 646,612"]):
    d.path(dd, f"Coat sheen {i+1}", fill=NONE, stroke="#D8955C",
           strokeWidth=3.5, opacity=35, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#33291A", strokeWidth=6)

# --- captions -------------------------------------------------------------------
d.text("DACHSHUND", "Name", x=500, y=934, size=56, font="Virelai Sans",
       color="#EDE4C4", justify="center")
LINE2, SZ2, TRK = "HOUND · GERMANY", 22, 280
r = d.text(LINE2, "Milestone", x=500, y=970, size=SZ2, font="Virelai Sans",
           color="#C9BFA0", justify="center")
d.cmd("text.setStyle", "Milestone tracking", id=r["id"], tracking=TRK)

b = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("milestone bounds", {k: round(v) for k, v in b.items()})
nearest = (min(max(PCX, b["x"]), b["x"] + b["width"]),
           min(max(PCY, b["y"]), b["y"] + b["height"]))
clear = math.hypot(nearest[0] - PCX, nearest[1] - PCY) - (PR + 3)
print("clears rim by %.1f" % clear)
assert clear > 0 and b["width"] <= 760 and b["x"] >= 10 and b["x"] + b["width"] <= 990, b

d.finish("dachshund-V1R00")
