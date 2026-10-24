#!/usr/bin/env python3
"""RoboShirker — mascot portrait V1R00.
Boxy robot whose casing presents as productive: routing LEDs lit,
status panel reading ALREADY ON IT, progress bar parked near done —
while the right flank of the torso ghosts one layer sideways into
managed elsewhere. 1000x1000.
Gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("RoboShirker — Mascot Portrait", 1000, 1000)

INK = "#1E222C"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#0E1218"}, {"offset": 1, "color": "#06080C"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4E5E74"}, {"offset": 0.7, "color": "#384558"},
    {"offset": 1, "color": "#1E2632"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2C3442"}, {"offset": 1, "color": "#161C26"}]}}
SHELL_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#A8B4C4"}, {"offset": 0.6, "color": "#78869C"},
    {"offset": 1, "color": "#525E74"}]}}
FACE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2A3444"}, {"offset": 1, "color": "#161D28"}]}}
PANEL_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#242E3E"}, {"offset": 1, "color": "#141B26"}]}}
GREEN = "#7FD08A"
AMBER = "#E8B86A"
DIM = "#5E6E82"
CYAN = "#7AC8D8"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#6E7E96", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C4D0E0", strokeWidth=3, opacity=35)
for i, (x, y, w) in enumerate([(190,240,8),(802,234,7),(152,522,9),(842,540,8),
                               (254,768,7),(748,754,9),(130,392,6),(864,398,7),
                               (390,110,7),(618,112,8),(338,822,6),(664,824,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#3A4658", opacity=50, stroke=NONE)

# --- floor ----------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0E141C",
       strokeWidth=4, opacity=70)

# --- acknowledged task queue, piling up left ---------------------------------------
d.shape("ellipse", "Queue shadow", x=200, y=676, width=190, height=18,
        fill="#0A0E14", opacity=50, stroke=NONE)
for i, (qx, qy, qrot) in enumerate([(250, 622, -5), (236, 588, 4), (262, 556, -8)]):
    d.path(rot_rect_path(qx, qy, 92, 60, qrot), f"Ticket {i+1}",
           fill="#D8D2C0", stroke=INK, strokeWidth=3, join="round")
    d.path(rot_rect_path(qx-14, qy-8, 52, 4, qrot), f"Ticket {i+1} rule",
           fill="#9A947E", stroke=NONE)
    # every one stamped ACK'D, none executed
    d.path(rot_rect_path(qx+8, qy+12, 56, 20, qrot), f"Ticket {i+1} stamp",
           fill=NONE, stroke="#A04A3E", strokeWidth=2.5, join="round",
           opacity=80)
    d.text("ACK'D", f"Ticket {i+1} stamp txt", x=qx+8, y=qy+19, size=10,
           font="Virelai Sans", color="#A04A3E", justify="center")

# --- RoboShirker --------------------------------------------------------------------
d.shape("ellipse", "Bot shadow", x=400, y=676, width=260, height=24,
        fill="#0A0E14", opacity=55, stroke=NONE)

# ghost flank FIRST, so the shell draws over its left edge:
# the torso itself, echoed sideways into managed elsewhere
d.path("M468,404 L628,404 L654,650 C654,664 642,672 628,672 L468,672 "
       "C454,672 442,664 442,650 Z", "Ghost echo 1",
       fill=SHELL_GRAD, stroke=NONE, opacity=20)
d.path("M516,404 L676,404 L702,650 C702,664 690,672 676,672 L516,672 "
       "C502,672 490,664 490,650 Z", "Ghost echo 2",
       fill=SHELL_GRAD, stroke=NONE, opacity=9)
for i, (gx, gy, gs) in enumerate([(740,480,16),(764,520,12),(752,580,10),
                                  (782,552,8),(768,470,6),(742,632,9)]):
    d.path(rot_rect_path(gx, gy, gs, gs, 8), f"Drift px {i+1}",
           fill="#8A9AB0", stroke=NONE, opacity=18)

# antenna: the little light that suggests active routing
d.path("M500,262 L500,224", "Antenna stem", fill=NONE, stroke=INK,
       strokeWidth=6, cap="round")
d.shape("ellipse", "Antenna glow", x=484, y=196, width=32, height=32,
        fill=GREEN, opacity=20, stroke=NONE)
d.shape("ellipse", "Antenna tip", x=491, y=203, width=18, height=18,
        fill=GREEN, stroke=INK, strokeWidth=3)

# head: rounded slab, ear bolts each side
d.shape("rectangle", "Ear bolt L", x=356, y=310, width=22, height=46,
        fill="#5E6A80", stroke=INK, strokeWidth=4, radius=6)
d.shape("rectangle", "Ear bolt R", x=622, y=310, width=22, height=46,
        fill="#5E6A80", stroke=INK, strokeWidth=4, radius=6)
d.shape("rectangle", "Head", x=378, y=238, width=244, height=140,
        fill=SHELL_GRAD, stroke=INK, strokeWidth=6, radius=20)
d.shape("ellipse", "Head hi", x=398, y=250, width=90, height=30,
        fill="#FFFFFF", opacity=16, stroke=NONE)
# face visor: warm, calm, slightly over-attentive
d.shape("rectangle", "Visor", x=400, y=262, width=200, height=92,
        fill=FACE_GRAD, stroke=INK, strokeWidth=4, radius=14)
for side, ex in [("L", 442), ("R", 530)]:
    d.shape("ellipse", f"Eye {side}", x=ex, y=292, width=24, height=28,
            fill=CYAN, stroke=NONE, opacity=95)
    d.shape("ellipse", f"Glint {side}", x=ex+5, y=296, width=7, height=7,
            fill="#FFFFFF", opacity=90, stroke=NONE)
d.path("M478,332 C488,340 512,340 522,332", "Smile", fill=NONE,
       stroke=CYAN, strokeWidth=4, cap="round", opacity=90)
# visor scanline — reassurance rendered nightly
d.path("M404,300 L596,300", "Scanline", fill=NONE, stroke="#9AD8E8",
       strokeWidth=1.5, opacity=15)

# neck
d.shape("rectangle", "Neck", x=478, y=378, width=44, height=26,
        fill="#5E6A80", stroke=INK, strokeWidth=4, radius=4)

# torso: tapered casing
d.path("M420,404 L580,404 L606,650 C606,664 594,672 580,672 L420,672 "
       "C406,672 394,664 394,650 Z",
       "Torso", fill=SHELL_GRAD, stroke=INK, strokeWidth=6, join="round")
d.shape("ellipse", "Torso hi", x=420, y=424, width=80, height=60,
        fill="#FFFFFF", opacity=12, stroke=NONE)
# torso seam where the ghosting begins — a faint dashed tear line
d.path("M586,420 C596,480 600,560 596,650", "Tear line", fill=NONE,
       stroke="#C4D0E0", strokeWidth=2, dash=[5, 8], opacity=35)

# stub arms; the right one fades with its flank
d.path("M398,440 C370,470 362,520 372,560", "Arm L ink", fill=NONE,
       stroke=INK, strokeWidth=30, cap="round")
d.path("M398,440 C370,470 362,520 372,560", "Arm L", fill=NONE,
       stroke=SHELL_GRAD, strokeWidth=21, cap="round")
d.path("M602,440 C634,466 644,514 634,556", "Arm R", fill=NONE,
       stroke="#78869C", strokeWidth=21, cap="round", opacity=55)
# a placid clamp hand on the left
d.path("M362,556 C354,576 366,592 384,590 C398,588 402,572 394,562 "
       "C388,554 372,550 362,556 Z", "Hand L", fill="#5E6A80",
       stroke=INK, strokeWidth=4, join="round")

# --- chest status panel: warm, calm, slightly over-attentive -------------------------
d.shape("rectangle", "Status panel", x=428, y=448, width=152, height=96,
        fill=PANEL_GRAD, stroke=INK, strokeWidth=4, radius=10)
# routing LEDs: all happily lit, none attached to work
for i, (lx, c) in enumerate([(448, GREEN), (470, GREEN), (492, AMBER), (514, DIM)]):
    d.shape("ellipse", f"LED glow {i+1}", x=lx-4, y=456, width=16, height=16,
            fill=c, opacity=20, stroke=NONE)
    d.shape("ellipse", f"LED {i+1}", x=lx, y=460, width=8, height=8,
            fill=c, stroke=NONE, opacity=90 if c != DIM else 45)
d.text("ROUTING", "LED label", x=534, y=469, size=9,
       font="Virelai Sans", color=DIM, justify="left")
# the status line itself
d.text("ALREADY ON IT", "Status", x=504, y=504, size=14,
       font="Virelai Sans", color="#CFE8D4", justify="center")
# progress bar parked at nearly-done since march
d.shape("rectangle", "Prog track", x=442, y=518, width=124, height=10,
        fill="#0E141E", stroke="#3A4658", strokeWidth=2, radius=5)
d.shape("rectangle", "Prog fill", x=444, y=520, width=108, height=6,
        fill=GREEN, stroke=NONE, radius=3, opacity=85)
# and below the panel: the honest part
r = d.text("EXECUTION: ELSEWHERE", "Truth", x=504, y=566, size=9,
           font="Virelai Sans", color=DIM, justify="center")
if r and r.get("id"):
    d.cmd("object.setProps", "truth fade", ids=[r["id"]], opacity=75)

# --- captions ----------------------------------------------------------------------
d.text("ROBOSHIRKER", "Name", x=500, y=930, size=58,
       font="Virelai Sans", color="#E4EAF2", justify="center")
r = d.text("DEFERRED EXECUTION WITNESS", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#9AAAC0", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("056.roboshirker-V1R00")
