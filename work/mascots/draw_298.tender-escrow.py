#!/usr/bin/env python3
"""Tender Escrow — mascot portrait V1R00.
The right answer is known, resourced, and locked: a velvet-lined lockbox
radiating a faint heat through the brass, the stack of signed pages beside
it still waiting on the final key the mascot holds but cannot turn.
1000x1000. Gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Tender Escrow — Mascot Portrait", 1000, 1000)

INK = "#221A20"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#0E1418"}, {"offset": 1, "color": "#06090C"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#36444E"}, {"offset": 0.7, "color": "#1C262E"},
    {"offset": 1, "color": "#0C1216"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#242C32"}, {"offset": 1, "color": "#0E1214"}]}}
BODY = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#C4CBD4"}, {"offset": 0.7, "color": "#96A2AE"},
    {"offset": 1, "color": "#6A7684"}]}}
BRASS = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#C9A24C"}, {"offset": 1, "color": "#8A6428"}]}}
BRASS_DK = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#8A6428"}, {"offset": 1, "color": "#4E3814"}]}}
VELVET = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#8A3A4E"}, {"offset": 0.7, "color": "#5C2434"},
    {"offset": 1, "color": "#341420"}]}}
GLOW = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E8A34C"}, {"offset": 0.6, "color": "#C87E34"},
    {"offset": 1, "color": "#8A5420"}]}}
PAPER = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E4DAC8"}, {"offset": 1, "color": "#B8AA92"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#6E8A9C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C2D4DE", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(193,233,8),(801,230,7),(157,524,9),(837,544,8),
                               (247,766,7),(753,749,9),(133,393,6),(864,391,7),
                               (391,113,7),(613,110,8),(333,823,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#2C3842", opacity=45, stroke=NONE)

# --- floor ----------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0A0C0E",
       strokeWidth=4, opacity=70)

# --- the stand under the lockbox ---------------------------------------------------
d.shape("ellipse", "Stand shadow", x=560, y=676, width=280, height=22,
        fill="#04060A", opacity=55, stroke=NONE)
d.shape("rectangle", "Stand top", x=560, y=566, width=260, height=18,
        fill=BRASS_DK, stroke=INK, strokeWidth=4, radius=6)
d.shape("rectangle", "Stand leg L", x=580, y=584, width=18, height=110,
        fill=BRASS_DK, stroke=INK, strokeWidth=4)
d.shape("rectangle", "Stand leg R", x=782, y=584, width=18, height=110,
        fill=BRASS_DK, stroke=INK, strokeWidth=4)
# warm spill of light on the stand and floor from the open box
d.shape("ellipse", "Light spill", x=560, y=560, width=260, height=30,
        fill="#E8A34C", opacity=18, stroke=NONE)
d.shape("ellipse", "Floor spill", x=570, y=660, width=250, height=34,
        fill="#E8A34C", opacity=12, stroke=NONE)

# --- the lockbox, lid open -------------------------------------------------------------
# open lid, tilted back: a brass panel leaning behind the mouth
d.path("M592,468 L770,428 L782,460 L604,500 Z", "Lid outer", fill=BRASS_DK,
       stroke=INK, strokeWidth=5, join="round")
d.path("M604,468 L758,434 L766,456 L612,490 Z", "Lid velvet face",
       fill=VELVET, stroke=INK, strokeWidth=3, join="round")
# the box mouth: velvet interior glowing faintly hot
d.path("M596,470 L764,470 L748,556 L612,556 Z", "Box interior",
       fill=VELVET, stroke=INK, strokeWidth=5, join="round")
# the heat inside: a warm core sitting in the velvet
d.shape("ellipse", "Warm core", x=636, y=492, width=88, height=44,
        fill=GLOW, stroke="#E8A34C", strokeWidth=2, opacity=95)
d.shape("ellipse", "Hot spot", x=662, y=502, width=40, height=20,
        fill="#F4C478", opacity=85, stroke=NONE)
# front face of the box
d.path("M596,470 L764,470 L748,556 L612,556 Z", "Box front hint",
       fill=NONE, stroke=INK, strokeWidth=5, join="round")
d.shape("rectangle", "Box front", x=600, y=510, width=160, height=58,
        fill=BRASS, stroke=INK, strokeWidth=5, radius=8)
# keyhole on the front, waiting
d.shape("ellipse", "Keyhole", x=672, y=526, width=16, height=16,
        fill="#241A10", stroke=INK, strokeWidth=3)
d.path("M680,538 L674,552 L686,552 Z", "Keyhole slot", fill="#241A10",
       stroke=INK, strokeWidth=2, join="round")
# faint heat shimmer above the open mouth
for i, (x, s) in enumerate([(640,1),(680,-1),(720,1)]):
    d.path(f"M{x},440 C{x+8*s},420 {x-8*s},404 {x+4*s},386",
           f"Heat shimmer {i+1}", fill=NONE, stroke="#E8A34C",
           strokeWidth=4, cap="round", opacity=45)

# --- the stack of signatures, waiting ----------------------------------------------------
# a tall pile of signed sheets beside the box on the stand
for i, (x, y, a) in enumerate([(548,556,-3),(546,548,2),(550,540,-2),
                               (545,532,3),(549,524,-1)]):
    d.path(rot_rect_path(x, y, 74, 16, a), f"Signed sheet {i+1}",
           fill=PAPER, stroke=INK, strokeWidth=3, join="round")
    d.path(f"M{x-22},{y} L{x+18},{y+2}", f"Signature line {i+1}",
           fill=NONE, stroke="#5A4632", strokeWidth=2, opacity=80)
    d.path(f"M{x+8},{y+3} C{x+14},{y-2} {x+20},{y+6} {x+26},{y+1}",
           f"Signature squiggle {i+1}", fill=NONE, stroke="#5A4632",
           strokeWidth=2, cap="round", opacity=80)

# --- the mascot ---------------------------------------------------------------------------
d.shape("ellipse", "Body shadow", x=280, y=668, width=200, height=26,
        fill="#04060A", opacity=55, stroke=NONE)
d.path("M380,392 C446,392 478,444 480,514 C482,584 468,644 458,690 "
       "L302,690 C292,644 278,584 280,514 C282,444 314,392 380,392 Z",
       "Body", fill=BODY, stroke=INK, strokeWidth=6)
d.shape("ellipse", "Body sheen", x=306, y=410, width=96, height=44,
        fill="#FFFFFF", opacity=16, stroke=NONE)
# faint warm cast on the box side of the body
d.path("M470,470 C480,540 470,620 458,672", "Warm rim", fill=NONE,
       stroke="#E8A34C", strokeWidth=6, cap="round", opacity=35)

# face: sincere concern, held too long
d.path("M334,470 C342,478 355,478 362,470", "Eye L", fill=NONE,
       stroke=INK, strokeWidth=6, cap="round")
d.path("M400,470 C407,478 420,478 428,470", "Eye R", fill=NONE,
       stroke=INK, strokeWidth=6, cap="round")
# worry crease between the eyes
d.path("M376,444 L382,458 M390,444 L386,458", "Worry", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round", opacity=70)
# small downturned mouth
d.path("M362,514 C372,506 390,506 398,514", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
d.shape("ellipse", "Blush L", x=318, y=486, width=26, height=12,
        fill="#B08A74", opacity=40, stroke=NONE)
d.shape("ellipse", "Blush R", x=418, y=486, width=26, height=12,
        fill="#B08A74", opacity=40, stroke=NONE)

# --- right arm extended, holding the final key near the lockbox, not turned ------------------
d.path("M464,520 C500,512 528,506 556,502", "Arm R", fill=NONE,
       stroke=INK, strokeWidth=15, cap="round")
d.shape("ellipse", "Hand R", x=552, y=490, width=30, height=24,
        fill=BODY, stroke=INK, strokeWidth=4)
# the final key, held out but not turned: shaft + teeth + bow
d.path("M578,500 L622,496", "Key shaft", fill=NONE, stroke="#D8B45E",
       strokeWidth=6, cap="round")
d.path("M614,497 L614,512 M624,496 L624,510", "Key teeth", fill=NONE,
       stroke="#D8B45E", strokeWidth=5, cap="round")
d.shape("ellipse", "Key bow", x=562, y=490, width=20, height=20,
        fill=NONE, stroke="#D8B45E", strokeWidth=5)
# hesitation marks between key and keyhole
d.path("M648,486 L654,480 M652,498 L660,494", "Hesitation", fill=NONE,
       stroke="#D8B45E", strokeWidth=3, cap="round", opacity=70)

# --- left arm folded back: nothing can be released yet ---------------------------------------
d.path("M292,520 C266,540 264,570 284,588", "Arm L", fill=NONE,
       stroke=INK, strokeWidth=15, cap="round")
d.shape("ellipse", "Hand L", x=272, y=578, width=30, height=24,
        fill=BODY, stroke=INK, strokeWidth=4)

# --- faint cool motes on the waiting side -----------------------------------------------------
for i, (x, y, w) in enumerate([(212,428,5),(306,300,6),(232,634,5),(448,220,5),
                               (180,540,5),(370,180,5)]):
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#A6BCC8", opacity=35, stroke=NONE)

# --- captions -------------------------------------------------------------------------
d.text("TENDER ESCROW", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#E4EAF0", justify="center")
r = d.text("CARE HELD IN TRUST", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#A9BCCD", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("298.tender-escrow-V1R00")
