#!/usr/bin/env python3
"""LIM-SVGON-THE-LINE — limerick plate V1R00. Vector supremacy made visual:
Svgon declaring "I scale beyond all meaning and sight" inside nested
infinite-zoom frames, golden-ratio staff planted, a crashed raster window
abandoned at the edge. Indigo night, luminous strokes. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("LIM-SVGON-THE-LINE — Limerick Plate", 1000, 1000)

INK = "#14122A"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#0F0D22"}, {"offset": 1, "color": "#060510"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#3E3C72"}, {"offset": 0.7, "color": "#242148"},
    {"offset": 1, "color": "#110F2A"}]}}
COAT = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#B8BCE4"}, {"offset": 0.6, "color": "#7078B4"},
    {"offset": 1, "color": "#3E4270"}]}}
GOLD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F6DC96"}, {"offset": 1, "color": "#C09038"}]}}
VISOR = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#D8F2FF"}, {"offset": 1, "color": "#6EB8E8"}]}}
ICE = "#E4E4FA"
SOFT = "#A8A4D8"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#7873B8", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#DCD8F8", strokeWidth=3, opacity=45)
# luminous heart behind the figure
d.shape("ellipse", "Glow pool", x=330, y=320, width=340, height=420,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#8E9BEE", "opacity": 0.22},
            {"offset": 1, "color": "#8E9BEE", "opacity": 0}]}},
        stroke=NONE)

# --- the declaration -------------------------------------------------------------
r = d.text("I SCALE BEYOND ALL MEANING AND SIGHT", "Declaration",
           x=500, y=148, size=17, font="Virelai Sans", color=ICE,
           justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "declaration tracking", ids=[r["id"]],
          tracking=110)
d.path("M330,168 L670,168", "Declaration rule", fill=NONE,
       stroke="#7873B8", strokeWidth=2, opacity=60)

# --- nested zoom frames receding to the vanishing point -----------------------------
FRAMES = [(580, 452, 55, "200%"), (500, 390, 45, "400%"),
          (390, 300, 36, "800%"), (300, 232, 28, "1600%"),
          (232, 180, 22, "3200%"), (178, 138, 17, "6400%")]
for i, (w, h, op, lbl) in enumerate(FRAMES):
    x, y = 500 - w / 2, 470 - h / 2
    d.shape("rectangle", f"Zoom frame {i+1}", x=x, y=y, width=w, height=h,
            radius=8, fill=NONE, stroke="#9EA0E4", strokeWidth=2,
            opacity=op)
    lx = x + w - 14 if i % 2 == 0 else x + 14
    d.text(lbl, f"Zoom label {i+1}", x=lx, y=y + 18, size=11,
           font="Virelai Sans", color="#8E8CC8", justify="right"
           if i % 2 == 0 else "left")

# --- the perfect curve, sweeping through every zoom level ---------------------------
CURVE = "M228,690 C400,540 596,610 782,296"
d.path(CURVE, "Curve glow", fill=NONE, stroke="#8E9BEE", strokeWidth=16,
       opacity=13, cap="round")
d.path(CURVE, "Curve halo", fill=NONE, stroke="#A8B4F2", strokeWidth=7,
       opacity=32, cap="round")
d.path(CURVE, "Curve spine", fill=NONE, stroke="#EDF0FF", strokeWidth=3,
       cap="round")
for i, (ax, ay) in enumerate([(228, 690), (782, 296)]):
    d.shape("rectangle", f"Anchor {i+1}", x=ax - 5, y=ay - 5, width=10,
            height=10, fill=ICE, stroke=INK, strokeWidth=2)

# --- crashed raster window, abandoned at the edge ------------------------------------
crash_ids = []
def crash_add(res):
    if res and res.get("id"):
        crash_ids.append(res["id"])

crash_add(d.shape("rectangle", "Raster window", x=196, y=620, width=140,
                  height=100, radius=5, fill={"gradient": {"kind": "linear",
                  "stops": [{"offset": 0, "color": "#5A5870"},
                            {"offset": 1, "color": "#33324A"}]}},
                  stroke=INK, strokeWidth=3))
crash_add(d.shape("rectangle", "Raster chrome", x=196, y=620, width=140,
                  height=18, radius=5, fill="#24223A", stroke=INK,
                  strokeWidth=2))
# checkerboard of pixels — the raster prison
for r_i in range(3):
    for c_i in range(4):
        if (r_i + c_i) % 2 == 0:
            crash_add(d.shape("rectangle", f"Pixel {r_i}-{c_i}",
                              x=206 + c_i * 20, y=648 + r_i * 20,
                              width=20, height=20, fill="#7A78A0",
                              opacity=55, stroke=NONE))
crash_add(d.path("M252,668 L284,700 M284,668 L252,700", "Crash X",
                 fill=NONE, stroke="#E4E4FA", strokeWidth=5, cap="round"))
crash_add(d.text("raster.exe", "Crash tag", x=266, y=635, size=10,
                 font="Virelai Sans", color="#A8A4D8", justify="center"))
if crash_ids:
    d.call("transform", {"ids": crash_ids, "rotate": -8,
                         "origin": [266, 670]}, "tilt crash")

# --- Svgon: judgmental bust, visor, medallion, staff ----------------------------------
d.shape("ellipse", "Svgon shadow", x=400, y=760, width=200, height=26,
        fill="#060510", opacity=45, stroke=NONE)
# shoulders / bust
d.path("M430,782 C432,690 448,610 470,556 L530,556 C552,610 568,690 "
       "570,782 Z",
       "Svgon bust", fill=COAT, stroke=INK, strokeWidth=5, join="round")
d.path("M448,600 C452,660 456,720 458,768", "Coat sheen", fill=NONE,
       stroke="#EDF0FF", strokeWidth=7, opacity=20, cap="round")
# head: sleek helm
d.path("M444,450 C444,392 556,392 556,450 C556,482 536,500 500,500 "
       "C464,500 444,482 444,450 Z",
       "Svgon helm", fill=COAT, stroke=INK, strokeWidth=5)
d.path("M500,396 C510,408 510,424 500,434", "Helm ridge", fill=NONE,
       stroke="#EDF0FF", strokeWidth=4, opacity=50, cap="round")
# anti-aliasing visor
d.shape("rectangle", "Visor", x=450, y=444, width=100, height=16, radius=8,
        fill=VISOR, stroke=INK, strokeWidth=2.5)
d.path("M456,452 L544,452", "Visor gleam", fill=NONE, stroke="#FFFFFF",
       strokeWidth=2, opacity=80, cap="round")
# judgmental brows, asymmetric — one arched high, one pressed flat
d.path("M460,424 Q476,412 492,420", "Brow high", fill=NONE, stroke=INK,
       strokeWidth=4.5, cap="round")
d.path("M508,428 L532,426", "Brow flat", fill=NONE, stroke=INK,
       strokeWidth=4.5, cap="round")
# flat mouth of disdain, just under the visor
d.path("M486,478 L514,478", "Mouth", fill=NONE, stroke=INK,
       strokeWidth=4.5, cap="round")
# validation medallion on the chest
d.shape("ellipse", "Medallion", x=468, y=580, width=64, height=64,
        fill=GOLD, stroke=INK, strokeWidth=4)
d.path("M484,612 L497,625 L518,598", "Medallion check", fill=NONE,
       stroke="#14122A", strokeWidth=6, cap="round", join="round")
d.shape("ellipse", "Medallion glint", x=478, y=588, width=20, height=12,
        fill="#FFFFFF", opacity=50, stroke=NONE)
# right arm holding the staff
d.path("M556,580 C596,584 620,600 630,632", "Arm R", fill=NONE,
       stroke="#3E4270", strokeWidth=20, cap="round")
d.shape("ellipse", "Hand R", x=618, y=624, width=28, height=26,
        fill="#B8BCE4", stroke=INK, strokeWidth=4)
# golden-ratio staff planted at his side
d.path("M640,336 L640,792", "Staff shaft", fill=NONE, stroke="#D8AC54",
       strokeWidth=6, cap="round")
d.path("M638,792 L642,792 L640,808 Z", "Staff tip", fill="#D8AC54",
       stroke=NONE)
d.shape("rectangle", "Golden rect", x=614, y=282, width=56, height=36,
        radius=3, fill="#1A1840", stroke="#F6DC96", strokeWidth=3)
d.path("M648,282 L648,318", "Phi split", fill=NONE, stroke="#F6DC96",
       strokeWidth=2)
d.path("M648,318 A21,21 0 0 0 627,297", "Phi arc", fill=NONE,
       stroke="#F6DC96", strokeWidth=2)
d.path("M661,282 L661,318", "Phi split 2", fill=NONE, stroke="#F6DC96",
       strokeWidth=1.5, opacity=70)
d.shape("ellipse", "Staff glow", x=606, y=274, width=72, height=52,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#F6DC96", "opacity": 0.3},
            {"offset": 1, "color": "#F6DC96", "opacity": 0}]}},
        stroke=NONE)

# --- name + role ------------------------------------------------------------------
d.text("SVGON THE LINE", "Name", x=500, y=930, size=58,
       font="Virelai Sans", color=ICE, justify="center")
r = d.text("LIM-SVGON-THE-LINE", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color=SOFT, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=190)

d.finish("lim-svgon-the-line-V1R00")
