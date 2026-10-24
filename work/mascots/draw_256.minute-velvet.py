#!/usr/bin/env python3
"""Minute Velvet — mascot portrait V1R00.
A plush velvet upholsterer draping a heavy cloth over the official minutes
of a meeting that has already emptied. One layer per degree of hostility;
the nap always runs toward the reader.
1000x1000. Gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Minute Velvet — Mascot Portrait", 1000, 1000)

INK = "#453030"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1A0E18"}, {"offset": 1, "color": "#0B060B"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#5A4456"}, {"offset": 0.7, "color": "#382838"},
    {"offset": 1, "color": "#1C121E"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#30222E"}, {"offset": 1, "color": "#140E16"}]}}
PAGE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F2E8D4"}, {"offset": 1, "color": "#D8C4A0"}]}}
VELVET = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#8A4662"}, {"offset": 0.55, "color": "#652C46"},
    {"offset": 1, "color": "#421A30"}]}}
VELVET_BODY = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#9A5470"}, {"offset": 0.7, "color": "#6E3050"},
    {"offset": 1, "color": "#471E38"}]}}
WOOD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6E4A3A"}, {"offset": 1, "color": "#3E2620"}]}}
GOLD_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E8C878"}, {"offset": 1, "color": "#A8803E"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#9A7E96", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8D8E4", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(193,233,8),(801,230,7),(157,524,9),(837,544,8),
                               (247,766,7),(753,749,9),(133,393,6),(864,391,7),
                               (391,113,7),(613,110,8),(333,823,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#4E3A4C", opacity=45, stroke=NONE)

# --- floor ----------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#120A12",
       strokeWidth=4, opacity=70)

# --- the emptied room: door ajar + abandoned chair, kept quiet ----------------------
d.path("M205,300 L268,288 L268,560 L205,548 Z", "Door ajar",
       fill="#241822", stroke=INK, strokeWidth=4, join="round", opacity=85)
d.shape("ellipse", "Door light slit", x=262, y=296, width=8, height=258,
        fill="#C8A868", opacity=25, stroke=NONE)
d.shape("ellipse", "Chair shadow", x=722, y=648, width=110, height=14,
        fill="#0E080E", opacity=45, stroke=NONE)
d.path("M745,560 L745,650 M795,560 L795,650", "Chair legs", fill=NONE,
       stroke="#241822", strokeWidth=7, cap="round", opacity=80)
d.path("M735,558 L805,558 L800,585 L740,585 Z", "Chair seat",
       fill="#2E1E2C", stroke=INK, strokeWidth=3, join="round", opacity=80)
d.path("M735,558 L740,470 L752,470 L748,558 Z", "Chair back",
       fill="#2E1E2C", stroke=INK, strokeWidth=3, join="round", opacity=80)

# --- easel + the minutes -----------------------------------------------------------
d.shape("ellipse", "Easel shadow", x=520, y=700, width=280, height=24,
        fill="#0E080E", opacity=50, stroke=NONE)
d.path("M575,600 L545,705 M725,600 L755,705 M650,610 L650,710",
       "Easel legs", fill=NONE, stroke=WOOD, strokeWidth=9, cap="round")
d.shape("rectangle", "Easel ledge", x=552, y=588, width=196, height=16,
        fill=WOOD, stroke=INK, strokeWidth=3, radius=4)

# the transcript page on the easel
d.shape("rectangle", "Page", x=560, y=322, width=180, height=270,
        fill=PAGE_GRAD, stroke=INK, strokeWidth=5)
d.path("M572,338 L728,338 M572,580 L728,580", "Page rules", fill=NONE,
       stroke="#A08858", strokeWidth=2.5, opacity=70)
d.path("M576,344 C576,340 580,340 580,344 M724,344 C724,340 720,340 720,344 "
       "M576,574 C576,578 580,578 580,574 M724,574 C724,578 720,578 720,574",
       "Corner flourishes", fill=NONE, stroke="#A08858", strokeWidth=2,
       opacity=60)
d.text("MINUTES", "Page head", x=650, y=360, size=19, font="Virelai Sans",
       color="#5E4630", justify="center")
d.path("M600,368 C630,376 670,376 700,368", "Head swash", fill=NONE,
       stroke="#A08858", strokeWidth=2.5, cap="round", opacity=75)
# elegant text rows — the calm record of a loud room
for i, (y, w) in enumerate([(392,120),(410,132),(428,110),(446,124),
                            (464,132),(505,126),(523,116),(541,128),
                            (559,104)]):
    d.shape("rectangle", f"Minute line {i+1}", x=580, y=y, width=w, height=6,
            fill="#9A8668", opacity=75, stroke=NONE, radius=3)
# wax seal at the foot of the page: it is official
d.shape("ellipse", "Seal", x=690, y=545, width=30, height=30,
        fill="#8A3A4A", stroke=INK, strokeWidth=2.5, opacity=90)
d.shape("ellipse", "Seal glint", x=697, y=551, width=10, height=6,
        fill="#D88A96", opacity=50, stroke=NONE)

# --- the velvet drape: one layer over the hostile part --------------------------------
# heavy cloth folded over the page's middle, scalloped hem, gold fringe
d.path("M534,392 C575,376 728,376 766,396 L766,462 "
       "C752,476 740,460 726,472 C712,484 700,464 686,476 "
       "C672,488 660,466 646,478 C632,490 620,468 606,478 "
       "C592,488 580,470 566,478 C552,486 534,476 534,462 Z",
       "Velvet drape", fill=VELVET, stroke=INK, strokeWidth=5, join="round")
# fold valleys
for i, (x0, y1) in enumerate([(578,468),(626,474),(676,472),(726,464)]):
    d.path(f"M{x0},390 C{x0-8},415 {x0-10},445 {x0-4},{y1}",
           f"Fold {i+1}", fill=NONE, stroke="#38141F", strokeWidth=3.5,
           cap="round", opacity=55)
# sheen high on the cloth — velvet catches light only at the crown
d.shape("ellipse", "Drape sheen", x=580, y=392, width=140, height=26,
        fill="#D88AA0", opacity=18, stroke=NONE)
d.shape("ellipse", "Drape sheen 2", x=660, y=398, width=70, height=16,
        fill="#E8A8BC", opacity=14, stroke=NONE)
# gold fringe along the scalloped hem
for i, x in enumerate(range(546, 762, 17)):
    y = 470 + (6 if (i % 3 == 1) else (0 if i % 3 == 0 else 10))
    d.path(f"M{x},{y-6} L{x},{y+10}", f"Fringe {i+1}", fill=NONE,
           stroke=GOLD_GRAD, strokeWidth=4, cap="round", opacity=90)

# --- the mascot: a small plush upholsterer, itself swaddled -------------------------
d.shape("ellipse", "Mascot shadow", x=320, y=692, width=170, height=18,
        fill="#0E080E", opacity=50, stroke=NONE)
# body: a rounded bolt of velvet, hem scalloped like its own work
d.path("M405,440 C445,440 466,470 468,510 C470,552 472,600 474,646 "
       "C462,660 452,646 440,658 C428,670 416,650 404,660 "
       "C392,670 380,652 368,660 C356,668 346,654 344,640 "
       "C346,596 344,548 342,506 C340,470 365,440 405,440 Z",
       "Mascot body", fill=VELVET_BODY, stroke=INK, strokeWidth=6)
# hem fringe, same gold as its work
for i, x in enumerate(range(356, 468, 16)):
    y = 654 + (4 if i % 2 else 8)
    d.path(f"M{x},{y-8} L{x},{y+8}", f"Hem fringe {i+1}", fill=NONE,
           stroke=GOLD_GRAD, strokeWidth=4, cap="round", opacity=90)
# crown sheen + nap ticks (the nap runs toward the reader)
d.shape("ellipse", "Body sheen", x=368, y=458, width=60, height=24,
        fill="#D88AA0", opacity=22, stroke=NONE)
for i, (x, y) in enumerate([(378,560),(402,576),(428,562),(392,600),
                            (418,604),(368,580),(438,586)]):
    d.path(f"M{x},{y} l6,10", f"Nap {i+1}", fill=NONE, stroke="#3A1626",
           strokeWidth=2.5, cap="round", opacity=45)
# face: closed, unbothered eyes — it has never read what it drapes
d.path("M386,506 C392,500 400,500 406,506", "Eye L", fill=NONE, stroke=INK,
       strokeWidth=4.5, cap="round")
d.path("M424,506 C430,500 438,500 444,506", "Eye R", fill=NONE, stroke=INK,
       strokeWidth=4.5, cap="round")
d.path("M402,528 C408,534 420,534 426,528", "Mouth", fill=NONE, stroke=INK,
       strokeWidth=4, cap="round")
d.shape("ellipse", "Blush L", x=374, y=514, width=18, height=9,
        fill="#C06A80", opacity=40, stroke=NONE)
d.shape("ellipse", "Blush R", x=440, y=514, width=18, height=9,
        fill="#C06A80", opacity=40, stroke=NONE)
# a brass draper's pin, worn like a brooch
d.shape("ellipse", "Pin head", x=404, y=548, width=14, height=14,
        fill=GOLD_GRAD, stroke=INK, strokeWidth=2.5)
d.path("M411,562 L411,574", "Pin point", fill=NONE, stroke="#A8803E",
       strokeWidth=3, cap="round")
# arms: one lifts the drape's edge, one smooths it down
d.path("M468,498 C500,490 522,478 540,462", "Arm top", fill=NONE,
       stroke=INK, strokeWidth=8, cap="round")
d.path("M470,540 C500,540 522,532 538,522", "Arm low", fill=NONE,
       stroke=INK, strokeWidth=8, cap="round")
d.shape("ellipse", "Hand top", x=534, y=452, width=16, height=14,
        fill="#8A4662", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Hand low", x=532, y=514, width=16, height=14,
        fill="#8A4662", stroke=INK, strokeWidth=3)

# --- quiet motes: the record settling to a sit-able register -------------------------
for i, (x, y, w) in enumerate([(510,250,5),(560,220,6),(610,255,4),(660,235,5),
                               (470,300,4),(700,270,5),(540,290,4),(760,300,5)]):
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#E8D8E4", opacity=30, stroke=NONE)

# --- captions ----------------------------------------------------------------------
d.text("MINUTE VELVET", "Name", x=500, y=930, size=56, font="Virelai Sans",
       color="#F0E4EA", justify="center")
r = d.text("PROCEDURAL SOFTENING", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#C09EB8", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("256.minute-velvet-V1R00")
