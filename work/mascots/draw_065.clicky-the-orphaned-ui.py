#!/usr/bin/env python3
"""Clicky the Orphaned UI — mascot portrait V1R00.
A small interface-window mascot reaching for a ghostly FINISH button in
a decommissioned onboarding flow: greyed modal card, stalled progress
bar, stepper dots that will never fill, and the faint concentric
residue of clicks that went nowhere.
1000x1000. Gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Clicky the Orphaned UI — Mascot Portrait", 1000, 1000)

INK = "#201C22"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#0C1016"}, {"offset": 1, "color": "#06080C"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#3A4656"}, {"offset": 0.7, "color": "#242E3A"},
    {"offset": 1, "color": "#121820"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#222E3A"}, {"offset": 1, "color": "#10161E"}]}}
FRAME_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F0E6CC"}, {"offset": 0.7, "color": "#D0C19A"},
    {"offset": 1, "color": "#A89878"}]}}
PANE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#DDE8EE"}, {"offset": 1, "color": "#A8BCC8"}]}}
TITLE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7E7494"}, {"offset": 1, "color": "#565070"}]}}
GHOST = "#BFE8F2"

# --- backdrop + plate -----------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#88A2BC", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#BCD2E4", strokeWidth=3, opacity=40)
for i, (x, y, w) in enumerate([(188,240,8),(804,232,7),(150,518,9),(844,538,8),
                               (252,764,7),(750,752,9),(130,390,6),(864,398,7),
                               (390,110,7),(618,112,8),(338,818,6),(664,820,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#2C3A48", opacity=55, stroke=NONE)

# --- the decommissioned onboarding modal, greyed out ------------------------------
CX0, CY0 = 310, 176   # card top-left; card is 400x390
d.shape("rectangle", "Dead modal", x=CX0, y=CY0, width=400, height=390,
        fill="#A8B8CC", opacity=16, stroke="#5A6E84", strokeWidth=4,
        radius=16)
d.shape("rectangle", "Modal titlebar", x=CX0, y=CY0, width=400, height=44,
        fill="#7E92A8", opacity=25, stroke=NONE, radius=16)
d.shape("rectangle", "Titlebar square-off", x=CX0, y=CY0 + 22, width=400,
        height=22, fill="#7E92A8", opacity=25, stroke=NONE)
t = d.text("SETUP", "Modal title", x=CX0 + 200, y=CY0 + 30, size=15,
           font="Virelai Sans", color="#7E92A8", justify="center")
if t and t.get("id"):
    d.cmd("object.setProps", "title fade", ids=[t["id"]], opacity=60)
# stepper: two dots filled, the rest forever hollow
for i in range(5):
    sx = CX0 + 130 + i * 35
    if i < 2:
        d.shape("ellipse", f"Step {i+1}", x=sx - 8, y=CY0 + 72,
                width=16, height=16, fill="#8FA4BC", opacity=60,
                stroke=NONE)
    else:
        d.shape("ellipse", f"Step {i+1}", x=sx - 8, y=CY0 + 72,
                width=16, height=16, fill=NONE, stroke="#8FA4BC",
                strokeWidth=2.5, opacity=50)
# progress bar stalled mid-flow
d.shape("rectangle", "Progress track", x=CX0 + 60, y=CY0 + 130, width=280,
        height=18, fill="#1E2830", stroke="#4A5A6A", strokeWidth=2,
        radius=9)
d.shape("rectangle", "Progress fill", x=CX0 + 63, y=CY0 + 133, width=118,
        height=12, fill="#6E86A0", opacity=70, stroke=NONE, radius=6)
# greyed body copy that once explained things
for i, (ly, lw) in enumerate([(CY0 + 184, 300), (CY0 + 212, 260),
                              (CY0 + 240, 284)]):
    d.shape("rectangle", f"Copy line {i+1}", x=CX0 + 50, y=ly, width=lw,
            height=10, fill="#7E92A8", opacity=35, stroke=NONE, radius=5)
# a disabled BACK pill, lower right where nobody left to click it
d.shape("rectangle", "Back pill", x=CX0 + 260, y=CY0 + 336, width=96,
        height=34, fill="#3A4654", opacity=55, stroke="#5A6E84",
        strokeWidth=2, radius=17)
t = d.text("BACK", "Back label", x=CX0 + 308, y=CY0 + 358, size=12,
           font="Virelai Sans", color="#7E92A8", justify="center")
if t and t.get("id"):
    d.cmd("object.setProps", "back fade", ids=[t["id"]], opacity=70)

# --- the ghost button: half-departed, still clickable in theory --------------------
GBX, GBY = 648, 420
# click ripples pooling around it — residue of phantom intent
for i, rr in enumerate([56, 78, 102]):
    d.shape("ellipse", f"Ripple {i+1}", x=GBX - rr, y=GBY - rr * 0.62,
            width=rr * 2, height=rr * 1.24, fill=NONE,
            stroke=GHOST, strokeWidth=2, opacity=26 - i * 7,
            dash=[4, 7])
# echo image, drifting off-model
d.shape("rectangle", "Ghost echo", x=GBX - 76, y=GBY - 20, width=180,
        height=62, fill=NONE, stroke=GHOST, strokeWidth=3, opacity=12,
        radius=31)
d.shape("rectangle", "Ghost button", x=GBX - 90, y=GBY - 31, width=180,
        height=62, fill=GHOST, opacity=16, stroke=GHOST, strokeWidth=3,
        dash=[8, 6], radius=31)
t = d.text("FINISH", "Ghost label", x=GBX, y=GBY + 7, size=20,
           font="Virelai Sans", color=GHOST, justify="center")
if t and t.get("id"):
    d.cmd("object.setProps", "ghost fade", ids=[t["id"]], opacity=55)

# --- floor ----------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#080C10",
       strokeWidth=4, opacity=70)
d.shape("ellipse", "Mascot shadow", x=300, y=684, width=210, height=20,
        fill="#04070A", opacity=60, stroke=NONE)

# --- Clicky: a little window that outlived its flow --------------------------------
# feet, tiptoeing toward the button
d.shape("ellipse", "Foot L", x=332, y=656, width=40, height=18,
        fill="#8E8270", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Foot R", x=402, y=656, width=40, height=18,
        fill="#8E8270", stroke=INK, strokeWidth=3)
# left arm hanging, right arm reaching up to the ghost
d.path("M300,540 C278,552 268,572 266,594", "Arm L ink", fill=NONE,
       stroke=INK, strokeWidth=26, cap="round")
d.path("M300,540 C278,552 268,572 266,594", "Arm L", fill=NONE,
       stroke="#A89878", strokeWidth=18, cap="round")
d.path("M462,512 C504,486 542,462 570,438", "Arm R ink", fill=NONE,
       stroke=INK, strokeWidth=26, cap="round")
d.path("M462,512 C504,486 542,462 570,438", "Arm R", fill=NONE,
       stroke="#A89878", strokeWidth=18, cap="round")
d.shape("ellipse", "Hand R", x=560, y=420, width=26, height=24,
        fill="#A89878", stroke=INK, strokeWidth=3)
# window body
d.shape("rectangle", "Window frame", x=292, y=462, width=180, height=196,
        fill=FRAME_GRAD, stroke=INK, strokeWidth=5, radius=14)
d.shape("rectangle", "Title bar", x=292, y=462, width=180, height=34,
        fill=TITLE_GRAD, stroke=INK, strokeWidth=4, radius=14)
d.shape("rectangle", "Title bar square-off", x=292, y=480, width=180,
        height=16, fill=TITLE_GRAD, stroke=NONE)
t = d.text("ONBOARD", "Window title", x=400, y=484, size=13,
           font="Virelai Sans", color="#D8D2E8", justify="center")
if t and t.get("id"):
    d.cmd("object.setProps", "win title fade", ids=[t["id"]], opacity=85)
# traffic dots — all dim except one faint amber
for i, (dx, col, o) in enumerate([(14, "#5A5068", 100),
                                  (30, "#5A5068", 100),
                                  (46, "#C8A44E", 80)]):
    d.shape("ellipse", f"Dot {i+1}", x=302 + dx, y=472, width=10,
            height=10, fill=col, opacity=o, stroke=NONE)
# the pane
d.shape("rectangle", "Pane", x=306, y=506, width=152, height=110,
        fill=PANE_GRAD, stroke=INK, strokeWidth=3, radius=8)
d.shape("ellipse", "Pane sheen", x=318, y=514, width=60, height=40,
        fill="#FFFFFF", opacity=35, stroke=NONE)
# face on the pane: hopeful, looking up-right at the button
d.shape("ellipse", "Eye L", x=342, y=540, width=20, height=24,
        fill="#2A2226", stroke=NONE)
d.shape("ellipse", "Eye R", x=398, y=540, width=20, height=24,
        fill="#2A2226", stroke=NONE)
d.shape("ellipse", "Glint L", x=348, y=545, width=6, height=6,
        fill="#F4F8FA", stroke=NONE)
d.shape("ellipse", "Glint R", x=404, y=545, width=6, height=6,
        fill="#F4F8FA", stroke=NONE)
d.path("M338,528 C346,522 356,521 364,525", "Brow L", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.path("M396,525 C404,521 414,522 422,528", "Brow R", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.path("M362,584 C370,590 382,590 390,583", "Hopeful mouth", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
# stale click residue on the pane itself
d.path("M330,596 m-7,0 a7,7 0 1,0 14,0 a7,7 0 1,0 -14,0", "Pane click ring",
       fill=NONE, stroke="#8A9EAC", strokeWidth=1.5, opacity=40,
       dash=[2, 4])

# --- captions ----------------------------------------------------------------------
d.text("CLICKY THE ORPHANED UI", "Name", x=500, y=930, size=50,
       font="Virelai Sans", color="#E0EAF2", justify="center")
r = d.text("RECORDER OF PHANTOM INTENT", "Role", x=500, y=968, size=22,
           font="Virelai Sans", color="#9EB8CC", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=160)

d.finish("065.clicky-the-orphaned-ui-V1R00")
