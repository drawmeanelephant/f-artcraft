#!/usr/bin/env python3
"""OG Kushkeeper — mascot portrait V1R00.
A pine-cloaked sentinel pressing the compliance stamp onto a patient
record, mist pooling around the lectern. 1000x1000.
Gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("OG Kushkeeper — Mascot Portrait", 1000, 1000)

INK = "#241E14"
BG_GRAD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000], "stops": [
    {"offset": 0, "color": "#0B120C"}, {"offset": 1, "color": "#040804"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#3E5E44"}, {"offset": 0.7, "color": "#243A2A"},
    {"offset": 1, "color": "#121E16"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "start": [0, 700], "end": [0, 880], "stops": [
    {"offset": 0, "color": "#223324"}, {"offset": 1, "color": "#0D140E"}]}}
ROBE = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#5E8A62"}, {"offset": 0.6, "color": "#3E5E42"},
    {"offset": 1, "color": "#223626"}]}}
HOOD = {"gradient": {"kind": "linear", "start": [0, 270], "end": [0, 430], "stops": [
    {"offset": 0, "color": "#4E7A54"}, {"offset": 1, "color": "#263A2C"}]}}
DESK = {"gradient": {"kind": "linear", "start": [0, 590], "end": [0, 700], "stops": [
    {"offset": 0, "color": "#5E4A32"}, {"offset": 1, "color": "#33261A"}]}}
PAPER = {"gradient": {"kind": "linear", "start": [0, 560], "end": [0, 640], "stops": [
    {"offset": 0, "color": "#EFE6CE"}, {"offset": 1, "color": "#C9BC9A"}]}}
STAMP = {"gradient": {"kind": "linear", "start": [0, 470], "end": [0, 570], "stops": [
    {"offset": 0, "color": "#8A5E3A"}, {"offset": 1, "color": "#4E3018"}]}}
SEAL = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#D8845E"}, {"offset": 1, "color": "#9A4A30"}]}}
PINE = {"gradient": {"kind": "linear", "start": [0, 400], "end": [0, 700], "stops": [
    {"offset": 0, "color": "#3A5E3E"}, {"offset": 1, "color": "#1C3020"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#6E8A62", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#CFE0C2", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(193,233,8),(801,230,7),(157,524,9),(837,544,8),
                               (247,766,7),(753,749,9),(133,393,6),(864,391,7),
                               (391,113,7),(613,110,8),(333,823,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#33503A", opacity=45, stroke=NONE)

# --- floor: bottom segment closed on the disc's own arc -----------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#081006",
       strokeWidth=4, opacity=70)

# --- pine boughs framing the plate sides -----------------------------------------
def bough(anchor_x, anchor_y, sign, label):
    d.path(f"M{anchor_x},{anchor_y+160} C{anchor_x+20*sign},{anchor_y+80} "
           f"{anchor_x+30*sign},{anchor_y+30} {anchor_x+18*sign},{anchor_y}",
           f"{label} stem", fill=NONE, stroke="#2A4430", strokeWidth=7,
           cap="round")
    for j in range(6):
        t = j / 5.0
        bx = anchor_x + (18 - 12*t) * sign
        by = anchor_y + 152 - 140 * t
        ln = 34 - j * 3
        for s2 in (-1, 1):
            d.path(f"M{bx:.0f},{by:.0f} C{bx+ln*0.6*s2:.0f},{by-8:.0f} "
                   f"{bx+ln*s2:.0f},{by-14:.0f} {bx+ln*1.25*s2:.0f},{by-18:.0f}",
                   f"{label} needle {j+1}{'L' if s2 < 0 else 'R'}",
                   fill=NONE, stroke=PINE, strokeWidth=4, cap="round",
                   opacity=85)

bough(238, 560, 1, "Bough L")
bough(762, 560, -1, "Bough R")

# --- the sentinel --------------------------------------------------------------------
# robe: wide shoulders tapering to a hem behind the desk
d.path("M500,330 C566,330 610,372 618,448 C624,520 610,600 596,648 "
       "L404,648 C390,600 376,520 382,448 C390,372 434,330 500,330 Z",
       "Robe", fill=ROBE, stroke=INK, strokeWidth=6, join="round")
# robe hem shadow + centre fold
d.path("M404,648 C450,632 550,632 596,648 L596,660 L404,660 Z",
       "Robe hem", fill="#1A2A1E", stroke=NONE, opacity=60)
d.path("M500,470 L500,640", "Centre fold", fill=NONE, stroke="#1E3022",
       strokeWidth=4, opacity=55)
# cloak clasp
d.shape("ellipse", "Clasp", x=485, y=462, width=30, height=30, fill="#C9A24E",
        stroke=INK, strokeWidth=4)
d.shape("ellipse", "Clasp glint", x=491, y=468, width=8, height=8,
        fill="#FFF2C8", opacity=80, stroke=NONE)
# hood: deep cowl over the face
d.path("M500,268 C556,268 592,312 590,368 C586,414 552,438 500,438 "
       "C448,438 414,414 410,368 C408,312 444,268 500,268 Z",
       "Hood", fill=HOOD, stroke=INK, strokeWidth=6, join="round")
# hood peak
d.path("M452,300 C470,268 530,268 548,300 C530,286 470,286 452,300 Z",
       "Hood peak", fill="#5E8A62", stroke=INK, strokeWidth=3, join="round")
# face shadow pool under the cowl
d.shape("ellipse", "Face shadow", x=442, y=352, width=116, height=76,
        fill="#101A12", opacity=80, stroke=NONE)
# two steady amber eyes in the shadow
d.shape("ellipse", "Eye L", x=468, y=378, width=16, height=12, fill="#E8B45E",
        stroke=NONE)
d.shape("ellipse", "Eye R", x=516, y=378, width=16, height=12, fill="#E8B45E",
        stroke=NONE)
d.shape("ellipse", "Eye glint L", x=472, y=380, width=4, height=4,
        fill="#FFF6D8", opacity=90, stroke=NONE)
d.shape("ellipse", "Eye glint R", x=520, y=380, width=4, height=4,
        fill="#FFF6D8", opacity=90, stroke=NONE)

# --- the lectern desk in front of the sentinel ------------------------------------------
d.shape("ellipse", "Desk shadow", x=330, y=672, width=340, height=30,
        fill="#060A05", opacity=50, stroke=NONE)
d.path("M330,596 L670,596 L650,700 L350,700 Z", "Lectern", fill=DESK,
       stroke=INK, strokeWidth=6, join="round")
d.path("M330,596 L670,596 L662,622 L338,622 Z", "Desk lip", fill="#6E583E",
       stroke=INK, strokeWidth=4, join="round", opacity=95)
# stacked record folders waiting their stamp, on the desk top
d.path("M352,540 L438,540 L438,596 L352,596 Z", "Folder stack", fill="#8A744E",
       stroke=INK, strokeWidth=4, join="round")
for j, y in enumerate([548, 560, 572]):
    d.path(f"M358,{y} L430,{y}", f"Stack line {j+1}", fill=NONE,
           stroke="#5E4A30", strokeWidth=2, opacity=70)
# the record sheet on the desk top, mid-stamp
d.path("M455,540 L585,540 L590,596 L450,596 Z", "Record sheet", fill=PAPER,
       stroke=INK, strokeWidth=4, join="round")
for j, y in enumerate([552, 564]):
    d.path(f"M462,{y} L540,{y}", f"Sheet rule {j+1}", fill=NONE,
           stroke="#8A7A58", strokeWidth=2, opacity=70)
# fresh compliance seal stamped on the sheet
d.shape("ellipse", "Seal ring", x=540, y=550, width=34, height=30,
        fill=NONE, stroke=SEAL, strokeWidth=4)
d.path("M548,564 L555,571 L568,556", "Seal check", fill=NONE, stroke=SEAL,
       strokeWidth=4, cap="round", join="round")

# --- arms + the stamp coming down onto the sheet ----------------------------------------
# sleeves reaching to the stamp handle
d.path("M428,470 C455,495 470,510 482,518", "Sleeve L", fill=NONE,
       stroke=ROBE, strokeWidth=24, cap="round")
d.path("M572,470 C545,495 530,510 518,518", "Sleeve R", fill=NONE,
       stroke=ROBE, strokeWidth=24, cap="round")
# stamp: wooden handle + base pressed on the sheet
d.shape("ellipse", "Stamp knob", x=482, y=466, width=36, height=26,
        fill=STAMP, stroke=INK, strokeWidth=4)
d.shape("rectangle", "Stamp neck", x=490, y=488, width=20, height=34,
        fill=STAMP, stroke=INK, strokeWidth=4, radius=4)
d.shape("rectangle", "Stamp base", x=468, y=520, width=64, height=24,
        fill="#3A2A18", stroke=INK, strokeWidth=4, radius=4)
# hands gripping the neck
d.shape("ellipse", "Hand L", x=468, y=498, width=26, height=22,
        fill="#6E8A62", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Hand R", x=506, y=498, width=26, height=22,
        fill="#6E8A62", stroke=INK, strokeWidth=3)
# motion ticks: the stamp just landed
d.path("M446,528 L430,520 M554,528 L570,520 M500,452 L500,436", "Stamp ticks",
       fill=NONE, stroke="#E8D8A8", strokeWidth=4, cap="round", opacity=70)

# --- pine mist pooling around the lectern ------------------------------------------------
d.path("M330,668 C400,646 470,672 540,656 C610,640 660,664 690,650",
       "Mist band", fill=NONE, stroke="#9AB89A", strokeWidth=16,
       opacity=18, cap="round")
d.path("M292,700 C360,682 430,706 500,690 C570,674 640,696 712,682",
       "Mist band low", fill=NONE, stroke="#9AB89A", strokeWidth=20,
       opacity=15, cap="round")
for i, (x, y, w) in enumerate([(368,640,10),(640,636,8),(452,668,7),(560,666,9)]):
    d.shape("ellipse", f"Mist puff {i+1}", x=x, y=y, width=w*3, height=w*1.6,
            fill="#AECBAE", opacity=12, stroke=NONE)
# faint motes in the lamp-green air
for i, (x, y, w, o) in enumerate([(300,220,4,45),(700,240,5,50),(240,380,4,40),
                                  (760,400,4,45),(420,170,4,40),(590,160,5,45)]):
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#D8E8C8", opacity=o, stroke=NONE)

# --- captions ------------------------------------------------------------------
d.text("OG KUSHKEEPER", "Name", x=500, y=934, size=56, font="Virelai Sans",
       color="#D6E4C6", justify="center")
r = d.text("SENTINEL OF PATIENT COMPLIANCE", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#9AB48E", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("208.og-kushkeeper-V1R00")
