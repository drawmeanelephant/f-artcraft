#!/usr/bin/env python3
"""Kiwi — field plate V1R00. Apteryx mantelli in full profile, facing left,
round and wingless, the long ivory bill angled down and probing the soil,
rictal bristles fanned at its base, one ear tuft, and a coat of hair-like
feathers laid as hundreds of soft brown strands over a gradient body. Mossy
plate with faint flowing raki lines. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Kiwi — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#2E2014"   # dark peat, not black
rng = random.Random(55)

def on_disc(x, y, pad):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

def disc_x(y, side):
    return PCX + side * math.sqrt(PR**2 - (y - PCY)**2)

def lin(c0, c1, start=None, end=None):
    g = {"kind": "linear", "stops": [{"offset": 0, "color": c0}, {"offset": 1, "color": c1}]}
    if start: g["start"], g["end"] = [round(v, 1) for v in start], [round(v, 1) for v in end]
    return {"gradient": g}

def rad(*stops):
    n = len(stops) - 1
    return {"gradient": {"kind": "radial", "stops": [
        {"offset": round(i / n, 3), "color": c} for i, c in enumerate(stops)]}}

def smooth(pts, closed=True, k=1.0):
    n = len(pts)
    s = "M%.1f,%.1f" % pts[0]
    for i in (range(n) if closed else range(n - 1)):
        p0 = pts[(i - 1) % n] if (closed or i > 0) else pts[0]
        p1, p2 = pts[i], pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (closed or i + 2 < n) else pts[-1]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6 * k, p1[1] + (p2[1] - p0[1]) / 6 * k)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6 * k, p2[1] - (p3[1] - p1[1]) / 6 * k)
        s += " C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (c1 + c2 + p2)
    return s + (" Z" if closed else "")

def qpt(p0, p1, p2, t):
    u = 1 - t
    return (u*u*p0[0] + 2*u*t*p1[0] + t*t*p2[0], u*u*p0[1] + 2*u*t*p1[1] + t*t*p2[1])

def qtan(p0, p1, p2, t):
    u = 1 - t
    return (2*u*(p1[0]-p0[0]) + 2*t*(p2[0]-p1[0]), 2*u*(p1[1]-p0[1]) + 2*t*(p2[1]-p1[1]))

def inside(poly, x, y):
    c = False
    for (x1, y1), (x2, y2) in zip(poly, poly[1:] + poly[:1]):
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
            c = not c
    return c

BG_GRAD = lin("#101A10", "#040804", [0, 0], [0, 1000])
PLATE_GRAD = rad("#5A7A40", "#38542C", "#1C2C18")
SOIL_GRAD = lin("#4A3420", "#22160C", [0, 700], [0, 880])
BODY_GRAD = rad("#C8A06A", "#94683E", "#5A3C20")
BILL_GRAD = lin("#F2E6D0", "#B8987A", (300, 486), (200, 700))
LEG_GRAD = lin("#E2D2C2", "#9C8A7A", (0, 620), (0, 720))

# --- backdrop + plate ------------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876, fill="#7A9A5A", opacity=7, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840, fill=PLATE_GRAD, stroke=NONE)
d.shape("ellipse", "Moon glow", x=280, y=70, width=440, height=300,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#E6F0C8", "opacity": 0.20},
            {"offset": 1, "color": "#E6F0C8", "opacity": 0}]}}, stroke=NONE)

# raki lines: faint flowing contours across the plate, ends kept inside the rim
for i in range(11):
    y = 110 + i * 54
    xl, xr = disc_x(y, -1) + 26, disc_x(y, 1) - 26
    n = 8
    pts = []
    for k in range(n + 1):
        x = xl + (xr - xl) * k / n
        pts.append((x, y + 14 * math.sin(k * 0.9 + i * 0.7) + 6 * math.sin(k * 2.1 + i)))
    assert all(on_disc(px, py, 12) for px, py in pts), i
    d.path(smooth(pts, closed=False), f"Raki line {i+1}", fill=NONE, stroke="#C8DCA8",
           strokeWidth=3, opacity=8 if i % 2 else 11, cap="round")

# --- forest floor: soil closed on the disc arc, moss along its lip ---------------------------
GY = 700
gx = math.sqrt(PR**2 - (GY - PCY)**2)
d.path(f"M{PCX - gx:.1f},{GY} Q{PCX},{GY - 22} {PCX + gx:.1f},{GY} A420,420 0 0 1 {PCX - gx:.1f},{GY} Z",
       "Soil", fill=SOIL_GRAD, stroke=NONE)
for i in range(30):
    x, y = rng.uniform(170, 830), rng.uniform(724, 860)
    if not on_disc(x, y, 18): continue
    a = rng.uniform(0, math.pi)
    L = rng.uniform(14, 26)
    d.path(f"M{x - L/2 * math.cos(a):.1f},{y - L/4 * math.sin(a):.1f} Q{x:.1f},{y - 6:.1f} "
           f"{x + L/2 * math.cos(a):.1f},{y + L/4 * math.sin(a):.1f}", f"Leaf litter {i+1}", fill=NONE,
           stroke=rng.choice(["#8A6234", "#6A4A26", "#A47A44"]), strokeWidth=4, opacity=55, cap="round")
# moss cushions along the soil lip (centres hug the lip, all on the disc)
for i, (x, r) in enumerate([(150, 24), (196, 30), (252, 22), (420, 18), (640, 26), (700, 34), (760, 28), (812, 22),
                            (590, 16), (330, 20)]):
    y = GY - 22 * (1 - ((x - PCX) / gx) ** 2) + 6
    if not on_disc(x, y, r + 8): continue
    d.shape("ellipse", f"Moss {i+1}", x=x - r, y=y - r * 0.7, width=2 * r, height=1.3 * r,
            fill=rad("#9CC45A", "#5E8A34", "#34521E"), stroke=NONE, opacity=92)
    for j in range(3):
        px = x - r * 0.5 + j * r * 0.5
        top = y - r * 0.7 - 16 - (j % 2) * 8
        d.path(f"M{px:.1f},{y - r * 0.4:.1f} Q{px + 3:.1f},{(y + top) / 2:.1f} {px + 2:.1f},{top:.1f}",
               f"Moss {i+1} seta {j+1}", fill=NONE, stroke="#B8A04A", strokeWidth=3, opacity=60, cap="round")
        d.shape("ellipse", f"Moss {i+1} capsule {j+1}", x=px - 1, y=top - 6, width=6, height=8,
                fill=rad("#E8D47A", "#9A7E30"), opacity=80, stroke=NONE)
# a fern frond leaning in from the right
F0, F1, F2 = (836, 690), (860, 520), (742, 410)
d.path(f"M{F0[0]},{F0[1]} Q{F1[0]},{F1[1]} {F2[0]},{F2[1]}", "Fern rachis", fill=NONE,
       stroke="#4E7A34", strokeWidth=4, cap="round", opacity=85)
for j in range(1, 16):
    t = j / 16
    x, y = qpt(F0, F1, F2, t)
    tx, ty = qtan(F0, F1, F2, t)
    ln = math.hypot(tx, ty); ux, uy = tx / ln, ty / ln
    L = 40 * math.sin(math.pi * (0.2 + 0.8 * t)) + 8
    for side in (1, -1):
        nx, ny = -uy * side, ux * side
        tip = (x + (nx * 0.85 + ux * 0.45) * L, y + (ny * 0.85 + uy * 0.45) * L)
        if not on_disc(*tip, 12): continue
        m = ((x + tip[0]) / 2, (y + tip[1]) / 2)
        d.path(f"M{x:.1f},{y:.1f} Q{m[0] - ux * 7:.1f},{m[1] - uy * 7:.1f} {tip[0]:.1f},{tip[1]:.1f} "
               f"Q{m[0] + ux * 7:.1f},{m[1] + uy * 7:.1f} {x + ux * 6:.1f},{y + uy * 6:.1f} Z",
               f"Fern pinna {j}{'a' if side > 0 else 'b'}", fill=lin("#7AAA4A", "#3A6228", (x, y), tip),
               stroke=NONE, opacity=80 if side > 0 else 62)

# --- kiwi -----------------------------------------------------------------------------------------
d.shape("ellipse", "Kiwi shadow", x=330, y=688, width=420, height=40, fill="#120A04", opacity=45, stroke=NONE)

def leg(name, pts, toes, dark=False):
    s = smooth(pts, closed=False)
    d.path(s, f"{name} ink", fill=NONE, stroke=INK, strokeWidth=26, cap="round")
    d.path(s, name, fill=NONE, stroke=lin("#B8A898", "#7A6A5C") if dark else LEG_GRAD, strokeWidth=19, cap="round")
    for k in range(3):
        a, b = pts[-2], pts[-1]
        y = a[1] + (b[1] - a[1]) * (0.25 + 0.25 * k)
        x = a[0] + (b[0] - a[0]) * (0.25 + 0.25 * k)
        d.path(f"M{x - 8:.1f},{y:.1f} Q{x:.1f},{y + 4:.1f} {x + 8:.1f},{y:.1f}", f"{name} scale {k+1}",
               fill=NONE, stroke="#6A5A4C", strokeWidth=3, opacity=45, cap="round")
    fx, fy = pts[-1]
    for i, (tx, ty) in enumerate(toes):
        ts = f"M{fx:.1f},{fy:.1f} Q{(fx + tx) / 2:.1f},{fy + 2:.1f} {tx:.1f},{ty:.1f}"
        d.path(ts, f"{name} toe {i+1} ink", fill=NONE, stroke=INK, strokeWidth=14, cap="round")
        d.path(ts, f"{name} toe {i+1}", fill=NONE, stroke="#A89888" if dark else "#D4C4B4", strokeWidth=8, cap="round")
        d.path(f"M{tx:.1f},{ty:.1f} l{-6 if tx < fx else 6},{3}", f"{name} claw {i+1}", fill=NONE,
               stroke="#3A2A1C", strokeWidth=4, cap="round")

# far leg planted back, near leg stepping forward
leg("Far leg", [(612, 610), (628, 660), (640, 700)], [(604, 708), (624, 712), (646, 712), (668, 706)], dark=True)
leg("Near leg", [(540, 616), (528, 660), (510, 702)], [(470, 712), (492, 716), (514, 716), (540, 708)])

# body: an egg tipped forward, small head fused to it
BODY_PTS = [(338, 430), (380, 382), (452, 344), (548, 330), (640, 344), (716, 384), (762, 446),
            (774, 510), (752, 572), (700, 620), (622, 648), (530, 650), (448, 628), (388, 586),
            (348, 534), (322, 484)]
d.path(smooth(BODY_PTS), "Body", fill=BODY_GRAD, stroke=INK, strokeWidth=4)
d.path(smooth([(410, 380), (500, 344), (600, 340), (680, 366)], closed=False), "Back light",
       fill=NONE, stroke="#F2D8A8", strokeWidth=26, opacity=20, cap="round")
d.path(smooth([(420, 610), (520, 644), (630, 640), (720, 600)], closed=False), "Belly shade",
       fill=NONE, stroke="#2E1E10", strokeWidth=30, opacity=28, cap="round")

# hair-like feathers: strands flowing back and down from the head
HEAD_C = (340, 460)
poly = BODY_PTS
strands = []
for i in range(520):
    x, y = rng.uniform(330, 775), rng.uniform(330, 650)
    if not inside(poly, x, y): continue
    vx, vy = x - HEAD_C[0] + 40, y - HEAD_C[1] + 70
    ln = math.hypot(vx, vy) or 1
    ux, uy = vx / ln, vy / ln
    L = rng.uniform(18, 34)
    curl = rng.uniform(-8, 8)
    lit = (650 - y) / 320 + (x < 560) * 0.1
    if lit > 0.75: cols = ["#E2C08A", "#C8A06A", "#A47C4C"]
    elif lit > 0.4: cols = ["#B08A58", "#8A6438", "#C8A472"]
    else: cols = ["#6A4A2A", "#4E341C", "#8A6438"]
    strands.append((x, y, ux, uy, L, curl, rng.choice(cols), rng.randint(40, 75), rng.choice([3, 3, 4])))
for k, (x, y, ux, uy, L, curl, c, op, w) in enumerate(strands):
    ex, ey = x + ux * L, y + uy * L
    if not inside(poly, ex, ey): continue
    d.path(f"M{x:.1f},{y:.1f} Q{(x + ex) / 2 - uy * curl:.1f},{(y + ey) / 2 + ux * curl:.1f} {ex:.1f},{ey:.1f}",
           f"Feather strand {k+1}", fill=NONE, stroke=c, strokeWidth=w, opacity=op, cap="round")
# shaggy fringe breaking the silhouette, pointing back/down
for k in range(60):
    t = k / 60
    i = int(t * len(BODY_PTS))
    (x1, y1), (x2, y2) = BODY_PTS[i % len(BODY_PTS)], BODY_PTS[(i + 1) % len(BODY_PTS)]
    f = t * len(BODY_PTS) - i
    x, y = x1 + (x2 - x1) * f, y1 + (y2 - y1) * f
    if (x < 360 and y < 520) or (y < 470 and x < 700): continue   # face clean, top sleek
    vx, vy = x - 560 + 30, y - 490 + 50
    ln = math.hypot(vx, vy); ux, uy = vx / ln, vy / ln
    L = rng.uniform(10, 18)
    sx, sy = x - ux * 10, y - uy * 10
    ex, ey = x + ux * L * 0.8 + 6, y + uy * L * 0.8 + 6
    assert on_disc(ex, ey, 10)
    c = "#A07A48" if y < 480 else "#5A3E22"
    d.path(f"M{sx:.1f},{sy:.1f} Q{x:.1f},{y:.1f} {ex:.1f},{ey:.1f}", f"Fringe strand {k+1}",
           fill=NONE, stroke=c, strokeWidth=4, opacity=58, cap="round")

# --- head: eye, ear tuft, bristles, the long probing bill ------------------------------------------------
d.shape("ellipse", "Face shade", x=304, y=420, width=96, height=100, fill="#4A3018", opacity=22, stroke=NONE)
# bill: tapered along a gentle downward curve, tip in the soil
B0, B1, B2 = (322, 482), (258, 548), (206, 704)
L_, R_ = [], []
NB = 16
for k in range(NB + 1):
    t = k / NB
    x, y = qpt(B0, B1, B2, t)
    tx, ty = qtan(B0, B1, B2, t)
    ln = math.hypot(tx, ty); nx, ny = -ty / ln, tx / ln
    w = (22 * (1 - t) ** 1.1 + 6) / 2
    L_.append((x + nx * w, y + ny * w)); R_.append((x - nx * w, y - ny * w))
bill = smooth(L_ + list(reversed(R_)))
d.path(bill, "Bill", fill=BILL_GRAD, stroke=INK, strokeWidth=3)
d.path(smooth([qpt(B0, B1, B2, t / 10) for t in range(1, 9)], closed=False), "Bill ridge light",
       fill=NONE, stroke="#FFF8EA", strokeWidth=3, opacity=60, cap="round")
d.path(smooth([R_[k] for k in range(2, 14)], closed=False), "Bill underside", fill=NONE,
       stroke="#8A6A50", strokeWidth=4, opacity=40, cap="round")
nx_, ny_ = qpt(B0, B1, B2, 0.93)
d.path(f"M{nx_ - 2:.1f},{ny_ - 8:.1f} L{nx_ + 1:.1f},{ny_ - 1:.1f}", "Nostril slit", fill=NONE,
       stroke=INK, strokeWidth=3, opacity=75, cap="round")
for i, (dx, dy, r) in enumerate([(-16, -2, 4), (12, 2, 5), (-6, 8, 3), (20, -6, 3), (-24, 6, 3)]):
    d.shape("ellipse", f"Soil crumb {i+1}", x=B2[0] + dx - r, y=B2[1] + dy - r, width=2 * r, height=1.6 * r,
            fill=rad("#7A5A36", "#3A2614"), opacity=85, stroke=NONE)
# rictal bristles fanned at the bill base
for i, a in enumerate([-150, -165, -180, 168, 156, 144, 132]):
    r = math.radians(a)
    L = 46 + (i % 3) * 8
    x0, y0 = 330, 478 + (i - 3) * 2
    tip = (x0 + L * math.cos(r), y0 + L * math.sin(r))
    d.path(f"M{x0},{y0} Q{(x0 + tip[0]) / 2:.1f},{(y0 + tip[1]) / 2 - 4:.1f} {tip[0]:.1f},{tip[1]:.1f}",
           f"Bristle {i+1}", fill=NONE, stroke="#2A1A0E", strokeWidth=3, opacity=80, cap="round")
# eye: small and beady
d.shape("ellipse", "Eye", x=344, y=444, width=16, height=16, fill=rad("#3A2A1E", "#0C0806"), stroke=NONE)
d.shape("ellipse", "Eye glint", x=348, y=447, width=5, height=5, fill="#FFFFFF", opacity=85, stroke=NONE)
d.path("M341,446 Q352,438 362,446", "Brow fluff", fill=NONE, stroke="#C8A472", strokeWidth=3, opacity=60, cap="round")
# one ear tuft over the ear opening, behind the eye
for i, (a, L) in enumerate([(-130, 26), (-112, 32), (-96, 28), (-80, 22), (-146, 18)]):
    r = math.radians(a)
    x0, y0 = 392, 452
    tip = (x0 + L * math.cos(r), y0 + L * math.sin(r))
    d.path(f"M{x0},{y0} Q{x0 + L * 0.5 * math.cos(r) + 6:.1f},{y0 + L * 0.5 * math.sin(r):.1f} {tip[0]:.1f},{tip[1]:.1f}",
           f"Ear tuft {i+1}", fill=NONE, stroke=lin("#5A3E22", "#D8B47E", (x0, y0), tip), strokeWidth=4, cap="round")
d.shape("ellipse", "Ear opening", x=384, y=448, width=16, height=12, fill="#3A2616", opacity=50, stroke=NONE)

# fireflies / glow-worms in the dark
for i, (x, y) in enumerate([(200, 300), (790, 300), (690, 160), (300, 170), (160, 520)]):
    assert on_disc(x, y, 24)
    d.shape("ellipse", f"Glow-worm {i+1} halo", x=x - 12, y=y - 12, width=24, height=24,
            fill={"gradient": {"kind": "radial", "stops": [
                {"offset": 0, "color": "#BDF2E0", "opacity": 0.5},
                {"offset": 1, "color": "#BDF2E0", "opacity": 0}]}}, stroke=NONE)
    d.shape("ellipse", f"Glow-worm {i+1}", x=x - 3, y=y - 3, width=6, height=6, fill="#E6FFF4", stroke=NONE)

# plate rim on top
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840, fill=NONE, stroke="#0E160C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8ECB8", strokeWidth=3, opacity=24)

# --- name + second line ---------------------------------------------------------------------------------
d.text("KIWI", "Name", x=500, y=940, size=60, font="Virelai Sans", color="#E6F0D2", justify="center")
LINE2, SZ2, TRK = "APTERYX MANTELLI", 22, 260
r = d.text(LINE2, "Second line", x=500, y=975, size=SZ2, font="Virelai Sans", color="#A8C08A", justify="center")
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

d.finish("kiwi-V1R00")
