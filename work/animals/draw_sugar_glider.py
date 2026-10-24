#!/usr/bin/env python3
"""Sugar glider — field plate V1R00. Mid-glide, seen from above-behind on a
steep descent: the patagium stretched wrist to ankle into two soft wing
lobes, four limbs splayed, the huge dark eyes and the bold dorsal stripe on
the grey coat, long tail streaming behind. Gum-tree plate, moonlit-glide
mood: a smooth-barked eucalypt drops in from the upper rim at right, the
glider is off it and away down-left. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math, re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Sugar Glider — Field Plate", 1000, 1000)

INK = "#141016"
PCX, PCY, PR = 500, 460, 420          # plate disc centre + radius

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def radO(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c, "opacity": a} for o, c, a in stops]}}

def polar(r, a):
    a = math.radians(a)
    return (PCX + r * math.cos(a), PCY + r * math.sin(a))

def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

def disc_x(y, side):
    return PCX + side * math.sqrt(PR * PR - (y - PCY) ** 2)

# --- glider local frame: nose toward -y locally, rotated -130 deg so it glides
#     away down-left from the gum trunk at the upper right -------------------------
OX, OY, ANG, S = 470, 495, -130, 1.4
_c, _s = math.cos(math.radians(ANG)), math.sin(math.radians(ANG))
FAR = [0.0]

def P(x, y, dx=0, dy=0):
    px, py = OX + S * (x * _c - y * _s) + dx, OY + S * (x * _s + y * _c) + dy
    FAR[0] = max(FAR[0], math.hypot(px - PCX, py - PCY))
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
            f"C{cx-rx},{cy-ry*k} {cx-rx},{cy-ry} {cx},{cy-ry} "
            f"C{cx+rx*k},{cy-ry} {cx+rx},{cy-ry*k} {cx+rx},{cy} Z")

BG_GRAD    = lin(0, 0, 0, 1000, (0, "#0C1018"), (1, "#040507"))
PLATE_GRAD = lin(660, 80, 360, 860, (0, "#3E5A54"), (0.5, "#1B2E2C"), (1, "#0A1210"))
FUR_GRAD   = rad((0, "#A8B2BC"), (0.6, "#707A88"), (1, "#424A56"))
MEMB_GRAD  = rad((0, "#9C988C"), (0.6, "#787264"), (1, "#4C463C"))
TRUNK_GRAD = lin(700, 80, 830, 460, (0, "#8A9078"), (0.55, "#5E6850"), (1, "#39402E"))
LEAF_GRAD  = lin(0, 90, 0, 320, (0, "#7A9478"), (1, "#3E523C"))

# --- backdrop + night plate ------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
for i, (x, y, w) in enumerate([(140,130,4),(880,150,5),(110,420,3),(900,470,4),(170,700,4),(860,760,4),
                               (240,180,3),(760,90,4),(340,110,3)]):
    d.shape("ellipse", f"Sky fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#D8E2D8", opacity=35, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880, fill="#5E7A70", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#1C2A26", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C4D8C4", strokeWidth=3, opacity=40)

# moon riding upper left, glow kept inside the disc
MX, MY = 268, 216
for i, (r, op) in enumerate([(82, 8), (66, 12), (52, 18)]):
    d.shape("ellipse", f"Moon glow {i+1}", x=MX - r, y=MY - r, width=2 * r, height=2 * r,
            fill="#E8F0DC", opacity=op, stroke=NONE)
d.shape("ellipse", "Moon", x=MX - 46, y=MY - 46, width=92, height=92,
        fill=rad((0, "#FBFAE8"), (0.75, "#EDE9D0"), (1, "#C9C6AC")), stroke=NONE)
for i, (ox, oy, w) in enumerate([(-14, -10, 18), (12, 8, 13), (-4, 20, 9), (18, -16, 8)]):
    d.shape("ellipse", f"Moon mare {i+1}", x=MX + ox - w / 2, y=MY + oy - w / 2,
            width=w, height=w, fill="#B9B69C", opacity=30, stroke=NONE)

# faint stars inside the plate
for i, (x, y, w) in enumerate([(330,150,4),(470,120,5),(620,130,4),(400,200,3),
                               (560,190,4),(250,330,3),(690,240,3),(160,470,4)]):
    assert on_disc(x, y, 8), (x, y)
    d.shape("ellipse", f"Star {i+1}", x=x, y=y, width=w, height=w,
            fill="#DCE8DC", opacity=55, stroke=NONE)

# --- dark canopy band closing on the disc's lower arc -------------------------------------
CY_ = 806
cl, cr = disc_x(CY_, -1), disc_x(CY_, 1)
d.path(f"M{cl:.1f},{CY_} C320,{CY_-18} 430,{CY_-2} 520,{CY_-14} "
       f"C610,{CY_-24} 680,{CY_-8} {cr:.1f},{CY_} "
       f"A{PR},{PR} 0 0 1 {cl:.1f},{CY_} Z", "Canopy band",
       fill="#0C1810", opacity=85, stroke=NONE)
# a few leaf silhouettes pricking up off the canopy edge
for i, (lx, ly, w) in enumerate([(310, 792, 40), (520, 782, 34), (640, 786, 30)]):
    assert on_disc(lx + w / 2, ly - 18, 8), (lx, ly)
    d.path(f"M{lx},{ly} Q{lx + w / 2},{ly - 26} {lx + w},{ly - 10} "
           f"Q{lx + w / 2},{ly + 4} {lx},{ly} Z",
           f"Canopy leaf {i+1}", fill="#223A28", opacity=70, stroke=NONE)

# --- the gum trunk: a smooth-barked bole entering at the rim, running down the right ------
t_in = polar(416, -70); t_out = polar(416, -38)
d.path(f"M{t_in[0]:.1f},{t_in[1]:.1f} L{t_out[0]:.1f},{t_out[1]:.1f} "
       f"C830,262 836,352 800,456 C780,470 748,472 734,458 "
       f"C716,392 700,330 690,272 C672,204 655,142 {t_in[0]:.1f},{t_in[1]:.1f} Z",
       "Trunk", fill=TRUNK_GRAD, stroke=INK, strokeWidth=3)
# moonlit edge along the trunk's inner side
d.path("M700,290 C714,352 726,404 736,450", "Trunk moonlight", fill=NONE,
       stroke="#B8BC98", strokeWidth=4, opacity=40, cap="round")
# the stub branch the glider kicked off from, angled toward its tail
d.path("M702,332 C676,344 650,356 630,364 C624,358 622,350 630,342 "
       "C652,332 678,322 700,318 Z",
       "Branch stub", fill=TRUNK_GRAD, stroke=INK, strokeWidth=3)
# bark grain and one peeling ribbon curling off the inner edge
for i, dd in enumerate(["M716,170 C736,238 756,306 774,382",
                        "M744,160 C760,226 772,290 784,350"]):
    d.path(dd, f"Bark grain {i+1}", fill=NONE, stroke="#3A4232",
           strokeWidth=4, opacity=55, cap="round")
d.path("M712,300 C730,318 740,344 736,372 C722,366 712,348 710,326 "
       "C708,316 710,308 712,300 Z",
       "Peeling bark", fill="#A8AC88", opacity=85, stroke="#39402E", strokeWidth=2)
# hanging gum leaves off the trunk's low fork
for i, (cx, cy, a, L, w_) in enumerate([(756, 448, 60, 90, 19), (790, 430, 95, 82, 17),
                                        (726, 458, 38, 70, 16), (806, 400, 125, 66, 15),
                                        (778, 462, 74, 62, 14)]):
    r_ = math.radians(a)
    ux, uy = math.cos(r_), math.sin(r_)
    tip = (cx + ux * L, cy + uy * L)
    nx, ny = -uy, ux
    m = (cx + ux * L / 2, cy + uy * L / 2)
    assert on_disc(*tip, 8), tip
    d.path(f"M{cx},{cy} Q{m[0] + nx * w_:.1f},{m[1] + ny * w_:.1f} {tip[0]:.1f},{tip[1]:.1f} "
           f"Q{m[0] - nx * w_:.1f},{m[1] - ny * w_:.1f} {cx},{cy} Z",
           f"Gum leaf {i+1}", fill=LEAF_GRAD, opacity=80, stroke=NONE)

# --- the glider ------------------------------------------------------------------------------
# tail first: a long tapered plume streaming up-right toward the trunk
tail = ("M-8,58 C-2,96 8,130 24,158 C38,182 44,206 38,228 "
        "C52,208 50,180 38,152 C26,124 14,94 10,58 Z")
d.path(T(tail), "Tail", fill="#4E5664", stroke=INK, strokeWidth=2)
d.path(T("M-2,66 C6,100 16,132 30,158"), "Tail light", fill=NONE,
       stroke="#8A94A4", strokeWidth=4, opacity=45, cap="round")

# hind limbs: hip -> ankle, ankles flared out
for i, sgn in enumerate([-1, 1]):
    d.path(T(f"M{18*sgn},44 C{30*sgn},52 {42*sgn},48 {54*sgn},40"),
           f"Hind limb {i+1}", fill=NONE, stroke="#565E6A", strokeWidth=9, cap="round")
    # toes fanning at the ankle
    for j in (-1, 0, 1):
        ax_, ay_ = 54 * sgn, 40
        d.path(T(f"M{ax_},{ay_} L{ax_ + 12*sgn},{ay_ + 6 + j*7}"), f"Hind toes {i+1}.{j}",
               fill=NONE, stroke="#3A424E", strokeWidth=3.5, cap="round")

# the patagium: membrane lobes wrist -> outer edge -> ankle, inner edge tucked under the body
for i, sgn in enumerate([-1, 1]):
    d.path(T(f"M{52*sgn},-58 C{76*sgn},-44 {82*sgn},-8 {66*sgn},40 "
             f"C{40*sgn},30 {20*sgn},8 {12*sgn},-18 "
             f"C{16*sgn},-40 {34*sgn},-54 {52*sgn},-58 Z"),
           f"Membrane {i+1}", fill=MEMB_GRAD, opacity=92, stroke=INK, strokeWidth=2)
    # the membrane's rolled outer edge, slightly thickened
    d.path(T(f"M{52*sgn},-58 C{76*sgn},-44 {82*sgn},-8 {66*sgn},40"),
           f"Membrane edge {i+1}", fill=NONE, stroke="#3A342C", strokeWidth=5,
           opacity=80, cap="round")
    # fine creases where the membrane stretches between wrist and ankle
    d.path(T(f"M{50*sgn},-52 C{58*sgn},-26 {60*sgn},6 {58*sgn},32"),
           f"Membrane crease {i+1}", fill=NONE, stroke="#4C463C", strokeWidth=3,
           opacity=50, cap="round")

# forelimbs: shoulder -> wrist, arms thrown forward
for i, sgn in enumerate([-1, 1]):
    d.path(T(f"M{16*sgn},-44 C{28*sgn},-56 {40*sgn},-60 {52*sgn},-58"),
           f"Forelimb {i+1}", fill=NONE, stroke="#565E6A", strokeWidth=8, cap="round")
    for j in (-1, 0, 1):
        d.path(T(f"M{52*sgn},-58 L{64*sgn},{-62 + j*8}"), f"Toes {i+1}.{j}",
               fill=NONE, stroke="#3A424E", strokeWidth=3.5, cap="round")

# body: fusiform grey back
d.path(T("M-24,-70 C-30,-40 -32,0 -24,40 C-16,58 16,58 24,40 "
         "C32,0 30,-40 24,-70 C12,-80 -12,-80 -24,-70 Z"),
       "Body", fill=FUR_GRAD, stroke=INK, strokeWidth=3)
# flank shading where the membrane meets the body
for i, sgn in enumerate([-1, 1]):
    d.path(T(f"M{24*sgn},-40 C{30*sgn},-8 {30*sgn},20 {22*sgn},44"),
           f"Flank shade {i+1}", fill=NONE, stroke="#2E3640",
           strokeWidth=6, opacity=45, cap="round")
# the bold dorsal stripe nose -> tail base
d.path(T("M0,-116 C-5,-80 -6,-20 -3,50"), "Dorsal stripe", fill=NONE,
       stroke="#262A34", strokeWidth=10, opacity=80, cap="round")
d.path(T("M0,-116 C-3,-80 -4,-20 -1,50"), "Stripe light edge", fill=NONE,
       stroke="#B8C0CC", strokeWidth=3, opacity=30, cap="round")

# head: broad wedge, ears flared out
d.path(T("M-26,-76 C-34,-96 -32,-118 -18,-132 C-8,-140 8,-140 18,-132 "
         "C32,-118 34,-96 26,-76 C12,-68 -12,-68 -26,-76 Z"),
       "Head", fill=FUR_GRAD, stroke=INK, strokeWidth=3)
# ears: thin fins flared out to the sides, swept back with the glide
for i, sgn in enumerate([-1, 1]):
    d.path(T(f"M{20*sgn},-96 C{30*sgn},-104 {40*sgn},-104 {46*sgn},-96 "
             f"C{44*sgn},-86 {38*sgn},-80 {30*sgn},-78 "
             f"C{24*sgn},-82 {20*sgn},-88 {20*sgn},-96 Z"),
           f"Ear {i+1}", fill="#4C545E", stroke=INK, strokeWidth=2.5)
# the huge dark eyes with moon glints
for i, sgn in enumerate([-1, 1]):
    d.path(T(ell(13 * sgn, -106, 11, 13)), f"Eye {i+1}", fill="#10121A", stroke=NONE)
    d.path(T(ell(10 * sgn, -110, 3.5, 3.5)), f"Glint {i+1}",
           fill="#E8F0F0", opacity=85, stroke=NONE)
# small pink nose at the tip
d.path(T(ell(0, -133, 5, 4)), "Nose", fill="#C4928A", stroke=NONE)
# muzzle shade under the eyes
d.path(T(ell(0, -88, 14, 8)), "Muzzle shade", fill="#8A92A0", opacity=40, stroke=NONE)

print("farthest glider point from plate centre:", round(FAR[0], 1))

# --- name ---------------------------------------------------------------------------------------------
r1 = d.text("SUGAR GLIDER", "Name", x=500, y=962, size=58, font="Virelai Sans",
            color="#D8E2DC", justify="center")

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

d.finish("sugar-glider-V1R00")
