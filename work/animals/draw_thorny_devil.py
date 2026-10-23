#!/usr/bin/env python3
"""Thorny devil — field plate V1R00. Moloch horridus in three-quarter view,
walking left: a squat body armoured in conical spines (ochre tips over rust
bases), the spined false-head knob on the neck raised while the real head
dips, and the near forefoot lifted mid-step. Dark red-soil plate.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Thorny Devil — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#3A1A10"   # burnt umber, not black
rng = random.Random(53)

def on_disc(x, y, pad):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

def lin(c0, c1, start=None, end=None):
    g = {"kind": "linear", "stops": [{"offset": 0, "color": c0}, {"offset": 1, "color": c1}]}
    if start: g["start"], g["end"] = start, end
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

def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)

# --- scale contexts: the animal is drawn in local coordinates and scaled up
# about a ground anchor; every scaled point is checked against the disc.
import re, contextlib
XF = []
PAIR = re.compile(r"(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)")

def tp(x, y):
    for s, ax, ay in reversed(XF):
        x, y = ax + (x - ax) * s, ay + (y - ay) * s
    return x, y

def tscale():
    s = 1.0
    for f in XF: s *= f[0]
    return s

@contextlib.contextmanager
def xf(s, ax, ay):
    XF.append((s, ax, ay)); yield; XF.pop()

def _paint(p):
    if isinstance(p, dict) and "gradient" in p and "start" in p["gradient"]:
        g = dict(p["gradient"])
        g["start"] = [round(v, 1) for v in tp(*g["start"])]
        g["end"] = [round(v, 1) for v in tp(*g["end"])]
        return {"gradient": g}
    return p

_path, _shape = d.path, d.shape
def path(s, label, **kw):
    if XF:
        def sub(m):
            x, y = tp(float(m.group(1)), float(m.group(2)))
            assert on_disc(x, y, 6), (label, round(x), round(y))
            return "%.1f,%.1f" % (x, y)
        s = PAIR.sub(sub, s)
        for k in ("fill", "stroke"):
            if k in kw: kw[k] = _paint(kw[k])
        if kw.get("strokeWidth"): kw["strokeWidth"] = round(kw["strokeWidth"] * tscale(), 2)
    return _path(s, label, **kw)
def shape(kind, label, **kw):
    if XF and kind == "ellipse":
        x, y = tp(kw["x"], kw["y"]); S = tscale()
        kw.update(x=round(x, 1), y=round(y, 1), width=round(kw["width"] * S, 1), height=round(kw["height"] * S, 1))
        assert on_disc(x + kw["width"] / 2, y + kw["height"] / 2, 6), label
        for k in ("fill", "stroke"):
            if k in kw: kw[k] = _paint(kw[k])
        if kw.get("strokeWidth"): kw["strokeWidth"] = round(kw["strokeWidth"] * S, 2)
    return _shape(kind, label, **kw)
d.path, d.shape = path, shape

BG_GRAD = lin("#1C0E0A", "#070302", [0, 0], [0, 1000])
PLATE_GRAD = rad("#7A3420", "#4E1E12", "#2A0F08")
SOIL_GRAD = lin("#8A4026", "#4A1C10", [0, 660], [0, 880])
BODY_GRAD = rad("#F0CC84", "#D89A4C", "#A85A2A")
DARK_GRAD = rad("#C0703A", "#8A4422", "#5A2614")
SPINE_GRAD = lin("#9A3E1C", "#F6D48A")          # rust base -> ochre tip
SPINE_DARK = lin("#6E2A14", "#D49A56")
HEAD_GRAD = rad("#F2D08C", "#D49048", "#9A5226")

# --- backdrop + plate ------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876, fill="#A0482A", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840, fill=PLATE_GRAD, stroke=NONE)
d.shape("ellipse", "Heat glow", x=180, y=110, width=640, height=360,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#F2A060", "opacity": 0.18},
            {"offset": 1, "color": "#F2A060", "opacity": 0}]}}, stroke=NONE)

# red soil ground, closed on the disc arc
GY = 664
gx = math.sqrt(PR**2 - (GY - PCY)**2)
d.path(f"M{PCX - gx:.1f},{GY} Q{PCX},{GY - 18} {PCX + gx:.1f},{GY} A420,420 0 0 1 {PCX - gx:.1f},{GY} Z",
       "Red soil", fill=SOIL_GRAD, stroke=NONE)
for i, (cx, cy, w) in enumerate([(300, 720, 150), (680, 728, 170), (480, 760, 240), (360, 800, 160),
                                 (620, 812, 180), (500, 846, 150)]):
    assert on_disc(cx - w / 2, cy, 10) and on_disc(cx + w / 2, cy, 10), (cx, cy)
    d.path(f"M{cx - w/2},{cy} Q{cx},{cy - 8} {cx + w/2},{cy}", f"Sand ripple {i+1}",
           fill=NONE, stroke="#C2683C", strokeWidth=3, opacity=35, cap="round")
for i in range(26):
    x, y = rng.uniform(200, 800), rng.uniform(690, 860)
    r = rng.uniform(2.5, 7)
    if not on_disc(x, y, 14): continue
    d.shape("ellipse", f"Pebble {i+1}", x=x - r, y=y - r * 0.7, width=2 * r, height=1.4 * r,
            fill=rad("#D88A5A", "#8A3E22"), opacity=70, stroke=NONE)

# spinifex tussock at the right of the ground
for i in range(9):
    a = math.radians(-150 + i * 14 + rng.uniform(-4, 4))
    L = rng.uniform(80, 130)
    x0, y0 = 800 + rng.uniform(-14, 14), 676
    tip = (x0 + L * math.cos(a) * 0.55 + 30, y0 + L * math.sin(a))
    assert on_disc(*tip, 14), tip
    d.path(f"M{x0:.0f},{y0} Q{x0 + 6:.0f},{(y0 + tip[1]) / 2:.0f} {tip[0]:.0f},{tip[1]:.0f}",
           f"Spinifex {i+1}", fill=NONE, stroke=lin("#8A7A3A", "#D8C878"), strokeWidth=4,
           opacity=75, cap="round")

# --- spine primitive -------------------------------------------------------------------
def spine(name, x, y, ang, L, w, grad=SPINE_GRAD, ink=True):
    a = math.radians(ang)
    ux, uy = math.cos(a), math.sin(a)
    nx, ny = -uy, ux
    tip = (x + ux * L, y + uy * L)
    b1 = (x + nx * w / 2, y + ny * w / 2)
    b2 = (x - nx * w / 2, y - ny * w / 2)
    c1 = (x + ux * L * 0.45 + nx * w * 0.32, y + uy * L * 0.45 + ny * w * 0.32)
    c2 = (x + ux * L * 0.45 - nx * w * 0.32, y + uy * L * 0.45 - ny * w * 0.32)
    s = (f"M{b1[0]:.1f},{b1[1]:.1f} Q{c1[0]:.1f},{c1[1]:.1f} {tip[0]:.1f},{tip[1]:.1f} "
         f"Q{c2[0]:.1f},{c2[1]:.1f} {b2[0]:.1f},{b2[1]:.1f} Q{x - ux * w * 0.2:.1f},{y - uy * w * 0.2:.1f} "
         f"{b1[0]:.1f},{b1[1]:.1f} Z")
    g = {"gradient": dict(grad["gradient"], start=[round(x), round(y)], end=[round(tip[0]), round(tip[1])])}
    d.path(s, name, fill=g, stroke=INK if ink else NONE, strokeWidth=3 if ink else 0, opacity=96)
    if L >= 20:
        # sunlit flank of the cone, light from the upper left
        sn = 1 if (nx * -0.6 + ny * -0.8) > 0 else -1
        h0 = (x + nx * sn * w * 0.22 + ux * L * 0.12, y + ny * sn * w * 0.22 + uy * L * 0.12)
        h1 = (x + nx * sn * w * 0.06 + ux * L * 0.66, y + ny * sn * w * 0.06 + uy * L * 0.66)
        d.path(f"M{h0[0]:.1f},{h0[1]:.1f} L{h1[0]:.1f},{h1[1]:.1f}", f"{name} light", fill=NONE,
               stroke="#FFF2C8", strokeWidth=3, opacity=55, cap="round")
    return tip

# --- body surface: far silhouette F, dorsal ridge R, near belly edge B ---------------------
F = ((388, 448), (548, 372), (716, 462))
R = ((392, 462), (550, 398), (716, 476))
B = ((362, 566), (548, 664), (726, 528))
Fu = lambda u: qpt(*F, u)
Ru = lambda u: qpt(*R, u)
Bu = lambda u: qpt(*B, u)

def draw_animal():
    # --- tail (behind the body) --------------------------------------------------------------
    T0, T1, T2 = (690, 500), (798, 500), (806, 388)
    tl, tr, tmid = [], [], []
    NTL = 20
    for k in range(NTL + 1):
        t = k / NTL
        x, y = qpt(T0, T1, T2, t)
        tx, ty = qtan(T0, T1, T2, t)
        ln = math.hypot(tx, ty)
        nx, ny = -ty / ln, tx / ln
        w = (64 * (1 - t) ** 0.9 + 7) / 2
        tl.append((x + nx * w, y + ny * w)); tr.append((x - nx * w, y - ny * w)); tmid.append((x, y, nx, ny, w))
    tail = smooth(tl + list(reversed(tr)))
    d.path(tail, "Tail", fill=lin("#E2B06A", "#A0522A", [700, 420], [820, 520]), stroke=INK, strokeWidth=4)
    for j, t in enumerate([0.2, 0.42, 0.62, 0.8]):
        x, y, nx, ny, w = tmid[round(t * NTL)]
        d.path(f"M{x + nx * w:.1f},{y + ny * w:.1f} L{x - nx * w:.1f},{y - ny * w:.1f}", f"Tail band {j+1}",
               fill=NONE, stroke="#8A3A1C", strokeWidth=max(4, w * 0.7), opacity=55, cap="round")
    for k in range(2, NTL, 2):
        x, y, nx, ny, w = tmid[k]
        t = k / NTL
        for side in (1, -1):
            bx, by = x + nx * w * side * 0.8, y + ny * w * side * 0.8
            ang = math.degrees(math.atan2(ny * side, nx * side)) + 25 * side
            tip = spine(f"Tail spine {k}{'a' if side > 0 else 'b'}", bx, by, ang, 20 - 9 * t, 11 - 5 * t)

    # --- far legs (behind the body, shaded) -----------------------------------------------------
    def leg(name, joints, w, grad, foot=None, toe_ang=(), toe_len=20, spines=True, dark=False):
        s = smooth(joints, closed=False)
        d.path(s, f"{name} ink", fill=NONE, stroke=INK, strokeWidth=w + 7, cap="round")
        d.path(s, name, fill=NONE, stroke=grad, strokeWidth=w, cap="round")
        if foot:
            for i, a in enumerate(toe_ang):
                r = math.radians(a)
                tip = (foot[0] + toe_len * math.cos(r), foot[1] + toe_len * math.sin(r))
                ts = f"M{foot[0]:.1f},{foot[1]:.1f} L{tip[0]:.1f},{tip[1]:.1f}"
                d.path(ts, f"{name} toe {i+1} ink", fill=NONE, stroke=INK, strokeWidth=11, cap="round")
                d.path(ts, f"{name} toe {i+1}", fill=NONE, stroke="#B86A34" if dark else "#DCA05C",
                       strokeWidth=6, cap="round")
                d.path(f"M{tip[0]:.1f},{tip[1]:.1f} L{tip[0] + 5 * math.cos(r):.1f},{tip[1] + 5 * math.sin(r) + 2:.1f}",
                       f"{name} claw {i+1}", fill=NONE, stroke="#2A140C", strokeWidth=3, cap="round")
        if spines:
            for i in range(len(joints) - 1):
                p, q = joints[i], joints[i + 1]
                m = lerp(p, q, 0.5)
                ang = math.degrees(math.atan2(q[1] - p[1], q[0] - p[0])) - 90
                spine(f"{name} spine {i+1}", m[0], m[1], ang - 15, 14, 9, SPINE_DARK if dark else SPINE_GRAD)

    d.shape("ellipse", "Ground shadow", x=250, y=640, width=560, height=64, fill="#1E0904", opacity=45, stroke=NONE)
    d.shape("ellipse", "Lifted foot shadow", x=232, y=676, width=90, height=18, fill="#1E0904", opacity=30, stroke=NONE)

    leg("Far hind leg", [(700, 524), (742, 558), (748, 606)], 26, DARK_GRAD, foot=(748, 608),
        toe_ang=(-20, 10, 40, 70, 100), toe_len=20, dark=True)
    leg("Far fore leg", [(424, 566), (424, 606), (408, 638)], 26, DARK_GRAD, foot=(408, 640),
        toe_ang=(150, 120, 90, 60, 30), toe_len=20, dark=True)

    # --- body -------------------------------------------------------------------------------------
    top = [Fu(i / 16) for i in range(17)]
    bot = [Bu(i / 16) for i in range(16, -1, -1)]
    body_pts = top + [(744, 494)] + bot + [(344, 512)]
    BODY = smooth(body_pts)
    d.path(BODY, "Body", fill=BODY_GRAD, stroke=NONE)

    # patterning under the spines: pale dorsal stripe, rust saddles with dark rims, belly shade
    for k, (uc, du, b0, b1) in enumerate([(0.16, 0.07, 0.10, 0.52), (0.38, 0.08, 0.14, 0.62),
                                          (0.60, 0.075, 0.10, 0.56), (0.80, 0.06, 0.12, 0.48),
                                          (0.27, 0.04, 0.58, 0.84), (0.50, 0.05, 0.66, 0.88),
                                          (0.71, 0.04, 0.60, 0.84)]):
        pts = []
        for j in range(10):
            a = 2 * math.pi * j / 10
            uu = uc + du * math.cos(a) * (1 + 0.18 * math.sin(3 * a + k))
            bb = (b0 + b1) / 2 + (b1 - b0) / 2 * math.sin(a) * (1 + 0.12 * math.cos(2 * a + k))
            pts.append(lerp(Ru(uu), Bu(uu), bb))
        d.path(smooth(pts), f"Saddle {k+1}", fill=DARK_GRAD, stroke="#4A1E0E", strokeWidth=4, opacity=80)
        d.path(smooth(pts), f"Saddle {k+1} pale rim", fill=NONE, stroke="#F8DDA0", strokeWidth=3, opacity=30)
    for k, (u0, u1) in enumerate([(0.14, 0.30), (0.40, 0.56), (0.66, 0.82)]):
        fpts = [lerp(Ru(u0 + (u1 - u0) * s / 5), Fu(u0 + (u1 - u0) * s / 5), 0.2) for s in range(6)]
        fpts += [lerp(Ru(u1 - (u1 - u0) * s / 5), Fu(u1 - (u1 - u0) * s / 5), 0.9) for s in range(6)]
        d.path(smooth(fpts), f"Far saddle {k+1}", fill=DARK_GRAD, stroke="#4A1E0E", strokeWidth=3, opacity=70)
    d.path(smooth([Ru(i / 12) for i in range(13)], closed=False), "Dorsal stripe", fill=NONE,
           stroke="#F8E2A8", strokeWidth=16, opacity=60, cap="round")
    d.path(smooth([lerp(Ru(i / 12), Bu(i / 12), 0.86) for i in range(1, 12)], closed=False), "Belly shade",
           fill=NONE, stroke="#6A2A14", strokeWidth=26, opacity=35, cap="round")

    # spine field, painted back (far side, top) to front (near side, low)
    field = []
    NU = 19
    for row, b in enumerate([-0.62, -0.32, -0.1, 0.06, 0.22, 0.38, 0.54, 0.7, 0.86]):
        for i in range(NU):
            u = (i + 0.5 * (row % 2) + 0.5) / (NU + 0.5)
            if not 0.03 < u < 0.97: continue
            if b < 0:
                P = lerp(Ru(u), Fu(u), -b)
            else:
                P = lerp(Ru(u), Bu(u), b)
            C = lerp(Ru(u), Bu(u), 0.62)
            vx, vy = P[0] - C[0], P[1] - C[1] - 60
            ang = math.degrees(math.atan2(vy, vx)) + 10      # lean back toward the tail
            ridge = 1 - min(1, abs(b) / 0.9)
            L = (14 + 18 * ridge) * (0.75 + 0.35 * math.sin(math.pi * u)) + rng.uniform(-2, 2)
            W = L * 0.55
            field.append((P[1], P, ang, L, W, row, i))
    field.sort(key=lambda f: f[0])
    for _, P, ang, L, W, row, i in field:
        spine(f"Body spine r{row} {i+1}", P[0], P[1], ang + rng.uniform(-6, 6), L, W)
    # silhouette spines along the far edge and the belly edge
    for i in range(1, 14):
        u = i / 14
        x, y = Fu(u)
        tx, ty = qtan(*F, u)
        ang = math.degrees(math.atan2(-tx, ty)) + 180 + 12
        spine(f"Crest spine {i}", x, y, ang, 26 + 8 * math.sin(math.pi * u), 14)
    for i in range(1, 12):
        u = i / 12
        x, y = Bu(u)
        tx, ty = qtan(*B, u)
        ang = math.degrees(math.atan2(tx, -ty)) + 180 - 10
        spine(f"Belly spine {i}", x, y, ang, 14, 10, SPINE_DARK)
    d.path(smooth([lerp(Fu(i / 10), Ru(i / 10), 0.5) for i in range(2, 9)], closed=False), "Back sheen",
           fill=NONE, stroke="#FFF0C8", strokeWidth=10, opacity=22, cap="round")

    # --- near legs ----------------------------------------------------------------------------------
    leg("Near hind leg", [(648, 590), (696, 618), (676, 652)], 32, lin("#E8BC72", "#B8682E"), foot=(676, 654),
        toe_ang=(170, 135, 100, 60, 20), toe_len=24)
    # near forefoot lifted mid-step: elbow back, wrist forward, toes curled down
    leg("Near fore leg", [(394, 578), (356, 614), (314, 604)], 30, lin("#E8BC72", "#B8682E"), foot=(310, 606),
        toe_ang=(150, 125, 100, 78, 56), toe_len=20)

    # --- false head: the spined knob on the neck, raised ---------------------------------------------
    # a fleshy hump rising out of the nape, so it reads as part of the neck
    KX, KY = 400, 440
    hump = smooth([(352, 500), (350, 462), (370, 424), (402, 408), (434, 420), (452, 452), (456, 492), (404, 512)])
    d.path(hump, "False head", fill=rad("#F8DC9C", "#DC9A50", "#A45626"), stroke=NONE)
    d.path(smooth([(354, 470), (368, 430), (402, 410), (436, 422), (452, 456)], closed=False), "False head rim",
           fill=NONE, stroke=INK, strokeWidth=4, cap="round")
    d.path("M362,470 Q402,494 448,466", "False head band", fill=NONE, stroke="#7A3218", strokeWidth=8,
           opacity=50, cap="round")
    d.path("M372,440 Q396,420 426,424", "False head sheen", fill=NONE, stroke="#FFF2CC", strokeWidth=6,
           opacity=45, cap="round")
    for j, (x, y, a, L, W) in enumerate([(362, 452, -150, 22, 12), (376, 424, -118, 36, 17), (404, 412, -92, 26, 13),
                                         (428, 420, -66, 36, 17), (446, 446, -36, 22, 12), (396, 452, -100, 16, 10),
                                         (420, 458, -78, 16, 10)]):
        spine(f"False head spine {j+1}", x, y, a, L, W)

    with xf(0.86, 392, 548):
        # --- head: dipped, wedge snout, horned brow ---------------------------------------------------------
        HEAD = smooth([(384, 494), (346, 478), (300, 486), (262, 512), (234, 552), (230, 584), (252, 598),
                       (300, 596), (344, 584), (376, 556), (390, 524)])
        d.path(HEAD, "Head", fill=HEAD_GRAD, stroke=INK, strokeWidth=5)
        d.path(smooth([(370, 500), (330, 490), (292, 500), (262, 530)], closed=False), "Head sheen",
               fill=NONE, stroke="#FFF2CC", strokeWidth=7, opacity=35, cap="round")
        d.path(smooth([(240, 586), (290, 590), (340, 580), (372, 560)], closed=False), "Jaw shade",
               fill=NONE, stroke="#7A3A1A", strokeWidth=12, opacity=35, cap="round")
        # dark eye stripe running back from the snout
        d.path("M246,552 C270,540 300,532 340,536 C356,538 368,546 376,556", "Eye stripe",
               fill=NONE, stroke="#6A2A14", strokeWidth=10, opacity=55, cap="round")
        d.shape("ellipse", "Eye ring", x=282, y=520, width=34, height=26, fill=rad("#F6D894", "#C8803C"),
                stroke=INK, strokeWidth=3)
        d.shape("ellipse", "Eye", x=289, y=525, width=20, height=16, fill=rad("#4A3020", "#120A06"), stroke=NONE)
        d.shape("ellipse", "Eye glint", x=294, y=527, width=6, height=5, fill="#FFFFFF", opacity=85, stroke=NONE)
        d.path("M236,584 C262,588 300,588 332,582", "Mouth", fill=NONE, stroke=INK, strokeWidth=4, cap="round")
        d.shape("ellipse", "Nostril", x=244, y=560, width=6, height=5, fill=INK, opacity=70, stroke=NONE)
        # brow horns over the eye (near one big, far one peeking)
        spine("Brow horn far", 324, 494, -106, 40, 16, SPINE_DARK)
        spine("Brow horn near", 300, 506, -118, 46, 18)
        for j, (x, y, a, L) in enumerate([(266, 520, -140, 14), (350, 492, -90, 18), (372, 506, -70, 16),
                                          (258, 548, -170, 12), (330, 568, 100, 12), (296, 576, 100, 11)]):
            spine(f"Head spine {j+1}", x, y, a, L, 9)


with xf(1.2, 480, 670):
    draw_animal()

# heat shimmer motes
for i, (x, y) in enumerate([(220, 300), (760, 250), (640, 160), (300, 180), (820, 330), (180, 430)]):
    assert on_disc(x, y, 20)
    d.shape("ellipse", f"Dust mote {i+1}", x=x - 4, y=y - 4, width=8, height=8, fill="#F8C890",
            opacity=35, stroke=NONE)

# plate rim on top so ground and decor close under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840, fill=NONE, stroke="#1E0A06", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F2B88A", strokeWidth=3, opacity=24)

# --- name + second line --------------------------------------------------------------------------
d.text("THORNY DEVIL", "Name", x=500, y=940, size=56, font="Virelai Sans", color="#F2D6B8", justify="center")
LINE2, SZ2, TRK = "MOLOCH HORRIDUS", 22, 260
r = d.text(LINE2, "Second line", x=500, y=975, size=SZ2, font="Virelai Sans", color="#C8957A", justify="center")
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

d.finish("thorny-devil-V1R00")
