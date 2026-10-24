#!/usr/bin/env python3
"""Giant Pacific octopus — field-guide plate V1R00. Mantle up, eight muscular
arms sprawled over the tide-reef, two raised in the kelp shadow, bar-pupil
eyes watching, a faint ink wisp — one escape plan. Kelp-canopy plate.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Giant Pacific Octopus — Field Plate", 1000, 1000)

INK = "#33190F"                    # warm dark ink, never pure black
CX, CY, R = 500, 460, 420          # plate disc centre + radius

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

BG_GRAD = lin(0, 0, 0, 1000, (0, "#0A130C"), (1, "#030704"))
PLATE_GRAD = lin(0, 40, 0, 880, (0, "#3E5C46"), (0.5, "#1E3A2C"), (1, "#0A1C14"))
MANTLE_GRAD = rad((0, "#C96A44"), (0.6, "#9E4630"), (1, "#5E2416"))
ARM_GRAD = rad((0, "#B85C3C"), (0.6, "#8E3E28"), (1, "#571F12"))
REEF_GRAD = lin(0, 700, 0, 880, (0, "#2A3826"), (1, "#0C120A"))

def rim_x(y, r=R, side=-1):
    return CX + side * math.sqrt(r * r - (y - CY) ** 2)

def quad(p0, p1, p2, t):
    u = 1 - t
    return (u*u*p0[0] + 2*u*t*p1[0] + t*t*p2[0],
            u*u*p0[1] + 2*u*t*p1[1] + t*t*p2[1],
            2*u*(p1[0]-p0[0]) + 2*t*(p2[0]-p1[0]),
            2*u*(p1[1]-p0[1]) + 2*t*(p2[1]-p1[1]))

def ribbon_pts(pts, w0, w1, label, **kw):
    n = len(pts) - 1
    L, Rr = [], []
    for k, (x, y) in enumerate(pts):
        if k == 0: dx, dy = pts[1][0]-x, pts[1][1]-y
        elif k == n: dx, dy = x-pts[k-1][0], y-pts[k-1][1]
        else: dx, dy = pts[k+1][0]-pts[k-1][0], pts[k+1][1]-pts[k-1][1]
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy/ln, dx/ln
        w = (w0 + (w1 - w0) * k / n) / 2
        L.append((x + nx*w, y + ny*w)); Rr.append((x - nx*w, y - ny*w))
    dd = "M%.1f,%.1f " % L[0] + " ".join("L%.1f,%.1f" % p for p in L[1:])
    dd += " " + " ".join("L%.1f,%.1f" % p for p in reversed(Rr)) + " Z"
    d.path(dd, label, **kw)

def frond(root, ctrl, tip, w0, w1, label, **kw):
    pts = [quad(root, ctrl, tip, k/16)[:2] for k in range(17)]
    ribbon_pts(pts, w0, w1, label, **kw)

# --- backdrop + kelp-shadow plate -------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#0A1F14", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#9CBFA4", strokeWidth=3, opacity=35)

# dim canopy light
d.shape("ellipse", "Canopy glow", x=240, y=90, width=400, height=240,
        fill=radO((0, "#8FB894", 34), (0.5, "#6A9A72", 12), (0.75, "#6A9A72", 0),
                  (1, "#6A9A72", 0)), stroke=NONE)
for i, (x0, x1, w_) in enumerate([(280, 400, 46), (480, 560, 34)]):
    d.path(f"M{x0},140 L{x0 + w_},140 L{x1 + w_},620 L{x1},620 Z", f"Light shaft {i+1}",
           fill=linO(x0 + w_/2, 140, x1 + w_/2, 620, (0, "#A4CCAA", 0),
                     (0.2, "#A4CCAA", 13), (0.65, "#8CBA94", 6),
                     (1, "#8CBA94", 0)), stroke=NONE)

# kelp canopy: dark straps hanging down from the surface
KELP = "#0E2115"
frond((420, 66), (408, 180), (432, 292), 26, 13, "Kelp L2", fill=KELP, opacity=88, stroke=NONE)
frond((505, 60), (508, 165), (488, 268), 30, 15, "Kelp C", fill="#12291A", opacity=92, stroke=NONE)
frond((582, 68), (592, 190), (572, 320), 24, 12, "Kelp R1", fill=KELP, opacity=88, stroke=NONE)
frond((660, 88), (642, 200), (664, 298), 18, 10, "Kelp R2", fill="#0A1B11", opacity=85, stroke=NONE)
frond((352, 90), (346, 190), (362, 278), 16, 9, "Kelp L1", fill="#0A1B11", opacity=85, stroke=NONE)
# frond edge lights (what little light gets through)
for dd in ["M424,80 C414,170 420,230 428,284", "M580,80 C590,180 580,250 574,312"]:
    d.path(dd, "Kelp edge", fill=NONE, stroke="#3E6A48",
           strokeWidth=3, opacity=40, cap="round")

# drifting motes in the dim water
for i, (x, y, w, o) in enumerate([(250,300,5,40),(350,200,4,45),(640,180,5,38),(700,280,4,35),
                                  (190,460,4,30),(760,440,5,32),(300,560,4,28),(700,600,5,30),
                                  (160,340,4,28),(830,320,4,28),(560,120,4,36),(420,640,4,26)]):
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#D8ECDC", opacity=o, stroke=NONE)

# --- tide-reef floor, closing on the disc's arc -----------------------------------
ry = 736
rl, rr = rim_x(ry, side=-1), rim_x(ry, side=1)
d.path(f"M{rl:.1f},{ry} C260,724 300,742 360,732 C410,724 440,744 500,736 "
       f"C560,728 620,746 680,736 C720,730 760,740 {rr:.1f},{ry} "
       f"A{R},{R} 0 0 1 {rl:.1f},{ry} Z", "Reef", fill=REEF_GRAD, stroke=NONE)
# stones on the reef lip
for i, (x, y, w, h) in enumerate([(230, 726, 56, 26), (330, 720, 40, 20),
                                  (640, 722, 48, 22), (740, 726, 40, 18)]):
    d.shape("ellipse", f"Stone {i+1}", x=x, y=y, width=w, height=h,
            fill="#1C2A1A", opacity=85, stroke=NONE)
    d.shape("ellipse", f"Stone light {i+1}", x=x + 6, y=y + 2, width=w - 22, height=h - 14,
            fill="#5E7A58", opacity=30, stroke=NONE)

# a faint ink wisp curling away — the escape plan
for i, (x, y, w, h, o) in enumerate([(690, 408, 60, 40, 30), (724, 384, 44, 30, 24),
                                     (752, 358, 30, 22, 18)]):
    d.shape("ellipse", f"Ink wisp {i+1}", x=x, y=y, width=w, height=h,
            fill="#0A1410", opacity=o, stroke=NONE)

# --- eight arms: tapered ribbons, sucker rows, curling tips -------------------------
def arm_pts(root, ctrl, tip, curl=0, n=16):
    pts = [quad(root, ctrl, tip, k/n)[:2] for k in range(n + 1)]
    if curl:
        x, y, dx, dy = quad(root, ctrl, tip, 1)
        a = math.atan2(dy, dx)
        for k in range(1, 11):
            t = k / 10
            a += curl * math.radians(15)
            step = (1 - t) * 15 + 6
            x += math.cos(a) * step
            y += math.sin(a) * step
            pts.append((x, y))
    return pts

def arm(i, root, ctrl, tip, w0, w1, curl=0, suckers=True):
    pts = arm_pts(root, ctrl, tip, curl)
    ribbon_pts(pts, w0, w1, f"Arm {i}", fill=ARM_GRAD,
               stroke=INK, strokeWidth=3)
    if not suckers:
        return pts
    # double row of cream suckers along the arm's underside
    for j, k in enumerate(range(3, len(pts) - 2, 2)):
        x, y = pts[k]
        dx = pts[k + 1][0] - pts[k - 1][0]
        dy = pts[k + 1][1] - pts[k - 1][1]
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy / ln, dx / ln
        off = (w0 + (w1 - w0) * k / (len(pts) - 1)) * 0.30
        side = 1 if j % 2 == 0 else -1
        sx, sy = x + nx * off * side, y + ny * off * side
        s = max(3.5, w0 * 0.22 * (1 - k / len(pts) * 0.6))
        d.shape("ellipse", f"Arm {i} sucker {j+1}", x=round(sx - s/2), y=round(sy - s/2),
                width=round(s), height=round(s), fill="#F2DFC4",
                opacity=60, stroke=NONE)
    return pts

# back pair reaching wide along the waterline of the body
arm(1, (452, 488), (352, 514), (254, 554), 34, 8, curl=+1)
arm(2, (548, 488), (648, 514), (746, 554), 34, 8, curl=-1)
# mid pair sloping down onto the reef
arm(3, (462, 502), (394, 594), (306, 658), 30, 7, curl=+1)
arm(4, (538, 502), (608, 594), (694, 658), 30, 7, curl=-1)
# raised pair curling beside the mantle
arm(5, (456, 470), (394, 444), (354, 344), 26, 6, curl=-1)
arm(6, (544, 470), (606, 444), (646, 344), 26, 6, curl=+1)

# --- mantle ----------------------------------------------------------------------
MANTLE = ("M500,238 C578,238 638,298 643,366 C646,412 630,448 600,470 "
          "C572,488 428,488 400,470 C370,448 354,412 357,366 "
          "C362,298 422,238 500,238 Z")
d.path(MANTLE, "Mantle", fill=MANTLE_GRAD, stroke=INK, strokeWidth=7)
# warty crown bumps along the top edge
for i, (x, y, r_) in enumerate([(458, 250, 11), (496, 244, 12), (534, 252, 10),
                                (366, 360, 9), (634, 360, 9)]):
    d.shape("ellipse", f"Papilla {i+1}", x=x - r_, y=y - r_, width=r_*2, height=r_*2,
            fill="#9E4630", stroke=INK, strokeWidth=2)
# mantle shading + sheen
d.path("M362,340 C370,420 420,470 500,476 C580,470 630,420 638,340 "
       "C632,430 580,478 500,482 C420,478 368,430 362,340 Z",
       "Mantle shade", fill="#571F12", opacity=32, stroke=NONE)
d.shape("ellipse", "Mantle sheen", x=410, y=262, width=140, height=80,
        fill="#F2A884", opacity=30, stroke=NONE)
# mottled camouflage patches
for i, (x, y, w, h, o) in enumerate([(430, 300, 60, 36, 30), (540, 320, 52, 32, 28),
                                     (480, 400, 70, 40, 26), (390, 380, 44, 30, 26)]):
    d.shape("ellipse", f"Mottle {i+1}", x=x, y=y, width=w, height=h,
            fill="#5E2416", opacity=o, stroke=NONE)
# pale skin flecks
for i, (x, y, w) in enumerate([(458, 330, 6), (512, 292, 5), (560, 370, 6), (420, 350, 5),
                               (540, 420, 5), (478, 258, 5), (600, 396, 5)]):
    d.shape("ellipse", f"Skin fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#F2C49C", opacity=45, stroke=NONE)

# --- eyes: watchful, bar pupils ----------------------------------------------------
for side, ex in (("L", 432), ("R", 560)):
    d.shape("ellipse", f"Eye mound {side}", x=ex - 8, y=402, width=48, height=52,
            fill="#8E3E28", opacity=60, stroke=NONE)
    d.shape("ellipse", f"Eye {side}", x=ex, y=410, width=32, height=36,
            fill="#3A1408", stroke=INK, strokeWidth=3)
    d.shape("rectangle", f"Pupil {side}", x=ex + 4, y=424, width=24, height=7,
            fill="#0C0604", stroke=NONE)
    d.shape("ellipse", f"Eye glint {side}", x=ex + 8, y=414, width=6, height=6,
            fill="#FFECD8", opacity=80, stroke=NONE)
    d.path(f"M{ex - 10},{408} C{ex + 6},{394} {ex + 30},{394} {ex + 42},{406}",
           f"Eyebrow fold {side}", fill=NONE, stroke="#5E2416",
           strokeWidth=6, opacity=60, cap="round")

# front pair over the reef, tips curling outward
arm(7, (484, 512), (448, 612), (428, 696), 30, 7, curl=+1)
arm(8, (516, 512), (560, 608), (588, 692), 30, 7, curl=-1)
# arm webbing shadow at the crown
d.shape("ellipse", "Arm crown shade", x=430, y=478, width=140, height=44,
        fill="#3A1408", opacity=35, stroke=NONE)

# --- name ----------------------------------------------------------------------------
d.text("GIANT PACIFIC OCTOPUS", "Name", x=500, y=962, size=44, font="Virelai Sans",
       color="#D4E4CC", justify="center")

d.finish("giant-pacific-octopus-V1R00")
