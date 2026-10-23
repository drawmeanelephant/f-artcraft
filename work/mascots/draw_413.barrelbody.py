#!/usr/bin/env python3
"""Barrelbody — mascot portrait V1R00.
Barrel-bodied mascot wedged too wide in a gate, wreckage of three mail
servers behind. 1000x1000. Gradients + translucency, never flat."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Barrelbody — Mascot Portrait", 1000, 1000)

INK = "#2E2A30"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#121A22"}, {"offset": 1, "color": "#060A0E"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#7E94A8"}, {"offset": 0.7, "color": "#526A82"},
    {"offset": 1, "color": "#2F3F52"}]}}
WOOD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#D9A868"}, {"offset": 0.7, "color": "#A87844"},
    {"offset": 1, "color": "#6E4A28"}]}}
METAL = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7C8698"}, {"offset": 1, "color": "#4A5264"}]}}
SERVER = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7A8494"}, {"offset": 1, "color": "#49505E"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#6E869C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D4E2EE", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(205,230,8),(792,236,7),(170,536,9),(822,558,8),
                               (255,750,7),(745,744,9),(145,396,6),(852,408,7),
                               (398,116,7),(602,114,8),(340,812,6),(660,810,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#42546A", opacity=45, stroke=NONE)

# --- wreckage: three dead mail servers ----------------------------------------
def server(x, y, w, h, tilt, label):
    # tilted box via rot_rect-ish path
    import math
    t = math.radians(tilt); c, s = math.cos(t), math.sin(t)
    def rot(px, py):
        return (x + px*c - py*s, y + px*s + py*c)
    pts = [rot(-w/2,-h/2), rot(w/2,-h/2), rot(w/2,h/2), rot(-w/2,h/2)]
    dd = "M" + " L".join(f"{p[0]:.0f},{p[1]:.0f}" for p in pts) + " Z"
    d.path(dd, label, fill=SERVER, stroke=INK, strokeWidth=5, join="round")
    for i in range(3):
        a = rot(-w/2+14, -h/2+16+i*16); b = rot(w/2-14, -h/2+16+i*16)
        d.path(f"M{a[0]:.0f},{a[1]:.0f} L{b[0]:.0f},{b[1]:.0f}",
               f"{label} vent {i+1}", fill=NONE, stroke="#39404C",
               strokeWidth=4, cap="round", opacity=80)
    for i in range(3):
        p = rot(-w/2+16+i*14, h/2-14)
        d.shape("ellipse", f"{label} led {i+1}", x=p[0]-4, y=p[1]-4,
                width=8, height=8, fill="#8E2E28", stroke=NONE)

server(300, 690, 150, 96, -9, "Server L")
server(700, 700, 150, 96, 8, "Server R")
server(640, 396, 120, 76, 14, "Server toppled")
# spilled envelopes
for i, (x, y, t) in enumerate([(255,760,-8),(355,748,6),(700,762,-12),(780,730,10)]):
    import math
    th = math.radians(t); c, s = math.cos(th), math.sin(th)
    pts = []
    for dx, dy in [(-26,-16),(26,-16),(26,16),(-26,16)]:
        pts.append((x+dx*c-dy*s, y+dx*s+dy*c))
    dd = "M" + " L".join(f"{p[0]:.0f},{p[1]:.0f}" for p in pts) + " Z"
    d.path(dd, f"Envelope {i+1}", fill="#E4DCC4", stroke=INK, strokeWidth=3)
    d.path(f"M{pts[0][0]:.0f},{pts[0][1]:.0f} L{x:.0f},{y+6:.0f} "
           f"L{pts[1][0]:.0f},{pts[1][1]:.0f}", f"Envelope flap {i+1}",
           fill=NONE, stroke=INK, strokeWidth=2, opacity=70)
# a crack + spark on the toppled server
d.path("M620,380 L640,398 L628,414", "Crack", fill=NONE, stroke=INK,
       strokeWidth=3, opacity=80)
d.shape("star", "Spark", cx=668, cy=362, radius1=12, radius2=4, points=4,
        fill="#F2CE5E", stroke=NONE, opacity=85)

# --- the gate the barrel can't pass --------------------------------------------
d.shape("rectangle", "Post L", x=352, y=330, width=34, height=400,
        fill=METAL, stroke=INK, strokeWidth=5, radius=6)
d.shape("rectangle", "Post R", x=614, y=330, width=34, height=400,
        fill=METAL, stroke=INK, strokeWidth=5, radius=6)
d.shape("rectangle", "Lintel", x=336, y=300, width=328, height=34,
        fill=METAL, stroke=INK, strokeWidth=5, radius=6)
# clearance marks on the posts
d.path("M352,380 L336,380 M352,410 L336,410", "Clear marks L", fill=NONE,
       stroke="#D4E2EE", strokeWidth=4, opacity=60)
d.path("M648,380 L664,380 M648,410 L664,410", "Clear marks R", fill=NONE,
       stroke="#D4E2EE", strokeWidth=4, opacity=60)
# ground shadow
d.shape("ellipse", "Ground shadow", x=290, y=722, width=420, height=46,
        fill="#202C3C", opacity=55, stroke=NONE)

# --- the barrel mascot, wedged -------------------------------------------------
d.path("M500,352 C412,352 348,430 348,540 C348,650 412,730 500,730 "
       "C588,730 652,650 652,540 C652,430 588,352 500,352 Z",
       "Barrel", fill=WOOD, stroke=INK, strokeWidth=8)
# staves
for i, (x0, x1) in enumerate([(412,420),(458,462),(542,538),(588,580)]):
    d.path(f"M{x0},380 C{x0-18},470 {x0-18},610 {x0},700" if x0 < 500 else
           f"M{x0},380 C{x0+18},470 {x0+18},610 {x0},700",
           f"Stave {i+1}", fill=NONE, stroke="#7A5230", strokeWidth=4,
           opacity=70)
# hoops
d.path("M352,470 C430,492 570,492 648,470 L648,494 C570,516 430,516 352,494 Z",
       "Hoop top", fill=METAL, stroke=INK, strokeWidth=5, join="round")
d.path("M352,600 C430,622 570,622 648,600 L648,624 C570,646 430,646 352,624 Z",
       "Hoop bottom", fill=METAL, stroke=INK, strokeWidth=5, join="round")
# highlight + lower shade
d.shape("ellipse", "Barrel highlight", x=400, y=380, width=140, height=60,
        fill="#FFFFFF", opacity=18, stroke=NONE)
d.path("M380,672 C440,706 560,706 620,672 C560,692 440,692 380,672 Z",
       "Barrel shade", fill="#5E3E24", opacity=40, stroke=NONE)
# squeeze arcs where the barrel presses the posts
d.path("M352,520 C342,545 342,575 352,600", "Squeeze L", fill=NONE,
       stroke=INK, strokeWidth=4, opacity=55)
d.path("M648,520 C658,545 658,575 648,600", "Squeeze R", fill=NONE,
       stroke=INK, strokeWidth=4, opacity=55)
# face: gritted grimace between the hoops
d.path("M428,540 C436,548 450,548 458,540", "Eye L squeeze", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
d.path("M542,540 C550,548 564,548 572,540", "Eye R squeeze", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
d.path("M440,522 L468,516 M560,516 L588,522", "Strain brows", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
# gritted teeth: rect with ticks
d.path("M455,568 L545,568 L545,592 L455,592 Z", "Grimace", fill="#F0E2C4",
       stroke=INK, strokeWidth=5, join="round")
for i, x in enumerate([473, 491, 509, 527]):
    d.path(f"M{x},568 L{x},592", f"Tooth {i+1}", fill=NONE, stroke=INK,
           strokeWidth=3)
d.path("M455,580 L545,580", "Tooth line", fill=NONE, stroke=INK, strokeWidth=3)
# sweat bead
d.path("M620,500 C612,516 610,526 620,532 C630,526 628,516 620,500 Z",
       "Sweat", fill="#BEE2EA", stroke=INK, strokeWidth=3, opacity=90)
# arms akimbo: hands braced on the posts
d.path("M370,545 C352,520 350,495 358,472", "Arm L", fill=NONE, stroke=WOOD,
       strokeWidth=20, cap="round")
d.shape("ellipse", "Hand L", x=346, y=452, width=30, height=34, fill=WOOD,
        stroke=INK, strokeWidth=5)
d.path("M630,545 C648,520 650,495 642,472", "Arm R", fill=NONE, stroke=WOOD,
       strokeWidth=20, cap="round")
d.shape("ellipse", "Hand R", x=624, y=452, width=30, height=34, fill=WOOD,
        stroke=INK, strokeWidth=5)
# feet straining under the barrel
d.shape("ellipse", "Foot L", x=438, y=722, width=50, height=30, fill="#5E4630",
        stroke=INK, strokeWidth=5)
d.shape("ellipse", "Foot R", x=512, y=722, width=50, height=30, fill="#5E4630",
        stroke=INK, strokeWidth=5)

# --- captions ------------------------------------------------------------------
d.text("BARRELBODY", "Name", x=500, y=930, size=56, font="Virelai Sans",
       color="#D4E2EE", justify="center")
r = d.text("TOO WIDE FOR THE GATE", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#98ACC0", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("413.barrelbody-V1R00")
