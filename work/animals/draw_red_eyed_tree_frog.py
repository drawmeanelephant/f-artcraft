#!/usr/bin/env python3
"""Red-eyed tree frog — field plate V1R00. Front-on squat on a broad bromeliad
leaf, both traffic-light eyes forward: leaf-green dome, red iris with vertical
pupil, blue flanks barred cream, orange toe pads splayed on the leaf. Rain-night
plate — mist, rain streaks, strap leaves in the dark. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Red-eyed Tree Frog — Field Plate", 1000, 1000)
rng = random.Random(17)

PCX, PCY, PR = 500, 460, 420
INK = "#0E1A12"   # warm near-black green

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

BG_GRAD    = lin(0, 0, 0, 1000, (0, "#0A1418"), (1, "#02060A"))
PLATE_GRAD = rad((0, "#3E5E44"), (0.55, "#24402C"), (1, "#0E2014"))
FROG_GRAD  = rad((0, "#8ADe6E"), (0.5, "#4CAE4E"), (1, "#227A36"))
BELLY_GRAD = lin(0, 520, 0, 660, (0, "#B8E8A0"), (1, "#5EA85C"))
EYE_GRAD   = rad((0, "#F4502E"), (0.6, "#D82412"), (1, "#8E0E08"))
FLANK_GRAD = lin(0, 480, 0, 620, (0, "#3A7ED8"), (1, "#1E4E96"))
LEAF_GRAD  = lin(0, 580, 0, 720, (0, "#4E7E3E"), (1, "#1E3A18"))
FLOOR_GRAD = lin(0, 750, 0, 880, (0, "#1E2A16"), (1, "#0A1208"))

# --- backdrop + rain-night plate ------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#4E7E5C", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#1E3424", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C8E0BC", strokeWidth=3, opacity=28)

# moon-mist glow high in the plate, fading before the rim
d.shape("ellipse", "Mist glow", x=300, y=110, width=400, height=240,
        fill=radO((0, "#B8DCC8", 22), (0.6, "#B8DCC8", 9), (1, "#B8DCC8", 0)), stroke=NONE)

# rain streaks falling through the plate
for i, (x, y, ln) in enumerate([(260, 160, 130), (380, 105, 90), (560, 120, 110),
                                (720, 150, 95), (300, 280, 80), (650, 300, 85),
                                (810, 260, 70), (170, 330, 75)]):
    assert on_disc(x, y, 25) and on_disc(x - ln * 0.12, y + ln, 25), (x, y)
    d.path(f"M{x},{y} L{x - ln * 0.12:.0f},{y + ln}", f"Rain streak {i+1}",
           fill=NONE, stroke="#BCD8D0", strokeWidth=1.8, opacity=15, cap="round")

# bromeliad strap leaves radiating in the dark behind the frog
for i, (bx, by, ang, L, w_) in enumerate([(290, 690, -118, 240, 30), (330, 700, -95, 280, 34),
                                          (670, 690, -62, 250, 30), (710, 680, -80, 220, 28),
                                          (240, 660, -135, 190, 26), (770, 650, -48, 180, 24)]):
    r_ = math.radians(ang)
    ux, uy = math.cos(r_), math.sin(r_)
    nx, ny = -uy, ux
    tip = (bx + ux * L, by + uy * L)
    mid = (bx + ux * L / 2, by + uy * L / 2)
    assert on_disc(*tip, 10), (bx, by, ang)
    d.path(f"M{bx},{by} Q{mid[0] + nx * w_:.1f},{mid[1] + ny * w_:.1f} {tip[0]:.1f},{tip[1]:.1f} "
           f"Q{mid[0] - nx * w_:.1f},{mid[1] - ny * w_:.1f} {bx},{by} Z",
           f"Strap leaf {i+1}",
           fill=lin(bx, by, tip[0], tip[1], (0, "#2E5228"), (1, "#122A14")),
           opacity=80, stroke=NONE)
    d.path(f"M{bx},{by} L{tip[0]:.1f},{tip[1]:.1f}", f"Strap rib {i+1}",
           fill=NONE, stroke="#5E8E4E", strokeWidth=3, opacity=30, cap="round")
# the bromeliad's red heart deep in the cup
d.shape("ellipse", "Bromeliad heart", x=452, y=660, width=96, height=40,
        fill=radO((0, "#C83A2E", 55), (1, "#7E1E16", 15)), stroke=NONE)

# --- floor: wet litter closing on the disc's own arc -----------------------------
fy = 762
x0, x1 = disc_x(fy, -1), disc_x(fy, 1)
d.path(f"M{x0:.1f},{fy} C320,748 680,748 {x1:.1f},{fy} "
       f"A{PR},{PR} 0 0 1 {x0:.1f},{fy} Z", "Floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{x0 + 6:.1f},{fy} C320,748 680,748 {x1 - 6:.1f},{fy}",
       "Floor sheen", fill=NONE, stroke="#8EA87E", strokeWidth=3, opacity=22, cap="round")
for i, (x, y, w) in enumerate([(240, 790, 80), (700, 800, 90), (430, 810, 70)]):
    d.path(f"M{x},{y} Q{x + w * 0.4},{y - w * 0.22} {x + w},{y} "
           f"Q{x + w * 0.5},{y + w * 0.16} {x},{y} Z",
           f"Litter leaf {i+1}", fill="#2E3A20", opacity=50, stroke=NONE)

# --- the broad bromeliad leaf the frog sits on ------------------------------------
d.path("M250,690 C300,640 430,618 560,624 C670,630 750,656 782,690 "
       "C740,724 620,738 500,734 C390,730 290,716 250,690 Z",
       "Perch leaf", fill=LEAF_GRAD, stroke="#122810", strokeWidth=4)
d.path("M266,688 C380,660 620,664 766,690", "Leaf midrib", fill=NONE,
       stroke="#7EA85E", strokeWidth=3.5, opacity=55, cap="round")
for i, (a, b, c, e) in enumerate([(360, 668, 340, 690), (460, 660, 450, 692),
                                  (560, 662, 570, 694), (660, 670, 690, 698)]):
    d.path(f"M{a},{b} L{c},{e}", f"Leaf vein {i+1}", fill=NONE,
           stroke="#5E8E4E", strokeWidth=2, opacity=40, cap="round")
d.path("M290,672 C400,646 600,650 740,676", "Leaf sheen", fill=NONE,
       stroke="#C2E8A8", strokeWidth=9, opacity=16, cap="round")
# rain beads standing on the leaf
for i, (x, y, w) in enumerate([(330, 678, 12), (640, 686, 15), (720, 694, 10)]):
    d.shape("ellipse", f"Bead {i+1}", x=x - w / 2, y=y - w * 0.35, width=w, height=w * 0.7,
            fill=rad((0, "#E4F4EE"), (1, "#7EA89E")), stroke="#1E342A", strokeWidth=1.5)
    d.shape("ellipse", f"Bead glint {i+1}", x=x - w * 0.2, y=y - w * 0.28,
            width=w * 0.28, height=w * 0.2, fill="#FFFFFF", opacity=85, stroke=NONE)
# frog's soft contact shadow on the leaf
d.shape("ellipse", "Contact shadow", x=340, y=666, width=320, height=30,
        fill="#0A1408", opacity=35, stroke=NONE)

# === the frog ====================================================================
# hind thighs folded at the flanks: green domes with the blue bars on the outer face
for sgn, lab in ((-1, "L"), (1, "R")):
    cx = 500 + sgn * 168
    d.path(f"M{cx - sgn * 66},560 C{cx - sgn * 78},600 {cx - sgn * 70},640 {cx - sgn * 44},662 "
           f"C{cx - sgn * 10},676 {cx + sgn * 30},668 {cx + sgn * 46},640 "
           f"C{cx + sgn * 58},606 {cx + sgn * 52},570 {cx + sgn * 30},548 "
           f"C{cx + sgn * 2},534 {cx - sgn * 50},536 {cx - sgn * 66},560 Z",
           f"Thigh {lab}", fill=FROG_GRAD, stroke=INK, strokeWidth=4.5)
    # blue flank patch + cream bars on the outer thigh face
    bx0 = cx + sgn * 6
    d.path(f"M{bx0},568 C{bx0 + sgn * 34},576 {bx0 + sgn * 44},606 {bx0 + sgn * 36},636 "
           f"C{bx0 + sgn * 20},652 {bx0 - sgn * 6},650 {bx0 - sgn * 16},636 "
           f"C{bx0 - sgn * 24},612 {bx0 - sgn * 16},584 {bx0},568 Z",
           f"Flank {lab}", fill=FLANK_GRAD, opacity=90, stroke=NONE)
    for k in range(3):
        bx = bx0 - sgn * 8 + sgn * k * 16
        d.path(f"M{bx},582 C{bx + sgn * 4},604 {bx + sgn * 4},624 {bx},640",
               f"Flank bar {lab}{k+1}", fill=NONE, stroke="#E8E4B8",
               strokeWidth=5, opacity=70, cap="round")

# body dome: broad head merging into the squat trunk
BODY = ("M352,586 C344,540 352,486 384,446 C400,424 424,410 452,404 "
        "C486,396 522,396 552,406 C582,414 606,432 622,458 "
        "C648,498 656,544 648,588 C642,626 606,652 556,660 "
        "C502,668 442,664 400,646 C370,632 356,612 352,586 Z")
d.path(BODY, "Body", fill=FROG_GRAD, stroke=INK, strokeWidth=6)
# belly patch: paler green washing up from the seat
d.path("M404,560 C420,620 460,648 510,648 C560,648 600,622 612,570 "
       "C616,610 596,640 556,652 C500,664 440,656 410,626 "
       "C400,608 398,584 404,560 Z", "Belly", fill=BELLY_GRAD, opacity=80, stroke=NONE)
# dorsal sheen between the eyes down the back
d.path("M436,432 C470,414 530,412 566,430", "Back sheen", fill=NONE,
       stroke="#D8F4C8", strokeWidth=13, opacity=28, cap="round")
d.path("M446,428 C476,416 524,416 556,428", "Back sheen core", fill=NONE,
       stroke="#EEFAE4", strokeWidth=5, opacity=38, cap="round")

# forelegs: slim columns planted on the leaf, toes splayed with orange pads
for sgn, lab in ((-1, "L"), (1, "R")):
    sx = 500 + sgn * 62
    d.path(f"M{sx - sgn * 14},540 C{sx - sgn * 20},590 {sx - sgn * 18},640 {sx - sgn * 10},676 "
           f"C{sx - sgn * 4},684 {sx + sgn * 10},684 {sx + sgn * 14},676 "
           f"C{sx + sgn * 18},640 {sx + sgn * 16},592 {sx + sgn * 14},544 Z",
           f"Foreleg {lab}", fill=FROG_GRAD, stroke=INK, strokeWidth=4)
    d.path(f"M{sx - sgn * 6},560 C{sx - sgn * 10},606 {sx - sgn * 8},646 {sx - sgn * 2},672",
           f"Foreleg sheen {lab}", fill=NONE, stroke="#D8F4C8", strokeWidth=3.5,
           opacity=35, cap="round")
    # toes fanned: left, middle, right under the wrist
    wx = sx
    for k, (dx, dy) in enumerate([(-30, 18), (-4, 30), (24, 22)]):
        tx, ty = wx + dx, 676 + dy
        d.path(f"M{wx},{676} C{wx + dx * 0.4},{688} {tx - dx * 0.15},{ty - 8} {tx},{ty}",
               f"Toe {lab}{k+1}", fill=NONE, stroke="#3E9E46", strokeWidth=6, cap="round")
        d.shape("ellipse", f"Toe pad {lab}{k+1}", x=tx - 8, y=ty - 7, width=16, height=13,
                fill=rad((0, "#F8A03E"), (1, "#D8641C")), stroke=INK, strokeWidth=2.5)

# hind foot peeking forward beside each foreleg, pads down on the leaf
for sgn, lab in ((-1, "L"), (1, "R")):
    fx = 500 + sgn * 132
    d.path(f"M{fx + sgn * 10},664 C{fx - sgn * 14},668 {fx - sgn * 34},674 {fx - sgn * 44},682",
           f"Hind toe {lab}", fill=NONE, stroke="#3E9E46", strokeWidth=7, cap="round")
    d.shape("ellipse", f"Hind pad {lab}", x=fx - sgn * 52 - 8, y=676, width=16, height=13,
            fill=rad((0, "#F8A03E"), (1, "#D8641C")), stroke=INK, strokeWidth=2.5)

# === face: the two traffic-light eyes =============================================
for sgn, lab in ((-1, "L"), (1, "R")):
    ex = 500 + sgn * 88
    # socket bulge rising off the dome
    d.shape("ellipse", f"Socket {lab}", x=ex - 52, y=352, width=104, height=98,
            fill=rad((0, "#6EC45E"), (1, "#2E8A3E")), stroke=INK, strokeWidth=4.5)
    # the red iris filling the socket
    d.shape("ellipse", f"Iris {lab}", x=ex - 40, y=362, width=80, height=78,
            fill=EYE_GRAD, stroke="#6E0A04", strokeWidth=3)
    # vertical slit pupil
    d.shape("ellipse", f"Pupil {lab}", x=ex - 7, y=372, width=14, height=58,
            fill="#120608", stroke=NONE)
    # wet glints
    d.shape("ellipse", f"Eye glint {lab}", x=ex - 24, y=372, width=14, height=12,
            fill="#FFFFFF", opacity=90, stroke=NONE)
    d.shape("ellipse", f"Eye glint2 {lab}", x=ex + 10, y=424, width=7, height=6,
            fill="#F8C8B8", opacity=55, stroke=NONE)

# mouth: the long quiet smile across the snout
d.path("M392,520 C440,548 560,548 608,520", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=5, opacity=75, cap="round")
d.path("M398,514 C444,540 556,540 602,514", "Mouth light", fill=NONE,
       stroke="#B8E8A0", strokeWidth=3, opacity=40, cap="round")
# nostrils high on the snout
d.shape("ellipse", "Nostril L", x=474, y=470, width=9, height=7, fill="#1E5A2E", stroke=NONE)
d.shape("ellipse", "Nostril R", x=519, y=470, width=9, height=7, fill="#1E5A2E", stroke=NONE)
# tympanum hints tucked behind the jaw
d.shape("ellipse", "Tympanum L", x=352, y=520, width=22, height=22,
        fill="#3E9E46", opacity=45, stroke="#1E5A2E", strokeWidth=2)
d.shape("ellipse", "Tympanum R", x=626, y=520, width=22, height=22,
        fill="#3E9E46", opacity=45, stroke="#1E5A2E", strokeWidth=2)

# rain bead on the frog's back
d.shape("ellipse", "Back bead", x=540, y=452, width=16, height=11,
        fill=rad((0, "#E4F4EE"), (1, "#7EA89E")), stroke="#1E5A2E", strokeWidth=1.5)
d.shape("ellipse", "Back bead glint", x=545, y=454, width=5, height=4,
        fill="#FFFFFF", opacity=85, stroke=NONE)

# foreground rain drops over the whole plate
for i, (x, y, w) in enumerate([(250, 420, 5), (780, 440, 6), (210, 560, 5),
                               (820, 590, 5), (350, 250, 5), (700, 200, 4)]):
    assert on_disc(x, y, 10), (x, y)
    d.shape("ellipse", f"Rain drop {i+1}", x=x - w / 2, y=y - w / 2, width=w, height=w * 1.4,
            fill="#D8EAE2", opacity=40, stroke=NONE)

# plate rim on top so everything inside closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840, fill=NONE,
        stroke="#0A1810", strokeWidth=6)
d.shape("ellipse", "Plate inner ring 2", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C8E0BC", strokeWidth=3, opacity=25)

# --- name -------------------------------------------------------------------------
r1 = d.text("RED-EYED TREE FROG", "Name", x=500, y=962, size=52, font="Virelai Sans",
            color="#D8ECDC", justify="center")

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

d.finish("red-eyed-tree-frog-V1R00")
