#!/usr/bin/env python3
"""Border collie — milestone card V1R00. The working crouch that defines
the breed: black-and-white, low in the stalking "eye" stance, head level
and stretched forward, gaze locked on the viewer as if we are the sheep.
White blaze, full white collar, rough coat, semi-pricked ears, tail
carried low with the tip just lifting. Muted moor-green disc, heather
tufts on a peat floor that closes on the disc's own arc. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Border Collie — Milestone Card", 1000, 1000)

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


BG_GRAD = lin(0, 0, 0, 1000, (0, "#141B12"), (1, "#070B06"))
PLATE_GRAD = rad((0, "#AEB88C"), (0.55, "#7D8D6A"), (1, "#43533E"))
COAT_GRAD = lin(380, 520, 660, 780, (0, "#463B34"), (0.5, "#2E2620"), (1, "#191210"))
DIM_GRAD = lin(380, 520, 660, 780, (0, "#332B26"), (1, "#140E0C"))
WHITE_GRAD = lin(300, 560, 500, 780, (0, "#F4EDDC"), (1, "#D9CBAE"))
FLOOR_GRAD = lin(0, 730, 0, 880, (0, "#5E5A3C"), (0.55, "#42402A"), (1, "#262415"))

# --- backdrop + moor plate -----------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#2E4028", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E2E4C4", strokeWidth=3, opacity=38)

# low dusk light pooling upper-left
d.shape("ellipse", "Light pool", x=240, y=150, width=400, height=230,
        fill="#EEE8C0", opacity=15, stroke=NONE)
# moor mist drifting in thin lenses
for i, (x, y, w) in enumerate([(320, 330, 90), (560, 250, 70), (700, 360, 80),
                               (250, 480, 60), (740, 500, 64), (450, 180, 55)]):
    assert on_disc(x, y, 20), i
    d.shape("ellipse", f"Mist {i+1}", x=x - w / 2, y=y - w / 5, width=w, height=w * 0.4,
            fill="#E8EAC8", opacity=12, stroke=NONE)

# --- peat floor, closing on the disc arc ---------------------------------------
fy = 780
fl, fr = rim_x(fy, -1), rim_x(fy, 1)
d.path(f"M{fl:.1f},{fy} C300,768 400,790 500,780 C600,770 700,776 {fr:.1f},{fy} "
       f"A{PR},{PR} 0 0 1 {fl:.1f},{fy} Z", "Floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{fl + 8:.0f},{fy} C300,768 400,790 500,780 C600,770 700,776 {fr - 8:.0f},{fy}",
       "Floor crest", fill=NONE, stroke="#9A9464", strokeWidth=5, opacity=42, cap="round")
# heather tufts — small clumps of muted purple ticks rooted on the crest
for i, (x, y) in enumerate([(330, 806), (400, 831), (520, 838), (612, 824), (668, 804)]):
    assert on_disc(x, y + 10, 14), i
    for j, (dx, dy) in enumerate([(-14, 10), (-6, -4), (2, -10), (10, -2), (16, 8)]):
        d.path(f"M{x + dx * 0.4:.0f},{y + 14} L{x + dx:.0f},{y + dy:.0f}",
               f"Heather {i+1}.{j+1}", fill=NONE, stroke="#6E5E70",
               strokeWidth=3.5, opacity=70, cap="round")
    d.shape("ellipse", f"Heather bloom {i+1}", x=x - 6, y=y - 6, width=10, height=8,
            fill="#8A7490", opacity=55, stroke=NONE)

# soft shadow the dog crouches over
d.shape("ellipse", "Dog shadow", x=300, y=752, width=420, height=34,
        fill="#171408", opacity=32, stroke=NONE)

# --- the collie, working crouch, head frontal on the stretched neck -------------
# tail — the low brush, sweeping down off the rump with the white tip lifting
d.path(smooth([(672, 610), (716, 626), (752, 656), (772, 688), (770, 714),
               (750, 722), (726, 704), (702, 676), (680, 646)]),
       "Tail", fill=lin(680, 610, 770, 720, (0, "#322A24"), (0.6, "#1C1410"), (1, "#2E2620")),
       stroke=INK, strokeWidth=5)
d.path(smooth([(748, 680), (770, 696), (772, 714), (756, 726), (736, 718),
               (734, 698)]),
       "Tail white tip", fill=WHITE_GRAD, stroke=INK, strokeWidth=3.5)
for i, dd in enumerate(["M694,644 C722,664 744,688 756,710",
                        "M686,658 C712,678 732,698 744,716"]):
    d.path(dd, f"Tail fur {i+1}", fill=NONE, stroke="#0F0A08",
           strokeWidth=4, opacity=45, cap="round")

# hind legs folded into the crouch — one hard bend at the hock
d.path(smooth([(560, 636), (600, 696), (628, 738), (652, 756), (646, 768),
               (616, 762), (586, 726), (548, 672), (540, 650)]),
       "Hind leg far", fill=DIM_GRAD, stroke=INK, strokeWidth=4.5)
d.path(smooth([(590, 626), (640, 686), (676, 734), (706, 750), (700, 766),
               (664, 762), (628, 722), (584, 668), (572, 644)]),
       "Hind leg near", fill=COAT_GRAD, stroke=INK, strokeWidth=5)
d.path("M676,748 C694,744 710,750 712,760 C706,770 686,772 676,764 "
       "C672,758 672,752 676,748 Z", "Hind paw near", fill=WHITE_GRAD,
       stroke=INK, strokeWidth=4)

# body — long low stalking line, back nearly level, belly hugging the ground
d.path(smooth([(400, 586), (470, 556), (560, 552), (640, 566), (692, 596),
               (700, 632), (664, 664), (580, 688), (480, 692), (420, 668),
               (392, 626)]),
       "Body", fill=COAT_GRAD, stroke=INK, strokeWidth=6)
# back sheen — thin cold light along the topline
d.path("M420,582 C490,556 580,552 650,570 C580,564 490,568 420,582 Z",
       "Back sheen", fill="#7A6E60", opacity=30, stroke=NONE)
# belly white fringe — the low edge between the legs
d.path("M470,680 C540,690 610,686 660,664 C630,692 540,700 480,690 "
       "C472,686 468,684 470,680 Z", "Belly white", fill=WHITE_GRAD, opacity=80, stroke=NONE)

# front legs — the creep: elbows bent, forearms reaching low and forward
d.path(smooth([(470, 646), (440, 700), (404, 740), (368, 760), (374, 772),
               (406, 768), (444, 734), (482, 690), (494, 658)]),
       "Front leg far", fill=DIM_GRAD, stroke=INK, strokeWidth=4.5)
d.path(smooth([(440, 632), (404, 696), (362, 742), (322, 762), (330, 776),
               (368, 770), (412, 728), (456, 682), (466, 646)]),
       "Front leg near", fill=COAT_GRAD, stroke=INK, strokeWidth=5)
# white front socks
d.path("M344,740 C326,750 312,762 316,772 C330,780 356,778 368,766 "
       "C372,754 360,742 344,740 Z", "Front sock near", fill=WHITE_GRAD,
       stroke=INK, strokeWidth=4)
d.path("M392,738 C380,746 372,756 376,766 C388,772 404,768 410,758 "
       "C410,748 402,738 392,738 Z", "Front sock far", fill=WHITE_GRAD,
       opacity=90, stroke=INK, strokeWidth=3.5)
# feathering on the back of the near foreleg
for i, dd in enumerate(["M448,662 C428,692 408,720 388,746",
                        "M458,680 C440,708 422,734 404,756",
                        "M436,646 C420,672 402,698 384,722"]):
    d.path(dd, f"Foreleg feather {i+1}", fill=NONE, stroke="#120C0A",
           strokeWidth=3.5, opacity=50, cap="round")

# neck — stretched forward and low off the withers into the back of the skull
d.path(smooth([(420, 636), (396, 614), (376, 596), (362, 582), (356, 566),
               (368, 558), (388, 568), (408, 590), (424, 616), (430, 640)]),
       "Neck", fill=COAT_GRAD, stroke=INK, strokeWidth=5)
# white throat running under the jaw into the chest bib
d.path(smooth([(352, 646), (384, 652), (414, 662), (426, 684), (414, 708),
               (388, 720), (356, 716), (336, 696), (334, 668)]),
       "Throat + bib", fill=WHITE_GRAD, stroke=INK, strokeWidth=3.5)

# skull — frontal, broad between the ears, tapering to the chin
d.path(smooth([(352, 538), (392, 544), (416, 568), (424, 604), (414, 642),
               (392, 672), (364, 690), (336, 690), (310, 672), (294, 642),
               (288, 604), (296, 568), (318, 546)]),
       "Skull", fill=COAT_GRAD, stroke=INK, strokeWidth=5)
# the blaze — narrow off the forehead, widening to cover the whole muzzle front
d.path(smooth([(342, 548), (362, 548), (370, 576), (382, 606), (388, 636),
               (386, 668), (370, 690), (348, 694), (326, 690), (314, 668),
               (316, 636), (324, 606), (334, 576)]),
       "Blaze + muzzle", fill=WHITE_GRAD, opacity=95, stroke=NONE)

# semi-pricked ears — short erect triangles, the top third folded inward-down
d.path("M318,556 L286,478 L346,522 Z", "Ear L base", fill=COAT_GRAD,
       stroke=INK, strokeWidth=4.5)
d.path("M286,478 L322,492 L300,520 Z", "Ear L fold", fill=DIM_GRAD,
       stroke=INK, strokeWidth=4)
d.path("M388,552 L420,476 L362,522 Z", "Ear R base", fill=COAT_GRAD,
       stroke=INK, strokeWidth=4.5)
d.path("M420,476 L384,490 L406,518 Z", "Ear R fold", fill=DIM_GRAD,
       stroke=INK, strokeWidth=4)
d.path("M310,540 L298,496", "Ear inner L", fill=NONE, stroke="#0F0A08",
       strokeWidth=3.5, opacity=55, cap="round")
d.path("M394,538 L408,494", "Ear inner R", fill=NONE, stroke="#0F0A08",
       strokeWidth=3.5, opacity=55, cap="round")

# the eye — the famous stare: two dark almonds levelled at the viewer
d.path("M310,596 C318,586 332,584 340,592 C338,604 324,610 314,606 "
       "C308,602 306,600 310,596 Z", "Eye L",
       fill=rad((0, "#8A6434"), (0.7, "#543A1C"), (1, "#2E1E0E")),
       stroke=INK, strokeWidth=3.5)
d.path("M368,594 C376,584 390,584 398,592 C396,604 382,608 372,604 "
       "C366,600 364,598 368,594 Z", "Eye R",
       fill=rad((0, "#8A6434"), (0.7, "#543A1C"), (1, "#2E1E0E")),
       stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Pupil L", x=321, y=593, width=10, height=11, fill="#0E0806", stroke=NONE)
d.shape("ellipse", "Pupil R", x=379, y=591, width=10, height=11, fill="#0E0806", stroke=NONE)
d.shape("ellipse", "Glint L", x=324, y=595, width=4.5, height=4.5, fill="#FFF4D8", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=382, y=593, width=4.5, height=4.5, fill="#FFF4D8", opacity=90, stroke=NONE)
# brow shading — the hard stare comes from under the brows
d.path("M306,580 C320,578 334,582 344,588", "Brow L", fill=NONE,
       stroke="#0F0A08", strokeWidth=4, opacity=55, cap="round")
d.path("M402,578 C388,576 374,580 364,586", "Brow R", fill=NONE,
       stroke="#0F0A08", strokeWidth=4, opacity=55, cap="round")

# nose — black on the white muzzle tip
d.path("M336,668 C324,668 316,676 320,686 C326,694 342,694 350,686 "
       "C354,676 348,668 336,668 Z", "Nose", fill="#17100C",
       stroke=INK, strokeWidth=3)
d.path("M326,676 C332,672 342,672 348,676", "Nose sheen", fill=NONE,
       stroke="#5E5046", strokeWidth=2.5, opacity=70, cap="round")
# level mouth under the nose — the quiet stare, no smile
d.path("M324,696 C334,700 346,700 356,694", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=3.5, cap="round")

# rough-coat texture — guard-hair ticks along the hackles and chest fringe
for i, dd in enumerate(["M430,572 C436,562 442,556 448,552",
                        "M470,560 C476,550 482,544 490,540",
                        "M516,556 C522,546 530,540 538,538",
                        "M564,556 C572,548 580,544 588,542",
                        "M614,562 C622,556 630,552 638,552"]):
    d.path(dd, f"Hackle {i+1}", fill=NONE, stroke="#100B08",
           strokeWidth=3.5, opacity=50, cap="round")
for i, dd in enumerate(["M360,700 C358,712 358,722 362,730",
                        "M384,706 C384,718 386,726 390,732",
                        "M404,700 C406,712 408,720 412,726"]):
    d.path(dd, f"Chest fringe {i+1}", fill=NONE, stroke="#B8A88C",
           strokeWidth=3, opacity=60, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#243A24", strokeWidth=6)

# --- captions -------------------------------------------------------------------
d.text("BORDER COLLIE", "Name", x=500, y=934, size=56, font="Virelai Sans",
       color="#EDEACB", justify="center")
LINE2, SZ2, TRK = "HERDING · SCOTTISH BORDERS", 22, 280
r = d.text(LINE2, "Milestone", x=500, y=970, size=SZ2, font="Virelai Sans",
           color="#C4C4A2", justify="center")
d.cmd("text.setStyle", "Milestone tracking", id=r["id"], tracking=TRK)

b = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("milestone bounds", {k: round(v) for k, v in b.items()})
nearest = (min(max(PCX, b["x"]), b["x"] + b["width"]),
           min(max(PCY, b["y"]), b["y"] + b["height"]))
clear = math.hypot(nearest[0] - PCX, nearest[1] - PCY) - (PR + 3)
print("clears rim by %.1f" % clear)
assert clear > 0 and b["width"] <= 760 and b["x"] >= 10 and b["x"] + b["width"] <= 990, b

d.finish("border-collie-V1R00")
