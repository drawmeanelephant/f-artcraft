#!/usr/bin/env python3
"""Glassy MacCheckface — mascot portrait V1R00.
Spectral QA inspector holding a translucent clipboard stamped
"ALPHA BATCH ONLY" in the pale rows of Transparent Terrace.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Glassy MacCheckface — Mascot Portrait", 1000, 1000)

INK = "#3B322E"
BG_GRAD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000], "stops": [
    {"offset": 0, "color": "#0E1A16"}, {"offset": 1, "color": "#050C09"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#D8E4CC"}, {"offset": 0.7, "color": "#A4BFA0"},
    {"offset": 1, "color": "#5E7A64"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "start": [0, 660], "end": [0, 880], "stops": [
    {"offset": 0, "color": "#9AB292"}, {"offset": 1, "color": "#58705C"}]}}
BODY_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F8F2CC"}, {"offset": 0.7, "color": "#E2DAA0"},
    {"offset": 1, "color": "#B4AE74"}]}}
GLASS = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F2FBF4"}, {"offset": 1, "color": "#BCD8CC"}]}}
LEAF_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#A8C48A"}, {"offset": 1, "color": "#5E7C50"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#7A9A7E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E4F0DC", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(190,240,8),(800,232,7),(160,520,9),(832,545,8),
                               (246,764,7),(754,748,9),(134,392,6),(862,392,7),
                               (392,114,7),(612,112,8),(334,822,6),(664,820,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#6E8C72", opacity=45, stroke=NONE)

# --- pale orchard: horizon grove + receding rows -------------------------------
# hazy horizon band of spectral trees
d.shape("ellipse", "Grove haze", x=230, y=360, width=540, height=90,
        fill="#EAF3DE", opacity=30, stroke=NONE)
for i, (x, w) in enumerate([(250,60),(330,74),(420,88),(510,80),(600,70),(680,58)]):
    d.shape("ellipse", f"Horizon tree {i+1}", x=x, y=372, width=w, height=w*0.7,
            fill="#C6D8B4", opacity=70, stroke=NONE)
# ground: orchard floor, closed on the disc's own arc
d.path("M135,660 L865,660 A420,420 0 0 1 135,660 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M135,660 L865,660", "Floor line", fill=NONE, stroke="#465E4C",
       strokeWidth=4, opacity=60)
# receding rows toward VP (500,430): pale trunks + Transparent canopies
rows = [
    # (x, y, canopy w, trunk h) left side then right side, far -> near
    (330, 470, 52, 26), (262, 540, 74, 36), (196, 630, 100, 46),
    (618, 470, 52, 26), (664, 540, 74, 36), (704, 630, 100, 46),
]
for i, (x, y, w, th) in enumerate(rows):
    d.shape("rectangle", f"Trunk {i+1}", x=x+w/2-4, y=y+w*0.4, width=8,
            height=th, fill="#6E5844", opacity=75, stroke=NONE, radius=3)
    d.shape("ellipse", f"Row tree {i+1}", x=x, y=y, width=w, height=w*0.72,
            fill="#E4EFD2", opacity=80, stroke="#8AA27C", strokeWidth=3)
    # one pale Yellow Transparent fruit per tree
    d.shape("ellipse", f"Fruit {i+1}", x=x+w*0.62, y=y+w*0.42, width=w*0.2,
            height=w*0.2, fill="#F4ECC0", opacity=90, stroke=NONE)
# drifting mist band
d.path("M160,560 C320,540 680,540 840,560 C700,585 300,585 160,560 Z",
       "Orchard mist", fill="#F0F7E4", opacity=22, stroke=NONE)

# --- Glassy: spectral translucent body -----------------------------------------
d.shape("ellipse", "Glassy shadow", x=365, y=660, width=270, height=32,
        fill="#2A3A2E", opacity=45, stroke=NONE)
# glassy body: a Yellow Transparent apple gone half-ghost
d.path("M500,318 C578,318 636,392 636,478 C636,572 576,646 500,646 "
       "C424,646 364,572 364,478 C364,392 422,318 500,318 Z",
       "Glassy body", fill=BODY_GRAD, stroke=INK, strokeWidth=6, opacity=88)
# inner translucency: plate shows faintly through her lower half
d.shape("ellipse", "Glassy core", x=420, y=470, width=160, height=150,
        fill="#F2EFD0", opacity=30, stroke=NONE)
d.path("M392,560 C430,610 570,610 608,560 C570,640 430,640 392,560 Z",
       "Glassy under-shadow", fill="#8A8A58", opacity=35, stroke=NONE)
# crown dimple + stem + leaf
d.path("M470,322 C478,338 522,338 530,322", "Crown dimple", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round", opacity=70)
d.path("M500,326 C498,300 506,282 520,268", "Stem", fill=NONE,
       stroke="#6E5844", strokeWidth=8, cap="round")
d.path("M520,272 C556,252 590,258 600,284 C570,300 536,296 520,272 Z",
       "Leaf", fill=LEAF_GRAD, stroke=INK, strokeWidth=4, join="round")
# body highlight
d.shape("ellipse", "Body hi", x=405, y=360, width=120, height=54,
        fill="#FFFFFF", opacity=25, stroke=NONE)

# --- face: meticulous yet anxious ----------------------------------------------
# left eye wide, right eye narrowed to an inspecting squint
d.shape("ellipse", "Eye L white", x=432, y=420, width=34, height=40,
        fill="#FDFBEE", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Eye L pupil", x=444, y=434, width=11, height=14,
        fill=INK, stroke=NONE)
d.path("M528,438 C538,430 556,430 566,438", "Eye R squint", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
# anxious raised brows
d.path("M428,404 C440,394 458,392 468,398", "Brow L", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.path("M530,398 C544,390 562,392 570,400", "Brow R", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
# tight worried mouth
d.path("M470,486 C482,478 518,478 530,486", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
# sweat bead at the temple
d.path("M618,398 C630,412 632,426 622,434 C612,426 610,412 618,398 Z",
       "Sweat bead", fill="#CDE8E4", stroke=INK, strokeWidth=3, opacity=85)

# --- arms reaching around the clipboard ----------------------------------------
d.path("M382,520 C350,545 342,575 352,600", "Arm L", fill=NONE,
       stroke="#C9C288", strokeWidth=16, cap="round")
d.path("M618,520 C650,545 658,575 648,600", "Arm R", fill=NONE,
       stroke="#C9C288", strokeWidth=16, cap="round")

# --- the translucent clipboard: ALPHA BATCH ONLY --------------------------------
# glass panel
d.shape("rectangle", "Clipboard glass", x=372, y=520, width=256, height=196,
        fill=GLASS, opacity=42, stroke=INK, strokeWidth=5, radius=10)
# panel highlight
d.path("M386,540 L430,540 L396,690 L386,690 Z", "Glass sheen",
       fill="#FFFFFF", opacity=20, stroke=NONE)
# clip at the top
d.shape("rectangle", "Clip", x=462, y=508, width=76, height=26,
        fill="#8A9A8E", stroke=INK, strokeWidth=4, radius=8)
d.shape("ellipse", "Clip rivet", x=494, y=516, width=12, height=12,
        fill="#D8E4CC", stroke=INK, strokeWidth=3)
# header
d.text("ALPHA BATCH ONLY", "Clipboard header", x=500, y=566, size=19,
       font="Virelai Sans", color="#2E4A38", justify="center")
d.path("M398,578 L602,578", "Header rule", fill=NONE, stroke="#2E4A38",
       strokeWidth=2, opacity=70)
# checklist rows: ticked boxes + ruled lines
for i in range(3):
    y = 596 + i*30
    d.shape("rectangle", f"Box {i+1}", x=398, y=y, width=18, height=18,
            fill="#F4FBF0", opacity=70, stroke="#2E4A38", strokeWidth=3, radius=3)
    d.path(f"M401,{y+9} L407,{y+14} L414,{y+4}", f"Tick {i+1}", fill=NONE,
           stroke="#3E7A4E", strokeWidth=3, cap="round")
    d.path(f"M426,{y+9} L{'596' if i < 2 else '520'},{y+9}", f"Line {i+1}",
           fill=NONE, stroke="#4A6858", strokeWidth=3, opacity=60, cap="round")
# hands gripping the panel edges
d.shape("ellipse", "Palm L", x=344, y=586, width=30, height=24,
        fill="#D6D09A", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Palm R", x=626, y=586, width=30, height=24,
        fill="#D6D09A", stroke=INK, strokeWidth=4)

# --- annotations escaping the panel ---------------------------------------------
d.shape("ellipse", "Note puff 1", x=640, y=470, width=18, height=13,
        fill="#EAF3DE", opacity=55, stroke=NONE)
d.shape("ellipse", "Note puff 2", x=668, y=444, width=12, height=9,
        fill="#EAF3DE", opacity=40, stroke=NONE)

# --- captions -------------------------------------------------------------------
d.text("GLASSY MACCHECKFACE", "Name", x=500, y=930, size=56, font="Virelai Sans",
       color="#DCE8D4", justify="center")
r = d.text("QA INSPECTOR", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#9AB8A0", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("219.glassy-maccheckface-V1R00")
