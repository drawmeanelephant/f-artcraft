#!/usr/bin/env python3
"""Forbiddy Noentry — mascot portrait V1R00. Permission Denial Oracle:
a stocky, professionally certain barring-figure planted in a dark doorway
under a brass '403' placard, one palm raised in settled refusal, the other
hand cradling a clipboard of crossed-out names (one line still pending —
she is considering it, and the answer is no). Velvet rope sagging across
the threshold between brass stanchions. Oxblood and brass. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Forbiddy Noentry — Mascot Plate", 1000, 1000)

INK = "#331B20"   # warm dark ink, never black
BG_GRAD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000], "stops": [
    {"offset": 0, "color": "#220D12"}, {"offset": 1, "color": "#0B0508"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#CF9C82"}, {"offset": 0.6, "color": "#9A5B4E"},
    {"offset": 1, "color": "#63383F"}]}}
DOOR_GRAD = {"gradient": {"kind": "linear", "start": [0, 170], "end": [0, 690], "stops": [
    {"offset": 0, "color": "#3A2830"}, {"offset": 1, "color": "#1C1218"}]}}
BODY_GRAD = {"gradient": {"kind": "linear", "start": [0, 360], "end": [0, 730], "stops": [
    {"offset": 0, "color": "#4E3444"}, {"offset": 0.55, "color": "#33222E"},
    {"offset": 1, "color": "#1E1420"}]}}
GLOW_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E8B878", "opacity": 0.5},
    {"offset": 0.55, "color": "#E8B878", "opacity": 0.18},
    {"offset": 1, "color": "#E8B878", "opacity": 0}]}}
PAPER_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F0E4CC"}, {"offset": 1, "color": "#CBB894"}]}}
BRASS = "#C89A4E"
ROPE = "#7E1F2E"
RED = "#A8342E"

PCX, PCY, PR = 500, 460, 420

def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

# --- backdrop + plate ------------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#8A4A44", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#2E181E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8C4AE", strokeWidth=3, opacity=40)
# patina + flecks
d.shape("ellipse", "Patina 1", x=190, y=170, width=240, height=150, fill="#B87A68", opacity=15, stroke=NONE)
d.shape("ellipse", "Patina 2", x=600, y=630, width=240, height=140, fill="#6E4048", opacity=18, stroke=NONE)
for i, (x, y, w) in enumerate([(220,360,6),(780,330,5),(190,580,7),(820,590,6),(260,760,5),
                               (740,770,6),(160,470,5),(850,470,4),(440,140,5),(640,160,6),
                               (330,170,4),(700,240,5),(190,660,4),(560,120,4)]):
    assert on_disc(x, y, 12), (x, y)
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#F0D4C0", opacity=45, stroke=NONE)

# --- the doorway ----------------------------------------------------------------------
# warm glow leaking around the door she occupies
d.shape("ellipse", "Door glow", x=300, y=240, width=400, height=480,
        fill=GLOW_GRAD, stroke=NONE)
# frame and door
d.shape("rectangle", "Door frame", x=366, y=156, width=268, height=536, radius=8,
        fill="#3E2C30", stroke=INK, strokeWidth=5)
d.shape("rectangle", "Door", x=388, y=178, width=224, height=506, radius=4,
        fill=DOOR_GRAD, stroke=INK, strokeWidth=3)
# recessed panels
d.shape("rectangle", "Panel upper", x=408, y=200, width=184, height=190, radius=6,
        fill=NONE, stroke="#4A343A", strokeWidth=3, opacity=80)
d.shape("rectangle", "Panel lower", x=408, y=430, width=184, height=220, radius=6,
        fill=NONE, stroke="#4A343A", strokeWidth=3, opacity=80)
# doorknob she will never let you turn
d.shape("ellipse", "Doorknob", x=576, y=420, width=22, height=22,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#E8C87E"}, {"offset": 1, "color": "#8A6230"}]}},
        stroke=INK, strokeWidth=2.5)
# the placard: form 403
d.shape("rectangle", "Plaque shadow", x=448, y=224, width=112, height=52, radius=8,
        fill="#120C0E", opacity=50, stroke=NONE)
d.shape("rectangle", "Plaque", x=444, y=220, width=112, height=52, radius=8,
        fill={"gradient": {"kind": "linear", "start": [0, 220], "end": [0, 272], "stops": [
            {"offset": 0, "color": "#E4C48A"}, {"offset": 1, "color": "#A87C3E"}]}},
        stroke=INK, strokeWidth=3)
d.text("403", "Plaque text", x=500, y=258, size=30, font="Source Sans 3",
       color="#33240E", justify="center")

# --- Forbiddy, planted in the doorway ----------------------------------------------------
# floor pool of the denied light
d.shape("ellipse", "Floor pool", x=330, y=690, width=340, height=40,
        fill="#E8B878", opacity=18, stroke=NONE)
d.shape("ellipse", "Ground shadow", x=392, y=700, width=220, height=26,
        fill="#120C0E", opacity=35, stroke=NONE)

# left arm up, palm out: the answer reached you before the question
d.path("M448,506 C414,492 388,470 374,442", "Arm L",
       fill=NONE, stroke="#33222E", strokeWidth=30, cap="round")
d.shape("rectangle", "Palm", x=336, y=376, width=64, height=76, radius=16,
        fill="#3E2A38", stroke=INK, strokeWidth=4)
for i, fx in enumerate([340, 356, 372]):
    d.shape("rectangle", f"Finger {i+1}", x=fx, y=360, width=14, height=26, radius=7,
            fill="#3E2A38", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Palm sheen", x=344, y=384, width=28, height=20,
        fill="#E8B878", opacity=22, stroke=NONE)

# body: a stocky, immovable silhouette
d.path("M502,356 C568,356 596,420 592,500 C588,570 584,648 578,706 "
       "C540,724 464,724 426,706 C420,648 416,570 412,500 C408,420 436,356 502,356 Z",
       "Body", fill=BODY_GRAD, stroke=INK, strokeWidth=6)
# warm rim light down the left flank, from the door she denies
d.path("M420,420 C412,480 414,580 424,680", "Rim light",
       fill=NONE, stroke="#D8A86E", strokeWidth=5, opacity=45, cap="round")
d.shape("ellipse", "Crown sheen", x=440, y=372, width=110, height=40,
        fill="#E8B878", opacity=14, stroke=NONE)

# face: heavy even brow, narrow amber eyes that have already decided
d.path("M442,452 L562,450", "Brow", fill=NONE, stroke=INK, strokeWidth=9, cap="round")
for ex in (466, 536):
    d.shape("ellipse", f"Eye {ex}", x=ex - 15, y=462, width=30, height=14,
            fill="#E8C87E", stroke=INK, strokeWidth=3)
    d.shape("ellipse", f"Pupil {ex}", x=ex - 4, y=464, width=8, height=10,
            fill="#241016", stroke=NONE)
# mouth: a short level line — settled
d.path("M478,540 L526,540", "Mouth", fill=NONE, stroke=INK, strokeWidth=5, cap="round")

# right arm down, cradling the clipboard of crossed-out names
d.path("M576,560 C606,576 620,600 624,626", "Arm R",
       fill=NONE, stroke="#33222E", strokeWidth=26, cap="round")
# clipboard tilted against her hip
d.path(rot_rect_path(668, 636, 116, 150, -8), "Clipboard",
       fill="#6A4634", stroke=INK, strokeWidth=4)
d.path(rot_rect_path(668, 636, 92, 118, -8), "Clip paper",
       fill=PAPER_GRAD, stroke=NONE)
d.path(rot_rect_path(668, 556, 44, 22, -8), "Clip",
       fill=BRASS, stroke=INK, strokeWidth=2.5)
# the list: three names struck through, the fourth still pending
for j, (yy, struck) in enumerate([(600, True), (636, True), (672, True), (706, False)]):
    # name squiggle
    pts = []
    for k in range(8):
        px = 626 + k * 11
        py = yy + (3 if k % 2 else -3)
        pts.append((px, py))
    s = "M%d,%d " % pts[0] + " ".join("L%d,%d" % p for p in pts[1:])
    d.path(s, f"Name row {j+1}", fill=NONE, stroke="#6A5638",
           strokeWidth=3.5, opacity=75, cap="round")
    if struck:
        d.path(f"M624,{yy+1} L706,{yy-4}", f"Strike {j+1}",
               fill=NONE, stroke=RED, strokeWidth=4, cap="round")

# --- the velvet rope across the threshold -------------------------------------------------
def stanchion(x):
    d.shape("ellipse", f"Stanchion base {x}", x=x - 34, y=772, width=68, height=22,
            fill="#8A6230", stroke=INK, strokeWidth=3)
    d.shape("rectangle", f"Stanchion pole {x}", x=x - 6, y=676, width=12, height=100,
            fill=BRASS, stroke=INK, strokeWidth=2.5)
    d.shape("ellipse", f"Stanchion ball {x}", x=x - 14, y=656, width=28, height=28,
            fill={"gradient": {"kind": "radial", "stops": [
                {"offset": 0, "color": "#F0D89A"}, {"offset": 1, "color": "#96702E"}]}},
            stroke=INK, strokeWidth=2.5)

# rope sags between the posts; draw it before the ball tops
d.path("M292,690 C390,788 610,788 708,690", "Velvet rope",
       fill=NONE, stroke=ROPE, strokeWidth=15, cap="round")
d.path("M292,686 C390,784 610,784 708,686", "Rope highlight",
       fill=NONE, stroke="#B03A4A", strokeWidth=5, cap="round", opacity=70)
stanchion(292)
stanchion(708)
for x, y in [(258, 794), (326, 794), (674, 794), (742, 794)]:
    assert on_disc(x, y, 4), (x, y)

# --- name + role ----------------------------------------------------------------------------
d.text("FORBIDDY NOENTRY", "Name", x=500, y=930, size=58, font="Virelai Sans",
       color="#F0D4BC", justify="center")
d.text("PERMISSION DENIAL ORACLE", "Role", x=500, y=968, size=23, font="Virelai Sans",
       color="#C48A74", justify="center")
doc = d.call("inspect_document", {"kind": "Type"}, "inspect type")
for n in (doc or {}).get("nodes", []):
    if str(n.get("name", "")) == "Role":
        d.call("run_command", {"command": "text.setStyle",
               "params": {"id": n["id"], "tracking": 250}}, "track role")

d.finish("010.forbiddy-noentry-V1R00")
