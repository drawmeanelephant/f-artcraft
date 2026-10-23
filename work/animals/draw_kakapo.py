#!/usr/bin/env python3
"""Kakapo — field-guide plate V1R00. Face-forward head/bust portrait with a
gentle, puzzled head tilt: big round moss-green face, owl-like buff facial disc
of fine radiating feathers, whiskery vibrissae around a pale hooked beak, dark
round eyes under mismatched brows. Moss/fern palette, night-forest backdrop.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os, math, re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Kakapo — Field Plate", 1000, 1000)

INK = "#2C3A22"
CX, CY = 500, 460          # plate disc centre (r=420)
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1E2E20"}, {"offset": 1, "color": "#0A130C"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E6EED2"}, {"offset": 0.7, "color": "#C2D4A2"},
    {"offset": 1, "color": "#8AA46C"}]}}
HEAD_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#B4CF72"}, {"offset": 0.65, "color": "#86A84A"},
    {"offset": 1, "color": "#557632"}]}}
BODY_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#A7C566"}, {"offset": 0.6, "color": "#7A9C42"},
    {"offset": 1, "color": "#4A682C"}]}}
DISC_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#EAE6B4"}, {"offset": 0.65, "color": "#CFC98A"},
    {"offset": 1, "color": "#A6A060"}]}}
BEAK_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#BDB79C"}, {"offset": 0.5, "color": "#F2EEDC"},
    {"offset": 1, "color": "#B3AD90"}]}}
FROND_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6E9046"}, {"offset": 1, "color": "#4A6A2E"}]}}

def disc_x(y, side, r=416):
    return CX + side*math.sqrt(r*r - (y - CY)**2)

def ell(cx, cy, rx, ry):
    """Ellipse as four cubics, so it survives the head-tilt point transform."""
    k = 0.5523
    return (f"M{cx+rx},{cy} C{cx+rx},{cy+k*ry} {cx+k*rx},{cy+ry} {cx},{cy+ry} "
            f"C{cx-k*rx},{cy+ry} {cx-rx},{cy+k*ry} {cx-rx},{cy} "
            f"C{cx-rx},{cy-k*ry} {cx-k*rx},{cy-ry} {cx},{cy-ry} "
            f"C{cx+k*rx},{cy-ry} {cx+rx},{cy-k*ry} {cx+rx},{cy} Z")

# the whole head tilts about the neck — a puzzled, gentle cock of the head
TILT, PX, PY = 9, 500, 560
_c, _s = math.cos(math.radians(TILT)), math.sin(math.radians(TILT))
def T(dd):
    def f(m):
        x, y = float(m.group(1)) - PX, float(m.group(2)) - PY
        return "%.1f,%.1f" % (PX + x*_c - y*_s, PY + x*_s + y*_c)
    return re.sub(r"(-?\d+\.?\d*),(-?\d+\.?\d*)", f, dd)
def hp(dd, label, **kw):
    d.path(T(dd), label, **kw)

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
for i, (x, y, w) in enumerate([(120,140,7),(880,160,6),(930,380,5),(70,420,6),(150,870,5),(860,880,7)]):
    d.shape("ellipse", f"Firefly glow {i+1}", x=x-w*2, y=y-w*2, width=w*4, height=w*4,
            fill="#D8F08A", opacity=10, stroke=NONE)
    d.shape("ellipse", f"Firefly {i+1}", x=x-w/2, y=y-w/2, width=w, height=w,
            fill="#E8F8A8", opacity=55, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#5E7A44", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F2F6E4", strokeWidth=3, opacity=55)
d.shape("ellipse", "Patina 1", x=160, y=170, width=240, height=150, fill="#A9BE88", opacity=24, stroke=NONE)
d.shape("ellipse", "Patina 2", x=620, y=200, width=220, height=130, fill="#A9BE88", opacity=20, stroke=NONE)
for i, (x, y, w) in enumerate([(210,300,8),(780,280,7),(150,470,9),(850,470,8),(330,140,7),(660,130,8)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w, fill="#6E8A52", opacity=35, stroke=NONE)

# moss mound — lower edge rides the plate's own arc
my = 690
d.path(f"M{disc_x(my,-1,420):.1f},{my} C260,650 380,676 500,664 C620,652 740,670 {disc_x(my,1,420):.1f},{my} "
       f"A420,420 0 0 1 {disc_x(my,-1,420):.1f},{my} Z", "Moss mound", fill="#5E7A3C", opacity=40, stroke=NONE)

# --- fern fronds either side ------------------------------------------------------
def frond(base, ctrl, tip, n, side, label, leaf=34):
    d.path(f"M{base[0]},{base[1]} Q{ctrl[0]},{ctrl[1]} {tip[0]},{tip[1]}", f"{label} rachis",
           fill=NONE, stroke="#4A6A2E", strokeWidth=5, opacity=80, cap="round")
    for j in range(n):
        t = 0.12 + 0.82*j/(n - 1)
        u = 1 - t
        x = u*u*base[0] + 2*u*t*ctrl[0] + t*t*tip[0]
        y = u*u*base[1] + 2*u*t*ctrl[1] + t*t*tip[1]
        tx = 2*u*(ctrl[0]-base[0]) + 2*t*(tip[0]-ctrl[0])
        ty = 2*u*(ctrl[1]-base[1]) + 2*t*(tip[1]-ctrl[1])
        ln = math.hypot(tx, ty); tx, ty = tx/ln, ty/ln
        L = leaf*(1 - 0.7*t)
        for sgn in (1, -1):
            nx, ny = -ty*sgn, tx*sgn
            ex, ey = x + (nx*0.85 + tx*0.5)*L, y + (ny*0.85 + ty*0.5)*L
            w = L*0.28
            d.path(f"M{x:.1f},{y:.1f} Q{(x+ex)/2 + tx*w:.1f},{(y+ey)/2 + ty*w:.1f} {ex:.1f},{ey:.1f} "
                   f"Q{(x+ex)/2 - tx*w:.1f},{(y+ey)/2 - ty*w:.1f} {x:.1f},{y:.1f} Z",
                   f"{label} pinna {j+1}{'a' if sgn > 0 else 'b'}", fill=FROND_GRAD, stroke=NONE, opacity=78)

frond((250, 720), (150, 560), (250, 330), 11, -1, "Frond L1", leaf=54)
frond((300, 740), (250, 600), (150, 520), 7, -1, "Frond L2", leaf=40)
frond((750, 720), (850, 560), (750, 330), 11, 1, "Frond R1", leaf=54)
frond((700, 740), (750, 600), (850, 520), 7, 1, "Frond R2", leaf=40)

# --- chunky moss-green body: closes on the plate's own arc ----------------------
by = 780
# shoulders rise to the head's flanks so head and body read as one chunky bird
d.path(f"M{disc_x(by,-1):.1f},{by} C214,690 240,560 332,468 C400,560 600,560 712,468 "
       f"C770,560 786,690 {disc_x(by,1):.1f},{by} A416,416 0 0 1 {disc_x(by,-1):.1f},{by} Z",
       "Body", fill=BODY_GRAD, stroke=INK, strokeWidth=7)
WING_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5E8036"}, {"offset": 1, "color": "#3E5A24"}]}}
# folded wings hugging the flanks; their lower edge stays well inside the arc
d.path("M318,556 C272,616 252,700 268,780 C298,768 326,746 344,716 C352,668 350,616 358,580 Z",
       "Wing L", fill=WING_GRAD, stroke=INK, strokeWidth=4, opacity=90)
d.path("M682,556 C728,616 748,700 732,780 C702,768 674,746 656,716 C648,668 650,616 642,580 Z",
       "Wing R", fill=WING_GRAD, stroke=INK, strokeWidth=4, opacity=90)
for side in (-1, 1):
    for k in range(5):
        y = 606 + k*30
        x = 500 + side*(186 - k*2)
        d.path(f"M{x - side*36},{y} Q{x - side*16},{y + 10} {x + side*6},{y + 2}",
               f"Wing bar {'L' if side < 0 else 'R'}{k+1}", fill=NONE,
               stroke="#24381A", strokeWidth=4, opacity=45, cap="round")
        d.path(f"M{x - side*28},{y + 8} Q{x - side*14},{y + 13} {x},{y + 9}",
               f"Wing fleck {'L' if side < 0 else 'R'}{k+1}", fill=NONE,
               stroke="#E2E88A", strokeWidth=3, opacity=35, cap="round")
d.shape("ellipse", "Breast light", x=400, y=600, width=200, height=140, fill="#D8EA9A", opacity=20, stroke=NONE)
# mottled barring: rows of feather-tip scallops, dark bar + yellow fleck
rows = [(620, [400, 460, 530, 590]), (670, [380, 440, 500, 560, 620]),
        (720, [370, 430, 490, 550, 610]), (770, [390, 450, 515, 580])]
JIT = [(-6, 3), (5, -4), (-3, 5), (7, 1), (-8, -2), (2, 6), (6, -5), (-4, 2)]
for r_, (y, xs) in enumerate(rows):
    for k, x in enumerate(xs):
        jx, jy = JIT[(r_*3 + k) % len(JIT)]
        x += jx + (15 if r_ % 2 else 0); y_ = y + jy
        y, y0_ = y_, y
        d.path(f"M{x-20},{y} Q{x},{y+14} {x+20},{y}", f"Body bar {r_+1}-{k+1}",
               fill=NONE, stroke="#2E4A1E", strokeWidth=4, opacity=45, cap="round")
        d.path(f"M{x-10},{y+7} Q{x},{y+11} {x+10},{y+7}", f"Body fleck {r_+1}-{k+1}",
               fill=NONE, stroke="#E2E88A", strokeWidth=3, opacity=40, cap="round")
        y = y0_

# --- head (tilted) --------------------------------------------------------------
hp(ell(500, 400, 208, 192), "Head", fill=HEAD_GRAD, stroke=INK, strokeWidth=7)
hp("M360,270 C420,224 580,224 640,270", "Crown light", fill=NONE,
   stroke="#E4F2A8", strokeWidth=14, opacity=25, cap="round")
for i, (x, y) in enumerate([(420,250),(470,236),(530,236),(580,250),(380,290),(620,290),
                            (450,280),(550,280),(340,340),(660,340),(330,420),(670,420),
                            (350,500),(650,500)]):
    hp(f"M{x-14},{y} Q{x},{y+10} {x+14},{y}", f"Head bar {i+1}", fill=NONE,
       stroke="#2E4A1E", strokeWidth=4, opacity=40, cap="round")
    hp(f"M{x-7},{y+6} Q{x},{y+9} {x+7},{y+6}", f"Head fleck {i+1}", fill=NONE,
       stroke="#E2E88A", strokeWidth=3, opacity=40, cap="round")

# --- owl-like facial disc --------------------------------------------------------
DISC = ("M500,318 C548,288 628,300 650,366 C672,440 640,520 566,560 "
        "C534,578 466,578 434,560 C360,520 328,440 350,366 C372,300 452,288 500,318 Z")
hp(DISC, "Facial disc", fill=DISC_GRAD, stroke="#8C8650", strokeWidth=4)
hp("M500,318 C548,288 628,300 650,366 C672,440 640,520 566,560", "Disc rim shade R",
   fill=NONE, stroke="#6E6A3A", strokeWidth=10, opacity=25, cap="round")
hp("M434,560 C360,520 328,440 350,366 C372,300 452,288 500,318", "Disc rim shade L",
   fill=NONE, stroke="#6E6A3A", strokeWidth=10, opacity=25, cap="round")
# fine radiating disc feathers, from the beak outward
for i in range(40):
    a = math.radians(-90 + i*9 + 4)
    r0, r1 = 62, 128 - 18*abs(math.sin(a))**3
    x0, y0 = 500 + r0*math.cos(a), 450 + r0*math.sin(a)*1.05
    x1, y1 = 500 + r1*math.cos(a)*1.12, 450 + r1*math.sin(a)*0.98
    hp(f"M{x0:.1f},{y0:.1f} L{x1:.1f},{y1:.1f}", f"Disc feather {i+1}", fill=NONE,
       stroke="#9A9456", strokeWidth=2, opacity=40, cap="round")

# --- eyes: dark, round, gentle -----------------------------------------------------
for side, (ex, ey) in (("L", (438, 410)), ("R", (562, 410))):
    hp(ell(ex, ey, 34, 34), f"Eye socket {side}", fill="#7E7A44", opacity=30, stroke=NONE)
    hp(ell(ex, ey, 23, 25), f"Eye {side}", fill="#1E1A12", stroke=INK, strokeWidth=3)
    hp(ell(ex + 2, ey + 8, 14, 9), f"Eye depth {side}", fill="#5A4628", opacity=40, stroke=NONE)
    hp(ell(ex - 8, ey - 9, 6, 6), f"Glint {side}", fill="#FFFFFF", opacity=92, stroke=NONE)
    hp(ell(ex + 9, ey + 8, 2.5, 2.5), f"Glint small {side}", fill="#FFFFFF", opacity=70, stroke=NONE)
    hp(f"M{ex-20},{ey+20} Q{ex},{ey+30} {ex+20},{ey+20}", f"Lower lid {side}", fill=NONE,
       stroke="#F4F0C8", strokeWidth=3, opacity=55, cap="round")
# mismatched brows: one raised, one level — the puzzled look
hp("M404,370 C418,346 446,338 470,352", "Brow L", fill=NONE,
   stroke="#F4F0C8", strokeWidth=7, opacity=80, cap="round")
hp("M532,370 C548,362 572,362 594,372", "Brow R", fill=NONE,
   stroke="#F4F0C8", strokeWidth=7, opacity=80, cap="round")

# --- whiskery vibrissae fanning from the beak base --------------------------------
for side in (-1, 1):
    for k, (dx, dy) in enumerate([(-92, -6), (-96, 22), (-88, 50), (-72, 76), (-50, 96)]):
        x0, y0 = 500 + side*28, 462 + k*6
        cx_, cy_ = x0 + side*(-dx)*0.5, y0 + dy*0.3
        x1, y1 = x0 + side*(-dx), y0 + dy
        hp(f"M{x0},{y0} Q{cx_:.0f},{cy_:.0f} {x1},{y1}", f"Vibrissa {'L' if side < 0 else 'R'}{k+1}",
           fill=NONE, stroke="#F6F2D4", strokeWidth=2.5, opacity=75, cap="round")
        hp(f"M{x0},{y0+4} Q{cx_:.0f},{cy_+6:.0f} {x1 - side*10},{y1+8}",
           f"Vibrissa dark {'L' if side < 0 else 'R'}{k+1}",
           fill=NONE, stroke="#5A5630", strokeWidth=1.5, opacity=45, cap="round")

# --- pale hooked beak -----------------------------------------------------------------
hp("M478,516 C486,536 514,536 522,516 C516,528 484,528 478,516 Z", "Lower mandible",
   fill="#A8A288", stroke=INK, strokeWidth=3)
hp("M472,446 C472,428 528,428 528,446 C534,486 522,526 500,550 C478,526 466,486 472,446 Z",
   "Upper mandible", fill=BEAK_GRAD, stroke=INK, strokeWidth=5)
hp("M500,436 C498,470 498,506 500,540", "Beak ridge", fill=NONE,
   stroke="#FFFFFF", strokeWidth=4, opacity=45, cap="round")
hp("M478,440 C486,432 514,432 522,440", "Cere", fill=NONE,
   stroke="#8E8870", strokeWidth=4, opacity=55, cap="round")
hp(ell(487, 446, 3.5, 3), "Nostril L", fill="#3A3628", opacity=80, stroke=NONE)
hp(ell(513, 446, 3.5, 3), "Nostril R", fill="#3A3628", opacity=80, stroke=NONE)

# --- name ---------------------------------------------------------------------------
d.text("KĀKĀPŌ", "Name", x=500, y=962, size=60, font="Virelai Sans",
       color="#DCE8C4", justify="center")

d.finish("kakapo-V1R00")
