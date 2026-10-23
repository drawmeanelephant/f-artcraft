#!/usr/bin/env python3
"""Obsolescence Steward — mascot portrait V1R00.
Steward polishing a shrouded retired structure from the scaffolding.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Obsolescence Steward — Mascot Portrait", 1000, 1000)

INK = "#332A33"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#141A10"}, {"offset": 1, "color": "#080B06"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#6A7350"}, {"offset": 0.7, "color": "#4A523A"},
    {"offset": 1, "color": "#2B3122"}]}}
FLOOR = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3A4130"}, {"offset": 1, "color": "#1E2418"}]}}
TARP = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#A8A2BC"}, {"offset": 0.7, "color": "#787294"},
    {"offset": 1, "color": "#4E4A62"}]}}
POLE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#9A7A4E"}, {"offset": 1, "color": "#6B4E30"}]}}
BODY = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F4E4C8"}, {"offset": 0.7, "color": "#E3C69E"},
    {"offset": 1, "color": "#C4A074"}]}}
CAP = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#66744E"}, {"offset": 1, "color": "#424E30"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#8A946A", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#DCE0C4", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(190,240,8),(800,230,7),(160,520,9),(830,540,8),
                               (240,760,7),(760,740,9),(130,390,6),(865,390,7),
                               (390,110,7),(610,110,8),(330,820,6),(665,815,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#5A6446", opacity=45, stroke=NONE)

# --- floor --------------------------------------------------------------------
d.shape("ellipse", "Floor", x=165, y=630, width=670, height=130,
        fill=FLOOR, stroke=NONE, opacity=90)
d.path("M255,676 C380,662 620,662 745,676", "Floor sheen", fill=NONE,
       stroke="#B0B68E", strokeWidth=3, opacity=20, cap="round")

# --- retired structure under its tarp -----------------------------------------
# drape silhouette, scalloped hem
d.path("M572,250 C622,250 646,306 652,388 C658,478 678,566 690,636 "
       "C672,650 650,640 636,652 C618,664 598,648 578,656 "
       "C556,664 534,648 514,656 C494,664 476,648 458,652 C442,656 428,648 418,636 "
       "C430,566 450,478 456,388 C462,306 522,250 572,250 Z",
       "Shrouded structure", fill=TARP, stroke=INK, strokeWidth=6)
# drape folds
d.path("M510,290 C506,390 500,500 492,620", "Fold 1", fill=NONE,
       stroke="#5A546E", strokeWidth=5, opacity=60, cap="round")
d.path("M580,270 C584,380 590,500 596,626", "Fold 2", fill=NONE,
       stroke="#5A546E", strokeWidth=5, opacity=60, cap="round")
d.path("M634,320 C632,420 630,520 640,622", "Fold 3", fill=NONE,
       stroke="#5A546E", strokeWidth=5, opacity=55, cap="round")
# top catchlight + deep fold shadow
d.shape("ellipse", "Tarp highlight", x=500, y=270, width=110, height=36,
        fill="#FFFFFF", opacity=16, stroke=NONE)
d.path("M640,400 C646,480 660,560 672,620 C660,600 652,520 644,430 Z",
       "Fold shadow", fill="#3E3A50", opacity=50, stroke=NONE)
# rope tied around the middle
d.path("M462,452 C520,472 616,472 668,450", "Rope", fill=NONE,
       stroke="#8A6B42", strokeWidth=8, cap="round")
d.path("M560,470 C562,486 558,498 550,506", "Rope tail", fill=NONE,
       stroke="#8A6B42", strokeWidth=6, cap="round")
d.shape("ellipse", "Rope knot", x=552, y=462, width=16, height=12,
        fill="#9A7A4E", stroke=INK, strokeWidth=3)
# plaque at the base
d.shape("rectangle", "Plaque", x=504, y=664, width=136, height=30,
        fill="#3E3524", stroke="#B09A62", strokeWidth=3, radius=4)
d.text("RETIRED", "Plaque text", x=572, y=684, size=14, font="Virelai Sans",
       color="#D8C88E", justify="center")

# --- scaffolding ---------------------------------------------------------------
# poles
d.shape("rectangle", "Pole L", x=352, y=308, width=14, height=392,
        fill=POLE, stroke=INK, strokeWidth=4, radius=4)
d.shape("rectangle", "Pole R", x=742, y=308, width=14, height=392,
        fill=POLE, stroke=INK, strokeWidth=4, radius=4)
# crossbars + plank the steward stands on
d.shape("rectangle", "Crossbar top", x=340, y=352, width=430, height=12,
        fill=POLE, stroke=INK, strokeWidth=4, radius=4)
d.shape("rectangle", "Plank", x=340, y=562, width=430, height=16,
        fill=POLE, stroke=INK, strokeWidth=4, radius=4)
# diagonal braces
d.path("M366,368 L474,562", "Brace L", fill=NONE, stroke="#7A5A36",
       strokeWidth=8, cap="round", opacity=85)
d.path("M742,368 L634,562", "Brace R", fill=NONE, stroke="#7A5A36",
       strokeWidth=8, cap="round", opacity=85)
# ladder rungs on the right pole
for i, y in enumerate([420, 470, 520]):
    d.path(f"M742,{y} L700,{y}", f"Rung {i+1}", fill=NONE, stroke="#7A5A36",
           strokeWidth=7, cap="round")

# --- the steward, mid-polish ----------------------------------------------------
# legs to the plank
d.path("M408,548 L404,566", "Leg back", fill=NONE, stroke="#C4A074",
       strokeWidth=11, cap="round")
d.path("M436,548 L440,566", "Leg front", fill=NONE, stroke="#D9BA8C",
       strokeWidth=11, cap="round")
d.shape("ellipse", "Shoe back", x=394, y=560, width=24, height=10,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Shoe front", x=430, y=560, width=24, height=10,
        fill=INK, stroke=NONE)
# body
d.path("M424,452 C462,452 482,480 480,510 C478,538 456,552 424,552 "
       "C392,552 370,538 368,510 C366,480 386,452 424,452 Z",
       "Steward body", fill=BODY, stroke=INK, strokeWidth=5)
d.shape("ellipse", "Body highlight", x=390, y=462, width=52, height=18,
        fill="#FFFFFF", opacity=20, stroke=NONE)
# caretaker cap
d.shape("ellipse", "Cap brim", x=388, y=446, width=76, height=12,
        fill="#35401F", stroke=INK, strokeWidth=3)
d.path("M398,448 L398,428 C398,416 410,410 426,410 C442,410 454,416 454,428 L454,448 Z",
       "Cap crown", fill=CAP, stroke=INK, strokeWidth=4, join="round")
# face: content at work, looking up at the tarp
d.shape("ellipse", "Eye L", x=408, y=496, width=11, height=14, fill=INK, stroke=NONE)
d.shape("ellipse", "Eye R", x=438, y=496, width=11, height=14, fill=INK, stroke=NONE)
d.shape("ellipse", "Glint L", x=411, y=499, width=4, height=4, fill="#FFFFFF", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=441, y=499, width=4, height=4, fill="#FFFFFF", opacity=90, stroke=NONE)
d.shape("ellipse", "Cheek L", x=394, y=516, width=18, height=10,
        fill="#E8A08C", opacity=55, stroke=NONE)
d.shape("ellipse", "Cheek R", x=442, y=516, width=18, height=10,
        fill="#E8A08C", opacity=55, stroke=NONE)
d.path("M416,528 C422,534 432,534 438,528", "Smile", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
# free arm holding the polish tin at its side
d.path("M376,506 C368,514 366,522 370,530", "Arm rest", fill=NONE,
       stroke="#D9BA8C", strokeWidth=10, cap="round")
d.shape("ellipse", "Polish tin", x=362, y=524, width=20, height=16,
        fill="#8A946A", stroke=INK, strokeWidth=3)
# working arm up to the tarp, cloth in hand
d.path("M470,496 C490,480 500,466 508,452", "Arm polish", fill=NONE,
       stroke="#E3C69E", strokeWidth=11, cap="round")
d.shape("ellipse", "Cloth", x=498, y=438, width=30, height=22,
        fill="#F4F0E2", stroke=INK, strokeWidth=3, opacity=95)
# polish arc on the tarp
d.path("M512,432 C530,420 556,418 574,428", "Polish arc 1", fill=NONE,
       stroke="#F4F0E2", strokeWidth=4, opacity=45, cap="round")
d.path("M518,444 C534,434 554,432 568,440", "Polish arc 2", fill=NONE,
       stroke="#F4F0E2", strokeWidth=4, opacity=30, cap="round")

# --- dust motes -----------------------------------------------------------------
for i, (x, y, w, o) in enumerate([(330,300,7,30),(760,300,5,25),(300,470,6,22),
                                  (790,470,4,24),(700,250,6,20),(250,620,5,20)]):
    d.shape("ellipse", f"Dust {i+1}", x=x, y=y, width=w, height=w,
            fill="#DCE0C4", opacity=o, stroke=NONE)

# --- captions -------------------------------------------------------------------
d.text("OBSOLESCENCE STEWARD", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#E4E8CC", justify="center")
r = d.text("KEEPER OF RETIRED STRUCTURES", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#AFB68E", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("434.obsolescence-steward-V1R00")
