#!/usr/bin/env python3
"""Akhal-Teke — milestone card V1R00. The metallic-sheen breed: slim
buckskin body with a gilded coat, long thin neck set high, small
refined head, sparse dark mane — the greyhound of horses. Buckskin
points: dark mane/tail, dark cannons, dorsal stripe on the topline.
Karakum world: desert-rose dusk disc, low sun, dune contours, pale
sand floor. 1000x1000. House style: gradients + translucent shading,
never flat fills. Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Akhal-Teke — Milestone Card", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#26180F"                    # warm dark ink, never pure black


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


BG_GRAD = lin(0, 0, 0, 1000, (0, "#1D1410"), (1, "#0C0805"))
PLATE_GRAD = rad((0, "#DCA98C"), (0.55, "#A4725C"), (1, "#55392C"))
COAT_GRAD = lin(330, 360, 720, 790, (0, "#D8A85E"), (0.5, "#A87B3E"), (1, "#5E3F1E"))
DIM_GRAD = lin(330, 360, 720, 790, (0, "#9A7340"), (1, "#432C16"))
HAIR_GRAD = lin(350, 370, 470, 560, (0, "#3A2A1A"), (1, "#150D07"))
FLOOR_GRAD = lin(0, 730, 0, 880, (0, "#A08862"), (0.55, "#6E5A3E"), (1, "#36281A"))
SHEEN = "#FFE4AE"

# --- backdrop + Karakum rose-dusk plate --------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#4A3326", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F2D8C0", strokeWidth=3, opacity=38)

# low desert sun on the skyline
d.shape("ellipse", "Low sun", x=640, y=255, width=64, height=64,
        fill="#F2D8B8", opacity=28, stroke=NONE)
# dune contours — long lazy curves on the upper plate
d.path("M150,340 C280,314 420,330 560,316 C680,304 780,318 850,310",
       "Dune 1", fill=NONE, stroke="#8E5F4A", strokeWidth=4.5,
       opacity=30, cap="round")
d.path("M200,380 C320,362 460,374 590,362 C700,352 790,364 830,358",
       "Dune 2", fill=NONE, stroke="#9A6A52", strokeWidth=4,
       opacity=24, cap="round")
# rose light pooling upper-left
d.shape("ellipse", "Light pool", x=235, y=140, width=420, height=220,
        fill="#F4DEC4", opacity=15, stroke=NONE)
# haze lenses
for i, (x, y, w) in enumerate([(340, 390, 90), (580, 245, 70), (730, 410, 80),
                               (260, 500, 60), (460, 205, 55)]):
    assert on_disc(x, y, 20), i
    d.shape("ellipse", f"Haze {i+1}", x=x - w / 2, y=y - w / 5, width=w, height=w * 0.4,
            fill="#F0D8BE", opacity=10, stroke=NONE)

# --- pale sand floor, closing on the disc arc --------------------------------------
fy = 782
fl, fr = rim_x(fy, -1), rim_x(fy, 1)
d.path(f"M{fl:.1f},{fy} C300,772 400,792 500,786 C600,780 700,782 {fr:.1f},{fy} "
       f"A{PR},{PR} 0 0 1 {fl:.1f},{fy} Z", "Floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{fl + 8:.0f},{fy} C300,772 400,792 500,786 C600,780 700,782 {fr - 8:.0f},{fy}",
       "Floor crest", fill=NONE, stroke="#D0B88A", strokeWidth=5, opacity=42, cap="round")
# wind-rippled sand line
d.path("M330,824 C430,812 560,810 680,818", "Sand line", fill=NONE,
       stroke="#54432A", strokeWidth=4, opacity=45, cap="round")

# soft shadow under the horse
d.shape("ellipse", "Horse shadow", x=310, y=758, width=430, height=26,
        fill="#1A1008", opacity=34, stroke=NONE)

# --- the akhal-teke, standing alert facing left ------------------------------------
# tail — sparse, fine, hanging off the dock
d.path(smooth([(674, 482), (700, 514), (714, 564), (718, 618), (708, 660),
               (696, 668), (688, 656), (684, 610), (678, 560), (668, 514),
               (660, 490)]),
       "Tail", fill=HAIR_GRAD, stroke=INK, strokeWidth=4.5)
for i, dd in enumerate(["M686,522 C698,560 706,600 706,638",
                        "M676,534 C686,570 692,606 692,644"]):
    d.path(dd, f"Tail strand {i+1}", fill=NONE, stroke="#5E4028",
           strokeWidth=3.5, opacity=55, cap="round")

# far legs — dimmer, slim columns
d.path(leg((654, 556), (666, 658), (658, 748), 32, 13, 9),
       "Hind leg far", fill=DIM_GRAD, stroke=INK, strokeWidth=4.5)
d.path(leg((444, 562), (442, 660), (440, 748), 30, 13, 9),
       "Foreleg far", fill=DIM_GRAD, stroke=INK, strokeWidth=4.5)

# one silhouette: small refined head -> long thin neck -> slim body,
# abdomen tucked up toward the flank
d.path(smooth([(302, 470), (296, 436), (304, 406), (318, 384), (338, 370),
               (370, 366), (400, 388), (428, 428), (470, 466), (540, 476),
               (612, 474), (656, 460), (684, 480), (696, 522), (690, 560),
               (668, 588), (614, 598), (520, 606), (452, 592), (424, 560),
               (408, 518), (386, 492), (356, 492), (334, 498)]),
       "Horse", fill=COAT_GRAD, stroke=INK, strokeWidth=6)

# near legs — long and thin, one fore resting slightly forward
d.path(leg((418, 558), (410, 656), (400, 744), 32, 14, 9),
       "Foreleg near", fill=COAT_GRAD, stroke=INK, strokeWidth=5)
d.path(leg((628, 558), (638, 662), (626, 748), 36, 15, 10),
       "Hind leg near", fill=COAT_GRAD, stroke=INK, strokeWidth=5)

# buckskin points — dark cannons as narrow fills inside the leg edges
d.path(smooth([(406, 640), (412, 672), (408, 710), (402, 738), (396, 738),
               (398, 706), (400, 670), (398, 644)], k=0.8),
       "Cannon point F", fill="#2A1C10", opacity=55, stroke=NONE)
d.path(smooth([(632, 648), (638, 682), (634, 718), (628, 744), (622, 742),
               (624, 712), (626, 678), (624, 652)], k=0.8),
       "Cannon point H", fill="#2A1C10", opacity=50, stroke=NONE)

# hooves — small dark caps
for i, (cx, cy) in enumerate([(400, 748), (440, 752), (626, 752), (658, 752)]):
    d.path(f"M{cx - 11},{cy - 8} C{cx - 5},{cy - 12} {cx + 6},{cy - 12} {cx + 11},{cy - 6} "
           f"C{cx + 9},{cy + 4} {cx - 8},{cy + 5} {cx - 11},{cy - 1} Z",
           f"Hoof {i+1}", fill="#170F08", stroke=INK, strokeWidth=3)

# the metallic read — dorsal stripe on the topline edge, gilded sheen under it
d.path("M442,448 C510,474 580,478 648,462", "Dorsal stripe", fill=NONE,
       stroke="#3A2814", strokeWidth=4, opacity=55, cap="round")
d.path("M446,452 C514,478 584,482 650,468 C584,488 514,482 448,458 Z",
       "Gilded band", fill=SHEEN, opacity=42, stroke=NONE)
d.path("M452,598 C520,610 586,606 640,592 C586,612 520,614 456,604 Z",
       "Barrel shade", fill="#3A240F", opacity=28, stroke=NONE)
d.path("M344,378 C372,390 396,414 414,444", "Crest sheen", fill=NONE,
       stroke=SHEEN, strokeWidth=4, opacity=60, cap="round")
d.path("M420,520 C416,540 412,556 406,572", "Shoulder gleam", fill=NONE,
       stroke=SHEEN, strokeWidth=4, opacity=35, cap="round")
# cheek gleam — a thin highlight along the jaw
d.path("M330,470 C350,478 372,476 388,466", "Cheek gleam", fill=NONE,
       stroke=SHEEN, strokeWidth=3.5, opacity=40, cap="round")

# mane — sparse: a thin dark band on the crest, a few strand strokes
d.path(smooth([(342, 364), (374, 362), (400, 382), (422, 414), (434, 444),
               (428, 456), (412, 440), (392, 414), (368, 390), (348, 378)]),
       "Mane", fill=HAIR_GRAD, stroke=INK, strokeWidth=4)
for i, dd in enumerate(["M356,374 C376,388 394,410 406,432",
                        "M350,386 C366,400 380,418 390,436"]):
    d.path(dd, f"Mane strand {i+1}", fill=NONE, stroke="#5E4028",
           strokeWidth=3.5, opacity=55, cap="round")
d.path("M344,366 C368,356 392,364 414,384", "Mane crest light", fill=NONE,
       stroke="#8E6A44", strokeWidth=3.5, opacity=45, cap="round")
# forelock — a small wisp only
d.path(smooth([(342, 374), (334, 386), (333, 398), (341, 406), (349, 396),
               (352, 384), (350, 374)]),
       "Forelock", fill=HAIR_GRAD, opacity=90, stroke=NONE)

# ears — fine, alert, pricked
d.path("M336,376 L330,336 L356,364 Z", "Ear near", fill=COAT_GRAD,
       stroke=INK, strokeWidth=4)
d.path("M358,372 L356,338 L374,362 Z", "Ear far", fill=DIM_GRAD,
       stroke=INK, strokeWidth=3.5)
d.path("M336,366 L332,348", "Ear inner", fill=NONE, stroke="#0F0A08",
       strokeWidth=3, opacity=55, cap="round")

# the eye — large, dark, hooded
d.path("M326,424 C332,416 344,414 352,420 C350,430 338,434 328,430 "
       "C324,428 324,426 326,424 Z", "Eye",
       fill=rad((0, "#5A3418"), (0.7, "#321E0C"), (1, "#140B05")),
       stroke=INK, strokeWidth=3)
d.shape("ellipse", "Pupil", x=335, y=421, width=9, height=10, fill="#0E0806", stroke=NONE)
d.shape("ellipse", "Glint", x=338, y=422, width=4.5, height=4.5, fill="#FFF0D0", opacity=95, stroke=NONE)
d.path("M324,416 C336,410 348,410 356,416", "Brow", fill=NONE,
       stroke="#6E4E28", strokeWidth=4, opacity=50, cap="round")

# muzzle — fine shading, small nostril, level mouth
d.path(smooth([(296, 442), (296, 466), (308, 482), (326, 488), (342, 480),
               (342, 460), (332, 442), (312, 436)]),
       "Muzzle shade", fill="#8E6238", opacity=45, stroke=NONE)
d.path("M302,468 C302,474 307,479 313,478 C318,476 319,470 315,466 "
       "C311,462 304,463 302,468 Z", "Nostril", fill="#120A05",
       stroke=INK, strokeWidth=2.5)
d.path("M310,486 C320,491 332,489 340,484", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=3, opacity=75, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#422E1D", strokeWidth=6)

# --- captions -------------------------------------------------------------------
d.text("AKHAL-TEKE", "Name", x=500, y=934, size=56, font="Virelai Sans",
       color="#F2DCBA", justify="center")
LINE2, SZ2, TRK = "METALLIC · TURKMENISTAN", 22, 280
r = d.text(LINE2, "Milestone", x=500, y=970, size=SZ2, font="Virelai Sans",
           color="#D4B99C", justify="center")
d.cmd("text.setStyle", "Milestone tracking", id=r["id"], tracking=TRK)

b = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("milestone bounds", {k: round(v) for k, v in b.items()})
nearest = (min(max(PCX, b["x"]), b["x"] + b["width"]),
           min(max(PCY, b["y"]), b["y"] + b["height"]))
clear = math.hypot(nearest[0] - PCX, nearest[1] - PCY) - (PR + 3)
print("clears rim by %.1f" % clear)
assert clear > 0 and b["width"] <= 760 and b["x"] >= 10 and b["x"] + b["width"] <= 990, b

d.finish("akhal-teke-V1R00")
