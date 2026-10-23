#!/usr/bin/env python3
"""Climate Cliff — mascot portrait V1R00.
Mascot beside a hardened floodwall; flood map shows the adjacent district
unprotected. 1000x1000. House style: gradients + translucent shading."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Climate Cliff — Mascot Portrait", 1000, 1000)

INK = "#26242C"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#141C1A"}, {"offset": 1, "color": "#070C0A"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4A6A5E"}, {"offset": 0.7, "color": "#304A42"},
    {"offset": 1, "color": "#1C2E28"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2A3E36"}, {"offset": 1, "color": "#14201C"}]}}
CONCRETE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#9AA4AE"}, {"offset": 1, "color": "#5E6A74"}]}}
MAP_PAPER = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#EFE4C8"}, {"offset": 1, "color": "#D4C49E"}]}}
WATER = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4A8A9A"}, {"offset": 1, "color": "#2A5A6A"}]}}
HARDHAT = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F0C95E"}, {"offset": 1, "color": "#C49434"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#5E8A7A", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D4E8DC", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(192,232,8),(802,228,7),(158,528,9),(836,542,8),
                               (248,768,7),(752,748,9),(134,392,6),(864,388,7),
                               (392,114,7),(612,112,8),(332,824,6),(665,822,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#40655A", opacity=45, stroke=NONE)

# --- floor: bottom segment closed on the disc's own arc -----------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#101C18",
       strokeWidth=4, opacity=70)

# --- the hardened floodwall -----------------------------------------------------
d.shape("ellipse", "Wall shadow", x=185, y=682, width=190, height=26,
        fill="#0A1410", opacity=45, stroke=NONE)
d.shape("rectangle", "Wall", x=200, y=195, width=140, height=505,
        fill=CONCRETE, stroke=INK, strokeWidth=6, radius=6)
# coping cap
d.shape("rectangle", "Coping", x=192, y=182, width=156, height=26,
        fill="#7A8490", stroke=INK, strokeWidth=5, radius=6)
# panel seams + rivets
for i in range(3):
    x = 235 + i*45
    d.path(f"M{x},208 L{x},695", f"Seam {i+1}", fill=NONE, stroke="#4E5862",
           strokeWidth=3, opacity=55)
for i, (x, y) in enumerate([(215,240),(320,240),(215,420),(320,420),(215,600),(320,600)]):
    d.shape("ellipse", f"Rivet {i+1}", x=x, y=y, width=9, height=9,
            fill="#4A545E", stroke=NONE, opacity=80)
# height ruler on the wall face
for i in range(5):
    w = 26 if i % 2 == 0 else 16
    d.shape("rectangle", f"Tick {i+1}", x=200, y=280+i*80, width=w, height=5,
            fill="#39434C", opacity=75, stroke=NONE)
# dry side: tiny safe house left of the wall
d.path("M168,662 L195,642 L222,662 L222,695 L168,695 Z", "Safe house",
       fill="#C9BBA0", stroke=INK, strokeWidth=4, join="round")
d.shape("rectangle", "Safe door", x=188, y=672, width=14, height=23,
        fill="#6A5E4A", stroke=NONE)
# wet side: water pooled against the wall's right foot
d.path("M340,660 C390,650 430,668 470,660 C510,652 540,668 560,662 L560,700 L340,700 Z",
       "Floodwater", fill=WATER, stroke=NONE, opacity=80)
for i, (x, y) in enumerate([(365,668),(425,662),(495,670)]):
    d.path(f"M{x},{y} C{x+8},{y-5} {x+16},{y-5} {x+24},{y}", f"Lap {i+1}",
           fill=NONE, stroke="#9AD0DA", strokeWidth=3, cap="round", opacity=60)

# --- flood map panel: adjacent district unprotected ------------------------------
d.shape("rectangle", "Map frame", x=585, y=210, width=240, height=210,
        fill="#5E5142", stroke=INK, strokeWidth=5, radius=8)
d.shape("rectangle", "Map paper", x=597, y=222, width=216, height=158,
        fill=MAP_PAPER, stroke=INK, strokeWidth=3)
# protected district (left half): calm hatch
for i in range(5):
    x0 = 606 + i*22
    d.path(f"M{x0},368 L{x0+16},368", f"Prot hatch {i+1}", fill=NONE,
           stroke="#7A9A6E", strokeWidth=5, opacity=60)
d.shape("rectangle", "Protected zone", x=604, y=230, width=96, height=142,
        fill="#9AB87E", opacity=35, stroke="#5E7A50", strokeWidth=3)
# the wall line inside the map
d.path("M700,230 L700,372", "Map wall line", fill=NONE, stroke="#3A4A56",
       strokeWidth=7)
# exposed district (right half): red + waves
d.shape("rectangle", "Exposed zone", x=704, y=230, width=102, height=142,
        fill="#C46A5E", opacity=40, stroke="#8A4238", strokeWidth=3)
for i in range(3):
    for j in range(2):
        x, y = 715 + j*46, 258 + i*42
        d.path(f"M{x},{y} C{x+9},{y-8} {x+18},{y-8} {x+27},{y} "
               f"C{x+36},{y+8} {x+45},{y+8} {x+54-18},{y}",
               f"Wave {i*2+j+1}", fill=NONE, stroke="#7A3A32",
               strokeWidth=3, cap="round", opacity=70)
d.text("EXPOSED", "Exposed label", x=710, y=352, size=13, font="Virelai Sans",
       color="#7A342C", justify="left")
d.text("HARDENED", "Hardened label", x=606, y=246, size=11, font="Virelai Sans",
       color="#4E6444", justify="left")
# map title strip
d.shape("rectangle", "Map title bar", x=597, y=390, width=216, height=22,
        fill="#4A3E32", stroke=NONE)
d.text("FLOOD MAP — REV. POST-PERMIT", "Map title", x=607, y=405, size=11,
       font="Virelai Sans", color="#E0D4B8", justify="left")

# --- Cliff: concrete-block mascot -------------------------------------------------
d.shape("ellipse", "Cliff shadow", x=395, y=688, width=190, height=28,
        fill="#0A1410", opacity=45, stroke=NONE)
# blocky body
d.shape("rectangle", "Cliff body", x=405, y=480, width=170, height=215,
        fill=CONCRETE, stroke=INK, strokeWidth=6, radius=16)
# concrete specks + seam
for i, (x, y, w) in enumerate([(425,505,8),(545,520,7),(430,650,7),(550,640,8),
                               (470,600,6),(520,560,6)]):
    d.shape("ellipse", f"Speck {i+1}", x=x, y=y, width=w, height=w,
            fill="#4A545E", opacity=50, stroke=NONE)
d.path("M405,600 L575,600", "Body seam", fill=NONE, stroke="#4E5862",
       strokeWidth=3, opacity=45)
# stub legs
d.shape("rectangle", "Leg L", x=435, y=695, width=38, height=26,
        fill="#5E6A74", stroke=INK, strokeWidth=4, radius=6)
d.shape("rectangle", "Leg R", x=507, y=695, width=38, height=26,
        fill="#5E6A74", stroke=INK, strokeWidth=4, radius=6)
# arm patting the wall
d.path("M410,530 C375,525 350,540 342,568", "Arm L", fill=NONE,
       stroke="#5E6A74", strokeWidth=16, cap="round")
d.shape("ellipse", "Hand L", x=326, y=556, width=26, height=26,
        fill="#7A8490", stroke=INK, strokeWidth=4)
# other arm gesturing at the map
d.path("M570,545 C590,530 600,520 612,510", "Arm R", fill=NONE,
       stroke="#5E6A74", strokeWidth=16, cap="round")
d.shape("ellipse", "Hand R", x=605, y=495, width=24, height=24,
        fill="#7A8490", stroke=INK, strokeWidth=4)
# face: wary eyes, flat worried mouth
d.shape("ellipse", "Eye L", x=438, y=528, width=20, height=24,
        fill="#26242C", stroke=NONE)
d.shape("ellipse", "Eye R", x=522, y=528, width=20, height=24,
        fill="#26242C", stroke=NONE)
d.shape("ellipse", "Glint L", x=443, y=533, width=6, height=6,
        fill="#FFFFFF", opacity=85, stroke=NONE)
d.shape("ellipse", "Glint R", x=527, y=533, width=6, height=6,
        fill="#FFFFFF", opacity=85, stroke=NONE)
d.path("M462,578 C478,570 502,570 518,578", "Worried mouth", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
# hard hat
d.path("M415,485 C415,445 445,425 490,425 C535,425 565,445 565,485 Z",
       "Hard hat dome", fill=HARDHAT, stroke=INK, strokeWidth=5)
d.shape("rectangle", "Hat brim", x=405, y=480, width=170, height=16,
        fill=HARDHAT, stroke=INK, strokeWidth=5, radius=8)
d.path("M470,428 L470,455 M510,428 L510,455", "Hat ridges", fill=NONE,
       stroke="#B08430", strokeWidth=4, opacity=70)

# --- captions ------------------------------------------------------------------
d.text("CLIMATE CLIFF", "Name", x=500, y=930, size=56, font="Virelai Sans",
       color="#D4E8DC", justify="center")
r = d.text("ASSET-PROTECTION PRIORITIZATION", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#9CBAA8", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("446.climate-cliff-V1R00")
