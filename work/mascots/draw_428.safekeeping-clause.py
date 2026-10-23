#!/usr/bin/env python3
"""Safekeeping Clause — mascot portrait V1R00. HTTP 428, "Precondition Required".
Warden mascot guarding a barred gate, clause papers in hand. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Safekeeping Clause — Mascot Portrait", 1000, 1000)

INK = "#2E2430"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#221E2E"}, {"offset": 1, "color": "#0E0C14"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E4E0E8"}, {"offset": 0.7, "color": "#B2A9BC"},
    {"offset": 1, "color": "#7C7288"}]}}
COAT_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#5E4256"}, {"offset": 0.7, "color": "#452F42"},
    {"offset": 1, "color": "#2E1F30"}]}}
STONE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#9A92A4"}, {"offset": 1, "color": "#6A6278"}]}}
PAPER_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#FDFBF2"}, {"offset": 1, "color": "#E8E2CE"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#6A6080", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#EEEAF4", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(215,225,7),(775,215,6),(245,712,7),(750,702,7),(170,450,6),
                               (832,452,6),(350,152,6),(655,148,7),(305,792,6),(695,788,6)]):
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#6A6080", opacity=40, stroke=NONE)

# --- the gate ----------------------------------------------------------------------
d.shape("ellipse", "Gate shadow", x=580, y=742, width=250, height=26,
        fill="#4A4258", opacity=40, stroke=NONE)
# darkness beyond the bars
d.path("M612,740 L612,430 C612,352 788,352 788,430 L788,740 Z",
       "Gate dark", fill={"gradient": {"kind": "linear", "stops": [
           {"offset": 0, "color": "#2A2234"}, {"offset": 1, "color": "#120E1C"}]}},
       stroke=NONE)
# bars, tops stepped to meet the arch
for i, (x, yt) in enumerate([(632, 428), (668, 400), (704, 392), (740, 400), (772, 428)]):
    d.path(f"M{x},{yt} L{x},736", f"Bar {i+1}", fill=NONE, stroke="#3A3644",
           strokeWidth=11, cap="round")
    d.path(f"M{x},{yt} L{x},736", f"Bar {i+1} shine", fill=NONE, stroke="#8A86A0",
           strokeWidth=3, cap="round", opacity=55)
# cross rails
d.path("M612,520 L788,520 M612,660 L788,660", "Rails",
       fill=NONE, stroke="#3A3644", strokeWidth=10)
# chain across the bars + padlock
d.path("M614,560 C660,586 740,586 786,556", "Chain",
       fill=NONE, stroke="#C4BECE", strokeWidth=5, cap="round", opacity=90)
d.shape("rectangle", "Padlock", x=686, y=566, width=34, height=40,
        radius=6, fill="#C9A84C", stroke=INK, strokeWidth=4)
d.path("M692,566 C692,552 714,552 714,566", "Padlock shackle",
       fill=NONE, stroke=INK, strokeWidth=4, cap="round")
d.shape("ellipse", "Padlock hole", x=700, y=582, width=7, height=10, fill="#1E1A14", stroke=NONE)
# stone pillars + arch band
for side, x in [("L", 580), ("R", 788)]:
    d.shape("rectangle", f"Pillar {side}", x=x, y=420, width=32, height=322,
            radius=6, fill=STONE_GRAD, stroke=INK, strokeWidth=5)
    d.shape("rectangle", f"Pillar cap {side}", x=x-8, y=404, width=48, height=24,
            radius=5, fill="#8A8299", stroke=INK, strokeWidth=4)
    for j, yb in enumerate([470, 530, 590, 650, 700]):
        d.path(f"M{x+4},{yb} L{x+28},{yb}", f"Pillar {side} course {j+1}",
               fill=NONE, stroke="#555063", strokeWidth=2.5, opacity=60)
d.path("M596,428 C612,344 788,344 804,428 L788,438 C772,374 628,374 612,438 Z",
       "Arch band", fill=STONE_GRAD, stroke=INK, strokeWidth=5, join="round")
d.shape("ellipse", "Keystone", x=690, y=352, width=24, height=34,
        fill="#8A8299", stroke=INK, strokeWidth=4)

# --- the warden -----------------------------------------------------------------------
d.shape("ellipse", "Figure shadow", x=300, y=744, width=280, height=28,
        fill="#4A4258", opacity=40, stroke=NONE)
# coat: broad shouldered, squared hem
d.path("M322,742 C316,650 322,552 352,494 C378,444 424,424 462,430 "
       "C506,438 534,488 540,556 C546,634 544,692 542,742 Z",
       "Coat", fill=COAT_GRAD, stroke=INK, strokeWidth=7, join="round")
# buttons
for i, y in enumerate([560, 596, 632]):
    d.shape("ellipse", f"Button {i+1}", x=430, y=y, width=12, height=12,
            fill="#C9A84C", stroke=INK, strokeWidth=2.5)
# epaulettes
d.shape("ellipse", "Epaulette L", x=344, y=486, width=46, height=22,
        fill="#C9A84C", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Epaulette R", x=492, y=478, width=46, height=22,
        fill="#C9A84C", stroke=INK, strokeWidth=4)
# head
d.shape("ellipse", "Head", x=392, y=352, width=132, height=118,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#F0DCC2"}, {"offset": 1, "color": "#D0AE90"}]}},
        stroke=INK, strokeWidth=6)
# peaked cap
d.path("M386,384 C390,338 424,314 462,316 C498,318 524,342 528,380 "
       "C496,368 418,366 386,384 Z", "Cap", fill="#33243A", stroke=INK, strokeWidth=5, join="round")
d.path("M380,386 C420,368 510,368 538,388 L530,396 C496,380 424,380 392,398 Z",
       "Cap brim", fill="#241A2C", stroke=INK, strokeWidth=4, join="round")
d.shape("ellipse", "Cap badge", x=452, y=332, width=18, height=16,
        fill="#C9A84C", stroke=INK, strokeWidth=3)
# stern face
d.shape("ellipse", "Eye L", x=428, y=408, width=20, height=22, fill="#33222A", stroke=NONE)
d.shape("ellipse", "Eye R", x=480, y=408, width=20, height=22, fill="#33222A", stroke=NONE)
d.shape("ellipse", "Glint L", x=433, y=412, width=6, height=6, fill="#FFFFFF", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=485, y=412, width=6, height=6, fill="#FFFFFF", opacity=90, stroke=NONE)
d.path("M424,394 L450,398 M480,398 L506,394", "Heavy brows",
       fill=NONE, stroke=INK, strokeWidth=5, cap="round")
d.path("M448,452 L482,452", "Mouth", fill=NONE, stroke=INK, strokeWidth=5, cap="round")
# raised hand: halt
d.path("M352,520 C330,510 316,494 310,470", "Arm L",
       fill=NONE, stroke="#452F42", strokeWidth=24, cap="round")
d.shape("ellipse", "Palm", x=284, y=428, width=44, height=52,
        fill="#E8CBA8", stroke=INK, strokeWidth=5)
d.path("M292,436 L292,424 M302,434 L302,420 M312,434 L312,420 M322,436 L322,424",
       "Fingers", fill=NONE, stroke=INK, strokeWidth=4, cap="round")
# right arm holding the clause papers at the chest
d.path("M532,520 C556,532 566,556 562,584", "Arm R",
       fill=NONE, stroke="#452F42", strokeWidth=24, cap="round")
d.shape("ellipse", "Hand R", x=540, y=572, width=30, height=28,
        fill="#E8CBA8", stroke=INK, strokeWidth=4)
# clause papers, fanned, marked with pilcrows
d.path("M452,566 L556,548 L566,608 L462,626 Z", "Clause paper A",
       fill=PAPER_GRAD, stroke=INK, strokeWidth=3.5, join="round")
d.path("M458,556 L548,538 L558,596 L468,614 Z", "Clause paper B",
       fill="#EFE9D4", stroke=INK, strokeWidth=3, join="round", opacity=95)
d.text("¶", "Pilcrow 1", x=478, y=586, size=22, font="Virelai Sans", color="#8A3444")
d.text("¶", "Pilcrow 2", x=508, y=580, size=22, font="Virelai Sans", color="#8A3444")
d.path("M470,598 L546,586 M472,608 L520,600", "Clause rules",
       fill=NONE, stroke="#9A9482", strokeWidth=3, opacity=80)

# --- name + role ----------------------------------------------------------------------
d.text("SAFEKEEPING CLAUSE", "Name", x=500, y=930, size=56, font="Virelai Sans",
       color="#EAE6F0", justify="center")
d.text(" ".join("PRECONDITION REQUIRED"), "Role", x=500, y=968, size=22, font="Virelai Sans",
       color="#B0A6C0", justify="center")

d.finish("428.safekeeping-clause-V1R00")
