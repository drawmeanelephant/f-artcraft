#!/usr/bin/env python3
"""Deck chair — furniture field plate V1R00. Near-side view with a slight
three-quarter from the front left: the promenade-deck folder — a leaning
teak outer frame (two posts, top rail, bottom rail, notch bar), seat arms
hooked into the frame, short front legs, and a navy/cream striped canvas
sling draped from the top rail to the front bar. Sea-air plate: cool marine
backdrop, horizon line, pale sky glow. 1000x1000.
Gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420. Modelled in 3D (inches), projected
with a fixed yaw + pitch."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Deck Chair — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#221A10"   # warm dark, never black


def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [dict(offset=s[0], color=s[1], **({"opacity": s[2]} if len(s) > 2 else {}))
                      for s in stops]}}


def rad(*stops):
    return {"gradient": {"kind": "radial", "stops": [
        dict(offset=s[0], color=s[1], **({"opacity": s[2]} if len(s) > 2 else {})) for s in stops]}}


def smooth(pts, closed=False, move=True):
    n = len(pts)

    def g(i):
        return pts[i % n] if closed else pts[max(0, min(n - 1, i))]
    s = ("M%.1f,%.1f" if move else "L%.1f,%.1f") % pts[0]
    for i in (range(n) if closed else range(n - 1)):
        p0, p1, p2, p3 = g(i - 1), g(i), g(i + 1), g(i + 2)
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        s += " C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (c1 + c2 + p2)
    return s + (" Z" if closed else "")


def poly(pts):
    return "M%.1f,%.1f " % pts[0] + " ".join("L%.1f,%.1f" % p for p in pts[1:]) + " Z"


# --- projection: x right, y up, z back (inches * S) -----------------------------------
YAW, PITCH = math.radians(34), math.radians(16)
S, OX, OY = 13.6, 505, 776
BOUNDS = []


def P(x, y, z):
    c, s = math.cos(YAW), math.sin(YAW)
    xr, zr = x * c + z * s, -x * s + z * c
    p = (OX + S * xr, OY - S * (y * math.cos(PITCH) + zr * math.sin(PITCH)))
    BOUNDS.append(p)
    return p


TEAK = ((0, "#8A6430"), (0.22, "#D8AE6A"), (0.42, "#A87C40"), (0.62, "#5E421C"),
        (0.8, "#B08A50"), (1, "#6E4C20"))


def bar(name, a, b, r=0.72, grad=TEAK, ink=2.4):
    """Rectangular-ish frame member between 3D points, lit across its width."""
    A, B = P(*a), P(*b)
    dx, dy = B[0] - A[0], B[1] - A[1]
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    nx, ny = -uy, ux
    w = r * S
    pts = []
    for k in range(9):
        t = math.pi * k / 8
        pts.append((B[0] + nx * w * math.cos(t) + ux * w * math.sin(t),
                    B[1] + ny * w * math.cos(t) + uy * w * math.sin(t)))
    for k in range(9):
        t = math.pi * k / 8
        pts.append((A[0] - nx * w * math.cos(t) - ux * w * math.sin(t),
                    A[1] - ny * w * math.cos(t) - uy * w * math.sin(t)))
    mx, my = (A[0] + B[0]) / 2, (A[1] + B[1]) / 2
    if nx > 0:
        nx, ny = -nx, -ny
    g = lin(mx + nx * w, my + ny * w, mx - nx * w, my - ny * w, *grad)
    d.path(poly(pts), name, fill=g, stroke=INK, strokeWidth=ink, join="round")
    assert 2 * w >= 3, "bar must stay >= 3pt"
    return A, B


def endgrain(name, p, r=5):
    x, y = P(*p)
    d.shape("ellipse", name, x=round(x - r), y=round(y - r * 0.8), width=2 * r, height=round(2 * r * 0.8),
            fill=rad((0, "#C89A58"), (1, "#6E4C20")), stroke=INK, strokeWidth=1.6)


def bolt(name, p):
    x, y = P(*p)
    d.shape("ellipse", name, x=round(x - 7), y=round(y - 7), width=14, height=14,
            fill=rad((0, "#FFF0B8"), (0.55, "#D2A24A"), (1, "#7A5418")), stroke=INK, strokeWidth=1.6)
    d.shape("ellipse", f"{name} glint", x=round(x - 3.5), y=round(y - 4.5), width=4.5, height=3.5,
            fill="#FFFFFF", opacity=80, stroke=NONE)


# --- backdrop + plate ------------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin(0, 0, 0, 1000, (0, "#101C22"), (1, "#050A0C")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880, fill="#6A8290", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#46586A"), (0.55, "#2E3C4A"), (1, "#171F28")), stroke="#0A1014", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C4D4DE", strokeWidth=3, opacity=26)
# pale sky glow upper right + sea horizon across the disc
d.shape("ellipse", "Sky glow", x=380, y=60, width=540, height=420,
        fill=rad((0, "#E8F0F4", 0.22), (0.6, "#C8D8E0", 0.07), (1, "#C8D8E0", 0)), stroke=NONE)
HH = 348
hw = math.sqrt(PR ** 2 - (HH - PCY) ** 2)
d.path(f"M{PCX - hw + 6:.1f},{HH} L{PCX + hw - 6:.1f},{HH}", "Horizon",
       fill=NONE, stroke="#9FB4C0", strokeWidth=2, opacity=30)
# a few distant gulls
for i, (gx, gy, gs) in enumerate([(690, 265, 10), (740, 285, 7), (650, 295, 6)]):
    d.path(f"M{gx - gs},{gy} Q{gx - gs * 0.4},{gy - gs * 0.7} {gx},{gy} "
           f"Q{gx + gs * 0.4},{gy - gs * 0.7} {gx + gs},{gy}",
           f"Gull {i+1}", fill=NONE, stroke="#C8D8E0", strokeWidth=2, opacity=40, cap="round")
# floor band closes on the disc's own arc — the promenade deck
FYB = 700
hw = math.sqrt(PR ** 2 - (FYB - PCY) ** 2)
d.path(f"M{PCX + hw:.1f},{FYB} L{PCX - hw:.1f},{FYB} A420,420 0 0 0 {PCX + hw:.1f},{FYB} Z",
       "Deck", fill=lin(0, FYB, 0, 880, (0, "#3A4048", 0), (0.4, "#2A3038", 0.6), (1, "#12161C", 0.85)),
       stroke=NONE)
for i, yb in enumerate([738, 780, 824]):
    h = math.sqrt(PR ** 2 - (yb - PCY) ** 2) - 4
    d.path(f"M{PCX - h:.1f},{yb} L{PCX + h:.1f},{yb}", f"Deck seam {i+1}",
           fill=NONE, stroke="#5A6672", strokeWidth=2, opacity=28)
# plank grooves fan toward the horizon
for i, x0 in enumerate([300, 420, 560, 700]):
    d.path(f"M{x0},878 L{x0 + (x0 - 500) * 0.25:.0f},{FYB + 6}", f"Plank groove {i+1}",
           fill=NONE, stroke="#1E242C", strokeWidth=2, opacity=35)

# --- frame geometry (inches) -------------------------------------------------------------
# side-view members, (z, y): post leans back; arm hooks into a notch; front leg drops ahead
POST = ((15.5, 0.4), (4.5, 40.0))       # rear post, bottom -> top
ARM = ((7.8, 21.6), (19.9, 10.2))       # seat arm, notch -> front bar joint
FLEG = ((20.0, 10.4), (24.0, 0.4))      # front leg
FX = 10.0                                # frame half width
TOPR = (4.5, 40.0)                       # top rail centre
NOTCH = (8.6, 22.4)                      # notch bar centre
BOTR = (15.5, 3.0)                       # bottom rail centre
FBAR = (19.9, 10.6)                      # canvas front bar centre

# shadow under the feet
feet = [P(sx * FX, 0, z) for sx in (-1, 1) for z in (POST[0][0], FLEG[1][0])]
fx0, fx1 = min(p[0] for p in feet) - 30, max(p[0] for p in feet) + 30
fy0, fy1 = min(p[1] for p in feet) - 20, max(p[1] for p in feet) + 22
d.shape("ellipse", "Chair shadow", x=round(fx0), y=round(fy0), width=round(fx1 - fx0),
        height=round(fy1 - fy0),
        fill=rad((0, "#04070A", 0.66), (0.6, "#04070A", 0.30), (1, "#04070A", 0)), stroke=NONE)


def side(a2, b2, sx):
    """(z,y) side-view pair -> 3D endpoints on frame plane x = sx*FX."""
    return (sx * FX, a2[1], a2[0]), (sx * FX, b2[1], b2[0])


def rail(name, zy, r=0.66, grad=TEAK):
    return bar(name, (-FX - 0.5, zy[1], zy[0]), (FX + 0.5, zy[1], zy[0]), r=r, grad=grad)


# far frame + shared rails first
far_post = side(*POST, 1)
far_leg = side(*FLEG, 1)
far_arm = side(*ARM, 1)
bar("Far post", *far_post)
bar("Far front leg", *far_leg, r=0.62)
rail("Bottom rail", BOTR)
rail("Notch bar", NOTCH)
bar("Far seat arm", *far_arm, r=0.62)

# --- canvas sling -------------------------------------------------------------------------
# drape path in the side plane: top rail -> down the back -> seat sag -> front bar -> under
DRAPE = [(4.6, 39.6), (5.4, 33.5), (6.4, 26.5), (7.6, 21.0),
         (10.5, 14.5), (13.5, 11.0), (16.5, 10.2), (19.0, 10.9),
         (19.9, 11.0), (19.7, 9.6)]
NU = 34


def drape(u):
    """Sample the canvas centreline in (z, y) via Catmull-Rom on DRAPE."""
    n = len(DRAPE)
    f = u * (n - 1)
    i = min(n - 2, int(f))
    t = f - i
    p0, p1, p2, p3 = DRAPE[max(0, i - 1)], DRAPE[i], DRAPE[i + 1], DRAPE[min(n - 1, i + 2)]
    z = 0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * t + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t * t +
               (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t ** 3)
    y = 0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * t + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t * t +
               (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t ** 3)
    return z, y


def sling(u, xf):
    z, y = drape(u)
    sn = math.sin(math.pi * u)
    xe = 9.55 - 0.55 * sn            # hems pull inward under load
    return (xf * xe, y + 0.5 * sn * (1 - xf * xf), z)


US = [i / NU for i in range(NU + 1)]
CREAM, NAVY = "#EDE2C4", "#2E4A66"
NB = 9
bounds_xf = [-1 + 2 * j / NB for j in range(NB + 1)]

# canvas drawn stripe by stripe so the stripes follow the drape over the seat
for j in range(NB):
    xl, xr = bounds_xf[j], bounds_xf[j + 1]
    pts = [P(*sling(u, xl)) for u in US] + [P(*sling(u, xr)) for u in US[::-1]]
    col = NAVY if j % 2 else CREAM
    d.path(poly(pts), f"Canvas stripe {j+1}", fill=col, stroke=NONE)

# canvas outline in ink over the stripes: one closed loop, no cross-lines
edge_l = [P(*sling(u, -1)) for u in US]
edge_r = [P(*sling(u, 1)) for u in US]
top_e = [P(*sling(0, xf)) for xf in bounds_xf]
bot_e = [P(*sling(1, xf)) for xf in bounds_xf]
loop = edge_l + bot_e[1:] + edge_r[::-1][1:] + top_e[::-1][1:]
d.path(poly(loop), "Canvas outline", fill=NONE, stroke=INK, strokeWidth=3, join="round")

# shading: the seat dip darkens, the back face catches the sky
shade = [P(*sling(u, -0.94)) for u in US if 0.30 <= u <= 0.78] + \
        [P(*sling(u, 0.94)) for u in US if 0.30 <= u <= 0.78][::-1]
d.path(poly(shade), "Seat dip shade", fill="#14202C", opacity=26, stroke=NONE)
sheen = [P(*sling(u, -0.7)) for u in US if 0.04 <= u <= 0.30] + \
        [P(*sling(u, 0.55)) for u in US if 0.04 <= u <= 0.30][::-1]
d.path(poly(sheen), "Back sheen", fill="#FFFFFF", opacity=12, stroke=NONE)
# tension creases from the bar corners
for side_, nm in ((-1, "L"), (1, "R")):
    cr = [P(*sling(u, side_ * (0.94 - 0.55 * (u - 0.78)))) for u in [0.78 + 0.02 * k for k in range(9)]]
    d.path(smooth(cr), f"Crease {nm}", fill=NONE, stroke="#14181E", strokeWidth=2.5,
           opacity=30, cap="round")
# top hem seam where the canvas loops the top rail
seam = [P(*sling(0.015, xf * 0.97)) for xf in [-1 + 2 * k / 16 for k in range(17)]]
d.path(smooth(seam), "Top hem", fill=NONE, stroke="#14181E", strokeWidth=2, opacity=45)
d.path(smooth([(x, y + 3) for x, y in seam]), "Top hem stitch", fill=NONE,
       stroke="#F4ECD8", strokeWidth=1.6, opacity=70, dash=[5, 4], cap="round")

# canvas wrapped round the front bar: a fatter capsule over the rail end
w_ = (0.7 + 0.18) * S
a, b = bar("Front bar wrap", (-9.9, FBAR[1], FBAR[0]), (9.9, FBAR[1], FBAR[0]),
           r=0.88, ink=2.4,
           grad=((0, "#5A5E66"), (0.3, "#D8D2BC"), (0.6, "#8A8E96"), (1, "#3E4248")))
d.path(f"M{a[0]:.1f},{a[1] - w_ * 0.35:.1f} L{b[0]:.1f},{b[1] - w_ * 0.35:.1f}",
       "Front wrap sheen", fill=NONE, stroke="#F4ECD8", strokeWidth=2.2, opacity=45, cap="round")
# stripes continue over the wrap: a narrow band of each colour across the bar
for j in range(NB):
    xm = (bounds_xf[j] + bounds_xf[j + 1]) / 2 * 9.55
    t0 = P(xm, FBAR[1] + 0.72, FBAR[0] - 0.1)
    t1 = P(xm, FBAR[1] - 0.45, FBAR[0] + 0.75)
    d.path("M%.1f,%.1f L%.1f,%.1f" % (t0 + t1), f"Wrap stripe {j+1}", fill=NONE,
           stroke=(NAVY if j % 2 else CREAM), strokeWidth=20, opacity=90, cap="butt")

# --- near frame over the canvas edges ------------------------------------------------------
near_arm = side(*ARM, -1)
bar("Near seat arm", *near_arm, r=0.62)
rail("Top rail", TOPR)
near_post = side(*POST, -1)
bar("Near post", *near_post)
near_leg = side(*FLEG, -1)
bar("Near front leg", *near_leg, r=0.62)
# bolts: arm pivot at the notch, front-leg joint at the bar
bolt("Near notch bolt", (-FX - 0.3, NOTCH[1], NOTCH[0]))
bolt("Far notch bolt", (FX + 0.3, NOTCH[1], NOTCH[0]))
bolt("Near leg bolt", (-FX - 0.3, FLEG[0][1], FLEG[0][0]))
# end grain on cut ends: post tops + feet
endgrain("Top cap L", (-FX, POST[1][1] + 0.3, POST[1][0]))
endgrain("Top cap R", (FX, POST[1][1] + 0.3, POST[1][0]))
for sx in (-1, 1):
    for z in (POST[0][0], FLEG[1][0]):
        x, y = P(sx * FX, 0, z)
        d.shape("ellipse", f"Foot pad {sx},{z}", x=round(x - 13), y=round(y - 3), width=26, height=9,
                fill=rad((0, "#000000", 0.5), (1, "#000000", 0)), stroke=NONE)

# --- extent check --------------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in BOUNDS)
print("chair extent: farthest point %.0f from centre (rim %d)" % (far, PR))
assert far < PR - 20, far

# --- captions --------------------------------------------------------------------------------
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
               color="#E8F0F2", justify="center")
    m = d.text(mats, "Materials", x=500, y=970, size=22, font="Virelai Sans",
               color="#A8BCC6", justify="center")
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


caption("DECK CHAIR", "TEAK · CANVAS · BRASS")
d.finish("deck-chair-V1R00")
