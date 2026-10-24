#!/usr/bin/env python3
"""Predictive Pete — mascot portrait V1R00.
Pete beside the pinned city map: red high-risk zones, dashed patrol
route that circles back to HQ. 1000x1000. House style: gradients +
translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Predictive Pete — Mascot Portrait", 1000, 1000)

INK = "#332A33"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#0C1420"}, {"offset": 1, "color": "#050A10"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#456280"}, {"offset": 0.7, "color": "#2F4660"},
    {"offset": 1, "color": "#182838"}]}}
PAPER = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#D9D2BC"}, {"offset": 1, "color": "#B0A88E"}]}}
BOARD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4E3F2C"}, {"offset": 1, "color": "#322618"}]}}
FLOOR = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2E4056"}, {"offset": 1, "color": "#16222E"}]}}
BODY = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#D8E2EE"}, {"offset": 0.7, "color": "#A9B9CC"},
    {"offset": 1, "color": "#788CA6"}]}}
UNIFORM = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3E5478"}, {"offset": 1, "color": "#263A56"}]}}
ZONE = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E86A5E"}, {"offset": 1, "color": "#B04038"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#6A8AAC", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C9DCEA", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(190,240,8),(800,230,7),(160,520,9),(830,540,8),
                               (240,760,7),(760,740,9),(130,390,6),(865,390,7),
                               (390,110,7),(610,110,8),(330,820,6),(665,815,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#3A5570", opacity=45, stroke=NONE)

# --- floor ----------------------------------------------------------------------
d.shape("ellipse", "Floor", x=170, y=625, width=660, height=130,
        fill=FLOOR, stroke=NONE, opacity=92)
d.shape("ellipse", "Pete shadow", x=280, y=676, width=160, height=30,
        fill="#060A10", opacity=55, stroke=NONE)

# --- the patrol map on its board ---------------------------------------------------
d.shape("rectangle", "Board", x=528, y=236, width=310, height=356,
        fill=BOARD, stroke=INK, strokeWidth=6, radius=8)
d.shape("rectangle", "Map", x=546, y=254, width=274, height=320,
        fill=PAPER, stroke="#8A8064", strokeWidth=3)
# street grid
for i, x in enumerate(range(578, 812, 42)):
    d.path(f"M{x},258 L{x},570", f"St v{i+1}", fill=NONE,
           stroke="#9A9076", strokeWidth=2, opacity=55)
for i, y in enumerate(range(292, 566, 44)):
    d.path(f"M550,{y} L816,{y}", f"St h{i+1}", fill=NONE,
           stroke="#9A9076", strokeWidth=2, opacity=55)
# high-risk zones
for i, (x, y, r) in enumerate([(640,330,46),(748,452,40),(620,480,30)]):
    d.shape("ellipse", f"Zone {i+1}", x=x-r, y=y-r, width=2*r, height=2*r,
            fill=ZONE, opacity=30, stroke=NONE)
    d.shape("ellipse", f"Zone ring {i+1}", x=x-r, y=y-r, width=2*r, height=2*r,
            fill=NONE, stroke="#B04038", strokeWidth=3, opacity=70)
    d.path(f"M{x},{y-r+8} L{x},{y+6} M{x},{y+14} L{x},{y+16}",
           f"Zone mark {i+1}", fill=NONE, stroke="#8A2E28", strokeWidth=5, cap="round")
# patrol route: dashed loop from HQ, circling through the zones, back to HQ
cx, cy, rx, ry = 676, 424, 86, 96
pts = []
for t in [i*0.26 for i in range(25)]:
    a = -math.pi/2 + t
    pts.append((cx + rx*math.cos(a), cy + ry*math.sin(a)))
for i in range(len(pts)-1):
    if i % 3 != 2:
        (x0,y0),(x1,y1) = pts[i], pts[i+1]
        d.path(f"M{x0:.0f},{y0:.0f} L{x1:.0f},{y1:.0f}", f"Route dash {i+1}",
               fill=NONE, stroke="#B5762E", strokeWidth=5, cap="round")
# return leg + arrowhead into HQ (HQ sits at 600,540 — route end curls back)
d.path("M610,516 L600,536 M610,516 L594,512", "Route return", fill=NONE,
       stroke="#B5762E", strokeWidth=5, cap="round", join="round")
# HQ pin
d.shape("ellipse", "HQ pin", x=590, y=532, width=20, height=20,
        fill="#3E5478", stroke=INK, strokeWidth=3)
d.shape("ellipse", "HQ dot", x=596, y=538, width=8, height=8,
        fill="#D8E2EE", stroke=NONE)
d.text("HQ", "HQ label", x=600, y=564, size=11, font="Virelai Sans",
       color="#4A3F2C", justify="center")
# map header + pins
d.shape("rectangle", "Map header", x=546, y=254, width=274, height=24,
        fill="#B0A88E", stroke=NONE)
d.text("CITY GRID · PATROL", "Map title", x=683, y=271, size=12,
       font="Virelai Sans", color="#4A3F2C", justify="center")
d.shape("ellipse", "Pin L", x=552, y=258, width=10, height=10,
        fill="#B04038", stroke=INK, strokeWidth=2)
d.shape("ellipse", "Pin R", x=804, y=258, width=10, height=10,
        fill="#B04038", stroke=INK, strokeWidth=2)

# --- Pete ---------------------------------------------------------------------------
# legs + shoes
d.path("M350,646 L346,682", "Leg L", fill=NONE, stroke="#788CA6",
       strokeWidth=13, cap="round")
d.path("M392,646 L396,682", "Leg R", fill=NONE, stroke="#6A7E98",
       strokeWidth=13, cap="round")
d.shape("ellipse", "Shoe L", x=330, y=676, width=32, height=15, fill=INK, stroke=NONE)
d.shape("ellipse", "Shoe R", x=384, y=676, width=32, height=15, fill=INK, stroke=NONE)
# body
d.path("M374,470 C428,470 452,514 449,560 C446,612 416,648 374,648 "
       "C332,648 302,612 299,560 C296,514 320,470 374,470 Z",
       "Pete body", fill=BODY, stroke=INK, strokeWidth=6)
# uniform jacket lower half
d.path("M336,540 C342,596 356,626 374,646 C392,626 406,596 412,540 "
       "C396,552 352,552 336,540 Z",
       "Jacket", fill=UNIFORM, stroke=INK, strokeWidth=4, join="round")
d.shape("ellipse", "Body highlight", x=318, y=482, width=66, height=26,
        fill="#FFFFFF", opacity=20, stroke=NONE)
# cap
d.path("M334,462 L334,438 C334,420 352,412 374,412 C396,412 414,420 414,438 L414,462 Z",
       "Cap crown", fill=UNIFORM, stroke=INK, strokeWidth=5, join="round")
d.shape("ellipse", "Cap brim", x=324, y=454, width=100, height=15,
        fill="#1E2C44", stroke=INK, strokeWidth=4)
# face: watching the map, hand to chin
d.shape("ellipse", "Eye L", x=344, y=500, width=14, height=18, fill=INK, stroke=NONE)
d.shape("ellipse", "Eye R", x=386, y=500, width=14, height=18, fill=INK, stroke=NONE)
d.shape("ellipse", "Glint L", x=348, y=504, width=4, height=4, fill="#FFFFFF", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=390, y=504, width=4, height=4, fill="#FFFFFF", opacity=90, stroke=NONE)
d.shape("ellipse", "Cheek L", x=330, y=524, width=22, height=13,
        fill="#C98A9A", opacity=50, stroke=NONE)
d.shape("ellipse", "Cheek R", x=396, y=524, width=22, height=13,
        fill="#C98A9A", opacity=50, stroke=NONE)
d.path("M358,544 C366,549 378,549 386,542", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
# pointer arm toward the map + thin pointer stick
d.path("M446,540 C472,522 494,502 512,482", "Arm point", fill=NONE,
       stroke="#A9B9CC", strokeWidth=12, cap="round")
d.shape("ellipse", "Hand stick", x=506, y=474, width=17, height=15,
        fill="#D8E2EE", stroke=INK, strokeWidth=3)
d.path("M514,480 L582,400", "Pointer", fill=NONE, stroke="#8A6B42",
       strokeWidth=5, cap="round")
# pointer tip rests in zone 1
d.shape("ellipse", "Pointer tip", x=580, y=396, width=9, height=9,
        fill="#8A6B42", stroke=NONE)
# other hand to chin
d.path("M312,560 C300,548 300,534 310,524", "Arm chin", fill=NONE,
       stroke="#A9B9CC", strokeWidth=11, cap="round")
d.shape("ellipse", "Hand chin", x=304, y=516, width=16, height=14,
        fill="#D8E2EE", stroke=INK, strokeWidth=3)

# --- captions ---------------------------------------------------------------------------
d.text("PREDICTIVE PETE", "Name", x=500, y=930, size=60,
       font="Virelai Sans", color="#D5E2EC", justify="center")
r = d.text("HIGH-RISK ZONE PATROL", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#96B2C6", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("441.predictive-pete-V1R00")
