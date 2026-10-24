#!/usr/bin/env python3
"""Blue poison dart frog — field-guide plate V1R00. A sapphire on the leaf
litter: side profile, sitting up on a stiff front arm, hind leg folded under,
toe pads spread on a fallen leaf. Aposematic blue peppered with black.
Rainforest-floor plate: mist, drips, litter closing on the disc's own arc.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math, re, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Blue Poison Dart Frog — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420          # plate disc centre + radius
INK = "#0A1018"
rng = random.Random(41)

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def on_disc(x, y, pad=0):
    return math.hypot(x - CX, y - CY) <= R - pad

BG_GRAD = lin(0, 0, 0, 1000, (0, "#0C1410"), (1, "#020504"))
PLATE_GRAD = rad((0, "#627454"), (0.55, "#3C4A38"), (1, "#1A2418"))
FLOOR_GRAD = lin(0, 730, 0, 880, (0, "#33301E"), (1, "#12100A"))
LEAF_GRAD = lin(0, 620, 0, 720, (0, "#56763E"), (1, "#223418"))
FROG_GRAD = rad((0, "#58A4F2"), (0.55, "#2A72DC"), (1, "#0F3C96"))
BELLY_GRAD = lin(0, 560, 0, 660, (0, "#1E58B8"), (1, "#0C2E6E"))

# --- backdrop + plate ------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#6A7E5C", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#24301E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#CBDCC0", strokeWidth=3, opacity=35)
# canopy gloom: broad soft bands of green dark
for i, dd in enumerate(["M140,180 C340,150 560,158 800,190",
                        "M110,300 C320,276 590,282 850,308"]):
    d.path(dd, f"Gloom band {i+1}", fill=NONE, stroke="#0E1A12",
           strokeWidth=44, opacity=14, cap="round")
# the drip: raindrops falling through the plate
for i, (x, y, ln) in enumerate([(260,150,110),(420,110,80),(620,120,95),(760,170,80),
                                (320,300,70),(700,320,75)]):
    assert on_disc(x, y, 25) and on_disc(x, y + ln, 25), (x, y)
    d.path(f"M{x},{y} L{x},{y + ln}", f"Drip streak {i+1}",
           fill=NONE, stroke="#BCD8D0", strokeWidth=1.6, opacity=16, cap="round")
    d.shape("ellipse", f"Drip bead {i+1}", x=x - 2.5, y=y + ln - 4, width=5, height=7,
            fill="#D8EAE2", opacity=35, stroke=NONE)
# motes and drifting spores
for i, (x, y, w) in enumerate([(200,220,5),(780,200,6),(170,430,6),(840,410,6),(300,130,5),
                               (700,140,5),(230,540,5),(820,560,5),(420,110,4),(580,150,4)]):
    assert on_disc(x + w/2, y + w/2, 8), (x, y)
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#DCE8CE", opacity=40, stroke=NONE)

# --- leaf litter floor, closing on the disc's own arc ------------------------------
fy = 735
fdx = math.sqrt(R * R - (fy - CY) ** 2)
x0, x1 = CX - fdx, CX + fdx
d.path(f"M{x0:.1f},{fy} C320,727 680,727 {x1:.1f},{fy} "
       f"A{R},{R} 0 0 1 {x0:.1f},{fy} Z", "Floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{x0 + 4:.1f},{fy} C320,727 680,727 {x1 - 4:.1f},{fy}",
       "Floor sheen", fill=NONE, stroke="#9AA884", strokeWidth=3, opacity=25, cap="round")
# litter silhouettes: a few curled dead leaves lying flat
for i, (x, y, w, rot) in enumerate([(230, 775, 90, 20), (340, 810, 70, -15), (690, 790, 85, 10),
                                    (790, 760, 60, -25), (560, 820, 75, 8)]):
    d.path(f"M{x},{y} Q{x + w*0.4},{y - w*0.28} {x + w},{y} Q{x + w*0.5},{y + w*0.2} {x},{y} Z",
           f"Litter leaf {i+1}", fill="#3A3A22", opacity=55, stroke=NONE)
    d.path(f"M{x + 6},{y - 2} L{x + w - 6},{y - 2}", f"Litter vein {i+1}",
           fill=NONE, stroke="#565230", strokeWidth=2, opacity=45)
# wet pinpricks on the litter
for i, (x, y) in enumerate([(280,760),(450,745),(620,758),(740,742),(530,790),(370,770)]):
    d.shape("ellipse", f"Wet glint {i+1}", x=x - 4, y=y - 2, width=8, height=4,
            fill="#D8E8DC", opacity=30, stroke=NONE)

# --- the leaf under the frog -----------------------------------------------------------
# a broad glossy leaf, stem end left, tip dipping right
d.path("M320,668 C340,630 420,612 520,616 C620,620 700,646 726,682 "
       "C700,712 610,724 510,722 C420,720 344,700 320,668 Z",
       "Leaf", fill=LEAF_GRAD, stroke="#162410", strokeWidth=4)
d.path("M336,664 C430,640 600,648 712,680", "Leaf midrib",
       fill=NONE, stroke="#7E9A5C", strokeWidth=3.5, opacity=60, cap="round")
for i, (x1_, y1_, x2_, y2_) in enumerate([(400,652,380,666),(470,646,462,670),(540,646,544,672),
                                          (610,652,626,676),(670,662,690,684)]):
    d.path(f"M{x1_},{y1_} L{x2_},{y2_}", f"Leaf vein {i+1}",
           fill=NONE, stroke="#6E8C50", strokeWidth=2, opacity=40, cap="round")
d.path("M340,650 C420,626 560,628 660,654", "Leaf sheen",
       fill=NONE, stroke="#C2DCA0", strokeWidth=8, opacity=18, cap="round")
# one bead of water standing on the leaf
d.shape("ellipse", "Standing drop", x=660, y=664, width=14, height=10,
        fill=rad((0, "#E4F2EE"), (1, "#8FB4AE")), stroke="#223A34", strokeWidth=1.5)
d.shape("ellipse", "Drop glint", x=664, y=666, width=4, height=3, fill="#FFFFFF",
        opacity=90, stroke=NONE)

# --- the frog: side profile facing left -------------------------------------------------
# soft contact shadow on the leaf first, then the dome
d.shape("ellipse", "Contact shadow", x=380, y=650, width=280, height=26,
        fill="#101808", opacity=35, stroke=NONE)
# body dome: snout low-left, convex back, rounded rump, belly tucked
BODY = ("M344,564 C340,538 352,508 384,486 C420,460 470,444 522,448 "
        "C584,452 640,486 660,534 C674,566 668,596 646,612 "
        "C610,634 540,642 478,634 C424,626 380,606 358,580 "
        "C350,574 345,570 344,564 Z")
d.path(BODY, "Body", fill=FROG_GRAD, stroke=INK, strokeWidth=6)
# belly shade: darker blue low on the body
d.path("M368,584 C420,616 520,630 610,614 C640,608 658,596 664,580 "
       "C668,598 660,612 646,624 C610,644 540,650 478,640 "
       "C430,632 390,612 368,584 Z", "Belly shade", fill=BELLY_GRAD, opacity=55, stroke=NONE)
# glossy sheen across the dome
d.path("M390,510 C430,478 490,462 548,468", "Back sheen",
       fill=NONE, stroke="#CFE4FC", strokeWidth=14, opacity=28, cap="round")
d.path("M400,502 C436,474 488,462 538,468", "Back sheen core",
       fill=NONE, stroke="#EAF4FE", strokeWidth=5, opacity=40, cap="round")

# the black speckle: irregular aposematic spots over the dome
rng2 = random.Random(7)
spots = []
for k in range(26):
    x = 380 + rng2.uniform(0, 270)
    y = 455 + rng2.uniform(0, 150)
    # keep inside a loose dome window
    if (x - 520)**2 / 160**2 + (y - 540)**2 / 110**2 > 1:
        continue
    r = rng2.uniform(5, 13)
    spots.append((x, y, r))
    d.path(f"M{x - r},{y} C{x - r},{y - r*0.7} {x - r*0.4},{y - r} {x},{y - r*0.9} "
           f"C{x + r*0.8},{y - r*0.8} {x + r},{y - r*0.2} {x + r*0.9},{y + r*0.3} "
           f"C{x + r*0.7},{y + r*0.9} {x - r*0.5},{y + r*0.8} {x - r},{y} Z",
           f"Spot {k+1}", fill="#0A1420", opacity=80, stroke=NONE)

# loreal mask: the dark patch sweeping from the eye down to the jaw
d.path("M360,500 C378,482 408,478 428,490 C440,500 442,522 434,540 "
       "C424,558 402,566 380,562 C362,556 352,540 354,522 C355,514 357,506 360,500 Z",
       "Loreal mask", fill="#0A1420", opacity=70, stroke=NONE)
# tympanum: faint circle behind the eye
d.shape("ellipse", "Tympanum", x=424, y=512, width=24, height=24,
        fill="#1A4A9E", opacity=45, stroke="#0A2A60", strokeWidth=2)

# the eye: big dark bead on the side of the head
d.shape("ellipse", "Eye rim", x=378, y=486, width=40, height=38,
        fill="#0A1420", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Iris", x=384, y=491, width=28, height=27,
        fill=rad((0, "#2A3A50"), (0.7, "#14202E"), (1, "#0A1018")), stroke=NONE)
d.shape("ellipse", "Eye glint", x=389, y=495, width=7, height=7,
        fill="#FFFFFF", opacity=90, stroke=NONE)
d.shape("ellipse", "Eye glint 2", x=401, y=508, width=3.5, height=3.5,
        fill="#BCD8F0", opacity=60, stroke=NONE)
# brow ridge over the eye
d.path("M370,492 C382,478 402,474 418,482", "Brow ridge",
       fill=NONE, stroke=INK, strokeWidth=4, opacity=55, cap="round")
# nostril + mouth line
d.shape("ellipse", "Nostril", x=348, y=556, width=6, height=5, fill="#2A4468", stroke=NONE)
d.path("M350,566 C378,574 408,576 434,570", "Mouth line",
       fill=NONE, stroke="#BCD8F0", strokeWidth=3.5, opacity=45, cap="round")

# front arm: stiff column propping the front up, hand splayed on the leaf
d.path("M426,556 C424,584 426,614 430,640 C432,652 438,658 448,658 "
       "C452,646 450,620 450,596 C450,576 448,562 446,556 Z",
       "Foreleg", fill=FROG_GRAD, stroke=INK, strokeWidth=4)
d.path("M432,572 C432,600 434,622 438,642", "Foreleg sheen",
       fill=NONE, stroke="#BCD8F0", strokeWidth=3, opacity=35, cap="round")
# hand + toe pads
d.path("M430,652 C440,660 456,664 472,664 C478,660 476,652 468,650 "
       "C456,648 442,648 430,652 Z", "Hand", fill=FROG_GRAD, stroke=INK, strokeWidth=3)
for i, (x, y) in enumerate([(452,662),(464,664),(442,660)]):
    d.shape("ellipse", f"Finger pad {i+1}", x=x - 5, y=y - 4, width=10, height=8,
            fill="#3E8AE4", stroke=INK, strokeWidth=2)

# hind leg folded under: thigh mass at the flank, shank tucked, long foot forward
d.path("M560,560 C600,556 636,570 650,596 C660,616 656,636 640,644 "
       "C612,652 576,644 556,622 C542,606 540,578 560,560 Z",
       "Thigh", fill=FROG_GRAD, stroke=INK, strokeWidth=5)
d.path("M572,580 C596,574 624,582 640,600", "Thigh sheen",
       fill=NONE, stroke="#CFE4FC", strokeWidth=6, opacity=25, cap="round")
for k, (x, y, r) in enumerate([(596,596,9),(620,606,8),(578,614,8),(606,624,7)]):
    d.shape("ellipse", f"Thigh spot {k+1}", x=x - r, y=y - r*0.7, width=r*2, height=r*1.4,
            fill="#0A1420", opacity=80, stroke=NONE)
# shank tucked under the thigh pointing forward
d.path("M636,634 C600,648 560,652 524,650 C516,644 518,636 528,634 "
       "C564,630 600,626 636,634 Z", "Shank", fill=FROG_GRAD, stroke=INK, strokeWidth=3.5)
# the long foot stretching forward on the leaf, toe pads spread
d.path("M524,646 C506,654 488,660 470,662 C464,658 466,650 474,648 "
       "C492,646 508,644 524,646 Z", "Foot", fill=FROG_GRAD, stroke=INK, strokeWidth=3)
for i, (x, y) in enumerate([(468,662),(482,666),(496,668)]):
    d.shape("ellipse", f"Toe pad {i+1}", x=x - 5, y=y - 4, width=10, height=8,
            fill="#3E8AE4", stroke=INK, strokeWidth=2)

# --- caption ---------------------------------------------------------------------------
r1 = d.text("BLUE POISON DART FROG", "Name", x=500, y=938, size=42, font="Virelai Sans",
            color="#D8E8DC", justify="center")
LINE2, SZ2, TRK = "DENDROBATES TINCTORIUS", 22, 150
r = d.text(LINE2, "Second line", x=500, y=974, size=SZ2, font="Virelai Sans",
           color="#9AB4A0", justify="center")
d.cmd("text.setStyle", "Second line tracking", id=r["id"], tracking=TRK)

def find(o, oid):
    if isinstance(o, dict):
        if o.get("id") == oid and "bounds" in o: return o
        o = list(o.values())
    if isinstance(o, list):
        for v in o:
            hit = find(v, oid)
            if hit: return hit
layers = d.call("inspect_document", {}, "inspect")["layers"]
for rr, lim in ((r1, 800), (r, 760)):
    b = find(layers, rr["id"])["bounds"]
    print("caption bounds", {k: round(v) for k, v in b.items()})
    assert b["width"] <= lim and b["x"] >= 100 and b["y"] + b["height"] <= 990, b

d.finish("blue-poison-dart-frog-V1R00")
