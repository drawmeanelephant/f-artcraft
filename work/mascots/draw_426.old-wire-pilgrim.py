#!/usr/bin/env python3
"""Old Wire Pilgrim — mascot portrait V1R00. HTTP 426, "Upgrade Required".
Hooded pilgrim walking a sagging rusty copper wire between two poles.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Old Wire Pilgrim — Mascot Portrait", 1000, 1000)

INK = "#3A241C"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2A1C14"}, {"offset": 1, "color": "#140C08"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#EBD9C4"}, {"offset": 0.7, "color": "#C9AD92"},
    {"offset": 1, "color": "#96755C"}]}}
CLOAK_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#8A5238"}, {"offset": 0.7, "color": "#633A26"},
    {"offset": 1, "color": "#462818"}]}}
WOOD_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7E5A3C"}, {"offset": 1, "color": "#523A26"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#8A6A4C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F2E4CE", strokeWidth=3, opacity=55)
# hazy ground band hugging the disc's lower arc
d.path("M168,700 C330,672 670,672 832,700 A420,420 0 0 1 168,700 Z",
       "Ground haze", fill="#7A5C42", opacity=30, stroke=NONE)
for i, (x, y, w) in enumerate([(230,225,7),(770,225,6),(180,430,6),(825,440,7),
                               (350,160,6),(650,155,7),(140,560,6),(855,560,6)]):
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#8A6A4C", opacity=40, stroke=NONE)

# --- poles ----------------------------------------------------------------------
for side, x in [("L", 206), ("R", 774)]:
    d.shape("rectangle", f"Pole {side}", x=x, y=388, width=22, height=352,
            radius=6, fill=WOOD_GRAD, stroke=INK, strokeWidth=4)
    d.shape("ellipse", f"Pole cap {side}", x=x-6, y=378, width=34, height=18,
            fill="#3E3A34", stroke=INK, strokeWidth=4)
    d.path(f"M{x+3},{388+28} L{x+19},{388+28} M{x+3},{388+64} L{x+19},{388+64}",
           f"Pole bands {side}", fill=NONE, stroke="#3E2C1E", strokeWidth=3, opacity=60)
    # glass insulator pegs
    d.shape("ellipse", f"Insulator {side}", x=x+3, y=396, width=16, height=14,
            fill="#8FBFB2", stroke=INK, strokeWidth=3)

# --- the old copper wires ---------------------------------------------------------
d.path("M222,402 Q500,616 778,402", "Wire main",
       fill=NONE, stroke="#B87333", strokeWidth=5.5, cap="round")
d.path("M222,432 Q500,640 778,432", "Wire lower",
       fill=NONE, stroke="#9A6228", strokeWidth=4, cap="round", opacity=75)
# verdigris patches + rust flecks seated on the main wire's sag curve
def wire_y(x):
    t = (x - 222) / 556.0
    return (1 - t) ** 2 * 402 + 2 * t * (1 - t) * 616 + t * t * 402
for i, x in enumerate([290, 360, 440, 560, 660]):
    y = wire_y(x)
    d.path(f"M{x-9},{y:.0f} L{x+9},{y+2:.0f}", f"Verdigris {i+1}",
           fill=NONE, stroke="#5FA88A", strokeWidth=5, opacity=70, cap="round")
# a frayed strand curling off near the right pole
d.path("M700,448 C720,452 736,462 744,478 C748,486 744,492 736,490",
       "Frayed strand", fill=NONE, stroke="#B87333", strokeWidth=3.5, cap="round")

# --- the pilgrim, mid-wire ----------------------------------------------------------
# standing on the sag's low point (~500, 502)
d.shape("ellipse", "Foot shadow", x=478, y=504, width=60, height=10,
        fill="#5E4228", opacity=50, stroke=NONE)
# cloak: broad cone from hood peak to the wire
d.path("M500,318 C460,330 434,380 428,436 C424,472 434,494 456,502 "
       "L470,508 C486,514 514,514 530,508 L544,502 C566,494 576,472 572,436 "
       "C566,380 540,330 500,318 Z", "Cloak", fill=CLOAK_GRAD, stroke=INK, strokeWidth=6, join="round")
# cloak folds + hem lift as he steps
d.path("M462,480 C458,430 466,384 486,352", "Fold L",
       fill=NONE, stroke="#3A2014", strokeWidth=7, opacity=45, cap="round")
d.path("M540,478 C544,432 536,388 518,354", "Fold R",
       fill=NONE, stroke="#3A2014", strokeWidth=6, opacity=40, cap="round")
# face inside the hood: shadowed, eyes out
d.path("M478,352 C484,338 516,338 522,352 C526,368 514,382 500,382 C486,382 474,368 478,352 Z",
       "Hood shadow", fill="#241812", stroke=NONE)
d.shape("ellipse", "Eye L", x=490, y=358, width=9, height=11, fill="#F4E9D2", stroke=NONE)
d.shape("ellipse", "Eye R", x=507, y=358, width=9, height=11, fill="#F4E9D2", stroke=NONE)
# balance staff held horizontally across the chest
d.path("M400,452 L600,436", "Staff", fill=NONE, stroke="#6E4E34",
       strokeWidth=9, cap="round")
d.path("M400,452 L600,436", "Staff ink", fill=NONE, stroke=INK,
       strokeWidth=2.5, cap="round", opacity=60)
# hands gripping the staff
d.shape("ellipse", "Hand L", x=424, y=440, width=26, height=24,
        fill="#D9BFA4", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Hand R", x=556, y=428, width=26, height=24,
        fill="#D9BFA4", stroke=INK, strokeWidth=4)
# boots: one planted on the wire, one lifted mid-step
d.path("M480,506 L494,503 L496,518 L478,518 Z", "Boot back",
       fill="#3E2C1E", stroke=INK, strokeWidth=3, join="round")
d.path("M510,520 C518,513 529,513 535,519 L531,530 L511,528 Z", "Boot front",
       fill="#3E2C1E", stroke=INK, strokeWidth=3, join="round")
# wobble ticks at the staff ends
d.path("M392,444 L384,452 M608,430 L614,422", "Wobble ticks",
       fill=NONE, stroke=INK, strokeWidth=4, cap="round", opacity=50)

# --- name + role ----------------------------------------------------------------------
d.text("OLD WIRE PILGRIM", "Name", x=500, y=930, size=56, font="Virelai Sans",
       color="#F0E2CC", justify="center")
d.text(" ".join("UPGRADE REQUIRED"), "Role", x=500, y=968, size=23, font="Virelai Sans",
       color="#C4A078", justify="center")

d.finish("426.old-wire-pilgrim-V1R00")
