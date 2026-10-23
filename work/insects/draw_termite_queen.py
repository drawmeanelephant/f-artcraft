#!/usr/bin/env python3
"""Termite queen — field-guide plate V1R00. The physogastric queen in profile
inside the royal cell: a huge banded abdomen whose dark tergite plates float on
stretched, translucent intersegmental membrane (eggs glowing through it), a
tiny head and thorax with wing stubs, small pale attendant workers feeding,
grooming and carrying eggs away. Vaulted clay chamber in pellet masonry.
Amber-dark plate. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math, re, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Termite Queen — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420
INK = "#2A160A"
FAR = []
random.seed(83)

def lin(angle, *stops):
    return {"gradient": {"kind": "linear", "angle": angle, "stops": [
        dict(offset=s[0], color=s[1], **({"opacity": s[2]} if len(s) > 2 else {})) for s in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial", "stops": [
        dict(offset=s[0], color=s[1], **({"opacity": s[2]} if len(s) > 2 else {})) for s in stops]}}

def chk(x, y, pad=24):
    if math.hypot(x - CX, y - CY) > R - pad:
        FAR.append((round(x), round(y)))

def cub(p0, p1, p2, p3, t):
    u = 1 - t
    x = u**3*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t**3*p3[0]
    y = u**3*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t**3*p3[1]
    return x, y

def lell(cx, cy, rx, ry, rot=0):
    k, a = 0.5523, math.radians(rot)
    ca, sa = math.cos(a), math.sin(a)
    def p(x, y):
        return "%.1f,%.1f" % (cx + x*ca - y*sa, cy + x*sa + y*ca)
    return (f"M{p(rx,0)} C{p(rx,ry*k)} {p(rx*k,ry)} {p(0,ry)} C{p(-rx*k,ry)} {p(-rx,ry*k)} {p(-rx,0)} "
            f"C{p(-rx,-ry*k)} {p(-rx*k,-ry)} {p(0,-ry)} C{p(rx*k,-ry)} {p(rx,-ry*k)} {p(rx,0)} Z")

def poly_d(pts, close=True):
    return "M" + " L".join("%.1f,%.1f" % p for p in pts) + (" Z" if close else "")

def inside(pt, poly):
    x, y = pt; c = False
    for i in range(len(poly)):
        x1, y1 = poly[i]; x2, y2 = poly[i - 1]
        if (y1 > y) != (y2 > y) and x < (x2 - x1)*(y - y1)/(y2 - y1) + x1:
            c = not c
    return c

_pair = re.compile(r"(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)")
def xf(dstr, f):
    return _pair.sub(lambda m: "%.1f,%.1f" % f(float(m.group(1)), float(m.group(2))), dstr)

# --- palette --------------------------------------------------------------------
BG = lin(90, (0, "#22160C"), (1, "#0C0804"))
PLATE = rad((0, "#8E5A2A"), (0.6, "#6A3E1C"), (1, "#3E220E"))
CHAMBER = rad((0, "#F0C27A"), (0.55, "#C88A44"), (1, "#7A4620"))
MEMBRANE = lin(90, (0, "#FAEED2", 0.92), (0.5, "#F0D8A6", 0.88), (1, "#C8945A", 0.92))
TERGITE = lin(90, (0, "#6A3A18", 0.96), (0.45, "#7E4A22", 0.82), (1, "#B07A40", 0.0))
STERNITE = lin(90, (0, "#B07A40", 0.0), (1, "#6A3A18", 0.8))
CHITIN = rad((0, "#A8642E"), (0.6, "#6E3A18"), (1, "#3E200C"))
LEG = lin(90, (0, "#B07A44"), (1, "#6A401C"))
W_BODY = rad((0, "#FFF6E2", 0.95), (0.7, "#F0DDB4", 0.9), (1, "#D8B880", 0.9))
W_HEAD = rad((0, "#F2C47A"), (1, "#C08038"))

# --- backdrop + plate (the clay mound) ------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG, stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876, fill="#8E5A2A", opacity=7, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840, fill=PLATE, stroke="#2E1A0A", strokeWidth=6)

CH = [[(172, 616), (136, 616), (124, 560), (132, 500)],
      [(132, 500), (148, 330), (305, 215), (500, 212)],
      [(500, 212), (695, 215), (852, 330), (868, 500)],
      [(868, 500), (876, 560), (864, 616), (828, 616)]]
ch_poly = []
for seg in CH:
    for k in range(30):
        ch_poly.append(cub(*seg, k/30))
ch_poly.append((828, 616))
for p in ch_poly:
    chk(*p)
CH_D = ("M172,616 C136,616 124,560 132,500 C148,330 305,215 500,212 "
        "C695,215 852,330 868,500 C876,560 864,616 828,616 Z")

# pellet masonry in the wall: only between the chamber and the rim
n = 0
for i in range(900):
    x, y = random.uniform(90, 910), random.uniform(50, 870)
    if math.hypot(x - CX, y - CY) > R - 16 or inside((x, y), ch_poly):
        continue
    near = min(math.hypot(x - px, y - py) for px, py in ch_poly[::3])
    if near < 12:
        continue
    n += 1
    w = random.uniform(9, 16)
    c = random.choice(["#A06A36", "#8A5428", "#5A3416", "#B47A40"])
    d.path(lell(x, y, w/2, w/2.6, random.uniform(-40, 40)), f"Clay pellet {n}",
           fill=rad((0, c), (1, "#3A200C")), opacity=random.randint(30, 55), stroke=NONE)
    if n >= 170:
        break
# ventilation tunnels opening into the wall
for i, (x, y, rx, ry) in enumerate([(240, 180, 22, 14), (790, 200, 18, 12), (170, 720, 16, 11),
                                     (830, 700, 20, 13), (500, 800, 24, 12)]):
    chk(x, y, rx + 18)
    d.path(lell(x, y, rx, ry), f"Tunnel {i+1}", fill=rad((0, "#0C0602"), (1, "#3A200C")), stroke="#2A160A",
           strokeWidth=2, opacity=85)
    d.path(f"M{x-rx+3},{y-ry*0.4:.1f} C{x-rx/2},{y-ry-3} {x+rx/2},{y-ry-3} {x+rx-3},{y-ry*0.4:.1f}",
           f"Tunnel {i+1} lip", fill=NONE, stroke="#C8904E", strokeWidth=3, opacity=45, cap="round")

d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8B878", strokeWidth=3, opacity=35)

# --- the royal cell ---------------------------------------------------------------------
d.path(CH_D, "Royal cell", fill=CHAMBER, stroke=INK, strokeWidth=6)
d.path("M148,470 C172,330 314,232 500,228 C686,232 828,330 852,470", "Vault lip light", fill=NONE,
       stroke="#FFE2A8", strokeWidth=4, opacity=35, cap="round")
d.path("M140,520 C154,360 304,250 500,246 C696,250 846,360 860,520", "Vault shade", fill=NONE,
       stroke="#5A3216", strokeWidth=10, opacity=18, cap="round")
for i in range(26):
    x, y = random.uniform(160, 840), random.uniform(250, 590)
    if inside((x, y), ch_poly) and not (260 < x < 860 and 300 < y < 620):
        d.path(lell(x, y, 6, 4, random.uniform(-30, 30)), f"Cell wall texture {i+1}",
               fill="#7A4620", opacity=22, stroke=NONE)
d.path("M180,610 C320,602 680,602 820,610 C680,606 320,606 180,610 Z", "Floor light",
       fill="#FFE0A0", opacity=40, stroke=NONE)

# --- the queen ---------------------------------------------------------------------------
ACX, ACY, AA, AB, NE = 562, 462, 270, 150, 2.2
def _u(x):
    return min(max((x - (ACX - AA)) / (2*AA), 0), 1)
def _sc(u):
    t = min(u/0.55, 1)
    return 0.7 + 0.3*(3*t*t - 2*t*t*t)        # narrow where it meets the thorax
def _yc(u):
    return ACY + 12*math.sin(math.pi*u) + (1 - _sc(u))*AB*0.55   # sag + front tucked low
def _hh(x):
    u = _u(x)
    q = min(abs(x - ACX)/AA, 1)
    return _sc(u)*AB*(1 - q**NE)**(1/NE)
def y_top(x):
    return _yc(_u(x)) - _hh(x)
def y_bot(x):
    return _yc(_u(x)) + _hh(x)
abd = []
for k in range(160):
    t = 2*math.pi*k/160
    c = math.cos(t)
    x = ACX + AA*math.copysign(abs(c)**(2/NE), c)
    abd.append((x, y_bot(x) if math.sin(t) > 0 else y_top(x)))
for p in abd:
    chk(*p)
d.path(lell(570, 618, 300, 14), "Queen floor shadow", fill="#3A1E0A", opacity=35, stroke=NONE)

# far-side legs first
def qleg(name, base, knee, foot, fill, sw):
    d.path(f"M{base[0]},{base[1]} L{knee[0]},{knee[1]}", f"{name} femur", fill=NONE, stroke=fill,
           strokeWidth=9, cap="round")
    d.path(f"M{knee[0]},{knee[1]} L{foot[0]},{foot[1]}", f"{name} tibia", fill=NONE, stroke=fill,
           strokeWidth=6, cap="round")
    d.path(f"M{foot[0]},{foot[1]} L{foot[0]-10},{foot[1]+1}", f"{name} tarsus", fill=NONE, stroke="#5A3416",
           strokeWidth=4, cap="round")
for nm, b, k, f in [("Far foreleg", (232, 548), (206, 574), (192, 612)),
                    ("Far midleg", (254, 552), (272, 582), (266, 612)),
                    ("Far hindleg", (274, 550), (306, 578), (322, 612))]:
    qleg(nm, b, k, f, "#5A3416", 9)

d.path(poly_d(abd), "Abdomen membrane", fill=MEMBRANE, stroke="#7A4A22", strokeWidth=4)
# what shows through the membrane: ovarioles packed with eggs, the gut
for i in range(46):
    x = random.uniform(ACX - AA + 50, ACX + AA - 40)
    y = random.uniform(y_top(x) + 40, y_bot(x) - 30)
    d.path(lell(x, y, random.uniform(7, 11), random.uniform(4, 6), random.uniform(-25, 25)), f"Egg within {i+1}",
           fill="#FFFFFF", opacity=random.randint(14, 26), stroke=NONE)
d.path(f"M{ACX-AA+40},{ACY+10} C{ACX-120},{ACY-20} {ACX+60},{ACY+40} {ACX+AA-30},{ACY+6}", "Gut shadow",
       fill=NONE, stroke="#A06A34", strokeWidth=16, opacity=18, cap="round")
# glow at the stretched seams
d.path(lell(ACX - 20, ACY - 30, AA*0.75, AB*0.45), "Membrane glow", fill="#FFFAE8", opacity=24, stroke=NONE)

# tergites (top) and sternites (bottom): dark plates adrift on the membrane
xs = [312 + i*50 for i in range(11)]
# intersegmental folds: faint bands running the full depth between plates
for i, x0 in enumerate(xs[1:]):
    xm = x0 - 6
    pts = [(xm + 3*math.sin(math.pi*k/12), y_top(xm) + 6 + (y_bot(xm) - y_top(xm) - 12)*k/12) for k in range(13)]
    d.path(poly_d(pts, False), f"Segment fold {i+1}", fill=NONE, stroke="#B07A40", strokeWidth=3,
           opacity=22, cap="round")
BAND = lin(90, (0, "#5E3416", 0.96), (0.28, "#8A5428", 0.70), (0.55, "#C8945A", 0.10),
           (0.8, "#9A6030", 0.40), (1, "#5E3416", 0.80))
for i, x0 in enumerate(xs):
    w = 38 if x0 + 38 < ACX + AA - 30 else 30
    x1 = x0 + w
    N = 12
    top = [(x, y_top(x) + 1.5) for x in [x0 + w*k/N for k in range(N + 1)]]
    rs = [(x1 + 3*math.sin(math.pi*k/N), y_top(x1) + (y_bot(x1) - y_top(x1))*k/N) for k in range(1, N)]
    bot = [(x, y_bot(x) - 1.5) for x in [x1 - w*k/N for k in range(N + 1)]]
    ls = [(x0 + 3*math.sin(math.pi*k/N), y_bot(x0) - (y_bot(x0) - y_top(x0))*k/N) for k in range(1, N)]
    d.path(poly_d(top + rs + bot + ls), f"Segment band {i+1}", fill=BAND, stroke=NONE)
    d.path(poly_d(top, False), f"Tergite {i+1} edge", fill=NONE, stroke=INK, strokeWidth=3, cap="round")
    d.path(poly_d(top[2:11], False), f"Tergite {i+1} light", fill=NONE, stroke="#E8B070", strokeWidth=3,
           opacity=50, cap="round")
    xm = x0 + w/2
    d.path(lell(xm, (y_top(xm) + y_bot(xm))/2 - 4, 3.5, 3.5), f"Spiracle {i+1}", fill="#5A3216",
           opacity=60, stroke=NONE)

def _sq(s):
    return max(math.sin(math.pi*s), 0) ** 0.3       # flat-bottomed band, rounded corners
d.path(f"M{ACX-AA+30},{ACY-AB*0.62} C{ACX-120},{ACY-AB-6} {ACX+140},{ACY-AB-6} {ACX+AA-50},{ACY-AB*0.6}",
       "Abdomen top sheen", fill=NONE, stroke="#FFFFFF", strokeWidth=6, opacity=28, cap="round")
d.path(f"M{ACX-AA+50},{ACY+AB*0.7} C{ACX-100},{ACY+AB+4} {ACX+120},{ACY+AB+4} {ACX+AA-60},{ACY+AB*0.68}",
       "Abdomen belly shade", fill=NONE, stroke="#6A3A18", strokeWidth=10, opacity=22, cap="round")
d.path(f"M{ACX+AA-8},{ACY-6} C{ACX+AA+6},{ACY} {ACX+AA+6},{ACY+10} {ACX+AA-6},{ACY+16}", "Cerci",
       fill=NONE, stroke="#6A3A18", strokeWidth=4, cap="round")

# thorax with wing stubs, tiny head
d.path("M286,500 C300,488 302,560 286,566 L262,566 C254,550 256,510 262,500 Z", "Metathorax",
       fill=CHITIN, stroke=INK, strokeWidth=3)
d.path("M244,504 C258,496 268,500 268,512 L268,556 C266,564 254,566 244,562 C238,544 238,520 244,504 Z",
       "Mesothorax", fill=CHITIN, stroke=INK, strokeWidth=3)
for i, (bx, by) in enumerate([(254, 500), (276, 496)]):
    d.path(f"M{bx-8},{by+2} L{bx+30},{by-12} L{bx+8},{by+6} Z", f"Wing stub {i+1}",
           fill=lin(0, (0, "#8A5A2C", 0.9), (1, "#C89A5E", 0.6)), stroke=INK, strokeWidth=2, join="round")
d.path("M214,506 C226,496 244,498 248,508 L248,556 C244,566 226,566 216,560 C210,544 210,520 214,506 Z",
       "Pronotum", fill=CHITIN, stroke=INK, strokeWidth=3)
d.path("M218,508 C228,502 240,502 246,510", "Pronotum light", fill=NONE, stroke="#E8B070",
       strokeWidth=3, opacity=50, cap="round")
d.path(lell(194, 530, 25, 22, -10), "Head", fill=CHITIN, stroke=INK, strokeWidth=3)
d.path(lell(186, 520, 10, 6, -20), "Head sheen", fill="#F0C080", opacity=30, stroke=NONE)
d.path(lell(196, 524, 6, 7), "Compound eye", fill=rad((0, "#4A4A3A"), (1, "#100C08")), stroke=INK, strokeWidth=1.5)
d.path(lell(194.5, 522, 1.8, 1.8), "Eye glint", fill="#FFFFFF", opacity=80, stroke=NONE)
d.path("M172,540 L160,548 L170,550 Z", "Mandible", fill="#3A200C", stroke=INK, strokeWidth=1.5)
for nm, c, col in [("Far antenna", [(182, 512), (170, 494), (150, 488), (136, 498)], "#5A3416"),
                   ("Antenna", [(178, 516), (160, 500), (140, 504), (130, 520)], "#7A4A22")]:
    d.path("M%d,%d C%d,%d %d,%d %d,%d" % (*c[0], *c[1], *c[2], *c[3]), nm, fill=NONE, stroke=col,
           strokeWidth=5, cap="round")
    d.path("M%d,%d C%d,%d %d,%d %d,%d" % (*c[0], *c[1], *c[2], *c[3]), nm + " beads", fill=NONE,
           stroke="#E0B070", strokeWidth=3, dash=[3, 4], opacity=55)
    for k in range(9):
        chk(*cub(*c, k/8))
for nm, b, k, f in [("Foreleg", (226, 556), (200, 580), (180, 612)),
                    ("Midleg", (248, 560), (262, 588), (252, 612)),
                    ("Hindleg", (270, 560), (296, 586), (306, 612))]:
    qleg(nm, b, k, f, LEG, 9)

# --- eggs, under the tail ---------------------------------------------------------------
for i, (x, y) in enumerate([(744, 604), (762, 606), (780, 604), (752, 592), (770, 592), (761, 580),
                            (796, 604), (788, 592)]):
    d.path(lell(x, y, 9, 6, -10), f"Egg {i+1}", fill=rad((0, "#FFFFFF"), (1, "#E8D6B0")), stroke="#8A6034",
           strokeWidth=1.5)

# --- attendant workers ---------------------------------------------------------------------
WORKER = [
    ("abdomen", lell(-14, 0, 24, 12), W_BODY, 2),
    ("gut", lell(-12, 1, 14, 5), None, 0),
    ("thorax", lell(10, -1, 9, 8), W_BODY, 2),
    ("head", lell(28, -2, 11, 10), W_HEAD, 2),
]
def worker(name, x, y, ang, s=1.0, flip=False, carry=False):
    a = math.radians(ang); ca, sa = math.cos(a), math.sin(a)
    fx = -1 if flip else 1
    def f(px, py):
        px *= s * fx; py *= s
        X, Y = px*ca - py*sa + x, px*sa + py*ca + y
        chk(X, Y, 20)
        return X, Y
    for k, (lx, ly) in enumerate([(4, 6), (10, 7), (16, 6)]):
        feet = [(-6, 19), (8, 20), (26, 19)][k]
        kn = [(-2, 12), (12, 14), (22, 12)][k]
        d.path(xf(f"M{lx},{ly} L{kn[0]},{kn[1]} L{feet[0]},{feet[1]}", f), f"{name} leg {k+1}", fill=NONE,
               stroke="#C89458", strokeWidth=3, cap="round", join="round")
    for part, pd, fill, sw in WORKER:
        if fill is None:
            d.path(xf(pd, f), f"{name} {part}", fill="#8A5A2C", opacity=30, stroke=NONE)
        else:
            d.path(xf(pd, f), f"{name} {part}", fill=fill, stroke="#7A4A22", strokeWidth=sw)
    for k, bx in enumerate([-26, -18, -10, -2]):
        d.path(xf(f"M{bx},-10 C{bx+2},-3 {bx+2},3 {bx},10", f), f"{name} band {k+1}", fill=NONE,
               stroke="#B08048", strokeWidth=2, opacity=55, cap="round")
    d.path(xf("M34,-9 C42,-18 52,-16 58,-8", f), f"{name} antenna", fill=NONE, stroke="#C89458",
           strokeWidth=3, cap="round")
    d.path(xf("M37,3 L44,6 L38,8 Z", f), f"{name} mandible", fill="#7A4A1C", stroke=NONE)
    d.path(xf(lell(24, -6, 4, 2.5), f), f"{name} head sheen", fill="#FFFFFF", opacity=45, stroke=NONE)
    if carry:
        d.path(xf(lell(48, 4, 9, 6), f), f"{name} carried egg", fill=rad((0, "#FFFFFF"), (1, "#E8D6B0")),
               stroke="#8A6034", strokeWidth=1.5)

worker("Worker feeding", 166, 594, -30, 0.9)
worker("Worker under belly", 420, 600, 0, 0.95, flip=True)
worker("Worker on back L", 470, y_top(470) - 16, math.degrees(math.atan2(y_top(490) - y_top(450), 40)), 0.9, flip=True)
worker("Worker on back R", 664, y_top(664) - 16, math.degrees(math.atan2(y_top(684) - y_top(644), 40)), 0.9)
worker("Worker grooming flank", 600, 520, -24, 0.95)
worker("Worker carrying egg", 676, 600, 0, 0.95, carry=True)

if FAR:
    print("WARN points near the rim:", FAR[:12])

d.text("TERMITE QUEEN", "Name", x=500, y=940, size=56, font="Virelai Sans", color="#F0D8B0", justify="center")
d.text("B L A T T O D E A", "Order", x=500, y=978, size=24, font="Virelai Sans", color="#C09A6A", justify="center")

d.finish("termite-queen-V1R00")
