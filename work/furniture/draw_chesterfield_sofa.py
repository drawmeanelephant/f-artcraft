#!/usr/bin/env python3
"""Chesterfield sofa — furniture field plate V1R00. Three-quarter from the
front left: arms level with the back, rolled arm scrolls with pleated fans and
brass nailheads, deep diamond buttoning on the inside back, inside arms and
outer arm, three seat cushions, short turned mahogany legs. Oxblood leather
catching a single warm light against a dark plate. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420. The sofa is modelled in 3D and drawn
with a rotated orthographic projection (affine, so Bezier control points
project exactly)."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Chesterfield Sofa — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#24100C"   # warm umber, never black

def stops(*ss):
    return [dict(offset=o, color=c, **({"opacity": a} if a is not None else {})) for o, c, a in ss]

def lin(x0, y0, x1, y1, *ss):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1], "stops": stops(*ss)}}

def rad(*ss):
    return {"gradient": {"kind": "radial", "stops": stops(*ss)}}

# --- sofa geometry (pt): x right, y up, z back ------------------------------------------
XO, XI = 300, 230            # outer side, inside-arm face
YB, YS, YC = 46, 136, 182    # base bottom, deck, cushion top
YT = 300                     # arm / back height (level)
ZI, ZB = 214, 280            # inside-back face, back of the sofa

CX, FY, SC = 538, 712, 0.93
TH, PH = math.radians(24), math.radians(20)
RO, RC = 26, 32            # arm roll overhang and crown rise
CT, ST, CP, SP = math.cos(TH), math.sin(TH), math.cos(PH), math.sin(PH)
BOUNDS = []

def P(x, y, z):
    depth = x * ST + z * CT
    return (CX + SC * (x * CT - z * ST), FY - SC * (y * CP + depth * SP))

def path3(ops, track=True):
    out = []
    for op in ops:
        xy = [P(*p) for p in op[1:]]
        if track:
            BOUNDS.extend(xy)
        out.append(op[0] + " ".join("%.1f,%.1f" % q for q in xy))
    return " ".join(out)

def px(x, ops):   # (z, y) in the plane x = const
    return [(op[0],) + tuple((x, v, u) for u, v in op[1:]) for op in ops]

def pz(z, ops):   # (x, y) in the plane z = const
    return [(op[0],) + tuple((u, v, z) for u, v in op[1:]) for op in ops]

def rect_ops(u0, v0, u1, v1):
    return [("M", (u0, v0)), ("L", (u1, v0)), ("L", (u1, v1)), ("L", (u0, v1)), ("Z",)]

def bez(p0, p1, p2, p3, t):
    u = 1 - t
    return tuple(u*u*u*a + 3*u*u*t*b + 3*u*t*t*c + t*t*t*e for a, b, c, e in zip(p0, p1, p2, p3))

# --- palette --------------------------------------------------------------------------------
BG_GRAD = lin(0, 0, 0, 1000, (0, "#151716", None), (1, "#060707", None))
PLATE_GRAD = rad((0, "#3C423C", None), (0.6, "#262A26", None), (1, "#121412", None))
FLOOR_GRAD = lin(0, 690, 0, 880, (0, "#0C0A08", 0), (0.4, "#0C0A08", 0.45), (1, "#050403", 0.85))
LAMP = rad((0, "#FFC890", 0.26), (0.5, "#FFB070", 0.07), (1, "#FFB070", 0))

L_TOP = lin(0, 180, 0, 420, (0, "#C25A4C", None), (1, "#7A2026", None))
L_FRONT = lin(0, 560, 0, 760, (0, "#8C2A2C", None), (1, "#4A1014", None))
L_SIDE = lin(140, 0, 400, 0, (0, "#3E0C10", None), (1, "#6A1C20", None))
L_CUSH = lin(0, 470, 0, 600, (0, "#7A2226", None), (1, "#B0463E", None))
L_CUSH_F = lin(0, 580, 0, 660, (0, "#9A3432", None), (1, "#541216", None))
MAHOG = lin(0, 690, 0, 780, (0, "#8A4A2C", None), (0.5, "#5A2A16", None), (1, "#2E140A", None))
BRASS = rad((0, "#FFF0B0", None), (0.5, "#D8A848", None), (1, "#7A5418", None))
SPEC = "#FFD2A8"

# --- backdrop, plate, light, floor -----------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880, fill="#4A524A", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840, fill=PLATE_GRAD, stroke="#0A0B0A", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C8B89A", strokeWidth=3, opacity=22)
d.shape("ellipse", "Warm light", x=150, y=170, width=560, height=560, fill=LAMP, stroke=NONE)
FYB = 650
hw = math.sqrt(PR ** 2 - (FYB - PCY) ** 2)
d.path(f"M{PCX + hw:.1f},{FYB} L{PCX - hw:.1f},{FYB} A420,420 0 0 0 {PCX + hw:.1f},{FYB} Z",
       "Floor", fill=FLOOR_GRAD, stroke=NONE)
for i, yb in enumerate([712, 762, 818]):
    h = math.sqrt(PR ** 2 - (yb - PCY) ** 2) - 4
    d.path(f"M{PCX - h:.1f},{yb} L{PCX + h:.1f},{yb}", f"Floor seam {i+1}",
           fill=NONE, stroke="#3A3530", strokeWidth=2, opacity=40)

sx, sy = P(0, 0, 140)
d.shape("ellipse", "Floor shadow", x=round(sx - 330), y=round(sy - 46), width=660, height=96,
        fill=rad((0, "#030202", 0.8), (0.7, "#030202", 0.4), (1, "#030202", 0)), stroke=NONE)

# --- legs -------------------------------------------------------------------------------------
def leg(label, x, z):
    tx, ty = P(x, YB, z)
    bx, by = P(x, 0, z)
    h = by - ty
    w = 13 * SC / 0.86
    dpath = ("M%.1f,%.1f L%.1f,%.1f L%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f "
             "C%.1f,%.1f %.1f,%.1f %.1f,%.1f L%.1f,%.1f L%.1f,%.1f L%.1f,%.1f "
             "C%.1f,%.1f %.1f,%.1f %.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f L%.1f,%.1f Z") % (
        tx - w, ty, tx + w, ty, tx + w * 0.8, ty + h * 0.18,
        tx + w * 1.5, ty + h * 0.26, tx + w * 1.5, ty + h * 0.62, tx + w * 0.7, ty + h * 0.72,
        bx + w * 0.4, by - h * 0.22, bx + w * 0.5, by - h * 0.12, bx + w * 0.55, by - h * 0.08,
        bx + w * 0.55, by, bx - w * 0.55, by, bx - w * 0.55, by - h * 0.08,
        bx - w * 0.5, by - h * 0.12, bx - w * 0.4, by - h * 0.22, tx - w * 0.7, ty + h * 0.72,
        tx - w * 1.5, ty + h * 0.62, tx - w * 1.5, ty + h * 0.26, tx - w * 0.8, ty + h * 0.18,
        tx - w, ty)
    BOUNDS.extend([(tx - w * 1.5, ty), (bx + w * 1.5, by)])
    d.path(dpath, label, fill=MAHOG, stroke=INK, strokeWidth=3, join="round")
    d.path("M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (
        tx - w * 0.9, ty + h * 0.3, tx - w * 1.2, ty + h * 0.42, tx - w * 1.0, ty + h * 0.58, tx - w * 0.6, ty + h * 0.66),
        label + " gloss", fill=NONE, stroke="#F2B488", strokeWidth=3, opacity=55, cap="round")
    d.shape("ellipse", label + " castor", x=round(bx - w * 0.6), y=round(by - 4), width=round(w * 1.2), height=7,
            fill=BRASS, stroke=INK, strokeWidth=1.5)

leg("Leg back right", XO - 22, ZB - 22)
leg("Leg back left", -XO + 22, ZB - 22)

# --- deep buttoning --------------------------------------------------------------------------
def tuft(label, M, u0, u1, v0, v1, nu, nv, lite, mid, dark, crease="#2A0608", button=None, margin=0):
    """Diamond tufting in a plane. M(u, v) -> (x, y, z). Buttons sit on the
    lattice points with i+j even; diamonds are centred on the odd ones and
    clamped to the panel so the edges get half-diamonds."""
    du, dv = (u1 - u0) / nu, (v1 - v0) / nv
    cl = lambda u, v: (min(u1, max(u0, u)), min(v1, max(v0, v)))
    k = 0
    for j in range(nv + 1):
        for i in range(nu + 1):
            if (i + j) % 2 == 0:
                continue
            u, v = u0 + i * du, v0 + j * dv
            T, Rr, B, L = cl(u, v + dv), cl(u + du, v), cl(u, v - dv), cl(u - du, v)
            pts = [T, Rr, B, L]
            cu, cv = sum(p[0] for p in pts) / 4, sum(p[1] for p in pts) / 4
            ops = [("M", M(*T))]
            for a, b in ((T, Rr), (Rr, B), (B, L), (L, T)):
                mu, mv = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
                c = cl(mu + (mu - cu) * 0.22, mv + (mv - cv) * 0.22)
                ops.append(("Q", M(*c), M(*b)))
            ops.append(("Z",))
            k += 1
            d.path(path3(ops, track=False), f"{label} diamond {k}",
                   fill=rad((0, lite, None), (0.62, mid, None), (1, dark, None)),
                   stroke=crease, strokeWidth=2.5, join="round")
    k = 0
    for j in range(1, nv):
        for i in range(1, nu):
            if (i + j) % 2:
                continue
            x, y = P(*M(u0 + i * du, v0 + j * dv))
            k += 1
            d.shape("ellipse", f"{label} dimple {k}", x=round(x - 6), y=round(y - 5), width=12, height=10,
                    fill="#1A0405", opacity=55, stroke=NONE)
            d.shape("ellipse", f"{label} button {k}", x=round(x - 3.5), y=round(y - 3.5), width=7, height=7,
                    fill=button or rad((0, "#C0504A", None), (1, "#4A0E10", None)), stroke=INK, strokeWidth=1)

# --- back top roll -------------------------------------------------------------------------
back_top = [("M", (-XI, YT - 2, ZI - 6)), ("C", (-XI, YT + 16, ZI - 6), (-XI, YT + 16, ZI + 30), (-XI, YT + 12, ZI + 40)),
            ("L", (-XI, YT + 4, ZB)), ("L", (XI, YT + 4, ZB)), ("L", (XI, YT + 12, ZI + 40)),
            ("C", (XI, YT + 16, ZI + 30), (XI, YT + 16, ZI - 6), (XI, YT - 2, ZI - 6)), ("Z",)]
d.path(path3(back_top), "Back top roll", fill=L_TOP, stroke=INK, strokeWidth=4)
d.path(path3([("M", (-XI + 10, YT + 14, ZI + 14)), ("L", (XI - 10, YT + 14, ZI + 14))]),
       "Back roll highlight", fill=NONE, stroke=SPEC, strokeWidth=5, opacity=40, cap="round")

# --- inside back --------------------------------------------------------------------------------
d.path(path3(pz(ZI, rect_ops(-XI, YC - 6, XI, YT))), "Inside back", fill=L_FRONT, stroke=INK, strokeWidth=4)
tuft("Back", lambda u, v: (u, v, ZI), -XI, XI, YC - 6, YT - 4, 10, 4, "#C4564C", "#8A2A2C", "#4E1216")
d.path(path3(pz(ZI, [("M", (-XI, YT - 4)), ("L", (XI, YT - 4)), ("L", (XI, YT - 22)), ("L", (-XI, YT - 22)), ("Z",)])),
       "Back roll underside shade", fill="#1A0405", opacity=30, stroke=NONE)

# --- right arm: inside face then the roll ---------------------------------------------------
d.path(path3(px(XI, rect_ops(0, YC - 6, ZI, YT - 2))), "Right inside arm", fill=L_SIDE, stroke=INK, strokeWidth=4)
tuft("Right inside arm", lambda u, v: (XI, v, u), 0, ZI, YC - 6, YT - 6, 5, 4,
     "#A84440", "#6E1E22", "#3A0A0E")
d.path(path3(px(XI, rect_ops(0, YC - 6, ZI, YC + 20))), "Right inside arm seat shade",
       fill="#140304", opacity=30, stroke=NONE)

def arm_top(xi, label):
    s = 1 if xi > 0 else -1
    xo = s * XO
    ov = xo + s * RO
    def prof(z):
        return [(xi, YT - 4, z), (xi, YT + 18, z), (xi + s * 22, YT + RC, z), (xi + s * 50, YT + RC, z),
                (xi + s * 80, YT + RC, z), (ov, YT + 18, z), (ov, YT - 2, z)]
    f, b = prof(0), prof(ZB)
    ops = [("M", f[0]), ("C", f[1], f[2], f[3]), ("C", f[4], f[5], f[6]), ("L", b[6]),
           ("C", b[5], b[4], b[3]), ("C", b[2], b[1], b[0]), ("Z",)]
    d.path(path3(ops), label, fill=L_TOP, stroke=INK, strokeWidth=4)
    d.path(path3([("M", (xi + s * 46, YT + RC, 6)), ("L", (xi + s * 46, YT + RC, ZB - 10))]),
           label + " highlight", fill=NONE, stroke=SPEC, strokeWidth=7, opacity=42, cap="round")
    d.path(path3([("M", (xi + s * 40, YT + RC, 20)), ("L", (xi + s * 40, YT + RC, 120))]),
           label + " hot spot", fill=NONE, stroke="#FFF0DC", strokeWidth=3, opacity=60, cap="round")

arm_top(XI, "Right arm top")

# --- seat cushions -------------------------------------------------------------------------------
cw = 2 * XI / 3
for i in range(3):
    x0, x1 = -XI + i * cw, -XI + (i + 1) * cw
    top = [("M", (x0 + 2, YC, 2)), ("C", (x0 + cw * 0.3, YC + 6, 0), (x1 - cw * 0.3, YC + 6, 0), (x1 - 2, YC, 2)),
           ("L", (x1 - 2, YC, ZI)), ("L", (x0 + 2, YC, ZI)), ("Z",)]
    d.path(path3(top), f"Cushion {i+1} top", fill=L_CUSH, stroke=INK, strokeWidth=3.5)
    d.path(path3([("M", (x0 + 24, YC + 3, 60)), ("C", (x0 + cw * 0.4, YC + 5, 40), (x1 - cw * 0.4, YC + 5, 40), (x1 - 24, YC + 3, 60))]),
           f"Cushion {i+1} sheen", fill=NONE, stroke=SPEC, strokeWidth=8, opacity=22, cap="round")
    d.path(path3([("M", (x0 + 2, YC, ZI)), ("L", (x1 - 2, YC, ZI)), ("L", (x1 - 2, YC, ZI - 60)),
                  ("C", (x1 - cw * 0.3, YC, ZI - 40), (x0 + cw * 0.3, YC, ZI - 40), (x0 + 2, YC, ZI - 56)), ("Z",)]),
           f"Cushion {i+1} back shade", fill="#160304", opacity=32, stroke=NONE)
for i in range(3):
    x0, x1 = -XI + i * cw, -XI + (i + 1) * cw
    fr = [("M", (x0 + 2, YS + 2)), ("C", (x0 - 2, YC - 14), (x0, YC + 2), (x0 + 14, YC + 2)),
          ("C", (x0 + cw * 0.35, YC + 7), (x1 - cw * 0.35, YC + 7), (x1 - 14, YC + 2)),
          ("C", (x1, YC + 2), (x1 + 2, YC - 14), (x1 - 2, YS + 2)), ("Z",)]
    d.path(path3(pz(0, fr)), f"Cushion {i+1} front", fill=L_CUSH_F, stroke=INK, strokeWidth=3.5)
    d.path(path3(pz(0, [("M", (x0 + 14, YC - 2)), ("C", (x0 + cw * 0.35, YC + 3), (x1 - cw * 0.35, YC + 3), (x1 - 14, YC - 2))])),
           f"Cushion {i+1} welt", fill=NONE, stroke="#D86A58", strokeWidth=3, opacity=55, cap="round")

# --- left arm: outer face (buttoned), roll -----------------------------------------------------
d.path(path3(px(-XO, rect_ops(0, YB, ZB, YT - 2))), "Left outer arm", fill=L_SIDE, stroke=INK, strokeWidth=4)
tuft("Left outer arm", lambda u, v: (-XO, v, u), 0, ZB, YS + 20, YT - 6, 6, 3,
     "#8E3434", "#5E1A1E", "#300A0C")
d.path(path3(px(-XO, rect_ops(0, YB, ZB, YS + 20))), "Left outer arm base",
       fill=lin(140, 0, 380, 0, (0, "#3A0C10", None), (1, "#5E181C", None)), stroke=INK, strokeWidth=3)
d.path(path3(px(-XO, [("M", (6, YS + 18)), ("L", (ZB - 6, YS + 18))])), "Left outer welt",
       fill=NONE, stroke="#B04A44", strokeWidth=3, opacity=45, cap="round")
d.path(path3(px(-XO, rect_ops(0, YB, ZB, YB + 26))), "Left outer arm floor shade",
       fill="#0A0203", opacity=35, stroke=NONE)
d.path(path3(px(-XO, rect_ops(0, YT - 30, ZB, YT - 2)), track=False), "Left roll shadow",
       fill="#140304", opacity=38, stroke=NONE)
arm_top(-XI, "Left arm top")

# --- front rail -------------------------------------------------------------------------------------
d.path(path3(pz(0, rect_ops(-XI, YB, XI, YS))), "Front rail", fill=L_FRONT, stroke=INK, strokeWidth=4)
d.path(path3(pz(0, rect_ops(-XI, YB, XI, YB + 24))), "Front rail shade", fill="#140304", opacity=30, stroke=NONE)
n = 34
for i in range(n + 1):
    x, y = P(-XI + 8 + i * (2 * XI - 16) / n, YS - 10, 0)
    d.shape("ellipse", f"Rail nail {i+1}", x=round(x - 3.2, 1), y=round(y - 3.2, 1), width=6.4, height=6.4,
            fill=BRASS, stroke=INK, strokeWidth=1)

# --- arm fronts: scroll, pleat fan, nailheads ---------------------------------------------
def arm_front(xi, label, lit):
    s = 1 if xi > 0 else -1
    xo, ov = s * XO, s * (XO + RO)
    segs = [((xi, YT - 4), (xi, YT + 18), (xi + s * 22, YT + RC), (xi + s * 50, YT + RC)),
            ((xi + s * 50, YT + RC), (xi + s * 80, YT + RC), (ov, YT + 18), (ov, YT - 2)),
            ((ov, YT - 2), (ov, YT - 22), (xo + s * 8, YT - 30), (xo, YT - 32))]
    ops = [("M", (xi, YB)), ("L", segs[0][0])]
    for a, b, c, e in segs:
        ops.append(("C", b, c, e))
    ops += [("L", (xo, YB)), ("Z",)]
    d.path(path3(pz(0, ops)), label, fill=lit, stroke=INK, strokeWidth=4)
    # pleat fan radiating from the scroll's eye
    eye = (xi + s * 48, YT - 2)
    d.shape("ellipse", label + " eye shade", x=round(P(eye[0], eye[1], 0)[0] - 16), y=round(P(eye[0], eye[1], 0)[1] - 12),
            width=32, height=24, fill="#1A0405", opacity=40, stroke=NONE)
    for k in range(9):
        t = k / 8
        a, b, c, e = segs[0] if t < 0.5 else segs[1]
        q = bez(a, b, c, e, (t * 2) % 1.0 if t < 1 else 1.0)
        ex, ey = eye
        qx, qy = ex + (q[0] - ex) * 0.86, ey + (q[1] - ey) * 0.86
        d.path(path3(pz(0, [("M", (ex + (q[0] - ex) * 0.25, ey + (q[1] - ey) * 0.25)), ("L", (qx, qy))]), track=False),
               f"{label} pleat {k+1}", fill=NONE, stroke="#2A0608", strokeWidth=2.5, opacity=65, cap="round")
    d.shape("ellipse", label + " eye", x=round(P(eye[0], eye[1], 0)[0] - 5), y=round(P(eye[0], eye[1], 0)[1] - 5),
            width=10, height=10, fill=rad((0, "#B04A44", None), (1, "#3A0A0C", None)), stroke=INK, strokeWidth=1.5)
    # vertical panel seam under the scroll
    d.path(path3(pz(0, [("M", (xi + s * 4, YT - 30)), ("L", (xi + s * 4, YB + 6))]), track=False),
           label + " seam", fill=NONE, stroke="#2A0608", strokeWidth=3, opacity=45, cap="round")
    d.path(path3(pz(0, rect_ops(xi, YB, xo, YB + 26)), track=False), label + " floor shade",
           fill="#0A0203", opacity=32, stroke=NONE)
    # brass nailheads tracing the scroll and down both edges
    pts = []
    for a, b, c, e in segs:
        for k in range(8):
            pts.append(bez(a, b, c, e, k / 8))
    for k in range(10):
        pts.append((xo - s * 6, YT - 30 - k * (YT - 30 - YB - 12) / 9))
        pts.append((xi + s * 8, YT - 30 - k * (YT - 30 - YB - 12) / 9))
    for k, (u, v) in enumerate(pts):
        # pull the nails a few points inside the scroll outline
        ex, ey = eye
        if v > YT - 32:
            ln = math.hypot(u - ex, v - ey) or 1
            u, v = u - (u - ex) / ln * 7, v - (v - ey) / ln * 7
        x, y = P(u, v, 0)
        d.shape("ellipse", f"{label} nail {k+1}", x=round(x - 3.2, 1), y=round(y - 3.2, 1), width=6.4, height=6.4,
                fill=BRASS, stroke=INK, strokeWidth=1)

arm_front(XI, "Right arm front", L_FRONT)
arm_front(-XI, "Left arm front", L_FRONT)

leg("Leg front right", XO - 22, 22)
leg("Leg front left", -XO + 22, 22)

# --- sanity: the whole sofa inside the disc --------------------------------------------------------
worst = min(PR - math.hypot(x - PCX, y - PCY) for x, y in BOUNDS)
xs, ys = [b[0] for b in BOUNDS], [b[1] for b in BOUNDS]
print("bounds x %.0f..%.0f y %.0f..%.0f" % (min(xs), max(xs), min(ys), max(ys)))
print("min clearance to rim: %.1f" % worst)
assert worst > 20, worst

# --- captions ----------------------------------------------------------------------------------------
def caption(txt, label, y, size, color, tracking=0):
    r = d.text(txt, label, x=500, y=y, size=size, font="Virelai Sans", color=color, justify="center")
    tid = (r or {}).get("id")
    if tracking and tid is not None:
        d.cmd("text.setStyle", f"{label} tracking", ids=[tid], tracking=tracking)
    return r

caption("CHESTERFIELD SOFA", "Name", 930, 56, "#F2DCCA")
caption("MAHOGANY · LEATHER · BRASS", "Materials", 968, 22, "#C89A84", tracking=260)

d.finish("chesterfield-sofa-V1R00")
