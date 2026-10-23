#!/usr/bin/env python3
"""Glass frog — field plate V1R00. Portrait from slightly below of
Hyalinobatrachium fleischmanni on a leaf above a night creek: lime back, a
belly of glass that lets the leaf ribs read through it, the white heart sac
and silver viscera inside, gold eyes with horizontal pupils. Leaf ribs and a
fern frond frame it. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Glass Frog — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#1C3326"   # deep moss, not black

def on_disc(x, y, pad):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

def lin(c0, c1, start=None, end=None, o0=None, o1=None):
    s0 = {"offset": 0, "color": c0}; s1 = {"offset": 1, "color": c1}
    if o0 is not None: s0["opacity"] = o0
    if o1 is not None: s1["opacity"] = o1
    g = {"kind": "linear", "stops": [s0, s1]}
    if start: g["start"], g["end"] = start, end
    return {"gradient": g}

def rad(*stops):
    n = len(stops) - 1
    return {"gradient": {"kind": "radial", "stops": [
        {"offset": round(i / n, 3), "color": c} for i, c in enumerate(stops)]}}

def smooth(pts, closed=True, k=1.0):
    """Catmull-Rom through pts as cubic Beziers."""
    n = len(pts)
    s = "M%.1f,%.1f" % pts[0]
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        p0 = pts[(i - 1) % n] if (closed or i > 0) else pts[0]
        p1, p2 = pts[i], pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (closed or i + 2 < n) else pts[-1]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6 * k, p1[1] + (p2[1] - p0[1]) / 6 * k)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6 * k, p2[1] - (p3[1] - p1[1]) / 6 * k)
        s += " C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (c1 + c2 + p2)
    return s + (" Z" if closed else "")

def mirror(right):
    """Right half listed top->bottom on the axis ends -> full closed outline."""
    left = [(2 * PCX - x, y) for x, y in reversed(right[1:-1])]
    return right + left

def quad(p0, p1, p2, t):
    u = 1 - t
    return (u*u*p0[0] + 2*u*t*p1[0] + t*t*p2[0], u*u*p0[1] + 2*u*t*p1[1] + t*t*p2[1]), \
           (2*u*(p1[0]-p0[0]) + 2*t*(p2[0]-p1[0]), 2*u*(p1[1]-p0[1]) + 2*t*(p2[1]-p1[1]))

BG_GRAD = lin("#0B1A1E", "#03080B", [0, 0], [0, 1000])
PLATE_GRAD = rad("#2F5E57", "#1A3E3C", "#0C2226")
LEAF_GRAD = lin("#3E8A3A", "#1D4E28", [300, 300], [700, 640])
SKIN_GRAD = rad("#E4F6C8", "#BDE59A", "#8CC46A")
BACK_GRAD = rad("#C8EC6A", "#98CC3E", "#5E9828")
EYE_GRAD = rad("#FFF2B8", "#F2C64A", "#C08A1E", "#7A5210")
WATER_GRAD = lin("#1E4A50", "#081A20", [0, 740], [0, 880])

# --- backdrop + plate -----------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876, fill="#4E8C7A", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840, fill=PLATE_GRAD, stroke=NONE)
# moon glow, upper right
d.shape("ellipse", "Moon glow", x=600, y=90, width=240, height=240,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#E8F4D8", "opacity": 0.32},
            {"offset": 1, "color": "#E8F4D8", "opacity": 0}]}}, stroke=NONE)

# --- night creek: water band closed on the disc arc --------------------------------
WY = 742
wx = math.sqrt(PR**2 - (WY - PCY)**2)
d.path(f"M{PCX - wx:.1f},{WY} L{PCX + wx:.1f},{WY} A420,420 0 0 1 {PCX - wx:.1f},{WY} Z",
       "Creek", fill=WATER_GRAD, stroke=NONE)
d.path(f"M{PCX - wx:.1f},{WY} L{PCX + wx:.1f},{WY}", "Creek bank light",
       fill=NONE, stroke="#9CD0C0", strokeWidth=3, opacity=30, cap="round")
for i, (cx, cy, w) in enumerate([(380, 772, 220), (620, 790, 200), (470, 818, 280),
                                 (600, 838, 120), (440, 846, 100), (510, 862, 100)]):
    assert on_disc(cx - w / 2, cy, 8) and on_disc(cx + w / 2, cy, 8), (cx, cy)
    d.path(f"M{cx - w/2},{cy} Q{cx},{cy - 7} {cx + w/2},{cy}", f"Ripple {i+1}",
           fill=NONE, stroke="#BFE6D8", strokeWidth=3, opacity=22 + (i % 3) * 6, cap="round")
# moon reflection on the water
for i, (cx, cy, w) in enumerate([(650, 760, 70), (658, 778, 46), (646, 800, 58), (652, 822, 30)]):
    assert on_disc(cx + w / 2, cy, 10), (cx, cy)
    d.path(f"M{cx - w/2},{cy} L{cx + w/2},{cy}", f"Moon glitter {i+1}",
           fill=NONE, stroke="#F2F6DA", strokeWidth=4, opacity=40, cap="round")

# --- fern frond, arching up the left side -----------------------------------------
F0, F1, F2 = (236, 712), (150, 420), (352, 150)
d.path(f"M{F0[0]},{F0[1]} Q{F1[0]},{F1[1]} {F2[0]},{F2[1]}", "Fern rachis",
       fill=NONE, stroke="#3C7A40", strokeWidth=5, cap="round")
NP = 22
for j in range(1, NP):
    t = j / NP
    (x, y), (tx, ty) = quad(F0, F1, F2, t)
    ln = math.hypot(tx, ty)
    ux, uy = tx / ln, ty / ln
    L = 58 * math.sin(math.pi * (0.15 + 0.85 * t)) * (1.15 - 0.5 * t) + 10
    for side in (1, -1):
        nx, ny = -uy * side, ux * side
        # pinna sweeps forward toward the frond tip
        tipx, tipy = x + (nx * 0.86 + ux * 0.5) * L, y + (ny * 0.86 + uy * 0.5) * L
        assert on_disc(tipx, tipy, 14), (j, side, tipx, tipy)
        w = 6 + 5 * (1 - t)
        bx, by = x + ux * w, y + uy * w
        midx, midy = (x + tipx) / 2, (y + tipy) / 2
        d.path(f"M{x - ux*w*0.6:.1f},{y - uy*w*0.6:.1f} Q{midx - ux*w + nx*2:.1f},{midy - uy*w + ny*2:.1f} "
               f"{tipx:.1f},{tipy:.1f} Q{midx + ux*w*1.2:.1f},{midy + uy*w*1.2:.1f} {bx:.1f},{by:.1f} Z",
               f"Fern pinna {j}{'a' if side > 0 else 'b'}",
               fill=lin("#5FAA4E", "#2C6A34"), stroke=NONE, opacity=88 if side > 0 else 72)

# --- the leaf: broad blade on a diagonal, midrib + lateral ribs ---------------------
LB, LT = (236, 712), (806, 222)          # base, tip
ax_, ay_ = LT[0] - LB[0], LT[1] - LB[1]
LL = math.hypot(ax_, ay_)
ux_, uy_ = ax_ / LL, ay_ / LL
nx_, ny_ = -uy_, ux_                     # points down-right of the axis
HALF = 190
def leaf_pt(s, side, shrink=1.0):
    """s along the axis 0..1, side +1/-1; width follows a leaf profile."""
    w = HALF * shrink * (math.sin(math.pi * s ** 0.85) ** 0.9)
    bow = 22 * math.sin(math.pi * s)      # gentle curl of the axis
    x = LB[0] + ax_ * s + nx_ * (side * w - bow)
    y = LB[1] + ay_ * s + ny_ * (side * w - bow)
    return (x, y)
upper = [leaf_pt(i / 20, -1) for i in range(21)]
lower = [leaf_pt(i / 20, 1) for i in range(20, -1, -1)]
for x, y in upper + lower:
    assert on_disc(x, y, 10), (x, y)
outline = upper + lower[1:-1]
d.path(smooth(outline), "Leaf", fill=LEAF_GRAD, stroke="#173D22", strokeWidth=4)
# shade on the far half, sheen near the midrib
shade = [leaf_pt(i / 20, -1) for i in range(21)] + [leaf_pt(i / 20, 0) for i in range(19, 0, -1)]
d.path(smooth(shade), "Leaf far shade", fill="#0E2A18", opacity=30, stroke=NONE)
mid = [leaf_pt(i / 20, 0) for i in range(21)]
d.path(smooth(mid, closed=False), "Leaf midrib", fill=NONE, stroke="#A6D88A", strokeWidth=6, opacity=70, cap="round")
d.path(smooth(mid, closed=False), "Leaf midrib core", fill=NONE, stroke="#E2F6C8", strokeWidth=3, opacity=50, cap="round")
for k in range(1, 9):
    s = 0.06 + k * 0.105
    for side in (-1, 1):
        p0 = leaf_pt(s, 0)
        p2 = leaf_pt(min(s + 0.13, 0.98), side, 0.9)
        p1 = leaf_pt(s + 0.03, side, 0.55)
        d.path(f"M{p0[0]:.1f},{p0[1]:.1f} Q{p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}",
               f"Leaf rib {k}{'a' if side > 0 else 'b'}", fill=NONE, stroke="#9ED080",
               strokeWidth=3, opacity=45 if side > 0 else 32, cap="round")
# leaf rim light along the moonlit edge
d.path(smooth(upper[3:18], closed=False), "Leaf rim light", fill=NONE, stroke="#CFEFB0",
       strokeWidth=3, opacity=40, cap="round")
# dew beads on the leaf
for i, (x, y, r) in enumerate([(330, 610, 9), (700, 300, 7), (742, 360, 10), (392, 666, 6), (650, 250, 6)]):
    d.shape("ellipse", f"Dew {i+1}", x=x - r, y=y - r, width=2 * r, height=2 * r,
            fill=rad("#FFFFFF", "#CFEFD8", "#6FA88A"), opacity=70, stroke=NONE)
    d.shape("ellipse", f"Dew {i+1} glint", x=x - r * 0.5, y=y - r * 0.6, width=r * 0.6, height=r * 0.6,
            fill="#FFFFFF", opacity=90, stroke=NONE)

# --- frog ---------------------------------------------------------------------------------
def limb(name, pts, w, toe_w=0):
    s = smooth(pts, closed=False)
    d.path(s, f"{name} ink", fill=NONE, stroke=INK, strokeWidth=w + 6, cap="round", opacity=80)
    d.path(s, name, fill=NONE, stroke=lin("#D4EFB4", "#9ACB72"), strokeWidth=w, cap="round", opacity=92)
    d.path(s, f"{name} bone", fill=NONE, stroke="#F2FBE6", strokeWidth=3, cap="round", opacity=40)

def toes(name, root, angles, length, pad=9):
    for i, a in enumerate(angles):
        r = math.radians(a)
        tip = (root[0] + length * math.cos(r), root[1] + length * math.sin(r))
        s = f"M{root[0]:.1f},{root[1]:.1f} L{tip[0]:.1f},{tip[1]:.1f}"
        d.path(s, f"{name} toe {i+1} ink", fill=NONE, stroke=INK, strokeWidth=11, cap="round", opacity=80)
        d.path(s, f"{name} toe {i+1}", fill=NONE, stroke="#C8E8A4", strokeWidth=6, cap="round")
        d.shape("ellipse", f"{name} pad {i+1}", x=tip[0] - pad, y=tip[1] - pad, width=2 * pad, height=2 * pad,
                fill=rad("#F0FADC", "#C4E49A", "#8CBE64"), stroke=INK, strokeWidth=3)

# shadow of the frog on the leaf
d.path(smooth([(330, 640), (500, 600), (690, 640), (660, 720), (500, 735), (340, 710)]),
       "Frog shadow", fill="#0A2414", opacity=35, stroke=NONE)

# hind legs folded in the crouch: fat haunch with the knee up by the elbow,
# shin tucked down beside it, long-toed foot splayed on the leaf
for sgn in (1, -1):
    X = lambda x: PCX + sgn * (x - PCX)
    nm = "R" if sgn > 0 else "L"
    shin = smooth([(X(700), 566), (X(712), 618), (X(694), 668)], closed=False)
    d.path(shin, f"Shin {nm} ink", fill=NONE, stroke=INK, strokeWidth=36, cap="round", opacity=80)
    d.path(shin, f"Shin {nm}", fill=NONE, stroke=lin("#D4EFB4", "#9ACB72"), strokeWidth=30, cap="round")
    limb(f"Foot {nm}", [(X(690), 668), (X(722), 686), (X(750), 694)], 16)
    base_a = [12, 36, 62, 88] if sgn > 0 else [168, 144, 118, 92]
    toes(f"Hind {nm}", (X(750), 694), base_a, 38, 9)
    haunch = [(X(588), 548), (X(650), 526), (X(704), 540), (X(724), 576),
              (X(702), 620), (X(650), 652), (X(600), 660), (X(574), 616)]
    d.path(smooth(haunch), f"Haunch {nm}", fill=rad("#E2F6C6", "#B8E096", "#86BC64"),
           stroke=INK, strokeWidth=4, opacity=90)
    d.path(smooth([(X(612), 548), (X(668), 536), (X(708), 556)], closed=False), f"Haunch {nm} sheen",
           fill=NONE, stroke="#F6FFE6", strokeWidth=6, opacity=40, cap="round")
    d.path(smooth([(X(704), 560), (X(690), 604), (X(648), 632)], closed=False), f"Femur {nm}",
           fill=NONE, stroke="#F2FBE6", strokeWidth=4, opacity=30, cap="round")

# body: one translucent silhouette, head top included
BODY_R = [(500, 268), (556, 270), (624, 300), (664, 352), (668, 410), (648, 452),
          (640, 512), (626, 574), (596, 632), (548, 666), (500, 674)]
BODY = smooth(mirror(BODY_R))
d.path(BODY, "Body glass", fill=SKIN_GRAD, opacity=58, stroke=NONE)
# the leaf's midrib and ribs read through the glass belly: redraw them faintly on top
d.path(smooth([leaf_pt(i / 20, 0) for i in range(6, 13)], closed=False), "Midrib through glass",
       fill=NONE, stroke="#5E9A48", strokeWidth=5, opacity=35, cap="round")

# viscera, seen through the belly
d.path(smooth([(500, 560), (560, 548), (588, 590), (566, 636), (500, 650), (434, 636), (412, 590), (440, 548)]),
       "Viscera sac", fill=rad("#F6FAF4", "#D6E4D8", "#A8BCB0"), opacity=55, stroke="#FFFFFF", strokeWidth=3)
for i, s in enumerate(["M444,606 C450,578 492,570 506,590 C518,608 498,628 476,622",
                       "M556,580 C572,600 562,630 536,634 C512,638 500,620 512,606",
                       "M470,560 C496,552 530,556 548,572"]):
    d.path(s, f"Gut loop {i+1}", fill=NONE, stroke="#F4F8F2", strokeWidth=12, opacity=26, cap="round")
    d.path(s, f"Gut loop {i+1} shine", fill=NONE, stroke="#FFFFFF", strokeWidth=3, opacity=38, cap="round")
d.path(smooth([(436, 528), (470, 508), (500, 520), (480, 556), (440, 562)]),
       "Liver lobe L", fill=rad("#FFFFFF", "#E2ECE6", "#B8C8C0"), opacity=72, stroke=NONE)
d.path(smooth([(564, 528), (530, 508), (500, 520), (520, 556), (560, 562)]),
       "Liver lobe R", fill=rad("#FFFFFF", "#E2ECE6", "#B8C8C0"), opacity=72, stroke=NONE)
# the white heart sac, with the red heart faintly inside it
for i, s in enumerate(["M494,458 C488,450 480,447 472,448", "M508,457 C514,449 522,447 530,449"]):
    d.path(s, f"Great vessel {i+1}", fill=NONE, stroke="#FFFFFF", strokeWidth=10, opacity=70, cap="round")
d.path(smooth([(500, 452), (528, 456), (544, 478), (536, 506), (510, 526), (486, 518), (464, 494), (470, 466)]),
       "Heart sac", fill=rad("#FFFFFF", "#F4F6F2", "#D2DCD6"), stroke="#FFFFFF", strokeWidth=3, opacity=94)
d.path(smooth([(502, 466), (522, 472), (528, 492), (514, 510), (494, 508), (480, 490), (484, 472)]),
       "Heart", fill=rad("#F28A8A", "#D6545E", "#A83240"), opacity=50, stroke=NONE)
d.path("M482,476 C488,466 498,462 510,464", "Heart sac shine", fill=NONE, stroke="#FFFFFF",
       strokeWidth=4, opacity=80, cap="round")
# vessels: aortic arches + a few belly veins, translucent red
for i, s in enumerate(["M494,458 C482,440 460,432 438,436", "M506,458 C518,440 540,432 562,436",
                       "M488,520 C470,540 456,566 452,600", "M512,520 C530,540 544,566 548,600",
                       "M500,650 C500,656 500,660 500,664"]):
    d.path(s, f"Vessel {i+1}", fill=NONE, stroke="#D04A58", strokeWidth=3, opacity=45, cap="round")
# belly volume: soft shade low, glow high
d.path(smooth([(392, 612), (500, 650), (608, 612), (596, 636), (500, 672), (404, 636)]),
       "Belly shade", fill="#3E7A3A", opacity=28, stroke=NONE)
d.shape("ellipse", "Belly glow", x=420, y=440, width=160, height=70, fill="#FFFFFF", opacity=14, stroke=NONE)

# back: the lime dorsal skin wraps over the head top and shoulders
BACK_R = [(500, 268), (556, 270), (624, 300), (664, 352), (668, 404), (640, 420),
          (590, 410), (540, 418), (500, 422)]
d.path(smooth(mirror(BACK_R)), "Back", fill=BACK_GRAD, stroke=NONE, opacity=96)
for i, (x, y, r) in enumerate([(470, 296, 5), (532, 300, 6), (500, 330, 4), (446, 360, 5), (556, 362, 5),
                               (612, 340, 4), (388, 340, 4), (500, 368, 5), (640, 384, 4), (360, 386, 4),
                               (580, 394, 3), (420, 396, 3)]):
    d.shape("ellipse", f"Back spot {i+1}", x=x - r, y=y - r, width=2 * r, height=2 * r,
            fill=rad("#FFF6B0", "#E8D85A"), opacity=85, stroke=NONE)
d.path("M408,292 C460,276 540,276 592,292", "Back sheen", fill=NONE, stroke="#F4FFD0",
       strokeWidth=8, opacity=30, cap="round")
# mouth line where the back meets the glass throat
d.path("M342,404 C400,424 460,430 500,430 C540,430 600,424 658,404", "Mouth",
       fill=NONE, stroke=INK, strokeWidth=4, opacity=75, cap="round")
d.path(BODY, "Body outline", fill=NONE, stroke=INK, strokeWidth=4, opacity=70)
d.path(smooth([(372, 470), (360, 530), (374, 600), (414, 648)], closed=False), "Body rim light L",
       fill=NONE, stroke="#F0FFE0", strokeWidth=4, opacity=40, cap="round")

# front arms gripping the leaf
for sgn in (1, -1):
    X = lambda x: PCX + sgn * (x - PCX)
    nm = "R" if sgn > 0 else "L"
    limb(f"Upper arm {nm}", [(X(622), 456), (X(654), 494), (X(664), 532)], 26)
    limb(f"Forearm {nm}", [(X(664), 532), (X(644), 580), (X(606), 612)], 22)
    base_a = [30, 62, 94, 124] if sgn > 0 else [150, 118, 86, 56]
    toes(f"Hand {nm}", (X(604), 614), base_a, 32, 8)

# eyes: gold with dark reticulation and horizontal pupils
for sgn in (1, -1):
    ex, ey, er = PCX + sgn * 82, 300, 50
    nm = "R" if sgn > 0 else "L"
    d.shape("ellipse", f"Eye socket {nm}", x=ex - er - 8, y=ey - er - 4, width=2 * er + 16, height=2 * er + 12,
            fill=BACK_GRAD, stroke=INK, strokeWidth=4)
    d.shape("ellipse", f"Eye {nm}", x=ex - er, y=ey - er, width=2 * er, height=2 * er,
            fill=EYE_GRAD, stroke=INK, strokeWidth=4)
    for j in range(14):
        a = j * 2.4 + 0.3
        rr = er * (0.35 + 0.5 * ((j * 37) % 11) / 11)
        d.shape("ellipse", f"Eye {nm} fleck {j+1}", x=ex + rr * math.cos(a) - 3, y=ey + rr * math.sin(a) - 3,
                width=6, height=6, fill="#6A4410", opacity=45, stroke=NONE)
    d.shape("ellipse", f"Pupil {nm}", x=ex - 30, y=ey - 11, width=60, height=22,
            fill=rad("#2A1E14", "#0E0A08"), stroke=NONE)
    d.shape("ellipse", f"Eye {nm} glint", x=ex - 26 + sgn * 4, y=ey - 34, width=18, height=12,
            fill="#FFFFFF", opacity=85, stroke=NONE)
    d.shape("ellipse", f"Eye {nm} glint 2", x=ex + 14, y=ey + 16, width=7, height=7,
            fill="#FFFFFF", opacity=55, stroke=NONE)
    d.path(f"M{ex - er + 6},{ey + 22} Q{ex},{ey + er + 8} {ex + er - 6},{ey + 22}",
           f"Eye {nm} lower lid", fill=NONE, stroke="#E8F8D0", strokeWidth=4, opacity=55, cap="round")
d.shape("ellipse", "Nostril L", x=478, y=372, width=8, height=6, fill=INK, opacity=60, stroke=NONE)
d.shape("ellipse", "Nostril R", x=514, y=372, width=8, height=6, fill=INK, opacity=60, stroke=NONE)

# fireflies over the creek
for i, (x, y) in enumerate([(220, 520), (790, 560), (268, 300), (760, 470), (612, 140)]):
    assert on_disc(x, y, 24)
    d.shape("ellipse", f"Firefly {i+1} halo", x=x - 14, y=y - 14, width=28, height=28,
            fill={"gradient": {"kind": "radial", "stops": [
                {"offset": 0, "color": "#F4F08A", "opacity": 0.55},
                {"offset": 1, "color": "#F4F08A", "opacity": 0}]}}, stroke=NONE)
    d.shape("ellipse", f"Firefly {i+1}", x=x - 3, y=y - 3, width=6, height=6, fill="#FFFBD0", stroke=NONE)

# plate rim drawn last so everything inside closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840, fill=NONE, stroke="#081614", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#BFE6C8", strokeWidth=3, opacity=28)

# --- name + second line -----------------------------------------------------------------
d.text("GLASS FROG", "Name", x=500, y=940, size=58, font="Virelai Sans", color="#DDF2D6", justify="center")
LINE2, SZ2, TRK = "HYALINOBATRACHIUM FLEISCHMANNI", 22, 200
r = d.text(LINE2, "Second line", x=500, y=975, size=SZ2, font="Virelai Sans", color="#9CC8AE", justify="center")
d.cmd("text.setStyle", "Second line tracking", id=r["id"], tracking=TRK)
def find(o, oid):
    if isinstance(o, dict):
        if o.get("id") == oid and "bounds" in o: return o
        o = list(o.values())
    if isinstance(o, list):
        for v in o:
            hit = find(v, oid)
            if hit: return hit
b2 = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("second line bounds", {k: round(v) for k, v in b2.items()})
assert b2["width"] <= 760 and b2["x"] >= 100 and b2["y"] + b2["height"] <= 990, b2

d.finish("glass-frog-V1R00")
