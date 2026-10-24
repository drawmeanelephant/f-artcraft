#!/usr/bin/env python3
"""Lined seahorse — field-guide plate V1R00. A horse's head on a question
mark: profile facing left, spiny coronet, ringed belly, tail curled forward
around a sea-grass blade. Sea-grass plate, drift mood — blades close on the
disc's own arc. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os, math, re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Lined Seahorse — Field Plate", 1000, 1000)

INK = "#2A2014"                    # warm dark ink, never pure black
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
    """radial gradient with per-stop opacity — edges can fade to nothing"""
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c, "opacity": a} for o, c, a in stops]}}

BG_GRAD = lin(0, 0, 0, 1000, (0, "#07130D"), (1, "#020704"))
PLATE_GRAD = lin(0, 40, 0, 880, (0, "#4E7A5C"), (0.5, "#24493A"), (1, "#0B2018"))
BODY_GRAD = rad((0, "#C8AE62"), (0.55, "#9C8442"), (1, "#5E4C26"))
GRASS_GRAD = lin(0, 700, 0, 880, (0, "#1C4230"), (1, "#071A10"))

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

def blade(root, ctrl, tip, w0, w1, label, **kw):
    pts = [quad(root, ctrl, tip, k/16)[:2] for k in range(17)]
    ribbon_pts(pts, w0, w1, label, **kw)

# --- backdrop + sea-grass plate --------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#0A2418", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#A8CCB4", strokeWidth=3, opacity=35)

# soft drift light fading at the edges
d.shape("ellipse", "Water glow", x=210, y=100, width=380, height=240,
        fill=radO((0, "#9CD0B0", 38), (0.45, "#7AB894", 14), (0.7, "#7AB894", 0),
                  (1, "#7AB894", 0)), stroke=NONE)
for i, (x0, x1, w_) in enumerate([(300, 420, 60), (430, 520, 40), (210, 290, 30)]):
    d.path(f"M{x0},130 L{x0 + w_},130 L{x1 + w_},640 L{x1},640 Z", f"Drift shaft {i+1}",
           fill=linO(x0 + w_/2, 130, x1 + w_/2, 640, (0, "#B4DCC4", 0),
                     (0.2, "#B4DCC4", 15), (0.65, "#9CC8AC", 7),
                     (1, "#9CC8AC", 0)), stroke=NONE)
# drifting motes
for i, (x, y, w, o) in enumerate([(240,250,5,45),(330,180,4,50),(560,170,5,40),(660,240,4,40),
                                  (740,330,5,35),(190,420,4,35),(690,470,4,30),(270,540,5,30),
                                  (760,560,4,30),(160,320,4,30),(620,120,4,35),(840,430,4,30)]):
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#DCF0DC", opacity=o, stroke=NONE)
# a few slow bubbles
for i, (x, y, w) in enumerate([(700,300,12),(722,240,8),(712,370,10),(180,260,9)]):
    d.shape("ellipse", f"Bubble {i+1}", x=x, y=y, width=w, height=w,
            fill="#FFFFFF", opacity=14, stroke="#CFEBD4", strokeWidth=2)

# --- sea grass: band closes on the disc's arc, blades rising ---------------------
gy = 748
gl, gr = rim_x(gy, side=-1), rim_x(gy, side=1)
d.path(f"M{gl:.1f},{gy} C300,734 400,758 500,748 C610,738 700,756 {gr:.1f},{gy} "
       f"A{R},{R} 0 0 1 {gl:.1f},{gy} Z", "Grass bed", fill=GRASS_GRAD, stroke=NONE)

GRASS = "#1E4A32"
blade((250, 760), (222, 550), (200, 396), 19, 5, "Blade L1", fill=GRASS, stroke=NONE)
blade((330, 764), (312, 560), (288, 428), 16, 4, "Blade L2", fill="#2A5A3C", stroke=NONE)
blade((426, 762), (410, 645), (398, 472), 16, 4, "Blade anchor", fill="#24553A", stroke=NONE)
blade((580, 760), (614, 575), (634, 418), 17, 5, "Blade R1", fill=GRASS, stroke=NONE)
blade((690, 758), (726, 585), (756, 440), 14, 4, "Blade R2", fill="#2A5A3C", stroke=NONE)
blade((770, 752), (796, 615), (816, 498), 11, 4, "Blade R3", fill="#183D28", stroke=NONE)
# blade edge lights
for dd in ["M247,748 C226,590 212,490 203,408", "M577,748 C608,595 624,500 632,430",
           "M423,750 C412,652 404,555 400,484"]:
    d.path(dd, "Blade edge", fill=NONE, stroke="#5E9A6C",
           strokeWidth=3, opacity=45, cap="round")

# --- the tail: taper down, then a forward spiral round the anchor blade ---------
tail_pts = [quad((490, 606), (482, 652), (452, 686), k/10)[:2] for k in range(11)]
cx, cy = 410, 660
for k in range(34):
    t = k / 33
    ang = math.radians(40 - 285 * t)
    r = 56 * (1 - t) + 15
    tail_pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
ribbon_pts(tail_pts, 15, 3, "Tail", fill=BODY_GRAD, stroke=INK, strokeWidth=3)
# tail rings
for i, k in enumerate([5, 11, 17, 23, 29]):
    x, y = tail_pts[k]
    d.path(f"M{x - 8},{y - 2} C{x - 2},{y + 4} {x + 4},{y + 4} {x + 9},{y}",
           f"Tail ring {i+1}", fill=NONE, stroke="#4E3E1E",
           strokeWidth=3, opacity=45, cap="round")

# --- the trunk + head: one slim silhouette, coronet spiking the crown -------------
BODY = ("M312,346 "
        "C326,338 350,335 370,338 "
        "C390,341 400,330 408,318 "
        "L415,306 L423,316 L433,303 L442,315 L451,301 L460,314 L468,307 "
        "C475,315 478,324 476,333 "
        "C484,346 498,356 510,368 "
        "C542,392 562,424 567,462 "
        "C571,506 558,548 534,578 "
        "C520,596 506,606 492,612 "
        "C476,604 462,592 452,574 "
        "C438,552 424,532 414,506 "
        "C402,476 402,444 412,414 "
        "C418,398 428,388 440,382 "
        "C430,376 418,372 406,372 "
        "C390,374 374,372 360,366 "
        "C342,359 326,354 312,346 Z")
d.path(BODY, "Trunk", fill=BODY_GRAD, stroke=INK, strokeWidth=7)

# back shading + belly light
d.path("M510,368 C542,392 562,424 567,462 C571,506 558,548 534,578 "
       "C548,536 550,478 536,434 C528,408 518,386 510,368 Z",
       "Back shade", fill="#3E3018", opacity=35, stroke=NONE)
d.shape("ellipse", "Belly light", x=410, y=440, width=80, height=120,
        fill="#EAD9A0", opacity=28, stroke=NONE)
# saddle patches across the back
for i, dd in enumerate(["M522,394 C548,406 562,428 568,452",
                        "M560,490 C566,510 562,536 548,560"]):
    d.path(dd, f"Saddle {i+1}", fill=NONE, stroke="#4E3E1E",
           strokeWidth=13, opacity=30, cap="round")

# belly rings: transverse arcs rising off the belly edge
for i, (x0, y0, x1, y1) in enumerate([(412, 428, 505, 430), (408, 462, 522, 464),
                                      (410, 496, 536, 498), (418, 530, 542, 528),
                                      (432, 560, 528, 556)]):
    d.path(f"M{x0},{y0} C{(x0 + x1) / 2},{(y0 + y1) / 2 + 8} {x1 - 24},{y1 + 6} {x1},{y1 - 2}",
           f"Ring {i+1}", fill=NONE, stroke="#4E3E1E",
           strokeWidth=3, opacity=38, cap="round")
# the pale "lines" that name the species
for i, (x, y, x2, y2) in enumerate([(452, 404, 468, 428), (436, 452, 450, 478),
                                    (470, 472, 484, 496), (448, 514, 460, 538),
                                    (496, 434, 510, 456), (498, 522, 510, 546)]):
    d.path(f"M{x},{y} C{x + 4},{(y + y2) / 2} {x2 - 4},{(y + y2) / 2} {x2},{y2}",
           f"Pale line {i+1}", fill=NONE, stroke="#EFE3B4",
           strokeWidth=3, opacity=55, cap="round")

# back spines along the dorsal edge
for i, (x, y, dx, dy) in enumerate([(524, 380, 13, -8), (546, 400, 15, -6), (560, 426, 16, -3),
                                    (570, 458, 16, 0), (570, 490, 14, 4), (560, 522, 12, 7),
                                    (544, 552, 10, 9)]):
    d.path(f"M{x},{y} L{x + dx},{y + dy} L{x - 4},{y + 12} Z",
           f"Spine {i+1}", fill="#6B572A", stroke=INK, strokeWidth=2)

# --- fins -----------------------------------------------------------------------
# dorsal fin: small translucent fan low on the back
d.path("M564,492 C592,470 626,466 644,478 C640,506 618,532 588,542 "
       "C572,546 562,534 560,516 Z",
       "Dorsal fin", fill="#D8C684", opacity=45, stroke=INK, strokeWidth=3)
for i, (x2, y2) in enumerate([(632, 482), (636, 504), (622, 524), (598, 536)]):
    d.path(f"M566,504 C590,{492 + i * 7} {x2 - 14},{y2 - 6} {x2},{y2}",
           f"Fin ray {i+1}", fill=NONE, stroke="#6B572A",
           strokeWidth=3, opacity=50, cap="round")
# pectoral fin behind the cheek
d.path("M470,368 C486,358 500,360 505,371 C501,384 488,391 477,386 "
       "C469,381 466,375 470,368 Z",
       "Pectoral fin", fill="#D8C684", opacity=50, stroke=INK, strokeWidth=3)
d.path("M474,376 C486,370 496,372 502,378", "Pec ray", fill=NONE,
       stroke="#6B572A", strokeWidth=2, opacity=50, cap="round")

# --- face -----------------------------------------------------------------------
d.shape("ellipse", "Eye", x=402, y=340, width=19, height=21,
        fill="#241C10", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Eye glint", x=407, y=344, width=6, height=6,
        fill="#FFF8E0", opacity=90, stroke=NONE)
d.path("M394,338 C402,329 416,327 426,334", "Brow", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.shape("ellipse", "Nostril", x=318, y=342, width=6, height=5,
        fill="#241C10", opacity=80, stroke=NONE)
d.path("M312,346 C318,352 328,354 338,353", "Mouth line", fill=NONE,
       stroke=INK, strokeWidth=3, opacity=70, cap="round")
# cheek plate seam + throat rings
d.path("M438,362 C448,374 450,390 444,404", "Gill seam", fill=NONE,
       stroke="#4E3E1E", strokeWidth=3, opacity=50, cap="round")
for i, y in enumerate([384, 398]):
    d.path(f"M414,{y} C428,{y + 6} 442,{y + 5} 452,{y - 2}", f"Throat ring {i+1}",
           fill=NONE, stroke="#4E3E1E", strokeWidth=3, opacity=40, cap="round")

# one blade crossing in front of the tail for depth
blade((352, 758), (376, 636), (350, 552), 9, 3, "Blade front",
      fill="#2E6242", opacity=85, stroke=NONE)

# --- name ---------------------------------------------------------------------------
d.text("LINED SEAHORSE", "Name", x=500, y=962, size=56, font="Virelai Sans",
       color="#D8E6C4", justify="center")

d.finish("lined-seahorse-V1R00")
