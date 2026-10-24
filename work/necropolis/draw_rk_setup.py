#!/usr/bin/env python3
"""setup.sh — The Provisioner. Necropolis plate V1R00.
A pine crate stenciled OLIVER winched down into the crypt on chains —
wax checksum seal on the lid, manifest nailed to the side, pin b84f636,
verified before burial. 1000x1000. Gradients + translucent shading."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Setup — Necropolis Plate", 1000, 1000)

INK = "#241A12"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#171009"}, {"offset": 1, "color": "#0A0605"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#5A4636"}, {"offset": 0.7, "color": "#352922"},
    {"offset": 1, "color": "#171110"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2E241C"}, {"offset": 1, "color": "#140E0A"}]}}
TIMBER = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5C422C"}, {"offset": 1, "color": "#332216"}]}}
WOOD_TOP = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#C49A66"}, {"offset": 1, "color": "#8A6440"}]}}
WOOD_FRONT = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#B08858"}, {"offset": 1, "color": "#7A5636"}]}}
WOOD_SIDE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6E4C30"}, {"offset": 1, "color": "#4A3020"}]}}
WAX = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#C04434"}, {"offset": 1, "color": "#7A1F18"}]}}
SHAFT = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#0A0705"}, {"offset": 1, "color": "#1E1610"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#8A744E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E4D3B0", strokeWidth=3, opacity=45)
for i, (x, y, w) in enumerate([(193,233,8),(801,230,7),(157,524,9),(837,544,8),
                               (247,766,7),(753,749,9),(133,393,6),(864,391,7),
                               (391,113,7),(613,110,8),(333,823,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#6A563F", opacity=35, stroke=NONE)

# cold light from the world above, following the crate down
d.path("M430,120 L570,120 L660,700 L340,700 Z", "Light shaft",
       fill="#C8D8E8", opacity=7, stroke=NONE)

# --- floor + the open shaft -----------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0E0A06",
       strokeWidth=4, opacity=70)
# shaft mouth cut into the floor
d.shape("ellipse", "Shaft rim", x=308, y=664, width=384, height=104,
        fill="#3E3226", stroke=INK, strokeWidth=5)
d.shape("ellipse", "Shaft dark", x=330, y=676, width=340, height=80,
        fill=SHAFT, stroke="#0E0A06", strokeWidth=4)
d.path("M360,700 C420,742 580,742 640,700", "Shaft throat", fill=NONE,
       stroke="#060402", strokeWidth=8, opacity=80)
# scattered grave goods straw at the rim
for i, (x, y, a) in enumerate([(340,700,-18),(660,695,14),(500,745,4),(390,730,-8)]):
    d.path(f"M{x},{y} L{x+a*2},{y+6}", f"Straw {i+1}", fill=NONE,
           stroke="#8A744E", strokeWidth=3, opacity=60, cap="round")

# --- winch beam across the crypt ------------------------------------------------
d.shape("rectangle", "Corbel L", x=218, y=196, width=44, height=40,
        fill="#4A3B2C", stroke=INK, strokeWidth=4, radius=4)
d.shape("rectangle", "Corbel R", x=738, y=196, width=44, height=40,
        fill="#4A3B2C", stroke=INK, strokeWidth=4, radius=4)
d.shape("rectangle", "Winch beam", x=230, y=182, width=540, height=34,
        fill=TIMBER, stroke=INK, strokeWidth=5, radius=5)
# drum + crank
d.shape("rectangle", "Drum", x=452, y=204, width=96, height=40,
        fill="#4E3A28", stroke=INK, strokeWidth=5, radius=8)
d.shape("ellipse", "Drum end L", x=444, y=200, width=16, height=48,
        fill="#5C422C", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Drum end R", x=540, y=200, width=16, height=48,
        fill="#5C422C", stroke=INK, strokeWidth=4)
d.path("M556,224 L596,224 L596,250", "Crank", fill=NONE, stroke="#6E5A40",
       strokeWidth=7, cap="round", join="round")
d.shape("ellipse", "Crank knob", x=588, y=246, width=16, height=16,
        fill="#8A744E", stroke=INK, strokeWidth=3)

# --- chains: drum to crate lugs ---------------------------------------------------
def chain(x0, y0, x1, y1, n, label):
    for i in range(n + 1):
        t = i / n
        x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
        d.shape("ellipse", f"{label} link {i+1}", x=x-4, y=y-5, width=9,
                height=11, fill=NONE, stroke="#7A8088", strokeWidth=3)

chain(478, 244, 427, 388, 15, "Chain L")
chain(522, 244, 587, 388, 15, "Chain R")

# --- the crate, mid-lowering ------------------------------------------------------
# lid face (seen from slightly below the winch)
d.path("M380,396 L412,366 L652,366 L620,396 Z", "Crate lid", fill=WOOD_TOP,
       stroke=INK, strokeWidth=5, join="round")
# side face
d.path("M620,396 L652,366 L652,536 L620,566 Z", "Crate side", fill=WOOD_SIDE,
       stroke=INK, strokeWidth=5, join="round")
# front face
d.shape("rectangle", "Crate front", x=380, y=396, width=240, height=170,
        fill=WOOD_FRONT, stroke=INK, strokeWidth=5)
# plank seams + battens
for i, py in enumerate([438, 480, 522]):
    d.path(f"M384,{py} L616,{py}", f"Plank seam {i+1}", fill=NONE,
           stroke="#5C422C", strokeWidth=3, opacity=60)
d.shape("rectangle", "Batten L", x=380, y=396, width=22, height=170,
        fill=WOOD_SIDE, stroke=INK, strokeWidth=4)
d.shape("rectangle", "Batten R", x=598, y=396, width=22, height=170,
        fill=WOOD_SIDE, stroke=INK, strokeWidth=4)
# chain lugs on the lid
d.shape("rectangle", "Lug L", x=416, y=384, width=22, height=14,
        fill="#5C4630", stroke=INK, strokeWidth=3, radius=3)
d.shape("rectangle", "Lug R", x=576, y=384, width=22, height=14,
        fill="#5C4630", stroke=INK, strokeWidth=3, radius=3)
# stencil
d.text("OLIVER", "Stencil", x=500, y=458, size=36, font="Virelai Sans",
       color="#2A2018", justify="center")
d.text("OLIVER", "Stencil ghost", x=497, y=455, size=36, font="Virelai Sans",
       color="#D8B98A", justify="center")
# wax checksum seal on the lid
d.path("M540,368 L562,372 L560,382 L542,380 Z", "Seal ribbon", fill="#7A1F18",
       stroke=INK, strokeWidth=2)
d.shape("ellipse", "Wax seal", x=530, y=352, width=36, height=30,
        fill=WAX, stroke=INK, strokeWidth=3)
d.path("M538,366 L558,366 M548,358 L548,374", "Seal stamp", fill=NONE,
       stroke="#5C140F", strokeWidth=3, opacity=80, cap="round")
# manifest nailed low on the front
d.path("M448,492 L566,488 L568,556 L450,560 Z", "Manifest", fill="#D9C69A",
       stroke=INK, strokeWidth=3, join="round")
d.text("MANIFEST", "Manifest title", x=458, y=510, size=10,
       font="Virelai Sans", color="#3A2C1C", justify="left")
d.path("M458,520 L545,517 M458,530 L540,527",
       "Manifest lines", fill=NONE, stroke="#8A7450", strokeWidth=2, opacity=80)
d.text("PIN b84f636", "Manifest pin", x=458, y=547, size=9,
       font="Virelai Sans", color="#3A2C1C", justify="left")
d.shape("ellipse", "Nail 1", x=451, y=494, width=7, height=7,
        fill="#4A3B2C", stroke=INK, strokeWidth=2)
d.shape("ellipse", "Nail 2", x=557, y=490, width=7, height=7,
        fill="#4A3B2C", stroke=INK, strokeWidth=2)
# verification tick on the manifest corner
d.path("M545,538 L552,546 L563,532", "Verify tick", fill=NONE,
       stroke="#3E5A34", strokeWidth=4, cap="round", join="round")

# --- captions ------------------------------------------------------------------
d.text("SETUP", "Name", x=500, y=930, size=58, font="Virelai Sans",
       color="#E8DAC2", justify="center")
r = d.text("GRAVE GOODS, VERIFIED", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#B09B78", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("rk-setup-V1R00")
