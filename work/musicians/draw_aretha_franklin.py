#!/usr/bin/env python3
"""Aretha Franklin — milestone card V1R00. Raised at the mic: chin lifted,
mouth open mid-note, bouffant, ivory gown under a fur stole — gospel
fervour with poise, no caricature. Dusty rose-plum plate, warm spot.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Aretha Franklin — Milestone Card", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#1C1418"                    # warm dark ink, never pure black


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


BG_GRAD = lin(0, 0, 0, 1000, (0, "#1A1016"), (1, "#090508"))
PLATE_GRAD = rad((0, "#A67E8E"), (0.5, "#6E4A5E"), (1, "#33202E"))
GOWN_GRAD = lin(350, 600, 660, 800, (0, "#6E3247"), (0.55, "#46202F"), (1, "#22101A"))
GOWN_DIM = lin(350, 600, 660, 800, (0, "#4A2434"), (1, "#1A0C13"))
SKIN_GRAD = rad((0, "#A6704A"), (0.6, "#7E5030"), (1, "#523019"))
HAIR_GRAD = lin(420, 320, 560, 520, (0, "#382820"), (0.6, "#1C1310"), (1, "#0C0806"))
FLOOR_GRAD = lin(0, 745, 0, 880, (0, "#5A4452"), (0.55, "#3C2E3A"), (1, "#1A1219"))
STOLE_GRAD = rad((0, "#F4EDE0"), (0.6, "#D8CBB4"), (1, "#A89A80"))

# --- backdrop + rose-plum plate -----------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#3E2A3A", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#EADCE4", strokeWidth=3, opacity=38)

# warm stage spot high left, bounded in the disc
spot = [(392, 70), (556, 70), (700, 748), (492, 748)]
for cx, cy in spot: assert on_disc(cx, cy, 8), (cx, cy)
d.path("M%.0f,%.0f L%.0f,%.0f L%.0f,%.0f L%.0f,%.0f Z" % tuple(sum(spot, ())),
       "Spot shaft",
       fill={"gradient": {"kind": "linear", "start": [452, 64], "end": [600, 760],
             "stops": [{"offset": 0, "color": "#F8ECE0", "opacity": 0.26},
                       {"offset": 0.7, "color": "#F8ECE0", "opacity": 0.09},
                       {"offset": 1, "color": "#F8ECE0", "opacity": 0}]}},
       stroke=NONE)
d.shape("ellipse", "Light pool", x=266, y=140, width=430, height=250,
        fill="#F2E4DC", opacity=13, stroke=NONE)
for i, (x, y, w) in enumerate([(356, 316, 90), (598, 238, 70), (724, 348, 80),
                               (264, 468, 60), (746, 494, 64), (478, 192, 55)]):
    assert on_disc(x, y, 20), i
    d.shape("ellipse", f"Haze {i+1}", x=x - w / 2, y=y - w / 5, width=w, height=w * 0.4,
            fill="#E8D8DE", opacity=9, stroke=NONE)

# --- stage floor, closing on the disc arc --------------------------------------------
fy = 790
fl, fr = rim_x(fy, -1), rim_x(fy, 1)
d.path(f"M{fl:.1f},{fy} C330,776 420,798 500,789 C580,780 670,786 {fr:.1f},{fy} "
       f"A{PR},{PR} 0 0 1 {fl:.1f},{fy} Z", "Floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{fl + 8:.0f},{fy} C330,776 420,798 500,789 C580,780 670,786 {fr - 8:.0f},{fy}",
       "Floor sheen", fill=NONE, stroke="#96798A", strokeWidth=5, opacity=36, cap="round")

# soft shadow under the figure
d.shape("ellipse", "Figure shadow", x=330, y=758, width=380, height=30,
        fill="#0C080C", opacity=34, stroke=NONE)

# --- Aretha: head & shoulders, chin lifted to the mic ---------------------------------
# gown — ivory 60s sheath widening to the floor
d.path(smooth([(354, 636), (328, 686), (338, 744), (354, 790),
               (658, 790), (666, 724), (652, 662), (616, 624),
               (564, 594), (468, 590), (408, 604)]),
       "Gown", fill=GOWN_GRAD, stroke=INK, strokeWidth=6)
# right-side shade so the gown turns
d.path(smooth([(566, 596), (616, 626), (650, 670), (660, 732),
               (652, 788), (566, 790), (560, 712), (552, 642)]),
       "Gown shade", fill=GOWN_DIM, opacity=55, stroke=NONE)
# neckline — a clean boat neck under the stole
d.path("M436,600 C470,622 520,622 552,600", "Neckline", fill=NONE,
       stroke="#C8B89E", strokeWidth=4, opacity=60, cap="round")

# fur stole — a scalloped band across the shoulders, cream on ivory
stole = [(352, 648), (330, 620), (346, 588), (384, 570), (424, 560),
         (470, 556), (520, 556), (566, 564), (612, 578), (646, 600),
         (660, 632), (652, 664), (618, 682), (572, 690), (520, 694),
         (466, 694), (416, 688), (376, 672)]
d.path(smooth(stole), "Fur stole", fill=STOLE_GRAD, stroke=INK, strokeWidth=5)
# scallop tufts along the stole's lower edge
for i, (tx, ty) in enumerate([(366, 664), (412, 684), (466, 694), (522, 694),
                              (578, 688), (630, 668)]):
    d.path(f"M{tx - 14},{ty - 8} C{tx - 4},{ty + 8} {tx + 10},{ty + 8} {tx + 18},{ty - 6}",
           f"Tuft {i+1}", fill=NONE, stroke="#8A7C66", strokeWidth=3,
           opacity=55, cap="round")
# stole's top edge catching the spot
d.path("M352,622 C400,584 470,570 540,572 C590,574 630,592 652,620",
       "Stole light", fill=NONE, stroke="#FBF6EC", strokeWidth=4,
       opacity=70, cap="round")

# neck — lifted, showing under the lifted chin
d.path("M460,528 C460,542 458,554 452,566 C466,578 492,578 506,566 "
       "C500,552 498,540 498,524 Z", "Neck", fill=lin(458, 524, 502, 578,
       (0, "#96683C"), (1, "#6E4524")), stroke=INK, strokeWidth=3.5)

# head — chin up toward the mic, three-quarter facing right
d.path(smooth([(426, 408), (422, 448), (428, 488), (446, 518),
               (472, 534), (498, 530), (518, 512), (530, 482),
               (532, 444), (524, 406), (504, 380), (478, 372),
               (452, 378)]),
       "Head", fill=SKIN_GRAD, stroke=INK, strokeWidth=5)
d.path("M428,462 C431,490 446,514 468,526 C446,518 430,494 427,470 Z",
       "Cheek shade", fill="#5C3418", opacity=40, stroke=NONE)
# under-chin light — head lifted into the spot
d.path("M452,524 C468,534 494,534 510,522", "Chin light", fill=NONE,
       stroke="#C89468", strokeWidth=3.5, opacity=55, cap="round")

# ears — pearl drop earrings
d.path("M424,446 C416,450 414,462 420,472 C426,476 432,472 434,462 "
       "C434,452 430,444 424,446 Z", "Ear L", fill="#6E4524",
       stroke=INK, strokeWidth=3)
d.shape("ellipse", "Earring", x=418, y=472, width=11, height=14,
        fill=rad((0, "#FBF6EA"), (1, "#BCAE94")), stroke=INK, strokeWidth=2)

# bouffant — a rounded dome rising off the crown, curled under at the nape
d.path(smooth([(418, 430), (406, 394), (412, 356), (442, 324),
               (482, 308), (524, 316), (552, 342), (564, 376),
               (564, 408), (554, 430), (542, 442), (534, 418),
               (522, 394), (498, 382), (470, 384), (446, 396),
               (428, 418)]),
       "Bouffant", fill=HAIR_GRAD, stroke=INK, strokeWidth=5)
# bouffant sheen — one smooth ridge over the dome
d.path("M432,378 C456,346 498,332 534,346", "Bouffant sheen", fill=NONE,
       stroke="#5A4034", strokeWidth=5, opacity=60, cap="round")
d.path("M428,400 C448,372 488,358 526,368", "Bouffant sheen 2", fill=NONE,
       stroke="#4A342A", strokeWidth=3.5, opacity=45, cap="round")
# curled-under ends at the nape and cheek
d.path("M416,420 C404,434 402,454 412,470 C420,476 430,472 432,462 "
       "C426,448 422,434 424,420 Z", "Nape curl", fill=HAIR_GRAD,
       stroke=INK, strokeWidth=3)
d.path("M548,414 C560,426 564,446 556,462 C549,468 540,465 538,456 "
       "C546,442 549,428 546,414 Z", "Side curl", fill=HAIR_GRAD,
       stroke=INK, strokeWidth=3)

# face — gaze lifted toward the mic, mouth open mid-note
# brows raised — fervour is in the forehead
d.path("M438,428 C450,420 466,418 478,423", "Brow L", fill=NONE,
       stroke="#2A1A12", strokeWidth=4.5, opacity=85, cap="round")
d.path("M496,423 C508,417 522,417 532,422", "Brow R", fill=NONE,
       stroke="#2A1A12", strokeWidth=4.5, opacity=85, cap="round")
# eyes open, gaze up — lids arcs, iris riding high under the upper lid
d.path("M440,446 C450,438 466,436 476,442", "Upper lid L", fill=NONE,
       stroke=INK, strokeWidth=4.5, cap="round")
d.path("M444,456 C452,460 464,460 472,454", "Lower lid L", fill=NONE,
       stroke=INK, strokeWidth=3, opacity=80, cap="round")
d.shape("ellipse", "Iris L", x=454, y=440, width=12, height=12,
        fill="#241108", stroke=NONE)
d.path("M496,442 C506,434 520,434 528,440", "Upper lid R", fill=NONE,
       stroke=INK, strokeWidth=4.5, cap="round")
d.path("M500,452 C508,456 518,456 525,450", "Lower lid R", fill=NONE,
       stroke=INK, strokeWidth=3, opacity=80, cap="round")
d.shape("ellipse", "Iris R", x=508, y=436, width=11, height=11,
        fill="#241108", stroke=NONE)
# nose — soft, tipped up a touch with the chin
d.path("M484,454 C481,468 477,482 474,490 C479,496 489,496 493,491",
       "Nose", fill=NONE, stroke="#5C341C", strokeWidth=3.5,
       opacity=80, cap="round")
# open mid-note mouth — dark interior, red lip rim, teeth glint on top
d.path(smooth([(458, 504), (474, 498), (496, 497), (514, 502),
               (518, 512), (508, 524), (490, 528), (472, 525),
               (460, 515)]),
       "Open mouth", fill=rad((0, "#40160F"), (1, "#1C0A06")),
       stroke="#6E2A20", strokeWidth=3.5)
d.path(smooth([(462, 505), (476, 500), (494, 499), (510, 502),
               (512, 507), (498, 509), (480, 510), (466, 508)]),
       "Teeth glint", fill="#F2E4D4", opacity=85, stroke=NONE)
d.path("M466,522 C476,530 492,531 504,526", "Lower lip", fill=NONE,
       stroke="#96522E", strokeWidth=3, opacity=60, cap="round")
# cheek warmth in the spot
d.shape("ellipse", "Blush L", x=434, y=482, width=22, height=12,
        fill="#B85C40", opacity=16, stroke=NONE)

# --- standing mic right of her face, tilted toward the lifted chin --------------------
# stand — slim pole from the floor
d.path("M668,556 L676,556 L674,790 L664,790 Z", "Mic stand",
       fill=lin(666, 556, 672, 790, (0, "#4E4452"), (1, "#1A141C")),
       stroke=INK, strokeWidth=2.5)
# tilted capsule — a round grill head leaning toward her mouth
d.path(rot_ellipse(646, 472, 30, 34, 30), "Mic capsule",
       fill=rad((0, "#8A8194"), (0.6, "#544C5C"), (1, "#26222C")),
       stroke=INK, strokeWidth=4)
for i in range(5):
    yy = 448 + i * 12
    wch = math.sqrt(max(0, 30 ** 2 - (yy - 472) ** 2)) * 0.8
    d.path(f"M{646 - wch:.0f},{yy} C{640:.0f},{yy - 4} {652:.0f},{yy - 4} {646 + wch:.0f},{yy}",
           f"Mic rib {i+1}", fill=NONE, stroke="#B8AEC2", strokeWidth=2.5,
           opacity=70, cap="round")
# capsule rim light
d.path("M626,456 C632,446 644,440 656,442", "Mic light", fill=NONE,
       stroke="#F4E8F0", strokeWidth=3.5, opacity=70, cap="round")
# tilted stem joining capsule to stand
d.path("M656,502 C662,518 666,536 668,556", "Mic stem", fill=NONE,
       stroke="#4E4452", strokeWidth=6, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#38242F", strokeWidth=6)

# --- captions -------------------------------------------------------------------
d.text("ARETHA FRANKLIN", "Name", x=500, y=934, size=56, font="Virelai Sans",
       color="#F2E4EA", justify="center")
LINE2, YEAR, SZ2, TRK = "RESPECT · 1967", "1967", 22, 280
r = d.text(LINE2, "Milestone", x=500, y=970, size=22, font="Virelai Sans",
           color="#C4AEBE", justify="center")
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

d.finish("aretha-franklin-V1R00")
