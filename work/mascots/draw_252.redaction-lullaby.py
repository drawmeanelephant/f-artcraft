#!/usr/bin/env python3
"""Redaction Lullaby — mascot portrait V1R00.
A small wisp perched on a document sings it to sleep; the page is covered
in thick redaction bars laid plumb across the paragraph. 1000x1000.
Gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Redaction Lullaby — Mascot Portrait", 1000, 1000)

INK = "#2A1E20"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#171019"}, {"offset": 1, "color": "#0A060C"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#7A6A7E"}, {"offset": 0.7, "color": "#574A5E"},
    {"offset": 1, "color": "#322A38"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4E3A30"}, {"offset": 1, "color": "#241812"}]}}
PAGE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#EFE4CC"}, {"offset": 1, "color": "#C9B996"}]}}
BACK_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#D8CBB0"}, {"offset": 1, "color": "#A89878"}]}}
WISP_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#D8D2EC"}, {"offset": 0.7, "color": "#A29AC4"},
    {"offset": 1, "color": "#6E6794"}]}}
BAR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2C2224"}, {"offset": 1, "color": "#181114"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#9A88A0", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E2D6E4", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(193,234,8),(801,229,7),(157,526,9),(837,544,8),
                               (246,766,7),(754,748,9),(133,394,6),(865,389,7),
                               (391,112,7),(613,109,8),(333,824,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#4A3E50", opacity=45, stroke=NONE)

# --- crescent moon, upper right (inside the rim) ---------------------------------
d.shape("ellipse", "Moon", x=712, y=177, width=76, height=76,
        fill="#F0E4C8", opacity=90, stroke=NONE)
d.shape("ellipse", "Moon cut", x=694, y=165, width=74, height=74,
        fill="#463D4D", stroke=NONE)
d.shape("ellipse", "Moon halo", x=702, y=167, width=96, height=96,
        fill="#F0E4C8", opacity=10, stroke=NONE)

# --- floor ---------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#160E0A",
       strokeWidth=4, opacity=70)

# --- the document: back sheet tilted, front page plumb -----------------------------
d.shape("ellipse", "Page shadow", x=330, y=690, width=400, height=24,
        fill="#0E0806", opacity=45, stroke=NONE)
d.path(rot_rect_path(572, 505, 360, 400, 4), "Back sheet",
       fill=BACK_GRAD, stroke=INK, strokeWidth=4)
d.shape("rectangle", "Page", x=360, y=330, width=360, height=390,
        fill=PAGE_GRAD, stroke=INK, strokeWidth=5)
# page header rule + faded stamp
d.path("M390,368 L690,368 M390,378 L560,378", "Header rule", fill=NONE,
       stroke="#8A7A60", strokeWidth=4, opacity=70)
d.shape("ellipse", "Stamp ring", x=640, y=345, width=58, height=58,
        fill=NONE, stroke="#A86A5A", strokeWidth=3.5, opacity=45)
d.shape("ellipse", "Stamp core", x=657, y=362, width=24, height=24,
        fill="#A86A5A", opacity=30, stroke=NONE)
# rows: thin surviving text lines alternating with thick plumb bars
rows = [("t", 400, 300), ("b", 432, 296), ("t", 464, 264), ("b", 496, 300),
        ("t", 528, 240), ("b", 560, 288), ("t", 592, 272), ("b", 624, 300),
        ("t", 656, 232)]
for i, (kind, y, w) in enumerate(rows):
    if kind == "t":
        d.shape("rectangle", f"Text line {i}", x=390, y=y, width=w, height=7,
                fill="#9A8E76", opacity=80, stroke=NONE, radius=3)
    else:
        d.shape("rectangle", f"Bar {i}", x=390, y=y-5, width=w, height=19,
                fill=BAR_GRAD, stroke="#120C0E", strokeWidth=2, radius=4)
        d.shape("rectangle", f"Bar sheen {i}", x=394, y=y-3, width=w-8,
                height=4, fill="#5E525A", opacity=35, stroke=NONE, radius=2)

# --- the singer: a plump wisp perched on the page's top edge -----------------------
d.shape("ellipse", "Wisp halo", x=340, y=140, width=250, height=220,
        fill="#CFCAE6", opacity=10, stroke=NONE)
# tail curl behind the body
d.path("M505,300 C540,300 558,318 552,342 C546,360 528,366 516,358 "
       "C530,352 536,338 528,326 C522,316 512,310 502,308 Z",
       "Tail curl", fill=WISP_GRAD, stroke=INK, strokeWidth=4, opacity=90)
# body, bottom edge resting on the page top (y=330)
d.path("M450,228 C508,228 536,268 532,306 C529,326 520,332 505,332 "
       "L395,332 C380,332 371,324 368,306 C363,268 392,228 450,228 Z",
       "Wisp body", fill=WISP_GRAD, stroke=INK, strokeWidth=6, opacity=94)
d.shape("ellipse", "Wisp highlight", x=390, y=245, width=90, height=36,
        fill="#FFFFFF", opacity=20, stroke=NONE)
d.path("M385,318 C410,328 490,328 515,318 C490,324 410,324 385,318 Z",
       "Wisp shade", fill="#5A5480", opacity=45, stroke=NONE)
# feet gripping the page edge
d.path("M415,332 L415,344 M485,332 L485,344", "Feet", fill=NONE,
       stroke="#6E6794", strokeWidth=5, cap="round")
# open beak, singing up-left toward the notes
d.path("M372,262 L340,246 L366,282 Z", "Beak open", fill="#E8C87A",
       stroke=INK, strokeWidth=4)
# closed, contented eye
d.path("M420,272 C428,266 438,266 446,272", "Eye", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
# cheek blush of sleep
d.shape("ellipse", "Blush", x=448, y=288, width=26, height=14,
        fill="#C48A9A", opacity=40, stroke=NONE)
# folded wing
d.path("M465,300 C495,295 512,306 514,322 C496,318 478,312 465,300 Z",
       "Wing", fill="#8F89B0", stroke=INK, strokeWidth=4, opacity=85)

# --- the lullaby: notes whose heads are little redaction bars -----------------------
def note(cx, cy, label, op):
    d.path(rot_rect_path(cx, cy, 26, 15, -18), f"{label} head",
           fill=BAR_GRAD, stroke=INK, strokeWidth=2.5, opacity=op)
    d.path(f"M{cx+11},{cy-6} L{cx+11},{cy-44} "
           f"C{cx+20},{cy-40} {cx+26},{cy-34} {cx+28},{cy-24}",
           f"{label} stem", fill=NONE, stroke="#E8DDF0",
           strokeWidth=4, cap="round", opacity=op)
note(340, 225, "Note 1", 90)
note(300, 192, "Note 2", 75)
note(266, 163, "Note 3", 55)
# drifting hush motes
for i, (x, y, w) in enumerate([(620,250,5),(660,290,6),(590,210,4),(700,330,5),
                               (300,420,5),(250,470,6),(760,420,5)]):
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#E2D6E4", opacity=35, stroke=NONE)

# --- captions ---------------------------------------------------------------------
d.text("REDACTION LULLABY", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#EDE4F2", justify="center")
r = d.text("BEDSIDE MANNER FOR DELETED HISTORY", "Role", x=500, y=968,
           size=23, font="Virelai Sans", color="#B8A8C0", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("252.redaction-lullaby-V1R00")
