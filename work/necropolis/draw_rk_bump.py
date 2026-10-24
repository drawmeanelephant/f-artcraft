#!/usr/bin/env python3
"""rc-bump.sh — The Version Stone. Necropolis plate V1R00.
A stonemason re-chiseling the great version tablet: the old semver lies
faintly legible beneath the fresh cuts, the mallet is mid-swing, gold
sparks and granite chips fly off the chisel's bite. One canonical stone —
the standing stones around it are conspicuously blank; no other version
may be carved anywhere. 1000x1000. Gradients + translucent shading."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("RC-Bump — Necropolis Plate", 1000, 1000)

INK = "#1A1E24"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#10141C"}, {"offset": 1, "color": "#06080C"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#46525E"}, {"offset": 0.7, "color": "#232C36"},
    {"offset": 1, "color": "#10161C"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2C3640"}, {"offset": 1, "color": "#121820"}]}}
GRANITE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#8A96A4"}, {"offset": 1, "color": "#4A5664"}]}}
GRANITE_DK = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5E6A78"}, {"offset": 1, "color": "#323C48"}]}}
STONE_DK = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3E4852"}, {"offset": 1, "color": "#222A32"}]}}
GOLD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F0C868"}, {"offset": 1, "color": "#B8842A"}]}}
WOOD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6A4E30"}, {"offset": 1, "color": "#3E2A18"}]}}
TUNIC = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#46505E"}, {"offset": 1, "color": "#262E38"}]}}
SKIN = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#D0AE84"}, {"offset": 1, "color": "#9A724F"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#66727E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D0D8E0", strokeWidth=3, opacity=40)
for i, (x, y, w) in enumerate([(193,233,8),(801,230,7),(157,524,9),(837,544,8),
                               (247,766,7),(753,749,9),(133,393,6),(864,391,7),
                               (391,113,7),(613,110,8),(333,823,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#525E6A", opacity=35, stroke=NONE)

# --- the other stones: standing blank, unmarked by decree -------------------------
for i, (x, top, w, h, op) in enumerate([(152,468,72,232,60),
                                        (236,500,56,200,45),
                                        (768,470,74,230,55)]):
    d.path(f"M{x},{top+h} L{x},{top+18} C{x},{top} {x+w},{top} {x+w},{top+18} "
           f"L{x+w},{top+h} Z", f"Blank stone {i+1}", fill=STONE_DK,
           opacity=op, stroke=INK, strokeWidth=3)
# conspicuously blank: bare chalk lines where no carving is permitted
d.path("M168,540 L208,540 M166,580 L210,580", "Blank marks", fill=NONE,
       stroke="#5E6A78", strokeWidth=3, opacity=25)

# --- floor ----------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0A0E12",
       strokeWidth=4, opacity=70)
d.shape("ellipse", "Stone shadow", x=270, y=682, width=340, height=20,
        fill="#02040A", opacity=55, stroke=NONE)
d.shape("ellipse", "Mason shadow", x=600, y=682, width=150, height=18,
        fill="#02040A", opacity=55, stroke=NONE)
# chips already fallen at the plinth
for i, (cx, cy, s) in enumerate([(265,706,10),(295,712,7),(590,704,9),(310,700,6)]):
    d.path(f"M{cx},{cy} L{cx+s},{cy-4} L{cx+s+3},{cy+3} L{cx+2},{cy+5} Z",
           f"Fallen chip {i+1}", fill=GRANITE_DK, stroke=INK, strokeWidth=2,
           join="round")

# --- the great version tablet -------------------------------------------------------
# plinth
d.path("M285,650 L575,650 L575,676 L285,676 Z", "Plinth top", fill=GRANITE_DK,
       stroke=INK, strokeWidth=4, join="round")
d.path("M270,676 L590,676 L590,700 L270,700 Z", "Plinth base", fill=STONE_DK,
       stroke=INK, strokeWidth=4, join="round")
# the stele
d.path("M305,650 L305,320 C305,278 332,258 370,258 L495,258 C533,258 560,278 "
       "560,320 L560,650 Z", "Version tablet", fill=GRANITE, stroke=INK,
       strokeWidth=6, join="round")
# edge light and a vein
d.path("M315,640 L315,325 C315,290 340,270 372,268", "Edge light", fill=NONE,
       stroke="#C8D2DC", strokeWidth=4, opacity=45, cap="round")
d.path("M320,560 C360,540 400,560 440,545 C470,534 500,540 540,525",
       "Stone vein", fill=NONE, stroke="#5E6A78", strokeWidth=3, opacity=45)
for i, (x, y, w) in enumerate([(340,300,6),(520,310,5),(335,600,7),(530,610,6),
                               (430,290,5),(370,625,5)]):
    d.shape("ellipse", f"Grain {i+1}", x=x, y=y, width=w, height=w,
            fill="#4A5664", opacity=50, stroke=NONE)

# the old semver: faintly legible beneath the fresh work — digits need Source Sans 3
r = d.text("1.9.4", "Old semver", x=430, y=352, size=38,
           font="Source Sans 3", color="#2E3540", justify="center")
if r and r.get("id"):
    d.cmd("object.setProps", "old semver fade", id=r["id"], opacity=30)
d.path("M342,338 L518,352", "Old strike", fill=NONE, stroke="#39424E",
       strokeWidth=3, opacity=40)
# snapped chalk lines for the fresh carving
d.path("M345,414 L520,414 M345,478 L520,478", "Chalk guides", fill=NONE,
       stroke="#D8E0E8", strokeWidth=2, opacity=30)
# the new cut: carved digits, incised dark then pale relief on top
d.text("2.0.0", "New cut dark", x=431, y=462, size=56, font="Source Sans 3",
       color="#232A32", justify="center")
d.text("2.0.0", "New cut", x=429, y=459, size=56, font="Source Sans 3",
       color="#D8E0E8", justify="center")
# fresh chisel kisses around the new figures
for i, (x1, y1, x2, y2) in enumerate([(352,430,368,424),(500,436,516,430),
                                      (356,486,372,492),(498,488,514,482)]):
    d.path(f"M{x1},{y1} L{x2},{y2}", f"Fresh cut {i+1}", fill=NONE,
           stroke="#E8EEF4", strokeWidth=3, opacity=70, cap="round")

# --- the stonemason, mallet mid-swing ------------------------------------------------
# boots + legs
d.path("M628,684 L662,684 L662,694 L628,694 Z", "Boot L", fill="#181410",
       stroke=INK, strokeWidth=3, join="round")
d.path("M668,684 L702,684 L702,694 L668,694 Z", "Boot R", fill="#181410",
       stroke=INK, strokeWidth=3, join="round")
d.path("M636,684 L640,632 M686,684 L682,632", "Legs", fill=NONE,
       stroke="#222A32", strokeWidth=14, cap="round")
# tunic + apron
d.path("M628,492 C618,505 614,528 616,555 L622,640 L700,640 L704,552 "
       "C706,526 700,504 688,494 Z", "Tunic", fill=TUNIC, stroke=INK,
       strokeWidth=5, join="round")
d.path("M636,540 L682,540 L686,640 L640,640 Z", "Work apron", fill="#3A3328",
       stroke="#241E18", strokeWidth=3, join="round")
# head, dust cap, facing the stone
d.shape("ellipse", "Head", x=636, y=434, width=36, height=40,
        fill=SKIN, stroke=INK, strokeWidth=4)
d.path("M634,452 C632,430 648,420 660,422 C674,424 678,438 674,452 L668,446 "
       "C660,438 646,438 640,446 Z", "Dust cap", fill=TUNIC, stroke=INK,
       strokeWidth=3, join="round")
d.shape("ellipse", "Eye", x=643, y=452, width=5, height=5,
        fill="#241812", stroke=NONE)
d.path("M640,466 L654,470", "Beard stubble", fill=NONE, stroke="#8A7454",
       strokeWidth=3, cap="round")
# left arm out, chisel against the tablet edge
d.path("M632,512 C610,505 594,496 580,486", "Chisel arm", fill=NONE,
       stroke="#3A4450", strokeWidth=12, cap="round")
d.shape("ellipse", "Chisel hand", x=566, y=478, width=18, height=15,
        fill=SKIN, stroke=INK, strokeWidth=3)
d.path("M566,484 L556,476", "Chisel", fill=NONE, stroke="#B8C4D0",
       strokeWidth=5, cap="round")
d.path("M558,474 L552,470", "Chisel tip", fill=NONE, stroke="#F0D9A0",
       strokeWidth=3, cap="round")
# right arm raised, mallet mid-swing
d.path("M690,500 C704,482 714,462 716,440", "Mallet arm", fill=NONE,
       stroke="#3A4450", strokeWidth=12, cap="round")
d.shape("ellipse", "Mallet hand", x=708, y=428, width=18, height=15,
        fill=SKIN, stroke=INK, strokeWidth=3)
d.path("M714,434 L688,392", "Mallet handle", fill=NONE, stroke="#6A4E30",
       strokeWidth=7, cap="round")
d.path(rot_rect_path(680, 380, 52, 26, -52), "Mallet head", fill=WOOD,
       stroke=INK, strokeWidth=4, join="round")
# the swing's trail
d.path("M742,436 C738,402 724,378 700,364", "Swing arc 1", fill=NONE,
       stroke="#D0D8E0", strokeWidth=3, opacity=35)
d.path("M760,450 C758,410 742,382 714,364", "Swing arc 2", fill=NONE,
       stroke="#D0D8E0", strokeWidth=3, opacity=22)

# --- sparks + chips at the bite -------------------------------------------------------
for i, (sx, sy, r_) in enumerate([(556,470,10),(542,452,7),(570,450,8),
                                  (552,496,6),(578,486,6)]):
    d.path(f"M{sx-r_},{sy} L{sx+r_},{sy} M{sx},{sy-r_} L{sx},{sy+r_}",
           f"Spark {i+1}", fill=NONE, stroke="#F0C868", strokeWidth=3,
           opacity=90, cap="round")
d.shape("ellipse", "Spark glow", x=538, y=448, width=44, height=44,
        fill="#F0C868", opacity=15, stroke=NONE)
for i, (cx, cy, s, dx, dy) in enumerate([(575,462,8,10,-8),(586,478,7,14,-2),
                                         (570,492,6,10,8),(548,444,5,-8,-10)]):
    d.path(f"M{cx},{cy} L{cx+s},{cy+dy*0.3:.0f} L{cx+s-3},{cy+s} "
           f"L{cx-3},{cy+s-4} Z", f"Flying chip {i+1}", fill=GRANITE_DK,
           stroke=INK, strokeWidth=2, join="round")

# --- captions ------------------------------------------------------------------
d.text("RC-BUMP", "Name", x=500, y=930, size=58, font="Virelai Sans",
       color="#DFE4EA", justify="center")
r = d.text("ONE CANONICAL STONE", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#A6B0BC", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("rk-bump-V1R00")
