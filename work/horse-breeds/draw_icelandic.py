#!/usr/bin/env python3
"""Icelandic — milestone card V1R00. The small gaited horse mid-tölt:
near forearm lifted to the horizontal, far hind reaching under the
body in the running-walk overstride, two legs planted. Thick double
coat = ragged ticks along the belly edge, heavy flaxen mane, full
tail. Volcanic world: moss-green dusk disc, black sand floor, a dark
ridge on the skyline, one faint steam wisp. 1000x1000. House style:
gradients + translucent shading, never flat fills. Plate = circle
center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Icelandic — Milestone Card", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#201812"                    # warm dark ink, never pure black


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


BG_GRAD = lin(0, 0, 0, 1000, (0, "#131712"), (1, "#070907"))
PLATE_GRAD = rad((0, "#9AA87E"), (0.55, "#5E6C48"), (1, "#2A301E"))
COAT_GRAD = lin(330, 380, 720, 780, (0, "#A5643A"), (0.5, "#71422A"), (1, "#3C2415"))
DIM_GRAD = lin(330, 380, 720, 780, (0, "#6E452C"), (1, "#2A1A10"))
HAIR_GRAD = lin(360, 400, 470, 560, (0, "#CFA96C"), (1, "#7C5A33"))
FLOOR_GRAD = lin(0, 730, 0, 880, (0, "#3A352C"), (0.55, "#262219"), (1, "#121008"))
SHEEN = "#E8C88E"

# --- backdrop + volcanic moss-dusk plate -------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#2C3220", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8E0BC", strokeWidth=3, opacity=38)

# volcanic ridge — one dark angular line on the skyline
d.path("M160,310 L260,268 L320,290 L420,252 L540,286 L640,262 L740,296 L840,272",
       "Volcanic ridge", fill=NONE, stroke="#2E3524", strokeWidth=6,
       opacity=38, cap="round", join="round")
# geothermal steam wisp rising off the far ridge
d.path("M668,262 C664,238 676,222 670,198 C666,182 672,168 668,152",
       "Steam wisp", fill=NONE, stroke="#D8E0C4", strokeWidth=5,
       opacity=14, cap="round")
# cold light pooling upper-left
d.shape("ellipse", "Light pool", x=240, y=140, width=410, height=220,
        fill="#E6ECD2", opacity=13, stroke=NONE)
# haze lenses
for i, (x, y, w) in enumerate([(335, 370, 90), (575, 235, 70), (725, 400, 80),
                               (260, 490, 60), (460, 195, 55)]):
    assert on_disc(x, y, 20), i
    d.shape("ellipse", f"Haze {i+1}", x=x - w / 2, y=y - w / 5, width=w, height=w * 0.4,
            fill="#DCE4C4", opacity=10, stroke=NONE)

# --- black-sand floor, closing on the disc arc -------------------------------------
fy = 782
fl, fr = rim_x(fy, -1), rim_x(fy, 1)
d.path(f"M{fl:.1f},{fy} C300,772 400,792 500,786 C600,780 700,782 {fr:.1f},{fy} "
       f"A{PR},{PR} 0 0 1 {fl:.1f},{fy} Z", "Floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{fl + 8:.0f},{fy} C300,772 400,792 500,786 C600,780 700,782 {fr - 8:.0f},{fy}",
       "Floor crest", fill=NONE, stroke="#8E9670", strokeWidth=5, opacity=38, cap="round")
# moss tussocks on the black sand
for i, (x, y, w) in enumerate([(340, 810, 40), (455, 836, 52), (575, 842, 46),
                               (660, 818, 42), (715, 796, 34)]):
    assert on_disc(x, y, 16), i
    d.shape("ellipse", f"Moss {i+1}", x=x - w / 2, y=y - w * 0.22, width=w,
            height=w * 0.44, fill="#5E7040", opacity=55, stroke=NONE)

# soft shadow under the horse
d.shape("ellipse", "Horse shadow", x=320, y=760, width=430, height=28,
        fill="#0B0A05", opacity=36, stroke=NONE)

# --- the icelandic, mid-tölt facing left -------------------------------------------
# tail — full and heavy, hanging off the dock
d.path(smooth([(682, 492), (710, 528), (726, 580), (730, 638), (720, 686),
               (706, 702), (694, 694), (688, 648), (682, 598), (674, 548),
               (666, 512)]),
       "Tail", fill=HAIR_GRAD, stroke=INK, strokeWidth=5)
for i, dd in enumerate(["M696,540 C710,580 718,622 716,664",
                        "M686,554 C698,592 704,632 702,670"]):
    d.path(dd, f"Tail wave {i+1}", fill=NONE, stroke="#8E683C",
           strokeWidth=3.5, opacity=55, cap="round")

# far legs — dimmer; far hind reaches under the body in the overstride
d.path(leg((664, 558), (638, 650), (590, 708), 42, 17, 11),
       "Hind leg far", fill=DIM_GRAD, stroke=INK, strokeWidth=4.5)
d.path(leg((458, 560), (452, 662), (448, 754), 36, 15, 10),
       "Foreleg far", fill=DIM_GRAD, stroke=INK, strokeWidth=4.5)

# one silhouette: small horse, deep chestnut body, shaggy outline
d.path(smooth([(300, 520), (296, 486), (306, 456), (322, 434), (344, 424),
               (378, 422), (410, 442), (444, 466), (478, 484), (556, 490),
               (628, 486), (670, 472), (698, 494), (708, 540), (700, 580),
               (676, 608), (620, 630), (520, 634), (446, 624), (416, 580),
               (402, 540), (374, 532), (342, 538), (322, 548)]),
       "Horse", fill=COAT_GRAD, stroke=INK, strokeWidth=6)

# double coat — ragged ticks hanging off the belly and chest edges
for i, (x, y, dx) in enumerate([(455, 628, -4), (488, 634, 2), (522, 636, -3),
                                (556, 636, 3), (590, 632, -2), (622, 628, 2),
                                (420, 600, -5), (700, 570, 3)]):
    d.path(f"M{x},{y} L{x + dx},{y + 12}", f"Coat tick {i+1}", fill=NONE,
           stroke="#3C2415", strokeWidth=4, opacity=60, cap="round")

# near legs — the tölt: forearm lifted near-horizontal, hind planted driving
d.path(leg((436, 556), (384, 568), (398, 634), 40, 16, 11),
       "Foreleg near", fill=COAT_GRAD, stroke=INK, strokeWidth=5)
d.path(leg((640, 556), (652, 664), (638, 756), 46, 18, 12),
       "Hind leg near", fill=COAT_GRAD, stroke=INK, strokeWidth=5)

# hooves — small dark caps
for i, (cx, cy) in enumerate([(398, 638), (448, 758), (638, 760), (590, 712)]):
    d.path(f"M{cx - 12},{cy - 8} C{cx - 5},{cy - 12} {cx + 7},{cy - 12} {cx + 12},{cy - 6} "
           f"C{cx + 10},{cy + 4} {cx - 9},{cy + 5} {cx - 12},{cy - 1} Z",
           f"Hoof {i+1}", fill="#150E08", stroke=INK, strokeWidth=3)

# shading kept at the silhouette edges
d.path("M462,490 C540,498 614,496 664,482 C610,500 538,502 466,494 Z",
       "Topline sheen", fill=SHEEN, opacity=34, stroke=NONE)
d.path("M466,624 C536,634 606,630 652,618 C606,634 538,638 470,630 Z",
       "Barrel shade", fill="#241408", opacity=30, stroke=NONE)
d.path(smooth([(422, 560), (446, 572), (452, 596), (438, 616), (416, 610),
               (408, 582)]),
       "Shoulder shade", fill="#E8C88E", opacity=16, stroke=NONE)

# mane — the breed's heavy fall: mass on the crest, scalloped hem,
# forelock over the brow
d.path(smooth([(340, 416), (378, 414), (410, 434), (434, 462), (440, 480),
               (426, 470), (420, 490), (404, 472), (396, 494), (380, 476),
               (372, 494), (358, 478), (350, 490), (340, 470), (336, 442)]),
       "Mane", fill=HAIR_GRAD, stroke=INK, strokeWidth=4)
for i, dd in enumerate(["M354,426 C376,440 394,460 408,480",
                        "M348,446 C366,462 380,478 390,492",
                        "M366,420 C388,432 406,450 420,470"]):
    d.path(dd, f"Mane wave {i+1}", fill=NONE, stroke="#8E683C",
           strokeWidth=3.5, opacity=55, cap="round")
d.path("M344,418 C370,410 396,418 420,438", "Mane crest light", fill=NONE,
       stroke="#E8C88E", strokeWidth=3.5, opacity=45, cap="round")
# forelock — a heavy fall over the brow
d.path(smooth([(338, 424), (328, 438), (326, 456), (334, 468), (346, 458),
               (352, 442), (350, 426)]),
       "Forelock", fill=HAIR_GRAD, opacity=92, stroke=NONE)

# ears — small, alert
d.path("M336,418 L330,384 L354,410 Z", "Ear near", fill=COAT_GRAD,
       stroke=INK, strokeWidth=4)
d.path("M356,414 L354,386 L372,408 Z", "Ear far", fill=DIM_GRAD,
       stroke=INK, strokeWidth=3.5)
d.path("M336,408 L332,392", "Ear inner", fill=NONE, stroke="#0F0A08",
       strokeWidth=3, opacity=55, cap="round")

# the eye — dark almond under the forelock hem
d.path("M320,472 C326,464 338,462 346,468 C344,478 332,482 322,478 "
       "C318,476 318,474 320,472 Z", "Eye",
       fill=rad((0, "#4A2E18"), (0.7, "#2A1A0C"), (1, "#120A05")),
       stroke=INK, strokeWidth=3)
d.shape("ellipse", "Pupil", x=329, y=469, width=9, height=10, fill="#0E0806", stroke=NONE)
d.shape("ellipse", "Glint", x=332, y=470, width=4.5, height=4.5, fill="#F6EED6", opacity=90, stroke=NONE)
d.path("M318,464 C330,458 342,458 350,464", "Brow", fill=NONE,
       stroke="#3A2414", strokeWidth=4, opacity=50, cap="round")

# muzzle — darker shading, nostril, level mouth
d.path(smooth([(294, 496), (294, 520), (306, 536), (324, 542), (340, 534),
               (340, 512), (330, 494), (312, 488)]),
       "Muzzle shade", fill="#5E3A22", opacity=45, stroke=NONE)
d.path("M298,520 C298,526 303,531 309,530 C314,528 315,522 311,518 "
       "C307,514 300,515 298,520 Z", "Nostril", fill="#120A06",
       stroke=INK, strokeWidth=2.5)
d.path("M306,536 C316,541 328,539 336,534", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=3, opacity=75, cap="round")
d.path("M334,500 C346,506 358,504 366,496", "Cheek line", fill=NONE,
       stroke="#3A2414", strokeWidth=3, opacity=45, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#262C1A", strokeWidth=6)

# --- captions -------------------------------------------------------------------
d.text("ICELANDIC", "Name", x=500, y=934, size=56, font="Virelai Sans",
       color="#E4E8CC", justify="center")
LINE2, SZ2, TRK = "GAITED · ICELAND", 22, 280
r = d.text(LINE2, "Milestone", x=500, y=970, size=SZ2, font="Virelai Sans",
           color="#BFC8A6", justify="center")
d.cmd("text.setStyle", "Milestone tracking", id=r["id"], tracking=TRK)

b = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("milestone bounds", {k: round(v) for k, v in b.items()})
nearest = (min(max(PCX, b["x"]), b["x"] + b["width"]),
           min(max(PCY, b["y"]), b["y"] + b["height"]))
clear = math.hypot(nearest[0] - PCX, nearest[1] - PCY) - (PR + 3)
print("clears rim by %.1f" % clear)
assert clear > 0 and b["width"] <= 760 and b["x"] >= 10 and b["x"] + b["width"] <= 990, b

d.finish("icelandic-V1R00")
