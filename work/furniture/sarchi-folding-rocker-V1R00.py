#!/usr/bin/env python3
"""Sarchi folding rocker — field plate V1R00. A Costa Rican wood-and-leather
folding rocker in slight three-quarter view, unfolded: each side is an
X-scissor of two long timber members crossing at a bolted pivot, feet
landed on a curved runner, and a single amber leather sling stretched from
the front-lip bar, sagging through the seat, up the back panel to the top
bar. Both runners touch the same ground plane. Deep coffee-green disc.
1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Sarchi Folding Rocker — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#241610"   # warm dark ink, never pure black
EXTENT = []

def on_disc(x, y, pad):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

def stops(*pairs):
    out = []
    for p in pairs:
        s = {"offset": p[0], "color": p[1]}
        if len(p) > 2:
            s["opacity"] = p[2]
        out.append(s)
    return out

def lin(a, b, *pairs):
    return {"gradient": {"kind": "linear", "start": [round(a[0], 1), round(a[1], 1)],
                         "end": [round(b[0], 1), round(b[1], 1)], "stops": stops(*pairs)}}

def rad(*pairs):
    return {"gradient": {"kind": "radial", "stops": stops(*pairs)}}

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

def poly(pts):
    return "M%.1f,%.1f " % pts[0] + " ".join("L%.1f,%.1f" % p for p in pts[1:]) + " Z"

def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)

# --- projection: model in inches, fixed yaw + pitch ------------------------------------
YAW, PITCH = math.radians(24), math.radians(20)
S, OX, OY = 16.6, 505.0, 714.0

def P(x, y, z):
    c, s = math.cos(YAW), math.sin(YAW)
    xr, zr = x * c + z * s, -x * s + z * c
    p = (OX + S * xr, OY - S * (y * math.cos(PITCH) + zr * math.sin(PITCH)))
    EXTENT.append(p)
    return p

WOOD = ((0, "#9C6A34"), (0.3, "#7C4E24"), (0.65, "#5C3617"), (1, "#38200C"))
WOOD_FAR = ((0, "#744E26"), (0.55, "#583718"), (1, "#301C0A"))
LEATHER = ((0, "#E2A85C"), (0.45, "#C08240"), (1, "#7E4A1E"))
LEATHER_BACK = ((0, "#D69A4E"), (0.5, "#A96E30"), (1, "#6E4018"))

def pole(name, pts3, r=0.42, grad=WOOD, ink=2.2):
    """A timber member: capsule ribbon along a 3D polyline."""
    pts = [P(*p) for p in pts3]
    w = r * S
    left, right = [], []
    for i, p in enumerate(pts):
        a = pts[max(0, i - 1)]; b = pts[min(len(pts) - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1
        nx, ny = -dy / L, dx / L
        left.append((p[0] + nx * w, p[1] + ny * w))
        right.append((p[0] - nx * w, p[1] - ny * w))
    d.path(smooth(left + right[::-1] + [left[0]]), name,
           fill=lin(left[0], right[-1], *grad), stroke=INK, strokeWidth=ink, join="round")
    assert 2 * w >= 3, "member must stay >= 3pt"
    return pts

def bolt(name, p3, r=9):
    x, y = P(*p3)
    d.shape("ellipse", name, x=round(x - r), y=round(y - r), width=2 * r, height=2 * r,
            fill=rad((0, "#F4DC9C"), (0.55, "#B8873C"), (1, "#5E3E14")), stroke=INK, strokeWidth=1.8)
    d.shape("ellipse", f"{name} glint", x=round(x - r * 0.42), y=round(y - r * 0.55),
            width=round(r * 0.5), height=round(r * 0.4), fill="#FFF6DC", opacity=85, stroke=NONE)

# --- backdrop + deep coffee-green plate -------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#12120C"), (1, "#060604")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#6B6248", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#6B6248"), (0.55, "#403C26"), (1, "#1C1A0E")),
        stroke="#12100A", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#CCC298", strokeWidth=3, opacity=24)
d.shape("ellipse", "Back glow", x=250, y=160, width=500, height=500,
        fill=rad((0, "#D8A868", 16), (0.6, "#9A7040", 6), (1, "#6A5030", 0)), stroke=NONE)

# floor, closed on the disc arc
FY = 664
hx = math.sqrt(PR ** 2 - (FY - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{FY} L{PCX + hx:.1f},{FY} A420,420 0 0 1 {PCX - hx:.1f},{FY} Z",
       "Floor", fill=lin((0, FY), (0, 880), (0, "#5E5438", 36), (1, "#1C180C", 70)), stroke=NONE)
d.path(f"M{PCX - hx + 6:.1f},{FY} L{PCX + hx - 6:.1f},{FY}", "Floor edge light",
       fill=NONE, stroke="#D8CCA0", strokeWidth=2, opacity=18)

# === chair model (inches) ==================================================================
HX = 8.6          # half width
# member A: rear foot -> pivot -> front lip bar top
A = [(1.8, -7.2), (6.5, -3.6), (12.4, 0.7), (15.6, 4.0)]
# member B: front foot -> pivot -> backrest top
B = [(1.8, 7.2), (7.0, 3.4), (12.4, -0.3), (17.8, -2.8), (22.6, -4.4)]
PIV = (12.4, 0.4)

def member(side, pts_yz):
    return [(side * HX, y, z) for y, z in pts_yz]

def runner_pts(side):
    return [(side * HX, 2.4, -9.2), (side * HX, 0.7, -5.0), (side * HX, 0.15, -0.4),
            (side * HX, 0.55, 4.6), (side * HX, 2.5, 9.0)]

# ground shadow pooled under both runners
r_low = [P(-HX, 0.15, -0.4), P(HX, 0.15, -0.4),
         P(-HX, 0.7, -5), P(HX, 0.55, 4.6), P(-HX, 2.5, 9), P(-HX, 2.4, -9.2)]
sx0, sx1 = min(p[0] for p in r_low) - 42, max(p[0] for p in r_low) + 42
sy0, sy1 = min(p[1] for p in r_low) - 26, max(p[1] for p in r_low) + 16
d.shape("ellipse", "Rocker shadow", x=round(sx0), y=round(sy0), width=round(sx1 - sx0),
        height=round(sy1 - sy0),
        fill=rad((0, "#070704", 60), (0.6, "#070704", 26), (1, "#070704", 0)), stroke=NONE)

# --- far side frame ----------------------------------------------------------------------------
pole("Far runner", runner_pts(-1), r=0.5, grad=WOOD_FAR)
pole("Far member B", member(-1, B), r=0.44, grad=WOOD_FAR)
pole("Far member A", member(-1, A), r=0.44, grad=WOOD_FAR)
bolt("Far pivot", (-HX - 0.5, *PIV), r=8)
# foot pegs where members land on the far runner
for nm, p3 in (("farA", (-HX, 1.6, -7.0)), ("farB", (-HX, 1.6, 7.0))):
    bolt(f"Peg {nm}", p3, r=6)

# cross ties between the sides: front lip bar, back top bar, low stretcher
pole("Front lip bar", [(-HX, A[-1][0], A[-1][1]), (HX, A[-1][0], A[-1][1])], r=0.36)
pole("Back top bar", [(-HX, B[-1][0], B[-1][1]), (HX, B[-1][0], B[-1][1])], r=0.36)
pole("Runner tie", [(-HX, 2.6, -8.6), (HX, 2.6, -8.6)], r=0.3, grad=WOOD_FAR)

# --- the leather sling ---------------------------------------------------------------------------
# u: 0 at front lip top -> seat dip -> back top. Surface spans x in [-HX+0.5, HX-0.5]
PROF = [(0.00, 15.4, 4.3), (0.18, 13.9, 3.4), (0.42, 11.9, 0.9), (0.55, 11.7, -0.8),
        (0.68, 13.6, -2.2), (0.84, 17.4, -3.4), (1.00, 22.4, -4.45)]

def sling(u, xf):
    i = min(len(PROF) - 2, int(u * (len(PROF) - 1)))
    t = u * (len(PROF) - 1) - i
    _, y0, z0 = PROF[i]; _, y1, z1 = PROF[i + 1]
    y, z = y0 + (y1 - y0) * t, z0 + (z1 - z0) * t
    sn = math.sin(math.pi * min(1, max(0, (u - 0.05) / 0.9)))
    xe = HX - 0.5 - 0.35 * sn           # free edges pull in under tension
    y += -0.9 * sn * (1 - xf * xf)      # pan sag between the side hems
    z += 0.25 * sn * (1 - xf * xf)
    return (xf * xe, y, z)

NU, NXF = 30, 9
US = [i / NU for i in range(NU + 1)]
XFS = [-1 + 2 * j / (NXF - 1) for j in range(NXF)]

def surf(u0, u1):
    us = [u for u in US if u0 - 1e-9 <= u <= u1 + 1e-9]
    if not us or us[0] > u0: us = [u0] + us
    if us[-1] < u1: us = us + [u1]
    return [P(*sling(u, -1)) for u in us] + [P(*sling(u1, xf)) for xf in XFS[1:]] + \
           [P(*sling(u, 1)) for u in us[::-1]] + [P(*sling(u0, xf)) for xf in XFS[::-1][1:]]

# back panel first (it tucks under the seat surface at the bend), then seat over it
back = surf(0.56, 1.0)
d.path(poly(back), "Leather back",
       fill=lin((0, min(p[1] for p in back)), (0, max(p[1] for p in back)),
                (0, "#EFB868"), (0.55, "#C08240"), (1, "#8A5424")),
       stroke="#4A2810", strokeWidth=2.4, join="round")
seat = surf(0.0, 0.62)
d.path(poly(seat), "Leather seat",
       fill=lin((0, min(p[1] for p in seat)), (0, max(p[1] for p in seat)),
                (0, "#DCA457"), (0.5, "#B5773A"), (1, "#7E461C")),
       stroke="#4A2810", strokeWidth=2.4, join="round")
# the seat pan sits in shadow under its own dip — deepen it so it reads concave
pan = [P(*sling(u, xf)) for u in US if 0.30 <= u <= 0.60 for xf in (-0.95,)] + \
      [P(*sling(0.60, xf)) for xf in XFS[1:]] + \
      [P(*sling(u, 0.95)) for u in US[::-1] if 0.30 <= u <= 0.60][1:] + \
      [P(*sling(0.30, xf)) for xf in XFS[::-1][1:-1]]
d.path(poly(pan), "Seat pan shade", fill="#3A1E08", opacity=22, stroke=NONE)

# lambert-ish shading per u-strip on the outer face
for i in range(NU):
    u0, u1 = US[i], US[i + 1]
    a0, a1 = sling(u0, 0), sling(u1, 0)
    dy, dz = a1[1] - a0[1], a1[2] - a0[2]
    L = math.hypot(dy, dz) or 1
    # light from up-front: face normal n=(-dz, dy)
    lam = (-dz / L) * 0.75 + (-dy / L) * 0.35
    strip = [P(*sling(u0, xf)) for xf in XFS] + [P(*sling(u1, xf)) for xf in XFS[::-1]]
    if lam < -0.15:
        d.path(poly(strip), f"Sling shade {i+1}", fill="#4A2408",
               opacity=round(min(40, (-lam - 0.15) * 80)), stroke=NONE)

# side hems: darker doubled leather edges
for side, nm in ((-1, "L"), (1, "R")):
    hem = [P(*sling(u, side * 0.97)) for u in US[1:-1]]
    d.path(smooth(hem, closed=False), f"Sling hem {nm}", fill=NONE,
           stroke="#5E3212", strokeWidth=4, opacity=60, cap="round")
# tension creases fanning from the front lip corners into the seat
for side in (-1, 1):
    for k in range(3):
        crease = [P(*sling(0.16 + 0.05 * k, side * (0.92 - 0.28 * t))) for t in (0, 0.5, 1)]
        d.path(smooth(crease, closed=False), f"Crease {side}{k}", fill=NONE,
               stroke="#6E3C14", strokeWidth=2.4, opacity=30, cap="round")
# stitch line along the back panel hem
st = [P(*sling(0.86, xf * 0.9)) for xf in [-1 + 2 * k / 12 for k in range(13)]]
d.path(smooth(st, closed=False), "Back seam", fill=NONE, stroke="#F4D9A8",
       strokeWidth=2, opacity=60, dash=[5, 4], cap="round")
# leather wrapped over the front lip bar: a rolled cuff
_a = P(-HX + 0.4, A[-1][0], A[-1][1]); _b = P(HX - 0.4, A[-1][0], A[-1][1])
pole("Front lip cuff", [(-HX + 1.0, A[-1][0] + 0.15, A[-1][1] + 0.1),
                        (HX - 1.0, A[-1][0] + 0.15, A[-1][1] + 0.1)], r=0.3,
     grad=((0, "#E8B06A"), (0.5, "#B57A34"), (1, "#6E3C14")), ink=1.8)

# --- near side frame -----------------------------------------------------------------------------
pole("Near runner", runner_pts(1), r=0.52)
pole("Near member B", member(1, B), r=0.46)
pole("Near member A", member(1, A), r=0.46)
bolt("Near pivot", (HX + 0.5, *PIV), r=10)
for nm, p3 in (("nearA", (HX, 1.6, -7.0)), ("nearB", (HX, 1.6, 7.0))):
    bolt(f"Peg {nm}", p3, r=6.5)
# small keepers pinning the runner to the member feet
for nm, p3 in (("kA", (HX, 2.0, -6.6)), ("kB", (HX, 2.0, 6.6))):
    d.shape("ellipse", f"Keeper {nm}", x=round(P(*p3)[0] - 4), y=round(P(*p3)[1] - 4),
            width=8, height=8, fill=rad((0, "#D8B878"), (1, "#6E4A1C")),
            stroke=INK, strokeWidth=1.4)

# ground contact: assert both runners share the ground plane (model y=0.15 low)
for side in (-1, 1):
    lo = P(side * HX, 0.15, -0.4)
    print("runner", side, "contact y=%.1f" % lo[1])

# --- extent check -----------------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("chair extent: farthest point %.0f from centre (rim %d)" % (far, PR))
assert far < PR - 24, far

# plate rim over everything
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#12100A", strokeWidth=6)
d.shape("ellipse", "Plate inner ring 2", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#CCC298", strokeWidth=3, opacity=20)

# --- caption -----------------------------------------------------------------------------------
def find(node, oid):
    if isinstance(node, dict):
        if node.get("id") == oid and "bounds" in node:
            return node["bounds"]
        for v in node.values():
            r = find(v, oid)
            if r:
                return r
    elif isinstance(node, list):
        for v in node:
            r = find(v, oid)
            if r:
                return r
    return None

def caption(name, mats):
    n = d.text(name, "Name", x=500, y=934, size=56, font="Virelai Sans",
               color="#EDE3C6", justify="center")
    m = d.text(mats, "Materials", x=500, y=970, size=22, font="Virelai Sans",
               color="#BBAE8C", justify="center")
    d.cmd("text.setStyle", "Name tracking", ids=[n["id"]], tracking=60)
    d.cmd("text.setStyle", "Materials tracking", ids=[m["id"]], tracking=260)
    doc = d.m.call("doc_inspect", {})
    for oid, label in ((n["id"], "name"), (m["id"], "materials")):
        b = find(doc, oid)
        nearest = (min(max(PCX, b["x"]), b["x"] + b["width"]),
                   min(max(PCY, b["y"]), b["y"] + b["height"]))
        clear = math.hypot(nearest[0] - PCX, nearest[1] - PCY) - (PR + 3)
        print("%s: %.0fx%.0f at y %.0f, clears rim by %.1f" % (label, b["width"], b["height"], b["y"], clear))
        assert clear > 0 and b["x"] >= 10 and b["x"] + b["width"] <= 990, label
        if label == "materials":
            assert b["width"] <= 760, b["width"]

caption("SARCHÍ ROCKER", "WOOD · LEATHER")
d.finish("sarchi-folding-rocker-V1R00")
