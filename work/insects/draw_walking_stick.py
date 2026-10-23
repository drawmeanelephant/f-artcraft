#!/usr/bin/env python3
"""Walking stick — field plate V1R00. A twig that has opinions: full-body
profile lying along a diagonal branch, painted in the branch's own bark so it
nearly disappears, given away only by a gradient seam along its underside, a
deadpan half-lidded eye and one antenna that moves. Brown-green plate with
bark grain. Played completely straight, like the potoo. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math, re, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Walking Stick — Field Plate", 1000, 1000)
rng = random.Random(80)   # fixed seed: the bark is the same every run

PCX, PCY, PR = 500, 460, 420
INK = "#2E2618"   # dark bark, not black

def lin(c0, c1, start=None, end=None, o0=None, o1=None):
    s0 = {"offset": 0, "color": c0}; s1 = {"offset": 1, "color": c1}
    if o0 is not None: s0["opacity"] = o0
    if o1 is not None: s1["opacity"] = o1
    g = {"kind": "linear", "stops": [s0, s1]}
    if start: g["start"], g["end"] = start, end
    return {"gradient": g}

def rad(*stops):
    n = len(stops) - 1
    return {"gradient": {"kind": "radial", "stops": [
        {"offset": round(i / n, 3), "color": c} for i, c in enumerate(stops)]}}

def smooth(pts, closed=True, k=1.0):
    """Catmull-Rom through pts as cubic Beziers."""
    n = len(pts)
    s = "M%.1f,%.1f" % pts[0]
    rng_ = range(n) if closed else range(n - 1)
    for i in rng_:
        p0 = pts[(i - 1) % n] if (closed or i > 0) else pts[0]
        p1, p2 = pts[i], pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (closed or i + 2 < n) else pts[-1]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6 * k, p1[1] + (p2[1] - p0[1]) / 6 * k)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6 * k, p2[1] - (p3[1] - p1[1]) / 6 * k)
        s += " C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (c1 + c2 + p2)
    return s + (" Z" if closed else "")

def P(a):
    t = math.radians(a)
    return (PCX + PR * math.cos(t), PCY + PR * math.sin(t))

def ang(p):
    return math.degrees(math.atan2(p[1] - PCY, p[0] - PCX)) % 360

def arc_to(a_from, a_to):
    """Close along the disc's own arc, the short way round."""
    delta = (a_to - a_from + 540) % 360 - 180
    x, y = P(a_to)
    return f"A420,420 0 0 {1 if delta > 0 else 0} {x:.1f},{y:.1f}"

def ray_circle(p, dv):
    fx, fy = p[0] - PCX, p[1] - PCY
    a = dv[0]**2 + dv[1]**2; b = 2*(fx*dv[0] + fy*dv[1]); c = fx*fx + fy*fy - PR*PR
    t = (-b + math.sqrt(b*b - 4*a*c)) / (2*a)
    return (p[0] + t*dv[0], p[1] + t*dv[1])

# --- the branch's frame: s runs along it toward the upper right, h is height above its axis --
C0 = P(155); C1 = P(-22)
ln = math.hypot(C1[0] - C0[0], C1[1] - C0[1])
U = ((C1[0] - C0[0]) / ln, (C1[1] - C0[1]) / ln)
N = (U[1], -U[0])                     # "up", away from the branch
MID = ((C0[0] + C1[0]) / 2, (C0[1] + C1[1]) / 2)
REACH = []
def B(s, h, track=True):
    p = (MID[0] + s*U[0] + h*N[0], MID[1] + s*U[1] + h*N[1])
    if track: REACH.append(p)
    return p

def bp(s_, track=True):
    out, buf = [], []
    for t in re.findall(r"[A-Za-z]|-?\d*\.?\d+", s_):
        if t.isalpha():
            out.append(t)
        else:
            buf.append(float(t))
            if len(buf) == 2:
                x, y = B(*buf, track=track); out.append(f"{x:.1f},{y:.1f}"); buf = []
    return " ".join(out)

def bell(cs, ch, rs, rh, track=True):
    k = 0.5523
    return bp(f"M{cs+rs},{ch} C{cs+rs},{ch+rh*k} {cs+rs*k},{ch+rh} {cs},{ch+rh} "
              f"C{cs-rs*k},{ch+rh} {cs-rs},{ch+rh*k} {cs-rs},{ch} "
              f"C{cs-rs},{ch-rh*k} {cs-rs*k},{ch-rh} {cs},{ch-rh} "
              f"C{cs+rs*k},{ch-rh} {cs+rs},{ch-rh*k} {cs+rs},{ch} Z", track)

