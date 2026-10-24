#!/usr/bin/env python3
"""Proxy Compassion Possum — mascot portrait V1R00. mascots/M-0228.
Possum smiling and nodding beside a locked gate, printed apology slips
stacked at the entrance. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Proxy Compassion Possum — Mascot Portrait", 1000, 1000)

INK = "#26202C"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#141826"}, {"offset": 1, "color": "#080A12"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#BCC8C0"}, {"offset": 0.7, "color": "#7E8C8A"},
    {"offset": 1, "color": "#46505C"}]}}
FUR_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#A8AEBA"}, {"offset": 0.7, "color": "#7C8290"},
    {"offset": 1, "color": "#565A6C"}]}}
FACE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F2EADC"}, {"offset": 1, "color": "#D8C8B4"}]}}
GATE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4A5064"}, {"offset": 1, "color": "#2C3040"}]}}
LOCK_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#D8B25E"}, {"offset": 1, "color": "#96702E"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#4E5A64", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#DCE4DC", strokeWidth=3, opacity=55)
# corridor haze — the institution's soft, evenly-lit nowhere
for i, (x, y, w, h) in enumerate([(250,190,180,60),(620,150,220,64),(300,500,140,44)]):
    d.shape("ellipse", f"Haze {i+1}", x=x, y=y, width=w, height=h,
            fill="#E6ECE4", opacity=14, stroke=NONE)

# --- floor, ends on the disc's own arc -----------------------------------------
d.path("M200,730 C330,720 670,720 800,730 A420,420 0 0 1 200,730 Z",
       "Floor", fill="#5E6A66", opacity=55, stroke=NONE)
d.path("M200,730 C330,720 670,720 800,730", "Floor edge",
       fill=NONE, stroke="#3A4442", strokeWidth=4, opacity=70, cap="round")

# --- the locked gate, right of centre -------------------------------------------
d.shape("ellipse", "Gate shadow", x=600, y=742, width=200, height=20,
        fill="#38404A", opacity=40, stroke=NONE)
# darkness beyond the bars
d.path("M618,330 L782,330 L782,742 L618,742 Z", "Beyond",
       fill="#232833", opacity=80, stroke=NONE)
# posts
d.shape("rectangle", "Post L", x=606, y=306, width=22, height=440,
        radius=6, fill=GATE_GRAD, stroke=INK, strokeWidth=5)
d.shape("rectangle", "Post R", x=772, y=306, width=22, height=440,
        radius=6, fill=GATE_GRAD, stroke=INK, strokeWidth=5)
# top and mid rails
d.shape("rectangle", "Rail top", x=606, y=330, width=188, height=20,
        radius=6, fill=GATE_GRAD, stroke=INK, strokeWidth=4)
d.shape("rectangle", "Rail mid", x=606, y=540, width=188, height=16,
        radius=5, fill=GATE_GRAD, stroke=INK, strokeWidth=4)
# bars
for i, x in enumerate([648, 686, 724, 762]):
    d.shape("rectangle", f"Bar {i+1}", x=x, y=306, width=14, height=436,
            radius=5, fill=GATE_GRAD, stroke=INK, strokeWidth=3)
# finials on the posts — ceremonial, unhelpful
for i, x in enumerate([617, 783]):
    d.shape("ellipse", f"Finial {i+1}", x=x-11, y=288, width=22, height=22,
            fill=GATE_GRAD, stroke=INK, strokeWidth=4)
# the padlock, front and centre on the mid rail — the only honest object here
d.path("M686,540 C686,516 694,502 705,502 C716,502 724,516 724,540",
       "Shackle", fill=NONE, stroke="#B8944E", strokeWidth=8, cap="round")
d.shape("rectangle", "Padlock", x=678, y=536, width=54, height=50,
        radius=8, fill=LOCK_GRAD, stroke=INK, strokeWidth=5)
d.path("M705,556 L705,568 M699,568 L711,568", "Keyhole",
       fill=NONE, stroke="#4A3A20", strokeWidth=5, cap="round")

# --- apology slips: the printed warmth, stacked at the entrance ------------------
d.shape("ellipse", "Pile shadow", x=556, y=730, width=110, height=14,
        fill="#38404A", opacity=45, stroke=NONE)
# neat stack of slips, slightly fanned
for i, (dx, dy, tilt) in enumerate([(0,0,-2),(4,-10,3),(-3,-20,-4),(2,-30,2),(-2,-40,-1)]):
    x0, y0 = 566+dx, 726+dy
    d.path(f"M{x0},{y0} L{x0+86},{y0+tilt*2} L{x0+88},{y0+14+tilt} L{x0+2},{y0+14-tilt} Z",
           f"Slip {i+1}", fill="#EFE8D8", stroke=INK, strokeWidth=3, join="round")
    d.path(f"M{x0+8},{y0+7} L{x0+60},{y0+7+tilt}", f"Slip rule {i+1}",
           fill=NONE, stroke="#9A9284", strokeWidth=2.5, opacity=80)
# two slips that made it no further than the threshold
d.path("M640,744 L712,748 L710,760 L638,756 Z", "Slip fallen 1",
       fill="#E8E0CE", stroke=INK, strokeWidth=3, join="round")
d.path("M596,758 L650,762 L648,772 L594,768 Z", "Slip fallen 2",
       fill="#E4DCC8", stroke=INK, strokeWidth=3, join="round", opacity=90)

# --- the possum, beside the gate, mid-nod ------------------------------------------
d.shape("ellipse", "Possum shadow", x=330, y=736, width=190, height=22,
        fill="#38404A", opacity=45, stroke=NONE)
# tail curling along the floor behind
d.path("M372,712 C330,724 300,742 288,764 C282,776 274,782 262,784",
       "Tail", fill=NONE, stroke="#C08A8E", strokeWidth=12, cap="round")
# seated body
d.path("M370,724 C356,646 380,580 430,556 C468,538 516,544 542,578 "
       "C562,606 566,652 554,696 C548,716 536,730 522,736 L402,736 "
       "C388,732 376,728 370,724 Z",
       "Body", fill=FUR_GRAD, stroke=INK, strokeWidth=6, join="round")
# belly
d.path("M414,660 C440,690 500,700 534,678 C530,708 516,726 496,732 L430,732 "
       "C420,716 414,692 414,660 Z", "Belly", fill="#C9C2BA",
       opacity=55, stroke=NONE)
# head, tilted into the nod
d.path("M392,470 C386,414 414,370 462,362 C508,354 548,382 556,430 "
       "C562,468 548,508 516,526 C484,544 440,538 416,510 "
       "C402,496 394,484 392,470 Z",
       "Head", fill=FUR_GRAD, stroke=INK, strokeWidth=6, join="round")
# white face blaze running to the nose
d.path("M452,398 C492,392 528,414 538,452 C546,482 536,510 514,524 "
       "C492,538 462,534 444,514 C428,496 424,466 432,440 "
       "C436,422 442,408 452,398 Z",
       "Face blaze", fill=FACE_GRAD, stroke=NONE)
# ears: dark with pale rims, the left one flopped by the tilt
d.path("M400,400 C382,376 380,348 396,332 C412,316 436,320 446,340 "
       "C438,362 420,384 400,400 Z", "Ear L", fill="#4A4250",
       stroke=INK, strokeWidth=5, join="round")
d.path("M402,382 C392,364 394,346 406,338", "Ear L inner",
       fill=NONE, stroke="#C08A8E", strokeWidth=4, opacity=80, cap="round")
d.path("M520,372 C536,346 560,338 578,350 C594,362 594,388 578,404 "
       "C560,398 538,386 520,372 Z", "Ear R", fill="#4A4250",
       stroke=INK, strokeWidth=5, join="round")
d.path("M538,372 C552,356 568,352 580,360", "Ear R inner",
       fill=NONE, stroke="#C08A8E", strokeWidth=4, opacity=80, cap="round")
# the smile that arrives a half-second early: closed happy eyes, soft grin
d.path("M452,462 C458,470 470,470 476,462 M508,462 C514,470 526,470 532,462",
       "Eyes", fill=NONE, stroke=INK, strokeWidth=5, cap="round")
# pink pointed nose at the blaze's tip, above the smile
d.path("M480,482 C484,478 496,478 500,482 C499,492 496,499 490,501 "
       "C485,498 481,491 480,482 Z",
       "Nose", fill="#D8989A", stroke=INK, strokeWidth=4, join="round")
d.path("M478,506 C486,516 502,516 510,506", "Smile",
       fill=NONE, stroke=INK, strokeWidth=5, cap="round")
# nod marks — the same angle, every time
d.path("M368,430 C356,446 354,466 362,484 M346,420 C330,442 328,472 340,496",
       "Nod arcs", fill=NONE, stroke="#5A5468", strokeWidth=4,
       opacity=60, cap="round")
# forepaw extended toward the slips — offering, never opening
d.path("M528,624 C556,636 578,654 590,676", "Arm",
       fill=NONE, stroke="#7C8290", strokeWidth=20, cap="round")
d.shape("ellipse", "Paw", x=582, y=666, width=30, height=24,
        fill="#C08A8E", stroke=INK, strokeWidth=4)
d.path("M588,678 L606,676 M590,686 L606,686", "Paw toes",
       fill=NONE, stroke=INK, strokeWidth=3, opacity=70, cap="round")
# hind foot
d.shape("ellipse", "Hind foot", x=388, y=720, width=46, height=18,
        fill="#8E94A4", stroke=INK, strokeWidth=4)

# --- name + role ------------------------------------------------------------------
d.text("PROXY COMPASSION POSSUM", "Name", x=500, y=930, size=50,
       font="Virelai Sans", color="#DEE4DA", justify="center")
d.text(" ".join("CARE WITHOUT POWER"), "Role", x=500, y=968, size=23,
       font="Virelai Sans", color="#A4B2AE", justify="center")

d.finish("228.proxy-compassion-possum-V1R00")
