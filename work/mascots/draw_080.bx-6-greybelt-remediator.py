#!/usr/bin/env python3
"""BX-6 Greybelt Remediator — mascot portrait V1R00.
A stout clerk-ghost on a dashboard, both hands in the chart stretching the
shaded deviation band wider around a perfectly straight baseline — remediating
the graph, not the system. 1000x1000 plate format.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("BX-6 Greybelt Remediator — Mascot Portrait", 1000, 1000)

INK = "#2E3230"
BG_GRAD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000], "stops": [
    {"offset": 0, "color": "#141B20"}, {"offset": 1, "color": "#05080B"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#DCE4DE"}, {"offset": 0.65, "color": "#ACBCB2"},
    {"offset": 1, "color": "#78907F"}]}}
PANEL_GRAD = {"gradient": {"kind": "linear", "start": [0, 140], "end": [0, 450], "stops": [
    {"offset": 0, "color": "#1E2C38"}, {"offset": 1, "color": "#121D28"}]}}
ROBE_GRAD = {"gradient": {"kind": "linear", "start": [0, 460], "end": [0, 780], "stops": [
    {"offset": 0, "color": "#9CBCAC"}, {"offset": 0.6, "color": "#6E8E7E"},
    {"offset": 1, "color": "#4A6456"}]}}

PCX, PCY, PR = 500, 460, 420
def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#A8C0B2", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#37493F", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8F0EA", strokeWidth=3, opacity=38)
d.shape("ellipse", "Patina 1", x=200, y=600, width=240, height=130,
        fill="#88A292", opacity=16, stroke=NONE)
d.shape("ellipse", "Patina 2", x=590, y=520, width=210, height=120,
        fill="#88A292", opacity=14, stroke=NONE)
for i, (x, y, w) in enumerate([(175, 340, 6), (835, 330, 7), (160, 540, 7), (848, 550, 6),
                               (260, 775, 6), (730, 765, 7), (310, 125, 5), (680, 120, 6)]):
    assert on_disc(x, y, 12), (x, y)
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#5E7A6C", opacity=32, stroke=NONE)
for i, (x, y, w) in enumerate([(65, 130, 4), (925, 100, 5), (48, 550, 4), (948, 610, 4),
                               (125, 895, 4), (875, 905, 5), (510, 28, 4), (250, 40, 3)]):
    d.shape("ellipse", f"Dust {i+1}", x=x, y=y, width=w, height=w,
            fill="#D2E0D8", opacity=26, stroke=NONE)

# --- dashboard panel (corners kept inside the disc) ---------------------------------
d.shape("rectangle", "Panel", x=240, y=155, width=520, height=295, radius=20,
        fill=PANEL_GRAD, stroke="#3A5262", strokeWidth=5)
# title bar strip + window dots
d.path("M240,197 L760,197", "Title seam", fill=NONE, stroke="#3A5262",
       strokeWidth=3, opacity=80)
for i, x in enumerate((264, 288, 312)):
    d.shape("ellipse", f"Win dot {i+1}", x=x, y=170, width=12, height=12,
            fill="#5E7A8C", opacity=80, stroke=NONE)
# faint gridlines inside the chart area
for i, y in enumerate((230, 350, 400)):
    d.path(f"M265,{y} L735,{y}", f"Grid {i+1}", fill=NONE,
           stroke="#3A5262", strokeWidth=2, opacity=45)
# y-axis ticks
for i, y in enumerate((230, 290, 350, 400)):
    d.path(f"M265,{y} L279,{y}", f"Axis tick {i+1}", fill=NONE,
           stroke="#5E7A8C", strokeWidth=3, opacity=70, cap="round")

# --- the greybelt: shaded deviation band, stretched wide in the middle -------------
# former narrow belt — dashed ghost inside the widened band
d.path("M280,268 L395,262 M605,262 L720,268", "Old belt top", fill=NONE,
       stroke="#8A94A0", strokeWidth=3, dash=[7, 7], opacity=55, cap="round")
d.path("M280,312 L395,318 M605,318 L720,312", "Old belt bottom", fill=NONE,
       stroke="#8A94A0", strokeWidth=3, dash=[7, 7], opacity=55, cap="round")
# the widened band itself: narrow at the ends, swelling where the hands pull it
d.path("M270,262 L400,256 C438,196 562,196 600,256 L730,262 "
       "L730,318 L600,324 C562,384 438,384 400,324 L270,318 Z",
       "Greybelt", fill="#7E8890", opacity=50, stroke="#5E6A72",
       strokeWidth=3)
# band shading: darker at the pulled edges, sheen across the bulge
d.path("M410,262 C445,208 555,208 590,262 C555,246 445,246 410,262 Z",
       "Belt top shade", fill="#4A545C", opacity=45, stroke=NONE)
d.path("M410,318 C445,374 555,374 590,318 C555,334 445,334 410,318 Z",
       "Belt bottom shade", fill="#4A545C", opacity=45, stroke=NONE)
d.shape("ellipse", "Belt sheen", x=440, y=230, width=120, height=34,
        fill="#C6D0D6", opacity=22, stroke=NONE)
# the baseline, unbothered, straight through everything
d.path("M270,290 L730,290", "Baseline", fill=NONE, stroke="#E4ECE6",
       strokeWidth=7, cap="round")

# --- the remediator: stout clerk-ghost under the bulge ------------------------------
d.shape("ellipse", "Shadow", x=370, y=776, width=260, height=26,
        fill="#1E2E28", opacity=22, stroke=NONE)
d.path("M390,752 C378,640 390,560 424,505 C446,470 554,470 576,505 "
       "C610,560 622,640 610,752 C582,774 546,780 500,780 "
       "C454,780 418,774 390,752 Z",
       "Robe", fill=ROBE_GRAD, stroke=INK, strokeWidth=6)
d.path("M442,580 C436,636 434,700 440,752", "Fold L", fill=NONE,
       stroke="#3E584C", strokeWidth=4, opacity=55, cap="round")
d.path("M558,580 C564,636 566,700 560,752", "Fold R", fill=NONE,
       stroke="#3E584C", strokeWidth=4, opacity=55, cap="round")
d.shape("ellipse", "Dome light", x=426, y=488, width=130, height=48,
        fill="#FFFFFF", opacity=15, stroke=NONE)
# arms raised in a V, mitts planted on the band's swollen lower edge
d.path("M438,540 C420,480 414,420 424,368", "Arm L", fill=NONE,
       stroke="#6E8E7E", strokeWidth=30, cap="round")
d.path("M562,540 C580,480 586,420 576,368", "Arm R", fill=NONE,
       stroke="#6E8E7E", strokeWidth=30, cap="round")
d.shape("ellipse", "Hand L", x=402, y=342, width=46, height=38,
        fill="#BCD0C2", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Hand R", x=552, y=342, width=46, height=38,
        fill="#BCD0C2", stroke=INK, strokeWidth=4)
# little stretch ticks where the band is being pulled
for i, (x, y, dx, dy) in enumerate([(398, 330, -16, -12), (384, 352, -22, 0),
                                    (600, 330, 16, -12), (614, 352, 22, 0)]):
    d.path(f"M{x},{y} L{x+dx},{y+dy}", f"Stretch tick {i+1}", fill=NONE,
           stroke="#E4ECE6", strokeWidth=4, opacity=80, cap="round")
# face: deadpan determination
d.shape("ellipse", "Eye L", x=444, y=540, width=36, height=44,
        fill="#FFFFFF", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Eye R", x=520, y=540, width=36, height=44,
        fill="#FFFFFF", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Pupil L", x=455, y=550, width=15, height=20,
        fill="#1E241F", stroke=NONE)
d.shape("ellipse", "Pupil R", x=531, y=550, width=15, height=20,
        fill="#1E241F", stroke=NONE)
d.shape("ellipse", "Glint L", x=458, y=554, width=6, height=6,
        fill="#FFFFFF", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=534, y=554, width=6, height=6,
        fill="#FFFFFF", opacity=90, stroke=NONE)
d.path("M442,540 L482,530", "Brow L", fill=NONE, stroke=INK,
       strokeWidth=7, cap="round")
d.path("M518,530 L558,540", "Brow R", fill=NONE, stroke=INK,
       strokeWidth=7, cap="round")
d.path("M482,612 L518,612", "Mouth", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
# collar tabs
d.path("M468,640 L500,664 L468,676 Z", "Collar L", fill="#F4EEE0",
       stroke=INK, strokeWidth=3)
d.path("M532,640 L500,664 L532,676 Z", "Collar R", fill="#F4EEE0",
       stroke=INK, strokeWidth=3)

# --- name + role ------------------------------------------------------------------
def text_id(text):
    # point-type nodes are named after their content, not the layer label
    doc = d.call("inspect_document", {"kind": "Type"}, "inspect type") or {}
    for nd in doc.get("nodes", []):
        if nd.get("name") == text:
            return nd["id"]
    return None

FALLBACK = set("0123456789Λ/™")
def digit_font(tid, text):
    b = 0
    for ch in text:
        n = len(ch.encode("utf-8"))
        if ch in FALLBACK:
            d.cmd("text.setStyle", f"fallback {ch}@{b}",
                  id=tid, font="Source Sans 3", start=b, end=b + n)
        b += n

NAME = "BX-6 GREYBELT REMEDIATOR"
d.text(NAME, "Name", x=500, y=930, size=50, font="Virelai Sans",
       color="#E2EAE4", justify="center")
tid = text_id(NAME)
if tid:
    digit_font(tid, NAME)

ROLE = "REMEDIATES GRAPHS NOT SYSTEMS"
d.text(ROLE, "Role", x=500, y=968, size=23,
       font="Virelai Sans", color="#96B0A2", justify="center")
rid = text_id(ROLE)
if rid:
    d.cmd("text.setStyle", "role tracking", id=rid, tracking=280)

d.finish("080.bx-6-greybelt-remediator-V1R00")
