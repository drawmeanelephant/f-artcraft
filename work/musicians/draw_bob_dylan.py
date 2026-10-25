#!/usr/bin/env python3
"""Bob Dylan — milestone card V1R00. The 60s troubadour: tousled curls,
harmonica on the neck rack at the mouth, small-body acoustic slung low —
the milestone line carries the 2016 Nobel. Muted moss-grey plate.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Bob Dylan — Milestone Card", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#14160F"                    # warm dark ink, never pure black


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


def rot_ellipse(cx, cy, a, b, deg):
    t = math.radians(deg)
    c, s = math.cos(t), math.sin(t)
    pts = []
    for i in range(8):
        u = 2 * math.pi * i / 8
        x, y = a * math.cos(u), b * math.sin(u)
        pts.append((cx + x * c - y * s, cy + x * s + y * c))
    return smooth(pts)


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


BG_GRAD = lin(0, 0, 0, 1000, (0, "#0E120D"), (1, "#050705"))
PLATE_GRAD = rad((0, "#7C8E78"), (0.5, "#4A5C4E"), (1, "#1E2820"))
JKT_GRAD = lin(350, 600, 660, 800, (0, "#3A4250"), (0.55, "#242A34"), (1, "#101318"))
JKT_DIM = lin(350, 600, 660, 800, (0, "#2A303C"), (1, "#0C0E12"))
SKIN_GRAD = rad((0, "#DDB288"), (0.6, "#B08256"), (1, "#74502C"))
HAIR_GRAD = lin(400, 300, 580, 540, (0, "#3A281C"), (0.6, "#201410"), (1, "#0E0906"))
FLOOR_GRAD = lin(0, 745, 0, 880, (0, "#48544A"), (0.55, "#303A30"), (1, "#141814"))
WOOD_GRAD = rad((0, "#A87844"), (0.55, "#74502A"), (1, "#38220F"))

# --- backdrop + moss-grey plate ------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#2A362C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#CCD8C4", strokeWidth=3, opacity=38)

# one grey-green pool high left + sparse haze
d.shape("ellipse", "Light pool", x=260, y=150, width=410, height=245,
        fill="#DCE4D2", opacity=11, stroke=NONE)
for i, (x, y, w) in enumerate([(348, 318, 90), (592, 242, 70), (724, 350, 80),
                               (264, 470, 60), (748, 494, 64), (478, 194, 55)]):
    assert on_disc(x, y, 20), i
    d.shape("ellipse", f"Haze {i+1}", x=x - w / 2, y=y - w / 5, width=w, height=w * 0.4,
            fill="#D4DCC8", opacity=9, stroke=NONE)

# --- floor chord, closing on the disc arc --------------------------------------------
fy = 790
fl, fr = rim_x(fy, -1), rim_x(fy, 1)
d.path(f"M{fl:.1f},{fy} C330,776 420,798 500,789 C580,780 670,786 {fr:.1f},{fy} "
       f"A{PR},{PR} 0 0 1 {fl:.1f},{fy} Z", "Floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{fl + 8:.0f},{fy} C330,776 420,798 500,789 C580,780 670,786 {fr - 8:.0f},{fy}",
       "Floor sheen", fill=NONE, stroke="#8A9A8C", strokeWidth=5, opacity=36, cap="round")

# soft shadow under the figure
d.shape("ellipse", "Figure shadow", x=330, y=758, width=380, height=30,
        fill="#070A06", opacity=34, stroke=NONE)

# --- Dylan: half-figure, harp rack at the mouth, guitar low --------------------------
# strum forearm (viewer's left) over the guitar top — root under the torso
d.path(smooth([(370, 700), (386, 670), (402, 648), (422, 638),
               (440, 640), (444, 660), (436, 680), (418, 698),
               (396, 716), (378, 732)]),
       "Forearm strum", fill=JKT_GRAD, stroke=INK, strokeWidth=5)

# torso — dark work jacket widening to the floor
d.path(smooth([(354, 636), (330, 686), (340, 744), (356, 790),
               (660, 790), (668, 724), (654, 662), (618, 624),
               (566, 594), (470, 590), (410, 604)]),
       "Jacket", fill=JKT_GRAD, stroke=INK, strokeWidth=6)
# right-side shade so the jacket turns
d.path(smooth([(568, 596), (616, 626), (650, 670), (660, 732),
               (654, 788), (568, 790), (562, 712), (554, 642)]),
       "Jacket shade", fill=JKT_DIM, opacity=58, stroke=NONE)
# denim collar wings + a placket seam
d.path(smooth([(452, 594), (430, 620), (426, 656), (442, 682),
               (462, 668), (468, 632), (464, 602)]),
       "Collar L", fill=lin(432, 598, 468, 682, (0, "#46506A"), (1, "#1E2430")),
       stroke=INK, strokeWidth=3)
d.path(smooth([(516, 596), (538, 624), (544, 660), (528, 686),
               (508, 672), (502, 636), (506, 606)]),
       "Collar R", fill=lin(508, 600, 542, 686, (0, "#46506A"), (1, "#1E2430")),
       stroke=INK, strokeWidth=3)
d.path("M498,664 C498,706 500,748 500,786", "Placket", fill=NONE,
       stroke="#0E1014", strokeWidth=3.5, opacity=60, cap="round")

# guitar strap — over the viewer's-right shoulder down to the heel
d.path("M564,592 C540,632 514,662 486,682", "Strap", fill=NONE,
       stroke="#1E140C", strokeWidth=8, opacity=85, cap="round")

# neck
d.path("M462,532 C462,548 460,562 456,574 C468,584 492,584 504,572 "
       "C500,558 498,544 498,530 Z", "Neck", fill=lin(460, 530, 500, 584,
       (0, "#C69A6E"), (1, "#8A623A")), stroke=INK, strokeWidth=3.5)

# head — narrow, chin dipped a touch toward the harp
d.path(smooth([(432, 420), (428, 456), (434, 494), (452, 522),
               (476, 538), (500, 536), (518, 520), (530, 492),
               (532, 452), (524, 414), (504, 388), (480, 380),
               (456, 386)]),
       "Head", fill=SKIN_GRAD, stroke=INK, strokeWidth=5)
d.path("M434,468 C437,492 450,514 470,526 C450,518 436,496 433,474 Z",
       "Cheek shade", fill="#8A623A", opacity=38, stroke=NONE)
# ears under the curls
d.path("M430,456 C422,460 420,472 426,482 C432,486 438,482 440,472 "
       "C440,462 436,454 430,456 Z", "Ear L", fill="#8A623A",
       stroke=INK, strokeWidth=3)

# tousled curls — a lobed cloud of bumps breaking the silhouette
curls = [(430, 444), (418, 418), (414, 384), (420, 352), (436, 322),
         (462, 300), (492, 292), (522, 298), (544, 318), (558, 346),
         (560, 378), (552, 408), (540, 430), (530, 444), (522, 428),
         (526, 408), (514, 390), (494, 384), (472, 388), (454, 400),
         (440, 420)]
d.path(smooth(curls), "Curls", fill=HAIR_GRAD, stroke=INK, strokeWidth=5)
# ringlet ticks around the outer edge — small curls, ≥3pt
for i, (cx, cy, r) in enumerate([(428, 366, 10), (438, 336, 9), (462, 310, 10),
                                 (492, 298, 10), (524, 306, 9), (548, 332, 10),
                                 (556, 366, 9), (552, 400, 8)]):
    d.path(f"M{cx - r},{cy} a{r},{r} 0 1 1 {r},{r * 0.9}",
           f"Ringlet {i+1}", fill=NONE, stroke="#241812", strokeWidth=4,
           opacity=85, cap="round")

# face — narrow eyes, level mouth, working the harp
d.path("M442,438 C454,432 468,430 478,434", "Brow L", fill=NONE,
       stroke="#241812", strokeWidth=4.5, opacity=85, cap="round")
d.path("M498,434 C510,430 522,430 532,434", "Brow R", fill=NONE,
       stroke="#241812", strokeWidth=4.5, opacity=85, cap="round")
# narrow watchful eyes
d.path("M442,452 C452,446 466,444 476,449", "Lid L", fill=NONE,
       stroke=INK, strokeWidth=4.5, cap="round")
d.path("M448,459 C456,462 468,462 474,457", "Eye L", fill=NONE,
       stroke=INK, strokeWidth=3, opacity=85, cap="round")
d.path("M498,450 C508,444 520,444 528,449", "Lid R", fill=NONE,
       stroke=INK, strokeWidth=4.5, cap="round")
d.path("M503,457 C511,460 521,460 527,455", "Eye R", fill=NONE,
       stroke=INK, strokeWidth=3, opacity=85, cap="round")
# nose — straight, thin
d.path("M485,456 C482,470 478,484 475,492 C480,498 489,498 493,493",
       "Nose", fill=NONE, stroke="#8A623A", strokeWidth=3.5,
       opacity=80, cap="round")

# --- the harmonica rack — wire frame on the neck, bar at the mouth --------------------
# wire sides from the collar up to the bar ends
d.path("M452,566 C446,544 444,522 448,506", "Rack L", fill=NONE,
       stroke="#8A8E96", strokeWidth=3.5, opacity=85, cap="round")
d.path("M512,566 C518,544 520,522 516,506", "Rack R", fill=NONE,
       stroke="#8A8E96", strokeWidth=3.5, opacity=85, cap="round")
# the harp — a horizontal metal bar across the mouth
d.path(smooth([(444, 500), (468, 496), (496, 496), (520, 500),
               (522, 512), (498, 518), (470, 518), (446, 512)]),
       "Harmonica", fill=lin(446, 496, 522, 518, (0, "#B8BCC4"), (1, "#5E646E")),
       stroke=INK, strokeWidth=3)
for i in range(7):
    xx = 452 + i * 10
    d.path(f"M{xx},500 l2,14", f"Reed {i+1}", fill=NONE,
           stroke="#3A3E46", strokeWidth=2.5, opacity=70, cap="round")
# mouth just peeks under the harp
d.path("M468,524 C478,529 492,529 500,525", "Lower lip", fill=NONE,
       stroke="#7E5230", strokeWidth=2.5, opacity=50, cap="round")

# --- small-body acoustic, neck to frame-right at a working angle ----------------------
# body — compact figure-eight, viewer-left
d.path(smooth([(400, 632), (368, 640), (348, 668), (348, 700),
               (356, 730), (380, 756), (412, 768), (446, 768),
               (476, 756), (490, 730), (488, 702), (472, 680),
               (452, 666), (428, 658), (412, 648)]),
       "Guitar body", fill=WOOD_GRAD, stroke=INK, strokeWidth=5)
d.path(smooth([(450, 672), (472, 688), (482, 712), (476, 740),
               (458, 760), (432, 766), (438, 744), (446, 716),
               (448, 694)]),
       "Body shade", fill="#2E1C0C", opacity=40, stroke=NONE)
d.path("M360,676 C370,654 392,640 414,638", "Body sheen", fill=NONE,
       stroke="#D8B074", strokeWidth=4, opacity=60, cap="round")
# soundhole + ring
d.shape("ellipse", "Soundhole", x=400, y=682, width=46, height=46,
        fill=rad((0, "#100A06"), (1, "#2A180A")), stroke=INK, strokeWidth=3)
d.shape("ellipse", "Rosette", x=395, y=677, width=56, height=56,
        fill=NONE, stroke="#C8A068", strokeWidth=3, opacity=65)
# bridge
d.path(smooth([(388, 738), (404, 734), (420, 734), (432, 738),
               (430, 747), (414, 750), (398, 748), (388, 744)]),
       "Bridge", fill=lin(390, 734, 432, 750, (0, "#36220F"), (1, "#1C1108")),
       stroke=INK, strokeWidth=2.5)
# fretboard up-right
d.path("M476,646 L630,556 L644,568 L490,660 Z", "Fretboard",
       fill=lin(490, 640, 630, 560, (0, "#3A2A1A"), (1, "#1C140C")),
       stroke=INK, strokeWidth=3)
for i in range(5):
    t = i / 4
    fx = 492 + (624 - 492) * t
    fy2 = 646 + (566 - 646) * t
    d.path(f"M{fx - 5:.0f},{fy2 - 3:.0f} l12,7", f"Fret {i+1}", fill=NONE,
           stroke="#8A7452", strokeWidth=2.5, opacity=70, cap="round")
# headstock
d.path(smooth([(630, 550), (652, 532), (672, 532), (680, 544),
               (670, 558), (648, 566), (634, 562)]),
       "Headstock", fill=lin(634, 532, 678, 564, (0, "#4E3620"), (1, "#241808")),
       stroke=INK, strokeWidth=3.5)
for i, (px, py) in enumerate([(654, 540), (666, 540), (674, 546)]):
    d.shape("ellipse", f"Peg {i+1}", x=px - 3.5, y=py - 3.5, width=7, height=7,
            fill="#C8B088", stroke=INK, strokeWidth=2)

# strum hand over the soundhole
d.path(smooth([(416, 656), (432, 648), (450, 652), (458, 666),
               (454, 682), (440, 690), (424, 686), (414, 674)]),
       "Strum hand", fill=SKIN_GRAD, stroke=INK, strokeWidth=3.5)
for i in range(3):
    d.path(f"M{422 + i * 4},{668 + i * 5} C{432 + i * 3},{664 + i * 5} {442 + i * 3},{666 + i * 5} {448 + i * 3},{672 + i * 5}",
           f"Strum finger {i+1}", fill=NONE, stroke="#74502C",
           strokeWidth=3, opacity=70, cap="round")

# fret forearm rooted inside the torso's right edge, hand on the board
d.path(smooth([(632, 706), (636, 672), (630, 640), (616, 616),
               (598, 598), (580, 592), (568, 598), (572, 616),
               (586, 638), (602, 668), (614, 698)]),
       "Fret forearm", fill=JKT_GRAD, stroke=INK, strokeWidth=5)
d.path(smooth([(556, 576), (572, 564), (592, 560), (606, 568),
               (610, 584), (600, 598), (582, 602), (566, 596),
               (556, 588)]),
       "Fret hand", fill=SKIN_GRAD, stroke=INK, strokeWidth=3.5)
for i in range(3):
    d.path(f"M{566 + i * 3},{576 + i * 7} C{576 + i * 3},{570 + i * 7} {588 + i * 3},{570 + i * 7} {598 + i * 3},{576 + i * 7}",
           f"Fret finger {i+1}", fill=NONE, stroke="#74502C",
           strokeWidth=3, opacity=70, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#24301F", strokeWidth=6)

# --- captions -------------------------------------------------------------------
d.text("BOB DYLAN", "Name", x=500, y=934, size=56, font="Virelai Sans",
       color="#E4EAD8", justify="center")
LINE2, YEAR, SZ2, TRK = "NOBEL PRIZE · 2016", "2016", 22, 280
r = d.text(LINE2, "Milestone", x=500, y=970, size=22, font="Virelai Sans",
           color="#B4C4A8", justify="center")
d.cmd("text.setStyle", "Milestone tracking", id=r["id"], tracking=TRK)
# Virelai Sans has no digit glyphs — set the year in Source Sans 3
off = len(LINE2[:LINE2.index(YEAR)].encode("utf-8"))
d.cmd("text.setRangeStyle", "Year digits font", id=r["id"], start=off,
      end=off + len(YEAR), font="Source Sans 3")

b = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("milestone bounds", {k: round(v) for k, v in b.items()})
nearest = (min(max(PCX, b["x"]), b["x"] + b["width"]),
           min(max(PCY, b["y"]), b["y"] + b["height"]))
clear = math.hypot(nearest[0] - PCX, nearest[1] - PCY) - (PR + 3)
print("clears rim by %.1f" % clear)
assert clear > 0 and b["width"] <= 760 and b["x"] >= 10 and b["x"] + b["width"] <= 990, b

d.finish("bob-dylan-V1R00")
