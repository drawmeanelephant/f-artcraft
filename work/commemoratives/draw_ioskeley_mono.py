#!/usr/bin/env python3
"""IoskeleyMono — commemorative plate V1R00. The Letterform: one monumental
lowercase 'g', the typeface's signature glyph, cast like a bronze sculpture
standing on a plinth against a dark specimen card, a faint ruled baseline
grid glowing behind it. Warm grey card, foundry amber light. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("IoskeleyMono — Commemorative Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#241A0E"   # warm dark, never pure black

def on_disc(x, y, pad):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

def lin(c0, c1, start=None, end=None):
    g = {"kind": "linear", "stops": [{"offset": 0, "color": c0}, {"offset": 1, "color": c1}]}
    if start: g["start"], g["end"] = [round(v, 1) for v in start], [round(v, 1) for v in end]
    return {"gradient": g}

def rad(*stops):
    return {"gradient": {"kind": "radial", "stops": stops}}

BRONZE = lin("#F0C87A", "#8A5620", (400, 240), (620, 780))

# --- backdrop + plate (the dark specimen card) --------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin("#1C1913", "#0A0806", (500, 0), (500, 1000)), stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad({"offset": 0, "color": "#4A443A"}, {"offset": 0.68, "color": "#2C2721"},
                 {"offset": 1, "color": "#171310"}),
        stroke="#8A6428", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8C88A", strokeWidth=3, opacity=30)
# card vignette + patina
d.shape("ellipse", "Card vignette", x=150, y=110, width=700, height=700,
        fill=rad({"offset": 0.55, "color": "#000000", "opacity": 0},
                 {"offset": 1, "color": "#000000", "opacity": 0.30}), stroke=NONE)
for i, (x, y, w) in enumerate([(230,250,7),(760,300,6),(200,560,8),(790,570,7),(300,790,6),
                               (690,800,8),(410,150,6),(600,145,7)]):
    assert on_disc(x, y, 12)
    d.shape("ellipse", f"Patina {i+1}", x=x-w/2, y=y-w/2, width=w, height=w,
            fill="#8A7A5C", opacity=35, stroke=NONE)

# --- faint ruled baseline grid, glowing amber behind the glyph -----------------
# ascender / cap / x-height / baseline / descender rules
BASE_Y = 655
for i, (y, o, wdt) in enumerate([(250, 16, 1.5), (295, 20, 2), (395, 22, 2),
                                 (BASE_Y, 42, 3.5), (772, 16, 1.5)]):
    half = math.sqrt(PR**2 - (y - PCY)**2) - 26
    x0, x1 = PCX - half, PCX + half
    d.path(f"M{x0},{y} L{x1},{y}", f"Grid rule {i+1}", fill=NONE,
           stroke="#E8A83C", strokeWidth=wdt, opacity=o, cap="round")
    # small tick at each end of the baseline row
    if i == 3:
        for tx in (x0, x1):
            d.path(f"M{tx},{y-9} L{tx},{y+9}", f"Baseline tick {tx}", fill=NONE,
                   stroke="#E8A83C", strokeWidth=2.5, opacity=45, cap="round")
# grid glow pooling behind the glyph
d.shape("ellipse", "Grid glow", x=270, y=240, width=460, height=560,
        fill=rad({"offset": 0, "color": "#E8A83C", "opacity": 0.14},
                 {"offset": 1, "color": "#E8A83C", "opacity": 0}), stroke=NONE)
# corner crop ticks of the specimen card
for i, (x, y, dx, dy) in enumerate([(205, 300, 1, 1), (795, 300, -1, 1),
                                    (225, 758, 1, -1), (775, 758, -1, -1)]):
    d.path(f"M{x},{y+dy*16} L{x},{y} L{x+dx*16},{y}", f"Crop tick {i+1}",
           fill=NONE, stroke="#C8973F", strokeWidth=2.5, opacity=40, cap="round")

# --- plinth the letter stands on ------------------------------------------------
d.shape("ellipse", "Plinth shadow", x=310, y=806, width=380, height=50,
        fill=rad({"offset": 0, "color": "#000000", "opacity": 0.5},
                 {"offset": 1, "color": "#000000", "opacity": 0}), stroke=NONE)
d.path("M372,664 L628,664 L664,806 L336,806 Z", "Plinth",
       fill=lin("#8A5E28", "#3A2A12", (400, 664), (600, 806)),
       stroke="#3A2810", strokeWidth=4)
d.path("M372,664 L628,664 L638,690 L362,690 Z", "Plinth top",
       fill=lin("#E0B468", "#9A7038", (370, 664), (630, 690)),
       stroke="#3A2810", strokeWidth=3)

# --- the monumental 'g', cast in bronze -----------------------------------------
GLYPH, GSIZE, GX, GY = "g", 470, 500, BASE_Y
# cast shadow thrown forward-right onto grid and plinth
r_sh = d.text(GLYPH, "g cast shadow", x=GX + 10, y=GY + 14, size=GSIZE,
              font="Virelai Sans", color="#1E1408", justify="center")
d.cmd("object.setProps", "g shadow opacity", id=r_sh["id"], opacity=50)
# rim light on the back-left edge
r_rim = d.text(GLYPH, "g rim light", x=GX - 5, y=GY - 6, size=GSIZE,
               font="Virelai Sans", color="#FFE9B0", justify="center")
d.cmd("object.setProps", "g rim opacity", id=r_rim["id"], opacity=30)
# the letter itself, bronze-cast
r_g = d.text(GLYPH, "Letter g", x=GX, y=GY, size=GSIZE, font="Virelai Sans",
             color="#C08A3C", justify="center")
d.call("run_command", {"command": "paint.setFill",
                       "params": {"id": r_g["id"], "gradient": BRONZE["gradient"]}},
       "g bronze fill")
d.call("run_command", {"command": "stroke.set",
                       "params": {"id": r_g["id"], "color": "#4A2E10", "weight": 3.5}},
       "g edge")
# measure the glyph to place spec marks
def find(o, oid):
    if isinstance(o, dict):
        if o.get("id") == oid and "bounds" in o: return o
        o = list(o.values())
    if isinstance(o, list):
        for v in o:
            hit = find(v, oid)
            if hit: return hit
gb = find(d.call("inspect_document", {}, "inspect")["layers"], r_g["id"])["bounds"]
print("glyph bounds", {k: round(v) for k, v in gb.items()})
# side-bearing marks at the baseline, just clear of the glyph
for side, x in (("L", gb["x"] - 26), ("R", gb["x"] + gb["width"] + 26)):
    d.path(f"M{x},{BASE_Y-14} L{x},{BASE_Y+14}", f"SB mark {side}", fill=NONE,
           stroke="#E8A83C", strokeWidth=2.5, opacity=55, cap="round")
# foundry sparks drifting up from the plinth
for i, (x, y, w, o) in enumerate([(415,240,6,45),(585,210,5,40),(540,170,4,32),(455,190,5,38)]):
    assert on_disc(x, y, 10)
    d.shape("ellipse", f"Spark {i+1}", x=x, y=y, width=w, height=w,
            fill="#FFCA6E", opacity=o, stroke=NONE)

# --- name + role ---------------------------------------------------------------
d.text("IOSKELEYMONO", "Name", x=500, y=930, size=58, font="Virelai Sans",
       color="#F0E4CC", justify="center")
LINE2, SZ2, TRK = "PROGRAMMING TYPEFACE", 24, 300
r = d.text(LINE2, "Second line", x=500, y=968, size=SZ2, font="Virelai Sans",
           color="#C8A868", justify="center")
d.cmd("text.setStyle", "Second line tracking", id=r["id"], tracking=TRK)
b2 = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("second line bounds", {k: round(v) for k, v in b2.items()})
assert b2["width"] <= 760 and b2["x"] >= 100 and b2["y"] + b2["height"] <= 990, b2

d.finish("ioskeley-mono-V1R00")
