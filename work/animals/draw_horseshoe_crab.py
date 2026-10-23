#!/usr/bin/env python3
"""Horseshoe crab — field-guide plate V1R00. Three-quarter top view of the
armored helmet: horseshoe prosoma dome with ridges and kidney eyes, hinged
spiny opisthosoma, long dagger telson. Bronze-olive shell on a wet primordial
shore with a tide lapping the top of the plate. 1000x1000.
House style: gradients + translucent shading, never flat fills.
The animal is drawn in a local frame (head up, hinge at the origin) and pushed
through one affine map — scale, foreshorten, rotate — so the 3/4 tilt stays
consistent across every part. Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Horseshoe Crab — Field Plate", 1000, 1000)

INK = "#2A2618"   # deep olive-brown, not black
BG_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#1A2420"}, {"offset": 1, "color": "#080D0B"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#EADBB4"}, {"offset": 0.65, "color": "#CDB584"},
    {"offset": 1, "color": "#9C8458"}]}}
WATER_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#3E6A68", "opacity": 0.85},
    {"offset": 0.7, "color": "#6F9A8E", "opacity": 0.55},
    {"offset": 1, "color": "#A9C4B0", "opacity": 0.25}]}}
DOME_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#B8A262"}, {"offset": 0.5, "color": "#86733C"},
    {"offset": 1, "color": "#4E4420"}]}}
RIM_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#4A3F1E"}, {"offset": 1, "color": "#2C2510"}]}}
ABDO_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#A8924F"}, {"offset": 0.6, "color": "#7A6834"},
    {"offset": 1, "color": "#4A401C"}]}}
SPINE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#8C7840"}, {"offset": 1, "color": "#4A3F1E"}]}}
TELSON_DARK = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#5E5026"}, {"offset": 1, "color": "#3A3216"}]}}
TELSON_LIGHT = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#A8924F"}, {"offset": 1, "color": "#6E5E2C"}]}}
EYE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#6A6A58"}, {"offset": 0.6, "color": "#2E2C22"},
    {"offset": 1, "color": "#16140E"}]}}

CX, CY, R = 500, 460, 420

# --- local frame -> canvas ------------------------------------------------------
S, SQ, ANG = 0.78, 0.78, math.radians(-32)
ANCHOR_L, ANCHOR_C = (0, 135), (488, 496)
_ca, _sa = math.cos(ANG), math.sin(ANG)
FAR = []   # points that strayed toward the rim

def T(x, y):
    lx, ly = (x - ANCHOR_L[0]) * S, (y - ANCHOR_L[1]) * S * SQ
    X = lx * _ca - ly * _sa + ANCHOR_C[0]
    Y = lx * _sa + ly * _ca + ANCHOR_C[1]
    if math.hypot(X - CX, Y - CY) > R - 30:
        FAR.append((round(X), round(Y)))
    return X, Y

def P(cmds, dx=0, dy=0):
    out = []
    for c in cmds:
        op, pts = c[0], c[1:]
        out.append(op + " ".join("%.1f,%.1f" % (T(*p)[0] + dx, T(*p)[1] + dy) for p in pts))
    return " ".join(out)

def lell(cx, cy, rx, ry):
    k = 0.5523
    return [("M", (cx + rx, cy)),
            ("C", (cx + rx, cy + ry*k), (cx + rx*k, cy + ry), (cx, cy + ry)),
            ("C", (cx - rx*k, cy + ry), (cx - rx, cy + ry*k), (cx - rx, cy)),
            ("C", (cx - rx, cy - ry*k), (cx - rx*k, cy - ry), (cx, cy - ry)),
            ("C", (cx + rx*k, cy - ry), (cx + rx, cy - ry*k), (cx + rx, cy)), ("Z",)]

def cubic(p0, p1, p2, p3, t):
    u = 1 - t
    x = u**3*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t**3*p3[0]
    y = u**3*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t**3*p3[1]
    dx = 3*u*u*(p1[0]-p0[0]) + 6*u*t*(p2[0]-p1[0]) + 3*t*t*(p3[0]-p2[0])
    dy = 3*u*u*(p1[1]-p0[1]) + 6*u*t*(p2[1]-p1[1]) + 3*t*t*(p3[1]-p2[1])
    return x, y, dx, dy

def on_disc(x, y, pad):
    return math.hypot(x - CX, y - CY) <= R - pad

# --- backdrop + plate -------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#C9B07A", opacity=6, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#5E4E2E", strokeWidth=6)

# tide lapping the top of the plate: wavy waterline, closed on the disc's own arc
WY = 292
wx0 = CX - math.sqrt(R*R - (WY - CY)**2); wx1 = CX + math.sqrt(R*R - (WY - CY)**2)
d.path(f"M{wx0:.1f},{WY} C220,318 300,270 390,300 C470,326 540,280 620,302 "
       f"C700,322 790,280 {wx1:.1f},{WY} A{R},{R} 0 0 0 {wx0:.1f},{WY} Z",
       "Tide water", fill=WATER_GRAD, stroke=NONE)
# wet-sand darkening just below the waterline
d.path(f"M{wx0:.1f},{WY} C220,318 300,270 390,300 C470,326 540,280 620,302 "
       f"C700,322 790,280 {wx1:.1f},{WY} C800,330 700,352 620,338 "
       f"C540,326 470,360 390,340 C300,318 220,352 {wx0+6:.1f},{WY+18} Z",
       "Wet sand band", fill="#7E6A44", opacity=22, stroke=NONE)
# foam lace riding the waterline
d.path("M128,300 C220,322 300,274 390,304 C470,330 540,284 620,306 C700,326 790,284 870,298",
       "Foam line", fill=NONE, stroke="#F4F0E0", strokeWidth=6, opacity=60, cap="round")
d.path("M160,282 C240,300 320,258 400,284 C480,306 550,262 630,284 C710,302 780,266 845,276",
       "Foam line back", fill=NONE, stroke="#F4F0E0", strokeWidth=3, opacity=35, cap="round")
for i, (x, y, w) in enumerate([(230,312,9),(352,294,7),(470,318,10),(585,296,7),(700,316,8),(800,296,6)]):
    d.shape("ellipse", f"Foam bubble {i+1}", x=x, y=y, width=w, height=w*0.7,
            fill="#FFFFFF", opacity=45, stroke=NONE)
# swell lines out in the water
for i, (y0, a) in enumerate([(200, 26), (150, 20), (110, 15)]):
    half = math.sqrt(R*R - (y0 - CY)**2) - 40
    d.path(f"M{CX-half:.0f},{y0} C{CX-half/2:.0f},{y0-14} {CX-half/4:.0f},{y0+12} {CX:.0f},{y0} "
           f"C{CX+half/4:.0f},{y0-12} {CX+half/2:.0f},{y0+14} {CX+half:.0f},{y0}",
           f"Swell {i+1}", fill=NONE, stroke="#D8EAE0", strokeWidth=4, opacity=a, cap="round")

d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F4E8C8", strokeWidth=3, opacity=50)

# sand ripples (strokes kept clear of the rim)
for i, (y0, a) in enumerate([(640, 26), (690, 22), (740, 18), (790, 14)]):
    half = math.sqrt(R*R - (y0 - CY)**2) - 60
    d.path(f"M{CX-half:.0f},{y0} C{CX-half/2:.0f},{y0-12} {CX:.0f},{y0+10} {CX+half/2:.0f},{y0-4} "
           f"C{CX+half*0.75:.0f},{y0-10} {CX+half*0.9:.0f},{y0+2} {CX+half:.0f},{y0}",
           f"Sand ripple {i+1}", fill=NONE, stroke="#8A7348", strokeWidth=5, opacity=a, cap="round")
# grains + pebbles + a broken shell; all checked to sit inside the rim
for i, (x, y, w) in enumerate([(190,420,6),(820,400,7),(160,560,8),(840,560,6),(260,760,7),
                               (720,780,6),(400,830,5),(600,840,6),(300,380,5),(700,372,5),
                               (150,480,5),(860,480,5),(500,860,4)]):
    assert on_disc(x, y, 14), (x, y)
    d.shape("ellipse", f"Sand grain {i+1}", x=x, y=y, width=w, height=w,
            fill="#6E5A38", opacity=40, stroke=NONE)
for i, (x, y, w, h, c) in enumerate([(205,640,30,20,"#8E8070"),(232,660,18,13,"#A89A86"),
                                     (770,690,26,18,"#7E7262"),(330,792,20,14,"#9A8C78")]):
    assert on_disc(x + w, y + h, 12)
    d.shape("ellipse", f"Pebble {i+1}", x=x, y=y, width=w, height=h,
            fill={"gradient": {"kind": "radial", "stops": [
                {"offset": 0, "color": "#D8CCB8"}, {"offset": 1, "color": c}]}},
            stroke="#5E5040", strokeWidth=2, opacity=85)
d.path("M520,808 C532,790 560,786 574,800 C564,800 554,806 548,818 C540,810 530,808 520,808 Z",
       "Shell shard", fill={"gradient": {"kind": "linear", "stops": [
           {"offset": 0, "color": "#F2E6D2"}, {"offset": 1, "color": "#C8A88A"}]}},
       stroke="#6E5A48", strokeWidth=2)
for i, (a, b) in enumerate([((534,804),(546,794)), ((542,808),(558,796))]):
    d.path(f"M{a[0]},{a[1]} L{b[0]},{b[1]}", f"Shard rib {i+1}", fill=NONE,
           stroke="#A88870", strokeWidth=2, opacity=70, cap="round")

# --- the animal's geometry (local frame) --------------------------------------------
PRO = [("M", (-300, 96)),
       ("C", (-334, -90), (-222, -305), (0, -308)),
       ("C", (222, -305), (334, -90), (300, 96)),
       ("C", (250, 44), (150, 28), (0, 28)),
       ("C", (-150, 28), (-250, 44), (-300, 96)), ("Z",)]
ABD_R = [(132, -20), (134, 40), (124, 104), (102, 140)]
ABD = [("M", (-132, -20)), ("L", (132, -20)),
       ("C", ABD_R[1], ABD_R[2], ABD_R[3]),
       ("C", (80, 170), (42, 184), (0, 186)),
       ("C", (-42, 184), (-80, 170), (-102, 140)),
       ("C", (-124, 104), (-134, 40), (-132, -20)), ("Z",)]
TEL_L = [("M", (-24, 160)), ("L", (0, 160)), ("L", (0, 590)), ("L", (-15, 400)), ("Z",)]
TEL_R = [("M", (0, 160)), ("L", (24, 160)), ("L", (15, 400)), ("L", (0, 590)), ("Z",)]
# outer front arc of the prosoma, genal tip to genal tip
ARC = [(-300, 96), (-334, -90), (-222, -305), (0, -308), (222, -305), (334, -90), (300, 96)]

def rim_band(arc, depth):
    """Crescent between the outer arc and its copy dropped by `depth` px:
    only the near edge shows its thickness, not the concave rear margin."""
    fwd = [T(*p) for p in arc]
    low = [(x, y + depth) for x, y in fwd]
    s = "M%.1f,%.1f" % low[0]
    for i in range(1, len(low), 3):
        s += " C" + " ".join("%.1f,%.1f" % low[i + k] for k in range(3))
    back = fwd[::-1]
    s += " L%.1f,%.1f" % back[0]
    for i in range(1, len(back), 3):
        s += " C" + " ".join("%.1f,%.1f" % back[i + k] for k in range(3))
    return s + " Z"

# --- cast shadow on the sand ----------------------------------------------------------
d.path(P(PRO, 22, 30), "Shell shadow", fill="#3C2E18", opacity=26, stroke=NONE)
d.path(P(ABD, 22, 30), "Abdomen shadow", fill="#3C2E18", opacity=24, stroke=NONE)
d.path(P([("M", (-20, 160)), ("L", (0, 590)), ("L", (20, 160)), ("Z",)], 18, 22),
       "Telson shadow", fill="#3C2E18", opacity=22, stroke=NONE)
# faint drag trail the telson left behind
tail_tip = T(0, 590)
tx, ty = tail_tip
d.path(f"M{tx+6:.0f},{ty+10:.0f} C{tx+20:.0f},{ty+28:.0f} {tx+28:.0f},{ty+46:.0f} {tx+34:.0f},{ty+66:.0f}",
       "Drag trail", fill=NONE, stroke="#7A6440", strokeWidth=4, opacity=30, cap="round")
assert on_disc(tx + 34, ty + 66, 20), (tx, ty)
for i, k in enumerate(range(3)):
    for side in (-1, 1):
        px, py = tx + 14 + k*9 + side*16, ty + 22 + k*20
        assert on_disc(px, py, 20)
        d.shape("ellipse", f"Leg print {i+1}{'L' if side < 0 else 'R'}", x=round(px), y=round(py),
                width=7, height=5, fill="#6E5836", opacity=30, stroke=NONE)

# --- telson: two faces of a triangular spike ------------------------------------------
d.path(P(TEL_L), "Telson shade face", fill=TELSON_DARK, stroke=INK, strokeWidth=4)
d.path(P(TEL_R), "Telson lit face", fill=TELSON_LIGHT, stroke=INK, strokeWidth=4)
d.path(P([("M", (0, 172)), ("L", (0, 560))]), "Telson keel light",
       fill=NONE, stroke="#E8D9A0", strokeWidth=3, opacity=55, cap="round")
for i, y in enumerate([205, 250, 295]):
    d.path(P([("M", (-1, y)), ("L", (-4, y + 14)), ("L", (2, y + 14)), ("Z",)]),
           f"Telson keel spine {i+1}", fill="#3A3216", stroke=NONE, opacity=70)

# --- shell thickness: the near edge you see in a 3/4 view ------------------------------
d.path(P(ABD, 0, 11), "Abdomen rim", fill=RIM_GRAD, stroke=INK, strokeWidth=4)

# --- opisthosoma marginal spines (drawn under the abdomen plate) ------------------------
def margin_spines(side):
    pts = [(side*p[0], p[1]) for p in ABD_R]
    for j, t in enumerate([0.22, 0.36, 0.50, 0.64, 0.78, 0.92]):
        x, y, ddx, ddy = cubic(*pts, t)
        ln = math.hypot(ddx, ddy) or 1
        ux, uy = ddx/ln, ddy/ln
        nx, ny = uy*side, -ux*side
        if nx*side < 0:
            nx, ny = -nx, -ny
        b0 = (x - ux*9 - nx*4, y - uy*9 - ny*4)
        b1 = (x + ux*9 - nx*4, y + uy*9 - ny*4)
        L = 30 + (6 if j % 2 == 0 else -4)
        tip = (x + nx*L + ux*14, y + ny*L + uy*14)
        d.path(P([("M", b0), ("L", tip), ("L", b1), ("Z",)]),
               f"Margin spine {'L' if side < 0 else 'R'}{j+1}", fill=SPINE_GRAD,
               stroke=INK, strokeWidth=3)
margin_spines(-1)
margin_spines(1)

# --- opisthosoma plate --------------------------------------------------------------------
d.path(P(ABD), "Abdomen", fill=ABDO_GRAD, stroke=INK, strokeWidth=5)
# flat border shelf: inner outline, translucent
d.path(P([("M", (-104, 20)), ("C", (-108, 60), (-100, 104), (-82, 128)),
          ("C", (-62, 152), (-32, 162), (0, 164)),
          ("C", (32, 162), (62, 152), (82, 128)),
          ("C", (100, 104), (108, 60), (104, 20))]),
       "Abdomen shelf", fill=NONE, stroke="#3A3216", strokeWidth=4, opacity=45, cap="round")
d.path(P([("M", (-98, 30)), ("C", (-102, 66), (-96, 104), (-78, 128))]),
       "Abdomen shelf light", fill=NONE, stroke="#D8C68A", strokeWidth=4, opacity=35, cap="round")
# median keel + spines
d.path(P([("M", (0, 20)), ("L", (0, 162))]), "Abdomen keel",
       fill=NONE, stroke="#3A3216", strokeWidth=6, opacity=50, cap="round")
d.path(P([("M", (-5, 24)), ("L", (-5, 156))]), "Abdomen keel light",
       fill=NONE, stroke="#D8C68A", strokeWidth=3, opacity=45, cap="round")
for i, y in enumerate([66, 108, 150]):
    d.path(P([("M", (-6, y)), ("L", (0, y - 18)), ("L", (6, y)), ("Z",)]),
           f"Keel spine {i+1}", fill=SPINE_GRAD, stroke=INK, strokeWidth=2)
# six apodeme dimples per side
for side in (-1, 1):
    for j in range(6):
        y = 40 + j*21
        x = side*(58 - j*3)
        d.path(P(lell(x, y, 9, 6)), f"Apodeme {'L' if side < 0 else 'R'}{j+1}",
               fill="#2E2810", opacity=45, stroke=NONE)
# sheen on the lit half
d.path(P(lell(-50, 90, 34, 52)), "Abdomen sheen", fill="#F2E2A8", opacity=16, stroke=NONE)

# --- prosoma: thickness, dome, ridges --------------------------------------------------------
d.path(rim_band(ARC, 21), "Shell rim", fill=RIM_GRAD, stroke=INK, strokeWidth=5)
d.path(P(PRO), "Prosoma", fill=DOME_GRAD, stroke=INK, strokeWidth=6)
# flattened brim around the dome
d.path(P([("M", (-262, 46)), ("C", (-288, -76), (-196, -262), (0, -264)),
          ("C", (196, -262), (288, -76), (262, 46))]),
       "Brim crease", fill=NONE, stroke="#2E2810", strokeWidth=5, opacity=40, cap="round")
d.path(P([("M", (-276, 30)), ("C", (-300, -86), (-208, -282), (0, -286))]),
       "Brim light", fill=NONE, stroke="#E8D69A", strokeWidth=4, opacity=40, cap="round")
# slope shading outside the lateral ridges (the dome falls away)
for side in (-1, 1):
    s = side
    d.path(P([("M", (s*112, -224)), ("C", (s*180, -200), (s*244, -110), (s*252, 30)),
              ("C", (s*210, 18), (s*160, 10), (s*124, 10)),
              ("C", (s*140, -60), (s*140, -150), (s*112, -224)), ("Z",)]),
           f"Dome slope {'L' if s < 0 else 'R'}", fill="#2A2410",
           opacity=16 if s < 0 else 34, stroke=NONE)
# dome highlight, light from upper left
d.path(P(lell(-80, -150, 130, 100)), "Dome glow", fill="#FFF2C4", opacity=12, stroke=NONE)
d.path(P(lell(-70, -175, 80, 52)), "Dome highlight", fill="#FFF2C4", opacity=18, stroke=NONE)
d.path(P(lell(-90, -200, 34, 18)), "Dome highlight core", fill="#FFFFFF", opacity=22, stroke=NONE)
# median ridge
d.path(P([("M", (0, -262)), ("C", (2, -180), (2, -80), (0, 18))]), "Median ridge shade",
       fill=NONE, stroke="#2E2810", strokeWidth=8, opacity=45, cap="round")
d.path(P([("M", (-6, -258)), ("C", (-4, -180), (-4, -80), (-6, 14))]), "Median ridge light",
       fill=NONE, stroke="#F0DFA4", strokeWidth=4, opacity=55, cap="round")
for i, y in enumerate([-150, -84, -22]):
    d.path(P([("M", (-7, y)), ("L", (0, y - 20)), ("L", (7, y)), ("Z",)]),
           f"Ridge spine {i+1}", fill=SPINE_GRAD, stroke=INK, strokeWidth=2)
# lateral ridges
for side in (-1, 1):
    s = side
    d.path(P([("M", (s*104, -226)), ("C", (s*138, -150), (s*142, -60), (s*124, 8))]),
           f"Lateral ridge shade {'L' if s < 0 else 'R'}", fill=NONE, stroke="#2E2810",
           strokeWidth=7, opacity=45, cap="round")
    d.path(P([("M", (s*98, -224)), ("C", (s*130, -150), (s*134, -60), (s*116, 6))]),
           f"Lateral ridge light {'L' if s < 0 else 'R'}", fill=NONE, stroke="#F0DFA4",
           strokeWidth=3, opacity=45, cap="round")
# kidney-shaped compound eyes on the outer flank of each ridge
for side in (-1, 1):
    s = side
    ex, ey = s*150, -128
    eye = [("M", (ex - s*6, ey - 26)),
           ("C", (ex + s*14, ey - 24), (ex + s*20, ey + 14), (ex + s*4, ey + 26)),
           ("C", (ex - s*8, ey + 30), (ex - s*14, ey + 14), (ex - s*8, ey + 2)),
           ("C", (ex - s*4, ey - 6), (ex - s*18, ey - 26), (ex - s*6, ey - 26)), ("Z",)]
    d.path(P(eye), f"Compound eye {'L' if s < 0 else 'R'}", fill=EYE_GRAD, stroke=INK, strokeWidth=3)
    d.path(P(lell(ex + s*2, ey - 10, 5, 7)), f"Eye glint {'L' if s < 0 else 'R'}",
           fill="#FFFFFF", opacity=70, stroke=NONE)
# median ocelli
for side in (-1, 1):
    d.path(P(lell(side*10, -236, 4, 4)), f"Ocellus {'L' if side < 0 else 'R'}",
           fill="#1A180E", opacity=85, stroke=NONE)
# bronze mottling
for i, (x, y, rx, ry, c, o) in enumerate([
        (-200, -100, 22, 14, "#C8B06A", 22), (-60, -250, 26, 12, "#C8B06A", 24),
        (70, -230, 20, 12, "#3A3216", 20), (210, -60, 24, 16, "#3A3216", 22),
        (-230, -10, 18, 10, "#3A3216", 18), (60, -40, 16, 10, "#C8B06A", 18),
        (-60, -60, 18, 12, "#C8B06A", 20), (180, -170, 16, 10, "#3A3216", 18)]):
    d.path(P(lell(x, y, rx, ry)), f"Mottle {i+1}", fill=c, opacity=o, stroke=NONE)
# a barnacle hitchhiker on the right flank
bx, by = 196, -20
d.path(P(lell(bx, by, 15, 13)), "Barnacle", fill={"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F2ECDC"}, {"offset": 1, "color": "#A89C84"}]}},
    stroke="#5E5444", strokeWidth=2)
d.path(P(lell(bx, by, 5, 4)), "Barnacle aperture", fill="#3E3828", opacity=80, stroke=NONE)
d.path(P(lell(bx + 26, by + 16, 8, 7)), "Barnacle small", fill="#D8CEB8",
       stroke="#5E5444", strokeWidth=2, opacity=90)
# wet glints on the shell edge
for i, (x, y) in enumerate([(-250, -60), (-160, -250), (40, -292)]):
    d.path(P(lell(x, y, 7, 4)), f"Wet glint {i+1}", fill="#FFFFFF", opacity=55, stroke=NONE)

if FAR:
    print("WARN points near the rim:", FAR[:12])

# --- name -------------------------------------------------------------------------------------
d.text("HORSESHOE CRAB", "Name", x=500, y=960, size=48, font="Virelai Sans",
       color="#E8DCBC", justify="center")

d.finish("horseshoe-crab-V1R00")
