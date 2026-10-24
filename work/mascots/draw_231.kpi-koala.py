#!/usr/bin/env python3
"""KPI Koala — mascot portrait V1R00.
A grey koala in a clip-on tie, forearms locked around a wall chart:
the trendline flattens politely inside the green band while a red
line droops below it, filed away as local detail. Spreadsheets are
strapped to his back. He naps only inside the band.
1000x1000. Gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("KPI Koala — Mascot Portrait", 1000, 1000)

INK = "#2A2530"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1B1E2E"}, {"offset": 1, "color": "#0A0C16"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#59627E"}, {"offset": 0.7, "color": "#3C435C"},
    {"offset": 1, "color": "#1D2236"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#303A58"}, {"offset": 1, "color": "#141A2C"}]}}
FUR = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#D6D9E2"}, {"offset": 0.72, "color": "#A8ADBE"},
    {"offset": 1, "color": "#7A8098"}]}}
FUR_MID = "#9AA0B4"
FUR_DARK = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#8E94A8"}, {"offset": 1, "color": "#5E6480"}]}}
CARD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F2EDDC"}, {"offset": 1, "color": "#D6CBAE"}]}}
PAPER = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#EFE9D6"}, {"offset": 1, "color": "#CFC5A8"}]}}
NOSE = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4C3C46"}, {"offset": 1, "color": "#221A20"}]}}
TIE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5ED494"}, {"offset": 1, "color": "#2C8C5A"}]}}
GREEN = "#54D488"
RED = "#D4685E"

def rot_pt(cx, cy, x, y, deg):
    t = math.radians(deg); c, s = math.cos(t), math.sin(t)
    dx, dy = x - cx, y - cy
    return cx + dx*c - dy*s, cy + dx*s + dy*c

def rot_line(cx, cy, x1, y1, x2, y2, deg):
    a = rot_pt(cx, cy, x1, y1, deg); b = rot_pt(cx, cy, x2, y2, deg)
    return f"M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#6E7FA6", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C8D4EC", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(196,240,8),(798,236,7),(162,524,9),(832,548,8),
                               (250,762,7),(750,746,9),(136,394,6),(862,396,7),
                               (396,114,7),(610,112,8),(336,820,6),(664,816,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#3E4A68", opacity=45, stroke=NONE)

# --- floor ---------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0A0F1A",
       strokeWidth=4, opacity=70)

# --- spreadsheets strapped to his back -----------------------------------------
# sheet stacks peeking out behind each shoulder, grid cells and all
for side, (cx, cy, deg) in enumerate([(296, 428, -11), (704, 428, 11)]):
    s = "L" if side == 0 else "R"
    d.path(rot_rect_path(cx + 10, cy + 14, 176, 138, deg), f"Sheet {s} back",
           fill="#B9AE90", stroke=NONE)
    d.path(rot_rect_path(cx, cy, 176, 138, deg), f"Sheet {s}",
           fill=PAPER, stroke=INK, strokeWidth=4)
    for j, fx in enumerate((-0.22, 0.12)):
        d.path(rot_line(cx, cy, cx + fx*176, cy - 58, cx + fx*176, cy + 58, deg),
               f"Sheet {s} col {j+1}", fill=NONE, stroke="#9A9074",
               strokeWidth=3, opacity=70)
    for j, fy in enumerate((-0.16, 0.18)):
        d.path(rot_line(cx, cy, cx - 74, cy + fy*138, cx + 74, cy + fy*138, deg),
               f"Sheet {s} row {j+1}", fill=NONE, stroke="#9A9074",
               strokeWidth=3, opacity=70)

# --- koala ----------------------------------------------------------------------
d.shape("ellipse", "Koala shadow", x=340, y=742, width=320, height=36,
        fill="#060A10", opacity=50, stroke=NONE)
# ears first: big grey saucers with pale fluff
for side, (ex, ey) in enumerate([(318, 218), (682, 218)]):
    s = "L" if side == 0 else "R"
    d.shape("ellipse", f"Ear {s}", x=ex - 82, y=ey - 72, width=164, height=150,
            fill=FUR_DARK, stroke=INK, strokeWidth=5)
    for j, (fx, fy, fw) in enumerate([(-66, -20, 26), (-58, 28, 22), (-30, 56, 20),
                                      (30, 56, 20), (58, 28, 22), (66, -20, 26)]):
        d.shape("ellipse", f"Ear {s} tuft {j+1}", x=ex + fx - fw/2, y=ey + fy - fw/2,
                width=fw, height=fw, fill=FUR_DARK, stroke=NONE)
    d.shape("ellipse", f"Ear {s} inner", x=ex - 52, y=ey - 44, width=104, height=96,
            fill="#DADCE4", opacity=90, stroke=NONE)
    d.shape("ellipse", f"Ear {s} shade", x=ex - 40, y=ey - 30, width=80, height=66,
            fill="#B4B8C8", opacity=60, stroke=NONE)
# body behind the chart
d.shape("ellipse", "Body", x=382, y=500, width=236, height=272,
        fill=FUR, stroke=INK, strokeWidth=5)
# feet planted on the floor
d.shape("ellipse", "Foot L", x=384, y=742, width=96, height=44,
        fill=FUR_DARK, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Foot R", x=520, y=742, width=96, height=44,
        fill=FUR_DARK, stroke=INK, strokeWidth=4)
# shoulder straps holding the sheet stacks
d.path("M316,470 C352,502 384,522 414,534", "Strap L", fill=NONE,
       stroke="#3A3244", strokeWidth=15, cap="round")
d.path("M684,470 C648,502 616,522 586,534", "Strap R", fill=NONE,
       stroke="#3A3244", strokeWidth=15, cap="round")
d.shape("ellipse", "Strap L buckle", x=362, y=500, width=16, height=12,
        fill="#C8A24E", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Strap R buckle", x=622, y=500, width=16, height=12,
        fill="#C8A24E", stroke=INK, strokeWidth=3)
# head
d.shape("ellipse", "Head", x=344, y=196, width=312, height=196,
        fill=FUR, stroke=INK, strokeWidth=5)
d.shape("ellipse", "Brow shade", x=380, y=214, width=240, height=60,
        fill="#8A90A4", opacity=28, stroke=NONE)
# face: half-lidded, mid-nap inside the green band
d.path("M406,300 C416,310 438,310 448,300", "Eye L", fill=NONE,
       stroke=INK, strokeWidth=6, cap="round")
d.path("M552,300 C562,310 584,310 594,300", "Eye R", fill=NONE,
       stroke=INK, strokeWidth=6, cap="round")
d.path("M414,282 L446,284", "Lid L", fill=NONE, stroke=INK, strokeWidth=4,
       cap="round", opacity=70)
d.path("M554,284 L586,282", "Lid R", fill=NONE, stroke=INK, strokeWidth=4,
       cap="round", opacity=70)
# the big koala nose
d.shape("ellipse", "Nose", x=474, y=306, width=52, height=66,
        fill=NOSE, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Nose shine", x=484, y=316, width=16, height=20,
        fill="#8A7480", opacity=70, stroke=NONE)
d.path("M500,372 L500,382 M500,382 C490,392 478,392 472,386 M500,382 "
       "C510,392 522,392 528,386", "Mouth", fill=NONE, stroke=INK,
       strokeWidth=4, cap="round")

# --- the wall chart, hugged ------------------------------------------------------
d.shape("rectangle", "Chart", x=360, y=412, width=280, height=282,
        fill=CARD, stroke=INK, strokeWidth=5, radius=14)
# header: label bar + tiny ledger squiggles
d.path("M360,452 L640,452", "Chart header rule", fill=NONE, stroke=INK,
       strokeWidth=3, opacity=60)
d.text("KPI", "Chart label", x=384, y=444, size=20, font="Virelai Sans",
       color=INK)
d.shape("rectangle", "Chart header dash", x=560, y=434, width=56, height=10,
        fill="#8A8068", stroke=NONE, radius=5)
# faint ledger rows — the drill-down layers, compressed to texture
for i, y in enumerate((478, 592, 626)):
    d.path(f"M382,{y} L618,{y}", f"Chart grid {i+1}", fill=NONE,
           stroke="#B4AA8E", strokeWidth=3, opacity=60)
# axes
d.path("M396,664 L396,472 M396,664 L616,664", "Chart axes", fill=NONE,
       stroke="#8A8068", strokeWidth=4, cap="round")
# the green band: widened, comfortable, official
d.shape("rectangle", "Green band", x=382, y=502, width=236, height=66,
        fill=GREEN, opacity=30, stroke=NONE)
d.path("M382,502 L618,502 M382,568 L618,568", "Band edges", fill=NONE,
       stroke=GREEN, strokeWidth=2, opacity=45)
# the trendline: climbs, then flattens politely inside the band
d.path("M404,644 L442,612 L474,578 L506,548 L546,538 L584,540 L612,538",
       "Trendline", fill=NONE, stroke="#2C9E62", strokeWidth=6,
       cap="round", join="round")
for i, (x, y) in enumerate([(404, 644), (442, 612), (474, 578), (506, 548),
                            (546, 538), (584, 540), (612, 538)]):
    d.shape("ellipse", f"Trend dot {i+1}", x=x - 4, y=y - 4, width=8, height=8,
            fill="#2C9E62", stroke=NONE)
# the red line: drooping, unaggregated, nobody's headline
d.path("M404,600 L448,616 L492,610 L536,636 L580,648 L612,652",
       "Red line", fill=NONE, stroke=RED, strokeWidth=4, cap="round",
       join="round", opacity=75)
# y-axis ticks
for i, y in enumerate((640, 608, 576)):
    d.path(f"M396,{y} L388,{y}", f"Tick {i+1}", fill=NONE, stroke="#8A8068",
           strokeWidth=4, cap="round")

# --- the grip: forearms around the chart, paws on its face -----------------------
# arms run behind the chart edges, paws land on top — the grip is not clip-on
d.path("M386,486 C342,514 330,596 362,652", "Arm L", fill=NONE,
       stroke=FUR_MID, strokeWidth=28, cap="round")
d.path("M614,486 C658,514 670,596 638,652", "Arm R", fill=NONE,
       stroke=FUR_MID, strokeWidth=28, cap="round")
d.shape("ellipse", "Paw L", x=342, y=622, width=52, height=42,
        fill=FUR, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Paw R", x=606, y=622, width=52, height=42,
        fill=FUR, stroke=INK, strokeWidth=4)
# one soft crease low on each paw, paw over paw mid-re-grip
d.path("M354,642 C362,650 378,650 386,642", "Paw crease L", fill=NONE,
       stroke=INK, strokeWidth=3, cap="round", opacity=70)
d.path("M614,642 C622,650 638,650 646,642", "Paw crease R", fill=NONE,
       stroke=INK, strokeWidth=3, cap="round", opacity=70)

# --- the clip-on tie, draped over the chart's top edge ----------------------------
d.path("M484,388 L516,388 L510,410 L490,410 Z", "Tie knot",
       fill=TIE, stroke=INK, strokeWidth=4, join="round")
d.path("M490,410 L510,410 L518,452 L500,466 L482,452 Z", "Tie blade",
       fill=TIE, stroke=INK, strokeWidth=4, join="round")
d.path("M488,392 L512,392", "Tie clip", fill=NONE, stroke="#C8A24E",
       strokeWidth=5, cap="round")

# --- captions ---------------------------------------------------------------------------
d.text("KPI KOALA", "Name", x=500, y=930, size=58,
       font="Virelai Sans", color="#E2E8F4", justify="center")
r = d.text("NAPS INSIDE THE GREEN BAND", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#9EACC6", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("231.kpi-koala-V1R00")
