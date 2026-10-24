#!/usr/bin/env python3
"""boris — commemorative plate V1R00. The Content Exit Hatch: a brass
publication engine mid-cycle. Raw Markdown sheets feed in the top, a
content graph turns as an escapement wheel of nodes and edges in the
middle, and validated pages stream out through a glowing exit hatch to a
waiting fleet of targets. Graphite and engine-green; gears drawn as
graph edges between node-teeth. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("boris — Commemorative Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#171310"   # warm dark, never pure black

def on_disc(x, y, pad):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

def lin(c0, c1, start=None, end=None):
    g = {"kind": "linear", "stops": [{"offset": 0, "color": c0}, {"offset": 1, "color": c1}]}
    if start: g["start"], g["end"] = [round(v, 1) for v in start], [round(v, 1) for v in end]
    return {"gradient": g}

def rad(*stops):
    return {"gradient": {"kind": "radial", "stops": stops}}

def rrect(x0, y0, x1, y1, r):
    return (f"M{x0+r},{y0} L{x1-r},{y0} Q{x1},{y0} {x1},{y0+r} L{x1},{y1-r} "
            f"Q{x1},{y1} {x1-r},{y1} L{x0+r},{y1} Q{x0},{y1} {x0},{y1-r} "
            f"L{x0},{y0+r} Q{x0},{y0} {x0+r},{y0} Z")

GREEN = "#46D992"
BRASS = "#C8973F"
SHEET_GRAD = lin("#F0EBDC", "#CFC9B4", (0, 0), (60, 80))

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin("#12161F", "#05070C", (500, 0), (500, 1000)), stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad({"offset": 0, "color": "#313845"}, {"offset": 0.68, "color": "#1B2029"},
                 {"offset": 1, "color": "#0B0E15"}),
        stroke="#8A6428", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#5AD99E", strokeWidth=3, opacity=30)
# faint graph-web field lines inside the disc
for i, (x0, y0, x1, y1) in enumerate([(180,300,300,200),(700,180,830,300),(160,560,260,660),
                                      (720,760,820,640),(300,140,420,110)]):
    assert on_disc(x0, y0, 12) and on_disc(x1, y1, 12)
    d.path(f"M{x0},{y0} L{x1},{y1}", f"Field line {i+1}", fill=NONE,
           stroke="#3FD68F", strokeWidth=2, opacity=12, cap="round")
    d.shape("ellipse", f"Field node {i+1}", x=x1-4, y=y1-4, width=8, height=8,
            fill="#3FD68F", opacity=18, stroke=NONE)

# --- feed: raw Markdown sheets sliding down the chute --------------------------
# chute rails (brass) converging on the machine throat
d.path("M415,300 L452,368", "Chute rail L", fill=NONE, stroke=BRASS, strokeWidth=10, cap="round")
d.path("M585,300 L548,368", "Chute rail R", fill=NONE, stroke=BRASS, strokeWidth=10, cap="round")
d.shape("ellipse", "Rivet L", x=446, y=360, width=12, height=12, fill="#E8C26A", stroke=NONE)
d.shape("ellipse", "Rivet R", x=542, y=360, width=12, height=12, fill="#E8C26A", stroke=NONE)

def md_sheet(cx, cy, w, h, deg, label, op=100):
    d.path(rot_rect_path(cx, cy, w, h, deg), label,
           fill=SHEET_GRAD, stroke="#8A8574", strokeWidth=3, opacity=op)
    t = math.radians(deg); c, s = math.cos(t), math.sin(t)
    def pt(dx, dy): return (cx + dx*c - dy*s, cy + dx*s + dy*c)
    # '#' heading mark
    hx, hy = pt(-w/2 + 14, -h/2 + 14)
    d.text("#", label + " hash", x=hx+5, y=hy+7, size=17, font="Virelai Sans",
           color="#4A4E58", justify="center")
    for j in range(3):
        y0, y1 = pt(-w/2 + 12, -h/2 + 34 + j*15), pt(w/2 - 12, -h/2 + 34 + j*15)
        d.path(f"M{y0[0]:.1f},{y0[1]:.1f} L{y1[0]:.1f},{y1[1]:.1f}",
               f"{label} line {j+1}", fill=NONE, stroke="#8A8574", strokeWidth=3,
               opacity=70, cap="round")

md_sheet(430, 195, 84, 104, -14, "MD sheet L")
md_sheet(505, 168, 88, 110, 2, "MD sheet C")
md_sheet(585, 205, 80, 100, 15, "MD sheet R")
# one sheet half-swallowed by the throat
md_sheet(500, 306, 68, 84, -4, "MD sheet feed", 92)
# throat funnel into the wheel housing
d.path("M452,368 L548,368 L560,396 L440,396 Z", "Throat", fill=lin("#3A2E18", "#241C0E", (440, 368), (560, 396)),
       stroke="#5E4014", strokeWidth=4)

# --- escapement wheel: the content graph turning --------------------------------
WCX, WCY, WR = 470, 480, 118
d.shape("ellipse", "Wheel shadow", x=WCX-130, y=WCY+92, width=260, height=44,
        fill=rad({"offset": 0, "color": "#000000", "opacity": 0.4},
                 {"offset": 1, "color": "#000000", "opacity": 0}), stroke=NONE)
# soft green corona behind the wheel
d.shape("ellipse", "Wheel corona", x=WCX-150, y=WCY-150, width=300, height=300,
        fill=rad({"offset": 0, "color": "#3FD68F", "opacity": 0.22},
                 {"offset": 1, "color": "#3FD68F", "opacity": 0}), stroke=NONE)

N = 12
nodes = [(WCX + WR*math.cos(2*math.pi*i/N - math.pi/2),
          WCY + WR*math.sin(2*math.pi*i/N - math.pi/2)) for i in range(N)]
# gear teeth: a diamond node sitting proud of each graph vertex
for i, (x, y) in enumerate(nodes):
    tx, ty = WCX + (x-WCX)*1.09, WCY + (y-WCY)*1.09
    a = math.atan2(ty-WCY, tx-WCX)
    d.path(rot_rect_path(tx, ty, 20, 14, math.degrees(a) + 90),
           f"Tooth {i+1}", fill=lin("#E8C26A", "#8A5E22", (tx-10, ty-10), (tx+10, ty+10)),
           stroke="#5E4014", strokeWidth=2.5)
# the graph edges: chords vertex to vertex (the gear rim) + spokes
for i in range(N):
    x0, y0 = nodes[i]; x1, y1 = nodes[(i+1) % N]
    d.path(f"M{x0:.0f},{y0:.0f} L{x1:.0f},{y1:.0f}", f"Rim edge {i+1}",
           fill=NONE, stroke=GREEN, strokeWidth=5, opacity=80, cap="round")
for i in (0, 3, 6, 9):
    x0, y0 = nodes[i]
    d.path(f"M{x0:.0f},{y0:.0f} L{WCX},{WCY}", f"Spoke {i+1}",
           fill=NONE, stroke=GREEN, strokeWidth=4, opacity=55, cap="round")
# inner ring of edges (a second graph orbit)
IN_R = 52
inodes = [(WCX + IN_R*math.cos(2*math.pi*i/6 + math.pi/6),
           WCY + IN_R*math.sin(2*math.pi*i/6 + math.pi/6)) for i in range(6)]
for i in range(6):
    x0, y0 = inodes[i]; x1, y1 = inodes[(i+1) % 6]
    d.path(f"M{x0:.0f},{y0:.0f} L{x1:.0f},{y1:.0f}", f"Inner edge {i+1}",
           fill=NONE, stroke="#7CE8B4", strokeWidth=3, opacity=60, cap="round")
for i, (x, y) in enumerate(inodes):
    d.shape("ellipse", f"Inner node {i+1}", x=x-6, y=y-6, width=12, height=12,
            fill="#7CE8B4", stroke="#0E2A1C", strokeWidth=2)
# vertex nodes (the graph's content nodes)
for i, (x, y) in enumerate(nodes):
    d.shape("ellipse", f"Node {i+1}", x=x-9, y=y-9, width=18, height=18,
            fill=rad({"offset": 0, "color": "#7CE8B4"}, {"offset": 1, "color": "#1E7A4E"}),
            stroke="#0E2A1C", strokeWidth=2.5)
# hub
d.shape("ellipse", "Hub", x=WCX-24, y=WCY-24, width=48, height=48,
        fill=rad({"offset": 0, "color": "#E8C26A"}, {"offset": 1, "color": "#8A5E22"}),
        stroke="#5E4014", strokeWidth=4)
d.shape("ellipse", "Hub pin", x=WCX-7, y=WCY-7, width=14, height=14,
        fill="#F2D488", stroke="#5E4014", strokeWidth=2)

# escapement anchor rocking above the wheel
d.path(f"M{WCX-96},{WCY-WR-40} Q{WCX},{WCY-WR-86} {WCX+96},{WCY-WR-40} "
       f"L{WCX+80},{WCY-WR-34} Q{WCX},{WCY-WR-66} {WCX-80},{WCY-WR-34} Z",
       "Escapement anchor", fill=lin("#C8973F", "#7A5218", (WCX-90, WCY-WR-80), (WCX+90, WCY-WR-30)),
       stroke="#5E4014", strokeWidth=3.5)
d.shape("ellipse", "Anchor pivot", x=WCX-8, y=WCY-WR-70, width=16, height=16,
        fill="#E8C26A", stroke="#5E4014", strokeWidth=2.5)

# satellite cog left, meshing (8 nodes)
SCX, SCY, SR = 300, 560, 58
for i in range(8):
    a = 2*math.pi*i/8 + math.pi/8
    x, y = SCX + SR*math.cos(a), SCY + SR*math.sin(a)
    tx, ty = SCX + (x-SCX)*1.2, SCY + (y-SCY)*1.2
    d.path(rot_rect_path(tx, ty, 14, 10, math.degrees(math.atan2(ty-SCY, tx-SCX)) + 90),
           f"Sat tooth {i+1}", fill="#B8863A", stroke="#5E4014", strokeWidth=2)
    x2, y2 = SCX + SR*math.cos(2*math.pi*(i+1)/8 + math.pi/8), SCY + SR*math.sin(2*math.pi*(i+1)/8 + math.pi/8)
    d.path(f"M{x:.0f},{y:.0f} L{x2:.0f},{y2:.0f}", f"Sat edge {i+1}",
           fill=NONE, stroke=GREEN, strokeWidth=4, opacity=70, cap="round")
    d.path(f"M{x:.0f},{y:.0f} L{SCX},{SCY}", f"Sat spoke {i+1}",
           fill=NONE, stroke=GREEN, strokeWidth=2.5, opacity=40, cap="round")
    d.shape("ellipse", f"Sat node {i+1}", x=x-6, y=y-6, width=12, height=12,
            fill="#46D992", stroke="#0E2A1C", strokeWidth=2)
d.shape("ellipse", "Sat hub", x=SCX-14, y=SCY-14, width=28, height=28,
        fill=rad({"offset": 0, "color": "#E8C26A"}, {"offset": 1, "color": "#8A5E22"}),
        stroke="#5E4014", strokeWidth=3)

# --- exit hatch: glowing doorway, pages streaming out ---------------------------
HX0, HY0, HX1, HY1 = 636, 560, 762, 706
# glow spilling out of the hatch
d.shape("ellipse", "Hatch glow", x=HX0-70, y=HY0-60, width=(HX1-HX0)+190, height=(HY1-HY0)+140,
        fill=rad({"offset": 0, "color": "#58F2A8", "opacity": 0.42},
                 {"offset": 0.6, "color": "#58F2A8", "opacity": 0.12},
                 {"offset": 1, "color": "#58F2A8", "opacity": 0}), stroke=NONE)
# hatch frame (arched top)
d.path(f"M{HX0},{HY1} L{HX0},{HY0+34} Q{HX0},{HY0} {HX0+34},{HY0} L{HX1-34},{HY0} "
       f"Q{HX1},{HY0} {HX1},{HY0+34} L{HX1},{HY1} Z",
       "Hatch frame", fill=lin("#3A2E18", "#1C150A", (HX0, HY0), (HX1, HY1)),
       stroke="#8A6428", strokeWidth=5)
# lit opening inside the frame
d.path(f"M{HX0+16},{HY1-8} L{HX0+16},{HY0+38} Q{HX0+16},{HY0+16} {HX0+40},{HY0+16} "
       f"L{HX1-40},{HY0+16} Q{HX1-16},{HY0+16} {HX1-16},{HY0+38} L{HX1-16},{HY1-8} Z",
       "Hatch opening", fill=lin("#9FFFD0", "#1E9A5C", (HX0+16, HY0+16), (HX1-16, HY1-8)),
       stroke=NONE)
# hatch door ajar, hinged on the left
d.path(f"M{HX0+10},{HY1-4} L{HX0-14},{HY1+2} L{HX0-14},{HY0+30} L{HX0+10},{HY0+24} Z",
       "Hatch door", fill=lin("#C8973F", "#7A5218", (HX0-14, HY0), (HX0+10, HY1)),
       stroke="#5E4014", strokeWidth=3)

# pages streaming out toward the targets
def page(cx, cy, w, h, deg, label, ok=True):
    d.path(rot_rect_path(cx, cy, w, h, deg), label, fill=SHEET_GRAD,
           stroke="#8A8574", strokeWidth=2.5)
    t = math.radians(deg); c, s = math.cos(t), math.sin(t)
    def pt(dx, dy): return (cx + dx*c - dy*s, cy + dx*s + dy*c)
    for j in range(2):
        y0, y1 = pt(-w/2 + 8, -h/2 + 16 + j*12), pt(w/2 - 8, -h/2 + 16 + j*12)
        d.path(f"M{y0[0]:.1f},{y0[1]:.1f} L{y1[0]:.1f},{y1[1]:.1f}",
               f"{label} line {j+1}", fill=NONE, stroke="#8A8574", strokeWidth=2.5,
               opacity=70, cap="round")
    if ok:  # validated: green check in the corner
        vx, vy = pt(w/2 - 10, -h/2 + 12)
        d.path(f"M{vx-6:.0f},{vy:.0f} L{vx-1:.0f},{vy+5:.0f} L{vx+7:.0f},{vy-5:.0f}",
               f"{label} check", fill=NONE, stroke="#1E9A5C", strokeWidth=3, cap="round")

for i, (x, y, w, h, dg) in enumerate([(700, 640, 44, 54, -18), (752, 656, 40, 50, -8),
                                      (795, 685, 36, 46, 4), (736, 720, 34, 42, -24)]):
    assert on_disc(x, y, 40), (x, y)
    page(x, y, w, h, dg, f"Out page {i+1}")

# fleet of targets waiting along the lower-right arc
for i, (x, y, r) in enumerate([(815, 555, 30), (835, 640, 25), (765, 722, 22)]):
    assert on_disc(x, y, r + 8), (x, y, r)
    d.shape("ellipse", f"Target {i+1} outer", x=x-r, y=y-r, width=2*r, height=2*r,
            fill=NONE, stroke="#3FD68F", strokeWidth=3, opacity=70)
    d.shape("ellipse", f"Target {i+1} mid", x=x-r*0.6, y=y-r*0.6, width=1.2*r, height=1.2*r,
            fill=NONE, stroke="#7CE8B4", strokeWidth=2.5, opacity=60)
    d.shape("ellipse", f"Target {i+1} core", x=x-4, y=y-4, width=8, height=8,
            fill="#9FFFD0", stroke=NONE)
    # tiny page homing into the bullseye of the first target
page(813, 552, 22, 28, -30, "Inbound page", False)

# --- name + role ---------------------------------------------------------------
d.text("BORIS", "Name", x=500, y=930, size=60, font="Virelai Sans",
       color="#D9F2E4", justify="center")
LINE2, SZ2, TRK = "GRAPH-NATIVE PUBLICATION COMPILER", 21, 150
r = d.text(LINE2, "Second line", x=500, y=968, size=SZ2, font="Virelai Sans",
           color="#6FD8A4", justify="center")
d.cmd("text.setStyle", "Second line tracking", id=r["id"], tracking=TRK)
def find(o, oid):
    if isinstance(o, dict):
        if o.get("id") == oid and "bounds" in o: return o
        o = list(o.values())
    if isinstance(o, list):
        for v in o:
            hit = find(v, oid)
            if hit: return hit
b2 = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("second line bounds", {k: round(v) for k, v in b2.items()})
assert b2["width"] <= 760 and b2["x"] >= 100 and b2["y"] + b2["height"] <= 990, b2

d.finish("boris-V1R00")
