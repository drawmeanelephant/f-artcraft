#!/usr/bin/env python3
"""Coverage Ledger Cherub — mascot portrait V1R00.
Small cherub writing a golden tally mark into a ledger.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Coverage Ledger Cherub — Mascot Portrait", 1000, 1000)

INK = "#4A2E28"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2A1812"}, {"offset": 1, "color": "#120806"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#D4A96E"}, {"offset": 0.7, "color": "#A57948"},
    {"offset": 1, "color": "#6E4A2E"}]}}
SKIN = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#FBE3CE"}, {"offset": 0.72, "color": "#EFC0A0"},
    {"offset": 1, "color": "#D6977A"}]}}
WING = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F6EDDD"}, {"offset": 1, "color": "#D9C4A6"}]}}
PAGE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F4E7C8"}, {"offset": 1, "color": "#DCC79C"}]}}
COVER = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7A3B2E"}, {"offset": 1, "color": "#4E241C"}]}}
GOLD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F2CE5E"}, {"offset": 1, "color": "#C08A28"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#8A5F3A", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F0DCB4", strokeWidth=3, opacity=55)
# paper-fleck patina
for i, (x, y, w) in enumerate([(200,220,8),(790,240,7),(170,540,9),(820,560,8),
                               (250,750,7),(740,740,9),(140,400,6),(855,410,7),
                               (390,120,7),(600,115,8),(340,810,6),(660,810,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#8A5F36", opacity=40, stroke=NONE)

# --- wings (behind cherub) ----------------------------------------------------
d.path("M385,430 C330,400 285,415 275,470 C268,515 300,555 352,560 "
       "C330,540 335,520 355,512 C335,500 335,478 358,472 C340,455 355,430 385,430 Z",
       "Wing L", fill=WING, stroke=INK, strokeWidth=6, join="round")
d.path("M615,430 C670,400 715,415 725,470 C732,515 700,555 648,560 "
       "C670,540 665,520 645,512 C665,500 665,478 642,472 C660,455 645,430 615,430 Z",
       "Wing R", fill=WING, stroke=INK, strokeWidth=6, join="round")

# --- cherub -------------------------------------------------------------------
# body: plump torso, hidden below by ledger
d.path("M500,470 C575,470 622,520 626,585 C628,640 585,668 500,668 "
       "C415,668 372,640 374,585 C378,520 425,470 500,470 Z",
       "Body", fill=SKIN, stroke=INK, strokeWidth=7)
# belly shade
d.path("M420,610 C470,640 545,640 590,606 C545,626 468,626 420,610 Z",
       "Belly shade", fill="#D6977A", opacity=45, stroke=NONE)
# head
d.shape("ellipse", "Head", x=400, y=290, width=200, height=190, fill=SKIN,
        stroke=INK, strokeWidth=7)
d.shape("ellipse", "Head highlight", x=435, y=305, width=90, height=40,
        fill="#FFFFFF", opacity=25, stroke=NONE)
# curls: ring of small circles around the crown
for i, (x, y, w) in enumerate([(430,278,42),(478,262,46),(530,266,44),(570,290,38),
                               (402,308,36),(596,318,34)]):
    d.shape("ellipse", f"Curl {i+1}", x=x, y=y, width=w, height=w,
            fill="#C9894B", stroke=INK, strokeWidth=5)
# face: content eyes, tiny nose, soft smile, blush
d.path("M448,385 C455,392 467,392 473,385", "Eye L", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
d.path("M528,385 C535,392 547,392 553,385", "Eye R", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
d.path("M497,402 C500,407 504,407 506,403", "Nose", fill=NONE, stroke=INK,
       strokeWidth=4, cap="round")
d.path("M475,428 C492,440 515,440 530,428", "Smile", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
d.shape("ellipse", "Blush L", x=430, y=408, width=26, height=16, fill="#E89B8A",
        opacity=55, stroke=NONE)
d.shape("ellipse", "Blush R", x=546, y=408, width=26, height=16, fill="#E89B8A",
        opacity=55, stroke=NONE)
# arms: left rests on the ledger's left page edge, right grips the quill
d.path("M420,540 C395,565 370,585 352,596", "Arm L", fill=NONE, stroke=SKIN,
       strokeWidth=24, cap="round")
d.shape("ellipse", "Hand L", x=336, y=584, width=30, height=24, fill=SKIN,
        stroke=INK, strokeWidth=5)
d.path("M582,540 C575,565 565,585 552,600", "Arm R", fill=NONE, stroke=SKIN,
       strokeWidth=24, cap="round")
d.shape("ellipse", "Hand R", x=538, y=586, width=30, height=24, fill=SKIN,
        stroke=INK, strokeWidth=5)
# quill: nib on the page, shaft up through the right hand, vane above
d.path("M540,642 L596,548", "Quill shaft", fill=NONE, stroke="#8A5A34",
       strokeWidth=6, cap="round")
d.path("M596,548 C638,512 668,512 678,536 C659,528 646,534 638,548 "
       "C654,546 663,556 658,568 C646,556 630,556 620,560 "
       "C611,568 600,560 596,548 Z",
       "Quill vane", fill=WING, stroke=INK, strokeWidth=4, join="round")
d.path("M598,550 L644,520", "Quill spine", fill=NONE, stroke="#B09B7E",
       strokeWidth=3)

# --- the ledger, open toward the viewer ---------------------------------------
# cover underneath
d.path("M296,600 L498,628 L498,738 L296,710 Z M502,628 L704,600 L704,710 L502,738 Z",
       "Ledger cover", fill=COVER, stroke=INK, strokeWidth=6, join="round")
# pages
d.path("M306,606 L497,632 L497,726 L306,700 Z", "Page L", fill=PAGE,
       stroke=INK, strokeWidth=5, join="round")
d.path("M503,632 L694,606 L694,700 L503,726 Z", "Page R", fill=PAGE,
       stroke=INK, strokeWidth=5, join="round")
# ruled lines, left page
for i, y in enumerate([632, 654, 676, 698]):
    d.path(f"M318,{y+8} L488,{y+30}", f"Rule L{i+1}", fill=NONE,
           stroke="#B89B6E", strokeWidth=2, opacity=70)
# earlier tally columns, left page (faint ink)
for i, x in enumerate([340, 368, 396]):
    for j in range(4):
        d.path(f"M{x+j*6},648 L{x+j*6},676", f"Tally faint {i}-{j}", fill=NONE,
               stroke="#7A5A3C", strokeWidth=3, opacity=45, cap="round")
    d.path(f"M{x-4},674 L{x+22},650", f"Tally faint {i} gate", fill=NONE,
           stroke="#7A5A3C", strokeWidth=3, opacity=45, cap="round")
# golden tally on the right page, just penned
for j, x in enumerate([560, 580, 600, 620]):
    d.path(f"M{x},648 L{x},688", f"Gold tally {j+1}", fill=NONE, stroke=GOLD,
           strokeWidth=8, cap="round")
d.path("M552,684 L628,650", "Gold tally gate", fill=NONE, stroke=GOLD,
       strokeWidth=8, cap="round")
# golden glow + sparkles
d.shape("ellipse", "Tally glow", x=540, y=636, width=104, height=64,
        fill="#F2CE5E", opacity=18, stroke=NONE)
for i, (x, y, r) in enumerate([(545,640,4),(635,664,5),(655,640,3)]):
    d.shape("star", f"Sparkle {i+1}", cx=x, cy=y, radius1=r*2.2, radius2=r,
            points=4, fill="#F7DE8E", stroke=NONE, opacity=85)
# nib scratch where the quill lands
d.path("M540,636 L548,642", "Nib mark", fill=NONE, stroke=GOLD, strokeWidth=6,
       cap="round")

# --- captions ------------------------------------------------------------------
d.text("COVERAGE LEDGER CHERUB", "Name", x=500, y=930, size=54, font="Virelai Sans",
       color="#F0DCB4", justify="center")
r = d.text("KEEPER OF THE GOLDEN TALLY", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#C9A877", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("326.coverage-ledger-cherub-V1R00")
