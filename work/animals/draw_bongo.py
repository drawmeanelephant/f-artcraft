#!/usr/bin/env python3
"""Bongo — field-guide plate V1R00. Bust to shoulder, profile facing left:
chestnut coat with a dozen white stripes over the shoulder, long lyre horns
with one open spiral and ivory tips, big ears, white chevron, cheek spots and
chest crescent. Deep green forest plate with dappled light; the bust closes on
the disc's own arc. 1000x1000. House style: gradients + translucent shading."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Bongo — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420


def disc_x(y, side):
    return CX + side * math.sqrt(R * R - (y - CY) ** 2)


def rim_y(x):
    return CY + math.sqrt(R * R - (x - CX) ** 2)


INK = "#2E1A12"
BG_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#13261A"}, {"offset": 1, "color": "#050D08"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#6E9A58"}, {"offset": 0.6, "color": "#3F6B3E"},
    {"offset": 1, "color": "#1D3E25"}]}}
COAT_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#C8622E"}, {"offset": 0.65, "color": "#9E4420"},
    {"offset": 1, "color": "#682812"}]}}
HEAD_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#CC6830"}, {"offset": 0.7, "color": "#A44A22"},
    {"offset": 1, "color": "#6E2C14"}]}}
MUZZLE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4A2A1C"}, {"offset": 1, "color": "#24130C"}]}}
EAR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#B65628"}, {"offset": 1, "color": "#7A3218"}]}}
EAR_FAR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7E3818"}, {"offset": 1, "color": "#4E200E"}]}}
INNER_EAR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F4E6D6"}, {"offset": 1, "color": "#C9A88E"}]}}
HORN_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5A3E2C"}, {"offset": 0.5, "color": "#3A281C"},
    {"offset": 1, "color": "#22160E"}]}}
HORN_FAR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3C2A1E"}, {"offset": 1, "color": "#1A110A"}]}}
TIP_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#FFF6E2"}, {"offset": 1, "color": "#D8C49C"}]}}
STRIPE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#FFFBF2"}, {"offset": 1, "color": "#E8D8C4"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#173320", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#DCEBC0", strokeWidth=3, opacity=40)
# canopy shadows: faint leaf shapes in the upper plate
for i, (cx, cy, ln, ang) in enumerate([(230, 230, 70, -30), (300, 170, 60, 20), (720, 210, 80, 40),
                                       (790, 300, 60, -10), (180, 340, 56, 60), (660, 140, 54, -50)]):
    a = math.radians(ang)
    ux, uy = math.cos(a), math.sin(a)
    px, py = -uy, ux
    x0, y0 = cx - ux * ln / 2, cy - uy * ln / 2
    x1, y1 = cx + ux * ln / 2, cy + uy * ln / 2
    w = ln * 0.32
    d.path(f"M{x0:.1f},{y0:.1f} Q{cx + px * w:.1f},{cy + py * w:.1f} {x1:.1f},{y1:.1f} "
           f"Q{cx - px * w:.1f},{cy - py * w:.1f} {x0:.1f},{y0:.1f} Z",
           f"Leaf shadow {i+1}", fill="#163322", opacity=30, stroke=NONE)
# dappled light: soft sunflecks scattered across the plate
DAPPLES = [(170, 420, 60, 40), (240, 300, 44, 30), (330, 220, 70, 44), (420, 140, 50, 32),
           (560, 110, 46, 28), (690, 260, 64, 40), (800, 400, 50, 34), (820, 520, 40, 26),
           (210, 560, 52, 34), (150, 500, 30, 20), (260, 680, 46, 30), (760, 640, 40, 26),
           (380, 300, 30, 20), (620, 180, 34, 22), (300, 400, 26, 18)]
def blob(cx, cy, rx, ry, seed, n=9):
    pts = []
    for j in range(n):
        a = 2 * math.pi * j / n
        k = 1 + 0.28 * math.sin(seed * 2.3 + j * 1.9) + 0.12 * math.cos(seed + j * 3.1)
        pts.append((cx + rx * k * math.cos(a), cy + ry * k * math.sin(a)))
    mids = [((pts[j][0] + pts[(j + 1) % n][0]) / 2, (pts[j][1] + pts[(j + 1) % n][1]) / 2) for j in range(n)]
    dd = "M%.1f,%.1f " % mids[-1]
    for j in range(n):
        dd += "Q%.1f,%.1f %.1f,%.1f " % (pts[j][0], pts[j][1], mids[j][0], mids[j][1])
    return dd + "Z"


for i, (x, y, w, h) in enumerate(DAPPLES):
    cx, cy = x + w / 2, y + h / 2
    d.path(blob(cx, cy, w * 0.75, h * 0.75, i), f"Sunfleck glow {i+1}", fill="#E8F2A8", opacity=9, stroke=NONE)
    d.path(blob(cx, cy, w * 0.5, h * 0.5, i + 7), f"Sunfleck {i+1}", fill="#F4FAC8", opacity=17, stroke=NONE)
for i, (x, y, w) in enumerate([(140, 380, 6), (860, 360, 7), (400, 100, 6), (600, 96, 5),
                               (190, 640, 6), (840, 600, 5), (330, 120, 5), (760, 160, 6)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#1A3A22", opacity=45, stroke=NONE)

# --- horns --------------------------------------------------------------------
def cubic(p0, p1, p2, p3, t):
    u = 1 - t
    x = u**3*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t**3*p3[0]
    y = u**3*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t**3*p3[1]
    dx = 3*u*u*(p1[0]-p0[0]) + 6*u*t*(p2[0]-p1[0]) + 3*t*t*(p3[0]-p2[0])
    dy = 3*u*u*(p1[1]-p0[1]) + 6*u*t*(p2[1]-p1[1]) + 3*t*t*(p3[1]-p2[1])
    return (x, y), (dx, dy)


def ribbon(spine, w0, w1, t0, t1, twists, amp, samples):
    left, right, mid = [], [], []
    for i in range(samples + 1):
        t = t0 + (t1 - t0) * i / samples
        (x, y), (dx, dy) = cubic(*spine, t)
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy/ln, dx/ln
        w = (w0 + (w1 - w0) * t) / 2
        ph = math.sin(t * math.pi * 2 * twists)
        mid.append((x, y, nx, ny, w))
        left.append((x + nx*w*(1 + amp*ph), y + ny*w*(1 + amp*ph)))
        right.append((x - nx*w*(1 - amp*ph), y - ny*w*(1 - amp*ph)))
    dd = "M%.1f,%.1f " % left[0] + " ".join("L%.1f,%.1f" % p for p in left[1:])
    dd += " " + " ".join("L%.1f,%.1f" % p for p in reversed(right)) + " Z"
    return dd, mid


def horn(spine, w0, w1, label, fill, ridge_col, n_ridges):
    dd, mid = ribbon(spine, w0, w1, 0, 1, 1.25, 0.30, 40)
    d.path(dd, label, fill=fill, stroke=INK, strokeWidth=4)
    # keel ridges: slanted rings that suggest the single open spiral
    for j in range(n_ridges):
        t = 0.08 + 0.66 * j / (n_ridges - 1)
        x, y, nx, ny, w = mid[round(t * 40)]
        ang = math.radians(30)
        rx, ry = nx*math.cos(ang) - ny*math.sin(ang), nx*math.sin(ang) + ny*math.cos(ang)
        e = w * 0.95
        d.path("M%.1f,%.1f L%.1f,%.1f" % (x - rx*e, y - ry*e, x + rx*e, y + ry*e),
               f"{label} ridge {j+1}", fill=NONE, stroke=ridge_col, strokeWidth=3,
               opacity=70, cap="round")
    # ivory tip
    tip, _ = ribbon(spine, w0, w1, 0.80, 1, 1.25, 0.30, 10)
    d.path(tip, f"{label} tip", fill=TIP_GRAD, stroke=INK, strokeWidth=3)
    # sheen along the lit edge
    a, b, c = mid[3], mid[20], mid[30]
    k = 0.55
    d.path("M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" % (
        a[0] + a[2]*a[4]*k, a[1] + a[3]*a[4]*k, b[0] + b[2]*b[4]*k, b[1] + b[3]*b[4]*k,
        c[0] + c[2]*c[4]*k, c[1] + c[3]*c[4]*k),
        f"{label} sheen", fill=NONE, stroke="#C8A888", strokeWidth=4, opacity=35, cap="round")


horn([(514, 402), (520, 300), (700, 300), (662, 126)], 42, 9, "Horn far", HORN_FAR_GRAD, "#0E0906", 9)

# --- far ear (behind everything on the head) ------------------------------------
d.path("M528,404 C548,360 590,322 640,306 C650,330 628,380 590,410 C570,424 544,424 528,404 Z",
       "Ear far", fill=EAR_FAR_GRAD, stroke=INK, strokeWidth=4)

# --- neck + shoulder bust, closing on the disc arc --------------------------------
RX, RY = 790, rim_y(790)          # back line meets the rim
LY = 822
LX = disc_x(LY, -1)               # chest meets the rim
BACK = [(530, 414), (650, 420), (748, 560), (RX, RY)]
d.path(f"M{BACK[0][0]},{BACK[0][1]} C{BACK[1][0]},{BACK[1][1]} {BACK[2][0]},{BACK[2][1]} {RX:.1f},{RY:.1f} "
       f"A420,420 0 0 1 {LX:.1f},{LY} "
       f"C{LX + 30:.1f},{LY - 60} 340,700 380,630 "
       "C400,600 430,560 470,540 C500,500 512,450 530,414 Z",
       "Bust", fill=COAT_GRAD, stroke=INK, strokeWidth=6)
# throat shade under the jaw and a lit back line
d.path("M400,640 C440,600 500,592 560,600", "Throat shade", fill=NONE,
       stroke="#4A1C0C", strokeWidth=22, opacity=28, cap="round")
d.path("M560,430 C650,440 720,520 760,640", "Back light", fill=NONE,
       stroke="#F0A070", strokeWidth=12, opacity=22, cap="round")
d.path("M330,790 C370,740 430,720 520,730", "Chest shade", fill=NONE,
       stroke="#4A1C0C", strokeWidth=18, opacity=22, cap="round")

# white stripes: a dozen, hanging off the back line toward the rim
stripes = []
BACK_PTS = [cubic(*BACK, i / 400)[0] for i in range(401)]
for k in range(12):
    tx = 572 + k * 17.5
    bx, by = min(BACK_PTS, key=lambda p: abs(p[0] - tx))
    nx, ny = -0.30, 0.954               # mostly downward, leaning toward the chest
    sx, sy = bx - 9, by + 8
    L = 200 + 90 * math.sin(k * 1.7 + 0.4) ** 2
    ex, ey = sx + nx * L, sy + ny * L
    lim = rim_y(ex) - 26
    if ey > lim:
        s = (lim - sy) / (ey - sy)
        ex, ey = sx + (ex - sx) * s, lim
    mx, my = (sx + ex) / 2 + 12, (sy + ey) / 2
    stripes.append(((sx, sy), (mx, my), (ex, ey)))
for i, (a, m, b) in enumerate(stripes):
    vx, vy = b[0] - a[0], b[1] - a[1]
    ln = math.hypot(vx, vy)
    px, py = -vy / ln, vx / ln
    w0, w1 = 6.5, 3.0
    dd = (f"M{a[0] + px*w0:.1f},{a[1] + py*w0:.1f} Q{m[0] + px*(w0+w1)/2:.1f},{m[1] + py*(w0+w1)/2:.1f} "
          f"{b[0] + px*w1:.1f},{b[1] + py*w1:.1f} L{b[0] - px*w1:.1f},{b[1] - py*w1:.1f} "
          f"Q{m[0] - px*(w0+w1)/2:.1f},{m[1] - py*(w0+w1)/2:.1f} {a[0] - px*w0:.1f},{a[1] - py*w0:.1f} Z")
    d.path(dd, f"Stripe {i+1}", fill=STRIPE_GRAD, opacity=88, stroke=NONE)

# dorsal crest: short dark erect mane along the spine
for k in range(14):
    t = 0.10 + 0.60 * k / 13
    (x, y), (dx, dy) = cubic(*BACK, t)
    ln = math.hypot(dx, dy) or 1
    nx, ny = -dy / ln, dx / ln
    if ny > 0:
        nx, ny = -nx, -ny
    h = 14 - abs(k - 5) * 0.8
    d.path(f"M{x - nx*4:.1f},{y - ny*4:.1f} Q{x + nx*h*0.5 + dx/ln*4:.1f},{y + ny*h*0.5 + dy/ln*4:.1f} "
           f"{x + nx*h + dx/ln*6:.1f},{y + ny*h + dy/ln*6:.1f}",
           f"Crest tuft {k+1}", fill=NONE, stroke="#2A140A", strokeWidth=5, cap="round", opacity=80)

# white chest crescent at the base of the neck
d.path("M352,712 C392,690 450,684 500,694 C470,704 420,712 372,734 Z",
       "Chest crescent", fill=STRIPE_GRAD, opacity=92, stroke=NONE)

# dapples falling on the coat
for i, (x, y, w, h) in enumerate([(600, 520, 50, 30), (520, 640, 40, 24), (660, 640, 36, 22),
                                  (430, 760, 44, 26), (700, 720, 30, 18)]):
    d.shape("ellipse", f"Coat sunfleck {i+1}", x=x, y=y, width=w, height=h,
            fill="#FFE2A8", opacity=16, stroke=NONE)

# --- head ----------------------------------------------------------------------
d.path("M262,548 C268,510 320,450 380,418 C420,396 470,380 510,392 "
       "C548,404 566,440 562,488 C558,540 536,590 500,612 "
       "C460,634 380,628 330,612 C300,602 278,590 270,578 C262,570 258,560 262,548 Z",
       "Head", fill=HEAD_GRAD, stroke=INK, strokeWidth=7)
# dark muzzle and nose
d.path("M262,548 C268,522 284,506 304,498 C314,530 316,570 312,604 "
       "C300,602 278,590 270,578 C262,570 258,560 262,548 Z",
       "Muzzle", fill=MUZZLE_GRAD, opacity=70, stroke=NONE)
d.path("M262,540 C266,526 280,520 292,526 C296,540 290,556 276,560 C266,560 260,552 262,540 Z",
       "Nose", fill="#120A06", stroke=NONE)
d.shape("ellipse", "Nose glint", x=270, y=530, width=8, height=5, fill="#FFFFFF", opacity=40, stroke=NONE)
d.path("M270,580 C290,592 312,598 332,598", "Mouth", fill=NONE, stroke="#120A06", strokeWidth=4, cap="round")
d.path("M276,592 C296,604 318,610 334,610", "Lip white", fill=NONE, stroke="#F4ECE0", strokeWidth=5,
       opacity=85, cap="round")
# white chevron across the nose bridge
d.path("M330,446 C356,452 378,470 388,500 C372,486 352,474 326,468 Z",
       "Chevron upper", fill=STRIPE_GRAD, opacity=92, stroke=NONE)
# cheek spots
d.shape("ellipse", "Cheek spot 1", x=430, y=528, width=26, height=22, fill="#FBF4E8", opacity=90, stroke=NONE)
d.shape("ellipse", "Cheek spot 2", x=466, y=548, width=20, height=17, fill="#FBF4E8", opacity=85, stroke=NONE)
# jaw shade + crown light
d.path("M340,610 C400,624 460,622 500,606", "Jaw shade", fill=NONE,
       stroke="#4A1C0C", strokeWidth=14, opacity=30, cap="round")
d.path("M400,420 C440,398 490,392 520,404", "Crown light", fill=NONE,
       stroke="#F4B080", strokeWidth=10, opacity=26, cap="round")
# eye: large and dark, pale lower rim
d.shape("ellipse", "Eye ring", x=398, y=448, width=48, height=40, fill="#3A1A0C", opacity=40, stroke=NONE)
d.shape("ellipse", "Eye", x=406, y=454, width=32, height=26, fill="#1A0E08", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Eye glint", x=413, y=458, width=8, height=7, fill="#FFFFFF", opacity=88, stroke=NONE)
d.path("M404,458 C414,446 432,446 442,456", "Upper lid", fill=NONE, stroke=INK, strokeWidth=4, cap="round")
d.path("M408,484 C418,490 432,490 442,482", "Lower lid light", fill=NONE, stroke="#F4E6D6",
       strokeWidth=3, opacity=60, cap="round")

# --- near horn (over the crown) ---------------------------------------------------
horn([(476, 406), (466, 296), (660, 290), (590, 110)], 50, 10, "Horn near", HORN_GRAD, "#140C06", 10)

# --- near ear -------------------------------------------------------------------------
d.path("M522,428 C554,388 616,356 682,350 C694,376 664,428 616,452 C578,470 540,462 522,428 Z",
       "Ear near", fill=EAR_GRAD, stroke=INK, strokeWidth=5)
d.path("M540,430 C568,400 618,376 668,368 C670,394 644,424 608,440 C580,452 552,448 540,430 Z",
       "Ear near inner", fill=INNER_EAR_GRAD, opacity=85, stroke=NONE)
for i, dd in enumerate(["M556,432 C590,412 626,394 660,384", "M562,440 C596,428 628,414 654,400"]):
    d.path(dd, f"Ear hair {i+1}", fill=NONE, stroke="#B89478", strokeWidth=3, opacity=55, cap="round")
d.path("M528,426 C560,388 620,358 680,352", "Ear rim dark", fill=NONE,
       stroke="#3A1A0C", strokeWidth=4, opacity=50, cap="round")

# --- rim redrawn over the bust so the edge stays crisp ---------------------------------
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#173320", strokeWidth=6)

# --- name ----------------------------------------------------------------------------
d.text("BONGO", "Name", x=500, y=960, size=60, font="Virelai Sans",
       color="#DCEBC8", justify="center")

d.finish("bongo-V1R00")
