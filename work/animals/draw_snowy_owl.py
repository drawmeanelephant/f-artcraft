#!/usr/bin/env python3
"""Snowy owl — field plate V1R00. Front bust out of a white sky: round head
with no ear tufts, gold forward eyes, small dark bill, sparse salt-and-pepper
barring melting down the breast. Tundra plate, noon-night mood — milky light,
blowing snow, snowdrift closing on the disc's own arc. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Snowy Owl — Field Plate", 1000, 1000)
rng = random.Random(31)

PCX, PCY, PR = 500, 460, 420
INK = "#222E38"   # warm dark slate, never pure black

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

BG_GRAD    = lin(0, 0, 0, 1000, (0, "#0C141C"), (1, "#03070B"))
PLATE_GRAD = rad((0, "#E4EDF2"), (0.6, "#B4C8D4"), (1, "#6E889A"))
OWL_GRAD   = rad((0, "#FDFEFD"), (0.55, "#E8F0F3"), (1, "#AEC2CE"))
SNOW_GRAD  = lin(0, 720, 0, 880, (0, "#F4FAFC"), (1, "#9EB8C8"))
EYE_GRAD   = rad((0, "#FADA5E"), (0.6, "#E8B02E"), (1, "#B07814"))

# --- backdrop + noon-night plate --------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#C8DAE4", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#4E6878", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F2F8FB", strokeWidth=3, opacity=50)

# low milky sun glow left of center, fading before the rim
d.shape("ellipse", "Sun glow", x=220, y=170, width=380, height=300,
        fill=radO((0, "#F6FAFC", 45), (0.55, "#F6FAFC", 18), (1, "#F6FAFC", 0)), stroke=NONE)
# cloud veil band across the light
for i, dd in enumerate(["M150,300 C330,272 560,276 780,306",
                        "M190,390 C360,368 600,372 820,398"]):
    d.path(dd, f"Cloud veil {i+1}", fill=NONE, stroke="#8AA2B0",
           strokeWidth=30, opacity=18, cap="round")

# blowing snow streaks, all endpoints inside the disc
for i, (x, y, ln) in enumerate([(210, 240, 90), (420, 180, 70), (620, 200, 85),
                                (760, 300, 75), (280, 420, 65), (690, 440, 70),
                                (180, 560, 60), (800, 540, 55)]):
    assert on_disc(x, y, 20) and on_disc(x + ln * 0.9, y + ln * 0.25, 20), (x, y)
    d.path(f"M{x},{y} L{x + ln * 0.9:.0f},{y + ln * 0.25:.0f}", f"Snow streak {i+1}",
           fill=NONE, stroke="#F4FAFC", strokeWidth=2.2, opacity=25, cap="round")
# distant flakes
for i, (x, y, w) in enumerate([(230, 180, 6), (750, 170, 6), (170, 360, 6), (840, 380, 6),
                               (330, 120, 5), (670, 130, 5), (250, 520, 5), (790, 500, 5),
                               (450, 105, 4), (580, 110, 4)]):
    assert on_disc(x + w / 2, y + w / 2, 8), (x, y)
    d.shape("ellipse", f"Flake {i+1}", x=x, y=y, width=w, height=w,
            fill="#F6FAFD", opacity=55, stroke=NONE)

# ghost drift shapes on the horizon
for i, (x, y, w, h, op) in enumerate([(200, 700, 120, 26, 20), (720, 706, 140, 30, 18),
                                      (330, 716, 90, 20, 14), (600, 722, 100, 22, 13)]):
    d.shape("ellipse", f"Drift ghost {i+1}", x=x - w / 2, y=y - h / 2, width=w, height=h,
            fill="#7E98A8", opacity=op, stroke=NONE)

# --- snowdrift floor, closing on the disc's own arc --------------------------------
fy = 748
x0, x1 = disc_x(fy, -1), disc_x(fy, 1)
d.path(f"M{x0:.1f},{fy} C340,734 660,734 {x1:.1f},{fy} "
       f"A{PR},{PR} 0 0 1 {x0:.1f},{fy} Z", "Snowdrift", fill=SNOW_GRAD,
       stroke="#8FA8B8", strokeWidth=3.5)
d.path(f"M{x0 + 6:.1f},{fy} C340,734 660,734 {x1 - 6:.1f},{fy}",
       "Drift light", fill=NONE, stroke="#FAFDFE", strokeWidth=3, opacity=55, cap="round")
for i, dd in enumerate(["M250,790 C380,780 560,782 700,790", "M320,830 C440,822 580,824 690,830"]):
    d.path(dd, f"Drift shade {i+1}", fill=NONE, stroke="#8AA4B4",
           strokeWidth=4, opacity=35, cap="round")
# the owl's contact shadow on the snow
d.shape("ellipse", "Owl shadow", x=360, y=736, width=280, height=26,
        fill="#4E6878", opacity=32, stroke=NONE)

# === the owl ======================================================================
# body: one upright mass — round head flowing into shoulders, sitting on the drift.
BODY = ("M500,288 C420,288 372,340 366,410 C362,460 356,500 342,548 "
        "C330,590 330,650 352,690 C382,732 438,752 500,752 "
        "C562,752 618,732 648,690 C670,650 670,590 658,548 "
        "C644,500 638,460 634,410 C628,340 580,288 500,288 Z")
d.path(BODY, "Owl", fill=OWL_GRAD, stroke=INK, strokeWidth=6)

# modelling shade under the chin and along both flanks
d.path("M356,470 C350,540 356,620 390,690", "Flank shade L", fill=NONE,
       stroke="#8AA2B2", strokeWidth=22, opacity=22, cap="round")
d.path("M644,470 C650,540 644,620 610,690", "Flank shade R", fill=NONE,
       stroke="#8AA2B2", strokeWidth=22, opacity=22, cap="round")
d.path("M420,470 C450,490 550,490 580,470", "Chin shade", fill=NONE,
       stroke="#8AA2B2", strokeWidth=14, opacity=25, cap="round")
# breast light: a cool dome of white on the chest
d.shape("ellipse", "Breast light", x=400, y=500, width=200, height=170,
        fill=radO((0, "#FFFFFF", 55), (0.6, "#FFFFFF", 20), (1, "#FFFFFF", 0)), stroke=NONE)

# facial discs: two pale lobes meeting above the bill
for sgn, lab in ((-1, "L"), (1, "R")):
    ex = 500 + sgn * 62
    d.shape("ellipse", f"Facial disc {lab}", x=ex - 74, y=330, width=148, height=140,
            fill="#F4F9FA", opacity=70, stroke=NONE)
    d.path(f"M{ex - sgn * 72},360 C{ex - sgn * 84},400 {ex - sgn * 78},440 {ex - sgn * 56},462",
           f"Disc rim {lab}", fill=NONE, stroke="#9EB4C2", strokeWidth=4,
           opacity=30, cap="round")

# sparse salt-and-pepper barring: a male, so keep it light —
# chevrons on the crown, scallops on the shoulders, all inside the silhouette
for i, (x, y, w) in enumerate([(430, 315, 16), (570, 315, 16), (398, 358, 14),
                               (602, 358, 14), (376, 530, 16), (624, 530, 16),
                               (388, 618, 14), (612, 618, 14)]):
    d.path(f"M{x - w / 2},{y} Q{x},{y + w * 0.5} {x + w / 2},{y}",
           f"Crown bar {i+1}", fill=NONE, stroke="#3E4E5A", strokeWidth=4,
           opacity=60, cap="round")
for i, (x, y) in enumerate([(420, 560), (500, 585), (580, 560), (450, 640),
                            (550, 640), (500, 700)]):
    d.path(f"M{x - 9},{y} Q{x},{y + 8} {x + 9},{y}", f"Breast bar {i+1}",
           fill=NONE, stroke="#4E5E6A", strokeWidth=3.5, opacity=50, cap="round")

# eyes: gold, forward-facing, slightly hooded
for sgn, lab in ((-1, "L"), (1, "R")):
    ex = 500 + sgn * 62
    d.shape("ellipse", f"Iris {lab}", x=ex - 22, y=392, width=44, height=44,
            fill=EYE_GRAD, stroke="#7A5410", strokeWidth=3)
    d.shape("ellipse", f"Pupil {lab}", x=ex - 11, y=403, width=22, height=22,
            fill="#0E1418", stroke=NONE)
    d.shape("ellipse", f"Glint {lab}", x=ex - 13, y=402, width=8, height=8,
            fill="#FFFFFF", opacity=90, stroke=NONE)
    # the hood: a brow shade casting the glare
    d.path(f"M{ex - sgn * 30},384 C{ex - sgn * 10},374 {ex + sgn * 18},376 {ex + sgn * 32},390",
           f"Brow {lab}", fill=NONE, stroke="#5E7280", strokeWidth=7,
           opacity=45, cap="round")

# bill: small dark hook pointing down between the discs
d.path("M486,442 C490,464 494,478 500,486 C506,478 510,464 514,442 "
       "C508,448 492,448 486,442 Z", "Bill", fill="#2E3A42",
       stroke=INK, strokeWidth=2.5)
d.path("M492,452 C496,462 500,468 504,462", "Bill light", fill=NONE,
       stroke="#7E94A2", strokeWidth=2.5, opacity=60, cap="round")
# faint bristles around the bill base
for sgn in (-1, 1):
    d.path(f"M{500 + sgn * 14},444 L{500 + sgn * 34},{452}", f"Bristle {sgn}",
           fill=NONE, stroke="#8AA0AE", strokeWidth=2, opacity=50, cap="round")

# crown light: the pale dome catching the noon-night sun
d.shape("ellipse", "Crown light", x=420, y=296, width=160, height=52,
        fill="#FFFFFF", opacity=35, stroke=NONE)

# foreground flakes over the bird
for i, (x, y, w) in enumerate([(330, 300, 7), (660, 280, 6), (270, 620, 6),
                               (740, 640, 7), (430, 220, 5), (610, 540, 5)]):
    assert on_disc(x + w / 2, y + w / 2, 8), (x, y)
    d.shape("ellipse", f"Front flake {i+1}", x=x, y=y, width=w, height=w,
            fill="#FFFFFF", opacity=70, stroke=NONE)

# plate rim on top so everything inside closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840, fill=NONE,
        stroke="#22323E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring 2", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F2F8FB", strokeWidth=3, opacity=40)

# --- name --------------------------------------------------------------------------
r1 = d.text("SNOWY OWL", "Name", x=500, y=962, size=58, font="Virelai Sans",
            color="#E2EDF2", justify="center")

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

d.finish("snowy-owl-V1R00")
