#!/usr/bin/env python3
"""Recourse Cushion — mascot portrait V1R00.
A plump tufted cushion absorbing a COMPLAINT form mid-sink, rage lines
dissolving into its padding. Behind: a wall built of marshmallows; to the
right, sponge stairs sag their way up to a small locked door. The appeal
path exists. It arrives nowhere fast. 1000x1000.
Gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Recourse Cushion — Mascot Portrait", 1000, 1000)

INK = "#261C20"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1C161E"}, {"offset": 1, "color": "#0B080C"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#948478"}, {"offset": 0.7, "color": "#67584A"},
    {"offset": 1, "color": "#332A22"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4E4234"}, {"offset": 1, "color": "#211A12"}]}}
MALLOW_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F2E8D8"}, {"offset": 0.8, "color": "#DACBB2"},
    {"offset": 1, "color": "#B8A68C"}]}}
SPONGE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#EAC98C"}, {"offset": 1, "color": "#B8925A"}]}}
DOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4A3A4C"}, {"offset": 1, "color": "#2A2030"}]}}
CUSHION_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#CE8E9C"}, {"offset": 0.72, "color": "#A66673"},
    {"offset": 1, "color": "#7A4852"}]}}
PAPER_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F0E7D2"}, {"offset": 1, "color": "#CDBFA2"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#B09A7E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#ECDCBE", strokeWidth=3, opacity=55)

# --- the marshmallow wall -------------------------------------------------------
for row, (y, xs) in enumerate([(150, [206, 318, 430, 542, 654]),
                               (216, [150, 262, 374, 486, 598, 710]),
                               (282, [140, 252, 364, 476, 588, 700]),
                               (348, [196, 308, 420, 532, 644, 756]),
                               (414, [140, 252, 364, 476, 588, 700])]):
    for i, x in enumerate(xs):
        o = 85 - ((row + i) % 3) * 12
        d.shape("rectangle", f"Mallow {row+1}.{i+1}", x=x, y=y,
                width=104, height=60, fill=MALLOW_GRAD, stroke=NONE,
                radius=26, opacity=o)

# --- the locked door, top right ---------------------------------------------------
d.shape("rectangle", "Door", x=716, y=298, width=92, height=128,
        fill=DOOR_GRAD, stroke=INK, strokeWidth=5, radius=6)
d.path("M736,298 L736,426 M788,298 L788,426", "Door planks", fill=NONE,
       stroke="#1E1622", strokeWidth=3, opacity=60)
# padlock: shackle + body, centered on the door
d.path("M748,352 C748,336 776,336 776,352", "Shackle", fill=NONE,
       stroke="#D9B25E", strokeWidth=8, cap="round")
d.shape("rectangle", "Padlock", x=742, y=350, width=40, height=36,
        fill="#D9B25E", stroke=INK, strokeWidth=4, radius=8)
d.path("M762,362 C766,362 769,365 769,369 C769,372 767,374 765,375 L766,380 "
       "L758,380 L759,375 C757,374 755,372 755,369 C755,365 758,362 762,362",
       "Keyhole", fill="#3A2C14", stroke=NONE)

# --- sponge stairs descending from the door -----------------------------------------
for i, (x, y, w, h) in enumerate([(700, 420, 96, 66), (672, 492, 112, 66),
                                  (644, 568, 128, 68), (616, 646, 144, 60)]):
    d.shape("rectangle", f"Step {i+1}", x=x, y=y, width=w, height=h,
            fill=SPONGE_GRAD, stroke=INK, strokeWidth=5, radius=24)
    # pores
    for j, (px, py, pw) in enumerate([(x+w*0.28, y+18, 9), (x+w*0.62, y+30, 12),
                                      (x+w*0.8, y+14, 7)]):
        d.shape("ellipse", f"Pore {i+1}.{j+1}", x=px, y=py, width=pw,
                height=pw*0.8, fill="#8A6A38", opacity=55, stroke=NONE)
# middle steps sag under the weight of precedent
d.path("M684,514 C712,526 752,526 780,514", "Step sag", fill=NONE,
       stroke="#8A6A38", strokeWidth=4, opacity=60, cap="round")
d.path("M656,592 C688,606 736,606 768,592", "Step sag 2", fill=NONE,
       stroke="#8A6A38", strokeWidth=4, opacity=60, cap="round")

# --- floor --------------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#120C08",
       strokeWidth=4, opacity=70)

# --- the cushion ----------------------------------------------------------------------
d.shape("ellipse", "Cushion shadow", x=360, y=676, width=290, height=24,
        fill="#0C0806", opacity=45, stroke=NONE)
d.shape("rectangle", "Cushion", x=352, y=496, width=280, height=190,
        fill=CUSHION_GRAD, stroke=INK, strokeWidth=6, radius=64)
# piping
d.shape("rectangle", "Piping", x=368, y=512, width=248, height=158,
        fill=NONE, stroke="#E8B4BE", strokeWidth=3.5, radius=52, opacity=60)
# corner tufts + crease rays
for i, (bx, by) in enumerate([(398, 544), (586, 544), (398, 640), (586, 640)]):
    cx, cy = 492, 591
    d.path(f"M{bx},{by} L{bx + (cx-bx)*0.25:.0f},{by + (cy-by)*0.25:.0f} "
           f"M{bx},{by} L{bx + (cx-bx)*0.18:.0f},{by + (cy-by)*0.1:.0f}",
           f"Crease {i+1}", fill=NONE, stroke="#6E424E", strokeWidth=3,
           cap="round", opacity=65)
    d.shape("ellipse", f"Tuft {i+1}", x=bx-7, y=by-7, width=14, height=14,
            fill="#5E3A46", stroke=INK, strokeWidth=2.5)
# the dent where the complaint is sinking in
d.shape("ellipse", "Absorb dent", x=440, y=486, width=130, height=26,
        fill="#6E424E", opacity=55, stroke=NONE)

# --- the complaint form, half swallowed ----------------------------------------------
d.path(rot_rect_path(505, 448, 96, 122, -16), "Complaint form",
       fill=PAPER_GRAD, stroke=INK, strokeWidth=4)
d.text("COMPLAINT", "Form title", x=496, y=416, size=15, font="Virelai Sans",
       color="#9A3A30", justify="center")
d.path(rot_rect_path(500, 442, 62, 4.5, -16), "Form line 1", fill=NONE,
       stroke="#9A8E76", strokeWidth=3.5, opacity=80)
d.path(rot_rect_path(497, 462, 68, 4.5, -16), "Form line 2", fill=NONE,
       stroke="#9A8E76", strokeWidth=3.5, opacity=80)
d.path(rot_rect_path(494, 482, 50, 4.5, -16), "Form line 3", fill=NONE,
       stroke="#9A8E76", strokeWidth=3.5, opacity=80)
# the cushion's lip folding over the paper's edge — it is being swallowed
d.path("M424,506 C470,490 540,488 584,498", "Cushion lip", fill=NONE,
       stroke="#8A5560", strokeWidth=14, cap="round")

# rage arriving, dissolving: concentric arcs fading into the padding
for i, (x, y, w, h, o) in enumerate([(398,330,200,140,60),(370,306,260,180,38),
                                     (344,286,320,220,20)]):
    d.path(f"M{x},{y+h} A{w/2:.0f},{h/2:.0f} 0 0 1 {x+w},{y+h}",
           f"Force arc {i+1}", fill=NONE, stroke="#D87A6A", strokeWidth=5,
           cap="round", opacity=o)

# --- the face: serene, absorbing ------------------------------------------------------
d.path("M452,582 C460,588 470,588 478,582 M514,582 C522,588 532,588 540,582",
       "Serene eyes", fill=NONE, stroke=INK, strokeWidth=5, cap="round")
d.path("M482,616 C490,622 502,622 510,616", "Soft mouth", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.shape("ellipse", "Blush L", x=434, y=596, width=22, height=12,
        fill="#E8A0AC", opacity=45, stroke=NONE)
d.shape("ellipse", "Blush R", x=534, y=596, width=22, height=12,
        fill="#E8A0AC", opacity=45, stroke=NONE)

# --- settling dust ----------------------------------------------------------------------
for i, (x, y, w) in enumerate([(240,540,5),(300,620,4),(680,300,5),(860,470,4),
                               (210,380,4),(830,600,5),(560,180,5),(340,170,4)]):
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#EADCC2", opacity=40, stroke=NONE)

# --- captions ----------------------------------------------------------------------------
d.text("RECOURSE CUSHION", "Name", x=500, y=930, size=56, font="Virelai Sans",
       color="#F0E4D2", justify="center")
r = d.text("ABSORBER OF OBJECTIONS", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#C2B096", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("262.recourse-cushion-V1R00")
