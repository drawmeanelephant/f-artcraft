#!/usr/bin/env python3
"""Shetland pony — milestone card V1R00. The little moor survivor
standing square into the wind: deep wide barrel, short legs planted,
dense winter coat, thick forelock tumbling over the face, heavy mane
and tail blown flat sideways. Heather tufts on a peat floor closing
on the disc's arc; wind streaks comb the moor. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Shetland Pony — Milestone Card", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#261C14"                    # warm dark ink, never pure black


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


BG_GRAD = lin(0, 0, 0, 1000, (0, "#151B14"), (1, "#080B07"))
PLATE_GRAD = rad((0, "#ADB88E"), (0.55, "#7C8C6B"), (1, "#43523E"))
COAT_GRAD = lin(320, 400, 700, 760, (0, "#7A5C3C"), (0.5, "#5A4028"), (1, "#38261A"))
DIM_GRAD = lin(320, 400, 700, 760, (0, "#5E452C"), (1, "#2C1E12"))
MANE_GRAD = lin(340, 380, 700, 680, (0, "#3C2C1C"), (0.6, "#261B10"), (1, "#181009"))
FLOOR_GRAD = lin(0, 720, 0, 880, (0, "#5E5A3C"), (0.55, "#42402A"), (1, "#262415"))

# --- backdrop + moor plate -------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#2E4028", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E2E4C4", strokeWidth=3, opacity=38)

# flat moor light pooling upper-left
d.shape("ellipse", "Light pool", x=240, y=150, width=400, height=230,
        fill="#EEE8C0", opacity=14, stroke=NONE)
# wind streaks combing the moor, all running right
for i, (x, y, w) in enumerate([(300, 320, 130), (620, 260, 110), (700, 420, 120),
                               (250, 560, 100), (600, 610, 90)]):
    assert on_disc(x, y, 20), i
    d.path(f"M{x - w / 2},{y} C{x - w / 6},{y - 7} {x + w / 6},{y + 7} {x + w / 2},{y}",
           f"Wind {i+1}", fill=NONE, stroke="#E8EAC8", strokeWidth=4,
           opacity=16, cap="round")

# --- peat floor, closing on the disc arc ------------------------------------------
fy = 782
fl, fr = rim_x(fy, -1), rim_x(fy, 1)
d.path(f"M{fl:.1f},{fy} C300,768 400,790 500,782 C600,774 700,780 {fr:.1f},{fy} "
       f"A{PR},{PR} 0 0 1 {fl:.1f},{fy} Z", "Floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{fl + 8:.0f},{fy} C300,768 400,790 500,782 C600,774 700,780 {fr - 8:.0f},{fy}",
       "Floor crest", fill=NONE, stroke="#9A9464", strokeWidth=5, opacity=42, cap="round")
# heather tufts on the crest
for i, (x, y) in enumerate([(330, 802), (430, 828), (560, 834), (660, 818), (706, 794)]):
    assert on_disc(x, y + 10, 14), i
    for j, (dx, dy) in enumerate([(-14, 10), (-6, -4), (2, -10), (10, -2), (16, 8)]):
        d.path(f"M{x + dx * 0.4:.0f},{y + 14} L{x + dx:.0f},{y + dy:.0f}",
               f"Heather {i+1}.{j+1}", fill=NONE, stroke="#6E5E70",
               strokeWidth=3.5, opacity=65, cap="round")
    d.shape("ellipse", f"Heather bloom {i+1}", x=x - 6, y=y - 6, width=10, height=8,
            fill="#8A7490", opacity=50, stroke=NONE)

# shadow the pony stands over
d.shape("ellipse", "Pony shadow", x=330, y=750, width=380, height=26,
        fill="#151106", opacity=32, stroke=NONE)

# --- the shetland, square into the wind, facing left -------------------------------
# tail — thick, full, blown flat sideways off the dock
d.path(smooth([(668, 486), (714, 512), (752, 556), (772, 610), (776, 660),
               (762, 692), (740, 696), (726, 668), (714, 620), (694, 566),
               (668, 524)]),
       "Tail", fill=MANE_GRAD, stroke=INK, strokeWidth=5)
for i, dd in enumerate(["M694,540 C720,580 736,624 746,668",
                        "M684,566 C706,602 720,640 728,676"]):
    d.path(dd, f"Tail wave {i+1}", fill=NONE, stroke="#100A06",
           strokeWidth=3.5, opacity=50, cap="round")

# far legs — dimmer, set back half a step
d.path(leg((458, 590), (452, 660), (446, 724), 30, 20, 13),
       "Foreleg far", fill=DIM_GRAD, stroke=INK, strokeWidth=4.5)
d.path(leg((636, 586), (646, 656), (656, 720), 34, 21, 13),
       "Hind leg far", fill=DIM_GRAD, stroke=INK, strokeWidth=4.5)

# body — the wide deep barrel, low to the ground, back level
d.path(smooth([(408, 536), (430, 496), (480, 478), (552, 472), (616, 474),
               (660, 480), (688, 512), (698, 556), (686, 600), (650, 632),
               (580, 646), (500, 650), (442, 640), (410, 606), (400, 566)]),
       "Body", fill=COAT_GRAD, stroke=INK, strokeWidth=6)
# topline sheen — thin grey daylight along the back
d.path("M432,498 C500,478 580,470 656,472 C584,482 508,490 434,506 Z",
       "Back sheen", fill="#D8D4B0", opacity=26, stroke=NONE)
# shaggy belly edge — ragged winter hair hanging under the barrel
for i, dd in enumerate(["M450,634 C452,646 450,656 444,664",
                        "M492,644 C494,656 492,666 486,674",
                        "M536,648 C538,660 536,668 530,676",
                        "M580,644 C582,656 580,664 574,672",
                        "M624,634 C626,646 624,654 618,662"]):
    d.path(dd, f"Belly shag {i+1}", fill=NONE, stroke="#2C1E12",
           strokeWidth=4, opacity=60, cap="round")

# near legs — short, sturdy, planted square
d.path(leg((428, 596), (424, 664), (416, 732), 34, 22, 14),
       "Foreleg near", fill=COAT_GRAD, stroke=INK, strokeWidth=5)
d.path(leg((612, 590), (622, 660), (632, 726), 38, 22, 14),
       "Hind leg near", fill=COAT_GRAD, stroke=INK, strokeWidth=5)
# fetlock tufts — soft hair over the pasterns
for i, (cx, cy) in enumerate([(416, 730), (446, 722), (632, 724), (656, 718)]):
    d.path(smooth([(cx - 14, cy - 10), (cx - 16, cy + 4), (cx - 8, cy + 14),
                   (cx + 6, cy + 16), (cx + 14, cy + 8), (cx + 12, cy - 6)]),
           f"Fetlock {i+1}", fill=COAT_GRAD, stroke=INK, strokeWidth=3)

# neck — short, deep, carried low into the wind
d.path(smooth([(318, 480), (340, 448), (356, 422), (380, 416), (408, 434),
               (432, 462), (448, 492), (444, 524), (410, 532), (368, 514),
               (336, 500)]),
       "Neck", fill=COAT_GRAD, stroke=INK, strokeWidth=5)

# head — broad pony brow, short deep face, muzzle fine
d.path(smooth([(356, 416), (330, 428), (302, 448), (280, 470), (268, 488),
               (266, 502), (274, 514), (292, 520), (316, 520), (340, 506),
               (354, 480)]),
       "Head", fill=COAT_GRAD, stroke=INK, strokeWidth=5)
# muzzle — soft and small
d.path(smooth([(266, 490), (264, 504), (272, 516), (290, 520), (304, 514),
               (304, 500), (294, 488), (278, 486)]),
       "Muzzle", fill="#4A3420", opacity=60, stroke=NONE)
# nostril
d.path("M272,496 C270,502 274,508 280,508 C286,506 288,500 284,495 "
       "C280,492 274,492 272,496 Z", "Nostril", fill="#120B06",
       stroke=INK, strokeWidth=2.5)
# mouth — level
d.path("M280,512 C290,514 300,512 308,508", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=3, cap="round")

# ears — small, wide-set, pricked but soft
d.path("M348,418 L338,386 L362,406 Z", "Ear near", fill=COAT_GRAD,
       stroke=INK, strokeWidth=4)
d.path("M362,420 L358,390 L378,410 Z", "Ear far", fill=DIM_GRAD,
       stroke=INK, strokeWidth=3.5)

# the eye — big, dark, kind; peeking out under the forelock hem
d.path("M296,464 C302,456 314,454 322,460 C320,470 308,474 298,470 "
       "C294,468 294,466 296,464 Z", "Eye",
       fill=rad((0, "#5E4020"), (0.7, "#382512"), (1, "#1A100A")),
       stroke=INK, strokeWidth=3)
d.shape("ellipse", "Pupil", x=305, y=461, width=9, height=10, fill="#0C0705", stroke=NONE)
d.shape("ellipse", "Glint", x=308, y=462, width=4, height=4, fill="#FFF4D8", opacity=85, stroke=NONE)

# mane — the moor signature: a heavy bushy fall blown flat along the crest,
# all strands combed right by the wind
d.path(smooth([(350, 410), (388, 402), (428, 410), (462, 428), (482, 452),
               (490, 478), (478, 496), (458, 492), (436, 498), (414, 490),
               (396, 496), (376, 486), (360, 468), (348, 440), (344, 420)]),
       "Mane", fill=MANE_GRAD, stroke=INK, strokeWidth=4)
for i, dd in enumerate(["M364,414 C400,410 438,420 470,442",
                        "M368,436 C402,432 440,442 474,464",
                        "M372,458 C404,456 440,464 470,484"]):
    d.path(dd, f"Mane wind {i+1}", fill=NONE, stroke="#0F0A06",
           strokeWidth=3.5, opacity=55, cap="round")
# forelock — the thick curtain tumbling over the face, ends swept right
d.path(smooth([(344, 412), (326, 424), (314, 444), (310, 468), (316, 486),
               (328, 490), (336, 474), (342, 452), (352, 430), (356, 416)]),
       "Forelock", fill=MANE_GRAD, stroke=INK, strokeWidth=3.5)
for i, dd in enumerate(["M330,428 C322,442 318,458 318,474",
                        "M340,424 C334,440 330,458 330,476"]):
    d.path(dd, f"Forelock strand {i+1}", fill=NONE, stroke="#100A06",
           strokeWidth=3, opacity=60, cap="round")

# shag texture — guard-hair ticks along the topline and rump
for i, dd in enumerate(["M448,492 C452,484 458,478 466,474",
                        "M500,478 C506,470 514,466 522,464",
                        "M560,472 C568,466 576,464 584,464",
                        "M616,476 C624,472 632,472 640,474"]):
    d.path(dd, f"Coat tick {i+1}", fill=NONE, stroke="#332416",
           strokeWidth=3.5, opacity=50, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#243A24", strokeWidth=6)

# --- captions -------------------------------------------------------------------
d.text("SHETLAND PONY", "Name", x=500, y=934, size=56, font="Virelai Sans",
       color="#EDEACB", justify="center")
LINE2, SZ2, TRK = "PONY · SHETLAND ISLES", 22, 280
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

d.finish("shetland-pony-V1R00")
