#!/usr/bin/env python3
"""Greyhound — milestone card V1R00. The sprint specialist at the
double-suspension gallop: all four feet off the turf, front pair reaching,
hind pair driving back, the aerodynamic line unbroken nose to tail.
Deep chest, hard-tucked waist, rose ears folded flat, long fine whip of
a tail. Fawn on a cool teal-slate disc, flattened grass on the floor that
closes on the disc's arc. 1000x1000. House style: gradients + translucent
shading, never flat fills. Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Greyhound — Milestone Card", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#241C18"                    # warm dark ink, never pure black


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


BG_GRAD = lin(0, 0, 0, 1000, (0, "#0E1817"), (1, "#050A09"))
PLATE_GRAD = rad((0, "#93A8A0"), (0.55, "#5E7A72"), (1, "#2F443E"))
COAT_GRAD = lin(240, 500, 760, 720, (0, "#CBA46C"), (0.5, "#A87E48"), (1, "#6E4E26"))
DIM_GRAD = lin(240, 500, 760, 720, (0, "#96713E"), (1, "#4C3214"))
FLOOR_GRAD = lin(0, 760, 0, 890, (0, "#4E6058"), (0.55, "#35463E"), (1, "#1A2420"))

# --- backdrop + teal-slate plate -------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#263832", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8E2DA", strokeWidth=3, opacity=38)

# thin dusk light pooling upper-left
d.shape("ellipse", "Light pool", x=250, y=150, width=400, height=230,
        fill="#E4EADA", opacity=13, stroke=NONE)
# drifting mist lenses
for i, (x, y, w) in enumerate([(320, 330, 90), (565, 245, 70), (710, 360, 80),
                               (252, 470, 60), (748, 490, 64), (450, 195, 55)]):
    assert on_disc(x, y, 20), i
    d.shape("ellipse", f"Mist {i+1}", x=x - w / 2, y=y - w / 5, width=w, height=w * 0.4,
            fill="#DAE2DA", opacity=12, stroke=NONE)

# --- turf floor, closing on the disc arc -----------------------------------------
fy = 790
fl, fr = rim_x(fy, -1), rim_x(fy, 1)
d.path(f"M{fl:.1f},{fy} C300,778 400,800 500,790 C600,780 700,786 {fr:.1f},{fy} "
       f"A{PR},{PR} 0 0 1 {fl:.1f},{fy} Z", "Floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{fl + 8:.0f},{fy} C300,778 400,800 500,790 C600,780 700,786 {fr - 8:.0f},{fy}",
       "Floor crest", fill=NONE, stroke="#8CA094", strokeWidth=5, opacity=42, cap="round")
# grass flattened flat by the pace — horizontal ticks trailing on the crest
for i, (x, y) in enumerate([(350, 816), (470, 836), (580, 834), (676, 814)]):
    assert on_disc(x, y, 16), i
    d.path(f"M{x - 14:.0f},{y + 4} C{x - 4:.0f},{y - 2} {x + 8:.0f},{y - 3} {x + 16:.0f},{y + 1}",
           f"Flat grass {i+1}", fill=NONE, stroke="#7E8E60", strokeWidth=3.5,
           opacity=58, cap="round")

# air shadow — the dog is off the ground, the pool of shade stays low
d.shape("ellipse", "Dog shadow", x=300, y=764, width=400, height=24,
        fill="#0E120C", opacity=26, stroke=NONE)

# --- the greyhound, double suspension facing left ---------------------------------
# tail — the long fine whip off the rump, tapering to a point down-right
d.path(smooth([(676, 566), (712, 590), (746, 614), (776, 638), (794, 658),
               (788, 668), (766, 654), (734, 632), (702, 606), (676, 586)]),
       "Tail", fill=lin(680, 570, 795, 665, (0, "#B08A50"), (1, "#6E4E26")),
       stroke=INK, strokeWidth=4.5)

# hind legs — both driving back, near leg the deeper reach
d.path(smooth([(614, 566), (644, 600), (672, 636), (694, 664), (706, 686),
               (698, 696), (680, 690), (652, 664), (624, 630), (606, 594)]),
       "Hind leg far", fill=DIM_GRAD, stroke=INK, strokeWidth=4.5)
d.path(smooth([(644, 556), (676, 592), (710, 626), (738, 652), (758, 668),
               (754, 680), (732, 674), (700, 650), (668, 618), (640, 584)]),
       "Hind leg near", fill=COAT_GRAD, stroke=INK, strokeWidth=5)

# body — stretched level: deep brisket low, waist tucked up hard to the loin
d.path(smooth([(356, 540), (420, 514), (510, 506), (600, 514), (664, 538),
               (686, 568), (678, 596), (640, 610), (560, 600), (480, 612),
               (420, 640), (386, 646), (358, 616), (348, 580)]),
       "Body", fill=COAT_GRAD, stroke=INK, strokeWidth=6)
# topline sheen — cold light on the stretched back
d.path("M390,528 C470,510 570,508 648,534 C570,518 470,520 390,540 Z",
       "Back sheen", fill="#F0D8AC", opacity=32, stroke=NONE)
# the tuck — a shade wedge where the belly sweeps up to the loin
d.path("M470,606 C540,594 600,596 646,584 C604,612 540,620 474,616 Z",
       "Tuck shade", fill="#5C4018", opacity=45, stroke=NONE)
# rib arcs — the faintest suggestion under the skin
for i, dd in enumerate(["M500,540 C508,556 510,574 506,592",
                        "M530,538 C538,554 540,572 536,590"]):
    d.path(dd, f"Rib {i+1}", fill=NONE, stroke="#6E4E26",
           strokeWidth=3, opacity=40, cap="round")

# neck — the long reach forward under the head, laid down before the legs
# so its lower edge tucks under them
d.path(smooth([(342, 512), (368, 532), (396, 560), (424, 596), (430, 608),
               (414, 616), (392, 592), (366, 558), (344, 532), (336, 516)]),
       "Neck", fill=COAT_GRAD, stroke=INK, strokeWidth=5)

# front legs — both reaching forward, near leg the deeper reach
d.path(smooth([(448, 566), (438, 602), (420, 642), (400, 672), (384, 690),
               (390, 700), (408, 696), (430, 672), (450, 634), (460, 598)]),
       "Front leg far", fill=DIM_GRAD, stroke=INK, strokeWidth=4.5)
d.path(smooth([(424, 560), (408, 598), (384, 642), (356, 678), (334, 700),
               (340, 712), (360, 708), (386, 680), (412, 638), (432, 596)]),
       "Front leg near", fill=COAT_GRAD, stroke=INK, strokeWidth=5)
# paws — tapered ends, no bulk
d.path("M330,696 C320,700 316,708 322,714 C334,718 350,714 356,706 "
       "C354,698 342,692 330,696 Z", "Front paw near", fill=COAT_GRAD,
       stroke=INK, strokeWidth=4)
d.path("M378,684 C368,688 364,696 370,702 C382,706 398,702 404,694 "
       "C402,686 390,680 378,684 Z", "Front paw far", fill=DIM_GRAD,
       stroke=INK, strokeWidth=3.5)
d.path("M700,660 C692,666 690,674 696,680 C708,682 722,676 726,668 "
       "C722,660 710,656 700,660 Z", "Hind paw near", fill=COAT_GRAD,
       stroke=INK, strokeWidth=4)
d.path("M672,678 C664,682 662,690 668,696 C678,700 692,696 698,688 "
       "C696,680 682,674 672,678 Z", "Hind paw far", fill=DIM_GRAD,
       stroke=INK, strokeWidth=3.5)

# head — the long fine muzzle carried level, slight stop, rose ear flat
d.path(smooth([(332, 496), (304, 498), (272, 506), (244, 518), (222, 530),
               (216, 540), (226, 550), (252, 558), (288, 562), (318, 558),
               (340, 544), (346, 522), (344, 504)]),
       "Skull + muzzle", fill=COAT_GRAD, stroke=INK, strokeWidth=5)
# dark mask shade on the muzzle tip
d.path("M222,530 C214,534 212,542 218,548 C228,552 242,550 250,542 "
       "C248,534 234,528 222,530 Z", "Mask", fill="#6E4E26",
       stroke=NONE, opacity=70)
# nose
d.path("M218,532 C210,534 207,541 211,547 C217,551 227,549 230,543 "
       "C230,537 225,532 218,532 Z", "Nose", fill="#17100C",
       stroke=INK, strokeWidth=3)
# eye — small dark almond, gaze on the line
d.path("M290,518 C298,512 310,512 316,518 C312,526 300,529 292,526 "
       "C286,522 285,521 290,518 Z", "Eye",
       fill=rad((0, "#7A5228"), (0.7, "#462E12"), (1, "#221204")),
       stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Pupil", x=301, y=517, width=8, height=9, fill="#0E0806", stroke=NONE)
d.shape("ellipse", "Glint", x=303, y=518, width=4, height=4, fill="#FFF4D8",
        opacity=90, stroke=NONE)

# rose ears — small, folded back flat against the skull top
d.path("M336,500 L366,486 L356,510 Z", "Ear near", fill=COAT_GRAD,
       stroke=INK, strokeWidth=4)
d.path("M342,506 L362,496 L352,512 Z", "Ear near fold", fill=DIM_GRAD,
       stroke=NONE, opacity=90)
d.path("M346,494 L370,484 L362,502 Z", "Ear far", fill=DIM_GRAD,
       stroke=INK, strokeWidth=3.5)

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#22322C", strokeWidth=6)

# --- captions -------------------------------------------------------------------
d.text("GREYHOUND", "Name", x=500, y=934, size=56, font="Virelai Sans",
       color="#E4EAD9", justify="center")
LINE2, SZ2, TRK = "HOUND · ENGLAND", 22, 300
r = d.text(LINE2, "Milestone", x=500, y=970, size=SZ2, font="Virelai Sans",
           color="#B8C4B4", justify="center")
d.cmd("text.setStyle", "Milestone tracking", id=r["id"], tracking=TRK)

b = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("milestone bounds", {k: round(v) for k, v in b.items()})
nearest = (min(max(PCX, b["x"]), b["x"] + b["width"]),
           min(max(PCY, b["y"]), b["y"] + b["height"]))
clear = math.hypot(nearest[0] - PCX, nearest[1] - PCY) - (PR + 3)
print("clears rim by %.1f" % clear)
assert clear > 0 and b["width"] <= 760 and b["x"] >= 10 and b["x"] + b["width"] <= 990, b

d.finish("greyhound-V1R00")
