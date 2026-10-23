#!/usr/bin/env python3
"""Wingback armchair — furniture field plate V1R00. Near-side view with a
slight three-quarter from the front left: tall wings with rounded ears, rolled
arms in deep moss wool, a buttoned back, one worn arm cap, short walnut
cabriole legs. Warm room-dark plate. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420. The chair is modelled in 3D and drawn
with an oblique projection (affine, so Bezier control points project exactly)."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Wingback Armchair — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#2A1A12"   # warm umber, never black

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [dict(offset=o, color=c, **({"opacity": a} if a is not None else {}))
                      for o, c, a in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial", "stops": [
        dict(offset=o, color=c, **({"opacity": a} if a is not None else {})) for o, c, a in stops]}}

def on_disc(x, y, pad):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

# --- geometry constants ---------------------------------------------------------------
XO, XW = 200, 172        # outer side, wing inner face
XA = 130                 # arm inner face
YB, YS, YC = 72, 150, 196   # base bottom, deck, cushion top
YA = 262                 # arm top at the outer side
ZB0, ZB1 = 250, 300      # back slab
WING_TOP = 506

# --- projection: x right, y up, z back (pt) -----------------------------------------
# turned 28° so the near (left) side shows, seen from 12° above
CX, FY = 548, 770
TH, PH = math.radians(28), math.radians(12)
CT, ST, CP, SP = math.cos(TH), math.sin(TH), math.cos(PH), math.sin(PH)
def flare(x, y, z):
    """Wings angle outward from their hinge at the back, only above the arms."""
    if abs(x) < 168:
        return x
    t = min(1.0, max(0.0, (y - 280) / 170))
    s = t * t * (3 - 2 * t)
    return x + math.copysign(0.24 * max(0.0, ZB0 - z) * s, x)

def P(x, y, z):
    x = flare(x, y, z)
    depth = x * ST + z * CT
    return (CX + x * CT - z * ST, FY - (y * CP + depth * SP))

BOUNDS = []
def path3(ops):
    """ops: ('M', p) ('L', p) ('C', p1, p2, p3) ('Z',) with 3D points."""
    out = []
    for op in ops:
        k, pts = op[0], op[1:]
        xy = [P(*p) for p in pts]
        BOUNDS.extend(xy)
        out.append(k + " ".join("%.1f,%.1f" % q for q in xy))
    return " ".join(out)

def plane_x(x, pts2):
    """Points given as (z, y) in the plane x = const."""
    return [(op[0],) + tuple((x, y, z) for z, y in op[1:]) for op in pts2]

def plane_z(z, pts2):
    """Points given as (x, y) in the plane z = const."""
    return [(op[0],) + tuple((x, y, z) for x, y in op[1:]) for op in pts2]

# --- palette -------------------------------------------------------------------------
BG_GRAD = lin(0, 0, 0, 1000, (0, "#1E140E", None), (1, "#0A0604", None))
PLATE_GRAD = rad((0, "#5A3E2A", None), (0.55, "#3A2618", None), (1, "#1E130C", None))
FLOOR_GRAD = lin(0, 690, 0, 880, (0, "#2A1A10", 0), (0.35, "#2A1A10", 0.55), (1, "#140C07", 0.85))
LAMP_GLOW = rad((0, "#FFC27A", 0.30), (0.55, "#FFB060", 0.08), (1, "#FFB060", 0))

W_TOP = lin(0, 160, 0, 520, (0, "#7C9C70", None), (1, "#4A6844", None))
W_FRONT = lin(0, 520, 0, 720, (0, "#56764E", None), (1, "#2C4228", None))
W_SIDE = lin(220, 0, 420, 0, (0, "#1C2A1A", None), (1, "#34482F", None))
W_BACK = lin(0, 230, 0, 560, (0, "#668A5C", None), (0.6, "#46663F", None), (1, "#2E4429", None))
W_WING = lin(560, 0, 740, 0, (0, "#3C5636", None), (1, "#6A8C60", None))
W_SEAT = lin(0, 520, 0, 600, (0, "#4E6C46", None), (1, "#7EA072", None))
WALNUT = lin(0, 640, 0, 780, (0, "#7A4A2A", None), (0.5, "#4E2C18", None), (1, "#2E1A0E", None))
WALNUT_SIDE = lin(0, 640, 0, 780, (0, "#5A361E", None), (1, "#24140A", None))
PIPING = "#9AB88A"

# --- backdrop + plate ----------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880, fill="#6A4A30", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840, fill=PLATE_GRAD, stroke="#120A06", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8C49A", strokeWidth=3, opacity=28)
# warm lamp pool from the upper left
d.shape("ellipse", "Lamp glow", x=120, y=90, width=560, height=560, fill=LAMP_GLOW, stroke=NONE)
# floor band closes on the disc's own arc
FYB = 700
hw = math.sqrt(PR ** 2 - (FYB - PCY) ** 2)
d.path(f"M{PCX + hw:.1f},{FYB} L{PCX - hw:.1f},{FYB} A420,420 0 0 0 {PCX + hw:.1f},{FYB} Z",
       "Floor", fill=FLOOR_GRAD, stroke=NONE)
# floorboard seams, each closing on the arc
for i, yb in enumerate([742, 792, 846]):
    h = math.sqrt(PR ** 2 - (yb - PCY) ** 2) - 4
    d.path(f"M{PCX - h:.1f},{yb} L{PCX + h:.1f},{yb}", f"Floor seam {i+1}",
           fill=NONE, stroke="#5A3C26", strokeWidth=2, opacity=30)
# wainscot line on the wall, inside the disc
for i, yw in enumerate([520]):
    h = math.sqrt(PR ** 2 - (yw - PCY) ** 2) - 6
    d.path(f"M{PCX - h:.1f},{yw} L{PCX + h:.1f},{yw}", "Wainscot rail",
           fill=NONE, stroke="#7A5638", strokeWidth=3, opacity=22)

# --- shadow ---------------------------------------------------------------------------
sx, sy = P(0, 0, 150)
d.shape("ellipse", "Floor shadow", x=round(sx - 300), y=round(sy - 52), width=600, height=104,
        fill=rad((0, "#080402", 0.75), (0.7, "#080402", 0.35), (1, "#080402", 0)), stroke=NONE)

# --- legs (back pair first) -----------------------------------------------------------
def leg(label, x, z, fill, w0=24, w1=13):
    """Short cabriole leg: knee swells outward, ankle pinches, pad foot."""
    tx, ty = P(x, 72, z)
    bx, by = P(x, 0, z)
    s = 1 if x > 0 else -1
    dpath = ("M%.1f,%.1f L%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f "
             "C%.1f,%.1f %.1f,%.1f %.1f,%.1f L%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f "
             "C%.1f,%.1f %.1f,%.1f %.1f,%.1f Z") % (
        tx - w0/2, ty, tx + w0/2, ty,
        tx + w0/2 + s*6, ty + 22, tx + w1/2 - s*4, by - 22, bx + w1/2, by - 6,
        bx + w1/2 + 3, by - 2, bx + w1/2 + 3, by, bx + w1/2 + 2, by,
        bx - w1/2 - 2, by,
        bx - w1/2 - 3, by, bx - w1/2 - 3, by - 2, bx - w1/2, by - 6,
        tx - w1/2 - s*4, by - 22, tx - w0/2 + s*6, ty + 22, tx - w0/2, ty)
    BOUNDS.extend([(tx, ty), (bx, by)])
    d.path(dpath, label, fill=fill, stroke=INK, strokeWidth=3)
    d.path("M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (
        tx - w0/2 + 6, ty + 4, tx - w0/2 + 8 + s*4, ty + 22, tx - 2, by - 26, bx - 2, by - 8),
        label + " gloss", fill=NONE, stroke="#E0A878", strokeWidth=3, opacity=45, cap="round")

leg("Leg back right", 182, 282, WALNUT_SIDE)
leg("Leg back left", -182, 282, WALNUT_SIDE)


def wing_profile(rev=False):
    """(z, y) along the wing's free edge from the back down to the arm."""
    segs = [("L", (ZB0, 500)), ("L", (150, WING_TOP)),
            ("C", (96, 512), (56, 496), (54, 440)),
            ("C", (52, 400), (40, 330), (12, 290))]
    return segs

