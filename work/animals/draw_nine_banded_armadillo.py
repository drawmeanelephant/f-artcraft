#!/usr/bin/env python3
"""Nine-banded armadillo — field plate V1R00. Dasypus novemcinctus side view,
facing left, caught at the apex of its notorious vertical leap: nine banded
strips between the shoulder and hip shields, feet tucked clear of the
ground, ringed tail streaming, dust burst rising off the desert floor.
Desert tan plate, scrub-dry mood.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Nine-banded Armadillo — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420          # plate disc centre + radius
INK = "#4A2C16"
rng = random.Random(554)

def on_disc(x, y, pad):
    return math.hypot(x - CX, y - CY) <= R - pad

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rim(y):
    dx = math.sqrt(R * R - (y - CY) ** 2)
    return CX - dx, CX + dx

def ground(label, yl, yr, mid, fill, **kw):
    """Band whose top runs rim-to-rim through `mid` (C-curve control pairs)
    and whose bottom closes on the disc's own arc."""
    xl, _ = rim(yl); _, xr = rim(yr)
    big = 1 if (yl + yr) / 2 < CY else 0
    dd = f"M{xl:.1f},{yl} " + mid.format(xr=f"{xr:.1f},{yr}") + \
         f" A{R},{R} 0 {big} 1 {xl:.1f},{yl} Z"
    d.path(dd, label, fill=fill, stroke=NONE, **kw)

def qpt(p0, p1, p2, t):
    u = 1 - t
    return (u*u*p0[0] + 2*u*t*p1[0] + t*t*p2[0], u*u*p0[1] + 2*u*t*p1[1] + t*t*p2[1])

def qtan(p0, p1, p2, t):
    u = 1 - t
    return (2*u*(p1[0]-p0[0]) + 2*t*(p2[0]-p1[0]), 2*u*(p1[1]-p0[1]) + 2*t*(p2[1]-p1[1]))

BG_GRAD = lin(0, 0, 0, 1000, (0, "#2A1D10"), (1, "#0F0804"))
PLATE_GRAD = rad((0, "#F2DDB2"), (0.62, "#DFBD85"), (1, "#B9895A"))
DUNE_GRAD = lin(0, 520, 0, 660, (0, "#D8AE74"), (1, "#B98A52"))
SOIL_GRAD = lin(0, 672, 0, 880, (0, "#C9A068"), (0.5, "#A67844"), (1, "#7C5128"))
SKIN_GRAD = lin(300, 480, 640, 640, (0, "#E4B48E"), (0.6, "#C98F66"), (1, "#A06B44"))
SKIN_DARK = lin(300, 480, 640, 660, (0, "#B97F56"), (1, "#8A5634"))
SHELL_A = lin(0, 390, 0, 582, (0, "#E4C894"), (0.45, "#C6A06C"), (1, "#96714A"))
SHELL_B = lin(0, 390, 0, 582, (0, "#DDBE88"), (0.45, "#B8915C"), (1, "#87633E"))
SHIELD_GRAD = lin(0, 395, 0, 582, (0, "#D9B781"), (0.5, "#B28A58"), (1, "#8A643C"))
HEAD_GRAD = lin(230, 470, 380, 580, (0, "#E2B28A"), (0.55, "#C68E62"), (1, "#9C6A42"))
FUR = "#E8D2AE"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
for i, (x, y, w) in enumerate([(110,150,4),(880,110,5),(52,470,4),(948,420,4),(120,880,4),(890,872,5),(30,720,3),(962,690,4)]):
    d.shape("ellipse", f"Sky fleck {i+1}", x=x, y=y, width=w, height=w, fill="#F0D6B0", opacity=28, stroke=NONE)
d.shape("ellipse", "Plate halo", x=64, y=24, width=872, height=872, fill="#D8A860", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840, fill=PLATE_GRAD, stroke=NONE)

# low scrubland sun + haze
d.shape("ellipse", "Sun halo", x=208, y=168, width=200, height=200, fill="#FFF2D8", opacity=26, stroke=NONE)
d.shape("ellipse", "Sun", x=252, y=212, width=112, height=112,
        fill=rad((0, "#FFFAEA"), (1, "#F2D3A0")), opacity=88, stroke=NONE)
