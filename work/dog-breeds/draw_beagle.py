#!/usr/bin/env python3
"""Beagle — milestone card V1R00. Nose to the ground mid-scent: tricolor
(black saddle, tan head and rear, white blaze, chest and legs), the long
ears swung forward with the lowered head, merry tail carried high with
its white tip. Autumn-leaf floor closing on the disc's own arc.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Beagle — Milestone Card", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#261A12"                    # warm dark ink, never pure black


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


BG_GRAD = lin(0, 0, 0, 1000, (0, "#1A1510"), (1, "#0A0705"))
PLATE_GRAD = rad((0, "#C8B078"), (0.55, "#907748"), (1, "#4E4026"))
TAN_GRAD = lin(300, 540, 700, 800, (0, "#C89355"), (0.5, "#9A6A36"), (1, "#5E3C1E"))
DIM_GRAD = lin(300, 540, 700, 800, (0, "#8A5C30"), (1, "#3C2412"))
SADDLE_GRAD = lin(430, 560, 660, 700, (0, "#463A30"), (0.6, "#2A211A"), (1, "#16100C"))
WHITE_GRAD = lin(300, 560, 500, 800, (0, "#F2EADA"), (1, "#D2C2A0"))
FLOOR_GRAD = lin(0, 745, 0, 880, (0, "#6E5030"), (0.55, "#4C3820"), (1, "#241C0E"))

# --- backdrop + autumn plate ----------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#42351E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8DCB4", strokeWidth=3, opacity=38)

# low amber light pooling upper-left
d.shape("ellipse", "Light pool", x=250, y=150, width=400, height=230,
        fill="#F2DDA6", opacity=14, stroke=NONE)
# drifting mist lenses
for i, (x, y, w) in enumerate([(320, 330, 90), (570, 245, 70), (710, 360, 80),
                               (245, 470, 60), (750, 490, 64), (455, 195, 55)]):
    assert on_disc(x, y, 20), i
    d.shape("ellipse", f"Mist {i+1}", x=x - w / 2, y=y - w / 5, width=w, height=w * 0.4,
            fill="#EDE0BC", opacity=11, stroke=NONE)

# --- leaf-litter floor, closing on the disc arc -----------------------------------
fy = 795
fl, fr = rim_x(fy, -1), rim_x(fy, 1)
d.path(f"M{fl:.1f},{fy} C300,782 400,806 500,796 C600,786 700,792 {fr:.1f},{fy} "
       f"A{PR},{PR} 0 0 1 {fl:.1f},{fy} Z", "Floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{fl + 8:.0f},{fy} C300,782 400,806 500,796 C600,786 700,792 {fr - 8:.0f},{fy}",
       "Floor crest", fill=NONE, stroke="#B28C4E", strokeWidth=5, opacity=42, cap="round")
# fallen autumn leaves — rust and ochre ovals along the crest
for i, (x, y, w, c) in enumerate([(315, 815, 24, "#9A5228"), (420, 836, 20, "#B07A34"),
                                  (560, 840, 24, "#86481F"), (655, 826, 20, "#A8662E"),
                                  (700, 808, 18, "#9A5228")]):
    assert on_disc(x, y, 14), i
    d.path(f"M{x},{y} C{x + w * 0.4},{y - w * 0.55} {x + w},{y - w * 0.2} {x + w * 1.1},{y} "
           f"C{x + w},{y + w * 0.3} {x + w * 0.4},{y + w * 0.4} {x},{y} Z",
           f"Leaf {i+1}", fill=c, opacity=62, stroke=NONE)
    d.path(f"M{x + 3},{y} L{x + w * 1.0},{y}", f"Leaf vein {i+1}", fill=NONE,
           stroke="#4E3014", strokeWidth=3, opacity=50, cap="round")
# two leaves still falling, mid-air inside the disc
for i, (x, y, w, c) in enumerate([(290, 560, 18, "#A8662E"), (720, 430, 16, "#9A5228")]):
    assert on_disc(x, y, 20), i
    d.path(f"M{x},{y} C{x + w * 0.4},{y - w * 0.55} {x + w},{y - w * 0.2} {x + w * 1.1},{y} "
           f"C{x + w},{y + w * 0.3} {x + w * 0.4},{y + w * 0.4} {x},{y} Z",
           f"Falling leaf {i+1}", fill=c, opacity=55, stroke=NONE)

# soft shadow under the working dog
d.shape("ellipse", "Dog shadow", x=280, y=765, width=440, height=30,
        fill="#161007", opacity=32, stroke=NONE)

# --- the beagle, nose-down profile facing left --------------------------------------
# merry tail first — high sickle off the rump, white tip
d.path(smooth([(686, 624), (706, 582), (716, 536), (718, 494), (710, 472),
               (698, 470), (690, 496), (684, 540), (674, 584), (666, 614)]),
       "Tail", fill=lin(660, 610, 710, 465, (0, "#6E4A28"), (0.7, "#3C2814"), (1, "#7E5630")),
       stroke=INK, strokeWidth=5)
d.path(smooth([(688, 502), (694, 484), (698, 470), (706, 468), (706, 486),
               (700, 502)]),
       "Tail white tip", fill=WHITE_GRAD, stroke=INK, strokeWidth=3.5)

# hind legs — near hind planted back, far hind stepping under
d.path(smooth([(600, 656), (596, 694), (588, 730), (572, 756), (556, 778),
               (552, 794), (568, 800), (592, 794), (614, 770), (630, 736),
               (634, 698), (630, 668)]),
       "Hind leg far", fill=DIM_GRAD, stroke=INK, strokeWidth=4.5)
d.path(smooth([(640, 648), (660, 692), (668, 730), (664, 760), (650, 782),
               (648, 796), (670, 800), (694, 790), (708, 760), (710, 720),
               (700, 682), (678, 656)]),
       "Hind leg near", fill=TAN_GRAD, stroke=INK, strokeWidth=5)
# white hind socks
d.path("M548,780 C538,788 536,796 544,802 C556,806 574,802 582,792 "
       "C580,782 562,776 548,780 Z", "Hind sock far", fill=WHITE_GRAD,
       opacity=90, stroke=INK, strokeWidth=3.5)
d.path("M646,782 C634,788 630,796 638,802 C652,806 672,802 680,792 "
       "C678,782 660,776 646,782 Z", "Hind sock near", fill=WHITE_GRAD,
       stroke=INK, strokeWidth=4)

# body — drawn BLACK: the tricolor saddle owns the whole upper torso,
# so the topline silhouette is the marking's own edge, never inset
d.path(smooth([(420, 596), (396, 624), (392, 662), (410, 700), (448, 722),
               (520, 732), (600, 728), (662, 706), (690, 672), (694, 636),
               (676, 612), (630, 598), (560, 590), (490, 590)]),
       "Body", fill=SADDLE_GRAD, stroke=INK, strokeWidth=6)
# tan underside + chest — one overlay whose wavy top edge is the blanket's
# lower boundary at mid-ribs; kept a few px inside the silhouette so the
# ink outline stays the outer edge
d.path(smooth([(414, 614), (448, 630), (492, 650), (528, 640), (562, 656),
               (596, 646), (630, 662), (652, 682), (676, 700), (640, 720),
               (560, 728), (478, 726), (428, 710), (404, 680), (398, 648)]),
       "Tan underside", fill=TAN_GRAD, stroke=NONE)
d.path("M440,600 C510,588 590,592 648,610", "Saddle sheen", fill=NONE,
       stroke="#6E5E50", strokeWidth=5, opacity=30, cap="round")
d.path("M480,640 C520,648 560,650 600,644", "Saddle sheen 2", fill=NONE,
       stroke="#5E5248", strokeWidth=4, opacity=22, cap="round")

# white chest + belly fringe under the saddle line
d.path("M414,690 C470,712 560,716 640,700 C590,728 470,730 420,706 "
       "C412,700 410,694 414,690 Z", "Belly white", fill=WHITE_GRAD, opacity=85, stroke=NONE)

# front legs — mid-scent walk: far leg vertical under the chest, near leg
# stepping forward toward the scent
d.path(smooth([(430, 668), (426, 706), (422, 744), (418, 772), (414, 790),
               (422, 800), (444, 798), (456, 780), (462, 748), (464, 712),
               (462, 684)]),
       "Front leg far", fill=DIM_GRAD, stroke=INK, strokeWidth=4.5)
d.path(smooth([(452, 662), (438, 702), (418, 740), (396, 768), (380, 788),
               (386, 802), (414, 800), (440, 782), (462, 748), (474, 712),
               (478, 680)]),
       "Front leg near", fill=TAN_GRAD, stroke=INK, strokeWidth=5)
# white front socks
d.path("M410,784 C398,790 394,798 402,804 C416,808 436,804 444,794 "
       "C442,784 424,778 410,784 Z", "Front sock far", fill=WHITE_GRAD,
       opacity=90, stroke=INK, strokeWidth=3.5)
d.path("M378,786 C364,792 360,800 368,806 C384,810 406,806 414,796 "
       "C412,786 392,780 378,786 Z", "Front sock near", fill=WHITE_GRAD,
       stroke=INK, strokeWidth=4)

# neck — sloping down-forward off the withers into the lowered skull
d.path(smooth([(424, 598), (396, 610), (366, 626), (340, 646), (322, 672),
               (318, 698), (330, 714), (354, 712), (380, 698), (402, 676),
               (420, 648), (430, 620)]),
       "Neck", fill=TAN_GRAD, stroke=INK, strokeWidth=5)
# white throat running down the neck front into the chest
d.path(smooth([(326, 684), (340, 706), (360, 722), (386, 732), (410, 730),
               (416, 714), (402, 700), (380, 690), (356, 682), (336, 676)]),
       "Throat white", fill=WHITE_GRAD, opacity=90, stroke=INK, strokeWidth=3.5)

# head — lowered, muzzle level to the ground, nose at the scent
d.path(smooth([(318, 676), (292, 680), (268, 692), (250, 708), (240, 726),
               (238, 744), (246, 758), (262, 764), (282, 764), (304, 756),
               (324, 742), (338, 722), (344, 700), (338, 682)]),
       "Head", fill=TAN_GRAD, stroke=INK, strokeWidth=5)
# white blaze + muzzle front — the white running nose to brow
d.path(smooth([(266, 696), (252, 708), (244, 724), (242, 742), (248, 756),
               (262, 762), (278, 758), (292, 746), (300, 728), (300, 710),
               (292, 698), (278, 694)]),
       "Blaze + muzzle", fill=WHITE_GRAD, opacity=95, stroke=NONE)
# nose — dark, at the dropped muzzle tip, almost touching the floor
d.path("M236,740 C228,746 228,758 238,762 C248,764 256,758 256,748 "
       "C254,738 244,734 236,740 Z", "Nose", fill="#140D09",
       stroke=INK, strokeWidth=3)
d.path("M234,748 C238,743 246,742 250,745", "Nose sheen", fill=NONE,
       stroke="#8A705A", strokeWidth=2.5, opacity=75, cap="round")
# scent ticks — short curls off the nose, kept well inside the rim
for i, dd in enumerate(["M234,764 C228,768 224,772 222,776",
                        "M246,772 C242,778 240,784 240,790"]):
    d.path(dd, f"Scent {i+1}", fill=NONE, stroke="#C4A872",
           strokeWidth=3, opacity=45, cap="round")
# level mouth under the muzzle
d.path("M252,760 C268,764 288,760 302,750", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=3.5, opacity=80, cap="round")

# the long ear — hangs down-forward off the lowered skull, draping over
# the cheek with its tip reaching toward the nose
d.path(smooth([(346, 656), (328, 660), (314, 676), (308, 702), (312, 730),
               (324, 752), (342, 760), (356, 752), (362, 726), (358, 696),
               (354, 672)]),
       "Ear", fill=DIM_GRAD, stroke=INK, strokeWidth=5)
d.path("M326,672 C320,700 320,730 330,752", "Ear fold", fill=NONE,
       stroke="#2A1808", strokeWidth=4, opacity=50, cap="round")

# eye — soft hound eye looking down the trail
d.path("M300,684 C308,676 322,676 328,684 C326,695 312,699 304,694 "
       "C299,690 298,688 300,684 Z", "Eye",
       fill=rad((0, "#7A5226"), (0.7, "#4A3014"), (1, "#241608")),
       stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Pupil", x=307, y=682, width=9, height=10, fill="#0E0806", stroke=NONE)
d.shape("ellipse", "Glint", x=309, y=683, width=4.5, height=4.5, fill="#FFF4D8", opacity=90, stroke=NONE)
d.path("M296,672 C310,666 326,666 336,672", "Brow", fill=NONE,
       stroke="#3C2410", strokeWidth=4, opacity=55, cap="round")

# short-coat sheen ticks on neck and quarter
for i, dd in enumerate(["M436,616 C446,608 458,604 470,604",
                        "M660,636 C672,630 682,628 690,630"]):
    d.path(dd, f"Coat sheen {i+1}", fill=NONE, stroke="#E0B87E",
           strokeWidth=3.5, opacity=35, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#3A2E18", strokeWidth=6)

# --- captions -------------------------------------------------------------------
d.text("BEAGLE", "Name", x=500, y=934, size=56, font="Virelai Sans",
       color="#F0E6C6", justify="center")
LINE2, SZ2, TRK = "HOUND · ENGLAND", 22, 280
r = d.text(LINE2, "Milestone", x=500, y=970, size=SZ2, font="Virelai Sans",
           color="#CEC2A2", justify="center")
d.cmd("text.setStyle", "Milestone tracking", id=r["id"], tracking=TRK)

b = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("milestone bounds", {k: round(v) for k, v in b.items()})
nearest = (min(max(PCX, b["x"]), b["x"] + b["width"]),
           min(max(PCY, b["y"]), b["y"] + b["height"]))
clear = math.hypot(nearest[0] - PCX, nearest[1] - PCY) - (PR + 3)
print("clears rim by %.1f" % clear)
assert clear > 0 and b["width"] <= 760 and b["x"] >= 10 and b["x"] + b["width"] <= 990, b

d.finish("beagle-V1R00")
