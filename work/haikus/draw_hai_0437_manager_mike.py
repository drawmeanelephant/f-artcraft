#!/usr/bin/env python3
"""HAI-0437 Manager Mike — haiku plate V1R00. The algorithmic manager: an empty
hi-vis vest hanging where a torso should be, a portcullis of steel thresholds
looming behind, workers reduced to data points under a firing line, and a
dashed empty slot where the appeal button used to be. Night shift, nobody home.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("HAI-0437 Manager Mike — Haiku Plate", 1000, 1000)

INK = "#33211B"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#18110D"}, {"offset": 1, "color": "#0A0706"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#32414C"}, {"offset": 0.7, "color": "#1B2830"},
    {"offset": 1, "color": "#0E171D"}]}}
STEEL = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7E93A0"}, {"offset": 1, "color": "#2C3C46"}]}}
VEST = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E8A24A"}, {"offset": 0.6, "color": "#C07A2C"},
    {"offset": 1, "color": "#8F5518"}]}}
STRIPE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#EDF2F2"}, {"offset": 1, "color": "#AEC0C6"}]}}
BADGE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#C8D4D8"}, {"offset": 1, "color": "#7E9098"}]}}
PALE = "#E6EFEA"
SOFT = "#93AEB0"
RED = "#E85C4A"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#6B7F8C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#DCE9E4", strokeWidth=3, opacity=38)
# cold light pool behind the vest
d.shape("ellipse", "Glow pool", x=280, y=230, width=440, height=420,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#9AB8C8", "opacity": 0.15},
            {"offset": 1, "color": "#9AB8C8", "opacity": 0}]}},
        stroke=NONE)

# --- night: a crescent moon keeps the only watch -------------------------------
d.shape("ellipse", "Moon", x=246, y=146, width=56, height=56,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#EDF2F0"}, {"offset": 1, "color": "#A9BEC4"}]}},
        stroke=NONE, opacity=85)
d.shape("ellipse", "Moon shadow", x=262, y=140, width=52, height=52,
        fill="#23333D", stroke=NONE, opacity=92)
d.shape("ellipse", "Moon glow", x=226, y=126, width=96, height=96,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#C8DEE4", "opacity": 0.16},
            {"offset": 1, "color": "#C8DEE4", "opacity": 0}]}},
        stroke=NONE)

# --- thresholds of steel: a portcullis looming behind everything -----------------
for i, bx in enumerate([330, 443, 557, 670]):
    d.shape("rectangle", f"Steel bar {i+1}", x=bx - 13, y=148, width=26,
            height=560, radius=4, fill=STEEL, stroke="#1B2830",
            strokeWidth=2, opacity=42)
d.shape("rectangle", "Gate lintel", x=300, y=138, width=400, height=30,
        radius=6, fill=STEEL, stroke="#1B2830", strokeWidth=2, opacity=48)
# rivets on the lintel
for i, rx in enumerate([330, 443, 557, 670]):
    d.shape("ellipse", f"Rivet {i+1}", x=rx - 4, y=147, width=8, height=8,
            fill="#AEC0C6", stroke=NONE, opacity=55)
# bar edge sheen
for i, bx in enumerate([330, 443, 557, 670]):
    d.path(f"M{bx - 7},160 L{bx - 7},700", f"Bar sheen {i+1}", fill=NONE,
           stroke="#C8DEE4", strokeWidth=3, opacity=20, cap="round")

# --- workers as data points: the chart panel ------------------------------------
d.shape("rectangle", "Chart panel", x=172, y=552, width=216, height=160,
        radius=10, fill={"gradient": {"kind": "linear", "stops": [
            {"offset": 0, "color": "#16232B"}, {"offset": 1, "color": "#0C161C"}]}},
        stroke="#4A626C", strokeWidth=3)
# faint grid
for i, gy in enumerate([586, 620, 654, 688]):
    d.path(f"M190,{gy} L372,{gy}", f"Panel grid {i+1}", fill=NONE,
           stroke="#33484F", strokeWidth=1, opacity=45)
# the firing threshold — a line of steel-red
d.path("M190,668 L372,668", "Threshold", fill=NONE, stroke=RED,
       strokeWidth=3, opacity=85, dash=[8, 5])
d.path("M190,664 L372,664", "Threshold glow", fill=NONE, stroke=RED,
       strokeWidth=8, opacity=15, cap="round")
# the workforce: a scatter of quiet dots above the line
for i, (cx, cy) in enumerate([(206, 600), (232, 636), (258, 592), (284, 622),
                              (310, 604), (336, 640), (358, 596), (220, 660),
                              (298, 646), (350, 628), (244, 612), (326, 588)]):
    d.shape("ellipse", f"Worker dot {i+1}", x=cx - 4, y=cy - 4, width=8,
            height=8, fill="#B9CDD4", stroke=NONE, opacity=75)
# the fired driver: falling, red, below the line
d.path("M268,684 L278,694 M278,684 L268,694", "Fired X 1", fill=NONE,
       stroke=RED, strokeWidth=3.5, cap="round")
d.path("M318,690 L328,700 M328,690 L318,700", "Fired X 2", fill=NONE,
       stroke=RED, strokeWidth=3.5, cap="round")
d.path("M346,682 L352,700", "Falling trail", fill=NONE, stroke=RED,
       strokeWidth=2, opacity=50, dash=[3, 3])

# --- the appeal slot: a dashed ghost where the button should be ------------------
d.shape("rectangle", "Appeal slot", x=628, y=596, width=196, height=72,
        radius=14, fill=NONE, stroke="#7E93A0", strokeWidth=3,
        opacity=45, dash=[9, 7])
r = d.text("APPEAL", "Appeal ghost", x=726, y=643, size=26,
           font="Virelai Sans", color="#7E93A0", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "appeal tracking", ids=[r["id"]], tracking=140)
    d.cmd("object.setProps", "appeal fade", ids=[r["id"]], opacity=38)
d.path("M662,654 L790,614", "Appeal strike", fill=NONE, stroke="#7E93A0",
       strokeWidth=3, opacity=40, cap="round")

# --- Manager Mike: the vest with no body ------------------------------------------
# void where the neck opens — the manager is the algorithm
d.path("M440,318 C455,295 545,295 560,318 C575,340 585,380 578,420 "
       "C585,470 588,520 585,565 L415,565 C412,520 415,470 422,420 "
       "C415,380 425,340 440,318 Z",
       "Vest body", fill=VEST, stroke=INK, strokeWidth=5, join="round")
# neck void: a dark V opening onto nothing
d.path("M474,298 L500,352 L526,298 C545,298 558,308 560,318 "
       "C545,304 455,304 440,318 C442,308 455,298 474,298 Z",
       "Neck void", fill="#10191F", stroke=INK, strokeWidth=3)
d.path("M476,300 L500,350 L524,300", "Neck void deep", fill=NONE,
       stroke="#060C0F", strokeWidth=8, opacity=55, cap="round")
# reflective harness: two vertical braces + two horizontal stripes
d.path("M458,306 L452,440 M542,306 L548,440", "Shoulder braces", fill=NONE,
       stroke="#D8E4E6", strokeWidth=15, opacity=90)
d.path("M424,446 L578,446", "Stripe upper", fill=NONE, stroke="#D8E4E6",
       strokeWidth=18, opacity=92)
d.path("M418,518 L584,518", "Stripe lower", fill=NONE, stroke="#D8E4E6",
       strokeWidth=18, opacity=92)
d.path("M424,446 L578,446 M418,518 L584,518", "Stripe gleam", fill=NONE,
       stroke="#FFFFFF", strokeWidth=4, opacity=45)
# zipper down the middle, undone at the void
d.path("M500,352 L500,565", "Zipper", fill=NONE, stroke="#6E3E12",
       strokeWidth=4, opacity=80)
# lanyard spilling out of the void, badge swinging
d.path("M500,352 C520,368 548,382 556,412", "Lanyard", fill=NONE,
       stroke="#33484F", strokeWidth=4, cap="round")
badge = d.shape("rectangle", "ID badge", x=536, y=408, width=44, height=58,
                radius=6, fill=BADGE, stroke=INK, strokeWidth=3)
d.shape("rectangle", "Badge photo", x=544, y=416, width=28, height=24,
        radius=3, fill="#46585F", stroke=NONE, opacity=80)
d.path("M546,448 L570,448 M546,456 L566,456", "Badge lines", fill=NONE,
       stroke="#46585F", strokeWidth=3, opacity=70, cap="round")
if badge and badge.get("id"):
    d.call("transform", {"ids": [badge["id"]], "rotate": 9,
                         "origin": [558, 412]}, "badge swing")
# vest shadow on the floor arc
d.shape("ellipse", "Vest shadow", x=415, y=572, width=170, height=20,
        fill="#060C0F", opacity=45, stroke=NONE)

# --- floor crescent, closed on the disc's own arc --------------------------------
d.path("M206,756 Q500,824 794,756 A420,420 0 0 1 206,756 Z",
       "Floor band", fill={"gradient": {"kind": "linear", "stops": [
           {"offset": 0, "color": "#0A1216", "opacity": 0},
           {"offset": 1, "color": "#060C0F", "opacity": 0.5}]}},
       stroke=NONE)

# --- name + key haiku line --------------------------------------------------------
r = d.text("no one to appeal.", "Key line", x=500, y=898, size=23,
           font="Virelai Sans", color=SOFT, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "key tracking", ids=[r["id"]], tracking=150)
d.text("MANAGER MIKE", "Name", x=500, y=948, size=58,
       font="Virelai Sans", color=PALE, justify="center")

d.finish("hai-0437-manager-mike-V1R00")
