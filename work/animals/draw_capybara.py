#!/usr/bin/env python3
"""Capybara — field-guide plate V1R00. The unbothered king, loafing full-body
in profile facing left, half-submerged: boxy head, calm half-lidded eye, a yuzu
balanced on top. Wet olive/brown palette; translucent water band across the
lower plate, closed on the disc's own arc so it never leaks past the rim.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Capybara — Field Plate", 1000, 1000)

INK = "#3A2E22"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#283322"}, {"offset": 1, "color": "#0E140D"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#ECE8CC"}, {"offset": 0.7, "color": "#C9C7A0"},
    {"offset": 1, "color": "#8E8F66"}]}}
FUR_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#B08A5E"}, {"offset": 0.7, "color": "#8A6642"},
    {"offset": 1, "color": "#614630"}]}}
HEAD_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#B9946A"}, {"offset": 0.72, "color": "#93704C"},
    {"offset": 1, "color": "#674B33"}]}}
EAR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#8A6642"}, {"offset": 1, "color": "#5E4430"}]}}
WATER_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7E9A80"}, {"offset": 1, "color": "#3C5646"}]}}
YUZU_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#FFE58A"}, {"offset": 0.65, "color": "#F2B83A"},
    {"offset": 1, "color": "#C98420"}]}}
REED_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7E8A58"}, {"offset": 1, "color": "#4D5A34"}]}}

CX, CY, R = 500, 460, 420
WL = 700   # waterline

def rim_x(y):
    """Left/right x where the plate circle crosses height y."""
    dx = math.sqrt(R*R - (y - CY)**2)
    return CX - dx, CX + dx

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#6C6E4C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F4F2DE", strokeWidth=3, opacity=55)
d.shape("ellipse", "Patina 1", x=170, y=180, width=240, height=140, fill="#A9A882", opacity=22, stroke=NONE)
d.shape("ellipse", "Patina 2", x=560, y=150, width=220, height=120, fill="#A9A882", opacity=18, stroke=NONE)
for i, (x, y, w) in enumerate([(200,300,8),(770,250,7),(170,560,9),(840,520,8),
                               (140,420,6),(860,400,7),(400,125,7),(600,120,8)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w, fill="#7F7F5C", opacity=40, stroke=NONE)

# --- reeds behind the animal (bases sink under the waterline) ------------------
for i, (bx, tx, ty, w) in enumerate([(770,742,300,14),(796,812,262,12),(818,846,330,10),(748,704,360,10)]):
    d.path(f"M{bx-w/2},{WL+20} Q{(bx+tx)/2-w/2},{(WL+ty)/2} {tx},{ty} "
           f"Q{(bx+tx)/2+w/2},{(WL+ty)/2} {bx+w/2},{WL+20} Z",
           f"Reed {i+1}", fill=REED_GRAD, stroke=INK, strokeWidth=3, opacity=80)
d.path("M808,262 L812,236 L818,262 Z", "Reed tip", fill="#4D5A34", stroke=NONE, opacity=80)
d.shape("ellipse", "Cattail head", x=731, y=300, width=22, height=70, fill="#6B4A2C", stroke=INK, strokeWidth=3)
d.path("M742,300 L742,276", "Cattail spike", fill=NONE, stroke=INK, strokeWidth=3, cap="round")

# --- body: the loaf (lower half sits under the water band) ----------------------
d.path("M392,470 C440,412 560,388 670,404 C760,418 812,478 816,560 "
       "C820,660 790,750 700,790 C620,812 480,810 410,782 "
       "C350,750 340,560 392,470 Z",
       "Body", fill=FUR_GRAD, stroke=INK, strokeWidth=8)
# back light (wet sheen) + belly shade
d.path("M470,430 C560,398 680,404 752,446", "Back sheen", fill=NONE,
       stroke="#E8D6B0", strokeWidth=16, opacity=24, cap="round")
d.path("M500,452 C570,432 650,434 700,452", "Back sheen 2", fill=NONE,
       stroke="#FFFFFF", strokeWidth=6, opacity=18, cap="round")
d.path("M420,660 C500,700 650,705 780,660", "Flank shade", fill=NONE,
       stroke="#4A3524", strokeWidth=28, opacity=22, cap="round")
# coarse fur strokes
for i, dd in enumerate(["M520,470 C540,480 552,494 560,510", "M600,460 C620,472 632,486 640,502",
                        "M680,470 C698,484 708,500 714,518", "M560,540 C580,552 592,566 600,582",
                        "M640,550 C660,562 672,578 680,594", "M720,560 C736,574 744,590 748,608",
                        "M480,560 C496,572 506,586 512,602", "M760,500 C772,516 778,532 780,550"]):
    d.path(dd, f"Body fur {i+1}", fill=NONE, stroke="#5A4130", strokeWidth=5, opacity=40, cap="round")
# hind haunch line
d.path("M690,540 C740,560 770,610 768,680", "Haunch", fill=NONE,
       stroke=INK, strokeWidth=5, opacity=45, cap="round")

# --- ear (behind head top) ------------------------------------------------------
d.shape("ellipse", "Ear", x=400, y=338, width=46, height=42, fill=EAR_GRAD, stroke=INK, strokeWidth=5)
d.shape("ellipse", "Inner ear", x=412, y=348, width=22, height=20, fill="#4A3424", opacity=70, stroke=NONE)

# --- head: big blunt box, profile facing left ------------------------------------
d.path("M462,388 C420,366 330,362 262,384 C214,400 190,430 188,480 "
       "C186,528 196,566 228,586 C270,610 350,620 420,626 "
       "C470,630 500,600 500,540 C500,470 490,410 462,388 Z",
       "Head", fill=HEAD_GRAD, stroke=INK, strokeWidth=8)
# forehead/snout bridge light + jowl shade
d.path("M440,392 C380,378 300,382 250,404", "Bridge light", fill=NONE,
       stroke="#F0DDB8", strokeWidth=18, opacity=26, cap="round")
d.path("M236,578 C290,604 370,614 440,614", "Jaw shade", fill=NONE,
       stroke="#4A3524", strokeWidth=16, opacity=28, cap="round")
d.shape("ellipse", "Cheek light", x=360, y=480, width=110, height=90, fill="#E8D2A8", opacity=18, stroke=NONE)
# darker blunt snout front
d.path("M262,388 C214,402 190,432 188,480 C186,528 196,566 228,586 "
       "C238,540 240,450 262,388 Z", "Snout shade", fill="#4A3524", opacity=30, stroke=NONE)
# cheek fur
for i, dd in enumerate(["M410,500 C428,512 440,526 446,542", "M380,540 C398,552 410,566 416,582",
                        "M440,460 C456,472 466,486 470,502"]):
    d.path(dd, f"Cheek fur {i+1}", fill=NONE, stroke="#5A4130", strokeWidth=5, opacity=40, cap="round")

# --- the half-lidded eye (the whole personality) ---------------------------------
d.shape("ellipse", "Eye socket shade", x=326, y=420, width=72, height=46, fill="#4A3524", opacity=22, stroke=NONE)
d.path("M336,446 C346,438 378,438 390,446 C380,456 346,456 336,446 Z",
       "Eye", fill="#2A1E16", stroke=NONE)
d.shape("ellipse", "Glint", x=362, y=446, width=5, height=4, fill="#FFFFFF", opacity=75, stroke=NONE)
d.path("M330,446 C344,434 380,434 396,446", "Heavy lid", fill=NONE,
       stroke=INK, strokeWidth=7, cap="round")
d.path("M336,434 C350,426 376,426 390,434", "Lid fold", fill=NONE,
       stroke="#5A4130", strokeWidth=4, opacity=50, cap="round")

# --- nose + mouth ------------------------------------------------------------------
d.path("M206,448 C214,442 224,444 228,452", "Nostril", fill=NONE,
       stroke="#241A12", strokeWidth=7, cap="round")
d.path("M214,470 C214,500 218,524 226,540", "Lip cleft", fill=NONE,
       stroke=INK, strokeWidth=5, opacity=70, cap="round")
d.path("M226,540 C246,556 272,562 300,558", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=6, cap="round")
# whisker stubs
for i, (x, y) in enumerate([(236,478),(248,494),(240,512)]):
    d.shape("ellipse", f"Whisker pore {i+1}", x=x, y=y, width=5, height=5, fill="#2A1E16", opacity=55, stroke=NONE)

# --- yuzu balanced on the head ------------------------------------------------------
d.shape("ellipse", "Yuzu shadow", x=310, y=366, width=70, height=14, fill="#4A3524", opacity=30, stroke=NONE)
d.shape("ellipse", "Yuzu", x=312, y=316, width=66, height=58, fill=YUZU_GRAD, stroke="#8A5A1A", strokeWidth=4)
d.shape("ellipse", "Yuzu shine", x=326, y=326, width=18, height=12, fill="#FFFFFF", opacity=45, stroke=NONE)
for i, (x, y) in enumerate([(352,334),(360,350),(340,356),(330,344)]):
    d.shape("ellipse", f"Yuzu pore {i+1}", x=x, y=y, width=3, height=3, fill="#B87A1E", opacity=60, stroke=NONE)
d.path("M346,318 L348,308", "Yuzu stem", fill=NONE, stroke="#5A4A22", strokeWidth=4, cap="round")
d.path("M348,310 C360,296 380,296 388,304 C376,314 360,316 348,310 Z",
       "Yuzu leaf", fill=REED_GRAD, stroke=INK, strokeWidth=3)

# --- water band: closed on the disc's own arc ---------------------------------------
lx, rx = rim_x(WL)
waves = []
n = 8
for k in range(1, n):
    x = lx + (rx - lx) * k / n
    waves.append(f"{x:.1f},{WL + (6 if k % 2 else -6)}")
wave_d = f"M{lx:.1f},{WL} " + " ".join(
    f"Q{(lx + (rx-lx)*(k-0.5)/n):.1f},{WL + (8 if k % 2 else -8)} {(lx + (rx-lx)*k/n):.1f},{WL}"
    for k in range(1, n + 1))
d.path(wave_d + f" A420,420 0 0 1 {lx:.1f},{WL} Z", "Water",
       fill=WATER_GRAD, stroke=NONE, opacity=78)
# surface glint + ripple rings around the body
d.path(wave_d, "Water surface line", fill=NONE, stroke="#DDE8D4", strokeWidth=4, opacity=55, cap="round")
d.shape("ellipse", "Ripple 1", x=240, y=704, width=540, height=32, fill=NONE, stroke="#E4EEDC", strokeWidth=3, opacity=40)
d.shape("ellipse", "Ripple 2", x=205, y=712, width=600, height=48, fill=NONE, stroke="#E4EEDC", strokeWidth=3, opacity=25)
for i, (x, y, w) in enumerate([(300,760,60),(560,790,90),(420,830,50),(680,750,40)]):
    d.path(f"M{x},{y} L{x+w},{y}", f"Water glint {i+1}", fill=NONE,
           stroke="#E4EEDC", strokeWidth=4, opacity=30, cap="round")
# redraw the rim on top so the water edge sits under the plate stroke
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#6C6E4C", strokeWidth=6)

# droplets on the wet fur
for i, (x, y, w) in enumerate([(470,420,8),(560,410,7),(650,418,9),(286,404,6)]):
    d.shape("ellipse", f"Droplet {i+1}", x=x, y=y, width=w, height=w*1.3, fill="#FFFFFF", opacity=45, stroke=NONE)

# --- name ----------------------------------------------------------------------
d.text("CAPYBARA", "Name", x=500, y=962, size=58, font="Virelai Sans",
       color="#E2DFC4", justify="center")

d.finish("capybara-V1R00")
