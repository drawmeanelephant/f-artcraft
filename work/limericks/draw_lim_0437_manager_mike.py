#!/usr/bin/env python3
"""LIM-0437 Manager Mike — limerick plate V1R00. The algorithmic manager:
a vest-wearing overseer with a monitor for a head, thresholds of steel
looming like a portcullis behind him, workers reduced to data points on
a graph he alone can read, and a console where the appeal button used
to be. Corporate surveillance, cold steel over warm dark ink.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("LIM-0437 Manager Mike — Limerick Plate", 1000, 1000)

INK = "#1C1916"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#181512"}, {"offset": 1, "color": "#0C0A08"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4E5258"}, {"offset": 0.7, "color": "#2E3236"},
    {"offset": 1, "color": "#17191C"}]}}
STEEL = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7A828C"}, {"offset": 0.5, "color": "#4E545C"},
    {"offset": 1, "color": "#2E3236"}]}}
VEST = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6E5A38"}, {"offset": 1, "color": "#453520"}]}}
BRASS = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#C9A05C"}, {"offset": 1, "color": "#8A6A38"}]}}
SCREEN = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#26333C"}, {"offset": 1, "color": "#111A20"}]}}
CONSOLE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5A5E64"}, {"offset": 1, "color": "#36393E"}]}}
RED = "#D04A3A"
GREEN = "#58C878"
CREAM = "#E4E0D4"
TAN = "#9AA0A8"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#5E6670", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8DCE2", strokeWidth=3, opacity=45)
for i, (x, y, w) in enumerate([(190, 240, 8), (800, 230, 7), (160, 520, 9),
                               (830, 540, 8), (240, 760, 7), (760, 740, 9),
                               (130, 390, 6), (865, 390, 7), (390, 110, 7),
                               (610, 110, 8), (330, 820, 6), (665, 815, 7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#3E434A", opacity=45, stroke=NONE)

# --- thresholds of steel: the looming portcullis ------------------------------------
# vertical slats rising the full height of the scene, cold and even
for i, bx in enumerate([196, 288, 380, 620, 712, 804]):
    d.shape("rectangle", f"Steel slat {i+1}", x=bx - 13, y=230,
            width=26, height=520, fill=STEEL, stroke=INK,
            strokeWidth=3, opacity=80, radius=3)
    # a machined glint on each slat's left edge
    d.path(f"M{bx - 8},248 L{bx - 8},730", f"Slat glint {i+1}",
           fill=NONE, stroke="#A8B0BA", strokeWidth=2.5, opacity=40)
# crossbar yoking them together
d.shape("rectangle", "Threshold beam", x=168, y=196, width=668,
        height=30, fill=STEEL, stroke=INK, strokeWidth=4, radius=4)
for i, rx in enumerate(range(196, 837, 92)):
    d.shape("ellipse", f"Rivet {i+1}", x=rx, y=204, width=12, height=12,
            fill="#2E3236", stroke="#7A828C", strokeWidth=2)
# red threshold line scored across the bars at head height
d.path("M172,352 L836,352", "Threshold line", fill=NONE, stroke=RED,
       strokeWidth=4, opacity=75, dash=[14, 10])

# --- floor ----------------------------------------------------------------------
d.shape("ellipse", "Floor", x=180, y=668, width=640, height=110,
        fill={"gradient": {"kind": "linear", "stops": [
            {"offset": 0, "color": "#23262A"},
            {"offset": 1, "color": "#121417"}]}},
        stroke=NONE, opacity=90)
d.shape("ellipse", "Mike shadow", x=390, y=724, width=220, height=28,
        fill="#08090B", opacity=55, stroke=NONE)

# --- the workers: data points under review -------------------------------------------
# evaluation panel, right side
d.shape("ellipse", "Panel glow", x=586, y=380, width=260, height=200,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#6EB8D8", "opacity": 0.10},
            {"offset": 1, "color": "#6EB8D8", "opacity": 0}]}},
        stroke=NONE)
d.shape("rectangle", "Eval panel", x=600, y=392, width=220, height=170,
        fill=SCREEN, stroke=INK, strokeWidth=5, radius=10)
d.text("HEADCOUNT METRICS", "Panel title", x=710, y=418, size=13,
       font="Virelai Sans", color="#7E96A4", justify="center")
# grid
for i, gy in enumerate([444, 478, 512]):
    d.path(f"M616,{gy} L804,{gy}", f"Eval grid {i+1}", fill=NONE,
           stroke="#1E2E36", strokeWidth=1.5, opacity=80)
# the threshold: a hard red rule; below it you are a rounding error
d.path("M616,478 L804,478", "Panel threshold", fill=NONE, stroke=RED,
       strokeWidth=3, opacity=85)
# workers as data points: greens above the line, reds sinking below it
pts = [(636, 452, GREEN), (668, 440, GREEN), (700, 458, GREEN),
       (732, 446, GREEN), (764, 452, GREEN), (790, 442, GREEN),
       (648, 500, RED), (686, 522, RED), (722, 508, RED),
       (756, 530, RED), (786, 516, RED)]
for i, (px, py, c) in enumerate(pts):
    d.shape("ellipse", f"Worker {i+1}", x=px - 5, y=py - 5, width=10,
            height=10, fill=c, opacity=85 if c == GREEN else 65,
            stroke=NONE)
# one point mid-fall through the line — a person becoming a statistic
d.shape("ellipse", "Falling worker", x=706, y=474, width=9, height=9,
        fill="#E8A84A", opacity=90, stroke=NONE)
d.path("M710,486 L710,498 M706,494 L710,498 L714,494", "Fall arrow",
       fill=NONE, stroke="#E8A84A", strokeWidth=2.5, opacity=80,
       cap="round")
d.text("Q3", "Panel quarter", x=632, y=418, size=11,
       font="Source Sans 3", color="#5E7884", justify="left")

# --- the console: where the appeal button used to be ---------------------------------
d.shape("rectangle", "Console", x=180, y=560, width=190, height=110,
        fill=CONSOLE, stroke=INK, strokeWidth=5, radius=10)
d.shape("rectangle", "Console top", x=180, y=560, width=190, height=26,
        fill="#6A6E74", stroke=INK, strokeWidth=4, radius=10)
# the empty socket: screw holes + ghost ring of the removed button
d.shape("ellipse", "Button ghost ring", x=224, y=606, width=46, height=46,
        fill=NONE, stroke="#7A828C", strokeWidth=3, opacity=60,
        dash=[6, 5])
d.shape("ellipse", "Socket dark", x=238, y=620, width=18, height=18,
        fill="#14161A", stroke=INK, strokeWidth=2.5)
for i, (sx, sy) in enumerate([(212, 614), (272, 614), (212, 648),
                              (272, 648)]):
    d.shape("ellipse", f"Screw hole {i+1}", x=sx, y=sy, width=7,
            height=7, fill="#14161A", stroke=NONE)
# dust that settled where fingers used to press
d.shape("ellipse", "Button dust", x=228, y=610, width=40, height=30,
        fill="#9AA0A8", opacity=10, stroke=NONE)
# remaining controls: a keypad nobody needs
for i, kx in enumerate([308, 322, 336]):
    d.shape("ellipse", f"Key {i+1}", x=kx, y=612, width=10, height=10,
            fill="#2E3236", stroke=INK, strokeWidth=2)
d.shape("rectangle", "Console slot", x=300, y=636, width=56, height=8,
        fill="#14161A", stroke=NONE, radius=3)
# the faintest worn legend under the socket — letters buffed away
t = d.text("APPEAL", "Worn legend", x=247, y=600, size=10,
           font="Virelai Sans", color="#6A6E74", justify="center")
if t and t.get("id"):
    d.cmd("object.setProps", "legend fade", ids=[t["id"]], opacity=35)

# --- Manager Mike: vest, monitor head, clipboard --------------------------------------
# legs + shoes
d.path("M466,648 L462,724", "Leg L", fill=NONE, stroke="#2A2C30",
       strokeWidth=15, cap="round")
d.path("M516,648 L520,724", "Leg R", fill=NONE, stroke="#24262A",
       strokeWidth=15, cap="round")
d.shape("ellipse", "Shoe L", x=442, y=716, width=38, height=17, fill=INK,
        stroke=NONE)
d.shape("ellipse", "Shoe R", x=506, y=716, width=38, height=17, fill=INK,
        stroke=NONE)
# the vest over a shirt — manager of nothing human
d.path("M430,470 L552,470 L566,648 L416,648 Z", "Shirt", fill="#3A3E44",
       stroke=INK, strokeWidth=5, join="round")
d.path("M436,478 L491,530 L546,478 L556,648 L426,648 Z", "Vest",
       fill=VEST, stroke=INK, strokeWidth=5, join="round")
d.path("M491,530 L491,648", "Vest seam", fill=NONE, stroke=INK,
       strokeWidth=4, opacity=60)
for i, by in enumerate([556, 596, 636]):
    d.shape("ellipse", f"Button {i+1}", x=484, y=by, width=13, height=13,
            fill=BRASS, stroke=INK, strokeWidth=3)
# collar + the world's plainest tie
d.path("M468,470 L491,494 L514,470", "Collar", fill=NONE,
       stroke="#C9CDD4", strokeWidth=7, join="round")
d.path("M491,494 L483,540 L491,566 L499,540 Z", "Tie", fill="#7A3A34",
       stroke=INK, strokeWidth=3, join="round")
# arms: left holding the clipboard, right flat at his side
d.path("M432,510 C404,540 396,580 404,614", "Arm L", fill=NONE,
       stroke="#3A3E44", strokeWidth=17, cap="round")
d.path("M552,510 C574,540 580,580 574,614", "Arm R", fill=NONE,
       stroke="#3A3E44", strokeWidth=17, cap="round")
d.shape("ellipse", "Hand R", x=564, y=606, width=22, height=20,
        fill="#C9CDD4", stroke=INK, strokeWidth=4)
# clipboard of verdicts
d.path(rot := "M404,568 L468,556 L482,632 L418,644 Z", "Clipboard",
       fill={"gradient": {"kind": "linear", "stops": [
           {"offset": 0, "color": "#5E6670"},
           {"offset": 1, "color": "#3A3E44"}]}},
       stroke=INK, strokeWidth=4, join="round")
d.shape("rectangle", "Clip", x=424, y=550, width=24, height=12,
        fill=BRASS, stroke=INK, strokeWidth=3, radius=3)
for i, ly in enumerate([580, 594, 608]):
    d.path(f"M420,{ly} L462,{ly-6}", f"Clip line {i+1}", fill=NONE,
           stroke="#8A929C", strokeWidth=2.5, opacity=70)
d.path("M420,626 L446,622 M458,616 L470,612", "Clip check", fill=NONE,
       stroke=RED, strokeWidth=3, opacity=80, cap="round")
d.shape("ellipse", "Hand L", x=460, y=596, width=20, height=18,
        fill="#C9CDD4", stroke=INK, strokeWidth=4)
# the monitor head, tilted a sympathetic four degrees
head_ids = []
def add_h(res):
    if res and res.get("id"):
        head_ids.append(res["id"])
add_h(d.shape("rectangle", "Monitor head", x=434, y=330, width=116,
              height=108, fill=CONSOLE, stroke=INK, strokeWidth=6,
              radius=10))
add_h(d.shape("rectangle", "Face screen", x=446, y=342, width=92,
              height=84, fill=SCREEN, stroke=NONE, radius=6))
# the face: a single evaluating readout — two eyes as status dots, flat mouth
add_h(d.shape("ellipse", "Eye L", x=466, y=368, width=14, height=14,
              fill="#7FD8E8", stroke=NONE))
add_h(d.shape("ellipse", "Eye R", x=506, y=368, width=14, height=14,
              fill="#7FD8E8", stroke=NONE))
add_h(d.path("M470,402 L516,402", "Mouth readout", fill=NONE,
             stroke="#7FD8E8", strokeWidth=4, cap="round", opacity=85))
# tiny descending sparkline where a smile would go
add_h(d.path("M452,416 L466,410 L478,414 L492,406", "Sentiment tick",
             fill=NONE, stroke=RED, strokeWidth=2.5, opacity=80))
# antenna + status LED
add_h(d.path("M548,344 L566,324", "Antenna", fill=NONE, stroke=INK,
             strokeWidth=5, cap="round"))
add_h(d.shape("ellipse", "Antenna tip", x=562, y=316, width=10, height=10,
              fill=RED, stroke=INK, strokeWidth=2))
add_h(d.shape("ellipse", "Neck", x=480, y=430, width=24, height=16,
              fill=INK, stroke=NONE))
if head_ids:
    d.cmd("object.rotate", "head tilt", ids=head_ids, angle=4,
          origin=[492, 384])
# scanline shimmer across the face screen
d.path("M450,376 L534,376 M450,394 L534,394", "Scanlines", fill=NONE,
       stroke="#3E525E", strokeWidth=1.5, opacity=40)

# --- captions -------------------------------------------------------------------------
k = d.text("THE ALGORITHM DOES WHAT IT LIKES BEST.", "Key line", x=500,
           y=862, size=23, font="Virelai Sans", color="#B8BEC6",
           justify="center")
if k and k.get("id"):
    d.cmd("text.setStyle", "key tracking", ids=[k["id"]], tracking=140)
d.text("MANAGER MIKE", "Name", x=500, y=930, size=58,
       font="Virelai Sans", color=CREAM, justify="center")
r = d.text("THRESHOLDS OF STEEL", "Role", x=500, y=968, size=20,
           font="Virelai Sans", color=TAN, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=190)

d.finish("lim-0437-manager-mike-V1R00")
