#!/usr/bin/env python3
"""Shelfmark Hollow — mascot portrait V1R00.
A tiny auditor in an eyeshade visor standing inside the dashed hollow a
missing book left between two neighbours on a full shelf, magnifier up.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Shelfmark Hollow — Mascot Portrait", 1000, 1000)

INK = "#3B2E26"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#161C16"}, {"offset": 1, "color": "#090C09"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#C4B493"}, {"offset": 0.7, "color": "#96805F"},
    {"offset": 1, "color": "#5C4A38"}]}}
WOOD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7A5B38"}, {"offset": 1, "color": "#4E3A24"}]}}
SKIN = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#EFD2B0"}, {"offset": 1, "color": "#C09A72"}]}}
COAT = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5C5648"}, {"offset": 1, "color": "#36302A"}]}}
PAPER = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F4F0E4"}, {"offset": 1, "color": "#D8D2BC"}]}}
GLASS = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#D8EFEF"}, {"offset": 1, "color": "#9AC4C6"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#6E5B42", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8DCC0", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(215,225,7),(778,215,6),(185,540,8),(812,545,7),
                               (255,755,7),(748,752,8),(390,125,7),(605,120,6),
                               (150,385,6),(852,390,7),(310,808,6),(680,806,7)]):
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#6E5B42", opacity=40, stroke=NONE)
d.shape("ellipse", "Patina 1", x=170, y=200, width=230, height=140,
        fill="#E8DCC0", opacity=10, stroke=NONE)
d.shape("ellipse", "Patina 2", x=600, y=560, width=260, height=150,
        fill="#3A2E22", opacity=12, stroke=NONE)

# --- the shelf -----------------------------------------------------------------
d.path("M228,690 L772,690 L764,734 L236,734 Z", "Shelf plank",
       fill=WOOD, stroke=INK, strokeWidth=6, join="round")
d.path("M232,692 L768,692", "Shelf top edge", fill=NONE,
       stroke="#C9A97A", strokeWidth=3, opacity=60)
# the auditor's pendant lamp, hanging over the scene
d.path("M500,120 L500,224", "Lamp cord", fill=NONE, stroke="#2E2118",
       strokeWidth=4, opacity=80)
d.path("M468,224 L532,224 L552,262 L448,262 Z", "Lamp shade",
       fill="#3A3226", stroke=INK, strokeWidth=5, join="round")
d.shape("ellipse", "Lamp bulb", x=488, y=258, width=24, height=20,
        fill="#F4DFA8", stroke=INK, strokeWidth=3, opacity=95)
d.shape("ellipse", "Lamp glow", x=380, y=262, width=240, height=90,
        fill="#F4DFA8", opacity=12, stroke=NONE)

# --- books, left of the hollow ---------------------------------------------------
def book(x, w, h, color, bands, label):
    y = 690 - h
    d.shape("ellipse", f"{label} shadow", x=x-4, y=686, width=w+8, height=9,
            fill="#2E2118", opacity=40, stroke=NONE)
    d.shape("rectangle", label, x=x, y=y, width=w, height=h, radius=5,
            fill=color, stroke=INK, strokeWidth=5)
    for i, by in enumerate(bands):
        d.path(f"M{x+4},{y+by} L{x+w-4},{y+by}", f"{label} band {i+1}",
               fill=NONE, stroke="#E8DCC0", strokeWidth=4, opacity=55)
    d.path(f"M{x+8},{y+h-26} L{x+w-8},{y+h-26} M{x+8},{y+h-16} L{x+w-14},{y+h-16}",
           f"{label} title", fill=NONE, stroke="#E8DCC0", strokeWidth=3, opacity=40)

book(250, 44, 205, "#8A4A42", [24, 38], "Book L1")
book(298, 38, 190, "#5A6480", [26], "Book L2")
book(340, 46, 220, "#4E6B58", [28, 42], "Book L3")
book(390, 36, 178, "#9A7A44", [22], "Book L4")
book(430, 34, 195, "#7A5A6E", [24, 36], "Book L5")

# --- books, right of the hollow --------------------------------------------------
book(676, 44, 200, "#4E6B58", [26, 40], "Book R2")
book(724, 38, 185, "#8A4A42", [24], "Book R3")
# the leaner: right-hand neighbour tipping into the gap
d.path(rot_rect_path(642, 588, 42, 204, -14), "Book R1 lean",
       fill="#9A7A44", stroke=INK, strokeWidth=5, join="round")
d.path(rot_rect_path(642, 588, 42, 204, -14), "Book R1 lean shade",
       fill="#3A2E22", stroke=NONE, opacity=25)
d.shape("ellipse", "Lean shadow", x=612, y=686, width=68, height=9,
        fill="#2E2118", opacity=40, stroke=NONE)

# --- the hollow: ghost outline of the missing book --------------------------------
# dark void where the tome should be
d.path("M452,448 C452,438 458,432 468,432 L594,432 C604,432 610,438 610,448 "
       "L610,690 L452,690 Z", "Hollow void", fill="#2E2118", opacity=14, stroke=NONE)
# its remembered outline, dashed
d.path("M452,448 C452,438 458,432 468,432 L594,432 C604,432 610,438 610,448 "
       "L610,690 L452,690 Z", "Hollow ghost",
       fill=NONE, stroke="#F0E6CC", strokeWidth=5,
       dash=[16, 10], cap="round", opacity=75)
# a bookmark ribbon left inside the hollow
d.path("M540,432 L540,482 L550,472 L560,482 L560,432 Z", "Hollow ribbon",
       fill="#8A4A42", opacity=60, stroke=INK, strokeWidth=3)
# MISSING tag pinned to the shelf front under the gap
d.path(rot_rect_path(522, 712, 76, 28, 3), "Missing tag",
       fill=PAPER, stroke=INK, strokeWidth=3, opacity=95)
d.shape("ellipse", "Tag pin", x=518, y=700, width=8, height=8,
        fill="#8A3444", stroke=INK, strokeWidth=2)
d.text("MISSING", "Tag text", x=522, y=717, size=10, font="Virelai Sans",
       color="#8A3444", justify="center")
# dust motes drifting in the gap
for i, (x, y, w) in enumerate([(470,560,10),(592,606,8),(478,640,7),(580,656,9),(530,600,6)]):
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#F4EFDA", opacity=20, stroke=NONE)

# --- the auditor -------------------------------------------------------------------
d.shape("ellipse", "Auditor shadow", x=452, y=684, width=128, height=13,
        fill="#2E2118", opacity=50, stroke=NONE)
# body: waistcoat robe down to the shelf
d.path("M508,575 C552,575 574,616 578,658 L582,690 L436,690 L440,658 "
       "C444,616 464,575 508,575 Z", "Robe", fill=COAT, stroke=INK,
       strokeWidth=6, join="round")
# shirt front + buttons
d.path("M496,579 L512,579 L506,627 Z", "Shirt front", fill="#E8DCC0",
       stroke=INK, strokeWidth=3, opacity=95)
for i, y in enumerate([637, 655]):
    d.shape("ellipse", f"Button {i+1}", x=501, y=y, width=8, height=8,
            fill="#C9A97A", stroke=INK, strokeWidth=2)
# left arm down to the clipboard
d.path("M458,597 C438,611 428,629 424,649", "Arm L", fill=NONE,
       stroke=COAT, strokeWidth=20, cap="round")
d.shape("ellipse", "Hand L", x=408, y=639, width=26, height=22, fill=SKIN,
        stroke=INK, strokeWidth=4)
# clipboard with the audit sheet
d.path(rot_rect_path(396, 615, 64, 86, -8), "Clipboard",
       fill="#6E5B42", stroke=INK, strokeWidth=4, join="round")
d.path(rot_rect_path(396, 617, 52, 70, -8), "Clip sheet",
       fill=PAPER, stroke=INK, strokeWidth=3)
d.shape("rectangle", "Clip", x=384, y=563, width=26, height=12, radius=4,
        fill="#9A9482", stroke=INK, strokeWidth=3)
for i in range(3):
    d.path(f"M{374+i*2},{609+i*14} L{412-i*4},{605+i*14}", f"Clip line {i+1}",
           fill=NONE, stroke="#A89E84", strokeWidth=4, cap="round", opacity=85)
# right arm out holding the magnifier into the hollow
d.path("M560,597 C580,593 594,583 604,567", "Arm R", fill=NONE,
       stroke=COAT, strokeWidth=20, cap="round")
d.shape("ellipse", "Hand R", x=592, y=553, width=26, height=22, fill=SKIN,
        stroke=INK, strokeWidth=4)
d.path("M604,567 L622,543", "Lens handle", fill=NONE, stroke=INK,
       strokeWidth=8, cap="round")
d.shape("ellipse", "Lens glass", x=596, y=481, width=62, height=62,
        fill=GLASS, stroke=INK, strokeWidth=6, opacity=55)
d.path("M606,497 C612,489 622,485 632,487", "Lens glint", fill=NONE,
       stroke="#FFFFFF", strokeWidth=5, cap="round", opacity=70)
# head
d.shape("ellipse", "Head", x=462, y=463, width=92, height=92, fill=SKIN,
        stroke=INK, strokeWidth=6)
# eyeshade visor: translucent green bill across the brow
d.path("M452,497 C452,481 476,471 508,471 C540,471 564,481 564,497 "
       "C564,505 540,509 508,509 C476,509 452,505 452,497 Z",
       "Visor bill", fill="#2A5A46", stroke=INK, strokeWidth=4, opacity=88)
d.path("M460,491 C480,479 536,479 556,491", "Visor sheen", fill=NONE,
       stroke="#7AB89A", strokeWidth=4, cap="round", opacity=70)
# face under the visor: concentrated eyes + small frown
d.shape("ellipse", "Eye L", x=482, y=519, width=16, height=18, fill="#FBF6E8",
        stroke=INK, strokeWidth=3)
d.shape("ellipse", "Eye R", x=518, y=519, width=16, height=18, fill="#FBF6E8",
        stroke=INK, strokeWidth=3)
d.shape("ellipse", "Pupil L", x=487, y=524, width=7, height=8, fill=INK, stroke=NONE)
d.shape("ellipse", "Pupil R", x=523, y=524, width=7, height=8, fill=INK, stroke=NONE)
d.path("M490,541 C498,537 518,537 526,541", "Frown", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")

# --- captions ------------------------------------------------------------------
d.text("SHELFMARK HOLLOW", "Name", x=500, y=930, size=56, font="Virelai Sans",
       color="#EADFC4", justify="center")
r = d.text("AUDITOR OF MISSING VOLUMES", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#B29A76", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("416.shelfmark-hollow-V1R00")
