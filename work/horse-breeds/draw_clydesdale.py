#!/usr/bin/env python3
"""Clydesdale — milestone card V1R00. The heavy horse standing square:
massive bay body, broad white blaze covering the face front, four white
stockings ending in layered feather that bells over the hooves (strands
>=3pt where they thin). Thick arched neck, deep chest, calm weight —
the draught breed carries mass, not gait. Peat-moor disc, heather tufts
on a floor that closes on the disc's own arc. 1000x1000. House style:
gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Clydesdale — Milestone Card", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#231A14"                    # warm dark ink, never pure black


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


BG_GRAD = lin(0, 0, 0, 1000, (0, "#161512"), (1, "#080705"))
PLATE_GRAD = rad((0, "#B4A684"), (0.55, "#7E7258"), (1, "#413A2C"))
COAT_GRAD = lin(360, 380, 720, 800, (0, "#9A6240"), (0.5, "#5E3A22"), (1, "#2A1810"))
DIM_GRAD = lin(360, 380, 720, 800, (0, "#5E3E24"), (1, "#1C100A"))
WHITE_GRAD = lin(300, 400, 560, 800, (0, "#F4EDDC"), (1, "#D9CBAE"))
HAIR_GRAD = lin(660, 540, 740, 700, (0, "#2A1C14"), (1, "#120B08"))
FLOOR_GRAD = lin(0, 730, 0, 880, (0, "#5C563C"), (0.55, "#413F2B"), (1, "#221F13"))

# --- backdrop + peat-moor plate -------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#332D20", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#EDE6C8", strokeWidth=3, opacity=38)

# low light pooling upper-left
d.shape("ellipse", "Light pool", x=245, y=150, width=400, height=230,
        fill="#EFE8C8", opacity=12, stroke=NONE)
# moor mist lenses
for i, (x, y, w) in enumerate([(320, 330, 90), (565, 245, 70), (715, 365, 80),
                               (250, 475, 60), (755, 495, 64), (455, 195, 55)]):
    assert on_disc(x, y, 20), i
    d.shape("ellipse", f"Mist {i+1}", x=x - w / 2, y=y - w / 5, width=w, height=w * 0.4,
            fill="#E4E0C4", opacity=11, stroke=NONE)

# --- peat floor, closing on the disc arc ----------------------------------------
fy = 780
fl, fr = rim_x(fy, -1), rim_x(fy, 1)
d.path(f"M{fl:.1f},{fy} C300,768 400,790 500,780 C600,770 700,776 {fr:.1f},{fy} "
       f"A{PR},{PR} 0 0 1 {fl:.1f},{fy} Z", "Floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{fl + 8:.0f},{fy} C300,768 400,790 500,780 C600,770 700,776 {fr - 8:.0f},{fy}",
       "Floor crest", fill=NONE, stroke="#A89C6C", strokeWidth=5, opacity=40, cap="round")
# heather tufts rooted on the crest
for i, (x, y) in enumerate([(335, 802), (415, 830), (545, 838), (635, 824), (692, 800)]):
    assert on_disc(x, y + 8, 14), i
    for j, (dx, dy) in enumerate([(-13, 9), (-6, -5), (2, -11), (11, -2), (16, 8)]):
        d.path(f"M{x + dx * 0.4:.0f},{y + 13} L{x + dx:.0f},{y + dy:.0f}",
               f"Heather {i+1}.{j+1}", fill=NONE, stroke="#6E5E70",
               strokeWidth=3.5, opacity=70, cap="round")
    d.shape("ellipse", f"Heather bloom {i+1}", x=x - 6, y=y - 6, width=10, height=8,
            fill="#8A7490", opacity=55, stroke=NONE)

# soft shadow under the standing horse
d.shape("ellipse", "Horse shadow", x=295, y=764, width=420, height=30,
        fill="#151106", opacity=34, stroke=NONE)

# --- the clydesdale, standing square facing left ---------------------------------
# tail — heavy natural switch hanging from the dock
d.path(smooth([(686, 556), (706, 580), (714, 620), (712, 656), (702, 682),
               (690, 690), (680, 676), (678, 640), (678, 600), (676, 575)]),
       "Tail", fill=HAIR_GRAD, stroke=INK, strokeWidth=5)
for i, dd in enumerate(["M692,575 C700,610 702,645 698,674",
                        "M686,570 C692,602 694,638 690,668"]):
    d.path(dd, f"Tail strand {i+1}", fill=NONE, stroke="#4A382A",
           strokeWidth=3.5, opacity=50, cap="round")

# legs before the body — thick draught columns; stockings + feather cover below
d.path(smooth([(428, 650), (434, 700), (431, 742), (428, 770), (434, 784),
               (420, 788), (410, 780), (410, 744), (414, 706), (418, 662)]),
       "Front leg far", fill=DIM_GRAD, stroke=INK, strokeWidth=4.5)
d.path(smooth([(462, 650), (468, 698), (465, 740), (462, 768), (468, 784),
               (454, 790), (442, 782), (440, 744), (442, 706), (444, 664)]),
       "Front leg near", fill=COAT_GRAD, stroke=INK, strokeWidth=5)
d.path(smooth([(608, 650), (630, 672), (636, 710), (626, 744), (618, 772),
               (624, 786), (608, 790), (596, 778), (592, 742), (598, 706),
               (594, 668)]),
       "Hind leg far", fill=DIM_GRAD, stroke=INK, strokeWidth=4.5)
d.path(smooth([(646, 644), (672, 666), (680, 706), (670, 742), (660, 772),
               (666, 788), (650, 792), (636, 780), (632, 744), (638, 706),
               (630, 664)]),
       "Hind leg near", fill=COAT_GRAD, stroke=INK, strokeWidth=5)

# one silhouette: big straight profile -> poll -> thick crest -> high
# withers -> level back -> round quarter -> deep barrel -> broad chest ->
# throatlatch -> heavy jaw -> muzzle
d.path(smooth([(290, 480), (300, 468), (316, 450), (330, 430), (348, 412),
               (368, 398), (392, 404), (432, 448), (472, 505), (492, 538),
               (575, 548), (672, 556), (704, 586), (710, 632), (688, 664),
               (652, 682), (558, 700), (470, 688), (422, 660), (402, 622),
               (404, 594), (385, 548), (372, 505), (362, 498), (336, 502),
               (312, 496), (296, 490)]),
       "Horse", fill=COAT_GRAD, stroke=INK, strokeWidth=6)

# muscle shading kept at the silhouette edges — mass, not gait
d.path("M500,540 C568,534 634,540 690,558 C630,544 566,540 500,540 Z",
       "Topline sheen", fill="#C09060", opacity=38, stroke=NONE)
d.path("M702,592 C708,622 702,648 684,664 C696,642 700,614 702,592 Z",
       "Quarter shade", fill="#1E1410", opacity=30, stroke=NONE)
d.path("M500,688 C552,696 610,694 650,684 C612,702 552,704 504,696 Z",
       "Barrel shade", fill="#1E1410", opacity=25, stroke=NONE)
d.path("M394,404 C428,426 458,470 482,516", "Crest sheen", fill=NONE,
       stroke="#C09062", strokeWidth=4, opacity=40, cap="round")
# throatlatch shadow under the heavy jaw
d.path("M368,500 C380,486 388,466 388,444 C393,470 387,494 375,508 Z",
       "Throatlatch", fill="#1E1410", opacity=35, stroke=NONE)

# the blaze — broad white covering the face front from brow to muzzle
d.path(smooth([(344, 406), (352, 418), (350, 436), (338, 454), (322, 468),
               (310, 478), (298, 486), (289, 481), (295, 465), (306, 449),
               (318, 431), (330, 414), (338, 404)]),
       "Blaze", fill=WHITE_GRAD, opacity=95, stroke=NONE)

# white stockings — covers cannon to fetlock on all four
d.path("M440,700 C450,696 462,696 468,702 C470,730 472,760 470,786 "
       "C460,792 444,792 436,786 C436,758 438,728 440,700 Z",
       "Stocking fore near", fill=WHITE_GRAD, stroke=INK, strokeWidth=3.5)
d.path("M412,700 C420,696 430,696 434,702 C436,730 438,758 436,782 "
       "C428,788 416,788 410,782 C409,754 410,726 412,700 Z",
       "Stocking fore far", fill=WHITE_GRAD, opacity=85, stroke=INK, strokeWidth=3)
d.path("M632,700 C644,696 660,696 668,702 C668,732 666,760 664,786 "
       "C654,792 640,792 630,786 C628,758 628,728 632,700 Z",
       "Stocking hind near", fill=WHITE_GRAD, stroke=INK, strokeWidth=3.5)
d.path("M594,700 C604,696 616,696 622,702 C624,730 626,758 624,782 "
       "C616,788 604,788 596,782 C594,754 594,726 594,700 Z",
       "Stocking hind far", fill=WHITE_GRAD, opacity=85, stroke=INK, strokeWidth=3)

# the feather — layered cream strands belling over each hoof
for i, cx in enumerate([452, 420, 650, 606]):
    fyy = 790
    d.path(f"M{cx - 22},{fyy - 34} C{cx - 27},{fyy - 20} {cx - 25},{fyy - 6} {cx - 16},{fyy + 2} "
           f"C{cx},{fyy + 9} {cx + 16},{fyy + 5} {cx + 22},{fyy - 5} "
           f"C{cx + 27},{fyy - 16} {cx + 22},{fyy - 28} {cx + 14},{fyy - 36} Z",
           f"Feather skirt {i+1}", fill=WHITE_GRAD, stroke=INK, strokeWidth=3)
    for j, dx in enumerate([-14, -5, 4, 13]):
        d.path(f"M{cx + dx},{fyy - 30} C{cx + dx - 3},{fyy - 20} {cx + dx - 1},{fyy - 8} {cx + dx - 4},{fyy + 2}",
               f"Feather strand {i+1}.{j+1}", fill=NONE, stroke="#C8B898",
               strokeWidth=3.5, opacity=80, cap="round")
    # dark hoof edge under the feather
    d.path(f"M{cx - 14},{fyy - 2} C{cx},{fyy + 5} {cx + 14},{fyy - 2} {cx + 10},{fyy + 5} "
           f"C{cx},{fyy + 8} {cx - 10},{fyy + 5} {cx - 14},{fyy - 2} Z",
           f"Hoof {i+1}", fill="#150D09", stroke=NONE)

# mane — thick draught mane, slightly wavy along the crest
d.path(smooth([(392, 398), (428, 432), (470, 492), (496, 536), (506, 552),
               (486, 544), (448, 494), (414, 444), (390, 404)]),
       "Mane", fill=HAIR_GRAD, stroke=INK, strokeWidth=4)
for i, dd in enumerate(["M414,438 C444,478 470,516 492,544",
                        "M404,428 C432,466 458,508 482,538"]):
    d.path(dd, f"Mane strand {i+1}", fill=NONE, stroke="#0E0806",
           strokeWidth=3, opacity=45, cap="round")

# ears — broad, tipped forward, calm
d.path("M356,396 L366,346 L390,386 Z", "Ear near", fill=COAT_GRAD,
       stroke=INK, strokeWidth=4)
d.path("M382,388 L400,352 L402,382 Z", "Ear far", fill=DIM_GRAD,
       stroke=INK, strokeWidth=3.5)
d.path("M364,388 L368,360", "Ear inner", fill=NONE, stroke="#0F0A08",
       strokeWidth=3, opacity=55, cap="round")

# forelock over the poll
d.path("M370,392 C361,398 355,409 353,421 C362,413 371,404 379,400 Z",
       "Forelock", fill=HAIR_GRAD, stroke=NONE)
# forehead sheen above the blaze
d.shape("ellipse", "Forehead sheen", x=344, y=400, width=26, height=18,
        fill="#C09062", opacity=30, stroke=NONE)

# eye — calm, heavy-lidded
d.path("M340,438 C348,430 362,430 368,438 C366,450 352,454 344,448 "
       "C339,444 338,442 340,438 Z", "Eye",
       fill=rad((0, "#6E4A24"), (0.7, "#422A12"), (1, "#1E1208")),
       stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Pupil", x=348, y=436, width=9, height=10, fill="#0E0806", stroke=NONE)
d.shape("ellipse", "Glint", x=350, y=437, width=4.5, height=4.5, fill="#FFF4D8", opacity=90, stroke=NONE)
d.path("M336,424 C350,418 364,418 374,424", "Brow", fill=NONE,
       stroke="#241812", strokeWidth=4, opacity=55, cap="round")

# nostril — big, soft
d.path("M292,468 C286,473 286,482 293,485 C301,487 306,481 304,474 "
       "C301,467 295,465 292,468 Z", "Nostril", fill="#120B07",
       stroke=INK, strokeWidth=3)
d.path("M291,475 C295,471 301,471 304,474", "Nostril sheen", fill=NONE,
       stroke="#8A705A", strokeWidth=2.5, opacity=70, cap="round")
# mouth under the white muzzle
d.path("M300,488 C312,492 324,494 336,493", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=3, opacity=75, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#2E2A1E", strokeWidth=6)

# --- captions -------------------------------------------------------------------
d.text("CLYDESDALE", "Name", x=500, y=934, size=56, font="Virelai Sans",
       color="#EFE6C4", justify="center")
LINE2, SZ2, TRK = "DRAFT · SCOTLAND", 22, 280
r = d.text(LINE2, "Milestone", x=500, y=970, size=SZ2, font="Virelai Sans",
           color="#C8BFA0", justify="center")
d.cmd("text.setStyle", "Milestone tracking", id=r["id"], tracking=TRK)

b = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("milestone bounds", {k: round(v) for k, v in b.items()})
nearest = (min(max(PCX, b["x"]), b["x"] + b["width"]),
           min(max(PCY, b["y"]), b["y"] + b["height"]))
clear = math.hypot(nearest[0] - PCX, nearest[1] - PCY) - (PR + 3)
print("clears rim by %.1f" % clear)
assert clear > 0 and b["width"] <= 760 and b["x"] >= 10 and b["x"] + b["width"] <= 990, b

d.finish("clydesdale-V1R00")
