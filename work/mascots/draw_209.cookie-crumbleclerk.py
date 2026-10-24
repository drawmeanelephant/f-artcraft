#!/usr/bin/env python3
"""Cookie Crumbleclerk — mascot portrait V1R00.
A gingerbread clerk in an eyeshade, crumbling an intake record into sugary
crumbs over an open jar, beside the cookie-jar drawer bank. 1000x1000.
Gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Cookie Crumbleclerk — Mascot Portrait", 1000, 1000)

INK = "#2E2014"
BG_GRAD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000], "stops": [
    {"offset": 0, "color": "#140D08"}, {"offset": 1, "color": "#080504"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#6A4A2E"}, {"offset": 0.7, "color": "#3A281A"},
    {"offset": 1, "color": "#1C120C"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "start": [0, 700], "end": [0, 880], "stops": [
    {"offset": 0, "color": "#33231A"}, {"offset": 1, "color": "#140C07"}]}}
COOKIE = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#D8A05E"}, {"offset": 0.65, "color": "#B07840"},
    {"offset": 1, "color": "#7E5228"}]}}
JAR = {"gradient": {"kind": "linear", "start": [0, 480], "end": [0, 700], "stops": [
    {"offset": 0, "color": "#8A6A48"}, {"offset": 1, "color": "#4A3420"}]}}
GLASS = {"gradient": {"kind": "linear", "start": [0, 500], "end": [0, 690], "stops": [
    {"offset": 0, "color": "#C4C0AE"}, {"offset": 1, "color": "#7E7662"}]}}
PAPER = {"gradient": {"kind": "linear", "start": [0, 380], "end": [0, 480], "stops": [
    {"offset": 0, "color": "#F2E8D2"}, {"offset": 1, "color": "#D2C2A0"}]}}
VISOR = {"gradient": {"kind": "linear", "start": [0, 330], "end": [0, 380], "stops": [
    {"offset": 0, "color": "#4E8A5E"}, {"offset": 1, "color": "#2A5238"}]}}
CABINET = {"gradient": {"kind": "linear", "start": [0, 480], "end": [0, 700], "stops": [
    {"offset": 0, "color": "#6E5238"}, {"offset": 1, "color": "#3E2C1C"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#A87E50", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#EEDCBE", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(193,233,8),(801,230,7),(157,524,9),(837,544,8),
                               (247,766,7),(753,749,9),(133,393,6),(864,391,7),
                               (391,113,7),(613,110,8),(333,823,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#5A3E28", opacity=45, stroke=NONE)

# --- floor: bottom segment closed on the disc's own arc -----------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0E0804",
       strokeWidth=4, opacity=70)

# --- sugar dust motes --------------------------------------------------------------
for i, (x, y, w, o) in enumerate([(250,200,4,55),(330,150,3,45),(680,170,4,55),
                                  (760,280,3,45),(210,340,4,40),(790,430,4,50),
                                  (430,140,3,40),(580,150,4,45)]):
    d.shape("ellipse", f"Sugar mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#F2E2C2", opacity=o, stroke=NONE)

# --- cookie-jar drawer bank, right side ----------------------------------------------
d.shape("ellipse", "Cabinet shadow", x=620, y=678, width=240, height=26,
        fill="#0A0603", opacity=50, stroke=NONE)
d.shape("rectangle", "Cabinet", x=630, y=470, width=215, height=225,
        fill=CABINET, stroke=INK, strokeWidth=6, radius=12)
# crown cornice
d.shape("rectangle", "Cabinet top", x=622, y=458, width=231, height=22,
        fill=CABINET, stroke=INK, strokeWidth=5, radius=8)
# 2x2 jar-drawers: glass front, cookies inside, knob
for r_i, ry in enumerate([490, 585]):
    for c_i, cx in enumerate([645, 752]):
        d.shape("rectangle", f"Drawer {r_i*2+c_i+1}", x=cx, y=ry, width=95,
                height=88, fill=JAR, stroke=INK, strokeWidth=4, radius=10)
        # cookies stacked inside, seen through glass
        for k, (ox, oy) in enumerate([(12, 58), (30, 50), (50, 56), (24, 64)]):
            d.shape("ellipse", f"Cookie {r_i*2+c_i+1}.{k+1}",
                    x=cx+ox, y=ry+oy, width=16, height=10, fill=COOKIE,
                    stroke="#5A3A20", strokeWidth=2)
        # glass sheen
        d.path(f"M{cx+10},{ry+8} L{cx+30},{ry+8} L{cx+16},{ry+74} L{cx+8},{ry+74} Z",
               f"Glass sheen {r_i*2+c_i+1}", fill="#E8F0F2", opacity=14,
               stroke=NONE)
        # label pull
        d.shape("rectangle", f"Label pull {r_i*2+c_i+1}", x=cx+28, y=ry+10,
                width=40, height=16, fill="#D8C49A", stroke=INK,
                strokeWidth=3, radius=4)

# --- the open crumb jar, front-left ---------------------------------------------------
d.shape("ellipse", "Jar shadow", x=215, y=672, width=130, height=22,
        fill="#0A0603", opacity=50, stroke=NONE)
d.path("M235,560 C230,600 228,650 240,685 C268,700 302,700 330,685 "
       "C342,650 340,600 335,560 Z",
       "Crumb jar", fill=GLASS, stroke=INK, strokeWidth=5, join="round",
       opacity=75)
# jar mouth + lid leaning beside it
d.path("M232,560 C255,548 315,548 338,560", "Jar mouth", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
d.shape("ellipse", "Jar lid", x=338, y=648, width=52, height=22,
        fill=JAR, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Lid knob", x=356, y=638, width=16, height=14,
        fill=JAR, stroke=INK, strokeWidth=3)
# crumbs collected at the jar's base
for i, (x, y, w) in enumerate([(255,662,10),(272,668,8),(290,664,11),(308,668,8),
                               (262,650,7),(298,654,7)]):
    d.shape("ellipse", f"Jar crumb {i+1}", x=x, y=y, width=w, height=w*0.7,
            fill=COOKIE, stroke="#5A3A20", strokeWidth=1, opacity=90)
# "INTAKE" tag tied to the jar neck
d.path("M300,562 L342,556 L348,584 L306,590 Z", "Intake tag", fill=PAPER,
       stroke=INK, strokeWidth=3, join="round")
d.text("INTAKE", "Tag text", x=306, y=576, size=11, font="Virelai Sans",
       color="#6E4A28", justify="left")

# --- the clerk -------------------------------------------------------------------------
d.shape("ellipse", "Clerk shadow", x=400, y=672, width=220, height=28,
        fill="#0A0603", opacity=50, stroke=NONE)
# torso: squat cookie body
d.path("M500,430 C570,430 612,478 612,548 C612,610 575,652 500,652 "
       "C425,652 388,610 388,548 C388,478 430,430 500,430 Z",
       "Torso", fill=COOKIE, stroke=INK, strokeWidth=6, join="round")
# icing trim squiggle across the belly
d.path("M412,560 C440,548 460,572 488,560 C516,548 536,572 564,560 "
       "C580,552 592,560 600,566", "Icing squiggle", fill=NONE,
       stroke="#F2E2C2", strokeWidth=6, cap="round", opacity=80)
# chocolate-chip buttons
for i, (x, y) in enumerate([(492, 590), (498, 615), (505, 545)]):
    d.shape("ellipse", f"Chip {i+1}", x=x, y=y, width=14, height=12,
            fill="#4A2E18", stroke=INK, strokeWidth=2)
# head: round cookie on top
d.shape("ellipse", "Head", x=415, y=330, width=170, height=140,
        fill=COOKIE, stroke=INK, strokeWidth=6)
# green eyeshade visor across the brow
d.path("M415,368 C460,350 540,350 585,368 L585,342 C540,324 460,324 415,342 Z",
       "Eyeshade", fill=VISOR, stroke=INK, strokeWidth=4, join="round",
       opacity=92)
d.path("M415,342 L408,338 M585,342 L592,338", "Visor strap", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
# eyes peering under the visor, slightly weary
d.shape("ellipse", "Eye L", x=458, y=392, width=20, height=22, fill="#33241A",
        stroke=NONE)
d.shape("ellipse", "Eye R", x=522, y=392, width=20, height=22, fill="#33241A",
        stroke=NONE)
d.shape("ellipse", "Glint L", x=463, y=396, width=6, height=6, fill="#FFF2DC",
        opacity=85, stroke=NONE)
d.shape("ellipse", "Glint R", x=527, y=396, width=6, height=6, fill="#FFF2DC",
        opacity=85, stroke=NONE)
# flat little clerk mouth
d.path("M482,434 L518,434", "Mouth", fill=NONE, stroke=INK, strokeWidth=5,
       cap="round")
# faint icing brow crumbs on the cheek
d.shape("ellipse", "Cheek crumb 1", x=440, y=430, width=8, height=6,
        fill="#7E5228", opacity=60, stroke=NONE)
d.shape("ellipse", "Cheek crumb 2", x=552, y=428, width=7, height=6,
        fill="#7E5228", opacity=60, stroke=NONE)

# --- arms crumbling a record sheet over the jar ------------------------------------------
# the half-crumpled intake sheet between the hands
d.path("M420,520 L382,498 L360,530 L372,556 L404,548 L414,560 L428,544 Z",
       "Crumpled sheet", fill=PAPER, stroke=INK, strokeWidth=4, join="round")
d.path("M382,514 L398,508 M386,530 L404,522 M390,542 L406,536",
       "Sheet creases", fill=NONE, stroke="#A89468", strokeWidth=2,
       opacity=70)
# stubby cookie arms reaching the sheet
d.path("M436,506 C414,514 398,524 386,538", "Arm L", fill=NONE,
       stroke=COOKIE, strokeWidth=20, cap="round")
d.path("M506,532 C470,544 442,548 420,548", "Arm R", fill=NONE,
       stroke=COOKIE, strokeWidth=20, cap="round")
# hands pinching the wad
d.shape("ellipse", "Hand L", x=374, y=530, width=24, height=20,
        fill=COOKIE, stroke=INK, strokeWidth=3)
d.shape("ellipse", "Hand R", x=404, y=540, width=24, height=20,
        fill=COOKIE, stroke=INK, strokeWidth=3)

# --- the crumble trail: crumbs arcing from the wad down into the jar --------------------
crumbs = [(356,566,7),(338,586,6),(322,606,8),(306,622,5),(292,634,7),
          (350,596,4),(330,624,5)]
for i, (x, y, w) in enumerate(crumbs):
    d.shape("ellipse", f"Crumb {i+1}", x=x, y=y, width=w, height=w*0.8,
            fill="#C08A4E", stroke="#5A3A20", strokeWidth=1.5, opacity=95)
# a couple of tumbling sugar specks
d.shape("ellipse", "Sugar speck 1", x=312, y=590, width=4, height=4,
        fill="#F2E2C2", opacity=80, stroke=NONE)
d.shape("ellipse", "Sugar speck 2", x=344, y=614, width=3, height=3,
        fill="#F2E2C2", opacity=70, stroke=NONE)

# --- captions ------------------------------------------------------------------
d.text("COOKIE CRUMBLECLERK", "Name", x=500, y=934, size=55, font="Virelai Sans",
       color="#F0DFC0", justify="center")
r = d.text("CLERK OF CRUMBLED INTAKE", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#C09A6C", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("209.cookie-crumbleclerk-V1R00")
