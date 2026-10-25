#!/usr/bin/env python3
"""Ring-tailed lemur — field plate V1R00. Lemur catta seated on a low
sun-warmed rock in the dry forest, amber eyes on the viewer, the ringed
tail arcing up behind the back and curling beside the hip onto the stone.
Madagascar dry-forest plate, late-amber mood — dusty taupe disc, low sun
glow, scrub silhouettes on the horizon, talus closing on the disc arc.
1000x1000. House style: gradients + translucent shading, never flat
fills. Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Ring-tailed Lemur — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420          # plate disc centre + radius
INK = "#1E1712"                    # warm dark ink, never pure black

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

def on_disc(x, y, pad=0):
    return math.hypot(x - CX, y - CY) <= R - pad

def disc_x(y, side):
    return CX + side * math.sqrt(R * R - (y - CY) ** 2)

BG_GRAD   = lin(0, 0, 0, 1000, (0, "#0E0B14"), (1, "#07050B"))
PLATE_GRAD = rad((0, "#77614E"), (0.5, "#443842"), (1, "#18121C"))
ROCK_GRAD = lin(0, 700, 0, 880, (0, "#6E5F52"), (0.55, "#443C44"), (1, "#211C28"))
COAT      = rad((0, "#B4A796"), (0.55, "#8A7A68"), (1, "#584A3C"))
BELLY     = rad((0, "#EDE4D2"), (1, "#C4B49A"))

# --- backdrop + dry-forest dusk plate -----------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
for i, (x, y, w) in enumerate([(150,120,4),(850,110,5),(120,450,3),(870,505,4),
                               (180,730,4),(855,760,4),(260,150,3)]):
    d.shape("ellipse", f"Sky fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#DCD2C8", opacity=26, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#77614E", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#241C24", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E4D8CC", strokeWidth=3, opacity=36)

# low sun glow pooling behind the seated animal
d.shape("ellipse", "Sun glow", x=300, y=330, width=420, height=300,
        fill=rad((0, "#F0B87C", 38), (0.6, "#F0B87C", 12), (1, "#F0B87C", 0)),
        stroke=NONE)
# dust motes and patina flecks inside the disc
for i, (x, y, w) in enumerate([(310,180,4),(455,140,5),(590,170,4),(225,270,3),
                               (370,220,4),(520,190,3),(690,150,4),(255,420,3),
                               (745,430,4),(200,560,3)]):
    assert on_disc(x, y, 15), (x, y)
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#E8DCC8", opacity=42, stroke=NONE)

# --- horizon: spiny-forest scrub silhouettes against the glow ------------------------
hy = 636
hl, hr = disc_x(hy, -1), disc_x(hy, 1)
d.path(f"M{hl:.1f},{hy} L{hr:.1f},{hy} L{hr:.1f},{hy+4} L{hl:.1f},{hy+4} Z",
       "Horizon line", fill="#241C20", opacity=80, stroke=NONE)
# dry scrub crowns: thin angular sprigs along the horizon, sparse
for i, (sx, sw, sh) in enumerate([(225, 60, 46), (305, 44, 34), (665, 70, 50),
                                  (745, 40, 30), (600, 36, 26)]):
    d.path(f"M{sx - sw/2},{hy} L{sx - sw*0.3},{hy - sh*0.7} L{sx - sw*0.12},{hy - sh*0.45} "
           f"L{sx},{hy - sh} L{sx + sw*0.15},{hy - sh*0.5} L{sx + sw*0.32},{hy - sh*0.72} "
           f"L{sx + sw/2},{hy} Z",
           f"Scrub {i+1}", fill="#2A2024", opacity=85, stroke=NONE)
# a far octopus-tree (didierea) silhouette: trunk + radiating wands
for j, ang in enumerate([-38, -18, 0, 18, 38]):
    a = math.radians(ang - 90)
    x0, y0 = 405, hy
    x1, y1 = x0 + 68 * math.cos(a), y0 + 68 * math.sin(a)
    d.path(f"M{x0},{y0} L{x1:.0f},{y1:.0f}", f"Wand {j+1}", fill=NONE,
           stroke="#241C20", strokeWidth=4, opacity=85, cap="round")

# --- the rock: a low sun-warmed slab closing on the disc arc -------------------------
fy = 800
fl, fr = disc_x(fy, -1), disc_x(fy, 1)
d.path(f"M{fl:.1f},{fy} L300,772 L430,782 L570,770 L700,784 L{fr:.1f},{fy} "
       f"A{R},{R} 0 0 1 {fl:.1f},{fy} Z", "Rock slab", fill=ROCK_GRAD, stroke=NONE)
# sun-struck top plane, slightly lighter
d.path(f"M{fl+6:.1f},{fy} L300,772 L430,782 L570,770 L700,784 L{fr-6:.1f},{fy} "
       f"L{fr-30:.1f},{fy+16} L{fl+30:.1f},{fy+16} Z",
       "Rock top", fill=lin(0, 764, 0, 820, (0, "#8A7660"), (1, "#4A4048")),
       stroke=NONE)
d.path(f"M{fl+10:.1f},{fy} L300,772 L430,782 L570,770 L700,784 L{fr-10:.1f},{fy}",
       "Rock crest light", fill=NONE, stroke="#E8C49A", strokeWidth=4,
       opacity=30, cap="round")
# strata cracks on the slab face
for i, (x0, y0, x1, y1) in enumerate([(330, 816, 300, 848), (560, 822, 580, 856),
                                      (680, 812, 660, 846)]):
    d.path(f"M{x0},{y0} L{x1},{y1}", f"Rock crack {i+1}", fill=NONE,
           stroke="#18141C", strokeWidth=3, opacity=60, cap="round")
# dry grass tufts at the slab's edge
for i, (gx, lean) in enumerate([(268, -8), (288, 6), (722, 10), (700, -6)]):
    for k in (-1, 0, 1):
        d.path(f"M{gx},{800} Q{gx + lean + k*7},{772} {gx + lean*2 + k*10},{760}",
               f"Grass {i+1}.{k+2}", fill=NONE, stroke="#A08C5E",
               strokeWidth=3, opacity=70, cap="round")

# contact shadow under the seated body
d.shape("ellipse", "Seat shadow", x=390, y=770, width=250, height=40,
        fill="#080610", opacity=50, stroke=NONE)

# === the ringed tail: arcing up behind the back, tip curling beside the shoulder =====
# centreline through a Catmull-Rom spline; each ring is a tapered band segment
CTRL = [(648, 776), (712, 690), (742, 566), (712, 452), (636, 408), (562, 414)]

def catmull(pts, n=64):
    out = []
    P = [pts[0]] + pts + [pts[-1]]
    for i in range(len(P) - 3):
        p0, p1, p2, p3 = P[i], P[i+1], P[i+2], P[i+3]
        for j in range(n // (len(P) - 3)):
            t = j / (n // (len(P) - 3))
            t2, t3 = t*t, t*t*t
            x = 0.5*((2*p1[0]) + (-p0[0]+p2[0])*t + (2*p0[0]-5*p1[0]+4*p2[0]-p3[0])*t2
                     + (-p0[0]+3*p1[0]-3*p2[0]+p3[0])*t3)
            y = 0.5*((2*p1[1]) + (-p0[1]+p2[1])*t + (2*p0[1]-5*p1[1]+4*p2[1]-p3[1])*t2
                     + (-p0[1]+3*p1[1]-3*p2[1]+p3[1])*t3)
            out.append((x, y))
    out.append(pts[-1])
    return out

CL = catmull(CTRL)
def offset_pts(pts, width):
    left, rght = [], []
    for i, (x, y) in enumerate(pts):
        if i == 0: dx, dy = pts[1][0]-x, pts[1][1]-y
        elif i == len(pts)-1: dx, dy = x-pts[i-1][0], y-pts[i-1][1]
        else: dx, dy = pts[i+1][0]-pts[i-1][0], pts[i+1][1]-pts[i-1][1]
        m = math.hypot(dx, dy) or 1
        nx, ny = -dy/m, dx/m
        left.append((x + nx*width, y + ny*width))
        rght.append((x - nx*width, y - ny*width))
    return left, rght

BANDS = 11                       # cream base + 10 dark rings, dark tip
for b in range(BANDS):
    i0 = int(b * (len(CL)-1) / BANDS)
    i1 = max(i0+2, int((b+1) * (len(CL)-1) / BANDS))
    seg = CL[i0:i1+1]
    t0, t1 = i0/(len(CL)-1), i1/(len(CL)-1)
    w0 = 34 - 12*t0; w1 = 34 - 12*t1
    left, rght = offset_pts(seg, 0)
    left = [ (seg[i][0] + (left[i][0]-seg[i][0]), seg[i][1] + (left[i][1]-seg[i][1])) for i in range(len(seg)) ]
    # per-point taper
    lp, rp = [], []
    for i, (x, y) in enumerate(seg):
        tt = (i0 + i) / (len(CL)-1)
        w = 34 - 12*tt
        if i == 0: dx, dy = seg[1][0]-x, seg[1][1]-y
        elif i == len(seg)-1: dx, dy = x-seg[i-1][0], y-seg[i-1][1]
        else: dx, dy = seg[i+1][0]-seg[i-1][0], seg[i+1][1]-seg[i-1][1]
        m = math.hypot(dx, dy) or 1
        lp.append((x - dy/m*w, y + dx/m*w))
        rp.append((x + dy/m*w, y - dx/m*w))
    pts = lp + rp[::-1]
    col = "#E4DAC4" if b % 2 == 0 else "#2C221C"
    d.path("M" + " L".join(f"{p[0]:.0f},{p[1]:.0f}" for p in pts) + " Z",
           f"Tail band {b+1}", fill=col, stroke=NONE)
# soft spine highlight along the tail's outer curve
d.path("M" + " L".join(f"{p[0]:.0f},{p[1]:.0f}" for p in CL[6:40:3]),
       "Tail sheen", fill=NONE, stroke="#F4ECDA", strokeWidth=3,
       opacity=28, cap="round")

# === the lemur: seated three-quarter, amber eyes on the viewer ========================
# haunches and folded hind leg mass on the rock
d.path("M560,560 "                                   # back of shoulder
       "C620,570 660,620 666,680 "                   # back rounding down
       "C670,730 650,768 610,780 "                   # rump onto the rock
       "C560,790 500,790 460,782 "                   # seat
       "C420,774 398,748 396,712 "                   # belly front
       "C394,668 404,624 428,596 "                   # chest rising
       "C452,568 486,556 516,556 "                   # throat/chest top
       "C532,556 548,558 560,560 Z",
       "Body", fill=COAT, stroke=INK, strokeWidth=6)
# pale belly wash down the front
d.path("M452,600 C430,634 420,684 426,724 C430,752 452,772 486,778 "
       "C464,762 452,730 452,688 C452,652 458,624 452,600 Z",
       "Belly wash", fill=BELLY, opacity=50, stroke=NONE)
# flank shading toward the back
d.path("M620,600 C648,636 658,690 646,734 C640,756 624,772 600,780 "
       "C624,752 632,706 624,656 C620,632 616,614 620,600 Z",
       "Flank shade", fill="#3E3228", opacity=35, stroke=NONE)

# hind feet planted on the rock, toes forward
for sgn, lab in ((-1, "L"), (1, "R")):
    fx = 436 + (0 if sgn < 0 else 180)
    fy_ = 782
    d.path(f"M{fx},{fy_-34} C{fx-16},{fy_-22} {fx-18},{fy_-4} {fx-8},{fy_+6} "
           f"C{fx+6},{fy_+14} {fx+30},{fy_+14} {fx+40},{fy_+4} "
           f"C{fx+46},{fy_-6} {fx+44},{fy_-22} {fx+34},{fy_-32} "
           f"C{fx+24},{fy_-38} {fx+8},{fy_-38} {fx},{fy_-34} Z",
           f"Hind foot {lab}", fill="#8A7560", stroke=INK, strokeWidth=3.5)
    for k in range(5):                                # five toes, >=3pt
        tx = fx - 6 + k * 11
        d.path(f"M{tx},{fy_-16} q3,10 1,20", f"Hind toe {lab}{k+1}",
               fill=NONE, stroke="#2A1E14", strokeWidth=3, opacity=80,
               cap="round")

# forearms reaching straight down to the rock, five-digit hands flat
for sgn, lab in ((-1, "L"), (1, "R")):
    ax = 452 + (0 if sgn < 0 else 92)
    d.path(f"M{ax},{600} C{ax-14},{650} {ax-16},{716} {ax-10},{764} "
           f"L{ax+26},{764} C{ax+30},{712} {ax+30},{654} {ax+24},{606} Z",
           f"Forearm {lab}", fill=rad((0, "#9C8C78"), (1, "#5C4C3E")),
           stroke=INK, strokeWidth=4)
    hx, hyy = ax + 6, 776
    d.path(f"M{hx-14},{hyy-6} C{hx-16},{hyy+8} {hx-6},{hyy+18} {hx+8},{hyy+18} "
           f"C{hx+22},{hyy+18} {hx+30},{hyy+8} {hx+28},{hyy-6} "
           f"C{hx+20},{hyy-14} {hx-4},{hyy-14} {hx-14},{hyy-6} Z",
           f"Hand {lab}", fill="#7A6752", stroke=INK, strokeWidth=3.5)
    for k in range(5):                                # five fingers, >=3pt
        fxx = hx - 10 + k * 9
        d.path(f"M{fxx},{hyy+2} q2,8 0,14", f"Finger {lab}{k+1}",
               fill=NONE, stroke="#2A1E14", strokeWidth=3, opacity=80,
               cap="round")

# === head: round grey skull, white face, dark mask, amber eyes =======================
d.path("M500,388 "                                   # crown
       "C556,390 596,424 604,472 "                   # back of skull
       "C610,514 596,550 564,570 "                   # jaw
       "C534,588 494,590 466,576 "                   # chin
       "C432,560 414,528 416,488 "                   # cheek
       "C418,444 448,402 490,390 "                   # brow
       "C494,389 497,388 500,388 Z",
       "Head", fill=rad((0, "#B8AC9C"), (0.6, "#8C7C6A"), (1, "#54463A")),
       stroke=INK, strokeWidth=5)
# pointed ears with pale tufts
for sgn, lab in ((-1, "L"), (1, "R")):
    ex, ey = 500 + sgn*66, 408
    d.path(f"M{ex-sgn*24},{ey+34} C{ex-sgn*30},{ey+6} {ex-sgn*20},{ey-18} {ex},{ey-26} "
           f"C{ex+sgn*18},{ey-16} {ex+sgn*26},{ey+8} {ex+sgn*22},{ey+32} Z",
           f"Ear {lab}", fill="#6A594A", stroke=INK, strokeWidth=4)
    d.path(f"M{ex-sgn*10},{ey+26} C{ex-sgn*14},{ey+8} {ex-sgn*8},{ey-6} {ex+sgn*2},{ey-12} "
           f"C{ex+sgn*8},{ey} {ex+sgn*10},{ey+14} {ex+sgn*8},{ey+26} Z",
           f"Ear tuft {lab}", fill="#EAE0CE", opacity=80, stroke=NONE)
# white face patch over the front of the skull
d.path("M500,420 C544,422 572,452 576,492 C578,524 564,550 536,562 "
       "C510,572 480,570 458,556 C436,540 426,514 430,486 "
       "C436,450 464,422 500,420 Z",
       "Face patch", fill="#EDE4D4", opacity=92, stroke=NONE)
# dark mask: triangular patches around the eyes converging to the muzzle
for sgn, lab in ((-1, "L"), (1, "R")):
    cx0 = 500 + sgn*30
    d.path(f"M{cx0-sgn*20},486 C{cx0-sgn*18},464 {cx0-sgn*8},450 {cx0+sgn*4},448 "
           f"C{cx0+sgn*16},452 {cx0+sgn*22},468 {cx0+sgn*20},488 "
           f"C{cx0+sgn*14},502 {cx0+sgn*4},514 {cx0-sgn*2},518 "
           f"C{cx0-sgn*12},512 {cx0-sgn*20},500 {cx0-sgn*20},486 Z",
           f"Mask {lab}", fill="#2A2018", opacity=94, stroke=NONE)
# dark muzzle wedge from between the eyes down to the nose
d.path("M490,516 C486,538 480,556 472,568 C484,576 500,578 514,574 "
       "C524,570 530,564 532,556 C524,542 512,528 500,520 "
       "C496,518 493,517 490,516 Z",
       "Muzzle shade", fill="#8C7C6A", opacity=45, stroke=NONE)
d.path("M486,560 C488,552 496,548 504,550 C514,552 520,558 520,566 "
       "C520,574 512,580 502,580 C492,580 484,572 486,560 Z",
       "Nose", fill="#241A12", stroke=NONE)
d.path("M502,580 C502,588 498,594 490,598", "Mouth", fill=NONE,
       stroke="#3A2A1C", strokeWidth=3, opacity=85, cap="round")
# amber eyes inside the mask
for sgn, lab in ((-1, "L"), (1, "R")):
    ex = 500 + sgn*30
    d.shape("ellipse", f"Eye amber {lab}", x=ex-13, y=470, width=26, height=27,
            fill=rad((0, "#F0A848"), (1, "#B46820")), stroke="#140E08",
            strokeWidth=3)
    d.shape("ellipse", f"Pupil {lab}", x=ex-5, y=476, width=11, height=14,
            fill="#140E08", stroke=NONE)
    d.shape("ellipse", f"Glint {lab}", x=ex+2, y=474, width=6, height=6,
            fill="#FFFFFF", opacity=90, stroke=NONE)
# brow shading and cheek fur strokes
d.path("M452,470 C462,458 480,452 500,452 C520,452 540,458 550,470",
       "Brow shade", fill=NONE, stroke="#6A5847", strokeWidth=4,
       opacity=50, cap="round")
for i, (x, y, dx, dy) in enumerate([(438,520,-12,6),(434,538,-12,4),
                                    (566,522,12,6),(570,540,12,4)]):
    d.path(f"M{x},{y} L{x+dx},{y+dy}", f"Cheek fur {i+1}", fill=NONE,
           stroke="#D8CCB8", strokeWidth=2.5, opacity=55, cap="round")
# warm rim light along the back from the low sun
d.path("M560,566 C614,580 650,626 656,684", "Back rim light", fill=NONE,
       stroke="#F0B87C", strokeWidth=6, opacity=32, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#120D16", strokeWidth=6)

# --- captions -----------------------------------------------------------------------
r1 = d.text("RING-TAILED LEMUR", "Name", x=500, y=930, size=56,
            font="Virelai Sans", color="#E4D8CC", justify="center")
r2 = d.text("LEMUR CATTA", "Second line", x=500, y=968, size=22,
            font="Virelai Sans", color="#B09A84", justify="center")
d.cmd("text.setStyle", "Second line tracking", id=r2["id"], tracking=320)

def find(o, oid):
    if isinstance(o, dict):
        if o.get("id") == oid and "bounds" in o: return o
        o = list(o.values())
    if isinstance(o, list):
        for v in o:
            hit = find(v, oid)
            if hit: return hit
layers = d.call("inspect_document", {}, "inspect")["layers"]
for r, lab, wmax in [(r1, "name", 800), (r2, "line2", 760)]:
    b = find(layers, r["id"])["bounds"]
    print(lab, "bounds", {k: round(v) for k, v in b.items()})
    assert b["width"] <= wmax and b["x"] >= 100 and b["y"] + b["height"] <= 990, b

d.finish("ring-tailed-lemur-V1R00")
