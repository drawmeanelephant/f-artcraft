#!/usr/bin/env python3
"""Green darner — field plate V1R00. A dragonfly caught mid-beat: three-quarter
dorsal from above, four translucent wings with fine dense venation and amber
pterostigmas, green thorax, blue abdomen, ghosted wing outlines as a faint
motion smear behind. Reedy green plate. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math, re, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Green Darner — Field Plate", 1000, 1000)
rng = random.Random(78)   # fixed seed: crossvein jitter is the same every run

PCX, PCY, PR = 500, 460, 420
INK = "#1F2A1E"   # deep reed-green, not black

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

def cross(edge, mid, p0, p1):
    """Cylinder shading across a body part: dark rim, lit band, dark rim."""
    return {"gradient": {"kind": "linear", "start": [round(p0[0], 1), round(p0[1], 1)],
                         "end": [round(p1[0], 1), round(p1[1], 1)], "stops": [
        {"offset": 0, "color": edge}, {"offset": 0.38, "color": mid}, {"offset": 1, "color": edge}]}}

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

def arc_to(a_from, a_to):
    """Close along the disc's own arc, the short way round."""
    delta = (a_to - a_from + 540) % 360 - 180
    x, y = P(a_to)
    return f"A420,420 0 0 {1 if delta > 0 else 0} {x:.1f},{y:.1f}"

# --- the insect's own frame: x runs tail->head, y across the back (+y = its right) -------
O = (500, 450)
A = math.radians(-83)
U = (math.cos(A), math.sin(A)); V = (-math.sin(A), math.cos(A))
REACH = []
def L(x, y, track=True):
    p = (O[0] + x*U[0] + y*V[0], O[1] + x*U[1] + y*V[1])
    if track: REACH.append(p)
    return p

def lp(s, track=True):
    out, buf = [], []
    for t in re.findall(r"[A-Za-z]|-?\d*\.?\d+", s):
        if t.isalpha():
            out.append(t)
        else:
            buf.append(float(t))
            if len(buf) == 2:
                x, y = L(*buf, track=track); out.append(f"{x:.1f},{y:.1f}"); buf = []
    return " ".join(out)

def lell(cx, cy, rx, ry):
    k = 0.5523
    return lp(f"M{cx+rx},{cy} C{cx+rx},{cy+ry*k} {cx+rx*k},{cy+ry} {cx},{cy+ry} "
              f"C{cx-rx*k},{cy+ry} {cx-rx},{cy+ry*k} {cx-rx},{cy} "
              f"C{cx-rx},{cy-ry*k} {cx-rx*k},{cy-ry} {cx},{cy-ry} "
              f"C{cx+rx*k},{cy-ry} {cx+rx},{cy-ry*k} {cx+rx},{cy} Z")

def poly(pts):
    return "M%.1f,%.1f " % pts[0] + " ".join("L%.1f,%.1f" % p for p in pts[1:])

# --- palette -----------------------------------------------------------------------------
BG_GRAD = lin("#0F1C11", "#040905", [0, 0], [0, 1000])
PLATE_GRAD = rad("#D6E6BE", "#A9C892", "#6E9362")
REED_A = lin("#5E8A4E", "#2F5232", [0, 300], [0, 880])
REED_B = lin("#7EA468", "#456E44", [0, 360], [0, 880])
EYE_GRAD = rad("#A6D49A", "#5E9A72", "#2C5A4C")
THORAX = "#4F9A3A"
VEIN = "#2B382C"

# --- backdrop + plate ----------------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840, fill=PLATE_GRAD, stroke=NONE)
d.shape("ellipse", "Plate haze", x=170, y=90, width=660, height=360,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#F4F8E6", "opacity": 0.35}, {"offset": 1, "color": "#F4F8E6", "opacity": 0}]}},
        stroke=NONE)

# --- reeds: every blade closes on the disc's own arc ---------------------------------------
def reed(name, a_lo, a_hi, tip, lean, fill, op):
    p0, p1 = P(a_lo), P(a_hi)
    s = (f"M{p0[0]:.1f},{p0[1]:.1f} "
         f"C{p0[0]+lean*0.2:.1f},{p0[1]-120:.1f} {tip[0]-lean*0.4:.1f},{tip[1]+160:.1f} {tip[0]:.1f},{tip[1]:.1f} "
         f"C{tip[0]-lean*0.5:.1f},{tip[1]+170:.1f} {p1[0]+lean*0.1:.1f},{p1[1]-110:.1f} {p1[0]:.1f},{p1[1]:.1f} "
         + arc_to(a_hi, a_lo) + " Z")
    d.path(s, name, fill=fill, stroke=NONE, opacity=op)
