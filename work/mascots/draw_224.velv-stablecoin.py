#!/usr/bin/env python3
"""Velv — mascot portrait V1R00.
A soft liquidity-backed blob, faintly glowing, on the presentation slide
that is always marked 12. 1000x1000. Gradients + translucent shading,
never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Velv — Mascot Portrait", 1000, 1000)

INK = "#2E2434"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#141C26"}, {"offset": 1, "color": "#070A10"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#3E5C60"}, {"offset": 0.7, "color": "#2A3E48"},
    {"offset": 1, "color": "#16222C"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#263642"}, {"offset": 1, "color": "#121C26"}]}}
SLIDE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#202E3C"}, {"offset": 1, "color": "#101A26"}]}}
VELV = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#EAFBF2"}, {"offset": 0.55, "color": "#BDE8D4"},
    {"offset": 0.85, "color": "#8CCCB4"}, {"offset": 1, "color": "#6EAE9C"}]}}
MINT = "#9FE8CC"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#5E8288", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C4E4DC", strokeWidth=3, opacity=50)
for i, (x, y, w) in enumerate([(192,238,8),(802,232,7),(160,520,9),(832,544,8),
                               (246,762,7),(756,746,9),(132,394,6),(864,392,7),
                               (394,112,7),(610,110,8),(332,820,6),(666,820,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#33505A", opacity=45, stroke=NONE)

# --- floor ---------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0A1018",
       strokeWidth=4, opacity=70)

# --- the presentation slide, propped like a screen -------------------------------
d.shape("ellipse", "Screen glow spill", x=170, y=200, width=660, height=440,
        fill=MINT, opacity=8, stroke=NONE)
d.shape("rectangle", "Slide", x=215, y=225, width=570, height=380,
        fill=SLIDE, stroke="#48606E", strokeWidth=6, radius=18)
d.shape("rectangle", "Slide inner bezel", x=233, y=243, width=534, height=344,
        fill=NONE, stroke="#2E4250", strokeWidth=3, radius=12)
# slide chrome: header rule + bullet ghosts, deliberately vague
d.path("M233,300 L767,300", "Slide header rule", fill=NONE, stroke="#3A5060",
       strokeWidth=3, opacity=80)
for i, (x, y, w) in enumerate([(258, 326, 150), (258, 352, 110), (620, 560, 122)]):
    d.shape("rectangle", f"Slide bullet {i+1}", x=x, y=y, width=w, height=12,
            fill="#3A5060", stroke=NONE, radius=6, opacity=70)
# slide number: always 12
d.shape("rectangle", "Slide tab", x=700, y=243, width=58, height=40,
        fill="#16222E", stroke="#48606E", strokeWidth=3, radius=8)
d.text("12", "Slide number", x=729, y=272, size=24,
       font="Source Sans 3", color=MINT, justify="center")
# projector beam hint from the top of the disc
d.path("M360,110 L215,240 M640,110 L785,240", "Beam", fill=NONE,
       stroke="#BDE8D4", strokeWidth=2, opacity=10)

# --- Velv: the glowing blob, on the slide ----------------------------------------
d.shape("ellipse", "Velv shadow", x=390, y=560, width=220, height=32,
        fill="#060A0E", opacity=50, stroke=NONE)
# consensus glow: concentric translucent rings
d.shape("ellipse", "Glow outer", x=285, y=265, width=430, height=360,
        fill=MINT, opacity=8, stroke=NONE)
d.shape("ellipse", "Glow mid", x=325, y=300, width=350, height=295,
        fill=MINT, opacity=12, stroke=NONE)
d.shape("ellipse", "Glow inner", x=370, y=335, width=260, height=225,
        fill=MINT, opacity=16, stroke=NONE)
# blob body: a settled, slightly asymmetric blob
d.path("M500,340 C575,340 636,392 644,458 C652,522 620,566 560,584 "
       "C510,599 448,596 404,570 C356,542 344,486 360,432 "
       "C376,378 430,340 500,340 Z",
       "Velv body", fill=VELV, stroke=INK, strokeWidth=6)
# inner softness: translucent core
d.shape("ellipse", "Velv core", x=420, y=390, width=170, height=140,
        fill="#F2FDF6", opacity=40, stroke=NONE)
# gentle closed eyes, nonverbal and serene
d.path("M442,452 C452,444 468,444 478,452", "Eye L", fill=NONE,
       stroke=INK, strokeWidth=6, cap="round")
d.path("M522,452 C532,444 548,444 558,452", "Eye R", fill=NONE,
       stroke=INK, strokeWidth=6, cap="round")
# the faintest suggestion of a mouth: no opinion expressed
d.path("M486,486 C494,490 506,490 514,486", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round", opacity=60)
# soft blush of consensus
d.shape("ellipse", "Cheek L", x=414, y=472, width=30, height=16,
        fill="#7EC8AC", opacity=45, stroke=NONE)
d.shape("ellipse", "Cheek R", x=556, y=472, width=30, height=16,
        fill="#7EC8AC", opacity=45, stroke=NONE)
# the peg: a level line under the blob, unperturbed
d.path("M340,640 L660,640", "Peg line", fill=NONE, stroke=MINT,
       strokeWidth=5, cap="round", opacity=70)
d.shape("ellipse", "Peg dot L", x=334, y=634, width=12, height=12,
        fill=MINT, opacity=80, stroke=NONE)
d.shape("ellipse", "Peg dot R", x=654, y=634, width=12, height=12,
        fill=MINT, opacity=80, stroke=NONE)

# --- captions ---------------------------------------------------------------------------
d.text("VELV", "Name", x=500, y=930, size=58,
       font="Virelai Sans", color="#D8F0E4", justify="center")
r = d.text("STABLECOIN OF EMPATHY", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#9CC4B4", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("224.velv-stablecoin-V1R00")