# --- left side panel (x = -200): base + arm + wing + back in one plane ------------------
side = [("M", (0, YB)), ("L", (ZB1, YB)), ("L", (ZB1, 500))] + wing_profile() + \
       [("L", (0, YA)), ("Z",)]
d.path(path3(plane_x(-XO, side)), "Side panel", fill=W_SIDE, stroke=INK, strokeWidth=4)
# soft lamp-side sheen down the wing's outer face, piping and shade on the lower panel
d.path(path3(plane_x(-XO, [("M", (236, 320)), ("C", (226, 410), (190, 480), (140, 496))])),
       "Side wing sheen", fill=NONE, stroke="#9AB88A", strokeWidth=16, opacity=14, cap="round")
d.path(path3(plane_x(-XO, [("M", (6, YB + 6)), ("L", (ZB1 - 6, YB + 6))])),
       "Side piping", fill=NONE, stroke=PIPING, strokeWidth=3, opacity=35, cap="round")
d.path(path3(plane_x(-XO, [("M", (0, YB)), ("L", (ZB1, YB)), ("L", (ZB1, YB + 40)), ("L", (0, YB + 40)), ("Z",)])),
       "Side skirt shade", fill="#060A05", opacity=28, stroke=NONE)
d.path(path3(plane_x(-XO, [("M", (20, YA - 10)), ("L", (ZB0 - 10, YA - 10))])),
       "Side arm roll light", fill=NONE, stroke="#9AB88A", strokeWidth=8, opacity=16, cap="round")