def bark(top, bot):
    """Bark shading across a stick: lit top, dark underside."""
    a, b = B(0, top, False), B(0, bot, False)
    return {"gradient": {"kind": "linear", "start": [round(a[0], 1), round(a[1], 1)],
                         "end": [round(b[0], 1), round(b[1], 1)], "stops": [
        {"offset": 0, "color": "#A08A62"}, {"offset": 0.4, "color": "#7C6846"},
        {"offset": 1, "color": "#45372A"}]}}

# --- backdrop + plate --------------------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin("#1D1B12", "#080705", [0, 0], [0, 1000]), stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad("#D2CCA4", "#A9A47C", "#76714F"), stroke=NONE)
# bark grain over the plate: long translucent strokes running with the branch, kept off the rim
n = 0
while n < 26:
    h = rng.uniform(-380, 380)
    half = math.sqrt(max(0.0, 360**2 - h**2)) * rng.uniform(0.4, 0.9)
    if half < 80:
        continue
    s0 = rng.uniform(-360 + half, 360 - half) if half < 360 else 0
    pts = [B(s0 - half + i * half / 3, h + rng.uniform(-6, 6), False) for i in range(7)]
    if max(math.hypot(x - PCX, y - PCY) for x, y in pts) > PR - 30:
        continue
    d.path(smooth(pts, closed=False), f"Plate grain {n+1}", fill=NONE,
           stroke=rng.choice(["#5E5838", "#E6E0BC"]), strokeWidth=3, opacity=rng.randint(7, 12), cap="round")
    n += 1
for i in range(14):
    while True:
        x, y = rng.uniform(140, 860), rng.uniform(100, 820)
        if math.hypot(x - PCX, y - PCY) < PR - 40:
            break
    w = rng.uniform(6, 14)
    d.shape("ellipse", f"Lichen fleck {i+1}", x=round(x, 1), y=round(y, 1), width=round(w, 1),
            height=round(w * 0.7, 1), fill="#8E9A6A", opacity=rng.randint(18, 32), stroke=NONE)

# --- side twigs (real ones; the legs will copy them) ------------------------------------------------
def twig(name, base_s, base_h, tip, w0, leaves):
    bs, bh = base_s, base_h
    ts, th = tip
    ds_, dh_ = ts - bs, th - bh
    l = math.hypot(ds_, dh_); ps, ph = -dh_ / l, ds_ / l
    s = bp(f"M{bs - ps*w0},{bh - ph*w0} Q{bs + ds_*0.5 - ps*w0*0.6 + 6},{bh + dh_*0.5 - ph*w0*0.6} "
           f"{ts - ps*2},{th - ph*2} L{ts + ps*2},{th + ph*2} "
           f"Q{bs + ds_*0.5 + ps*w0*0.6 + 6},{bh + dh_*0.5 + ph*w0*0.6} {bs + ps*w0},{bh + ph*w0} Z")
    d.path(s, name, fill=bark(bh + 10, bh - 10), stroke=INK, strokeWidth=3)
    for j, (ls, lh, rot, size) in enumerate(leaves):
        r = math.radians(rot); cs, sn = math.cos(r), math.sin(r)
        def T(a, b): return (ls + a*cs - b*sn, lh + a*sn + b*cs)
        pts = [T(0, 0), T(size*0.3, size*0.22), T(size*0.75, size*0.16), T(size, 0),
               T(size*0.75, -size*0.16), T(size*0.3, -size*0.22)]
        cv = [B(*p) for p in pts]
        d.path(smooth(cv), f"{name} leaf {j+1}", fill=lin("#9AAA62", "#5A6E38", [cv[0][0], cv[0][1]],
               [cv[3][0], cv[3][1]]), stroke="#4A5A2C", strokeWidth=3, opacity=92)
        a, b = B(*T(size*0.08, 0)), B(*T(size*0.9, 0))
        d.path(f"M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}", f"{name} leaf {j+1} vein", fill=NONE,
               stroke="#E4E8C0", strokeWidth=3, opacity=45, cap="round")

twig("Twig up", 270, 20, (304, 126), 9, [(304, 126, -60, 52), (300, 118, 40, 46)])
twig("Twig down", 40, -20, (96, -122), 8, [(96, -122, 70, 50)])
twig("Twig back", -300, 20, (-352, 118), 8, [(-352, 118, -120, 48)])

# --- the branch: both ends close on the disc's own arc ----------------------------------------------
HB = 26
def edge(h, sign):
    pts = []
    for i in range(-6, 7):
        s = i * 60
        pts.append(B(s, h + rng.uniform(-2.5, 2.5) + 6 * math.sin(i * 0.9) * 0.4, False))
    a = ray_circle(pts[1], (-U[0], -U[1])); b = ray_circle(pts[-2], U)
    return [a] + pts[1:-1] + [b]
