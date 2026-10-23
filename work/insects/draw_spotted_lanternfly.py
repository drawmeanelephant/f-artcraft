#!/usr/bin/env python3
"""Spotted lanternfly — field plate V1R00. Three-quarter dorsal with the
wings half-lifted in the threat display: grey forewings with black spots
spread like shutters, the red-black-white hindwing banding showing beneath;
bark-brown plate with one pale ridge. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Spotted Lanternfly — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420
INK = "#241610"

def lin(angle, *stops):
    return {"gradient": {"kind": "linear", "angle": angle, "stops": [
        {"offset": o, "color": c} for o, c in stops]}}

def linp(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1], "stops": [
        {"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial", "stops": [
        {"offset": o, "color": c} for o, c in stops]}}

def disc_pt(deg, r=R):
    a = math.radians(deg)
    return (CX + r * math.cos(a), CY + r * math.sin(a))

def rot(x, y, cx, cy, deg):
    a = math.radians(deg); c, s = math.cos(a), math.sin(a)
    return (cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c)

# --- backdrop + bark-brown plate ---------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin(-90, (0, "#14100C"), (1, "#060403")), stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#8A6248"), (0.6, "#54381F"), (1, "#2C1A0E")),
        stroke="#3C2410", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C09A72", strokeWidth=3, opacity=40)
# bark furrows running down the plate
for i, (x0, x1, cy1, cy2, w, op) in enumerate([
        (150, 260, 300, 720, 7, 45), (210, 180, 400, 640, 5, 35),
        (310, 330, 180, 800, 6, 40), (660, 690, 160, 780, 6, 40),
        (760, 720, 280, 700, 5, 35), (830, 800, 380, 620, 7, 40)]):
    d.path(f"M{x0},{cy1} C{x0 + 24},{(cy1 + cy2) / 2} {x1 - 24},{(cy1 + cy2) / 2} {x1},{cy2}",
           f"Bark furrow {i+1}", fill=NONE, stroke="#1C0E06", strokeWidth=w,
           opacity=op, cap="round")
# the one pale ridge the brief asks for — a lit bark edge, left of centre
d.path("M262,150 C286,340 268,540 292,770", "Pale ridge", fill=NONE,
       stroke="#C8A87E", strokeWidth=9, opacity=55, cap="round")
d.path("M274,160 C296,340 280,540 302,760", "Ridge light", fill=NONE,
       stroke="#EED9B8", strokeWidth=4, opacity=60, cap="round")
d.path("M250,160 C274,340 256,540 280,760", "Ridge shadow", fill=NONE,
       stroke="#241408", strokeWidth=5, opacity=45, cap="round")
# lichen flecks
for i, (x, y, w, h) in enumerate([(180, 340, 40, 18), (760, 300, 52, 22), (810, 560, 44, 18),
                                  (220, 620, 38, 16), (560, 170, 46, 20)]):
    d.shape("ellipse", f"Lichen {i+1}", x=x, y=y, width=w, height=h,
            fill=rad((0, "#B8BE8E"), (1, "#6E7448")), opacity=45, stroke=NONE)
# contact shadow under the insect
d.shape("ellipse", "Lanternfly shadow", x=330, y=640, width=340, height=40,
        fill="#000000", opacity=35, stroke=NONE)

# everything from here is the insect; collect it so it can be nudged
BUG = []
_call = d.call
def _capture(tool, args, label):
    r = _call(tool, args, label)
    if tool in ("draw_path", "draw_shape") and isinstance(r, dict) and "id" in r:
        BUG.append(r["id"])
    return r
d.call = _capture

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

# --- hindwings first (they sit under the half-lifted forewings) -------------------
def hindwing(name, spine, widths, far=False):
    """Red fan built as a ribbon: red field, black band, cream band at the tip."""
    op = 72 if far else 100
    (hx, hy), _, _, (tx, ty) = spine
    d.path(ribbon(spine, widths), f"{name} fan",
           fill=linp(hx, hy, tx, ty, (0, "#DC3E2C"), (0.6, "#B0281E"), (1, "#7E1812")),
           stroke="#3A1408", strokeWidth=4, opacity=op)

    def halfw(t):
        s = t * (len(widths) - 1); k = min(int(s), len(widths) - 2); f = s - k
        return (widths[k] * (1 - f) + widths[k + 1] * f) / 2

    def band(t, color, width, opacity, label):
        x, y, ux, uy, nx, ny = frame(spine, t)
        hw = halfw(t) * 0.96
        d.path(f"M{x - nx*hw:.0f},{y - ny*hw:.0f} L{x + nx*hw:.0f},{y + ny*hw:.0f}",
               f"{name} {label}", fill=NONE, stroke=color, strokeWidth=width,
               opacity=opacity, cap="round")

    band(0.58, "#1E0E0A", 30, 80 if not far else 58, "black band")
    band(0.80, "#F0E0C0", 20, 85 if not far else 60, "cream band")
    # black spots on the red base
    for j, (t, off, w) in enumerate([(0.16, 0.4, 9), (0.28, -0.35, 8), (0.38, 0.3, 7)]):
        x, y, ux, uy, nx, ny = frame(spine, t)
        hw = halfw(t)
        px, py = x + nx * hw * off, y + ny * hw * off
        d.shape("ellipse", f"{name} spot {j+1}", x=px - w/2, y=py - w/2,
                width=w, height=w, fill="#1E0E0A", opacity=72, stroke=NONE)

hindwing("Far hindwing", ((484, 434), (424, 486), (356, 542), (312, 612)),
         [18, 52, 74, 30], far=True)
hindwing("Near hindwing", ((516, 434), (580, 486), (648, 548), (692, 618)),
         [18, 54, 78, 32])

# --- abdomen: dark, banded, tucked under the wings ---------------------------------
d.path("M452,470 C440,540 452,600 480,640 C494,658 516,658 528,640 "
       "C552,600 558,540 548,470 C520,452 480,452 452,470 Z",
       "Abdomen", fill=linp(500, 460, 500, 650, (0, "#4A3828"), (0.5, "#2E2014"),
                            (1, "#18100A")), stroke=INK, strokeWidth=5)
# pale segment bands
for j, (y, w) in enumerate([(500, 74), (545, 66), (590, 54), (628, 38)]):
    d.path(f"M{500 - w},{y} C{500 - w/2},{y + 12} {500 + w/2},{y + 12} {500 + w},{y}",
           f"Abdomen band {j+1}", fill=NONE, stroke="#C8A05A", strokeWidth=5,
           opacity=45, cap="round")

# --- forewings: grey, spotted, reticulated tips, lifted like shutters ---------------
def forewing(name, spine, widths, far=False):
    """Grey tegmen built as a ribbon along a cubic spine: pale grey field,
    black spots on the basal 2/3, reticulated dark veins near the tip."""
    op = 88 if far else 96
    (hx, hy), _, _, (tx, ty) = spine
    # the wing membrane, semi-translucent over the plate beneath
    d.path(ribbon(spine, widths), f"{name} wing",
           fill=linp(hx, hy, tx, ty,
                     (0, "#CFC9AC"), (0.5, "#ADA789"), (0.82, "#7E785C"),
                     (1, "#5C563F")), stroke=INK, strokeWidth=5, opacity=op)
    # leading-edge rim light along the outer rim
    x0, y0, ux, uy, nx, ny = frame(spine, 0.08)
    if nx * (x0 - 500) + ny * (y0 - 430) < 0:
        nx, ny = -nx, -ny
    x1, y1 = frame(spine, 0.55)[:2]
    d.path(f"M{x0 + nx*widths[0]*0.4:.0f},{y0 + ny*widths[0]*0.4:.0f} "
           f"Q{(x0+x1)/2 + nx*60:.0f},{(y0+y1)/2 + ny*60:.0f} "
           f"{x1 + nx*widths[2]*0.42:.0f},{y1 + ny*widths[2]*0.42:.0f}",
           f"{name} leading light", fill=NONE, stroke="#EDE6CC",
           strokeWidth=4, opacity=55, cap="round")
    # black spots scattered over the basal 2/3, placed along the spine normals
    spot_ts = [(0.14, 0.5, 9), (0.14, -0.5, 8), (0.26, 0.1, 10), (0.30, -0.6, 7),
               (0.34, 0.55, 8), (0.44, -0.2, 9), (0.46, 0.5, 7), (0.55, 0.0, 8),
               (0.58, -0.55, 6), (0.63, 0.45, 7), (0.68, -0.15, 6), (0.72, 0.3, 6)]
    for j, (t, off, w) in enumerate(spot_ts):
        x, y, ux, uy, nx2, ny2 = frame(spine, t)
        s = t * (len(widths) - 1); k = min(int(s), len(widths) - 2); f = s - k
        hw = (widths[k] * (1 - f) + widths[k + 1] * f) / 2
        px, py = x + nx2 * hw * off, y + ny2 * hw * off
        d.shape("ellipse", f"{name} spot {j+1}", x=px - w/2, y=py - w/2,
                width=w, height=w * 0.85, fill="#18100C", opacity=78, stroke=NONE)
    # reticulation: cross veins + a long vein near the apical third
    for j, t in enumerate([0.66, 0.78, 0.90]):
        x, y, ux, uy, nx2, ny2 = frame(spine, t)
        s = t * (len(widths) - 1); k = min(int(s), len(widths) - 2); f = s - k
        hw = (widths[k] * (1 - f) + widths[k + 1] * f) / 2
        d.path(f"M{x - nx2*hw*0.8:.0f},{y - ny2*hw*0.8:.0f} "
               f"L{x + nx2*hw*0.8:.0f},{y + ny2*hw*0.8:.0f}",
               f"{name} crossvein {j+1}", fill=NONE, stroke="#2E2416",
               strokeWidth=3, opacity=55, cap="round")
    xa, ya, ux, uy = cubic(spine, 0.62)[0], cubic(spine, 0.62)[1], 0, 0
    xb, yb = cubic(spine, 0.97)[0], cubic(spine, 0.97)[1]
    xc, yc = cubic(spine, 0.8)[0] + 10, cubic(spine, 0.8)[1] + 14
    d.path(f"M{xa:.0f},{ya:.0f} Q{xc:.0f},{yc:.0f} {xb:.0f},{yb:.0f}",
           f"{name} long vein", fill=NONE, stroke="#2E2416", strokeWidth=3,
           opacity=50, cap="round")

# far forewing: a touch steeper, half-shadowed
forewing("Far forewing",
         ((482, 378), (386, 320), (300, 400), (262, 540)), [16, 54, 66, 22], far=True)
# near forewing: broader and lower, catches the light
forewing("Near forewing",
         ((518, 378), (622, 318), (726, 410), (758, 556)), [16, 58, 72, 24])
# sheen on the near wing
d.path("M560,392 C640,360 716,420 748,530 C700,462 620,420 560,412 Z",
       "Near wing sheen", fill="#FFF6E0", opacity=28, stroke=NONE)

# --- thorax + head -----------------------------------------------------------------
d.path("M452,380 C448,344 468,318 500,314 C532,318 552,344 548,380 "
       "C544,410 524,428 500,428 C476,428 456,410 452,380 Z", "Thorax",
       fill=rad((0, "#5A4630"), (0.6, "#33241A"), (1, "#17100A")),
       stroke=INK, strokeWidth=5)
d.path("M468,336 C484,324 518,324 534,336", "Thorax rim light", fill=NONE,
       stroke="#C8A87E", strokeWidth=4, opacity=60, cap="round")
# small head with the planthopper's short snout
d.path("M468,318 C466,296 480,282 500,282 C520,282 534,296 532,318 "
       "C528,336 514,346 500,346 C486,346 472,336 468,318 Z", "Head",
       fill=rad((0, "#6E5238"), (0.6, "#3A2818"), (1, "#1A0F08")),
       stroke=INK, strokeWidth=4)
d.path("M486,332 C494,338 506,338 514,332 C510,348 490,348 486,332 Z",
       "Snout", fill="#2E1E10", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Far eye", x=466, y=300, width=20, height=24,
        fill=rad((0, "#7E5E3E"), (1, "#140C06")), stroke=INK, strokeWidth=3)
d.shape("ellipse", "Near eye", x=516, y=300, width=20, height=24,
        fill=rad((0, "#7E5E3E"), (1, "#140C06")), stroke=INK, strokeWidth=3)
d.shape("ellipse", "Far eye glint", x=471, y=305, width=5, height=5,
        fill="#FFFFFF", opacity=80, stroke=NONE)
d.shape("ellipse", "Near eye glint", x=521, y=305, width=5, height=5,
        fill="#FFFFFF", opacity=80, stroke=NONE)
# short bristle antennae
d.path("M488,288 C478,266 466,254 452,248", "Far antenna", fill=NONE,
       stroke=INK, strokeWidth=3.5, cap="round")
d.path("M512,288 C522,266 534,254 548,248", "Near antenna", fill=NONE,
       stroke=INK, strokeWidth=3.5, cap="round")
d.shape("ellipse", "Far antenna tip", x=449, y=245, width=6, height=6,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Near antenna tip", x=545, y=245, width=6, height=6,
        fill=INK, stroke=NONE)

# --- legs: six splayed, gripping the bark --------------------------------------------
def leg(name, hip, foot, mirror, far=False):
    col = "#1C110A" if far else "#3A2414"
    op = 70 if far else 100
    hx, hy = hip; fx, fy = foot
    kx, ky = hx + (fx - hx) * 0.45 + mirror * 26, hy + (fy - hy) * 0.45 - 14
    d.path(f"M{hx},{hy} L{kx},{ky} L{fx},{fy}", f"{name} ink",
           fill=NONE, stroke=INK, strokeWidth=8, cap="round", join="round", opacity=op)
    d.path(f"M{hx},{hy} L{kx},{ky} L{fx},{fy}", name,
           fill=NONE, stroke=col, strokeWidth=4.5, cap="round", join="round", opacity=op)
    d.path(f"M{fx},{fy} L{fx + mirror*12},{fy + 8}", f"{name} tarsus",
           fill=NONE, stroke=INK, strokeWidth=3.5, cap="round", opacity=op)

leg("Far fore leg", (470, 396), (400, 428), -1, far=True)
leg("Far mid leg", (458, 470), (380, 510), -1, far=True)
leg("Far hind leg", (468, 560), (402, 620), -1, far=True)
leg("Near fore leg", (530, 396), (602, 430), 1)
leg("Near mid leg", (542, 470), (624, 512), 1)
leg("Near hind leg", (532, 560), (600, 622), 1)

d.call = _call
d.call("transform", {"ids": BUG, "dy": -12}, "nudge lanternfly up")

# --- caption --------------------------------------------------------------------------
d.text("SPOTTED LANTERNFLY", "Name", x=500, y=938, size=48, font="Virelai Sans",
       color="#EAD9BC", justify="center")
o = d.text("HEMIPTERA", "Order", x=500, y=974, size=22, font="Virelai Sans",
           color="#B8966C", justify="center")
if o and "id" in o:
    d.cmd("text.setStyle", "Order tracking", ids=[o["id"]], tracking=400)

d.finish("spotted-lanternfly-V1R00")
