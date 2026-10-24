#!/usr/bin/env python3
"""Fiddler crab — field plate V1R00. Front-on male on a low-tide mudflat:
squarish carapace, close-set eyestalks, walking legs in the wet mud, and the
major claw held high in the semaphore wave. One claw for waving, one for
eating — the small feeding claw sits by the mouth. Feeding pellets and a
burrow entrance dot the mud floor, which closes on the disc's own arc.
A second male waves far off on the flat. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Fiddler Crab — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420
INK = "#241608"                    # warm dark ink, never pure black

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    ss = []
    for s in stops:
        st = {"offset": s[0], "color": s[1]}
        if len(s) > 2: st["opacity"] = s[2]
        ss.append(st)
    return {"gradient": {"kind": "radial", "stops": ss}}

def rim_x(y, r=R, side=-1):
    return CX + side * math.sqrt(r * r - (y - CY) ** 2)

BG_GRAD    = lin(0, 0, 0, 1000, (0, "#17110A"), (1, "#070402"))
PLATE_GRAD = rad((0, "#E4D8AE"), (0.55, "#A89C6E"), (1, "#52482C"))
MUD_GRAD   = lin(0, 690, 0, 880, (0, "#7A6440"), (0.55, "#4A3A22"), (1, "#221A0C"))
CARA_GRAD  = rad((0, "#4E7A72"), (0.55, "#2E5048"), (1, "#16302A"))
CLAW_GRAD  = rad((0, "#F2A04E"), (0.6, "#D8722A"), (1, "#9A4A14"))
LEG_GRAD   = lin(0, 560, 0, 700, (0, "#C4A06C"), (1, "#8A6C3E"))

# --- backdrop + mudflat plate -------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#A89C6E", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#3E3A22", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F0E8C4", strokeWidth=3, opacity=45)
# low-tide glare: high pale band + heat shimmer strokes
d.shape("ellipse", "Tide glare", x=240, y=150, width=520, height=180,
        fill="#F6EDC8", opacity=16, stroke=NONE)
for i, dd in enumerate(["M250,300 C370,288 480,290 610,302",
                        "M330,370 C440,360 560,362 680,372"]):
    d.path(dd, f"Shimmer {i+1}", fill=NONE, stroke="#F4ECC8",
           strokeWidth=4, opacity=14, cap="round")
# wind-blown grit motes
for i, (x, y, w) in enumerate([(210,340,5),(790,290,6),(170,480,5),(840,460,6),
                               (420,120,5),(610,110,6),(330,150,4),(700,170,5),
                               (140,600,4),(870,390,4)]):
    d.shape("ellipse", f"Grit {i+1}", x=x, y=y, width=w, height=w*0.8,
            fill="#D8CC9C", opacity=38, stroke=NONE)

# --- distant crab: the semaphore answered far off on the flat ------------------------
d.shape("ellipse", "Distant crab", x=742, y=648, width=36, height=24,
        fill="#332814", opacity=62, stroke=NONE)
for s in (-1, 1):
    d.path(f"M{760+s*9},652 L{760+s*10},640", f"Distant stalk {'L' if s<0 else 'R'}",
           fill=NONE, stroke="#332814", strokeWidth=3, opacity=62, cap="round")
d.path("M772,652 C782,636 792,628 800,630 C806,632 806,642 800,648 "
       "C792,654 780,656 772,652 Z",
       "Distant claw", fill="#3E3018", opacity=55, stroke=NONE)

# --- mudflat floor, closing on the disc's own arc -------------------------------------
fy = 706
fl, fr = rim_x(fy, side=-1), rim_x(fy, side=1)
d.path(f"M{fl:.1f},{fy} C280,694 420,710 560,700 C680,692 790,698 {fr:.1f},{fy} "
       f"A{R},{R} 0 0 1 {fl:.1f},{fy} Z", "Mud floor", fill=MUD_GRAD, stroke=NONE)
# wet crest + tide ripples
d.path(f"M{fl+8:.0f},{fy-3} C280,691 420,707 560,697 C680,689 790,695 {fr-8:.0f},{fy-3}",
       "Wet crest", fill=NONE, stroke="#E8DCB0", strokeWidth=5, opacity=32, cap="round")
for i, dd in enumerate(["M240,752 C340,742 460,744 560,752",
                        "M300,790 C420,780 560,782 690,790",
                        "M430,824 C540,816 650,818 740,824"]):
    d.path(dd, f"Ripple {i+1}", fill=NONE, stroke="#8C7648",
           strokeWidth=4, opacity=45, cap="round")
# standing water glints on the flat
d.shape("ellipse", "Pool 1", x=220, y=724, width=150, height=14,
        fill="#C8B890", opacity=30, stroke=NONE)
d.shape("ellipse", "Pool 2", x=640, y=768, width=180, height=16,
        fill="#C8B890", opacity=24, stroke=NONE)
# burrow entrance with its collar of excavated pellets
d.shape("ellipse", "Burrow", x=300, y=742, width=64, height=26,
        fill="#160E06", opacity=85, stroke=NONE)
d.shape("ellipse", "Burrow lip", x=304, y=740, width=58, height=12,
        fill="#8C7648", opacity=50, stroke=NONE)
# feeding pellets — the crab rolls one per scoop
for i, (x, y, w) in enumerate([(264,730,9),(282,760,7),(250,776,8),(368,748,7),
                               (390,762,8),(340,772,6),(588,726,7),(612,742,8),
                               (628,712,6),(556,738,7),(700,748,7),(760,724,6)]):
    d.shape("ellipse", f"Pellet {i+1}", x=x, y=y, width=w, height=w*0.8,
            fill="#96805A", opacity=75, stroke=INK, strokeWidth=1.5)

# contact shadow under the crab
d.shape("ellipse", "Contact shadow", x=380, y=678, width=280, height=22,
        fill="#14100A", opacity=48, stroke=NONE)

# === the animal =====================================================================
# --- walking legs: thin strokes planted in the mud (>=3.5pt at plate scale) -----------
for i, (x0, y0, x1, y1, x2, y2) in enumerate([
        (428,586, 372,624, 340,690), (444,596, 402,648, 390,706),
        (462,602, 436,660, 438,712),
        (572,586, 622,620, 646,684), (556,598, 590,646, 596,704),
        (540,604, 562,658, 560,712)]):
    d.path(f"M{x0},{y0} L{x1},{y1} L{x2},{y2}", f"Leg {i+1} edge",
           fill=NONE, stroke="#2A1C0C", strokeWidth=8, cap="round")
    d.path(f"M{x0},{y0} L{x1},{y1} L{x2},{y2}", f"Leg {i+1}",
           fill=NONE, stroke=LEG_GRAD, strokeWidth=4.5, cap="round")

# --- minor claw: the small feeding claw tucked by the mouth ---------------------------
d.path("M470,592 C456,602 444,616 438,632 C436,640 442,646 450,644 "
       "C462,640 472,626 476,612 C478,602 476,594 470,592 Z",
       "Feeding claw", fill="#C08A4E", stroke=INK, strokeWidth=3.5)
d.path("M440,634 L430,648 M442,636 L436,652", "Feeding pincer",
       fill=NONE, stroke="#9A6C36", strokeWidth=3.5, cap="round")

# --- major arm: the semaphore, raised right -------------------------------------------
# arm segments root → elbow → wrist
d.path("M568,560 C600,546 630,528 648,500 C658,484 664,468 664,452",
       "Major arm edge", fill=NONE, stroke="#2A1C0C", strokeWidth=17, cap="round")
d.path("M568,560 C600,546 630,528 648,500 C658,484 664,468 664,452",
       "Major arm", fill=NONE, stroke="#B8702E", strokeWidth=10, cap="round")

# --- the great claw: bulbous manus + fixed finger down, dactyl raised -----------------
d.path("M664,340 C700,334 736,352 754,384 C768,410 768,440 754,462 "
       "C744,478 726,488 706,488 C682,488 660,476 646,456 "
       "C632,436 630,406 640,382 C648,362 652,344 664,340 Z",
       "Major claw", fill=CLAW_GRAD, stroke=INK, strokeWidth=6)
# fixed finger pointing down-forward from the palm
d.path("M652,452 C640,478 638,506 648,524 C654,534 668,536 676,528 "
       "C684,518 686,498 682,478 C678,462 666,452 652,452 Z",
       "Fixed finger", fill="#D8722A", stroke=INK, strokeWidth=5)
# dactyl raised up and open — the wave
d.path("M712,340 C724,318 742,302 762,296 C774,292 786,296 790,306 "
       "C794,318 788,332 776,342 C762,354 742,360 724,358 "
       "C714,354 708,348 712,340 Z",
       "Dactyl", fill="#F2B25C", stroke=INK, strokeWidth=5)
# claw sheen + finger ridge + pale tips
d.shape("ellipse", "Claw sheen", x=662, y=366, width=52, height=34,
        fill="#FAD49A", opacity=35, stroke=NONE)
d.path("M652,470 C646,490 646,510 652,524", "Finger ridge",
       fill=NONE, stroke="#8A4210", strokeWidth=3.5, opacity=70, cap="round")
d.shape("ellipse", "Dactyl tip", x=774, y=300, width=14, height=10,
        fill="#F8DCA8", opacity=80, stroke=NONE)
# manus bumps — the claw is not smooth
for i, (x, y, w) in enumerate([(668,400,10),(700,382,9),(724,410,9),(690,442,8),(736,436,8)]):
    d.shape("ellipse", f"Claw bump {i+1}", x=x, y=y, width=w, height=w*0.7,
            fill="#B85E1E", opacity=55, stroke=NONE)

# --- carapace: squarish dome, narrower at the front ------------------------------------
d.path("M400,520 C398,492 404,466 428,452 C446,441 554,441 572,452 "
       "C596,466 602,492 600,520 C598,552 584,580 550,592 "
       "C516,602 484,602 450,592 C416,580 402,552 400,520 Z",
       "Carapace", fill=CARA_GRAD, stroke=INK, strokeWidth=6)
# shell sheen + rear shade + mottle
d.shape("ellipse", "Carapace sheen", x=438, y=462, width=124, height=52,
        fill="#A8CCC0", opacity=25, stroke=NONE)
d.path("M420,556 C450,584 550,584 580,556 C560,592 440,592 420,556 Z",
       "Rear shade", fill="#122620", opacity=45, stroke=NONE)
for i, (x, y, w) in enumerate([(452,500,14),(512,486,12),(552,514,11),(486,540,13),
                               (538,556,10),(450,552,10),(500,470,9)]):
    d.shape("ellipse", f"Shell mottle {i+1}", x=x, y=y, width=w, height=w*0.6,
            fill="#1C3A32", opacity=40, stroke=NONE)
# pale speckles — the species' blue-white flecking
for i, (x, y, w) in enumerate([(462,488,5),(524,498,5),(548,530,4),(478,520,4),
                               (508,560,5),(556,486,4),(438,534,4)]):
    d.shape("ellipse", f"Speckle {i+1}", x=x, y=y, width=w, height=w,
            fill="#9ECCC8", opacity=60, stroke=NONE)
# front lip between the eyestalks
d.path("M460,452 C476,444 524,444 540,452 C526,462 474,462 460,452 Z",
       "Front lip", fill="#1E3A32", stroke=NONE)

# --- eyestalks: long, close-set, clubbed eyes -----------------------------------------
for s, ex in ((-1, 462), (1, 538)):
    d.path(f"M{ex},{452} C{ex-2*s},{424} {ex-2*s},{404} {ex},{388}",
           f"Stalk {'L' if s<0 else 'R'} edge", fill=NONE,
           stroke="#2A1C0C", strokeWidth=10, cap="round")
    d.path(f"M{ex},{452} C{ex-2*s},{424} {ex-2*s},{404} {ex},{388}",
           f"Stalk {'L' if s<0 else 'R'}", fill=NONE,
           stroke="#7A6A44", strokeWidth=5.5, cap="round")
    d.shape("ellipse", f"Eye {'L' if s<0 else 'R'}", x=ex-9, y=374,
            width=18, height=17, fill="#181008", stroke=INK, strokeWidth=2.5)
    d.shape("ellipse", f"Eye glint {'L' if s<0 else 'R'}", x=ex-4, y=378,
            width=5, height=5, fill="#F4ECC8", opacity=85, stroke=NONE)

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#2E2818", strokeWidth=6)

# --- name ----------------------------------------------------------------------------
d.text("FIDDLER CRAB", "Name", x=500, y=962, size=58, font="Virelai Sans",
       color="#EDE2B8", justify="center")

d.finish("fiddler-crab-V1R00")
