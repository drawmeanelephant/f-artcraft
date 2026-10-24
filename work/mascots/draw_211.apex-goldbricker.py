#!/usr/bin/env python3
"""Apex Goldbricker — mascot portrait V1R00.
Mascot leaning back with shoes on the desk, immaculate utilization
dashboard on the monitor, a wall calendar of fully blocked time.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Apex Goldbricker — Mascot Portrait", 1000, 1000)

INK = "#33261F"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#16120C"}, {"offset": 1, "color": "#080604"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#6B5432"}, {"offset": 0.7, "color": "#42331D"},
    {"offset": 1, "color": "#241A0E"}]}}
FLOOR = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3A2E1C"}, {"offset": 1, "color": "#1E160C"}]}}
DESK_TOP = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7A5A34"}, {"offset": 1, "color": "#4E381F"}]}}
DESK_FRONT = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5E4527"}, {"offset": 1, "color": "#3A2A16"}]}}
SCREEN = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#16302A"}, {"offset": 1, "color": "#0A1812"}]}}
BODY = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F0DDBE"}, {"offset": 0.7, "color": "#D4B48C"},
    {"offset": 1, "color": "#A87F5A"}]}}
SHIRT = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E8E0D0"}, {"offset": 1, "color": "#B8AC94"}]}}
PAPER = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F0E8D6"}, {"offset": 1, "color": "#CFC4A8"}]}}
CHAIR = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4A3B2C"}, {"offset": 1, "color": "#2A211A"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#8A6E42", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8D9B0", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(190,235,8),(800,230,7),(160,520,9),(830,540,8),
                               (240,760,7),(760,740,9),(130,390,6),(865,390,7),
                               (390,110,7),(610,110,8),(330,820,6),(665,815,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#54401F", opacity=45, stroke=NONE)

# --- floor: closed on the disc's own arc ----------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR, stroke=NONE)

# --- wall calendar: every cell blocked -------------------------------------------
d.shape("rectangle", "Calendar frame", x=648, y=190, width=200, height=190,
        fill="#3A2E22", stroke=INK, strokeWidth=5, radius=6)
d.shape("rectangle", "Calendar paper", x=660, y=202, width=176, height=166,
        fill=PAPER, stroke=NONE)
d.shape("rectangle", "Calendar header", x=660, y=202, width=176, height=34,
        fill="#8A4B2E", stroke=NONE)
d.text("Q3", "Calendar title", x=748, y=226, size=16,
       font="Virelai Sans", color="#F0E8D6", justify="center")
for r in range(3):
    for c in range(4):
        x = 672 + c*40
        y = 248 + r*36
        d.shape("rectangle", f"Blocked {r}-{c}", x=x, y=y, width=34, height=28,
                fill="#C9A03E", stroke="#8A6E42", strokeWidth=2, radius=3)
        d.path(f"M{x+6},{y+6} L{x+28},{y+22} M{x+28},{y+6} L{x+6},{y+22}",
               f"Blocked X {r}-{c}", fill=NONE, stroke="#7A3A28",
               strokeWidth=3, cap="round", opacity=80)

# --- swivel chair behind the desk -----------------------------------------------
d.shape("rectangle", "Chair back", x=570, y=470, width=150, height=230,
        fill=CHAIR, stroke=INK, strokeWidth=5, radius=40)
d.shape("ellipse", "Chair top", x=600, y=458, width=66, height=30,
        fill=CHAIR, stroke=INK, strokeWidth=5)

# --- the mascot, leaning back ----------------------------------------------------
# body: shirt blob, lower half hidden by desk
d.path("M505,470 C575,470 612,520 608,580 C604,640 570,672 505,672 "
       "C440,672 406,640 402,580 C398,520 435,470 505,470 Z",
       "Apex body", fill=BODY, stroke=INK, strokeWidth=6)
# open collar shirt front
d.path("M452,552 C462,612 478,648 505,668 C532,648 548,612 558,552 "
       "C540,566 470,566 452,552 Z",
       "Shirt front", fill=SHIRT, stroke=INK, strokeWidth=4, join="round")
# gold tie, perfectly straight — peak effort signaling
d.path("M505,566 L489,596 L505,644 L521,596 Z",
       "Tie", fill={"gradient": {"kind": "linear", "stops": [
           {"offset": 0, "color": "#D9AE4E"}, {"offset": 1, "color": "#9A7428"}]}},
       stroke=INK, strokeWidth=3, join="round")
# STRONG CONTRIBUTOR badge on the right chest
d.shape("ellipse", "Badge", x=546, y=588, width=32, height=32,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#E8C568"}, {"offset": 1, "color": "#A87F28"}]}},
        stroke=INK, strokeWidth=3)
d.path("M554,606 L561,599 L570,608", "Badge check", fill=NONE,
       stroke="#4E381F", strokeWidth=4, cap="round", join="round")
# arms folded behind the head — hands resting at the sides
d.path("M455,565 C428,548 420,512 438,488", "Arm L", fill=NONE,
       stroke="#D4B48C", strokeWidth=13, cap="round")
d.path("M585,565 C614,548 620,512 600,488", "Arm R", fill=NONE,
       stroke="#C9A87E", strokeWidth=13, cap="round")
d.shape("ellipse", "Hand L", x=420, y=472, width=22, height=17,
        fill="#F0DDBE", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Hand R", x=598, y=472, width=22, height=17,
        fill="#F0DDBE", stroke=INK, strokeWidth=3)
# serene closed eyes, smug smirk
d.path("M462,508 Q477,518 492,508", "Eye L", fill=NONE, stroke=INK,
       strokeWidth=6, cap="round")
d.path("M518,508 Q533,518 548,508", "Eye R", fill=NONE, stroke=INK,
       strokeWidth=6, cap="round")
d.shape("ellipse", "Cheek L", x=448, y=524, width=24, height=14,
        fill="#C98A74", opacity=45, stroke=NONE)
d.shape("ellipse", "Cheek R", x=538, y=524, width=24, height=14,
        fill="#C98A74", opacity=45, stroke=NONE)
d.path("M486,540 C502,550 522,548 534,536", "Smirk", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")

# --- desk: slab, then front panel -------------------------------------------------
d.shape("rectangle", "Desktop", x=228, y=636, width=544, height=34,
        fill=DESK_TOP, stroke=INK, strokeWidth=5, radius=8)
d.shape("rectangle", "Desk front", x=250, y=670, width=500, height=120,
        fill=DESK_FRONT, stroke=INK, strokeWidth=5, radius=6)
# brass nameplate
d.shape("rectangle", "Nameplate", x=430, y=712, width=150, height=34,
        fill={"gradient": {"kind": "linear", "stops": [
            {"offset": 0, "color": "#C9A03E"}, {"offset": 1, "color": "#8A6E28"}]}},
        stroke=INK, strokeWidth=3, radius=4)
d.text("A. GOLDBRICKER", "Nameplate text", x=505, y=734, size=13,
       font="Virelai Sans", color="#33261F", justify="center")

# --- feet up on the desk -----------------------------------------------------------
d.path("M470,640 C515,618 552,612 584,616", "Leg L", fill=NONE,
       stroke="#6E5940", strokeWidth=16, cap="round")
d.path("M540,642 C580,622 618,620 650,628", "Leg R", fill=NONE,
       stroke="#6E5940", strokeWidth=16, cap="round")
d.path(rot_rect_path(606, 610, 52, 26, -8), "Shoe L",
       fill=INK, stroke="#1A120C", strokeWidth=2)
d.path(rot_rect_path(670, 622, 52, 26, -8), "Shoe R",
       fill=INK, stroke="#1A120C", strokeWidth=2)

# --- monitor: immaculate dashboard ---------------------------------------------------
d.shape("rectangle", "Monitor stand", x=332, y=592, width=16, height=46,
        fill="#3A3428", stroke=INK, strokeWidth=3)
d.shape("rectangle", "Monitor", x=250, y=428, width=182, height=168,
        fill="#2A241C", stroke=INK, strokeWidth=5, radius=10)
d.shape("rectangle", "Screen", x=263, y=442, width=156, height=140,
        fill=SCREEN, stroke=NONE)
d.text("UTILIZATION", "Dash title", x=341, y=462, size=11,
       font="Virelai Sans", color="#7FAE98", justify="center")
d.text("100%", "Dash score", x=341, y=504, size=32,
       font="Virelai Sans", color="#8FE0A8", justify="center")
for i, x in enumerate([277, 312, 347, 382]):
    d.shape("rectangle", f"Dash bar {i+1}", x=x, y=556-42, width=20, height=42,
            fill="#4E9E5C", stroke="#2E5A38", strokeWidth=2, radius=2)
d.text("ALL GREEN", "Dash caption", x=341, y=574, size=10,
       font="Virelai Sans", color="#5E8E76", justify="center")

# --- coffee mug + report stack --------------------------------------------------------
d.shape("rectangle", "Mug", x=452, y=604, width=30, height=32,
        fill={"gradient": {"kind": "linear", "stops": [
            {"offset": 0, "color": "#B04A3E"}, {"offset": 1, "color": "#7A2E26"}]}},
        stroke=INK, strokeWidth=4, radius=4)
d.path("M482,611 C496,611 496,627 482,627", "Mug handle", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.path("M460,592 C462,586 464,582 466,578 M472,592 C474,586 476,582 478,578",
       "Steam", fill=NONE, stroke="#D8CBA8", strokeWidth=3, cap="round", opacity=60)
d.shape("rectangle", "Report stack", x=706, y=614, width=64, height=24,
        fill=PAPER, stroke=INK, strokeWidth=4, radius=2)
d.shape("rectangle", "Report top", x=702, y=606, width=64, height=14,
        fill=PAPER, stroke=INK, strokeWidth=4, radius=2)
d.text("RE: RE:", "Report label", x=734, y=616, size=9,
       font="Virelai Sans", color="#6E5A3C", justify="center")

# --- captions ---------------------------------------------------------------------------
d.text("APEX GOLDBRICKER", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#E8D9B0", justify="center")
r = d.text("ASPIRATIONAL NON-CONTRIBUTOR", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#B09A62", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("211.apex-goldbricker-V1R00")
