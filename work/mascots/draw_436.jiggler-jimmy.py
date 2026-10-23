#!/usr/bin/env python3
"""Jiggler Jimmy — mascot portrait V1R00.
USB dongle keeping a mouse awake, dashboard chip glowing ACTIVE.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Jiggler Jimmy — Mascot Portrait", 1000, 1000)

INK = "#332A33"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#0D1A1D"}, {"offset": 1, "color": "#050D0E"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#3F7076"}, {"offset": 0.7, "color": "#2A4E55"},
    {"offset": 1, "color": "#163038"}]}}
DESK = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2E4A50"}, {"offset": 1, "color": "#172A2E"}]}}
BODY = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#7FD0CE"}, {"offset": 0.7, "color": "#54A8A9"},
    {"offset": 1, "color": "#357880"}]}}
METAL = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#D8DEE2"}, {"offset": 1, "color": "#93A0A8"}]}}
MOUSE = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#5E7E88"}, {"offset": 0.7, "color": "#415E68"},
    {"offset": 1, "color": "#2A4048"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#5E9A9C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C8ECEA", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(190,240,8),(800,230,7),(160,520,9),(830,540,8),
                               (240,760,7),(760,740,9),(130,390,6),(865,390,7),
                               (390,110,7),(610,110,8),(330,820,6),(665,815,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#3A626A", opacity=45, stroke=NONE)

# --- desk ----------------------------------------------------------------------
d.shape("ellipse", "Desk", x=170, y=615, width=660, height=135,
        fill=DESK, stroke=NONE, opacity=92)
d.shape("ellipse", "Jimmy shadow", x=410, y=640, width=170, height=34,
        fill="#081114", opacity=50, stroke=NONE)
d.shape("ellipse", "Mouse shadow", x=575, y=635, width=160, height=30,
        fill="#081114", opacity=45, stroke=NONE)

# --- dashboard chip: green ACTIVE status ----------------------------------------
d.shape("ellipse", "Chip glow", x=268, y=222, width=230, height=100,
        fill="#4ADE80", opacity=10, stroke=NONE)
d.shape("rectangle", "Chip", x=278, y=240, width=210, height=64,
        fill="#0E2226", stroke="#4A7278", strokeWidth=4, radius=12, opacity=95)
d.shape("ellipse", "Dot glow", x=296, y=258, width=28, height=28,
        fill="#4ADE80", opacity=30, stroke=NONE)
d.shape("ellipse", "Dot", x=300, y=262, width=20, height=20,
        fill="#58E896", stroke="#1E5A3E", strokeWidth=3)
d.text("ACTIVE", "Chip label", x=334, y=280, size=20, font="Virelai Sans",
       color="#8FE8B0", justify="left")
# cable from chip down to the desk, as if reporting the mouse
d.path("M440,304 C470,360 480,430 470,480", "Chip lead", fill=NONE,
       stroke="#4A7278", strokeWidth=3, opacity=50)

# --- the mouse -----------------------------------------------------------------
# cable curling away to the rim's edge of the scene
d.path("M712,568 C790,556 830,590 824,640 C820,672 800,690 780,694",
       "Mouse cable", fill=NONE, stroke="#243840", strokeWidth=6, cap="round")
# body
d.shape("ellipse", "Mouse", x=590, y=545, width=140, height=92,
        fill=MOUSE, stroke=INK, strokeWidth=6)
# button split + wheel
d.path("M665,545 C660,560 660,575 665,591", "Button split", fill=NONE,
       stroke=INK, strokeWidth=4, opacity=70)
d.shape("ellipse", "Wheel", x=654, y=566, width=16, height=24,
        fill="#1E3038", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Mouse highlight", x=610, y=556, width=50, height=18,
        fill="#FFFFFF", opacity=14, stroke=NONE)
# jiggle marks above the mouse
for i, (x, y) in enumerate([(618,508),(650,494),(684,508)]):
    d.path(f"M{x},{y} C{x-10},{y+12} {x-10},{y+24} {x},{y+36}",
           f"Jiggle {i+1}", fill=NONE, stroke="#9FD8D4", strokeWidth=5,
           opacity=55, cap="round")

# --- Jimmy: the dongle ------------------------------------------------------------
# legs + feet
d.path("M452,592 L450,622", "Leg L", fill=NONE, stroke="#357880",
       strokeWidth=13, cap="round")
d.path("M500,592 L504,622", "Leg R", fill=NONE, stroke="#2E6A72",
       strokeWidth=13, cap="round")
d.shape("ellipse", "Shoe L", x=434, y=616, width=32, height=15,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Shoe R", x=492, y=616, width=32, height=15,
        fill=INK, stroke=NONE)
# body: rounded rect dongle
d.shape("rectangle", "Jimmy body", x=416, y=415, width=120, height=182,
        fill=BODY, stroke=INK, strokeWidth=6, radius=18)
d.shape("ellipse", "Body highlight", x=428, y=428, width=60, height=26,
        fill="#FFFFFF", opacity=20, stroke=NONE)
d.path("M500,570 C490,584 470,590 452,586 C470,592 500,590 514,574 Z",
       "Body shadow", fill="#24555C", opacity=45, stroke=NONE)
# USB-A plug hat
d.shape("rectangle", "Plug", x=446, y=378, width=60, height=42,
        fill=METAL, stroke=INK, strokeWidth=5, radius=6)
d.shape("rectangle", "Contact 1", x=456, y=388, width=14, height=10,
        fill="#3E4A52", stroke=NONE)
d.shape("rectangle", "Contact 2", x=482, y=388, width=14, height=10,
        fill="#3E4A52", stroke=NONE)
d.path("M452,415 L500,415", "Plug seam", fill=NONE, stroke="#5A666E",
       strokeWidth=4, opacity=60)
# face: bright eyes + confident smirk
d.shape("ellipse", "Eye L", x=446, y=478, width=17, height=21, fill=INK, stroke=NONE)
d.shape("ellipse", "Eye R", x=492, y=478, width=17, height=21, fill=INK, stroke=NONE)
d.shape("ellipse", "Glint L", x=450, y=482, width=5, height=5, fill="#FFFFFF", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=496, y=482, width=5, height=5, fill="#FFFFFF", opacity=90, stroke=NONE)
d.shape("ellipse", "Cheek L", x=428, y=508, width=26, height=15,
        fill="#E89A8C", opacity=50, stroke=NONE)
d.shape("ellipse", "Cheek R", x=502, y=508, width=26, height=15,
        fill="#E89A8C", opacity=50, stroke=NONE)
d.path("M462,532 C476,542 496,542 510,530", "Smirk", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
# etched USB glyph low on the body
d.path("M476,584 L476,556 M476,568 L468,562 M476,562 L484,556",
       "USB glyph", fill=NONE, stroke="#24555C", strokeWidth=4,
       cap="round", opacity=70)
d.shape("ellipse", "USB dot", x=472, y=550, width=8, height=8,
        fill="#24555C", opacity=70, stroke=NONE)

# --- arms: one pressing the mouse, one thumbs-up --------------------------------
d.path("M534,500 C560,520 580,540 600,556", "Arm press", fill=NONE,
       stroke="#54A8A9", strokeWidth=13, cap="round")
d.shape("ellipse", "Finger press", x=594, y=548, width=20, height=17,
        fill="#7FD0CE", stroke=INK, strokeWidth=3)
d.path("M418,494 C398,478 390,458 394,438", "Arm up", fill=NONE,
       stroke="#54A8A9", strokeWidth=13, cap="round")
d.shape("ellipse", "Thumb hand", x=384, y=424, width=22, height=20,
        fill="#7FD0CE", stroke=INK, strokeWidth=3)
d.path("M388,424 L392,410", "Thumb", fill=NONE, stroke="#7FD0CE",
       strokeWidth=8, cap="round")

# --- captions --------------------------------------------------------------------
d.text("JIGGLER JIMMY", "Name", x=500, y=930, size=60,
       font="Virelai Sans", color="#D0EEE9", justify="center")
r = d.text("USB MOUSE MOVER · ALWAYS ACTIVE", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#8FC0BC", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("436.jiggler-jimmy-V1R00")
