#!/usr/bin/env python3
"""Chien-Shiung Wu — milestone card V1R00. An elegant 1950s qipao under an
open lab coat, standing left-of-centre at the cobalt-60 cryostat — her
hand resting on its flange, the glowing source preferentially spraying
down-left. The apparatus pulls the whole composition subtly off
balance, the way the experiment broke parity. Hair swept up in a neat
bun, composed smile. Both figure and apparatus stand on a floor band
closed on the disc's own arc. 1000x1000. House style: gradients +
translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Chien-Shiung Wu — Milestone Card", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#1E150F"                    # warm dark ink, never pure black
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


BG_GRAD = lin(0, 0, 0, 1000, (0, "#12121E"), (1, "#05050A"))
PLATE_GRAD = rad((0, "#6A6E8E"), (0.5, "#3E4260"), (1, "#1A1C30"))
SKIN_GRAD = lin(400, 300, 520, 560, (0, "#E6C6A2"), (0.55, "#C29E80"), (1, "#8A6852"))
SKIN_DIM = lin(400, 300, 520, 560, (0, "#C4A284"), (1, "#7E5E48"))
HAIR_GRAD = lin(400, 220, 530, 420, (0, "#3A2C20"), (0.5, "#241812"), (1, "#0F0A06"))
QIPAO_GRAD = lin(400, 500, 560, 780, (0, "#2E6E5E"), (0.5, "#1C4A40"), (1, "#0C221C"))
COAT_GRAD = lin(330, 500, 590, 810, (0, "#DCDCD4"), (0.5, "#B0B2A8"), (1, "#62655E"))
COAT_DIM = lin(330, 500, 590, 810, (0, "#C2C4B8"), (1, "#50544C"))
STOCK_GRAD = lin(0, 720, 0, 795, (0, "#C6A283"), (1, "#8A6852"))
STEEL_GRAD = lin(630, 400, 720, 800, (0, "#4A5064"), (0.5, "#2A2E3E"), (1, "#101218"))
FLOOR_GRAD = lin(0, 795, 0, 885, (0, "#232838"), (0.55, "#141822"), (1, "#080A10"))
PAPER_GRAD = lin(375, 640, 430, 690, (0, "#D8CCAE"), (1, "#94876C"))
GLOW = "#9FD8F0"

# --- backdrop + cool violet plate -------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#2C2E44", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D0D8EC", strokeWidth=3, opacity=32)

# light pooling upper-left, leaving the apparatus side dark
d.shape("ellipse", "Light pool", x=230, y=150, width=360, height=220,
        fill="#DDE4F0", opacity=10, stroke=NONE)
# drifting lenses — weighted left so the apparatus mass reads heavier
for i, (x, y, w) in enumerate([(280, 300, 76), (245, 480, 62), (330, 640, 56),
                               (600, 240, 64)]):
    assert on_disc(x, y, 18), i
    d.shape("ellipse", f"Mist {i+1}", x=x - w / 2, y=y - w / 5, width=w,
            height=w * 0.4, fill="#D8E0EC", opacity=9, stroke=NONE)

# --- floor band — figure and apparatus both stand on it ------------------------------------
fy = 800
fl, fr = rim_x(fy, -1), rim_x(fy, 1)
d.path(f"M{fl:.1f},{fy} C330,784 660,786 {fr:.1f},{fy} "
       f"A{PR},{PR} 0 0 1 {fl:.1f},{fy} Z", "Floor", fill=FLOOR_GRAD,
       stroke=NONE)
d.path(f"M{fl + 8:.0f},{fy} C330,784 660,786 {fr - 8:.0f},{fy}",
       "Floor crest", fill=NONE, stroke="#46506A", strokeWidth=5,
       opacity=38, cap="round")
d.shape("ellipse", "Shoe shadow", x=390, y=788, width=130, height=20,
        fill="#0A0C12", opacity=45, stroke=NONE)

# --- the cobalt-60 cryostat — the apparatus leaning the plate right -------------------------
# main column, dome-topped, standing on the floor
d.path("M640,796 L640,455 C640,424 655,404 676,404 C697,404 712,424 "
       "712,455 L712,796 Z", "Cryostat", fill=STEEL_GRAD, stroke=INK,
       strokeWidth=5)
# base flange + top cap ring
d.path("M632,780 L720,780 L720,796 L632,796 Z", "Base flange",
       fill="#1C202C", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Cap ring", x=646, y=398, width=60, height=18,
        fill="#2E3444", stroke=INK, strokeWidth=3.5)
d.path("M672,398 L672,380 L680,380 L680,398", "Valve stem", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
d.shape("ellipse", "Valve knob", x=668, y=370, width=16, height=12,
        fill="#3A4154", stroke=INK, strokeWidth=3)
# gauge dial on the upper column
d.shape("ellipse", "Gauge", x=654, y=442, width=44, height=44,
        fill="#161A24", stroke=INK, strokeWidth=3.5)
for i, a in enumerate([-50, 0, 50]):
    t = math.radians(a - 90)
    x1, y1 = 676 + 14 * math.cos(t), 464 + 14 * math.sin(t)
    x2, y2 = 676 + 18 * math.cos(t), 464 + 18 * math.sin(t)
    d.path(f"M{x1:.0f},{y1:.0f} L{x2:.0f},{y2:.0f}", f"Gauge tick {i+1}",
           fill=NONE, stroke="#8A94AC", strokeWidth=2.5, opacity=70,
           cap="round")
d.path("M676,464 L686,454", "Gauge needle", fill=NONE, stroke="#C8D2E4",
       strokeWidth=3, cap="round")
# chamber window with the glowing source inside
d.path(smooth([(652, 520), (700, 520), (702, 524), (702, 636), (698, 640),
               (654, 640), (650, 636), (650, 524)], k=0.8), "Chamber",
       fill="#0E1620", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Source glow", x=658, y=550, width=40, height=52,
        fill=rad((0, "#D8F0F8"), (0.55, "#7FC8E8"), (1, "#2E6884")),
        opacity=95, stroke=NONE)
d.shape("ellipse", "Source pellet", x=672, y=570, width=12, height=14,
        fill="#E8F8FC", stroke=NONE)
# the parity gag — electrons prefer one way: three strokes spray
# down-left inside the chamber, one weak one up
for i, (dd, op) in enumerate([
        ("M674,588 C662,598 656,610 656,624", 80),
        ("M678,584 C668,596 664,606 666,618", 65),
        ("M670,582 C660,588 652,596 650,608", 55),
        ("M680,576 C684,568 686,560 685,552", 30)]):
    d.path(dd, f"Beta {i+1}", fill=NONE, stroke=GLOW, strokeWidth=3,
           opacity=op, cap="round")
for i, (x, y, r_, op) in enumerate([(656, 628, 4, 85), (667, 622, 3.5, 70),
                                    (649, 612, 3, 60), (685, 548, 2.5, 35)]):
    d.shape("ellipse", f"Beta dot {i+1}", x=x - r_, y=y - r_,
            width=2 * r_, height=2 * r_, fill=GLOW, opacity=op,
            stroke=NONE)
# detector ring hugging the column at the chamber
d.path("M626,588 C648,604 704,604 726,588", "Detector front", fill=NONE,
       stroke="#5E6A86", strokeWidth=7, opacity=85, cap="round")
d.path("M630,566 C650,552 702,552 722,566", "Detector back", fill=NONE,
       stroke="#4A5470", strokeWidth=5, opacity=50, cap="round")
# cable drooping to a small electronics box left of the column base
d.path("M640,700 C624,722 616,738 618,756", "Cable", fill=NONE,
       stroke="#161A24", strokeWidth=6, cap="round")
d.path("M576,754 L640,754 L644,794 L572,794 Z", "Electronics box",
       fill="#1C202C", stroke=INK, strokeWidth=4)
for i, x in enumerate([590, 606]):
    d.shape("ellipse", f"Box light {i+1}", x=x, y=764, width=6, height=6,
            fill=GLOW if i == 0 else "#D8A862", opacity=75, stroke=NONE)
# a ledge on the column's left edge for her resting hand
d.path("M614,634 L646,634 L646,648 L614,648 Z", "Flange ledge",
       fill="#2E3444", stroke=INK, strokeWidth=3.5)

# --- legs + shoes — stockinged calves under the qipao hem ------------------------------------
d.path(smooth([(420, 726), (416, 750), (414, 772), (420, 786), (436, 786),
               (440, 758), (442, 726)], k=0.8), "Calf L",
       fill=STOCK_GRAD, stroke=INK, strokeWidth=3.5)
d.path(smooth([(474, 726), (476, 758), (480, 786), (496, 786), (502, 772),
               (500, 750), (496, 726)], k=0.8), "Calf R",
       fill=STOCK_GRAD, stroke=INK, strokeWidth=3.5)
d.path(smooth([(410, 782), (406, 794), (414, 802), (444, 802), (450, 794),
               (446, 782), (428, 778)], k=0.9), "Shoe L",
       fill="#241A12", stroke=INK, strokeWidth=3)
d.path(smooth([(468, 782), (470, 794), (478, 802), (508, 802), (514, 794),
               (510, 782), (488, 778)], k=0.9), "Shoe R",
       fill="#241A12", stroke=INK, strokeWidth=3)

# --- lab coat open over the qipao ------------------------------------------------------------
d.path(smooth([(338, 800), (346, 700), (340, 610), (336, 552), (354, 506),
               (412, 492), (510, 492), (568, 506), (582, 556), (576, 616),
               (570, 700), (574, 800)], k=0.9), "Coat",
       fill=COAT_GRAD, stroke=INK, strokeWidth=5)
# qipao front showing between the open coat fronts
d.path(smooth([(398, 782), (404, 690), (410, 600), (416, 548), (428, 510),
               (452, 502), (492, 502), (516, 512), (522, 560), (520, 640),
               (524, 730), (522, 782)], k=0.9), "Qipao",
       fill=QIPAO_GRAD, stroke=INK, strokeWidth=4)
# coat front edges falling open
d.path("M430,510 C412,560 402,650 398,780", "Coat edge L", fill=NONE,
       stroke="#4A4E44", strokeWidth=4, opacity=55, cap="round")
d.path("M516,512 C522,570 524,660 522,780", "Coat edge R", fill=NONE,
       stroke="#4A4E44", strokeWidth=4, opacity=55, cap="round")
# mandarin collar + the diagonal frog closure — asymmetry at wardrobe scale
d.path(smooth([(428, 502), (446, 492), (478, 492), (496, 500), (492, 514),
               (462, 508), (432, 514)], k=0.9), "Mandarin collar",
       fill=lin(428, 492, 496, 514, (0, "#3E8470"), (1, "#1E4A3E")),
       stroke=INK, strokeWidth=3.5)
d.path("M494,510 C480,540 456,568 432,586", "Closure edge", fill=NONE,
       stroke="#0C221C", strokeWidth=3.5, opacity=70, cap="round")
for i, (x, y) in enumerate([(488, 524), (472, 544), (454, 562), (438, 578)]):
    d.shape("ellipse", f"Frog {i+1}", x=x - 3.5, y=y - 3.5, width=7,
            height=7, fill="#9EC8B8", opacity=85, stroke=INK,
            strokeWidth=1.5)
# qipao hem slit + a faint woven sheen
d.path("M470,760 L470,782", "Hem slit", fill=NONE, stroke="#0C221C",
       strokeWidth=3.5, opacity=60, cap="round")
d.path("M430,540 C440,600 444,670 442,740", "Qipao sheen", fill=NONE,
       stroke="#5E9C88", strokeWidth=4, opacity=30, cap="round")

# left arm — bent, holding a small notebook at the hip
d.path(smooth([(354, 506), (336, 540), (330, 586), (332, 620), (346, 630),
               (358, 620), (362, 586), (366, 548), (372, 522)], k=0.9),
       "Sleeve L", fill=COAT_DIM, stroke=INK, strokeWidth=4)
d.path(smooth([(340, 622), (344, 642), (352, 660), (362, 668), (372, 664),
               (370, 646), (364, 628)], k=0.9), "Forearm L",
       fill=COAT_GRAD, stroke=INK, strokeWidth=3.5)
d.path("M360,650 L414,640 L420,684 L366,694 Z", "Notebook",
       fill=PAPER_GRAD, stroke=INK, strokeWidth=3)
for i, (y1, y2) in enumerate([(656, 652), (666, 662), (676, 672)]):
    d.path(f"M370,{y1} L406,{y2}", f"Note line {i+1}", fill=NONE,
           stroke="#6A5E48", strokeWidth=2.5, opacity=60, cap="round")
d.path(smooth([(356, 664), (366, 656), (378, 658), (382, 668), (376, 676),
               (364, 676), (356, 672)], k=0.9), "Hand note",
       fill=SKIN_GRAD, stroke=INK, strokeWidth=3.5)

# right arm — extended to the apparatus, hand on the flange ledge
d.path(smooth([(568, 508), (588, 536), (600, 570), (606, 600), (598, 612),
               (584, 606), (576, 576), (568, 542)], k=0.9), "Sleeve R",
       fill=COAT_DIM, stroke=INK, strokeWidth=4)
d.path(smooth([(600, 604), (608, 618), (616, 632), (626, 638), (634, 630),
               (628, 616), (618, 602), (610, 596)], k=0.9), "Forearm R",
       fill=COAT_GRAD, stroke=INK, strokeWidth=3.5)
d.path(smooth([(618, 646), (622, 634), (632, 628), (644, 630), (648, 640),
               (642, 650), (628, 652)], k=0.9), "Hand apparatus",
       fill=SKIN_GRAD, stroke=INK, strokeWidth=3.5)

# neck
d.path("M438,446 L438,500 C446,507 462,507 470,500 L470,446 Z", "Neck",
       fill=SKIN_DIM, stroke=INK, strokeWidth=3.5)

# --- head — hair swept up into the bun, composed ----------------------------------------------
# bun first, slightly right of centre — the composition leans
d.shape("ellipse", "Bun", x=442, y=224, width=58, height=46,
        fill=HAIR_GRAD, stroke=INK, strokeWidth=4)
d.path("M450,244 C460,236 474,236 484,242", "Bun wave", fill=NONE,
       stroke="#6E5240", strokeWidth=3, opacity=50, cap="round")
# a slim hairpin with a jade bead — period elegance
d.path("M436,238 L470,228", "Hairpin", fill=NONE, stroke="#C8B88E",
       strokeWidth=3, opacity=85, cap="round")
d.shape("ellipse", "Pin bead", x=432, y=234, width=8, height=8,
        fill="#7EC8A8", stroke=INK, strokeWidth=2)
# hair mass framing the face, swept up
d.path(smooth([(410, 420), (396, 360), (398, 302), (414, 262), (444, 246),
               (478, 246), (508, 262), (524, 300), (526, 356), (516, 414),
               (504, 402), (506, 384), (404, 384), (406, 404)], k=0.9),
       "Hair mass", fill=HAIR_GRAD, stroke=INK, strokeWidth=4)
# face — oval, fine arched brows, composed
d.path(smooth([(460, 296), (506, 316), (514, 368), (502, 418), (460, 452),
               (418, 418), (406, 368), (414, 316)], k=0.85), "Face",
       fill=SKIN_GRAD, stroke=INK, strokeWidth=4)
# hairline sweeping up off the forehead
d.path("M410,342 C416,308 436,290 460,288 C486,288 508,306 514,340 "
       "C502,312 484,300 460,300 C438,300 420,316 410,342 Z",
       "Hairline", fill=HAIR_GRAD, stroke=NONE)
for i, dd in enumerate(["M448,292 C434,300 422,314 416,330",
                        "M478,290 C492,298 504,312 510,328"]):
    d.path(dd, f"Hair sweep {i+1}", fill=NONE, stroke="#5E4632",
           strokeWidth=3, opacity=45, cap="round")
# ears peeking under the sweep
d.path("M404,354 C396,360 396,374 406,380", "Ear L", fill=NONE,
       stroke=INK, strokeWidth=3, cap="round")
d.path("M516,354 C524,360 524,374 514,380", "Ear R", fill=NONE,
       stroke=INK, strokeWidth=3, cap="round")
# soft cheek shades
d.path("M416,398 C420,416 428,428 440,436", "Cheek shade L", fill=NONE,
       stroke="#9A7658", strokeWidth=5, opacity=25, cap="round")
d.path("M504,398 C500,416 492,428 480,436", "Cheek shade R", fill=NONE,
       stroke="#9A7658", strokeWidth=5, opacity=25, cap="round")

# fine arched brows — higher arc, refined
d.path("M420,354 C428,344 444,342 452,348", "Brow L", fill=NONE,
       stroke="#2E2015", strokeWidth=3.5, opacity=75, cap="round")
d.path("M468,348 C476,342 492,344 500,354", "Brow R", fill=NONE,
       stroke="#2E2015", strokeWidth=3.5, opacity=75, cap="round")
# eyes — dark, direct
d.path("M422,370 C429,363 443,363 450,370 C443,377 429,377 422,370 Z",
       "Eye L", fill="#EFE4D0", stroke=INK, strokeWidth=3)
d.path("M470,370 C477,363 491,363 498,370 C491,377 477,377 470,370 Z",
       "Eye R", fill="#EFE4D0", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Iris L", x=432, y=365, width=10, height=11,
        fill="#241A12", stroke=NONE)
d.shape("ellipse", "Iris R", x=480, y=365, width=10, height=11,
        fill="#241A12", stroke=NONE)
d.shape("ellipse", "Glint L", x=434.5, y=367, width=3, height=3,
        fill="#FFF4DC", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=482.5, y=367, width=3, height=3,
        fill="#FFF4DC", opacity=90, stroke=NONE)
# nose + composed smile
d.path("M463,382 C467,396 467,408 460,416", "Nose shade", fill=NONE,
       stroke="#9A7658", strokeWidth=3.5, opacity=45, cap="round")
d.path("M453,417 C458,420 465,420 470,417", "Nose base", fill=NONE,
       stroke="#8A6248", strokeWidth=3, opacity=55, cap="round")
d.path("M436,428 C450,436 470,436 484,427", "Mouth", fill=NONE,
       stroke="#7A4436", strokeWidth=4.5, opacity=85, cap="round")
d.path("M444,438 C454,441 466,441 476,438", "Lip shade", fill=NONE,
       stroke="#9A6248", strokeWidth=3, opacity=40, cap="round")

# cool rim light off the source — her right side only
for i, dd in enumerate([
        "M516,306 C522,330 524,360 518,388",      # head right edge
        "M570,514 C578,540 580,570 578,600",      # coat right edge
        "M600,604 C608,618 616,630 624,638"]):    # forearm to the ledge
    d.path(dd, f"Source light {i+1}", fill=NONE, stroke=GLOW,
           strokeWidth=4, opacity=[40, 35, 45][i], cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#242638", strokeWidth=6)

# --- captions -------------------------------------------------------------------------------
d.text("CHIEN-SHIUNG WU", "Name", x=500, y=934, size=56,
       font="Virelai Sans", color="#E4E8F0", justify="center")
LINE2, SZ2, TRK = "PARITY VIOLATION · 1957", 22, 420
r = d.text(LINE2, "Milestone", x=500, y=970, size=SZ2, font=SS3,
           color="#BCC4D6", justify="center")
d.cmd("text.setStyle", "Milestone tracking", id=r["id"], tracking=TRK)

b = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("milestone bounds", {k: round(v) for k, v in b.items()})
nearest = (min(max(PCX, b["x"]), b["x"] + b["width"]),
           min(max(PCY, b["y"]), b["y"] + b["height"]))
clear = math.hypot(nearest[0] - PCX, nearest[1] - PCY) - (PR + 3)
print("clears rim by %.1f" % clear)
assert clear > 0 and b["width"] <= 760 and b["x"] >= 10 and b["x"] + b["width"] <= 990, b

d.finish("chien-shiung-wu-V1R00")
