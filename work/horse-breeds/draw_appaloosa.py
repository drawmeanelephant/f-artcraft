#!/usr/bin/env python3
"""Appaloosa — milestone card V1R00. The blanket pattern doing the breed
work: dark bay body, a big white blanket draped over loin and rump,
scattered with individually placed dark spots — never a texture fill.
Mottled skin shows on the muzzle; thin striped hooves where the feet
read. Nez Perce country: rolling wheat-hill dusk behind, a spur of
bunchgrass on the floor. 1000x1000. House style: gradients +
translucent shading, never flat fills. Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Appaloosa — Milestone Card", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#221A14"                    # warm dark ink, never pure black
SPOT = "#241810"                   # spot dark — warm, never pure


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


def spot(cx, cy, w, h):
    """One hand-placed spot — a slightly irregular blob, never a stamp."""
    pts = [(cx - w / 2, cy + h * 0.08), (cx - w * 0.22, cy - h * 0.42),
           (cx + w * 0.28, cy - h / 2), (cx + w / 2, cy - h * 0.06),
           (cx + w * 0.24, cy + h * 0.46), (cx - w * 0.3, cy + h / 2)]
    return smooth(pts)


BG_GRAD = lin(0, 0, 0, 1000, (0, "#181510"), (1, "#090705"))
PLATE_GRAD = rad((0, "#C4B280"), (0.55, "#8E8054"), (1, "#463E2A"))
COAT_GRAD = lin(340, 380, 720, 800, (0, "#6E4A30"), (0.5, "#462E1C"), (1, "#201510"))
DIM_GRAD = lin(340, 380, 720, 800, (0, "#482F1C"), (1, "#180F0A"))
WHITE_GRAD = lin(560, 540, 700, 690, (0, "#F4EDDC"), (1, "#D9CBAE"))
HAIR_GRAD = lin(660, 540, 740, 700, (0, "#2A1C14"), (1, "#120B08"))
FLOOR_GRAD = lin(0, 730, 0, 880, (0, "#6E6440"), (0.55, "#4B4428"), (1, "#242012"))

# --- backdrop + Palouse dusk plate -------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#36301E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#EDE4BE", strokeWidth=3, opacity=38)

# rolling-hill contours high on the disc — the Palouse horizon
d.path("M140,300 C260,284 380,292 500,284 C620,276 740,288 856,282",
       "Hill line 1", fill=NONE, stroke="#5E5536", strokeWidth=4,
       opacity=30, cap="round")
d.path("M180,330 C300,318 420,326 540,318 C660,310 760,320 830,316",
       "Hill line 2", fill=NONE, stroke="#6E6242", strokeWidth=3.5,
       opacity=25, cap="round")
# thin light pooling upper-left
d.shape("ellipse", "Light pool", x=245, y=150, width=400, height=230,
        fill="#F0E4BC", opacity=12, stroke=NONE)
# dust lenses
for i, (x, y, w) in enumerate([(320, 370, 90), (565, 245, 70), (715, 395, 80),
                               (250, 490, 60), (755, 500, 64), (455, 200, 55)]):
    assert on_disc(x, y, 20), i
    d.shape("ellipse", f"Dust {i+1}", x=x - w / 2, y=y - w / 5, width=w, height=w * 0.4,
            fill="#EADCB0", opacity=10, stroke=NONE)

# --- bunchgrass floor, closing on the disc arc --------------------------------------
fy = 780
fl, fr = rim_x(fy, -1), rim_x(fy, 1)
d.path(f"M{fl:.1f},{fy} C300,768 400,790 500,780 C600,770 700,776 {fr:.1f},{fy} "
       f"A{PR},{PR} 0 0 1 {fl:.1f},{fy} Z", "Floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{fl + 8:.0f},{fy} C300,768 400,790 500,780 C600,770 700,776 {fr - 8:.0f},{fy}",
       "Floor crest", fill=NONE, stroke="#B8A468", strokeWidth=5, opacity=40, cap="round")
d.path("M330,820 C430,808 560,806 680,814", "Sod line", fill=NONE,
       stroke="#3E3620", strokeWidth=4, opacity=45, cap="round")
# bunchgrass tufts on the crest
for i, (x, y) in enumerate([(338, 800), (422, 828), (548, 836), (640, 820), (694, 798)]):
    assert on_disc(x, y + 8, 14), i
    for j, (dx, dy) in enumerate([(-13, 9), (-6, -5), (2, -11), (11, -2), (16, 8)]):
        d.path(f"M{x + dx * 0.4:.0f},{y + 13} L{x + dx:.0f},{y + dy:.0f}",
               f"Tuft {i+1}.{j+1}", fill=NONE, stroke="#8E7C4E",
               strokeWidth=3.5, opacity=65, cap="round")

# soft shadow under the horse
d.shape("ellipse", "Horse shadow", x=295, y=764, width=420, height=30,
        fill="#151106", opacity=33, stroke=NONE)

# --- the appaloosa, standing alert facing left ---------------------------------------
# tail — sparse, natural, hanging just clear of the rump edge
d.path(smooth([(700, 552), (722, 578), (730, 618), (726, 654), (714, 684),
               (702, 692), (692, 678), (690, 640), (690, 600), (688, 572)]),
       "Tail", fill=HAIR_GRAD, stroke=INK, strokeWidth=5)
for i, dd in enumerate(["M706,570 C714,604 716,640 712,670",
                        "M700,566 C706,598 708,634 704,664"]):
    d.path(dd, f"Tail strand {i+1}", fill=NONE, stroke="#5E4028",
           strokeWidth=3.5, opacity=50, cap="round")

# legs before the body — tops hide under the silhouette
d.path(smooth([(430, 652), (434, 700), (431, 740), (426, 768), (431, 786),
               (422, 793), (410, 788), (408, 752), (410, 710), (416, 664)]),
       "Front leg far", fill=DIM_GRAD, stroke=INK, strokeWidth=4.5)
d.path(smooth([(458, 652), (464, 698), (461, 738), (458, 764), (465, 786),
               (456, 795), (444, 789), (442, 750), (444, 708), (442, 664)]),
       "Front leg near", fill=COAT_GRAD, stroke=INK, strokeWidth=5)
d.path(smooth([(604, 648), (628, 670), (634, 706), (624, 740), (612, 768),
               (616, 784), (601, 788), (589, 776), (587, 742), (595, 706),
               (590, 666)]),
       "Hind leg far", fill=DIM_GRAD, stroke=INK, strokeWidth=4.5)
d.path(smooth([(642, 642), (670, 666), (680, 702), (668, 738), (656, 772),
               (662, 788), (646, 793), (630, 782), (628, 744), (634, 706),
               (626, 664)]),
       "Hind leg near", fill=COAT_GRAD, stroke=INK, strokeWidth=5)

# one silhouette: plain straight profile -> poll -> crest -> high withers
# -> level back -> round quarter -> deep girth -> chest -> throatlatch -> muzzle
d.path(smooth([(288, 466), (300, 452), (314, 438), (332, 418), (350, 404),
               (368, 392), (390, 400), (424, 438), (462, 494), (488, 540),
               (570, 550), (668, 558), (700, 588), (706, 632), (684, 662),
               (650, 680), (558, 690), (478, 684), (428, 662), (409, 626),
               (408, 600), (394, 552), (378, 505), (368, 498), (338, 498),
               (312, 490), (294, 480)]),
       "Horse", fill=COAT_GRAD, stroke=INK, strokeWidth=6)

# the blanket — a white sheet draped over loin and rump, ragged-edged
d.path(smooth([(576, 552), (622, 548), (668, 556), (698, 584), (708, 624),
               (692, 656), (656, 676), (616, 672), (586, 646), (572, 600)]),
       "Blanket", fill=WHITE_GRAD, opacity=92, stroke=NONE)

# --- the spots — individually placed inside the blanket, varied, asymmetric ---------
for i, (cx, cy, w, h) in enumerate([
        (600, 570, 26, 22), (642, 562, 30, 24), (676, 574, 20, 17),
        (608, 606, 22, 18), (646, 604, 34, 28), (686, 610, 18, 15),
        (592, 640, 16, 14), (626, 644, 26, 20), (662, 640, 20, 16),
        (686, 640, 14, 12), (566, 576, 14, 12), (704, 612, 12, 10),
        (566, 612, 13, 11)]):
    d.path(spot(cx, cy, w, h), f"Spot {i+1}", fill=SPOT, stroke=NONE, opacity=92)
# a few strays creeping forward of the blanket edge onto the flank
for i, (cx, cy, w, h) in enumerate([(548, 620, 12, 10), (532, 586, 10, 9),
                                    (556, 664, 11, 9)]):
    d.path(spot(cx, cy, w, h), f"Stray spot {i+1}", fill=SPOT, stroke=NONE, opacity=80)

# hooves — dark caps with two pale stripes each
for i, (cx, cy) in enumerate([(455, 790), (414, 788), (648, 790), (604, 786)]):
    d.path(f"M{cx - 13},{cy - 9} C{cx - 6},{cy - 13} {cx + 7},{cy - 13} {cx + 13},{cy - 7} "
           f"C{cx + 11},{cy + 4} {cx - 9},{cy + 6} {cx - 13},{cy - 1} Z",
           f"Hoof {i+1}", fill="#150D09", stroke=INK, strokeWidth=3)
    for j, dx in enumerate([-5, 4]):
        d.path(f"M{cx + dx},{cy - 10} L{cx + dx - 1},{cy + 3}",
               f"Hoof stripe {i+1}.{j+1}", fill=NONE, stroke="#8A7A60",
               strokeWidth=3, opacity=75, cap="round")

# shading kept at the silhouette edges
d.path("M470,552 C540,546 614,550 672,566 C612,554 542,552 470,552 Z",
       "Topline sheen", fill="#C09A66", opacity=38, stroke=NONE)
d.path("M500,682 C550,690 604,688 642,678 C606,694 552,696 504,690 Z",
       "Barrel shade", fill="#1E1410", opacity=25, stroke=NONE)
d.path("M382,404 C414,426 448,472 474,520", "Crest sheen", fill=NONE,
       stroke="#B08A5E", strokeWidth=4, opacity=40, cap="round")
d.path("M376,502 C388,488 396,468 395,446 C400,472 394,496 382,510 Z",
       "Throatlatch", fill="#1E1410", opacity=35, stroke=NONE)

# mane — thin, sparse (the breed runs sparse), short band on the crest
d.path(smooth([(372, 390), (402, 402), (438, 444), (470, 498), (490, 538),
               (498, 552), (484, 544), (456, 500), (422, 452), (394, 412),
               (372, 398)]),
       "Mane", fill=HAIR_GRAD, stroke=INK, strokeWidth=4)

# ears — alert, tips slightly in
d.path("M358,394 L368,346 L388,386 Z", "Ear near", fill=COAT_GRAD,
       stroke=INK, strokeWidth=4)
d.path("M382,386 L398,352 L400,382 Z", "Ear far", fill=DIM_GRAD,
       stroke=INK, strokeWidth=3.5)
d.path("M366,386 L370,358", "Ear inner", fill=NONE, stroke="#0F0A08",
       strokeWidth=3, opacity=55, cap="round")

# forelock wisp
d.path("M370,390 C361,396 355,407 353,419 C362,411 371,402 379,398 Z",
       "Forelock", fill=HAIR_GRAD, stroke=NONE)
d.shape("ellipse", "Forehead sheen", x=340, y=398, width=26, height=18,
        fill="#B08A5E", opacity=32, stroke=NONE)

# eye — the breed's white sclera shows: a wide pale ring around the pupil
d.shape("ellipse", "Sclera", x=336, y=434, width=30, height=24,
        fill="#E8E0CC", opacity=90, stroke=NONE)
d.path("M336,442 C344,434 358,434 364,442 C362,454 348,458 340,452 "
       "C335,448 334,446 336,442 Z", "Eye",
       fill=rad((0, "#6E4A24"), (0.7, "#422A12"), (1, "#1E1208")),
       stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Pupil", x=344, y=440, width=9, height=10, fill="#0E0806", stroke=NONE)
d.shape("ellipse", "Glint", x=346, y=441, width=4.5, height=4.5, fill="#FFF4D8", opacity=90, stroke=NONE)
d.path("M332,428 C346,422 360,422 370,428", "Brow", fill=NONE,
       stroke="#241812", strokeWidth=4, opacity=55, cap="round")

# mottled muzzle — soft pink-grey marbling around nostril and lips
d.path("M286,464 C294,458 306,458 312,464 C312,476 304,484 294,484 "
       "C286,480 282,472 286,464 Z", "Mottled skin", fill="#B89A8A",
       opacity=55, stroke=NONE)
for i, (cx, cy, w) in enumerate([(292, 470, 5), (300, 476, 4), (306, 468, 4),
                                 (296, 480, 3)]):
    d.shape("ellipse", f"Mottle {i+1}", x=cx, y=cy, width=w, height=w * 0.8,
            fill="#7E5E4E", opacity=60, stroke=NONE)
d.path("M292,462 C286,467 286,476 293,479 C301,481 306,475 304,468 "
       "C301,461 295,459 292,462 Z", "Nostril", fill="#120B07",
       stroke=INK, strokeWidth=3)
d.path("M300,486 C310,490 322,492 334,491", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=3, opacity=75, cap="round")
d.path("M344,472 C358,476 372,474 382,466", "Cheek line", fill=NONE,
       stroke="#241812", strokeWidth=3, opacity=40, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#332C1C", strokeWidth=6)

# --- captions -------------------------------------------------------------------
d.text("APPALOOSA", "Name", x=500, y=934, size=56, font="Virelai Sans",
       color="#EDE4BC", justify="center")
LINE2, SZ2, TRK = "SPOTTED · PALOUSE COUNTRY", 22, 280
r = d.text(LINE2, "Milestone", x=500, y=970, size=SZ2, font="Virelai Sans",
           color="#CCBD9C", justify="center")
d.cmd("text.setStyle", "Milestone tracking", id=r["id"], tracking=TRK)

b = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("milestone bounds", {k: round(v) for k, v in b.items()})
nearest = (min(max(PCX, b["x"]), b["x"] + b["width"]),
           min(max(PCY, b["y"]), b["y"] + b["height"]))
clear = math.hypot(nearest[0] - PCX, nearest[1] - PCY) - (PR + 3)
print("clears rim by %.1f" % clear)
assert clear > 0 and b["width"] <= 760 and b["x"] >= 10 and b["x"] + b["width"] <= 990, b

d.finish("appaloosa-V1R00")
