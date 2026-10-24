#!/usr/bin/env python3
"""Pamphlet Quietus — mascot portrait V1R00.
A soft clerk of informational closure offering a tri-fold pamphlet —
three bullet points and a stock photo of a calm lake — beside a stack
already laminated before the incident. 1000x1000.
Gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Pamphlet Quietus — Mascot Portrait", 1000, 1000)

INK = "#2E2A1E"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#101512"}, {"offset": 1, "color": "#070A08"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4A5A48"}, {"offset": 0.7, "color": "#2A3628"},
    {"offset": 1, "color": "#121A12"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2A3226"}, {"offset": 1, "color": "#10160E"}]}}
BODY = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#ECE8D2"}, {"offset": 0.7, "color": "#CBC5A2"},
    {"offset": 1, "color": "#9E9674"}]}}
PAGE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F4EFDC"}, {"offset": 1, "color": "#DCD2B0"}]}}
SKY = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#C8DEE8"}, {"offset": 1, "color": "#8FB4C6"}]}}
LAKE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7FA8BA"}, {"offset": 1, "color": "#4E7484"}]}}
STAND = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5A664E"}, {"offset": 1, "color": "#2E3626"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#8FA88A", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8E4D0", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(193,233,8),(801,230,7),(157,524,9),(837,544,8),
                               (247,766,7),(753,749,9),(133,393,6),(864,391,7),
                               (391,113,7),(613,110,8),(333,823,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#42523E", opacity=45, stroke=NONE)

# --- floor --------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0C1208",
       strokeWidth=4, opacity=70)

# --- TAKE ONE placard on the wall ------------------------------------------------
d.path(rot_rect_path(268, 218, 152, 58, -4), "Placard", fill="#E4DCBE",
       stroke=INK, strokeWidth=4, join="round")
d.text("TAKE ONE", "Placard text", x=208, y=230, size=22,
       font="Virelai Sans", color="#4A442E", justify="left")
d.path("M288,248 L312,258", "Placard pin", fill=NONE, stroke=INK,
       strokeWidth=3, cap="round", opacity=60)

# --- a pamphlet already distributed — on the floor, unread --------------------------
d.path(rot_rect_path(312, 668, 96, 40, 12), "Dropped pamphlet",
       fill=PAGE, stroke=INK, strokeWidth=3, join="round", opacity=85)
d.path(rot_rect_path(312, 668, 4, 40, 12), "Dropped fold", fill="#B8AA86",
       stroke=NONE, opacity=70)

# --- the mascot: a soft clerk of printed closure --------------------------------------
d.shape("ellipse", "Body shadow", x=390, y=668, width=270, height=30,
        fill="#0A0E06", opacity=50, stroke=NONE)
# body — calm pear shape, hands full of answers
d.path("M520,300 C600,300 648,360 650,440 C652,520 640,600 620,668 "
       "L424,668 C404,600 392,520 394,440 C396,360 444,300 520,300 Z",
       "Body", fill=BODY, stroke=INK, strokeWidth=6)
d.shape("ellipse", "Body sheen", x=440, y=320, width=110, height=50,
        fill="#FFFFFF", opacity=20, stroke=NONE)
# a sash of authority: the lanyard of someone who means well
d.path("M452,330 C480,390 500,440 512,500", "Lanyard", fill=NONE,
       stroke="#7A8C66", strokeWidth=8, cap="round", opacity=80)
d.shape("rectangle", "Badge", x=502, y=496, width=34, height=26,
        fill="#E4DCBE", stroke=INK, strokeWidth=3, radius=3)
d.path("M508,506 L530,506 M508,514 L524,514", "Badge lines", fill=NONE,
       stroke="#8E8264", strokeWidth=2, cap="round", opacity=70)

# face: professionally serene
d.path("M452,398 C460,407 474,407 482,398", "Eye L", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
d.path("M556,398 C564,407 578,407 586,398", "Eye R", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
d.path("M490,438 C503,449 537,449 550,438", "Smile", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
d.shape("ellipse", "Blush L", x=436, y=414, width=30, height=14,
        fill="#B08A62", opacity=40, stroke=NONE)
d.shape("ellipse", "Blush R", x=574, y=414, width=30, height=14,
        fill="#B08A62", opacity=40, stroke=NONE)

# --- right arm: presenting the stack on the stand -------------------------------------
d.path("M648,520 C682,540 692,580 676,612", "Arm R", fill=NONE,
       stroke=INK, strokeWidth=14, cap="round")
d.shape("ellipse", "Hand R", x=658, y=600, width=30, height=24,
        fill=BODY, stroke=INK, strokeWidth=4)

# --- distribution stand with the laminated stack ---------------------------------------
d.shape("rectangle", "Stand top", x=676, y=590, width=150, height=18,
        fill=STAND, stroke=INK, strokeWidth=5, radius=4)
d.path("M706,608 L698,700 M796,608 L804,700", "Stand legs", fill=NONE,
       stroke=INK, strokeWidth=8, cap="round")
# the stack: five tri-folds, creased into thirds, waiting
for i in range(5):
    y = 586 - i*13
    d.shape("rectangle", f"Stack fold {i+1}", x=692, y=y, width=118,
            height=13, fill=PAGE, stroke=INK, strokeWidth=2.5, radius=2)
    d.path(f"M732,{y} L732,{y+13} M770,{y} L770,{y+13}", f"Creases {i+1}",
           fill=NONE, stroke="#A89A78", strokeWidth=1.5, opacity=70)

# --- left arm: offering the open tri-fold toward the viewer -----------------------------
d.path("M394,470 C350,470 322,490 312,520", "Arm L", fill=NONE,
       stroke=INK, strokeWidth=14, cap="round")

# --- the tri-fold itself, held open and readable ---------------------------------------
# three panels fanned toward the viewer; left panel angled back
d.path("M150,392 L252,370 L252,562 L150,584 Z", "Panel L", fill=PAGE,
       stroke=INK, strokeWidth=5, join="round")
d.path("M252,370 L354,386 L354,570 L252,562 Z", "Panel M",
       fill="#F8F2DE", stroke=INK, strokeWidth=5, join="round")
d.path("M354,386 L442,398 L442,574 L354,570 Z", "Panel R", fill=PAGE,
       stroke=INK, strokeWidth=5, join="round")
# crease shadows
d.path("M252,370 L252,562", "Crease 1", fill=NONE, stroke="#A89A78",
       strokeWidth=2.5, opacity=70)
d.path("M354,386 L354,570", "Crease 2", fill=NONE, stroke="#A89A78",
       strokeWidth=2.5, opacity=70)

# Panel L: the three bullet points — the entire resolution
d.text("YOUR", "Bullet head a", x=160, y=422, size=13,
       font="Virelai Sans", color="#5E5438", justify="left")
d.text("INCIDENT", "Bullet head b", x=160, y=440, size=13,
       font="Virelai Sans", color="#5E5438", justify="left")
for i in range(3):
    y = 462 + i*36
    d.shape("ellipse", f"Bullet {i+1}", x=164, y=y, width=9, height=9,
            fill="#8FA88A", stroke=INK, strokeWidth=1.5)
    d.path(f"M182,{y+5} L236,{y+2}", f"Bullet line {i+1}a", fill=NONE,
           stroke="#9E9474", strokeWidth=3.5, cap="round", opacity=80)
    d.path(f"M182,{y+17} L222,{y+15}", f"Bullet line {i+1}b", fill=NONE,
           stroke="#B8AC86", strokeWidth=3, cap="round", opacity=70)

# Panel M: the stock photo of a calm lake
d.path("M264,402 L342,412 L342,492 L264,486 Z", "Lake photo", fill=SKY,
       stroke=INK, strokeWidth=3, join="round")
d.path("M264,448 L342,454 L342,492 L264,486 Z", "Lake water", fill=LAKE,
       stroke=NONE)
d.path("M264,448 L342,454", "Horizon", fill=NONE, stroke="#5E7E8E",
       strokeWidth=2, opacity=80)
d.shape("ellipse", "Lake sun", x=288, y=414, width=16, height=16,
        fill="#F0E6C0", opacity=90, stroke=NONE)
d.path("M276,462 L300,463 M288,472 L318,473", "Lake ripples", fill=NONE,
       stroke="#C8DEE8", strokeWidth=2, cap="round", opacity=70)
# digits go to Source Sans 3 — Virelai Sans has no digit glyphs
d.text("fig. 1", "Lake caption", x=270, y=516, size=11,
       font="Source Sans 3", color="#8E8264", justify="left")
d.path("M300,514 L342,516", "Caption rule", fill=NONE, stroke="#B8AC86",
       strokeWidth=2.5, cap="round", opacity=70)
d.path("M268,540 L338,544", "Panel M line", fill=NONE, stroke="#B8AC86",
       strokeWidth=3, cap="round", opacity=60)

# Panel R: the closing panel — reassurance in type
d.text("REMAIN", "Panel R t1", x=364, y=432, size=17,
       font="Virelai Sans", color="#5E5438", justify="left")
d.text("CALM", "Panel R t2", x=364, y=456, size=17,
       font="Virelai Sans", color="#5E5438", justify="left")
for i in range(3):
    y = 482 + i*26
    w = 62 if i < 2 else 40
    d.path(f"M364,{y} L{364+w},{y+2}", f"Panel R line {i+1}", fill=NONE,
           stroke="#B8AC86", strokeWidth=3, cap="round", opacity=70)

# hand gripping the fold's right edge
d.shape("ellipse", "Hand L", x=430, y=540, width=30, height=24,
        fill=BODY, stroke=INK, strokeWidth=4)

# --- captions ----------------------------------------------------------------------
d.text("PAMPHLET QUIETUS", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#E4EAD6", justify="center")
r = d.text("TRI-FOLD RESOLUTION DESK", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#AEC4A4", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("285.pamphlet-quietus-V1R00")
