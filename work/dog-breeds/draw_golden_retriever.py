#!/usr/bin/env python3
"""Golden retriever — milestone card V1R00. Seated front-facing on a
Highland moor: broad feathered chest, drop ears with feathered edges,
the soft-mouthed gentle expression the breed lives on, feathered tail
curled around the hip onto the floor. Warm golds over a dark bronze
disc; heather tufts at the feet. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Golden Retriever — Milestone Card", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#2A1E12"                    # warm dark ink, never pure black


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


BG_GRAD = lin(0, 0, 0, 1000, (0, "#131009"), (1, "#080604"))
PLATE_GRAD = rad((0, "#8A7C56"), (0.5, "#5C5238"), (1, "#2E2A1C"))
GOLD_GRAD = lin(430, 320, 560, 780, (0, "#DCAC60"), (0.55, "#B0803E"), (1, "#7E5524"))
DIM_GOLD = lin(430, 320, 560, 780, (0, "#A87C40"), (1, "#5E3E1C"))
CREAM_GRAD = lin(470, 460, 540, 780, (0, "#F2DFB6"), (1, "#C8A468"))
FLOOR_GRAD = lin(0, 760, 0, 880, (0, "#5E4F30"), (0.55, "#413622"), (1, "#241C10"))

# --- backdrop + dark bronze plate ------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#3C341F", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E0D2A8", strokeWidth=3, opacity=36)

# warm dusk glow high in the disc behind the dog
d.shape("ellipse", "Light pool", x=330, y=150, width=380, height=240,
        fill="#F0DCA0", opacity=16, stroke=NONE)
# moor mist lenses
for i, (x, y, w) in enumerate([(290, 310, 80), (620, 240, 70), (720, 370, 75),
                               (240, 470, 60), (760, 490, 60), (460, 200, 55)]):
    assert on_disc(x, y, 20), i
    d.shape("ellipse", f"Mist {i+1}", x=x - w / 2, y=y - w / 5, width=w, height=w * 0.4,
            fill="#EBDDB4", opacity=11, stroke=NONE)

# --- moor floor, closing on the disc arc ------------------------------------------
fy = 800
fl, fr = rim_x(fy, -1), rim_x(fy, 1)
d.path(f"M{fl:.1f},{fy} C300,790 400,812 500,804 C600,796 700,800 {fr:.1f},{fy} "
       f"A{PR},{PR} 0 0 1 {fl:.1f},{fy} Z", "Floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{fl + 8:.0f},{fy} C300,790 400,812 500,804 C600,796 700,800 {fr - 8:.0f},{fy}",
       "Floor crest", fill=NONE, stroke="#A08E58", strokeWidth=5, opacity=42, cap="round")
# heather at the dog's feet — muted purple ticks + one bloom each
for i, (x, y) in enumerate([(345, 816), (410, 838), (590, 838), (658, 814)]):
    assert on_disc(x, y + 10, 14), i
    for j, (dx, dy) in enumerate([(-14, 10), (-6, -4), (2, -10), (10, -2), (16, 8)]):
        d.path(f"M{x + dx * 0.4:.0f},{y + 14} L{x + dx:.0f},{y + dy:.0f}",
               f"Heather {i+1}.{j+1}", fill=NONE, stroke="#6E5E70",
               strokeWidth=3.5, opacity=70, cap="round")
    d.shape("ellipse", f"Heather bloom {i+1}", x=x - 6, y=y - 6, width=10, height=8,
            fill="#8A7490", opacity=55, stroke=NONE)

# soft shadow under the seated dog
d.shape("ellipse", "Dog shadow", x=300, y=770, width=400, height=34,
        fill="#181006", opacity=32, stroke=NONE)

# --- the golden, seated front-facing ---------------------------------------------
# tail — feathered, curled around the right hip onto the floor
d.path(smooth([(640, 700), (692, 706), (726, 726), (734, 752), (716, 770),
               (680, 774), (648, 762), (632, 738), (630, 716)]),
       "Tail", fill=DIM_GOLD, stroke=INK, strokeWidth=5)
for i, dd in enumerate(["M648,730 C680,736 706,748 720,764",
                        "M642,746 C672,754 698,762 712,772",
                        "M654,714 C684,720 708,732 722,750"]):
    d.path(dd, f"Tail feather {i+1}", fill=NONE, stroke="#F0DCA8",
           strokeWidth=4, opacity=45, cap="round")

# hindquarters folded — hocks flat to the floor, paws poking out front
d.path(smooth([(340, 700), (330, 640), (352, 596), (392, 572), (420, 588),
               (424, 636), (412, 692), (398, 736), (370, 758), (346, 740)]),
       "Haunch L", fill=DIM_GOLD, stroke=INK, strokeWidth=5)
d.path(smooth([(660, 700), (670, 640), (648, 596), (608, 572), (580, 588),
               (576, 636), (588, 692), (602, 736), (630, 758), (654, 740)]),
       "Haunch R", fill=DIM_GOLD, stroke=INK, strokeWidth=5)
d.path("M336,736 C352,726 374,726 386,738 C382,752 362,760 346,754 "
       "C336,748 332,742 336,736 Z", "Hind paw L", fill=CREAM_GRAD,
       stroke=INK, strokeWidth=4)
d.path("M614,738 C628,726 650,726 662,736 C666,744 662,752 652,758 "
       "C636,762 616,754 612,744 Z", "Hind paw R", fill=CREAM_GRAD,
       stroke=INK, strokeWidth=4)

# body — the seated column: broad chest rising off the floor, back easing
# up into the shoulders
d.path(smooth([(400, 560), (378, 610), (368, 668), (368, 722), (390, 762),
               (430, 780), (500, 786), (570, 780), (610, 762), (632, 722),
               (632, 668), (622, 610), (600, 560), (560, 540), (500, 534),
               (440, 540)]),
       "Body", fill=GOLD_GRAD, stroke=INK, strokeWidth=6)
# the feathered chest — a cream bib over the breast, ending above the
# front legs so the forelegs still read as columns
d.path(smooth([(440, 560), (418, 600), (412, 650), (424, 700), (452, 730),
               (484, 744), (516, 744), (548, 730), (576, 700), (588, 650),
               (582, 600), (560, 560), (532, 546), (468, 546)]),
       "Chest feathering", fill=CREAM_GRAD, stroke=INK, strokeWidth=3)
# feather edge strokes down the bib
for i, dd in enumerate(["M430,610 C426,642 428,676 438,706",
                        "M458,600 C454,640 456,684 464,718",
                        "M500,596 C497,640 498,688 502,724",
                        "M542,600 C546,640 544,684 536,718",
                        "M570,610 C574,642 572,676 562,706"]):
    d.path(dd, f"Chest feather {i+1}", fill=NONE, stroke="#C89E5E",
           strokeWidth=3.5, opacity=55, cap="round")

# front legs — straight sound columns flanking the bib to the floor
d.path(smooth([(428, 640), (424, 690), (426, 736), (436, 764), (456, 770),
               (468, 762), (470, 720), (468, 668), (462, 640)]),
       "Front leg L", fill=GOLD_GRAD, stroke=INK, strokeWidth=5)
d.path(smooth([(538, 640), (532, 668), (530, 720), (532, 762), (544, 770),
               (564, 764), (574, 736), (576, 690), (572, 640)]),
       "Front leg R", fill=GOLD_GRAD, stroke=INK, strokeWidth=5)
d.path("M426,754 C442,744 464,744 474,756 C470,770 448,778 434,770 "
       "C426,764 422,760 426,754 Z", "Front paw L", fill=CREAM_GRAD,
       stroke=INK, strokeWidth=4)
d.path("M526,756 C538,744 560,744 574,754 C578,760 574,764 566,770 "
       "C552,778 530,770 526,756 Z", "Front paw R", fill=CREAM_GRAD,
       stroke=INK, strokeWidth=4)

# neck rising into the head
d.path(smooth([(440, 560), (446, 524), (458, 496), (478, 478), (522, 478),
               (542, 496), (554, 524), (560, 560), (540, 574), (460, 574)]),
       "Neck", fill=GOLD_GRAD, stroke=INK, strokeWidth=6)

# head — broad gentle skull, frontal
d.path(smooth([(500, 330), (544, 336), (576, 358), (592, 392), (590, 428),
               (576, 458), (550, 480), (522, 492), (500, 494), (478, 492),
               (450, 480), (424, 458), (410, 428), (408, 392), (424, 358),
               (456, 336)]),
       "Head", fill=GOLD_GRAD, stroke=INK, strokeWidth=6)
# crown sheen
d.path("M438,364 C466,344 534,344 564,366 C528,354 472,354 438,376 Z",
       "Crown sheen", fill="#F2DCA8", opacity=35, stroke=NONE)

# drop ears with feathered lower edges — hanging beside the cheeks
d.path(smooth([(418, 380), (402, 404), (394, 440), (396, 478), (408, 506),
               (426, 514), (438, 498), (442, 462), (438, 420), (430, 394)]),
       "Ear L", fill=DIM_GOLD, stroke=INK, strokeWidth=5)
d.path(smooth([(582, 380), (598, 404), (606, 440), (604, 478), (592, 506),
               (574, 514), (562, 498), (558, 462), (562, 420), (570, 394)]),
       "Ear R", fill=DIM_GOLD, stroke=INK, strokeWidth=5)
# feathering off the ear bottoms
for i, dd in enumerate(["M404,470 C400,490 402,508 410,522",
                        "M418,478 C414,496 416,512 424,524",
                        "M596,470 C600,490 598,508 590,522",
                        "M582,478 C586,496 584,512 576,524"]):
    d.path(dd, f"Ear feather {i+1}", fill=NONE, stroke="#B8894A",
           strokeWidth=3.5, opacity=60, cap="round")

# muzzle — broad and soft, the gentle mouth
d.path(smooth([(452, 470), (440, 478), (436, 494), (444, 510), (462, 522),
               (482, 528), (518, 528), (538, 522), (556, 510), (564, 494),
               (560, 478), (548, 470), (530, 464), (470, 464)]),
       "Muzzle", fill=CREAM_GRAD, stroke=INK, strokeWidth=4)
# nose — broad dark, soft sheen
d.path("M478,474 C468,478 464,488 470,496 C478,502 496,502 504,494 "
       "C510,486 504,476 492,474 Z", "Nose", fill="#171009",
       stroke=INK, strokeWidth=3)
d.path("M474,482 C480,478 490,477 496,480", "Nose sheen", fill=NONE,
       stroke="#8A7452", strokeWidth=2.5, opacity=75, cap="round")
# the soft mouth — a level line with the corners easing down, no grin
d.path("M456,508 C480,518 520,518 544,508", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.path("M500,510 L500,516", "Chin cleft", fill=NONE, stroke=INK,
       strokeWidth=3, opacity=70, cap="round")

# kind eyes — level, soft, wide-set on the golden face
d.path("M434,430 C442,420 458,418 468,426 C466,439 450,444 440,440 "
       "C434,436 432,434 434,430 Z", "Eye L",
       fill=rad((0, "#7A5224"), (0.7, "#4A2E12"), (1, "#241606")),
       stroke=INK, strokeWidth=3.5)
d.path("M532,426 C542,418 558,420 566,430 C568,434 566,436 560,440 "
       "C550,444 534,439 532,426 Z", "Eye R",
       fill=rad((0, "#7A5224"), (0.7, "#4A2E12"), (1, "#241606")),
       stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Pupil L", x=447, y=427, width=10, height=11, fill="#0E0806", stroke=NONE)
d.shape("ellipse", "Pupil R", x=543, y=427, width=10, height=11, fill="#0E0806", stroke=NONE)
d.shape("ellipse", "Glint L", x=450, y=429, width=4.5, height=4.5, fill="#FFF4D8", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=546, y=429, width=4.5, height=4.5, fill="#FFF4D8", opacity=90, stroke=NONE)
# soft level brows — kind, never worried
d.path("M430,420 C442,412 458,412 470,418", "Brow L", fill=NONE,
       stroke="#6B4820", strokeWidth=3.5, opacity=50, cap="round")
d.path("M530,418 C542,412 558,412 570,420", "Brow R", fill=NONE,
       stroke="#6B4820", strokeWidth=3.5, opacity=50, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#38301C", strokeWidth=6)

# --- captions -------------------------------------------------------------------
d.text("GOLDEN RETRIEVER", "Name", x=500, y=934, size=56, font="Virelai Sans",
       color="#F0E2BC", justify="center")
LINE2, SZ2, TRK = "SPORTING · SCOTLAND", 22, 300
r = d.text(LINE2, "Milestone", x=500, y=970, size=SZ2, font="Virelai Sans",
           color="#C4AE84", justify="center")
d.cmd("text.setStyle", "Milestone tracking", id=r["id"], tracking=TRK)

b = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("milestone bounds", {k: round(v) for k, v in b.items()})
nearest = (min(max(PCX, b["x"]), b["x"] + b["width"]),
           min(max(PCY, b["y"]), b["y"] + b["height"]))
clear = math.hypot(nearest[0] - PCX, nearest[1] - PCY) - (PR + 3)
print("clears rim by %.1f" % clear)
assert clear > 0 and b["width"] <= 760 and b["x"] >= 10 and b["x"] + b["width"] <= 990, b

d.finish("golden-retriever-V1R00")
