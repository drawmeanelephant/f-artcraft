#!/usr/bin/env python3
"""APH-005 Bricky Goldbricksworth — aphorism plate V1R00. A ceremonial
gold-handled stamp mid-impression of ACKNOWLEDGED on an incident form that
never moves; a leaning mountain of stamped paperwork, one gold-brick
paperweight, and a cobwebbed ACTION tray. Warm dark ink, olive-gold.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("APH-005 Bricky Goldbricksworth — Aphorism Plate", 1000, 1000)

INK = "#2E2010"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#221A0E"}, {"offset": 1, "color": "#0D0904"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#54401C"}, {"offset": 0.7, "color": "#2E2010"},
    {"offset": 1, "color": "#181007"}]}}
PAPER_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#EEE0BE"}, {"offset": 0.65, "color": "#D8C496"},
    {"offset": 1, "color": "#B09A6A"}]}}
GOLD_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E8C860"}, {"offset": 0.55, "color": "#B8862E"},
    {"offset": 1, "color": "#7A5418"}]}}
STAMP_RED = "#A63A2E"
CREAM = "#EEE0BE"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#A87A34", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8CC90", strokeWidth=3, opacity=40)
for i, (x, y, w) in enumerate([(205, 215, 7), (800, 205, 8), (160, 500, 6),
                               (845, 490, 7), (240, 730, 6), (765, 745, 7)]):
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#8A7040", opacity=35, stroke=NONE)
# desk horizon
d.shape("ellipse", "Desktop", x=180, y=630, width=640, height=50,
        fill="#3A2A14", opacity=80, stroke=INK, strokeWidth=3)
d.shape("ellipse", "Desk sheen", x=250, y=636, width=500, height=14,
        fill="#6E5226", opacity=45, stroke=NONE)

# --- the paperwork mountain (left) -------------------------------------------
# a leaning stack of already-stamped sheets
sheets = [(272, 632, -5), (266, 606, 3), (270, 580, -3), (264, 554, 4),
          (268, 528, -4), (262, 502, 5), (266, 476, -3), (260, 450, 6)]
for i, (sx, sy, srot) in enumerate(sheets):
    d.path(rot_rect_path(sx, sy, 150, 20, srot), f"Pile sheet {i+1}",
           fill=PAPER_GRAD, stroke=INK, strokeWidth=2, opacity=95)
# the top sheet shows its stamp — every one of them acknowledged, none moved
d.path(rot_rect_path(258, 428, 140, 52, 6), "Pile top sheet",
       fill=PAPER_GRAD, stroke=INK, strokeWidth=2.5)
d.shape("ellipse", "Pile stamp", x=296, y=410, width=62, height=30,
        fill=NONE, stroke=STAMP_RED, strokeWidth=3, opacity=60)
# a gold brick keeps the pile down — literally goldbricking
d.path("M212,398 L262,388 L310,398 L300,424 L222,424 Z", "Gold brick",
       fill=GOLD_GRAD, stroke=INK, strokeWidth=3)
d.path("M226,402 L296,402", "Brick sheen", fill=NONE, stroke="#F4E4A0",
       strokeWidth=3, opacity=70, cap="round")
d.text("AU", "Brick mark", x=258, y=417, size=11,
       font="Virelai Sans", color="#6E4A12", justify="center")

# --- the trays (right): ACTION cobwebbed, PENDING stuffed ---------------------
def tray(cx, cy, label, tag=True):
    # wire tray: base rail + side rails, open front
    d.path(f"M{cx},{cy} L{cx + 150},{cy} L{cx + 140},{cy + 44} "
           f"L{cx + 10},{cy + 44} Z", f"{label} tray", fill="#241A0E",
           opacity=70, stroke="#8A7040", strokeWidth=3, join="round")
    for k in range(3):
        ry = cy + 10 + k * 12
        d.path(f"M{cx + 4},{ry} L{cx + 146},{ry}", f"{label} rail {k+1}",
               fill=NONE, stroke="#8A7040", strokeWidth=2, opacity=70)
    if tag:
        d.text(label, f"{label} tag", x=cx + 75, y=cy + 58, size=12,
               font="Virelai Sans", color="#C9A868", justify="center")

tray(660, 470, "ACTION", tag=False)
# cobweb across the empty ACTION tray: radials + sagging arcs
for ang in [-64, -38, -12, 14]:
    a = math.radians(ang)
    d.path(f"M668,478 L{668 + math.cos(a) * 66:.0f},{478 + math.sin(a) * 66:.0f}",
           f"Web spoke {ang}", fill=NONE, stroke=CREAM, strokeWidth=1.5,
           opacity=45)
d.path("M688,474 Q706,486 726,480", "Web arc 1", fill=NONE, stroke=CREAM,
       strokeWidth=2, opacity=55)
d.path("M700,490 Q716,499 733,494", "Web arc 2", fill=NONE, stroke=CREAM,
       strokeWidth=2, opacity=45)
# PENDING overflows — sheets tucked behind the tray front
for i, (px, prot) in enumerate([(690, -8), (740, 4), (712, 12)]):
    d.path(rot_rect_path(px, 556, 60, 78, prot), f"Pending sheet {i+1}",
           fill=PAPER_GRAD, stroke=INK, strokeWidth=2, opacity=95)
tray(660, 570, "PENDING")
# ACTION label inside the empty tray — nothing in it but the name
d.text("ACTION", "ACTION tag", x=735, y=502, size=12,
       font="Virelai Sans", color="#C9A868", justify="center")

# --- the form + ceremonial stamp -----------------------------------------------
d.shape("rectangle", "Form shadow", x=368, y=448, width=280, height=200,
        radius=4, fill="#000000", opacity=35, stroke=NONE)
d.shape("rectangle", "Incident form", x=360, y=440, width=280, height=205,
        radius=4, fill=PAPER_GRAD, stroke=INK, strokeWidth=4)
d.text("ROOT CAUSE:", "Field label", x=372, y=508, size=13,
       font="Virelai Sans", color=INK, justify="left")
d.shape("rectangle", "Field box", x=372, y=518, width=256, height=56,
        fill=NONE, stroke=INK, strokeWidth=2, opacity=75)
# the ACKNOWLEDGED impression, mid-stamp
d.shape("ellipse", "Impression ghost", x=422, y=524, width=168, height=58,
        fill=NONE, stroke=STAMP_RED, strokeWidth=4, opacity=25)
d.shape("ellipse", "Impression ring", x=416, y=518, width=168, height=58,
        fill=NONE, stroke=STAMP_RED, strokeWidth=5, opacity=80)
r = d.text("ACKNOWLEDGED", "Impression text", x=500, y=556, size=15,
           font="Virelai Sans", color=STAMP_RED, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "impression tracking", ids=[r["id"]], tracking=30)
# the checkbox that never gets ticked
d.shape("rectangle", "Action checkbox", x=374, y=596, width=14, height=14,
        fill=NONE, stroke=INK, strokeWidth=2)
d.text("ACTION TAKEN", "Checkbox label", x=396, y=608, size=11,
       font="Virelai Sans", color=INK, justify="left")
# title lives at the foot of the form, the only place the stamp never reaches
d.text("INCIDENT REPORT — FORM 00-B", "Form footer", x=500, y=634, size=11,
       font="Virelai Sans", color=INK, justify="center")

# ceremonial stamp: brass grip, descending onto the field
for i, (mx, mh) in enumerate([(455, 26), (545, 26), (470, 18), (530, 18)]):
    d.path(f"M{mx},{238 - mh} L{mx},238", f"Stamp motion {i+1}", fill=NONE,
           stroke=CREAM, strokeWidth=3.5, opacity=55, cap="round")
d.shape("ellipse", "Stamp grip", x=456, y=252, width=88, height=44,
        fill=GOLD_GRAD, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Grip sheen", x=472, y=258, width=40, height=14,
        fill="#F4E4A0", opacity=60, stroke=NONE)
# grip collar ring — ceremonial flourish
d.shape("ellipse", "Grip collar", x=466, y=286, width=68, height=16,
        fill="#7A5418", stroke=INK, strokeWidth=3)
d.shape("rectangle", "Stamp neck", x=482, y=298, width=36, height=22,
        fill="#8A6220", stroke=INK, strokeWidth=3)
d.shape("rectangle", "Stamp stem", x=490, y=340, width=20, height=104,
        fill=GOLD_GRAD, stroke=INK, strokeWidth=3)
d.shape("rectangle", "Stamp collar", x=452, y=440, width=96, height=18,
        radius=3, fill="#B8862E", stroke=INK, strokeWidth=3)
d.shape("rectangle", "Stamp base", x=444, y=456, width=112, height=34,
        radius=4, fill="#7E2B22", stroke=INK, strokeWidth=4)
d.shape("rectangle", "Base sheen", x=450, y=460, width=100, height=10,
        fill="#B8543E", opacity=55, stroke=NONE)

# --- aphorism line + name + role --------------------------------------------------
r = d.text("ACKNOWLEDGMENT IS NOT ACTION,", "Key line 1", x=500, y=712,
           size=22, font="Virelai Sans", color="#E8CC90", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "key1 tracking", ids=[r["id"]], tracking=100)
r = d.text("BUT IT DOES PRODUCE PAPERWORK.", "Key line 2", x=500, y=746,
           size=22, font="Virelai Sans", color="#E8CC90", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "key2 tracking", ids=[r["id"]], tracking=100)

d.text("BRICKY GOLDBRICKSWORTH", "Name", x=500, y=905, size=52,
       font="Virelai Sans", color=CREAM, justify="center")
r = d.text("ACKNOWLEDGMENT IS NOT ACTION", "Role", x=500, y=950, size=18,
           font="Virelai Sans", color="#C9A868", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=160)

d.finish("aph-005-bricky-goldbricksworth-V1R00")
