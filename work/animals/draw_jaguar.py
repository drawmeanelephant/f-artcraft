#!/usr/bin/env python3
"""Jaguar — field-guide plate V1R00. Cenote plate, jungle-murk mood: the cat's
massive head front-on, gold coat gone green in the shade, rosettes across the
broad skull and heavy jowls, eyes level and amber under a low brow. Lianas
and wet leaves hang from the rim, dark water closes on the disc's own arc.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math, re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Jaguar — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420          # plate disc centre + radius
INK = "#1C1208"                    # warm dark ink, never pure black
SPOT = "#281504"

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

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

def rosette(cx, cy, rr, label, seed=0):
    """A jaguar rosette: 4-5 broken ring blobs around a center spot."""
    for k in range(5):
        a = math.radians(seed + k * 72)
        bx, by = cx + math.cos(a) * rr, cy + math.sin(a) * rr * 0.8
        bw = 5.5 + (k % 2) * 2
        d.shape("ellipse", f"{label}.{k+1}", x=bx - bw, y=by - bw*0.8,
                width=bw*2, height=bw*1.6, fill=SPOT, opacity=88, stroke=NONE)
    d.shape("ellipse", f"{label} core", x=cx - 3, y=cy - 2.4,
            width=6, height=4.8, fill=SPOT, opacity=70, stroke=NONE)

BG_GRAD = lin(0, 0, 0, 1000, (0, "#08120E"), (1, "#030604"))
PLATE_GRAD = rad((0, "#6E8E6A"), (0.5, "#3A5844"), (1, "#12221A"))
COAT_GRAD = rad((0, "#E0A040"), (0.55, "#B87420"), (1, "#6E3E10"))
PALE_GRAD = rad((0, "#F2E4C0"), (1, "#D0B480"))
MUZZLE_GRAD = rad((0, "#E8D0A0"), (1, "#B08A50"))

# --- backdrop + cenote plate ------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=64, y=24, width=872, height=872,
        fill="#3A5844", opacity=12, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#0C1A12", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#BCD0A8", strokeWidth=3, opacity=35)

# murk glow above the water — light falling into the sinkhole
d.shape("ellipse", "Cenote glow", x=330, y=170, width=340, height=280,
        fill="#C8D8B0", opacity=14, stroke=NONE)
# limestone drips down the left rim — pale stalactite hints
for i, (x, y, w, h) in enumerate([(170, 130, 26, 90), (210, 108, 20, 70),
                                  (792, 118, 24, 84), (824, 148, 18, 62)]):
    d.path(f"M{x},{y} q{w/2},{h*0.4} {w*0.3},{h} q-{w*0.5},{h*0.2} -{w*0.4},-{h*0.4} Z",
           f"Limestone {i+1}", fill="#8A9878", opacity=35, stroke=NONE)

# hanging lianas from the top rim, jungle-murk silhouettes
for i, (x, y0, y1, sway) in enumerate([(230, 60, 330, 30), (290, 52, 250, -24),
                                       (720, 56, 300, 26), (776, 70, 230, -20),
                                       (150, 90, 260, 18)]):
    d.path(f"M{x},{y0} C{x + sway},{(y0+y1)/2 - 30} {x - sway},{(y0+y1)/2 + 30} {x + sway//2},{y1}",
           f"Liana {i+1}", fill=NONE, stroke="#0E1E14", strokeWidth=6,
           opacity=75, cap="round")
# wet leaves on the lianas — simple pointed ovals
for i, (x, y, a) in enumerate([(226, 210, -25), (244, 300, 20), (288, 160, -30),
                               (716, 190, 25), (742, 270, -18), (780, 150, 30),
                               (156, 190, -20), (232, 260, 35)]):
    t = math.radians(a); c, s = math.cos(t), math.sin(t)
    d.path(f"M{x},{y} q{14*c - 4*s:.0f},{14*s + 4*c:.0f} {26*c:.0f},{26*s:.0f} "
           f"q{-12*c - 8*s:.0f},{-12*s + 8*c:.0f} {-26*c:.0f},{-26*s:.0f} Z",
           f"Leaf {i+1}", fill="#1E3423", opacity=80, stroke=NONE)

# --- chest mass rising out of the dark water, closing on the disc arc ---------------
cy_ = 736
cl, cr = rim_x(cy_, side=-1), rim_x(cy_, side=1)
d.path(f"M{cl:.1f},{cy_} C300,724 380,748 470,738 C560,728 640,732 {cr:.1f},{cy_} "
       f"A{R},{R} 0 0 1 {cl:.1f},{cy_} Z", "Cenote water",
       fill=lin(0, 730, 0, 880, (0, "#2A4634"), (0.5, "#162A20"), (1, "#0A1612")),
       stroke=NONE)
d.path(f"M{cl+8:.0f},{cy_} C300,724 380,748 470,738 C560,728 640,732 {cr-8:.0f},{cy_}",
       "Water line", fill=NONE, stroke="#9CBCA0", strokeWidth=5, opacity=45, cap="round")
# reflected light ripples
for i, (x, y, w) in enumerate([(260, 768, 90), (400, 784, 120), (560, 772, 100),
                               (700, 790, 80), (330, 820, 110), (590, 830, 90)]):
    d.path(f"M{x},{y} q{w/2},-{4 + i % 3} {w},0", f"Ripple {i+1}", fill=NONE,
           stroke="#7A9C80", strokeWidth=3.5, opacity=35, cap="round")

# chest and shoulders — the cat shouldering out of the murk
d.path("M300,730 C300,640 340,570 410,540 L590,540 C660,570 700,640 700,730 "
       "C700,760 660,780 500,780 C340,780 300,760 300,730 Z",
       "Chest", fill=lin(0, 540, 0, 780, (0, "#B87420"), (1, "#5E3210")),
       stroke=INK, strokeWidth=6)
# chest rosettes scattered on the shoulders
for i, (x, y, rr, s) in enumerate([(360, 640, 12, 30), (410, 690, 10, 80),
                                   (640, 640, 12, 50), (590, 695, 10, 10),
                                   (470, 720, 9, 60), (545, 725, 9, 100)]):
    rosette(x, y, rr, f"Chest rosette {i+1}", seed=s)

# --- ears: small, rounded, seated low on the skull corners -----------------------------
EAR = ("M356,368 C330,348 322,310 336,282 C348,258 380,252 402,268 "
       "C422,282 426,316 414,342 C402,366 378,380 356,368 Z")
pair(EAR, "Ear", fill=rad((0, "#6E3E10"), (1, "#2E1808")),
     stroke=INK, strokeWidth=5)
pair("M364,346 C350,332 348,310 358,296 C368,284 386,284 396,296 "
     "C406,308 404,328 394,340 C384,350 374,354 364,346 Z",
     "Inner ear", fill="#241408", opacity=80, stroke=NONE)

# --- the head: broad skull, heavy jaw, the skull-crusher build -------------------------
HEAD = ("M500,296 C590,296 660,346 682,430 C698,492 688,562 650,622 "
        "C622,666 566,696 500,696 C434,696 378,666 350,622 "
        "C312,562 302,492 318,430 C340,346 410,296 500,296 Z")
d.path(HEAD, "Head", fill=COAT_GRAD, stroke=INK, strokeWidth=7)
# skull breadth shading — the wide cheekbone sweep
pair("M336,430 C328,490 338,548 366,596", "Cheek edge", fill=NONE,
     stroke="#5E3210", strokeWidth=14, opacity=40, cap="round")
# crown light between the ears
d.shape("ellipse", "Crown light", x=420, y=310, width=160, height=60,
        fill="#F0C060", opacity=25, stroke=NONE)

# --- rosettes: broken rings across crown, temples and cheeks ---------------------------
for i, (x, y, rr, s) in enumerate([
        (430, 330, 11, 10), (500, 322, 12, 70), (570, 330, 11, 130),
        (400, 372, 10, 40), (462, 368, 9, 100), (538, 368, 9, 20),
        (600, 372, 10, 160), (356, 410, 11, 80), (644, 410, 11, 140)]):
    rosette(x, y, rr, f"Crown rosette {i+1}", seed=s)
for i, (x, y, rr, s) in enumerate([
        (342, 470, 10, 30), (352, 530, 9, 90), (378, 585, 10, 150),
        (658, 470, 10, 60), (648, 530, 9, 120), (622, 585, 10, 180)]):
    rosette(x, y, rr, f"Cheek rosette {i+1}", seed=s)
# small solid spots between brow and eyes
for i, (x, y) in enumerate([(452, 420), (486, 412), (514, 412), (548, 420),
                            (470, 444), (530, 444)]):
    d.shape("ellipse", f"Brow spot {i+1}", x=x - 4.5, y=y - 3.5,
            width=9, height=7, fill=SPOT, opacity=85, stroke=NONE)

# --- the pale mask: eye surrounds, muzzle and chin -------------------------------------
pair("M370,470 C380,510 410,540 446,552 C470,560 478,584 470,608 "
     "C456,640 412,652 382,632 C356,614 348,576 356,540 "
     "C360,514 364,490 370,470 Z",
     "Cheek pale", fill=PALE_GRAD, opacity=80, stroke=NONE)
d.path("M430,600 C440,640 460,668 500,672 C540,668 560,640 570,600 "
       "C576,646 560,686 500,690 C440,686 424,646 430,600 Z",
       "Throat pale", fill=PALE_GRAD, opacity=90, stroke=NONE)

# --- eyes: level, amber-green, the flat jaguar stare ------------------------------------
pair("M392,470 C408,448 444,442 466,458 C462,484 432,496 404,488 "
     "C396,484 392,478 392,470 Z",
     "Eye", fill=rad((0, "#D8BC50"), (0.6, "#A08A28"), (1, "#5E5214")),
     stroke=INK, strokeWidth=5)
pair("M410,458 C420,452 436,454 444,464 C446,480 438,490 424,490 "
     "C412,488 406,472 410,458 Z",
     "Pupil", fill="#120C06", stroke=NONE)
d.shape("ellipse", "Glint L", x=416, y=462, width=7, height=7,
        fill="#FFF4D8", opacity=85, stroke=NONE)
d.shape("ellipse", "Glint R", x=577, y=462, width=7, height=7,
        fill="#FFF4D8", opacity=85, stroke=NONE)
# the low heavy brow — brow folds make the stare
pair("M384,448 C404,428 446,424 470,442", "Brow fold", fill=NONE,
     stroke="#6E3E10", strokeWidth=9, opacity=70, cap="round")
d.path("M486,428 C492,444 492,462 488,478 M514,428 C508,444 508,462 512,478",
       "Forehead furrow", fill=NONE, stroke="#8A5018", strokeWidth=6,
       opacity=60, cap="round")

# --- muzzle: broad pale pad, wide nose, heavy jowls -------------------------------------
d.path("M430,540 C440,516 470,504 500,504 C530,504 560,516 570,540 "
       "C580,570 570,606 544,624 C528,636 472,636 456,624 "
       "C430,606 420,570 430,540 Z",
       "Muzzle pad", fill=MUZZLE_GRAD, stroke=NONE)
# whisker pits — the jaguar's dense dot rows
for i, (x, y) in enumerate([(446, 556), (440, 574), (448, 592), (462, 566),
                            (458, 584), (554, 556), (560, 574), (552, 592),
                            (538, 566), (542, 584)]):
    d.shape("ellipse", f"Whisker pit {i+1}", x=x - 3, y=y - 2.5,
            width=6, height=5, fill=SPOT, opacity=60, stroke=NONE)
# nose: the wide trapezoid, rust-red top
d.path("M468,520 C482,512 518,512 532,520 C540,536 536,554 522,562 "
       "C510,568 490,568 478,562 C464,554 460,536 468,520 Z",
       "Nose", fill=lin(470, 512, 530, 568, (0, "#9C4A30"), (1, "#582414")),
       stroke=INK, strokeWidth=4)
pair("M478,548 C474,540 478,532 486,530 C492,532 494,540 490,546 "
     "C486,551 480,551 478,548 Z",
     "Nostril", fill="#2E1008", stroke=NONE)
d.path("M500,566 L500,580", "Philtrum", fill=NONE, stroke=INK,
       strokeWidth=4, cap="round")
# mouth: a heavy level line — the big jaw doesn't smile
d.path("M500,580 C474,586 448,586 430,582 M500,580 C526,586 552,586 570,582",
       "Mouth", fill=NONE, stroke=INK, strokeWidth=5, cap="round")
pair("M430,582 C424,588 420,596 420,604", "Jowl droop", fill=NONE,
     stroke=INK, strokeWidth=4, opacity=60, cap="round")
# whiskers — sparse, pale, drooping
for i, (x1, y1, x2, y2) in enumerate([(440,560,330,540),(438,578,322,578),(442,594,336,612),
                                      (560,560,670,540),(562,578,678,578),(558,594,664,612)]):
    d.path(f"M{x1},{y1} Q{(x1+x2)/2},{min(y1,y2)-8} {x2},{y2}", f"Whisker {i+1}",
           fill=NONE, stroke="#E8D8B8", strokeWidth=2.5, opacity=45, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#081410", strokeWidth=6)

# --- name ---------------------------------------------------------------------------
d.text("JAGUAR", "Name", x=500, y=962, size=58, font="Virelai Sans",
       color="#D8E4C8", justify="center")

d.finish("jaguar-V1R00")
