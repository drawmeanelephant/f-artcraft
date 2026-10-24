#!/usr/bin/env python3
"""Witness Mink-9 — mascot portrait V1R00.
A mink standing at the margin beside a routing slip that carries a stapled,
handwritten sympathy note: fully observed, compassionately noted,
operationally unchanged. 1000x1000. Gradients + translucent shading,
never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Witness Mink-9 — Mascot Portrait", 1000, 1000)

INK = "#2E2028"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1E161C"}, {"offset": 1, "color": "#0C080C"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#6E5A52"}, {"offset": 0.7, "color": "#4E3E3C"},
    {"offset": 1, "color": "#2E2228"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#46363A"}, {"offset": 1, "color": "#241C20"}]}}
FUR = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#7A5A48"}, {"offset": 0.7, "color": "#5A4034"},
    {"offset": 1, "color": "#3E2C24"}]}}
FUR_DARK = "#4A342C"
CREAM = "#E8E0CC"
PAPER = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E4DAC0"}, {"offset": 1, "color": "#C4B694"}]}}
NOTE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F0E8D2"}, {"offset": 1, "color": "#D2C6A4"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#8A7462", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8C8B4", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(192,236,8),(800,232,7),(158,524,9),(834,542,8),
                               (246,762,7),(754,748,9),(132,394,6),(864,392,7),
                               (392,112,7),(612,110,8),(332,820,6),(666,818,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#503F3C", opacity=45, stroke=NONE)

# --- floor ---------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#161014",
       strokeWidth=4, opacity=70)

# --- the routing slip, standing right of center ----------------------------------
d.shape("ellipse", "Slip shadow", x=556, y=664, width=250, height=34,
        fill="#0C0808", opacity=50, stroke=NONE)
# clipboard board behind the slip
d.path("M560,268 L798,268 L798,668 L560,668 Z", "Board",
       fill="#54423C", stroke=INK, strokeWidth=6, join="round")
d.shape("rectangle", "Clip", x=646, y=252, width=66, height=34,
        fill="#8A7C68", stroke=INK, strokeWidth=4, radius=8)
d.shape("ellipse", "Clip hinge", x=672, y=258, width=14, height=10,
        fill="#C4B89E", stroke=INK, strokeWidth=3)
# the slip itself
d.shape("rectangle", "Routing slip", x=576, y=288, width=206, height=356,
        fill=PAPER, stroke=INK, strokeWidth=4, radius=4)
d.text("ROUTING SLIP", "Slip header", x=679, y=318, size=15,
       font="Virelai Sans", color="#4E3E34", justify="center")
d.path("M590,330 L768,330", "Header rule", fill=NONE, stroke="#8A7A60",
       strokeWidth=3)
# routing rows: label stubs and empty boxes, all unsigned
for i, y in enumerate((348, 388, 428, 468)):
    d.shape("rectangle", f"Route box {i+1}", x=590, y=y, width=60, height=26,
            fill="#D2C6A8", stroke="#8A7A60", strokeWidth=3, radius=3)
    d.shape("rectangle", f"Route line {i+1}", x=660, y=y+7, width=108, height=12,
            fill="#B4A888", stroke=NONE, radius=6, opacity=70)
# stapled sympathy note, rotated onto the slip's lower half
d.path("M598,506 L764,494 L770,604 L604,616 Z", "Sympathy note",
       fill=NOTE, stroke=INK, strokeWidth=4, join="round")
# the staple, pressed flat
d.path("M600,522 L634,519", "Staple", fill=NONE, stroke="#9A9284",
       strokeWidth=5, cap="round")
d.path("M600,522 L598,528 M634,519 L634,525", "Staple legs", fill=NONE,
       stroke="#9A9284", strokeWidth=4, cap="round")
# handwritten line: "this was seen." — the whole testimony
n = d.text("this was seen.", "Note hand", x=684, y=560, size=17,
           font="Source Sans 3", color="#5A4A3C", justify="center")
if n and n.get("id"):
    d.cmd("text.setStyle", "note italic", ids=[n["id"]], style="Italic")
d.path("M630,584 C660,590 700,586 736,580", "Note underline", fill=NONE,
       stroke="#8A7A60", strokeWidth=3, cap="round", opacity=60)

# --- Witness Mink-9, standing at the margin -------------------------------------
d.shape("ellipse", "Mink shadow", x=270, y=664, width=240, height=34,
        fill="#0C0808", opacity=55, stroke=NONE)
# tail curling low behind him
d.path("M330,560 C290,600 260,640 268,668 C274,690 310,692 336,676",
       "Tail", fill=NONE, stroke=FUR_DARK, strokeWidth=26, cap="round")
d.path("M330,560 C290,600 260,640 268,668 C274,690 310,692 336,676",
       "Tail sheen", fill=NONE, stroke="#6E5040", strokeWidth=12,
       cap="round", opacity=60)
# long upright body
d.path("M400,336 C452,336 486,384 488,452 C490,530 470,620 448,656 "
       "C432,678 380,678 362,656 C338,626 322,530 324,452 "
       "C326,384 348,336 400,336 Z",
       "Mink body", fill=FUR, stroke=INK, strokeWidth=6)
# pale chest bib
d.path("M400,420 C430,420 448,460 448,512 C448,566 430,616 404,632 "
       "C380,616 362,566 362,512 C362,460 372,420 400,420 Z",
       "Chest bib", fill="#C9B294", opacity=85, stroke=NONE)
# hind feet
d.shape("ellipse", "Foot L", x=342, y=652, width=52, height=22,
        fill=FUR_DARK, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Foot R", x=418, y=652, width=52, height=22,
        fill=FUR_DARK, stroke=INK, strokeWidth=4)
# forepaws folded, never intervening
d.path("M368,520 C384,540 416,540 432,520", "Paws folded", fill=NONE,
       stroke=FUR_DARK, strokeWidth=14, cap="round")
d.shape("ellipse", "Paw L", x=366, y=510, width=26, height=20,
        fill="#6E5040", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Paw R", x=408, y=510, width=26, height=20,
        fill="#6E5040", stroke=INK, strokeWidth=3)
# head: wedge snout, small round ears
d.path("M354,306 C346,284 356,262 378,254 C368,236 378,218 396,216 "
       "C402,200 422,196 434,206 C452,198 470,212 468,232 "
       "C484,240 490,262 480,278 C492,296 484,322 462,330 "
       "C430,344 372,338 354,306 Z",
       "Head", fill=FUR, stroke=INK, strokeWidth=6)
d.shape("ellipse", "Ear L", x=366, y=214, width=34, height=30,
        fill=FUR_DARK, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Ear R", x=448, y=210, width=34, height=30,
        fill=FUR_DARK, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Ear in L", x=374, y=222, width=18, height=15,
        fill="#8A6A56", stroke=NONE)
d.shape("ellipse", "Ear in R", x=456, y=218, width=18, height=15,
        fill="#8A6A56", stroke=NONE)
# pale muzzle + nose
d.path("M414,296 C432,290 452,294 460,306 C452,318 430,320 416,314 Z",
       "Muzzle", fill="#C9B294", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Nose", x=452, y=300, width=16, height=12,
        fill=INK, stroke=NONE)
# eyes: soft, observant, never intervening
d.shape("ellipse", "Eye L", x=392, y=270, width=15, height=18, fill=INK, stroke=NONE)
d.shape("ellipse", "Eye R", x=444, y=268, width=15, height=18, fill=INK, stroke=NONE)
d.shape("ellipse", "Glint L", x=396, y=274, width=4, height=4,
        fill="#FFFFFF", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=448, y=272, width=4, height=4,
        fill="#FFFFFF", opacity=90, stroke=NONE)
# whiskers
d.path("M440,306 L482,300 M440,312 L480,316 M416,306 L376,300 M416,312 L380,318",
       "Whiskers", fill=NONE, stroke="#C9B294", strokeWidth=2.5,
       cap="round", opacity=80)

# --- captions ---------------------------------------------------------------------------
nm = d.text("WITNESS MINK-9", "Name", x=500, y=930, size=58,
            font="Virelai Sans", color="#E8DAC4", justify="center")
# Virelai Sans has no digit glyphs: the trailing 9 falls back to Source Sans 3
if nm and nm.get("id"):
    d.cmd("text.setStyle", "name digit fallback", ids=[nm["id"]],
          start=13, end=14, font="Source Sans 3")
r = d.text("JURISDICTIONAL WITNESS", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#C0A88E", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("225.witness-mink-9-V1R00")
