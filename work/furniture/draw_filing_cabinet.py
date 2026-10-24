#!/usr/bin/env python3
"""Filing cabinet — field plate V1R00. Three-quarter from the front
right: a four-drawer vertical letter file in office grey-green enamel —
recessed base, four deep drawer fronts each carrying a recessed pull and
a nickel card frame, key cylinder on the top drawer. Office mood: cool
slate plate, a wash of fluorescent light from the upper left, venetian
streaks across the wall. 1000x1000.
Modelled in inches (x right, y up, +z back), fixed yaw + pitch projection;
carcass and drawer fronts are 8-corner prisms, hardware is drawn in the
case's front plane.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Filing Cabinet — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#14181A"   # cool warm-dark, not black
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
YAW, PITCH = math.radians(21), math.radians(10)
S, OX, OY = 10.6, 498.0, 786.0
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
LIGHT = (-0.42, 0.82, -0.38)
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


STEEL_D, STEEL_L = "#202726", "#7E8B84"    # enamelled steel ramp
STEEL_HI = "#BCC6BE"                       # enamel sheen


def prism(name, corners, lo=0.06, hi=0.94, ink=1.8, c1=STEEL_D, c2=STEEL_L):
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


NICKEL_STOPS = ((0, "#3E4442"), (0.45, "#9AA49C"),
                (0.62, "#E4EAE0"), (1, "#565E58"))


def nickel(pts):
    """Vertical metal ramp spanning the projected points' own y-extent."""
    y0 = min(p[1] for p in pts)
    y1 = max(p[1] for p in pts)
    return lin((0, y0), (0, y1), *NICKEL_STOPS)


# --- backdrop + plate ---------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#141B1E"), (1, "#070B0D")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#5E7078", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#37434A"), (0.6, "#262F35"), (1, "#10161A")),
        stroke="#0A0F12", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D2DEE2", strokeWidth=3, opacity=20)
# fluorescent wash from the upper left
d.shape("ellipse", "Office light", x=180, y=90, width=560, height=560,
        fill=rad((0, "#CFE0D8", 15), (0.55, "#8AA098", 6), (1, "#8AA098", 0)),
        stroke=NONE)
# venetian streaks — short soft bands across the upper disc
for i, (bx, by, bw) in enumerate([(288, 196, 210), (330, 236, 190), (376, 276, 160)]):
    d.path(f"M{bx},{by} L{bx + bw},{by - bw * 0.16}", f"Blind band {i + 1}",
           fill=NONE, stroke="#DEEAE2", strokeWidth=9, opacity=7, cap="round")

