#!/usr/bin/env python3
"""Jimi Hendrix — milestone card V1R00. Feedback-era stance: Strat-style
guitar flipped left-handed, neck held HIGH to frame-left, wild hair under
a headband, fringed suede jacket. Rust dawn plate. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Jimi Hendrix — Milestone Card", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#1C1410"                    # warm dark ink, never pure black


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


BG_GRAD = lin(0, 0, 0, 1000, (0, "#181008"), (1, "#070402"))
PLATE_GRAD = rad((0, "#C08A5E"), (0.5, "#7E5238"), (1, "#35201A"))
JKT_GRAD = lin(350, 600, 660, 800, (0, "#C4A678"), (0.55, "#96744C"), (1, "#523A24"))
JKT_DIM = lin(350, 600, 660, 800, (0, "#8A6A44"), (1, "#3E2C1A"))
SKIN_GRAD = rad((0, "#8E5A34"), (0.6, "#684024"), (1, "#40240F"))
HAIR_GRAD = lin(400, 300, 580, 540, (0, "#2A1C12"), (0.6, "#150E08"), (1, "#0A0604"))
FLOOR_GRAD = lin(0, 745, 0, 880, (0, "#5C4634"), (0.55, "#3E2E22"), (1, "#18100C"))
GTR_GRAD = rad((0, "#F2EDE2"), (0.55, "#C8BFAC"), (1, "#7E7464"))

# --- backdrop + rust dawn plate ------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#402A1E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F0D8BC", strokeWidth=3, opacity=38)

# low warm wash + sparse haze — morning field light
d.shape("ellipse", "Light pool", x=270, y=140, width=420, height=250,
        fill="#F0DCC0", opacity=12, stroke=NONE)
for i, (x, y, w) in enumerate([(350, 320, 90), (594, 240, 70), (724, 350, 80),
                               (266, 470, 60), (746, 494, 64), (478, 194, 55)]):
    assert on_disc(x, y, 20), i
    d.shape("ellipse", f"Haze {i+1}", x=x - w / 2, y=y - w / 5, width=w, height=w * 0.4,
            fill="#ECD8C4", opacity=9, stroke=NONE)

# --- field floor, closing on the disc arc --------------------------------------------
fy = 790
fl, fr = rim_x(fy, -1), rim_x(fy, 1)
d.path(f"M{fl:.1f},{fy} C330,776 420,798 500,789 C580,780 670,786 {fr:.1f},{fy} "
       f"A{PR},{PR} 0 0 1 {fl:.1f},{fy} Z", "Floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{fl + 8:.0f},{fy} C330,776 420,798 500,789 C580,780 670,786 {fr - 8:.0f},{fy}",
       "Floor sheen", fill=NONE, stroke="#A08460", strokeWidth=5, opacity=36, cap="round")

# soft shadow under the figure
d.shape("ellipse", "Figure shadow", x=320, y=758, width=400, height=30,
        fill="#0C0806", opacity=34, stroke=NONE)

# --- Jimi: half-figure, Strat neck held high to frame-left ----------------------------
# fret arm (viewer's left) raised to the high neck — sleeve first, root under torso
d.path(smooth([(390, 640), (366, 608), (352, 570), (354, 528),
               (362, 496), (378, 480), (394, 490), (394, 518),
               (388, 552), (392, 588), (404, 620)]),
       "Sleeve fret", fill=JKT_GRAD, stroke=INK, strokeWidth=5)
# sleeve fringe — short tassels hanging off its underside
for i, (fx, fy2) in enumerate([(366, 596), (360, 566), (360, 534)]):
    d.path(f"M{fx},{fy2} l-7,16 M{fx + 8},{fy2 + 4} l-6,15",
           f"Sleeve fringe {i+1}", fill=NONE, stroke="#DCC49A",
           strokeWidth=3, opacity=75, cap="round")

# torso — fringed suede jacket widening to the floor
d.path(smooth([(352, 636), (328, 686), (338, 744), (354, 790),
               (660, 790), (668, 722), (654, 660), (618, 622),
               (566, 592), (470, 588), (408, 602)]),
       "Jacket", fill=JKT_GRAD, stroke=INK, strokeWidth=6)
# right-side shade
d.path(smooth([(566, 594), (616, 624), (650, 668), (662, 730),
               (656, 788), (566, 790), (560, 710), (552, 640)]),
       "Jacket shade", fill=JKT_DIM, opacity=55, stroke=NONE)
# jacket front seam + fringe line down the chest
d.path("M498,600 C500,650 502,720 502,786", "Jacket seam", fill=NONE,
       stroke="#4A3520", strokeWidth=3.5, opacity=60, cap="round")
for i, yy in enumerate(range(628, 776, 21)):
    d.path(f"M{486},{yy} l-9,15 M{516},{yy} l9,15",
           f"Chest fringe {i+1}", fill=NONE, stroke="#DCC49A",
           strokeWidth=3, opacity=70, cap="round")
# collar lapels — wide suede wings
d.path(smooth([(452, 590), (430, 618), (426, 660), (442, 690),
               (464, 676), (472, 634), (468, 602)]),
       "Jacket lapel L", fill=lin(432, 594, 470, 690, (0, "#D8BC90"), (1, "#8A6A44")),
       stroke=INK, strokeWidth=3.5)
d.path(smooth([(514, 592), (536, 622), (542, 664), (526, 694),
               (506, 680), (500, 636), (504, 604)]),
       "Jacket lapel R", fill=lin(506, 596, 540, 694, (0, "#D8BC90"), (1, "#8A6A44")),
       stroke=INK, strokeWidth=3.5)

# neck
d.path("M462,538 C462,552 460,566 456,578 C468,588 492,588 504,576 "
       "C500,562 498,550 498,536 Z", "Neck", fill=lin(460, 536, 500, 588,
       (0, "#7E5230"), (1, "#583718")), stroke=INK, strokeWidth=3.5)

# head — chin lifted toward the high neck, facing up-left
d.path(smooth([(430, 416), (426, 452), (432, 492), (450, 520),
               (474, 536), (498, 534), (518, 516), (530, 486),
               (532, 448), (524, 410), (504, 384), (478, 376),
               (452, 382)]),
       "Head", fill=SKIN_GRAD, stroke=INK, strokeWidth=5)
d.path("M430,466 C433,492 448,514 468,526 C448,518 432,496 429,472 Z",
       "Cheek shade", fill="#4A2C14", opacity=40, stroke=NONE)
# ears peek out of the hair mass
d.path("M424,460 C416,464 414,476 420,486 C426,490 432,486 434,476 "
       "C434,466 430,458 424,460 Z", "Ear L", fill="#583718",
       stroke=INK, strokeWidth=3)

# wild hair — a big rounded cloud breaking the silhouette all around
d.path(smooth([(420, 448), (406, 416), (404, 372), (418, 330),
               (444, 298), (482, 284), (520, 288), (550, 310),
               (566, 344), (568, 384), (560, 420), (548, 442),
               (538, 424), (528, 400), (508, 384), (480, 380),
               (454, 388), (434, 408), (426, 434)]),
       "Hair cloud", fill=HAIR_GRAD, stroke=INK, strokeWidth=5)
# a few loose curl ticks around the cloud edge
for i, (cx, cy, dx, dy) in enumerate([(412, 352, -14, -8), (424, 320, -12, -12),
                                      (456, 296, -6, -16), (498, 288, 4, -16),
                                      (540, 304, 12, -12), (560, 342, 14, -6)]):
    d.path(f"M{cx},{cy} q{dx},{dy} {dx + 4},{dy - 14}",
           f"Curl {i+1}", fill=NONE, stroke="#241812", strokeWidth=4,
           opacity=85, cap="round")

# the headband — a band across the forehead, knot and tails at right
d.path(smooth([(430, 398), (452, 384), (486, 378), (518, 382),
               (540, 394), (542, 408), (518, 402), (486, 398),
               (452, 402), (432, 410)]),
       "Headband", fill=lin(430, 380, 542, 410, (0, "#A83A2E"), (1, "#5E1E16")),
       stroke=INK, strokeWidth=3)
d.path(smooth([(540, 394), (556, 392), (566, 402), (560, 414),
               (548, 414), (540, 406)]),
       "Band knot", fill="#8A2E24", stroke=INK, strokeWidth=3)
d.path("M560,410 C574,414 584,424 586,438 M552,414 C562,422 568,432 570,444",
       "Band tails", fill=NONE, stroke="#8A2E24", strokeWidth=5, cap="round")

# face — gaze up-left at the raised neck, faint moustache
d.path("M438,432 C450,424 464,422 476,426", "Brow L", fill=NONE,
       stroke="#1C1008", strokeWidth=4.5, opacity=85, cap="round")
d.path("M496,426 C508,420 522,420 532,424", "Brow R", fill=NONE,
       stroke="#1C1008", strokeWidth=4.5, opacity=85, cap="round")
# eyes half-open, lifted left
d.path("M440,448 C450,440 464,438 474,443", "Lid L", fill=NONE,
       stroke=INK, strokeWidth=4.5, cap="round")
d.path("M446,456 C454,460 466,460 472,455", "Eye L", fill=NONE,
       stroke=INK, strokeWidth=3, opacity=85, cap="round")
d.path("M496,443 C506,436 518,436 527,441", "Lid R", fill=NONE,
       stroke=INK, strokeWidth=4.5, cap="round")
d.path("M501,451 C509,455 519,455 525,450", "Eye R", fill=NONE,
       stroke=INK, strokeWidth=3, opacity=85, cap="round")
# nose
d.path("M482,456 C479,470 475,484 472,492 C477,498 486,498 490,493",
       "Nose", fill=NONE, stroke="#4A2C14", strokeWidth=3.5,
       opacity=80, cap="round")
# thin moustache + open jaw set
d.path("M458,500 C472,496 490,496 502,499", "Moustache", fill=NONE,
       stroke="#1E120A", strokeWidth=4, opacity=80, cap="round")
d.path("M460,512 C472,517 490,517 502,512", "Mouth", fill=NONE,
       stroke="#4A2018", strokeWidth=4.5, opacity=90, cap="round")
d.path("M466,518 C474,524 488,525 496,520", "Lower lip", fill=NONE,
       stroke="#6E4424", strokeWidth=2.5, opacity=50, cap="round")

# --- the flipped Strat — neck HIGH to frame-left, body low right -----------------------
# strap from the viewer's-left shoulder down to the body
d.path("M420,600 C470,650 530,684 596,702", "Strap", fill=NONE,
       stroke="#2A1C10", strokeWidth=8, opacity=80, cap="round")
# neck + fretboard climbing up-left at ~48°
d.path("M568,646 L392,470 L376,486 L552,662 Z", "Fretboard",
       fill=lin(560, 640, 390, 480, (0, "#3A2A1A"), (1, "#1C140C")),
       stroke=INK, strokeWidth=3)
# two string lines on the board
d.path("M560,648 L388,472 M566,640 L396,466", "Strings", fill=NONE,
       stroke="#C8B890", strokeWidth=3, opacity=60, cap="round")
# fret ticks
for i in range(5):
    t = i / 4
    fx = 548 + (392 - 548) * t
    fy3 = 638 + (474 - 638) * t
    d.path(f"M{fx - 4:.0f},{fy3 + 4:.0f} l9,-7", f"Fret {i+1}", fill=NONE,
           stroke="#8A7452", strokeWidth=2.5, opacity=70, cap="round")
# long headstock — the flipped Strat's crowning wedge
d.path(smooth([(376, 486), (346, 454), (324, 438), (306, 442),
               (302, 458), (316, 476), (340, 492), (358, 500)]),
       "Headstock", fill=lin(306, 440, 376, 500, (0, "#EDE8DC"), (1, "#8A8070")),
       stroke=INK, strokeWidth=3.5)
for i, (px, py) in enumerate([(322, 452), (336, 466), (350, 478)]):
    d.shape("ellipse", f"Peg {i+1}", x=px - 3.5, y=py - 3.5, width=7, height=7,
            fill="#D8CCB4", stroke=INK, strokeWidth=2)
# Strat-style offset body — two horns up-left, big lower bout to the right
d.path(smooth([(556, 640), (538, 614), (546, 590), (572, 584),
               (588, 600), (604, 592), (628, 596), (644, 618),
               (688, 640), (710, 680), (700, 722), (670, 750),
               (630, 762), (592, 752), (566, 724), (552, 688)]),
       "Guitar body", fill=GTR_GRAD, stroke=INK, strokeWidth=5)
# body edge shade
d.path(smooth([(648, 630), (680, 650), (694, 686), (688, 720),
               (664, 744), (632, 754), (644, 730), (654, 696),
               (652, 664)]),
       "Body shade", fill="#7E7464", opacity=40, stroke=NONE)
# pickups — three bars across the body's string axis, no pickguard blob
for i in range(3):
    px, py = 566 + i * 16, 638 + i * 13
    d.path(f"M{px},{py} L{px + 15},{py - 19}", f"Pickup {i+1}", fill=NONE,
           stroke="#4A443C", strokeWidth=6, cap="round")
# bridge block low on the body
d.path("M620,706 L668,720 L664,734 L616,720 Z", "Bridge",
       fill="#4A443C", stroke=INK, strokeWidth=2.5)

# fret hand high on the neck (his right, viewer's left)
d.path(smooth([(358, 486), (372, 472), (392, 466), (406, 474),
               (408, 490), (398, 504), (380, 508), (364, 500)]),
       "Fret hand", fill=SKIN_GRAD, stroke=INK, strokeWidth=3.5)
for i in range(3):
    d.path(f"M{368 + i * 3},{480 + i * 7} C{378 + i * 3},{474 + i * 7} {390 + i * 3},{474 + i * 7} {398 + i * 3},{480 + i * 7}",
           f"Fret finger {i+1}", fill=NONE, stroke="#3E2410",
           strokeWidth=3, opacity=70, cap="round")
# strum hand over the bridge end of the guard (his left, viewer's right)
d.path(smooth([(632, 700), (650, 692), (670, 696), (680, 710),
               (676, 726), (660, 734), (644, 730), (632, 718)]),
       "Strum hand", fill=SKIN_GRAD, stroke=INK, strokeWidth=3.5)
for i in range(3):
    d.path(f"M{640 + i * 4},{710 + i * 5} C{650 + i * 3},{706 + i * 5} {660 + i * 3},{708 + i * 5} {666 + i * 3},{714 + i * 5}",
           f"Strum finger {i+1}", fill=NONE, stroke="#3E2410",
           strokeWidth=3, opacity=70, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#3A2418", strokeWidth=6)

# --- captions -------------------------------------------------------------------
d.text("JIMI HENDRIX", "Name", x=500, y=934, size=56, font="Virelai Sans",
       color="#F4E4CE", justify="center")
LINE2, YEAR, SZ2, TRK = "WOODSTOCK · 1969", "1969", 22, 280
r = d.text(LINE2, "Milestone", x=500, y=970, size=22, font="Virelai Sans",
           color="#D8B894", justify="center")
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

d.finish("jimi-hendrix-V1R00")