# --- back: top strip + inner face with deep buttoning -----------------------------------
def arch(x):  # top of the back, arched
    return 500 + 20 * (1 - (x / XO) ** 2)

top_strip = [("M", (-XO, 500, ZB0)), ("C", (-110, 522, ZB0), (110, 522, ZB0), (XO, 500, ZB0)),
             ("L", (XO, 500, ZB1)), ("C", (110, 522, ZB1), (-110, 522, ZB1), (-XO, 500, ZB1)), ("Z",)]
d.path(path3(top_strip), "Back top", fill=W_TOP, stroke=INK, strokeWidth=4)

back_face = [("M", (-XW, YC)), ("L", (-XW, arch(XW))),
             ("C", (-96, 521), (96, 521), (XW, arch(XW))), ("L", (XW, YC)), ("Z",)]
d.path(path3(plane_z(ZB0, back_face)), "Inside back", fill=W_BACK, stroke=INK, strokeWidth=4)

# buttons: alternate rows make the diamond grid
rows = [(452, [-120, -40, 40, 120]), (392, [-150, -80, 0, 80, 150]),
        (332, [-120, -40, 40, 120]), (272, [-150, -80, 0, 80, 150])]
btn = [(x, y) for y, xs in rows for x in xs]
# diamond puffs: a soft highlight inside each diamond, upper-left lit
for r in range(len(rows) - 1):
    ya, xa = rows[r]; yb, xb = rows[r + 1]
    for x in xa:
        for xx in xb:
            if abs(xx - x) < 45:
                pass
    for x in (xa if len(xa) < len(xb) else xb):
        cy = (ya + yb) / 2
        px, py = P(x, cy, ZB0)
        d.shape("ellipse", f"Tuft puff {r+1} {x}", x=round(px - 30), y=round(py - 22), width=48, height=34,
                fill=rad((0, "#A6C494", 0.42), (1, "#A6C494", 0)), stroke=NONE)
# pleats: each button to its diagonal neighbours
pairs = []
for r in range(len(rows) - 1):
    for x, y in [(x, rows[r][0]) for x in rows[r][1]]:
        for xx in rows[r + 1][1]:
            if 30 < abs(xx - x) < 50:
                pairs.append(((x, y), (xx, rows[r + 1][0])))
for i, (a, b) in enumerate(pairs):
    ax, ay = P(a[0], a[1], ZB0); bx, by = P(b[0], b[1], ZB0)
    d.path(f"M{ax:.1f},{ay:.1f} L{bx:.1f},{by:.1f}", f"Pleat {i+1}",
           fill=NONE, stroke="#1E2E1A", strokeWidth=3, opacity=55, cap="round")
    d.path(f"M{ax+2:.1f},{ay+2:.1f} L{bx+2:.1f},{by+2:.1f}", f"Pleat {i+1} light",
           fill=NONE, stroke="#B4D0A0", strokeWidth=1.6, opacity=30, cap="round")
# vertical pleats falling from the lowest row into the seat
for i, x in enumerate(rows[-1][1]):
    ax, ay = P(x, rows[-1][0], ZB0); bx, by = P(x, YC + 6, ZB0)
    d.path(f"M{ax:.1f},{ay:.1f} L{bx:.1f},{by:.1f}", f"Seat pleat {i+1}",
           fill=NONE, stroke="#1E2E1A", strokeWidth=3, opacity=40, cap="round")
