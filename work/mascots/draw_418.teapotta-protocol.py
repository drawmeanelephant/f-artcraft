#!/usr/bin/env python3
"""Teapotta Protocol — mascot portrait V1R00. HTTP 418, "I'm a teapot".
Short, stout teapot floating in a digital space. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Teapotta Protocol — Mascot Portrait", 1000, 1000)

INK = "#4A2E33"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#12283A"}, {"offset": 1, "color": "#060E18"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#D8EDF0"}, {"offset": 0.7, "color": "#A4CBD4"},
    {"offset": 1, "color": "#6E99A8"}]}}
BODY_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#FDF3DF"}, {"offset": 0.65, "color": "#F0D5AC"},
    {"offset": 1, "color": "#CE9F6E"}]}}
TRIM_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E88A5F"}, {"offset": 1, "color": "#B85C3E"}]}}

# --- backdrop + plate --------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
# digital grid, faint
for i, y in enumerate([120, 240, 360, 480, 600, 720, 840]):
    d.path(f"M0,{y} L1000,{y}", f"Gridline {i+1}", fill=NONE,
           stroke="#2E5A70", strokeWidth=1.5, opacity=18)
for i, x in enumerate([170, 380, 620, 830]):
    d.path(f"M{x},0 L{x},1000", f"Vgrid {i+1}", fill=NONE,
           stroke="#2E5A70", strokeWidth=1.5, opacity=12)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#4F8291", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E4F5F4", strokeWidth=3, opacity=55)

# digital confetti on the plate: tiny squares + plus marks, kept inside the disc
for i, (x, y, s) in enumerate([(210,220,12),(780,200,10),(250,690,9),(740,660,12),
                               (170,450,8),(830,430,10),(330,150,8),(680,140,9),
                               (300,780,10),(700,770,9),(150,330,7),(850,560,8)]):
    d.shape("rectangle", f"Pixel {i+1}", x=x, y=y, width=s, height=s,
            fill="#9FE3EA", opacity=30, stroke=NONE)
for i, (x, y) in enumerate([(255,320),(760,300),(205,560),(795,610),(440,140),(560,150),(380,800),(625,795)]):
    d.path(f"M{x-9},{y} L{x+9},{y} M{x},{y-9} L{x},{y+9}", f"Plus {i+1}",
           fill=NONE, stroke="#C9F0F0", strokeWidth=4, opacity=40, cap="round")

# --- steam curls --------------------------------------------------------------
d.path("M455,372 C435,340 480,322 462,290 C450,268 470,252 478,238",
       "Steam L", fill=NONE, stroke="#FFFFFF", strokeWidth=9, opacity=45, cap="round")
d.path("M548,378 C570,348 528,326 550,296 C564,276 548,258 540,246",
       "Steam R", fill=NONE, stroke="#FFFFFF", strokeWidth=8, opacity=35, cap="round")

# --- teapot -------------------------------------------------------------------
# spout (behind body, left)
d.path("M392,572 C356,556 318,522 306,470 L300,446 C298,434 312,428 320,438 "
       "C344,462 376,490 400,506 C408,528 404,552 392,572 Z",
       "Spout", fill=BODY_GRAD, stroke=INK, strokeWidth=6, join="round")
d.path("M306,470 L300,446 C298,434 312,428 320,438", "Spout lip",
       fill=NONE, stroke=INK, strokeWidth=6, cap="round")
# handle (behind body, right)
d.path("M622,506 C700,494 716,606 628,610", "Handle",
       fill=NONE, stroke="#C68E5E", strokeWidth=30, cap="round")
d.path("M622,506 C700,494 716,606 628,610", "Handle ink",
       fill=NONE, stroke=INK, strokeWidth=6, cap="round", opacity=70)
# body: short, stout pot
d.path("M352,560 C352,478 416,428 500,428 C584,428 648,478 648,560 "
       "C648,628 596,676 500,676 C404,676 352,628 352,560 Z",
       "Body", fill=BODY_GRAD, stroke=INK, strokeWidth=7, join="round")
# belly band, teapot glaze stripe
d.path("M360,588 C420,612 580,612 640,588 C636,640 590,672 500,672 C410,672 364,640 360,588 Z",
       "Glaze band", fill=TRIM_GRAD, stroke=NONE, opacity=80)
# body highlight
d.shape("ellipse", "Body highlight", x=386, y=462, width=150, height=78,
        fill="#FFFFFF", opacity=35, stroke=NONE)
# lid: dome + rim + knob
d.shape("ellipse", "Lid rim", x=420, y=404, width=160, height=44,
        fill=TRIM_GRAD, stroke=INK, strokeWidth=5)
d.path("M436,412 C450,378 550,378 564,412 Z", "Lid dome",
       fill=BODY_GRAD, stroke=INK, strokeWidth=5)
d.shape("ellipse", "Knob", x=487, y=362, width=26, height=24,
        fill=TRIM_GRAD, stroke=INK, strokeWidth=5)
# face: calm, self-aware
d.shape("ellipse", "Eye L", x=446, y=518, width=24, height=30, fill="#33222A", stroke=NONE)
d.shape("ellipse", "Eye R", x=530, y=518, width=24, height=30, fill="#33222A", stroke=NONE)
d.shape("ellipse", "Glint L", x=452, y=524, width=7, height=7, fill="#FFFFFF", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=536, y=524, width=7, height=7, fill="#FFFFFF", opacity=90, stroke=NONE)
d.path("M462,566 C480,582 520,582 538,566", "Smile",
       fill=NONE, stroke=INK, strokeWidth=7, cap="round")
d.shape("ellipse", "Blush L", x=412, y=552, width=34, height=16, fill="#E88A5F", opacity=40, stroke=NONE)
d.shape("ellipse", "Blush R", x=554, y=552, width=34, height=16, fill="#E88A5F", opacity=40, stroke=NONE)

# --- floating: hover shadow + levitation ticks --------------------------------
d.shape("ellipse", "Hover shadow", x=372, y=724, width=256, height=34,
        fill="#274B57", opacity=40, stroke=NONE)
for i, (x, w) in enumerate([(432,26),(487,34),(556,26)]):
    d.path(f"M{x},764 L{x+w},764", f"Levitation tick {i+1}",
           fill=NONE, stroke="#C9F0F0", strokeWidth=5, opacity=55, cap="round")

# --- name + role ----------------------------------------------------------------
d.text("TEAPOTTA PROTOCOL", "Name", x=500, y=930, size=58, font="Virelai Sans",
       color="#D5ECEF", justify="center")
d.text(" ".join("I'M A TEAPOT"), "Role", x=500, y=968, size=23, font="Virelai Sans",
       color="#8FBEC9", justify="center")

d.finish("418.teapotta-protocol-V1R00")
