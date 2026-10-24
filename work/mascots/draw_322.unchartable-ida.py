#!/usr/bin/env python3
"""Unchartable Ida — mascot portrait V1R00.
A small archivist in spectacles beside a wall monitor; the plotted
trendline has burst through the top bezel and embedded itself in the
drywall. Some burdens refuse the shape of a dashboard. 1000x1000.
Gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Unchartable Ida — Mascot Portrait", 1000, 1000)

INK = "#1A2020"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#0E1414"}, {"offset": 1, "color": "#050808"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#465E58"}, {"offset": 0.7, "color": "#2C3E3A"},
    {"offset": 1, "color": "#141E1C"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3A322C"}, {"offset": 1, "color": "#181310"}]}}
BEZEL = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3E4A50"}, {"offset": 1, "color": "#1C2428"}]}}
SCREEN = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#12261E"}, {"offset": 1, "color": "#08120E"}]}}
COAT = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#EDE6D8"}, {"offset": 1, "color": "#B8AE9C"}]}}
SKIN = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E8C9A8"}, {"offset": 1, "color": "#B08E6E"}]}}
HOT = "#F0A04A"
PHOS = "#7EE8A8"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#6E8E84", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D2E4DC", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(193,233,8),(801,230,7),(157,524,9),(837,544,8),
                               (247,766,7),(753,749,9),(133,393,6),(864,391,7),
                               (391,113,7),(613,110,8),(333,823,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#2E423C", opacity=45, stroke=NONE)

# --- floor ----------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0C0808",
       strokeWidth=4, opacity=70)

# --- drywall damage: the trendline embedded in the wall -----------------------------
d.shape("ellipse", "Impact glow", x=688, y=150, width=170, height=140,
        fill=HOT, opacity=12, stroke=NONE)
# radiating plaster cracks
for i, (x1, y1, x2, y2) in enumerate([
        (758,222, 706,196), (758,222, 700,244), (758,222, 810,176),
        (758,222, 824,214), (758,222, 800,268), (758,222, 762,148)]):
    d.path(f"M{x1},{y1} L{x2},{y2}", f"Wall crack {i+1}", fill=NONE,
           stroke="#0E1210", strokeWidth=3, cap="round", opacity=75)
# secondary crack forks
d.path("M706,196 L686,182 M810,176 L824,158 M824,214 L846,222",
       "Crack forks", fill=NONE, stroke="#0E1210", strokeWidth=2,
       cap="round", opacity=60)
# impact hole
d.shape("ellipse", "Drywall hole", x=744, y=206, width=30, height=32,
        fill="#0A0E0C", stroke="#3E4A42", strokeWidth=3)
# falling plaster chips + dust
for i, (x, y, w) in enumerate([(736,262,9),(784,286,7),(762,312,6),
                               (810,250,5),(718,282,6)]):
    d.shape("ellipse", f"Plaster chip {i+1}", x=x, y=y, width=w, height=w,
            fill="#8A948C", opacity=60, stroke=NONE)

# --- the escaped trendline: jagged, hot, still climbing -------------------------------
d.path("M690,348 L712,312 L700,282 L736,252 L726,230 L758,222",
       "Escaped line glow", fill=NONE, stroke=HOT, strokeWidth=11,
       cap="round", join="round", opacity=25)
d.path("M690,348 L712,312 L700,282 L736,252 L726,230 L758,222",
       "Escaped line", fill=NONE, stroke=HOT, strokeWidth=5,
       cap="round", join="round")

# --- the monitor ----------------------------------------------------------------------
d.shape("ellipse", "Monitor shadow", x=430, y=682, width=400, height=24,
        fill="#060A08", opacity=50, stroke=NONE)
# stand
d.path("M596,640 L640,640 L646,688 L590,688 Z", "Stand neck",
       fill=BEZEL, stroke=INK, strokeWidth=4)
d.path("M560,688 L676,688 L692,700 L544,700 Z", "Stand foot",
       fill=BEZEL, stroke=INK, strokeWidth=4, join="round")
# bezel + screen
d.shape("rectangle", "Bezel", x=430, y=330, width=380, height=310,
        fill=BEZEL, stroke=INK, strokeWidth=6, radius=10)
d.shape("rectangle", "Screen", x=452, y=352, width=336, height=252,
        fill=SCREEN, stroke="#0C1410", strokeWidth=3, radius=4)
# bezel breach notch where the line exits
d.path("M672,330 L700,330 L694,352 L678,352 Z", "Bezel breach",
       fill="#0C1410", stroke=NONE)
# screen cracks radiating down from the breach
for i, (x2, y2) in enumerate([(640,420),(716,404),(668,470),(742,442)]):
    d.path(f"M690,352 L{x2},{y2}", f"Screen crack {i+1}", fill=NONE,
           stroke="#4A6E5E", strokeWidth=2, opacity=60)
# faint grid + axes inside the screen
for gy in (400, 448, 496, 544):
    d.path(f"M452,{gy} L788,{gy}", f"Grid {gy}", fill=NONE,
           stroke="#1E3A2E", strokeWidth=1.5, opacity=70)
for gx in (536, 620, 704):
    d.path(f"M{gx},352 L{gx},604", f"Vgrid {gx}", fill=NONE,
           stroke="#1E3A2E", strokeWidth=1.5, opacity=60)
d.path("M470,604 L470,368 M470,604 L780,604", "Axes", fill=NONE,
       stroke="#3E5E50", strokeWidth=3, opacity=85)
# the plotted trendline inside the screen — calm at first, then escaping
d.path("M478,580 L540,556 L590,574 L636,520 L664,470 L682,412 L690,352",
       "Trendline glow", fill=NONE, stroke=PHOS, strokeWidth=9,
       cap="round", join="round", opacity=22)
d.path("M478,580 L540,556 L590,574 L636,520 L664,470 L682,412 L690,352",
       "Trendline", fill=NONE, stroke=PHOS, strokeWidth=4,
       cap="round", join="round")
# data dots along the trend
for i, (x, y) in enumerate([(478,580),(540,556),(590,574),(636,520),
                            (664,470),(682,412)]):
    d.shape("ellipse", f"Data dot {i+1}", x=x-4, y=y-4, width=8, height=8,
            fill=PHOS, stroke=NONE)
# status strip on the bezel lip
d.text("BURDEN INDEX", "Screen label", x=470, y=376, size=12,
       font="Virelai Sans", color="#4E7A66", justify="left")
d.shape("ellipse", "Bezel LED", x=788, y=626, width=10, height=10,
        fill=HOT, stroke=NONE, opacity=90)

# --- Ida: small archivist in a lab coat, looking up at the breach ---------------------
d.shape("ellipse", "Ida shadow", x=270, y=682, width=140, height=20,
        fill="#060A08", opacity=50, stroke=NONE)
# coat body
d.path("M338,478 C306,478 286,506 284,552 L280,690 L392,690 L388,552 "
       "C386,506 366,478 338,478 Z", "Coat", fill=COAT, stroke=INK,
       strokeWidth=5, join="round")
# coat collar + buttons
d.path("M320,486 L336,512 L352,486", "Collar", fill=NONE, stroke=INK,
       strokeWidth=4, cap="round", join="round")
d.path("M336,512 L336,690", "Coat seam", fill=NONE, stroke="#8A8272",
       strokeWidth=3, opacity=70)
for i, by in enumerate([545, 590, 635]):
    d.shape("ellipse", f"Button {i+1}", x=345, y=by, width=9, height=9,
            fill="#6E6658", stroke=NONE)
# pocket with pens
d.shape("rectangle", "Pocket", x=292, y=596, width=44, height=34,
        fill="#DCD4C2", stroke=INK, strokeWidth=3, radius=3)
d.path("M300,592 L304,578 M314,592 L314,574", "Pens", fill=NONE,
       stroke=HOT, strokeWidth=4, cap="round")
# head
d.shape("ellipse", "Head", x=292, y=368, width=92, height=96,
        fill=SKIN, stroke=INK, strokeWidth=5)
# hair: a tidy bun + fringe
d.path("M292,414 C290,382 312,362 338,362 C366,362 386,382 384,414 "
       "C370,398 306,398 292,414 Z", "Hair cap", fill="#4E3A2E",
       stroke=INK, strokeWidth=4, join="round")
d.shape("ellipse", "Bun", x=322, y=344, width=34, height=30,
        fill="#4E3A2E", stroke=INK, strokeWidth=4)
# spectacles, tilted up toward the screen
for cx in (322, 358):
    d.shape("ellipse", f"Lens {cx}", x=cx-13, y=404, width=26, height=24,
            fill="#FFFFFF", opacity=18, stroke=INK, strokeWidth=3.5)
d.path("M335,416 L345,416 M309,412 L292,404 M371,412 L384,404",
       "Specs frame", fill=NONE, stroke=INK, strokeWidth=3, cap="round")
# worried eyes behind the lenses
d.shape("ellipse", "Eye L", x=316, y=414, width=7, height=9,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Eye R", x=352, y=414, width=7, height=9,
        fill=INK, stroke=NONE)
# raised brows — alarm
d.path("M310,398 L330,394 M348,394 L368,398", "Brows", fill=NONE,
       stroke=INK, strokeWidth=3.5, cap="round")
# small open mouth
d.shape("ellipse", "Mouth", x=332, y=440, width=14, height=10,
        fill="#6E3E34", stroke=INK, strokeWidth=3)
# arm raised, pointing at the breach
d.path("M384,540 C420,510 448,478 470,442 L484,452 C464,492 434,526 398,552 Z",
       "Arm", fill=COAT, stroke=INK, strokeWidth=4, join="round")
d.shape("ellipse", "Hand", x=464, y=430, width=22, height=20,
        fill=SKIN, stroke=INK, strokeWidth=3.5)
# clipboard under the other arm
d.path(rot_rect_path(288, 580, 46, 62, 8), "Clipboard",
       fill={"gradient": {"kind": "linear", "stops": [
           {"offset": 0, "color": "#8A6E4E"}, {"offset": 1, "color": "#5E4A32"}]}},
       stroke=INK, strokeWidth=3.5)
d.path(rot_rect_path(288, 580, 36, 48, 8), "Clip page",
       fill="#EDE6D8", stroke=INK, strokeWidth=2.5)
# a chart on the clipboard that flatlines
d.path("M272,586 L284,586 L290,592 L296,586 L306,586", "Clip flatline",
       fill=NONE, stroke="#8A4A42", strokeWidth=2.5, cap="round",
       join="round")

# --- dropped chart pages on the floor ---------------------------------------------------
d.path(rot_rect_path(452, 690, 54, 40, -12), "Fallen page 1",
       fill="#D8D2C0", stroke=INK, strokeWidth=3, opacity=90)
d.path("M436,688 L452,684 L466,690", "Fallen chart 1", fill=NONE,
       stroke="#6E7A72", strokeWidth=2, opacity=70)
d.path(rot_rect_path(514, 698, 46, 34, 9), "Fallen page 2",
       fill="#C8C2B0", stroke=INK, strokeWidth=3, opacity=85)

# --- captions ----------------------------------------------------------------------
d.text("UNCHARTABLE IDA", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#D2E4DC", justify="center")
r = d.text("CUSTODIAN OF THE UNMEASURED", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#8EB0A4", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("322.unchartable-ida-V1R00")
