#!/usr/bin/env python3
"""Stag beetle — field plate V1R00. Side view facing right, mandibles open like
antlers, glossy black-brown carapace with a warm amber edge highlight, heavy
legs gripping an oak branch; dark oak plate. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Stag Beetle — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420
INK = "#1F130C"

def lin(angle, *stops):
    return {"gradient": {"kind": "linear", "angle": angle, "stops": [
        {"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial", "stops": [
        {"offset": o, "color": c} for o, c in stops]}}

def disc_pt(deg, r=R):
    a = math.radians(deg)
    return (CX + r * math.cos(a), CY + r * math.sin(a))

def cubic(p, t):
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = p
    mt = 1 - t
    x = mt**3*x0 + 3*mt*mt*t*x1 + 3*mt*t*t*x2 + t**3*x3
    y = mt**3*y0 + 3*mt*mt*t*y1 + 3*mt*t*t*y2 + t**3*y3
    tx = 3*mt*mt*(x1-x0) + 6*mt*t*(x2-x1) + 3*t*t*(x3-x2)
    ty = 3*mt*mt*(y1-y0) + 6*mt*t*(y2-y1) + 3*t*t*(y3-y2)
    return x, y, tx, ty

def frame(p, t):
    x, y, tx, ty = cubic(p, t)
    ln = math.hypot(tx, ty) or 1
    return x, y, tx / ln, ty / ln, -ty / ln, tx / ln

def ribbon(p, widths, n=32):
    left, right = [], []
    k = len(widths) - 1
    for i in range(n + 1):
        t = i / n
        x, y, ux, uy, nx, ny = frame(p, t)
        s = t * k; j = min(int(s), k - 1); f = s - j
        w = (widths[j] * (1 - f) + widths[j + 1] * f) / 2
        left.append((x + nx * w, y + ny * w))
        right.append((x - nx * w, y - ny * w))
    pts = left + right[::-1]
    return f"M{pts[0][0]:.1f},{pts[0][1]:.1f} " + " ".join(
        f"L{x:.1f},{y:.1f}" for x, y in pts[1:]) + " Z"

def polyline(pts):
    return f"M{pts[0][0]},{pts[0][1]} " + " ".join(f"L{x},{y}" for x, y in pts[1:])

def oak_leaf(x0, y0, ang, L, W, lobes=4):
    """Lobed oak-leaf outline along an axis from (x0,y0) at angle ang."""
    ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    side = []
    n = 48
    for i in range(n + 1):
        t = i / n
        w = W * (math.sin(math.pi * t) ** 0.7) * (0.72 + 0.28 * math.cos(lobes * 2 * math.pi * t))
        side.append((t * L, w))
    pts = [(u, v) for u, v in side] + [(u, -v) for u, v in side[::-1]]
    xy = [(x0 + u * ca - v * sa, y0 + u * sa + v * ca) for u, v in pts]
    return f"M{xy[0][0]:.1f},{xy[0][1]:.1f} " + " ".join(f"L{x:.1f},{y:.1f}" for x, y in xy[1:]) + " Z"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin(-90, (0, "#21160D"), (1, "#0A0604")), stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#C9A47C"), (0.6, "#94693F"), (1, "#5A3B21")),
        stroke="#3E2814", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8CFA8", strokeWidth=3, opacity=45)
# oak grain: faint concentric rings on the plate
for i, (w, h, op) in enumerate([(640, 520, 14), (520, 400, 12), (400, 300, 12), (280, 200, 10)]):
    d.shape("ellipse", f"Grain ring {i+1}", x=500 - w / 2 + 40, y=380 - h / 2, width=w, height=h,
            fill=NONE, stroke="#5A3B21", strokeWidth=3, opacity=op)
# faint oak leaves behind the animal
for i, (x, y, ang, L, W, op) in enumerate([(150, 330, -38, 220, 52, 26), (190, 450, -12, 170, 40, 20),
                                           (640, 130, 24, 190, 44, 20)]):
    d.path(oak_leaf(x, y, ang, L, W), f"Oak leaf {i+1}",
           fill=lin(0, (0, "#6E4C28"), (1, "#4A3018")), stroke=NONE, opacity=op)
d.path("M150,330 L323,195", "Oak leaf 1 midrib", fill=NONE, stroke="#3A2410",
       strokeWidth=3, opacity=22, cap="round")

# --- oak branch the beetle grips (closes on the disc arc) ---------------------------
a0, a1 = disc_pt(150), disc_pt(30)
d.path(f"M{a0[0]:.1f},{a0[1]:.1f} C300,694 650,694 {a1[0]:.1f},{a1[1]:.1f} "
       f"A420,420 0 0 1 {a0[0]:.1f},{a0[1]:.1f} Z", "Oak branch",
       fill=lin(-90, (0, "#7A5E46"), (0.3, "#5A4232"), (1, "#2E2018")),
       stroke="#1E140C", strokeWidth=5)
d.path(f"M{a0[0]+8:.0f},{a0[1]+6:.0f} C300,700 650,700 {a1[0]-8:.0f},{a1[1]+6:.0f}",
       "Branch top light", fill=NONE, stroke="#C8A27C", strokeWidth=5, opacity=40, cap="round")
for i, (x0, y0, x1, y1, c1) in enumerate([(160, 712, 360, 730, 742), (380, 740, 600, 738, 752),
                                          (620, 730, 820, 706, 734), (200, 760, 420, 790, 792),
                                          (440, 800, 680, 790, 808), (680, 768, 820, 740, 770),
                                          (300, 830, 520, 852, 856), (540, 850, 700, 826, 846)]):
    d.path(f"M{x0},{y0} Q{(x0+x1)/2},{c1} {x1},{y1}", f"Bark furrow {i+1}",
           fill=NONE, stroke="#1A100A", strokeWidth=5, opacity=45, cap="round")
    d.path(f"M{x0+10},{y0-6} Q{(x0+x1)/2},{c1-6} {x1-10},{y1-6}", f"Bark ridge light {i+1}",
           fill=NONE, stroke="#B89474", strokeWidth=3, opacity=25, cap="round")
for i, (x, y, w, h) in enumerate([(210, 720, 60, 22), (760, 712, 50, 18), (520, 770, 44, 16)]):
    d.shape("ellipse", f"Lichen {i+1}", x=x, y=y, width=w, height=h,
            fill=rad((0, "#C8D29A"), (1, "#7E8A58")), opacity=55, stroke=NONE)
# an acorn resting on the branch
d.shape("ellipse", "Acorn nut", x=178, y=640, width=40, height=50,
        fill=rad((0, "#E0B070"), (0.6, "#B07A3A"), (1, "#6E4620")), stroke=INK, strokeWidth=3)
d.path("M174,656 C176,634 220,634 222,656 C206,664 190,664 174,656 Z", "Acorn cup",
       fill=lin(-90, (0, "#8A6A44"), (1, "#4E3820")), stroke=INK, strokeWidth=3)
d.path("M198,636 L200,624", "Acorn stalk", fill=NONE, stroke=INK, strokeWidth=4, cap="round")
d.path("M186,668 C188,678 194,684 200,686", "Acorn sheen", fill=NONE,
       stroke="#FFE2B0", strokeWidth=3, opacity=60, cap="round")
d.shape("ellipse", "Beetle shadow", x=250, y=676, width=520, height=26,
        fill="#120A06", opacity=35, stroke=NONE)

# everything drawn from here on is the beetle; collect it so it can be nudged
BEETLE = []
_call = d.call
def _capture(tool, args, label):
    r = _call(tool, args, label)
    if tool in ("draw_path", "draw_shape") and isinstance(r, dict) and "id" in r:
        BEETLE.append(r["id"])
    return r
d.call = _capture

# --- legs ---------------------------------------------------------------------------
LEG = "#3A2418"
def leg(name, coxa, knee, ankle, grip, far=False):
    col = "#1E120A" if far else LEG
    op = 90 if far else 100
    fx, fy = coxa; kx, ky = knee
    d.path(ribbon(((fx, fy), (fx + (kx-fx)/3, fy + (ky-fy)/3),
                   (fx + 2*(kx-fx)/3, fy + 2*(ky-fy)/3), (kx, ky)), [16, 24, 14]),
           f"{name} femur", fill=lin(90, (0, col), (1, "#6A4630" if not far else "#2E1E14")),
           stroke=INK, strokeWidth=3, opacity=op)
    # heavy, flattened tibia with outer spines
    ax, ay = ankle
    tib = ((kx, ky), (kx + (ax-kx)/3, ky + (ay-ky)/3), (kx + 2*(ax-kx)/3, ky + 2*(ay-ky)/3), (ax, ay))
    d.path(ribbon(tib, [12, 14, 16]), f"{name} tibia",
           fill=lin(0, (0, "#5A3A26" if not far else "#24160E"), (1, col)),
           stroke=INK, strokeWidth=3, opacity=op)
    for j, t in enumerate([0.4, 0.7, 0.95]):
        x, y, ux, uy, nx, ny = frame(tib, t)
        sgn = 1 if (nx * (ax - kx) - 0) >= 0 else -1
        d.path(f"M{x+nx*7:.0f},{y+ny*7:.0f} L{x+nx*15+ux*5:.0f},{y+ny*15+uy*5:.0f}",
               f"{name} spine {j+1}", fill=NONE, stroke=INK, strokeWidth=3.5,
               cap="round", opacity=op)
    # tarsus bends over the bark, ending in hooked claws
    gx, gy = grip
    d.path(f"M{ax},{ay} Q{(ax+gx)/2},{min(ay,gy)-6} {gx},{gy}", f"{name} tarsus ink",
           fill=NONE, stroke=INK, strokeWidth=10, cap="round", opacity=op)
    d.path(f"M{ax},{ay} Q{(ax+gx)/2},{min(ay,gy)-6} {gx},{gy}", f"{name} tarsus",
           fill=NONE, stroke="#5A3A26" if not far else col, strokeWidth=6, cap="round", opacity=op)
    for j, t in enumerate([0.3, 0.55, 0.8]):
        x = (1-t)**2*ax + 2*(1-t)*t*(ax+gx)/2 + t*t*gx
        y = (1-t)**2*ay + 2*(1-t)*t*(min(ay,gy)-6) + t*t*gy
        d.shape("ellipse", f"{name} tarsal joint {j+1}", x=x-3, y=y-3, width=6, height=6,
                fill=INK, opacity=op * 0.7, stroke=NONE)
    dirx = 1 if gx >= ax else -1
    d.path(f"M{gx},{gy} Q{gx+dirx*9},{gy} {gx+dirx*8},{gy+9}", f"{name} claw",
           fill=NONE, stroke=INK, strokeWidth=3.5, cap="round", opacity=op)
    if not far:
        d.path(polyline([(fx + (kx-fx)*0.2, fy + (ky-fy)*0.2 - 4), (fx + (kx-fx)*0.8, fy + (ky-fy)*0.8 - 4)]),
               f"{name} femur rim light", fill=NONE, stroke="#E8A868", strokeWidth=3,
               opacity=55, cap="round")

leg("Far fore leg", (628, 566), (694, 590), (726, 660), (756, 678), far=True)
leg("Far mid leg", (520, 598), (548, 630), (552, 674), (580, 684), far=True)
leg("Far hind leg", (410, 600), (372, 626), (360, 672), (336, 682), far=True)

# --- far mandible (behind the head) ---------------------------------------------------
MAND = lin(0, (0, "#8A4A26"), (0.55, "#5E2E16"), (1, "#2E160A"))
# the open jaws read as a pincer: far mandible arcs up and over, near one
# swings out and under, tips curling toward each other
far_m = ((718, 500), (782, 418), (880, 388), (900, 452))
d.path(ribbon(far_m, [30, 24, 16, 6]), "Far mandible", fill=lin(0, (0, "#5A2E16"), (1, "#24120A")),
       stroke=INK, strokeWidth=4)
for j, (t, L) in enumerate([(0.45, 26), (0.97, 16)]):
    x, y, ux, uy, nx, ny = frame(far_m, t)
    w = 11 if t < 0.9 else 3
    d.path(f"M{x+nx*w-ux*6:.0f},{y+ny*w-uy*6:.0f} L{x+nx*(w+L):.0f},{y+ny*(w+L):.0f} "
           f"L{x+nx*w+ux*6:.0f},{y+ny*w+uy*6:.0f} Z", f"Far mandible tine {j+1}",
           fill="#3A1C0E", stroke=INK, strokeWidth=3)

# --- body --------------------------------------------------------------------------------
d.path("M282,580 C300,624 380,636 450,634 C520,632 572,618 596,580 Z", "Abdomen underside",
       fill=lin(-90, (0, "#2E1C12"), (1, "#120A06")), stroke=INK, strokeWidth=4)
ELY = rad((0, "#5E3620"), (0.5, "#30190C"), (1, "#120804"))
d.path("M264,548 C262,492 320,458 410,454 C490,452 552,468 572,504 "
       "C584,536 576,580 548,600 C506,628 336,628 294,602 C276,588 266,570 264,548 Z",
       "Elytra", fill=ELY, stroke=INK, strokeWidth=6)
d.path("M276,520 C296,478 360,462 420,462 C480,462 534,472 560,500", "Elytra rim light",
       fill=NONE, stroke="#F0A860", strokeWidth=5, opacity=60, cap="round")
d.path("M300,500 C330,478 380,472 430,472", "Elytra specular", fill=NONE,
       stroke="#FFE4C0", strokeWidth=4, opacity=70, cap="round")
d.shape("ellipse", "Elytra gloss", x=320, y=470, width=200, height=56,
        fill="#E8B888", opacity=16, stroke=NONE)
d.path("M280,566 C320,600 420,612 520,598", "Elytra lower edge", fill=NONE,
       stroke="#8A4E2A", strokeWidth=4, opacity=45, cap="round")
d.path("M290,586 C340,612 450,618 540,602", "Elytra belly shade", fill=NONE,
       stroke="#000000", strokeWidth=10, opacity=22, cap="round")

# pronotum
d.path("M556,486 C586,466 640,468 656,494 C668,522 656,562 622,574 "
       "C592,582 562,568 556,540 C552,522 552,500 556,486 Z", "Pronotum",
       fill=rad((0, "#5E3820"), (0.55, "#331C0E"), (1, "#140A04")), stroke=INK, strokeWidth=5)
d.path("M566,494 C590,478 628,476 648,496", "Pronotum rim light", fill=NONE,
       stroke="#F0A860", strokeWidth=4, opacity=65, cap="round")
d.path("M576,500 C590,492 606,490 620,492", "Pronotum specular", fill=NONE,
       stroke="#FFE4C0", strokeWidth=3, opacity=70, cap="round")

# near mandible: the antler, sweeping up and curling back
near_m = ((710, 520), (800, 594), (900, 576), (906, 480))
d.path(ribbon(near_m, [36, 28, 18, 6]), "Near mandible", fill=MAND, stroke=INK, strokeWidth=5)
for j, (t, L) in enumerate([(0.45, 32), (0.68, 14), (0.98, 12)]):
    x, y, ux, uy, nx, ny = frame(near_m, t)
    nx, ny = -nx, -ny
    w = (36 - t * 30) / 2
    d.path(f"M{x+nx*w-ux*7:.0f},{y+ny*w-uy*7:.0f} L{x+nx*(w+L)+ux*4:.0f},{y+ny*(w+L)+uy*4:.0f} "
           f"L{x+nx*w+ux*7:.0f},{y+ny*w+uy*7:.0f} Z", f"Near mandible tine {j+1}",
           fill="#6E3418", stroke=INK, strokeWidth=3)
d.path("M736,550 C800,600 890,582 896,514", "Near mandible rim light", fill=NONE,
       stroke="#F6B878", strokeWidth=5, opacity=60, cap="round")
d.path("M744,534 C788,568 836,574 872,562", "Near mandible specular", fill=NONE,
       stroke="#FFFFFF", strokeWidth=3, opacity=55, cap="round")
d.path("M730,484 C784,420 860,396 892,424", "Far mandible rim light", fill=NONE,
       stroke="#E8A060", strokeWidth=4, opacity=45, cap="round")

# broad head (over the mandible roots)
d.path("M640,500 C660,474 714,470 734,494 C750,514 744,548 716,560 "
       "C688,570 654,558 644,536 C638,524 636,512 640,500 Z", "Head",
       fill=rad((0, "#64402A"), (0.55, "#381E10"), (1, "#160A04")), stroke=INK, strokeWidth=5)
d.path("M652,494 C670,478 706,476 726,494", "Head rim light", fill=NONE,
       stroke="#F0A860", strokeWidth=4, opacity=65, cap="round")
d.shape("ellipse", "Eye", x=690, y=500, width=15, height=14,
        fill=rad((0, "#6A4A3A"), (1, "#1A0E08")), stroke=INK, strokeWidth=2)
d.shape("ellipse", "Eye glint", x=694, y=503, width=4, height=4, fill="#FFFFFF", opacity=85, stroke=NONE)
d.path("M690,520 L716,530", "Canthus ridge", fill=NONE, stroke="#1A0E08", strokeWidth=3,
       opacity=50, cap="round")

# elbowed antenna with a comb club
d.path("M704,552 L728,596", "Antenna scape", fill=NONE, stroke=INK, strokeWidth=4.5, cap="round")
d.path("M728,596 C740,600 752,600 762,596", "Antenna funicle", fill=NONE, stroke=INK,
       strokeWidth=3.5, cap="round")
for j, (x, y) in enumerate([(758, 596), (766, 594), (774, 591)]):
    d.path(f"M{x},{y} L{x+6},{y+12}", f"Antenna lamella {j+1}", fill=NONE,
           stroke="#6E3E20", strokeWidth=4, cap="round")

# --- near legs ---------------------------------------------------------------------------
leg("Hind leg", (392, 606), (330, 632), (312, 674), (282, 684))
leg("Mid leg", (502, 606), (462, 636), (476, 676), (506, 688))
leg("Fore leg", (610, 568), (668, 600), (692, 664), (724, 682))

d.call = _call
d.call("transform", {"ids": BEETLE, "dx": -38}, "shift beetle left")

# --- caption --------------------------------------------------------------------------
d.text("STAG BEETLE", "Name", x=500, y=940, size=56, font="Virelai Sans",
       color="#EED8B8", justify="center")
o = d.text("COLEOPTERA", "Order", x=500, y=975, size=22, font="Virelai Sans",
           color="#C0A07C", justify="center")
if o and "id" in o:
    d.cmd("text.setStyle", "Order tracking", ids=[o["id"]], tracking=400)

d.finish("stag-beetle-V1R00")
