#!/usr/bin/env python3
"""Corridor Heat — mascot portrait V1R00.
A furred mascot in an institutional corridor — boardroom door left, light
still leaking under it; elevator right — holding a Geiger counter's probe
to the space between two boxes on the wall's organizational chart. The
needle is parked in the red. 1000x1000.
Gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Corridor Heat — Mascot Portrait", 1000, 1000)

INK = "#2C1E14"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1A0F08"}, {"offset": 1, "color": "#0A0604"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#7A5E44"}, {"offset": 0.7, "color": "#54402C"},
    {"offset": 1, "color": "#2E2016"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4A4038"}, {"offset": 1, "color": "#241C14"}]}}
WALL_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6F6A58"}, {"offset": 1, "color": "#4C483C"}]}}
DOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3E3630"}, {"offset": 1, "color": "#2A201A"}]}}
ELEV_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#827B6E"}, {"offset": 1, "color": "#57524A"}]}}
FUR_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#B8A488"}, {"offset": 0.7, "color": "#94816A"},
    {"offset": 1, "color": "#6E5E4C"}]}}
FUR_DARK = "#7A6A56"
GEIGER_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5C6148"}, {"offset": 1, "color": "#434730"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#B08A62", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F0DCBC", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(193,234,8),(801,229,7),(157,526,9),(837,544,8),
                               (246,766,7),(754,748,9),(133,394,6),(865,389,7),
                               (391,112,7),(613,109,8),(333,824,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#5E4832", opacity=45, stroke=NONE)

# --- floor ---------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#140C08",
       strokeWidth=4, opacity=70)

# --- the corridor wall -------------------------------------------------------------
d.shape("rectangle", "Corridor wall", x=205, y=225, width=590, height=475,
        fill=WALL_GRAD, stroke=NONE)
d.shape("rectangle", "Ceiling shade", x=205, y=225, width=590, height=52,
        fill="#2E2A22", opacity=45, stroke=NONE)
d.path("M205,688 L795,688", "Baseboard", fill=NONE, stroke="#332E26",
       strokeWidth=5, opacity=80)
d.shape("rectangle", "Wall shade L", x=205, y=277, width=26, height=411,
        fill="#33302A", opacity=40, stroke=NONE)
d.shape("rectangle", "Wall shade R", x=769, y=277, width=26, height=411,
        fill="#33302A", opacity=40, stroke=NONE)

# --- boardroom door, left: meeting over, heat remaining -------------------------------
d.shape("rectangle", "Door frame", x=226, y=270, width=142, height=430,
        fill="#241C14", stroke=INK, strokeWidth=4)
d.shape("rectangle", "Door", x=240, y=284, width=114, height=416,
        fill=DOOR_GRAD, stroke=INK, strokeWidth=3)
for i, y in enumerate([310, 430]):
    d.shape("rectangle", f"Door panel {i+1}", x=252, y=y, width=90,
            height=100, fill=NONE, stroke="#1E1610", strokeWidth=3,
            opacity=70, radius=4)
d.shape("ellipse", "Knob", x=336, y=498, width=12, height=12,
        fill="#8A7452", stroke=INK, strokeWidth=2.5)
# light still leaking under the door
d.shape("rectangle", "Door light", x=246, y=692, width=102, height=8,
        fill="#E8B86A", opacity=85, stroke=NONE)
d.shape("ellipse", "Door light glow", x=236, y=678, width=122, height=22,
        fill="#E8B86A", opacity=20, stroke=NONE)
# plaque: blank, like the minutes
d.shape("rectangle", "Door plaque", x=258, y=246, width=72, height=18,
        fill="#8A7452", stroke=INK, strokeWidth=2.5, radius=3)

# --- elevator, right -------------------------------------------------------------------
d.shape("rectangle", "Elevator frame", x=632, y=280, width=154, height=420,
        fill="#241C14", stroke=INK, strokeWidth=4)
d.shape("rectangle", "Elevator header", x=640, y=290, width=138, height=26,
        fill="#1E1A14", stroke=NONE)
d.path("M709,306 L701,294 L717,294 Z", "Going down", fill="#E89858",
       stroke=NONE)
d.shape("rectangle", "Elevator door L", x=644, y=322, width=63, height=378,
        fill=ELEV_GRAD, stroke=INK, strokeWidth=3)
d.shape("rectangle", "Elevator door R", x=711, y=322, width=63, height=378,
        fill=ELEV_GRAD, stroke=INK, strokeWidth=3)
d.path("M660,340 L660,690 M758,340 L758,690", "Door sheen", fill=NONE,
       stroke="#A8A294", strokeWidth=4, opacity=35)
# call plate between chart and elevator
d.shape("rectangle", "Call plate", x=612, y=470, width=16, height=42,
        fill="#4A463C", stroke=INK, strokeWidth=2.5, radius=4)
d.path("M620,498 L616,490 L624,490 Z", "Call lit", fill="#E89858",
       stroke=NONE)

# --- the organizational chart on the wall ------------------------------------------------
d.shape("ellipse", "Chart halo", x=380, y=200, width=250, height=210,
        fill="#E89058", opacity=12, stroke=NONE)
d.shape("rectangle", "Chart frame", x=396, y=210, width=208, height=180,
        fill="#2C2418", stroke=INK, strokeWidth=4)
d.shape("rectangle", "Chart paper", x=408, y=222, width=184, height=156,
        fill="#DFD3B8", stroke=NONE)
# title scribble, intentionally unreadable
d.path("M470,236 L530,236 M478,243 L522,243", "Chart title", fill=NONE,
       stroke="#8A7E64", strokeWidth=3, opacity=70)
# connectors
d.path("M500,262 L500,278 M452,278 L548,278 M452,278 L452,290 "
       "M548,278 L548,290 M452,310 L452,322 M430,322 L500,322 "
       "M430,322 L430,334 M500,322 L500,334 M548,310 L548,322 "
       "M570,322 L570,334 M548,322 L570,322",
       "Chart connectors", fill=NONE, stroke="#6E6250", strokeWidth=2.5)
# top box: calm on paper
d.shape("rectangle", "Box top", x=472, y=240, width=56, height=22,
        fill="#C8BBA0", stroke=INK, strokeWidth=2.5, radius=3)
# the two directors: the air between them is boiling
d.shape("ellipse", "Directors heat", x=424, y=274, width=152, height=56,
        fill="#E89058", opacity=30, stroke=NONE)
d.shape("rectangle", "Director L", x=428, y=290, width=48, height=20,
        fill="#D06A44", stroke=INK, strokeWidth=2.5, radius=3)
d.shape("rectangle", "Director R", x=524, y=290, width=48, height=20,
        fill="#D06A44", stroke=INK, strokeWidth=2.5, radius=3)
d.shape("rectangle", "Box L3", x=410, y=334, width=40, height=18,
        fill="#C8BBA0", stroke=INK, strokeWidth=2.5, radius=3)
d.shape("rectangle", "Box M3", x=480, y=334, width=40, height=18,
        fill="#C8BBA0", stroke=INK, strokeWidth=2.5, radius=3)
d.shape("rectangle", "Box R3", x=550, y=334, width=40, height=18,
        fill="#C8BBA0", stroke=INK, strokeWidth=2.5, radius=3)
# heat shimmer rising between the two directors
for i, x in enumerate([488, 502, 516]):
    d.path(f"M{x},288 C{x-6},272 {x+6},262 {x},248 C{x-6},234 {x+5},226 {x},216",
           f"Heat wave {i+1}", fill=NONE, stroke="#E89858", strokeWidth=3.5,
           cap="round", opacity=55-i*14)

# --- a minutes page curling on the floor --------------------------------------------------
d.path(rot_rect_path(520, 680, 46, 20, 12), "Minutes page",
       fill="#E0D6BE", stroke=INK, strokeWidth=2.5)
d.path(rot_rect_path(514, 676, 22, 4, 12), "Minutes line 1", fill=NONE,
       stroke="#8A7E64", strokeWidth=2, opacity=75)
d.path(rot_rect_path(518, 683, 26, 4, 12), "Minutes line 2", fill=NONE,
       stroke="#8A7E64", strokeWidth=2, opacity=75)
d.path("M540,672 C548,668 552,672 550,678", "Page curl", fill=NONE,
       stroke="#B0A488", strokeWidth=2.5, cap="round")

# --- the furred mascot ----------------------------------------------------------------------
d.shape("ellipse", "Mascot shadow", x=296, y=684, width=196, height=20,
        fill="#0E0806", opacity=45, stroke=NONE)
# body + feet
d.shape("ellipse", "Body", x=300, y=500, width=150, height=178,
        fill=FUR_GRAD, stroke=INK, strokeWidth=5)
for x in (312, 394):
    d.shape("ellipse", f"Foot {x}", x=x, y=668, width=56, height=24,
            fill=FUR_DARK, stroke=INK, strokeWidth=4)
# fur tufts along the body's shaded side
for i, (fx, fy, fw) in enumerate([(300,540,15),(297,578,14),(304,616,15),
                                  (449,548,14),(452,590,13)]):
    d.shape("ellipse", f"Body tuft {i+1}", x=fx, y=fy, width=fw, height=fw,
            fill=FUR_DARK, stroke=NONE)
# ears
for side, ex in enumerate([332, 424]):
    s = "L" if side == 0 else "R"
    d.path(f"M{ex-14},{392} C{ex-16},{364} {ex-6},{350} {ex+4},{348} "
           f"C{ex+14},{350} {ex+18},{366} {ex+14},{392} Z",
           f"Ear {s}", fill=FUR_DARK, stroke=INK, strokeWidth=4)
# head
d.shape("ellipse", "Head", x=318, y=372, width=124, height=112,
        fill=FUR_GRAD, stroke=INK, strokeWidth=5)
# cheek fluff
for i, (fx, fy) in enumerate([(316,458),(326,470),(440,458),(432,470)]):
    d.shape("ellipse", f"Cheek tuft {i+1}", x=fx, y=fy, width=13, height=13,
            fill=FUR_DARK, stroke=NONE)
# deadpan face, eyes on the instrument
d.shape("ellipse", "Eye L", x=356, y=418, width=10, height=10,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Eye R", x=398, y=418, width=10, height=10,
        fill=INK, stroke=NONE)
d.path("M352,410 L368,409 M394,409 L410,410", "Lids", fill=NONE,
       stroke=INK, strokeWidth=3, cap="round", opacity=70)
d.path("M370,452 L396,452", "Mouth", fill=NONE, stroke=INK,
       strokeWidth=3.5, cap="round")

# --- the Geiger counter ------------------------------------------------------------------------
# box in the left paw, dial parked in the red
d.shape("ellipse", "Paw on box", x=336, y=560, width=22, height=20,
        fill=FUR_GRAD, stroke=INK, strokeWidth=3.5)
d.shape("rectangle", "Counter box", x=296, y=576, width=76, height=88,
        fill=GEIGER_GRAD, stroke=INK, strokeWidth=4, radius=8)
d.shape("ellipse", "Dial rim", x=308, y=588, width=52, height=40,
        fill="#14120E", stroke=INK, strokeWidth=2.5)
d.path("M313,618 C318,598 350,598 355,618", "Dial arc", fill=NONE,
       stroke="#DFD3B8", strokeWidth=3)
d.path("M348,604 C353,606 356,610 357,616", "Dial red zone", fill=NONE,
       stroke="#D06040", strokeWidth=4, cap="round")
d.path("M334,616 L352,602", "Dial needle", fill=NONE, stroke="#D06040",
       strokeWidth=3.5, cap="round")
d.shape("ellipse", "Needle hub", x=331, y=613, width=7, height=7,
        fill="#D06040", stroke=NONE)
d.path("M306,642 L362,642 M306,652 L350,652", "Box vents", fill=NONE,
       stroke="#2E3122", strokeWidth=3, opacity=80)
# cable sagging up to the wand
d.path("M356,576 C390,560 396,520 420,500 C436,486 444,462 448,436",
       "Cable", fill=NONE, stroke="#241C12", strokeWidth=4, cap="round")
# raised arm + wand aimed between the two directors
d.path("M430,540 C446,505 452,470 454,430", "Arm raised", fill=NONE,
       stroke="#94816A", strokeWidth=17, cap="round")
d.shape("ellipse", "Wand paw", x=444, y=414, width=20, height=18,
        fill="#94816A", stroke=INK, strokeWidth=3.5)
d.path("M460,420 L498,326", "Wand", fill=NONE, stroke="#3A3428",
       strokeWidth=5, cap="round")
d.shape("ellipse", "Wand tip", x=494, y=318, width=10, height=10,
        fill="#E89858", stroke=NONE)
# the counter is ticking
for i, (x1, y1, x2, y2) in enumerate([(508,318,518,312),(512,330,524,330),
                                      (506,306,513,296)]):
    d.path(f"M{x1},{y1} L{x2},{y2}", f"Tick {i+1}", fill=NONE,
           stroke="#E89858", strokeWidth=3, cap="round", opacity=80-i*20)

# --- stray warm motes ---------------------------------------------------------------
for i, (x, y, w) in enumerate([(250,420,6),(560,190,5),(300,240,5),(850,470,6),
                               (220,600,6),(820,620,5),(480,160,5)]):
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#F0C898", opacity=40, stroke=NONE)

# --- captions -------------------------------------------------------------------------
d.text("CORRIDOR HEAT", "Name", x=500, y=930, size=58,
       font="Virelai Sans", color="#F0E2CE", justify="center")
r = d.text("UNMINUTED TENSION, IN DEGREES", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#C8A884", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("264.corridor-heat-V1R00")