top = edge(HB, 1); bot = edge(-HB, -1)
s = smooth(top, closed=False) + " " + arc_to(ang(top[-1]), ang(bot[-1])) + " " + \
    smooth(list(reversed(bot)), closed=False).replace("M", "L", 1) + " " + arc_to(ang(bot[0]), ang(top[0])) + " Z"
d.path(s, "Branch", fill=bark(HB, -HB), stroke=INK, strokeWidth=4)
def grooves(prefix, s_lo, s_hi, h_lo, h_hi, count):
    for i in range(count):
        s0 = rng.uniform(s_lo, s_hi); hh = rng.uniform(h_lo, h_hi); L_ = rng.uniform(40, 120)
        pts = [B(s0 + j * L_ / 4, hh + rng.uniform(-1.5, 1.5), False) for j in range(5)]
        dark = rng.random() < 0.65
        d.path(smooth(pts, closed=False), f"{prefix} {i+1}", fill=NONE,
               stroke="#2E2418" if dark else "#C8B48C", strokeWidth=3,
               opacity=rng.randint(30, 50) if dark else rng.randint(20, 35), cap="round")
grooves("Bark groove", -390, 300, -20, 20, 46)
for i, (ks, kh, rs, rh) in enumerate([(-170, -4, 16, 9), (150, 2, 12, 7), (-330, 4, 10, 6)]):
    d.path(bell(ks, kh, rs, rh, False), f"Knot {i+1}", fill=rad("#3A2E20", "#6A5838"), stroke=INK, strokeWidth=3, opacity=85)
    d.path(bell(ks, kh, rs + 7, rh + 5, False), f"Knot ring {i+1}", fill=NONE, stroke="#2E2418", strokeWidth=3, opacity=35)
for i in range(10):
    ls, lh = rng.uniform(-340, 320), rng.uniform(-18, 22)
    d.path(bell(ls, lh, rng.uniform(5, 11), rng.uniform(3, 6), False), f"Branch lichen {i+1}",
           fill="#A8B47E", opacity=rng.randint(35, 55), stroke=NONE)
d.path(smooth([B(s, HB - 3 + rng.uniform(-1, 1), False) for s in range(-360, 361, 60)], closed=False),
       "Branch top light", fill=NONE, stroke="#D2C098", strokeWidth=4, opacity=35, cap="round")

# --- the insect, in the branch's own bark ---------------------------------------------------------
H0 = HB + 1                       # its underside rests on the branch
def leg(name, pts, op=100, w=7):
    cv = [B(*p) for p in pts]
    s_ = "M%.1f,%.1f " % cv[0] + " ".join("L%.1f,%.1f" % p for p in cv[1:])
    d.path(s_, name + " edge", fill=NONE, stroke=INK, strokeWidth=w + 3, cap="round", join="round", opacity=op * 0.7)
    d.path(s_, name, fill=NONE, stroke="#7C6846", strokeWidth=w, cap="round", join="round", opacity=op)
    d.path(s_, name + " light", fill=NONE, stroke="#B49E74", strokeWidth=3, cap="round", join="round", opacity=op * 0.35)
    for p in cv[1:-1]:
        d.shape("ellipse", name + " knee", x=round(p[0] - 4.5, 1), y=round(p[1] - 4.5, 1), width=9, height=9,
                fill=rad("#9A8660", "#5A4832"), stroke=INK, strokeWidth=2, opacity=op)

# far-side legs first, a step back
leg("Far hind leg", [(-14, H0 + 8), (-48, H0 + 86), (-98, H0)], 70, 5)
leg("Far mid leg", [(46, H0 + 8), (96, H0 + 80), (134, H0)], 70, 5)

# body: a tapered tube, abdomen -> thorax -> head
prof = [(-232, 4), (-215, 8), (-170, 10), (-110, 11), (-40, 12), (20, 13), (80, 13), (122, 12),
        (130, 10), (138, 13), (148, 15), (160, 14), (170, 10), (176, 4)]
upper = [(s_, H0 + t * 1.45) for s_, t in prof]
lower = [(s_, H0 + (0 if s_ < 136 else -1)) for s_, t in reversed(prof)]
body = [B(*p) for p in upper + lower[1:-1]]
d.path(smooth(body), "Body", fill=bark(H0 + 21, H0), stroke=INK, strokeWidth=3)
grooves("Body groove", -220, 110, H0 + 4, H0 + 14, 11)
for i, s_ in enumerate([-180, -140, -100, -62, -24, 128, 136]):
    a, b = B(s_, H0), B(s_ + 1, H0 + 16)
    d.path(f"M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}", f"Segment line {i+1}", fill=NONE,
           stroke="#3A2E20", strokeWidth=3, opacity=40, cap="round")
