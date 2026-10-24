#!/usr/bin/env python3
"""Gila monster — field plate V1R00. Heloderma suspectum in profile, walking
left: the heavy low-slung body paved in bead osteoderms — pink-orange beads
banded over black — the blunt snout dipped, the fat sausage tail curling
behind. Desert plate, creosote mood: dusty dusk disc, a creosote sprig,
scattered grit. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Gila Monster — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#26140E"   # warm dark ink, never pure black
rng = random.Random(1106)

def on_disc(x, y, pad):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

def lin(c0, c1, start=None, end=None):
    g = {"kind": "linear", "stops": [{"offset": 0, "color": c0}, {"offset": 1, "color": c1}]}
    if start: g["start"], g["end"] = start, end
    return {"gradient": g}

def lin3(c0, c1, c2, start=None, end=None):
    g = {"kind": "linear", "stops": [{"offset": 0, "color": c0},
         {"offset": 0.55, "color": c1}, {"offset": 1, "color": c2}]}
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

BG_GRAD    = lin("#18100C", "#060302", [0, 0], [0, 1000])
PLATE_GRAD = rad("#C8825E", "#8A4E32", "#4A2414", "#28120A")
FLOOR_GRAD = lin("#9A5836", "#3E1E10", [0, 660], [0, 880])
BODY_GRAD  = rad("#3A2418", "#241510", "#120A06")
DARK_BEAD  = rad("#3E2A1E", "#241510")
PINK_BEADS = [rad("#F8C8A0", "#E88A5E"), rad("#F2A878", "#D06844"),
              rad("#EE9668", "#C85A38"), rad("#E8845A", "#B04C30")]

# --- backdrop + dusk desert plate ------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876, fill="#C8825E", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840, fill=PLATE_GRAD, stroke=NONE)
# dusk glow low on the horizon
d.shape("ellipse", "Dusk glow", x=180, y=380, width=640, height=280,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#F0A868", "opacity": 0.30},
            {"offset": 0.6, "color": "#E08850", "opacity": 0.12},
            {"offset": 1, "color": "#E08850", "opacity": 0}]}}, stroke=NONE)
# far mesa silhouettes, very faint, above the ground line
d.path("M150,640 L208,556 L296,556 L330,596 L420,596 L470,640 Z",
       "Far mesa L", fill="#5A2E1C", opacity=45, stroke=NONE)
d.path("M560,636 L620,572 L720,572 L768,606 L836,606 L858,640 Z",
       "Far mesa R", fill="#552B1A", opacity=40, stroke=NONE)

# --- desert floor, closed on the disc arc -------------------------------------------
GY = 672
gx = math.sqrt(PR**2 - (GY - PCY)**2)
d.path(f"M{PCX - gx:.1f},{GY} Q{PCX},{GY - 14} {PCX + gx:.1f},{GY} A420,420 0 0 1 {PCX - gx:.1f},{GY} Z",
       "Desert floor", fill=FLOOR_GRAD, stroke=NONE)
# scattered grit + pebbles on the floor
for i in range(30):
    x, y = rng.uniform(190, 810), rng.uniform(690, 856)
    r = rng.uniform(2.5, 7)
    if not on_disc(x, y, 14): continue
    d.shape("ellipse", f"Grit {i+1}", x=x - r, y=y - r * 0.7, width=2 * r, height=1.4 * r,
            fill=rad("#C8885C", "#6A341E"), opacity=rng.choice((40, 55, 70)), stroke=NONE)
for i, (cx, cy, w) in enumerate([(280, 736, 130), (700, 730, 150), (480, 776, 220),
                                 (360, 800, 140), (610, 818, 170)]):
    assert on_disc(cx - w / 2, cy, 10) and on_disc(cx + w / 2, cy, 10), (cx, cy)
    d.path(f"M{cx - w/2},{cy} Q{cx},{cy - 7} {cx + w/2},{cy}", f"Sand ripple {i+1}",
           fill=NONE, stroke="#C07040", strokeWidth=3, opacity=30, cap="round")

# --- creosote sprig, left of the animal ------------------------------------------------
def creosote(x0, y0, label):
    # sparse zig-zag twigs with tiny paired leaflets; olive-drab, thin but >=3pt
    twigs = [((x0, y0), (x0 + 4, y0 - 60), (x0 - 6, y0 - 118)),
             ((x0 + 2, y0 - 52), (x0 + 40, y0 - 86), (x0 + 58, y0 - 128)),
             ((x0 - 2, y0 - 84), (x0 - 38, y0 - 116), (x0 - 52, y0 - 152))]
    for j, (a, b, c) in enumerate(twigs):
        d.path(f"M{a[0]},{a[1]} Q{b[0]},{b[1]} {c[0]},{c[1]}", f"{label} twig {j+1}",
               fill=NONE, stroke="#4E4A2A", strokeWidth=3.5, cap="round")
        for k, t in enumerate((0.45, 0.7, 0.92)):
            px, py = qpt(a, b, c, t)
            tx, ty = qtan(a, b, c, t)
            ln = math.hypot(tx, ty) or 1
            nx, ny = -ty / ln, tx / ln
            for s in (1, -1):
                lx, ly = px + nx * 9 * s, py + ny * 9 * s
                assert on_disc(lx, ly, 8), (label, lx, ly)
                d.shape("ellipse", f"{label} leaf {j}{k}{'a' if s > 0 else 'b'}",
                        x=lx - 5, y=ly - 3.5, width=10, height=7,
                        fill=lin("#7E7C46", "#52522C"), opacity=85, stroke=NONE)
    # creosote's little yellow flowers
    for k, t in enumerate((0.55, 0.85)):
        for j, (a, b, c) in enumerate(twigs[1:], 1):
            px, py = qpt(a, b, c, t + 0.04 * (j - 1))
            assert on_disc(px, py, 8)
            for m in range(5):
                a0 = 2 * math.pi * m / 5
                d.shape("ellipse", f"{label} petal {j}{k}{m}",
                        x=px + 5 * math.cos(a0) - 3, y=py + 5 * math.sin(a0) - 3,
                        width=6, height=6, fill="#E8C84A", opacity=80, stroke=NONE)
creosote(238, 662, "Creosote")

# === the gila monster: profile walk, left ================================================
# top and belly rails of the trunk
T = ((358, 476), (545, 412), (706, 470))
B = ((344, 578), (545, 636), (728, 520))
Tu = lambda u: qpt(*T, u)
Bu = lambda u: qpt(*B, u)

# tail: fat sausage curling right, behind the body
T0, T1, T2 = (694, 512), (838, 560), (772, 664)
tl, tr, tm = [], [], []
NT = 22
for k in range(NT + 1):
    t = k / NT
    x, y = qpt(T0, T1, T2, t)
    tx, ty = qtan(T0, T1, T2, t)
    ln = math.hypot(tx, ty)
    nx, ny = -ty / ln, tx / ln
    w = (58 * (1 - t) ** 0.85 + 8) / 2
    tl.append((x + nx * w, y + ny * w)); tr.append((x - nx * w, y - ny * w))
    tm.append((x, y, nx, ny, w, t))
tail = smooth(tl + list(reversed(tr)))
d.path(tail, "Tail", fill=lin3("#382216", "#241510", "#140B07", [690, 460], [820, 660]),
       stroke=INK, strokeWidth=4)
# pale bead bands ringing the tail
for j, t in enumerate((0.22, 0.45, 0.66)):
    x, y, nx, ny, w, _ = tm[round(t * NT)]
    d.path(f"M{x + nx * w * 0.96:.1f},{y + ny * w * 0.96:.1f} "
           f"L{x - nx * w * 0.96:.1f},{y - ny * w * 0.96:.1f}",
           f"Tail band {j+1}", fill=NONE, stroke="#E88A5E", strokeWidth=max(7, w * 0.62),
           opacity=70, cap="round")
    # bead dots along the lit band, jittered so they don't read as corn rows
    for s in (-0.62, -0.28, 0.08, 0.42, 0.72):
        bx = x + nx * w * s + rng.uniform(-2, 2)
        by = y + ny * w * s + rng.uniform(-2, 2)
        rr = rng.uniform(7, 10)
        d.shape("ellipse", f"Tail band {j+1} bead", x=bx - rr / 2, y=by - rr * 0.44,
                width=rr, height=rr * 0.88,
                fill=PINK_BEADS[(j + int((s + 1) * 2)) % 4], opacity=85,
                stroke="#2A1610", strokeWidth=1)

# ground shadow under the animal
d.shape("ellipse", "Contact shadow", x=255, y=640, width=500, height=50,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#100704", "opacity": 0.55},
            {"offset": 0.7, "color": "#100704", "opacity": 0.22},
            {"offset": 1, "color": "#100704", "opacity": 0}]}}, stroke=NONE)

# --- far legs (behind the body, shaded dark) ---------------------------------------------
def leg(name, joints, w, col, foot=None, toe_ang=(), toe_len=18, dark=False):
    s = smooth(joints, closed=False)
    d.path(s, f"{name} ink", fill=NONE, stroke=INK, strokeWidth=w + 6, cap="round")
    d.path(s, name, fill=NONE, stroke=col, strokeWidth=w, cap="round")
    # bead stipple along the leg
    for i in range(len(joints) - 1):
        p, q = joints[i], joints[i + 1]
        for tt in (0.3, 0.65):
            m = lerp(p, q, tt)
            px = m[0] + rng.uniform(-w * 0.28, w * 0.28)
            py = m[1] + rng.uniform(-w * 0.28, w * 0.28)
            light = rng.random() < 0.45
            d.shape("ellipse", f"{name} bead", x=px - 4, y=py - 3.5, width=8, height=7,
                    fill=rng.choice(PINK_BEADS) if light else DARK_BEAD,
                    opacity=85 if light else 70, stroke=NONE)
    if foot:
        for i, a in enumerate(toe_ang):
            r = math.radians(a)
            tip = (foot[0] + toe_len * math.cos(r), foot[1] + toe_len * math.sin(r))
            d.path(f"M{foot[0]:.1f},{foot[1]:.1f} L{tip[0]:.1f},{tip[1]:.1f}",
                   f"{name} toe {i+1} ink", fill=NONE, stroke=INK, strokeWidth=10, cap="round")
            d.path(f"M{foot[0]:.1f},{foot[1]:.1f} L{tip[0]:.1f},{tip[1]:.1f}",
                   f"{name} toe {i+1}", fill=NONE,
                   stroke="#3A2214" if dark else "#4E2C1A", strokeWidth=6, cap="round")
            d.path(f"M{tip[0]:.1f},{tip[1]:.1f} L{tip[0] + 6 * math.cos(r):.1f},{tip[1] + 6 * math.sin(r) + 2:.1f}",
                   f"{name} claw {i+1}", fill=NONE, stroke="#140A06", strokeWidth=3, cap="round")

leg("Far hind leg", [(660, 560), (696, 600), (690, 648)], 30, "#2A1810",
    foot=(690, 650), toe_ang=(0, 30, 60, 95), toe_len=13, dark=True)
leg("Far fore leg", [(430, 570), (426, 614), (412, 648)], 30, "#2A1810",
    foot=(410, 650), toe_ang=(130, 100, 70, 40), toe_len=13, dark=True)

# --- trunk silhouette ----------------------------------------------------------------------
top = [Tu(i / 16) for i in range(17)]
bot = [Bu(i / 16) for i in range(16, -1, -1)]
# head runs on past the neck: low blunt snout dipped, jowls wide at the throat
head_pts = [(354, 488), (336, 472), (306, 466), (278, 472), (256, 488),
            (244, 506), (244, 522), (258, 542), (284, 556), (320, 562), (348, 566)]
body_pts = head_pts + top + [(726, 492)] + bot
d.path(smooth(body_pts), "Body", fill=BODY_GRAD, stroke=INK, strokeWidth=4.5)
# belly shade + back sheen
d.path(smooth([lerp(Tu(i / 12), Bu(i / 12), 0.88) for i in range(1, 12)], closed=False),
       "Belly shade", fill=NONE, stroke="#080402", strokeWidth=22, opacity=35, cap="round")
d.path(smooth([Tu(i / 12) for i in range(1, 12)], closed=False), "Back sheen",
       fill=NONE, stroke="#C89268", strokeWidth=8, opacity=22, cap="round")

# --- the bead field --------------------------------------------------------------------------
# light-bead bands along the trunk: irregular crossbands like the live pattern
def light_band(u, v):
    # gila reticulation: pink-orange blotched crossbands on black
    bands = ((0.10, 0.19, 0.12, 0.80), (0.31, 0.41, 0.05, 0.70),
             (0.53, 0.61, 0.15, 0.88), (0.73, 0.81, 0.10, 0.78),
             (0.90, 0.96, 0.22, 0.82))
    for k, (u0, u1, v0, v1) in enumerate(bands):
        if u0 <= u <= u1 and v0 <= v <= v1:
            return 0.95
    # stray flecks anywhere
    return 0.10

NU, NV = 26, 9
beads = []
for row in range(NV):
    v = (row + 0.5) / NV
    for i in range(NU):
        u = (i + 0.5 * (row % 2) + 0.5) / (NU + 0.5)
        if not 0.02 < u < 0.99: continue
        P = lerp(Tu(u), Bu(u), v)
        # squash the grid a touch toward midline so edge beads sit inside ink
        edge = min(1, (0.5 - abs(v - 0.5)) * 3.2)
        r = (7.5 + 2.5 * math.sin(math.pi * u)) * (0.7 + 0.3 * edge)
        beads.append((P, u, v, r))

for j, (P, u, v, r) in enumerate(beads):
    px = P[0] + rng.uniform(-1.5, 1.5)
    py = P[1] + rng.uniform(-1.5, 1.5)
    light = rng.random() < light_band(u, v)
    if light:
        g = rng.choice(PINK_BEADS)
        # darker pink toward the belly
        d.shape("ellipse", f"Bead {j}", x=px - r / 2, y=py - r * 0.44, width=r, height=r * 0.88,
                fill=g, opacity=92, stroke="#1E100A", strokeWidth=1.2)
    else:
        d.shape("ellipse", f"Bead {j}", x=px - r / 2, y=py - r * 0.44, width=r, height=r * 0.88,
                fill=DARK_BEAD, opacity=65, stroke=NONE)

# head beads: bigger, clustered, pale patch over the snout top
for j, (hx, hy, hr, lite) in enumerate([
        (298, 476, 9, 1), (280, 480, 8, 1), (316, 474, 9, 0), (334, 482, 8, 0),
        (262, 494, 8, 0), (286, 496, 9, 1), (306, 492, 9, 1), (328, 496, 8, 0),
        (256, 514, 8, 0), (280, 516, 9, 0), (302, 512, 9, 0), (324, 516, 8, 0),
        (262, 534, 8, 0), (286, 536, 9, 0), (310, 532, 9, 0), (332, 536, 8, 0),
        (276, 550, 8, 0), (300, 550, 9, 0), (324, 548, 8, 0), (344, 500, 8, 0)]):
    d.shape("ellipse", f"Head bead {j}", x=hx - hr / 2, y=hy - hr * 0.44,
            width=hr, height=hr * 0.88,
            fill=rng.choice(PINK_BEADS) if lite else DARK_BEAD,
            opacity=90 if lite else 65, stroke="#1E100A" if lite else NONE, strokeWidth=1.1)

# --- near legs ---------------------------------------------------------------------------------
leg("Near hind leg", [(622, 580), (666, 614), (650, 656)], 36, "#4E2C1A",
    foot=(648, 658), toe_ang=(175, 140, 105, 70), toe_len=15)
leg("Near fore leg", [(406, 576), (374, 616), (356, 652)], 34, "#4E2C1A",
    foot=(354, 656), toe_ang=(155, 125, 95, 65), toe_len=15)

# --- head dressing -------------------------------------------------------------------------------
# snout sheen + jaw shade
d.path("M252,494 C268,474 300,466 332,472", "Snout sheen", fill=NONE,
       stroke="#E8B088", strokeWidth=6, opacity=30, cap="round")
d.path("M258,548 C290,560 328,562 356,554", "Jaw shade", fill=NONE,
       stroke="#0C0504", strokeWidth=10, opacity=40, cap="round")
# mouth line — the slight downturned grin
d.path("M248,534 C272,546 312,554 346,550", "Mouth", fill=NONE, stroke=INK,
       strokeWidth=4, cap="round")
d.shape("ellipse", "Nostril", x=252, y=506, width=7, height=5.5, fill=INK, opacity=75, stroke=NONE)
# the small dark eye, bead-ringed
d.shape("ellipse", "Eye rim", x=304, y=496, width=26, height=22,
        fill=rad("#6E4A2E", "#3A2214"), stroke=INK, strokeWidth=2.5)
d.shape("ellipse", "Eye", x=309, y=500, width=16, height=14,
        fill=rad("#4A2E1C", "#0E0604"), stroke=NONE)
d.shape("ellipse", "Eye glint", x=313, y=502, width=5, height=4, fill="#FFFFFF", opacity=80, stroke=NONE)
# ear slot behind the jowl + the neck crease where head meets trunk
d.path("M344,508 C352,514 354,526 348,536", "Ear slot", fill=NONE, stroke=INK,
       strokeWidth=4, opacity=70, cap="round")
d.path("M356,486 C366,510 366,542 354,566", "Neck crease", fill=NONE,
       stroke="#0C0504", strokeWidth=8, opacity=28, cap="round")

# dusk motes
for i, (x, y) in enumerate([(190, 300), (770, 210), (640, 150), (310, 200), (830, 360)]):
    assert on_disc(x, y, 20)
    d.shape("ellipse", f"Dust mote {i+1}", x=x - 4, y=y - 4, width=8, height=8,
            fill="#F0B078", opacity=30, stroke=NONE)

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#170B06", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F2C098", strokeWidth=3, opacity=24)

# --- name -----------------------------------------------------------------------------------------
r1 = d.text("GILA MONSTER", "Name", x=500, y=962, size=58, font="Virelai Sans",
            color="#F2D0B0", justify="center")

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

d.finish("gila-monster-V1R00")
