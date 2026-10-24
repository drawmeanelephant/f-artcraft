#!/usr/bin/env python3
"""Witness Felt — mascot portrait V1R00.
The clerk lines the evidence tray with grey felt before the testimony
arrives; the microphone is wrapped in velvet so the facts keep their
shape but lose their frequency. Nothing essential was removed.
1000x1000. Gradients + translucent shading, no flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Witness Felt — Mascot Portrait", 1000, 1000)

INK = "#26202A"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#181624"}, {"offset": 1, "color": "#0A0912"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4E4F62"}, {"offset": 0.7, "color": "#35364A"},
    {"offset": 1, "color": "#1D1E2E"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3A3C50"}, {"offset": 1, "color": "#181A2C"}]}}
FUR_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#CBB096"}, {"offset": 0.7, "color": "#A1815F"},
    {"offset": 1, "color": "#75593F"}]}}
FELT_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#ABAEBC"}, {"offset": 0.6, "color": "#838696"},
    {"offset": 1, "color": "#5B5E6E"}]}}
VELVET_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#8A3A52"}, {"offset": 0.65, "color": "#62243A"},
    {"offset": 1, "color": "#3E1524"}]}}
BRASS_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#D4AE62"}, {"offset": 0.6, "color": "#A37C3A"},
    {"offset": 1, "color": "#6E5226"}]}}
TRAY_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#46445A"}, {"offset": 1, "color": "#262434"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#6E6A80", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C9C4D8", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(196,236,8),(798,232,7),(160,528,9),(834,548,8),
                               (250,764,7),(748,750,9),(138,396,6),(860,392,7),
                               (394,114,7),(610,110,8),(336,822,6),(662,820,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#3E4056", opacity=45, stroke=NONE)

# --- floor ----------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#121020",
       strokeWidth=4, opacity=70)

# --- hush arcs: the room upholstered in advance -----------------------------------
for i, (x, y, r) in enumerate([(318,258,58),(706,300,44),(500,214,36)]):
    d.path(f"M{x-r},{y+r//3} A{r},{r} 0 0 1 {x+r},{y+r//3}",
           f"Hush arc {i+1}", fill=NONE, stroke="#9A94B8", strokeWidth=3,
           cap="round", opacity=22 - i * 4)

# --- the microphone, wrapped in velvet ------------------------------------------
d.shape("ellipse", "Mic shadow", x=196, y=686, width=110, height=18,
        fill="#0C0A16", opacity=50, stroke=NONE)
d.shape("ellipse", "Mic base", x=210, y=664, width=82, height=24,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#5A5468"}, {"offset": 1, "color": "#322E44"}]}},
        stroke=INK, strokeWidth=4)
d.path("M251,668 L251,576", "Mic stem", fill=NONE, stroke="#3C3852",
       strokeWidth=8, cap="round")
# damped arcs that never leave the velvet: sound, handled
for i, x in enumerate([292, 312, 330]):
    d.path(f"M{x},{524 - i*8} C{x+8},{534 - i*6} {x+8},{548 - i*4} "
           f"{x},{558 - i*2}", f"Damped arc {i+1}", fill=NONE,
           stroke="#B6AECB", strokeWidth=3, cap="round",
           opacity=45 - i * 13)
# the velvet bundle over the capsule, gathered and tied
d.path("M222,556 C216,522 224,492 240,478 C246,472 256,472 262,478 "
       "C278,492 286,522 280,556 C268,566 234,566 222,556 Z",
       "Velvet wrap", fill=VELVET_GRAD, stroke=INK, strokeWidth=4,
       join="round")
# gathered knot at the crown
d.shape("ellipse", "Gather knot", x=240, y=462, width=22, height=16,
        fill="#4E1E30", stroke=INK, strokeWidth=3.5)
# fold lines down the nap
d.path("M238,486 C232,506 230,528 234,550", "Fold 1", fill=NONE,
       stroke="#3A1422", strokeWidth=3, opacity=65, cap="round")
d.path("M262,486 C268,508 270,530 266,552", "Fold 2", fill=NONE,
       stroke="#3A1422", strokeWidth=3, opacity=65, cap="round")
d.path("M250,492 L250,552", "Fold 3", fill=NONE, stroke="#3A1422",
       strokeWidth=2.5, opacity=45, cap="round")
# the tie cord where the velvet is cinched
d.path("M224,540 C240,548 262,548 278,540", "Tie cord", fill=NONE,
       stroke="#2E2233", strokeWidth=5, cap="round")
d.path("M268,544 L286,556 M268,544 L284,534", "Cord ends", fill=NONE,
       stroke="#2E2233", strokeWidth=3.5, cap="round")
# sheen on the nap — velvet catches one light and keeps it
d.shape("ellipse", "Velvet sheen", x=232, y=498, width=16, height=30,
        fill="#C97E96", opacity=30, stroke=NONE)

# --- the clerk, smoothing the lining before the witness arrives -------------------
# body behind the tray
d.shape("ellipse", "Body", x=470, y=496, width=200, height=164,
        fill=FUR_GRAD, stroke=INK, strokeWidth=5)
# ears
for ex in (514, 648):
    d.shape("ellipse", f"Ear {ex}", x=ex - 11, y=336, width=26, height=24,
            fill="#A1815F", stroke=INK, strokeWidth=3.5)
# head, bent low over the work
d.shape("ellipse", "Head", x=500, y=340, width=162, height=146,
        fill=FUR_GRAD, stroke=INK, strokeWidth=5)
# calm half-lidded eyes — the gentlest face in the archive
d.shape("ellipse", "Eye L", x=536, y=400, width=16, height=12,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Eye R", x=606, y=400, width=16, height=12,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Glint L", x=539, y=402, width=4, height=4,
        fill="#FFF6E4", opacity=80, stroke=NONE)
d.shape("ellipse", "Glint R", x=609, y=402, width=4, height=4,
        fill="#FFF6E4", opacity=80, stroke=NONE)
# the smallest mouth, closed, having said its five sentences
d.path("M570,444 C575,447 584,447 589,444", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=3.5, cap="round")

# --- the evidence tray, brass-rimmed, felt-lined -----------------------------------
d.shape("ellipse", "Tray shadow", x=350, y=686, width=470, height=26,
        fill="#0C0A16", opacity=50, stroke=NONE)
# brass outer rim
d.path("M390,566 L788,566 L808,642 L370,642 Z", "Tray rim",
       fill=BRASS_GRAD, stroke=INK, strokeWidth=5, join="round")
# the felt lining inside, fitted to the furniture in advance
d.path("M406,580 L768,580 L782,630 L392,630 Z", "Felt lining",
       fill=FELT_GRAD, stroke=INK, strokeWidth=3.5, join="round")
# padding seams pressed into the nap
d.path("M446,584 L458,628 M566,582 L572,630 M680,582 L684,628",
       "Felt seams", fill=NONE, stroke="#55586A", strokeWidth=3,
       opacity=60, cap="round")
# two soft dimples where earlier testimony was set down
d.shape("ellipse", "Dimple 1", x=476, y=600, width=54, height=13,
        fill="#4A4D5E", opacity=35, stroke=NONE)
d.shape("ellipse", "Dimple 2", x=606, y=608, width=60, height=15,
        fill="#4A4D5E", opacity=30, stroke=NONE)
# front wall of the tray
d.path("M370,642 L808,642 L796,698 L382,698 Z", "Tray front",
       fill=TRAY_GRAD, stroke=INK, strokeWidth=5, join="round")
# brass corner studs on the front wall
for sx in (412, 584, 758):
    d.shape("ellipse", f"Stud {sx}", x=sx, y=662, width=11, height=11,
            fill=BRASS_GRAD, stroke=INK, strokeWidth=3)
# sheen across the felt — it is soft, not invisible
d.path("M420,586 L700,580 L706,592 L414,598 Z", "Felt sheen",
       fill="#FFFFFF", opacity=8, stroke=NONE)

# --- paws at work on the lining -----------------------------------------------------
# left paw pressing the lining into the far corner
d.path("M505,540 C478,556 462,574 456,594", "Arm L", fill=NONE,
       stroke="#A1815F", strokeWidth=17, cap="round")
d.shape("ellipse", "Paw L", x=438, y=586, width=32, height=28,
        fill="#CBB096", stroke=INK, strokeWidth=4)
# the felt strip being laid — one end held, draping into the tray
d.path("M462,602 C520,596 580,586 640,566 L652,584 C596,606 534,618 "
       "470,622 Z", "Felt strip", fill="#B2B5C4", stroke=INK,
       strokeWidth=3.5, join="round")
# right paw holding the strip's free end aloft
d.path("M650,536 C668,544 682,552 692,562", "Arm R", fill=NONE,
       stroke="#A1815F", strokeWidth=17, cap="round")
d.shape("ellipse", "Paw R", x=656, y=548, width=32, height=28,
        fill="#CBB096", stroke=INK, strokeWidth=4)

# --- the stack of pre-cut lining, sized to the furniture ------------------------------
for i, y in enumerate([612, 598, 584]):
    d.path(f"M{688 - i*5},{y} L{756 - i*3},{y} L{762 - i*3},{y+12} "
           f"L{694 - i*5},{y+12} Z", f"Felt sheet {i+1}",
           fill=["#75788A", "#8C8FA0", "#A5A8B6"][i], stroke=INK,
           strokeWidth=3.5, join="round")

# --- motes, muffled ------------------------------------------------------------------
for i, (x, y, w) in enumerate([(258,428,5),(300,580,6),(676,246,5),(826,480,6),
                               (216,636,5),(836,624,5),(362,296,5)]):
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#A8A2C4", opacity=35, stroke=NONE)

# --- captions -------------------------------------------------------------------------
d.text("WITNESS FELT", "Name", x=500, y=930, size=58,
       font="Virelai Sans", color="#EDE4D4", justify="center")
r = d.text("MEASURED IN DECIBELS PREVENTED", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#A9A2C0", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("291.witness-felt-V1R00")
