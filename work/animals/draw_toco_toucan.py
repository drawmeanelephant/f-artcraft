#!/usr/bin/env python3
"""Toco toucan — field plate V1R00. Profile facing right, perched upright on a
mossy bough: the absurd orange bill reaches toward a hanging fruit sprig, the
white throat bib over the black body, blue orbital skin around a dark patient
eye, the long tail squared off below the perch. Canopy plate — layered leaf
shade overhead, one shaft of light, fruit dangling. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Toco Toucan — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#160F0A"   # warm near-black

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def linO(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c, "opacity": a} for o, c, a in stops]}}

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

BG_GRAD    = lin(0, 0, 0, 1000, (0, "#0E1A10"), (1, "#030704"))
PLATE_GRAD = rad((0, "#567C4A"), (0.55, "#2E4E2E"), (1, "#11220F"))
BODY_GRAD  = rad((0, "#3A3230"), (0.55, "#1E1815"), (1, "#0C0806"))
BIB_GRAD   = rad((0, "#FDF8EC"), (0.65, "#EDE2C8"), (1, "#C9B894"))
BILL_GRAD  = lin(470, 280, 780, 400, (0, "#F8C23C"), (0.55, "#F08E1E"), (1, "#D4640E"))
BOUGH_GRAD = lin(0, 620, 0, 700, (0, "#4A3620"), (1, "#241A0E"))
LEAF_GRAD  = lin(0, 80, 0, 340, (0, "#4E7A44"), (1, "#1E3A20"))

# --- backdrop + canopy plate ------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880, fill="#4E7A44", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840, fill=PLATE_GRAD, stroke=NONE)

# canopy light shafting down through the leaves
d.shape("ellipse", "Canopy light", x=280, y=100, width=440, height=300,
        fill=radO((0, "#D8ECB8", 20), (0.6, "#D8ECB8", 8), (1, "#D8ECB8", 0)), stroke=NONE)

# layered canopy leaves crowding the upper rim
for i, (cx, cy, a, L, w_) in enumerate([(180, 250, -35, 150, 26), (270, 180, -60, 100, 24),
                                        (150, 380, -15, 120, 22), (830, 230, 215, 150, 26),
                                        (760, 150, 210, 90, 22), (860, 370, 190, 110, 22),
                                        (330, 130, -40, 90, 20), (680, 110, 200, 80, 20)]):
    r_ = math.radians(a)
    ux, uy = math.cos(r_), math.sin(r_)
    nx, ny = -uy, ux
    tip = (cx + ux * L, cy + uy * L)
    m = (cx + ux * L / 2, cy + uy * L / 2)
    assert on_disc(*tip, 8) and on_disc(cx, cy, 8), i
    d.path(f"M{cx},{cy} Q{m[0] + nx * w_:.1f},{m[1] + ny * w_:.1f} {tip[0]:.1f},{tip[1]:.1f} "
           f"Q{m[0] - nx * w_:.1f},{m[1] - ny * w_:.1f} {cx},{cy} Z", f"Canopy leaf {i+1}",
           fill=lin(cx, cy, tip[0], tip[1], (0, "#3E6A38"), (1, "#1C3420")),
           opacity=55, stroke=NONE)
    d.path(f"M{cx},{cy} L{tip[0]:.1f},{tip[1]:.1f}", f"Leaf rib {i+1}", fill=NONE,
           stroke="#7AA464", strokeWidth=3, opacity=30, cap="round")

# --- fruit sprig hanging from the upper right, in reach of the bill tip -------------
assert on_disc(716, 110, 2)
d.path("M716,110 C714,140 718,168 716,196", "Fruit stem", fill=NONE,
       stroke="#3E5228", strokeWidth=5, cap="round")
d.path("M716,196 C708,210 702,222 700,236", "Fruit stem low", fill=NONE,
       stroke="#3E5228", strokeWidth=4, cap="round")
# a leaf on the sprig
assert on_disc(766, 140, 2) and on_disc(722, 116, 2)
d.path("M722,116 C744,112 762,122 766,140 C746,144 730,134 722,116 Z",
       "Sprig leaf", fill="#3E6A38", opacity=85, stroke=NONE)
# the fruit cluster: three orange berries dangling
for i, (x, y, r_) in enumerate([(704, 218, 26), (736, 200, 22), (690, 250, 20)]):
    d.shape("ellipse", f"Fruit {i+1}", x=x - r_, y=y - r_, width=r_ * 2, height=r_ * 2,
            fill=rad((0, "#F8A03E"), (0.7, "#E0681E"), (1, "#A83A10")), stroke=NONE)
    d.shape("ellipse", f"Fruit {i+1} light", x=x - r_ * 0.5, y=y - r_ * 0.55,
            width=r_ * 0.7, height=r_ * 0.45, fill="#FCD89A", opacity=45, stroke=NONE)
# calyx tips
for i, (x, y) in enumerate([(704, 194), (736, 180)]):
    d.path(f"M{x - 6},{y} L{x},{y - 8} L{x + 6},{y}", f"Calyx {i+1}",
           fill=NONE, stroke="#2E4420", strokeWidth=3, cap="round")

# --- understory dark massing at the floor, closing on the arc ---------------------------
uy_ = 762
ul, ur = disc_x(uy_, -1), disc_x(uy_, 1)
d.path(f"M{ul:.1f},{uy_} C300,744 420,760 520,750 C620,742 700,754 {ur:.1f},{uy_} "
       f"A{PR},{PR} 0 0 1 {ul:.1f},{uy_} Z", "Understory", fill="#0E1C0C", opacity=80, stroke=NONE)
# pale leaf silhouettes catching light at the floor's edge
for i, (x, y, w) in enumerate([(250, 730, 60), (680, 716, 74), (380, 744, 56)]):
    d.path(f"M{x},{y} Q{x + w / 2},{y - 20} {x + w},{y - 4} Q{x + w / 2},{y + 8} {x},{y} Z",
           f"Floor leaf {i+1}", fill="#567C4A", opacity=25, stroke=NONE)

# --- the bough: mossy, angled, the perch -----------------------------------------------------
d.path("M216,690 C340,662 560,648 754,640 C780,644 784,662 764,672 "
       "C580,690 360,706 226,720 C204,716 200,700 216,690 Z",
       "Bough", fill=BOUGH_GRAD, stroke=NONE)
# moss + lichen on the bough's top edge
for i, (x, y, w) in enumerate([(300, 668, 26), (420, 656, 32), (560, 648, 24), (680, 642, 20)]):
    d.shape("ellipse", f"Moss {i+1}", x=x, y=y, width=w, height=10,
            fill="#7A9A50", opacity=45, stroke=NONE)
d.path("M230,694 C350,668 560,652 748,644", "Bough light", fill=NONE,
       stroke="#6E5638", strokeWidth=4, opacity=50, cap="round")

# --- tail: the long squared plume hanging below the perch ------------------------------------
d.path(smooth([(340, 560), (300, 620), (286, 690), (292, 742), (336, 748),
               (352, 700), (368, 620), (380, 560)]),
       "Tail", fill=BODY_GRAD, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Tail sheen", x=300, y=620, width=26, height=90,
        fill="#6E645C", opacity=20, stroke=NONE)
# the red vent patch at the tail's root
d.path("M330,548 C346,540 366,542 376,554 C366,566 344,566 330,548 Z",
       "Vent", fill="#C83A28", opacity=90, stroke=NONE)

# --- body: upright black mass, breast forward -----------------------------------------------
d.path(smooth([(388, 560), (348, 540), (316, 490), (312, 430), (336, 372),
               (382, 330), (438, 316), (478, 330), (500, 380), (506, 440),
               (498, 500), (470, 550), (430, 574)]),
       "Body", fill=BODY_GRAD, stroke=INK, strokeWidth=5)
# sheen along the back + soft shadow under the wing mass
d.path("M330,410 C324,470 340,520 376,552", "Back sheen", fill=NONE,
       stroke="#5A504A", strokeWidth=9, opacity=35, cap="round")
# folded wing: a long black-on-black teardrop with feather seams
d.path("M356,420 C390,406 440,410 464,440 C478,478 470,530 446,556 "
       "C416,570 380,560 366,530 C352,496 348,456 356,420 Z",
       "Wing", fill="#14100C", opacity=75, stroke=NONE)
for i, dd in enumerate(["M372,450 C400,442 434,448 452,466",
                        "M376,490 C404,484 436,490 452,506",
                        "M386,528 C410,524 434,528 446,540"]):
    d.path(dd, f"Wing seam {i+1}", fill=NONE, stroke="#3E3630", strokeWidth=3,
           opacity=55, cap="round")

# --- the white bib washing down the throat and breast ----------------------------------------
d.path(smooth([(432, 320), (470, 330), (494, 366), (502, 414), (492, 452),
               (462, 472), (428, 470), (404, 450), (394, 412), (398, 366),
               (410, 336)]),
       "Bib", fill=BIB_GRAD, stroke=NONE)
# a warm shadow where the bib meets the black body
d.path("M398,436 C420,462 460,470 490,448 C478,478 420,482 398,436 Z",
       "Bib shadow", fill="#A8906C", opacity=35, stroke=NONE)
# the bib's lemon tint high on the throat
d.shape("ellipse", "Bib tint", x=440, y=340, width=52, height=44,
        fill="#F8E8B8", opacity=50, stroke=NONE)

# --- head + the bill --------------------------------------------------------------------------
d.path(smooth([(398, 330), (400, 292), (428, 262), (468, 252), (500, 262),
               (512, 292), (506, 326), (480, 344), (440, 346)]),
       "Head", fill=BODY_GRAD, stroke=INK, strokeWidth=5)
# crown sheen
d.shape("ellipse", "Crown sheen", x=418, y=262, width=80, height=34,
        fill="#6E645C", opacity=25, stroke=NONE)

# the bill: a great orange blade sweeping right, slightly down-curved tip
d.path("M486,272 C560,258 660,270 730,302 C758,316 774,338 776,360 "
       "C756,372 730,380 700,380 C620,384 540,372 486,352 "
       "C472,326 472,298 486,272 Z",
       "Bill", fill=BILL_GRAD, stroke=INK, strokeWidth=4)
# the black patch at the tip — toco's telltale
d.path("M724,306 C752,318 770,338 776,358 C762,368 742,376 720,378 "
       "C728,352 730,328 724,306 Z",
       "Bill tip", fill="#181014", stroke=NONE)
# the narrow black seam at the bill's base
d.path("M486,274 C480,300 480,326 488,350", "Bill base seam", fill=NONE,
       stroke="#181014", strokeWidth=5, opacity=85, cap="round")
# the culmen ridge light running the bill's length
d.path("M492,286 C560,274 660,286 726,314", "Culmen light", fill=NONE,
       stroke="#FCE8A8", strokeWidth=6, opacity=50, cap="round")
# soft shade under the bill's lower edge
d.path("M500,346 C570,366 650,374 716,370", "Bill under shade", fill=NONE,
       stroke="#8E3A0C", strokeWidth=5, opacity=45, cap="round")

# --- the eye: blue orbital skin, dark patient eye inside ---------------------------------------
d.shape("ellipse", "Orbital skin", x=424, y=282, width=56, height=56,
        fill=rad((0, "#7ADCF0"), (0.7, "#38B4D8"), (1, "#1E7EA4")), stroke=NONE)
d.shape("ellipse", "Eye", x=442, y=300, width=22, height=22, fill="#140C08", stroke=NONE)
d.shape("ellipse", "Eye glint", x=447, y=304, width=6, height=6, fill="#E8F8FC", opacity=85, stroke=NONE)

# --- feet gripping the bough ------------------------------------------------------------------
d.path("M392,560 C386,600 396,640 410,664", "Leg", fill=NONE,
       stroke="#1E1815", strokeWidth=16, cap="round")
for i, (x0, x1) in enumerate([(398, 372), (412, 442)]):
    d.path(f"M{x0},664 C{x0 - 8},684 {x0 - 14},696 {x1 - 16},700 "
           f"C{x1 - 2},702 {x1 + 6},696 {x1 + 4},682",
           f"Toe {i+1}", fill=NONE, stroke="#6E7A80", strokeWidth=7, cap="round")
# a third toe hooking back behind the bough
d.path("M430,668 C446,676 456,690 452,706", "Rear toe", fill=NONE,
       stroke="#5A666C", strokeWidth=6, cap="round")

# plate rim on top so everything inside closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840, fill=NONE,
        stroke="#0A1408", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C8E0BC", strokeWidth=3, opacity=28)

# --- name + second line -------------------------------------------------------------------------
d.text("TOCO TOUCAN", "Name", x=500, y=940, size=58, font="Virelai Sans",
       color="#E4F0D8", justify="center")
LINE2, SZ2, TRK = "RAMPHASTOS TOCO", 22, 280
r = d.text(LINE2, "Second line", x=500, y=975, size=SZ2, font="Virelai Sans",
           color="#AAC8A0", justify="center")
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

d.finish("toco-toucan-V1R00")
