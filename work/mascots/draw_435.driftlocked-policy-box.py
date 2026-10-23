#!/usr/bin/env python3
"""Driftlocked Policy Box — mascot portrait V1R00.
Locked policy box with brass ring handles on the floor, JUN 11 stamped
on the lid, padlock shut, half-asleep. 1000x1000. House style:
gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Driftlocked Policy Box — Mascot Portrait", 1000, 1000)

INK = "#332A33"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#17130C"}, {"offset": 1, "color": "#0A0805"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#7A6544"}, {"offset": 0.7, "color": "#57482E"},
    {"offset": 1, "color": "#322A1C"}]}}
FLOOR = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#443A28"}, {"offset": 1, "color": "#241D12"}]}}
BOX_FRONT = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#8A6644"}, {"offset": 0.7, "color": "#6B4C30"},
    {"offset": 1, "color": "#4A3320"}]}}
BOX_LID = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#9C7750"}, {"offset": 1, "color": "#6B4C30"}]}}
BRASS = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E8BC62"}, {"offset": 1, "color": "#A87C34"}]}}
BRASS_DK = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#C89A4A"}, {"offset": 1, "color": "#8A6226"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#9A825A", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8D9B4", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(190,240,8),(800,230,7),(160,520,9),(830,540,8),
                               (240,760,7),(760,740,9),(130,390,6),(865,390,7),
                               (390,110,7),(610,110,8),(330,820,6),(665,815,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#5F4F34", opacity=45, stroke=NONE)

# --- floor --------------------------------------------------------------------
d.shape("ellipse", "Floor", x=175, y=610, width=650, height=140,
        fill=FLOOR, stroke=NONE, opacity=92)
d.shape("ellipse", "Box shadow", x=340, y=668, width=320, height=46,
        fill="#100C06", opacity=55, stroke=NONE)

# --- the policy box -------------------------------------------------------------
# feet
d.shape("ellipse", "Foot L", x=394, y=656, width=46, height=22,
        fill=BRASS_DK, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Foot R", x=560, y=656, width=46, height=22,
        fill=BRASS_DK, stroke=INK, strokeWidth=4)
# front face
d.shape("rectangle", "Box front", x=370, y=458, width=260, height=200,
        fill=BOX_FRONT, stroke=INK, strokeWidth=6, radius=10)
# wood grain
for i, y in enumerate([510, 556, 618]):
    d.path(f"M384,{y} C460,{y-6} 540,{y+6} 616,{y}", f"Grain {i+1}",
           fill=NONE, stroke="#3E2A18", strokeWidth=3, opacity=35)
# lid top face (slight perspective)
d.path("M370,458 L398,408 L602,408 L630,458 Z", "Lid top",
       fill=BOX_LID, stroke=INK, strokeWidth=6, join="round")
# lid seam highlight
d.path("M378,458 L622,458", "Lid seam", fill=NONE, stroke="#C09A62",
       strokeWidth=3, opacity=50)
# corner brackets
for i, (x, y) in enumerate([(370,458),(598,458),(370,626),(598,626)]):
    d.path(f"M{x},{y+16} L{x},{y} L{x+32},{y}" if x==370 else f"M{x+32},{y+16} L{x+32},{y} L{x},{y}",
           f"Bracket {i+1}", fill=NONE, stroke=BRASS_DK, strokeWidth=5, cap="round")
# JUN 11 stamp on the lid
d.text("JUN 11", "Lid stamp", x=500, y=446, size=18, font="Virelai Sans",
       color="#4A3220", justify="center")
d.shape("rectangle", "Stamp border", x=450, y=420, width=100, height=32,
        fill=NONE, stroke="#4A3220", strokeWidth=2, opacity=70, radius=3)
# ring handles, left + right
for side, cx in (("L", 348), ("R", 652)):
    d.shape("rectangle", f"Mount {side}", x=cx-9, y=520, width=18, height=32,
            fill=BRASS_DK, stroke=INK, strokeWidth=3, radius=4)
    d.shape("ellipse", f"Ring {side}", x=cx-22, y=548, width=44, height=38,
            fill=NONE, stroke=BRASS, strokeWidth=8)
# hasp + padlock
d.shape("rectangle", "Hasp", x=488, y=450, width=24, height=74,
        fill=BRASS_DK, stroke=INK, strokeWidth=4, radius=4)
d.path("M500,516 C478,516 468,536 468,550 L468,554 L532,554 L532,550 C532,536 522,516 500,516 Z",
       "Shackle", fill=NONE, stroke="#D8AC52", strokeWidth=8)
d.shape("rectangle", "Padlock", x=466, y=548, width=68, height=56,
        fill=BRASS, stroke=INK, strokeWidth=5, radius=8)
d.shape("ellipse", "Keyhole", x=493, y=566, width=14, height=14, fill=INK, stroke=NONE)
d.path("M497,578 L492,590 L508,590 L503,578", "Keyhole slot", fill=INK, stroke=NONE)

# --- the face: half-lidded, long sealed ------------------------------------------
# droopy lids
d.path("M418,548 C430,540 450,540 462,548 C450,553 430,553 418,548 Z",
       "Eye L", fill=INK, stroke=NONE)
d.path("M538,548 C550,540 570,540 582,548 C570,553 550,553 538,548 Z",
       "Eye R", fill=INK, stroke=NONE)
d.shape("ellipse", "Glint L", x=436, y=544, width=5, height=4, fill="#FFFFFF", opacity=70, stroke=NONE)
d.shape("ellipse", "Glint R", x=558, y=544, width=5, height=4, fill="#FFFFFF", opacity=70, stroke=NONE)
# flat patient mouth + cheeks
d.path("M466,632 L534,632", "Mouth", fill=NONE, stroke=INK, strokeWidth=5, cap="round")
d.shape("ellipse", "Cheek L", x=396, y=600, width=38, height=20,
        fill="#B46A4E", opacity=45, stroke=NONE)
d.shape("ellipse", "Cheek R", x=566, y=600, width=38, height=20,
        fill="#B46A4E", opacity=45, stroke=NONE)

# --- cobwebs + drift lines --------------------------------------------------------
d.path("M370,458 C380,480 392,494 410,500 M370,458 C384,468 398,472 414,474",
       "Cobweb L", fill=NONE, stroke="#E8D9B4", strokeWidth=2, opacity=30)
d.path("M630,458 C620,480 608,494 590,500 M630,458 C616,468 602,472 586,474",
       "Cobweb R", fill=NONE, stroke="#E8D9B4", strokeWidth=2, opacity=30)
for i, (y, x0, x1, o) in enumerate([(310,260,430,20),(350,300,470,16),
                                    (640,280,420,18),(680,620,760,14)]):
    d.path(f"M{x0},{y} L{x1},{y}", f"Drift line {i+1}", fill=NONE,
           stroke="#E8D9B4", strokeWidth=3, opacity=o, cap="round")
# drifting motes
for i, (x, y, w, o) in enumerate([(300,420,6,28),(700,400,7,24),(280,560,5,20),
                                  (720,580,6,26),(460,300,5,18),(560,290,6,22)]):
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#F0DCAC", opacity=o, stroke=NONE)
# sleepy z's off the lid corner
d.text("z", "Z1", x=620, y=396, size=20, font="Virelai Sans",
       color="#E8D9B4", justify="center")
d.text("z", "Z2", x=648, y=364, size=26, font="Virelai Sans",
       color="#E8D9B4", justify="center")

# --- captions ----------------------------------------------------------------------
d.text("DRIFTLOCKED POLICY BOX", "Name", x=500, y=930, size=52,
       font="Virelai Sans", color="#EFDFB4", justify="center")
r = d.text("SEALED SINCE JUNE 11", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#C0A878", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("435.driftlocked-policy-box-V1R00")
