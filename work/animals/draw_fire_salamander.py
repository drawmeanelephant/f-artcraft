#!/usr/bin/env python3
"""Fire salamander — field plate V1R00. Warning yellow on rain-black, out on
the wettest nights: a glossy black body in an S-curve across wet beech
litter, irregular yellow bands barring its back, rain still coming down.
Beech-forest plate, drip mood. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Fire Salamander — Field Plate", 1000, 1000)
rng = random.Random(31)

CX, CY, R = 500, 460, 420          # plate disc centre + radius
INK = "#0A0C10"                    # warm dark ink, never pure black

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    ss = []
    for s in stops:
        st = {"offset": s[0], "color": s[1]}
        if len(s) > 2: st["opacity"] = s[2]
        ss.append(st)
    return {"gradient": {"kind": "radial", "stops": ss}}

def rim_x(y, r=R, side=-1):
    return CX + side * math.sqrt(r * r - (y - CY) ** 2)

def on_disc(x, y, pad=0, r=R):
    return math.hypot(x - CX, y - CY) <= r - pad

BG_GRAD    = lin(0, 0, 0, 1000, (0, "#0A1016"), (1, "#03050A"))
PLATE_GRAD = rad((0, "#4A5E6E"), (0.55, "#26333E"), (1, "#0E141C"))
SKIN_GRAD  = lin(330, 400, 680, 760, (0, "#2A3038"), (0.5, "#14181E"), (1, "#080A0E"))
FLOOR_GRAD = lin(0, 780, 0, 890, (0, "#3E3424"), (1, "#140F08"))
LEAF_GRAD  = lin(0, 700, 0, 860, (0, "#6E5E36"), (1, "#322A16"))

# --- backdrop + rain-night plate ------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=64, y=24, width=872, height=872,
        fill="#4A5E6E", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#1C2730", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#BCD0DC", strokeWidth=3, opacity=28)

# wet moon of a sky-glow, high and dim
d.shape("ellipse", "Night light", x=320, y=120, width=340, height=220,
        fill=rad((0, "#C8D8E2", 15), (0.6, "#C8D8E2", 6), (1, "#C8D8E2", 0)), stroke=NONE)

# rain: thin near-vertical streaks inside the disc, denser top half
for i in range(14):
    a = rng.uniform(0, math.tau); rr = math.sqrt(rng.uniform(0, 1)) * 360
    x, y = CX + rr * math.cos(a), CY - 40 + rr * math.sin(a) * 0.8
    if not on_disc(x, y - 26, 12): continue
    d.path(f"M{x:.0f},{y:.0f} L{x + 6:.0f},{y + 26:.0f}",
           f"Rain {i+1}", fill=NONE, stroke="#A8C4D4", strokeWidth=2.5,
           opacity=rng.uniform(14, 26), cap="round")
# droplet glints hanging in the air
for i, (x, y, w) in enumerate([(330,300,5),(560,240,4),(660,360,5),(240,470,4),
                               (450,190,4),(720,250,5),(380,640,4),(600,540,4)]):
    assert on_disc(x, y, 10), (x, y)
    d.shape("ellipse", f"Drip {i+1}", x=x, y=y, width=w, height=w*1.6,
            fill="#C8DCE8", opacity=40, stroke=NONE)

# --- wet beech litter: floor crest ~y800 closing on the disc arc -----------------
fy = 800
fdx = math.sqrt(R * R - (fy - CY) ** 2)
d.path(f"M{CX-fdx:.1f},{fy} C320,786 420,796 540,790 C640,786 720,794 {CX+fdx:.1f},{fy} "
       f"A{R},{R} 0 0 1 {CX-fdx:.1f},{fy} Z", "Floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{CX-fdx+8:.1f},{fy-2} C330,786 430,792 540,786 C640,782 720,790 {CX+fdx-8:.1f},{fy-2}",
       "Floor light", fill=NONE, stroke="#C4D2C0", strokeWidth=4, opacity=32, cap="round")

def beechleaf(x, y, L, ang, label):
    """Wet beech leaf: pointed oval with a midrib, rotated about its stem end."""
    t = math.radians(ang); ux, uy = math.cos(t), math.sin(t); nx, ny = -uy, ux
    tip = (x + ux * L, y + uy * L)
    m = (x + ux * L * 0.5, y + uy * L * 0.5)
    w = L * 0.3
    assert on_disc(*tip, 8), tip
    d.path(f"M{x},{y} Q{m[0] + nx*w:.0f},{m[1] + ny*w:.0f} {tip[0]:.0f},{tip[1]:.0f} "
           f"Q{m[0] - nx*w:.0f},{m[1] - ny*w:.0f} {x},{y} Z",
           label, fill=LEAF_GRAD, stroke=INK, strokeWidth=2.5)
    d.path(f"M{x},{y} L{tip[0]:.0f},{tip[1]:.0f}", f"{label} midrib",
           fill=NONE, stroke="#8A7648", strokeWidth=2, opacity=60, cap="round")
    d.shape("ellipse", f"{label} bead", x=m[0] + 6, y=m[1] - 4, width=7, height=5,
            fill="#DCE8EC", opacity=45, stroke=NONE)

beechleaf(255, 810, 95, -25, "Leaf 1")
beechleaf(640, 818, 85, 195, "Leaf 2")
beechleaf(450, 824, 58, 150, "Leaf 3")
# rain rings on a wet patch
for i, (x, y, w_, op) in enumerate([(340, 826, 36, 40), (340, 826, 20, 55),
                                    (660, 822, 30, 35), (660, 822, 16, 50)]):
    assert on_disc(x, y, 14), (x, y)
    d.path(f"M{x - w_},{y} C{x - w_*0.5},{y + 10} {x + w_*0.5},{y + 10} {x + w_},{y}",
           f"Rain ring {i+1}", fill=NONE, stroke="#AEC4CC", strokeWidth=2.5,
           opacity=op, cap="round")

# --- the salamander: ribbon body on a smoothed S-curve ---------------------------
SPINE = [(335, 388), (372, 448), (428, 516), (505, 578), (585, 632),
         (650, 690), (688, 742), (672, 782)]
HALF  = [26, 30, 34, 33, 27, 19, 11, 4]

def normals(pts):
    ns = []
    for i, p in enumerate(pts):
        a = pts[i - 1] if i else pts[0]
        b = pts[i + 1] if i < len(pts) - 1 else pts[-1]
        dx, dy = b[0] - a[0], b[1] - a[1]
        ln = math.hypot(dx, dy) or 1
        ns.append((-dy / ln, dx / ln))
    return ns

NS = normals(SPINE)
left  = [(p[0] + n[0] * w, p[1] + n[1] * w) for p, n, w in zip(SPINE, NS, HALF)]
right = [(p[0] - n[0] * w, p[1] - n[1] * w) for p, n, w in zip(SPINE, NS, HALF)]

def smooth(pts, close=True):
    s = f"M{pts[0][0]:.1f},{pts[0][1]:.1f} "
    for i in range(1, len(pts) - 1):
        mx, my = (pts[i][0] + pts[i + 1][0]) / 2, (pts[i][1] + pts[i + 1][1]) / 2
        s += f"Q{pts[i][0]:.1f},{pts[i][1]:.1f} {mx:.1f},{my:.1f} "
    s += f"L{pts[-1][0]:.1f},{pts[-1][1]:.1f}"
    return s + (" Z" if close else "")

# body outline: down the left flank, round the tail tip, back up the right flank
body_d = smooth(left, close=False)
body_d += f" L{right[-1][0]:.1f},{right[-1][1]:.1f} " + \
          smooth(list(reversed(right)), close=False).split(" ", 1)[1] + " Z"
d.path(body_d, "Body", fill=SKIN_GRAD, stroke=INK, strokeWidth=4)
# head: blunt wedge cap over the ribbon's front end, wider than the neck
d.path("M306,378 C310,362 326,352 344,358 C366,366 380,388 384,412 "
       "C370,426 350,432 330,424 C312,416 302,396 306,378 Z",
       "Head", fill=SKIN_GRAD, stroke=INK, strokeWidth=4)

def spine_pt(t):
    """Point + normal + halfwidth at param t in [0,1] along SPINE."""
    f = t * (len(SPINE) - 1)
    i = min(int(f), len(SPINE) - 2)
    u = f - i
    x = SPINE[i][0] + (SPINE[i + 1][0] - SPINE[i][0]) * u
    y = SPINE[i][1] + (SPINE[i + 1][1] - SPINE[i][1]) * u
    nx = NS[i][0] + (NS[i + 1][0] - NS[i][0]) * u
    ny = NS[i][1] + (NS[i + 1][1] - NS[i][1]) * u
    w = HALF[i] + (HALF[i + 1] - HALF[i]) * u
    return (x, y), (nx, ny), w

# --- legs: four short bent limbs, toes splayed -----------------------------------
def leg(t, side, reach, label):
    (x, y), (nx, ny), w = spine_pt(t)
    elbow = (x + nx * side * (w + 26), y + ny * side * (w + 26))
    wrist = (elbow[0] + nx * side * 30 + reach * 0.3, elbow[1] + ny * side * 30 + abs(reach) * 0.25)
    d.path(f"M{x:.0f},{y:.0f} L{elbow[0]:.0f},{elbow[1]:.0f} L{wrist[0]:.0f},{wrist[1]:.0f}",
           f"{label} limb", fill=NONE, stroke="#10141A", strokeWidth=11, cap="round")
    for j in (-1, 0, 1):
        d.path(f"M{wrist[0]:.0f},{wrist[1]:.0f} L{wrist[0] + nx*side*12 + j*7:.0f},{wrist[1] + ny*side*12 + 6:.0f}",
               f"{label} toe {j}", fill=NONE, stroke="#0A0E12", strokeWidth=3.5, cap="round")

leg(0.22, -1, -20, "Fore leg near")
leg(0.26, 1, 15, "Fore leg far")
leg(0.62, -1, -18, "Hind leg near")
leg(0.58, 1, 20, "Hind leg far")

# --- yellow warning bands: irregular bars across the back ------------------------
BANDS = [(0.14, 0.9, 0.0, 20), (0.26, 0.62, -0.3, 17), (0.38, 0.85, 0.1, 22),
         (0.50, 0.55, 0.4, 18), (0.61, 0.8, -0.1, 20), (0.70, 0.6, 0.35, 15),
         (0.80, 0.7, 0.0, 12), (0.89, 0.55, 0.0, 9)]
for i, (t, span, off, w_) in enumerate(BANDS):
    (x, y), (nx, ny), w = spine_pt(t)
    cx_, cy_ = x + nx * off * w, y + ny * off * w
    hl = w * span
    # slight wobble so bands read organic, not rulered
    bow = rng.uniform(-4, 4)
    d.path(f"M{cx_ - nx*hl:.0f},{cy_ - ny*hl:.0f} "
           f"Q{cx_ + bow:.0f},{cy_ + bow:.0f} {cx_ + nx*hl:.0f},{cy_ + ny*hl:.0f}",
           f"Band {i+1}", fill=NONE, stroke="#E8BE34", strokeWidth=w_, cap="round")
    d.path(f"M{cx_ - nx*hl*0.5:.0f},{cy_ - ny*hl*0.5:.0f} Q{cx_ + bow:.0f},{cy_ + bow:.0f} "
           f"{cx_ + nx*hl*0.5:.0f},{cy_ + ny*hl*0.5:.0f}",
           f"Band light {i+1}", fill=NONE, stroke="#F4D860", strokeWidth=w_*0.4,
           opacity=70, cap="round")
# parotoid patches behind the eyes + crown spots — the fire salamander's badge
for i, (x, y, w, h) in enumerate([(318, 376, 12, 20), (352, 390, 11, 17),
                                  (332, 366, 8, 8), (348, 376, 7, 7)]):
    d.shape("ellipse", f"Head spot {i+1}", x=x, y=y, width=w, height=h,
            fill="#E8BE34", opacity=92, stroke=NONE)
# tail spots between the bands
for i, (t, off) in enumerate([(0.47, -0.4), (0.57, 0.45), (0.78, -0.3)]):
    (x, y), (nx, ny), w = spine_pt(t)
    d.shape("ellipse", f"Spot {i+1}", x=x + nx*off*w - 6, y=y + ny*off*w - 6,
            width=12, height=9, fill="#E8BE34", opacity=90, stroke=NONE)

# wet sheen: long specular run along the dorsal edge + glints
sheen = " ".join(f"{'M' if i == 0 else 'L'}{p[0] + n[0]*w*0.55:.0f},{p[1] + n[1]*w*0.55:.0f}"
                 for i, (p, n, w) in enumerate(zip(SPINE[1:6], NS[1:6], HALF[1:6])))
d.path(sheen, "Wet sheen", fill=NONE, stroke="#BCD0DC", strokeWidth=6, opacity=30, cap="round")
for i, (x, y, w) in enumerate([(400, 470, 8), (500, 540, 7), (600, 620, 6)]):
    d.shape("ellipse", f"Sheen glint {i+1}", x=x, y=y, width=w, height=w*0.6,
            fill="#E8F0F4", opacity=50, stroke=NONE)

# glossy eyes on the head's flanks
for i, (ex, ey) in enumerate([(322, 380), (358, 398)]):
    d.shape("ellipse", f"Eye {i+1}", x=ex - 8, y=ey - 8, width=16, height=15,
            fill="#0A0C10", stroke=INK, strokeWidth=2)
    d.shape("ellipse", f"Eye glint {i+1}", x=ex - 4, y=ey - 5, width=5, height=5,
            fill="#E8F0F4", opacity=90, stroke=NONE)

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#060A0E", strokeWidth=6)

# --- name ----------------------------------------------------------------------
r1 = d.text("FIRE SALAMANDER", "Name", x=500, y=962, size=56, font="Virelai Sans",
            color="#C8D4DC", justify="center")

def find(o, oid):
    if isinstance(o, dict):
        if o.get("id") == oid and "bounds" in o: return o
        o = list(o.values())
    if isinstance(o, list):
        for v in o:
            hit = find(v, oid)
            if hit: return hit
layers = d.call("inspect_document", {}, "inspect")["layers"]
b = find(layers, r1["id"])["bounds"]
print("name bounds", {k: round(v) for k, v in b.items()})
assert b["width"] <= 800 and b["x"] >= 100 and b["y"] + b["height"] <= 990, b

d.finish("fire-salamander-V1R00")
