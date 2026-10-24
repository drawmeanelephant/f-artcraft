#!/usr/bin/env python3
"""Porcupinefish — field plate V1R00. A pincushion that remembers being a
fish: inflated to a bristling ball, hovering over a coral-reef floor at
dusk — coral plate, inflate mood. Three-quarter face on: two huge eyes, a
pursed little beak, spines radiating in every direction, fins reduced to
paddles. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Porcupinefish — Field Plate", 1000, 1000)
rng = random.Random(29)

CX, CY, R = 500, 460, 420          # plate disc centre + radius
INK = "#241608"                    # warm dark ink, never pure black

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

BG_GRAD    = lin(0, 0, 0, 1000, (0, "#120A06"), (1, "#060302"))
PLATE_GRAD = rad((0, "#D9A878"), (0.5, "#8E5B3C"), (1, "#3E2414"))
SAND_GRAD  = lin(0, 700, 0, 880, (0, "#A4744A"), (0.6, "#5E3E24"), (1, "#2E1C0E"))
BODY_GRAD  = rad((0, "#F0DCAE"), (0.55, "#C9A468"), (1, "#7E5A30"))
SPINE_GRAD = lin(500, 280, 500, 640, (0, "#E4C88E"), (1, "#8E6A38"))
BELLY      = "#F4E4BC"
CORAL_GRAD = lin(0, 620, 0, 800, (0, "#B85A44"), (1, "#5E2818"))

# --- backdrop + coral dusk plate ---------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=64, y=24, width=872, height=872,
        fill="#B87A50", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#2E180C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#EFD3A8", strokeWidth=3, opacity=30)

# dusk light shafted through the water, fading before the rim
d.shape("ellipse", "Dusk light", x=300, y=110, width=400, height=250,
        fill=rad((0, "#F2CE9A", 24), (0.6, "#F2CE9A", 10), (1, "#F2CE9A", 0)), stroke=NONE)
# drifting sediment motes
for i in range(26):
    a = rng.uniform(0, math.tau); rr = math.sqrt(rng.uniform(0, 1)) * 380
    x, y = CX + rr * math.cos(a), CY + rr * math.sin(a)
    if not on_disc(x, y, 20): continue
    w = rng.uniform(2.5, 5)
    d.shape("ellipse", f"Mote {i+1}", x=x - w/2, y=y - w/2, width=w, height=w,
            fill="#F2DCB4", opacity=rng.randint(14, 30), stroke=NONE)

# --- reef floor: sand closing on the arc, corals riding it --------------------------
fy = 690
fl, fr = rim_x(fy, side=-1), rim_x(fy, side=1)
d.path(f"M{fl:.1f},{fy} C300,672 480,700 640,690 C740,684 820,688 {fr:.1f},{fy} "
       f"A{R},{R} 0 0 1 {fl:.1f},{fy} Z", "Sand floor", fill=SAND_GRAD, stroke=NONE)
d.path(f"M{fl + 6:.1f},{fy} C300,672 480,700 640,690 C740,684 820,688 {fr - 6:.1f},{fy}",
       "Sand crest light", fill=NONE, stroke="#E4BC86", strokeWidth=4, opacity=35, cap="round")

# staghorn coral left — branching strokes
for k, dd in enumerate([
        "M225,700 C218,668 210,640 196,616 M210,652 C202,640 192,632 182,626",
        "M225,700 C232,668 240,642 252,620 M238,654 C248,646 256,636 262,624",
        "M225,700 C225,672 228,650 230,628"]):
    d.path(dd, f"Staghorn {k+1}", fill=NONE, stroke=CORAL_GRAD,
           strokeWidth=7 - k, opacity=85, cap="round")
# brain coral dome right — concentric meander arcs on a mound
d.path("M700,724 C700,676 740,640 790,640 C840,640 880,676 880,724 Z",
       "Brain coral", fill=lin(0, 640, 0, 724, (0, "#C47858"), (1, "#6E3822")),
       stroke=INK, strokeWidth=4)
for k in range(3):
    yy = 672 + k * 18
    d.path(f"M{716 + k*6},{yy} C{740},{yy - 12} {770},{yy + 10} {800},{yy - 6} "
           f"C{826},{yy - 14} {850},{yy + 4} {864 - k*4},{yy}",
           f"Brain fold {k+1}", fill=NONE, stroke="#5E2E1C",
           strokeWidth=4, opacity=70, cap="round")
# a sea fan between them — small fan of strokes
for k in range(6):
    a = -70 + k * 26
    x1 = 356 + 66 * math.sin(math.radians(a)) * 0.9
    y1 = 706 - 66 * math.cos(math.radians(a))
    d.path(f"M356,706 Q{356 + (x1-356)*0.5},{y1 - 14} {x1:.0f},{y1:.0f}",
           f"Fan rib {k+1}", fill=NONE, stroke="#8E4A6A",
           strokeWidth=3.5, opacity=70, cap="round")
# rubble dots on the sand
for i, (x, y, w) in enumerate([(300, 740, 12), (430, 756, 9), (560, 744, 14),
                               (660, 762, 10), (190, 730, 8), (780, 748, 12)]):
    d.shape("ellipse", f"Rubble {i+1}", x=x - w/2, y=y - w/4, width=w, height=w*0.55,
            fill="#4A2E18", opacity=50, stroke=NONE)

# the fish's own soft shadow on the sand
d.shape("ellipse", "Fish shadow", x=380, y=668, width=260, height=30,
        fill=rad((0, "#241204", 45), (1, "#241204", 0)), stroke=NONE)

# === the pincushion ==================================================================
BCX, BCY, BR = 500, 430, 150        # ball centre + radius

# tail paddle peeking behind the ball, right side
d.path("M636,420 C672,404 700,406 716,424 C704,444 678,452 646,448 Z",
       "Tail", fill=SPINE_GRAD, stroke=INK, strokeWidth=4)
for k in range(3):
    d.path(f"M{650 + k*8},{424 + k*2} C{672 + k*6},{424 + k*4} {690 + k*6},{428 + k*4} {704 + k*4},{432 + k*4}",
           f"Tail rib {k+1}", fill=NONE, stroke="#7E5A30", strokeWidth=2.5, opacity=60)
# dorsal paddle top-right, anal paddle bottom-left
d.path("M560,296 C584,272 610,268 624,282 C614,302 592,312 566,310 Z",
       "Dorsal fin", fill=SPINE_GRAD, stroke=INK, strokeWidth=4)
d.path("M408,560 C390,584 366,592 350,584 C356,562 376,550 400,548 Z",
       "Anal fin", fill=SPINE_GRAD, stroke=INK, strokeWidth=4)

# pectoral paddles splayed wide — the little oars that hold a ball in place
d.path("M370,420 C336,404 306,406 292,424 C304,446 334,452 366,446 Z",
       "Pectoral L", fill=lin(370, 410, 295, 445, (0, "#D8B87E"), (1, "#8E6A38")),
       stroke=INK, strokeWidth=4)
d.path("M630,430 C662,416 692,420 706,438 C694,458 664,462 634,456 Z",
       "Pectoral R", fill=lin(630, 420, 705, 460, (0, "#D8B87E"), (1, "#8E6A38")),
       stroke=INK, strokeWidth=4)

# --- spines: tapered triangles radiating, denser on the back, sparse on the face ----
# face sector ~ -20..100 deg (right/down of centre) gets shorter sparser spines
def spines(angles, base_r, tip_r, half_w, fill):
    for i, ad in enumerate(angles):
        a = math.radians(ad)
        bx, by = BCX + base_r * math.cos(a), BCY + base_r * math.sin(a) * 0.96
        tx, ty = BCX + tip_r * math.cos(a), BCY + tip_r * math.sin(a)
        px, py = -math.sin(a) * half_w, math.cos(a) * half_w
        d.path(f"M{bx - px:.1f},{by - py:.1f} L{tx:.1f},{ty:.1f} L{bx + px:.1f},{by + py:.1f} Z",
               f"Spine {i+1:02d} @{ad}", fill=fill, stroke="#3A2810", strokeWidth=1.5)

long_angles  = [100, 115, 130, 145, 160, 175, 190, 205, 220, 235, 250, 265, 280, 295]
back_angles  = [310, 325, 340, 355, 10, 25, 40, 55]
spines(long_angles, 138, 200, 5.5, SPINE_GRAD)          # long defensive ring
spines(back_angles, 138, 178, 5, SPINE_GRAD)             # shorter over the crown
spines([70, 85], 138, 170, 4.5, SPINE_GRAD)              # strays above the face

# --- the ball ------------------------------------------------------------------------
d.shape("ellipse", "Body", x=BCX - BR, y=BCY - BR, width=BR * 2, height=BR * 2,
        fill=BODY_GRAD, stroke=INK, strokeWidth=6)
# spine-root rosettes around the rim — darker dots where each spine seats
for i, ad in enumerate(long_angles + back_angles):
    a = math.radians(ad)
    x, y = BCX + 132 * math.cos(a), BCY + 128 * math.sin(a) * 0.96
    d.shape("ellipse", f"Root {i+1}", x=x - 4, y=y - 4, width=8, height=8,
            fill="#5E421E", opacity=55, stroke=NONE)
# pale belly band low across the face
d.path("M382,478 C420,540 470,566 520,562 C576,556 622,522 636,470 "
       "C600,506 540,524 484,516 C444,510 408,496 382,478 Z",
       "Belly", fill=BELLY, opacity=75, stroke=NONE)
# cheek light
d.shape("ellipse", "Cheek light", x=390, y=340, width=120, height=80,
        fill=rad((0, "#F8ECD0", 45), (1, "#F8ECD0", 0)), stroke=NONE)
# dark body spots — the leopard under the pins
for i, (x, y, w) in enumerate([(420, 350, 16), (560, 330, 14), (610, 420, 15), (390, 450, 12),
                               (530, 520, 14), (450, 500, 11), (600, 500, 12), (480, 330, 10)]):
    d.shape("ellipse", f"Spot {i+1}", x=x - w/2, y=y - w/2.6, width=w, height=w*0.72,
            fill="#4A3214", opacity=60, stroke=NONE)

# --- the face --------------------------------------------------------------------------
# two huge eyes, wide set — the fish that remembers
for sgn, ex, ew in ((-1, 432, 52), (1, 572, 46)):
    d.shape("ellipse", f"Eye {'L' if sgn < 0 else 'R'} ring", x=ex - ew/2 - 4, y=384 - ew/2 - 4,
            width=ew + 8, height=ew + 8, fill="#6E4E22", opacity=70, stroke=NONE)
    d.shape("ellipse", f"Eye {'L' if sgn < 0 else 'R'}", x=ex - ew/2, y=384 - ew/2,
            width=ew, height=ew, fill="#1A1006", stroke=INK, strokeWidth=3)
    d.shape("ellipse", f"Eye glint {sgn}", x=ex - ew/2 + ew*0.6, y=384 - ew/2 + ew*0.22,
            width=ew*0.24, height=ew*0.24, fill="#FFF6DC", opacity=90, stroke=NONE)
    d.shape("ellipse", f"Eye glint 2 {sgn}", x=ex - ew/2 + ew*0.3, y=384 - ew/2 + ew*0.6,
            width=ew*0.12, height=ew*0.12, fill="#FFF6DC", opacity=45, stroke=NONE)
# brow crease between the eyes — worried expression for free
d.path("M468,348 C492,338 520,338 544,346", "Brow crease", fill=NONE,
       stroke="#7E5A30", strokeWidth=4, opacity=50, cap="round")
# the pursed beak — a little heart of a mouth
d.path("M476,470 C486,458 500,454 512,458 C524,462 530,474 524,486 "
       "C514,494 498,496 488,490 C478,484 472,478 476,470 Z",
       "Beak", fill="#3A2810", stroke=INK, strokeWidth=3.5)
d.path("M482,474 C494,478 508,478 520,474", "Beak seam", fill=NONE,
       stroke="#0E0804", strokeWidth=3, cap="round")
d.path("M486,468 C496,464 508,464 518,468", "Beak sheen", fill=NONE,
       stroke="#8E6A38", strokeWidth=2.5, opacity=70, cap="round")
# nostril dots above the beak
for sgn in (-1, 1):
    d.shape("ellipse", f"Nostril {sgn}", x=500 + sgn * 10 - 3, y=446 - 3, width=6, height=6,
            fill="#4A3214", opacity=75, stroke=NONE)

# bubbles trailing up past the flank — the last of the held breath
for i, (x, y, w) in enumerate([(660, 430, 10), (684, 392, 14), (700, 348, 8), (714, 306, 11)]):
    assert on_disc(x, y, 12), (x, y)
    d.shape("ellipse", f"Bubble {i+1}", x=x - w/2, y=y - w/2, width=w, height=w,
            fill=NONE, stroke="#F2DCB4", strokeWidth=2.5, opacity=45)
    d.shape("ellipse", f"Bubble gleam {i+1}", x=x - w/4, y=y - w/4, width=w*0.3, height=w*0.3,
            fill="#F8ECD0", opacity=55, stroke=NONE)

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#221208", strokeWidth=6)

# --- name ---------------------------------------------------------------------------
r1 = d.text("PORCUPINEFISH", "Name", x=500, y=962, size=56, font="Virelai Sans",
            color="#F0DCB4", justify="center")

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

d.finish("porcupinefish-V1R00")
