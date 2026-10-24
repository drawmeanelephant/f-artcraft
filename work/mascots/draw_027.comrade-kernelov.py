#!/usr/bin/env python3
"""Comrade Kernelov — mascot portrait V1R00.
A stern little enforcer patrolling a phosphor process table at 2:22 a.m.,
red banner raised in the cooling-fan breeze, kill-switch labeled
CTRL+ALT+Д (the Д is drawn — no tofu). 1000x1000.
Gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Comrade Kernelov — Mascot Portrait", 1000, 1000)

INK = "#1C1A16"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#0D0E0C"}, {"offset": 1, "color": "#060706"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#535B4E"}, {"offset": 0.7, "color": "#3B4338"},
    {"offset": 1, "color": "#21261F"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2C3028"}, {"offset": 1, "color": "#161913"}]}}
BOARD_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#212A26"}, {"offset": 1, "color": "#12161A"}]}}
BANNER_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#B83434"}, {"offset": 1, "color": "#7C1E1E"}]}}
COAT_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#6E7454"}, {"offset": 0.7, "color": "#4E543C"},
    {"offset": 1, "color": "#363B2A"}]}}
PHOS = "#8FD0A0"
PHOS_DIM = "#5E8E70"
RED = "#B83434"
GOLD = "#E0B84C"
FACE = "#D8CCB8"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#7E8878", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C9D2C2", strokeWidth=3, opacity=38)
for i, (x, y, w) in enumerate([(188,238,8),(806,236,7),(152,522,9),(844,542,8),
                               (254,770,7),(746,754,9),(132,390,6),(866,396,7),
                               (388,112,7),(616,110,8),(336,824,6),(664,822,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#454D42", opacity=55, stroke=NONE)

# --- clock at 2:22 a.m.: hands only, never digits ------------------------------
d.shape("ellipse", "Clock", x=176, y=130, width=88, height=88,
        fill="#2C322C", stroke="#8E9884", strokeWidth=5)
d.shape("ellipse", "Clock face", x=185, y=139, width=70, height=70,
        fill="#D4D0C0", stroke=NONE)
d.path("M220,174 L242,194", "Minute hand", fill=NONE, stroke="#38342C",
       strokeWidth=5, cap="round")
d.path("M220,174 L237,168", "Hour hand", fill=NONE, stroke="#38342C",
       strokeWidth=6, cap="round")
d.shape("ellipse", "Clock pin", x=215, y=169, width=10, height=10,
        fill="#38342C", stroke=NONE)

# --- floor: bottom segment closed on the disc's own arc ------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0F110C",
       strokeWidth=4, opacity=70)

# --- the process table: phosphor board, one row condemned ------------------------
d.shape("ellipse", "Board shadow", x=210, y=686, width=380, height=24,
        fill="#08080A", opacity=55, stroke=NONE)
d.path("M258,580 L286,580 L292,700 L252,700 Z", "Board leg L",
       fill="#2A2E28", stroke=INK, strokeWidth=5, join="round")
d.path("M506,580 L534,580 L540,700 L500,700 Z", "Board leg R",
       fill="#2A2E28", stroke=INK, strokeWidth=5, join="round")
d.shape("rectangle", "Board", x=196, y=246, width=384, height=336,
        fill=BOARD_GRAD, stroke=INK, strokeWidth=7, radius=12)
d.shape("rectangle", "Board header", x=208, y=258, width=360, height=34,
        fill="#2E3833", stroke=NONE, radius=6)
d.text("PROCESS TABLE", "Board title", x=220, y=280, size=14,
       font="Virelai Sans", color="#C4D4C4", justify="left")
# column heads + separators
d.text("PID", "Col PID", x=224, y=318, size=11, font="Virelai Sans",
       color=PHOS_DIM, justify="left")
d.text("NAME", "Col NAME", x=296, y=318, size=11, font="Virelai Sans",
       color=PHOS_DIM, justify="left")
d.text("STATE", "Col STATE", x=452, y=318, size=11, font="Virelai Sans",
       color=PHOS_DIM, justify="left")
for i, sx in enumerate([288, 444]):
    d.path(f"M{sx},302 L{sx},556", f"Col sep {i+1}", fill=NONE,
           stroke="#38423C", strokeWidth=2, opacity=80)
d.path("M212,326 L564,326", "Head rule", fill=NONE, stroke="#38423C",
       strokeWidth=2, opacity=80)
# rows: PIDs need digits — Source Sans 3 carries those strings
rows = [("001", "INIT", "RUN", PHOS), ("042", "SHELLD", "RUN", PHOS),
        ("117", "CRON", "SLEEP", PHOS_DIM), ("666", "BUREAUC", "ZOMBIE", None),
        ("233", "TTYD", "RUN", PHOS), ("404", "WATCHDOG", "SLEEP", PHOS_DIM)]
for i, (pid, name, state, col) in enumerate(rows):
    y = 352 + i * 37
    if col is None:
        # the condemned row: process equality's offender
        d.shape("rectangle", "Zombie band", x=212, y=y-20, width=352,
                height=28, fill=RED, opacity=28, stroke=NONE)
        col = "#F0A0A0"
    d.text(pid, f"PID {i+1}", x=224, y=y, size=13, font="Source Sans 3",
           color=col, justify="left")
    d.text(name, f"Name {i+1}", x=296, y=y, size=13,
           font="Virelai Sans", color=col, justify="left")
    d.text(state, f"State {i+1}", x=452, y=y, size=13,
           font="Virelai Sans", color=col, justify="left")
# cursor glow under the condemned row
d.shape("ellipse", "Zombie glow", x=360, y=452, width=80, height=24,
        fill=RED, opacity=15, stroke=NONE)

# --- the kill-switch pedestal, labeled CTRL+ALT+Д ---------------------------------
d.shape("ellipse", "Switch shadow", x=160, y=686, width=144, height=20,
        fill="#08080A", opacity=50, stroke=NONE)
d.path("M178,622 L282,622 L294,702 L166,702 Z", "Switch pedestal",
       fill="#3A3E36", stroke=INK, strokeWidth=5, join="round")
# label plate
d.shape("rectangle", "Switch label", x=178, y=636, width=104, height=22,
        fill="#D4CDB8", stroke=INK, strokeWidth=3, radius=3)
d.text("CTRL+ALT+", "Label latin", x=184, y=652, size=11,
       font="Virelai Sans", color="#3A3428", justify="left")
# the Д — hand-drawn: triangle set on a protruding ledge
d.path("M250,652 L274,652 L274,646 L268,646 L264,638 L260,638 L256,646 "
       "L250,646 Z",
       "Label De", fill="#3A3428", stroke=NONE)
# mushroom button, guarded and patient
d.shape("ellipse", "Button collar", x=218, y=596, width=26, height=10,
        fill="#2A2E26", stroke=INK, strokeWidth=3)
d.path("M218,600 C218,584 244,584 244,600 L244,604 L218,604 Z",
       "Kill button", fill=RED, stroke=INK, strokeWidth=4, join="round")
d.shape("ellipse", "Button hi", x=222, y=588, width=10, height=5,
        fill="#E88", opacity=70, stroke=NONE)

# --- the banner: hanging from its crossbar, tail lifted by the fan -----------------
d.shape("ellipse", "Pole foot", x=824, y=690, width=40, height=14,
        fill="#2A2E26", stroke=INK, strokeWidth=4)
d.path("M838,700 L838,212", "Banner pole", fill=NONE, stroke="#4E4A38",
       strokeWidth=10, cap="round")
d.shape("ellipse", "Pole finial", x=828, y=198, width=20, height=20,
        fill=GOLD, stroke=INK, strokeWidth=4)
d.path("M838,232 L636,232", "Crossbar", fill=NONE, stroke="#4E4A38",
       strokeWidth=7, cap="round")
d.shape("ellipse", "Crossbar cap", x=630, y=226, width=12, height=12,
        fill=GOLD, stroke=INK, strokeWidth=3)
# fabric: hangs from the bar, lower edge fluttering right toward the fan
d.path("M640,238 L836,238 L836,430 C812,448 796,420 776,442 "
       "C758,460 742,434 724,452 C708,466 694,444 678,458 "
       "C664,470 650,452 640,462 Z",
       "Banner", fill=BANNER_GRAD, stroke=INK, strokeWidth=6, join="round")
# fold shading
d.path("M700,238 C694,320 700,380 694,452 M764,238 C758,320 766,382 758,442",
       "Banner folds", fill=NONE, stroke="#5E1616", strokeWidth=4,
       opacity=50)
# the star of process equality
d.path("M738,296 L744,314 L762,314 L748,326 L753,344 L738,334 L723,344 "
       "L728,326 L714,314 L732,314 Z",
       "Banner star", fill=GOLD, stroke=INK, strokeWidth=3, join="round")
# gold fringe along the fluttering hem
for i, (x, y) in enumerate([(668,458),(702,456),(736,448),(770,436),
                             (804,436)]):
    d.path(f"M{x},{y} L{x},{y+14}", f"Fringe {i+1}", fill=NONE,
           stroke=GOLD, strokeWidth=3, cap="round", opacity=80)

# --- the cooling fan: the breeze made visible -------------------------------------
d.shape("rectangle", "Fan frame", x=740, y=634, width=76, height=64,
        fill="#2C3028", stroke=INK, strokeWidth=5, radius=8)
d.shape("ellipse", "Fan well", x=748, y=640, width=60, height=52,
        fill="#181C16", stroke=NONE)
# four blades mid-spin
d.path("M778,666 C778,654 792,652 794,660 C796,668 786,670 778,666 "
       "M778,666 C766,666 764,652 772,650 C780,648 782,658 778,666 "
       "M778,666 C778,678 764,680 762,672 C760,664 770,662 778,666 "
       "M778,666 C790,666 792,680 784,682 C776,684 774,674 778,666 Z",
       "Fan blades", fill="#5A624F", stroke=INK, strokeWidth=3,
       join="round")
d.shape("ellipse", "Fan hub", x=774, y=662, width=8, height=8,
        fill="#3E4438", stroke=INK, strokeWidth=2)
# rising breeze lines, curling left into the banner tail
d.path("M760,630 C740,600 736,560 752,520", "Breeze 1", fill=NONE,
       stroke="#A9C0B0", strokeWidth=3, cap="round", dash=[2, 9],
       opacity=55)
d.path("M788,630 C772,596 768,540 784,492", "Breeze 2", fill=NONE,
       stroke="#A9C0B0", strokeWidth=3, cap="round", dash=[2, 9],
       opacity=55)

# --- Comrade Kernelov: mid-patrol, pointing at the condemned row -------------------
d.shape("ellipse", "Kern shadow", x=590, y=686, width=190, height=22,
        fill="#08080A", opacity=50, stroke=NONE)
# marching boots under the coat hem
d.path("M628,676 L660,676 L664,700 L622,700 Z", "Boot back",
       fill="#26241E", stroke=INK, strokeWidth=4, join="round")
d.path("M690,672 L734,672 L750,694 L692,700 Z", "Boot forward",
       fill="#26241E", stroke=INK, strokeWidth=4, join="round")
# the greatcoat: bell silhouette, belted
d.path("M656,500 C632,560 624,630 626,682 C664,694 730,694 764,682 "
       "C766,630 758,560 734,500 C710,486 680,486 656,500 Z",
       "Greatcoat", fill=COAT_GRAD, stroke=INK, strokeWidth=6,
       join="round")
# belt + buckle
d.path("M630,594 C668,604 722,604 760,594", "Belt", fill=NONE,
       stroke="#2C2A20", strokeWidth=12, opacity=90)
d.shape("rectangle", "Buckle", x=686, y=588, width=20, height=14,
        fill=GOLD, stroke=INK, strokeWidth=3, radius=2)
# collar + shoulder boards
d.path("M656,500 C680,486 710,486 734,500 L726,520 C706,510 684,510 664,520 Z",
       "Collar", fill="#3A3F2C", stroke=INK, strokeWidth=4, join="round")
d.shape("ellipse", "Board L", x=632, y=502, width=30, height=12,
        fill=RED, stroke=INK, strokeWidth=3)
d.shape("ellipse", "Board R", x=728, y=502, width=30, height=12,
        fill=RED, stroke=INK, strokeWidth=3)
# head: pale, watchful
d.shape("ellipse", "Head", x=652, y=404, width=88, height=88,
        fill=FACE, stroke=INK, strokeWidth=6)
# peaked cap with red star
d.path("M650,424 C650,392 668,372 696,372 C724,372 742,392 742,424 "
       "C724,414 668,414 650,424 Z",
       "Cap crown", fill="#4A5038", stroke=INK, strokeWidth=5,
       join="round")
d.path("M642,424 C664,410 728,410 750,424 L742,438 C720,428 672,428 650,438 Z",
       "Cap brim", fill="#2E3224", stroke=INK, strokeWidth=4, join="round")
d.path("M696,384 L699,393 L708,393 L701,399 L704,408 L696,402 L688,408 "
       "L691,399 L684,393 L693,393 Z",
       "Cap star", fill=RED, stroke=INK, strokeWidth=2, join="round")
# the stare: heavy flat eyes, carved for vigilance
d.path("M664,446 L690,446 M702,446 L728,446", "Eyes", fill=NONE,
       stroke=INK, strokeWidth=6, cap="round")
d.path("M660,434 L692,430 M700,430 L732,434", "Brow", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round", opacity=80)
# the moustache of the state
d.path("M674,466 C682,460 692,462 696,468 C700,462 710,460 718,466 "
       "C714,476 702,478 696,474 C690,478 678,476 674,466 Z",
       "Moustache", fill="#3A3028", stroke=INK, strokeWidth=2,
       join="round")
# the pointing arm: indictment extended toward the ZOMBIE row
d.path("M652,530 C620,514 596,494 574,470", "Arm point", fill=NONE,
       stroke="#4E543C", strokeWidth=17, cap="round")
d.shape("ellipse", "Pointing hand", x=556, y=452, width=26, height=20,
        fill=FACE, stroke=INK, strokeWidth=4)
d.path("M560,458 L542,450", "Index finger", fill=NONE, stroke=INK,
       strokeWidth=6, cap="round")
# the other arm, swung behind in march
d.path("M752,540 C772,560 778,586 772,608", "Arm back", fill=NONE,
       stroke="#4E543C", strokeWidth=16, cap="round")

# --- captions ----------------------------------------------------------------------
d.text("COMRADE KERNELOV", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#E4E4D2", justify="center")
r = d.text("STATE UI ENFORCER", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#A8B098", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("027.comrade-kernelov-V1R00")
