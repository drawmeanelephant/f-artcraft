#!/usr/bin/env python3
"""Thoroughbred — milestone card V1R00. The lean bay athlete at extended
canter: near fore leading low and forward, far fore trailing, hinds
staggered with the near leg driving off behind. Long flat muscles, thin
coat with a satin sheen, dark points on the lower legs. Tail streaming
back level with the spine. Turf-green dusk disc, grass floor closing on
the disc's own arc. 1000x1000. House style: gradients + translucent
shading, never flat fills. Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Thoroughbred — Milestone Card", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#201812"                    # warm dark ink, never pure black


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


BG_GRAD = lin(0, 0, 0, 1000, (0, "#0E1418"), (1, "#06090B"))
PLATE_GRAD = rad((0, "#A0AC8E"), (0.55, "#60725A"), (1, "#2E4034"))
COAT_GRAD = lin(300, 380, 720, 800, (0, "#8A5C3C"), (0.5, "#563821"), (1, "#241510"))
DIM_GRAD = lin(300, 380, 720, 800, (0, "#54371F"), (1, "#180E08"))
HAIR_GRAD = lin(680, 540, 830, 600, (0, "#241812"), (1, "#100A06"))
FLOOR_GRAD = lin(0, 730, 0, 880, (0, "#5A6448"), (0.55, "#3E4A34"), (1, "#1E2818"))

# --- backdrop + turf-dusk plate --------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#26342A", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E2E8CE", strokeWidth=3, opacity=38)

# thin dusk light pooling upper-left
d.shape("ellipse", "Light pool", x=245, y=150, width=400, height=230,
        fill="#ECEECB", opacity=12, stroke=NONE)
# turf mist drifting in thin lenses
for i, (x, y, w) in enumerate([(320, 330, 90), (565, 245, 70), (715, 365, 80),
                               (250, 475, 60), (760, 500, 64), (455, 195, 55)]):
    assert on_disc(x, y, 20), i
    d.shape("ellipse", f"Mist {i+1}", x=x - w / 2, y=y - w / 5, width=w, height=w * 0.4,
            fill="#DDE4C6", opacity=10, stroke=NONE)

# --- turf floor, closing on the disc arc -----------------------------------------
fy = 780
fl, fr = rim_x(fy, -1), rim_x(fy, 1)
d.path(f"M{fl:.1f},{fy} C300,768 400,790 500,780 C600,770 700,776 {fr:.1f},{fy} "
       f"A{PR},{PR} 0 0 1 {fl:.1f},{fy} Z", "Floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{fl + 8:.0f},{fy} C300,768 400,790 500,780 C600,770 700,776 {fr - 8:.0f},{fy}",
       "Floor crest", fill=NONE, stroke="#A8B288", strokeWidth=5, opacity=40, cap="round")
# mown turf bands below the crest
d.path("M300,818 C410,806 545,804 700,814", "Turf line 1", fill=NONE,
       stroke="#323E28", strokeWidth=4, opacity=45, cap="round")
d.path("M355,843 C460,834 580,832 665,838", "Turf line 2", fill=NONE,
       stroke="#262E1C", strokeWidth=4, opacity=40, cap="round")
# kicked-up grass blades on the crest behind the driving hind
for i, (x, y) in enumerate([(690, 800), (716, 790), (340, 812), (400, 830), (540, 836)]):
    assert on_disc(x, y + 8, 14), i
    for j, (dx, dy) in enumerate([(-10, 6), (-3, -7), (5, -11), (13, -3)]):
        d.path(f"M{x + dx * 0.3:.0f},{y + 10} L{x + dx:.0f},{y + dy:.0f}",
               f"Blade {i+1}.{j+1}", fill=NONE, stroke="#7E8A5E",
               strokeWidth=3.5, opacity=65, cap="round")

# soft shadow under the cantering horse
d.shape("ellipse", "Horse shadow", x=290, y=766, width=430, height=28,
        fill="#0E1208", opacity=32, stroke=NONE)

# --- the thoroughbred, extended canter facing left --------------------------------
# tail first — streaming back level with the spine
d.path(smooth([(675, 548), (730, 538), (785, 546), (822, 564), (826, 584),
               (806, 596), (768, 592), (724, 580), (692, 572)]),
       "Tail", fill=HAIR_GRAD, stroke=INK, strokeWidth=5)
for i, dd in enumerate(["M694,562 C740,552 786,556 816,572",
                        "M700,572 C744,566 786,570 812,584"]):
    d.path(dd, f"Tail strand {i+1}", fill=NONE, stroke="#4A382A",
           strokeWidth=3.5, opacity=50, cap="round")

# legs before the body — tops hide under the silhouette
# near fore leads the canter: reaching low and forward
d.path(smooth([(442, 648), (452, 688), (430, 730), (402, 766), (380, 788),
               (368, 797), (356, 789), (368, 770), (396, 738), (424, 700),
               (430, 660)]),
       "Front leg near", fill=COAT_GRAD, stroke=INK, strokeWidth=5)
# far fore trailing, slightly folded
d.path(smooth([(458, 648), (462, 692), (456, 728), (450, 760), (458, 772),
               (446, 778), (436, 770), (438, 738), (442, 700), (444, 660)]),
       "Front leg far", fill=DIM_GRAD, stroke=INK, strokeWidth=4.5)
# near hind driving off behind
d.path(smooth([(640, 645), (672, 672), (692, 712), (706, 752), (716, 784),
               (708, 793), (694, 790), (690, 760), (676, 722), (652, 682),
               (630, 660)]),
       "Hind leg near", fill=COAT_GRAD, stroke=INK, strokeWidth=5)
# far hind tucked under, hock low
d.path(smooth([(612, 648), (622, 690), (610, 738), (596, 772), (590, 790),
               (578, 792), (570, 782), (582, 750), (596, 712), (600, 672)]),
       "Hind leg far", fill=DIM_GRAD, stroke=INK, strokeWidth=4.5)
# bay's dark points — narrow shading down each cannon, kept inside the leg
for i, dd in enumerate(["M392,742 C382,758 372,772 366,784",
                        "M452,730 C448,744 446,756 448,768",
                        "M694,738 C700,752 706,768 710,780",
                        "M596,742 C590,756 585,770 582,782"]):
    d.path(dd, f"Point {i+1}", fill=NONE, stroke="#180F08",
           strokeWidth=9, opacity=45, cap="round")

# one silhouette: muzzle -> long flat face -> poll -> stretched crest ->
# withers -> back -> croup -> quarter -> tucked flank -> belly -> deep
# chest -> throatlatch -> jaw -> muzzle
d.path(smooth([(255, 478), (266, 466), (282, 452), (302, 432), (318, 414),
               (336, 398), (358, 404), (400, 438), (448, 492), (478, 522),
               (575, 532), (672, 548), (702, 578), (708, 620), (688, 652),
               (652, 668), (560, 680), (482, 672), (438, 650), (416, 616),
               (414, 590), (392, 538), (368, 496), (356, 488), (330, 492),
               (306, 490), (284, 488)]),
       "Horse", fill=COAT_GRAD, stroke=INK, strokeWidth=6)

# dark hoof + pastern caps
for i, (cx, cy) in enumerate([(368, 790), (448, 774), (712, 788), (580, 786)]):
    d.path(f"M{cx - 13},{cy - 9} C{cx - 6},{cy - 13} {cx + 7},{cy - 13} {cx + 13},{cy - 7} "
           f"C{cx + 11},{cy + 4} {cx - 9},{cy + 6} {cx - 13},{cy - 1} Z",
           f"Hoof {i+1}", fill="#150D09", stroke=INK, strokeWidth=3)

# satin sheen — long flat highlights along topline, shoulder, quarter
d.path("M480,524 C548,518 622,524 678,544 C618,528 548,524 480,524 Z",
       "Topline sheen", fill="#C89468", opacity=40, stroke=NONE)
d.path("M700,580 C706,610 700,636 682,652 C694,630 698,604 700,580 Z",
       "Quarter shade", fill="#1E1410", opacity=30, stroke=NONE)
d.path("M500,668 C548,676 606,674 646,664 C608,682 550,684 504,678 Z",
       "Barrel shade", fill="#1E1410", opacity=25, stroke=NONE)
d.path("M400,442 C430,466 458,496 478,526", "Crest sheen", fill=NONE,
       stroke="#C09062", strokeWidth=4, opacity=45, cap="round")
# long flat muscle planes — thigh and forearm
d.path("M648,656 C664,676 672,700 670,724 C658,700 650,678 646,658 Z",
       "Thigh plane", fill="#1E1410", opacity=25, stroke=NONE)
d.path("M440,656 C450,684 452,712 446,738 C438,712 436,684 438,658 Z",
       "Forearm plane", fill="#1E1410", opacity=25, stroke=NONE)
# throatlatch shadow
d.path("M362,492 C374,478 382,458 382,436 C387,462 381,486 369,500 Z",
       "Throatlatch", fill="#1E1410", opacity=35, stroke=NONE)

# mane — thin racer's band along the crest, combed flat
d.path(smooth([(360, 396), (398, 428), (444, 482), (478, 522), (488, 538),
               (470, 530), (430, 478), (392, 430), (360, 404)]),
       "Mane", fill=HAIR_GRAD, stroke=INK, strokeWidth=4)
for i, dd in enumerate(["M396,432 C428,468 456,506 478,538",
                        "M386,426 C416,460 444,498 468,534"]):
    d.path(dd, f"Mane strand {i+1}", fill=NONE, stroke="#0E0806",
           strokeWidth=3, opacity=45, cap="round")

# ears — pricked forward into the gallop
d.path("M342,398 L344,352 L372,384 Z", "Ear near", fill=COAT_GRAD,
       stroke=INK, strokeWidth=4)
d.path("M366,388 L384,352 L386,382 Z", "Ear far", fill=DIM_GRAD,
       stroke=INK, strokeWidth=3.5)
d.path("M350,388 L352,362", "Ear inner", fill=NONE, stroke="#0F0A08",
       strokeWidth=3, opacity=55, cap="round")

# forelock wisp
d.path("M356,396 C349,402 344,412 342,424 C350,416 358,406 366,400 Z",
       "Forelock", fill=HAIR_GRAD, stroke=NONE)
# forehead sheen
d.shape("ellipse", "Forehead sheen", x=322, y=402, width=26, height=18,
        fill="#C09062", opacity=35, stroke=NONE)

# eye — dark, focused forward
d.path("M330,432 C338,424 352,424 358,432 C356,444 342,448 334,442 "
       "C329,438 328,436 330,432 Z", "Eye",
       fill=rad((0, "#5E3C1C"), (0.7, "#38200E"), (1, "#1A0E06")),
       stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Pupil", x=338, y=430, width=9, height=10, fill="#0E0806", stroke=NONE)
d.shape("ellipse", "Glint", x=340, y=431, width=4.5, height=4.5, fill="#FFF4D8", opacity=90, stroke=NONE)
d.path("M324,418 C338,412 352,412 362,418", "Brow", fill=NONE,
       stroke="#241812", strokeWidth=4, opacity=55, cap="round")

# nostril — flared at the reaching muzzle
d.path("M262,468 C256,473 256,482 263,485 C271,487 276,481 274,474 "
       "C271,467 265,465 262,468 Z", "Nostril", fill="#120B07",
       stroke=INK, strokeWidth=3)
d.path("M261,475 C265,471 271,471 274,474", "Nostril sheen", fill=NONE,
       stroke="#8A705A", strokeWidth=2.5, opacity=70, cap="round")
# mouth line back along the jaw
d.path("M274,486 C290,490 310,492 330,490", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=3, opacity=75, cap="round")
# faint cheek line
d.path("M336,464 C350,468 364,466 374,458", "Cheek line", fill=NONE,
       stroke="#241812", strokeWidth=3, opacity=40, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#242E22", strokeWidth=6)

# --- captions -------------------------------------------------------------------
d.text("THOROUGHBRED", "Name", x=500, y=934, size=56, font="Virelai Sans",
       color="#E8EACC", justify="center")
LINE2, SZ2, TRK = "RACER · ENGLAND", 22, 280
r = d.text(LINE2, "Milestone", x=500, y=970, size=SZ2, font="Virelai Sans",
           color="#BEC4A8", justify="center")
d.cmd("text.setStyle", "Milestone tracking", id=r["id"], tracking=TRK)

b = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("milestone bounds", {k: round(v) for k, v in b.items()})
nearest = (min(max(PCX, b["x"]), b["x"] + b["width"]),
           min(max(PCY, b["y"]), b["y"] + b["height"]))
clear = math.hypot(nearest[0] - PCX, nearest[1] - PCY) - (PR + 3)
print("clears rim by %.1f" % clear)
assert clear > 0 and b["width"] <= 760 and b["x"] >= 10 and b["x"] + b["width"] <= 990, b

d.finish("thoroughbred-V1R00")
