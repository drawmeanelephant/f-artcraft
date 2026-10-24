#!/usr/bin/env python3
"""Kraken — field-guide plate V1R00. Storm plate, rigging-snap mood: the great
oxblood mantle rising out of a green-black sea, two gold eyes set wide, arms
climbing the rim in tapering curls with pale sucker rows, foam and a snapped
spar where the waves close on the disc's own arc. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math, re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Kraken — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420          # plate disc centre + radius
INK = "#1E1016"                    # warm dark ink, never pure black

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rim_x(y, r=R, side=-1):
    return CX + side * math.sqrt(r * r - (y - CY) ** 2)

def on_disc(x, y, pad=0, r=R):
    return math.hypot(x - CX, y - CY) <= r - pad

def quad(p0, p1, p2, t):
    u = 1 - t
    return (u*u*p0[0] + 2*u*t*p1[0] + t*t*p2[0],
            u*u*p0[1] + 2*u*t*p1[1] + t*t*p2[1])

def ribbon_pts(p0, p1, p2, w0, w1, n=24):
    """Edge points of a tapered strip along a quadratic."""
    L, Rr = [], []
    for k in range(n + 1):
        t = k / n
        x, y = quad(p0, p1, p2, t)
        x0, y0 = quad(p0, p1, p2, max(0, t - 0.01))
        x1, y1 = quad(p0, p1, p2, min(1, t + 0.01))
        dx, dy = x1 - x0, y1 - y0
        ln = math.hypot(dx, dy) or 1
        w = (w0 + (w1 - w0) * t) / 2
        L.append((x - dy/ln * w, y + dx/ln * w))
        Rr.append((x + dy/ln * w, y - dx/ln * w))
    return L, Rr

def ribbon(p0, p1, p2, w0, w1, label, n=24, **kw):
    L, Rr = ribbon_pts(p0, p1, p2, w0, w1, n)
    s = "M%.1f,%.1f " % L[0] + " ".join("L%.1f,%.1f" % p for p in L[1:])
    s += " " + " ".join("L%.1f,%.1f" % p for p in reversed(Rr)) + " Z"
    return d.path(s, label, **kw)

def sucker_row(p0, p1, p2, w0, w1, side, ts, label, color="#E8D8C0"):
    """Suckers along one edge of a tapered arm: `side` -1 inner-left, +1 right."""
    for i, t in enumerate(ts):
        x, y = quad(p0, p1, p2, t)
        x0, y0 = quad(p0, p1, p2, max(0, t - 0.01))
        x1, y1 = quad(p0, p1, p2, min(1, t + 0.01))
        dx, dy = x1 - x0, y1 - y0
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy/ln, dx/ln
        w = (w0 + (w1 - w0) * t) / 2
        sx, sy = x + nx * w * 0.55 * side, y + ny * w * 0.55 * side
        rw = max(3.5, w * 0.42)
        d.shape("ellipse", f"{label} sucker {i+1}", x=sx - rw, y=sy - rw*0.8,
                width=rw*2, height=rw*1.6, fill=color, opacity=85,
                stroke=INK, strokeWidth=1.5)
        d.shape("ellipse", f"{label} cup {i+1}", x=sx - rw*0.55, y=sy - rw*0.45,
                width=rw*1.1, height=rw*0.9, fill="#8A5048", opacity=70, stroke=NONE)

def mirror(dd):
    out, toks, ex = [], re.findall(r"[A-Za-z]|-?\d*\.?\d+", dd), True
    for t in toks:
        if t.isalpha():
            out.append(t); ex = True
        elif ex:
            out.append(f"{1000 - float(t):g},"); ex = False
        else:
            out[-1] += f"{float(t):g}"; ex = True
    return " ".join(out)

def pair(dd, label, **kw):
    d.path(dd, f"{label} L", **kw)
    d.path(mirror(dd), f"{label} R", **kw)

BG_GRAD = lin(0, 0, 0, 1000, (0, "#0A1418"), (1, "#04080A"))
PLATE_GRAD = rad((0, "#7A9A8C"), (0.55, "#3E6055"), (1, "#16282A"))
SEA_GRAD = lin(0, 660, 0, 880, (0, "#2E5048"), (0.6, "#1B3632"), (1, "#0C1E20"))
MANTLE_GRAD = rad((0, "#8A4048"), (0.55, "#5E2830"), (1, "#331418"))
ARM_GRAD = lin(400, 640, 300, 240, (0, "#6E3038"), (0.6, "#50222B"), (1, "#3A161C"))
ARM_GRAD_R = lin(600, 640, 700, 240, (0, "#6E3038"), (0.6, "#50222B"), (1, "#3A161C"))
FOAM = "#DCE8DC"

# --- backdrop + storm plate -------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=64, y=24, width=872, height=872,
        fill="#3E6055", opacity=12, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#0E1E1E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#B8D0C0", strokeWidth=3, opacity=35)

# lightning-pale glow behind the mantle + a far fork
d.shape("ellipse", "Storm glow", x=330, y=180, width=340, height=300,
        fill="#C8DCD0", opacity=18, stroke=NONE)
d.path("M648,120 L622,220 L648,212 L606,330", "Far lightning", fill=NONE,
       stroke="#DCE8DC", strokeWidth=3.5, opacity=30, cap="round")

# rain — thin diagonal streaks, all inside the rim
for i, (x, y, ln) in enumerate([(240, 190, 60), (300, 150, 48), (360, 200, 55),
                                (440, 140, 44), (560, 160, 58), (640, 200, 50),
                                (710, 170, 44), (770, 260, 40), (200, 330, 46),
                                (800, 350, 44), (260, 260, 40), (690, 300, 42)]):
    assert on_disc(x, y, 30), (x, y)
    d.path(f"M{x},{y} L{x - ln*0.35},{y + ln}", f"Rain {i+1}", fill=NONE,
           stroke="#B8D0C0", strokeWidth=3, opacity=16, cap="round")

# snapped rigging: a broken yardarm top-left, two parted lines whipping free
d.path("M150,150 L258,196", "Broken yard", fill=NONE, stroke="#241A12",
       strokeWidth=9, opacity=80, cap="round")
d.path("M196,168 C216,230 190,270 208,330", "Parted line 1", fill=NONE,
       stroke="#2E2016", strokeWidth=3.5, opacity=65, cap="round")
d.path("M236,186 C268,236 250,300 284,352", "Parted line 2", fill=NONE,
       stroke="#2E2016", strokeWidth=3.5, opacity=60, cap="round")
d.path("M150,150 L128,132 M150,150 L172,122", "Yard splinters", fill=NONE,
       stroke="#241A12", strokeWidth=4, opacity=70, cap="round")

# --- the sea: churned band closing on the disc's own arc ----------------------------
fy = 712
fl, fr = rim_x(fy, side=-1), rim_x(fy, side=1)
d.path(f"M{fl:.1f},{fy} C300,688 380,724 470,706 C560,688 650,700 {fr:.1f},{fy} "
       f"A{R},{R} 0 0 1 {fl:.1f},{fy} Z", "Sea", fill=SEA_GRAD, stroke=NONE)
# second darker swell in front, also arc-closed
fy2 = 790
fl2, fr2 = rim_x(fy2, side=-1), rim_x(fy2, side=1)
d.path(f"M{fl2:.1f},{fy2} C360,772 440,800 520,788 C600,776 680,784 {fr2:.1f},{fy2} "
       f"A{R},{R} 0 0 1 {fl2:.1f},{fy2} Z", "Front swell",
       fill=lin(0, 790, 0, 880, (0, "#122628"), (1, "#081416")), stroke=NONE)
# foam crests along the wave tops
d.path(f"M{fl+8:.0f},{fy} C300,688 380,724 470,706 C560,688 650,700 {fr-8:.0f},{fy}",
       "Foam crest", fill=NONE, stroke=FOAM, strokeWidth=7, opacity=55, cap="round")
d.path(f"M{fl2+10:.0f},{fy2} C360,772 440,800 520,788 C600,776 680,784 {fr2-10:.0f},{fy2}",
       "Foam crest 2", fill=NONE, stroke=FOAM, strokeWidth=6, opacity=40, cap="round")
for i, (x, y, w) in enumerate([(250, 720, 14), (330, 700, 10), (430, 716, 16),
                               (540, 698, 12), (640, 708, 14), (730, 722, 10),
                               (300, 796, 12), (470, 806, 14), (610, 792, 10)]):
    d.shape("ellipse", f"Foam blob {i+1}", x=x - w/2, y=y - 5, width=w, height=10,
            fill=FOAM, opacity=45, stroke=NONE)
# spray where the arms break the surface
for i, (x, y) in enumerate([(300, 690), (330, 678), (356, 694), (676, 684), (704, 700), (648, 692)]):
    d.path(f"M{x},{y} q-3,-18 4,-26", f"Spray {i+1}", fill=NONE,
           stroke=FOAM, strokeWidth=3.5, opacity=45, cap="round")

# --- back arms: the two long climbers, tapering to curled tips ----------------------
# left climber: root at the mantle base, swinging wide left then hooking back in
ARM_L = ((452, 600), (240, 470), (268, 250))
ribbon(*ARM_L, 74, 26, "Arm up L", fill=ARM_GRAD, stroke=INK, strokeWidth=5)
# tip hook: small inward curl at the top of the left climber
ribbon((268, 250), (300, 196), (352, 214), 26, 10, "Arm tip curl L",
       fill=lin(268, 250, 352, 214, (0, "#50222B"), (1, "#3A161C")),
       stroke=INK, strokeWidth=4)
sucker_row(*ARM_L, 74, 26, -1, [0.15, 0.28, 0.41, 0.54, 0.67, 0.80], "Arm L")
# right climber, mirrored
ARM_R = ((548, 600), (760, 470), (732, 250))
ribbon(*ARM_R, 74, 26, "Arm up R", fill=ARM_GRAD_R, stroke=INK, strokeWidth=5)
ribbon((732, 250), (700, 196), (648, 214), 26, 10, "Arm tip curl R",
       fill=lin(732, 250, 648, 214, (0, "#50222B"), (1, "#3A161C")),
       stroke=INK, strokeWidth=4)
sucker_row(*ARM_R, 74, 26, 1, [0.15, 0.28, 0.41, 0.54, 0.67, 0.80], "Arm R")

# --- mid arms sweeping low into the sea ----------------------------------------------
ARM_ML = ((468, 620), (330, 660), (238, 560))
ribbon(*ARM_ML, 60, 22, "Arm low L",
       fill=lin(468, 620, 238, 560, (0, "#5E2830"), (1, "#3A161C")),
       stroke=INK, strokeWidth=5)
ARM_MR = ((532, 620), (670, 660), (762, 560))
ribbon(*ARM_MR, 60, 22, "Arm low R",
       fill=lin(532, 620, 762, 560, (0, "#5E2830"), (1, "#3A161C")),
       stroke=INK, strokeWidth=5)
sucker_row(*ARM_ML, 60, 22, 1, [0.2, 0.38, 0.56, 0.74], "Arm low L")
sucker_row(*ARM_MR, 60, 22, -1, [0.2, 0.38, 0.56, 0.74], "Arm low R")

# --- the mantle: a great dome shouldering out of the waves --------------------------
d.path("M500,226 C588,226 660,300 678,396 C690,462 676,540 640,600 "
       "C612,646 560,672 500,672 C440,672 388,646 360,600 "
       "C324,540 310,462 322,396 C340,300 412,226 500,226 Z",
       "Mantle", fill=MANTLE_GRAD, stroke=INK, strokeWidth=7)
# dome sheen and flank shading
d.shape("ellipse", "Mantle sheen", x=410, y=270, width=180, height=120,
        fill="#C87878", opacity=22, stroke=NONE)
pair("M360,420 C352,480 366,540 398,586", "Flank shade", fill=NONE,
     stroke="#2A0E12", strokeWidth=14, opacity=35, cap="round")
# crown ridge creases
for i, dd in enumerate(["M452,250 C470,300 478,340 478,380",
                        "M500,244 C500,300 500,340 500,380",
                        "M548,250 C530,300 522,340 522,380"]):
    d.path(dd, f"Mantle crease {i+1}", fill=NONE, stroke="#3A1418",
           strokeWidth=5, opacity=50, cap="round")

# --- front arms in an S over the mantle base -----------------------------------------
ARM_FL = ((452, 640), (330, 560), (372, 430))
ribbon(*ARM_FL, 58, 20, "Arm front L",
       fill=lin(452, 640, 372, 430, (0, "#6E3038"), (1, "#46202A")),
       stroke=INK, strokeWidth=5)
ARM_FR = ((548, 640), (670, 560), (628, 430))
ribbon(*ARM_FR, 58, 20, "Arm front R",
       fill=lin(548, 640, 628, 430, (0, "#6E3038"), (1, "#46202A")),
       stroke=INK, strokeWidth=5)
sucker_row(*ARM_FL, 58, 20, 1, [0.18, 0.36, 0.54, 0.72], "Front L")
sucker_row(*ARM_FR, 58, 20, -1, [0.18, 0.36, 0.54, 0.72], "Front R")
# two short outer feelers barely clear of the water
ribbon((420, 660), (300, 700), (252, 640), 44, 14, "Feeler L",
       fill="#4A2028", stroke=INK, strokeWidth=4)
ribbon((580, 660), (700, 700), (748, 640), 44, 14, "Feeler R",
       fill="#4A2028", stroke=INK, strokeWidth=4)

# --- eyes: set wide on the mantle flanks, gold and watchful ---------------------------
pair("M386,470 C400,446 436,440 458,456 C462,480 448,500 422,504 "
     "C404,506 390,492 386,470 Z",
     "Eye", fill=rad((0, "#E8C86A"), (0.7, "#B89038"), (1, "#7A5A20")),
     stroke=INK, strokeWidth=5)
pair("M414,458 C424,452 438,454 444,464 C446,478 438,490 424,490 "
     "C412,488 408,470 414,458 Z",
     "Pupil", fill="#160A0C", stroke=NONE)
d.shape("ellipse", "Eye glint L", x=420, y=462, width=8, height=8,
        fill="#FFF4D8", opacity=85, stroke=NONE)
d.shape("ellipse", "Eye glint R", x=572, y=462, width=8, height=8,
        fill="#FFF4D8", opacity=85, stroke=NONE)
# heavy brow folds above the eyes
pair("M378,452 C396,428 436,422 462,440", "Brow", fill=NONE,
     stroke="#3A1418", strokeWidth=8, opacity=70, cap="round")

# beak shadow tucked under the mantle between the front arms
d.path("M470,636 C482,624 518,624 530,636 C526,656 512,668 500,668 "
       "C488,668 474,656 470,636 Z", "Beak shadow", fill="#20090C",
       opacity=80, stroke=INK, strokeWidth=3)

# --- the drowned spar: a snapped mast the sea is taking, lower right -------------------
d.path("M700,640 L792,560", "Broken mast", fill=NONE, stroke="#3A2A1A",
       strokeWidth=11, cap="round")
d.path("M724,608 L776,632", "Spar yard", fill=NONE, stroke="#3A2A1A",
       strokeWidth=7, cap="round")
d.path("M792,560 L806,540 M792,560 L818,556", "Mast splinters", fill=NONE,
       stroke="#3A2A1A", strokeWidth=4, cap="round")
# a tentacle already on it
ribbon((640, 660), (700, 640), (730, 590), 34, 12, "Arm on spar",
       fill="#4A2028", stroke=INK, strokeWidth=4)

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#0A1818", strokeWidth=6)

# --- name ---------------------------------------------------------------------------
d.text("KRAKEN", "Name", x=500, y=962, size=58, font="Virelai Sans",
       color="#D8E8DC", justify="center")

d.finish("kraken-V1R00")
