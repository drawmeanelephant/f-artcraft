#!/usr/bin/env python3
"""Indexer Hexley — mascot portrait V1R00.
Lost Query Archivist at a dusty card catalog offline since 1996,
holding the only query result the index ever returned: "Result 0 of 404".
Absent-minded and dusty. 1000x1000. Gradients + translucent shading."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Indexer Hexley — Mascot Portrait", 1000, 1000)

INK = "#2C2420"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#221B12"}, {"offset": 1, "color": "#0E0A06"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#776344"}, {"offset": 0.7, "color": "#463827"},
    {"offset": 1, "color": "#211A10"}]}}
WOOD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7A5E3C"}, {"offset": 1, "color": "#4A3620"}]}}
WOOD_DK = "#38280F"
CARDIGAN = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6E5A44"}, {"offset": 1, "color": "#453524"}]}}
CARDIGAN_DK = "#372A1C"
FACE = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#EFE0C4"}, {"offset": 1, "color": "#CFB48C"}]}}
CARD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F0E7CC"}, {"offset": 1, "color": "#D4C6A0"}]}}
DUST = "#C9B890"
BRASS = "#B89A5C"
DIM = "#8A7A56"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#6E5C3C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8CBA4", strokeWidth=3, opacity=45)
for i, (x, y, w) in enumerate([(193,232,8),(800,234,7),(158,522,9),(835,542,8),
                               (245,768,7),(755,746,9),(132,392,6),(862,394,7),
                               (390,110,7),(614,112,8),(332,824,6),(666,818,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#33291A", opacity=50, stroke=NONE)

# dust motes drifting through a shaft of lamplight, upper left
d.path("M180,120 L420,120 L340,640 L140,640 Z", "Dust shaft", fill="#E8D9A8",
       opacity=7, stroke=NONE)
for i, (x, y, w) in enumerate([(230,220,5),(300,290,4),(260,380,6),(330,450,4),
                               (210,480,5),(360,540,4),(280,560,5),(190,330,4),
                               (390,180,4),(350,350,5)]):
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill=DUST, opacity=55, stroke=NONE)

# --- ground -------------------------------------------------------------------
d.shape("ellipse", "Ground", x=210, y=710, width=580, height=86,
        fill="#100C06", opacity=75, stroke=NONE)

# --- the card catalog, right side ----------------------------------------------
d.path("M560,330 L812,330 L812,730 L560,730 Z", "Cabinet",
       fill=WOOD, stroke=INK, strokeWidth=7)
d.path("M552,318 L820,318 L812,340 L560,340 Z", "Cabinet top",
       fill="#8A6C44", stroke=INK, strokeWidth=5, join="round")
# drawers: 3 columns x 4 rows
for r_i in range(4):
    for c_i in range(3):
        x = 576 + c_i * 78
        y = 352 + r_i * 92
        d.shape("rectangle", f"Drawer {r_i+1}.{c_i+1}", x=x, y=y,
                width=68, height=80, fill="#6A4F2E", stroke=INK,
                strokeWidth=4)
        # brass label holder + typed label
        d.shape("rectangle", f"Label {r_i+1}.{c_i+1}", x=x+12, y=y+14,
                width=44, height=18, fill=BRASS, stroke=INK, strokeWidth=2)
        d.shape("rectangle", f"Label card {r_i+1}.{c_i+1}", x=x+16, y=y+17,
                width=36, height=12, fill="#E8DFC0", stroke=NONE)
        d.shape("ellipse", f"Knob {r_i+1}.{c_i+1}", x=x+28, y=y+50,
                width=12, height=10, fill=BRASS, stroke=INK, strokeWidth=2)
# drawer 2.2 pulled open, cards fanned out of it
d.path(rot_rect_path(660, 420, 78, 64, 8), "Open drawer",
       fill="#5A4226", stroke=INK, strokeWidth=5)
d.path(rot_rect_path(660, 394, 70, 26, 8), "Drawer dark", fill="#241A0C",
       stroke=INK, strokeWidth=4)
for i, deg in enumerate([-14, -4, 7]):
    d.path(rot_rect_path(660 + i*6, 372 + i*4, 52, 34, deg),
           f"Fanned card {i+1}", fill=CARD, stroke=INK, strokeWidth=3)
# cobweb in the cabinet's upper left corner
cx, cy = 568, 340
for i, ang in enumerate([0, 25, 50, 75]):
    a = math.radians(ang)
    d.path(f"M{cx},{cy} L{cx + 74*math.cos(a):.0f},{cy + 74*math.sin(a):.0f}",
           f"Web spoke {i+1}", fill=NONE, stroke=DUST, strokeWidth=2,
           opacity=50)
for i, r in enumerate([26, 48, 70]):
    d.path(f"M{cx + r:.0f},{cy} A{r},{r} 0 0 1 {cx},{cy + r:.0f}",
           f"Web arc {i+1}", fill=NONE, stroke=DUST, strokeWidth=2,
           opacity=45)
# taped sign: OFFLINE SINCE 1996 — digits need Source Sans 3
d.path(rot_rect_path(690, 316, 180, 34, -4), "Offline sign",
       fill="#E8DFC0", stroke=INK, strokeWidth=4)
d.path(rot_rect_path(612, 310, 26, 16, -30), "Tape L", fill="#D8CFA8",
       stroke=NONE, opacity=80)
d.path(rot_rect_path(768, 306, 26, 16, 25), "Tape R", fill="#D8CFA8",
       stroke=NONE, opacity=80)
d.text("OFFLINE SINCE 1996", "Sign text", x=690, y=324, size=13,
       font="Source Sans 3", color="#5A4A30", justify="center")

# --- hexley: the archivist -------------------------------------------------------
# hunched cardigan
d.path("M390,445 C455,445 510,490 522,555 C532,616 528,668 522,730 "
       "L270,730 C262,668 258,616 268,555 C280,490 330,445 390,445 Z",
       "Cardigan", fill=CARDIGAN, stroke=INK, strokeWidth=7)
# shawl collar + buttons
d.path("M344,458 L390,500 L436,458", "Shawl collar", fill=NONE,
       stroke=CARDIGAN_DK, strokeWidth=10, join="round")
d.path("M390,500 L390,700", "Cardigan placket", fill=NONE,
       stroke=CARDIGAN_DK, strokeWidth=5)
for i, y in enumerate([540, 596, 652]):
    d.shape("ellipse", f"Button {i+1}", x=384, y=y, width=12, height=12,
            fill=BRASS, stroke=INK, strokeWidth=3)
# elbow patches
d.path("M286,586 C296,576 314,576 322,588 C318,606 296,610 286,598 Z",
       "Elbow patch L", fill=WOOD_DK, stroke=INK, strokeWidth=3, opacity=90)

# head, tipped with distracted softness
d.shape("ellipse", "Head", x=310, y=310, width=152, height=144,
        fill=FACE, stroke=INK, strokeWidth=7)
# wispy hair tufts
d.path("M320,330 C300,318 290,300 292,284 C302,296 316,302 328,304",
       "Tuft L", fill="#D8CFA8", stroke=INK, strokeWidth=4, join="round")
d.path("M452,328 C468,314 474,298 470,282 C462,294 448,300 438,302",
       "Tuft R", fill="#D8CFA8", stroke=INK, strokeWidth=4, join="round")
d.path("M350,306 C360,290 380,280 398,280 C386,292 374,300 366,308",
       "Tuft top", fill="#D8CFA8", stroke=INK, strokeWidth=4, join="round")
# round spectacles, slightly askew
d.shape("ellipse", "Lens L", x=330, y=352, width=40, height=40, fill=NONE,
        stroke=INK, strokeWidth=4)
d.shape("ellipse", "Lens R", x=396, y=348, width=40, height=40, fill=NONE,
        stroke=INK, strokeWidth=4)
d.path("M370,368 C378,362 388,360 396,364", "Bridge", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.path("M436,360 L458,352", "Temple arm", fill=NONE, stroke=INK,
       strokeWidth=4, cap="round")
d.shape("ellipse", "Eye L", x=342, y=362, width=14, height=16, fill=INK,
        stroke=NONE)
d.shape("ellipse", "Eye R", x=408, y=358, width=14, height=16, fill=INK,
        stroke=NONE)
# one brow up — mildly surprised the drawer is empty
d.path("M334,338 C344,330 358,329 366,334", "Brow L", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.path("M400,332 C412,324 428,325 436,331", "Brow R raised", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
# soft absent smile
d.path("M356,418 C368,428 392,430 408,422", "Absent smile", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
# dust on the head and shoulders
for i, (x, y) in enumerate([(336,322),(448,344),(306,466),(498,500)]):
    d.shape("ellipse", f"Dust on hexley {i+1}", x=x, y=y, width=6, height=5,
            fill=DUST, opacity=70, stroke=NONE)

# --- the result card, held out at arm's length -------------------------------------
# arm reaching toward the viewer-left, card pinched in two fingers
d.path("M310,540 C280,560 258,584 246,610", "Arm L", fill=NONE,
       stroke=CARDIGAN, strokeWidth=30, cap="round")
d.shape("ellipse", "Hand L", x=232, y=602, width=30, height=24, fill=FACE,
        stroke=INK, strokeWidth=5)
d.path(rot_rect_path(210, 560, 118, 76, -8), "Result card", fill=CARD,
       stroke=INK, strokeWidth=4)
# header rule + the result, digits in Source Sans 3
d.path(rot_rect_path(210, 542, 96, 4, -8), "Card rule", fill="#9A8F6C",
       stroke=NONE, opacity=80)
d.text("RESULT 0 OF 404", "Result text", x=208, y=576, size=15,
       font="Source Sans 3", color="#6A3226", justify="center")
d.path("M176,592 L246,584", "Card underline", fill=NONE, stroke="#9A8F6C",
       strokeWidth=3, opacity=70)

# right hand trailing an index card back toward the open drawer
d.path("M470,540 C500,560 522,586 534,612", "Arm R", fill=NONE,
       stroke=CARDIGAN, strokeWidth=30, cap="round")
d.shape("ellipse", "Hand R", x=522, y=600, width=30, height=24, fill=FACE,
        stroke=INK, strokeWidth=5)
d.path(rot_rect_path(560, 570, 56, 40, 18), "Trailing card", fill=CARD,
       stroke=INK, strokeWidth=3, opacity=85)

# --- captions -------------------------------------------------------------------
d.text("INDEXER HEXLEY", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#E8DCC0", justify="center")
r = d.text("LOST QUERY ARCHIVIST", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#B8A678", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("015.indexer-hexley-V1R00")
