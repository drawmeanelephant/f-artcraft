#!/usr/bin/env python3
"""Datty Puritas — mascot portrait V1R00.
Ritualist chanting in indentation cadence over a YAML scroll: clean
key lines hold fast while the malformed keys lift off the page and
dissolve into red motes. 1000x1000. Gradients + translucent shading."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Datty Puritas — Mascot Portrait", 1000, 1000)

INK = "#201A14"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#141C22"}, {"offset": 1, "color": "#080C10"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4C5E6A"}, {"offset": 0.7, "color": "#32424C"},
    {"offset": 1, "color": "#181F28"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2E363C"}, {"offset": 1, "color": "#12161A"}]}}
ROBE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3E6A66"}, {"offset": 0.65, "color": "#2A4C4C"},
    {"offset": 1, "color": "#16302F"}]}}
SKIN = "#DCC6A4"
GOLD = "#E0C078"
PARCH = "#EFE6CE"
MOTE = "#D86454"
CHANT = "#E8D9A8"

def rot_pt(cx, cy, x, y, deg):
    a = math.radians(deg); c, s = math.cos(a), math.sin(a)
    return (cx + (x - cx) * c - (y - cy) * s,
            cy + (x - cx) * s + (y - cy) * c)

# --- backdrop + plate ----------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#6E8290", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#BCCCD4", strokeWidth=3, opacity=35)
d.shape("ellipse", "Patina 1", x=190, y=210, width=220, height=140,
        fill="#5E7880", opacity=18, stroke=NONE)
d.shape("ellipse", "Patina 2", x=590, y=600, width=240, height=150,
        fill="#5E7880", opacity=16, stroke=NONE)

# --- the rite circle: faint indentation-grid on the plate --------------------------
for i, x in enumerate([300, 340, 380]):
    d.path(f"M{x},250 L{x},330", f"Indent guide {i+1}", fill=NONE,
           stroke="#7E96A0", strokeWidth=2, dash=[3, 6], opacity=40)
for i, x in enumerate([640, 680, 720]):
    d.path(f"M{x},560 L{x},640", f"Indent guide R{i+1}", fill=NONE,
           stroke="#7E96A0", strokeWidth=2, dash=[3, 6], opacity=40)
# floating clean keys, at rest
for i, (cx, cy, w, deg) in enumerate([(268, 400, 92, -8), (736, 380, 84, 7),
                                      (700, 210, 96, -5)]):
    d.path(rot_rect_path(cx, cy, w, 26, deg), f"Calm key {i+1}",
           fill="#3E5460", stroke="#8AA0AA", strokeWidth=2,
           join="round", opacity=75)
    x1 = cx - w/2 + 12; x2 = cx + w/2 - 12
    a = rot_pt(cx, cy, x1, cy, deg); b = rot_pt(cx, cy, x2, cy, deg)
    d.path(f"M{a[0]:.0f},{a[1]:.0f} L{b[0]:.0f},{b[1]:.0f}",
           f"Calm key line {i+1}", fill=NONE, stroke="#B8CCC8",
           strokeWidth=4, cap="round", opacity=70)

# --- floor ----------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0A0E12",
       strokeWidth=4, opacity=70)

# --- Datty: mid-chant over the scroll -----------------------------------------------
# robe: broad shoulders, kneeling-wide hem behind the scroll
d.path("M500,430 C566,430 606,478 614,548 C620,608 632,660 648,694 "
       "C566,712 434,712 352,694 C368,660 380,608 386,548 "
       "C394,478 434,430 500,430 Z",
       "Robe", fill=ROBE_GRAD, stroke=INK, strokeWidth=6, join="round")
# ceremonial stole with gold fringe
d.path("M486,452 L476,660 M514,452 L524,660", "Stole edges", fill=NONE,
       stroke=GOLD, strokeWidth=5, cap="round", opacity=90)
for i, y in enumerate(range(470, 650, 30)):
    d.path(f"M484,{y} L478,{y+8} M516,{y} L522,{y+8}", f"Stole bar {i+1}",
           fill=NONE, stroke=GOLD, strokeWidth=2.5, cap="round",
           opacity=70)
# --- the YAML scroll, unrolled across her feet -------------------------------------
d.shape("ellipse", "Datty shadow", x=380, y=684, width=250, height=24,
        fill="#05080A", opacity=50, stroke=NONE)
# scroll sheet with rolled top and bottom edges
d.path("M388,548 L620,548 C630,560 630,574 620,584 L628,676 "
       "C630,690 622,700 608,700 L398,700 C384,700 376,690 378,676 "
       "L386,584 C376,574 376,560 388,548 Z",
       "Scroll", fill=PARCH, stroke="#8A7C58", strokeWidth=4,
       join="round")
d.path("M388,548 C430,538 578,538 620,548 C578,558 430,558 388,548 Z",
       "Scroll top roll", fill="#D8CCA8", stroke="#8A7C58",
       strokeWidth=3, join="round")
# indentation guides down the sheet
for i, x in enumerate([416, 452, 488]):
    d.path(f"M{x},584 L{x},676", f"Sheet indent {i+1}", fill=NONE,
           stroke="#C4B890", strokeWidth=1.5, dash=[3, 5], opacity=70)
# clean keys: bars + colon dots, holding fast
for i, (ly, x1, kw, vx) in enumerate([(594, 402, 44, 68),
                                      (620, 402, 40, 76),
                                      (646, 438, 36, 60),
                                      (672, 438, 42, 66)]):
    d.path(f"M{x1},{ly} L{x1+kw},{ly}", f"Key {i+1}", fill=NONE,
           stroke="#6E6448", strokeWidth=6, cap="round")
    d.shape("ellipse", f"Key {i+1} colon", x=x1+kw+7, y=ly-3, width=6,
            height=6, fill="#6E6448", stroke=NONE)
    d.path(f"M{x1+kw+22},{ly} L{x1+kw+22+vx},{ly}", f"Val {i+1}",
           fill=NONE, stroke="#9A8F6A", strokeWidth=6, cap="round",
           opacity=85)

# both arms raised in the chant
d.path("M430,540 C390,520 356,486 344,442", "Arm L ink", fill=NONE,
       stroke=INK, strokeWidth=32, cap="round")
d.path("M430,540 C390,520 356,486 344,442", "Arm L", fill=NONE,
       stroke="#2A4C4C", strokeWidth=22, cap="round")
d.path("M570,540 C610,520 644,486 656,442", "Arm R ink", fill=NONE,
       stroke=INK, strokeWidth=32, cap="round")
d.path("M570,540 C610,520 644,486 656,442", "Arm R", fill=NONE,
       stroke="#2A4C4C", strokeWidth=22, cap="round")
# open palms, up
d.shape("ellipse", "Palm L", x=320, y=412, width=40, height=32,
        fill=SKIN, stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Palm R", x=640, y=412, width=40, height=32,
        fill=SKIN, stroke=INK, strokeWidth=3.5)
for i, (px, flip) in enumerate([(340, -1), (640, 1)]):
    d.path(f"M{px-14*flip},422 L{px-26*flip},412 "
           f"M{px-8*flip},412 L{px-14*flip},398 "
           f"M{px+2*flip},410 L{px+4*flip},394",
           f"Fingers {'L' if flip<0 else 'R'}", fill=NONE, stroke=INK,
           strokeWidth=3.5, cap="round")

# head: open hood, face lifted mid-syllable
d.path("M500,346 C556,346 590,388 590,438 C590,478 562,504 500,504 "
       "C438,504 410,478 410,438 C410,388 444,346 500,346 Z",
       "Hood", fill=ROBE_GRAD, stroke=INK, strokeWidth=6)
d.shape("ellipse", "Face", x=438, y=392, width=124, height=96,
        fill=SKIN, stroke=NONE)
# face dusk inside the hood rim
d.path("M438,428 C444,398 464,382 500,382 C536,382 556,398 562,428 "
       "C548,404 524,396 500,396 C476,396 452,404 438,428 Z",
       "Hood shade", fill="#16302F", opacity=55, stroke=NONE)
# closed chant eyes + open mouth mid-syllable
d.path("M456,432 C464,426 474,426 480,432", "Eye L", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.path("M520,432 C526,426 536,426 544,432", "Eye R", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.shape("ellipse", "Chant mouth", x=486, y=448, width=28, height=22,
        fill="#5E3428", stroke=INK, strokeWidth=3)
# brows lifted in devotion to schema
d.path("M450,414 C462,406 478,406 486,412", "Brow L", fill=NONE,
       stroke=INK, strokeWidth=3.5, cap="round")
d.path("M514,412 C522,406 538,406 550,414", "Brow R", fill=NONE,
       stroke=INK, strokeWidth=3.5, cap="round")

# --- the chant: syllable arcs rising from her mouth ----------------------------------
d.path("M470,330 C486,314 514,314 530,330", "Chant arc 1", fill=NONE,
       stroke=CHANT, strokeWidth=4, cap="round", opacity=75)
d.path("M452,306 C478,282 522,282 548,306", "Chant arc 2", fill=NONE,
       stroke=CHANT, strokeWidth=4, cap="round", opacity=55)
d.path("M436,280 C472,248 528,248 564,280", "Chant arc 3", fill=NONE,
       stroke=CHANT, strokeWidth=4, cap="round", opacity=38)

# --- malformed keys, dissolving off the page ------------------------------------------
# two red keys mid-flight above the scroll, breaking into motes
for i, (cx, cy, w, deg) in enumerate([(566, 512, 60, 16), (440, 520, 54, -13)]):
    d.path(rot_rect_path(cx, cy, w, 18, deg), f"Bad key {i+1}",
           fill=MOTE, stroke="#8A3628", strokeWidth=2, join="round",
           opacity=85)
# the dissolution: motes scatter upward, thinning as they rise
motes = [(584, 476, 8), (596, 446, 6), (606, 414, 6), (614, 384, 4),
         (452, 484, 7), (444, 452, 5), (438, 420, 5), (434, 390, 3),
         (500, 330, 5), (520, 300, 4)]
for i, (x, y, s) in enumerate(motes):
    d.shape("rectangle", f"Mote {i+1}", x=x, y=y, width=s, height=s,
            fill=MOTE, opacity=max(25, 80 - i * 6), stroke=NONE,
            radius=1)

# --- captions ----------------------------------------------------------------------
d.text("DATTY PURITAS", "Name", x=500, y=930, size=58,
       font="Virelai Sans", color="#E2E8E4", justify="center")
r = d.text("PURGER OF MALFORMED KEYS", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#A4B8B2", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("073.datty-puritas-V1R00")
