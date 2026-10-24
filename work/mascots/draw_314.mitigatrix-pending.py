#!/usr/bin/env python3
"""Mitigatrix Pending — mascot portrait V1R00.
Title at full size, authority at the size the audit left: the paper crown
worn level, the scepter laid beside her with its batteries removed.
She sits correctly. There is no documented way to sit wrong. 1000x1000.
Gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Mitigatrix Pending — Mascot Portrait", 1000, 1000)

INK = "#2A1C22"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1B1420"}, {"offset": 1, "color": "#0E0A12"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#5E4C68"}, {"offset": 0.7, "color": "#3C3048"},
    {"offset": 1, "color": "#211A2A"}]}}
THRONE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7A3850"}, {"offset": 1, "color": "#48202F"}]}}
GOLD_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#D8B46A"}, {"offset": 1, "color": "#8A6836"}]}}
GOWN_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#5E6E8A"}, {"offset": 0.75, "color": "#3E4C68"},
    {"offset": 1, "color": "#28334A"}]}}
SKIN_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E4BE90"}, {"offset": 0.72, "color": "#C4976A"},
    {"offset": 1, "color": "#96683F"}]}}
PAPER_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F0E8D2"}, {"offset": 1, "color": "#C9BC9C"}]}}
GOLD = "#C9A45C"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#6E5A80", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C4B4D4", strokeWidth=3, opacity=45)
for i, (x, y, w) in enumerate([(200,240,8),(796,238,7),(164,534,9),(834,552,8),
                               (252,764,7),(746,750,9),(144,400,6),(856,396,7),
                               (398,118,7),(608,114,8),(338,822,6),(662,820,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#463A54", opacity=45, stroke=NONE)

# --- floor shadow under the throne --------------------------------------------
d.shape("ellipse", "Throne shadow", x=300, y=730, width=400, height=44,
        fill="#120C18", opacity=55, stroke=NONE)

# --- the throne: full size, as filed -------------------------------------------
# back panel with a rounded crest
d.path("M380,700 L380,310 C380,236 430,186 500,186 C570,186 620,236 620,310 "
       "L620,700 Z", "Throne back", fill=THRONE_GRAD, stroke=INK,
       strokeWidth=6, join="round")
# velvet inset panel + piping
d.path("M402,680 L402,316 C402,254 442,214 500,214 C558,214 598,254 598,316 "
       "L598,680 Z", "Back inset", fill="#5C2A3E", stroke=GOLD,
       strokeWidth=3.5, opacity=90)
# tufting buttons, dim
for i, (x, y) in enumerate([(455,290),(545,290),(500,340),(455,390),
                            (545,390),(500,440)]):
    d.shape("ellipse", f"Tuft {i+1}", x=x-7, y=y-7, width=14, height=14,
            fill="#7A3850", stroke=INK, strokeWidth=2.5, opacity=80)
# crest finials
for fx in (372, 628):
    d.shape("ellipse", f"Finial {fx}", x=fx-15, y=296, width=30, height=30,
            fill=GOLD_GRAD, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Crest orb", x=484, y=164, width=32, height=32,
        fill=GOLD_GRAD, stroke=INK, strokeWidth=4)
# armrests: rails on posts
d.path("M356,540 L440,540 L440,586 L356,586 Z", "Armrest L",
       fill=THRONE_GRAD, stroke=INK, strokeWidth=5, join="round")
d.path("M560,540 L644,540 L644,586 L560,586 Z", "Armrest R",
       fill=THRONE_GRAD, stroke=INK, strokeWidth=5, join="round")
d.path("M356,540 L440,540", "Armrest rail L", fill=NONE, stroke=GOLD,
       strokeWidth=4, cap="round")
d.path("M560,540 L644,540", "Armrest rail R", fill=NONE, stroke=GOLD,
       strokeWidth=4, cap="round")
for px in (366, 570):
    d.path(f"M{px},586 L{px},730 L{px+28},730 L{px+28},586 Z",
           f"Armrest post {px}", fill=THRONE_GRAD, stroke=INK,
           strokeWidth=5, join="round")
# seat cushion
d.shape("rectangle", "Seat cushion", x=386, y=566, width=228, height=72,
        fill="#6E3450", stroke=INK, strokeWidth=5, radius=18)
d.path("M398,586 C440,596 560,596 602,586", "Cushion seam", fill=NONE,
       stroke=GOLD, strokeWidth=2.5, opacity=60)
# throne base steps
d.path("M370,700 L630,700 L646,738 L354,738 Z", "Throne base",
       fill="#3A1C28", stroke=INK, strokeWidth=5, join="round")

# --- the mitigatrix: seated correctly ------------------------------------------
# gown: a composed bell over the seat front
d.path("M440,780 C436,720 438,650 460,606 C474,580 526,580 540,606 "
       "C562,650 564,720 560,780 Z", "Gown", fill=GOWN_GRAD,
       stroke=INK, strokeWidth=5, join="round")
d.shape("ellipse", "Gown light", x=462, y=620, width=76, height=80,
        fill="#8A9AB4", opacity=25, stroke=NONE)
# sash of office across the gown — broad enough to comfort
d.path("M468,610 L532,676 L518,690 L454,624 Z", "Sash", fill=GOLD_GRAD,
       stroke=INK, strokeWidth=3, join="round", opacity=92)
# collar
d.path("M478,596 L500,618 L522,596 L512,586 L500,598 L488,586 Z",
       "Collar", fill="#EFE6D2", stroke=INK, strokeWidth=3, join="round")
# sleeves bowed down-out to the armrests, hands soft on the rails
d.path("M462,616 C430,630 410,596 406,556", "Sleeve L", fill=NONE,
       stroke="#3E4C68", strokeWidth=27, cap="round")
d.path("M538,616 C570,630 590,596 594,556", "Sleeve R", fill=NONE,
       stroke="#3E4C68", strokeWidth=27, cap="round")
# gold cuff bands at the wrists
d.shape("ellipse", "Cuff L", x=390, y=550, width=24, height=18,
        fill=GOLD_GRAD, stroke=INK, strokeWidth=3)
d.shape("ellipse", "Cuff R", x=586, y=550, width=24, height=18,
        fill=GOLD_GRAD, stroke=INK, strokeWidth=3)
d.shape("ellipse", "Hand L", x=392, y=536, width=30, height=24,
        fill="#E4BE90", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Hand R", x=578, y=536, width=30, height=24,
        fill="#E4BE90", stroke=INK, strokeWidth=4)
# head
d.shape("ellipse", "Head", x=448, y=452, width=104, height=96,
        fill=SKIN_GRAD, stroke=INK, strokeWidth=5)
# heavy-lidded eyes: supervision complete on paper
d.shape("ellipse", "Eye L", x=472, y=502, width=13, height=15,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Eye R", x=515, y=502, width=13, height=15,
        fill=INK, stroke=NONE)
d.path("M468,500 C474,494 484,494 490,499", "Lid L", fill=NONE,
       stroke="#8A5E3C", strokeWidth=3.5, cap="round")
d.path("M511,499 C517,494 527,494 533,500", "Lid R", fill=NONE,
       stroke="#8A5E3C", strokeWidth=3.5, cap="round")
# the level mouth: neither protest nor consent
d.path("M484,532 C494,535 506,535 516,532", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=3.5, cap="round")
# hair at the temples
d.path("M448,470 C444,490 446,510 452,524", "Hair L", fill=NONE,
       stroke="#6E5638", strokeWidth=8, cap="round")
d.path("M552,470 C556,490 554,510 548,524", "Hair R", fill=NONE,
       stroke="#6E5638", strokeWidth=8, cap="round")

# --- the paper crown, worn level -------------------------------------------------
d.path("M456,466 L456,442 L472,458 L486,430 L500,456 L514,430 L528,458 "
       "L544,442 L544,466 Z", "Paper crown", fill=PAPER_GRAD,
       stroke=INK, strokeWidth=4, join="round")
# fold lines — paper is a supplies item
for fx in (472, 486, 500, 514, 528):
    d.path(f"M{fx},462 L{fx},452", f"Crown fold {fx}", fill=NONE,
           stroke="#A89878", strokeWidth=1.8, opacity=80)
# the tape seam where replacement pages meet
d.shape("rectangle", "Crown tape", x=494, y=446, width=14, height=10,
        fill="#D8C8A0", stroke=INK, strokeWidth=2, radius=2, opacity=90)

# --- the scepter, unpowered in the record's own wording --------------------------
# lying on the floor beside the throne, hatch open, batteries out
d.shape("ellipse", "Scepter shadow", x=640, y=746, width=150, height=18,
        fill="#120C18", opacity=50, stroke=NONE)
# shaft, angled gently down to the right
d.path("M624,712 L748,742 L744,756 L620,726 Z", "Scepter shaft",
       fill=GOLD_GRAD, stroke=INK, strokeWidth=4, join="round")
# orb head at the left end
d.shape("ellipse", "Scepter orb", x=600, y=692, width=38, height=38,
        fill=GOLD_GRAD, stroke=INK, strokeWidth=4)
d.path("M619,690 L619,674", "Orb stem", fill=NONE, stroke=INK,
       strokeWidth=4, cap="round")
d.path("M608,674 L630,674 M619,663 L619,685", "Orb cross", fill=NONE,
       stroke=GOLD, strokeWidth=4, cap="round")
# the dark socket where the light was specified
d.shape("ellipse", "Orb socket", x=612, y=704, width=12, height=12,
        fill="#241812", stroke=NONE)
# battery hatch, open on the shaft
d.path("M668,722 L694,728 L692,740 L666,734 Z", "Hatch opening",
       fill="#1C1210", stroke=INK, strokeWidth=3)
d.path("M694,728 L706,720 L708,732 L692,740 Z", "Hatch door",
       fill=GOLD_GRAD, stroke=INK, strokeWidth=3, join="round")
# the batteries, removed and set neatly beside
for i, (bx, by, rot) in enumerate([(700,762,-8),(726,754,12)]):
    w, h = 30, 13
    d.path(f"M{bx},{by} l{w*0.9},{rot*0.2} l0,{h} l-{w*0.9},{-rot*0.2} Z",
           f"Battery {i+1}", fill="#6E7884", stroke=INK, strokeWidth=3)
    d.shape("ellipse", f"Battery cap {i+1}",
            x=bx + w*0.82, y=by + rot*0.2 - 1, width=8, height=h + 2,
            fill="#C9A45C", stroke=INK, strokeWidth=2.5)

# --- the requests she reads: annotated, never signed ------------------------------
# a small stack of forms at floor left
d.shape("ellipse", "Forms shadow", x=238, y=742, width=120, height=16,
        fill="#120C18", opacity=50, stroke=NONE)
for i, (ox, oy) in enumerate([(0, 22), (6, 12), (-4, 2)]):
    d.path(f"M{252+ox},{706+oy} L{342+ox},{700+oy} L{348+ox},{726+oy} "
           f"L{256+ox},{732+oy} Z", f"Form {i+1}", fill=PAPER_GRAD,
           stroke=INK, strokeWidth=3.5, join="round")
# her annotation on the top form — the hand the audit permitted
d.path("M268,714 C282,710 296,714 308,710", "Annotation", fill=NONE,
       stroke="#5E4A38", strokeWidth=2.5, cap="round")
# the authorization line beneath it, unsigned
d.path("M314,722 L340,719", "Unsigned line", fill=NONE, stroke=INK,
       strokeWidth=2, cap="round", opacity=70)

# --- dust in the supervision -----------------------------------------------------
for i, (x, y, w) in enumerate([(300,340,5),(380,370,4),(560,350,5),(640,400,4),
                               (330,470,4),(600,470,5),(260,430,5),(500,390,4)]):
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#C4B4D4", opacity=30, stroke=NONE)

# --- captions ---------------------------------------------------------------------
d.text("MITIGATRIX PENDING", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#E4D8EA", justify="center")
r = d.text("DIRECTOR OF CRISIS RESOLUTION", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#B09CC0", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("314.mitigatrix-pending-V1R00")
