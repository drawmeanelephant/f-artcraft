#!/usr/bin/env python3
"""Staged Sobriety — mascot portrait V1R00.
Mascot at a podium before the cameras, tie straightened in the corridor
interval, expression grave; smoke clearing behind. 1000x1000.
Gradients + translucency, never flat."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Staged Sobriety — Mascot Portrait", 1000, 1000)

INK = "#232028"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#161A22"}, {"offset": 1, "color": "#080A0E"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#CAD2DC"}, {"offset": 0.7, "color": "#93A0B2"},
    {"offset": 1, "color": "#5B6579"}]}}
SUIT_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#3E4657"}, {"offset": 0.7, "color": "#272E3B"},
    {"offset": 1, "color": "#171B24"}]}}
FACE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F0D2B4"}, {"offset": 1, "color": "#D2A57F"}]}}
SHIRT_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F0EDE4"}, {"offset": 1, "color": "#D2CDBE"}]}}
WOOD_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#74512F"}, {"offset": 1, "color": "#432B19"}]}}
STEEL_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#C6CCD4"}, {"offset": 1, "color": "#7E8692"}]}}
CAM_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#343B47"}, {"offset": 1, "color": "#1B2029"}]}}
GOLD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E8C868"}, {"offset": 1, "color": "#A4803A"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#7E889C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E4E9F0", strokeWidth=3, opacity=50)
for i, (x, y, w) in enumerate([(214,228,7),(782,220,6),(244,710,7),(746,700,7),(174,454,6),
                               (830,458,6),(354,154,6),(642,148,7),(298,792,6),(702,796,6)]):
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#5F6979", opacity=38, stroke=NONE)

# --- smoke clearing behind: thin, drifting off the top of the plate ---------------
for i, (x0, y0, w0) in enumerate([(300,300,240),(560,240,300),(420,180,260),(660,330,190),(240,380,170)]):
    d.path(f"M{x0-w0/2},{y0} C{x0-w0/4},{y0-50} {x0+w0/4},{y0+50} {x0+w0/2},{y0-10}",
           f"Smoke bank {i+1}", fill=NONE, stroke="#D8DCE2",
           strokeWidth=26, cap="round", opacity=14)
for i, (x0, y0) in enumerate([(350,240),(520,200),(640,270),(440,140)]):
    d.path(f"M{x0},{y0} C{x0-20},{y0-36} {x0+18},{y0-58} {x0+2},{y0-88}",
           f"Smoke wisp {i+1}", fill=NONE, stroke="#E4E8EE",
           strokeWidth=12, cap="round", opacity=18)

# --- press cameras, flanking, aimed at the podium -----------------------------------
def camera(x, y, flip, label):
    """Press camera on a tripod, lens toward center."""
    s = -1 if flip else 1
    # tripod
    d.path(f"M{x},{y+60} L{x-28*s},{y+178} M{x},{y+60} L{x+30*s},{y+178} "
           f"M{x},{y+60} L{x+2*s},{y+182}",
           f"{label} tripod", fill=NONE, stroke=INK, strokeWidth=6, cap="round")
    # body
    d.shape("rectangle", f"{label} body", x=x-52, y=y-34, width=104, height=70,
            fill=CAM_GRAD, stroke=INK, strokeWidth=5, radius=8)
    # lens barrel pointing at the podium
    d.shape("rectangle", f"{label} lens", x=x-14 if not flip else x-36,
            y=y-12, width=50, height=34, fill="#2A3140",
            stroke=INK, strokeWidth=4, radius=6)
    d.shape("ellipse", f"{label} glass", x=(x+16 if not flip else x-34),
            y=y-6, width=20, height=22, fill=STEEL_GRAD, stroke=INK, strokeWidth=3)
    # viewfinder bump + flash
    d.shape("rectangle", f"{label} finder", x=x-12, y=y-52, width=24, height=20,
            fill=CAM_GRAD, stroke=INK, strokeWidth=4, radius=4)
    d.shape("star", f"{label} flash", cx=x, cy=y-66, radius1=16, radius2=5,
            points=4, fill="#F4E6A0", stroke=NONE, opacity=80)

camera(238, 596, False, "Camera L")
camera(764, 600, True, "Camera R")

# --- the mascot, grave, at the podium -----------------------------------------------
# torso behind the lectern
d.path("M348,720 C352,620 380,540 430,502 C456,482 544,482 570,502 "
       "C620,540 648,620 652,720 Z",
       "Suit", fill=SUIT_GRAD, stroke=INK, strokeWidth=7, join="round")
# shirt V + lapels
d.path("M458,512 L500,588 L542,512 L520,506 L500,540 L480,506 Z",
       "Shirt V", fill=SHIRT_GRAD, stroke=INK, strokeWidth=3.5, join="round")
d.path("M430,504 L478,506 L470,590 L436,560 Z", "Lapel L",
       fill="#20262F", stroke=INK, strokeWidth=4, join="round")
d.path("M570,504 L522,506 L530,590 L564,560 Z", "Lapel R",
       fill="#20262F", stroke=INK, strokeWidth=4, join="round")
# the tie, just straightened — knot crisp, blade centered
d.path("M488,514 L512,514 L516,534 L484,534 Z", "Tie knot",
       fill="#4A2E34", stroke=INK, strokeWidth=3.5, join="round")
d.path("M488,534 L516,534 L524,610 L500,640 L476,610 Z", "Tie blade",
       fill="#4A2E34", stroke=INK, strokeWidth=4, join="round")
# head: calm marble set in the doorway
d.shape("ellipse", "Head", x=410, y=310, width=180, height=172,
        fill=FACE_GRAD, stroke=INK, strokeWidth=7)
# hair: neat, side-parted
d.path("M414,364 C420,320 458,296 502,298 C548,300 580,330 586,368 "
       "C560,344 540,340 500,338 C462,336 436,346 414,364 Z",
       "Hair", fill="#2A2530", stroke=INK, strokeWidth=4, join="round")
d.path("M468,300 L464,340", "Part line", fill=NONE, stroke="#16121C",
       strokeWidth=3, opacity=60)
# grave expression: level brows, steady eyes, flat mouth
d.path("M436,386 C448,381 464,381 474,385", "Brow L",
       fill=NONE, stroke=INK, strokeWidth=4.5, cap="round")
d.path("M526,385 C536,381 552,381 564,386", "Brow R",
       fill=NONE, stroke=INK, strokeWidth=4.5, cap="round")
d.shape("ellipse", "Eye L", x=446, y=398, width=16, height=19, fill="#1E1820", stroke=NONE)
d.shape("ellipse", "Eye R", x=536, y=398, width=16, height=19, fill="#1E1820", stroke=NONE)
d.shape("ellipse", "Glint L", x=450, y=402, width=5, height=5, fill="#FFFFFF", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=540, y=402, width=5, height=5, fill="#FFFFFF", opacity=90, stroke=NONE)
d.path("M466,452 C480,456 520,456 534,452", "Grave mouth",
       fill=NONE, stroke=INK, strokeWidth=5, cap="round")
# the faint soot smudge the corridor left on his cheek
d.shape("ellipse", "Soot", x=540, y=424, width=30, height=12,
        fill="#8A7A6C", opacity=30, stroke=NONE)
d.shape("ellipse", "Cheek L", x=424, y=428, width=22, height=10, fill="#C98E72", opacity=25, stroke=NONE)

# --- the podium ----------------------------------------------------------------------
d.shape("ellipse", "Podium shadow", x=350, y=792, width=320, height=26,
        fill="#3E4657", opacity=40, stroke=NONE)
d.path("M382,640 L618,640 L640,800 L360,800 Z", "Podium",
       fill=WOOD_GRAD, stroke=INK, strokeWidth=6, join="round")
# slanted top
d.path("M372,618 L628,618 L640,646 L360,646 Z", "Podium top",
       fill=WOOD_GRAD, stroke=INK, strokeWidth=6, join="round")
# official seal on the front
d.shape("ellipse", "Seal", x=460, y=676, width=80, height=80,
        fill=GOLD, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Seal ring", x=474, y=690, width=52, height=52,
        fill=NONE, stroke="#6A4E22", strokeWidth=3, opacity=80)
d.shape("star", "Seal mark", cx=500, cy=716, radius1=16, radius2=6,
        points=5, fill="#6A4E22", stroke=NONE, opacity=85)
# podium panel lines
d.path("M400,672 L440,672 M560,672 L600,672 M404,720 L440,720 M560,720 L596,720",
       "Podium panels", fill=NONE, stroke="#33200F", strokeWidth=4,
       cap="round", opacity=55)
# microphones: two stalks leaning in from the top
d.path("M470,618 C464,580 458,556 446,540", "Mic L stem",
       fill=NONE, stroke=INK, strokeWidth=5, cap="round")
d.shape("ellipse", "Mic L", x=428, y=522, width=34, height=24,
        fill=CAM_GRAD, stroke=INK, strokeWidth=4)
d.path("M530,618 C536,580 542,556 554,540", "Mic R stem",
       fill=NONE, stroke=INK, strokeWidth=5, cap="round")
d.shape("ellipse", "Mic R", x=538, y=522, width=34, height=24,
        fill=CAM_GRAD, stroke=INK, strokeWidth=4)

# --- hands: left flat on the podium top, right still at the tie -----------------------
d.shape("ellipse", "Hand podium", x=392, y=600, width=48, height=26,
        fill=FACE_GRAD, stroke=INK, strokeWidth=4)
d.path("M400,610 L432,610", "Knuckles", fill=NONE, stroke=INK,
       strokeWidth=2.5, opacity=60)
# hand at the knot — the interval no footage covers
d.shape("ellipse", "Hand tie", x=512, y=508, width=34, height=40,
        fill=FACE_GRAD, stroke=INK, strokeWidth=4)
d.path("M518,522 C524,528 532,528 538,522", "Grip",
       fill=NONE, stroke=INK, strokeWidth=2.5, cap="round", opacity=70)
# sleeve edge where the arm meets the knot hand
d.path("M548,540 C560,560 566,584 570,606 L544,614 C540,590 534,566 524,548 Z",
       "Sleeve knot", fill=SUIT_GRAD, stroke=INK, strokeWidth=4)

# --- name + role -------------------------------------------------------------------
d.text("STAGED SOBRIETY", "Name", x=500, y=930, size=60,
       font="Virelai Sans", color="#E4E9F0", justify="center")
r = d.text("POST-CRISIS OPTICS", "Role", x=500, y=968,
           size=23, font="Virelai Sans", color="#A6B0C2", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("312.staged-sobriety-V1R00")
