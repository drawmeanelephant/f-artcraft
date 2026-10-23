#!/usr/bin/env python3
"""Firefly — field plate V1R00. A lantern with legs: three-quarter dorsal,
perched on a grass blade at dusk, the light organ a warm gradient bloom inside
layered translucent halos, brown-grey elytra lifted a crack so the hind-wing
membranes show. Deep blue-green night plate. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math, re, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Firefly — Field Plate", 1000, 1000)
rng = random.Random(77)   # fixed seed: stars and specks are the same every run

PCX, PCY, PR = 500, 460, 420
INK = "#2A211C"   # warm umber, not black

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

def glow(color, peak):
    return {"gradient": {"kind": "radial", "stops": [
        {"offset": 0, "color": color, "opacity": peak},
        {"offset": 0.55, "color": color, "opacity": peak * 0.45},
        {"offset": 1, "color": color, "opacity": 0}]}}

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
    """First hit of p + t*dv (t > 0) on the disc rim."""
    fx, fy = p[0] - PCX, p[1] - PCY
    a = dv[0]**2 + dv[1]**2; b = 2*(fx*dv[0] + fy*dv[1]); c = fx*fx + fy*fy - PR*PR
    t = (-b + math.sqrt(b*b - 4*a*c)) / (2*a)
    return (p[0] + t*dv[0], p[1] + t*dv[1])

# --- the insect's own frame: x runs tail->head, y across the back ---------------------
O = (512, 440)
A = math.radians(-152)                     # head toward upper left
U = (math.cos(A), math.sin(A)); V = (-math.sin(A), math.cos(A))
REACH = []
def L(x, y, track=True):
    p = (O[0] + x*U[0] + y*V[0], O[1] + x*U[1] + y*V[1])
    if track: REACH.append(p)
    return p

def lp(s, track=True):
    """Path data written in the insect frame -> canvas path data."""
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

def circ(name, c, r, **kw):
    d.shape("ellipse", name, x=round(c[0]-r, 1), y=round(c[1]-r, 1), width=2*r, height=2*r, **kw)

# --- palette ---------------------------------------------------------------------------
BG_GRAD = lin("#071419", "#020709", [0, 0], [0, 1000])
PLATE_GRAD = rad("#285A5A", "#1A4245", "#0D272C")
BLADE_GRAD = lin("#5E8F4C", "#21402A", [0, 0], [0, 1])
ELY_GRAD = rad("#8C8174", "#625850", "#3A322C")
PRO_GRAD = rad("#FBEBB0", "#F1C886", "#D98F6E")
LANTERN_GRAD = rad("#FFFDE0", "#FBF08A", "#D6E25A")
EYE_GRAD = rad("#5C5C58", "#24201D")
WING_FILL = lin("#E9F2F0", "#BFD6D4", o0=0.30, o1=0.16)
LEG = "#3A2E27"
GLOW = "#F4F07A"

# --- backdrop, stars, distant fireflies --------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
n = 0
while n < 40:
    x, y = rng.uniform(14, 986), rng.uniform(14, 990)
    if math.hypot(x - PCX, y - PCY) < PR + 14 or (y > 900 and 230 < x < 770):
        continue
    w = rng.uniform(2, 4.5)
    d.shape("ellipse", f"Star {n+1}", x=round(x, 1), y=round(y, 1), width=round(w, 1), height=round(w, 1),
            fill="#DDE8F0", opacity=rng.randint(25, 60), stroke=NONE)
    n += 1
for i, (x, y, r) in enumerate([(52, 150, 10), (930, 120, 8), (60, 820, 9), (944, 760, 11)]):
    circ(f"Far firefly halo {i+1}", (x, y), r * 3, fill=glow(GLOW, 0.30), stroke=NONE)
    circ(f"Far firefly {i+1}", (x, y), r * 0.45, fill="#FBF6B0", opacity=85, stroke=NONE)

# --- plate ------------------------------------------------------------------------------
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840, fill=PLATE_GRAD, stroke=NONE)
d.shape("ellipse", "Plate dusk sheen", x=160, y=90, width=520, height=300,
        fill=glow("#7FB7B0", 0.16), stroke=NONE)
for i in range(16):
    while True:
        x, y = rng.uniform(150, 850), rng.uniform(90, 470)
        if math.hypot(x - PCX, y - PCY) < PR - 50:
            break
    w = rng.uniform(2.5, 4)
    d.shape("ellipse", f"Plate star {i+1}", x=round(x, 1), y=round(y, 1), width=round(w, 1), height=round(w, 1),
            fill="#E6F0EC", opacity=rng.randint(18, 40), stroke=NONE)
# fellow fireflies drifting over the meadow, each a tiny layered bloom
for i, (x, y, r) in enumerate([(232, 250, 9), (770, 300, 7), (300, 560, 6), (812, 470, 8),
                               (640, 170, 6), (190, 430, 5)]):
    circ(f"Meadow firefly halo {i+1}a", (x, y), r * 5, fill=glow(GLOW, 0.18), stroke=NONE)
    circ(f"Meadow firefly halo {i+1}b", (x, y), r * 2.2, fill=glow("#FBF6B0", 0.45), stroke=NONE)
    circ(f"Meadow firefly {i+1}", (x, y), r * 0.5, fill="#FFFDE0", opacity=90, stroke=NONE)

# --- background grass: every blade closes on the disc's own arc ---------------------------
def grass(name, a_lo, a_hi, tip, lean, fill, op):
    p0, p1 = P(a_lo), P(a_hi)
    s = (f"M{p0[0]:.1f},{p0[1]:.1f} "
         f"C{p0[0]+lean*0.2:.1f},{p0[1]-60:.1f} {tip[0]-lean*0.4:.1f},{tip[1]+80:.1f} {tip[0]:.1f},{tip[1]:.1f} "
         f"C{tip[0]-lean*0.5:.1f},{tip[1]+90:.1f} {p1[0]+lean*0.1:.1f},{p1[1]-50:.1f} {p1[0]:.1f},{p1[1]:.1f} "
         + arc_to(a_hi, a_lo) + " Z")
    d.path(s, name, fill=fill, stroke=NONE, opacity=op)
G1 = lin("#2C5E50", "#0D2422", [0, 600], [0, 880])
G2 = lin("#3A7360", "#123430", [0, 560], [0, 880])
for i, (lo, hi, tip, lean, f, o) in enumerate([
        (124, 128, (190, 610), -30, G1, 85), (116, 119, (262, 640), 20, G2, 75),
        (108, 111, (300, 700), -24, G1, 80), (99, 102, (390, 720), 30, G2, 70),
        (88, 91, (470, 760), -10, G1, 80), (78, 81, (600, 720), 28, G2, 70),
        (70, 73, (670, 690), -18, G1, 82), (60, 63, (740, 640), 26, G2, 75),
        (52, 55, (812, 600), -20, G1, 85)]):
    grass(f"Meadow grass {i+1}", lo, hi, tip, lean, f, o)

# --- the perch: one long blade running under the insect, rooted on the rim -----------------
nb = ray_circle(L(-200, -112, False), (-U[0], -U[1]))
fb = ray_circle(L(-200, -38, False), (-U[0], -U[1]))
blade = (f"M{fb[0]:.1f},{fb[1]:.1f} L{lp('M-200,-38')[1:]} "
         + lp("C-60,-40 120,-46 210,-70 C250,-82 282,-104 300,-138 "
              "C270,-118 230,-110 190,-104 C100,-102 -60,-110 -200,-112")
         .replace("M", "") + f" L{nb[0]:.1f},{nb[1]:.1f} " + arc_to(ang(nb), ang(fb)) + " Z")
d.path(blade, "Grass blade", fill=lin("#5E8F4C", "#1F3D2A", [500, 300], [800, 700]),
       stroke="#132A1E", strokeWidth=4)
d.path(lp("M-380,-76 C-200,-76 0,-76 120,-82 C200,-88 250,-104 280,-126", False), "Blade midrib",
       fill=NONE, stroke="#A6CC8A", strokeWidth=3, opacity=40, cap="round")
d.path(lp("M-380,-44 C-200,-42 0,-44 140,-52", False), "Blade edge light",
       fill=NONE, stroke="#D6F0A8", strokeWidth=3, opacity=30, cap="round")

# --- the lantern's light: layered translucent halos, widest first --------------------------
LC = L(-178, 0, False)
for i, (r, c, pk) in enumerate([(360, "#CFEA62", 0.14), (260, "#D9EE6A", 0.22), (180, "#E8F27A", 0.32),
                                (120, "#F4F28A", 0.45), (80, "#FBF6A8", 0.60)]):
    circ(f"Lantern halo {i+1}", LC, r, fill=glow(c, pk), stroke=NONE)
# warm light pooling on the blade under the tail
d.path(lp("M-260,-44 C-210,-40 -140,-40 -100,-46 L-100,-106 C-150,-110 -210,-110 -260,-108 Z", False),
       "Blade lantern wash", fill=glow("#F6F08A", 0.45), stroke=NONE)

# --- far-side legs (behind the body) -------------------------------------------------------
def leg(name, pts, w=6, op=100):
    s = "M%.1f,%.1f " % L(*pts[0]) + " ".join("L%.1f,%.1f" % L(*p) for p in pts[1:])
    d.path(s, name, fill=NONE, stroke=LEG, strokeWidth=w, cap="round", join="round", opacity=op)
    d.path(s, name + " sheen", fill=NONE, stroke="#8A7868", strokeWidth=3, cap="round",
           join="round", opacity=40)
# far legs sit in the body's shadow, so they read a step back
leg("Far foreleg", [(70, 60), (100, 100), (134, 96), (148, 84)], 5, 80)
leg("Far midleg", [(20, 66), (30, 108), (-6, 104), (-18, 90)], 5, 80)
leg("Far hindleg", [(-26, 64), (-52, 104), (-94, 98), (-106, 86)], 5, 80)

# --- hind-wing membranes, peeking out from under the lifted elytra -------------------------
def hindwing(side):
    k = side
    s = lp(f"M10,{40*k} C-50,{96*k} -150,{118*k} -214,{98*k} C-232,{90*k} -228,{70*k} -206,{62*k} "
           f"C-150,{56*k} -60,{50*k} 10,{30*k} Z")
    nm = "far" if side > 0 else "near"
    d.path(s, f"Hind wing {nm}", fill=WING_FILL, stroke="#A9C4C2", strokeWidth=3, opacity=90)
    for j, v in enumerate([f"M0,{42*k} C-70,{80*k} -150,{96*k} -208,{84*k}",
                           f"M-40,{52*k} C-100,{86*k} -160,{104*k} -200,{96*k}",
                           f"M-90,{60*k} C-120,{74*k} -150,{80*k} -180,{70*k}",
                           f"M-130,{90*k} C-138,{78*k} -140,{70*k} -136,{62*k}",
                           f"M-170,{100*k} C-176,{88*k} -178,{78*k} -172,{66*k}"]):
        d.path(lp(v), f"Hind wing {nm} vein {j+1}", fill=NONE, stroke="#D8E8E4",
               strokeWidth=3, opacity=55, cap="round")
hindwing(1)
hindwing(-1)

# --- abdomen + the light organ -------------------------------------------------------------
d.path(lp("M-60,-66 C-120,-70 -170,-64 -205,-38 C-224,-20 -224,20 -205,38 "
          "C-170,64 -120,70 -60,66 Z"), "Abdomen", fill=lin("#7A6A58", "#3B302A"), stroke=INK, strokeWidth=4)
d.path(lp("M-140,-60 C-176,-56 -200,-40 -212,-22 C-220,-8 -220,8 -212,22 "
          "C-200,40 -176,56 -140,60 C-150,30 -150,-30 -140,-60 Z"),
       "Lantern", fill=LANTERN_GRAD, stroke="#B7B14A", strokeWidth=3)
d.path(lp("M-178,-50 C-188,-20 -188,20 -178,50"), "Lantern seam", fill=NONE,
       stroke="#C8BE52", strokeWidth=3, opacity=55, cap="round")
# near flank: the underside rolling into view, glowing toward the tail
d.path(lp("M48,-62 C0,-82 -70,-90 -140,-66 L-136,-56 C-70,-76 0,-72 48,-54 Z"),
       "Near flank", fill=lin("#6B5E50", "#E8E07A", [0, 0], [1, 0]), stroke=NONE, opacity=85)

# --- elytra: lifted a crack, so the seam opens toward the tail ------------------------------
for side, nm in ((1, "far"), (-1, "near")):
    k = side
    d.path(lp(f"M40,{3*k} L-146,{16*k} C-160,{28*k} -162,{54*k} -144,{70*k} "
              f"C-104,{84*k} -24,{84*k} 40,{74*k} Z"), f"Elytron {nm}",
           fill=ELY_GRAD, stroke=INK, strokeWidth=5)
    d.path(lp(f"M36,{72*k} C-20,{82*k} -100,{82*k} -142,{66*k}"), f"Elytron margin {nm}",
           fill=NONE, stroke="#DCCB90", strokeWidth=5, opacity=80, cap="round")
    for j, yy in enumerate([24, 46]):
        d.path(lp(f"M34,{yy*k} C-30,{(yy+2)*k} -100,{(yy+6)*k} -140,{(yy+10)*k}"),
               f"Elytron ridge {nm} {j+1}", fill=NONE, stroke="#2E2621", strokeWidth=3, opacity=30, cap="round")
    d.path(lell(-40, 40*k, 72, 12), f"Elytron sheen {nm}", fill="#FFFFFF", opacity=12, stroke=NONE)
# lantern light catching the elytron tips
d.path(lell(-138, 0, 26, 52), "Elytra tip glow", fill=glow("#F6F08A", 0.5), stroke=NONE)

# --- head, eyes, antennae ------------------------------------------------------------------
for side, nm, pts in ((1, "far", "M156,16 C190,34 226,66 246,120"),
                      (-1, "near", "M156,-16 C204,-26 246,-56 274,-104")):
    d.path(lp(pts), f"Antenna {nm}", fill=NONE, stroke=LEG, strokeWidth=6, cap="round")
    d.path(lp(pts), f"Antenna {nm} segments", fill=NONE, stroke="#9C8A76", strokeWidth=3,
           dash=[4, 10], cap="round", opacity=70)
d.path(lell(138, 0, 28, 38), "Head", fill=lin("#4A3D35", "#2A221E"), stroke=INK, strokeWidth=4)
for side, nm in ((1, "far"), (-1, "near")):
    d.path(lell(146, 30*side, 17, 19), f"Eye {nm}", fill=EYE_GRAD, stroke=INK, strokeWidth=3)
    d.path(lell(152, 26*side, 5, 5), f"Eye glint {nm}", fill="#FFFFFF", opacity=70, stroke=NONE)

# --- pronotum: the shield over the head, pale and rosy with its dark saddle ----------------
d.path(lp("M36,-80 C72,-84 122,-64 140,-32 C148,-12 148,12 140,32 C122,64 72,84 36,80 "
          "C30,40 30,-40 36,-80 Z"), "Pronotum", fill=PRO_GRAD, stroke=INK, strokeWidth=5)
d.path(lp("M120,-50 C136,-30 140,-10 140,0 C140,10 136,30 120,50 C128,20 128,-20 120,-50 Z"),
       "Pronotum window", fill="#FFF8E0", opacity=35, stroke=NONE)
for side in (1, -1):
    d.path(lell(84, 30*side, 28, 14), f"Pronotum rose {'far' if side > 0 else 'near'}",
           fill="#D2564A", opacity=50, stroke=NONE)
d.path(lell(82, 0, 36, 13), "Pronotum saddle", fill=lin("#3A2C26", "#1E1714"), opacity=88, stroke=NONE)
d.path(lp("M50,-60 C80,-64 110,-50 124,-30"), "Pronotum rim light", fill=NONE,
       stroke="#FFFFFF", strokeWidth=4, opacity=30, cap="round")

# --- near-side legs (in front, gripping the blade's near edge) ------------------------------
leg("Near foreleg", [(70, -62), (104, -118), (138, -110), (150, -112)])
leg("Near midleg", [(20, -66), (34, -128), (-6, -116), (-18, -114)])
leg("Near hindleg", [(-26, -64), (-56, -128), (-100, -116), (-114, -114)])

# --- hot core of the lantern, on top of everything -----------------------------------------
circ("Lantern bloom", LC, 46, fill=glow("#FFFDE6", 0.60), stroke=NONE)
circ("Lantern core", L(-188, 0, False), 14, fill=glow("#FFFFFF", 0.85), stroke=NONE)

# --- rim drawn last so everything inside closes under it ------------------------------------
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840, fill=NONE, stroke="#3E7C78", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#9AD0C4", strokeWidth=3, opacity=30)

far = max(math.hypot(x - PCX, y - PCY) for x, y in REACH)
print(f"insect reach from disc center: {far:.0f} (inner ring 396)")
assert far < 392, far

# --- name + second line ----------------------------------------------------------------------
d.text("FIREFLY", "Name", x=500, y=940, size=58, font="Virelai Sans", color="#F1E8B0", justify="center")
r = d.text("COLEOPTERA", "Second line", x=500, y=975, size=22, font="Virelai Sans",
           color="#93C4B8", justify="center")
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

d.finish("firefly-V1R00")
