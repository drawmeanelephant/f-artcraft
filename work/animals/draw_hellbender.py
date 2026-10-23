#!/usr/bin/env python3
"""Hellbender — field-guide plate V1R00. Dorsal full body: broad flattened
head, beady eyes, wrinkled skin-folds along the flanks, keeled paddle tail.
Murky river-rock palette — olive and slate. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420; pebble band closes on the disc arc."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Hellbender — Field Plate", 1000, 1000)

INK = "#2E2E22"          # dark olive-slate, not black
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#182019"}, {"offset": 1, "color": "#080D0A"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#B9C4A4"}, {"offset": 0.55, "color": "#8B9A74"},
    {"offset": 1, "color": "#55664C"}]}}
BODY_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#9A9668"}, {"offset": 0.5, "color": "#7E7C50"},
    {"offset": 1, "color": "#5F5E3C"}]}}
HEAD_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#A8A470"}, {"offset": 0.7, "color": "#86824F"},
    {"offset": 1, "color": "#66643E"}]}}
FRILL_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#8C885A"}, {"offset": 1, "color": "#575636"}]}}
ROCK_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#8E9484"}, {"offset": 1, "color": "#5A6152"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=56, y=16, width=888, height=888,
        fill="#7E9478", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#41523C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D9E4C8", strokeWidth=3, opacity=50)
# murky-water blotches + current streaks
d.shape("ellipse", "Haze 1", x=170, y=180, width=240, height=150, fill="#A9B896", opacity=20, stroke=NONE)
d.shape("ellipse", "Haze 2", x=580, y=560, width=230, height=140, fill="#6E7E5C", opacity=20, stroke=NONE)
d.path("M170,330 C330,306 560,302 760,318", "Current 1", fill=NONE,
       stroke="#CBD8B4", strokeWidth=5, opacity=18, cap="round")
d.path("M150,400 C340,378 580,376 800,392", "Current 2", fill=NONE,
       stroke="#CBD8B4", strokeWidth=4, opacity=14, cap="round")
for i, (x, y, w) in enumerate([(200,290,7),(770,240,6),(165,520,8),(820,480,7),(250,180,6),
                               (700,160,7),(140,380,5),(860,360,6),(420,110,6),(590,105,7),
                               (320,130,5),(660,200,5),(230,660,5),(780,620,5),(500,95,4)]):
    d.shape("ellipse", f"Silt fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#D6E0C2", opacity=35, stroke=NONE)

# --- riverbed: pebble band closing on the disc arc ------------------------------
# chord at y=750 on circle (500,460) r420 -> x = 500 +/- 303.8
d.path("M196.2,750 C320,724 430,738 500,744 C590,752 690,724 803.8,750 "
       "A420,420 0 0 1 196.2,750 Z",
       "Gravel bed", fill="#5F6854", opacity=80, stroke=NONE)
for i, (cx, cy, rx, ry) in enumerate([(300,762,52,30),(430,772,62,32),(580,768,55,28),
                                     (710,756,48,26),(230,780,40,22),(650,790,44,20)]):
    d.shape("ellipse", f"Stone {i+1}", x=cx-rx, y=cy-ry, width=rx*2, height=ry*2,
            fill=ROCK_GRAD, stroke="#49503F", strokeWidth=4)
    d.shape("ellipse", f"Stone {i+1} light", x=cx-rx*0.55, y=cy-ry*0.7,
            width=rx*0.9, height=ry*0.45, fill="#C9D2BC", opacity=25, stroke=NONE)

# --- the body: tapered ribbon along a cubic spine -------------------------------
P0, P1, P2, P3 = (430, 330), (320, 470), (620, 580), (560, 720)

def cubic(t):
    u = 1 - t
    x = u**3*P0[0] + 3*u*u*t*P1[0] + 3*u*t*t*P2[0] + t**3*P3[0]
    y = u**3*P0[1] + 3*u*u*t*P1[1] + 3*u*t*t*P2[1] + t**3*P3[1]
    dx = 3*u*u*(P1[0]-P0[0]) + 6*u*t*(P2[0]-P1[0]) + 3*t*t*(P3[0]-P2[0])
    dy = 3*u*u*(P1[1]-P0[1]) + 6*u*t*(P2[1]-P1[1]) + 3*t*t*(P3[1]-P2[1])
    return x, y, dx, dy

WKEYS = [(0.0, 56), (0.12, 106), (0.45, 100), (0.68, 62), (0.87, 34), (1.0, 14)]
def width_at(t):
    for (t0, w0), (t1, w1) in zip(WKEYS, WKEYS[1:]):
        if t <= t1:
            return w0 + (w1 - w0) * (t - t0) / (t1 - t0)
    return WKEYS[-1][1]

N = 44
mid = []
for k in range(N + 1):
    t = k / N
    x, y, dx, dy = cubic(t)
    ln = math.hypot(dx, dy) or 1
    mid.append((x, y, -dy/ln, dx/ln, width_at(t)/2, t))   # x,y,nx,ny,halfw,t

# soft cast shadow under the body
sh_L, sh_R = [], []
for x, y, nx, ny, hw, t in mid:
    sh_L.append((x + nx*(hw+14) + 12, y + ny*(hw+14) + 16))
    sh_R.append((x - nx*(hw+14) + 12, y - ny*(hw+14) + 16))
dd = "M%.1f,%.1f " % sh_L[0] + " ".join("L%.1f,%.1f" % p for p in sh_L[1:])
dd += " " + " ".join("L%.1f,%.1f" % p for p in reversed(sh_R)) + " Z"
d.path(dd, "Body cast shadow", fill="#3C4630", opacity=28, stroke=NONE)

# legs first so roots tuck under the body
def leg(t, side, label, length=56):
    x, y, nx, ny, hw, _ = mid[round(t*N)]
    ox, oy = nx*side, ny*side
    root = (x + ox*hw*0.5, y + oy*hw*0.5)
    tip = (x + ox*(hw + length), y + oy*(hw + length) + 10)
    ctrl = ((root[0]+tip[0])/2 + ox*10, (root[1]+tip[1])/2 + 6)
    # tapered ribbon
    Ls, Rs = [], []
    for k in range(9):
        u = k / 8
        qx = (1-u)**2*root[0] + 2*(1-u)*u*ctrl[0] + u*u*tip[0]
        qy = (1-u)**2*root[1] + 2*(1-u)*u*ctrl[1] + u*u*tip[1]
        qdx = 2*(1-u)*(ctrl[0]-root[0]) + 2*u*(tip[0]-ctrl[0])
        qdy = 2*(1-u)*(ctrl[1]-root[1]) + 2*u*(tip[1]-ctrl[1])
        ql = math.hypot(qdx, qdy) or 1
        w = (24 - 13*u) / 2
        Ls.append((qx - qdy/ql*w, qy + qdx/ql*w))
        Rs.append((qx + qdy/ql*w, qy - qdx/ql*w))
    dd = "M%.1f,%.1f " % Ls[0] + " ".join("L%.1f,%.1f" % p for p in Ls[1:])
    dd += " " + " ".join("L%.1f,%.1f" % p for p in reversed(Rs)) + " Z"
    d.path(dd, label, fill=BODY_GRAD, stroke=INK, strokeWidth=4)
    # stubby toes tucked onto the tip
    for j, f in enumerate([-11, 0, 11]):
        tx = tip[0] + ox*4 - ny*f*0.8
        ty = tip[1] + oy*4 + nx*f*0.8
        d.shape("ellipse", f"{label} toe {j+1}", x=tx-5, y=ty-5, width=10, height=9,
                fill=BODY_GRAD, stroke=INK, strokeWidth=3)

leg(0.16,  1, "Leg front L", 50)
leg(0.18, -1, "Leg front R", 52)
leg(0.62,  1, "Leg rear L", 54)
leg(0.60, -1, "Leg rear R", 56)

# body ribbon
Lpts = [(x + nx*hw, y + ny*hw) for x, y, nx, ny, hw, t in mid]
Rpts = [(x - nx*hw, y - ny*hw) for x, y, nx, ny, hw, t in mid]
dd = "M%.1f,%.1f " % Lpts[0] + " ".join("L%.1f,%.1f" % p for p in Lpts[1:])
dd += " " + " ".join("L%.1f,%.1f" % p for p in reversed(Rpts)) + " Z"
d.path(dd, "Body", fill=BODY_GRAD, stroke=INK, strokeWidth=7)

# dorsal sheen + belly-shade edging
dorsal = "M%.1f,%.1f " % (mid[2][0], mid[2][1])
dorsal += " ".join("L%.1f,%.1f" % (x, y) for x, y, nx, ny, hw, t in mid[3:-3])
d.path(dorsal, "Dorsal ridge light", fill=NONE, stroke="#C4BC82",
       strokeWidth=14, opacity=25, cap="round")
dorsal2 = "M%.1f,%.1f " % (mid[4][0], mid[4][1])
dorsal2 += " ".join("L%.1f,%.1f" % (x, y) for x, y, nx, ny, hw, t in mid[5:round(0.8*N)])
d.path(dorsal2, "Dorsal ridge", fill=NONE, stroke="#55522F",
       strokeWidth=5, opacity=30, cap="round")

# tail keel — laterally compressed fin ridge along the last third
keel_L, keel_R = [], []
for x, y, nx, ny, hw, t in mid[round(0.62*N):]:
    f = 1 + 0.45 * math.sin((t - 0.62) / 0.38 * math.pi)   # flare mid-tail
    keel_L.append((x + nx*hw*f, y + ny*hw*f))
    keel_R.append((x - nx*hw*f, y - ny*hw*f))
dd = "M%.1f,%.1f " % keel_L[0] + " ".join("L%.1f,%.1f" % p for p in keel_L[1:])
dd += " " + " ".join("L%.1f,%.1f" % p for p in reversed(keel_R)) + " Z"
d.path(dd, "Tail keel", fill=FRILL_GRAD, stroke=INK, strokeWidth=5, opacity=80)

# --- flank frills: wavy folded-skin ruffles hugging both edges -------------------
for side, s in (("L", 1), ("R", -1)):
    pts = []
    for x, y, nx, ny, hw, t in mid[round(0.06*N):round(0.9*N)]:
        off = hw + 9 + 6*math.sin(t*44 + (0 if s == 1 else 1.6))
        pts.append((x + nx*off*s, y + ny*off*s))
    dd = "M%.1f,%.1f " % pts[0] + " ".join("L%.1f,%.1f" % p for p in pts[1:])
    d.path(dd, f"Frill {side}", fill=NONE, stroke=FRILL_GRAD,
           strokeWidth=13, opacity=80, cap="round")
    d.path(dd, f"Frill {side} rim", fill=NONE, stroke="#B4AE74",
           strokeWidth=4, opacity=45, cap="round")
    # wrinkle creases crossing the edge — irregular spacing and length
    crease_ts = [0.09, 0.15, 0.21, 0.28, 0.34, 0.41, 0.47, 0.54, 0.60, 0.67, 0.73, 0.80]
    for j, t in enumerate(crease_ts):
        x, y, nx, ny, hw, _ = mid[round(t*N)]
        reach = 0.45 + 0.25 * ((j * 7 + (0 if s == 1 else 3)) % 5) / 4
        p_in = (x + nx*hw*reach*s, y + ny*hw*reach*s)
        p_out = (x + nx*(hw+11)*s, y + ny*(hw+11)*s)
        d.path("M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" % (
            p_in[0], p_in[1],
            x + nx*(hw+4)*s + 4, y + ny*(hw+4)*s,
            p_out[0], p_out[1]),
            f"Crease {side} {j+1}", fill=NONE, stroke="#4C4B2E",
            strokeWidth=4, opacity=38, cap="round")

# --- mottling -------------------------------------------------------------------
for i, (x, y, w, h) in enumerate([(392,400,60,34),(468,470,74,38),(540,540,66,30),
                                  (372,470,44,24),(500,610,54,26),(575,650,40,20),
                                  (440,545,40,20),(600,585,36,18)]):
    d.shape("ellipse", f"Mottle {i+1}", x=x, y=y, width=w, height=h,
            fill="#4E4D2F", opacity=30, stroke=NONE)
for i, (x, y, w) in enumerate([(420,430,7),(510,500,6),(585,575,7),(380,520,5),
                               (545,645,6),(470,585,5),(525,685,5)]):
    d.shape("ellipse", f"Body speckle {i+1}", x=x, y=y, width=w, height=w,
            fill="#CBC38A", opacity=40, stroke=NONE)

# --- head: broad, flat, blunt shovel snout ---------------------------------------
d.path("M338,272 C352,222 392,204 437,204 C486,204 528,222 546,270 "
       "C560,304 552,334 526,350 C492,368 384,368 350,348 "
       "C330,334 328,302 338,272 Z",
       "Head", fill=HEAD_GRAD, stroke=INK, strokeWidth=7)
# skull-top light + jaw shade
d.shape("ellipse", "Head highlight", x=368, y=222, width=140, height=44,
        fill="#FFFFFF", opacity=14, stroke=NONE)
d.path("M352,336 C400,358 486,358 524,336 C494,364 388,364 352,336 Z",
       "Jaw shade", fill="#55522F", opacity=30, stroke=NONE)
# wide mouth crease hugging the snout rim
d.path("M352,256 C396,226 482,226 526,256", "Mouth line", fill=NONE,
       stroke=INK, strokeWidth=5, opacity=55, cap="round")
# beady eyes, wide-set on the skull top
for side, ex in (("L", 390), ("R", 484)):
    d.shape("ellipse", f"Eye {side}", x=ex, y=262, width=15, height=13,
            fill="#1E2012", stroke=NONE)
    d.shape("ellipse", f"Eye glint {side}", x=ex+4, y=264, width=4, height=4,
            fill="#FFFFFF", opacity=85, stroke=NONE)
    # fleshy brow fold above each eye
    d.path("M%.0f,%.0f C%.0f,%.0f %.0f,%.0f %.0f,%.0f" % (
        ex-8, 260, ex+2, 250, ex+12, 250, ex+22, 258),
        f"Brow {side}", fill=NONE, stroke="#6B6740", strokeWidth=5,
        opacity=70, cap="round")
# nostrils at the snout rim
d.shape("ellipse", "Nostril L", x=410, y=216, width=8, height=6, fill="#33321E", opacity=80, stroke=NONE)
d.shape("ellipse", "Nostril R", x=460, y=216, width=8, height=6, fill="#33321E", opacity=80, stroke=NONE)
# neck wrinkle behind the head
d.path("M356,346 C410,364 500,366 540,344", "Neck crease", fill=NONE,
       stroke="#4C4B2E", strokeWidth=6, opacity=50, cap="round")
# blunt tail tip cap
d.shape("ellipse", "Tail tip", x=549, y=708, width=20, height=18,
        fill="#6E6C44", stroke=NONE)
# head speckles
for i, (x, y, w) in enumerate([(380,238,6),(478,234,6),(520,282,5),(356,288,5),(442,242,4)]):
    d.shape("ellipse", f"Head speckle {i+1}", x=x, y=y, width=w, height=w,
            fill="#57552F", opacity=50, stroke=NONE)

# --- name ------------------------------------------------------------------------
d.text("HELLBENDER", "Name", x=500, y=962, size=60, font="Virelai Sans",
       color="#CBD8B4", justify="center")

d.finish("hellbender-V1R00")
