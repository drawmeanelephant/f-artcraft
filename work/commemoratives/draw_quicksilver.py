#!/usr/bin/env python3
"""quicksilver — commemorative plate V1R00. The Mercury Leap: a single
droplet of liquid mercury mid-leap above a command key, stretched into
that impossible quicksilver shape — the launcher as alchemical metal.
Gunmetal dark, mercury bright, one silver trail. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("quicksilver — Commemorative Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#0A0E14"   # warm dark, never pure black

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

def smooth(pts, closed=False, k=1.0):
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

def rounded_rect(x, y, w, h, r):
    return (f"M{x+r},{y} L{x+w-r},{y} Q{x+w},{y} {x+w},{y+r} "
            f"L{x+w},{y+h-r} Q{x+w},{y+h} {x+w-r},{y+h} "
            f"L{x+r},{y+h} Q{x},{y+h} {x},{y+h-r} "
            f"L{x},{y+r} Q{x},{y} {x+r},{y} Z")

MERC_HI, MERC_MID, MERC_LO = "#F8FCFF", "#B9C6D2", "#5E6C7A"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin("#131920", "#04060A", (500, 0), (500, 1000)), stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad({"offset": 0, "color": "#333D48"},
                 {"offset": 0.68, "color": "#1A212A"},
                 {"offset": 1, "color": "#0A0E14"}),
        stroke="#8A97A5", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8E2EC", strokeWidth=3, opacity=26)
# metal dust
for i, (x, y, w, o) in enumerate([(218,208,4,22),(790,200,5,24),(162,450,4,20),
                                  (845,422,4,22),(252,748,4,18),(738,778,5,20),
                                  (352,110,3,22),(652,106,4,22),(140,596,3,18),
                                  (858,586,4,20),(700,300,3,18),(290,330,3,18)]):
    assert on_disc(x, y, 12)
    d.shape("ellipse", f"Dust {i+1}", x=x-w/2, y=y-w/2, width=w, height=w,
            fill="#D8E2EC", opacity=o, stroke=NONE)
# cool glow around the leaping droplet
d.shape("ellipse", "Leap glow", x=340, y=110, width=330, height=400,
        fill=rad({"offset": 0, "color": "#B9C6D2", "opacity": 0.14},
                 {"offset": 1, "color": "#B9C6D2", "opacity": 0}), stroke=NONE)

# --- the desk, closing on the disc's own arc -----------------------------------
d.path("M206.1,760 Q500,690 793.9,760 A420,420 0 0 1 206.1,760 Z", "Desk",
       fill=lin("#1C232C", "#080B10", (500, 700), (500, 880)), stroke=NONE)
# mercury sheen pooled on the desk under the key
d.shape("ellipse", "Desk sheen", x=350, y=694, width=300, height=48,
        fill=rad({"offset": 0, "color": "#B9C6D2", "opacity": 0.16},
                 {"offset": 1, "color": "#B9C6D2", "opacity": 0}), stroke=NONE)

# --- the silver trail: the leap's arc, behind everything -------------------------
d.path("M338,628 C300,520 330,400 440,330 C460,318 478,308 496,300",
       "Silver trail", fill=NONE, stroke="#D8E2EC", strokeWidth=7,
       opacity=45, cap="round")
d.path("M352,624 C320,528 348,420 448,352", "Trail core",
       fill=NONE, stroke="#F8FCFF", strokeWidth=3, opacity=40, cap="round")
# speed ticks off the trail
for i, (x0, y0, x1, y1) in enumerate([(352,470,378,452),(330,545,358,532),
                                      (400,375,420,362)]):
    d.path(f"M{x0},{y0} L{x1},{y1}", f"Tick {i+1}", fill=NONE,
           stroke="#B9C6D2", strokeWidth=4, opacity=30, cap="round")

# --- the command key ----------------------------------------------------------------
d.shape("ellipse", "Key shadow", x=350, y=690, width=300, height=42,
        fill=rad({"offset": 0, "color": "#000000", "opacity": 0.55},
                 {"offset": 1, "color": "#000000", "opacity": 0}), stroke=NONE)
# key body (dark base skirt) then top face
d.path(rounded_rect(402, 552, 196, 158, 30), "Key base",
       fill=lin("#2A323C", "#10151B", (402, 552), (598, 710)),
       stroke=INK, strokeWidth=5)
d.path(rounded_rect(412, 542, 176, 140, 26), "Key face",
       fill=lin("#4A5662", "#1C232B", (412, 542), (588, 682),
                extra=[{"offset": 0.45, "color": "#38424C"}]),
       stroke=INK, strokeWidth=4)
# keycap top sheen
d.path(rounded_rect(422, 550, 156, 60, 20), "Key sheen",
       fill="#D8E2EC", opacity=12, stroke=NONE)
# dished crown of the cap
d.shape("ellipse", "Key dish", x=452, y=566, width=96, height=84,
        fill=rad({"offset": 0, "color": "#10151B", "opacity": 0.5},
                 {"offset": 1, "color": "#10151B", "opacity": 0}), stroke=NONE)

# the command glyph: four loops + the knot's square, one silver strand
GC = "#E4ECF4"   # glyph silver
GW = 10          # strand width, >=3pt rule honoured several times over
KCX, KCY, LS, LR = 500, 608, 34, 19          # knot centre, lobe spacing, lobe radius
for i, (lx, ly) in enumerate([(KCX-LS, KCY-LS), (KCX+LS, KCY-LS),
                              (KCX+LS, KCY+LS), (KCX-LS, KCY+LS)]):
    d.shape("ellipse", f"Cmd lobe {i+1}", x=lx-LR, y=ly-LR, width=LR*2, height=LR*2,
            fill=NONE, stroke=GC, strokeWidth=GW)
d.path(f"M{KCX-LS},{KCY-LS} L{KCX+LS},{KCY-LS} L{KCX+LS},{KCY+LS} "
       f"L{KCX-LS},{KCY+LS} Z", "Cmd knot",
       fill=NONE, stroke=GC, strokeWidth=GW)
# glyph glint on the top-left strand
d.path(f"M{KCX-LS},{KCY-LS} L{KCX-8},{KCY-LS}", "Cmd glint", fill=NONE,
       stroke="#FFFFFF", strokeWidth=3, opacity=60, cap="round")

# --- the mercury droplet, mid-leap ---------------------------------------------------
DROPS = [(455,362),(444,326),(452,290),(468,254),(480,220),(490,190),
         (498,164),(508,146),(524,152),(522,182),(514,212),(522,246),
         (546,276),(559,312),(558,348),(534,374),(500,386),(468,378)]
d.path(smooth(DROPS, closed=True, k=1.15), "Mercury droplet",
       fill=rad({"offset": 0, "color": MERC_HI},
                {"offset": 0.45, "color": MERC_MID},
                {"offset": 0.8, "color": "#8A97A5"},
                {"offset": 1, "color": MERC_LO}),
       stroke="#39434D", strokeWidth=4)
# mercury mirrors the dark room: a wavy dark band inside the blob
d.path(smooth([(462,300),(486,286),(516,292),(540,282),(548,306),
               (522,318),(492,312),(466,320)], closed=True, k=1.2),
       "Room reflection", fill="#2A323C", opacity=60, stroke=NONE)
d.path(smooth([(478,222),(494,214),(512,220),(518,238),
               (500,246),(484,240)], closed=True, k=1.2),
       "Room reflection 2", fill="#39434D", opacity=45, stroke=NONE)
# specular: the leap's hot edge, left side and tip glint
d.path("M462,340 C452,310 458,280 474,252", "Spec streak", fill=NONE,
       stroke="#FFFFFF", strokeWidth=7, opacity=70, cap="round")
d.path("M486,196 C492,178 500,162 508,152", "Spec streak 2", fill=NONE,
       stroke="#FFFFFF", strokeWidth=5, opacity=55, cap="round")
d.path("M510,142 L514,156 M504,148 L518,150", "Tip glint", fill=NONE,
       stroke="#FFFFFF", strokeWidth=3, opacity=80, cap="round")
# bright bulb belly-light
d.shape("ellipse", "Bulb light", x=472, y=330, width=56, height=40,
        fill=rad({"offset": 0, "color": "#FFFFFF", "opacity": 0.55},
                 {"offset": 1, "color": "#FFFFFF", "opacity": 0}), stroke=NONE)

# mercury beads shed by the leap, falling toward the key
for i, (x, y, r) in enumerate([(452,418,11),(548,452,9),(500,468,7)]):
    d.shape("ellipse", f"Bead {i+1}", x=x-r, y=y-r, width=r*2, height=r*2,
            fill=rad({"offset": 0, "color": MERC_HI},
                     {"offset": 0.6, "color": MERC_MID},
                     {"offset": 1, "color": MERC_LO}),
            stroke="#39434D", strokeWidth=2.5)
    d.shape("ellipse", f"Bead glint {i+1}", x=x-r*0.45, y=y-r*0.55,
            width=r*0.7, height=r*0.5, fill="#FFFFFF", opacity=75, stroke=NONE)
# two tiny beads clinging to the key where it leapt from
for i, (x, y, r) in enumerate([(438,586,5),(566,574,4)]):
    d.shape("ellipse", f"Key bead {i+1}", x=x-r, y=y-r, width=r*2, height=r*2,
            fill=rad({"offset": 0, "color": MERC_HI},
                     {"offset": 1, "color": MERC_LO}), stroke=NONE)

# --- name + role ------------------------------------------------------------------
d.text("QUICKSILVER", "Name", x=500, y=930, size=56, font="Virelai Sans",
       color="#E8F0F8", justify="center")
LINE2, SZ2, TRK = "MACOS PRODUCTIVITY LEGEND", 23, 280
r = d.text(LINE2, "Second line", x=500, y=968, size=SZ2, font="Virelai Sans",
           color="#8A97A5", justify="center")
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

d.finish("quicksilver-V1R00")
