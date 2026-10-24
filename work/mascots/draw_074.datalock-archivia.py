#!/usr/bin/env python3
"""Datalock Archivia — mascot portrait V1R00.
A stern little archivist in spectacles and a tight bun cross-checking
YAML fields against The Manifest — a great tilted ledger whose rows she
ticks off in green, save one unauthorized field struck through in red
pencil and annotated OUT OF SPEC. 1000x1000.
Gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Datalock Archivia — Mascot Portrait", 1000, 1000)

INK = "#2A1E2E"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#171321"}, {"offset": 1, "color": "#0A0712"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#5D5680"}, {"offset": 0.7, "color": "#403A5C"},
    {"offset": 1, "color": "#221E36"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#322C4C"}, {"offset": 1, "color": "#171426"}]}}
ROBE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5A5482"}, {"offset": 1, "color": "#322E50"}]}}
SKIN_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F2DECA"}, {"offset": 0.75, "color": "#DDBDA2"},
    {"offset": 1, "color": "#B98F78"}]}}
PAGE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F4ECD6"}, {"offset": 1, "color": "#D6C8A2"}]}}
HAIR = "#3A2E3C"
CHIP_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4A4468"}, {"offset": 1, "color": "#2E2A48"}]}}
SEAL_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E8CE8A"}, {"offset": 1, "color": "#B08E44"}]}}
CREAM = "#F0E6CC"
GREEN = "#5EA87A"
RED = "#B84840"
GOLD = "#D8B868"
LAMP = "#F0DCA8"
KEY_INK = "#7A6A52"
VAL_INK = "#A6937A"

def rot_pt(cx, cy, x, y, deg):
    a = math.radians(deg); c, s = math.cos(a), math.sin(a)
    return (cx + (x - cx) * c - (y - cy) * s,
            cy + (x - cx) * s + (y - cy) * c)

# --- backdrop + plate -----------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#7E7396", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#CEC6E2", strokeWidth=3, opacity=45)
for i, (x, y, w) in enumerate([(196,236,8),(798,228,7),(160,522,9),(836,548,8),
                               (250,764,7),(756,748,9),(136,394,6),(862,392,7),
                               (394,112,7),(610,112,8),(336,822,6),(664,820,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#463E64", opacity=45, stroke=NONE)

# --- floor ----------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0E0B1A",
       strokeWidth=4, opacity=70)

# --- lamplight pool from upper left ----------------------------------------------
d.path("M240,140 L470,640 L660,640 L400,140 Z", "Lamp beam", fill=LAMP,
       opacity=9, stroke=NONE)
d.shape("ellipse", "Lamp pool", x=300, y=560, width=420, height=160,
        fill=LAMP, opacity=8, stroke=NONE)
for i, (x, y, s) in enumerate([(300,250,4),(380,330,5),(450,430,4),(520,520,5)]):
    d.shape("ellipse", f"Beam mote {i+1}", x=x, y=y, width=s, height=s,
            fill=LAMP, opacity=40, stroke=NONE)

# --- stray field chips adrift upper-left -------------------------------------------
for i, (cx, cy, w, h, deg, txt) in enumerate([
        (238, 268, 128, 34, -8, "status: ok"),
        (300, 332, 118, 34, 6, "mood: rogue")]):
    d.path(rot_rect_path(cx, cy, w, h, deg), f"Chip {i+1}",
           fill=CHIP_GRAD, stroke="#8A80A8", strokeWidth=2.5,
           join="round", opacity=92)
    tx, ty = rot_pt(cx, cy, cx, cy + 5, deg)
    t = d.text(txt, f"Chip {i+1} label", x=tx, y=ty, size=11,
               font="Virelai Sans", color="#C8BEDE", justify="center")
    if t and t.get("id"):
        d.cmd("object.rotate", f"chip {i+1} tilt", ids=[t["id"]], angle=deg,
              origin=[tx, ty])
# the rogue field is already struck
p1 = rot_pt(300, 332, 256, 332, 6); p2 = rot_pt(300, 332, 344, 332, 6)
d.path(f"M{p1[0]:.0f},{p1[1]:.0f} L{p2[0]:.0f},{p2[1]:.0f}",
       "Rogue strike", fill=NONE, stroke=RED, strokeWidth=3.5, cap="round")

# --- The Manifest: the great ledger page --------------------------------------------
PCX, PCY, PDEG = 668, 448, -4
# back pages fanned behind
for i, dd in enumerate((-9, -1)):
    d.path(rot_rect_path(PCX, PCY, 300, 372, PDEG + dd), f"Back page {i+1}",
           fill="#C9B98F", stroke=INK, strokeWidth=4, join="round", opacity=95)
# front page
d.path(rot_rect_path(PCX, PCY, 300, 372, PDEG), "Manifest page",
       fill=PAGE_GRAD, stroke=INK, strokeWidth=5, join="round")
# header band
hx, hy = rot_pt(PCX, PCY, PCX, PCY - 152, PDEG)
d.path(rot_rect_path(PCX, PCY - 152, 268, 46, PDEG), "Manifest header",
       fill="#3E3858", stroke=INK, strokeWidth=3, join="round")
t = d.text("THE MANIFEST", "Header text", x=hx, y=hy + 6, size=17,
           font="Virelai Sans", color="#EDE4CC", justify="center")
if t and t.get("id"):
    d.cmd("object.rotate", "header tilt", ids=[t["id"]], angle=PDEG,
          origin=[hx, hy])

# --- ledger rows: key stroke, colon, value stroke, verdict mark ---------------------
rows = [
    # (key_w, val_w, verdict) verdict: ok | bad | none
    (66, 96, "ok"), (84, 70, "ok"), (58, 112, "ok"), (76, 88, "ok"),
    (70, 104, "bad"), (88, 64, "ok"), (62, 98, "ok"), (80, 76, "ok"),
    (68, 90, "ok"),
]
row_y0 = PCY - 96
for i, (kw, vw, verdict) in enumerate(rows):
    ry = row_y0 + i * 30
    x0 = PCX - 124
    # key
    a = rot_pt(PCX, PCY, x0, ry, PDEG); b = rot_pt(PCX, PCY, x0 + kw, ry, PDEG)
    d.path(f"M{a[0]:.0f},{a[1]:.0f} L{b[0]:.0f},{b[1]:.0f}",
           f"Row {i+1} key", fill=NONE, stroke=KEY_INK, strokeWidth=5,
           cap="round", opacity=85)
    # colon
    c1 = rot_pt(PCX, PCY, x0 + kw + 8, ry - 2, PDEG)
    d.shape("ellipse", f"Row {i+1} colon", x=c1[0]-2, y=c1[1]-2, width=5,
            height=5, fill=KEY_INK, opacity=85, stroke=NONE)
    # value
    a = rot_pt(PCX, PCY, x0 + kw + 20, ry, PDEG)
    b = rot_pt(PCX, PCY, x0 + kw + 20 + vw, ry, PDEG)
    d.path(f"M{a[0]:.0f},{a[1]:.0f} L{b[0]:.0f},{b[1]:.0f}",
           f"Row {i+1} value", fill=NONE, stroke=VAL_INK, strokeWidth=5,
           cap="round", opacity=75)
    # verdict
    vx = PCX + 122
    if verdict == "ok":
        p1 = rot_pt(PCX, PCY, vx, ry, PDEG)
        p2 = rot_pt(PCX, PCY, vx + 7, ry + 7, PDEG)
        p3 = rot_pt(PCX, PCY, vx + 20, ry - 9, PDEG)
        d.path(f"M{p1[0]:.0f},{p1[1]:.0f} L{p2[0]:.0f},{p2[1]:.0f} "
               f"L{p3[0]:.0f},{p3[1]:.0f}", f"Row {i+1} check", fill=NONE,
               stroke=GREEN, strokeWidth=4, cap="round", join="round")
    elif verdict == "bad":
        # unauthorized field: red strike over key+value and a ring round the row
        a = rot_pt(PCX, PCY, x0 - 6, ry, PDEG)
        b = rot_pt(PCX, PCY, x0 + kw + 20 + vw + 6, ry, PDEG)
        d.path(f"M{a[0]:.0f},{a[1]:.0f} L{b[0]:.0f},{b[1]:.0f}",
               "Bad row strike", fill=NONE, stroke=RED, strokeWidth=4.5,
               cap="round")
        ca = rot_pt(PCX, PCY, x0 + 88, ry, PDEG)
        d.shape("ellipse", "Bad row ring", x=ca[0]-132, y=ca[1]-17,
                width=264, height=34, fill=NONE, stroke=RED,
                strokeWidth=3.5, opacity=85)
        # margin annotation at the foot of the page, clear of the rows
        mx, my = rot_pt(PCX, PCY, PCX - 30, PCY + 166, PDEG)
        t = d.text("OUT OF SPEC", "Margin note", x=mx, y=my, size=10,
                   font="Virelai Sans", color=RED, justify="center")
        if t and t.get("id"):
            d.cmd("object.rotate", "note tilt", ids=[t["id"]], angle=PDEG,
                  origin=[mx, my])

# --- Archivia: the archivist herself --------------------------------------------------
d.shape("ellipse", "Her shadow", x=308, y=688, width=220, height=26,
        fill="#0A0712", opacity=55, stroke=NONE)
# robe: a stern bell of indigo, hem on the floor
d.path("M330,700 C334,616 352,552 388,518 C400,507 430,507 442,518 "
       "C478,552 496,616 500,700 Z",
       "Robe", fill=ROBE_GRAD, stroke=INK, strokeWidth=6, join="round")
# robe shading fold
d.path("M415,540 C420,592 420,650 418,698", "Robe fold", fill=NONE,
       stroke="#241F3C", strokeWidth=4, cap="round", opacity=60)
# collar
d.path("M392,516 L415,542 L438,516 L430,508 L415,520 L400,508 Z",
       "Collar", fill=CREAM, stroke=INK, strokeWidth=3, join="round")
# badge of office: a small wax seal on the chest
d.shape("ellipse", "Seal badge", x=378, y=566, width=30, height=30,
        fill=SEAL_GRAD, stroke=INK, strokeWidth=3)
d.shape("ellipse", "Seal badge core", x=385, y=573, width=16, height=16,
        fill=NONE, stroke="#8A6A2E", strokeWidth=2.5)

# head
d.shape("ellipse", "Head", x=363, y=394, width=104, height=116,
        fill=SKIN_GRAD, stroke=INK, strokeWidth=6)
# hair: severe cap + tight bun
d.path("M365,458 C358,408 384,382 415,382 C446,382 472,408 465,458 "
       "C458,428 442,414 415,414 C388,414 372,428 365,458 Z",
       "Hair cap", fill=HAIR, stroke=INK, strokeWidth=4, join="round")
d.shape("ellipse", "Bun", x=398, y=360, width=34, height=28,
        fill=HAIR, stroke=INK, strokeWidth=4)
d.path("M405,368 C410,374 420,374 426,368", "Bun pin", fill=NONE,
       stroke="#6A5A70", strokeWidth=2.5, cap="round", opacity=80)
# spectacles: round rims, bridge, temples — she reads everything twice
for ex in (395, 439):
    d.shape("ellipse", f"Spec rim {ex}", x=ex-17, y=437, width=34, height=34,
            fill=NONE, stroke=INK, strokeWidth=3.5)
d.path("M412,454 L422,454", "Spec bridge", fill=NONE, stroke=INK,
       strokeWidth=3, cap="round")
d.path("M378,450 L366,444 M456,450 L464,444", "Spec temples", fill=NONE,
       stroke=INK, strokeWidth=3, cap="round")
# eyes behind glass: half-lidded, auditing
d.path("M388,455 L404,455", "Eye L", fill=NONE, stroke=INK, strokeWidth=4,
       cap="round")
d.path("M432,455 L448,455", "Eye R", fill=NONE, stroke=INK, strokeWidth=4,
       cap="round")
# brows: level, unmoved
d.path("M384,432 L406,428", "Brow L", fill=NONE, stroke=INK, strokeWidth=4,
       cap="round")
d.path("M430,428 L452,432", "Brow R", fill=NONE, stroke=INK, strokeWidth=4,
       cap="round")
# nose + the flat line of a mouth that has seen unauthorized fields
d.path("M417,462 L414,472 L420,474", "Nose", fill=NONE, stroke=INK,
       strokeWidth=3, cap="round", join="round")
d.path("M402,490 L430,490", "Mouth", fill=NONE, stroke=INK, strokeWidth=4,
       cap="round")

# right arm: extended to the ledger, red pencil in hand
d.path("M470,556 C506,540 534,512 552,486", "Arm ink", fill=NONE,
       stroke=INK, strokeWidth=30, cap="round")
d.path("M470,556 C506,540 534,512 552,486", "Arm", fill=NONE,
       stroke="#4A4470", strokeWidth=20, cap="round")
d.shape("ellipse", "Hand", x=538, y=466, width=30, height=26,
        fill=SKIN_GRAD, stroke=INK, strokeWidth=4)
# the red pencil, its point resting on the struck row
d.path("M548,468 L614,472", "Pencil shaft", fill=NONE, stroke=RED,
       strokeWidth=10, cap="round")
d.path("M612,467 L636,473 L612,479 Z", "Pencil wood", fill="#D8B06A",
       stroke=INK, strokeWidth=2.5, join="round")
d.path("M632,471 L642,473 L632,476 Z", "Pencil lead", fill=INK,
       stroke=NONE, join="round")
# left arm: cradling a truth slip against the chest
d.path("M362,556 C340,576 334,604 346,624", "Arm L ink", fill=NONE,
       stroke=INK, strokeWidth=28, cap="round")
d.path("M362,556 C340,576 334,604 346,624", "Arm L", fill=NONE,
       stroke="#4A4470", strokeWidth=18, cap="round")
d.shape("ellipse", "Hand L", x=336, y=612, width=26, height=24,
        fill=SKIN_GRAD, stroke=INK, strokeWidth=4)
d.path(rot_rect_path(372, 626, 64, 46, -6), "Truth slip", fill=CREAM,
       stroke=INK, strokeWidth=3, join="round")
d.path("M352,622 L362,632 L386,610", "Truth check", fill=NONE,
       stroke=GREEN, strokeWidth=4, cap="round", join="round")

# stray annotation slips at her feet
for i, (cx, cy, deg) in enumerate([(296, 688, -12), (520, 692, 8)]):
    d.path(rot_rect_path(cx, cy, 44, 30, deg), f"Slip {i+1}",
           fill=CREAM, stroke="#8A7A5A", strokeWidth=2, opacity=85,
           join="round")

# --- captions ----------------------------------------------------------------------
d.text("DATALOCK ARCHIVIA", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#E4DEEE", justify="center")
r = d.text("KEEPER OF THE MANIFEST", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#A89CC4", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("074.datalock-archivia-V1R00")
