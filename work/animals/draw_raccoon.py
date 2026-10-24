#!/usr/bin/env python3
"""Raccoon — field plate V1R00. The burglar that washes its hands first:
seated up on its haunches at the curb, forepaws folded together over a
stolen red apple, ringed tail sweeping the lawn, a knocked-over garbage
can spilling nearby under a big amber trash-moon. Suburban night plate,
floor closes on the disc arc. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Raccoon — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420          # plate disc centre + radius
INK = "#16120E"                    # warm dark ink, never pure black

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

def quad(p0, p1, p2, t):
    x = (1-t)**2*p0[0] + 2*(1-t)*t*p1[0] + t*t*p2[0]
    y = (1-t)**2*p0[1] + 2*(1-t)*t*p1[1] + t*t*p2[1]
    tx = 2*(1-t)*(p1[0]-p0[0]) + 2*t*(p2[0]-p1[0])
    ty = 2*(1-t)*(p1[1]-p0[1]) + 2*t*(p2[1]-p1[1])
    return (x, y), (tx, ty)

BG_GRAD   = lin(0, 0, 0, 1000, (0, "#0D1220"), (1, "#04060B"))
PLATE_GRAD = rad((0, "#5A6680"), (0.55, "#2A3448"), (1, "#0F1722"))
FLOOR_GRAD = lin(0, 640, 0, 880, (0, "#1B2B22"), (1, "#0A140E"))
COAT      = rad((0, "#8A7E6C"), (0.55, "#5E554A"), (1, "#362F28"))
DARKFUR   = lin(0, 380, 0, 700, (0, "#453E36"), (1, "#1E1A16"))
MASK      = "#211C17"
CAN_GRAD  = lin(0, 540, 0, 700, (0, "#9AA2AE"), (0.55, "#6E7684"), (1, "#3E4550"))

# --- backdrop + night plate -----------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
for i, (x, y, w) in enumerate([(150,110,4),(850,120,5),(110,430,3),(880,470,4),
                               (180,720,4),(870,740,4),(260,150,3)]):
    d.shape("ellipse", f"Sky fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#C8D2DC", opacity=28, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#5A6680", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#141C28", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C2CCDA", strokeWidth=3, opacity=38)

# trash-moon: big amber harvest disc hanging low over the cul-de-sac
MX, MY = 662, 208
for i, (r_, op) in enumerate([(95, 6), (78, 10), (62, 15)]):
    d.shape("ellipse", f"Moon glow {i+1}", x=MX-r_, y=MY-r_, width=2*r_, height=2*r_,
            fill="#F0C87A", opacity=op, stroke=NONE)
d.shape("ellipse", "Moon", x=MX-52, y=MY-52, width=104, height=104,
        fill=rad((0, "#F6DCA0"), (0.75, "#EDBE6E"), (1, "#C89248")), stroke=NONE)
for i, (ox, oy, w) in enumerate([(-16, -10, 18), (14, 8, 13), (-2, 20, 10)]):
    d.shape("ellipse", f"Moon mare {i+1}", x=MX+ox-w/2, y=MY+oy-w/2,
            width=w, height=w, fill="#BE9248", opacity=32, stroke=NONE)
for i, (x, y, w) in enumerate([(285,135,4),(430,110,5),(560,150,4),(200,280,3),
                               (350,215,4),(480,180,3),(160,430,4)]):
    assert on_disc(x, y, 15), (x, y)
    d.shape("ellipse", f"Star {i+1}", x=x, y=y, width=w, height=w,
            fill="#DEE4DC", opacity=45, stroke=NONE)

# suburb skyline: gabled rooftops + a phone-pole silhouette on the crest
d.path("M185,596 L185,540 L235,502 L285,540 L285,596 Z", "House L",
       fill="#0D1520", opacity=95, stroke=NONE)
d.path("M285,596 L285,552 L360,512 L435,552 L435,596 Z", "House mid",
       fill="#0D1520", opacity=95, stroke=NONE)
d.path("M700,596 L700,548 L760,514 L820,548 L820,596 Z", "House R",
       fill="#0D1520", opacity=95, stroke=NONE)
# one lit window in the far house — somebody's still up
d.shape("rectangle", "Lit window", x=738, y=560, width=14, height=16,
        fill="#F0C87A", opacity=55, stroke=NONE)
d.path("M612,600 L612,470 M596,486 L628,486", "Phone pole", fill=NONE,
       stroke="#0D1520", strokeWidth=7, opacity=95, cap="round")

# --- lawn floor closing on the arc ----------------------------------------------
fy = 646
fl, fr = disc_x(fy, -1), disc_x(fy, 1)
d.path(f"M{fl:.1f},{fy} C260,632 400,644 540,636 C660,632 780,642 {fr:.1f},{fy} "
       f"A{R},{R} 0 0 1 {fl:.1f},{fy} Z", "Floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{fl+10:.1f},{fy-2} C260,630 400,640 540,634 C660,630 770,638 {fr-10:.1f},{fy-2}",
       "Floor light", fill=NONE, stroke="#A8C8AE", strokeWidth=4, opacity=28, cap="round")
# moonlit dew flecks on the grass
for i, (x, y, w) in enumerate([(240,700,5),(330,740,4),(620,730,5),(740,700,4),
                               (300,790,5),(680,790,4),(500,760,4)]):
    d.shape("ellipse", f"Dew {i+1}", x=x, y=y, width=w, height=w,
            fill="#C8D8C8", opacity=25, stroke=NONE)

# --- the knocked-over garbage can, mouth toward the raccoon ---------------------
# can body lying on its side, axis tilted ~12 degrees
d.path(rot_rect_path(216, 622, 150, 92, -12), "Can body",
       fill=CAN_GRAD, stroke=INK, strokeWidth=4)
# ribbing bands along the barrel
for i, (cx, cy) in enumerate([(196, 628), (234, 620)]):
    d.path(rot_rect_path(cx, cy, 10, 92, -12), f"Can rib {i+1}",
           fill="#4A525E", opacity=55, stroke=NONE)
# the open mouth — thin ellipse, dark inside, pale rolled rim
d.path("M146,566 C128,592 124,636 140,668 C152,692 172,692 180,668 "
       "C190,638 188,594 172,570 C162,556 154,554 146,566 Z",
       "Can mouth", fill="#0A0E14", stroke="#8E96A2", strokeWidth=4)
# lid rolled off and leaning against the floor
d.shape("ellipse", "Can lid", x=250, y=662, width=92, height=30,
        fill=lin(0, 660, 0, 700, (0, "#8A929E"), (1, "#4C545E")),
        stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Lid handle", x=282, y=658, width=16, height=10,
        fill="#5A626E", stroke=INK, strokeWidth=2.5)
# spilled loot: a tipped tin + scattered scraps near the mouth
d.path("M318,676 L352,668 L358,692 L324,700 Z", "Spilled tin",
       fill="#7E8894", stroke=INK, strokeWidth=3)
d.path("M352,668 C360,664 368,668 368,676 C368,684 362,690 358,692 Z",
       "Tin mouth", fill="#0A0E14", stroke="#6E7884", strokeWidth=2.5)
for i, (x, y) in enumerate([(300,706),(342,712),(382,706),(276,724)]):
    d.path(f"M{x},{y} l10,-6 l8,8 l-10,6 Z", f"Scrap {i+1}",
           fill="#B8BCB2", opacity=65, stroke=NONE)

# contact shadow under the sitter
d.shape("ellipse", "Body shadow", x=380, y=652, width=320, height=58,
        fill="#04080A", opacity=48, stroke=NONE)

# === the raccoon ================================================================
# --- tail: thick ringed brush sweeping out of the rump along the floor ----------
TAIL_P0, TAIL_P1, TAIL_P2 = (576, 610), (724, 640), (742, 726)
TAIL_W0, TAIL_W2 = 92, 30                 # width at base vs tip
ts = [i / 14 for i in range(15)]
pts, nrm, wid = [], [], []
for t in ts:
    (x, y), (tx, ty) = quad(TAIL_P0, TAIL_P1, TAIL_P2, t)
    ln = math.hypot(tx, ty) or 1
    nx, ny = -ty / ln, tx / ln
    w = TAIL_W0 + (TAIL_W2 - TAIL_W0) * t
    pts.append((x, y)); nrm.append((nx, ny)); wid.append(w / 2)
tail_d = (f"M{pts[0][0]+nrm[0][0]*wid[0]:.1f},{pts[0][1]+nrm[0][1]*wid[0]:.1f} " +
          " ".join(f"L{p[0]+n[0]*w:.1f},{p[1]+n[1]*w:.1f}" for p, n, w in zip(pts, nrm, wid)) +
          f" L{pts[-1][0]-nrm[-1][0]*wid[-1]:.1f},{pts[-1][1]-nrm[-1][1]*wid[-1]:.1f} " +
          " ".join(f"L{p[0]-n[0]*w:.1f},{p[1]-n[1]*w:.1f}" for p, n, w in
                   reversed(list(zip(pts, nrm, wid)))) + " Z")
d.path(tail_d, "Tail", fill=lin(570, 600, 750, 730, (0, "#7A6E5E"), (1, "#4A4038")),
       stroke=INK, strokeWidth=5)
# rings: quads spanning the band at sampled stations
for i, (a, b) in enumerate([(2, 4), (5, 7), (8, 10), (11, 13)]):
    pA, nA, wA = pts[a], nrm[a], wid[a]
    pB, nB, wB = pts[b], nrm[b], wid[b]
    d.path(f"M{pA[0]+nA[0]*wA:.1f},{pA[1]+nA[1]*wA:.1f} "
           f"L{pB[0]+nB[0]*wB:.1f},{pB[1]+nB[1]*wB:.1f} "
           f"L{pB[0]-nB[0]*wB:.1f},{pB[1]-nB[1]*wB:.1f} "
           f"L{pA[0]-nA[0]*wA:.1f},{pA[1]-nA[1]*wA:.1f} Z",
           f"Tail ring {i+1}", fill="#262019", opacity=88, stroke=NONE)
# dark tail tip
pE, nE, wE = pts[-1], nrm[-1], wid[-1]
p13, n13, w13 = pts[13], nrm[13], wid[13]
d.path(f"M{p13[0]+n13[0]*w13:.1f},{p13[1]+n13[1]*w13:.1f} "
       f"L{pE[0]+nE[0]*wE:.1f},{pE[1]+nE[1]*wE:.1f} "
       f"L{pE[0]-nE[0]*wE:.1f},{pE[1]-nE[1]*wE:.1f} "
       f"L{p13[0]-n13[0]*w13:.1f},{p13[1]-n13[1]*w13:.1f} Z",
       "Tail tip", fill="#1A1611", stroke=NONE)

# --- hind feet flat on the lawn at the base --------------------------------------
for sgn, lab in ((-1, "L"), (1, "R")):
    fx = 500 + sgn * 92
    d.path(f"M{fx-52},668 C{fx-56},646 {fx-40},634 {fx-20},632 "
           f"C{fx+6},630 {fx+30},636 {fx+40},648 C{fx+48},658 {fx+42},668 {fx+28},672 "
           f"C{fx+2},678 {fx-44},680 {fx-52},668 Z",
           f"Hind foot {lab}", fill="#3A332C", stroke=INK, strokeWidth=4)
    for j in range(3):
        d.path(f"M{fx-30+j*22},{642 + j%2*4} q6,-8 12,0",
               f"Toe {lab}{j+1}", fill=NONE, stroke="#16120E",
               strokeWidth=3, opacity=70, cap="round")

# --- body: a hunched pear sitting up on its haunches -----------------------------
d.path("M500,376 "                                   # crown between the ears
       "C556,378 602,412 622,462 "                   # right shoulder
       "C644,514 650,580 630,634 "                   # right flank to haunch
       "C606,676 556,690 500,690 "                   # seat across the floor
       "C444,690 394,676 370,634 "                   # left haunch
       "C350,580 356,514 378,462 "                   # left flank
       "C398,412 444,378 500,376 Z",
       "Body", fill=COAT, stroke=INK, strokeWidth=6)
# darker grizzle saddle over the shoulders and spine
d.path("M408,470 C430,420 462,394 500,392 C538,394 570,420 592,470 "
       "C560,438 530,424 500,424 C470,424 440,438 408,470 Z",
       "Saddle", fill=DARKFUR, opacity=55, stroke=NONE)
# flank shading + a pale belly wash kept small
d.shape("ellipse", "Belly light", x=440, y=520, width=130, height=110,
        fill="#B8AE9C", opacity=14, stroke=NONE)
d.path("M378,600 C400,652 450,676 500,676 C550,676 600,652 622,600",
       "Seat line", fill=NONE, stroke="#26201A", strokeWidth=5, opacity=35, cap="round")
# guard-hair flicks over the silhouette
for i, (x, y, dx, dy) in enumerate([(382,480,-14,-8),(366,540,-14,-4),(372,600,-12,0),
                                    (620,480,14,-8),(636,540,14,-4),(628,606,12,0),
                                    (448,384,-8,-10),(554,384,8,-10)]):
    d.path(f"M{x},{y} L{x+dx},{y+dy}", f"Guard hair {i+1}",
           fill=NONE, stroke="#9A8E7C", strokeWidth=2.5, opacity=55, cap="round")

# --- forelegs folded together over the stolen apple -------------------------------
for sgn, lab in ((-1, "L"), (1, "R")):
    ax = 500 + sgn * 42
    d.path(f"M{ax+sgn*38},520 C{ax+sgn*16},548 {ax+sgn*4},576 {ax-sgn*6},604 "
           f"C{ax-sgn*10},616 {ax-sgn*4},624 {ax+sgn*6},624 "
           f"C{ax+sgn*22},622 {ax+sgn*40},598 {ax+sgn*52},560 "
           f"C{ax+sgn*58},540 {ax+sgn*52},524 {ax+sgn*38},520 Z",
           f"Foreleg {lab}", fill="#4C443A", stroke=INK, strokeWidth=4)
# the loot: one red apple cupped in both dark hands
d.shape("ellipse", "Apple", x=462, y=580, width=74, height=66,
        fill=rad((0, "#E4604E"), (0.6, "#C0382C"), (1, "#7E1E16")),
        stroke=INK, strokeWidth=3.5)
d.path("M498,582 C500,572 506,566 514,562", "Apple stem", fill=NONE,
       stroke="#4A3420", strokeWidth=4, cap="round")
d.shape("ellipse", "Apple shine", x=478, y=594, width=16, height=22,
        fill="#F6DCC8", opacity=45, stroke=NONE)
# dark mitt hands cupping the apple's flanks
for sgn, lab in ((-1, "L"), (1, "R")):
    hx = 500 + sgn * 42
    d.path(f"M{hx+sgn*6},596 C{hx+sgn*14},610 {hx+sgn*6},624 {hx-sgn*8},630 "
           f"C{hx-sgn*22},634 {hx-sgn*34},630 {hx-sgn*34},616 "
           f"C{hx-sgn*34},606 {hx-sgn*24},598 {hx-sgn*12},594 "
           f"C{hx},590 {hx+sgn*2},592 {hx+sgn*6},596 Z",
           f"Hand {lab}", fill="#2E2822", stroke=INK, strokeWidth=3)
    for j in range(2):
        d.path(f"M{hx-sgn*22},{606+j*8} q{sgn*10},4 {sgn*18},0",
               f"Finger {lab}{j+1}", fill=NONE, stroke="#120E0A",
               strokeWidth=2.5, opacity=70, cap="round")

# --- head: broad cheeks narrowing to the pointed snout ----------------------------
d.path("M500,352 "                                   # crown
       "C552,352 592,384 598,428 "                   # right cheek
       "C602,462 588,492 558,508 "                   # cheek into jaw
       "C540,518 520,522 500,522 "                   # chin
       "C480,522 460,518 442,508 "                   # jaw left
       "C412,492 398,462 402,428 "                   # left cheek
       "C408,384 448,352 500,352 Z",
       "Head", fill=rad((0, "#9A8E7A"), (0.6, "#6E6254"), (1, "#463E34")),
       stroke=INK, strokeWidth=5)
# ears: small rounded shells tucked into the head's corners, pale inner moon
for sgn, lab in ((-1, "L"), (1, "R")):
    ex = 500 + sgn * 72
    d.path(f"M{ex-sgn*4},376 C{ex-sgn*18},366 {ex-sgn*30},350 {ex-sgn*30},334 "
           f"C{ex-sgn*28},314 {ex-sgn*10},306 {ex+sgn*4},312 "
           f"C{ex+sgn*20},320 {ex+sgn*26},340 {ex+sgn*22},360 "
           f"C{ex+sgn*18},372 {ex+sgn*6},380 {ex-sgn*4},376 Z",
           f"Ear {lab}", fill="#4C443A", stroke=INK, strokeWidth=4)
    d.path(f"M{ex-sgn*4},362 C{ex-sgn*12},352 {ex-sgn*14},338 {ex-sgn*10},326 "
           f"C{ex},332 {ex+sgn*8},346 {ex+sgn*8},358 "
           f"C{ex+sgn*4},364 {ex-sgn*2},366 {ex-sgn*4},362 Z",
           f"Ear in {lab}", fill="#8A7E6E", opacity=80, stroke=NONE)
# the mask: one dark band across the eyes, flaring toward the ears
d.path("M416,430 C440,414 470,406 500,406 C530,406 560,414 584,430 "
       "C592,446 588,464 570,472 C548,480 524,482 500,482 "
       "C476,482 452,480 430,472 C412,464 408,446 416,430 Z",
       "Mask", fill=MASK, opacity=96, stroke=NONE)
# white brow strokes over the mask — the burglar's eyebrow flash
for sgn, lab in ((-1, "L"), (1, "R")):
    bx = 500 + sgn * 38
    d.path(f"M{bx-sgn*20},408 C{bx-sgn*6},398 {bx+sgn*10},396 {bx+sgn*22},404 "
           f"C{bx+sgn*10},402 {bx-sgn*4},404 {bx-sgn*20},408 Z",
           f"Brow {lab}", fill="#E8E2D2", opacity=85, stroke=NONE)
# eyes inside the mask
for sgn, lab in ((-1, "L"), (1, "R")):
    ex = 500 + sgn * 38
    d.shape("ellipse", f"Eye {lab}", x=ex-13, y=428, width=26, height=30,
            fill="#120E0A", stroke=NONE)
    d.shape("ellipse", f"Glint {lab}", x=ex-5, y=434, width=7, height=7,
            fill="#FFFFFF", opacity=92, stroke=NONE)
# white muzzle running down from the mask to the nose
d.path("M470,478 C478,470 490,466 500,466 C510,466 522,470 530,478 "
       "C538,492 536,508 522,516 C510,522 490,522 478,516 "
       "C464,508 462,492 470,478 Z",
       "Muzzle", fill=rad((0, "#ECE6D6"), (1, "#B8B09E")), stroke=NONE)
d.path("M484,494 C484,486 492,482 500,482 C508,482 516,486 516,494 "
       "C516,502 508,508 500,508 C492,508 484,502 484,494 Z",
       "Nose", fill="#1A1512", stroke=NONE)
d.path("M500,508 C500,514 496,518 490,520 M500,508 C500,514 504,518 510,520",
       "Mouth", fill=NONE, stroke="#4A423A", strokeWidth=3, cap="round")
# cheek whiskers — short droops kept on the face
for sgn, lab in ((-1, "L"), (1, "R")):
    for j, (y0, dy) in enumerate([(488, -2), (496, 4)]):
        d.path(f"M{500+sgn*60},{y0} C{500+sgn*82},{y0+dy} {500+sgn*100},{y0+dy+4} {500+sgn*112},{y0+dy+8}",
               f"Whisker {lab}{j+1}", fill=NONE, stroke="#C8C2B2",
               strokeWidth=2.5, opacity=55, cap="round")
# moonlight rim on the right shoulder and head
d.path("M560,392 C592,414 610,452 614,496", "Rim light head", fill=NONE,
       stroke="#F0D8A0", strokeWidth=5, opacity=30, cap="round")
d.path("M618,478 C640,530 644,586 626,634", "Rim light body", fill=NONE,
       stroke="#F0D8A0", strokeWidth=6, opacity=22, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#0A1018", strokeWidth=6)

# --- name -------------------------------------------------------------------------
r1 = d.text("RACCOON", "Name", x=500, y=962, size=58, font="Virelai Sans",
            color="#D8DCE4", justify="center")

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

d.finish("raccoon-V1R00")
