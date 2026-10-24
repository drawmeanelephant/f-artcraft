#!/usr/bin/env python3
"""LIM-0440 Score Sam — limerick plate V1R00. Mathematical redlining:
a giant phosphor score glows inside a gauge dial, a small figure stands
under it reduced to the number, the formula hides behind a curtain, and
the appeal stamp is already struck. Ledger-olive palette, warm dark ink.
1000x1000. House style: gradients + translucent shading, never flat fills.
Digits set in Source Sans 3 — Virelai Sans carries no figures."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("LIM-0440 Score Sam — Limerick Plate", 1000, 1000)

INK = "#241C10"
CREAM = "#F0E2C4"
TAN = "#B8A680"
RED = "#B8402E"
PHOS = "#F2C96A"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#161A10"}, {"offset": 1, "color": "#090B06"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#5E6248"}, {"offset": 0.7, "color": "#383B28"},
    {"offset": 1, "color": "#1C1D12"}]}}
COAT = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5C5240"}, {"offset": 1, "color": "#33291C"}]}}
SKIN = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E2CEA8"}, {"offset": 0.75, "color": "#B89E78"},
    {"offset": 1, "color": "#84704E"}]}}
CURTAIN = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4E2A24"}, {"offset": 1, "color": "#281410"}]}}
BOARD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2E3324"}, {"offset": 1, "color": "#1A1E12"}]}}
GLOW = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F2C96A", "opacity": 0.4},
    {"offset": 1, "color": "#F2C96A", "opacity": 0}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#7A7448", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8DCB8", strokeWidth=3, opacity=45)
for i, (x, y, w) in enumerate([(180, 220, 8), (800, 200, 7), (150, 500, 9),
                               (850, 560, 8), (240, 740, 7), (750, 720, 8),
                               (130, 370, 6), (860, 380, 7), (350, 140, 7),
                               (620, 150, 8)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#4A4426", opacity=40, stroke=NONE)

# --- the score gauge: dial arc looming at the top of the plate ---------------------
# dial face
d.shape("ellipse", "Dial face", x=330, y=150, width=340, height=340,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#464A34"}, {"offset": 0.8, "color": "#262A18"},
            {"offset": 1, "color": "#1A1E10"}]}},
        stroke=INK, strokeWidth=5)
# zone arcs: red (bad) left, amber middle, green (good) right
d.path("M332,322 A168,168 0 0 1 430,178", "Zone red", fill=NONE,
       stroke="#A04432", strokeWidth=16, cap="round")
d.path("M450,170 A168,168 0 0 1 550,170", "Zone amber", fill=NONE,
       stroke="#B8923C", strokeWidth=16, cap="round")
d.path("M570,178 A168,168 0 0 1 668,322", "Zone green", fill=NONE,
       stroke="#5E7A44", strokeWidth=16, cap="round")
# ticks around the dial
for i, (tx, ty) in enumerate([(360, 290), (380, 240), (415, 200), (455, 178),
                              (500, 172), (545, 178), (585, 200), (620, 240),
                              (640, 290)]):
    d.shape("ellipse", f"Dial tick {i+1}", x=tx - 3, y=ty - 3, width=6,
            height=6, fill="#8E8A62", stroke=NONE)
# the score, looming — digits in Source Sans 3
d.shape("ellipse", "Score glow", x=350, y=240, width=300, height=140,
        fill=GLOW, stroke=NONE)
d.text("587", "Score shadow", x=504, y=378, size=120, font="Source Sans 3",
       color="#14120A", justify="center")
d.text("587", "Score", x=500, y=374, size=120, font="Source Sans 3",
       color=PHOS, justify="center")
# needle pinned deep in the red zone
d.path("M500,320 L368,268", "Needle", fill=NONE, stroke=RED,
       strokeWidth=7, cap="round")
d.shape("ellipse", "Needle hub", x=488, y=308, width=24, height=24,
        fill=INK, stroke="#8E8A62", strokeWidth=3)
d.text("SCORE", "Dial label", x=500, y=432, size=18,
       font="Virelai Sans", color=TAN, justify="center")

# --- the hidden formula behind the curtain -----------------------------------------
d.shape("rectangle", "Formula board", x=640, y=430, width=180, height=180,
        radius=6, fill=BOARD, stroke=INK, strokeWidth=4)
d.text("f(x) = w\u00B7x + \u03B5", "Formula 1", x=730, y=478, size=15,
       font="Source Sans 3", color="#9AA480", justify="center")
d.text("w = [REDACTED]", "Formula 2", x=730, y=506, size=11,
       font="Virelai Sans", color="#7A7E58", justify="center")
d.text("err \u2192 DENY", "Formula 3", x=730, y=534, size=11,
       font="Virelai Sans", color="#8A5E4A", justify="center")
# chalk squiggle nobody may read
d.path("M662,560 C690,548 718,568 748,556 C768,548 786,556 798,550",
       "Chalk squiggle", fill=NONE, stroke="#9AA480", strokeWidth=2,
       opacity=60, cap="round")
# curtain swept across the board — the formula stays behind it
d.path("M820,400 C790,430 760,470 750,520 C742,560 748,596 742,640 "
       "L842,640 L842,400 Z",
       "Curtain", fill=CURTAIN, stroke=INK, strokeWidth=4, join="round")
d.path("M800,430 C786,470 780,540 782,620", "Curtain fold 1", fill=NONE,
       stroke="#5E342C", strokeWidth=5, opacity=70, cap="round")
d.path("M822,420 C812,470 808,550 812,625", "Curtain fold 2", fill=NONE,
       stroke="#5E342C", strokeWidth=4, opacity=60, cap="round")
# curtain tie-back cord
d.path("M738,560 C760,575 800,578 836,566", "Tie cord", fill=NONE,
       stroke="#B8923C", strokeWidth=4, cap="round")
d.shape("ellipse", "Cord knot", x=828, y=558, width=14, height=14,
        fill="#B8923C", stroke=INK, strokeWidth=2)

# --- Sam: a person reduced to the number ---------------------------------------------
d.shape("ellipse", "Sam shadow", x=400, y=720, width=200, height=20,
        fill="#0E1008", opacity=45, stroke=NONE)
# coat
d.path("M462,560 L538,560 L552,720 L448,720 Z", "Sam coat", fill=COAT,
       stroke=INK, strokeWidth=5, join="round")
d.path("M474,575 L468,700", "Coat sheen", fill=NONE, stroke="#E8DCB8",
       strokeWidth=6, opacity=14, cap="round")
# head tipped up toward the score
d.shape("ellipse", "Sam head", x=472, y=506, width=56, height=56,
        fill=SKIN, stroke=INK, strokeWidth=5)
# eyes fixed upward, tired
d.shape("ellipse", "Eye L", x=486, y=522, width=8, height=10,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Eye R", x=506, y=522, width=8, height=10,
        fill=INK, stroke=NONE)
d.path("M486,546 Q500,540 514,546", "Flat mouth", fill=NONE, stroke=INK,
       strokeWidth=4, cap="round")
d.path("M480,510 L494,506 M506,506 L520,510", "Weary brows", fill=NONE,
       stroke=INK, strokeWidth=3.5, cap="round", opacity=80)
# hairline
d.path("M476,520 C480,502 520,502 524,518", "Hair", fill=NONE, stroke=INK,
       strokeWidth=4, cap="round", opacity=60)
# barcode tag pinned to the chest — the person is the number
d.shape("rectangle", "Barcode tag", x=480, y=596, width=52, height=34,
        radius=3, fill="#E8E0CC", stroke=INK, strokeWidth=3)
for i, bx in enumerate([486, 490, 496, 500, 506, 512, 518, 524]):
    w = 2 if i % 3 else 3.5
    d.path(f"M{bx},600 L{bx},{622}", f"Bar {i+1}", fill=NONE, stroke=INK,
           strokeWidth=w)
d.text("587", "Tag digits", x=506, y=630, size=8, font="Source Sans 3",
       color=INK, justify="center")
# weight of the number: faint downward rays from the dial onto Sam
for i, (rx, ry) in enumerate([(470, 495), (500, 500), (530, 495)]):
    d.path(f"M{rx},470 L{rx},{ry + 6}", f"Weight ray {i+1}", fill=NONE,
           stroke=PHOS, strokeWidth=2.5, opacity=35, cap="round")

# --- APPEAL DENIED stamp, lower left ---------------------------------------------------
stamp_ids = []
for res in [
    d.shape("rectangle", "Stamp frame", x=170, y=610, width=180, height=64,
            radius=6, fill=NONE, stroke=RED, strokeWidth=5),
    d.shape("rectangle", "Stamp frame inner", x=178, y=618, width=164,
            height=48, radius=4, fill=NONE, stroke=RED, strokeWidth=2,
            opacity=80),
    d.text("APPEAL", "Stamp line 1", x=260, y=636, size=17,
           font="Virelai Sans", color=RED, justify="center"),
    d.text("DENIED", "Stamp line 2", x=260, y=658, size=17,
           font="Virelai Sans", color=RED, justify="center"),
]:
    if res and res.get("id"):
        stamp_ids.append(res["id"])
if stamp_ids:
    d.call("transform", {"ids": stamp_ids, "rotate": -14,
                         "origin": [260, 642]}, "tilt stamp")

# --- key line + name + role ---------------------------------------------------------
r = d.text("A NUMBER IS ALL YOU BECOME.", "Key line", x=500, y=780,
           size=22, font="Virelai Sans", color=CREAM, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "key line tracking", ids=[r["id"]], tracking=60)
d.text("SCORE SAM", "Name", x=500, y=930, size=58,
       font="Virelai Sans", color=CREAM, justify="center")
r = d.text("THE SCORE IS THE FINAL OUTCOME", "Role", x=500, y=967,
           size=20, font="Virelai Sans", color=TAN, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=170)

d.finish("lim-0440-score-sam-V1R00")
