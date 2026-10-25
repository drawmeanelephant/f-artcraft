#!/usr/bin/env python3
"""Miles Davis — milestone card V1R00. Muted cool: trumpet held low at the
hip, bell to the floor, sharp dark suit, the face half in shadow — nothing
grins. Club floor closing on the disc's arc. 1000x1000. House style:
gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Miles Davis — Milestone Card", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#1A161A"                    # warm dark ink, never pure black


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


BG_GRAD = lin(0, 0, 0, 1000, (0, "#0E131C"), (1, "#05070B"))
PLATE_GRAD = rad((0, "#70809A"), (0.5, "#465470"), (1, "#202A3A"))
SUIT_GRAD = lin(350, 600, 660, 800, (0, "#2C3242"), (0.55, "#1A1E2A"), (1, "#0C0E14"))
SUIT_DIM = lin(350, 600, 660, 800, (0, "#1E2230"), (1, "#0A0C12"))
SKIN_GRAD = rad((0, "#9A6238"), (0.6, "#6E4424"), (1, "#422410"))
FLOOR_GRAD = lin(0, 745, 0, 880, (0, "#3E4656"), (0.55, "#2A3040"), (1, "#121620"))
BRASS_GRAD = lin(640, 640, 760, 780, (0, "#C0A058"), (0.55, "#96742E"), (1, "#54401A"))

# --- backdrop + cool steel plate -------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#28303E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C8D4E4", strokeWidth=3, opacity=38)

# one dim light pool upper-left — nothing sparkling
d.shape("ellipse", "Light pool", x=250, y=150, width=400, height=240,
        fill="#D8E0EC", opacity=11, stroke=NONE)
for i, (x, y, w) in enumerate([(340, 325, 90), (585, 245, 70), (720, 355, 80),
                               (262, 470, 60), (748, 495, 64), (470, 195, 55)]):
    assert on_disc(x, y, 20), i
    d.shape("ellipse", f"Haze {i+1}", x=x - w / 2, y=y - w / 5, width=w, height=w * 0.4,
            fill="#C4CEDC", opacity=9, stroke=NONE)

# --- club floor, closing on the disc arc ------------------------------------------------
fy = 790
fl, fr = rim_x(fy, -1), rim_x(fy, 1)
d.path(f"M{fl:.1f},{fy} C330,776 420,798 500,789 C580,780 670,786 {fr:.1f},{fy} "
       f"A{PR},{PR} 0 0 1 {fl:.1f},{fy} Z", "Floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{fl + 8:.0f},{fy} C330,776 420,798 500,789 C580,780 670,786 {fr - 8:.0f},{fy}",
       "Floor sheen", fill=NONE, stroke="#7E8CA0", strokeWidth=5, opacity=36, cap="round")
# a folded music stand silhouette at far left — the bandstand cue
d.path("M296,690 L352,682 L358,716 L302,724 Z", "Stand desk",
       fill="#14181F", stroke=INK, strokeWidth=3)
d.path("M326,722 L330,786", "Stand pole", fill=NONE, stroke="#14181F",
       strokeWidth=5, cap="round")
d.path("M310,788 C322,780 340,780 352,788", "Stand feet", fill=NONE,
       stroke="#14181F", strokeWidth=4, cap="round")

# soft shadow under the figure
d.shape("ellipse", "Figure shadow", x=340, y=758, width=380, height=30,
        fill="#080A0E", opacity=34, stroke=NONE)

# --- Miles Davis: half-figure, trumpet low, face half-shadowed --------------------------
# left sleeve (viewer's left) hanging relaxed to the side
d.path(smooth([(388, 650), (362, 690), (352, 734), (358, 772),
               (372, 784), (388, 778), (392, 740), (394, 700),
               (398, 668)]),
       "Sleeve L", fill=SUIT_GRAD, stroke=INK, strokeWidth=5)

# torso — sharp dark suit, narrow shoulders, widening to the floor
d.path(smooth([(352, 634), (328, 682), (338, 740), (354, 790),
               (656, 790), (664, 724), (650, 662), (614, 624),
               (564, 594), (470, 590), (410, 602)]),
       "Suit", fill=SUIT_GRAD, stroke=INK, strokeWidth=6)
# right-side shade so the torso turns — deeper on this card
d.path(smooth([(566, 596), (614, 626), (648, 668), (660, 732),
               (652, 788), (566, 790), (560, 712), (552, 642)]),
       "Suit shade", fill=SUIT_DIM, opacity=60, stroke=NONE)
# slim white shirt wedge + narrow tie
d.path(smooth([(456, 600), (480, 644), (494, 706), (498, 782),
               (528, 784), (530, 706), (522, 644), (506, 604),
               (482, 596)]),
       "Shirt front", fill=lin(474, 604, 524, 782, (0, "#DDE2E8"), (1, "#A8AEBA")),
       stroke=INK, strokeWidth=3.5)
d.path(smooth([(488, 610), (499, 616), (507, 610), (511, 646),
               (505, 706), (496, 744), (488, 706), (484, 646)]),
       "Tie", fill=lin(488, 610, 507, 744, (0, "#1C2028"), (1, "#0C0E14")),
       stroke=INK, strokeWidth=3)
# notch lapels — crisp 50s slim cut
d.path(smooth([(456, 598), (432, 634), (424, 696), (438, 762),
               (468, 782), (480, 762), (468, 702), (480, 650),
               (472, 618)]),
       "Lapel L", fill=lin(434, 604, 474, 782, (0, "#343C4E"), (1, "#181C26")),
       stroke=INK, strokeWidth=3.5)
d.path(smooth([(514, 600), (534, 636), (542, 702), (532, 772),
               (550, 782), (560, 724), (552, 660), (542, 620)]),
       "Lapel R", fill=lin(532, 604, 558, 782, (0, "#343C4E"), (1, "#181C26")),
       stroke=INK, strokeWidth=3.5)
# lapel light edge — one cold highlight
d.path("M434,632 C428,662 428,700 436,734", "Lapel light", fill=NONE,
       stroke="#5A6A84", strokeWidth=3, opacity=60, cap="round")
# breast-pocket handkerchief — a pale triangle
d.path("M404,692 L430,688 L426,706 L406,708 Z", "Pocket square",
       fill="#C9CFD8", stroke=INK, strokeWidth=2.5)

# neck
d.path("M460,538 C460,554 458,568 454,582 C466,592 490,592 502,580 "
       "C498,566 496,552 496,536 Z", "Neck", fill=lin(458, 538, 498, 592,
       (0, "#8A5A32"), (1, "#5E3A1E")), stroke=INK, strokeWidth=3.5)

# head — facing a touch left, jaw set, nothing soft
d.path(smooth([(426, 414), (422, 454), (428, 494), (446, 524),
               (470, 540), (496, 538), (518, 520), (530, 490),
               (532, 450), (524, 412), (504, 386), (478, 378),
               (450, 383)]),
       "Head", fill=SKIN_GRAD, stroke=INK, strokeWidth=5)

# the half-shadow — right half of the face drops into blue shade
d.path(smooth([(490, 382), (508, 388), (522, 412), (530, 446),
               (532, 484), (524, 514), (506, 532), (490, 538),
               (494, 500), (496, 460), (494, 420)]),
       "Face shadow", fill="#12161F", opacity=42, stroke=NONE)
# a matching shadow wedge on the suit's right shoulder
d.path(smooth([(560, 600), (612, 628), (646, 672), (656, 732),
               (648, 788), (586, 788), (580, 700), (570, 640)]),
       "Shoulder shadow", fill="#0A0C12", opacity=30, stroke=NONE)

# close-cropped hair — a very dark cap with a clean hairline
d.path(smooth([(424, 428), (418, 392), (430, 356), (460, 334),
               (494, 328), (522, 340), (540, 366), (546, 398),
               (542, 424), (534, 436), (526, 410), (508, 394),
               (482, 388), (456, 392), (436, 406), (428, 430)]),
       "Hair", fill=lin(428, 330, 544, 430, (0, "#241C16"), (1, "#0E0A08")),
       stroke=INK, strokeWidth=4)
d.path("M438,406 C460,390 486,386 512,394", "Hairline", fill=NONE,
       stroke="#0A0706", strokeWidth=3.5, opacity=70, cap="round")
# ears
d.path("M424,452 C416,456 414,468 420,478 C426,482 432,478 434,468 "
       "C434,458 430,450 424,452 Z", "Ear L", fill="#5E3A1E",
       stroke=INK, strokeWidth=3)

# face — half-lidded eyes, level mouth, the light on the left half only
# brows low and level
d.path("M438,442 C450,436 464,434 476,438", "Brow L", fill=NONE,
       stroke="#1C120C", strokeWidth=4.5, opacity=85, cap="round")
d.path("M496,438 C508,434 520,434 530,438", "Brow R", fill=NONE,
       stroke="#1C120C", strokeWidth=4.5, opacity=85, cap="round")
# half-lidded eyes — upper lid line hoods a smaller almond
d.path("M440,452 C450,446 464,446 472,452", "Lid L", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.path("M444,458 C452,463 464,463 470,458", "Eye L", fill=NONE,
       stroke=INK, strokeWidth=3, opacity=85, cap="round")
d.path("M496,450 C506,444 518,444 526,450", "Lid R", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.path("M500,456 C508,461 518,461 524,456", "Eye R", fill=NONE,
       stroke=INK, strokeWidth=3, opacity=85, cap="round")
# nose — a single sure stroke
d.path("M482,456 C479,471 475,485 472,493 C477,499 486,499 490,494",
       "Nose", fill=NONE, stroke="#3C2412", strokeWidth=3.5,
       opacity=80, cap="round")
# mouth — level, unimpressed
d.path("M458,512 C472,515 490,515 502,511", "Mouth", fill=NONE,
       stroke="#241410", strokeWidth=4.5, opacity=90, cap="round")
# moustache shadow hint above the lip — the 50s pencil moustache
d.path("M462,502 C474,500 490,500 500,502", "Moustache", fill=NONE,
       stroke="#241812", strokeWidth=2.5, opacity=45, cap="round")
# jaw shade under the chin
d.path("M456,530 C470,540 490,542 504,536", "Jaw shade", fill=NONE,
       stroke="#3C2412", strokeWidth=3, opacity=50, cap="round")

# --- trumpet held low in the right hand (viewer's right), bell to the floor ------------
# sleeve from the right shoulder down to the hip
d.path(smooth([(622, 640), (646, 676), (660, 716), (662, 752),
               (650, 772), (632, 768), (624, 736), (618, 700),
               (614, 666)]),
       "Sleeve R", fill=SUIT_GRAD, stroke=INK, strokeWidth=5)
d.path("M630,752 C642,744 656,744 666,752", "Cuff R", fill=NONE,
       stroke="#C9CFD8", strokeWidth=7, opacity=80, cap="round")
# hand gripping the horn loosely at hip height
d.path("M636,742 C650,736 664,742 666,754 C664,768 650,774 638,768 "
       "C630,760 629,750 636,742 Z", "Trumpet hand", fill=SKIN_GRAD,
       stroke=INK, strokeWidth=3.5)
# horn angled down-right: leadpipe from the grip to the bell mouth
d.path("M648,752 L726,690 L734,700 L656,762 Z", "Leadpipe",
       fill=BRASS_GRAD, stroke=INK, strokeWidth=3)
# valve block at the grip
d.path("M646,738 L704,692 L714,702 L656,748 Z", "Valve casing",
       fill=BRASS_GRAD, stroke=INK, strokeWidth=3)
for i, (vx, vy) in enumerate([(656, 716), (672, 702), (688, 688)]):
    d.shape("ellipse", f"Valve {i+1}", x=vx, y=vy, width=13, height=8,
            fill="#C0A058", stroke=INK, strokeWidth=2.5)
# bell flare down-right — mouth toward the floor corner
d.path(smooth([(726, 690), (748, 678), (772, 670), (790, 672),
               (784, 688), (768, 702), (744, 712), (728, 716)]),
       "Bell flare", fill=BRASS_GRAD, stroke=INK, strokeWidth=3.5)
d.path(rot_ellipse(788, 690, 22, 36, -38), "Bell mouth",
       fill=rad((0, "#503612"), (0.7, "#6E4C1E"), (1, "#B08A46")),
       stroke=INK, strokeWidth=3.5)
# dim sheen along the horn
d.path("M656,748 C688,724 716,704 740,684", "Horn sheen", fill=NONE,
       stroke="#E8D09A", strokeWidth=3, opacity=45, cap="round")
# mouthpiece nub at the grip
d.path("M640,752 L654,742 L658,750 L644,760 Z", "Mouthpiece",
       fill="#96742E", stroke=INK, strokeWidth=2.5)

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#222A38", strokeWidth=6)

# --- captions -------------------------------------------------------------------
d.text("MILES DAVIS", "Name", x=500, y=934, size=56, font="Virelai Sans",
       color="#DDE4EE", justify="center")
LINE2, YEAR, SZ2, TRK = "KIND OF BLUE · 1959", "1959", 22, 280
r = d.text(LINE2, "Milestone", x=500, y=970, size=SZ2, font="Virelai Sans",
           color="#A8B4C6", justify="center")
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

d.finish("miles-davis-V1R00")
