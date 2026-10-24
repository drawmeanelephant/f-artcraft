#!/usr/bin/env python3
"""Guacamole Gardener — mascot portrait V1R00.
An avocado gardener tending a crate of recipe records in a verdant grove,
lime zest scattered over the filings. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Guacamole Gardener — Mascot Portrait", 1000, 1000)

INK = "#26301C"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#12200F"}, {"offset": 1, "color": "#060C05"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4A7A4E"}, {"offset": 0.7, "color": "#2E5238"},
    {"offset": 1, "color": "#152A1C"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#27462E"}, {"offset": 1, "color": "#0F1E12"}]}}
BODY_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#8CC765"}, {"offset": 0.65, "color": "#5E9A44"},
    {"offset": 1, "color": "#33602C"}]}}
PIT_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#A9743E"}, {"offset": 0.75, "color": "#7A4E28"},
    {"offset": 1, "color": "#4E3018"}]}}
CRATE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#8A6A42"}, {"offset": 1, "color": "#54401F"}]}}
CARD_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F2E9C8"}, {"offset": 1, "color": "#CDBD8E"}]}}
HAT_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E4C87E"}, {"offset": 1, "color": "#A8854A"}]}}
POT_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#A86A4A"}, {"offset": 1, "color": "#6E4028"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#4E7A56", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D6ECD2", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(193,233,8),(801,230,7),(157,524,9),(837,544,8),
                               (247,766,7),(753,749,9),(133,393,6),(864,391,7),
                               (391,113,7),(613,110,8),(333,823,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#3A6042", opacity=45, stroke=NONE)

# --- distant grove: soft tree masses inside the disc --------------------------
d.shape("ellipse", "Grove L", x=110, y=180, width=220, height=300,
        fill="#1E3A24", opacity=55, stroke=NONE)
d.shape("ellipse", "Grove R", x=690, y=160, width=210, height=310,
        fill="#1E3A24", opacity=55, stroke=NONE)
d.shape("ellipse", "Grove top", x=360, y=70, width=300, height=140,
        fill="#24402A", opacity=45, stroke=NONE)
# hanging avocados in the far boughs
for i, (x, y) in enumerate([(215,300),(770,290),(255,380),(745,365)]):
    d.shape("ellipse", f"Far fruit {i+1}", x=x, y=y, width=20, height=26,
            fill="#3E6A38", opacity=70, stroke=NONE)

# --- floor: bottom segment closed on the disc's own arc -----------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0B180D",
       strokeWidth=4, opacity=70)

# --- recipe crate, right of the mascot ----------------------------------------
d.shape("ellipse", "Crate shadow", x=600, y=672, width=230, height=26,
        fill="#071007", opacity=50, stroke=NONE)
# recipe cards sticking up out of the crate
for i, (x, y, rot) in enumerate([(640,500,-8),(688,492,4),(736,502,10)]):
    d.path(f"M{x},{y+66} L{x},{y} L{x+40},{y} L{x+40},{y+66} Z",
           f"Recipe card {i+1}", fill=CARD_GRAD, stroke=INK, strokeWidth=3,
           join="round")
    for j in range(3):
        d.path(f"M{x+7},{y+14+j*12} L{x+33},{y+14+j*12}",
               f"Card {i+1} line {j+1}", fill=NONE, stroke="#8A7A52",
               strokeWidth=3, opacity=70, cap="round")
# crate body
d.shape("rectangle", "Crate", x=615, y=570, width=200, height=105,
        fill=CRATE_GRAD, stroke=INK, strokeWidth=5, radius=6)
d.path("M615,604 L815,604 M615,640 L815,640", "Crate slats", fill=NONE,
       stroke="#3E2E16", strokeWidth=4, opacity=65)
d.shape("rectangle", "Crate label", x=672, y=610, width=86, height=26,
        fill="#E8DCB4", stroke=INK, strokeWidth=3, radius=4)
d.text("RECIPES", "Crate text", x=715, y=628, size=13, font="Virelai Sans",
       color="#5A4A28", justify="center")

# --- potted avocado sprout, left ----------------------------------------------
d.shape("ellipse", "Pot shadow", x=185, y=668, width=150, height=22,
        fill="#071007", opacity=50, stroke=NONE)
d.path("M225,600 L305,600 L292,672 L238,672 Z", "Pot", fill=POT_GRAD,
       stroke=INK, strokeWidth=5, join="round")
d.shape("rectangle", "Pot rim", x=215, y=586, width=100, height=22,
        fill=POT_GRAD, stroke=INK, strokeWidth=4, radius=5)
d.path("M265,586 C265,556 258,540 250,524", "Sprout stem", fill=NONE,
       stroke="#4E8A3C", strokeWidth=6, cap="round")
d.path("M250,524 C232,516 226,498 232,484 C250,490 258,506 250,524 Z",
       "Sprout leaf L", fill="#6EB04E", stroke=INK, strokeWidth=3, join="round")
d.path("M252,530 C270,520 288,522 296,534 C282,546 262,544 252,530 Z",
       "Sprout leaf R", fill="#7CC25A", stroke=INK, strokeWidth=3, join="round")

# --- the mascot: avocado gardener ---------------------------------------------
d.shape("ellipse", "Body shadow", x=380, y=668, width=240, height=30,
        fill="#071007", opacity=50, stroke=NONE)
# feet
d.shape("ellipse", "Foot L", x=430, y=648, width=52, height=30,
        fill="#2A4A24", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Foot R", x=518, y=648, width=52, height=30,
        fill="#2A4A24", stroke=INK, strokeWidth=4)
# pear-shaped body
d.path("M500,330 C568,330 604,404 604,488 C604,582 562,656 500,656 "
       "C438,656 396,582 396,488 C396,404 432,330 500,330 Z",
       "Avocado body", fill=BODY_GRAD, stroke=INK, strokeWidth=6)
# belly pit — the creamy heart of the record
d.shape("ellipse", "Pit", x=446, y=520, width=108, height=116,
        fill=PIT_GRAD, stroke=INK, strokeWidth=5)
d.shape("ellipse", "Pit sheen", x=462, y=534, width=34, height=22,
        fill="#D8A86A", opacity=55, stroke=NONE)
# stubby arms: left pats the crate, right holds a trowel
d.path("M400,470 C368,478 356,506 362,532", "Arm L", fill=NONE,
       stroke="#4E8038", strokeWidth=18, cap="round")
d.path("M600,460 C636,448 662,452 680,470", "Arm R", fill=NONE,
       stroke="#4E8038", strokeWidth=18, cap="round")
# trowel in right hand
d.path("M676,468 L700,442", "Trowel handle", fill=NONE, stroke="#6E4A28",
       strokeWidth=9, cap="round")
d.path("M700,442 L728,416 L734,424 L712,452 Z", "Trowel blade",
       fill="#9AA8B0", stroke=INK, strokeWidth=3, join="round")
# face: content arched eyes, small smile, cheek blush
d.path("M440,432 C448,422 462,422 470,432", "Eye L", fill=NONE, stroke=INK,
       strokeWidth=6, cap="round")
d.path("M530,432 C538,422 552,422 560,432", "Eye R", fill=NONE, stroke=INK,
       strokeWidth=6, cap="round")
d.path("M472,470 C486,482 514,482 528,470", "Smile", fill=NONE, stroke=INK,
       strokeWidth=6, cap="round")
d.shape("ellipse", "Blush L", x=424, y=448, width=26, height=14,
        fill="#E8986A", opacity=45, stroke=NONE)
d.shape("ellipse", "Blush R", x=550, y=448, width=26, height=14,
        fill="#E8986A", opacity=45, stroke=NONE)
# leaf sprout poking from under the hat
d.path("M500,330 C500,308 492,296 484,286", "Head stem", fill=NONE,
       stroke="#4E8A3C", strokeWidth=7, cap="round")
d.path("M484,286 C466,280 458,264 464,250 C482,256 492,270 484,286 Z",
       "Head leaf", fill="#6EB04E", stroke=INK, strokeWidth=3, join="round")
# straw gardener hat, tipped forward
d.path("M430,326 C440,280 560,280 570,326 Z", "Hat dome",
       fill=HAT_GRAD, stroke=INK, strokeWidth=5, join="round")
d.shape("ellipse", "Hat brim", x=398, y=312, width=204, height=34,
        fill=HAT_GRAD, stroke=INK, strokeWidth=5)
d.path("M436,314 C460,304 540,304 564,314", "Hat band", fill=NONE,
       stroke="#7A5A30", strokeWidth=8, cap="round")

# --- scattered lime zest over the filings -------------------------------------
for i, (x, y, c) in enumerate([(630,560,"#D8E850"),(700,540,"#C8E838"),
                               (770,565,"#D8E850"),(655,690,"#C8E838"),
                               (745,692,"#D8E850"),(352,678,"#C8E838"),
                               (595,682,"#D8E850")]):
    d.path(f"M{x},{y} c6,-8 16,-8 20,0", f"Zest {i+1}", fill=NONE,
           stroke=c, strokeWidth=5, cap="round")
for i, (x, y) in enumerate([(668,556),(722,548),(788,580),(620,694),(700,700)]):
    d.shape("ellipse", f"Zest fleck {i+1}", x=x, y=y, width=7, height=5,
            fill="#DCEC58", opacity=80, stroke=NONE)

# --- captions ------------------------------------------------------------------
d.text("GUACAMOLE GARDENER", "Name", x=500, y=930, size=52, font="Virelai Sans",
       color="#D6ECD2", justify="center")
r = d.text("ZEST CURATOR", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#8EBA8E", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("215.guacamole-gardener-V1R00")
