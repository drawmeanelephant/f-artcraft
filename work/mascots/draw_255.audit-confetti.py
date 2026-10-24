#!/usr/bin/env python3
"""Audit Confetti — mascot portrait V1R00.
A party-popper mascot mid-detonation, spraying shredded-spreadsheet confetti
down onto a basement server rack, paper drifting deepest over the exhaust fan.
It is detonated, not deployed; cleanup remains a separate jurisdiction.
1000x1000. Gradients + translucent shading, never flat fills."""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Audit Confetti — Mascot Portrait", 1000, 1000)

INK = "#40302C"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#0C1E22"}, {"offset": 1, "color": "#050D10"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#41586A"}, {"offset": 0.7, "color": "#283945"},
    {"offset": 1, "color": "#14202A"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#26343E"}, {"offset": 1, "color": "#101A20"}]}}
RACK_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3A4756"}, {"offset": 1, "color": "#1C2630"}]}}
BAY_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#232E3A"}, {"offset": 1, "color": "#141C24"}]}}
CONE_ROSE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E8B4BC"}, {"offset": 1, "color": "#C07884"}]}}
CONE_CREAM = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F2E8CC"}, {"offset": 1, "color": "#D8C498"}]}}
GOLD_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E8C878"}, {"offset": 1, "color": "#B8924A"}]}}
PAPER = ["#A8C8A0", "#E8A0B0", "#E8D08A", "#90B8C8", "#EFE8D8", "#C8A8C8"]

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#6E8894", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C8DCE0", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(193,233,8),(801,230,7),(157,524,9),(837,544,8),
                               (247,766,7),(753,749,9),(133,393,6),(864,391,7),
                               (391,113,7),(613,110,8),(333,823,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#3E5A68", opacity=45, stroke=NONE)

# --- floor: bottom segment closed on the disc's own arc ------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0A1418",
       strokeWidth=4, opacity=70)

# --- distant second rack, mostly silhouette -------------------------------------
d.shape("rectangle", "Far rack", x=190, y=470, width=120, height=250,
        fill="#1E2A34", stroke=NONE, radius=8, opacity=65)
for j, ry in enumerate([495, 545, 595, 645]):
    d.shape("ellipse", f"Far LED {j+1}", x=205, y=ry, width=7, height=7,
            fill="#7EC88A" if j != 2 else "#E8B04A", opacity=40, stroke=NONE)

# --- the server rack --------------------------------------------------------------
d.shape("ellipse", "Rack shadow", x=545, y=712, width=230, height=26,
        fill="#060D10", opacity=50, stroke=NONE)
d.shape("rectangle", "Rack", x=560, y=385, width=175, height=335,
        fill=RACK_GRAD, stroke=INK, strokeWidth=6, radius=10)
d.path("M575,392 L575,715", "Rack spine", fill=NONE, stroke="#0E161C",
       strokeWidth=3, opacity=60)
d.text("EVIDENCE", "Rack spine label", x=588, y=503, size=11,
       font="Virelai Sans", color="#6E8494", justify="left")

# exhaust fan, top bay — the vent the paper seeks
d.shape("ellipse", "Fan rim", x=610, y=408, width=84, height=84,
        fill="#141E26", stroke=INK, strokeWidth=4)
for i in range(6):
    a = math.radians(i * 60 + 14)
    x1, y1 = 652 + 12*math.cos(a), 450 + 12*math.sin(a)
    x2, y2 = 652 + 36*math.cos(a), 450 + 36*math.sin(a)
    d.path(f"M{x1:.0f},{y1:.0f} L{x2:.0f},{y2:.0f}", f"Fan spoke {i+1}",
           fill=NONE, stroke="#4A5E6C", strokeWidth=5, cap="round")
d.shape("ellipse", "Fan hub", x=641, y=439, width=22, height=22,
        fill="#2E3E4A", stroke=INK, strokeWidth=3)
# paper strips sucked flat against the grille
for i, (cx, cy, w, h, rot, c) in enumerate([
        (628, 418, 34, 13, -30, "#E8A0B0"), (664, 424, 30, 12, 25, "#EFE8D8"),
        (640, 452, 36, 14, -8, "#A8C8A0"), (672, 462, 28, 11, 55, "#E8D08A"),
        (622, 470, 26, 11, -55, "#90B8C8")]):
    d.path(rot_rect_path(cx, cy, w, h, rot), f"Fan clog {i+1}",
           fill=c, stroke=INK, strokeWidth=2, opacity=95)
# warm air shimmer escaping around the clog
for i, (x0, h) in enumerate([(700, 60), (716, 44)]):
    d.path(f"M{x0},{452} C{x0+8},{452-18} {x0-6},{452-30} {x0+6},{452-h}",
           f"Shimmer {i+1}", fill=NONE, stroke="#C8DCE0", strokeWidth=3,
           cap="round", opacity=14)

# lower bays: vent slits + status LEDs
for j, by in enumerate([512, 572, 632]):
    d.shape("rectangle", f"Bay {j+1}", x=575, y=by, width=145, height=44,
            fill=BAY_GRAD, stroke=INK, strokeWidth=3.5, radius=6)
    for k in range(3):
        d.shape("rectangle", f"Bay {j+1} slit {k+1}", x=588, y=by+9+k*11,
                width=92, height=6, fill="#0C141A", stroke=NONE, radius=3)
    for k, c in enumerate(["#7EC88A", "#E8B04A"]):
        d.shape("ellipse", f"Bay {j+1} LED {k+1}", x=692+k*14, y=by+16,
                width=8, height=8, fill=c, stroke=NONE, opacity=90)
        d.shape("ellipse", f"Bay {j+1} LED glow {k+1}", x=690+k*14, y=by+14,
                width=12, height=12, fill=c, opacity=15, stroke=NONE)
# one fault light, low
d.shape("ellipse", "Fault LED", x=692, y=676, width=8, height=8,
        fill="#E06A5A", stroke=NONE, opacity=90)
d.shape("rectangle", "Low slit", x=588, y=672, width=92, height=6,
        fill="#0C141A", stroke=NONE, radius=3)

# confetti heaped on the rack's top edge, sliding off
for i, (cx, cy, w, h, rot, c) in enumerate([
        (600, 378, 30, 12, -12, "#E8A0B0"), (645, 372, 34, 13, 8, "#EFE8D8"),
        (688, 380, 28, 12, -20, "#A8C8A0"), (720, 390, 24, 11, 40, "#E8D08A"),
        (570, 386, 26, 11, 15, "#90B8C8"), (625, 384, 22, 10, -45, "#C8A8C8")]):
    d.path(rot_rect_path(cx, cy, w, h, rot), f"Rack-top drift {i+1}",
           fill=c, stroke=INK, strokeWidth=1.5, opacity=95)

# --- floor drift: the pile the janitorial ticket will find -------------------------
for i, (cx, cy, w, h, rot, c) in enumerate([
        (560, 726, 40, 14, 5, "#EFE8D8"), (610, 736, 44, 15, -8, "#E8A0B0"),
        (665, 730, 38, 13, 12, "#A8C8A0"), (715, 742, 34, 12, -18, "#E8D08A"),
        (520, 742, 30, 12, 20, "#90B8C8"), (755, 732, 26, 11, 30, "#EFE8D8"),
        (590, 752, 36, 13, -25, "#C8A8C8"), (650, 756, 40, 14, 10, "#E8D08A"),
        (480, 730, 26, 11, -35, "#E8A0B0"), (450, 748, 30, 12, 15, "#A8C8A0")]):
    d.path(rot_rect_path(cx, cy, w, h, rot), f"Floor drift {i+1}",
           fill=c, stroke=INK, strokeWidth=1.5, opacity=95)

# --- the confetti fall: deterministic scatter along the burst arc -------------------
rng = random.Random(255)
def confetti(cx, cy, idx, scale=1.0, op=95):
    w, h = rng.choice([(26, 11), (22, 9), (30, 12), (18, 8)])
    rot = rng.uniform(-70, 70)
    c = PAPER[idx % len(PAPER)]
    d.path(rot_rect_path(cx, cy, w*scale, h*scale, rot), f"Confetti {idx}",
           fill=c, stroke=INK, strokeWidth=1.5, opacity=op)
    # shred ticks: faint cell lines on the wider strips
    if w >= 26:
        t = math.radians(rot)
        mx, my = -math.sin(t), math.cos(t)
        d.path(f"M{cx-mx*h*scale*0.4:.0f},{cy+my*h*scale*0.4:.0f} "
               f"L{cx+mx*h*scale*0.4:.0f},{cy-my*h*scale*0.4:.0f}",
               f"Cell tick {idx}", fill=NONE, stroke=INK, strokeWidth=1,
               opacity=35)

# burst arc: mouth (400,338) -> peak -> rack
idx = 0
for t in [i/22 for i in range(23)]:
    bx = (1-t)**2*400 + 2*(1-t)*t*560 + t*t*700
    by = (1-t)**2*330 + 2*(1-t)*t*250 + t*t*560
    confetti(bx + rng.uniform(-26, 26), by + rng.uniform(-24, 24), idx,
             scale=1.05 - t*0.25)
    idx += 1
# strays drifting wide
for (sx, sy) in [(300,470),(350,560),(255,560),(420,640),(370,700),(500,600),
                 (470,720),(560,540),(740,500),(770,580),(530,430),(610,320),
                 (660,270),(560,230),(700,420),(300,620),(240,680),(510,370)]:
    confetti(sx + rng.uniform(-14, 14), sy + rng.uniform(-14, 14), idx,
             scale=0.9, op=88)
    idx += 1
# two curled ribbon spirals
d.path("M470,400 C510,390 530,410 518,432 C508,448 488,446 486,430 "
       "C484,416 498,410 508,418", "Ribbon curl 1", fill=NONE,
       stroke="#E8A0B0", strokeWidth=6, cap="round", opacity=90)

# --- a checked-off fragment, mid-air: the record it was -------------------------
d.path(rot_rect_path(505, 190, 96, 72, 12), "Sheet fragment",
       fill="#EFE8D8", stroke=INK, strokeWidth=3, opacity=95)
for k in range(3):
    y0 = 168 + k*16
    d.path(f"M478,{y0} L494,{y0} M502,{y0} L528,{y0}",
           f"Frag row {k+1}", fill=NONE, stroke="#8A7A60", strokeWidth=2.5,
           opacity=70)
    d.path(f"M462,{y0-3} L465,{y0} L471,{y0-6}", f"Frag tick {k+1}",
           fill=NONE, stroke="#5A8A60", strokeWidth=2.5, cap="round")

# --- the mascot: a party popper, detonated -----------------------------------------
# soft halo behind the cone
d.shape("ellipse", "Popper halo", x=210, y=185, width=220, height=200,
        fill="#E8D08A", opacity=10, stroke=NONE)
# cone: apex P, mouth centre C; bands along the axis, then outline, then rim
P = (250, 222); C = (375, 345)
vx, vy = C[0]-P[0], C[1]-P[1]
L = math.hypot(vx, vy); ux, uy = vx/L, vy/L
nx, ny = -uy, ux
HW = 58
M1 = (C[0]-nx*HW, C[1]-ny*HW)
M2 = (C[0]+nx*HW, C[1]+ny*HW)
def edge(t, side):
    mx, my = M1 if side == 1 else M2
    return (P[0] + (mx-P[0])*t, P[1] + (my-P[1])*t)
for i, (ta, tb, fill) in enumerate([(0.0, 0.30, CONE_ROSE),
                                    (0.30, 0.48, CONE_CREAM),
                                    (0.48, 0.62, CONE_ROSE),
                                    (0.62, 0.80, CONE_CREAM),
                                    (0.80, 1.03, CONE_ROSE)]):
    a1, a2 = edge(ta, 1), edge(ta, 2)
    b1, b2 = edge(tb, 1), edge(tb, 2)
    d.path(f"M{a1[0]:.0f},{a1[1]:.0f} L{a2[0]:.0f},{a2[1]:.0f} "
           f"L{b2[0]:.0f},{b2[1]:.0f} L{b1[0]:.0f},{b1[1]:.0f} Z",
           f"Cone band {i+1}", fill=fill, stroke=NONE)
# cone sheen + outline
midx, midy = P[0]+vx*0.45, P[1]+vy*0.45
d.shape("ellipse", "Cone sheen", x=midx-52, y=midy-40, width=70, height=26,
        fill="#FFFFFF", opacity=18, stroke=NONE)
bulge = (C[0]+ux*26, C[1]+uy*26)
d.path(f"M{P[0]},{P[1]} L{M1[0]:.0f},{M1[1]:.0f} "
       f"Q{bulge[0]:.0f},{bulge[1]:.0f} {M2[0]:.0f},{M2[1]:.0f} Z",
       "Cone outline", fill=NONE, stroke=INK, strokeWidth=6, join="round")
# mouth: crimped gold rim + dark maw where the burst leaves
d.path(f"M{M1[0]:.0f},{M1[1]:.0f} Q{bulge[0]:.0f},{bulge[1]:.0f} "
       f"{M2[0]:.0f},{M2[1]:.0f}", "Mouth rim", fill=NONE, stroke=GOLD_GRAD,
       strokeWidth=12, cap="round")
mcx, mcy = (M1[0]+M2[0])/2, (M1[1]+M2[1])/2
q1 = (mcx + (M1[0]-mcx)*0.55 + ux*2, mcy + (M1[1]-mcy)*0.55 + uy*2)
q2 = (mcx + (M2[0]-mcx)*0.55 + ux*2, mcy + (M2[1]-mcy)*0.55 + uy*2)
d.path(f"M{q1[0]:.0f},{q1[1]:.0f} "
       f"Q{mcx+ux*22:.0f},{mcy+uy*22:.0f} {q2[0]:.0f},{q2[1]:.0f} "
       f"Q{mcx+ux*4:.0f},{mcy+uy*4:.0f} {q1[0]:.0f},{q1[1]:.0f} Z",
       "Maw", fill="#241418", stroke=NONE, opacity=75)
# apex pull-stub + ring
d.path(f"M{P[0]-4},{P[1]-4} L{P[0]-18},{P[1]-18}", "Pull stub", fill=NONE,
       stroke=INK, strokeWidth=6, cap="round")
d.shape("ellipse", "Pull ring", x=P[0]-30, y=P[1]-30, width=15, height=15,
        fill=NONE, stroke=GOLD_GRAD, strokeWidth=4)
# gleeful face on the cone body, screen-upright
fx, fy = P[0]+vx*0.50, P[1]+vy*0.50
d.path(f"M{fx-30},{fy-16} C{fx-24},{fy-24} {fx-14},{fy-24} {fx-8},{fy-16}",
       "Eye L", fill=NONE, stroke=INK, strokeWidth=4.5, cap="round")
d.path(f"M{fx+8},{fy-16} C{fx+14},{fy-24} {fx+24},{fy-24} {fx+30},{fy-16}",
       "Eye R", fill=NONE, stroke=INK, strokeWidth=4.5, cap="round")
d.path(f"M{fx-14},{fy-2} C{fx-4},{fy+12} {fx+10},{fy+12} {fx+18},{fy-2}",
       "Grin", fill=NONE, stroke=INK, strokeWidth=4.5, cap="round")
d.shape("ellipse", "Cheek L", x=fx-42, y=fy-6, width=18, height=10,
        fill="#C0485C", opacity=40, stroke=NONE)
d.shape("ellipse", "Cheek R", x=fx+28, y=fy-6, width=18, height=10,
        fill="#C0485C", opacity=40, stroke=NONE)
# stubby arms, thrown up by the detonation
d.path(f"M{fx-46},{fy+18} C{fx-64},{fy+8} {fx-72},{fy-8} {fx-74},{fy-24}",
       "Arm L", fill=NONE, stroke=INK, strokeWidth=7, cap="round")
d.path(f"M{fx+42},{fy+22} C{fx+60},{fy+30} {fx+74},{fy+28} {fx+84},{fy+18}",
       "Arm R", fill=NONE, stroke=INK, strokeWidth=7, cap="round")
# burst ticks at the mouth
for i, (dx, dy) in enumerate([(30,-4),(16,34),(52,20)]):
    bx0, by0 = bulge[0]+dx, bulge[1]+dy
    d.path(f"M{bx0:.0f},{by0:.0f} L{bx0+dx*0.7:.0f},{by0+dy*0.7:.0f}",
           f"Burst tick {i+1}", fill=NONE, stroke="#E8D08A", strokeWidth=5,
           cap="round", opacity=85)

# --- captions ----------------------------------------------------------------------
d.text("AUDIT CONFETTI", "Name", x=500, y=930, size=56, font="Virelai Sans",
       color="#E4ECEA", justify="center")
r = d.text("DECORATIVE CLOSURE", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#9AB8B4", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("255.audit-confetti-V1R00")
