#!/usr/bin/env python3
"""Tabby Fields — mascot portrait V1R00.
Mouse field-inspector over a tilted spreadsheet, clipboard in one paw,
red marking pen in the other, color-coded sticky notes piled nearby.
Merged cells circled in red where found. 1000x1000.
Gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Tabby Fields — Mascot Portrait", 1000, 1000)

INK = "#2E2420"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#161410"}, {"offset": 1, "color": "#0A0806"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#7A8A6A"}, {"offset": 0.7, "color": "#58654C"},
    {"offset": 1, "color": "#333D2C"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3A3F30"}, {"offset": 1, "color": "#1C2016"}]}}
FUR_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#D8C4B2"}, {"offset": 0.7, "color": "#AE927C"},
    {"offset": 1, "color": "#7C6252"}]}}
SHEET_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#EFEAD8"}, {"offset": 1, "color": "#D8D2BC"}]}}
BOARD_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#8A6248"}, {"offset": 1, "color": "#5E412E"}]}}
RED = "#C84444"
PEN_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#D85A5A"}, {"offset": 1, "color": "#8E2E2E"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#8A9678", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8E0C8", strokeWidth=3, opacity=35)
for i, (x, y, w) in enumerate([(190,240,8),(802,234,7),(152,522,9),(842,540,8),
                               (254,768,7),(748,754,9),(130,392,6),(864,398,7),
                               (390,110,7),(618,112,8),(338,822,6),(664,824,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#4E5A44", opacity=50, stroke=NONE)

# --- floor ----------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#141810",
       strokeWidth=4, opacity=70)

# --- the spreadsheet: trapezoid lying on the floor, perspective grid --------------
# top edge y=560 x[230..770], bottom edge y=700 x[180..820]
d.path("M230,560 L770,560 L820,700 L180,700 Z", "Sheet",
       fill=SHEET_GRAD, stroke=INK, strokeWidth=5, join="round")
d.path("M230,560 L770,560 L820,700 L180,700 Z", "Sheet shade",
       fill="#8A8468", opacity=15, stroke=NONE)
# column lines fanning out
for i in range(1, 10):
    xt = 230 + i * 54
    xb = 180 + i * 64
    d.path(f"M{xt},560 L{xb},700", f"Col {i}", fill=NONE,
           stroke="#9A9478", strokeWidth=1.5, opacity=80)
# row lines: interpolate between top and bottom edge x-positions
for j, t in enumerate([0.22, 0.45, 0.68, 0.88]):
    y = 560 + t * 140
    xl = 230 - t * 50
    xr = 770 + t * 50
    d.path(f"M{xl:.0f},{y:.0f} L{xr:.0f},{y:.0f}", f"Row {j+1}", fill=NONE,
           stroke="#9A9478", strokeWidth=1.5, opacity=80)
# header band
d.path("M230,560 L770,560 L774,568 L226,568 Z", "Sheet header",
       fill="#C8C2A4", stroke=NONE)
d.text("FIELD-AUDIT.CSV", "Sheet title", x=246, y=578, size=11,
       font="Virelai Sans", color="#6E6850", justify="left")
# the crime scene, kept in the visible strips either side of the body:
# a merged cell block on the left, circled in red
d.path("M216,592 L336,588 L342,618 L220,622 Z", "Merged cell",
       fill="#E4DCC4", stroke="#8A8468", strokeWidth=2)
d.text("CNTRD", "Merged txt", x=278, y=611, size=9,
       font="Virelai Sans", color="#8A3040", justify="center")
d.path("M210,586 C240,576 316,576 344,588 C350,604 338,626 296,630 "
       "C246,634 206,626 206,608 C206,598 208,590 210,586 Z",
       "Red circle", fill=NONE, stroke=RED, strokeWidth=4,
       cap="round", opacity=90)
# red strike through an invalid row + margin X, also left
d.path("M216,656 L336,650", "Red strike", fill=NONE, stroke=RED,
       strokeWidth=3.5, cap="round", opacity=85)
d.path("M224,668 L246,690 M246,668 L224,690", "Red X", fill=NONE,
       stroke=RED, strokeWidth=4.5, cap="round")
# a surviving valid row gets a green tick, right strip
d.path("M684,616 L694,626 L712,604", "Green tick", fill=NONE,
       stroke="#5E8A4E", strokeWidth=4.5, cap="round", join="round")

# --- sticky notes piled right -----------------------------------------------------
notes = [
    (742, 636, 52, -10, "#F0D878", "#C8B45A"),
    (788, 616, 48, 8, "#E8A8B8", "#C88494"),
    (726, 580, 46, 4, "#A8D8A0", "#84B07C"),
    (794, 664, 50, -6, "#F0D878", "#C8B45A"),
    (758, 690, 46, 12, "#A0C8E0", "#7AA4BC"),
]
for i, (cx, cy, s, rot, c, edge) in enumerate(notes):
    d.path(rot_rect_path(cx, cy, s, s, rot), f"Note {i+1}",
           fill=c, stroke=INK, strokeWidth=2.5, join="round")
    # curled corner + scribble
    d.path(rot_rect_path(cx + s*0.22, cy - s*0.14, s*0.45, 3, rot),
           f"Note {i+1} line", fill=edge, stroke=NONE)
    d.path(rot_rect_path(cx, cy + s*0.12, s*0.6, 3, rot),
           f"Note {i+1} line2", fill=edge, stroke=NONE, opacity=70)
d.shape("ellipse", "Notes shadow", x=712, y=688, width=140, height=16,
        fill="#141810", opacity=45, stroke=NONE)

# --- Tabby Fields ------------------------------------------------------------------
d.shape("ellipse", "Tabby shadow", x=370, y=682, width=280, height=24,
        fill="#141810", opacity=50, stroke=NONE)
# tail: slips out right, curls along the floor behind the notes
d.path("M610,640 C680,660 710,684 700,700", "Tail ink", fill=NONE,
       stroke=INK, strokeWidth=17, cap="round")
d.path("M610,640 C680,660 710,684 700,700", "Tail", fill=NONE,
       stroke="#A0846E", strokeWidth=11, cap="round")
# body pear
d.path("M500,470 C600,470 656,540 656,620 C656,676 590,700 500,700 "
       "C410,700 344,676 344,620 C344,540 400,470 500,470 Z",
       "Body", fill=FUR_GRAD, stroke=INK, strokeWidth=6, join="round")
# belly patch
d.shape("ellipse", "Belly", x=430, y=560, width=140, height=120,
        fill="#E8D8C4", opacity=55, stroke=NONE)
# ears: big rounds behind the head
for side, ex in [("L", 396), ("R", 588)]:
    d.shape("ellipse", f"Ear {side}", x=ex, y=282, width=92, height=92,
            fill=FUR_GRAD, stroke=INK, strokeWidth=5)
    d.shape("ellipse", f"Ear {side} inner", x=ex+16, y=300, width=60,
            height=58, fill="#D8A8A0", stroke=NONE, opacity=85)
# head
d.path("M500,330 C580,330 632,384 632,446 C632,500 574,534 500,534 "
       "C426,534 368,500 368,446 C368,384 420,330 500,330 Z",
       "Head", fill=FUR_GRAD, stroke=INK, strokeWidth=6, join="round")
d.shape("ellipse", "Head hi", x=414, y=356, width=70, height=40,
        fill="#FFFFFF", opacity=10, stroke=NONE)
# face: bright inspector eyes, twitchy nose, six whiskers
for side, ex in [("L", 442), ("R", 528)]:
    d.shape("ellipse", f"Eye {side}", x=ex, y=404, width=26, height=30,
            fill=INK, stroke=NONE)
    d.shape("ellipse", f"Glint {side}", x=ex+6, y=408, width=8, height=8,
            fill="#FFFFFF", opacity=90, stroke=NONE)
d.path("M492,462 L508,462 L500,474 Z", "Nose", fill="#B86A6A",
       stroke=INK, strokeWidth=2.5, join="round")
d.path("M500,474 C494,482 486,484 478,480 M500,474 C506,482 514,484 522,480",
       "Mouth", fill=NONE, stroke=INK, strokeWidth=3.5, cap="round")
for side, pts in [("L", [(478,458,404,446),(478,466,398,466),(480,474,404,486)]),
                  ("R", [(522,458,596,446),(522,466,602,466),(520,474,596,486)])]:
    for j, (x1, y1, x2, y2) in enumerate(pts):
        d.path(f"M{x1},{y1} L{x2},{y2}", f"Whisker {side}{j+1}", fill=NONE,
               stroke=INK, strokeWidth=2, cap="round", opacity=60)
d.shape("ellipse", "Cheek L", x=412, y=472, width=30, height=14,
        fill="#D89A8A", opacity=40, stroke=NONE)
d.shape("ellipse", "Cheek R", x=558, y=472, width=30, height=14,
        fill="#D89A8A", opacity=40, stroke=NONE)

# --- clipboard held against the chest -----------------------------------------------
d.path(rot_rect_path(500, 596, 150, 130, -3), "Clipboard",
       fill=BOARD_GRAD, stroke=INK, strokeWidth=5, join="round")
d.path(rot_rect_path(500, 598, 122, 100, -3), "Clip paper",
       fill="#EFEAD8", stroke=INK, strokeWidth=3, join="round")
d.path(rot_rect_path(500, 542, 44, 18, -3), "Clip", fill="#6E6E6E",
       stroke=INK, strokeWidth=3, join="round")
# ruled lines + red verdicts on the paper
for j, dy in enumerate([-26, -8, 10, 28]):
    d.path(rot_rect_path(500, 598+dy, 96, 2.5, -3), f"Clip rule {j+1}",
           fill="#A8A28A", stroke=NONE, opacity=80)
d.path("M452,584 L462,592 L474,578", "Clip tick", fill=NONE,
       stroke="#5E8A4E", strokeWidth=4, cap="round", join="round")
d.path("M448,614 L470,610", "Clip strike", fill=NONE, stroke=RED,
       strokeWidth=4, cap="round")
# paws gripping the board edges
d.shape("ellipse", "Paw L", x=404, y=560, width=34, height=28,
        fill=FUR_GRAD, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Paw R", x=566, y=556, width=34, height=28,
        fill=FUR_GRAD, stroke=INK, strokeWidth=4)
# the red marking pen in her right paw, diagonal and ready
d.path(rot_rect_path(606, 522, 12, 78, 38), "Pen body",
       fill=PEN_GRAD, stroke=INK, strokeWidth=3, join="round")
d.path(rot_rect_path(630, 486, 12, 16, 38), "Pen cap",
       fill="#6E2020", stroke=INK, strokeWidth=3, join="round")
d.path(rot_rect_path(584, 560, 8, 14, 38), "Pen tip",
       fill="#F0E0C8", stroke=INK, strokeWidth=2.5, join="round")
# feet poking under the body
d.shape("ellipse", "Foot L", x=416, y=686, width=52, height=22,
        fill=FUR_GRAD, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Foot R", x=532, y=686, width=52, height=22,
        fill=FUR_GRAD, stroke=INK, strokeWidth=4)

# --- captions ----------------------------------------------------------------------
d.text("TABBY FIELDS", "Name", x=500, y=930, size=58,
       font="Virelai Sans", color="#ECE8DA", justify="center")
r = d.text("MERGED CELLS ARE A CRIME AGAINST LEGIBILITY", "Role",
           x=500, y=968, size=21, font="Virelai Sans", color="#C0C8AE",
           justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=140)

d.finish("053.tabby-fields-V1R00")
