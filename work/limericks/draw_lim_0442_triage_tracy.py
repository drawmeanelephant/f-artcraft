#!/usr/bin/env python3
"""LIM-0442 Triage Tracy — limerick plate V1R00. Profit over survival:
a balance where the coin pan outweights the heart pan, a triage terminal
sorting patients by margin, an EKG that decays into a downward slope,
and the care criteria clipboard — cited everywhere, written by nobody.
Clinical teal palette, warm dark ink. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Digits set in Source Sans 3 — Virelai Sans carries no figures."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("LIM-0442 Triage Tracy — Limerick Plate", 1000, 1000)

INK = "#18201C"
CREAM = "#ECE8D4"
TAN = "#A8AE9C"
RED = "#C04434"
PHOS = "#9BD4B4"
GOLD = "#D8AC54"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#111917"}, {"offset": 1, "color": "#070C0A"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4E5C54"}, {"offset": 0.7, "color": "#2C3833"},
    {"offset": 1, "color": "#151C19"}]}}
STEEL = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5A645E"}, {"offset": 1, "color": "#2E3630"}]}}
SCREEN = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#1E2E26"}, {"offset": 1, "color": "#0C140F"}]}}
PAPER = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E8E2CE"}, {"offset": 1, "color": "#C2B896"}]}}
GLOW = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#9BD4B4", "opacity": 0.35},
    {"offset": 1, "color": "#9BD4B4", "opacity": 0}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#64705F", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E0E4CC", strokeWidth=3, opacity=45)
for i, (x, y, w) in enumerate([(185, 215, 8), (805, 225, 7), (150, 520, 9),
                               (855, 570, 8), (245, 745, 7), (735, 735, 8),
                               (128, 390, 6), (868, 410, 7), (340, 135, 7),
                               (660, 140, 8)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#3E4A40", opacity=40, stroke=NONE)

# --- the margin scale: coin pan outweighs the heart pan ------------------------------
# fulcrum
d.path("M500,168 L478,222 L522,222 Z", "Fulcrum", fill=STEEL,
       stroke=INK, strokeWidth=4, join="round")
# beam, tilted — right (margin) side heavy
d.path("M385,180 L615,225", "Beam", fill=NONE, stroke=INK,
       strokeWidth=7, cap="round")
d.shape("ellipse", "Beam pivot", x=492, y=196, width=16, height=16,
        fill=GOLD, stroke=INK, strokeWidth=3)
# left pan: the heart, up in the air
d.path("M385,180 L362,240 M385,180 L408,240", "Heart pan strings",
       fill=NONE, stroke=INK, strokeWidth=2.5, opacity=80)
d.path("M362,240 L408,240 L385,262 Z", "Heart pan", fill=STEEL,
       stroke=INK, strokeWidth=3, join="round")
d.path("M385,206 C385,196 371,194 367,203 C363,212 372,220 385,230 "
       "C398,220 407,212 403,203 C399,194 385,196 385,206 Z",
       "Heart", fill=RED, stroke=INK, strokeWidth=3)
# right pan: the margin, sinking
d.path("M615,225 L592,290 M615,225 L638,290", "Coin pan strings",
       fill=NONE, stroke=INK, strokeWidth=2.5, opacity=80)
d.path("M592,290 L638,290 L615,314 Z", "Coin pan", fill=STEEL,
       stroke=INK, strokeWidth=3, join="round")
for i, cy in enumerate([252, 264, 276]):
    d.shape("ellipse", f"Coin {i+1}", x=600, y=cy, width=30, height=12,
            fill=GOLD, stroke=INK, strokeWidth=2.5)

# --- the triage terminal -------------------------------------------------------------
d.shape("rectangle", "Terminal body", x=330, y=330, width=340, height=290,
        radius=14, fill=STEEL, stroke=INK, strokeWidth=5)
d.shape("rectangle", "Screen", x=350, y=352, width=300, height=214,
        radius=6, fill=SCREEN, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Screen glow", x=380, y=370, width=240, height=90,
        fill=GLOW, stroke=NONE)
# terminal stand
d.path("M470,620 L530,620 L540,668 L460,668 Z", "Stand", fill=STEEL,
       stroke=INK, strokeWidth=4, join="round")
d.shape("ellipse", "Stand foot", x=430, y=664, width=140, height=18,
        fill=STEEL, stroke=INK, strokeWidth=4)
# queue header
d.text("TRIAGE QUEUE — BY MARGIN", "Queue head", x=500, y=382, size=13,
       font="Virelai Sans", color=PHOS, justify="center")
d.path("M370,392 L630,392", "Queue rule", fill=NONE, stroke=PHOS,
       strokeWidth=1.5, opacity=50)
# queue rows — patient numbers in Source Sans 3, verdicts in Virelai
rows = [("PT-0114", "TREAT", "#9BD4B4", 416),
        ("PT-0207", "WAIT", "#C9BC86", 452),
        ("PT-0331", "DECAY", RED, 488)]
for i, (pt, verdict, vc, ry) in enumerate(rows):
    d.text(pt, f"Row {i+1} id", x=395, y=ry, size=14,
           font="Source Sans 3", color="#8FA898", justify="left")
    d.text(verdict, f"Row {i+1} verdict", x=605, y=ry, size=14,
           font="Virelai Sans", color=vc, justify="right")
    d.path(f"M380,{ry + 12} L620,{ry + 12}", f"Row {i+1} sep", fill=NONE,
           stroke=PHOS, strokeWidth=1, opacity=25)
# margin column header, right-aligned over the verdicts
d.text("OUTCOME", "Outcome col", x=605, y=402, size=9,
       font="Virelai Sans", color="#6E8274", justify="right")
d.text("UNIT", "Unit col", x=395, y=402, size=9,
       font="Virelai Sans", color="#6E8274", justify="left")
# the EKG strip: heartbeat, then the margin line runs away downhill
d.path("M360,540 L420,540 L432,516 L446,566 L458,540 L510,540",
       "EKG beat", fill=NONE, stroke=PHOS, strokeWidth=3, cap="round",
       join="round")
d.path("M510,540 L545,548 L580,544 L618,556", "EKG decay slope",
       fill=NONE, stroke=RED, strokeWidth=3, cap="round", join="round")
d.path("M612,549 L626,558 L610,560 Z", "Slope arrowhead", fill=RED,
       stroke=NONE)
# DECAY stamp across the screen corner
stamp_ids = []
for res in [
    d.shape("rectangle", "Decay stamp", x=532, y=500, width=112, height=36,
            radius=4, fill=NONE, stroke=RED, strokeWidth=4),
    d.text("DECAY", "Decay word", x=588, y=525, size=20,
           font="Virelai Sans", color=RED, justify="center"),
]:
    if res and res.get("id"):
        stamp_ids.append(res["id"])
if stamp_ids:
    d.call("transform", {"ids": stamp_ids, "rotate": -10,
                         "origin": [588, 518]}, "tilt stamp")

# --- the care criteria: cited by nobody, written by nobody -----------------------------
d.shape("rectangle", "Clipboard", x=205, y=548, width=172, height=195,
        radius=8, fill={"gradient": {"kind": "linear", "stops": [
            {"offset": 0, "color": "#5C4A38"},
            {"offset": 1, "color": "#382C20"}]}},
        stroke=INK, strokeWidth=5)
d.shape("rectangle", "Criteria page", x=220, y=563, width=142, height=162,
        radius=3, fill=PAPER, stroke=INK, strokeWidth=3)
d.shape("rectangle", "Clip", x=248, y=540, width=56, height=22,
        radius=8, fill=GOLD, stroke=INK, strokeWidth=3)
d.text("CARE CRITERIA", "Form header", x=291, y=589, size=12,
       font="Virelai Sans", color=INK, justify="center")
d.path("M230,597 L352,597", "Form head rule", fill=NONE, stroke=INK,
       strokeWidth=2, opacity=60)
# ruled lines — all of them blank
for i, ly in enumerate([613, 631, 649, 667, 685, 703]):
    d.path(f"M230,{ly} L352,{ly}", f"Blank line {i+1}", fill=NONE,
           stroke="#8A8070", strokeWidth=1.5, opacity=55,
           dash=[4, 3])
d.text("(nothing written)", "Form footnote", x=291, y=717, size=9,
       font="Virelai Sans", color="#8A8070", justify="center")
# faint red CITED stamp on the blank page
cite_ids = []
for res in [
    d.shape("rectangle", "Cited frame", x=243, y=625, width=96, height=32,
            radius=4, fill=NONE, stroke=RED, strokeWidth=3, opacity=75),
    d.text("CITED", "Cited word", x=291, y=647, size=15,
           font="Virelai Sans", color=RED, justify="center"),
]:
    if res and res.get("id"):
        cite_ids.append(res["id"])
if cite_ids:
    d.call("transform", {"ids": cite_ids, "rotate": -8,
                         "origin": [291, 641]}, "tilt cited")

# --- key line + name + role ---------------------------------------------------------
r = d.text("DECIDE WHO GETS TO DECAY.", "Key line", x=500, y=800,
           size=22, font="Virelai Sans", color=CREAM, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "key line tracking", ids=[r["id"]], tracking=70)
d.text("TRIAGE TRACY", "Name", x=500, y=930, size=58,
       font="Virelai Sans", color=CREAM, justify="center")
r = d.text("PROFIT OVER SURVIVAL", "Role", x=500, y=967, size=20,
           font="Virelai Sans", color=TAN, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=190)

d.finish("lim-0442-triage-tracy-V1R00")
