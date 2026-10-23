#!/usr/bin/env python3
"""Dobsonfly — field-guide plate V1R00. A male Corydalus in lateral view on a
stream stone, head raised, the absurd sickle mandibles open and crossing at
the tips, curving filiform antennae, smoky wings folded over the abdomen with
dense ladder venation. Mottled brown body. Slate stream-stone plate.
1000x1000. House style: gradients + translucent shading, never flat fills.
The insect is drawn in a local frame (ground at y=GROUND) and pushed through
one similarity map (scale + head-up tilt) so every part shares the pose.
Plate = circle center (500,460) r420."""
import sys, os, math, re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Dobsonfly — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420
INK = "#2B2016"
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

# --- local frame -> canvas ----------------------------------------------------------
GROUND = 622
S, ANG = 1.04, math.radians(7)
PIV_L, PIV_C = (520, GROUND), (478, 628)
_c, _s = math.cos(ANG), math.sin(ANG)

def T(x, y):
    lx, ly = (x - PIV_L[0]) * S, (y - PIV_L[1]) * S
    X, Y = lx*_c - ly*_s + PIV_C[0], lx*_s + ly*_c + PIV_C[1]
    chk(X, Y)
    return X, Y

_pair = re.compile(r"(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)")
def I(dstr):
    return _pair.sub(lambda m: "%.1f,%.1f" % T(float(m.group(1)), float(m.group(2))), dstr)

def ip(dstr, name, **kw):
    return d.path(I(dstr), name, **kw)

def cub(p0, p1, p2, p3, t):
    u = 1 - t
    x = u**3*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t**3*p3[0]
    y = u**3*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t**3*p3[1]
    dx = 3*u*u*(p1[0]-p0[0]) + 6*u*t*(p2[0]-p1[0]) + 3*t*t*(p3[0]-p2[0])
    dy = 3*u*u*(p1[1]-p0[1]) + 6*u*t*(p2[1]-p1[1]) + 3*t*t*(p3[1]-p2[1])
    return x, y, dx, dy

def taper(c, w0, w1, n=32, bulge=0.0):
    L, Rr = [], []
    for i in range(n + 1):
        t = i / n
        x, y, dx, dy = cub(*c, t)
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy/ln, dx/ln
        w = (w0 + (w1 - w0)*t + bulge*math.sin(math.pi*t)) / 2
        L.append((x + nx*w, y + ny*w)); Rr.append((x - nx*w, y - ny*w))
    return "M" + " L".join("%.1f,%.1f" % p for p in L + Rr[::-1]) + " Z"

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

# --- palette ---------------------------------------------------------------------
BG = lin(90, (0, "#1C2426"), (1, "#0A0F10"))
PLATE = rad((0, "#D3D9CC"), (0.62, "#A6B1A3"), (1, "#748276"))
ROCK = rad((0, "#ABA392"), (0.5, "#7C7562"), (1, "#433E30"))
WATER = lin(90, (0, "#5E8A86", 0.5), (0.5, "#3E6866", 0.68), (1, "#24403E", 0.85))
BODY = rad((0, "#B4895A"), (0.6, "#7E5A36"), (1, "#4A321C"))
HEAD = rad((0, "#C49A64"), (0.6, "#8A6338"), (1, "#523720"))
ABDO = lin(90, (0, "#8E6A40"), (1, "#4E3620"))
MAND_NEAR = lin(0, (0, "#3A2410"), (0.55, "#7A5530"), (1, "#4A3018"))
MAND_FAR = lin(0, (0, "#2A1A0C"), (1, "#3E2814"))
LEG = lin(90, (0, "#B89260"), (1, "#6E4E2C"))
LEG_FAR = lin(90, (0, "#6E5236"), (1, "#3E2C1A"))
WING = lin(90, (0, "#8A7E66", 0.28), (0.55, "#6E6450", 0.40), (1, "#4E4636", 0.52))
EYE = rad((0, "#6E7466"), (0.6, "#2E3028"), (1, "#14140E"))

