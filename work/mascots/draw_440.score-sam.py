#!/usr/bin/env python3
"""Score Sam — mascot portrait V1R00.
Gatekeeper at the binary gate, paddle up showing the three-digit score.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Score Sam — Mascot Portrait", 1000, 1000)

INK = "#332A33"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#150F2C"}, {"offset": 1, "color": "#090617"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#574F88"}, {"offset": 0.7, "color": "#3B3462"},
    {"offset": 1, "color": "#201B3C"}]}}
STONE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6E6598"}, {"offset": 1, "color": "#453D70"}]}}
FLOOR = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3A3358"}, {"offset": 1, "color": "#1C1830"}]}}
BODY = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#C9CEEC"}, {"offset": 0.7, "color": "#9AA3D4"},
    {"offset": 1, "color": "#6E77AC"}]}}
UNIFORM = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4A5490"}, {"offset": 1, "color": "#2E3460"}]}}
AMBER = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F5CE7E"}, {"offset": 1, "color": "#C08A3C"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#7E74AE", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8D2EE", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(190,240,8),(800,230,7),(160,520,9),(830,540,8),
                               (240,760,7),(760,740,9),(130,390,6),(865,390,7),
                               (390,110,7),(610,110,8),(330,820,6),(665,815,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#474070", opacity=45, stroke=NONE)

# --- floor ---------------------------------------------------------------------
d.shape("ellipse", "Floor", x=170, y=620, width=660, height=135,
        fill=FLOOR, stroke=NONE, opacity=92)
d.shape("ellipse", "Sam shadow", x=390, y=676, width=160, height=30,
        fill="#080614", opacity=55, stroke=NONE)

# --- the binary gate ---------------------------------------------------------------
# light through the gateway
d.path("M400,640 L400,380 L600,380 L600,640 Z", "Gate light", fill="#F0C878",
       opacity=12, stroke=NONE)
d.path("M430,640 L430,420 L570,420 L570,640 Z", "Gate light core",
       fill="#F7DB9A", opacity=10, stroke=NONE)
# pillars: carved 0 and 1
d.shape("rectangle", "Pillar 0", x=298, y=300, width=96, height=348,
        fill=STONE, stroke=INK, strokeWidth=6, radius=12)
d.shape("rectangle", "Pillar 1", x=606, y=300, width=96, height=348,
        fill=STONE, stroke=INK, strokeWidth=6, radius=12)
d.text("0", "Digit 0", x=346, y=570, size=96, font="Virelai Sans",
       color="#2E284E", justify="center")
d.text("1", "Digit 1", x=654, y=570, size=96, font="Virelai Sans",
       color="#2E284E", justify="center")
# pillar caps + feet
for side, x in (("L", 290), ("R", 598)):
    d.shape("rectangle", f"Cap {side}", x=x, y=282, width=112, height=24,
            fill="#564E80", stroke=INK, strokeWidth=5, radius=6)
    d.shape("rectangle", f"Foot {side}", x=x, y=648, width=112, height=22,
            fill="#564E80", stroke=INK, strokeWidth=5, radius=6)
# lintel with threshold plaque
d.shape("rectangle", "Lintel", x=278, y=232, width=444, height=34,
        fill=STONE, stroke=INK, strokeWidth=6, radius=8)
d.shape("rectangle", "Threshold plaque", x=425, y=274, width=150, height=30,
        fill="#241E44", stroke="#7E74AE", strokeWidth=3, radius=5)
d.text("MIN SCORE 700", "Threshold", x=500, y=294, size=13,
       font="Virelai Sans", color="#C9BEEC", justify="center")
# turnstile bar between the pillars
d.path("M394,600 L606,600", "Turnstile", fill=NONE, stroke="#6E6598",
       strokeWidth=10, cap="round")
d.path("M394,600 L394,640 M606,600 L606,640", "Turnstile mounts", fill=NONE,
       stroke="#564E80", strokeWidth=8, cap="round")

# --- the small queue, waiting to be scored -----------------------------------------
for i, (x, y, s, o) in enumerate([(212,560,34,45),(252,586,26,35)]):
    d.shape("ellipse", f"Queue body {i+1}", x=x-s/2, y=y-s/2, width=s, height=s*1.2,
            fill="#4A4276", opacity=o+30, stroke=INK, strokeWidth=3)
    d.shape("ellipse", f"Queue eye {i+1}", x=x-4, y=y-6, width=7, height=9,
            fill="#14102A", opacity=o+40, stroke=NONE)

# --- Sam ----------------------------------------------------------------------------
# legs + boots
d.path("M446,640 L442,676", "Leg L", fill=NONE, stroke="#6E77AC",
       strokeWidth=13, cap="round")
d.path("M486,640 L490,676", "Leg R", fill=NONE, stroke="#5E67A0",
       strokeWidth=13, cap="round")
d.shape("ellipse", "Boot L", x=426, y=670, width=32, height=15, fill=INK, stroke=NONE)
d.shape("ellipse", "Boot R", x=478, y=670, width=32, height=15, fill=INK, stroke=NONE)
# body in a little uniform coat
d.path("M470,462 C524,462 548,508 545,556 C542,610 514,646 470,646 "
       "C426,646 396,610 393,556 C390,508 416,462 470,462 Z",
       "Sam body", fill=BODY, stroke=INK, strokeWidth=6)
# uniform coat front
d.path("M430,540 C436,596 452,626 470,646 C488,626 504,596 510,540 "
       "C494,552 446,552 430,540 Z",
       "Coat", fill=UNIFORM, stroke=INK, strokeWidth=4, join="round")
d.shape("ellipse", "Body highlight", x=414, y=476, width=70, height=26,
        fill="#FFFFFF", opacity=20, stroke=NONE)
# peaked cap
d.path("M428,452 L428,428 C428,410 446,402 470,402 C494,402 512,410 512,428 L512,452 Z",
       "Cap crown", fill=UNIFORM, stroke=INK, strokeWidth=5, join="round")
d.shape("ellipse", "Cap brim", x=418, y=444, width=104, height=16,
        fill="#242A52", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Cap badge", x=462, y=414, width=16, height=16,
        fill=AMBER, stroke=INK, strokeWidth=3)
# face: appraising squint, one brow up
d.shape("ellipse", "Eye L", x=438, y=492, width=15, height=19, fill=INK, stroke=NONE)
d.shape("ellipse", "Eye R", x=486, y=492, width=15, height=19, fill=INK, stroke=NONE)
d.shape("ellipse", "Glint L", x=442, y=496, width=4, height=4, fill="#FFFFFF", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=490, y=496, width=4, height=4, fill="#FFFFFF", opacity=90, stroke=NONE)
d.path("M434,474 L454,470", "Brow L", fill=NONE, stroke=INK, strokeWidth=4, cap="round")
d.path("M484,468 L504,472", "Brow R", fill=NONE, stroke=INK, strokeWidth=4, cap="round")
d.shape("ellipse", "Cheek L", x=422, y=518, width=24, height=14,
        fill="#C98A9A", opacity=50, stroke=NONE)
d.shape("ellipse", "Cheek R", x=498, y=518, width=24, height=14,
        fill="#C98A9A", opacity=50, stroke=NONE)
d.path("M454,540 C464,546 478,546 488,538", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
# free hand on hip
d.path("M398,560 C380,570 374,590 382,604", "Arm hip", fill=NONE,
       stroke="#9AA3D4", strokeWidth=12, cap="round")
d.shape("ellipse", "Hand hip", x=376, y=596, width=18, height=15,
        fill="#C9CEEC", stroke=INK, strokeWidth=3)
# arm holding the score paddle
d.path("M542,540 C566,524 584,506 596,486", "Arm paddle", fill=NONE,
       stroke="#9AA3D4", strokeWidth=12, cap="round")
d.shape("ellipse", "Hand paddle", x=588, y=476, width=18, height=15,
        fill="#C9CEEC", stroke=INK, strokeWidth=3)

# --- the score paddle ------------------------------------------------------------------
d.path("M598,486 L610,540", "Paddle stick", fill=NONE, stroke="#564E80",
       strokeWidth=7, cap="round")
d.shape("rectangle", "Paddle", x=560, y=388, width=140, height=88,
        fill="#1E1A38", stroke=INK, strokeWidth=5, radius=10)
d.shape("rectangle", "Paddle inner", x=570, y=398, width=120, height=68,
        fill="#2A2450", stroke="#564E80", strokeWidth=2, radius=6)
d.text("742", "Score", x=630, y=448, size=34, font="Virelai Sans",
       color="#F5CE7E", justify="center")
# pass glow off the paddle
d.shape("ellipse", "Paddle glow", x=580, y=400, width=100, height=64,
        fill="#F5CE7E", opacity=12, stroke=NONE)

# --- captions ---------------------------------------------------------------------------
d.text("SCORE SAM", "Name", x=500, y=930, size=60,
       font="Virelai Sans", color="#DCD8F2", justify="center")
r = d.text("BINARY GATE GATEKEEPER", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#A094CC", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("440.score-sam-V1R00")
