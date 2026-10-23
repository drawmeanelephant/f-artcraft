#!/usr/bin/env python3
"""The Quiet Injunction — mascot portrait V1R00.
Robed mascot drawing a curtain over a shelf; the filing stub remains and a
document stands stamped UNAVAILABLE. 1000x1000. House style: gradients +
translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("The Quiet Injunction — Mascot Portrait", 1000, 1000)

INK = "#2A1E26"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1A0F16"}, {"offset": 1, "color": "#0A0508"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#5E3A50"}, {"offset": 0.7, "color": "#3A2434"},
    {"offset": 1, "color": "#221420"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#38222F"}, {"offset": 1, "color": "#1A1018"}]}}
CURTAIN = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#8A3A4C"}, {"offset": 1, "color": "#4E1E2A"}]}}
ROBE = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#54456E"}, {"offset": 0.75, "color": "#3A2E52"},
    {"offset": 1, "color": "#262040"}]}}
PARCHMENT = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#EFE2C2"}, {"offset": 1, "color": "#CDB98E"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#7A5670", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E4CEDC", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(192,235,8),(800,232,7),(156,525,9),(838,545,8),
                               (245,765,7),(755,748,9),(132,393,6),(866,390,7),
                               (390,112,7),(612,110,8),(334,822,6),(664,820,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#50304A", opacity=45, stroke=NONE)

# --- floor: bottom segment closed on the disc's own arc -----------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#140C14",
       strokeWidth=4, opacity=70)

# --- the shelf being censored ---------------------------------------------------
d.shape("rectangle", "Shelf board", x=455, y=215, width=330, height=18,
        fill="#4A3428", stroke=INK, strokeWidth=4, radius=4)
d.shape("rectangle", "Shelf board 2", x=455, y=395, width=330, height=18,
        fill="#4A3428", stroke=INK, strokeWidth=4, radius=4)
# books on the upper shelf (left part stays visible)
for i, (x, w, h, c) in enumerate([(470,26,120,"#6A4A58"),(500,22,108,"#4A5A68"),
                                  (526,30,124,"#7A5A3E"),(560,24,110,"#5E6A4A"),
                                  (588,26,118,"#6A3E46"),(618,22,104,"#54607A")]):
    d.shape("rectangle", f"Book {i+1}", x=x, y=215-h+14, width=w, height=h,
            fill=c, stroke=INK, strokeWidth=3, radius=2)
    d.shape("rectangle", f"Book band {i+1}", x=x, y=215-h+34, width=w, height=6,
            fill="#E8DCC0", opacity=35, stroke=NONE)
# lower shelf: a few visible books left, then the curtain takes over
for i, (x, w, h, c) in enumerate([(468,24,110,"#54607A"),(496,28,118,"#7A5A3E"),
                                  (528,22,100,"#6A4A58")]):
    d.shape("rectangle", f"Low book {i+1}", x=x, y=395-h+12, width=w, height=h,
            fill=c, stroke=INK, strokeWidth=3, radius=2)

# --- curtain rod + the drawn curtain ---------------------------------------------
d.path("M445,190 L780,190", "Rod", fill=NONE, stroke="#8A6A42",
       strokeWidth=8, cap="round")
d.shape("ellipse", "Finial L", x=437, y=182, width=16, height=16,
        fill="#B08A52", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Finial R", x=762, y=182, width=16, height=16,
        fill="#B08A52", stroke=INK, strokeWidth=3)
# curtain: drawn from the right, scalloped leading edge stops mid-shelf
d.path("M612,196 L770,196 L770,470 "
       "C745,455 728,475 706,460 C685,448 660,470 640,458 "
       "C625,450 612,462 606,452 Z",
       "Curtain", fill=CURTAIN, stroke=INK, strokeWidth=5)
# fold lines following the gathers
for i, (x0, sway) in enumerate([(640,-8),(668,6),(700,-6),(734,8),(758,-4)]):
    d.path(f"M{x0},210 C{x0+sway},290 {x0-sway},360 {x0+sway//2},440",
           f"Fold {i+1}", fill=NONE, stroke="#3A1420", strokeWidth=4,
           opacity=55)
# gathered top
for i in range(6):
    x = 616 + i*26
    d.path(f"M{x},196 C{x+8},206 {x+14},206 {x+20},196", f"Gather {i+1}",
           fill=NONE, stroke="#3A1420", strokeWidth=3, opacity=50)
# filing stub left behind on the shelf edge
d.path("M596,316 L640,316 L640,368 L630,368 L630,376 L606,376 L606,368 L596,368 Z",
       "Filing stub", fill="#E0CFA2", stroke=INK, strokeWidth=4, join="round")
d.text("451-A", "Stub label", x=605, y=350, size=12, font="Virelai Sans",
       color="#5E4A2E", justify="left")
# pull cord down to the mascot's hand
d.path("M610,455 C560,500 500,520 452,540", "Pull cord", fill=NONE,
       stroke="#C9A86A", strokeWidth=4, cap="round")
d.shape("ellipse", "Cord ring", x=600, y=444, width=18, height=18,
        fill=NONE, stroke="#C9A86A", strokeWidth=4)
d.shape("ellipse", "Cord tassel", x=444, y=532, width=16, height=22,
        fill="#C9A86A", stroke=INK, strokeWidth=3)

# --- the stamped document on its stand -------------------------------------------
d.path("M655,640 L640,700 M655,640 L670,700", "Easel legs", fill=NONE,
       stroke="#4A3428", strokeWidth=6, cap="round")
d.shape("rectangle", "Easel board", x=590, y=505, width=140, height=140,
        fill="#5E4A38", stroke=INK, strokeWidth=5, radius=6)
d.shape("rectangle", "Document", x=602, y=517, width=116, height=116,
        fill=PARCHMENT, stroke=INK, strokeWidth=3)
for i, w in enumerate([92, 92, 70, 92]):
    d.shape("rectangle", f"Doc line {i+1}", x=614, y=532+i*15, width=w, height=5,
            fill="#8A7A5E", opacity=55, stroke=NONE)
# red UNAVAILABLE stamp across the middle
d.shape("rectangle", "Stamp box", x=607, y=586, width=106, height=30,
        fill=NONE, stroke="#B03A3E", strokeWidth=4, radius=4)
d.text("UNAVAILABLE", "Stamp text", x=613, y=606, size=13, font="Virelai Sans",
       color="#B03A3E", justify="left")

# --- the mascot: a robed, hooded clerk --------------------------------------------
d.shape("ellipse", "Mascot shadow", x=290, y=685, width=220, height=30,
        fill="#120812", opacity=50, stroke=NONE)
# robe body
d.path("M400,470 C470,470 505,540 505,630 C505,690 460,712 400,712 "
       "C340,712 295,690 295,630 C295,540 330,470 400,470 Z",
       "Robe body", fill=ROBE, stroke=INK, strokeWidth=6)
# robe folds
d.path("M350,560 C355,610 350,660 345,695", "Robe fold L", fill=NONE,
       stroke="#241C3A", strokeWidth=5, opacity=60)
d.path("M450,560 C445,610 450,660 455,695", "Robe fold R", fill=NONE,
       stroke="#241C3A", strokeWidth=5, opacity=60)
# hood + shadowed face
d.path("M330,480 C330,415 360,385 400,385 C440,385 470,415 470,480 "
       "C470,505 440,515 400,515 C360,515 330,505 330,480 Z",
       "Hood", fill="#2E2448", stroke=INK, strokeWidth=6)
d.shape("ellipse", "Face shadow", x=355, y=430, width=90, height=70,
        fill="#171226", stroke=NONE, opacity=85)
# calm bound eyes, no mouth — silence
d.path("M368,465 C374,471 383,471 389,465", "Eye L", fill=NONE,
       stroke="#C9A86A", strokeWidth=5, cap="round")
d.path("M411,465 C417,471 426,471 432,465", "Eye R", fill=NONE,
       stroke="#C9A86A", strokeWidth=5, cap="round")
# arm raised holding the cord
d.path("M495,560 C500,545 480,540 458,540", "Arm raised", fill=NONE,
       stroke="#3A2E52", strokeWidth=17, cap="round")

# --- captions ------------------------------------------------------------------
d.text("THE QUIET INJUNCTION", "Name", x=500, y=930, size=54, font="Virelai Sans",
       color="#E4CEDC", justify="center")
r = d.text("LEGAL CENSORSHIP ENTITY", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#B08AA0", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("451.the-quiet-injunction-V1R00")
