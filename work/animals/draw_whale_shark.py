#!/usr/bin/env python3
"""Whale shark — field plate V1R00. The biggest fish, filtering the sea a
galaxy at a time. Blue plate, plankton-haze mood: the disc is the water
column, sunlit at the top, the shark cruising right in profile with its
great scoop of a mouth open on a drifting cloud of plankton — the white
spot field across its back doing the galaxy. Remoras ride the belly.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Whale Shark — Field Plate", 1000, 1000)
rng = random.Random(11)

CX, CY, R = 500, 460, 420          # plate disc centre + radius
INK = "#0E1A22"                    # warm dark ink, never pure black

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

BG_GRAD    = lin(0, 0, 0, 1000, (0, "#03101A"), (1, "#010508"))
WATER_GRAD = lin(500, 40, 500, 880, (0, "#42789A"), (0.45, "#1E425A"), (1, "#0A1C28"))
BODY_GRAD  = lin(500, 340, 500, 540, (0, "#54707E"), (0.5, "#30444E"), (1, "#18282E"))
BELLY_GRAD = lin(500, 470, 500, 560, (0, "#8CA4AA"), (1, "#4E666C"))
FIN_GRAD   = lin(500, 330, 500, 560, (0, "#3C545E"), (1, "#14222A"))
SPOT       = "#D8E4D4"

# --- backdrop + blue water plate --------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=64, y=24, width=872, height=872,
        fill="#42789A", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=WATER_GRAD, stroke="#16303E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#9EC4D4", strokeWidth=3, opacity=28)

# god rays dying down the water column — tops seated just inside the disc's curve
def disc_top(x):
    return CY - math.sqrt(max(0.0, R * R - (x - CX) ** 2))
for i, (x0, w, op) in enumerate([(260, 70, 8), (450, 100, 10), (660, 60, 7)]):
    y0 = disc_top(x0) + 12
    d.path(f"M{x0 - w/2},{y0} L{x0 + w/2},{y0} L{x0 + w * 0.9},{y0 + 330} "
           f"L{x0 - w * 0.7},{y0 + 330} Z",
           f"God ray {i+1}", fill=lin(x0, y0, x0, y0 + 330,
           (0, "#BEE0EA"), (1, "#BEE0EA")), opacity=op, stroke=NONE)
# sun glare pooled at the top of the disc
d.shape("ellipse", "Surface glare", x=330, y=70, width=360, height=160,
        fill=rad((0, "#C6E4EC", 22), (0.6, "#C6E4EC", 9), (1, "#C6E4EC", 0)), stroke=NONE)

# --- plankton haze: the drifting galaxy the shark is filtering ----------------------
# sparse motes across the water, then a dense swirl feeding toward the mouth
for i in range(90):
    a = rng.uniform(0, math.tau); rr = math.sqrt(rng.uniform(0, 1)) * 395
    x, y = CX + rr * math.cos(a), CY + rr * math.sin(a)
    if not on_disc(x, y, 18): continue
    w = rng.uniform(2.5, 6)
    d.shape("ellipse", f"Mote {i+1}", x=x - w/2, y=y - w/2, width=w, height=w,
            fill="#CFE4E8", opacity=rng.randint(14, 38), stroke=NONE)
# the dense cloud ahead of the gape — a loose spiral of feed
for i in range(60):
    t = i / 60 * math.tau * 1.6
    rr = 18 + i * 1.1 + rng.uniform(-8, 8)
    x = 845 + rr * math.cos(t) * 0.85
    y = 440 + rr * math.sin(t) * 0.6
    if not on_disc(x, y, 12): continue
    w = rng.uniform(3, 7)
    d.shape("ellipse", f"Feed {i+1}", x=x - w/2, y=y - w/2, width=w, height=w,
            fill="#E2EFE8", opacity=rng.randint(30, 60), stroke=NONE)
# faint glow around the cloud
d.shape("ellipse", "Plankton glow", x=750, y=370, width=200, height=140,
        fill=rad((0, "#BEE0D8", 16), (1, "#BEE0D8", 0)), stroke=NONE)

# a shadowed floor of deep water far below — just a tone change, closing on the arc
dy = 780
dl, dr = rim_x(dy, side=-1), rim_x(dy, side=1)
d.path(f"M{dl:.1f},{dy} C300,764 700,764 {dr:.1f},{dy} "
       f"A{R},{R} 0 0 1 {dl:.1f},{dy} Z", "Deep floor", fill="#081822",
       opacity=55, stroke=NONE)

# === the shark ======================================================================
# tail first — long crescent, upper lobe much longer, behind the body
d.path("M212,428 C175,392 132,352 102,318 C94,309 88,316 94,328 "
       "C128,364 168,406 200,446 C188,458 176,468 170,480 "
       "C162,505 153,528 146,548 C140,557 134,551 139,540 "
       "C154,510 176,486 204,466 C212,452 214,440 212,428 Z",
       "Tail fin", fill=FIN_GRAD, stroke=INK, strokeWidth=5)
# caudal keel — the lateral ridge where tail meets body
d.path("M206,452 C218,448 230,448 240,452", "Caudal keel", fill=NONE,
       stroke="#A8C4CC", strokeWidth=4, opacity=50, cap="round")

# body — the broad hull, head blunt and square-fronted, mouth terminal
d.path("M812,398 C780,370 715,358 650,364 C560,372 458,388 370,414 "
       "C300,434 246,444 212,450 C214,458 216,466 218,474 "
       "C262,484 332,496 402,506 C482,516 566,514 642,500 "
       "C700,492 748,498 772,494 C796,488 810,468 814,448 "
       "C817,432 817,414 812,398 Z",
       "Body", fill=BODY_GRAD, stroke=INK, strokeWidth=6)
# belly countershading washing up the underside
d.path("M250,468 C340,486 440,502 540,502 C610,502 678,496 740,490 "
       "C700,504 620,514 540,516 C430,518 320,500 250,468 Z",
       "Belly", fill=BELLY_GRAD, opacity=70, stroke=NONE)
# mouth interior — a dark crescent opening on the very face of the head
d.path("M812,416 C815,432 813,452 806,468 C796,486 780,494 762,496 "
       "C756,484 754,470 758,456 C766,434 786,420 812,416 Z",
       "Mouth", fill="#101418", stroke="#0A1014", strokeWidth=3)
# faint gill-raker fan inside the scoop
for k, dd in enumerate(["M772,442 C780,454 784,468 782,482",
                        "M788,432 C796,446 800,460 798,474"]):
    d.path(dd, f"Raker {k+1}", fill=NONE, stroke="#3E5258",
           strokeWidth=3.5, opacity=55, cap="round")
# lip line — the pale seam along the terminal gape
d.path("M764,492 C780,486 796,474 806,458", "Lower lip", fill=NONE,
       stroke="#AEC8CE", strokeWidth=3.5, opacity=50, cap="round")
d.path("M760,452 C772,432 790,420 810,412", "Upper lip", fill=NONE,
       stroke="#AEC8CE", strokeWidth=4, opacity=55, cap="round")
# gill slits behind the head — five short dark arcs
for k in range(5):
    x = 700 - k * 22
    d.path(f"M{x},{420 + k*4} C{x - 6},{440 + k*4} {x - 8},{460 + k*3} {x - 6},{478 + k*2}",
           f"Gill {k+1}", fill=NONE, stroke="#0E1C22",
           strokeWidth=4, opacity=65, cap="round")
# eye — small, low, well behind the gape
d.shape("ellipse", "Eye", x=730, y=432, width=13, height=13,
        fill="#0A1214", stroke=NONE)
d.shape("ellipse", "Eye glint", x=734, y=435, width=3.5, height=3.5,
        fill="#EAF6F2", opacity=80, stroke=NONE)
# the three flank ridges — light lines converging to the peduncle
for i, dd in enumerate(["M648,382 C560,392 440,408 300,436 C270,442 246,446 226,448",
                        "M640,420 C540,432 420,450 290,470 C262,474 240,478 224,480",
                        "M636,458 C540,470 430,484 320,496"]):
    d.path(dd, f"Ridge {i+1}", fill=NONE, stroke="#9CBCC2",
           strokeWidth=3.5, opacity=40, cap="round")

# the spot field — the galaxy; rows of pale dots on the dark flank
# body mask approximated by an ellipse over the flank
def on_body(x, y):
    return ((x - 470) / 295) ** 2 + ((y - 442) / 78) ** 2 <= 1.0
n = 0
for row in range(9):
    y = 368 + row * 16
    for col in range(20):
        x = 240 + col * 23 + (11 if row % 2 else 0)
        x += rng.uniform(-4, 4); yy = y + rng.uniform(-4, 4)
        if not on_body(x, yy): continue
        if x > 640 and yy > 450: continue          # keep off the gape/jaw
        w = rng.uniform(4.5, 7.5)
        n += 1
        d.shape("ellipse", f"Spot {n}", x=x - w/2, y=yy - w/2, width=w, height=w * 0.85,
                fill=SPOT, opacity=rng.randint(45, 70), stroke=NONE)

# dorsal fins — first set far back, second a bump by the tail
d.path("M452,396 C470,356 492,326 508,310 C516,304 522,312 516,326 "
       "C506,356 496,380 488,398 Z",
       "Dorsal 1", fill=FIN_GRAD, stroke=INK, strokeWidth=4.5)
d.path("M288,442 C300,420 314,404 326,396 C332,392 336,398 330,408 "
       "C320,424 310,436 302,446 Z",
       "Dorsal 2", fill=FIN_GRAD, stroke=INK, strokeWidth=4)
# pectoral fin — long sickle sweeping back under the gills
d.path("M626,472 C600,512 560,548 514,574 C504,580 496,572 506,562 "
       "C544,526 584,496 616,474 Z",
       "Pectoral near", fill=lin(600, 470, 510, 575, (0, "#42565E"), (1, "#1A2A30")),
       stroke=INK, strokeWidth=4.5)
# far pectoral hint behind the belly
d.path("M560,496 C544,522 522,544 500,560", "Pectoral far", fill=NONE,
       stroke="#14222A", strokeWidth=6, opacity=55, cap="round")
# pelvic finlet
d.path("M386,508 C376,524 366,536 356,544 C368,542 380,532 390,516 Z",
       "Pelvic", fill="#1A2A30", stroke=INK, strokeWidth=3)

# remoras riding the shark — two slim riders under the belly, one by the gills
for i, (x, y, s) in enumerate([(560, 522, 1), (470, 530, -1)]):
    d.path(f"M{x},{y} C{x + 24*s},{y - 8} {x + 46*s},{y - 6} {x + 58*s},{y + 2} "
           f"C{x + 44*s},{y + 8} {x + 20*s},{y + 8} {x},{y} Z",
           f"Remora {i+1}", fill="#2E4248", stroke="#0E1A1E", strokeWidth=2.5)
    d.path(f"M{x + 58*s},{y + 2} L{x + 72*s},{y - 3} L{x + 70*s},{y + 6} Z",
           f"Remora tail {i+1}", fill="#2E4248", stroke="#0E1A1E", strokeWidth=2)
    d.path(f"M{x + 8*s},{y - 1} L{x + 22*s},{y - 3}",
           f"Remora disc {i+1}", fill=NONE, stroke="#8AA0A2",
           strokeWidth=2.5, opacity=60, cap="round")

# plankton grains streaming into the gape — drawn over the shark
for i, (x, y) in enumerate([(824, 426), (832, 450), (818, 468), (840, 410), (806, 404)]):
    d.shape("ellipse", f"Intake {i+1}", x=x - 3, y=y - 3, width=6, height=6,
            fill="#EAF4EE", opacity=55, stroke=NONE)

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#0A1A22", strokeWidth=6)

# --- name ---------------------------------------------------------------------------
r1 = d.text("WHALE SHARK", "Name", x=500, y=962, size=58, font="Virelai Sans",
            color="#C8DEE4", justify="center")

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

d.finish("whale-shark-V1R00")
