#!/usr/bin/env python3
"""Mustang — milestone card V1R00. The feral survivor in a suspended
gallop: all four legs off the ground, fore pair reaching, hind pair
trailing, wiry dun body, long tangled mane and tail streaming back,
head stretched low into the desert wind. Dust puffs off a dry floor
that closes on the disc's own arc; a far mesa on the skyline gives
the distance. Muted desert-storm light. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Mustang — Milestone Card", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#2A2016"                    # warm dark ink, never pure black


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


BG_GRAD = lin(0, 0, 0, 1000, (0, "#1B1D19"), (1, "#090B09"))
PLATE_GRAD = rad((0, "#C9B691"), (0.55, "#9E8C68"), (1, "#57503C"))
COAT_GRAD = lin(300, 420, 720, 680, (0, "#C29E66"), (0.5, "#9A7648"), (1, "#6B4E2E"))
DIM_GRAD = lin(300, 420, 720, 680, (0, "#8A6C44"), (1, "#4C361F"))
POINT_GRAD = lin(360, 380, 820, 680, (0, "#3E2E1C"), (0.6, "#241A10"), (1, "#171009"))
FLOOR_GRAD = lin(0, 720, 0, 880, (0, "#71603F"), (0.55, "#52452C"), (1, "#2E2717"))
DUST = "#DEC99A"

# --- backdrop + storm-dust plate ----------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#40382A", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8DCB4", strokeWidth=3, opacity=38)

# storm light pooling upper-left
d.shape("ellipse", "Light pool", x=230, y=140, width=420, height=230,
        fill="#F0E4BC", opacity=14, stroke=NONE)
# wind lenses — the desert air in motion
for i, (x, y, w) in enumerate([(330, 300, 100), (560, 230, 80), (710, 340, 90),
                               (240, 470, 66), (750, 470, 70), (460, 170, 60)]):
    assert on_disc(x, y, 20), i
    d.shape("ellipse", f"Wind {i+1}", x=x - w / 2, y=y - w / 6, width=w, height=w * 0.33,
            fill="#E6D9AE", opacity=11, stroke=NONE)

# --- desert floor, closing on the disc arc --------------------------------------
fy = 782
fl, fr = rim_x(fy, -1), rim_x(fy, 1)
d.path(f"M{fl:.1f},{fy} C300,770 380,792 480,784 C580,776 700,782 {fr:.1f},{fy} "
       f"A{PR},{PR} 0 0 1 {fl:.1f},{fy} Z", "Floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{fl + 8:.0f},{fy} C300,770 380,792 480,784 C580,776 700,782 {fr - 8:.0f},{fy}",
       "Floor crest", fill=NONE, stroke="#A08C58", strokeWidth=5, opacity=42, cap="round")

# far mesa — one flat-top butte on the skyline, deep in the dust
MESA = [(250, 772), (258, 728), (346, 722), (362, 768)]
for x, y in MESA:
    assert on_disc(x, y, 8), (x, y)
d.path(smooth(MESA, k=0.3), "Mesa", fill="#5A4C34", opacity=42, stroke=NONE)
# dry grass ticks rooted on the crest
for i, (x, y) in enumerate([(350, 800), (430, 826), (560, 832), (660, 820), (704, 790)]):
    assert on_disc(x, y + 8, 14), i
    for j, (dx, dy) in enumerate([(-12, 8), (-4, -8), (3, -12), (11, -4)]):
        d.path(f"M{x + dx * 0.4:.0f},{y + 12} L{x + dx:.0f},{y + dy:.0f}",
               f"Grass {i+1}.{j+1}", fill=NONE, stroke="#6E5C38",
               strokeWidth=3.5, opacity=60, cap="round")

# dust kicked off the floor behind the gallop — corners stay inside the rim
for i, (x, y, w, h, op) in enumerate([(640, 736, 170, 40, 18), (470, 750, 190, 42, 17),
                                      (330, 736, 140, 34, 15)]):
    for cx in (x - w / 2, x + w / 2):
        assert on_disc(cx, y, 8), (i, cx, y)
    d.shape("ellipse", f"Dust {i+1}", x=x - w / 2, y=y - h / 2, width=w, height=h,
            fill=DUST, opacity=op, stroke=NONE)

# long soft shadow racing under the airborne horse
d.shape("ellipse", "Horse shadow", x=290, y=756, width=440, height=30,
        fill="#171206", opacity=30, stroke=NONE)

# --- the mustang, suspended gallop, facing left ---------------------------------
# tail — long and tangled, streaming back off the croup
d.path(smooth([(668, 468), (720, 448), (776, 436), (822, 434), (836, 450),
               (818, 474), (770, 490), (718, 498), (678, 500)]),
       "Tail", fill=POINT_GRAD, stroke=INK, strokeWidth=5)
for i, dd in enumerate(["M700,468 C742,454 784,448 820,450",
                        "M696,484 C738,474 780,468 812,472",
                        "M714,454 C752,442 792,438 824,442"]):
    d.path(dd, f"Tail strand {i+1}", fill=NONE, stroke="#0F0A06",
           strokeWidth=3.5, opacity=50, cap="round")

# far legs first — dimmer, tucked half a stride behind
d.path(leg((452, 554), (396, 618), (356, 668), 36, 16, 10),
       "Foreleg far", fill=DIM_GRAD, stroke=INK, strokeWidth=4.5)
d.path(leg((640, 548), (698, 598), (744, 650), 42, 18, 11),
       "Hind leg far", fill=DIM_GRAD, stroke=INK, strokeWidth=4.5)

# body — lean barrel, tucked-up flank, wiry not fat
d.path(smooth([(404, 528), (436, 500), (490, 492), (560, 490), (622, 486),
               (660, 472), (688, 492), (700, 528), (688, 560), (648, 578),
               (580, 584), (500, 588), (444, 580), (412, 560)]),
       "Body", fill=COAT_GRAD, stroke=INK, strokeWidth=6)
# topline sheen — storm light along the back
d.path("M436,502 C510,486 590,482 656,474 C590,490 510,494 438,508 Z",
       "Back sheen", fill="#EAD9AC", opacity=30, stroke=NONE)
# dun dorsal stripe — the primitive mark riding the spine itself
d.path("M442,498 C514,486 590,482 654,470", "Dorsal stripe", fill=NONE,
       stroke="#3A2A18", strokeWidth=6, opacity=50, cap="round")
# soft flank shadow, not a contour line
d.path(smooth([(470, 560), (540, 570), (620, 566), (660, 552), (640, 576),
               (560, 586), (490, 584)]),
       "Flank shade", fill="#4C361E", opacity=22, stroke=NONE)

# near legs over the body — one hard joint each, never sausages
d.path(leg((430, 556), (362, 612), (298, 650), 38, 17, 11),
       "Foreleg near", fill=COAT_GRAD, stroke=INK, strokeWidth=5)
d.path(leg((616, 552), (692, 606), (762, 660), 46, 19, 12),
       "Hind leg near", fill=COAT_GRAD, stroke=INK, strokeWidth=5)
# hooves — small dark points tipping each cannon
for i, (cx, cy, ang) in enumerate([(306, 652, -30), (356, 668, -25),
                                   (758, 660, 35), (742, 650, 30)]):
    c, s = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    pts = [(cx + 13 * c - 8 * s, cy + 13 * s + 8 * c),
           (cx + 15 * c + 5 * s, cy + 15 * s - 5 * c),
           (cx + 4 * c + 11 * s, cy + 4 * s - 11 * c),
           (cx - 12 * c + 7 * s, cy - 12 * s - 7 * c),
           (cx - 14 * c - 4 * s, cy - 14 * s + 4 * c)]
    d.path(smooth(pts, k=0.7), f"Hoof {i+1}", fill="#1C130C", stroke=NONE)

# neck — stretched forward and low, deep through the base into the chest
d.path(smooth([(312, 474), (342, 446), (354, 424), (378, 424), (406, 448),
               (432, 484), (456, 516), (452, 550), (412, 552), (366, 524),
               (330, 498)]),
       "Neck", fill=COAT_GRAD, stroke=INK, strokeWidth=5)

# head — long and plain, straight face running into the wind
d.path(smooth([(356, 420), (332, 432), (300, 450), (272, 468), (256, 482),
               (252, 496), (260, 506), (282, 512), (312, 512), (338, 498),
               (352, 476)]),
       "Head", fill=COAT_GRAD, stroke=INK, strokeWidth=5)
# muzzle — darker tip
d.path(smooth([(252, 484), (250, 498), (260, 508), (280, 510), (294, 504),
               (294, 490), (282, 480), (264, 478)]),
       "Muzzle", fill="#4C3620", opacity=55, stroke=NONE)
# nostril — flared, working
d.path("M262,490 C260,496 264,502 270,502 C276,500 278,494 274,489 "
       "C270,486 264,486 262,490 Z", "Nostril", fill="#140D08",
       stroke=INK, strokeWidth=2.5)
# mouth line — level, no smile
d.path("M274,504 C286,506 298,504 308,500", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=3, cap="round")

# ears — short, alert, tipped into the wind
d.path("M350,424 L340,388 L366,412 Z", "Ear near", fill=COAT_GRAD,
       stroke=INK, strokeWidth=4)
d.path("M364,426 L360,392 L384,416 Z", "Ear far", fill=DIM_GRAD,
       stroke=INK, strokeWidth=3.5)
d.path("M346,416 L342,396", "Ear inner", fill=NONE, stroke="#0F0A06",
       strokeWidth=3, opacity=55, cap="round")

# the eye — dark almond, calm-hard, set high
d.path("M314,456 C320,448 332,446 340,452 C338,462 326,466 316,462 "
       "C312,460 312,458 314,456 Z", "Eye",
       fill=rad((0, "#5E4020"), (0.7, "#3A2712"), (1, "#1E130A")),
       stroke=INK, strokeWidth=3)
d.shape("ellipse", "Pupil", x=323, y=453, width=9, height=10, fill="#0E0806", stroke=NONE)
d.shape("ellipse", "Glint", x=326, y=454, width=4, height=4, fill="#FFF4D8", opacity=90, stroke=NONE)

# mane — one heavy fall draped over the crest, ends tearing back in the wind
d.path(smooth([(348, 418), (390, 402), (448, 404), (512, 420), (566, 446),
               (548, 462), (492, 452), (440, 446), (398, 448), (364, 442)]),
       "Mane", fill=POINT_GRAD, opacity=92, stroke=NONE)
d.path(smooth([(390, 442), (440, 430), (500, 434), (556, 454), (540, 470),
               (486, 464), (432, 460), (396, 458)]),
       "Mane lower", fill=POINT_GRAD, opacity=85, stroke=NONE)
for i, dd in enumerate(["M360,422 C410,412 470,414 528,432",
                        "M372,436 C424,426 484,428 544,448",
                        "M394,450 C444,442 500,444 552,462",
                        "M360,418 C376,408 396,402 418,400"]):
    d.path(dd, f"Mane tangle {i+1}", fill=NONE, stroke="#0F0A06",
           strokeWidth=3.5, opacity=55, cap="round")
# loose ends snapping past the mass
for i, dd in enumerate(["M556,448 C580,442 602,442 622,450",
                        "M540,462 C564,460 586,462 606,470",
                        "M512,424 C536,418 560,418 580,426"]):
    d.path(dd, f"Mane fly {i+1}", fill=NONE, stroke="#241A10",
           strokeWidth=4, opacity=70, cap="round")
# forelock spilling over the face between the ears
d.path(smooth([(348, 420), (336, 430), (330, 444), (332, 458), (342, 452),
               (350, 438), (356, 426)]),
       "Forelock", fill=POINT_GRAD, opacity=90, stroke=NONE)

# a last breath of dust over the trailing hoof
d.shape("ellipse", "Dust kick", x=700, y=690, width=90, height=26,
        fill=DUST, opacity=16, stroke=NONE)

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#332D1F", strokeWidth=6)

# --- captions -------------------------------------------------------------------
d.text("MUSTANG", "Name", x=500, y=934, size=56, font="Virelai Sans",
       color="#EDE6C6", justify="center")
LINE2, SZ2, TRK = "FERAL · AMERICAN WEST", 22, 280
r = d.text(LINE2, "Milestone", x=500, y=970, size=22, font="Virelai Sans",
           color="#C6BB96", justify="center")
d.cmd("text.setStyle", "Milestone tracking", id=r["id"], tracking=TRK)

b = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("milestone bounds", {k: round(v) for k, v in b.items()})
nearest = (min(max(PCX, b["x"]), b["x"] + b["width"]),
           min(max(PCY, b["y"]), b["y"] + b["height"]))
clear = math.hypot(nearest[0] - PCX, nearest[1] - PCY) - (PR + 3)
print("clears rim by %.1f" % clear)
assert clear > 0 and b["width"] <= 760 and b["x"] >= 10 and b["x"] + b["width"] <= 990, b

d.finish("mustang-V1R00")
