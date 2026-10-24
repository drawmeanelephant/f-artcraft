#!/usr/bin/env python3
"""Malrex Voidrender — mascot portrait V1R00.
A monitor whose screen is mid-collapse: log lines still lit at the top,
everything below dissolving into pixels that spiral into a black void.
Malrex has no form — two faint eyes in the void are all the logs know of him.
1000x1000. Gradients + translucent shading, never flat fills."""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Malrex Voidrender — Mascot Portrait", 1000, 1000)

INK = "#3A2630"
BG_GRAD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000], "stops": [
    {"offset": 0, "color": "#100C16"}, {"offset": 1, "color": "#070509"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#5A5068"}, {"offset": 0.7, "color": "#3C3450"},
    {"offset": 1, "color": "#211A30"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "start": [500, 700], "end": [500, 880], "stops": [
    {"offset": 0, "color": "#322A42"}, {"offset": 1, "color": "#181222"}]}}
BEZEL_GRAD = {"gradient": {"kind": "linear", "start": [500, 208], "end": [500, 560], "stops": [
    {"offset": 0, "color": "#585064"}, {"offset": 1, "color": "#2A2432"}]}}
SCREEN_GRAD = {"gradient": {"kind": "linear", "start": [500, 232], "end": [500, 532], "stops": [
    {"offset": 0, "color": "#A8DCD0"}, {"offset": 0.32, "color": "#5E8E92"},
    {"offset": 0.62, "color": "#16222E"}, {"offset": 1, "color": "#060810"}]}}
VOID_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#08040E"}, {"offset": 0.75, "color": "#0C0816"},
    {"offset": 1, "color": "#241E36"}]}}
STAND_GRAD = {"gradient": {"kind": "linear", "start": [500, 556], "end": [500, 660], "stops": [
    {"offset": 0, "color": "#453C50"}, {"offset": 1, "color": "#221C2A"}]}}

PCX, PCY, PR = 500, 460, 420

