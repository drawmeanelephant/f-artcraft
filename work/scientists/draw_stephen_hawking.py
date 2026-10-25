#!/usr/bin/env python3
"""Stephen Hawking — milestone card V1R00. The silhouette everyone knows:
a seated figure in wheelchair profile facing left against a starfield
plate, a faint event-horizon ring glowing upper-right. Cool cyan rim
light on the head, shoulder and wheel; dignified and cosmic, not
mournful. Wheels stand on a low chord closed on the disc's own arc.
1000x1000. House style: gradients + translucent shading, never flat
fills. Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Stephen Hawking — Milestone Card", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#181209"                    # warm dark ink, never pure black
SS3 = "Source Sans 3"              # Virelai Sans has no digit glyphs


def _stops(*pairs):
    out = []
    for p in pairs:
        s = {"offset": p[0], "color": p[1]}
        if len(p) > 2:
            s["opacity"] = p[2]
        out.append(s)
    return out


def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": _stops(*stops)}}


def rad(*stops):
    return {"gradient": {"kind": "radial", "stops": _stops(*stops)}}


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


def ellipse_pts(cx, cy, rx, ry, deg, n=20):
    t = math.radians(deg)
    c, s = math.cos(t), math.sin(t)
    return [(cx + rx * math.cos(2 * math.pi * i / n) * c
             - ry * math.sin(2 * math.pi * i / n) * s,
             cy + rx * math.cos(2 * math.pi * i / n) * s
             + ry * math.sin(2 * math.pi * i / n) * c)
            for i in range(n)]


def rot(p, deg, pivot=(528, 432)):
    """Rotate a point about the neck pivot — the head's forward tilt."""
    t = math.radians(deg)
    c, s = math.cos(t), math.sin(t)
    dx, dy = p[0] - pivot[0], p[1] - pivot[1]
    return (pivot[0] + dx * c - dy * s, pivot[1] + dx * s + dy * c)


def rpts(pts, deg, pivot=(528, 432)):
    return [rot(p, deg, pivot) for p in pts]


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


BG_GRAD = lin(0, 0, 0, 1000, (0, "#0E121C"), (1, "#04050A"))
PLATE_GRAD = rad((0, "#4A5478"), (0.5, "#2A3050"), (1, "#12162A"))
SKIN_GRAD = lin(460, 300, 540, 440, (0, "#E2C4A0"), (0.55, "#C09C7C"), (1, "#8A6650"))
SKIN_DIM = lin(460, 300, 540, 440, (0, "#BE9E80"), (1, "#7C5C46"))
HAIR_GRAD = lin(460, 290, 550, 400, (0, "#8A7052"), (0.5, "#5A422C"), (1, "#2A1C10"))
JACKET_GRAD = lin(500, 460, 620, 660, (0, "#4A4E5E"), (0.5, "#2A2D3A"), (1, "#12141C"))
TROUSER_GRAD = lin(400, 620, 560, 760, (0, "#3C4050"), (0.5, "#22242E"), (1, "#0E1016"))
CHAIR_GRAD = lin(390, 430, 660, 800, (0, "#3E424E"), (0.5, "#24262E"), (1, "#0E0F14"))
FLOOR_GRAD = lin(0, 795, 0, 885, (0, "#1E2430"), (0.55, "#12161E"), (1, "#080A0E"))
GLOW = "#9FE8E0"
STAR = "#E8F0F8"

# --- backdrop + starfield plate ------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#232840", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C8D4E8", strokeWidth=3, opacity=30)

# starfield — scattered, a few with a cross sparkle
stars = [(200, 200, 2.5, 70), (300, 150, 2, 55), (400, 120, 3, 80),
         (540, 140, 2, 50), (700, 160, 2.5, 65), (780, 240, 2, 55),
         (240, 320, 2, 60), (180, 450, 2.5, 70), (760, 420, 2, 50),
         (820, 340, 3, 75), (700, 540, 2, 55), (250, 560, 2, 50),
         (200, 640, 2.5, 60), (790, 600, 2, 55), (340, 180, 1.8, 45),
         (620, 120, 2, 60), (150, 280, 2, 50), (840, 470, 2.5, 65),
         (280, 700, 2, 50), (680, 660, 2.2, 55), (600, 190, 1.8, 45),
         (350, 250, 1.8, 40), (440, 170, 2.2, 55)]
for i, (x, y, r_, op) in enumerate(stars):
    assert on_disc(x, y, 6), i
    d.shape("ellipse", f"Star {i+1}", x=x - r_, y=y - r_, width=2 * r_,
            height=2 * r_, fill=STAR, opacity=op, stroke=NONE)
