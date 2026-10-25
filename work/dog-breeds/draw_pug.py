#!/usr/bin/env python3
"""Pug — milestone card V1R00. Front-facing head study: the big round
wrinkled skull, fawn coat, black mask and velvet button ears, huge dark
eyes staring out, the double-curl tail peeking over one shoulder. Bust
closes on the disc's own arc (portrait rule). Warm porcelain disc.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Pug — Milestone Card", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#261C15"                    # warm dark ink, never pure black


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


BG_GRAD = lin(0, 0, 0, 1000, (0, "#1B1613"), (1, "#0A0706"))
PLATE_GRAD = rad((0, "#E8D8BC"), (0.55, "#B89C74"), (1, "#65513A"))
FAWN_GRAD = lin(340, 300, 660, 820, (0, "#E4C89E"), (0.5, "#C29B6C"), (1, "#8A6640"))
MASK_GRAD = lin(420, 430, 580, 660, (0, "#453429"), (0.6, "#2A1E17"), (1, "#150E0A"))
EAR_GRAD = lin(380, 300, 620, 420, (0, "#382B22"), (1, "#171009"))
FLOOR_GRAD = lin(0, 760, 0, 880, (0, "#7A6444"), (0.55, "#54432C"), (1, "#2A2114"))

# --- backdrop + porcelain plate -------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#4A3B28", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F2E6C8", strokeWidth=3, opacity=38)

# warm light pooling high centre
d.shape("ellipse", "Light pool", x=330, y=140, width=360, height=220,
        fill="#F6ECD2", opacity=15, stroke=NONE)
# thin drifting mist
for i, (x, y, w) in enumerate([(310, 330, 80), (630, 240, 70), (720, 370, 75),
                               (250, 460, 60), (760, 480, 60), (460, 195, 55)]):
    assert on_disc(x, y, 20), i
    d.shape("ellipse", f"Mist {i+1}", x=x - w / 2, y=y - w / 5, width=w, height=w * 0.4,
            fill="#F2E8CC", opacity=11, stroke=NONE)

# --- floor, closing on the disc arc ---------------------------------------------
fy = 800
fl, fr = rim_x(fy, -1), rim_x(fy, 1)
d.path(f"M{fl:.1f},{fy} C320,790 420,810 500,800 C580,790 680,796 {fr:.1f},{fy} "
       f"A{PR},{PR} 0 0 1 {fl:.1f},{fy} Z", "Floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{fl + 8:.0f},{fy} C320,790 420,810 500,800 C580,790 680,796 {fr - 8:.0f},{fy}",
       "Floor crest", fill=NONE, stroke="#B79C6A", strokeWidth=5, opacity=40, cap="round")

# soft shadow under the bust
d.shape("ellipse", "Bust shadow", x=290, y=790, width=420, height=32,
        fill="#171008", opacity=30, stroke=NONE)

# --- the pug, front-facing bust ---------------------------------------------------
# double-curl tail peeking over the right shoulder — a tight spiral
d.path("M690,648 C726,632 760,648 766,684 C771,716 748,742 718,738 "
       "C694,734 682,712 690,692 C697,674 718,668 732,680 C744,690 744,708 734,716 "
       "C726,722 716,720 712,712",
       "Tail curl", fill=NONE, stroke="#8A6640", strokeWidth=16, cap="round")
d.path("M690,648 C726,632 760,648 766,684 C771,716 748,742 718,738 "
       "C694,734 682,712 690,692 C697,674 718,668 732,680 C744,690 744,708 734,716 "
       "C726,722 716,720 712,712",
       "Tail curl sheen", fill=NONE, stroke="#C29B6C", strokeWidth=6,
       opacity=70, cap="round")

# shoulders + chest — sides land inside the rim, bottom closes on the arc
sl, sr = rim_x(815, -1) + 16, rim_x(815, 1) - 16
d.path(smooth([(sl, 815), (300, 770), (318, 706), (356, 660), (400, 640),
               (470, 632), (560, 634), (640, 650), (694, 690), (716, 748),
               (sr, 815), (640, 852), (500, 862), (370, 850)]),
       "Shoulders", fill=FAWN_GRAD, stroke=INK, strokeWidth=6)
# chest sheen
d.path("M360,700 C420,672 520,664 600,676 C660,686 700,714 714,748",
       "Chest sheen", fill=NONE, stroke="#EFDCB4", strokeWidth=6,
       opacity=35, cap="round")
# dewlap folds — the pug's loose neck skin, two soft arcs
d.path("M400,690 C460,714 540,714 600,692", "Dewlap 1", fill=NONE,
       stroke="#7A5A38", strokeWidth=5, opacity=45, cap="round")
d.path("M420,720 C470,738 530,738 580,722", "Dewlap 2", fill=NONE,
       stroke="#7A5A38", strokeWidth=4.5, opacity=35, cap="round")

# neck — short thick wedge into the skull
d.path(smooth([(400, 660), (404, 610), (414, 566), (430, 540), (470, 528),
               (540, 528), (576, 542), (592, 570), (600, 612), (600, 656),
               (560, 676), (440, 676)]),
       "Neck", fill=FAWN_GRAD, stroke=INK, strokeWidth=6)

# skull — one big rounded shape, broad cheeks, slightly flat crown
d.path(smooth([(362, 420), (370, 372), (396, 334), (436, 314), (480, 306),
               (528, 306), (570, 316), (606, 338), (630, 374), (638, 420),
               (634, 470), (618, 516), (592, 552), (556, 574), (512, 584),
               (466, 582), (424, 570), (392, 546), (370, 508), (362, 464)]),
       "Skull", fill=FAWN_GRAD, stroke=INK, strokeWidth=6)

# button ears — small velvet flaps folded onto the skull corners
d.path(smooth([(378, 366), (360, 344), (356, 316), (368, 300), (392, 296),
               (414, 306), (424, 328), (420, 356), (404, 372)]),
       "Ear L", fill=EAR_GRAD, stroke=INK, strokeWidth=5)
d.path(smooth([(622, 366), (640, 344), (644, 316), (632, 300), (608, 296),
               (586, 306), (576, 328), (580, 356), (596, 372)]),
       "Ear R", fill=EAR_GRAD, stroke=INK, strokeWidth=5)
d.path("M378,332 C390,324 404,324 414,332", "Ear L fold", fill=NONE,
       stroke="#0E0806", strokeWidth=3.5, opacity=60, cap="round")
d.path("M622,332 C610,324 596,324 586,332", "Ear R fold", fill=NONE,
       stroke="#0E0806", strokeWidth=3.5, opacity=60, cap="round")

# the mask — black velvety face front: muzzle + around the eyes
d.path(smooth([(420, 452), (404, 470), (398, 496), (404, 524), (420, 546),
               (444, 560), (472, 568), (502, 570), (532, 568), (560, 558),
               (582, 542), (596, 518), (600, 492), (592, 468), (576, 452),
               (552, 442), (524, 438), (496, 438), (468, 440), (444, 444)]),
       "Mask", fill=MASK_GRAD, stroke=INK, strokeWidth=4.5, opacity=96)

# the wrinkles — furrow arcs on the fawn brow above the mask
for i, dd in enumerate(["M412,398 C440,388 470,384 500,384",
                        "M588,398 C560,388 530,384 500,384",
                        "M428,368 C460,356 540,356 572,368",
                        "M446,340 C480,330 520,330 554,340"]):
    d.path(dd, f"Brow furrow {i+1}", fill=NONE, stroke="#8A6640",
           strokeWidth=4, opacity=55, cap="round")
# the vertical furrow between the eyes and the diamond thumbprint
d.path("M496,404 C494,420 494,434 496,448", "Central furrow", fill=NONE,
       stroke="#8A6640", strokeWidth=4, opacity=50, cap="round")
d.path("M500,388 C508,398 508,410 500,418 C492,410 492,398 500,388 Z",
       "Thumbprint", fill="#B08A5C", opacity=50, stroke=NONE)

# huge round eyes — the whole point of the breed
d.shape("ellipse", "Eye L", x=414, y=452, width=52, height=54,
        fill=rad((0, "#3A2A1A"), (0.7, "#1C120A"), (1, "#0C0705")),
        stroke=INK, strokeWidth=4)
d.shape("ellipse", "Eye R", x=534, y=452, width=52, height=54,
        fill=rad((0, "#3A2A1A"), (0.7, "#1C120A"), (1, "#0C0705")),
        stroke=INK, strokeWidth=4)
d.shape("ellipse", "Glint L", x=428, y=460, width=12, height=12,
        fill="#FFF6DC", opacity=95, stroke=NONE)
d.shape("ellipse", "Glint R", x=548, y=460, width=12, height=12,
        fill="#FFF6DC", opacity=95, stroke=NONE)
# eye-rim wrinkles — the worried lines over each eye
d.path("M408,446 C424,434 448,432 464,442", "Eye rim L", fill=NONE,
       stroke="#100A06", strokeWidth=4, opacity=60, cap="round")
d.path("M592,446 C576,434 552,432 536,442", "Eye rim R", fill=NONE,
       stroke="#100A06", strokeWidth=4, opacity=60, cap="round")

# the short square muzzle on the mask — nose broad and high
d.path("M472,486 C468,472 478,462 500,462 C522,462 532,472 528,486 "
       "C524,498 512,504 500,504 C488,504 476,498 472,486 Z",
       "Nose", fill="#120B08", stroke=INK, strokeWidth=3.5)
d.path("M478,478 C484,472 494,470 502,471", "Nose sheen", fill=NONE,
       stroke="#7E6852", strokeWidth=3, opacity=75, cap="round")
# nostril shadow slits
d.path("M480,488 C484,492 490,494 494,492", "Nostril L", fill=NONE,
       stroke="#050302", strokeWidth=3.5, opacity=80, cap="round")
d.path("M520,488 C516,492 510,494 506,492", "Nostril R", fill=NONE,
       stroke="#050302", strokeWidth=3.5, opacity=80, cap="round")
# the w-mouth and jowl folds
d.path("M500,504 C500,514 496,520 488,522 C476,526 462,522 456,512",
       "Jowl L", fill=NONE, stroke="#0C0705", strokeWidth=4.5, cap="round")
d.path("M500,504 C500,514 504,520 512,522 C524,526 538,522 544,512",
       "Jowl R", fill=NONE, stroke="#0C0705", strokeWidth=4.5, cap="round")
d.path("M470,538 C486,548 514,548 530,538", "Chin", fill=NONE,
       stroke="#0C0705", strokeWidth=4, opacity=85, cap="round")
# whisker-dot ticks on the muzzle, sparse
for i, (x, y) in enumerate([(452, 500), (462, 512), (548, 500), (538, 512)]):
    d.shape("ellipse", f"Whisker dot {i+1}", x=x, y=y, width=5, height=5,
            fill="#0C0705", opacity=70, stroke=NONE)

# soft fawn shading under the jaw
d.path("M430,560 C470,580 530,580 570,560 C550,586 450,586 430,560 Z",
       "Jaw shade", fill="#8A6640", opacity=35, stroke=NONE)

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#403322", strokeWidth=6)

# --- captions -------------------------------------------------------------------
d.text("PUG", "Name", x=500, y=934, size=56, font="Virelai Sans",
       color="#F0E4C8", justify="center")
LINE2, SZ2, TRK = "TOY · CHINA", 22, 280
r = d.text(LINE2, "Milestone", x=500, y=970, size=SZ2, font="Virelai Sans",
           color="#CDBFA0", justify="center")
d.cmd("text.setStyle", "Milestone tracking", id=r["id"], tracking=TRK)

b = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("milestone bounds", {k: round(v) for k, v in b.items()})
nearest = (min(max(PCX, b["x"]), b["x"] + b["width"]),
           min(max(PCY, b["y"]), b["y"] + b["height"]))
clear = math.hypot(nearest[0] - PCX, nearest[1] - PCY) - (PR + 3)
print("clears rim by %.1f" % clear)
assert clear > 0 and b["width"] <= 760 and b["x"] >= 10 and b["x"] + b["width"] <= 990, b

d.finish("pug-V1R00")
