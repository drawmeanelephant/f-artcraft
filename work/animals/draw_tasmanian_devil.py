#!/usr/bin/env python3
"""Tasmanian devil — field plate V1R00. Front-facing crouch, the famous gape
thrown wide in the screech: eyes squeezed shut, the mouth a dark red cavern
rimmed with pale teeth, white crescent across the chest, pink-lit ears.
Button-grass plate: dusk moor, sage tufts and pale button-heads on thin
stems around the floor arc. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Tasmanian Devil — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#1A1210"   # warm near-black

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

BG_GRAD    = lin(0, 0, 0, 1000, (0, "#0B1512"), (1, "#030705"))
PLATE_GRAD = rad((0, "#A4B494"), (0.55, "#5E7052"), (1, "#27301F"))
FUR_GRAD   = rad((0, "#2E2624"), (0.6, "#1A1412"), (1, "#0B0806"))
GAPE_GRAD  = rad((0, "#8A2E38"), (0.6, "#5A1A24"), (1, "#2E0A10"))
GROUND_GRAD = lin(0, 720, 0, 880, (0, "#4A5A38"), (1, "#1E2614"))

# --- backdrop + plate --------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880, fill="#A4B494", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#1E2817", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E2EAC8", strokeWidth=3, opacity=40)

# dusk mist lying low over the moor
d.shape("ellipse", "Mist band", x=140, y=640, width=720, height=90,
        fill=radO((0, "#D8E0C0", 10), (1, "#D8E0C0", 0)), stroke=NONE)
# a cold moon riding high left
d.shape("ellipse", "Moon glow", x=180, y=120, width=200, height=200,
        fill=radO((0, "#E8F0D8", 16), (1, "#E8F0D8", 0)), stroke=NONE)
d.shape("ellipse", "Moon", x=236, y=168, width=52, height=52,
        fill=rad((0, "#F2F4DE"), (1, "#C9CFA8")), opacity=85, stroke=NONE)

# --- button-grass moor: tufts + the pale button heads on thin stems -------------------
GY = 762
gl, gr = disc_x(GY, -1), disc_x(GY, 1)
d.path(f"M{gl:.1f},{GY} C300,{GY-10} 420,{GY-2} 520,{GY-8} C620,{GY-12} 700,{GY-4} {gr:.1f},{GY} "
       f"A{PR},{PR} 0 0 1 {gl:.1f},{GY} Z", "Moor floor", fill=GROUND_GRAD, stroke=NONE)

# radiating blades behind the animal
for i, (gx, gy, s) in enumerate([(230, 756, 1), (300, 748, -1), (620, 748, 1), (700, 752, -1), (768, 748, 1)]):
    for j in range(5):
        bx = gx + j * 6 * s
        tipx = bx + (j - 2) * 10 * s
        tipy = gy - 46 - j * 7
        assert on_disc(tipx, tipy, 6), (tipx, tipy)
        d.path(f"M{bx},{gy} C{bx + 2*s},{gy - 18} {tipx},{tipy + 16} {tipx},{tipy}",
               f"Tuft {i+1}.{j+1}", fill=NONE,
               stroke="#A8BC84" if j % 2 else "#6E8052",
               strokeWidth=3, opacity=60, cap="round")
# button-grass heads: thin stems topped with the pale globes
for i, (sx, sy, h) in enumerate([(258, 748, 88), (330, 756, 110), (430, 764, 84),
                                 (566, 760, 104), (660, 752, 92), (740, 744, 76)]):
    assert on_disc(sx, sy - h, 8), (sx, sy)
    d.path(f"M{sx},{sy} C{sx - 2},{sy - h * 0.5} {sx + 3},{sy - h * 0.8} {sx},{sy - h}",
           f"Button stem {i+1}", fill=NONE, stroke="#8A9A66", strokeWidth=3,
           opacity=80, cap="round")
    d.shape("ellipse", f"Button {i+1}", x=sx - 7, y=sy - h - 8, width=14, height=14,
            fill=rad((0, "#E8EAC4"), (1, "#A8AE7E")), stroke=NONE)

# soft contact shadow under the devil
d.shape("ellipse", "Contact shadow", x=310, y=730, width=340, height=28,
        fill="#0E1408", opacity=40, stroke=NONE)

# --- tail: stout at the base, tapering along the ground to the right ----------------------
d.path("M586,672 C640,684 686,716 726,740 C738,748 736,760 722,760 "
       "C686,754 646,736 606,716 C598,700 588,684 586,672 Z",
       "Tail", fill="#2E2220", stroke=INK, strokeWidth=3)
d.path("M620,700 C654,712 686,728 712,748", "Tail light", fill=NONE,
       stroke="#5C423C", strokeWidth=4, opacity=50, cap="round")

# --- body: the squat black mass behind the head ------------------------------------------
d.path(smooth([(318, 660), (306, 590), (324, 516), (360, 456), (410, 428),
               (470, 420), (530, 426), (580, 452), (612, 508), (624, 580),
               (616, 656), (580, 700), (470, 714), (366, 700)]),
       "Body", fill=FUR_GRAD, stroke=INK, strokeWidth=5)
# flank shading
d.shape("ellipse", "Flank shade L", x=310, y=560, width=80, height=110,
        fill="#060403", opacity=35, stroke=NONE)
d.shape("ellipse", "Flank shade R", x=556, y=560, width=80, height=110,
        fill="#060403", opacity=35, stroke=NONE)

# --- forelegs and splayed paws ------------------------------------------------------------
for i, (x0, sgn) in enumerate([(352, -1), (564, 1)]):
    d.path(f"M{x0},{600} C{x0 + 8*sgn},{652} {x0 + 4*sgn},{690} {x0},{724}",
           f"Foreleg {i+1}", fill=NONE, stroke="#1E1614", strokeWidth=26, cap="round")
    # paw: three toes fanning on the ground
    for j, dx in enumerate([-16, 0, 16]):
        d.path(f"M{x0 + dx + 4*sgn},{726} L{x0 + dx + 10*sgn},{742} "
               f"L{x0 + dx - 4*sgn},{742} Z",
               f"Toe {i+1}.{j+1}", fill="#120C0A", stroke=NONE)
        d.path(f"M{x0 + dx + 9*sgn},{742} L{x0 + dx + 14*sgn},{748} "
               f"L{x0 + dx + 5*sgn},{748} Z",
               f"Claw {i+1}.{j+1}", fill="#E4DCC4", opacity=75, stroke=NONE)

# --- the white chest crescent --------------------------------------------------------------
d.path("M368,676 C420,700 512,700 566,672 C560,696 520,718 468,720 "
       "C420,722 380,702 368,676 Z",
       "Chest crescent", fill=rad((0, "#EDE4D0"), (1, "#B8AC90")),
       opacity=90, stroke=NONE)
d.path("M372,680 C420,700 510,700 560,676", "Crescent shade", fill=NONE,
       stroke="#8A8070", strokeWidth=4, opacity=40, cap="round")

# --- ears: broad rounded triangles flanking the skull ---------------------------------------
for i, (cx_, sgn) in enumerate([(364, -1), (566, 1)]):
    d.path(f"M{cx_},436 C{cx_ - 30*sgn},408 {cx_ - 34*sgn},372 {cx_ - 26*sgn},344 "
           f"C{cx_ - 10*sgn},330 {cx_ + 12*sgn},336 {cx_ + 24*sgn},352 "
           f"C{cx_ + 38*sgn},382 {cx_ + 30*sgn},418 {cx_ + 14*sgn},440 Z",
           f"Ear {i+1}", fill="#1E1614", stroke=INK, strokeWidth=4)
    d.path(f"M{cx_ - 6*sgn},424 C{cx_ - 18*sgn},402 {cx_ - 20*sgn},376 {cx_ - 16*sgn},356 "
           f"C{cx_ - 6*sgn},348 {cx_ + 6*sgn},354 {cx_ + 12*sgn},366 "
           f"C{cx_ + 20*sgn},390 {cx_ + 16*sgn},414 {cx_ + 4*sgn},428 Z",
           f"Ear inner {i+1}", fill=rad((0, "#B06A5E"), (1, "#7C3E38")),
           opacity=85, stroke=NONE)

# --- head: broad jowls, the gape thrown open --------------------------------------------------
# skull dome -> wide cheeks -> jaw corners -> chin
d.path(smooth([(364, 436), (344, 480), (338, 536), (352, 588), (382, 632),
               (430, 660), (500, 660), (548, 630), (576, 586), (586, 534),
               (578, 478), (556, 434), (500, 414), (430, 414)]),
       "Head", fill=FUR_GRAD, stroke=INK, strokeWidth=5)
# brow ridge shading over the squeezed eyes
d.path("M390,470 C420,456 502,456 534,472", "Brow ridge", fill=NONE,
       stroke="#3A2E28", strokeWidth=8, opacity=50, cap="round")
# eyes squeezed shut in the screech
for i, (ex, sgn) in enumerate([(408, -1), (524, 1)]):
    d.path(f"M{ex - 16},{496} C{ex - 4},{504} {ex + 8},{504} {ex + 18},{496}",
           f"Eye {i+1}", fill=NONE, stroke="#0A0605", strokeWidth=5, cap="round")
    d.path(f"M{ex},{506} L{ex + 4*sgn},{514}", f"Eye crease {i+1}", fill=NONE,
           stroke="#0A0605", strokeWidth=3, opacity=60, cap="round")

# muzzle pad over the gape
d.path("M424,516 C436,502 496,502 508,516 C500,532 432,532 424,516 Z",
       "Nose pad", fill="#0E0908", stroke=NONE)
d.path("M438,512 C444,516 452,517 458,514", "Nostril L", fill=NONE,
       stroke="#3A2E28", strokeWidth=3, cap="round")
d.path("M478,514 C484,517 492,516 496,512", "Nostril R", fill=NONE,
       stroke="#3A2E28", strokeWidth=3, cap="round")

# --- the gape: a dark red cavern rimmed with teeth ---------------------------------------------
d.path("M376,548 C390,532 540,532 556,548 C574,578 566,616 540,640 "
       "C508,662 426,662 396,640 C368,618 360,578 376,548 Z",
       "Gape", fill=GAPE_GRAD, stroke="#20060A", strokeWidth=4)
# tongue pressed low in the mouth floor
d.path("M404,610 C430,596 502,596 530,612 C512,636 428,638 404,610 Z",
       "Tongue", fill=rad((0, "#A44850"), (1, "#64242E")), stroke=NONE)
# teeth: pale hooks hanging from the upper rim, rising from the lower
for i, (tx, ty, h) in enumerate([(398, 552, 22), (430, 546, 18), (462, 544, 16),
                                 (494, 544, 16), (526, 546, 18), (550, 552, 22)]):
    d.path(f"M{tx - 7},{ty} L{tx},{ty + h} L{tx + 7},{ty} Z",
           f"Tooth upper {i+1}", fill="#F0E8D4", stroke="#B8AC90", strokeWidth=1)
for i, (tx, ty, h) in enumerate([(412, 640, -16), (448, 650, -14),
                                 (486, 650, -14), (522, 642, -16)]):
    d.path(f"M{tx - 6},{ty} L{tx},{ty + h} L{tx + 6},{ty} Z",
           f"Tooth lower {i+1}", fill="#E4DCC4", stroke="#B8AC90", strokeWidth=1)

# whiskers bristling off the muzzle
for i, (dd) in enumerate(["M380,560 C340,552 300,548 262,550",
                          "M382,578 C340,576 300,580 268,590",
                          "M384,594 C346,600 312,612 284,630",
                          "M554,560 C594,552 634,548 672,550",
                          "M552,578 C594,576 634,580 666,590",
                          "M550,594 C588,600 622,612 650,630"]):
    d.path(dd, f"Whisker {i+1}", fill=NONE, stroke="#D8D2C0",
           strokeWidth=3, opacity=55, cap="round")

# --- name ---------------------------------------------------------------------------------------------
r1 = d.text("TASMANIAN DEVIL", "Name", x=500, y=962, size=56, font="Virelai Sans",
            color="#E6E4C8", justify="center")

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

d.finish("tasmanian-devil-V1R00")