for i, (x, y, w, h) in enumerate([(560,196,250,24),(190,330,210,18),(630,304,180,15)]):
    assert on_disc(x + w / 2, y, 24), (x, y)
    d.shape("ellipse", f"Haze {i+1}", x=x, y=y, width=w, height=h, fill="#FFFFFF", opacity=20, stroke=NONE)

# far dune band, closing on the disc arc
ground("Dune far", 566, 548, "C240,548 360,530 520,552 C650,568 760,540 {xr}", DUNE_GRAD, opacity=80)
d.path("M232,556 C330,540 430,540 520,552", "Dune crest light", fill=NONE, stroke="#FFF0D2",
       strokeWidth=4, opacity=50, cap="round")
# distant scrub silhouettes on the dune
for i, (x, y, s) in enumerate([(706, 548, 1.0), (240, 560, 0.8), (640, 556, 0.7)]):
    for k, dx in enumerate([-10, -5, 0, 5, 10]):
        d.path(f"M{x},{y} Q{x+dx*0.5*s},{y-12*s} {x+dx*s},{y-20*s+abs(dx)*0.6}",
               f"Far scrub {i+1}-{k+1}", fill=NONE, stroke="#8A6438",
               strokeWidth=3, opacity=55, cap="round")

# --- desert floor, closing on the disc arc -------------------------------------
ground("Soil", 706, 686, "C180,690 300,682 420,692 C560,702 680,682 780,688 C810,690 830,688 {xr}", SOIL_GRAD)
# leaping shadow on the soil
d.shape("ellipse", "Leap shadow", x=338, y=700, width=300, height=34, fill="#5E3A1C",
        opacity=22, stroke=NONE)
# sand ripples + speckle, all inside the disc
for i, dd in enumerate(["M196,736 C290,724 380,728 460,738", "M520,742 C610,732 700,734 780,744",
                        "M240,788 C330,778 420,782 500,790", "M560,800 C640,792 710,794 770,802",
                        "M300,842 C380,834 460,836 540,844"]):
    d.path(dd, f"Ripple {i+1}", fill=NONE, stroke="#8A5E30", strokeWidth=3, opacity=35, cap="round")
for i in range(20):
    x, y = rng.uniform(190, 800), rng.uniform(716, 856)
    if not on_disc(x, y, 16):
        continue
    w = rng.uniform(3, 7)
    d.shape("ellipse", f"Soil speck {i+1}", x=x - w / 2, y=y - w / 2, width=w, height=w * 0.8,
            fill=rng.choice(["#8A5E30", "#B0824C", "#6E4520"]), opacity=55, stroke=NONE)
for i, (x, y, w) in enumerate([(232,724,10),(646,736,8),(352,792,7),(726,796,9),(470,836,8)]):
    assert on_disc(x, y, 14)
    d.shape("ellipse", f"Pebble {i+1}", x=x - w * 0.7, y=y - w / 2, width=w * 1.4, height=w,
            fill=lin(0, y - w / 2, 0, y + w / 2, (0, "#CBA678"), (1, "#8E6440")), stroke=NONE)

# dry scrub tufts flanking the launch site
for i, (x, y, s) in enumerate([(204, 712, 1.0), (786, 700, 1.1), (268, 782, 0.9), (722, 788, 0.8)]):
    assert on_disc(x, y, 18)
    for k, dx in enumerate([-16, -9, -3, 3, 9, 16]):
        d.path(f"M{x},{y} Q{x+dx*0.5*s},{y-20*s} {x+dx*1.2*s},{y-38*s+abs(dx)*0.8}",
               f"Tuft {i+1}-{k+1}", fill=NONE,
               stroke=lin(0, y - 38 * s, 0, y, (0, "#D0AC6E"), (1, "#8C6234")),
               strokeWidth=3, opacity=90, cap="round")
# one leaning dead stalk, snapped where the leap launched
d.path("M300,706 C296,676 292,652 284,630", "Dead stalk", fill=NONE,
       stroke=lin(0, 630, 0, 706, (0, "#C09A5E"), (1, "#7C5228")), strokeWidth=4, cap="round")
