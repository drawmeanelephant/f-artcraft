#!/usr/bin/env python3
"""Attestation Mole — mascot portrait V1R00.
A blind mole underground pressing a seal-stamp onto a form it cannot read —
placement accurate to the signature line anyway; one form already struck twice,
once over the other. 1000x1000. Gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Attestation Mole — Mascot Portrait", 1000, 1000)

INK = "#2E241E"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1E1610"}, {"offset": 1, "color": "#0D0906"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#7A6248"}, {"offset": 0.7, "color": "#54402E"},
    {"offset": 1, "color": "#2A1F16"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4A3828"}, {"offset": 1, "color": "#221910"}]}}
FUR_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#8A7A6E"}, {"offset": 0.72, "color": "#655649"},
    {"offset": 1, "color": "#443830"}]}}
PAPER = "#E8DCC0"
SEAL = "#A8463E"
STONE = "#6E5B45"
ROOT = "#8A7458"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#8A6F52", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E0CBA8", strokeWidth=3, opacity=45)
# burrow vignette: the chamber darkens toward its walls
d.shape("ellipse", "Vignette", x=140, y=100, width=720, height=720,
        fill="#1A120C", opacity=22, stroke=NONE)
d.shape("ellipse", "Chamber glow", x=280, y=280, width=440, height=380,
        fill="#D8B988", opacity=10, stroke=NONE)
# strata flecks + stones worked into the soil
for i, (x, y, w) in enumerate([(190,230,8),(804,232,7),(158,516,9),(836,540,8),
                               (252,764,7),(750,746,9),(134,388,6),(864,390,7),
                               (394,112,7),(612,110,8),(334,820,6),(668,820,7)]):
    d.shape("ellipse", f"Stone {i+1}", x=x, y=y, width=w, height=w,
            fill=STONE, opacity=50, stroke=NONE)
for i, (x, y, w, h) in enumerate([(240,340,34,16),(700,300,28,14),(190,470,26,13),
                                  (790,480,32,15),(420,240,24,12),(610,210,22,11)]):
    d.shape("ellipse", f"Pebble {i+1}", x=x, y=y, width=w, height=h,
            fill=STONE, opacity=35, stroke=NONE)

# --- hanging roots: the ceiling of every underground office ---------------------
for i, (x0, y1, x1) in enumerate([(250,268,238),(330,224,338),(585,238,574),
                                  (660,290,668),(745,230,752)]):
    d.path(f"M{x0},118 C{x0-8},{(118+y1)//2} {x1+8},{(118+y1)//2+20} {x1},{y1}",
           f"Root {i+1}", fill=NONE, stroke=ROOT, strokeWidth=5,
           cap="round", opacity=65)
d.path("M338,224 C344,244 350,258 358,268", "Rootlet L", fill=NONE,
       stroke=ROOT, strokeWidth=3, cap="round", opacity=50)
d.path("M668,290 C676,306 684,318 694,326", "Rootlet R", fill=NONE,
       stroke=ROOT, strokeWidth=3, cap="round", opacity=50)

# --- floor: bottom segment closed on the disc's own arc -------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#171009",
       strokeWidth=4, opacity=70)

# --- the form: lying where the signature line already was ------------------------
d.shape("ellipse", "Form shadow", x=520, y=676, width=280, height=18,
        fill="#0C0806", opacity=45, stroke=NONE)
d.path("M540,600 L768,586 L784,682 L552,696 Z", "Form", fill=PAPER,
       stroke=INK, strokeWidth=4, join="round")
# ruled lines the mole does not read but knows
for i in range(3):
    y = 616 + i*18
    d.path(f"M560,{y} L740,{y-7}", f"Rule {i+1}", fill=NONE,
           stroke="#B4A488", strokeWidth=3, opacity=60)
# signature line: the one that matters
d.path("M566,672 C584,656 600,676 618,662 C632,652 646,664 660,658",
       "Signature", fill=NONE, stroke="#4A3E30", strokeWidth=3, cap="round")
d.path("M560,680 L690,672", "Sig line", fill=NONE, stroke="#4A3E30",
       strokeWidth=3, opacity=70)
# the seal, struck twice — the only documented hesitation on record
d.shape("ellipse", "Seal ghost", x=692, y=620, width=58, height=58,
        fill=NONE, stroke=SEAL, strokeWidth=5, opacity=35)
d.shape("ellipse", "Seal", x=700, y=614, width=58, height=58,
        fill=NONE, stroke=SEAL, strokeWidth=6, opacity=85)
d.shape("ellipse", "Seal star", x=714, y=628, width=30, height=30,
        fill=SEAL, opacity=85, stroke=NONE)
for i in range(6):
    import math
    a = i * 60
    x1 = 729 + 16*math.cos(math.radians(a)); y1 = 643 + 16*math.sin(math.radians(a))
    x2 = 729 + 24*math.cos(math.radians(a)); y2 = 643 + 24*math.sin(math.radians(a))
    d.path(f"M{x1:.0f},{y1:.0f} L{x2:.0f},{y2:.0f}", f"Seal ray {i+1}",
           fill=NONE, stroke=SEAL, strokeWidth=4, cap="round", opacity=85)

# --- the stamp: knob proud of the paws, base flush on the paper --------------------
d.path("M648,458 C648,438 664,428 680,428 C696,428 712,438 712,458 "
       "C712,470 706,478 696,482 L664,482 C654,478 648,470 648,458 Z",
       "Stamp knob", fill="#6A4A32", stroke=INK, strokeWidth=4, join="round")
d.shape("ellipse", "Knob hi", x=660, y=434, width=22, height=12,
        fill="#FFFFFF", opacity=18, stroke=NONE)
d.path("M660,482 L700,482 L704,556 L656,556 Z", "Stamp neck",
       fill="#8A6244", stroke=INK, strokeWidth=4)
d.path("M636,556 L724,556 L734,594 L626,594 Z", "Stamp base",
       fill="#4A3428", stroke=INK, strokeWidth=4, join="round")
d.path("M632,588 L728,588", "Base edge", fill=NONE, stroke=INK,
       strokeWidth=3, opacity=60)
# impression just landed: a ghost of fresh red under the base
d.path("M634,596 L726,596 L730,620 L630,624 Z", "Fresh ink",
       fill=SEAL, opacity=25, stroke=NONE)

# --- the Mole: it stamps in the dark without error -------------------------------
d.shape("ellipse", "Mole shadow", x=280, y=680, width=280, height=26,
        fill="#0C0806", opacity=50, stroke=NONE)
# haunched body, all shoulders and patience
d.path("M300,700 C296,600 300,540 330,495 C352,462 390,450 415,455 "
       "C470,468 520,540 540,610 C550,650 555,675 552,700 Z",
       "Mole body", fill=FUR_GRAD, stroke=INK, strokeWidth=6)
d.shape("ellipse", "Body hi", x=330, y=500, width=120, height=70,
        fill="#FFFFFF", opacity=10, stroke=NONE)
# fur texture: a few short strokes on the haunch
for i, (x, y) in enumerate([(340,590),(360,640),(390,560),(370,610)]):
    d.path(f"M{x},{y} C{x+14},{y+10} {x+24},{y+16} {x+30},{y+26}",
           f"Fur {i+1}", fill=NONE, stroke="#4A3C30", strokeWidth=3,
           cap="round", opacity=55)

# head: no brow, no eyes to speak of — just certainty
d.path("M400,470 C400,415 445,385 495,392 C545,399 570,440 565,485 "
       "C560,525 525,545 480,540 C435,535 400,515 400,470 Z",
       "Head", fill=FUR_GRAD, stroke=INK, strokeWidth=6)
# closed eyes: two content arcs — it has never needed to see the form
d.path("M455,452 C463,459 473,459 481,452", "Eye L", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
d.path("M505,455 C513,462 523,462 531,455", "Eye R", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
# the snout: pink, tipped down toward the work — it reads pressure, not print
d.path("M545,495 C570,488 596,496 604,514 C610,530 596,542 574,540 "
       "C552,538 538,522 540,508 C541,501 542,498 545,495 Z",
       "Snout", fill="#C08A7E", stroke=INK, strokeWidth=5, join="round")
d.shape("ellipse", "Nose tip", x=590, y=512, width=16, height=13,
        fill="#8A5A50", stroke=INK, strokeWidth=3)
# whiskers: the instrumentation, straight off the muzzle
d.path("M598,520 C618,514 636,512 652,514 M596,529 C614,530 632,535 646,542",
       "Whiskers", fill=NONE, stroke="#D8C8B4", strokeWidth=3,
       cap="round", opacity=70)
# small assured mouth under the snout root
d.path("M516,518 C524,524 536,524 544,518", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")

# forepaws: wide shovels stacked on the stamp neck, pressing home
d.path("M598,492 C620,480 648,478 668,486 C684,492 692,504 686,514 "
       "C680,523 662,526 644,520 C622,513 606,504 598,492 Z",
       "Paw T", fill=FUR_GRAD, stroke=INK, strokeWidth=5, join="round")
d.path("M594,532 C616,520 644,518 664,526 C680,532 688,544 682,554 "
       "C676,563 658,566 640,560 C618,553 602,544 594,532 Z",
       "Paw B", fill=FUR_GRAD, stroke=INK, strokeWidth=5, join="round")
# claws: three pale spades per paw, gripping the far side of the shaft
for i in range(3):
    y = 490 + i*9
    d.path(f"M692,{y} C704,{y+2} 712,{y+6} 716,{y+12}", f"Claw T{i+1}",
           fill=NONE, stroke="#E0D2BC", strokeWidth=5, cap="round")
for i in range(3):
    y = 530 + i*9
    d.path(f"M688,{y} C700,{y+2} 708,{y+6} 712,{y+12}", f"Claw B{i+1}",
           fill=NONE, stroke="#E0D2BC", strokeWidth=5, cap="round")

# --- the earlier form: already sealed, already load-bearing -----------------------
d.shape("ellipse", "Old form shadow", x=200, y=678, width=180, height=14,
        fill="#0C0806", opacity=40, stroke=NONE)
d.path("M196,610 L340,620 L330,682 L186,672 Z", "Old form", fill="#D8CBA8",
       stroke=INK, strokeWidth=4, join="round")
for i in range(2):
    y = 630 + i*16
    d.path(f"M208,{y} L310,{y+5}", f"Old rule {i+1}", fill=NONE,
           stroke="#A89878", strokeWidth=3, opacity=55)
d.shape("ellipse", "Old seal", x=268, y=642, width=34, height=34,
        fill=NONE, stroke=SEAL, strokeWidth=4, opacity=55)

# --- captions ---------------------------------------------------------------------
d.text("ATTESTATION MOLE", "Name", x=500, y=930, size=58,
       font="Virelai Sans", color="#EAD9BC", justify="center")
r = d.text("CERTIFIES THE UNSEEABLE", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#B49E7E", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("248.attestation-mole-V1R00")
