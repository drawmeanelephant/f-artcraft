#!/usr/bin/env python3
"""rotkeeper.sh — The Dispatcher. Necropolis plate V1R00.
A hooded sexton at the necropolis gates holding a great ring of keys —
each key stamped with a subcommand. Lamp-black robes, brass keys,
one lit gate lantern. 1000x1000. Gradients + translucent shading."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Rotkeeper — Necropolis Plate", 1000, 1000)

INK = "#241E2C"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#14101C"}, {"offset": 1, "color": "#080610"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4C4458"}, {"offset": 0.7, "color": "#2E2838"},
    {"offset": 1, "color": "#181422"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2A2434"}, {"offset": 1, "color": "#12101A"}]}}
ROBE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4B4152"}, {"offset": 0.62, "color": "#2A2433"},
    {"offset": 1, "color": "#17131F"}]}}
BRASS = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E8C56A"}, {"offset": 1, "color": "#8A6420"}]}}
GLASS = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#FFE8A8"}, {"offset": 1, "color": "#C8842A"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#7A6A4E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#CFC4DC", strokeWidth=3, opacity=50)
for i, (x, y, w) in enumerate([(193,233,8),(801,230,7),(157,524,9),(837,544,8),
                               (247,766,7),(753,749,9),(133,393,6),(864,391,7),
                               (391,113,7),(613,110,8),(333,823,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#5A5068", opacity=40, stroke=NONE)

# --- gate arch behind the figure ----------------------------------------------
d.path("M250,700 L250,340 C250,230 360,160 500,160 C640,160 750,230 750,340 L750,700",
       "Gate arch", fill=NONE, stroke="#0E0B14", strokeWidth=10, opacity=55)
for i, gx in enumerate([300, 375, 625, 700]):
    d.path(f"M{gx},700 L{gx},{300 if gx in (375,625) else 330}",
           f"Gate bar {i+1}", fill=NONE, stroke="#0E0B14", strokeWidth=7,
           opacity=40, cap="round")

# --- floor: bottom segment closed on the disc's own arc -----------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0C0A12",
       strokeWidth=4, opacity=70)
# flagstones
d.path("M190,752 C360,772 640,772 810,752", "Flagstone 1", fill=NONE,
       stroke="#3A3344", strokeWidth=3, opacity=45)
d.path("M240,812 C400,838 600,838 760,812", "Flagstone 2", fill=NONE,
       stroke="#3A3344", strokeWidth=3, opacity=35)
d.path("M380,712 L372,762 M620,712 L628,762 M500,790 L500,840",
       "Flagstone joints", fill=NONE, stroke="#3A3344", strokeWidth=3, opacity=35)

# --- lantern on its crook, left of the figure ----------------------------------
d.shape("ellipse", "Lantern spill", x=140, y=300, width=260, height=300,
        fill="#FFD98A", opacity=12, stroke=NONE)
d.shape("ellipse", "Lantern glow", x=185, y=350, width=150, height=170,
        fill="#FFD98A", opacity=18, stroke=NONE)
d.path("M248,695 L248,430 C248,392 268,372 292,372", "Lantern crook",
       fill=NONE, stroke=INK, strokeWidth=9, cap="round")
d.path("M292,372 L292,392", "Lantern hanger", fill=NONE, stroke=INK,
       strokeWidth=4, cap="round")
# lantern body: cap, glass, base
d.path("M268,392 L316,392 L306,410 L278,410 Z", "Lantern cap",
       fill="#3A3242", stroke=INK, strokeWidth=4, join="round")
d.shape("rectangle", "Lantern glass", x=276, y=410, width=32, height=52,
        fill=GLASS, stroke=INK, strokeWidth=4)
d.path("M292,452 C285,442 288,432 292,426 C296,432 299,442 292,452 Z",
       "Lantern flame", fill="#FFF3C4", stroke=NONE)
d.path("M272,462 L312,462 L306,474 L278,474 Z", "Lantern base",
       fill="#3A3242", stroke=INK, strokeWidth=4, join="round")

# --- the sexton ----------------------------------------------------------------
d.shape("ellipse", "Figure shadow", x=330, y=678, width=340, height=30,
        fill="#060409", opacity=55, stroke=NONE)
# cloak: hood point at crown, shoulders, widening to a pooled hem
d.path("M355,700 C350,610 362,505 405,440 C420,416 438,400 455,385 "
       "C442,340 462,285 500,272 C538,285 558,340 545,385 "
       "C562,400 580,416 595,440 C638,505 650,610 645,700 "
       "C600,716 400,716 355,700 Z",
       "Cloak", fill=ROBE_GRAD, stroke=INK, strokeWidth=7, join="round")
# hood opening: the face is a lamp-black void
d.path("M500,300 C462,312 452,352 460,390 C474,408 526,408 540,390 "
       "C548,352 538,312 500,300 Z",
       "Hood void", fill="#0E0B13", stroke="#3A3242", strokeWidth=4)
# two faint embers where eyes would be — lantern light caught in the dark
d.shape("ellipse", "Eye ember L", x=478, y=358, width=7, height=7,
        fill="#E8B45A", opacity=80, stroke=NONE)
d.shape("ellipse", "Eye ember R", x=515, y=358, width=7, height=7,
        fill="#E8B45A", opacity=80, stroke=NONE)
# robe folds
d.path("M430,470 C418,540 414,620 420,690", "Fold L", fill=NONE,
       stroke="#14101C", strokeWidth=5, opacity=50, cap="round")
d.path("M570,470 C582,540 586,620 580,690", "Fold R", fill=NONE,
       stroke="#14101C", strokeWidth=5, opacity=50, cap="round")
d.path("M500,450 C500,530 500,620 500,692", "Fold C", fill=NONE,
       stroke="#14101C", strokeWidth=4, opacity=35, cap="round")
# lantern light catching the left edge of the robe
d.path("M405,440 C372,505 362,605 366,690", "Robe rim light", fill=NONE,
       stroke="#E8B45A", strokeWidth=5, opacity=30, cap="round")

# --- arm + hand offering the key ring -------------------------------------------
d.path("M415,468 C448,490 466,505 476,512", "Sleeve", fill=NONE,
       stroke="#3A3242", strokeWidth=42, cap="round")
d.path("M415,468 C448,490 466,505 476,512", "Sleeve crease", fill=NONE,
       stroke="#14101C", strokeWidth=4, opacity=45, cap="round")
d.shape("ellipse", "Hand", x=462, y=500, width=30, height=22,
        fill="#8A7E90", stroke=INK, strokeWidth=3)

# --- the great ring of keys ------------------------------------------------------
d.shape("ellipse", "Key ring", x=466, y=512, width=68, height=68,
        fill=NONE, stroke="#C9A24C", strokeWidth=9)
d.shape("ellipse", "Key ring glint", x=472, y=518, width=20, height=16,
        fill="#FFE8A8", opacity=35, stroke=NONE)

def key(cx, tag):
    """One brass key hanging from the ring at (cx,582): bow, shaft, bit,
    and the parchment tag stamped with its subcommand tied below."""
    top = 582
    d.shape("ellipse", f"{tag} bow", x=cx-11, y=top, width=22, height=20,
            fill=NONE, stroke="#C9A24C", strokeWidth=5)
    d.path(f"M{cx},{top+20} L{cx},640", f"{tag} shaft",
           fill=NONE, stroke=BRASS, strokeWidth=7, cap="round")
    d.path(f"M{cx},624 L{cx+14},624 M{cx},636 L{cx+11},636",
           f"{tag} bit", fill=NONE, stroke=BRASS, strokeWidth=6, cap="round")
    # stamped tag tied below the bit
    d.path(f"M{cx},640 L{cx},656", f"{tag} tag string",
           fill=NONE, stroke="#8A7E90", strokeWidth=2, opacity=80)
    d.shape("rectangle", f"{tag} tag", x=cx-27, y=656, width=54, height=18,
            fill="#D8C9A2", stroke=INK, strokeWidth=2, radius=3)
    d.text(tag, f"{tag} tag text", x=cx, y=669, size=9.5,
           font="Virelai Sans", color="#3A2F22", justify="center")

for cx, tag in [(418, "RENDER"), (478, "PACK"), (538, "SCAN"), (598, "BOOK")]:
    key(cx, tag)

# --- captions ------------------------------------------------------------------
d.text("ROTKEEPER", "Name", x=500, y=930, size=58, font="Virelai Sans",
       color="#DCD4E6", justify="center")
r = d.text("THE DISPATCHER", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#9A8FA8", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("rk-dispatcher-V1R00")
