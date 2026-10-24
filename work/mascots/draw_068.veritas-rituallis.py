#!/usr/bin/env python3
"""Veritas Rituallis — mascot portrait V1R00.
A hooded seal-keeper pressing a cryptic compliance glyph into an open
audit ledger. She does not explain the correction; the mark is the whole
of the law. 1000x1000. Gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Veritas Rituallis — Mascot Portrait", 1000, 1000)

INK = "#3A2630"
BG_GRAD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000], "stops": [
    {"offset": 0, "color": "#140D0E"}, {"offset": 1, "color": "#080506"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#6E5258"}, {"offset": 0.7, "color": "#46323E"},
    {"offset": 1, "color": "#241C2A"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "start": [500, 700], "end": [500, 880], "stops": [
    {"offset": 0, "color": "#3A2C36"}, {"offset": 1, "color": "#1C141E"}]}}
ROBE_GRAD = {"gradient": {"kind": "linear", "start": [430, 390], "end": [430, 690], "stops": [
    {"offset": 0, "color": "#7E3E4C"}, {"offset": 1, "color": "#46222F"}]}}
HOOD_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#8E4A58"}, {"offset": 0.7, "color": "#63303E"},
    {"offset": 1, "color": "#3E1E2C"}]}}
FACE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F2E0C8"}, {"offset": 0.75, "color": "#DEC0A0"},
    {"offset": 1, "color": "#C09A80"}]}}
PAGE_GRAD = {"gradient": {"kind": "linear", "start": [670, 580], "end": [670, 700], "stops": [
    {"offset": 0, "color": "#F0E2BE"}, {"offset": 1, "color": "#D6C096"}]}}
WOOD_GRAD = {"gradient": {"kind": "linear", "start": [600, 500], "end": [600, 556], "stops": [
    {"offset": 0, "color": "#6E4A34"}, {"offset": 1, "color": "#3E2A20"}]}}
SEAL = "#B04040"
GOLD = "#C8A44E"

PCX, PCY, PR = 500, 460, 420

def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

def sigil(cx, cy, kind, color, w=2.5, op=None):
    """One cryptic compliance glyph. Three rites: dot-circle, diamond-bar,
    triad."""
    kw = {} if op is None else {"opacity": op}
    if kind == "dot-circle":
        d.shape("ellipse", "sigil ring", x=cx-7, y=cy-7, width=14, height=14,
                fill=NONE, stroke=color, strokeWidth=w, **kw)
        d.shape("ellipse", "sigil dot", x=cx-2, y=cy-2, width=4, height=4,
                fill=color, stroke=NONE, **kw)
    elif kind == "diamond-bar":
        d.path(f"M{cx},{cy-8} L{cx+8},{cy} L{cx},{cy+8} L{cx-8},{cy} Z",
               "sigil diamond", fill=NONE, stroke=color, strokeWidth=w,
               join="round", **kw)
        d.path(f"M{cx-6},{cy} L{cx+6},{cy}", "sigil bar", fill=NONE,
               stroke=color, strokeWidth=w, cap="round", **kw)
    else:  # triad
        d.path(f"M{cx},{cy-8} L{cx+7},{cy+6} L{cx-7},{cy+6} Z",
               "sigil tri", fill=NONE, stroke=color, strokeWidth=w,
               join="round", **kw)

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#C8A44E", opacity=6, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#8A6068", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C8A4AC", strokeWidth=3, opacity=30)
for i, (x, y, w) in enumerate([(196,236,8),(796,230,7),(158,514,9),(836,534,8),
                               (262,762,7),(742,748,9),(136,388,6),(858,392,7),
                               (388,112,7),(616,114,8),(346,816,6),(660,820,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#3E2A34", opacity=55, stroke=NONE)

# --- floor ---------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#120C12",
       strokeWidth=4, opacity=70)

# --- her halo: the legitimacy loop, recognized by itself ------------------------------
d.shape("ellipse", "Halo", x=318, y=182, width=224, height=224,
        fill=NONE, stroke=GOLD, strokeWidth=3, opacity=40)
# faint sigils she has already spoken, hanging in the air
for i, (sx, sy, k) in enumerate([(300, 380, "diamond-bar"),
                                 (280, 452, "dot-circle"),
                                 (312, 522, "triad")]):
    sigil(sx, sy, k, GOLD, w=2.5, op=45)

# --- the figure -----------------------------------------------------------------------
d.shape("ellipse", "Robe shadow", x=318, y=672, width=224, height=22,
        fill="#100A0E", opacity=55, stroke=NONE)
# robe
d.path("M349,392 C380,402 480,402 511,392 L537,682 L323,682 Z",
       "Robe", fill=ROBE_GRAD, stroke=INK, strokeWidth=6, join="round")
# robe folds
d.path("M385,430 C395,510 398,590 392,668", "Fold 1", fill=NONE,
       stroke="#34181F", strokeWidth=3, opacity=50)
d.path("M478,430 C470,510 468,590 474,668", "Fold 2", fill=NONE,
       stroke="#34181F", strokeWidth=3, opacity=50)
# sash: a band of office down the front, marked with her three rites
d.path("M417,398 L443,398 L452,682 L408,682 Z", "Sash",
       fill="#5E2A36", stroke=INK, strokeWidth=3, join="round")
sigil(430, 455, "dot-circle", GOLD, w=2, op=75)
sigil(430, 520, "diamond-bar", GOLD, w=2, op=75)
sigil(430, 585, "triad", GOLD, w=2, op=75)

# hood
d.path("M430,255 C488,255 516,298 514,358 L511,392 L349,392 L346,358 "
       "C344,298 372,255 430,255 Z", "Hood", fill=HOOD_GRAD,
       stroke=INK, strokeWidth=6, join="round")
# hood folds
d.path("M400,272 C388,300 384,330 388,360", "Hood fold L", fill=NONE,
       stroke="#34181F", strokeWidth=3, opacity=50)
d.path("M460,272 C472,300 476,330 472,360", "Hood fold R", fill=NONE,
       stroke="#34181F", strokeWidth=3, opacity=50)

# face in the hood's shade — serene, eyes lowered to the work
d.shape("ellipse", "Face", x=388, y=302, width=84, height=78,
        fill=FACE_GRAD, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Face shade", x=388, y=302, width=84, height=40,
        fill="#8E5E50", opacity=30, stroke=NONE)
d.path("M400,346 C406,353 416,353 422,346", "Eye L", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.path("M438,346 C444,353 454,353 460,346", "Eye R", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.path("M424,370 C428,372 432,372 436,370", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=3, cap="round")

# --- the stamping arm: a long sleeve reaching to the ledger ----------------------------
d.path("M490,430 C540,455 586,488 618,514 L604,548 C568,524 524,496 "
       "488,474 Z", "Sleeve", fill=ROBE_GRAD, stroke=INK, strokeWidth=5,
       join="round")
d.shape("ellipse", "Hand", x=600, y=526, width=26, height=20,
        fill=FACE_GRAD, stroke=INK, strokeWidth=4)
# the seal stamp, mid-press
st_h = d.shape("rectangle", "Stamp handle", x=606, y=522, width=18, height=52,
               radius=6, fill=WOOD_GRAD, stroke=INK, strokeWidth=3)
st_b = d.shape("rectangle", "Stamp base", x=586, y=572, width=52, height=15,
               radius=5, fill="#4A3226", stroke=INK, strokeWidth=3)

# --- the audit ledger, open on the floor -----------------------------------------------
d.shape("ellipse", "Book shadow", x=548, y=676, width=260, height=20,
        fill="#100A0E", opacity=55, stroke=NONE)
# left page
d.path("M555,600 C590,585 630,582 672,596 L672,690 C630,676 590,678 "
       "555,694 Z", "Page L", fill=PAGE_GRAD, stroke=INK, strokeWidth=4,
       join="round")
# right page
d.path("M672,596 C714,582 754,585 795,600 L795,694 C754,678 714,676 "
       "672,690 Z", "Page R", fill=PAGE_GRAD, stroke=INK, strokeWidth=4,
       join="round")
d.path("M672,596 L672,690", "Spine crease", fill=NONE, stroke="#A88E62",
       strokeWidth=3)
# log lines, each already marked except the fresh one under the stamp
for i in range(4):
    y0 = 616 + i * 17
    d.path(f"M570,{y0} L652,{y0-11}", f"Entry L{i+1}", fill=NONE,
           stroke="#8A765A", strokeWidth=2.5, opacity=70, cap="round")
for i in range(4):
    y0 = 616 + i * 17
    d.path(f"M688,{y0-11} L775,{y0+2}", f"Entry R{i+1}", fill=NONE,
           stroke="#8A765A", strokeWidth=2.5, opacity=70, cap="round")
# witness marks — the ledger's margin is her signature
sigil(580, 640, "dot-circle", SEAL, w=2, op=80)
sigil(580, 672, "diamond-bar", SEAL, w=2, op=80)
sigil(762, 630, "triad", SEAL, w=2, op=80)
sigil(762, 664, "dot-circle", SEAL, w=2, op=80)
# the fresh mark, still wet under the seal
sigil(612, 590, "diamond-bar", SEAL, w=3)

# --- captions ----------------------------------------------------------------------
d.text("VERITAS RITUALLIS", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#F0E0CE", justify="center")
r = d.text("KEEPER OF THE WITNESS MARK", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#C8A898", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("068.veritas-rituallis-V1R00")
