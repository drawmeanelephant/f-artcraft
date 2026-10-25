#!/usr/bin/env python3
"""Pembroke welsh corgi — milestone card V1R00. Low loaf body on stubby
legs, big foxy erect ears, smiling foxy face, docked nub of a tail; red
over white — blaze, chest and legs. Mid-heel-nip lunge: head stretched
low and forward, near fore stepping out — the herding job the short legs
were built for. Misty slate hill disc, turf floor closing on the arc.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Pembroke Welsh Corgi — Milestone Card", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#241B14"                    # warm dark ink, never pure black


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


BG_GRAD = lin(0, 0, 0, 1000, (0, "#12161A"), (1, "#06080B"))
PLATE_GRAD = rad((0, "#AABCC2"), (0.55, "#6E8490"), (1, "#384852"))
RED_GRAD = lin(300, 460, 700, 800, (0, "#C8843E"), (0.5, "#9A5E26"), (1, "#5C3616"))
DIM_GRAD = lin(300, 460, 700, 800, (0, "#8A5426"), (1, "#3C2210"))
WHITE_GRAD = lin(300, 560, 500, 800, (0, "#F4EEE0"), (1, "#D2C4A6"))
FLOOR_GRAD = lin(0, 750, 0, 880, (0, "#4E5648"), (0.55, "#343C30"), (1, "#1A2018"))

# --- backdrop + slate hill plate ---------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#2C3A42", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#DCE6E4", strokeWidth=3, opacity=38)

# low misty light pooling upper-left
d.shape("ellipse", "Light pool", x=250, y=150, width=400, height=230,
        fill="#EAF0EC", opacity=13, stroke=NONE)
# drifting mist lenses
for i, (x, y, w) in enumerate([(320, 330, 90), (570, 245, 70), (710, 360, 80),
                               (250, 470, 60), (750, 490, 64), (455, 195, 55)]):
    assert on_disc(x, y, 20), i
    d.shape("ellipse", f"Mist {i+1}", x=x - w / 2, y=y - w / 5, width=w, height=w * 0.4,
            fill="#E4ECE6", opacity=12, stroke=NONE)

# --- turf floor, closing on the disc arc --------------------------------------------
fy = 795
fl, fr = rim_x(fy, -1), rim_x(fy, 1)
d.path(f"M{fl:.1f},{fy} C300,782 400,806 500,796 C600,786 700,792 {fr:.1f},{fy} "
       f"A{PR},{PR} 0 0 1 {fl:.1f},{fy} Z", "Floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{fl + 8:.0f},{fy} C300,782 400,806 500,796 C600,786 700,792 {fr - 8:.0f},{fy}",
       "Floor crest", fill=NONE, stroke="#8A9678", strokeWidth=5, opacity=42, cap="round")
# turf tufts — short bent strokes rooted on the crest
for i, (x, y) in enumerate([(330, 815), (415, 835), (545, 840), (640, 826), (695, 808)]):
    assert on_disc(x, y + 8, 14), i
    for j, (dx, dy) in enumerate([(-12, 8), (-4, -6), (4, -12), (12, -2)]):
        d.path(f"M{x + dx * 0.4:.0f},{y + 12} L{x + dx:.0f},{y + dy:.0f}",
               f"Tuft {i+1}.{j+1}", fill=NONE, stroke="#5E6E50",
               strokeWidth=3.5, opacity=65, cap="round")

# soft shadow under the loaf
d.shape("ellipse", "Dog shadow", x=290, y=760, width=440, height=30,
        fill="#0E140E", opacity=32, stroke=NONE)

# --- the corgi, heel-nip lunge facing left ---------------------------------------------
# docked nub — a tiny rounded stub at the rump
d.path("M676,628 C690,622 700,626 702,636 C698,646 684,650 676,644 Z",
       "Tail nub", fill=DIM_GRAD, stroke=INK, strokeWidth=4)

# hind legs — bent, driving, rump slightly high
d.path(smooth([(596, 656), (592, 694), (584, 730), (570, 758), (556, 780),
               (560, 794), (584, 792), (604, 772), (620, 740), (628, 704),
               (626, 672)]),
       "Hind leg far", fill=DIM_GRAD, stroke=INK, strokeWidth=4.5)
d.path(smooth([(638, 650), (656, 692), (668, 728), (672, 758), (664, 782),
               (672, 796), (696, 794), (712, 774), (716, 742), (710, 706),
               (694, 674), (668, 654)]),
       "Hind leg near", fill=RED_GRAD, stroke=INK, strokeWidth=5)
# white hind socks
d.path("M554,780 C542,786 538,794 546,800 C560,804 580,800 588,790 "
       "C586,780 568,774 554,780 Z", "Hind sock far", fill=WHITE_GRAD,
       opacity=90, stroke=INK, strokeWidth=3.5)
d.path("M664,782 C652,788 648,796 656,802 C670,806 692,802 700,792 "
       "C698,782 678,776 664,782 Z", "Hind sock near", fill=WHITE_GRAD,
       stroke=INK, strokeWidth=4)

# body — the long loaf, back level-ish, deep chest, short legs under
d.path(smooth([(400, 606), (372, 634), (364, 672), (380, 708), (420, 728),
               (490, 738), (575, 734), (645, 714), (680, 682), (690, 646),
               (676, 618), (634, 602), (560, 594), (480, 592), (430, 596)]),
       "Body", fill=RED_GRAD, stroke=INK, strokeWidth=6)
# topline sheen
d.path("M424,600 C500,590 590,594 656,612 C580,600 490,598 424,608 Z",
       "Back sheen", fill="#E8AE6A", opacity=35, stroke=NONE)
# white underside — chest through belly, the corgi's low white skirt
d.path(smooth([(366, 668), (382, 706), (420, 726), (490, 736), (570, 732),
               (640, 714), (668, 692), (660, 680), (610, 690), (530, 694),
               (450, 692), (390, 680)]),
       "White underside", fill=WHITE_GRAD, stroke=NONE, opacity=95)

# front legs — near fore stepping out low for the nip, far fore under chest
d.path(smooth([(414, 676), (404, 714), (392, 750), (378, 776), (366, 792),
               (372, 804), (398, 802), (418, 782), (434, 748), (442, 712),
               (444, 684)]),
       "Front leg far", fill=DIM_GRAD, stroke=INK, strokeWidth=4.5)
d.path(smooth([(444, 668), (428, 706), (406, 742), (382, 770), (364, 788),
               (370, 802), (398, 800), (424, 780), (448, 746), (462, 710),
               (466, 678)]),
       "Front leg near", fill=RED_GRAD, stroke=INK, strokeWidth=5)
# white front legs/socks — corgis carry white up the forelegs
d.path("M370,752 C360,766 356,784 362,798 C376,806 400,802 412,790 "
       "C416,772 408,756 392,750 Z", "Front sock far", fill=WHITE_GRAD,
       opacity=90, stroke=INK, strokeWidth=3.5)
d.path("M368,748 C352,762 344,782 352,798 C368,808 398,804 414,790 "
       "C420,772 412,754 394,748 Z", "Front sock near", fill=WHITE_GRAD,
       stroke=INK, strokeWidth=4)

# neck — stretched forward and low for the nip
d.path(smooth([(408, 608), (382, 594), (356, 580), (336, 566), (326, 548),
               (334, 532), (356, 530), (380, 544), (400, 566), (412, 592),
               (414, 614)]),
       "Neck", fill=RED_GRAD, stroke=INK, strokeWidth=5)
# white throat running under the jaw into the chest
d.path(smooth([(322, 586), (344, 600), (366, 616), (386, 638), (396, 664),
               (388, 680), (366, 678), (344, 664), (328, 642), (318, 616),
               (316, 598)]),
       "Throat white", fill=WHITE_GRAD, stroke=INK, strokeWidth=3.5)

# head — foxy wedge, muzzle level, ears tall
d.path(smooth([(336, 528), (310, 522), (286, 526), (262, 538), (246, 554),
               (240, 570), (246, 584), (260, 592), (280, 598), (302, 602),
               (324, 610), (346, 620), (364, 630), (380, 626), (390, 608),
               (392, 582), (388, 556), (374, 538), (356, 528)]),
       "Head", fill=RED_GRAD, stroke=INK, strokeWidth=5)
# white blaze widening over the muzzle front
d.path(smooth([(300, 528), (284, 532), (268, 542), (254, 556), (248, 572),
               (254, 586), (268, 592), (284, 592), (298, 584), (306, 568),
               (308, 550), (306, 538)]),
       "Blaze + muzzle", fill=WHITE_GRAD, opacity=95, stroke=NONE)

# the big foxy ears — far ear drawn first slightly behind, near ear tall
# and forward-cupped; both tips spread, never crossing
d.path("M372,512 L404,436 L408,534 Z", "Ear far", fill=DIM_GRAD,
       stroke=INK, strokeWidth=4.5)
d.path("M344,530 L306,420 L378,506 Z", "Ear near", fill=RED_GRAD,
       stroke=INK, strokeWidth=4.5)
d.path("M318,434 L334,468 L326,492 Z", "Ear near inner", fill="#3C2210",
       stroke=INK, strokeWidth=3.5)
d.path("M384,462 L392,494 L386,516 Z", "Ear far inner", fill="#241408",
       stroke=INK, strokeWidth=3)

# the smile — mouth line upturned at the corner, slight open with tongue hint
d.path("M250,582 C268,592 290,598 312,600", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=3.5, cap="round")
d.path("M312,600 C318,602 322,600 324,596", "Smile corner", fill=NONE,
       stroke=INK, strokeWidth=3.5, cap="round")
d.path("M268,596 C278,602 290,604 300,602 C292,610 276,610 268,602 Z",
       "Tongue", fill="#C4706A", stroke=INK, strokeWidth=3)
# nose — black, at the muzzle tip
d.path("M238,556 C230,562 230,574 240,578 C250,580 258,574 258,564 "
       "C256,554 246,550 238,556 Z", "Nose", fill="#140D09",
       stroke=INK, strokeWidth=3)
d.path("M236,564 C240,559 248,558 252,561", "Nose sheen", fill=NONE,
       stroke="#8A705A", strokeWidth=2.5, opacity=75, cap="round")

# eye — bright foxy almond, looking ahead
d.path("M310,552 C318,544 332,544 338,552 C336,563 322,567 314,562 "
       "C309,558 308,556 310,552 Z", "Eye",
       fill=rad((0, "#7A5226"), (0.7, "#4A3014"), (1, "#241608")),
       stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Pupil", x=317, y=550, width=9, height=10, fill="#0E0806", stroke=NONE)
d.shape("ellipse", "Glint", x=319, y=551, width=4.5, height=4.5, fill="#FFF4D8", opacity=90, stroke=NONE)
# tan cheek point + brow point of the red-and-white pattern
d.shape("ellipse", "Brow point", x=318, y=532, width=16, height=9,
        fill="#8A5426", opacity=70, stroke=NONE)
d.path("M304,540 C318,534 334,534 344,540", "Brow", fill=NONE,
       stroke="#5C3616", strokeWidth=4, opacity=55, cap="round")

# cheek fluff — the corgi's foxy cheek ruffs
for i, dd in enumerate(["M368,606 C378,614 386,620 392,626",
                        "M352,592 C360,600 366,606 372,610"]):
    d.path(dd, f"Cheek ruff {i+1}", fill=NONE, stroke="#E8AE6A",
           strokeWidth=3.5, opacity=45, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#26343A", strokeWidth=6)

# --- captions -------------------------------------------------------------------
d.text("PEMBROKE WELSH CORGI", "Name", x=500, y=934, size=56, font="Virelai Sans",
       color="#E8ECE6", justify="center")
LINE2, SZ2, TRK = "HERDING · WALES", 22, 280
r = d.text(LINE2, "Milestone", x=500, y=970, size=SZ2, font="Virelai Sans",
           color="#BCC8C0", justify="center")
d.cmd("text.setStyle", "Milestone tracking", id=r["id"], tracking=TRK)

b = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("milestone bounds", {k: round(v) for k, v in b.items()})
nearest = (min(max(PCX, b["x"]), b["x"] + b["width"]),
           min(max(PCY, b["y"]), b["y"] + b["height"]))
clear = math.hypot(nearest[0] - PCX, nearest[1] - PCY) - (PR + 3)
print("clears rim by %.1f" % clear)
assert clear > 0 and b["width"] <= 760 and b["x"] >= 10 and b["x"] + b["width"] <= 990, b

d.finish("pembroke-welsh-corgi-V1R00")
