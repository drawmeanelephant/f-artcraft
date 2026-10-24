#!/usr/bin/env python3
"""rc-init.sh — The Groundbreaking. Necropolis plate V1R00.
A ceremonial first shovel breaks ground for a new plot at dawn: the sod is
folded back carefully, respectfully, nothing existing disturbed, and a
small carved marker already waits — NON-DESTRUCTIVE.
1000x1000. Gradients + translucent shading."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("RC-Init — Necropolis Plate", 1000, 1000)

INK = "#201812"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#131720"}, {"offset": 1, "color": "#08090D"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#8A7A5E"}, {"offset": 0.68, "color": "#4E463A"},
    {"offset": 1, "color": "#201C16"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3A3226"}, {"offset": 1, "color": "#171209"}]}}
SOIL = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5C4326"}, {"offset": 1, "color": "#2E1F10"}]}}
SOIL_DK = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3A2917"}, {"offset": 1, "color": "#1C1208"}]}}
TURF = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7A8A52"}, {"offset": 1, "color": "#46522E"}]}}
STONE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#8D8A7E"}, {"offset": 1, "color": "#4E4A40"}]}}
WOOD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#8A6238"}, {"offset": 1, "color": "#53371C"}]}}
STEEL = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#B8BCC0"}, {"offset": 1, "color": "#5E6468"}]}}
GOLD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F0C868"}, {"offset": 1, "color": "#B8842A"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#6E6858", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#DCD4BC", strokeWidth=3, opacity=40)
for i, (x, y, w) in enumerate([(193,233,8),(801,230,7),(157,524,9),(837,544,8),
                               (247,766,7),(753,749,9),(133,393,6),(864,391,7),
                               (391,113,7),(613,110,8),(333,823,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#6E6455", opacity=35, stroke=NONE)

# --- dawn: low sun + mist, before the ground covers the horizon ------------------
d.shape("ellipse", "Dawn glow", x=430, y=460, width=400, height=240,
        fill="#E8C87A", opacity=16, stroke=NONE)
d.shape("ellipse", "Sun sliver", x=618, y=636, width=96, height=60,
        fill="#F0D9A0", opacity=85, stroke=NONE)
for i, (x, y, w, op) in enumerate([(260,505,330,20),(430,545,380,16),
                                   (250,585,280,13)]):
    d.path(f"M{x},{y} C{x+w*0.4},{y-6} {x+w*0.6},{y+6} {x+w},{y}",
           f"Mist {i+1}", fill=NONE, stroke="#D8CFAE", strokeWidth=8,
           opacity=op, cap="round")
# two distant birds, barely awake
d.path("M310,340 C318,332 326,332 334,340 M334,340 C342,332 350,332 358,340",
       "Bird 1", fill=NONE, stroke="#4A4438", strokeWidth=3, opacity=60,
       cap="round")
d.path("M370,310 C376,304 382,304 388,310 M388,310 C394,304 400,304 406,310",
       "Bird 2", fill=NONE, stroke="#4A4438", strokeWidth=3, opacity=45,
       cap="round")

# --- floor ----------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0B0805",
       strokeWidth=4, opacity=70)
d.shape("ellipse", "Marker shadow", x=255, y=690, width=180, height=14,
        fill="#040302", opacity=50, stroke=NONE)
d.shape("ellipse", "Dig shadow", x=560, y=692, width=260, height=16,
        fill="#040302", opacity=50, stroke=NONE)

# --- the carved marker, already waiting ------------------------------------------
d.path("M260,700 L260,608 C260,584 278,570 302,570 L368,570 C392,570 410,584 "
       "410,608 L410,700 Z", "Marker", fill=STONE, stroke=INK,
       strokeWidth=5, join="round")
# incised border
d.path("M273,690 L273,612 C273,594 286,583 304,583 L366,583 C384,583 397,594 "
       "397,612 L397,690 Z", "Marker border", fill=NONE, stroke="#3A362E",
       strokeWidth=2, opacity=70, join="round")
d.text("NON-", "Marker line 1", x=335, y=624, size=15, font="Source Sans 3",
       color="#2E2A22", justify="center")
d.text("DESTRUCTIVE", "Marker line 2", x=335, y=650, size=15,
       font="Source Sans 3", color="#2E2A22", justify="center")
# chisel nicks at the corners — freshly carved
for i, (x1, y1, x2, y2) in enumerate([(274,592,288,598),(396,590,384,598),
                                      (278,678,290,674)]):
    d.path(f"M{x1},{y1} L{x2},{y2}", f"Nick {i+1}", fill=NONE,
           stroke="#BDBAAE", strokeWidth=2, opacity=60, cap="round")

# --- the new plot: opened earth ---------------------------------------------------
# the cut: a clean dark scoop, nothing broken
d.path("M560,700 C570,672 620,660 680,660 C720,660 748,674 752,700 Z",
       "The cut", fill=SOIL_DK, stroke=INK, strokeWidth=4, join="round")
d.path("M580,688 C620,676 700,676 736,690", "Cut shadow", fill=NONE,
       stroke="#0D0804", strokeWidth=6, opacity=60, cap="round")
# heap of fresh spoil, lumpy but tidy, behind the cut
d.path("M600,664 C596,640 622,624 648,628 C658,612 690,610 700,626 "
       "C724,622 744,640 738,664 Z", "Spoil heap", fill=SOIL, stroke=INK,
       strokeWidth=4, join="round")
for i, (x, y, w) in enumerate([(628,644,10),(668,634,8),(708,648,9)]):
    d.shape("ellipse", f"Clod {i+1}", x=x, y=y, width=w, height=w,
            fill="#2E1F10", opacity=60, stroke=NONE)
# loose soil pearls at the cut's lip
for i, (x, y, w) in enumerate([(566,676,8),(598,668,6),(742,678,7),
                               (560,692,5)]):
    d.shape("ellipse", f"Loose soil {i+1}", x=x, y=y, width=w, height=w,
            fill="#5C4326", stroke=INK, strokeWidth=2)

# --- the sod, folded back like a page ----------------------------------------------
# underside: soil dark, grass edge curled away from the cut
d.path("M470,690 C466,664 488,648 518,650 C540,652 552,664 550,686 "
       "C530,694 492,696 470,690 Z", "Sod underside", fill=SOIL_DK,
       stroke=INK, strokeWidth=4, join="round")
d.path("M470,690 C460,672 462,652 482,644 C500,638 522,642 534,652 "
       "C514,648 490,652 480,668 C476,676 474,684 470,690 Z",
       "Sod fold", fill=TURF, stroke=INK, strokeWidth=4, join="round")
# grass blades on the flap
for i, (x0, y0, x1, y1) in enumerate([(478,650,474,640),(492,646,492,634),
                                      (508,644,512,634),(522,650,528,642)]):
    d.path(f"M{x0},{y0} L{x1},{y1}", f"Blade {i+1}", fill=NONE,
           stroke="#8FA05C", strokeWidth=3, cap="round")
# dew on the folded turf
for i, (x, y, w) in enumerate([(484,658,4),(504,654,3),(520,660,3)]):
    d.shape("ellipse", f"Dew {i+1}", x=x, y=y, width=w, height=w,
            fill="#E8F0D8", opacity=60, stroke=NONE)

# --- the ceremonial shovel, blade in the new earth ----------------------------------
# shaft: driven at a slight lean into the heap
d.path("M622,648 L576,428", "Shaft", fill=NONE, stroke="#7A5630",
       strokeWidth=11, cap="round")
d.path("M618,650 L574,430", "Shaft light", fill=NONE, stroke="#A87C48",
       strokeWidth=4, cap="round", opacity=80)
# D-handle
d.path("M564,428 C552,408 566,388 584,392 C600,396 604,416 592,430 Z",
       "D-handle", fill=WOOD, stroke=INK, strokeWidth=4, join="round")
# ceremonial ribbon tied under the grip
d.path("M574,442 C560,438 550,444 548,456 C560,460 570,454 574,442 Z",
       "Ribbon loop L", fill=GOLD, stroke=INK, strokeWidth=3, join="round")
d.path("M578,444 C592,442 600,450 600,460 C588,462 580,456 578,444 Z",
       "Ribbon loop R", fill=GOLD, stroke=INK, strokeWidth=3, join="round")
d.shape("ellipse", "Ribbon knot", x=570, y=438, width=14, height=12,
        fill="#B8842A", stroke=INK, strokeWidth=3)
d.path("M572,452 C568,470 564,480 556,488", "Ribbon tail", fill=NONE,
       stroke="#B8842A", strokeWidth=4, cap="round")
# spade: sunk into the heap
d.path("M600,668 C594,636 604,612 622,604 C642,614 648,640 640,668 Z",
       "Spade", fill=STEEL, stroke=INK, strokeWidth=4, join="round")
d.path("M606,628 L640,622", "Spade socket", fill=NONE, stroke="#3E4448",
       strokeWidth=3, opacity=70, cap="round")
d.path("M610,654 C610,636 615,622 623,614", "Spade shine", fill=NONE,
       stroke="#E8EEF2", strokeWidth=3, opacity=70, cap="round")

# --- dewy grass along the plot edge -------------------------------------------------
for i, (x0, y0, x1, y1) in enumerate([(430,700,426,688),(448,700,450,686),
                                      (770,700,774,688),(792,700,790,690),
                                      (414,700,416,692)]):
    d.path(f"M{x0},{y0} L{x1},{y1}", f"Edge grass {i+1}", fill=NONE,
           stroke="#5A6A3E", strokeWidth=3, cap="round")

# --- captions ------------------------------------------------------------------
d.text("RC-INIT", "Name", x=500, y=930, size=58, font="Virelai Sans",
       color="#E4DCC4", justify="center")
r = d.text("BREAKING GROUND, GENTLY", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#ADA287", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("rk-init-V1R00")