for i, (x, y, s) in enumerate([(400, 120, 9), (820, 340, 10), (620, 120, 8)]):
    d.path(f"M{x - s},{y} L{x + s},{y} M{x},{y - s} L{x},{y + s}",
           f"Sparkle {i+1}", fill=NONE, stroke=STAR, strokeWidth=2,
           opacity=45, cap="round")

# --- event horizon — a faint ring glowing upper-right ---------------------------------
d.shape("ellipse", "EH glow", x=556, y=206, width=190, height=190,
        fill=rad((0, GLOW, 28), (1, GLOW, 0)), stroke=NONE)
# the black disc itself
d.shape("ellipse", "EH hole", x=606, y=252, width=88, height=88,
        fill="#0A0E16", stroke=NONE)
# tilted accretion ring sweeping through the hole
ring = smooth(ellipse_pts(650, 296, 112, 30, -16), k=0.95)
d.path(ring, "Accretion ring", fill=NONE, stroke=GLOW, strokeWidth=5,
       opacity=50, cap="round")
d.path(ring, "Accretion halo", fill=NONE, stroke=GLOW, strokeWidth=11,
       opacity=18, cap="round")
# brighter lensed arc along the ring's lower-front leg
d.path("M566,326 C600,344 660,346 706,318", "Lensed arc", fill=NONE,
       stroke="#DFFCF6", strokeWidth=4, opacity=55, cap="round")
# a second, wider dust band behind
d.path("M560,262 C610,238 700,238 748,268", "Dust band", fill=NONE,
       stroke=GLOW, strokeWidth=3.5, opacity=22, cap="round", dash=[5, 8])

# --- floor chord the wheels stand on — closed on the disc's own arc --------------------
fy = 800
fl, fr = rim_x(fy, -1), rim_x(fy, 1)
d.path(f"M{fl:.1f},{fy} C350,788 650,788 {fr:.1f},{fy} "
       f"A{PR},{PR} 0 0 1 {fl:.1f},{fy} Z", "Floor", fill=FLOOR_GRAD,
       stroke=NONE)
d.path(f"M{fl + 8:.0f},{fy} C350,788 650,788 {fr - 8:.0f},{fy}",
       "Floor crest", fill=NONE, stroke="#3A465A", strokeWidth=5,
       opacity=38, cap="round")

# --- the chair, profile facing left -----------------------------------------------------
# backrest — tall, slightly reclined
d.path(smooth([(592, 660), (600, 560), (608, 470), (612, 428), (640, 426),
               (638, 470), (632, 560), (624, 658)], k=0.9), "Backrest",
       fill=CHAIR_GRAD, stroke=INK, strokeWidth=4.5)
# headrest pad tucked behind the head, on a short strut off the backrest
d.path("M586,396 L614,428", "Headrest strut", fill=NONE, stroke="#2A2D38",
       strokeWidth=8, cap="round")
d.path(smooth([(552, 348), (572, 338), (596, 342), (604, 364), (598, 390),
               (574, 396), (556, 384)], k=0.9), "Headrest",
       fill="#2E313C", stroke=INK, strokeWidth=4)
# seat slab
d.path("M450,634 L604,634 L600,660 L454,660 Z", "Seat",
       fill="#2A2D38", stroke=INK, strokeWidth=4)
# rear wheel — the big spoked wheel
wx, wy, wr = 575, 725, 70
d.shape("ellipse", "Wheel tire", x=wx - wr, y=wy - wr, width=2 * wr,
        height=2 * wr, fill="#14101C", stroke=INK, strokeWidth=6)
d.shape("ellipse", "Wheel rim", x=wx - 54, y=wy - 54, width=108,
        height=108, fill="#1C1E28", stroke="#4A4658", strokeWidth=4)
d.shape("ellipse", "Handrim", x=wx - 42, y=wy - 42, width=84, height=84,
        fill=NONE, stroke="#7A7286", strokeWidth=4, opacity=80)
for i in range(6):
    a = math.radians(i * 60 + 15)
    x2, y2 = wx + 52 * math.cos(a), wy + 52 * math.sin(a)
    d.path(f"M{wx},{wy} L{x2:.0f},{y2:.0f}", f"Spoke {i+1}", fill=NONE,
           stroke="#3E3A48", strokeWidth=3.5, cap="round")
d.shape("ellipse", "Hub", x=wx - 9, y=wy - 9, width=18, height=18,
        fill="#3E3A48", stroke=INK, strokeWidth=3)
# frame struts
d.path("M575,725 L545,650", "Frame strut", fill=NONE, stroke="#2A2D38",
       strokeWidth=8, cap="round")
