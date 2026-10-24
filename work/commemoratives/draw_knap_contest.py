#!/usr/bin/env python3
"""knap-contest — commemorative plate V1R00. The Rosette: a prize rosette made
of knap template braces — concentric rings of {{ }} folding into ribbon
pleats, a GAMEPLAN medallion at the center, two ribbon tails ending in tiny
route paths. Contest-night velvet behind. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("knap-contest — Commemorative Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#1E0E08"              # warm dark, never pure black
GOLD = "#E8CF90"
RIB_HI = "#A8323E"
RIB_LO = "#5E1420"

def on_disc(x, y, pad):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

def lin(c0, c1, start=None, end=None, extra=None):
    stops = [{"offset": 0, "color": c0}]
    if extra: stops += extra
    stops.append({"offset": 1, "color": c1})
    g = {"kind": "linear", "stops": stops}
    if start: g["start"], g["end"] = [round(v, 1) for v in start], [round(v, 1) for v in end]
    return {"gradient": g}

def rad(*stops):
    return {"gradient": {"kind": "radial", "stops": stops}}

def pol(r, deg, cx=PCX, cy=PCY):
    t = math.radians(deg)
    return (cx + r * math.cos(t), cy + r * math.sin(t))

def rot(cx, cy, deg, x, y):
    """Rotate local point (x,y) by deg about (cx,cy)."""
    t = math.radians(deg); c, s = math.cos(t), math.sin(t)
    return (cx + x * c - y * s, cy + x * s + y * c)

def brace_path(cx, cy, deg, h=13.0):
    """One '{' motif at (cx,cy), local y rotated to deg. Returns path data.
    Local: stem runs along y, notch pokes toward -x."""
    pts = [
        ("M", (4, -h)),
        ("Q", (0, -h), (0, -h + 4)),
        ("L", (0, -4)),
        ("Q", (0, 0), (-5, 0)),
        ("Q", (0, 0), (0, 4)),
        ("L", (0, h - 4)),
        ("Q", (0, h), (4, h)),
    ]
    out = []
    for op in pts:
        if op[0] == "M":
            x, y = rot(cx, cy, deg, *op[1]); out.append(f"M{x:.1f},{y:.1f}")
        elif op[0] == "L":
            x, y = rot(cx, cy, deg, *op[1]); out.append(f"L{x:.1f},{y:.1f}")
        else:
            x1, y1 = rot(cx, cy, deg, *op[1])
            x2, y2 = rot(cx, cy, deg, *op[2])
            out.append(f"Q{x1:.1f},{y1:.1f} {x2:.1f},{y2:.1f}")
    return " ".join(out)

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin("#140609", "#050203", (500, 0), (500, 1000)), stroke=NONE)
# velvet plate
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad({"offset": 0, "color": "#5E2030"},
                 {"offset": 0.62, "color": "#2E0E18"},
                 {"offset": 1, "color": "#140609"}),
        stroke="#A87E4E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8CF90", strokeWidth=3, opacity=26)
# velvet sheen sweep, upper-left
d.shape("ellipse", "Velvet sheen", x=150, y=90, width=520, height=380,
        fill=rad({"offset": 0, "color": "#8A3A50", "opacity": 0.20},
                 {"offset": 1, "color": "#8A3A50", "opacity": 0}), stroke=NONE)
# pin flecks on the velvet
for i, (x, y, w) in enumerate([(212,244,4),(792,238,5),(160,470,4),(848,488,4),
                               (256,708,4),(744,742,5),(352,124,4),(652,120,4),
                               (152,606,3),(852,600,4),(440,812,3),(586,810,4)]):
    assert on_disc(x, y, 12)
    d.shape("ellipse", f"Fleck {i+1}", x=x-w/2, y=y-w/2, width=w, height=w,
            fill="#E8CF90", opacity=18, stroke=NONE)

# --- ribbon tails, hanging behind the rosette --------------------------------------
d.shape("ellipse", "Rosette shadow", x=300, y=290, width=440, height=400,
        fill=rad({"offset": 0, "color": "#0A0306", "opacity": 0.5},
                 {"offset": 1, "color": "#0A0306", "opacity": 0}), stroke=NONE)
# left tail
d.path("M452,664 C432,720 412,756 396,792 L406,778 L418,800 "
       "C436,762 458,726 474,678 Z", "Tail L",
       fill=lin("#9A2E3A", "#541220", (440, 664), (410, 800)),
       stroke=INK, strokeWidth=4)
d.path("M452,664 C432,720 412,756 396,792", "Tail L fold", fill=NONE,
       stroke="#3A0C14", strokeWidth=3, opacity=70)
d.path("M474,678 C458,726 436,762 418,800", "Tail L edge", fill=NONE,
       stroke="#D88A6A", strokeWidth=2.5, opacity=50, cap="round")
# right tail
d.path("M548,664 C568,720 588,756 604,792 L594,778 L582,800 "
       "C564,762 542,726 526,678 Z", "Tail R",
       fill=lin("#9A2E3A", "#541220", (560, 664), (590, 800)),
       stroke=INK, strokeWidth=4)
d.path("M548,664 C568,720 588,756 604,792", "Tail R fold", fill=NONE,
       stroke="#3A0C14", strokeWidth=3, opacity=70)
d.path("M526,678 C542,726 564,762 582,800", "Tail R edge", fill=NONE,
       stroke="#D88A6A", strokeWidth=2.5, opacity=50, cap="round")
# tiny route-path tags on the tail ends
for side, tx, tag in (("L", 386, "/e/{s}"), ("R", 614, "/r/{k}")):
    d.shape("rectangle", f"Tag {side}", x=tx-30, y=792, width=60, height=20,
            fill=lin("#E8CF90", "#B08C4E", (tx-30, 792), (tx+30, 812)),
            stroke=INK, strokeWidth=2.5)
    d.text(tag, f"Route {side}", x=tx, y=805, size=9, font="Source Sans 3",
           color="#3A2408", justify="center")

# --- the pleated ring ----------------------------------------------------------------
R_IN, R_OUT, N = 158, 250, 28
for k in range(N):
    a0 = k * 360 / N - 90
    a1 = a0 + 360 / N
    i0, i1 = pol(R_IN, a0), pol(R_IN, a1)
    o0, o1 = pol(R_OUT, a0), pol(R_OUT, a1)
    tone = RIB_HI if k % 2 else "#8A2434"
    d.path(f"M{i0[0]:.1f},{i0[1]:.1f} L{o0[0]:.1f},{o0[1]:.1f} "
           f"L{o1[0]:.1f},{o1[1]:.1f} L{i1[0]:.1f},{i1[1]:.1f} Z",
           f"Pleat {k+1}", fill=tone, stroke="#3A0C14", strokeWidth=1.5)
# pleat shading: inner edge shadow + outer dim, plus sheen on the lit half
d.shape("ellipse", "Pleat inner shade", x=PCX-R_IN-14, y=PCY-R_IN-14,
        width=2*(R_IN+14), height=2*(R_IN+14),
        fill=rad({"offset": 0, "color": "#2A0810", "opacity": 0},
                 {"offset": 0.82, "color": "#2A0810", "opacity": 0},
                 {"offset": 1, "color": "#2A0810", "opacity": 0.55}),
        stroke=NONE)
d.shape("ellipse", "Pleat sheen", x=330, y=300, width=300, height=260,
        fill=rad({"offset": 0, "color": "#E8A088", "opacity": 0.14},
                 {"offset": 1, "color": "#E8A088", "opacity": 0}), stroke=NONE)
# ring edge lines
d.shape("ellipse", "Pleat outer edge", x=PCX-R_OUT, y=PCY-R_OUT,
        width=2*R_OUT, height=2*R_OUT, fill=NONE, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Pleat inner edge", x=PCX-R_IN, y=PCY-R_IN,
        width=2*R_IN, height=2*R_IN, fill=NONE, stroke=INK, strokeWidth=3)
# gold edging just inside the pleats
d.shape("ellipse", "Gold edge", x=PCX-151, y=PCY-151, width=302, height=302,
        fill=NONE, stroke=GOLD, strokeWidth=2.5, opacity=70)

# --- concentric rings of {{ }} ----------------------------------------------------------
def brace_ring(r, n, phase, h, label):
    for k in range(n):
        a = k * 360 / n + phase
        # two braces offset radially -> reads as {{ from outside the ring
        d.path(brace_path(*pol(r - 4, a), a, h=h) + " " +
               brace_path(*pol(r + 4, a), a, h=h + 2),
               f"{label} {k+1}", fill=NONE, stroke=GOLD,
               strokeWidth=3, cap="round")

brace_ring(112, 14, -90, 12, "Inner brace")
brace_ring(136, 18, -90 + 360/36, 12, "Outer brace")

# --- the GAMEPLAN medallion --------------------------------------------------------------
d.shape("ellipse", "Medallion glow", x=PCX-105, y=PCY-105, width=210, height=210,
        fill=rad({"offset": 0, "color": "#F0D878", "opacity": 0.22},
                 {"offset": 1, "color": "#F0D878", "opacity": 0}), stroke=NONE)
d.shape("ellipse", "Medallion", x=PCX-80, y=PCY-80, width=160, height=160,
        fill=rad({"offset": 0, "color": "#F0D878"},
                 {"offset": 0.7, "color": "#C8A04E"},
                 {"offset": 1, "color": "#8A6428"}),
        stroke=INK, strokeWidth=4)
d.shape("ellipse", "Medallion ring", x=PCX-68, y=PCY-68, width=136, height=136,
        fill=NONE, stroke="#7A5A20", strokeWidth=2.5, opacity=70)
d.shape("ellipse", "Medallion sheen", x=PCX-58, y=PCY-68, width=92, height=56,
        fill="#FFF6D8", opacity=22, stroke=NONE)
m = d.text("GAMEPLAN", "Medallion word", x=PCX, y=PCY+2, size=17,
           font="Virelai Sans", color="#3A2408", justify="center")
d.cmd("text.setStyle", "Medallion tracking", ids=[m["id"]], tracking=140)
# laurel ticks under the word
d.path(f"M{PCX-30},{PCY+18} Q{PCX},{PCY+26} {PCX+30},{PCY+18}",
       "Medallion tick", fill=NONE, stroke="#7A5A20", strokeWidth=3,
       opacity=80, cap="round")

# --- name + role ------------------------------------------------------------------
d.text("KNAP-CONTEST", "Name", x=500, y=930, size=56, font="Virelai Sans",
       color="#F0E0C8", justify="center")
LINE2, SZ2, TRK = "A KNAP TEMPLATE CONTEST", 24, 300
r = d.text(LINE2, "Second line", x=500, y=968, size=SZ2, font="Virelai Sans",
           color="#C88A6A", justify="center")
d.cmd("text.setStyle", "Second line tracking", ids=[r["id"]], tracking=TRK)
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

d.finish("knap-contest-V1R00")
