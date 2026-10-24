#!/usr/bin/env python3
"""Warthog — field plate V1R00. Profile facing left, head carried low on a
heavy neck: paired tusks curling up off the wide muzzle, wart bumps on the
cheek, a bristle mane along the neck, and the tail held vertical like a
signal flag off the rump. Savanna plate, termite-mound mood: dusty gold
disc, cathedral mounds rising behind, dry grass closing on the floor arc.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Warthog — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#2A1C10"   # warm near-black

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def radO(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c, "opacity": a} for o, c, a in stops]}}

def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

def disc_x(y, side):
    return PCX + side * math.sqrt(PR * PR - (y - PCY) ** 2)

def smooth(pts, closed=True):
    n = len(pts)
    s = "M%.1f,%.1f" % pts[0]
    for i in (range(n) if closed else range(n - 1)):
        p0 = pts[(i - 1) % n] if (closed or i > 0) else pts[0]
        p1, p2 = pts[i], pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (closed or i + 2 < n) else pts[-1]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        s += " C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (c1 + c2 + p2)
    return s + (" Z" if closed else "")

BG_GRAD    = lin(0, 0, 0, 1000, (0, "#1A1409"), (1, "#070503"))
PLATE_GRAD = rad((0, "#DFCB90"), (0.55, "#B0965A"), (1, "#5F4B24"))
GROUND_GRAD = lin(0, 720, 0, 880, (0, "#7E6130"), (1, "#3C2C12"))
MOUND_GRAD = lin(0, 540, 0, 790, (0, "#9A7040"), (1, "#54391B"))
SKIN_GRAD  = rad((0, "#8A7458"), (0.6, "#5E4B38"), (1, "#372A1C"))
HEAD_GRAD  = rad((0, "#94805F"), (0.65, "#66503A"), (1, "#3C2E1E"))
TUSK_GRAD  = lin(258, 580, 304, 468, (0, "#B4A480"), (0.6, "#EFE6C8"), (1, "#FFF8E0"))

# --- backdrop + plate --------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880, fill="#D8B96A", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#3E3016", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F0E2B0", strokeWidth=3, opacity=40)

# heat haze banding across the upper plate
for i, dd in enumerate(["M210,300 C360,284 560,284 720,306",
                        "M170,380 C340,362 600,362 790,388",
                        "M260,240 C400,228 540,230 660,246"]):
    d.path(dd, f"Haze {i+1}", fill=NONE, stroke="#F4E6B4",
           strokeWidth=6, opacity=14, cap="round")

# low pale sun caught in the haze, upper right inside the disc
d.shape("ellipse", "Sun glow", x=560, y=110, width=240, height=240,
        fill=radO((0, "#F8ECC0", 22), (1, "#F8ECC0", 0)), stroke=NONE)
d.shape("ellipse", "Sun", x=650, y=178, width=58, height=58,
        fill=rad((0, "#FBF2D2"), (1, "#E8CE8E")), opacity=85, stroke=NONE)

# --- distant flat-top acacia on the left horizon --------------------------------------
assert on_disc(168, 560, 8) and on_disc(240, 640, 8)
d.path("M204,674 C202,648 200,624 204,600", "Acacia trunk", fill=NONE,
       stroke="#4E3B1C", strokeWidth=5, opacity=70, cap="round")
d.path("M204,622 C190,614 178,608 168,606", "Acacia limb L", fill=NONE,
       stroke="#4E3B1C", strokeWidth=4, opacity=70, cap="round")
d.path("M204,614 C216,606 228,600 240,598", "Acacia limb R", fill=NONE,
       stroke="#4E3B1C", strokeWidth=4, opacity=70, cap="round")
d.path("M150,602 C176,582 240,580 262,600 C238,608 174,610 150,602 Z",
       "Acacia crown", fill="#5C4A20", opacity=60, stroke=NONE)

# --- termite mounds rising behind the animal ------------------------------------------
# right mound: twin cathedral spires behind the rump
d.path(smooth([(652, 788), (656, 700), (668, 620), (680, 566), (692, 548),
               (700, 584), (706, 640), (714, 560), (724, 544), (734, 600),
               (744, 700), (750, 788)]),
       "Mound R", fill=MOUND_GRAD, opacity=92, stroke=NONE)
for i, dd in enumerate(["M686,780 C682,700 684,620 692,566",
                        "M724,780 C722,700 724,640 728,580"]):
    d.path(dd, f"Mound ridge R{i+1}", fill=NONE, stroke="#3E2A10",
           strokeWidth=4, opacity=45, cap="round")
# left mound: one leaning spire
d.path(smooth([(222, 780), (226, 700), (236, 624), (244, 572), (254, 560),
               (264, 596), (274, 672), (282, 780)]),
       "Mound L", fill=MOUND_GRAD, opacity=92, stroke=NONE)
d.path("M252,780 C250,700 252,628 258,572", "Mound ridge L", fill=NONE,
       stroke="#3E2A10", strokeWidth=4, opacity=45, cap="round")
# a low distant dome between them
d.path("M400,742 C420,706 468,700 492,736 C470,750 424,752 400,742 Z",
       "Mound far", fill="#8A6A38", opacity=55, stroke=NONE)

# --- ground strip, closing on the disc's own arc ---------------------------------------
GY = 758
gl, gr = disc_x(GY, -1), disc_x(GY, 1)
d.path(f"M{gl:.1f},{GY} C300,746 420,756 520,750 C620,744 700,752 {gr:.1f},{GY} "
       f"A{PR},{PR} 0 0 1 {gl:.1f},{GY} Z", "Ground", fill=GROUND_GRAD, stroke=NONE)
d.path(f"M{gl+30:.0f},{GY+14} C380,{GY+6} 620,{GY+6} {gr-30:.0f},{GY+16}",
       "Ground shade", fill=NONE, stroke="#2E2110", strokeWidth=5, opacity=40, cap="round")

# dry grass tufts along the floor
for i, (gx, gy, s) in enumerate([(238, 748, 1), (336, 742, -1), (560, 744, 1),
                                 (648, 748, -1), (742, 744, 1)]):
    for j in range(4):
        bx = gx + j * 7 * s
        tipx = bx + (j - 1.5) * 9 * s
        tipy = gy - 40 - j * 8
        assert on_disc(tipx, tipy, 6), (tipx, tipy)
        d.path(f"M{bx},{gy} C{bx + 2*s},{gy - 16} {tipx},{tipy + 14} {tipx},{tipy}",
               f"Grass {i+1}.{j+1}", fill=NONE,
               stroke="#C9A856" if j % 2 else "#8F7434",
               strokeWidth=3, opacity=65, cap="round")

# soft contact shadow under the animal
d.shape("ellipse", "Contact shadow", x=350, y=736, width=340, height=26,
        fill="#241809", opacity=30, stroke=NONE)

# --- legs: thin for the body's bulk, front pair slightly knelt ---------------------------
for i, (x0, bend, shade) in enumerate([(386, -8, SKIN_GRAD), (412, -14, "#4A3A28"),
                                       (618, 8, "#4A3A28"), (644, 6, SKIN_GRAD)]):
    d.path(f"M{x0},600 C{x0 - 3},660 {x0 + bend},700 {x0 + bend - 2},742",
           f"Leg {i+1}", fill=NONE, stroke=shade, strokeWidth=15, cap="round")
    d.path(f"M{x0 + bend - 10},738 L{x0 + bend + 10},738 L{x0 + bend + 7},750 L{x0 + bend - 8},750 Z",
           f"Hoof {i+1}", fill="#1E140A", stroke=NONE)

# --- tail: the signal flag, vertical off the rump ----------------------------------------
d.path("M698,516 C712,478 720,432 724,390", "Tail", fill=NONE,
       stroke="#3A2C1C", strokeWidth=6, cap="round")
d.path("M718,394 C710,372 714,352 726,346 C736,356 738,376 730,394 Z",
       "Tail tuft", fill="#201408", stroke=NONE)

# --- body -----------------------------------------------------------------------------------
d.path(smooth([(352, 516), (350, 470), (390, 438), (470, 430), (560, 442),
               (640, 464), (690, 502), (708, 552), (698, 610), (668, 650),
               (600, 664), (470, 668), (400, 652), (368, 602)]),
       "Body", fill=SKIN_GRAD, stroke=INK, strokeWidth=5)
# flank shade + top light
d.path("M400,640 C470,660 580,660 650,640 C590,672 460,672 400,640 Z",
       "Belly shade", fill="#241809", opacity=30, stroke=NONE)
d.path("M392,452 C460,436 560,446 640,468", "Back light", fill=NONE,
       stroke="#C0A87C", strokeWidth=8, opacity=35, cap="round")

# --- mane: an irregular crest of dark bristles from poll to mid-back ---------------------------
spikes = []
mx0, my0, mx1, my1 = 350, 424, 566, 446
lens = [42, 34, 46, 30, 38, 26, 40, 30, 34, 24, 28, 22, 24, 18]
nsp = len(lens)
for i, L in enumerate(lens):
    t = i / (nsp - 1)
    x0 = mx0 + (mx1 - mx0) * t
    y0 = my0 + (my1 - my0) * t
    spikes.append((x0, y0, L, i % 3 * 3))
mane = f"M{mx0 - 6},{my0 + 8} "
for (x0, y0, L, jit) in spikes:
    mane += f"L{x0 + 4:.0f},{y0 - L + jit:.0f} L{x0 + 13:.0f},{y0 + 5:.0f} "
mane += f"L{mx1 + 10},{my1 + 10} L{mx0 - 4},{my0 + 16} Z"
d.path(mane, "Mane", fill="#241809", opacity=88, stroke=NONE)

# --- head: the armoured wedge, carried low -----------------------------------------------------
d.path("M352,434 C330,442 306,462 288,486 C268,512 250,536 240,556 "
       "C234,570 238,584 252,594 C272,606 300,612 322,606 "
       "C340,600 352,584 356,560 C358,540 356,516 352,494 "
       "C350,474 350,452 352,434 Z",
       "Head", fill=HEAD_GRAD, stroke=INK, strokeWidth=5)
# forehead plane + muzzle shadow
d.shape("ellipse", "Forehead light", x=272, y=446, width=86, height=40,
        fill="#B49A6E", opacity=28, stroke=NONE)
d.path("M246,562 C258,586 284,600 312,598 C288,612 250,604 238,574 Z",
       "Jowl shade", fill="#241809", opacity=32, stroke=NONE)
# wart bumps: soft shading on snout ridge + cheek, no outlines
d.shape("ellipse", "Wart under eye", x=292, y=534, width=30, height=22,
        fill="#48371F", opacity=55, stroke=NONE)
d.shape("ellipse", "Wart cheek", x=318, y=566, width=26, height=20,
        fill="#48371F", opacity=50, stroke=NONE)
# the nose disc and nostrils
d.shape("ellipse", "Nose disc", x=230, y=546, width=30, height=38,
        fill="#332413", opacity=90, stroke=NONE)
d.shape("ellipse", "Nostril", x=238, y=558, width=9, height=12,
        fill="#140C04", stroke=NONE)
# neck wedge closing the throat silhouette into the chest
d.path("M336,540 C352,570 368,604 386,640 C400,650 420,652 430,640 "
       "C412,610 396,576 386,548 C372,540 350,536 336,540 Z",
       "Neck fill", fill=HEAD_GRAD, stroke=NONE)
# wrinkle creases where the jaw folds back into the neck
for i, dd in enumerate(["M350,486 C358,514 360,544 354,574",
                        "M364,478 C370,506 372,538 366,570"]):
    d.path(dd, f"Neck fold {i+1}", fill=NONE, stroke="#2E2112",
           strokeWidth=4, opacity=45, cap="round")
# mouth line
d.path("M244,578 C258,588 274,592 290,590", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")

# --- tusks: the great upward curl out in front of the face ---------------------------------------
d.path("M258,588 C252,556 256,522 270,494 C278,476 288,462 298,452 "
       "C292,480 284,506 280,532 C276,554 274,572 276,590 "
       "C270,592 262,592 258,588 Z",
       "Tusk upper", fill=TUSK_GRAD, stroke="#5C4C2C", strokeWidth=2)
# the short lower tusk pushing forward at the chin
d.path("M250,586 C256,570 266,556 280,548 C280,564 274,580 264,592 Z",
       "Tusk lower", fill="#D9CCA4", stroke="#5C4C2C", strokeWidth=2)

# --- ears: pointed, swept back, two distinct blades ----------------------------------------------
d.path("M356,438 C340,424 322,404 320,382 C322,368 334,362 344,370 "
       "C360,382 370,404 372,424 C368,434 362,440 356,438 Z",
       "Ear near", fill="#5E4B34", stroke=INK, strokeWidth=4)
d.path("M378,434 C370,414 368,394 374,378 C382,366 392,370 396,382 "
       "C400,400 398,420 390,436 Z",
       "Ear far", fill="#4C3A26", stroke=INK, strokeWidth=4)
d.path("M342,420 C334,404 336,390 344,380", "Ear fold", fill=NONE,
       stroke="#2E2112", strokeWidth=3, opacity=55, cap="round")

# --- eye: small, high, watching ------------------------------------------------------------------
d.shape("ellipse", "Eye", x=306, y=504, width=18, height=15, fill="#1A1008", stroke=NONE)
d.shape("ellipse", "Glint", x=310, y=506, width=5, height=5, fill="#F4E8C8", opacity=80, stroke=NONE)
d.path("M300,494 C310,488 322,488 330,494", "Brow", fill=NONE,
       stroke="#2E2112", strokeWidth=3, opacity=50, cap="round")

# --- name ------------------------------------------------------------------------------------------
r1 = d.text("WARTHOG", "Name", x=500, y=962, size=60, font="Virelai Sans",
            color="#F2E2B4", justify="center")

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

d.finish("warthog-V1R00")
