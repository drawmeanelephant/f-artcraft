#!/usr/bin/env python3
"""APH-057 Zhuzhing Ping — aphorism plate V1R00. A document page crushed
by its own decoration: double gilt frame, corner rosettes, comically
bold margin bands, a corner ribbon, a wax seal — while the body text
underneath is a cramped gray scribble, fully illegible. Sparkles ring
the whole thing, each with a ghosted echo because they are rendering
at a flawless sixty frames per second. Deep teal plate, gold + rose
bling, cyan shimmer. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("APH-057 Zhuzhing Ping — Aphorism Plate", 1000, 1000)

INK = "#14241F"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#10201E"}, {"offset": 1, "color": "#060D0C"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#2E4E4A"}, {"offset": 0.7, "color": "#1A2E2C"},
    {"offset": 1, "color": "#0C1514"}]}}
PAPER_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F2ECD8"}, {"offset": 0.65, "color": "#DFD4B4"},
    {"offset": 1, "color": "#BFB18A"}]}}
GOLD_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F0D078"}, {"offset": 0.55, "color": "#C09A3E"},
    {"offset": 1, "color": "#7E5E1E"}]}}
SEAL_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#C04858"}, {"offset": 1, "color": "#6E1E2E"}]}}
GOLD = "#E0B84E"
ROSE = "#D87A9A"
SHIM = "#7AD8D0"
SCRIB = "#6A6A60"
CREAM = "#EEE8D0"
FAINT = "#7EA09A"
KEY = "#B8D8CC"

def sparkle(cx, cy, r, color, op, label):
    k = r * 0.24
    pts = [(cx, cy - r), (cx + k, cy - k), (cx + r, cy), (cx + k, cy + k),
           (cx, cy + r), (cx - k, cy + k), (cx - r, cy),
           (cx - k, cy - k)]
    ds = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"
    return d.path(ds, label, fill=color, opacity=op, stroke=NONE)

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#5E8A7E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#B8D8CC", strokeWidth=3, opacity=40)
# plate patina
d.shape("ellipse", "Patina 1", x=200, y=185, width=200, height=120,
        fill="#3E6258", opacity=20, stroke=NONE)
d.shape("ellipse", "Patina 2", x=620, y=590, width=220, height=130,
        fill="#3E6258", opacity=16, stroke=NONE)
for i, (x, y, w) in enumerate([(206, 258, 7), (794, 248, 8), (158, 503, 6),
                               (843, 498, 7), (250, 736, 6), (760, 726, 7)]):
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#4E7A6E", opacity=35, stroke=NONE)

# halo: the page is radiant about itself
d.shape("ellipse", "Page halo", x=265, y=150, width=470, height=560,
        fill=GOLD, opacity=9, stroke=NONE)

# --- the page: every margin bold --------------------------------------------------
d.shape("rectangle", "Page shadow", x=342, y=206, width=340, height=430,
        radius=3, fill="#000000", opacity=35, stroke=NONE)
d.shape("rectangle", "Page", x=330, y=195, width=340, height=430,
        radius=3, fill=PAPER_GRAD, stroke=INK, strokeWidth=4)
# gilt double frame
d.shape("rectangle", "Frame outer", x=344, y=209, width=312, height=402,
        radius=3, fill=NONE, stroke=GOLD, strokeWidth=5, opacity=90)
d.shape("rectangle", "Frame inner", x=358, y=223, width=284, height=374,
        radius=3, fill=NONE, stroke=ROSE, strokeWidth=2.5, opacity=80)
# corner rosettes on the frame
for i, (cx, cy) in enumerate([(344, 209), (656, 209), (344, 611),
                              (656, 611)]):
    sparkle(cx, cy, 13, GOLD, 95, f"Rosette {i+1}")
    d.shape("ellipse", f"Rosette dot {i+1}", x=cx - 3.5, y=cy - 3.5,
            width=7, height=7, fill=ROSE, stroke=INK, strokeWidth=1.5)
# the margins must be BOLD: heavy gilt bands down both sides
for i, mx in enumerate([368, 630]):
    d.shape("rectangle", f"Margin band {i+1}", x=mx, y=232, width=18,
            height=360, radius=4, fill=GOLD_GRAD, stroke=INK,
            strokeWidth=2.5, opacity=85)
    for j, sy in enumerate([280, 372, 464, 556]):
        sparkle(mx + 9, sy, 7, "#F8E8B0", 90, f"Margin stud {i+1}-{j+1}")

# --- the text: completely illegible ------------------------------------------------
# cramped gray scribble rows overlapping one another, smeared
for k in range(9):
    sy = 268 + k * 30
    x0 = 400 + (k % 3) * 6
    x1 = 598 - (k % 2) * 8
    seg = f"M{x0},{sy}"
    xx = x0
    up = -1 if k % 2 else 1
    while xx < x1 - 16:
        seg += f" Q{xx + 8},{sy + up * 9} {xx + 16},{sy}"
        xx += 16
        up = -up
    d.path(seg, f"Scribble {k+1}", fill=NONE, stroke=SCRIB,
           strokeWidth=5, opacity=55, cap="round")
# smears over the scribble — the ink gave up
d.shape("ellipse", "Smear 1", x=430, y=330, width=140, height=70,
        fill="#8A8A7A", opacity=30, stroke=NONE)
d.shape("ellipse", "Smear 2", x=470, y=450, width=150, height=80,
        fill="#8A8A7A", opacity=25, stroke=NONE)
d.shape("ellipse", "Smear 3", x=440, y=540, width=100, height=50,
        fill="#8A8A7A", opacity=28, stroke=NONE)

# --- corner ribbon -----------------------------------------------------------------
d.path(rot_rect_path(358, 228, 150, 26, -38), "Ribbon", fill=SEAL_GRAD,
       stroke=INK, strokeWidth=3)
d.path("M292,270 L306,288 L320,268", "Ribbon tail", fill=SEAL_GRAD,
       stroke=INK, strokeWidth=2.5)
d.path("M412,196 L424,214 L440,198", "Ribbon tail 2", fill=SEAL_GRAD,
       stroke=INK, strokeWidth=2.5)

# --- wax seal with its own star -----------------------------------------------------
d.shape("ellipse", "Seal", x=606, y=560, width=56, height=56,
        fill=SEAL_GRAD, stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Seal inner", x=618, y=572, width=32, height=32,
        fill=NONE, stroke="#F0A8B8", strokeWidth=2, opacity=60)
sparkle(634, 588, 10, "#F0C8D0", 90, "Seal star")

# --- sparkles, flawless sixty frames per second --------------------------------------
# each hero sparkle gets a ghost echo one frame behind
SPARKS = [(296, 172, 26, GOLD), (706, 232, 21, SHIM), (252, 408, 17, ROSE),
          (748, 430, 23, GOLD), (350, 648, 17, SHIM), (668, 660, 15, GOLD),
          (500, 150, 14, SHIM)]
for i, (sx, sy, sr, sc) in enumerate(SPARKS):
    sparkle(sx + 12, sy + 9, sr * 0.8, sc, 22, f"Spark echo {i+1}")
    sparkle(sx + 6, sy + 5, sr * 0.9, sc, 45, f"Spark mid {i+1}")
    sparkle(sx, sy, sr, sc, 95, f"Spark {i+1}")
# confetti dust
for i, (cx, cy, cr, cc) in enumerate([
        (330, 150, 3, GOLD), (400, 120, 2.5, SHIM), (610, 140, 3, ROSE),
        (680, 170, 2.5, GOLD), (240, 300, 2.5, SHIM), (765, 320, 3, GOLD),
        (230, 520, 3, ROSE), (770, 560, 2.5, SHIM), (420, 668, 3, GOLD),
        (580, 672, 2.5, ROSE), (310, 620, 2, SHIM), (700, 600, 2, GOLD)]):
    d.shape("ellipse", f"Confetti {i+1}", x=cx - cr, y=cy - cr,
            width=cr * 2, height=cr * 2, fill=cc, opacity=60, stroke=NONE)

# --- aphorism line + name + role ------------------------------------------------
r = d.text("ZHUZH IS NEVER DONE.", "Key line", x=500, y=740,
           size=22, font="Virelai Sans", color=KEY, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "key tracking", ids=[r["id"]], tracking=100)

d.text("ZHUZHING PING", "Name", x=500, y=905, size=56,
       font="Virelai Sans", color=CREAM, justify="center")
r = d.text("ZHUZH IS NEVER DONE", "Role", x=500, y=950, size=18,
           font="Virelai Sans", color=FAINT, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=160)

d.finish("aph-057-zhuzhing-ping-V1R00")
