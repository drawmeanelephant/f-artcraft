#!/usr/bin/env python3
"""Ami Ghostbyte — mascot portrait V1R00.
A translucent ghost hovering over a failed floppy handoff, Guru Meditation
red-box alert burning on the CRT, broken joystick abandoned on the floor.
1000x1000. Gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Ami Ghostbyte — Mascot Portrait", 1000, 1000)

INK = "#221A26"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#0C0F1A"}, {"offset": 1, "color": "#05060C"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#5A6190"}, {"offset": 0.7, "color": "#3C4266"},
    {"offset": 1, "color": "#222842"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2A2F46"}, {"offset": 1, "color": "#141828"}]}}
CASE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#CFC7B4"}, {"offset": 1, "color": "#948C78"}]}}
SCREEN_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#14141E"}, {"offset": 1, "color": "#08080C"}]}}
GHOST_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#DCF4F2"}, {"offset": 0.7, "color": "#A8DCDC"},
    {"offset": 1, "color": "#6AAFB6"}]}}
JOY_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3E4450"}, {"offset": 1, "color": "#22262E"}]}}
RED = "#C03232"
DISK = "#2E3450"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#767EA6", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C6D4DE", strokeWidth=3, opacity=40)
for i, (x, y, w) in enumerate([(190,240,8),(800,230,7),(150,520,9),(846,540,8),
                               (255,768,7),(745,756,9),(130,392,6),(866,398,7),
                               (390,112,7),(618,110,8),(336,822,6),(662,824,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#4A5078", opacity=50, stroke=NONE)

# --- floor: bottom segment closed on the disc's own arc -----------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#10121E",
       strokeWidth=4, opacity=70)

# --- the CRT monitor: Guru Meditation up on screen ------------------------------
d.shape("ellipse", "Monitor shadow", x=555, y=688, width=290, height=24,
        fill="#08080E", opacity=55, stroke=NONE)
d.shape("rectangle", "Monitor foot", x=688, y=628, width=36, height=52,
        fill="#8C8472", stroke=INK, strokeWidth=5)
d.path("M636,676 L776,676 L794,702 L618,702 Z", "Monitor base",
       fill=CASE_GRAD, stroke=INK, strokeWidth=5, join="round")
d.shape("rectangle", "Monitor body", x=545, y=288, width=290, height=330,
        fill=CASE_GRAD, stroke=INK, strokeWidth=7, radius=16)
# case vents
for i, vx in enumerate([566, 578, 590, 602]):
    d.path(f"M{vx},306 L{vx},330", f"Vent {i+1}", fill=NONE,
           stroke="#7E7662", strokeWidth=4, cap="round")
# screen
d.shape("rectangle", "Screen", x=580, y=348, width=220, height=240,
        fill=SCREEN_GRAD, stroke="#171320", strokeWidth=6, radius=10)
# screen glass sheen
d.path("M590,352 L690,352 L610,580 L586,580 Z", "Screen sheen",
       fill="#FFFFFF", opacity=6, stroke=NONE)
# scanlines
for i, sy in enumerate([400, 452, 504, 556]):
    d.path(f"M584,{sy} L796,{sy}", f"Scanline {i+1}", fill=NONE,
           stroke="#FFFFFF", strokeWidth=1.5, opacity=6)
# the alert: red-bordered box, black inside
d.shape("rectangle", "Alert box", x=592, y=362, width=196, height=66,
        fill="#0C0608", stroke=RED, strokeWidth=5, radius=2)
d.text("SOFTWARE FAILURE.", "Alert line 1", x=602, y=384, size=11,
       font="Virelai Sans", color="#F2E6DA", justify="left")
d.text("PRESS LEFT MOUSE BUTTON", "Alert line 2", x=602, y=400, size=9,
       font="Virelai Sans", color="#C8B2A6", justify="left")
d.text("TO CONTINUE.", "Alert line 3", x=602, y=416, size=9,
       font="Virelai Sans", color="#C8B2A6", justify="left")
d.text("GURU MEDITATION", "Guru label", x=602, y=452, size=12,
       font="Virelai Sans", color="#E88", justify="left")
# hex dump: Virelai Sans has no digits — Source Sans 3 carries this line
d.text("#00000003.00C0FFEE", "Guru hex", x=602, y=470, size=11,
       font="Source Sans 3", color="#D8A08E", justify="left")
# dead cursor blinking below the error
d.shape("rectangle", "Cursor", x=604, y=492, width=10, height=16,
        fill="#E8DCC8", opacity=70, stroke=NONE)
# power LED
d.shape("ellipse", "Power LED", x=802, y=596, width=10, height=10,
        fill="#E08A3C", stroke=INK, strokeWidth=2)
d.shape("ellipse", "LED glow", x=796, y=590, width=22, height=22,
        fill="#E08A3C", opacity=20, stroke=NONE)

# --- the floppy drive on the floor, slot agape ---------------------------------
d.shape("ellipse", "Drive shadow", x=382, y=690, width=190, height=20,
        fill="#08080E", opacity=50, stroke=NONE)
d.path("M392,620 L566,620 L578,702 L380,702 Z", "Drive case",
       fill=CASE_GRAD, stroke=INK, strokeWidth=6, join="round")
d.shape("rectangle", "Drive slot", x=404, y=634, width=146, height=16,
        fill="#120F16", stroke=INK, strokeWidth=4, radius=3)
# eject button
d.shape("rectangle", "Eject", x=520, y=664, width=34, height=16,
        fill="#B0A890", stroke=INK, strokeWidth=3, radius=3)
d.shape("ellipse", "Drive LED", x=404, y=666, width=9, height=9,
        fill=RED, stroke=INK, strokeWidth=2)
d.shape("ellipse", "Drive LED glow", x=399, y=661, width=19, height=19,
        fill=RED, opacity=20, stroke=NONE)

# --- the disk that never landed: frozen mid-handoff, sparking -------------------
d.path("M470,540 L540,528 L548,588 L478,600 Z", "Floppy",
       fill=DISK, stroke=INK, strokeWidth=5, join="round")
d.shape("rectangle", "Floppy shutter", x=486, y=536, width=40, height=20,
        fill="#8A92A8", stroke=INK, strokeWidth=3, radius=2)
d.shape("rectangle", "Floppy label", x=482, y=566, width=52, height=26,
        fill="#C9C2AE", stroke=INK, strokeWidth=3)
d.path("M488,574 L524,570 M488,582 L516,578", "Label lines", fill=NONE,
       stroke="#8E846E", strokeWidth=2, opacity=80)
# where it should have been: fading echo at the slot mouth
d.path("M462,608 L532,596 L540,656 L470,668 Z", "Floppy echo",
       fill=DISK, stroke=NONE, opacity=18)
# static around the stalled disk
d.path("M448,556 L462,564 L452,574 L466,582", "Static 1", fill=NONE,
       stroke="#8FE8E4", strokeWidth=4, cap="round", join="round")
d.path("M556,540 L570,548 L560,560", "Static 2", fill=NONE,
       stroke="#8FE8E4", strokeWidth=4, cap="round", join="round")
for i, (x, y, s) in enumerate([(442,592,7),(560,596,6),(452,528,5),
                               (552,512,6),(566,570,5)]):
    d.shape("rectangle", f"Pixel spark {i+1}", x=x, y=y, width=s, height=s,
            fill="#9FE8E4", opacity=70, stroke=NONE)
# the handoff that failed: dashed guide between hand and slot
d.path("M420,540 C450,530 480,540 500,560", "Handoff arc", fill=NONE,
       stroke="#8FE8E4", strokeWidth=3, dash=[3, 10], cap="round",
       opacity=50)

# --- the broken joystick, nearby and ignored ------------------------------------
d.shape("ellipse", "Joystick shadow", x=622, y=688, width=140, height=18,
        fill="#08080E", opacity=50, stroke=NONE)
d.path("M640,660 L736,660 L754,700 L622,700 Z", "Joystick base",
       fill=JOY_GRAD, stroke=INK, strokeWidth=5, join="round")
d.shape("ellipse", "Joy button", x=652, y=668, width=22, height=14,
        fill=RED, stroke=INK, strokeWidth=3)
# stick snapped: lower stub tilted, top half lying loose beside it
d.path("M700,660 L692,606", "Stick stub", fill=NONE, stroke="#2A2E38",
       strokeWidth=14, cap="round")
d.path("M690,610 L684,596 M696,608 L692,592", "Snap splinters", fill=NONE,
       stroke="#14161C", strokeWidth=3, cap="round")
d.path("M742,690 L706,700", "Stick top", fill=NONE, stroke="#2A2E38",
       strokeWidth=13, cap="round")
d.shape("ellipse", "Stick ball", x=738, y=676, width=20, height=20,
        fill=RED, stroke=INK, strokeWidth=3)
# cable trailing off toward the machine, dead
d.path("M736,676 C780,664 800,672 830,660", "Joy cable", fill=NONE,
       stroke="#2A2E38", strokeWidth=4, cap="round", opacity=80)

# --- Ami Ghostbyte: flicker echoes first (behind), then the ghost ----------------
ECHO = "M300,392 C362,392 402,448 402,530 C402,576 388,604 402,644 " \
       "C386,634 372,648 360,640 C344,628 336,652 316,642 " \
       "C298,634 288,650 272,640 C256,630 242,644 232,632 " \
       "C214,612 198,576 198,530 C198,448 238,392 300,392 Z"
d.path("M308,392 C370,392 410,448 410,530 C410,576 396,604 410,644 "
       "C394,634 380,648 368,640 C352,628 344,652 324,642 "
       "C306,634 296,650 280,640 C264,630 250,644 240,632 "
       "C222,612 206,576 206,530 C206,448 246,392 308,392 Z",
       "Echo R", fill="#E88AA0", opacity=14, stroke=NONE)
d.path("M292,392 C354,392 394,448 394,530 C394,576 380,604 396,644 "
       "C380,634 366,648 354,640 C338,628 330,652 310,642 "
       "C292,634 282,650 266,640 C250,630 236,644 226,632 "
       "C208,612 192,576 192,530 C192,448 232,392 292,392 Z",
       "Echo C", fill="#8FE8E4", opacity=16, stroke=NONE)
# the ghost herself: blob body dissolving into a wavy tail
d.path(ECHO, "Ami body", fill=GHOST_GRAD, stroke="#3C4C58",
       strokeWidth=6, opacity=62, join="round")
d.shape("ellipse", "Body hi", x=230, y=420, width=80, height=50,
        fill="#FFFFFF", opacity=20, stroke=NONE)
# scanline flicker across the body
for i, sy in enumerate([440, 488, 536, 584]):
    d.shape("rectangle", f"Flicker {i+1}", x=200, y=sy, width=200,
            height=6, fill="#FFFFFF", opacity=10, stroke=NONE)
# pixelated dissolution off the tail and shoulder
for i, (x, y, s) in enumerate([(392,640,10),(412,616,8),(376,664,7),
                               (400,586,6),(186,560,7),(204,600,5),
                               (416,470,7),(196,470,6)]):
    d.shape("rectangle", f"Dissolve {i+1}", x=x, y=y, width=s, height=s,
            fill="#A8DCDC", opacity=45, stroke=NONE)
# hollow eyes, worried upward — she knows the handoff failed
d.path("M252,478 C252,462 264,452 276,452 C288,452 298,462 298,478 "
       "C298,492 288,500 276,500 C264,500 252,492 252,478 Z",
       "Eye L", fill="#262033", opacity=85, stroke=NONE)
d.path("M322,478 C322,462 334,452 346,452 C358,452 368,462 368,478 "
       "C368,492 358,500 346,500 C334,500 322,492 322,478 Z",
       "Eye R", fill="#262033", opacity=85, stroke=NONE)
d.shape("ellipse", "Eye glint L", x=266, y=462, width=8, height=8,
        fill="#FFFFFF", opacity=70, stroke=NONE)
d.shape("ellipse", "Eye glint R", x=336, y=462, width=8, height=8,
        fill="#FFFFFF", opacity=70, stroke=NONE)
# small open wail of a mouth
d.path("M296,524 C296,514 304,508 310,508 C316,508 324,514 324,524 "
       "C324,534 316,540 310,540 C304,540 296,534 296,524 Z",
       "Mouth", fill="#262033", opacity=80, stroke=NONE)
# reaching arm toward the stalled disk
d.path("M392,516 C412,516 426,524 436,536", "Arm reach", fill=NONE,
       stroke="#9ED6D8", strokeWidth=16, cap="round", opacity=75)
d.shape("ellipse", "Hand", x=426, y=528, width=24, height=20,
        fill="#B8E4E2", opacity=75, stroke="#3C4C58", strokeWidth=3)

# --- captions ---------------------------------------------------------------------
d.text("AMI GHOSTBYTE", "Name", x=500, y=930, size=58,
       font="Virelai Sans", color="#DAEDEE", justify="center")
r = d.text("GHOST OF THE BOOT LOOP", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#9DB9C4", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("025.ami-ghostbyte-V1R00")