for i, (x, y) in enumerate(btn):
    px, py = P(x, y, ZB0)
    d.shape("ellipse", f"Button {i+1} dimple", x=round(px - 9), y=round(py - 8), width=18, height=16,
            fill="#14200F", opacity=45, stroke=NONE)
    d.shape("ellipse", f"Button {i+1}", x=round(px - 5.5), y=round(py - 5.5), width=11, height=11,
            fill=rad((0, "#7E9E70", None), (1, "#2E4428", None)), stroke=INK, strokeWidth=1.5)
# shade under the back's top rail
d.path(path3(plane_z(ZB0, [("M", (-XW, arch(XW) - 2)), ("C", (-96, 519), (96, 519), (XW, arch(XW) - 2)),
                          ("L", (XW, arch(XW) - 40)), ("C", (96, 478), (-96, 478), (-XW, arch(XW) - 40)),
                          ("Z",)])),
       "Back top shade", fill="#0E180C", opacity=22, stroke=NONE)

# --- right wing (inner face visible) -----------------------------------------------------
rw = [("M", (ZB0, YC)), ("L", (ZB0, 500))] + wing_profile()[1:] + [("L", (12, YC)), ("Z",)]
d.path(path3(plane_x(XW, rw)), "Right wing inner", fill=W_WING, stroke=INK, strokeWidth=4)
d.path(path3(plane_x(XW, [("M", (200, 470)), ("C", (150, 486), (96, 480), (78, 430))])),
       "Right wing sheen", fill=NONE, stroke="#C2DCAE", strokeWidth=10, opacity=22, cap="round")
d.path(path3(plane_x(XW, [("M", (ZB0 - 4, YC + 8)), ("L", (ZB0 - 4, 494))])),
       "Right wing crease", fill=NONE, stroke="#14200F", strokeWidth=8, opacity=30, cap="round")

def wing_edge(x0, x1, label, fill):
    """The wing's thickness strip along its free edge (faces forward / up)."""
    pr = [("M", (ZB1, 500))] + wing_profile()
    a = path3(plane_x(x0, pr))
    pts = [(ZB1, 500), (ZB0, 500), (165, WING_TOP)]
    rev = [("M", (12, 290)), ("C", (40, 330), (52, 400), (54, 440)),
           ("C", (56, 496), (96, 512), (150, WING_TOP)), ("L", (ZB0, 500)), ("L", (ZB1, 500))]
    b = path3(plane_x(x1, rev)).replace("M", "L", 1)
    d.path(a + " " + b + " Z", label, fill=fill, stroke=INK, strokeWidth=4, join="round")

wing_edge(XW, XO, "Right wing edge", W_TOP)
# piping along both ears
for lbl, x in (("Left", -XO + 2), ("Right", XW + 2)):
    d.path(path3(plane_x(x, [("M", (ZB0, 502)), ("L", (150, WING_TOP + 2)),
                             ("C", (96, 514), (56, 498), (54, 442)),
                             ("C", (52, 402), (40, 332), (12, 292))])),
           f"{lbl} ear piping", fill=NONE, stroke=PIPING, strokeWidth=3, opacity=55, cap="round")

# --- arms + cushion ----------------------------------------------------------------------
def scroll(x_in, x_out):
    """Rolled-arm front profile (x, y) at z=0; the roll overhangs outward."""
    s = 1 if x_out > x_in else -1
    ov = x_out + s * 14
    return [("M", (x_in, YS)), ("L", (x_in, 248)),
            ("C", (x_in, 270), (x_in + s * 20, 286), (x_in + s * 42, 286)),
            ("C", (x_in + s * 62, 286), (ov, 278), (ov, 260)),
            ("C", (ov, 246), (x_out + s * 4, 240), (x_out, 238)),
            ("L", (x_out, YS)), ("Z",)]

def arm_top(x_in, x_out, label):
    s = 1 if x_out > x_in else -1
    ov = x_out + s * 14
    front = [(x_in, 248), (x_in + s * 42, 286), (ov, 260)]
    z1 = ZB0
    ops = [("M", (x_in, 250, 0)),
           ("C", (x_in, 270, 0), (x_in + s * 20, 286, 0), (x_in + s * 42, 286, 0)),
           ("C", (x_in + s * 62, 286, 0), (ov, 278, 0), (ov, 262, 0)),
           ("L", (ov, 262, z1)),
           ("C", (ov, 278, z1), (x_in + s * 62, 286, z1), (x_in + s * 42, 286, z1)),
           ("C", (x_in + s * 20, 286, z1), (x_in, 270, z1), (x_in, 250, z1)), ("Z",)]
    d.path(path3(ops), label, fill=W_TOP, stroke=INK, strokeWidth=4)
    d.path(path3([("M", (x_in + s * 40, 286, 8)), ("L", (x_in + s * 40, 286, z1 - 10))]),
           label + " crown light", fill=NONE, stroke="#C8E0B2", strokeWidth=6, opacity=30, cap="round")

