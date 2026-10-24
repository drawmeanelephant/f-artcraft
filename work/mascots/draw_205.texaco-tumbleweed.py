#!/usr/bin/env python3
"""Texaco Tumbleweed — mascot portrait V1R00.
Spectral mascot drifting through the rusted pumps of a crumbling
station, neon sign flickering. 1000x1000. House style: gradients +
translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Texaco Tumbleweed — Mascot Portrait", 1000, 1000)

INK = "#22302A"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#0E1210"}, {"offset": 1, "color": "#060A08"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#3A4E42"}, {"offset": 0.7, "color": "#24342B"},
    {"offset": 1, "color": "#121C16"}]}}
GHOST = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#EAF6EE"}, {"offset": 0.65, "color": "#B4D4C6"},
    {"offset": 1, "color": "#7AA394"}]}}
PUMP = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#54655A"}, {"offset": 1, "color": "#33403A"}]}}
RUST = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#8A4A30"}, {"offset": 1, "color": "#5A2E1E"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#C9A86A", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C9DCCB", strokeWidth=3, opacity=50)
for i, (x, y, w) in enumerate([(190,240,8),(800,230,7),(160,520,9),(830,540,8),
                               (240,760,7),(760,740,9),(130,390,6),(865,390,7),
                               (390,110,7),(610,110,8),(330,820,6),(665,815,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#4A5E50", opacity=45, stroke=NONE)

# --- dead canopy band across the top of the scene --------------------------------
d.path("M200,340 L800,320 L800,368 L200,388 Z", "Canopy fascia",
       fill="#2A3830", stroke=INK, strokeWidth=5, opacity=85, join="round")
d.path("M200,352 L800,332", "Fascia rust streak", fill=NONE,
       stroke="#6A3423", strokeWidth=4, opacity=50)
# hanging dead wires
d.path("M330,385 C332,420 324,450 330,480", "Wire 1", fill=NONE,
       stroke=INK, strokeWidth=4, opacity=70, cap="round")
d.path("M660,372 C664,400 656,428 662,452", "Wire 2", fill=NONE,
       stroke=INK, strokeWidth=4, opacity=70, cap="round")

# --- flickering neon sign on the fascia -------------------------------------------
d.shape("ellipse", "Neon halo", x=380, y=270, width=240, height=110,
        fill="#7EDCCB", opacity=12, stroke=NONE)
d.shape("rectangle", "Sign panel", x=372, y=288, width=256, height=66,
        fill="#16201B", stroke=INK, strokeWidth=5, radius=10)
d.text("G", "Neon G lit", x=420, y=336, size=44, font="Virelai Sans",
       color="#9FF2DC", justify="center")
d.shape("ellipse", "G halo", x=392, y=296, width=58, height=58,
        fill="#7EDCCB", opacity=22, stroke=NONE)
d.text("A", "Neon A flicker", x=500, y=336, size=44, font="Virelai Sans",
       color="#5A9684", justify="center")
d.text("S", "Neon S dead", x=580, y=336, size=44, font="Virelai Sans",
       color="#33473E", justify="center")

# --- ground: cracked asphalt --------------------------------------------------------
d.shape("ellipse", "Ground shadow", x=180, y=690, width=640, height=70,
        fill="#050B08", opacity=60, stroke=NONE)
for i, (x0, y0, x1, y1) in enumerate([(260,712,310,720),(420,722,470,714),
                                      (580,716,640,724),(700,706,750,714)]):
    d.path(f"M{x0},{y0} L{x1},{y1}", f"Crack {i+1}", fill=NONE,
           stroke=INK, strokeWidth=3, opacity=45)
# puddle of spilled spectral light
d.shape("ellipse", "Spectral puddle", x=400, y=700, width=240, height=30,
        fill="#9FD8C4", opacity=14, stroke=NONE)

# --- left pump husk, leaning ---------------------------------------------------------
d.path("M196,520 C196,502 210,492 232,492 C254,492 268,502 268,520 L274,694 L202,694 Z",
       "Pump left", fill=PUMP, stroke=INK, strokeWidth=5, join="round")
d.shape("ellipse", "Dial left", x=212, y=534, width=44, height=44,
        fill="#2A3830", stroke=INK, strokeWidth=4)
d.path("M234,556 L224,546", "Dead needle L", fill=NONE, stroke="#6A7A70",
       strokeWidth=3, cap="round")
# rust bleeding down
for i, (x, y, h) in enumerate([(208,560,60),(248,552,84),(226,584,44)]):
    d.path(f"M{x},{y} L{x-2},{y+h}", f"Rust streak L{i+1}", fill=NONE,
           stroke="#7A3E26", strokeWidth=5, opacity=45, cap="round")
d.shape("ellipse", "Rust bloom L", x=200, y=640, width=70, height=54,
        fill="#7A3E26", opacity=25, stroke=NONE)
# torn hose dangling
d.path("M268,560 C296,570 300,610 286,640", "Hose L", fill=NONE,
       stroke=INK, strokeWidth=8, cap="round", opacity=85)

# --- right pump husk, tilted ----------------------------------------------------------
d.path(rot_rect_path(772, 580, 76, 200, -4), "Pump right",
       fill=PUMP, stroke=INK, strokeWidth=5, join="round")
d.shape("ellipse", "Dial right", x=744, y=510, width=44, height=44,
        fill="#2A3830", stroke=INK, strokeWidth=4)
d.path("M766,532 L778,522", "Dead needle R", fill=NONE, stroke="#6A7A70",
       strokeWidth=3, cap="round")
for i, (x, y, h) in enumerate([(742,540,70),(786,548,54),(764,576,60)]):
    d.path(f"M{x},{y} L{x-1},{y+h}", f"Rust streak R{i+1}", fill=NONE,
           stroke="#7A3E26", strokeWidth=5, opacity=45, cap="round")
d.shape("ellipse", "Rust bloom R", x=738, y=636, width=80, height=56,
        fill="#7A3E26", opacity=25, stroke=NONE)
# snapped hose trailing on the ground
d.path("M806,640 C830,660 826,690 800,700 C780,706 762,700 758,690",
       "Hose R", fill=NONE, stroke=INK, strokeWidth=8, cap="round", opacity=85)

# --- tumbleweed rolling in from the right ----------------------------------------------
for i, (cx, cy, r, a0, a1) in enumerate([(736,672,34,0.2,4.9),(752,664,30,1.2,5.8),
                                          (724,676,32,2.4,6.9),(744,682,26,0.8,4.4),
                                          (736,662,30,3.4,7.0)]):
    d.path(f"M{cx-r},{cy} A{r},{r} 0 0 1 {cx+r*0.8:.0f},{cy-r*0.6:.0f}",
           f"Tumble arc {i+1}", fill=NONE, stroke="#8A6A44",
           strokeWidth=3, opacity=60, cap="round")
for i, (x0, y0, x1, y1) in enumerate([(716,660,760,686),(720,690,756,652),
                                      (712,674,764,672),(728,650,748,694)]):
    d.path(f"M{x0},{y0} L{x1},{y1}", f"Tumble twig {i+1}", fill=NONE,
           stroke="#7A5C3A", strokeWidth=2, opacity=55)

# --- the drifter ------------------------------------------------------------------------
d.shape("ellipse", "Ghost shadow", x=400, y=688, width=220, height=30,
        fill="#050B08", opacity=45, stroke=NONE)
# spectral halo
d.shape("ellipse", "Ghost halo", x=340, y=290, width=320, height=430,
        fill="#9FD8C4", opacity=10, stroke=NONE)
# sheet-ghost body: domed head, wavy trailing hem drifting left
d.path("M500,310 C432,310 398,368 398,448 C398,520 392,570 372,630 "
       "C392,618 402,646 420,624 C434,652 460,628 476,656 "
       "C492,630 516,654 534,628 C550,652 574,622 588,646 "
       "C606,626 620,600 616,560 C610,500 612,470 610,440 "
       "C606,362 568,310 500,310 Z",
       "Ghost body", fill=GHOST, stroke=INK, strokeWidth=5,
       opacity=92, join="round")
# inner glow core
d.shape("ellipse", "Ghost core", x=430, y=380, width=150, height=190,
        fill="#EAF6EE", opacity=30, stroke=NONE)
# hollow eyes + wistful mouth
d.shape("ellipse", "Eye L", x=452, y=420, width=26, height=34, fill="#16211B", stroke=NONE)
d.shape("ellipse", "Eye R", x=522, y=420, width=26, height=34, fill="#16211B", stroke=NONE)
d.shape("ellipse", "Eye glow L", x=452, y=420, width=26, height=34,
        fill=NONE, stroke="#9FD8C4", strokeWidth=2, opacity=60)
d.shape("ellipse", "Eye glow R", x=522, y=420, width=26, height=34,
        fill=NONE, stroke="#9FD8C4", strokeWidth=2, opacity=60)
d.shape("ellipse", "Mouth", x=482, y=486, width=32, height=26,
        fill="#16211B", stroke=NONE, opacity=90)
# wisp arms
d.path("M398,470 C366,478 348,500 344,528", "Arm L", fill=NONE,
       stroke="#B4D4C6", strokeWidth=20, cap="round", opacity=80)
d.path("M610,470 C640,484 656,510 654,540", "Arm R", fill=NONE,
       stroke="#B4D4C6", strokeWidth=20, cap="round", opacity=80)
# she passes through the left pump: faint edge of pump visible through her
d.path("M268,540 C300,560 320,600 318,650", "Pump through ghost",
       fill=NONE, stroke="#54655A", strokeWidth=8, opacity=30, cap="round")
# drifting wisps off her hem
d.path("M560,640 C600,650 640,640 668,616", "Wisp trail 1", fill=NONE,
       stroke="#9FD8C4", strokeWidth=6, opacity=30, cap="round")
d.path("M540,662 C580,676 626,668 654,644", "Wisp trail 2", fill=NONE,
       stroke="#9FD8C4", strokeWidth=4, opacity=22, cap="round")

# --- dust on the wind -------------------------------------------------------------------
for i, (x, y, w, o) in enumerate([(320,430,5,45),(360,520,4,40),(660,460,5,45),
                                  (700,540,4,35),(300,600,4,35),(680,610,5,40),
                                  (420,300,4,30),(580,280,4,30)]):
    d.shape("ellipse", f"Dust {i+1}", x=x, y=y, width=w, height=w,
            fill="#C9DCCB", opacity=o, stroke=NONE)

# --- captions ----------------------------------------------------------------------
d.text("TEXACO TUMBLEWEED", "Name", x=500, y=930, size=54, font="Virelai Sans",
       color="#E2EEE6", justify="center")
r = d.text("SPECTRAL DRIFTER", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#9FC4B2", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("205.texaco-tumbleweed-V1R00")
