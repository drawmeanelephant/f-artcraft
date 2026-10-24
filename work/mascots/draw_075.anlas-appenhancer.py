#!/usr/bin/env python3
"""Anlas the Application Enhancer — mascot portrait V1R00.
An earnest bronze gear-icon daemon seated in an open LaunchAgents folder
among the plist files he whispers to, annotated crash logs stacked
nearby — helpful, obsolete, and still faintly proud of every patch.
1000x1000. Gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Anlas the Application Enhancer — Mascot Portrait", 1000, 1000)

INK = "#241E22"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#11151C"}, {"offset": 1, "color": "#07090E"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#5E6E80"}, {"offset": 0.7, "color": "#3C4856"},
    {"offset": 1, "color": "#1E2733"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2C3540"}, {"offset": 1, "color": "#12161D"}]}}
FOLDER_BACK = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6E94C2"}, {"offset": 1, "color": "#43648E"}]}}
FOLDER_FRONT = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5C82B0"}, {"offset": 1, "color": "#33507A"}]}}
GEAR_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E8BC62"}, {"offset": 0.7, "color": "#C09040"},
    {"offset": 1, "color": "#8A5E28"}]}}
HUB_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F2D490"}, {"offset": 1, "color": "#C89848"}]}}
DOC_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F2EDE0"}, {"offset": 1, "color": "#CFC6AE"}]}}
LOG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E8E4D8"}, {"offset": 1, "color": "#BDB6A0"}]}}
RED = "#B84840"
LIGHT = "#F0E4B4"

def rot_pt(cx, cy, x, y, deg):
    a = math.radians(deg); c, s = math.cos(a), math.sin(a)
    return (cx + (x - cx) * c - (y - cy) * s,
            cy + (x - cx) * s + (y - cy) * c)

# --- backdrop + plate -----------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#8898AA", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C4D0DC", strokeWidth=3, opacity=40)
for i, (x, y, w) in enumerate([(194,240,8),(800,232,7),(158,526,9),(838,544,8),
                               (248,766,7),(754,750,9),(134,394,6),(864,390,7),
                               (392,112,7),(612,110,8),(334,822,6),(666,822,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#46525F", opacity=45, stroke=NONE)

# --- floor ----------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0C0E13",
       strokeWidth=4, opacity=70)

# spectral drift: a second ghostly LaunchAgent tab still haunting the corner
d.path(rot_rect_path(738, 192, 104, 34, 6), "Ghost plist",
       fill="#8A98A8", stroke=NONE, join="round", opacity=18)
d.path("M704,188 L768,188 M704,196 L752,196", "Ghost lines", fill=NONE,
       stroke="#C4D0DC", strokeWidth=2.5, cap="round", opacity=20)

# --- the LaunchAgents folder ------------------------------------------------------
d.shape("ellipse", "Folder shadow", x=255, y=676, width=500, height=30,
        fill="#06080B", opacity=55, stroke=NONE)
# back panel with the named tab
d.path("M286,428 L286,398 Q286,384 300,384 L392,384 Q406,384 410,396 "
       "L418,414 L714,414 Q728,414 728,428 L728,664 L286,664 Z",
       "Folder back", fill=FOLDER_BACK, stroke=INK, strokeWidth=6,
       join="round")

# plist residents peeking out of the back of the folder
for i, (cx, cy, w, h, deg) in enumerate([
        (316, 452, 96, 128, -12), (676, 446, 96, 128, 10),
        (604, 420, 92, 124, 3)]):
    d.path(rot_rect_path(cx, cy, w, h, deg), f"Plist {i+1}",
           fill=DOC_GRAD, stroke=INK, strokeWidth=4, join="round")
    # folded corner
    a = rot_pt(cx, cy, cx + w/2 - 22, cy - h/2, deg)
    b = rot_pt(cx, cy, cx + w/2, cy - h/2 + 22, deg)
    c = rot_pt(cx, cy, cx + w/2, cy - h/2, deg)
    d.path(f"M{a[0]:.0f},{a[1]:.0f} L{c[0]:.0f},{c[1]:.0f} "
           f"L{b[0]:.0f},{b[1]:.0f} Z", f"Plist {i+1} fold",
           fill="#B8AE94", stroke=INK, strokeWidth=2.5, join="round")
    # xml-ish line strokes
    for j in range(4):
        ly = cy - h/2 + 30 + j * 16
        lw = w - 30 - (j % 2) * 18
        a = rot_pt(cx, cy, cx - w/2 + 12, ly, deg)
        b = rot_pt(cx, cy, cx - w/2 + 12 + lw, ly, deg)
        d.path(f"M{a[0]:.0f},{a[1]:.0f} L{b[0]:.0f},{b[1]:.0f}",
               f"Plist {i+1} line {j+1}", fill=NONE, stroke="#9A8F76",
               strokeWidth=3, cap="round", opacity=75)

# --- Anlas: the gear himself, seated -----------------------------------------------
GCX, GCY = 500, 442
# teeth first: nine honest teeth
for i in range(9):
    a = math.radians(i * 40 - 90)
    tx, ty = GCX + 106 * math.cos(a), GCY + 106 * math.sin(a)
    d.path(rot_rect_path(tx, ty, 34, 30, math.degrees(a) + 90),
           f"Tooth {i+1}", fill=GEAR_GRAD, stroke=INK, strokeWidth=4,
           join="round")
# gear body
d.shape("ellipse", "Gear body", x=GCX-100, y=GCY-100, width=200, height=200,
        fill=GEAR_GRAD, stroke=INK, strokeWidth=6)
# hub: his face plate
d.shape("ellipse", "Hub", x=GCX-58, y=GCY-58, width=116, height=116,
        fill=HUB_GRAD, stroke=INK, strokeWidth=5)
d.shape("ellipse", "Hub ring", x=GCX-44, y=GCY-44, width=88, height=88,
        fill=NONE, stroke="#8A5E28", strokeWidth=3, opacity=60)
# earnest eyes, one brow hoisted in eternal optimism
d.shape("ellipse", "Eye L", x=GCX-38, y=GCY-28, width=26, height=32,
        fill="#2A2020", stroke=NONE)
d.shape("ellipse", "Eye R", x=GCX+12, y=GCY-28, width=26, height=32,
        fill="#2A2020", stroke=NONE)
d.shape("ellipse", "Glint L", x=GCX-32, y=GCY-22, width=9, height=9,
        fill="#FFFFFF", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=GCX+18, y=GCY-22, width=9, height=9,
        fill="#FFFFFF", opacity=90, stroke=NONE)
d.path(f"M{GCX-42},{GCY-42} C{GCX-32},{GCY-48} {GCX-22},{GCY-48} {GCX-14},{GCY-44}",
       "Brow L", fill=NONE, stroke=INK, strokeWidth=4, cap="round")
d.path(f"M{GCX+12},{GCY-50} C{GCX+22},{GCY-56} {GCX+34},{GCY-56} {GCX+44},{GCY-50}",
       "Brow R hopeful", fill=NONE, stroke=INK, strokeWidth=4, cap="round")
# the smile of someone about to "enhance" your Finder
d.path(f"M{GCX-26},{GCY+14} C{GCX-10},{GCY+30} {GCX+16},{GCY+30} {GCX+30},{GCY+12}",
       "Eager smile", fill=NONE, stroke=INK, strokeWidth=5, cap="round")
d.path(f"M{GCX+30},{GCY+12} L{GCX+34},{GCY+8}", "Smile corner", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
# a guilty little sweat drop for Leopard
d.path(f"M{GCX+78},{GCY-70} C{GCX+88},{GCY-56} {GCX+88},{GCY-44} {GCX+78},{GCY-44} "
       f"C{GCX+68},{GCY-44} {GCX+68},{GCY-56} {GCX+78},{GCY-70} Z",
       "Sweat drop", fill="#AAD4E8", stroke=INK, strokeWidth=2.5,
       join="round", opacity=85)

# whisper curl toward the nearest plist — he is always whispering
d.path(f"M{GCX+72},{GCY+26} C{GCX+116},{GCY+10} {GCX+140},{GCY-10} {GCX+150},{GCY-38}",
       "Whisper curl", fill=NONE, stroke="#C8BEDE", strokeWidth=3,
       cap="round", dash=[4, 8], opacity=70)
for i, (x, y) in enumerate([(GCX+128, GCY-16), (GCX+144, GCY-30)]):
    d.shape("ellipse", f"Whisper dot {i+1}", x=x, y=y, width=5, height=5,
            fill="#C8BEDE", opacity=60, stroke=NONE)

# folder front panel: he sits inside it
d.path("M268,520 L732,520 L756,664 L244,664 Z", "Folder front",
       fill=FOLDER_FRONT, stroke=INK, strokeWidth=6, join="round")
d.path("M268,520 L732,520", "Folder lip", fill=NONE, stroke="#16202C",
       strokeWidth=4, opacity=70)
# sheen on the front panel
d.path("M300,548 L520,548 L500,620 L310,620 Z", "Front sheen",
       fill="#FFFFFF", opacity=8, stroke=NONE)
t = d.text("LAUNCHAGENTS", "Folder label", x=500, y=602, size=20,
           font="Virelai Sans", color="#D8E4F0", justify="center")
if t and t.get("id"):
    d.cmd("text.setStyle", "label tracking", ids=[t["id"]], tracking=150)

# stubby arms over the lip: left rests, right waves a tiny wrench
d.path("M402,510 C386,536 378,556 380,574", "Arm L ink", fill=NONE,
       stroke=INK, strokeWidth=26, cap="round")
d.path("M402,510 C386,536 378,556 380,574", "Arm L", fill=NONE,
       stroke="#C09040", strokeWidth=16, cap="round")
d.shape("ellipse", "Hand L", x=368, y=564, width=26, height=22,
        fill=HUB_GRAD, stroke=INK, strokeWidth=3.5)
d.path("M598,510 C618,540 626,562 622,584", "Arm R ink", fill=NONE,
       stroke=INK, strokeWidth=26, cap="round")
d.path("M598,510 C618,540 626,562 622,584", "Arm R", fill=NONE,
       stroke="#C09040", strokeWidth=16, cap="round")
d.shape("ellipse", "Hand R", x=610, y=574, width=26, height=22,
        fill=HUB_GRAD, stroke=INK, strokeWidth=3.5)
# the little wrench of runtime enhancement
d.path("M624,560 L654,598", "Wrench shaft", fill=NONE, stroke="#9AA6B4",
       strokeWidth=9, cap="round")
d.path("M648,592 A17,17 0 1 1 664,584", "Wrench jaw", fill=NONE,
       stroke="#9AA6B4", strokeWidth=7, cap="round")

# dangling feet over the lip
for side, fx in (("L", 452), ("R", 532)):
    d.path(f"M{fx},640 C{fx-4},660 {fx-6},672 {fx-8},684", f"Leg {side}",
           fill=NONE, stroke=INK, strokeWidth=22, cap="round")
    d.path(f"M{fx},640 C{fx-4},660 {fx-6},672 {fx-8},684", f"Leg {side} fill",
           fill=NONE, stroke="#C09040", strokeWidth=13, cap="round")
    d.shape("ellipse", f"Foot {side}", x=fx-30, y=676, width=36, height=20,
            fill=HUB_GRAD, stroke=INK, strokeWidth=3.5)

# --- annotated crash logs, stacked nearby --------------------------------------------
for i, (cx, cy, w, h, deg) in enumerate([
        (252, 660, 150, 104, -7), (266, 652, 150, 104, -2),
        (244, 646, 150, 104, 4)]):
    d.path(rot_rect_path(cx, cy, w, h, deg), f"Crash log {i+1}",
           fill=LOG_GRAD, stroke=INK, strokeWidth=3.5, join="round")
# top sheet gets the treatment: header + log lines + red annotations
for j in range(4):
    ly = 616 + j * 16
    a = rot_pt(244, 646, 186, ly, 4); b = rot_pt(244, 646, 304 - (j % 2) * 22, ly, 4)
    d.path(f"M{a[0]:.0f},{a[1]:.0f} L{b[0]:.0f},{b[1]:.0f}",
           f"Log line {j+1}", fill=NONE, stroke="#6E6656", strokeWidth=3,
           cap="round", opacity=80)
# he underlined the frame that was definitely him
a = rot_pt(244, 646, 186, 648, 4); b = rot_pt(244, 646, 282, 648, 4)
d.path(f"M{a[0]:.0f},{a[1]:.0f} L{b[0]:.0f},{b[1]:.0f}", "Red underline",
       fill=NONE, stroke=RED, strokeWidth=3.5, cap="round")
ca = rot_pt(244, 646, 236, 664, 4)
d.shape("ellipse", "Red circle", x=ca[0]-52, y=ca[1]-14, width=104,
        height=28, fill=NONE, stroke=RED, strokeWidth=3, opacity=85)
t = d.text("me.", "Log note", x=ca[0]+62, y=ca[1]+8, size=10,
           font="Virelai Sans", color=RED, justify="left")
if t and t.get("id"):
    d.cmd("object.rotate", "note tilt", ids=[t["id"]], angle=4,
          origin=[ca[0]+62, ca[1]+8])

# helpful sparkles — he did try
for i, (cx, cy, s) in enumerate([(346, 300, 16), (668, 316, 13), (392, 210, 11)]):
    d.path(f"M{cx},{cy-s} L{cx+4},{cy-4} L{cx+s},{cy} L{cx+4},{cy+4} "
           f"L{cx},{cy+s} L{cx-4},{cy+4} L{cx-s},{cy} L{cx-4},{cy-4} Z",
           f"Sparkle {i+1}", fill=LIGHT, stroke=NONE, opacity=55)

# --- captions ----------------------------------------------------------------------
d.text("ANLAS THE APPLICATION ENHANCER", "Name", x=500, y=930, size=48,
       font="Virelai Sans", color="#E4EAF0", justify="center")
r = d.text("SIP CRASHLOG WHISPERER", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#9AAABE", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("075.anlas-appenhancer-V1R00")
