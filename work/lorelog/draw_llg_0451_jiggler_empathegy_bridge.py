#!/usr/bin/env python3
"""LLG-0451 Jiggler Economics & Empathegy Curve-Coherence — V1R00. A mouse
jiggler vibrating beside a dashboard with a smooth rising green curve; faint
human silhouette in the background, not touching the mouse; Serotonin Sam as
mascot of the curve, chart under one arm, sticker in the other. 1000x1000."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("LLG-0451 Jiggler Empathegy Bridge", 1000, 1000)

INK = "#33271E"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#20241E"}, {"offset": 1, "color": "#0D100C"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#D9C9A4"}, {"offset": 0.72, "color": "#A8916B"},
    {"offset": 1, "color": "#6E5B40"}]}}
SCR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#26343C"}, {"offset": 1, "color": "#131C22"}]}}
BRASS_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#C9A86A"}, {"offset": 1, "color": "#8A6A3E"}]}}
SAM_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F2C98A"}, {"offset": 1, "color": "#C98A4E"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#54462E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#EFE3C4", strokeWidth=3, opacity=55)
d.shape("ellipse", "Patina 1", x=170, y=170, width=240, height=150,
        fill="#8C7852", opacity=25, stroke=NONE)
d.shape("ellipse", "Patina 2", x=600, y=690, width=250, height=140,
        fill="#8C7852", opacity=22, stroke=NONE)
for i, (x, y, w) in enumerate([(210,310,8),(780,250,7),(160,550,9),(830,550,8),
                               (260,780,7),(750,760,9),(140,430,6),(860,420,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#6E5A3C", opacity=40, stroke=NONE)

# --- faint human silhouette, background, never touching the mouse -------------
# standing figure: head + shoulders, translucent dark
d.shape("ellipse", "Human head", x=368, y=352, width=64, height=74,
        fill="#2A2118", opacity=16, stroke=NONE)
d.path("M340,470 C340,430 460,430 460,470 L470,640 C470,660 330,660 330,640 Z",
       "Human shoulders", fill="#2A2118", opacity=14, stroke=NONE)
# the silhouette's dead arm hangs — it does not reach the mouse
d.path("M452,500 C460,540 458,580 450,610", "Human arm", fill=NONE,
       stroke="#2A2118", strokeWidth=20, opacity=12, cap="round")

# --- dashboard with the smooth rising curve ------------------------------------
d.shape("rectangle", "Dashboard", x=470, y=300, width=380, height=250,
        radius=10, fill=SCR_GRAD, stroke=INK, strokeWidth=5)
d.shape("rectangle", "Dash stand", x=648, y=550, width=26, height=24,
        fill="#2E2620", stroke=NONE)
# axes
d.path("M505,510 L505,330 M505,510 L820,510", "Dash axes", fill=NONE,
       stroke="#5A6E62", strokeWidth=3)
for i, ty in enumerate([360, 405, 450, 495]):
    d.path(f"M498,{ty} L508,{ty}", f"Tick {i+1}", fill=NONE,
           stroke="#5A6E62", strokeWidth=2)
# the curve — smooth, upward, glowing green
CURVE = "M510,492 C580,488 640,470 690,436 C740,402 780,362 818,336"
d.path(CURVE, "Curve glow", fill=NONE, stroke="#5FC98A", strokeWidth=18,
       opacity=22, cap="round")
d.path(CURVE, "Curve", fill=NONE, stroke="#7ED9A2", strokeWidth=6, cap="round")
# arrowhead at the curve's end
d.path("M818,336 L800,342 L812,358 Z", "Curve arrow", fill="#7ED9A2",
       stroke=NONE)
# data dots along the curve
for i, t in enumerate([0.15, 0.4, 0.65, 0.9]):
    # coarse bezier interpolation for dot placement
    x = 510 + (818 - 510) * t
    y = 492 - (492 - 336) * (t ** 1.35)
    d.shape("ellipse", f"Dot {i+1}", x=x - 5, y=y - 5, width=10, height=10,
            fill="#B8F0CC", stroke=NONE)
d.text("E M P A T H E G Y", "Dash label", x=615, y=290, size=13,
       font="Virelai Sans", color="#7ED9A2", justify="center")

# --- Serotonin Sam: mascot of the curve, chart-armed, holding a sticker --------
# perched on the dashboard's top-right corner
d.path("M762,196 Q800,178 838,196 L838,292 Q800,308 762,292 Z", "Sam body",
       fill=SAM_GRAD, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Sam eye L", x=786, y=228, width=11, height=14,
        fill="#2A1C16", stroke=NONE)
d.shape("ellipse", "Sam eye R", x=812, y=228, width=11, height=14,
        fill="#2A1C16", stroke=NONE)
d.shape("ellipse", "Sam glint L", x=789, y=231, width=3, height=3,
        fill="#FFFFFF", opacity=85, stroke=NONE)
d.shape("ellipse", "Sam glint R", x=815, y=231, width=3, height=3,
        fill="#FFFFFF", opacity=85, stroke=NONE)
d.path("M784,258 Q800,270 818,256", "Sam grin", fill=NONE, stroke=INK,
       strokeWidth=4, cap="round")
# chart under the left arm — Sam is chart-armed
d.shape("rectangle", "Sam chart", x=700, y=238, width=62, height=48,
        radius=5, fill="#EDE4CC", stroke=INK, strokeWidth=3)
d.path("M706,274 L728,262 L738,266 L756,248", "Sam chart line", fill=NONE,
       stroke="#2A6B4C", strokeWidth=3, cap="round")
d.path("M764,250 Q752,258 746,264", "Sam arm L", fill=NONE,
       stroke="#C98A4E", strokeWidth=8, cap="round")
# sticker held up in the right hand: little star on a peel-back square
d.shape("rectangle", "Sticker", x=836, y=214, width=40, height=40,
        radius=6, fill="#F2E4B8", stroke=INK, strokeWidth=3)
d.path("M856,222 L859,229 L866,229 L860,233 L862,240 L856,236 L850,240 "
       "L852,233 L846,229 L853,229 Z", "Sticker star", fill="#E8A33D",
       stroke=NONE)
d.path("M836,248 L872,214", "Sticker peel", fill=NONE, stroke="#C9BA96",
       strokeWidth=2)
d.path("M838,248 Q842,240 844,234", "Sam arm R", fill=NONE,
       stroke="#C98A4E", strokeWidth=8, cap="round")

# --- the jiggler: small mechanical device, vibrating, mouse on top -------------
# machine base
d.shape("rectangle", "Jiggler base", x=196, y=672, width=170, height=96,
        radius=12, fill=BRASS_GRAD, stroke=INK, strokeWidth=5)
d.shape("rectangle", "Jiggler faceplate", x=212, y=690, width=60, height=40,
        radius=5, fill="#5A4230", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Jiggler lamp", x=222, y=700, width=14, height=14,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#FFDF8A"}, {"offset": 1, "color": "#C9862E"}]}},
        stroke=INK, strokeWidth=2)
d.path("M244,706 L262,706 M244,714 L256,714", "Jiggler gauge", fill=NONE,
       stroke="#C9BA96", strokeWidth=3, cap="round")
# feet
d.shape("rectangle", "Jiggler foot L", x=214, y=768, width=28, height=14,
        radius=4, fill="#4A3524", stroke=NONE)
d.shape("rectangle", "Jiggler foot R", x=320, y=768, width=28, height=14,
        radius=4, fill="#4A3524", stroke=NONE)
# piston column up to the mouse platform
d.shape("rectangle", "Piston", x=272, y=620, width=20, height=56,
        fill="#6E5B40", stroke=INK, strokeWidth=3)
d.shape("rectangle", "Platform", x=238, y=610, width=88, height=14,
        radius=5, fill="#4A3524", stroke=INK, strokeWidth=3)
# the mouse on the platform
MOUSE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#D8D4CC"}, {"offset": 1, "color": "#8E8A82"}]}}
d.path("M252,610 C252,576 312,576 312,610 Z", "Mouse", fill=MOUSE_GRAD,
       stroke=INK, strokeWidth=4)
d.path("M282,578 L282,610", "Mouse split", fill=NONE, stroke=INK,
       strokeWidth=2)
d.shape("ellipse", "Mouse wheel", x=278, y=588, width=8, height=14,
        fill="#4A3524", stroke=NONE)
# cable curling away
d.path("M312,600 C350,596 370,610 388,622", "Mouse cable", fill=NONE,
       stroke=INK, strokeWidth=3, cap="round")
# vibration: double ghost + motion arcs around the device
d.path("M246,602 C246,570 306,570 306,602 Z", "Mouse ghost", fill=NONE,
       stroke="#8A7A5E", strokeWidth=3, opacity=45)
for i, (ax, ay, sweep) in enumerate([(216, 560, -1), (206, 600, -1),
                                      (240, 548, -1)]):
    x1 = ax + (24 * sweep)
    d.path(f"M{ax},{ay} Q{ax + 14*sweep},{ay - 14} {x1},{ay - 30}",
           f"Jiggle arc {i+1}", fill=NONE, stroke="#8A7A5E", strokeWidth=4,
           opacity=55, cap="round")
# vibration blur under the piston
d.shape("ellipse", "Jiggler blur", x=250, y=640, width=64, height=20,
        fill="#6E5B40", opacity=35, stroke=NONE)

# --- name + role -----------------------------------------------------------------
d.text("JIGGLER ECONOMICS", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#EFE3C4", justify="center")
d.text("C U R V E   E A T S   T H E   H U M A N", "Role", x=500, y=968,
       size=20, font="Virelai Sans", color="#B8A67E", justify="center")

d.finish("llg-0451-jiggler-empathegy-bridge-V1R00")
