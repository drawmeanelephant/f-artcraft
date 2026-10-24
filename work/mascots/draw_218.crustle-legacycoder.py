#!/usr/bin/env python3
"""Crustle the Legacy Coder — mascot portrait V1R00.
A Roxbury Russet apple compiling harvest records on an ancient computer
in a spectral russet orchard. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Crustle the Legacy Coder — Mascot Portrait", 1000, 1000)

INK = "#2E1E12"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#16100B"}, {"offset": 1, "color": "#080503"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#7A5A3C"}, {"offset": 0.7, "color": "#4A3524"},
    {"offset": 1, "color": "#221711"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3A2A1C"}, {"offset": 1, "color": "#160F08"}]}}
APPLE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#C08A50"}, {"offset": 0.68, "color": "#8A5A32"},
    {"offset": 1, "color": "#57351D"}]}}
CRT_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#D8C8A4"}, {"offset": 1, "color": "#94805E"}]}}
SCR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2E2412"}, {"offset": 1, "color": "#171008"}]}}
DESK_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5A4030"}, {"offset": 1, "color": "#2E1D10"}]}}
KEY_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#C4B490"}, {"offset": 1, "color": "#84724E"}]}}
PAPER_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#EDE4CC"}, {"offset": 1, "color": "#C0B08C"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#7A6246", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E4D6BC", strokeWidth=3, opacity=50)
for i, (x, y, w) in enumerate([(193,233,8),(801,230,7),(157,524,9),(837,544,8),
                               (247,766,7),(753,749,9),(133,393,6),(864,391,7),
                               (391,113,7),(613,110,8),(333,823,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#5E4630", opacity=45, stroke=NONE)

# --- gnarled russet orchard: twisted boughs at the edges -------------------------
d.path("M124,700 C112,560 152,470 130,382 C114,318 152,258 184,222",
       "Gnarled trunk L", fill=NONE, stroke="#1E130C", strokeWidth=22,
       cap="round", opacity=85)
d.path("M150,380 C200,340 230,300 236,250", "Bough L1", fill=NONE,
       stroke="#1E130C", strokeWidth=10, cap="round", opacity=85)
d.path("M140,500 C190,480 220,450 226,410", "Bough L2", fill=NONE,
       stroke="#1E130C", strokeWidth=9, cap="round", opacity=80)
d.path("M876,700 C888,570 848,480 870,392 C886,328 848,262 812,226",
       "Gnarled trunk R", fill=NONE, stroke="#1E130C", strokeWidth=22,
       cap="round", opacity=85)
d.path("M852,400 C805,365 780,330 775,285", "Bough R1", fill=NONE,
       stroke="#1E130C", strokeWidth=10, cap="round", opacity=85)
for i, (x, y) in enumerate([(230,255),(222,415),(778,290),(248,470)]):
    d.shape("ellipse", f"Russet fruit {i+1}", x=x, y=y, width=20, height=24,
            fill="#6E4526", opacity=80, stroke=NONE)

# --- floor ---------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0C0805",
       strokeWidth=4, opacity=70)

# --- the desk -------------------------------------------------------------------
d.shape("ellipse", "Desk shadow", x=430, y=672, width=420, height=28,
        fill="#060302", opacity=55, stroke=NONE)
d.shape("rectangle", "Desk top", x=380, y=566, width=400, height=24,
        fill=DESK_GRAD, stroke=INK, strokeWidth=5, radius=5)
d.shape("rectangle", "Desk leg L", x=405, y=590, width=26, height=88,
        fill=DESK_GRAD, stroke=INK, strokeWidth=4)
d.shape("rectangle", "Desk leg R", x=730, y=590, width=26, height=88,
        fill=DESK_GRAD, stroke=INK, strokeWidth=4)

# --- the ancient computer: a great beige CRT -------------------------------------
# amber glow washing the desk and the coder's face
d.shape("ellipse", "Screen glow", x=500, y=330, width=330, height=240,
        fill="#E8B44A", opacity=10, stroke=NONE)
d.shape("rectangle", "CRT case", x=520, y=298, width=250, height=220,
        fill=CRT_GRAD, stroke=INK, strokeWidth=6, radius=12)
d.shape("rectangle", "CRT screen", x=540, y=318, width=178, height=140,
        fill=SCR_GRAD, stroke="#241A0C", strokeWidth=4, radius=8)
# phosphor readout
d.text("HARVEST.BAT", "Screen title", x=554, y=344, size=13,
       font="Virelai Sans", color="#E8B44A", justify="left")
for i, w in enumerate([140, 96, 128, 60]):
    d.shape("rectangle", f"Code line {i+1}", x=554, y=360+i*16, width=w,
            height=7, fill="#C89A3E", opacity=65, stroke=NONE, radius=2)
d.text("0 ERRORS", "Screen status", x=554, y=436, size=12,
       font="Virelai Sans", color="#8AE078", justify="left")
d.shape("rectangle", "Cursor", x=626, y=426, width=12, height=14,
        fill="#E8B44A", opacity=85, stroke=NONE)
# drive slot, badge, vents
d.shape("rectangle", "Drive slot", x=738, y=330, width=20, height=70,
        fill="#4A3C28", stroke=INK, strokeWidth=3, radius=3)
for i in range(3):
    d.path(f"M738,{420+i*12} L758,{420+i*12}", f"Vent {i+1}", fill=NONE,
           stroke="#6E5C3C", strokeWidth=4, cap="round", opacity=70)
d.shape("ellipse", "Power lamp", x=742, y=480, width=14, height=14,
        fill="#8AE078", stroke=INK, strokeWidth=2)
d.path("M560,298 L540,280 M735,298 L755,282", "Case scuffs", fill=NONE,
       stroke="#B09A72", strokeWidth=3, cap="round", opacity=60)
# cobweb in the top corner — this OS has never been updated
d.path("M520,298 C545,305 560,320 565,345 C545,330 528,318 520,318 Z",
       "Cobweb", fill=NONE, stroke="#B8C4CC", strokeWidth=2, opacity=40)
# keyboard in front
d.shape("rectangle", "Keyboard", x=536, y=530, width=190, height=34,
        fill=KEY_GRAD, stroke=INK, strokeWidth=4, radius=6)
for r_i, row_y in enumerate([538, 548]):
    for k in range(8):
        d.shape("rectangle", f"Key {r_i+1}-{k+1}", x=546+k*22, y=row_y,
                width=16, height=6, fill="#6E5C3C", opacity=70,
                stroke=NONE, radius=2)
# a floppy disk resting by the keyboard
d.path("M748,534 L792,534 L792,578 L748,578 Z", "Floppy", fill="#3A3230",
       stroke=INK, strokeWidth=4, join="round")
d.shape("rectangle", "Floppy shutter", x=756, y=534, width=20, height=16,
        fill="#8A8E96", stroke=INK, strokeWidth=3)
d.shape("rectangle", "Floppy label", x=754, y=560, width=32, height=14,
        fill="#D8CCAC", stroke=INK, strokeWidth=2)

# --- fanfold printout spilling off the desk's left edge ---------------------------
d.path("M430,540 L492,540 L492,570 L430,570 Z", "Printout sheet",
       fill=PAPER_GRAD, stroke=INK, strokeWidth=3, join="round")
d.path("M430,570 L470,570 L478,688 L438,688 Z", "Printout tail",
       fill=PAPER_GRAD, stroke=INK, strokeWidth=4, join="round")
for j in range(4):
    d.path(f"M436,{590+j*20} L468,{590+j*20}", f"Print line {j+1}",
           fill=NONE, stroke="#8A7A58", strokeWidth=3, opacity=70)
for j in range(6):
    d.shape("ellipse", f"Perf L {j+1}", x=432, y=582+j*17, width=4, height=4,
            fill="#6E5C3C", opacity=60, stroke=NONE)
    d.shape("ellipse", f"Perf R {j+1}", x=466, y=582+j*17, width=4, height=4,
            fill="#6E5C3C", opacity=60, stroke=NONE)

# --- Crustle: a Roxbury Russet, amber-lit ---------------------------------------
d.shape("ellipse", "Apple shadow", x=200, y=668, width=210, height=28,
        fill="#060302", opacity=55, stroke=NONE)
d.shape("ellipse", "Foot L", x=228, y=650, width=48, height=26,
        fill="#4A2C16", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Foot R", x=326, y=650, width=48, height=26,
        fill="#4A2C16", stroke=INK, strokeWidth=4)
# russet body — rougher, matte, patched
d.path("M300,452 C318,436 356,432 384,458 C418,488 426,548 404,604 "
       "C390,642 362,664 338,656 C324,650 314,654 300,654 "
       "C286,654 276,650 262,656 C240,664 212,642 198,604 "
       "C176,548 184,488 218,458 C246,432 282,436 300,452 Z",
       "Russet body", fill=APPLE_GRAD, stroke=INK, strokeWidth=6)
# russeting: matte patches + rough speckle
d.shape("ellipse", "Russet patch 1", x=206, y=486, width=70, height=60,
        fill="#D8A868", opacity=30, stroke=NONE)
d.shape("ellipse", "Russet patch 2", x=340, y=560, width=60, height=70,
        fill="#6E4423", opacity=35, stroke=NONE)
for i, (x, y) in enumerate([(242,540),(276,566),(328,548),(360,584),(250,610),(320,620),(290,500)]):
    d.shape("ellipse", f"Speckle {i+1}", x=x, y=y, width=6, height=4,
            fill="#D8B87A", opacity=45, stroke=NONE)
# stem + leaf
d.path("M300,448 C302,428 296,416 288,406", "Stem", fill=NONE,
       stroke="#3A2414", strokeWidth=7, cap="round")
d.path("M292,414 C274,406 268,390 276,378 C294,384 302,398 292,414 Z",
       "Stem leaf", fill="#5A6638", stroke=INK, strokeWidth=3, join="round")
# amber screen-light on the face
d.shape("ellipse", "Face glow", x=300, y=486, width=90, height=80,
        fill="#E8B44A", opacity=16, stroke=NONE)
# weary eyes behind little round glasses, glancing at the terminal
for cx in (262, 332):
    d.shape("ellipse", f"Lens {cx}", x=cx-22, y=502, width=44, height=44,
            fill="#F5E8C8", opacity=28, stroke=INK, strokeWidth=4)
d.path("M284,522 L310,522", "Bridge", fill=NONE, stroke=INK, strokeWidth=4)
d.path("M240,516 C226,510 216,504 210,496", "Temple L", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.path("M354,516 C368,510 378,504 384,496", "Temple R", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.path("M252,522 C258,528 268,528 274,522", "Eye L", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
d.path("M322,522 C328,528 338,528 344,522", "Eye R", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
# the secretive half-smile of an OS that never fails
d.path("M268,576 C284,588 312,588 328,576", "Smile", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
# arms: right reaches the keyboard, left rests on the desk edge
d.path("M398,536 C430,540 462,548 490,552", "Arm R", fill=NONE,
       stroke="#8A5A32", strokeWidth=18, cap="round")
d.path("M204,548 C190,566 192,588 206,602", "Arm L", fill=NONE,
       stroke="#8A5A32", strokeWidth=18, cap="round")
# fingertips hovering over the keys
for i, (x, y) in enumerate([(518,548),(528,552),(538,556)]):
    d.path(f"M{x},{y} l6,4", f"Key tap {i+1}", fill=NONE, stroke="#8A5A32",
           strokeWidth=6, cap="round")

# --- captions ------------------------------------------------------------------
d.text("CRUSTLE THE LEGACY CODER", "Name", x=500, y=930, size=42,
       font="Virelai Sans", color="#E8DCC4", justify="center")
r = d.text("LEGACY COMPILER", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#B89468", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("218.crustle-legacycoder-V1R00")