for i, (lo, hi, tip, lean, f, o) in enumerate([
        (131, 134, (150, 300), -40, REED_A, 55), (121, 124, (240, 200), 30, REED_B, 45),
        (112, 114.5, (330, 330), -20, REED_A, 50), (104, 106, (380, 470), 26, REED_B, 40),
        (76, 78, (640, 420), -24, REED_B, 40), (66, 68.5, (700, 210), 30, REED_A, 50),
        (57, 60, (790, 300), -30, REED_B, 45), (48, 51, (860, 380), 20, REED_A, 55)]):
    reed(f"Reed {i+1}", lo, hi, tip, lean, f, o)
# two cattails standing in the reeds
for i, (lo, hi, top) in enumerate([(117, 118.2, (282, 250)), (61.5, 62.7, (742, 230))]):
    p0, p1 = P(lo), P(hi)
    s = (f"M{p0[0]:.1f},{p0[1]:.1f} L{top[0]+3:.1f},{top[1]:.1f} L{top[0]-3:.1f},{top[1]:.1f} "
         f"L{p1[0]:.1f},{p1[1]:.1f} " + arc_to(hi, lo) + " Z")
    d.path(s, f"Cattail stem {i+1}", fill=lin("#6E8A4C", "#3E5530"), stroke=NONE, opacity=70)
    d.shape("ellipse", f"Cattail head {i+1}", x=top[0]-11, y=top[1]+18, width=22, height=74,
            fill=lin("#8A5A34", "#4E301C"), stroke=NONE, opacity=80)
    d.path(f"M{top[0]:.1f},{top[1]+18:.1f} L{top[0]:.1f},{top[1]-14:.1f}", f"Cattail spike {i+1}",
           fill=NONE, stroke="#6E8A4C", strokeWidth=3, opacity=70, cap="round")

# --- wings ----------------------------------------------------------------------------------
def make_wing(root, tip, cmax, profile, side, span_k=1.0, rot=0.0):
    """Returns P(s, w): s root->tip along the span, w leading->trailing edge."""
    rx, ry = root
    tx, ty = tip
    tx, ty = rx + (tx - rx) * 1.0, ry + (ty - ry) * span_k
    ca, sa = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    def turn(x, y):
        dx, dy = x - rx, y - ry
        return (rx + dx*ca - dy*sa*side, ry + dx*sa*side + dy*ca)
    def pt(s, w):
        lx = rx + (tx - rx) * s + 14 * math.sin(math.pi * s)       # leading edge bows forward
        ly = ry + (ty - ry) * s
        c = cmax * profile(s) * span_k ** 0.3
        return L(*turn(lx - c * w, ly + side * c * w * 0.10))
    return pt

def fore_profile(s):
    return (0.55 + 0.45 * math.sin(min(s / 0.32, 1) * math.pi / 2)) * max(0.0, 1 - s**3.2) ** 0.5

def hind_profile(s):
    return (1.0 - 0.28 * s) * max(0.0, 1 - s**3.0) ** 0.5

def outline(pt, n=30):
    lead = [pt(i / n, 0) for i in range(n + 1)]
    trail = [pt(i / n, 1) for i in range(n, -1, -1)]
    return smooth(lead + trail[1:-1], closed=True)

WINGS = [  # name, root, tip, chord, profile, side
    ("Fore wing R", (44, 30), (72, 352), 70, fore_profile, 1),
    ("Fore wing L", (44, -30), (72, -340), 68, fore_profile, -1),
    ("Hind wing R", (-6, 32), (-52, 338), 104, hind_profile, 1),
    ("Hind wing L", (-6, -32), (-52, -326), 100, hind_profile, -1),
]

# ghost outlines first: the same wings caught a beat earlier and later
for k, (sk, rot, op) in enumerate([(0.86, 9, 7), (0.74, 17, 5)]):
    for name, root, tip, c, prof, side in WINGS:
        pt = make_wing(root, tip, c, prof, side, span_k=sk, rot=rot if "Hind" in name else -rot)
        d.path(outline(pt), f"{name} ghost {k+1}", fill="#F6FAF0", opacity=op * 2,
               stroke="#2B382C", strokeWidth=3)
for i, (name, root, tip, c, prof, side) in enumerate(WINGS):
    pt = make_wing(root, tip, c, prof, side, span_k=1.08, rot=4 if "Hind" in name else -4)
    a = [pt(s / 12, 1.15) for s in range(3, 12)]
    d.path(smooth(a, closed=False), f"{name} smear arc", fill=NONE, stroke="#FFFFFF",
           strokeWidth=4, opacity=22, cap="round")

