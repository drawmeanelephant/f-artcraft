#!/usr/bin/env python3
"""HAI-0440 Score Sam — haiku plate V1R00. Mathematical redlining made
visual: a small figure dwarfed by three glowing digits on the scoreboard,
the hidden formula behind a parted curtain, the appeal path dead-ending
at a bricked door. Warm dark ink, amber ledger light. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Virelai Sans has no digit glyphs — digits set in Source Sans 3."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("HAI-0440 Score Sam — Haiku Plate", 1000, 1000)

INK = "#2E1F14"
AMBER = "#F0B64A"
CREAM = "#F2E4C6"
SOFT = "#C9AE86"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1C130C"}, {"offset": 1, "color": "#0B0705"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4E3B26"}, {"offset": 0.7, "color": "#2C2013"},
    {"offset": 1, "color": "#150E08"}]}}
CURTAIN = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6A2A34"}, {"offset": 0.6, "color": "#461C26"},
    {"offset": 1, "color": "#2A1016"}]}}
PANEL = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#241A10"}, {"offset": 1, "color": "#120C07"}]}}
FIG = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#8A7458"}, {"offset": 1, "color": "#4A3A28"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#6E5638", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8D8B8", strokeWidth=3, opacity=40)
# amber pool glowing out of the scoreboard
d.shape("ellipse", "Amber pool", x=280, y=300, width=440, height=400,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#F0B64A", "opacity": 0.20},
            {"offset": 1, "color": "#F0B64A", "opacity": 0}]}},
        stroke=NONE)
# dust motes in the beam
for i, (x, y, w) in enumerate([(290,420,7),(700,400,6),(240,560,8),
                               (770,580,7),(340,240,6),(660,220,7),
                               (200,660,6),(820,680,7),(450,130,5)]):
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#E8D8B8", opacity=18, stroke=NONE)

# --- the black box: a curtained window hiding the formula -----------------------
# arched frame, opening glowing with the formula inside
d.path("M380,410 L380,240 C380,178 620,178 620,240 L620,410 Z",
       "Window frame", fill="#1E140C", stroke=INK, strokeWidth=6)
d.path("M398,394 L398,246 C398,198 602,198 602,246 L602,394 Z",
       "Window opening", fill={"gradient": {"kind": "linear", "stops": [
           {"offset": 0, "color": "#F5D98E", "opacity": 0.75},
           {"offset": 1, "color": "#C98F3A", "opacity": 0.45}]}},
       stroke="#8A6A34", strokeWidth=3)
# the formula fragment, half-hidden — the model stays silent
d.text("f(x) = w · x + b", "Formula", x=500, y=250, size=15,
       font="Source Sans 3", color="#3A2A14", justify="center")
d.path("M462,290 L538,290 M462,318 L528,318", "Weight bars", fill=NONE,
       stroke="#6A4A22", strokeWidth=4, opacity=65, cap="round",
       dash=[9, 7])
d.text("w = ?", "Hidden weight", x=500, y=342, size=19,
       font="Source Sans 3", color="#3A2A14", justify="center")
# curtain rod + finials
d.path("M364,186 L636,186", "Curtain rod", fill=NONE, stroke="#8A6A34",
       strokeWidth=7, cap="round")
for i, x in enumerate([364, 636]):
    d.shape("ellipse", f"Finial {i+1}", x=x - 8, y=178, width=16, height=16,
            fill="#8A6A34", stroke=INK, strokeWidth=2.5)
# the parted drapes inside the opening
d.path("M398,206 C436,214 458,230 464,252 C468,300 462,350 448,394 "
       "L398,394 Z",
       "Drape L", fill=CURTAIN, stroke=INK, strokeWidth=4, join="round")
d.path("M602,206 C564,214 542,230 536,252 C532,300 538,350 552,394 "
       "L602,394 Z",
       "Drape R", fill=CURTAIN, stroke=INK, strokeWidth=4, join="round")
d.path("M418,220 C432,280 432,340 420,388", "Drape L fold", fill=NONE,
       stroke="#1E0B10", strokeWidth=9, opacity=40, cap="round")
d.path("M582,220 C568,280 568,340 580,388", "Drape R fold", fill=NONE,
       stroke="#1E0B10", strokeWidth=9, opacity=40, cap="round")

# --- the scoreboard: three digits loom over everything --------------------------
d.shape("ellipse", "Board glow", x=330, y=330, width=340, height=220,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#F0B64A", "opacity": 0.35},
            {"offset": 1, "color": "#F0B64A", "opacity": 0}]}},
        stroke=NONE)
d.shape("rectangle", "Scoreboard", x=296, y=350, width=408, height=196,
        radius=16, fill=PANEL, stroke=INK, strokeWidth=6)
d.shape("rectangle", "Board inner rim", x=312, y=366, width=376, height=164,
        radius=10, fill=NONE, stroke="#6A4A22", strokeWidth=2.5,
        opacity=80)
d.text("742", "Score digits", x=500, y=488, size=128,
       font="Source Sans 3", color=AMBER, justify="center")
# digit gleam strip
d.shape("rectangle", "Digit gleam", x=312, y=366, width=376, height=40,
        radius=10, fill={"gradient": {"kind": "linear", "stops": [
            {"offset": 0, "color": "#F5D98E", "opacity": 0.16},
            {"offset": 1, "color": "#F5D98E", "opacity": 0}]}},
        stroke=NONE)
# board feet — it stands over everything
d.path("M360,546 L360,590 M640,546 L640,590", "Board legs", fill=NONE,
       stroke=INK, strokeWidth=10, cap="round")

# --- reason codes: the factor named, the weight never ---------------------------
for i, (x, label) in enumerate([(338, "UTILIZATION  ?"),
                                (500, "HISTORY  ?"),
                                (662, "MIX  ?")]):
    d.shape("rectangle", f"Reason chip {i+1}", x=x - 76, y=610, width=152,
            height=44, radius=8, fill=PANEL, stroke="#6A4A22",
            strokeWidth=3)
    d.text(label, f"Reason {i+1}", x=x, y=638, size=16,
           font="Virelai Sans", color=SOFT, justify="center")

# --- the appeal path: dashed, dead-ending at a bricked door ---------------------
d.path("M560,760 C640,772 706,766 752,738", "Appeal path", fill=NONE,
       stroke=SOFT, strokeWidth=4, dash=[9, 8], cap="round",
       opacity=75)
# door outline, bricked up
d.path("M752,738 L752,650 C752,624 810,624 810,650 L810,738 Z",
       "Appeal door", fill="#1E140C", stroke=INK, strokeWidth=5)
# brick courses — alternating bonds
for i, yy in enumerate(range(652, 732, 16)):
    d.path(f"M754,{yy} L808,{yy}", f"Brick course {i+1}", fill=NONE,
           stroke="#5A4630", strokeWidth=2.5, opacity=85)
    if i < 4:
        off = 12 if i % 2 == 0 else 30
        d.path(f"M{754 + off},{yy} L{754 + off},{yy + 16} "
               f"M{794 - off // 3},{yy} L{794 - off // 3},{yy + 16}",
               f"Brick joints {i+1}", fill=NONE, stroke="#5A4630",
               strokeWidth=2.5, opacity=85)
d.text("appeal", "Appeal label", x=650, y=730, size=14,
       font="Virelai Sans", color=SOFT, justify="center")

# --- the training data: a faint declining distribution, left of the figure ------
for i, (bx, bh) in enumerate([(222, 78), (250, 60), (278, 88),
                              (306, 44), (334, 26)]):
    fill = "#C98F3A" if i == 3 else "#6A4A22"
    d.shape("rectangle", f"Dist bar {i+1}", x=bx, y=752 - bh, width=22,
            height=bh, radius=2, fill=fill, opacity=55 if i == 3 else 35,
            stroke=NONE)
d.path("M214,752 L364,752", "Dist baseline", fill=NONE, stroke="#5A4630",
       strokeWidth=2.5, opacity=70)
d.text("the trained", "Dist label", x=290, y=774, size=12,
       font="Virelai Sans", color="#8A7458", justify="center")

# --- the queue: a faint earlier applicant, scored and gone ------------------------
d.shape("ellipse", "Queued wisp", x=196, y=642, width=28, height=38,
        fill="#8A7458", opacity=12, stroke=NONE)

# --- the person: small, reduced to a number --------------------------------------
d.shape("ellipse", "Figure shadow", x=420, y=822, width=160, height=22,
        fill="#0C0705", opacity=50, stroke=NONE)
# body — a plain hooded silhouette, face turned up at the digits
d.path("M458,822 C458,770 463,732 474,712 Q500,700 526,712 "
       "C537,732 542,770 542,822 Z",
       "Figure body", fill=FIG, stroke=INK, strokeWidth=5)
d.path("M472,734 C468,762 466,792 466,818", "Figure sheen", fill=NONE,
       stroke="#E8D8B8", strokeWidth=6, opacity=20, cap="round")
# head tipped back toward the score
d.shape("ellipse", "Figure head", x=476, y=662, width=48, height=48,
        fill=FIG, stroke=INK, strokeWidth=5)
# the upturned face catches the amber light
d.shape("ellipse", "Face glow", x=487, y=670, width=26, height=18,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#F0B64A", "opacity": 0.45},
            {"offset": 1, "color": "#F0B64A", "opacity": 0}]}},
        stroke=NONE)
# number tag hanging from the neck — the person IS the score
d.path("M490,728 L500,750 L510,728", "Tag string", fill=NONE,
       stroke=INK, strokeWidth=2.5)
d.shape("rectangle", "Number tag", x=476, y=748, width=48, height=32,
        radius=4, fill="#241A10", stroke="#8A6A34", strokeWidth=3)
d.text("742", "Tag digits", x=500, y=771, size=19,
       font="Source Sans 3", color=AMBER, justify="center")

# --- caption stack: key line over the name ----------------------------------------
r = d.text("Three digits decide.", "Key line", x=500, y=898, size=23,
           font="Virelai Sans", color=SOFT, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "key tracking", ids=[r["id"]], tracking=300)
d.text("SCORE SAM", "Name", x=500, y=944, size=56,
       font="Virelai Sans", color=CREAM, justify="center")

d.finish("hai-0440-score-sam-V1R00")
