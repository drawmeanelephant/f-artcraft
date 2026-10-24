#!/usr/bin/env python3
"""Soft Green Sealie — mascot portrait V1R00. mascots/M-0229.
Round green seal mascot smiling from the edge of a dashboard pane.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Soft Green Sealie — Mascot Portrait", 1000, 1000)

INK = "#22302C"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#101C1E"}, {"offset": 1, "color": "#070D10"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#C4D4C8"}, {"offset": 0.7, "color": "#86A094"},
    {"offset": 1, "color": "#46545C"}]}}
SEAL_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#BCE4B4"}, {"offset": 0.7, "color": "#7EBE8A"},
    {"offset": 1, "color": "#4E8A62"}]}}
PANE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#37444E"}, {"offset": 1, "color": "#222C36"}]}}
GREEN_SOFT = "#8FD8A0"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#4E6058", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#DEEAE0", strokeWidth=3, opacity=55)
# ambient scanline haze — a room that is mostly screens
for i, (x, y, w) in enumerate([(250,210,200),(580,160,240),(330,320,140)]):
    d.shape("ellipse", f"Haze {i+1}", x=x, y=y, width=w, height=w*0.32,
            fill="#DEEEe4", opacity=13, stroke=NONE)

# --- the dashboard pane ----------------------------------------------------------
d.shape("ellipse", "Pane shadow", x=270, y=782, width=480, height=26,
        fill="#2E3A38", opacity=50, stroke=NONE)
d.shape("rectangle", "Pane", x=240, y=410, width=500, height=380,
        radius=26, fill=PANE_GRAD, stroke=INK, strokeWidth=6)
# pane top bezel highlight — the seam she is softening
d.path("M262,424 C400,414 600,414 718,424", "Bezel light",
       fill=NONE, stroke="#7E94A0", strokeWidth=4, opacity=60, cap="round")
# header strip: three window dots and a title rule
for i, x in enumerate([272, 296, 320]):
    d.shape("ellipse", f"Win dot {i+1}", x=x, y=438, width=14, height=14,
            fill=["#D88A8A","#D8C48A",GREEN_SOFT][i], stroke=INK,
            strokeWidth=3, opacity=90)
d.shape("rectangle", "Title rule", x=352, y=438, width=180, height=14,
        radius=7, fill="#5A6E78", stroke=NONE, opacity=80)
# left column: bars climbing gently, none of them red
for i, (x, h) in enumerate([(288,60),(330,88),(372,74),(414,104)]):
    d.shape("rectangle", f"Bar {i+1}", x=x, y=678-h, width=30, height=h,
            radius=6, fill=GREEN_SOFT, stroke=INK, strokeWidth=3,
            opacity=55+i*10)
# center: the gauge that has never needed the red half
d.path("M470,640 A78,78 0 0 1 626,640", "Gauge arc", fill=NONE,
       stroke="#5A6E78", strokeWidth=12, cap="round")
d.path("M470,640 A78,78 0 0 1 560,578", "Gauge green", fill=NONE,
       stroke=GREEN_SOFT, strokeWidth=12, cap="round")
d.path("M548,640 L586,596", "Needle", fill=NONE, stroke="#D8E4DC",
       strokeWidth=6, cap="round")
d.shape("ellipse", "Needle hub", x=540, y=632, width=16, height=16,
        fill="#D8E4DC", stroke=INK, strokeWidth=3)
# sparkline drifting along the bottom, survivable all the way across
d.path("M272,724 C310,712 340,730 372,720 C404,710 430,726 462,718 "
       "C494,710 520,726 552,716 C584,708 614,722 646,714 C672,708 696,716 712,712",
       "Sparkline", fill=NONE, stroke=GREEN_SOFT, strokeWidth=5,
       opacity=80, cap="round")
d.path("M272,748 L712,748", "Baseline", fill=NONE, stroke="#5A6E78",
       strokeWidth=3, opacity=60)

# --- Sealie, settled into the pane's top-right corner ------------------------------
# comfort glow she carries with her
d.shape("ellipse", "Sealie glow", x=470, y=170, width=330, height=300,
        fill=GREEN_SOFT, opacity=18, stroke=NONE)
d.shape("ellipse", "Sealie shadow", x=520, y=428, width=240, height=24,
        fill="#1E2A2E", opacity=45, stroke=NONE)
# one round body — head and torso are the same decision
d.shape("ellipse", "Body", x=496, y=210, width=250, height=240,
        fill=SEAL_GRAD, stroke=INK, strokeWidth=6)
# belly light pooling low on the round
d.path("M540,360 C560,410 620,436 680,424 C660,444 620,452 580,444 "
       "C548,438 532,408 540,360 Z", "Belly light", fill="#DCEAD2",
       opacity=50, stroke=NONE)
# hind flippers splayed at the base, resting on the bezel
d.path("M500,424 C480,432 464,446 458,462 C474,466 496,462 510,450 Z",
       "Flipper L", fill="#5E9470", stroke=INK, strokeWidth=5, join="round")
d.path("M736,414 C758,418 774,430 782,446 C768,452 746,450 732,438 Z",
       "Flipper R", fill="#5E9470", stroke=INK, strokeWidth=5, join="round")
# a front flipper draped over the pane's edge, claiming the seam
d.path("M528,430 C514,458 512,488 520,514 C530,522 546,520 552,508 "
       "C548,482 550,456 558,434 Z", "Arm flipper", fill="#6FAA80",
       stroke=INK, strokeWidth=5, join="round")
# the face: eyes shut in unbothered green assurance
d.path("M572,318 C580,326 594,326 602,318 M648,318 C656,326 670,326 678,318",
       "Eyes", fill=NONE, stroke=INK, strokeWidth=6, cap="round")
d.path("M604,352 C616,364 638,364 648,352", "Smile",
       fill=NONE, stroke=INK, strokeWidth=6, cap="round")
# muzzle softening around the smile
d.path("M592,346 C604,376 646,380 660,350 C652,378 600,380 592,346 Z",
       "Muzzle", fill="#DCEAD2", opacity=45, stroke=NONE)
# whisker freckles
for i, (x, y) in enumerate([(566,336),(560,348),(572,356),(688,336),(694,348),(682,356)]):
    d.shape("ellipse", f"Freckle {i+1}", x=x, y=y, width=5, height=5,
            fill="#2E4438", opacity=70, stroke=NONE)
# blush — the retrospective tolerance, tinted
d.shape("ellipse", "Blush L", x=548, y=338, width=26, height=14,
        fill="#D8989A", opacity=35, stroke=NONE)
d.shape("ellipse", "Blush R", x=680, y=338, width=26, height=14,
        fill="#D8989A", opacity=35, stroke=NONE)

# --- name + role ------------------------------------------------------------------
d.text("SOFT GREEN SEALIE", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#DDE8DC", justify="center")
d.text(" ".join("LIVE SURFACE REASSURANCE"), "Role", x=500, y=968, size=23,
       font="Virelai Sans", color="#A0B8A8", justify="center")

d.finish("229.soft-green-sealie-V1R00")
