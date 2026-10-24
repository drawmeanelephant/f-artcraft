#!/usr/bin/env python3
"""Chairwoman Deferred Change — mascot portrait V1R00.
She does not refuse urgency; she declines to recognize it early.
The steering lantern is being rotated over the change request, and the
light has gone acceptably red — the submission will be approved once it
has suffered visibly enough to deserve the window. 1000x1000.
Gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Chairwoman Deferred Change — Mascot Portrait", 1000, 1000)

INK = "#1A1E2A"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#181C26"}, {"offset": 1, "color": "#131620"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#46506A"}, {"offset": 0.7, "color": "#2E354A"},
    {"offset": 1, "color": "#161A26"}]}}
DESK_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4E3A30"}, {"offset": 1, "color": "#271C16"}]}}
FUR_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#C2B2C8"}, {"offset": 0.7, "color": "#94849E"},
    {"offset": 1, "color": "#665A72"}]}}
HAIR_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#7A7086"}, {"offset": 1, "color": "#4A4258"}]}}
BRASS_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#D8B46A"}, {"offset": 0.55, "color": "#A8843E"},
    {"offset": 1, "color": "#6E5226"}]}}
PAPER_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F0E6CE"}, {"offset": 1, "color": "#CDBB94"}]}}
RED_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F0705C"}, {"offset": 0.7, "color": "#B23430"},
    {"offset": 1, "color": "#6E1C20"}]}}
LENS_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#FF9A80"}, {"offset": 0.75, "color": "#D84038"},
    {"offset": 1, "color": "#7E1E1E"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#5E6884", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C8D0E4", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(198,238,8),(800,234,7),(162,530,9),(836,550,8),
                               (252,766,7),(750,752,9),(140,398,6),(862,394,7),
                               (396,116,7),(612,112,8),(338,824,6),(664,822,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#3A4156", opacity=45, stroke=NONE)

# --- the board-room floor, closed on the disc arc -------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill={"gradient": {"kind": "linear", "stops": [
           {"offset": 0, "color": "#2E2C3A"}, {"offset": 1, "color": "#14121C"}]}},
       stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0C0A12",
       strokeWidth=4, opacity=70)

# --- the freeze-window calendar on the wall, every day politely blacked out -------
d.path(rot_rect_path(676, 252, 190, 140, 3), "Calendar", fill=PAPER_GRAD,
       stroke=INK, strokeWidth=4, join="round")
for r_i, ry in enumerate(range(218, 290, 22)):
    for c_i, cx in enumerate(range(612, 732, 24)):
        d.shape("rectangle", f"Cal cell {r_i},{c_i}", x=cx, y=ry, width=18,
                height=14, fill="#2A2430", opacity=80, stroke=NONE,
                radius=2)
d.path("M608,190 L748,190", "Cal header", fill=NONE, stroke="#8A2430",
       strokeWidth=5, cap="round", opacity=85)

# --- the desk ----------------------------------------------------------------------
d.path("M238,580 L762,580 L796,636 L204,636 Z", "Desk top",
       fill=DESK_GRAD, stroke=INK, strokeWidth=5, join="round")
d.path("M204,636 L796,636 L786,662 L214,662 Z", "Desk edge",
       fill="#221812", stroke=INK, strokeWidth=4, join="round")
d.shape("ellipse", "Desk sheen", x=320, y=588, width=220, height=14,
        fill="#8A6A58", opacity=20, stroke=NONE)

# --- the change request under judgment ----------------------------------------------
d.path("M310,548 L470,540 L478,600 L318,610 Z", "Change request",
       fill=PAPER_GRAD, stroke=INK, strokeWidth=4, join="round")
for i, y in enumerate(range(556, 590, 10)):
    d.path(f"M324,{y} L412,{y - 2}", f"Request line {i+1}", fill=NONE,
           stroke="#8A7A5E", strokeWidth=2.5, cap="round", opacity=80)
# the stamp that returned it for posture
d.path(rot_rect_path(430, 578, 84, 30, -8), "Deferred stamp",
       fill=NONE, stroke="#8A2430", strokeWidth=3, join="round",
       opacity=90)
d.text("DEFERRED", "Stamp text", x=395, y=586, size=13,
       font="Virelai Sans", color="#8A2430", justify="left")

# --- the steering lantern, mid-rotation, rollback aspect showing --------------------
# wash of red light over desk and request — the acceptable colour
d.shape("ellipse", "Red wash wide", x=330, y=420, width=420, height=300,
        fill="#C03028", opacity=14, stroke=NONE)
d.shape("ellipse", "Red wash core", x=430, y=470, width=240, height=190,
        fill="#E04034", opacity=16, stroke=NONE)
# hanger: the little crane the lantern turns on
d.path("M560,470 C560,430 540,410 510,404", "Lantern arm", fill=NONE,
       stroke=BRASS_GRAD, strokeWidth=7, cap="round")
d.shape("ellipse", "Crane base", x=548, y=464, width=30, height=18,
        fill=BRASS_GRAD, stroke=INK, strokeWidth=3)
# rotating bezel ring with its direction arrow
d.shape("ellipse", "Bezel", x=438, y=330, width=140, height=140,
        fill=NONE, stroke=BRASS_GRAD, strokeWidth=8)
d.path("M560,352 C574,366 582,384 582,404 M582,404 L570,392 M582,404 L566,404",
       "Turn arrow", fill=NONE, stroke="#E8C87E", strokeWidth=4,
       cap="round", opacity=85)
# dead aspects around the ring: amber and green, waiting their century
for i, (a, c) in enumerate([(205, "#8A7A3E"), (335, "#3E6E46")]):
    ax = 508 + 78 * math.cos(math.radians(a))
    ay = 400 + 78 * math.sin(math.radians(a))
    d.shape("ellipse", f"Aspect {i+1}", x=ax - 14, y=ay - 14, width=28,
            height=28, fill=c, stroke=INK, strokeWidth=3, opacity=60)
# the lantern body at ring centre
d.path("M470,352 L546,352 L556,440 L460,440 Z", "Lantern body",
       fill={"gradient": {"kind": "linear", "stops": [
           {"offset": 0, "color": "#3A3440"}, {"offset": 1, "color": "#1C1822"}]}},
       stroke=INK, strokeWidth=4, join="round")
d.path("M478,352 C482,330 534,330 538,352", "Lantern cap", fill=BRASS_GRAD,
       stroke=INK, strokeWidth=3.5)
# the red lens, lit — rollback is the visible posture now
d.shape("ellipse", "Red lens", x=484, y=368, width=48, height=52,
        fill=LENS_GRAD, stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Lens hot core", x=496, y=380, width=24, height=26,
        fill="#FFB8A0", opacity=55, stroke=NONE)
# glow thrown forward
d.shape("ellipse", "Lens halo", x=474, y=358, width=68, height=72,
        fill="#E04034", opacity=22, stroke=NONE)

# --- the Chairwoman herself -----------------------------------------------------------
d.shape("ellipse", "Body", x=600, y=512, width=190, height=150,
        fill=FUR_GRAD, stroke=INK, strokeWidth=5)
# the high collar of office
d.path("M622,528 C650,542 740,542 768,528 L760,552 C730,564 660,564 "
       "630,552 Z", "Collar", fill="#5A5470", stroke=INK, strokeWidth=3.5,
       join="round")
d.shape("ellipse", "Head", x=622, y=360, width=156, height=142,
        fill=FUR_GRAD, stroke=INK, strokeWidth=5)
# the bun of presiding authority, pinned tight
d.shape("ellipse", "Bun", x=672, y=322, width=56, height=48,
        fill=HAIR_GRAD, stroke=INK, strokeWidth=4)
d.path("M676,344 C690,336 710,336 724,344", "Bun part", fill=NONE,
       stroke="#3A3448", strokeWidth=2.5, opacity=70, cap="round")
d.shape("ellipse", "Hair cap", x=634, y=350, width=132, height=58,
        fill=HAIR_GRAD, stroke=INK, strokeWidth=4)
# ears under the hairline
for ex in (632, 768):
    d.shape("ellipse", f"Ear {ex}", x=ex - 11, y=424, width=24, height=22,
            fill="#94849E", stroke=INK, strokeWidth=3.5)
# the eyes: calendar-bound apprehension
d.shape("ellipse", "Eye L", x=654, y=428, width=15, height=18,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Eye R", x=728, y=428, width=15, height=18,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Glint L", x=658, y=432, width=5, height=5,
        fill="#FFF6E4", opacity=85, stroke=NONE)
d.shape("ellipse", "Glint R", x=732, y=432, width=5, height=5,
        fill="#FFF6E4", opacity=85, stroke=NONE)
# brows level, posture impeccable
d.path("M648,410 C658,405 670,405 678,409", "Brow L", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.path("M722,409 C732,405 744,405 752,410", "Brow R", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.path("M678,470 C688,475 704,475 714,470", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=3.5, cap="round")
# the arm doing the rotating — ceremony, not refusal
d.path("M614,540 C586,520 566,494 556,466", "Arm rotating", fill=NONE,
       stroke="#94849E", strokeWidth=16, cap="round")
d.shape("ellipse", "Paw on bezel", x=538, y=448, width=32, height=27,
        fill="#C2B2C8", stroke=INK, strokeWidth=4)
# the other paw resting on the queue of resubmissions
d.path("M778,556 C792,570 798,584 800,598", "Arm queue", fill=NONE,
       stroke="#94849E", strokeWidth=15, cap="round")
d.shape("ellipse", "Paw queue", x=784, y=592, width=30, height=25,
        fill="#C2B2C8", stroke=INK, strokeWidth=4)
# the resubmission stack: identical work, visibly more strained each time
for j, (sx, sa) in enumerate([(722, -6), (730, 4), (740, -3)]):
    d.path(rot_rect_path(sx, 600 + j * 8, 96, 26, sa),
           f"Resubmission {j+1}", fill=PAPER_GRAD, stroke=INK,
           strokeWidth=3, join="round", opacity=95)
d.path("M700,586 L800,580", "Queue edge", fill=NONE, stroke="#8A2430",
       strokeWidth=2.5, opacity=70, cap="round")

# --- motes in the committee air -----------------------------------------------------
for i, (x, y, w) in enumerate([(252,428,5),(330,300,6),(664,140,5),(820,480,6),
                               (240,660,5),(830,620,5),(480,240,5),(340,500,4)]):
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#9AA4C4", opacity=32, stroke=NONE)

# --- captions ---------------------------------------------------------------------
d.text("CHAIRWOMAN DEFERRED CHANGE", "Name", x=500, y=930, size=46,
       font="Virelai Sans", color="#E4E8F2", justify="center")
r = d.text("CAB PRESIDING DELAY OFFICER", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#9AA2BE", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=160)

d.finish("307.chairwoman-deferred-change-V1R00")
