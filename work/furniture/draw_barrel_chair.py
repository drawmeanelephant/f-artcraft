#!/usr/bin/env python3
"""Barrel chair — field plate V1R00. Three-quarter from the front right:
a tub of vertical oak staves hooped with iron bands, the front third cut
away; inside, a wool seat pad and a slumped cushion against the back wall.
Snug mood: warm russet plate, low amber light. 1000x1000.
Modelled in inches (x right, y up, +z back), fixed yaw + pitch projection;
staves are rotated 8-corner prisms set on a circle, hoops and seat bands
are arc ribbons on the tub's surface.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Barrel Chair — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#201410"   # warm dark, not black
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
YAW, PITCH = math.radians(26), math.radians(22)
S, OX, OY = 14.5, 500.0, 688.0
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


FACES = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4),
         (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
TO_VIEWER = (SY * CP, SP, -CY * CP)          # normals facing this draw
LIGHT = (-0.45, 0.80, -0.42)
_l = math.sqrt(sum(c * c for c in LIGHT))
LIGHT = tuple(c / _l for c in LIGHT)


OAK_D, OAK_L = "#2E1A0C", "#96642E"        # oak ramp
OAK_HI = "#C89050"


def prism(name, corners, lo=0.06, hi=0.94, ink=1.8, c1=OAK_D, c2=OAK_L,
          bias=0.0):
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
        b = lo + (hi - lo) * max(0.0, lam + bias) ** 0.8
        b = max(0.0, min(1.0, b))
        y0, y1 = min(p[1] for p in pts), max(p[1] for p in pts)
        g = lin((0, y0), (0, y1), (0, shade(c1, c2, min(1, b + 0.12))),
                                 (1, shade(c1, c2, b)))
        d.path(poly(pts), name, fill=g, stroke=INK, strokeWidth=ink, join="round")
    return faces


def rbox(cx, cz, y0, y1, hw, ht, ang):
    """Box hw x ht in plan, rotated ang about y through (cx,cz), box() ordering."""
    ca, sa = math.cos(ang), math.sin(ang)
    cs = [(cx + lx * ca + lz * sa, cz - lx * sa + lz * ca)
          for lx, lz in ((-hw, -ht), (hw, -ht), (hw, ht), (-hw, ht))]
    A, B, C, D = cs
    return [(A[0], y0, A[1]), (B[0], y0, B[1]), (B[0], y1, B[1]),
            (A[0], y1, A[1]), (D[0], y0, D[1]), (C[0], y0, C[1]),
            (C[0], y1, C[1]), (D[0], y1, D[1])]


def arc_pts(r, y, a0, a1, n=18, cz0=2.0):
    """Points on the tub's surface: angle a measured from straight back (+z)."""
    return [P(r * math.sin(math.radians(a0 + (a1 - a0) * i / n)), y,
              cz0 + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)))
            for i in range(n + 1)]


def band(r, y0, y1, a0, a1, n=18):
    """Vertical ribbon on the tub wall between y0 and y1."""
    return poly(arc_pts(r, y1, a0, a1, n) + arc_pts(r, y0, a1, a0, n))


# --- backdrop + plate ---------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#1A100E"), (1, "#0A0605")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#8A5A3A", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#52382C"), (0.6, "#3A2620"), (1, "#18100C")),
        stroke="#0E0806", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8CBA8", strokeWidth=3, opacity=22)
d.shape("ellipse", "Hearth light", x=200, y=140, width=560, height=560,
        fill=rad((0, "#E09A4E", 18), (0.55, "#96602E", 6), (1, "#96602E", 0)),
        stroke=NONE)

