#!/usr/bin/env python3
"""Threshold Crooner — mascot portrait V1R00.
A bouncer of a man crooning an endless song beside his own velvet rope,
the members' gate behind him shut. Denial never enters the lyric.
1000x1000. Gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Threshold Crooner — Mascot Portrait", 1000, 1000)

INK = "#241820"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1E1220"}, {"offset": 1, "color": "#0A060C"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#563C50"}, {"offset": 0.7, "color": "#342432"},
    {"offset": 1, "color": "#181018"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3A2438"}, {"offset": 1, "color": "#160E18"}]}}
DOOR = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3E2A24"}, {"offset": 1, "color": "#1E1410"}]}}
BRASS = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E8C06A"}, {"offset": 0.6, "color": "#B08A3E"},
    {"offset": 1, "color": "#7A5A24"}]}}
ROPE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#A83048"}, {"offset": 1, "color": "#6E1E32"}]}}
TUX = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#363240"}, {"offset": 0.7, "color": "#221E2C"},
    {"offset": 1, "color": "#141019"}]}}
SKIN = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E4B290"}, {"offset": 0.75, "color": "#C08A64"},
    {"offset": 1, "color": "#96603E"}]}}
CHROME = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#D8DEE4"}, {"offset": 1, "color": "#7A828C"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#8A6478", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8C4CE", strokeWidth=3, opacity=50)
for i, (x, y, w) in enumerate([(193,233,8),(801,230,7),(157,524,9),(837,544,8),
                               (247,766,7),(753,749,9),(133,393,6),(864,391,7),
                               (391,113,7),(613,110,8),(333,823,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#463046", opacity=45, stroke=NONE)

# --- floor: bottom segment closed on the disc's own arc -----------------------
d.path("M187,740 L813,740 A420,420 0 0 1 187,740 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M187,740 L813,740", "Floor line", fill=NONE, stroke="#120A14",
       strokeWidth=4, opacity=70)

# --- the gate: closed double doors, arched, behind everything -------------------
# door frame with arch top
d.path("M540,690 L540,300 C540,230 580,190 640,190 C700,190 740,230 740,300 L740,690 Z",
       "Door frame", fill="#241216", stroke=INK, strokeWidth=6)
d.path("M556,690 L556,306 C556,244 592,208 640,208 C688,208 724,244 724,306 L724,690 Z",
       "Doors", fill=DOOR, stroke=INK, strokeWidth=4)
# centre seam — shut
d.path("M640,208 L640,690", "Door seam", fill=NONE, stroke="#120A0C",
       strokeWidth=4)
# panel mouldings on each leaf
for side, x in (("L", 570), ("R", 650)):
    d.shape("rectangle", f"Panel top {side}", x=x, y=330, width=60, height=120,
            fill=NONE, stroke="#4A342C", strokeWidth=3, radius=4, opacity=80)
    d.shape("rectangle", f"Panel low {side}", x=x, y=480, width=60, height=140,
            fill=NONE, stroke="#4A342C", strokeWidth=3, radius=4, opacity=80)
# knobs, a breath apart — nobody's opened them tonight
d.shape("ellipse", "Knob L", x=622, y=470, width=12, height=12,
        fill=BRASS, stroke=INK, strokeWidth=2)
d.shape("ellipse", "Knob R", x=646, y=470, width=12, height=12,
        fill=BRASS, stroke=INK, strokeWidth=2)
# plaque over the arch
d.shape("rectangle", "Plaque", x=586, y=240, width=108, height=26,
        fill="#181014", stroke="#5A4234", strokeWidth=2, radius=4)
d.text("MEMBERS ONLY", "Plaque text", x=597, y=258, size=13,
       font="Virelai Sans", color="#B89A6A", justify="left")
# the thin line of warm light the door is keeping to itself
d.path("M560,690 L720,690", "Light under door", fill=NONE,
       stroke="#E8B060", strokeWidth=4, opacity=50, cap="round")
d.shape("ellipse", "Light pool", x=560, y=686, width=160, height=10,
        fill="#E8B060", opacity=15, stroke=NONE)

# --- the velvet rope -------------------------------------------------------------
def stanchion(x, tag):
    d.shape("ellipse", f"{tag} base", x=x-26, y=712, width=52, height=18,
            fill=BRASS, stroke=INK, strokeWidth=4)
    d.shape("rectangle", f"{tag} pole", x=x-7, y=570, width=14, height=145,
            fill=BRASS, stroke=INK, strokeWidth=3, radius=6)
    d.shape("ellipse", f"{tag} ball", x=x-13, y=552, width=26, height=26,
            fill=BRASS, stroke=INK, strokeWidth=3)
    d.shape("ellipse", f"{tag} ball sheen", x=x-8, y=556, width=9, height=7,
            fill="#FFF2CC", opacity=60, stroke=NONE)

stanchion(238, "Post L")
stanchion(668, "Post R")
# the rope itself: a heavy sagging crimson swag between the posts
d.path("M238,566 C330,650 576,650 668,566", "Velvet rope",
       fill=NONE, stroke=NONE)
rope = d.path("M238,566 C330,652 576,652 668,566", "Velvet rope fill",
              fill=NONE, stroke="#6E1E32", strokeWidth=22, cap="round")
d.path("M238,560 C330,640 576,640 668,560", "Rope sheen", fill=NONE,
       stroke="#C05070", strokeWidth=6, cap="round", opacity=55)
# brass cuffs where the rope meets each post
d.shape("ellipse", "Cuff L", x=230, y=556, width=16, height=22,
        fill=BRASS, stroke=INK, strokeWidth=3)
d.shape("ellipse", "Cuff R", x=660, y=556, width=16, height=22,
        fill=BRASS, stroke=INK, strokeWidth=3)

# --- the spotlight he works in --------------------------------------------------
d.path("M430,118 L300,720 L560,720 Z", "Spot cone", fill="#F0D090",
       opacity=9, stroke=NONE)
d.shape("ellipse", "Spot pool", x=300, y=700, width=260, height=34,
        fill="#F0D090", opacity=12, stroke=NONE)

# --- the crooner ------------------------------------------------------------------
CX = 430          # figure centreline
# shoes
d.shape("ellipse", "Shoe L", x=CX-68, y=712, width=62, height=22,
        fill="#14101C", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Shoe R", x=CX+8, y=712, width=62, height=22,
        fill="#14101C", stroke=INK, strokeWidth=4)
# legs
d.shape("rectangle", "Leg L", x=CX-52, y=640, width=44, height=78,
        fill="#1A1624", stroke=INK, strokeWidth=4, radius=8)
d.shape("rectangle", "Leg R", x=CX+8, y=640, width=44, height=78,
        fill="#1A1624", stroke=INK, strokeWidth=4, radius=8)
# the bouncer torso: broad, bulletproof, tuxedoed
d.path(f"M{CX-105},640 C{CX-118},540 {CX-112},470 {CX-90},430 "
       f"C{CX-60},400 {CX+60},400 {CX+90},430 "
       f"C{CX+112},470 {CX+118},540 {CX+105},640 Z",
       "Torso", fill=TUX, stroke=INK, strokeWidth=6)
# shirt wedge and bowtie
d.path(f"M{CX-34},424 L{CX+34},424 L{CX+16},540 L{CX-16},540 Z",
       "Shirt", fill="#E8E2D4", stroke=INK, strokeWidth=3)
d.path(f"M{CX-30},424 L{CX},414 L{CX},434 Z M{CX+30},424 L{CX},414 L{CX},434 Z",
       "Bowtie", fill="#7E1E34", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Bowtie knot", x=CX-7, y=414, width=14, height=14,
        fill="#7E1E34", stroke=INK, strokeWidth=3)
# shirt buttons
for i, y in enumerate([470, 505]):
    d.shape("ellipse", f"Button {i+1}", x=CX-4, y=y, width=8, height=8,
            fill=INK, stroke=NONE)
# lapels
d.path(f"M{CX-34},424 L{CX-70},408 L{CX-56},470 L{CX-20},540 Z",
       "Lapel L", fill="#2A2434", stroke=INK, strokeWidth=3)
d.path(f"M{CX+34},424 L{CX+70},408 L{CX+56},470 L{CX+20},540 Z",
       "Lapel R", fill="#2A2434", stroke=INK, strokeWidth=3)
# the hand that owns the rope: arm down to the right post's cuff
d.path(f"M{CX+96},470 C{CX+140},500 {CX+185},540 {CX+215},568",
       "Arm rope", fill=NONE, stroke="#1C1826", strokeWidth=26,
       cap="round")
d.shape("ellipse", "Hand rope", x=CX+206, y=556, width=26, height=26,
        fill=SKIN, stroke=INK, strokeWidth=4)
# head: bald dome, serene
d.shape("ellipse", "Head", x=CX-56, y=316, width=112, height=104,
        fill=SKIN, stroke=INK, strokeWidth=5)
# five-o'clock shadow under the jaw
d.path(f"M{CX-46},392 C{CX-20},410 {CX+20},410 {CX+46},392 C{CX+30},416 {CX-30},416 {CX-46},392 Z",
       "Stubble", fill="#8A5C40", opacity=45, stroke=NONE)
# shades — he has never once looked over them
d.path(f"M{CX-48},352 C{CX-46},344 {CX-36},340 {CX-24},340 L{CX-8},340 "
       f"C{CX+2},340 {CX+4},346 {CX+4},352 C{CX+4},362 {CX-4},370 {CX-16},370 "
       f"L{CX-32},370 C{CX-42},370 {CX-48},362 {CX-48},352 Z",
       "Shade L", fill="#181420", stroke=INK, strokeWidth=3)
d.path(f"M{CX+8},352 C{CX+8},346 {CX+10},340 {CX+20},340 L{CX+36},340 "
       f"C{CX+46},340 {CX+52},346 {CX+52},354 C{CX+52},364 {CX+44},370 {CX+32},370 "
       f"L{CX+18},370 C{CX+10},370 {CX+8},362 {CX+8},352 Z",
       "Shade R", fill="#181420", stroke=INK, strokeWidth=3)
d.path(f"M{CX-4},348 L{CX+10},348", "Shade bridge", fill=NONE,
       stroke=INK, strokeWidth=3)
d.path(f"M{CX-56},350 L{CX-48},350 M{CX+52},352 L{CX+56},352",
       "Shade arms", fill=NONE, stroke=INK, strokeWidth=3)
d.path(f"M{CX-42},346 C{CX-38},343 {CX-30},342 {CX-24},343",
       "Shade glint L", fill=NONE, stroke="#5A5668", strokeWidth=3,
       cap="round", opacity=80)
# open baritone mouth
d.shape("ellipse", "Mouth", x=CX-14, y=384, width=28, height=22,
        fill="#5A2430", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Mouth tongue", x=CX-8, y=394, width=16, height=10,
        fill="#A04050", stroke=NONE)
# dome sheen
d.shape("ellipse", "Dome sheen", x=CX-40, y=326, width=36, height=18,
        fill="#F4D0B0", opacity=45, stroke=NONE)
# the mic arm: bent up, holding a chrome ribbon mic to the mouth
d.path(f"M{CX-96},470 C{CX-140},490 {CX-150},520 {CX-138},540",
       "Arm mic upper", fill=NONE, stroke="#1C1826", strokeWidth=26,
       cap="round")
d.path(f"M{CX-138},540 C{CX-124},516 {CX-96},472 {CX-44},424",
       "Arm mic fore", fill=NONE, stroke="#1C1826", strokeWidth=22,
       cap="round")
# mic in hand, tilted toward the open mouth
d.shape("ellipse", "Hand mic", x=CX-66, y=414, width=28, height=26,
        fill=SKIN, stroke=INK, strokeWidth=4)
d.path(f"M{CX-48},420 L{CX-60},452", "Mic handle", fill=NONE,
       stroke="#4A4E58", strokeWidth=10, cap="round")
d.shape("ellipse", "Mic head", x=CX-62, y=396, width=30, height=34,
        fill=CHROME, stroke=INK, strokeWidth=4)
for i in range(3):
    y = 404 + i * 8
    d.path(f"M{CX-58},{y} L{CX-36},{y}", f"Mic grill {i+1}", fill=NONE,
           stroke="#5A626C", strokeWidth=2, opacity=80)

# --- the song: notes drifting off, never resolving ---------------------------------
def note(x, y, tag, scale=1.0):
    d.shape("ellipse", f"{tag} head", x=x, y=y, width=20*scale, height=15*scale,
            fill="#D8B88A", stroke=INK, strokeWidth=3)
    d.path(f"M{x+17*scale},{y+7*scale} L{x+17*scale},{y-38*scale} "
           f"C{x+26*scale},{y-34*scale} {x+30*scale},{y-26*scale} {x+32*scale},{y-18*scale}",
           f"{tag} stem", fill=NONE, stroke="#D8B88A", strokeWidth=4,
           cap="round")

note(560, 320, "Note 1", 1.0)
note(622, 270, "Note 2", 0.8)
note(300, 300, "Note 3", 0.85)
# the last note always coincides with somebody leaving — a faint one, going
n4 = note(680, 210, "Note 4", 0.65)

# --- captions ------------------------------------------------------------------
d.text("THRESHOLD CROONER", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#EAD9C4", justify="center")
r = d.text("SOFT GATEKEEPING", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#B89AAA", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("318.threshold-crooner-V1R00")
