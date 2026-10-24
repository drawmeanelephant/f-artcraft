#!/usr/bin/env python3
"""Moveda Permanently — mascot portrait V1R00. 301 Redirect Oracle.
A decisive oracle holding aloft a Location: header slip; beside her an
arrow signpost reading PLEASE UPDATE YOUR BOOKMARKS, a dashed trail leads
to it, and the old doorway fades behind. "It has moved. It stays moved."
1000x1000. House style: gradients + translucent shading, never flat fills.
Digits are set in Source Sans 3 (Virelai carries no figures)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Moveda Permanently — Mascot Portrait", 1000, 1000)

INK = "#2C2630"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1E2030"}, {"offset": 1, "color": "#0C0D16"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E6DDF2"}, {"offset": 0.7, "color": "#B2A4CE"},
    {"offset": 1, "color": "#74659A"}]}}
ROBE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#5E6E88"}, {"offset": 0.72, "color": "#3E4A60"},
    {"offset": 1, "color": "#2A3040"}]}}
FACE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F2E2C2"}, {"offset": 1, "color": "#D4B98E"}]}}
WOOD_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#96744E"}, {"offset": 1, "color": "#6E5234"}]}}
BRASS = "#C89A4A"
SLIP_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F6EFDA"}, {"offset": 1, "color": "#D8CBA4"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#5C5078", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#EAE4F4", strokeWidth=3, opacity=50)
for i, (x, y, w) in enumerate([(204,226,8),(790,222,7),(174,522,9),(824,534,8),
                               (254,766,7),(750,752,9),(146,394,6),(852,390,7),
                               (398,108,7),(606,118,8),(338,814,6),(660,824,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#8C7EAE", opacity=42, stroke=NONE)

# --- the old doorway, already fading ----------------------------------------------
d.path("M252,580 L252,430 L304,392 L356,430 L356,580",
       "Old doorway", fill=NONE, stroke="#6A6080", strokeWidth=5,
       dash=[7, 9], opacity=45, cap="round", join="round")
d.path("M276,542 L332,542 M276,508 L332,508", "Old doorway shelf",
       fill=NONE, stroke="#6A6080", strokeWidth=3.5, dash=[5, 8],
       opacity=35, cap="round")
d.path("M296,470 L312,470 M304,462 L304,478", "Gone mark", fill=NONE,
       stroke="#6A6080", strokeWidth=4, opacity=40, cap="round")

# --- the relocation trail: footprints marching right along the floor --------------
d.path("M250,756 C380,742 640,742 786,750", "Floor line",
       fill=NONE, stroke="#6A6080", strokeWidth=3, opacity=50, cap="round")
for i, (x, y) in enumerate([(470, 738), (530, 732), (590, 736), (650, 730)]):
    d.shape("ellipse", f"Step {i+1}", x=x, y=y, width=16, height=9,
            fill="#4A4262", opacity=55 - i * 4, stroke=NONE)
# --- the signpost: an arrow placard pointing right ----------------------------------
d.shape("ellipse", "Post shadow", x=730, y=738, width=90, height=14,
        fill="#4A4262", opacity=40, stroke=NONE)
d.shape("rectangle", "Post", x=758, y=448, width=18, height=296,
        fill=WOOD_GRAD, stroke=INK, strokeWidth=4)
# 301 badge crowning the post — digits in Source Sans 3
d.shape("ellipse", "Badge", x=741, y=396, width=52, height=48,
        fill=BRASS, stroke=INK, strokeWidth=4)
r = d.text("301", "Badge digits", x=767, y=429, size=20,
           font="Source Sans 3", color=INK, justify="center")
# arrow placard
d.path("M588,478 L742,478 L742,458 L810,498 L742,538 L742,518 L588,518 Z",
       "Sign arrow", fill=SLIP_GRAD, stroke=INK, strokeWidth=5, join="round")
d.text("PLEASE UPDATE", "Sign line 1", x=664, y=492, size=14,
       font="Virelai Sans", color=INK, justify="center")
d.text("YOUR BOOKMARKS", "Sign line 2", x=664, y=510, size=14,
       font="Virelai Sans", color=INK, justify="center")
# hanging moss of old URLs under the sign
d.path("M610,518 C610,532 606,540 610,552 M640,518 C638,528 642,536 638,546",
       "Old URL moss", fill=NONE, stroke="#7A6E96", strokeWidth=3,
       cap="round", opacity=55)

# --- Moveda: the redirect oracle -----------------------------------------------------
d.shape("ellipse", "Figure shadow", x=356, y=740, width=280, height=26,
        fill="#4A4262", opacity=38, stroke=NONE)
# robe: upright column, forward shoulders — decisive
d.path("M384,744 C378,646 384,556 408,494 C428,442 462,420 502,424 "
       "C546,430 576,476 582,548 C588,634 588,696 586,744 Z",
       "Robe", fill=ROBE_GRAD, stroke=INK, strokeWidth=7, join="round")
d.path("M444,570 C442,628 442,686 444,734 M540,566 C546,626 548,684 546,734",
       "Robe folds", fill=NONE, stroke="#232836", strokeWidth=4,
       opacity=45, cap="round")
# shoulder drape
d.path("M402,506 C410,452 448,424 496,422 C544,424 576,456 582,506 "
       "C552,478 520,466 492,466 C458,466 428,480 402,506 Z",
       "Drape", fill="#4A5670", stroke=INK, strokeWidth=5, join="round")
# head, chin up, eyes already on the destination
d.shape("ellipse", "Head", x=432, y=346, width=130, height=114,
        fill=FACE_GRAD, stroke=INK, strokeWidth=6)
# hair: swept back into a firm knot
d.path("M438,392 C440,352 468,332 500,332 C534,332 558,354 560,392 "
       "C534,374 466,374 438,392 Z", "Hair", fill="#5E5248",
       stroke=INK, strokeWidth=5, join="round")
d.shape("ellipse", "Knot", x=540, y=350, width=34, height=30,
        fill="#5E5248", stroke=INK, strokeWidth=4.5)
# circlet band with a small arrow gem
d.path("M444,392 C468,380 530,380 556,392", "Circlet", fill=NONE,
       stroke=BRASS, strokeWidth=5, cap="round")
d.path("M494,374 L508,380 L494,386 Z", "Circlet gem", fill=BRASS,
       stroke=INK, strokeWidth=2.5, join="round")
# level brows, eyes looking right
d.path("M456,424 L486,424 M518,424 L548,424", "Brows",
       fill=NONE, stroke=INK, strokeWidth=4.5, cap="round")
d.shape("ellipse", "Eye L", x=464, y=434, width=14, height=16,
        fill="#33222A", stroke=NONE)
d.shape("ellipse", "Eye R", x=528, y=434, width=14, height=16,
        fill="#33222A", stroke=NONE)
d.shape("ellipse", "Glint L", x=470, y=437, width=4.5, height=4.5,
        fill="#FFFFFF", stroke=NONE)
d.shape("ellipse", "Glint R", x=534, y=437, width=4.5, height=4.5,
        fill="#FFFFFF", stroke=NONE)
# calm resolved mouth
d.path("M482,474 C494,478 508,478 520,473", "Mouth",
       fill=NONE, stroke=INK, strokeWidth=4.5, cap="round")

# left arm raised: the Location header slip
d.path("M408,524 C380,506 366,480 368,452", "Sleeve L",
       fill=NONE, stroke="#3E4A60", strokeWidth=28, cap="round")
d.shape("ellipse", "Hand L", x=356, y=432, width=30, height=26,
        fill="#E8CBA0", stroke=INK, strokeWidth=4)
# the slip itself — a header, brass-clipped
d.path(rot_rect_path(400, 388, 168, 46, -8), "Location slip",
       fill=SLIP_GRAD, stroke=INK, strokeWidth=4, join="round")
t = d.text("LOCATION: /NEW", "Slip text", x=400, y=394, size=15,
           font="Virelai Sans", color=INK, justify="center")
if t and t.get("id"):
    d.cmd("object.rotate", "slip text tilt", ids=[t["id"]],
          angle=8, origin=[400, 388])
# right arm extended toward the sign — the pointing hand
d.path("M576,530 C612,536 636,552 648,574", "Sleeve R",
       fill=NONE, stroke="#3E4A60", strokeWidth=28, cap="round")
d.shape("ellipse", "Hand R", x=640, y=566, width=30, height=26,
        fill="#E8CBA0", stroke=INK, strokeWidth=4)
# pointing finger: skin stroke inked by a thinner line
d.path("M666,574 L692,570", "Point", fill=NONE, stroke=INK,
       strokeWidth=13, cap="round")
d.path("M666,574 L692,570", "Finger", fill=NONE, stroke="#E8CBA0",
       strokeWidth=8, cap="round")

# --- name + role -------------------------------------------------------------------
d.text("MOVEDA PERMANENTLY", "Name", x=500, y=930, size=52,
       font="Virelai Sans", color="#ECE6F6", justify="center")
r = d.text("301 REDIRECT ORACLE", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#BCAEDA", justify="center")
if r and r.get("id"):
    # Virelai Sans has no digit glyphs: "301" falls back to Source Sans 3
    d.cmd("text.setStyle", "role digits", ids=[r["id"]], start=0, end=3,
          font="Source Sans 3")
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("024.moveda-permanently-V1R00")
