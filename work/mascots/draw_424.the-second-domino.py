#!/usr/bin/env python3
"""The Second Domino — mascot portrait V1R00. HTTP 424, "Failed Dependency".
Second tile in a row of dominoes beginning to fall; the first is already down.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("The Second Domino — Mascot Portrait", 1000, 1000)

INK = "#38262B"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2A1A24"}, {"offset": 1, "color": "#120A10"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F0E4CE"}, {"offset": 0.7, "color": "#D4B98C"},
    {"offset": 1, "color": "#9A7E54"}]}}
BONE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#FAF4E4"}, {"offset": 0.7, "color": "#E4D6B8"},
    {"offset": 1, "color": "#C2AE8C"}]}}
BONE_DIM = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E2D8C2"}, {"offset": 1, "color": "#A89878"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#8A6E44", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F4E9D2", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(215,225,7),(775,215,6),(245,710,7),(745,700,7),(175,455,6),
                               (830,445,6),(355,155,6),(645,150,7),(310,790,6),(690,785,6)]):
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#8A6E44", opacity=40, stroke=NONE)

# --- tile 4: standing far back, dimmed -------------------------------------------
d.shape("rectangle", "Domino 4", x=782, y=492, width=88, height=226, radius=10,
        fill=BONE_DIM, stroke=INK, strokeWidth=4, opacity=85)
d.path("M788,606 L864,606", "Domino 4 divider", fill=NONE, stroke=INK, strokeWidth=3, opacity=70)
d.shape("ellipse", "D4 pip a", x=815, y=540, width=12, height=12, fill=INK, opacity=70, stroke=NONE)
d.shape("ellipse", "D4 pip b", x=815, y=660, width=12, height=12, fill=INK, opacity=70, stroke=NONE)

# --- tile 3: upright, next to go ---------------------------------------------------
d.shape("ellipse", "D3 shadow", x=648, y=716, width=130, height=18,
        fill="#5E4A30", opacity=45, stroke=NONE)
d.shape("rectangle", "Domino 3", x=652, y=468, width=106, height=250, radius=10,
        fill=BONE_GRAD, stroke=INK, strokeWidth=5)
d.path("M660,593 L750,593", "Domino 3 divider", fill=NONE, stroke=INK, strokeWidth=4)
for i, (x, y) in enumerate([(676,512),(734,512),(676,556),(734,556)]):
    d.shape("ellipse", f"D3 top pip {i+1}", x=x, y=y, width=13, height=13, fill=INK, stroke=NONE)
for i, (x, y) in enumerate([(705,634),(676,676),(734,676)]):
    d.shape("ellipse", f"D3 bot pip {i+1}", x=x, y=y, width=13, height=13, fill=INK, stroke=NONE)
# faint wobble marks at its top — it knows what's coming
d.path("M664,448 C660,440 660,432 664,424 M746,448 C750,440 750,432 746,424",
       "Wobble", fill=NONE, stroke=INK, strokeWidth=4, cap="round", opacity=55)

# --- tile 1: already flat ------------------------------------------------------------
d.shape("ellipse", "D1 shadow", x=178, y=712, width=240, height=20,
        fill="#5E4A30", opacity=50, stroke=NONE)
d.path("M196,676 L412,660 L424,708 L208,726 Z", "Domino 1",
       fill=BONE_DIM, stroke=INK, strokeWidth=5, join="round")
d.path("M300,668 L312,716", "D1 divider", fill=NONE, stroke=INK, strokeWidth=4)
for i, (x, y) in enumerate([(230,690),(258,687),(244,706),(336,682),(372,678)]):
    d.shape("ellipse", f"D1 pip {i+1}", x=x, y=y, width=11, height=9, fill=INK, opacity=80, stroke=NONE)
# dust kicked where it landed
d.shape("ellipse", "Dust 1", x=168, y=690, width=60, height=18, fill="#F0E4CE", opacity=30, stroke=NONE)
d.shape("ellipse", "Dust 2", x=390, y=700, width=52, height=16, fill="#F0E4CE", opacity=25, stroke=NONE)
# impact star at the leading corner
d.path("M212,664 L206,646 M212,664 L230,654 M212,664 L194,672", "Impact star",
       fill=NONE, stroke="#FFF2CF", strokeWidth=4, cap="round", opacity=80)

# --- tile 2: THE SECOND DOMINO, mid-fall ----------------------------------------------
CX, CY, ANG = 522, 585, -33
def rp(dx, dy):
    t = math.radians(ANG); c, s = math.cos(t), math.sin(t)
    return CX + dx*c - dy*s, CY + dx*s + dy*c

d.shape("ellipse", "D2 shadow", x=470, y=712, width=180, height=20,
        fill="#5E4A30", opacity=50, stroke=NONE)
# fall-trail arcs, swept back from the top edge, pivot near the bottom corner
px, py = 572, 706
for i, r in enumerate([196, 218, 240]):
    a0, a1 = math.radians(-121), math.radians(-97)
    x0, y0 = px + r*math.cos(a0), py + r*math.sin(a0)
    x1, y1 = px + r*math.cos(a1), py + r*math.sin(a1)
    d.path(f"M{x0:.0f},{y0:.0f} A{r},{r} 0 0 1 {x1:.0f},{y1:.0f}",
           f"Fall trail {i+1}", fill=NONE, stroke="#F6EAD0",
           strokeWidth=4, opacity=55 - i*12, cap="round")

d.path(rot_rect_path(CX, CY, 112, 250, ANG), "Domino 2",
       fill=BONE_GRAD, stroke=INK, strokeWidth=5)
# face — the mascot, alarmed (upper half in tile-local coords)
ex, ey = rp(-20, -42); d.shape("ellipse", "D2 eye L", x=ex-11, y=ey-13, width=22, height=26, fill=INK, stroke=NONE)
ex, ey = rp(22, -42);  d.shape("ellipse", "D2 eye R", x=ex-11, y=ey-13, width=22, height=26, fill=INK, stroke=NONE)
ex, ey = rp(-24, -46); d.shape("ellipse", "D2 glint L", x=ex, y=ey, width=6, height=6, fill="#FFFFFF", opacity=90, stroke=NONE)
ex, ey = rp(18, -46);  d.shape("ellipse", "D2 glint R", x=ex, y=ey, width=6, height=6, fill="#FFFFFF", opacity=90, stroke=NONE)
bx, by = rp(-30, -66); d.path(f"M{bx-10:.0f},{by+6:.0f} C{bx-3:.0f},{by-6:.0f} {bx+8:.0f},{by-6:.0f} {bx+14:.0f},{by-1:.0f}",
       "D2 brow L", fill=NONE, stroke=INK, strokeWidth=4, cap="round")
bx, by = rp(34, -64);  d.path(f"M{bx-12:.0f},{by-2:.0f} C{bx-4:.0f},{by-8:.0f} {bx+6:.0f},{by-7:.0f} {bx+12:.0f},{by+3:.0f}",
       "D2 brow R", fill=NONE, stroke=INK, strokeWidth=4, cap="round")
mx, my = rp(2, -8)
d.shape("ellipse", "D2 mouth", x=mx-9, y=my-11, width=18, height=22, fill=INK, stroke=NONE)
# sweat drop flicked off the crown
sx, sy = rp(52, -92)
d.path(f"M{sx:.0f},{sy:.0f} C{sx-8:.0f},{sy+12:.0f} {sx-8:.0f},{sy+22:.0f} {sx:.0f},{sy+26:.0f} "
       f"C{sx+8:.0f},{sy+22:.0f} {sx+8:.0f},{sy+12:.0f} {sx:.0f},{sy:.0f} Z",
       "Sweat", fill="#BFE4EE", stroke=INK, strokeWidth=3)
# divider + pips on the lower half
dx0, dy0 = rp(-48, 26); dx1, dy1 = rp(48, 26)
d.path(f"M{dx0:.0f},{dy0:.0f} L{dx1:.0f},{dy1:.0f}", "D2 divider",
       fill=NONE, stroke=INK, strokeWidth=4)
for i, (lx, ly) in enumerate([(-26, 58), (26, 58), (0, 88)]):
    qx, qy = rp(lx, ly)
    d.shape("ellipse", f"D2 pip {i+1}", x=qx-7, y=qy-7, width=14, height=14, fill=INK, stroke=NONE)

# --- name + role ----------------------------------------------------------------------
d.text("THE SECOND DOMINO", "Name", x=500, y=930, size=56, font="Virelai Sans",
       color="#F0E6CE", justify="center")
d.text(" ".join("FAILED DEPENDENCY"), "Role", x=500, y=968, size=23, font="Virelai Sans",
       color="#C4A97C", justify="center")

d.finish("424.the-second-domino-V1R00")
