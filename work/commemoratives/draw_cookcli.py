#!/usr/bin/env python3
"""cookcli — commemorative plate V1R00. The Recipe Engine: a copper pot on
a quiet stove, steam rising off it and resolving into Cooklang markup —
@ingredient{}, #cookware, ~timers curling like steam tendrils. Enamel blue
and copper; a recipe parsed the way a kitchen smells. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("cookcli — Commemorative Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#1E0E06"   # warm dark, never pure black

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

def tendril(pts, widths, label, color, opacity):
    """A tapering steam wisp: closed smooth path around a centerline."""
    left, right = [], []
    for (x, y), w in zip(pts, widths):
        left.append((x - w / 2, y))
        right.append((x + w / 2, y))
    d.path(smooth(left + right[::-1], closed=True, k=1.1), label,
           fill=color, opacity=opacity, stroke=NONE)

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin("#101828", "#04060C", (500, 0), (500, 1000)), stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad({"offset": 0, "color": "#2E4A66"},
                 {"offset": 0.68, "color": "#17293C"},
                 {"offset": 1, "color": "#0A141F"}),
        stroke="#A06A3E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F0E2CC", strokeWidth=3, opacity=28)
# enamel dust / spice flecks
for i, (x, y, w, c, o) in enumerate([(215,210,4,"#F0E2CC",22),(792,205,5,"#D98B4E",26),
                                     (165,450,4,"#F0E2CC",20),(845,425,4,"#D98B4E",22),
                                     (250,745,4,"#F0E2CC",18),(735,780,5,"#D98B4E",20),
                                     (350,112,3,"#F0E2CC",22),(650,108,4,"#D98B4E",22),
                                     (142,598,3,"#F0E2CC",18),(858,588,4,"#D98B4E",20)]):
    assert on_disc(x, y, 12)
    d.shape("ellipse", f"Fleck {i+1}", x=x-w/2, y=y-w/2, width=w, height=w,
            fill=c, opacity=o, stroke=NONE)
# warm kitchen glow behind the pot
d.shape("ellipse", "Hearth glow", x=240, y=180, width=520, height=480,
        fill=rad({"offset": 0, "color": "#D98B4E", "opacity": 0.12},
                 {"offset": 1, "color": "#D98B4E", "opacity": 0}), stroke=NONE)

# --- the counter closing on the disc's own arc ---------------------------------
d.path("M206.1,760 Q500,690 793.9,760 A420,420 0 0 1 206.1,760 Z", "Counter",
       fill=lin("#18202E", "#070A10", (500, 700), (500, 880)), stroke=NONE)
# stove top band on the counter
d.path("M280,724 Q500,700 720,724 L720,760 Q500,738 280,760 Z", "Stovetop",
       fill=lin("#232C3C", "#0C1018", (500, 700), (500, 760)), stroke=NONE)
# copper light pooled on the stove under the pot
d.shape("ellipse", "Stove pool", x=350, y=700, width=300, height=46,
        fill=rad({"offset": 0, "color": "#E89858", "opacity": 0.22},
                 {"offset": 1, "color": "#E89858", "opacity": 0}), stroke=NONE)

# --- the burner: dark ring + quiet blue flame ------------------------------------
d.shape("ellipse", "Burner ring", x=356, y=700, width=288, height=52,
        fill=NONE, stroke="#0E1420", strokeWidth=10)
d.shape("ellipse", "Burner glow", x=390, y=708, width=220, height=34,
        fill=rad({"offset": 0, "color": "#7AB8F0", "opacity": 0.30},
                 {"offset": 1, "color": "#7AB8F0", "opacity": 0}), stroke=NONE)
for i, x in enumerate(range(408, 600, 24)):
    y = 724 + 8 * math.sin((x - 408) / 60.0)
    d.path(f"M{x},{y-12} Q{x+4},{y} {x},{y+4}", f"Flame {i+1}", fill=NONE,
           stroke="#9CCCF4", strokeWidth=4, opacity=55, cap="round")

# --- steam tendrils (behind the rim so they read as rising out of the pot) -------
tendril([(455,470),(448,420),(462,368),(440,315),(452,262),(430,215),(442,178)],
        [26,30,26,20,15,10,5], "Steam L", "#EAF2F8", 20)
tendril([(520,468),(532,415),(512,360),(528,305),(508,250),(522,205),(512,168)],
        [30,34,28,22,16,11,5], "Steam C", "#F4F0E4", 24)
tendril([(580,472),(592,428),(574,378),(596,330),(580,282),(598,244),(588,214)],
        [22,26,22,17,12,8,4], "Steam R", "#EAF2F8", 17)
# faint secondary wisps
tendril([(485,468),(478,430),(490,392),(480,350)], [16,14,10,6],
        "Steam wisp 1", "#F4F0E4", 12)
tendril([(548,470),(558,436),(546,398),(556,360)], [14,12,9,5],
        "Steam wisp 2", "#EAF2F8", 10)

# --- Cooklang markup condensing out of the steam ----------------------------------
# markup is code: set in Source Sans 3 (Virelai Sans has no digits either)
d.text("@salt{}", "Markup ingredient", x=402, y=196, size=21,
       font="Source Sans 3", color="#F0E2CC", justify="center")
d.text("#stockpot", "Markup cookware", x=522, y=152, size=21,
       font="Source Sans 3", color="#D8E4F0", justify="center")
d.text("~{15%min}", "Markup timer", x=610, y=216, size=20,
       font="Source Sans 3", color="#F0E2CC", justify="center")
d.text("@thyme{2%sprigs}", "Markup herb", x=470, y=248, size=15,
       font="Source Sans 3", color="#C4B89E", justify="center")
# tiny stray glyphs drifting off the tendrils
for i, (t, x, y, s, c) in enumerate([("@",352,268,18,"#D8E4F0"),("{}",660,300,16,"#C4B89E"),
                                     ("~",575,120,18,"#F0E2CC"),("#",448,132,15,"#D8E4F0"),
                                     ("{}",352,158,13,"#C4B89E")]):
    assert on_disc(x, y, 16)
    d.text(t, f"Glyph {i+1}", x=x, y=y, size=s, font="Source Sans 3",
           color=c, justify="center")

# --- the copper pot ----------------------------------------------------------------
d.shape("ellipse", "Pot shadow", x=340, y=700, width=320, height=44,
        fill=rad({"offset": 0, "color": "#000000", "opacity": 0.55},
                 {"offset": 1, "color": "#000000", "opacity": 0}), stroke=NONE)
# side handles first so the body overlaps their roots
for side, sgn in (("L", -1), ("R", 1)):
    x0 = 500 + sgn * 118
    d.path(f"M{x0},505 C{x0 + sgn*52},498 {x0 + sgn*66},540 {x0 + sgn*30},556",
           f"Handle {side}", fill=NONE, stroke="#6E3416", strokeWidth=13, cap="round")
    d.path(f"M{x0},505 C{x0 + sgn*50},500 {x0 + sgn*62},538 {x0 + sgn*32},552",
           f"Handle {side} hi", fill=NONE, stroke="#D98B4E", strokeWidth=5,
           opacity=80, cap="round")
# body: rounded belly, top edge hidden under the rim ellipse
d.path("M382,466 C372,575 402,686 500,710 C598,686 628,575 618,466 Z",
       "Pot body",
       fill=lin("#5E2C12", "#6E3416", (382, 560), (618, 560),
                extra=[{"offset": 0.30, "color": "#D98B4E"},
                       {"offset": 0.48, "color": "#F2B87A"},
                       {"offset": 0.66, "color": "#C47434"}]),
       stroke=INK, strokeWidth=5)
# belly highlight band + lower shade
d.path("M404,540 C440,560 560,560 596,540 C590,600 560,650 500,662 "
       "C440,650 410,600 404,540 Z",
       "Pot sheen", fill="#F8D0A0", opacity=16, stroke=NONE)
d.path("M420,676 C460,700 540,700 580,676 C560,700 440,700 420,676 Z",
       "Pot base shade", fill="#3A1A08", opacity=35, stroke=NONE)
# hammered-copper dimples
for i, (x, y, w) in enumerate([(430,560,10),(470,600,9),(530,585,10),(565,620,9),
                               (455,640,8),(545,535,8),(500,560,9),(485,625,7),
                               (420,610,7),(580,575,8)]):
    d.shape("ellipse", f"Dimple {i+1}", x=x-w/2, y=y-w/2, width=w, height=w*0.7,
            fill="#F8D0A0", opacity=12, stroke=NONE)
# rim: bright copper ring
d.shape("ellipse", "Pot rim", x=380, y=442, width=240, height=48,
        fill=lin("#8A4318", "#7A3C1A", (380, 466), (620, 466),
                 extra=[{"offset": 0.35, "color": "#F2B87A"},
                        {"offset": 0.55, "color": "#E89858"}]),
        stroke=INK, strokeWidth=5)
# the stew surface inside the rim
d.shape("ellipse", "Stew", x=396, y=452, width=208, height=32,
        fill=rad({"offset": 0, "color": "#5A2E14"},
                 {"offset": 0.75, "color": "#381A08"},
                 {"offset": 1, "color": "#200D04"}),
        stroke="#1E0E06", strokeWidth=3)
# simmer shimmer + bubbles
d.path("M430,464 Q500,452 570,464", "Stew shimmer", fill=NONE,
       stroke="#E89858", strokeWidth=4, opacity=40, cap="round")
for i, (x, y, w) in enumerate([(455,462,7),(505,458,6),(545,464,8),(480,466,5)]):
    d.shape("ellipse", f"Bubble {i+1}", x=x-w/2, y=y-w/2, width=w, height=w*0.6,
            fill="#D98B4E", opacity=45, stroke=NONE)

# --- name + role ------------------------------------------------------------------
d.text("COOKCLI", "Name", x=500, y=930, size=58, font="Virelai Sans",
       color="#F2E4CC", justify="center")
LINE2, SZ2, TRK = "COOKLANG COMMAND LINE", 23, 300
r = d.text(LINE2, "Second line", x=500, y=968, size=SZ2, font="Virelai Sans",
           color="#B98A5E", justify="center")
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

d.finish("cookcli-V1R00")
