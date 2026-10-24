#!/usr/bin/env python3
"""Cinder Forgememo — mascot portrait V1R00.
Ember scribe etching a dictate into an ash tablet with a burning quill
in a smoldering vault. 1000x1000. House style: gradients + translucent
shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Cinder Forgememo — Mascot Portrait", 1000, 1000)

INK = "#38201A"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#170C08"}, {"offset": 1, "color": "#0A0504"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#6B3A24"}, {"offset": 0.7, "color": "#442416"},
    {"offset": 1, "color": "#2A1209"}]}}
STONE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7A7268"}, {"offset": 1, "color": "#4A4238"}]}}
STONE_DARK = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#564E44"}, {"offset": 1, "color": "#322A22"}]}}
CLOAK = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4E3830"}, {"offset": 0.7, "color": "#35241D"},
    {"offset": 1, "color": "#241510"}]}}
GLASS = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#FFD98A"}, {"offset": 1, "color": "#C97B3A"}]}}
FEATHER = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#EEDCB4"}, {"offset": 1, "color": "#B8976A"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#C97E4E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F2C9A0", strokeWidth=3, opacity=50)
for i, (x, y, w) in enumerate([(190,240,8),(800,230,7),(160,520,9),(830,540,8),
                               (240,760,7),(760,740,9),(130,390,6),(865,390,7),
                               (390,110,7),(610,110,8),(330,820,6),(665,815,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#7A4630", opacity=45, stroke=NONE)
for i, (x, y, w) in enumerate([(300,200,5),(700,300,4),(210,640,5),(790,660,4),
                               (500,160,4),(420,780,5)]):
    d.shape("ellipse", f"Ember fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#C97B4A", opacity=60, stroke=NONE)

# --- vault ambience: faint arches on the plate ---------------------------------
d.path("M250,720 C250,400 375,290 500,290 C625,290 750,400 750,720",
       "Vault arch outer", fill=NONE, stroke="#8A5A3C", strokeWidth=4, opacity=18)
d.path("M300,720 C300,440 400,340 500,340 C600,340 700,440 700,720",
       "Vault arch inner", fill=NONE, stroke="#8A5A3C", strokeWidth=3, opacity=14)

# --- floor ----------------------------------------------------------------------
d.shape("ellipse", "Floor shadow", x=270, y=690, width=460, height=66,
        fill="#140A06", opacity=60, stroke=NONE)
d.shape("ellipse", "Tablet underglow", x=340, y=690, width=270, height=40,
        fill="#FF8A3C", opacity=12, stroke=NONE)

# --- lantern on a crook, left ---------------------------------------------------
d.path("M240,706 L240,440 M240,440 C240,418 258,410 274,418",
       "Lantern post", fill=NONE, stroke=INK, strokeWidth=9, cap="round")
d.shape("ellipse", "Lantern glow", x=200, y=420, width=150, height=170,
        fill="#FFB85C", opacity=16, stroke=NONE)
d.shape("ellipse", "Lantern glow inner", x=228, y=448, width=94, height=108,
        fill="#FFC97E", opacity=20, stroke=NONE)
d.path("M250,452 L296,452 L288,516 L258,516 Z", "Lantern body",
       fill=GLASS, stroke=INK, strokeWidth=5, join="round")
d.shape("rectangle", "Lantern cap", x=258, y=438, width=30, height=14,
        fill=INK, stroke=NONE, radius=4)
d.path("M262,516 L284,516 L290,530 L256,530 Z", "Lantern foot",
       fill=INK, stroke=NONE, join="round")
d.path("M270,498 C266,486 270,476 276,470 C280,480 284,490 278,498 Z",
       "Candle flame", fill="#FFE9B0", stroke=NONE, opacity=95)

# --- ash tablet on its lectern --------------------------------------------------
d.path("M398,676 L572,650 L560,724 L414,724 Z", "Lectern",
       fill=STONE_DARK, stroke=INK, strokeWidth=5, join="round")
d.path("M330,588 L560,558 L600,650 L370,690 Z", "Ash tablet",
       fill=STONE, stroke=INK, strokeWidth=6, join="round")
# etched dictate, still glowing
for i, (x0, y0, x1, y1) in enumerate([(368,606,516,584),(378,630,540,606),
                                      (388,654,500,636)]):
    d.path(f"M{x0},{y0} L{x1},{y1}", f"Etch glow {i+1}", fill=NONE,
           stroke="#FFB84D", strokeWidth=12, opacity=22, cap="round")
    d.path(f"M{x0},{y0} L{x1},{y1}", f"Etch line {i+1}", fill=NONE,
           stroke="#FFC35C", strokeWidth=5, opacity=95, cap="round")
# last line half-etched, brightest at the quill tip
d.path("M398,676 L470,664", "Etch line 4", fill=NONE,
       stroke="#FFE1A0", strokeWidth=5, opacity=100, cap="round")
d.shape("ellipse", "Nib spark", x=464, y=650, width=26, height=22,
        fill="#FFE9B0", opacity=85, stroke=NONE)
# crumbled ash at the lectern foot
d.shape("ellipse", "Ash mound", x=560, y=706, width=90, height=24,
        fill="#5C5348", opacity=80, stroke=NONE)
for i, (x, y, w) in enumerate([(600,700,5),(630,708,4),(575,712,4)]):
    d.shape("ellipse", f"Ash speck {i+1}", x=x, y=y, width=w, height=w,
            fill="#8A8078", opacity=70, stroke=NONE)

# --- the scribe -------------------------------------------------------------------
d.shape("ellipse", "Scribe shadow", x=520, y=700, width=240, height=36,
        fill="#0E0604", opacity=55, stroke=NONE)
# hooded cloak: pointed hood, shoulders, flared hem
d.path("M640,352 C592,360 556,408 550,462 C546,540 528,620 516,706 "
       "C570,726 712,726 764,706 C752,620 734,540 730,462 "
       "C724,408 688,360 640,352 Z",
       "Cloak", fill=CLOAK, stroke=INK, strokeWidth=6, join="round")
# hem ember-light
d.path("M540,690 C600,706 690,706 742,688", "Hem glow", fill=NONE,
       stroke="#B4643A", strokeWidth=5, opacity=45, cap="round")
# face void inside the hood
d.path("M598,452 C598,418 616,400 640,400 C664,400 682,418 682,452 "
       "C682,480 664,494 640,494 C616,494 598,480 598,452 Z",
       "Face void", fill="#150B07", stroke=NONE)
# warm rim light inside hood
d.path("M604,470 C616,486 664,486 676,470", "Hood rim light", fill=NONE,
       stroke="#B4643A", strokeWidth=4, opacity=55, cap="round")
# glowing eyes
d.shape("ellipse", "Eye L", x=616, y=440, width=17, height=13, fill="#FFC35C", stroke=NONE)
d.shape("ellipse", "Eye R", x=648, y=440, width=17, height=13, fill="#FFC35C", stroke=NONE)
d.shape("ellipse", "Eye L core", x=620, y=443, width=9, height=7, fill="#FFE9B0", stroke=NONE)
d.shape("ellipse", "Eye R core", x=652, y=443, width=9, height=7, fill="#FFE9B0", stroke=NONE)
# faint ember mouth
d.path("M628,474 C636,478 646,478 654,473", "Mouth", fill=NONE,
       stroke="#FF9A3C", strokeWidth=3, opacity=70, cap="round")
# ember cracks through the charred cloak
d.path("M560,560 C576,576 582,602 572,628", "Crack 1", fill=NONE,
       stroke="#FF9A3C", strokeWidth=3, opacity=75, cap="round")
d.path("M706,540 C696,568 700,596 714,618", "Crack 2", fill=NONE,
       stroke="#FF9A3C", strokeWidth=3, opacity=70, cap="round")
d.path("M620,650 C630,668 626,686 634,700", "Crack 3", fill=NONE,
       stroke="#FF9A3C", strokeWidth=3, opacity=65, cap="round")
d.shape("ellipse", "Crack glow 1", x=562, y=590, width=24, height=34,
        fill="#FF8A3C", opacity=14, stroke=NONE)
d.shape("ellipse", "Crack glow 2", x=694, y=560, width=24, height=34,
        fill="#FF8A3C", opacity=12, stroke=NONE)
# sleeve reaching down-left to the tablet
d.path("M566,528 C548,548 534,570 524,592", "Sleeve", fill=NONE,
       stroke="#35241D", strokeWidth=30, cap="round")
d.path("M566,528 C548,548 534,570 524,592", "Sleeve seam", fill=NONE,
       stroke=INK, strokeWidth=4, opacity=60, cap="round")
d.shape("ellipse", "Hand", x=510, y=584, width=24, height=20,
        fill="#8A5030", stroke=INK, strokeWidth=4)

# --- burning quill ------------------------------------------------------------------
# vane
d.path("M520,586 C500,550 486,512 482,478 C478,452 492,442 502,458 "
       "C516,482 524,536 528,580 Z",
       "Quill vane", fill=FEATHER, stroke=INK, strokeWidth=4, join="round")
d.path("M520,584 C508,548 498,508 494,470", "Quill shaft", fill=NONE,
       stroke=INK, strokeWidth=3, opacity=80)
# flame at the plume tip
d.shape("ellipse", "Flame halo", x=452, y=392, width=92, height=110,
        fill="#FF8A3C", opacity=20, stroke=NONE)
d.path("M496,458 C478,430 484,398 500,378 C510,402 522,432 506,458 Z",
       "Flame outer", fill="#FF8A2A", stroke=NONE, opacity=95)
d.path("M498,452 C488,432 492,410 501,396 C507,414 512,434 504,452 Z",
       "Flame inner", fill="#FFD98A", stroke=NONE)

# --- rising embers + smoke -----------------------------------------------------------
d.path("M540,540 C530,500 556,482 546,442 C538,412 560,396 552,368",
       "Smoke curl", fill=NONE, stroke="#C9A98C", strokeWidth=6,
       opacity=25, cap="round")
for i, (x, y, w, o) in enumerate([(430,540,6,70),(470,498,5,60),(612,536,7,75),
                                  (664,478,5,60),(560,428,6,65),(502,378,4,55),
                                  (644,378,5,60),(704,430,4,50),(452,438,4,55),
                                  (592,340,5,60),(684,330,4,45),(420,300,4,40)]):
    d.shape("ellipse", f"Ember {i+1}", x=x, y=y, width=w, height=w,
            fill="#FFB85C", opacity=o, stroke=NONE)
for i, (x, y) in enumerate([(480,460),(640,410),(560,360)]):
    d.path(f"M{x},{y} l5,8 l-5,8 l-5,-8 Z", f"Spark {i+1}",
           fill="#FFE1A0", opacity=80, stroke=NONE)

# --- captions ----------------------------------------------------------------------
d.text("CINDER FORGEMEMO", "Name", x=500, y=930, size=56, font="Virelai Sans",
       color="#F2D9C0", justify="center")
r = d.text("EMBER SCRIBE", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#C9936E", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("203.cinder-forgememo-V1R00")
