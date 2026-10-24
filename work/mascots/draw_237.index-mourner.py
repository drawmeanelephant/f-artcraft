#!/usr/bin/env python3
"""Index Mourner — mascot portrait V1R00.
A hooded mourner holding a 404 folded like a memorial flag beside a standing
index of broken links. 1000x1000. Gradients + translucent shading, never
flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Index Mourner — Mascot Portrait", 1000, 1000)

INK = "#22202C"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#151E24"}, {"offset": 1, "color": "#090E12"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#5E7472"}, {"offset": 0.7, "color": "#3C514E"},
    {"offset": 1, "color": "#1C2828"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2C3C3C"}, {"offset": 1, "color": "#131C1C"}]}}
ROBE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#767F94"}, {"offset": 0.72, "color": "#525A70"},
    {"offset": 1, "color": "#353B4C"}]}}
HOOD_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#454C62"}, {"offset": 1, "color": "#272C3C"}]}}
BOARD_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4E5E64"}, {"offset": 1, "color": "#2B383C"}]}}
FLAG = "#E9DDC2"
DEAD = "#C4706A"
LIVE = "#A9BCBC"

# --- backdrop + plate ------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#72908C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C4DAD4", strokeWidth=3, opacity=50)
for i, (x, y, w) in enumerate([(188,230,8),(808,232,7),(158,518,9),(836,546,8),
                               (248,768,7),(752,746,9),(134,392,6),(864,394,7),
                               (394,112,7),(612,108,8),(334,820,6),(668,824,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#4E6662", opacity=45, stroke=NONE)

# --- floor: bottom segment closed on the disc's own arc ---------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0D1515",
       strokeWidth=4, opacity=70)

# --- the index of broken links: a standing board on a plinth -----------------------
d.shape("ellipse", "Board shadow", x=600, y=688, width=220, height=22,
        fill="#0A1010", opacity=45, stroke=NONE)
d.shape("rectangle", "Plinth", x=628, y=640, width=164, height=52,
        fill="#39474B", stroke=INK, strokeWidth=5, radius=5)
d.shape("rectangle", "Board", x=596, y=270, width=228, height=380,
        fill=BOARD_GRAD, stroke=INK, strokeWidth=6, radius=10)
# header
d.shape("rectangle", "Board header", x=614, y=288, width=192, height=34,
        fill="#1E2A2E", stroke=INK, strokeWidth=4, radius=5)
d.text("INDEX", "Board title", x=710, y=311, size=16, font="Virelai Sans",
       color="#A9BCBC", justify="center")
# rows: three live links, three dead — the dead keep their legible pointing
rows = [(342, True), (386, False), (430, False), (474, True),
        (518, False), (562, True)]
for i, (ry, alive) in enumerate(rows):
    col = LIVE if alive else "#5F7172"
    d.shape("ellipse", f"Bullet {i+1}", x=618, y=ry-5, width=10, height=10,
            fill=col, stroke=NONE, opacity=95 if alive else 70)
    d.path(f"M638,{ry} L{762 + (i%3)*14},{ry}", f"Link {i+1}", fill=NONE,
           stroke=col, strokeWidth=7, cap="round",
           opacity=95 if alive else 65)
    if not alive:
        # struck through — dead but still pointing
        d.path(f"M634,{ry} L{766 + (i%3)*14},{ry}", f"Strike {i+1}",
               fill=NONE, stroke=DEAD, strokeWidth=3, cap="round",
               opacity=90)
        d.path(f"M{772 + (i%3)*14},{ry-8} L{784 + (i%3)*14},{ry+8} "
               f"M{784 + (i%3)*14},{ry-8} L{772 + (i%3)*14},{ry+8}",
               f"Dead X {i+1}", fill=NONE, stroke=DEAD, strokeWidth=3,
               cap="round", opacity=85)
# dust on the top edge — the only maintenance it performs is legibility
d.shape("ellipse", "Board dust", x=630, y=266, width=160, height=14,
        fill="#8FA3A0", opacity=18, stroke=NONE)

# --- the Mourner ------------------------------------------------------------------
d.shape("ellipse", "Mourner shadow", x=310, y=676, width=290, height=28,
        fill="#0A1010", opacity=45, stroke=NONE)
# robe: a bell widening to the floor
d.path("M448,414 C540,414 588,505 598,650 C598,684 560,700 448,700 "
       "C336,700 298,684 298,650 C308,505 356,414 448,414 Z",
       "Robe", fill=ROBE_GRAD, stroke=INK, strokeWidth=6)
# robe folds
d.path("M380,480 C370,540 366,600 370,660 M448,500 C448,560 448,620 448,672 "
       "M516,480 C526,540 530,600 526,660", "Robe folds", fill=NONE,
       stroke="#3C4256", strokeWidth=4, cap="round", opacity=60)
d.shape("ellipse", "Robe hi", x=360, y=460, width=90, height=46,
        fill="#FFFFFF", opacity=10, stroke=NONE)

# hood: deep dome, face in shadow inside
d.path("M448,282 C522,282 570,332 570,398 C570,448 520,470 448,470 "
       "C376,470 326,448 326,398 C326,332 374,282 448,282 Z",
       "Hood", fill=HOOD_GRAD, stroke=INK, strokeWidth=6)
# face opening
d.path("M448,326 C500,326 534,358 534,402 C534,436 500,452 448,452 "
       "C396,452 362,436 362,402 C362,358 396,326 448,326 Z",
       "Face opening", fill="#1A1622", stroke=INK, strokeWidth=4)
# downcast eyes: pale half-moons under hood shadow
d.path("M404,404 C412,412 424,412 432,404", "Eye L", fill=NONE,
       stroke="#C9D4D2", strokeWidth=5, cap="round")
d.path("M464,404 C472,412 484,412 492,404", "Eye R", fill=NONE,
       stroke="#C9D4D2", strokeWidth=5, cap="round")
# one tear, kept accurate
d.path("M428,416 C426,426 425,432 426,438", "Tear", fill=NONE,
       stroke="#9FC4CC", strokeWidth=4, cap="round", opacity=80)
# small mouth, set level
d.path("M440,432 C446,434 452,434 458,432", "Mouth", fill=NONE,
       stroke="#8A97A0", strokeWidth=4, cap="round", opacity=80)

# --- the folded flag: a 404 creased lengthwise, held to the chest -------------------
# triangle pointing down, top edge across the arms
d.path("M352,486 L544,486 L448,602 Z", "Flag", fill=FLAG,
       stroke=INK, strokeWidth=5, join="round")
# fold creases: the lengthwise crease plus the flag-fold diagonals
d.path("M448,486 L448,602", "Center crease", fill=NONE, stroke="#B4A488",
       strokeWidth=3, opacity=80)
d.path("M352,486 L448,546 L544,486", "Fold creases", fill=NONE,
       stroke="#B4A488", strokeWidth=3, opacity=60)
# a worn star field at the left corner of the fold
d.path("M370,498 L402,498 L386,516 Z", "Fold facet", fill="#D8CBAA",
       stroke=INK, strokeWidth=3, join="round", opacity=90)
# the dead error itself — digits in Source Sans 3 (Virelai has none)
d.text("404", "Flag 404", x=448, y=540, size=30, font="Source Sans 3",
       color=DEAD, justify="center")

# arms: sleeves folded over the flag's upper corners
d.path("M336,470 C362,480 380,486 398,492", "Sleeve L", fill=NONE,
       stroke="#525A70", strokeWidth=22, cap="round")
d.path("M560,470 C534,480 516,486 498,492", "Sleeve R", fill=NONE,
       stroke="#525A70", strokeWidth=22, cap="round")
d.shape("ellipse", "Hand L", x=392, y=478, width=26, height=20,
        fill="#767F94", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Hand R", x=478, y=478, width=26, height=20,
        fill="#767F94", stroke=INK, strokeWidth=4)

# a dried bloom pinned at the fold — the caretaker's only decoration
d.shape("ellipse", "Bloom c", x=441, y=594, width=14, height=14,
        fill="#C4706A", stroke=INK, strokeWidth=2)
for dx, dy in [(-11,0),(11,0),(0,-11),(0,11)]:
    d.shape("ellipse", f"Petal {dx},{dy}", x=448+dx-7, y=601+dy-7,
            width=14, height=14, fill="#A86A62", stroke=INK, strokeWidth=2)

# --- captions -----------------------------------------------------------------------
d.text("INDEX MOURNER", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#C4DAD4", justify="center")
r = d.text("CARETAKER OF DEAD POINTERS", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#8AA39E", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("237.index-mourner-V1R00")
