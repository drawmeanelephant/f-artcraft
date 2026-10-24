#!/usr/bin/env python3
"""APH-016 Jay Skript — aphorism plate V1R00. One terminal window split by
a crack: localhost green and ordered on the left, production red and
arriving out of order on the right. An elegant patch bandage over the
crack, already peeling on the prod side; error toasts popping out of the
frame. Dark slate plate. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("APH-016 Jay Skript — Aphorism Plate", 1000, 1000)

INK = "#16202A"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#141E26"}, {"offset": 1, "color": "#070B0E"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#2E4250"}, {"offset": 0.7, "color": "#182630"},
    {"offset": 1, "color": "#0B1218"}]}}
TERM_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1E2C34"}, {"offset": 1, "color": "#0E161B"}]}}
BAR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3A4E5C"}, {"offset": 1, "color": "#24333C"}]}}
GREEN = "#4EC488"
GREEN_DIM = "#3A8A64"
RED = "#E05A4A"
RED_DIM = "#A04034"
CREAM = "#D8E8E0"
FAINT = "#7A96A8"
PATCH_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E8D8A8"}, {"offset": 1, "color": "#B09A62"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#4E7A8C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#9FC4D8", strokeWidth=3, opacity=40)
for i, (x, y, w) in enumerate([(205, 220, 7), (798, 215, 8), (162, 500, 6),
                               (842, 495, 7), (245, 742, 6), (762, 738, 7)]):
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#4E7488", opacity=35, stroke=NONE)
# floor shadow under the terminal
d.shape("ellipse", "Floor shadow", x=280, y=640, width=440, height=50,
        fill="#000000", opacity=30, stroke=NONE)

# --- the terminal window -------------------------------------------------------
d.shape("rectangle", "Terminal", x=280, y=240, width=440, height=400,
        radius=12, fill=TERM_GRAD, stroke="#5E8296", strokeWidth=4)
# half-tints: local confidence left, production regret right
d.shape("rectangle", "Local tint", x=286, y=288, width=212, height=346,
        radius=8, fill=GREEN, opacity=8, stroke=NONE)
d.shape("rectangle", "Prod tint", x=502, y=288, width=212, height=346,
        radius=8, fill=RED, opacity=10, stroke=NONE)
# title bar
d.shape("rectangle", "Title bar", x=282, y=242, width=436, height=44,
        radius=10, fill=BAR_GRAD, stroke="#5E8296", strokeWidth=3)
d.shape("ellipse", "Dot local", x=298, y=256, width=16, height=16,
        fill=GREEN, stroke=INK, strokeWidth=2)
d.shape("ellipse", "Dot prod", x=322, y=256, width=16, height=16,
        fill=RED, stroke=INK, strokeWidth=2)
d.shape("ellipse", "Dot idle", x=346, y=256, width=16, height=16,
        fill="#C4A468", stroke=INK, strokeWidth=2)
d.text("localhost:3000", "Local tab", x=372, y=272, size=13,
       font="Virelai Sans", color=GREEN, justify="left")
d.text("prod", "Prod tab", x=646, y=272, size=13,
       font="Virelai Sans", color=RED, justify="left")

# --- left pane: clean, ordered, smug -------------------------------------------
lines_l = [("01", 330), ("02", 380), ("03", 430), ("04", 480)]
for num, ly in lines_l:
    d.text(num, f"L num {num}", x=300, y=ly, size=12,
           font="Virelai Sans", color=FAINT, justify="left")
    d.path(f"M330,{ly} L330,{ly - 9} M330,{ly - 5} L342,{ly - 17}",
           f"L check {num}", fill=NONE, stroke=GREEN, strokeWidth=3,
           cap="round")
    d.shape("rectangle", f"L bar {num}", x=352, y=ly - 15, width=110,
            height=12, radius=6, fill=GREEN, opacity=45, stroke=NONE)
    d.shape("rectangle", f"L bar2 {num}", x=352, y=ly + 2, width=70,
            height=10, radius=5, fill=GREEN, opacity=25, stroke=NONE)
d.text("$ npm test — all green", "Local caption", x=300, y=560, size=12,
       font="Virelai Sans", color=GREEN_DIM, justify="left")
d.text("$ deploy --prod --yolo", "Yolo caption", x=300, y=588, size=12,
       font="Virelai Sans", color=FAINT, justify="left")

# --- right pane: same lines, observed in production ------------------------------
lines_r = [("03", 330), ("01", 380), ("04", 430), ("02", 480)]
for num, ly in lines_r:
    d.text(num, f"R num {num}", x=516, y=ly, size=12,
           font="Virelai Sans", color=RED, justify="left")
    d.path(f"M546,{ly - 15} L560,{ly - 1} M546,{ly - 1} L560,{ly - 15}",
           f"R cross {num}", fill=NONE, stroke=RED, strokeWidth=3,
           cap="round")
    d.shape("rectangle", f"R bar {num}", x=572, y=ly - 15, width=110,
            height=12, radius=6, fill=RED, opacity=40, stroke=NONE)
    d.shape("rectangle", f"R bar2 {num}", x=572, y=ly + 2, width=70,
            height=10, radius=5, fill=RED, opacity=22, stroke=NONE)
# one line glitches sideways — async regret arriving out of order
d.shape("rectangle", "Glitch bar", x=600, y=512, width=100, height=12,
        radius=6, fill=RED, opacity=55, stroke=NONE)
d.shape("rectangle", "Glitch bar b", x=560, y=528, width=64, height=10,
        radius=5, fill=RED, opacity=30, stroke=NONE)
d.text("UnhandledPromiseRejection", "Prod caption", x=516, y=560, size=12,
       font="Virelai Sans", color=RED_DIM, justify="left")
d.text("(node:1) it worked locally", "Prod caption 2", x=516, y=588,
       size=12, font="Virelai Sans", color=FAINT, justify="left")

# --- the crack down the middle ---------------------------------------------------
d.path("M500,286 L488,330 L512,368 L492,414 L514,458 L494,508 L510,556 "
       "L498,600 L506,634", "The crack", fill=NONE, stroke="#0A0F13",
       strokeWidth=7, cap="round")
d.path("M500,286 L488,330 L512,368 L492,414 L514,458 L494,508 L510,556 "
       "L498,600 L506,634", "Crack highlight", fill=NONE, stroke="#6E96A8",
       strokeWidth=2, opacity=50, cap="round")

# --- the elegant patch, peeling on the prod side ---------------------------------
d.path(rot_rect_path(505, 424, 96, 34, 18), "Patch bandage",
       fill=PATCH_GRAD, stroke=INK, strokeWidth=3)
d.path(rot_rect_path(505, 424, 34, 20, 18), "Patch pad",
       fill="#C4AE76", stroke=INK, strokeWidth=2)
# lifted corner on the prod side — the patch observed in production
d.path("M540,404 L562,396 L548,418 Z", "Patch peel", fill="#8A7440",
       stroke=INK, strokeWidth=2)
r = d.text("PATCH", "Patch label", x=505, y=430, size=11,
           font="Virelai Sans", color="#5E4E22", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "patch tracking", ids=[r["id"]], tracking=30)

# --- error toasts popping out of the frame ---------------------------------------
for i, (tx, ty, msg) in enumerate([(742, 300, "ERR 500"),
                                   (756, 380, "TypeError"),
                                   (736, 462, "ERR ✕")]):
    d.shape("rectangle", f"Toast {i+1}", x=tx, y=ty, width=92, height=34,
            radius=8, fill="#2A1410", stroke=RED, strokeWidth=3)
    d.text(msg, f"Toast text {i+1}", x=tx + 46, y=ty + 22, size=12,
           font="Virelai Sans", color=RED, justify="center")
    # pop lines
    d.path(f"M{tx - 6},{ty + 10} L{tx - 18},{ty + 4} M{tx - 4},{ty + 26} "
           f"L{tx - 16},{ty + 30}", f"Toast pop {i+1}", fill=NONE,
           stroke=CREAM, strokeWidth=2.5, opacity=50, cap="round")

# --- aphorism line + name + role ---------------------------------------------------
r = d.text("DEPLOYS FIRST, INTERPRETS LATER:", "Key line 1", x=500, y=722,
           size=22, font="Virelai Sans", color="#9FC4D8", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "key1 tracking", ids=[r["id"]], tracking=100)
r = d.text("WORKS ON MY MACHINE.", "Key line 2", x=500, y=756,
           size=22, font="Virelai Sans", color="#9FC4D8", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "key2 tracking", ids=[r["id"]], tracking=100)

d.text("JAY SKRIPT", "Name", x=500, y=905, size=56,
       font="Virelai Sans", color=CREAM, justify="center")
r = d.text("CLIENT-SIDE CONFIDENCE BRIEFLY", "Role", x=500, y=950, size=18,
           font="Virelai Sans", color="#7A96A8", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=160)

d.finish("aph-016-jay-skript-V1R00")
