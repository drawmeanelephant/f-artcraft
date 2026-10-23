#!/usr/bin/env python3
"""Vampire squid — field-guide plate V1R00. The webbed cloak spread face-on:
dark crimson membrane between eight arms, pale globular eyes, cirri spikes
along the arms, two sensory filaments trailing. Deep crimson-on-void.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420; cloak tips and filaments stay inside."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Vampire Squid — Field Plate", 1000, 1000)

INK = "#2A0710"          # near-black maroon
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#0E060A"}, {"offset": 1, "color": "#050204"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4A1622"}, {"offset": 0.55, "color": "#2A0C16"},
    {"offset": 1, "color": "#120510"}]}}
WEB_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#8A2434"}, {"offset": 0.6, "color": "#611526"},
    {"offset": 1, "color": "#3E0C18"}]}}
ARM_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#9A3040"}, {"offset": 1, "color": "#5A1220"}]}}
MANTLE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#93303E"}, {"offset": 0.7, "color": "#641828"},
    {"offset": 1, "color": "#420E1A"}]}}
EYE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F6EAE2"}, {"offset": 0.75, "color": "#DBB4AC"},
    {"offset": 1, "color": "#B98A88"}]}}
PALE = "#E8CEC4"

# --- backdrop + void plate -------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo outer", x=54, y=14, width=892, height=892,
        fill="#8A2434", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate halo inner", x=68, y=28, width=864, height=864,
        fill="#A8344A", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#4A1622", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#9A5A68", strokeWidth=3, opacity=45)
# faint embers + glowing mucus motes in the blackwater
for i, (x, y, w) in enumerate([(200,290,7),(770,250,6),(170,470,8),(825,450,7),(240,690,6),
                               (750,715,8),(150,380,5),(855,560,6),(400,110,6),(605,105,7),
                               (310,160,5),(700,175,6),(335,815,6),(660,820,5),(500,98,5)]):
    d.shape("ellipse", f"Ember {i+1}", x=x, y=y, width=w, height=w,
            fill="#C86A72", opacity=35, stroke=NONE)
for i, (x, y, w) in enumerate([(260,220,5),(720,300,4),(190,600,5),(800,640,4),
                               (450,150,4),(620,700,5),(300,740,4)]):
    d.shape("ellipse", f"Mucus mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#9AD4DC", opacity=55, stroke=NONE)

# --- the cloak: web between eight arms, scalloped rim -----------------------------
C = (500, 460)
TIPS = [(236,362), (247,482), (312,600), (420,688),
        (580,688), (690,598), (753,482), (762,362)]
web = "M404,292 C330,304 268,330 %d,%d" % TIPS[0]
for (x0, y0), (x1, y1) in zip(TIPS, TIPS[1:]):
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    cx, cy = mx + (C[0] - mx) * 0.30, my + (C[1] - my) * 0.30
    web += " Q%.0f,%.0f %d,%d" % (cx, cy, x1, y1)
web += " C740,320 670,300 596,292 C560,286 440,286 404,292 Z"
d.path(web, "Web cloak", fill=WEB_GRAD, stroke=INK, strokeWidth=6)
# inner glow where the head sits + darker rim band hugging the scallops
d.shape("ellipse", "Cloak glow", x=392, y=330, width=216, height=180,
        fill="#B03444", opacity=30, stroke=NONE)
d.path("M300,420 C260,470 300,560 380,620 C430,656 570,656 620,620 "
       "C700,560 740,470 700,420 C730,480 690,570 615,625 "
       "C560,660 440,660 385,625 C310,570 270,480 300,420 Z",
       "Rim shadow", fill="#2E0812", opacity=35, stroke=NONE)

# --- arms: tapered ridges radiating to the tips -----------------------------------
def quad(p0, p1, p2, t):
    u = 1 - t
    x = u*u*p0[0] + 2*u*t*p1[0] + t*t*p2[0]
    y = u*u*p0[1] + 2*u*t*p1[1] + t*t*p2[1]
    dx = 2*u*(p1[0]-p0[0]) + 2*t*(p2[0]-p1[0])
    dy = 2*u*(p1[1]-p0[1]) + 2*t*(p2[1]-p1[1])
    return x, y, dx, dy

ROOT = (500, 452)
def arm(i, tip, w0=34, w1=10, n=18):
    mx, my = (ROOT[0]+tip[0])/2, (ROOT[1]+tip[1])/2
    bow = (tip[0] - 500) * 0.06
    ctrl = (mx + bow, my - 14)
    L, Rr, mid = [], [], []
    for k in range(n + 1):
        t = k / n
        x, y, dx, dy = quad(ROOT, ctrl, tip, t)
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy/ln, dx/ln
        w = (w0 + (w1 - w0) * t) / 2
        mid.append((x, y, nx, ny, dx/ln, dy/ln, w, t))
        L.append((x + nx*w, y + ny*w)); Rr.append((x - nx*w, y - ny*w))
    dd = "M%.1f,%.1f " % L[0] + " ".join("L%.1f,%.1f" % p for p in L[1:])
    dd += " " + " ".join("L%.1f,%.1f" % p for p in reversed(Rr)) + " Z"
    d.path(dd, f"Arm {i+1}", fill=ARM_GRAD, stroke="#3E0C18", strokeWidth=3, opacity=90)
    # pale tip cap — vampire squid arm tips fade light
    x, y, ux, uy = mid[-1][0], mid[-1][1], mid[-1][5], mid[-1][6]
    d.shape("ellipse", f"Arm {i+1} tip", x=x-8, y=y-8, width=16, height=14,
            fill="#D8A8A0", opacity=50, stroke=NONE)
    # cirri: fleshy spikes alternating along both edges
    for j, t in enumerate([0.30, 0.44, 0.58, 0.72, 0.85]):
        x, y, nx, ny, ux, uy, w, _ = mid[round(t*n)]
        for s in (1, -1):
            ex, ey = x + nx*(w+1)*s, y + ny*(w+1)*s
            # spike leans outward + toward the tip
            exx = ex + (nx*s*9 + ux*6)
            eyy = ey + (ny*s*9 + uy*6)
            d.path("M%.1f,%.1f L%.1f,%.1f" % (ex, ey, exx, eyy),
                   f"Arm {i+1} cirrus {j+1}{'a' if s==1 else 'b'}",
                   fill=NONE, stroke=PALE, strokeWidth=3, opacity=75, cap="round")

for i, tip in enumerate(TIPS):
    arm(i, tip)

# --- head + eyes at the cloak's heart ---------------------------------------------
# head/mouth shadow nestled between the arm roots
d.shape("ellipse", "Head shadow", x=442, y=420, width=116, height=84,
        fill="#360A14", opacity=70, stroke=NONE)
for side, ex in (("L", 430), ("R", 512)):
    d.shape("ellipse", f"Eye globe {side}", x=ex, y=346, width=58, height=58,
            fill=EYE_GRAD, stroke=INK, strokeWidth=5)
    d.shape("ellipse", f"Iris {side}", x=ex+16, y=362, width=26, height=26,
            fill="#8A1428", stroke=NONE)
    d.shape("ellipse", f"Eye glint {side}", x=ex+10, y=356, width=13, height=13,
            fill="#FFFFFF", opacity=90, stroke=NONE)
    d.shape("ellipse", f"Eye glint 2 {side}", x=ex+36, y=380, width=6, height=6,
            fill="#FFFFFF", opacity=60, stroke=NONE)
    # lid crease arcing over the globe
    d.path("M%.0f,%.0f C%.0f,%.0f %.0f,%.0f %.0f,%.0f" % (
        ex-4, 368, ex+12, 348, ex+46, 348, ex+62, 368),
        f"Lid {side}", fill=NONE, stroke="#5A1220", strokeWidth=5,
        opacity=65, cap="round")

# --- mantle + ear fins above the cloak rim ------------------------------------------
for s in (1, -1):
    X = lambda v: 500 + (v - 500) * s
    d.path("M%.0f,250 C%.0f,214 %.0f,202 %.0f,200 C%.0f,222 %.0f,254 %.0f,274 Z" % (
        X(452), X(414), X(392), X(390), X(394), X(424), X(456)),
        f"Mantle fin {'L' if s==1 else 'R'}", fill=MANTLE_GRAD,
        stroke=INK, strokeWidth=5)
d.path("M500,178 C560,178 584,224 580,274 C576,314 546,338 500,338 "
       "C454,338 424,314 420,274 C416,224 440,178 500,178 Z",
       "Mantle", fill=MANTLE_GRAD, stroke=INK, strokeWidth=6)
# crown highlight + base shade
d.shape("ellipse", "Mantle highlight", x=452, y=192, width=90, height=44,
        fill="#E8A8A8", opacity=30, stroke=NONE)
d.path("M430,300 C460,326 540,326 570,300 C548,322 452,322 430,300 Z",
       "Mantle shade", fill="#3E0C18", opacity=45, stroke=NONE)
# mantle speckles
for i, (x, y, w) in enumerate([(468,222,5),(528,214,5),(548,254,5),(452,264,5),(502,246,4)]):
    d.shape("ellipse", f"Mantle fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#B03444", opacity=55, stroke=NONE)

# --- sensory filaments: thin trailing threads ---------------------------------------
d.path("M438,648 C380,660 300,690 252,724 C244,730 238,736 234,742",
       "Filament L", fill=NONE, stroke=PALE, strokeWidth=3.5, opacity=80, cap="round")
d.shape("ellipse", "Filament L bead", x=228, y=740, width=9, height=9,
        fill=PALE, opacity=80, stroke=NONE)
d.path("M564,650 C622,664 700,694 748,726 C756,732 762,738 766,744",
       "Filament R", fill=NONE, stroke=PALE, strokeWidth=3.5, opacity=80, cap="round")
d.shape("ellipse", "Filament R bead", x=762, y=742, width=9, height=9,
        fill=PALE, opacity=80, stroke=NONE)

# --- name ---------------------------------------------------------------------------
d.text("VAMPIRE SQUID", "Name", x=500, y=962, size=56, font="Virelai Sans",
       color="#D8A8A0", justify="center")

d.finish("vampire-squid-V1R00")
