#!/usr/bin/env python3
"""Ludwig van Beethoven — milestone card V1R00. The storm-browed mature
master: wild grey-streaked mane swept up and back, dark high-collared coat
over a white cravat, mid-frown as if hearing the Ninth from inside.
Portrait bust — the likeness lives in the hair silhouette. Stormy slate
plate. 1000x1000. House style: gradients + translucent shading, never flat
fills. Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Ludwig van Beethoven — Milestone Card", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#1A1614"                    # warm dark ink, never pure black


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


BG_GRAD = lin(0, 0, 0, 1000, (0, "#12141C"), (1, "#06070B"))
PLATE_GRAD = rad((0, "#8E96A4"), (0.5, "#525E6E"), (1, "#20262F"))
COAT_GRAD = lin(350, 580, 660, 800, (0, "#32363F"), (0.55, "#1E2129"), (1, "#0D0F14"))
COAT_DIM = lin(350, 580, 660, 800, (0, "#22252D"), (1, "#0A0C10"))
SKIN_GRAD = rad((0, "#C89A72"), (0.6, "#9A6B46"), (1, "#5E3E24"))
HAIR_GRAD = lin(400, 290, 580, 540, (0, "#5A5046"), (0.55, "#332B24"), (1, "#181310"))
FLOOR_GRAD = lin(0, 745, 0, 880, (0, "#4A5160"), (0.55, "#30363F"), (1, "#12151B"))
CRAVAT_GRAD = lin(460, 560, 520, 640, (0, "#EFE8D6"), (0.6, "#C9BFA4"), (1, "#8E8468"))

# --- backdrop + stormy slate plate ----------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#2C3340", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D4DAE4", strokeWidth=3, opacity=38)

# one cold pool high left + sparse haze
d.shape("ellipse", "Light pool", x=265, y=145, width=420, height=250,
        fill="#DCE2EC", opacity=12, stroke=NONE)
for i, (x, y, w) in enumerate([(350, 320, 90), (598, 244, 70), (722, 352, 80),
                               (268, 472, 60), (746, 496, 64), (482, 196, 55)]):
    assert on_disc(x, y, 20), i
    d.shape("ellipse", f"Haze {i+1}", x=x - w / 2, y=y - w / 5, width=w, height=w * 0.4,
            fill="#D0D8E4", opacity=9, stroke=NONE)

# --- floor chord, closing on the disc arc --------------------------------------------
fy = 790
fl, fr = rim_x(fy, -1), rim_x(fy, 1)
d.path(f"M{fl:.1f},{fy} C330,776 420,798 500,789 C580,780 670,786 {fr:.1f},{fy} "
       f"A{PR},{PR} 0 0 1 {fl:.1f},{fy} Z", "Floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{fl + 8:.0f},{fy} C330,776 420,798 500,789 C580,780 670,786 {fr - 8:.0f},{fy}",
       "Floor sheen", fill=NONE, stroke="#8A96A8", strokeWidth=5, opacity=36, cap="round")

# manuscript sheet leaning on the floor, right of the bust — the world cue
d.path(smooth([(618, 700), (694, 682), (726, 700), (724, 752),
               (700, 776), (632, 778), (610, 748)]),
       "Score sheet", fill=lin(618, 682, 724, 776, (0, "#B8B4A2"), (1, "#6E6A58")),
       opacity=62, stroke=INK, strokeWidth=3)
for i in range(3):
    yy = 714 + i * 14
    d.path(f"M632,{yy} C662,{yy - 8} 692,{yy - 8} 716,{yy}", f"Staff {i+1}",
           fill=NONE, stroke="#3E3A2E", strokeWidth=2.5, opacity=55, cap="round")

# soft shadow under the bust
d.shape("ellipse", "Figure shadow", x=330, y=758, width=380, height=30,
        fill="#08090D", opacity=34, stroke=NONE)

# --- Beethoven: portrait bust, the mane is the likeness --------------------------------
# coat — dark, high-collared, widening to the floor
d.path(smooth([(352, 640), (328, 688), (338, 744), (354, 790),
               (658, 790), (666, 726), (652, 666), (616, 626),
               (566, 594), (468, 590), (408, 606)]),
       "Coat", fill=COAT_GRAD, stroke=INK, strokeWidth=6)
# right-side shade so the coat turns
d.path(smooth([(566, 596), (614, 626), (648, 670), (658, 732),
               (652, 788), (566, 790), (560, 712), (552, 642)]),
       "Coat shade", fill=COAT_DIM, opacity=55, stroke=NONE)
# white cravat — a wrapped band bunching under the chin, drawn before
# the collar wings so the wings overlap its sides
d.path(smooth([(440, 584), (466, 570), (500, 568), (532, 578),
               (542, 600), (530, 618), (504, 628), (474, 626),
               (450, 612)]),
       "Cravat", fill=CRAVAT_GRAD, stroke=INK, strokeWidth=3.5)
d.path("M456,596 C472,606 496,608 516,600", "Cravat fold", fill=NONE,
       stroke="#8E8468", strokeWidth=3, opacity=70, cap="round")
d.path("M468,614 C484,620 502,620 514,612", "Cravat fold 2", fill=NONE,
       stroke="#8E8468", strokeWidth=2.5, opacity=55, cap="round")
# upturned collar — one tall band behind the cravat, wings folding forward
d.path(smooth([(414, 566), (408, 606), (414, 648), (434, 676),
               (458, 686), (478, 690), (506, 690), (534, 684),
               (556, 670), (570, 640), (570, 600), (560, 566),
               (540, 552), (520, 560), (516, 580), (524, 604),
               (540, 616), (452, 618), (434, 602), (428, 578)]),
       "Collar", fill=lin(420, 552, 570, 690, (0, "#3E434E"), (1, "#14161C")),
       stroke=INK, strokeWidth=4)
# collar fold lines where the wings break forward
d.path("M430,586 C426,616 430,646 444,668", "Collar fold L", fill=NONE,
       stroke="#0E1014", strokeWidth=3, opacity=60, cap="round")
d.path("M548,584 C554,612 550,642 536,664", "Collar fold R", fill=NONE,
       stroke="#0E1014", strokeWidth=3, opacity=60, cap="round")

# neck
d.path("M462,540 C462,554 460,566 456,578 C468,588 492,588 504,576 "
       "C500,562 498,550 498,536 Z", "Neck", fill=lin(460, 538, 500, 588,
       (0, "#A87A52"), (1, "#74502E")), stroke=INK, strokeWidth=3.5)

# head — broad mature face, slight forward thrust into the frown
d.path(smooth([(428, 424), (424, 460), (430, 498), (448, 526),
               (474, 542), (500, 540), (520, 522), (532, 492),
               (534, 452), (526, 414), (506, 390), (480, 382),
               (452, 388)]),
       "Head", fill=SKIN_GRAD, stroke=INK, strokeWidth=5)
d.path("M430,472 C433,498 447,520 468,532 C446,524 431,501 429,478 Z",
       "Cheek shade", fill="#5E3E24", opacity=38, stroke=NONE)
# jowl weight at the jaw corners — the mature face
d.path("M436,506 C440,522 452,534 466,538 C452,534 439,522 435,510 Z",
       "Jowl L", fill="#6E4526", opacity=35, stroke=NONE)
d.path("M524,502 C520,518 510,530 498,536 C510,530 520,518 523,506 Z",
       "Jowl R", fill="#6E4526", opacity=30, stroke=NONE)

# the mane — a leonine mass swept up and back that WRAPS the skull: it
# covers the crown, frames both cheeks down to the jaw, and the silhouette
# itself runs turbulent — big pointed tufts are built into the outline by
# alternating out/in pairs, not stuck on as blobs.
mane = [(424, 520), (412, 492), (404, 458), (392, 428), (378, 400),
        (366, 372), (376, 344), (366, 330), (384, 306), (376, 288),
        (400, 268), (398, 244), (424, 240), (432, 218), (458, 232),
        (474, 210), (496, 228), (524, 216), (540, 238), (566, 232),
        (582, 256), (580, 278), (604, 292), (602, 316), (620, 336),
        (610, 360), (622, 384), (606, 404), (606, 430), (590, 452),
        (584, 482), (568, 506), (556, 528), (544, 506), (548, 468),
        (546, 430), (536, 404), (518, 390), (494, 384), (468, 388),
        (448, 402), (438, 424), (436, 456), (438, 492)]
d.path(smooth(mane), "Mane", fill=HAIR_GRAD, stroke=INK, strokeWidth=5)
# grey streaks — long strands following the swept-back flow of the mane
for i, (x0, y0, cx1, cy1, x2, y2) in enumerate([
        (438, 396, 428, 348, 442, 296), (470, 384, 464, 330, 478, 272),
        (504, 382, 508, 328, 528, 268), (532, 396, 546, 344, 566, 300),
        (416, 440, 404, 402, 398, 356), (556, 436, 570, 396, 582, 354),
        (452, 368, 448, 330, 458, 292)]):
    d.path(f"M{x0},{y0} C{cx1},{cy1} {cx1},{cy1} {x2},{y2}", f"Grey streak {i+1}",
           fill=NONE, stroke="#A8A094", strokeWidth=4, opacity=60, cap="round")
# darker parting strokes for depth between the locks
for i, (x0, y0, x2, y2) in enumerate([(448, 380, 436, 320), (520, 374, 540, 310),
                                      (488, 376, 490, 296)]):
    d.path(f"M{x0},{y0} C{x0 + 8},{y0 - 22} {x2 - 8},{y2 + 18} {x2},{y2}",
           f"Mane part {i+1}", fill=NONE, stroke="#0E0A08", strokeWidth=3.5,
           opacity=55, cap="round")

# face — the frown: heavy knit brows, deep furrows, downturned mouth
# brows drawn thick and low, inner ends dropping toward the nose
d.path("M440,442 C452,432 468,428 480,434", "Brow L", fill=NONE,
       stroke="#2A1E14", strokeWidth=6, opacity=90, cap="round")
d.path("M496,434 C508,428 522,428 532,436", "Brow R", fill=NONE,
       stroke="#2A1E14", strokeWidth=6, opacity=90, cap= "round")
# the frown furrows — two short verticals between the brows
d.path("M482,436 C483,444 484,450 484,456", "Furrow L", fill=NONE,
       stroke="#5E3E24", strokeWidth=3.5, opacity=75, cap="round")
d.path("M492,434 C492,442 492,448 491,454", "Furrow R", fill=NONE,
       stroke="#5E3E24", strokeWidth=3.5, opacity=70, cap="round")
# eyes — shadowed under the brow overhang, looking slightly down-inward
d.path("M442,458 C452,452 466,450 476,456", "Lid L", fill=NONE,
       stroke=INK, strokeWidth=4.5, cap="round")
d.path("M448,465 C456,468 468,468 474,462", "Eye L", fill=NONE,
       stroke=INK, strokeWidth=3, opacity=85, cap="round")
d.path("M498,456 C508,450 520,450 528,456", "Lid R", fill=NONE,
       stroke=INK, strokeWidth=4.5, cap="round")
d.path("M503,463 C511,466 521,466 527,460", "Eye R", fill=NONE,
       stroke=INK, strokeWidth=3, opacity=85, cap="round")
# brow shadow — a soft band under the brow line
d.path("M438,452 C462,444 508,442 532,452 C508,446 462,448 438,456 Z",
       "Brow shadow", fill="#5E3E24", opacity=28, stroke=NONE)
# nose — strong, slightly broad at the tip
d.path("M484,458 C481,474 476,488 472,496 C478,503 490,503 496,496",
       "Nose", fill=NONE, stroke="#7E5230", strokeWidth=4,
       opacity=85, cap="round")
# mouth — set hard, corners pulled down; the frown lives here
d.path("M458,518 C470,512 490,511 504,517", "Mouth", fill=NONE,
       stroke="#5E2E20", strokeWidth=5.5, opacity=90, cap="round")
d.path("M454,522 C458,526 460,528 462,530", "Mouth corner L", fill=NONE,
       stroke="#5E2E20", strokeWidth=3.5, opacity=70, cap="round")
d.path("M506,520 C508,524 510,527 512,529", "Mouth corner R", fill=NONE,
       stroke="#5E2E20", strokeWidth=3.5, opacity=70, cap="round")
d.path("M466,530 C476,536 490,537 500,532", "Under lip", fill=NONE,
       stroke="#8A5C36", strokeWidth=2.5, opacity=45, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#232935", strokeWidth=6)

# --- captions -------------------------------------------------------------------
d.text("BEETHOVEN", "Name", x=500, y=934, size=56, font="Virelai Sans",
       color="#E2E6EE", justify="center")
LINE2, YEAR, SZ2, TRK = "THE NINTH · 1824", "1824", 22, 280
r = d.text(LINE2, "Milestone", x=500, y=970, size=SZ2, font="Virelai Sans",
           color="#B4BECE", justify="center")
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

d.finish("ludwig-van-beethoven-V1R00")
