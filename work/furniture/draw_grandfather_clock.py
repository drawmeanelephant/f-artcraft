#!/usr/bin/env python3
"""Grandfather clock — field plate V1R00. Three-quarter from the front
right: a mahogany longcase — stepped plinth, trunk with a glazed door,
pendulum caught mid-swing behind the glass, hood with a cream dial and
brass finials on a flat cornice. Hallway mood: deep green-baize plate,
low warm light. 1000x1000.
Modelled in inches (x right, y up, +z back), fixed yaw + pitch projection;
case volumes are 8-corner prisms, the dial and its furniture are drawn in
the hood's front plane.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Grandfather Clock — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#1E120C"   # warm dark, not black
EXTENT = []


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


def poly(pts):
    return "M%.1f,%.1f " % pts[0] + " ".join("L%.1f,%.1f" % p for p in pts[1:]) + " Z"


def smooth(pts, closed=True):
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


# --- projection ------------------------------------------------------------------
YAW, PITCH = math.radians(24), math.radians(11)
S, OX, OY = 7.9, 500.0, 702.0
CY, SY = math.cos(YAW), math.sin(YAW)
CP, SP = math.cos(PITCH), math.sin(PITCH)


def P(x, y, z):
    xr, zr = x * CY + z * SY, -x * SY + z * CY
    p = (OX + S * xr, OY - S * (y * CP + zr * SP))
    EXTENT.append(p)
    return p


def depth(x, y, z):
    """View-space distance; smaller = nearer the viewer (front-right-above)."""
    return -x * SY * CP - y * SP + z * CY * CP


def box(x0, y0, z0, x1, y1, z1):
    """8 corners of an axis-aligned box, near quad (-z) first, CCW from below-left."""
    return [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
            (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]


FACES = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4),
         (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
TO_VIEWER = (SY * CP, SP, -CY * CP)          # normals facing this draw
LIGHT = (-0.45, 0.80, -0.42)
_l = math.sqrt(sum(c * c for c in LIGHT))
LIGHT = tuple(c / _l for c in LIGHT)


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def normal(c, f):
    u = sub(c[f[1]], c[f[0]])
    v = sub(c[f[3]], c[f[0]])
    n = (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2],
         u[0] * v[1] - u[1] * v[0])
    l = math.sqrt(sum(k * k for k in n))
    return tuple(k / l for k in n)


def shade(hex1, hex2, b):
    """Mix two hex colors at brightness b in [0,1]."""
    a = [int(hex1[i:i + 2], 16) for i in (1, 3, 5)]
    c = [int(hex2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02X%02X%02X" % tuple(round(a[i] + (c[i] - a[i]) * b) for i in range(3))


WOOD_D, WOOD_L = "#241009", "#7C4022"      # mahogany ramp
WOOD_HI = "#B06A38"                        # polished sheen


def prism(name, corners, lo=0.06, hi=0.94, ink=1.8, c1=WOOD_D, c2=WOOD_L):
    """Draw the viewer-facing faces of an 8-corner prism, far to near."""
    faces = []
    for f in FACES:
        n = normal(corners, f)
        if n[0] * TO_VIEWER[0] + n[1] * TO_VIEWER[1] + n[2] * TO_VIEWER[2] <= 0.02:
            continue
        lam = max(0.0, sum(n[i] * LIGHT[i] for i in range(3)))
        dep = sum(depth(*corners[i]) for i in f) / len(f)
        pts = [P(*corners[i]) for i in f]
        faces.append((dep, pts, lam))
    for dep, pts, lam in sorted(faces, key=lambda t: -t[0]):
        b = lo + (hi - lo) * lam ** 0.8
        y0, y1 = min(p[1] for p in pts), max(p[1] for p in pts)
        g = lin((0, y0), (0, y1), (0, shade(c1, c2, min(1, b + 0.12))),
                                 (1, shade(c1, c2, b)))
        d.path(poly(pts), name, fill=g, stroke=INK, strokeWidth=ink, join="round")
    return faces


def fquad(x0, y0, x1, y1, z):
    return [P(x0, y0, z), P(x1, y0, z), P(x1, y1, z), P(x0, y1, z)]


def fcircle(cx, cy, z, r, n=30):
    return [P(cx + r * math.cos(2 * math.pi * i / n),
              cy + r * math.sin(2 * math.pi * i / n), z)
            for i in range(n)]


BRASS_STOPS = ((0, "#4A2A0E"), (0.45, "#B8842E"),
               (0.62, "#F2C97E"), (1, "#5A3410"))
WBRASS_STOPS = ((0, "#6A4218"), (0.45, "#C8923A"),
                (0.62, "#F8D48A"), (1, "#7A4A16"))


def brass(pts, stops_=BRASS_STOPS):
    """Vertical brass ramp spanning the projected points' own y-extent."""
    y0 = min(p[1] for p in pts)
    y1 = max(p[1] for p in pts)
    return lin((0, y0), (0, y1), *stops_)


