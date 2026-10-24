#!/usr/bin/env python3
"""Hippopotamus — field-guide plate V1R00. Eyes, ears and the broad nostrilled
snout break a murky river surface; below the waterline only a translucent
rumor of the bulk. Reed-bed mood — cattails inside the rim, ripple rings
around the dome, the river closing on the disc's own arc. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os, math, re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Hippopotamus — Field Plate", 1000, 1000)

INK = "#241A12"                    # warm dark ink, never pure black
CX, CY, R = 500, 460, 420          # plate disc centre + radius

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

BG_GRAD = lin(0, 0, 0, 1000, (0, "#121A10"), (1, "#050805"))
PLATE_GRAD = rad((0, "#9AA06E"), (0.55, "#6E7852"), (1, "#3A4A38"))
SKIN_GRAD = rad((0, "#A89084"), (0.6, "#806A5E"), (1, "#52443C"))
PINK_GRAD = rad((0, "#B89A8C"), (1, "#8E6E60"))
WATER_GRAD = lin(0, 560, 0, 880, (0, "#82865A"), (0.5, "#4E5638"), (1, "#232E22"))
REED_GRAD = lin(0, 300, 0, 620, (0, "#7C904C"), (1, "#4E6234"))
CATTAIL_GRAD = lin(0, 0, 90, 0, (0, "#8A5E34"), (1, "#5E3E22"))

def rim_x(y, r=R, side=-1):
    return CX + side * math.sqrt(r * r - (y - CY) ** 2)

def on_disc(x, y, pad=0, r=R):
    return math.hypot(x - CX, y - CY) <= r - pad

def mirror(dd):
    out, toks, ex = [], re.findall(r"[A-Za-z]|-?\d*\.?\d+", dd), True
    for t in toks:
        if t.isalpha():
            out.append(t); ex = True
        elif ex:
            out.append(f"{1000 - float(t):g},"); ex = False
        else:
            out[-1] += f"{float(t):g}"; ex = True
    return " ".join(out)

def pair(dd, label, **kw):
    d.path(dd, f"{label} L", **kw)
    d.path(mirror(dd), f"{label} R", **kw)

# --- backdrop + river-murk plate -----------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#232E22", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8DCC0", strokeWidth=3, opacity=40)
# silt motes in the air half
for i, (x, y, w) in enumerate([(200,240,5),(330,170,4),(500,140,5),(660,160,4),(790,250,5),
                               (170,380,4),(850,390,4),(300,300,3),(720,330,3),(440,220,3)]):
    assert on_disc(x, y, 12)
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w, fill="#D8DCB4", opacity=35, stroke=NONE)

# --- the water: surface at y=565, closing on the disc's own arc ------------------------
wy = 565
wl, wr = rim_x(wy, side=-1), rim_x(wy, side=1)
d.path(f"M{wl:.1f},{wy} C330,556 420,572 500,564 C580,556 670,560 {wr:.1f},{wy} "
       f"A{R},{R} 0 0 1 {wl:.1f},{wy} Z", "River", fill=WATER_GRAD, stroke=NONE)
# surface sheen along the waterline
d.path(f"M{wl + 10:.1f},{wy} C330,556 420,571 500,564 C580,557 670,560 {wr - 10:.1f},{wy}",
       "Waterline sheen", fill=NONE, stroke="#C8CCA0", strokeWidth=4, opacity=50, cap="round")
# the rumor: the submerged bulk, ghosted through the murk
d.path("M335,575 C330,690 370,780 500,792 C630,780 670,690 665,575 "
       "C620,596 560,606 500,606 C440,606 380,596 335,575 Z",
       "Submerged bulk", fill="#2C3628", opacity=20, stroke=NONE)
d.path("M390,640 C400,700 440,740 500,746 M610,640 C600,700 560,740 500,746",
       "Bulk shade", fill=NONE, stroke="#1E261C", strokeWidth=8, opacity=18, cap="round")
# drifting duckweed flecks
for i, (x, y, w, h) in enumerate([(300,600,26,6),(620,618,30,7),(420,640,22,5),(680,660,26,6),
                                  (350,700,30,7),(560,716,24,6),(470,780,28,7),(640,790,24,6)]):
    d.shape("ellipse", f"Duckweed {i+1}", x=x, y=y, width=w, height=h, fill="#5E7038", opacity=50, stroke=NONE)
for i, (x, y, w) in enumerate([(340,660,20),(530,676,24),(610,740,18),(430,742,16),(520,800,20)]):
    d.path(f"M{x},{y} C{x + w*0.3},{y - 3} {x + w*0.7},{y - 3} {x + w},{y}",
           f"Murk glint {i+1}", fill=NONE, stroke="#9AA46E", strokeWidth=2.5, opacity=30, cap="round")

# --- cattails at the reed-bed edge (all inside the rim) ----------------------------------
def cattail(x, y_tip, y_base, h_head, lean, label):
    """stem + brown head, leaning `lean` px at the tip"""
    tx = x + lean
    d.path(f"M{x},{y_base} Q{x + lean*0.5},{(y_tip + y_base)/2} {tx},{y_tip + h_head}",
           f"{label} stem", fill=NONE, stroke="#4E6234", strokeWidth=4, opacity=80, cap="round")
    d.path(f"M{tx},{y_tip + h_head + 4} L{tx},{y_tip + h_head - 14}",
           f"{label} spike", fill=NONE, stroke="#8A9A5C", strokeWidth=2.5, opacity=80, cap="round")
    d.shape("ellipse", f"{label} head", x=tx - 7, y=y_tip, width=14, height=h_head,
            fill=CATTAIL_GRAD, stroke=NONE)

cattail(158, 380, 590, 62, -14, "Cattail L1")
cattail(196, 430, 585, 50, 10, "Cattail L2")
cattail(844, 372, 590, 62, 14, "Cattail R1")
cattail(806, 438, 588, 48, -8, "Cattail R2")
# blade leaves sweeping up
for i, (x0, y0, x1, y1, w_) in enumerate([(150, 590, 210, 370, 7), (172, 592, 150, 400, 6),
                                          (206, 586, 250, 430, 6), (846, 588, 800, 380, 7),
                                          (824, 590, 852, 420, 6), (790, 584, 756, 446, 6)]):
    for p in [(x0, y0), (x1, y1)]:
        assert on_disc(p[0], p[1], 40), p
    d.path(f"M{x0},{y0} Q{(x0 + x1)/2 + 8},{(y0 + y1)/2} {x1},{y1}",
           f"Blade {i+1}", fill=NONE, stroke=REED_GRAD, strokeWidth=w_, opacity=70, cap="round")

# --- the hippo crown: broad snout dome rising through the waterline -----------------------
d.path("M340,574 C332,500 360,446 410,424 C445,410 555,410 590,424 "
       "C640,446 668,500 660,574 C610,588 555,594 500,594 "
       "C445,594 390,588 340,574 Z",
       "Snout dome", fill=SKIN_GRAD, stroke=INK, strokeWidth=6)
# pinkish crown top
d.shape("ellipse", "Crown pink", x=400, y=412, width=200, height=70,
        fill=PINK_GRAD, opacity=45, stroke=NONE)
# ears: tiny flaps at the dome's upper corners
pair("M368,442 C356,428 358,410 374,404 C390,398 404,408 402,424 "
     "C394,438 380,446 368,442 Z",
     "Ear", fill=PINK_GRAD, stroke=INK, strokeWidth=3.5)
# eyes: the topmost bumps on the head ridge, half-lidded patience
pair("M414,438 C406,418 418,400 438,398 C458,396 470,410 470,428 "
     "C458,442 432,446 414,438 Z",
     "Eye bump", fill=SKIN_GRAD, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Eye L", x=428, y=414, width=16, height=14, fill="#241812", stroke=NONE)
d.shape("ellipse", "Eye R", x=556, y=414, width=16, height=14, fill="#241812", stroke=NONE)
d.shape("ellipse", "Eye glint L", x=432, y=416, width=4, height=4, fill="#F4ECE0", opacity=80, stroke=NONE)
d.shape("ellipse", "Eye glint R", x=560, y=416, width=4, height=4, fill="#F4ECE0", opacity=80, stroke=NONE)
pair("M418,424 C428,414 448,412 460,420", "Eye lid", fill=NONE,
     stroke="#52443C", strokeWidth=4, opacity=70, cap="round")
# nostril pads: two raised mounds on the snout's front-top, below and between the eyes
pair("M436,470 C430,452 444,440 462,440 C480,440 490,452 488,468 "
     "C476,478 452,480 436,470 Z",
     "Nostril mound", fill=PINK_GRAD, stroke=INK, strokeWidth=4)
pair("M446,458 C452,450 464,449 471,455", "Nostril slit", fill=NONE,
     stroke="#1C120C", strokeWidth=5, cap="round")
# skin folds across the dome + jowl creases
d.path("M400,486 C440,474 560,474 600,486", "Fold 1", fill=NONE,
       stroke="#4E3E34", strokeWidth=4, opacity=50, cap="round")
d.path("M412,520 C452,510 548,510 588,520", "Fold 2", fill=NONE,
       stroke="#4E3E34", strokeWidth=4, opacity=45, cap="round")
pair("M372,500 C362,526 364,552 376,570", "Jowl crease", fill=NONE,
     stroke="#4E3E34", strokeWidth=4, opacity=50, cap="round")
# dome sheen where light catches the wet skin + the midline groove
d.path("M440,502 C470,494 530,494 560,502", "Wet sheen", fill=NONE,
       stroke="#D8C8BC", strokeWidth=6, opacity=30, cap="round")
d.path("M500,474 C498,510 498,540 500,564", "Midline groove", fill=NONE,
       stroke="#4E3E34", strokeWidth=3.5, opacity=40, cap="round")

# --- ripple rings where the dome breaks the surface ---------------------------------------
for i, (dd_, w_, o_) in enumerate([
        ("M306,580 C390,566 610,566 694,580", 5, 55),
        ("M280,606 C380,588 620,588 720,606", 4, 40),
        ("M330,630 C410,616 590,616 670,630", 3.5, 35),
        ("M380,548 C420,540 580,540 620,548", 4, 45)]):
    d.path(dd_, f"Ripple {i+1}", fill=NONE, stroke="#C8CCA0",
           strokeWidth=w_, opacity=o_, cap="round")
# meniscus highlight hugging the dome base
d.path("M360,568 C400,580 460,586 500,586 C540,586 600,580 640,568",
       "Meniscus", fill=NONE, stroke="#E4E8C4", strokeWidth=4, opacity=55, cap="round")
# a dragonfly skimming, right of the dome
d.path("M700,318 L736,306", "Dragonfly body", fill=NONE, stroke="#3E4A2E", strokeWidth=3, cap="round")
d.shape("ellipse", "Dragonfly wing 1", x=706, y=298, width=26, height=9, fill="#E8EED4", opacity=55, stroke=NONE)
d.shape("ellipse", "Dragonfly wing 2", x=716, y=308, width=22, height=8, fill="#E8EED4", opacity=45, stroke=NONE)

# --- name ------------------------------------------------------------------------------------
d.text("HIPPOPOTAMUS", "Name", x=500, y=962, size=48, font="Virelai Sans",
       color="#DCE0C0", justify="center")

d.finish("hippopotamus-V1R00")
