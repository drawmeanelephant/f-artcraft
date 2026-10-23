#!/usr/bin/env python3
"""Sidecar Conflict Porter — mascot portrait V1R00.
Porter hauling boxed contradictions to a shelf in the adjacent annex.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Sidecar Conflict Porter — Mascot Portrait", 1000, 1000)

INK = "#332A33"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#161B33"}, {"offset": 1, "color": "#090B18"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4A5480"}, {"offset": 0.7, "color": "#333C62"},
    {"offset": 1, "color": "#1E2542"}]}}
FLOOR = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2A3157"}, {"offset": 1, "color": "#151A33"}]}}
BODY = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F4E4C8"}, {"offset": 0.7, "color": "#E3C69E"},
    {"offset": 1, "color": "#C4A074"}]}}
CAP = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#8E4556"}, {"offset": 1, "color": "#5E2C3C"}]}}
BOX_HI = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#D9AE72"}, {"offset": 1, "color": "#B0804C"}]}}
BOX_LO = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#C79B60"}, {"offset": 1, "color": "#9A6E3E"}]}}
LIGHT = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F5CE7E"}, {"offset": 1, "color": "#B57E3D"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#5E6E9C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C9D4F2", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(190,240,8),(800,230,7),(160,520,9),(830,540,8),
                               (240,760,7),(760,740,9),(130,390,6),(865,390,7),
                               (390,110,7),(610,110,8),(330,820,6),(665,815,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#48547E", opacity=45, stroke=NONE)

# --- floor --------------------------------------------------------------------
d.shape("ellipse", "Floor", x=165, y=620, width=670, height=135,
        fill=FLOOR, stroke=NONE, opacity=90)
d.path("M255,664 C380,650 620,650 745,664", "Floor sheen", fill=NONE,
       stroke="#8892C2", strokeWidth=3, opacity=22, cap="round")

# --- annex doorway (right), warm light spilling -------------------------------
d.path("M652,620 L652,392 C652,330 690,296 738,296 C786,296 824,330 824,392 L824,620 Z",
       "Annex opening", fill="#141A30", stroke=NONE)
d.path("M664,620 L664,396 C664,344 696,312 738,312 C780,312 812,344 812,396 L812,620 Z",
       "Annex light", fill=LIGHT, opacity=85, stroke=NONE)
# inner annex depth: shelf silhouettes in the light
for i, y in enumerate([420, 480, 540]):
    d.shape("rectangle", f"Annex shelf {i+1}", x=688, y=y, width=102, height=10,
            fill="#7A5426", opacity=55, stroke=NONE)
for i, (x, y, w, h) in enumerate([(694,392,30,28),(736,392,44,28),(700,452,52,28),
                                  (762,452,28,28),(696,512,40,28),(748,512,52,28)]):
    d.shape("rectangle", f"Annex box {i+1}", x=x, y=y, width=w, height=h,
            fill="#96692F", opacity=60, stroke=NONE)
# architrave
d.path("M652,620 L652,392 C652,330 690,296 738,296 C786,296 824,330 824,392 L824,620",
       "Annex frame", fill=NONE, stroke=INK, strokeWidth=7, cap="round")
# light spill on the floor
d.path("M664,620 L812,620 L772,700 L590,700 Z", "Door light spill",
       fill="#F0C878", opacity=14, stroke=NONE)
d.text("ANNEX", "Annex plaque", x=738, y=268, size=17, font="Virelai Sans",
       color="#D9B988", justify="center")

# --- wall shelf, left, holding shelved contradictions -------------------------
d.shape("rectangle", "Shelf board", x=168, y=352, width=196, height=16,
        fill="#2C2F4E", stroke=INK, strokeWidth=4, radius=4)
d.path("M186,368 L186,390 M348,368 L348,390", "Shelf brackets", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
d.shape("rectangle", "Shelf box 1", x=180, y=296, width=62, height=56,
        fill=BOX_LO, stroke=INK, strokeWidth=4, radius=5)
d.path("M211,296 L211,352", "Shelf box 1 tape", fill=NONE, stroke="#7A5426",
       strokeWidth=6, opacity=70)
d.shape("rectangle", "Shelf box 2", x=254, y=312, width=52, height=40,
        fill=BOX_HI, stroke=INK, strokeWidth=4, radius=5)
d.path("M280,312 L280,352", "Shelf box 2 tape", fill=NONE, stroke="#7A5426",
       strokeWidth=6, opacity=70)
d.text("YES / NO", "Shelf label 1", x=211, y=330, size=10, font="Virelai Sans",
       color="#4A3220", justify="center")
d.text("UP ↓", "Shelf label 2", x=280, y=338, size=10, font="Virelai Sans",
       color="#4A3220", justify="center")

# --- motion lines behind the porter -------------------------------------------
for i, (y, x0, x1) in enumerate([(500, 262, 318), (545, 252, 306), (590, 268, 320)]):
    d.path(f"M{x0},{y} L{x1},{y}", f"Motion {i+1}", fill=NONE,
           stroke="#C9D4F2", strokeWidth=5, opacity=35, cap="round")

# --- the porter ---------------------------------------------------------------
# legs mid-step (behind body)
d.path("M448,636 L436,684", "Leg back", fill=NONE, stroke="#C4A074",
       strokeWidth=15, cap="round")
d.path("M478,636 L492,682", "Leg front", fill=NONE, stroke="#D9BA8C",
       strokeWidth=15, cap="round")
d.shape("ellipse", "Shoe back", x=420, y=676, width=34, height=16,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Shoe front", x=478, y=674, width=34, height=16,
        fill=INK, stroke=NONE)
# body: round little porter
d.path("M462,420 C522,420 548,472 545,528 C542,590 512,636 462,636 "
       "C412,636 382,590 379,528 C376,472 402,420 462,420 Z",
       "Porter body", fill=BODY, stroke=INK, strokeWidth=6)
d.shape("ellipse", "Body highlight", x=400, y=436, width=90, height=30,
        fill="#FFFFFF", opacity=20, stroke=NONE)
d.path("M410,614 C440,626 486,626 512,612 C486,620 438,620 410,614 Z",
       "Body shadow", fill="#A57E54", opacity=45, stroke=NONE)
# porter cap: flat bellhop pill + brim + badge
d.shape("ellipse", "Cap brim", x=402, y=412, width=120, height=18,
        fill="#4A2430", stroke=INK, strokeWidth=4)
d.path("M418,414 L418,384 C418,368 436,360 462,360 C488,360 506,368 506,384 L506,414 Z",
       "Cap crown", fill=CAP, stroke=INK, strokeWidth=5, join="round")
d.shape("ellipse", "Cap badge", x=454, y=378, width=16, height=16,
        fill="#F0C878", stroke=INK, strokeWidth=3)
# face: eyes fixed on the boxes, effort cheeks, small o mouth
d.shape("ellipse", "Eye L", x=434, y=486, width=17, height=21, fill=INK, stroke=NONE)
d.shape("ellipse", "Eye R", x=478, y=486, width=17, height=21, fill=INK, stroke=NONE)
d.shape("ellipse", "Glint L", x=438, y=490, width=5, height=5, fill="#FFFFFF", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=482, y=490, width=5, height=5, fill="#FFFFFF", opacity=90, stroke=NONE)
d.shape("ellipse", "Cheek L", x=408, y=516, width=26, height=15,
        fill="#E8A08C", opacity=55, stroke=NONE)
d.shape("ellipse", "Cheek R", x=494, y=516, width=26, height=15,
        fill="#E8A08C", opacity=55, stroke=NONE)
d.shape("ellipse", "Mouth", x=456, y=534, width=16, height=14,
        fill="NONE" if False else "#7A4638", stroke=INK, strokeWidth=3)

# --- arms reaching around the box stack ---------------------------------------
d.path("M512,512 L560,540", "Arm upper", fill=NONE, stroke="#E3C69E",
       strokeWidth=14, cap="round")
d.path("M514,566 L560,586", "Arm lower", fill=NONE, stroke="#D9BA8C",
       strokeWidth=14, cap="round")
d.shape("ellipse", "Hand upper", x=552, y=532, width=18, height=16,
        fill="#EED3AC", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Hand lower", x=552, y=578, width=18, height=16,
        fill="#EED3AC", stroke=INK, strokeWidth=3)

# --- the contradiction stack ---------------------------------------------------
d.shape("rectangle", "Box bottom", x=560, y=548, width=132, height=92,
        fill=BOX_LO, stroke=INK, strokeWidth=5, radius=6)
d.path("M668,548 L668,640", "Box bottom tape", fill=NONE, stroke="#7A5426",
       strokeWidth=8, opacity=70)
d.shape("rectangle", "Box top", x=572, y=458, width=108, height=82,
        fill=BOX_HI, stroke=INK, strokeWidth=5, radius=6)
d.path("M626,458 L626,540", "Box top tape", fill=NONE, stroke="#7A5426",
       strokeWidth=8, opacity=70)
# contradictory labels
d.text("DO NOT OPEN", "Label bottom", x=610, y=600, size=12, font="Virelai Sans",
       color="#4A3220", justify="center")
d.text("OPEN FIRST", "Label top", x=626, y=512, size=12, font="Virelai Sans",
       color="#4A3220", justify="center")
# THIS SIDE UP tag on the top box, arrow drawn pointing down
d.text("THIS SIDE UP", "Label side", x=622, y=482, size=9, font="Virelai Sans",
       color="#6B4A28", justify="center")
d.path("M658,470 L658,482 M652,476 L658,482 L664,476", "Up arrow (down)",
       fill=NONE, stroke="#6B4A28", strokeWidth=3, cap="round", join="round")

# --- dust motes in the door light ---------------------------------------------
for i, (x, y, w, o) in enumerate([(700,640,7,30),(740,668,5,25),(676,690,6,20),
                                  (724,700,4,22),(760,640,5,26)]):
    d.shape("ellipse", f"Dust {i+1}", x=x, y=y, width=w, height=w,
            fill="#F5DC9E", opacity=o, stroke=NONE)

# --- captions ------------------------------------------------------------------
d.text("SIDECAR CONFLICT PORTER", "Name", x=500, y=930, size=48,
       font="Virelai Sans", color="#D8DFF2", justify="center")
r = d.text("COURIER OF BOXED CONTRADICTIONS", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#9FAAD4", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("433.sidecar-conflict-porter-V1R00")
