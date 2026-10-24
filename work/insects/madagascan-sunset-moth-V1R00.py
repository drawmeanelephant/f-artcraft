#!/usr/bin/env python3
"""Madagascan sunset moth — field plate V1R00. Living Chrysiridia rhipheus
basking dorsal-spread on foliage: dark wings crossed by iridescent
green/blue-violet bands, hindwings carrying the orange-red field and three
ribbon tails. Day-flying moth — slim feathered antennae, no pin, no board.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420; tails and antennae stay inside."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Madagascan Sunset Moth — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#22100A"


def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad


def F(p):
    return "%.1f,%.1f" % p


def cr(pts, closed=True):
    n = len(pts)
    s = "M" + F(pts[0])
    for i in range(n if closed else n - 1):
        p0 = pts[(i - 1) % n] if (closed or i > 0) else pts[0]
        p1, p2 = pts[i], pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (closed or i + 2 < n) else pts[-1]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        s += " C%s %s %s" % (F(c1), F(c2), F(p2))
    return s + (" Z" if closed else "")


def blob(cx, cy, rx, ry, X, n=10):
    return cr([X((cx + rx * math.cos(2 * math.pi * k / n), cy + ry * math.sin(2 * math.pi * k / n)))
               for k in range(n)])


def pid(r):
    return r["id"] if r else None


def lin(a, b, stops):
    return {"gradient": {"kind": "linear", "start": list(a), "end": list(b),
                         "stops": [{"offset": o, "color": c} for o, c in stops]}}


def rad(stops):
    return {"gradient": {"kind": "radial",
                         "stops": [{"offset": o, "color": c} for o, c in stops]}}


# moth drawn on the right half in raw space, scaled onto the disc; left is mirrored
S, OY = 0.95, 470
def T(p):
    return (500 + S * (p[0] - 500), OY + S * (p[1] - 440))
def Tm(p):
    q = T(p)
    return (1000 - q[0], q[1])

BG_GRAD    = lin((0, 0), (0, 1000), [(0, "#141A10"), (1, "#060804")])
PLATE_GRAD = rad([(0, "#4A7A54"), (0.6, "#2A4E36"), (1, "#122418")])
FLOOR_GRAD = lin((0, 780), (0, 880), [(0, "#3A5A34"), (1, "#182A16")])
LEAF_GRAD  = lin((300, 560), (760, 700), [(0, "#5E8A46"), (0.55, "#3E6634"), (1, "#22401E")])
FORE_DARK  = lin((540, 320), (840, 300), [(0, "#3A1C10"), (0.5, "#2A140C"), (1, "#1C0E08")])
HIND_WARM  = rad([(0, "#F08030"), (0.55, "#D84E20"), (1, "#6E1E10")])

# --- backdrop + forest plate -----------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876, fill="#4A7A54", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840, fill=PLATE_GRAD,
        stroke="#0C1C12", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792, fill=NONE,
        stroke="#A8D6B0", strokeWidth=3, opacity=28)
for i, (x, y, w) in enumerate([(180, 330, 6), (820, 300, 5), (150, 500, 6), (860, 470, 5),
                               (420, 100, 5), (600, 96, 6), (300, 150, 4), (700, 160, 5),
                               (240, 250, 4), (770, 230, 4), (130, 420, 4), (880, 560, 4)]):
    assert on_disc(x, y, 12), (x, y)
    d.shape("ellipse", f"Pollen {i+1}", x=x, y=y, width=w, height=w, fill="#F0E8C8",
            opacity=32, stroke=NONE)

# --- floor band closing on the disc arc -------------------------------------------------
gy = 796
gdx = math.sqrt(PR * PR - (gy - PCY) ** 2)
d.path(f"M{PCX-gdx:.1f},{gy} C330,790 420,800 500,798 C590,796 670,800 {PCX+gdx:.1f},{gy} "
       f"A{PR},{PR} 0 0 1 {PCX-gdx:.1f},{gy} Z",
       "Floor", fill=FLOOR_GRAD, opacity=92, stroke=NONE)

# --- foliage the moth sits on ------------------------------------------------------------
# stem rising from the floor, leaf spreading under the wings
d.path("M310,838 C340,740 390,660 460,610", "Leaf stem", fill=NONE,
       stroke="#4E7A3E", strokeWidth=7, cap="round")
d.path(cr([(300,640),(360,592),(470,566),(590,566),(700,596),(760,642),
           (700,690),(560,712),(420,704),(330,676)]),
       "Perch leaf", fill=LEAF_GRAD, stroke=INK, strokeWidth=4)
d.path("M310,648 C420,620 560,610 740,632", "Leaf midrib", fill=NONE,
       stroke="#2A4A22", strokeWidth=3.5, opacity=80, cap="round")
for k, (x0, x1, y) in enumerate([(360, 470, 640), (420, 560, 672), (540, 660, 668)]):
    d.path(f"M{x0},{y} Q{(x0+x1)//2},{y+16} {x1},{y+4}", f"Leaf vein {k+1}",
           fill=NONE, stroke="#2A4A22", strokeWidth=2.5, opacity=60, cap="round")
# a second leaf curling in from the right
d.path("M760,700 C720,690 690,672 672,646 C706,652 736,668 760,700 Z",
       "Side leaf", fill="#3E6634", opacity=80, stroke=INK, strokeWidth=2.5)

# --- wing geometry (raw, right side) ------------------------------------------------------
# forewing: near-triangular, apex high and out
FORE = [(512, 314), (560, 282), (640, 250), (724, 226), (806, 218), (852, 232),
        (862, 258), (838, 282), (788, 306), (734, 336), (688, 368), (644, 398),
        (596, 416), (552, 420), (516, 406)]
# hindwing: rounded lobe falling into three tails (longest at the bottom)
HIND = [(514, 414), (580, 432), (660, 462), (726, 502), (762, 548),
        (756, 590), (786, 606), (792, 648),                       # tail 1 (outer, short)
        (742, 640), (726, 682), (722, 726),                       # tail 2 (longest)
        (674, 694), (656, 706), (628, 690),                       # tail 3 (inner)
        (604, 650), (566, 600), (534, 540), (516, 470)]

for pts, lbl in [(FORE, "fore"), (HIND, "hind")]:
    for p in pts:
        assert on_disc(*T(p), 14), (lbl, T(p))


def stroke(X, pts, label, color, w, op=100):
    return pid(d.path(cr([X(p) for p in pts], closed=False), label, fill=NONE, stroke=color,
                      strokeWidth=w, opacity=op, cap="round"))


def fore_patterns(X, side):
    L = f"Forewing {side}"
    ids = []
    # iridescent margin band, broken into colour steps green -> teal -> violet
    for k, (seg, col) in enumerate([
            ([(856,244),(824,272),(780,300)], "#3FCF8E"),
            ([(780,300),(734,336),(692,366)], "#3AA8D8"),
            ([(692,366),(652,394),(612,412)], "#8A5AE0"),
            ([(612,412),(576,418),(548,416)], "#6A4AC8")]):
        ids.append(stroke(X, seg, f"{L} iridescence {k+1}", col, 15, 80))
    # darker margin shading inside the band
    ids.append(stroke(X, [(848,252),(812,282),(762,310),(712,342),(664,374),
                          (618,402),(576,414),(548,414)],
                      L + " margin shade", "#120805", 5, 60))
    # basal red-orange flame patch
    ids.append(pid(d.path(blob(560, 356, 44, 58, X), L + " basal flame",
                          fill=rad([(0, "#E86A30"), (0.7, "#B03418"), (1, "#6E1E10")]),
                          opacity=85, stroke=NONE)))
    # veins, subordinate to the colour
    for k, (tx, ty) in enumerate([(640,252),(724,230),(800,224),(788,306),(694,372),(610,416)]):
        mx, my = (520 + tx) / 2, (352 + ty) / 2
        ids.append(stroke(X, [(522,352),(mx + (ty-352)*0.05, my - (tx-522)*0.05),(tx,ty)],
                          f"{L} vein {k+1}", "#1C0C06", 3, 55))
    return ids


def hind_patterns(X, side):
    L = f"Hindwing {side}"
    ids = []
    # dark margin band around the lobe
    ids.append(stroke(X, [(740,486),(770,540),(756,592),(786,608),(790,644)],
                      L + " margin dark", "#1C0C08", 16, 85))
    ids.append(stroke(X, [(724,674),(722,712)], L + " tail2 edge", "#1C0C08", 14, 85))
    ids.append(stroke(X, [(678,690),(634,684)], L + " tail3 edge", "#1C0C08", 12, 85))
    # pale tail tips, the moth's white edging
    for k, (tx, ty) in enumerate([(792,652),(726,718),(628,688)]):
        ids.append(pid(d.path(blob(tx, ty, 8, 6, X), f"{L} tail tip {k+1}",
                              fill="#F2EBD8", opacity=85, stroke=NONE)))
    # blue-violet margin spots between the dark band and the orange field
    for k, (x, y) in enumerate([(726,500),(752,548),(744,592)]):
        ids.append(pid(d.path(blob(x, y, 12, 9, X), f"{L} blue spot {k+1}",
                              fill=rad([(0, "#4AC8E8"), (1, "#5A4AD0")]), opacity=90, stroke=NONE)))
    # green sheen washing the upper lobe
    ids.append(pid(d.path(blob(660, 486, 60, 40, X), L + " green sheen",
                          fill=rad([(0, "#4AC890"), (1, "#2A6E50")]), opacity=40, stroke=NONE)))
    # veins
    for k, (tx, ty) in enumerate([(660,466),(726,508),(758,552),(748,620),(700,680),(620,660)]):
        mx, my = (522 + tx) / 2, (452 + ty) / 2
        ids.append(stroke(X, [(522,452),(mx + (ty-452)*0.05, my - (tx-522)*0.05),(tx,ty)],
                          f"{L} vein {k+1}", "#1C0C06", 3, 50))
    return ids


def wing(label, raw, grad, X, patterns, side):
    wd = cr([X(p) for p in raw])
    w = pid(d.path(wd, label, fill=grad, stroke=NONE, opacity=95))
    ids = [w] + [i for i in patterns(X, side) if i]
    m = pid(d.path(wd, label + " mask", fill="#000000", stroke=NONE))
    d.cmd("object.clippingMask.make", label + " clip", ids=ids + [m])
    d.path(wd, label + " outline", fill=NONE, stroke=INK, strokeWidth=4, opacity=92)


def fore_grad(X):
    return FORE_DARK

def hind_grad(X):
    return {"gradient": {"kind": "linear", "start": list(X((530, 440))),
                         "end": list(X((740, 620))),
                         "stops": [{"offset": 0, "color": "#F08030"},
                                   {"offset": 0.55, "color": "#D84E20"},
                                   {"offset": 1, "color": "#5E1E10"}]}}


# --- cast shadow on the leaf ---------------------------------------------------------------
d.shape("ellipse", "Moth shadow", x=380, y=600, width=260, height=30,
        fill="#0E1808", opacity=35, stroke=NONE)

# --- wings: hind under fore ----------------------------------------------------------------
for X, side in [(T, "R"), (Tm, "L")]:
    wing(f"Hindwing {side}", HIND, hind_grad(X), X, hind_patterns, side)
for X, side in [(T, "R"), (Tm, "L")]:
    wing(f"Forewing {side}", FORE, fore_grad(X), X, fore_patterns, side)

# --- body ---------------------------------------------------------------------------------
ABD = [(500, 400), (520, 414), (524, 470), (512, 520), (500, 540), (488, 520), (476, 470), (480, 414)]
d.path(cr([T(p) for p in ABD]), "Abdomen",
       fill=lin(T((478, 0)), T((522, 0)), [(0, "#3A1C10"), (0.5, "#6A3418"), (1, "#2E1408")]),
       stroke=INK, strokeWidth=4)
for k, y in enumerate([428, 452, 476, 500]):
    hw = {428: 20, 452: 21, 476: 19, 500: 14}[y]
    d.path(cr([T((500 - hw, y - 2)), T((500, y + 4)), T((500 + hw, y - 2))], closed=False),
           f"Abdomen band {k+1}", fill=NONE, stroke="#E8DCC0", strokeWidth=3, opacity=55, cap="round")
d.path(cr([T(p) for p in [(500, 322), (526, 336), (530, 372), (516, 402), (500, 408),
                          (484, 402), (470, 372), (474, 336)]]), "Thorax",
       fill=rad([(0, "#7A3E20"), (0.7, "#4A2410"), (1, "#2A1208")]), stroke=INK, strokeWidth=4)
d.path(cr([T((476, 340)), T((500, 332)), T((524, 340))], closed=False), "Collar",
       fill=NONE, stroke="#E8DCC0", strokeWidth=5, opacity=80, cap="round")
d.path(blob(494, 362, 13, 20, T), "Thorax sheen", fill="#FFE2C0", opacity=16, stroke=NONE)
d.path(blob(500, 316, 14, 10, T), "Head", fill=rad([(0, "#6A3418"), (1, "#2E1408")]),
       stroke=INK, strokeWidth=3)
# eyes, on the head in transformed space
for sgn in (-1, 1):
    ex, ey = T((500 + sgn * 6, 311))
    d.shape("ellipse", f"Eye {'L' if sgn<0 else 'R'}", x=ex - 3.5, y=ey - 4,
            width=7, height=8, fill="#0C0604", stroke=NONE)

# --- slim feathered antennae (day moth: fine, not a fan) --------------------------------------
def quad(p0, p1, p2, t):
    u = 1 - t
    return ((u * u * p0[0] + 2 * u * t * p1[0] + t * t * p2[0],
             u * u * p0[1] + 2 * u * t * p1[1] + t * t * p2[1]),
            (2 * u * (p1[0] - p0[0]) + 2 * t * (p2[0] - p1[0]),
             2 * u * (p1[1] - p0[1]) + 2 * t * (p2[1] - p1[1])))


A0, A1, A2 = (505, 308), (520, 258), (558, 236)
for X, side in [(T, "R"), (Tm, "L")]:
    for k in range(11):
        t = 0.15 + 0.8 * k / 10
        (x, y), (tx, ty) = quad(A0, A1, A2, t)
        ln = math.hypot(tx, ty)
        ux, uy, nx, ny = tx / ln, ty / ln, -ty / ln, tx / ln
        L = 10 * (1 - 0.5 * t)
        for sgn in (1, -1):
            d.path("M%s L%s" % (F(X((x, y))), F(X((x + sgn * nx * L + ux * L * 0.5,
                                                    y + sgn * ny * L + uy * L * 0.5)))),
                   f"Antenna {side} barb {k+1}{'ab'[sgn < 0]}", fill=NONE, stroke="#8A5A34",
                   strokeWidth=2.5, opacity=70, cap="round")
    d.path("M%s Q%s %s" % (F(X(A0)), F(X(A1)), F(X(A2))), f"Antenna {side}", fill=NONE,
           stroke="#4A2410", strokeWidth=3.5, cap="round")

# --- legs gripping the leaf -------------------------------------------------------------------
for sgn in (-1, 1):
    for k, (x0, y0, x1, y1) in enumerate([(478, 470, 440, 560), (486, 490, 470, 580),
                                          (494, 500, 508, 588)]):
        sx = 500 + sgn * (x0 - 500); ex = 500 + sgn * (x1 - 500)
        d.path(f"M{sx},{y0} L{ex},{y1}", f"Leg {sgn}.{k+1}", fill=NONE,
               stroke="#2A140C", strokeWidth=3, opacity=80, cap="round")

# --- captions -----------------------------------------------------------------------------------
d.text("SUNSET MOTH", "Name", x=500, y=930, size=58, font="Virelai Sans",
       color="#E4EFD8", justify="center")
d.text("L E P I D O P T E R A", "Order", x=500, y=970, size=22, font="Virelai Sans",
       color="#A0C9A8", justify="center")

d.finish("madagascan-sunset-moth-V1R00")
