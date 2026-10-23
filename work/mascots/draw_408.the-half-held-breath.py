#!/usr/bin/env python3
"""The Half-Held Breath — mascot portrait V1R00.
Empty corridor, door slightly ajar, terminal log ending at "connected—".
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("The Half-Held Breath — Mascot Portrait", 1000, 1000)

INK = "#332A33"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#0E181D"}, {"offset": 1, "color": "#04090C"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#3A5760"}, {"offset": 0.7, "color": "#25404A"},
    {"offset": 1, "color": "#15262D"}]}}
WALL_L = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2C4750"}, {"offset": 1, "color": "#1C3038"}]}}
WALL_R = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#16262D"}, {"offset": 1, "color": "#243B44"}]}}
FLOOR = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#22363F"}, {"offset": 1, "color": "#0F1D23"}]}}
LIGHT = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F5CE7E"}, {"offset": 1, "color": "#B57E3D"}]}}
DOOR = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4C3A28"}, {"offset": 1, "color": "#2E2118"}]}}
WISP = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#EAF7F5"}, {"offset": 0.7, "color": "#A8D4D6"},
    {"offset": 1, "color": "#6FA8AE"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#50808A", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8EFEA", strokeWidth=3, opacity=55)
# plate patina speckles
for i, (x, y, w) in enumerate([(190,240,8),(800,230,7),(160,520,9),(830,540,8),
                               (240,760,7),(760,740,9),(130,390,6),(865,390,7),
                               (390,110,7),(610,110,8),(330,820,6),(665,815,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#3E646E", opacity=45, stroke=NONE)

# --- corridor (near frame corners sit just inside the plate rim) --------------
# near frame F=(226,168)-(774,752), back wall B=(400,320)-(600,540), VP ~(500,430)
d.path("M226,168 L774,168 L600,320 L400,320 Z", "Ceiling", fill="#16252C", stroke=NONE)
d.path("M226,168 L400,320 L400,540 L226,752 Z", "Wall L", fill=WALL_L, stroke=NONE)
d.path("M774,168 L600,320 L600,540 L774,752 Z", "Wall R", fill=WALL_R, stroke=NONE)
d.path("M226,752 L774,752 L600,540 L400,540 Z", "Floor", fill=FLOOR, stroke=NONE)
d.shape("rectangle", "Back wall", x=400, y=320, width=200, height=220,
        fill="#213741", stroke=NONE)
# floor seams converging to VP
for i, (x1, y1) in enumerate([(330,752),(435,752),(565,752),(670,752)]):
    x0 = 500 + (x1-500)*0.32
    d.path(f"M{x1},{y1} L{x0:.0f},540", f"Floor seam {i+1}",
           fill=NONE, stroke="#0C181D", strokeWidth=3, opacity=60)
# skirting lines
d.path("M226,700 L400,505", "Skirt L", fill=NONE, stroke="#3C5A64", strokeWidth=4, opacity=70)
d.path("M774,700 L600,505", "Skirt R", fill=NONE, stroke="#3C5A64", strokeWidth=4, opacity=70)

# --- door, slightly ajar, light spilling --------------------------------------
# lit interior behind the slab
d.shape("rectangle", "Doorway light", x=452, y=352, width=96, height=188,
        fill=LIGHT, stroke=NONE)
# light wedge on the floor (translucent)
d.path("M455,540 L545,540 L620,700 L390,700 Z", "Light wedge",
       fill="#F0C878", opacity=18, stroke=NONE)
d.path("M470,540 L530,540 L575,660 L430,660 Z", "Light wedge core",
       fill="#F7DB9A", opacity=16, stroke=NONE)
# door frame
d.path("M445,348 L445,540 M445,348 L555,348 M555,348 L555,540", "Door frame",
       fill=NONE, stroke=INK, strokeWidth=7)
# door slab ajar: hinge at left edge, free edge swung toward viewer-left
d.path("M445,352 L405,378 L405,560 L445,540 Z", "Door slab",
       fill=DOOR, stroke=INK, strokeWidth=5, join="round")
# slab edge highlight + peephole dot
d.path("M405,378 L405,560", "Slab edge light", fill=NONE, stroke="#F5CE7E",
       strokeWidth=3, opacity=70)
d.shape("ellipse", "Knob", x=411, y=460, width=9, height=9, fill="#E8C57F", stroke=NONE)

# --- the wisp: a held breath --------------------------------------------------
d.shape("ellipse", "Wisp glow", x=455, y=400, width=190, height=170,
        fill="#BFEFEA", opacity=12, stroke=NONE)
# wispy tail curls
d.path("M540,560 C560,600 535,625 555,650 C568,668 560,690 542,696",
       "Wisp tail", fill=NONE, stroke=WISP, strokeWidth=16, cap="round", opacity=75)
d.path("M505,558 C490,592 512,612 498,640",
       "Wisp tail 2", fill=NONE, stroke="#9CCFCF", strokeWidth=10, cap="round", opacity=60)
# body: a held puff of air
d.path("M545,448 C600,448 640,486 640,520 C640,556 600,578 545,578 "
       "C490,578 452,556 452,520 C452,486 492,448 545,448 Z",
       "Wisp body", fill=WISP, stroke=INK, strokeWidth=6, opacity=95)
# top highlight + under-shadow
d.shape("ellipse", "Wisp highlight", x=492, y=458, width=110, height=34,
        fill="#FFFFFF", opacity=22, stroke=NONE)
d.path("M490,566 C525,576 575,576 606,564 C575,572 522,572 490,566 Z",
       "Wisp shadow", fill="#5E939B", opacity=45, stroke=NONE)
# face: held breath — squeezed-shut eyes, puffed cheeks, small flat mouth
d.path("M492,500 C498,508 510,508 516,500", "Eye L shut", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
d.path("M574,500 C580,508 592,508 598,500", "Eye R shut", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
d.shape("ellipse", "Cheek L", x=470, y=516, width=30, height=18,
        fill="#EFB9B4", opacity=55, stroke=NONE)
d.shape("ellipse", "Cheek R", x=592, y=516, width=30, height=18,
        fill="#EFB9B4", opacity=55, stroke=NONE)
d.path("M530,536 L560,536", "Held mouth", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
# two tiny escaped puffs
d.shape("ellipse", "Puff 1", x=620, y=430, width=16, height=12,
        fill="#D8EFEA", opacity=60, stroke=NONE)
d.shape("ellipse", "Puff 2", x=648, y=406, width=11, height=9,
        fill="#D8EFEA", opacity=45, stroke=NONE)

# --- terminal session log, ending "connected—" ---------------------------------
d.shape("rectangle", "Terminal", x=272, y=580, width=180, height=118,
        fill="#0A1A20", stroke="#3C5A64", strokeWidth=4, opacity=92, radius=8)
loglines = ["$ ssh archive", "user: breath", "pass: ••••••", "handshake ok", "connected—"]
for i, t in enumerate(loglines):
    bright = (i == len(loglines)-1)
    d.text(t, f"Log {i+1}", x=284, y=606 + i*19, size=13, font="Virelai Sans",
           color="#A8DED8" if bright else "#5E9490", justify="left")
d.shape("rectangle", "Cursor", x=356, y=676, width=10, height=13,
        fill="#CFF2EA", opacity=90, stroke=NONE)

# --- captions ------------------------------------------------------------------
d.text("THE HALF-HELD BREATH", "Name", x=500, y=930, size=56, font="Virelai Sans",
       color="#CDE7E4", justify="center")
r = d.text("KEEPER OF LOST SESSIONS", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#93BCB7", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("408.the-half-held-breath-V1R00")