def draw_wing(name, root, tip, cmax, prof, side):
    pt = make_wing(root, tip, cmax, prof, side)
    base, far_tip = pt(0, 0.5), pt(1, 0)
    d.path(outline(pt), name, fill={"gradient": {"kind": "linear",
           "start": [round(base[0], 1), round(base[1], 1)], "end": [round(far_tip[0], 1), round(far_tip[1], 1)],
           "stops": [{"offset": 0, "color": "#E6D49A", "opacity": 0.42},
                     {"offset": 0.35, "color": "#EEF4E6", "opacity": 0.24},
                     {"offset": 1, "color": "#F4F8F0", "opacity": 0.16}]}},
           stroke=VEIN, strokeWidth=4, opacity=90)
    # longitudinal veins: subcosta, radius, radial sector, media, cubitus, anal
    W = [(0.07, 0.46), (0.14, 0.98), (0.30, 0.93), (0.46, 0.88), (0.64, 0.78), (0.82, 0.55)]
    for j, (w, s_end) in enumerate(W):
        pts = [pt(s_end * i / 18, w) for i in range(19)]
        d.path(smooth(pts, closed=False), f"{name} vein {j+1}", fill=NONE, stroke=VEIN,
               strokeWidth=3.5, opacity=62, cap="round")
    # crossveins: one compound path per wing, dense near the leading edge
    segs = []
    bands = [0.0] + [w for w, _ in W] + [1.0]
    ends = [0.98] + [e for _, e in W] + [1.0]
    for b in range(len(bands) - 1):
        w0, w1 = bands[b], bands[b + 1]
        s_stop = min(ends[b], ends[b + 1]) if b > 0 else 0.96
        step = 0.030 if b < 3 else 0.042
        s = 0.04 + rng.uniform(0, step)
        while s < s_stop - 0.01:
            j1 = s + rng.uniform(-0.008, 0.008)
            a, bb = pt(s, w0), pt(j1, w1)
            segs.append(f"M{a[0]:.1f},{a[1]:.1f} L{bb[0]:.1f},{bb[1]:.1f}")
            s += step * rng.uniform(0.85, 1.15)
    # trailing-edge cells: short offset ticks between the last vein and the margin
    s = 0.12
    while s < 0.95:
        a, bb = pt(s, 0.9), pt(s + 0.02, 1.0)
        segs.append(f"M{a[0]:.1f},{a[1]:.1f} L{bb[0]:.1f},{bb[1]:.1f}")
        s += 0.045
    d.path(" ".join(segs), f"{name} crossveins", fill=NONE, stroke=VEIN, strokeWidth=3,
           opacity=30, cap="round")
    # nodus and pterostigma
    a, bb = pt(0.46, 0), pt(0.46, 0.16)
    d.path(f"M{a[0]:.1f},{a[1]:.1f} L{bb[0]:.1f},{bb[1]:.1f}", f"{name} nodus", fill=NONE,
           stroke=VEIN, strokeWidth=5, opacity=80, cap="round")
    q = [pt(0.83, 0.02), pt(0.89, 0.02), pt(0.89, 0.13), pt(0.83, 0.13)]
    d.path(poly(q) + " Z", f"{name} pterostigma", fill=lin("#C89A52", "#7A5428"), stroke=VEIN,
           strokeWidth=3, opacity=90)
    # glassy sheen along the leading third
    g = [pt(0.08 + i * 0.07, 0.22) for i in range(11)]
    d.path(smooth(g, closed=False), f"{name} sheen", fill=NONE, stroke="#FFFFFF", strokeWidth=6,
           opacity=22, cap="round")
for w in WINGS[2:] + WINGS[:2]:   # hind wings under fore wings
    draw_wing(*w)

# --- legs, tucked forward under the thorax ----------------------------------------------------
for i, (x0, pts) in enumerate([(60, [(64, 34), (96, 58), (118, 50)]), (34, [(36, 38), (70, 70), (98, 70)]),
                               (8, [(8, 38), (38, 78), (66, 86)])]):
    for side in (1, -1):
        p = [L(x, y * side) for x, y in pts]
        d.path(poly(p), f"Leg {i+1} {'R' if side > 0 else 'L'}", fill=NONE, stroke="#2A2620",
               strokeWidth=5, cap="round", join="round")
        d.path(poly(p), f"Leg {i+1} {'R' if side > 0 else 'L'} sheen", fill=NONE, stroke="#9AA488",
               strokeWidth=3, cap="round", join="round", opacity=30)

# --- abdomen: ten segments, teal at the base deepening to cobalt ------------------------------
SEG = [(-36, 22), (-62, 24), (-96, 20), (-118, 13), (-158, 13), (-198, 13.5), (-238, 14),
       (-276, 14.5), (-312, 15.5), (-342, 15), (-362, 12.5), (-374, 9)]
