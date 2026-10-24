#!/usr/bin/env python3
"""Peatworthy Abstention Clerk — mascot portrait V1R00.
Clerk taking roll beside an empty folding chair in a chapter hall; the
absent linger as ghost chairs behind. He does not call the roll so much
as keep it warm. 1000x1000. Gradients + translucency, never flat."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Peatworthy Abstention Clerk — Mascot Portrait", 1000, 1000)

INK = "#2C2418"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#21241B"}, {"offset": 1, "color": "#0E110A"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#D6D7BD"}, {"offset": 0.7, "color": "#A2A486"},
    {"offset": 1, "color": "#696B51"}]}}
TWEED_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#6E4E3A"}, {"offset": 0.7, "color": "#4C3527"},
    {"offset": 1, "color": "#302117"}]}}
FACE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F1D2B2"}, {"offset": 1, "color": "#D3A780"}]}}
SHIRT_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F1E8D2"}, {"offset": 1, "color": "#D6C9A9"}]}}
PAPER_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F7F0DC"}, {"offset": 1, "color": "#DFD2B0"}]}}
STEEL_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#C2C8D0"}, {"offset": 1, "color": "#7D838E"}]}}
SEAT_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#8A6B4C"}, {"offset": 1, "color": "#5A422E"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#7C7E5C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#EEF0DA", strokeWidth=3, opacity=50)
for i, (x, y, w) in enumerate([(212,226,7),(784,218,6),(242,712,7),(748,702,7),(172,452,6),
                               (832,456,6),(352,152,6),(644,146,7),(296,794,6),(704,798,6)]):
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#6A6C50", opacity=38, stroke=NONE)

# --- ghost chairs: the absent, present in the minutes ----------------------------
def ghost_chair(x, y, s, op, label):
    """Translucent folding chair outline — members no one has asked to stand."""
    st = "#565840"
    d.path(f"M{x},{y} L{x+18*s},{y-140*s}", f"{label} back L",
           fill=NONE, stroke=st, strokeWidth=6, cap="round", opacity=op)
    d.path(f"M{x+70*s},{y} L{x+52*s},{y-140*s}", f"{label} back R",
           fill=NONE, stroke=st, strokeWidth=6, cap="round", opacity=op)
    d.shape("rectangle", f"{label} rest", x=x+10*s, y=y-140*s,
            width=50*s, height=26*s, fill=NONE, stroke=st,
            strokeWidth=5, radius=6, opacity=op)
    d.shape("rectangle", f"{label} seat", x=x-2*s, y=y-58*s,
            width=74*s, height=14*s, fill=NONE, stroke=st,
            strokeWidth=5, radius=5, opacity=op)
    d.path(f"M{x+4*s},{y-44*s} L{x+64*s},{y}", f"{label} leg X1",
           fill=NONE, stroke=st, strokeWidth=5, cap="round", opacity=op)
    d.path(f"M{x+66*s},{y-44*s} L{x+6*s},{y}", f"{label} leg X2",
           fill=NONE, stroke=st, strokeWidth=5, cap="round", opacity=op)

ghost_chair(210, 690, 1.0, 30, "Ghost L")
ghost_chair(700, 700, 0.9, 24, "Ghost R")
ghost_chair(560, 560, 0.75, 18, "Ghost far")

# --- the empty folding chair, lit and very present --------------------------------
d.shape("ellipse", "Chair glow", x=580, y=460, width=220, height=330,
        fill="#EDEFD8", opacity=22, stroke=NONE)
d.shape("ellipse", "Chair shadow", x=590, y=772, width=200, height=24,
        fill="#565840", opacity=40, stroke=NONE)
# back posts + backrest
d.path("M634,774 L644,470", "Chair post L", fill=NONE, stroke=INK,
       strokeWidth=9, cap="round")
d.path("M758,774 L748,470", "Chair post R", fill=NONE, stroke=INK,
       strokeWidth=9, cap="round")
d.shape("rectangle", "Chair rest", x=622, y=452, width=148, height=44,
        fill=SEAT_GRAD, stroke=INK, strokeWidth=6, radius=10)
d.path("M640,474 L752,474", "Rest seam", fill=NONE, stroke="#4A3423",
       strokeWidth=3, opacity=60)
# seat
d.shape("rectangle", "Chair seat", x=610, y=596, width=172, height=34,
        fill=SEAT_GRAD, stroke=INK, strokeWidth=6, radius=12)
# folding X legs
d.path("M626,632 L646,786 M766,632 L746,786", "Chair legs front",
       fill=NONE, stroke=STEEL_GRAD, strokeWidth=8, cap="round")
d.path("M628,780 L664,636 M764,780 L728,636", "Chair legs back",
       fill=NONE, stroke=STEEL_GRAD, strokeWidth=8, cap="round")
# pivot bolts where the X crosses
d.shape("ellipse", "Pivot L", x=650, y=702, width=12, height=12,
        fill="#565840", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Pivot R", x=736, y=702, width=12, height=12,
        fill="#565840", stroke=INK, strokeWidth=3)
# the courtesy card left on the seat — the abstention, placed
d.path("M660,600 L726,596 L728,616 L662,620 Z", "Seat card",
       fill=PAPER_GRAD, stroke=INK, strokeWidth=3, join="round")
d.path("M672,608 L714,606", "Seat card mark", fill=NONE, stroke="#8A7454",
       strokeWidth=3, cap="round")

# --- the clerk ---------------------------------------------------------------------
d.shape("ellipse", "Figure shadow", x=250, y=766, width=330, height=30,
        fill="#565840", opacity=40, stroke=NONE)
# cardigan body
d.path("M310,766 C306,680 314,596 338,536 C360,480 396,458 424,464 "
       "C476,474 512,542 518,616 C522,682 520,728 518,766 Z",
       "Cardigan", fill=TWEED_GRAD, stroke=INK, strokeWidth=7, join="round")
# shirt front + tie
d.path("M404,486 L448,486 L444,600 L408,600 Z", "Shirt front",
       fill=SHIRT_GRAD, stroke=INK, strokeWidth=4)
d.path("M426,494 L438,494 L434,560 L422,560 Z", "Tie",
       fill="#7A3A30", stroke=INK, strokeWidth=3.5, join="round")
d.path("M410,486 L426,502 L404,510 Z", "Collar L",
       fill=SHIRT_GRAD, stroke=INK, strokeWidth=3)
d.path("M442,486 L438,502 L458,510 Z", "Collar R",
       fill=SHIRT_GRAD, stroke=INK, strokeWidth=3)
# cardigan opening edge + buttons
d.path("M400,510 C396,580 396,680 400,760", "Cardigan edge L",
       fill=NONE, stroke=INK, strokeWidth=4, opacity=70)
d.path("M452,510 C456,580 456,680 452,760", "Cardigan edge R",
       fill=NONE, stroke=INK, strokeWidth=4, opacity=70)
for j, yy in enumerate([560, 616, 672]):
    d.shape("ellipse", f"Cardigan button {j+1}", x=390, y=yy, width=12,
            height=12, fill="#8A6B4C", stroke=INK, strokeWidth=3)
# head
d.shape("ellipse", "Head", x=348, y=320, width=150, height=146,
        fill=FACE_GRAD, stroke=INK, strokeWidth=6)
# clerk's translucent green eyeshade visor
d.path("M350,368 C360,334 400,318 438,320 C476,322 500,340 504,368 "
       "C470,352 386,350 350,368 Z",
       "Visor band", fill=TWEED_GRAD, stroke=INK, strokeWidth=4, join="round")
d.path("M344,368 C384,348 472,350 512,370 L506,392 C468,374 388,372 350,390 Z",
       "Eyeshade", fill="#5A7A50", opacity=55, stroke=INK, strokeWidth=4)
# face: courteous regard toward the empty chair — eyes cast right
d.shape("ellipse", "Eye L", x=392, y=402, width=15, height=18, fill="#241C12", stroke=NONE)
d.shape("ellipse", "Eye R", x=452, y=402, width=15, height=18, fill="#241C12", stroke=NONE)
d.shape("ellipse", "Glint L", x=398, y=406, width=5, height=5, fill="#FFFFFF", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=458, y=406, width=5, height=5, fill="#FFFFFF", opacity=90, stroke=NONE)
d.path("M386,384 C396,380 408,380 416,384", "Brow L",
       fill=NONE, stroke=INK, strokeWidth=3.5, cap="round", opacity=70)
d.path("M446,384 C456,380 468,380 476,384", "Brow R",
       fill=NONE, stroke=INK, strokeWidth=3.5, cap="round", opacity=70)
d.path("M404,440 C414,447 434,447 444,440", "Courteous smile",
       fill=NONE, stroke=INK, strokeWidth=4.5, cap="round")
d.shape("ellipse", "Cheek L", x=374, y=424, width=22, height=10, fill="#C98E72", opacity=35, stroke=NONE)
d.shape("ellipse", "Cheek R", x=456, y=424, width=22, height=10, fill="#C98E72", opacity=35, stroke=NONE)

# --- the roll: clipboard in his left arm --------------------------------------------
d.path("M316,560 L446,548 L458,690 L328,702 Z", "Clipboard",
       fill="#7A5638", stroke=INK, strokeWidth=5, join="round")
d.path("M330,570 L434,560 L444,676 L340,686 Z", "Roll sheet",
       fill=PAPER_GRAD, stroke=INK, strokeWidth=3)
d.path("M366,554 L402,551 L404,566 L368,569 Z", "Clip",
       fill="#C9C2A8", stroke=INK, strokeWidth=3, join="round")
# the roll itself: name scribbles, each answered with the same courteous dash
for j, yy in enumerate([588, 612, 636, 660]):
    d.path(f"M344,{yy} L392,{yy-4}", f"Roll name {j+1}", fill=NONE,
           stroke="#8A7454", strokeWidth=3, cap="round", opacity=85)
    d.path(f"M406,{yy-4} L424,{yy-5}", f"Abstention {j+1}", fill=NONE,
           stroke="#5A4A34", strokeWidth=4, cap="round")
# his left hand at the board's lower edge
d.shape("ellipse", "Hand L", x=322, y=660, width=32, height=38,
        fill=FACE_GRAD, stroke=INK, strokeWidth=4)
d.path("M310,640 C318,626 332,622 344,630 L336,660 C326,654 316,648 310,640 Z",
       "Sleeve L", fill=TWEED_GRAD, stroke=INK, strokeWidth=4)

# --- right arm raised toward the chair, pencil poised --------------------------------
d.path("M512,560 C540,548 566,540 590,532 L598,556 C574,564 550,574 528,584 Z",
       "Sleeve R", fill=TWEED_GRAD, stroke=INK, strokeWidth=4, join="round")
d.shape("ellipse", "Hand R", x=584, y=520, width=30, height=34,
        fill=FACE_GRAD, stroke=INK, strokeWidth=4)
# the pencil, mid-entry
d.path("M596,514 L636,498 L640,506 L600,522 Z", "Pencil",
       fill="#D9A03C", stroke=INK, strokeWidth=2.5, join="round")
d.path("M636,498 L646,498 L640,506 Z", "Pencil tip", fill="#2C2418", stroke=NONE)
d.shape("ellipse", "Pencil end", x=592, y=514, width=10, height=10,
        fill="#B43A28", stroke=INK, strokeWidth=2)

# --- name + role -------------------------------------------------------------------
d.text("PEATWORTHY ABSTENTION CLERK", "Name", x=500, y=930, size=46,
       font="Virelai Sans", color="#EEF0DA", justify="center")
r = d.text("MEMORIAL QUORUM STEWARD", "Role", x=500, y=968,
           size=23, font="Virelai Sans", color="#B8BA98", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("305.peatworthy-abstention-clerk-V1R00")
