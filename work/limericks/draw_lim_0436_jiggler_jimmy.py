#!/usr/bin/env python3
"""LIM-0436 Jiggler Jimmy — limerick plate V1R00. Metric homeostasis:
a dashboard whose presence curve stays perfectly smooth, a green dot
glowing out of pure spite, a mouse cursor vibrating in place, and an
empty office chair where the human used to be. Jimmy the dongle keeps
the mouse jiggling. Teal dark, green phosphor glow.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("LIM-0436 Jiggler Jimmy — Limerick Plate", 1000, 1000)

INK = "#241E24"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#0D1A1D"}, {"offset": 1, "color": "#050D0E"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#3F6E74"}, {"offset": 0.7, "color": "#29494F"},
    {"offset": 1, "color": "#142C32"}]}}
DESK = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2E4A50"}, {"offset": 1, "color": "#15272B"}]}}
SCREEN = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#0F252B"}, {"offset": 1, "color": "#081418"}]}}
BODY = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#7FD0CE"}, {"offset": 0.7, "color": "#54A8A9"},
    {"offset": 1, "color": "#357880"}]}}
METAL = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#D8DEE2"}, {"offset": 1, "color": "#93A0A8"}]}}
MOUSE = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#5E7E88"}, {"offset": 0.7, "color": "#415E68"},
    {"offset": 1, "color": "#2A4048"}]}}
GREEN = "#4ADE80"
GREEN_SOFT = "#8FE8B0"
CREAM = "#D8EEE8"
TAN = "#8FBEB8"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#5E9A9C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C8ECEA", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(190, 240, 8), (800, 230, 7), (160, 520, 9),
                               (830, 540, 8), (240, 760, 7), (760, 740, 9),
                               (130, 390, 6), (865, 390, 7), (390, 110, 7),
                               (610, 110, 8), (330, 820, 6), (665, 815, 7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#3A626A", opacity=45, stroke=NONE)

# --- the empty chair, where the human used to be ---------------------------------
# silhouette, slightly transparent — presence as absence
CH = "#16282C"
d.path("M262,300 C252,300 246,310 246,330 L246,430 C246,450 252,458 "
       "264,458 L316,458 C328,458 334,450 334,430 L334,330 C334,310 "
       "328,300 318,300 Z",
       "Chair back", fill=CH, stroke="#2E4A50", strokeWidth=4,
       opacity=80, join="round")
d.path("M258,344 L322,344 M258,394 L322,394", "Chair seams", fill=NONE,
       stroke="#2E4A50", strokeWidth=3, opacity=60)
# seat cushion + armrest stubs
d.path("M238,470 L342,470 C350,470 354,478 354,486 L354,494 C354,502 "
       "348,506 340,506 L240,506 C232,506 226,502 226,494 L226,486 "
       "C226,478 232,470 238,470 Z",
       "Chair seat", fill=CH, stroke="#2E4A50", strokeWidth=4,
       opacity=80, join="round")
d.path("M226,452 L226,474 M354,452 L354,474", "Armrests", fill=NONE,
       stroke="#2E4A50", strokeWidth=8, opacity=75, cap="round")
# gas post + five-star base
d.path("M290,506 L290,566", "Chair post", fill=NONE, stroke=CH,
       strokeWidth=13, opacity=85)
for i, (lx, ly) in enumerate([(238, 590), (342, 590), (290, 600),
                              (254, 566), (326, 566)]):
    d.path(f"M290,566 L{lx},{ly}", f"Chair leg {i+1}", fill=NONE,
           stroke=CH, strokeWidth=9, opacity=85, cap="round")
    d.shape("ellipse", f"Caster {i+1}", x=lx - 7, y=ly - 2, width=14,
            height=12, fill=CH, opacity=85, stroke=NONE)
# a pale halo of absence around the headrest
d.shape("ellipse", "Chair absence", x=238, y=286, width=104, height=60,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#9FD8D4", "opacity": 0.10},
            {"offset": 1, "color": "#9FD8D4", "opacity": 0}]}},
        stroke=NONE)

# --- the dashboard: the curve that ate the human ---------------------------------
# screen glow spilling onto the plate
d.shape("ellipse", "Screen glow", x=400, y=300, width=460, height=340,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#4ADE80", "opacity": 0.09},
            {"offset": 1, "color": "#4ADE80", "opacity": 0}]}},
        stroke=NONE)
# bezel + screen
d.shape("rectangle", "Monitor", x=404, y=268, width=392, height=280,
        fill="#122126", stroke=INK, strokeWidth=7, radius=14)
d.shape("rectangle", "Screen", x=420, y=284, width=360, height=248,
        fill=SCREEN, stroke=NONE, radius=8)
# stand
d.path("M600,548 L600,662 M552,662 L648,662", "Stand", fill=NONE,
       stroke="#1A2E33", strokeWidth=11, cap="round", join="round")
# panel header
d.text("PRESENCE", "Panel title", x=448, y=312, size=15,
       font="Virelai Sans", color="#5E8E88", justify="left")
# grid lines, faint and even
for i, gy in enumerate([346, 390, 434, 478]):
    d.path(f"M440,{gy} L764,{gy}", f"Grid {i+1}", fill=NONE,
           stroke="#1E3A40", strokeWidth=1.5, opacity=70)
# the curve itself: suspiciously, perfectly smooth
d.path("M448,470 C500,466 540,452 580,430 C620,408 660,402 700,404 "
       "C730,405 752,400 764,394",
       "Presence curve", fill=NONE, stroke=GREEN, strokeWidth=5,
       cap="round")
d.path("M448,470 C500,466 540,452 580,430 C620,408 660,402 700,404 "
       "C730,405 752,400 764,394",
       "Curve glow", fill=NONE, stroke=GREEN_SOFT, strokeWidth=13,
       opacity=18, cap="round")
# uptime ticks along the axis — not one gap in the log
for i, tx in enumerate(range(448, 765, 28)):
    d.path(f"M{tx},500 L{tx},506", f"Tick {i+1}", fill=NONE,
           stroke="#1E3A40", strokeWidth=2, opacity=80)
# the green presence dot, glowing out of spite
d.shape("ellipse", "Dot halo", x=712, y=288, width=58, height=58,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#4ADE80", "opacity": 0.45},
            {"offset": 1, "color": "#4ADE80", "opacity": 0}]}},
        stroke=NONE)
d.shape("ellipse", "Green dot", x=724, y=300, width=34, height=34,
        fill="#58E896", stroke="#1E5A3E", strokeWidth=4)
d.shape("ellipse", "Dot gleam", x=731, y=306, width=11, height=8,
        fill="#FFFFFF", opacity=70, stroke=NONE)
d.text("ONLINE", "Dot label", x=768, y=322, size=13, font="Virelai Sans",
       color=GREEN_SOFT, justify="left")
# session timer — digits in Source Sans 3 (Virelai Sans has none)
t = d.text("99:59:58", "Session timer", x=600, y=522, size=17,
           font="Source Sans 3", color="#5E8E88", justify="center")
# the vibrating cursor on the curve: ghost offsets + the arrow itself
for i, (dx, dy, op) in enumerate([(-7, 5, 22), (7, -5, 22)]):
    d.path(f"M{588+dx},{392+dy} L{588+dx},{428+dy} L{598+dx},{418+dy} "
           f"L{606+dx},{432+dy} L{612+dx},{428+dy} L{604+dx},{414+dy} "
           f"L{616+dx},{414+dy} Z",
           f"Cursor ghost {i+1}", fill="#CFE8E4", opacity=op, stroke=NONE)
d.path("M588,392 L588,428 L598,418 L606,432 L612,428 L604,414 "
       "L616,414 Z",
       "Cursor", fill="#E8F4F0", stroke=INK, strokeWidth=2.5,
       join="round")
# jiggle marks bracketing the cursor
for i, sx in enumerate([-1, 1]):
    d.path(f"M{588+34*sx},{386} C{588+40*sx},{396} {588+40*sx},{408} "
           f"{588+34*sx},{418}",
           f"Cursor jiggle {i+1}", fill=NONE, stroke="#9FD8D4",
           strokeWidth=3.5, opacity=60, cap="round")

# --- desk -----------------------------------------------------------------------
d.shape("ellipse", "Desk", x=170, y=636, width=660, height=130,
        fill=DESK, stroke=NONE, opacity=92)
d.shape("ellipse", "Mouse shadow", x=560, y=672, width=170, height=26,
        fill="#081114", opacity=50, stroke=NONE)
d.shape("ellipse", "Jimmy shadow", x=400, y=682, width=140, height=24,
        fill="#081114", opacity=50, stroke=NONE)
# screen spill on the desk surface
d.path("M440,648 L780,648 L740,700 L480,700 Z", "Desk spill",
       fill=GREEN, opacity=6, stroke=NONE)

# --- the physical mouse, mid-jiggle ------------------------------------------------
# cable curling off toward the rim
d.path("M724,624 C790,610 830,636 824,676 C820,700 802,714 784,716",
       "Mouse cable", fill=NONE, stroke="#243840", strokeWidth=6,
       cap="round")
# ghost shells, vibrating in place
for i, (dx, dy, op) in enumerate([(-9, 3, 20), (9, -3, 20)]):
    d.shape("ellipse", f"Mouse ghost {i+1}", x=596 + dx, y=612 + dy,
            width=128, height=84, fill="#415E68", opacity=op,
            stroke=NONE)
# body
d.shape("ellipse", "Mouse", x=596, y=612, width=128, height=84,
        fill=MOUSE, stroke=INK, strokeWidth=6)
d.path("M664,612 C660,626 660,640 664,654", "Button split", fill=NONE,
       stroke=INK, strokeWidth=4, opacity=70)
d.shape("ellipse", "Wheel", x=654, y=630, width=14, height=22,
        fill="#1E3038", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Mouse highlight", x=614, y=622, width=44, height=16,
        fill="#FFFFFF", opacity=14, stroke=NONE)
# jiggle marks above
for i, (x, y) in enumerate([(622, 570), (656, 556), (690, 570)]):
    d.path(f"M{x},{y} C{x-9},{y+11} {x-9},{y+22} {x},{y+33}",
           f"Jiggle mark {i+1}", fill=NONE, stroke="#9FD8D4",
           strokeWidth=4.5, opacity=55, cap="round")

# --- Jimmy: the dongle on duty -------------------------------------------------------
# legs + feet
d.path("M456,622 L452,676", "Leg L", fill=NONE, stroke="#357880",
       strokeWidth=12, cap="round")
d.path("M498,622 L504,676", "Leg R", fill=NONE, stroke="#2E6A72",
       strokeWidth=12, cap="round")
d.shape("ellipse", "Shoe L", x=434, y=668, width=32, height=15, fill=INK,
        stroke=NONE)
d.shape("ellipse", "Shoe R", x=494, y=668, width=32, height=15, fill=INK,
        stroke=NONE)
# body: rounded-rect dongle
d.shape("rectangle", "Jimmy body", x=424, y=452, width=112, height=174,
        fill=BODY, stroke=INK, strokeWidth=6, radius=18)
d.shape("ellipse", "Body highlight", x=435, y=464, width=54, height=24,
        fill="#FFFFFF", opacity=20, stroke=NONE)
# USB-A plug hat
d.shape("rectangle", "Plug", x=452, y=416, width=56, height=40,
        fill=METAL, stroke=INK, strokeWidth=5, radius=6)
d.shape("rectangle", "Contact 1", x=461, y=425, width=13, height=9,
        fill="#3E4A52", stroke=NONE)
d.shape("rectangle", "Contact 2", x=486, y=425, width=13, height=9,
        fill="#3E4A52", stroke=NONE)
d.path("M458,452 L502,452", "Plug seam", fill=NONE, stroke="#5A666E",
       strokeWidth=4, opacity=60)
# face: bright eyes, professional smirk
d.shape("ellipse", "Eye L", x=452, y=512, width=16, height=20, fill=INK,
        stroke=NONE)
d.shape("ellipse", "Eye R", x=496, y=512, width=16, height=20, fill=INK,
        stroke=NONE)
d.shape("ellipse", "Glint L", x=456, y=516, width=5, height=5,
        fill="#FFFFFF", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=500, y=516, width=5, height=5,
        fill="#FFFFFF", opacity=90, stroke=NONE)
d.shape("ellipse", "Cheek L", x=435, y=538, width=24, height=14,
        fill="#E89A8C", opacity=50, stroke=NONE)
d.shape("ellipse", "Cheek R", x=503, y=538, width=24, height=14,
        fill="#E89A8C", opacity=50, stroke=NONE)
d.path("M466,560 C479,569 496,569 509,558", "Smirk", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
# etched USB glyph low on the body
d.path("M480,608 L480,582 M480,594 L473,589 M480,588 L487,582",
       "USB glyph", fill=NONE, stroke="#24555C", strokeWidth=4,
       cap="round", opacity=70)
d.shape("ellipse", "USB dot", x=476, y=576, width=8, height=8,
        fill="#24555C", opacity=70, stroke=NONE)
# right arm reaching to keep the mouse honest
d.path("M534,540 C558,556 578,580 594,606", "Arm press", fill=NONE,
       stroke="#54A8A9", strokeWidth=13, cap="round")
d.shape("ellipse", "Finger press", x=586, y=600, width=20, height=17,
        fill="#7FD0CE", stroke=INK, strokeWidth=3)
# left arm on his hip — easy shift tonight
d.path("M426,534 C410,548 406,568 414,584", "Arm hip", fill=NONE,
       stroke="#54A8A9", strokeWidth=13, cap="round")
d.shape("ellipse", "Hand hip", x=406, y=578, width=20, height=17,
        fill="#7FD0CE", stroke=INK, strokeWidth=3)

# --- captions -------------------------------------------------------------------------
k = d.text("THE GREEN DOT PERSISTS OUT OF SPITE.", "Key line", x=500,
           y=862, size=23, font="Virelai Sans", color="#9FD8CC",
           justify="center")
if k and k.get("id"):
    d.cmd("text.setStyle", "key tracking", ids=[k["id"]], tracking=150)
d.text("JIGGLER JIMMY", "Name", x=500, y=930, size=58,
       font="Virelai Sans", color=CREAM, justify="center")
r = d.text("CURVE EATS THE HUMAN", "Role", x=500, y=968, size=20,
           font="Virelai Sans", color=TAN, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=190)

d.finish("lim-0436-jiggler-jimmy-V1R00")