# --- backdrop + plate -------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG, stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876, fill="#AEB7AA", opacity=6, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840, fill=PLATE, stroke="#4E5A52", strokeWidth=6)
for i, (x, y, rx, ry, o) in enumerate([(280, 190, 90, 50, 13), (700, 180, 110, 56, 11), (560, 320, 120, 44, 8),
                                       (780, 360, 56, 32, 9)]):
    d.path(lell(x, y, rx, ry, -12), f"Dapple {i+1}", fill="#FFFFF0", opacity=o, stroke=NONE)
# overhanging streamside fronds, top-right, kept inside the rim
for i, (base, tip, w) in enumerate([((808, 290), (660, 160), 0.85), ((830, 360), (712, 262), 0.7)]):
    bx, by = base; tx, ty = tip
    c = [(bx, by), (bx - 60, by - 70), (tx + 70, ty + 10), (tx, ty)]
    d.path(cpath(c), f"Frond {i+1} rib", fill=NONE, stroke="#4E6A40", strokeWidth=4, opacity=55, cap="round")
    for k in range(1, 12):
        x, y, dx, dy = cub(*c, k/12)
        ln = math.hypot(dx, dy); nx, ny = -dy/ln, dx/ln
        L = 34 * w * math.sin(math.pi * k/12) + 8
        for sgn in (1, -1):
            ex, ey = x + nx*L*sgn + dx/ln*10, y + ny*L*sgn + dy/ln*10
            chk(ex, ey, 30)
            d.path(f"M{x:.1f},{y:.1f} Q{(x+ex)/2 + nx*3*sgn:.1f},{(y+ey)/2 + ny*3*sgn:.1f} {ex:.1f},{ey:.1f}",
                   f"Frond {i+1} leaflet {k}{'ab'[sgn<0]}", fill=NONE, stroke="#5E7E4A",
                   strokeWidth=6, opacity=40, cap="round")
for i, (x, y, w) in enumerate([(180, 300, 7), (300, 120, 6), (640, 420, 5), (860, 470, 5),
                               (150, 470, 6), (420, 160, 5)]):
    chk(x, y, 12)
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w, fill="#5E6A60", opacity=35, stroke=NONE)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F0F2E8", strokeWidth=3, opacity=45)

# --- stream stone: domed, its ridge is the insect's ground line ----------------------
Gl, Gr = T(286, GROUND + 2), T(716, GROUND + 2)
ly0, ry0 = 770, 744
x0, _ = disc_x(ly0); _, x1 = disc_x(ry0)
ROCK_D = (f"M{x0:.1f},{ly0} C{x0-40:.1f},{ly0-70} {Gl[0]-70:.1f},{Gl[1]+12:.1f} {Gl[0]:.1f},{Gl[1]:.1f} "
          f"C{Gl[0]+140:.1f},{Gl[1]+(Gr[1]-Gl[1])/3:.1f} {Gr[0]-140:.1f},{Gr[1]-(Gr[1]-Gl[1])/3:.1f} {Gr[0]:.1f},{Gr[1]:.1f} "
          f"C{Gr[0]+90:.1f},{Gr[1]+6:.1f} {x1+40:.1f},{ry0-60:.1f} {x1:.1f},{ry0} "
          f"A420,420 0 0 1 {x0:.1f},{ly0} Z")
d.path(ROCK_D, "Stream stone", fill=ROCK, stroke=INK, strokeWidth=5)
d.path(f"M{Gl[0]+20:.1f},{Gl[1]+16:.1f} C{Gl[0]+80:.1f},{Gl[1]+4:.1f} {Gr[0]-80:.1f},{Gr[1]-4:.1f} {Gr[0]+40:.1f},{Gr[1]+16:.1f} "
       f"C{Gr[0]-80:.1f},{Gr[1]+14:.1f} {Gl[0]+80:.1f},{Gl[1]+26:.1f} {Gl[0]+20:.1f},{Gl[1]+16:.1f} Z",
       "Stone crown light", fill="#F0EAD8", opacity=32, stroke=NONE)
