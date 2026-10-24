#!/usr/bin/env python3
"""Courier Rat — mascot portrait V1R00.
Interdepartmental courier mid-scurry through the ductwork toward
grate-light: official delivery sash across the chest, satchel full of
misrouted memos, Form 88-R riding shotgun, tail negotiating the bend.
Duct 7B-Delta. 1000x1000. Gradients + translucent shading, never flat."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Courier Rat — Mascot Portrait", 1000, 1000)

INK = "#241C1E"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#121418"}, {"offset": 1, "color": "#08090C"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4A5460"}, {"offset": 0.7, "color": "#323A46"},
    {"offset": 1, "color": "#1A1F28"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2C3138"}, {"offset": 1, "color": "#14171C"}]}}
FUR_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#C4B49E"}, {"offset": 0.7, "color": "#94826E"},
    {"offset": 1, "color": "#62544A"}]}}
GRATE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4E5A66"}, {"offset": 1, "color": "#2C343E"}]}}
BAG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#8A6444"}, {"offset": 1, "color": "#5C4028"}]}}
SASH = "#C04858"
PINK = "#D8A0A0"
GOLD = "#E8C878"
PAPER = "#EDE4CC"
STEEL = "#7E8A96"
LIGHT = "#F0E4B4"

def rot_pt(cx, cy, x, y, deg):
    a = math.radians(deg); c, s = math.cos(a), math.sin(a)
    return (cx + (x - cx) * c - (y - cy) * s,
            cy + (x - cx) * s + (y - cy) * c)

# --- backdrop + plate -----------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#7E8A96", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C0CAD4", strokeWidth=3, opacity=40)

# --- ductwork: seams + rivets on the plate, all ending well inside the arc --------
d.path("M168,640 L832,640", "Duct seam", fill=NONE, stroke="#4A525C",
       strokeWidth=3, opacity=55)
for i in range(12):
    d.shape("ellipse", f"Rivet {i+1}", x=196 + i * 56, y=634,
            width=9, height=9, fill="#5A646E", opacity=70, stroke=NONE)
d.path("M186,300 L186,392 M812,286 L812,380", "Duct seams v", fill=NONE,
       stroke="#4A525C", strokeWidth=3, opacity=50)
for i, (x, y) in enumerate([(186, 310), (186, 344), (186, 378),
                            (812, 296), (812, 330), (812, 364)]):
    d.shape("ellipse", f"Rivet v{i+1}", x=x - 4, y=y - 4, width=8, height=8,
            fill="#5A646E", opacity=70, stroke=NONE)

# --- the grate: where the light gets in ----------------------------------------------
for i, (x1, y1, x2, y2, op) in enumerate([
        (196, 196, 580, 560, 12), (250, 150, 690, 510, 9),
        (152, 214, 470, 540, 10)]):
    d.path(f"M{x1},{y1} L{x2},{y2} L{x2+46},{y2-60} L{x1+40},{y1-52} Z",
           f"Light beam {i+1}", fill=LIGHT, opacity=op, stroke=NONE)
d.path(rot_rect_path(232, 168, 196, 96, -8), "Grate frame",
       fill=GRATE_GRAD, stroke=INK, strokeWidth=5, join="round")
for i in range(4):
    sx, sy = rot_pt(232, 168, 232, 136 + i * 20, -8)
    d.path(rot_rect_path(sx, sy, 176, 9, -8), f"Grate slat {i+1}",
           fill="#1A2028", stroke=NONE)
for i, (lx, ly) in enumerate([(148, 138), (316, 120), (160, 196), (328, 178)]):
    d.shape("ellipse", f"Grate bolt {i+1}", x=lx, y=ly, width=10, height=10,
            fill="#6E7A86", stroke=INK, strokeWidth=2)
# dust in the beam
for i, (x, y, s) in enumerate([(340, 330, 5), (420, 420, 4), (300, 380, 4),
                               (500, 470, 5), (380, 300, 3), (560, 520, 4)]):
    d.shape("ellipse", f"Dust {i+1}", x=x, y=y, width=s, height=s,
            fill=LIGHT, opacity=45, stroke=NONE)

# --- duct address stencil --------------------------------------------------------------
d.shape("rectangle", "Duct sign", x=668, y=128, width=190, height=52,
        fill="#2C343E", stroke=STEEL, strokeWidth=3, radius=6, opacity=95)
t = d.text("DUCT 7B-DELTA", "Duct label", x=763, y=162, size=17,
           font="Source Sans 3", color="#C8D2DA", justify="center")
if t and t.get("id"):
    d.cmd("text.setStyle", "duct tracking", ids=[t["id"]], tracking=80)
for i, (lx, ly) in enumerate([(676, 136), (848, 136), (676, 172), (848, 172)]):
    d.shape("ellipse", f"Sign rivet {i+1}", x=lx, y=ly, width=6, height=6,
            fill=STEEL, stroke=NONE)

# --- floor ----------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0E1014",
       strokeWidth=4, opacity=70)

# --- shredded memos adrift ---------------------------------------------------------------
for i, (cx, cy, w, h, deg) in enumerate([(330, 500, 56, 40, -14),
                                         (700, 470, 48, 34, 10),
                                         (624, 386, 44, 30, -6)]):
    d.path(rot_rect_path(cx, cy, w, h, deg), f"Memo {i+1}",
           fill=PAPER, stroke="#8A7A5A", strokeWidth=2, opacity=85,
           join="round")
    for j in range(2):
        ly = cy - 6 + j * 12
        p1 = rot_pt(cx, cy, cx - w / 2 + 8, ly, deg)
        p2 = rot_pt(cx, cy, cx + w / 2 - 8, ly, deg)
        d.path(f"M{p1[0]:.0f},{p1[1]:.0f} L{p2[0]:.0f},{p2[1]:.0f}",
               f"Memo {i+1} line {j+1}", fill=NONE, stroke="#9A8A68",
               strokeWidth=2.5, cap="round", opacity=70)

# --- Courier Rat: custody authority in motion ------------------------------------------
d.shape("ellipse", "Rat shadow", x=400, y=686, width=270, height=24,
        fill="#06080A", opacity=55, stroke=NONE)
# tail: negotiating the bend, curling along the floor behind
d.path("M626,672 C712,700 792,690 810,644 C822,610 796,588 768,602",
       "Tail", fill=NONE, stroke=PINK, strokeWidth=14, cap="round",
       opacity=95)
d.path("M626,672 C712,700 792,690 810,644 C822,610 796,588 768,602",
       "Tail shade", fill=NONE, stroke="#A87878", strokeWidth=5,
       cap="round", opacity=60)
# ears first (behind head): big, thin, listening
d.shape("ellipse", "Ear L", x=426, y=398, width=76, height=82,
        fill=FUR_GRAD, stroke=INK, strokeWidth=5)
d.shape("ellipse", "Ear L inner", x=438, y=412, width=52, height=56,
        fill=PINK, opacity=70, stroke=NONE)
d.shape("ellipse", "Ear R", x=558, y=390, width=82, height=88,
        fill=FUR_GRAD, stroke=INK, strokeWidth=5)
d.shape("ellipse", "Ear R inner", x=572, y=404, width=56, height=62,
        fill=PINK, opacity=70, stroke=NONE)
# body leaning into the scurry
d.path("M500,452 C576,452 622,512 622,584 C622,658 572,700 500,700 "
       "C428,700 378,658 378,584 C378,512 424,452 500,452 Z",
       "Rat body", fill=FUR_GRAD, stroke=INK, strokeWidth=6)
# snout: the professional's profile, pointed left toward the light
d.path("M420,500 C380,516 348,544 336,574 C356,596 402,602 438,590 "
       "C452,566 448,524 420,500 Z", "Snout", fill=FUR_GRAD,
       stroke=INK, strokeWidth=5, join="round")
d.shape("ellipse", "Nose", x=326, y=562, width=24, height=20,
        fill=PINK, stroke=INK, strokeWidth=3)
# whiskers doing the navigating
d.path("M348,552 L288,534 M346,570 L284,570 M350,586 L292,604",
       "Whiskers L", fill=NONE, stroke=INK, strokeWidth=2.5,
       cap="round", opacity=75)
d.path("M452,566 L416,556 M454,584 L420,586", "Whiskers R",
       fill=NONE, stroke=INK, strokeWidth=2.5, cap="round", opacity=60)
# eyes: alert, both on the route ahead
d.shape("ellipse", "Eye L", x=416, y=512, width=28, height=32,
        fill="#2A2020", stroke=NONE)
d.shape("ellipse", "Eye R", x=508, y=504, width=30, height=34,
        fill="#2A2020", stroke=NONE)
d.shape("ellipse", "Glint L", x=418, y=518, width=9, height=9,
        fill=LIGHT, opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=510, y=510, width=9, height=9,
        fill=LIGHT, opacity=90, stroke=NONE)
d.path("M530,486 C542,480 556,480 566,488", "Brow R", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round", opacity=80)
d.path("M448,548 C462,556 478,556 488,546", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round", opacity=80)
# the official delivery sash: shoulder to hip, gold-piped
d.path("M544,470 C500,530 452,584 412,650", "Sash edge A", fill=NONE,
       stroke=INK, strokeWidth=42, cap="round")
d.path("M544,470 C500,530 452,584 412,650", "Sash", fill=NONE,
       stroke=SASH, strokeWidth=32, cap="round")
t = d.text("COURIER", "Sash text", x=470, y=592, size=11,
           font="Virelai Sans", color="#F8E4C8", justify="center")
if t and t.get("id"):
    d.cmd("object.rotate", "sash tilt", ids=[t["id"]], angle=56,
          origin=[470, 588])
# the satchel: custody authority hangs at the hip
d.path(rot_rect_path(636, 612, 118, 96, 6), "Satchel",
       fill=BAG_GRAD, stroke=INK, strokeWidth=5, join="round")
d.path(rot_rect_path(636, 584, 118, 30, 6), "Satchel flap",
       fill="#74522F", stroke=INK, strokeWidth=4, join="round")
d.shape("ellipse", "Satchel clasp", x=630, y=586, width=16, height=14,
        fill=GOLD, stroke=INK, strokeWidth=2)
d.path("M560,540 C600,560 640,572 690,578", "Satchel strap",
       fill=NONE, stroke="#6E4E30", strokeWidth=10, cap="round")
# mail poking out: two letters and the sacred form
for i, (cx, cy, w, h, deg) in enumerate([(616, 536, 54, 40, -10),
                                         (664, 528, 48, 36, 8)]):
    d.path(rot_rect_path(cx, cy, w, h, deg), f"Mail {i+1}",
           fill=PAPER, stroke="#8A7A5A", strokeWidth=2.5, join="round")
    v1 = rot_pt(cx, cy, cx - w / 2, cy - h / 2, deg)
    v2 = rot_pt(cx, cy, cx, cy - 4, deg)
    v3 = rot_pt(cx, cy, cx + w / 2, cy - h / 2, deg)
    d.path(f"M{v1[0]:.0f},{v1[1]:.0f} L{v2[0]:.0f},{v2[1]:.0f} "
           f"L{v3[0]:.0f},{v3[1]:.0f}", f"Mail {i+1} flap",
           fill=NONE, stroke="#8A7A5A", strokeWidth=2, cap="round")
d.path(rot_rect_path(590, 520, 66, 46, -18), "Form card",
       fill="#E8D8B0", stroke=INK, strokeWidth=3, join="round")
t = d.text("88-R", "Form number", x=590, y=528, size=15,
           font="Source Sans 3", color="#8A3828", justify="center")
if t and t.get("id"):
    d.cmd("object.rotate", "form tilt", ids=[t["id"]], angle=18,
          origin=[590, 524])
# front paw extended mid-scurry
d.path("M430,640 C402,656 384,672 376,690", "Paw arm ink", fill=NONE,
       stroke=INK, strokeWidth=30, cap="round")
d.path("M430,640 C402,656 384,672 376,690", "Paw arm", fill=NONE,
       stroke="#94826E", strokeWidth=20, cap="round")
d.shape("ellipse", "Paw", x=356, y=676, width=34, height=22,
        fill=PINK, stroke=INK, strokeWidth=3)
# rear foot braced
d.shape("ellipse", "Foot R", x=560, y=686, width=52, height=20,
        fill=PINK, stroke=INK, strokeWidth=3)

# --- captions ----------------------------------------------------------------------
d.text("COURIER RAT", "Name", x=500, y=930, size=58,
       font="Virelai Sans", color="#E8ECF0", justify="center")
r = d.text("INTERDEPARTMENTAL COURIER", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#AAB4C0", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("060.courier-rat-V1R00")
