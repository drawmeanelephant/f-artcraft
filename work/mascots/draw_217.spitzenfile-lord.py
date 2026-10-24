#!/usr/bin/env python3
"""Lord Spitzenfile — mascot portrait V1R00.
An Esopus Spitzenberg aristocrat sealing a metadata vault-box with a wax
cipher on a spectral orchard estate. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Lord Spitzenfile — Mascot Portrait", 1000, 1000)

INK = "#331C18"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1C1014"}, {"offset": 1, "color": "#0B0508"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#6E4A44"}, {"offset": 0.7, "color": "#452E30"},
    {"offset": 1, "color": "#211318"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3A262A"}, {"offset": 1, "color": "#170D10"}]}}
APPLE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#D85838"}, {"offset": 0.68, "color": "#A02E1E"},
    {"offset": 1, "color": "#5E1A12"}]}}
BOX_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4A3E52"}, {"offset": 1, "color": "#241C2E"}]}}
BRASS_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E0B85E"}, {"offset": 1, "color": "#96702A"}]}}
WOOD_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7A5232"}, {"offset": 1, "color": "#4A2E1A"}]}}
WAX_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#C23A30"}, {"offset": 0.75, "color": "#8E1F1C"},
    {"offset": 1, "color": "#5A0F12"}]}}
CLOTH_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7A2E38"}, {"offset": 1, "color": "#3E141C"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#7A5A56", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8D8CC", strokeWidth=3, opacity=50)
for i, (x, y, w) in enumerate([(193,233,8),(801,230,7),(157,524,9),(837,544,8),
                               (247,766,7),(753,749,9),(133,393,6),(864,391,7),
                               (391,113,7),(613,110,8),(333,823,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#5A3E3C", opacity=45, stroke=NONE)

# --- the estate: fluted columns + a spectral arch -------------------------------
for side, x in (("L", 152), ("R", 788)):
    d.shape("rectangle", f"Column {side}", x=x, y=250, width=52, height=430,
            fill="#2A1A1E", stroke=NONE, opacity=80)
    d.shape("rectangle", f"Column capital {side}", x=x-8, y=232, width=68,
            height=26, fill="#33211F", stroke=NONE, opacity=85)
    d.shape("rectangle", f"Column base {side}", x=x-8, y=672, width=68,
            height=22, fill="#33211F", stroke=NONE, opacity=85)
    for j in range(3):
        d.path(f"M{x+12+j*14},262 L{x+12+j*14},668",
               f"Flute {side} {j+1}", fill=NONE, stroke="#1E1214",
               strokeWidth=4, opacity=60)
# arching bough between the capitals
d.path("M178,246 C310,150 690,150 822,246", "Estate bough", fill=NONE,
       stroke="#261819", strokeWidth=16, cap="round", opacity=85)
for i, (x, y, r) in enumerate([(300,196,-30),(430,172,-12),(570,172,12),(700,196,30)]):
    a = math.radians(r)
    d.path(f"M{x},{y} C{x-14*math.cos(a):.0f},{y-16} {x+8},{y-30} {x+22*math.cos(a):.0f},{y-26} "
           f"C{x+14},{y-10} {x+6},{y-2} {x},{y} Z",
           f"Bough leaf {i+1}", fill="#3A2A22", stroke=NONE, opacity=85)

# --- floor ---------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0D0709",
       strokeWidth=4, opacity=70)

# --- the vault-box on its draped pedestal ---------------------------------------
d.shape("ellipse", "Pedestal shadow", x=600, y=672, width=220, height=26,
        fill="#0A0406", opacity=55, stroke=NONE)
# draped plinth
d.path("M640,560 L780,560 L800,676 L620,676 Z", "Draped plinth",
       fill=CLOTH_GRAD, stroke=INK, strokeWidth=5, join="round")
d.path("M640,560 L620,676 M780,560 L800,676 M710,560 L712,676",
       "Drape folds", fill=NONE, stroke="#2A0E14", strokeWidth=3, opacity=60)
# the strongbox itself
d.shape("rectangle", "Vault box", x=636, y=428, width=148, height=132,
        fill=BOX_GRAD, stroke=INK, strokeWidth=5, radius=8)
d.shape("rectangle", "Box lid", x=628, y=408, width=164, height=34,
        fill=BOX_GRAD, stroke=INK, strokeWidth=5, radius=7)
# banding + corner studs
for x in (648, 772):
    d.path(f"M{x},444 L{x},556", "Box band", fill=NONE, stroke="#171020",
           strokeWidth=8, opacity=70)
for i, (x, y) in enumerate([(646,452),(766,452),(646,540),(766,540)]):
    d.shape("ellipse", f"Stud {i+1}", x=x-5, y=y-5, width=10, height=10,
            fill="#8A7A96", stroke=INK, strokeWidth=2)
# clasp tongue under the lid
d.path("M700,442 L720,442 L718,470 L702,470 Z", "Clasp", fill=BRASS_GRAD,
       stroke=INK, strokeWidth=3, join="round")
# the wax cipher: scalloped seal pressed over the clasp
for i in range(10):
    a = math.radians(i * 36)
    cx, cy = 710 + 34*math.cos(a), 496 + 34*math.sin(a)
    d.shape("ellipse", f"Wax lobe {i+1}", x=cx-9, y=cy-9, width=18, height=18,
            fill=WAX_GRAD, stroke=NONE)
d.shape("ellipse", "Wax seal", x=672, y=458, width=76, height=76,
        fill=WAX_GRAD, stroke=INK, strokeWidth=4)
# the cipher: an unsolvable monogram of S and ?
d.text("S", "Cipher S", x=710, y=512, size=34, font="Virelai Sans",
       color="#5A0F12", justify="center")
d.path("M690,478 c10,-9 30,-9 38,2", "Cipher flourish", fill=NONE,
       stroke="#5A0F12", strokeWidth=3, cap="round", opacity=80)
# wax drips down the box face
for i, (x, ln) in enumerate([(676,26),(742,18)]):
    d.path(f"M{x},470 C{x-3},{470+ln/2} {x+3},{470+ln/2} {x},{470+ln}",
           f"Wax drip {i+1}", fill=NONE, stroke="#8E1F1C", strokeWidth=7,
           cap="round")

# --- Lord Spitzenfile: an Esopus Spitzenberg apple ------------------------------
d.shape("ellipse", "Apple shadow", x=310, y=668, width=210, height=28,
        fill="#0A0406", opacity=55, stroke=NONE)
d.shape("ellipse", "Foot L", x=338, y=650, width=48, height=26,
        fill="#4A1410", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Foot R", x=436, y=650, width=48, height=26,
        fill="#4A1410", stroke=INK, strokeWidth=4)
# apple body
d.path("M410,452 C428,436 466,432 494,458 C528,488 536,548 514,604 "
       "C500,642 472,664 448,656 C434,650 424,654 410,654 "
       "C396,654 386,650 372,656 C350,664 322,642 308,604 "
       "C286,548 294,488 328,458 C356,432 392,436 410,452 Z",
       "Spitzenberg body", fill=APPLE_GRAD, stroke=INK, strokeWidth=6)
# golden blush + lenticel freckles
d.shape("ellipse", "Cheek blush", x=318, y=490, width=56, height=84,
        fill="#E88A4A", opacity=30, stroke=NONE)
for i, (x, y) in enumerate([(352,540),(386,566),(438,548),(470,584),(360,610),(430,620)]):
    d.shape("ellipse", f"Lenticel {i+1}", x=x, y=y, width=6, height=4,
            fill="#E8B87A", opacity=55, stroke=NONE)
# stem + leaf
d.path("M410,448 C412,428 406,416 398,406", "Stem", fill=NONE,
       stroke="#3A2418", strokeWidth=7, cap="round")
d.path("M402,414 C384,406 378,390 386,378 C404,384 412,398 402,414 Z",
       "Stem leaf", fill="#4A5A34", stroke=INK, strokeWidth=3, join="round")
# high collar / cravat at the crown
d.path("M352,470 C380,448 440,448 468,470 C456,486 432,492 410,492 "
       "C388,492 364,486 352,470 Z", "Cravat", fill="#EDE4D2",
       stroke=INK, strokeWidth=4, join="round", opacity=95)
d.path("M398,486 C404,502 416,502 422,486 L418,540 C414,552 406,552 402,540 Z",
       "Cravat fall", fill="#E0D4BE", stroke=INK, strokeWidth=3, join="round")
# enigmatic face: one raised brow, monocle over the right eye, half-smile
d.path("M330,506 L362,500", "Brow L", fill=NONE, stroke=INK,
       strokeWidth=6, cap="round")
d.shape("ellipse", "Eye L", x=336, y=514, width=20, height=13,
        fill="#F5ECD8", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Pupil L", x=344, y=518, width=7, height=7,
        fill=INK, stroke=NONE)
# monocle: lens, glint, chain down to the cravat
d.shape("ellipse", "Monocle", x=436, y=498, width=56, height=56,
        fill="#D8E4F0", opacity=35, stroke="#C89E46", strokeWidth=6)
d.shape("ellipse", "Eye R", x=454, y=518, width=20, height=13,
        fill="#F5ECD8", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Pupil R", x=462, y=522, width=7, height=7,
        fill=INK, stroke=NONE)
d.path("M446,510 C452,504 462,503 468,507", "Monocle glint", fill=NONE,
       stroke="#FFFFFF", strokeWidth=3, cap="round", opacity=70)
d.path("M464,554 C470,580 452,596 430,600", "Monocle chain", fill=NONE,
       stroke="#C89E46", strokeWidth=3, cap="round", opacity=85)
d.path("M362,560 C378,572 402,574 416,562", "Half smile", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
# left arm gesturing cryptically toward the viewer
d.path("M312,540 C280,548 264,574 268,600", "Arm L", fill=NONE,
       stroke="#A02E1E", strokeWidth=18, cap="round")
# right arm raised, holding the seal stamp over the box
d.path("M510,520 C552,508 580,486 594,452", "Arm R", fill=NONE,
       stroke="#A02E1E", strokeWidth=18, cap="round")
# the seal stamp: wooden handle + brass face, fresh from the wax
d.path("M594,452 L620,418", "Stamp handle", fill=NONE, stroke="#6E4828",
       strokeWidth=12, cap="round")
d.shape("ellipse", "Stamp grip", x=580, y=440, width=30, height=24,
        fill=WOOD_GRAD, stroke=INK, strokeWidth=3)
d.path("M612,428 L636,396 L650,410 L626,442 Z", "Stamp neck",
       fill=WOOD_GRAD, stroke=INK, strokeWidth=3, join="round")
d.shape("ellipse", "Stamp face", x=634, y=384, width=34, height=22,
        fill=BRASS_GRAD, stroke=INK, strokeWidth=3)
d.shape("ellipse", "Stamp wax residue", x=640, y=392, width=22, height=12,
        fill="#8E1F1C", opacity=70, stroke=NONE)

# --- captions ------------------------------------------------------------------
d.text("LORD SPITZENFILE", "Name", x=500, y=930, size=56, font="Virelai Sans",
       color="#EADFD2", justify="center")
r = d.text("ENIGMATIC CURATOR", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#B89888", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("217.spitzenfile-lord-V1R00")
