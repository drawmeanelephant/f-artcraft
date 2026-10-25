#!/usr/bin/env python3
"""Louis Armstrong — milestone card V1R00. Joy at silhouette level: trumpet
raised high off the mouthpiece, white handkerchief waving in the free hand,
the huge open grin, 1920s suit. Stage floor closing on the disc's arc.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Louis Armstrong — Milestone Card", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#241A12"                    # warm dark ink, never pure black


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


BG_GRAD = lin(0, 0, 0, 1000, (0, "#161310"), (1, "#080605"))
PLATE_GRAD = rad((0, "#C79C5E"), (0.55, "#8A6238"), (1, "#402A18"))
SUIT_GRAD = lin(340, 600, 660, 800, (0, "#443C34"), (0.55, "#2A241E"), (1, "#151210"))
SUIT_DIM = lin(340, 600, 660, 800, (0, "#2C2620"), (1, "#100D0A"))
SKIN_GRAD = rad((0, "#B0794A"), (0.6, "#8A5A30"), (1, "#5C3418"))
SKIN_DIM = rad((0, "#8A5A30"), (1, "#4A2812"))
FLOOR_GRAD = lin(0, 745, 0, 880, (0, "#5C4C38"), (0.55, "#403324"), (1, "#1E1610"))
BRASS_GRAD = lin(540, 460, 760, 300, (0, "#E8C068"), (0.5, "#B8893C"), (1, "#6E4C1E"))

# --- backdrop + brass-club plate -----------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#43301C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F0E2BC", strokeWidth=3, opacity=40)

# warm stage pooling upper-left + drifting smoke haze
d.shape("ellipse", "Light pool", x=240, y=140, width=420, height=240,
        fill="#F2DCAC", opacity=14, stroke=NONE)
for i, (x, y, w) in enumerate([(335, 320, 90), (580, 235, 70), (720, 350, 80),
                               (258, 470, 60), (748, 495, 64), (465, 190, 55)]):
    assert on_disc(x, y, 20), i
    d.shape("ellipse", f"Haze {i+1}", x=x - w / 2, y=y - w / 5, width=w, height=w * 0.4,
            fill="#F2E4BC", opacity=11, stroke=NONE)

# --- stage floor, closing on the disc arc --------------------------------------------
fy = 790
fl, fr = rim_x(fy, -1), rim_x(fy, 1)
d.path(f"M{fl:.1f},{fy} C330,776 420,798 500,789 C580,780 670,786 {fr:.1f},{fy} "
       f"A{PR},{PR} 0 0 1 {fl:.1f},{fy} Z", "Floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{fl + 8:.0f},{fy} C330,776 420,798 500,789 C580,780 670,786 {fr - 8:.0f},{fy}",
       "Footlights", fill=NONE, stroke="#C8A060", strokeWidth=5, opacity=42, cap="round")
# a row of footlight glows along the crest
for i, xx in enumerate(range(int(fl) + 40, int(fr) - 30, 70)):
    d.shape("ellipse", f"Footlight {i+1}", x=xx, y=756, width=16, height=8,
            fill="#F2CE8A", opacity=60, stroke=NONE)

# soft shadow under the figure
d.shape("ellipse", "Figure shadow", x=320, y=758, width=400, height=30,
        fill="#100C06", opacity=32, stroke=NONE)

# --- Armstrong: half-figure, head thrown back at the horn -----------------------------
# sleeves first — roots tuck under the torso so the arms join the shoulders
# left arm (viewer's left) raised toward the handkerchief
d.path(smooth([(384, 650), (340, 620), (312, 572), (300, 524),
               (302, 486), (316, 456), (336, 452), (348, 476),
               (346, 522), (356, 566), (374, 608), (392, 638)]),
       "Sleeve L", fill=SUIT_GRAD, stroke=INK, strokeWidth=5)
# right arm (viewer's right) bent up to the trumpet valves
d.path(smooth([(622, 642), (656, 612), (672, 572), (664, 538),
               (650, 516), (630, 518), (622, 548), (620, 588),
               (614, 622)]),
       "Sleeve R", fill=SUIT_GRAD, stroke=INK, strokeWidth=5)

# torso — 1920s suit, seated bust widening to the floor
d.path(smooth([(350, 630), (326, 680), (336, 740), (352, 790),
               (660, 790), (668, 722), (654, 660), (618, 622),
               (566, 592), (470, 588), (408, 600)]),
       "Suit", fill=SUIT_GRAD, stroke=INK, strokeWidth=6)
# right-side shade so the torso turns
d.path(smooth([(566, 594), (616, 624), (650, 668), (662, 730),
               (656, 788), (566, 790), (560, 710), (552, 640)]),
       "Suit shade", fill=SUIT_DIM, opacity=55, stroke=NONE)
# white shirt front + dark tie
d.path(smooth([(452, 596), (478, 640), (494, 700), (498, 780),
               (534, 782), (536, 700), (528, 640), (510, 600),
               (482, 592)]),
       "Shirt front", fill=lin(470, 600, 530, 780, (0, "#F2ECDC"), (1, "#C4B8A0")),
       stroke=INK, strokeWidth=3.5)
d.path(smooth([(486, 606), (498, 612), (506, 606), (510, 640),
               (504, 700), (494, 740), (486, 700), (482, 640)]),
       "Tie", fill=lin(486, 606, 506, 740, (0, "#5E2A22"), (1, "#2E1410")),
       stroke=INK, strokeWidth=3)
# lapels — two notched folds flanking the shirt
d.path(smooth([(452, 594), (428, 630), (420, 690), (436, 760),
               (466, 780), (478, 760), (466, 700), (478, 648),
               (470, 614)]),
       "Lapel L", fill=lin(430, 600, 470, 780, (0, "#4E453A"), (1, "#241E18")),
       stroke=INK, strokeWidth=3.5)
d.path(smooth([(512, 596), (534, 634), (542, 700), (530, 770),
               (548, 780), (560, 720), (552, 656), (540, 616)]),
       "Lapel R", fill=lin(530, 600, 556, 780, (0, "#4E453A"), (1, "#241E18")),
       stroke=INK, strokeWidth=3.5)
# pocket square — a little white fold at the left chest
d.path("M400,690 L428,686 L424,706 L402,708 Z", "Pocket square",
       fill="#F2ECDC", stroke=INK, strokeWidth=2.5)

# neck
d.path("M462,540 C462,556 460,570 456,584 C468,594 492,594 504,582 "
       "C500,568 498,554 498,538 Z", "Neck", fill=lin(460, 540, 500, 594,
       (0, "#96683C"), (1, "#6E4522")), stroke=INK, strokeWidth=3.5)

# head — thrown slightly back-right toward the horn, chin up
d.path(smooth([(430, 408), (424, 446), (430, 486), (448, 516),
               (472, 532), (498, 528), (520, 510), (532, 480),
               (534, 442), (526, 406), (506, 382), (480, 374),
               (452, 380)]),
       "Head", fill=SKIN_GRAD, stroke=INK, strokeWidth=5)
# cheek volume + under-jaw shade
d.path("M430,462 C432,490 446,514 468,526 C446,518 430,494 428,470 Z",
       "Cheek shade", fill="#5C3418", opacity=40, stroke=NONE)
# short natural hair — a dark cap hugging the skull, receded hairline
d.path(smooth([(428, 420), (422, 384), (434, 352), (462, 332),
               (496, 326), (524, 338), (542, 364), (548, 396),
               (544, 418), (536, 428), (528, 406), (510, 392),
               (484, 386), (458, 390), (438, 404), (432, 424)]),
       "Hair", fill=lin(430, 330, 545, 425, (0, "#33241A"), (1, "#140D08")),
       stroke=INK, strokeWidth=4)
d.path("M436,404 C458,388 484,384 510,392", "Hairline", fill=NONE,
       stroke="#0E0806", strokeWidth=3.5, opacity=70, cap="round")
# ears
d.path("M426,452 C418,456 416,468 422,478 C428,482 434,478 436,468 "
       "C436,458 432,450 426,452 Z", "Ear L", fill=SKIN_DIM,
       stroke=INK, strokeWidth=3)
d.path("M530,448 C538,452 540,464 534,474 C528,478 522,474 520,464 "
       "C520,454 524,446 530,448 Z", "Ear R", fill=SKIN_DIM,
       stroke=INK, strokeWidth=3)

# the huge grin — cheeks up, eyes crinkled shut, open mouth with teeth
# cheek rises under each squinted eye
d.path("M442,468 C454,460 468,458 480,462", "Cheek lift L", fill=NONE,
       stroke="#6E4522", strokeWidth=4, opacity=60, cap="round")
d.path("M498,462 C508,456 520,455 528,458", "Cheek lift R", fill=NONE,
       stroke="#6E4522", strokeWidth=4, opacity=60, cap="round")
# squinted smiling eyes — upward arcs
d.path("M446,452 C456,444 468,443 476,449", "Eye L", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
d.path("M500,448 C510,441 521,440 529,445", "Eye R", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
# raised brows
d.path("M440,434 C452,426 468,424 480,429", "Brow L", fill=NONE,
       stroke="#2E2014", strokeWidth=4.5, opacity=80, cap="round")
d.path("M498,429 C510,423 524,422 534,427", "Brow R", fill=NONE,
       stroke="#2E2014", strokeWidth=4.5, opacity=80, cap="round")
# nose — broad, joyful lift
d.path("M478,458 C475,472 471,484 468,492 C473,499 484,500 490,494",
       "Nose", fill=NONE, stroke="#5C3418", strokeWidth=3.5,
       opacity=80, cap="round")
# the grin — wide open mouth, dark inside, bright teeth band on top
d.path(smooth([(448, 506), (462, 500), (486, 499), (510, 502),
               (524, 508), (520, 522), (504, 532), (482, 534),
               (462, 530), (450, 518)]),
       "Grin", fill=rad((0, "#38180E"), (1, "#180A05")),
       stroke=INK, strokeWidth=4)
d.path(smooth([(452, 508), (466, 502), (488, 501), (508, 504),
               (522, 509), (518, 515), (502, 519), (482, 520),
               (464, 518), (454, 513)]),
       "Teeth", fill="#F4EAD6", stroke=NONE)
# chin roundness under the grin
d.path("M462,538 C474,548 492,550 506,544", "Chin fold", fill=NONE,
       stroke="#5C3418", strokeWidth=3, opacity=55, cap="round")

# --- trumpet raised off the mouthpiece ----------------------------------------------
# axis: mouthpiece at the lips' right corner (~524,510) → bell mouth (806,312)
# leadpipe — long tube
d.path("M538,508 L738,363 L734,357 L534,502 Z", "Leadpipe",
       fill=BRASS_GRAD, stroke=INK, strokeWidth=3)
# bell flare — widening cone to the mouth ellipse
d.path(smooth([(738, 333), (762, 315), (790, 299), (810, 295),
               (806, 311), (790, 327), (762, 345), (746, 357)]),
       "Bell flare", fill=BRASS_GRAD, stroke=INK, strokeWidth=3.5)
d.path(rot_ellipse(806, 312, 24, 40, -40), "Bell mouth",
       fill=rad((0, "#5E3A12"), (0.7, "#8A5E22"), (1, "#E8C068")),
       stroke=INK, strokeWidth=3.5)
# bell lip highlight
d.path("M788,297 C798,289 812,289 820,297", "Bell lip", fill=NONE,
       stroke="#F2D88E", strokeWidth=4, opacity=80, cap="round")
# valve block + three valve caps under the right hand
d.path("M596,454 L660,410 L674,424 L610,468 Z", "Valve casing",
       fill=BRASS_GRAD, stroke=INK, strokeWidth=3)
for i, (vx, vy) in enumerate([(612, 434), (632, 421), (652, 408)]):
    d.shape("ellipse", f"Valve {i+1}", x=vx, y=vy, width=14, height=9,
            fill="#E8C068", stroke=INK, strokeWidth=2.5)
# tubing loop under the valves
d.path("M604,466 C620,478 646,476 664,462 C672,452 670,440 660,434",
       "Valve loop", fill=NONE, stroke="#B8893C", strokeWidth=5, cap="round")
# mouthpiece touching the lip corner
d.path("M518,514 L540,502 L545,511 L523,523 Z", "Mouthpiece",
       fill="#C8A050", stroke=INK, strokeWidth=2.5)
# brass sheen along the leadpipe
d.path("M560,494 C620,448 690,392 742,346", "Horn sheen", fill=NONE,
       stroke="#F6E2A0", strokeWidth=3.5, opacity=60, cap="round")

# right hand (viewer's right) gripping the valve casing
d.path(smooth([(602, 468), (616, 456), (638, 452), (656, 460),
               (662, 476), (654, 492), (636, 498), (616, 494),
               (604, 484)]),
       "Valve hand", fill=SKIN_GRAD, stroke=INK, strokeWidth=4)
for i in range(3):
    yy = 466 + i * 9
    d.path(f"M620,{yy} C630,{yy - 4} 642,{yy - 4} 652,{yy}",
           f"Grip finger {i+1}", fill=NONE, stroke="#4A2812",
           strokeWidth=3, opacity=70, cap="round")
d.path("M624,514 C636,504 650,502 662,510", "Cuff R", fill=NONE,
       stroke="#F2ECDC", strokeWidth=7, opacity=85, cap="round")

# left wrist cuff + the raised hand + handkerchief
d.path("M308,456 C318,446 334,444 346,452", "Cuff L", fill=NONE,
       stroke="#F2ECDC", strokeWidth=7, opacity=85, cap="round")
# the raised hand
d.path("M300,414 C306,400 322,394 336,400 C346,410 346,426 336,434 "
       "C322,440 306,434 300,414 Z", "Hankie hand", fill=SKIN_GRAD,
       stroke=INK, strokeWidth=4)
# handkerchief — a limp white cloth pinched at the hand, wavy hem
d.path(smooth([(302, 398), (288, 384), (268, 380), (250, 388),
               (240, 404), (244, 420), (238, 436), (250, 448),
               (268, 452), (286, 446), (300, 434), (308, 418)]),
       "Handkerchief", fill=lin(250, 380, 310, 450, (0, "#FAF6EC"), (1, "#CFC8B2")),
       stroke=INK, strokeWidth=3.5)
d.path("M258,396 C266,408 280,416 296,418", "Hankie fold 1", fill=NONE,
       stroke="#A89E88", strokeWidth=2.5, opacity=60, cap="round")
d.path("M252,424 C264,432 280,436 296,434", "Hankie fold 2", fill=NONE,
       stroke="#A89E88", strokeWidth=2.5, opacity=50, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#3A2A16", strokeWidth=6)

# --- captions -------------------------------------------------------------------
d.text("LOUIS ARMSTRONG", "Name", x=500, y=934, size=56, font="Virelai Sans",
       color="#F4E8CC", justify="center")
LINE2, YEAR, SZ2, TRK = "WEST END BLUES · 1928", "1928", 22, 280
r = d.text(LINE2, "Milestone", x=500, y=970, size=SZ2, font="Virelai Sans",
           color="#DCC79E", justify="center")
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

d.finish("louis-armstrong-V1R00")
