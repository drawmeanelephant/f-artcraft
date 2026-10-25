#!/usr/bin/env python3
"""Friesian — milestone card V1R00. The black baroque horse at a
high-stepping trot: near foreleg raised and folded, arched crest,
near-vertical head carriage, extravagant wavy mane cascading down
the neck, tail sweeping low, feathered fetlocks. The silhouette does
the work — internal detail kept to cold sheens on the dark coat.
Moonlit slate disc, dark stable floor closing on the disc's own arc.
1000x1000. House style: gradients + translucent shading, never flat
fills. Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Friesian — Milestone Card", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#15171D"                    # cold dark ink, never pure black


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


def feather(cx, cy):
    """Fetlock feather — a wavy fall of hair hooding the hoof."""
    pts = [(cx - 16, cy - 18), (cx - 20, cy - 4), (cx - 18, cy + 12),
           (cx - 8, cy + 18), (cx + 4, cy + 16), (cx + 14, cy + 18),
           (cx + 18, cy + 8), (cx + 16, cy - 6), (cx + 10, cy - 16),
           (cx - 4, cy - 20)]
    return smooth(pts, k=0.55)


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


BG_GRAD = lin(0, 0, 0, 1000, (0, "#141923"), (1, "#07090D"))
PLATE_GRAD = rad((0, "#AFBCCC"), (0.55, "#77859A"), (1, "#454E5E"))
COAT_GRAD = lin(330, 360, 720, 740, (0, "#3C3A40"), (0.5, "#26242A"), (1, "#121014"))
DIM_GRAD = lin(330, 360, 720, 740, (0, "#2A2830"), (1, "#0E0C10"))
FLOOR_GRAD = lin(0, 720, 0, 880, (0, "#4E5462"), (0.55, "#383D4A"), (1, "#1E212B"))
SHEEN = "#8E9CB4"

# --- backdrop + moonlit plate ----------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#323947", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8E2EE", strokeWidth=3, opacity=38)

# moonlight pooling upper-left
d.shape("ellipse", "Light pool", x=230, y=140, width=420, height=230,
        fill="#E8EEF6", opacity=14, stroke=NONE)
# thin haze lenses
for i, (x, y, w) in enumerate([(340, 300, 100), (580, 230, 80), (720, 350, 90),
                               (250, 480, 66), (460, 170, 60)]):
    assert on_disc(x, y, 20), i
    d.shape("ellipse", f"Haze {i+1}", x=x - w / 2, y=y - w / 6, width=w, height=w * 0.33,
            fill="#DCE6F2", opacity=10, stroke=NONE)

# --- stable floor, closing on the disc arc ----------------------------------------
fy = 782
fl, fr = rim_x(fy, -1), rim_x(fy, 1)
d.path(f"M{fl:.1f},{fy} C300,772 400,792 500,786 C600,780 700,784 {fr:.1f},{fy} "
       f"A{PR},{PR} 0 0 1 {fl:.1f},{fy} Z", "Floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{fl + 8:.0f},{fy} C300,772 400,792 500,786 C600,780 700,784 {fr - 8:.0f},{fy}",
       "Floor crest", fill=NONE, stroke="#8E97A8", strokeWidth=5, opacity=42, cap="round")

# soft shadow the trot lands on
d.shape("ellipse", "Horse shadow", x=330, y=748, width=400, height=28,
        fill="#0E0F14", opacity=32, stroke=NONE)

# --- the friesian, high-stepping trot, facing left ---------------------------------
# tail — extravagant, sweeping low off the croup, ends curling
d.path(smooth([(664, 464), (712, 500), (748, 552), (772, 612), (784, 668),
               (776, 710), (756, 728), (738, 716), (736, 672), (722, 616),
               (696, 560), (664, 516), (648, 492)]),
       "Tail", fill=COAT_GRAD, stroke=INK, strokeWidth=5)
for i, dd in enumerate(["M700,540 C724,584 742,632 752,684",
                        "M688,566 C710,606 726,650 734,696",
                        "M716,530 C738,570 754,616 764,664"]):
    d.path(dd, f"Tail wave {i+1}", fill=NONE, stroke="#0B090C",
           strokeWidth=3.5, opacity=55, cap="round")

# far legs — dimmer, half a stride behind, roots tucked under the barrel
d.path(leg((452, 556), (432, 650), (418, 728), 34, 15, 10),
       "Foreleg far", fill=DIM_GRAD, stroke=INK, strokeWidth=4.5)
d.path(leg((648, 548), (612, 614), (566, 652), 40, 17, 11),
       "Hind leg far", fill=DIM_GRAD, stroke=INK, strokeWidth=4.5)

# body — powerful baroque barrel, high croup
d.path(smooth([(404, 524), (432, 490), (486, 476), (560, 472), (626, 466),
               (662, 458), (690, 482), (702, 522), (690, 558), (648, 580),
               (576, 590), (500, 594), (442, 584), (412, 560)]),
       "Body", fill=COAT_GRAD, stroke=INK, strokeWidth=6)
# cold sheens on the dark coat — the only internal modelling
d.path("M430,494 C500,472 590,464 658,458 C590,474 505,482 432,500 Z",
       "Back sheen", fill=SHEEN, opacity=26, stroke=NONE)
d.path(smooth([(430, 528), (456, 540), (462, 566), (446, 584), (422, 580),
               (412, 554)]),
       "Shoulder sheen", fill=SHEEN, opacity=16, stroke=NONE)

# near legs — the signature: fore folded high, hind planted driving
d.path(leg((430, 546), (514, 540), (486, 608), 38, 17, 11),
       "Foreleg near", fill=COAT_GRAD, stroke=INK, strokeWidth=5)
d.path(leg((622, 552), (642, 654), (610, 738), 44, 18, 12),
       "Hind leg near", fill=COAT_GRAD, stroke=INK, strokeWidth=5)

# feathered fetlocks hooding every hoof — the breed mark
for i, (cx, cy) in enumerate([(486, 606), (418, 726), (610, 736), (566, 652)]):
    d.path(feather(cx, cy), f"Feather {i+1}", fill=COAT_GRAD,
           stroke=INK, strokeWidth=3.5)
for i, (cx, cy) in enumerate([(482, 622), (614, 750)]):
    d.path(feather(cx, cy), f"Feather shade {i+1}", fill="#0B090C",
           opacity=45, stroke=NONE)

# neck — the arched baroque crest, deep and powerful
d.path(smooth([(312, 458), (330, 420), (344, 384), (368, 366), (392, 376),
               (418, 412), (440, 452), (456, 492), (450, 528), (414, 530),
               (372, 508), (338, 486)]),
       "Neck", fill=COAT_GRAD, stroke=INK, strokeWidth=5)

# head — near-vertical carriage, long noble face, small muzzle
d.path(smooth([(354, 370), (330, 390), (316, 424), (310, 458), (312, 482),
               (322, 496), (340, 502), (360, 498), (378, 484), (386, 458),
               (384, 428), (372, 398)]),
       "Head", fill=COAT_GRAD, stroke=INK, strokeWidth=5)
# muzzle — finer than the face
d.path(smooth([(310, 460), (310, 482), (320, 498), (338, 502), (354, 496),
               (356, 478), (346, 464), (326, 460)]),
       "Muzzle", fill="#1C1A20", opacity=70, stroke=NONE)
# nostril
d.path("M318,484 C318,490 322,496 328,496 C334,494 335,488 331,483 "
       "C327,480 320,480 318,484 Z", "Nostril", fill="#080608",
       stroke=INK, strokeWidth=2.5)
# mouth — level
d.path("M326,500 C336,502 346,500 354,496", "Mouth", fill=NONE,
       stroke="#060507", strokeWidth=3, cap="round")

# ears — small, alert, pricked
d.path("M352,376 L344,342 L368,364 Z", "Ear near", fill=COAT_GRAD,
       stroke=INK, strokeWidth=4)
d.path("M366,378 L362,346 L384,368 Z", "Ear far", fill=DIM_GRAD,
       stroke=INK, strokeWidth=3.5)
d.path("M348,368 L344,350", "Ear inner", fill=NONE, stroke="#080608",
       strokeWidth=3, opacity=55, cap="round")

# the eye — quiet, dark, kind beneath the brow
d.path("M330,432 C336,424 348,422 356,428 C354,438 342,442 332,438 "
       "C328,436 328,434 330,432 Z", "Eye",
       fill=rad((0, "#4A3520"), (0.7, "#2C1E10"), (1, "#140D08")),
       stroke=INK, strokeWidth=3)
d.shape("ellipse", "Pupil", x=339, y=429, width=9, height=10, fill="#0A0604", stroke=NONE)
d.shape("ellipse", "Glint", x=342, y=430, width=4, height=4, fill="#EAF0F8", opacity=90, stroke=NONE)

# mane — the extravagant fall: one heavy mass riding the crest, hanging
# in waves over the neck face, its hem kept inside the throat silhouette
d.path(smooth([(348, 362), (388, 366), (424, 394), (452, 434), (470, 478),
               (480, 514), (458, 540), (430, 532), (400, 516), (374, 498),
               (360, 476), (356, 450), (354, 424), (350, 392)]),
       "Mane", fill=DIM_GRAD, stroke=INK, strokeWidth=4)
# wave strokes inside the fall
for i, dd in enumerate(["M366,382 C394,402 418,432 436,470",
                        "M362,410 C388,432 410,464 424,502",
                        "M360,440 C382,462 400,494 412,528",
                        "M380,376 C404,392 428,418 446,452"]):
    d.path(dd, f"Mane wave {i+1}", fill=NONE, stroke="#0B090C",
           strokeWidth=3.5, opacity=55, cap="round")
# forelock spilling between the ears over the brow
d.path(smooth([(348, 370), (338, 382), (336, 398), (342, 412), (350, 402),
               (356, 388), (356, 374)]),
       "Forelock", fill=DIM_GRAD, opacity=90, stroke=NONE)
# crest sheen tracing the arch, over the mane
d.path("M352,372 C376,362 402,374 426,404 C402,382 376,372 356,378 Z",
       "Crest sheen", fill=SHEEN, opacity=30, stroke=NONE)

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#2B303C", strokeWidth=6)

# --- captions -------------------------------------------------------------------
d.text("FRIESIAN", "Name", x=500, y=934, size=56, font="Virelai Sans",
       color="#E8EDF4", justify="center")
LINE2, SZ2, TRK = "BAROQUE · FRIESLAND", 22, 280
r = d.text(LINE2, "Milestone", x=500, y=970, size=SZ2, font="Virelai Sans",
           color="#B9C3D2", justify="center")
d.cmd("text.setStyle", "Milestone tracking", id=r["id"], tracking=TRK)

b = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("milestone bounds", {k: round(v) for k, v in b.items()})
nearest = (min(max(PCX, b["x"]), b["x"] + b["width"]),
           min(max(PCY, b["y"]), b["y"] + b["height"]))
clear = math.hypot(nearest[0] - PCX, nearest[1] - PCY) - (PR + 3)
print("clears rim by %.1f" % clear)
assert clear > 0 and b["width"] <= 760 and b["x"] >= 10 and b["x"] + b["width"] <= 990, b

d.finish("friesian-V1R00")
