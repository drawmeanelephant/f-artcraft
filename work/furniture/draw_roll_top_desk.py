#!/usr/bin/env python3
"""Roll-top desk — field plate V1R00. Twin-pedestal oak desk in three-quarter
view from the front-right, the tambour half-raised so its slats sweep over the
quarter-round hood as a light-to-dark gradient curve. Below the leading rail
(brass lock) the interior shows: pigeonholes with letters, one small drawer,
a leather writing surface. Study-dark plate. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Roll-top Desk — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#2B1A0C"   # warm umber, not black

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [round(x0, 1), round(y0, 1)],
            "end": [round(x1, 1), round(y1, 1)],
            "stops": [dict(offset=s[0], color=s[1], **({"opacity": s[2]} if len(s) > 2 else {}))
                      for s in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial", "stops": [
        dict(offset=s[0], color=s[1], **({"opacity": s[2]} if len(s) > 2 else {})) for s in stops]}}

def mix(c0, c1, t):
    a = [int(c0[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(p + (q - p) * t):02X}" for p, q in zip(a, b))

# --- projection: x right, y up, z toward the viewer; seen from front-right, above -------
TH = math.radians(34)
CT, ST = math.cos(TH), math.sin(TH)
K, VC = 0.42, 0.90

def proj(x, y, z):
    return (x * CT - z * ST, (x * ST + z * CT) * K - y * VC)

OPS = []   # collected in local screen space, fitted to the disc at the end

def poly(label, pts3, fill=None, stroke=INK, sw=2.5, opacity=None, g=None):
    OPS.append(("poly", label, [proj(*p) for p in pts3], fill, stroke, sw, opacity,
                None if g is None else (proj(*g[0]), proj(*g[1]), g[2])))

def line(label, pts3, stroke, sw, opacity=None):
    OPS.append(("line", label, [proj(*p) for p in pts3], NONE, stroke, sw, opacity, None))

def front(x0, x1, y0, y1, z):
    return [(x0, y1, z), (x1, y1, z), (x1, y0, z), (x0, y0, z)]

def side(x, z0, z1, y0, y1):
    return [(x, y1, z1), (x, y1, z0), (x, y0, z0), (x, y0, z1)]

def top(x0, x1, z0, z1, y):
    return [(x0, y, z0), (x1, y, z0), (x1, y, z1), (x0, y, z1)]

def disc_front(cx, cy, z, r, n=16):
    return [(cx + r * math.cos(i / n * math.tau), cy + r * math.sin(i / n * math.tau), z) for i in range(n)]

# oak palette
TOP_ST = [(0, "#E2B374"), (0.6, "#C99350"), (1, "#A8743A")]
FRONT_ST = [(0, "#C48B48"), (1, "#93602C")]
SIDE_ST = [(0, "#8E5D2C"), (1, "#5E3C1B")]
DRAWER_ST = [(0, "#D19A55"), (1, "#A06A31")]
DARK_ST = [(0, "#2A1A0E"), (1, "#140C06")]
BRASS = [(0, "#F6DE96"), (0.5, "#CFA04A"), (1, "#8A6224")]
LEATHER = [(0, "#4C6B45"), (1, "#2C4229")]

W, D, H = 520, 300, 300        # body width, depth, writing height (top of carcase)
KX0, KX1 = 176, 344            # kneehole
BAND = 56                      # centre drawer band height
SLAB = 14
Y0 = H + SLAB                  # writing surface level

def fg(x0, x1, y0, y1, z, st):     # vertical gradient on a front rect
    return ((x0, y1, z), (x0 + (x1 - x0) * 0.25, y0, z), st)

def bail(nm, cx, cy, z):
    poly(f"{nm} backplate", [(cx - 18, cy + 6, z), (cx + 18, cy + 6, z), (cx + 18, cy - 6, z), (cx - 18, cy - 6, z)],
         sw=2, g=((cx - 18, cy + 6, z), (cx + 18, cy - 6, z), BRASS))
    pts = [(cx - 14 * math.cos(a / 10 * math.pi), cy - 2 - 12 * math.sin(a / 10 * math.pi), z) for a in range(11)]
    line(f"{nm} bail", pts, "#7A5420", 5.5)
    line(f"{nm} bail light", pts[1:6], "#F8E2A0", 2.6, 80)

def keyhole(nm, cx, cy, z):
    poly(f"{nm} escutcheon", disc_front(cx, cy, z, 8, 14), sw=2, g=((cx - 8, cy + 8, z), (cx + 8, cy - 8, z), BRASS))
    poly(f"{nm} keyhole", [(cx - 1.6, cy + 3, z), (cx + 1.6, cy + 3, z), (cx + 2.4, cy - 4, z), (cx - 2.4, cy - 4, z)],
         fill="#2A1A0C", stroke=NONE)

def drawer(nm, x0, x1, y0, y1, z, pull=True):
    poly(f"{nm} front", front(x0, x1, y0, y1, z), sw=2.5, g=fg(x0, x1, y0, y1, z, DRAWER_ST))
    line(f"{nm} bevel light", [(x0 + 3, y0 + 3, z), (x0 + 3, y1 - 3, z), (x1 - 3, y1 - 3, z)], "#F0C88A", 2.4, 55)
    line(f"{nm} bevel shade", [(x1 - 3, y1 - 3, z), (x1 - 3, y0 + 3, z), (x0 + 3, y0 + 3, z)], "#5E3A18", 2.4, 50)
    for k in range(3):   # quarter-sawn ray fleck
        fx = x0 + (x1 - x0) * (0.22 + 0.27 * k)
        fy = y0 + (y1 - y0) * (0.35 + 0.18 * (k % 2))
        line(f"{nm} ray fleck {k+1}", [(fx, fy, z), (fx + 16, fy + 2, z)], "#F3D29C", 2.2, 40)
    if pull:
        bail(f"{nm} pull", (x0 + x1) / 2, (y0 + y1) / 2 + 4, z)

# --- carcase -------------------------------------------------------------------------
# kneehole interior first; the fronts around it are drawn over its edges
poly("Kneehole back", front(KX0, KX1, 0, H - BAND, 70), stroke=NONE, g=((KX0, H - BAND, 70), (KX0, 0, 70), DARK_ST))
poly("Kneehole left wall", side(KX0, 70, D, 0, H - BAND), stroke=NONE,
     g=((KX0, 0, 70), (KX0, 0, D), [(0, "#24160B"), (1, "#5B3A1C")]))
poly("Kneehole floor shade", top(KX0, KX1, 70, D, 0), stroke=NONE,
     g=((KX0, 0, 70), (KX0, 0, D), [(0, "#0C0704", 0.8), (1, "#0C0704", 0.2)]))

for nm, x0, x1 in [("Left plinth", -5, KX0 + 4), ("Right plinth", KX1 - 4, W + 5)]:
    poly(f"{nm} front", front(x0, x1, 0, 16, D + 5), g=fg(x0, x1, 0, 16, D + 5, SIDE_ST))
    poly(f"{nm} top", top(x0, x1, D, D + 5, 16), stroke=NONE, fill="#B98345", opacity=80)
poly("Right plinth side", side(W + 5, -5, D + 5, 0, 16), g=((W + 5, 16, D), (W + 5, 16, 0), SIDE_ST))

for nm, x0, x1 in [("Left pedestal", 0, KX0), ("Right pedestal", KX1, W)]:
    poly(f"{nm} front", front(x0, x1, 16, H - BAND, D), g=fg(x0, x1, 16, H - BAND, D, FRONT_ST))
    hh = (H - BAND - 16 - 4 * 8) / 3
    for k in range(3):
        y0 = 16 + 8 + k * (hh + 8)
        drawer(f"{nm} drawer {3-k}", x0 + 12, x1 - 12, y0, y0 + hh, D)
poly("Centre band front", front(0, W, H - BAND, H, D), g=fg(0, W, H - BAND, H, D, FRONT_ST))
drawer("Centre drawer", KX0, KX1, H - BAND + 8, H - 8, D, pull=False)
keyhole("Centre drawer", (KX0 + KX1) / 2, H - BAND / 2, D)
for nm, x0, x1 in [("Left frieze drawer", 12, KX0 - 12), ("Right frieze drawer", KX1 + 12, W - 12)]:
    drawer(nm, x0, x1, H - BAND + 8, H - 8, D)
# right side: frame and raised panel
poly("Carcase right side", side(W, 0, D, 16, H), g=((W, H, D), (W, 16, 0), SIDE_ST))
poly("Right side panel", side(W, 30, D - 30, 46, H - 30), sw=2, g=((W, H, D), (W, 16, 0), [(0, "#9C6834"), (1, "#6A4420")]))
line("Right side panel light", [(W, 48, D - 32), (W, H - 32, D - 32), (W, H - 32, 32)], "#D8A562", 2.4, 50)

# writing slab
SX0, SX1, SZ0, SZ1 = -8, W + 8, -4, D + 18
poly("Writing slab top", top(SX0, SX1, SZ0, SZ1, Y0), sw=3, g=((SX0, Y0, SZ0), (SX1, Y0, SZ1), TOP_ST))
poly("Leather writing surface", top(26, W - 26, 140, D + 2, Y0), sw=2, g=((26, Y0, 140), (W - 26, Y0, D), LEATHER))
line("Leather tooling", [(36, Y0, 150), (W - 36, Y0, 150), (W - 36, Y0, D - 8), (36, Y0, D - 8), (36, Y0, 150)], "#D9B860", 2.2, 70)
poly("Leather sheen", top(80, 250, 150, D - 8, Y0), stroke=NONE,
     g=((80, Y0, 150), (250, Y0, D), [(0, "#E8F0D8", 0.14), (1, "#E8F0D8", 0)]))
poly("Writing slab front edge", front(SX0, SX1, H, Y0, SZ1), sw=3, g=fg(SX0, SX1, H, Y0, SZ1, FRONT_ST))
poly("Writing slab right edge", side(SX1, SZ0, SZ1, H, Y0), sw=3, g=((SX1, Y0, SZ1), (SX1, Y0, SZ0), SIDE_ST))
line("Slab edge highlight", [(SX0 + 4, Y0, SZ1), (SX1 - 2, Y0, SZ1), (SX1, Y0, SZ0 + 4)], "#F6D49C", 2.4, 75)

# --- superstructure -------------------------------------------------------------------
PT = 16                         # side panel thickness
HOOD = 250                      # hood height above the writing surface
HZ, PRZ, PRY = 60, 186, HOOD    # panel curve: centre z, radii
TRZ, TRY = 168, 236             # tambour curve (inside the panel groove)
CAB_Z, CAB_H = 130, 190         # pigeonhole cabinet front + height

def panel_curve(n=24):
    return [(HZ + PRZ * math.sin(i / n * math.pi / 2), Y0 + PRY * math.cos(i / n * math.pi / 2)) for i in range(n + 1)]

def tamb(phi, extra=0):
    return HZ + (TRZ + extra) * math.sin(phi), Y0 + (TRY + extra) * math.cos(phi)

poly("Hood back panel", front(PT, W - PT, Y0, Y0 + HOOD, 10), stroke=NONE, g=((0, Y0 + HOOD, 10), (0, Y0, 10), DARK_ST))
prof = [(0, Y0)] + [(HZ - 60, Y0 + HOOD)] + panel_curve()
poly("Left panel inner face", [(PT, y, z) for z, y in prof], stroke=NONE,
     g=((PT, Y0, 0), (PT, Y0, 240), [(0, "#3A2412"), (1, "#7A4F26")]))

# pigeonhole cabinet
X0c, X1c = PT, W - PT
poly("Cabinet top", top(X0c, X1c, 10, CAB_Z, Y0 + CAB_H), sw=2, g=((0, Y0 + CAB_H, 10), (0, Y0 + CAB_H, CAB_Z), FRONT_ST))
poly("Cabinet face", front(X0c, X1c, Y0, Y0 + CAB_H, CAB_Z), sw=2.5,
     g=((X0c, Y0 + CAB_H, CAB_Z), (X1c, Y0, CAB_Z), [(0, "#C8914C"), (1, "#8E5C2A")]))

def cubby(nm, x0, x1, y0, y1, letters=0, tint=0):
    z = CAB_Z
    poly(f"{nm} void", front(x0, x1, y0, y1, z), sw=2, g=((x0, y1, z), (x0, y0, z), DARK_ST))
    poly(f"{nm} floor", [(x0, y0, z), (x1, y0, z), (x1, y0, z - 34), (x0, y0, z - 34)], stroke=NONE,
         g=((x0, y0, z - 34), (x0, y0, z), [(0, "#4A2E15", 0.2), (1, "#A06C34", 0.9)]))
    poly(f"{nm} left wall", [(x0, y1, z), (x0, y1, z - 30), (x0, y0, z - 30), (x0, y0, z)], stroke=NONE,
         g=((x0, y0, z), (x0, y0, z - 30), [(0, "#8E5C2A", 0.9), (1, "#3A2412", 0.3)]))
    for j in range(letters):
        lx0 = x0 + 8 + j * 12 + tint * 6
        poly(f"{nm} letter {j+1}", [(lx0, y0 + 2, z - 8), (lx0 + 30, y0 + 2, z - 8), (lx0 + 32, y0 + (y1 - y0) * 0.62, z - 8),
                                    (lx0 + 2, y0 + (y1 - y0) * 0.66, z - 8)], sw=1.8,
             g=((lx0, y0 + 40, z), (lx0 + 30, y0, z), [(0, "#F7EBD0"), (1, "#CDBA92")]))

# bottom row: slot · one small drawer · slot; two rows of pigeonholes above
cw = X1c - X0c
cubby("Low slot left", X0c + 8, X0c + cw * 0.36, Y0 + 8, Y0 + 54, letters=2)
drawer("Small drawer", X0c + cw * 0.36 + 8, X0c + cw * 0.64 - 8, Y0 + 8, Y0 + 54, CAB_Z, pull=False)
sx = X0c + cw / 2
poly("Small drawer knob", disc_front(sx, Y0 + 31, CAB_Z, 7), sw=2, g=((sx - 7, Y0 + 38, CAB_Z), (sx + 7, Y0 + 24, CAB_Z), BRASS))
cubby("Low slot right", X0c + cw * 0.64, X1c - 8, Y0 + 8, Y0 + 54, letters=1, tint=2)
n = 6
for r, (y0, y1) in enumerate([(Y0 + 62, Y0 + 122), (Y0 + 130, Y0 + CAB_H - 8)]):
    for c in range(n):
        x0 = X0c + 8 + c * (cw - 16) / n
        cubby(f"Pigeonhole r{r+1}c{c+1}", x0 + 4, x0 + (cw - 16) / n - 4, y0, y1,
              letters=(1 if (r * 5 + c * 3) % 4 == 0 else 0) + (1 if (r + c) % 5 == 2 else 0), tint=c % 2)

# tambour: slats from the top down to the half-raised leading rail
PHI_LEAD = math.radians(51)
NS = 16
TX0, TX1 = PT, W - PT
LIGHT, DARKC = "#F7D498", "#6A4220"
for i in range(NS):
    p0, p1 = PHI_LEAD * i / NS, PHI_LEAD * (i + 1) / NS
    (z0, y0), (z1, y1) = tamb(p0), tamb(p1)
    t = (i + 0.5) / NS
    c0, c1 = mix(LIGHT, DARKC, t * 0.85), mix(LIGHT, DARKC, min(1, t * 0.85 + 0.18))
    poly(f"Tambour slat {i+1}", [(TX0, y0, z0), (TX1, y0, z0), (TX1, y1, z1), (TX0, y1, z1)], sw=2.2,
         g=((TX0, y0, z0), (TX1, y1, z1), [(0, c0), (1, c1)]))
    line(f"Tambour slat {i+1} light", [(TX0 + 2, y0 - 2, z0 + 1.5), (TX1 - 2, y0 - 2, z0 + 1.5)], "#FFE7B8", 2, 30 + 30 * (1 - t))
# leading rail: proud lip with the lock in its face
(za, ya), (zb, yb) = tamb(PHI_LEAD), tamb(PHI_LEAD, 14)
(zc, yc) = tamb(PHI_LEAD + 0.06, 14)
(zd, yd) = tamb(PHI_LEAD + 0.06)
poly("Tambour rail top", [(TX0, ya, za), (TX1, ya, za), (TX1, yb, zb), (TX0, yb, zb)], sw=2.2,
     g=((TX0, ya, za), (TX1, ya, za), [(0, "#B37A3C"), (1, "#8A5A2A")]))
poly("Tambour rail face", [(TX0, yb, zb), (TX1, yb, zb), (TX1, yc, zc), (TX0, yc, zc)], sw=2.5,
     g=((TX0, yb, zb), (TX1, yc, zc), [(0, "#A86F35"), (1, "#6A4320")]))
poly("Tambour rail underside", [(TX0, yd, zd), (TX1, yd, zd), (TX1, yc, zc), (TX0, yc, zc)], sw=2,
     g=((TX0, yd, zd), (TX0, yc, zc), [(0, "#3A2412"), (1, "#5E3C1B")]))
mx = (TX0 + TX1) / 2
zl, yl = (zb + zc) / 2, (yb + yc) / 2
poly("Lock escutcheon", [(mx - 24, yl + 13, zl + 4), (mx + 24, yl + 13, zl + 4), (mx + 24, yl - 13, zl - 4), (mx - 24, yl - 13, zl - 4)],
     sw=2.4, g=((mx - 24, yl + 13, zl), (mx + 24, yl - 13, zl), BRASS))
poly("Lock keyhole", [(mx - 2.6, yl + 6, zl + 3), (mx + 2.6, yl + 6, zl + 3), (mx + 3.6, yl - 7, zl - 2), (mx - 3.6, yl - 7, zl - 2)],
     fill="#2A1A0C", stroke=NONE)
line("Lock glint", [(mx - 19, yl + 9, zl + 4), (mx - 5, yl + 9, zl + 4)], "#FFF4CC", 2.4, 85)
for nm, kx in [("left", TX0 + 70), ("right", TX1 - 70)]:
    poly(f"Tambour knob {nm}", [(kx + 9 * math.cos(a / 14 * math.tau), yl + 9 * math.sin(a / 14 * math.tau), zl + 2) for a in range(14)],
         sw=2.2, g=((kx - 9, yl + 9, zl), (kx + 9, yl - 9, zl), BRASS))

# side panels: curved edge strips, right outer face
curve = panel_curve()
for nm, xa, xb in [("Left", 0, PT), ("Right", W - PT, W)]:
    poly(f"{nm} hood edge", [(xa, y, z) for z, y in curve] + [(xb, y, z) for z, y in reversed(curve)], sw=2.5,
         g=((xa, Y0 + HOOD, HZ), (xb, Y0, HZ + PRZ), [(0, "#E7B676"), (1, "#9C6834")]))
poly("Right hood panel", [(W, y, z) for z, y in prof], sw=3, g=((W, Y0 + HOOD, 0), (W, Y0, 240), SIDE_ST))
inner = [(HZ + (PRZ - 34) * math.sin(i / 16 * math.pi / 2), Y0 + 26 + (PRY - 58) * math.cos(i / 16 * math.pi / 2)) for i in range(17)]
poly("Right hood raised panel", [(W, Y0 + 26, 24), (W, Y0 + PRY - 32, 24)] + [(W, y, z) for z, y in inner], sw=2,
     g=((W, Y0 + HOOD, 0), (W, Y0, 220), [(0, "#A06C36"), (1, "#6A4420")]))
line("Right hood panel light", [(W, Y0 + 28, 26), (W, Y0 + PRY - 34, 26)] + [(W, y + 2, z - 2) for z, y in inner[:6]], "#D8A562", 2.4, 50)

# top board
BX0, BX1, BZ0, BZ1, BY = -6, W + 6, -6, HZ + 14, Y0 + HOOD
poly("Top board", top(BX0, BX1, BZ0, BZ1, BY + 16), sw=3, g=((BX0, BY, BZ0), (BX1, BY, BZ1), TOP_ST))
poly("Top board front", front(BX0, BX1, BY, BY + 16, BZ1), sw=3, g=fg(BX0, BX1, BY, BY + 16, BZ1, FRONT_ST))
poly("Top board right", side(BX1, BZ0, BZ1, BY, BY + 16), sw=3, g=((BX1, BY, BZ1), (BX1, BY, BZ0), SIDE_ST))
line("Top board highlight", [(BX0 + 4, BY + 16, BZ1), (BX1 - 2, BY + 16, BZ1), (BX1, BY + 16, BZ0 + 4)], "#F6D49C", 2.4, 75)

FLOOR_N = 0
# --- fit to the disc ------------------------------------------------------------------
xs = [p[0] for op in OPS for p in op[2]]
ys = [p[1] for op in OPS for p in op[2]]
bw, bh = max(xs) - min(xs), max(ys) - min(ys)
SC = min(580 / bw, 540 / bh)
OX = 500 - SC * (min(xs) + max(xs)) / 2
OY = 470 - SC * (min(ys) + max(ys)) / 2

def S(p):
    return (OX + SC * p[0], OY + SC * p[1])

def path_of(pts, closed):
    q = [S(p) for p in pts]
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in q) + (" Z" if closed else "")

screen = [S(p) for op in OPS for p in op[2]]
for x, y in screen:
    assert math.hypot(x - PCX, y - PCY) <= PR - 26, (x, y)
FOOT_Y = max(y for _, y in screen)
print("fit: scale %.3f  bbox x %.0f..%.0f  y %.0f..%.0f" % (
    SC, min(s[0] for s in screen), max(s[0] for s in screen), min(s[1] for s in screen), FOOT_Y))

# --- backdrop + plate -------------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin(0, 0, 0, 1000, (0, "#171A14"), (1, "#070806")), stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#3E4632"), (0.6, "#283022"), (1, "#151A12")), stroke=NONE)
# lamplight pooling from the upper left
d.shape("ellipse", "Lamplight", x=150, y=90, width=520, height=460,
        fill=rad((0, "#FFD99A", 0.20), (1, "#FFD99A", 0)), stroke=NONE)
# wainscot panels on the study wall, behind the desk
for i, x in enumerate([150, 770]):
    d.path(f"M{x},400 L{x + 80},400 L{x + 80},600 L{x},600 Z", f"Wainscot panel {i+1}",
           fill=lin(x, 400, x, 600, (0, "#4A533C", 0.5), (1, "#1E2419", 0.2)), stroke="#5E6A4C", strokeWidth=3, opacity=30)
for nm, yy in [("Chair rail", 380)]:
    xx = math.sqrt(PR ** 2 - (yy - PCY) ** 2) - 4
    d.path(f"M{PCX - xx:.1f},{yy} L{PCX + xx:.1f},{yy}", nm, fill=NONE, stroke="#6E7A58", strokeWidth=4, opacity=30)
for i, (x, y, w) in enumerate([(210, 210, 6), (780, 250, 7), (170, 620, 6), (820, 600, 7), (420, 100, 6), (610, 96, 7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w, fill="#6E7A58", opacity=40, stroke=NONE)

HZN = 640
hx = math.sqrt(PR ** 2 - (HZN - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{HZN} L{PCX + hx:.1f},{HZN} A420,420 0 0 1 {PCX - hx:.1f},{HZN} Z", "Floor",
       fill=lin(0, HZN, 0, 880, (0, "#5A4630", 0.6), (1, "#221A12", 0.9)), stroke=NONE)
for i, yy in enumerate([690, 750, 815]):
    xx = math.sqrt(PR ** 2 - (yy - PCY) ** 2) - 6
    d.path(f"M{PCX - xx:.1f},{yy} L{PCX + xx:.1f},{yy}", f"Floorboard seam {i+1}",
           fill=NONE, stroke="#16100A", strokeWidth=3, opacity=30)
d.shape("ellipse", "Desk shadow", x=210, y=FOOT_Y - 80, width=600, height=130,
        fill=rad((0, "#0A0704", 0.65), (1, "#0A0704", 0)), stroke=NONE)

# --- the desk -----------------------------------------------------------------------------
for kind, label, pts, fill, stroke, sw, op, g in OPS:
    kw = {}
    if g is not None and kind == "poly":
        s0, s1, stops = g
        a, b = S(s0), S(s1)
        if abs(a[0] - b[0]) + abs(a[1] - b[1]) < 1:
            b = (a[0], a[1] + 1)
        fill = lin(a[0], a[1], b[0], b[1], *stops)
    if op is not None:
        kw["opacity"] = op
    if kind == "poly":
        d.path(path_of(pts, True), label, fill=fill, stroke=stroke,
               **({"strokeWidth": sw, "join": "round"} if stroke != NONE else {}), **kw)
    else:
        d.path(path_of(pts, False), label, fill=NONE, stroke=stroke, strokeWidth=sw, cap="round", join="round", **kw)

d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840, fill=NONE, stroke="#0C0E09", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D9C79A", strokeWidth=3, opacity=26)

# --- name + second line ---------------------------------------------------------------------
d.text("ROLL-TOP DESK", "Name", x=500, y=940, size=58, font="Virelai Sans", color="#F0E2C4", justify="center")
LINE2, SZ2, TRK = "OAK · LEATHER · BRASS", 22, 300
r = d.text(LINE2, "Second line", x=500, y=975, size=SZ2, font="Virelai Sans", color="#C2AE7E", justify="center")
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

d.finish("roll-top-desk-V1R00")