for i, (x, y, rx, ry, c, o, rot) in enumerate([
        (250, 700, 56, 20, "#6E8A4A", 42, -14), (720, 668, 66, 18, "#6E8A4A", 38, 6),
        (430, 690, 50, 13, "#5A7A3C", 28, -4), (800, 712, 36, 13, "#5A7A3C", 30, 18),
        (560, 726, 120, 26, "#2E2A1E", 26, 0), (300, 760, 90, 22, "#2E2A1E", 24, 0),
        (360, 660, 40, 10, "#F0EAD8", 18, -8)]):
    d.path(lell(x, y, rx, ry, rot), f"Stone patch {i+1}", fill=c, opacity=o, stroke=NONE)
for i, (x, y) in enumerate([(260, 730), (350, 690), (610, 690), (740, 720), (480, 740), (650, 760), (200, 740)]):
    d.shape("ellipse", f"Stone grain {i+1}", x=x, y=y, width=6, height=5, fill="#2E2A20", opacity=45, stroke=NONE)

# --- legs --------------------------------------------------------------------------
def leg(name, base, knee, ax, toe_dx, fill, far=False):
    ankle = (ax, GROUND - 3)
    toe = (ax + toe_dx, GROUND)
    fx, fy = knee[0]-base[0], knee[1]-base[1]
    fem = [base, (base[0]+fx*0.33, base[1]+fy*0.33 - 5), (base[0]+fx*0.66, base[1]+fy*0.66 - 5), knee]
    tx, ty = ankle[0]-knee[0], ankle[1]-knee[1]
    tib = [knee, (knee[0]+tx*0.33, knee[1]+ty*0.33), (knee[0]+tx*0.66, knee[1]+ty*0.66), ankle]
    sw = 2 if far else 2.5
    ip(taper(fem, 12, 8, bulge=4), f"{name} femur", fill=fill, stroke=INK, strokeWidth=sw)
    ip(taper(tib, 7, 5), f"{name} tibia", fill=fill, stroke=INK, strokeWidth=sw)
    ip(f"M{ankle[0]:.1f},{ankle[1]:.1f} L{(ankle[0]*0.6+toe[0]*0.4):.1f},{GROUND-1:.1f} L{toe[0]:.1f},{toe[1]:.1f}",
       f"{name} tarsus", fill=NONE, stroke="#3E2A16" if far else "#5A3E20", strokeWidth=4, cap="round", join="round")
    ip(f"M{toe[0]:.1f},{toe[1]:.1f} L{toe[0]+3*(1 if toe_dx > 0 else -1):.1f},{toe[1]+3:.1f}",
       f"{name} claw", fill=NONE, stroke="#2E1E10", strokeWidth=3, cap="round")
    ip(lell(knee[0], knee[1], 5, 5), f"{name} knee", fill="#3E2A16", opacity=70, stroke=NONE)
    if not far:
        ip(f"M{base[0]+fx*0.2:.1f},{base[1]+fy*0.2-4:.1f} L{base[0]+fx*0.78:.1f},{base[1]+fy*0.78-4:.1f}",
           f"{name} femur light", fill=NONE, stroke="#F0D8A8", strokeWidth=3, opacity=45, cap="round")

leg("Far foreleg", (394, 542), (366, 566), 352, -22, LEG_FAR, far=True)
leg("Far midleg", (478, 548), (522, 568), 534, 20, LEG_FAR, far=True)
leg("Far hindleg", (512, 548), (606, 562), 662, 26, LEG_FAR, far=True)

