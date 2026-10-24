#!/usr/bin/env python3
"""HAI-0438 Mod Maria — haiku plate V1R00. Industrialized empathy: an endless
queue of flagged items streams past Maria's terminal into the learning engine,
guidelines drift off as smoke, her silhouette sheds fading particles, and
wellness is a single PDF on the desk. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("HAI-0438 Mod Maria — Haiku Plate", 1000, 1000)

INK = "#33211B"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#181010"}, {"offset": 1, "color": "#0B0707"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#3C3549"}, {"offset": 0.7, "color": "#221D2F"},
    {"offset": 1, "color": "#130F1B"}]}}
FIGURE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5C5470"}, {"offset": 1, "color": "#2B2438"}]}}
SCREEN = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1E3038"}, {"offset": 1, "color": "#0E1B21"}]}}
CARD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#D8D2E2"}, {"offset": 1, "color": "#9A92AC"}]}}
CORE = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#8FB8E8"}, {"offset": 0.6, "color": "#4A5E8C"},
    {"offset": 1, "color": "#2A3352"}]}}
PALE = "#EBE5F0"
SOFT = "#A79BB8"
RED = "#E85C4A"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#7B6F8C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E4DCF0", strokeWidth=3, opacity=38)
d.shape("ellipse", "Glow pool", x=300, y=280, width=460, height=380,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#9A8CC0", "opacity": 0.14},
            {"offset": 1, "color": "#9A8CC0", "opacity": 0}]}},
        stroke=NONE)

# --- the queue that never empties: flagged cards arcing in from the rim ---------
cards = [(256, 204, 40, 30, -12, 40), (292, 250, 46, 34, -8, 55),
         (332, 296, 52, 38, -4, 70), (374, 344, 58, 42, 2, 85),
         (414, 392, 64, 46, 6, 100)]
for i, (cx, cy, w, h, rot, op) in enumerate(cards):
    r = d.shape("rectangle", f"Queue card {i+1}", x=cx - w/2, y=cy - h/2,
                width=w, height=h, radius=5, fill=CARD, stroke=INK,
                strokeWidth=3, opacity=op)
    d.path(f"M{cx - w/2 + 8},{cy - 2} L{cx - w/2 + 8},{cy - h/2 + 16} "
           f"L{cx - w/2 + 8 + w*0.32},{cy - h/2 + 10} Z",
           f"Card flag {i+1}", fill=RED, stroke=NONE, opacity=op)
    d.path(f"M{cx - w/2 + 8},{cy - 2} L{cx - w/2 + 8},{cy + h/2 - 6}",
           f"Flag pole {i+1}", fill=NONE, stroke=INK, strokeWidth=2,
           opacity=op)
    if r and r.get("id") and rot:
        d.call("transform", {"ids": [r["id"]], "rotate": rot,
                             "origin": [cx, cy]}, f"card {i+1} tilt")

# --- the learning engine: a node-mesh hexagon drinking the stream ----------------
d.shape("ellipse", "Core glow", x=630, y=220, width=220, height=220,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#7FA4E0", "opacity": 0.22},
            {"offset": 1, "color": "#7FA4E0", "opacity": 0}]}},
        stroke=NONE)
d.path("M740,252 L792,282 L792,342 L740,372 L688,342 L688,282 Z",
       "AI core", fill=CORE, stroke=INK, strokeWidth=4, join="round")
# internal mesh: absorbed judgments crystallizing
nodes = [(740, 312), (714, 292), (766, 292), (722, 336), (758, 336), (740, 272)]
for i, (x1, y1) in enumerate(nodes):
    for j, (x2, y2) in enumerate(nodes):
        if j > i and abs(x1 - x2) + abs(y1 - y2) < 55:
            d.path(f"M{x1},{y1} L{x2},{y2}", f"Mesh {i}-{j}", fill=NONE,
                   stroke="#C8D8F0", strokeWidth=1.5, opacity=40)
for i, (nx, ny) in enumerate(nodes):
    d.shape("ellipse", f"Core node {i+1}", x=nx - 4, y=ny - 4, width=8,
            height=8, fill="#DCE8F8", stroke=NONE, opacity=90)
# what it learned: one tiny red flag, digested
d.path("M735,318 L735,300 L752,306 Z", "Learned flag", fill=RED,
       stroke=NONE, opacity=85)
# the stream in: cards shrinking into the core
for i, (cx, cy, w) in enumerate([(560, 330, 34), (606, 318, 26),
                                 (648, 310, 18)]):
    d.shape("rectangle", f"Inflow {i+1}", x=cx - w/2, y=cy - w*0.38,
            width=w, height=w*0.76, radius=3, fill=CARD, stroke=INK,
            strokeWidth=2, opacity=80 - i * 15)

# --- guidelines, shifting like smoke ---------------------------------------------
for i, (sx, sy, drift) in enumerate([(300, 470, -30), (340, 450, 20),
                                     (380, 480, -15)]):
    d.path(f"M{sx},{sy} C{sx + drift},{sy - 60} {sx - drift},{sy - 110} "
           f"{sx + drift},{sy - 170}",
           f"Smoke {i+1}", fill=NONE, stroke="#B8ACD0", strokeWidth=6 - i,
           opacity=16, cap="round")

# --- Maria at the terminal, her edges already dissolving --------------------------
d.shape("ellipse", "Maria shadow", x=330, y=688, width=210, height=24,
        fill="#0A0710", opacity=50, stroke=NONE)
# chair hint
d.path("M362,560 L362,690 M338,690 L386,690", "Chair back", fill=NONE,
       stroke="#241D30", strokeWidth=14, cap="round")
# torso: hunched forward into the screen
d.path("M392,560 C386,600 384,648 386,690 L496,690 C496,640 492,596 480,566 "
       "C462,548 414,546 392,560 Z",
       "Maria torso", fill=FIGURE, stroke=INK, strokeWidth=4.5)
# head, bowed
d.shape("ellipse", "Maria head", x=404, y=472, width=64, height=68,
        fill=FIGURE, stroke=INK, strokeWidth=4.5)
# headset band + muff — the uniform of the queue
d.path("M408,500 C404,470 466,468 464,498", "Headset band", fill=NONE,
       stroke="#181220", strokeWidth=7, cap="round")
d.shape("ellipse", "Headset muff", x=456, y=498, width=16, height=24,
        fill="#181220", stroke=INK, strokeWidth=2.5)
d.path("M462,522 C470,528 476,534 478,542", "Mic boom", fill=NONE,
       stroke="#181220", strokeWidth=4, cap="round")
# memory fading: particles sloughing off her back
for i, (cx, cy, w, op) in enumerate([(376, 540, 7, 45), (356, 576, 6, 38),
                                     (368, 616, 5, 32), (336, 552, 5, 28),
                                     (348, 636, 4, 24), (318, 590, 5, 20),
                                     (328, 516, 4, 18), (300, 560, 4, 14),
                                     (352, 500, 4, 22), (306, 620, 3, 12)]):
    d.shape("ellipse", f"Fading {i+1}", x=cx, y=cy, width=w, height=w,
            fill="#9A8CC0", stroke=NONE, opacity=op)
# reaching arm to the keyboard
d.path("M470,600 C500,604 524,616 540,634", "Maria arm", fill=NONE,
       stroke="#4A4260", strokeWidth=16, cap="round")

# --- the terminal: her whole horizon ----------------------------------------------
d.shape("rectangle", "Monitor", x=520, y=430, width=150, height=180,
        radius=8, fill=SCREEN, stroke=INK, strokeWidth=4)
# the feed, clean on our side: rows of thumbnails, one flagged
for i, ty in enumerate([452, 490, 528]):
    d.shape("rectangle", f"Feed row {i+1}", x=534, y=ty, width=88,
            height=26, radius=4, fill="#3A4E58", stroke=NONE, opacity=85)
    d.shape("ellipse", f"Row dot {i+1}", x=632, y=ty + 6, width=14,
            height=14, fill="#7FA4B0", stroke=NONE, opacity=70)
d.shape("rectangle", "Flagged row", x=534, y=566, width=88, height=26,
        radius=4, fill="#4A3440", stroke=RED, strokeWidth=2.5, opacity=95)
d.path("M632,584 L642,590 L642,572 Z", "Row flag", fill=RED, stroke=NONE)
# monitor glow on her face
d.path("M452,486 L468,520", "Screen light", fill=NONE, stroke="#A8D8E0",
       strokeWidth=5, opacity=25, cap="round")
# desk line
d.path("M330,692 L784,692", "Desk", fill=NONE, stroke="#241D30",
       strokeWidth=8, cap="round")

# --- wellness is a PDF -------------------------------------------------------------
d.shape("rectangle", "Wellness PDF", x=700, y=610, width=56, height=72,
        radius=4, fill={"gradient": {"kind": "linear", "stops": [
            {"offset": 0, "color": "#E8E2EC"}, {"offset": 1, "color": "#B0A6C0"}]}},
        stroke=INK, strokeWidth=3)
d.path("M738,610 L756,610 L756,628 Z", "PDF fold", fill="#8C80A0",
       stroke=INK, strokeWidth=2)
# a little lotus of corporate serenity
d.path("M714,652 C716,642 722,636 728,634 C734,636 740,642 742,652 "
       "C736,656 720,656 714,652 Z",
       "Lotus", fill="#7FA4B0", stroke=NONE, opacity=90)
d.path("M714,668 L744,668 M718,674 L740,674", "PDF text lines", fill=NONE,
       stroke="#6A5E80", strokeWidth=2.5, opacity=70, cap="round")

# --- floor crescent, closed on the disc's own arc ----------------------------------
d.path("M206,756 Q500,824 794,756 A420,420 0 0 1 206,756 Z",
       "Floor band", fill={"gradient": {"kind": "linear", "stops": [
           {"offset": 0, "color": "#0C0912", "opacity": 0},
           {"offset": 1, "color": "#080610", "opacity": 0.55}]}},
       stroke=NONE)

# --- name + key haiku line ----------------------------------------------------------
r = d.text("wellness is a PDF.", "Key line", x=500, y=898, size=23,
           font="Virelai Sans", color=SOFT, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "key tracking", ids=[r["id"]], tracking=150)
d.text("MOD MARIA", "Name", x=500, y=948, size=58,
       font="Virelai Sans", color=PALE, justify="center")

d.finish("hai-0438-mod-maria-V1R00")
