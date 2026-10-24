#!/usr/bin/env python3
"""Mosasaurus — field plate V1R00. The lizard that took the ocean: long
countershaded body cruising just under the surface, head and neck breaching
the waterline at left with a foam ring and a flung crown of droplets, jaws
open. Tail ends in the two-lobed fluke; pectoral paddle tucked under the
trunk. Pale air-glare cap above the wave line, deep teal water below
closing on the disc's own arc. Cretaceous-sea plate, surface-break mood.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Mosasaurus — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420
INK = "#0E1C1E"                    # warm-dark teal ink, never pure black

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

def cubic(p0, p1, p2, p3, t):
    u = 1 - t
    return (u**3*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t**3*p3[0],
            u**3*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t**3*p3[1])

def ribbon(p0, p1, p2, p3, w0, w1, label, n=22, **kw):
    L, Rr = [], []
    for k in range(n + 1):
        t = k / n
        x, y = cubic(p0, p1, p2, p3, t)
        x0, y0 = cubic(p0, p1, p2, p3, max(0, t - 0.01))
        x1, y1 = cubic(p0, p1, p2, p3, min(1, t + 0.01))
        dx, dy = x1 - x0, y1 - y0
        ln = math.hypot(dx, dy) or 1
        w = (w0 + (w1 - w0) * t) / 2
        L.append((x - dy/ln * w, y + dx/ln * w))
        Rr.append((x + dy/ln * w, y - dx/ln * w))
    s = "M%.1f,%.1f " % L[0] + " ".join("L%.1f,%.1f" % p for p in L[1:])
    s += " " + " ".join("L%.1f,%.1f" % p for p in reversed(Rr)) + " Z"
    return d.path(s, label, **kw)

BG_GRAD    = lin(0, 0, 0, 1000, (0, "#0A1418"), (1, "#030607"))
PLATE_GRAD = rad((0, "#E4EEE0"), (0.55, "#9EBCAC"), (1, "#4A6E62"))
WATER_GRAD = lin(0, 330, 0, 880, (0, "#4A8884"), (0.45, "#20525A"), (1, "#0A2530"))
HIDE_GRAD  = lin(0, 300, 0, 640, (0, "#66847C"), (0.5, "#3E5C56"), (1, "#243C38"))
BELLY      = "#A8C0AC"
FOAM       = "#EAF6EE"

# --- backdrop + sea plate ---------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#7EA89C", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#2E4A42", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#EAF4E8", strokeWidth=3, opacity=45)
# pale glare in the air cap
d.shape("ellipse", "Air glare", x=560, y=120, width=300, height=140,
        fill="#F6F4DC", opacity=15, stroke=NONE)

# --- the sea: wavy surface line, water closing on the disc's own arc ----------------------
wy = 336
wl, wr = rim_x(wy, side=-1), rim_x(wy, side=1)
d.path(f"M{wl:.1f},{wy} C280,{wy-12} 400,{wy+10} 540,{wy-4} "
       f"C660,{wy-14} 780,{wy+8} {wr:.1f},{wy} "
       f"A{R},{R} 0 1 1 {wl:.1f},{wy} Z", "Sea", fill=WATER_GRAD, stroke=NONE)
# the crest: light along the surface line
d.path(f"M{wl+8:.0f},{wy-4} C280,{wy-16} 400,{wy+6} 540,{wy-8} "
       f"C660,{wy-18} 780,{wy+4} {wr-8:.0f},{wy-4}",
       "Surface crest", fill=NONE, stroke=FOAM, strokeWidth=5, opacity=55, cap="round")
# sunshafts slanting down through the water
for i, dd in enumerate(["M600,340 L516,620 L556,626 L640,342 Z",
                        "M430,344 L396,560 L428,564 L462,342 Z"]):
    d.path(dd, f"Sunshaft {i+1}", fill="#DFF0E4", opacity=7, stroke=NONE)
# marine snow
for i, (x, y, w) in enumerate([(250,430,5),(760,420,6),(210,560,5),(830,540,5),
                               (300,690,4),(740,680,6),(420,380,4),(600,376,5),
                               (180,640,4),(850,620,4),(500,760,5),(660,760,4)]):
    d.shape("ellipse", f"Snow {i+1}", x=x, y=y, width=w, height=w,
            fill="#C8E4D8", opacity=35, stroke=NONE)
# a dim ammonite drifting in the deep, lower left
d.shape("ellipse", "Ammonite shell", x=252, y=672, width=64, height=60,
        fill="#2E4E48", opacity=55, stroke="#162E2A", strokeWidth=3)
for i, (cx, cy, w) in enumerate([(276, 694, 34), (276, 696, 20), (276, 697, 9)]):
    d.shape("ellipse", f"Ammonite coil {i+1}", x=cx-w/2, y=cy-w/2, width=w, height=w,
            fill=NONE, stroke="#162E2A", strokeWidth=2.5, opacity=60)

# === the animal (submerged body slightly ghosted under the water) ========================
# --- tail + two-lobed fluke --------------------------------------------------------------
d.path("M770,452 C806,440 838,434 862,438 C854,454 836,466 812,472 "
       "C800,474 784,468 770,452 Z",
       "Fluke upper", fill=HIDE_GRAD, stroke=INK, strokeWidth=4, opacity=88)
d.path("M776,470 C806,490 828,514 832,544 C812,536 792,516 780,492 "
       "C774,482 772,474 776,470 Z",
       "Fluke lower", fill=HIDE_GRAD, stroke=INK, strokeWidth=4, opacity=88)

# --- rear paddle, darker (far side) -------------------------------------------------------
d.path("M676,520 C664,536 658,556 664,570 C672,580 688,578 696,566 "
       "C702,554 700,536 690,524 C684,518 680,516 676,520 Z",
       "Paddle far", fill="#243C38", opacity=85, stroke=NONE)

# --- trunk: the long body running to the tail ---------------------------------------------
d.path("M424,404 C490,398 590,412 680,432 C730,442 768,452 794,462 "
       "C780,494 744,522 694,540 C610,566 512,564 460,540 "
       "C424,522 408,486 412,450 C415,428 418,412 424,404 Z",
       "Trunk", fill=HIDE_GRAD, stroke=INK, strokeWidth=5, opacity=88)
# pale belly — the countershade
d.path("M432,486 C470,524 560,552 646,544 C700,538 742,518 768,492 "
       "C740,532 660,560 560,558 C500,556 452,534 432,486 Z",
       "Belly", fill=BELLY, opacity=45, stroke=NONE)
# low dorsal ridge along the back
d.path("M446,408 C520,398 610,410 690,432 C730,442 760,452 780,462 "
       "C740,446 640,420 540,412 C500,408 468,406 446,408 Z",
       "Dorsal ridge", fill="#162E2A", opacity=50, stroke=NONE)
# flank scale flecks
for i, (x, y, w) in enumerate([(520,440,14),(590,448,12),(660,448,13),(480,470,10),
                               (550,486,12),(620,480,11),(700,470,10),(510,512,9),
                               (600,516,10),(680,506,9)]):
    d.shape("ellipse", f"Scale {i+1}", x=x, y=y, width=w, height=w*0.5,
            fill="#162E2A", opacity=25, stroke=NONE)
# lateral line
d.path("M440,470 C520,472 620,480 720,486", "Lateral line", fill=NONE,
       stroke="#8AA89A", strokeWidth=3.5, opacity=40, cap="round")

# --- pectoral paddle (near side) ----------------------------------------------------------
d.path("M508,516 C492,538 484,562 490,580 C498,594 518,594 530,580 "
       "C540,566 542,544 532,526 C524,514 514,510 508,516 Z",
       "Paddle near", fill=HIDE_GRAD, stroke=INK, strokeWidth=4, opacity=88)
d.path("M498,540 C496,556 500,570 508,580", "Paddle crease", fill=NONE,
       stroke="#162E2A", strokeWidth=3.5, opacity=50, cap="round")

# --- neck rising through the surface -------------------------------------------------------
ribbon((432,438), (404,406), (376,372), (348,338), 58, 38,
       "Neck", fill=HIDE_GRAD, stroke=INK, strokeWidth=4, opacity=90)

# --- head above the waterline, jaws open ---------------------------------------------------
# skull + upper jaw: long tapering snout
d.path("M344,320 C330,300 306,286 278,278 C258,272 240,272 232,280 "
       "C226,286 230,294 240,298 C266,306 298,320 320,338 "
       "C332,348 346,346 352,336 C356,328 352,324 344,320 Z",
       "Upper jaw", fill=lin(344, 270, 240, 330, (0, "#5E7A72"), (0.6, "#3E5C56"), (1, "#2A4440")),
       stroke=INK, strokeWidth=5)
# mouth interior — the dark gape
d.path("M242,296 C268,304 298,318 318,336 C304,342 276,332 254,320 "
       "C244,314 238,306 242,296 Z", "Gape", fill="#3A1416", stroke=NONE)
# lower jaw dropped open
d.path("M338,346 C316,348 284,342 256,328 C246,322 242,314 248,308 "
       "C256,302 270,304 286,312 C306,322 326,336 338,346 Z",
       "Lower jaw", fill=lin(338, 308, 250, 348, (0, "#4E6B62"), (1, "#2A4440")),
       stroke=INK, strokeWidth=4.5)
# teeth: conical, upper jaw pointing down, lower pointing up
for i, (x, y) in enumerate([(250,300),(266,306),(282,312),(298,320),(312,328)]):
    d.path(f"M{x-4},{y-2} L{x+4},{y+1} L{x+1},{y+10} Z",
           f"Tooth U{i+1}", fill="#E8E4CC", stroke=INK, strokeWidth=1.5)
for i, (x, y) in enumerate([(258,314),(274,320),(290,327),(306,333)]):
    d.path(f"M{x-4},{y+3} L{x+4},{y+1} L{x+1},{y-8} Z",
           f"Tooth L{i+1}", fill="#E8E4CC", stroke=INK, strokeWidth=1.5)
# nostril + eye + brow
d.shape("ellipse", "Nostril", x=260, y=284, width=11, height=7,
        fill="#0E1C1E", opacity=80, stroke=NONE)
d.shape("ellipse", "Eye socket", x=320, y=310, width=30, height=22,
        fill="#0E1C1E", opacity=35, stroke=NONE)
d.shape("ellipse", "Eye", x=328, y=313, width=15, height=14,
        fill="#0A140E", stroke=NONE)
d.shape("ellipse", "Eye glint", x=332, y=315, width=4.5, height=4.5,
        fill="#EAF6EE", opacity=90, stroke=NONE)
d.path("M314,308 C326,298 344,296 356,302", "Brow", fill=NONE,
       stroke=INK, strokeWidth=4, opacity=70, cap="round")
# wet sheen on the snout
d.path("M252,282 C270,276 296,282 316,296", "Snout sheen", fill=NONE,
       stroke="#CFE4D8", strokeWidth=4, opacity=50, cap="round")

# --- the breach: foam collar + flung droplets ----------------------------------------------
d.shape("ellipse", "Foam collar", x=296, y=326, width=170, height=24,
        fill=NONE, stroke=FOAM, strokeWidth=6, opacity=70)
d.shape("ellipse", "Foam inner", x=330, y=330, width=96, height=14,
        fill=FOAM, opacity=35, stroke=NONE)
# splash crown: short arcs up both sides of the neck
for i, dd in enumerate(["M306,322 C296,310 290,298 292,286",
                        "M330,316 C324,302 322,290 326,278",
                        "M392,320 C400,308 404,296 402,284",
                        "M420,326 C432,318 440,306 442,294"]):
    d.path(dd, f"Splash {i+1}", fill=NONE, stroke=FOAM,
           strokeWidth=4.5, opacity=65, cap="round")
for i, (x, y, w) in enumerate([(288,272,7),(318,266,6),(404,270,7),(448,282,5),
                               (346,254,5),(424,258,5)]):
    d.shape("ellipse", f"Droplet {i+1}", x=x, y=y, width=w, height=w,
            fill=FOAM, opacity=80, stroke=NONE)
# wake rolling off the breach, left along the surface
d.path("M180,338 C230,328 280,330 310,338", "Wake L", fill=NONE,
       stroke=FOAM, strokeWidth=4, opacity=45, cap="round")
d.path("M470,342 C540,330 620,332 680,342", "Wake R", fill=NONE,
       stroke=FOAM, strokeWidth=4, opacity=40, cap="round")
# bubbles rising beside the neck
for i, (x, y, w) in enumerate([(452,300,10),(462,272,14),(472,238,8),(452,206,12)]):
    d.shape("ellipse", f"Breach bubble {i+1}", x=x, y=y, width=w, height=w,
            fill=FOAM, opacity=30, stroke=NONE)

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#1E3A32", strokeWidth=6)

# --- name ----------------------------------------------------------------------------------
d.text("MOSASAURUS", "Name", x=500, y=962, size=56, font="Virelai Sans",
       color="#E2EEE4", justify="center")

d.finish("mosasaurus-V1R00")
