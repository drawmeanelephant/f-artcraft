#!/usr/bin/env python3
"""Armoire — field plate V1R00. The wardrobe as architecture: a cherry
provincial armoire, arched crown, two fielded-panel doors — the left one
swung open on the rail and the coats that hang from it. Seen from
front-right, above. Cherry plate, provincial mood. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Armoire — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#1E0E08"

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [round(x0, 1), round(y0, 1)],
            "end": [round(x1, 1), round(y1, 1)],
            "stops": [dict(offset=s[0], color=s[1], **({"opacity": s[2]} if len(s) > 2 else {}))
                      for s in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial", "stops": [
        dict(offset=s[0], color=s[1], **({"opacity": s[2]} if len(s) > 2 else {})) for s in stops]}}

# --- projection: x right, y up, z toward the viewer; seen from front-right, above ---
TH = math.radians(30)
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

# cherry palette
FRONT_ST = [(0, "#A85838"), (1, "#74301C")]
SIDE_ST  = [(0, "#6E3520"), (1, "#3E1808")]
TOP_ST   = [(0, "#BC6C48"), (0.6, "#96492A"), (1, "#6A2C16")]
DOOR_ST  = [(0, "#B26040"), (1, "#7C341E")]
INNER_ST = [(0, "#7E3E20"), (1, "#4A1E0C")]
DARK_ST  = [(0, "#1E0E06"), (1, "#0C0502")]
BRASS    = [(0, "#F6DE96"), (0.5, "#CFA04A"), (1, "#8A6224")]
IRON     = "#3A3430"

W, D, H = 340, 150, 540      # body box
FOOT, PLINTH = 26, 30        # bun feet + shaped plinth apron
CORN = 26                    # cornice band
B0 = FOOT + PLINTH           # body bottom = 56
CO, CD = 14, 12              # cornice overhang / crown crest
DOOR_T = 10
DZ = D                       # front plane of the carcass

# --- feet + shaped plinth -------------------------------------------------------------------
for nm, fx in [("L", 30), ("R", W - 58)]:
    poly(f"Bun foot {nm}", front(fx, fx + 28, 0, FOOT, D), sw=2,
         g=((fx, FOOT, D), (fx, 0, D), [(0, "#6A3018"), (1, "#341608")]))
poly("Rear foot hint", side(W, D - 56, D - 28, 0, FOOT), stroke=NONE, fill="#2A1208")
# plinth apron: a shallow serpentine — low flat face with a centre swallow cut
serp = []
for t in range(25):
    u = t / 24
    x = u * W
    y = FOOT + 10 * math.sin(math.pi * u) ** 2 - 6 * math.sin(math.pi * u)
    serp.append((x, y, D + 2))
poly("Plinth apron", [(0, B0, D + 2), (W, B0, D + 2)] + [(x, y, z) for x, y, z in reversed(serp)],
     sw=2.4, g=((0, B0, D + 2), (W, FOOT, D + 2), [(0, "#8E4426"), (1, "#5A2410")]))
poly("Plinth right", side(W, 0, D + 2, FOOT, B0), sw=2,
     g=((W, B0, D), (W, FOOT, 0), SIDE_ST))

# --- carcass: right side, then the open left half ---------------------------------------------
poly("Right side", side(W, 0, D, B0, H), sw=2.5,
     g=((W, H, D), (W, B0, 0), SIDE_ST))

# interior of the open left half: back wall, left wall, floor, ceiling shadow
OX0, OX1 = 8, W / 2 - 2          # opening under the (removed) left door
OY0, OY1 = B0 + 8, H - 12
poly("Cavity back", front(OX0 + 4, OX1, OY0, OY1, 16), stroke=NONE,
     g=((OX0 + 4, OY1, 16), (OX1, OY0, 16), DARK_ST))
poly("Cavity floor", top(OX0 + 4, OX1, 16, DZ, OY0), stroke=NONE,
     g=((OX0 + 4, OY0, DZ), (OX1, OY0, 16), [(0, "#3A1C0C"), (1, "#180C04")]))
poly("Cavity ceiling", top(OX0 + 4, OX1, 16, DZ, OY1), stroke=NONE, fill="#0E0602")
poly("Cavity left wall", side(OX0 + 4, 16, DZ, OY0, OY1), stroke=NONE,
     g=((OX0 + 4, OY1, DZ), (OX0 + 4, OY0, 16), [(0, "#4A2410"), (1, "#1E0E04")]))

# the hanging rail: brass rod on iron sockets, mid-depth
RY = OY1 - 92
RZ = DZ * 0.52
line("Rail", [(OX0 + 10, RY, RZ), (OX1 - 8, RY, RZ)], "#C8A258", 5.5)
line("Rail light", [(OX0 + 10, RY + 1.5, RZ), (OX1 - 8, RY + 1.5, RZ)], "#F6DE96", 2, 70)
for sx in (OX0 + 12, OX1 - 10):
    poly(f"Rail socket {sx:.0f}", front(sx - 5, sx + 5, RY - 8, RY + 8, RZ - 3), stroke=NONE, fill=IRON)

# generations of coats: three silhouettes on hangers, oldest darkest
def coat(nm, cx, hem, half_w, col):
    """Hanger + coat silhouette at the rail depth; hem is the bottom y."""
    line(f"{nm} hook", [(cx, RY - 2, RZ), (cx, RY + 10, RZ), (cx + 4, RY + 14, RZ)], "#8A8274", 2.6)
    line(f"{nm} hanger", [(cx - half_w * 0.7, RY - 26, RZ), (cx, RY - 2, RZ),
                          (cx + half_w * 0.7, RY - 26, RZ)], "#8A8274", 2.6)
    pts = [(cx - half_w * 0.7, RY - 26, RZ + 1), (cx - half_w, RY - 40, RZ + 1),
           (cx - half_w * 0.92, hem + 30, RZ + 1), (cx - half_w * 0.8, hem, RZ + 1),
           (cx + half_w * 0.8, hem, RZ + 1), (cx + half_w * 0.92, hem + 30, RZ + 1),
           (cx + half_w, RY - 40, RZ + 1), (cx + half_w * 0.7, RY - 26, RZ + 1)]
    poly(nm, pts, stroke=NONE,
         g=((cx - half_w, RY - 26, RZ), (cx + half_w, hem, RZ),
            [(0, col[0]), (1, col[1])]))

coat("Greatcoat", 44, 210, 34, ("#3A3230", "#1C1814"))
coat("Walking jacket", 88, 268, 28, ("#4A3424", "#241408"))
coat("Town coat", 130, 236, 26, ("#33402E", "#1A2216"))
# a scarf slipped over the rail end
poly("Scarf", [(OX1 - 22, RY + 2, RZ + 1), (OX1 - 10, RY + 2, RZ + 1),
               (OX1 - 12, 296, RZ + 1), (OX1 - 24, 300, RZ + 1)],
     stroke=NONE, g=((OX1 - 22, RY, RZ), (OX1 - 12, 298, RZ), [(0, "#6E2A20"), (1, "#3A140E")]))

# carcass front: stiles and rails framing the opening, and the closed right door
poly("Top rail front", front(0, W, H - 14, H, DZ + 2), sw=2.4,
     g=((0, H, DZ + 2), (W, H - 14, DZ + 2), FRONT_ST))
poly("Left stile", front(0, 8, B0, H - 14, DZ + 2), sw=2.2,
     g=((0, H, DZ + 2), (8, B0, DZ + 2), FRONT_ST))
poly("Bottom rail front", front(0, W, B0, B0 + 8, DZ + 2), sw=2.2,
     g=((0, B0 + 8, DZ + 2), (W, B0, DZ + 2), FRONT_ST))
poly("Centre stile", front(W / 2 - 2, W / 2 + 6, B0 + 8, H - 14, DZ + 2), sw=2,
     g=((W / 2 - 2, H, DZ + 2), (W / 2 + 6, B0, DZ + 2), FRONT_ST))
poly("Right stile", front(W - 8, W, B0, H - 14, DZ + 2), sw=2.2,
     g=((W - 8, H, DZ + 2), (W, B0, DZ + 2), FRONT_ST))

# --- closed right door: two fielded panels, arched upper --------------------------------------
DX0, DX1 = W / 2 + 8, W - 8
DY0, DY1 = B0 + 10, H - 16
poly("Right door", front(DX0, DX1, DY0, DY1, DZ + DOOR_T), sw=2.4,
     g=((DX0, DY1, DZ + DOOR_T), (DX1, DY0, DZ + DOOR_T), DOOR_ST))

def panel(nm, x0, x1, y0, y1, arch=0):
    """Raised panel: moulding ring, bevel, field. arch = crown height of an arched top."""
    m = 7
    if arch:
        pts = [(x0, y0, DZ + DOOR_T + 1), (x0, y1 - arch, DZ + DOOR_T + 1)]
        ax = (x0 + x1) / 2
        ar = (x1 - x0) / 2
        for i in range(1, 13):
            a = math.pi - math.pi * i / 12
            pts.append((ax + ar * math.cos(a), y1 - arch + arch * math.sin(a), DZ + DOOR_T + 1))
        pts.append((x1, y0, DZ + DOOR_T + 1))
    else:
        pts = front(x0, x1, y0, y1, DZ + DOOR_T + 1)
    poly(f"{nm} field", pts, sw=1.8,
         g=((x0, y1, DZ), (x1, y0, DZ), [(0, "#9A4E30"), (1, "#6A2A14")]))
    # moulding shadow + light
    line(f"{nm} mould shade", [(x0 - m, y1 + m, DZ + DOOR_T + 1), (x1 + m, y1 + m, DZ + DOOR_T + 1),
                               (x1 + m, y0 - m, DZ + DOOR_T + 1)], "#381606", 2.4, 65)
    line(f"{nm} mould light", [(x1 + m, y0 - m, DZ + DOOR_T + 1), (x0 - m, y0 - m, DZ + DOOR_T + 1),
                               (x0 - m, y1 + m, DZ + DOOR_T + 1)], "#D88A5C", 2.4, 60)
    line(f"{nm} bevel", [(x0 + 3, y0 + 3, DZ + DOOR_T + 2), (x0 + 3, y1 - 3, DZ + DOOR_T + 2)],
         "#E09A68", 2, 45)

PX0, PX1 = DX0 + 12, DX1 - 12
panel("Upper panel", PX0, PX1, DY0 + (DY1 - DY0) * 0.42, DY1 - 14, arch=26)
panel("Lower panel", PX0, PX1, DY0 + 14, DY0 + (DY1 - DY0) * 0.36)
# escutcheon on the meeting stile side
EX, EY = DX0 + 13, (DY0 + DY1) / 2
poly("Escutcheon", [(EX + 6 * math.cos(a / 14 * math.tau), EY + 10 * math.sin(a / 14 * math.tau),
                     DZ + DOOR_T + 2) for a in range(14)], sw=1.6,
     g=((EX - 6, EY + 10, DZ), (EX + 6, EY - 10, DZ), BRASS))
poly("Keyhole", front(EX - 1.5, EX + 1.5, EY - 3, EY + 2, DZ + DOOR_T + 3), stroke=NONE, fill="#1E0E04")

# --- the open left door, hinged on the left stile, swung ~50 deg -----------------------------
A = math.radians(46)
CA, SA = math.cos(A), math.sin(A)
HX, HZ = 8, DZ + DOOR_T        # hinge line at the door's outer face corner
DL0, DL1 = 8, W / 2 - 4        # door width when closed
DT = DOOR_T

def dpt(x, y, off):
    """Door-local point: x across the leaf, off = 0 outer face / DT inner face."""
    return (HX + (x - HX) * CA - off * SA, y, HZ + (x - HX) * SA + off * CA)

# inner face (toward the viewer): panels hinted darker
poly("Open door inner", [dpt(DL0, DY0, DT), dpt(DL1, DY0, DT), dpt(DL1, DY1, DT), dpt(DL0, DY1, DT)],
     sw=2.4, g=(dpt(DL0, DY1, DT), dpt(DL1, DY0, DT), INNER_ST))
# free-edge stile face
poly("Open door edge", [dpt(DL1, DY0, DT), dpt(DL1, DY0, 0), dpt(DL1, DY1, 0), dpt(DL1, DY1, DT)],
     sw=2, g=(dpt(DL1, DY1, 0), dpt(DL1, DY0, DT), [(0, "#5A2A14"), (1, "#321204")]))
# outer face sliver
poly("Open door outer", [dpt(DL0, DY0, 0), dpt(DL1, DY0, 0), dpt(DL1, DY1, 0), dpt(DL0, DY1, 0)],
     sw=2.4, g=(dpt(DL0, DY1, 0), dpt(DL1, DY0, 0), [(0, "#6A2E16"), (1, "#421A08")]))
# panel mouldings hinted on the inner face
for i, (u0, u1, v0, v1) in enumerate([(14, DL1 - 20, DY0 + 14, DY0 + (DY1 - DY0) * 0.36),
                                      (14, DL1 - 20, DY0 + (DY1 - DY0) * 0.42, DY1 - 14)]):
    line(f"Inner panel {i+1} a", [dpt(u0, v0, DT + 1), dpt(u0, v1, DT + 1), dpt(u1, v1, DT + 1)],
         "#5E2A14", 2.2, 70)
    line(f"Inner panel {i+1} b", [dpt(u1, v1, DT + 1), dpt(u1, v0, DT + 1), dpt(u0, v0, DT + 1)],
         "#2A1208", 2.2, 70)
# hinges on the left stile
for i, hy in enumerate([DY0 + 40, DY1 - 40]):
    poly(f"Hinge {i+1}", front(HX - 4, HX + 4, hy - 16, hy + 16, DZ + DOOR_T + 2), sw=1.6,
         g=((HX - 4, hy + 16, DZ), (HX + 4, hy - 16, DZ), BRASS))

# --- cornice + crest ---------------------------------------------------------------------------
CX0, CX1, CZ0, CZ1 = -CO, W + CO, -CO, D + CO
poly("Cornice side", side(CX1, CZ0, CZ1, H, H + CORN), sw=2.4,
     g=((CX1, H + CORN, CZ1), (CX1, H, CZ0), SIDE_ST))
poly("Cornice front", front(CX0, CX1, H, H + CORN, CZ1), sw=2.4,
     g=((CX0, H + CORN, CZ1), (CX1, H, CZ1), FRONT_ST))
poly("Cornice top", top(CX0, CX1, CZ0, CZ1, H + CORN), sw=2.4,
     g=((CX0, H + CORN, CZ0), (CX1, H + CORN, CZ1), TOP_ST))
line("Cornice light", [(CX0 + 4, H + CORN + 1, CZ1 - 3), (CX1 - 4, H + CORN + 1, CZ1 - 3)], "#E8A870", 2.6, 60)
# serpentine crest along the cornice front: a shallow arch rising at centre
crest = [(CX0 + 30, H + CORN + 2, CZ1 + 2)]
for i in range(1, 25):
    u = i / 24
    x = CX0 + 30 + (CX1 - CX0 - 60) * u
    y = H + CORN + 2 + CD * math.sin(math.pi * u) ** 1.4
    crest.append((x, y, CZ1 + 2))
crest.append((CX1 - 30, H + CORN + 2, CZ1 + 2))
poly("Crest", crest + [(CX1 - 30, H + CORN - 6, CZ1 + 2), (CX0 + 30, H + CORN - 6, CZ1 + 2)],
     sw=2.2, g=((CX0, H + CORN + CD, CZ1), (CX1, H + CORN - 6, CZ1),
                [(0, "#B06040"), (1, "#7A3018")]))
line("Crest light", crest[2:14], "#E8A870", 2.6, 60)

# --- fit to the disc ---------------------------------------------------------------------------
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

# --- backdrop + plate ---------------------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin(0, 0, 0, 1000, (0, "#160D0A"), (1, "#070302")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#7A5A50", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#5E2836"), (0.6, "#3A1620"), (1, "#160A0E")),
        stroke="#120608", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E0C8C0", strokeWidth=3, opacity=26)
d.shape("ellipse", "Firelight", x=220, y=120, width=560, height=470,
        fill=rad((0, "#FFC890", 0.15), (0.6, "#FFC890", 0.05), (1, "#FFC890", 0)), stroke=NONE)
for i, (x, y, w) in enumerate([(208, 215, 6), (782, 245, 7), (168, 615, 6), (830, 590, 7),
                               (428, 102, 6), (648, 108, 7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w, fill="#C89080", opacity=30, stroke=NONE)

HZN = 700
hx = math.sqrt(PR ** 2 - (HZN - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{HZN} L{PCX + hx:.1f},{HZN} A420,420 0 0 1 {PCX - hx:.1f},{HZN} Z", "Floor",
       fill=lin(0, HZN, 0, 880, (0, "#2E1E16", 0.55), (1, "#120806", 0.9)), stroke=NONE)
d.shape("ellipse", "Armoire shadow", x=250, y=FOOT_Y - 40, width=540, height=96,
        fill=rad((0, "#060302", 0.65), (1, "#060302", 0)), stroke=NONE)

# --- the armoire -----------------------------------------------------------------------------------
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

d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840, fill=NONE, stroke="#0C0608", strokeWidth=6)

# --- captions ---------------------------------------------------------------------------------------
d.text("ARMOIRE", "Name", x=500, y=940, size=58, font="Virelai Sans",
       color="#F0E2D4", justify="center")
LINE2, SZ2, TRK = "CHERRY · IRON", 22, 300
r = d.text(LINE2, "Second line", x=500, y=975, size=SZ2, font="Virelai Sans",
           color="#C8A8A0", justify="center")
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

d.finish("armoire-V1R00")