FY = 700
hx = math.sqrt(PR ** 2 - (FY - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{FY} L{PCX + hx:.1f},{FY} A420,420 0 0 1 {PCX - hx:.1f},{FY} Z",
       "Floor", fill=lin((0, FY), (0, 880), (0, "#563E2E", 36), (1, "#140C08", 72)),
       stroke=NONE)
d.path(f"M{PCX - hx + 6:.1f},{FY} L{PCX + hx - 6:.1f},{FY}", "Floor edge light",
       fill=NONE, stroke="#EACBA0", strokeWidth=2, opacity=18)

# --- tub geometry (inches; barrel centre at (0,2), radius ~13.5) -----------------------
RT, CZ = 13.5, 2.0            # stave centreline radius / tub centre z
STAVE_Y0, STAVE_Y1 = 1.5, 21.0

# grounding shadow
sp = [P(x, 0, z) for x, z in [(-14.5, -12), (14.5, -12), (14.5, 16), (-14.5, 16)]]
sx0, sx1 = min(p[0] for p in sp) - 34, max(p[0] for p in sp) + 34
sy0, sy1 = min(p[1] for p in sp) - 14, max(p[1] for p in sp) + 16
d.shape("ellipse", "Chair shadow", x=round(sx0), y=round(sy0),
        width=round(sx1 - sx0), height=round(sy1 - sy0),
        fill=rad((0, "#050302", 70), (0.6, "#050302", 28), (1, "#050302", 0)),
        stroke=NONE)

# --- staves: rotated prisms on the circle -------------------------------------------------
# tall staves wrap the back (|a|<=72); the tub continues around the front as
# staves cut low to seat height — the opening is the cut-down front, not a hole.
def stave_pts(a, y1):
    cx = RT * math.sin(math.radians(a))
    cz = CZ + RT * math.cos(math.radians(a))
    return cx, cz


tall, short = [], []
for i, a in enumerate([x * 9.0 for x in range(-8, 33)]):
    cx, cz = stave_pts(a, 0)
    (tall if abs(a) <= 72 else short).append((a, cx, cz))
for a, cx, cz in sorted(tall, key=lambda t: -depth(t[1], 11, t[2])):
    jitter = (0.5 - ((int(a + 90) * 37) % 10) / 10) * 0.10
    prism(f"Stave {a:+.0f}", rbox(cx, cz, 0.6, STAVE_Y1, 0.95, 0.5,
                                  math.radians(a)),
          lo=0.04, hi=0.98, ink=1.5, bias=jitter)

# interior wall shadow: dims the staves' inward faces above the seat
d.path(band(RT - 1.0, 9.0, 20.7, -70, 70), "Interior shade",
       fill="#140A06", opacity=30, stroke=NONE)
# dark skin behind the low front staves, so the seams read as depth
d.path(band(RT - 1.0, 0.6, 9.2, -66, 250), "Trough shade",
       fill="#100805", opacity=55, stroke=NONE)

# --- seat: wool pad with a front wall band, then the top disc ----------------------------
seat_pts = arc_pts(11.4, 8.6, 95, 265, 24) + arc_pts(11.4, 10.7, 265, 95, 24)
d.path(poly(seat_pts), "Seat front",
       fill=lin((0, min(p[1] for p in seat_pts)), (0, max(p[1] for p in seat_pts)),
                (0, "#3A1216"), (0.6, "#7A2C32"), (1, "#2C0E12")),
       stroke=INK, strokeWidth=1.8, join="round")
top_pts = [P(11.4 * math.sin(math.radians(t)), 10.7,
             CZ + 11.4 * math.cos(math.radians(t)))
           for t in range(0, 360, 12)]
d.path(smooth(top_pts), "Seat pad",
       fill=rad((0, "#A03840"), (0.55, "#72242C"), (1, "#40141A")),
       stroke=INK, strokeWidth=2.0, join="round")
# stitched welt around the pad's edge, front half
welt = arc_pts(10.5, 10.8, 95, 265, 26)
d.path(smooth(welt, closed=False), "Seat welt", fill=NONE,
       stroke="#2C0E12", strokeWidth=2.4, opacity=60)

# --- cushion: a slumped pad leaning back on the wall, left of centre ----------------------
pc, rdir, upv = (-4.6, 13.0, 8.2), (0.92, 0.0, -0.39), (0.0, 0.88, 0.47)
w, h = 7.2, 3.5
pts = []
for i in range(8):
    t = 2 * math.pi * i / 8 + math.pi / 8
    pts.append((pc[0] + math.cos(t) * w * rdir[0] + math.sin(t) * h * upv[0],
                pc[1] + math.sin(t) * h * upv[1],
                pc[2] + math.cos(t) * w * rdir[2] + math.sin(t) * h * upv[2]))
# contact shadow where the cushion meets the seat
csx, csy = P(pc[0] + 0.6, 10.9, pc[2] + 1.0)
d.shape("ellipse", "Cushion seat shadow", x=round(csx - 52), y=round(csy - 7),
        width=110, height=16, fill="#200808", opacity=45, stroke=NONE)
d.path(smooth([P(*p) for p in pts]), "Cushion",
       fill=rad((0, "#A8443C"), (0.55, "#7A2A26"), (1, "#401310")),
       stroke=INK, strokeWidth=1.8)
pcx, pcy = P(pc[0] + 0.3, pc[1] - 0.6, pc[2] - 0.3)
d.shape("ellipse", "Cushion dimple", x=round(pcx - 4), y=round(pcy - 3),
        width=8, height=6, fill="#2C0E0C", opacity=45, stroke=NONE)

# --- low front staves: nearest the viewer, drawn over the seat edge -------------------------
for a, cx, cz in sorted(short, key=lambda t: -depth(t[1], 5, t[2])):
    jitter = (0.5 - ((int(a + 180) * 37) % 10) / 10) * 0.10
    prism(f"Stave low {a:+.0f}", rbox(cx, cz, 0.6, 8.8, 0.95, 0.5,
                                      math.radians(a)),
          lo=0.06, hi=0.95, ink=1.5, bias=jitter)

# --- hoops: iron bands on the tub's outside ------------------------------------------------
def hoop(r, y0, y1, a0, a1, name):
    pts = arc_pts(r, y1, a0, a1, 24) + arc_pts(r, y0, a1, a0, 24)
    y0s = min(p[1] for p in pts)
    y1s = max(p[1] for p in pts)
    d.path(poly(pts), name,
           fill=lin((0, y0s), (0, y1s), (0, "#14100C"), (0.5, "#453A2E"),
                    (0.72, "#5E5042"), (1, "#1C1611")),
           stroke=INK, strokeWidth=1.5, join="round")
    return pts


# lower hoop runs the whole front of the tub (rail zone) and tucks behind the ends
hoop(RT + 0.62, 2.4, 4.2, 62, 242, "Hoop low")
# upper hoop: only the right shoulder faces this viewer
hoop(RT + 0.62, 17.9, 19.7, 62, 75, "Hoop high")

# --- edge light on the opening's cut stave ends --------------------------------------------
for a, lbl in ((73.5, "R"), (-73.5, "L")):
    cx = RT * math.sin(math.radians(a))
    cz = CZ + RT * math.cos(math.radians(a))
    ta, tb = P(cx, 3.0, cz), P(cx, 20.0, cz)
    d.path(f"M{ta[0]:.1f},{ta[1]:.1f} L{tb[0]:.1f},{tb[1]:.1f}",
           f"Cut edge light {lbl}", fill=NONE, stroke=OAK_HI,
           strokeWidth=2.6, opacity=40, cap="round")

# top rim: warm kiss along the far stave tops seen through the opening
rim = arc_pts(RT - 1.0, 20.6, -55, 55, 20)
d.path(smooth(rim, closed=False), "Rim light", fill=NONE, stroke=OAK_HI,
       strokeWidth=2.2, opacity=30, cap="round")

# --- extent check ---------------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("chair extent: farthest point %.0f from centre (rim %d)" % (far, PR))
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
               color="#F4E0C8", justify="center")
    m = d.text(mats, "Materials", x=500, y=970, size=22, font="Virelai Sans",
               color="#CDA884", justify="center")
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


caption("BARREL CHAIR", "OAK · WOOL · IRON")
d.finish("barrel-chair-V1R00")
