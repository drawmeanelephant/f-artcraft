#!/usr/bin/env python3
"""Brother Optout Pending — mascot portrait V1R00.
A cowled clerk receives an opt-out filing across the counter; the requester
is still seated, the drawer is open, the exit sign stays politely lit.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Brother Optout Pending — Mascot Portrait", 1000, 1000)

INK = "#2C2218"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#15110C"}, {"offset": 1, "color": "#080604"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#423828"}, {"offset": 0.7, "color": "#261E14"},
    {"offset": 1, "color": "#120D08"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2A2318"}, {"offset": 1, "color": "#100C08"}]}}
ROBE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#74604A"}, {"offset": 1, "color": "#463828"}]}}
HOOD_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#82704F"}, {"offset": 0.75, "color": "#5C4C36"},
    {"offset": 1, "color": "#3E3020"}]}}
FACE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E0CDA8"}, {"offset": 0.8, "color": "#B89B72"},
    {"offset": 1, "color": "#8A704E"}]}}
DESK_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5A4630"}, {"offset": 1, "color": "#33261A"}]}}
PAPER = "#E8DCC0"
REQ_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#C8A9A2"}, {"offset": 0.75, "color": "#9E8078"},
    {"offset": 1, "color": "#6E5850"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#8A7A58", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8CCA8", strokeWidth=3, opacity=50)
for i, (x, y, w) in enumerate([(193,233,8),(801,230,7),(157,524,9),(837,544,8),
                               (247,766,7),(753,749,9),(133,393,6),(864,391,7),
                               (391,113,7),(613,110,8),(333,823,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#4A3E2C", opacity=45, stroke=NONE)

# --- floor ----------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0C0806",
       strokeWidth=4, opacity=70)

# --- the exit sign: fully visible, gently lit -------------------------------------
d.shape("ellipse", "Exit glow", x=172, y=196, width=120, height=66,
        fill="#9FD8B0", opacity=10, stroke=NONE)
d.shape("rectangle", "Exit sign", x=196, y=206, width=72, height=34,
        fill="#18241C", stroke="#5A7A62", strokeWidth=3, radius=5)
d.text("EXIT", "Exit text", x=232, y=229, size=15, font="Source Sans 3",
       color="#9FD8B0", justify="center")

# --- the clerk: cowled, courteous, load-bearing -------------------------------------
# robe: a wide habit pooling behind the counter
d.path("M560,700 C552,560 556,452 590,398 C606,372 640,360 668,360 "
       "C696,360 730,372 746,398 C780,452 784,560 776,700 Z",
       "Robe", fill=ROBE_GRAD, stroke=INK, strokeWidth=7)
# habit folds
for lbl, dd in [("Fold L", "M596,470 C586,540 584,610 590,668"),
                ("Fold R", "M742,470 C752,540 754,610 748,668")]:
    d.path(dd, lbl, fill=NONE, stroke="#3E3020", strokeWidth=5,
           opacity=45, cap="round")
# rope belt with three knots of procedure
d.path("M584,592 L754,592", "Rope belt", fill=NONE, stroke="#C9B892",
       strokeWidth=7, cap="round")
for i, x in enumerate([624, 668, 712]):
    d.shape("ellipse", f"Knot {i+1}", x=x - 6, y=586, width=12, height=12,
            fill="#C9B892", stroke=INK, strokeWidth=2.5)

# the hood: a soft peak over a shadowed opening
d.path("M668,262 C722,262 762,304 764,360 C765,402 748,434 722,452 "
       "L614,452 C588,434 571,402 572,360 C574,304 614,262 668,262 Z",
       "Hood", fill=HOOD_GRAD, stroke=INK, strokeWidth=6)
# hood opening: the warm face inside the cowl's shadow
d.shape("ellipse", "Cowl shadow", x=616, y=330, width=104, height=110,
        fill="#241A10", stroke=NONE, opacity=85)
d.shape("ellipse", "Face", x=626, y=340, width=84, height=92,
        fill=FACE_GRAD, stroke=NONE)
# face shading under the hood's brow
d.shape("ellipse", "Brow shade", x=628, y=340, width=80, height=30,
        fill="#3A2C1C", opacity=30, stroke=NONE)
# eyes half-lowered in procedural kindness
for i, cx2 in enumerate([652, 692]):
    d.shape("ellipse", f"Eye {i+1}", x=cx2 - 8, y=382, width=16, height=14,
            fill="#241A18", stroke=NONE)
    d.path(f"M{cx2-12},380 L{cx2+12},380", f"Lid {i+1}", fill=NONE,
           stroke=INK, strokeWidth=3, cap="round", opacity=60)
# the gentle smile that is, on second reading, the discouraging part
d.path("M656,414 C666,422 678,422 688,414", "Smile", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
# hood highlight along the peak
d.path("M600,330 C614,292 642,272 676,270", "Hood sheen", fill=NONE,
       stroke="#C9B892", strokeWidth=5, opacity=35, cap="round")

# --- the counter -----------------------------------------------------------------------
d.shape("ellipse", "Counter shadow", x=180, y=686, width=660, height=26,
        fill="#080604", opacity=55, stroke=NONE)
d.shape("rectangle", "Counter top", x=186, y=560, width=640, height=28,
        fill=DESK_GRAD, stroke=INK, strokeWidth=5, radius=8)
d.shape("rectangle", "Counter front", x=202, y=588, width=608, height=112,
        fill={"gradient": {"kind": "linear", "stops": [
            {"offset": 0, "color": "#4A3A26"}, {"offset": 1, "color": "#241A10"}]}},
        stroke=INK, strokeWidth=5, radius=6)
# panel seams on the counter face
for i, x in enumerate([300, 420, 540, 660]):
    d.path(f"M{x},598 L{x},692", f"Panel seam {i+1}", fill=NONE,
           stroke="#241A10", strokeWidth=3, opacity=70)

# BIN 8C — the drawer receives everything and rules on nothing
d.shape("rectangle", "Bin 8C", x=560, y=612, width=120, height=54,
        fill="#33261A", stroke=INK, strokeWidth=4, radius=6)
d.shape("rectangle", "Bin slot", x=576, y=620, width=88, height=14,
        fill="#1A120C", stroke=NONE, radius=6)
# filings in the slot, descending in order of arrival
for i, yy in enumerate([618, 624, 630]):
    d.path(rot_rect_path(620, yy + 2, 74, 8, -3 + i * 2), f"Filed {i+1}",
           fill=PAPER, stroke=INK, strokeWidth=1.5, join="round",
           opacity=90 - i * 15)
t = d.text("8C", "Bin label", x=620, y=658, size=14, font="Source Sans 3",
           color="#C9B892", justify="center")

# --- the handoff: the opt-out filing mid-transfer ---------------------------------------
# clerk's sleeve extends left, receiving the sheet from below
d.path("M600,520 C552,530 512,542 482,556", "Sleeve L", fill=NONE,
       stroke="#74604A", strokeWidth=30, cap="round")
d.shape("ellipse", "Clerk hand L", x=458, y=540, width=44, height=30,
        fill="#C9B28E", stroke=INK, strokeWidth=4)
# the filing, tilted between two hands
d.path(rot_rect_path(436, 530, 92, 64, -18), "Filing shadow",
       fill="#080604", opacity=35, stroke=NONE)
d.path(rot_rect_path(430, 524, 92, 64, -18), "Opt-out filing",
       fill=PAPER, stroke=INK, strokeWidth=3.5, join="round")
d.text("OPT OUT", "Filing label", x=412, y=519, size=12,
       font="Virelai Sans", color="#4A3626", justify="left")
d.path("M398,532 L452,519", "Filing line 1", fill=NONE, stroke="#A89878",
       strokeWidth=2, opacity=80)
d.path("M402,542 L452,530", "Filing line 2", fill=NONE, stroke="#A89878",
       strokeWidth=2, opacity=80)
# clerk's second hand cups beneath the page's corner
d.path("M560,560 C534,566 516,572 506,580", "Sleeve R", fill=NONE,
       stroke="#74604A", strokeWidth=24, cap="round")
d.shape("ellipse", "Clerk hand R", x=488, y=566, width=38, height=26,
        fill="#C9B28E", stroke=INK, strokeWidth=4)

# --- the requester: still seated ------------------------------------------------------------
# stool
d.shape("ellipse", "Stool shadow", x=252, y=684, width=110, height=16,
        fill="#080604", opacity=50, stroke=NONE)
d.shape("ellipse", "Stool seat", x=264, y=556, width=92, height=22,
        fill="#4A3A26", stroke=INK, strokeWidth=4)
for lbl, dd in [("Leg L", "M282,574 L276,686"), ("Leg R", "M338,574 L344,686"),
                ("Leg bar", "M280,640 L342,640")]:
    d.path(dd, lbl, fill=NONE, stroke=INK, strokeWidth=5, cap="round")
# the small figure, seen from behind, holding nothing anymore
d.path("M310,392 C354,392 382,432 380,486 C378,534 352,566 310,566 "
       "C268,566 242,534 240,486 C238,432 266,392 310,392 Z",
       "Requester", fill=REQ_GRAD, stroke=INK, strokeWidth=6)
d.shape("ellipse", "Req sheen", x=262, y=410, width=80, height=40,
        fill="#FFFFFF", opacity=12, stroke=NONE)
# a queued ticket stub still in its fist
d.shape("rectangle", "Ticket", x=350, y=508, width=22, height=14,
        fill=PAPER, stroke=INK, strokeWidth=2.5, radius=3)
# the offering arm, raised to the counter, gripping the sheet's left edge
d.path("M356,505 C382,512 392,524 398,536", "Req arm", fill=NONE,
       stroke="#9E8078", strokeWidth=20, cap="round")
d.shape("ellipse", "Req hand", x=384, y=538, width=36, height=22,
        fill="#B89B8E", stroke=INK, strokeWidth=4)

# --- captions -------------------------------------------------------------------------
d.text("BROTHER OPTOUT PENDING", "Name", x=500, y=930, size=50,
       font="Virelai Sans", color="#EFE4C8", justify="center")
r = d.text("WITHDRAWAL PERSISTENCE CLERK", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#C4AE84", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("304.brother-optout-pending-V1R00")
