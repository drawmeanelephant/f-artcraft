#!/usr/bin/env python3
"""Nautilus — field-guide plate V1R00. Side profile of the chambered nautilus:
an involute shell whose outline is a true logarithmic spiral (whorl expansion
x3 per turn, the measured Nautilus pompilius rate), russet flame stripes on
cream that fade out toward the aperture, hood, pinhole eye and a fan of
tentacles peeking from the coil. A faint cutaway diagram of the same spiral
shows the septa and siphuncle. Dark abyss backdrop. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Nautilus — Field Plate", 1000, 1000)

INK = "#3A2418"   # warm umber, not black
BG_GRAD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000], "stops": [
    {"offset": 0, "color": "#0A1420"}, {"offset": 1, "color": "#02050A"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#2C5674"}, {"offset": 0.6, "color": "#173650"},
    {"offset": 1, "color": "#0B1C2E"}]}}
SHELL_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#FFF8EA"}, {"offset": 0.6, "color": "#F2E2C4"},
    {"offset": 1, "color": "#D2B48E"}]}}
STRIPE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#8A3A1A"}, {"offset": 1, "color": "#C2602E"}]}}
HOOD_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E8C9A4"}, {"offset": 0.6, "color": "#B98458"},
    {"offset": 1, "color": "#7A4A2C"}]}}
TENT_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F4D8C0"}, {"offset": 1, "color": "#C99474"}]}}
FUNNEL_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E2B898"}, {"offset": 1, "color": "#A8704E"}]}}
EYE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#3A3440"}, {"offset": 1, "color": "#0E0C12"}]}}
RAY_GRAD = {"gradient": {"kind": "linear", "start": [0, 80], "end": [0, 640], "stops": [
    {"offset": 0, "color": "#BFE0F2", "opacity": 0}, {"offset": 0.18, "color": "#BFE0F2", "opacity": 0.16},
    {"offset": 1, "color": "#BFE0F2", "opacity": 0}]}}

PCX, PCY, PR = 500, 460, 420

def on_disc(x, y, pad):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

# --- the log spiral -------------------------------------------------------------
# r(th) = R * exp(B*(th - TH_END)); one full turn multiplies r by W = 3.
W = 3.0
B = math.log(W) / (2 * math.pi)

class Spiral:
    def __init__(self, cx, cy, R, th_end):
        self.cx, self.cy, self.R, self.te = cx, cy, R, th_end

    def r(self, th):
        return self.R * math.exp(B * (th - self.te))

    def pt(self, th, rf=1.0):
        r = self.r(th) * rf
        return (self.cx + r * math.cos(th), self.cy + r * math.sin(th))

    def tan(self, th, rf=1.0):
        r = self.r(th) * rf
        return (r * (B * math.cos(th) - math.sin(th)), r * (B * math.sin(th) + math.cos(th)))

    def edge(self, th):
        """Outline radius in direction th (the last whorl covers everything)."""
        while th >= self.te: th -= 2 * math.pi
        while th < self.te - 2 * math.pi: th += 2 * math.pi
        return self.r(th)

    def curve(self, th0, th1, rf=1.0, seg_per_turn=24, move=True):
        """Exact-tangent cubic Beziers along the spiral from th0 to th1."""
        n = max(1, int(math.ceil(abs(th1 - th0) / (2 * math.pi) * seg_per_turn)))
        h = (th1 - th0) / n
        x, y = self.pt(th0, rf)
        s = ("M%.1f,%.1f" % (x, y)) if move else ("L%.1f,%.1f" % (x, y))
        for k in range(n):
            a, b = th0 + k * h, th0 + (k + 1) * h
            p0, p1 = self.pt(a, rf), self.pt(b, rf)
            t0, t1 = self.tan(a, rf), self.tan(b, rf)
            c1 = (p0[0] + t0[0] * h / 3, p0[1] + t0[1] * h / 3)
            c2 = (p1[0] - t1[0] * h / 3, p1[1] - t1[1] * h / 3)
            s += " C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (c1 + c2 + p1)
        return s

TE = math.radians(100)
SH = Spiral(560, 352, 330, TE)
DORSAL = SH.pt(TE - 2 * math.pi)     # aperture's inner corner, against the coil
VENTRAL = SH.pt(TE)                 # aperture's outer corner
ax, ay = (DORSAL[0] + VENTRAL[0]) / 2 - 26, (DORSAL[1] + VENTRAL[1]) / 2
APERTURE = "Q%.1f,%.1f %.1f,%.1f" % (ax, ay, DORSAL[0], DORSAL[1])
SHELL = SH.curve(TE - 2 * math.pi, TE) + " " + APERTURE + " Z"

# --- backdrop + plate -------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#2C5674", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#0A1826", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#9CC4DA", strokeWidth=3, opacity=35)
# light falling from the surface (tops start inside the rim, then fade out)
for i, (x0, x1, x2, x3) in enumerate([(380, 420, 520, 400), (470, 500, 640, 560), (560, 584, 760, 690)]):
    assert on_disc(x0, 80, 6) and on_disc(x1, 80, 6)
    d.path(f"M{x0},80 L{x1},80 L{x2},640 L{x3},640 Z", f"Light ray {i+1}",
           fill=RAY_GRAD, stroke=NONE)
for i, (x, y, w) in enumerate([(180,330,6),(820,300,5),(160,520,7),(850,500,6),(240,720,5),(760,740,7),
                               (140,420,5),(870,600,5),(420,100,5),(620,110,6),(300,140,4),(700,180,5),
                               (330,820,5),(660,820,4),(120,600,4),(880,380,4),(520,860,4),(210,640,4),
                               (790,660,5),(450,780,4)]):
    assert on_disc(x, y, 10), (x, y)
    d.shape("ellipse", f"Marine snow {i+1}", x=x, y=y, width=w, height=w,
            fill="#E8F2F8", opacity=45, stroke=NONE)

# --- field-guide inset: cutaway of the same spiral, septa + siphuncle -------------
IN = Spiral(262, 222, 92, math.radians(60))
in_te = IN.te
# whorl walls, five turns inward
walls = IN.curve(in_te - 5 * 2 * math.pi, in_te, seg_per_turn=20)
d.path(walls, "Inset whorl wall", fill=NONE, stroke="#CFE4F0", strokeWidth=2.5, opacity=45, cap="round")
d.path("M%.1f,%.1f L%.1f,%.1f" % (IN.pt(in_te) + IN.pt(in_te - 2 * math.pi)),
       "Inset aperture", fill=NONE, stroke="#CFE4F0", strokeWidth=2.5, opacity=45, cap="round")
# body chamber is the last ~third of a turn; septa every 1/11 turn behind it
step = 2 * math.pi / 11
th = in_te - 0.75 * math.pi
k = 0
while th > in_te - 4.4 * 2 * math.pi:
    o = IN.pt(th); i_ = IN.pt(th - 2 * math.pi)
    mx, my = (o[0] + i_[0]) / 2, (o[1] + i_[1]) / 2
    tx, ty = IN.tan(th)
    ln = math.hypot(tx, ty) or 1
    bow = 0.28 * math.hypot(o[0] - i_[0], o[1] - i_[1])
    cx, cy = mx - tx / ln * bow, my - ty / ln * bow    # concave toward the aperture
    k += 1
    d.path("M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" % (o[0], o[1], cx, cy, i_[0], i_[1]),
           f"Inset septum {k}", fill=NONE, stroke="#CFE4F0", strokeWidth=1.6,
           opacity=38, cap="round")
    th -= step
# siphuncle threading the chambers
d.path(IN.curve(in_te - 4.2 * 2 * math.pi, in_te - 0.75 * math.pi, rf=0.62),
       "Inset siphuncle", fill=NONE, stroke="#F2B48A", strokeWidth=2, opacity=40, cap="round")
d.path(IN.curve(in_te - 2 * math.pi, in_te) + " L%.1f,%.1f " % IN.pt(in_te - 2 * math.pi) + "Z",
       "Inset body chamber", fill="#CFE4F0", opacity=8, stroke=NONE)
for x, y in [IN.pt(a) for a in (in_te, in_te - 1.0 * math.pi)]:
    assert on_disc(x, y, 30), (x, y)


# --- tentacles (behind the hood, in front of nothing) ----------------------------------
def quad(p0, p1, p2, t):
    u = 1 - t
    x = u*u*p0[0] + 2*u*t*p1[0] + t*t*p2[0]
    y = u*u*p0[1] + 2*u*t*p1[1] + t*t*p2[1]
    dx = 2*u*(p1[0]-p0[0]) + 2*t*(p2[0]-p1[0])
    dy = 2*u*(p1[1]-p0[1]) + 2*t*(p2[1]-p1[1])
    return x, y, dx, dy

def tentacle(i, root, ctrl, tip, w0, w1, curl, opacity=90, n=18, cs=1.0):
    L, Rr, mid = [], [], []
    for k in range(n + 1):
        t = k / n
        x, y, dx, dy = quad(root, ctrl, tip, t)
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy/ln, dx/ln
        w = (w0 + (w1 - w0) * t) / 2
        mid.append((x, y, dx/ln, dy/ln))
        L.append((x + nx*w, y + ny*w)); Rr.append((x - nx*w, y - ny*w))
    s = "M%.1f,%.1f " % L[0] + " ".join("L%.1f,%.1f" % p for p in L[1:])
    s += " " + " ".join("L%.1f,%.1f" % p for p in reversed(Rr)) + " Z"
    d.path(s, f"Tentacle {i}", fill=TENT_GRAD, stroke="#8A5A40", strokeWidth=2, opacity=opacity)
    # ringed texture: faint bands across the tentacle
    for j, t in enumerate([0.3, 0.45, 0.6, 0.75]):
        x, y, ux, uy = mid[round(t * n)]
        w = (w0 + (w1 - w0) * t) / 2
        d.path("M%.1f,%.1f L%.1f,%.1f" % (x - uy*w*0.8, y + ux*w*0.8, x + uy*w*0.8, y - ux*w*0.8),
               f"Tentacle {i} ring {j+1}", fill=NONE, stroke="#9A6448", strokeWidth=1.5, opacity=35)
    x, y, ux, uy = mid[-1]
    px, py = -uy * curl, ux * curl
    p1 = (x + ux*12*cs, y + uy*12*cs)
    p2 = (x + ux*16*cs + px*12*cs, y + uy*16*cs + py*12*cs)
    p3 = (x + ux*6*cs + px*16*cs, y + uy*6*cs + py*16*cs)
    d.path("M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (x, y, p1[0], p1[1], p2[0], p2[1], p3[0], p3[1]),
           f"Tentacle {i} tip", fill=NONE, stroke="#D8A888", strokeWidth=max(2.5, w1 - 1), cap="round")
    assert on_disc(p2[0], p2[1], 20), (i, p2)

dx_, dy_ = VENTRAL[0] - DORSAL[0], VENTRAL[1] - DORSAL[1]
def ap(t, out=0.0):
    """Point along the aperture (0=dorsal, 1=ventral), pushed `out` px forward."""
    return (DORSAL[0] + dx_ * t - out, DORSAL[1] + dy_ * t)

# a fan of slender tentacles; back row (darker, thinner) first
NT = 16
rng = random.Random(32)
order = [k for k in range(NT) if k % 2] + [k for k in range(NT) if not k % 2]
for k in order:
    f = k / (NT - 1)
    root = ap(0.46 + 0.40 * f, 4)
    a = math.radians(200 - 60 * f + rng.uniform(-5, 5))
    L = 170 + 40 * math.sin(f * math.pi) + rng.uniform(-22, 18) - (16 if k % 2 else 0)
    bend = rng.uniform(-0.30, 0.34)
    tip = (root[0] + L * math.cos(a), root[1] + L * math.sin(a))
    ctrl = (root[0] + 0.55 * L * math.cos(a + bend), root[1] + 0.55 * L * math.sin(a + bend))
    back = bool(k % 2)
    tentacle(k + 1, root, ctrl, tip, 9 if back else 12, 3 if back else 4,
             1 if bend < 0 else -1, 62 if back else 94, cs=rng.uniform(0.6, 1.4))

# funnel (hyponome) tucked under the tentacles at the ventral lip
f0 = ap(0.84, 2); f1 = ap(0.96, 2)
d.path("M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f "
       "C%.1f,%.1f %.1f,%.1f %.1f,%.1f Z" % (
    f0[0], f0[1], f0[0] - 24, f0[1] + 4, f0[0] - 44, f0[1] + 14, f0[0] - 56, f0[1] + 28,
    f0[0] - 60, f0[1] + 36, f0[0] - 50, f0[1] + 42, f0[0] - 40, f0[1] + 38,
    f1[0] - 20, f1[1] + 6, f1[0] - 8, f1[1] + 2, f1[0], f1[1]),
    "Funnel", fill=FUNNEL_GRAD, stroke=INK, strokeWidth=3)
d.path("M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (
    f0[0] - 8, f0[1] + 8, f0[0] - 26, f0[1] + 12, f0[0] - 40, f0[1] + 20, f0[0] - 50, f0[1] + 30),
    "Funnel sheen", fill=NONE, stroke="#FFE8D4", strokeWidth=3, opacity=45, cap="round")

# --- shell ---------------------------------------------------------------------------------
d.path(SHELL, "Shell", fill=SHELL_GRAD, stroke=NONE)

# russet flame stripes on the older two thirds of the last whorl, fading toward the aperture
UMB = 0.07
def stripe(k, psi, w0, sweep, alpha):
    n = 22
    left, right = [], []
    for j in range(n + 1):
        s = j / n
        th = psi - sweep * s + 0.12 * math.sin(math.pi * s)
        w = w0 * (0.25 + 0.75 * s)
        for side, acc in ((-1, left), (1, right)):
            a = th + side * w / 2
            r0 = SH.R * UMB
            r = r0 + (SH.edge(a) * 0.995 - r0) * (s ** 0.9)
            acc.append((SH.cx + r * math.cos(a), SH.cy + r * math.sin(a)))
    s_ = "M%.1f,%.1f " % left[0] + " ".join("L%.1f,%.1f" % p for p in left[1:])
    s_ += " " + " ".join("L%.1f,%.1f" % p for p in reversed(right)) + " Z"
    d.path(s_, f"Stripe {k}", fill=STRIPE_GRAD, stroke=NONE, opacity=alpha)

start = TE - 2 * math.pi + 0.55
end = TE - 0.85 * math.pi
N = 12
gap = (end - start) / (N - 1)
for k in range(N):
    f = k / (N - 1)
    psi = start + gap * k
    w0 = gap * (0.48 + 0.10 * math.sin(k * 1.7))
    alpha = round(90 - 62 * f ** 1.5)
    stripe(k + 1, psi, w0, -0.42, alpha)
    # flames fork near the venter: a short thin sister stripe
    if k < N - 1:
        stripe(f"{k+1}b", psi + gap * 0.62, gap * 0.16, -0.42, round(alpha * 0.6))

# growth lines near the aperture (parallel to the lip), very faint
for j, thg in enumerate([TE - 0.22, TE - 0.55, TE - 0.95]):
    o = SH.pt(thg, 0.985); i_ = SH.pt(thg, 0.1)
    d.path("M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" % (i_[0], i_[1], (o[0] + i_[0]) / 2 - 14, (o[1] + i_[1]) / 2,
                                               o[0], o[1]),
           f"Growth line {j+1}", fill=NONE, stroke="#B8946C", strokeWidth=2, opacity=22, cap="round")

# volume: shade along the ventral rim, highlight across the upper flank
d.path(SH.curve(TE - 1.6 * math.pi, TE, rf=1.0) + " " +
       SH.curve(TE, TE - 1.6 * math.pi, rf=0.86, move=False).replace("M", "L", 1) + " Z",
       "Venter shade", fill="#6E3E22", opacity=20, stroke=NONE)
d.path(SH.curve(TE - 1.55 * math.pi, TE - 0.9 * math.pi, rf=0.78), "Flank highlight",
       fill=NONE, stroke="#FFFFFF", strokeWidth=26, opacity=16, cap="round")
d.path(SH.curve(TE - 1.45 * math.pi, TE - 1.05 * math.pi, rf=0.80), "Flank highlight core",
       fill=NONE, stroke="#FFFFFF", strokeWidth=8, opacity=30, cap="round")
# umbilical callus: the coil's eye
uc = SH.R * 0.075
d.shape("ellipse", "Umbilicus shade", x=round(SH.cx - uc * 1.6), y=round(SH.cy - uc * 1.6),
        width=round(uc * 3.2), height=round(uc * 3.2), fill="#5A3020", opacity=28, stroke=NONE)
d.shape("ellipse", "Umbilical callus", x=round(SH.cx - uc), y=round(SH.cy - uc),
        width=round(uc * 2), height=round(uc * 2),
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#FFF6E6"}, {"offset": 1, "color": "#C8A47C"}]}},
        stroke="#7A4A2C", strokeWidth=2)
# shell outline on top, hiding stripe ends
d.path(SHELL, "Shell outline", fill=NONE, stroke=INK, strokeWidth=6)
d.path(SH.curve(TE - 1.5 * math.pi, TE - 0.4 * math.pi, rf=0.975), "Venter rim light",
       fill=NONE, stroke="#FFF6E2", strokeWidth=3, opacity=45, cap="round")

# --- hood + eye ------------------------------------------------------------------------------
h0 = ap(-0.10, -10); h1 = ap(0.50, -4)
d.path("M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f "
       "C%.1f,%.1f %.1f,%.1f %.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f Z" % (
        h0[0], h0[1],
        h0[0] - 30, h0[1] - 26, h0[0] - 96, h0[1] - 22, h0[0] - 122, h0[1] + 18,
        h0[0] - 140, h0[1] + 48, h0[0] - 132, h0[1] + 86, h1[0] - 96, h1[1] - 6,
        h1[0] - 70, h1[1] + 4, h1[0] - 40, h1[1] + 8, h1[0] - 14, h1[1] + 4,
        h1[0] - 4, h1[1] - 30, h0[0] + 10, h0[1] + 40, h0[0], h0[1]),
       "Hood", fill=HOOD_GRAD, stroke=INK, strokeWidth=4)
for i, (ox, oy, w, h) in enumerate([(-50, 0, 26, 14), (-92, 18, 20, 12), (-30, 30, 18, 10),
                                    (-114, 50, 14, 9), (-70, 46, 18, 10), (-40, 70, 14, 8),
                                    (-96, 80, 12, 8)]):
    d.shape("ellipse", f"Hood mottle {i+1}", x=round(h0[0] + ox), y=round(h0[1] + oy),
            width=w, height=h, fill="#6A3A20", opacity=35, stroke=NONE)
d.path("M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (
        h0[0] - 24, h0[1] - 10, h0[0] - 76, h0[1] - 14, h0[0] - 110, h0[1] + 10, h0[0] - 122, h0[1] + 40),
       "Hood sheen", fill=NONE, stroke="#FFF0DC", strokeWidth=4, opacity=40, cap="round")
e = ap(0.56, 34)
d.shape("ellipse", "Eye socket", x=round(e[0] - 21), y=round(e[1] - 19), width=42, height=38,
        fill="#C8946C", opacity=55, stroke=NONE)
d.shape("ellipse", "Eye", x=round(e[0] - 14), y=round(e[1] - 13), width=28, height=26,
        fill=EYE_GRAD, stroke=INK, strokeWidth=3)
d.shape("ellipse", "Eye glint", x=round(e[0] - 8), y=round(e[1] - 8), width=7, height=7,
        fill="#FFFFFF", opacity=85, stroke=NONE)

print("shell corners", [round(v) for v in DORSAL + VENTRAL])

# --- name ------------------------------------------------------------------------------------
d.text("NAUTILUS", "Name", x=500, y=960, size=58, font="Virelai Sans",
       color="#E6EEF4", justify="center")

d.finish("nautilus-V1R00")