for j, (x, y, ang) in enumerate([(290, 660, -30), (287, 646, -25), (294, 676, -35)]):
    a = math.radians(ang)
    d.path(f"M{x},{y} L{x + 14*math.cos(a):.0f},{y + 14*math.sin(a):.0f}", f"Stalk barb {j+1}",
           fill=NONE, stroke="#A87E46", strokeWidth=3, opacity=80, cap="round")

# ======================================================================================
# THE ARMADILLO — mid-leap, facing left, feet tucked.
# Shell dome: x in [SX0, SX1], base line SBASE, apex height SH.
SX0, SX1, SBASE, SH = 322, 694, 578, 176
SCX, SA = (SX0 + SX1) / 2, (SX1 - SX0) / 2

def ytop(x):
    """Carapace profile: rounded over the shoulders, fullest behind centre."""
    t = max(-1.0, min(1.0, (x - SCX) / SA))
    p = 2.6 if t < 0 else 3.8
    return SBASE - SH * (1 - abs(t) ** p) ** (1 / p)

def bow(x):
    return (x - SCX) / SA * 11

# --- tail: drawn first, streaming down behind (behind the shell) -------------------------
T0, T1, T2 = (672, 540), (792, 576), (822, 668)
tl, tr, tmid = [], [], []
NTL = 18
for k in range(NTL + 1):
    t = k / NTL
    x, y = qpt(T0, T1, T2, t)
    tx, ty = qtan(T0, T1, T2, t)
    ln = math.hypot(tx, ty)
    nx, ny = -ty / ln, tx / ln
    w = (30 * (1 - t) ** 1.1 + 5) / 2
    tl.append((x + nx * w, y + ny * w)); tr.append((x - nx * w, y - ny * w)); tmid.append((x, y, nx, ny, w))
def smooth(pts, closed=True, k=1.0):
    n = len(pts)
    s = "M%.1f,%.1f" % pts[0]
    for i in (range(n) if closed else range(n - 1)):
        p0 = pts[(i - 1) % n] if (closed or i > 0) else pts[0]
        p1, p2 = pts[i], pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (closed or i + 2 < n) else pts[-1]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6 * k, p1[1] + (p2[1] - p0[1]) / 6 * k)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6 * k, p2[1] - (p3[1] - p1[1]) / 6 * k)
        s += " C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (c1 + c2 + p2)
    return s + (" Z" if closed else "")
d.path(smooth(tl + list(reversed(tr))), "Tail",
       fill=lin(672, 540, 822, 668, (0, "#D4B183"), (1, "#9A7448")), stroke=INK, strokeWidth=4)
# tail rings
for k in range(2, NTL, 2):
    x, y, nx, ny, w = tmid[k]
    d.path(f"M{x + nx*w:.1f},{y + ny*w:.1f} L{x - nx*w:.1f},{y - ny*w:.1f}", f"Tail ring {k//2}",
           fill=NONE, stroke=INK, strokeWidth=3, opacity=55, cap="round")
# tail top sheen
d.path("M690,548 C740,566 780,596 806,640", "Tail sheen", fill=NONE, stroke="#F6E4BC",
       strokeWidth=4, opacity=45, cap="round")

# --- far legs (darker, behind the belly) --------------------------------------------------
def leg(name, pts, grad, w=0, claw=None):
    """Tucked leg as a closed smooth blob; claw = (x, y, dir) for ivory claw fan."""
    d.path(smooth(pts), f"{name} ink", fill=INK, stroke=NONE, opacity=90)
    inner = [(px, py - 2) for px, py in pts]
    d.path(smooth(inner), name, fill=grad, stroke=NONE)
    if claw:
        cx, cy, sgn = claw
        for j, dd in enumerate([-14, -5, 4]):
            tip = (cx + (18 - abs(dd) * 0.4) * sgn, cy + 16 + dd * 0.3)
            d.path(f"M{cx + dd*0.4},{cy} Q{(cx + tip[0])/2},{cy + 10} {tip[0]:.1f},{tip[1]:.1f}",
                   f"{name} claw {j+1}", fill=NONE, stroke="#F4EAD2", strokeWidth=4, cap="round")

# far foreleg + far hind leg
leg("Foreleg far", [(392, 556), (372, 586), (366, 612), (384, 626), (410, 620), (416, 590)],
    SKIN_DARK, claw=(368, 616, -1))