def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#6A7A9A", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#6A5E7E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#9A8CB0", strokeWidth=3, opacity=30)
for i, (x, y, w) in enumerate([(196,236,8),(796,230,7),(158,514,9),(836,534,8),
                               (262,762,7),(742,748,9),(136,388,6),(858,392,7),
                               (388,112,7),(616,114,8),(346,816,6),(660,820,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#2A2138", opacity=55, stroke=NONE)

# --- floor ---------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0E0A14",
       strokeWidth=4, opacity=70)

# --- monitor glow behind the bezel ------------------------------------------------
d.shape("ellipse", "Screen halo", x=252, y=160, width=496, height=380,
        fill="#7FC8BC", opacity=14, stroke=NONE)

# --- the monitor ------------------------------------------------------------------
d.shape("ellipse", "Monitor shadow", x=330, y=668, width=340, height=24,
        fill="#0A0710", opacity=55, stroke=NONE)
# stand
d.path("M462,556 L538,556 L552,640 L448,640 Z", "Stand neck",
       fill=STAND_GRAD, stroke=INK, strokeWidth=5, join="round")
d.shape("rectangle", "Stand foot", x=400, y=634, width=200, height=26,
        radius=10, fill=STAND_GRAD, stroke=INK, strokeWidth=5)
# bezel
d.shape("rectangle", "Bezel", x=298, y=208, width=404, height=352,
        radius=22, fill=BEZEL_GRAD, stroke=INK, strokeWidth=7)
d.shape("rectangle", "Bezel inner lip", x=312, y=222, width=376, height=324,
        radius=14, fill=NONE, stroke="#0E0A14", strokeWidth=3, opacity=60)
# power LED — the one thing still reporting "fine"
d.shape("ellipse", "Power LED", x=652, y=542, width=10, height=10,
        fill="#8FE0A8", stroke="#0E0A14", strokeWidth=2)
d.shape("ellipse", "LED glow", x=646, y=536, width=22, height=22,
        fill="#8FE0A8", opacity=25, stroke=NONE)

# --- the screen: lit at top, void at bottom ----------------------------------------
d.shape("rectangle", "Screen", x=322, y=232, width=356, height=300,
        radius=10, fill=SCREEN_GRAD, stroke=NONE)

# log lines still legible at the top — the last things your logs knew
for i, (ly, lw) in enumerate([(252, 240), (272, 300), (292, 196), (312, 268)]):
    col = "#1E3A38" if i != 2 else "#7E2B30"
    d.shape("rectangle", f"Log line {i+1}", x=342, y=ly, width=lw, height=10,
            radius=4, fill=col, stroke=NONE, opacity=85)
# cursor at end of the red line — the misplaced comment
d.shape("rectangle", "Cursor", x=542, y=290, width=9, height=14,
        fill="#C8685E", stroke=NONE, opacity=90)

# glare, kept up in the lit corner — nothing reflects off a void
d.path("M322,232 L470,232 L416,352 L322,330 Z", "Screen glare",
       fill="#FFFFFF", opacity=10, stroke=NONE)

# the void itself — nothing reflective left in it
d.shape("ellipse", "Void rim glow", x=352, y=408, width=296, height=136,
        fill="#4E3E6A", opacity=35, stroke=NONE)
d.shape("ellipse", "Void", x=372, y=424, width=256, height=108,
        fill=VOID_GRAD, stroke=NONE)
# Malrex: formless — two faint eyes are all the logs recorded
d.shape("ellipse", "Eye L", x=464, y=466, width=13, height=17,
        fill="#BFE0D4", opacity=30, stroke=NONE)
d.shape("ellipse", "Eye R", x=521, y=466, width=13, height=17,
        fill="#BFE0D4", opacity=30, stroke=NONE)

# --- the dissolve: intact pixels at the seam, sparser as they fall -----------------
rng = random.Random(66)
PIX = ["#8FC8BC", "#6FA8A2", "#4E7C82", "#34565E", "#22383F"]

def void_frac(x, y):
    return ((x - 500) / 128.0) ** 2 + ((y - 478) / 54.0) ** 2

# seam row: a solid ragged edge where content stops being content
for i in range(24):
    sx = 330 + i * 14.4
    sy = 352 + rng.uniform(-4, 10)
    if sx + 13 > 670:
        continue
    d.shape("rectangle", f"Seam px {i+1}", x=sx, y=sy, width=13, height=13,
            fill=PIX[0], stroke=NONE, opacity=90)
# falling pixels: sparser, darker, smaller, leaning toward the void
n = 0
for row in range(8):
    y0 = 372 + row * 21
    density = 1.0 - row * 0.11
    for col in range(20):
        if rng.random() > density * 0.62:
            continue
        x0 = 336 + col * 16.6 + rng.uniform(-8, 8)
        # drift toward the void's mouth
        pull = min(0.5, (y0 - 350) / 320.0)
        x0 += (500 - x0) * pull * rng.uniform(0.3, 0.9)
        y1 = y0 + rng.uniform(-7, 9)
        if void_frac(x0, y1) < 0.72:   # swallowed already — skip
            continue
        s = max(4.0, 12.5 - row * 1.1 + rng.uniform(-1.5, 1.5))
        shade = min(4, 1 + row // 2)
        px = d.shape("rectangle", f"Fall px {n+1}", x=x0, y=y1,
                     width=s, height=s, fill=PIX[shade], stroke=NONE,
                     opacity=max(30, 92 - row * 8))
        if px and px.get("id") and rng.random() < 0.3:
            d.cmd("object.rotate", f"px rot {n+1}", ids=[px["id"]],
                  angle=rng.uniform(-24, 24), origin=[x0 + s/2, y1 + s/2])
        n += 1
# a few escapees that missed the mouth and drift below it
for i, (x0, y0, s, op) in enumerate([
        (392, 560, 8, 40), (612, 566, 7, 35), (458, 592, 5, 28),
        (548, 600, 4, 22), (500, 566, 6, 30)]):
    d.shape("rectangle", f"Escapee {i+1}", x=x0, y=y0, width=s, height=s,
            fill=PIX[4], stroke=NONE, opacity=op)

# --- captions ----------------------------------------------------------------------
d.text("MALREX VOIDRENDER", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#DDD4E4", justify="center")
r = d.text("THE ENTROPY BRICKY FEARS", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#A494B8", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("066.malrex-voidrender-V1R00")
