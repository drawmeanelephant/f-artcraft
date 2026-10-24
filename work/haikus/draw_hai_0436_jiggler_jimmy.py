#!/usr/bin/env python3
"""HAI-0436 Jiggler Jimmy — haiku plate V1R00. Metric homeostasis: a cursor
vibrating in place on a dashboard whose curve stays perfectly smooth, a green
presence dot pulsing beside an empty avatar ring, an empty chair underneath.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("HAI-0436 Jiggler Jimmy — Haiku Plate", 1000, 1000)

INK = "#2E1F1A"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1A1410"}, {"offset": 1, "color": "#0B0806"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#2C4650"}, {"offset": 0.7, "color": "#17282F"},
    {"offset": 1, "color": "#0D181E"}]}}
SCREEN_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#12242C"}, {"offset": 1, "color": "#0A151B"}]}}
CHAIR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3A4A54"}, {"offset": 1, "color": "#1B262C"}]}}
GREEN_DOT = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#C9FFD9"}, {"offset": 0.55, "color": "#5CE88E"},
    {"offset": 1, "color": "#1F9B52"}]}}
CURSOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F2FAFF"}, {"offset": 1, "color": "#A9C4D4"}]}}
PALE = "#DCEFEA"
SOFT = "#8FB3AE"
GREEN = "#5CE88E"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#5E8894", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#DCEFEA", strokeWidth=3, opacity=40)
# cool screen-glow pool behind the dashboard
d.shape("ellipse", "Glow pool", x=250, y=150, width=500, height=420,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#6FD8C8", "opacity": 0.16},
            {"offset": 1, "color": "#6FD8C8", "opacity": 0}]}},
        stroke=NONE)
# the curve eating the world: one faint continent-scale echo behind everything
d.path("M140,635 C300,540 560,560 700,380 C770,290 800,255 835,240",
       "World echo", fill=NONE, stroke="#6FD8C8", strokeWidth=26,
       opacity=8, cap="round")

# --- dashboard: the perfectly smooth curve ------------------------------------
d.shape("rectangle", "Screen bezel", x=262, y=162, width=476, height=272,
        radius=16, fill={"gradient": {"kind": "linear", "stops": [
            {"offset": 0, "color": "#3D545E"}, {"offset": 1, "color": "#1C2A31"}]}},
        stroke=INK, strokeWidth=4)
d.shape("rectangle", "Screen", x=278, y=178, width=444, height=240,
        radius=8, fill=SCREEN_GRAD, stroke=NONE)
# faint grid
for i, gx in enumerate([340, 420, 500, 580, 660]):
    d.path(f"M{gx},190 L{gx},410", f"Grid v{i+1}", fill=NONE,
           stroke="#3A5A60", strokeWidth=1, opacity=35)
for i, gy in enumerate([245, 300, 355]):
    d.path(f"M290,{gy} L710,{gy}", f"Grid h{i+1}", fill=NONE,
           stroke="#3A5A60", strokeWidth=1, opacity=35)
# axes
d.path("M296,398 L296,196 M296,398 L708,398", "Axes", fill=NONE,
       stroke="#5E8894", strokeWidth=2, opacity=70)
# the smooth curve: glow, halo, spine — suspiciously serene
CURVE = "M302,382 C380,378 430,352 486,318 C552,278 610,236 700,206"
d.path(CURVE, "Curve glow", fill=NONE, stroke=GREEN, strokeWidth=20,
       opacity=12, cap="round")
d.path(CURVE, "Curve halo", fill=NONE, stroke="#8FF0B4", strokeWidth=8,
       opacity=30, cap="round")
d.path(CURVE, "Curve spine", fill=NONE, stroke="#D6FFE4", strokeWidth=3.5,
       cap="round")
# data points along the curve — each one a worker, all silent
for i, (cx, cy) in enumerate([(360, 368), (444, 342), (528, 292),
                              (610, 244), (686, 212)]):
    d.shape("ellipse", f"Data point {i+1}", x=cx - 4, y=cy - 4, width=8,
            height=8, fill="#D6FFE4", stroke=INK, strokeWidth=1.5,
            opacity=90)

# --- jiggler cursor: vibrating in place on the screen --------------------------
# ghosts first (subpixel jitter), then the live cursor
CURSOR = "M596,296 L596,366 L613,349 L624,376 L634,372 L623,345 L645,345 Z"
d.path("M601,293 L601,363 L618,346 L629,373 L639,369 L628,342 L650,342 Z",
       "Cursor ghost +", fill="#BFD8E4", opacity=16, stroke=NONE)
d.path("M591,299 L591,369 L608,352 L619,379 L629,375 L618,348 L640,348 Z",
       "Cursor ghost -", fill="#BFD8E4", opacity=12, stroke=NONE)
d.path(CURSOR, "Cursor", fill=CURSOR_GRAD, stroke=INK, strokeWidth=3,
       join="round")
# vibration ticks
for i, (x1, y1, x2, y2) in enumerate([(568, 306, 552, 298), (566, 340, 548, 342),
                                      (652, 300, 668, 290), (658, 332, 676, 334)]):
    d.path(f"M{x1},{y1} L{x2},{y2}", f"Jitter tick {i+1}", fill=NONE,
           stroke="#BFD8E4", strokeWidth=3, opacity=60, cap="round")

# --- presence chip: green dot pulses, avatar ring empty -------------------------
d.shape("rectangle", "Presence chip", x=330, y=452, width=340, height=56,
        radius=28, fill={"gradient": {"kind": "linear", "stops": [
            {"offset": 0, "color": "#1E343C"}, {"offset": 1, "color": "#101E24"}]}},
        stroke="#4A707A", strokeWidth=3)
# pulsing green dot
d.shape("ellipse", "Dot glow", x=342, y=462, width=72, height=36,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#5CE88E", "opacity": 0.45},
            {"offset": 1, "color": "#5CE88E", "opacity": 0}]}},
        stroke=NONE)
d.shape("ellipse", "Pulse ring 1", x=356, y=466, width=26, height=26,
        fill=NONE, stroke=GREEN, strokeWidth=2, opacity=45)
d.shape("ellipse", "Pulse ring 2", x=349, y=459, width=40, height=40,
        fill=NONE, stroke=GREEN, strokeWidth=1.5, opacity=22)
d.shape("ellipse", "Green dot", x=362, y=472, width=14, height=14,
        fill=GREEN_DOT, stroke=NONE)
# empty avatar: dashed ring where a person should be
d.shape("ellipse", "Avatar ring", x=596, y=462, width=36, height=36,
        fill=NONE, stroke="#8FB3AE", strokeWidth=2.5, opacity=70,
        dash=[5, 4])
d.path("M604,480 Q614,470 624,480 M607,490 Q614,484 621,490", "Ghost person",
       fill=NONE, stroke="#8FB3AE", strokeWidth=2, opacity=40, cap="round")
# heartbeat trace runs longer to bridge dot and empty avatar
d.path("M414,480 L440,480 L448,470 L458,492 L466,480 L560,480",
       "Heartbeat run", fill=NONE, stroke=GREEN, strokeWidth=2,
       opacity=45, cap="round", join="round")

# --- empty chair, pushed back, nobody in it -------------------------------------
# floor band: crescent closed on the disc's own arc (rim rule)
d.path("M206,756 Q500,824 794,756 A420,420 0 0 1 206,756 Z",
       "Floor band", fill={"gradient": {"kind": "linear", "stops": [
           {"offset": 0, "color": "#0A1216", "opacity": 0},
           {"offset": 1, "color": "#060C0F", "opacity": 0.55}]}},
       stroke=NONE)
# chair shadow
d.shape("ellipse", "Chair shadow", x=392, y=778, width=216, height=26,
        fill="#060C0F", opacity=50, stroke=NONE)
# five-star base
for i, (x1, y1, x2, y2) in enumerate([(500, 742, 440, 776), (500, 742, 560, 776),
                                      (500, 742, 500, 786), (500, 742, 452, 762),
                                      (500, 742, 548, 762)]):
    d.path(f"M{x1},{y1} L{x2},{y2}", f"Base spoke {i+1}", fill=NONE,
           stroke="#26343D", strokeWidth=10, cap="round")
for i, (cx, cy) in enumerate([(440, 778), (560, 778), (500, 788)]):
    d.shape("ellipse", f"Caster {i+1}", x=cx - 8, y=cy - 6, width=16,
            height=12, fill="#141D22", stroke=INK, strokeWidth=2.5)
# stem + seat + backrest, seen from behind, slightly rolled away
d.shape("rectangle", "Chair stem", x=491, y=694, width=18, height=54,
        radius=6, fill=CHAIR_GRAD, stroke=INK, strokeWidth=3.5)
d.shape("rectangle", "Seat", x=438, y=664, width=124, height=34, radius=14,
        fill=CHAIR_GRAD, stroke=INK, strokeWidth=4)
d.shape("rectangle", "Backrest", x=446, y=546, width=108, height=126,
        radius=20, fill=CHAIR_GRAD, stroke=INK, strokeWidth=4.5)
d.shape("rectangle", "Headrest", x=466, y=516, width=68, height=34,
        radius=14, fill=CHAIR_GRAD, stroke=INK, strokeWidth=4)
# sheen on the backrest — the light is on, the sitter is gone
d.path("M462,556 C456,592 456,632 462,662", "Backrest sheen", fill=NONE,
       stroke="#BFD8E4", strokeWidth=8, opacity=14, cap="round")

# --- name + key haiku line --------------------------------------------------------
r = d.text("green dot pulses, human absent, curve eats the world.",
           "Key line", x=500, y=898, size=21, font="Virelai Sans",
           color=SOFT, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "key tracking", ids=[r["id"]], tracking=70)
d.text("JIGGLER JIMMY", "Name", x=500, y=948, size=56,
       font="Virelai Sans", color=PALE, justify="center")

d.finish("hai-0436-jiggler-jimmy-V1R00")
