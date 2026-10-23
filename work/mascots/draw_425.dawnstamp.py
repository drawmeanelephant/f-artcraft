#!/usr/bin/env python3
"""Dawnstamp — mascot portrait V1R00. HTTP 425, "Too Early".
Mascot pressing a stamp onto a document before sunrise. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Dawnstamp — Mascot Portrait", 1000, 1000)

INK = "#2E2430"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1C1A30"}, {"offset": 1, "color": "#0B0A16"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#D3DCE8"}, {"offset": 0.7, "color": "#9AA8C2"},
    {"offset": 1, "color": "#5F6E92"}]}}
BODY_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#5A6480"}, {"offset": 0.7, "color": "#3E4658"},
    {"offset": 1, "color": "#2A303E"}]}}
CAP_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7A5680"}, {"offset": 1, "color": "#4E3654"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#556284", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E2EAF4", strokeWidth=3, opacity=55)
# last stars of the night, high on the disc
for i, (x, y) in enumerate([(255,235),(745,245),(320,165),(680,170),(500,140),(210,430),(800,430)]):
    d.path(f"M{x-8},{y} L{x+8},{y} M{x},{y-8} L{x},{y+8}", f"Star {i+1}",
           fill=NONE, stroke="#EDF2FA", strokeWidth=3.5, opacity=40, cap="round")

# --- pre-dawn horizon inside the disc -------------------------------------------
# warm glow pooled on the horizon line
d.shape("ellipse", "Dawn glow", x=290, y=560, width=420, height=180,
        fill="#F2C48A", opacity=30, stroke=NONE)
d.shape("ellipse", "Glow core", x=400, y=600, width=200, height=90,
        fill="#FFD9A0", opacity=30, stroke=NONE)
# horizon land strip, ends on the disc's own curvature
d.path("M152,640 C300,612 700,612 848,640 A420,420 0 0 1 152,640 Z",
       "Horizon", fill="#2C3252", opacity=55, stroke=NONE)

# --- desk -------------------------------------------------------------------------
d.shape("ellipse", "Desk shadow", x=340, y=770, width=330, height=26,
        fill="#262C44", opacity=45, stroke=NONE)
d.shape("rectangle", "Desk", x=356, y=648, width=290, height=118,
        radius=8, fill="#4A3A50", stroke=INK, strokeWidth=5)
d.shape("rectangle", "Desk top edge", x=348, y=636, width=306, height=22,
        radius=8, fill="#5E4A62", stroke=INK, strokeWidth=4)

# --- the mascot, leaning in to stamp ------------------------------------------------
# body mound behind the desk
d.path("M378,648 C372,540 420,470 500,468 C580,470 628,540 622,648 Z",
       "Body", fill=BODY_GRAD, stroke=INK, strokeWidth=6, join="round")
d.path("M412,620 C412,560 436,512 470,494", "Body fold",
       fill=NONE, stroke="#222836", strokeWidth=7, opacity=40, cap="round")
# head
d.shape("ellipse", "Head", x=428, y=352, width=144, height=130,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#EDE0CC"}, {"offset": 1, "color": "#CBAF96"}]}},
        stroke=INK, strokeWidth=6)
# nightcap: floppy cone drooping right, pompom at the tip
d.path("M424,384 C428,330 462,296 506,296 C546,296 574,322 580,362 "
       "C610,352 640,362 654,388 C640,402 614,402 596,392 C580,410 560,424 534,430 "
       "C500,438 456,422 424,384 Z", "Nightcap",
       fill=CAP_GRAD, stroke=INK, strokeWidth=5, join="round")
d.shape("ellipse", "Pompom", x=644, y=382, width=34, height=34,
        fill="#EDE0CC", stroke=INK, strokeWidth=4)
d.path("M428,388 C470,368 540,368 576,384", "Cap band",
       fill=NONE, stroke=INK, strokeWidth=4, cap="round", opacity=60)
# sleepy half-lidded eyes
d.path("M456,414 L456,404", "Lid L hint", fill=NONE, stroke=INK, strokeWidth=0, opacity=0)
d.path("M452,418 C458,424 470,424 476,418 M510,418 C516,424 528,424 534,418",
       "Eyes", fill=NONE, stroke=INK, strokeWidth=5, cap="round")
d.path("M450,402 L478,406 M508,406 L536,402", "Heavy lids",
       fill=NONE, stroke=INK, strokeWidth=4, cap="round", opacity=65)
d.path("M480,452 C488,458 500,458 506,452", "Mouth",
       fill=NONE, stroke=INK, strokeWidth=5, cap="round")
# left arm braced on the desk edge
d.path("M400,560 C388,592 388,616 396,638", "Arm L",
       fill=NONE, stroke="#3E4658", strokeWidth=24, cap="round")
d.shape("ellipse", "Hand L", x=382, y=624, width=32, height=26,
        fill="#D9BFA4", stroke=INK, strokeWidth=4)
# right arm reaching to the stamp
d.path("M584,548 C612,566 630,590 638,614", "Arm R",
       fill=NONE, stroke="#3E4658", strokeWidth=24, cap="round")
# the stamp, pressed down onto the paper
d.path("M580,516 L624,512 L630,558 L574,562 Z", "Stamp neck",
       fill="#8A6238", stroke=INK, strokeWidth=4, join="round")
d.shape("ellipse", "Stamp knob", x=590, y=486, width=24, height=26,
        fill="#6E4A2A", stroke=INK, strokeWidth=4)
d.path("M570,556 L636,552 L640,584 L566,588 Z", "Stamp base",
       fill="#3E3A34", stroke=INK, strokeWidth=4, join="round")
# pressure ticks under the stamp
d.path("M556,592 L544,598 M650,586 L662,590", "Press ticks",
       fill=NONE, stroke=INK, strokeWidth=4, cap="round", opacity=60)
# the document on the desk's front edge, under the stamp
d.path("M470,600 L636,596 L648,636 L478,642 Z", "Document",
       fill="#F4EEDA", stroke=INK, strokeWidth=3, join="round")
d.path("M486,610 L560,608 M488,622 L596,618", "Doc rules",
       fill=NONE, stroke="#9A9482", strokeWidth=3, opacity=80)
# fresh stamp imprint: still-wet red seal ring on the paper
d.shape("ellipse", "Imprint ring", x=578, y=602, width=40, height=26,
        fill=NONE, stroke="#C8483A", strokeWidth=4, opacity=85)
d.path("M586,615 L608,614", "Imprint bar", fill=NONE, stroke="#C8483A",
       strokeWidth=3, opacity=85, cap="round")
# hand gripping the stamp, over the paper edge
d.shape("ellipse", "Hand R", x=624, y=596, width=32, height=30,
        fill="#D9BFA4", stroke=INK, strokeWidth=4)

# --- name + role ----------------------------------------------------------------------
d.text("DAWNSTAMP", "Name", x=500, y=930, size=58, font="Virelai Sans",
       color="#DEE6F2", justify="center")
d.text(" ".join("TOO EARLY"), "Role", x=500, y=968, size=23, font="Virelai Sans",
       color="#A2B2CC", justify="center")

d.finish("425.dawnstamp-V1R00")
