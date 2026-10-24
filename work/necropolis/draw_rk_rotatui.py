#!/usr/bin/env python3
"""rotatui.sh — The Ossuary Kiosk. Necropolis plate V1R00.
A terminal window set into a crypt wall like a ticket kiosk, its menu
options glowing as votive candles in a row, cursor blinking like a held
breath. Screen-green phosphor on tomb grey. 1000x1000.
Gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Rotatui — Necropolis Plate", 1000, 1000)

INK = "#141A16"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#101512"}, {"offset": 1, "color": "#070A08"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#49524E"}, {"offset": 0.7, "color": "#2B332F"},
    {"offset": 1, "color": "#141917"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#262E2A"}, {"offset": 1, "color": "#101512"}]}}
STONE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5A645C"}, {"offset": 1, "color": "#333B36"}]}}
RECESS = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#0C120E"}, {"offset": 1, "color": "#050908"}]}}
WAX = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E8D9B0"}, {"offset": 1, "color": "#B09B6E"}]}}
PHOS, PHOS_DIM = "#A8F0C0", "#3F6B52"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#6E7A66", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D6E2D4", strokeWidth=3, opacity=45)
for i, (x, y, w) in enumerate([(193,233,8),(801,230,7),(157,524,9),(837,544,8),
                               (247,766,7),(753,749,9),(133,393,6),(864,391,7),
                               (391,113,7),(613,110,8),(333,823,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#59645C", opacity=35, stroke=NONE)

# --- crypt wall: mortar courses inside the disc -------------------------------
for i, my in enumerate([180, 250, 320, 390, 590, 660]):
    hw = int(math.sqrt(max(0, 420**2 - (my - 460)**2))) - 8
    d.path(f"M{500-hw},{my} L{500+hw},{my}", f"Mortar {i+1}", fill=NONE,
           stroke="#0E1311", strokeWidth=4, opacity=30)
for i, (x, y, h) in enumerate([(300,180,70),(640,180,70),(230,250,70),(500,250,70),
                               (760,250,70),(200,320,70),(800,320,70),(280,590,70),
                               (720,590,70),(420,660,40),(580,660,40)]):
    d.path(f"M{x},{y} L{x},{y+h}", f"Wall joint {i+1}", fill=NONE,
           stroke="#0E1311", strokeWidth=4, opacity=25)

# --- floor --------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0A0E0C",
       strokeWidth=4, opacity=70)

# --- the kiosk niche: arched recess in the wall --------------------------------
d.path("M350,650 L350,350 C350,268 412,222 500,222 C588,222 650,268 650,350 L650,650 Z",
       "Niche recess", fill=RECESS, stroke=NONE)
d.path("M340,660 L340,350 C340,262 408,210 500,210 C592,210 660,262 660,350 L660,660",
       "Niche surround", fill=NONE, stroke="#1C2420", strokeWidth=26)
d.path("M352,648 L352,352 C352,272 412,226 500,226 C588,226 648,272 648,352 L648,648",
       "Niche edge light", fill=NONE, stroke="#5A645C", strokeWidth=3, opacity=60)
# voussoir ticks around the arch
for i in range(7):
    a = math.radians(200 + i * (140 / 6))
    x1, y1 = 500 + 178 * math.cos(a), 300 + 178 * math.sin(a)
    x2, y2 = 500 + 206 * math.cos(a), 300 + 206 * math.sin(a)
    d.path(f"M{x1:.0f},{y1:.0f} L{x2:.0f},{y2:.0f}", f"Voussoir {i+1}",
           fill=NONE, stroke="#0E1311", strokeWidth=5, opacity=50, cap="round")

# --- the terminal window --------------------------------------------------------
d.shape("ellipse", "Screen spill", x=330, y=330, width=340, height=320,
        fill="#6AE0A0", opacity=12, stroke=NONE)
d.shape("rectangle", "Screen", x=385, y=295, width=230, height=290,
        fill={"gradient": {"kind": "linear", "stops": [
            {"offset": 0, "color": "#081B11"},
            {"offset": 1, "color": "#030B07"}]}},
        stroke=INK, strokeWidth=5, radius=6)
d.shape("rectangle", "Screen header", x=385, y=295, width=230, height=24,
        fill={"gradient": {"kind": "linear", "stops": [
            {"offset": 0, "color": "#0E2A1C"},
            {"offset": 1, "color": "#081B11"}]}},
        stroke=INK, strokeWidth=3, radius=6)
d.text("OSSUARY.OS", "Header", x=397, y=311, size=11, font="Virelai Sans",
       color=PHOS_DIM, justify="left")
d.shape("ellipse", "Header lamp", x=592, y=302, width=10, height=10,
        fill=PHOS, opacity=85, stroke=NONE)
# scanlines
for i, sy in enumerate([350, 400, 450, 500, 550]):
    d.path(f"M392,{sy} L608,{sy}", f"Scanline {i+1}", fill=NONE,
           stroke="#9AE8B0", strokeWidth=2, opacity=8)
# console text
d.text("OSSUARY KIOSK — NIGHT DESK", "Line 1", x=397, y=346, size=12,
       font="Virelai Sans", color=PHOS, justify="left")
d.text("PLOT 12C ....... RESERVED", "Line 2", x=397, y=372, size=11,
       font="Virelai Sans", color=PHOS_DIM, justify="left")
d.text("KEYS ......... DISPATCHER", "Line 3", x=397, y=390, size=11,
       font="Virelai Sans", color=PHOS_DIM, justify="left")
d.text("GATE LANTERN ....... LIT", "Line 4", x=397, y=408, size=11,
       font="Virelai Sans", color=PHOS_DIM, justify="left")
# menu options as votive candles in a row
for i, (cx, label) in enumerate([(420, "PLOTS"), (465, "INTER"), (510, "LEDGER"),
                                 (555, "EXHUME"), (600, "EXIT")]):
    d.shape("ellipse", f"{label} halo", x=cx-16, y=442, width=32, height=30,
            fill="#9AE8B0", opacity=14, stroke=NONE)
    d.shape("rectangle", f"{label} wax", x=cx-5, y=466, width=10, height=22,
            fill="#123426", stroke=PHOS_DIM, strokeWidth=2, radius=2)
    d.path(f"M{cx},466 C{cx-4},459 {cx-2},453 {cx},449 "
           f"C{cx+2},453 {cx+4},459 {cx},466 Z",
           f"{label} flame", fill=PHOS, stroke=NONE)
    d.text(label, f"{label} label", x=cx, y=502, size=9, font="Virelai Sans",
           color=PHOS, justify="center")
# the blinking cursor, mid-breath
d.text("READY", "Prompt", x=397, y=552, size=12, font="Virelai Sans",
       color=PHOS_DIM, justify="left")
d.shape("ellipse", "Cursor breath", x=446, y=536, width=30, height=24,
        fill="#9AE8B0", opacity=20, stroke=NONE)
d.shape("rectangle", "Cursor", x=452, y=540, width=12, height=16,
        fill=PHOS, stroke=NONE)

# --- stone sill + real votives ---------------------------------------------------
d.path("M330,650 L670,650 L690,682 L310,682 Z", "Sill", fill=STONE,
       stroke=INK, strokeWidth=4, join="round")
d.shape("ellipse", "Sill phosphor sheen", x=390, y=648, width=220, height=14,
        fill="#9AE8B0", opacity=18, stroke=NONE)
d.shape("ellipse", "Sill shadow", x=330, y=676, width=340, height=18,
        fill="#050908", opacity=50, stroke=NONE)
for i, cx in enumerate([368, 636]):
    d.shape("ellipse", f"Votive glow {i+1}", x=cx-22, y=580, width=44, height=60,
            fill="#FFDF96", opacity=12, stroke=NONE)
    d.shape("rectangle", f"Votive wax {i+1}", x=cx-8, y=622, width=16, height=28,
            fill=WAX, stroke=INK, strokeWidth=3, radius=3)
    d.path(f"M{cx},622 C{cx-5},614 {cx-2},607 {cx},602 "
           f"C{cx+2},607 {cx+5},614 {cx},622 Z",
           f"Votive flame {i+1}", fill="#FFDF96", stroke=NONE)

# --- captions ------------------------------------------------------------------
d.text("ROTATUI", "Name", x=500, y=930, size=58, font="Virelai Sans",
       color="#DCE8DC", justify="center")
r = d.text("THE FRONT DESK", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#93AC9A", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("rk-rotatui-V1R00")
