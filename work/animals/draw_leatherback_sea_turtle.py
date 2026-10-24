#!/usr/bin/env python3
"""Leatherback sea turtle — field plate V1R00. A turtle built like a diving
bell: dark leathery carapace with seven longitudinal keels and pale mottle,
the signature long sickle fore-flippers spread mid-stroke, head down on the
dive toward a moon-jelly bloom. Open-ocean plate, no floor — depth vignette
closing on the disc's own arc. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Leatherback Sea Turtle — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#181410"


def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}


def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}


def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad


def rim_x(y, side=-1):
    return PCX + side * math.sqrt(PR * PR - (y - PCY) ** 2)


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


# --- palette ---------------------------------------------------------------------
BG_GRAD = lin(0, 0, 0, 1000, (0, "#061420"), (1, "#02070C"))
PLATE_GRAD = rad((0, "#24506E"), (0.55, "#123248"), (1, "#071524"))
SHELL = lin(360, 300, 640, 640, (0, "#3A5468"), (0.5, "#223749"), (1, "#101D29"))
SHELL_DIM = lin(400, 300, 660, 620, (0, "#2A4052"), (1, "#0E1822"))
FLIPPER = lin(400, 400, 640, 700, (0, "#33485C"), (0.6, "#1E303F"), (1, "#0E1820"))
KEEL = "#9CB4C6"
MOTTLE = "#D8E2DC"
JELLY = "#C8DCF0"
FLOOR = lin(0, 660, 0, 880, (0, "#0A1E30"), (1, "#030A12"))

# --- backdrop + plate ----------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=58, y=18, width=884, height=884, fill="#6EA8D0", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#081C2E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#7FA8CC", strokeWidth=3, opacity=35)

# god-rays leaning down from the top of the disc
for i, (x0, x1, wd) in enumerate([(300, 385, 60), (470, 545, 80), (620, 690, 55)]):
    d.path(f"M{x0},{PCY - PR + 6} L{x1},{PCY - PR + 6} L{x1 + wd},{PCY + 300} "
           f"L{x0 + wd * 0.4},{PCY + 300} Z",
           f"Ray {i+1}", fill="#A8CCF0", opacity=7, stroke=NONE)

# marine snow
for i, (x, y, w) in enumerate([(250, 240, 5), (400, 180, 6), (560, 150, 4), (700, 220, 6),
                               (790, 350, 5), (200, 420, 5), (300, 560, 4), (620, 640, 5),
                               (760, 560, 6), (440, 700, 4), (180, 300, 4), (840, 460, 4),
                               (680, 120, 5), (360, 360, 3), (580, 480, 3)]):
    assert on_disc(x, y, 16), i
    d.shape("ellipse", f"Snow {i+1}", x=x, y=y, width=w, height=w,
            fill="#C8DCF0", opacity=26, stroke=NONE)

# depth vignette closing on the disc arc — open ocean, no floor
dy = 700
dl, dr = rim_x(dy, -1), rim_x(dy, 1)
d.path(f"M{dl:.1f},{dy} C360,{dy - 14} 640,{dy - 14} {dr:.1f},{dy} "
       f"A{PR},{PR} 0 0 1 {dl:.1f},{dy} Z", "Depth shade", fill=FLOOR,
       opacity=60, stroke=NONE)

# --- the jelly bloom ------------------------------------------------------------------
def jelly(cx, cy, r, op, label):
    d.path(f"M{cx - r},{cy} C{cx - r},{cy - r * 1.15} {cx + r},{cy - r * 1.15} {cx + r},{cy} "
           f"Q{cx + r * 0.5},{cy + r * 0.18} {cx},{cy + r * 0.14} "
           f"Q{cx - r * 0.5},{cy + r * 0.18} {cx - r},{cy} Z",
           f"{label} bell", fill=JELLY, opacity=op, stroke=NONE)
    d.shape("ellipse", f"{label} ring", x=cx - r * 0.42, y=cy - r * 0.62,
            width=r * 0.84, height=r * 0.5, fill=NONE, stroke=JELLY,
            strokeWidth=2.6, opacity=min(op + 12, 60))
    for j in range(5):
        x = cx - r * 0.8 + j * r * 0.4
        d.path(f"M{x:.0f},{cy + r * 0.1:.0f} q3,{r * 0.5:.0f} {(-1) ** j * 6},{r * 0.8:.0f}",
               f"{label} arm {j+1}", fill=NONE, stroke=JELLY, strokeWidth=2,
               opacity=min(op + 8, 55), cap="round")


jelly(265, 300, 58, 16, "Jelly far L")
jelly(720, 200, 44, 14, "Jelly far R")
jelly(830, 520, 36, 13, "Jelly mid R")
jelly(220, 560, 40, 15, "Jelly mid L")

# --- the turtle ----------------------------------------------------------------------
# shell axis: rear tip up-left, neck down-right — the dive
C = (500, 430)
U = (math.cos(math.radians(35)), math.sin(math.radians(35)))     # tail -> head
N = (-U[1], U[0])

def P(s, t):
    return (C[0] + U[0] * s + N[0] * t, C[1] + U[1] * s + N[1] * t)

# (hind flippers and tail trail behind the shell's taper in this view —
#  anything attached at the tip reads as an antenna, so the taper stays clean)

# far fore-flipper sweeping up-right, mostly behind the shell
d.path(smooth([(636, 372), (688, 330), (748, 288), (806, 258), (820, 262),
               (792, 292), (726, 342), (664, 400), (642, 414)]),
       "Flipper far", fill=SHELL_DIM, stroke=INK, strokeWidth=5)

# carapace — the domed teardrop
shell_pts = [P(-192, 0), P(-138, 62), P(-40, 124), P(80, 128), P(168, 48),
             P(190, 0), P(168, -48), P(80, -128), P(-40, -124), P(-138, -62)]
d.path(smooth(shell_pts), "Carapace", fill=SHELL, stroke=INK, strokeWidth=6)
# sheen along the upper-left dome
d.shape("ellipse", "Shell sheen", x=390, y=330, width=230, height=90,
        fill="#7E9AB0", opacity=16, stroke=NONE)
# under-rim shadow on the lower-right edge
d.path(smooth([P(150, 52), P(80, 122), P(-30, 120), P(60, 132), P(140, 62)]),
       "Shell edge shade", fill="#0A141E", opacity=45, stroke=NONE)

# seven keels — pale ridges fanning along the dome
for i, t in enumerate((-96, -58, -22, 0, 22, 58, 96)):
    if not t:
        pth = f"M{P(-160, 0)[0]:.0f},{P(-160, 0)[1]:.0f} L{P(150, 0)[0]:.0f},{P(150, 0)[1]:.0f}"
    else:
        a = P(-150, t * 0.45); b = P(-20, t * 1.12); c = P(140, t * 0.92)
        pth = f"M{a[0]:.0f},{a[1]:.0f} Q{b[0]:.0f},{b[1]:.0f} {c[0]:.0f},{c[1]:.0f}"
    d.path(pth, f"Keel {i+1}", fill=NONE, stroke=KEEL,
           strokeWidth=4.5 if t else 5.5,
           opacity=55 if abs(t) < 90 else 38, cap="round")

# pale mottle — leatherback spots, denser toward the edges
for i, (s, t, w) in enumerate([(-120, 40, 10), (-90, -70, 8), (-60, 90, 9), (-30, -90, 8),
                               (0, 60, 10), (30, -40, 7), (60, 95, 8), (90, -80, 9),
                               (-140, -30, 8), (-100, 70, 7), (-40, 30, 6), (20, 110, 8),
                               (110, 40, 7), (120, -30, 6), (-10, -120, 8), (60, -110, 7),
                               (-70, -20, 6), (40, 20, 5), (-160, 10, 7), (130, 70, 6)]):
    x, y = P(s, t)
    d.shape("ellipse", f"Mottle {i+1}", x=x - w / 2, y=y - w / 3, width=w, height=w * 0.7,
            fill=MOTTLE, opacity=42, stroke=NONE)

# near fore-flipper — the long sickle sweeping down-left
d.path(smooth([(588, 508), (545, 568), (485, 640), (420, 695), (378, 718),
               (368, 732), (388, 732), (452, 698), (522, 632), (565, 566),
               (575, 540)]),
       "Flipper near", fill=FLIPPER, stroke=INK, strokeWidth=5.5)
# pale leading-edge glint + mottle at the base
d.path("M585,520 C545,578 480,652 398,712", "Flipper glint", fill=NONE,
       stroke="#8FA8BC", strokeWidth=4, opacity=45, cap="round")
d.shape("ellipse", "Flipper mottle", x=530, y=585, width=40, height=16,
        fill=MOTTLE, opacity=30, stroke=NONE)

# neck + head tucked close under the shell edge — leatherback necks are short
d.path(smooth([(610, 545), (640, 565), (668, 585), (686, 602), (682, 618),
               (656, 610), (628, 592), (598, 575)]),
       "Neck", fill=FLIPPER, stroke=INK, strokeWidth=4.5)
d.path(smooth([(680, 598), (700, 602), (718, 612), (726, 626), (718, 638),
               (698, 636), (680, 626), (674, 612)]),
       "Head", fill=FLIPPER, stroke=INK, strokeWidth=4.5)
# pale throat patch — the leatherback's light underside, kept under the jaw
d.path(smooth([(684, 618), (700, 630), (714, 638), (704, 644),
               (688, 634), (678, 624)]),
       "Throat patch", fill=MOTTLE, opacity=35, stroke=NONE)
# eye + snout shading
d.shape("ellipse", "Eye", x=696, y=612, width=12, height=10, fill="#0A0C10", stroke=NONE)
d.shape("ellipse", "Eye glint", x=699, y=614, width=4, height=4, fill="#C8DCF0", opacity=80, stroke=NONE)
d.path("M718,622 C724,624 727,629 725,634", "Snout shade", fill=NONE,
       stroke="#0A141E", strokeWidth=3.5, opacity=70, cap="round")
# neck mottle flecks
for i, (x, y, w) in enumerate([(620, 572, 7), (648, 596, 6), (676, 614, 6)]):
    d.shape("ellipse", f"Neck fleck {i+1}", x=x, y=y, width=w, height=w * 0.7,
            fill=MOTTLE, opacity=45, stroke=NONE)

# two bloom members up front — one just beyond the head, one low-left foreground
jelly(798, 700, 62, 20, "Jelly prey")
jelly(330, 800, 50, 17, "Jelly front")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#081C2E", strokeWidth=6)

# --- name ------------------------------------------------------------------------------
d.text("LEATHERBACK SEA TURTLE", "Name", x=500, y=962, size=46,
       font="Virelai Sans", color="#C4D8E8", justify="center")

d.finish("leatherback-sea-turtle-V1R00")
