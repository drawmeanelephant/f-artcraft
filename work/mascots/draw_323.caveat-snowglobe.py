#!/usr/bin/env python3
"""Caveat Snowglobe — mascot portrait V1R00.
A snowglobe on a boardroom table, small red flags suspended inside like snow —
warnings preserved as decorative context, sealed beyond reach.
1000x1000. Gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Caveat Snowglobe — Mascot Portrait", 1000, 1000)

INK = "#2A2226"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#141F27"}, {"offset": 1, "color": "#060A0F"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#3E525C"}, {"offset": 0.7, "color": "#243640"},
    {"offset": 1, "color": "#121F26"}]}}
TABLE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6B4630"}, {"offset": 1, "color": "#2E1C12"}]}}
BASE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#D2A468"}, {"offset": 0.55, "color": "#9C6C34"},
    {"offset": 1, "color": "#5E3C1C"}]}}
GLASS = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#EAFBF8"}, {"offset": 0.75, "color": "#B8DCDA"},
    {"offset": 1, "color": "#7FAEB0"}]}}
MOUND = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F4FBFA"}, {"offset": 1, "color": "#B9D4D8"}]}}
FLAG = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#D84838"}, {"offset": 1, "color": "#8E1F16"}]}}
PAPER = "#EDE4CE"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#54707C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D0E4E2", strokeWidth=3, opacity=45)
for i, (x, y, w) in enumerate([(192,235,8),(802,232,7),(158,526,9),(836,545,8),
                               (246,765,7),(754,748,9),(134,394,6),(863,392,7),
                               (392,112,7),(612,111,8),(334,822,6),(664,820,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#3A545E", opacity=45, stroke=NONE)

# warm downlight pooling over the centerpiece
d.shape("ellipse", "Downlight", x=300, y=190, width=400, height=230,
        fill="#F0C878", opacity=8, stroke=NONE)

# faint chair backs flanking the table, well inside the lower rim
d.path("M255,790 C255,742 290,716 330,716 C370,716 405,742 405,790 Z",
       "Chair back L", fill="#0E181E", opacity=55, stroke=NONE)
d.path("M595,790 C595,742 630,716 670,716 C710,716 745,742 745,790 Z",
       "Chair back R", fill="#0E181E", opacity=55, stroke=NONE)

# --- boardroom table ------------------------------------------------------------
d.shape("ellipse", "Table", x=210, y=652, width=580, height=120,
        fill=TABLE_GRAD, stroke=INK, strokeWidth=6)
# polished sheen + front-edge highlight
d.shape("ellipse", "Table sheen", x=270, y=666, width=460, height=34,
        fill="#9A6A44", opacity=30, stroke=NONE)
d.path("M240,742 A265,52 0 0 0 760,742", "Table edge light", fill=NONE,
       stroke="#8A5E40", strokeWidth=4, opacity=55, cap="round")
# globe's soft reflection on the polish
d.shape("ellipse", "Globe reflection", x=390, y=716, width=220, height=26,
        fill="#D8B87E", opacity=13, stroke=NONE)

# --- the paperwork that cites the caveat -----------------------------------------
# risk register sheet, left of the globe — kept clear of the plinth silhouette
d.path(rot_rect_path(272, 702, 116, 80, -8), "Risk sheet",
       fill=PAPER, stroke=INK, strokeWidth=4)
r0 = d.text("RISK REGISTER", "Sheet head", x=270, y=680, size=10,
            font="Virelai Sans", color="#6E5844", justify="center")
if r0 and r0.get("id"):
    d.cmd("text.setStyle", "sheet track", ids=[r0["id"]], tracking=40)
for i in range(3):
    d.path(f"M228,{700+i*13} L{300-i*6},{695+i*13}", f"Sheet line {i+1}",
           fill=NONE, stroke="#A89E84", strokeWidth=4, cap="round", opacity=80)
# one flagged line — the caveat, miniaturized
d.path("M286,734 L312,732", "Flagged line", fill=NONE, stroke="#C23A2E",
       strokeWidth=4, cap="round", opacity=85)
d.path("M304,716 L304,734 L320,727 Z", "Sheet flag", fill=FLAG,
       stroke=INK, strokeWidth=2.5, join="round")

# appendix binder, right of the globe — caveats live here too
d.path(rot_rect_path(730, 700, 110, 46, 7), "Appendix binder",
       fill="#31434E", stroke=INK, strokeWidth=5)
d.path("M696,680 L686,706", "Binder spine", fill=NONE, stroke=INK,
       strokeWidth=3, opacity=70)
r1 = d.text("APPENDIX", "Binder label", x=736, y=700, size=11,
            font="Virelai Sans", color="#C2D2D4", justify="center")
if r1 and r1.get("id"):
    d.cmd("text.setStyle", "binder track", ids=[r1["id"]], tracking=80)

# --- inside the globe (drawn before the glass) ------------------------------------
# dome interior air — a shade cooler than the room
d.shape("ellipse", "Dome air", x=325, y=280, width=350, height=350,
        fill="#28424C", opacity=65, stroke=NONE)
# snow mound along the dome's floor
d.shape("ellipse", "Snow mound", x=410, y=566, width=180, height=58,
        fill=MOUND, stroke="#8FB4B8", strokeWidth=3, opacity=95)
d.shape("ellipse", "Mound shadow", x=440, y=602, width=120, height=20,
        fill="#7FA8AC", opacity=40, stroke=NONE)

# planted red flags — warnings on poles, stuck in the snow
for i, (px, top, bot, flip) in enumerate([(458, 505, 602, 1),
                                          (512, 468, 606, -1),
                                          (556, 528, 606, 1)]):
    d.path(f"M{px},{bot} L{px},{top}", f"Flag pole {i+1}", fill=NONE,
           stroke="#3A3236", strokeWidth=4, cap="round")
    # swallowtail pennant
    s = 1 if flip > 0 else -1
    d.path(f"M{px},{top} L{px+30*s},{top+6} L{px+21*s},{top+13} "
           f"L{px+30*s},{top+20} L{px},{top+18} Z",
           f"Pennant {i+1}", fill=FLAG, stroke=INK, strokeWidth=3, join="round")

# loose flags adrift in the snow-swirl — swallowtails, suspended like flakes
def rot_poly(cx, cy, pts, deg):
    t = math.radians(deg); c, s = math.cos(t), math.sin(t)
    out = [(cx + px*c - py*s, cy + px*s + py*c) for px, py in pts]
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in out) + " Z"
for i, (x, y, rot) in enumerate([(436, 366, -24), (562, 344, 18),
                                 (488, 402, 40), (608, 452, -14),
                                 (398, 458, 30), (540, 490, -36)]):
    d.path(rot_poly(x, y, [(-14,-7),(14,-4),(7,0),(14,5),(-14,7)], rot),
           f"Drift flag {i+1}", fill=FLAG, stroke=INK, strokeWidth=2.5,
           join="round", opacity=92)

# snow flakes settling over the red
for i, (x, y, r) in enumerate([(452,330,5),(530,318,4),(596,394,5),(420,416,4),
                               (482,442,5),(576,508,4),(448,520,5),(518,552,4),
                               (612,420,3),(392,500,4),(560,392,3),(506,362,4)]):
    d.shape("ellipse", f"Flake {i+1}", x=x, y=y, width=r*2, height=r*2,
            fill="#F4FBFA", opacity=75, stroke=NONE)

# --- the glass --------------------------------------------------------------------
d.shape("ellipse", "Glass dome", x=325, y=280, width=350, height=350,
        fill=GLASS, stroke=INK, strokeWidth=7, opacity=22)
# specular sweep upper-left + faint bounce lower-right
d.path("M382,352 C410,312 458,296 500,300", "Specular main", fill=NONE,
       stroke="#FFFFFF", strokeWidth=14, cap="round", opacity=35)
d.path("M398,336 C420,312 452,300 478,300", "Specular core", fill=NONE,
       stroke="#FFFFFF", strokeWidth=6, cap="round", opacity=50)
d.path("M600,560 C622,548 636,528 640,506", "Bounce arc", fill=NONE,
       stroke="#CFEAE8", strokeWidth=8, cap="round", opacity=22)
d.shape("ellipse", "Glass glint", x=368, y=330, width=26, height=16,
        fill="#FFFFFF", opacity=55, stroke=NONE)

# --- the plinth the room never opens ------------------------------------------------
# brass seat ring where glass meets base
d.shape("ellipse", "Seat ring", x=318, y=600, width=364, height=44,
        fill=BASE_GRAD, stroke=INK, strokeWidth=6)
d.shape("ellipse", "Seat sheen", x=352, y=606, width=296, height=16,
        fill="#F0D49A", opacity=35, stroke=NONE)
# plinth body
d.path("M352,630 L648,630 L668,694 C668,704 660,712 650,712 L350,712 "
       "C340,712 332,704 332,694 Z", "Plinth", fill=BASE_GRAD,
       stroke=INK, strokeWidth=7, join="round")
d.path("M352,646 L648,646", "Plinth groove", fill=NONE, stroke="#5E3C1C",
       strokeWidth=3, opacity=60)
d.path("M356,634 L644,634", "Plinth top light", fill=NONE, stroke="#F0D49A",
       strokeWidth=3, opacity=50)
# the engraved instruction the base exists to perform
r2 = d.text("NOTED", "Plinth engraving", x=500, y=682, size=15,
            font="Virelai Sans", color="#4A2E14", justify="center")
if r2 and r2.get("id"):
    d.cmd("text.setStyle", "engrave track", ids=[r2["id"]], tracking=160)

# --- captions ----------------------------------------------------------------------
d.text("CAVEAT SNOWGLOBE", "Name", x=500, y=930, size=56, font="Virelai Sans",
       color="#D8E6E4", justify="center")
r = d.text("DECORATIVE DILIGENCE", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#98B8B4", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("323.caveat-snowglobe-V1R00")
