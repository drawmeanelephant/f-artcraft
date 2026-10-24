#!/usr/bin/env python3
"""The Unmet Bell — mascot portrait V1R00.
A brass desk bell, never rung, on an untouched desk; behind it a promise
dashboard glowing amber and red with not one green light. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("The Unmet Bell — Mascot Portrait", 1000, 1000)

INK = "#2A2434"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#101420"}, {"offset": 1, "color": "#06070C"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#9AA4BC"}, {"offset": 0.7, "color": "#6B7488"},
    {"offset": 1, "color": "#3E4356"}]}}
PANEL = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#232836"}, {"offset": 1, "color": "#141822"}]}}
WOOD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6E5340"}, {"offset": 1, "color": "#41302A"}]}}
BRASS = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F0D68C"}, {"offset": 0.6, "color": "#C89A3E"},
    {"offset": 1, "color": "#8A5E1E"}]}}
BRASS_D = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#9A7430"}, {"offset": 1, "color": "#5E4218"}]}}
PAPER = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F4F0E4"}, {"offset": 1, "color": "#D8D2BC"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#565E78", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8DCE8", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(210,220,7),(782,208,6),(178,545,8),(818,540,7),
                               (252,758,7),(750,755,8),(395,120,7),(600,118,6),
                               (148,390,6),(855,385,7),(312,810,6),(685,808,7)]):
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#565E78", opacity=40, stroke=NONE)

# --- the promise dashboard -----------------------------------------------------
d.shape("rectangle", "Dashboard", x=240, y=185, width=520, height=290, radius=14,
        fill=PANEL, stroke=INK, strokeWidth=6)
d.path("M252,238 L748,238", "Panel header rule", fill=NONE,
       stroke="#3E4658", strokeWidth=3)
d.text("PROMISE BOARD", "Panel header", x=310, y=222, size=17,
       font="Virelai Sans", color="#8A92A8", justify="left")
# the SLA gauge, needle pinned at zero
d.path("M640,214 C640,186 664,166 692,166 C720,166 744,186 744,214",
       "Gauge arc", fill=NONE, stroke="#4A4F62", strokeWidth=8, cap="round")
d.path("M646,214 C646,191 666,174 692,174", "Gauge dead zone", fill=NONE,
       stroke="#A04A42", strokeWidth=8, cap="round", opacity=75)
d.path("M692,212 L654,192", "Gauge needle", fill=NONE, stroke="#D8DCE8",
       strokeWidth=4, cap="round")
d.shape("ellipse", "Gauge hub", x=686, y=206, width=12, height=12,
        fill="#D8DCE8", stroke=INK, strokeWidth=2)
# rows of indicator lamps — amber, red, off. never green.
rows = [
    ("INTAKE",    ["#C8912E", "#3A3F4E", "#A04A42", "#3A3F4E", "#3A3F4E", "#C8912E", "#3A3F4E"]),
    ("PROMISED",  ["#3A3F4E", "#A04A42", "#3A3F4E", "#C8912E", "#3A3F4E", "#3A3F4E", "#A04A42"]),
    ("SHIPPED",   ["#3A3F4E", "#3A3F4E", "#3A3F4E", "#3A3F4E", "#A04A42", "#3A3F4E", "#3A3F4E"]),
    ("SIGNED OFF",["#3A3F4E", "#3A3F4E", "#3A3F4E", "#3A3F4E", "#3A3F4E", "#3A3F4E", "#3A3F4E"]),
]
for ri, (label, lights) in enumerate(rows):
    y = 268 + ri * 48
    d.text(label, f"Row label {ri}", x=268, y=y+13, size=12,
           font="Virelai Sans", color="#6B7288", justify="left")
    for ci, color in enumerate(lights):
        x = 372 + ci * 52
        lit = color != "#3A3F4E"
        d.shape("ellipse", f"Lamp {ri}-{ci}", x=x, y=y, width=18, height=18,
                fill=color, stroke=INK, strokeWidth=3,
                opacity=95 if lit else 80)
        if lit:
            d.shape("ellipse", f"Lamp glow {ri}-{ci}", x=x-6, y=y-6,
                    width=30, height=30, fill=color, opacity=18, stroke=NONE)
# a fine cobweb in the panel's top-left corner: nobody has touched it
d.path("M248,196 C268,206 288,216 300,232 M248,196 C262,222 268,240 270,258 "
       "M262,210 C274,218 284,226 292,238", "Cobweb", fill=NONE,
       stroke="#C8CCDA", strokeWidth=2, opacity=35, cap="round")

# --- the desk ---------------------------------------------------------------------
d.path("M212,640 L788,640 L768,700 L232,700 Z", "Desk slab",
       fill=WOOD, stroke=INK, strokeWidth=6, join="round")
d.path("M216,642 L784,642", "Desk edge", fill=NONE, stroke="#C9A97A",
       strokeWidth=3, opacity=55)
# dust film on the untouched desk
d.shape("ellipse", "Dust L", x=250, y=648, width=140, height=18,
        fill="#C8CCDA", opacity=14, stroke=NONE)
d.shape("ellipse", "Dust R", x=610, y=650, width=150, height=16,
        fill="#C8CCDA", opacity=14, stroke=NONE)

# --- the tent card: PLEASE RING ---------------------------------------------------
d.path(rot_rect_path(668, 596, 118, 52, -6), "Tent card",
       fill=PAPER, stroke=INK, strokeWidth=4, join="round")
d.text("PLEASE RING", "Card text", x=664, y=590, size=12, font="Virelai Sans",
       color="#8A3444", justify="center")
d.text("FOR SERVICE", "Card text 2", x=666, y=608, size=10, font="Virelai Sans",
       color="#6E5844", justify="center")

# --- the bell ----------------------------------------------------------------------
d.shape("ellipse", "Bell shadow", x=370, y=644, width=260, height=24,
        fill="#241F30", opacity=55, stroke=NONE)
# plinth
d.shape("rectangle", "Bell plinth", x=384, y=632, width=232, height=36, radius=14,
        fill=BRASS_D, stroke=INK, strokeWidth=6)
# dome
d.path("M398,632 C398,556 442,508 500,508 C558,508 602,556 602,632 Z",
       "Bell dome", fill=BRASS, stroke=INK, strokeWidth=7, join="round")
# dome shading + shine
d.path("M540,530 C575,552 595,590 598,632 L560,632 C558,596 552,562 540,530 Z",
       "Dome shade", fill="#8A5E1E", opacity=30, stroke=NONE)
d.path("M428,600 C430,566 448,538 470,524", "Dome shine", fill=NONE,
       stroke="#FFF4D4", strokeWidth=10, cap="round", opacity=55)
# plunger: stem + button, untouched on top
d.shape("rectangle", "Plunger stem", x=492, y=480, width=16, height=32, radius=6,
        fill=BRASS_D, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Plunger button", x=480, y=458, width=40, height=28,
        fill=BRASS, stroke=INK, strokeWidth=5)
d.shape("ellipse", "Button glint", x=486, y=463, width=14, height=8,
        fill="#FFF4D4", opacity=70, stroke=NONE)
# the face, gazing up at the plunger it has never felt
d.shape("ellipse", "Eye L", x=452, y=572, width=20, height=26, fill="#FBF6E8",
        stroke=INK, strokeWidth=4)
d.shape("ellipse", "Eye R", x=528, y=572, width=20, height=26, fill="#FBF6E8",
        stroke=INK, strokeWidth=4)
d.shape("ellipse", "Pupil L", x=460, y=576, width=9, height=11, fill=INK, stroke=NONE)
d.shape("ellipse", "Pupil R", x=535, y=576, width=9, height=11, fill=INK, stroke=NONE)
d.path("M478,618 C490,614 510,614 522,618", "Flat mouth", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")

# --- captions ------------------------------------------------------------------
d.text("THE UNMET BELL", "Name", x=500, y=930, size=58, font="Virelai Sans",
       color="#E4E8F2", justify="center")
r = d.text("WARDEN OF UNKEPT PROMISES", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#9AA4C0", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("417.the-unmet-bell-V1R00")
