#!/usr/bin/env python3
"""Red kangaroo — field-guide plate V1R00. The outback's own piston, caught
mid-bound in side profile: tail streaming level as counterweight, hind legs
folded under with the long feet dangling, forearms tucked, ears raked back
at speed. Baked red-dust plate under a noon-white sun, heat shimmer over a
flat mesa horizon, spinifex on the dust floor. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Red Kangaroo — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420          # plate disc centre + radius
INK = "#341309"

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def on_disc(x, y, pad=0):
    return math.hypot(x - CX, y - CY) <= R - pad

def quad(p0, p1, p2, t):
    u = 1 - t
    return (u*u*p0[0] + 2*u*t*p1[0] + t*t*p2[0],
            u*u*p0[1] + 2*u*t*p1[1] + t*t*p2[1])

def ribbon(p0, p1, p2, w0, w1, label, n=20, **kw):
    """Tapered strip along a quadratic; w0/w1 are full widths at root/tip."""
    L, Rr = [], []
    for k in range(n + 1):
        t = k / n
        x, y = quad(p0, p1, p2, t)
        x0, y0 = quad(p0, p1, p2, max(0, t - 0.01))
        x1, y1 = quad(p0, p1, p2, min(1, t + 0.01))
        dx, dy = x1 - x0, y1 - y0
        ln = math.hypot(dx, dy) or 1
        w = (w0 + (w1 - w0) * t) / 2
        L.append((x - dy/ln * w, y + dx/ln * w))
        Rr.append((x + dy/ln * w, y - dx/ln * w))
    s = "M%.1f,%.1f " % L[0] + " ".join("L%.1f,%.1f" % p for p in L[1:])
    s += " " + " ".join("L%.1f,%.1f" % p for p in reversed(Rr)) + " Z"
    return d.path(s, label, **kw)

BG_GRAD = lin(0, 0, 0, 1000, (0, "#1E0C05"), (1, "#0A0301"))
PLATE_GRAD = rad((0, "#F2A75E"), (0.55, "#D97B3C"), (1, "#9A4A1E"))
FLOOR_GRAD = lin(0, 735, 0, 890, (0, "#9A441C"), (1, "#57210B"))
FUR = lin(500, 290, 480, 660, (0, "#E8944C"), (0.5, "#C4642A"), (1, "#8C3E18"))
FUR_DARK = lin(500, 420, 500, 700, (0, "#9A4620"), (1, "#662610"))

# --- backdrop + red-dust plate -------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#E08A44", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#6E2E10", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#FFD9A8", strokeWidth=3, opacity=45)

# noon sun, high in the plate, with a bleached-hot glow
d.shape("ellipse", "Sun glow", x=320, y=60, width=290, height=210,
        fill=rad((0, "#FFF3D0"), (1, "#FFF3D0")), opacity=22, stroke=NONE)
d.shape("ellipse", "Sun", x=420, y=118, width=96, height=96,
        fill=rad((0, "#FFFDF0"), (0.75, "#FFEFC0"), (1, "#F8DCA0")),
        stroke="#FFE9BC", strokeWidth=2)

# heat shimmer: faint wavy lines across the upper sky
for i, (y, amp, op) in enumerate([(268, 7, 14), (308, 9, 12), (352, 8, 10), (396, 10, 8)]):
    pts = "M180,%.0f" % y + "".join(
        " Q%.0f,%.0f %.0f,%.0f" % (x + 42.5, y + (amp if k % 2 == 0 else -amp), x + 85, y)
        for k, x in enumerate(range(180, 775, 85)))
    d.path(pts, f"Shimmer {i+1}", fill=NONE, stroke="#FFE9C4", strokeWidth=4,
           opacity=op, cap="round")

# distant mesas on the horizon, baked almost into the haze
ly = 742
ldx = math.sqrt(R * R - (ly - CY) ** 2)
d.path("M196,742 L206,714 L232,706 L300,706 L318,714 L328,742 Z",
       "Mesa left", fill="#8A3C18", opacity=45, stroke=NONE)
d.path("M700,742 L710,720 L736,713 L788,713 L800,721 L806,742 Z",
       "Mesa right", fill="#8A3C18", opacity=38, stroke=NONE)

# dust floor: top edge dips and rises gently, bottom closes on the disc arc
d.path(f"M{CX-ldx:.1f},{ly} C340,730 440,736 540,733 C650,730 740,735 {CX+ldx:.1f},{ly} "
       f"A{R},{R} 0 0 1 {CX-ldx:.1f},{ly} Z", "Dust floor", fill=FLOOR_GRAD, stroke=NONE)
# shimmer along the horizon line
d.path(f"M{CX-ldx+8:.1f},{ly-2} C340,728 440,734 540,731 C650,728 740,733 {CX+ldx-8:.1f},{ly-2}",
       "Horizon light", fill=NONE, stroke="#F0B070", strokeWidth=5, opacity=38, cap="round")

# spinifex clumps: dry spiky fans along the horizon
def spinifex(x, y, s, label):
    for j, (a, ln) in enumerate([(-58, 26), (-38, 34), (-18, 30), (0, 36),
                                 (18, 30), (38, 34), (58, 25)]):
        r = math.radians(a - 90)
        x1 = x + math.cos(r) * ln * s
        y1 = y + math.sin(r) * ln * s
        d.path(f"M{x},{y} Q{x + (x1-x)*0.5},{y + (y1-y)*0.7} {x1:.0f},{y1:.0f}",
               f"{label}.{j+1}", fill=NONE, stroke="#C89A50", strokeWidth=3,
               opacity=60, cap="round")
spinifex(252, 746, 1.0, "Spinifex 1")
spinifex(316, 748, 0.75, "Spinifex 2")
spinifex(770, 744, 0.9, "Spinifex 3")
spinifex(722, 747, 0.65, "Spinifex 4")

# drifting dust motes in the heat
for i, (x, y, w) in enumerate([(200,330,5),(830,320,5),(160,520,6),(852,500,5),(235,660,4),
                               (770,690,5),(140,430,4),(868,410,5),(400,120,5),(610,110,4),
                               (330,140,4),(690,150,5),(300,790,4),(660,800,5),(500,840,4)]):
    assert on_disc(x, y, 12), (x, y)
    d.shape("ellipse", f"Dust {i+1}", x=x, y=y, width=w, height=w,
            fill="#E8A860", opacity=35, stroke=NONE)

# === the kangaroo, mid-bound, facing right =====================================
# --- tail: streams back almost level with the spine ------------------------------
ribbon((388, 448), (258, 492), (138, 566), 50, 8, "Tail",
       fill=lin(388, 448, 138, 566, (0, "#B85A26"), (1, "#80401A")),
       stroke=INK, strokeWidth=4)
d.path("M372,452 C300,478 220,520 152,556", "Tail top light", fill=NONE,
       stroke="#E89458", strokeWidth=5, opacity=45, cap="round")
assert on_disc(138, 566, 12)

# --- far hind leg: one folded silhouette, behind the torso, darker ----------------
d.path("M420,480 C448,468 485,468 508,488 C526,505 530,530 524,552 "
       "C552,566 610,588 662,604 C674,608 677,619 667,625 "
       "C632,632 568,620 530,600 C516,590 510,575 510,560 "
       "C492,542 468,528 446,515 C430,505 414,494 420,480 Z",
       "Far hind leg", fill=FUR_DARK, stroke=INK, strokeWidth=3, opacity=85)
# far forearm peeking under the chest
ribbon((598, 440), (618, 470), (644, 478), 14, 8, "Far forearm",
       fill=FUR_DARK, stroke=NONE, opacity=75)
# far ear rakes further back, splayed away from the near one
d.path("M646,300 C612,280 580,255 558,222 C552,212 559,203 569,208 "
       "C604,224 634,258 652,294 Z", "Far ear", fill="#7E3414",
       stroke=INK, strokeWidth=3)

# --- body: torso, neck and head as one grand silhouette ---------------------------
d.path("M375,442 C400,395 445,368 505,360 C548,354 575,358 590,372 "
       "C598,355 610,338 624,326 C640,310 660,298 680,294 "
       "C710,288 738,301 751,322 C760,337 762,352 754,361 "
       "C746,371 732,374 718,370 C696,365 676,361 662,356 "
       "C652,352 646,352 642,355 C632,372 622,392 616,414 "
       "C612,436 614,458 604,478 C570,494 505,505 448,498 "
       "C410,494 384,480 375,462 C372,455 372,449 375,442 Z",
       "Body", fill=FUR, stroke=INK, strokeWidth=5)
# noon sun on the loin
d.path("M415,398 C455,372 520,363 580,372", "Back light", fill=NONE,
       stroke="#F8C084", strokeWidth=10, opacity=40, cap="round")
# cream belly + chest
d.path("M415,478 C455,494 535,500 592,490 C572,506 480,514 428,498 "
       "C410,492 406,485 415,478 Z", "Belly cream", fill="#F2C48C", opacity=50, stroke=NONE)

# --- near hind leg: thigh, hock and long foot in one silhouette --------------------
d.path("M435,482 C465,468 505,468 528,490 C546,507 550,534 542,560 "
       "C575,576 640,600 700,617 C713,621 716,633 705,639 "
       "C668,647 596,635 552,612 C538,600 530,584 529,568 "
       "C506,548 476,532 452,517 C435,506 428,492 435,482 Z",
       "Near hind leg", fill=lin(460, 470, 640, 640, (0, "#D8803E"), (1, "#8A3C16")),
       stroke=INK, strokeWidth=5)
# thigh muscle: sun on the quad, shade in the fold
d.path("M452,492 C475,478 508,478 526,496", "Quad light", fill=NONE,
       stroke="#F4B878", strokeWidth=9, opacity=45, cap="round")
d.path("M445,505 C470,522 505,540 528,556", "Thigh fold shade", fill=NONE,
       stroke="#7E3010", strokeWidth=8, opacity=35, cap="round")
# foot underside shade
d.path("M560,602 C605,622 660,634 700,632", "Foot shade", fill=NONE,
       stroke="#7E3010", strokeWidth=6, opacity=30, cap="round")
# toe claws
for i, (x, y) in enumerate([(710, 638), (702, 628)]):
    d.path(f"M{x},{y} l9,{4 - i*2}", f"Toe claw {i+1}", fill=NONE,
           stroke=INK, strokeWidth=3, cap="round")
assert on_disc(713, 621, 10) and on_disc(674, 608, 10)

# --- near forearm: dangling loose at the bound --------------------------------------
ribbon((604, 448), (622, 478), (648, 488), 15, 8, "Near forearm",
       fill=lin(604, 448, 648, 488, (0, "#C4642A"), (1, "#8A3C16")),
       stroke=INK, strokeWidth=3)
d.shape("ellipse", "Forepaw", x=646, y=482, width=15, height=11,
        fill="#8A3C16", stroke=INK, strokeWidth=2.5)
for i in range(2):
    d.path(f"M{658 + i*4},{486 + i*2} l6,-1", f"Paw claw {i+1}", fill=NONE,
           stroke=INK, strokeWidth=2, cap="round")

# --- face ---------------------------------------------------------------------------
# muzzle shading + nose leather at the tip
d.path("M716,340 C732,344 746,352 753,360 C746,371 732,374 718,370 "
       "C722,360 721,349 716,340 Z", "Muzzle shade", fill="#7E3414", opacity=38, stroke=NONE)
d.shape("ellipse", "Nose", x=742, y=355, width=15, height=11,
        fill="#3A1408", stroke=NONE)
d.shape("ellipse", "Nostril", x=747, y=358, width=5, height=4,
        fill="#0C0502", stroke=NONE)
# mouth line
d.path("M716,368 C728,372 742,371 751,364", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=3, cap="round")
# pale cheek + chin — reds carry cream on the muzzle underside
d.path("M668,358 C685,366 705,370 722,370", "Chin cream", fill=NONE,
       stroke="#F2C48C", strokeWidth=7, opacity=45, cap="round")
# whisker dots + fine whiskers ahead of the nose
for i, (x, y) in enumerate([(730, 350), (736, 354), (727, 357)]):
    d.shape("ellipse", f"Whisker dot {i+1}", x=x-2, y=y-2, width=4, height=4,
            fill="#5E2A10", opacity=60, stroke=NONE)
d.path("M734,348 Q754,342 766,336", "Whisker 1", fill=NONE,
       stroke="#F2C48C", strokeWidth=1.8, opacity=50, cap="round")
d.path("M736,355 Q756,354 768,352", "Whisker 2", fill=NONE,
       stroke="#F2C48C", strokeWidth=1.8, opacity=50, cap="round")
# eye: amber, alert
d.shape("ellipse", "Eye socket shade", x=680, y=311, width=30, height=26,
        fill="#8A3C16", opacity=45, stroke=NONE)
d.shape("ellipse", "Eye", x=686, y=315, width=17, height=19,
        fill=rad((0, "#4A2210"), (1, "#180A04")), stroke=INK, strokeWidth=2)
d.shape("ellipse", "Eye glint", x=690, y=318, width=5, height=5,
        fill="#FFFFFF", opacity=90, stroke=NONE)
# brow line
d.path("M676,309 C688,303 704,303 714,309", "Brow", fill=NONE,
       stroke=INK, strokeWidth=3.5, opacity=60, cap="round")

# --- near ear: tall blade raked back at speed ----------------------------------------
d.path("M666,296 C645,268 622,234 610,196 C607,185 616,178 625,185 "
       "C652,208 668,250 672,290 Z", "Near ear",
       fill=rad((0, "#D8803E"), (1, "#8A3C16")), stroke=INK, strokeWidth=4)
d.path("M660,286 C645,262 630,234 622,204 C621,197 626,195 630,200 "
       "C648,222 658,254 662,282 Z", "Inner ear", fill="#F4C896", opacity=65, stroke=NONE)
# dark ear tip
d.path("M610,196 C607,185 616,178 625,185 C626,192 622,197 617,197 "
       "C614,197 611,196 610,196 Z", "Ear tip", fill="#4A1E0C", opacity=70, stroke=NONE)

# --- volume: rump shade + chest tuck -------------------------------------------------
d.path("M378,455 C374,472 384,488 402,496 C388,496 377,487 373,474 "
       "C370,464 372,457 378,455 Z", "Rump shade", fill="#5E220C", opacity=45, stroke=NONE)
d.path("M560,492 C590,488 608,480 616,470 C614,486 596,496 575,500 Z",
       "Chest tuck shade", fill="#5E220C", opacity=35, stroke=NONE)

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#3A1408", strokeWidth=6)

# --- caption ---------------------------------------------------------------------
d.text("RED KANGAROO", "Name", x=500, y=940, size=58, font="Virelai Sans",
       color="#F6DCA8", justify="center")
LINE2, SZ2, TRK = "MACROPUS RUFUS", 22, 340
r = d.text(LINE2, "Second line", x=500, y=975, size=SZ2, font="Virelai Sans",
           color="#CE9A66", justify="center")
if r and "id" in r:
    d.cmd("text.setStyle", "Second line tracking", id=r["id"], tracking=TRK)

def find(o, oid):
    if isinstance(o, dict):
        if o.get("id") == oid and "bounds" in o: return o
        o = list(o.values())
    if isinstance(o, list):
        for v in o:
            hit = find(v, oid)
            if hit: return hit
if r and "id" in r:
    b2 = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
    print("second line bounds", {k: round(v) for k, v in b2.items()})
    assert b2["width"] <= 760 and b2["x"] >= 100 and b2["y"] + b2["height"] <= 990, b2

d.finish("red-kangaroo-V1R00")