# --- far mandible + far antenna ------------------------------------------------------
MF = [(306, 500), (248, 458), (184, 462), (152, 520)]
ip(taper(MF, 17, 3, bulge=5), "Far mandible", fill=MAND_FAR, stroke=INK, strokeWidth=2.5)
AF = [(332, 478), (334, 400), (240, 384), (262, 284)]
ip(cpath(AF), "Far antenna", fill=NONE, stroke="#3A2814", strokeWidth=5, cap="round")
ip(cpath(AF), "Far antenna rings", fill=NONE, stroke="#7A5E3C", strokeWidth=3, dash=[2, 6], opacity=60)

# --- abdomen (shows through the wing) -------------------------------------------------
ip("M478,502 C560,494 680,498 770,512 C792,516 800,532 782,542 C700,558 580,562 486,554 Z",
   "Abdomen", fill=ABDO, stroke=INK, strokeWidth=4)
for i, x in enumerate(range(520, 770, 32)):
    ip(f"M{x},{502 - (x-480)*0.02:.0f} C{x+6},520 {x+6},540 {x},{556 - (x-480)*0.03:.0f}",
       f"Tergite seam {i+1}", fill=NONE, stroke="#2E2010", strokeWidth=3, opacity=50, cap="round")
ip("M786,530 C804,532 818,528 830,520", "Cercus", fill=NONE, stroke="#4A3018", strokeWidth=4, cap="round")

# --- thorax ---------------------------------------------------------------------------
ip("M436,484 C452,470 486,470 502,486 C512,500 512,540 500,552 C486,560 450,560 438,550 Z",
   "Pterothorax", fill=BODY, stroke=INK, strokeWidth=4)
ip("M368,488 C390,482 420,482 440,486 C450,488 454,496 454,506 L454,532 "
   "C454,542 446,548 436,548 L374,548 C366,548 362,542 362,532 L362,498 C362,492 364,489 368,488 Z",
   "Pronotum", fill=BODY, stroke=INK, strokeWidth=4)
ip("M372,494 C396,489 424,489 444,494", "Pronotum rim light", fill=NONE,
   stroke="#F2D9A6", strokeWidth=3, opacity=50, cap="round")
ip("M370,542 C396,546 424,546 448,540", "Pronotum belly shade", fill=NONE,
   stroke="#2E2010", strokeWidth=4, opacity=35, cap="round")
for i, (x, y, rx, ry, c, o) in enumerate([(388, 512, 12, 8, "#E8C890", 40), (420, 518, 10, 7, "#E8C890", 34),
                                          (404, 534, 14, 6, "#2E2010", 30), (440, 512, 6, 9, "#2E2010", 28),
                                          (476, 500, 14, 9, "#E8C890", 26)]):
    ip(lell(x, y, rx, ry), f"Thorax mottle {i+1}", fill=c, opacity=o, stroke=NONE)

# --- head -----------------------------------------------------------------------------
ip("M302,494 C302,480 320,474 340,474 L360,476 C372,478 378,488 378,500 L378,530 "
   "C378,542 368,550 354,550 L320,550 C306,550 298,542 298,528 Z", "Head", fill=HEAD, stroke=INK, strokeWidth=4)
ip("M310,486 C322,478 346,478 362,482", "Head crown light", fill=NONE,
   stroke="#F6E0B0", strokeWidth=3, opacity=55, cap="round")
for i, (x, y, rx, ry, c, o) in enumerate([(322, 506, 10, 7, "#F0D498", 42), (336, 530, 13, 6, "#2E2010", 28),
                                          (366, 528, 7, 9, "#F0D498", 30)]):
    ip(lell(x, y, rx, ry), f"Head mottle {i+1}", fill=c, opacity=o, stroke=NONE)
