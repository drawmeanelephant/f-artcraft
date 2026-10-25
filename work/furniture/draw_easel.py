#!/usr/bin/env python3
"""Easel — field plate V1R00. A beech A-frame studio easel: two front legs
splaying from the brass apex hinge, a third leg kicking back, the ledge
tray across them at mid-height, a sliding clamp above, and a primed canvas
leaning on the tray with a blocked-in oval sketch in charcoal. A low
stretcher ties the legs; paint dabs spot the floor. Seen from front-right,
slightly above. Beech plate, north-light studio mood. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Easel — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#241606"


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


# --- projection: x right, y up, z toward the viewer; front-right, above ---
TH = math.radians(32)
CT, ST = math.cos(TH), math.sin(TH)
K, VC = 0.42, 0.95


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


def member(label, a, b, w0, w1, stops, ink=1.8, axis="z"):
    """A straight tapered member a->b in 3D, widened across `axis`."""
    ax, ay, az = a
    bx, by, bz = b
    n = 14
    pts = []
    for i in range(n + 1):
        t = i / n
        x, y, z = ax + (bx - ax) * t, ay + (by - ay) * t, az + (bz - az) * t
        w = w0 + (w1 - w0) * t
        if axis == "z":
            quad = [(x, y, z - w), (x, y, z + w)]
        else:
            quad = [(x - w, y, z), (x + w, y, z)]
        pts.append(quad)
    outline = [p[0] for p in pts] + [p[1] for p in reversed(pts)]
    g = (a, b, stops)
    OPS.append(("poly", label, [proj(*p) for p in outline], None, INK, ink, None,
                (proj(*g[0]), proj(*g[1]), g[2])))


# --- beech + canvas palette ----------------------------------------------------------------------------------
BEECH    = [(0, "#DCB478"), (0.5, "#B08A50"), (1, "#7A5628")]
BEECH_DK = [(0, "#8A6234"), (0.5, "#68441F"), (1, "#402610")]
BEECH_HI = "#F0D8A8"
CANVAS   = [(0, "#EFE8D4"), (0.55, "#DDD2B8"), (1, "#B8AC90")]
BRASS    = "#D9A84E"

W, D = 250, 205          # easel spread (x), feet depth (z)
APEX = (W / 2, 468, 78)  # hinge point
YLEDGE = 200

# --- rear leg first (darkest, behind everything) -------------------------------------------------------------
member("Rear leg", (W / 2 + 6, 458, 72), (W / 2 + 26, 0, -8), 8, 13, BEECH_DK, ink=1.5)

# --- low stretcher between the front legs ----------------------------------------------------------------------
member("Stretcher", (34, 74, 190), (W - 34, 74, 190), 9, 9, BEECH_DK, ink=1.6, axis="z")

# --- front legs: apex hinge down to splayed feet ---------------------------------------------------------------
member("Leg L", (W / 2 - 12, APEX[1], APEX[2]), (8, 2, D), 9, 13, BEECH)
member("Leg R", (W / 2 + 12, APEX[1], APEX[2]), (W - 8, 2, D), 9, 13, BEECH)
# edge lights on the outside of each leg
line("Leg L light", [(W / 2 - 15, APEX[1] - 8, APEX[2] + 2), (5, 10, D - 4)],
     BEECH_HI, 2.6, 62)
line("Leg R light", [(W / 2 + 15, APEX[1] - 8, APEX[2] + 2), (W - 5, 10, D - 4)],
     BEECH_HI, 2.6, 50)

# --- apex: mast stub rising past the hinge ---------------------------------------------------------------------
OPS.append(("poly", "Mast stub face",
            [proj(W / 2 - 7, APEX[1] + 24, APEX[2] - 2), proj(W / 2 + 7, APEX[1] + 24, APEX[2] - 2),
             proj(W / 2 + 9, APEX[1] - 4, APEX[2]), proj(W / 2 - 9, APEX[1] - 4, APEX[2])],
            None, INK, 1.8, None,
            (proj(W / 2, APEX[1] + 24, APEX[2]), proj(W / 2, APEX[1] - 4, APEX[2]), BEECH)))

# --- the canvas: a primed panel leaning on the ledge ----------------------------------------------------------
# canvas plane: bottom edge rests on the tray lip, top leans back
CX0, CX1 = 56, 196
CY0, CY1 = 208, 392
CZ_B, CZ_T = 226, 104    # foot forward on the tray, top back against the mast
poly("Canvas face", [(CX0, CY0, CZ_B), (CX1, CY0, CZ_B), (CX1, CY1, CZ_T),
                     (CX0, CY1, CZ_T)],
     sw=2.2, g=((CX0, CY1, CZ_T), (CX1, CY0, CZ_B), CANVAS))
poly("Canvas right edge", [(CX1, CY0, CZ_B), (CX1 + 7, CY0, CZ_B - 4),
                           (CX1 + 7, CY1, CZ_T - 4), (CX1, CY1, CZ_T)],
     sw=1.5, g=((CX1, CY1, CZ_T), (CX1 + 7, CY0, CZ_B), [(0, "#C8BCA0"), (1, "#8A8068")]))
poly("Canvas top edge", [(CX0, CY1, CZ_T), (CX1, CY1, CZ_T),
                         (CX1 + 7, CY1 + 4, CZ_T - 6), (CX0 + 7, CY1 + 4, CZ_T - 6)],
     sw=1.5, g=((CX0, CY1 + 4, CZ_T), (CX1, CY1 + 4, CZ_T), [(0, "#F6EFDC"), (1, "#C8BCA0")]))
# blocked-in sketch: charcoal oval + centre lines, faint on the gesso
SK = "#5A5248"


def sketch(label, pts3, sw=2.0, op=40):
    line(label, pts3, SK, sw, op)


# oval head blocked in the upper half of the canvas
ovcx, ovcy, orx, ory = (CX0 + CX1) / 2, 318, 34, 44
ovpts = [(ovcx + orx * math.cos(2 * math.pi * k / 16),
          ovcy + ory * math.sin(2 * math.pi * k / 16)) for k in range(17)]


def on_canvas(x, y):
    """A point on the leaning canvas plane: z varies with height."""
    t = (y - CY0) / (CY1 - CY0)
    return (x, y, CZ_B + (CZ_T - CZ_B) * t)


sketch("Sketch oval", [on_canvas(p[0], p[1]) for p in ovpts], 2.2, 42)
sketch("Sketch brow", [on_canvas(ovcx - 34, ovcy - 10), on_canvas(ovcx, ovcy - 18),
                       on_canvas(ovcx + 34, ovcy - 10)], 1.8, 36)
sketch("Sketch neck", [on_canvas(ovcx - 16, ovcy + 44), on_canvas(ovcx - 14, ovcy + 62),
                       on_canvas(ovcx + 16, ovcy + 62), on_canvas(ovcx + 14, ovcy + 44)],
       1.8, 36)
sketch("Sketch shoulder", [on_canvas(ovcx - 58, CY0 + 22), on_canvas(ovcx - 34, ovcy + 58),
                           on_canvas(ovcx + 34, ovcy + 58), on_canvas(ovcx + 56, CY0 + 22)],
       1.8, 32)

# --- ledge tray across the front legs (covers canvas foot) ---------------------------------------------------
poly("Ledge front", front(28, W - 28, YLEDGE - 8, YLEDGE + 16, 232), sw=2.2,
     g=((28, YLEDGE + 16, 232), (W - 28, YLEDGE - 8, 232), BEECH))
poly("Ledge top", top(28, W - 28, 208, 232, YLEDGE + 16), sw=1.8,
     g=((28, YLEDGE + 16, 208), (W - 28, YLEDGE + 16, 232),
        [(0, "#E8C88E"), (1, "#9A7040")]))
poly("Ledge lip", front(30, W - 30, YLEDGE + 16, YLEDGE + 26, 228), sw=1.8,
     g=((30, YLEDGE + 26, 228), (W - 30, YLEDGE + 16, 228),
        [(0, "#C89A5C"), (1, "#7A5628")]))

# --- top clamp sliding on the mast over the canvas top ---------------------------------------------------------
poly("Clamp face", front(W / 2 - 26, W / 2 + 26, 398, 424, 112), sw=2.0,
     g=((W / 2 - 26, 424, 112), (W / 2 + 26, 398, 112), BEECH))
poly("Clamp top", top(W / 2 - 26, W / 2 + 26, 100, 112, 424), sw=1.6,
     g=((W / 2 - 26, 424, 100), (W / 2 + 26, 424, 112), [(0, "#E8C88E"), (1, "#9A7040")]))

# --- fit to the disc -------------------------------------------------------------------------------------------
xs = [p[0] for op in OPS for p in op[2]]
ys = [p[1] for op in OPS for p in op[2]]
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

# --- backdrop + plate -------------------------------------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin(0, 0, 0, 1000, (0, "#1A1814"), (1, "#080604")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#9A8462", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#6E5B40"), (0.6, "#43351F"), (1, "#170F07")),
        stroke="#0E0804", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F0E2C2", strokeWidth=3, opacity=24)
# north-light window: tall cool patch on the upper left of the studio wall
d.shape("ellipse", "North light", x=150, y=90, width=520, height=520,
        fill=rad((0, "#DDE8EA", 0.14), (0.6, "#C4D4D6", 0.05), (1, "#C4D4D6", 0)),
        stroke=NONE)
for i, (x, y, w) in enumerate([(205, 220, 6), (780, 240, 7), (170, 610, 6), (828, 588, 7),
                               (425, 105, 6), (645, 108, 7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#D0B888", opacity=30, stroke=NONE)

HZN = 704
hx = math.sqrt(PR ** 2 - (HZN - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{HZN} L{PCX + hx:.1f},{HZN} A420,420 0 0 1 {PCX - hx:.1f},{HZN} Z", "Floor",
       fill=lin(0, HZN, 0, 880, (0, "#3E3220", 0.55), (1, "#150E06", 0.9)), stroke=NONE)
for i, yy in enumerate([750, 796, 838]):
    xx = math.sqrt(PR ** 2 - (yy - PCY) ** 2) - 6
    d.path(f"M{PCX - xx:.1f},{yy} L{PCX + xx:.1f},{yy}", f"Floor seam {i+1}",
           fill=NONE, stroke="#100A04", strokeWidth=3, opacity=30)
d.shape("ellipse", "Easel shadow", x=300, y=FOOT_Y - 32, width=440, height=84,
        fill=rad((0, "#080503", 0.65), (1, "#080503", 0)), stroke=NONE)
# paint dabs on the studio floor
for i, (x, y, w, c) in enumerate([(392, FOOT_Y + 16, 14, "#B84A30"),
                                  (596, FOOT_Y + 24, 11, "#28487A"),
                                  (528, FOOT_Y + 34, 12, "#E8E2D0")]):
    d.shape("ellipse", f"Paint dab {i+1}", x=x, y=y, width=w, height=round(w * 0.5),
            fill=rad((0, mix(c, "#FFFFFF", 0.25)), (1, c)), stroke=NONE, opacity=85)

# --- the easel ---------------------------------------------------------------------------------------------------
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
        d.path(path_of(pts, False), label, fill=NONE, stroke=stroke,
               strokeWidth=sw, cap="round", join="round", **kw)

# brass hinge at the apex
hxp, hyp = S(proj(W / 2, APEX[1] - 4, APEX[2] + 10))
d.shape("ellipse", "Apex hinge", x=round(hxp - 9), y=round(hyp - 9), width=18, height=18,
        fill=rad((0, "#F2D98A"), (0.6, BRASS), (1, "#7A5A1E")), stroke=INK, strokeWidth=1.4)
d.shape("ellipse", "Hinge pin", x=round(hxp - 3), y=round(hyp - 3), width=6, height=6,
        fill="#3A2A12", stroke=NONE)

d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840, fill=NONE,
        stroke="#0C0603", strokeWidth=6)

# --- captions -----------------------------------------------------------------------------------------------------
d.text("EASEL", "Name", x=500, y=940, size=54, font="Virelai Sans",
       color="#F4EAD2", justify="center")
LINE2, SZ2, TRK = "BEECH · LINEN · BRASS", 22, 300
r = d.text(LINE2, "Second line", x=500, y=975, size=SZ2, font="Virelai Sans",
           color="#D0BC94", justify="center")
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

d.finish("easel-V1R00")
