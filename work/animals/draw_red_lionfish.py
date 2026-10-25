#!/usr/bin/env python3
"""Red lionfish — field plate V1R00. Lateral view facing left over a dusk
reef: every dorsal spine a bare needle, the pectoral fin a striped fan of
pennants sweeping back. Banded red-and-cream body, translucent fin
membranes over the disc. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Red Lionfish — Field Plate", 1000, 1000)

INK = "#2A1418"
CX, CY, R = 500, 460, 420

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

BG_GRAD    = lin(0, 0, 0, 1000, (0, "#0F1E22"), (1, "#050B0E"))
PLATE_GRAD = rad((0, "#97ACAC"), (0.62, "#5F7E80"), (1, "#2E4348"))
BODY_GRAD  = lin(460, 430, 460, 535, (0, "#E8CFA8"), (0.5, "#C89468"), (1, "#8A5A3C"))
BAND_GRAD  = lin(460, 430, 460, 535, (0, "#8E3220"), (1, "#4E1A10"))
FAN_MEMB   = rad((0, "#C46A50"), (1, "#7E3A2A"))
GROUND_GRAD = lin(0, 745, 0, 880, (0, "#567072"), (1, "#24363A"))
CREAM = "#F0E2C8"

def on_disc(x, y, pad=10):
    return math.hypot(x - CX, y - CY) <= R - pad

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#1E3034", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#CFE0DC", strokeWidth=3, opacity=26)
for i, (x, y, w, o) in enumerate([(200, 250, 9, 34), (770, 230, 7, 32), (165, 490, 8, 30),
                                  (825, 600, 9, 34), (310, 180, 7, 30), (640, 155, 8, 32),
                                  (235, 680, 7, 30), (770, 710, 8, 28), (430, 135, 6, 28),
                                  (150, 610, 6, 28), (855, 390, 7, 30), (560, 805, 7, 28)]):
    assert on_disc(x + w / 2, y + w / 2), (x, y)
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#2E4A4C", opacity=o, stroke=NONE)
# slow bubbles, upper left
for i, (x, y, w) in enumerate([(230, 320, 12), (255, 260, 8), (212, 390, 9), (268, 210, 6)]):
    assert on_disc(x, y), (x, y)
    d.shape("ellipse", f"Bubble {i+1}", x=x, y=y, width=w, height=w,
            fill="#D8EAE4", opacity=14, stroke=NONE)

# --- reef floor: dark chord closing on the disc arc ------------------------------
gy = 756
gdx = math.sqrt(R * R - (gy - CY) ** 2)
d.path(f"M{CX-gdx:.1f},{gy} C300,744 420,752 520,748 C620,744 715,750 {CX+gdx:.1f},{gy} "
       f"A{R},{R} 0 0 1 {CX-gdx:.1f},{gy} Z", "Reef floor", fill=GROUND_GRAD, stroke=NONE)
# branching coral sprigs rising from the floor, kept well inside the disc
def coral(x0, y0, s, label, color):
    d.path(f"M{x0},{y0} C{x0-4*s},{y0-30*s} {x0-14*s},{y0-48*s} {x0-24*s},{y0-62*s} "
           f"M{x0},{y0-8*s} C{x0+6*s},{y0-28*s} {x0+16*s},{y0-42*s} {x0+28*s},{y0-50*s} "
           f"M{x0-12*s},{y0-36*s} C{x0-20*s},{y0-46*s} {x0-30*s},{y0-50*s} {x0-38*s},{y0-56*s}",
           label, fill=NONE, stroke=color, strokeWidth=8, opacity=85, cap="round")
coral(760, 752, 1.0, "Coral R", "#7E4A44")
coral(300, 754, 0.8, "Coral L", "#6E4452")
# sponge lumps + urchin hint
for i, (x, y, w, h) in enumerate([(640, 738, 56, 26), (700, 744, 38, 18), (216, 742, 46, 22)]):
    d.shape("ellipse", f"Sponge {i+1}", x=x, y=y, width=w, height=h,
            fill="#5E4A5E", opacity=70, stroke=NONE)
for i in range(7):
    a = math.radians(-160 + i * 25)
    x0, y0 = 392 + math.cos(a) * 14, 744 + math.sin(a) * 10
    d.path(f"M392,744 L{x0 + math.cos(a)*12:.0f},{y0 + math.sin(a)*10:.0f}",
           f"Urchin spine {i+1}", fill=NONE, stroke="#3A2E3E", strokeWidth=4,
           opacity=80, cap="round")
d.shape("ellipse", "Urchin body", x=382, y=736, width=20, height=14,
        fill="#2A1E2E", stroke=NONE)
d.shape("ellipse", "Lionfish shadow", x=300, y=744, width=400, height=18,
        fill="#16303A", opacity=40, stroke=NONE)

# --- dorsal spines: a rank of bare needles, leaning back --------------------------
spine_bases = [(372, 452), (398, 448), (424, 445), (450, 443), (476, 441),
               (502, 440), (528, 440), (554, 441), (580, 443), (606, 447)]
for i, (bx, by) in enumerate(spine_bases):
    ln = 210 - abs(i - 4) * 14          # longest over the front body
    tipx = bx + ln * 0.22
    tipy = by - ln
    midx, midy = bx + ln * 0.08, by - ln * 0.55
    d.path(f"M{bx},{by} Q{midx:.0f},{midy:.0f} {tipx:.0f},{tipy:.0f}",
           f"Dorsal spine {i+1}", fill=NONE, stroke=CREAM, strokeWidth=5, cap="round")
    # dark flag near the tip — the pennant
    d.path(f"M{bx + ln*0.16},{by - ln*0.82} Q{bx + ln*0.19},{by - ln*0.9} {tipx},{tipy}",
           f"Spine flag {i+1}", fill=NONE, stroke="#6E2418", strokeWidth=5,
           opacity=85, cap="round")

# --- far pectoral fan: a few rays peeking below the body, dimmer ----------------------
FXO, FYO = 448, 500
for i, ang in enumerate([40, 58, 76, 94]):
    a = math.radians(ang)
    ln = 132
    tx, ty = FXO + math.cos(a) * ln, FYO + math.sin(a) * ln * 0.92
    d.path(f"M{FXO},{FYO} L{tx:.0f},{ty:.0f}", f"Far ray {i+1}", fill=NONE,
           stroke="#8A5A44", strokeWidth=5, opacity=40, cap="round")

# --- body silhouette + banding -------------------------------------------------------
d.path("M306,468 C340,452 380,444 422,442 C482,436 560,438 615,450 "
       "C630,455 637,463 635,472 C637,482 629,492 616,496 "
       "C580,515 520,530 468,530 C420,530 372,522 340,510 "
       "C318,500 307,486 306,468 Z",
       "Body", fill=BODY_GRAD, stroke=INK, strokeWidth=6)

TOP_PTS = [(306, 468), (360, 450), (422, 442), (520, 439), (615, 450), (635, 472)]
BOT_PTS = [(306, 468), (330, 496), (400, 518), (470, 530), (560, 524), (616, 496), (635, 472)]

def interp(pts, x):
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if x0 <= x <= x1:
            t = (x - x0) / (x1 - x0) or 0
            return y0 + (y1 - y0) * t
    return pts[0][1] if x < pts[0][0] else pts[-1][1]

# warning bars: each strip lands just inside the body outline
for i, (x0, x1) in enumerate([(322, 348), (368, 396), (416, 446), (466, 496),
                              (518, 546), (566, 594)]):
    t0, t1 = interp(TOP_PTS, x0) + 3, interp(TOP_PTS, x1) + 3
    b0, b1 = interp(BOT_PTS, x0) - 3, interp(BOT_PTS, x1) - 3
    d.path(f"M{x0},{t0} C{(x0+x1)/2},{t0-4} {(x0+x1)/2},{t1-2} {x1},{t1} "
           f"C{x1+6},{(t1+b1)/2} {x1+2},{b1-6} {x1},{b1} "
           f"C{(x0+x1)/2},{b1+6} {(x0+x1)/2},{b0+4} {x0},{b0} "
           f"C{x0-6},{(t0+b0)/2} {x0-4},{t0+6} {x0},{t0} Z",
           f"Body band {i+1}", fill=BAND_GRAD, opacity=80, stroke=NONE)

# --- tail fin -------------------------------------------------------------------------
d.path("M634,452 C672,436 706,442 714,468 C720,494 704,516 672,522 "
       "C652,526 638,514 632,498 C628,480 628,464 634,452 Z",
       "Tail fin", fill=FAN_MEMB, opacity=75, stroke=INK, strokeWidth=5)
for i, (x, y) in enumerate([(668, 466), (684, 486), (664, 502), (692, 472), (678, 458)]):
    d.shape("ellipse", f"Tail spot {i+1}", x=x, y=y, width=7, height=7,
            fill="#3A1410", opacity=70, stroke=NONE)
# peduncle bars
for i, x in enumerate([618, 630]):
    d.path(f"M{x},{458} C{x+4},470 {x+4},482 {x},{496}", f"Peduncle bar {i+1}",
           fill=NONE, stroke="#6E2418", strokeWidth=8, opacity=70, cap="round")

# --- anal + pelvic fins ------------------------------------------------------------------
d.path("M545,530 C575,540 605,560 620,590 C596,590 566,576 548,554 C542,544 542,536 545,530 Z",
       "Anal fin", fill=FAN_MEMB, opacity=70, stroke=INK, strokeWidth=4)
for i, ang in enumerate([20, 45, 68]):
    a = math.radians(ang)
    d.path(f"M552,536 L{552 + math.cos(a)*62:.0f},{536 + math.sin(a)*56:.0f}",
           f"Anal spine {i+1}", fill=NONE, stroke=CREAM, strokeWidth=4,
           opacity=80, cap="round")
# pelvic filaments trailing under the chin
d.path("M410,522 C402,560 396,600 398,646", "Pelvic filament 1", fill=NONE,
       stroke=CREAM, strokeWidth=4, cap="round")
d.path("M424,524 C418,562 414,598 416,638", "Pelvic filament 2", fill=NONE,
       stroke="#B44A34", strokeWidth=4, cap="round")

# --- near pectoral fan: the banner ------------------------------------------------------
FOX, FOY = 442, 492
# translucent membrane wedge first (inner half of the fan)
memb_pts = []
for ang in range(-62, 80, 12):
    a = math.radians(ang)
    memb_pts.append((FOX + math.cos(a) * 132, FOY + math.sin(a) * 132 * 0.92))
memb_d = f"M{FOX},{FOY} " + " ".join(f"L{x:.0f},{y:.0f}" for x, y in memb_pts) + " Z"
d.path(memb_d, "Fan membrane", fill=FAN_MEMB, opacity=55, stroke=NONE)
# the rays: striped pennants, each ≥5pt, alternating cream / dark red
ray_angles = list(range(-62, 77, 11))
for i, ang in enumerate(ray_angles):
    a = math.radians(ang)
    ln = 216 - (0 if -40 < ang < 40 else 18)
    tx, ty = FOX + math.cos(a) * ln, FOY + math.sin(a) * ln * 0.92
    col = CREAM if i % 2 == 0 else "#8E3220"
    d.path(f"M{FOX + math.cos(a)*30:.0f},{FOY + math.sin(a)*30*0.92:.0f} "
           f"L{tx:.0f},{ty:.0f}", f"Fan ray {i+1}", fill=NONE,
           stroke=col, strokeWidth=5.5, cap="round")
    # dark pennant flag near the tip of the cream rays
    if i % 2 == 0:
        fx, fy = FOX + math.cos(a) * (ln - 34), FOY + math.sin(a) * (ln - 34) * 0.92
        d.path(f"M{fx:.0f},{fy:.0f} L{tx:.0f},{ty:.0f}", f"Ray flag {i+1}",
               fill=NONE, stroke="#5C1E14", strokeWidth=5.5, opacity=85, cap="round")
# membrane spots
for i, (x, y) in enumerate([(520, 420), (560, 470), (545, 540), (590, 430), (575, 515)]):
    d.shape("ellipse", f"Membrane spot {i+1}", x=x, y=y, width=8, height=8,
            fill="#4E1A10", opacity=45, stroke=NONE)

# --- head: bony face, big eye, cirri ----------------------------------------------------
d.path("M306,468 C316,458 330,452 346,450 C360,448 372,452 380,460 "
       "C372,470 370,484 374,496 C364,506 348,512 334,510 "
       "C318,506 308,490 306,468 Z",
       "Head plate", fill=lin(300, 450, 360, 510, (0, "#D8B083"), (1, "#8A5A38")),
       stroke=INK, strokeWidth=5)
# brow ridge + bony striations on the cheek
d.path("M322,460 C334,452 352,450 366,456", "Brow ridge", fill=NONE,
       stroke=INK, strokeWidth=4, opacity=70, cap="round")
for i, dd in enumerate(["M330,478 L360,482", "M332,490 L356,496", "M344,466 L352,474"]):
    d.path(dd, f"Cheek striation {i+1}", fill=NONE, stroke="#6E3A22",
           strokeWidth=4, opacity=55, cap="round")
# eye
d.shape("ellipse", "Eye", x=338, y=462, width=22, height=22, fill="#160C08",
        stroke=INK, strokeWidth=3)
d.shape("ellipse", "Eye glint", x=343, y=466, width=6, height=6, fill="#F4E8D2",
        opacity=90, stroke=NONE)
# eye tentacle: small branched cirrus above the eye, ≥4pt
d.path("M344,452 C346,442 350,434 358,428 M350,442 L358,436 M346,448 L354,444",
       "Eye cirrus", fill=NONE, stroke=INK, strokeWidth=4, cap="round")
# mouth: downturned, small; two chin barbels
d.path("M306,486 C314,490 322,492 330,492", "Mouth", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
d.path("M318,502 C314,514 312,524 314,534", "Chin barbel 1", fill=NONE,
       stroke="#B44A34", strokeWidth=4, cap="round")
d.path("M330,506 C328,516 328,524 330,532", "Chin barbel 2", fill=NONE,
       stroke=CREAM, strokeWidth=4, cap="round")
# nostril + snout shading
d.shape("ellipse", "Nostril", x=310, y=474, width=6, height=5, fill="#3A1C12",
        opacity=80, stroke=NONE)
d.path("M306,468 C312,460 322,455 334,452", "Snout light", fill=NONE,
       stroke="#F0DCB8", strokeWidth=4, opacity=50, cap="round")

# plate rim on top
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840, fill=NONE,
        stroke="#142428", strokeWidth=6)

# --- name + second line --------------------------------------------------------
d.text("RED LIONFISH", "Name", x=500, y=932, size=58, font="Virelai Sans",
       color="#D8E8E4", justify="center")
LINE2, SZ2, TRK = "PTEROIS VOLITANS", 22, 240
r = d.text(LINE2, "Second line", x=500, y=968, size=SZ2, font="Virelai Sans",
           color="#8FB4AE", justify="center")
d.cmd("text.setStyle", "Second line tracking", id=r["id"], tracking=TRK)
def find(o, oid):
    if isinstance(o, dict):
        if o.get("id") == oid and "bounds" in o: return o
        o = list(o.values())
    if isinstance(o, list):
        for v in o:
            hit = find(v, oid)
            if hit: return hit
b2 = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("second line bounds", {k: round(v) for k, v in b2.items()})
assert b2["width"] <= 760 and b2["x"] >= 100 and b2["y"] + b2["height"] <= 990, b2

d.finish("red-lionfish-V1R00")
