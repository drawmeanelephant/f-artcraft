#!/usr/bin/env python3
"""rc-glue.sh — The Signpost Stitcher. Necropolis plate V1R00.
Between two crypt corridors, a worker in overalls gluing a fresh index
signpost — index.md — pointing both ways, older signposts receding down
the hall marking every directory that once went unindexed. Wayfinding
for the wandering dead. Oak, glue, and torchlight. 1000x1000.
Gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("RC-Glue — Necropolis Plate", 1000, 1000)

INK = "#26190E"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#161009"}, {"offset": 1, "color": "#0A0705"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4E3F30"}, {"offset": 0.7, "color": "#2E251C"},
    {"offset": 1, "color": "#14100C"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2A2118"}, {"offset": 1, "color": "#100C08"}]}}
CORRIDOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#241B12"}, {"offset": 1, "color": "#080604"}]}}
OAK = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#8A6238"}, {"offset": 1, "color": "#54371E"}]}}
OAK_FRESH = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#C79A5C"}, {"offset": 1, "color": "#8A5E30"}]}}
OAK_OLD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5C4228"}, {"offset": 1, "color": "#342214"}]}}
DENIM = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4A6A8C"}, {"offset": 1, "color": "#2C4258"}]}}
SHIRT = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#8C4030"}, {"offset": 1, "color": "#542418"}]}}
SKIN = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E8C49A"}, {"offset": 1, "color": "#B08858"}]}}
FLAME = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#FFE8A0"}, {"offset": 1, "color": "#D86820"}]}}
GLUE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F0DCA8"}, {"offset": 1, "color": "#C4A054"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#7E6238", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E4D3B0", strokeWidth=3, opacity=45)
for i, (x, y, w) in enumerate([(193,233,8),(801,230,7),(157,524,9),(837,544,8),
                               (247,766,7),(753,749,9),(133,393,6),(864,391,7),
                               (391,113,7),(613,110,8),(333,823,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#6A5238", opacity=35, stroke=NONE)

# --- torchlight glows ---------------------------------------------------------
for i, (x, y) in enumerate([(272, 300), (728, 300)]):
    d.shape("ellipse", f"Torch glow {i+1}", x=x-95, y=y-95, width=190,
            height=190, fill="#E89A50", opacity=14, stroke=NONE)
    d.shape("ellipse", f"Torch core {i+1}", x=x-40, y=y-40, width=80,
            height=80, fill="#F0B868", opacity=16, stroke=NONE)

# --- the two crypt corridors ---------------------------------------------------
for i, cx in enumerate([275, 725]):
    d.path(f"M{cx-88},700 L{cx-88},430 C{cx-88},345 {cx+88},345 {cx+88},430 "
           f"L{cx+88},700 Z", f"Corridor {i+1}", fill=CORRIDOR_GRAD,
           stroke=INK, strokeWidth=5, join="round")
    # keystone + arch band
    d.path(f"M{cx-88},430 C{cx-88},345 {cx+88},345 {cx+88},430", f"Arch {i+1}",
           fill=NONE, stroke="#4A3826", strokeWidth=7, opacity=85)
    d.path(f"M{cx-9},350 L{cx+9},350 L{cx+6},375 L{cx-6},375 Z",
           f"Keystone {i+1}", fill="#54402A", stroke=INK, strokeWidth=3,
           join="round")

# older signposts receding down the left corridor
def signpost(cx, top, h, arrow_w, arrow_h, op, tag):
    d.path(f"M{cx-4},{top} L{cx+4},{top} L{cx+4},{top+h} L{cx-4},{top+h} Z",
           f"{tag} post", fill=OAK_OLD, stroke=INK, strokeWidth=2, opacity=op)
    ay = top + 14
    d.path(f"M{cx-arrow_w},{ay+arrow_h/2} L{cx-arrow_w+16},{ay} "
           f"L{cx-2},{ay} L{cx-2},{ay+arrow_h} L{cx-arrow_w+16},{ay+arrow_h} Z",
           f"{tag} arrow L", fill=OAK_OLD, stroke=INK, strokeWidth=2,
           opacity=op, join="round")
    ay2 = top + 46
    d.path(f"M{cx+2},{ay2} L{cx+arrow_w-14},{ay2} L{cx+arrow_w},{ay2+arrow_h/2} "
           f"L{cx+arrow_w-14},{ay2+arrow_h} L{cx+2},{ay2} Z",
           f"{tag} arrow R", fill=OAK_OLD, stroke=INK, strokeWidth=2,
           opacity=op, join="round")

signpost(232, 470, 150, 62, 22, 62, "Recede L1")
signpost(300, 440, 105, 48, 17, 38, "Recede L2")
# one dim signpost deep in the right corridor
signpost(760, 485, 120, 52, 18, 42, "Recede R1")

# corridor floor lines suggesting depth
for i, (x0, x1) in enumerate([(200, 285), (355, 322), (645, 678), (800, 715)]):
    d.path(f"M{x0},700 L{x1},560", f"Corridor floor line {i+1}", fill=NONE,
           stroke="#1A130C", strokeWidth=3, opacity=70)

# --- torch sconces over each corridor ------------------------------------------
for i, (cx, side) in enumerate([(272, -1), (728, 1)]):
    d.path(f"M{cx},{300+side*0} L{cx + 20*side},282", f"Sconce arm {i+1}",
           fill=NONE, stroke="#3A2A18", strokeWidth=6, cap="round")
    d.path(f"M{cx + 20*side - 12},270 L{cx + 20*side + 12},270 "
           f"L{cx + 20*side + 8},288 L{cx + 20*side - 8},288 Z",
           f"Sconce cup {i+1}", fill="#4A3826", stroke=INK, strokeWidth=3,
           join="round")
    d.path(f"M{cx + 20*side},268 C{cx + 20*side - 11},254 "
           f"{cx + 20*side - 5},238 {cx + 20*side},228 "
           f"C{cx + 20*side + 6},238 {cx + 20*side + 10},254 "
           f"{cx + 20*side},268 Z", f"Flame {i+1}", fill=FLAME,
           stroke=NONE, opacity=95)

# --- floor ---------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0E0A06",
       strokeWidth=4, opacity=70)
d.shape("ellipse", "Post shadow", x=390, y=684, width=230, height=18,
        fill="#050302", opacity=55, stroke=NONE)
d.shape("ellipse", "Worker shadow", x=590, y=684, width=120, height=15,
        fill="#050302", opacity=50, stroke=NONE)

# --- the great signpost ---------------------------------------------------------
# post
d.path("M486,340 C486,330 514,330 514,340 L514,690 L486,690 Z", "Signpost",
       fill=OAK, stroke=INK, strokeWidth=5, join="round")
d.shape("ellipse", "Post finial", x=491, y=316, width=18, height=18,
        fill=OAK_FRESH, stroke=INK, strokeWidth=4)
# wood grain
d.path("M494,380 L493,560 M506,400 L508,640", "Post grain", fill=NONE,
       stroke="#3A2412", strokeWidth=2, opacity=60)

# weathered arrow L — drafts
d.path("M334,398 L368,382 L512,382 L512,414 L368,414 Z", "Arrow drafts",
       fill=OAK_OLD, stroke=INK, strokeWidth=4, join="round")
d.text("drafts", "Drafts label", x=448, y=406, size=13, font="Virelai Sans",
       color="#2A1C0E", justify="center")
# weathered arrow R — log
d.path("M488,442 L644,442 L676,459 L644,476 L488,476 Z", "Arrow log",
       fill=OAK_OLD, stroke=INK, strokeWidth=4, join="round")
d.text("log", "Log label", x=560, y=468, size=13, font="Virelai Sans",
       color="#2A1C0E", justify="center")
# bolts pinning each board to the post
for i, by in enumerate([398, 459, 532]):
    d.shape("ellipse", f"Bolt {i+1}", x=495, y=by-4, width=9, height=9,
            fill="#3A2A1A", stroke=INK, strokeWidth=2)

# fresh double-headed arrow — index.md (the one being glued)
d.path("M380,532 L414,514 L586,514 L620,532 L586,550 L414,550 Z",
       "Arrow index.md", fill=OAK_FRESH, stroke=INK, strokeWidth=4,
       join="round")
d.path("M396,532 L420,520 M604,532 L580,520", "Arrow fresh grain",
       fill=NONE, stroke="#8A5E30", strokeWidth=2, opacity=70)
d.text("index.md", "Index label", x=500, y=538, size=15, font="Virelai Sans",
       color="#2A1C0E", justify="center")
# wet glue seeping at the board/post seam + a falling drop
d.path("M504,514 C506,524 508,530 505,540 C502,530 502,522 504,514 Z",
       "Glue seam", fill=GLUE, stroke=NONE, opacity=85)
d.shape("ellipse", "Glue drop", x=500, y=566, width=7, height=10,
        fill=GLUE, stroke=NONE, opacity=90)

# --- the worker in overalls, pressing the fresh board on -------------------------
# legs
d.shape("rectangle", "Leg L", x=616, y=636, width=20, height=54,
        fill=DENIM, stroke=INK, strokeWidth=4, radius=6)
d.shape("rectangle", "Leg R", x=644, y=636, width=20, height=54,
        fill=DENIM, stroke=INK, strokeWidth=4, radius=6)
# boots
d.path("M610,684 L640,684 L640,694 L610,694 Z", "Boot L", fill="#33241A",
       stroke=INK, strokeWidth=3, join="round")
d.path("M642,684 L672,684 L672,694 L642,694 Z", "Boot R", fill="#33241A",
       stroke=INK, strokeWidth=3, join="round")
# torso: shirt + overalls bib + straps
d.path("M606,570 L672,570 L668,644 L610,644 Z", "Shirt torso", fill=SHIRT,
       stroke=INK, strokeWidth=4, join="round")
d.path("M616,596 L662,596 L660,646 L618,646 Z", "Overall bib", fill=DENIM,
       stroke=INK, strokeWidth=4, join="round")
d.path("M620,596 L612,566 M656,596 L664,566", "Straps", fill=NONE,
       stroke=DENIM["gradient"]["stops"][0]["color"], strokeWidth=8,
       cap="round")
# head + work cap
d.shape("ellipse", "Head", x=620, y=524, width=38, height=40,
        fill=SKIN, stroke=INK, strokeWidth=4)
d.path("M618,540 C618,522 660,522 660,540 L656,534 C648,526 630,526 624,534 Z",
       "Cap", fill=DENIM, stroke=INK, strokeWidth=3, join="round")
d.shape("ellipse", "Cap brim", x=606, y=534, width=16, height=8,
        fill=DENIM, stroke=INK, strokeWidth=3)
d.shape("ellipse", "Eye", x=627, y=548, width=5, height=5,
        fill="#241812", stroke=NONE)
# far arm holding the glue pot at his side
d.path("M668,578 C684,590 690,606 688,624", "Arm pot", fill=NONE,
       stroke="#8C4030", strokeWidth=9, cap="round")
d.path("M676,622 L698,622 L695,646 L679,646 Z", "Glue pot", fill="#5A4630",
       stroke=INK, strokeWidth=3, join="round")
d.path("M678,624 L696,624", "Glue surface", fill=NONE, stroke="#F0DCA8",
       strokeWidth=3, opacity=90, cap="round")
# near arm raised, pressing the board edge
d.path("M614,576 C596,566 584,552 578,538", "Arm press", fill=NONE,
       stroke="#8C4030", strokeWidth=10, cap="round")
d.shape("ellipse", "Hand", x=566, y=524, width=20, height=18,
        fill=SKIN, stroke=INK, strokeWidth=3)
# glue brush in the pressing hand
d.path("M574,534 L586,520", "Brush handle", fill=NONE, stroke="#6A4A28",
       strokeWidth=5, cap="round")
d.path("M584,522 L590,512 L596,517 L588,526 Z", "Brush head", fill=GLUE,
       stroke=INK, strokeWidth=2, join="round")

# glue drips on the floor under the work
d.shape("ellipse", "Floor drip 1", x=512, y=688, width=16, height=6,
        fill="#C4A054", opacity=75, stroke=NONE)
d.shape("ellipse", "Floor drip 2", x=536, y=692, width=10, height=4,
        fill="#C4A054", opacity=60, stroke=NONE)

# --- captions ------------------------------------------------------------------
d.text("RC-GLUE", "Name", x=500, y=930, size=58, font="Virelai Sans",
       color="#E8DCC8", justify="center")
r = d.text("INDEX OF CORRIDORS", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#B8A488", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("rk-glue-V1R00")
