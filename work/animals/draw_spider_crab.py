#!/usr/bin/env python3
"""Japanese spider crab — field plate V1R00. Seen from above, head down:
a small spiky carapace with a long forked rostrum, stalked eyes, ten
appendages radiating in two-jointed sweeps — the front legs the longest
things in the ocean. Deep crimson against kelp-dark water; kelp blades
close on the disc arc below. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420; every leg tip stays inside."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Spider Crab — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420
INK = "#3A0E08"

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def smooth(pts, closed=True, k=1.0):
    n = len(pts)
    s = "M%.1f,%.1f" % pts[0]
    for i in (range(n) if closed else range(n - 1)):
        p0 = pts[(i - 1) % n] if (closed or i > 0) else pts[0]
        p1, p2 = pts[i], pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (closed or i + 2 < n) else pts[-1]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6 * k, p1[1] + (p2[1] - p0[1]) / 6 * k)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6 * k, p2[1] - (p3[1] - p1[1]) / 6 * k)
        s += " C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (c1 + c2 + p2)
    return s + (" Z" if closed else "")

BG_GRAD    = lin(0, 0, 0, 1000, (0, "#0C201A"), (1, "#030A08"))
PLATE_GRAD = rad((0, "#3E6E58"), (0.55, "#234A3C"), (1, "#0E2620"))
CARA_GRAD  = rad((0, "#E05A30"), (0.55, "#B03420"), (1, "#6E160E"))
LEG_GRAD_L = lin(560, 480, 160, 640, (0, "#C84020"), (0.6, "#A02818"), (1, "#7E1A0E"))
LEG_GRAD_R = lin(440, 480, 840, 640, (0, "#C84020"), (0.6, "#A02818"), (1, "#7E1A0E"))
CLAW_GRAD  = lin(500, 560, 420, 740, (0, "#C84020"), (1, "#8A1E10"))
KELP = "#1E4A38"
SPINE_TIP = "#F2C89A"

# --- backdrop + kelp-dark plate ------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876, fill="#2E6B54", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#0A2018", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#7FB49C", strokeWidth=3, opacity=40)
# drifting motes + faint light shafts in the water
for i, (x, y, w) in enumerate([(210,300,6),(780,270,7),(170,470,7),(838,450,6),(250,690,6),(752,700,7),
                               (150,570,5),(855,560,5),(400,112,6),(610,120,7),(330,810,5),(688,806,6),
                               (300,240,4),(700,200,5),(500,96,5)]):
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#9AD0B8", opacity=40, stroke=NONE)
d.path("M360,60 L300,330 L330,335 L390,64 Z", "Light shaft 1", fill="#BFE8D2", opacity=7, stroke=NONE)
d.path("M470,64 L450,300 L478,304 L498,66 Z", "Light shaft 2", fill="#BFE8D2", opacity=6, stroke=NONE)

# rising bubbles beside the crab
for i, (x, y, w) in enumerate([(770,560,16),(792,470,10),(775,390,20),(800,300,12),(782,230,8)]):
    d.shape("ellipse", f"Bubble {i+1}", x=x, y=y, width=w, height=w,
            fill="#FFFFFF", opacity=14, stroke=NONE)

# --- kelp bed closing on the disc's own arc -------------------------------------------
gy = 800
gdx = math.sqrt(R * R - (gy - CY) ** 2)
d.path(f"M{CX-gdx:.1f},{gy} C340,792 430,804 500,800 C580,796 660,804 {CX+gdx:.1f},{gy} "
       f"A{R},{R} 0 0 1 {CX-gdx:.1f},{gy} Z",
       "Sea floor", fill=lin(0, 792, 0, 880, (0, "#163A2C"), (1, "#0A221A")),
       opacity=85, stroke=NONE)
def kelp(x0, tip_x, tip_y, w, label):
    d.path(f"M{x0},{gy + 6} C{x0 - 8},{gy - 60} {tip_x - w},{tip_y + 70} {tip_x},{tip_y} "
           f"C{tip_x + w},{tip_y + 70} {x0 + 8},{gy - 50} {x0 + 14},{gy + 6} Z",
           label, fill=KELP, opacity=75, stroke=NONE)
kelp(268, 242, 700, 18, "Kelp 1")
kelp(760, 790, 690, 20, "Kelp 2")
kelp(700, 726, 730, 14, "Kelp 3")
for i, (x, y, w) in enumerate([(400,810,26),(560,818,30),(640,806,22)]):
    d.shape("ellipse", f"Stone {i+1}", x=x, y=y, width=w, height=w * 0.6,
            fill="#26453A", opacity=80, stroke=NONE)

# --- legs: two-jointed sweeps, dark outline + crimson core + spiny ticks ---------------
def leg(base, mid, tip, side, label):
    grad = LEG_GRAD_L if side == -1 else LEG_GRAD_R
    dd = f"M{base[0]},{base[1]} L{mid[0]},{mid[1]} L{tip[0]},{tip[1]}"
    d.path(dd, label + " edge", fill=NONE, stroke="#4A1008", strokeWidth=12, cap="round")
    d.path(dd, label, fill=NONE, stroke=grad, strokeWidth=6.5, cap="round")
    # knobby joint at the bend
    d.shape("ellipse", label + " joint", x=mid[0] - 7, y=mid[1] - 7, width=14, height=14,
            fill=rad((0, "#C04020"), (1, "#6E140C")), stroke=INK, strokeWidth=2)
    # spiny ticks on the upper side of each segment
    for (x0, y0), (x1, y1) in [(base, mid), (mid, tip)]:
        dx, dy = x1 - x0, y1 - y0
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy / ln, dx / ln
        for k, t in enumerate((0.35, 0.7)):
            px, py = x0 + dx * t, y0 + dy * t
            d.path(f"M{px:.0f},{py:.0f} l{nx * 9 * side:.0f},{ny * 9 * side:.0f}",
                   f"{label} spine", fill=NONE, stroke="#8A2010",
                   strokeWidth=2.4, cap="round")

# walking legs — left then right, front pair reaching lowest and longest
leg((458,530), (330,652), (212,748), -1, "Leg L1")
leg((448,505), (296,562), (150,672), -1, "Leg L2")
leg((450,478), (298,440), (174,384), -1, "Leg L3")
leg((466,455), (348,360), (262,268), -1, "Leg L4")
leg((542,530), (670,652), (788,748), 1, "Leg R1")
leg((552,505), (704,562), (850,672), 1, "Leg R2")
leg((550,478), (702,440), (826,384), 1, "Leg R3")
leg((534,455), (652,360), (738,268), 1, "Leg R4")

# --- carapace: spiky pear, wider at the rear -------------------------------------------
# base shell
d.path(smooth([(500,418),(556,426),(582,462),(578,506),(548,540),
               (500,556),(452,540),(422,506),(418,462),(444,426)], k=1.1),
       "Carapace", fill=CARA_GRAD, stroke=INK, strokeWidth=5)
# rim spines — small triangles riding the edge
def rim_spine(x, y, ang, L, w, label):
    t = math.radians(ang)
    tx, ty = x + math.cos(t) * L, y + math.sin(t) * L
    nx, ny = -math.sin(t) * w / 2, math.cos(t) * w / 2
    d.path(f"M{x - nx:.0f},{y - ny:.0f} L{tx:.0f},{ty:.0f} L{x + nx:.0f},{y + ny:.0f} Z",
           label, fill=CARA_GRAD, stroke=INK, strokeWidth=2)
for i, (x, y, a) in enumerate([(440,432,-145),(470,424,-170),(530,424,-10),(560,432,-35),
                               (578,462,-5),(576,500,20),(548,534,50),(452,534,130),
                               (424,500,160),(422,462,175)]):
    rim_spine(x, y, a, 18, 14, f"Rim spine {i+1}")
# dorsal bumps + pale spine tips
for i, (x, y, w) in enumerate([(478,452,12),(524,452,12),(500,478,14),(458,486,10),
                               (542,486,10),(486,514,9),(516,514,9),(500,440,10)]):
    d.shape("ellipse", f"Carapace bump {i+1}", x=x - w / 2, y=y - w / 2, width=w, height=w * 0.8,
            fill="#E06838", opacity=70, stroke=NONE)
    d.shape("ellipse", f"Bump tip {i+1}", x=x - 2, y=y - w / 2 - 2, width=4, height=4,
            fill=SPINE_TIP, opacity=85, stroke=NONE)
# shell sheen + rear shade
d.shape("ellipse", "Carapace sheen", x=452, y=434, width=90, height=44,
        fill="#F2A070", opacity=25, stroke=NONE)
# epibionts: the crab wears the ocean — sponge + algae tufts on the carapace
d.shape("ellipse", "Sponge 1", x=470, y=446, width=18, height=12, fill="#5E7A3A", stroke=INK, strokeWidth=1.5)
d.shape("ellipse", "Sponge 2", x=524, y=498, width=14, height=10, fill="#6E5A2E", stroke=INK, strokeWidth=1.5)
for i, (x0, y0, x1, y1) in enumerate([(480,450,474,436),(484,451,486,434),(530,502,536,488)]):
    d.path(f"M{x0},{y0} Q{(x0+x1)//2+3},{(y0+y1)//2-4} {x1},{y1}", f"Algae blade {i+1}",
           fill=NONE, stroke="#3E6B34", strokeWidth=2.5, cap="round")
d.path("M440,520 C470,538 530,538 560,518 C540,540 460,542 440,520 Z",
       "Rear shade", fill="#4E1008", opacity=40, stroke=NONE)

# --- chelipeds: long thin arms ending in small pincers ----------------------------------
for s, (mid, claw) in [(-1, ((430,640), (398,706))), (1, ((570,640), (602,706)))]:
    base = (486 if s == -1 else 514, 552)
    dd = f"M{base[0]},{base[1]} L{mid[0]},{mid[1]} L{claw[0]},{claw[1]}"
    d.path(dd, f"Arm {'L' if s == -1 else 'R'} edge", fill=NONE,
           stroke="#4A1008", strokeWidth=9, cap="round")
    d.path(dd, f"Arm {'L' if s == -1 else 'R'}", fill=NONE,
           stroke=CLAW_GRAD, strokeWidth=5, cap="round")
    d.shape("ellipse", f"Arm {'L' if s == -1 else 'R'} joint",
            x=mid[0] - 5, y=mid[1] - 5, width=10, height=10,
            fill="#8A1E10", stroke=INK, strokeWidth=1.5)
    # pincer: two short prongs
    d.path(f"M{claw[0]},{claw[1]} L{claw[0] - 10 * s},{claw[1] + 16} "
           f"M{claw[0]},{claw[1]} L{claw[0] + 8 * s},{claw[1] + 18}",
           f"Pincer {'L' if s == -1 else 'R'}", fill=NONE, stroke="#C84020",
           strokeWidth=4, cap="round")

# --- rostrum + stalked eyes --------------------------------------------------------------
d.path("M492,548 L478,600 L486,602 L496,556 Z", "Rostrum spike L", fill=CARA_GRAD, stroke=INK, strokeWidth=2)
d.path("M508,548 L522,600 L514,602 L504,556 Z", "Rostrum spike R", fill=CARA_GRAD, stroke=INK, strokeWidth=2)
d.shape("ellipse", "Eye stalk L", x=470, y=538, width=10, height=16, fill="#8A1E10", stroke=INK, strokeWidth=1.5)
d.shape("ellipse", "Eye stalk R", x=520, y=538, width=10, height=16, fill="#8A1E10", stroke=INK, strokeWidth=1.5)
d.shape("ellipse", "Eye L", x=471, y=534, width=8, height=8, fill="#1E0804", stroke=NONE)
d.shape("ellipse", "Eye R", x=521, y=534, width=8, height=8, fill="#1E0804", stroke=NONE)
d.shape("ellipse", "Eye glint L", x=473, y=535, width=2.5, height=2.5, fill="#FFFFFF", opacity=90, stroke=NONE)
d.shape("ellipse", "Eye glint R", x=523, y=535, width=2.5, height=2.5, fill="#FFFFFF", opacity=90, stroke=NONE)

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#081C14", strokeWidth=6)

# --- name -----------------------------------------------------------------------------------
d.text("SPIDER CRAB", "Name", x=500, y=940, size=58, font="Virelai Sans",
       color="#C8E4D4", justify="center")
LINE2, SZ2, TRK = "MACROCHEIRA KAEMPFERI", 20, 260
r = d.text(LINE2, "Second line", x=500, y=973, size=SZ2, font="Virelai Sans",
           color="#7FAE96", justify="center")
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

d.finish("spider-crab-V1R00")
