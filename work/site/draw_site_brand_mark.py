#!/usr/bin/env python3
"""Site brand mark — site equity plate V1R00. The archive's ◈ rendered as a
faceted gem: gold gradient diamond, parchment inset panel, warm-ink core,
spark ticks at the four points. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Site Brand Mark — Site Equity", 1000, 1000)

INK = "#3A2418"   # warm umber, not black
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2A1C10"}, {"offset": 1, "color": "#100904"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F4E8CC"}, {"offset": 0.7, "color": "#D9BE92"},
    {"offset": 1, "color": "#A9845A"}]}}
MARK_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F4CE72"}, {"offset": 0.6, "color": "#D9A03C"},
    {"offset": 1, "color": "#9C6218"}]}}
FIELD_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E9D6AC"}, {"offset": 1, "color": "#C6A472"}]}}
CORE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#5E3A20"}, {"offset": 1, "color": "#2A1608"}]}}

PCX, PCY, PR = 500, 460, 420
def on_disc(x, y, pad):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

def diamond(cx, cy, r):
    return f"M{cx},{cy-r} L{cx+r},{cy} L{cx},{cy+r} L{cx-r},{cy} Z"

MX, MY, R = 500, 430, 205   # mark centre + circumradius

# --- backdrop + plate -------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#D9BE92", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#2E1C0E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F8F0DC", strokeWidth=3, opacity=40)
# patina blotches + flecks, all inside the disc
d.shape("ellipse", "Patina 1", x=190, y=640, width=240, height=130, fill="#B08C5E", opacity=20, stroke=NONE)
d.shape("ellipse", "Patina 2", x=600, y=150, width=220, height=120, fill="#B08C5E", opacity=18, stroke=NONE)
for i, (x, y, w) in enumerate([(200,330,7),(790,290,6),(170,540,8),(830,520,7),(250,730,6),
                               (740,720,8),(145,430,6),(855,410,7),(420,120,7),(600,130,6),
                               (300,170,5),(700,180,6),(330,810,5),(660,800,6),(500,105,5)]):
    assert on_disc(x, y, 12), (x, y)
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#8A6844", opacity=35, stroke=NONE)

# --- the mark ---------------------------------------------------------------
# glow + drop shadow
d.shape("ellipse", "Mark glow", x=MX-260, y=MY-260, width=520, height=520,
        fill="#F4CE72", opacity=14, stroke=NONE)
d.path(diamond(MX, MY+16, R+6), "Mark shadow", fill="#3A2418", opacity=18, stroke=NONE)
# outer diamond
d.path(diamond(MX, MY, R), "Mark outer", fill=MARK_GRAD, stroke=INK, strokeWidth=12, join="round")
# facet seams centre -> corners
for i, (ex, ey) in enumerate([(MX, MY-R), (MX+R, MY), (MX, MY+R), (MX-R, MY)]):
    d.path(f"M{MX},{MY} L{ex},{ey}", f"Facet {i+1}", fill=NONE,
           stroke="#7A4A14", strokeWidth=3, opacity=30)
# bevel: highlight the upper-left edges, shadow the lower-right
d.path(f"M{MX-R+26},{MY} L{MX},{MY-R+26}", "Bevel light", fill=NONE,
       stroke="#FFF2CC", strokeWidth=7, opacity=55, cap="round")
d.path(f"M{MX+R-26},{MY} L{MX},{MY+R-26}", "Bevel shade", fill=NONE,
       stroke="#6E3E10", strokeWidth=7, opacity=40, cap="round")
# inset field (the "white" interior of the ◈)
d.path(diamond(MX, MY, 118), "Mark field", fill=FIELD_GRAD, stroke=INK, strokeWidth=6, join="round")
# core diamond
d.path(diamond(MX, MY, 64), "Mark core", fill=CORE_GRAD, stroke="#F0C96A", strokeWidth=3, join="round")
d.shape("ellipse", "Core glint", x=MX-34, y=MY-40, width=18, height=12,
        fill="#FFE9B8", opacity=70, stroke=NONE)
# spark ticks past the four points
for i, (sx, sy) in enumerate([(MX, MY-R-46), (MX+R+46, MY), (MX, MY+R+46), (MX-R-46, MY)]):
    assert on_disc(sx, sy, 20), (sx, sy)
    d.path(f"M{sx-13},{sy} L{sx+13},{sy} M{sx},{sy-13} L{sx},{sy+13}", f"Spark {i+1}",
           fill=NONE, stroke="#F4CE72", strokeWidth=6, opacity=75, cap="round")

# --- name + role --------------------------------------------------------------
d.text("BRAND MARK", "Name", x=500, y=930, size=58, font="Virelai Sans",
       color="#F0E2C4", justify="center")
d.text(" ".join("FILED & FORGOTTEN"), "Role", x=500, y=968, size=23, font="Virelai Sans",
       color="#C6A472", justify="center")

d.finish("site-brand-mark-V1R00")
