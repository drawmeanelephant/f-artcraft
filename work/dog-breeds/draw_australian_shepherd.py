#!/usr/bin/env python3
"""Australian shepherd — milestone card V1R00. Blue-merle coat at the
working trot in profile: silver base marbled with slate patches, cream
collar, blaze and socks, copper points on cheek, brow and pasterns.
Natural bobtail — a stub, not a whip. Near ear pricked, far ear tipped.
Ranch dog: dusty gold disc, dry-grass ticks on an earthen floor that
closes on the disc's arc. 1000x1000. House style: gradients + translucent
shading, never flat fills. Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Australian Shepherd — Milestone Card", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#241C18"                    # warm dark ink, never pure black
MERLE = "#26221E"                  # slate patch — warm dark, never pure


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


def merle(cx, cy, w, h):
    """One slate marbling patch — a lumpy blob, never a circle stamp."""
    pts = [(cx - w / 2, cy + h * 0.08), (cx - w * 0.22, cy - h * 0.42),
           (cx + w * 0.28, cy - h / 2), (cx + w / 2, cy - h * 0.06),
           (cx + w * 0.24, cy + h * 0.46), (cx - w * 0.3, cy + h / 2)]
    return smooth(pts)


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


BG_GRAD = lin(0, 0, 0, 1000, (0, "#161310"), (1, "#070604"))
PLATE_GRAD = rad((0, "#B9AC84"), (0.55, "#837A58"), (1, "#453F2C"))
COAT_GRAD = lin(380, 460, 700, 800, (0, "#9AA6B4"), (0.5, "#6E7A88"), (1, "#414C58"))
DIM_GRAD = lin(380, 460, 700, 800, (0, "#6E7A88"), (1, "#333C46"))
WHITE_GRAD = lin(300, 540, 500, 800, (0, "#F2EDE0"), (1, "#D2C8AE"))
COPPER = "#A86834"
FLOOR_GRAD = lin(0, 760, 0, 890, (0, "#6B6144"), (0.55, "#4C442E"), (1, "#262216"))

# --- backdrop + dusty gold plate -------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#3E3A26", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E4DCB8", strokeWidth=3, opacity=38)

# low sun pooling upper-left
d.shape("ellipse", "Light pool", x=250, y=150, width=400, height=230,
        fill="#F0E4B8", opacity=14, stroke=NONE)
# dust haze in thin lenses
for i, (x, y, w) in enumerate([(320, 330, 90), (565, 245, 70), (710, 360, 80),
                               (252, 470, 60), (748, 490, 64), (450, 195, 55)]):
    assert on_disc(x, y, 20), i
    d.shape("ellipse", f"Mist {i+1}", x=x - w / 2, y=y - w / 5, width=w, height=w * 0.4,
            fill="#EAE2C4", opacity=12, stroke=NONE)

# --- earthen floor, closing on the disc arc --------------------------------------
fy = 790
fl, fr = rim_x(fy, -1), rim_x(fy, 1)
d.path(f"M{fl:.1f},{fy} C300,778 400,800 500,790 C600,780 700,786 {fr:.1f},{fy} "
       f"A{PR},{PR} 0 0 1 {fl:.1f},{fy} Z", "Floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{fl + 8:.0f},{fy} C300,778 400,800 500,790 C600,780 700,786 {fr - 8:.0f},{fy}",
       "Floor crest", fill=NONE, stroke="#9E945F", strokeWidth=5, opacity=42, cap="round")
# dry-grass ticks rooted on the crest
for i, (x, y) in enumerate([(340, 812), (445, 832), (560, 838), (660, 822)]):
    assert on_disc(x, y - 8, 16), i
    for j, (dx, dy) in enumerate([(-8, 8), (0, -10), (8, 6)]):
        d.path(f"M{x:.0f},{y + 10} L{x + dx:.0f},{y + dy:.0f}",
               f"Grass {i+1}.{j+1}", fill=NONE, stroke="#8A7C46",
               strokeWidth=3.5, opacity=62, cap="round")

# soft shadow under the trotting dog
d.shape("ellipse", "Dog shadow", x=290, y=762, width=420, height=30,
        fill="#14110A", opacity=32, stroke=NONE)

# --- the aussie, working trot facing left ------------------------------------------
# bobtail — the natural stub, a short wedge off the rump
d.path(smooth([(678, 606), (712, 610), (732, 624), (734, 644), (720, 656),
               (700, 648), (684, 632), (676, 616)]),
       "Bobtail", fill=lin(680, 600, 735, 650, (0, "#8A96A4"), (1, "#4A545E")),
       stroke=INK, strokeWidth=4.5)

# hind legs — trot diagonal: far hind reaching under, near hind driving back
d.path(smooth([(608, 650), (596, 690), (580, 728), (558, 758), (542, 780),
               (546, 794), (570, 792), (594, 772), (616, 740), (630, 704),
               (634, 672)]),
       "Hind leg far", fill=DIM_GRAD, stroke=INK, strokeWidth=4.5)
d.path(smooth([(648, 644), (664, 686), (676, 722), (682, 752), (676, 776),
               (686, 790), (708, 788), (722, 770), (724, 738), (716, 702),
               (698, 672), (674, 652)]),
       "Hind leg near", fill=COAT_GRAD, stroke=INK, strokeWidth=5)
# hind feet — copper pastern above the cream sock on the near leg
d.path("M540,780 C528,786 524,794 532,800 C546,804 566,800 574,790 "
       "C572,780 554,774 540,780 Z", "Hind paw far", fill=DIM_GRAD,
       stroke=INK, strokeWidth=3.5)
d.path("M682,778 C670,784 666,792 674,798 C688,802 708,798 716,788 "
       "C714,778 696,772 682,778 Z", "Hind sock near", fill=WHITE_GRAD,
       stroke=INK, strokeWidth=4)
d.path("M678,758 C690,754 706,758 712,768 C702,772 688,772 680,768 Z",
       "Hind copper", fill=COPPER, opacity=80, stroke=NONE)

# body — medium, deep chest, level back, double-coat fullness
d.path(smooth([(392, 592), (366, 622), (360, 660), (376, 698), (414, 722),
               (480, 732), (570, 728), (640, 706), (676, 676), (690, 640),
               (676, 610), (634, 596), (566, 588), (480, 586), (424, 588)]),
       "Body", fill=COAT_GRAD, stroke=INK, strokeWidth=6)
# topline sheen
d.path("M420,592 C500,582 590,586 660,606", "Back sheen", fill=NONE,
       stroke="#D8DEE4", strokeWidth=5, opacity=40, cap="round")
# merle marbling over the barrel — lumpy slate patches, varied, no symmetry
for i, (cx, cy, w, h) in enumerate([(430, 630, 52, 40), (496, 602, 62, 46),
                                    (556, 646, 44, 36), (616, 612, 56, 44),
                                    (566, 698, 40, 32), (652, 662, 36, 28),
                                    (462, 676, 36, 30), (512, 706, 30, 24),
                                    (606, 584, 34, 26), (678, 630, 26, 22),
                                    (390, 640, 30, 26)]):
    d.path(merle(cx, cy, w, h), f"Merle {i+1}", fill=MERLE,
           stroke=NONE, opacity=85)

# front legs — near fore reaching forward-down, far fore planted vertical
d.path(smooth([(424, 660), (420, 700), (418, 736), (416, 764), (412, 784),
               (420, 796), (444, 794), (458, 776), (464, 742), (466, 706),
               (464, 678)]),
       "Front leg far", fill=DIM_GRAD, stroke=INK, strokeWidth=4.5)
d.path(smooth([(446, 656), (432, 696), (414, 734), (392, 764), (374, 786),
               (380, 800), (408, 798), (434, 778), (456, 744), (468, 708),
               (472, 676)]),
       "Front leg near", fill=COAT_GRAD, stroke=INK, strokeWidth=5)
# merle on the reaching foreleg
d.path(merle(434, 700, 28, 24), "Merle foreleg", fill=MERLE, stroke=NONE, opacity=85)
# cream sock + copper pastern on the near fore
d.path("M374,784 C360,790 356,798 364,804 C380,808 402,804 410,794 "
       "C408,784 388,778 374,784 Z", "Front sock near", fill=WHITE_GRAD,
       stroke=INK, strokeWidth=4)
d.path("M410,782 C398,788 394,796 402,802 C416,806 436,802 444,792 "
       "C442,782 424,776 410,782 Z", "Front paw far", fill=DIM_GRAD,
       stroke=INK, strokeWidth=3.5)
d.path("M386,760 C398,754 414,756 422,766 C412,772 396,772 388,768 Z",
       "Front copper", fill=COPPER, opacity=80, stroke=NONE)

# neck — ruffed arch off the withers into the lifted head
d.path(smooth([(404, 596), (380, 566), (360, 536), (348, 508), (352, 484),
               (370, 472), (394, 480), (412, 504), (424, 536), (430, 570),
               (428, 598)]),
       "Neck", fill=COAT_GRAD, stroke=INK, strokeWidth=5)
# cream collar — the white wrapping the front of the neck into the chest
d.path(smooth([(360, 522), (372, 560), (382, 604), (392, 652), (402, 694),
               (388, 704), (368, 680), (354, 630), (346, 578), (348, 540)]),
       "Collar bib", fill=WHITE_GRAD, opacity=92, stroke=NONE)
d.path(merle(408, 524, 26, 22), "Merle neck", fill=MERLE, stroke=NONE, opacity=85)

# head — clean wedge muzzle carried level, alert ahead; cream blaze
d.path(smooth([(360, 468), (332, 458), (304, 460), (282, 470), (264, 484),
               (256, 498), (262, 512), (282, 524), (312, 532), (344, 530),
               (368, 516), (376, 492), (372, 474)]),
       "Skull + muzzle", fill=COAT_GRAD, stroke=INK, strokeWidth=5)
# the blaze — narrow off the forehead, widening over the muzzle front
d.path(smooth([(316, 464), (330, 464), (332, 484), (322, 502), (300, 518),
               (280, 526), (266, 522), (262, 508), (272, 490), (294, 474)]),
       "Blaze + muzzle front", fill=WHITE_GRAD, opacity=95, stroke=NONE)
# merle patch on the skull
d.path(merle(352, 480, 22, 18), "Merle skull", fill=MERLE, stroke=NONE, opacity=85)
# copper cheek + brow point
d.path("M300,500 C314,494 332,496 340,506 C330,516 310,516 300,510 Z",
       "Cheek copper", fill=COPPER, opacity=80, stroke=NONE)
d.path("M330,452 C338,446 348,446 354,452 C348,458 336,458 330,452 Z",
       "Brow copper", fill=COPPER, opacity=85, stroke=NONE)

# ears — near ear pricked with the tip folded forward-down inside the
# base silhouette; far ear erect, set a step behind
d.path("M342,470 L318,392 L384,446 Z", "Ear near base", fill=COAT_GRAD,
       stroke=INK, strokeWidth=4.5)
d.path("M318,392 L298,424 L342,440 Z", "Ear near fold", fill=DIM_GRAD,
       stroke=INK, strokeWidth=4)
d.path("M380,466 L400,396 L420,458 Z", "Ear far", fill=DIM_GRAD,
       stroke=INK, strokeWidth=4)

# eye — dark almond, working gaze ahead
d.path("M300,478 C310,470 324,470 332,478 C328,488 314,492 304,488 "
       "C296,484 294,482 300,478 Z", "Eye",
       fill=rad((0, "#7A5228"), (0.7, "#462E12"), (1, "#221204")),
       stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Pupil", x=312, y=477, width=9, height=10, fill="#0E0806", stroke=NONE)
d.shape("ellipse", "Glint", x=315, y=479, width=4.5, height=4.5, fill="#FFF4D8",
        opacity=90, stroke=NONE)
# nose
d.path("M258,494 C248,496 244,504 248,512 C254,518 266,516 270,508 "
       "C270,500 266,494 258,494 Z", "Nose", fill="#17100C",
       stroke=INK, strokeWidth=3)
d.path("M252,504 C256,500 262,499 266,501", "Nose sheen", fill=NONE,
       stroke="#5E5046", strokeWidth=2.5, opacity=70, cap="round")

# double-coat texture — feathering ticks on chest, belly and thigh
for i, dd in enumerate(["M362,650 C356,662 354,674 358,686",
                        "M386,680 C382,692 382,702 388,712",
                        "M540,724 C544,734 544,744 540,752",
                        "M590,714 C596,724 596,734 592,742",
                        "M650,690 C658,698 660,708 656,716"]):
    d.path(dd, f"Fur {i+1}", fill=NONE, stroke="#333C46",
           strokeWidth=3.5, opacity=50, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#3A3624", strokeWidth=6)

# --- captions -------------------------------------------------------------------
d.text("AUSTRALIAN SHEPHERD", "Name", x=500, y=934, size=56, font="Virelai Sans",
       color="#EEEADB", justify="center")
LINE2, SZ2, TRK = "HERDING · UNITED STATES", 22, 280
r = d.text(LINE2, "Milestone", x=500, y=970, size=SZ2, font="Virelai Sans",
           color="#C4BCA0", justify="center")
d.cmd("text.setStyle", "Milestone tracking", id=r["id"], tracking=TRK)

b = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("milestone bounds", {k: round(v) for k, v in b.items()})
nearest = (min(max(PCX, b["x"]), b["x"] + b["width"]),
           min(max(PCY, b["y"]), b["y"] + b["height"]))
clear = math.hypot(nearest[0] - PCX, nearest[1] - PCY) - (PR + 3)
print("clears rim by %.1f" % clear)
assert clear > 0 and b["width"] <= 760 and b["x"] >= 10 and b["x"] + b["width"] <= 990, b

d.finish("australian-shepherd-V1R00")
