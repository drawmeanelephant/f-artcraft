#!/usr/bin/env python3
"""Carpet Jurisdiction — mascot portrait V1R00.
The mascot stands on the plush side of the one border everyone
observes and no one will minute. Beyond the brass threshold strip:
industrial tile, where disagreements are formally logged.
Asked where the decision was made, it indicated the threshold.
1000x1000. Gradients + translucent shading, no flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Carpet Jurisdiction — Mascot Portrait", 1000, 1000)

INK = "#2A1E26"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1C1420"}, {"offset": 1, "color": "#0C0810"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#554252"}, {"offset": 0.7, "color": "#3B2E3C"},
    {"offset": 1, "color": "#1E1722"}]}}
CARPET_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7A3A50"}, {"offset": 0.6, "color": "#5C2A3E"},
    {"offset": 1, "color": "#3E1C2C"}]}}
TILE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#565F6E"}, {"offset": 0.6, "color": "#3B434F"},
    {"offset": 1, "color": "#252B35"}]}}
FUR_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#D6BA96"}, {"offset": 0.7, "color": "#A9885F"},
    {"offset": 1, "color": "#7A5C3E"}]}}
BRASS_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E0BA6A"}, {"offset": 0.55, "color": "#AE8640"},
    {"offset": 1, "color": "#73552A"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#7A6070", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8C6D2", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(196,236,8),(800,232,7),(160,528,9),(836,548,8),
                               (250,764,7),(750,750,9),(138,396,6),(862,392,7),
                               (394,114,7),(612,110,8),(336,822,6),(664,820,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#463646", opacity=45, stroke=NONE)

# --- the ground: plush carpet ending at the brass strip, tile beyond --------------
# carpet fills the back of the room to the threshold (chord ends on the disc arc)
d.path("M92,560 L908,560 A420,420 0 0 1 92,560 Z", "Carpet field",
       fill=CARPET_GRAD, stroke=NONE)
# baseboard where the wall meets the weave — the second-quietest border
d.path("M100,548 L900,548 L900,560 L100,560 Z", "Baseboard",
       fill="#2C2230", opacity=85, stroke=NONE)
d.path("M100,549 L900,549", "Baseboard cap", fill=NONE, stroke="#5A4656",
       strokeWidth=2.5, opacity=60)
# pile nap: short strokes raked one way, denser near the threshold
import random
random.seed(293)
for i in range(150):
    x = random.uniform(150, 850); y = random.uniform(575, 800)
    # stay inside the disc (cx 500 cy 460 r 420)
    if (x - 500) ** 2 + (y - 460) ** 2 > 405 ** 2:
        continue
    dx = random.uniform(-4, 4)
    d.path(f"M{x:.0f},{y:.0f} L{x + dx:.0f},{y - random.uniform(5, 10):.0f}",
           f"Nap {i+1}", fill=NONE, stroke="#9A5268", strokeWidth=2,
           cap="round", opacity=random.choice([25, 35, 45]))
# sound dying into the pile — dissent, absorbed at the weave
for i, x in enumerate([330, 700]):
    d.path(f"M{x - 40},{646 + i * 10} A40,22 0 0 1 {x + 40},{646 + i * 10}",
           f"Absorbed ripple {i+1}", fill=NONE, stroke="#B47A8E",
           strokeWidth=3, opacity=30 - i * 8, cap="round")

# --- industrial tile: the foreground, where objections are filed ----------------------
d.path("M272,812 L728,812 A420,420 0 0 1 272,812 Z", "Tile field",
       fill=TILE_GRAD, stroke=NONE)
# tile seams: transverse joints running back toward the strip
for tx in (340, 430, 520, 610):
    d.path(f"M{tx},812 L{tx + 14},860", f"Tile seam {tx}", fill=NONE,
           stroke="#1E2530", strokeWidth=3, opacity=65)
d.path("M296,840 L700,844", "Tile joint", fill=NONE, stroke="#1E2530",
       strokeWidth=3, opacity=60)
# hard sheen — tile returns the light the carpet swallows
d.path("M310,818 L560,816 L566,827 L306,829 Z", "Tile sheen",
       fill="#FFFFFF", opacity=10, stroke=NONE)
# one scuff — the tile keeps a record the carpet cannot
d.path("M590,838 C610,832 632,834 646,843", "Scuff", fill=NONE,
       stroke="#78828E", strokeWidth=3, opacity=45, cap="round")

# --- the brass threshold strip: the border no one will minute ----------------------------
# trapezoid band tapering with the floor plane
d.path("M236,786 L764,786 L728,812 L272,812 Z", "Threshold strip",
       fill=BRASS_GRAD, stroke=INK, strokeWidth=4, join="round")
d.path("M244,790 L756,790", "Strip bevel", fill=NONE, stroke="#F0D68E",
       strokeWidth=2.5, opacity=60)
# countersunk screws, evenly spaced, all facing the soft side
for sx in (300, 400, 500, 600, 700):
    d.shape("ellipse", f"Screw {sx}", x=sx - 6, y=792, width=12, height=12,
            fill="#8A6830", stroke=INK, strokeWidth=3)
    d.path(f"M{sx - 3},798 L{sx + 3},798", f"Screw slot {sx}", fill=NONE,
           stroke=INK, strokeWidth=2, opacity=75)

# --- the mascot, standing on the soft side ----------------------------------------------
d.shape("ellipse", "Shadow on pile", x=392, y=744, width=216, height=26,
        fill="#20101C", opacity=45, stroke=NONE)
# feet pressed into the pile — the pile holds them
d.shape("ellipse", "Foot L", x=422, y=724, width=60, height=32,
        fill="#A9885F", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Foot R", x=518, y=724, width=60, height=32,
        fill="#A9885F", stroke=INK, strokeWidth=4)
# dimples where the feet sink in
d.shape("ellipse", "Sink L", x=414, y=748, width=76, height=12,
        fill="#2E1420", opacity=35, stroke=NONE)
d.shape("ellipse", "Sink R", x=510, y=748, width=76, height=12,
        fill="#2E1420", opacity=35, stroke=NONE)
# body
d.shape("ellipse", "Body", x=400, y=505, width=200, height=235,
        fill=FUR_GRAD, stroke=INK, strokeWidth=5)
# arms down, the right one indicating the threshold
d.path("M412,600 C392,644 386,684 388,716", "Arm L", fill=NONE,
       stroke="#A9885F", strokeWidth=18, cap="round")
d.path("M588,596 C606,634 614,672 616,704", "Arm R", fill=NONE,
       stroke="#A9885F", strokeWidth=18, cap="round")
d.shape("ellipse", "Paw L", x=374, y=708, width=32, height=28,
        fill="#D6BA96", stroke=INK, strokeWidth=4)
# the indicating paw, held low and open over the strip
d.shape("ellipse", "Paw R", x=602, y=698, width=32, height=28,
        fill="#D6BA96", stroke=INK, strokeWidth=4)
d.path("M617,724 L612,748", "Indicating finger", fill=NONE,
       stroke="#D6BA96", strokeWidth=10, cap="round")
# ears
for ex in (448, 552):
    d.shape("ellipse", f"Ear {ex}", x=ex - 13, y=338, width=29, height=27,
            fill="#A9885F", stroke=INK, strokeWidth=3.5)
# head
d.shape("ellipse", "Head", x=406, y=346, width=188, height=170,
        fill=FUR_GRAD, stroke=INK, strokeWidth=5)
# composed eyes — it has watched rulings land softer
d.shape("ellipse", "Eye L", x=446, y=414, width=17, height=14,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Eye R", x=537, y=414, width=17, height=14,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Glint L", x=449, y=417, width=4, height=4,
        fill="#FFF6E4", opacity=80, stroke=NONE)
d.shape("ellipse", "Glint R", x=540, y=417, width=4, height=4,
        fill="#FFF6E4", opacity=80, stroke=NONE)
# level, unbothered mouth
d.path("M483,462 C491,466 511,466 519,462", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=3.5, cap="round")

# --- motes, hushed ---------------------------------------------------------------------
for i, (x, y, w) in enumerate([(252,430,5),(300,290,6),(672,240,5),(822,480,6),
                               (226,520,5),(830,330,5),(380,240,5)]):
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#C4A0B4", opacity=35, stroke=NONE)

# --- captions -------------------------------------------------------------------------
d.text("CARPET JURISDICTION", "Name", x=500, y=930, size=54,
       font="Virelai Sans", color="#F0E2D4", justify="center")
r = d.text("ON THE SOFT SIDE OF THE STRIP", "Role", x=500, y=968,
           size=23, font="Virelai Sans", color="#C2A0B2",
           justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("293.carpet-jurisdiction-V1R00")
