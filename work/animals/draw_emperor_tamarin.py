#!/usr/bin/env python3
"""Emperor tamarin — field-guide plate V1R00. Three-quarter bust, a tiny
monkey outranked by its own moustache: long white whiskers sweeping past
the jaw, dark face, salt-and-pepper grey fur over a rusty chest, and the
long red-brown tail curling back into frame. Mossy green plate, warm
highlights from the upper left; bust and fern close on the disc's own arc.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Emperor Tamarin — Field Plate", 1000, 1000)

INK = "#1C1712"
WARM = "#FFD27A"                   # warm highlight, from the upper left
CX, CY, R = 500, 460, 420          # plate disc centre + radius
rng = random.Random(57)

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def on_disc(deg):
    t = math.radians(deg)
    return CX + R*math.cos(t), CY + R*math.sin(t)

def cubic(p0, p1, p2, p3, t):
    u = 1 - t
    return (u**3*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t**3*p3[0],
            u**3*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t**3*p3[1])

def spine_of(segs, n=16):
    pts = []
    for k, seg in enumerate(segs):
        pts += [cubic(*seg, i/n) for i in range(0 if k == 0 else 1, n + 1)]
    return pts

def ribbon(pts, w0, w1, round_tip=True):
    """Closed tapered outline around a polyline spine; returns (d, normals)."""
    L, Rr, norms, n = [], [], [], len(pts)
    for i, (x, y) in enumerate(pts):
        ax, ay = pts[max(i - 1, 0)]; bx, by = pts[min(i + 1, n - 1)]
        dx, dy = bx - ax, by - ay
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy/ln, dx/ln
        w = (w0 + (w1 - w0)*i/(n - 1)) / 2
        norms.append((nx, ny, w))
        L.append((x + nx*w, y + ny*w)); Rr.append((x - nx*w, y - ny*w))
    dd = "M%.1f,%.1f " % L[0] + " ".join("L%.1f,%.1f" % p for p in L[1:])
    tw = norms[-1][2]
    dd += (" A%.1f,%.1f 0 0 0 %.1f,%.1f " % (tw, tw, *Rr[-1])) if round_tip else " L%.1f,%.1f " % Rr[-1]
    dd += " ".join("L%.1f,%.1f" % p for p in reversed(Rr[:-1])) + " Z"
    return dd, norms

def offset_line(pts, norms, f, a=0, b=None):
    sel = list(zip(pts, norms))[a:b]
    return "M" + " L".join("%.1f,%.1f" % (x + nx*w*f, y + ny*w*f) for (x, y), (nx, ny, w) in sel)

BG_GRAD = lin(0, 0, 0, 1000, (0, "#1F2A17"), (1, "#090D06"))
PLATE_GRAD = rad((0, "#B4C487"), (0.6, "#84995A"), (1, "#4C5F33"))
HEAD_GRAD = rad((0, "#A08E7C"), (0.6, "#6E5E50"), (1, "#3A3028"))
BUST_GRAD = lin(0, 560, 0, 880, (0, "#8E897A"), (1, "#4A463C"))
CHEST_GRAD = rad((0, "#E0A05A"), (0.7, "#B4703A"), (1, "#86502A"))
TAIL_GRAD = lin(0, 220, 0, 760, (0, "#B8642E"), (1, "#7A3A1A"))
IRIS_GRAD = rad((0, "#D69A48"), (0.6, "#7C4A1E"), (1, "#2A160A"))
STACHE_GRAD = lin(0, 450, 0, 670, (0, "#FFFFFF"), (1, "#D8D6CC"))
FERN_GRAD = lin(0, 520, 0, 880, (0, "#5F7A3A"), (1, "#26361A"))

# --- backdrop + mossy plate -----------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
for i, (x, y, w, o) in enumerate([(70,110,6,35),(140,40,4,25),(45,420,5,30),(925,80,6,35),
                                  (950,360,5,30),(60,820,5,25),(935,820,5,25)]):
    d.shape("ellipse", f"Pollen {i+1}", x=x, y=y, width=w, height=w, fill="#E6D48A", opacity=o, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#2E3A1E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E4EEC4", strokeWidth=3, opacity=45)
# warm light pooling in from the upper left (crescents close on the disc arc)
for k, (w, h) in enumerate([(320, 260), (240, 196), (170, 140), (100, 84)]):
    d.shape("ellipse", f"Warm pool {k+1}", x=360 - w/2, y=270 - h/2, width=w, height=h,
            fill=WARM, opacity=6, stroke=NONE)
# moss patina + lichen dapples
for i, (x, y, w, h) in enumerate([(170,220,200,120),(600,600,240,140),(640,140,150,90),(150,520,150,100)]):
    d.shape("ellipse", f"Moss patch {i+1}", x=x, y=y, width=w, height=h, fill="#5E7638", opacity=13, stroke=NONE)
for i, (x, y, w) in enumerate([(230,300,9),(760,230,8),(190,430,8),(820,420,9),(420,120,8),
                               (580,110,7),(300,180,6),(700,520,7),(840,520,6),(260,620,7)]):
    d.shape("ellipse", f"Lichen {i+1}", x=x, y=y, width=w, height=w, fill="#E8E0A0", opacity=40, stroke=NONE)
# hanging moss strands from the top of the disc
for i, (x0, ln) in enumerate([(318, 120), (338, 160), (358, 96), (630, 110), (650, 170), (672, 130), (694, 84)]):
    top = CY - math.sqrt(R*R - (x0 - CX)**2) + 10
    sway = 10 if i % 2 else -10
    d.path(f"M{x0},{top:.1f} C{x0 + sway},{top + ln*0.35:.1f} {x0 - sway},{top + ln*0.7:.1f} {x0 + sway/2},{top + ln:.1f}",
           f"Hanging moss {i+1}", fill=NONE, stroke=["#4E6630", "#6A8442"][i % 2], strokeWidth=6 - i % 3,
           opacity=50, cap="round")

# fern mass lower left, closing on the disc arc
fx0, fy0 = on_disc(172); fx1, fy1 = on_disc(118)
d.path(f"M{fx0:.1f},{fy0:.1f} Q150,480 214,520 Q170,556 200,590 Q262,580 300,640 "
       f"Q250,660 268,706 Q316,710 330,770 Q300,780 {fx1:.1f},{fy1:.1f} "
       f"A{R},{R} 0 0 1 {fx0:.1f},{fy0:.1f} Z", "Fern L", fill=FERN_GRAD, opacity=90, stroke=NONE)
for i, dd in enumerate(["M104,560 Q160,532 210,522", "M140,650 Q220,620 296,642", "M190,740 Q260,722 326,770"]):
    d.path(dd, f"Fern rib {i+1}", fill=NONE, stroke="#A8BE72", strokeWidth=4, opacity=40, cap="round")
gx0, gy0 = on_disc(10); gx1, gy1 = on_disc(62)
d.path(f"M{gx0:.1f},{gy0:.1f} A{R},{R} 0 0 1 {gx1:.1f},{gy1:.1f} "
       f"Q720,760 760,720 Q740,680 790,650 Q840,640 850,600 Q860,560 {gx0:.1f},{gy0:.1f} Z",
       "Fern R", fill=FERN_GRAD, opacity=70, stroke=NONE)

# --- the long tail, curling back into frame (behind the bust) ----------------------------
tail_pts = spine_of([((650,700), (770,700), (848,640), (854,540)),
                     ((854,540), (860,430), (842,300), (760,244)),
                     ((760,244), (700,206), (650,236), (672,280)),
                     ((672,280), (690,312), (736,300), (728,268))])
tdd, tn = ribbon(tail_pts, 34, 12)
d.path(tdd, "Tail", fill=TAIL_GRAD, stroke=INK, strokeWidth=5)
d.path(offset_line(tail_pts, tn, -0.55, 2, -6), "Tail shade", fill=NONE, stroke="#4E2410",
       strokeWidth=8, opacity=35, cap="round")
d.path(offset_line(tail_pts, tn, 0.45, 4, -10), "Tail light", fill=NONE, stroke="#F0B070",
       strokeWidth=5, opacity=45, cap="round")
for k in range(4, len(tail_pts) - 6, 4):
    (x, y), (nx, ny, w) = tail_pts[k], tn[k]
    d.path(f"M{x + nx*w*0.6:.1f},{y + ny*w*0.6:.1f} L{x - nx*w*0.2:.1f},{y - ny*w*0.2:.1f}",
           f"Tail fur {k}", fill=NONE, stroke="#5A2A12", strokeWidth=3, opacity=40, cap="round")

# --- bust: speckled grey shoulders, closing on the disc arc -------------------------------
bx0, by0 = on_disc(122); bx1, by1 = on_disc(58)
BUST = (f"M{bx0:.1f},{by0:.1f} C286,700 316,566 396,500 C424,480 448,470 470,470 "
        f"L560,470 C590,474 620,490 642,508 C704,566 718,700 {bx1:.1f},{by1:.1f} "
        f"A{R},{R} 0 0 1 {bx0:.1f},{by0:.1f} Z")
d.path(BUST, "Shoulders", fill=BUST_GRAD, stroke=INK, strokeWidth=6)
d.path(f"M{bx0 + 8:.1f},{by0 - 24:.1f} C294,700 322,576 392,512", "Shoulder warm rim",
       fill=NONE, stroke=WARM, strokeWidth=6, opacity=45, cap="round")
d.path("M452,590 C424,650 440,740 478,812 C496,846 538,846 556,812 "
       "C594,740 610,650 580,590 C544,570 488,570 452,590 Z",
       "Chest", fill=CHEST_GRAD, opacity=55, stroke=NONE)
d.path("M470,600 C452,650 460,720 488,780", "Chest light", fill=NONE, stroke="#F4C890",
       strokeWidth=8, opacity=30, cap="round")
# arms hanging in front of the body, to break the bell silhouette
for side, dd in (("L", "M348,612 C376,680 398,750 408,836"), ("R", "M666,620 C640,688 622,756 614,836")):
    d.path(dd, f"Arm contour {side}", fill=NONE, stroke=INK, strokeWidth=5, opacity=70, cap="round")
d.path("M392,640 C408,700 420,760 424,830", "Arm shade L", fill=NONE, stroke="#3A362E", strokeWidth=14, opacity=25, cap="round")
d.path("M626,648 C610,706 600,764 598,830", "Arm shade R", fill=NONE, stroke="#3A362E", strokeWidth=14, opacity=25, cap="round")
d.path("M336,640 C356,700 372,760 380,830", "Arm warm light", fill=NONE, stroke=WARM, strokeWidth=5, opacity=30, cap="round")
for i, dd in enumerate(["M452,690 C460,720 466,750 470,780", "M578,690 C570,720 564,750 560,780",
                        "M516,700 L516,800"]):
    d.path(dd, f"Chest fur {i+1}", fill=NONE, stroke="#7A4420", strokeWidth=4, opacity=40, cap="round")
for i in range(70):
    x, y = rng.uniform(300, 700), rng.uniform(610, 850)
    if ((x - 500)/215)**2 + ((y - 840)/250)**2 > 1 or 440 < x < 592 and y > 590:
        continue
    w = rng.uniform(4, 7)
    d.shape("ellipse", f"Grizzle {i+1}", x=x, y=y, width=w, height=w*0.7,
            fill=rng.choice(["#E8DFC0", "#D6CBA4", "#2A241C"]), opacity=55, stroke=NONE)

for i, dd in enumerate(["M322,640 C328,660 330,680 328,700", "M690,630 C686,650 686,670 690,690"]):
    d.path(dd, f"Shoulder fur {i+1}", fill=NONE, stroke="#3A362E", strokeWidth=4, opacity=40, cap="round")

# --- near ear, mostly buried in fur -------------------------------------------------------
d.shape("ellipse", "Ear", x=626, y=360, width=44, height=58,
        fill=lin(626, 0, 670, 0, (0, "#3A2E26"), (1, "#18120E")), stroke=INK, strokeWidth=5)
d.shape("ellipse", "Inner ear", x=636, y=372, width=22, height=34, fill="#8A6A58", opacity=55, stroke=NONE)

# --- head: three-quarter to the viewer's left ----------------------------------------------
HEAD = ("M502,252 C598,248 662,314 660,398 C658,474 604,532 520,540 "
        "C440,548 372,502 366,422 C360,332 420,256 502,252 Z")
d.path(HEAD, "Head", fill=HEAD_GRAD, stroke=INK, strokeWidth=7)
d.path("M378,370 C392,310 440,268 500,258", "Crown warm rim", fill=NONE, stroke=WARM,
       strokeWidth=7, opacity=45, cap="round")
d.shape("ellipse", "Crown light", x=430, y=266, width=150, height=44, fill="#FFF2D8", opacity=12, stroke=NONE)
for i in range(60):
    x, y = rng.uniform(370, 650), rng.uniform(262, 530)
    if ((x - 508)/136)**2 + ((y - 396)/138)**2 > 0.92 or ((x - 470)/96)**2 + ((y - 428)/96)**2 < 1:
        continue
    w = rng.uniform(3.5, 6)
    d.shape("ellipse", f"Head grizzle {i+1}", x=x, y=y, width=w, height=w*0.7,
            fill=rng.choice(["#C8BC9C", "#A89C80"]), opacity=50, stroke=NONE)
# dark face mask, offset toward the viewer's left
d.path("M470,342 C522,342 556,378 556,424 C556,474 520,506 474,508 "
       "C424,510 388,476 388,428 C388,380 420,342 470,342 Z",
       "Face mask", fill=rad((0, "#3A2E28"), (1, "#14100C")), opacity=95, stroke=NONE)
d.path("M470,334 C530,334 566,376 566,426 C566,480 526,516 474,518 "
       "C418,520 378,482 378,430 C378,376 414,334 470,334 Z", "Mask halo",
       fill=NONE, stroke="#B8AC94", strokeWidth=8, opacity=30)
d.path("M400,388 C426,370 456,368 470,380 C486,368 520,366 548,386", "Brow ridge",
       fill=NONE, stroke="#5E5046", strokeWidth=6, opacity=60, cap="round")
d.path("M394,452 C400,478 418,500 444,508", "Far cheek contour", fill=NONE, stroke="#5E5046",
       strokeWidth=4, opacity=55, cap="round")
d.path("M556,400 C566,430 562,466 540,492", "Near cheek light", fill=NONE, stroke="#8A7A6A",
       strokeWidth=6, opacity=45, cap="round")
# eyes: the near eye larger
d.shape("ellipse", "Eye far", x=418, y=388, width=34, height=30, fill=IRIS_GRAD, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Eye near", x=502, y=384, width=44, height=38, fill=IRIS_GRAD, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Pupil far", x=429, y=397, width=14, height=13, fill="#0A0604", stroke=NONE)
d.shape("ellipse", "Pupil near", x=516, y=395, width=18, height=17, fill="#0A0604", stroke=NONE)
d.shape("ellipse", "Glint far", x=428, y=394, width=7, height=7, fill="#FFFFFF", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint near", x=514, y=391, width=9, height=9, fill="#FFFFFF", opacity=92, stroke=NONE)
d.path("M506,420 C516,426 534,426 544,418", "Lower lid near", fill=NONE, stroke="#6A5A50",
       strokeWidth=3, opacity=60, cap="round")
# pale lips + nose
d.path("M440,448 C452,436 492,436 504,448 C512,470 496,490 472,492 "
       "C448,490 432,470 440,448 Z", "Muzzle skin",
       fill=rad((0, "#F2E4DA"), (1, "#C8AE9E")), opacity=90, stroke=NONE)
d.path("M458,436 C462,428 482,428 486,436 C486,444 478,450 472,450 C466,450 458,444 458,436 Z",
       "Nose", fill=lin(0, 428, 0, 450, (0, "#4A3A32"), (1, "#1A120E")), stroke=INK, strokeWidth=3)
d.shape("ellipse", "Nostril far", x=462, y=440, width=6, height=5, fill="#000000", opacity=60, stroke=NONE)
d.shape("ellipse", "Nostril near", x=475, y=440, width=7, height=5, fill="#000000", opacity=60, stroke=NONE)
d.path("M452,480 C462,486 486,486 496,478", "Mouth", fill=NONE, stroke=INK, strokeWidth=4, cap="round")
# white chin tuft
d.path("M452,494 C460,508 466,524 470,540 C476,524 484,510 494,496 C480,502 466,502 452,494 Z",
       "Chin tuft", fill=STACHE_GRAD, stroke=NONE)

# --- the moustache --------------------------------------------------------------------------
def moustache(segs, w0, label, strands):
    pts = spine_of(segs, 20)
    dd, nn = ribbon(pts, w0, 3)
    d.path(dd, label, fill=STACHE_GRAD, stroke="#9C9A8C", strokeWidth=3)
    d.path(offset_line(pts, nn, -0.45, 3, -4), f"{label} shade", fill=NONE, stroke="#AEB0A6",
           strokeWidth=5, opacity=45, cap="round")
    for k, f in enumerate(strands):
        d.path(offset_line(pts, nn, f, 2, -2 - 3*k), f"{label} strand {k+1}", fill=NONE,
               stroke="#FFFFFF", strokeWidth=3, opacity=80, cap="round")
    return pts, nn

moustache([((466,462), (420,456), (372,478), (352,528)),
           ((352,528), (336,572), (318,610), (290,634))], 24, "Moustache far", [0.9, 1.5])
p, n = moustache([((480,462), (540,454), (604,478), (628,540)),
                  ((628,540), (646,590), (662,636), (694,660))], 30, "Moustache near", [0.9, -1.3, 1.6])
d.path(offset_line(p, n, 0.3, 4, 24), "Moustache warm glint", fill=NONE, stroke=WARM,
       strokeWidth=4, opacity=55, cap="round")
# loose whisker hairs past the tips
for i, dd in enumerate(["M300,628 C284,644 274,656 262,662", "M312,618 C296,640 290,656 286,672",
                        "M684,654 C700,668 716,676 732,678", "M674,646 C688,664 696,680 700,696"]):
    d.path(dd, f"Stray hair {i+1}", fill=NONE, stroke="#FFFFFF", strokeWidth=3, opacity=70, cap="round")

# --- name -----------------------------------------------------------------------------------
d.text("EMPEROR TAMARIN", "Name", x=500, y=960, size=48, font="Virelai Sans",
       color="#E2EAC6", justify="center")

d.finish("emperor-tamarin-V1R00")