# the only tell: a gradient seam where the insect lies on the wood
a, b = B(-232, H0, False), B(176, H0, False)
d.path(bp(f"M-228,{H0 + 1} C-120,{H0 + 1} 40,{H0 + 1} 172,{H0}"), "Seam", fill=NONE, strokeWidth=4, cap="round",
       stroke={"gradient": {"kind": "linear", "start": [round(a[0], 1), round(a[1], 1)],
               "end": [round(b[0], 1), round(b[1], 1)], "stops": [
               {"offset": 0, "color": "#C8D29A", "opacity": 0}, {"offset": 0.3, "color": "#C8D29A", "opacity": 0.75},
               {"offset": 0.7, "color": "#E0D8A4", "opacity": 0.85}, {"offset": 1, "color": "#E0D8A4", "opacity": 0}]}})

# near-side legs: hind and mid bent like twigs, fore legs stretched straight ahead
leg("Near hind leg", [(-20, H0 + 6), (-62, H0 + 98), (-118, H0)])
leg("Near mid leg", [(40, H0 + 6), (84, H0 + 92), (122, H0)])
leg("Fore legs", [(130, H0 + 6), (210, H0 + 7), (282, H0 + 4)], 100, 5)

# head: one small bead of an eye under a flat lid
d.path(bell(160, H0 + 11, 5, 5), "Eye", fill=rad("#4A3E2C", "#1A140C"), stroke=INK, strokeWidth=2)
d.path(bp(f"M153,{H0 + 13} L167,{H0 + 13}"), "Eye lid", fill=NONE, stroke="#5A4832", strokeWidth=3, cap="round")
d.path(bell(158, H0 + 9, 1.6, 1.6), "Eye glint", fill="#F2E8D0", opacity=55, stroke=NONE)

# antennae: one lies along the branch like a splinter; the other is the whole performance
d.path(bp(f"M174,{H0 + 8} C220,{H0 + 9} 270,{H0 + 9} 312,{H0 + 7}"), "Antenna still", fill=NONE,
       stroke="#6E5C40", strokeWidth=3, cap="round")
d.path(bp(f"M172,{H0 + 11} C196,{H0 + 50} 220,{H0 + 104} 236,{H0 + 150}"), "Antenna ghost", fill=NONE,
       stroke="#5A4832", strokeWidth=3, cap="round", opacity=22)
d.path(bp(f"M172,{H0 + 11} C206,{H0 + 44} 240,{H0 + 92} 266,{H0 + 134}"), "Antenna moving", fill=NONE,
       stroke="#5A4832", strokeWidth=3.5, cap="round")
for i, (s0, h0, s1, h1, s2, h2) in enumerate([(258, H0 + 156, 272, H0 + 160, 284, H0 + 152),
                                              (276, H0 + 170, 292, H0 + 172, 304, H0 + 162),
                                              (238, H0 + 170, 250, H0 + 178, 264, H0 + 176)]):
    d.path(bp(f"M{s0},{h0} Q{s1},{h1} {s2},{h2}"), f"Twitch {i+1}", fill=NONE, stroke="#3E3222",
           strokeWidth=3, opacity=55, cap="round")

# --- rim drawn last so everything inside closes under it -------------------------------------------
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840, fill=NONE, stroke="#5C5638", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F2EED4", strokeWidth=3, opacity=40)

far, fp = max((math.hypot(x - PCX, y - PCY), (round(x), round(y))) for x, y in REACH)
print("farthest point", fp)
print(f"insect + twig reach from disc center: {far:.0f} (inner ring 396)")
assert far < 392, far

# --- name + second line ------------------------------------------------------------------------------
d.text("WALKING STICK", "Name", x=500, y=940, size=58, font="Virelai Sans", color="#E4DEC0", justify="center")
r = d.text("PHASMATODEA", "Second line", x=500, y=975, size=22, font="Virelai Sans",
           color="#B4AE86", justify="center")
d.cmd("text.setStyle", "Second line tracking", id=r["id"], tracking=300)
def find(o, oid):
    if isinstance(o, dict):
        if o.get("id") == oid and "bounds" in o: return o
        o = list(o.values())
    if isinstance(o, list):
        for v in o:
            hit = find(v, oid)
            if hit: return hit
b2 = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("second line bounds", {k: round(v) for k, v in b2.items()})
assert b2["width"] <= 760 and b2["x"] >= 100 and b2["y"] + b2["height"] <= 990, b2

d.finish("walking-stick-V1R00")
