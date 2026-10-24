#!/usr/bin/env python3
"""Ketchup Keeper — mascot portrait V1R00.
Keeper in a riveted vault dripping with ketchup: bandana, apron, key
ring, ladle raised mid-drip; recipe ledgers stacked under a hanging
lamp. 1000x1000. House style: gradients + translucent shading."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Ketchup Keeper — Mascot Portrait", 1000, 1000)

INK = "#332226"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#140C0E"}, {"offset": 1, "color": "#070404"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#7A4238"}, {"offset": 0.7, "color": "#4E2A28"},
    {"offset": 1, "color": "#2A1515"}]}}
FLOOR = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#463028"}, {"offset": 1, "color": "#201412"}]}}
STEEL = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#5E4E4A"}, {"offset": 0.75, "color": "#423638"},
    {"offset": 1, "color": "#2A2022"}]}}
SAUCE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#C93B2E"}, {"offset": 1, "color": "#8A1E16"}]}}
BODY = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F2DCC4"}, {"offset": 0.7, "color": "#D6B28E"},
    {"offset": 1, "color": "#AA7E5C"}]}}
APRON = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#8A3E36"}, {"offset": 1, "color": "#5A2624"}]}}
PAPER = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F0E6CE"}, {"offset": 1, "color": "#CBBD9C"}]}}
LAMP = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E8B84E"}, {"offset": 1, "color": "#A8762A"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#A05E50", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F0D6C4", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(190,235,8),(800,230,7),(160,520,9),(830,540,8),
                               (240,760,7),(760,740,9),(130,390,6),(865,390,7),
                               (390,110,7),(610,110,8),(330,820,6),(665,815,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#5E342C", opacity=45, stroke=NONE)

# --- vault door behind, upper-left ----------------------------------------------
d.shape("ellipse", "Vault door", x=180, y=170, width=290, height=290,
        fill=STEEL, stroke=INK, strokeWidth=6)
d.shape("ellipse", "Vault ring", x=196, y=186, width=258, height=258,
        fill=NONE, stroke="#6E5A56", strokeWidth=5, opacity=80)
for i in range(12):
    import math
    a = math.radians(i*30)
    x = 325 + 138*math.cos(a) - 5
    y = 315 + 138*math.sin(a) - 5
    d.shape("ellipse", f"Rivet {i+1}", x=x, y=y, width=10, height=10,
            fill="#2E2224", stroke="#6E5A56", strokeWidth=1)
# wheel handle
d.shape("ellipse", "Wheel rim", x=285, y=275, width=80, height=80,
        fill=NONE, stroke="#8A7470", strokeWidth=7)
for dx, dy in [(0,-30),(26,15),(-26,15)]:
    d.path(f"M325,315 L{325+dx},{315+dy}", "Wheel spoke", fill=NONE,
           stroke="#8A7470", strokeWidth=6, cap="round")
d.shape("ellipse", "Wheel hub", x=313, y=303, width=24, height=24,
        fill="#6E5A56", stroke=INK, strokeWidth=3)

# --- ketchup drips from the vault top --------------------------------------------
d.path("M250,120 C400,148 620,148 760,118 L762,168 C720,178 690,168 660,178 "
       "C650,208 632,214 622,192 C608,166 580,172 566,190 C552,240 528,246 518,206 "
       "C510,176 480,178 466,196 C452,232 430,238 424,204 C420,182 390,180 372,196 "
       "C350,232 330,230 330,196 C330,176 300,168 280,178 C262,186 252,160 250,120 Z",
       "Ketchup drip band", fill=SAUCE, stroke=NONE, opacity=88)
d.path("M300,150 C420,172 600,172 710,148", "Sauce sheen", fill=NONE,
       stroke="#E8725E", strokeWidth=6, cap="round", opacity=55)
# two stray drips mid-air
d.shape("ellipse", "Drip 1", x=556, y=250, width=10, height=20,
        fill="#B03226", opacity=80, stroke=NONE)
d.shape("ellipse", "Drip 2", x=590, y=268, width=8, height=14,
        fill="#B03226", opacity=70, stroke=NONE)

# --- hanging lamp + light pool -----------------------------------------------------
d.path("M640,96 L640,176", "Lamp cord", fill=NONE, stroke="#3A2E2A",
       strokeWidth=5, cap="round")
d.path("M640,176 L604,232 L676,232 Z", "Lamp shade",
       fill=LAMP, stroke=INK, strokeWidth=4, join="round")
d.shape("ellipse", "Bulb", x=628, y=232, width=24, height=18,
        fill="#F8E8B8", stroke=NONE, opacity=95)
d.path("M604,232 L676,232 L780,660 L500,660 Z", "Light cone",
       fill="#F8E0A8", opacity=10, stroke=NONE)

# --- floor -------------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR, stroke=NONE)
d.shape("ellipse", "Keeper shadow", x=350, y=676, width=180, height=30,
        fill="#0A0606", opacity=55, stroke=NONE)

# --- ledger table under the lamp -----------------------------------------------------
d.shape("rectangle", "Table top", x=540, y=620, width=230, height=22,
        fill={"gradient": {"kind": "linear", "stops": [
            {"offset": 0, "color": "#6E4A34"}, {"offset": 1, "color": "#46301F"}]}},
        stroke=INK, strokeWidth=5, radius=6)
d.path("M566,642 L560,768 M744,642 L750,768", "Table legs", fill=NONE,
       stroke="#3A281A", strokeWidth=10, cap="round")
# stacked ledgers
d.shape("rectangle", "Ledger 1", x=566, y=592, width=110, height=28,
        fill={"gradient": {"kind": "linear", "stops": [
            {"offset": 0, "color": "#6E3E2E"}, {"offset": 1, "color": "#4A261C"}]}},
        stroke=INK, strokeWidth=4, radius=3)
d.shape("rectangle", "Ledger 2", x=574, y=566, width=96, height=26,
        fill={"gradient": {"kind": "linear", "stops": [
            {"offset": 0, "color": "#7A5A3A"}, {"offset": 1, "color": "#54401F"}]}},
        stroke=INK, strokeWidth=4, radius=3)
d.text("RECIPES", "Spine label", x=621, y=584, size=11,
       font="Virelai Sans", color="#E8D9B0", justify="center")
# open ledger on top, fanned
d.path("M694,586 L694,616 L758,606 L758,578 Z", "Ledger page R",
       fill=PAPER, stroke=INK, strokeWidth=3, join="round")
d.path("M694,586 L694,616 L690,606 L690,578 Z", "Ledger page L",
       fill=PAPER, stroke=INK, strokeWidth=3, join="round")
for i, y in enumerate([588, 596, 604]):
    d.path(f"M700,{y} L750,{y-4}", f"Recipe line {i+1}", fill=NONE,
           stroke="#8A7A54", strokeWidth=2, opacity=60)
# ketchup bottle on the table
d.shape("rectangle", "Bottle body", x=756, y=560, width=26, height=58,
        fill=SAUCE, stroke=INK, strokeWidth=4, radius=6)
d.shape("rectangle", "Bottle neck", x=762, y=544, width=14, height=20,
        fill="#8A1E16", stroke=INK, strokeWidth=3, radius=3)
d.shape("rectangle", "Bottle label", x=760, y=578, width=18, height=18,
        fill=PAPER, stroke="#8A6E42", strokeWidth=1)

# --- the keeper -----------------------------------------------------------------------
# legs + shoes
d.path("M405,648 L400,684", "Leg L", fill=NONE, stroke="#AA7E5C",
       strokeWidth=13, cap="round")
d.path("M455,648 L460,684", "Leg R", fill=NONE, stroke="#9A724E",
       strokeWidth=13, cap="round")
d.shape("ellipse", "Shoe L", x=384, y=678, width=32, height=15, fill=INK, stroke=NONE)
d.shape("ellipse", "Shoe R", x=448, y=678, width=32, height=15, fill=INK, stroke=NONE)
# body
d.path("M430,452 C492,452 524,500 520,556 C516,620 484,656 430,656 "
       "C376,656 344,620 340,556 C336,500 368,452 430,452 Z",
       "Keeper body", fill=BODY, stroke=INK, strokeWidth=6)
# apron with bib + straps
d.path("M380,540 C390,596 408,634 430,650 C452,634 470,596 480,540 "
       "C462,554 398,554 380,540 Z",
       "Apron", fill=APRON, stroke=INK, strokeWidth=4, join="round")
d.path("M394,542 L412,556 M466,542 L448,556", "Apron straps", fill=NONE,
       stroke="#5A2624", strokeWidth=6, cap="round")
d.shape("rectangle", "Apron pocket", x=408, y=586, width=44, height=34,
        fill="#6E322C", stroke=INK, strokeWidth=3, radius=3)
d.path("M408,596 L452,596", "Pocket seam", fill=NONE, stroke=INK,
       strokeWidth=2, opacity=70)
# ketchup smear on the apron
d.path("M392,600 C400,592 416,596 420,606 C412,616 396,614 392,600 Z",
       "Sauce smear", fill="#C93B2E", stroke=NONE, opacity=70)
# key ring at the hip
d.shape("ellipse", "Key ring", x=498, y=596, width=26, height=26,
        fill=NONE, stroke="#C9A03E", strokeWidth=5)
d.path("M514,618 L514,644 M514,644 L506,644 M514,636 L508,636", "Key 1",
       fill=NONE, stroke="#C9A03E", strokeWidth=5, cap="round")
d.path("M524,616 L528,640 M528,640 L520,642 M526,632 L519,634", "Key 2",
       fill=NONE, stroke="#A8792E", strokeWidth=5, cap="round")
# bandana, knotted at the side
d.path("M378,470 C372,440 396,424 430,424 C464,424 488,440 482,470 "
       "C470,452 390,452 378,470 Z",
       "Bandana", fill=SAUCE, stroke=INK, strokeWidth=5, join="round")
d.shape("ellipse", "Bandana knot", x=482, y=452, width=16, height=14,
        fill="#8A1E16", stroke=INK, strokeWidth=3)
d.path("M492,458 L506,468 M494,462 L502,478", "Knot tails", fill=NONE,
       stroke="#8A1E16", strokeWidth=5, cap="round")
# face: bold, warm
d.shape("ellipse", "Eye L", x=400, y=502, width=14, height=18, fill=INK, stroke=NONE)
d.shape("ellipse", "Eye R", x=448, y=502, width=14, height=18, fill=INK, stroke=NONE)
d.shape("ellipse", "Glint L", x=404, y=506, width=4, height=4, fill="#FFFFFF", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=452, y=506, width=4, height=4, fill="#FFFFFF", opacity=90, stroke=NONE)
d.path("M396,486 L412,482", "Brow L", fill=NONE, stroke=INK, strokeWidth=4, cap="round")
d.path("M444,482 L460,486", "Brow R", fill=NONE, stroke=INK, strokeWidth=4, cap="round")
d.shape("ellipse", "Cheek L", x=388, y=526, width=22, height=13,
        fill="#C9725E", opacity=50, stroke=NONE)
d.shape("ellipse", "Cheek R", x=452, y=526, width=22, height=13,
        fill="#C9725E", opacity=50, stroke=NONE)
d.path("M410,544 C424,554 442,554 454,544", "Smile", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
# right arm raised with the dripping ladle
d.path("M500,540 C535,528 556,505 564,478", "Arm ladle", fill=NONE,
       stroke="#D6B28E", strokeWidth=12, cap="round")
d.shape("ellipse", "Ladle hand", x=556, y=466, width=18, height=15,
        fill="#F2DCC4", stroke=INK, strokeWidth=3)
d.path("M566,470 L590,420", "Ladle handle", fill=NONE, stroke="#8A7470",
       strokeWidth=7, cap="round")
d.shape("ellipse", "Ladle cup", x=578, y=394, width=30, height=24,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#B03226"}, {"offset": 1, "color": "#6E5A56"}]}},
        stroke=INK, strokeWidth=3)
d.shape("ellipse", "Ladle drip", x=592, y=424, width=8, height=16,
        fill="#C93B2E", opacity=85, stroke=NONE)
# left arm resting on the ledger table
d.path("M362,548 C340,566 332,592 342,612", "Arm table", fill=NONE,
       stroke="#C9A87E", strokeWidth=12, cap="round")
d.shape("ellipse", "Rest hand", x=336, y=606, width=18, height=15,
        fill="#F2DCC4", stroke=INK, strokeWidth=3)

# --- captions ---------------------------------------------------------------------------
d.text("KETCHUP KEEPER", "Name", x=500, y=930, size=58,
       font="Virelai Sans", color="#F0D6C4", justify="center")
r = d.text("TANG STEWARD", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#C99A8A", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("213.ketchup-keeper-V1R00")
