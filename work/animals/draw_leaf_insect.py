#!/usr/bin/env python3
"""Leaf insect — field-guide plate V1R00. Dorsal view, played straight: the
body is a leaf — broad nibbled lamina with a midrib and lateral veins in
lighter line work, brown edge-rot spots, six legs folded like leaflets, small
head with antennae. Fresh green over a deep forest plate; decor leaves
clamped inside the disc. 1000x1000. Gradients + translucent shading."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Leaf Insect — Field Plate", 1000, 1000)

INK = "#16220F"
CX, CY, R = 500, 460, 420
BG_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#12240F"}, {"offset": 1, "color": "#040A04"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#5E8C60"}, {"offset": 0.6, "color": "#35603E"},
    {"offset": 1, "color": "#152C1E"}]}}
LAMINA_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#A6DC62"}, {"offset": 0.5, "color": "#6FAE44"},
    {"offset": 1, "color": "#3E7A2E"}]}}
LOBE_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#92C957"}, {"offset": 1, "color": "#4E8C36"}]}}
LEG_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#88BE50"}, {"offset": 1, "color": "#467A30"}]}}
DECOR_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#4A7A4A"}, {"offset": 1, "color": "#24462C"}]}}

def clamp(x, y, r=396):
    dx, dy = x - CX, y - CY
    k = math.hypot(dx, dy)
    return (x, y) if k <= r else (CX + dx*r/k, CY + dy*r/k)

def smooth_path(pts, close=False):
    """Catmull-Rom spline through pts as a cubic path string."""
    n = len(pts)
    s = f"M{pts[0][0]:.1f},{pts[0][1]:.1f} "
    last = n if close else n - 1
    for i in range(last):
        p0 = pts[(i-1) % n]; p1 = pts[i % n]; p2 = pts[(i+1) % n]; p3 = pts[(i+2) % n]
        c1 = (p1[0] + (p2[0]-p0[0])/6.0, p1[1] + (p2[1]-p0[1])/6.0)
        c2 = (p2[0] - (p3[0]-p1[0])/6.0, p2[1] - (p3[1]-p1[1])/6.0)
        s += f"C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f} "
    return s + ("Z" if close else "")

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#5E8A5E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C8E4B8", strokeWidth=3, opacity=50)
d.shape("ellipse", "Patina 1", x=170, y=190, width=240, height=140, fill="#7FA678", opacity=18, stroke=NONE)
d.shape("ellipse", "Patina 2", x=590, y=590, width=240, height=130, fill="#0F2416", opacity=28, stroke=NONE)
for i, (x, y, w) in enumerate([(200,300,7),(790,250,6),(170,540,8),(830,450,7),
                               (260,760,6),(740,740,7),(140,420,5),(860,380,6)]):
    d.shape("ellipse", f"Forest fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#A8CC90", opacity=30, stroke=NONE)

# --- two background leaves, ghosted, clamped inside the disc --------------------
def decor_leaf(label, x, y, L, ang, op):
    a = math.radians(ang)
    tx, ty = clamp(x + math.cos(a)*L, y + math.sin(a)*L)
    mx, my = (x + tx)/2, (y + ty)/2
    nx, ny = -math.sin(a)*L*0.30, math.cos(a)*L*0.30
    d.path(f"M{x:.0f},{y:.0f} Q{mx+nx:.0f},{my+ny:.0f} {tx:.0f},{ty:.0f} "
           f"Q{mx-nx:.0f},{my-ny:.0f} {x:.0f},{y:.0f} Z",
           label, fill=DECOR_GRAD, opacity=op, stroke=NONE)
    d.path(f"M{x:.0f},{y:.0f} L{tx:.0f},{ty:.0f}", f"{label} rib",
           fill=NONE, stroke="#6E9A66", strokeWidth=3, opacity=op+10, cap="round")
decor_leaf("Decor leaf L", 200, 700, 240, -35, 45)
decor_leaf("Decor leaf R", 810, 210, 220, 145, 40)

# --- drop shadow under the insect ------------------------------------------------
d.shape("ellipse", "Insect shadow", x=320, y=330, width=370, height=460,
        fill="#0A1608", opacity=30, stroke=NONE)

# --- legs: femur stroke + flattened leaf-lobe tibia, folded like leaflets ---------
def leaflet(label, cx, cy, ln, wd, ang, fill=LOBE_GRAD, op=100):
    a = math.radians(ang)
    ux, uy = math.cos(a), math.sin(a)
    px, py = -uy, ux
    tip = (cx + ux*ln, cy + uy*ln)
    b1 = (cx + px*wd*0.5 + ux*ln*0.30, cy + py*wd*0.5 + uy*ln*0.30)
    b2 = (cx + px*wd*0.42 + ux*ln*0.72, cy + py*wd*0.42 + uy*ln*0.72)
    b3 = (cx - px*wd*0.42 + ux*ln*0.72, cy - py*wd*0.42 + uy*ln*0.72)
    b4 = (cx - px*wd*0.5 + ux*ln*0.30, cy - py*wd*0.5 + uy*ln*0.30)
    d.path(f"M{cx:.0f},{cy:.0f} C{b1[0]:.0f},{b1[1]:.0f} {b2[0]:.0f},{b2[1]:.0f} {tip[0]:.0f},{tip[1]:.0f} "
           f"C{b3[0]:.0f},{b3[1]:.0f} {b4[0]:.0f},{b4[1]:.0f} {cx:.0f},{cy:.0f} Z",
           label, fill=fill, stroke=INK, strokeWidth=4, opacity=op)
    d.path(f"M{cx+ux*4:.0f},{cy+uy*4:.0f} L{cx+ux*ln*0.88:.0f},{cy+uy*ln*0.88:.0f}",
           f"{label} vein", fill=NONE, stroke="#3E6E2C", strokeWidth=2.5,
           opacity=60, cap="round")

def leg(label, root, knee, tip):
    rx, ry = root; kx, ky = knee
    tx, ty = clamp(*tip)
    # femur: thin round section root -> knee
    d.path(f"M{rx},{ry} L{kx},{ky}", f"{label} femur", fill=NONE,
           stroke=INK, strokeWidth=8, cap="round")
    d.path(f"M{rx},{ry} L{kx},{ky}", f"{label} femur fill", fill=NONE,
           stroke=LEG_GRAD, strokeWidth=5, cap="round")
    # tibia: flattened leaflet from knee toward the tip
    ang = math.degrees(math.atan2(ty - ky, tx - kx))
    leaflet(f"{label} tibia", kx, ky, math.hypot(tx-kx, ty-ky)*0.72, 46, ang)
    # tarsus: thin tip segment + foot dot
    d.path(f"M{kx + (tx-kx)*0.55:.0f},{ky + (ty-ky)*0.55:.0f} L{tx:.0f},{ty:.0f}",
           f"{label} tarsus", fill=NONE, stroke=INK, strokeWidth=4, cap="round")
    d.shape("ellipse", f"{label} foot", x=tx-5, y=ty-4, width=10, height=8,
            fill=INK, stroke=NONE)

# far-side legs first (darker, behind the lamina edge)
leg("Foreleg far",  (474,300), (392,236), (330,176))
leg("Midleg far",   (368,452), (268,430), (196,432))
leg("Hindleg far",  (412,610), (330,700), (292,792))

# --- lamina: the leaf body, nibbled edge ------------------------------------------
# right edge top->tip with two bite notches, left tip->top with two more
right = [(500,252),(566,262),(616,300),(650,352),(662,404),
         (642,412),(656,448),(664,498),(658,548),
         (632,556),(640,596),(612,652),(566,700),(500,746)]
left  = [(500,746),(438,712),(390,666),(360,612),
         (378,604),(352,560),(340,508),(342,458),
         (360,450),(348,410),(358,356),(392,300),(440,264),(500,252)]
loop = right[:-1] + left[:-1]
d.path(smooth_path(loop, close=True), "Lamina", fill=LAMINA_GRAD,
       stroke=INK, strokeWidth=6)
# lamina shading: translucent shade down the right flank, glow upper-left
d.path("M540,300 C620,380 646,500 590,640", "Flank shade", fill=NONE,
       stroke="#2E5A22", strokeWidth=26, opacity=18, cap="round")
d.shape("ellipse", "Lamina glow", x=380, y=330, width=180, height=150,
        fill="#E2F4AC", opacity=18, stroke=NONE)
# brown edge-rot at the bite notches + one margin spot
for i, (x, y, w, h) in enumerate([(636,398,30,22),(618,544,26,20),(352,436,26,18)]):
    d.shape("ellipse", f"Edge rot {i+1}", x=x, y=y, width=w, height=h,
            fill="#8A6B38", opacity=55, stroke="#5E4A26", strokeWidth=3)
# midrib + lateral veins, lighter line work
d.path("M500,258 C496,380 496,560 500,738", "Midrib", fill=NONE,
       stroke="#C9E89A", strokeWidth=5, opacity=85, cap="round")
for i, y in enumerate([310, 366, 424, 484, 546, 606, 660, 706]):
    t = (y - 252) / (746 - 252)
    reach = 150 * math.sin(math.pi * (0.18 + t*0.78)) + 20
    for s in (1, -1):
        d.path(f"M498,{y} C{498 + s*reach*0.5:.0f},{y + 14} {498 + s*reach*0.85:.0f},{y + 40} "
               f"{498 + s*reach:.0f},{y + 66}",
               f"Vein {i+1}{'r' if s>0 else 'l'}", fill=NONE,
               stroke="#B8DE8C", strokeWidth=3.5, opacity=60, cap="round")
# dewdrops on the lamina
for i, (x, y, w) in enumerate([(430,420,16),(556,520,13),(478,610,11)]):
    d.shape("ellipse", f"Dew {i+1}", x=x, y=y, width=w, height=w*0.9,
            fill="#FFFFFF", opacity=28, stroke="#E8F6D8", strokeWidth=1.5)
    d.shape("ellipse", f"Dew glint {i+1}", x=x+3, y=y+3, width=w*0.3, height=w*0.28,
            fill="#FFFFFF", opacity=70, stroke=NONE)

# --- thorax collar: a small leaf segment above the lamina --------------------------
leaflet("Thorax", 500, 296, 84, 72, -90)
# --- head + antennae ---------------------------------------------------------------
d.path("M478,262 C468,238 472,214 492,204 C512,196 532,206 534,228 "
       "C536,248 526,264 508,268 C494,270 482,270 478,262 Z",
       "Head", fill=LOBE_GRAD, stroke=INK, strokeWidth=5)
d.shape("ellipse", "Eye L", x=486, y=228, width=10, height=12, fill="#101A0C", stroke=NONE)
d.shape("ellipse", "Eye R", x=510, y=228, width=10, height=12, fill="#101A0C", stroke=NONE)
d.shape("ellipse", "Eye glint L", x=488, y=230, width=4, height=4, fill="#FFFFFF", opacity=85, stroke=NONE)
d.shape("ellipse", "Eye glint R", x=512, y=230, width=4, height=4, fill="#FFFFFF", opacity=85, stroke=NONE)
d.path("M488,214 C470,196 452,186 430,182", "Antenna L", fill=NONE,
       stroke=INK, strokeWidth=3.5, cap="round")
d.path("M516,212 C534,192 552,182 574,178", "Antenna R", fill=NONE,
       stroke=INK, strokeWidth=3.5, cap="round")

# --- near-side legs, over the lamina edge --------------------------------------------
leg("Foreleg near", (524,302), (606,238), (668,178))
leg("Midleg near",  (632,452), (734,428), (806,430))
leg("Hindleg near", (588,610), (672,698), (712,790))

# --- name ---------------------------------------------------------------------------
d.text("LEAF INSECT", "Name", x=500, y=962, size=56, font="Virelai Sans",
       color="#D2E4BC", justify="center")

d.finish("leaf-insect-V1R00")
