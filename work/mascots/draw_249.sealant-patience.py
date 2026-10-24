#!/usr/bin/env python3
"""Sealant Patience — mascot portrait V1R00.
A resin mascot mid-grip on a torn file: edges already set, center still
moving, one slow drip descending. The unresolved text stays legible under
the bond — it does not obscure the problem, it laminates it. 1000x1000.
Gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Sealant Patience — Mascot Portrait", 1000, 1000)

INK = "#241E14"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#18201C"}, {"offset": 1, "color": "#090D0B"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#6E7A64"}, {"offset": 0.7, "color": "#46523F"},
    {"offset": 1, "color": "#212820"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3E4839"}, {"offset": 1, "color": "#1A2018"}]}}
MANILA = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E2C896"}, {"offset": 1, "color": "#B2945E"}]}}
MANILA_DK = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#C8AA72"}, {"offset": 1, "color": "#8E7040"}]}}
RESIN = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F0C65E"}, {"offset": 0.65, "color": "#D89A32"},
    {"offset": 1, "color": "#96601C"}]}}
RESIN_DK = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#C88A2E"}, {"offset": 1, "color": "#7E5016"}]}}
RULE = "#9E8862"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#8A9678", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8E0C4", strokeWidth=3, opacity=45)
# amber halo: the slow warmth of something curing
d.shape("ellipse", "Resin halo", x=270, y=250, width=460, height=440,
        fill="#E8C06A", opacity=10, stroke=NONE)
for i, (x, y, w) in enumerate([(190,230,8),(804,232,7),(158,516,9),(836,540,8),
                               (252,764,7),(750,746,9),(134,388,6),(864,390,7),
                               (394,112,7),(612,110,8),(334,820,6),(668,820,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#5E6852", opacity=45, stroke=NONE)

# --- floor: bottom segment closed on the disc's own arc -------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#121810",
       strokeWidth=4, opacity=70)

# --- the unresolved file: a folder torn across its middle -------------------------
d.shape("ellipse", "File shadow", x=350, y=680, width=310, height=22,
        fill="#0C100A", opacity=50, stroke=NONE)
# bottom half: still standing, still unresolved
d.path("M372,540 L368,692 L646,692 L648,540 "
       "L612,556 L578,544 L540,560 L500,548 L462,562 L424,548 L388,560 Z",
       "File bottom", fill=MANILA, stroke=INK, strokeWidth=5, join="round")
# ruled lines on the bottom half, running under the tear
for i in range(3):
    y = 600 + i*26
    d.path(f"M398,{y} L620,{y-2}", f"Bot rule {i+1}", fill=NONE,
           stroke=RULE, strokeWidth=3, opacity=60)
d.path("M398,666 L520,664", "Bot rule stub", fill=NONE, stroke=RULE,
       strokeWidth=3, opacity=45)
# top half: peeled back but not gone — it leans left, hanging by the bond
d.path("M382,332 L356,494 L390,482 L428,496 L466,478 L505,494 L544,480 "
       "L582,494 L620,480 L642,494 L640,332 Z",
       "File top", fill=MANILA_DK, stroke=INK, strokeWidth=5, join="round")
# folder tab: it was a file before it was a gap
d.path("M382,332 L382,306 L452,306 L466,332 Z", "Folder tab",
       fill=MANILA_DK, stroke=INK, strokeWidth=5, join="round")
for i in range(3):
    y = 356 + i*26
    d.path(f"M392,{y} L616,{y}", f"Top rule {i+1}", fill=NONE,
           stroke="#8E7448", strokeWidth=3, opacity=60)
# the PENDING overstamp: Source Sans 3 — Virelai keeps its dignity elsewhere
d.path("M452,388 L586,388 L586,420 L452,420 Z", "Pending box", fill=NONE,
       stroke="#A8463E", strokeWidth=4, opacity=75)
d.text("PENDING", "Pending", x=519, y=414, size=24, font="Source Sans 3",
       color="#A8463E", justify="center")

# --- the bond: resin bridging the tear, set at the edges, wet at the middle -------
# main seam blob: gripped onto both torn edges
d.path("M398,500 C420,472 460,462 502,462 C556,462 610,478 630,506 "
       "C644,526 636,548 612,556 C580,568 540,560 502,562 "
       "C462,564 424,556 404,538 C390,524 388,512 398,500 Z",
       "Seam", fill=RESIN, stroke=INK, strokeWidth=5, join="round", opacity=92)
# where the bond wraps the edges: set, opaque, already structural
d.path("M404,496 L424,548 L388,560 L380,528 Z", "Set L",
       fill=RESIN_DK, stroke=INK, strokeWidth=4, join="round")
d.path("M612,502 L620,480 L650,496 L636,540 Z", "Set R",
       fill=RESIN_DK, stroke=INK, strokeWidth=4, join="round")
# the text preserved under the bond: legible through the laminate
d.path("M430,510 L520,510 M424,526 L560,526 M448,542 L540,542",
       "Laminated lines", fill=NONE, stroke="#7A5416", strokeWidth=3,
       cap="round", opacity=40)
# wet center: the gloss of a cure that has not finished
d.shape("ellipse", "Seam gloss", x=440, y=474, width=130, height=38,
        fill="#FFF2CC", opacity=45, stroke=NONE)
d.shape("ellipse", "Seam gloss 2", x=560, y=500, width=60, height=20,
        fill="#FFF2CC", opacity=30, stroke=NONE)
# one slow drip: the gap closing at its own speed
d.path("M520,562 C516,584 514,604 518,622 C522,634 534,634 538,622 "
       "C542,604 540,584 534,562 Z",
       "Drip", fill=RESIN, stroke=INK, strokeWidth=4, join="round")
d.shape("ellipse", "Drip bead", x=516, y=622, width=24, height=26,
        fill=RESIN, stroke=INK, strokeWidth=4)
d.path("M524,566 C522,584 521,600 523,614", "Drip sheen", fill=NONE,
       stroke="#FFF2CC", strokeWidth=3, cap="round", opacity=60)
# a second bead pooled on the floor: patience, accumulated
d.shape("ellipse", "Pool", x=500, y=682, width=64, height=16,
        fill=RESIN, stroke=INK, strokeWidth=3, opacity=85)
d.shape("ellipse", "Pool hi", x=510, y=684, width=26, height=6,
        fill="#FFF2CC", opacity=50, stroke=NONE)

# --- the face: mid-grip, unhurried, soft at the center ----------------------------
# half-lidded eyes: it has watched files skin over before
d.path("M452,500 C460,492 474,492 482,500", "Lid L", fill=NONE,
       stroke=INK, strokeWidth=6, cap="round")
d.path("M534,500 C542,492 556,492 564,500", "Lid R", fill=NONE,
       stroke=INK, strokeWidth=6, cap="round")
d.shape("ellipse", "Pupil L", x=462, y=502, width=8, height=7,
        fill=INK, stroke=NONE, opacity=80)
d.shape("ellipse", "Pupil R", x=544, y=502, width=8, height=7,
        fill=INK, stroke=NONE, opacity=80)
# level, unbothered mouth
d.path("M486,530 C496,536 514,536 524,530", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
# amber blush: effort is not the same as hurry
d.shape("ellipse", "Cheek L", x=432, y=514, width=22, height=11,
        fill="#B8781E", opacity=45, stroke=NONE)
d.shape("ellipse", "Cheek R", x=560, y=514, width=22, height=11,
        fill="#B8781E", opacity=45, stroke=NONE)

# --- small escape beads: tacky edges still finding their level ---------------------
for i, (x, y, w) in enumerate([(392,480,10),(636,540,9),(410,556,7),(622,470,8)]):
    d.shape("ellipse", f"Bead {i+1}", x=x, y=y, width=w, height=w,
            fill=RESIN, stroke=INK, strokeWidth=3, opacity=80)

# --- captions ---------------------------------------------------------------------
d.text("SEALANT PATIENCE", "Name", x=500, y=930, size=58,
       font="Virelai Sans", color="#E4D9B0", justify="center")
r = d.text("THE WAIT, INSTITUTIONALIZED", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#A8AE8E", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("249.sealant-patience-V1R00")
