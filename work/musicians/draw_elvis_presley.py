#!/usr/bin/env python3
"""Elvis Presley — milestone card V1R00. Sun-era: pompadour with the
falling forelock, loose pale shirt, acoustic dreadnought slung low and
diagonal mid-swivel — all hips and nerve, pre-jumpsuit. Teal plate.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Elvis Presley — Milestone Card", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#14161A"                    # warm dark ink, never pure black


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


BG_GRAD = lin(0, 0, 0, 1000, (0, "#0C1516"), (1, "#040708"))
PLATE_GRAD = rad((0, "#5E9096"), (0.5, "#3A5E66"), (1, "#172E34"))
SHIRT_GRAD = lin(350, 600, 660, 800, (0, "#E4DAC2"), (0.55, "#B4A888"), (1, "#6E6250"))
SHIRT_DIM = lin(350, 600, 660, 800, (0, "#A89C80"), (1, "#524838"))
SKIN_GRAD = rad((0, "#D9A876"), (0.6, "#B07E4E"), (1, "#6E4424"))
HAIR_GRAD = lin(420, 320, 560, 520, (0, "#2E2018"), (0.6, "#171009"), (1, "#0A0705"))
FLOOR_GRAD = lin(0, 745, 0, 880, (0, "#3E565A"), (0.55, "#2A3A40"), (1, "#10181B"))
WOOD_GRAD = rad((0, "#C89258"), (0.55, "#96622E"), (1, "#4E2F14"))

# --- backdrop + teal plate -----------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#1E3840", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C4DADE", strokeWidth=3, opacity=38)

# one dim cool pool high left
d.shape("ellipse", "Light pool", x=260, y=150, width=400, height=240,
        fill="#D4E4E4", opacity=11, stroke=NONE)
for i, (x, y, w) in enumerate([(345, 318, 90), (592, 242, 70), (724, 350, 80),
                               (264, 470, 60), (748, 494, 64), (476, 194, 55)]):
    assert on_disc(x, y, 20), i
    d.shape("ellipse", f"Haze {i+1}", x=x - w / 2, y=y - w / 5, width=w, height=w * 0.4,
            fill="#C4D4D4", opacity=9, stroke=NONE)

# --- stage floor, closing on the disc arc --------------------------------------------
fy = 790
fl, fr = rim_x(fy, -1), rim_x(fy, 1)
d.path(f"M{fl:.1f},{fy} C330,776 420,798 500,789 C580,780 670,786 {fr:.1f},{fy} "
       f"A{PR},{PR} 0 0 1 {fl:.1f},{fy} Z", "Floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{fl + 8:.0f},{fy} C330,776 420,798 500,789 C580,780 670,786 {fr - 8:.0f},{fy}",
       "Floor sheen", fill=NONE, stroke="#7E9AA0", strokeWidth=5, opacity=36, cap="round")

# soft shadow under the figure
d.shape("ellipse", "Figure shadow", x=330, y=758, width=380, height=30,
        fill="#06090A", opacity=34, stroke=NONE)

# --- Elvis: half-figure, torso cocked mid-swivel -------------------------------------
# right forearm (viewer's left) reaching over the soundhole — root under torso
d.path(smooth([(368, 700), (384, 668), (400, 646), (420, 634),
               (438, 636), (442, 656), (434, 676), (416, 696),
               (394, 716), (376, 732)]),
       "Forearm strum", fill=SHIRT_GRAD, stroke=INK, strokeWidth=5)
# rolled sleeve cuff at the forearm's end
d.path("M382,700 C392,690 406,686 418,690", "Roll cuff L", fill=NONE,
       stroke="#F2E9D6", strokeWidth=6, opacity=80, cap="round")

# torso — loose Sun-era shirt, shoulders tilted, hem swinging right
d.path(smooth([(352, 644), (324, 690), (336, 746), (352, 790),
               (664, 790), (668, 720), (648, 656), (608, 618),
               (560, 592), (466, 596), (408, 612)]),
       "Shirt", fill=SHIRT_GRAD, stroke=INK, strokeWidth=6)
# right-side shade + a swing fold so the hem reads mid-motion
d.path(smooth([(566, 598), (614, 622), (646, 664), (658, 726),
               (656, 788), (572, 790), (562, 714), (552, 646)]),
       "Shirt shade", fill=SHIRT_DIM, opacity=55, stroke=NONE)
d.path("M344,706 C390,736 448,752 510,752", "Hem swing", fill=NONE,
       stroke="#847856", strokeWidth=4, opacity=60, cap="round")
# open collar — a loose V showing the chest hollow
d.path(smooth([(452, 592), (474, 606), (492, 630), (500, 660),
               (508, 630), (526, 606), (548, 594), (524, 590),
               (500, 586), (476, 588)]),
       "Open collar", fill=lin(474, 590, 526, 660, (0, "#B98A5C"), (1, "#7E522E")),
       stroke=INK, strokeWidth=3.5)
# collar wings + placket line
d.path(smooth([(448, 590), (430, 606), (426, 634), (438, 652),
               (458, 640), (466, 616), (462, 596)]),
       "Collar wing L", fill=lin(430, 592, 462, 652, (0, "#EFE5CC"), (1, "#B4A888")),
       stroke=INK, strokeWidth=3)
d.path(smooth([(552, 592), (570, 610), (574, 638), (560, 656),
               (542, 644), (534, 618), (538, 598)]),
       "Collar wing R", fill=lin(538, 594, 572, 656, (0, "#EFE5CC"), (1, "#B4A888")),
       stroke=INK, strokeWidth=3)
d.path("M500,664 C498,700 498,740 500,786", "Placket", fill=NONE,
       stroke="#847856", strokeWidth=3.5, opacity=60, cap="round")
# a couple of loose fold strokes — the shirt is untucked energy
d.path("M392,660 C420,676 448,682 474,678", "Shirt fold 1", fill=NONE,
       stroke="#8A7E62", strokeWidth=3.5, opacity=50, cap="round")
d.path("M560,668 C590,682 616,700 632,722", "Shirt fold 2", fill=NONE,
       stroke="#8A7E62", strokeWidth=3.5, opacity=50, cap="round")

# guitar strap — dark leather over the viewer's-right shoulder down to the heel
d.path("M566,592 C540,640 510,676 478,700", "Strap", fill=NONE,
       stroke="#241A12", strokeWidth=9, opacity=85, cap="round")

# neck
d.path("M462,530 C462,546 460,560 456,574 C468,584 492,584 504,572 "
       "C500,558 498,544 498,528 Z", "Neck", fill=lin(460, 528, 500, 584,
       (0, "#C89A66"), (1, "#8A5E36")), stroke=INK, strokeWidth=3.5)

# head — tipped a few degrees right, chin level, the smirk does the rest
d.path(smooth([(428, 418), (424, 456), (430, 496), (448, 526),
               (472, 542), (498, 540), (518, 522), (530, 492),
               (532, 452), (524, 414), (504, 386), (478, 378),
               (452, 384)]),
       "Head", fill=SKIN_GRAD, stroke=INK, strokeWidth=5)
d.path("M428,468 C431,494 446,516 466,528 C446,520 430,496 427,474 Z",
       "Cheek shade", fill="#8A5E36", opacity=38, stroke=NONE)
# ears + the start of a long sideburn
d.path("M424,452 C416,456 414,468 420,478 C426,482 432,478 434,468 "
       "C434,458 430,450 424,452 Z", "Ear L", fill="#8A5E36",
       stroke=INK, strokeWidth=3)
d.path("M530,448 C538,452 540,464 534,474 C528,478 522,474 520,464 "
       "C520,454 524,446 530,448 Z", "Ear R", fill="#8A5E36",
       stroke=INK, strokeWidth=3)
d.path("M428,470 L424,502 L432,508 L436,476 Z", "Sideburn L",
       fill="#1A120C", stroke=NONE)

# pompadour — tall swept-back mass with the forelock falling over the brow
d.path(smooth([(426, 440), (420, 402), (428, 358), (452, 322),
               (488, 306), (524, 312), (546, 336), (556, 370),
               (558, 406), (552, 430), (544, 444), (536, 420),
               (524, 396), (500, 384), (474, 386), (450, 398),
               (434, 420)]),
       "Pompadour", fill=HAIR_GRAD, stroke=INK, strokeWidth=5)
# swept ridges running back over the crown
d.path("M438,388 C460,356 496,340 528,348", "Pomp ridge 1", fill=NONE,
       stroke="#4A3524", strokeWidth=5, opacity=65, cap="round")
d.path("M434,408 C454,378 490,362 524,368", "Pomp ridge 2", fill=NONE,
       stroke="#3C2A1C", strokeWidth=4, opacity=50, cap="round")
# the forelock — one lock dropping loose onto the forehead
d.path(smooth([(452, 396), (442, 408), (438, 424), (444, 438),
               (454, 444), (462, 436), (460, 420), (462, 406)]),
       "Forelock", fill=HAIR_GRAD, stroke=INK, strokeWidth=3.5)

# face — heavy lids, low lazy brows, the half-smirk
d.path("M438,438 C450,432 466,430 478,434", "Brow L", fill=NONE,
       stroke="#1C120C", strokeWidth=5, opacity=85, cap="round")
d.path("M496,434 C508,430 522,430 532,434", "Brow R", fill=NONE,
       stroke="#1C120C", strokeWidth=5, opacity=85, cap="round")
# bedroom eyes — lid hoods a smaller almond, gaze straight
d.path("M440,452 C450,446 464,444 474,449", "Lid L", fill=NONE,
       stroke=INK, strokeWidth=4.5, cap="round")
d.path("M446,459 C454,462 466,462 472,457", "Eye L", fill=NONE,
       stroke=INK, strokeWidth=3, opacity=85, cap="round")
d.path("M496,450 C506,444 518,444 527,449", "Lid R", fill=NONE,
       stroke=INK, strokeWidth=4.5, cap="round")
d.path("M501,457 C509,460 519,460 525,455", "Eye R", fill=NONE,
       stroke=INK, strokeWidth=3, opacity=85, cap="round")
# nose — long and straight
d.path("M483,456 C480,470 476,484 473,492 C478,498 487,498 491,493",
       "Nose", fill=NONE, stroke="#7E522E", strokeWidth=3.5,
       opacity=80, cap="round")
# the smirk — mouth level left, corner curling up right
d.path("M456,510 C470,514 488,514 500,510", "Mouth", fill=NONE,
       stroke="#5E2E20", strokeWidth=4.5, opacity=90, cap="round")
d.path("M500,510 C508,508 514,504 518,498", "Smirk corner", fill=NONE,
       stroke="#5E2E20", strokeWidth=4, opacity=85, cap="round")
d.path("M462,516 C472,522 488,523 498,518", "Lower lip", fill=NONE,
       stroke="#8A5E36", strokeWidth=2.5, opacity=50, cap="round")

# --- the acoustic dreadnought slung low, neck to frame-right --------------------------
# body — figure-eight bout at viewer-left, tilted
d.path(smooth([(396, 622), (360, 630), (338, 660), (336, 692),
               (344, 726), (368, 756), (404, 772), (444, 776),
               (478, 766), (496, 738), (496, 706), (478, 680),
               (456, 664), (430, 656), (412, 644)]),
       "Guitar body", fill=WOOD_GRAD, stroke=INK, strokeWidth=5)
# bout edge shade + top sheen
d.path(smooth([(448, 668), (474, 686), (486, 712), (482, 742),
               (462, 764), (432, 772), (436, 750), (446, 720),
               (448, 694)]),
       "Body shade", fill="#3C2410", opacity=40, stroke=NONE)
d.path("M356,668 C368,644 392,630 416,630", "Body sheen", fill=NONE,
       stroke="#E8C890", strokeWidth=4, opacity=60, cap="round")
# soundhole + rosette ring
d.shape("ellipse", "Soundhole", x=398, y=676, width=52, height=52,
        fill=rad((0, "#120C06"), (1, "#2E1C0C")), stroke=INK, strokeWidth=3)
d.shape("ellipse", "Rosette", x=392, y=670, width=64, height=64,
        fill=NONE, stroke="#D8B884", strokeWidth=3, opacity=70)
# bridge — dark bar low on the body
d.path(smooth([(382, 738), (398, 734), (416, 734), (430, 738),
               (428, 748), (410, 752), (394, 750), (382, 746)]),
       "Bridge", fill=lin(384, 734, 430, 752, (0, "#3A2410"), (1, "#1E1208")),
       stroke=INK, strokeWidth=2.5)
# fretboard — long strip up-right to the headstock
d.path("M470,640 L642,508 L658,522 L486,654 Z", "Fretboard",
       fill=lin(500, 620, 640, 520, (0, "#3A2A1A"), (1, "#1C140C")),
       stroke=INK, strokeWidth=3)
# fret markers — short cross lines down the board
for i in range(6):
    t = i / 5
    fx = 488 + (640 - 488) * t
    fy2 = 644 + (516 - 644) * t
    d.path(f"M{fx - 5:.0f},{fy2 - 4:.0f} l12,9", f"Fret {i+1}", fill=NONE,
           stroke="#8A7452", strokeWidth=2.5, opacity=70, cap="round")
# headstock — a tapered block past the nut
d.path(smooth([(642, 500), (668, 478), (690, 478), (696, 492),
               (684, 508), (660, 516), (646, 514)]),
       "Headstock", fill=lin(644, 480, 696, 514, (0, "#4E3620"), (1, "#241808")),
       stroke=INK, strokeWidth=3.5)
for i, (px, py) in enumerate([(666, 486), (678, 486), (688, 490)]):
    d.shape("ellipse", f"Peg {i+1}", x=px - 3.5, y=py - 3.5, width=7, height=7,
            fill="#C8B088", stroke=INK, strokeWidth=2)

# strum hand — fingers fanned over the soundhole
d.path(smooth([(414, 650), (430, 642), (448, 646), (456, 660),
               (452, 676), (438, 684), (422, 680), (412, 668)]),
       "Strum hand", fill=SKIN_GRAD, stroke=INK, strokeWidth=3.5)
for i in range(3):
    d.path(f"M{420 + i * 4},{662 + i * 5} C{430 + i * 3},{658 + i * 5} {440 + i * 3},{660 + i * 5} {446 + i * 3},{666 + i * 5}",
           f"Strum finger {i+1}", fill=NONE, stroke="#6E4424",
           strokeWidth=3, opacity=70, cap="round")

# fret arm (viewer's right) — a forearm rooted inside the torso edge,
# rising to the board mid-neck
d.path(smooth([(630, 706), (634, 668), (628, 632), (614, 606),
               (596, 586), (578, 576), (564, 580), (568, 600),
               (582, 624), (598, 656), (612, 692)]),
       "Fret forearm", fill=SHIRT_GRAD, stroke=INK, strokeWidth=5)
d.path("M570,592 C578,582 590,578 600,582", "Roll cuff R", fill=NONE,
       stroke="#F2E9D6", strokeWidth=6, opacity=80, cap="round")
# fret hand — wrapped around the board mid-neck
d.path(smooth([(556, 566), (572, 556), (592, 552), (606, 560),
               (610, 576), (600, 590), (582, 594), (566, 588),
               (556, 578)]),
       "Fret hand", fill=SKIN_GRAD, stroke=INK, strokeWidth=3.5)
for i in range(3):
    d.path(f"M{566 + i * 3},{568 + i * 7} C{576 + i * 3},{562 + i * 7} {588 + i * 3},{562 + i * 7} {598 + i * 3},{568 + i * 7}",
           f"Fret finger {i+1}", fill=NONE, stroke="#6E4424",
           strokeWidth=3, opacity=70, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#1C3038", strokeWidth=6)

# --- captions -------------------------------------------------------------------
d.text("ELVIS PRESLEY", "Name", x=500, y=934, size=56, font="Virelai Sans",
       color="#DCF0F0", justify="center")
LINE2, YEAR, SZ2, TRK = "SUN SESSIONS · 1954", "1954", 22, 280
r = d.text(LINE2, "Milestone", x=500, y=970, size=22, font="Virelai Sans",
           color="#A8C4C8", justify="center")
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

d.finish("elvis-presley-V1R00")
