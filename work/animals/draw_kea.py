#!/usr/bin/env python3
"""Kea — field plate V1R00. Head/bust portrait, face-on: the alpine parrot
that dismantles cars. Olive plumage in scalloped covert rows, a long dark
decurved beak, bright dark eyes, and one hot orange flash where the raised
wing shows its underwing. Slate green plate, faint peaks high inside the
rim, dark alpine backdrop. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Kea — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#1E241C"   # dark olive-slate, not black


def on_disc(x, y, pad):
    return math.hypot(x - PCX, y - PCY) <= PR - pad


def disc_x(y, side):
    return PCX + side * math.sqrt(PR ** 2 - (y - PCY) ** 2)


def lin(c0, c1, start=None, end=None):
    g = {"kind": "linear", "stops": [{"offset": 0, "color": c0}, {"offset": 1, "color": c1}]}
    if start: g["start"], g["end"] = [round(v, 1) for v in start], [round(v, 1) for v in end]
    return {"gradient": g}


def rad(*stops):
    n = len(stops) - 1
    return {"gradient": {"kind": "radial", "stops": [
        {"offset": round(i / n, 3), "color": c} for i, c in enumerate(stops)]}}


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


def arc_closed(contour):
    """contour runs left disc point -> right disc point over the top; close it
    clockwise along the disc's own arc through the bottom."""
    (lx, ly), (rx, ry) = contour[0], contour[-1]
    for x, y in (contour[0], contour[-1]):
        assert abs(math.hypot(x - PCX, y - PCY) - PR) < 1.5, (x, y)
    return smooth(contour, closed=False) + f" A420,420 0 0 1 {lx:.1f},{ly:.1f} Z"


BG_GRAD = lin("#15201A", "#060A08", [0, 0], [0, 1000])
PLATE_GRAD = rad("#B4C6B2", "#75917C", "#33463C")
HEAD_GRAD = rad("#A9B269", "#7E8A46", "#4C5628")
WING_GRAD = lin("#77843F", "#424E22", [640, 540], [800, 780])
BEAK_GRAD = lin("#5C6058", "#1C201E", [475, 400], [530, 620])
ORANGE = "#E07B28"
ORANGE_GRAD = lin("#F09238", "#B85A18", [660, 560], [760, 760])

# --- backdrop + plate -----------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876, fill="#C4D6C0", opacity=6, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#2C3E34", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#DCE8D6", strokeWidth=3, opacity=50)
# faint alpine peaks high inside the rim, snow caps
for i, (x0, ytop, hw) in enumerate([(240, 176, 95), (355, 226, 80), (672, 190, 90), (560, 236, 70)]):
    assert on_disc(x0, ytop, 8) and on_disc(x0 - hw, ytop + hw * 0.9, 8) and on_disc(x0 + hw, ytop + hw * 0.9, 8), i
    d.path(f"M{x0 - hw},{ytop + hw * 0.9:.0f} L{x0},{ytop} L{x0 + hw},{ytop + hw * 0.9:.0f} Z",
           f"Peak {i+1}", fill="#3E5248", opacity=20, stroke=NONE)
    d.path(f"M{x0 - hw * 0.22:.0f},{ytop + hw * 0.20:.0f} L{x0},{ytop} L{x0 + hw * 0.22:.0f},{ytop + hw * 0.20:.0f} Z",
           f"Snowcap {i+1}", fill="#E4EDE0", opacity=22, stroke=NONE)
# plate patina + flecks
d.shape("ellipse", "Patina 1", x=185, y=330, width=210, height=140, fill="#4E665A", opacity=18, stroke=NONE)
d.shape("ellipse", "Patina 2", x=600, y=590, width=250, height=150, fill="#4E665A", opacity=16, stroke=NONE)
for i, (x, y, w) in enumerate([(200, 300, 7), (770, 280, 7), (175, 540, 8), (820, 540, 8), (255, 745, 7),
                               (735, 745, 8), (140, 420, 6), (860, 410, 6), (470, 120, 7), (640, 130, 7),
                               (365, 810, 6), (635, 812, 6)]):
    assert on_disc(x + w / 2, y + w / 2, 4), i
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w, fill="#3A5044", opacity=35, stroke=NONE)

