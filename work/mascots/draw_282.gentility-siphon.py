#!/usr/bin/env python3
"""Gentility Siphon — mascot portrait V1R00.
A courteous figure in a sweater vest smiles its fixed professional smile
while one soft hand slides a ticket into the DONE column. On the board the
OPEN cards still steam with justified fury; the wisps rise red, bend toward
the siphon, and arrive at its shoulder as calm pale motes — fury in,
minutes out. The ticket it closes carries a real key. 1000x1000.
Gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Gentility Siphon — Mascot Portrait", 1000, 1000)

INK = "#1C2430"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#121B26"}, {"offset": 1, "color": "#070A10"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#7E8CA0"}, {"offset": 0.7, "color": "#4C586C"},
    {"offset": 1, "color": "#252E3E"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2E3A48"}, {"offset": 1, "color": "#141B24"}]}}
CARD_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#EAEDF0"}, {"offset": 1, "color": "#C4CAD2"}]}}
HOT_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E8BCAC"}, {"offset": 1, "color": "#C89A8C"}]}}
VEST_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5C8A82"}, {"offset": 1, "color": "#33524C"}]}}
FACE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F0E4CE"}, {"offset": 1, "color": "#D4C2A2"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#96A2B4", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D6DEE8", strokeWidth=3, opacity=50)
for i, (x, y, w) in enumerate([(193,234,8),(801,229,7),(157,526,9),(837,544,8),
                               (246,766,7),(754,748,9),(133,394,6),(865,389,7),
                               (391,112,7),(613,109,8),(333,824,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#465264", opacity=50, stroke=NONE)

# --- floor ---------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0A0F16",
       strokeWidth=4, opacity=70)

# --- the board: three columns, one quietly closing ticket ------------------------
d.shape("rectangle", "Board", x=196, y=236, width=392, height=380,
        fill="#1E2836", stroke="#3C4858", strokeWidth=5, radius=10,
        opacity=95)
for i, cx in enumerate([326, 456]):
    d.path(f"M{cx},252 L{cx},600", f"Column sep {i+1}", fill=NONE,
           stroke="#3C4858", strokeWidth=3, opacity=80)
d.text("OPEN", "Col head 1", x=261, y=272, size=12, font="Virelai Sans",
       color="#D88A78", justify="center")
d.text("DOING", "Col head 2", x=391, y=272, size=12, font="Virelai Sans",
       color="#C8B88A", justify="center")
d.text("DONE", "Col head 3", x=521, y=272, size=12, font="Virelai Sans",
       color="#9EC49A", justify="center")

def card(x, y, w, h, label, fill, stroke, op=100):
    d.shape("rectangle", label, x=x, y=y, width=w, height=h, fill=fill,
            stroke=stroke, strokeWidth=3.5, radius=6, opacity=op)
    d.path(f"M{x + 10},{y + 16} L{x + w - 10},{y + 16}",
           f"{label} title", fill=NONE, stroke="#8A94A0",
           strokeWidth=5, cap="round", opacity=70)
    d.path(f"M{x + 10},{y + 32} L{x + w - 26},{y + 32}",
           f"{label} line", fill=NONE, stroke="#9AA4AE",
           strokeWidth=4, cap="round", opacity=55)

# OPEN column — the justified grievances, still warm
card(216, 296, 90, 56, "Hot card 1", HOT_GRAD, "#A85A48")
card(224, 372, 90, 56, "Hot card 2", HOT_GRAD, "#A85A48")
d.path(rot_rect_path(288, 478, 92, 58, -7), "Hot card 3, slipped",
       fill=HOT_GRAD, stroke="#A85A48", strokeWidth=3.5)
d.path("M252,470 L320,476", "Hot 3 title", fill=NONE, stroke="#8A94A0",
       strokeWidth=5, cap="round", opacity=60)
# DOING column — captured for alignment
card(346, 306, 90, 56, "Doing card", CARD_GRAD, "#78848F")
card(352, 390, 90, 56, "Doing card 2", CARD_GRAD, "#78848F", op=75)

# the ticket being closed — tilted mid-slide into DONE, the hand on its corner
d.path(rot_rect_path(548, 452, 96, 60, -14), "The ticket",
       fill=CARD_GRAD, stroke="#6E7A86", strokeWidth=4)
d.text("FS-4221", "Ticket key", x=512, y=448, size=10,
       font="Source Sans 3", color="#5E6A76")
d.path("M516,468 L566,460", "Ticket line", fill=NONE, stroke="#9AA4AE",
       strokeWidth=4, cap="round", opacity=60)
# a check already ghosting onto it — closure arriving before the click lands
d.path("M524,478 L534,488 L552,468", "Resolving check", fill=NONE,
       stroke="#7EA87A", strokeWidth=5, cap="round", opacity=70)

# the settled DONE card behind it — greyed, calm, motionless
card(476, 522, 90, 56, "Done card", "#BCC6BA", "#8A9884", op=80)
d.path("M508,548 L518,558 L540,538", "Done check", fill=NONE,
       stroke="#7EA87A", strokeWidth=5, cap="round", opacity=85)

# --- the siphon: fury rising off the OPEN column, arriving calm -------------------
for i, (x0, y0) in enumerate([(240, 296), (270, 372), (300, 452)]):
    d.path(f"M{x0},{y0} C{x0 - 8},{y0 - 24} {x0 + 6},{y0 - 40} {x0 - 4},{y0 - 58}",
           f"Steam {i+1}", fill=NONE, stroke="#D88A6E", strokeWidth=4,
           cap="round", opacity=60 - i * 8)
# the long polite draw: heat bending right and cooling mid-flight
d.path("M262,238 C340,190 480,190 580,236 C620,254 648,284 660,318",
       "The siphon", fill=NONE, stroke="#D88A6E", strokeWidth=5,
       cap="round", opacity=50)
d.path("M580,236 C620,254 648,284 660,318", "Siphon cool half",
       fill=NONE, stroke="#AFC4C8", strokeWidth=5, cap="round", opacity=65)
# what reaches the shoulder: pale settled motes
for i, (x, y, w) in enumerate([(656,332,7),(668,354,6),(676,378,5),(664,300,5)]):
    d.shape("ellipse", f"Calm mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#C4D4D4", opacity=60, stroke=NONE)

# --- the figure: courtesy incarnate -----------------------------------------------
d.shape("ellipse", "Figure shadow", x=640, y=686, width=140, height=18,
        fill="#0C1218", opacity=45, stroke=NONE)
# torso — the sweater vest over a collar
d.path("M652,690 C644,620 646,556 668,522 L740,522 C762,556 764,620 756,690 Z",
       "Vest", fill=VEST_GRAD, stroke=INK, strokeWidth=5)
d.path("M668,524 L704,568 L740,524 L726,514 L704,544 L682,514 Z",
       "Collar V", fill="#E8E2D2", stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Vest sheen", x=664, y=540, width=26, height=90,
        fill="#FFFFFF", opacity=8, stroke=NONE)
# vest buttons
for i, by in enumerate([596, 628, 660]):
    d.shape("ellipse", f"Button {i+1}", x=700, y=by, width=8, height=8,
            fill="#26343A", stroke=NONE)
# the quiet arm, extended to the ticket's corner
d.path("M664,548 C636,528 606,492 588,472", "Arm", fill=NONE,
       stroke="#5C8A82", strokeWidth=13, cap="round")
d.shape("ellipse", "Hand", x=574, y=456, width=22, height=18,
        fill=FACE_GRAD, stroke=INK, strokeWidth=3.5)
# head — round, serene
d.shape("ellipse", "Head", x=652, y=412, width=104, height=104,
        fill=FACE_GRAD, stroke=INK, strokeWidth=5)
d.shape("ellipse", "Head light", x=668, y=424, width=50, height=34,
        fill="#FFFFFF", opacity=18, stroke=NONE)
# eyes: pleasant half-moons, nothing behind them
d.path("M676,456 C682,450 690,450 696,456", "Eye L", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.path("M714,456 C720,450 728,450 734,456", "Eye R", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
# the fixed professional smile — a hair too wide
d.path("M678,478 C692,494 716,494 730,478", "The smile", fill=NONE,
       stroke=INK, strokeWidth=4.5, cap="round")
d.path("M674,474 L670,478 M734,474 L738,478", "Smile dimples", fill=NONE,
       stroke=INK, strokeWidth=3, cap="round", opacity=70)
# small neat hair
d.path("M664,420 C676,404 730,402 744,418", "Hair", fill=NONE,
       stroke="#4A3E34", strokeWidth=7, cap="round")

# ambient motes
for i, (x, y, w) in enumerate([(330,160,4),(700,180,5),(200,470,4),(800,430,5),
                               (430,140,4),(580,130,5),(320,740,4),(700,740,5)]):
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#C4D0DC", opacity=35, stroke=NONE)

# --- captions ------------------------------------------------------------------
d.text("GENTILITY SIPHON", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#E8ECF2", justify="center")
r = d.text("CONFLICT SOFTENING ENTITY", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#AEBACC", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("282.gentility-siphon-V1R00")
