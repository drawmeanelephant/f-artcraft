#!/usr/bin/env python3
"""Percheron — milestone card V1R00. The dark draft horse at a working
walk: deep barrel, thick column legs CLEAN of feather (the tell versus
the clydesdale), alert little ears, far hind reaching under the body
mid-stride. Muscle shown as edge-hugging translucent shades. Perche
farmland: furrow rows on the floor, a hedgerow line on the skyline.
1000x1000. House style: gradients + translucent shading, never flat
fills. Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Percheron — Milestone Card", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#211A14"                    # warm dark ink, never pure black


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


BG_GRAD = lin(0, 0, 0, 1000, (0, "#161310"), (1, "#0A0806"))
PLATE_GRAD = rad((0, "#B8AC84"), (0.55, "#7E7452"), (1, "#3E3520"))
COAT_GRAD = lin(330, 360, 720, 800, (0, "#4A4642"), (0.5, "#2E2B28"), (1, "#171512"))
DIM_GRAD = lin(330, 360, 720, 800, (0, "#33312E"), (1, "#121110"))
HAIR_GRAD = lin(360, 380, 480, 560, (0, "#2A2724"), (1, "#0F0D0B"))
FLOOR_GRAD = lin(0, 730, 0, 880, (0, "#6E5F42"), (0.55, "#4A3F28"), (1, "#241E12"))
SHEEN = "#8E8878"

# --- backdrop + Perche dusk plate --------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#3A3421", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E4DCB8", strokeWidth=3, opacity=38)

# hedgerow — a broken treeline low on the skyline
d.path("M170,318 C240,308 290,316 350,306 C420,296 470,306 540,298 C610,290 660,300 720,292 C770,286 810,292 838,286",
       "Hedgerow", fill=NONE, stroke="#4E452E", strokeWidth=5,
       opacity=30, cap="round")
for i, (x, y, w) in enumerate([(235, 300, 26), (405, 296, 30), (590, 290, 34),
                               (755, 282, 28)]):
    d.shape("ellipse", f"Tree {i+1}", x=x - w / 2, y=y - w * 0.7, width=w,
            height=w * 1.4, fill="#4E452E", opacity=22, stroke=NONE)
# late light pooling upper-left
d.shape("ellipse", "Light pool", x=245, y=140, width=400, height=220,
        fill="#EAE0BA", opacity=13, stroke=NONE)
# haze lenses
for i, (x, y, w) in enumerate([(335, 375, 90), (580, 250, 70), (725, 400, 80),
                               (260, 495, 60), (455, 205, 55)]):
    assert on_disc(x, y, 20), i
    d.shape("ellipse", f"Haze {i+1}", x=x - w / 2, y=y - w / 5, width=w, height=w * 0.4,
            fill="#E4D8AE", opacity=10, stroke=NONE)

# --- furrowed floor, closing on the disc arc ---------------------------------------
fy = 782
fl, fr = rim_x(fy, -1), rim_x(fy, 1)
d.path(f"M{fl:.1f},{fy} C300,772 400,792 500,786 C600,780 700,782 {fr:.1f},{fy} "
       f"A{PR},{PR} 0 0 1 {fl:.1f},{fy} Z", "Floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{fl + 8:.0f},{fy} C300,772 400,792 500,786 C600,780 700,782 {fr - 8:.0f},{fy}",
       "Floor crest", fill=NONE, stroke="#A8966A", strokeWidth=5, opacity=40, cap="round")
# furrow rows converging gently
for i, (yy, bend) in enumerate([(806, 10), (824, 6), (842, 2)]):
    d.path(f"M{rim_x(yy, -1) + 16:.0f},{yy} C380,{yy - bend} 620,{yy - bend} {rim_x(yy, 1) - 16:.0f},{yy}",
           f"Furrow {i+1}", fill=NONE, stroke="#3E341F", strokeWidth=4,
           opacity=42, cap="round")

# soft shadow under the horse
d.shape("ellipse", "Horse shadow", x=320, y=762, width=440, height=28,
        fill="#141006", opacity=33, stroke=NONE)

# --- the percheron, working walk facing left ---------------------------------------
# tail — natural, medium, hanging off the dock
d.path(smooth([(684, 492), (712, 528), (728, 580), (732, 636), (722, 682),
               (708, 698), (696, 690), (690, 644), (684, 596), (676, 546),
               (668, 512)]),
       "Tail", fill=HAIR_GRAD, stroke=INK, strokeWidth=5)
for i, dd in enumerate(["M698,540 C712,580 720,622 718,662",
                        "M688,554 C700,592 706,632 704,668"]):
    d.path(dd, f"Tail wave {i+1}", fill=NONE, stroke="#4A4238",
           strokeWidth=3.5, opacity=55, cap="round")

# far legs — dimmer; far hind reaches under the body mid-stride
d.path(leg((666, 560), (640, 652), (592, 712), 44, 18, 12),
       "Hind leg far", fill=DIM_GRAD, stroke=INK, strokeWidth=4.5)
d.path(leg((458, 560), (462, 664), (468, 754), 38, 16, 11),
       "Foreleg far", fill=DIM_GRAD, stroke=INK, strokeWidth=4.5)

# one silhouette: low working head -> face -> poll -> thick crest ->
# withers -> level back -> round croup -> deep barrel -> chest -> jaw
d.path(smooth([(300, 524), (296, 490), (306, 458), (324, 436), (348, 428),
               (380, 428), (412, 448), (448, 472), (480, 486), (560, 490),
               (632, 486), (674, 472), (702, 494), (712, 542), (702, 584),
               (678, 612), (622, 636), (520, 640), (448, 630), (418, 588),
               (404, 548), (372, 542), (340, 544), (318, 552)]),
       "Horse", fill=COAT_GRAD, stroke=INK, strokeWidth=6)

# near legs — the working walk: fore reaching forward, hind planted driving
d.path(leg((434, 560), (400, 650), (376, 730), 44, 18, 12),
       "Foreleg near", fill=COAT_GRAD, stroke=INK, strokeWidth=5)
d.path(leg((640, 556), (654, 666), (640, 758), 48, 19, 13),
       "Hind leg near", fill=COAT_GRAD, stroke=INK, strokeWidth=5)

# hooves — big dark draft caps
for i, (cx, cy, w) in enumerate([(376, 734, 15), (468, 758, 14), (640, 762, 16),
                                 (592, 716, 14)]):
    d.path(f"M{cx - w},{cy - 9} C{cx - 6},{cy - 14} {cx + 8},{cy - 14} {cx + w},{cy - 7} "
           f"C{cx + w - 2},{cy + 5} {cx - w + 3},{cy + 6} {cx - w},{cy - 1} Z",
           f"Hoof {i+1}", fill="#14100C", stroke=INK, strokeWidth=3)

# muscle and sheen kept at the silhouette edges
d.path("M466,488 C540,496 616,494 668,480 C612,498 540,502 468,494 Z",
       "Topline sheen", fill=SHEEN, opacity=34, stroke=NONE)
d.path("M470,628 C540,638 610,634 656,620 C610,638 540,642 474,634 Z",
       "Barrel shade", fill="#0F0D0B", opacity=30, stroke=NONE)
d.path(smooth([(424, 566), (450, 578), (456, 602), (440, 622), (418, 616),
               (410, 588)]),
       "Shoulder muscle", fill=SHEEN, opacity=16, stroke=NONE)
d.path(smooth([(620, 560), (652, 572), (660, 598), (644, 620), (620, 612),
               (610, 584)]),
       "Thigh muscle", fill=SHEEN, opacity=14, stroke=NONE)
d.path("M430,575 C424,608 418,640 410,672", "Forearm line", fill=NONE,
       stroke="#0F0D0B", strokeWidth=3, opacity=40, cap="round")

# mane — short and tidy: a neat band hugging the crest, scalloped hem
d.path(smooth([(344, 418), (378, 420), (408, 438), (436, 462), (442, 476),
               (430, 468), (424, 482), (410, 468), (404, 480), (390, 462),
               (382, 472), (370, 456), (360, 464), (352, 446), (346, 432)]),
       "Mane", fill=HAIR_GRAD, stroke=INK, strokeWidth=4)
for i, dd in enumerate(["M358,428 C378,440 396,458 410,476",
                        "M352,442 C368,454 382,466 392,478"]):
    d.path(dd, f"Mane strand {i+1}", fill=NONE, stroke="#4A4238",
           strokeWidth=3.5, opacity=55, cap="round")
d.path("M346,422 C372,414 398,424 422,444", "Mane crest light", fill=NONE,
       stroke="#6A5E4A", strokeWidth=3.5, opacity=40, cap="round")

# ears — little and alert, the draft tell
d.path("M340,424 L336,392 L356,416 Z", "Ear near", fill=COAT_GRAD,
       stroke=INK, strokeWidth=4)
d.path("M360,420 L360,392 L376,412 Z", "Ear far", fill=DIM_GRAD,
       stroke=INK, strokeWidth=3.5)
d.path("M340,414 L338,400", "Ear inner", fill=NONE, stroke="#0F0A08",
       strokeWidth=3, opacity=55, cap="round")

# the eye — dark, quiet, a touch of kindness
d.path("M322,472 C328,464 340,462 348,468 C346,478 334,482 324,478 "
       "C320,476 320,474 322,472 Z", "Eye",
       fill=rad((0, "#4A3520"), (0.7, "#2C1E10"), (1, "#140D08")),
       stroke=INK, strokeWidth=3)
d.shape("ellipse", "Pupil", x=331, y=469, width=9, height=10, fill="#0E0806", stroke=NONE)
d.shape("ellipse", "Glint", x=334, y=470, width=4.5, height=4.5, fill="#F2EAD2", opacity=90, stroke=NONE)
d.path("M320,464 C332,458 344,458 352,464", "Brow", fill=NONE,
       stroke="#0F0D0B", strokeWidth=4, opacity=50, cap="round")

# muzzle — gentle shading, wide draft nostril, level mouth
d.path(smooth([(296, 500), (296, 522), (308, 538), (326, 544), (342, 536),
               (342, 514), (332, 496), (314, 490)]),
       "Muzzle shade", fill="#5E5850", opacity=40, stroke=NONE)
d.path("M300,522 C300,528 305,533 311,532 C316,530 317,524 313,520 "
       "C309,516 302,517 300,522 Z", "Nostril", fill="#0E0A07",
       stroke=INK, strokeWidth=2.5)
d.path("M308,538 C318,543 330,541 338,536", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=3, opacity=75, cap="round")
d.path("M336,502 C348,508 360,506 368,498", "Cheek line", fill=NONE,
       stroke="#0F0D0B", strokeWidth=3, opacity=45, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#332C1C", strokeWidth=6)

# --- captions -------------------------------------------------------------------
d.text("PERCHERON", "Name", x=500, y=934, size=56, font="Virelai Sans",
       color="#E8E0BA", justify="center")
LINE2, SZ2, TRK = "DRAFT · FRANCE", 22, 280
r = d.text(LINE2, "Milestone", x=500, y=970, size=SZ2, font="Virelai Sans",
           color="#C4B891", justify="center")
d.cmd("text.setStyle", "Milestone tracking", id=r["id"], tracking=TRK)

b = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("milestone bounds", {k: round(v) for k, v in b.items()})
nearest = (min(max(PCX, b["x"]), b["x"] + b["width"]),
           min(max(PCY, b["y"]), b["y"] + b["height"]))
clear = math.hypot(nearest[0] - PCX, nearest[1] - PCY) - (PR + 3)
print("clears rim by %.1f" % clear)
assert clear > 0 and b["width"] <= 760 and b["x"] >= 10 and b["x"] + b["width"] <= 990, b

d.finish("percheron-V1R00")
