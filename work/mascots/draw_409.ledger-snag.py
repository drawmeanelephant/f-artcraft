#!/usr/bin/env python3
"""Ledger Snarl — mascot portrait V1R00 (slug 409.ledger-snag).
Mascot holding open a ledger, both facing pages stamped VALID.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Ledger Snarl — Mascot Portrait", 1000, 1000)

INK = "#3A2B22"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#141F14"}, {"offset": 1, "color": "#070C07"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#A8BC84"}, {"offset": 0.7, "color": "#7C9160"},
    {"offset": 1, "color": "#4C5E3C"}]}}
BODY = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#8FD8C8"}, {"offset": 0.72, "color": "#5FB0A0"},
    {"offset": 1, "color": "#3E8478"}]}}
PAGE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F4ECD2"}, {"offset": 1, "color": "#DCCFA4"}]}}
COVER = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4E6E3A"}, {"offset": 1, "color": "#324A24"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#5E7448", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8F0D0", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(200,230,8),(795,235,7),(165,535,9),(825,555,8),
                               (250,755,7),(745,745,9),(140,395,6),(858,405,7),
                               (395,118,7),(605,112,8),(335,815,6),(662,812,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#5E7448", opacity=42, stroke=NONE)

# --- mascot body (behind the ledger) ------------------------------------------
d.path("M500,430 C575,430 622,478 626,548 C630,622 590,700 500,700 "
       "C410,700 370,622 374,548 C378,478 425,430 500,430 Z",
       "Body", fill=BODY, stroke=INK, strokeWidth=7)
d.shape("ellipse", "Body highlight", x=425, y=445, width=120, height=50,
        fill="#FFFFFF", opacity=20, stroke=NONE)
# feet peeking under the ledger
d.shape("ellipse", "Foot L", x=435, y=690, width=46, height=30, fill=BODY,
        stroke=INK, strokeWidth=6)
d.shape("ellipse", "Foot R", x=519, y=690, width=46, height=30, fill=BODY,
        stroke=INK, strokeWidth=6)
# the snarl: a tangled knot-loop sprouting from the crown
d.path("M500,432 C492,400 470,392 468,368 C466,346 488,336 502,350 "
       "C516,336 540,348 534,370 C530,388 512,392 508,408 "
       "M482,362 C496,352 514,358 518,372",
       "Snarl knot", fill=NONE, stroke=INK, strokeWidth=6, cap="round")
d.path("M474,384 C490,370 516,370 530,388 C518,382 500,386 492,398",
       "Knot cross", fill=NONE, stroke=INK, strokeWidth=5, cap="round")
d.path("M500,432 C496,415 490,408 485,398", "Knot stem", fill=NONE,
       stroke=INK, strokeWidth=6, cap="round")
# face: flat brows, side-eye, crooked smug snarl-smile
d.path("M425,492 L470,486", "Brow L", fill=NONE, stroke=INK, strokeWidth=6, cap="round")
d.path("M530,486 L575,492", "Brow R", fill=NONE, stroke=INK, strokeWidth=6, cap="round")
d.shape("ellipse", "Eye L", x=432, y=502, width=30, height=34, fill="#FBF6E8",
        stroke=INK, strokeWidth=5)
d.shape("ellipse", "Eye R", x=538, y=502, width=30, height=34, fill="#FBF6E8",
        stroke=INK, strokeWidth=5)
d.shape("ellipse", "Pupil L", x=444, y=512, width=12, height=14, fill=INK, stroke=NONE)
d.shape("ellipse", "Pupil R", x=550, y=512, width=12, height=14, fill=INK, stroke=NONE)
# crooked smile with a tooth tick
d.path("M448,568 C480,584 525,586 556,572 L556,562", "Snarl smile", fill=NONE,
       stroke=INK, strokeWidth=6, cap="round", join="round")
d.shape("ellipse", "Blush L", x=412, y=540, width=26, height=15, fill="#E89B8A",
        opacity=45, stroke=NONE)
d.shape("ellipse", "Blush R", x=566, y=540, width=26, height=15, fill="#E89B8A",
        opacity=45, stroke=NONE)
# arms around the ledger edges
d.path("M392,600 C360,605 340,615 322,632", "Arm L", fill=NONE, stroke=BODY,
       strokeWidth=24, cap="round")
d.path("M608,600 C640,605 660,615 678,632", "Arm R", fill=NONE, stroke=BODY,
       strokeWidth=24, cap="round")

# --- the open ledger, held toward the viewer -----------------------------------
d.path("M272,556 L494,572 L494,714 L272,696 Z M506,572 L728,556 L728,696 L506,714 Z",
       "Ledger cover", fill=COVER, stroke=INK, strokeWidth=6, join="round")
d.path("M282,562 L492,577 L492,703 L282,687 Z", "Page L", fill=PAGE,
       stroke=INK, strokeWidth=5, join="round")
d.path("M508,577 L718,562 L718,687 L508,703 Z", "Page R", fill=PAGE,
       stroke=INK, strokeWidth=5, join="round")
# faint ruled lines on both pages
for i in range(4):
    y = 594 + i*26
    d.path(f"M296,{y} L478,{y+12}", f"Rule L{i+1}", fill=NONE,
           stroke="#B8A878", strokeWidth=2, opacity=60)
    d.path(f"M522,{y+12} L704,{y}", f"Rule R{i+1}", fill=NONE,
           stroke="#B8A878", strokeWidth=2, opacity=60)
# hands gripping the outer page edges
d.shape("ellipse", "Hand L", x=268, y=608, width=34, height=40, fill=BODY,
        stroke=INK, strokeWidth=6)
d.shape("ellipse", "Hand R", x=698, y=608, width=34, height=40, fill=BODY,
        stroke=INK, strokeWidth=6)

# --- VALID stamps, one per page ------------------------------------------------
def stamp(cx, cy, label):
    d.shape("ellipse", f"{label} outer", x=cx-44, y=cy-44, width=88, height=88,
            fill=NONE, stroke="#3E8A54", strokeWidth=5, opacity=85)
    d.shape("ellipse", f"{label} inner", x=cx-36, y=cy-36, width=72, height=72,
            fill=NONE, stroke="#3E8A54", strokeWidth=2, opacity=70)
    t = d.text("VALID", f"{label} word", x=cx, y=cy+7, size=22,
               font="Virelai Sans", color="#3E8A54", justify="center")
    if t and t.get("id"):
        d.cmd("text.setStyle", f"{label} track", ids=[t["id"]], tracking=60)

stamp(388, 628, "Stamp L")
stamp(612, 628, "Stamp R")
# fresh-ink smudge beside the right stamp
d.path("M660,668 C672,662 684,664 690,672", "Ink smudge", fill=NONE,
       stroke="#3E8A54", strokeWidth=4, opacity=45, cap="round")

# --- captions ------------------------------------------------------------------
d.text("LEDGER SNARL", "Name", x=500, y=930, size=56, font="Virelai Sans",
       color="#E4EDD0", justify="center")
r = d.text("VALIDATOR IN RESIDENCE", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#A9BE8A", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("409.ledger-snag-V1R00")
