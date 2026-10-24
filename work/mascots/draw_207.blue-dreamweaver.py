#!/usr/bin/env python3
"""Blue Dreamweaver — mascot portrait V1R00.
A spectral weaver adrift above the medical-record shelves, spinning
berry-scented mist into a small glowing dreamweb between its hands.
1000x1000. Gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Blue Dreamweaver — Mascot Portrait", 1000, 1000)

INK = "#2A2038"
BG_GRAD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000], "stops": [
    {"offset": 0, "color": "#0C1020"}, {"offset": 1, "color": "#05070F"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#46527E"}, {"offset": 0.7, "color": "#2A3358"},
    {"offset": 1, "color": "#161C36"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "start": [0, 700], "end": [0, 880], "stops": [
    {"offset": 0, "color": "#232C4E"}, {"offset": 1, "color": "#0F1428"}]}}
SHELF = {"gradient": {"kind": "linear", "start": [0, 560], "end": [0, 700], "stops": [
    {"offset": 0, "color": "#2E3A66"}, {"offset": 1, "color": "#1A2244"}]}}
GHOST = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#CFE4FF"}, {"offset": 0.55, "color": "#8FA8E0"},
    {"offset": 1, "color": "#5A6EB4"}]}}
HOOD = {"gradient": {"kind": "linear", "start": [0, 250], "end": [0, 380], "stops": [
    {"offset": 0, "color": "#6A7EC4"}, {"offset": 1, "color": "#3E4C8E"}]}}
BERRY = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E08AB4"}, {"offset": 0.7, "color": "#B85C8A"},
    {"offset": 1, "color": "#7E3A62"}]}}
BERRY_B = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#9AA8F0"}, {"offset": 0.7, "color": "#6A7AE0"},
    {"offset": 1, "color": "#4450A8"}]}}
THREAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E0D4FF"}, {"offset": 1, "color": "#9A8AD8"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#7E8ABE", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C8D0F0", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(193,233,8),(801,230,7),(157,524,9),(837,544,8),
                               (247,766,7),(753,749,9),(133,393,6),(864,391,7),
                               (391,113,7),(613,110,8),(333,823,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#3E4A72", opacity=45, stroke=NONE)

# --- floor: bottom segment closed on the disc's own arc -----------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0A0E20",
       strokeWidth=4, opacity=70)

# --- spectral sparkles in the upper plate --------------------------------------
for i, (x, y, w, o) in enumerate([(250,180,5,60),(330,140,4,45),(670,150,5,55),
                                  (745,205,4,45),(210,300,4,40),(790,320,5,50),
                                  (420,120,3,40),(585,135,4,45)]):
    d.shape("ellipse", f"Sparkle {i+1}", x=x, y=y, width=w, height=w,
            fill="#D8E2FF", opacity=o, stroke=NONE)

# --- archive shelves: two rows of medical-record files --------------------------
# faint back row
for i, (x, w, h) in enumerate([(190,52,88),(252,60,104),(322,54,80),(586,58,96),
                               (654,52,84),(716,60,100),(262,0,0)]):
    if not w:
        continue
    d.shape("rectangle", f"Back file {i+1}", x=x, y=700-h-28, width=w, height=h,
            fill=SHELF, stroke="#161D3C", strokeWidth=3, radius=6, opacity=65)
# shelf rail the back row sits on
d.shape("rectangle", "Back shelf rail", x=180, y=584, width=620, height=14,
        fill="#141B38", stroke=NONE, radius=4, opacity=80)
# front row: taller folders with tabs
for i, (x, w, h, tab) in enumerate([(205,64,128,1),(279,58,112,0),(764,60,120,1),
                                    (692,56,104,0),(166,56,96,1)]):
    d.shape("rectangle", f"File {i+1}", x=x, y=700-h, width=w, height=h,
            fill=SHELF, stroke=INK, strokeWidth=4, radius=7, opacity=92)
    if tab:
        d.shape("rectangle", f"File tab {i+1}", x=x+w-24, y=700-h-12, width=22,
                height=14, fill=SHELF, stroke=INK, strokeWidth=3, radius=4,
                opacity=92)
    # label line on each folder
    d.path(f"M{x+12},{700-h+34} L{x+w-12},{700-h+34}", f"File label {i+1}",
           fill=NONE, stroke="#8A9ACE", strokeWidth=3, opacity=55, cap="round")

# --- the spectral mascot ----------------------------------------------------------
# drifting shadow on the floor, no feet
d.shape("ellipse", "Wisp shadow", x=400, y=688, width=200, height=24,
        fill="#070B18", opacity=50, stroke=NONE)
# body: hooded wisp, rounded crown flowing to a scalloped hem
d.path("M500,252 C568,252 614,308 614,382 C614,442 596,486 566,522 "
       "C578,556 566,588 540,594 C520,600 512,584 500,584 "
       "C488,584 480,600 460,594 C434,588 422,556 434,522 "
       "C404,486 386,442 386,382 C386,308 432,252 500,252 Z",
       "Spectral body", fill=GHOST, stroke=INK, strokeWidth=6, join="round")
# hood: darker cowl sweeping over the crown
d.path("M500,252 C566,252 610,304 614,372 C580,332 546,318 500,318 "
       "C454,318 420,332 386,372 C390,304 434,252 500,252 Z",
       "Hood", fill=HOOD, stroke=INK, strokeWidth=5, join="round", opacity=95)
# hood peak lip
d.path("M438,318 C462,296 538,296 562,318", "Hood lip", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round", opacity=70)
# translucent body shading: cool shadow at the hem, moonlit core
d.shape("ellipse", "Body core glow", x=440, y=380, width=120, height=130,
        fill="#E8F2FF", opacity=20, stroke=NONE)
d.path("M434,522 C455,545 545,545 566,522 C552,566 448,566 434,522 Z",
       "Hem shadow", fill="#4A5CA8", opacity=35, stroke=NONE)
# wispy arms reaching out to the threads
d.path("M430,408 C404,428 384,444 372,462", "Arm L", fill=NONE,
       stroke=GHOST, strokeWidth=22, cap="round", opacity=90)
d.path("M570,408 C596,428 616,444 628,462", "Arm R", fill=NONE,
       stroke=GHOST, strokeWidth=22, cap="round", opacity=90)
# hand glows where the threads take off
d.shape("ellipse", "Hand glow L", x=358, y=452, width=28, height=22,
        fill="#D8CCFF", opacity=55, stroke=NONE)
d.shape("ellipse", "Hand glow R", x=614, y=452, width=28, height=22,
        fill="#D8CCFF", opacity=55, stroke=NONE)
# face inside the hood shadow: serene closed eyes + faint smile
d.path("M452,372 C460,380 472,380 480,372", "Eye L", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
d.path("M520,372 C528,380 540,380 548,372", "Eye R", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
d.path("M482,404 C492,412 508,412 518,404", "Smile", fill=NONE, stroke=INK,
       strokeWidth=4, cap="round", opacity=80)
# blush-lit cheeks, spectral style
d.shape("ellipse", "Cheek L", x=438, y=388, width=24, height=12,
        fill="#B85C8A", opacity=30, stroke=NONE)
d.shape("ellipse", "Cheek R", x=538, y=388, width=24, height=12,
        fill="#B85C8A", opacity=30, stroke=NONE)

# --- the dreamweb spun in front of the hem -----------------------------------------
d.path("M500,505 L395,568 M500,505 L450,582 M500,505 L550,582 M500,505 L605,568",
       "Web spokes", fill=NONE, stroke="#C9B8FF", strokeWidth=4, opacity=70,
       cap="round")
# scalloped cross-rows
d.path("M462,530 C478,540 522,540 538,530", "Web row 1", fill=NONE,
       stroke="#C9B8FF", strokeWidth=3, opacity=60, cap="round")
d.path("M432,552 C465,568 535,568 568,552", "Web row 2", fill=NONE,
       stroke="#C9B8FF", strokeWidth=3, opacity=55, cap="round")
# dewy berry beads caught on the web
d.shape("ellipse", "Web bead 1", x=381, y=554, width=14, height=14, fill=BERRY,
        stroke=INK, strokeWidth=2)
d.shape("ellipse", "Web bead 2", x=540, y=568, width=13, height=13, fill=BERRY_B,
        stroke=INK, strokeWidth=2)
d.shape("ellipse", "Web bead 3", x=438, y=569, width=12, height=12, fill=BERRY,
        stroke=INK, strokeWidth=2)
# threads running from the web knot up to each hand
for side, hx in (("L", 372), ("R", 628)):
    d.path(f"M500,505 C470,485 {hx+30},470 {hx},458", f"Glow strand {side}",
           fill=NONE, stroke=THREAD, strokeWidth=9, opacity=20, cap="round")
    d.path(f"M500,505 C470,485 {hx+30},470 {hx},458", f"Thread {side}",
           fill=NONE, stroke="#D8CCFF", strokeWidth=3, opacity=80, cap="round")

# --- berry-scented mist curling off the weave --------------------------------------
d.path("M560,560 C610,540 640,560 632,592 C626,616 596,618 592,598",
       "Mist curl R", fill=NONE, stroke="#C8B8F0", strokeWidth=8,
       opacity=30, cap="round")
d.path("M440,556 C396,540 364,562 374,592 C380,612 406,614 410,596",
       "Mist curl L", fill=NONE, stroke="#C8B8F0", strokeWidth=8,
       opacity=30, cap="round")
d.path("M614,340 C660,320 686,340 678,368", "Mist wisp upper", fill=NONE,
       stroke="#AFC8F0", strokeWidth=6, opacity=25, cap="round")
# berry clusters riding the mist
for name, (cx, cy), g in [("Berry A", (648,560), BERRY),
                          ("Berry B", (368,548), BERRY_B)]:
    for j, (dx, dy, r) in enumerate([(-10, 4, 9), (8, -6, 10), (10, 10, 8)]):
        d.shape("ellipse", f"{name} b{j+1}", x=cx+dx-r, y=cy+dy-r,
                width=2*r, height=2*r, fill=g, stroke=INK, strokeWidth=2)
    d.shape("ellipse", f"{name} shine", x=cx+2, y=cy-12, width=5, height=5,
            fill="#FFFFFF", opacity=70, stroke=NONE)

# --- captions ------------------------------------------------------------------
d.text("BLUE DREAMWEAVER", "Name", x=500, y=930, size=56, font="Virelai Sans",
       color="#D0DCF8", justify="center")
r = d.text("WEAVER OF BERRY-SCENTED MIST", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#9AA8D8", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("207.blue-dreamweaver-V1R00")
