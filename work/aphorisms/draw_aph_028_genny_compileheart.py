#!/usr/bin/env python3
"""APH-028 Genny Compileheart — motivational-poster aphorism plate V1R00.
BUILD SUCCESS poster energy: inside the gilt card, a factory conveyor
ships a sealed box labeled ITSELF — and the belt loops under itself to
feed the box straight back into its own input. On the line, two compiled
components sit back-to-back across a dead gap, connector ports facing
away, link line cut mid-span. Steel + safety amber, warm ink. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("APH-028 Genny Compileheart — Motivational Poster", 1000, 1000)

INK = "#0E1214"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1A2228"}, {"offset": 1, "color": "#080C10"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#36505C"}, {"offset": 0.7, "color": "#1C2C34"},
    {"offset": 1, "color": "#0C1418"}]}}
POSTER_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#20262B"}, {"offset": 1, "color": "#0E1113"}]}}
BELT_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4A5058"}, {"offset": 1, "color": "#2C3136"}]}}
COMP_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7A8794"}, {"offset": 1, "color": "#49525C"}]}}
BOX_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#C9A365"}, {"offset": 1, "color": "#8A6A38"}]}}
GOLD = "#C8A858"
FRAME = "#B8AC8A"
HEAD = "#EDE8D8"
PUNCH = "#D0CAB8"
CREAM = "#EDE8D8"
FAINT = "#8898A0"
AMBER = "#E8A850"
LED_G = "#4CE87A"
DEAD = "#E85A4A"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#4E7078", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#A8CCD0", strokeWidth=3, opacity=35)
d.shape("ellipse", "Patina 1", x=200, y=170, width=200, height=110,
        fill="#3E5C66", opacity=20, stroke=NONE)
d.shape("ellipse", "Patina 2", x=620, y=620, width=200, height=110,
        fill="#3E5C66", opacity=16, stroke=NONE)
for i, (x, y, w) in enumerate([(215, 280, 7), (790, 255, 8), (165, 480, 6),
                               (838, 475, 7), (250, 655, 6), (755, 665, 7)]):
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#5C7A80", opacity=35, stroke=NONE)

# --- the poster card -------------------------------------------------------------
PX, PY, PW, PH = 220, 150, 560, 440
d.shape("rectangle", "Poster shadow", x=PX + 8, y=PY + 10, width=PW,
        height=PH, fill="#000000", opacity=35, stroke=NONE)
d.shape("rectangle", "Poster", x=PX, y=PY, width=PW, height=PH,
        fill=POSTER_GRAD, stroke="#2E3438", strokeWidth=4)
d.shape("rectangle", "Frame outer", x=PX + 16, y=PY + 16,
        width=PW - 32, height=PH - 32, fill=NONE, stroke=FRAME,
        strokeWidth=2, opacity=80)
d.shape("rectangle", "Frame inner", x=PX + 24, y=PY + 24,
        width=PW - 48, height=PH - 48, fill=NONE, stroke=GOLD,
        strokeWidth=1.5, opacity=60)

# headline — maximum motivational energy
r = d.text("BUILD SUCCESS", "Headline", x=500, y=PY + 64,
           size=36, font="Virelai Sans", color=HEAD, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "headline tracking", ids=[r["id"]], tracking=70)
# rule + diamond under the headline
d.path("M355,244 L472,244 M528,244 L645,244", "Headline rules", fill=NONE,
       stroke=GOLD, strokeWidth=2, opacity=80)
d.path(rot_rect_path(500, 244, 11, 11, 45), "Headline diamond",
       fill=GOLD, opacity=85, stroke=NONE)

# --- the scene: factory floor glow ----------------------------------------------------
d.shape("ellipse", "Floor glow", x=330, y=330, width=340, height=120,
        fill=AMBER, opacity=12, stroke=NONE)

# --- conveyor belt + the loop that feeds it -------------------------------------------
BELT_Y, BELT_H = 432, 26
BELT_X0, BELT_X1 = 292, 708
# return loop: from the output end, down and back underneath to the input
d.path(f"M{BELT_X1},{BELT_Y + BELT_H} "
       f"C{BELT_X1 + 20},{BELT_Y + 62} {BELT_X1 - 60},{BELT_Y + 78} "
       f"{BELT_X0 + 200},{BELT_Y + 78} "
       f"C{BELT_X0 + 60},{BELT_Y + 78} {BELT_X0 + 8},{BELT_Y + 66} "
       f"{BELT_X0 + 4},{BELT_Y + BELT_H + 6}", "Return loop",
       fill=NONE, stroke="#5A626C", strokeWidth=8, cap="round",
       opacity=90)
# chevrons on the return run, pointing back toward the input
for i, cx in enumerate([620, 540, 460, 380]):
    cy = BELT_Y + 74
    d.path(f"M{cx + 8},{cy - 5} L{cx},{cy + 1} L{cx + 8},{cy + 7}",
           f"Return chevron {i+1}", fill=NONE, stroke=AMBER,
           strokeWidth=2.5, cap="round", opacity=70)
# the belt itself
d.shape("rectangle", "Belt", x=BELT_X0, y=BELT_Y,
        width=BELT_X1 - BELT_X0, height=BELT_H, radius=6,
        fill=BELT_GRAD, stroke="#1C2024", strokeWidth=3)
# rollers
for i in range(9):
    rx = BELT_X0 + 22 + i * 47
    d.shape("ellipse", f"Roller {i+1}", x=rx - 6, y=BELT_Y + 7,
            width=12, height=12, fill="#23272C", stroke="#5A626C",
            strokeWidth=2)
# drive direction ticks on the belt, toward output
for i, cx in enumerate([330, 420, 510, 600]):
    d.path(f"M{cx},{BELT_Y + 8} L{cx + 8},{BELT_Y + 13} L{cx},{BELT_Y + 18}",
           f"Belt tick {i+1}", fill=NONE, stroke="#707A84",
           strokeWidth=2, cap="round", opacity=60)
# support legs
for i, lx in enumerate([BELT_X0 + 30, BELT_X1 - 42]):
    d.shape("rectangle", f"Leg {i+1}", x=lx, y=BELT_Y + BELT_H,
            width=12, height=26, fill="#2C3136", stroke="#1C2024",
            strokeWidth=2)

# --- two compiled components, back to back across a dead gap ---------------------------
COMP_Y, COMP_H = 386, 46
def component(cx, w, port_side, label):
    x0 = cx - w / 2
    d.shape("ellipse", f"{label} shadow", x=x0 - 4, y=BELT_Y - 6,
            width=w + 8, height=10, fill="#000000", opacity=35,
            stroke=NONE)
    d.shape("rectangle", label, x=x0, y=COMP_Y, width=w, height=COMP_H,
            radius=4, fill=COMP_GRAD, stroke="#22282E", strokeWidth=2.5)
    d.path(f"M{x0 + 6},{COMP_Y + 6} L{x0 + w - 6},{COMP_Y + 6}",
           f"{label} sheen", fill=NONE, stroke="#9AA6B2",
           strokeWidth=2, opacity=55)
    # status LED — powered, smug
    d.shape("ellipse", f"{label} LED", x=x0 + w - 14, y=COMP_Y + 10,
            width=6, height=6, fill=LED_G, stroke=NONE)
    # connector port faces AWAY from the gap
    px = x0 - 10 if port_side < 0 else x0 + w
    d.shape("rectangle", f"{label} port", x=px, y=COMP_Y + 16,
            width=10, height=14, fill="#3A424A", stroke="#22282E",
            strokeWidth=2)
    d.shape("ellipse", f"{label} port pin", x=px + 3,
            y=COMP_Y + 20, width=4, height=6, fill=AMBER, opacity=80,
            stroke=NONE)

component(360, 76, -1, "Comp A")
component(520, 76, 1, "Comp B")
# the dead link across the gap: two stubs that never meet
GAP_Y = COMP_Y + 23
d.path("M398,%d L418,%d" % (GAP_Y, GAP_Y), "Dead link A", fill=NONE,
       stroke=DEAD, strokeWidth=3, cap="round", opacity=75)
d.path("M482,%d L462,%d" % (GAP_Y, GAP_Y), "Dead link B", fill=NONE,
       stroke=DEAD, strokeWidth=3, cap="round", opacity=75)
# frayed ends + a refusal spark hanging in the silence
d.path("M418,%d L424,%d M462,%d L456,%d" % (GAP_Y - 3, GAP_Y, GAP_Y - 3, GAP_Y),
       "Frayed ends", fill=NONE, stroke=DEAD, strokeWidth=2,
       cap="round", opacity=60)
d.path("M434,%d L440,%d L446,%d L452,%d" % (GAP_Y + 4, GAP_Y - 6,
       GAP_Y + 4, GAP_Y - 6), "Refusal spark", fill=NONE, stroke=AMBER,
       strokeWidth=2, cap="round", opacity=65)
# each component mutters outward — away from the other
d.text("...", "Comp A mutter", x=330, y=COMP_Y - 12, size=14,
       font="Source Sans 3", color=FAINT, justify="center")
d.text("...", "Comp B mutter", x=550, y=COMP_Y - 12, size=14,
       font="Source Sans 3", color=FAINT, justify="center")

# --- the product: a sealed box labeled ITSELF, already at output ------------------------
BX, BY, BW2, BH2 = 614, 366, 88, 66
d.shape("ellipse", "Box shadow", x=BX - 8, y=BELT_Y - 6,
        width=BW2 + 16, height=11, fill="#000000", opacity=35,
        stroke=NONE)
d.shape("rectangle", "Product box", x=BX, y=BY, width=BW2, height=BH2,
        radius=3, fill=BOX_GRAD, stroke="#5E4622", strokeWidth=2.5)
# closed flaps on top
d.path(f"M{BX},{BY} L{BX + BW2 / 2},{BY - 14} L{BX + BW2},{BY}",
       "Box flaps", fill="#B08D50", stroke="#5E4622", strokeWidth=2)
d.path(f"M{BX + BW2 / 2},{BY - 14} L{BX + BW2 / 2},{BY}",
       "Flap seam", fill=NONE, stroke="#5E4622", strokeWidth=1.5)
# shipping tape down the face
d.shape("rectangle", "Tape", x=BX + BW2 / 2 - 6, y=BY + 4, width=12,
        height=BH2 - 8, fill="#E4D4AE", opacity=45, stroke=NONE)
# the label
d.shape("rectangle", "Box label", x=BX + 14, y=BY + 22, width=BW2 - 28,
        height=22, fill="#EFE6CE", stroke="#8A7448", strokeWidth=1.5)
d.text("ITSELF", "Label text", x=BX + BW2 / 2, y=BY + 37, size=11,
       font="Source Sans 3", color="#4A3A22", justify="center")

# --- punchline sub-caption -------------------------------------------------------------
r = d.text("THE SYSTEM REQUIRES ITSELF TO EXIST", "Punchline 1", x=500,
           y=PY + PH - 58, size=19, font="Virelai Sans", color=PUNCH,
           justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "punch1 tracking", ids=[r["id"]], tracking=80)
r = d.text("BEFORE IT CAN BE CREATED.", "Punchline 2", x=500,
           y=PY + PH - 32, size=19, font="Virelai Sans", color=PUNCH,
           justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "punch2 tracking", ids=[r["id"]], tracking=80)

# --- flourish on the plate below the poster ----------------------------------------------
d.path("M415,668 L485,668 M515,668 L585,668", "Flourish rules", fill=NONE,
       stroke=GOLD, strokeWidth=2, opacity=55)
d.path(rot_rect_path(500, 668, 9, 9, 45), "Flourish diamond", fill=GOLD,
       opacity=60, stroke=NONE)

# --- name + role ----------------------------------------------------------------------
d.text("GENNY COMPILEHEART", "Name", x=500, y=905, size=56,
       font="Virelai Sans", color=CREAM, justify="center")
r = d.text("THE SYSTEM REQUIRES ITSELF", "Role", x=500, y=950, size=18,
           font="Virelai Sans", color=FAINT, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=160)

d.finish("aph-028-genny-compileheart-V1R00")
