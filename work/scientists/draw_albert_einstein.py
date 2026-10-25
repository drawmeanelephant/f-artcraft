#!/usr/bin/env python3
"""Albert Einstein — milestone card V1R00. The icon: wild white hair as a
spiky halo wider than the skull, droopy warm eyes, white mustache, a hint
of kindly mischief. Chalk-fine equations ghost into the chalkboard-dark
plate behind the bust. Tweed jacket, open collar; the bust closes on the
disc's own lower arc. 1000x1000. House style: gradients + translucent
shading, never flat fills. Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Albert Einstein — Milestone Card", 1000, 1000)

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


BG_GRAD = lin(0, 0, 0, 1000, (0, "#121716"), (1, "#060908"))
PLATE_GRAD = rad((0, "#6E7D70"), (0.5, "#44524A"), (1, "#1E2825"))
SKIN_GRAD = lin(430, 340, 510, 550, (0, "#E0C2A0"), (0.55, "#C09C7E"), (1, "#8E6C52"))
SKIN_DIM = lin(430, 340, 510, 550, (0, "#BE9E80"), (1, "#7C5C46"))
HAIR_GRAD = lin(360, 220, 580, 520, (0, "#F2EFE6"), (0.5, "#C9C5B5"), (1, "#8C8878"))
MUST_GRAD = lin(440, 470, 505, 510, (0, "#DDD9C9"), (1, "#9B9684"))
TWEED_GRAD = lin(300, 560, 700, 840, (0, "#574B3E"), (0.5, "#2E251C"), (1, "#130E09"))
CHALK = "#DCE6DC"

# --- backdrop + chalkboard plate ------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#2C3630", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8E4DA", strokeWidth=3, opacity=34)

# thin light pooling upper-left
d.shape("ellipse", "Light pool", x=250, y=150, width=380, height=220,
        fill="#E0EADD", opacity=11, stroke=NONE)

# --- chalk equations ghosting in the dark — faint, never competing ----------------
r = d.text("E = mc²", "Chalk eq", x=295, y=240, size=24, font=SS3,
           color=CHALK, justify="center")
d.cmd("object.setProps", "Chalk eq fade", id=r["id"], opacity=15)
d.path("M252,258 C280,264 320,264 348,258", "Chalk underline", fill=NONE,
       stroke=CHALK, strokeWidth=3, opacity=14, cap="round")
# loose chalk dashes upper-right — a worked board implied, not written
for i, (x1, y1, x2, y2) in enumerate([(640, 220, 700, 218), (648, 244, 686, 240),
                                      (700, 248, 728, 244), (660, 272, 712, 268)]):
    assert on_disc(x1, y1, 12) and on_disc(x2, y2, 12), i
    d.path(f"M{x1},{y1} L{x2},{y2}", f"Chalk dash {i+1}", fill=NONE,
           stroke=CHALK, strokeWidth=3, opacity=12, cap="round")
# a faint chalk light-cone: two crossed strokes
d.path("M655,300 L735,360 M735,300 L655,360", "Chalk cone", fill=NONE,
       stroke=CHALK, strokeWidth=3, opacity=10, cap="round")

# --- jacket bust — silhouette closes on the disc's own arc -----------------------
fj = 800
jl, jr = rim_x(fj, -1), rim_x(fj, 1)
d.path(f"M{jl:.1f},{fj} C285,730 300,662 350,612 C388,580 420,568 445,562 "
       f"L495,562 C540,570 585,582 622,614 C664,652 690,720 {jr:.1f},{fj} "
       f"A{PR},{PR} 0 0 1 {jl:.1f},{fj} Z", "Jacket",
       fill=TWEED_GRAD, stroke=INK, strokeWidth=5)

# shirt V at the open collar + collar wings
d.path("M446,560 L494,560 L470,634 Z", "Shirt V",
       fill=lin(446, 560, 470, 634, (0, "#C8BCA2"), (1, "#6E6250")),
       stroke=INK, strokeWidth=3.5)
d.path("M446,560 L420,584 L452,600 Z", "Collar L",
       fill="#3A3128", stroke=INK, strokeWidth=3)
d.path("M494,560 L520,584 L488,600 Z", "Collar R",
       fill="#3A3128", stroke=INK, strokeWidth=3)
# tweed weave hints + shoulder sheen
for i, dd in enumerate(["M380,640 C370,690 368,740 376,790",
                        "M560,640 C576,694 586,744 590,790",
                        "M470,660 C470,710 470,750 470,790"]):
    d.path(dd, f"Tweed fold {i+1}", fill=NONE, stroke="#141009",
           strokeWidth=4, opacity=40, cap="round")
d.path("M316,660 C350,620 396,592 440,578", "Shoulder sheen", fill=NONE,
       stroke="#7A6A56", strokeWidth=5, opacity=30, cap="round")

# neck
d.path("M440,512 L440,560 C452,570 486,570 498,560 L498,512 Z", "Neck",
       fill=SKIN_DIM, stroke=INK, strokeWidth=3.5)

# --- the hair halo — the signature ------------------------------------------------
# irregular spiky cloud, stretched wider than tall, tufts out/in — wild,
# not a starburst: uneven angles and radii
HX, HY = 469, 375
ring = [(148, 122), (160, 170), (172, 118), (191, 172), (204, 126),
        (220, 176), (237, 128), (253, 178), (268, 132), (284, 168),
        (299, 126), (315, 162), (329, 124), (343, 156), (357, 122),
        (14, 148), (30, 160), (43, 118)]
hpts = [(HX + r * 1.16 * math.cos(math.radians(a)),
         HY + r * 0.94 * math.sin(math.radians(a)))
        for a, r in ring]
for x, y in hpts:
    assert on_disc(x, y, 10), (round(x), round(y))
d.path(smooth(hpts, k=0.7), "Hair halo", fill=HAIR_GRAD, stroke=INK,
       strokeWidth=4.5)
# silver strand strokes following the tufts
for i, (a0, r0, a1, r1) in enumerate([(160, 120, 195, 158), (230, 125, 262, 165),
                                      (250, 130, 285, 160), (300, 128, 335, 152),
                                      (330, 125, 20, 145)]):
    p0 = (HX + r0 * math.cos(math.radians(a0)), HY + r0 * math.sin(math.radians(a0)))
    p1 = (HX + r1 * math.cos(math.radians(a1)), HY + r1 * math.sin(math.radians(a1)))
    mid = ((p0[0] + p1[0]) / 2 - 14, (p0[1] + p1[1]) / 2 - 14)
    d.path(f"M{p0[0]:.0f},{p0[1]:.0f} Q{mid[0]:.0f},{mid[1]:.0f} {p1[0]:.0f},{p1[1]:.0f}",
           f"Hair strand {i+1}", fill=NONE, stroke="#FBF8EC",
           strokeWidth=3.5, opacity=45, cap="round")

# --- face ------------------------------------------------------------------------
# jowly elder face — wider jaw than the curie rig
d.path(smooth([(469, 354), (522, 366), (528, 424), (514, 482), (494, 522),
               (469, 544), (444, 522), (424, 482), (410, 424), (416, 366)],
              k=0.85), "Face", fill=SKIN_GRAD, stroke=INK, strokeWidth=4)
# high hairline — the forehead shows under the halo
d.path("M414,396 C424,362 448,348 469,346 C492,348 516,364 525,398 "
       "C512,370 490,358 469,356 C448,358 426,370 414,396 Z",
       "Hairline", fill=HAIR_GRAD, stroke=NONE)
# sideburn wisps
d.path("M414,396 C410,414 410,432 414,448 L424,444 C420,428 420,412 422,398 Z",
       "Sideburn L", fill=HAIR_GRAD, stroke=NONE)
d.path("M525,398 C528,414 528,432 524,448 L515,444 C519,428 519,412 517,398 Z",
       "Sideburn R", fill=HAIR_GRAD, stroke=NONE)
# forehead wrinkles — two faint arcs
d.path("M432,392 C446,386 492,386 506,392", "Wrinkle 1", fill=NONE,
       stroke="#9A7658", strokeWidth=3, opacity=30, cap="round")
d.path("M438,404 C450,400 488,400 500,404", "Wrinkle 2", fill=NONE,
       stroke="#9A7658", strokeWidth=3, opacity=25, cap="round")

# bushy brows — the left a touch higher: the mischief
d.path("M425,408 C436,400 452,400 461,406", "Brow L", fill=NONE,
       stroke="#8C8878", strokeWidth=6, opacity=85, cap="round")
d.path("M479,408 C489,402 503,402 512,408", "Brow R", fill=NONE,
       stroke="#8C8878", strokeWidth=6, opacity=85, cap="round")
# heavy upper lids + eyes
d.path("M428,420 C436,413 452,413 460,420", "Lid L", fill=NONE,
       stroke="#7A5C44", strokeWidth=3.5, opacity=60, cap="round")
d.path("M480,420 C488,413 503,413 511,420", "Lid R", fill=NONE,
       stroke="#7A5C44", strokeWidth=3.5, opacity=60, cap="round")
d.path("M431,425 C437,418 452,418 459,425 C452,432 437,432 431,425 Z",
       "Eye L", fill="#EDE2CC", stroke=INK, strokeWidth=3)
d.path("M482,425 C489,418 504,418 511,425 C504,432 489,432 482,425 Z",
       "Eye R", fill="#EDE2CC", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Iris L", x=441, y=419, width=11, height=12,
        fill="#33241A", stroke=NONE)
d.shape("ellipse", "Iris R", x=493, y=419, width=11, height=12,
        fill="#33241A", stroke=NONE)
d.shape("ellipse", "Glint L", x=444, y=421, width=3.5, height=3.5,
        fill="#FFF4DC", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=496, y=421, width=3.5, height=3.5,
        fill="#FFF4DC", opacity=90, stroke=NONE)
# the bags
d.path("M433,438 C441,443 453,443 459,439", "Bag L", fill=NONE,
       stroke="#9A7658", strokeWidth=3, opacity=35, cap="round")
d.path("M484,439 C491,443 503,443 509,438", "Bag R", fill=NONE,
       stroke="#9A7658", strokeWidth=3, opacity=35, cap="round")
# broad nose
d.path("M474,428 C479,444 479,460 472,472", "Nose shade", fill=NONE,
       stroke="#9A7658", strokeWidth=4, opacity=45, cap="round")
d.path("M462,474 C468,478 478,478 484,473", "Nose base", fill=NONE,
       stroke="#8A6248", strokeWidth=3.5, opacity=55, cap="round")

# --- the mustache — droopy white mass over the upper lip ---------------------------
d.path(smooth([(436, 486), (448, 475), (462, 471), (469, 477), (476, 471),
               (490, 475), (503, 486), (505, 499), (495, 508), (478, 512),
               (460, 512), (443, 507), (434, 496)], k=0.9), "Mustache",
       fill=MUST_GRAD, stroke=INK, strokeWidth=3.5)
# a small warm smile peeking under it
d.path("M456,518 C464,522 476,522 484,518", "Mouth", fill=NONE,
       stroke="#7A4A3A", strokeWidth=4, opacity=70, cap="round")
# cheek shade
d.path("M420,448 C423,468 431,484 443,494", "Cheek shade", fill=NONE,
       stroke="#9A7658", strokeWidth=5, opacity=22, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#28322C", strokeWidth=6)

# --- captions -------------------------------------------------------------------
d.text("ALBERT EINSTEIN", "Name", x=500, y=934, size=56, font="Virelai Sans",
       color="#E6EDE2", justify="center")
LINE2, SZ2, TRK = "MIRACLE YEAR · 1905", 22, 520
r = d.text(LINE2, "Milestone", x=500, y=970, size=SZ2, font=SS3,
           color="#BCCABB", justify="center")
d.cmd("text.setStyle", "Milestone tracking", id=r["id"], tracking=TRK)

b = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("milestone bounds", {k: round(v) for k, v in b.items()})
nearest = (min(max(PCX, b["x"]), b["x"] + b["width"]),
           min(max(PCY, b["y"]), b["y"] + b["height"]))
clear = math.hypot(nearest[0] - PCX, nearest[1] - PCY) - (PR + 3)
print("clears rim by %.1f" % clear)
assert clear > 0 and b["width"] <= 760 and b["x"] >= 10 and b["x"] + b["width"] <= 990, b

d.finish("albert-einstein-V1R00")
