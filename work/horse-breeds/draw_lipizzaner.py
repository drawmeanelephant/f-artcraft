#!/usr/bin/env python3
"""Lipizzaner — milestone card V1R00. The mature white baroque horse
in the levade: croup dropped low, hinds deeply flexed under the mass,
forelegs tucked, neck arched with the muzzle drawn in — the haute
ecole pose without a costume in sight. Riding-school world: warm
bronze dusk disc, pale arena sand, three faint tall windows high on
the plate. 1000x1000. House style: gradients + translucent shading,
never flat fills. Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Lipizzaner — Milestone Card", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#241C14"                    # warm dark ink, never pure black


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


def leg(p_top, p_joint, p_hoof, w_top, w_j, w_h):
    """Bent limb silhouette — two segments, one hard joint, tapered."""

    def norm(a, b):
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1
        return (-dy / L, dx / L)

    def off(p, n, w):
        return (p[0] + n[0] * w / 2, p[1] + n[1] * w / 2)

    n1 = norm(p_top, p_joint)
    n2 = norm(p_joint, p_hoof)
    pts = [off(p_top, n1, w_top), off(p_joint, n1, w_j), off(p_hoof, n2, w_h),
           off(p_hoof, n2, -w_h), off(p_joint, n2, -w_j), off(p_top, n1, -w_top)]
    return smooth(pts, k=0.5)


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


BG_GRAD = lin(0, 0, 0, 1000, (0, "#181410"), (1, "#0A0705"))
PLATE_GRAD = rad((0, "#C8AC7E"), (0.55, "#8A7050"), (1, "#463723"))
COAT_GRAD = lin(320, 350, 720, 780, (0, "#F0EBE0"), (0.5, "#CFC8B8"), (1, "#9A9282"))
DIM_GRAD = lin(320, 350, 720, 780, (0, "#B8B0A0"), (1, "#6E675A"))
HAIR_GRAD = lin(350, 370, 470, 560, (0, "#D8D0BE"), (1, "#9C927C"))
FLOOR_GRAD = lin(0, 730, 0, 880, (0, "#8E7B58"), (0.55, "#61523A"), (1, "#33291A"))
SHEEN = "#FFF8E8"

# --- backdrop + riding-school bronze plate -----------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#3E3220", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#EFE4C4", strokeWidth=3, opacity=38)

# three tall school windows, faint on the upper plate
for i, x in enumerate([(205, 175), (472, 150), (708, 168)]):
    cx, top = x
    assert on_disc(cx + 30, top + 10, 20), i
    d.path(f"M{cx},340 L{cx},{top + 55} C{cx},{top + 18} {cx + 12},{top} {cx + 30},{top} "
           f"C{cx + 48},{top} {cx + 60},{top + 18} {cx + 60},{top + 55} L{cx + 60},340",
           f"Window {i+1}", fill=NONE, stroke="#D8C8A0", strokeWidth=4,
           opacity=13, cap="round")
# stage light pooling upper-left
d.shape("ellipse", "Light pool", x=235, y=130, width=420, height=230,
        fill="#F4E8C8", opacity=15, stroke=NONE)
# haze lenses
for i, (x, y, w) in enumerate([(340, 380, 90), (585, 240, 70), (730, 405, 80),
                               (260, 500, 60), (470, 200, 55)]):
    assert on_disc(x, y, 20), i
    d.shape("ellipse", f"Haze {i+1}", x=x - w / 2, y=y - w / 5, width=w, height=w * 0.4,
            fill="#ECDFB8", opacity=10, stroke=NONE)

# --- arena sand floor, closing on the disc arc -------------------------------------
fy = 782
fl, fr = rim_x(fy, -1), rim_x(fy, 1)
d.path(f"M{fl:.1f},{fy} C300,772 400,792 500,786 C600,780 700,782 {fr:.1f},{fy} "
       f"A{PR},{PR} 0 0 1 {fl:.1f},{fy} Z", "Floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{fl + 8:.0f},{fy} C300,772 400,792 500,786 C600,780 700,782 {fr - 8:.0f},{fy}",
       "Floor crest", fill=NONE, stroke="#C0AE82", strokeWidth=5, opacity=42, cap="round")
# a raked-sand line
d.path("M330,822 C430,810 560,808 680,816", "Sand line", fill=NONE,
       stroke="#4A3E26", strokeWidth=4, opacity=45, cap="round")

# soft shadow under the crouched hindquarters
d.shape("ellipse", "Horse shadow", x=380, y=762, width=430, height=28,
        fill="#171006", opacity=34, stroke=NONE)

# --- the lipizzaner, levade facing left --------------------------------------------
# tail — long and luxuriant, hanging off the dropped croup
d.path(smooth([(664, 634), (694, 660), (708, 696), (710, 732), (700, 752),
               (688, 746), (682, 712), (676, 678), (666, 652)]),
       "Tail", fill=HAIR_GRAD, stroke=INK, strokeWidth=5)
for i, dd in enumerate(["M686,664 C696,694 700,716 698,740",
                        "M676,672 C686,700 690,720 688,742"]):
    d.path(dd, f"Tail wave {i+1}", fill=NONE, stroke="#8A8070",
           strokeWidth=3.5, opacity=55, cap="round")

# far legs — dimmer
# far hind: hock sunk low and forward, hoof planted under the mass
d.path(leg((655, 618), (672, 700), (648, 752), 42, 20, 11),
       "Hind leg far", fill=DIM_GRAD, stroke=INK, strokeWidth=4.5)
# far fore: tucked level with the near, slightly higher
d.path(leg((444, 568), (510, 582), (484, 644), 34, 15, 10),
       "Foreleg far", fill=DIM_GRAD, stroke=INK, strokeWidth=4.5)

# one silhouette: the levade diagonal — poll high, withers up,
# back descending to the dropped croup, haunch a full rounded mass
d.path(smooth([(310, 474), (306, 440), (316, 410), (336, 388), (358, 372),
               (390, 366), (424, 392), (456, 442), (525, 505), (590, 552),
               (640, 586), (684, 620), (706, 656), (700, 692), (664, 712),
               (596, 710), (528, 686), (468, 644), (436, 596), (430, 548),
               (408, 508), (376, 502), (350, 494), (326, 500)]),
       "Horse", fill=COAT_GRAD, stroke=INK, strokeWidth=6)

# near legs — hinds crouched deep with a true hock flex, fore tucked level
d.path(leg((428, 562), (496, 568), (470, 634), 36, 16, 11),
       "Foreleg near", fill=COAT_GRAD, stroke=INK, strokeWidth=5)
d.path(leg((630, 612), (650, 694), (600, 752), 46, 20, 12),
       "Hind leg near", fill=COAT_GRAD, stroke=INK, strokeWidth=5)

# hooves — dark caps
for i, (cx, cy) in enumerate([(470, 638), (484, 648), (600, 756), (648, 756)]):
    d.path(f"M{cx - 12},{cy - 8} C{cx - 5},{cy - 12} {cx + 7},{cy - 12} {cx + 12},{cy - 6} "
           f"C{cx + 10},{cy + 4} {cx - 9},{cy + 5} {cx - 12},{cy - 1} Z",
           f"Hoof {i+1}", fill="#17110C", stroke=INK, strokeWidth=3)

# shading kept at the silhouette edges — soft modelling for a white coat
d.path("M456,436 C506,488 556,536 610,584 C556,542 506,494 460,444 Z",
       "Topline sheen", fill=SHEEN, opacity=40, stroke=NONE)
d.path("M470,650 C530,690 596,710 650,712 C596,714 528,694 474,656 Z",
       "Belly shade", fill="#A89E8C", opacity=30, stroke=NONE)
d.path(smooth([(436, 540), (452, 556), (454, 578), (440, 594), (424, 588),
               (420, 562)]),
       "Chest shade", fill="#A89E8C", opacity=28, stroke=NONE)
d.path("M596,706 C622,712 646,712 662,706", "Flank crease", fill=NONE,
       stroke="#9A9080", strokeWidth=3.5, opacity=40, cap="round")
d.path(smooth([(616, 616), (652, 626), (668, 656), (654, 688), (624, 680),
               (612, 648)]),
       "Quarter shade", fill="#A89E8C", opacity=20, stroke=NONE)
d.path("M382,378 C404,390 424,410 440,432", "Crest sheen", fill=NONE,
       stroke=SHEEN, strokeWidth=4, opacity=55, cap="round")

# mane — full baroque fall on the crest, scalloped hem
d.path(smooth([(352, 366), (386, 360), (416, 382), (440, 414), (452, 444),
               (444, 464), (432, 452), (424, 472), (408, 456), (400, 474),
               (384, 458), (376, 472), (362, 456), (352, 464), (344, 436),
               (340, 402)]),
       "Mane", fill=HAIR_GRAD, stroke=INK, strokeWidth=4)
for i, dd in enumerate(["M364,378 C386,394 404,418 416,446",
                        "M356,402 C376,420 390,442 398,462",
                        "M380,372 C400,384 418,404 430,430"]):
    d.path(dd, f"Mane wave {i+1}", fill=NONE, stroke="#8A8070",
           strokeWidth=3.5, opacity=55, cap="round")
d.path("M354,368 C376,358 400,366 424,388", "Mane crest light", fill=NONE,
       stroke=SHEEN, strokeWidth=3.5, opacity=50, cap="round")
# forelock over the brow
d.path(smooth([(348, 376), (338, 390), (336, 406), (344, 418), (354, 408),
               (358, 392), (356, 378)]),
       "Forelock", fill=HAIR_GRAD, opacity=92, stroke=NONE)

# ears — small, curved inward, alert
d.path("M348,378 L342,338 L366,368 Z", "Ear near", fill=COAT_GRAD,
       stroke=INK, strokeWidth=4)
d.path("M368,374 L366,340 L386,366 Z", "Ear far", fill=DIM_GRAD,
       stroke=INK, strokeWidth=3.5)
d.path("M348,368 L344,350", "Ear inner", fill=NONE, stroke="#0F0A08",
       strokeWidth=3, opacity=55, cap="round")

# the eye — dark and warm against the white
d.path("M330,428 C336,420 348,418 356,424 C354,434 342,438 332,434 "
       "C328,432 328,430 330,428 Z", "Eye",
       fill=rad((0, "#5A4028"), (0.7, "#34220F"), (1, "#160D07")),
       stroke=INK, strokeWidth=3)
d.shape("ellipse", "Pupil", x=339, y=425, width=9, height=10, fill="#0E0806", stroke=NONE)
d.shape("ellipse", "Glint", x=342, y=426, width=4.5, height=4.5, fill="#FFF8E0", opacity=95, stroke=NONE)
d.path("M328,420 C340,414 352,414 360,420", "Brow", fill=NONE,
       stroke="#8E8474", strokeWidth=4, opacity=55, cap="round")

# muzzle — dark skin showing through the white at lips and nostril
d.path(smooth([(302, 444), (302, 468), (314, 484), (332, 490), (348, 482),
               (348, 462), (338, 446), (318, 440)]),
       "Muzzle shade", fill="#A09480", opacity=50, stroke=NONE)
d.path("M310,470 C310,476 315,481 321,480 C326,478 327,472 323,468 "
       "C319,464 312,465 310,470 Z", "Nostril", fill="#1A110B",
       stroke=INK, strokeWidth=2.5)
d.path("M316,488 C326,493 338,491 346,486", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=3, opacity=75, cap="round")
d.path("M342,458 C354,464 366,462 374,454", "Cheek line", fill=NONE,
       stroke="#9A9080", strokeWidth=3, opacity=50, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#382D1B", strokeWidth=6)

# --- captions -------------------------------------------------------------------
d.text("LIPIZZANER", "Name", x=500, y=934, size=56, font="Virelai Sans",
       color="#F2E8C8", justify="center")
LINE2, SZ2, TRK = "CLASSICAL · LIPIZZA", 22, 280
r = d.text(LINE2, "Milestone", x=500, y=970, size=SZ2, font="Virelai Sans",
           color="#D2C29E", justify="center")
d.cmd("text.setStyle", "Milestone tracking", id=r["id"], tracking=TRK)

b = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("milestone bounds", {k: round(v) for k, v in b.items()})
nearest = (min(max(PCX, b["x"]), b["x"] + b["width"]),
           min(max(PCY, b["y"]), b["y"] + b["height"]))
clear = math.hypot(nearest[0] - PCX, nearest[1] - PCY) - (PR + 3)
print("clears rim by %.1f" % clear)
assert clear > 0 and b["width"] <= 760 and b["x"] >= 10 and b["x"] + b["width"] <= 990, b

d.finish("lipizzaner-V1R00")
