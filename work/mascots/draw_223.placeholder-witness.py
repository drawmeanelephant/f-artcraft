#!/usr/bin/env python3
"""Placeholder Witness — mascot portrait V1R00.
A featureless figure standing at its mark beside an empty podium; a brass
paperweight holds the empty chair, and a blank lanyard hangs by the door.
1000x1000. Gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Placeholder Witness — Mascot Portrait", 1000, 1000)

INK = "#3A2E28"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1C1A14"}, {"offset": 1, "color": "#0B0A07"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#8A8468"}, {"offset": 0.7, "color": "#665F48"},
    {"offset": 1, "color": "#403A2C"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4C4634"}, {"offset": 1, "color": "#2A251A"}]}}
PODIUM = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6E5E46"}, {"offset": 1, "color": "#463B2C"}]}}
FIGURE = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#D9D4C4"}, {"offset": 0.7, "color": "#B4AE9C"},
    {"offset": 1, "color": "#8C8674"}]}}
CHAIR = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5C5240"}, {"offset": 1, "color": "#3A3226"}]}}
BRASS = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E8C87A"}, {"offset": 0.6, "color": "#B8924A"},
    {"offset": 1, "color": "#7A5C28"}]}}
DOOR = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4E4434"}, {"offset": 1, "color": "#332C20"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#948C6C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8D0B4", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(190,235,8),(800,232,7),(160,524,9),(834,542,8),
                               (246,764,7),(754,748,9),(134,392,6),(862,394,7),
                               (392,112,7),(612,110,8),(334,822,6),(664,818,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#5A5340", opacity=45, stroke=NONE)

# --- floor: bottom segment closed on the disc's own arc -----------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#1E1A10",
       strokeWidth=4, opacity=70)

# --- door slab at right edge of the disc, blank lanyard on its hook ------------
d.path("M726,256 L848,256 L848,660 L726,660 Z", "Door",
       fill=DOOR, stroke=INK, strokeWidth=5, join="round")
d.path("M738,268 L738,648", "Door seam", fill=NONE, stroke="#241E14",
       strokeWidth=3, opacity=70)
d.shape("ellipse", "Door shadow", x=718, y=656, width=140, height=26,
        fill="#0C0A06", opacity=45, stroke=NONE)
# hook + blank lanyard
d.shape("ellipse", "Hook", x=788, y=312, width=14, height=14,
        fill="#8A7C5C", stroke=INK, strokeWidth=3)
d.path("M795,326 C772,352 764,396 766,440 M795,326 C818,352 826,396 824,440",
       "Lanyard strap", fill=NONE, stroke="#C7BFA8", strokeWidth=5, cap="round")
d.shape("rectangle", "Blank badge", x=760, y=438, width=62, height=44,
        fill="#E2DCC8", stroke=INK, strokeWidth=4, radius=5)
d.shape("ellipse", "Badge clip", x=784, y=430, width=14, height=10,
        fill="#8A7C5C", stroke=INK, strokeWidth=3)
# no name on the badge: one faint ruled line where a name would go
d.path("M772,462 L810,462", "Nameless line", fill=NONE, stroke="#B4AC94",
       strokeWidth=3, cap="round", opacity=60)

# --- empty podium, center-left --------------------------------------------------
d.shape("ellipse", "Podium shadow", x=430, y=640, width=230, height=38,
        fill="#0C0A06", opacity=50, stroke=NONE)
d.path("M468,420 L632,420 L616,650 L484,650 Z", "Podium body",
       fill=PODIUM, stroke=INK, strokeWidth=6, join="round")
d.path("M456,402 L644,402 L632,428 L468,428 Z", "Podium lectern",
       fill="#7C6C50", stroke=INK, strokeWidth=6, join="round")
# dusted clean top: a pale sheen across the lectern
d.path("M464,406 L636,406 L630,422 L470,422 Z", "Lectern sheen",
       fill="#C9C0A4", opacity=30, stroke=NONE)
# mic, bent over nothing
d.path("M512,402 C508,378 494,368 474,366", "Mic stem", fill=NONE,
       stroke=INK, strokeWidth=6, cap="round")
d.shape("ellipse", "Mic head", x=448, y=356, width=28, height=20,
        fill="#2E2620", stroke=INK, strokeWidth=4)
# front panel: blank agenda card pinned where a seal would be
d.shape("rectangle", "Agenda card", x=508, y=478, width=84, height=104,
        fill="#DDD6BE", stroke=INK, strokeWidth=4, radius=4)
for i, yy in enumerate((500, 520, 540, 560)):
    d.path(f"M518,{yy} L{582 - (i % 2) * 14},{yy}", f"Agenda line {i+1}",
           fill=NONE, stroke="#A89E84", strokeWidth=4, cap="round", opacity=70)

# --- chair with the brass paperweight, left -------------------------------------
d.shape("ellipse", "Chair shadow", x=228, y=646, width=180, height=30,
        fill="#0C0A06", opacity=50, stroke=NONE)
# chair back
d.path("M250,420 L250,560 M360,420 L360,560", "Chair back posts", fill=NONE,
       stroke=INK, strokeWidth=10, cap="round")
d.shape("rectangle", "Chair back top", x=244, y=414, width=122, height=22,
        fill=CHAIR, stroke=INK, strokeWidth=5, radius=8)
d.shape("rectangle", "Chair back mid", x=244, y=466, width=122, height=18,
        fill=CHAIR, stroke=INK, strokeWidth=5, radius=7)
# seat + legs
d.path("M236,558 L374,558 L364,592 L246,592 Z", "Chair seat",
       fill="#6A5E48", stroke=INK, strokeWidth=6, join="round")
d.path("M252,592 L246,652 M358,592 L364,652", "Chair legs", fill=NONE,
       stroke=INK, strokeWidth=9, cap="round")
# the brass paperweight holding the empty seat
d.shape("ellipse", "Weight glow", x=272, y=520, width=80, height=44,
        fill="#E8C87A", opacity=14, stroke=NONE)
d.shape("ellipse", "Paperweight", x=284, y=522, width=56, height=42,
        fill=BRASS, stroke=INK, strokeWidth=5)
d.path("M292,534 C298,526 312,524 320,530", "Weight highlight", fill=NONE,
       stroke="#F4E4B4", strokeWidth=4, cap="round", opacity=80)

# --- the Placeholder Witness: featureless, standing at its mark -------------------
d.shape("ellipse", "Witness shadow", x=592, y=650, width=140, height=28,
        fill="#0C0A06", opacity=55, stroke=NONE)
# the mark it stands on: a taped X
d.path("M620,646 L664,668 M664,646 L620,668", "Floor mark", fill=NONE,
       stroke="#D8D0B4", strokeWidth=6, cap="round", opacity=55)
# legs and shoes
d.path("M626,560 L622,646", "Witness leg L", fill=NONE, stroke="#8C8674",
       strokeWidth=14, cap="round")
d.path("M664,560 L668,646", "Witness leg R", fill=NONE, stroke="#7E7866",
       strokeWidth=14, cap="round")
d.shape("ellipse", "Shoe L", x=604, y=640, width=34, height=15, fill=INK, stroke=NONE)
d.shape("ellipse", "Shoe R", x=656, y=640, width=34, height=15, fill=INK, stroke=NONE)
# featureless body: a smooth capsule with no face at all
d.path("M645,318 C700,318 730,368 728,432 C726,506 700,578 645,578 "
       "C590,578 564,506 562,432 C560,368 590,318 645,318 Z",
       "Witness body", fill=FIGURE, stroke=INK, strokeWidth=6)
# where a face would be: a faint oval sheen, nothing else
d.shape("ellipse", "Face sheen", x=600, y=356, width=90, height=70,
        fill="#EFEADA", opacity=25, stroke=NONE)
# hands where a mascot's hands would be: mitten nubs at the sides
d.shape("ellipse", "Hand L", x=556, y=498, width=30, height=40,
        fill=FIGURE, stroke=INK, strokeWidth=5)
d.shape("ellipse", "Hand R", x=704, y=498, width=30, height=40,
        fill=FIGURE, stroke=INK, strokeWidth=5)
# the one dishonest act: a participant ribbon it misfiled on itself
d.shape("rectangle", "Ribbon card", x=616, y=452, width=58, height=40,
        fill="#E4DECA", stroke=INK, strokeWidth=4, radius=4)
t = d.text("TBD", "Ribbon text", x=645, y=479, size=14,
           font="Virelai Sans", color="#6E6450", justify="center")
d.shape("ellipse", "Ribbon pin", x=640, y=444, width=10, height=10,
        fill=BRASS, stroke=INK, strokeWidth=2)

# --- captions ---------------------------------------------------------------------------
d.text("PLACEHOLDER WITNESS", "Name", x=500, y=930, size=54,
       font="Virelai Sans", color="#E4DECA", justify="center")
r = d.text("PREEMPTIVE VACANCY OBSERVER", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#B4AA8C", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("223.placeholder-witness-V1R00")