# right arm: inner face, top
d.path(path3(plane_x(XA, [("M", (0, YS)), ("L", (ZB0, YS)), ("L", (ZB0, 250)), ("L", (0, 250)), ("Z",)])),
       "Right arm inner", fill=lin(0, 0, 0, 1, (0, "#3E5838", None), (1, "#24361F", None)),
       stroke=INK, strokeWidth=4)
arm_top(XA, XO, "Right arm top")

# cushion: top then front
cush_top = [("M", (-XA, YC, 4)), ("L", (XA, YC, 4)), ("L", (XA, YC, ZB0)), ("L", (-XA, YC, ZB0)), ("Z",)]
d.path(path3(cush_top), "Seat cushion top", fill=W_SEAT, stroke=INK, strokeWidth=4)
# shadow the back casts onto the seat
d.path(path3([("M", (-XA, YC, ZB0)), ("L", (XA, YC, ZB0)), ("L", (XA, YC, ZB0 - 70)),
              ("C", (40, YC, ZB0 - 40), (-40, YC, ZB0 - 40), (-XA, YC, ZB0 - 60)), ("Z",)]),
       "Seat back shadow", fill="#0E180C", opacity=30, stroke=NONE)
d.path(path3([("M", (-90, YC, 70)), ("C", (-30, YC, 90), (40, YC, 90), (96, YC, 64))]),
       "Seat sit-mark", fill=NONE, stroke="#B6D2A0", strokeWidth=10, opacity=18, cap="round")
cush_front = [("M", (-XA, YS + 4)), ("C", (-XA - 3, YC - 12), (-XA + 2, YC + 2), (-XA + 14, YC + 2)),
              ("L", (XA - 14, YC + 2)), ("C", (XA - 2, YC + 2), (XA + 3, YC - 12), (XA, YS + 4)), ("Z",)]
d.path(path3(plane_z(0, cush_front)), "Seat cushion front", fill=W_FRONT, stroke=INK, strokeWidth=4)
d.path(path3(plane_z(0, [("M", (-XA + 12, YC - 1)), ("L", (XA - 12, YC - 1))])),
       "Cushion piping", fill=NONE, stroke=PIPING, strokeWidth=3, opacity=60, cap="round")

# left arm: its outer face, then the top, then the wing that sits on it
d.path(path3(plane_x(-XO, [("M", (0, YS - 2)), ("L", (ZB0, YS - 2)), ("L", (ZB0, YA)), ("L", (0, YA)), ("Z",)])),
       "Left arm outer", fill=lin(250, 0, 400, 0, (0, "#1C2A1A", None), (1, "#30442C", None)), stroke=INK, strokeWidth=4)
d.path(path3(plane_x(-XO, [("M", (12, YA - 12)), ("L", (ZB0 - 10, YA - 12))])),
       "Left arm roll light", fill=NONE, stroke="#9AB88A", strokeWidth=8, opacity=18, cap="round")
arm_top(-XA, -XO, "Left arm top")
# left wing sits in front of the inside back: its outer face carries the ear silhouette
lw = [("M", (ZB0, 288)), ("L", (ZB0, 500))] + wing_profile()[1:] + [("L", (12, 288)), ("Z",)]
d.path(path3(plane_x(-XO, lw)), "Left wing outer",
       fill=lin(250, 0, 330, 0, (0, "#2A3E27", None), (1, "#48663F", None)), stroke=INK, strokeWidth=4)
d.path(path3(plane_x(-XO, [("M", (226, 330)), ("C", (220, 420), (180, 486), (120, 496))])),
       "Left wing sheen", fill=NONE, stroke="#B4D0A0", strokeWidth=12, opacity=16, cap="round")
d.path(path3(plane_x(-XO, [("M", (ZB0 - 6, 292)), ("L", (ZB0 - 6, 494))])),
       "Left wing hinge shade", fill=NONE, stroke="#0A1208", strokeWidth=10, opacity=30, cap="round")
