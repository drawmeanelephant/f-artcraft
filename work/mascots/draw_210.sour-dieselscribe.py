#!/usr/bin/env python3
"""Sour Dieselscribe — mascot portrait V1R00.
A hunched scribe racing a quill across the ledger; the nib trails oily,
diesel-scented fumes and the page still shimmers wet. 1000x1000.
Gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Sour Dieselscribe — Mascot Portrait", 1000, 1000)

INK = "#262014"
BG_GRAD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000], "stops": [
    {"offset": 0, "color": "#0D0F08"}, {"offset": 1, "color": "#060704"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#5E5E38"}, {"offset": 0.7, "color": "#33341F"},
    {"offset": 1, "color": "#17170E"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "start": [0, 700], "end": [0, 880], "stops": [
    {"offset": 0, "color": "#2C2C1E"}, {"offset": 1, "color": "#12120A"}]}}
ROBE = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#8A9452"}, {"offset": 0.65, "color": "#5E6638"},
    {"offset": 1, "color": "#333A20"}]}}
DESK = {"gradient": {"kind": "linear", "start": [0, 580], "end": [0, 700], "stops": [
    {"offset": 0, "color": "#54402A"}, {"offset": 1, "color": "#2E2114"}]}}
PAPER = {"gradient": {"kind": "linear", "start": [0, 540], "end": [0, 660], "stops": [
    {"offset": 0, "color": "#F0EAD2"}, {"offset": 1, "color": "#CDBF9A"}]}}
QUILL = {"gradient": {"kind": "linear", "start": [560, 420], "end": [660, 560], "stops": [
    {"offset": 0, "color": "#EAE0C8"}, {"offset": 1, "color": "#9A8E6E"}]}}
FUME = {"gradient": {"kind": "linear", "start": [640, 380], "end": [780, 240], "stops": [
    {"offset": 0, "color": "#B8D85E"}, {"offset": 0.6, "color": "#7A9A6A"},
    {"offset": 1, "color": "#8A7AD8"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#A8A860", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E6E2B8", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(193,233,8),(801,230,7),(157,524,9),(837,544,8),
                               (247,766,7),(753,749,9),(133,393,6),(864,391,7),
                               (391,113,7),(613,110,8),(333,823,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#4C4C2E", opacity=45, stroke=NONE)

# --- floor: bottom segment closed on the disc's own arc -----------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0A0A04",
       strokeWidth=4, opacity=70)

# --- speed dust + oily motes --------------------------------------------------------
for i, (x, y, w, o) in enumerate([(255,195,4,50),(335,145,3,40),(675,160,4,50),
                                  (755,265,3,40),(215,330,4,40),(785,415,4,45),
                                  (430,130,3,40),(575,140,4,45)]):
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#E8E4B8", opacity=o, stroke=NONE)

# --- the desk slab ---------------------------------------------------------------------
d.shape("ellipse", "Desk shadow", x=330, y=676, width=360, height=28,
        fill="#080804", opacity=50, stroke=NONE)
d.path("M318,596 L690,596 L672,700 L336,700 Z", "Desk", fill=DESK,
       stroke=INK, strokeWidth=6, join="round")
d.path("M318,596 L690,596 L682,620 L326,620 Z", "Desk edge", fill="#665032",
       stroke=INK, strokeWidth=4, join="round", opacity=95)

# --- the open ledger, pages fluttering with speed ---------------------------------------
d.path("M410,552 L600,540 L612,604 L418,616 Z", "Ledger page", fill=PAPER,
       stroke=INK, strokeWidth=4, join="round")
d.path("M418,616 L612,604 L616,612 L422,624 Z", "Page edge", fill="#9A8A62",
       stroke=INK, strokeWidth=3, join="round")
# written rows — earlier lines settled, latest still wet and bright
rows = [(556, "#9A8A62", 65), (568, "#8A7A58", 70), (580, "#6E5E42", 90)]
for j, (ry, col, op) in enumerate(rows):
    d.path(f"M426,{ry} L{560-j*8},{ry-8-j*1} M{570-j*6},{ry-2} L596,{ry-3}",
           f"Ledger row {j+1}", fill=NONE, stroke=col, strokeWidth=3,
           opacity=op, cap="round")
# the wet last line, chartreuse ink still gleaming
d.path("M428,592 C470,584 530,582 576,578", "Wet line", fill=NONE,
       stroke="#B8D85E", strokeWidth=5, cap="round", opacity=90)
d.path("M428,592 C470,584 530,582 576,578", "Wet sheen", fill=NONE,
       stroke="#EAF6B0", strokeWidth=2, cap="round", opacity=60)
# a curled page corner lifting with the speed
d.path("M588,542 L600,540 L606,566 C596,556 590,550 588,542 Z",
       "Page curl", fill="#E2D8B6", stroke=INK, strokeWidth=3, join="round")

# --- the scribe, hunched low over the ledger ----------------------------------------------
# body leaning forward: shoulders high, head down
d.path("M430,330 C492,322 540,352 556,412 C570,462 566,540 548,600 "
       "L380,600 C368,540 366,470 382,420 C394,374 402,336 430,330 Z",
       "Scribe body", fill=ROBE, stroke=INK, strokeWidth=6, join="round")
# hood back — head is down, we see the cowl's back
d.path("M432,326 C480,318 522,340 542,382 C522,368 492,360 460,364 "
       "C428,368 406,384 394,406 C398,368 408,336 432,326 Z",
       "Cowl back", fill="#3E4626", stroke=INK, strokeWidth=5, join="round")
# the visible sliver of face under the cowl, tipped down at the page
d.path("M410,396 C424,382 452,376 474,380 C470,404 456,420 436,424 "
       "C420,420 410,410 410,396 Z", "Face sliver", fill="#C8B86A",
       stroke=INK, strokeWidth=4, join="round")
# one squinting, concentrating eye + knit brow
d.shape("ellipse", "Eye", x=436, y=396, width=14, height=10, fill="#2A2014",
        stroke=NONE)
d.path("M428,386 L458,382", "Brow", fill=NONE, stroke=INK, strokeWidth=4,
       cap="round")

# --- the quill: blurred with speed ----------------------------------------------------------
# ghost trail of the quill's last stroke
d.path("M540,470 C580,442 620,428 662,424", "Quill ghost", fill=NONE,
       stroke="#D8D0B0", strokeWidth=14, cap="round", opacity=18)
# the quill proper: long feather arcing down to the wet line
d.path("M566,470 C590,428 630,396 676,378 C668,416 640,452 596,478 "
       "C584,484 572,478 566,470 Z",
       "Quill feather", fill=QUILL, stroke=INK, strokeWidth=4, join="round")
d.path("M566,470 C600,438 640,406 676,378", "Quill shaft", fill=NONE,
       stroke="#6E6248", strokeWidth=3, opacity=80)
# feather barbs
for i, (x, y) in enumerate([(610,432),(628,418),(646,402)]):
    d.path(f"M{x},{y} L{x+14},{y-8}", f"Barb {i+1}", fill=NONE,
           stroke="#8A7E5E", strokeWidth=2, opacity=70)
# nib kissing the page
d.path("M566,470 L556,486 L570,484 Z", "Nib", fill="#3A3018", stroke=INK,
       strokeWidth=3, join="round")
# hand clamped on the quill
d.shape("ellipse", "Writing hand", x=556, y=458, width=34, height=26,
        fill="#B8A860", stroke=INK, strokeWidth=4)
# scribble motion ticks around the nib
d.path("M540,494 L522,500 M548,506 L534,516 M590,486 L600,496", "Scribble ticks",
       fill=NONE, stroke="#E8E4B8", strokeWidth=3, cap="round", opacity=70)

# --- speed lines streaming back off the quill and hand ------------------------------------
for i, (y, x0, x1) in enumerate([(452,300,520),(478,286,536),(504,300,528)]):
    d.path(f"M{x0},{y} L{x1},{y-6}", f"Speed line {i+1}", fill=NONE,
           stroke="#C8C478", strokeWidth=3, cap="round", opacity=35)

# --- diesel fumes curling off the feather ---------------------------------------------------
d.path("M676,378 C712,352 726,320 716,290 C708,266 726,246 750,242",
       "Fume spine", fill=NONE, stroke=FUME, strokeWidth=14, cap="round",
       opacity=30)
d.path("M676,378 C712,352 726,320 716,290 C708,266 726,246 750,242",
       "Fume core", fill=NONE, stroke="#C8DE7A", strokeWidth=5, cap="round",
       opacity=45)
# a second lazy curl
d.path("M660,388 C686,376 700,356 694,336 C690,320 700,306 716,304",
       "Fume curl 2", fill=NONE, stroke="#9A8AD8", strokeWidth=9,
       cap="round", opacity=25)
# oily droplets beading off the plume
for i, (x, y, w) in enumerate([(734,262,9),(700,332,7),(752,224,6)]):
    d.shape("ellipse", f"Fume bead {i+1}", x=x, y=y, width=w, height=w,
            fill="#B8D85E", opacity=50, stroke=NONE)

# --- finished sheets stacking up at the desk's right edge -------------------------------------
d.path("M700,560 L788,556 L794,596 L706,600 Z", "Done sheet", fill=PAPER,
       stroke=INK, strokeWidth=4, join="round", opacity=95)
d.path("M712,568 L770,565 M714,578 L768,575 M716,588 L756,585",
       "Done rows", fill=NONE, stroke="#8A7A58", strokeWidth=2, opacity=70)
# speed tick showing the pile just grew
d.path("M796,540 L812,528 M806,556 L824,548", "Pile ticks", fill=NONE,
       stroke="#E8E4B8", strokeWidth=3, cap="round", opacity=60)

# --- captions ------------------------------------------------------------------
d.text("SOUR DIESELSCRIBE", "Name", x=500, y=934, size=56, font="Virelai Sans",
       color="#ECE8BC", justify="center")
r = d.text("HIGH-SPEED RECORD SCRIBE", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#B0AE78", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("210.sour-dieselscribe-V1R00")
