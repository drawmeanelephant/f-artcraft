#!/usr/bin/env python3
"""Joni Mitchell — milestone card V1R00. Laurel Canyon light: long
centre-parted blonde hair falling in two curtains, a lap dulcimer held
diagonal across the body, the far-off upward gaze. Soft golds over a dark
disc. 1000x1000. House style: gradients + translucent shading, never flat
fills. Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Joni Mitchell — Milestone Card", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#1C150E"                    # warm dark ink, never pure black


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


BG_GRAD = lin(0, 0, 0, 1000, (0, "#161207"), (1, "#080604"))
PLATE_GRAD = rad((0, "#9C8B5C"), (0.5, "#5E5238"), (1, "#262015"))
DRESS_GRAD = lin(350, 580, 660, 800, (0, "#3C4654"), (0.55, "#252C38"), (1, "#0F1219"))
DRESS_DIM = lin(350, 580, 660, 800, (0, "#2A313D"), (1, "#0B0D12"))
SKIN_GRAD = rad((0, "#E0B288"), (0.6, "#B4845A"), (1, "#6E4A28"))
HAIR_GRAD = lin(400, 320, 580, 700, (0, "#D9B878"), (0.5, "#A9854C"), (1, "#5E4224"))
FLOOR_GRAD = lin(0, 745, 0, 880, (0, "#585033"), (0.55, "#3A3524"), (1, "#181510"))
WOOD_GRAD = lin(420, 640, 640, 560, (0, "#A87C44"), (0.55, "#6E4C26"), (1, "#33200F"))

# --- backdrop + warm gold plate -------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#38301E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8DCB4", strokeWidth=3, opacity=38)

# Laurel Canyon light — one warm pool high left, sparse haze
d.shape("ellipse", "Light pool", x=262, y=142, width=430, height=255,
        fill="#F0E4BC", opacity=14, stroke=NONE)
for i, (x, y, w) in enumerate([(352, 318, 90), (596, 244, 70), (724, 350, 80),
                               (266, 472, 60), (744, 496, 64), (480, 196, 55)]):
    assert on_disc(x, y, 20), i
    d.shape("ellipse", f"Haze {i+1}", x=x - w / 2, y=y - w / 5, width=w, height=w * 0.4,
            fill="#EADFB8", opacity=9, stroke=NONE)

# --- floor chord, closing on the disc arc --------------------------------------------
fy = 790
fl, fr = rim_x(fy, -1), rim_x(fy, 1)
d.path(f"M{fl:.1f},{fy} C330,776 420,798 500,789 C580,780 670,786 {fr:.1f},{fy} "
       f"A{PR},{PR} 0 0 1 {fl:.1f},{fy} Z", "Floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{fl + 8:.0f},{fy} C330,776 420,798 500,789 C580,780 670,786 {fr - 8:.0f},{fy}",
       "Floor sheen", fill=NONE, stroke="#9C9066", strokeWidth=5, opacity=36, cap="round")

# soft shadow under the figure
d.shape("ellipse", "Figure shadow", x=330, y=758, width=380, height=30,
        fill="#0A0806", opacity=34, stroke=NONE)

# --- Joni: half-figure, dulcimer on the diagonal ---------------------------------------
# torso — dark indigo blouse widening to the floor
d.path(smooth([(356, 636), (330, 686), (340, 744), (356, 790),
               (656, 790), (664, 724), (650, 664), (614, 626),
               (564, 596), (470, 592), (412, 606)]),
       "Blouse", fill=DRESS_GRAD, stroke=INK, strokeWidth=6)
# right-side shade so the blouse turns
d.path(smooth([(566, 598), (614, 628), (648, 672), (656, 734),
               (650, 788), (566, 790), (560, 712), (552, 644)]),
       "Blouse shade", fill=DRESS_DIM, opacity=55, stroke=NONE)
# open collar — a soft V with a lapel shadow each side
d.path(smooth([(452, 596), (470, 618), (490, 640), (504, 642),
               (498, 618), (480, 600), (462, 592)]),
       "Collar V L", fill=lin(456, 592, 500, 642, (0, "#4A5464"), (1, "#181D26")),
       stroke=INK, strokeWidth=3)
d.path(smooth([(516, 596), (512, 620), (504, 642), (518, 640),
               (538, 616), (532, 596)]),
       "Collar V R", fill=lin(508, 596, 536, 640, (0, "#4A5464"), (1, "#181D26")),
       stroke=INK, strokeWidth=3)

# neck
d.path("M464,530 C464,546 462,560 458,574 C470,584 494,584 506,572 "
       "C502,558 500,544 500,528 Z", "Neck", fill=lin(460, 530, 502, 584,
       (0, "#C89A6E"), (1, "#8A6238")), stroke=INK, strokeWidth=3.5)

# head — oval, chin lifted a touch into the far-off gaze
d.path(smooth([(436, 418), (432, 456), (438, 496), (456, 526),
               (480, 542), (504, 540), (522, 522), (534, 492),
               (536, 452), (528, 414), (508, 388), (484, 380),
               (458, 386)]),
       "Head", fill=SKIN_GRAD, stroke=INK, strokeWidth=5)
d.path("M438,470 C441,496 455,518 474,530 C454,522 440,499 437,476 Z",
       "Cheek shade", fill="#8A5E34", opacity=36, stroke=NONE)
# high cheekbone light — the other likeness anchor
d.path("M444,488 C454,480 468,478 478,482", "Cheekbone L", fill=NONE,
       stroke="#E8C49A", strokeWidth=4, opacity=55, cap="round")
d.path("M508,484 C518,478 528,478 534,482", "Cheekbone R", fill=NONE,
       stroke="#E8C49A", strokeWidth=3.5, opacity=45, cap="round")

# hair — centre-parted blonde, two long curtains falling past the
# shoulders to the chest; the part dip at the crown is the signature.
# drawn as one mass behind+over the head, then the two front curtains
# as separate long shapes hugging the face.
hair_back = [(432, 540), (420, 500), (416, 452), (420, 406), (434, 366),
             (458, 338), (488, 326), (516, 330), (540, 350), (554, 384),
             (558, 424), (554, 470), (548, 510), (540, 542)]
d.path(smooth(hair_back), "Hair mass", fill=HAIR_GRAD, stroke=INK, strokeWidth=5)
# left curtain — from the centre part, down past the jaw to the chest
d.path(smooth([(470, 384), (448, 390), (434, 412), (428, 446),
               (426, 486), (430, 528), (436, 566), (444, 600),
               (452, 628), (462, 640), (468, 616), (462, 576),
               (456, 532), (452, 488), (452, 448), (458, 416),
               (466, 396)]),
       "Curtain L", fill=HAIR_GRAD, stroke=INK, strokeWidth=4)
# right curtain — mirrored, slightly fuller in the light
d.path(smooth([(502, 382), (522, 388), (534, 410), (540, 444),
               (542, 484), (540, 526), (536, 564), (528, 598),
               (518, 626), (508, 638), (502, 614), (508, 574),
               (514, 530), (518, 486), (518, 446), (512, 414),
               (506, 394)]),
       "Curtain R", fill=HAIR_GRAD, stroke=INK, strokeWidth=4)
# the centre part — a fine dark seam from the crown to the hairline
d.path("M486,384 C486,372 487,360 489,348", "Part", fill=NONE,
       stroke="#3E2C16", strokeWidth=3, opacity=80, cap="round")
# strand texture down each curtain — long, following the fall
for i, (x0, y0, x2, y2) in enumerate([(436, 420, 436, 560), (446, 404, 452, 580),
                                      (528, 418, 530, 560), (518, 402, 514, 578)]):
    d.path(f"M{x0},{y0} C{x0 - 3},{y0 + 50} {x2 - 3},{y2 - 60} {x2},{y2}",
           f"Strand {i+1}", fill=NONE, stroke="#EAD09A", strokeWidth=3,
           opacity=55, cap="round")

# face — brows soft and level, the gaze tipped up-left, mouth nearly closed
d.path("M448,438 C460,432 472,430 482,434", "Brow L", fill=NONE,
       stroke="#5E4224", strokeWidth=4.5, opacity=80, cap="round")
d.path("M500,434 C512,430 524,430 532,436", "Brow R", fill=NONE,
       stroke="#5E4224", strokeWidth=4.5, opacity=80, cap="round")
# eyes — lids level, irises set high-left so the gaze goes off and up
d.path("M448,456 C458,450 470,448 480,453", "Lid L", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.shape("ellipse", "Iris L", x=456, y=451, width=9, height=9,
        fill="#241A10", stroke=NONE)
d.path("M500,453 C510,448 522,448 530,453", "Lid R", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.shape("ellipse", "Iris R", x=508, y=449, width=9, height=9,
        fill="#241A10", stroke=NONE)
# under-lid shadow so the lids read open
d.path("M452,463 C460,466 472,466 478,461", "Eye L low", fill=NONE,
       stroke=INK, strokeWidth=2.5, opacity=70, cap="round")
d.path("M504,460 C512,463 522,463 528,458", "Eye R low", fill=NONE,
       stroke=INK, strokeWidth=2.5, opacity=70, cap="round")
# nose — straight, fine
d.path("M488,458 C485,472 481,486 478,494 C483,500 492,500 496,495",
       "Nose", fill=NONE, stroke="#8A5E34", strokeWidth=3.5,
       opacity=80, cap="round")
# mouth — small, level, contemplative
d.path("M466,516 C478,521 494,521 504,516", "Mouth", fill=NONE,
       stroke="#7E4630", strokeWidth=4.5, opacity=88, cap="round")
d.path("M472,521 C480,527 492,527 500,521", "Lower lip", fill=NONE,
       stroke="#A86A42", strokeWidth=2.5, opacity=45, cap="round")

# --- the lap dulcimer — a long narrow teardrop held on the diagonal ---------------------
# fret end up-left near the left hand, body resting low-right on the lap
# body — slender waisted shape, tip at lower right
d.path(smooth([(420, 700), (430, 668), (456, 646), (490, 636),
               (530, 634), (566, 646), (592, 668), (604, 696),
               (608, 722), (598, 748), (578, 768), (552, 778),
               (524, 776), (500, 762), (482, 740), (466, 722),
               (444, 714)]),
       "Dulcimer body", fill=WOOD_GRAD, stroke=INK, strokeWidth=5)
d.path(smooth([(560, 660), (584, 680), (594, 706), (590, 734),
               (572, 758), (548, 770), (554, 744), (560, 712),
               (562, 684)]),
       "Body shade", fill="#2A1A0C", opacity=42, stroke=NONE)
d.path("M596,700 C596,716 590,734 578,748", "Body sheen", fill=NONE,
       stroke="#D8B074", strokeWidth=4, opacity=55, cap="round")
# heart soundholes — two small hearts up the body
d.path("M536,668 c-6,-8 -16,-4 -14,6 c1,8 14,14 14,14 c0,0 13,-6 14,-14 c2,-10 -8,-14 -14,-6 Z",
       "Heart hole 1", fill="#1A1008", stroke=INK, strokeWidth=2.5)
d.path("M566,706 c-5,-7 -14,-3 -12,5 c1,7 12,12 12,12 c0,0 11,-5 12,-12 c2,-9 -7,-12 -12,-5 Z",
       "Heart hole 2", fill="#1A1008", stroke=INK, strokeWidth=2.5)
# fretboard — the long taper up-left
d.path("M438,672 L312,560 L326,546 L452,660 Z", "Fretboard",
       fill=lin(320, 548, 450, 668, (0, "#4A3620"), (1, "#241808")),
       stroke=INK, strokeWidth=3.5)
# strings — three fine lines down the fretboard onto the body
for i in range(3):
    t = i / 2
    sx, sy = 316 + 12 * t, 552 + 12 * t
    ex, ey = 540 + 30 * t, 700 + 38 * t
    d.path(f"M{sx:.0f},{sy:.0f} L{ex:.0f},{ey:.0f}", f"String {i+1}", fill=NONE,
           stroke="#D8C89A", strokeWidth=1.8, opacity=70, cap="round")
# head + pegs
d.path(smooth([(312, 556), (296, 540), (296, 524), (310, 516),
               (324, 522), (328, 538), (322, 552)]),
       "Dulcimer head", fill=lin(298, 516, 326, 554, (0, "#563E22"), (1, "#2A1C0C")),
       stroke=INK, strokeWidth=3)
for i, (px, py) in enumerate([(306, 532), (316, 526)]):
    d.shape("ellipse", f"Peg {i+1}", x=px - 3, y=py - 3, width=6, height=6,
            fill="#C8B088", stroke=INK, strokeWidth=2)
# frets — short ticks across the board
for i in range(4):
    t = i / 3
    fx = 330 + (430 - 330) * t
    fyy = 558 + (662 - 558) * t
    d.path(f"M{fx - 6:.0f},{fyy + 8:.0f} l14,-10", f"Fret {i+1}", fill=NONE,
           stroke="#8A7452", strokeWidth=2.5, opacity=70, cap="round")

# fretting hand — a mitt wrapping the board just short of the head
d.path(smooth([(300, 566), (296, 548), (304, 534), (322, 530),
               (338, 538), (344, 554), (338, 570), (324, 580),
               (308, 578)]),
       "Fret hand", fill=SKIN_GRAD, stroke=INK, strokeWidth=3.5)
for i in range(3):
    d.path(f"M{306 + i * 9},{556 + i * 2} C{312 + i * 9},{560 + i * 2} "
           f"{320 + i * 9},{560 + i * 2} {326 + i * 9},{556 + i * 2}",
           f"Fret finger {i+1}", fill=NONE, stroke="#8A6238",
           strokeWidth=2.5, opacity=70, cap="round")
# strumming hand — a mitt overlapping the body's lower edge
d.path(smooth([(548, 722), (562, 712), (582, 714), (596, 728),
               (598, 746), (586, 760), (566, 762), (552, 752),
               (546, 738)]),
       "Strum hand", fill=SKIN_GRAD, stroke=INK, strokeWidth=3.5)

# forearms — sleeves rooting into the torso and reaching their hands
d.path(smooth([(388, 706), (362, 686), (340, 656), (326, 624),
               (318, 596), (310, 578), (300, 566), (308, 552),
               (326, 550), (342, 566), (356, 596), (370, 630),
               (386, 664), (402, 690)]),
       "Sleeve L", fill=DRESS_GRAD, stroke=INK, strokeWidth=5)
d.path(smooth([(646, 730), (650, 694), (640, 656), (622, 624),
               (600, 600), (580, 592), (572, 604), (584, 630),
               (596, 662), (606, 700), (612, 736), (600, 748),
               (584, 752)]),
       "Sleeve R", fill=DRESS_GRAD, stroke=INK, strokeWidth=5)

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#2C2818", strokeWidth=6)

# --- captions -------------------------------------------------------------------
d.text("JONI MITCHELL", "Name", x=500, y=934, size=56, font="Virelai Sans",
       color="#EEE4C4", justify="center")
LINE2, YEAR, SZ2, TRK = "BLUE · 1971", "1971", 22, 280
r = d.text(LINE2, "Milestone", x=500, y=970, size=SZ2, font="Virelai Sans",
           color="#C4B88E", justify="center")
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

d.finish("joni-mitchell-V1R00")
