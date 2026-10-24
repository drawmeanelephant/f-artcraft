#!/usr/bin/env python3
"""404Sy McLostalot — mascot portrait V1R00.
A lost mascot in a jacket stitched from breadcrumb trails, holding an
upside-down map, dead ends on every side. Guidance system failure.
1000x1000. Gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("404Sy McLostalot — Mascot Portrait", 1000, 1000)

INK = "#28222A"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#171A22"}, {"offset": 1, "color": "#090B10"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4C4858"}, {"offset": 0.7, "color": "#2E2A3A"},
    {"offset": 1, "color": "#171420"}]}}
COAT = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#8E7842"}, {"offset": 1, "color": "#5A4826"}]}}
COAT_DK = "#4A3A20"
FACE = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F2E4C4"}, {"offset": 1, "color": "#D8BF96"}]}}
MAP = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F0E6CC"}, {"offset": 1, "color": "#D6C8A2"}]}}
WOOD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7A5C3E"}, {"offset": 1, "color": "#4E3822"}]}}
NOPE = "#C23A2E"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#6A6478", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#DCD4E8", strokeWidth=3, opacity=45)
for i, (x, y, w) in enumerate([(193,232,8),(800,234,7),(158,522,9),(835,542,8),
                               (245,768,7),(755,746,9),(132,392,6),(862,394,7),
                               (390,110,7),(614,112,8),(332,824,6),(666,818,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#423C50", opacity=45, stroke=NONE)

# faint maze corner stubs — the path has already ended twice behind him
for i, (x, y, s) in enumerate([(180, 560, 1), (700, 300, -1)]):
    d.path(f"M{x},{y} h{120*s} M{x},{y} v-110", f"Maze corner {i+1}",
           fill=NONE, stroke="#554E66", strokeWidth=10, opacity=35,
           cap="round")

# --- ground: a path that forks into dead ends ------------------------------------
d.shape("ellipse", "Ground", x=230, y=690, width=540, height=90,
        fill="#1E1A28", opacity=80, stroke=NONE)
# two stubs flanking the figure, each ending in a big X — dead ends both ways
for s in (-1, 1):
    x1 = 500 + 188*s
    d.path(f"M{500+110*s},752 C{500+140*s},756 {500+160*s},754 {x1},750",
           f"Stub {('L','R')[s>0]}", fill=NONE, stroke="#3A3444",
           strokeWidth=22, cap="round", opacity=90)
    d.path(f"M{x1+6},730 L{x1+34},758 M{x1+34},730 L{x1+6},758",
           f"Stub X {('L','R')[s>0]}", fill=NONE, stroke=NOPE,
           strokeWidth=7, cap="round", opacity=95)

# --- dead-end signposts, left and right -------------------------------------------
for side, sx in enumerate([232, 768]):
    lbl = "L" if side == 0 else "R"
    d.path(f"M{sx},560 L{sx},400", f"Post {lbl}", fill=NONE, stroke=WOOD,
           strokeWidth=14, cap="round")
    # plaque pointing outward, crossed out
    px = sx + (34 if side == 0 else -110)
    d.path(rot_rect_path(px + 38, 396, 116, 44, -4 if side == 0 else 4),
           f"Plaque {lbl}", fill=WOOD, stroke=INK, strokeWidth=5)
    # arrow + big X, drawn in plaque space
    ax = px + 38
    ay = 396
    sg = 1 if side == 0 else -1
    d.path(f"M{ax-34*sg},{ay} L{ax+30*sg},{ay} "
           f"M{ax+12*sg},{ay-9} L{ax+30*sg},{ay} L{ax+12*sg},{ay+9}",
           f"Plaque arrow {lbl}", fill=NONE, stroke="#E8D9BC",
           strokeWidth=5, cap="round", join="round")
    d.path(f"M{ax-40},{ay-16} L{ax+40},{ay+16} M{ax+40},{ay-16} L{ax-40},{ay+16}",
           f"Plaque X {lbl}", fill=NONE, stroke=NOPE, strokeWidth=5,
           cap="round", opacity=90)

# a dangling tag on the left post — the error itself
d.path("M262,420 C282,442 292,462 296,486", "Tag string", fill=NONE,
       stroke="#8A7A5C", strokeWidth=3, opacity=80)
d.path(rot_rect_path(298, 500, 66, 40, 12), "Tag", fill="#E8DCC0",
       stroke=INK, strokeWidth=4)
# digits must be Source Sans 3 — Virelai Sans has no digit glyphs
d.text("404", "Tag number", x=298, y=508, size=20, font="Source Sans 3",
       color="#8E2A20", justify="center")

# --- 404sy: the lost one -------------------------------------------------------------
# coat: a jacket stitched from breadcrumb trails
d.path("M500,420 C580,420 640,470 650,555 C658,640 646,700 632,730 "
       "L368,730 C354,700 342,640 350,555 C360,470 420,420 500,420 Z",
       "Coat", fill=COAT, stroke=INK, strokeWidth=7)
# hem + lapels
d.path("M368,706 L632,706", "Hem stitch", fill=NONE, stroke="#C9B47E",
       strokeWidth=4, opacity=60)
d.path("M452,468 L500,730 M548,468 L500,730", "Lapels", fill=NONE,
       stroke=COAT_DK, strokeWidth=6, opacity=80)
d.path("M452,468 L484,530 L500,470 L516,530 L548,468", "Collar", fill=NONE,
       stroke=INK, strokeWidth=5, join="round")
# breadcrumb trails stitched across the coat: dots + a chevron each
for i, (bx, by) in enumerate([(400, 560), (460, 610), (560, 560),
                              (610, 620), (430, 660), (580, 660)]):
    for k in range(3):
        d.shape("ellipse", f"Crumb {i+1}.{k+1}", x=bx + k*14, y=by,
                width=6, height=6, fill="#E4D4A8", opacity=85, stroke=NONE)
    d.path(f"M{bx+48},{by-6} l10,9 l-10,9", f"Crumb chevron {i+1}",
           fill=NONE, stroke="#E4D4A8", strokeWidth=3, cap="round",
           join="round", opacity=85)
# two stitch seams down the front
d.path("M476,545 L476,700 M524,545 L524,700", "Front seams", fill=NONE,
       stroke="#C9B47E", strokeWidth=3, opacity=50)

# head
d.shape("ellipse", "Head", x=415, y=300, width=170, height=150,
        fill=FACE, stroke=INK, strokeWidth=7)
# a little traveller's cap, tipped
d.path("M424,330 C424,272 576,272 576,330 L560,330 C560,300 440,300 440,330 Z",
       "Cap", fill=COAT, stroke=INK, strokeWidth=6, join="round")
d.path("M430,314 C470,296 530,296 570,314", "Cap brim line", fill=NONE,
       stroke=COAT_DK, strokeWidth=4, opacity=70)
d.shape("ellipse", "Cap button", x=492, y=282, width=16, height=12,
        fill=COAT, stroke=INK, strokeWidth=4)
# bewildered face: mismatched eyes, raised brow, wavy mouth
d.shape("ellipse", "Eye L", x=448, y=352, width=24, height=30, fill="#FBF6E8",
        stroke=INK, strokeWidth=4)
d.shape("ellipse", "Eye R", x=524, y=346, width=30, height=36, fill="#FBF6E8",
        stroke=INK, strokeWidth=4)
d.shape("ellipse", "Pupil L", x=456, y=362, width=10, height=12, fill=INK,
        stroke=NONE)
d.shape("ellipse", "Pupil R", x=530, y=358, width=12, height=14, fill=INK,
        stroke=NONE)
d.path("M442,340 C452,330 466,328 474,332", "Brow L flat", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.path("M520,324 C534,314 550,314 560,320", "Brow R raised", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.path("M462,414 C474,408 482,420 494,414 C506,408 514,420 526,414",
       "Uncertain mouth", fill=NONE, stroke=INK, strokeWidth=4, cap="round")
# the little question that follows him everywhere
d.text("?", "Question", x=610, y=290, size=44, font="Virelai Sans",
       color="#C9BCA0", justify="center")

# --- the upside-down map --------------------------------------------------------------
# held in both hands in front of the coat, tilted hard — clearly wrong way up
d.path("M596,560 L760,600 L726,730 L560,690 Z", "Map sheet", fill=MAP,
       stroke=INK, strokeWidth=6, join="round")
# fold crease
d.path("M648,578 L616,706", "Map fold", fill=NONE, stroke="#B4A488",
       strokeWidth=3, opacity=70)
# the route, wandering to an X near the lower edge (the map's "top")
d.path("M736,614 C700,600 668,620 672,648 C676,676 640,690 604,684",
       "Map route", fill=NONE, stroke="#8A94A0", strokeWidth=5,
       cap="round", dash=[8, 7])
# compass rose — its N points down, because the map is upside down
d.shape("ellipse", "Compass ring", x=696, y=676, width=44, height=44,
        fill=NONE, stroke="#8A94A0", strokeWidth=3, opacity=90)
d.path("M718,678 L710,706 L726,706 Z", "Compass needle", fill="#8A94A0",
       stroke=NONE, opacity=90)
d.text("N", "Compass N", x=718, y=724, size=13, font="Virelai Sans",
       color="#8A94A0", justify="center")
# the X the route dies on
d.path("M596,672 L620,696 M620,672 L596,696", "Map X", fill=NONE,
       stroke=NOPE, strokeWidth=6, cap="round")
# hands gripping the map's lower corners
d.path("M640,560 C610,560 580,575 570,600", "Arm L", fill=NONE,
       stroke=COAT, strokeWidth=26, cap="round")
d.shape("ellipse", "Hand L", x=566, y=590, width=30, height=26, fill=FACE,
        stroke=INK, strokeWidth=5)
d.path("M700,700 C670,716 640,716 620,706", "Arm R", fill=NONE,
       stroke=COAT, strokeWidth=26, cap="round")
d.shape("ellipse", "Hand R", x=614, y=694, width=30, height=26, fill=FACE,
        stroke=INK, strokeWidth=5)

# boots under the hem
d.shape("ellipse", "Boot L", x=420, y=724, width=70, height=34, fill="#3A3026",
        stroke=INK, strokeWidth=5)
d.shape("ellipse", "Boot R", x=510, y=724, width=70, height=34, fill="#3A3026",
        stroke=INK, strokeWidth=5)

# --- captions -------------------------------------------------------------------------
nm = d.text("404SY MCLOSTALOT", "Name", x=500, y=930, size=56,
            font="Virelai Sans", color="#E4DCCE", justify="center")
# Virelai Sans has no digit glyphs: "404" falls back to Source Sans 3
if nm and nm.get("id"):
    d.cmd("text.setStyle", "name digit fallback", ids=[nm["id"]],
          start=0, end=3, font="Source Sans 3")
r = d.text("GUIDANCE SYSTEM FAILURE", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#A8A0BC", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("404.404sy-mclostalot-V1R00")
