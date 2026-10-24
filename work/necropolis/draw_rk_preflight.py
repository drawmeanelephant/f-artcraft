#!/usr/bin/env python3
"""rc-preflight.sh — The Lamp Check. Necropolis plate V1R00.
A sexton at the locked gates before opening, mid lamp-ritual: one small
flame cupped in his hands, the Oliver lantern waiting at his feet, the
whole necropolis dark behind him holding its breath for the verdict —
is it present, does it light, does it burn the right color? 1000x1000.
Gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("RC-Preflight — Necropolis Plate", 1000, 1000)

INK = "#161220"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#0C0914"}, {"offset": 1, "color": "#050308"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#3A3350"}, {"offset": 0.7, "color": "#1E1A30"},
    {"offset": 1, "color": "#0C0A16"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#221C30"}, {"offset": 1, "color": "#0E0B16"}]}}
IRON = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3A3450"}, {"offset": 1, "color": "#1C1830"}]}}
IRON_DK = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2A2640"}, {"offset": 1, "color": "#141124"}]}}
ROBE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2A2340"}, {"offset": 1, "color": "#130F20"}]}}
SKIN = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#C8A882"}, {"offset": 1, "color": "#8A6248"}]}}
FLAME = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F0B45A"}, {"offset": 1, "color": "#B8641E"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#5A5272", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C8C4D8", strokeWidth=3, opacity=40)
for i, (x, y, w) in enumerate([(193,233,8),(801,230,7),(157,524,9),(837,544,8),
                               (247,766,7),(753,749,9),(133,393,6),(864,391,7),
                               (391,113,7),(613,110,8),(333,823,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#4A4462", opacity=35, stroke=NONE)
# pinprick stars over the sleeping necropolis
for i, (x, y, w) in enumerate([(300,178,4),(688,148,3),(436,122,3),(762,258,4),
                               (242,302,3),(560,168,3)]):
    d.shape("ellipse", f"Star {i+1}", x=x, y=y, width=w, height=w,
            fill="#D8CCB0", opacity=35, stroke=NONE)

# --- flanking walls -------------------------------------------------------------
d.path("M140,700 L140,438 L310,438 L310,700 Z", "Wall L", fill="#0D0A14",
       stroke="#241E33", strokeWidth=4, join="round")
d.path("M136,438 L314,438 L314,452 L136,452 Z", "Coping L", fill="#1A1626",
       stroke=INK, strokeWidth=3, join="round")
d.path("M690,700 L690,438 L845,438 L845,700 Z", "Wall R", fill="#0D0A14",
       stroke="#241E33", strokeWidth=4, join="round")
d.path("M686,438 L849,438 L849,452 L686,452 Z", "Coping R", fill="#1A1626",
       stroke=INK, strokeWidth=3, join="round")

# --- tombstones waiting in the gloom behind the bars ------------------------------
d.shape("ellipse", "Back gloom", x=330, y=520, width=360, height=190,
        fill="#080611", opacity=55, stroke=NONE)
for i, (x, top, w, h) in enumerate([(372,596,48,100),(542,612,44,84),
                                    (618,580,54,116)]):
    d.path(f"M{x},{top+h} L{x},{top+14} C{x},{top} {x+w},{top} {x+w},{top+14} "
           f"L{x+w},{top+h} Z", f"Stone {i+1}", fill="#0F0D18", opacity=75,
           stroke="#1E1A2C", strokeWidth=3)

# --- the locked gates --------------------------------------------------------------
# posts + finials
for side, px in [("L", 310), ("R", 652)]:
    d.path(f"M{px},700 L{px},200 L{px+38},200 L{px+38},700 Z", f"Post {side}",
           fill=IRON, stroke=INK, strokeWidth=4, join="round")
    d.path(f"M{px+6},200 L{px+19},168 L{px+32},200 Z", f"Finial {side}",
           fill=IRON_DK, stroke=INK, strokeWidth=3, join="round")
# rails
d.path("M348,240 L652,240 L652,258 L348,258 Z", "Rail top", fill=IRON_DK,
       stroke=INK, strokeWidth=3, join="round")
d.path("M348,618 L652,618 L652,636 L348,636 Z", "Rail low", fill=IRON_DK,
       stroke=INK, strokeWidth=3, join="round")
# bars
for i, bx in enumerate([372, 408, 444, 480, 516, 552, 588, 624]):
    d.path(f"M{bx-5},258 L{bx-5},695 L{bx+5},695 L{bx+5},258 Z", f"Bar {i+1}",
           fill=IRON_DK, stroke="#0C0A14", strokeWidth=2, join="round")
    d.path(f"M{bx-5},258 L{bx},240 L{bx+5},258 Z", f"Bar spike {i+1}",
           fill=IRON_DK, stroke="#0C0A14", strokeWidth=2, join="round")
# the chain, sagging and locked — the lock hangs off-center, clear of the sexton
d.path("M348,436 C420,468 580,468 652,436", "Chain", fill=NONE,
       stroke="#3E3A52", strokeWidth=7)
d.path("M398,476 C398,456 430,456 430,476", "Padlock shackle", fill=NONE,
       stroke="#4A4462", strokeWidth=6)
d.path("M394,476 L434,476 L434,518 L394,518 Z", "Padlock", fill=IRON,
       stroke=INK, strokeWidth=4, join="round")
d.shape("ellipse", "Keyhole", x=410, y=490, width=8, height=10,
        fill="#0C0A14", stroke=NONE)

# --- floor ----------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0A0810",
       strokeWidth=4, opacity=70)
d.shape("ellipse", "Sexton shadow", x=420, y=684, width=170, height=18,
        fill="#030208", opacity=60, stroke=NONE)

# --- the verdict's glow, thrown ahead of the flame -------------------------------
d.shape("ellipse", "Glow wide", x=330, y=390, width=340, height=330,
        fill="#E8A44A", opacity=10, stroke=NONE)
d.shape("ellipse", "Glow mid", x=415, y=470, width=170, height=210,
        fill="#E8A44A", opacity=13, stroke=NONE)
d.shape("ellipse", "Floor pool", x=415, y=660, width=180, height=44,
        fill="#E8A44A", opacity=13, stroke=NONE)

# --- the Oliver lantern at his feet ------------------------------------------------
d.path("M606,614 C606,600 622,600 622,614", "Lantern ring", fill=NONE,
       stroke="#4A4462", strokeWidth=5)
d.path("M594,632 L600,616 L628,616 L634,632 Z", "Lantern cap", fill=IRON,
       stroke=INK, strokeWidth=3, join="round")
d.path("M596,632 L632,632 L630,678 L598,678 Z", "Lantern body", fill=IRON_DK,
       stroke=INK, strokeWidth=3, join="round")
d.path("M602,638 L626,638 L625,672 L603,672 Z", "Lantern glass",
       fill="#2A2418", stroke="#0C0A14", strokeWidth=2)
# the right color: a small amber heart already lit inside
d.path("M614,668 C609,663 609,655 613,649 C614,652 616,654 617,655 "
       "C620,651 620,657 619,661 C618,665 616,668 614,668 Z",
       "Lantern flamelet", fill=FLAME, opacity=85, stroke=NONE)
d.shape("ellipse", "Lantern glow", x=596, y=636, width=36, height=44,
        fill="#E8A44A", opacity=18, stroke=NONE)
d.path("M592,678 L636,678 L636,692 L592,692 Z", "Lantern base", fill=IRON,
       stroke=INK, strokeWidth=3, join="round")
# the engine's little cog stamped on the base
d.shape("ellipse", "Oliver cog", x=607, y=681, width=14, height=9,
        fill=NONE, stroke="#6A5A42", strokeWidth=2)

# --- the sexton, cupping the test flame ---------------------------------------------
# robe
d.path("M455,498 C440,505 432,525 430,555 L424,690 L578,690 L572,552 "
       "C570,522 562,504 546,497 C530,489 470,490 455,498 Z", "Robe",
       fill=ROBE, stroke=INK, strokeWidth=5, join="round")
# flame-light caught on the robe front
d.path("M474,548 C468,580 465,630 467,688 L534,688 C536,632 534,582 528,548 "
       "C514,540 488,540 474,548 Z", "Robe lit front", fill="#E8A44A",
       opacity=11, stroke=NONE)
# hem fold lines
d.path("M450,690 C452,650 456,610 462,575 M552,690 C550,652 546,612 540,576",
       "Robe folds", fill=NONE, stroke="#0C0A16", strokeWidth=4, opacity=60)
# head in the hood, face lit from below by the flame
d.shape("ellipse", "Face", x=480, y=426, width=40, height=46,
        fill=SKIN, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Face uplight", x=487, y=444, width=26, height=24,
        fill="#F0B45A", opacity=28, stroke=NONE)
d.path("M472,448 C468,418 486,404 500,404 C514,404 532,418 528,448 L528,454 "
       "C520,438 510,434 500,434 C490,434 480,438 472,454 Z", "Hood",
       fill=ROBE, stroke=INK, strokeWidth=4, join="round")
d.shape("ellipse", "Eye L", x=490, y=448, width=5, height=5,
        fill="#241812", stroke=NONE)
d.shape("ellipse", "Eye R", x=505, y=448, width=5, height=5,
        fill="#241812", stroke=NONE)
d.path("M493,464 C497,462 503,462 507,464", "Mouth", fill=NONE,
       stroke="#5A3A28", strokeWidth=3, cap="round")
# arms converging to the cupped hands
d.path("M462,512 C478,536 486,554 491,570", "Arm L", fill=NONE,
       stroke="#241E33", strokeWidth=14, cap="round")
d.path("M538,512 C524,536 515,554 509,570", "Arm R", fill=NONE,
       stroke="#241E33", strokeWidth=14, cap="round")
# cupped hands: a bowl for the flame
d.shape("ellipse", "Palm L", x=479, y=564, width=20, height=13,
        fill=SKIN, stroke=INK, strokeWidth=3)
d.shape("ellipse", "Palm R", x=500, y=564, width=20, height=13,
        fill=SKIN, stroke=INK, strokeWidth=3)
d.path("M483,576 C490,582 510,582 517,575", "Cup line", fill=NONE,
       stroke="#8A6248", strokeWidth=3, cap="round")
# the test flame, burning the right color
d.path("M500,572 C488,562 486,546 496,530 C498,526 500,522 501,517 "
       "C504,524 508,529 511,536 C517,548 512,564 502,572 Z",
       "Flame outer", fill=FLAME, stroke="#7A3A10", strokeWidth=2, join="round")
d.path("M500,566 C495,560 494,551 499,542 C500,539 501,536 502,533 "
       "C507,541 507,554 503,563 Z", "Flame core", fill="#F5DFA8", stroke=NONE)
d.shape("ellipse", "Flame glow", x=468, y=505, width=64, height=72,
        fill="#F0B45A", opacity=22, stroke=NONE)

# --- captions ------------------------------------------------------------------
d.text("RC-PREFLIGHT", "Name", x=500, y=930, size=56, font="Virelai Sans",
       color="#E2DED2", justify="center")
r = d.text("THE LAMP RITUAL", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#A8A2BC", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("rk-preflight-V1R00")
