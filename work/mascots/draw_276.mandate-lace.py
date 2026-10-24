#!/usr/bin/env python3
"""Mandate Lace — mascot portrait V1R00.
A mascot dressing an iron fist in a hand-woven lace glove, a pastel
compliance checklist standing beside. The requirement is unchanged;
it is now heirloom. 1000x1000.
Gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Mandate Lace — Mascot Portrait", 1000, 1000)

INK = "#2C2418"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#161B1C"}, {"offset": 1, "color": "#090B0C"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#98A49A"}, {"offset": 0.7, "color": "#6C7A70"},
    {"offset": 1, "color": "#424E46"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4A544C"}, {"offset": 1, "color": "#20261F"}]}}
IRON_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7E8894"}, {"offset": 0.55, "color": "#4C545E"},
    {"offset": 1, "color": "#2A2E34"}]}}
IRON_DARK = "#22262C"
IRON_SHEEN = "#A8B4C2"
LACE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F6F0DE"}, {"offset": 1, "color": "#D2C6A8"}]}}
LACE_LINE = "#B4A684"
FUR_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#C2AE92"}, {"offset": 0.7, "color": "#9E8A70"},
    {"offset": 1, "color": "#74634E"}]}}
FUR_MID = "#9E8A70"
MINT = "#CFE6D6"
BLUSH = "#E4C9C2"
CHECK = "#3E6A50"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#8FA092", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#DCE8DA", strokeWidth=3, opacity=50)
for i, (x, y, w) in enumerate([(193,234,8),(801,229,7),(157,526,9),(837,544,8),
                               (246,766,7),(754,748,9),(133,394,6),(865,389,7),
                               (391,112,7),(613,109,8),(333,824,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#46544A", opacity=45, stroke=NONE)

# --- floor ----------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#141A14",
       strokeWidth=4, opacity=70)

# --- the iron fist, raised center-right ---------------------------------------------
d.shape("ellipse", "Fist shadow", x=390, y=672, width=270, height=20,
        fill="#0E120E", opacity=35, stroke=NONE)
# wrist/cuff base
d.path("M448,640 L448,560 L590,560 L590,640 Z", "Wrist base",
       fill=IRON_GRAD, stroke=INK, strokeWidth=4)
# palm block with knuckle bumps on top
d.path("M420,600 L420,430 "
       "C420,392 436,374 462,372 "
       "C468,342 502,342 510,372 "
       "C518,340 554,340 562,372 "
       "C570,344 604,346 610,376 "
       "C632,382 642,402 640,432 "
       "L640,600 Z",
       "Fist", fill=IRON_GRAD, stroke=INK, strokeWidth=5)
# knuckle separations + rivets
for i, x in enumerate([486, 536, 584]):
    d.path(f"M{x},372 L{x},452", f"Knuckle seam {i+1}", fill=NONE,
           stroke=IRON_DARK, strokeWidth=3.5, opacity=65)
    d.shape("ellipse", f"Rivet {i+1}", x=x-4, y=462, width=8, height=8,
            fill=IRON_DARK, opacity=70, stroke=NONE)
# plate sheen + edge highlight
d.path("M436,400 C436,388 446,380 458,378", "Knuckle sheen", fill=NONE,
       stroke=IRON_SHEEN, strokeWidth=6, opacity=55, cap="round")
d.path("M430,440 L430,580", "Fist rim light", fill=NONE,
       stroke=IRON_SHEEN, strokeWidth=4, opacity=35, cap="round")
# thumb plate resting against the right side
d.path("M618,470 C652,470 668,494 660,524 C652,552 626,562 606,548 "
       "C614,524 616,496 618,470 Z",
       "Thumb", fill=IRON_GRAD, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Thumb rivet", x=630, y=508, width=9, height=9,
        fill=IRON_DARK, opacity=70, stroke=NONE)

# --- the lace glove, drawn on over the iron ------------------------------------------
# glove body: scalloped hem at mid-finger, flaring to a wide cuff
d.path("M414,470 "
       "C426,452 446,452 458,470 "
       "C470,452 490,452 502,470 "
       "C514,452 534,452 546,470 "
       "C558,452 578,452 590,470 "
       "C602,452 622,452 634,470 "
       "L656,660 L392,660 Z",
       "Lace glove", fill=LACE_GRAD, stroke=INK, strokeWidth=4, opacity=92)
# cuff band + eyelet row
d.path("M392,620 L656,620 L656,660 L392,660 Z", "Cuff band",
       fill="#E4D8BC", stroke=INK, strokeWidth=3.5)
for i, x in enumerate([416, 460, 504, 548, 592, 636]):
    d.shape("ellipse", f"Cuff eyelet {i+1}", x=x, y=634, width=12, height=12,
            fill=NONE, stroke=LACE_LINE, strokeWidth=2.5)
# lace weave: diagonal mesh, eyelet dots, two floral motifs
for i, (x0, x1) in enumerate([(430,470),(478,518),(526,566),(574,614)]):
    d.path(f"M{x0},560 L{x1},520", f"Mesh a{i+1}", fill=NONE,
           stroke=LACE_LINE, strokeWidth=1.8, opacity=55)
    d.path(f"M{x1},560 L{x0},520", f"Mesh b{i+1}", fill=NONE,
           stroke=LACE_LINE, strokeWidth=1.8, opacity=55)
for i, (x, y) in enumerate([(440,590),(480,585),(520,592),(560,586),(600,590),
                              (460,540),(540,540)]):
    d.shape("ellipse", f"Weave dot {i+1}", x=x, y=y, width=7, height=7,
            fill=NONE, stroke=LACE_LINE, strokeWidth=1.8, opacity=70)
for i, (cx, cy) in enumerate([(500,540),(580,545)]):
    d.shape("ellipse", f"Flower {i+1} core", x=cx-4, y=cy-4, width=9, height=9,
            fill=LACE_LINE, opacity=60, stroke=NONE)
    for j, (px, py) in enumerate([(cx-13,cy),(cx+5,cy),(cx-4,cy-13),(cx-4,cy+5)]):
        d.shape("ellipse", f"Flower {i+1} petal {j+1}", x=px, y=py,
                width=8, height=8, fill=NONE, stroke=LACE_LINE,
                strokeWidth=2, opacity=70)
# loose thread curling off the weave
d.path("M470,660 C462,676 472,690 488,688 C502,686 504,672 494,668",
       "Loose thread", fill=NONE, stroke=LACE_LINE, strokeWidth=2.5,
       opacity=80, cap="round")

# --- the pastel compliance checklist, standing beside ---------------------------------
d.path(rot_rect_path(724, 556, 150, 178, 7), "Checklist shadow",
       fill="#0E120E", opacity=30, stroke=NONE)
d.path(rot_rect_path(716, 546, 150, 178, 7), "Checklist",
       fill=MINT, stroke=INK, strokeWidth=4)
d.path(rot_rect_path(716, 480, 132, 16, 7), "Checklist head",
       fill=BLUSH, opacity=85, stroke=NONE)
for i, (cx, cy, done) in enumerate([(680,508,1),(676,540,1),(672,572,1),(668,604,0)]):
    d.path(rot_rect_path(cx, cy, 15, 15, 7), f"Box {i+1}", fill="#F6F2E4",
           stroke=INK, strokeWidth=2.5)
    if done:
        d.path(f"M{cx-6},{cy} L{cx-2},{cy+5} L{cx+7},{cy-6}", f"Tick {i+1}",
               fill=NONE, stroke=CHECK, strokeWidth=3.5, cap="round")
    d.path(rot_rect_path(cx+48, cy+1, 62, 4, 7), f"Item rule {i+1}",
           fill=NONE, stroke="#8FAE9A", strokeWidth=2.5, opacity=75)
# little easel legs under the card
d.path("M672,646 L656,700", "Easel leg L", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
d.path("M756,658 L768,702", "Easel leg R", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")

# --- the mascot, tugging the glove on ---------------------------------------------------
d.shape("ellipse", "Mascot shadow", x=180, y=684, width=170, height=18,
        fill="#0E120E", opacity=35, stroke=NONE)
# body leaning back against the pull
d.path("M250,688 C222,640 218,560 246,506 C268,462 330,458 356,502 "
       "C378,540 380,610 362,688 Z",
       "Body", fill=FUR_GRAD, stroke=INK, strokeWidth=5)
d.shape("ellipse", "Head", x=236, y=372, width=126, height=122,
        fill=FUR_GRAD, stroke=INK, strokeWidth=5)
for ex in (246, 350):
    d.shape("ellipse", f"Ear {ex}", x=ex-10, y=368, width=25, height=23,
            fill=FUR_MID, stroke=INK, strokeWidth=3.5)
# effort face: squinting toward the work
d.path("M266,436 C272,431 280,431 286,437", "Eye L", fill=NONE,
       stroke=INK, strokeWidth=4.5, cap="round")
d.path("M310,437 C316,432 324,432 330,438", "Eye R", fill=NONE,
       stroke=INK, strokeWidth=4.5, cap="round")
d.path("M282,466 C290,470 302,470 310,465", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
# both arms extended forward, gripping the stretched lace flap
d.path("M348,514 C340,528 332,540 320,550", "Arm upper", fill=NONE,
       stroke=FUR_MID, strokeWidth=15, cap="round")
d.path("M344,560 C336,564 328,568 318,572", "Arm lower", fill=NONE,
       stroke=FUR_MID, strokeWidth=15, cap="round")
# the flap: lace pulled taut off the glove's edge into her paws
d.path("M392,536 C360,528 336,534 312,550 C326,570 356,584 392,592 Z",
       "Pulled lace flap", fill=LACE_GRAD, stroke=INK, strokeWidth=3.5)
d.path("M330,548 C352,544 372,548 388,556", "Flap crease", fill=NONE,
       stroke=LACE_LINE, strokeWidth=2.5, opacity=70)
d.shape("ellipse", "Paw upper", x=302, y=538, width=26, height=22,
        fill=FUR_MID, stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Paw lower", x=296, y=564, width=26, height=22,
        fill=FUR_MID, stroke=INK, strokeWidth=3.5)

# --- captions -------------------------------------------------------------------------
d.text("MANDATE LACE", "Name", x=500, y=930, size=58,
       font="Virelai Sans", color="#E8F0E4", justify="center")
r = d.text("THE REQUIREMENT, NOW HEIRLOOM", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#BCCCB6", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("276.mandate-lace-V1R00")
