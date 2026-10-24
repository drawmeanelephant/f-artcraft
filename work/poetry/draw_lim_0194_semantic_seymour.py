#!/usr/bin/env python3
"""LIM-0194 Semantic Seymour — limerick plate V1R00. Semantic supremacy
made visual: Seymour scowling under the cape of an unused <aside>, red
pencil annotating a printed screenshot, private validator humming, DOM
inspections by moonlight. W3C spec-paper palette, red annotation marks.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("LIM-0194 Semantic Seymour — Limerick Plate", 1000, 1000)

INK = "#2A2118"
RED = "#C23A2E"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1A1510"}, {"offset": 1, "color": "#0C0A07"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#524838"}, {"offset": 0.7, "color": "#332C21"},
    {"offset": 1, "color": "#1A1510"}]}}
ROBE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6E6252"}, {"offset": 1, "color": "#3E352A"}]}}
CAPE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4A4034"}, {"offset": 1, "color": "#26201A"}]}}
SKIN = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E4D4B8"}, {"offset": 0.75, "color": "#BFA88A"},
    {"offset": 1, "color": "#8A7458"}]}}
PAPER = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#EDE6D4"}, {"offset": 1, "color": "#C9BFA4"}]}}
CREAM = "#EBDCC0"
TAN = "#B09A7A"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#7A6A50", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8DCC4", strokeWidth=3, opacity=45)
# ghost tags haunting the spec sheet
for i, (tag, tx, ty, ts, op) in enumerate([
        ("<main>", 180, 280, 15, 30), ("<article>", 720, 250, 15, 28),
        ("<nav>", 790, 520, 15, 26), ("</div>", 190, 620, 15, 30),
        ("<section>", 660, 790, 15, 24), ("<footer>", 300, 180, 14, 26)]):
    d.text(tag, f"Ghost tag {i+1}", x=tx, y=ty, size=ts,
           font="Virelai Sans", color="#6E5F4A", justify="center")
# moon for the night-shift DOM inspections — a true crescent
d.path("M206,140 A40,40 0 0 0 206,220 A46,46 0 0 1 206,140 Z",
       "Moon", fill="#E8DCC4", opacity=75, stroke=NONE)

# --- the printed screenshot, annotated in red ------------------------------------
card_ids = []
def card_add(res):
    if res and res.get("id"):
        card_ids.append(res["id"])

card_add(d.shape("rectangle", "Screenshot card", x=172, y=330, width=210,
                 height=180, radius=4, fill=PAPER, stroke=INK,
                 strokeWidth=4))
card_add(d.shape("rectangle", "Browser chrome", x=172, y=330, width=210,
                 height=24, radius=4, fill="#8A7E68", stroke=INK,
                 strokeWidth=3))
for i, dx in enumerate([184, 196, 208]):
    card_add(d.shape("ellipse", f"Chrome dot {i+1}", x=dx, y=338, width=8,
                     height=8, fill="#4A4034", stroke=NONE))
for i, line in enumerate(["<div class=\"everything\">", "<div>",
                          "<div>", "</div></div></div>"]):
    card_add(d.text(line, f"Code line {i+1}", x=184, y=382 + i * 28,
                    size=12, font="Virelai Sans", color="#4A4034",
                    justify="left"))
# red corrections: strike the first div, circle the third
card_add(d.path("M182,386 L312,386", "Strike", fill=NONE, stroke=RED,
                strokeWidth=3, cap="round"))
card_add(d.text("<section>", "Fix", x=214, y=374, size=11,
                font="Virelai Sans", color=RED, justify="left"))
card_add(d.shape("ellipse", "Circle tag", x=180, y=430, width=64,
                 height=26, fill=NONE, stroke=RED, strokeWidth=2.5))
card_add(d.path("M246,448 C280,462 296,478 302,496", "Arrow", fill=NONE,
                stroke=RED, strokeWidth=2.5, cap="round"))
card_add(d.path("M298,498 L308,496 L303,488 Z", "Arrowhead", fill=RED,
                stroke=NONE))
card_add(d.text("semantic!", "Margin note", x=306, y=506, size=11,
                font="Virelai Sans", color=RED, justify="left"))
if card_ids:
    d.call("transform", {"ids": card_ids, "rotate": -7,
                         "origin": [277, 420]}, "tilt card")

# --- the private validator, humming -------------------------------------------------
d.shape("rectangle", "Validator", x=700, y=640, width=150, height=96,
        radius=10, fill={"gradient": {"kind": "linear", "stops": [
            {"offset": 0, "color": "#5E5348"},
            {"offset": 1, "color": "#36302A"}]}},
        stroke=INK, strokeWidth=4)
d.shape("ellipse", "Validator lamp", x=712, y=654, width=14, height=14,
        fill="#7EC27E", stroke=INK, strokeWidth=2)
d.shape("ellipse", "Lamp glow", x=708, y=650, width=22, height=22,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#9EE89E", "opacity": 0.5},
            {"offset": 1, "color": "#9EE89E", "opacity": 0}]}},
        stroke=NONE)
d.text("PRIVATE", "Validator tag 1", x=792, y=676, size=13,
       font="Virelai Sans", color=CREAM, justify="center")
d.text("VALIDATOR", "Validator tag 2", x=792, y=694, size=13,
       font="Virelai Sans", color=TAN, justify="center")
d.path("M716,716 L834,716", "Validator slot", fill=NONE, stroke=INK,
       strokeWidth=3, opacity=70)
# hum waves off the left side
for i, (hx, hr) in enumerate([(686, 12), (664, 18), (640, 24)]):
    d.path(f"M{hx},{708-hr} A{hr},{hr} 0 0 0 {hx},{708+hr}",
           f"Hum {i+1}", fill=NONE, stroke="#B09A7A", strokeWidth=2.5,
           opacity=50, cap="round")

# --- Seymour: scowl, <aside> cape, red pencil ---------------------------------------
d.shape("ellipse", "Seymour shadow", x=455, y=782, width=210, height=24,
        fill="#0C0A07", opacity=45, stroke=NONE)
# the cape of the unused <aside>, billowing left
d.path("M512,448 C460,500 430,600 418,720 L478,742 C500,640 512,540 "
       "520,470 Z",
       "Aside cape", fill=CAPE, stroke=INK, strokeWidth=4, join="round")
d.path("M440,680 C450,640 462,590 478,540", "Cape fold", fill=NONE,
       stroke="#5E5348", strokeWidth=5, opacity=60, cap="round")
d.text("<aside>", "Cape hem tag", x=455, y=712, size=13,
       font="Virelai Sans", color=TAN, justify="center")
# robed body
d.path("M510,470 L610,470 L626,782 L494,782 Z", "Seymour robe",
       fill=ROBE, stroke=INK, strokeWidth=5, join="round")
d.path("M522,486 L512,760", "Robe sheen", fill=NONE, stroke="#E8DCC4",
       strokeWidth=7, opacity=15, cap="round")
# stiff validator collar
d.path("M540,470 L560,496 L580,470", "Collar", fill=NONE, stroke="#EDE6D4",
       strokeWidth=6, join="round")
# head
d.shape("ellipse", "Seymour head", x=514, y=356, width=92, height=92,
        fill=SKIN, stroke=INK, strokeWidth=5)
# the scowl: brows driven down toward the nose
d.path("M532,396 L552,404", "Brow L", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
d.path("M588,396 L568,404", "Brow R", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
d.path("M556,398 L556,410 M564,398 L564,410", "Furrow", fill=NONE,
       stroke=INK, strokeWidth=2.5, cap="round", opacity=70)
d.shape("ellipse", "Eye L", x=537, y=410, width=11, height=13,
        fill="#2A2118", stroke=NONE)
d.shape("ellipse", "Eye R", x=573, y=410, width=11, height=13,
        fill="#2A2118", stroke=NONE)
# downturned mouth — tag-shaming in progress
d.path("M540,438 Q560,428 580,438", "Scowl mouth", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
# severe side part
d.path("M518,370 C540,352 580,352 602,368", "Hairline", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round", opacity=60)
# left arm reaching toward the annotated screenshot
d.path("M512,500 C476,506 448,522 428,546", "Arm L", fill=NONE,
       stroke="#3E352A", strokeWidth=20, cap="round")
d.shape("ellipse", "Hand L", x=414, y=536, width=26, height=24,
        fill="#BFA88A", stroke=INK, strokeWidth=4)
# right arm raised, red pencil high like a censor's blade
d.path("M606,492 C636,478 656,458 668,432", "Arm R", fill=NONE,
       stroke="#3E352A", strokeWidth=20, cap="round")
d.shape("ellipse", "Hand R", x=656, y=414, width=26, height=24,
        fill="#BFA88A", stroke=INK, strokeWidth=4)
d.path("M666,428 L694,388", "Red pencil", fill=NONE, stroke=RED,
       strokeWidth=9, cap="round")
d.path("M691,392 L702,378 L696,396 Z", "Pencil tip", fill="#EBDCC0",
       stroke=INK, strokeWidth=1.5)
# annotation sparks off the pencil
for i, (ax, ay) in enumerate([(706, 372), (692, 366), (712, 388)]):
    d.path(f"M{ax},{ay} l5,-5", f"Red mark {i+1}", fill=NONE, stroke=RED,
           strokeWidth=2.5, cap="round", opacity=80)

# --- name + role ------------------------------------------------------------------
d.text("SEMANTIC SEYMOUR", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color=CREAM, justify="center")
r = d.text("LIM-0194 SEMANTIC SEYMOUR", "Role", x=500, y=968, size=20,
           font="Virelai Sans", color=TAN, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=170)

d.finish("lim-0194-semantic-seymour-V1R00")
