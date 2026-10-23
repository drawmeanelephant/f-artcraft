#!/usr/bin/env python3
"""Vacancy Notice — mascot portrait V1R00.
A paper notice reading VACANCY (the mascot) pinned to a door that opens
onto uncut drywall. 1000x1000. Gradients + translucency, never flat."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Vacancy Notice — Mascot Portrait", 1000, 1000)

INK = "#3A2C22"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1A1510"}, {"offset": 1, "color": "#0B0806"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#B09A7E"}, {"offset": 0.7, "color": "#826C50"},
    {"offset": 1, "color": "#4E3F2E"}]}}
DOOR = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#96684A"}, {"offset": 1, "color": "#5E3E2A"}]}}
DRYWALL = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#CFCFC0"}, {"offset": 1, "color": "#A4A694"}]}}
PAPER = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F6EFDC"}, {"offset": 1, "color": "#DACFAE"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#7A6448", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8DAC0", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(205,230,8),(790,238,7),(170,538,9),(822,556,8),
                               (255,750,7),(745,742,9),(145,398,6),(852,406,7),
                               (398,116,7),(602,114,8),(340,810,6),(660,808,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#6E5A40", opacity=45, stroke=NONE)

# --- the doorway: uncut drywall revealed ---------------------------------------
# door frame
d.shape("rectangle", "Frame outer", x=348, y=268, width=304, height=464,
        fill="#4E3826", stroke=INK, strokeWidth=6, radius=4)
# drywall behind, in the opening
d.shape("rectangle", "Drywall", x=366, y=286, width=268, height=430,
        fill=DRYWALL, stroke=NONE)
# joint tape seams + screws: unfinished board
d.shape("rectangle", "Tape seam V", x=556, y=286, width=26, height=430,
        fill="#DCDBCB", opacity=80, stroke=NONE)
for i, y in enumerate(range(320, 700, 54)):
    d.shape("ellipse", f"Screw {i+1}", x=566, y=y, width=7, height=7,
            fill="#8A8C7C", stroke=NONE)
d.path("M370,540 L634,540", "Tape seam H", fill=NONE, stroke="#DCDBCB",
       strokeWidth=18, opacity=75)
for i, x in enumerate(range(400, 640, 60)):
    d.shape("ellipse", f"Screw h{i+1}", x=x, y=537, width=7, height=7,
            fill="#8A8C7C", stroke=NONE)
# corner bead + raw edge shadow
d.shape("rectangle", "Opening shade", x=366, y=286, width=268, height=430,
        fill="#3A3226", opacity=18, stroke=NONE)
d.shape("rectangle", "Corner bead", x=622, y=286, width=12, height=430,
        fill="#B8BAA8", stroke=NONE, opacity=90)

# --- door slab, hinged left, swung open toward the viewer ----------------------
d.path("M372,290 L372,714 L566,664 L566,336 Z", "Door slab", fill=DOOR,
       stroke=INK, strokeWidth=6, join="round")
# slab edge (thickness) at the free side
d.path("M566,336 L578,344 L578,672 L566,664 Z", "Slab edge", fill="#4A3222",
       stroke=INK, strokeWidth=4, join="round")
# recessed panels, skewed to the slab's perspective
d.path("M394,360 L530,390 L530,480 L394,456 Z", "Panel top", fill="#7A5238",
       stroke=INK, strokeWidth=4, join="round")
d.path("M396,368 L522,395 L522,470 L396,448 Z", "Panel top inset",
       fill="#8A5E40", stroke=NONE)
d.path("M394,520 L530,540 L530,636 L394,624 Z", "Panel bottom", fill="#7A5238",
       stroke=INK, strokeWidth=4, join="round")
d.path("M396,528 L522,547 L522,626 L396,616 Z", "Panel bottom inset",
       fill="#8A5E40", stroke=NONE)
# knob on the free edge + soft light through the gap
d.shape("ellipse", "Knob", x=540, y=520, width=22, height=22, fill="#C8A24A",
        stroke=INK, strokeWidth=4)
d.path("M566,340 L640,300 L640,710 L566,662 Z", "Gap light",
       fill="#E8E4CE", opacity=15, stroke=NONE)

# --- the VACANCY notice, pinned, with a face -----------------------------------
d.path("M394,342 L550,361 L542,492 L386,474 Z", "Notice shadow", fill="#2E2118",
       opacity=30, stroke=NONE)
d.path("M390,336 L546,355 L538,486 L382,468 Z", "Notice", fill=PAPER,
       stroke=INK, strokeWidth=5, join="round")
# pin tack at top centre
d.shape("ellipse", "Pin", x=460, y=342, width=18, height=18, fill="#B43A32",
       stroke=INK, strokeWidth=3)
d.shape("ellipse", "Pin glint", x=464, y=345, width=5, height=5,
        fill="#FFFFFF", opacity=80, stroke=NONE)
# the mascot face: weary eyes, flat mouth
d.shape("ellipse", "Notice eye L", x=432, y=390, width=12, height=14,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Notice eye R", x=490, y=390, width=12, height=14,
        fill=INK, stroke=NONE)
d.path("M428,384 L442,381", "Notice brow L", fill=NONE, stroke=INK,
       strokeWidth=3, cap="round")
d.path("M494,381 L508,384", "Notice brow R", fill=NONE, stroke=INK,
       strokeWidth=3, cap="round")
d.path("M452,414 C460,410 474,410 482,414", "Notice mouth", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
# the word
r1 = d.text("VACANCY", "Vacancy word", x=464, y=456, size=22,
            font="Virelai Sans", color="#8A2E28", justify="center")
if r1 and r1.get("id"):
    d.cmd("text.setStyle", "vacancy track", ids=[r1["id"]], tracking=90)
# two staple marks low on the paper
d.path("M396,460 L404,462 M524,474 L532,476", "Staples", fill=NONE,
       stroke="#8A8C7C", strokeWidth=3)

# --- captions ------------------------------------------------------------------
d.text("VACANCY NOTICE", "Name", x=500, y=930, size=56, font="Virelai Sans",
       color="#EADFC4", justify="center")
r = d.text("HERALD OF EMPTY ROOMS", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#B29A76", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("410.vacancy-notice-V1R00")
