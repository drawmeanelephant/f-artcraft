#!/usr/bin/env python3
"""rc-env.sh — The Grounds Surveyor. Necropolis plate V1R00.
A surveyor's transit on a tripod at the center of the graveyard, plotting
three different cemetery plans on one parchment — the crypt, the busy,
the sterile — with every path derived and every boundary resolved by
realpath before a single stone is laid. Ink, brass, and dusk. 1000x1000.
Gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("RC-Env — Necropolis Plate", 1000, 1000)

INK = "#1E1C28"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#131020"}, {"offset": 1, "color": "#080610"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4A4460"}, {"offset": 0.7, "color": "#2C2838"},
    {"offset": 1, "color": "#14121E"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#282436"}, {"offset": 1, "color": "#121018"}]}}
BRASS = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E8C56A"}, {"offset": 1, "color": "#8A6420"}]}}
BRASS_DK = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#A8853E"}, {"offset": 1, "color": "#5C4218"}]}}
PARCH = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E4D6B4"}, {"offset": 1, "color": "#B8A67E"}]}}
WOOD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5C422C"}, {"offset": 1, "color": "#332216"}]}}
STONE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6A7080"}, {"offset": 1, "color": "#3C4152"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#7E7458", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#DAD4E8", strokeWidth=3, opacity=45)
for i, (x, y, w) in enumerate([(193,233,8),(801,230,7),(157,524,9),(837,544,8),
                               (247,766,7),(753,749,9),(133,393,6),(864,391,7),
                               (391,113,7),(613,110,8),(333,823,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#564E6E", opacity=35, stroke=NONE)

# --- dusk: low warm glow on the horizon + early moon ------------------------------
d.shape("ellipse", "Dusk glow", x=200, y=470, width=600, height=200,
        fill="#D88A50", opacity=10, stroke=NONE)
d.shape("ellipse", "Moon", x=188, y=196, width=58, height=58,
        fill="#E8DCBE", opacity=85, stroke=NONE)
d.shape("ellipse", "Moon shade", x=206, y=186, width=56, height=56,
        fill="#2C2838", opacity=90, stroke=NONE)

# --- floor --------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0C0A12",
       strokeWidth=4, opacity=70)
d.shape("ellipse", "Transit shadow", x=380, y=680, width=260, height=20,
        fill="#040308", opacity=55, stroke=NONE)
d.shape("ellipse", "Table shadow", x=210, y=684, width=240, height=18,
        fill="#040308", opacity=45, stroke=NONE)

# --- headstones waiting to be plotted ---------------------------------------------
d.path("M700,650 L700,610 C700,590 736,590 736,610 L736,650 Z",
       "Headstone 1", fill=STONE, stroke=INK, strokeWidth=4, join="round")
d.path("M752,656 L752,588 M742,606 L762,606 M746,656 L746,630 L758,630 L758,656",
       "Headstone 2", fill=STONE, stroke=INK, strokeWidth=4, join="round")
d.path("M780,650 L780,600 L806,600 L806,650 Z", "Headstone 3", fill=STONE,
       stroke=INK, strokeWidth=4, join="round")
d.shape("ellipse", "Stone shadows", x=690, y=650, width=130, height=12,
        fill="#040308", opacity=45, stroke=NONE)

# --- the drafting table with the parchment of three plans ----------------------------
# table legs first
d.path("M258,600 L246,690", "Table leg L", fill=NONE, stroke="#3E2A1C",
       strokeWidth=9, cap="round")
d.path("M414,584 L424,690", "Table leg R", fill=NONE, stroke="#3E2A1C",
       strokeWidth=9, cap="round")
# table top (tilted toward the viewer)
d.path("M226,556 L424,536 L446,592 L246,614 Z", "Table top", fill=WOOD,
       stroke=INK, strokeWidth=5, join="round")
# the parchment, one sheet, three plans
d.path("M240,556 L408,540 L428,582 L258,600 Z", "Plan parchment",
       fill=PARCH, stroke=INK, strokeWidth=3, join="round")
# parchment curl at the right edge + a holding pebble
d.path("M408,540 C420,544 426,556 428,582 L416,584 C414,562 410,548 404,542 Z",
       "Plan curl", fill="#C4AE7E", stroke=INK, strokeWidth=2)
d.shape("ellipse", "Plan pebble", x=248, y=552, width=14, height=10,
        fill=STONE, stroke=INK, strokeWidth=2)
# zone dividers on the parchment
d.path("M298,548 L312,594", "Zone line 1", fill=NONE, stroke="#8A7450",
       strokeWidth=2, opacity=80)
d.path("M352,544 L366,590", "Zone line 2", fill=NONE, stroke="#8A7450",
       strokeWidth=2, opacity=80)
# zone 1 — the crypt: two vault doors
for i, (vx, vy) in enumerate([(258, 566), (276, 564)]):
    d.path(f"M{vx},{vy+14} L{vx},{vy+4} C{vx},{vy} {vx+10},{vy} {vx+10},{vy+4} "
           f"L{vx+10},{vy+14} Z", f"Crypt vault {i+1}", fill=NONE,
           stroke="#4A3A28", strokeWidth=2)
# zone 2 — the busy: plotted paths + plot crosses
d.path("M316,590 C320,578 330,580 334,570 C338,562 344,566 346,556",
       "Busy path", fill=NONE, stroke="#4A3A28", strokeWidth=2)
for i, (px, py) in enumerate([(320, 560), (334, 584), (344, 548)]):
    d.path(f"M{px},{py} L{px+7},{py+7} M{px+7},{py} L{px},{py+7}",
           f"Busy plot {i+1}", fill=NONE, stroke="#5A4A34", strokeWidth=2)
# zone 3 — the sterile: a bare grid
for i, (gx, gy) in enumerate([(372, 552), (392, 550), (376, 574), (396, 572)]):
    d.shape("rectangle", f"Sterile plot {i+1}", x=gx, y=gy, width=10,
            height=9, fill=NONE, stroke="#5A4A34", strokeWidth=2)

# --- the surveyor's transit on its tripod ----------------------------------------------
# tripod legs
d.path("M500,392 L392,690", "Tripod leg L", fill=NONE, stroke="#3E2A1C",
       strokeWidth=11, cap="round")
d.path("M500,392 L500,694", "Tripod leg C", fill=NONE, stroke="#33241A",
       strokeWidth=11, cap="round")
d.path("M500,392 L612,690", "Tripod leg R", fill=NONE, stroke="#3E2A1C",
       strokeWidth=11, cap="round")
# leg braces
d.path("M446,540 L554,540", "Leg brace", fill=NONE, stroke="#5C422C",
       strokeWidth=5, opacity=80, cap="round")
# head + leveling screws
d.shape("ellipse", "Tripod head", x=468, y=372, width=64, height=26,
        fill=BRASS_DK, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Screw L", x=452, y=384, width=12, height=12,
        fill=BRASS, stroke=INK, strokeWidth=2)
d.shape("ellipse", "Screw R", x=536, y=384, width=12, height=12,
        fill=BRASS, stroke=INK, strokeWidth=2)
# standards (yoke arms) + the telescope barrel across them
d.shape("rectangle", "Standard L", x=466, y=316, width=14, height=60,
        fill=BRASS_DK, stroke=INK, strokeWidth=4, radius=4)
d.shape("rectangle", "Standard R", x=520, y=316, width=14, height=60,
        fill=BRASS_DK, stroke=INK, strokeWidth=4, radius=4)
d.shape("rectangle", "Scope barrel", x=404, y=296, width=192, height=34,
        fill=BRASS, stroke=INK, strokeWidth=5, radius=14)
# collar rings + objective glass + eyepiece
d.shape("rectangle", "Collar L", x=428, y=292, width=12, height=42,
        fill=BRASS_DK, stroke=INK, strokeWidth=3, radius=3)
d.shape("rectangle", "Collar R", x=560, y=292, width=12, height=42,
        fill=BRASS_DK, stroke=INK, strokeWidth=3, radius=3)
d.shape("ellipse", "Objective", x=398, y=301, width=16, height=24,
        fill="#2E3A46", stroke=INK, strokeWidth=3)
d.path("M596,306 L612,306 L612,320 L596,320 Z", "Eyepiece", fill=BRASS_DK,
       stroke=INK, strokeWidth=3, join="round")
# glint along the barrel + compass rose on top
d.path("M414,302 L560,302", "Barrel glint", fill=NONE, stroke="#F4E2A8",
       strokeWidth=4, opacity=70, cap="round")
d.shape("ellipse", "Compass", x=486, y=276, width=28, height=22,
        fill=BRASS, stroke=INK, strokeWidth=3)
d.path("M500,278 L500,296 M492,287 L508,287", "Compass rose", fill=NONE,
       stroke="#4A3010", strokeWidth=2)

# --- surveyed boundary: stakes + a taut resolved line -----------------------------------
d.path("M654,690 L660,646", "Stake 1", fill=NONE, stroke="#5C422C",
       strokeWidth=6, cap="round")
d.path("M800,690 L806,646", "Stake 2", fill=NONE, stroke="#5C422C",
       strokeWidth=6, cap="round")
d.path("M660,650 L806,650", "Boundary line", fill=NONE, stroke="#E8C56A",
       strokeWidth=2, opacity=85)
d.shape("ellipse", "Stake knob 1", x=656, y=642, width=8, height=8,
        fill=BRASS, stroke=INK, strokeWidth=2)
d.shape("ellipse", "Stake knob 2", x=802, y=642, width=8, height=8,
        fill=BRASS, stroke=INK, strokeWidth=2)

# --- captions ------------------------------------------------------------------
d.text("RC-ENV", "Name", x=500, y=930, size=58, font="Virelai Sans",
       color="#E2DEEA", justify="center")
r = d.text("THE GROUNDS, SURVEYED", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#A29CB8", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("rk-env-V1R00")
