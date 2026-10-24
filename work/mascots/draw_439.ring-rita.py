#!/usr/bin/env python3
"""Ring Rita — mascot portrait V1R00.
Doorbell camera on the front porch at night; her field-of-view cone
spills onto the neighboring porch. 1000x1000. House style: gradients +
translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Ring Rita — Mascot Portrait", 1000, 1000)

INK = "#332A33"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#0B1322"}, {"offset": 1, "color": "#05080F"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#3E547C"}, {"offset": 0.7, "color": "#2A3B5C"},
    {"offset": 1, "color": "#16203A"}]}}
WALL = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#33486E"}, {"offset": 1, "color": "#1C2A48"}]}}
CAM = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E4EAF2"}, {"offset": 0.7, "color": "#B0BCCC"},
    {"offset": 1, "color": "#7E8CA0"}]}}
LENS = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#5E80B8"}, {"offset": 0.6, "color": "#2E4468"},
    {"offset": 1, "color": "#141E30"}]}}
LAMPGLOW = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F5CE7E"}, {"offset": 1, "color": "#F5CE7E"}]}}
FOV = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#B8D4F0"}, {"offset": 1, "color": "#6E94C4"}]}}
PORCH = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2E3C5C"}, {"offset": 1, "color": "#18223C"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#5E7AA8", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C8D8F0", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(190,240,8),(800,230,7),(160,520,9),(830,540,8),
                               (240,760,7),(760,740,9),(130,390,6),(865,390,7),
                               (390,110,7),(610,110,8),(330,820,6),(665,815,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#35486C", opacity=45, stroke=NONE)

# --- her porch wall: clapboard siding, left edge on the disc arc -----------------
d.path("M470,180 L183,185 A420,420 0 0 0 156,700 L470,700 Z", "Wall",
       fill=WALL, stroke=NONE)
for i, y in enumerate(range(220, 700, 44)):
    d.path(f"M168,{y} L470,{y}", f"Siding {i+1}", fill=NONE,
           stroke="#141E30", strokeWidth=4, opacity=55)
d.path("M470,180 L470,700", "House corner", fill=NONE, stroke="#101828",
       strokeWidth=8, opacity=70)

# --- porch lamp, warm -------------------------------------------------------------
d.shape("ellipse", "Lamp glow", x=170, y=205, width=190, height=160,
        fill="#F5CE7E", opacity=13, stroke=NONE)
d.path("M218,236 L262,236 M240,236 L240,218", "Lamp arm", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
d.path("M226,236 L254,236 L260,268 L220,268 Z", "Lantern", fill=LAMPGLOW,
       stroke=INK, strokeWidth=4, join="round")
d.path("M226,236 L254,236", "Lantern cap", fill=NONE, stroke=INK, strokeWidth=5)

# --- neighbor's porch, right edge, inside her cone -------------------------------
d.shape("rectangle", "Neighbor post", x=748, y=280, width=22, height=360,
        fill=PORCH, stroke=INK, strokeWidth=4, radius=3)
for i, y in enumerate([470, 552]):
    d.shape("rectangle", f"Neighbor rail {i+1}", x=620, y=y, width=150, height=14,
            fill=PORCH, stroke=INK, strokeWidth=3, radius=4)
for i, x in enumerate([652, 696]):
    d.shape("rectangle", f"Baluster {i+1}", x=x, y=484, width=10, height=68,
            fill=PORCH, stroke=INK, strokeWidth=3)
# their door edge + number
d.shape("rectangle", "Neighbor door", x=786, y=300, width=60, height=240,
        fill="#243254", stroke=INK, strokeWidth=4)
d.text("2B", "Neighbor number", x=816, y=360, size=15, font="Virelai Sans",
       color="#7E94BC", justify="center")

# --- her field of view, washing over the neighbor porch --------------------------
d.path("M382,432 L836,290 L836,650 Z", "FOV cone", fill=FOV,
       opacity=12, stroke=NONE)
d.path("M382,432 L836,290 M382,432 L836,650", "FOV edges", fill=NONE,
       stroke="#B8D4F0", strokeWidth=3, opacity=30)
# faint scan sweeps inside the cone
d.path("M382,432 L836,470", "FOV mid", fill=NONE, stroke="#B8D4F0",
       strokeWidth=2, opacity=18)
d.shape("ellipse", "FOV footprint", x=560, y=430, width=290, height=170,
        fill="#B8D4F0", opacity=7, stroke=NONE)

# --- doormat ----------------------------------------------------------------------
d.shape("rectangle", "Mat", x=280, y=664, width=150, height=30,
        fill="#243452", stroke=INK, strokeWidth=4, radius=5)
d.text("WELCOME", "Mat text", x=355, y=684, size=12, font="Virelai Sans",
       color="#5E7AA8", justify="center")

# --- Rita: the doorbell camera ----------------------------------------------------
# mounting bracket on the wall
d.shape("rectangle", "Bracket", x=296, y=430, width=20, height=52,
        fill="#4A5878", stroke=INK, strokeWidth=4, radius=4)
# body, slight tilt toward the neighbor side
d.shape("rectangle", "Rita body", x=312, y=368, width=96, height=158,
        fill=CAM, stroke=INK, strokeWidth=6, radius=16)
d.shape("ellipse", "Body highlight", x=322, y=378, width=48, height=20,
        fill="#FFFFFF", opacity=30, stroke=NONE)
# the lens is her eye
d.shape("ellipse", "Lens ring", x=334, y=392, width=64, height=64,
        fill="#1C2840", stroke=INK, strokeWidth=5)
d.shape("ellipse", "Lens", x=342, y=400, width=48, height=48,
        fill=LENS, stroke="#0E1626", strokeWidth=3)
d.shape("ellipse", "Iris glint", x=354, y=410, width=14, height=12,
        fill="#C8DCF4", opacity=85, stroke=NONE)
d.shape("ellipse", "Iris glint 2", x=372, y=428, width=6, height=6,
        fill="#8FB0DC", opacity=60, stroke=NONE)
# recording LED + little smile under the lens
d.shape("ellipse", "REC dot", x=388, y=466, width=10, height=10,
        fill="#E86A6A", stroke=NONE)
d.path("M344,478 C354,486 368,486 378,478", "Smile", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
# bell button at the base
d.shape("ellipse", "Button ring", x=348, y=492, width=34, height=26,
        fill="#3E4C66", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Button", x=356, y=497, width=18, height=16,
        fill="#6E80A0", stroke=NONE)
# one little arm, gesturing at the neighbor porch
d.path("M408,470 C436,458 462,452 486,452", "Arm point", fill=NONE,
       stroke="#B0BCCC", strokeWidth=11, cap="round")
d.shape("ellipse", "Hand point", x=480, y=444, width=17, height=15,
        fill="#E4EAF2", stroke=INK, strokeWidth=3)

# --- captions ----------------------------------------------------------------------
d.text("RING RITA", "Name", x=500, y=930, size=60,
       font="Virelai Sans", color="#D4E2F4", justify="center")
r = d.text("PORCH CAMERA · ADJACENT COVERAGE", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#94AACB", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("439.ring-rita-V1R00")
