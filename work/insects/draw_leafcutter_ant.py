#!/usr/bin/env python3
"""Leafcutter ant — field-guide plate V1R00. An Atta worker in three-quarter
side view walking right on a soil trail, a cut leaf fragment bigger than
itself raised above its head in the mandibles like a sail: translucent green
with midrib, secondary and tertiary veins, one serrated natural margin and the
smooth arc of the cut. Small dark spiny body beneath. Soil-and-leaf plate.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Leafcutter Ant — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420
INK = "#24160E"
FAR = []

def lin(angle, *stops):
    return {"gradient": {"kind": "linear", "angle": angle, "stops": [
        dict(offset=s[0], color=s[1], **({"opacity": s[2]} if len(s) > 2 else {})) for s in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial", "stops": [
        dict(offset=s[0], color=s[1], **({"opacity": s[2]} if len(s) > 2 else {})) for s in stops]}}

def chk(x, y, pad=24):
    if math.hypot(x - CX, y - CY) > R - pad:
        FAR.append((round(x), round(y)))

def cub(p0, p1, p2, p3, t):
    u = 1 - t
    x = u**3*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t**3*p3[0]
    y = u**3*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t**3*p3[1]
    dx = 3*u*u*(p1[0]-p0[0]) + 6*u*t*(p2[0]-p1[0]) + 3*t*t*(p3[0]-p2[0])
    dy = 3*u*u*(p1[1]-p0[1]) + 6*u*t*(p2[1]-p1[1]) + 3*t*t*(p3[1]-p2[1])
    return x, y, dx, dy

def taper(c, w0, w1, n=28, bulge=0.0):
    L, Rr = [], []
    for i in range(n + 1):
        t = i / n
        x, y, dx, dy = cub(*c, t)
        chk(x, y)
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy/ln, dx/ln
        w = (w0 + (w1 - w0)*t + bulge*math.sin(math.pi*t)) / 2
        L.append((x + nx*w, y + ny*w)); Rr.append((x - nx*w, y - ny*w))
    return "M" + " L".join("%.1f,%.1f" % p for p in L + Rr[::-1]) + " Z"

def straight(a, b):
    return [a, (a[0]+(b[0]-a[0])/3, a[1]+(b[1]-a[1])/3), (a[0]+2*(b[0]-a[0])/3, a[1]+2*(b[1]-a[1])/3), b]

def cpath(c):
    return "M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (*c[0], *c[1], *c[2], *c[3])

def lell(cx, cy, rx, ry, rot=0):
    k, a = 0.5523, math.radians(rot)
    ca, sa = math.cos(a), math.sin(a)
    def p(x, y):
        return "%.1f,%.1f" % (cx + x*ca - y*sa, cy + x*sa + y*ca)
    return (f"M{p(rx,0)} C{p(rx,ry*k)} {p(rx*k,ry)} {p(0,ry)} C{p(-rx*k,ry)} {p(-rx,ry*k)} {p(-rx,0)} "
            f"C{p(-rx,-ry*k)} {p(-rx*k,-ry)} {p(0,-ry)} C{p(rx*k,-ry)} {p(rx,-ry*k)} {p(rx,0)} Z")

def disc_x(y):
    h = math.sqrt(R*R - (y - CY)**2)
    return CX - h, CX + h

def poly_d(pts, close=True):
    return "M" + " L".join("%.1f,%.1f" % p for p in pts) + (" Z" if close else "")

def inside(pt, poly):
    x, y = pt; c = False
    for i in range(len(poly)):
        x1, y1 = poly[i]; x2, y2 = poly[i - 1]
        if (y1 > y) != (y2 > y) and x < (x2 - x1)*(y - y1)/(y2 - y1) + x1:
            c = not c
    return c

# --- palette --------------------------------------------------------------------
BG = lin(90, (0, "#1F2416"), (1, "#0B0D07"))
PLATE = rad((0, "#E6E0B6"), (0.6, "#BFB680"), (1, "#8A7E4C"))
SOIL = lin(90, (0, "#7A5A36"), (0.5, "#5E4228"), (1, "#3A2818"))
LEAF = lin(60, (0, "#A8D456", 0.86), (0.5, "#6EA834", 0.80), (1, "#3E7A24", 0.88))
BODY = rad((0, "#7A4A2A"), (0.55, "#4A2A16"), (1, "#24140A"))
GASTER = rad((0, "#80502E"), (0.5, "#4E2E18"), (1, "#22120A"))
LEG = lin(90, (0, "#6E4428"), (1, "#2E1A0E"))
LEG_FAR = lin(90, (0, "#3E2616"), (1, "#1E120A"))
EYE = rad((0, "#5E5E4E"), (0.6, "#24221A"), (1, "#100E0A"))

# --- backdrop + plate -----------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG, stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876, fill="#BFB680", opacity=6, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840, fill=PLATE, stroke="#5E5430", strokeWidth=6)
# out-of-focus canopy leaves behind
for i, (x, y, rx, ry, rot, o) in enumerate([(230, 200, 110, 46, -35, 16), (790, 260, 96, 40, 40, 14),
                                            (740, 140, 70, 28, 20, 10), (170, 400, 70, 28, -60, 10)]):
    chk(x, y, rx + 10)
    d.path(lell(x, y, rx, ry, rot), f"Canopy leaf {i+1}", fill="#4E7A2E", opacity=o, stroke=NONE)
for i, (x, y, w) in enumerate([(300, 110, 6), (680, 100, 7), (860, 430, 6), (140, 520, 6), (840, 560, 5),
                               (420, 640, 5)]):
    chk(x, y, 12)
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w, fill="#6E643A", opacity=35, stroke=NONE)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F6F0D4", strokeWidth=3, opacity=45)

# --- soil trail (closed on the disc arc) ---------------------------------------------
def soil_y(x):
    return 694 + 7*math.sin(x/58.0) + 4*math.sin(x/23.0 + 1)
SY0 = soil_y(0)
sx0, _ = disc_x(soil_y(110)); _, sx1 = disc_x(soil_y(890))
top = [(x, soil_y(x)) for x in [sx0 + k*(sx1 - sx0)/60 for k in range(61)]]
d.path(poly_d(top, False)[0:] + f" A420,420 0 0 1 {top[0][0]:.1f},{top[0][1]:.1f} Z",
       "Soil", fill=SOIL, stroke=INK, strokeWidth=4)
d.path(poly_d([(x, y + 3) for x, y in top[4:-4]], False), "Soil crust light", fill=NONE,
       stroke="#C8A878", strokeWidth=4, opacity=40, cap="round")
# worn trail: a paler band the colony has walked flat
d.path(f"M180,{soil_y(180)+18:.1f} C320,712 520,716 820,{soil_y(820)+16:.1f} "
       f"C640,734 360,736 180,{soil_y(180)+18:.1f} Z", "Trail band", fill="#B89870", opacity=22, stroke=NONE)
for i, (x, y, w, h, c) in enumerate([(220, 730, 26, 16, "#8E7A62"), (250, 748, 14, 10, "#A8927A"),
                                     (700, 740, 22, 14, "#7E6A52"), (560, 790, 16, 11, "#9A8670"),
                                     (380, 780, 20, 13, "#8A765E"), (780, 712, 14, 9, "#A08A70")]):
    chk(x + w, y + h, 14)
    d.shape("ellipse", f"Pebble {i+1}", x=x, y=y, width=w, height=h,
            fill=rad((0, "#E0D2BC"), (1, c)), stroke="#4A3A28", strokeWidth=2, opacity=90)
for i, (x, y) in enumerate([(300, 720), (330, 760), (460, 744), (520, 770), (620, 724), (660, 800),
                            (410, 820), (740, 770), (262, 782), (500, 840), (590, 846)]):
    chk(x, y, 14)
    d.shape("ellipse", f"Soil grain {i+1}", x=x, y=y, width=6, height=5, fill="#2E1E10", opacity=45, stroke=NONE)
# two dropped leaf discs on the trail, closed shapes inside the rim
for i, (x, y, rx, ry, rot) in enumerate([(770, 690, 28, 10, -8), (190, 702, 22, 8, 10)]):
    d.path(lell(x, y, rx, ry, rot), f"Dropped leaf bit {i+1}", fill=LEAF, stroke="#2E5A1A", strokeWidth=2)
    d.path(f"M{x-rx+6},{y} L{x+rx-6},{y}", f"Dropped leaf bit {i+1} vein", fill=NONE,
           stroke="#D8EA8A", strokeWidth=3, opacity=55, cap="round")

# --- legs ------------------------------------------------------------------------
def leg(name, base, knee, ax, toe_dx, fill, far=False, dx=0, dy=0):
    base = (base[0]+dx, base[1]+dy); knee = (knee[0]+dx, knee[1]+dy); ax += dx
    ankle = (ax, soil_y(ax) - 5)
    toe = (ax + toe_dx, soil_y(ax + toe_dx) - 2)
    fx, fy = knee[0]-base[0], knee[1]-base[1]
    fem = [base, (base[0]+fx*0.33, base[1]+fy*0.33 - 4), (base[0]+fx*0.66, base[1]+fy*0.66 - 4), knee]
    sw = 2 if far else 2.5
    d.path(taper(fem, 11, 7, bulge=3), f"{name} femur", fill=fill, stroke=INK, strokeWidth=sw)
    d.path(taper(straight(knee, ankle), 7, 5), f"{name} tibia", fill=fill, stroke=INK, strokeWidth=sw)
    mid = (ankle[0]*0.5 + toe[0]*0.5, min(ankle[1], toe[1]) - 1)
    d.path(f"M{ankle[0]:.1f},{ankle[1]:.1f} L{mid[0]:.1f},{mid[1]:.1f} L{toe[0]:.1f},{toe[1]:.1f}",
           f"{name} tarsus", fill=NONE, stroke="#1E120A" if far else "#3A2414", strokeWidth=4,
           cap="round", join="round")
    d.path(lell(knee[0], knee[1], 5, 5), f"{name} knee", fill="#1A0E06", opacity=70, stroke=NONE)
    if not far:
        d.path(f"M{base[0]+fx*0.2:.1f},{base[1]+fy*0.2-3:.1f} L{base[0]+fx*0.8:.1f},{base[1]+fy*0.8-3:.1f}",
               f"{name} femur light", fill=NONE, stroke="#D8A878", strokeWidth=3, opacity=45, cap="round")

FDX, FDY = 16, -8
leg("Far foreleg", (512, 600), (552, 624), 582, 22, LEG_FAR, True, FDX, FDY)
leg("Far midleg", (470, 604), (452, 634), 432, -20, LEG_FAR, True, FDX, FDY)
leg("Far hindleg", (436, 604), (388, 630), 344, -26, LEG_FAR, True, FDX, FDY)

# far mandible + far antenna sit behind the leaf
d.path("M612,552 C636,540 654,534 668,534 C660,546 646,558 628,566 Z", "Far mandible", fill=lin(0, (0, "#3A2010"), (1, "#5E3A1E")),
       stroke=INK, strokeWidth=2)

# --- the leaf fragment --------------------------------------------------------------
G = (664, 544)
CUT_R = [G, (720, 440), (736, 236), (598, 112)]
MARGIN = [(598, 112), (470, 132), (320, 230), (206, 352)]
CUT_L = [(206, 352), (250, 462), (470, 498), G]
outline = []
for k in range(0, 40):
    x, y, _, _ = cub(*CUT_R, k/40); outline.append((x, y))
for k in range(0, 44):
    x, y, dx, dy = cub(*MARGIN, k/44)
    ln = math.hypot(dx, dy); nx, ny = dy/ln, -dx/ln   # outward = up-left
    off = 7 if k % 2 else 0
    outline.append((x + nx*off, y + ny*off))
for k in range(0, 40):
    x, y, _, _ = cub(*CUT_L, k/40); outline.append((x, y))
for p in outline:
    chk(*p)
d.path(poly_d([(x + 10, y + 12) for x, y in outline]), "Leaf shadow glow", fill="#2E4A16", opacity=14, stroke=NONE)
d.path(poly_d(outline), "Leaf fragment", fill=LEAF, stroke="#2E5A1A", strokeWidth=3, join="round")
# cut edge browning where the mandibles sliced
for nm, c in (("right", CUT_R), ("left", CUT_L)):
    d.path(cpath(c), f"Cut edge {nm}", fill=NONE, stroke="#8A7A2E", strokeWidth=4, opacity=40, cap="round")

def clipped(pts, name, **kw):
    run = []
    k = 0
    for p in pts + [None]:
        if p is not None and inside(p, outline):
            run.append(p); continue
        if len(run) >= 2:
            k += 1
            d.path(poly_d(run, False), f"{name} {k}", fill=NONE, cap="round", join="round", **kw)
        run = []

# midrib crosses the fragment; secondaries run off it toward the natural margin
MID = [(150, 520), (330, 420), (560, 300), (800, 150)]
mid_pts = [cub(*MID, k/80)[:2] for k in range(81)]
clipped(mid_pts, "Midrib", stroke="#E2F09A", strokeWidth=7, opacity=75)
clipped([(x + 2, y + 4) for x, y in mid_pts], "Midrib shade", stroke="#2E5A1A", strokeWidth=3, opacity=35)
SEC = {1: [], -1: []}
for j, t in enumerate([k/12 for k in range(0, 12)]):
    x, y, dx, dy = cub(*MID, t)
    ln = math.hypot(dx, dy); ux, uy = dx/ln, dy/ln
    for side in (1, -1):
        nx, ny = uy*side, -ux*side          # side 1 = up-left, toward the natural margin
        a = math.radians(50)
        vx, vy = ux*math.cos(a) + nx*math.sin(a), uy*math.cos(a) + ny*math.sin(a)
        pts = []
        for s in range(0, 44):
            L = s * 7
            bend = 0.0016 * L * L
            pts.append((x + vx*L + ux*bend, y + vy*L + uy*bend))
        SEC[side].append(pts)
        clipped(pts, f"Secondary vein {j+1}{'ab'[side < 0]}", stroke="#D2E688", strokeWidth=4, opacity=60)
# tertiary net: slightly kinked links between neighbouring secondaries
for side in (1, -1):
    vs = SEC[side]
    for j in range(len(vs) - 1):
        for s in range(5, 44, 6):
            a, b = vs[j][s], vs[j + 1][min(s + (1 if (j + s) % 2 else -1), 43)]
            m = ((a[0] + b[0])/2 + (3 if s % 4 else -3), (a[1] + b[1])/2)
            if inside(a, outline) and inside(b, outline) and inside(m, outline):
                d.path(f"M{a[0]:.1f},{a[1]:.1f} L{m[0]:.1f},{m[1]:.1f} L{b[0]:.1f},{b[1]:.1f}",
                       f"Tertiary vein {side}-{j}-{s}", fill=NONE, stroke="#C8E080", strokeWidth=3,
                       opacity=28, cap="round", join="round")
d.path(lell(420, 290, 130, 60, -32), "Leaf backlight", fill="#F6FFD0", opacity=10, stroke=NONE)
d.path(lell(600, 250, 50, 90, 10), "Leaf sheen", fill="#FFFFFF", opacity=6, stroke=NONE)

# --- gaster, waist, mesosoma ----------------------------------------------------------
d.path(lell(298, 612, 66, 52, -12), "Gaster", fill=GASTER, stroke=INK, strokeWidth=4)
for i, (rx, o) in enumerate([(40, 45), (16, 40)]):
    d.path(f"M{298+rx:.0f},{566+i*4} C{300+rx-6:.0f},600 {300+rx-8:.0f},630 {290+rx:.0f},{660-i*6}",
           f"Gaster band {i+1}", fill=NONE, stroke="#1A0E06", strokeWidth=3, opacity=o, cap="round")
d.path(lell(278, 590, 30, 14, -20), "Gaster highlight", fill="#E8B080", opacity=22, stroke=NONE)
d.path(lell(268, 584, 10, 5, -20), "Gaster glint", fill="#FFFFFF", opacity=40, stroke=NONE)
for i, (x, y, r) in enumerate([(372, 602, 13), (398, 596, 14)]):
    d.path(lell(x, y, r, r - 2), f"Waist node {i+1}", fill=BODY, stroke=INK, strokeWidth=3)
d.path("M398,584 L392,566 L404,582 Z", "Postpetiole spine", fill="#3A2010", stroke=INK, strokeWidth=1.5)

def spine(name, base, tip, w=9):
    bx, by = base; tx, ty = tip
    ln = math.hypot(tx - bx, ty - by); nx, ny = -(ty - by)/ln*w/2, (tx - bx)/ln*w/2
    d.path(f"M{bx+nx:.1f},{by+ny:.1f} Q{(bx+tx)/2+nx*0.6:.1f},{(by+ty)/2+ny*0.6:.1f} {tx:.1f},{ty:.1f} "
           f"Q{(bx+tx)/2-nx*0.6:.1f},{(by+ty)/2-ny*0.6:.1f} {bx-nx:.1f},{by-ny:.1f} Z",
           name, fill=lin(90, (0, "#6E4428"), (1, "#2E1A0E")), stroke=INK, strokeWidth=2)

spine("Far propodeal spine", (444, 570), (428, 538))
spine("Far pronotal spine", (512, 540), (512, 510))
d.path("M410,600 C406,582 418,568 436,566 C452,566 458,560 466,552 C480,536 506,534 520,546 "
       "C532,556 534,590 522,604 C502,616 432,618 410,600 Z", "Mesosoma", fill=BODY, stroke=INK, strokeWidth=4)
d.path("M420,580 C430,572 450,570 462,560 C476,546 500,542 514,550", "Mesosoma ridge light",
       fill=NONE, stroke="#D8A070", strokeWidth=3, opacity=45, cap="round")
d.path("M428,606 C460,612 500,610 518,598", "Mesosoma belly shade", fill=NONE,
       stroke="#120A04", strokeWidth=4, opacity=40, cap="round")
spine("Propodeal spine", (436, 568), (412, 540))
spine("Mesonotal spine", (466, 554), (458, 532), 7)
spine("Pronotal spine", (500, 538), (488, 510))

# --- head ------------------------------------------------------------------------------
d.path("M532,580 C528,566 532,556 540,552", "Neck", fill=NONE, stroke="#2E1A0E", strokeWidth=10, cap="round")
spine("Far occipital spine", (560, 520), (560, 496), 8)
d.path("M540,560 C536,530 556,510 584,510 C612,510 632,528 632,556 C632,584 612,604 584,604 "
       "C560,604 544,588 540,560 Z", "Head", fill=BODY, stroke=INK, strokeWidth=4)
spine("Occipital spine", (548, 526), (532, 502), 8)
d.path("M552,528 C564,516 590,514 608,522", "Head crown light", fill=NONE, stroke="#E0A878",
       strokeWidth=3, opacity=50, cap="round")
d.path(lell(568, 538, 18, 10, -20), "Head sheen", fill="#F0C090", opacity=18, stroke=NONE)
d.path(lell(600, 548, 8, 9), "Compound eye", fill=EYE, stroke=INK, strokeWidth=2)
d.path(lell(598, 545, 2.5, 2.5), "Eye glint", fill="#FFFFFF", opacity=80, stroke=NONE)
for i, (x, y) in enumerate([(566, 570), (580, 584), (598, 576), (560, 552)]):
    d.path(lell(x, y, 2.5, 2.5), f"Head pit {i+1}", fill="#120A04", opacity=40, stroke=NONE)
# near mandible gripping the leaf's lower point
d.path("M614,566 C640,554 658,546 674,542 L666,552 L660,551 L656,560 L648,560 L644,569 L636,569 L630,580 Z", "Mandible",
       fill=lin(0, (0, "#4A2A14"), (1, "#8A5A30")), stroke=INK, strokeWidth=2.5, join="round")
d.path("M624,564 C640,556 652,551 664,547", "Mandible sheen", fill=NONE, stroke="#E0B080", strokeWidth=3, opacity=45, cap="round")

# --- antennae: elbowed, scape up, funiculus drooping forward ---------------------------
def antenna(name, base, elbow, c2, color, w, ring):
    d.path(taper(straight(base, elbow), w + 2, w), f"{name} scape", fill=color, stroke=INK, strokeWidth=1.5)
    c = [elbow] + c2
    d.path(cpath(c), f"{name} funiculus", fill=NONE, stroke=color, strokeWidth=w, cap="round")
    d.path(cpath(c), f"{name} rings", fill=NONE, stroke=ring, strokeWidth=3, dash=[2, 5], opacity=60)
    x, y, _, _ = cub(*c, 1)
    d.path(lell(x, y, w*0.9, w*1.1), f"{name} club", fill=color, stroke=INK, strokeWidth=1.5)

antenna("Far antenna", (612, 530), (640, 494), [(670, 486), (700, 500), (712, 530)], "#2E1A0E", 5, "#6E4A2A")
antenna("Near antenna", (604, 534), (626, 488), [(660, 470), (700, 486), (708, 522)], "#4A2A16", 6, "#B07A4A")

# --- near legs ---------------------------------------------------------------------------
leg("Foreleg", (512, 604), (550, 628), 576, 24, LEG)
leg("Midleg", (470, 608), (458, 638), 440, -20, LEG)
leg("Hindleg", (436, 608), (384, 636), 340, -26, LEG)

if FAR:
    print("WARN points near the rim:", FAR[:12])

d.text("LEAFCUTTER ANT", "Name", x=500, y=940, size=56, font="Virelai Sans", color="#ECE6C8", justify="center")
d.text("H Y M E N O P T E R A", "Order", x=500, y=978, size=24, font="Virelai Sans",
       color="#B8B088", justify="center")

d.finish("leafcutter-ant-V1R00")
