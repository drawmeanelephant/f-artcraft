#!/usr/bin/env python3
"""Deepfake Dave — mascot portrait V1R00.
Mascot at a generation pipeline rendering a synthetic video from a small
source sample. 1000x1000. House style: gradients + translucent shading."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Deepfake Dave — Mascot Portrait", 1000, 1000)

INK = "#24222E"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#0C1A22"}, {"offset": 1, "color": "#040E12"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#2F6B6E"}, {"offset": 0.7, "color": "#1E4A50"},
    {"offset": 1, "color": "#12333A"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1F4248"}, {"offset": 1, "color": "#10262C"}]}}
MACHINE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#46586A"}, {"offset": 1, "color": "#26323E"}]}}
SCREEN = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#123840"}, {"offset": 1, "color": "#081E24"}]}}
HOODIE = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#6E5A96"}, {"offset": 0.75, "color": "#4A3A6E"},
    {"offset": 1, "color": "#332850"}]}}
CLAPPER = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3A3E48"}, {"offset": 1, "color": "#22242C"}]}}
FACE_HALF = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F0CDA8"}, {"offset": 1, "color": "#C99A72"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#4E8A8C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#CFE8E4", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(195,235,8),(800,225,7),(155,525,9),(838,540,8),
                               (250,765,7),(750,750,9),(132,395,6),(862,385,7),
                               (390,112,7),(615,108,8),(330,822,6),(668,818,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#3E7078", opacity=45, stroke=NONE)

# --- floor: bottom segment closed on the disc's own arc -----------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0C1E24",
       strokeWidth=4, opacity=70)

# --- output screen: the rendered face, half pixelated --------------------------
d.shape("ellipse", "Screen glow", x=520, y=130, width=320, height=230,
        fill="#5FD8C8", opacity=10, stroke=NONE)
d.shape("rectangle", "Out bezel", x=545, y=140, width=280, height=200,
        fill=MACHINE, stroke=INK, strokeWidth=5, radius=10)
d.shape("rectangle", "Out screen", x=560, y=155, width=250, height=170,
        fill=SCREEN, stroke="#06181C", strokeWidth=3, radius=6)
# face: left half smooth, right half dissolving into pixels
d.path("M685,185 C720,185 745,212 745,248 C745,285 720,312 685,312 "
       "C650,312 627,285 627,248 C627,212 650,185 685,185 Z",
       "Render face", fill=FACE_HALF, stroke=INK, strokeWidth=4, opacity=95)
# pixel dissolves on the right side
for i, (x, y, s, o) in enumerate([(730,200,16,85),(748,222,12,70),(742,255,15,80),
                                  (726,280,11,65),(756,240,9,55),(715,190,9,60),
                                  (762,265,8,45),(736,300,10,60)]):
    d.shape("rectangle", f"Pixel {i+1}", x=x, y=y, width=s, height=s,
            fill="#F0CDA8", opacity=o, stroke=NONE)
for i, (x, y, s) in enumerate([(770,215,7),(778,255,6),(768,290,7),(782,240,5)]):
    d.shape("rectangle", f"Stray pixel {i+1}", x=x, y=y, width=s, height=s,
            fill="#5FD8C8", opacity=45, stroke=NONE)
# one real eye, one pixel-block eye
d.shape("ellipse", "Eye real", x=648, y=238, width=14, height=17,
        fill="#24222E", stroke=NONE)
d.shape("rectangle", "Eye block", x=706, y=236, width=15, height=15,
        fill="#24222E", stroke=NONE, radius=2)
d.path("M655,282 C665,290 682,290 690,282", "Half smile", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
# scanline sweeping the face
d.path("M627,262 L760,262", "Scanline", fill=NONE, stroke="#5FD8C8",
       strokeWidth=3, opacity=60)
d.text("RENDER 87%", "Render label", x=575, y=318, size=12, font="Virelai Sans",
       color="#7EDCCB", justify="left")
d.shape("rectangle", "Stand", x=665, y=340, width=40, height=115,
        fill=MACHINE, stroke=INK, strokeWidth=4)
d.path("M640,455 L730,455 L740,469 L630,469 Z", "Foot",
       fill=MACHINE, stroke=INK, strokeWidth=4)

# --- the pipeline machine -------------------------------------------------------
d.shape("rectangle", "Machine", x=520, y=470, width=290, height=210,
        fill=MACHINE, stroke=INK, strokeWidth=6, radius=12)
# hopper on top
d.path("M555,470 L555,415 L650,415 L650,470", "Hopper", fill="#33404E",
       stroke=INK, strokeWidth=5, join="round")
d.path("M560,420 L645,420", "Hopper lip", fill=NONE, stroke="#5FD8C8",
       strokeWidth=3, opacity=60)
# gear window
d.shape("ellipse", "Gear well", x=545, y=505, width=100, height=100,
        fill="#16232C", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Gear", x=565, y=525, width=60, height=60,
        fill="#5FD8C8", opacity=80, stroke=INK, strokeWidth=4)
for i in range(8):
    import math
    a = math.radians(i*45)
    cx, cy = 595, 555
    x1, y1 = cx+34*math.cos(a), cy+34*math.sin(a)
    x2, y2 = cx+44*math.cos(a), cy+44*math.sin(a)
    d.path(f"M{x1:.0f},{y1:.0f} L{x2:.0f},{y2:.0f}", f"Tooth {i+1}",
           fill=NONE, stroke="#5FD8C8", strokeWidth=7, cap="round")
d.shape("ellipse", "Gear hub", x=583, y=543, width=24, height=24,
        fill="#16232C", stroke=INK, strokeWidth=3)
# vents + progress bar
for i in range(4):
    d.shape("rectangle", f"Vent {i+1}", x=680, y=515+i*20, width=100, height=8,
            fill="#16232C", opacity=70, stroke=NONE, radius=4)
d.shape("rectangle", "Bar shell", x=680, y=605, width=105, height=16,
        fill="#16232C", stroke=INK, strokeWidth=3, radius=8)
d.shape("rectangle", "Bar fill", x=683, y=608, width=88, height=10,
        fill="#5FD8C8", stroke=NONE, radius=5)
d.text("SYNTH NODE", "Machine label", x=680, y=655, size=14, font="Virelai Sans",
       color="#9AB8C4", justify="left")
# feet
d.shape("rectangle", "Foot L", x=545, y=680, width=30, height=18,
        fill="#26323E", stroke=INK, strokeWidth=4, radius=4)
d.shape("rectangle", "Foot R", x=755, y=680, width=30, height=18,
        fill="#26323E", stroke=INK, strokeWidth=4, radius=4)

# --- source sample: the tiny photo feeding the hopper ---------------------------
d.path("M470,470 L545,470 L545,545 L470,545 Z", "Source photo",
       fill="#E8DCC8", stroke=INK, strokeWidth=4, join="round")
d.shape("ellipse", "Source face", x=488, y=488, width=40, height=40,
        fill=FACE_HALF, stroke=INK, strokeWidth=3)
d.path("M495,505 L503,505 M512,505 L520,505", "Source eyes", fill=NONE,
       stroke=INK, strokeWidth=3, cap="round")
d.path("M500,518 C505,521 512,521 517,518", "Source smile", fill=NONE,
       stroke=INK, strokeWidth=3, cap="round")
# feed arrow into hopper
d.path("M530,455 C560,440 575,435 590,432", "Feed arrow", fill=NONE,
       stroke="#5FD8C8", strokeWidth=4, dash=[7,6], cap="round", opacity=75)
d.path("M588,424 L604,430 L588,438", "Feed head", fill=NONE,
       stroke="#5FD8C8", strokeWidth=4, cap="round", join="round", opacity=75)

# --- Dave: clapperboard-headed operator -----------------------------------------
d.shape("ellipse", "Dave shadow", x=255, y=680, width=230, height=30,
        fill="#08181C", opacity=45, stroke=NONE)
# body: hoodie blob
d.path("M370,540 C440,540 482,595 482,650 C482,695 440,715 370,715 "
       "C300,715 258,695 258,650 C258,595 300,540 370,540 Z",
       "Dave body", fill=HOODIE, stroke=INK, strokeWidth=6)
# hood fold + pocket
d.path("M330,560 C350,585 390,585 410,560", "Hood fold", fill=NONE,
       stroke="#2E2448", strokeWidth=7, cap="round", opacity=70)
d.path("M330,655 L410,655 L400,690 L340,690 Z", "Pocket",
       fill="#3A2E58", stroke=INK, strokeWidth=4, join="round", opacity=85)
# arm reaching out with the photo
d.path("M475,610 C495,585 500,560 495,540", "Arm R", fill=NONE,
       stroke="#4A3A6E", strokeWidth=18, cap="round")
d.path("M265,615 C245,635 242,660 252,678", "Arm L", fill=NONE,
       stroke="#4A3A6E", strokeWidth=18, cap="round")
# head: clapperboard
d.path("M295,440 L295,545 L455,545 L455,440 Z", "Board",
       fill=CLAPPER, stroke=INK, strokeWidth=6, join="round")
# striped clap top
d.path("M295,440 L295,403 L455,403 L455,440", "Clap bar", fill="#2A2D36",
       stroke=INK, strokeWidth=5)
for i in range(5):
    x0 = 298 + i*32
    d.path(f"M{x0},439 L{x0+22},405 L{x0+38},405 L{x0+16},439 Z",
           f"Clap stripe {i+1}", fill="#E8E4DC", stroke=NONE, opacity=90)
# face on the board: calm, pleased
d.path("M325,487 C332,495 343,495 350,487", "Eye L", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
d.path("M400,487 C407,495 418,495 425,487", "Eye R", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
d.path("M350,517 C365,527 385,527 400,517", "Smirk", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
# "TAKE ∞" scribble on board corner
d.text("TAKE ∞", "Take label", x=308, y=535, size=12, font="Virelai Sans",
       color="#8A94A8", justify="left")

# --- captions ------------------------------------------------------------------
d.text("DEEPFAKE DAVE", "Name", x=500, y=930, size=56, font="Virelai Sans",
       color="#CFE8E4", justify="center")
r = d.text("EVIDENCE-DENIABILITY AMPLIFIER", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#8FB8B2", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("445.deepfake-dave-V1R00")
