#!/usr/bin/env python3
"""Andean condor — field plate V1R00. Dorsal soar: the ten-foot plank of wing
spread flat across the disc, slotted primaries at the tips, the white covert
panels riding each upper wing, the pale ruff collaring the neck, the small
bare head ahead. Cordillera plate, updraft mood — dawn amber climbing the
peaks, a far pale ridge behind the dark one. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Andean Condor — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#1A1410"   # warm dark ink, never pure black

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
    return math.hypot(x - PCX, y - PCY) <= PR - pad

def rim_x(y, side):
    return PCX + side * math.sqrt(PR * PR - (y - PCY) ** 2)

BG_GRAD    = lin(0, 0, 0, 1000, (0, "#12101A"), (1, "#050408"))
PLATE_GRAD = rad((0, "#8E8EA8"), (0.55, "#545670"), (1, "#20222F"))
NEAR_GRAD  = lin(0, 540, 0, 880, (0, "#4E4458"), (0.5, "#322C3E"), (1, "#181420"))
WING_GRAD  = lin(500, 420, 860, 330, (0, "#3A3440"), (0.55, "#1E1C24"), (1, "#0C0B10"))
BODY_GRAD  = lin(500, 370, 500, 640, (0, "#38323C"), (0.6, "#1C1A22"), (1, "#0C0B10"))
PANEL_GRAD = lin(560, 420, 810, 310, (0, "#F2EADC"), (1, "#C4B9A2"))

# --- backdrop + cordillera plate -------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#8E8EA8", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#14121C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E2DDE8", strokeWidth=3, opacity=35)

# dawn amber climbing the peaks — the updraft's light
d.shape("ellipse", "Dawn glow", x=300, y=480, width=400, height=260,
        fill=rad((0, "#E8B06E", 40), (0.55, "#E8B06E", 14), (1, "#E8B06E", 0)), stroke=NONE)
# thin thermal haze rising into the light
for i, (x, h) in enumerate([(430, 70), (505, 85), (585, 65)]):
    y0 = 700
    d.path(f"M{x},{y0} C{x - 8},{y0 - h / 3:.0f} {x + 8},{y0 - 2 * h / 3:.0f} {x},{y0 - h:.0f}",
           f"Thermal {i+1}", fill=NONE, stroke="#E8C88E", strokeWidth=3,
           opacity=22, cap="round")

# a far pale ridge, ends tapered to points tucked inside the near mass
d.path("M205,690 C245,606 300,578 365,562 C445,542 510,575 575,555 "
       "C650,537 715,570 785,735 L205,740 Z",
       "Far ridge", fill="#6A6478", opacity=50, stroke=NONE)

# two distant soaring condors riding the same wind, high in the plate
for i, (x, y, s) in enumerate([(255, 185, 1), (735, 165, -1)]):
    assert on_disc(x, y, 20), (x, y)
    d.path(f"M{x - 34 * s},{y + 4} C{x - 16 * s},{y - 6} {x + 10 * s},{y - 4} {x + 34 * s},{y + 2}",
           f"Far soar {i+1}", fill=NONE, stroke="#1E1C26", strokeWidth=5,
           opacity=60, cap="round")

# --- the cordillera: a sawtooth range closing on the disc's own arc -----------------
yl, yr = 690, 742
xl, xr = rim_x(yl, -1), rim_x(yr, 1)
d.path(f"M{xl:.1f},{yl} L250,640 L330,586 L390,648 L470,556 L545,636 "
       f"L620,572 L690,662 L760,600 L{xr:.1f},{yr} "
       f"A{PR},{PR} 0 0 1 {xl:.1f},{yl} Z", "Near ridge", fill=NEAR_GRAD, stroke=NONE)
# snow caps on the summits, dawnlit
for i, (px, py) in enumerate([(330, 586), (470, 556), (620, 572), (760, 600), (250, 640)]):
    d.path(f"M{px - 26},{py + 18} L{px},{py - 6} L{px + 26},{py + 18} "
           f"C{px + 14},{py + 26} {px - 14},{py + 26} {px - 26},{py + 18} Z",
           f"Snow cap {i+1}", fill="#E8E4DC", opacity=80, stroke=NONE)
# ridgeline light on the western faces
for i, (x0, y0, x1, y1) in enumerate([(330, 586, 390, 648), (470, 556, 545, 636),
                                      (620, 572, 690, 662)]):
    d.path(f"M{x0},{y0} L{x1},{y1}", f"Face light {i+1}", fill=NONE,
           stroke="#C8B498", strokeWidth=3.5, opacity=35, cap="round")

# === the condor: dorsal soar, wings spread flat =====================================
# wings — broad black planks, slotted primaries at each tip
for sgn, lab in ((1, "R"), (-1, "L")):
    def mx(x): return 500 + sgn * (x - 500)
    d.path(f"M{mx(492)},412 C{mx(585)},372 {mx(700)},330 {mx(828)},300 "
           f"Q{mx(846)},286 {mx(853)},296 Q{mx(818)},305 {mx(812)},318 "
           f"Q{mx(848)},316 {mx(852)},330 Q{mx(815)},330 {mx(806)},344 "
           f"Q{mx(836)},346 {mx(838)},360 Q{mx(802)},356 {mx(790)},370 "
           f"Q{mx(806)},382 {mx(796)},394 "
           f"C{mx(730)},425 {mx(615)},455 {mx(528)},472 "
           f"C{mx(515)},452 {mx(500)},432 {mx(492)},412 Z",
           f"Wing {lab}", fill=WING_GRAD, stroke=INK, strokeWidth=5)
    # the white covert panel riding the upper wing
    d.path(f"M{mx(560)},392 C{mx(630)},358 {mx(720)},326 {mx(792)},306 "
           f"C{mx(752)},334 {mx(680)},370 {mx(612)},400 "
           f"C{mx(585)},406 {mx(568)},402 {mx(560)},392 Z",
           f"Wing panel {lab}", fill=PANEL_GRAD, opacity=92, stroke="#8E8672", strokeWidth=2)
    # faint primary separations at the tip slots
    for i, (a, b, c, e) in enumerate([(812, 320, 784, 348), (806, 346, 776, 372)]):
        d.path(f"M{mx(a)},{b} L{mx(c)},{e}", f"Slot {lab}{i+1}", fill=NONE,
               stroke="#050408", strokeWidth=3, opacity=60, cap="round")
    # sheen along the leading edge
    d.path(f"M{mx(500)},410 C{mx(590)},372 {mx(700)},332 {mx(820)},302",
           f"Leading sheen {lab}", fill=NONE, stroke="#9E96B0",
           strokeWidth=6, opacity=25, cap="round")

# body — the broad keel between the wings, tail a short flared wedge
d.path("M500,364 C528,378 542,414 540,454 C538,500 528,545 514,578 "
       "C510,590 505,598 500,602 C495,598 490,590 486,578 "
       "C472,545 462,500 460,454 C458,414 472,378 500,364 Z",
       "Body", fill=BODY_GRAD, stroke=INK, strokeWidth=5)
d.path("M486,572 L470,634 C486,648 514,648 530,634 L514,572 "
       "C505,582 495,582 486,572 Z",
       "Tail", fill=lin(500, 570, 500, 645, (0, "#1C1A22"), (1, "#0C0B10")),
       stroke=INK, strokeWidth=4.5)
for i in range(2):
    d.path(f"M{492 + i * 16},582 L{482 + i * 32},640", f"Tail edge {i+1}",
           fill=NONE, stroke="#050408", strokeWidth=3, opacity=55, cap="round")
# back sheen down the spine
d.path("M500,400 C508,440 508,500 502,545", "Spine sheen", fill=NONE,
       stroke="#8E8698", strokeWidth=5, opacity=25, cap="round")

# the white ruff — one collar of down ringing the neck, scalloped at its hem
d.path("M438,414 C444,388 470,370 500,370 C530,370 556,388 562,414 "
       "C556,434 532,446 500,446 C468,446 444,434 438,414 Z",
       "Ruff", fill=rad((0, "#F4EEE2"), (0.7, "#E4DAC4"), (1, "#C9C0AA")),
       stroke=INK, strokeWidth=3.5)
for i, (x0, x1) in enumerate([(452, 458), (478, 482), (504, 504), (528, 524), (548, 542)]):
    d.path(f"M{x0},428 Q{(x0 + x1) / 2},442 {x1},434", f"Ruff scallop {i+1}",
           fill=NONE, stroke="#A89E88", strokeWidth=2.5, opacity=65, cap="round")

# the small bare head ahead of the ruff — wrinkled rose, a low comb
d.path("M500,352 C512,352 522,360 524,372 C526,384 518,394 506,397 "
       "C494,400 484,394 480,384 C476,372 480,360 490,355 Z",
       "Head", fill=rad((0, "#C07A5E"), (1, "#7E4434")), stroke=INK, strokeWidth=3)
d.path("M492,352 C498,344 510,344 516,352 C510,348 498,348 492,352 Z",
       "Comb", fill="#A85E44", stroke=INK, strokeWidth=2)
# head wrinkles + the pale ear fold
for i, (x0, y0, x1, y1) in enumerate([(486, 366, 500, 364), (486, 376, 500, 376),
                                      (488, 386, 498, 388)]):
    d.path(f"M{x0},{y0} C{(x0 + x1) / 2:.0f},{y0 - 3} {(x0 + x1) / 2:.0f},{y1 + 3} {x1},{y1}",
           f"Wrinkle {i+1}", fill=NONE, stroke="#6E3826", strokeWidth=2,
           opacity=70, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#14121C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring 2", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E2DDE8", strokeWidth=3, opacity=28)

# --- name -------------------------------------------------------------------------
r1 = d.text("ANDEAN CONDOR", "Name", x=500, y=962, size=58, font="Virelai Sans",
            color="#E2DDE8", justify="center")

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

d.finish("andean-condor-V1R00")
