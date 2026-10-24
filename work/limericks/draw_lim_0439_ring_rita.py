#!/usr/bin/env python3
"""LIM-0439 Ring Rita — limerick plate V1R00. The voluntary panopticon:
a smart doorbell whose camera lens is a watching eye, a subscription
receipt curling out of the mail slot, and the homeowner's key held
inside the portal ring — the portal keeps the key. Porchlight palette,
warm dark ink. 1000x1000. House style: gradients + translucent shading,
never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("LIM-0439 Ring Rita — Limerick Plate", 1000, 1000)

INK = "#2E1B12"
CREAM = "#F2DFC0"
TAN = "#C4A87E"
RED = "#C0392B"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1E130E"}, {"offset": 1, "color": "#0C0705"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#C99755"}, {"offset": 0.7, "color": "#7A5228"},
    {"offset": 1, "color": "#402715"}]}}
DOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4A2E1C"}, {"offset": 1, "color": "#2A1810"}]}}
BRASS = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#D8AC64"}, {"offset": 1, "color": "#8A5E28"}]}}
GLASS = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4A4238"}, {"offset": 0.7, "color": "#241E18"},
    {"offset": 1, "color": "#0E0A08"}]}}
IRIS = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F0C06A"}, {"offset": 0.75, "color": "#B87830"},
    {"offset": 1, "color": "#6E3E14"}]}}
PAPER = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#EFE4C8"}, {"offset": 1, "color": "#C9B892"}]}}
GLOW = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F6D896", "opacity": 0.45},
    {"offset": 1, "color": "#F6D896", "opacity": 0}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#8A6438", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F0DCB8", strokeWidth=3, opacity=45)
# porch-night flecks on the plate
for i, (x, y, w) in enumerate([(170, 240, 8), (830, 220, 7), (140, 520, 9),
                               (855, 600, 8), (230, 770, 7), (760, 760, 8),
                               (120, 380, 6), (870, 420, 7), (320, 130, 7),
                               (680, 140, 8)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#5A3A1E", opacity=40, stroke=NONE)
# panopticon sight-lines fanning out of the lens, faint
for i, (ex, ey) in enumerate([(780, 260), (800, 385), (775, 500)]):
    d.path(f"M488,355 L{ex},{ey}", f"Sight line {i+1}", fill=NONE,
           stroke="#F6D896", strokeWidth=2, opacity=18, cap="round")
d.path("M488,345 L800,250 L800,490 L488,370 Z", "Gaze wedge",
       fill="#F6D896", opacity=6, stroke=NONE)

# --- door slab ------------------------------------------------------------------
d.shape("rectangle", "Door slab", x=330, y=170, width=260, height=620,
        radius=10, fill=DOOR_GRAD, stroke=INK, strokeWidth=5)
for i, gx in enumerate([395, 460, 525]):
    d.path(f"M{gx},185 L{gx},775", f"Plank groove {i+1}", fill=NONE,
           stroke="#1E120C", strokeWidth=3, opacity=60, cap="round")
# house number — digits in Source Sans 3 (Virelai carries no figures)
d.shape("rectangle", "Number plate", x=425, y=205, width=70, height=42,
        radius=6, fill=BRASS, stroke=INK, strokeWidth=3)
d.text("439", "House number", x=460, y=236, size=24,
       font="Source Sans 3", color=INK, justify="center")

# --- doorbell: the watching eye ---------------------------------------------------
d.shape("rectangle", "Doorbell body", x=408, y=295, width=104, height=200,
        radius=24, fill=BRASS, stroke=INK, strokeWidth=5)
# REC indicator
d.shape("ellipse", "REC dot", x=424, y=310, width=10, height=10,
        fill=RED, stroke=NONE)
d.text("REC", "REC label", x=452, y=320, size=10, font="Virelai Sans",
       color=INK, justify="left")
# lens = eye
d.shape("ellipse", "Lens glow", x=396, y=305, width=108, height=108,
        fill=GLOW, stroke=NONE)
d.shape("ellipse", "Lens glass", x=416, y=325, width=68, height=68,
        fill=GLASS, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Iris", x=435, y=344, width=30, height=30,
        fill=IRIS, stroke=INK, strokeWidth=3)
d.shape("ellipse", "Pupil", x=444, y=353, width=12, height=12,
        fill="#120A06", stroke=NONE)
d.shape("ellipse", "Lens glint", x=438, y=336, width=10, height=7,
        fill="#FFFFFF", opacity=70, stroke=NONE)
# heavy upper lid — the camera never blinks but the house does
d.path("M424,352 Q450,336 476,352", "Upper lid", fill=NONE, stroke=INK,
       strokeWidth=7, cap="round")
# focus-reticle brackets around the lens
for i, (bx, by, sx, sy) in enumerate([(404, 313, 1, 1), (496, 313, -1, 1),
                                     (404, 405, 1, -1), (496, 405, -1, -1)]):
    d.path(f"M{bx},{by + 12 * sy} L{bx},{by} L{bx + 12 * sx},{by}",
           f"Reticle {i+1}", fill=NONE, stroke=INK, strokeWidth=2.5,
           opacity=70, cap="round")
# the ring button — glow where the subscription tolls
d.shape("ellipse", "Button glow", x=418, y=418, width=64, height=64,
        fill=GLOW, stroke=NONE)
d.shape("ellipse", "Button ring", x=428, y=428, width=44, height=44,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#5A4632"}, {"offset": 1, "color": "#2A1E14"}]}},
        stroke="#F0C87A", strokeWidth=4)
d.shape("ellipse", "Button core", x=442, y=442, width=16, height=16,
        fill="#1E130C", stroke=NONE)
# mic grille
for i, gy in enumerate([478, 484]):
    d.path(f"M428,{gy} L492,{gy}", f"Grille {i+1}", fill=NONE, stroke=INK,
           strokeWidth=2.5, opacity=70, cap="round")

# --- the subscription receipt, curling out of the mail slot -------------------------
d.shape("rectangle", "Mail slot", x=395, y=545, width=130, height=18,
        radius=4, fill="#1E130C", stroke=BRASS, strokeWidth=3)
d.path("M428,563 C424,615 430,675 436,730 L450,723 L464,731 L478,723 "
       "L492,731 L506,723 L520,731 L534,723 L544,728 C550,675 556,615 "
       "560,563 Z",
       "Receipt", fill=PAPER, stroke=INK, strokeWidth=3.5, join="round")
d.text("PORCH PASS", "Receipt head", x=494, y=592, size=13,
       font="Virelai Sans", color=INK, justify="center")
d.path("M448,604 L540,604", "Receipt rule", fill=NONE, stroke=INK,
       strokeWidth=2, opacity=60)
d.text("MONTHLY FEE", "Receipt fee", x=494, y=624, size=11,
       font="Virelai Sans", color="#4A3524", justify="center")
d.text("$12.99", "Receipt price", x=494, y=650, size=19,
       font="Source Sans 3", color=INK, justify="center")
d.text("AUTO-RENEW ON", "Receipt renew", x=494, y=676, size=10,
       font="Virelai Sans", color="#4A3524", justify="center")
d.text("NO OPT-OUT", "Receipt optout", x=494, y=700, size=11,
       font="Virelai Sans", color=RED, justify="center")

# --- the portal keeps the key ---------------------------------------------------
d.shape("ellipse", "Portal glow", x=620, y=330, width=200, height=200,
        fill=GLOW, stroke=NONE)
d.shape("ellipse", "Portal ring", x=645, y=355, width=150, height=150,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#241A12"}, {"offset": 1, "color": "#100A06"}]}},
        stroke="#E8BC72", strokeWidth=9)
d.path("M668,430 A55,55 0 0 1 700,385", "Portal swirl 1", fill=NONE,
       stroke="#E8BC72", strokeWidth=3, opacity=60, cap="round")
d.path("M770,455 A52,52 0 0 1 738,478", "Portal swirl 2", fill=NONE,
       stroke="#E8BC72", strokeWidth=3, opacity=45, cap="round")
# the key, suspended upright inside the portal — out of the owner's reach
d.shape("ellipse", "Key bow", x=704, y=398, width=32, height=32,
        fill=NONE, stroke=BRASS, strokeWidth=8)
d.path("M720,430 L720,480", "Key shaft", fill=NONE, stroke=BRASS,
       strokeWidth=9, cap="round")
d.path("M720,462 L736,462 M720,476 L732,476", "Key teeth", fill=NONE,
       stroke=BRASS, strokeWidth=8, cap="round")
d.shape("ellipse", "Key glint", x=709, y=403, width=8, height=8,
        fill="#F6E0B0", opacity=80, stroke=NONE)
# sparkles at the portal rim
for i, (sx, sy) in enumerate([(648, 372), (796, 432), (716, 340)]):
    d.path(f"M{sx},{sy} l10,0 M{sx + 5},{sy - 5} l0,10", f"Spark {i+1}",
           fill=NONE, stroke="#F6E0B0", strokeWidth=2, opacity=70,
           cap="round")

# --- ground shadow inside the plate ----------------------------------------------
d.shape("ellipse", "Slab shadow", x=355, y=778, width=250, height=22,
        fill="#1E1008", opacity=40, stroke=NONE)

# --- key line + name + role ---------------------------------------------------------
r = d.text("THE PANOPTICON'S MONTHLY ART.", "Key line", x=500, y=762,
           size=21, font="Virelai Sans", color=CREAM, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "key line tracking", ids=[r["id"]], tracking=50)
d.text("RING RITA", "Name", x=500, y=930, size=58,
       font="Virelai Sans", color=CREAM, justify="center")
r = d.text("SUBSCRIPTION IS THE FEE", "Role", x=500, y=967, size=20,
           font="Virelai Sans", color=TAN, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=170)

d.finish("lim-0439-ring-rita-V1R00")