d.path("M575,725 L448,748", "Frame lower", fill=NONE, stroke="#2A2D38",
       strokeWidth=7, cap="round")
# front caster
d.shape("ellipse", "Caster", x=397, y=754, width=36, height=36,
        fill="#14101C", stroke=INK, strokeWidth=5)
d.shape("ellipse", "Caster hub", x=409, y=766, width=12, height=12,
        fill="#3E3A48", stroke=NONE)
d.path("M430,760 L452,660", "Caster fork", fill=NONE, stroke="#2A2D38",
       strokeWidth=7, cap="round")
# legrest down to the foot platform
d.path("M458,656 L414,752", "Legrest strut", fill=NONE, stroke="#2A2D38",
       strokeWidth=7, cap="round")
d.path("M392,748 L448,748 L448,762 L388,762 Z", "Foot platform",
       fill="#2A2D38", stroke=INK, strokeWidth=3.5)

# --- the figure — reclined into the chair, facing left -----------------------------------
# trousers: thigh to the knee, shin down to the footrest
d.path(smooth([(550, 618), (478, 618), (432, 636), (420, 660), (414, 700),
               (402, 744), (430, 752), (442, 708), (450, 674), (522, 668),
               (556, 658)], k=0.9), "Trousers",
       fill=TROUSER_GRAD, stroke=INK, strokeWidth=4.5)
# shoe resting on the platform
d.path(smooth([(398, 744), (392, 756), (402, 764), (438, 764), (446, 754),
               (438, 742), (416, 738)], k=0.9), "Shoe",
       fill="#1A140E", stroke=INK, strokeWidth=3.5)
# jacket torso — leaning back onto the backrest
d.path(smooth([(534, 652), (542, 560), (550, 492), (568, 462), (606, 460),
               (614, 536), (608, 616), (592, 654)], k=0.9), "Jacket",
       fill=JACKET_GRAD, stroke=INK, strokeWidth=5)
# arm resting down to the lap — hand folded in
d.path(smooth([(560, 488), (584, 532), (590, 574), (576, 590), (508, 594),
               (472, 590), (468, 574), (504, 570), (556, 570)], k=0.9),
       "Arm", fill=JACKET_GRAD, stroke=INK, strokeWidth=4)
d.path(smooth([(462, 590), (458, 576), (466, 566), (484, 564), (494, 574),
               (492, 588), (480, 596)], k=0.9), "Hand lap",
       fill=SKIN_DIM, stroke=INK, strokeWidth=3.5)
# shirt collar hint at the open neck
d.path("M540,470 L566,462 L558,486 Z", "Collar",
       fill=lin(540, 462, 566, 486, (0, "#C8C0AC"), (1, "#7E765E")),
       stroke=INK, strokeWidth=3)
# neck
d.path(smooth([(518, 404), (516, 448), (522, 462), (542, 462), (546, 440),
               (542, 404)], k=0.85), "Neck",
       fill=SKIN_DIM, stroke=INK, strokeWidth=3.5)

# head — profile facing left, tipped -8 deg into the known forward lean
HT = -8
d.path(smooth(rpts([(516, 292), (482, 300), (466, 318), (458, 338),
                    (446, 352), (450, 360), (460, 368), (456, 380),
                    (462, 392), (470, 404), (492, 416), (522, 414),
                    (538, 396), (545, 348), (540, 306)], HT), k=0.85),
       "Head", fill=SKIN_GRAD, stroke=INK, strokeWidth=4)
# thinning hair over crown and back
d.path(smooth(rpts([(470, 316), (478, 294), (512, 284), (540, 296),
                    (546, 316), (544, 344), (534, 352), (528, 318),
                    (510, 302), (486, 306)], HT), k=0.9), "Hair",
       fill=HAIR_GRAD, stroke=INK, strokeWidth=3.5)
d.path(smooth(rpts([(540, 320), (544, 336), (544, 354), (540, 368)], HT),
              closed=False), "Hair back", fill=NONE, stroke="#5A422C",
       strokeWidth=3.5, opacity=60, cap="round")
# ear
d.path(smooth(rpts([(516, 352), (510, 358), (511, 368), (518, 378)], HT),
              closed=False), "Ear", fill=NONE, stroke=INK, strokeWidth=3,
       cap="round")
# glasses — one lens in profile + temple to the ear
d.path(smooth(rpts([(462, 342), (492, 342), (494, 346), (494, 366),
                    (490, 370), (464, 370), (460, 366)], HT), k=0.75),
       "Frame", fill=NONE, stroke=INK, strokeWidth=4, cap="round")
