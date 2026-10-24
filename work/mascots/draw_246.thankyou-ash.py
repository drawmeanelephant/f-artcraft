#!/usr/bin/env python3
"""Thankyou Ash — mascot portrait V1R00.
A courteous little figure sweeping fine grey ash into the corner seam of a
ticket tracker. The courtesy is warm; the outcomes were cold. 1000x1000.
Gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Thankyou Ash — Mascot Portrait", 1000, 1000)

INK = "#241E18"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#161310"}, {"offset": 1, "color": "#0B0908"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#79726A"}, {"offset": 0.7, "color": "#514C45"},
    {"offset": 1, "color": "#29251F"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#453F38"}, {"offset": 1, "color": "#221E19"}]}}
BODY_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#C0AC9E"}, {"offset": 0.72, "color": "#948078"},
    {"offset": 1, "color": "#62514C"}]}}
PANEL_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#343A3E"}, {"offset": 1, "color": "#1E2226"}]}}
BRISTLE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#D4B06A"}, {"offset": 1, "color": "#9A7C48"}]}}
CARD = "#B4AA96"
CARD_DIM = "#9A9284"
ASH = "#C6BFB4"
ASH_D = "#8E877C"
EMBER = "#C07848"
KERCHIEF = "#7E8A92"

# --- backdrop + plate ----------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#94897A", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#DCD2C2", strokeWidth=3, opacity=45)
for i, (x, y, w) in enumerate([(186,236,8),(808,234,7),(150,520,9),(842,542,8),
                               (250,768,7),(750,752,9),(128,390,6),(866,394,7),
                               (388,110,7),(620,108,8),(334,824,6),(666,822,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#5E584E", opacity=45, stroke=NONE)

# --- floor: bottom segment closed on the disc's own arc ------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#14100C",
       strokeWidth=4, opacity=70)

# --- the ticket tracker: cold slate board, warm dust in its seams ----------------
d.shape("rectangle", "Tracker panel", x=250, y=190, width=470, height=430,
        fill=PANEL_GRAD, stroke=INK, strokeWidth=6, radius=14)
d.shape("rectangle", "Tracker header", x=262, y=202, width=446, height=36,
        fill="#3E4448", stroke=NONE, radius=8)
d.text("TICKET TRACKER", "Tracker title", x=278, y=226, size=15,
       font="Virelai Sans", color="#B8AE9E", justify="left")
d.shape("ellipse", "Status dot", x=682, y=212, width=14, height=14,
        fill=EMBER, stroke=INK, strokeWidth=3)
d.shape("ellipse", "Status glow", x=676, y=206, width=26, height=26,
        fill=EMBER, opacity=25, stroke=NONE)
# column heads + separators
for i, (cx, label) in enumerate([(292, "OPEN"), (434, "WAITING"),
                                 (576, "CLOSED")]):
    d.text(label, f"Col head {i+1}", x=cx, y=262, size=11,
           font="Virelai Sans", color="#8A8274", justify="left")
for i, sx in enumerate([402, 544]):
    d.path(f"M{sx},250 L{sx},600", f"Col sep {i+1}", fill=NONE,
           stroke="#44484C", strokeWidth=2, opacity=70)
# cards: the work, flattened to slips
for i, (x, y, c) in enumerate([(272,272,CARD),(272,326,CARD_DIM),
                               (414,272,CARD),(414,326,CARD_DIM),
                               (414,380,CARD_DIM),(556,326,CARD_DIM)]):
    d.shape("rectangle", f"Card {i+1}", x=x, y=y, width=110, height=42,
            fill=c, stroke=INK, strokeWidth=3, radius=4)
    d.path(f"M{x+10},{y+14} L{x+96},{y+14} M{x+10},{y+26} L{x+78},{y+26}",
           f"Card rules {i+1}", fill=NONE, stroke="#6E6454", strokeWidth=2,
           opacity=70)
# the card that over-harvests the phrase
d.shape("rectangle", "Thanks card", x=556, y=272, width=110, height=42,
        fill="#C9BCA2", stroke=INK, strokeWidth=3, radius=4)
d.text("THANKS!", "Thanks text", x=568, y=298, size=12,
       font="Virelai Sans", color="#6E4A38", justify="left")
# ash settled inside the board's bottom-right corner
d.path("M620,614 C646,592 686,588 710,600 L710,614 Z", "Corner ash",
       fill=ASH, stroke=NONE, opacity=60)
for i, (x, y, r) in enumerate([(648,600,3),(672,594,2),(694,602,3),
                               (662,608,2),(704,608,2)]):
    d.shape("ellipse", f"Board speck {i+1}", x=x, y=y, width=r*2, height=r*2,
            fill=ASH_D, opacity=70, stroke=NONE)
# a film of it settling on the lowest card
d.path("M418,412 L518,412", "Card dust line", fill=NONE, stroke=ASH,
       strokeWidth=5, cap="round", opacity=35)
for i, (x, y, r) in enumerate([(434,404,2),(468,406,3),(502,404,2)]):
    d.shape("ellipse", f"Card speck {i+1}", x=x, y=y, width=r*2,
            height=r*2, fill=ASH, opacity=50, stroke=NONE)

# --- ash film along the floor seam ------------------------------------------------
d.shape("ellipse", "Floor film", x=250, y=690, width=560, height=22,
        fill=ASH, opacity=18, stroke=NONE)

# --- the pile she has gathered, tucked into the board's foot ------------------------
d.path("M688,702 C700,684 732,676 764,678 C798,680 824,690 832,702 Z",
       "Ash pile", fill=ASH, stroke=INK, strokeWidth=4, join="round")
d.path("M700,694 C720,686 752,684 776,688", "Pile crest", fill=NONE,
       stroke="#E4DED2", strokeWidth=3, cap="round", opacity=70)
for i, (x, y, r) in enumerate([(676,696,3),(846,700,3),(700,682,2),
                               (824,684,2),(760,668,2)]):
    d.shape("ellipse", f"Loose speck {i+1}", x=x, y=y, width=r*2,
            height=r*2, fill=ASH_D, opacity=75, stroke=NONE)
# the afterglow: embers of acknowledgment where the help burned away
for i, (x, y, r) in enumerate([(736,690,4),(788,694,3),(712,698,3)]):
    d.shape("ellipse", f"Ember {i+1}", x=x, y=y, width=r*2, height=r*2,
            fill=EMBER, opacity=80, stroke=NONE)
# motes still settling — it settles rather than lands
for i, (x, y, r) in enumerate([(762,560,3),(800,600,2),(736,610,2),
                               (836,640,3),(786,648,2)]):
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=r*2, height=r*2,
            fill=ASH, opacity=40, stroke=NONE)

# --- Thankyou Ash: small, courteous, mid-sweep ------------------------------------
d.shape("ellipse", "Ash shadow", x=580, y=686, width=190, height=22,
        fill="#100C08", opacity=50, stroke=NONE)
# body: a polite pear leaning into the work
d.path("M660,478 C712,478 742,538 742,606 C742,662 708,694 660,694 "
       "C612,694 578,662 578,606 C578,538 608,478 660,478 Z",
       "Ash body", fill=BODY_GRAD, stroke=INK, strokeWidth=6)
d.shape("ellipse", "Body hi", x=596, y=522, width=90, height=44,
        fill="#FFFFFF", opacity=12, stroke=NONE)
# apron: the uniform of defensive gratitude
d.path("M614,538 C640,528 682,528 706,538 L700,658 C680,672 640,672 620,658 Z",
       "Apron", fill="#CFC6B4", stroke=INK, strokeWidth=4, join="round",
       opacity=95)
d.path("M620,576 L698,576", "Apron seam", fill=NONE, stroke="#8E8272",
       strokeWidth=2, opacity=70)

# head with kerchief knotted at the side
d.path("M660,372 C706,372 734,402 734,436 C734,468 702,488 660,488 "
       "C618,488 586,468 586,436 C586,402 614,372 660,372 Z",
       "Head", fill=BODY_GRAD, stroke=INK, strokeWidth=6)
d.path("M588,418 C588,390 618,368 660,368 C702,368 732,390 732,418 "
       "C710,400 686,392 660,392 C634,392 610,400 588,418 Z",
       "Kerchief", fill=KERCHIEF, stroke=INK, strokeWidth=4, join="round")
d.path("M726,414 L750,434 L724,442 Z", "Kerchief knot", fill=KERCHIEF,
       stroke=INK, strokeWidth=4, join="round")
# eyes: closed in a courteous arc
d.path("M618,444 C626,434 640,434 648,444", "Eye L", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
d.path("M672,444 C680,434 694,434 702,444", "Eye R", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
# the small smile that weighs more than the resolution
d.path("M646,468 C654,475 668,475 676,468", "Smile", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
# cheeks: traces of social brightness
d.shape("ellipse", "Cheek L", x=610, y=452, width=26, height=13,
        fill="#C08A6A", opacity=40, stroke=NONE)
d.shape("ellipse", "Cheek R", x=686, y=452, width=26, height=13,
        fill="#C08A6A", opacity=40, stroke=NONE)

# the broom: handle across the body, bristles at the pile
d.path("M652,548 L800,682", "Broom handle", fill=NONE, stroke="#6A5238",
       strokeWidth=9, cap="round")
# arms gripping it: one high, one low — the sweep already in motion
d.path("M620,518 C604,546 616,568 648,580", "Arm L", fill=NONE,
       stroke="#8C7468", strokeWidth=15, cap="round")
d.path("M702,528 C718,554 716,578 700,592", "Arm R", fill=NONE,
       stroke="#8C7468", strokeWidth=15, cap="round")
d.shape("ellipse", "Palm L", x=640, y=568, width=24, height=18,
        fill="#B09A8C", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Palm R", x=688, y=582, width=24, height=18,
        fill="#B09A8C", stroke=INK, strokeWidth=3)
# binding band + splayed bristles
d.path("M770,650 L792,672", "Broom band", fill=NONE, stroke="#8A6A48",
       strokeWidth=14, cap="round")
d.path("M782,664 L830,686 C838,692 836,700 826,700 L768,702 "
       "C756,698 752,690 762,682 Z",
       "Bristles", fill=BRISTLE_GRAD, stroke=INK, strokeWidth=4,
       join="round")
d.path("M788,676 L780,698 M800,680 L794,700 M812,684 L808,700",
       "Bristle tines", fill=NONE, stroke="#7E6238", strokeWidth=2,
       opacity=80)

# --- captions ---------------------------------------------------------------------
d.text("THANKYOU ASH", "Name", x=500, y=930, size=58,
       font="Virelai Sans", color="#E4DCCB", justify="center")
r = d.text("WHAT THE ENCOUNTER LEFT", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#A99E8C", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("246.thankyou-ash-V1R00")
