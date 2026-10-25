#!/usr/bin/env python3
"""Andalusian — milestone card V1R00. The grey baroque horse in a
collected canter / near-piaffe: croup lowered, near fore raised and
folded, face near-vertical, thick wavy mane spilling down the neck,
long full tail. Classical school silhouette, no tack. Iberian world:
dusty ochre arena floor, a faint sierra ridge high on the disc.
1000x1000. House style: gradients + translucent shading, never flat
fills. Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Andalusian — Milestone Card", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#241B14"                    # warm dark ink, never pure black


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


BG_GRAD = lin(0, 0, 0, 1000, (0, "#1B1712"), (1, "#0B0806"))
PLATE_GRAD = rad((0, "#D2BC8E"), (0.55, "#97825E"), (1, "#4D4029"))
COAT_GRAD = lin(330, 360, 720, 780, (0, "#D9D2C4"), (0.5, "#ABA495"), (1, "#6E6659"))
DIM_GRAD = lin(330, 360, 720, 780, (0, "#8F887B"), (1, "#4A4439"))
HAIR_GRAD = lin(360, 380, 480, 560, (0, "#3A3028"), (1, "#16100B"))
FLOOR_GRAD = lin(0, 730, 0, 880, (0, "#7A6A46"), (0.55, "#56482C"), (1, "#2A2214"))
SHEEN = "#EDE6D4"

# --- backdrop + Iberian dusk plate -------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#3A3220", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#EDE4BE", strokeWidth=3, opacity=38)

# sierra ridge lines high on the disc — the Iberian skyline
d.path("M150,290 C260,272 340,284 430,270 C540,254 640,272 740,262 C790,258 830,264 856,258",
       "Sierra ridge 1", fill=NONE, stroke="#5E5234", strokeWidth=4,
       opacity=28, cap="round")
d.path("M190,326 C300,312 420,322 530,310 C640,298 740,312 820,304",
       "Sierra ridge 2", fill=NONE, stroke="#6E6040", strokeWidth=3.5,
       opacity=22, cap="round")
# late light pooling upper-left
d.shape("ellipse", "Light pool", x=240, y=145, width=410, height=230,
        fill="#F0E2B8", opacity=13, stroke=NONE)
# dust lenses
for i, (x, y, w) in enumerate([(330, 375, 90), (575, 250, 70), (720, 400, 80),
                               (255, 495, 60), (750, 505, 64), (460, 205, 55)]):
    assert on_disc(x, y, 20), i
    d.shape("ellipse", f"Dust {i+1}", x=x - w / 2, y=y - w / 5, width=w, height=w * 0.4,
            fill="#EADCB0", opacity=10, stroke=NONE)

# --- arena floor, closing on the disc arc ------------------------------------------
fy = 782
fl, fr = rim_x(fy, -1), rim_x(fy, 1)
d.path(f"M{fl:.1f},{fy} C300,770 400,792 500,784 C600,776 700,780 {fr:.1f},{fy} "
       f"A{PR},{PR} 0 0 1 {fl:.1f},{fy} Z", "Floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{fl + 8:.0f},{fy} C300,770 400,792 500,784 C600,776 700,780 {fr - 8:.0f},{fy}",
       "Floor crest", fill=NONE, stroke="#B8A468", strokeWidth=5, opacity=40, cap="round")
d.path("M330,822 C430,810 560,808 680,816", "Sod line", fill=NONE,
       stroke="#3E3620", strokeWidth=4, opacity=45, cap="round")
# dry-grass tufts on the crest
for i, (x, y) in enumerate([(340, 802), (428, 830), (552, 838), (646, 822), (698, 800)]):
    assert on_disc(x, y + 8, 14), i
    for j, (dx, dy) in enumerate([(-13, 9), (-6, -5), (2, -11), (11, -2), (16, 8)]):
        d.path(f"M{x + dx * 0.4:.0f},{y + 13} L{x + dx:.0f},{y + dy:.0f}",
               f"Tuft {i+1}.{j+1}", fill=NONE, stroke="#8E7C4E",
               strokeWidth=3.5, opacity=60, cap="round")

# soft shadow under the horse
d.shape("ellipse", "Horse shadow", x=330, y=760, width=420, height=28,
        fill="#151106", opacity=33, stroke=NONE)

# --- the andalusian, collected canter facing left ----------------------------------
# tail — full, long, wavy; dock tucked under the croup edge
d.path(smooth([(676, 486), (706, 522), (726, 576), (734, 636), (726, 690),
               (710, 722), (694, 716), (684, 664), (676, 604), (668, 552),
               (660, 512)]),
       "Tail", fill=HAIR_GRAD, stroke=INK, strokeWidth=5)
for i, dd in enumerate(["M690,530 C706,574 716,624 716,676",
                        "M680,546 C694,588 702,636 700,684",
                        "M700,522 C716,562 726,610 728,656"]):
    d.path(dd, f"Tail wave {i+1}", fill=NONE, stroke="#54432F",
           strokeWidth=3.5, opacity=55, cap="round")

# far legs — dimmer, roots tucked under the barrel
# far hind: engaged, hock bent, hoof lifted just off the floor mid-step
d.path(leg((652, 556), (636, 656), (586, 720), 40, 17, 11),
       "Hind leg far", fill=DIM_GRAD, stroke=INK, strokeWidth=4.5)
# far fore: planted vertical, half-hidden behind the near pair
d.path(leg((454, 556), (450, 664), (444, 762), 30, 14, 10),
       "Foreleg far", fill=DIM_GRAD, stroke=INK, strokeWidth=4.5)

# one silhouette: muzzle -> near-vertical face -> poll -> high arched crest ->
# withers -> level back -> round croup -> deep barrel -> chest -> jaw
d.path(smooth([(310, 492), (304, 458), (312, 426), (326, 402), (348, 384),
               (385, 374), (420, 398), (450, 452), (478, 478), (560, 484),
               (630, 480), (668, 468), (698, 492), (708, 540), (700, 580),
               (676, 604), (618, 616), (520, 618), (448, 606), (416, 572),
               (404, 528), (380, 496), (352, 498), (330, 506)]),
       "Horse", fill=COAT_GRAD, stroke=INK, strokeWidth=6)

# near legs — the signature: fore raised and folded, hind planted driving
d.path(leg((432, 552), (508, 546), (482, 614), 36, 16, 11),
       "Foreleg near", fill=COAT_GRAD, stroke=INK, strokeWidth=5)
d.path(leg((624, 552), (648, 672), (620, 766), 44, 18, 12),
       "Hind leg near", fill=COAT_GRAD, stroke=INK, strokeWidth=5)

# hooves — dark caps under each cannon
for i, (cx, cy) in enumerate([(482, 616), (444, 766), (620, 770), (586, 724)]):
    d.path(f"M{cx - 12},{cy - 8} C{cx - 5},{cy - 12} {cx + 7},{cy - 12} {cx + 12},{cy - 6} "
           f"C{cx + 10},{cy + 4} {cx - 9},{cy + 5} {cx - 12},{cy - 1} Z",
           f"Hoof {i+1}", fill="#17110C", stroke=INK, strokeWidth=3)

# shading kept at the silhouette edges
d.path("M466,488 C540,496 616,492 668,478 C612,496 540,500 468,494 Z",
       "Topline sheen", fill=SHEEN, opacity=40, stroke=NONE)
d.path("M470,608 C540,616 610,612 656,600 C610,616 540,620 474,614 Z",
       "Barrel shade", fill="#4E463A", opacity=25, stroke=NONE)
d.path(smooth([(420, 540), (444, 552), (450, 576), (436, 594), (414, 590),
               (406, 562)]),
       "Shoulder shade", fill="#8B8272", opacity=22, stroke=NONE)

# mane — the breed's thick wavy fall: one heavy mass riding the crest,
# scalloped hem; neck face shows below it
d.path(smooth([(346, 372), (380, 368), (412, 386), (436, 416), (450, 450),
               (448, 468), (438, 456), (428, 476), (412, 458), (400, 474),
               (386, 456), (374, 468), (360, 452), (350, 460), (342, 420),
               (340, 395)]),
       "Mane", fill=HAIR_GRAD, stroke=INK, strokeWidth=4)
# wave strokes inside the fall
for i, dd in enumerate(["M356,384 C380,398 402,424 416,456",
                        "M350,412 C372,430 390,454 400,476",
                        "M370,378 C394,392 416,416 430,446",
                        "M346,440 C358,454 366,464 372,472"]):
    d.path(dd, f"Mane wave {i+1}", fill=NONE, stroke="#5A4632",
           strokeWidth=3.5, opacity=60, cap="round")
# warm trace along the mane's crest edge
d.path("M348,374 C372,364 398,372 424,394", "Mane crest light", fill=NONE,
       stroke="#6E5C40", strokeWidth=3.5, opacity=45, cap="round")
# forelock spilling over the brow between the ears
d.path(smooth([(344, 380), (334, 392), (332, 408), (340, 420), (350, 410),
               (356, 394), (354, 380)]),
       "Forelock", fill=HAIR_GRAD, opacity=92, stroke=NONE)

# ears — small, alert, tips slightly inward
d.path("M340,378 L334,336 L360,368 Z", "Ear near", fill=COAT_GRAD,
       stroke=INK, strokeWidth=4)
d.path("M362,374 L360,340 L380,366 Z", "Ear far", fill=DIM_GRAD,
       stroke=INK, strokeWidth=3.5)
d.path("M340,368 L336,348", "Ear inner", fill=NONE, stroke="#0F0A08",
       strokeWidth=3, opacity=55, cap="round")

# the eye — dark almond, quiet
d.path("M330,432 C336,424 348,422 356,428 C354,438 342,442 332,438 "
       "C328,436 328,434 330,432 Z", "Eye",
       fill=rad((0, "#5A4028"), (0.7, "#34220F"), (1, "#160D07")),
       stroke=INK, strokeWidth=3)
d.shape("ellipse", "Pupil", x=339, y=429, width=9, height=10, fill="#0E0806", stroke=NONE)
d.shape("ellipse", "Glint", x=342, y=430, width=4.5, height=4.5, fill="#FFF4D8", opacity=90, stroke=NONE)
d.path("M328,424 C340,418 352,418 360,424", "Brow", fill=NONE,
       stroke="#6E6254", strokeWidth=4, opacity=50, cap="round")

# muzzle — grey skin shading, nostril, level mouth
d.path(smooth([(302, 456), (302, 480), (314, 496), (332, 502), (348, 494),
               (348, 474), (338, 458), (318, 452)]),
       "Muzzle shade", fill="#8A8072", opacity=45, stroke=NONE)
d.path("M306,484 C306,490 311,495 317,494 C322,492 323,486 319,482 "
       "C315,478 308,479 306,484 Z", "Nostril", fill="#1A110B",
       stroke=INK, strokeWidth=2.5)
d.path("M314,500 C324,505 336,503 344,498", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=3, opacity=75, cap="round")
d.path("M340,464 C352,470 364,468 372,460", "Cheek line", fill=NONE,
       stroke="#7A6E5E", strokeWidth=3, opacity=45, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#332C1C", strokeWidth=6)

# --- captions -------------------------------------------------------------------
d.text("ANDALUSIAN", "Name", x=500, y=934, size=56, font="Virelai Sans",
       color="#EDE4BC", justify="center")
LINE2, SZ2, TRK = "IBERIAN · SPAIN", 22, 280
r = d.text(LINE2, "Milestone", x=500, y=970, size=SZ2, font="Virelai Sans",
           color="#CCBD9C", justify="center")
d.cmd("text.setStyle", "Milestone tracking", id=r["id"], tracking=TRK)

b = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("milestone bounds", {k: round(v) for k, v in b.items()})
nearest = (min(max(PCX, b["x"]), b["x"] + b["width"]),
           min(max(PCY, b["y"]), b["y"] + b["height"]))
clear = math.hypot(nearest[0] - PCX, nearest[1] - PCY) - (PR + 3)
print("clears rim by %.1f" % clear)
assert clear > 0 and b["width"] <= 760 and b["x"] >= 10 and b["x"] + b["width"] <= 990, b

d.finish("andalusian-V1R00")