_t1, _t2 = rot((494, 352), HT), rot((516, 356), HT)
d.path(f"M{_t1[0]:.0f},{_t1[1]:.0f} L{_t2[0]:.0f},{_t2[1]:.0f}", "Temple",
       fill=NONE, stroke=INK, strokeWidth=3.5, cap="round")
_s1, _s2 = rot((466, 350), HT), rot((476, 346), HT)
d.path(f"M{_s1[0]:.0f},{_s1[1]:.0f} L{_s2[0]:.0f},{_s2[1]:.0f}",
       "Lens sheen", fill=NONE, stroke="#F2F6F0", strokeWidth=3,
       opacity=30, cap="round")
# eye, brow, nose shade, the small known smile
d.path(smooth(rpts([(468, 358), (473, 353), (482, 353), (486, 358),
                    (482, 363), (473, 363)], HT), k=0.9), "Eye",
       fill="#EFE4D0", stroke=INK, strokeWidth=2.5)
_ix, _iy = rot((478, 358), HT)
d.shape("ellipse", "Iris", x=_ix - 4, y=_iy - 4.5, width=8, height=9,
        fill="#2A2018", stroke=NONE)
d.path(smooth(rpts([(462, 338), (470, 333), (482, 333), (490, 338)], HT),
              closed=False), "Brow", fill=NONE, stroke="#4A3626",
       strokeWidth=3.5, opacity=70, cap="round")
d.path(smooth(rpts([(456, 392), (462, 397), (470, 398), (476, 395)], HT),
              closed=False), "Mouth", fill=NONE, stroke="#7A4A3A",
       strokeWidth=3.5, opacity=80, cap="round")
d.path(smooth(rpts([(452, 368), (456, 374), (456, 380), (452, 384)], HT),
              closed=False), "Nose shade", fill=NONE, stroke="#9A7658",
       strokeWidth=3, opacity=45, cap="round")
# cheek shade under the glasses
d.path(smooth(rpts([(478, 378), (486, 386), (492, 394), (494, 402)], HT),
              closed=False), "Cheek shade", fill=NONE, stroke="#9A7658",
       strokeWidth=4, opacity=22, cap="round")

# armrest + control box over the arm
d.path("M470,548 L608,548 L606,562 L468,562 Z", "Armrest",
       fill="#2E313C", stroke=INK, strokeWidth=3.5)
d.path("M452,532 L478,532 L478,548 L452,548 Z", "Control box",
       fill="#1C1E28", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Control light", x=458, y=537, width=6, height=6,
        fill=GLOW, opacity=70, stroke=NONE)
d.path("M480,562 L488,640", "Armrest strut", fill=NONE, stroke="#2A2D38",
       strokeWidth=6, cap="round")

# --- cool rim light off the event horizon ------------------------------------------------
d.path(smooth(rpts([(540, 306), (545, 330), (546, 360), (540, 386)], HT),
              closed=False), "Rim light head", fill=NONE, stroke=GLOW,
       strokeWidth=4, opacity=50, cap="round")
for i, dd in enumerate([
        "M572,464 C594,462 610,466 618,478",      # shoulder top
        "M612,486 C614,540 610,590 604,636",      # backrest rear
        "M428,638 C418,660 414,690 410,716",      # knee/shin front
        "M636,668 C646,690 648,716 644,742"]):    # wheel rear
    d.path(dd, f"Rim light {i+1}", fill=NONE, stroke=GLOW,
           strokeWidth=4 if i != 3 else 3.5,
           opacity=[45, 35, 30, 40][i], cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#1E2338", strokeWidth=6)

# --- captions ---------------------------------------------------------------------------
d.text("STEPHEN HAWKING", "Name", x=500, y=934, size=56,
       font="Virelai Sans", color="#E2E8F0", justify="center")
LINE2, SZ2, TRK = "BLACK HOLE RADIATION · 1974", 22, 400
r = d.text(LINE2, "Milestone", x=500, y=970, size=SZ2, font=SS3,
           color="#B8C2D4", justify="center")
d.cmd("text.setStyle", "Milestone tracking", id=r["id"], tracking=TRK)

b = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("milestone bounds", {k: round(v) for k, v in b.items()})
nearest = (min(max(PCX, b["x"]), b["x"] + b["width"]),
           min(max(PCY, b["y"]), b["y"] + b["height"]))
clear = math.hypot(nearest[0] - PCX, nearest[1] - PCY) - (PR + 3)
print("clears rim by %.1f" % clear)
assert clear > 0 and b["width"] <= 760 and b["x"] >= 10 and b["x"] + b["width"] <= 990, b

d.finish("stephen-hawking-V1R00")
