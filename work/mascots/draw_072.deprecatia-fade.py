#!/usr/bin/env python3
"""Deprecatia Fade — mascot portrait V1R00.
A half-faded documentation ghost beside a stubbornly unstyled sidebar:
greyed-out buttons nobody can press, a TODO note curling off the panel,
and her beloved list of functions, most of them struck through.
1000x1000. Gradients + translucent shading, never flat."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Deprecatia Fade — Mascot Portrait", 1000, 1000)

INK = "#221E1C"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#181A1C"}, {"offset": 1, "color": "#0B0C0E"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#5C5A62"}, {"offset": 0.7, "color": "#3C3A42"},
    {"offset": 1, "color": "#1E1D24"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#333136"}, {"offset": 1, "color": "#141316"}]}}
GHOST_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#B4AEC6"}, {"offset": 0.6, "color": "#8E88A4"},
    {"offset": 1, "color": "#5E5A76"}]}}
PANEL_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#DAD6CC"}, {"offset": 1, "color": "#B8B4AA"}]}}
BTN = "#C6C2B8"
BTN_TXT = "#8A867C"
PAPER = "#E8E2CC"
FADE = "#8E88A4"

# --- backdrop + plate ----------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#7A7880", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C2C0CA", strokeWidth=3, opacity=30)
d.shape("ellipse", "Patina 1", x=560, y=170, width=230, height=150,
        fill="#6E6C78", opacity=18, stroke=NONE)
d.shape("ellipse", "Patina 2", x=170, y=560, width=240, height=140,
        fill="#6E6C78", opacity=16, stroke=NONE)

# --- the unstyled sidebar: default-grey, out of place, unbothered -----------------
d.shape("rectangle", "Sidebar", x=190, y=196, width=220, height=456,
        fill=PANEL_GRAD, stroke="#8A867E", strokeWidth=4, radius=4,
        opacity=97)
# hairline header + a title nobody styled
d.path("M190,258 L410,258", "Sidebar divider", fill=NONE,
       stroke="#9A968C", strokeWidth=2.5, opacity=80)
d.shape("rectangle", "Sidebar titlebar", x=204, y=212, width=120,
        height=18, fill="#B0ACA2", stroke=NONE, radius=3, opacity=90)
d.shape("ellipse", "Sidebar dot", x=382, y=216, width=12, height=12,
        fill="#9A968C", stroke=NONE)
# greyed-out buttons down the panel
for i, label in enumerate(["Save", "Apply", "Delete"]):
    by = 282 + i * 74
    d.shape("rectangle", f"Btn {label}", x=214, y=by, width=172,
            height=52, fill=BTN, stroke="#A29E94", strokeWidth=2.5,
            radius=4, opacity=90)
    d.text(label, f"Btn label {label}", x=300, y=by + 34, size=19,
           font="Source Sans 3", color=BTN_TXT, justify="center")
# a disabled link row
d.path("M218,530 L382,530", "Dead link", fill=NONE, stroke=BTN_TXT,
       strokeWidth=3, opacity=55, dash=[5, 4])
# the TODO note that will outlive us all, curling off the sidebar
d.path(rot_rect_path(314, 552, 96, 66, 14), "TODO note",
       fill="#E4D89A", stroke="#A89A5E", strokeWidth=2.5, join="round")
t = d.text("TODO:", "Todo text", x=314, y=558, size=15,
           font="Source Sans 3", color="#6E6438", justify="center")
if t and t.get("id"):
    d.cmd("object.rotate", "todo tilt", ids=[t["id"]], angle=14,
          origin=[314, 552])
t = d.text("clean up later", "Todo sub", x=314, y=576, size=10,
           font="Source Sans 3", color="#8A8050", justify="center")
if t and t.get("id"):
    d.cmd("object.rotate", "todo2 tilt", ids=[t["id"]], angle=14,
          origin=[314, 570])

# --- floor ----------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0C0B0E",
       strokeWidth=4, opacity=70)

# --- Deprecatia: the fade herself ---------------------------------------------------
d.shape("ellipse", "Fade shadow", x=470, y=682, width=240, height=22,
        fill="#060608", opacity=40, stroke=NONE)
# shroud body, deliberately translucent — she is leaving
d.path("M580,400 C648,400 686,452 692,528 C696,586 704,640 716,678 "
       "C688,690 676,672 664,690 C650,708 636,678 618,694 "
       "C600,710 586,680 570,692 C552,706 540,678 524,688 "
       "C500,702 486,676 470,686 C456,694 448,690 444,680 "
       "C456,640 464,586 468,528 C474,452 512,400 580,400 Z",
       "Shroud", fill=GHOST_GRAD, stroke=INK, strokeWidth=5,
       join="round", opacity=82)
# tattered hem is the path's own edge; deepen the fade below it
d.path("M462,660 C540,682 650,680 706,664", "Hem fade", fill=NONE,
       stroke=FADE, strokeWidth=10, cap="round", opacity=35)
# hood
d.path("M580,352 C636,352 670,394 670,446 C670,482 644,504 580,504 "
       "C516,504 490,482 490,446 C490,394 524,352 580,352 Z",
       "Hood", fill=GHOST_GRAD, stroke=INK, strokeWidth=5, opacity=88)
d.shape("ellipse", "Face dusk", x=520, y=398, width=120, height=86,
        fill="#3A3648", opacity=90, stroke=NONE)
# tired eyes — nothing here is angry, only unmaintained
d.shape("ellipse", "Eye L", x=540, y=428, width=18, height=22,
        fill="#CFC8DE", opacity=90, stroke=NONE)
d.shape("ellipse", "Eye R", x=602, y=428, width=18, height=22,
        fill="#CFC8DE", opacity=90, stroke=NONE)
d.path("M534,420 C544,412 556,412 562,418", "Brow L", fill=NONE,
       stroke="#5A5470", strokeWidth=3.5, cap="round", opacity=80)
d.path("M598,418 C606,412 618,412 626,420", "Brow R", fill=NONE,
       stroke="#5A5470", strokeWidth=3.5, cap="round", opacity=80)
d.path("M566,466 C574,472 588,472 596,466", "Gentle frown", fill=NONE,
       stroke="#8A84A0", strokeWidth=3.5, cap="round", opacity=85)

# --- the list of functions she loved --------------------------------------------------
d.path("M508,540 C470,560 452,590 448,624", "Arm L ink", fill=NONE,
       stroke=INK, strokeWidth=26, cap="round", opacity=85)
d.path("M508,540 C470,560 452,590 448,624", "Arm L", fill=NONE,
       stroke="#8E88A4", strokeWidth=17, cap="round", opacity=90)
d.shape("ellipse", "Hand L", x=430, y=610, width=30, height=25,
        fill="#B4AEC6", stroke=INK, strokeWidth=3, opacity=90)
# curled list, top edge rolled
d.path("M370,560 C400,540 470,538 500,556 L494,690 C466,706 404,706 378,690 Z",
       "Fn list", fill=PAPER, stroke="#8A8060", strokeWidth=3,
       join="round", opacity=96)
d.path("M370,560 C400,576 470,574 500,556", "List curl", fill=NONE,
       stroke="#B0A884", strokeWidth=3, opacity=80)
# function entries: some gone, some going
for i, (txt, gone) in enumerate([("init()", True), ("render()", True),
                                 ("onload()", False), ("main()", False)]):
    ly = 594 + i * 26
    d.text(txt, f"fn {txt}", x=436, y=ly, size=14, font="Source Sans 3",
           color="#6E6850" if not gone else "#A09A80", justify="center")
    if gone:
        d.path(f"M394,{ly-5} L478,{ly-5}", f"strike {txt}", fill=NONE,
               stroke="#9A9478", strokeWidth=2.5, cap="round", opacity=85)
# small footnote mark at the list's foot
d.text("legacy", "List footnote", x=436, y=700, size=10,
       font="Source Sans 3", color="#9A9478", justify="center")

# right hand rests on the sidebar's edge — she is not done with it
d.path("M648,540 C614,566 596,600 590,632", "Arm R ink", fill=NONE,
       stroke=INK, strokeWidth=26, cap="round", opacity=85)
d.path("M648,540 C614,566 596,600 590,632", "Arm R", fill=NONE,
       stroke="#8E88A4", strokeWidth=17, cap="round", opacity=90)
d.shape("ellipse", "Hand R", x=574, y=620, width=30, height=25,
        fill="#B4AEC6", stroke=INK, strokeWidth=3, opacity=90)

# motes of her, already elsewhere
for i, (x, y, s) in enumerate([(700, 560, 5), (724, 600, 4), (712, 640, 4),
                               (688, 680, 5), (736, 540, 3)]):
    d.shape("ellipse", f"Fade mote {i+1}", x=x, y=y, width=s, height=s,
            fill=FADE, opacity=50, stroke=NONE)

# --- captions ----------------------------------------------------------------------
d.text("DEPRECATIA FADE", "Name", x=500, y=930, size=58,
       font="Virelai Sans", color="#E0DEE4", justify="center")
r = d.text("KEEPER OF DEPRECATED PATHS", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#AAA8B4", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("072.deprecatia-fade-V1R00")