leg("Hind leg far", [(624, 570), (648, 596), (656, 620), (638, 634), (612, 626), (604, 596)],
    SKIN_DARK, claw=(656, 622, 1))

# --- belly skin under the shell base ------------------------------------------
d.path("M360,556 C420,578 560,584 650,570 L656,614 C580,634 460,634 380,616 "
       "C364,608 356,584 360,556 Z", "Belly", fill=SKIN_GRAD, stroke=NONE)
for i in range(16):
    x = 382 + i * 16
    d.path(f"M{x},{604} Q{x-4},{614} {x-9},{622}", f"Belly fur {i+1}", fill=NONE,
           stroke=FUR, strokeWidth=3, opacity=60, cap="round")

# --- head: long snout dipping forward under the shoulder shield ---------------------------
d.path("M368,450 C346,442 318,446 294,464 C270,482 250,510 234,538 "
       "C228,550 236,560 248,558 C274,554 302,558 330,564 L372,566 Z",
       "Head", fill=HEAD_GRAD, stroke=INK, strokeWidth=5)
# head-shield scale grid on the crown
for i, dd in enumerate(["M352,448 C334,462 318,478 306,492", "M330,446 C314,460 300,476 290,490",
                        "M308,452 C294,464 282,478 272,490", "M288,470 C312,464 338,468 358,478",
                        "M270,494 C292,488 314,490 334,498"]):
    d.path(dd, f"Head shield seam {i+1}", fill=NONE, stroke=INK, strokeWidth=3, opacity=40, cap="round")
d.path("M258,492 C286,472 322,458 354,456", "Head shield sheen", fill=NONE, stroke="#FFFFFF",
       strokeWidth=6, opacity=35, cap="round")
# snout tip: nose pad, nostril, mouth
d.path("M236,538 C226,544 220,550 222,556 C226,562 238,560 246,554 Z", "Nose pad",
       fill=lin(0, 538, 0, 560, (0, "#E8A88E"), (1, "#B06E52")), stroke=NONE)
d.shape("ellipse", "Nostril", x=226, y=547, width=6, height=5, fill="#5E3220", opacity=80, stroke=NONE)
d.path("M240,560 C262,562 284,564 306,568", "Mouth", fill=NONE, stroke=INK, strokeWidth=3,
       opacity=70, cap="round")
# eye — alert, wide for the leap
d.shape("ellipse", "Eye ring", x=282, y=494, width=22, height=18, fill="#B87F5C", opacity=40, stroke=NONE)
d.shape("ellipse", "Eye", x=285, y=496, width=15, height=14, fill="#241108", stroke=NONE)
d.shape("ellipse", "Eye glint", x=289, y=499, width=5, height=4, fill="#FFFFFF", opacity=85, stroke=NONE)

# --- carapace: dome, shoulder shield, NINE bands, hip shield --------------------------------
dome = f"M{SX0},{SBASE} " + " ".join(
    f"L{x:.1f},{ytop(x):.1f}" for x in [SX0 + (SX1 - SX0) * i / 60 for i in range(61)]) + \
    f" L{SX1},{SBASE} Z"
d.path(dome, "Carapace", fill=SHELL_A, stroke=NONE)

# shoulder shield (front cap) + hip shield (rear cap), tint overlays
front_cap = f"M{SX0},{SBASE} " + " ".join(
    f"L{x:.1f},{ytop(x) + 1:.1f}" for x in [SX0 + (424 - SX0) * i / 20 for i in range(21)]) + \
    f" L424,{SBASE} Z"
d.path(front_cap, "Shoulder shield", fill=SHIELD_GRAD, opacity=85, stroke=NONE)
rear_cap = f"M592,{SBASE} " + " ".join(
    f"L{x:.1f},{ytop(x) + 1:.1f}" for x in [592 + (SX1 - 592) * i / 20 for i in range(21)]) + \
    f" L{SX1},{SBASE} Z"
d.path(rear_cap, "Hip shield", fill=SHIELD_GRAD, opacity=80, stroke=NONE)