ip("M374,496 L388,488 L380,506 Z", "Postocular spine", fill="#5A3E20", stroke=INK, strokeWidth=2)
ip(lell(352, 496, 12, 13), "Compound eye", fill=EYE, stroke=INK, strokeWidth=2.5)
ip(lell(348, 491, 4, 3.5), "Eye glint", fill="#FFFFFF", opacity=80, stroke=NONE)
for i, (x, y) in enumerate([(330, 484), (340, 481)]):
    ip(lell(x, y, 2.6, 2.6), f"Ocellus {i+1}", fill="#F4E4C0", opacity=75, stroke=NONE)
ip("M308,546 C300,558 292,562 282,564", "Palp", fill=NONE, stroke="#6E4E2C", strokeWidth=4, cap="round")

# --- near mandible: the absurd one -----------------------------------------------------
MN = [(304, 526), (246, 566), (180, 558), (152, 486)]
ip(taper(MN, 19, 3, bulge=6), "Near mandible", fill=MAND_NEAR, stroke=INK, strokeWidth=3)
ip(cpath([(294, 528), (250, 558), (198, 552), (170, 506)]), "Near mandible sheen",
   fill=NONE, stroke="#E2C08A", strokeWidth=3, opacity=45, cap="round")
for i, t in enumerate([0.34, 0.52]):
    for c, nm, sgn, w0 in [(MN, "Near", 1, 19), (MF, "Far", -1, 17)]:
        x, y, dx, dy = cub(*c, t)
        ln = math.hypot(dx, dy); nx, ny = -dy/ln*sgn, dx/ln*sgn
        w = (w0 + (3 - w0)*t + 6*math.sin(math.pi*t)) / 2
        bx, by = x + nx*w, y + ny*w
        ux, uy = dx/ln, dy/ln
        ip(f"M{bx-ux*5:.1f},{by-uy*5:.1f} L{bx+nx*8:.1f},{by+ny*8:.1f} L{bx+ux*5:.1f},{by+uy*5:.1f} Z",
           f"{nm} mandible tooth {i+1}", fill="#3A2410", stroke=INK, strokeWidth=1.5)

# --- near antenna ------------------------------------------------------------------------
AN = [(318, 478), (306, 398), (196, 392), (212, 294)]
ip(cpath(AN), "Near antenna", fill=NONE, stroke="#4A3018", strokeWidth=6, cap="round")
ip(cpath(AN), "Near antenna rings", fill=NONE, stroke="#B08A58", strokeWidth=3, dash=[2, 6], opacity=70)

# --- near legs ---------------------------------------------------------------------------
leg("Foreleg", (384, 546), (350, 566), 334, -24, LEG)
leg("Midleg", (466, 552), (504, 572), 490, -22, LEG)
leg("Hindleg", (500, 552), (588, 566), 640, 28, LEG)

# --- wings, folded over the abdomen --------------------------------------------------------
def wing_outline(dx=0, dy=0):
    return (f"M{452+dx},{482+dy} C{560+dx},{466+dy} {700+dx},{468+dy} {800+dx},{478+dy} "
            f"C{846+dx},{486+dy} {866+dx},{506+dy} {858+dx},{530+dy} "
            f"C{850+dx},{548+dy} {790+dx},{560+dy} {700+dx},{566+dy} "
            f"C{600+dx},{570+dy} {520+dx},{566+dy} {470+dx},{560+dy} "
            f"C{446+dx},{548+dy} {444+dx},{500+dy} {452+dx},{482+dy} Z")

ip(wing_outline(2, 8), "Hind wing", fill=WING, stroke="#3E3424", strokeWidth=3, opacity=50)
ip(wing_outline(), "Forewing", fill=WING, stroke="#3E3424", strokeWidth=3.5)
VEINS = [
    [(456, 488), (560, 474), (700, 476), (812, 486)],
    [(456, 496), (580, 484), (720, 486), (848, 500)],
    [(458, 512), (590, 502), (720, 506), (860, 520)],
    [(458, 528), (590, 522), (720, 530), (852, 542)],
    [(458, 542), (580, 542), (700, 552), (800, 558)],
    [(462, 552), (540, 558), (600, 562), (660, 566)],
]
for i, v in enumerate(VEINS):
    ip(cpath(v), f"Vein {i+1}", fill=NONE, stroke="#3A3020", strokeWidth=3, opacity=75, cap="round")
