#!/usr/bin/env python3
"""Spooler Gremlin — mascot portrait V1R00. Print Queue Intercessor:
a moss-green gremlin behind an office printer, holding a print job up
into the lamp light to study it; the printer wears a taped
OUT OF PAPER sign that isn't true. Affectionately obstructive.
Dusty-teal plate on an office-night backdrop. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Prop labels in Source Sans 3. Plate = circle (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Spooler Gremlin — Mascot Plate", 1000, 1000)

INK = "#241C14"   # warm dark ink, never black
BG_GRAD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000], "stops": [
    {"offset": 0, "color": "#10141C"}, {"offset": 1, "color": "#06080C"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#5E6E66"}, {"offset": 0.62, "color": "#3A4A42"},
    {"offset": 1, "color": "#182420"}]}}
SKIN_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#9CBA7E"}, {"offset": 0.7, "color": "#73945C"},
    {"offset": 1, "color": "#4E6B3E"}]}}
EAR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#8AAE6E"}, {"offset": 1, "color": "#557444"}]}}
PRINTER_GRAD = {"gradient": {"kind": "linear", "start": [0, 520], "end": [0, 780], "stops": [
    {"offset": 0, "color": "#C9C2B2"}, {"offset": 0.55, "color": "#9A9284"},
    {"offset": 1, "color": "#6E685C"}]}}
PRINTER_TOP = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#8A8478"}, {"offset": 1, "color": "#5E594E"}]}}
SHEET_GRAD = {"gradient": {"kind": "linear", "start": [520, 220], "end": [660, 420], "stops": [
    {"offset": 0, "color": "#FFF6DC"}, {"offset": 0.55, "color": "#F0E2BC"},
    {"offset": 1, "color": "#D6C49A"}]}}
LAMP = "#F2C96A"

PCX, PCY, PR = 500, 460, 420

def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#7A8E80", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#0E1410", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C4D4C8", strokeWidth=3, opacity=26)
# office patina + flecks
d.shape("ellipse", "Patina 1", x=190, y=340, width=230, height=150,
        fill="#4E6258", opacity=22, stroke=NONE)
d.shape("ellipse", "Patina 2", x=620, y=580, width=230, height=140,
        fill="#2A3C34", opacity=30, stroke=NONE)
for i, (x, y, w) in enumerate([(215,345,5),(795,340,6),(180,545,5),(848,565,5),
                               (260,765,5),(735,770,6),(158,450,5),(855,630,5),
                               (430,128,5),(600,140,6),(338,162,4),(705,200,5),
                               (250,650,4),(660,720,5)]):
    assert on_disc(x, y, 12), (x, y)
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#D8E4D4", opacity=28, stroke=NONE)
# ghost arcs on the dark backdrop
d.path("M932,155 A105,105 0 0 0 848,62", "Ghost arc TR",
       fill=NONE, stroke="#5E7A6A", strokeWidth=14, opacity=10, cap="round")
d.path("M78,775 A118,118 0 0 0 188,878", "Ghost arc BL",
       fill=NONE, stroke="#5E7A6A", strokeWidth=10, opacity=8, cap="round")

# --- the lamp light: cone from the ceiling fixture ------------------------------
d.path("M596,138 L470,430 L700,430 Z", "Light cone",
       fill=LAMP, opacity=10, stroke=NONE)
d.shape("ellipse", "Cone core", x=520, y=250, width=130, height=200,
        fill=LAMP, opacity=9, stroke=NONE)
# little pull-chain fixture at the plate's top
d.shape("ellipse", "Lamp shade", x=560, y=110, width=80, height=34,
        fill={"gradient": {"kind": "linear", "stops": [
            {"offset": 0, "color": "#6E6858"}, {"offset": 1, "color": "#3A362C"}]}},
        stroke=INK, strokeWidth=3)
d.shape("ellipse", "Bulb glow", x=580, y=140, width=40, height=22,
        fill=LAMP, opacity=55, stroke=NONE)
d.shape("ellipse", "Bulb", x=592, y=144, width=16, height=12,
        fill="#FFE9A8", stroke=NONE)
d.path("M640,140 L644,178", "Pull chain",
       fill=NONE, stroke="#8A8478", strokeWidth=2, opacity=70)
d.shape("ellipse", "Chain knob", x=640, y=178, width=8, height=10,
        fill="#8A8478", stroke=NONE)

# --- the gremlin, behind the printer ----------------------------------------------
# ears first: two big pointed sails behind the head
d.path("M430,420 C400,380 372,330 368,280 C404,296 436,340 452,392 Z",
       "Ear L", fill=EAR_GRAD, stroke=INK, strokeWidth=4)
d.path("M408,392 C392,364 380,334 380,308 C400,324 420,352 432,384 Z",
       "Ear L inner", fill="#3E5732", opacity=65, stroke=NONE)
d.path("M570,420 C600,380 628,330 632,280 C596,296 564,340 548,392 Z",
       "Ear R", fill=EAR_GRAD, stroke=INK, strokeWidth=4)
d.path("M592,392 C608,364 620,334 620,308 C600,324 580,352 568,384 Z",
       "Ear R inner", fill="#3E5732", opacity=65, stroke=NONE)
# head: soft dome with cheek tufts
d.path("M500,380 C556,380 592,420 590,478 C588,540 552,580 500,580 "
       "C448,580 412,540 410,478 C408,420 444,380 500,380 Z",
       "Head", fill=SKIN_GRAD, stroke=INK, strokeWidth=4.5)
# cheek tufts
d.path("M410,470 C396,478 390,492 392,506 C402,500 410,492 414,480 Z",
       "Tuft L", fill=SKIN_GRAD, stroke=INK, strokeWidth=3)
d.path("M590,470 C604,478 610,492 608,506 C598,500 590,492 586,480 Z",
       "Tuft R", fill=SKIN_GRAD, stroke=INK, strokeWidth=3)
# brow shade + muzzle light
d.path("M424,430 C440,402 470,390 500,390 C530,390 560,402 576,430 "
       "C556,416 530,410 500,410 C470,410 444,416 424,430 Z",
       "Brow shade", fill="#3E5732", opacity=35, stroke=NONE)
d.shape("ellipse", "Muzzle light", x=452, y=490, width=96, height=66,
        fill="#C4D9A4", opacity=40, stroke=NONE)
# big interested eyes, glinting
d.shape("ellipse", "Eye L", x=448, y=440, width=44, height=50,
        fill="#F2EDD8", stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Eye R", x=508, y=440, width=44, height=50,
        fill="#F2EDD8", stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Pupil L", x=462, y=456, width=18, height=24,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Pupil R", x=522, y=456, width=18, height=24,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Glint L", x=466, y=460, width=7, height=7,
        fill="#FFF6DC", stroke=NONE)
d.shape("ellipse", "Glint R", x=526, y=460, width=7, height=7,
        fill="#FFF6DC", stroke=NONE)
# innocent little mouth + one fang
d.path("M480,518 C492,526 510,526 522,518", "Mouth",
       fill=NONE, stroke=INK, strokeWidth=3.5, cap="round")
d.path("M513,523 L519,534 L525,523 Z", "Fang",
       fill="#F2EDD8", stroke=INK, strokeWidth=2)
# arms raised, holding the sheet into the light
d.path("M420,470 C396,430 400,390 428,356 C440,352 450,360 448,372 "
       "C430,398 430,436 444,462 Z",
       "Arm L", fill=SKIN_GRAD, stroke=INK, strokeWidth=4)
d.path("M580,470 C604,430 600,390 572,356 C560,352 550,360 552,372 "
       "C570,398 570,436 556,462 Z",
       "Arm R", fill=SKIN_GRAD, stroke=INK, strokeWidth=4)
# claws gripping the sheet's lower corners
d.shape("ellipse", "Claw L", x=424, y=344, width=28, height=26,
        fill=SKIN_GRAD, stroke=INK, strokeWidth=3)
d.shape("ellipse", "Claw R", x=548, y=344, width=28, height=26,
        fill=SKIN_GRAD, stroke=INK, strokeWidth=3)

# --- the held print job, up in the light -------------------------------------------
d.path("M432,240 L586,222 L600,352 L446,370 Z", "Held sheet",
       fill=SHEET_GRAD, stroke=INK, strokeWidth=4)
# lamp-light wash on the sheet's upper half
d.path("M432,240 L586,222 L592,284 L438,300 Z", "Sheet light wash",
       fill="#FFF9E2", opacity=50, stroke=NONE)
# faint print lines on the held sheet
for j, (y0, y1, x0, x1) in enumerate([(262, 258, 452, 566), (286, 282, 454, 570),
                                      (310, 306, 456, 552), (332, 328, 458, 576)]):
    d.path(f"M{x0},{y0} L{x1},{y1}", f"Held line {j+1}",
           fill=NONE, stroke="#9A8A68", strokeWidth=5, opacity=40,
           cap="round")

# --- the printer -------------------------------------------------------------------
d.shape("ellipse", "Printer shadow", x=280, y=772, width=440, height=40,
        fill="#060A08", opacity=45, stroke=NONE)
# body
d.path("M300,560 L700,560 L716,740 C716,756 704,762 688,762 L312,762 "
       "C296,762 284,756 284,740 Z",
       "Printer body", fill=PRINTER_GRAD, stroke=INK, strokeWidth=5)
# top deck + paper slot
d.path("M312,540 L688,540 L700,560 L300,560 Z", "Printer top",
       fill=PRINTER_TOP, stroke=INK, strokeWidth=4)
d.path("M360,548 L640,548", "Paper slot",
       fill=NONE, stroke="#14100C", strokeWidth=7, cap="round")
# a page mid-eject from the top slot — the job that made it
d.path("M352,546 L356,510 L462,510 L466,546 Z", "Ejecting page",
       fill="#EFE6CC", stroke=INK, strokeWidth=3.5)
d.path("M368,524 L448,524 M368,536 L448,536", "Eject lines",
       fill=NONE, stroke="#9A8A68", strokeWidth=4, opacity=45, cap="round")
# front seam + control strip
d.path("M292,600 L708,600", "Front seam",
       fill=NONE, stroke="#4E483E", strokeWidth=3, opacity=60)
d.shape("ellipse", "Status LED glow", x=636, y=618, width=26, height=26,
        fill="#E05A3A", opacity=35, stroke=NONE)
d.shape("ellipse", "Status LED", x=644, y=624, width=11, height=11,
        fill="#E05A3A", stroke="#7A2A18", strokeWidth=2)
# output tray + a blank page in it
d.path("M340,700 L660,700 L652,730 L348,730 Z", "Output tray",
       fill="#3A362E", stroke=INK, strokeWidth=3.5)
d.path("M380,704 L620,704 L616,722 L384,722 Z", "Tray page",
       fill="#E4DCC4", stroke=NONE, opacity=85)
# taped sign: OUT OF PAPER (a lie)
d.path("M398,626 L602,620 L606,672 L402,678 Z", "Sign paper",
       fill="#F0E8D0", stroke=INK, strokeWidth=3)
d.path("M396,620 L436,618 L434,634 L398,636 Z", "Tape L",
       fill="#D9CEA8", opacity=85, stroke="#B0A480", strokeWidth=1.5)
d.path("M566,616 L604,614 L606,630 L568,632 Z", "Tape R",
       fill="#D9CEA8", opacity=85, stroke="#B0A480", strokeWidth=1.5)
d.text("OUT OF PAPER", "Sign text", x=502, y=657, size=20,
       font="Source Sans 3", color="#5A4E38", justify="center")

# --- loose pages scattered at the base ----------------------------------------------
d.path("M232,720 L300,706 L310,742 L242,756 Z", "Floor page 1",
       fill="#D8CFB6", stroke=INK, strokeWidth=3)
d.path("M242,726 L292,716 M246,738 L294,728", "Floor lines 1",
       fill=NONE, stroke="#8A7A5C", strokeWidth=3.5, opacity=45, cap="round")
d.path("M706,724 L772,736 L764,770 L700,758 Z", "Floor page 2",
       fill="#D8CFB6", stroke=INK, strokeWidth=3)
d.path("M716,738 L756,746 M712,750 L752,758", "Floor lines 2",
       fill=NONE, stroke="#8A7A5C", strokeWidth=3.5, opacity=45, cap="round")
for x, y in [(266, 731), (736, 747)]:
    assert on_disc(x, y, 30), (x, y)

# --- name + role ----------------------------------------------------------------------
d.text("SPOOLER GREMLIN", "Name", x=500, y=930, size=56, font="Virelai Sans",
       color="#E4EBDC", justify="center")
r = d.text("PRINT QUEUE INTERCESSOR", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#A9C4A2", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=190)

d.finish("044.spooler-gremlin-V1R00")
