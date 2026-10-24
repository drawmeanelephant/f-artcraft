#!/usr/bin/env python3
"""Star-nosed mole — field plate V1R00. Twenty-two pink rays reading the dark
faster than any eye. Loam plate, touch-first mood: the mole sits head-on in
its burrow, the star held out front, two palmate paws planted on the loam
floor while root threads let down from the burrow ceiling. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Star-Nosed Mole — Field Plate", 1000, 1000)
rng = random.Random(73)

CX, CY, R = 500, 460, 420          # plate disc centre + radius
INK = "#160D08"                    # warm dark ink, never pure black

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

def on_disc(x, y, pad=0, r=R):
    return math.hypot(x - CX, y - CY) <= r - pad

def polar(cx, cy, r, a):
    """a in degrees, 0 = up, positive clockwise."""
    t = math.radians(a)
    return (cx + r * math.sin(t), cy - r * math.cos(t))

BG_GRAD    = lin(0, 0, 0, 1000, (0, "#0E0A06"), (1, "#050302"))
PLATE_GRAD = rad((0, "#6B5238"), (0.55, "#3E2E1E"), (1, "#181009"))
FUR_GRAD   = rad((0, "#4A3A2E"), (0.55, "#2E221A"), (1, "#150D08"))
FLOOR_GRAD = lin(0, 760, 0, 880, (0, "#4E3A26"), (1, "#1C120A"))
PAW_GRAD   = lin(0, 640, 0, 800, (0, "#C9A08C"), (1, "#7A5442"))

# --- backdrop + loam plate ---------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=64, y=24, width=872, height=872,
        fill="#6B5238", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#20150C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C9AE84", strokeWidth=3, opacity=28)

# a dim shaft finding the burrow face, fading before the rim
d.shape("ellipse", "Burrow light", x=330, y=150, width=340, height=240,
        fill=rad((0, "#D8C098", 16), (0.6, "#D8C098", 7), (1, "#D8C098", 0)), stroke=NONE)
# loam motes on the plate
for i in range(26):
    a = rng.uniform(0, math.tau); rr = math.sqrt(rng.uniform(0, 1)) * 375
    x, y = CX + rr * math.cos(a), CY + rr * math.sin(a)
    w = rng.uniform(3, 8)
    d.shape("ellipse", f"Loam mote {i+1}", x=x - w/2, y=y - w/2, width=w, height=w,
            fill="#8A6B48", opacity=rng.uniform(14, 30), stroke=NONE)

# --- burrow ceiling: root threads letting down from the upper rim -------------
for i, (x0, y0, cx1, cy1, x1, y1, w_) in enumerate([
        (rim_x(128, side=-1), 128, 210, 190, 226, 268, 5),
        (rim_x(96,  side=-1)+30, 96, 300, 150, 288, 210, 4),
        (rim_x(150, side=-1)+8, 150, 255, 210, 240, 236, 3),
        (rim_x(120, side=1), 120, 760, 180, 742, 252, 5),
        (rim_x(88,  side=1)-34, 88, 700, 140, 716, 196, 4),
        (rim_x(170, side=1)-12, 170, 790, 236, 778, 300, 3)]):
    assert on_disc(x0, y0, -10) and on_disc(x1, y1, 10), (x0, y0, x1, y1)
    d.path(f"M{x0:.1f},{y0:.1f} C{cx1},{cy1} {cx1},{cy1+30} {x1},{y1}",
           f"Root {i+1}", fill=NONE, stroke="#3E2C1A", strokeWidth=w_,
           opacity=80, cap="round")
    # hairlets off each root
    hx, hy = x0 + (x1 - x0) * 0.55, y0 + (y1 - y0) * 0.55
    d.path(f"M{hx:.0f},{hy:.0f} L{hx + (10 if x0 < CX else -10):.0f},{hy + 12:.0f}",
           f"Rootlet {i+1}", fill=NONE, stroke="#3E2C1A", strokeWidth=2,
           opacity=55, cap="round")

# --- the mole: a dome of dark velvet, star held out front ----------------------
d.path("M500,346 C606,346 668,440 676,560 C682,652 640,724 566,756 "
       "C544,766 522,770 500,770 C478,770 456,766 434,756 "
       "C360,724 318,652 324,560 C332,440 394,346 500,346 Z",
       "Fur dome", fill=FUR_GRAD, stroke=INK, strokeWidth=5)
# crown light + velvet shading strokes along the dome
d.path("M400,392 C440,372 480,364 520,368", "Crown light", fill=NONE,
       stroke="#8A6E52", strokeWidth=10, opacity=30, cap="round")
for i, dd in enumerate(["M356,470 C348,540 352,610 376,676",
                        "M644,470 C652,540 648,610 624,676",
                        "M408,716 C448,742 552,742 592,716"]):
    d.path(dd, f"Velvet {i+1}", fill=NONE, stroke="#0E0805",
           strokeWidth=6, opacity=35, cap="round")
# the eyes: pinpricks buried in the velvet — nearly nothing, as they should be
for i, sgn in enumerate([-1, 1]):
    d.shape("ellipse", f"Eye {i+1}", x=500 + sgn*88 - 6, y=452, width=12, height=12,
            fill="#0A0604", opacity=70, stroke=NONE)
    d.shape("ellipse", f"Eye fleck {i+1}", x=500 + sgn*88 - 4, y=454, width=4, height=4,
            fill="#C9AE84", opacity=40, stroke=NONE)

# --- the star: 22 rays in 11 mirrored pairs, base-deep rose to pale tips ------
SX, SY = 500, 585                    # star centre on the snout tip
# soft muzzle shadow under the snout so the star sits in a socket, not on fur
d.path(f"M{SX-110},{SY-30} C{SX-60},{SY+58} {SX+60},{SY+58} {SX+110},{SY-30} "
       f"C{SX+70},{SY+34} {SX-70},{SY+34} {SX-110},{SY-30} Z",
       "Muzzle shadow", fill="#1A100B", opacity=45, stroke=NONE)
# a soft glow under the rays so they lift off the dark fur
d.shape("ellipse", "Star aureole", x=SX-110, y=SY-110, width=220, height=220,
        fill=rad((0, "#C07878", 26), (0.65, "#C07878", 10), (1, "#C07878", 0)), stroke=NONE)

def ray(a, ln, w0, label):
    """Fleshy tapered ray leaning out at angle a (deg clockwise from up)."""
    bx, by = polar(SX, SY, 17, a)
    tx, ty = polar(SX, SY, 17 + ln, a)
    mx, my = polar(SX, SY, 17 + ln * 0.55, a)
    t = math.radians(a)
    nx, ny = math.cos(t), math.sin(t)
    w1 = w0 * 0.45
    d.path(f"M{bx - nx*w0:.1f},{by - ny*w0:.1f} "
           f"Q{mx - nx*w1:.1f},{my - ny*w1:.1f} {tx:.1f},{ty:.1f} "
           f"Q{mx + nx*w1:.1f},{my + ny*w1:.1f} {bx + nx*w0:.1f},{by + ny*w0:.1f} Z",
           label, fill=lin(bx, by, tx, ty,
                           (0, "#A84A55"), (0.55, "#D8848C"), (1, "#F2BCB6")),
           stroke=INK, strokeWidth=1.5)

# 11 pairs mirrored about the vertical: longest up top, shortest hanging low.
# angles run the right half 0 -> 150 deg; the low pair at +-150 leaves a
# shadow gap under the snout, like the real rosette's mobile lower rays.
lens = [70, 67, 63, 59, 56, 53, 50, 47, 42, 36, 30]
for i, a in enumerate([8 + k * 14.2 for k in range(11)]):
    ray(a, lens[i], 6.8, f"Ray R{i+1}")
    ray(-a, lens[i], 6.8, f"Ray L{i+1}")

# centre pad + twin nostrils the rays read from
d.path(f"M{SX-26},{SY-18} C{SX-31},{SY-3} {SX-21},{SY+13} {SX},{SY+16} "
       f"C{SX+21},{SY+13} {SX+31},{SY-3} {SX+26},{SY-18} "
       f"C{SX+16},{SY-26} {SX-16},{SY-26} {SX-26},{SY-18} Z",
       "Star pad", fill=rad((0, "#B25A62"), (1, "#7E343C")), stroke=INK, strokeWidth=2)
for i, sgn in enumerate([-1, 1]):
    d.shape("ellipse", f"Nostril {i+1}", x=SX + sgn*11 - 4.5, y=SY-8, width=9, height=7,
            fill="#3A1014", stroke=NONE)

# --- the spade paws, planted on the loam either side of the chest -------------
def paw(cxp, cyp, s, label):
    """Palmate forepaw: broad spade, digits + claws splayed toward +s in x
    (mole forepaws rotate permanently outward, digits to the outside)."""
    d.path(f"M{cxp - s*6},{cyp-56} "
           f"C{cxp + s*40},{cyp-54} {cxp + s*62},{cyp-30} {cxp + s*64},{cyp-2} "
           f"C{cxp + s*64},{cyp+24} {cxp + s*48},{cyp+42} {cxp + s*20},{cyp+48} "
           f"C{cxp - s*8},{cyp+52} {cxp - s*30},{cyp+44} {cxp - s*34},{cyp+18} "
           f"C{cxp - s*36},{cyp-10} {cxp - s*26},{cyp-44} {cxp - s*6},{cyp-56} Z",
           f"{label} palm", fill=PAW_GRAD, stroke=INK, strokeWidth=3)
    # digit grooves radiating to the outer edge + ivory claws riding it
    tips = [(58, -34), (63, -8), (61, 16), (50, 38)]
    for j, (ox, oy) in enumerate(tips):
        gx, gy = cxp + s * ox, cyp + oy
        sx_, sy_ = cxp + s * (6 - j * 4), cyp - 14 + j * 12
        d.path(f"M{sx_:.0f},{sy_:.0f} Q{cxp + s*ox*0.55:.0f},{cyp + oy*0.5:.0f} {gx:.0f},{gy:.0f}",
               f"{label} groove {j+1}", fill=NONE, stroke="#5E3C2C",
               strokeWidth=3, opacity=50, cap="round")
        d.path(f"M{gx - s*2:.0f},{gy-8:.0f} L{gx + s*17:.0f},{gy+2:.0f} L{gx - s*2:.0f},{gy+10:.0f} Z",
               f"{label} claw {j+1}", fill="#E4D2B4", stroke=INK, strokeWidth=1.5)

paw(372, 706, -1, "Paw L")
paw(628, 706, 1, "Paw R")

# --- loam floor: crest at y806, bottom closes on the disc arc ------------------
fy = 806
fdx = math.sqrt(R * R - (fy - CY) ** 2)
d.path(f"M{CX-fdx:.1f},{fy} C320,790 420,800 540,794 C640,790 720,798 {CX+fdx:.1f},{fy} "
       f"A{R},{R} 0 0 1 {CX-fdx:.1f},{fy} Z", "Floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{CX-fdx+8:.1f},{fy-2} C330,788 430,796 540,790 C640,786 720,794 {CX+fdx-8:.1f},{fy-2}",
       "Floor light", fill=NONE, stroke="#C9AE84", strokeWidth=4, opacity=30, cap="round")
# soil crumbs on the fresh digging
for i, (x, y, w) in enumerate([(300,815,16),(352,838,11),(470,826,14),(560,840,10),
                               (650,822,17),(680,824,9),(405,848,8),(610,850,7)]):
    assert on_disc(x, y, 10), (x, y)
    d.shape("ellipse", f"Crumb {i+1}", x=x, y=y, width=w, height=w*0.7,
            fill="#5E462E", opacity=80, stroke=NONE)
# an unearthed worm nosing out of the loam, mid-curve
d.path("M636,808 C648,798 662,798 672,806 C680,812 680,822 672,827",
       "Worm", fill=NONE, stroke="#C08A84", strokeWidth=10, cap="round")
d.path("M636,808 C648,798 662,798 672,806", "Worm light", fill=NONE,
       stroke="#E4B4AC", strokeWidth=4, opacity=70, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#0C0704", strokeWidth=6)

# --- name ----------------------------------------------------------------------
r1 = d.text("STAR-NOSED MOLE", "Name", x=500, y=962, size=58, font="Virelai Sans",
            color="#D6BE96", justify="center")

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

d.finish("star-nosed-mole-V1R00")