for i, t in enumerate([k/22 for k in range(2, 21)]):
    x, y, _, _ = cub(*VEINS[0], t)
    ip(f"M{x:.1f},{y:.1f} L{x-3:.1f},{y-9:.1f}", f"Costal crossvein {i+1}", fill=NONE,
       stroke="#3A3020", strokeWidth=3, opacity=55, cap="round")
for j in range(1, len(VEINS) - 1):
    a, b = VEINS[j], VEINS[j + 1]
    n = 13 if j < 3 else 10
    for k in range(1, n):
        t = k / n + (0.012 if (k + j) % 2 else -0.012)
        xa, ya, _, _ = cub(*a, t)
        xb, yb, _, _ = cub(*b, min(t + 0.01, 1))
        ip(f"M{xa:.1f},{ya:.1f} L{xb:.1f},{yb:.1f}", f"Crossvein {j}-{k}", fill=NONE,
           stroke="#3A3020", strokeWidth=3, opacity=45, cap="round")
for i, (x, y, rx, ry) in enumerate([(540, 500, 9, 6), (610, 520, 10, 7), (680, 498, 8, 6), (720, 536, 11, 7),
                                     (790, 512, 9, 6), (640, 548, 8, 5), (560, 532, 7, 5)]):
    ip(lell(x, y, rx, ry), f"Wing spot {i+1}", fill="#F4EEDC", opacity=40, stroke=NONE)
ip("M470,486 C580,470 700,472 820,486 C700,482 580,482 470,494 Z", "Wing sheen",
   fill="#FFFFFF", opacity=26, stroke=NONE)
ip("M600,474 C680,470 740,474 790,480", "Wing iridescence", fill=NONE,
   stroke="#B8D8E0", strokeWidth=4, opacity=30, cap="round")

# --- the stream, over the stone's lower body ------------------------------------------------
WY = 752
wx0, wx1 = disc_x(WY)
d.path(f"M{wx0:.1f},{WY} C240,742 320,762 420,752 C520,742 620,764 720,752 C790,744 840,758 {wx1:.1f},{WY} "
       f"A420,420 0 0 1 {wx0:.1f},{WY} Z", "Stream water", fill=WATER, stroke=NONE)
for i, (y0, o, sw) in enumerate([(752, 60, 5), (780, 32, 4), (812, 22, 3)]):
    a, b = disc_x(y0)
    a, b = a + 40, b - 40
    d.path(f"M{a:.0f},{y0} C{a+(b-a)*0.25:.0f},{y0-9} {a+(b-a)*0.45:.0f},{y0+9} {(a+b)/2:.0f},{y0} "
           f"C{a+(b-a)*0.6:.0f},{y0-9} {a+(b-a)*0.8:.0f},{y0+9} {b:.0f},{y0}",
           f"Ripple {i+1}", fill=NONE, stroke="#E6F2EE", strokeWidth=sw, opacity=o, cap="round")
for i, (x, y, w) in enumerate([(250, 746, 10), (420, 756, 8), (560, 744, 9), (720, 754, 7), (330, 762, 6)]):
    d.shape("ellipse", f"Foam fleck {i+1}", x=x, y=y, width=w, height=w*0.6, fill="#FFFFFF", opacity=50, stroke=NONE)

if FAR:
    print("WARN points near the rim:", FAR[:12])

d.text("DOBSONFLY", "Name", x=500, y=940, size=58, font="Virelai Sans", color="#E2E6DC", justify="center")
d.text("M E G A L O P T E R A", "Order", x=500, y=978, size=24, font="Virelai Sans",
       color="#A9B4AA", justify="center")

d.finish("dobsonfly-V1R00")
