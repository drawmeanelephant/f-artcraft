#!/usr/bin/env python3
"""Atlas moth — field plate V1R00. Full dorsal spread of Attacus atlas: rust
wings mapped with pale cream banding, a translucent window cut clean through
each wing, and forewing tips curled into cobra heads (the mimicry is the
point). Deep emerald plate. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Atlas Moth — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#2E140C"   # warm umber, not black


def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad


def F(p):
    return "%.1f,%.1f" % p


def cr(pts, closed=True):
    """Catmull-Rom spline through pts as cubic Beziers."""
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


# the moth is drawn on its right half in "raw" space, then scaled onto the disc;
# the left half is the mirror image
S, OY = 0.92, 452
def T(p):
    return (500 + S * (p[0] - 500), OY + S * (p[1] - 440))
def Tm(p):
    q = T(p)
    return (1000 - q[0], q[1])
def ident(p):
    return p


BG_GRAD = lin((0, 0), (0, 1000), [(0, "#0A2219"), (1, "#020A07")])
PLATE_GRAD = rad([(0, "#2F8C69"), (0.62, "#1B5F47"), (1, "#0C3527")])

# --- backdrop + plate ----------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876, fill="#2F8C69", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840, fill=PLATE_GRAD,
        stroke="#06201A", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792, fill=NONE,
        stroke="#9EE0BE", strokeWidth=3, opacity=28)


def rim(theta):
    t = math.radians(theta)
    return (PCX + PR * math.cos(t), PCY + PR * math.sin(t))


# contour-map hills rising from the lower rim: fills close on the disc's own arc,
# contour lines stop just inside it
def rim_in(theta, inset):
    t = math.radians(theta)
    return (PCX + (PR - inset) * math.cos(t), PCY + (PR - inset) * math.sin(t))


for h, (tc, spans, peaks) in enumerate([(122, (30, 22, 14), (600, 668, 730)),
                                        (58, (30, 22, 14), (600, 668, 730))]):
    for k, (hs, py) in enumerate(zip(spans, peaks)):
        a, b = rim(tc - hs), rim(tc + hs)
        px = (a[0] + b[0]) / 2
        c1 = (b[0] + (px - b[0]) * 0.25, py)
        c2 = (a[0] + (px - a[0]) * 0.25, py)
        d.path("M%s C%s %s %s A420,420 0 0 1 %s Z" % (F(b), F(c1), F(c2), F(a), F(b)),
               f"Hill {h+1} tier {k+1}", fill="#7CCBA2", opacity=7, stroke=NONE)
        ai, bi = rim_in(tc - hs, 8), rim_in(tc + hs, 8)
        d.path("M%s C%s %s %s" % (F(bi), F(c1), F(c2), F(ai)), f"Hill {h+1} contour {k+1}",
               fill=NONE, stroke="#8AD6AE", strokeWidth=3, opacity=24, cap="round")
for i, (x, y, w) in enumerate([(180, 330, 6), (820, 300, 5), (150, 500, 6), (860, 470, 5),
                               (420, 100, 5), (600, 96, 6), (300, 150, 4), (700, 160, 5),
                               (240, 250, 4), (770, 230, 4), (130, 420, 4), (880, 560, 4)]):
    assert on_disc(x, y, 12), (x, y)
    d.shape("ellipse", f"Pollen {i+1}", x=x, y=y, width=w, height=w, fill="#F4E8C8",
            opacity=35, stroke=NONE)

# --- wing geometry (raw, right side) ------------------------------------------------
FORE = [(512, 318), (560, 286), (640, 248), (720, 222), (790, 208), (838, 204), (868, 220),
        (880, 246), (868, 266), (846, 273), (824, 278), (806, 302), (796, 334), (770, 372),
        (730, 404), (690, 424), (640, 426), (580, 416), (518, 398)]
FORE_WIN = [(670, 300), (716, 284), (706, 312), (690, 338)]
HIND = [(514, 392), (580, 410), (660, 430), (730, 458), (772, 502), (778, 556), (750, 610),
        (698, 646), (632, 660), (578, 642), (542, 602), (522, 542), (510, 470)]
HIND_WIN = [(634, 500), (664, 492), (660, 520), (646, 546), (638, 528)]

for pts, lbl in [(FORE, "fore"), (HIND, "hind")]:
    for p in pts:
        assert on_disc(*T(p), 14), (lbl, T(p))


def fore_grad(X):
    return lin(X((520, 360)), X((870, 240)),
               [(0, "#561C10"), (0.32, "#8E3620"), (0.62, "#BC5C34"), (1, "#D8904E")])


def hind_grad(X):
    return lin(X((515, 430)), X((760, 650)),
               [(0, "#561C10"), (0.4, "#9C3E24"), (1, "#C86C3C")])


def stroke(X, pts, label, color, w, op=100):
    return pid(d.path(cr([X(p) for p in pts], closed=False), label, fill=NONE, stroke=color,
                      strokeWidth=w, opacity=op, cap="round"))


def wavy(pts, amp, n):
    """Resample a polyline by arc length and kick alternate samples sideways."""
    segs = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:])]
    total, out = sum(segs), []
    for k in range(n + 1):
        s, i = total * k / n, 0
        while i < len(segs) - 1 and s > segs[i]:
            s -= segs[i]
            i += 1
        a, b = pts[i], pts[i + 1]
        f = min(1.0, s / segs[i])
        ux, uy = (b[0] - a[0]) / segs[i], (b[1] - a[1]) / segs[i]
        o = amp * (1 if k % 2 else -1) * (0 if k in (0, n) else 1)
        out.append((a[0] + (b[0] - a[0]) * f - uy * o, a[1] + (b[1] - a[1]) * f + ux * o))
    return out


def band(X, pts, label):
    """Pale cream band with a dark inner border and a pink outer one."""
    ids = [stroke(X, [(x - 9, y) for x, y in pts], label + " dark edge", "#2A100A", 5, 80),
           stroke(X, pts, label, "#F4E6CC", 12, 90),
           stroke(X, [(x + 9, y) for x, y in pts], label + " pink edge", "#E9A898", 4, 75)]
    return ids


def veins(X, base, tips, label, w=3):
    ids = []
    for k, (tx, ty) in enumerate(tips):
        mx, my = (base[0] + tx) / 2, (base[1] + ty) / 2
        ids.append(stroke(X, [base, (mx + (ty - base[1]) * 0.06, my - (tx - base[0]) * 0.06), (tx, ty)],
                          f"{label} vein {k+1}", "#341208", w, 72))
    return ids


def fore_patterns(X, side):
    L = f"Forewing {side}"
    ids = [pid(d.path(blob(548, 352, 60, 70, X), L + " basal shade", fill="#3E140A", opacity=45, stroke=NONE)),
           pid(d.path(blob(790, 300, 70, 60, X), L + " lilac field", fill="#C8A0A0", opacity=30, stroke=NONE))]
    # map contours in the outer field
    for k, inset in enumerate([46, 66]):
        ids.append(stroke(X, [(790 - inset * 0.3, 230 + inset), (770 - inset * 0.6, 330),
                              (728 - inset * 0.5, 392 - inset * 0.3), (650, 418 - inset * 0.4)],
                          f"{L} contour {k+1}", "#F6E2C4", 3, 24))
    ids += veins(X, (526, 352), [(640, 252), (720, 226), (790, 214), (800, 312), (780, 356),
                                 (742, 396), (694, 420), (620, 424)], L)
    ids += band(X, [(646, 230), (614, 290), (604, 350), (612, 404), (606, 440)], L + " band")
    # submarginal band + its dark wavy line
    ids.append(stroke(X, [(806, 300), (790, 338), (762, 374), (724, 404), (684, 420), (630, 424)],
                      L + " submarginal", "#E6C088", 18, 65))
    ids.append(stroke(X, wavy([(784, 330), (764, 362), (734, 390), (696, 408), (650, 414)], 4, 16),
                      L + " wavy line", "#3A160C", 3, 75))
    # cobra head: ochre crown, dark eye, mouth, pink throat
    ids.append(pid(d.path(blob(846, 238, 42, 34, X), L + " head",
                          fill=rad([(0, "#F4CC6A"), (0.7, "#E0A24A"), (1, "#C07A30")]), stroke=NONE)))
    ids.append(pid(d.path(blob(812, 262, 22, 16, X), L + " throat", fill="#E9A898", opacity=55, stroke=NONE)))
    ids.append(stroke(X, [(790, 214), (820, 222), (846, 226)], L + " brow", "#7A2E18", 6, 80))
    ids.append(stroke(X, [(878, 254), (860, 258), (838, 256)], L + " mouth", "#2A100A", 4, 90))
    ids.append(pid(d.path(blob(850, 236, 7.5, 6.5, X), L + " eye", fill="#1E0C08", stroke=NONE)))
    ids.append(pid(d.path(blob(848, 234, 2.4, 2.2, X), L + " eye glint", fill="#FFF4E0", opacity=85, stroke=NONE)))
    return ids


def hind_patterns(X, side):
    L = f"Hindwing {side}"
    ids = [pid(d.path(blob(540, 460, 44, 70, X), L + " basal shade", fill="#3E140A", opacity=45, stroke=NONE))]
    ids += veins(X, (522, 440), [(600, 414), (680, 436), (750, 480), (772, 540), (750, 606),
                                 (700, 642), (630, 656), (566, 630)], L)
    for k, inset in enumerate([40, 58]):
        ids.append(stroke(X, [(760 - inset, 500), (762 - inset, 556), (736 - inset, 604 - inset * 0.3),
                              (690 - inset * 0.6, 636 - inset * 0.6)],
                          f"{L} contour {k+1}", "#F6E2C4", 3, 24))
    ids += band(X, [(612, 416), (604, 470), (600, 540), (612, 604), (640, 664)], L + " band")
    ids.append(stroke(X, [(724, 456), (758, 504), (760, 556), (734, 606), (690, 636), (630, 648)],
                      L + " submarginal", "#E6C088", 20, 65))
    ids.append(stroke(X, wavy([(712, 464), (742, 506), (744, 556), (722, 598), (684, 624), (634, 636)], 4, 20),
                      L + " wavy line", "#3A160C", 3, 75))
    for k, (x, y) in enumerate([(766, 528), (762, 576), (738, 614), (700, 640), (654, 652)]):
        ids.append(pid(d.path(blob(x, y, 6, 4.5, X), f"{L} margin spot {k+1}", fill="#2A100A",
                              opacity=60, stroke=NONE)))
    return ids


def wing(label, raw, raw_win, grad, X, patterns, side):
    wd, hd = cr([X(p) for p in raw]), cr([X(p) for p in raw_win])
    w = pid(d.path(wd, label, fill=grad, stroke=NONE, opacity=92))
    h = pid(d.path(hd, label + " window cut", fill="#000000", stroke=NONE))
    r = d.call("pathfinder", {"operation": "minusFront", "ids": [w, h]}, label + " cut window")
    w = r["ids"][0]
    d.call("set_paint", {"ids": [w], "stroke": "none"}, label + " no stroke")
    ids = [w] + [i for i in patterns(X, side) if i]
    m1 = pid(d.path(wd, label + " mask", fill="#000000", stroke=NONE))
    m2 = pid(d.path(hd, label + " mask window", fill="#000000", stroke=NONE))
    m = d.call("pathfinder", {"operation": "minusFront", "ids": [m1, m2]}, label + " mask cut")
    d.cmd("object.clippingMask.make", label + " clip", ids=ids + [m["ids"][0]])
    # window: a faint glaze so the plate reads through, dark rim, cream inner rim
    d.path(hd, label + " window glaze", fill={"gradient": {"kind": "radial", "stops": [
        {"offset": 0, "color": "#FFF6E4", "opacity": 0.05},
        {"offset": 1, "color": "#FFF6E4", "opacity": 0.28}]}}, stroke=NONE)
    d.path(hd, label + " window rim", fill=NONE, stroke="#F2D9A8", strokeWidth=7, opacity=70)
    d.path(hd, label + " window edge", fill=NONE, stroke=INK, strokeWidth=3)
    d.path(wd, label + " outline", fill=NONE, stroke=INK, strokeWidth=4, opacity=90)


# --- cast shadow -----------------------------------------------------------------------
for X, side in [(T, "R"), (Tm, "L")]:
    for raw, nm in [(HIND, "hind"), (FORE, "fore")]:
        d.path(cr([(x + 8, y + 16) for x, y in (X(p) for p in raw)]), f"Shadow {nm} {side}",
               fill="#021810", opacity=30, stroke=NONE)

# --- wings: hind under fore -------------------------------------------------------------
for X, side in [(T, "R"), (Tm, "L")]:
    wing(f"Hindwing {side}", HIND, HIND_WIN, hind_grad(X), X, hind_patterns, side)
for X, side in [(T, "R"), (Tm, "L")]:
    wing(f"Forewing {side}", FORE, FORE_WIN, fore_grad(X), X, fore_patterns, side)

# --- body ------------------------------------------------------------------------------
ABD = [(500, 376), (524, 390), (530, 440), (520, 492), (500, 524), (480, 492), (470, 440), (476, 390)]
d.path(cr([T(p) for p in ABD]), "Abdomen",
       fill=lin(T((470, 0)), T((530, 0)), [(0, "#6A2A16"), (0.5, "#B05A32"), (1, "#5A2212")]),
       stroke=INK, strokeWidth=4)
for k, y in enumerate([404, 428, 452, 476, 498]):
    hw = {404: 26, 428: 28, 452: 27, 476: 22, 498: 14}[y]
    d.path(cr([T((500 - hw, y - 3)), T((500, y + 4)), T((500 + hw, y - 3))], closed=False),
           f"Abdomen band {k+1}", fill=NONE, stroke="#F4E6CC", strokeWidth=3, opacity=60, cap="round")
d.path(cr([T(p) for p in [(500, 312), (528, 326), (532, 360), (518, 392), (500, 398),
                          (482, 392), (468, 360), (472, 326)]]), "Thorax",
       fill=rad([(0, "#C2683A"), (0.7, "#8E3820"), (1, "#5E2010")]), stroke=INK, strokeWidth=4)
d.path(cr([T((474, 330)), T((500, 322)), T((526, 330))], closed=False), "Collar",
       fill=NONE, stroke="#F4E6CC", strokeWidth=6, opacity=85, cap="round")
d.path(blob(494, 350, 14, 22, T), "Thorax sheen", fill="#FFE2C0", opacity=18, stroke=NONE)
for k, (x0, y0, x1, y1) in enumerate([(482, 372, 476, 388), (500, 378, 500, 394), (518, 372, 524, 388)]):
    d.path("M%s L%s" % (F(T((x0, y0))), F(T((x1, y1)))), f"Thorax tuft {k+1}", fill=NONE,
           stroke="#D88A58", strokeWidth=3, opacity=50, cap="round")
d.path(blob(500, 306, 15, 11, T), "Head", fill=rad([(0, "#A84E2C"), (1, "#5A2010")]),
       stroke=INK, strokeWidth=3)


# --- feathered antennae -------------------------------------------------------------------
def quad(p0, p1, p2, t):
    u = 1 - t
    return ((u * u * p0[0] + 2 * u * t * p1[0] + t * t * p2[0],
             u * u * p0[1] + 2 * u * t * p1[1] + t * t * p2[1]),
            (2 * u * (p1[0] - p0[0]) + 2 * t * (p2[0] - p1[0]),
             2 * u * (p1[1] - p0[1]) + 2 * t * (p2[1] - p1[1])))


A0, A1, A2 = (506, 300), (518, 252), (566, 232)
for X, side in [(T, "R"), (Tm, "L")]:
    for k in range(14):
        t = 0.12 + 0.82 * k / 13
        (x, y), (tx, ty) = quad(A0, A1, A2, t)
        ln = math.hypot(tx, ty)
        ux, uy, nx, ny = tx / ln, ty / ln, -ty / ln, tx / ln
        L = 15 * (1 - 0.55 * t)
        for sgn in (1, -1):
            d.path("M%s L%s" % (F(X((x, y))), F(X((x + sgn * nx * L + ux * L * 0.5,
                                                    y + sgn * ny * L + uy * L * 0.5)))),
                   f"Antenna {side} barb {k+1}{'ab'[sgn < 0]}", fill=NONE, stroke="#B0683C",
                   strokeWidth=3, opacity=70, cap="round")
    d.path("M%s Q%s %s" % (F(X(A0)), F(X(A1)), F(X(A2))), f"Antenna {side}", fill=NONE,
           stroke="#6A2E16", strokeWidth=4, cap="round")

# --- captions ---------------------------------------------------------------------------
d.text("ATLAS MOTH", "Name", x=500, y=930, size=58, font="Virelai Sans",
       color="#DDF2E6", justify="center")
d.text("L E P I D O P T E R A", "Order", x=500, y=970, size=22, font="Virelai Sans",
       color="#93C9AE", justify="center")

d.finish("atlas-moth-V1R00")
