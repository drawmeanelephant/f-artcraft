#!/usr/bin/env python3
"""Updatey Delaybot — mascot portrait V1R00. Maintenance Window.
A droopy little kiosk robot slumped against a monitor whose progress bar
has been stuck at 99% since yesterday; a RESTART NOW prompt glows
beneath it, cursor spinning, one antenna folded in defeat. Amber-CRT
plate on a night-shift backdrop. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Digits (99%) in Source Sans 3 — Virelai carries no figures.
Plate = circle (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Updatey Delaybot — Mascot Portrait", 1000, 1000)

INK = "#261E14"   # warm dark ink, never black
BG_GRAD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000], "stops": [
    {"offset": 0, "color": "#1A140E"}, {"offset": 1, "color": "#0A0705"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#8A7440"}, {"offset": 0.62, "color": "#5A4A28"},
    {"offset": 1, "color": "#2A2110"}]}}
BOT_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#C8CCCE"}, {"offset": 0.7, "color": "#969CA2"},
    {"offset": 1, "color": "#5E646C"}]}}
BEZEL_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4A4E54"}, {"offset": 1, "color": "#22262C"}]}}
SCREEN_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#3A2E12"}, {"offset": 0.75, "color": "#241B0A"},
    {"offset": 1, "color": "#140E05"}]}}
AMBER = "#F0B43C"
AMBER_DIM = "#8A6420"
GLOW = "#FFD98A"

PCX, PCY, PR = 500, 460, 420

def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

def faint_text(t, label, opacity, **kw):
    r = d.text(t, label, **kw)
    if r and r.get("id"):
        d.cmd("object.setProps", f"{label} opacity", id=r["id"],
              opacity=opacity)

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#8A7040", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#1C1408", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#EADCB0", strokeWidth=3, opacity=28)
d.shape("ellipse", "Patina 1", x=200, y=560, width=250, height=150,
        fill="#9A8250", opacity=16, stroke=NONE)
d.shape("ellipse", "Patina 2", x=560, y=220, width=260, height=150,
        fill="#3A2E16", opacity=32, stroke=NONE)
for i, (x, y, w) in enumerate([(225,345,5),(788,340,6),(185,548,5),(838,575,5),
                               (258,758,5),(728,762,6),(165,452,5),(850,648,5),
                               (435,132,5),(598,142,6),(338,168,4),(702,205,5),
                               (252,658,4),(662,718,5)]):
    assert on_disc(x, y, 12), (x, y)
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#F4E4B4", opacity=28, stroke=NONE)
# ghost arcs on the dark backdrop
d.path("M932,162 A100,100 0 0 0 852,72", "Ghost arc TR",
       fill=NONE, stroke="#9A7C48", strokeWidth=14, opacity=10, cap="round")
d.path("M78,778 A115,115 0 0 0 182,880", "Ghost arc BL",
       fill=NONE, stroke="#9A7C48", strokeWidth=10, opacity=8, cap="round")

# --- the monitor: bezel, stand, glowing screen --------------------------------
d.shape("ellipse", "Monitor shadow", x=400, y=680, width=380, height=42,
        fill="#0A0704", opacity=45, stroke=NONE)
d.shape("rectangle", "Stand neck", x=560, y=620, width=44, height=52,
        fill="#3A3E44", stroke=INK, strokeWidth=4)
d.path("M520,672 L644,672 C654,672 660,680 656,688 L508,688 C504,680 510,672 520,672 Z",
       "Stand foot", fill="#3A3E44", stroke=INK, strokeWidth=4)
d.shape("rectangle", "Bezel", x=390, y=250, width=380, height=380,
        radius=22, fill=BEZEL_GRAD, stroke=INK, strokeWidth=5)
d.shape("rectangle", "Screen", x=414, y=274, width=332, height=290,
        radius=10, fill=SCREEN_GRAD, stroke="#0E0A04", strokeWidth=3)
# screen glass sweep
d.path("M430,290 L560,290 L470,548 L430,548 Z", "Glass sweep",
       fill="#FFF4D8", opacity=6, stroke=NONE)
# screen top label — amber system header
d.text("SYSTEM UPDATE", "Screen header", x=580, y=310, size=16,
       font="Source Sans 3", color=AMBER_DIM, justify="center")

# the progress bar — 99% forever
d.shape("rectangle", "Bar track", x=452, y=368, width=256, height=34,
        radius=17, fill="#120C04", stroke=AMBER_DIM, strokeWidth=2.5)
d.path("M469,385 L694,385", "Bar fill", fill=NONE, stroke=AMBER,
       strokeWidth=18, cap="round", opacity=90)
d.path("M469,385 L694,385", "Bar shine", fill=NONE, stroke=GLOW,
       strokeWidth=6, cap="round", opacity=60)
# the last 1% that never comes — empty cap glows faint
d.shape("ellipse", "Missing cap", x=688, y=371, width=28, height=28,
        fill=NONE, stroke=AMBER, strokeWidth=2, dash=[3, 4], opacity=45)
faint_text("99%", "Percent", 100, x=580, y=352, size=30,
           font="Source Sans 3", color=AMBER, justify="center")

# spinning wait cursor at the bar's stalled end — dashed circle mid-spin
d.shape("ellipse", "Wait cursor", x=690, y=330, width=30, height=30,
        fill=NONE, stroke=AMBER, strokeWidth=3.5, dash=[6, 7],
        opacity=80)

# restart prompt below the bar
d.shape("rectangle", "Prompt box", x=478, y=436, width=204, height=88,
        radius=10, fill="#2A2010", stroke=AMBER_DIM, strokeWidth=2.5,
        opacity=95)
d.text("RESTART REQUIRED", "Prompt title", x=580, y=462, size=15,
       font="Source Sans 3", color=GLOW, justify="center")
d.shape("rectangle", "Restart button", x=512, y=476, width=136, height=32,
        radius=16, fill=AMBER, stroke=INK, strokeWidth=3)
d.text("RESTART NOW", "Button label", x=580, y=498, size=14,
       font="Source Sans 3", color="#2A1E08", justify="center")
# do-not-turn-off whisper
faint_text("do not turn off", "Whisper", 60, x=580, y=548, size=14,
           font="Source Sans 3", color=AMBER_DIM, justify="center")

# --- Updatey the robot ---------------------------------------------------------
d.shape("ellipse", "Bot shadow", x=160, y=760, width=260, height=40,
        fill="#0A0704", opacity=45, stroke=NONE)
# tread feet
d.shape("rectangle", "Foot L", x=190, y=746, width=70, height=30, radius=14,
        fill="#3A3E44", stroke=INK, strokeWidth=3.5)
d.shape("rectangle", "Foot R", x=290, y=746, width=70, height=30, radius=14,
        fill="#3A3E44", stroke=INK, strokeWidth=3.5)
# body — rounded torso leaning slightly toward the screen
d.path("M275,470 C215,478 178,540 180,620 C182,700 220,748 278,748 "
       "C336,748 372,700 372,620 C374,540 335,478 275,470 Z",
       "Body", fill=BOT_GRAD, stroke=INK, strokeWidth=5)
# belly panel — a status LED and vent lines
d.shape("rectangle", "Belly panel", x=222, y=600, width=106, height=96,
        radius=12, fill="#7E848C", stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Status LED", x=240, y=618, width=14, height=14,
        fill=AMBER, stroke=NONE)
d.shape("ellipse", "Status glow", x=234, y=612, width=26, height=26,
        fill=AMBER, opacity=30, stroke=NONE)
for j, yy in enumerate((648, 662, 676)):
    d.path(f"M244,{yy} L312,{yy}", f"Vent {j+1}",
           fill=NONE, stroke="#4A4E54", strokeWidth=5, cap="round",
           opacity=70)
# rim light + shade
d.path("M196,540 C188,590 190,650 204,700", "Rim light",
       fill=NONE, stroke="#E8ECEF", strokeWidth=4, opacity=40, cap="round")
d.path("M352,540 C360,590 358,660 344,706 C356,660 354,596 344,548 Z",
       "Body shade", fill="#4A4E56", opacity=35, stroke=NONE)

# head dome merged into body top; droopy antenna, one folded
d.path("M276,470 L276,440", "Antenna stem L",
       fill=NONE, stroke=INK, strokeWidth=5, cap="round")
d.shape("ellipse", "Antenna tip L", x=270, y=424, width=12, height=12,
        fill=AMBER, stroke=INK, strokeWidth=2)
# folded antenna — bent over in defeat
d.path("M320,474 C330,450 348,442 366,446 C352,452 344,464 342,478",
       "Antenna folded", fill=NONE, stroke=INK, strokeWidth=5,
       cap="round")
d.shape("ellipse", "Folded tip", x=360, y=440, width=12, height=12,
        fill="#7E848C", stroke=INK, strokeWidth=2)

# face: heavy-lidded exhausted eyes, flat mouth
d.path("M222,540 C236,532 254,532 266,540 C254,548 236,548 222,540 Z",
       "Eye L", fill="#F4F0E4", stroke=INK, strokeWidth=3.5)
d.path("M290,540 C304,532 322,532 334,540 C322,548 304,548 290,540 Z",
       "Eye R", fill="#F4F0E4", stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Pupil L", x=240, y=537, width=9, height=9,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Pupil R", x=308, y=537, width=9, height=9,
        fill=INK, stroke=NONE)
# drooping lids
d.path("M220,536 C238,527 258,527 268,536", "Lid L",
       fill=NONE, stroke=INK, strokeWidth=4, cap="round")
d.path("M288,536 C306,527 326,527 336,536", "Lid R",
       fill=NONE, stroke=INK, strokeWidth=4, cap="round")
# bags under the eyes
d.path("M232,558 C242,562 254,562 262,558", "Bag L",
       fill=NONE, stroke="#5E646C", strokeWidth=2.5, cap="round", opacity=70)
d.path("M298,558 C308,562 320,562 328,558", "Bag R",
       fill=NONE, stroke="#5E646C", strokeWidth=2.5, cap="round", opacity=70)
d.path("M252,586 L302,586", "Mouth",
       fill=NONE, stroke=INK, strokeWidth=4, cap="round")

# left arm dangles; right arm props against the monitor bezel
d.path("M188,600 C166,630 162,668 174,696 C186,702 198,694 198,680 "
       "C192,656 196,630 206,612 Z",
       "Arm L", fill=BOT_GRAD, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Hand L", x=166, y=686, width=28, height=26,
        fill="#969CA2", stroke=INK, strokeWidth=3)
d.path("M366,556 C390,540 404,520 410,498 C422,494 432,504 428,516 "
       "C420,540 400,562 380,576 Z",
       "Arm R", fill=BOT_GRAD, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Hand R", x=404, y=492, width=28, height=28,
        fill="#969CA2", stroke=INK, strokeWidth=3)

# "…" sigh drifting up from the dome
faint_text("...", "Sigh", 55, x=350, y=400, size=34,
           font="Source Sans 3", color=GLOW, justify="center")

# --- name + role ----------------------------------------------------------------------
d.text("UPDATEY DELAYBOT", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#F0E4C4", justify="center")
r = d.text("MAINTENANCE WINDOW", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#D0B87E", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("049.updatey-delaybot-V1R00")
