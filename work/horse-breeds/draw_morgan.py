#!/usr/bin/env python3
"""Morgan — milestone card V1R00. One clean profile of the compact
bay: arched neck held high, head up and proud but the eye stays kind,
hind pair parked a half-step back in the show stance, tail carried
high off the croup. Black points on the bay coat. A Vermont pasture —
rolling hill, rail fence on the floor, dusk-green disc closing on
its own arc. 1000x1000. House style: gradients + translucent
shading, never flat fills. Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Morgan — Milestone Card", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#231A12"                    # warm dark ink, never pure black


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


BG_GRAD = lin(0, 0, 0, 1000, (0, "#131A15"), (1, "#070A07"))
PLATE_GRAD = rad((0, "#A6B284"), (0.55, "#6F8258"), (1, "#3C4A34"))
COAT_GRAD = lin(320, 360, 700, 760, (0, "#A06A38"), (0.5, "#754C26"), (1, "#462A14"))
DIM_GRAD = lin(320, 360, 700, 760, (0, "#7A4E28"), (1, "#38200F"))
POINT_GRAD = lin(340, 360, 760, 740, (0, "#34261A"), (0.6, "#1E150D"), (1, "#120C07"))
FLOOR_GRAD = lin(0, 720, 0, 880, (0, "#5C5E38"), (0.55, "#40422A"), (1, "#222314"))
FENCE = "#DCD6BE"

# --- backdrop + dusk pasture plate -------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#2C3C28", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E0E4C2", strokeWidth=3, opacity=38)

# late light pooling upper-left over the pasture
d.shape("ellipse", "Light pool", x=240, y=140, width=420, height=230,
        fill="#EFE8C2", opacity=15, stroke=NONE)
# haze lenses drifting
for i, (x, y, w) in enumerate([(330, 310, 96), (580, 230, 74), (716, 350, 84),
                               (250, 480, 62), (460, 170, 56)]):
    assert on_disc(x, y, 20), i
    d.shape("ellipse", f"Haze {i+1}", x=x - w / 2, y=y - w / 6, width=w, height=w * 0.33,
            fill="#E4E8C0", opacity=11, stroke=NONE)

# --- pasture floor, closing on the disc arc ------------------------------------------
fy = 782
fl, fr = rim_x(fy, -1), rim_x(fy, 1)
d.path(f"M{fl:.1f},{fy} C300,770 400,790 500,782 C600,774 700,780 {fr:.1f},{fy} "
       f"A{PR},{PR} 0 0 1 {fl:.1f},{fy} Z", "Floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{fl + 8:.0f},{fy} C300,770 400,790 500,782 C600,774 700,780 {fr - 8:.0f},{fy}",
       "Floor crest", fill=NONE, stroke="#9C9A60", strokeWidth=5, opacity=42, cap="round")
# rolling hill on the skyline behind the horse
HILL = [(560, 776), (596, 742), (646, 736), (698, 748), (742, 764), (758, 776)]
for x, y in HILL:
    assert on_disc(x, y, 8), (x, y)
d.path(smooth(HILL, k=0.5), "Hill", fill="#4E5234", opacity=45, stroke=NONE)
# a short two-rail pasture fence on the left stretch
for i, (x, y0, y1) in enumerate([(268, 736, 776), (330, 738, 778), (392, 740, 778)]):
    d.path(f"M{x},{y0} L{x},{y1}", f"Fence post {i+1}", fill=NONE,
           stroke=FENCE, strokeWidth=5, opacity=45, cap="round")
d.path(f"M258,738 C300,736 360,738 404,740", "Fence rail 1", fill=NONE,
       stroke=FENCE, strokeWidth=4.5, opacity=45, cap="round")
d.path(f"M260,756 C302,754 362,756 402,758", "Fence rail 2", fill=NONE,
       stroke=FENCE, strokeWidth=4, opacity=38, cap="round")
# pasture grass ticks on the crest
for i, (x, y) in enumerate([(440, 818), (540, 830), (640, 816)]):
    assert on_disc(x, y + 8, 14), i
    for j, (dx, dy) in enumerate([(-12, 8), (-4, -8), (3, -12), (11, -4)]):
        d.path(f"M{x + dx * 0.4:.0f},{y + 12} L{x + dx:.0f},{y + dy:.0f}",
               f"Grass {i+1}.{j+1}", fill=NONE, stroke="#6E6C40",
               strokeWidth=3.5, opacity=60, cap="round")

# shadow under the parked stance
d.shape("ellipse", "Horse shadow", x=310, y=752, width=420, height=28,
        fill="#141106", opacity=32, stroke=NONE)

# --- the morgan, clean profile, head high, facing left -------------------------------
# tail — carried high, a dark flag off the croup
d.path(smooth([(640, 462), (676, 452), (712, 468), (736, 506), (748, 556),
               (744, 608), (730, 648), (714, 656), (702, 622), (694, 570),
               (678, 522), (656, 490)]),
       "Tail", fill=POINT_GRAD, stroke=INK, strokeWidth=5)
for i, dd in enumerate(["M682,480 C706,514 720,556 728,600",
                        "M672,506 C692,540 706,580 712,618"]):
    d.path(dd, f"Tail strand {i+1}", fill=NONE, stroke="#0C0705",
           strokeWidth=3.5, opacity=50, cap="round")

# far legs — dimmer, half a step back in the parked stance
d.path(leg((448, 556), (444, 646), (440, 724), 34, 18, 12),
       "Foreleg far", fill=DIM_GRAD, stroke=INK, strokeWidth=4.5)
d.path(leg((634, 560), (668, 646), (694, 726), 40, 19, 12),
       "Hind leg far", fill=DIM_GRAD, stroke=INK, strokeWidth=4.5)

# body — compact, short back, deep heartgirth, level croup
d.path(smooth([(402, 528), (426, 492), (470, 474), (536, 468), (596, 466),
               (634, 464), (664, 482), (680, 518), (678, 556), (652, 586),
               (592, 598), (512, 602), (452, 594), (420, 570), (404, 550)]),
       "Body", fill=COAT_GRAD, stroke=INK, strokeWidth=6)
# dusk sheen along the topline
d.path("M430,494 C498,474 576,466 646,466 C580,478 504,486 432,502 Z",
       "Back sheen", fill="#E8D9AE", opacity=28, stroke=NONE)
# barrel shade under the heartgirth
d.path(smooth([(460, 570), (530, 584), (600, 580), (636, 566), (612, 590),
               (540, 600), (470, 592)]),
       "Barrel shade", fill="#3A2210", opacity=30, stroke=NONE)

# near legs — clean, front vertical, hind parked a half-step back
d.path(leg((426, 560), (422, 650), (416, 730), 36, 19, 12),
       "Foreleg near", fill=COAT_GRAD, stroke=INK, strokeWidth=5)
d.path(leg((610, 564), (652, 652), (682, 732), 44, 20, 13),
       "Hind leg near", fill=COAT_GRAD, stroke=INK, strokeWidth=5)
# black points rising up the cannons
for i, dd in enumerate(["M416,700 C414,714 414,724 416,730",
                        "M682,700 C680,714 680,724 682,730",
                        "M440,694 C439,706 439,716 440,722",
                        "M694,696 C692,708 692,718 694,724"]):
    d.path(dd, f"Point {i+1}", fill=NONE, stroke="#241A10",
           strokeWidth=13, opacity=55, cap="round")

# neck — the arched upright crest, deep but refined
d.path(smooth([(314, 470), (332, 436), (344, 400), (364, 380), (388, 384),
               (416, 412), (440, 448), (454, 486), (452, 520), (420, 526),
               (378, 508), (344, 490)]),
       "Neck", fill=COAT_GRAD, stroke=INK, strokeWidth=5)

# head — refined, straight face held high, small ears
d.path(smooth([(356, 384), (334, 400), (316, 426), (306, 454), (304, 476),
               (310, 492), (324, 502), (344, 502), (362, 492), (372, 468),
               (372, 438), (364, 410)]),
       "Head", fill=COAT_GRAD, stroke=INK, strokeWidth=5)
# muzzle — fine, dark-tipped
d.path(smooth([(304, 462), (302, 480), (310, 496), (326, 502), (342, 498),
               (344, 484), (334, 470), (316, 466)]),
       "Muzzle", fill="#5E3C22", opacity=60, stroke=NONE)
# nostril
d.path("M310,478 C310,484 314,490 320,490 C326,488 327,482 323,477 "
       "C319,474 312,474 310,478 Z", "Nostril", fill="#140C06",
       stroke=INK, strokeWidth=2.5)
# mouth — level
d.path("M320,496 C330,498 340,496 348,492", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=3, cap="round")

# ears — small, pricked, alert
d.path("M352,388 L344,356 L366,378 Z", "Ear near", fill=COAT_GRAD,
       stroke=INK, strokeWidth=4)
d.path("M364,390 L360,360 L380,380 Z", "Ear far", fill=DIM_GRAD,
       stroke=INK, strokeWidth=3.5)
d.path("M348,380 L344,362", "Ear inner", fill=NONE, stroke="#0C0705",
       strokeWidth=3, opacity=55, cap="round")

# the eye — proud but kind: large, soft, dark, set high under the brow
d.path("M326,436 C332,428 344,426 352,432 C350,442 338,446 328,442 "
       "C324,440 324,438 326,436 Z", "Eye",
       fill=rad((0, "#6A4420"), (0.7, "#402812"), (1, "#1E1208")),
       stroke=INK, strokeWidth=3)
d.shape("ellipse", "Pupil", x=335, y=433, width=10, height=11, fill="#0C0604", stroke=NONE)
d.shape("ellipse", "Glint", x=338, y=434, width=4.5, height=4.5, fill="#FFF4D8", opacity=90, stroke=NONE)

# mane — black, fine, a short neat fall along the arched crest
d.path(smooth([(352, 380), (388, 384), (418, 408), (442, 438), (456, 472),
               (462, 502), (450, 522), (430, 518), (406, 506), (384, 488),
               (366, 464), (356, 436), (350, 408)]),
       "Mane", fill=POINT_GRAD, stroke=INK, strokeWidth=4)
for i, dd in enumerate(["M368,392 C394,400 420,420 440,446",
                        "M370,418 C394,430 416,452 432,478",
                        "M372,446 C392,458 410,478 422,500"]):
    d.path(dd, f"Mane strand {i+1}", fill=NONE, stroke="#0C0705",
           strokeWidth=3.5, opacity=55, cap="round")
# forelock — a modest dark lick between the ears
d.path(smooth([(350, 386), (342, 396), (340, 410), (346, 424), (352, 414),
               (356, 400), (356, 388)]),
       "Forelock", fill=POINT_GRAD, opacity=90, stroke=NONE)

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#26331F", strokeWidth=6)

# --- captions -------------------------------------------------------------------
d.text("MORGAN", "Name", x=500, y=934, size=56, font="Virelai Sans",
       color="#EDEAC9", justify="center")
LINE2, SZ2, TRK = "FOUNDATION · VERMONT", 22, 280
r = d.text(LINE2, "Milestone", x=500, y=970, size=SZ2, font="Virelai Sans",
           color="#C3C7A0", justify="center")
d.cmd("text.setStyle", "Milestone tracking", id=r["id"], tracking=TRK)

b = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("milestone bounds", {k: round(v) for k, v in b.items()})
nearest = (min(max(PCX, b["x"]), b["x"] + b["width"]),
           min(max(PCY, b["y"]), b["y"] + b["height"]))
clear = math.hypot(nearest[0] - PCX, nearest[1] - PCY) - (PR + 3)
print("clears rim by %.1f" % clear)
assert clear > 0 and b["width"] <= 760 and b["x"] >= 10 and b["x"] + b["width"] <= 990, b

d.finish("morgan-V1R00")
