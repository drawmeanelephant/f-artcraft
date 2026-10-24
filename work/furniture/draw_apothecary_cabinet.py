#!/usr/bin/env python3
"""Apothecary cabinet — field plate V1R00. Three-quarter from the front
right: an oak counter chest of thirty-six small drawers in six columns
and six rows, every drawer with a brass card frame and a cup pull,
bracket feet under a plinth, a stepped cornice on top. Two amber
tincture bottles stand on the cornice to pin the scale. Tincture mood:
deep amber plate, warm lamplight from the left. 1000x1000.
Modelled in inches (x right, y up, +z back), fixed yaw + pitch projection;
carcass and drawer fronts are 8-corner prisms, labels and pulls are
drawn in the front plane.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Apothecary Cabinet — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#241608"   # warm dark, not black
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
YAW, PITCH = math.radians(20), math.radians(10)
S, OX, OY = 12.0, 498.0, 712.0
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
LIGHT = (-0.50, 0.78, -0.38)
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


OAK_D, OAK_L = "#2C1808", "#8A5A26"        # oak ramp
OAK_HI = "#C89A58"                         # polished sheen


def prism(name, corners, lo=0.06, hi=0.94, ink=1.8, c1=OAK_D, c2=OAK_L):
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


BRASS_STOPS = ((0, "#4A2A0E"), (0.45, "#B8842E"),
               (0.62, "#F2C97E"), (1, "#5A3410"))


def brass(pts):
    """Vertical brass ramp spanning the projected points' own y-extent."""
    y0 = min(p[1] for p in pts)
    y1 = max(p[1] for p in pts)
    return lin((0, y0), (0, y1), *BRASS_STOPS)


# --- backdrop + plate ---------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#1C140C"), (1, "#090604")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#7A6238", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#463A26"), (0.6, "#2E2416"), (1, "#120D06")),
        stroke="#0C0804", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E4D6B4", strokeWidth=3, opacity=20)
# warm lamp pool from the left — the shop's amber light
d.shape("ellipse", "Lamplight", x=110, y=140, width=560, height=560,
        fill=rad((0, "#F0C878", 20), (0.5, "#9A6E30", 7), (1, "#9A6E30", 0)),
        stroke=NONE)
# dusty shelf line far back right + two vague jar silhouettes
d.path("M640,330 L846,318", "Back shelf", fill=NONE, stroke="#C8A860",
       strokeWidth=2.5, opacity=14)
for i, (jx, jy, jw, jh) in enumerate([(700, 280, 34, 48), (748, 292, 26, 36)]):
    d.shape("ellipse", f"Back jar {i + 1}", x=jx, y=jy, width=jw, height=jh,
            fill=rad((0, "#8A6A34", 22), (1, "#3A2A12", 10)), stroke=NONE)

