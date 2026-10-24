#!/usr/bin/env python3
"""rc-assets.sh — The Seal Registry. Necropolis plate V1R00.
A registrar's desk in the undercroft: every asset stamped with a wax
SHA-256 seal and copied into a great mirrored cabinet — the source tree
on the left, its ghost-perfect reflection on the right.
Wax red and ledger brown. 1000x1000. Gradients + translucent shading."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("RC-Assets — Necropolis Plate", 1000, 1000)

INK = "#241A12"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#171009"}, {"offset": 1, "color": "#0A0605"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#5A4636"}, {"offset": 0.7, "color": "#352922"},
    {"offset": 1, "color": "#171110"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2E241C"}, {"offset": 1, "color": "#140E0A"}]}}
CABINET = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6A4A30"}, {"offset": 1, "color": "#3E2A1C"}]}}
DOOR = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#543A26"}, {"offset": 1, "color": "#2E1E14"}]}}
RECESS = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2E2216"}, {"offset": 1, "color": "#18100A"}]}}
GLASS = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3E4E5C"}, {"offset": 1, "color": "#1E262E"}]}}
CARD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#D9C69A"}, {"offset": 1, "color": "#AB9264"}]}}
WAX = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#C04434"}, {"offset": 1, "color": "#7A1F18"}]}}
LEDGER = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E4D3A8"}, {"offset": 1, "color": "#B8A06E"}]}}
DESK_TOP = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7A5636"}, {"offset": 1, "color": "#4E3018"}]}}
DESK_FRONT = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5C3E24"}, {"offset": 1, "color": "#36200E"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#8A744E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E4D3B0", strokeWidth=3, opacity=45)
for i, (x, y, w) in enumerate([(193,233,8),(801,230,7),(157,524,9),(837,544,8),
                               (247,766,7),(753,749,9),(133,393,6),(864,391,7),
                               (391,113,7),(613,110,8),(333,823,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#6A563F", opacity=35, stroke=NONE)

# --- floor: bottom segment closed on the disc's own arc -----------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0E0A06",
       strokeWidth=4, opacity=70)
# flagstones + a dropped seal tag on the flags
d.path("M210,762 C380,784 620,784 790,762", "Flagstone 1", fill=NONE,
       stroke="#3A2E22", strokeWidth=3, opacity=45)
d.path("M320,716 L314,756 M690,714 L696,756", "Flagstone joints", fill=NONE,
       stroke="#3A2E22", strokeWidth=3, opacity=35)
d.shape("ellipse", "Desk shadow", x=300, y=688, width=400, height=22,
        fill="#050302", opacity=55, stroke=NONE)
d.path("M238,742 L262,738 L264,752 L240,756 Z", "Dropped tag", fill="#C9B586",
       stroke=INK, strokeWidth=2)
d.shape("ellipse", "Dropped wax", x=252, y=748, width=9, height=8,
        fill=WAX, stroke=INK, strokeWidth=1)

# --- the great mirrored cabinet -------------------------------------------------
d.shape("ellipse", "Cabinet shadow", x=240, y=676, width=520, height=20,
        fill="#050302", opacity=45, stroke=NONE)
# cornice
d.path("M250,196 L262,168 L738,168 L750,196 Z", "Cornice", fill=CABINET,
       stroke=INK, strokeWidth=5, join="round")
d.path("M262,196 L738,196", "Cornice shade", fill=NONE, stroke="#0E0A06",
       strokeWidth=3, opacity=60)
# body
d.shape("rectangle", "Cabinet body", x=268, y=196, width=464, height=468,
        fill=CABINET, stroke=INK, strokeWidth=6)
# left door — open shelves with the source tree
d.shape("rectangle", "Left door", x=290, y=214, width=200, height=410,
        fill=DOOR, stroke=INK, strokeWidth=4)
d.shape("rectangle", "Left recess", x=306, y=232, width=168, height=372,
        fill=RECESS, stroke=INK, strokeWidth=3)
# right door — the mirror
d.shape("rectangle", "Right door", x=510, y=214, width=200, height=410,
        fill=DOOR, stroke=INK, strokeWidth=4)
d.shape("rectangle", "Mirror glass", x=526, y=232, width=168, height=372,
        fill=GLASS, stroke=INK, strokeWidth=3)
d.path("M548,604 L668,240 L678,240 L558,604 Z", "Mirror sheen",
       fill="#CFE0EC", opacity=12, stroke=NONE)
d.path("M586,604 L694,296 L700,296 L592,604 Z", "Mirror sheen 2",
       fill="#CFE0EC", opacity=8, stroke=NONE)
# center stile + keyhole
d.shape("rectangle", "Center stile", x=490, y=214, width=20, height=410,
        fill=CABINET, stroke=INK, strokeWidth=3)
d.shape("ellipse", "Keyhole", x=495, y=416, width=10, height=14,
        fill="#0E0A06", stroke="#8A744E", strokeWidth=2)
# plinth on the floor
d.shape("rectangle", "Plinth", x=260, y=664, width=480, height=26,
        fill=DOOR, stroke=INK, strokeWidth=4, radius=3)

# --- the source tree, left recess (cards + elbow connectors) ---------------------
def node(cx, cy, w, h, label, seal=False):
    d.shape("rectangle", label, x=cx-w/2, y=cy-h/2, width=w, height=h,
            fill=CARD, stroke=INK, strokeWidth=2, radius=2)
    d.path(f"M{cx-w/2+4},{cy-h/4} L{cx+w/2-4},{cy-h/4}",
           f"{label} rule", fill=NONE, stroke="#6E5A40", strokeWidth=2,
           opacity=60)
    if seal:
        d.shape("ellipse", f"{label} seal", x=cx+w/2-10, y=cy+h/2-10,
                width=8, height=8, fill=WAX, stroke=INK, strokeWidth=1)

def elbow(x0, y0, x1, y1, label, ghost=False):
    col = "#9FB2C0" if ghost else "#8A7450"
    op = 55 if ghost else 85
    d.path(f"M{x0},{y0} L{x0},{(y0+y1)/2} L{x1},{(y0+y1)/2} L{x1},{y1}",
           label, fill=NONE, stroke=col, strokeWidth=2, opacity=op)

# trunk rising to the root folder
d.path("M390,596 L390,566", "Trunk", fill=NONE, stroke="#8A7450",
       strokeWidth=3, opacity=85)
d.path("M370,566 L370,552 L404,552 L404,544 L424,544 L424,566 Z",
       "Root folder", fill=CARD, stroke=INK, strokeWidth=3, join="round")
# level 2: two children
elbow(390, 566, 344, 512, "Branch L1")
elbow(390, 566, 436, 512, "Branch R1")
node(344, 494, 40, 30, "Node src", seal=True)
node(436, 494, 40, 30, "Node lib", seal=True)
# level 3: four leaves
elbow(344, 479, 322, 446, "Leaf L1")
elbow(344, 479, 366, 446, "Leaf L2")
elbow(436, 479, 414, 446, "Leaf R1")
elbow(436, 479, 458, 446, "Leaf R2")
node(322, 430, 30, 24, "Leaf a")
node(366, 430, 30, 24, "Leaf b", seal=True)
node(414, 430, 30, 24, "Leaf c")
node(458, 430, 30, 24, "Leaf d", seal=True)
# shelf line under the tree
d.path("M312,596 L468,596", "Shelf", fill=NONE, stroke="#4A3826",
       strokeWidth=5, opacity=80)

# --- the ghost-perfect reflection, in the mirror (pre-blended ghost ink) ---------
GH = "#9FB2C0"
d.path("M610,596 L610,566", "Ghost trunk", fill=NONE, stroke=GH,
       strokeWidth=3, opacity=50)
d.path("M590,566 L590,552 L624,552 L624,544 L644,544 L644,566 Z",
       "Ghost root", fill=NONE, stroke=GH, strokeWidth=3, opacity=50,
       join="round")
elbow(610, 566, 656, 512, "Ghost branch L", ghost=True)
elbow(610, 566, 564, 512, "Ghost branch R", ghost=True)
for i, (cx, cy, w, h) in enumerate([(656,494,40,30),(564,494,40,30),
                                    (678,430,30,24),(634,430,30,24),
                                    (586,430,30,24),(542,430,30,24)]):
    d.shape("rectangle", f"Ghost node {i+1}", x=cx-w/2, y=cy-h/2, width=w,
            height=h, fill=NONE, stroke=GH, strokeWidth=2, opacity=48, radius=2)
elbow(656, 479, 678, 446, "Ghost leaf L1", ghost=True)
elbow(656, 479, 634, 446, "Ghost leaf L2", ghost=True)
elbow(564, 479, 586, 446, "Ghost leaf R1", ghost=True)
elbow(564, 479, 542, 446, "Ghost leaf R2", ghost=True)
for i, (cx, cy) in enumerate([(663,501),(563,501),(678,437),(542,437)]):
    d.shape("ellipse", f"Ghost seal {i+1}", x=cx, y=cy, width=7, height=7,
            fill="#8A5A50", opacity=50, stroke=NONE)
d.path("M532,596 L688,596", "Ghost shelf", fill=NONE, stroke=GH,
       strokeWidth=4, opacity=35)

# --- seal tags hanging from the cornice -------------------------------------------
for i, (tx, tl) in enumerate([(330, 34), (470, 44), (610, 30)]):
    d.path(f"M{tx},196 L{tx},{196+tl}", f"Tag string {i+1}", fill=NONE,
           stroke="#8A7450", strokeWidth=2, opacity=70)
    d.shape("ellipse", f"Hanging wax {i+1}", x=tx-9, y=196+tl-2, width=18,
            height=16, fill=WAX, stroke=INK, strokeWidth=2)
    d.shape("rectangle", f"Hanging tag {i+1}", x=tx-8, y=196+tl+12, width=16,
            height=20, fill=CARD, stroke=INK, strokeWidth=2, radius=2)

# --- the registrar's desk -----------------------------------------------------------
# slab
d.shape("rectangle", "Desk slab", x=330, y=614, width=340, height=30,
        fill=DESK_TOP, stroke=INK, strokeWidth=5, radius=3)
d.path("M336,618 L664,618", "Slab highlight", fill=NONE, stroke="#C49A66",
       strokeWidth=3, opacity=50)
# front + drawer + legs
d.shape("rectangle", "Desk front", x=348, y=644, width=304, height=52,
        fill=DESK_FRONT, stroke=INK, strokeWidth=5)
d.shape("rectangle", "Drawer", x=440, y=652, width=120, height=34,
        fill=DOOR, stroke=INK, strokeWidth=3, radius=3)
d.shape("ellipse", "Drawer knob", x=494, y=664, width=12, height=12,
        fill="#8A744E", stroke=INK, strokeWidth=2)
d.shape("rectangle", "Leg L", x=356, y=644, width=18, height=52,
        fill="#3A2412", stroke=INK, strokeWidth=3)
d.shape("rectangle", "Leg R", x=626, y=644, width=18, height=52,
        fill="#3A2412", stroke=INK, strokeWidth=3)

# open ledger on the slab
d.path("M404,614 L446,584 L500,584 L500,614 Z", "Ledger page L", fill=LEDGER,
       stroke=INK, strokeWidth=3, join="round")
d.path("M500,614 L500,584 L554,584 L596,614 Z", "Ledger page R", fill=LEDGER,
       stroke=INK, strokeWidth=3, join="round")
d.path("M500,584 L500,614", "Ledger spine", fill=NONE, stroke="#6E5A40",
       strokeWidth=3)
for i, ly in enumerate([592, 599, 606]):
    d.path(f"M452,{ly} L492,{ly}", f"Ledger line L{i+1}", fill=NONE,
           stroke="#8A7450", strokeWidth=2, opacity=75)
    d.path(f"M508,{ly} L548,{ly}", f"Ledger line R{i+1}", fill=NONE,
           stroke="#8A7450", strokeWidth=2, opacity=75)
# the wax SHA-256 seal stamped on the right page
d.shape("ellipse", "Ledger wax", x=552, y=576, width=30, height=26,
        fill=WAX, stroke=INK, strokeWidth=3)
d.path("M559,588 L575,588 M567,582 L567,594", "Seal cross", fill=NONE,
       stroke="#5C140F", strokeWidth=2, opacity=80, cap="round")
d.text("SHA-256", "Seal hash", x=567, y=611, size=9, font="Virelai Sans",
       color="#4A2C20", justify="center")

# seal stamp + wax stick + ink pot + quill on the slab
d.shape("rectangle", "Stamp handle", x=622, y=572, width=12, height=30,
        fill="#5C3E24", stroke=INK, strokeWidth=3, radius=4)
d.shape("ellipse", "Stamp head", x=616, y=598, width=24, height=16,
        fill="#8A744E", stroke=INK, strokeWidth=3)
d.shape("rectangle", "Wax stick", x=370, y=600, width=40, height=10,
        fill=WAX, stroke=INK, strokeWidth=2, radius=4)
d.shape("ellipse", "Ink pot", x=350, y=584, width=22, height=26,
        fill="#2A1C10", stroke=INK, strokeWidth=3)
d.path("M361,584 L361,570", "Quill stem", fill=NONE, stroke="#C9B586",
       strokeWidth=3, cap="round")
d.path("M361,570 C355,556 358,544 366,536 C370,548 368,562 361,570 Z",
       "Quill feather", fill="#D9C69A", stroke=INK, strokeWidth=2)

# two sealed tags lying on the slab
d.path("M650,600 L672,596 L674,610 L652,614 Z", "Slab tag", fill="#C9B586",
       stroke=INK, strokeWidth=2)
d.shape("ellipse", "Slab tag wax", x=662, y=604, width=8, height=8,
        fill=WAX, stroke=INK, strokeWidth=1)

# --- captions ------------------------------------------------------------------
d.text("RC-ASSETS", "Name", x=500, y=930, size=58, font="Virelai Sans",
       color="#E8DAC2", justify="center")
r = d.text("MANIFEST OF SEALS", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#B09B78", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("rk-assets-V1R00")