# --- body / shoulders, closing on the disc arc ------------------------------------
y0 = 756
SH = [(disc_x(y0, -1), y0), (172, 726), (232, 688), (315, 662), (405, 652), (500, 656)]
SH = SH + [(2 * PCX - x, y) for x, y in reversed(SH[:-1])]
d.path(arc_closed(SH), "Shoulders", fill=lin("#6E7A3E", "#38421E", (500, 650), (500, 880)),
       stroke=INK, strokeWidth=6)

# --- the hot orange flash: raised wing on the viewer's right ----------------------
# underwing lining first (innermost layer), then the olive outer wing over it
d.path(smooth([(648, 545), (722, 560), (772, 630), (786, 716), (742, 780),
               (700, 730), (676, 640)]),
       "Underwing lining", fill=ORANGE_GRAD, stroke="#8A3E10", strokeWidth=4)
# covert scallops inside the orange panel
for lbl, dd in [("Orange covert 1", "M690,600 C712,612 734,634 748,662"),
                ("Orange covert 2", "M700,668 C718,682 734,706 740,734"),
                ("Orange covert 3", "M672,626 C692,644 708,672 716,706")]:
    d.path(dd, lbl, fill=NONE, stroke="#8A3E10", strokeWidth=4, opacity=45, cap="round")
# olive outer wing edge folded over the lining's outer rim
d.path(smooth([(712, 548), (780, 588), (806, 668), (792, 748), (756, 796),
               (742, 762), (756, 690), (752, 620)]),
       "Outer wing", fill=WING_GRAD, stroke=INK, strokeWidth=5)
for lbl, dd in [("Wing edge 1", "M742,592 C764,616 780,652 786,692"),
                ("Wing edge 2", "M748,706 C756,728 758,752 752,772")]:
    d.path(dd, lbl, fill=NONE, stroke="#A8B465", strokeWidth=4, opacity=50, cap="round")
# dark far wing sliver on the left, no orange — the plate keeps one accent
d.path(smooth([(352, 545), (292, 580), (268, 656), (284, 736), (318, 776),
               (330, 720), (324, 640), (330, 585)]),
       "Far wing", fill=lin("#4A5426", "#2E3616", [352, 545], [290, 776]),
       stroke=INK, strokeWidth=5, opacity=95)

# --- chest covert rows, painted bottom row first so upper rows overlap ------------
def interp(pts, v):
    for (a1, b1), (a2, b2) in zip(pts, pts[1:]):
        if a1 <= v <= a2: return b1 + (b2 - b1) * (v - a1) / (a2 - a1)
    return pts[-1][1] if v > pts[-1][0] else pts[0][1]


def sh_y(x):
    ax = abs(x - PCX)
    return interp(sorted((abs(px - PCX), py) for px, py in SH[:6]), ax)


def feather(name, x, y, w, h, c0, c1, edge_op):
    d.shape("ellipse", name, x=x - w / 2, y=y, width=w, height=h,
            fill=lin(c0, c1, (x, y), (x, y + h)), stroke=NONE)
    d.path(f"M{x - w * 0.44:.1f},{y + h * 0.62:.1f} Q{x:.1f},{y + h * 1.12:.1f} {x + w * 0.44:.1f},{y + h * 0.62:.1f}",
           f"{name} edge", fill=NONE, stroke="#2C3416", strokeWidth=3, opacity=edge_op, cap="round")


def fits_disc(x, y, w, h, pad=8):
    return all(on_disc(px, py, pad) for px, py in
               [(x - w / 2, y + h / 2), (x + w / 2, y + h / 2), (x, y + h),
                (x - w * 0.35, y + h * 0.9), (x + w * 0.35, y + h * 0.9)])


for row in range(8, -1, -1):
    yy = 640 + row * 26
    for j in range(-6, 7):
        x = PCX + j * 46 + (row % 2) * 23
        w, h = 56, 48
        if yy < sh_y(x) - 4 or not fits_disc(x, yy, w, h): continue
        t = row / 8
        feather(f"Covert r{row} {j+7}", x, yy, w, h, "#9AA454" if t < 0.5 else "#828D46",
                "#55612C", round(30 + 14 * t))
# chest light + under-head shadow
d.shape("ellipse", "Chest light", x=430, y=690, width=140, height=80, fill="#C4CC84", opacity=30, stroke=NONE)
d.shape("ellipse", "Under-head shadow", x=365, y=596, width=270, height=60, fill="#2E3618", opacity=30, stroke=NONE)

