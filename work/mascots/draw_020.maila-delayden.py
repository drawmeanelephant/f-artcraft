#!/usr/bin/env python3
"""Maila Delayden — mascot portrait V1R00. Message Queue Oracle.
Hooded oracle sorting yellowed envelopes; a queue of waiting letters
recedes to her right, delivery ledger open at her feet.
"It will arrive. It always arrives."
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Maila Delayden — Mascot Portrait", 1000, 1000)

INK = "#33262E"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#232A36"}, {"offset": 1, "color": "#0D1016"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#EEDCB4"}, {"offset": 0.7, "color": "#CBAF80"},
    {"offset": 1, "color": "#8C704C"}]}}
ROBE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#5E6280"}, {"offset": 0.72, "color": "#41445C"},
    {"offset": 1, "color": "#2B2D3E"}]}}
ENV_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F0E2B4"}, {"offset": 1, "color": "#CBB077"}]}}
PAGE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F4EAD0"}, {"offset": 1, "color": "#DCC99C"}]}}
SKIN = "#E4C49A"
SEAL = "#A84438"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#7A5F42", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F2E8CC", strokeWidth=3, opacity=50)
for i, (x, y, w) in enumerate([(200,215,8),(792,220,7),(168,520,9),(830,530,8),
                               (248,772,7),(748,756,9),(140,390,6),(858,396,7),
                               (395,112,7),(610,114,8),(330,820,6),(664,814,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#9A7A52", opacity=42, stroke=NONE)

# halo of held time behind the oracle
d.shape("ellipse", "Halo", x=330, y=190, width=340, height=340,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#F6E9C2", "opacity": 0.55},
            {"offset": 1, "color": "#F6E9C2", "opacity": 0}]}}, stroke=NONE)

# floor line, ends well inside the rim
d.path("M240,748 C380,734 640,734 792,744", "Floor line",
       fill=NONE, stroke="#8A6A48", strokeWidth=3, opacity=50, cap="round")

# --- the queue of yellowed envelopes, receding right ----------------------------
queue = [
    (606, 640, 96, 66),   # next up, biggest
    (700, 655, 78, 54),
    (776, 666, 62, 44),
    (812, 642, 44, 32),   # the queue curves up as it recedes, ends on the rim arc
]
for i, (x, y, w, h) in enumerate(queue):
    op = max(45, 100 - i * 16)
    d.shape("ellipse", f"Env{i} shadow", x=x - 5, y=y + h + 2, width=w + 10,
            height=9, fill="#6E4E38", opacity=30, stroke=NONE)
    d.shape("rectangle", f"Env{i} body", x=x, y=y, width=w, height=h, radius=6,
            fill=ENV_GRAD, stroke=INK, strokeWidth=4, opacity=op)
    d.path(f"M{x+4},{y+5} L{x+w/2},{y+h*0.52} L{x+w-4},{y+5}",
           f"Env{i} flap", fill=NONE, stroke=INK, strokeWidth=3,
           join="round", opacity=max(40, op - 8))
    if i < 2:  # the front two wait with eyes open
        es = w * 0.09
        d.shape("ellipse", f"Env{i} eye L", x=x + w * 0.36, y=y + h * 0.62,
                width=es, height=es * 1.25, fill="#33222A", stroke=NONE,
                opacity=op)
        d.shape("ellipse", f"Env{i} eye R", x=x + w * 0.56, y=y + h * 0.62,
                width=es, height=es * 1.25, fill="#33222A", stroke=NONE,
                opacity=op)
    if i == 0:  # wax seal on the next letter out
        d.shape("ellipse", "Env0 seal", x=x + w / 2 - 8, y=y + h * 0.28,
                width=16, height=14, fill=SEAL, stroke=INK, strokeWidth=2.5)
    # stamp corner, top right of each envelope
    d.shape("rectangle", f"Env{i} stamp", x=x + w - 18, y=y + 6,
            width=12, height=10, fill="#F6EFDA", stroke=INK,
            strokeWidth=2, opacity=max(40, op - 8))
# patience marks over the last in line
d.path("M814,628 L822,620 M840,632 L846,624", "Wait marks", fill=NONE,
       stroke=INK, strokeWidth=3, cap="round", opacity=40)

# --- the delivery ledger, open at lower left -------------------------------------
# book shadow + cover
d.shape("ellipse", "Ledger shadow", x=206, y=712, width=180, height=18,
        fill="#6E4E38", opacity=35, stroke=NONE)
d.path("M222,664 L296,650 L372,664 L372,716 L296,702 L222,716 Z",
       "Ledger cover", fill="#5E4630", stroke=INK, strokeWidth=4, join="round")
# fanned pages: left page, right page
d.path("M228,660 L294,648 L294,698 L228,710 Z", "Ledger page L",
       fill=PAGE_GRAD, stroke=INK, strokeWidth=3.5, join="round")
d.path("M298,648 L366,660 L366,710 L298,698 Z", "Ledger page R",
       fill=PAGE_GRAD, stroke=INK, strokeWidth=3.5, join="round")
# ruled entries — some struck through, delivered at last
for j, yy in enumerate([662, 672, 682, 692]):
    d.path(f"M236,{yy} L282,{yy - 6}", f"Entry L{j+1}", fill=NONE,
           stroke="#8A7A5C", strokeWidth=2.5, opacity=75)
for j, yy in enumerate([662, 672, 682]):
    d.path(f"M308,{yy - 6} L356,{yy}", f"Entry R{j+1}", fill=NONE,
           stroke="#8A7A5C", strokeWidth=2.5, opacity=75)
d.path("M236,684 L282,678", "Struck entry", fill=NONE, stroke=SEAL,
       strokeWidth=3, opacity=70)
# bookmark ribbon trailing out
d.path("M296,700 C294,714 298,724 292,734 L300,732 C304,722 300,712 302,700 Z",
       "Ribbon", fill=SEAL, stroke=INK, strokeWidth=2.5, join="round")

# --- Maila: the oracle ------------------------------------------------------------
d.shape("ellipse", "Figure shadow", x=346, y=740, width=300, height=26,
        fill="#6E4E38", opacity=38, stroke=NONE)
# robe: bell silhouette
d.path("M370,748 C360,646 366,556 396,486 C420,430 458,408 496,412 "
       "C540,418 570,468 578,548 C586,636 588,700 586,748 Z",
       "Robe", fill=ROBE_GRAD, stroke=INK, strokeWidth=7, join="round")
# robe folds
d.path("M420,560 C416,620 414,680 416,730 M500,560 C506,624 508,684 506,734",
       "Robe folds", fill=NONE, stroke="#2A2C3A", strokeWidth=4,
       opacity=45, cap="round")
# hem band
d.path("M372,716 C440,728 540,728 584,716 L586,748 L370,748 Z",
       "Hem band", fill="#262836", opacity=60, stroke=NONE)
# hood: arch over the head, falling into the shoulders
d.path("M396,492 C384,418 410,342 482,332 C554,342 582,418 572,492 "
       "C548,462 516,450 484,450 C450,450 420,464 396,492 Z",
       "Hood", fill="#4C4F68", stroke=INK, strokeWidth=6, join="round")
d.path("M404,478 C400,420 424,362 482,354 C540,362 564,420 560,478",
       "Hood rim light", fill=NONE, stroke="#8B8FA8", strokeWidth=4,
       opacity=55, cap="round")
# face shadow inside the hood
d.shape("ellipse", "Face shadow", x=438, y=398, width=92, height=76,
        fill="#1E1A22", stroke=NONE)
# oracle eyes, lit from within
d.shape("ellipse", "Eye L", x=460, y=428, width=15, height=18,
        fill="#F0C878", stroke=NONE)
d.shape("ellipse", "Eye R", x=494, y=428, width=15, height=18,
        fill="#F0C878", stroke=NONE)
d.shape("ellipse", "Eye glint L", x=463, y=431, width=5, height=5,
        fill="#FFF6DC", stroke=NONE)
d.shape("ellipse", "Eye glint R", x=497, y=431, width=5, height=5,
        fill="#FFF6DC", stroke=NONE)
# small knowing mouth, barely there
d.path("M476,458 C482,462 490,462 496,458", "Mouth",
       fill=NONE, stroke="#8A7458", strokeWidth=3.5, cap="round", opacity=80)

# left sleeve raised, holding the letter under consideration
d.path("M398,520 C368,540 352,572 356,602", "Sleeve L",
       fill=NONE, stroke="#41445C", strokeWidth=30, cap="round")
d.shape("ellipse", "Hand L", x=344, y=580, width=32, height=26,
        fill=SKIN, stroke=INK, strokeWidth=4)
# the letter in her hand — held up, considered
d.path(rot_rect_path(340, 566, 62, 44, -10), "Held letter",
       fill=ENV_GRAD, stroke=INK, strokeWidth=4, join="round")
d.path("M314,556 L342,578 L368,564", "Held letter flap", fill=NONE,
       stroke=INK, strokeWidth=3, join="round")
# right arm extended over the queue, unhurried blessing
d.path("M560,540 C596,556 614,584 616,612", "Sleeve R",
       fill=NONE, stroke="#41445C", strokeWidth=30, cap="round")
d.shape("ellipse", "Hand R", x=600, y=600, width=32, height=28,
        fill=SKIN, stroke=INK, strokeWidth=4)

# the slow delivery route: dashed arc overhead, one envelope mid-flight
d.path("M560,300 C640,220 760,210 830,280", "Delivery arc",
       fill=NONE, stroke="#E8D4A0", strokeWidth=3.5, dash=[4, 12],
       cap="round", opacity=60)
d.path(rot_rect_path(838, 268, 44, 30, 14), "Envelope in transit",
       fill=ENV_GRAD, stroke=INK, strokeWidth=3.5, join="round", opacity=90)
d.path("M822,262 L840,276 L858,266", "Transit flap", fill=NONE,
       stroke=INK, strokeWidth=2.5, join="round", opacity=80)

# --- name + role -------------------------------------------------------------------
d.text("MAILA DELAYDEN", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#F0E4C8", justify="center")
r = d.text("MESSAGE QUEUE ORACLE", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#C8AE84", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=180)

d.finish("020.maila-delayden-V1R00")
