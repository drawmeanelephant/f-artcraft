#!/usr/bin/env python3
"""Cassowary — field-guide plate V1R00. Head-and-neck bust, profile facing left:
the tall horn casque, electric-blue bare skin with a violet-to-crimson nape,
two crimson wattles hanging from the throat, glossy hair-like black plumage
closing on the disc's own arc. Rainforest-understorey plate with fern fronds.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Cassowary — Field Plate", 1000, 1000)

INK = "#141820"
CX, CY, R = 500, 460, 420
BG_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#14261C"}, {"offset": 1, "color": "#060D09"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#EEF0D6"}, {"offset": 0.65, "color": "#B9CBA0"},
    {"offset": 1, "color": "#6C8A66"}]}}
FROND_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#5E8A58"}, {"offset": 1, "color": "#3A5E3C"}]}}
CASQUE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6A5A40"}, {"offset": 0.45, "color": "#A8946A"},
    {"offset": 1, "color": "#4E4230"}]}}
SKIN_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#7FD0F4"}, {"offset": 0.55, "color": "#2E9AD8"},
    {"offset": 1, "color": "#1A5CA8"}]}}
NAPE_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#6A48B8"}, {"offset": 0.55, "color": "#8A3A9E"},
    {"offset": 1, "color": "#C42A44"}]}}
WATTLE_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#E8475A"}, {"offset": 1, "color": "#A3142C"}]}}
WATTLE_FAR_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#B82A40"}, {"offset": 1, "color": "#76101F"}]}}
BILL_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#4A4C52"}, {"offset": 1, "color": "#16171B"}]}}
PLUME_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#2A2E38"}, {"offset": 1, "color": "#08090C"}]}}
IRIS_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E8A050"}, {"offset": 0.7, "color": "#A85A24"},
    {"offset": 1, "color": "#5E2E10"}]}}

def chord_x(y, r=R):
    h = math.sqrt(r*r - (y - CY)**2)
    return CX - h, CX + h

def inside(x, y, r=386):
    dx, dy = x - CX, y - CY
    k = math.hypot(dx, dy)
    return (x, y) if k <= r else (CX + dx*r/k, CY + dy*r/k)

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#4A6A48", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F4F6E4", strokeWidth=3, opacity=55)
# dappled canopy light
for i, (x, y, w, h, o) in enumerate([(560,140,150,90,22),(650,250,110,70,18),(200,230,130,80,16),
                                     (300,140,90,56,14),(700,420,90,60,14)]):
    d.shape("ellipse", f"Dapple {i+1}", x=x, y=y, width=w, height=h, fill="#FFFBE0", opacity=o, stroke=NONE)

# fern fronds: midrib + paired leaflets, every point pulled inside the inner ring
def frond(label, p0, p1, p2, n, length, op):
    d.path(f"M{p0[0]},{p0[1]} Q{p1[0]},{p1[1]} {p2[0]},{p2[1]}", f"{label} rib",
           fill=NONE, stroke="#3A5E3C", strokeWidth=5, opacity=op, cap="round")
    for k in range(1, n):
        t = k / n
        u = 1 - t
        x = u*u*p0[0] + 2*u*t*p1[0] + t*t*p2[0]
        y = u*u*p0[1] + 2*u*t*p1[1] + t*t*p2[1]
        tx = 2*u*(p1[0]-p0[0]) + 2*t*(p2[0]-p1[0])
        ty = 2*u*(p1[1]-p0[1]) + 2*t*(p2[1]-p1[1])
        ln = math.hypot(tx, ty) or 1
        ux, uy = tx/ln, ty/ln
        L = length * (1 - t*0.7)
        for s in (1, -1):
            nx, ny = -uy*s, ux*s
            ex, ey = inside(x + (nx*0.9 + ux*0.45)*L, y + (ny*0.9 + uy*0.45)*L)
            mx, my = x + nx*L*0.5 - ux*L*0.05, y + ny*L*0.5 - uy*L*0.05
            wx, wy = -(ey - y), ex - x
            wl = math.hypot(wx, wy) or 1
            wx, wy = wx/wl*L*0.22, wy/wl*L*0.22
            d.path(f"M{x:.0f},{y:.0f} Q{mx + wx:.0f},{my + wy:.0f} {ex:.0f},{ey:.0f} "
                   f"Q{mx - wx:.0f},{my - wy:.0f} {x:.0f},{y:.0f} Z",
                   f"{label} leaflet {k}{'a' if s > 0 else 'b'}", fill=FROND_GRAD, opacity=op, stroke=NONE)

frond("Frond L1", (150, 640), (180, 420), (300, 230), 9, 60, 55)
frond("Frond L2", (200, 720), (150, 560), (170, 420), 7, 46, 38)
frond("Frond R1", (850, 620), (830, 420), (700, 230), 9, 60, 55)
frond("Frond R2", (800, 720), (860, 560), (840, 420), 7, 46, 38)

# --- casque: tall horn helmet, laterally flattened ----------------------------------
# broad base from forehead to crown, peak swept back like a helmet crest
d.path("M366,384 C362,330 382,262 420,212 C446,178 484,166 508,184 "
       "C532,204 532,282 522,362 Z",
       "Casque", fill=CASQUE_GRAD, stroke=INK, strokeWidth=6)
for i, dd in enumerate(["M392,350 C392,300 408,250 436,212", "M424,346 C426,296 440,248 462,200",
                        "M456,346 C460,298 472,246 486,194", "M488,350 C494,304 502,252 508,206"]):
    d.path(dd, f"Casque striation {i+1}", fill=NONE, stroke="#3E3424", strokeWidth=3, opacity=32, cap="round")
d.path("M390,316 C392,270 408,232 436,202", "Casque sheen", fill=NONE,
       stroke="#F2E6C4", strokeWidth=8, opacity=35, cap="round")
d.path("M446,186 C466,174 490,174 502,188", "Casque crown light", fill=NONE,
       stroke="#F2E6C4", strokeWidth=5, opacity=40, cap="round")
d.path("M516,250 C520,290 518,330 512,360", "Casque back shade", fill=NONE,
       stroke="#2E261A", strokeWidth=8, opacity=30, cap="round")
for i, (x, y, w, h) in enumerate([(430,240,26,16),(470,280,22,14),(410,300,18,12),(486,224,16,12)]):
    d.shape("ellipse", f"Casque mottle {i+1}", x=x, y=y, width=w, height=h,
            fill="#3E3424", opacity=22, stroke=NONE)


# --- bill -------------------------------------------------------------------------------
d.path("M384,396 C334,394 294,400 254,414 C250,418 252,422 258,422 "
       "C292,424 330,426 384,432 Z",
       "Upper bill", fill=BILL_GRAD, stroke=INK, strokeWidth=4)
d.path("M382,432 C330,430 296,430 266,426 C290,436 330,442 382,448 Z",
       "Lower bill", fill=BILL_GRAD, stroke=INK, strokeWidth=3)
d.path("M362,400 C330,398 298,404 270,412", "Bill sheen", fill=NONE,
       stroke="#B8BCC6", strokeWidth=3, opacity=45, cap="round")
d.shape("ellipse", "Nostril", x=300, y=406, width=14, height=6, fill="#0A0B0E", opacity=80, stroke=NONE)
# --- head + neck: bare, electric-blue skin ---------------------------------------------
d.path("M358,404 C366,352 404,326 448,324 C500,324 530,360 530,414 "
       "C532,478 548,560 582,660 L330,660 C342,580 352,506 368,456 "
       "C360,440 354,422 358,404 Z",
       "Head and neck", fill=SKIN_GRAD, stroke=INK, strokeWidth=7)
# violet-to-crimson nape running down the back of the neck
# two layers: a wide faint wash feathers the front edge of the colour band
d.path("M506,356 C528,380 532,420 532,470 C536,540 556,600 582,660 "
       "L462,660 C460,600 462,540 466,486 C470,430 484,390 506,356 Z",
       "Nape colour wash", fill=NAPE_GRAD, opacity=35, stroke=NONE)
d.path("M512,370 C528,394 532,430 532,470 C536,540 556,600 582,660 "
       "L496,660 C490,600 488,540 490,490 C492,440 500,400 512,370 Z",
       "Nape colour", fill=NAPE_GRAD, opacity=80, stroke=NONE)
d.path("M530,414 C532,478 548,560 582,660", "Nape edge", fill=NONE,
       stroke=INK, strokeWidth=7, cap="round")
# skin folds + sheen
for i, dd in enumerate(["M380,470 C410,480 450,482 486,474", "M370,520 C410,532 456,534 494,524",
                        "M360,574 C404,588 456,590 500,580"]):
    d.path(dd, f"Neck fold {i+1}", fill=NONE, stroke="#123E78", strokeWidth=3, opacity=22, cap="round")
d.path("M400,350 C430,334 470,332 500,346", "Crown sheen", fill=NONE,
       stroke="#E0F6FF", strokeWidth=7, opacity=40, cap="round")
d.path("M384,480 C374,530 364,590 356,640", "Throat sheen", fill=NONE,
       stroke="#C8F0FF", strokeWidth=8, opacity=30, cap="round")
d.shape("ellipse", "Cheek glow", x=404, y=402, width=70, height=46, fill="#B8ECFF", opacity=28, stroke=NONE)
# ear opening
d.shape("ellipse", "Ear", x=470, y=388, width=16, height=20, fill="#0E2E5A", opacity=70, stroke=NONE)

# --- eye: red-brown iris under a lidded brow ------------------------------------------------
d.shape("ellipse", "Eye socket", x=400, y=366, width=44, height=38, fill="#123E78", opacity=35, stroke=NONE)
d.shape("ellipse", "Iris", x=408, y=372, width=28, height=26, fill=IRIS_GRAD, stroke=INK, strokeWidth=3)
d.shape("ellipse", "Pupil", x=417, y=380, width=10, height=10, fill="#0A0806", stroke=NONE)
d.shape("ellipse", "Eye glint", x=413, y=376, width=6, height=5, fill="#FFFFFF", opacity=90, stroke=NONE)
d.path("M400,374 C412,362 432,362 446,372", "Brow", fill=NONE, stroke=INK, strokeWidth=5, cap="round")


# --- far wattle: hangs beside the near one, darker, half hidden ------------------------
d.path("M396,468 C412,500 420,548 412,592 C406,620 386,626 380,604 "
       "C374,576 380,524 384,474 Z",
       "Wattle far", fill=WATTLE_FAR_GRAD, stroke=INK, strokeWidth=4)
d.path("M400,500 C406,536 406,570 400,598", "Wattle far sheen", fill=NONE,
       stroke="#F08A98", strokeWidth=3, opacity=35, cap="round")
# --- near wattle: crimson, hanging from the throat -------------------------------------------
d.path("M370,454 C356,486 344,530 346,574 C348,612 372,628 386,606 "
       "C398,584 392,530 386,480 Z",
       "Wattle near", fill=WATTLE_GRAD, stroke=INK, strokeWidth=5)
d.path("M366,486 C358,520 356,560 362,596", "Wattle sheen", fill=NONE,
       stroke="#FFC4CC", strokeWidth=4, opacity=45, cap="round")
d.path("M380,500 C384,540 384,576 378,600", "Wattle shade", fill=NONE,
       stroke="#6E0A1A", strokeWidth=4, opacity=35, cap="round")

# --- glossy black plumage: hair-like, closed on the disc's own arc -------------------------
py = 744
pl, pr = chord_x(py, 417)
# ragged, hair-like collar: curved spikes of uneven height swept back (right)
collar = ""
xs = list(range(306, 650, 22))
for k, x in enumerate(xs):
    tip_h = [34, 52, 28, 46, 60, 30, 42, 56, 26, 48, 38, 58, 32, 44, 50, 30][k % 16]
    base_y = 636 + abs(x - 470) * 0.06
    lean = [14, 8, 20, 4, 16, 24, 10, 18, 6, 22, 12, 2, 18, 10, 26, 8][k % 16]
    tx, ty = x + lean, base_y - tip_h
    nx = x + 22
    collar += (f" Q{x + 2:.0f},{base_y - tip_h*0.5:.0f} {tx:.0f},{ty:.0f}"
               f" Q{x + 12:.0f},{base_y - tip_h*0.35:.0f} {nx:.0f},{base_y + 4:.0f}")
d.path(f"M{pl:.1f},{py} C{pl+10:.0f},690 248,650 306,{636 + 164*0.06:.0f}" + collar +
       f" C{700:.0f},656 {pr-10:.0f},690 {pr:.1f},{py} A417,417 0 0 1 {pl:.1f},{py} Z",
       "Plumage", fill=PLUME_GRAD, stroke=INK, strokeWidth=5)
# hair-like feather strands with a blue-black gloss, all kept inside the plumage mass
for i in range(26):
    x0 = 270 + i*18
    y0 = 652 + abs(x0 - 480) * 0.10 + (i % 3) * 8
    sway = (x0 - 480) * 0.16
    x1, y1 = inside(x0 + sway, y0 + 150 + (i % 4) * 18, r=404)
    d.path(f"M{x0:.0f},{y0:.0f} C{x0 + sway*0.2:.0f},{y0 + 50:.0f} {x0 + sway*0.7:.0f},{y1 - 50:.0f} {x1:.0f},{y1:.0f}",
           f"Plume strand {i+1}", fill=NONE, stroke="#000000" if i % 2 else "#3A4258",
           strokeWidth=3 if i % 3 else 4, opacity=60, cap="round")
for i, dd in enumerate(["M280,700 C320,676 362,664 404,660", "M572,664 C620,674 666,694 706,722",
                        "M410,716 C460,704 520,704 568,716", "M236,744 C260,722 290,708 320,700"]):
    d.path(dd, f"Plume gloss {i+1}", fill=NONE, stroke="#6E86B4", strokeWidth=7, opacity=28, cap="round")

# --- name ----------------------------------------------------------------------
d.text("CASSOWARY", "Name", x=500, y=962, size=58, font="Virelai Sans",
       color="#E0EAD6", justify="center")

d.finish("cassowary-V1R00")