# the NINE bands
XB0, XB1, NB = 424, 592, 9
xs = [XB0 + (XB1 - XB0) * k / NB for k in range(NB + 1)]
for k in range(NB):
    xa, xb = xs[k], xs[k + 1]
    top = " ".join(f"L{x:.1f},{ytop(x) + 1.5:.1f}" for x in [xa + (xb - xa) * i / 4 for i in range(5)])
    ya, yb = ytop(xa), ytop(xb)
    dd = (f"M{xa:.1f},{ya + 1.5:.1f} {top[1:]} "
          f"Q{xb + bow(xb):.1f},{(yb + SBASE)/2:.1f} {xb:.1f},{SBASE - 2} "
          f"L{xa:.1f},{SBASE - 2} Q{xa + bow(xa):.1f},{(ya + SBASE)/2:.1f} {xa:.1f},{ya + 1.5:.1f} Z")
    d.path(dd, f"Band {k+1}", fill=SHELL_A if k % 2 else SHELL_B, stroke=NONE)
    # front lip of each band catches the sun
    d.path(f"M{xa + 3:.1f},{ya + 7:.1f} Q{xa + bow(xa) + 3:.1f},{(ya + SBASE)/2:.1f} {xa + 3:.1f},{SBASE - 20}",
           f"Band lip {k+1}", fill=NONE, stroke="#FFF2D2", strokeWidth=3, opacity=45, cap="round")
# skin folds at every seam — sparse hairs escaping between the bands
for k, x in enumerate(xs):
    y = ytop(x)
    heavy = k in (0, NB)
    d.path(f"M{x:.1f},{y + 1:.1f} Q{x + bow(x):.1f},{(y + SBASE)/2:.1f} {x:.1f},{SBASE - 2}",
           f"Seam {k}", fill=NONE, stroke=INK, strokeWidth=3 if not heavy else 4,
           opacity=75, cap="round")
    if 0 < k < NB:
        for j in range(rng.choice([1, 2, 2])):
            yy = rng.uniform(y + 26, SBASE - 44)
            ln2 = rng.uniform(7, 14); sgn = rng.choice([-1, 1])
            d.path(f"M{x + bow(x)*0.3:.1f},{yy:.1f} q{sgn*rng.uniform(2,5):.1f},{ln2*0.5:.1f} "
                   f"{sgn*3 - rng.uniform(2,5):.1f},{ln2:.1f}", f"Seam fur {k}-{j+1}",
                   fill=NONE, stroke=FUR, strokeWidth=3, opacity=rng.choice([60, 75]), cap="round")
# shield scale-grid hints
for i, dd in enumerate(["M336,470 C356,462 380,460 402,464", "M330,500 C356,490 384,488 410,494",
                        "M332,532 C358,524 386,522 412,528", "M352,452 L352,566", "M384,448 L386,570",
                        "M614,470 C640,462 664,462 686,470", "M620,502 C644,494 666,494 686,502",
                        "M624,536 C646,530 666,530 684,536", "M646,456 L648,572", "M672,462 L676,566"]):
    d.path(dd, f"Shield grid {i+1}", fill=NONE, stroke=INK, strokeWidth=3, opacity=28, cap="round")
# crown sheen + base shade
crest = " ".join(f"L{x:.1f},{ytop(x) + 22:.1f}" for x in range(360, 660, 12))
d.path("M" + crest[1:], "Carapace sheen", fill=NONE, stroke="#FFF6DC", strokeWidth=12,
       opacity=32, cap="round")
crest2 = " ".join(f"L{x:.1f},{ytop(x) + 10:.1f}" for x in range(430, 590, 12))
d.path("M" + crest2[1:], "Carapace glint", fill=NONE, stroke="#FFFFFF", strokeWidth=4,
       opacity=55, cap="round")
d.path(f"M{SX0 + 24},{SBASE - 12} L{SX1 - 12},{SBASE - 12}", "Carapace base shade", fill=NONE,
       stroke="#6E4A26", strokeWidth=16, opacity=24, cap="round")
d.path(dome, "Carapace outline", fill=NONE, stroke=INK, strokeWidth=5)

# ears: tall, up and perked even mid-leap — drawn over the shield rim so the
# full ear reads on the head (near ear big, far ear peeking)
d.path("M314,460 C310,442 314,422 326,410 C334,404 340,410 338,420 C336,436 330,452 324,462 Z",
       "Ear far", fill=SKIN_DARK, stroke=INK, strokeWidth=4)
