#!/usr/bin/env python3
"""Belgian — milestone card V1R00. The sorrel gentle giant standing
calm and square: massive deep chest, big plain head with small ears,
clean legs like columns, flaxen mane and tail. Warm stable light
glowing on the coat, a straw-scattered floor closing on the disc's
own arc. 1000x1000. House style: gradients + translucent shading,
never flat fills. Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Belgian — Milestone Card", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#2E2014"                    # warm dark ink, never pure black


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
    """Limb silhouette — two segments, one joint, columnar not tapered."""

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


BG_GRAD = lin(0, 0, 0, 1000, (0, "#1C1610"), (1, "#0A0705"))
PLATE_GRAD = rad((0, "#C4A870"), (0.55, "#8F744C"), (1, "#4E3E2A"))
COAT_GRAD = lin(330, 400, 720, 760, (0, "#C08348"), (0.5, "#8F5C2E"), (1, "#59351A"))
DIM_GRAD = lin(330, 400, 720, 760, (0, "#96693A"), (1, "#432712"))
FLAX_GRAD = lin(340, 380, 780, 720, (0, "#E4CE9E"), (0.6, "#BE9F68"), (1, "#8A6C3C"))
FLOOR_GRAD = lin(0, 720, 0, 880, (0, "#6E5734"), (0.55, "#4E3E24"), (1, "#2A2012"))
GLOW = "#F2DCAC"

# --- backdrop + stable-amber plate -------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#3E3220", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#EADFB8", strokeWidth=3, opacity=38)

# stable light pooling warm from upper-left
d.shape("ellipse", "Light pool", x=240, y=140, width=420, height=240,
        fill=GLOW, opacity=16, stroke=NONE)
# soft shafts of light angling down
for i, (x, y, w) in enumerate([(330, 300, 110), (600, 230, 80), (730, 360, 90)]):
    assert on_disc(x, y, 20), i
    d.shape("ellipse", f"Shaft {i+1}", x=x - w / 2, y=y - w / 6, width=w, height=w * 0.33,
            fill="#F0DCA6", opacity=11, stroke=NONE)

# --- stable floor, closing on the disc arc ------------------------------------------
fy = 782
fl, fr = rim_x(fy, -1), rim_x(fy, 1)
d.path(f"M{fl:.1f},{fy} C300,772 400,790 500,784 C600,778 700,782 {fr:.1f},{fy} "
       f"A{PR},{PR} 0 0 1 {fl:.1f},{fy} Z", "Floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{fl + 8:.0f},{fy} C300,772 400,790 500,784 C600,778 700,782 {fr - 8:.0f},{fy}",
       "Floor crest", fill=NONE, stroke="#A68C54", strokeWidth=5, opacity=42, cap="round")
# scattered straw on the floor
for i, (x, y, a) in enumerate([(340, 806, -8), (410, 830, 12), (480, 838, -4),
                               (560, 836, 8), (640, 824, -14), (700, 800, 6),
                               (380, 812, 18), (600, 812, -10)]):
    assert on_disc(x, y, 14), i
    dx, dy = 16 * math.cos(math.radians(a)), 16 * math.sin(math.radians(a))
    d.path(f"M{x - dx:.0f},{y - dy:.0f} L{x + dx:.0f},{y + dy:.0f}",
           f"Straw {i+1}", fill=NONE, stroke="#C2A458",
           strokeWidth=3.5, opacity=55, cap="round")

# broad shadow under the standing giant
d.shape("ellipse", "Horse shadow", x=300, y=752, width=440, height=30,
        fill="#140D05", opacity=34, stroke=NONE)

# --- the belgian, standing square and calm, facing left ------------------------------
# tail — flaxen, full but tidy, hanging nearly straight with a low sway
d.path(smooth([(668, 480), (706, 512), (734, 560), (750, 616), (752, 668),
               (740, 700), (722, 706), (710, 676), (700, 622), (684, 568),
               (662, 522)]),
       "Tail", fill=FLAX_GRAD, stroke=INK, strokeWidth=5)
for i, dd in enumerate(["M694,530 C712,572 724,620 732,662",
                        "M684,556 C698,594 710,634 716,672"]):
    d.path(dd, f"Tail strand {i+1}", fill=NONE, stroke="#6E5328",
           strokeWidth=3.5, opacity=50, cap="round")

# far legs — dimmer, half a step back, clean columns
d.path(leg((470, 590), (466, 664), (462, 736), 44, 26, 17),
       "Foreleg far", fill=DIM_GRAD, stroke=INK, strokeWidth=4.5)
d.path(leg((648, 584), (654, 656), (660, 730), 50, 28, 18),
       "Hind leg far", fill=DIM_GRAD, stroke=INK, strokeWidth=4.5)

# body — the mass is the breed: deep broad chest, level back, huge round rump
d.path(smooth([(396, 544), (414, 498), (452, 470), (520, 458), (596, 456),
               (650, 458), (684, 476), (704, 516), (708, 560), (690, 610),
               (646, 638), (576, 654), (500, 656), (442, 646), (410, 612),
               (398, 572)]),
       "Body", fill=COAT_GRAD, stroke=INK, strokeWidth=6)
# warm glow riding the topline
d.path("M428,490 C500,466 590,458 666,464 C590,474 505,482 430,498 Z",
       "Topline glow", fill=GLOW, opacity=32, stroke=NONE)
# broad glow on the chest — stable light on red sorrel
d.path(smooth([(420, 548), (444, 566), (450, 600), (434, 620), (412, 610),
               (404, 574)]),
       "Chest glow", fill=GLOW, opacity=14, stroke=NONE)
# the underline: deep belly shadow
d.path("M444,636 C520,652 600,648 664,622 C636,652 540,662 460,646 Z",
       "Belly shade", fill="#3A2210", opacity=40, stroke=NONE)

# near legs — clean columns, no feather, planted square
d.path(leg((436, 600), (430, 668), (424, 738), 48, 28, 18),
       "Foreleg near", fill=COAT_GRAD, stroke=INK, strokeWidth=5)
d.path(leg((616, 588), (624, 656), (632, 732), 54, 30, 19),
       "Hind leg near", fill=COAT_GRAD, stroke=INK, strokeWidth=5)

# neck — massive and short, the draft crest without excess height
d.path(smooth([(312, 488), (338, 450), (352, 420), (378, 404), (410, 414),
               (440, 446), (460, 486), (466, 524), (452, 556), (410, 552),
               (364, 528), (332, 508)]),
       "Neck", fill=COAT_GRAD, stroke=INK, strokeWidth=5)

# head — big and plain, broad forehead, small ears, quiet muzzle
d.path(smooth([(358, 412), (332, 424), (304, 444), (282, 466), (268, 484),
               (262, 500), (268, 514), (286, 522), (310, 522), (336, 510),
               (352, 486)]),
       "Head", fill=COAT_GRAD, stroke=INK, strokeWidth=5)
# muzzle — broad and soft
d.path(smooth([(262, 488), (260, 504), (268, 518), (288, 522), (304, 516),
               (306, 500), (294, 486), (276, 484)]),
       "Muzzle", fill="#6E4423", opacity=60, stroke=NONE)
# nostril — large, calm
d.path("M272,498 C270,506 274,512 282,512 C288,510 290,502 286,497 "
       "C281,494 274,494 272,498 Z", "Nostril", fill="#160D07",
       stroke=INK, strokeWidth=2.5)
# mouth — level, peaceful
d.path("M282,516 C292,518 302,516 312,512", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=3, cap="round")

# ears — SMALL on the big head; the proportion is the breed
d.path("M350,414 L344,392 L360,408 Z", "Ear near", fill=COAT_GRAD,
       stroke=INK, strokeWidth=3.5)
d.path("M362,416 L360,396 L374,410 Z", "Ear far", fill=DIM_GRAD,
       stroke=INK, strokeWidth=3)

# the eye — big, dark, calm; the gentle giant's kindness
d.path("M312,458 C318,450 330,448 338,454 C336,464 324,468 314,464 "
       "C310,462 310,460 312,458 Z", "Eye",
       fill=rad((0, "#5E3A1C"), (0.7, "#382212"), (1, "#1A0F08")),
       stroke=INK, strokeWidth=3)
d.shape("ellipse", "Pupil", x=321, y=455, width=10, height=11, fill="#0C0705", stroke=NONE)
d.shape("ellipse", "Glint", x=324, y=456, width=4.5, height=4.5, fill="#FFF4D8", opacity=90, stroke=NONE)

# mane — flaxen, a moderate band riding the crest; the draft mane is
# tidy, not a cascade — hem stays well inside the throat silhouette
d.path(smooth([(348, 402), (384, 396), (420, 410), (448, 434), (464, 466),
               (470, 498), (458, 518), (434, 514), (406, 502), (380, 486),
               (362, 462), (352, 436), (346, 414)]),
       "Mane", fill=FLAX_GRAD, stroke=INK, strokeWidth=4)
for i, dd in enumerate(["M364,412 C394,414 424,428 450,452",
                        "M368,436 C396,440 424,456 448,480",
                        "M372,462 C396,468 420,484 440,506"]):
    d.path(dd, f"Mane strand {i+1}", fill=NONE, stroke="#6E5328",
           strokeWidth=3.5, opacity=55, cap="round")
# forelock — a modest pale fall between the ears
d.path(smooth([(346, 410), (336, 420), (332, 436), (338, 450), (346, 442),
               (352, 428), (356, 414)]),
       "Forelock", fill=FLAX_GRAD, stroke=INK, strokeWidth=3)

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#382C1C", strokeWidth=6)

# --- captions -------------------------------------------------------------------
d.text("BELGIAN", "Name", x=500, y=934, size=56, font="Virelai Sans",
       color="#F0E6C8", justify="center")
LINE2, SZ2, TRK = "DRAFT · BELGIUM", 22, 280
r = d.text(LINE2, "Milestone", x=500, y=970, size=SZ2, font="Virelai Sans",
           color="#CBBD94", justify="center")
d.cmd("text.setStyle", "Milestone tracking", id=r["id"], tracking=TRK)

b = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("milestone bounds", {k: round(v) for k, v in b.items()})
nearest = (min(max(PCX, b["x"]), b["x"] + b["width"]),
           min(max(PCY, b["y"]), b["y"] + b["height"]))
clear = math.hypot(nearest[0] - PCX, nearest[1] - PCY) - (PR + 3)
print("clears rim by %.1f" % clear)
assert clear > 0 and b["width"] <= 760 and b["x"] >= 10 and b["x"] + b["width"] <= 990, b

d.finish("belgian-V1R00")
