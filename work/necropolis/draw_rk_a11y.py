#!/usr/bin/env python3
"""rc-a11y.sh — The Contrast Vigil. Necropolis plate V1R00.
An eye chart in a candlelit crypt — rows of shrinking glyphs in failing
contrast — while a robed optometrist holds palette swatches up to the
flame, marking which pass WCAG and which get buried. 1000x1000.
Gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("RC-A11Y — Necropolis Plate", 1000, 1000)

INK = "#1E222C"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#12151E"}, {"offset": 1, "color": "#07080C"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#454E60"}, {"offset": 0.7, "color": "#2A303E"},
    {"offset": 1, "color": "#141822"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#262C38"}, {"offset": 1, "color": "#10131A"}]}}
PARCH = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E4D6B4"}, {"offset": 1, "color": "#B8A67E"}]}}
BOARD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3E444F"}, {"offset": 1, "color": "#232833"}]}}
ROBE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#454E5E"}, {"offset": 0.62, "color": "#272D3A"},
    {"offset": 1, "color": "#151924"}]}}
CANDLE_WAX = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#EAE0C4"}, {"offset": 1, "color": "#B09B6E"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#8A8060", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D9DEE8", strokeWidth=3, opacity=45)
for i, (x, y, w) in enumerate([(193,233,8),(801,230,7),(157,524,9),(837,544,8),
                               (247,766,7),(753,749,9),(133,393,6),(864,391,7),
                               (391,113,7),(613,110,8),(333,823,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#525C70", opacity=35, stroke=NONE)

# --- floor --------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0B0D12",
       strokeWidth=4, opacity=70)

# --- candlelight: one warm pool over the right half ------------------------------
d.shape("ellipse", "Candle spill", x=520, y=330, width=400, height=360,
        fill="#FFCE6E", opacity=10, stroke=NONE)
d.shape("ellipse", "Candle glow", x=700, y=420, width=190, height=170,
        fill="#FFCE6E", opacity=18, stroke=NONE)

# --- the eye chart, pinned to its backboard on the wall --------------------------
d.path("M395,208 L283,252 M395,208 L527,252", "Chart cord", fill=NONE,
       stroke="#6E6452", strokeWidth=3, opacity=80)
d.shape("ellipse", "Cord nail", x=391, y=202, width=9, height=9,
        fill="#8A8060", stroke=INK, strokeWidth=2)
d.shape("rectangle", "Chart board", x=258, y=240, width=296, height=340,
        fill=BOARD, stroke=INK, strokeWidth=5, radius=6)
d.shape("rectangle", "Chart sheet", x=276, y=258, width=260, height=304,
        fill=PARCH, stroke=INK, strokeWidth=3)
# sheet shadow inside the board
d.path("M276,258 L536,258", "Sheet top shade", fill=NONE, stroke="#6E6452",
       strokeWidth=3, opacity=40)
for i, (px, py) in enumerate([(286, 268), (524, 268)]):
    d.shape("ellipse", f"Pin {i+1}", x=px-4, y=py-4, width=8, height=8,
            fill="#8A8060", stroke=INK, strokeWidth=2)

# rows of shrinking glyphs in failing contrast (ink blended toward parchment)
rows = [
    (306, 40, "#322B24", "E F P"),
    (352, 30, "#50483B", "T O Z L"),
    (392, 22, "#6F6451", "P E C F D"),
    (426, 16, "#8B7E66", "E D F C Z P"),
    (456, 12, "#A39477", "F E L O P Z D"),
]
for i, (y, size, col, txt) in enumerate(rows):
    d.text(txt, f"Chart row {i+1}", x=395, y=y, size=size, font="Virelai Sans",
           color=col, justify="center")
# audit marks down the right margin: ticks pass, crosses get buried
for i, (y, ok) in enumerate([(296, True), (342, True), (384, None),
                             (418, False), (450, False)]):
    if ok is True:
        d.path(f"M498,{y+8} L504,{y+16} L516,{y}", f"Pass {i+1}", fill=NONE,
               stroke="#3E5A34", strokeWidth=4, cap="round", join="round")
    elif ok is False:
        d.path(f"M500,{y} L514,{y+14} M514,{y} L500,{y+14}", f"Buried {i+1}",
               fill=NONE, stroke="#7A2E24", strokeWidth=4, cap="round")
    else:
        d.path(f"M500,{y+10} L516,{y+10}", f"Retest {i+1}", fill=NONE,
               stroke="#8A7450", strokeWidth=3, cap="round")
# the chart's own legend, half-faded
d.text("CONTRAST TABLE VII — CRYPT ISSUE", "Chart legend", x=405, y=540,
       size=11, font="Virelai Sans", color="#6E6350", justify="center")

# --- the candle on its stand ------------------------------------------------------
d.shape("ellipse", "Stand shadow", x=748, y=682, width=110, height=16,
        fill="#05060A", opacity=50, stroke=NONE)
d.path("M803,690 L803,560", "Stand pole", fill=NONE, stroke="#4A4438",
       strokeWidth=9, cap="round")
d.path("M782,692 L824,692 L812,676 L794,676 Z", "Stand foot", fill="#4A4438",
       stroke=INK, strokeWidth=4, join="round")
d.shape("ellipse", "Drip pan", x=786, y=548, width=34, height=12,
        fill="#5C5443", stroke=INK, strokeWidth=3)
d.shape("rectangle", "Candle", x=792, y=496, width=22, height=56,
        fill=CANDLE_WAX, stroke=INK, strokeWidth=4, radius=4)
d.path("M803,496 C797,486 799,476 803,468 C807,476 809,486 803,496 Z",
       "Flame", fill="#FFE9B0", stroke="#C8842A", strokeWidth=2)
d.shape("ellipse", "Flame core", x=799, y=482, width=8, height=12,
        fill="#FFF7DC", stroke=NONE)

# --- the robed optometrist ---------------------------------------------------------
d.shape("ellipse", "Figure shadow", x=560, y=682, width=180, height=20,
        fill="#05060A", opacity=50, stroke=NONE)
d.path("M600,695 C596,630 606,570 636,535 C650,518 668,508 684,502 "
       "C676,470 692,440 716,434 C740,440 754,470 748,502 "
       "C764,508 780,520 792,538 C818,576 826,634 822,695 "
       "C780,710 640,710 600,695 Z",
       "Optometrist robe", fill=ROBE_GRAD, stroke=INK, strokeWidth=6, join="round")
# hood void + spectacles catching the flame
d.path("M716,452 C690,462 682,490 688,514 C700,528 732,528 744,514 "
       "C750,490 742,462 716,452 Z",
       "Hood void", fill="#0D0F16", stroke="#39404E", strokeWidth=3)
d.shape("ellipse", "Spectacle L", x=697, y=488, width=16, height=16,
        fill=NONE, stroke="#E8C56A", strokeWidth=3, opacity=85)
d.shape("ellipse", "Spectacle R", x=720, y=488, width=16, height=16,
        fill=NONE, stroke="#E8C56A", strokeWidth=3, opacity=85)
d.path("M713,496 L720,496", "Spectacle bridge", fill=NONE, stroke="#E8C56A",
       strokeWidth=3, opacity=85)
# robe folds
d.path("M660,560 C652,610 650,655 654,690", "Robe fold L", fill=NONE,
       stroke="#101320", strokeWidth=4, opacity=50, cap="round")
d.path("M760,560 C768,610 770,655 766,690", "Robe fold R", fill=NONE,
       stroke="#101320", strokeWidth=4, opacity=50, cap="round")

# --- arm raised, swatch fanned to the flame ----------------------------------------
d.path("M655,545 C640,528 632,516 626,502", "Swatch arm", fill=NONE,
       stroke="#39404E", strokeWidth=30, cap="round")
d.shape("ellipse", "Swatch hand", x=608, y=488, width=26, height=18,
        fill="#7A8290", stroke=INK, strokeWidth=3)
for i, (cx, cy, deg, col, label) in enumerate([
        (584, 476, -26, "#E8E0D0", "Swatch pass"),
        (606, 466, -4, "#8A8276", "Swatch marginal"),
        (627, 474, 18, "#3E3A44", "Swatch buried")]):
    d.path(rot_rect_path(cx, cy, 30, 44, deg), label, fill=col,
           stroke=INK, strokeWidth=2, join="round")
# the marking stylus in the far hand
d.path("M770,560 L795,548", "Far arm", fill=NONE, stroke="#39404E",
       strokeWidth=24, cap="round")
d.path("M792,552 L810,540", "Stylus", fill=NONE, stroke="#8A8060",
       strokeWidth=4, cap="round")

# --- captions ------------------------------------------------------------------
d.text("RC-A11Y", "Name", x=500, y=930, size=58, font="Virelai Sans",
       color="#DEE2EC", justify="center")
r = d.text("CONTRAST AUDIT", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#98A2B8", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("rk-a11y-V1R00")