FY = 716
hx = math.sqrt(PR ** 2 - (FY - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{FY} L{PCX + hx:.1f},{FY} A420,420 0 0 1 {PCX - hx:.1f},{FY} Z",
       "Floor", fill=lin((0, FY), (0, 880), (0, "#4A3A22", 30), (1, "#0E0904", 70)),
       stroke=NONE)
d.path(f"M{PCX - hx + 6:.1f},{FY} L{PCX + hx - 6:.1f},{FY}", "Floor edge light",
       fill=NONE, stroke="#E0CE9E", strokeWidth=2, opacity=16)

# --- case geometry (inches; x right, y up, +z back) ------------------------------------
# counter chest: 40 wide, 42 tall to the cornice, 10 deep
XW, ZD = 20.0, 5.0
shadow_pts = [P(-XW, 0, -ZD), P(XW, 0, -ZD), P(XW, 0, ZD), P(-XW, 0, ZD)]
sx0 = min(p[0] for p in shadow_pts) - 46
sx1 = max(p[0] for p in shadow_pts) + 40
sy0 = min(p[1] for p in shadow_pts) - 12
sy1 = max(p[1] for p in shadow_pts) + 22
d.shape("ellipse", "Cabinet shadow", x=round(sx0), y=round(sy0),
        width=round(sx1 - sx0), height=round(sy1 - sy0),
        fill=rad((0, "#050302", 70), (0.6, "#050302", 28), (1, "#050302", 0)),
        stroke=NONE)

# bracket feet: two little squared paws under the plinth
for i, fx in enumerate((-17.6, 15.6)):
    prism(f"Foot {i + 1}", box(fx, 0, -ZD - 0.5, fx + 2.0, 3.2, ZD - 0.8),
          lo=0.05, hi=0.8, ink=1.7)
# plinth rail between the feet
prism("Plinth", box(-XW, 2.6, -ZD - 0.4, XW, 5.4, ZD), lo=0.05, hi=0.85, ink=1.8)

# carcass
prism("Carcass", box(-XW, 5.4, -ZD, XW, 40.4, ZD), lo=0.06, hi=0.95, ink=2.0)
# cornice: stepped cap, two courses
prism("Cornice low", box(-XW - 0.7, 40.4, -ZD - 0.7, XW + 0.7, 41.8, ZD + 0.7),
      lo=0.08, hi=0.95, ink=1.9)
prism("Cornice top", box(-XW - 0.3, 41.8, -ZD - 0.3, XW + 0.3, 43.0, ZD + 0.3),
      lo=0.10, hi=1.0, ink=1.9)

# --- drawer grid: 6 x 6 small drawers, proud fronts ------------------------------------
COLS, ROWS = 6, 6
GX0, GX1 = -19.4, 19.4
GY0, GY1 = 6.4, 39.6
CW = (GX1 - GX0) / COLS
RH = (GY1 - GY0) / ROWS
FRT = -ZD - 0.42                      # front plane of the drawer faces

for r in range(ROWS):
    for c in range(COLS):
        x0 = GX0 + c * CW + 0.32
        x1 = GX0 + (c + 1) * CW - 0.32
        y0 = GY0 + r * RH + 0.30
        y1 = GY0 + (r + 1) * RH - 0.30
        prism(f"Drawer {r + 1}-{c + 1}", box(x0, y0, FRT - 0.22, x1, y1, -ZD),
              lo=0.10, hi=0.98, ink=1.3)

# per-drawer furniture: brass card frame + card, cup pull below
for r in range(ROWS):
    for c in range(COLS):
        xm = GX0 + (c + 0.5) * CW
        ym = GY0 + (r + 0.5) * RH
        # card frame: brass border, cream card, ruled lines that vary by drawer
        cf = fquad(xm - 1.85, ym + 0.55, xm + 1.85, ym + 1.85, FRT - 0.26)
        d.path(poly(cf), f"Label frame {r + 1}-{c + 1}", fill=brass(cf),
               stroke=INK, strokeWidth=1.1, join="round")
        cd = fquad(xm - 1.55, ym + 0.8, xm + 1.55, ym + 1.6, FRT - 0.30)
        d.path(poly(cd), f"Label card {r + 1}-{c + 1}",
               fill=lin((0, cd[0][1]), (0, cd[2][1]), (0, "#EEE0BC"), (1, "#C9B98E")),
               stroke="#6A5A38", strokeWidth=0.8)
        nlines = 1 + (r * COLS + c) % 3          # each remedy's card differs
        for k in range(nlines):
            lx0 = xm - 1.1
            lx1 = xm - 0.3 + 1.2 * ((r + c + k) % 3) / 2
            la, lb = P(lx0, ym + 1.02 + 0.26 * k, FRT - 0.34), \
                     P(lx1, ym + 1.02 + 0.26 * k, FRT - 0.34)
            d.path(f"M{la[0]:.1f},{la[1]:.1f} L{lb[0]:.1f},{lb[1]:.1f}",
                   f"Label rule {r + 1}-{c + 1}-{k}", fill=NONE,
                   stroke="#7A6A44", strokeWidth=0.9, opacity=70)
        # cup pull: dark scoop with a brass rim glint
        cup = fquad(xm - 1.3, ym - 1.75, xm + 1.3, ym - 0.95, FRT - 0.26)
        d.path(poly(cup), f"Cup pull {r + 1}-{c + 1}",
               fill=lin((0, cup[0][1]), (0, cup[2][1]),
                        (0, "#1C0E04"), (1, "#4A3010")),
               stroke=INK, strokeWidth=1.1, join="round")
        ga, gb = P(xm - 1.15, ym - 1.02, FRT - 0.30), P(xm + 1.15, ym - 1.02, FRT - 0.30)
        d.path(f"M{ga[0]:.1f},{ga[1]:.1f} L{gb[0]:.1f},{gb[1]:.1f}",
               f"Cup glint {r + 1}-{c + 1}", fill=NONE, stroke="#F2C97E",
               strokeWidth=1.5, opacity=80, cap="round")

# side-face grain: two long soft strokes down the lit flank
for i, (gz, ga_) in enumerate([(1.4, 30), (3.2, 20)]):
    pts = smooth([P(XW + 0.04, 7 + i * 1.2, gz - 1.6), P(XW + 0.04, 17, gz),
                  P(XW + 0.04, 27, gz + 0.9), P(XW + 0.04, 38, gz + 0.4)],
                 closed=False)
    d.path(pts, f"Side grain {i + 1}", fill=NONE, stroke="#1E1006",
           strokeWidth=1.6, opacity=ga_)

# case edge sheen up the near front corner
ea, eb = P(XW - 0.35, 7, FRT + 0.1), P(XW - 0.35, 39, FRT + 0.1)
d.path(f"M{ea[0]:.1f},{ea[1]:.1f} L{eb[0]:.1f},{eb[1]:.1f}", "Corner sheen",
       fill=NONE, stroke=OAK_HI, strokeWidth=3.0, opacity=28, cap="round")

# --- tincture bottles on the cornice -----------------------------------------------------
def bottle(name, bx, base_y, w, h, hue):
    """Amber bottle silhouette in plane z=-1: round body, narrow neck, glint."""
    z = -1.0
    cx = bx
    body = smooth([P(cx - w, base_y + 0.4, z), P(cx - w * 1.02, base_y + h * 0.42, z),
                   P(cx - w * 0.8, base_y + h * 0.62, z), P(cx - w * 0.30, base_y + h * 0.66, z),
                   P(cx + w * 0.30, base_y + h * 0.66, z), P(cx + w * 0.8, base_y + h * 0.62, z),
                   P(cx + w * 1.02, base_y + h * 0.42, z), P(cx + w, base_y + 0.4, z)])
    neck = fquad(cx - w * 0.30, base_y + h * 0.66, cx + w * 0.30, base_y + h, z)
    d.path(body, f"{name} body",
           fill=lin((0, P(cx, base_y + h, z)[1]), (0, P(cx, base_y, z)[1]),
                    (0, hue[0], 88), (0.5, hue[1], 80), (1, hue[2], 92)),
           stroke=INK, strokeWidth=1.6, join="round")
    d.path(poly(neck), f"{name} neck",
           fill=lin((0, P(cx, base_y + h, z)[1]), (0, P(cx, base_y + h * 0.6, z)[1]),
                    (0, hue[1], 85), (1, hue[2], 90)),
           stroke=INK, strokeWidth=1.5, join="round")
    # cork
    ck = fquad(cx - w * 0.24, base_y + h, cx + w * 0.24, base_y + h + 0.55, z)
    d.path(poly(ck), f"{name} cork",
           fill=lin((0, ck[0][1]), (0, ck[2][1]), (0, "#C8A060"), (1, "#8A6430")),
           stroke=INK, strokeWidth=1.3)
    # glass glint down the body's left shoulder
    gx, gy = P(cx - w * 0.55, base_y + h * 0.52, z - 0.05)
    d.shape("ellipse", f"{name} glint", x=round(gx - 3), y=round(gy - 7),
            width=6, height=13, fill="#FFE8B0", opacity=55, stroke=NONE)


bottle("Round tincture", -14.5, 43.0, 2.5, 5.2, ("#8A4E12", "#C8822E", "#5E340C"))
bottle("Tall vial", -8.6, 43.0, 1.5, 7.2, ("#6E3E10", "#A96E22", "#4A280A"))

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
               color="#F0E4C4", justify="center")
    m = d.text(mats, "Materials", x=500, y=970, size=22, font="Virelai Sans",
               color="#C8B480", justify="center")
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


caption("APOTHECARY CABINET", "OAK · BRASS · CARD")
d.finish("apothecary-cabinet-V1R00")
