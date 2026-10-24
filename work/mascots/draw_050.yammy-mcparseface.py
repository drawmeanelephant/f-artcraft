#!/usr/bin/env python3
"""Yammy McParseface — mascot portrait V1R00. Frontmatter Interrogator.
A fragile yam-orange lump of a creature holding a translucent ruler
hard against the indentation of a YAML document — one key sits a space
too shallow, the ruler edge proves it, and Yammy is already sweating.
Sage-dark plate on a config-night backdrop. 1000x1000.
House style: gradients + translucent shading, never flat fills.
YAML glyphs in Source Sans 3. Plate = circle (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Yammy McParseface — Mascot Portrait", 1000, 1000)

INK = "#25200F"   # warm dark ink, never black
BG_GRAD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000], "stops": [
    {"offset": 0, "color": "#10160E"}, {"offset": 1, "color": "#060A05"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#7A8455"}, {"offset": 0.62, "color": "#4C5536"},
    {"offset": 1, "color": "#222917"}]}}
YAM_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F0B060"}, {"offset": 0.7, "color": "#D88A3C"},
    {"offset": 1, "color": "#A85E24"}]}}
SHEET_GRAD = {"gradient": {"kind": "linear", "start": [0, 240], "end": [0, 640], "stops": [
    {"offset": 0, "color": "#F2EDDA"}, {"offset": 0.7, "color": "#DFD6B8"},
    {"offset": 1, "color": "#C2B690"}]}}
RULER_GRAD = {"gradient": {"kind": "linear", "start": [430, 0], "end": [478, 0], "stops": [
    {"offset": 0, "color": "#F0C868"}, {"offset": 1, "color": "#C89838"}]}}
RED = "#D96A5A"
FADE = "#D8D0B0"

PCX, PCY, PR = 500, 460, 420

def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

def faint_text(t, label, opacity, **kw):
    r = d.text(t, label, **kw)
    if r and r.get("id"):
        d.cmd("object.setProps", f"{label} opacity", id=r["id"],
              opacity=opacity)

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#6E7A48", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#151A0C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#DCE4C0", strokeWidth=3, opacity=28)
d.shape("ellipse", "Patina 1", x=560, y=580, width=260, height=150,
        fill="#8A9460", opacity=16, stroke=NONE)
d.shape("ellipse", "Patina 2", x=200, y=230, width=240, height=150,
        fill="#333D20", opacity=32, stroke=NONE)
for i, (x, y, w) in enumerate([(222,342,5),(790,338,6),(182,545,5),(840,572,5),
                               (256,756,5),(730,760,6),(162,452,5),(848,645,5),
                               (432,134,5),(596,140,6),(336,166,4),(700,203,5),
                               (250,656,4),(658,716,5)]):
    assert on_disc(x, y, 12), (x, y)
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#EAEED2", opacity=28, stroke=NONE)
# faint yaml fragments drifting on the plate
for i, (t, x, y, s) in enumerate([("---", 215, 255, 22), ("key:", 780, 210, 20),
                                  ("---", 175, 640, 20), ("~", 805, 705, 26),
                                  ("- ", 610, 128, 20)]):
    assert on_disc(x, y, 20), (x, y)
    faint_text(t, f"Drift {i+1}", 25, x=x, y=y, size=s,
               font="Source Sans 3", color=FADE, justify="center")
# ghost arcs on the dark backdrop
d.path("M932,162 A100,100 0 0 0 852,72", "Ghost arc TR",
       fill=NONE, stroke="#7A8A50", strokeWidth=14, opacity=10, cap="round")
d.path("M78,778 A115,115 0 0 0 182,880", "Ghost arc BL",
       fill=NONE, stroke="#7A8A50", strokeWidth=10, opacity=8, cap="round")

# --- the YAML document ---------------------------------------------------------
d.shape("ellipse", "Doc shadow", x=420, y=640, width=340, height=38,
        fill="#080C05", opacity=42, stroke=NONE)
d.shape("rectangle", "Doc", x=430, y=235, width=310, height=410,
        radius=8, fill=SHEET_GRAD, stroke=INK, strokeWidth=5)
d.path("M710,250 L710,630 C710,636 706,640 700,640 L702,250 Z",
       "Doc shade R", fill="#A8946C", opacity=35, stroke=NONE)
d.path("M438,248 L732,248", "Doc top light",
       fill=NONE, stroke="#FFF9E8", strokeWidth=3, opacity=55, cap="round")

CODE = "#4E4630"
# frontmatter fence
d.text("---", "Fence open", x=455, y=276, size=18, font="Source Sans 3",
       color=CODE)
# yaml keys — level-1 at x=524, level-2 at x=576 (one em = 52pt of indent)
for j, (key, val, xx, yy) in enumerate([
        ("name:", "yammy", 524, 312),
        ("mood:", "fragile", 524, 344),
        ("config:", "", 524, 376),
        ("indent:", "sacred", 576, 408),
        ("tabs:", "forbidden", 576, 440)]):
    d.text(key, f"Key {j+1}", x=xx, y=yy, size=17, font="Source Sans 3",
           color=CODE)
    if val:
        d.text(val, f"Val {j+1}", x=xx + 92, y=yy, size=17,
               font="Source Sans 3", color="#8A7A56")
# THE violation: level-2 key sits one space shallow (x=561, not 576)
d.text("spaces:", "Bad key", x=561, y=472, size=17,
       font="Source Sans 3", color=RED)
d.text("unclear", "Bad val", x=653, y=472, size=17,
       font="Source Sans 3", color="#8A7A56")
# proper indent level ticks — dotted guides down the doc
for gx in (524, 576):
    d.path(f"M{gx},296 L{gx},500", f"Indent guide {gx}",
           fill=NONE, stroke="#A8986E", strokeWidth=1.5, dash=[2, 7],
           opacity=55)
# closing fence
d.text("...", "Fence close", x=470, y=560, size=18, font="Source Sans 3",
       color=CODE)
d.text("---", "Fence end", x=470, y=592, size=18, font="Source Sans 3",
       color=CODE)
# red squiggle under the bad indent gap
d.path("M561,482 C565,486 569,486 573,482 C577,486 581,486 585,482",
       "Squiggle", fill=NONE, stroke=RED, strokeWidth=2.5, cap="round")

# --- translucent ruler pressed against the indents ------------------------------
# vertical ruler spanning the code rows; its right edge = level-1 indent
d.shape("rectangle", "Ruler", x=456, y=290, width=52, height=230,
        radius=6, fill=RULER_GRAD, stroke=INK, strokeWidth=3.5,
        opacity=80)
for j, yy in enumerate(range(300, 516, 18)):
    ln = 14 if (yy - 300) % 54 == 0 else 8
    d.path(f"M{508 - ln},{yy} L508,{yy}", f"Tick {j+1}",
           fill=NONE, stroke=INK, strokeWidth=2, opacity=75)
# the level-2 guide segment the bad line misses, picked out in red
d.path("M576,458 L576,486", "True indent edge",
       fill=NONE, stroke=RED, strokeWidth=3, opacity=85)
# gap arrow: bad key's left edge → true indent guide
d.path("M556,494 C564,498 572,498 578,494 M578,494 L571,490 M578,494 L571,498",
       "Gap arrow", fill=NONE, stroke=RED, strokeWidth=2.5, cap="round",
       opacity=85)

# --- Yammy himself ----------------------------------------------------------------
d.shape("ellipse", "Yam shadow", x=150, y=756, width=280, height=40,
        fill="#080C05", opacity=45, stroke=NONE)
# feet — small rootlets
d.path("M230,742 C222,760 230,772 252,772 C270,772 276,762 272,750 Z",
       "Foot L", fill=YAM_GRAD, stroke=INK, strokeWidth=3.5)
d.path("M312,742 C320,760 312,772 290,772 C272,772 266,762 270,750 Z",
       "Foot R", fill=YAM_GRAD, stroke=INK, strokeWidth=3.5)
# lumpy yam body — wider at the bottom, pinched waist, knotty bumps
d.path("M272,468 C240,470 218,492 214,524 C190,540 178,580 184,640 "
       "C190,712 226,752 276,752 C326,752 360,712 366,644 "
       "C371,584 360,544 338,524 C336,492 310,466 272,468 Z",
       "Body", fill=YAM_GRAD, stroke=INK, strokeWidth=5)
# yam knots + shading
d.path("M330,540 C346,580 348,650 332,700 C344,650 342,586 330,548 Z",
       "Side shade", fill="#8A4E1E", opacity=38, stroke=NONE)
d.path("M198,560 C192,610 196,670 214,712", "Rim light",
       fill=NONE, stroke="#FAD09A", strokeWidth=4, opacity=45, cap="round")
d.shape("ellipse", "Knot 1", x=214, y=586, width=12, height=8,
        fill="#B26A28", opacity=55, stroke=NONE)
d.shape("ellipse", "Knot 2", x=322, y=650, width=14, height=9,
        fill="#B26A28", opacity=55, stroke=NONE)
d.shape("ellipse", "Knot 3", x=250, y=700, width=10, height=7,
        fill="#B26A28", opacity=50, stroke=NONE)
# sprout on top — one worried leaf
d.path("M272,468 C272,444 262,430 244,426 C256,440 258,454 256,468 Z",
       "Sprout stem", fill="#6A8A3E", stroke=INK, strokeWidth=2.5)
d.path("M244,426 C228,420 218,426 216,438 C230,440 240,436 244,426 Z",
       "Sprout leaf", fill="#7C9A48", stroke=INK, strokeWidth=2.5)

# face — tight, picky, one eye squinting down the ruler edge
d.path("M216,552 C228,546 244,546 254,552 C244,558 228,558 216,552 Z",
       "Eye L", fill="#FBF4E4", stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Pupil L", x=238, y=549, width=8, height=8,
        fill=INK, stroke=NONE)
# right eye squinted to a measuring slit
d.path("M296,550 C310,544 326,544 338,549", "Eye R slit",
       fill=NONE, stroke=INK, strokeWidth=4.5, cap="round")
d.path("M300,556 L334,554", "Eye R lower",
       fill=NONE, stroke=INK, strokeWidth=2.5, cap="round", opacity=70)
# raised picky brows, uneven
d.path("M214,528 C228,518 248,517 260,524", "Brow L",
       fill=NONE, stroke=INK, strokeWidth=3.5, cap="round")
d.path("M298,522 C312,516 328,516 340,521", "Brow R",
       fill=NONE, stroke=INK, strokeWidth=3, cap="round")
# small worried frown
d.path("M250,602 C262,594 284,594 296,602", "Frown",
       fill=NONE, stroke=INK, strokeWidth=4, cap="round")
# sweat drop — fragility under pressure
d.path("M352,560 C356,570 360,576 360,582 C360,590 354,594 348,592 "
       "C342,590 340,584 342,578 C344,572 348,566 352,560 Z",
       "Sweat", fill="#BEE0E8", stroke=INK, strokeWidth=2.5)

# left arm bracing the ruler's lower half
d.path("M190,620 C172,640 168,668 178,690 C190,696 202,688 202,676 "
       "C196,656 200,638 210,626 Z",
       "Arm L", fill=YAM_GRAD, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Hand L", x=172, y=678, width=28, height=26,
        fill="#D88A3C", stroke=INK, strokeWidth=3)
# right arm stretched up, hand pressing the ruler's top edge
d.path("M352,510 C382,498 408,482 424,462 C436,458 446,468 442,480 "
       "C428,502 402,522 374,534 Z",
       "Arm R", fill=YAM_GRAD, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Hand R", x=428, y=456, width=28, height=28,
        fill="#D88A3C", stroke=INK, strokeWidth=3)
# fingers gripping the ruler edge
d.path("M440,472 L452,480 M436,480 L448,488", "Grip fingers",
       fill=NONE, stroke=INK, strokeWidth=2.5, cap="round")

# --- name + role ----------------------------------------------------------------------
d.text("YAMMY MCPARSEFACE", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#EDE6C8", justify="center")
r = d.text("FRONTMATTER INTERROGATOR", "Role", x=500, y=968, size=22,
           font="Virelai Sans", color="#C6CE9C", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=140)

d.finish("050.yammy-mcparseface-V1R00")
