#!/usr/bin/env python3
"""Quill Staticvox — mascot portrait V1R00.
A spectral quill-figure tuning radio dials in the Static Spire — a
crumbling tower of rusted antennae — a spectral ledger open beside her.
1000x1000. Gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Quill Staticvox — Mascot Portrait", 1000, 1000)

INK = "#1E1A22"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#0B1420"}, {"offset": 1, "color": "#05080E"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#2E4A56"}, {"offset": 0.7, "color": "#1A2C38"},
    {"offset": 1, "color": "#0C141C"}]}}
TOWER = "#2A2E36"
RUST = "#8A5A34"
CONSOLE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3A4656"}, {"offset": 1, "color": "#222B38"}]}}
QUILL = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#C9DCE4"}, {"offset": 0.55, "color": "#8FAEBE"},
    {"offset": 1, "color": "#5E7A8E"}]}}
QUILL_CORE = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E4F0F4"}, {"offset": 1, "color": "#9AB8C6"}]}}
GHOST = "#7FE0CE"
DIAL = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4E5E74"}, {"offset": 1, "color": "#2A3444"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#4E7A8A", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C4E4EA", strokeWidth=3, opacity=40)
for i, (x, y, w) in enumerate([(193,232,8),(800,234,7),(158,522,9),(835,542,8),
                               (245,768,7),(755,746,9),(132,392,6),(862,394,7),
                               (390,110,7),(614,112,8),(332,824,6),(666,818,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#2E4450", opacity=45, stroke=NONE)

# --- the Static Spire: crumbling tower of rusted antennae, left -------------------
# main mast, slightly leaning, kept clear of the plate rim
d.path("M258,700 L242,230 L254,228 L272,700 Z", "Mast",
       fill=TOWER, stroke=INK, strokeWidth=5, join="round")
d.path("M242,230 L248,200 L254,228", "Mast tip", fill=TOWER,
       stroke=INK, strokeWidth=4, join="round")
# crossarms with antenna rods, some whole, some snapped off
for i, (y, wl, wr, tilt) in enumerate([(250, 70, 75, 0), (310, 95, 65, -2),
                                       (375, 65, 85, 3), (440, 85, 55, -3)]):
    d.path(f"M{250-wl},{y+tilt} L{260+wr},{y-tilt}", f"Crossarm {i+1}",
           fill=NONE, stroke=TOWER, strokeWidth=8, cap="round")
    for j, (ex, ey, ln) in enumerate([(250-wl, y+tilt, 34), (260+wr, y-tilt, 36),
                                      (205, y+tilt-4, 26)]):
        if (i + j) % 3 == 2:
            continue
        d.path(f"M{ex},{ey} L{ex},{ey-ln}", f"Rod {i+1}-{j+1}", fill=NONE,
               stroke=TOWER, strokeWidth=5, cap="round")
# one snapped rod dangling
d.path("M310,268 C318,288 316,306 306,320", "Snapped rod", fill=NONE,
       stroke=TOWER, strokeWidth=5, cap="round")
# bent whip antenna at the tip
d.path("M248,200 C244,178 250,162 262,152", "Whip antenna", fill=NONE,
       stroke=TOWER, strokeWidth=5, cap="round")
# small dish, tilted down like it gave up
d.path("M272,340 C300,330 318,342 322,366 C298,372 278,362 272,340 Z",
       "Dish", fill=TOWER, stroke=INK, strokeWidth=4, join="round")
# rust streaks bleeding down the mast
for i, (x, y, ln) in enumerate([(246, 220, 60), (258, 300, 80), (250, 420, 90),
                                (262, 200, 40)]):
    d.path(f"M{x},{y} L{x+4},{y+ln}", f"Rust {i+1}", fill=NONE,
           stroke=RUST, strokeWidth=4, opacity=55, cap="round")
# crumbling base rubble
for i, (x, y, w, h) in enumerate([(205, 690, 40, 22), (255, 700, 34, 18),
                                  (222, 668, 26, 16)]):
    d.shape("ellipse", f"Rubble {i+1}", x=x, y=y, width=w, height=h,
            fill=TOWER, opacity=80, stroke=INK, strokeWidth=3)

# signal rings still leaking out of the tip — the tower half-remembers
for i, r_ in enumerate((25, 45, 62)):
    d.path(f"M{248-r_},190 A{r_},{r_} 0 0 1 {248+r_},190",
           f"Signal ring {i+1}", fill=NONE, stroke=GHOST, strokeWidth=3,
           opacity=30-8*i, dash=[6, 10])

# --- floor ----------------------------------------------------------------------
d.shape("ellipse", "Floor", x=170, y=690, width=660, height=115,
        fill="#0E1A22", opacity=85, stroke=NONE)
d.shape("ellipse", "Tower shadow", x=195, y=700, width=130, height=26,
        fill="#04080C", opacity=55, stroke=NONE)
d.shape("ellipse", "Quill shadow", x=400, y=716, width=170, height=30,
        fill="#04080C", opacity=55, stroke=NONE)
d.shape("ellipse", "Console shadow", x=570, y=712, width=250, height=30,
        fill="#04080C", opacity=55, stroke=NONE)

# --- spectral ledger, open and glowing, floating left of the console -----------------
d.shape("ellipse", "Ledger aura", x=300, y=520, width=190, height=130,
        fill=GHOST, opacity=12, stroke=NONE)
d.path("M330,560 C356,544 386,544 400,556 C414,544 444,544 470,560 "
       "L470,618 C444,604 414,604 400,614 C386,604 356,604 330,618 Z",
       "Ledger open", fill="#1E3A38", stroke=GHOST, strokeWidth=3,
       join="round", opacity=92)
d.path("M400,556 L400,614", "Ledger spine", fill=NONE, stroke=GHOST,
       strokeWidth=2, opacity=80)
for i, y in enumerate((570, 582, 594)):
    d.path(f"M340,{y} C358,{y-6} 380,{y-6} 392,{y}", f"Page line L{i+1}",
           fill=NONE, stroke=GHOST, strokeWidth=2, opacity=55)
    d.path(f"M408,{y} C420,{y-6} 442,{y-6} 460,{y}", f"Page line R{i+1}",
           fill=NONE, stroke=GHOST, strokeWidth=2, opacity=55)
# ink drifting up off the page — entries writing themselves
for i, (x, y, w) in enumerate([(352,528,6),(396,512,5),(438,522,6),(372,494,4)]):
    d.shape("ellipse", f"Ink mote {i+1}", x=x, y=y, width=w, height=w,
            fill=GHOST, opacity=60, stroke=NONE)

# --- radio console ------------------------------------------------------------------
d.shape("rectangle", "Console", x=560, y=470, width=255, height=250,
        fill=CONSOLE, stroke=INK, strokeWidth=6, radius=12)
d.shape("rectangle", "Console face", x=576, y=486, width=223, height=218,
        fill="#161E2A", stroke=INK, strokeWidth=4, radius=8)
# frequency readout — digits need Source Sans 3 (Virelai Sans has none)
d.shape("rectangle", "Readout", x=592, y=502, width=120, height=34,
        fill="#0A1210", stroke="#3E5A52", strokeWidth=3, radius=4)
d.text("88.3", "Frequency", x=610, y=527, size=22, font="Source Sans 3",
       color=GHOST, justify="left")
d.text("FM", "Band", x=682, y=527, size=13, font="Virelai Sans",
       color="#5E8A80", justify="left")
# signal meter
d.shape("rectangle", "Meter bg", x=592, y=548, width=190, height=10,
        fill="#0E141C", stroke=NONE, radius=5)
d.shape("rectangle", "Meter fill", x=592, y=548, width=118, height=10,
        fill=GHOST, opacity=75, stroke=NONE, radius=5)
# the big tuning dial her hand rests on
d.shape("ellipse", "Dial glow", x=600, y=576, width=105, height=105,
        fill=GHOST, opacity=10, stroke=NONE)
d.shape("ellipse", "Tuning dial", x=610, y=586, width=85, height=85,
        fill=DIAL, stroke=INK, strokeWidth=5)
for a in range(0, 360, 30):
    t = math.radians(a)
    x1 = 652 + 34*math.cos(t); y1 = 628 + 34*math.sin(t)
    x2 = 652 + 40*math.cos(t); y2 = 628 + 40*math.sin(t)
    d.path(f"M{x1:.0f},{y1:.0f} L{x2:.0f},{y2:.0f}", f"Dial tick {a}",
           fill=NONE, stroke="#7E94AC", strokeWidth=3)
d.shape("ellipse", "Dial knob", x=640, y=616, width=25, height=25,
        fill="#8A744E", stroke=INK, strokeWidth=3)
# two smaller dials + a row of station buttons
for i, x in enumerate((735, 770)):
    d.shape("ellipse", f"Small dial {i+1}", x=x, y=606, width=26, height=26,
            fill=DIAL, stroke=INK, strokeWidth=3)
    d.path(f"M{x+13},{606+13} L{x+13},{606+4}",
           f"Small dial mark {i+1}", fill=NONE, stroke="#7E94AC", strokeWidth=3)
for i in range(4):
    d.shape("rectangle", f"Button {i+1}", x=724+i*18, y=650, width=12, height=9,
            fill=GHOST if i == 2 else "#2E3A48", stroke=INK,
            strokeWidth=2, radius=2, opacity=90 if i == 2 else 100)
# speaker grille
d.path("M592,684 L700,684 M592,696 L700,696 M592,708 L700,708",
       "Speaker grille", fill=NONE, stroke="#0E141C", strokeWidth=5,
       cap="round")

# --- Quill herself: a spectral quill-figure -------------------------------------------
# body: feather-shaped — wide shoulders tapering to a drifting quill tip
d.path("M480,330 C530,330 560,380 562,450 C564,520 540,600 520,660 "
       "C508,700 500,730 506,760 C486,742 470,700 462,650 "
       "C450,580 440,500 446,430 C450,380 458,340 480,330 Z",
       "Quill body", fill=QUILL, stroke=INK, strokeWidth=6, opacity=94)
# feather barbs down both sides — her namesake
d.path("M452,420 C466,430 480,432 494,428 M448,470 C464,480 480,482 496,478 "
       "M448,520 C462,530 476,532 490,528 M452,570 C464,578 476,580 488,576",
       "Barbs L", fill=NONE, stroke="#5E7A8E", strokeWidth=4, opacity=70,
       cap="round")
d.path("M556,440 C544,450 532,452 520,448 M560,492 C548,502 534,504 522,500 "
       "M556,544 C546,552 534,554 524,550",
       "Barbs R", fill=NONE, stroke="#5E7A8E", strokeWidth=4, opacity=70,
       cap="round")
# pale chest core where the signal lives
d.shape("ellipse", "Chest core", x=472, y=430, width=56, height=80,
        fill=QUILL_CORE, opacity=55, stroke=NONE)
d.shape("ellipse", "Core glow", x=484, y=456, width=32, height=32,
        fill=GHOST, opacity=35, stroke=NONE)
# head merges with the feather; sad, listening eyes
d.shape("ellipse", "Eye L", x=466, y=378, width=14, height=18, fill=INK, stroke=NONE)
d.shape("ellipse", "Eye R", x=510, y=378, width=14, height=18, fill=INK, stroke=NONE)
d.shape("ellipse", "Glint L", x=469, y=382, width=4, height=4,
        fill="#FFFFFF", opacity=85, stroke=NONE)
d.shape("ellipse", "Glint R", x=513, y=382, width=4, height=4,
        fill="#FFFFFF", opacity=85, stroke=NONE)
# worried brows slanting up toward the middle — melancholic yet persistent
d.path("M460,376 L482,366", "Brow L", fill=NONE, stroke=INK, strokeWidth=4, cap="round")
d.path("M508,366 L530,376", "Brow R", fill=NONE, stroke=INK, strokeWidth=4, cap="round")
d.path("M482,412 C490,408 500,408 506,412", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
# arm reaching the tuning dial
d.path("M540,520 C570,540 600,570 636,610", "Arm to dial", fill=NONE,
       stroke="#8FAEBE", strokeWidth=13, cap="round")
d.shape("ellipse", "Hand on dial", x=626, y=598, width=22, height=19,
        fill="#A8C4D2", stroke=INK, strokeWidth=3)
# other hand hovering over the spectral ledger
d.path("M452,540 C438,556 426,564 412,568", "Arm to ledger", fill=NONE,
       stroke="#8FAEBE", strokeWidth=12, cap="round")
d.shape("ellipse", "Hand over ledger", x=398, y=560, width=19, height=16,
        fill="#A8C4D2", stroke=INK, strokeWidth=3)

# --- static: sparks and hiss around the dial hand -------------------------------------
d.path("M700,560 L712,544 L704,542 L718,524", "Static spark 1", fill=NONE,
       stroke=GHOST, strokeWidth=4, cap="round", join="round", opacity=85)
d.path("M680,520 L688,506 L682,504 L692,490", "Static spark 2", fill=NONE,
       stroke=GHOST, strokeWidth=3, cap="round", join="round", opacity=60)
for i, (x, y, w) in enumerate([(716,560,6),(734,540,5),(700,584,5),
                               (726,506,4),(688,548,4)]):
    d.shape("ellipse", f"Hiss {i+1}", x=x, y=y, width=w, height=w,
            fill=GHOST, opacity=55, stroke=NONE)
# faint echo wave from the dial toward Quill's ear — every echo finds her
d.path("M600,540 C560,500 540,460 528,420", "Echo arc 1", fill=NONE,
       stroke=GHOST, strokeWidth=3, opacity=40, dash=[5, 9])
d.path("M616,556 C570,510 552,470 544,430", "Echo arc 2", fill=NONE,
       stroke=GHOST, strokeWidth=3, opacity=25, dash=[5, 9])

# --- captions ---------------------------------------------------------------------------
d.text("QUILL STATICVOX", "Name", x=500, y=930, size=58,
       font="Virelai Sans", color="#D8E8EE", justify="center")
r = d.text("ECHO PRESERVER", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#8FB4BC", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("201.quill-staticvox-V1R00")
