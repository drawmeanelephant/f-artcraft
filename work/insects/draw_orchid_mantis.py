#!/usr/bin/env python3
"""Orchid mantis — field plate V1R00. Three-quarter view on a curving stem,
raptorial forelegs folded up in the classic praying pose, mid and hind femora
flared into wide petal lobes; white-to-pink gradient body with a green eye
spot, antennae barely there; orchid-pink plate. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Orchid Mantis — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420
INK = "#4A2038"

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

PETAL = linp(420, 320, 620, 660, (0, "#FFF6F4"), (0.55, "#F4C4D4"), (1, "#D98CA6"))
PETAL_EDGE = "#C86E8E"

# --- backdrop + orchid-pink plate ---------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin(-90, (0, "#180C16"), (1, "#080406")), stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#EAC2D4"), (0.6, "#B87E96"), (1, "#6E3E52")),
        stroke="#4E2A3C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F6DCE8", strokeWidth=3, opacity=45)
# faint orchid-petal veins radiating on the plate
for i, (x1, y1, x2, y2, cx1, cy1, op) in enumerate([
        (180, 300, 420, 200, 300, 220, 12), (240, 180, 560, 150, 400, 140, 10),
        (640, 160, 830, 300, 760, 200, 12), (160, 470, 300, 620, 210, 560, 10)]):
    d.path(f"M{x1},{y1} Q{cx1},{cy1} {x2},{y2}", f"Plate petal vein {i+1}",
           fill=NONE, stroke="#8A4E66", strokeWidth=4, opacity=op, cap="round")
# speckled pollinia dots
for i, (x, y, w) in enumerate([(220, 360, 7), (700, 240, 6), (790, 500, 8), (300, 720, 7),
                               (620, 760, 6), (170, 540, 6), (470, 150, 7), (840, 380, 5)]):
    d.shape("ellipse", f"Pollinia {i+1}", x=x, y=y, width=w, height=w,
            fill="#7E445A", opacity=30, stroke=NONE)

# --- stem the mantis stands on (ends land on the disc arc) ----------------------
s0, s1 = disc_pt(158), disc_pt(18)
d.path(f"M{s0[0]:.1f},{s0[1]:.1f} C320,706 620,690 {s1[0]:.1f},{s1[1]:.1f} "
       f"A420,420 0 0 1 {s0[0]:.1f},{s0[1]:.1f} Z", "Stem",
       fill=lin(-90, (0, "#8AA476"), (0.4, "#5E7A4E"), (1, "#2E4426")),
       stroke="#22331C", strokeWidth=5)
d.path(f"M{s0[0]+10:.0f},{s0[1]+8:.0f} C330,712 620,696 {s1[0]-10:.0f},{s1[1]+8:.0f}",
       "Stem top light", fill=NONE, stroke="#C8DCA8", strokeWidth=4, opacity=45, cap="round")
# a leaf and a bud on the stem
d.path("M300,694 C270,650 230,636 190,644 C220,676 258,696 300,694 Z", "Stem leaf",
       fill=lin(0, (0, "#7A9A62"), (1, "#3E5A34")), stroke="#22331C", strokeWidth=4)
d.path("M248,662 C236,676 222,684 208,686", "Leaf vein", fill=NONE,
       stroke="#2E4426", strokeWidth=3, opacity=60, cap="round")
d.path("M690,686 C700,650 726,632 752,636 C744,668 720,686 690,686 Z", "Stem bud leaf",
       fill=lin(0, (0, "#8AA470"), (1, "#44603A")), stroke="#22331C", strokeWidth=4)
d.shape("ellipse", "Bud", x=742, y=616, width=34, height=44,
        fill=rad((0, "#F2C6D6"), (0.7, "#CE8AA2"), (1, "#9A5670")),
        stroke=INK, strokeWidth=3)
d.path("M750,632 C756,626 766,624 772,628", "Bud sepal light", fill=NONE,
       stroke="#F8E2EA", strokeWidth=3, opacity=60, cap="round")
# mantis contact shadow on the stem
d.shape("ellipse", "Mantis shadow", x=380, y=656, width=280, height=30,
        fill="#1E2A16", opacity=35, stroke=NONE)

# everything from here is the mantis; collect it so it can be nudged
MANTIS = []
_call = d.call
def _capture(tool, args, label):
    r = _call(tool, args, label)
    if tool in ("draw_path", "draw_shape") and isinstance(r, dict) and "id" in r:
        MANTIS.append(r["id"])
    return r
d.call = _capture

# --- far-side legs (darker, behind everything) ------------------------------------
def petal(cx0, cy0, ang, L, W):
    """A petal lobe: lens shape along an axis from (cx0,cy0) at angle ang."""
    ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    pts = []
    n = 24
    for i in range(n + 1):
        t = i / n
        w = W * math.sin(math.pi * t) ** 0.8
        pts.append((t * L, w))
    xy = [(u, v) for u, v in pts] + [(u, -v) for u, v in pts[::-1]]
    out = [(cx0 + u * ca - v * sa, cy0 + u * sa + v * ca) for u, v in xy]
    return f"M{out[0][0]:.1f},{out[0][1]:.1f} " + " ".join(
        f"L{x:.1f},{y:.1f}" for x, y in out[1:]) + " Z"

def walking_leg(name, hip, knee, foot, far=False):
    col = "#B87A90" if far else PETAL
    edge = "#8A4E66" if far else PETAL_EDGE
    op = 60 if far else 100
    hx, hy = hip; kx, ky = knee; fx, fy = foot
    ang = math.degrees(math.atan2(ky - hy, kx - hx))
    L = math.hypot(kx - hx, ky - hy) + 26
    # femur flares into a broad petal lobe — the orchid-mantis signature
    d.path(petal(hx - 8 * math.cos(math.radians(ang)),
                 hy - 8 * math.sin(math.radians(ang)), ang, L, 30 if not far else 22),
           f"{name} petal femur", fill=col, stroke=edge, strokeWidth=4, opacity=op)
    # tibia + tarsus down to the stem
    d.path(f"M{kx},{ky} Q{(kx+fx)/2 + 4},{(ky+fy)/2} {fx},{fy}", f"{name} tibia ink",
           fill=NONE, stroke=INK, strokeWidth=7, cap="round", opacity=op)
    d.path(f"M{kx},{ky} Q{(kx+fx)/2 + 4},{(ky+fy)/2} {fx},{fy}", f"{name} tibia",
           fill=NONE, stroke="#E8B4C6" if not far else "#B87A90",
           strokeWidth=4, cap="round", opacity=op)
    d.path(f"M{fx},{fy} L{fx-8},{fy+9}", f"{name} tarsus",
           fill=NONE, stroke=INK, strokeWidth=3.5, cap="round", opacity=op)
    if not far:
        d.path(f"M{hx+4},{hy+2} L{kx-6},{ky-4}", f"{name} femur vein", fill=NONE,
               stroke="#D98CA6", strokeWidth=3, opacity=55, cap="round")

walking_leg("Far mid leg", (488, 556), (520, 612), (528, 668), far=True)
walking_leg("Far hind leg", (540, 566), (596, 614), (620, 664), far=True)

# --- abdomen: plump, lobed like petals, tipped pink -------------------------------
# lateral petal lobes peeking below the abdomen's silhouette
for i, (x, y, ang, L, W) in enumerate([(560, 636, 28, 78, 24), (620, 612, 48, 66, 20)]):
    d.path(petal(x, y, ang, L, W), f"Abdomen lobe {i+1}",
           fill=PETAL, stroke=PETAL_EDGE, strokeWidth=4)
d.path("M470,500 C530,470 610,486 660,540 C700,584 690,636 648,656 "
       "C600,678 520,666 478,624 C450,596 448,540 470,500 Z",
       "Abdomen", fill=PETAL, stroke=INK, strokeWidth=5)
d.path("M492,596 C540,640 610,650 656,622", "Abdomen lower lobe", fill=NONE,
       stroke=PETAL_EDGE, strokeWidth=5, opacity=55, cap="round")
d.path("M500,540 C560,516 630,528 668,568", "Abdomen segment 1", fill=NONE,
       stroke="#D98CA6", strokeWidth=3, opacity=45, cap="round")
d.path("M506,576 C560,554 624,562 660,598", "Abdomen segment 2", fill=NONE,
       stroke="#D98CA6", strokeWidth=3, opacity=45, cap="round")
# pink flush at the abdomen tip
d.shape("ellipse", "Abdomen tip blush", x=614, y=590, width=58, height=40,
        fill="#D97E9E", opacity=35, stroke=NONE)
# folded wing (tegmen): translucent petal over the back, hint of venation
d.path("M462,510 C520,478 600,490 654,544 C620,556 540,556 492,540 "
       "C472,532 462,522 462,510 Z", "Tegmen",
       fill=lin(0, (0, "#FDF0F2"), (1, "#EFC2D2")), opacity=62,
       stroke="#C8849E", strokeWidth=3)
d.path("M478,516 C540,498 606,510 648,544", "Tegmen vein 1", fill=NONE,
       stroke="#B86E88", strokeWidth=3, opacity=50, cap="round")
d.path("M490,528 C546,512 604,522 640,550", "Tegmen vein 2", fill=NONE,
       stroke="#B86E88", strokeWidth=3, opacity=40, cap="round")

# --- prothorax: the long mantis neck ----------------------------------------------
d.path("M404,468 C398,432 404,398 420,372 C440,362 462,370 470,392 "
       "C480,424 478,466 466,500 C444,514 414,502 404,468 Z",
       "Prothorax", fill=linp(400, 360, 480, 510, (0, "#FFF8F6"), (0.6, "#F2C0D0"),
                              (1, "#D0889E")), stroke=INK, strokeWidth=5)
d.path("M416,400 C420,430 418,462 412,486", "Prothorax keel", fill=NONE,
       stroke="#D98CA6", strokeWidth=3, opacity=50, cap="round")
d.path("M428,376 C444,368 460,374 466,390", "Prothorax rim light", fill=NONE,
       stroke="#FFFFFF", strokeWidth=4, opacity=65, cap="round")

# --- raptorial forelegs folded in prayer -------------------------------------------
def foreleg(name, coxa, femtip, tibtip, far=False):
    col = "#E8B0C2" if far else PETAL
    edge = "#8A4E66" if far else PETAL_EDGE
    op = 70 if far else 100
    cx, cy = coxa; fx, fy = femtip; tx, ty = tibtip
    # femur: thick, flared into a petal lobe, spines along the inner edge
    ang = math.degrees(math.atan2(fy - cy, fx - cx))
    L = math.hypot(fx - cx, fy - cy) + 20
    d.path(petal(cx - 6 * math.cos(math.radians(ang)),
                 cy - 6 * math.sin(math.radians(ang)), ang, L,
                 26 if not far else 18), f"{name} femur lobe", fill=col,
           stroke=edge, strokeWidth=4, opacity=op)
    for j, t in enumerate([0.5, 0.68, 0.85]):
        x = cx + (fx - cx) * t; y = cy + (fy - cy) * t
        d.path(f"M{x:.0f},{y + 8:.0f} L{x - 4:.0f},{y + 20:.0f}",
               f"{name} femur spine {j+1}", fill=NONE, stroke=INK,
               strokeWidth=3, cap="round", opacity=op)
    # tibia folds back parallel against the femur
    tib = ((fx, fy), (fx + (tx-fx)*0.4 - 8, fy + (ty-fy)*0.4),
           (fx + (tx-fx)*0.7 - 6, fy + (ty-fy)*0.7), (tx, ty))
    d.path(ribbon(tib, [10, 14, 7]), f"{name} tibia", fill=col,
           stroke=edge, strokeWidth=4, opacity=op)
    d.path(f"M{tx},{ty} L{tx + 12},{ty + 8}", f"{name} tarsus",
           fill=NONE, stroke=INK, strokeWidth=3.5, cap="round", opacity=op)

foreleg("Far foreleg", (436, 460), (392, 396), (428, 452), far=True)
foreleg("Near foreleg", (458, 476), (402, 408), (446, 478))

# --- near walking legs --------------------------------------------------------------
walking_leg("Near mid leg", (500, 560), (456, 622), (442, 672))
walking_leg("Near hind leg", (560, 570), (560, 630), (556, 680))

# --- head: broad triangle, huge lateral eyes, one green spot ------------------------
d.path("M396,394 C376,388 360,368 358,344 C370,322 396,310 424,314 "
       "C448,318 462,336 460,360 C456,384 430,398 396,394 Z", "Head",
       fill=rad((0, "#FFF4F4"), (0.6, "#F0C2D0"), (1, "#CE8AA0")),
       stroke=INK, strokeWidth=5)
# two big compound eyes at the head's upper corners
d.path("M366,346 C360,326 372,308 392,304 C404,310 408,324 402,340 "
       "C392,352 376,354 366,346 Z", "Far eye",
       fill=rad((0, "#E8C8D6"), (1, "#B87A94")), stroke=INK, strokeWidth=4)
d.path("M420,318 C438,310 458,318 462,338 C458,356 442,364 428,356 "
       "C416,346 412,330 420,318 Z", "Near eye",
       fill=rad((0, "#E8C8D6"), (1, "#B87A94")), stroke=INK, strokeWidth=4)
# the green eye spot — an orchid-mantis tell — on the near eye
d.shape("ellipse", "Green eye spot", x=430, y=322, width=22, height=20,
        fill=rad((0, "#8AD8A2"), (0.7, "#3E9A5E"), (1, "#1E5C36")),
        stroke="#17502E", strokeWidth=3)
d.shape("ellipse", "Spot glint", x=436, y=326, width=6, height=6,
        fill="#FFFFFF", opacity=85, stroke=NONE)
d.shape("ellipse", "Far eye glint", x=378, y=316, width=6, height=6,
        fill="#FFFFFF", opacity=70, stroke=NONE)
# little ocellar bump between the eyes + mouth line
d.shape("ellipse", "Ocellus", x=408, y=332, width=10, height=8,
        fill="#D98CA6", stroke=INK, strokeWidth=2)
d.path("M384,378 C396,386 414,388 428,382", "Mouth line", fill=NONE,
       stroke=INK, strokeWidth=3, opacity=60, cap="round")
# antennae barely there: two whisper-thin strokes, low opacity
d.path("M392,318 C368,288 342,272 316,266", "Far antenna", fill=NONE,
       stroke="#E8C4D2", strokeWidth=3, opacity=55, cap="round")
d.path("M428,310 C444,278 466,258 490,248", "Near antenna", fill=NONE,
       stroke="#E8C4D2", strokeWidth=3, opacity=55, cap="round")

# two drifting petals — a flower that eats visitors sheds decoys
for i, (x, y, ang, L, W, op) in enumerate([(700, 250, -30, 84, 30, 55), (620, 180, 18, 62, 22, 40)]):
    d.path(petal(x, y, ang, L, W), f"Drifting petal {i+1}",
           fill=PETAL, stroke=PETAL_EDGE, strokeWidth=3, opacity=op)
    d.path(f"M{x+6},{y} L{x + L*0.7*math.cos(math.radians(ang)):.0f},"
           f"{y + L*0.7*math.sin(math.radians(ang)):.0f}",
           f"Drifting petal {i+1} vein", fill=NONE, stroke="#C8849E",
           strokeWidth=3, opacity=op - 15, cap="round")

d.call = _call
d.call("transform", {"ids": MANTIS, "dx": 6, "dy": -6}, "nudge mantis")

# --- caption --------------------------------------------------------------------------
d.text("ORCHID MANTIS", "Name", x=500, y=940, size=56, font="Virelai Sans",
       color="#F8E4EC", justify="center")
o = d.text("MANTODEA", "Order", x=500, y=975, size=22, font="Virelai Sans",
           color="#D8A8BC", justify="center")
if o and "id" in o:
    d.cmd("text.setStyle", "Order tracking", ids=[o["id"]], tracking=400)

d.finish("orchid-mantis-V1R00")
