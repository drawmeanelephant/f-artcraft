#!/usr/bin/env python3
"""Blue-ringed octopus — field plate V1R00. A golf ball of venom seen from the
front-top: tan dome of a mantle, eight arms draped over a wet tide-pool rock,
tips curled. Every papilla ring flashes electric blue — the don't-touch mood.
Low wet-rock floor closes on the disc's own arc. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Blue-ringed Octopus — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420
INK = "#241408"                    # warm dark ink, never pure black

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

def cubic(p0, p1, p2, p3, t):
    u = 1 - t
    return (u**3*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t**3*p3[0],
            u**3*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t**3*p3[1])

def ribbon(p0, p1, p2, p3, w0, w1, label, n=22, **kw):
    L, Rr = [], []
    for k in range(n + 1):
        t = k / n
        x, y = cubic(p0, p1, p2, p3, t)
        x0, y0 = cubic(p0, p1, p2, p3, max(0, t - 0.01))
        x1, y1 = cubic(p0, p1, p2, p3, min(1, t + 0.01))
        dx, dy = x1 - x0, y1 - y0
        ln = math.hypot(dx, dy) or 1
        w = (w0 + (w1 - w0) * t) / 2
        L.append((x - dy/ln * w, y + dx/ln * w))
        Rr.append((x + dy/ln * w, y - dx/ln * w))
    s = "M%.1f,%.1f " % L[0] + " ".join("L%.1f,%.1f" % p for p in L[1:])
    s += " " + " ".join("L%.1f,%.1f" % p for p in reversed(Rr)) + " Z"
    return d.path(s, label, **kw)

BG_GRAD    = lin(0, 0, 0, 1000, (0, "#0C1E24"), (1, "#04090B"))
PLATE_GRAD = rad((0, "#CFE6DA"), (0.55, "#86B3A2"), (1, "#3E6656"))
ROCK_GRAD  = lin(0, 700, 0, 880, (0, "#5E6A5E"), (0.5, "#3E4A42"), (1, "#1A241E"))
SKIN_GRAD  = rad((0, "#F0CE8C"), (0.55, "#D8A85E"), (1, "#9A7034"))
ARM_GRAD   = lin(500, 500, 500, 780, (0, "#DCAC64"), (0.6, "#B88644"), (1, "#8A5E28"))
RING_BLUE  = "#3FA8DC"
RING_CORE  = "#7FD4F2"

# --- backdrop + tide-pool plate ---------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#6FA294", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#2C4A3E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E4F2E8", strokeWidth=3, opacity=45)
# water haze blotches + caustic arcs in the pool light
d.shape("ellipse", "Haze 1", x=180, y=160, width=240, height=130,
        fill="#DDEEE4", opacity=20, stroke=NONE)
d.shape("ellipse", "Haze 2", x=600, y=580, width=220, height=120,
        fill="#5E8A76", opacity=20, stroke=NONE)
for i, dd in enumerate(["M220,300 C340,282 470,284 590,300",
                        "M300,380 C420,364 560,366 690,382",
                        "M250,470 C360,456 480,458 610,472"]):
    d.path(dd, f"Caustic {i+1}", fill=NONE, stroke="#EAF6EC",
           strokeWidth=4, opacity=14, cap="round")
# drifting motes + a few rising bubbles
for i, (x, y, w) in enumerate([(200,330,6),(790,300,7),(170,510,6),(838,480,6),
                               (250,660,5),(760,690,7),(420,120,6),(620,110,7),
                               (330,150,5),(700,180,5),(140,610,5),(870,380,5)]):
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#C8E4D6", opacity=40, stroke=NONE)
for i, (x, y, w) in enumerate([(778,540,16),(798,460,10),(782,380,20),(806,300,12)]):
    d.shape("ellipse", f"Bubble {i+1}", x=x, y=y, width=w, height=w,
            fill="#FFFFFF", opacity=14, stroke=NONE)

# --- wet rock floor, closing on the disc's own arc ---------------------------------
fy = 758
fl, fr = rim_x(fy, side=-1), rim_x(fy, side=1)
d.path(f"M{fl:.1f},{fy} C300,742 420,758 540,750 C660,744 760,750 {fr:.1f},{fy} "
       f"A{R},{R} 0 0 1 {fl:.1f},{fy} Z", "Rock floor", fill=ROCK_GRAD, stroke=NONE)
# wet sheen along the crest + a standing pool
d.path(f"M{fl+8:.0f},{fy-3} C300,739 420,755 540,747 C660,741 760,747 {fr-8:.0f},{fy-3}",
       "Wet sheen", fill=NONE, stroke="#D8EAD8", strokeWidth=5, opacity=35, cap="round")
d.shape("ellipse", "Pool", x=300, y=788, width=200, height=20,
        fill="#A8C4B4", opacity=28, stroke=NONE)
d.shape("ellipse", "Pool light", x=330, y=792, width=130, height=8,
        fill="#E4F0E4", opacity=30, stroke=NONE)
# barnacles + limpet on the rock
for i, (x, y, w) in enumerate([(260,770,18),(286,778,12),(742,768,16),(770,780,11),(706,786,10)]):
    d.shape("ellipse", f"Barnacle {i+1}", x=x, y=y, width=w, height=w*0.7,
            fill="#8A9078", opacity=75, stroke=INK, strokeWidth=2)
    d.shape("ellipse", f"Barnacle tip {i+1}", x=x+w*0.35, y=y+w*0.18, width=w*0.3,
            height=w*0.2, fill="#4A503E", opacity=80, stroke=NONE)
d.path("M620,796 C640,782 672,782 690,796 C672,804 640,804 620,796 Z",
       "Limpet", fill="#767C62", opacity=80, stroke=INK, strokeWidth=3)
# rock shading cracks
for i, dd in enumerate(["M350,796 L392,812", "M560,806 L596,796", "M430,820 L462,814"]):
    d.path(dd, f"Rock crack {i+1}", fill=NONE, stroke="#141C16",
           strokeWidth=4, opacity=45, cap="round")

# contact shadow under the animal
d.shape("ellipse", "Contact shadow", x=330, y=736, width=340, height=26,
        fill="#0C140E", opacity=45, stroke=NONE)

# === the animal =====================================================================
# warning aura: the rings are on, the pool glows faintly blue around it
d.shape("ellipse", "Ring aura", x=290, y=330, width=420, height=380,
        fill="#4FB4E0", opacity=10, stroke=NONE)

# --- far arms: four tips curling on the rock ------------------------------------------
def arm(root, c1, c2, tip, w0, w1, label, grad=None):
    ribbon(root, c1, c2, tip, w0, w1, label,
           fill=grad or ARM_GRAD, stroke=INK, strokeWidth=4)
    # sucker row on the inner edge
    n = 22
    for j, t in enumerate((0.5, 0.65, 0.8)):
        x, y = cubic(root, c1, c2, tip, t)
        x0, y0 = cubic(root, c1, c2, tip, max(0, t - 0.01))
        x1, y1 = cubic(root, c1, c2, tip, min(1, t + 0.01))
        dx, dy = x1 - x0, y1 - y0
        ln = math.hypot(dx, dy) or 1
        w = (w0 + (w1 - w0) * t) / 2
        s = max(4.5, w * 0.5)
        d.shape("ellipse", f"{label} sucker {j+1}", x=round(x - s/2),
                y=round(y - s/2), width=round(s), height=round(s),
                fill="#F6E4BC", opacity=55, stroke=NONE)

# arms drape out and down over the rock — tips inside the rim
arm((470,540), (400,560), (340,620), (296,690), 30, 8, "Arm L1")
arm((446,556), (360,600), (300,680), (268,742), 28, 7, "Arm L2")
arm((452,576), (390,650), (356,720), (344,772), 26, 7, "Arm L3")
arm((530,540), (600,560), (660,620), (704,690), 30, 8, "Arm R1")
arm((554,556), (640,600), (700,680), (732,742), 28, 7, "Arm R2")
arm((548,576), (610,650), (644,720), (656,772), 26, 7, "Arm R3")
# two front arms curling inward over the rock
arm((478,584), (450,660), (430,720), (418,768), 30, 8, "Arm F1")
arm((522,584), (550,660), (570,720), (582,768), 30, 8, "Arm F2")

# webbing between the arm bases — kills the spider read, hides the root angles
d.path("M404,552 C424,588 452,608 478,616 C488,619 512,619 522,616 "
       "C548,608 576,588 596,552 C560,578 532,586 500,586 "
       "C468,586 440,578 404,552 Z",
       "Web skirt", fill="#B88644", opacity=90, stroke=NONE)
# little hooks at the arm tips — the curl the ribbons can't give
for i, (x, y, ex, ey) in enumerate([
        (296,690, 278,712), (268,742, 252,760), (344,772, 330,788),
        (704,690, 722,712), (732,742, 748,760), (656,772, 670,788),
        (418,768, 402,782), (582,768, 598,782)]):
    d.path(f"M{x},{y} C{x-8 if ex<x else x+8},{y+8} {ex},{ey} {ex+ (4 if ex<x else -4)},{ey+4}",
           f"Tip curl {i+1}", fill=NONE, stroke="#8A5E28",
           strokeWidth=7, cap="round")

# --- mantle: the tan dome ------------------------------------------------------------
d.path("M500,296 C570,296 620,352 622,424 C624,486 596,540 556,560 "
       "C536,570 464,570 444,560 C404,540 376,486 378,424 "
       "C380,352 430,296 500,296 Z",
       "Mantle", fill=SKIN_GRAD, stroke=INK, strokeWidth=6)
# dome highlight + under-shadow where the head narrows
d.shape("ellipse", "Mantle light", x=420, y=316, width=160, height=90,
        fill="#FFFFFF", opacity=22, stroke=NONE)
d.path("M404,500 C440,548 560,548 596,500 C566,540 434,540 404,500 Z",
       "Mantle shade", fill="#8A5E28", opacity=45, stroke=NONE)
# head wedge between the eyes
d.path("M440,520 C456,504 476,496 500,496 C524,496 544,504 560,520 "
       "C556,548 536,566 500,568 C464,566 444,548 440,520 Z",
       "Head", fill="#C08A48", opacity=90, stroke=NONE)

# --- eyes: low-set, half-lidded — the unimpressed look -------------------------------
for s, ex in ((-1, 448), (1, 552)):
    d.shape("ellipse", f"Eye bump {'L' if s<0 else 'R'}", x=ex-16, y=482,
            width=32, height=30, fill="#D8A85E", stroke=INK, strokeWidth=4)
    d.shape("ellipse", f"Eye {'L' if s<0 else 'R'}", x=ex-9, y=488,
            width=18, height=17, fill="#201408", stroke=NONE)
    d.shape("ellipse", f"Eye glint {'L' if s<0 else 'R'}", x=ex-4, y=491,
            width=6, height=6, fill="#FFFFFF", opacity=85, stroke=NONE)
    d.path(f"M{ex-15},{488} C{ex-6},{478} {ex+7},{478} {ex+15},{487}",
           f"Lid {'L' if s<0 else 'R'}", fill=NONE, stroke=INK,
           strokeWidth=4, cap="round")

# --- the rings: electric blue loops all over -----------------------------------------
def ring(x, y, w, h, label):
    d.shape("ellipse", f"{label} glow", x=x-w*0.28, y=y-h*0.28,
            width=w*1.56, height=h*1.56, fill="#5EC4F0", opacity=22, stroke=NONE)
    d.shape("ellipse", label, x=x, y=y, width=w, height=h,
            fill=NONE, stroke=RING_BLUE, strokeWidth=6)
    d.shape("ellipse", f"{label} core", x=x+w*0.3, y=y+h*0.24,
            width=w*0.4, height=h*0.4, fill=RING_CORE, opacity=45, stroke=NONE)

# mantle rings — scattered, varying sizes
for i, (x, y, w, h) in enumerate([
        (440,330,40,32),(510,318,34,30),(560,350,30,26),(468,368,36,30),
        (536,392,34,28),(452,420,30,26),(586,410,26,22),(500,436,32,28),
        (416,392,26,22),(560,440,28,24),(470,462,26,22),(528,476,24,20)]):
    ring(x, y, w, h, f"Mantle ring {i+1}")
# head + arm-base rings
for i, (x, y, w, h) in enumerate([(500,528,22,18),(462,540,18,15),(538,540,18,15)]):
    ring(x, y, w, h, f"Head ring {i+1}")
for i, (x, y) in enumerate([(404,584),(340,656),(376,692),(596,584),(660,656),
                            (624,692),(446,684),(554,684),(432,736),(568,736)]):
    d.shape("ellipse", f"Arm ring {i+1}", x=x-8, y=y-6, width=16, height=12,
            fill=NONE, stroke=RING_BLUE, strokeWidth=4.5)
# skin papillae: small tan bumps between the rings
for i, (x, y, w) in enumerate([(420,352,8),(490,342,7),(544,330,7),(578,384,8),
                               (434,444,7),(508,402,6),(590,452,7),(480,492,6)]):
    d.shape("ellipse", f"Papilla {i+1}", x=x, y=y, width=w, height=w*0.7,
            fill="#B88644", opacity=70, stroke=NONE)

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#14281F", strokeWidth=6)

# --- name ---------------------------------------------------------------------------
d.text("BLUE-RINGED OCTOPUS", "Name", x=500, y=958, size=44, font="Virelai Sans",
       color="#D8F0E4", justify="center")

d.finish("blue-ringed-octopus-V1R00")
