#!/usr/bin/env python3
"""Nina Simone — milestone card V1R00. Seated at the piano, upright and
regal: a tall wrapped headwrap, gold drop earrings, hands raised over the
keys — the high priestess at full authority. The grand lid rises behind
her at frame right. Deep indigo plate. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Nina Simone — Milestone Card", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#141019"                    # warm dark ink, never pure black


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


BG_GRAD = lin(0, 0, 0, 1000, (0, "#0E1019"), (1, "#05060A"))
PLATE_GRAD = rad((0, "#6E7698"), (0.5, "#424A68"), (1, "#1B1E2E"))
GOWN_GRAD = lin(350, 580, 660, 800, (0, "#265A5C"), (0.55, "#163639"), (1, "#0A1A1C"))
GOWN_DIM = lin(350, 580, 660, 800, (0, "#1B4245"), (1, "#081416"))
SKIN_GRAD = rad((0, "#9A6A44"), (0.6, "#6E4526"), (1, "#3E2412"))
WRAP_GRAD = lin(440, 330, 540, 460, (0, "#D2A458"), (0.55, "#96702F"), (1, "#52401C"))
FLOOR_GRAD = lin(0, 745, 0, 880, (0, "#3E4456"), (0.55, "#282C3C"), (1, "#101320"))
GOLD = "#D8AE5E"
PIANO_GRAD = lin(0, 620, 0, 800, (0, "#2A2E3A"), (1, "#0C0E14"))

# --- backdrop + deep indigo plate -----------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#2E3248", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8DCe8".upper(), strokeWidth=3, opacity=38)

# cool light pool high left + sparse haze
d.shape("ellipse", "Light pool", x=262, y=142, width=430, height=255,
        fill="#E2E6F2", opacity=13, stroke=NONE)
for i, (x, y, w) in enumerate([(352, 318, 90), (596, 244, 70), (724, 350, 80),
                               (266, 472, 60), (744, 496, 64), (480, 196, 55)]):
    assert on_disc(x, y, 20), i
    d.shape("ellipse", f"Haze {i+1}", x=x - w / 2, y=y - w / 5, width=w, height=w * 0.4,
            fill="#DCE0EE", opacity=9, stroke=NONE)

# --- floor chord, closing on the disc arc --------------------------------------------
fy = 790
fl, fr = rim_x(fy, -1), rim_x(fy, 1)
d.path(f"M{fl:.1f},{fy} C330,776 420,798 500,789 C580,780 670,786 {fr:.1f},{fy} "
       f"A{PR},{PR} 0 0 1 {fl:.1f},{fy} Z", "Floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{fl + 8:.0f},{fy} C330,776 420,798 500,789 C580,780 670,786 {fr - 8:.0f},{fy}",
       "Floor sheen", fill=NONE, stroke="#8A92AC", strokeWidth=5, opacity=36, cap="round")

# --- the grand lid rising behind her, frame right ------------------------------------
# the open lid's silhouette: low at the tail (left), sweeping up-right
lid = [(610, 720), (620, 640), (646, 566), (686, 512), (730, 478),
       (770, 462), (796, 472), (800, 508), (784, 560), (752, 620),
       (724, 678), (708, 722)]
for x, y in lid: assert on_disc(x, y, 6), (x, y)
d.path(smooth(lid), "Grand lid", fill=lin(620, 470, 790, 720,
       (0, "#262B38"), (0.6, "#171B24"), (1, "#0B0D12")),
       stroke=INK, strokeWidth=5)
# the lid's edge highlight — the long curve catching light
d.path("M624,644 C648,570 690,510 736,486 C756,476 776,472 790,478",
       "Lid sheen", fill=NONE, stroke="#8A92AC", strokeWidth=4.5,
       opacity=55, cap="round")
# the prop stick — the slim rod holding the lid open, joining lid to case
d.path("M686,668 C712,616 740,566 764,524", "Prop stick", fill=NONE,
       stroke="#3A3E4C", strokeWidth=5, cap="round")
d.path("M688,664 C714,614 740,566 762,528", "Prop sheen", fill=NONE,
       stroke=GOLD, strokeWidth=2, opacity=45, cap="round")

# soft shadow under figure + piano
d.shape("ellipse", "Figure shadow", x=310, y=760, width=400, height=30,
        fill="#08090E", opacity=34, stroke=NONE)

# --- Nina: seated, upright and regal ---------------------------------------------------
# gown — deep teal, high-shouldered, widening to the floor; seated, so
# the skirt spreads wider than a standing figure
d.path(smooth([(340, 640), (316, 692), (328, 748), (348, 790),
               (640, 790), (652, 726), (640, 664), (606, 622),
               (560, 590), (466, 586), (404, 600)]),
       "Gown", fill=GOWN_GRAD, stroke=INK, strokeWidth=6)
d.path(smooth([(560, 592), (606, 622), (638, 668), (648, 730),
               (642, 788), (556, 790), (550, 710), (542, 642)]),
       "Gown shade", fill=GOWN_DIM, opacity=55, stroke=NONE)
# collar — a high wrapped neckline, matching the headwrap's gold edge
d.path(smooth([(446, 566), (472, 556), (504, 556), (528, 568),
               (534, 592), (520, 606), (496, 610), (468, 606),
               (450, 590)]),
       "Collar", fill=lin(448, 556, 530, 610, (0, "#2E6668"), (1, "#122628")),
       stroke=INK, strokeWidth=3.5)
d.path("M452,574 C472,564 506,564 526,574", "Collar gold trim", fill=NONE,
       stroke=GOLD, strokeWidth=3.5, opacity=80, cap="round")

# neck — held long and upright
d.path("M462,520 C462,538 460,554 456,568 C468,580 492,580 504,566 "
       "C500,552 498,536 498,518 Z", "Neck", fill=lin(460, 520, 500, 580,
       (0, "#8A5E3A"), (1, "#5C3C1E")), stroke=INK, strokeWidth=3.5)

# head — held high, level, chin neither dipped nor raised
d.path(smooth([(436, 404), (432, 442), (438, 484), (456, 516),
               (480, 534), (504, 532), (522, 514), (534, 482),
               (536, 440), (528, 402), (508, 376), (484, 368),
               (458, 374)]),
       "Head", fill=SKIN_GRAD, stroke=INK, strokeWidth=5)
d.path("M438,458 C441,486 455,510 474,522 C454,514 439,489 437,464 Z",
       "Cheek shade", fill="#3E2412", opacity=38, stroke=NONE)
# cheekbone light
d.path("M442,474 C454,466 468,464 478,468", "Cheekbone L", fill=NONE,
       stroke="#C08E5C", strokeWidth=4, opacity=55, cap="round")

# ears + statement earrings — big gold drops at the lobes
d.path("M434,448 C426,452 424,464 430,474 C436,478 442,474 444,464 "
       "C444,454 440,446 434,448 Z", "Ear L", fill="#6E4526",
       stroke=INK, strokeWidth=3)
d.shape("ellipse", "Earring L", x=420, y=474, width=20, height=34,
        fill=NONE, stroke=GOLD, strokeWidth=4)
d.path("M534,444 C542,448 544,460 538,470 C532,474 526,470 524,460 "
       "C524,450 528,442 534,444 Z", "Ear R", fill="#6E4526",
       stroke=INK, strokeWidth=3)
d.shape("ellipse", "Earring R", x=528, y=470, width=20, height=34,
        fill=NONE, stroke=GOLD, strokeWidth=4)

# the headwrap — stacked ochre wraps rising above the hairline, taller
# than the skull; the crown knot sits high-right
d.path(smooth([(430, 420), (424, 386), (428, 352), (440, 322),
               (458, 298), (480, 284), (504, 282), (526, 292),
               (544, 310), (554, 336), (556, 366), (550, 396),
               (544, 420), (536, 398), (532, 368), (522, 342),
               (506, 324), (486, 318), (466, 322), (450, 336),
               (440, 360), (436, 388)]),
       "Headwrap", fill=WRAP_GRAD, stroke=INK, strokeWidth=5)
# wrap folds — curved bands following the turban's rise
for i in range(3):
    yy = 344 + i * 30
    d.path(f"M{436 - i * 2},{yy} C{470},{yy - 26} {512},{yy - 28} {548 + i * 2},{yy - 4}",
           f"Wrap fold {i+1}", fill=NONE, stroke="#52401C", strokeWidth=4,
           opacity=60, cap="round")
# the knot — a gathered puff high-right
d.path(smooth([(520, 292), (528, 272), (544, 262), (560, 268),
               (568, 284), (562, 300), (546, 308), (530, 304)]),
       "Wrap knot", fill=WRAP_GRAD, stroke=INK, strokeWidth=4)
d.path("M534,282 C542,276 552,276 558,282", "Knot fold", fill=NONE,
       stroke="#52401C", strokeWidth=3, opacity=65, cap="round")

# face — level dark brows, heavy-lidded eyes at half-mast (authority,
# not sleep), full mouth set firm
d.path("M448,424 C460,418 474,416 484,420", "Brow L", fill=NONE,
       stroke="#241410", strokeWidth=5, opacity=88, cap="round")
d.path("M500,420 C512,416 526,416 536,422", "Brow R", fill=NONE,
       stroke="#241410", strokeWidth=5, opacity=88, cap="round")
d.path("M448,442 C458,436 472,434 482,440", "Lid L", fill=NONE,
       stroke=INK, strokeWidth=4.5, cap="round")
d.shape("ellipse", "Iris L", x=462, y=438, width=9, height=8,
        fill="#160E08", stroke=NONE)
d.path("M500,440 C510,434 524,434 534,440", "Lid R", fill=NONE,
       stroke=INK, strokeWidth=4.5, cap="round")
d.shape("ellipse", "Iris R", x=514, y=437, width=9, height=8,
        fill="#160E08", stroke=NONE)
# nose — broader, the nostril wings hinted
d.path("M486,444 C483,460 478,476 474,486 C480,494 492,494 498,487",
       "Nose", fill=NONE, stroke="#4E3018", strokeWidth=4,
       opacity=85, cap="round")
d.path("M472,486 C468,490 468,494 472,496", "Nostril L", fill=NONE,
       stroke="#4E3018", strokeWidth=3, opacity=75, cap="round")
d.path("M500,485 C504,489 504,493 500,495", "Nostril R", fill=NONE,
       stroke="#4E3018", strokeWidth=3, opacity=75, cap="round")
# mouth — full, level, resolved
d.path("M464,506 C476,512 494,512 506,506", "Mouth", fill=NONE,
       stroke="#5E2A20", strokeWidth=5.5, opacity=90, cap="round")
d.path("M470,512 C480,518 492,518 500,512", "Lower lip", fill=NONE,
       stroke="#8E5236", strokeWidth=3, opacity=50, cap="round")

# --- the piano across the front: case + keyboard band + raised hands -------------------
# piano case — a dark band across the lower figure, top edge the keybed
d.path(smooth([(330, 722), (340, 700), (380, 692), (430, 688),
               (500, 686), (570, 688), (630, 694), (660, 706),
               (664, 750), (660, 790), (348, 790), (336, 758)]),
       "Piano case", fill=PIANO_GRAD, stroke=INK, strokeWidth=5)
# keybed — ivory strip with black keys
d.path(smooth([(352, 694), (400, 688), (480, 686), (560, 688),
               (640, 694), (652, 702), (648, 716), (560, 712),
               (470, 710), (392, 710), (354, 714)]),
       "Keybed", fill=lin(350, 686, 650, 716, (0, "#EDE4CE"), (1, "#B4A888")),
       stroke=INK, strokeWidth=3.5)
# black keys — short dark ticks along the bed
for i in range(9):
    kx = 372 + i * 30
    ky = 694 + (i % 3) * 2
    d.path(f"M{kx},{ky} l4,14", f"Black key {i+1}", fill=NONE,
           stroke="#1A140C", strokeWidth=6, cap="round")
# case sheen — lacquer catching the light
d.path("M352,730 C440,718 560,718 648,730", "Case sheen", fill=NONE,
       stroke="#5A6480", strokeWidth=5, opacity=45, cap="round")

# forearms reaching forward over the keys — sleeves from the shoulders
d.path(smooth([(382, 660), (366, 682), (360, 706), (368, 726),
               (384, 738), (402, 736), (412, 718), (412, 696),
               (406, 674), (396, 658)]),
       "Sleeve L", fill=GOWN_GRAD, stroke=INK, strokeWidth=4.5)
d.path(smooth([(596, 656), (612, 678), (618, 702), (612, 722),
               (596, 734), (578, 732), (568, 714), (568, 692),
               (574, 670), (584, 654)]),
       "Sleeve R", fill=GOWN_GRAD, stroke=INK, strokeWidth=4.5)
# the hands raised over the keys — hovering, fingers curled to play:
# each a mitt with finger ticks, palms down
d.path(smooth([(396, 700), (402, 686), (418, 680), (434, 684),
               (442, 698), (438, 712), (424, 720), (408, 716)]),
       "Hand L", fill=SKIN_GRAD, stroke=INK, strokeWidth=3.5)
for i in range(3):
    d.path(f"M{404 + i * 10},{714} C{408 + i * 10},{718} {412 + i * 10},{718} {416 + i * 10},{714}",
           f"Key finger L{i+1}", fill=NONE, stroke="#3E2412",
           strokeWidth=2.5, opacity=70, cap="round")
d.path(smooth([(548, 696), (556, 682), (572, 676), (588, 680),
               (596, 694), (592, 708), (578, 716), (562, 712)]),
       "Hand R", fill=SKIN_GRAD, stroke=INK, strokeWidth=3.5)
for i in range(3):
    d.path(f"M{556 + i * 10},{710} C{560 + i * 10},{714} {564 + i * 10},{714} {568 + i * 10},{710}",
           f"Key finger R{i+1}", fill=NONE, stroke="#3E2412",
           strokeWidth=2.5, opacity=70, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#252A40", strokeWidth=6)

# --- captions -------------------------------------------------------------------
d.text("NINA SIMONE", "Name", x=500, y=934, size=56, font="Virelai Sans",
       color="#E4E8F2", justify="center")
LINE2, YEAR, SZ2, TRK = "MISSISSIPPI GODDAM · 1964", "1964", 22, 240
r = d.text(LINE2, "Milestone", x=500, y=970, size=SZ2, font="Virelai Sans",
           color="#B0B8CC", justify="center")
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

d.finish("nina-simone-V1R00")