# --- backdrop + plate ---------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#131912"), (1, "#070A07")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#5E7050", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#3A4636"), (0.6, "#283226"), (1, "#111710")),
        stroke="#0A0D08", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#DEE4D0", strokeWidth=3, opacity=22)
d.shape("ellipse", "Hall light", x=250, y=120, width=520, height=520,
        fill=rad((0, "#E0B96A", 16), (0.55, "#8A6A34", 6), (1, "#8A6A34", 0)),
        stroke=NONE)

FY = 706
hx = math.sqrt(PR ** 2 - (FY - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{FY} L{PCX + hx:.1f},{FY} A420,420 0 0 1 {PCX - hx:.1f},{FY} Z",
       "Floor", fill=lin((0, FY), (0, 880), (0, "#46523E", 34), (1, "#0D1109", 72)),
       stroke=NONE)
d.path(f"M{PCX - hx + 6:.1f},{FY} L{PCX + hx - 6:.1f},{FY}", "Floor edge light",
       fill=NONE, stroke="#DCE2CC", strokeWidth=2, opacity=18)

# --- case geometry (inches; x right, y up, +z back) ------------------------------------
# grounding shadow under the plinth
shadow_pts = [P(-11, 0, -5), P(11, 0, -5), P(11, 0, 5), P(-11, 0, 5)]
sx0 = min(p[0] for p in shadow_pts) - 40
sx1 = max(p[0] for p in shadow_pts) + 40
sy0 = min(p[1] for p in shadow_pts) - 12
sy1 = max(p[1] for p in shadow_pts) + 20
d.shape("ellipse", "Clock shadow", x=round(sx0), y=round(sy0),
        width=round(sx1 - sx0), height=round(sy1 - sy0),
        fill=rad((0, "#040604", 72), (0.6, "#040604", 30), (1, "#040604", 0)),
        stroke=NONE)

# --- trunk interior, drawn before the case: back panel, works, pendulum ----------------
d.path(poly(fquad(-7, 19, 7, 57, 3.4)), "Trunk interior",
       fill=lin((0, P(0, 57, 3.4)[1]), (0, P(0, 19, 3.4)[1]),
                (0, "#4E3018"), (1, "#180C06")), stroke=NONE)
# two brass weights flanking the pendulum, hanging at different heights
for i, (wx, wy0, wy1) in enumerate([(-4.6, 30, 46), (4.6, 36, 52)]):
    wpts = fquad(wx - 1.2, wy0, wx + 1.2, wy1, 1.6)
    d.path(poly(wpts), f"Weight {i+1}", fill=brass(wpts, WBRASS_STOPS),
           stroke=INK, strokeWidth=1.6)
    d.path(f"M{P(wx, wy1, 1.6)[0]:.1f},{P(wx, wy1, 1.6)[1]:.1f} "
           f"L{P(wx, 57, 1.6)[0]:.1f},{P(wx, 57, 1.6)[1]:.1f}",
           f"Weight cord {i+1}", fill=NONE, stroke="#0F0A06",
           strokeWidth=1.6, opacity=70)
# pendulum: rod slanting off plumb, bob below — mid-beat, not parked
ROD_TOP, ROD_BOT = (0.0, 53.0), (-2.3, 32.5)
pa, pb = P(*ROD_TOP, 2.2), P(*ROD_BOT, 2.2)
d.path(f"M{pa[0]:.1f},{pa[1]:.1f} L{pb[0]:.1f},{pb[1]:.1f}", "Pendulum rod",
       fill=NONE, stroke="#8A6A34", strokeWidth=3.4, cap="round")
bob = fcircle(-2.3, 29.0, 2.2, 3.5)
d.path(smooth(bob), "Pendulum bob", fill=brass(bob, WBRASS_STOPS),
       stroke=INK, strokeWidth=1.8)
bcx, bcy = P(-3.0, 30.0, 2.2)
d.shape("ellipse", "Bob glint", x=round(bcx - 6), y=round(bcy - 8),
        width=9, height=12, fill="#F2C97E", opacity=55, stroke=NONE)

# --- case: far side stile, trunk sides, plinth -------------------------------------------
# trunk = two full-depth side cheeks + rails, front left open for the door
prism("Trunk side L", box(-8.5, 18, -4, -5.8, 58, 4), lo=0.05, hi=0.9)
prism("Trunk rail top", box(-8.5, 55.5, -4, 8.5, 58, 4), lo=0.05, hi=0.9)
prism("Trunk rail bottom", box(-8.5, 18, -4, 8.5, 20.5, 4), lo=0.05, hi=0.9)
# plinth: wider base block + stepped foot moulding + front panel
prism("Plinth", box(-10.5, 3, -5, 10.5, 18, 5), lo=0.06, hi=0.95, ink=2.0)
prism("Base moulding", box(-11.4, 0, -5.6, 11.4, 3.4, 5.6), lo=0.05, hi=0.9)
d.path(poly(fquad(-7.5, 6, 7.5, 15.5, -5.05)), "Plinth panel",
       fill=lin((0, P(0, 15.5, -5)[1]), (0, P(0, 6, -5)[1]),
                (0, "#4A2412"), (1, "#2A140A")),
       stroke=INK, strokeWidth=2.0, join="round")
d.path(poly(fquad(-6.3, 7.2, 6.3, 14.3, -5.05)), "Plinth panel inset",
       fill=NONE, stroke="#C08048", strokeWidth=1.6, opacity=40)

# --- door: glass over the trunk opening, then its frame ---------------------------------
d.path(poly(fquad(-5.8, 20.5, 5.8, 55.5, -4.05)), "Door glass",
       fill=lin((0, P(0, 55.5, -4)[1]), (0, P(0, 20.5, -4)[1]),
                (0, "#C8DCD0", 14), (0.5, "#9AB8AC", 7), (1, "#C8DCD0", 18)),
       stroke=NONE)
# long sheen down the glass
ga, gb = P(-4.0, 54.5, -4.1), P(0.5, 22, -4.1)
gc, gd = P(-1.5, 54.5, -4.1), P(3.0, 22, -4.1)
d.path(poly([ga, gc, gd, gb]), "Glass sheen", fill="#F4FBF6",
       opacity=7, stroke=NONE)
# door frame: stiles and rails standing proud of the case front
prism("Door stile L", box(-7.6, 19, -4.9, -5.4, 57, -4.0), lo=0.10, hi=1.0, ink=1.6)
prism("Door stile R", box(5.4, 19, -4.9, 7.6, 57, -4.0), lo=0.10, hi=1.0, ink=1.6)
prism("Door rail T", box(-7.6, 55.4, -4.9, 7.6, 57.6, -4.0), lo=0.10, hi=1.0, ink=1.6)
prism("Door rail B", box(-7.6, 18.4, -4.9, 7.6, 20.6, -4.0), lo=0.10, hi=1.0, ink=1.6)
# escutcheon on the near stile — the mechanism read by its pivot
ecx, ecy = P(6.5, 39, -4.95)
d.shape("ellipse", "Escutcheon", x=round(ecx - 4), y=round(ecy - 5),
        width=8, height=10,
        fill=rad((0, "#F2C97E"), (0.55, "#9A6428"), (1, "#3A2210")),
        stroke=INK, strokeWidth=1.4)

# near trunk cheek last — it overlaps the door's right edge
prism("Trunk side R", box(5.8, 18, -4, 8.5, 58, 4), lo=0.08, hi=1.0)

# --- hood: case, cornice, columns, dial ---------------------------------------------------
prism("Hood", box(-9.5, 58, -4.5, 9.5, 74, 4.5), lo=0.06, hi=0.95, ink=2.0)
prism("Cornice", box(-10.8, 74, -5.4, 10.8, 77, 5.4), lo=0.05, hi=0.9, ink=2.0)
# frieze line under the cornice
fa, fb = P(-9.5, 73.2, -4.55), P(9.5, 73.2, -4.55)
d.path(f"M{fa[0]:.1f},{fa[1]:.1f} L{fb[0]:.1f},{fb[1]:.1f}", "Frieze line",
       fill=NONE, stroke="#C08048", strokeWidth=1.6, opacity=45)
# finials: three brass balls on the cornice
for i, fx in enumerate((-8, 0, 8)):
    fcx, fcy = P(fx, 78.2, 0)
    d.shape("ellipse", f"Finial {i+1}", x=round(fcx - 8), y=round(fcy - 8),
            width=16, height=16,
            fill=rad((0, "#F2C97E"), (0.55, "#9A6428"), (1, "#3A2210")),
            stroke=INK, strokeWidth=1.6)
    d.path(f"M{fcx - 3:.1f},{fcy + 6:.1f} L{fcx + 3:.1f},{fcy + 6:.1f}",
           f"Finial stem {i+1}", fill=NONE, stroke=INK, strokeWidth=3.0)
# hood columns flanking the dial
for i, cx in enumerate((-8.2, 8.2)):
    prism(f"Hood column {i+1}", box(cx - 0.9, 59.5, -5.3, cx + 0.9, 73, -4.2),
          lo=0.14, hi=1.0, ink=1.6)
    cap = fquad(cx - 1.3, 72.4, cx + 1.3, 73.6, -4.6)
    d.path(poly(cap), f"Column cap {i+1}", fill=brass(cap), stroke=INK,
           strokeWidth=1.4)
    base = fquad(cx - 1.3, 59.0, cx + 1.3, 60.2, -4.6)
    d.path(poly(base), f"Column base {i+1}", fill=brass(base), stroke=INK,
           strokeWidth=1.4)

# dial: brass bezel, silvered chapter ring, tick marks, two hands at ten past ten
DX, DY, DZ = 0, 66.4, -4.55
bez = fcircle(DX, DY, DZ, 7.3)
d.path(smooth(bez), "Dial bezel", fill=brass(bez), stroke=INK,
       strokeWidth=2.0)
d.path(smooth(fcircle(DX, DY, DZ - 0.02, 6.4)), "Dial face",
       fill=rad((0, "#F2E8CC"), (0.7, "#D8C9A2"), (1, "#A89878")),
       stroke="#4A3820", strokeWidth=1.6)
# ticks: cardinals longer and heavier
for i in range(12):
    a = math.radians(i * 30)
    card = i % 3 == 0
    r0, r1 = (5.0, 6.0) if card else (5.4, 6.0)
    t0 = P(DX + r0 * math.sin(a), DY + r0 * math.cos(a), DZ - 0.04)
    t1 = P(DX + r1 * math.sin(a), DY + r1 * math.cos(a), DZ - 0.04)
    d.path(f"M{t0[0]:.1f},{t0[1]:.1f} L{t1[0]:.1f},{t1[1]:.1f}",
           f"Tick {i+1}", fill=NONE, stroke="#2E2010",
           strokeWidth=3.4 if card else 2.6, cap="round")


def hand(angle_deg, length, w0, w1):
    a = math.radians(angle_deg)
    ux, uy = math.sin(a), math.cos(a)
    nx, ny = uy, -ux
    pts = [P(DX - nx * w0, DY - ny * w0, DZ - 0.06),
           P(DX + ux * length - nx * w1, DY + uy * length - ny * w1, DZ - 0.06),
           P(DX + ux * length + nx * w1, DY + uy * length + ny * w1, DZ - 0.06),
           P(DX + nx * w0, DY + ny * w0, DZ - 0.06)]
    return poly(pts)


d.path(hand(305, 3.4, 0.55, 0.22), "Hour hand", fill="#241608",
       stroke="#241608", strokeWidth=1.0, join="round")
d.path(hand(62, 4.9, 0.45, 0.18), "Minute hand", fill="#241608",
       stroke="#241608", strokeWidth=1.0, join="round")
pcx, pcy = P(DX, DY, DZ - 0.08)
d.shape("ellipse", "Hand pin", x=round(pcx - 4), y=round(pcy - 4),
        width=8, height=8,
        fill=rad((0, "#F2C97E"), (0.55, "#9A6428"), (1, "#3A2210")),
        stroke=INK, strokeWidth=1.2)

# case edge sheen: a long polished line up the near trunk corner
ea, eb = P(8.5, 20, -4.1), P(8.5, 56, -4.1)
d.path(f"M{ea[0]:.1f},{ea[1]:.1f} L{eb[0]:.1f},{eb[1]:.1f}", "Case edge sheen",
       fill=NONE, stroke=WOOD_HI, strokeWidth=3.0, opacity=30, cap="round")

# --- extent check ---------------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("clock extent: farthest point %.0f from centre (rim %d)" % (far, PR))
assert far < PR - 26, far


# --- caption ----------------------------------------------------------------------------------
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
               color="#F0EAD4", justify="center")
    m = d.text(mats, "Materials", x=500, y=970, size=22, font="Virelai Sans",
               color="#C0B898", justify="center")
    d.cmd("text.setStyle", "Name tracking", ids=[n["id"]], tracking=60)
    d.cmd("text.setStyle", "Materials tracking", ids=[m["id"]], tracking=260)
    doc = d.m.call("doc_inspect", {})
    for oid, label in ((n["id"], "name"), (m["id"], "materials")):
        b = find(doc, oid)
        nearest = (min(max(PCX, b["x"]), b["x"] + b["width"]),
                   min(max(PCY, b["y"]), b["y"] + b["height"]))
        clear = math.hypot(nearest[0] - PCX, nearest[1] - PCY) - (PR + 3)
        print("%s: %.0fx%.0f at y %.0f, clears rim by %.1f" %
              (label, b["width"], b["height"], b["y"], clear))
        assert clear > 0 and b["x"] >= 10 and b["x"] + b["width"] <= 990, label
        if label == "materials":
            assert b["width"] <= 760, b["width"]


caption("GRANDFATHER CLOCK", "MAHOGANY · BRASS · GLASS")
d.finish("grandfather-clock-V1R00")