COLS = [("#3E8A7A", "#8ED3BE"), ("#3C8494", "#8CCFE0"), ("#2F78A8", "#86C8EE"), ("#2C70A8", "#80C2EC"),
        ("#2B6AA6", "#7ABCE8"), ("#2A64A2", "#76B6E4"), ("#295E9C", "#70ADDE"), ("#2A5490", "#6A9FD2"),
        ("#2B4A82", "#5E8EC2"), ("#2C4478", "#5884B6"), ("#2E3E6C", "#5078A8")]
for i in range(len(SEG) - 1):
    (xa, wa), (xb, wb) = SEG[i], SEG[i + 1]
    xm = (xa + xb) / 2
    s = lp(f"M{xa},{-wa} C{xa+2},{-wa*0.4} {xa+2},{wa*0.4} {xa},{wa} "
           f"C{xm},{(wa+wb)/2*1.06} {xm},{(wa+wb)/2*1.06} {xb},{wb} "
           f"C{xb+2},{wb*0.4} {xb+2},{-wb*0.4} {xb},{-wb} "
           f"C{xm},{-(wa+wb)/2*1.06} {xm},{-(wa+wb)/2*1.06} {xa},{-wa} Z")
    edge, mid = COLS[i]
    d.path(s, f"Abdomen S{i+1}", fill=cross(edge, mid, L(xm, -wa), L(xm, wa, False)),
           stroke=INK, strokeWidth=3)
d.path(lp("M-100,0 C-180,0 -280,0 -362,0"), "Dorsal carina", fill=NONE, stroke="#1C2E50",
       strokeWidth=4, opacity=50, cap="round")
d.path(lp("M-60,-12 C-140,-8 -260,-8 -350,-7"), "Abdomen highlight", fill=NONE, stroke="#E6F6FF",
       strokeWidth=3, opacity=45, cap="round")
for side in (1, -1):
    d.path(lp(f"M-372,{4*side} C-382,{7*side} -392,{9*side} -400,{8*side}"),
           f"Cercus {'R' if side > 0 else 'L'}", fill=NONE, stroke="#2A3448", strokeWidth=5, cap="round")

# --- thorax: unmarked green, robust -----------------------------------------------------------
d.path(lp("M-40,-24 C-40,-46 10,-50 50,-46 C80,-42 92,-24 92,0 C92,24 80,42 50,46 "
          "C10,50 -40,46 -40,24 Z"), "Thorax", fill=cross("#2E6E2A", "#86C860", L(20, -46), L(20, 46, False)),
       stroke=INK, strokeWidth=5)
d.path(lp("M-30,-10 C0,-16 40,-18 80,-12"), "Thorax suture", fill=NONE, stroke="#2A5A26", strokeWidth=3, opacity=45, cap="round")
d.path(lp("M-30,12 C0,16 40,18 80,12"), "Thorax suture 2", fill=NONE, stroke="#2A5A26", strokeWidth=3, opacity=45, cap="round")
d.path(lell(30, -22, 38, 9), "Thorax gloss", fill="#E8FFD8", opacity=26, stroke=NONE)

# --- head: wraparound eyes and the bull's-eye on the frons ---------------------------------------
for side, nm in ((1, "R"), (-1, "L")):
    d.path(lell(110, 24 * side, 30, 31), f"Eye {nm}", fill=EYE_GRAD, stroke=INK, strokeWidth=4)
    d.path(lell(118, 30 * side, 9, 7), f"Eye glint {nm}", fill="#FFFFFF", opacity=60, stroke=NONE)
    d.path(lell(102, 16 * side, 14, 10), f"Eye facet sheen {nm}", fill="#DFF5D0", opacity=20, stroke=NONE)
d.path(lp("M126,-28 C146,-24 154,-10 154,0 C154,10 146,24 126,28 C134,10 134,-10 126,-28 Z"),
       "Frons", fill=lin("#E4EA9A", "#9CC25A"), stroke=INK, strokeWidth=3)
d.path(lell(136, 0, 8, 8), "Bull's-eye ring", fill="#4A86C0", opacity=85, stroke=NONE)
d.path(lell(136, 0, 4, 4), "Bull's-eye", fill="#1A1C24", stroke=NONE)

# --- rim drawn last so everything inside closes under it ----------------------------------------
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840, fill=NONE, stroke="#4C6D42", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F0F6E0", strokeWidth=3, opacity=40)

far = max(math.hypot(x - PCX, y - PCY) for x, y in REACH)
print(f"insect reach from disc center: {far:.0f} (inner ring 396)")
assert far < 394, far

# --- name + second line -----------------------------------------------------------------------
d.text("GREEN DARNER", "Name", x=500, y=940, size=58, font="Virelai Sans", color="#E2EFD0", justify="center")
r = d.text("ODONATA", "Second line", x=500, y=975, size=22, font="Virelai Sans",
           color="#A6C796", justify="center")
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

d.finish("green-darner-V1R00")
