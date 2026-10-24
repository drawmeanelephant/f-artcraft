#!/usr/bin/env python3
"""HAI-0446 Climate Cliff — haiku plate V1R00. Survival, business hours: a
hardened wall keeps the condo towers dry while the far side drowns, capital
crowned overhead, a lifeboat on the flood still charging a fare. The wall
wears a clock and a CLOSED placard — even the shelter keeps hours.
Warm dark ink, 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE
import math

d = Draw()
d.new_doc("HAI-0446 Climate Cliff — Haiku Plate", 1000, 1000)

INK = "#22241F"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#131B15"}, {"offset": 1, "color": "#070C08"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4E6E58"}, {"offset": 0.7, "color": "#2E4A3C"},
    {"offset": 1, "color": "#172A20"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#26392F"}, {"offset": 1, "color": "#12201A"}]}}
CONCRETE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#9AA4AE"}, {"offset": 1, "color": "#5E6A74"}]}}
TOWER = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5A6E7E"}, {"offset": 1, "color": "#33424E"}]}}
WATER = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3E7E8E"}, {"offset": 1, "color": "#224A58"}]}}
SUN = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F4D07A"}, {"offset": 0.65, "color": "#E09A4A"},
    {"offset": 1, "color": "#B06A34"}]}}
GOLD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F0CE7E"}, {"offset": 1, "color": "#B8873A"}]}}
HARDHAT = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F0C95E"}, {"offset": 1, "color": "#C49434"}]}}
BONE = "#E8E4D2"
DIM = "#9CB8A4"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#6E9480", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D4E8D8", strokeWidth=3, opacity=45)
for i, (x, y, w) in enumerate([(192, 232, 8), (800, 226, 7), (158, 528, 9),
                               (836, 542, 8), (248, 762, 7), (750, 750, 9),
                               (132, 392, 6), (864, 388, 7), (392, 112, 7),
                               (612, 110, 8), (330, 820, 6), (668, 818, 7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#42685A", opacity=45, stroke=NONE)

# --- floor: bottom segment closed on the disc's own arc -----------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0C1611",
       strokeWidth=4, opacity=70)

# --- ghost ledger lines high on the plate --------------------------------------
d.text("FLOOD MAP PENDING — PERMIT ISSUED", "Ghost 1", x=500, y=140, size=13,
       font="Virelai Sans", color="#7A9478", justify="center")
d.text("HEAT INDEX: BILLABLE", "Ghost 2", x=500, y=163, size=12,
       font="Virelai Sans", color="#6A8468", justify="center")

# --- the sun over the wet side: it peaks at eight --------------------------------
d.shape("ellipse", "Sun glow", x=640, y=140, width=220, height=170,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#F4C86A", "opacity": 0.22},
            {"offset": 1, "color": "#F4C86A", "opacity": 0}]}},
        stroke=NONE)
d.shape("ellipse", "Sun", x=706, y=178, width=92, height=92,
        fill=SUN, stroke=INK, strokeWidth=4)
for i, a in enumerate(range(0, 360, 45)):
    ar = math.radians(a + 22)
    x1, y1 = 752 + 54 * math.cos(ar), 224 + 54 * math.sin(ar)
    x2, y2 = 752 + 66 * math.cos(ar), 224 + 66 * math.sin(ar)
    d.path(f"M{x1:.0f},{y1:.0f} L{x2:.0f},{y2:.0f}", f"Ray {i+1}",
           fill=NONE, stroke="#E8B86A", strokeWidth=4, cap="round",
           opacity=70)

# --- dry side: condo towers, crowned --------------------------------------------
d.shape("rectangle", "Tower A", x=235, y=305, width=95, height=380,
        fill=TOWER, stroke=INK, strokeWidth=5, radius=4)
d.shape("rectangle", "Tower B", x=335, y=365, width=80, height=320,
        fill=TOWER, stroke=INK, strokeWidth=5, radius=4)
# lit windows, generous on the dry side
for r_i in range(7):
    for c_i in range(3):
        lit = (r_i * 3 + c_i) % 4 != 2
        d.shape("rectangle", f"Win A {r_i+1}-{c_i+1}", x=247 + c_i * 27,
                y=320 + r_i * 48, width=16, height=22,
                fill="#E8D88E" if lit else "#2A363E",
                opacity=85 if lit else 70, stroke=NONE, radius=2)
for r_i in range(6):
    for c_i in range(2):
        lit = (r_i * 2 + c_i) % 3 != 1
        d.shape("rectangle", f"Win B {r_i+1}-{c_i+1}", x=348 + c_i * 32,
                y=382 + r_i * 46, width=18, height=22,
                fill="#E8D88E" if lit else "#2A363E",
                opacity=85 if lit else 70, stroke=NONE, radius=2)
# parapets
d.path("M230,305 L235,288 L330,288 L335,305", "Crown parapet A", fill="#42545E",
       stroke=INK, strokeWidth=4)
d.path("M330,365 L335,350 L415,350 L420,365", "Crown parapet B", fill="#42545E",
       stroke=INK, strokeWidth=4)
# the crown: capital floating over the dry side
d.shape("ellipse", "Crown glow", x=240, y=190, width=120, height=80,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#F0CE7E", "opacity": 0.25},
            {"offset": 1, "color": "#F0CE7E", "opacity": 0}]}},
        stroke=NONE)
d.path("M258,252 L258,222 L276,238 L298,212 L320,238 L338,222 L338,252 Z",
       "Crown", fill=GOLD, stroke=INK, strokeWidth=4, join="round")
d.shape("rectangle", "Crown band", x=258, y=252, width=80, height=14,
        fill=GOLD, stroke=INK, strokeWidth=4, radius=3)
for i, cx in enumerate([268, 298, 328]):
    d.shape("ellipse", f"Crown jewel {i+1}", x=cx - 4, y=228 + (6 if i == 1 else 0),
            width=8, height=8, fill="#8A3428" if i == 1 else "#4E6E58",
            stroke=INK, strokeWidth=2)
d.path("M272,266 L324,266", "Crown band line", fill=NONE, stroke="#8A6428",
       strokeWidth=3)

# --- the wall: keeps the money dry -----------------------------------------------
d.shape("rectangle", "Wall", x=445, y=215, width=130, height=485,
        fill=CONCRETE, stroke=INK, strokeWidth=6, radius=6)
d.shape("rectangle", "Coping", x=437, y=202, width=146, height=24,
        fill="#7A8490", stroke=INK, strokeWidth=5, radius=6)
for i in range(2):
    x = 488 + i * 45
    d.path(f"M{x},228 L{x},695", f"Seam {i+1}", fill=NONE, stroke="#4E5862",
           strokeWidth=3, opacity=55)
for i, (x, y) in enumerate([(462, 250), (548, 250), (462, 430), (548, 430),
                            (462, 610), (548, 610)]):
    d.shape("ellipse", f"Rivet {i+1}", x=x, y=y, width=9, height=9,
            fill="#4A545E", stroke=NONE, opacity=80)
# height ruler on the dry face
for i in range(4):
    w = 24 if i % 2 == 0 else 14
    d.shape("rectangle", f"Tick {i+1}", x=445, y=300 + i * 100, width=w,
            height=5, fill="#39434C", opacity=75, stroke=NONE)

# --- the cooling center on the wall: a clock, a CLOSED placard -------------------
d.shape("ellipse", "Clock", x=478, y=330, width=64, height=64,
        fill="#E8E4D2", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Clock hub", x=506, y=358, width=8, height=8,
        fill="#22241F", stroke=NONE)
d.path("M510,362 L503,344 M510,362 L507,382", "Clock hands", fill=NONE,
       stroke="#22241F", strokeWidth=3.5, cap="round")
d.shape("rectangle", "Placard", x=474, y=408, width=72, height=30,
        fill="#C9BBA0", stroke=INK, strokeWidth=3, radius=4)
d.text("CLOSED", "Placard word", x=510, y=428, size=13,
       font="Virelai Sans", color="#6A2E28", justify="center")
d.path("M510,394 L510,408", "Placard nail string", fill=NONE, stroke=INK,
       strokeWidth=2.5)

# --- wet side: the neighbourhood drowns -------------------------------------------
# drowned rooftops poking out of the flood
d.path("M628,640 L668,606 L708,640 L708,700 L628,700 Z", "Drowned house 1",
       fill="#3A3230", stroke=INK, strokeWidth=4, join="round")
d.path("M720,655 L756,622 L792,655 L792,700 L720,700 Z", "Drowned house 2",
       fill="#342E2A", stroke=INK, strokeWidth=4, join="round")
d.shape("rectangle", "Chimney", x=688, y=600, width=14, height=26,
        fill="#3A3230", stroke=INK, strokeWidth=3)
# the flood itself, lapping the wall's right foot
d.path("M575,640 C615,630 645,648 685,640 C725,632 755,648 795,640 "
       "C815,636 830,642 844,638 L844,700 L575,700 Z",
       "Floodwater", fill=WATER, stroke=NONE, opacity=82)
for i, (x, y) in enumerate([(600, 646), (670, 640), (740, 646), (810, 642)]):
    d.path(f"M{x},{y} C{x+9},{y-6} {x+18},{y-6} {x+27},{y}", f"Lap {i+1}",
           fill=NONE, stroke="#9AD0DA", strokeWidth=3, cap="round",
           opacity=60)
# a rising line up the wall's wet face — the map came late
d.path("M575,640 C615,630 645,648 685,640", "High water mark", fill=NONE,
       stroke="#B8D8DE", strokeWidth=3, cap="round", opacity=45)

# --- the lifeboat: still charging for entry ---------------------------------------
d.path("M615,645 C645,675 725,675 755,645 L747,630 L623,630 Z",
       "Boat hull", fill="#8A5E3A", stroke=INK, strokeWidth=4, join="round")
d.path("M625,641 L745,641", "Gunwale", fill=NONE, stroke="#5E3E24",
       strokeWidth=3)
# the toll: a little fare box bolted to the stern
d.shape("rectangle", "Fare box", x=701, y=597, width=46, height=36,
        fill="#C9BBA0", stroke=INK, strokeWidth=3, radius=5)
d.shape("ellipse", "Coin slot", x=717, y=605, width=14, height=5,
        fill="#22241F", stroke=NONE)
d.text("FARE", "Fare word", x=707, y=627, size=10, font="Virelai Sans",
       color="#5A4526", justify="left")
d.path("M641,630 L641,595", "Boat pole", fill=NONE, stroke="#5E3E24",
       strokeWidth=4, cap="round")
d.path("M641,595 L675,603 L641,613 Z", "Boat flag", fill="#B8873A",
       stroke=INK, strokeWidth=3, join="round")
# wake ripple at the waterline
d.path("M607,660 C645,670 725,670 763,660", "Wake", fill=NONE,
       stroke="#9AD0DA", strokeWidth=3, cap="round", opacity=50)

# --- Cliff: the concrete block that works here -------------------------------------
d.shape("ellipse", "Cliff shadow", x=330, y=688, width=150, height=22,
        fill="#0A1410", opacity=45, stroke=NONE)
d.shape("rectangle", "Cliff body", x=345, y=530, width=110, height=165,
        fill=CONCRETE, stroke=INK, strokeWidth=6, radius=14)
for i, (x, y, w) in enumerate([(360, 550, 7), (430, 560, 6), (365, 650, 6),
                               (428, 640, 7), (395, 600, 5)]):
    d.shape("ellipse", f"Speck {i+1}", x=x, y=y, width=w, height=w,
            fill="#4A545E", opacity=50, stroke=NONE)
d.path("M345,610 L455,610", "Body seam", fill=NONE, stroke="#4E5862",
       strokeWidth=3, opacity=45)
# stub legs
d.shape("rectangle", "Leg L", x=365, y=695, width=28, height=20,
        fill="#5E6A74", stroke=INK, strokeWidth=4, radius=6)
d.shape("rectangle", "Leg R", x=407, y=695, width=28, height=20,
        fill="#5E6A74", stroke=INK, strokeWidth=4, radius=6)
# arm patting the wall
d.path("M450,560 C470,555 478,545 482,532", "Arm pat", fill=NONE,
       stroke="#5E6A74", strokeWidth=14, cap="round")
d.shape("ellipse", "Hand pat", x=470, y=516, width=22, height=22,
        fill="#7A8490", stroke=INK, strokeWidth=4)
# face: content — he is on the dry side
d.shape("ellipse", "Eye L", x=372, y=572, width=16, height=20,
        fill="#22241F", stroke=NONE)
d.shape("ellipse", "Eye R", x=412, y=572, width=16, height=20,
        fill="#22241F", stroke=NONE)
d.shape("ellipse", "Glint L", x=376, y=576, width=5, height=5,
        fill="#FFFFFF", opacity=85, stroke=NONE)
d.shape("ellipse", "Glint R", x=416, y=576, width=5, height=5,
        fill="#FFFFFF", opacity=85, stroke=NONE)
d.path("M382,598 C392,606 408,606 418,598", "Smug mouth", fill=NONE,
       stroke=INK, strokeWidth=4.5, cap="round")
# hard hat
d.path("M352,536 C352,506 372,490 400,490 C428,490 448,506 448,536 Z",
       "Hard hat dome", fill=HARDHAT, stroke=INK, strokeWidth=5)
d.shape("rectangle", "Hat brim", x=345, y=531, width=110, height=13,
        fill=HARDHAT, stroke=INK, strokeWidth=5, radius=6)
d.path("M388,493 L388,516 M412,493 L412,516", "Hat ridges", fill=NONE,
       stroke="#B08430", strokeWidth=3.5, opacity=70)

# --- captions --------------------------------------------------------------------
k = d.text("survival, business hours.", "Key line", x=500, y=896, size=23,
           font="Virelai Sans", color="#C4D8C4", justify="center")
if k and k.get("id"):
    d.cmd("text.setStyle", "key tracking", ids=[k["id"]], tracking=260)
d.text("CLIMATE CLIFF", "Name", x=500, y=941, size=56, font="Virelai Sans",
       color=BONE, justify="center")
r = d.text("SURVIVAL AS ASSET CLASS", "Role", x=500, y=973, size=19,
           font="Virelai Sans", color="#8AAE94", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=180)

d.finish("hai-0446-climate-cliff-V1R00")
