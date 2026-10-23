#!/usr/bin/env python3
"""Colugo — field-guide plate V1R00. Full-body spread mid-glide, seen from
above: the patagium stretched chin -> fingertips -> toes -> tail tip like a
fur-lined kite, mottled grey-brown, tiny splayed hands and feet. Night
canopy plate: dark leaf band closing on the disc arc, pale moon in the gap.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os, math, re, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Colugo — Field Plate", 1000, 1000)

INK = "#1B1612"
CX, CY, R = 500, 460, 420          # plate disc centre + radius
random.seed(60)

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def polar(r, a):
    a = math.radians(a)
    return (CX + r*math.cos(a), CY + r*math.sin(a))

# --- colugo frame: drawn in a local frame (head toward -y), rotated into the plate
OX, OY, ANG, S = 488, 486, -20, 1.0
_c, _s = math.cos(math.radians(ANG)), math.sin(math.radians(ANG))
FAR = [0.0]

def P(x, y, dx=0, dy=0):
    px, py = OX + S*(x*_c - y*_s) + dx, OY + S*(x*_s + y*_c) + dy
    FAR[0] = max(FAR[0], math.hypot(px - CX, py - CY))
    return px, py

def T(dd, dx=0, dy=0):
    """Map an absolute local path (M/L/C/Q/Z only) into plate coordinates."""
    out, nums = [], []
    for t in re.findall(r"[A-Za-z]|-?\d*\.?\d+", dd):
        if t.isalpha():
            out.append(t)
        else:
            nums.append(float(t))
            if len(nums) == 2:
                x, y = P(*nums, dx, dy); out.append(f"{x:.1f},{y:.1f}"); nums = []
    return " ".join(out)

def ell(cx, cy, rx, ry):
    k = 0.5523
    return (f"M{cx+rx},{cy} C{cx+rx},{cy+ry*k} {cx+rx*k},{cy+ry} {cx},{cy+ry} "
            f"C{cx-rx*k},{cy+ry} {cx-rx},{cy+ry*k} {cx-rx},{cy} "
            f"C{cx-rx},{cy-ry*k} {cx-rx*k},{cy-ry} {cx},{cy-ry} "
            f"C{cx+rx*k},{cy-ry} {cx+rx},{cy-ry*k} {cx+rx},{cy} Z")

def cubic(p0, p1, p2, p3, t):
    u = 1 - t
    return (u**3*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t**3*p3[0],
            u**3*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t**3*p3[1])

BG_GRAD = lin(0, 0, 0, 1000, (0, "#0C1414"), (1, "#030606"))
PLATE_GRAD = lin(600, 60, 380, 880, (0, "#3E5A62"), (0.45, "#1B2E30"), (1, "#0A1313"))
MOON_GRAD = rad((0, "#FFFDF0"), (0.75, "#EEEAD2"), (1, "#CFCCB2"))
CANOPY_BACK = lin(0, 40, 0, 880, (0, "#132520"), (1, "#081210"))
CANOPY_FRONT = lin(0, 40, 0, 880, (0, "#22392C"), (1, "#0F1C15"))
LEAF_GRAD = lin(0, 80, 0, 600, (0, "#2E4A38"), (1, "#16271D"))
MEMBRANE = rad((0, "#A29480"), (0.55, "#7B6E5E"), (1, "#51463B"))
BODY = rad((0, "#A69884"), (0.7, "#7E715F"), (1, "#5A4E40"))
HEAD = rad((0, "#B0A28C"), (0.7, "#867864"), (1, "#5E5243"))
LIMB = "#3E342A"

# --- backdrop + night plate ------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
for i, (x, y, w) in enumerate([(110,150,4),(880,110,5),(50,500,4),(950,430,4),(120,880,4),(890,880,5),(30,740,3),(960,700,4)]):
    d.shape("ellipse", f"Sky fleck {i+1}", x=x, y=y, width=w, height=w, fill="#D8E2D6", opacity=30, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#2F4644", strokeWidth=6)

# moon in the canopy gap (glow kept inside the disc)
MX, MY = polar(298, -75)
for i, (r, op) in enumerate([(104, 7), (84, 10), (66, 16)]):
    d.shape("ellipse", f"Moon glow {i+1}", x=MX-r, y=MY-r, width=2*r, height=2*r,
            fill="#E8F0DC", opacity=op, stroke=NONE)
d.shape("ellipse", "Moon", x=MX-44, y=MY-44, width=88, height=88, fill=MOON_GRAD, stroke=NONE)
for i, (ox, oy, w) in enumerate([(-14,-10,18),(10,8,13),(-4,18,9),(16,-16,8)]):
    d.shape("ellipse", f"Moon mare {i+1}", x=MX+ox-w/2, y=MY+oy-w/2, width=w, height=w,
            fill="#B9B69C", opacity=35, stroke=NONE)
# stars in the gap
for i in range(16):
    a, r = random.uniform(-118, -36), random.uniform(170, 370)
    x, y = polar(r, a)
    if math.hypot(x - MX, y - MY) < 112:
        continue
    w = random.choice([3, 3, 4, 5])
    d.shape("ellipse", f"Star {i+1}", x=x-w/2, y=y-w/2, width=w, height=w,
            fill="#F2F4E6", opacity=random.choice([55, 70, 85]), stroke=NONE)

# --- canopy bands: outer edge rides the disc arc, inner edge is leafy lobes --------------
def band(a0, a1, base, depth, lobes, seed):
    rnd = random.Random(seed)
    span = a1 - a0
    def rv(a):
        w = min(1.0, min(a - a0, a1 - a) / 8.0)
        return R - w*(R - base), w
    p0, p1 = polar(R, a0), polar(R, a1)
    dd = f"M{p0[0]:.1f},{p0[1]:.1f} A{R},{R} 0 {1 if span > 180 else 0} 1 {p1[0]:.1f},{p1[1]:.1f}"
    edge = []
    for k in range(lobes):
        aa, ab = a1 - span*k/lobes, a1 - span*(k + 1)/lobes
        am = (aa + ab) / 2
        r_m, w = rv(am)
        r_b, _ = rv(ab)
        cpt = polar(r_m - depth*w*rnd.uniform(0.7, 1.3), am)
        # round the band's two ends into a leafy cap that leans into the gap
        if k == 0:
            cpt = polar((R + r_b)/2 - 10, a1 + 7)
        elif k == lobes - 1:
            cpt = polar((R + rv(aa)[0])/2 - 10, a0 - 7)
        ept = polar(r_b, ab)
        edge.append((am, cpt, ept))
        dd += f" Q{cpt[0]:.1f},{cpt[1]:.1f} {ept[0]:.1f},{ept[1]:.1f}"
    return dd + " Z", edge

back, _ = band(-22, 232, 296, 56, 26, 1)
d.path(back, "Canopy back", fill=CANOPY_BACK, stroke=NONE)
front, edge = band(-28, 238, 340, 52, 28, 2)
d.path(front, "Canopy front", fill=CANOPY_FRONT, stroke=NONE)
# moonlit leaf rims near the gap
for side, (lo, hi) in enumerate([(-30, 30), (180, 240)]):
    seg = [e for e in edge if lo <= e[0] <= hi]
    seg.sort(key=lambda e: e[0])
    for j, (am, cpt, ept) in enumerate(seg[:-1]):
        nxt = seg[j + 1]
        d.path(f"M{ept[0]:.1f},{ept[1]:.1f} Q{nxt[1][0]:.1f},{nxt[1][1]:.1f} {nxt[2][0]:.1f},{nxt[2][1]:.1f}"
               if False else
               f"M{cpt[0]:.1f},{cpt[1]:.1f} Q{(cpt[0]+ept[0])/2:.1f},{(cpt[1]+ept[1])/2:.1f} {ept[0]:.1f},{ept[1]:.1f}",
               f"Leaf rim {side+1}-{j+1}", fill=NONE, stroke="#7C9C82",
               strokeWidth=3, opacity=28, cap="round")

def leaf(cx, cy, ln, ang, w, label, fill, op=100):
    t = math.radians(ang); ux, uy = math.cos(t), math.sin(t); nx, ny = -uy, ux
    tip = (cx + ux*ln, cy + uy*ln)
    a = (cx + ux*ln*0.45 + nx*w, cy + uy*ln*0.45 + ny*w)
    b = (cx + ux*ln*0.45 - nx*w, cy + uy*ln*0.45 - ny*w)
    d.path(f"M{cx:.1f},{cy:.1f} Q{a[0]:.1f},{a[1]:.1f} {tip[0]:.1f},{tip[1]:.1f} "
           f"Q{b[0]:.1f},{b[1]:.1f} {cx:.1f},{cy:.1f} Z", label, fill=fill, stroke=NONE, opacity=op)
    d.path(f"M{cx:.1f},{cy:.1f} L{cx+ux*ln*0.8:.1f},{cy+uy*ln*0.8:.1f}", f"{label} vein",
           fill=NONE, stroke="#0A140F", strokeWidth=3, opacity=40, cap="round")

# twigs reaching out of the canopy into the moon gap, leaves alternating along them
n = 0
for ti, (a0, r0, a1, r1, bend) in enumerate([(-12, 380, -40, 330, -30), (224, 380, 254, 300, -40)]):
    p0, p1 = polar(r0, a0), polar(r1, a1)
    pm = polar((r0 + r1)/2 + bend, (a0 + a1)/2)
    d.path(f"M{p0[0]:.1f},{p0[1]:.1f} Q{pm[0]:.1f},{pm[1]:.1f} {p1[0]:.1f},{p1[1]:.1f}",
           f"Twig {ti+1}", fill=NONE, stroke="#1A2A20", strokeWidth=5, cap="round")
    for k in range(6):
        t = 0.2 + 0.8*k/5
        x = (1-t)**2*p0[0] + 2*(1-t)*t*pm[0] + t*t*p1[0]
        y = (1-t)**2*p0[1] + 2*(1-t)*t*pm[1] + t*t*p1[1]
        tx = 2*(1-t)*(pm[0]-p0[0]) + 2*t*(p1[0]-pm[0])
        ty = 2*(1-t)*(pm[1]-p0[1]) + 2*t*(p1[1]-pm[1])
        base = math.degrees(math.atan2(ty, tx))
        n += 1
        leaf(x, y, 40 - k*2, base + (48 if k % 2 else -48), 11, f"Gap leaf {n}", LEAF_GRAD)
        if k == 5:
            n += 1
            leaf(x, y, 36, base, 10, f"Gap leaf {n}", LEAF_GRAD)
# lighter leaf texture scattered on the band
for i in range(30):
    a = random.uniform(-20, 232); r = random.uniform(350, 378)
    x, y = polar(r, a)
    leaf(x, y, 26, a + 180 + random.uniform(-40, 40), 7, f"Band leaf {i+1}", "#3C5A45", 45)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#B8CCC0", strokeWidth=3, opacity=30)

# --- colugo ----------------------------------------------------------------------------------
# right half of the patagium, top-centre clockwise to the tail tip
SEGS = [((12, -180), (60, -204), (170, -204), (250, -152)),    # propatagium -> wrist
        ((250, -152), (186, -66), (186, 70), (236, 160)),       # plagiopatagium -> ankle
        ((236, 160), (150, 168), (60, 214), (12, 270)),         # uropatagium -> tail
        ((12, 270), (7, 278), (3, 284), (0, 290))]
mir = lambda p: (-p[0], p[1])
LSEGS = [(mir(s[3]), mir(s[2]), mir(s[1]), mir(s[0])) for s in reversed(SEGS)]
f2 = lambda p: f"{p[0]},{p[1]}"
MEM = f"M{f2(SEGS[0][0])} " + " ".join(f"C{f2(s[1])} {f2(s[2])} {f2(s[3])}" for s in SEGS + LSEGS) \
      + f" Q0,-168 {f2(SEGS[0][0])} Z"
poly = [cubic(*s, i/24) for s in SEGS + LSEGS for i in range(24)]

def inside(x, y):
    c = False
    for i in range(len(poly)):
        (x1, y1), (x2, y2) = poly[i], poly[i - 1]
        if (y1 > y) != (y2 > y) and x < (x2 - x1)*(y - y1)/(y2 - y1) + x1:
            c = not c
    return c

def edge_dist(x, y):
    return min(math.hypot(x - px, y - py) for px, py in poly)

d.path(T(MEM, 16, 24), "Glide shade", fill="#020404", opacity=32, stroke=NONE)
d.path(T(MEM), "Fur halo", fill=NONE, stroke="#B8AA92", strokeWidth=12, opacity=22)
d.path(T(MEM), "Patagium", fill=MEMBRANE, stroke=INK, strokeWidth=4)
# moonlight falls from the upper right: lift that side, sink the far corner
d.path(T(MEM), "Patagium light", fill=lin(*P(160, -200), *P(-200, 200),
       (0, "#E9E6D2"), (0.5, "#8C806E"), (1, "#1E1812")), opacity=30, stroke=NONE)

# mottling: irregular translucent blots, kept off the rim
def blot(cx, cy, r, rnd):
    pts = []
    for k in range(7):
        a = 2*math.pi*k/7 + rnd.uniform(-0.2, 0.2)
        rr = r*rnd.uniform(0.6, 1.15)
        pts.append((cx + rr*math.cos(a), cy + rr*0.8*math.sin(a)))
    mids = [((pts[k][0] + pts[k-1][0])/2, (pts[k][1] + pts[k-1][1])/2) for k in range(7)]
    dd = f"M{mids[0][0]:.1f},{mids[0][1]:.1f}"
    for k in range(7):
        m2 = mids[(k + 1) % 7]
        dd += f" Q{pts[k][0]:.1f},{pts[k][1]:.1f} {m2[0]:.1f},{m2[1]:.1f}"
    return dd + " Z"

rnd = random.Random(7)
placed = 0
while placed < 78:
    x, y = rnd.uniform(-240, 240), rnd.uniform(-185, 280)
    r = rnd.uniform(7, 19)
    if not inside(x, y) or edge_dist(x, y) < r + 7:
        continue
    placed += 1
    dark = rnd.random() < 0.6
    d.path(T(blot(x, y, r, rnd)), f"Mottle {placed}",
           fill="#3A3026" if dark else "#C8BDA8",
           opacity=rnd.choice([30, 38, 46]) if dark else rnd.choice([22, 28, 34]), stroke=NONE)

# membrane stretch creases fanning from the flanks
for i, (a, b) in enumerate([((52, -70), (196, -60)), ((54, -10), (192, 10)), ((46, 50), (196, 90)),
                            ((34, 100), (150, 182)), ((16, 130), (56, 226))]):
    for sx in (1, -1):
        d.path(T(f"M{a[0]*sx},{a[1]} Q{(a[0]+b[0])/2*sx},{(a[1]+b[1])/2 + 8} {b[0]*sx},{b[1]}"),
               f"Crease {i+1}{'R' if sx > 0 else 'L'}", fill=NONE, stroke="#2E261E",
               strokeWidth=3, opacity=16, cap="round")

# fur fringe along the trailing edges (sides + tail membrane)
nf = 0
for s in [SEGS[1], SEGS[2], LSEGS[1], LSEGS[2]]:
    for i in range(1, 16):
        t = i/16 + rnd.uniform(-0.015, 0.015)
        x, y = cubic(*s, t)
        x2, y2 = cubic(*s, t + 0.01)
        tx, ty = x2 - x, y2 - y; ln = math.hypot(tx, ty) or 1
        nx, ny = -ty/ln, tx/ln
        if nx*x + ny*(y - 40) < 0:
            nx, ny = -nx, -ny
        nf += 1
        L = rnd.uniform(4, 8)
        d.path(T(f"M{x - nx*2:.1f},{y - ny*2:.1f} L{x + nx*L:.1f},{y + ny*L:.1f}"), f"Fringe {nf}",
               fill=NONE, stroke="#8C7E6A", strokeWidth=3, opacity=24, cap="round")

# limb bones under the skin: shoulder -> wrist, hip -> ankle
for sx, tag in [(1, "R"), (-1, "L")]:
    d.path(T(f"M{40*sx},-112 Q{150*sx},-112 {244*sx},-150"), f"Arm {tag}", fill=NONE,
           stroke=LIMB, strokeWidth=10, opacity=40, cap="round")
    d.path(T(f"M{42*sx},-120 Q{150*sx},-122 {238*sx},-158"), f"Arm light {tag}", fill=NONE,
           stroke="#C9BCA6", strokeWidth=3, opacity=30, cap="round")
    d.path(T(f"M{34*sx},88 Q{130*sx},114 {230*sx},158"), f"Leg {tag}", fill=NONE,
           stroke=LIMB, strokeWidth=10, opacity=40, cap="round")

# tiny splayed hands and feet with pale claws
def digits(cx, cy, base_ang, spread, ln, tag):
    d.path(T(ell(cx, cy, 9, 8)), f"{tag} palm", fill="#5A4D3E", stroke=INK, strokeWidth=3)
    for k, da in enumerate(spread):
        a = math.radians(base_ang + da)
        ex, ey = cx + math.cos(a)*ln, cy + math.sin(a)*ln
        d.path(T(f"M{cx},{cy} L{ex:.1f},{ey:.1f}"), f"{tag} digit {k+1}", fill=NONE,
               stroke="#4A3E32", strokeWidth=4, cap="round")
        cx2, cy2 = ex + math.cos(a)*6, ey + math.sin(a)*6
        d.path(T(f"M{ex:.1f},{ey:.1f} L{cx2:.1f},{cy2:.1f}"), f"{tag} claw {k+1}", fill=NONE,
               stroke="#E9E0CC", strokeWidth=3, cap="round")

for sx, tag in [(1, "R"), (-1, "L")]:
    base = -30 if sx > 0 else 210
    digits(252*sx, -152, base, [-52, -26, 0, 24, 48], 20, f"Hand {tag}")
    base = 28 if sx > 0 else 152
    digits(238*sx, 162, base, [-44, -20, 4, 28, 52], 18, f"Foot {tag}")

# tail inside the uropatagium
d.path(T("M-12,118 C-10,170 -5,230 0,282 C5,230 10,170 12,118 Z"), "Tail",
       fill=lin(*P(0, 118), *P(0, 282), (0, "#6A5D4D"), (1, "#3A3026")), opacity=80, stroke=NONE)

# body
d.path(T("M0,-170 C36,-170 64,-140 66,-92 C68,-36 56,24 40,66 C30,92 16,104 0,106 "
         "C-16,104 -30,92 -40,66 C-56,24 -68,-36 -66,-92 C-64,-140 -36,-170 0,-170 Z", -8, 12),
       "Body cast shadow", fill="#1A140F", opacity=30, stroke=NONE)
d.path(T("M0,-170 C36,-170 64,-140 66,-92 C68,-36 56,24 40,66 C30,92 16,104 0,106 "
         "C-16,104 -30,92 -40,66 C-56,24 -68,-36 -66,-92 C-64,-140 -36,-170 0,-170 Z"),
       "Body", fill=BODY, stroke="#3A3026", strokeWidth=3)
d.path(T("M0,-156 C8,-96 8,30 0,96"), "Dorsal shade", fill=NONE, stroke="#3E342A",
       strokeWidth=18, opacity=20, cap="round")
d.path(T("M30,-150 C48,-120 52,-70 48,-20"), "Body light", fill=NONE, stroke="#E6DCC6",
       strokeWidth=8, opacity=22, cap="round")
for i, dd in enumerate(["M-30,-120 C-38,-90 -42,-60 -42,-30", "M30,-120 C38,-90 42,-60 42,-30",
                        "M-40,0 C-40,30 -36,56 -28,78", "M40,0 C40,30 36,56 28,78",
                        "M-14,-60 L-18,-34", "M14,-40 L18,-14", "M-12,40 L-15,62", "M12,58 L15,80"]):
    d.path(T(dd), f"Body fur {i+1}", fill=NONE, stroke="#4A3F33", strokeWidth=3, opacity=40, cap="round")
for i, (x, y, r) in enumerate([(-26,-40,9),(24,-82,8),(26,24,10),(-20,56,8),(10,-130,7)]):
    d.path(T(blot(x, y, r, rnd)), f"Body mottle {i+1}", fill="#3A3026", opacity=30, stroke=NONE)

# head: small round ears, big night eyes, short muzzle
for sx, tag in [(1, "R"), (-1, "L")]:
    d.path(T(ell(36*sx, -178, 12, 10)), f"Ear {tag}", fill=HEAD, stroke=INK, strokeWidth=4)
    d.path(T(ell(36*sx, -178, 6, 5)), f"Ear inner {tag}", fill="#3A3026", opacity=60, stroke=NONE)
d.path(T("M0,-252 C18,-252 30,-238 40,-222 C50,-206 50,-178 36,-166 "
         "C24,-156 -24,-156 -36,-166 C-50,-178 -50,-206 -40,-222 C-30,-238 -18,-252 0,-252 Z"),
       "Head", fill=HEAD, stroke=INK, strokeWidth=5)
d.path(T(ell(0, -238, 15, 12)), "Muzzle light", fill="#E2D8C4", opacity=30, stroke=NONE)
d.path(T("M-30,-180 C-14,-170 14,-170 30,-180"), "Nape shade", fill=NONE, stroke="#3E342A",
       strokeWidth=6, opacity=30, cap="round")
for sx, tag in [(1, "R"), (-1, "L")]:
    d.path(T(ell(23*sx, -212, 17, 17)), f"Eye ring {tag}", fill="#2E261E", opacity=45, stroke=NONE)
    d.path(T(ell(23*sx, -212, 12, 13)), f"Eye {tag}",
           fill=rad((0, "#3A2A1C"), (0.7, "#160F0A"), (1, "#050302")), stroke=INK, strokeWidth=2)
    d.path(T(ell(23*sx + 4, -217, 4, 4)), f"Eye glint {tag}", fill="#F4F6EA", opacity=90, stroke=NONE)
    d.path(T(ell(23*sx - 4, -207, 2, 2)), f"Eye glint small {tag}", fill="#F4F6EA", opacity=60, stroke=NONE)
d.path(T(ell(0, -249, 6, 4)), "Nose", fill="#1A120C", stroke=NONE)
d.path(T("M-8,-242 Q0,-238 8,-242"), "Mouth", fill=NONE, stroke=INK, strokeWidth=3, opacity=70, cap="round")

# moonlight: the leading edges face the moon
d.path(T("M18,-182 C72,-196 166,-176 232,-138"), "Moon rim R", fill=NONE, stroke="#EEF2DE",
       strokeWidth=4, opacity=50, cap="round")
d.path(T("M-18,-182 C-72,-196 -166,-176 -232,-138"), "Moon rim L", fill=NONE, stroke="#EEF2DE",
       strokeWidth=3, opacity=28, cap="round")
d.path(T("M232,-120 C210,-50 214,50 228,140"), "Moon rim side", fill=NONE, stroke="#EEF2DE",
       strokeWidth=3, opacity=22, cap="round")
d.path(T("M-20,-244 C-6,-252 10,-252 26,-240"), "Head rim light", fill=NONE, stroke="#F4F6EA",
       strokeWidth=3, opacity=55, cap="round")
d.path(T("M-30,-150 C-6,-160 20,-158 44,-140"), "Shoulder rim light", fill=NONE, stroke="#EEF2DE",
       strokeWidth=3, opacity=30, cap="round")

print(f"colugo max radius from disc centre: {FAR[0]:.1f} (rim {R})")

# --- name -----------------------------------------------------------------------------------
d.text("COLUGO", "Name", x=500, y=962, size=58, font="Virelai Sans",
       color="#DCE6D6", justify="center")

d.finish("colugo-V1R00")