# --- head --------------------------------------------------------------------------
d.path(smooth([(500, 262), (606, 278), (668, 352), (682, 458), (652, 552),
               (596, 632), (500, 664), (404, 632), (348, 552), (318, 458),
               (332, 352), (394, 278)]),
       "Head", fill=HEAD_GRAD, stroke=INK, strokeWidth=7)
# crown feather tufts
for lbl, dd in [("Crown tuft 1", "M448,282 C454,266 466,256 480,252"),
                ("Crown tuft 2", "M520,252 C534,256 546,266 552,282"),
                ("Crown tuft 3", "M486,268 C494,258 506,258 514,268")]:
    d.path(dd, lbl, fill=NONE, stroke="#55612C", strokeWidth=5, opacity=50, cap="round")
# head top highlight + cheek shading
d.shape("ellipse", "Head highlight", x=395, y=290, width=210, height=76, fill="#FFFFFF", opacity=12, stroke=NONE)
d.shape("ellipse", "Cheek shade L", x=330, y=470, width=64, height=60, fill="#55612C", opacity=28, stroke=NONE)
d.shape("ellipse", "Cheek shade R", x=606, y=470, width=64, height=60, fill="#55612C", opacity=28, stroke=NONE)
# pale buff throat wash under the beak
d.shape("ellipse", "Throat wash", x=435, y=560, width=130, height=80, fill="#C4B86A", opacity=30, stroke=NONE)

# --- face ----------------------------------------------------------------------------
# eyes: dark, knowing, set slightly low — the car-dismantler's stare
d.shape("ellipse", "Eye L", x=382, y=408, width=46, height=52, fill="#181410", stroke=NONE)
d.shape("ellipse", "Eye R", x=572, y=408, width=46, height=52, fill="#181410", stroke=NONE)
d.shape("ellipse", "Eye ring L", x=378, y=404, width=54, height=60, fill=NONE,
        stroke="#C4B86A", strokeWidth=3, opacity=40)
d.shape("ellipse", "Eye ring R", x=568, y=404, width=54, height=60, fill=NONE,
        stroke="#C4B86A", strokeWidth=3, opacity=40)
d.shape("ellipse", "Glint L", x=394, y=418, width=10, height=10, fill="#FFFFFF", opacity=92, stroke=NONE)
d.shape("ellipse", "Glint R", x=584, y=418, width=10, height=10, fill="#FFFFFF", opacity=92, stroke=NONE)
# the beak: long slender decurved upper mandible, face-on it drops to the chest
d.path("M500,370 C524,374 540,388 546,414 C552,452 544,496 526,540 "
       "C514,576 506,608 500,634 C494,608 486,576 474,540 "
       "C456,496 448,452 454,414 C460,388 476,374 500,370 Z",
       "Beak", fill=BEAK_GRAD, stroke=INK, strokeWidth=6)
# beak ridge highlight + tip hook shade
d.path("M500,382 C507,438 507,500 500,570", "Beak ridge", fill=NONE,
       stroke="#9AA094", strokeWidth=5, opacity=50, cap="round")
d.path("M478,584 C488,606 494,622 500,632 C506,622 512,606 522,584 "
       "C512,596 488,596 478,584 Z", "Beak tip shade", fill="#10140F", opacity=55, stroke=NONE)
# cere + nares at the beak base
d.shape("ellipse", "Cere", x=476, y=376, width=48, height=22, fill="#6E6A52", opacity=80, stroke=NONE)
d.shape("ellipse", "Nare L", x=485, y=382, width=8, height=5, fill="#181410", stroke=NONE)
d.shape("ellipse", "Nare R", x=507, y=382, width=8, height=5, fill="#181410", stroke=NONE)
# loral shadow between eye and beak
d.path("M438,414 C452,420 462,430 468,444", "Lore L", fill=NONE,
       stroke="#3A421E", strokeWidth=5, opacity=55, cap="round")
d.path("M562,414 C548,420 538,430 532,444", "Lore R", fill=NONE,
       stroke="#3A421E", strokeWidth=5, opacity=55, cap="round")

# --- name ----------------------------------------------------------------------------
d.text("KEA", "Name", x=500, y=962, size=60, font="Virelai Sans",
       color="#D6E2CC", justify="center")

d.finish("kea-V1R00")
