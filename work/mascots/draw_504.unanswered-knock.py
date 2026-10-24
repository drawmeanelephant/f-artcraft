#!/usr/bin/env python3
"""The Unanswered Knock — mascot portrait V1R00.
A small expectant wisp suspended mid-knock at a closed door; no answer
arriving. 1000x1000. Gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("The Unanswered Knock — Mascot Portrait", 1000, 1000)

INK = "#2C2018"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#161410"}, {"offset": 1, "color": "#0A0806"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#5E5244"}, {"offset": 0.7, "color": "#3E362C"},
    {"offset": 1, "color": "#241E16"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#342A20"}, {"offset": 1, "color": "#181210"}]}}
DOOR = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6E4A2E"}, {"offset": 1, "color": "#3E2818"}]}}
FRAME = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#8A6238"}, {"offset": 1, "color": "#5A3E22"}]}}
WISP = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#DCEAF2"}, {"offset": 0.7, "color": "#9AB4C4"},
    {"offset": 1, "color": "#66849A"}]}}
BRASS = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F0CE7E"}, {"offset": 1, "color": "#A87E38"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#8A7A5E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8DCC4", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(193,234,8),(801,229,7),(157,526,9),(837,544,8),
                               (246,766,7),(754,748,9),(133,394,6),(865,389,7),
                               (391,112,7),(613,109,8),(333,824,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#4C4234", opacity=45, stroke=NONE)

# --- floor: bottom segment closed on the disc's own arc -----------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#14100C",
       strokeWidth=4, opacity=70)

# --- wall wainscot behind the door ----------------------------------------------
d.path("M300,560 L500,560 M760,560 L830,560", "Wainscot", fill=NONE,
       stroke="#4C4234", strokeWidth=5, opacity=50)

# --- the closed door: no. 504 ----------------------------------------------------
d.shape("rectangle", "Door frame", x=500, y=185, width=265, height=515,
        fill=FRAME, stroke=INK, strokeWidth=6, radius=4)
d.shape("rectangle", "Door slab", x=515, y=200, width=235, height=500,
        fill=DOOR, stroke=INK, strokeWidth=5, radius=3)
# recessed panels
for i, y in enumerate([225, 415]):
    d.shape("rectangle", f"Panel {i+1}", x=540, y=y, width=185, height=160,
            fill=NONE, stroke="#2C1C10", strokeWidth=4, radius=6, opacity=80)
    d.shape("rectangle", f"Panel hi {i+1}", x=545, y=y+5, width=175, height=150,
            fill=NONE, stroke="#8A6038", strokeWidth=2, radius=5, opacity=50)
# number plate: 504
d.shape("rectangle", "Number plate", x=595, y=165, width=75, height=34,
        fill=BRASS, stroke=INK, strokeWidth=4, radius=6)
d.text("504", "Door number", x=615, y=189, size=19, font="Virelai Sans",
       color="#3E2C14", justify="left")
# knob + keyhole
d.shape("ellipse", "Knob", x=705, y=430, width=26, height=26,
        fill=BRASS, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Keyhole", x=712, y=462, width=11, height=18,
        fill="#1A100A", stroke=NONE)
# mail slot: dark, shut, nothing coming through
d.shape("rectangle", "Mail slot", x=555, y=610, width=130, height=26,
        fill="#241608", stroke=INK, strokeWidth=4, radius=10)
# peephole
d.shape("ellipse", "Peephole", x=618, y=290, width=14, height=14,
        fill="#241608", stroke=INK, strokeWidth=3)
# the seam of darkness under the door — deliberately unlit
d.path("M515,700 L750,700", "Door seam", fill=NONE, stroke="#0A0604",
       strokeWidth=5)

# --- knock marks at the contact point ---------------------------------------------
for i, r_ in enumerate([0, 1, 2]):
    y0 = 300 - i*6
    d.path(f"M{468-i*22},{y0-46} C{455-i*24},{y0-20} {455-i*24},{y0+20} {468-i*22},{y0+46}",
           f"Knock ring {i+1}", fill=NONE, stroke="#E8DCC4",
           strokeWidth=5-i, cap="round", opacity=70-i*18)

# --- the Knock: a suspended little wisp, fist to the door ---------------------------
# faint halo where it hovers
d.shape("ellipse", "Wisp halo", x=280, y=380, width=200, height=210,
        fill="#C4DCEA", opacity=10, stroke=NONE)
# wisp body, slightly translucent, tail curling down
d.path("M390,395 C450,395 480,440 470,485 C462,520 430,545 395,545 "
       "C355,545 322,520 318,482 C315,445 335,395 390,395 Z",
       "Wisp body", fill=WISP, stroke=INK, strokeWidth=6, opacity=92)
d.path("M400,545 C415,575 400,605 375,615 C392,618 408,610 415,595 "
       "C425,575 420,555 408,545 Z",
       "Wisp tail", fill=WISP, stroke=INK, strokeWidth=5, opacity=85)
# top highlight + under-shadow
d.shape("ellipse", "Wisp hi", x=345, y=412, width=80, height=30,
        fill="#FFFFFF", opacity=25, stroke=NONE)
d.path("M335,520 C360,535 415,535 445,520 C415,530 360,530 335,520 Z",
       "Wisp shade", fill="#5E7A8E", opacity=50, stroke=NONE)
# extended knocking arm, fist at the door edge
d.path("M465,445 C485,435 495,425 505,415", "Knocking arm", fill=NONE,
       stroke="#9AB4C4", strokeWidth=15, cap="round", opacity=90)
d.shape("ellipse", "Fist", x=495, y=398, width=26, height=26,
        fill="#B8CCDA", stroke=INK, strokeWidth=4)
# face: wide expectant eyes, small open mouth
d.shape("ellipse", "Eye L", x=350, y=440, width=20, height=26,
        fill="#241F2C", stroke=NONE)
d.shape("ellipse", "Eye R", x=400, y=440, width=20, height=26,
        fill="#241F2C", stroke=NONE)
d.shape("ellipse", "Glint L", x=355, y=445, width=6, height=6,
        fill="#FFFFFF", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=405, y=445, width=6, height=6,
        fill="#FFFFFF", opacity=90, stroke=NONE)
d.shape("ellipse", "Open mouth", x=375, y=492, width=18, height=14,
        fill="#241F2C", stroke=NONE)
# suspended dust motes: time passing
for i, (x, y, w) in enumerate([(300,320,6),(330,290,5),(255,420,7),(240,350,5),(285,480,5)]):
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#D8C9A8", opacity=45, stroke=NONE)

# --- the answer that is not arriving --------------------------------------------------
d.text(". . .", "Ellipsis", x=580, y=525, size=44, font="Virelai Sans",
       color="#9A8A68", justify="left")

# --- captions ------------------------------------------------------------------
d.text("THE UNANSWERED KNOCK", "Name", x=500, y=930, size=50, font="Virelai Sans",
       color="#E8DCC4", justify="center")
r = d.text("GATEWAY TIMEOUT ENTITY", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#B09E7E", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("504.unanswered-knock-V1R00")
