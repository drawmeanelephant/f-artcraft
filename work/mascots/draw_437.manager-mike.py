#!/usr/bin/env python3
"""Manager Mike — mascot portrait V1R00.
An empty vest on the hook beside a green dashboard showing his
deactivation notice. 1000x1000. House style: gradients + translucent
shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Manager Mike — Mascot Portrait", 1000, 1000)

INK = "#332A33"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#0C1614"}, {"offset": 1, "color": "#050B0A"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#47625C"}, {"offset": 0.7, "color": "#31473F"},
    {"offset": 1, "color": "#1A2724"}]}}
VEST = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#6E7A6C"}, {"offset": 0.7, "color": "#4E584A"},
    {"offset": 1, "color": "#343C32"}]}}
BRASS = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E8BC62"}, {"offset": 1, "color": "#A87C34"}]}}
PANEL = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#0F2622"}, {"offset": 1, "color": "#081613"}]}}
FLOOR = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2A3A34"}, {"offset": 1, "color": "#141F1C"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#6E948A", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#CFE4DA", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(190,240,8),(800,230,7),(160,520,9),(830,540,8),
                               (240,760,7),(760,740,9),(130,390,6),(865,390,7),
                               (390,110,7),(610,110,8),(330,820,6),(665,815,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#3F5A50", opacity=45, stroke=NONE)

# --- floor ---------------------------------------------------------------------
d.shape("ellipse", "Floor", x=170, y=640, width=660, height=120,
        fill=FLOOR, stroke=NONE, opacity=90)
d.shape("ellipse", "Vest shadow", x=240, y=676, width=180, height=30,
        fill="#060D0B", opacity=50, stroke=NONE)

# --- dashboard: green status board, deactivation notice --------------------------
d.shape("ellipse", "Dash glow", x=585, y=290, width=280, height=220,
        fill="#4ADE80", opacity=8, stroke=NONE)
d.shape("rectangle", "Dashboard", x=600, y=300, width=230, height=190,
        fill=PANEL, stroke="#4A7A6A", strokeWidth=5, radius=12)
d.text("TEAM STATUS", "Dash title", x=715, y=330, size=15, font="Virelai Sans",
       color="#7FBEA8", justify="center")
# roster rows: three green actives, one greyed
rows = [("DEE", "#58E896"), ("RAJ", "#58E896"), ("LOU", "#58E896")]
for i, (nm, dot) in enumerate(rows):
    y = 352 + i*26
    d.shape("ellipse", f"Row dot {nm}", x=620, y=y, width=12, height=12,
            fill=dot, stroke=NONE)
    d.shape("rectangle", f"Row bar {nm}", x=644, y=y+1, width=110, height=10,
            fill="#2E5A4C", stroke=NONE, radius=4)
    d.text(nm, f"Row name {nm}", x=766, y=y+11, size=11, font="Virelai Sans",
           color="#9FD8C2", justify="left")
# deactivation notice card
d.shape("rectangle", "Notice", x=614, y=438, width=202, height=40,
        fill="#1E1214", stroke="#B06A6A", strokeWidth=3, radius=8)
d.shape("ellipse", "Notice avatar", x=624, y=448, width=20, height=20,
        fill="#4A4448", stroke="#7A6A6A", strokeWidth=2)
d.text("MIKE — DEACTIVATED", "Notice text", x=652, y=464, size=12,
       font="Virelai Sans", color="#E8A8A0", justify="left")

# --- the hook + hanger -----------------------------------------------------------
d.shape("ellipse", "Hook base", x=316, y=296, width=28, height=28,
        fill=BRASS, stroke=INK, strokeWidth=4)
d.path("M330,322 C330,336 342,340 348,334 C352,330 350,322 344,320",
       "Hook curve", fill=NONE, stroke=BRASS, strokeWidth=7, cap="round")
# hanger: wire triangle under the collar
d.path("M330,348 L278,408 M330,348 L382,408 M278,408 L382,408",
       "Hanger", fill=NONE, stroke="#9A7A4E", strokeWidth=6, cap="round", join="round")

# --- the empty vest ----------------------------------------------------------------
d.path("M292,398 C278,402 266,414 262,434 C254,474 262,552 268,604 "
       "C271,636 268,656 268,660 L392,660 C392,656 389,636 392,604 "
       "C398,552 406,474 398,434 C394,414 382,402 368,398 L352,398 "
       "L330,446 L308,398 Z",
       "Vest", fill=VEST, stroke=INK, strokeWidth=6, join="round")
# hollow collar void + the faintest echo of Mike
d.path("M312,400 L330,438 L348,400 Z", "Collar void", fill="#141A16", stroke=NONE)
d.shape("ellipse", "Echo eye L", x=321, y=414, width=6, height=8,
        fill="#CFE4DA", opacity=24, stroke=NONE)
d.shape("ellipse", "Echo eye R", x=334, y=414, width=6, height=8,
        fill="#CFE4DA", opacity=24, stroke=NONE)
d.path("M323,430 C327,427 333,427 337,430", "Echo mouth", fill=NONE,
       stroke="#CFE4DA", strokeWidth=3, opacity=20, cap="round")
# front seam + buttons
d.path("M330,446 L330,652", "Vest seam", fill=NONE, stroke=INK,
       strokeWidth=4, opacity=60)
for i, y in enumerate([486, 540, 594]):
    d.shape("ellipse", f"Button {i+1}", x=322, y=y, width=15, height=15,
            fill=BRASS, stroke=INK, strokeWidth=3)
# pocket welts
d.path("M284,566 L314,560", "Pocket L", fill=NONE, stroke=INK,
       strokeWidth=4, cap="round", opacity=70)
d.path("M346,560 L376,566", "Pocket R", fill=NONE, stroke=INK,
       strokeWidth=4, cap="round", opacity=70)
# name tag still pinned
d.shape("rectangle", "Name tag", x=290, y=488, width=52, height=22,
        fill=BRASS, stroke=INK, strokeWidth=3, radius=3)
d.text("MIKE", "Tag text", x=316, y=503, size=11, font="Virelai Sans",
       color="#3A2814", justify="center")
# vest sheen + hem shadow
d.shape("ellipse", "Vest highlight", x=280, y=420, width=70, height=30,
        fill="#FFFFFF", opacity=10, stroke=NONE)
d.path("M272,630 C300,642 360,642 388,630 C360,636 300,636 272,630 Z",
       "Hem shadow", fill="#242C24", opacity=50, stroke=NONE)

# --- dust + a slack lanyard on a second, unused hook -------------------------------
d.shape("ellipse", "Hook base 2", x=452, y=296, width=28, height=28,
        fill=BRASS, stroke=INK, strokeWidth=4)
d.path("M466,322 C466,336 478,340 484,334 C488,330 486,322 480,320",
       "Hook curve 2", fill=NONE, stroke=BRASS, strokeWidth=7, cap="round")
d.path("M466,336 C452,380 452,430 466,470 C480,430 480,380 466,336",
       "Lanyard loop", fill=NONE, stroke="#5A6A60", strokeWidth=5, cap="round")
d.shape("rectangle", "Badge", x=452, y=466, width=30, height=40,
        fill="#3E4A44", stroke=INK, strokeWidth=3, radius=4)
d.shape("ellipse", "Badge photo", x=459, y=475, width=16, height=14,
        fill="#2A322E", stroke=NONE)
for i, (x, y, w, o) in enumerate([(250,300,6,25),(430,420,5,20),(300,700,5,18),
                                  (560,330,6,22),(240,470,5,20)]):
    d.shape("ellipse", f"Dust {i+1}", x=x, y=y, width=w, height=w,
            fill="#CFE4DA", opacity=o, stroke=NONE)

# --- captions ----------------------------------------------------------------------
d.text("MANAGER MIKE", "Name", x=500, y=930, size=60,
       font="Virelai Sans", color="#D8EBE2", justify="center")
r = d.text("VEST ON THE HOOK · DEACTIVATED", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#96B8AA", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("437.manager-mike-V1R00")
