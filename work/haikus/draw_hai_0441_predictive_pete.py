#!/usr/bin/env python3
"""HAI-0441 Predictive Pete — haiku plate V1R00. Predictive policing made
visual: a child silhouette standing inside the patrol loop that draws
itself, a permanent record card pinned to their back, a firework burst
mislabeled as gunfire at midnight. Circular logic armed, cold slate ink,
one red flag. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("HAI-0441 Predictive Pete — Haiku Plate", 1000, 1000)

INK = "#241E18"
RED = "#C8503E"
CREAM = "#E8E4D8"
SOFT = "#9FB4CC"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#141A24"}, {"offset": 1, "color": "#080B10"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#3E5068"}, {"offset": 0.7, "color": "#243244"},
    {"offset": 1, "color": "#101822"}]}}
LOOP_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7E96B4"}, {"offset": 1, "color": "#42566E"}]}}
CARD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#D8D2C0"}, {"offset": 1, "color": "#A8A08A"}]}}
FIG = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5E7086"}, {"offset": 1, "color": "#2E3C4E"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#4E6480", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D0DCE8", strokeWidth=3, opacity=40)
# cold pool under the map light
d.shape("ellipse", "Cold pool", x=290, y=300, width=420, height=420,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#7E96B4", "opacity": 0.22},
            {"offset": 1, "color": "#7E96B4", "opacity": 0}]}},
        stroke=NONE)

# --- the map: faint city grid drawn before the line ----------------------------
for i, x in enumerate(range(200, 801, 100)):
    d.path(f"M{x},140 L{x},800", f"Grid V {i+1}", fill=NONE,
           stroke="#5E7086", strokeWidth=1.5, opacity=22)
for i, y in enumerate(range(160, 801, 110)):
    d.path(f"M160,{y} L840,{y}", f"Grid H {i+1}", fill=NONE,
           stroke="#5E7086", strokeWidth=1.5, opacity=22)

# --- the loop is the law: a patrol circle that closes on itself ------------------
# thick translucent ring, then the spine, then the arrowhead
RING = "M500,300 A170,170 0 1 1 336,560"
d.path(RING, "Loop glow", fill=NONE, stroke="#7E96B4", strokeWidth=26,
       opacity=18, cap="round")
d.path(RING, "Loop band", fill=NONE, stroke=LOOP_GRAD, strokeWidth=14,
       opacity=85, cap="round")
d.path(RING, "Loop spine", fill=NONE, stroke="#D0DCE8", strokeWidth=4,
       opacity=60, cap="round", dash=[14, 10])
# arrowhead where the loop rejoins — the chase never ends
d.path("M328,540 L372,560 L340,596 Z", "Loop arrow", fill=LOOP_GRAD,
       stroke=INK, strokeWidth=3, join="round")
# the pin the loop answers to — patrol starts here
d.shape("ellipse", "Patrol pin", x=486, y=252, width=28, height=28,
        fill=RED, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Pin core", x=496, y=262, width=8, height=8,
        fill="#F0D8D0", stroke=NONE)
d.text("patrol", "Pin label", x=500, y=236, size=13,
       font="Virelai Sans", color=SOFT, justify="center")
# orbit markers — beats logged around the ring
for i, (bx, by) in enumerate([(640,380),(655,545),(500,640),(360,640)]):
    d.shape("ellipse", f"Beat {i+1}", x=bx - 4, y=by - 4, width=8, height=8,
            fill="#D0DCE8", opacity=55, stroke=NONE)

# --- the predicted zone: the map draws the line ------------------------------------
d.shape("ellipse", "Zone outer", x=620, y=200, width=200, height=200,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#C8503E", "opacity": 0.30},
            {"offset": 1, "color": "#C8503E", "opacity": 0.06}]}},
        stroke=RED, strokeWidth=3, dash=[10, 8])
d.shape("ellipse", "Zone core", x=682, y=262, width=76, height=76,
        fill=NONE, stroke=RED, strokeWidth=2.5, opacity=70)
d.path("M720,228 L720,246 M720,354 L720,372 M646,300 L664,300 "
       "M776,300 L794,300", "Zone ticks", fill=NONE, stroke=RED,
       strokeWidth=2.5, opacity=75, cap="round")
d.shape("rectangle", "Zone chip", x=650, y=412, width=140, height=40,
        radius=8, fill="#1A2230", stroke=RED, strokeWidth=2.5)
d.text("predicted zone", "Zone label", x=720, y=438, size=14,
       font="Virelai Sans", color="#E8C8C0", justify="center")

# --- the record card: pinned, permanent ------------------------------------------
CARD_IDS = []
r = d.shape("rectangle", "Record card", x=600, y=560, width=170, height=104,
            radius=8, fill=CARD, stroke=INK, strokeWidth=4)
CARD_IDS.append((r or {}).get("id"))
d.path("M616,594 L754,594", "Card rule 1", fill=NONE, stroke="#6A6250",
       strokeWidth=3, opacity=70)
d.path("M616,620 L730,620", "Card rule 2", fill=NONE, stroke="#6A6250",
       strokeWidth=3, opacity=70)
d.text("GANG DB", "Card title", x=685, y=588, size=15,
       font="Virelai Sans", color="#3A352A", justify="center")
d.text("never clears", "Card note", x=685, y=648, size=13,
       font="Virelai Sans", color=RED, justify="center")
# pin through the card into the loop
d.shape("ellipse", "Card pin", x=678, y=548, width=16, height=16,
        fill=RED, stroke=INK, strokeWidth=3)
# chain from the card to the child's shoulder
d.path("M600,606 C560,620 540,636 528,660", "Card chain", fill=NONE,
       stroke="#8A94A2", strokeWidth=3.5, dash=[5, 5], cap="round",
       opacity=85)

# --- the child: small silhouette, backpack, shadow cast long ---------------------
# long institutional shadow toward lower right
d.path("M492,806 C540,820 600,836 660,848 C600,848 540,842 480,828 Z",
       "Long shadow", fill="#080B10", opacity=40, stroke=NONE)
d.shape("ellipse", "Figure shadow", x=430, y=800, width=140, height=20,
        fill="#080B10", opacity=50, stroke=NONE)
# body — hoodie silhouette, head down
d.path("M464,800 C464,748 468,714 478,696 Q502,684 526,696 "
       "C536,714 540,748 540,800 Z",
       "Child body", fill=FIG, stroke=INK, strokeWidth=5)
d.path("M476,716 C472,742 470,770 470,796", "Body sheen", fill=NONE,
       stroke="#D0DCE8", strokeWidth=6, opacity=18, cap="round")
# head bowed — hood up
d.path("M478,690 C478,662 494,650 503,650 C512,650 528,662 528,690 "
       "C528,700 478,700 478,690 Z",
       "Hood", fill=FIG, stroke=INK, strokeWidth=5)
# backpack — the thing that follows into school
d.path("M536,704 C556,710 562,736 558,764 L540,764 C544,740 542,720 536,704 Z",
       "Backpack", fill={"gradient": {"kind": "linear", "stops": [
           {"offset": 0, "color": "#6A5E4E"}, {"offset": 1, "color": "#3E362A"}]}},
       stroke=INK, strokeWidth=4)
d.shape("ellipse", "Pack badge", x=542, y=724, width=12, height=12,
        fill=RED, stroke=INK, strokeWidth=2.5)

# --- the firework: flagged as gunfire ---------------------------------------------
# burst at upper left, listening dot below it
CX, CY = 300, 300
for i in range(12):
    import math
    a = i * math.pi / 6
    x0, y0 = CX + 22 * math.cos(a), CY + 22 * math.sin(a)
    x1, y1 = CX + 58 * math.cos(a), CY + 58 * math.sin(a)
    d.path(f"M{x0:.0f},{y0:.0f} L{x1:.0f},{y1:.0f}", f"Spark {i+1}",
           fill=NONE, stroke="#E8C87A", strokeWidth=4, opacity=80,
           cap="round")
d.shape("ellipse", "Burst core", x=CX - 12, y=CY - 12, width=24, height=24,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#F5E0A0"},
            {"offset": 1, "color": "#C89038"}]}}, stroke=NONE)
# the sensor that heard wrong
d.shape("ellipse", "Sensor", x=306, y=372, width=18, height=18,
        fill="#2E3C4E", stroke="#8A94A2", strokeWidth=3)
d.path("M300,376 C288,368 288,352 300,344", "Sensor wave 1", fill=NONE,
       stroke="#8A94A2", strokeWidth=2.5, cap="round", opacity=80)
d.path("M312,384 C296,376 292,354 306,338", "Sensor wave 2", fill=NONE,
       stroke="#8A94A2", strokeWidth=2.5, cap="round", opacity=60)
# the mislabel chip
d.shape("rectangle", "Flag chip", x=226, y=404, width=190, height=44,
        radius=8, fill="#1A2230", stroke=RED, strokeWidth=3)
d.text("firework → gunfire", "Flag text", x=321, y=431, size=15,
       font="Virelai Sans", color="#E8C8C0", justify="center")
d.path("M321,390 L321,404", "Flag lead", fill=NONE, stroke=RED,
       strokeWidth=2.5, dash=[4, 4])

# --- caption stack: key line over the name -----------------------------------------
r = d.text("THE LOOP IS THE LAW.", "Key line", x=500, y=898, size=22,
           font="Virelai Sans", color=SOFT, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "key tracking", ids=[r["id"]], tracking=300)
d.text("PREDICTIVE PETE", "Name", x=500, y=944, size=56,
       font="Virelai Sans", color=CREAM, justify="center")

d.finish("hai-0441-predictive-pete-V1R00")
