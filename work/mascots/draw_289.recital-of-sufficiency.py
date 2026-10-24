#!/usr/bin/env python3
"""Recital of Sufficiency — mascot portrait V1R00.
The last five minutes of the meeting: the mascot at the lectern, card in
paw, pronouncing the closing words into the board microphone while the
review panel sits in shadow behind their little green lamps. It does not
conclude the argument; it stops it — the room has run out of ways to ask.
1000x1000. Gradients + translucent shading, no flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Recital of Sufficiency — Mascot Portrait", 1000, 1000)

INK = "#2C1F14"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#0F1512"}, {"offset": 1, "color": "#060A08"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#3E4C40"}, {"offset": 0.7, "color": "#26332B"},
    {"offset": 1, "color": "#131B16"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#332C22"}, {"offset": 1, "color": "#1C1712"}]}}
TABLE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4E3A26"}, {"offset": 1, "color": "#2E2216"}]}}
LECTERN_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5E472E"}, {"offset": 1, "color": "#3A2C1C"}]}}
FUR_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#D2AE84"}, {"offset": 0.7, "color": "#A87F58"},
    {"offset": 1, "color": "#7A5A3E"}]}}
SHADE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5E9A72"}, {"offset": 1, "color": "#2E4A3A"}]}}
RAY_GRAD = {"gradient": {"kind": "linear", "start": [0, 60], "end": [0, 740], "stops": [
    {"offset": 0, "color": "#F4E8C8", "opacity": 0.11},
    {"offset": 0.55, "color": "#F4E8C8", "opacity": 0.04},
    {"offset": 1, "color": "#F4E8C8", "opacity": 0}]}}
MIC_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#8A8E9C"}, {"offset": 1, "color": "#4A4E60"}]}}

PCX, PCY, PR = 500, 460, 420
def on_disc(x, y, pad):
    assert math.hypot(x - PCX, y - PCY) <= PR - pad, (x, y)

def rrect(x, y, w, h, r):
    return (f"M{x+r},{y} L{x+w-r},{y} Q{x+w},{y} {x+w},{y+r} "
            f"L{x+w},{y+h-r} Q{x+w},{y+h} {x+w-r},{y+h} "
            f"L{x+r},{y+h} Q{x},{y+h} {x},{y+h-r} "
            f"L{x},{y+r} Q{x},{y} {x+r},{y} Z")

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#3E4C40", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#5E7060", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C4D4BC", strokeWidth=3, opacity=40)
for i, (x, y, w) in enumerate([(205,250,7),(800,242,8),(162,470,8),(840,482,7),
                               (268,766,6),(732,770,7),(138,362,6),(864,352,6),
                               (400,106,7),(606,102,8),(324,150,5),(690,146,6)]):
    on_disc(x + w / 2, y + w / 2, 8)
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#4E6052", opacity=45, stroke=NONE)

# --- the agenda clock: four fifty-five -------------------------------------------
CX, CY, CR = 232, 262, 42
d.shape("ellipse", "Clock", x=CX - CR, y=CY - CR, width=CR * 2, height=CR * 2,
        fill="#E8E0CC", stroke="#6A6458", strokeWidth=5)
for i in range(12):
    a = math.radians(i * 30)
    tx = CX + (CR - 9) * math.sin(a); ty = CY - (CR - 9) * math.cos(a)
    d.shape("ellipse", f"Clock tick {i+1}", x=round(tx - 2), y=round(ty - 2),
            width=4, height=4, fill="#6A6458", stroke=NONE)
# hour hand near five, minute at eleven — the recital's hour
for ang, ln, wdt in [(155, 20, 5), (330, 30, 4)]:
    a = math.radians(ang)
    d.path(f"M{CX},{CY} L{CX + ln * math.sin(a):.1f},{CY - ln * math.cos(a):.1f}",
           f"Clock hand {ang}", fill=NONE, stroke=INK, strokeWidth=wdt,
           cap="round")
d.shape("ellipse", "Clock pin", x=CX - 3, y=CY - 3, width=7, height=7,
        fill=INK, stroke=NONE)

# --- the review board, seated in shadow --------------------------------------------
def member(cx, cy, s, tag):
    """Seated silhouette: head + shoulders, nothing on the record."""
    d.path(f"M{cx - 52*s},{cy + 66*s} C{cx - 50*s},{cy + 30*s} {cx - 34*s},{cy + 18*s} "
           f"{cx - 30*s},{cy + 8*s} C{cx - 34*s},{cy - 18*s} {cx - 22*s},{cy - 38*s} "
           f"{cx},{cy - 38*s} C{cx + 22*s},{cy - 38*s} {cx + 34*s},{cy - 18*s} "
           f"{cx + 30*s},{cy + 8*s} C{cx + 34*s},{cy + 18*s} {cx + 50*s},{cy + 30*s} "
           f"{cx + 52*s},{cy + 66*s} Z", f"Board member {tag}",
           fill="#181F1A", stroke="#0C110D", strokeWidth=3)
    # faint top light on the head — the lamps reach them, barely
    d.path(f"M{cx - 20*s},{cy - 26*s} C{cx - 8*s},{cy - 36*s} {cx + 8*s},{cy - 36*s} "
           f"{cx + 20*s},{cy - 26*s}", f"Rim {tag}", fill=NONE,
           stroke="#6A7A6E", strokeWidth=3, opacity=50, cap="round")

member(238, 452, 0.92, "1")
member(376, 442, 1.0, "2")
member(624, 442, 1.0, "3")
member(762, 452, 0.92, "4")

# --- the board table ------------------------------------------------------------------
d.path("M170,505 L830,505 L842,560 L158,560 Z", "Table top",
       fill=TABLE_GRAD, stroke=INK, strokeWidth=4, join="round")
d.path("M158,560 L842,560 L834,584 L166,584 Z", "Table face",
       fill="#241A10", stroke=INK, strokeWidth=3, join="round")
# name cards — each member equally illegible
for i, cx in enumerate([238, 376, 624, 762]):
    d.path(rot_rect_path(cx, 524, 56, 20, 0), f"Name card {i+1}",
           fill="#D8D2C0", stroke="#8A8474", strokeWidth=2, opacity=85)
    d.path(f"M{cx - 18},522 L{cx + 16},522", f"Card line {i+1}a", fill=NONE,
           stroke="#8A8474", strokeWidth=2.5, cap="round", opacity=60)
    d.path(f"M{cx - 18},529 L{cx + 8},529", f"Card line {i+1}b", fill=NONE,
           stroke="#8A8474", strokeWidth=2.5, cap="round", opacity=45)
# papers awaiting the verdict
for i, (x, y, a) in enumerate([(300, 545, -8), (548, 548, 5), (700, 542, -4)]):
    d.path(rot_rect_path(x, y, 40, 26, a), f"Papers {i+1}",
           fill="#D8D2C0", opacity=70, stroke=NONE)

# --- banker's lamps, the only light the board permits ----------------------------------
def lamp(x, tag):
    d.shape("ellipse", f"Lamp {tag} pool", x=x - 34, y=488, width=68, height=16,
            fill="#E8C060", opacity=12, stroke=NONE)
    d.path(f"M{x},486 L{x},470", f"Lamp {tag} stem", fill=NONE,
           stroke="#3A3E34", strokeWidth=4, cap="round")
    d.shape("ellipse", f"Lamp {tag} foot", x=x - 12, y=482, width=24,
            height=8, fill="#3A3E34", stroke=NONE)
    d.path(f"M{x - 24},470 C{x - 24},456 {x - 14},450 {x},450 "
           f"C{x + 14},450 {x + 24},456 {x + 24},470 Z",
           f"Lamp {tag} shade", fill=SHADE_GRAD, stroke=INK, strokeWidth=3)
    d.shape("ellipse", f"Lamp {tag} underlight", x=x - 20, y=462, width=40,
            height=10, fill="#E8C060", opacity=30, stroke=NONE)

lamp(305, "L")
lamp(695, "R")

# --- floor -----------------------------------------------------------------------------
d.path("M131,660 L869,660 A420,420 0 0 1 131,660 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M131,660 L869,660", "Floor line", fill=NONE, stroke="#12100A",
       strokeWidth=4, opacity=70)

# --- the speaker's spot, a light cone earned by cadence ----------------------------------
d.path("M430,60 L570,60 L660,740 L340,740 Z", "Spotlight",
       fill=RAY_GRAD, stroke=NONE)

# --- the mascot at the lectern -------------------------------------------------------------
d.shape("ellipse", "Mascot shadow", x=380, y=720, width=260, height=20,
        fill="#0E0B08", opacity=50, stroke=NONE)
# body, from the chest up over the lectern
d.shape("ellipse", "Ear L", x=430, y=452, width=28, height=26,
        fill="#A87F58", stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Ear R", x=548, y=452, width=28, height=26,
        fill="#A87F58", stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Body", x=402, y=468, width=196, height=200,
        fill=FUR_GRAD, stroke=INK, strokeWidth=5)
# half-lidded eyes — fatigue is unanimous, the voice is not
for i, ex in enumerate([462, 538]):
    d.shape("ellipse", f"Eye {i+1}", x=ex - 11, y=530, width=22, height=18,
            fill="#2C1F14", stroke=NONE)
    d.path(f"M{ex - 14},536 C{ex - 6},528 {ex + 6},528 {ex + 14},536",
           f"Lid {i+1}", fill=NONE, stroke="#7A5A3E", strokeWidth=6,
           cap="round")
d.shape("ellipse", "Glint L", x=457, y=536, width=5, height=5,
        fill="#FFF8E8", opacity=70, stroke=NONE)
d.shape("ellipse", "Glint R", x=533, y=536, width=5, height=5,
        fill="#FFF8E8", opacity=70, stroke=NONE)
# the reciting mouth, open on the third identical sentence
d.shape("ellipse", "Mouth", x=490, y=572, width=34, height=24,
        fill="#3A2418", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Mouth inner", x=498, y=580, width=18, height=10,
        fill="#8A5040", stroke=NONE)

# --- the lectern ------------------------------------------------------------------------------
d.path("M398,596 L602,596 L614,616 L386,616 Z", "Lectern top",
       fill=LECTERN_GRAD, stroke=INK, strokeWidth=4, join="round")
d.path("M414,616 L586,616 L574,732 L426,732 Z", "Lectern column",
       fill=LECTERN_GRAD, stroke=INK, strokeWidth=4, join="round")
d.path("M400,732 L600,732 L608,748 L392,748 Z", "Lectern base",
       fill="#2E2214", stroke=INK, strokeWidth=4, join="round")
d.shape("ellipse", "Lectern sheen", x=430, y=600, width=90, height=10,
        fill="#8A6A44", opacity=40, stroke=NONE)
# the seal of the office: a small octagonal crest on the column
d.path(rot_rect_path(500, 668, 42, 42, 22.5), "Lectern crest",
       fill="#6A5236", stroke=INK, strokeWidth=3)
d.path(rot_rect_path(500, 668, 26, 26, 22.5), "Crest inner",
       fill="#8A6A44", opacity=80, stroke=NONE)

# --- the arm raised with the closing words, the card held high ---------------------------------
d.path("M584,556 C608,550 624,534 634,510", "Raised arm", fill=NONE,
       stroke="#A87F58", strokeWidth=20, cap="round")
d.shape("ellipse", "Card paw", x=618, y=494, width=30, height=26,
        fill="#D2AE84", stroke=INK, strokeWidth=3.5)
d.path(rot_rect_path(652, 486, 62, 40, -14), "Closing words",
       fill="#EDE6D2", stroke="#8A8474", strokeWidth=2.5)
for i, dy in enumerate([-8, 0, 8]):
    d.path(rot_rect_path(652, 486 + dy, 44, 4, -14), f"Words line {i+1}",
           fill="#8A8474", opacity=65, stroke=NONE)
# the left paw rests on the lectern, patient
d.shape("ellipse", "Rest paw", x=424, y=586, width=34, height=22,
        fill="#D2AE84", stroke=INK, strokeWidth=3.5)

# --- the board microphone ------------------------------------------------------------------------
d.shape("ellipse", "Mic base shadow", x=540, y=598, width=64, height=10,
        fill="#0E0B08", opacity=50, stroke=NONE)
d.shape("ellipse", "Mic base", x=546, y=584, width=56, height=18,
        fill=MIC_GRAD, stroke=INK, strokeWidth=3.5)
d.path("M574,584 C572,574 568,568 560,566", "Gooseneck", fill=NONE,
       stroke="#3A3E50", strokeWidth=6, cap="round")
d.path(rot_rect_path(552, 564, 40, 26, -18), "Mic head",
       fill=MIC_GRAD, stroke=INK, strokeWidth=3.5)
for i in range(3):
    d.path(rot_rect_path(546 + i * 8, 568 - i * 3, 24, 3, -18),
           f"Grille {i+1}", fill="#2C2E40", opacity=85, stroke=NONE)

# --- the recital made visible: the closing words rising off the capsule ---------------
for i, (x, y, s, op) in enumerate([(586, 540, 7, 60), (600, 522, 6, 48),
                                   (614, 504, 5, 36)]):
    d.path(f"M{x},{y - s} L{x + s * .6},{y} L{x},{y + s} L{x - s * .6},{y} Z",
           f"Word {i+1}", fill="#D8C89A", opacity=op, stroke=NONE)

# --- motes, settling as the room stops asking -------------------------------------------------------
for i, (x, y, w) in enumerate([(300,380,5),(700,360,5),(240,540,4),(780,540,4),
                               (420,220,4),(580,210,5),(350,640,4)]):
    on_disc(x + w / 2, y + w / 2, 8)
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#C4D4BC", opacity=35, stroke=NONE)

# --- captions --------------------------------------------------------------------------------------
d.text("RECITAL OF SUFFICIENCY", "Name", x=500, y=930, size=48,
       font="Virelai Sans", color="#E8ECD8", justify="center")
r = d.text("IT STOPS THE ARGUMENT", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#A8BC9E", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("289.recital-of-sufficiency-V1R00")
