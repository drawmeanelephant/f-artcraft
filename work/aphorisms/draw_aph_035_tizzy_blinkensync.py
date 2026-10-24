#!/usr/bin/env python3
"""APH-035 Tizzy Blinkensync — motivational-poster aphorism plate V1R00.
A LOADING... poster that never completes: a smartphone that never booted,
its screen lit with a ghost grid of apps that installed anyway, a status
bar with no time and no signal, and a progress bar parked at 99% with
corporate-optimism blue. Ghost apps drift outside the glass, still
arriving. Periwinkle night, hopeful gold accent. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("APH-035 Tizzy Blinkensync — Motivational Poster", 1000, 1000)

INK = "#101222"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1E2238"}, {"offset": 1, "color": "#0A0C16"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#444C74"}, {"offset": 0.7, "color": "#232742"},
    {"offset": 1, "color": "#101222"}]}}
POSTER_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#252A44"}, {"offset": 1, "color": "#12142A"}]}}
PHONE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#343C5C"}, {"offset": 1, "color": "#181C32"}]}}
SCR_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#242C50"}, {"offset": 0.7, "color": "#141834"},
    {"offset": 1, "color": "#0C0E1C"}]}}
BAR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#8FC4F8"}, {"offset": 1, "color": "#4E7FD8"}]}}
TRACK_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1A2038"}, {"offset": 1, "color": "#12162A"}]}}
GOLD = "#F0C860"
FRAME = "#A8B0D0"
HEAD = "#EEF0F8"
PUNCH = "#D4D8EA"
CREAM = "#EEF0F8"
FAINT = "#8A90B0"
BLUE = "#7FB8F0"
GHOST = "#5E6A8C"
REDL = "#E86A5A"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#5A6494", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#B8C4E8", strokeWidth=3, opacity=30)
d.shape("ellipse", "Patina 1", x=200, y=170, width=200, height=110,
        fill="#3E4670", opacity=20, stroke=NONE)
d.shape("ellipse", "Patina 2", x=620, y=620, width=200, height=110,
        fill="#3E4670", opacity=16, stroke=NONE)
for i, (x, y, w) in enumerate([(215, 280, 7), (790, 255, 8), (165, 480, 6),
                               (838, 475, 7), (250, 655, 6), (755, 665, 7)]):
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#56629A", opacity=35, stroke=NONE)
# buffering dots on the plate, never resolving
for i, (x, y, op) in enumerate([(270, 215, 50), (292, 208, 38),
                                 (314, 203, 26), (690, 580, 50),
                                 (712, 588, 38), (732, 598, 26)]):
    d.shape("ellipse", f"Buffer {i+1}", x=x, y=y, width=6, height=6,
            fill=BLUE, opacity=op, stroke=NONE)

# --- the poster card -------------------------------------------------------------
PX, PY, PW, PH = 220, 150, 560, 440
d.shape("rectangle", "Poster shadow", x=PX + 8, y=PY + 10, width=PW,
        height=PH, fill="#000000", opacity=35, stroke=NONE)
d.shape("rectangle", "Poster", x=PX, y=PY, width=PW, height=PH,
        fill=POSTER_GRAD, stroke="#3E4668", strokeWidth=4)
d.shape("rectangle", "Frame outer", x=PX + 16, y=PY + 16,
        width=PW - 32, height=PH - 32, fill=NONE, stroke=FRAME,
        strokeWidth=2, opacity=80)
d.shape("rectangle", "Frame inner", x=PX + 24, y=PY + 24,
        width=PW - 48, height=PH - 48, fill=NONE, stroke=GOLD,
        strokeWidth=1.5, opacity=60)

# kicker + headline
r = d.text("LOADING...", "Kicker", x=500, y=PY + 44, size=12,
           font="Virelai Sans", color=GOLD, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "kicker tracking", ids=[r["id"]], tracking=280)
r = d.text("THE INTERFACE IS FULLY LOADED", "Headline", x=500, y=PY + 80,
           size=27, font="Virelai Sans", color=HEAD, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "headline tracking", ids=[r["id"]], tracking=15)
d.path("M350,254 L472,254 M528,254 L650,254", "Headline rules", fill=NONE,
       stroke=GOLD, strokeWidth=2, opacity=80)
d.path(rot_rect_path(500, 254, 10, 10, 45), "Headline diamond",
       fill=GOLD, opacity=85, stroke=NONE)

# --- ghost apps still arriving, outside the glass ------------------------------------
for i, (ax, ay, op) in enumerate([(318, 350, 26), (330, 428, 20),
                                  (660, 372, 24)]):
    d.shape("rectangle", f"Ghost app {i+1}", x=ax, y=ay, width=22,
            height=22, radius=6, fill=NONE, stroke=GHOST, strokeWidth=2,
            opacity=op)
    d.shape("ellipse", f"Ghost app dot {i+1}", x=ax + 8, y=ay + 8,
            width=6, height=6, fill=GHOST, opacity=op, stroke=NONE)
# dashed install paths that never reach the phone
d.path("M342,361 C372,361 400,368 424,380", "Install path 1", fill=NONE,
       stroke=GHOST, strokeWidth=2, dash=[4, 5], cap="round", opacity=30)
d.path("M354,439 C380,436 402,432 424,428", "Install path 2", fill=NONE,
       stroke=GHOST, strokeWidth=2, dash=[4, 5], cap="round", opacity=26)
d.path("M658,383 C636,386 612,392 578,402", "Install path 3", fill=NONE,
       stroke=GHOST, strokeWidth=2, dash=[4, 5], cap="round", opacity=30)

# --- the phone that never turned on ------------------------------------------------------
HX, HY, HW, HH = 430, 290, 140, 212
d.shape("ellipse", "Phone shadow", x=HX - 10, y=HY + HH - 4,
        width=HW + 20, height=12, fill="#000000", opacity=35, stroke=NONE)
# dead side buttons
d.shape("rectangle", "Power button", x=HX + HW, y=HY + 44, width=4,
        height=26, radius=2, fill="#222842", stroke="#0C0E1C",
        strokeWidth=1.5)
d.shape("rectangle", "Vol button", x=HX - 4, y=HY + 36, width=4,
        height=18, radius=2, fill="#222842", stroke="#0C0E1C",
        strokeWidth=1.5)
d.shape("rectangle", "Phone body", x=HX, y=HY, width=HW, height=HH,
        radius=18, fill=PHONE_GRAD, stroke="#0A0C18", strokeWidth=3)
# glass edge sheen
d.path(f"M{HX + 8},{HY + 30} Q{HX + 6},{HY + 10} {HX + 24},{HY + 6}",
       "Glass sheen", fill=NONE, stroke="#9AA8D8", strokeWidth=2,
       cap="round", opacity=40)
# screen
SX, SY, SW, SH = HX + 8, HY + 14, HW - 16, HH - 28
d.shape("rectangle", "Screen", x=SX, y=SY, width=SW, height=SH,
        radius=10, fill=SCR_GRAD, stroke="#080A14", strokeWidth=2)
# the almost-on glow, warm at the core
d.shape("ellipse", "Boot glow", x=SX + 20, y=SY + 30, width=SW - 40,
        height=90, fill=BLUE, opacity=8, stroke=NONE)

# status bar: no time, no signal, no battery
d.text("--:--", "Status time", x=SX + 10, y=SY + 14, size=8,
       font="Source Sans 3", color=FAINT, justify="left")
# signal bars, all empty
for i in range(4):
    bx = SX + SW - 56 + i * 7
    d.shape("rectangle", f"Sig bar {i+1}", x=bx, y=SY + 12 - i * 2,
            width=4, height=5 + i * 2, radius=1, fill=NONE,
            stroke=GHOST, strokeWidth=1.5, opacity=60)
# battery outline, one red sliver
BX, BY = SX + SW - 26, SY + 8
d.shape("rectangle", "Battery", x=BX, y=BY, width=16, height=9, radius=2,
        fill=NONE, stroke=GHOST, strokeWidth=1.5, opacity=70)
d.shape("rectangle", "Battery nub", x=BX + 16, y=BY + 2.5, width=2.5,
        height=4, radius=1, fill=GHOST, opacity=70, stroke=NONE)
d.shape("rectangle", "Battery sliver", x=BX + 2, y=BY + 2, width=3,
        height=5, radius=1, fill=REDL, opacity=85, stroke=NONE)

# ghost app grid — fully loaded, none of them real
for row in range(3):
    for col in range(4):
        ax = SX + 12 + col * 27
        ay = SY + 34 + row * 30
        if row == 2 and col == 3:
            # one slot is still installing, forever
            d.shape("rectangle", "App installing", x=ax, y=ay, width=21,
                    height=21, radius=6, fill=NONE, stroke=BLUE,
                    strokeWidth=2, dash=[3, 3], opacity=55)
            d.path(f"M{ax + 10.5},{ay + 6} L{ax + 10.5},{ay + 14} "
                   f"M{ax + 7},{ay + 12} L{ax + 10.5},{ay + 15} "
                   f"L{ax + 14},{ay + 12}", "Install arrow", fill=NONE,
                   stroke=BLUE, strokeWidth=1.5, cap="round", opacity=55)
        else:
            d.shape("rectangle", f"App {row}.{col}", x=ax, y=ay, width=21,
                    height=21, radius=6, fill=GHOST, opacity=14,
                    stroke=GHOST, strokeWidth=1.5)
            d.shape("ellipse", f"App dot {row}.{col}", x=ax + 7.5,
                    y=ay + 7.5, width=6, height=6, fill=GHOST,
                    opacity=18, stroke=NONE)

# the progress bar, parked at 99%
TBX, TBY, TBW, TBH = SX + 12, SY + SH - 50, SW - 24, 9
d.shape("rectangle", "Progress track", x=TBX, y=TBY, width=TBW,
        height=TBH, radius=4.5, fill=TRACK_GRAD, stroke="#2A3050",
        strokeWidth=1.5)
d.shape("rectangle", "Progress fill", x=TBX + 1.5, y=TBY + 1.5,
        width=(TBW - 3) * 0.99, height=TBH - 3, radius=3,
        fill=BAR_GRAD, stroke=NONE)
# the last percent that will never fill
d.shape("ellipse", "Stall pip", x=TBX + TBW - 6, y=TBY + 2, width=5,
        height=5, fill=NONE, stroke=GOLD, strokeWidth=1.5, opacity=80)
d.text("99%", "Progress label", x=SX + SW/2, y=TBY + 24, size=11,
       font="Source Sans 3", color=BLUE, justify="center")
# home indicator
d.shape("rectangle", "Home bar", x=SX + SW/2 - 22, y=SY + SH - 8,
        width=44, height=4, radius=2, fill=GHOST, opacity=45, stroke=NONE)

# microcopy under the phone
d.text("PLEASE WAIT — PURGATORY STILL RENDERING", "Microcopy", x=500,
       y=HY + HH + 20, size=8, font="Source Sans 3", color=FAINT,
       justify="center")

# --- punchline sub-caption -------------------------------------------------------------
r = d.text("THE DEVICE WILL NEVER TURN ON.", "Punchline", x=500,
           y=PY + PH - 34, size=20, font="Virelai Sans", color=PUNCH,
           justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "punch tracking", ids=[r["id"]], tracking=80)

# --- flourish on the plate below the poster ----------------------------------------------
d.path("M415,668 L485,668 M515,668 L585,668", "Flourish rules", fill=NONE,
       stroke=GOLD, strokeWidth=2, opacity=55)
d.path(rot_rect_path(500, 668, 9, 9, 45), "Flourish diamond", fill=GOLD,
       opacity=60, stroke=NONE)

# --- name + role ----------------------------------------------------------------------
d.text("TIZZY BLINKENSYNC", "Name", x=500, y=905, size=56,
       font="Virelai Sans", color=CREAM, justify="center")
r = d.text("THE INTERFACE IS FULLY LOADED", "Role", x=500, y=950,
           size=18, font="Virelai Sans", color=FAINT, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=160)

d.finish("aph-035-tizzy-blinkensync-V1R00")
