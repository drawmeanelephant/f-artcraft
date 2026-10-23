#!/usr/bin/env python3
"""Echidna — field-guide plate V1R00. Three-quarter body shot facing left so
the spines read: a dome of cream quills with umber tips (each quill its own
base-to-tip gradient) over rust fur, long probing snout nosing an ant trail,
digging claws, hind feet turned backward. Dusty outback dusk with a termite
mound; the ground band closes on the disc's own arc.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Echidna — Field Plate", 1000, 1000)
rng = random.Random(21)   # fixed seed: the quill jitter is the same every run

INK = "#2E1A10"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3A1E16"}, {"offset": 1, "color": "#120806"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#FCE8C4"}, {"offset": 0.6, "color": "#EDB980"},
    {"offset": 1, "color": "#B86A44"}]}}
GROUND_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#B4583A"}, {"offset": 1, "color": "#6E2E1E"}]}}
MOUND_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#D08A5C"}, {"offset": 1, "color": "#9A4E32"}]}}
FUR_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#B8683E"}, {"offset": 0.7, "color": "#8A4426"},
    {"offset": 1, "color": "#5A2A16"}]}}
HEAD_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#C27448"}, {"offset": 1, "color": "#7E3E22"}]}}
SNOUT_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5E4436"}, {"offset": 1, "color": "#33231A"}]}}
LEG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7E3E22"}, {"offset": 1, "color": "#4A2414"}]}}
LEG_FAR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5E2E1A"}, {"offset": 1, "color": "#3A1C10"}]}}
CLAW_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E8D8C0"}, {"offset": 1, "color": "#8A7660"}]}}

GROUND_Y = 712
CX, CY, R = 500, 460, 420
def disc_x(y):
    return math.sqrt(R*R - (y - CY)**2)

# --- backdrop + plate ---------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#7A3A24", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#FFF2DC", strokeWidth=3, opacity=50)
d.shape("ellipse", "Sun glow", x=170, y=150, width=280, height=280, fill="#FFF0D0", opacity=30, stroke=NONE)
d.shape("ellipse", "Sun", x=240, y=220, width=140, height=140, fill="#FFF6E2", opacity=60, stroke=NONE)
d.shape("ellipse", "Dust haze", x=520, y=200, width=280, height=110, fill="#FFE4C0", opacity=18, stroke=NONE)
for i, (x, y, w) in enumerate([(780,260,6),(820,420,7),(150,440,6),(420,110,6),(620,110,7),
                               (700,190,5),(330,150,5),(860,520,5),(140,540,5),(560,140,4)]):
    d.shape("ellipse", f"Dust fleck {i+1}", x=x, y=y, width=w, height=w, fill="#B0623E", opacity=35, stroke=NONE)

# distant mesas on the horizon, faint (they sit on the ground line, inside the disc)
d.path("M176,712 L186,690 L214,684 L226,664 L296,660 L310,684 L344,690 L352,712 Z",
       "Mesa left", fill="#A65A3E", opacity=34, stroke=NONE)
d.path("M640,712 L652,694 L700,690 L712,670 L790,666 L804,690 L826,694 L830,712 Z",
       "Mesa right", fill="#A65A3E", opacity=34, stroke=NONE)
d.path("M226,664 L296,660", "Mesa left rim light", fill=NONE, stroke="#FFE2C0", strokeWidth=3, opacity=40, cap="round")
d.path("M712,670 L790,666", "Mesa right rim light", fill=NONE, stroke="#FFE2C0", strokeWidth=3, opacity=40, cap="round")
for i, x in enumerate([206, 812]):
    for j, (dx, h, lean) in enumerate([(-8, 30, -16), (-3, 42, -6), (2, 46, 4), (7, 36, 14), (11, 26, 22)]):
        d.path(f"M{x+dx},{GROUND_Y} Q{x+dx+lean*0.3},{GROUND_Y-h*0.6} {x+dx+lean},{GROUND_Y-h}",
               f"Spinifex {i+1}.{j+1}", fill=NONE, stroke="#8A8A4A", strokeWidth=3, opacity=75, cap="round")

# ground band: top edge across, bottom closes on the disc arc
xl, xr = CX - disc_x(GROUND_Y), CX + disc_x(GROUND_Y)
d.path(f"M{xl:.1f},{GROUND_Y} C{xl + 160:.1f},{GROUND_Y - 8} {xr - 160:.1f},{GROUND_Y - 8} {xr:.1f},{GROUND_Y} "
       f"A{R},{R} 0 0 1 {xl:.1f},{GROUND_Y} Z", "Ground", fill=GROUND_GRAD, opacity=92, stroke=NONE)
d.path(f"M{xl + 20:.1f},{GROUND_Y + 2} C{xl + 180:.1f},{GROUND_Y - 5} {xr - 180:.1f},{GROUND_Y - 5} {xr - 20:.1f},{GROUND_Y + 2}",
       "Ground rim light", fill=NONE, stroke="#FFD2A8", strokeWidth=3, opacity=40, cap="round")
for i, (x, y, w, h) in enumerate([(250,760,18,9),(560,790,14,7),(690,750,20,10),(410,820,12,6),(330,742,10,5),(620,840,16,7)]):
    d.shape("ellipse", f"Pebble {i+1}", x=x, y=y, width=w, height=h, fill="#E2A27A", opacity=55, stroke=NONE)
d.shape("ellipse", "Echidna shadow", x=280, y=704, width=520, height=30, fill="#3A140A", opacity=35, stroke=NONE)

# ant trail toward the snout tip
for i, t in enumerate([0.0, 0.14, 0.28, 0.42, 0.56, 0.7, 0.84, 1.0]):
    x = 236 + t*140
    y = 744 + math.sin(t*math.pi*2)*8 + t*24
    d.shape("ellipse", f"Ant {i+1} body", x=round(x), y=round(y), width=9, height=5, fill="#2A1008", opacity=85, stroke=NONE)
    d.shape("ellipse", f"Ant {i+1} head", x=round(x - 4), y=round(y), width=5, height=5, fill="#2A1008", opacity=85, stroke=NONE)

# --- far legs (behind the body) ----------------------------------------------------------
d.path("M458,650 C450,676 444,694 440,710 L476,712 C478,692 484,672 492,652 Z",
       "Leg far front", fill=LEG_FAR_GRAD, stroke=INK, strokeWidth=3)
d.path("M640,640 C646,668 650,690 652,708 L686,708 C682,686 676,664 670,640 Z",
       "Leg far hind", fill=LEG_FAR_GRAD, stroke=INK, strokeWidth=3)

# --- body: rust fur dome -------------------------------------------------------------------
d.path("M334,620 C338,512 420,428 540,416 C664,406 764,476 784,566 "
       "C800,640 774,698 722,712 C620,698 492,698 392,712 C350,700 332,664 334,620 Z",
       "Body fur", fill=FUR_GRAD, stroke=INK, strokeWidth=6)
d.path("M372,690 C460,708 620,710 730,694", "Belly shade", fill=NONE,
       stroke="#3A1A0C", strokeWidth=14, opacity=30, cap="round")

# --- quills: computed over the dome, back-to-front so tips overlap roots --------------------
QC = (560, 664)
RX, RY = 214, 232
BACK = (0.96, -0.26)
quills = []
rows = [(1.0, 30), (0.9, 28), (0.8, 26), (0.7, 24), (0.6, 21), (0.5, 18), (0.4, 15), (0.3, 11), (0.2, 7)]
for rr, n in rows:
    a0, a1 = 194, 354
    for k in range(n):
        a = math.radians(a0 + (a1 - a0) * (k + 0.5) / n + rng.uniform(-2.5, 2.5))
        ox, oy = math.cos(a), math.sin(a)
        bx = QC[0] + RX*rr*ox + rng.uniform(-5, 5)
        by = QC[1] + RY*rr*oy + rng.uniform(-5, 5)
        if by > 664:
            continue
        w_n = 0.25 + 0.75*rr
        dx, dy = ox*w_n + BACK[0]*(1.2 - rr), oy*w_n + BACK[1]*(1.2 - rr)
        ln = math.hypot(dx, dy)
        dx, dy = dx/ln, dy/ln
        L = (40 + 24*rr) * rng.uniform(0.88, 1.1)
        W = 15 + 5*rr
        quills.append((rr, bx, by, dx, dy, L, W))
# outer rows first, then sweep back (right) to front (left) within the same depth
quills.sort(key=lambda q: (-q[0], -q[1]))
for i, (rr, bx, by, dx, dy, L, W) in enumerate(quills):
    px, py = -dy, dx
    tx, ty = bx + dx*L, by + dy*L
    dd = (f"M{bx + px*W/2:.1f},{by + py*W/2:.1f} "
          f"Q{bx + dx*L*0.55 + px*W*0.32:.1f},{by + dy*L*0.55 + py*W*0.32:.1f} {tx:.1f},{ty:.1f} "
          f"Q{bx + dx*L*0.55 - px*W*0.32:.1f},{by + dy*L*0.55 - py*W*0.32:.1f} {bx - px*W/2:.1f},{by - py*W/2:.1f} Z")
    grad = {"gradient": {"kind": "linear", "start": [round(bx), round(by)], "end": [round(tx), round(ty)],
            "stops": [{"offset": 0, "color": "#F6EAD0"}, {"offset": 0.5, "color": "#EAD6B0"},
                      {"offset": 0.62, "color": "#A8743E"}, {"offset": 1, "color": "#3A200F"}]}}
    d.path(dd, f"Quill {i+1}", fill=grad, stroke="#4A2C18", strokeWidth=1.2)
    d.path(f"M{bx + dx*L*0.08:.1f},{by + dy*L*0.08:.1f} L{bx + dx*L*0.5:.1f},{by + dy*L*0.5:.1f}",
           f"Quill {i+1} sheen", fill=NONE, stroke="#FFFFFF", strokeWidth=2, opacity=45, cap="round")
# soft dome highlight + lower shading over the quill mass
d.shape("ellipse", "Dome light", x=470, y=430, width=200, height=110, fill="#FFF4E0", opacity=16, stroke=NONE)
d.path("M360,640 C440,684 640,690 770,620 C700,672 460,676 360,640 Z",
       "Dome under-shade", fill="#3A1A0C", opacity=22, stroke=NONE)

# --- near legs: stout, splayed, digging claws (hind foot turned backward) ----------------------
def claws(label, pts):
    for k, (x0, y0, x1, y1) in enumerate(pts):
        d.path(f"M{x0},{y0} Q{(x0 + x1)/2},{min(y0, y1) - 4} {x1},{y1}", f"{label} claw {k+1}",
               fill=NONE, stroke=CLAW_GRAD, strokeWidth=6, cap="round")

d.path("M384,648 C364,664 352,686 348,704 C346,714 352,720 364,720 "
       "L404,720 C404,700 410,680 424,660 Z", "Leg near front", fill=LEG_GRAD, stroke=INK, strokeWidth=4)
claws("Front foot", [(358,712,336,718), (368,714,346,724), (380,716,360,728)])
d.path("M378,664 C368,680 362,694 360,706", "Front leg fur", fill=NONE,
       stroke="#C88058", strokeWidth=4, opacity=40, cap="round")
d.path("M676,640 C698,660 712,684 720,702 C734,704 750,710 752,720 "
       "L690,720 C686,700 674,680 656,660 Z", "Leg near hind", fill=LEG_GRAD, stroke=INK, strokeWidth=4)
claws("Hind foot", [(738,708,762,712), (744,714,768,720), (742,718,764,728)])

# --- head + long snout ----------------------------------------------------------------------
d.path("M392,560 C356,552 322,568 306,596 C294,618 276,636 248,656 "
       "C226,670 206,682 200,694 C208,702 226,700 244,694 "
       "C280,684 314,678 344,674 C376,668 398,646 400,616 Z",
       "Head", fill=HEAD_GRAD, stroke=INK, strokeWidth=5)
d.path("M310,606 C290,628 266,648 238,664 C222,674 206,684 200,694 "
       "C208,702 226,700 244,694 C268,686 292,680 318,676 C304,656 302,630 310,606 Z",
       "Snout", fill=SNOUT_GRAD, stroke=INK, strokeWidth=4)
d.path("M306,612 C288,630 264,648 236,664", "Snout sheen", fill=NONE,
       stroke="#C8A890", strokeWidth=4, opacity=45, cap="round")
d.shape("ellipse", "Snout tip", x=198, y=686, width=12, height=10, fill="#1A0E08", opacity=85, stroke=NONE)
for i, (x, y) in enumerate([(340,590),(360,610),(372,636),(344,640),(382,584)]):
    d.path(f"M{x},{y} Q{x + 6},{y + 6} {x + 8},{y + 16}", f"Head fur {i+1}", fill=NONE,
           stroke="#5A2A16", strokeWidth=4, opacity=40, cap="round")
d.path("M330,574 C350,562 374,560 392,566", "Brow light", fill=NONE,
       stroke="#F2B68A", strokeWidth=5, opacity=40, cap="round")
d.shape("ellipse", "Eye", x=330, y=600, width=14, height=12, fill="#140A06", stroke=NONE)
d.shape("ellipse", "Eye glint", x=333, y=602, width=5, height=5, fill="#FFFFFF", opacity=90, stroke=NONE)
d.path("M326,600 C332,594 342,594 348,600", "Eye lid", fill=NONE, stroke=INK, strokeWidth=3, cap="round")
# a few short quills on the crown, in front of the head edge
for i, (bx, by, ang, L) in enumerate([(382, 566, -62, 34), (396, 576, -48, 38), (370, 562, -74, 26)]):
    a = math.radians(ang)
    dx, dy = math.cos(a), math.sin(a)
    px, py = -dy, dx
    tx, ty = bx + dx*L, by + dy*L
    grad = {"gradient": {"kind": "linear", "start": [bx, by], "end": [round(tx), round(ty)],
            "stops": [{"offset": 0, "color": "#F6EAD0"}, {"offset": 0.6, "color": "#E0C8A0"},
                      {"offset": 1, "color": "#4A2C18"}]}}
    d.path(f"M{bx + px*5:.1f},{by + py*5:.1f} L{tx:.1f},{ty:.1f} L{bx - px*5:.1f},{by - py*5:.1f} Z",
           f"Crown quill {i+1}", fill=grad, stroke="#4A2C18", strokeWidth=1.5)

# --- name -------------------------------------------------------------------------------------
d.text("ECHIDNA", "Name", x=500, y=962, size=60, font="Virelai Sans",
       color="#F6DCC2", justify="center")

d.finish("echidna-V1R00")
