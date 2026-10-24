#!/usr/bin/env python3
"""Bea Crashwell — mascot portrait V1R00.
Half-vanished speed queen beside a BeBox-era CRT at 3 a.m.: one perfect
frame still burning on the screen, every screenshot beside it blank.
1000x1000. Gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Bea Crashwell — Mascot Portrait", 1000, 1000)

INK = "#1E1C26"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#0B0D16"}, {"offset": 1, "color": "#05060B"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4E5C80"}, {"offset": 0.7, "color": "#364160"},
    {"offset": 1, "color": "#1D2438"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#272C42"}, {"offset": 1, "color": "#131728"}]}}
CASE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#CCC4B0"}, {"offset": 1, "color": "#8E8672"}]}}
SCREEN_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#10121C"}, {"offset": 1, "color": "#07080E"}]}}
FRAME_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#FFF2C4"}, {"offset": 0.55, "color": "#F0A85C"},
    {"offset": 1, "color": "#A8527C"}]}}
BEA_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E4DEF4"}, {"offset": 0.7, "color": "#B0A6D6"},
    {"offset": 1, "color": "#7E72AC"}]}}
GOLD = "#F0C040"
PAPER = "#EAE6DA"
PAPER_IN = "#B4B0A4"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#707AA0", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C4CEDE", strokeWidth=3, opacity=40)
for i, (x, y, w) in enumerate([(196,236,8),(804,238,7),(152,524,9),(844,544,8),
                               (252,770,7),(748,754,9),(132,392,6),(864,396,7),
                               (392,110,7),(614,112,8),(338,824,6),(664,822,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#46507A", opacity=50, stroke=NONE)

# --- wall clock stuck at 3 a.m. (hands only — no digits anywhere) --------------
d.shape("ellipse", "Clock", x=712, y=128, width=96, height=96,
        fill="#2C3350", stroke="#8E98BC", strokeWidth=5)
d.shape("ellipse", "Clock face", x=722, y=138, width=76, height=76,
        fill="#D8D4C8", stroke=NONE)
for i, (x, y, w) in enumerate([(756,146,6),(786,172,5),(788,196,5)]):
    d.shape("ellipse", f"Tick {i+1}", x=x, y=y, width=w, height=w,
            fill="#6A6480", opacity=70, stroke=NONE)
d.path("M760,176 L760,152", "Minute hand", fill=NONE, stroke="#3A3650",
       strokeWidth=5, cap="round")
d.path("M760,176 L782,176", "Hour hand", fill=NONE, stroke="#3A3650",
       strokeWidth=6, cap="round")
d.shape("ellipse", "Clock pin", x=755, y=171, width=10, height=10,
        fill="#3A3650", stroke=NONE)
# one weary spark of moonlight on the clock glass
d.path("M734,148 C744,140 760,138 772,142", "Clock glint", fill=NONE,
       stroke="#FFFFFF", strokeWidth=4, cap="round", opacity=40)

# --- floor: bottom segment closed on the disc's own arc -----------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#10121C",
       strokeWidth=4, opacity=70)
# the one frame's glow pooling on the floor in front of the set
d.path("M340,640 L560,640 L620,700 L280,700 Z", "Screen light pool",
       fill="#F0C060", opacity=10, stroke=NONE)

# --- the monitor: one perfect frame still on screen -----------------------------
d.shape("ellipse", "Monitor shadow", x=200, y=688, width=300, height=24,
        fill="#08080E", opacity=55, stroke=NONE)
d.shape("rectangle", "Monitor foot", x=330, y=616, width=40, height=60,
        fill="#8C8470", stroke=INK, strokeWidth=5)
d.path("M272,668 L428,668 L446,700 L254,700 Z", "Monitor base",
       fill=CASE_GRAD, stroke=INK, strokeWidth=5, join="round")
d.shape("rectangle", "Monitor body", x=185, y=296, width=310, height=310,
        fill=CASE_GRAD, stroke=INK, strokeWidth=7, radius=16)
for i, vx in enumerate([206, 218, 230]):
    d.path(f"M{vx},314 L{vx},338", f"Vent {i+1}", fill=NONE,
           stroke="#7E7662", strokeWidth=4, cap="round")
# bezel + the screen
d.shape("rectangle", "Screen", x=214, y=352, width=252, height=220,
        fill=SCREEN_GRAD, stroke="#171320", strokeWidth=6, radius=10)
# THE frame: a rendered sunrise, centered, still warm
d.shape("rectangle", "Rendered frame", x=244, y=382, width=192, height=128,
        fill=FRAME_GRAD, stroke="#F8E8C0", strokeWidth=4, radius=4)
d.path("M244,472 L436,472", "Frame horizon", fill=NONE, stroke="#8E4468",
       strokeWidth=3, opacity=70)
d.shape("ellipse", "Frame sun", x=312, y=416, width=56, height=56,
        fill="#FFF6DC", opacity=90, stroke=NONE)
d.path("M262,410 C268,403 276,403 282,410 C288,403 296,403 302,410 "
       "M384,398 C390,391 398,391 404,398 C410,391 418,391 424,398",
       "Frame gulls", fill=NONE, stroke="#6E3A5C", strokeWidth=3,
       cap="round", opacity=80)
# glow halo around the frame on the dark screen
d.shape("ellipse", "Frame glow", x=224, y=362, width=232, height=168,
        fill="#F0B060", opacity=12, stroke=NONE)
# scanlines — the cycle she never survives
for i, sy in enumerate([400, 452, 504, 556]):
    d.path(f"M218,{sy} L462,{sy}", f"Scanline {i+1}", fill=NONE,
           stroke="#FFFFFF", strokeWidth=1.5, opacity=5)
d.shape("ellipse", "Power LED", x=452, y=580, width=10, height=10,
        fill=GOLD, stroke=INK, strokeWidth=2)
d.shape("ellipse", "LED glow", x=446, y=574, width=22, height=22,
        fill=GOLD, opacity=20, stroke=NONE)

# --- blank screenshots: the proof that never came -------------------------------
for i, (cx, cy, deg) in enumerate([(530,668,-8),(586,672,6),(548,694,-3),
                                   (646,680,12),(692,688,-10)]):
    d.path(rot_rect_path(cx, cy, 64, 48, deg), f"Blank shot {i+1}",
           fill=PAPER, stroke=INK, strokeWidth=3, join="round")
    # empty grey window where the image should be
    d.path(rot_rect_path(cx, cy-2, 48, 32, deg), f"Shot void {i+1}",
           fill=PAPER_IN, stroke=NONE, opacity=70)
# one still pinned to the monitor's flank, equally blank
d.path(rot_rect_path(492, 470, 62, 46, 6), "Pinned shot",
       fill=PAPER, stroke=INK, strokeWidth=3, join="round")
d.path(rot_rect_path(492, 468, 46, 30, 6), "Pinned void",
       fill=PAPER_IN, stroke=NONE, opacity=70)

# --- Bea Crashwell: present for exactly one frame --------------------------------
d.shape("ellipse", "Bea glow", x=560, y=380, width=300, height=340,
        fill="#B0A6D6", opacity=8, stroke=NONE)
# body: a trim upright figure, solid to the waist
d.path("M686,318 C752,318 800,372 800,448 C800,500 778,532 760,556 "
       "C744,574 736,586 730,606 L642,606 C636,586 628,574 612,556 "
       "C594,532 572,500 572,448 C572,372 620,318 686,318 Z",
       "Bea body", fill=BEA_GRAD, stroke=INK, strokeWidth=6)
d.shape("ellipse", "Body hi", x=608, y=352, width=90, height=54,
        fill="#FFFFFF", opacity=16, stroke=NONE)
# below the waist she is already a rumor: translucent tail + dissolving pixels
d.path("M642,600 L730,600 C726,626 720,646 712,664 "
       "C700,656 692,672 682,664 C672,656 664,674 654,664 "
       "C646,656 642,630 642,600 Z",
       "Fading tail", fill=BEA_GRAD, stroke="#4A4468", strokeWidth=4,
       opacity=38, join="round")
for i, (x, y, s, o) in enumerate([(642,676,10,30),(676,690,8,24),
                                  (706,672,9,28),(658,712,7,18),
                                  (694,718,6,14),(630,700,6,16),
                                  (720,700,8,20),(668,652,7,26)]):
    d.shape("rectangle", f"Vanish pixel {i+1}", x=x, y=y, width=s, height=s,
            fill="#B0A6D6", opacity=o, stroke=NONE)
# scanlines where she used to be
for i, sy in enumerate([614, 644]):
    d.shape("rectangle", f"Afterline {i+1}", x=620, y=sy, width=140,
            height=5, fill="#D8D2EE", opacity=12, stroke=NONE)
# lightning cowl: the bolt she was named for
d.path("M686,296 L668,332 L690,332 L664,376 L716,326 L692,326 L706,296 Z",
       "Lightning cowl", fill=GOLD, stroke=INK, strokeWidth=4,
       join="round")
# eyes: closed mid-blink — she only ever sees one frame
d.path("M630,436 C640,426 656,426 666,436", "Eye L", fill=NONE,
       stroke=INK, strokeWidth=6, cap="round")
d.path("M706,436 C716,426 732,426 742,436", "Eye R", fill=NONE,
       stroke=INK, strokeWidth=6, cap="round")
# the small satisfied smile of undocumented victory
d.path("M668,472 C680,482 694,482 706,472", "Smile", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
d.shape("ellipse", "Cheek L", x=618, y=452, width=26, height=13,
        fill="#C08AB0", opacity=40, stroke=NONE)
d.shape("ellipse", "Cheek R", x=730, y=452, width=26, height=13,
        fill="#C08AB0", opacity=40, stroke=NONE)
# arm extended to the screen: the touch that made the frame
d.path("M580,480 C556,478 540,470 522,458", "Arm reach", fill=NONE,
       stroke="#A89ED0", strokeWidth=16, cap="round")
d.shape("ellipse", "Hand", x=506, y=446, width=26, height=22,
        fill="#C6BEE4", stroke=INK, strokeWidth=4)
# the spark where finger met frame
d.path("M496,440 L488,424 M496,440 L480,438 M496,440 L490,456 "
       "M496,440 L506,428 M496,440 L508,452", "Render spark",
       fill=NONE, stroke=GOLD, strokeWidth=4, cap="round")
d.shape("ellipse", "Spark core", x=490, y=434, width=12, height=12,
        fill="#FFF2C4", opacity=90, stroke=NONE)

# --- captions ---------------------------------------------------------------------
d.text("BEA CRASHWELL", "Name", x=500, y=930, size=58,
       font="Virelai Sans", color="#EAE4F2", justify="center")
r = d.text("MULTIMEDIA SPEED QUEEN", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#A8A0C8", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("026.bea-crashwell-V1R00")