wing_edge(-XO, -XW, "Left wing edge", W_TOP)

# --- front faces -----------------------------------------------------------------------------
skirt = [("M", (-XO, YB)), ("L", (XO, YB)), ("L", (XO, YS)), ("L", (-XO, YS)), ("Z",)]
d.path(path3(plane_z(0, skirt)), "Front rail", fill=W_FRONT, stroke=INK, strokeWidth=4)
d.path(path3(plane_z(0, [("M", (-XO + 6, YB + 6)), ("L", (XO - 6, YB + 6))])),
       "Front rail piping", fill=NONE, stroke=PIPING, strokeWidth=3, opacity=45, cap="round")
d.path(path3(plane_z(0, [("M", (-XO + 4, YB + 2)), ("L", (XO - 4, YB + 2)), ("L", (XO - 4, YB + 30)),
                          ("L", (-XO + 4, YB + 30)), ("Z",)])),
       "Front rail shade", fill="#0E180C", opacity=22, stroke=NONE)

for lbl, xi, xo in (("Right", XA, XO), ("Left", -XA, -XO)):
    d.path(path3(plane_z(0, scroll(xi, xo))), f"{lbl} arm front", fill=W_FRONT, stroke=INK, strokeWidth=4)
    s = 1 if xo > xi else -1
    cx_ = xi + s * 44
    # the scroll's spiral panel
    d.path(path3(plane_z(0, [("M", (xi + s * 10, 252)),
                             ("C", (xi + s * 12, 274), (xi + s * 40, 280), (xi + s * 56, 272)),
                             ("C", (xi + s * 70, 264), (xi + s * 66, 246), (xi + s * 50, 244)),
                             ("C", (xi + s * 38, 244), (xi + s * 36, 258), (xi + s * 46, 260))])),
           f"{lbl} scroll curl", fill=NONE, stroke="#1A2816", strokeWidth=3, opacity=70, cap="round")
    d.path(path3(plane_z(0, [("M", (xi + s * 8, 244)), ("L", (xi + s * 8, YS + 6))])),
           f"{lbl} arm panel seam", fill=NONE, stroke=PIPING, strokeWidth=3, opacity=40, cap="round")

# worn arm cap: the nap rubbed flat on the right arm's crown and scroll, paler and shinier
d.path(path3([("M", (140, 280, 2)), ("C", (156, 290, 4), (186, 290, 4), (206, 274, 2)),
              ("L", (206, 274, 110)), ("C", (186, 290, 120), (156, 290, 120), (140, 280, 100)), ("Z",)]),
       "Worn arm cap", fill=rad((0, "#C8C094", 0.62), (0.7, "#B8B488", 0.35), (1, "#B8B488", 0.08)), stroke=NONE)
d.path(path3(plane_z(0, [("M", (138, 262)), ("C", (142, 280), (160, 288), (178, 286)),
                         ("C", (196, 284), (210, 276), (212, 262)),
                         ("C", (196, 270), (160, 274), (138, 262)), ("Z",)])),
       "Worn scroll", fill=rad((0, "#D2C898", 0.70), (1, "#B8B488", 0.15)), stroke=NONE)

# front legs last
leg("Leg front right", 182, 14, WALNUT)
leg("Leg front left", -182, 14, WALNUT)

# --- sanity: whole chair well inside the disc ------------------------------------------------
worst = min(PR - math.hypot(x - PCX, y - PCY) for x, y in BOUNDS)
xs, ys = [b[0] for b in BOUNDS], [b[1] for b in BOUNDS]
print("bounds x %.0f..%.0f y %.0f..%.0f" % (min(xs), max(xs), min(ys), max(ys)))
print("min clearance to rim: %.1f" % worst)
assert worst > 20, worst

# --- captions ---------------------------------------------------------------------------------
def caption(txt, label, y, size, color, tracking=0):
    r = d.text(txt, label, x=500, y=y, size=size, font="Virelai Sans", color=color, justify="center")
    tid = (r or {}).get("id")
    if tracking and tid is not None:
        d.cmd("text.setStyle", f"{label} tracking", ids=[tid], tracking=tracking)
    return r

print(caption("WINGBACK ARMCHAIR", "Name", 930, 56, "#F0DEC4"))
print(caption("WALNUT · WOOL · HORSEHAIR", "Materials", 968, 22, "#C8A884", tracking=260))

d.finish("wingback-armchair-V1R00")
