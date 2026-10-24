#!/usr/bin/env python3
"""Cass D Failure — mascot portrait V1R00.
A teal administrator filing apology notes into key-value pairs, three
identical copies of the same record stacked on her desk. She renders with
two faint out-of-sync echoes of herself — eventual consistency made
visible; each copy believes it is canonical.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Cass D Failure — Mascot Portrait", 1000, 1000)

INK = "#1A1E26"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#0D1218"}, {"offset": 1, "color": "#05070B"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#32454E"}, {"offset": 0.7, "color": "#1B2930"},
    {"offset": 1, "color": "#0B1216"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#26343C"}, {"offset": 1, "color": "#0B1216"}]}}
BODY_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#9AD8CE"}, {"offset": 0.72, "color": "#5FA89C"},
    {"offset": 1, "color": "#38786E"}]}}
CAB_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5E6E7A"}, {"offset": 0.55, "color": "#42505A"},
    {"offset": 1, "color": "#28323A"}]}}
CARD_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F2E8D4"}, {"offset": 0.65, "color": "#DECFAE"},
    {"offset": 1, "color": "#BFA87E"}]}}
SORRY = "#C86A72"
PALE = "#C8DDE2"
DESK_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4A3E2E"}, {"offset": 0.6, "color": "#332A1E"},
    {"offset": 1, "color": "#1E1810"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#52707A", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#A8CCD4", strokeWidth=3, opacity=45)
for i, (x, y, w) in enumerate([(193, 233, 8), (801, 230, 7), (157, 524, 9),
                               (837, 544, 8), (247, 766, 7), (753, 749, 9),
                               (133, 393, 6), (864, 391, 7), (391, 113, 7),
                               (613, 110, 8), (333, 823, 6), (665, 821, 7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#3E525A", opacity=45, stroke=NONE)

# --- floor ----------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#080D10",
       strokeWidth=4, opacity=70)

# --- the key-value store: an open card drawer, left --------------------------------
vx0, vy0, vw, vh = 210, 470, 150, 224
d.shape("ellipse", "Cabinet shadow", x=vx0 - 10, y=vy0 + vh - 2,
        width=vw + 20, height=20, fill="#000000", opacity=30, stroke=NONE)
d.shape("rectangle", "KV cabinet", x=vx0, y=vy0, width=vw, height=vh,
        radius=8, fill=CAB_GRAD, stroke=INK, strokeWidth=5)
d.shape("rectangle", "KV top lip", x=vx0 - 4, y=vy0 - 8, width=vw + 8,
        height=14, radius=4, fill="#6E7E8A", stroke=INK, strokeWidth=3)
# open drawer tray: a dark slot; the card riding up out of it reads
# "sorry" -> "accepted"
d.shape("rectangle", "Drawer slot", x=vx0 + 14, y=vy0 + 26, width=vw - 28,
        height=64, radius=4, fill="#14181E", stroke=INK, strokeWidth=3)
d.path(rot_rect_path(vx0 + 46, vy0 + 8, 108, 60, -3), "Drawer card",
       fill=CARD_GRAD, stroke=INK, strokeWidth=2.5)
d.text("SORRY", "Card key", x=vx0 + 24, y=vy0 - 2, size=11,
       font="Virelai Sans", color=SORRY, justify="center")
d.path(f"M{vx0 + 38},{vy0 + 14} L{vx0 + 54},{vy0 + 14}",
       "Card arrow", fill=NONE, stroke="#5E7A68", strokeWidth=2)
d.path(f"M{vx0 + 54},{vy0 + 14} L{vx0 + 50},{vy0 + 10} "
       f"L{vx0 + 50},{vy0 + 18} Z", "Arrow head",
       fill="#5E7A68", stroke=NONE)
d.text("ACCEPTED", "Card val", x=vx0 + 74, y=vy0 + 24, size=10,
       font="Virelai Sans", color="#5E7A68", justify="center")
# lower drawers: shut, indexed
for j, dy in enumerate([vy0 + 108, vy0 + 164]):
    d.shape("rectangle", f"KV drawer {j+1}", x=vx0 + 14, y=dy, width=vw - 28,
            height=46, radius=4, fill="#3A4650", stroke=INK, strokeWidth=3)
    d.shape("rectangle", f"KV label {j+1}", x=vx0 + 48, y=dy + 8, width=54,
            height=14, radius=2, fill="#C9BFA0", stroke=INK, strokeWidth=2)
    d.path(f"M{vx0 + 60},{dy + 34} L{vx0 + 92},{dy + 34}", f"KV pull {j+1}",
           fill=NONE, stroke="#7E8E9A", strokeWidth=5, cap="round")
# --- desk, right ---------------------------------------------------------------------
dx0, dy0, dw = 560, 604, 270
d.shape("ellipse", "Desk shadow", x=dx0 - 12, y=dy0 + 90, width=dw + 24,
        height=20, fill="#000000", opacity=32, stroke=NONE)
d.shape("rectangle", "Desk top", x=dx0 - 8, y=dy0 - 14, width=dw + 16,
        height=24, radius=8, fill=DESK_GRAD, stroke=INK, strokeWidth=4)
d.shape("rectangle", "Desk side", x=dx0 + 8, y=dy0 + 8, width=dw - 16,
        height=84, fill={"gradient": {"kind": "linear", "stops": [
            {"offset": 0, "color": "#3A3024"}, {"offset": 1, "color": "#1E1810"}]}},
        stroke=INK, strokeWidth=4)
# three identical copies of the same record, stacked and slightly fanned
for k in range(3):
    d.path(rot_rect_path(dx0 + 186 - k * 26, dy0 - 26 - k * 4, 92, 58, -4 - k * 3),
           f"Record copy {k+1}", fill=CARD_GRAD, stroke=INK, strokeWidth=2.5)
    for m in range(2):
        d.path(rot_rect_path(dx0 + 186 - k * 26, dy0 - 30 - k * 4 + m * 12,
                             60 - m * 6, 2.5, -4 - k * 3),
               f"Record line {k+1}.{m+1}", fill=INK, opacity=45, stroke=NONE)
    d.path(rot_rect_path(dx0 + 186 - k * 26, dy0 - 44 - k * 4, 34, 8, -4 - k * 3),
           f"Record tab {k+1}", fill=SORRY, stroke=NONE, opacity=75)

# --- Cass: three reads of the same write ----------------------------------------------
# two out-of-sync echoes first — translucent, offset, unstroked
ECHO_D = "M470,268 C548,268 602,334 610,440 C616,524 600,616 578,682 " \
         "C556,692 388,692 366,682 C344,616 328,524 334,440 " \
         "C342,334 396,268 470,268 Z"
d.path(ECHO_D, "Echo left", fill="#5FA89C", opacity=12, stroke=NONE)
d.path(ECHO_D, "Echo right", fill="#9AD8CE", opacity=10, stroke=NONE)
doc = d.call("inspect_document", {"kind": "Path"}, "inspect paths")
echo_ids = [n["id"] for n in (doc or {}).get("nodes", [])
            if str(n.get("name", "")).startswith("Echo")]
if len(echo_ids) == 2:
    d.cmd("object.move", "echo L shift", ids=[echo_ids[0]], dx=-22, dy=-10)
    d.cmd("object.move", "echo R shift", ids=[echo_ids[1]], dx=20, dy=8)

# canonical Cass: teal blob, forward
d.path(ECHO_D, "Body", fill=BODY_GRAD, stroke=INK, strokeWidth=6)
# side shade + belly light
d.shape("ellipse", "Belly light", x=380, y=500, width=190, height=160,
        fill="#FFFFFF", opacity=13, stroke=NONE)
d.shape("ellipse", "Top light", x=392, y=286, width=150, height=42,
        fill="#FFFFFF", opacity=15, stroke=NONE)
# feet
for lbl, fx in [("Foot L", 386), ("Foot R", 512)]:
    d.shape("ellipse", lbl, x=fx, y=674, width=74, height=34,
            fill="#5FA89C", stroke=INK, strokeWidth=4)

# the face: cheerful, a little lost — one eye blinking out of sync
d.shape("ellipse", "Eye L", x=412, y=430, width=28, height=32,
        fill="#10161A", stroke=NONE)
d.shape("ellipse", "Glint L", x=419, y=436, width=8, height=8,
        fill="#FFFFFF", opacity=85, stroke=NONE)
# right eye mid-glitch: half-lidded
d.shape("ellipse", "Eye R", x=500, y=434, width=28, height=24,
        fill="#10161A", stroke=NONE)
d.shape("ellipse", "Glint R", x=507, y=440, width=8, height=8,
        fill="#FFFFFF", opacity=85, stroke=NONE)
d.path("M498,430 L532,430", "Lid line", fill=NONE, stroke="#38786E",
       strokeWidth=3, cap="round")
# calm brows — she doesn't know which version she's in
d.path("M400,414 C412,404 430,402 444,410", "Brow L", fill=NONE,
       stroke=INK, strokeWidth=4.5, cap="round")
d.path("M488,412 C500,402 518,402 532,410", "Brow R", fill=NONE,
       stroke=INK, strokeWidth=4.5, cap="round")
# warm, slightly lopsided smile
d.path("M424,498 C450,516 494,516 518,496", "Smile", fill=NONE,
       stroke=INK, strokeWidth=7, cap="round")
# blush, a tint too warm — the un-synced cheek
for lbl, bx, op in [("Blush L", 388, 36), ("Blush R", 512, 28)]:
    d.shape("ellipse", lbl, x=bx, y=478, width=44, height=24,
            fill=SORRY, opacity=op, stroke=NONE)

# left arm: dropping the apology note into the drawer
d.path("M366,478 C336,466 318,458 300,450", "Arm L", fill=NONE,
       stroke="#5FA89C", strokeWidth=26, cap="round")
d.shape("ellipse", "Hand L", x=280, y=430, width=38, height=32,
        fill="#7FBEB4", stroke=INK, strokeWidth=4)
# the note, mid-release over the open slot
d.path(rot_rect_path(302, 428, 50, 38, -18), "Sorry note", fill=CARD_GRAD,
       stroke=INK, strokeWidth=2.5)
d.text("sorry", "Note word", x=300, y=434, size=11, font="Source Sans 3",
       color=SORRY, justify="center")

# right arm: an uncertain wave toward the record stack
d.path("M578,480 C612,498 626,520 630,544", "Arm R", fill=NONE,
       stroke="#5FA89C", strokeWidth=26, cap="round")
d.shape("ellipse", "Hand R", x=614, y=534, width=38, height=32,
        fill="#7FBEB4", stroke=INK, strokeWidth=4)
# hesitation ticks — she may already have filed this
for i, (hx, hy) in enumerate([(656, 500), (668, 520)]):
    d.path(f"M{hx},{hy} L{hx + 10},{hy - 10}", f"Hesitate {i+1}",
           fill=NONE, stroke=PALE, strokeWidth=4, opacity=60, cap="round")

# a small sync badge pinned on her chest: two arrows chasing each other,
# never quite catching up
d.shape("ellipse", "Sync badge", x=442, y=560, width=56, height=56,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#EAF4F0"}, {"offset": 1, "color": "#A8CCC4"}]}},
        stroke="#38786E", strokeWidth=4)
d.path("M456,582 A16,16 0 0 1 480,572", "Sync arc 1", fill=NONE,
       stroke="#38786E", strokeWidth=4, cap="round")
d.path("M480,572 L472,572 L478,564 Z", "Sync head 1", fill="#38786E",
       stroke=NONE)
d.path("M484,590 A16,16 0 0 1 460,600", "Sync arc 2", fill=NONE,
       stroke="#38786E", strokeWidth=4, cap="round")
d.path("M460,600 L468,600 L462,608 Z", "Sync head 2", fill="#38786E",
       stroke=NONE)

# --- captions ----------------------------------------------------------------------
d.text("CASS D FAILURE", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#DCECEA", justify="center")
r = d.text("MEMORY LOSS ADMINISTRATOR", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#8FB8B2", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("006.cass-d-failure-V1R00")
