#!/usr/bin/env python3
"""Dumbo octopus — field-guide plate V1R00. Full body, face-forward: ear-fins
spread, eight arms joined by a scalloped web, curled arm tips. Soft pink/peach
gradients; abyss-dark backdrop with the plate glowing as the only light.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Dumbo Octopus — Field Plate", 1000, 1000)

INK = "#5A2E3C"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#0C1426"}, {"offset": 1, "color": "#03060E"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#EAF0F6"}, {"offset": 0.55, "color": "#A9C2D6"},
    {"offset": 1, "color": "#4E6B88"}]}}
MANTLE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#FFE3D6"}, {"offset": 0.65, "color": "#F7B9AE"},
    {"offset": 1, "color": "#E08A8E"}]}}
FIN_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F9C4B4"}, {"offset": 1, "color": "#DD8790"}]}}
WEB_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#FBD3C4"}, {"offset": 0.7, "color": "#EFA6A0"},
    {"offset": 1, "color": "#D27582"}]}}
ARM_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F2AFA6"}, {"offset": 1, "color": "#D67D86"}]}}
EYE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#5A3646"}, {"offset": 1, "color": "#1E1118"}]}}

# --- backdrop + glowing plate --------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
# halo: the plate is the only light in the abyss
d.shape("ellipse", "Plate halo outer", x=50, y=10, width=900, height=900,
        fill="#6F95BC", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate halo inner", x=66, y=26, width=868, height=868,
        fill="#8FB2D2", opacity=12, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#3E5873", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#EEF4FA", strokeWidth=3, opacity=50)
# deep-water haze blotches
d.shape("ellipse", "Haze 1", x=170, y=170, width=240, height=140, fill="#C9DAE8", opacity=22, stroke=NONE)
d.shape("ellipse", "Haze 2", x=560, y=620, width=240, height=130, fill="#7F9AB4", opacity=18, stroke=NONE)
# marine snow drifting through the light
for i, (x, y, w) in enumerate([(190,300,7),(780,250,6),(160,470,8),(830,450,7),(230,700,6),(760,720,8),
                               (140,380,5),(865,560,6),(400,110,6),(610,105,7),(300,160,5),(700,170,6),
                               (330,820,6),(660,825,5),(120,560,5),(880,340,5),(500,96,5),(210,620,4)]):
    d.shape("ellipse", f"Marine snow {i+1}", x=x, y=y, width=w, height=w,
            fill="#FFFFFF", opacity=45, stroke=NONE)

# --- soft shadow below the body -----------------------------------------------
d.shape("ellipse", "Body shadow", x=300, y=772, width=400, height=40,
        fill="#2F4660", opacity=22, stroke=NONE)

# --- ear-fins (behind mantle) --------------------------------------------------
def mirror(dd_pts):
    return [(1000 - x, y) for x, y in dd_pts]

def fin(label, pts):
    (a, b, c, e, f, g, h, i, j, k) = pts
    d.path("M%d,%d C%d,%d %d,%d %d,%d C%d,%d %d,%d %d,%d C%d,%d %d,%d %d,%d Z" % (
        a[0], a[1], b[0], b[1], c[0], c[1], e[0], e[1], f[0], f[1], g[0], g[1], h[0], h[1],
        i[0], i[1], j[0], j[1], k[0], k[1]),
        label, fill=FIN_GRAD, stroke=INK, strokeWidth=6)

FIN_L = [(352,282), (300,226), (222,206), (190,244), (162,280), (180,342),
         (236,368), (274,384), (318,386), (344,374)]
fin("Fin L", FIN_L)
fin("Fin R", mirror(FIN_L))
# fin ribs + rim light (translucent)
for side, s in (("L", 1), ("R", -1)):
    X = lambda x: x if s == 1 else 1000 - x
    for j, (p, q, r_) in enumerate([((340,300),(280,262),(214,252)),
                                    ((338,330),(270,312),(196,300)),
                                    ((338,356),(282,356),(226,344))]):
        d.path(f"M{X(p[0])},{p[1]} Q{X(q[0])},{q[1]} {X(r_[0])},{r_[1]}",
               f"Fin {side} rib {j+1}", fill=NONE, stroke="#C46A78",
               strokeWidth=4, opacity=35, cap="round")
    d.path(f"M{X(222)},{236} C{X(254)},{228} {X(294)},{242} {X(324)},{274}",
           f"Fin {side} rim light", fill=NONE, stroke="#FFF1E8",
           strokeWidth=6, opacity=45, cap="round")

# --- webbed arm skirt -----------------------------------------------------------
TIPS = [(200,590), (262,684), (354,742), (454,768), (546,768), (646,742), (738,684), (800,590)]
WC = (500, 540)
web = "M346,410 C300,446 236,512 %d,%d" % TIPS[0]
for (x0, y0), (x1, y1) in zip(TIPS, TIPS[1:]):
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    cx, cy = mx + (WC[0] - mx) * 0.32, my + (WC[1] - my) * 0.32
    web += " Q%.0f,%.0f %d,%d" % (cx, cy, x1, y1)
web += " C764,512 700,446 654,410 Z"
d.path(web, "Web", fill=WEB_GRAD, stroke=INK, strokeWidth=6)
# translucent darker band hugging the scalloped edge, lighter centre
d.shape("ellipse", "Web glow", x=360, y=470, width=280, height=180,
        fill="#FFEDE4", opacity=28, stroke=NONE)

# --- arms: tapered ribbons on the web, suckers, curled tips ----------------------
def quad(p0, p1, p2, t):
    u = 1 - t
    x = u*u*p0[0] + 2*u*t*p1[0] + t*t*p2[0]
    y = u*u*p0[1] + 2*u*t*p1[1] + t*t*p2[1]
    dx = 2*u*(p1[0]-p0[0]) + 2*t*(p2[0]-p1[0])
    dy = 2*u*(p1[1]-p0[1]) + 2*t*(p2[1]-p1[1])
    return x, y, dx, dy

def arm(i, root, tip, w0=30, w1=9, n=20):
    mx, my = (root[0] + tip[0]) / 2, (root[1] + tip[1]) / 2
    bend = (tip[0] - 500) * 0.18
    ctrl = (mx + bend, my - abs(tip[0] - 500) * 0.12)
    L, Rr, mid = [], [], []
    for k in range(n + 1):
        t = k / n
        x, y, dx, dy = quad(root, ctrl, tip, t)
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy/ln, dx/ln
        w = (w0 + (w1 - w0) * t) / 2
        mid.append((x, y, dx/ln, dy/ln, w))
        L.append((x + nx*w, y + ny*w)); Rr.append((x - nx*w, y - ny*w))
    dd = "M%.1f,%.1f " % L[0] + " ".join("L%.1f,%.1f" % p for p in L[1:])
    dd += " " + " ".join("L%.1f,%.1f" % p for p in reversed(Rr)) + " Z"
    d.path(dd, f"Arm {i+1}", fill=ARM_GRAD, stroke="#B5606E", strokeWidth=3, opacity=85)
    # sucker row
    for j, t in enumerate([0.36, 0.50, 0.63, 0.75, 0.86]):
        x, y, _, _, w = mid[round(t*n)]
        s = max(4, w * 0.62)
        d.shape("ellipse", f"Arm {i+1} sucker {j+1}", x=round(x - s/2), y=round(y - s/2),
                width=round(s), height=round(s), fill="#FFF0E6", opacity=55, stroke=NONE)
    # curled tip past the web edge, curling outward
    x, y, ux, uy, _ = mid[-1]
    side = 1 if tip[0] >= 500 else -1
    px, py = -uy*side, ux*side
    p1 = (x + ux*18, y + uy*18)
    p2 = (x + ux*26 + px*16, y + uy*26 + py*16)
    p3 = (x + ux*14 + px*24, y + uy*14 + py*24)
    d.path("M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (x, y, p1[0], p1[1], p2[0], p2[1], p3[0], p3[1]),
           f"Arm {i+1} curl", fill=NONE, stroke="#D67D86", strokeWidth=8, cap="round")
    d.path("M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (x, y, p1[0], p1[1], p2[0], p2[1], p3[0], p3[1]),
           f"Arm {i+1} curl light", fill=NONE, stroke="#FFE6DC", strokeWidth=3, opacity=50, cap="round")

ROOTS = [(404 + k * 27.4, 486) for k in range(8)]
for i in (0, 7, 1, 6, 2, 5, 3, 4):
    arm(i, ROOTS[i], TIPS[i])

# --- mantle (the "head") ----------------------------------------------------------
d.path("M500,172 C606,172 668,252 668,352 C668,430 630,482 570,500 "
       "C540,508 460,508 430,500 C370,482 332,430 332,352 C332,252 394,172 500,172 Z",
       "Mantle", fill=MANTLE_GRAD, stroke=INK, strokeWidth=7)
# lower shadow + crown highlight
d.path("M346,420 C372,476 430,500 500,502 C570,500 628,476 654,420 "
       "C620,462 566,482 500,484 C434,482 380,462 346,420 Z",
       "Mantle shade", fill="#C76B7C", opacity=32, stroke=NONE)
d.shape("ellipse", "Mantle highlight", x=392, y=196, width=150, height=78,
        fill="#FFFFFF", opacity=30, stroke=NONE)
d.shape("ellipse", "Mantle highlight small", x=560, y=214, width=46, height=26,
        fill="#FFFFFF", opacity=22, stroke=NONE)
# freckles
for i, (x, y, w) in enumerate([(430,262,7),(470,236,5),(552,248,6),(596,286,7),(404,318,5),
                               (612,340,6),(500,300,5),(450,332,4),(560,318,4)]):
    d.shape("ellipse", f"Freckle {i+1}", x=x, y=y, width=w, height=w,
            fill="#D98A8E", opacity=50, stroke=NONE)

# --- face -------------------------------------------------------------------------
for side, ex in (("L", 404), ("R", 548)):
    d.shape("ellipse", f"Eye socket {side}", x=ex - 8, y=376, width=64, height=70,
            fill="#E59A9C", opacity=40, stroke=NONE)
    d.shape("ellipse", f"Eye {side}", x=ex, y=384, width=48, height=54,
            fill=EYE_GRAD, stroke=INK, strokeWidth=4)
    d.shape("ellipse", f"Glint {side}", x=ex + 10, y=394, width=14, height=14,
            fill="#FFFFFF", opacity=92, stroke=NONE)
    d.shape("ellipse", f"Glint small {side}", x=ex + 30, y=420, width=6, height=6,
            fill="#FFFFFF", opacity=70, stroke=NONE)
    d.path(f"M{ex - 4},{386} C{ex + 10},{370} {ex + 38},{370} {ex + 52},{386}",
           f"Lid {side}", fill=NONE, stroke=INK, strokeWidth=5, cap="round")
    d.shape("ellipse", f"Blush {side}", x=ex - 14 if side == "L" else ex + 26, y=446,
            width=36, height=18, fill="#F08A96", opacity=40, stroke=NONE)

# --- name ---------------------------------------------------------------------------
d.text("DUMBO OCTOPUS", "Name", x=500, y=960, size=48, font="Virelai Sans",
       color="#DCE6F0", justify="center")

d.finish("dumbo-octopus-V1R00")
