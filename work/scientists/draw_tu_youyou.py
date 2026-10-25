#!/usr/bin/env python3
"""Tu Youyou — milestone card V1R00. In a modest lab behind the bench
band, holding a sprig of qinghao (sweet wormwood) up beside her face —
the plant is the hero prop, lifted into the warm light. White working
coat over a muted garment, short bob with straight fringe, dark
rectangular glasses, gentle smile. Mortar & pestle and a flask sit
dead-dark on the bench; nothing rivals the sprig. Figure crops behind
the bench band closed on the disc's own arc. 1000x1000. House style:
gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Tu Youyou — Milestone Card", 1000, 1000)

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


def leaf(bx, by, tx, ty, w=13):
    """A pointed-oval leaf from base (bx,by) to tip (tx,ty), half-width w."""
    dx, dy = tx - bx, ty - by
    ln = math.hypot(dx, dy) or 1
    px, py = -dy / ln * w, dx / ln * w
    mx, my = bx + dx * 0.45, by + dy * 0.45
    return smooth([(bx, by), (mx + px, my + py), (tx, ty),
                   (mx - px, my - py)], k=0.9)


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


BG_GRAD = lin(0, 0, 0, 1000, (0, "#171510"), (1, "#070503"))
PLATE_GRAD = rad((0, "#7E7A54"), (0.5, "#4E5034"), (1, "#202217"))
SKIN_GRAD = lin(440, 300, 540, 560, (0, "#E2C4A0"), (0.55, "#C09C7C"), (1, "#8A6650"))
SKIN_DIM = lin(440, 300, 540, 560, (0, "#BE9E80"), (1, "#7C5C46"))
HAIR_GRAD = lin(430, 230, 570, 430, (0, "#3A2A1E"), (0.5, "#241812"), (1, "#0F0A06"))
COAT_GRAD = lin(380, 500, 620, 810, (0, "#E4E0CE"), (0.5, "#B8B39C"), (1, "#6E6A58"))
COAT_DIM = lin(380, 500, 620, 810, (0, "#C8C4AE"), (1, "#5C5848"))
INNER_GRAD = lin(470, 494, 530, 600, (0, "#5A6E68"), (1, "#2A3633"))
BENCH_GRAD = lin(0, 792, 0, 880, (0, "#4A3E2E"), (0.55, "#2A2218"), (1, "#100C08"))
LEAF_GRAD = lin(550, 500, 620, 430, (0, "#A4B864"), (1, "#5A7330"))
LEAF_DIM = lin(550, 500, 620, 430, (0, "#8AA052"), (1, "#4C6228"))
BUD = "#D8C05C"

# --- backdrop + warm olive plate ---------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#33301F", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E4E0C4", strokeWidth=3, opacity=32)

# warm light pooling upper-left
d.shape("ellipse", "Light pool", x=245, y=140, width=400, height=235,
        fill="#F2E4BC", opacity=13, stroke=NONE)
# warm dust lenses — clear of the face zone
for i, (x, y, w) in enumerate([(292, 300, 78), (720, 300, 70), (255, 480, 62),
                               (745, 500, 70), (330, 620, 56)]):
    assert on_disc(x, y, 18), i
    d.shape("ellipse", f"Dust {i+1}", x=x - w / 2, y=y - w / 5, width=w,
            height=w * 0.4, fill="#EEDFB8", opacity=9, stroke=NONE)

# --- the lab coat, cropped by the bench band later -----------------------------------
d.path(smooth([(378, 810), (384, 700), (380, 616), (374, 552), (392, 505),
               (446, 492), (554, 492), (608, 505), (626, 552), (620, 616),
               (616, 700), (622, 810)], k=0.9), "Coat",
       fill=COAT_GRAD, stroke=INK, strokeWidth=5)
# coat fold shading — the hangs read vertical
for i, dd in enumerate([
        "M424,560 C418,630 416,700 420,770",
        "M576,560 C582,630 584,700 580,770"]):
    d.path(dd, f"Coat fold {i+1}", fill=NONE, stroke="#4C4838",
           strokeWidth=4, opacity=40, cap="round")
d.path("M400,514 C440,498 560,498 600,514", "Shoulder sheen", fill=NONE,
       stroke="#F4F0DC", strokeWidth=5, opacity=35, cap="round")
# patch pockets, sketched faint
d.path("M414,660 L462,660 L462,712 L414,712 Z", "Pocket L", fill=NONE,
       stroke="#4C4838", strokeWidth=3.5, opacity=40, cap="round")
d.path("M538,660 L586,660 L586,712 L538,712 Z", "Pocket R", fill=NONE,
       stroke="#4C4838", strokeWidth=3.5, opacity=40, cap="round")

# left sleeve — long lab-coat sleeve running down to the wrist at the bench
d.path(smooth([(392, 505), (364, 540), (348, 588), (338, 652), (336, 720),
               (340, 768), (360, 770), (366, 700), (372, 628), (382, 560),
               (402, 552)], k=0.9), "Sleeve L",
       fill=COAT_DIM, stroke=INK, strokeWidth=4)
# right sleeve — bent, forearm rising to hold the sprig
d.path(smooth([(608, 505), (632, 540), (644, 578), (644, 610), (630, 622),
               (614, 612), (606, 578), (600, 540)], k=0.9), "Sleeve R",
       fill=COAT_DIM, stroke=INK, strokeWidth=4)
# forearm sleeve to the wrist
d.path(smooth([(640, 612), (628, 600), (610, 592), (596, 590), (592, 600),
               (606, 610), (624, 620)], k=0.9), "Forearm sleeve",
       fill=COAT_GRAD, stroke=INK, strokeWidth=3.5)

# neck + garment under the coat
d.path("M484,448 L484,502 C492,509 508,509 516,502 L516,448 Z", "Neck",
       fill=SKIN_DIM, stroke=INK, strokeWidth=3.5)
d.path("M470,494 L530,494 L500,598 Z", "Inner garment",
       fill=INNER_GRAD, stroke=INK, strokeWidth=3.5)
# collar band + slim lapel edges hugging the V
d.path(smooth([(456, 498), (478, 488), (522, 488), (544, 498), (538, 516),
               (500, 508), (462, 516)], k=0.9), "Collar band",
       fill=lin(456, 488, 544, 516, (0, "#F0ECDA"), (1, "#A8A48C")),
       stroke=INK, strokeWidth=3.5)
d.path("M470,496 L496,580", "Lapel edge L", fill=NONE, stroke="#4C4838",
       strokeWidth=3.5, opacity=55, cap="round")
d.path("M530,496 L504,580", "Lapel edge R", fill=NONE, stroke="#4C4838",
       strokeWidth=3.5, opacity=55, cap="round")
d.path("M500,598 L500,760", "Coat placket", fill=NONE, stroke="#4C4838",
       strokeWidth=3, opacity=45, cap="round")
for i, yy in enumerate([612, 662, 712]):
    d.shape("ellipse", f"Coat button {i+1}", x=497.5, y=yy, width=5,
            height=5, fill="#E8E4D0", opacity=80, stroke=NONE)

# --- the bench — floor band closing on the disc's own arc -----------------------------
fy = 795
fl, fr = rim_x(fy, -1), rim_x(fy, 1)
d.path(f"M{fl:.1f},{fy} C350,780 650,782 {fr:.1f},{fy} "
       f"A{PR},{PR} 0 0 1 {fl:.1f},{fy} Z", "Bench", fill=BENCH_GRAD,
       stroke=NONE)
d.path(f"M{fl + 8:.0f},{fy} C350,780 650,782 {fr - 8:.0f},{fy}",
       "Bench crest", fill=NONE, stroke="#8A785C", strokeWidth=5,
       opacity=40, cap="round")

# left hand resting flat on the bench
d.path(smooth([(344, 786), (342, 772), (350, 764), (368, 764), (378, 772),
               (376, 786), (360, 792)], k=0.9), "Hand bench",
       fill=SKIN_DIM, stroke=INK, strokeWidth=3.5)
for i, xx in enumerate([352, 360, 368]):
    d.path(f"M{xx},768 L{xx - 1},784", f"Rest finger {i+1}", fill=NONE,
           stroke="#7A5238", strokeWidth=2.5, opacity=65, cap="round")

# dead-dark props — nothing may rival the sprig
# erlenmeyer flask, left
assert on_disc(312, 762, 8)
d.path("M306,738 L306,756 L290,792 L338,792 L322,756 L322,738 Z", "Flask",
       fill="#1C1812", stroke=INK, strokeWidth=3.5)
d.path("M298,784 L330,784", "Flask content", fill=NONE, stroke="#3A4434",
       strokeWidth=4, opacity=50, cap="round")
# mortar & pestle, right — the extraction that found artemisinin
assert on_disc(676, 766, 8)
d.path(smooth([(648, 760), (652, 784), (664, 794), (692, 794), (704, 784),
               (708, 760), (678, 752)], k=0.85), "Mortar",
       fill="#1C1812", stroke=INK, strokeWidth=3.5)
d.path("M672,742 L694,762", "Pestle", fill=NONE, stroke="#241E16",
       strokeWidth=9, cap="round")
d.path("M672,742 L694,762", "Pestle edge", fill=NONE, stroke=INK,
       strokeWidth=2.5, opacity=70, cap="round")

# --- the sprig — hero prop, lifted into the light --------------------------------------
# soft warm halo behind the sprig head
d.shape("ellipse", "Sprig halo", x=525, y=415, width=160, height=160,
        fill=rad((0, "#E8DCA8", 20), (1, "#E8DCA8", 0)), stroke=NONE)
# stem the hand grips, rising beside the face
d.path("M596,588 C592,540 586,494 572,446", "Sprig stem", fill=NONE,
       stroke="#5E7434", strokeWidth=4, cap="round")
# feathery alternate leaflets
for i, (bx, by, tx, ty, w, g) in enumerate([
        (594, 564, 562, 556, 15, LEAF_DIM),
        (590, 542, 626, 530, 14, LEAF_GRAD),
        (585, 522, 556, 506, 14, LEAF_GRAD),
        (580, 502, 612, 486, 13, LEAF_DIM),
        (576, 482, 550, 464, 12, LEAF_GRAD),
        (572, 462, 598, 446, 11, LEAF_GRAD),
        (572, 448, 566, 418, 10, LEAF_GRAD)]):
    assert on_disc(tx, ty, 8), i
    d.path(leaf(bx, by, tx, ty, w), f"Qinghao leaf {i+1}", fill=g,
           stroke=INK, strokeWidth=2.5, opacity=95)
# tiny yellow qinghao buds at the tip
for i, (x, y, r_) in enumerate([(564, 430, 4.5), (574, 422, 4), (556, 440, 3.5)]):
    assert on_disc(x, y, 8), i
    d.shape("ellipse", f"Bud {i+1}", x=x - r_, y=y - r_, width=2 * r_,
            height=2 * r_, fill=BUD, opacity=90, stroke=INK, strokeWidth=2)
# right hand gripping the stem base
d.path(smooth([(588, 600), (584, 584), (592, 572), (606, 570), (616, 580),
               (616, 596), (608, 606), (596, 606)], k=0.9), "Hand sprig",
       fill=SKIN_GRAD, stroke=INK, strokeWidth=3.5)
for i, xx in enumerate([590, 599]):
    d.path(f"M{xx},582 C{xx + 1},589 {xx + 1},595 {xx},600",
           f"Sprig finger {i+1}", fill=NONE, stroke="#7A5238",
           strokeWidth=2.5, opacity=70, cap="round")

# --- head -----------------------------------------------------------------------------
# bob hair mass — short, sides to the jaw
d.path(smooth([(440, 424), (420, 352), (424, 296), (446, 254), (482, 232),
               (520, 232), (554, 252), (576, 294), (580, 352), (560, 424),
               (546, 414), (552, 388), (448, 388), (454, 414)], k=0.9),
       "Hair mass", fill=HAIR_GRAD, stroke=INK, strokeWidth=4)
# face — round, mild
d.path(smooth([(500, 296), (546, 314), (554, 368), (540, 420), (500, 452),
               (460, 420), (446, 368), (454, 314)], k=0.85), "Face",
       fill=SKIN_GRAD, stroke=INK, strokeWidth=4)
# straight fringe across the forehead
d.path("M450,344 L550,344 C548,306 526,288 500,288 C474,288 454,306 "
       "450,344 Z", "Fringe", fill=HAIR_GRAD, stroke=NONE)
for i, dd in enumerate(["M470,300 C468,314 468,328 470,340",
                        "M500,294 C500,310 500,326 500,340",
                        "M530,300 C532,314 532,328 530,340"]):
    d.path(dd, f"Bang strand {i+1}", fill=NONE, stroke="#5E4632",
           strokeWidth=3, opacity=45, cap="round")
# soft cheek shades
d.path("M456,398 C460,416 468,430 480,438", "Cheek shade L", fill=NONE,
       stroke="#9A7658", strokeWidth=5, opacity=25, cap="round")
d.path("M544,398 C540,416 532,430 520,438", "Cheek shade R", fill=NONE,
       stroke="#9A7658", strokeWidth=5, opacity=25, cap="round")

# brows — level, mild
d.path("M456,352 C466,346 480,346 488,351", "Brow L", fill=NONE,
       stroke="#3A2A1E", strokeWidth=4, opacity=70, cap="round")
d.path("M512,351 C520,346 534,346 544,352", "Brow R", fill=NONE,
       stroke="#3A2A1E", strokeWidth=4, opacity=70, cap="round")
# rectangular glasses — the dark frames
d.path(smooth([(454, 354), (494, 354), (496, 358), (496, 380), (492, 384),
               (458, 384), (454, 380)], k=0.75), "Frame L", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.path(smooth([(546, 354), (506, 354), (504, 358), (504, 380), (508, 384),
               (542, 384), (546, 380)], k=0.75), "Frame R", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.path("M496,364 C498,361 502,361 504,364", "Bridge", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.path("M454,360 L442,354", "Temple L", fill=NONE, stroke=INK,
       strokeWidth=3.5, cap="round")
d.path("M546,360 L558,354", "Temple R", fill=NONE, stroke=INK,
       strokeWidth=3.5, cap="round")
d.path("M462,360 L472,356", "Lens sheen L", fill=NONE, stroke="#F2F6F0",
       strokeWidth=3, opacity=28, cap="round")
d.path("M514,360 L524,356", "Lens sheen R", fill=NONE, stroke="#F2F6F0",
       strokeWidth=3, opacity=28, cap="round")
# eyes behind the lenses — gentle
d.path("M462,372 C468,366 480,366 486,372 C480,378 468,378 462,372 Z",
       "Eye L", fill="#EFE4D0", stroke=INK, strokeWidth=3)
d.path("M514,372 C520,366 532,366 538,372 C532,378 520,378 514,372 Z",
       "Eye R", fill="#EFE4D0", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Iris L", x=470, y=367, width=10, height=11,
        fill="#2A2018", stroke=NONE)
d.shape("ellipse", "Iris R", x=520, y=367, width=10, height=11,
        fill="#2A2018", stroke=NONE)
d.shape("ellipse", "Glint L", x=472.5, y=369, width=3, height=3,
        fill="#FFF4DC", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=522.5, y=369, width=3, height=3,
        fill="#FFF4DC", opacity=90, stroke=NONE)
# nose + gentle smile
d.path("M503,384 C506,396 506,408 500,415", "Nose shade", fill=NONE,
       stroke="#9A7658", strokeWidth=3.5, opacity=45, cap="round")
d.path("M493,416 C498,419 505,419 510,416", "Nose base", fill=NONE,
       stroke="#8A6248", strokeWidth=3, opacity=55, cap="round")
d.path("M476,428 C489,435 511,435 524,427", "Mouth", fill=NONE,
       stroke="#7A4A3A", strokeWidth=4.5, opacity=80, cap="round")
d.path("M484,438 C493,441 507,441 516,438", "Lip shade", fill=NONE,
       stroke="#9A6248", strokeWidth=3, opacity=40, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#2B2A1C", strokeWidth=6)

# --- captions ----------------------------------------------------------------------
d.text("TU YOUYOU", "Name", x=500, y=934, size=60, font="Virelai Sans",
       color="#ECE8D4", justify="center")
LINE2, SZ2, TRK = "ARTEMISININ · 1972", 22, 500
r = d.text(LINE2, "Milestone", x=500, y=970, size=SZ2, font=SS3,
           color="#C4C8B4", justify="center")
d.cmd("text.setStyle", "Milestone tracking", id=r["id"], tracking=TRK)

b = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("milestone bounds", {k: round(v) for k, v in b.items()})
nearest = (min(max(PCX, b["x"]), b["x"] + b["width"]),
           min(max(PCY, b["y"]), b["y"] + b["height"]))
clear = math.hypot(nearest[0] - PCX, nearest[1] - PCY) - (PR + 3)
print("clears rim by %.1f" % clear)
assert clear > 0 and b["width"] <= 760 and b["x"] >= 10 and b["x"] + b["width"] <= 990, b

d.finish("tu-youyou-V1R00")
