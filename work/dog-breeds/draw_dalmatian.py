#!/usr/bin/env python3
"""Dalmatian — milestone card V1R00. Trotting coach-dog profile: white
coat, crisp black spots of varied size and no symmetry — each spot an
individually placed shape, never a texture fill. Long tapering tail,
thin pendant ears, the light loose trot of a dog built to run under a
carriage axle. Dusk-stone disc, cobble floor closing on the disc's arc.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Dalmatian — Milestone Card", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#221A15"                    # warm dark ink, never pure black
SPOT = "#1E1610"                   # spot black — warm, never pure


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


def spot(cx, cy, w, h):
    """One hand-placed spot — a slightly irregular blob, never a circle stamp."""
    pts = [(cx - w / 2, cy + h * 0.08), (cx - w * 0.22, cy - h * 0.42),
           (cx + w * 0.28, cy - h / 2), (cx + w / 2, cy - h * 0.06),
           (cx + w * 0.24, cy + h * 0.46), (cx - w * 0.3, cy + h / 2)]
    return smooth(pts)


BG_GRAD = lin(0, 0, 0, 1000, (0, "#14161A"), (1, "#07080A"))
PLATE_GRAD = rad((0, "#AAB0A0"), (0.55, "#707A6C"), (1, "#3A443C"))
COAT_GRAD = lin(300, 480, 700, 800, (0, "#F4EEE0"), (0.5, "#DBD0B8"), (1, "#A99C80"))
DIM_GRAD = lin(300, 480, 700, 800, (0, "#C8BCA2"), (1, "#847660"))
FLOOR_GRAD = lin(0, 750, 0, 880, (0, "#5C6052"), (0.55, "#40443A"), (1, "#20241C"))

# --- backdrop + dusk-stone plate --------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#30382E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E4E8D2", strokeWidth=3, opacity=38)

# thin light pooling upper-left
d.shape("ellipse", "Light pool", x=250, y=150, width=400, height=230,
        fill="#ECF0DA", opacity=13, stroke=NONE)
# drifting mist lenses
for i, (x, y, w) in enumerate([(320, 330, 90), (570, 245, 70), (710, 360, 80),
                               (250, 470, 60), (750, 490, 64), (455, 195, 55)]):
    assert on_disc(x, y, 20), i
    d.shape("ellipse", f"Mist {i+1}", x=x - w / 2, y=y - w / 5, width=w, height=w * 0.4,
            fill="#E8ECD8", opacity=11, stroke=NONE)

# --- cobble floor, closing on the disc arc ----------------------------------------
fy = 790
fl, fr = rim_x(fy, -1), rim_x(fy, 1)
d.path(f"M{fl:.1f},{fy} C300,778 400,800 500,790 C600,780 700,786 {fr:.1f},{fy} "
       f"A{PR},{PR} 0 0 1 {fl:.1f},{fy} Z", "Floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{fl + 8:.0f},{fy} C300,778 400,800 500,790 C600,780 700,786 {fr - 8:.0f},{fy}",
       "Floor crest", fill=NONE, stroke="#98A088", strokeWidth=5, opacity=42, cap="round")
# cobbles — scattered rounded stones on the crest
for i, (x, y, w) in enumerate([(330, 812, 34), (420, 832, 28), (540, 838, 36),
                               (645, 824, 30), (700, 806, 26)]):
    assert on_disc(x, y, 14), i
    d.shape("ellipse", f"Cobble {i+1}", x=x - w / 2, y=y - 6, width=w, height=13,
            fill="#6E7260", opacity=55, stroke=NONE)
    d.path(f"M{x - w * 0.3},{y - 4} C{x - w * 0.1},{y - 8} {x + w * 0.2},{y - 8} {x + w * 0.35},{y - 4}",
           f"Cobble sheen {i+1}", fill=NONE, stroke="#A8AE94", strokeWidth=2.5,
           opacity=40, cap="round")

# soft shadow under the trotting dog
d.shape("ellipse", "Dog shadow", x=290, y=758, width=420, height=30,
        fill="#12150E", opacity=32, stroke=NONE)

# --- the dalmatian, trotting profile facing left ------------------------------------
# tail — long tapering whip off the rump, carried low with a slight lift
d.path(smooth([(676, 610), (716, 618), (748, 632), (768, 650), (776, 668),
               (766, 676), (748, 664), (722, 648), (698, 632), (676, 622)]),
       "Tail", fill=lin(680, 610, 775, 670, (0, "#E8E0CC"), (1, "#B4A888")),
       stroke=INK, strokeWidth=5)

# hind legs — trot diagonal: far hind reaching under, near hind pushing back
d.path(smooth([(608, 650), (596, 690), (580, 728), (558, 758), (542, 780),
               (546, 794), (570, 792), (594, 772), (616, 740), (630, 704),
               (634, 672)]),
       "Hind leg far", fill=DIM_GRAD, stroke=INK, strokeWidth=4.5)
d.path(smooth([(648, 644), (664, 686), (676, 722), (682, 752), (676, 776),
               (686, 790), (708, 788), (722, 770), (724, 738), (716, 702),
               (698, 672), (674, 652)]),
       "Hind leg near", fill=COAT_GRAD, stroke=INK, strokeWidth=5)
# hind paws
d.path("M540,780 C528,786 524,794 532,800 C546,804 566,800 574,790 "
       "C572,780 554,774 540,780 Z", "Hind paw far", fill=DIM_GRAD,
       stroke=INK, strokeWidth=3.5)
d.path("M682,778 C670,784 666,792 674,798 C688,802 708,798 716,788 "
       "C714,778 696,772 682,778 Z", "Hind paw near", fill=COAT_GRAD,
       stroke=INK, strokeWidth=4)

# body — lean coach dog: deep chest, tucked belly, level back
d.path(smooth([(392, 592), (366, 622), (360, 660), (376, 698), (414, 720),
               (480, 730), (570, 726), (640, 706), (676, 676), (690, 640),
               (676, 610), (634, 596), (566, 588), (480, 586), (424, 588)]),
       "Body", fill=COAT_GRAD, stroke=INK, strokeWidth=6)
# topline sheen
d.path("M420,592 C500,582 590,586 660,606", "Back sheen", fill=NONE,
       stroke="#FDF8E8", strokeWidth=5, opacity=45, cap="round")
# belly tuck shading
d.path("M430,716 C500,728 590,724 650,700 C596,732 480,736 434,724 Z",
       "Belly shade", fill="#8A7E66", opacity=40, stroke=NONE)

# front legs — the trot: near fore reaching forward-down, far fore planted
# near-vertical under the shoulder
d.path(smooth([(424, 660), (420, 700), (418, 736), (416, 764), (412, 784),
               (420, 796), (444, 794), (458, 776), (464, 742), (466, 706),
               (464, 678)]),
       "Front leg far", fill=DIM_GRAD, stroke=INK, strokeWidth=4.5)
d.path(smooth([(446, 656), (432, 696), (414, 734), (392, 764), (374, 786),
               (380, 800), (408, 798), (434, 778), (456, 744), (468, 708),
               (472, 676)]),
       "Front leg near", fill=COAT_GRAD, stroke=INK, strokeWidth=5)
# front paws
d.path("M410,782 C398,788 394,796 402,802 C416,806 436,802 444,792 "
       "C442,782 424,776 410,782 Z", "Front paw far", fill=DIM_GRAD,
       stroke=INK, strokeWidth=3.5)
d.path("M374,784 C360,790 356,798 364,804 C380,808 402,804 410,794 "
       "C408,784 388,778 374,784 Z", "Front paw near", fill=COAT_GRAD,
       stroke=INK, strokeWidth=4)

# neck — clean arch off the withers into the lifted head
d.path(smooth([(404, 596), (380, 566), (360, 536), (348, 508), (352, 484),
               (370, 472), (394, 480), (412, 504), (424, 536), (430, 570),
               (428, 598)]),
       "Neck", fill=COAT_GRAD, stroke=INK, strokeWidth=5)

# head — long clean muzzle, slight stop, alert ahead
d.path(smooth([(356, 476), (330, 470), (304, 472), (280, 482), (262, 496),
               (252, 512), (254, 526), (266, 536), (284, 542), (306, 548),
               (326, 556), (346, 568), (364, 576), (380, 570), (390, 550),
               (392, 522), (386, 498), (372, 482)]),
       "Head", fill=COAT_GRAD, stroke=INK, strokeWidth=5)
# nose — dark leather at the muzzle tip
d.path("M250,512 C242,518 242,530 252,534 C262,536 270,530 270,520 "
       "C268,510 258,506 250,512 Z", "Nose", fill="#140D09",
       stroke=INK, strokeWidth=3)
d.path("M248,520 C252,515 260,514 264,517", "Nose sheen", fill=NONE,
       stroke="#8A705A", strokeWidth=2.5, opacity=75, cap="round")
# level mouth
d.path("M266,540 C284,548 306,552 326,552", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=3.5, opacity=80, cap="round")
# stop — the dip where muzzle meets forehead, kept faint
d.path("M332,486 C336,496 337,506 335,514", "Stop", fill=NONE,
       stroke="#8A7E66", strokeWidth=3.5, opacity=30, cap="round")

# pendant ears — thin, set high, hanging close beside the cheeks
d.path(smooth([(370, 478), (386, 490), (396, 512), (398, 540), (392, 566),
               (378, 582), (362, 580), (352, 560), (350, 530), (354, 500)]),
       "Ear", fill=DIM_GRAD, stroke=INK, strokeWidth=5)
d.path("M372,500 C380,524 380,552 372,572", "Ear fold", fill=NONE,
       stroke="#6E6250", strokeWidth=4, opacity=50, cap="round")

# eye — alert dark almond
d.path("M306,506 C314,498 328,498 334,506 C332,517 318,521 310,516 "
       "C305,512 304,510 306,506 Z", "Eye",
       fill=rad((0, "#6E4A24"), (0.7, "#422A12"), (1, "#1E1208")),
       stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Pupil", x=313, y=504, width=9, height=10, fill="#0E0806", stroke=NONE)
d.shape("ellipse", "Glint", x=315, y=505, width=4.5, height=4.5, fill="#FFF4D8", opacity=90, stroke=NONE)
d.path("M300,494 C314,488 330,488 340,494", "Brow", fill=NONE,
       stroke="#8A7E66", strokeWidth=4, opacity=55, cap="round")

# --- the spots — individually placed, varied, asymmetric -----------------------------
# each tuple: (cx, cy, w, h) — scattered over neck, body, legs, head, ear
for i, (cx, cy, w, h) in enumerate([
        (392, 500, 26, 22), (366, 552, 18, 15), (416, 566, 32, 26),
        (452, 612, 22, 18), (508, 600, 34, 28), (556, 622, 20, 17),
        (600, 600, 28, 24), (646, 618, 18, 15), (620, 652, 30, 24),
        (560, 668, 22, 18), (500, 660, 16, 14), (452, 664, 26, 20),
        (416, 700, 18, 15), (668, 660, 20, 16), (686, 640, 14, 12),
        (446, 720, 14, 12), (610, 706, 16, 13), (356, 642, 15, 13),
        (340, 590, 13, 11), (690, 690, 15, 12), (296, 512, 12, 10),
        (318, 534, 10, 9), (368, 540, 12, 10), (452, 700, 15, 12)]):
    d.path(spot(cx, cy, w, h), f"Spot {i+1}", fill=SPOT, stroke=NONE, opacity=92)

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#2C3628", strokeWidth=6)

# --- captions -------------------------------------------------------------------
d.text("DALMATIAN", "Name", x=500, y=934, size=56, font="Virelai Sans",
       color="#ECF0E0", justify="center")
LINE2, SZ2, TRK = "NON-SPORTING · DALMATIA", 22, 280
r = d.text(LINE2, "Milestone", x=500, y=970, size=SZ2, font="Virelai Sans",
           color="#C2C8B2", justify="center")
d.cmd("text.setStyle", "Milestone tracking", id=r["id"], tracking=TRK)

b = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("milestone bounds", {k: round(v) for k, v in b.items()})
nearest = (min(max(PCX, b["x"]), b["x"] + b["width"]),
           min(max(PCY, b["y"]), b["y"] + b["height"]))
clear = math.hypot(nearest[0] - PCX, nearest[1] - PCY) - (PR + 3)
print("clears rim by %.1f" % clear)
assert clear > 0 and b["width"] <= 760 and b["x"] >= 10 and b["x"] + b["width"] <= 990, b

d.finish("dalmatian-V1R00")