FY = 712
hx = math.sqrt(PR ** 2 - (FY - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{FY} L{PCX + hx:.1f},{FY} A420,420 0 0 1 {PCX - hx:.1f},{FY} Z",
       "Floor", fill=lin((0, FY), (0, 880), (0, "#3E4844", 30), (1, "#0C100E", 70)),
       stroke=NONE)
d.path(f"M{PCX - hx + 6:.1f},{FY} L{PCX + hx - 6:.1f},{FY}", "Floor edge light",
       fill=NONE, stroke="#D8E2DA", strokeWidth=2, opacity=16)

# --- case geometry (inches; x right, y up, +z back) ------------------------------------
# letter file: 15.5 wide, 25 deep, 52 tall on a recessed base
XW, ZD = 7.75, 12.5
shadow_pts = [P(-XW, 0, -ZD), P(XW, 0, -ZD), P(XW, 0, ZD), P(-XW, 0, ZD)]
sx0 = min(p[0] for p in shadow_pts) - 46
sx1 = max(p[0] for p in shadow_pts) + 40
sy0 = min(p[1] for p in shadow_pts) - 12
sy1 = max(p[1] for p in shadow_pts) + 22
d.shape("ellipse", "Cabinet shadow", x=round(sx0), y=round(sy0),
        width=round(sx1 - sx0), height=round(sy1 - sy0),
        fill=rad((0, "#030605", 70), (0.6, "#030605", 28), (1, "#030605", 0)),
        stroke=NONE)

# recessed plinth: inset toe-kick block, darker
prism("Plinth", box(-6.9, 0.6, -11.4, 6.9, 3.4, 11.4),
      lo=0.03, hi=0.55, ink=1.8, c1="#101414", c2="#3E4642")
# two levelling glides peeking under the front lip
for i, gx in enumerate((-5.4, 5.4)):
    gcx, gcy = P(gx, 0.3, -11.6)
    d.shape("ellipse", f"Glide {i + 1}", x=round(gcx - 8), y=round(gcy - 2),
            width=16, height=6,
            fill=rad((0, "#6A746C"), (1, "#1A1E1C")), stroke=INK, strokeWidth=1.2)

# carcass
prism("Carcass", box(-XW, 3.4, -ZD, XW, 52.4, ZD), lo=0.06, hi=0.95, ink=2.0)
# top cap: a hair overhang all round, enamel catching the light
prism("Top cap", box(-XW - 0.35, 52.4, -ZD - 0.35, XW + 0.35, 53.6, ZD + 0.35),
      lo=0.10, hi=1.0, ink=2.0)

# --- drawer fronts, proud of the carcass -----------------------------------------------
# four drawers from y=5.2 to y=50.8, each ~10.7 tall with 0.7 gaps
FRT = -ZD - 0.55                      # front plane of the drawer faces
for i in range(4):
    y0 = 5.2 + i * 11.4
    y1 = y0 + 10.7
    prism(f"Drawer {i + 1}", box(-7.3, y0, FRT - 0.25, 7.3, y1, -ZD),
          lo=0.10, hi=0.98, ink=1.7)

# per-drawer hardware in the front plane: recessed pull + card frame
for i in range(4):
    y0 = 5.2 + i * 11.4
    y1 = y0 + 10.7
    ym = (y0 + y1) / 2
    # recessed pull: dark slot, finger lip catching the light on its upper edge
    slot = fquad(-3.1, ym - 0.55, 3.1, ym + 1.15, FRT - 0.30)
    d.path(poly(slot), f"Pull recess {i + 1}",
           fill=lin((0, slot[0][1]), (0, slot[2][1]),
                    (0, "#161C1B"), (1, "#38423E")),
           stroke=INK, strokeWidth=1.5, join="round")
    lip = fquad(-3.0, ym + 0.72, 3.0, ym + 1.12, FRT - 0.36)
    d.path(poly(lip), f"Pull lip {i + 1}", fill=nickel(lip), stroke=NONE)
    la, lb = P(-2.9, ym + 0.78, FRT - 0.40), P(2.9, ym + 0.78, FRT - 0.40)
    d.path(f"M{la[0]:.1f},{la[1]:.1f} L{lb[0]:.1f},{lb[1]:.1f}",
           f"Pull glint {i + 1}", fill=NONE, stroke="#E8EEE6",
           strokeWidth=1.6, opacity=70, cap="round")
    # card frame above the pull: nickel border, manila card, two ruled lines
    cf = fquad(-2.15, ym + 1.75, 2.15, ym + 3.35, FRT - 0.28)
    d.path(poly(cf), f"Card frame {i + 1}", fill=nickel(cf),
           stroke=INK, strokeWidth=1.4, join="round")
    cd = fquad(-1.8, ym + 2.0, 1.8, ym + 3.1, FRT - 0.32)
    d.path(poly(cd), f"Card {i + 1}",
           fill=lin((0, cd[0][1]), (0, cd[2][1]), (0, "#E8DCBE"), (1, "#C4B694")),
           stroke="#6A5E40", strokeWidth=0.9)
    for k in range(2):
        la, lb = P(-1.35, ym + 2.45 + 0.42 * k, FRT - 0.36), \
                 P(1.35, ym + 2.45 + 0.42 * k, FRT - 0.36)
        d.path(f"M{la[0]:.1f},{la[1]:.1f} L{lb[0]:.1f},{lb[1]:.1f}",
               f"Card rule {i + 1}-{k + 1}", fill=NONE,
               stroke="#8A7C58", strokeWidth=1.1, opacity=70)

# key cylinder above the top drawer's pull, offset right
kcx, kcy = P(5.3, 50.0, FRT - 0.30)
d.shape("ellipse", "Key bezel", x=round(kcx - 7), y=round(kcy - 7),
        width=14, height=14,
        fill=rad((0, "#E4EAE0"), (0.55, "#9AA49C"), (1, "#3E4442")),
        stroke=INK, strokeWidth=1.4)
d.shape("ellipse", "Key slot", x=round(kcx - 2.5), y=round(kcy - 1),
        width=5, height=8, fill="#14181A", stroke=NONE)

# baked-enamel sheen down the near front corner + a softer one on the far
ea, eb = P(XW - 0.4, 8, FRT - 0.1), P(XW - 0.4, 50, FRT - 0.1)
d.path(f"M{ea[0]:.1f},{ea[1]:.1f} L{eb[0]:.1f},{eb[1]:.1f}", "Corner sheen",
       fill=NONE, stroke=STEEL_HI, strokeWidth=3.2, opacity=26, cap="round")
sa, sb = P(-XW + 1.2, 10, -ZD - 0.1), P(-XW + 1.2, 48, -ZD - 0.1)
d.path(f"M{sa[0]:.1f},{sa[1]:.1f} L{sb[0]:.1f},{sb[1]:.1f}", "Far sheen",
       fill=NONE, stroke=STEEL_HI, strokeWidth=4.5, opacity=12, cap="round")
# soft reflected band across the side face, painted-steel glow
q0, q1 = P(XW + 0.05, 6, -4), P(XW + 0.05, 6, 8)
q2, q3 = P(XW + 0.05, 50, 10), P(XW + 0.05, 50, -1)
d.path(poly([q0, q1, q2, q3]), "Side sheen", fill="#C8D2CA",
       opacity=9, stroke=NONE)

# --- extent check ---------------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("cabinet extent: farthest point %.0f from centre (rim %d)" % (far, PR))
assert far < PR - 20, far


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
               color="#E2ECE8", justify="center")
    m = d.text(mats, "Materials", x=500, y=970, size=22, font="Virelai Sans",
               color="#AEC0B8", justify="center")
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


caption("FILING CABINET", "STEEL · ENAMEL · NICKEL")
d.finish("filing-cabinet-V1R00")
