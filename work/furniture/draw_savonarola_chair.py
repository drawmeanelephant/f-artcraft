#!/usr/bin/env python3
"""Savonarola chair — field plate V1R00. The Renaissance folding chair:
each side is a scissor lattice — pairs of long S-slats crossing in X cells
between a floor pivot row and the seat-rail pivot row. Rear stiles rake
back to a wide carved crest board; a sagging leather strap seat spans the
rails; brass pins mark the scissor crossings. Seen from front-right, above.
Walnut plate, palazzo mood. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Savonarola Chair — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#241206"


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


# --- projection: x right, y up, z toward the viewer; mostly side-on so the
# scissor lattice reads, enough three-quarter to keep the seat and crest ---
TH = math.radians(70)
CT, ST = math.cos(TH), math.sin(TH)
K, VC = 0.40, 0.95


def proj(x, y, z):
    return (x * CT - z * ST, (x * ST + z * CT) * K - y * VC)


OPS = []
PINS = []           # brass pivot pins, drawn after the lattice (screen space, pre-scale)


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


def ribbon(label, spine3, w0, w1, stops, ink=1.6, opacity=None):
    """Tapered filled ribbon along a 3D spine; outline stored for fit+draw."""
    pts = [proj(*p) for p in spine3]
    n = len(pts)
    left, right = [], []
    for i, p in enumerate(pts):
        q0 = pts[max(0, i - 1)]
        q1 = pts[min(n - 1, i + 1)]
        tx, ty = q1[0] - q0[0], q1[1] - q0[1]
        L = math.hypot(tx, ty) or 1
        nx, ny = -ty / L, tx / L
        w = w0 + (w1 - w0) * i / (n - 1)
        left.append((p[0] + nx * w, p[1] + ny * w))
        right.append((p[0] - nx * w, p[1] - ny * w))
    outline = left + right[::-1]
    g = (pts[0], pts[-1], stops)
    OPS.append(("path", label, outline, None, INK, ink, opacity, g))


def catmull(pts, closed=True):
    n = len(pts)

    def g(i):
        return pts[i % n] if closed else pts[max(0, min(n - 1, i))]
    s = "M%.1f,%.1f" % pts[0]
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        p0, p1, p2, p3 = g(i - 1), g(i), g(i + 1), g(i + 2)
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        s += " C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (c1 + c2 + p2)
    return s + (" Z" if closed else "")


# --- palette: walnut + leather + brass --------------------------------------------------------------
SLAT_A = [(0, "#9A6434"), (0.5, "#74461F"), (1, "#4A2812")]      # outer slats
SLAT_B = [(0, "#7A4A26"), (0.5, "#573318"), (1, "#33200E")]      # inner slats
SLAT_FAR = [(0, "#38200E"), (0.5, "#281408"), (1, "#160A04")]
RAIL_ST = [(0, "#7A4E28"), (1, "#462812")]
RAIL_FAR = [(0, "#3C2410"), (1, "#201006")]
CREST_ST = [(0, "#96622F"), (0.5, "#6E421E"), (1, "#3C2010")]

W, D = 250, 230          # chair width (x), depth (z)
YBOT, YSEAT = 6, 214     # floor, seat-rail height
YTOP = YSEAT + 12
BAYS = [16 + p * 42 for p in range(6)]     # pivot bays in z: 16..226
BOW = 7.0                # gentle ogee of each slat


def slat3(cx, z_bot, z_top, bow, n=26):
    """One S-slat: dominant diagonal, shallow ogee ripple on top."""
    return [(cx, YBOT + (YTOP - YBOT) * (k / n),
             z_bot + (z_top - z_bot) * (k / n) + bow * math.sin(2 * math.pi * k / n))
            for k in range(n + 1)]


def lattice(cx, near, tag):
    """Folding-gate trellis: every slat spans two bays; each slat crosses its
    opposite-leaning neighbours at the quarter points — a chain of X cells."""
    stA = SLAT_A if near else SLAT_FAR
    stB = [(s[0], mix(s[1], "#140A04", 0.0 if near else 0.25)) for s in SLAT_B]
    xo = 0 if near else -4
    # inner family first so outer slats read over them at crossings
    for i in range(len(BAYS) - 2):
        ribbon(f"{tag} B slat {i+1}", slat3(cx - 9 + xo, BAYS[i + 2], BAYS[i], -BOW),
               11, 8.5, stB, ink=1.5 if near else 1.3)
    for i in range(len(BAYS) - 2):
        sp = slat3(cx + xo, BAYS[i], BAYS[i + 2], BOW)
        ribbon(f"{tag} A slat {i+1}", sp, 11, 8.5, stA, ink=1.7 if near else 1.4)
        if near:
            # warm edge-light down the spine so each slat stays separate
            line(f"Near A edge {i+1}", [(p[0] + 3, p[1], p[2]) for p in sp[3:-3]],
                 "#D8A05C", 2.6, 45)
    if near:
        for i in range(len(BAYS) - 2):
            for j in range(len(BAYS) - 2):
                t = (j + 2 - i) / 4
                if 0 < t < 1:                              # A_i x B_j crossing
                    zc = BAYS[i] + (BAYS[i + 2] - BAYS[i]) * t
                    PINS.append(proj(cx + 7, YBOT + t * (YTOP - YBOT), zc))
    # floor runner: the slat feet die into a clean ground rail
    rail = RAIL_ST if near else RAIL_FAR
    face_x = cx + 12 if near else cx - 12
    poly(f"{tag} runner face", side(face_x, 4, 232, -2, 18), sw=2.0,
         g=((face_x, 18, 4), (face_x, -2, 232), rail))
    poly(f"{tag} runner top", top(cx - 10, cx + 10, 4, 232, 18), sw=1.5,
         g=((cx - 10, 18, 4), (cx + 10, 18, 232),
            [(0, mix(rail[0][1], "#C89058", 0.25)), (1, rail[0][1])]))
    # seat rail: the slat tops die into it
    poly(f"{tag} seat rail face", side(face_x, 6, 230, YSEAT - 14, YTOP + 8),
         sw=2.0, g=((face_x, YTOP + 8, 6), (face_x, YSEAT - 14, 230), rail))
    poly(f"{tag} seat rail top", top(cx - 11, cx + 11, 6, 230, YTOP + 8), sw=1.6,
         g=((cx - 11, YTOP + 8, 6), (cx + 11, YTOP + 8, 230),
            [(0, mix(rail[0][1], "#C89058", 0.3)), (1, rail[0][1])]))
    # rear stile: rakes gently back from the rail up to the crest
    poly(f"{tag} stile", [(face_x, YTOP, 24), (face_x, YTOP, 2),
                          (face_x, 428, -4), (face_x, 428, 14)],
         sw=2.0, g=((face_x, 428, 6), (face_x, YTOP, 12), rail))


# --- far side lattice (x=0), dim ----------------------------------------------------------------------
lattice(0, False, "Far")

# --- back stretcher tying the stiles, then the wide carved crest board ------
poly("Back stretcher", front(6, W - 6, 318, 338, 10), sw=2.0,
     g=((6, 338, 10), (W - 6, 318, 10), RAIL_ST))
CZ0, CZ1, CY0, CY1 = -4, 12, 424, 468
poly("Crest front", front(-12, W + 12, CY0, CY1, CZ1), sw=2.4,
     g=((-12, CY1, CZ1), (W + 12, CY0, CZ1), CREST_ST))
poly("Crest top edge", top(-12, W + 12, CZ0, CZ1, CY1), sw=1.8,
     g=((-12, CY1, CZ0), (W + 12, CY1, CZ1), [(0, "#B88048"), (1, "#6E421E")]))
poly("Crest right edge", side(W + 12, CZ0, CZ1, CY0, CY1), sw=1.8,
     g=((W + 12, CY1, CZ1), (W + 12, CY0, CZ0), [(0, "#5C3418"), (1, "#2A1608")]))
line("Crest ogee", [(8, CY1 - 8, CZ1 + 1), (W * 0.3, CY1 - 14, CZ1 + 1),
                    (W * 0.5, CY1 - 8, CZ1 + 1), (W * 0.7, CY1 - 14, CZ1 + 1),
                    (W - 8, CY1 - 8, CZ1 + 1)], "#2A1608", 2.4, 70)
mx, my = W / 2, (CY0 + CY1) / 2 + 2
poly("Crest medallion", [(mx, my + 13, CZ1 + 0.6), (mx + 11, my, CZ1 + 0.6),
                         (mx, my - 13, CZ1 + 0.6), (mx - 11, my, CZ1 + 0.6)],
     sw=1.6, stroke="#2A1608",
     g=((mx, my + 13, CZ1), (mx, my - 13, CZ1), [(0, "#C89058"), (1, "#5C3418")]))
line("Medallion ring", [(mx, my + 6, CZ1 + 1), (mx + 6, my, CZ1 + 1),
                        (mx, my - 6, CZ1 + 1), (mx - 6, my, CZ1 + 1),
                        (mx, my + 6, CZ1 + 1)], "#3A2210", 1.6, 75)

# --- seat: dark well under sagging leather straps (straps run front-to-back) ----
poly("Seat well", top(8, W - 8, 12, 224, YSEAT - 12), stroke=NONE, fill="#160B04")
# front apron rail across the seat's front edge
poly("Front apron", front(6, W - 6, YSEAT - 16, YTOP + 4, 230), sw=2.0,
     g=((6, YTOP + 4, 230), (W - 6, YSEAT - 16, 230), RAIL_ST))
poly("Front apron edge", top(6, W - 6, 224, 230, YTOP + 4), sw=1.5,
     g=((6, YTOP + 4, 224), (W - 6, YTOP + 4, 230), [(0, "#9A6834"), (1, "#5C3418")]))
STRAPS = 6
for k in range(STRAPS):
    xk = 26 + k * (198 / (STRAPS - 1))
    seg = []
    for t in [i / 24 for i in range(25)]:
        z = 14 + 212 * t
        y = YSEAT + 8 - 11 * math.sin(math.pi * t)
        seg.append((xk - 12, y, z))
    poly(f"Strap {k+1}", seg + [(x + 24, y, z) for x, y, z in reversed(seg)],
         sw=1.2, stroke="#1E0E04",
         g=((xk - 12, YSEAT + 8, 14), (xk + 12, YSEAT - 2, 226),
            [(0, "#7A4E28"), (0.55, "#5A3418"), (1, "#33200E")]))

# --- near side lattice (x=W) ----------------------------------------------------------------------------
lattice(W, True, "Near")

# --- fit to the disc -------------------------------------------------------------------------------------
xs = [p[0] for op in OPS for p in op[2]] + [p[0] for p in PINS]
ys = [p[1] for op in OPS for p in op[2]] + [p[1] for p in PINS]
bw, bh = max(xs) - min(xs), max(ys) - min(ys)
SC = min(600 / bw, 600 / bh)
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

# --- backdrop + plate -------------------------------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin(0, 0, 0, 1000, (0, "#181009"), (1, "#070403")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#8A6A44", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#5C4630"), (0.6, "#38250F"), (1, "#150C05")),
        stroke="#0E0804", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8D0A8", strokeWidth=3, opacity=24)
d.shape("ellipse", "Palazzo glow", x=210, y=100, width=560, height=480,
        fill=rad((0, "#FFD9A0", 0.13), (0.6, "#FFD9A0", 0.04), (1, "#FFD9A0", 0)),
        stroke=NONE)
for i, (x, y, w) in enumerate([(205, 220, 6), (780, 240, 7), (170, 610, 6), (828, 588, 7),
                               (425, 105, 6), (645, 108, 7), (150, 420, 6), (852, 415, 6)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#C8A878", opacity=30, stroke=NONE)

HZN = 702
hx = math.sqrt(PR ** 2 - (HZN - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{HZN} L{PCX + hx:.1f},{HZN} A420,420 0 0 1 {PCX - hx:.1f},{HZN} Z", "Floor",
       fill=lin(0, HZN, 0, 880, (0, "#3A2818", 0.55), (1, "#140C05", 0.9)), stroke=NONE)
for i, yy in enumerate([748, 794, 836]):
    xx = math.sqrt(PR ** 2 - (yy - PCY) ** 2) - 6
    d.path(f"M{PCX - xx:.1f},{yy} L{PCX + xx:.1f},{yy}", f"Floor seam {i+1}",
           fill=NONE, stroke="#0E0804", strokeWidth=3, opacity=30)
d.shape("ellipse", "Chair shadow", x=290, y=FOOT_Y - 30, width=430, height=80,
        fill=rad((0, "#060302", 0.65), (1, "#060302", 0)), stroke=NONE)

# --- the chair ---------------------------------------------------------------------------------------------
for kind, label, pts, fill, stroke, sw, op, g in OPS:
    kw = {}
    if g is not None and kind in ("poly", "path"):
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
    elif kind == "path":
        d.path(catmull([S(p) for p in pts]), label, fill=fill, stroke=stroke,
               **({"strokeWidth": sw, "join": "round"} if stroke != NONE else {}), **kw)
    else:
        d.path(path_of(pts, False), label, fill=NONE, stroke=stroke,
               strokeWidth=sw, cap="round", join="round", **kw)

for i, (px, py) in enumerate(PINS):
    cx, cy = S((px, py))
    d.shape("ellipse", f"Pivot pin {i+1}", x=round(cx - 5), y=round(cy - 5),
            width=10, height=10,
            fill=rad((0, "#F2D98A"), (0.6, "#D9A84E"), (1, "#7A5A1E")),
            stroke="#241206", strokeWidth=1.2)

d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840, fill=NONE,
        stroke="#0C0603", strokeWidth=6)

# --- captions ------------------------------------------------------------------------------------------------
d.text("SAVONAROLA CHAIR", "Name", x=500, y=940, size=54, font="Virelai Sans",
       color="#F0E0C4", justify="center")
LINE2, SZ2, TRK = "WALNUT · LEATHER · BRASS", 22, 300
r = d.text(LINE2, "Second line", x=500, y=975, size=SZ2, font="Virelai Sans",
           color="#C4A880", justify="center")
d.cmd("text.setStyle", "Second line tracking", id=r["id"], tracking=TRK)


def find(o, oid):
    if isinstance(o, dict):
        if o.get("id") == oid and "bounds" in o:
            return o
        o = list(o.values())
    if isinstance(o, list):
        for v in o:
            hit = find(v, oid)
            if hit:
                return hit


b2 = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("second line bounds", {k: round(v) for k, v in b2.items()})
assert b2["width"] <= 760 and b2["x"] >= 100 and b2["y"] + b2["height"] <= 990, b2

d.finish("savonarola-chair-V1R00")
