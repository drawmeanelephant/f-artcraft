#!/usr/bin/env python3
"""Shorthand Reliquary — mascot portrait V1R00.
The mascot stands custodian over a gilded reliquary whose shrine holds a
single post-it note: the letter F and a tiny bulleted list, the whole
record compressed to fit the glass. 1000x1000.
Gradients + translucent shading, no flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Shorthand Reliquary — Mascot Portrait", 1000, 1000)

INK = "#20180F"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#0D1214"}, {"offset": 1, "color": "#060809"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#62593F"}, {"offset": 0.7, "color": "#443E2C"},
    {"offset": 1, "color": "#272319"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3C372A"}, {"offset": 1, "color": "#1C1912"}]}}
FUR_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#D8B892"}, {"offset": 0.7, "color": "#B08A62"},
    {"offset": 1, "color": "#84643F"}]}}
GOLD_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E8C868"}, {"offset": 0.55, "color": "#B8933A"},
    {"offset": 1, "color": "#7A5E20"}]}}
CAVITY_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#3A2E1A"}, {"offset": 1, "color": "#1C150C"}]}}
POSTIT_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F0E28A"}, {"offset": 1, "color": "#D3BE5C"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#8A7A50", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8C896", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(193,234,8),(801,229,7),(157,526,9),(837,544,8),
                               (246,766,7),(754,748,9),(133,394,6),(865,389,7),
                               (391,112,7),(613,109,8),(333,824,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#4E4634", opacity=45, stroke=NONE)

# --- floor ---------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#100D08",
       strokeWidth=4, opacity=70)

# --- the halo the note was never asked to earn ------------------------------------
d.shape("ellipse", "Halo glow", x=230, y=240, width=330, height=330,
        fill="#E8C868", opacity=12, stroke=NONE)
for i, (x2, y2) in enumerate([(300, 165), (395, 150), (470, 185),
                              (205, 300), (215, 415)]):
    d.path(f"M395,455 L{x2},{y2} L{x2+26},{y2+18} Z", f"Halo ray {i+1}",
           fill="#E8C868", opacity=10, stroke=NONE)

# --- the mascot, guarding ---------------------------------------------------------
d.shape("ellipse", "Body", x=575, y=430, width=185, height=225,
        fill=FUR_GRAD, stroke=INK, strokeWidth=5)
# feet on the floor
for x in (585, 690):
    d.shape("ellipse", f"Foot {x}", x=x, y=646, width=58, height=24,
            fill="#84643F", stroke=INK, strokeWidth=4)
# head + ears
for ex in (600, 742):
    d.shape("ellipse", f"Ear {ex}", x=ex - 11, y=300, width=26, height=24,
            fill="#B08A62", stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Head", x=596, y=302, width=150, height=136,
        fill=FUR_GRAD, stroke=INK, strokeWidth=5)
# wide solemn eyes — it does not interpret what it guards
d.shape("ellipse", "Eye L", x=630, y=358, width=17, height=21,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Eye R", x=694, y=358, width=17, height=21,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Glint L", x=634, y=362, width=5, height=6,
        fill="#FFF8E8", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=698, y=362, width=5, height=6,
        fill="#FFF8E8", opacity=90, stroke=NONE)
# raised inner brows — vigilance, not worry
d.path("M624,342 C634,336 646,336 654,342", "Brow L", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.path("M688,342 C698,336 710,336 718,342", "Brow R", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
# flat keeper's mouth
d.path("M658,404 L694,404", "Mouth", fill=NONE, stroke=INK,
       strokeWidth=4, cap="round")

# --- the reliquary ------------------------------------------------------------------
# stepped plinth
d.path("M275,600 L485,600 L500,630 L260,630 Z", "Plinth step 1",
       fill=GOLD_GRAD, stroke=INK, strokeWidth=4, join="round")
d.path("M252,630 L508,630 L524,662 L236,662 Z", "Plinth step 2",
       fill="#8A6E30", stroke=INK, strokeWidth=4, join="round")
# case: gothic arch body
d.path("M288,600 L288,422 C288,362 328,328 380,328 "
       "C432,328 472,362 472,422 L472,600 Z", "Case",
       fill=GOLD_GRAD, stroke=INK, strokeWidth=5, join="round")
# dome + finial
d.shape("ellipse", "Case dome", x=356, y=306, width=48, height=30,
        fill=GOLD_GRAD, stroke=INK, strokeWidth=4)
d.path("M380,288 L372,308 L388,308 Z", "Finial", fill="#E8C868",
       stroke=INK, strokeWidth=3)
# inner cavity
d.path("M316,584 L316,432 C316,388 346,362 380,362 "
       "C414,362 444,388 444,432 L444,584 Z", "Cavity",
       fill=CAVITY_GRAD, stroke=INK, strokeWidth=3.5)
# corner rivets
for i, (x, y) in enumerate([(300,590),(460,590),(300,432),(460,432),
                            (380,340)]):
    d.shape("ellipse", f"Rivet {i+1}", x=x-4, y=y-4, width=8, height=8,
            fill="#E8C868", stroke=INK, strokeWidth=2)

# --- the relic: a post-it note -----------------------------------------------------
d.path(rot_rect_path(380, 470, 80, 80, -5), "Post-it",
       fill=POSTIT_GRAD, stroke=INK, strokeWidth=3)
# dog-ear curl
d.path("M400,504 L416,490 L415,506 Z", "Post-it curl",
       fill="#B8A44E", stroke=INK, strokeWidth=2)
# the letter F — all of it
d.text("F", "Relic letter", x=380, y=470, size=36, font="Virelai Sans",
       color="#4A3E1E", justify="center")
# the tiny bulleted list
for i, y in enumerate([483, 492, 501]):
    d.shape("ellipse", f"Bullet {i+1}", x=354, y=y-2, width=4, height=4,
            fill="#4A3E1E", stroke=NONE)
    d.path(f"M362,{y} L{394 - i * 6},{y}", f"Bullet line {i+1}",
           fill=NONE, stroke="#4A3E1E", strokeWidth=2.5, cap="round")
# glass sheen over the relic
d.path("M330,560 L352,392 L368,382 L346,560 Z", "Glass sheen",
       fill="#E8F0E8", opacity=16, stroke=NONE)

# --- guardian paws on the shrine ----------------------------------------------------
# one paw flat on the case edge
d.path("M590,520 C550,512 512,504 492,500", "Case arm", fill=NONE,
       stroke="#B08A62", strokeWidth=20, cap="round")
d.shape("ellipse", "Case paw", x=452, y=486, width=40, height=30,
        fill="#D8B892", stroke=INK, strokeWidth=4)
d.path("M468,490 L484,488 M468,498 L484,498 M468,506 L482,508",
       "Case paw toes", fill=NONE, stroke=INK, strokeWidth=2.5,
       cap="round", opacity=70)
# one paw hovering over the dome — the custody gesture
d.path("M612,470 C590,436 566,402 540,378", "Guard arm", fill=NONE,
       stroke="#B08A62", strokeWidth=20, cap="round")
d.shape("ellipse", "Guard paw", x=510, y=348, width=44, height=34,
        fill="#D8B892", stroke=INK, strokeWidth=4)
d.path("M522,356 L522,340 M534,354 L536,338 M546,356 L550,342",
       "Guard paw toes", fill=NONE, stroke=INK, strokeWidth=2.5,
       cap="round", opacity=70)

# --- votive candles ------------------------------------------------------------------
for i, cx in enumerate([(238,), (524,)]):
    cx = cx[0]
    d.shape("ellipse", f"Candle glow {i+1}", x=cx-34, y=452, width=68,
            height=60, fill="#F0C878", opacity=14, stroke=NONE)
    d.path(f"M{cx-3},466 C{cx-9},456 {cx-7},446 {cx},438 "
           f"C{cx+7},446 {cx+9},456 {cx+3},466 Z", f"Flame {i+1}",
           fill="#F0C060", stroke="#B87828", strokeWidth=2, opacity=95)
    d.path(f"M{cx},468 L{cx},476", f"Wick {i+1}", fill=NONE,
           stroke=INK, strokeWidth=2.5)
    d.shape("rectangle", f"Candle {i+1}", x=cx-11, y=476, width=22,
            height=46, fill="#E4D6B4", stroke=INK, strokeWidth=3, radius=4)
    d.shape("ellipse", f"Candle wax {i+1}", x=cx-11, y=472, width=22,
            height=8, fill="#C8B88E", stroke=INK, strokeWidth=2.5)
    d.path(f"M{cx-16},522 L{cx+16},522 L{cx+22},532 L{cx-22},532 Z",
           f"Candle cup {i+1}", fill=GOLD_GRAD, stroke=INK,
           strokeWidth=3, join="round")

# --- motes ------------------------------------------------------------------------------
for i, (x, y, w) in enumerate([(262,420,5),(244,560,6),(648,240,5),(836,470,6),
                               (224,640,5),(812,300,6),(548,212,5)]):
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#E8C878", opacity=40, stroke=NONE)

# --- captions -------------------------------------------------------------------------
d.text("SHORTHAND RELIQUARY", "Name", x=500, y=930, size=54,
       font="Virelai Sans", color="#F0E4C8", justify="center")
r = d.text("KEEPER OF THE UNEXPANDED", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#C8B084", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("272.shorthand-reliquary-V1R00")
