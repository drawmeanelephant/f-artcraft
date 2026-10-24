#!/usr/bin/env python3
"""Dhole — field plate V1R00. The whistling dog at full extension through
sal forest: russet coat, muzzle thrown up mid-call, mouth open on the
whistle, dark-tipped tail streaming low. Behind on the floor line a dim
packmate answers — the chorus line. Leaf-litter floor closes on the
disc's own arc. Asian-forest plate, pack-call mood. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Dhole — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#231208"                    # warm dark ink, never pure black


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


BG_GRAD = lin(0, 0, 0, 1000, (0, "#131C0E"), (1, "#050803"))
PLATE_GRAD = rad((0, "#CCC092"), (0.55, "#8E9A6A"), (1, "#465C44"))
COAT_GRAD = lin(420, 400, 620, 620, (0, "#C06630"), (0.55, "#9A4A20"), (1, "#642E12"))
DIM_GRAD = lin(420, 400, 620, 620, (0, "#8A4A24"), (1, "#542610"))
PALE = "#EEDCB4"
FLOOR_GRAD = lin(0, 740, 0, 880, (0, "#7A6234"), (0.5, "#52401E"), (1, "#2C2010"))
TRUNK_GRAD = lin(0, 150, 0, 760, (0, "#3A4A30"), (1, "#1E2A1A"))

# --- backdrop + forest plate ---------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=58, y=18, width=884, height=884, fill="#A8B078", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#2C3E28", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8E4C0", strokeWidth=3, opacity=40)

# canopy dusk-light pooling in the upper disc
d.shape("ellipse", "Light pool", x=330, y=140, width=380, height=220,
        fill="#F0E2B0", opacity=18, stroke=NONE)
# dappled light flecks drifting down
for i, (x, y, w) in enumerate([(300, 300, 26), (420, 240, 18), (560, 210, 22),
                               (660, 300, 16), (240, 430, 20), (740, 440, 24),
                               (480, 330, 14), (620, 380, 18)]):
    assert on_disc(x, y, 20), i
    d.shape("ellipse", f"Dapple {i+1}", x=x - w / 2, y=y - w / 3, width=w, height=w * 0.66,
            fill="#F4E8BE", opacity=16, stroke=NONE)

# sal trunks — tall straight columns inside the disc
for i, (x, w, y0, lean) in enumerate([(218, 30, 178, -8), (778, 26, 170, 10), (650, 18, 150, -4)]):
    y_rim = PCY - math.sqrt(PR * PR - (x - PCX) ** 2)
    y0 = max(y0, y_rim + 12)
    assert on_disc(x, y0, 8), i
    d.path(f"M{x - w / 2},{y0} C{x - w / 2 + lean},{(y0 + 745) / 2} {x - w / 2 + lean},{700} {x - w / 2 + lean},745 "
           f"L{x + w / 2 + lean},745 C{x + w / 2 + lean},700 {x + w / 2 + lean},{(y0 + 745) / 2} {x + w / 2},{y0} Z",
           f"Trunk {i+1}", fill=TRUNK_GRAD, opacity=70, stroke=NONE)
    d.path(f"M{x + w * 0.2},{y0 + 40} C{x + w * 0.2 + lean},{(y0 + 700) / 2} {x + w * 0.2 + lean},660 {x + w * 0.2 + lean},730",
           f"Trunk edge {i+1}", fill=NONE, stroke="#141E10", strokeWidth=3, opacity=40, cap="round")

# far packmate on the floor line — small silhouette answering, head thrown up
d.path(smooth([(258, 690), (282, 678), (316, 678), (342, 688), (350, 706),
               (340, 720), (314, 726), (280, 724), (256, 712)]),
       "Packmate body", fill="#33402E", opacity=60, stroke=NONE)
d.path("M258,698 C246,688 236,672 234,656 C232,646 240,638 250,642 "
       "C260,646 264,660 266,674 C268,686 266,694 258,698 Z",
       "Packmate neck+head", fill="#33402E", opacity=60, stroke=NONE)
d.path("M238,648 L232,632 L248,640 Z", "Packmate ear", fill="#33402E", opacity=60, stroke=NONE)
d.path("M348,694 C364,688 374,678 376,666 C382,682 374,700 356,708 Z",
       "Packmate tail", fill="#33402E", opacity=60, stroke=NONE)
for i, (x0, y1) in enumerate([(272, 756), (296, 758), (322, 756)]):
    d.path(f"M{x0},724 L{x0 - 4},{y1}", f"Packmate leg {i+1}", fill=NONE,
           stroke="#33402E", strokeWidth=7, opacity=60, cap="round")

# --- leaf-litter floor, closing on the disc arc ---------------------------------
fy = 756
fl, fr = rim_x(fy, -1), rim_x(fy, 1)
d.path(f"M{fl:.1f},{fy} C300,742 400,764 500,754 C600,744 700,750 {fr:.1f},{fy} "
       f"A{PR},{PR} 0 0 1 {fl:.1f},{fy} Z", "Floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{fl + 8:.0f},{fy} C300,742 400,764 500,754 C600,744 700,750 {fr - 8:.0f},{fy}",
       "Floor crest", fill=NONE, stroke="#C8AE70", strokeWidth=5, opacity=45, cap="round")
# fallen leaves — pointed ovals scattered on the litter
for i, (x, y, a, c) in enumerate([(280, 790, 30, "#8A6E34"), (360, 810, -50, "#6E5626"),
                                  (470, 796, 70, "#9A7E40"), (560, 812, -20, "#7A6030"),
                                  (660, 792, 40, "#8A6E34"), (700, 798, -60, "#6E5626"),
                                  (340, 822, 10, "#7A6030"), (510, 844, -35, "#8A6E34"),
                                  (610, 842, 55, "#6E5626"), (430, 830, 15, "#9A7E40")]):
    assert on_disc(x, y, 14), i
    t = math.radians(a); c_, s_ = math.cos(t), math.sin(t)
    d.path(f"M{x},{y} q{10 * c_ - 3 * s_:.0f},{10 * s_ + 3 * c_:.0f} {20 * c_:.0f},{20 * s_:.0f} "
           f"q{-9 * c_ - 4 * s_:.0f},{-9 * s_ + 4 * c_:.0f} {-20 * c_:.0f},{-20 * s_:.0f} Z",
           f"Leaf {i+1}", fill=c, opacity=75, stroke=NONE)

# soft shadow where the dog hangs over the floor
d.shape("ellipse", "Dog shadow", x=390, y=742, width=320, height=30,
        fill="#1E160A", opacity=30, stroke=NONE)

# --- the dhole, full extension, facing left --------------------------------------
# tail streaming right, low and bushy, dark-tipped
d.path(smooth([(624, 452), (692, 446), (752, 462), (800, 486), (816, 508),
               (800, 516), (748, 508), (696, 500), (646, 494)]),
       "Tail", fill=lin(640, 450, 810, 510, (0, "#8A4A20"), (0.6, "#6E3414"), (1, "#48200C")),
       stroke=INK, strokeWidth=5)
d.path(smooth([(748, 462), (788, 480), (816, 508), (800, 516), (756, 508)]),
       "Tail dark tip", fill="#2E1808", opacity=85, stroke=NONE)
# tail fluff strokes
for i, dd in enumerate(["M676,470 C710,468 744,476 774,492",
                        "M668,484 C704,486 738,494 768,504"]):
    d.path(dd, f"Tail fur {i+1}", fill=NONE, stroke="#5A2A10",
           strokeWidth=4, opacity=50, cap="round")

# hind legs kicked back-right — bent at the hock, toes trailing
d.path(smooth([(520, 510), (568, 566), (612, 632), (662, 682), (690, 696),
               (664, 708), (612, 656), (556, 596), (500, 548)]),
       "Hind leg far", fill=DIM_GRAD, stroke=INK, strokeWidth=4.5)
d.path(smooth([(560, 505), (616, 560), (670, 640), (722, 690), (754, 700),
               (728, 718), (680, 668), (626, 600), (556, 555)]),
       "Hind leg near", fill=COAT_GRAD, stroke=INK, strokeWidth=5)
d.path("M726,696 C744,698 756,708 752,720 C740,730 720,724 716,710 "
       "C716,702 720,696 726,696 Z", "Hind foot near", fill="#4A2210",
       stroke=INK, strokeWidth=4)

# body — the lean gallop line, belly tucked high
d.path(smooth([(415, 480), (460, 450), (545, 440), (620, 450), (662, 478),
               (650, 505), (605, 522), (525, 532), (455, 528), (412, 505)]),
       "Body", fill=COAT_GRAD, stroke=INK, strokeWidth=6)
# pale belly + chest, tucked high
d.path("M448,512 C490,526 556,528 610,514 C584,536 506,542 462,526 "
       "C450,520 446,516 448,512 Z", "Belly pale", fill=PALE, opacity=50, stroke=NONE)
d.shape("ellipse", "Back sheen", x=470, y=444, width=160, height=30,
        fill="#E89858", opacity=35, stroke=NONE)
d.path("M440,468 C500,450 575,450 636,466", "Spine crease", fill=NONE,
       stroke="#642E12", strokeWidth=5, opacity=50, cap="round")

# front legs reaching forward — bent at the wrist, toes leading
d.path(smooth([(500, 500), (470, 570), (432, 630), (400, 672), (378, 690),
               (400, 702), (438, 654), (488, 592), (530, 540)]),
       "Front leg far", fill=DIM_GRAD, stroke=INK, strokeWidth=4.5)
d.path(smooth([(466, 494), (428, 574), (380, 640), (346, 678), (324, 698),
               (350, 708), (388, 654), (446, 598), (500, 532)]),
       "Front leg near", fill=COAT_GRAD, stroke=INK, strokeWidth=5)
d.path("M326,688 C344,688 356,698 352,710 C340,718 320,712 318,700 "
       "C318,692 322,688 326,688 Z", "Front foot near", fill="#4A2210",
       stroke=INK, strokeWidth=4)

# neck thrown up into the call, continuous with the chest
d.path(smooth([(452, 508), (428, 470), (398, 428), (368, 396), (344, 378),
               (328, 384), (334, 410), (350, 444), (378, 480), (414, 512)]),
       "Neck", fill=COAT_GRAD, stroke=INK, strokeWidth=5)
# pale throat running up the underside of the neck
d.path("M414,498 C392,466 366,432 346,404 C360,410 384,444 402,476 "
       "C410,490 416,496 414,498 Z", "Throat pale", fill=PALE, opacity=55, stroke=NONE)

# skull + raised muzzle
d.path(smooth([(322, 332), (346, 322), (372, 334), (386, 358), (386, 386),
               (372, 408), (350, 418), (328, 414), (310, 400), (302, 376),
               (304, 352)]),
       "Skull", fill=COAT_GRAD, stroke=INK, strokeWidth=5)
# upper muzzle up-left, lower jaw dropped — the open call
d.path(smooth([(310, 344), (292, 330), (270, 316), (252, 310), (248, 322),
               (262, 336), (286, 348), (308, 358)]),
       "Upper muzzle", fill=COAT_GRAD, stroke=INK, strokeWidth=4)
d.path(smooth([(308, 372), (294, 376), (276, 370), (264, 362), (260, 372),
               (274, 384), (294, 390), (310, 388)]),
       "Lower jaw", fill="#7A3818", stroke=INK, strokeWidth=4)
# mouth interior — the dark wedge the whistle comes out of
d.path("M252,318 L292,344 L286,368 L262,362 Z", "Mouth dark",
       fill="#3A0E08", stroke=NONE)
d.path("M266,358 L280,364 L270,370 Z", "Tongue hint", fill="#B85A40",
       opacity=80, stroke=NONE)
# nose — dark on the muzzle tip
d.path("M248,306 C240,308 236,316 240,324 C246,330 256,328 260,320 "
       "C260,312 254,306 248,306 Z", "Nose", fill="#2E1408",
       stroke=INK, strokeWidth=3)

# rounded ears — dhole, not fox
d.path("M330,330 C324,308 336,290 358,290 C376,290 388,306 386,324 "
       "C372,316 350,318 338,332 Z", "Ear near", fill="#7A3818",
       stroke=INK, strokeWidth=4)
d.path("M342,320 C340,310 346,300 356,300 C366,300 372,308 372,318 "
       "C362,312 350,314 342,320 Z", "Ear inner", fill="#3A1E0C",
       opacity=80, stroke=NONE)
d.path("M372,340 C372,326 382,316 396,318 C408,320 414,332 410,344 "
       "C398,336 382,334 372,340 Z", "Ear far", fill="#5A2A10",
       stroke=INK, strokeWidth=3.5)

# eye — amber, screwed nearly shut on the high note
d.path("M306,362 C316,352 332,350 342,358 C338,370 324,374 314,370 "
       "C308,368 304,366 306,362 Z", "Eye",
       fill=rad((0, "#E8BC4E"), (0.7, "#A87E24"), (1, "#6E5212")),
       stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Pupil", x=320, y=357, width=8, height=10, fill="#140C04", stroke=NONE)
d.shape("ellipse", "Eye glint", x=322, y=359, width=4, height=4, fill="#FFF4D8", opacity=85, stroke=NONE)
# short muzzle fur strokes + whisker roots
d.path("M286,324 C298,332 308,344 314,358", "Muzzle fur", fill=NONE,
       stroke="#642E12", strokeWidth=3.5, opacity=50, cap="round")
for j, (x2, y2) in enumerate([(238, 368), (244, 380), (250, 390)]):
    d.path(f"M286,{362 + j * 6} Q258,{368 + j * 8} {x2},{y2}", f"Whisker {j+1}",
           fill=NONE, stroke="#F0E4C4", strokeWidth=2, opacity=55, cap="round")

# the whistle itself — arcs ringing off the open mouth
for i, dd in enumerate(["M234,310 C202,292 180,264 172,228",
                        "M224,326 C186,314 158,288 146,252",
                        "M220,342 C178,336 146,316 128,284"]):
    d.path(dd, f"Whistle arc {i+1}", fill=NONE, stroke="#F4ECD0",
           strokeWidth=4, opacity=42 - i * 10, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#243A24", strokeWidth=6)

# --- name ----------------------------------------------------------------------
d.text("DHOLE", "Name", x=500, y=962, size=60, font="Virelai Sans",
       color="#E4E0BC", justify="center")

d.finish("dhole-V1R00")
