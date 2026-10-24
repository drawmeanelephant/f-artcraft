#!/usr/bin/env python3
"""Scarlet macaw — field plate V1R00. Primary colors, primary volume: a macaw
clinging upright to a riverbank clay lick, bill pressed to the clay, long red
tail braced down the bank face. Canopy plate, clay-lick mood — dappled gold
light in the gloom above, distant macaws circling, the eroded bank closing on
the disc's own arc. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Scarlet Macaw — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420          # plate disc centre + radius
INK = "#1C0E08"                    # warm dark ink, never pure black

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    ss = []
    for s in stops:
        st = {"offset": s[0], "color": s[1]}
        if len(s) > 2: st["opacity"] = s[2]
        ss.append(st)
    return {"gradient": {"kind": "radial", "stops": ss}}

def rim_x(y, r=R, side=-1):
    return CX + side * math.sqrt(r * r - (y - CY) ** 2)

def on_disc(x, y, pad=0, r=R):
    return math.hypot(x - CX, y - CY) <= r - pad

BG_GRAD    = lin(0, 0, 0, 1000, (0, "#0B1309"), (1, "#030603"))
PLATE_GRAD = rad((0, "#AEBE7E"), (0.55, "#5F7442"), (1, "#22311A"))
BANK_GRAD  = lin(0, 500, 0, 880, (0, "#B87A48"), (0.5, "#7E4A26"), (1, "#3E2210"))
RED_GRAD   = lin(600, 460, 520, 720, (0, "#E8482C"), (0.55, "#C02414"), (1, "#7E130A"))
WING_GRAD  = lin(575, 515, 535, 745,
                 (0, "#E8482C"), (0.40, "#CE2A16"),
                 (0.48, "#F2C03A"), (0.66, "#E8A824"),
                 (0.74, "#2C5AD0"), (1, "#1A3E92"))
TAIL_GRAD  = lin(520, 660, 445, 835, (0, "#D03420"), (0.7, "#A01E10"), (1, "#6E1008"))

# --- backdrop + canopy plate ----------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=64, y=24, width=872, height=872,
        fill="#5F7442", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#1B2812", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8E2B4", strokeWidth=3, opacity=30)

# dappled gold light falling from the canopy gap, fading before the rim
d.shape("ellipse", "Canopy light", x=270, y=110, width=380, height=240,
        fill=rad((0, "#E8DCA0", 30), (0.6, "#E8DCA0", 12), (1, "#E8DCA0", 0)), stroke=NONE)
d.shape("ellipse", "Light pool 2", x=580, y=300, width=220, height=140,
        fill=rad((0, "#D8D094", 18), (1, "#D8D094", 0)), stroke=NONE)

# canopy silhouettes — leaf sprays hanging in from the top of the disc
for i, (x, y, s) in enumerate([(190, 215, 1), (285, 150, -1), (760, 160, 1), (800, 230, -1)]):
    assert on_disc(x, y, 20), (x, y)
    for k in range(3):
        lx, ly = x + k * 22 * s, y + k * 14
        d.path(f"M{lx},{ly} C{lx + 14*s},{ly - 8} {lx + 26*s},{ly + 2} {lx + 30*s},{ly + 16} "
               f"C{lx + 16*s},{ly + 18} {lx + 4*s},{ly + 10} {lx},{ly} Z",
               f"Leaf {i*3+k+1}", fill="#16220F", opacity=55, stroke=NONE)
# a liana swaying down the left side
d.path("M206,168 C214,220 200,280 186,336 C178,372 180,406 194,432",
       "Liana", fill=NONE, stroke="#243019", strokeWidth=5, opacity=50, cap="round")

# distant macaws circling over the river — small red silhouettes, long tails
for i, (x, y, s) in enumerate([(300, 250, 1), (380, 210, -1), (710, 235, 1)]):
    assert on_disc(x, y, 15), (x, y)
    d.path(f"M{x},{y} C{x + 8*s},{y - 5} {x + 20*s},{y - 5} {x + 27*s},{y} "
           f"C{x + 18*s},{y + 4} {x + 7*s},{y + 4} {x},{y} Z",
           f"Far macaw body {i+1}", fill="#8E2A18", opacity=55, stroke=NONE)
    d.path(f"M{x + 4*s},{y} C{x + 12*s},{y - 13} {x + 26*s},{y - 15} {x + 36*s},{y - 9}",
           f"Far macaw wing {i+1}", fill=NONE, stroke="#8E2A18",
           strokeWidth=4, opacity=55, cap="round")
    d.path(f"M{x - 2*s},{y + 2} L{x - 30*s},{y + 13}",
           f"Far macaw tail {i+1}", fill=NONE, stroke="#8E2A18",
           strokeWidth=4, opacity=55, cap="round")

# --- the clay lick: an eroded riverbank face closing on the disc's own arc --------
ly = 505
ll = rim_x(ly, side=-1)
lr = rim_x(560, side=1)
d.path(f"M{ll:.1f},{ly} C240,478 380,502 500,518 C620,534 780,540 {lr:.1f},560 "
       f"A{R},{R} 0 0 1 {ll:.1f},{ly} Z", "Clay bank", fill=BANK_GRAD, stroke=NONE)
# sunlit eroded rim line along the bank top
d.path(f"M{ll + 6:.1f},{ly} C240,478 380,502 500,518 C620,534 780,540 {lr - 6:.1f},560",
       "Bank rim light", fill=NONE, stroke="#E0A86A", strokeWidth=5, opacity=45, cap="round")
# strata bands across the face — old flood lines in the clay
for i, dd in enumerate(["M180,600 C340,588 560,600 800,622",
                        "M170,690 C330,676 570,690 810,710",
                        "M260,782 C420,772 580,782 740,794"]):
    d.path(dd, f"Stratum {i+1}", fill=NONE, stroke="#5A3218",
           strokeWidth=6, opacity=40, cap="round")
# darker damp seam low on the face
d.path("M310,824 C420,814 580,824 690,834", "Damp seam", fill=NONE,
       stroke="#2E1A0C", strokeWidth=10, opacity=35, cap="round")
# grass tufts and roots hanging over the lip
for i, (x, y, s) in enumerate([(150, 500, 1), (300, 495, -1), (820, 545, 1)]):
    for k in (-1, 0, 1):
        d.path(f"M{x},{y} C{x + k*8 - 4},{y - 16} {x + k*10},{y - 26} {x + k*14 + s*4},{y - 34}",
               f"Tuft {i*3+k+2}", fill=NONE, stroke="#3E5222",
               strokeWidth=3.5, opacity=60, cap="round")
for i, (x, y) in enumerate([(420, 512), (700, 532)]):
    d.path(f"M{x},{y} C{x - 4},{y + 14} {x + 4},{y + 26} {x - 2},{y + 38}",
           f"Root {i+1}", fill=NONE, stroke="#4A2C12",
           strokeWidth=3, opacity=50, cap="round")
# peck pits worked into the face — the lick is mined, not just visited
for i, (x, y, w) in enumerate([(752, 548, 30), (390, 640, 22), (560, 760, 26), (250, 700, 18)]):
    d.shape("ellipse", f"Peck pit {i+1}", x=x - w/2, y=y - w/3, width=w, height=w*0.66,
            fill="#3A2010", opacity=45, stroke=NONE)
    d.shape("ellipse", f"Pit lip {i+1}", x=x - w/2, y=y - w/3 - 4, width=w, height=w*0.4,
            fill="#D89A5E", opacity=30, stroke=NONE)
# fresh clay crumbs fallen below the bill's working
for i, (x, y) in enumerate([(742, 588), (762, 596), (726, 602), (752, 610)]):
    d.shape("ellipse", f"Crumb {i+1}", x=x - 4, y=y - 4, width=8, height=8,
            fill="#8A5428", opacity=60, stroke=NONE)

# contact shadow where the body presses the clay
d.shape("ellipse", "Body shadow", x=520, y=590, width=190, height=150,
        fill=rad((0, "#2A1608", 45), (1, "#2A1608", 0)), stroke=NONE)

# === the macaw: clinging upright, tail braced below ================================
# tail first — two feathers fanned down the bank, pressed flat for a prop
d.path("M508,660 C490,706 472,756 452,812 C448,824 444,832 442,838 "
       "C454,836 464,826 472,810 C488,776 504,730 516,684 Z",
       "Tail far", fill=lin(510, 660, 450, 830, (0, "#8E1A0E"), (1, "#5E0E06")),
       stroke=INK, strokeWidth=4)
d.path("M536,664 C522,714 508,768 494,822 C492,832 492,840 494,846 "
       "C506,840 514,826 520,808 C532,770 542,720 548,676 Z",
       "Tail near", fill=TAIL_GRAD, stroke=INK, strokeWidth=4.5)
# the blue outer edge that shows on the near tail feather
d.path("M540,676 C530,724 520,776 506,826", "Tail blue edge", fill=NONE,
       stroke="#2C5AD0", strokeWidth=5, opacity=70, cap="round")

# body — upright egg angled into the bank, chest out, back to the light
d.path("M606,468 C572,474 542,498 522,532 C500,570 488,622 494,670 "
       "C498,700 514,716 538,718 C574,718 610,696 632,666 "
       "C654,636 664,598 662,566 C660,540 652,522 640,508 "
       "C628,494 614,482 606,468 Z",
       "Body", fill=RED_GRAD, stroke=INK, strokeWidth=6)
# chest light — the bird's front catching the canopy gap
d.path("M630,540 C646,576 646,624 624,664 C610,686 588,700 566,704 "
       "C596,684 614,650 620,612 C624,584 628,560 630,540 Z",
       "Chest light", fill="#F06848", opacity=50, stroke=NONE)
# back shade down the lit side away from the bank
d.path("M524,534 C504,570 494,620 500,664", "Back shade", fill=NONE,
       stroke="#7E130A", strokeWidth=10, opacity=45, cap="round")

# folded wing drooping down the body's lit side — red shoulder, yellow band,
# blue primaries; one silhouette, three colours banded along its axis
d.path("M574,516 C540,524 514,550 500,588 C488,628 490,676 508,716 "
       "C518,738 536,750 554,744 C564,706 566,656 562,610 "
       "C559,574 564,542 574,516 Z",
       "Wing", fill=WING_GRAD, stroke=INK, strokeWidth=5)
# primary separations in the blue tip
for k, (x0, x1) in enumerate([(524, 516), (536, 530), (548, 544)]):
    d.path(f"M{x0},676 C{x0 - 6},700 {x0 - 4},718 {x1},736",
           f"Primary {k+1}", fill=NONE, stroke="#122A66",
           strokeWidth=3.5, opacity=65, cap="round")
# the yellow covert band edge
d.path("M506,612 C524,626 546,630 562,622", "Band edge", fill=NONE,
       stroke="#8E6A14", strokeWidth=3, opacity=50, cap="round")

# legs + zygodactyl feet spread on the face, gripping clay knobs
for i, (x, y, dx) in enumerate([(608, 692, -14), (664, 682, 10)]):
    d.path(f"M{x},{y} C{x - 6},{y + 12} {x - 4},{y + 20} {x + dx*0.3},{y + 28}",
           f"Leg {i+1}", fill=NONE, stroke="#4A4640",
           strokeWidth=7, cap="round")
    fx, fy = x + dx * 0.3, y + 28
    for k, (tx, ty) in enumerate([(-16, 10), (-4, 14), (10, 12), (20, 6)]):
        d.path(f"M{fx},{fy} C{fx + tx*0.5},{fy + 4} {fx + tx*0.8},{fy + ty*0.7} {fx + tx},{fy + ty}",
               f"Toe {i*4+k+1}", fill=NONE, stroke="#4A4640",
               strokeWidth=5, cap="round")
        d.path(f"M{fx + tx},{fy + ty} l4,3", f"Toenail {i*4+k+1}", fill=NONE,
               stroke="#2A2620", strokeWidth=3, cap="round")
# the little clay knobs the toes close on
d.shape("ellipse", "Toe knob 1", x=596, y=726, width=26, height=14,
        fill="#5E3818", opacity=70, stroke=NONE)
d.shape("ellipse", "Toe knob 2", x=668, y=716, width=24, height=12,
        fill="#5E3818", opacity=70, stroke=NONE)

# head — the white bare face, the hooked horn bill buried in the clay
d.path("M690,522 C698,496 692,468 672,452 C650,434 618,436 600,454 "
       "C584,470 580,498 588,520 C596,540 618,552 642,550 "
       "C666,548 684,540 690,522 Z",
       "Head", fill=lin(660, 450, 610, 550, (0, "#E8482C"), (1, "#B01E12")),
       stroke=INK, strokeWidth=5)
# the bare white cheek patch from lores to under the eye
d.path("M684,512 C686,490 678,470 660,460 C642,450 620,454 608,468 "
       "C598,480 596,498 602,512 C612,504 628,500 646,502 "
       "C662,504 676,508 684,512 Z",
       "Face patch", fill="#F0EADC", opacity=95, stroke="#8E7E66", strokeWidth=2)
# fine red feather tracks fanning across the white skin
for k in range(4):
    d.path(f"M614,{478 + k*9} C{636},{474 + k*8} {656},{478 + k*8} {676},{490 + k*6}",
           f"Face track {k+1}", fill=NONE, stroke="#C02414",
           strokeWidth=2, opacity=70, cap="round")
# eye — dark bead set in the skin
d.shape("ellipse", "Eye", x=640, y=484, width=15, height=15,
        fill="#1A0E08", stroke=NONE)
d.shape("ellipse", "Eye glint", x=644, y=487, width=4, height=4,
        fill="#FFF6DC", opacity=85, stroke=NONE)

# the great pale bill, tip pressed into a peck pit
d.path("M672,470 C700,458 730,462 748,480 C760,494 762,512 754,524 "
       "C744,536 728,540 716,534 C722,522 720,508 708,498 "
       "C696,488 682,482 672,470 Z",
       "Upper bill", fill=lin(700, 465, 730, 535, (0, "#EDE4CC"), (0.7, "#C9BC98"), (1, "#9C8E6E")),
       stroke=INK, strokeWidth=4)
# dark lower mandible tucked under
d.path("M692,522 C706,528 718,534 726,542 C714,546 700,542 692,534 Z",
       "Lower bill", fill="#2A2118", stroke=INK, strokeWidth=3)
# bill sheen along the culmen
d.path("M680,476 C702,466 724,468 742,482", "Culmen light", fill=NONE,
       stroke="#FBF6E4", strokeWidth=3.5, opacity=60, cap="round")
# nostril dot
d.shape("ellipse", "Nostril", x=694, y=488, width=6, height=6,
        fill="#4A3E2C", opacity=80, stroke=NONE)

# stray feather down stuck to the clay beside the working — scale tell
d.path("M780,660 C790,670 798,682 802,696 C792,690 782,678 780,660 Z",
       "Shed feather", fill="#C02414", opacity=70, stroke=NONE)

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#141F0C", strokeWidth=6)

# --- name ---------------------------------------------------------------------------
r1 = d.text("SCARLET MACAW", "Name", x=500, y=962, size=58, font="Virelai Sans",
            color="#E2E8C0", justify="center")

def find(o, oid):
    if isinstance(o, dict):
        if o.get("id") == oid and "bounds" in o: return o
        o = list(o.values())
    if isinstance(o, list):
        for v in o:
            hit = find(v, oid)
            if hit: return hit
layers = d.call("inspect_document", {}, "inspect")["layers"]
b = find(layers, r1["id"])["bounds"]
print("name bounds", {k: round(v) for k, v in b.items()})
assert b["width"] <= 800 and b["x"] >= 100 and b["y"] + b["height"] <= 990, b

d.finish("scarlet-macaw-V1R00")
