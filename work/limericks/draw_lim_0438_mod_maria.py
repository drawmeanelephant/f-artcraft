#!/usr/bin/env python3
"""LIM-0438 Mod Maria — limerick plate V1R00. The night shift that never
ends: a review queue receding into darkness above the monitor, a
guidelines sheet whose words have lifted off as smoke, and Maria still
flagging items one by one while her own edges dim out of the frame.
Invisible labor, industrialized trauma, warm dark ink and violet night.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("LIM-0438 Mod Maria — Limerick Plate", 1000, 1000)

INK = "#201A28"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#16121E"}, {"offset": 1, "color": "#0A0710"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4C4470"}, {"offset": 0.7, "color": "#2E2846"},
    {"offset": 1, "color": "#161222"}]}}
DESK = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#38304E"}, {"offset": 1, "color": "#1A1526"}]}}
SCREEN = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1E3240"}, {"offset": 1, "color": "#0E1A24"}]}}
BODY = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E8ADA6"}, {"offset": 0.7, "color": "#C98A84"},
    {"offset": 1, "color": "#A06A66"}]}}
HAIR = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5E5480"}, {"offset": 1, "color": "#3A3252"}]}}
PAPER = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E4DCCA"}, {"offset": 1, "color": "#BFB69E"}]}}
CARD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3E3652"}, {"offset": 1, "color": "#262038"}]}}
AMBER = "#F0C878"
RED = "#D85448"
CREAM = "#E8E2F2"
TAN = "#A89CCC"
MOON = "#E4DCF0"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#6E6498", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#DCD4EC", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(190, 240, 8), (800, 230, 7), (160, 520, 9),
                               (830, 540, 8), (240, 760, 7), (760, 740, 9),
                               (130, 390, 6), (865, 390, 7), (390, 110, 7),
                               (610, 110, 8), (330, 820, 6), (665, 815, 7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#4A4266", opacity=45, stroke=NONE)

# --- the night: crescent moon + a couple of very late stars -------------------------
d.path("M232,152 A34,34 0 0 0 232,220 A40,40 0 0 1 232,152 Z",
       "Moon", fill=MOON, opacity=70, stroke=NONE)
for i, (sx, sy) in enumerate([(740, 150), (790, 196), (300, 140)]):
    d.path(f"M{sx},{sy-6} L{sx+2},{sy-2} L{sx+6},{sy} L{sx+2},{sy+2} "
           f"L{sx},{sy+6} L{sx-2},{sy+2} L{sx-6},{sy} L{sx-2},{sy-2} Z",
           f"Star {i+1}", fill=MOON, opacity=45, stroke=NONE)

# --- the queue that never ends: cards receding into the dark -------------------------
# a perspective column of pending items rising off the monitor into night
queue_cards = [
    (646, 470, 168, 40, 90), (640, 422, 156, 36, 78),
    (634, 378, 144, 33, 66), (630, 338, 132, 30, 55),
    (627, 302, 120, 27, 45), (625, 270, 108, 24, 36),
    (624, 242, 96, 21, 27), (623, 218, 84, 18, 19),
    (622, 198, 72, 15, 12),
]
for i, (cx, cy, cw, ch, op) in enumerate(queue_cards):
    d.shape("rectangle", f"Queue card {i+1}", x=cx, y=cy, width=cw,
            height=ch, fill=CARD, stroke="#565070",
            strokeWidth=max(1, 3 - i // 3), opacity=op, radius=4)
    if i < 5:
        # a flag notch + item line on the nearer cards
        fy = cy + ch // 2 - 5
        d.path(f"M{cx + 10},{fy} L{cx + 10},{fy + 10} L{cx + 20},{fy + 5} Z",
               f"Queue flag {i+1}", fill=AMBER, opacity=op - 5,
               stroke=NONE)
        d.shape("rectangle", f"Queue bar {i+1}", x=cx + 28,
                y=cy + ch // 2 - 3, width=int(cw * 0.62), height=6,
                fill="#565070", opacity=op - 10, stroke=NONE, radius=3)
# --- desk ---------------------------------------------------------------------------
d.shape("ellipse", "Desk", x=170, y=646, width=660, height=130,
        fill=DESK, stroke=NONE, opacity=92)
d.shape("ellipse", "Maria shadow", x=300, y=694, width=200, height=30,
        fill="#0A0714", opacity=55, stroke=NONE)

# --- the monitor she works -------------------------------------------------------------
d.path("M732,560 L732,636 M690,636 L774,636", "Monitor stand", fill=NONE,
       stroke=INK, strokeWidth=10, cap="round", join="round")
d.shape("rectangle", "Monitor", x=610, y=390, width=244, height=176,
        fill="#1C1626", stroke=INK, strokeWidth=6, radius=10)
d.shape("rectangle", "Screen", x=624, y=404, width=216, height=148,
        fill=SCREEN, stroke=NONE, radius=5)
# warm spill from the screen onto the desk
d.path("M624,552 L840,552 L806,634 L654,634 Z", "Screen spill",
       fill="#F0C878", opacity=9, stroke=NONE)
# queue header on screen
d.shape("rectangle", "Queue header", x=624, y=404, width=216, height=24,
        fill="#2E4250", stroke=NONE, radius=5)
d.text("REVIEW QUEUE", "Queue title", x=732, y=420, size=11,
       font="Virelai Sans", color="#BFE0E8", justify="center")
# the count — digits in Source Sans 3 (Virelai Sans has none)
d.text("2,147 PENDING", "Queue count", x=636, y=545, size=10,
       font="Source Sans 3", color="#8FD8C8", justify="left")
# rows: flag + item bar; one mid-flag amber, next already condemned red
rows = [(442, "#8FA8B2", "#3A5260"), (468, AMBER, "#5A4630"),
        (494, RED, "#5A3230"), (520, "#8FA8B2", "#3A5260")]
for i, (ry, flag, bar) in enumerate(rows):
    d.path(f"M634,{ry} L634,{ry+12} L646,{ry+6} Z", f"Row flag {i+1}",
           fill=flag, stroke=NONE)
    d.shape("rectangle", f"Row bar {i+1}", x=654, y=ry + 1, width=172,
            height=11, fill=bar, stroke=NONE, radius=3)
# the scrollbar that never shrinks
d.shape("rectangle", "Scrollbar track", x=830, y=428, width=5,
        height=118, fill="#141E28", stroke=NONE, radius=2)
d.shape("rectangle", "Scrollbar thumb", x=830, y=428, width=5,
        height=14, fill="#4A5E6E", stroke=NONE, radius=2)

# --- guidelines, rewriting themselves as smoke -------------------------------------------
# the sheet on the desk, half its lines already airborne
d.path("M228,584 L372,568 L384,660 L240,676 Z", "Guidelines sheet",
       fill=PAPER, stroke=INK, strokeWidth=4, join="round")
d.text("GUIDELINES v38", "Doc title", x=306, y=596, size=12,
       font="Source Sans 3", color="#5A5040", justify="center")
# remaining printed lines, getting fainter down the page
for i, (ly, lw, op) in enumerate([(612, 120, 75), (626, 104, 60),
                                  (640, 88, 45), (654, 66, 30)]):
    d.shape("rectangle", f"Doc line {i+1}", x=252, y=ly, width=lw,
            height=5, fill="#6A5E48", opacity=op, stroke=NONE,
            radius=2)
# the lifted lines: smoke wisps carrying the words away
for i, (sx, sy, sw, bend) in enumerate([(268, 548, 60, -18),
                                         (316, 540, 72, 14),
                                         (356, 552, 56, -8)]):
    d.path(f"M{sx},{sy} C{sx + bend},{sy - 30} {sx + sw - bend},"
           f"{sy - 46} {sx + sw},{sy - 78}",
           f"Smoke wisp {i+1}", fill=NONE, stroke="#C9BED8",
           strokeWidth=4, opacity=30 - i * 5, cap="round")
# ghost fragments of the old rules dissolving upward
for i, (gx, gy, gl, op) in enumerate([(246, 506, 34, 22),
                                      (300, 486, 28, 18),
                                      (350, 500, 22, 14)]):
    d.shape("rectangle", f"Ghost line {i+1}", x=gx, y=gy, width=gl,
            height=4, fill="#C9BED8", opacity=op, stroke=NONE,
            radius=2)

# --- Maria, still flagging, dimming ------------------------------------------------------
# legs — already less there
d.path("M388,652 L384,690", "Leg L", fill=NONE, stroke="#B07472",
       strokeWidth=13, cap="round", opacity=70)
d.path("M448,652 L454,690", "Leg R", fill=NONE, stroke="#A86A68",
       strokeWidth=13, cap="round", opacity=55)
d.shape("ellipse", "Shoe L", x=368, y=682, width=34, height=15, fill=INK,
        stroke=NONE, opacity=70)
d.shape("ellipse", "Shoe R", x=440, y=682, width=34, height=15, fill=INK,
        stroke=NONE, opacity=55)
# body, leaning toward the screen
d.path("M424,478 C482,478 510,524 507,576 C504,626 474,654 426,654 "
       "C378,654 348,626 345,576 C342,524 366,478 424,478 Z",
       "Maria body", fill=BODY, stroke=INK, strokeWidth=6)
d.path("M392,636 C420,648 462,648 488,634 C462,642 418,642 392,636 Z",
       "Body shadow", fill="#A86A68", opacity=45, stroke=NONE)
# hair cap + bun
d.path("M372,486 C366,436 392,404 426,404 C460,404 486,436 480,486 "
       "C468,468 452,458 426,458 C400,458 384,468 372,486 Z",
       "Hair", fill=HAIR, stroke=INK, strokeWidth=5)
d.shape("ellipse", "Bun", x=364, y=424, width=30, height=28, fill=HAIR,
        stroke=INK, strokeWidth=4)
# headset
d.path("M384,448 C390,420 408,408 426,408 C444,408 462,420 468,448",
       "Headset band", fill=NONE, stroke="#4E4470", strokeWidth=8,
       cap="round")
d.shape("ellipse", "Earpad L", x=378, y=458, width=20, height=26,
        fill="#3E3654", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Earpad R", x=454, y=458, width=20, height=26,
        fill="#3E3654", stroke=INK, strokeWidth=4)
d.path("M466,476 C482,490 490,504 488,518", "Mic boom", fill=NONE,
       stroke="#3E3654", strokeWidth=5, cap="round")
d.shape("ellipse", "Mic", x=480, y=514, width=14, height=12,
        fill="#3E3654", stroke=INK, strokeWidth=3)
# tired-warm face, lit by the queue
d.shape("ellipse", "Eye L", x=410, y=504, width=15, height=19, fill=INK,
        stroke=NONE)
d.shape("ellipse", "Eye R", x=448, y=504, width=15, height=19, fill=INK,
        stroke=NONE)
d.shape("ellipse", "Glint L", x=414, y=508, width=4, height=4,
        fill="#FFFFFF", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=452, y=508, width=4, height=4,
        fill="#FFFFFF", opacity=90, stroke=NONE)
# under-eye shadows — the shift shows
d.path("M408,528 Q417,533 426,529", "Under-eye L", fill=NONE,
       stroke="#8A5E5C", strokeWidth=3, opacity=60, cap="round")
d.path("M446,529 Q455,533 464,528", "Under-eye R", fill=NONE,
       stroke="#8A5E5C", strokeWidth=3, opacity=60, cap="round")
d.shape("ellipse", "Cheek L", x=394, y=530, width=22, height=13,
        fill="#E88C84", opacity=45, stroke=NONE)
d.shape("ellipse", "Cheek R", x=458, y=530, width=22, height=13,
        fill="#E88C84", opacity=45, stroke=NONE)
d.path("M422,552 C430,556 440,556 448,550", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.shape("ellipse", "Face glow", x=448, y=492, width=62, height=54,
        fill="#F5CE7E", opacity=10, stroke=NONE)
# right arm mid-flag over the keyboard
d.path("M500,564 C536,574 564,582 592,588", "Arm keys", fill=NONE,
       stroke="#D89E98", strokeWidth=12, cap="round")
d.shape("ellipse", "Hand keys", x=586, y=582, width=18, height=14,
        fill="#F2C9C0", stroke=INK, strokeWidth=3)
# the flag she's raising against item two
d.path("M560,584 L560,548", "Flag pole", fill=NONE, stroke="#8A90A0",
       strokeWidth=3.5, cap="round")
d.path("M560,548 L590,556 L560,564 Z", "Flag", fill=AMBER,
       stroke=INK, strokeWidth=2.5, join="round")
# left arm dangling a spent stylus — or what's left of one
d.path("M352,560 C336,580 332,604 338,624", "Arm stylus", fill=NONE,
       stroke="#C98882", strokeWidth=11, cap="round", opacity=75)
d.shape("ellipse", "Hand stylus", x=330, y=618, width=18, height=14,
        fill="#F2C9C0", stroke=INK, strokeWidth=3, opacity=75)
d.path("M344,626 L338,646", "Stylus", fill=NONE, stroke="#8A90A0",
       strokeWidth=3, cap="round", opacity=60)
# keyboard
d.path("M560,604 L706,604 L724,640 L544,640 Z", "Keyboard",
       fill="#2A2438", stroke=INK, strokeWidth=4, join="round")
for i, kx in enumerate(range(566, 706, 22)):
    d.path(f"M{kx},616 L{kx + 14},616", f"Key {i+1}", fill=NONE,
           stroke="#4A4262", strokeWidth=3, opacity=80)
# her edges dim: a wash of plate-dark over her left side, memory going
d.shape("ellipse", "Memory fade", x=272, y=470, width=200, height=240,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#2E2846", "opacity": 0.45},
            {"offset": 1, "color": "#2E2846", "opacity": 0}]}},
        stroke=NONE)

# --- cold coffee, long past steam ---------------------------------------------------------
d.shape("rectangle", "Mug", x=262, y=690, width=40, height=44,
        fill="#5E5480", stroke=INK, strokeWidth=4, radius=6)
d.path("M302,700 C316,700 316,722 302,722", "Mug handle", fill=NONE,
       stroke=INK, strokeWidth=5)
d.path("M276,690 L294,690", "Cold coffee", fill=NONE, stroke="#241C14",
       strokeWidth=4, opacity=80)

# --- captions -----------------------------------------------------------------------------
k = d.text("THE QUEUE NEVER EMPTIES AT NIGHT.", "Key line", x=500,
           y=862, size=23, font="Virelai Sans", color="#B4AAD8",
           justify="center")
if k and k.get("id"):
    d.cmd("text.setStyle", "key tracking", ids=[k["id"]], tracking=160)
d.text("MOD MARIA", "Name", x=500, y=930, size=58,
       font="Virelai Sans", color=CREAM, justify="center")
r = d.text("THE QUEUE NEVER EMPTIES", "Role", x=500, y=968, size=20,
           font="Virelai Sans", color=TAN, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=190)

d.finish("lim-0438-mod-maria-V1R00")
