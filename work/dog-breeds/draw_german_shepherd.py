#!/usr/bin/env python3
"""German shepherd — milestone card V1R00. Alert standing profile facing
left: erect pointed ears, long wedge muzzle with the black mask, level
topline easing down to the croup, deep chest, the bushy sabre tail
carried low. Black-and-tan saddle markings over a strong frame. Aloof
and capable, never aggressive. Dusk-field disc, stubble floor closing on
the disc's own arc. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("German Shepherd — Milestone Card", 1000, 1000)

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


BG_GRAD = lin(0, 0, 0, 1000, (0, "#161310"), (1, "#090706"))
PLATE_GRAD = rad((0, "#B5AC8A"), (0.55, "#8C8262"), (1, "#484434"))
TAN_GRAD = lin(340, 340, 640, 780, (0, "#C28E52"), (0.55, "#96683A"), (1, "#6B4826"))
DIM_TAN = lin(340, 340, 640, 780, (0, "#8F683C"), (1, "#523620"))
SADDLE_GRAD = lin(400, 380, 660, 560, (0, "#3E332A"), (0.6, "#261D16"), (1, "#171009"))
FLOOR_GRAD = lin(0, 740, 0, 880, (0, "#6B5F3C"), (0.55, "#4A4229"), (1, "#2B2415"))

# --- backdrop + dusk-field plate ------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#3C3826", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E4DCBC", strokeWidth=3, opacity=38)

# last light pooling upper-centre
d.shape("ellipse", "Light pool", x=330, y=140, width=380, height=220,
        fill="#F0E4B4", opacity=15, stroke=NONE)
# drifting dust/mist lenses
for i, (x, y, w) in enumerate([(300, 300, 80), (610, 240, 70), (720, 370, 75),
                               (245, 460, 60), (755, 480, 60), (470, 195, 55)]):
    assert on_disc(x, y, 20), i
    d.shape("ellipse", f"Mist {i+1}", x=x - w / 2, y=y - w / 5, width=w, height=w * 0.4,
            fill="#EDE4BE", opacity=11, stroke=NONE)

# --- stubble field floor, closing on the disc arc --------------------------------
fy = 782
fl, fr = rim_x(fy, -1), rim_x(fy, 1)
d.path(f"M{fl:.1f},{fy} C310,772 420,792 500,784 C580,776 690,780 {fr:.1f},{fy} "
       f"A{PR},{PR} 0 0 1 {fl:.1f},{fy} Z", "Floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{fl + 8:.0f},{fy} C310,772 420,792 500,784 C580,776 690,780 {fr - 8:.0f},{fy}",
       "Floor crest", fill=NONE, stroke="#A8986A", strokeWidth=5, opacity=42, cap="round")
# stubble ticks on the crest
for i, (x, y) in enumerate([(340, 800), (420, 822), (500, 830), (590, 818), (664, 800)]):
    assert on_disc(x, y + 8, 14), i
    for j, (dx, dy) in enumerate([(-10, 6), (-3, -6), (5, -8), (12, 2)]):
        d.path(f"M{x + dx * 0.4:.0f},{y + 10} L{x + dx:.0f},{y + dy:.0f}",
               f"Stubble {i+1}.{j+1}", fill=NONE, stroke="#8C7A50",
               strokeWidth=3.5, opacity=60, cap="round")

# soft shadow under the dog
d.shape("ellipse", "Dog shadow", x=300, y=760, width=430, height=32,
        fill="#191206", opacity=32, stroke=NONE)

# --- the shepherd, alert standing profile, facing left ----------------------------
# tail — bushy sabre hanging low off the croup, tip nearly to the hocks
d.path(smooth([(668, 470), (706, 500), (722, 548), (716, 600), (694, 644),
               (670, 664), (652, 656), (660, 616), (670, 570), (662, 526)]),
       "Tail", fill=lin(660, 470, 720, 660, (0, "#3E332A"), (0.6, "#221A12"), (1, "#4A3620")),
       stroke=INK, strokeWidth=5)
for i, dd in enumerate(["M676,500 C700,536 706,580 694,622",
                        "M668,520 C690,556 696,596 688,632",
                        "M682,486 C704,520 712,560 706,596"]):
    d.path(dd, f"Tail fur {i+1}", fill=NONE, stroke="#0F0B08",
           strokeWidth=4, opacity=45, cap="round")

# hind legs — the stacked stance: thigh forward into the stifle, hock back
d.path(smooth([(620, 540), (648, 596), (646, 648), (634, 706), (628, 748),
               (646, 764), (662, 758), (664, 716), (676, 656), (678, 600),
               (664, 552)]),
       "Hind leg far", fill=DIM_TAN, stroke=INK, strokeWidth=4.5)
d.path(smooth([(582, 548), (626, 594), (642, 640), (632, 678), (612, 716),
               (608, 752), (628, 766), (648, 756), (652, 716), (664, 656),
               (662, 600), (646, 552)]),
       "Hind leg near", fill=TAN_GRAD, stroke=INK, strokeWidth=5)
d.path("M614,744 C632,738 652,740 660,750 C656,762 634,768 620,760 "
       "C612,754 610,750 614,744 Z", "Hind paw near", fill="#7A5630",
       stroke=INK, strokeWidth=4)
d.path("M644,742 C660,738 676,742 682,752 C676,762 656,766 646,758 "
       "C640,752 640,746 644,742 Z", "Hind paw far", fill="#5E4022",
       stroke=INK, strokeWidth=3.5)

# body — the strong frame: withers high, level back easing to the croup,
# deep chest, slight tuck-up to the loin
d.path(smooth([(380, 470), (430, 430), (520, 428), (610, 448), (666, 482),
               (676, 520), (648, 556), (586, 586), (520, 600), (460, 600),
               (412, 574), (386, 528)]),
       "Body", fill=TAN_GRAD, stroke=INK, strokeWidth=6)
# the black saddle — nape running off the skull's back, opening into the
# blanket over the back to the hips and tail head
d.path(smooth([(430, 396), (462, 372), (500, 368), (524, 384), (524, 418),
               (506, 452), (478, 472), (446, 478), (430, 456), (426, 424)]),
       "Nape", fill=SADDLE_GRAD, stroke=INK, strokeWidth=4)
d.path(smooth([(424, 452), (480, 424), (560, 426), (630, 446), (664, 480),
               (640, 496), (580, 482), (516, 476), (456, 478), (420, 470)]),
       "Saddle", fill=SADDLE_GRAD, stroke=INK, strokeWidth=4)
d.path(smooth([(640, 460), (664, 476), (676, 508), (662, 528), (640, 516),
               (630, 488)]),
       "Hip saddle", fill=SADDLE_GRAD, stroke=INK, strokeWidth=3.5)
# saddle edge feathering into the tan — the broken blanket line
for i, dd in enumerate(["M448,478 C470,486 496,488 520,486",
                        "M540,484 C566,490 594,492 620,490",
                        "M470,472 C470,484 466,494 458,502",
                        "M580,478 C584,490 582,500 576,508"]):
    d.path(dd, f"Saddle edge {i+1}", fill=NONE, stroke="#3A2C1E",
           strokeWidth=4, opacity=55, cap="round")
# chest depth line + belly tuck
d.path("M414,540 C420,566 436,586 462,596", "Chest depth", fill=NONE,
       stroke="#5A3C1E", strokeWidth=4.5, opacity=55, cap="round")
d.path("M510,596 C548,596 590,586 622,568", "Tuck-up", fill=NONE,
       stroke="#5A3C1E", strokeWidth=4, opacity=45, cap="round")
# topline sheen along the saddle
d.path("M450,442 C510,426 590,430 648,456", "Topline sheen", fill=NONE,
       stroke="#6A5640", strokeWidth=5, opacity=35, cap="round")

# front legs — the near column straight and sound, far leg a shade back
d.path(smooth([(488, 580), (494, 640), (496, 700), (498, 744), (514, 752),
               (524, 744), (520, 700), (518, 640), (514, 584)]),
       "Front leg far", fill=DIM_TAN, stroke=INK, strokeWidth=4.5)
d.path(smooth([(438, 578), (442, 640), (446, 700), (448, 748), (466, 756),
               (478, 746), (474, 700), (472, 640), (468, 582)]),
       "Front leg near", fill=TAN_GRAD, stroke=INK, strokeWidth=5)
d.path("M446,744 C462,738 480,740 486,750 C480,762 458,766 448,758 "
       "C442,752 442,748 446,744 Z", "Front paw near", fill="#7A5630",
       stroke=INK, strokeWidth=4)
d.path("M496,740 C510,736 524,738 530,748 C524,758 506,762 496,754 "
       "C490,748 490,744 496,740 Z", "Front paw far", fill="#5E4022",
       stroke=INK, strokeWidth=3.5)

# neck — strong and long, rising at 45 degrees into the alert head
d.path(smooth([(372, 478), (388, 442), (402, 406), (422, 378), (454, 360),
               (486, 360), (504, 382), (504, 414), (490, 448), (464, 472),
               (420, 494)]),
       "Neck", fill=TAN_GRAD, stroke=INK, strokeWidth=6)
# shoulder blade shading where the neck meets the chest
d.path("M412,470 C428,492 444,514 458,536", "Shoulder blade", fill=NONE,
       stroke="#5A3C1E", strokeWidth=5, opacity=45, cap="round")

# head — one silhouette: forehead easing into the long level muzzle,
# nose at the tip, under-jaw back to the neck. No separate muzzle blob.
d.path(smooth([(300, 428), (318, 416), (350, 406), (384, 398), (404, 378),
               (432, 358), (464, 350), (492, 358), (512, 378), (518, 402),
               (508, 424), (486, 440), (452, 450), (414, 452), (372, 452),
               (336, 446), (312, 438)]),
       "Head", fill=TAN_GRAD, stroke=INK, strokeWidth=5)
# black mask — covers the muzzle top, forehead front and the eye surround,
# then runs into the nape
d.path(smooth([(306, 420), (330, 406), (362, 396), (394, 392), (416, 396),
               (428, 408), (424, 424), (404, 436), (372, 442), (338, 440),
               (314, 432)]),
       "Mask", fill=SADDLE_GRAD, opacity=88, stroke=NONE)
# nose — black on the mask tip
d.path("M296,414 C286,418 284,428 292,434 C300,440 314,436 318,428 "
       "C320,420 312,412 296,414 Z", "Nose", fill="#120C08",
       stroke=INK, strokeWidth=3)
d.path("M292,422 C297,418 305,417 311,420", "Nose sheen", fill=NONE,
       stroke="#7A6248", strokeWidth=2.5, opacity=75, cap="round")
# level mouth under the muzzle
d.path("M312,440 C338,446 368,448 394,446", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=3.5, cap="round")

# erect ears — tall open triangles pricked off the skull top
d.path("M436,360 L424,272 L474,330 Z", "Ear near", fill=TAN_GRAD,
       stroke=INK, strokeWidth=5)
d.path("M440,350 L432,294 L464,332 Z", "Ear near inner", fill="#3A2A18",
       stroke=NONE)
d.path("M490,364 L498,282 L524,342 Z", "Ear far", fill=DIM_TAN,
       stroke=INK, strokeWidth=4.5)
d.path("M496,354 L500,306 L516,340 Z", "Ear far inner", fill="#2E2012",
       stroke=NONE)

# eye — dark almond, level and watchful (aloof, never hard)
d.path("M414,406 C422,398 436,397 444,404 C442,415 428,420 418,416 "
       "C412,412 410,410 414,406 Z", "Eye",
       fill=rad((0, "#8A5E2C"), (0.7, "#543514"), (1, "#2A1A0A")),
       stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Pupil", x=425, y=403, width=9, height=10, fill="#0E0806", stroke=NONE)
d.shape("ellipse", "Glint", x=427, y=404, width=4, height=4, fill="#FFF4D8", opacity=88, stroke=NONE)
d.path("M410,396 C422,390 438,390 448,396", "Brow", fill=NONE,
       stroke="#0F0A08", strokeWidth=3.5, opacity=50, cap="round")

# guard-coat texture — a few ticks on neck and thigh
for i, dd in enumerate(["M408,438 C404,424 404,412 408,400",
                        "M424,456 C420,442 420,428 424,416",
                        "M560,560 C568,584 568,608 560,630",
                        "M588,548 C596,572 596,596 588,618"]):
    d.path(dd, f"Fur {i+1}", fill=NONE, stroke="#4A3018",
           strokeWidth=3.5, opacity=45, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#38341F", strokeWidth=6)

# --- captions -------------------------------------------------------------------
d.text("GERMAN SHEPHERD", "Name", x=500, y=934, size=56, font="Virelai Sans",
       color="#EDE4C4", justify="center")
LINE2, SZ2, TRK = "HERDING · GERMANY", 22, 300
r = d.text(LINE2, "Milestone", x=500, y=970, size=SZ2, font="Virelai Sans",
           color="#C4B890", justify="center")
d.cmd("text.setStyle", "Milestone tracking", id=r["id"], tracking=TRK)

b = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("milestone bounds", {k: round(v) for k, v in b.items()})
nearest = (min(max(PCX, b["x"]), b["x"] + b["width"]),
           min(max(PCY, b["y"]), b["y"] + b["height"]))
clear = math.hypot(nearest[0] - PCX, nearest[1] - PCY) - (PR + 3)
print("clears rim by %.1f" % clear)
assert clear > 0 and b["width"] <= 760 and b["x"] >= 10 and b["x"] + b["width"] <= 990, b

d.finish("german-shepherd-V1R00")
