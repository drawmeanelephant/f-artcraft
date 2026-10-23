#!/usr/bin/env python3
"""Plywood lounge chair — furniture field plate V1R00. Three-quarter view of
the low moulded-plywood lounge chair: a dished seat shell and a curved,
reclined back shell, both laminated so their edges show the ply stripes,
floating on a bent steel spine with splayed front and rear legs and rubber
feet. Tan wood against a cool grey plate. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420. Modelled in 3D, drawn with a rotated
orthographic projection; the shells are sampled surfaces."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Plywood Lounge Chair — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#2A1C12"   # warm umber, never black

def stops(*ss):
    return [dict(offset=o, color=c, **({"opacity": a} if a is not None else {})) for o, c, a in ss]

def lin(x0, y0, x1, y1, *ss):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1], "stops": stops(*ss)}}

def rad(*ss):
    return {"gradient": {"kind": "radial", "stops": stops(*ss)}}

# --- projection -----------------------------------------------------------------------------
CX, FY, SC = 614, 723, 0.82
TH, PH = math.radians(34), math.radians(24)
CT, ST, CP, SP = math.cos(TH), math.sin(TH), math.cos(PH), math.sin(PH)
BOUNDS = []

def P(x, y, z):
    depth = x * ST + z * CT
    return (CX + SC * (x * CT - z * ST), FY - SC * (y * CP + depth * SP))

def poly(pts3, close=True, track=True):
    xy = [P(*p) for p in pts3]
    if track:
        BOUNDS.extend(xy)
    s = "M%.1f,%.1f " % xy[0] + " ".join("L%.1f,%.1f" % q for q in xy[1:])
    return s + (" Z" if close else "")

def superellipse(a, b, n, k=96):
    out = []
    for i in range(k):
        t = 2 * math.pi * i / k
        c, s = math.cos(t), math.sin(t)
        out.append((a * math.copysign(abs(c) ** (2 / n), c), b * math.copysign(abs(s) ** (2 / n), s)))
    return out

# --- palette ------------------------------------------------------------------------------------
BG_GRAD = lin(0, 0, 0, 1000, (0, "#1A1E22", None), (1, "#090B0D", None))
PLATE_GRAD = rad((0, "#8A939C", None), (0.55, "#5E676F", None), (1, "#363D44", None))
FLOOR_GRAD = lin(0, 660, 0, 880, (0, "#2A3036", 0), (0.4, "#2A3036", 0.40), (1, "#1A1E22", 0.75))
WOOD_SEAT = lin(0, 420, 0, 640, (0, "#F0C890", None), (0.55, "#D6A065", None), (1, "#B07A44", None))
WOOD_BACK = lin(0, 200, 0, 520, (0, "#E6B87C", None), (0.6, "#C68E54", None), (1, "#A06A38", None))
EDGE_LIGHT, EDGE_DARK = "#F6E2C0", "#8E5E36"
STEEL = lin(0, 300, 0, 800, (0, "#4A4F56", None), (1, "#1C1F22", None))
RUBBER = rad((0, "#5A5048", None), (1, "#1E1A16", None))

# --- backdrop, plate, floor -------------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880, fill="#8A939C", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840, fill=PLATE_GRAD, stroke="#1E2328", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E4EAF0", strokeWidth=3, opacity=30)
d.shape("ellipse", "Soft key light", x=170, y=110, width=520, height=480,
        fill=rad((0, "#FFFFFF", 0.16), (1, "#FFFFFF", 0)), stroke=NONE)
FYB = 660
hw = math.sqrt(PR ** 2 - (FYB - PCY) ** 2)
d.path(f"M{PCX + hw:.1f},{FYB} L{PCX - hw:.1f},{FYB} A420,420 0 0 0 {PCX + hw:.1f},{FYB} Z",
       "Floor", fill=FLOOR_GRAD, stroke=NONE)
sx, sy = P(0, 0, 250)
d.shape("ellipse", "Floor shadow", x=round(sx - 270), y=round(sy - 60), width=540, height=120,
        fill=rad((0, "#14181C", 0.65), (0.7, "#14181C", 0.28), (1, "#14181C", 0)), stroke=NONE)
# shadow pools of the seat and back, projected straight down
seat_shadow = [(x, 0, z + 200) for x, z in superellipse(215, 200, 3.0, 48)]
d.path(poly(seat_shadow, track=False), "Seat shadow", fill="#101418", opacity=22, stroke=NONE)

# --- shells ----------------------------------------------------------------------------------------
T = 16   # ply thickness, pt

def seat_pt(x, z, t=0.0):
    w = max(0.0, (46 - z) / 46)
    y = 252 - 0.07 * z + 16 * (x / 215) ** 2 - 26 * w * w
    return (x, y - t, z)

SEAT_OUT = [(x * (1 + 0.06 * (200 - (z + 200)) / 200), z + 200) for x, z in superellipse(212, 198, 3.0)]

RECL = math.radians(16)
def back_pt(u, v, t=0.0):
    z = 432 + v * math.sin(RECL) - 40 * (u / 232) ** 2 + t * math.cos(RECL)
    y = 318 + v * math.cos(RECL) - t * math.sin(RECL)
    return (u, y, z)

BACK_OUT = [(u, v + 112) for u, v in superellipse(232, 112, 3.6)]
# the back is a touch wider across the top
BACK_OUT = [(u * (0.94 + 0.08 * v / 224), v) for u, v in BACK_OUT]

def laminated(label, outline, surf, face_fill, layers=8):
    """Draw a shell from its far skin up: alternating ply stripes, then the face."""
    for k in range(layers + 1):
        t = T * (1 - k / layers)
        col = EDGE_DARK if k % 2 == 0 else EDGE_LIGHT
        d.path(poly([surf(a, b, t) for a, b in outline], track=(k == 0)), f"{label} ply {k+1}",
               fill=col, stroke=INK if k == 0 else NONE, strokeWidth=3 if k == 0 else 0)
    d.path(poly([surf(a, b, 0) for a, b in outline]), f"{label} face", fill=face_fill, stroke=INK, strokeWidth=2.5)

# --- steel frame: rear legs, spine, back shell -----------------------------------------------------
def rod(label, pts3, w=8):
    xy = [P(*p) for p in pts3]
    BOUNDS.extend(xy)
    s = "M%.1f,%.1f " % xy[0] + " ".join("L%.1f,%.1f" % q for q in xy[1:])
    d.path(s, label, fill=NONE, stroke=STEEL, strokeWidth=w, cap="round", join="round")
    d.path(s, label + " glint", fill=NONE, stroke="#D8DEE4", strokeWidth=1.5, opacity=35, cap="round", join="round")

def bend(p0, p1, p2, n=10):
    out = []
    for i in range(n + 1):
        t = i / n
        u = 1 - t
        out.append(tuple(u * u * a + 2 * u * t * b + t * t * c for a, b, c in zip(p0, p1, p2)))
    return out

def foot(label, p):
    x, y = P(*p)
    BOUNDS.append((x, y + 6))
    d.shape("ellipse", label, x=round(x - 9), y=round(y - 7), width=18, height=13, fill=RUBBER, stroke=INK, strokeWidth=2)

RL, RR = (-206, 0, 492), (206, 0, 492)
rear = bend(RL, (-196, 120, 452), (-128, 192, 384)) + bend((128, 192, 384), (196, 120, 452), RR)
rod("Rear legs", rear)
foot("Foot rear left", RL); foot("Foot rear right", RR)
spine = bend((0, 194, 92), (0, 190, 240), (0, 192, 384)) + \
        bend((0, 192, 384), (0, 188, 470), (0, 270, 474))[1:] + [(0, 360, 470)]
rod("Spine", spine, w=9)
d.shape("ellipse", "Back shock mount", x=round(P(0, 362, 462)[0] - 10), y=round(P(0, 362, 462)[1] - 7),
        width=20, height=14, fill=RUBBER, stroke=INK, strokeWidth=2)

laminated("Back", BACK_OUT, back_pt, WOOD_BACK)
# veneer grain runs across the back, following its curve
for i, v in enumerate([40, 70, 100, 130, 160, 190]):
    span = 232 * (1 - abs((v - 112) / 112) ** 3.6) ** (1 / 3.6) * (0.94 + 0.08 * v / 224) - 26
    pts = [back_pt(-span + 2 * span * k / 24, v) for k in range(25)]
    d.path(poly(pts, close=False, track=False), f"Back grain {i+1}", fill=NONE,
           stroke="#9A622E", strokeWidth=1.6, opacity=26, cap="round")
d.path(poly([back_pt(-150 + 300 * k / 20, 168) for k in range(21)], close=False, track=False),
       "Back sheen", fill=NONE, stroke="#FFF2DC", strokeWidth=14, opacity=24, cap="round")
for side in (-1, 1):
    pts = [back_pt(side * 200, 40 + 150 * k / 12) for k in range(13)]
    d.path(poly(pts, close=False, track=False), f"Back curl shade {'L' if side < 0 else 'R'}", fill=NONE,
           stroke="#6A3E1C", strokeWidth=26, opacity=14, cap="round")
d.path(poly([back_pt(-110 + 220 * k / 20, 36) for k in range(21)], close=False, track=False),
       "Back lower shade", fill=NONE, stroke="#5A3418", strokeWidth=30, opacity=10, cap="round")

# --- front legs, then the seat ----------------------------------------------------------------------
FL, FR = (-214, 0, 18), (214, 0, 18)
front = bend(FL, (-204, 120, 52), (-134, 194, 92)) + bend((134, 194, 92), (204, 120, 52), FR)
rod("Front legs", front)
foot("Foot front left", FL); foot("Foot front right", FR)
laminated("Seat", SEAT_OUT, seat_pt, WOOD_SEAT)
for i, x in enumerate([-150, -100, -50, 0, 50, 100, 150]):
    a = 212 * (1 + 0.06 * 0)  # nominal
    span = 198 * (1 - abs(x / 222) ** 3.0) ** (1 / 3.0) - 30
    pts = [seat_pt(x * (1 + 0.04 * k / 24), 200 - span + 2 * span * k / 24) for k in range(25)]
    d.path(poly(pts, close=False, track=False), f"Seat grain {i+1}", fill=NONE,
           stroke="#A8703A", strokeWidth=1.6, opacity=24, cap="round")
d.path(poly([seat_pt(-120 + 240 * k / 20, 300) for k in range(21)], close=False, track=False),
       "Seat back dish shade", fill=NONE, stroke="#6A3E1C", strokeWidth=40, opacity=10, cap="round")
d.path(poly([seat_pt(-130 + 260 * k / 20, 80 + 10 * math.sin(math.pi * k / 20)) for k in range(21)],
            close=False, track=False),
       "Seat sheen", fill=NONE, stroke="#FFF4E0", strokeWidth=16, opacity=26, cap="round")
d.path(poly([seat_pt(-150 + 300 * k / 24, 22) for k in range(25)], close=False, track=False),
       "Waterfall edge light", fill=NONE, stroke="#FFF4E0", strokeWidth=4, opacity=45, cap="round")

# --- sanity -------------------------------------------------------------------------------------------
worst = min(PR - math.hypot(x - PCX, y - PCY) for x, y in BOUNDS)
xs, ys = [b[0] for b in BOUNDS], [b[1] for b in BOUNDS]
print("bounds x %.0f..%.0f y %.0f..%.0f" % (min(xs), max(xs), min(ys), max(ys)))
print("min clearance to rim: %.1f" % worst)
assert worst > 20, worst

def caption(txt, label, y, size, color, tracking=0):
    r = d.text(txt, label, x=500, y=y, size=size, font="Virelai Sans", color=color, justify="center")
    tid = (r or {}).get("id")
    if tracking and tid is not None:
        d.cmd("text.setStyle", f"{label} tracking", ids=[tid], tracking=tracking)
    return r

caption("PLYWOOD LOUNGE CHAIR", "Name", 930, 52, "#E8EEF2")
caption("ASH PLYWOOD · STEEL · RUBBER", "Materials", 968, 22, "#AEB8C2", tracking=240)

d.finish("plywood-lounge-chair-V1R00")
