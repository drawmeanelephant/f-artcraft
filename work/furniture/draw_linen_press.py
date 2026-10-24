#!/usr/bin/env python3
"""Linen press — field plate V1R00. A pine press: two fielded doors up top,
the left one swung open on the sliding trays that hold the household's
folded wealth — one tray pulled halfway out under a sprig of lavender —
over two deep drawers. Seen from front-right, above. Lavender plate,
keepsake mood. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Linen Press — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#1C1408"

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [round(x0, 1), round(y0, 1)],
            "end": [round(x1, 1), round(y1, 1)],
            "stops": [dict(offset=s[0], color=s[1], **({"opacity": s[2]} if len(s) > 2 else {}))
                      for s in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial", "stops": [
        dict(offset=s[0], color=s[1], **({"opacity": s[2]} if len(s) > 2 else {})) for s in stops]}}

# --- projection: x right, y up, z toward the viewer; seen from front-right, above ---
TH = math.radians(28)
CT, ST = math.cos(TH), math.sin(TH)
K, VC = 0.40, 0.95

def proj(x, y, z):
    return (x * CT - z * ST, (x * ST + z * CT) * K - y * VC)

OPS = []

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

# pine + linen palette
FRONT_ST = [(0, "#D9A75C"), (1, "#9C6C30")]
SIDE_ST  = [(0, "#96682E"), (1, "#5E3C18")]
TOP_ST   = [(0, "#E8BC74"), (0.6, "#C08E48"), (1, "#8A5C26")]
DOOR_ST  = [(0, "#DCAC60"), (1, "#A3742F")]
INNER_ST = [(0, "#B8894C"), (1, "#6E4820")]
TRAY_ST  = [(0, "#E4BE80"), (1, "#AE7F40")]
LINEN_ST = [(0, "#F4EEDD"), (0.6, "#DDD2B4"), (1, "#B0A080")]
LINEN2_ST= [(0, "#DCE4E8"), (0.6, "#B4C2CC"), (1, "#8498A6")]   # blue-tinged set
LAV_S, LAV_T = "#5A7A4A", "#8E68B8"                            # lavender sprig
BRASS    = [(0, "#F6DE96"), (0.5, "#CFA04A"), (1, "#8A6224")]

W, D = 270, 125
FOOT = 24
B0, B1 = FOOT, FOOT + 150       # drawer base
H0, H1 = B1 + 14, B1 + 14 + 330 # press section (rail above the drawers)
CORN = 18
DZ = D

# --- press interior: back, left wall, trays + folded linen -----------------------------
poly("Cavity back", front(16, W - 16, H0 + 8, H1 - 8, 20), stroke=NONE,
     g=((16, H1 - 8, 20), (W - 16, H0 + 8, 20), [(0, "#C79A58"), (1, "#7E5424")]))
poly("Cavity left inner", side(16, 20, DZ, H0 + 8, H1 - 8), stroke=NONE,
     g=((16, H1 - 8, DZ), (16, H0 + 8, 20), INNER_ST))
poly("Cavity floor", top(16, W - 16, 20, DZ, H0 + 8), stroke=NONE,
     g=((16, H0 + 8, DZ), (W - 16, H0 + 8, 20), [(0, "#B07C3E"), (1, "#6E4620")]))
poly("Cavity ceiling", top(16, W - 16, 20, DZ, H1 - 8), stroke=NONE, fill="#3A2410")

def tray(nm, y0, pull=0):
    """Sliding tray: bottom board + front board + side cheeks when pulled."""
    z0, z1 = 24, DZ - 10 + pull
    x0, x1 = 20, W - 20
    poly(nm + " board", top(x0, x1, z0, z1 - 8, y0 + 8), sw=1.8,
         g=((x0, y0 + 8, z1), (x1, y0 + 8, z0), TRAY_ST))
    poly(nm + " front", front(x0, x1, y0, y0 + 10, z1), sw=1.8,
         g=((x0, y0 + 10, z1), (x1, y0, z1), [(0, "#D6A860"), (1, "#8A5C26")]))
    if pull:
        # side cheeks: shallow boards standing on the tray ends
        poly(nm + " cheek R", side(x1 - 6, z1 - 26, z1, y0 + 8, y0 + 22), sw=1.6,
             g=((x1 - 6, y0 + 22, z1), (x1 - 6, y0 + 8, z1 - 26), [(0, "#C89A58"), (1, "#8A5C26")]))
        poly(nm + " cheek L", side(x0 + 2, z1 - 26, z1, y0 + 8, y0 + 22), sw=1.6,
             g=((x0 + 2, y0 + 22, z1), (x0 + 2, y0 + 8, z1 - 26), [(0, "#B8884A"), (1, "#6E4420")]))
    line(nm + " lip light", [(x0 + 4, y0 + 10, z1 + 0.4), (x1 - 4, y0 + 10, z1 + 0.4)],
         "#F0D8A0", 2, 55)

def linens(nm, x0, y0, z, n, w, palette):
    """A stack of n folded cloths: rounded-end bands with fold seams."""
    hh = 0
    for i in range(n):
        h = 13 - i * 1.2
        pts = [(x0, y0 + hh, z), (x0 + w, y0 + hh, z),
               (x0 + w - 2, y0 + hh + h, z), (x0 + 2, y0 + hh + h, z)]
        poly(f"{nm} {i+1}", pts, sw=1.5,
             g=((x0, y0 + hh + h, z), (x0 + w, y0 + hh, z), palette))
        line(f"{nm} fold {i+1}", [(x0 + 5, y0 + hh + h * 0.45, z + 0.4),
                                  (x0 + w - 5, y0 + hh + h * 0.45, z + 0.4)],
             "#A89878" if palette is LINEN_ST else "#7E92A0", 1.8, 45)
        hh += h + 1.5
    return hh

TRAY_Y = [H0 + 78, H0 + 168, H0 + 250]
# bottom tray + its linen pile
tray("Tray low", TRAY_Y[0])
linens("Low pile", 40, TRAY_Y[0] + 10, DZ - 22, 3, 88, LINEN_ST)
# middle tray + two piles
tray("Tray mid", TRAY_Y[1])
linens("Mid pile A", 36, TRAY_Y[1] + 10, DZ - 24, 4, 78, LINEN_ST)
linens("Mid pile B", 160, TRAY_Y[1] + 10, DZ - 22, 3, 70, LINEN2_ST)
# folded cloths on the cavity floor beside the trays
linens("Floor pile", 40, H0 + 10, DZ - 26, 3, 96, LINEN2_ST)

# --- carcass shell ----------------------------------------------------------------------
poly("Right side", side(W, 0, DZ, B0, H1), sw=2.5,
     g=((W, H1, DZ), (W, B0, 0), SIDE_ST))
poly("Right side top sliver", top(W - 10, W, 0, DZ, H1), stroke=NONE, fill="#4A2E10")
# face frame around the press opening
poly("Press left stile", front(0, 16, H0, H1, DZ + 1), sw=2.2,
     g=((0, H1, DZ), (16, H0, DZ), FRONT_ST))
poly("Press right stile", front(W - 16, W, H0, H1, DZ + 1), sw=2.2,
     g=((W - 16, H1, DZ), (W, H0, DZ), FRONT_ST))
poly("Press centre stile", front(W / 2 - 4, W / 2 + 4, H0, H1, DZ + 1), sw=2,
     g=((W / 2 - 4, H1, DZ), (W / 2 + 4, H0, DZ), FRONT_ST))
poly("Press top rail", front(0, W, H1 - 12, H1, DZ + 1), sw=2.2,
     g=((0, H1, DZ), (W, H1 - 12, DZ), FRONT_ST))
poly("Press bottom rail", front(0, W, H0, H0 + 10, DZ + 1), sw=2.2,
     g=((0, H0 + 10, DZ), (W, H0, DZ), FRONT_ST))
# the rail band between press and drawers
poly("Mid band", front(-4, W + 4, B1, H0, DZ + 2), sw=2.2,
     g=((-4, H0, DZ + 2), (W + 4, B1, DZ + 2), [(0, "#C08E48"), (1, "#7E5020")]))
poly("Mid band side", side(W + 4, 0, DZ + 2, B1, H0), sw=2,
     g=((W + 4, H0, DZ), (W + 4, B1, 0), SIDE_ST))

# --- closed right door: two fielded panels ----------------------------------------------
DX0, DX1 = W / 2 + 4, W - 16
DY0, DY1 = H0 + 10, H1 - 12
poly("Right door", front(DX0, DX1, DY0, DY1, DZ + 8), sw=2.4,
     g=((DX0, DY1, DZ + 8), (DX1, DY0, DZ + 8), DOOR_ST))

def field(nm, x0, x1, y0, y1, z):
    m = 6
    poly(nm + " field", front(x0, x1, y0, y1, z), sw=1.8,
         g=((x0, y1, z), (x1, y0, z), [(0, "#C08E48"), (1, "#8A5824")]))
    line(nm + " shade", [(x0 - m, y1 + m, z), (x1 + m, y1 + m, z), (x1 + m, y0 - m, z)],
         "#5E3C14", 2.2, 65)
    line(nm + " light", [(x1 + m, y0 - m, z), (x0 - m, y0 - m, z), (x0 - m, y1 + m, z)],
         "#F0CC8E", 2.2, 60)

PX0, PX1 = DX0 + 12, DX1 - 12
field("RD upper", PX0, PX1, DY0 + (DY1 - DY0) * 0.5, DY1 - 14, DZ + 9)
field("RD lower", PX0, PX1, DY0 + 14, DY0 + (DY1 - DY0) * 0.42, DZ + 9)
# knob on the meeting stile
kx, ky = DX0 + 10, (DY0 + DY1) / 2
poly("RD knob", [(kx + 4.4 * math.cos(a / 12 * math.tau), ky + 4.4 * math.sin(a / 12 * math.tau),
                  DZ + 10) for a in range(12)], sw=1.4,
     g=((kx - 4, ky + 4, DZ), (kx + 4, ky - 4, DZ), BRASS))

# --- the pulled top tray + its linens + lavender — in front of frame and doors ------------
tray("Tray top", TRAY_Y[2], pull=34)
linens("Top pile", 52, TRAY_Y[2] + 10, DZ + 12, 3, 84, LINEN_ST)
linens("Top pile 2", 168, TRAY_Y[2] + 10, DZ + 8, 2, 64, LINEN2_ST)
# lavender sprig across the top pile: two stems + bud tufts as small lozenges
lx0 = 60
line("Lavender stem 1", [(lx0, TRAY_Y[2] + 56, DZ + 16), (lx0 + 38, TRAY_Y[2] + 98, DZ + 18)],
     LAV_S, 2.8)
line("Lavender stem 2", [(lx0 + 10, TRAY_Y[2] + 54, DZ + 14), (lx0 + 52, TRAY_Y[2] + 90, DZ + 16)],
     LAV_S, 2.8)
for i in range(6):
    u = i / 5
    for j, (sx0, sy0, col) in enumerate(((lx0 + 28 + 10 * u, TRAY_Y[2] + 82 + 16 * u, LAV_T),
                                         (lx0 + 40 + 10 * u, TRAY_Y[2] + 74 + 16 * u, "#7A58A0"))):
        pts = [(sx0 - 3, sy0, DZ + 17), (sx0, sy0 + 5, DZ + 17.5),
               (sx0 + 3, sy0 + 8, DZ + 17), (sx0, sy0 + 3, DZ + 16.5)]
        poly(f"Lav bud {j}{i}", pts, stroke=NONE, fill=col, opacity=88)

# --- the open left door, hinged on the left stile, swung ~50 deg -------------------------
A = math.radians(36)
CA, SA = math.cos(A), math.sin(A)
HX, HZ = 16, DZ + 8
DL0, DL1 = 16, W / 2 - 4
DT = 8

def dpt(x, y, off):
    """Door-local point: x across the leaf, off = 0 outer face / DT inner face."""
    return (HX + (x - HX) * CA - off * SA, y, HZ + (x - HX) * SA + off * CA)

poly("Open door inner", [dpt(DL0, DY0, DT), dpt(DL1, DY0, DT),
                         dpt(DL1, DY1, DT), dpt(DL0, DY1, DT)], sw=2.4,
     g=(dpt(DL0, DY1, DT), dpt(DL1, DY0, DT), INNER_ST))
poly("Open door edge", [dpt(DL1, DY0, DT), dpt(DL1, DY0, 0),
                        dpt(DL1, DY1, 0), dpt(DL1, DY1, DT)], sw=2,
     g=(dpt(DL1, DY1, 0), dpt(DL1, DY0, DT), [(0, "#8A5C26"), (1, "#4A2E10")]))
poly("Open door outer", [dpt(DL0, DY0, 0), dpt(DL1, DY0, 0),
                         dpt(DL1, DY1, 0), dpt(DL0, DY1, 0)], sw=2.4,
     g=(dpt(DL0, DY1, 0), dpt(DL1, DY0, 0), DOOR_ST))
# inner-face panel hints
for i, (v0, v1) in enumerate([(DY0 + 14, DY0 + (DY1 - DY0) * 0.42),
                              (DY0 + (DY1 - DY0) * 0.5, DY1 - 14)]):
    u0, u1 = DL0 + 14, DL1 - 14
    line(f"OD panel {i+1} a", [dpt(u0, v0, DT + 0.5), dpt(u0, v1, DT + 0.5),
                               dpt(u1, v1, DT + 0.5)], "#7E5424", 2.2, 70)
    line(f"OD panel {i+1} b", [dpt(u1, v1, DT + 0.5), dpt(u1, v0, DT + 0.5),
                               dpt(u0, v0, DT + 0.5)], "#4A2E10", 2.2, 70)
# knob + hinges
kp = dpt(DL1 - 10, (DY0 + DY1) / 2, DT)
poly("OD knob", [(kp[0] + 4.4 * math.cos(a / 12 * math.tau),
                  kp[1] + 4.4 * math.sin(a / 12 * math.tau), kp[2] + 0.6)
                 for a in range(12)], sw=1.4,
     g=((kp[0] - 4, kp[1] + 4, kp[2]), (kp[0] + 4, kp[1] - 4, kp[2]), BRASS))
for i, hy in enumerate([DY0 + 40, DY1 - 40]):
    poly(f"Hinge {i+1}", front(HX - 5, HX + 3, hy - 15, hy + 15, DZ + 9), sw=1.5,
         g=((HX - 5, hy + 15, DZ), (HX + 3, hy - 15, DZ), BRASS))

# --- cornice -----------------------------------------------------------------------------
CX0, CX1, CZ0, CZ1 = -8, W + 8, -8, D + 8
poly("Cornice side", side(CX1, CZ0, CZ1, H1, H1 + CORN), sw=2.4,
     g=((CX1, H1 + CORN, CZ1), (CX1, H1, CZ0), SIDE_ST))
poly("Cornice front", front(CX0, CX1, H1, H1 + CORN, CZ1), sw=2.4,
     g=((CX0, H1 + CORN, CZ1), (CX1, H1, CZ1), FRONT_ST))
poly("Cornice top", top(CX0, CX1, CZ0, CZ1, H1 + CORN), sw=2.4,
     g=((CX0, H1 + CORN, CZ0), (CX1, H1 + CORN, CZ1), TOP_ST))
line("Cornice light", [(CX0 + 4, H1 + CORN - 2.5, CZ1 + 1), (CX1 - 4, H1 + CORN - 2.5, CZ1 + 1)],
     "#F0D0A0", 2.4, 55)

# --- drawer base ---------------------------------------------------------------------------
for j, (dy0, dy1) in enumerate(((B0 + 6, B0 + 76), (B0 + 80, B1 - 4))):
    poly(f"Drawer {j+1}", front(8, W - 8, dy0, dy1, DZ + 1), sw=2.4,
         g=((8, dy1, DZ), (W - 8, dy0, DZ), DOOR_ST))
    field(f"Drawer {j+1}", 22, W - 22, dy0 + 12, dy1 - 10, DZ + 2)
    for i, bx in enumerate((W * 0.34, W * 0.66)):
        by = (dy0 + dy1) / 2
        poly(f"Drawer {j+1} pull {i+1}",
             [(bx + 5 * math.cos(a / 12 * math.tau), by + 5 * math.sin(a / 12 * math.tau),
               DZ + 3) for a in range(12)], sw=1.4,
             g=((bx - 5, by + 5, DZ), (bx + 5, by - 5, DZ), BRASS))

# bracket feet + apron
for nm, fx in (("L", 0), ("R", W - 28)):
    poly(f"Foot {nm}", [(fx + 4, FOOT, DZ + 2), (fx + 24, FOOT, DZ + 2),
                        (fx + 26, FOOT + 10, DZ + 2), (fx + 16, FOOT + 16, DZ + 2),
                        (fx + 6, FOOT + 16, DZ + 2)], sw=2,
         g=((fx, FOOT + 16, DZ), (fx, FOOT, DZ), [(0, "#8A5C26"), (1, "#462C0E")]))
poly("Apron face", front(6, W - 6, B0 - 4, B0 + 4, DZ + 1), sw=2,
     g=((0, B0 + 4, DZ), (W, B0 - 4, DZ), [(0, "#9C6C30"), (1, "#5E3C18")]))

# --- fit to the disc --------------------------------------------------------------------------
xs = [p[0] for op in OPS for p in op[2]]
ys = [p[1] for op in OPS for p in op[2]]
bw, bh = max(xs) - min(xs), max(ys) - min(ys)
SC = min(560 / bw, 560 / bh)
OX = 500 - SC * (min(xs) + max(xs)) / 2
OY = 480 - SC * (min(ys) + max(ys)) / 2

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

# --- backdrop + plate ----------------------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin(0, 0, 0, 1000, (0, "#141018"), (1, "#060408")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#7A6890", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#503E58"), (0.6, "#332438"), (1, "#150E18")),
        stroke="#0E0810", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8C4E0", strokeWidth=3, opacity=24)
d.shape("ellipse", "Window light", x=200, y=110, width=580, height=560,
        fill=rad((0, "#E8D8F0", 0.13), (0.6, "#C8B0D8", 0.05), (1, "#C8B0D8", 0)), stroke=NONE)

HZN = 690
hx = math.sqrt(PR ** 2 - (HZN - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{HZN} L{PCX + hx:.1f},{HZN} A420,420 0 0 1 {PCX - hx:.1f},{HZN} Z", "Floor",
       fill=lin(0, HZN, 0, 880, (0, "#2A2030", 0.55), (1, "#0E0810", 0.9)), stroke=NONE)
d.shape("ellipse", "Press shadow", x=255, y=FOOT_Y - 34, width=500, height=86,
        fill=rad((0, "#050305", 0.65), (1, "#050305", 0)), stroke=NONE)

# --- the press ------------------------------------------------------------------------------------
for kind, label, pts, fill, stroke, sw, op, g in OPS:
    kw = {}
    if g is not None and kind == "poly":
        s0, s1, stops_ = g
        a, b = S(s0), S(s1)
        if abs(a[0] - b[0]) + abs(a[1] - b[1]) < 1:
            b = (a[0], a[1] + 1)
        fill = lin(a[0], a[1], b[0], b[1], *stops_)
    if op is not None:
        kw["opacity"] = op
    if kind == "poly":
        d.path(path_of(pts, True), label, fill=fill, stroke=stroke,
               **({"strokeWidth": sw, "join": "round"} if stroke != NONE else {}), **kw)
    else:
        d.path(path_of(pts, False), label, fill=NONE, stroke=stroke, strokeWidth=sw,
               cap="round", join="round", **kw)

d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840, fill=NONE, stroke="#0C0810", strokeWidth=6)

# --- captions ---------------------------------------------------------------------------------------
d.text("LINEN PRESS", "Name", x=500, y=940, size=58, font="Virelai Sans",
       color="#F0E8DC", justify="center")
LINE2, SZ2, TRK = "PINE · LINEN · BRASS", 22, 300
r = d.text(LINE2, "Second line", x=500, y=975, size=SZ2, font="Virelai Sans",
           color="#C4B0CC", justify="center")
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

d.finish("linen-press-V1R00")
