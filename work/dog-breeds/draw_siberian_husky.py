#!/usr/bin/env python3
"""Siberian husky — milestone card V1R00. Harness-ready stance on a snow
crust: compact powerful frame in profile facing left, pricked triangular
ears, the masked face with ice-blue eyes, the sickle tail curled up over
the back. Grey-and-white coat on a cold blue-grey disc; a puff of
breath-frost off the nose. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Siberian Husky — Milestone Card", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#1E2226"                    # cold warm-dark ink, never pure black


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


BG_GRAD = lin(0, 0, 0, 1000, (0, "#0E1418"), (1, "#050809"))
PLATE_GRAD = rad((0, "#B4C6CE"), (0.55, "#76909C"), (1, "#3C4E58"))
GREY_GRAD = lin(340, 360, 640, 780, (0, "#8A96A0"), (0.55, "#5E6A74"), (1, "#38424A"))
DIM_GREY = lin(340, 360, 640, 780, (0, "#6A767E"), (1, "#2E363C"))
WHITE_GRAD = lin(380, 420, 560, 780, (0, "#F0F4F4"), (1, "#C2CCD0"))
SNOW_GRAD = lin(0, 770, 0, 880, (0, "#DCE8EA"), (0.55, "#A8BCc0".upper()), (1, "#6E8086"))

# --- backdrop + cold blue-grey plate ---------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#2C3C44", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E4F0F2", strokeWidth=3, opacity=38)

# pale arctic light pooling high in the disc
d.shape("ellipse", "Light pool", x=320, y=140, width=380, height=230,
        fill="#F0F6F2", opacity=16, stroke=NONE)
# blowing-snow streaks, thin lenses
for i, (x, y, w) in enumerate([(300, 300, 80), (620, 230, 70), (720, 360, 75),
                               (245, 460, 60), (760, 480, 60), (470, 195, 55)]):
    assert on_disc(x, y, 20), i
    d.shape("ellipse", f"Drift {i+1}", x=x - w / 2, y=y - w / 6, width=w, height=w * 0.33,
            fill="#EAF2F4", opacity=12, stroke=NONE)

# --- snow crust, closing on the disc arc ------------------------------------------
fy = 790
fl, fr = rim_x(fy, -1), rim_x(fy, 1)
d.path(f"M{fl:.1f},{fy} C300,780 400,802 500,794 C600,786 700,790 {fr:.1f},{fy} "
       f"A{PR},{PR} 0 0 1 {fl:.1f},{fy} Z", "Snow", fill=SNOW_GRAD, stroke=NONE)
d.path(f"M{fl + 8:.0f},{fy} C300,780 400,802 500,794 C600,786 700,790 {fr - 8:.0f},{fy}",
       "Crust line", fill=NONE, stroke="#F4FAFA", strokeWidth=5, opacity=55, cap="round")
# kicked crust chips and wind-scored grooves
for i, (x, y) in enumerate([(330, 812), (420, 834), (560, 838), (650, 812)]):
    assert on_disc(x, y + 8, 14), i
    for j, (dx, dy) in enumerate([(-10, 4), (-2, -6), (8, -4), (14, 6)]):
        d.path(f"M{x + dx * 0.4:.0f},{y + 8} L{x + dx:.0f},{y + dy:.0f}",
               f"Crust {i+1}.{j+1}", fill=NONE, stroke="#8FA4AC",
               strokeWidth=3.5, opacity=55, cap="round")
for i, dd in enumerate(["M322,838 C390,830 460,830 528,838",
                        "M480,852 C536,846 586,846 636,852"]):
    d.path(dd, f"Score {i+1}", fill=NONE, stroke="#7E929A",
           strokeWidth=3, opacity=35, cap="round")

# breath-frost — a small pale puff drifting off the nose
d.shape("ellipse", "Breath frost", x=250, y=430, width=52, height=30,
        fill="#E8F2F4", opacity=22, stroke=NONE)

# soft shadow under the dog on the crust
d.shape("ellipse", "Dog shadow", x=300, y=776, width=420, height=30,
        fill="#16202A", opacity=30, stroke=NONE)

# --- the husky, harness-ready stance, facing left ---------------------------------
# tail — the sickle curl carried up over the back: a thick brush that
# springs off the croup, sweeps up and curls its tip over the spine
d.path("M650,484 C686,444 714,414 736,402 C754,394 764,412 748,430",
       "Tail curl", fill=NONE,
       stroke=lin(650, 480, 750, 400, (0, "#8A96A0"), (0.6, "#5E6A74"), (1, "#48545E")),
       strokeWidth=30, cap="round")
# white under-tip where the curl turns in
d.path("M748,404 C760,408 758,422 744,430", "Tail white tip", fill=NONE,
       stroke="#E8EEEE", strokeWidth=16, opacity=85, cap="round")
for i, dd in enumerate(["M660,474 C690,442 714,420 734,410",
                        "M656,490 C688,458 716,434 740,420"]):
    d.path(dd, f"Tail fur {i+1}", fill=NONE, stroke="#2E3840",
           strokeWidth=4, opacity=45, cap="round")

# hind legs — compact angulation, standing square
d.path(smooth([(600, 556), (632, 606), (644, 652), (638, 704), (634, 744),
               (652, 758), (668, 748), (668, 708), (676, 656), (672, 606),
               (658, 560)]),
       "Hind leg far", fill=DIM_GREY, stroke=INK, strokeWidth=4.5)
d.path(smooth([(562, 560), (602, 606), (618, 652), (612, 704), (608, 748),
               (628, 762), (646, 750), (644, 708), (650, 654), (644, 604),
               (628, 560)]),
       "Hind leg near", fill=GREY_GRAD, stroke=INK, strokeWidth=5)
d.path("M606,746 C622,738 642,742 650,752 C646,764 624,770 612,762 "
       "C604,756 602,750 606,746 Z", "Hind paw near", fill=WHITE_GRAD,
       stroke=INK, strokeWidth=4)
d.path("M634,742 C648,736 664,740 670,750 C666,760 648,764 638,756 "
       "C632,750 630,746 634,742 Z", "Hind paw far", fill=WHITE_GRAD,
       opacity=90, stroke=INK, strokeWidth=3.5)

# body — compact and powerful, level topline, deep chest, slight tuck-up
d.path(smooth([(386, 480), (430, 446), (510, 440), (590, 452), (650, 478),
               (664, 512), (644, 550), (588, 576), (522, 588), (458, 586),
               (408, 562), (384, 524)]),
       "Body", fill=GREY_GRAD, stroke=INK, strokeWidth=6)
# the white underline — belly, chest and inner legs
d.path(smooth([(400, 540), (420, 570), (460, 592), (524, 600), (580, 588),
               (610, 566), (600, 584), (560, 610), (500, 616), (446, 606),
               (410, 578)]),
       "White underline", fill=WHITE_GRAD, opacity=92, stroke=NONE)
# topline sheen — cold light along the back
d.path("M430,458 C490,442 570,444 634,466", "Topline sheen", fill=NONE,
       stroke="#C8D6DC", strokeWidth=5, opacity=40, cap="round")

# front legs — straight columns, white stockings
d.path(smooth([(480, 568), (486, 626), (490, 682), (492, 734), (506, 748),
               (518, 740), (516, 688), (514, 630), (508, 572)]),
       "Front leg far", fill=DIM_GREY, stroke=INK, strokeWidth=4.5)
d.path(smooth([(430, 566), (436, 626), (440, 682), (442, 738), (458, 752),
               (472, 744), (470, 690), (468, 630), (462, 570)]),
       "Front leg near", fill=GREY_GRAD, stroke=INK, strokeWidth=5)
# white stockings on both front legs
d.path("M440,690 C450,684 462,684 468,692 L470,738 C464,748 446,750 440,742 Z",
       "Stocking near", fill=WHITE_GRAD, opacity=90, stroke=NONE)
d.path("M490,684 C498,680 510,680 516,686 L518,734 C512,744 496,746 490,738 Z",
       "Stocking far", fill=WHITE_GRAD, opacity=80, stroke=NONE)
d.path("M440,744 C456,736 474,738 482,750 C478,762 456,768 444,760 "
       "C436,754 436,748 440,744 Z", "Front paw near", fill=WHITE_GRAD,
       stroke=INK, strokeWidth=4)
d.path("M488,740 C502,734 518,736 524,746 C518,758 500,762 490,754 "
       "C484,748 484,744 488,740 Z", "Front paw far", fill=WHITE_GRAD,
       stroke=INK, strokeWidth=3.5)

# neck — thick double-coated ruff rising into the head
d.path(smooth([(380, 486), (388, 448), (400, 414), (420, 388), (448, 372),
               (478, 372), (496, 392), (498, 420), (490, 452), (472, 478),
               (436, 498), (402, 500)]),
       "Neck", fill=GREY_GRAD, stroke=INK, strokeWidth=6)
# white ruff wrapping the front of the neck into the chest
d.path(smooth([(384, 470), (392, 442), (404, 420), (424, 408), (448, 410),
               (462, 426), (460, 452), (448, 476), (428, 494), (400, 496)]),
       "Ruff", fill=WHITE_GRAD, opacity=95, stroke=NONE)
for i, dd in enumerate(["M398,440 C404,458 412,472 424,482",
                        "M412,424 C420,442 430,458 444,468",
                        "M390,460 C396,474 404,486 416,494"]):
    d.path(dd, f"Ruff fur {i+1}", fill=NONE, stroke="#C2CCD0",
           strokeWidth=3.5, opacity=60, cap="round")

# head — one silhouette, wedge muzzle level to the left
d.path(smooth([(298, 430), (318, 418), (350, 408), (384, 400), (404, 378),
               (432, 358), (462, 352), (490, 360), (510, 380), (516, 404),
               (508, 426), (486, 440), (452, 448), (414, 448), (372, 446),
               (336, 442), (312, 436)]),
       "Head", fill=GREY_GRAD, stroke=INK, strokeWidth=5)
# the mask — dark cap over the forehead and muzzle top, dropping to a
# goggle line around the eyes; white face below
d.path(smooth([(300, 428), (322, 414), (354, 404), (388, 396), (412, 374),
               (438, 358), (464, 356), (488, 366), (504, 386), (502, 406),
               (488, 418), (468, 412), (450, 404), (430, 402), (408, 408),
               (390, 416), (360, 420), (330, 426), (310, 432)]),
       "Mask", fill=DIM_GREY, opacity=85, stroke=NONE)
# muzzle band — white underside of the muzzle
d.path(smooth([(302, 434), (330, 438), (360, 440), (392, 438), (408, 430),
               (404, 442), (384, 450), (350, 452), (318, 446)]),
       "Muzzle white", fill=WHITE_GRAD, opacity=90, stroke=NONE)
# nose — black on the muzzle tip
d.path("M292,414 C282,418 280,428 288,434 C296,440 310,436 314,428 "
       "C316,420 308,412 292,414 Z", "Nose", fill="#0F1418",
       stroke=INK, strokeWidth=3)
d.path("M288,422 C293,418 301,417 307,420", "Nose sheen", fill=NONE,
       stroke="#8FA0AA", strokeWidth=2.5, opacity=75, cap="round")
# level mouth
d.path("M310,440 C336,446 364,448 390,444", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=3.5, cap="round")

# pricked triangular ears — smaller and closer-set than the shepherd's
d.path("M430,360 L424,290 L466,336 Z", "Ear near", fill=GREY_GRAD,
       stroke=INK, strokeWidth=5)
d.path("M438,350 L432,308 L456,336 Z", "Ear near inner", fill="#2E3840",
       stroke=NONE)
d.path("M482,360 L492,296 L516,344 Z", "Ear far", fill=DIM_GREY,
       stroke=INK, strokeWidth=4.5)
d.path("M488,352 L494,318 L508,342 Z", "Ear far inner", fill="#22282E",
       stroke=NONE)

# the ice-blue eyes — the breed signature, almond and level
d.path("M412,406 C420,398 434,397 442,404 C440,415 426,420 416,416 "
       "C410,412 408,410 412,406 Z", "Eye",
       fill=rad((0, "#BEE0EC"), (0.7, "#6E9EB4"), (1, "#3A5C6E")),
       stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Pupil", x=423, y=403, width=9, height=10, fill="#0A0E10", stroke=NONE)
d.shape("ellipse", "Glint", x=425, y=404, width=4, height=4, fill="#FFFFFF", opacity=95, stroke=NONE)
d.path("M408,396 C420,390 436,390 446,396", "Brow", fill=NONE,
       stroke="#10161A", strokeWidth=3.5, opacity=55, cap="round")

# double-coat texture ticks on neck and thigh
for i, dd in enumerate(["M404,450 C400,436 400,422 406,410",
                        "M424,470 C420,456 422,440 428,428",
                        "M560,560 C568,584 568,606 560,626",
                        "M586,552 C594,574 596,596 588,616"]):
    d.path(dd, f"Fur {i+1}", fill=NONE, stroke="#2C343C",
           strokeWidth=3.5, opacity=45, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#26343C", strokeWidth=6)

# --- captions -------------------------------------------------------------------
d.text("SIBERIAN HUSKY", "Name", x=500, y=934, size=56, font="Virelai Sans",
       color="#EAF2F0", justify="center")
LINE2, SZ2, TRK = "WORKING · SIBERIA", 22, 300
r = d.text(LINE2, "Milestone", x=500, y=970, size=SZ2, font="Virelai Sans",
           color="#BCCCD2", justify="center")
d.cmd("text.setStyle", "Milestone tracking", id=r["id"], tracking=TRK)

b = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("milestone bounds", {k: round(v) for k, v in b.items()})
nearest = (min(max(PCX, b["x"]), b["x"] + b["width"]),
           min(max(PCY, b["y"]), b["y"] + b["height"]))
clear = math.hypot(nearest[0] - PCX, nearest[1] - PCY) - (PR + 3)
print("clears rim by %.1f" % clear)
assert clear > 0 and b["width"] <= 760 and b["x"] >= 10 and b["x"] + b["width"] <= 990, b

d.finish("siberian-husky-V1R00")