d.path("M340,466 C336,444 342,418 358,404 C368,396 376,404 373,414 C370,434 360,454 350,468 Z",
       "Ear near", fill=HEAD_GRAD, stroke=INK, strokeWidth=4)
d.path("M350,458 C348,440 354,422 366,412 C370,408 373,412 372,418 C370,434 362,448 356,460 Z",
       "Ear inner", fill="#C98E6A", opacity=60, stroke=NONE)

# --- near legs, tucked for the leap --------------------------------------------------------
leg("Foreleg near", [(402, 560), (376, 588), (368, 614), (388, 632), (420, 626), (430, 592)],
    SKIN_GRAD, claw=(372, 620, -1))
leg("Hind leg near", [(608, 566), (640, 592), (652, 618), (634, 638), (602, 630), (592, 596)],
    SKIN_GRAD, claw=(652, 624, 1))

# --- leap cues: rising dust off the launch point -------------------------------------------
for i, (x, y, w, h, op) in enumerate([(360, 672, 90, 40, 24), (430, 686, 120, 44, 30),
                                       (520, 678, 110, 42, 26), (600, 692, 80, 34, 20),
                                       (460, 648, 70, 30, 18)]):
    assert on_disc(x + w / 2, y + h / 2, 10), (x, y)
    d.shape("ellipse", f"Dust puff {i+1}", x=x, y=y, width=w, height=h, fill="#EBD3A4",
            opacity=op, stroke=NONE)
for i in range(14):
    x, y = rng.uniform(340, 640), rng.uniform(630, 700)
    if not on_disc(x, y, 14):
        continue
    w = rng.choice([3, 4, 5])
    d.shape("ellipse", f"Dust grain {i+1}", x=x, y=y, width=w, height=w,
            fill=rng.choice(["#C9A068", "#E0BE86", "#A87C44"]), opacity=rng.choice([60, 75, 90]), stroke=NONE)
# three short motion ticks under the tucked body
for i, (x, y0, y1) in enumerate([(430, 622, 656), (492, 632, 664), (556, 622, 654)]):
    d.path(f"M{x},{y0} L{x - 4},{y1}", f"Leap tick {i+1}", fill=NONE, stroke="#A87C44",
           strokeWidth=5, opacity=45, cap="round")

# heat-shimmer motes in the sky
for i, (x, y) in enumerate([(226, 300), (762, 250), (640, 160), (310, 170), (820, 330), (186, 430)]):
    assert on_disc(x, y, 20)
    d.shape("ellipse", f"Mote {i+1}", x=x - 4, y=y - 4, width=8, height=8, fill="#F8DCA0",
            opacity=32, stroke=NONE)

# --- rim on top so ground and decor close under it -----------------------------------------
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840, fill=NONE,
        stroke="#3A2210", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#FFF2D2", strokeWidth=3, opacity=40)

# --- name + second line ----------------------------------------------------------------------
r1 = d.text("NINE-BANDED ARMADILLO", "Name", x=500, y=938, size=44, font="Virelai Sans",
            color="#F6E4C2", justify="center")
LINE2, SZ2, TRK = "DASYPUS NOVEMCINCTUS", 22, 200
r = d.text(LINE2, "Second line", x=500, y=974, size=SZ2, font="Virelai Sans",
           color="#CBA674", justify="center")
d.cmd("text.setStyle", "Second line tracking", id=r["id"], tracking=TRK)
def find(o, oid):
    if isinstance(o, dict):
        if o.get("id") == oid and "bounds" in o: return o
        o = list(o.values())
    if isinstance(o, list):
        for v in o:
            hit = find(v, oid)
            if hit: return hit
layers = d.call("inspect_document", {}, "inspect")["layers"]
for rr, lim in ((r1, 800), (r, 760)):
    b = find(layers, rr["id"])["bounds"]
    print("caption bounds", {k: round(v) for k, v in b.items()})
    assert b["width"] <= lim and b["x"] >= 100 and b["y"] + b["height"] <= 990, b

d.finish("nine-banded-armadillo-V1R00")
