#!/usr/bin/env python3
"""American alligator — field plate V1R00. The comeback reptile, armored and
patient: an ambush float, eyes and the broad U-snout held just above the
tannin water, a low scute ridge trailing off to the right. Bayou plate,
cypress-knee mood — woody knees standing in the water, spanish moss
letting down from the rim. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("American Alligator — Field Plate", 1000, 1000)
rng = random.Random(19)

CX, CY, R = 500, 460, 420          # plate disc centre + radius
INK = "#0E0D08"                    # warm dark ink, never pure black

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

BG_GRAD    = lin(0, 0, 0, 1000, (0, "#0A0E08"), (1, "#030402"))
PLATE_GRAD = rad((0, "#4A5A38"), (0.55, "#2A361E"), (1, "#0E140A"))
WATER_GRAD = lin(0, 650, 0, 890, (0, "#2A3822"), (0.5, "#16200F"), (1, "#080D05"))
KNEE_GRAD  = lin(0, 480, 0, 700, (0, "#6A4E32"), (0.6, "#45311E"), (1, "#221708"))
SKIN_GRAD  = lin(0, 420, 0, 660, (0, "#5A6238"), (0.5, "#3C4426"), (1, "#1E2412"))
RIDGE_GRAD = lin(560, 480, 780, 640, (0, "#4A522E"), (1, "#1A2010"))

# --- backdrop + bayou plate ---------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=64, y=24, width=872, height=872,
        fill="#4A5A38", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#18220F", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C4CE9E", strokeWidth=3, opacity=26)

# a dim shaft through the canopy, fading before the rim
d.shape("ellipse", "Bayou light", x=310, y=130, width=360, height=250,
        fill=rad((0, "#D8DCAE", 15), (0.6, "#D8DCAE", 6), (1, "#D8DCAE", 0)), stroke=NONE)
# drifting pollen / duckweed motes on the air
for i in range(24):
    a = rng.uniform(0, math.tau); rr = math.sqrt(rng.uniform(0, 1)) * 380
    x, y = CX + rr * math.cos(a), CY + rr * math.sin(a)
    if y > 640: continue
    w = rng.uniform(3, 7)
    d.shape("ellipse", f"Mote {i+1}", x=x - w/2, y=y - w/2, width=w, height=w,
            fill="#9AAE6E", opacity=rng.uniform(12, 26), stroke=NONE)

# --- spanish moss letting down from the upper rim ------------------------------
for i, (x0, y0, sw, ln_) in enumerate([
        (rim_x(150, side=-1), 150, -18, 130), (rim_x(108, side=-1) + 36, 108, -8, 170),
        (rim_x(196, side=-1) + 10, 196, -24, 95), (rim_x(140, side=1), 140, 16, 140),
        (rim_x(96, side=1) - 30, 96, 6, 110)]):
    x1, y1 = x0 + sw, y0 + ln_
    assert on_disc(x0, y0, -10) and on_disc(x1, y1, 12), (x0, y0, x1, y1)
    d.path(f"M{x0:.1f},{y0:.1f} C{x0 + sw*0.3:.0f},{y0 + ln_*0.4:.0f} "
           f"{x1 - sw*0.2:.0f},{y1 - ln_*0.3:.0f} {x1:.0f},{y1:.0f}",
           f"Moss {i+1}", fill=NONE, stroke="#6E7E58", strokeWidth=5,
           opacity=55, cap="round")
    for j in range(2):  # side strands off each curtain
        mx_, my_ = x0 + sw*0.4, y0 + ln_*(0.45 + j*0.25)
        d.path(f"M{mx_:.0f},{my_:.0f} L{mx_ + sw*0.5 + (4 if j else -4):.0f},{my_ + 26:.0f}",
               f"Moss strand {i+1}.{j+1}", fill=NONE, stroke="#6E7E58",
               strokeWidth=2.5, opacity=40, cap="round")

# --- cypress knees standing in the water (drawn before the surface so their
# bases submerge) ---------------------------------------------------------------
def knee(x, base, top, half, label):
    d.path(f"M{x - half},{base} "
           f"C{x - half - 4},{base - 60} {x - half*0.5},{top + 46} {x - 6},{top + 16} "
           f"C{x - 2},{top} {x + 8},{top + 4} {x + 12},{top + 22} "
           f"C{x + half*0.7},{top + 60} {x + half + 6},{base - 70} {x + half},{base} Z",
           label, fill=KNEE_GRAD, stroke=INK, strokeWidth=3)
    # wood grain + a moss flecked crown
    d.path(f"M{x - 4},{top + 30} C{x - 6},{top + 90} {x - 4},{base - 40} {x - 2},{base - 10}",
           f"{label} grain", fill=NONE, stroke="#2A1C0E", strokeWidth=3,
           opacity=50, cap="round")
    d.path(f"M{x - 8},{top + 12} C{x - 2},{top + 2} {x + 10},{top + 6} {x + 12},{top + 20}",
           f"{label} crown moss", fill=NONE, stroke="#7E9058", strokeWidth=4,
           opacity=60, cap="round")

knee(252, 712, 500, 30, "Knee L1")
knee(310, 700, 545, 24, "Knee L2")
knee(722, 706, 540, 27, "Knee R")

# --- the tannin water: surface crest ~y652, bottom closes on the disc arc ------
wy = 652
wdx = math.sqrt(R * R - (wy - CY) ** 2)
d.path(f"M{CX-wdx:.1f},{wy} C300,644 420,656 540,650 C640,646 720,654 {CX+wdx:.1f},{wy} "
       f"A{R},{R} 0 0 1 {CX-wdx:.1f},{wy} Z", "Water", fill=WATER_GRAD, stroke=NONE)
d.path(f"M{CX-wdx+8:.1f},{wy-2} C310,644 430,652 540,646 C640,642 720,650 {CX+wdx-8:.1f},{wy-2}",
       "Water light", fill=NONE, stroke="#AEBE8A", strokeWidth=4, opacity=35, cap="round")
# knee reflections: soft vertical streaks under each knee
for i, (x, w_) in enumerate([(252, 30), (310, 24), (722, 27)]):
    d.shape("ellipse", f"Reflection {i+1}", x=x - w_, y=662, width=w_*2, height=120,
            fill=lin(0, 662, 0, 782, (0, "#3E3220"), (1, "#3E3220")),
            opacity=25, stroke=NONE)
# duckweed flecks on the surface
for i, (x, y, w) in enumerate([(200,690,14),(280,730,10),(640,700,12),(760,690,9),
                               (380,760,8),(580,740,10),(700,790,7),(300,800,9)]):
    assert on_disc(x, y, 12), (x, y)
    d.shape("ellipse", f"Duckweed {i+1}", x=x, y=y, width=w, height=w*0.45,
            fill="#6E8A4A", opacity=55, stroke=NONE)

# --- the gator: profile float, snout left, ridge trailing right ----------------
# the head mass in profile: long flat U-snout, raised nostril dome at the tip,
# raised eye orbit behind it — the signature ambush silhouette
d.path("M322,540 C318,522 330,506 350,502 "
       "C390,492 440,486 486,482 C530,478 566,478 596,488 "
       "C646,504 680,530 692,562 C700,586 696,612 682,630 "
       "C640,646 560,652 480,650 C410,648 352,636 336,612 "
       "C324,594 320,566 322,540 Z",
       "Head", fill=SKIN_GRAD, stroke=INK, strokeWidth=4)
# nostril dome raised on the snout tip — the first thing above water
d.path("M330,514 C326,498 336,486 352,484 C368,482 380,492 380,508 "
       "C380,520 368,528 352,528 C340,528 332,524 330,514 Z",
       "Nostril dome", fill=rad((0, "#6E7644"), (1, "#3A4222")), stroke=INK, strokeWidth=3)
for i, (nx, ny) in enumerate([(344, 498), (364, 496)]):
    d.shape("ellipse", f"Nostril {i+1}", x=nx-5, y=ny-3, width=10, height=6,
            fill="#14180C", stroke=INK, strokeWidth=1.5)
# raised eye orbit: a dome on the skull line, amber eye riding the front slope
d.path("M512,486 C508,452 522,428 548,426 C574,424 592,444 592,474 "
       "C580,488 528,492 512,486 Z",
       "Orbit", fill=SKIN_GRAD, stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Eye", x=528, y=438, width=26, height=22,
        fill="#C8963C", stroke=INK, strokeWidth=2.5)
d.shape("ellipse", "Pupil", x=538, y=439, width=7, height=20,
        fill="#12140A", stroke=NONE)
d.shape("ellipse", "Eye glint", x=533, y=441, width=5, height=5,
        fill="#F0E4B8", opacity=85, stroke=NONE)
# brow ridge running back over the orbit into the skull
d.path("M560,448 C590,450 616,462 634,480", "Brow ridge", fill=NONE,
       stroke="#14180C", strokeWidth=5, opacity=50, cap="round")
# the long closed jaw seam from snout tip, tipping up at the hinge — the smile
d.path("M336,556 C400,584 480,592 560,588 C614,584 656,570 680,548",
       "Jaw seam", fill=NONE, stroke="#14180C", strokeWidth=4.5, cap="round")
d.path("M336,552 C340,544 348,538 358,536", "Snout tip line", fill=NONE,
       stroke="#14180C", strokeWidth=3.5, opacity=70, cap="round")
# a few upper teeth nubs over the seam — lower teeth tucked inside, the gator tell
for i, (x, y) in enumerate([(392,572),(424,580),(456,584),(488,586)]):
    d.path(f"M{x-8},{y} L{x},{y+11} L{x+8},{y} Z",
           f"Tooth {i+1}", fill="#D8CEAA", stroke=INK, strokeWidth=2)
# scute table behind the orbit, then the neck rows
for i, (x, y, s) in enumerate([(606,506,9),(634,518,10),(586,530,9),
                               (614,548,10),(644,556,9),(566,556,8)]):
    d.path(f"M{x-s},{y+5} L{x},{y-7} L{x+s},{y+5} Z",
           f"Neck scute {i+1}", fill="#464F2A", opacity=85, stroke=NONE)
# the trailing back: dorsal scute bumps sinking into the water to the right
d.path("M640,570 C700,584 760,612 806,638 C792,652 740,656 700,648 "
       "C664,640 646,612 640,570 Z",
       "Back ridge", fill=RIDGE_GRAD, stroke=INK, strokeWidth=3)
for i, (x, y, s) in enumerate([(676,592,13),(716,610,14),(752,626,12),(784,640,10)]):
    d.path(f"M{x-s},{y+6} L{x},{y-10} L{x+s},{y+6} Z",
           f"Back scute {i+1}", fill="#3A4224", stroke=INK, strokeWidth=2)

# surface tension: ripple rings around the snout, chin and knees
for i, (rx_, ry_, w_, op) in enumerate([(360,652,110,42),(470,656,200,26),(560,660,300,14),
                                      (252,668,80,30),(722,668,70,28),(310,664,60,24)]):
    d.path(f"M{rx_-w_},{ry_} C{rx_-w_*0.5},{ry_+18} {rx_+w_*0.5},{ry_+18} {rx_+w_},{ry_}",
           f"Ripple {i+1}", fill=NONE, stroke="#AEBE8A", strokeWidth=3,
           opacity=op, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#080C05", strokeWidth=6)

# --- name ----------------------------------------------------------------------
r1 = d.text("AMERICAN ALLIGATOR", "Name", x=500, y=962, size=52, font="Virelai Sans",
            color="#C8D2A0", justify="center")

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

d.finish("american-alligator-V1R00")
