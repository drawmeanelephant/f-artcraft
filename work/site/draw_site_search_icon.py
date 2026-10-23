#!/usr/bin/env python3
"""Search interface icon — site equity plate V1R00. The archive ⌕ as a real
magnifier: gold rim, translucent glass, a card-catalog card underneath that
appears magnified inside the lens, handle with a diamond collar rivet.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE
from vc import rot_rect_path

d = Draw()
d.new_doc("Search Icon — Site Equity", 1000, 1000)

INK = "#3A2418"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2A1C10"}, {"offset": 1, "color": "#100904"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F4E8CC"}, {"offset": 0.7, "color": "#D9BE92"},
    {"offset": 1, "color": "#A9845A"}]}}
GOLD_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F4CE72"}, {"offset": 0.6, "color": "#D9A03C"},
    {"offset": 1, "color": "#9C6218"}]}}
GLASS_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#FFF6E0", "opacity": 0.55},
    {"offset": 0.7, "color": "#F0E0BC", "opacity": 0.35},
    {"offset": 1, "color": "#D9BE92", "opacity": 0.5}]}}
CORE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#5E3A20"}, {"offset": 1, "color": "#2A1608"}]}}

PCX, PCY, PR = 500, 460, 420
def on_disc(x, y, pad):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

def diamond(cx, cy, r):
    return f"M{cx},{cy-r} L{cx+r},{cy} L{cx},{cy+r} L{cx-r},{cy} Z"

LX, LY, R_OUT, R_IN = 445, 380, 222, 168   # lens centre, rim outer edge, glass radius
R_MID = (R_OUT + R_IN) // 2                # 195, centre of the gold rim band

def in_glass(x, y, pad):
    return math.hypot(x - LX, y - LY) <= R_IN - pad

# --- backdrop + plate -------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#D9BE92", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#2E1C0E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F8F0DC", strokeWidth=3, opacity=40)
d.shape("ellipse", "Patina 1", x=640, y=600, width=230, height=130, fill="#B08C5E", opacity=18, stroke=NONE)
d.shape("ellipse", "Patina 2", x=150, y=140, width=220, height=120, fill="#B08C5E", opacity=16, stroke=NONE)
for i, (x, y, w) in enumerate([(200,330,7),(790,290,6),(170,540,8),(830,520,7),(250,730,6),
                               (740,720,8),(145,430,6),(855,410,7),(420,120,7),(600,130,6),
                               (300,170,5),(700,180,6),(330,810,5),(660,800,6),(500,105,5)]):
    assert on_disc(x, y, 12), (x, y)
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#8A6844", opacity=35, stroke=NONE)

# --- the card being searched (under the lens, peeking out lower-left) -------
CXr, CYr = 330, 565      # small card centre
CARD = rot_rect_path(CXr, CYr, 190, 118, -9)
d.path(CARD, "Catalog card", fill="#EEDCB4", stroke=INK, strokeWidth=4, opacity=55, join="round")
for j, (w_, off) in enumerate([(150, -26), (150, 0), (110, 26)]):
    p = rot_rect_path(CXr, CYr + off, w_, 9, -9)
    d.path(p, f"Card line {j+1}", fill="#8A6844", opacity=45, stroke=NONE)
# punched thumb-notch
d.shape("ellipse", "Card notch", x=CXr-14, y=CYr+38, width=28, height=12,
        fill="#C6A472", opacity=60, stroke=NONE)

# --- lens: drop shadow, glass, magnified card, rim ---------------------------
d.shape("ellipse", "Lens shadow", x=LX-R_OUT+10, y=LY-R_OUT+16, width=R_OUT*2, height=R_OUT*2,
        fill="#3A2418", opacity=18, stroke=NONE)
d.shape("ellipse", "Glass", x=LX-R_IN, y=LY-R_IN, width=R_IN*2, height=R_IN*2,
        fill=GLASS_GRAD, stroke=NONE)

# what the lens sees: the same card, magnified, fully inside the glass
MCX, MCY = 452, 412
d.path(rot_rect_path(MCX, MCY, 132, 86, -9), "Magnified card", fill="#F2E2BC",
       stroke=INK, strokeWidth=5, opacity=85, join="round")
for j, (w_, off) in enumerate([(108, -21), (108, 0), (84, 21)]):
    d.path(rot_rect_path(MCX, MCY + off, w_, 7, -9), f"Mag line {j+1}",
           fill="#7A5428", opacity=70, stroke=NONE)
d.shape("ellipse", "Mag notch", x=MCX-16, y=MCY+28, width=32, height=13,
        fill="#B8905E", opacity=60, stroke=NONE)
for px, py in [(MCX-66, MCY-43), (MCX+66, MCY+43), (MCX-66, MCY+43), (MCX+66, MCY-43)]:
    assert in_glass(px, py, 40), (px, py)

# glass shading: crescent highlight + rim inner shadow
d.path(f"M{LX-R_IN+34},{LY-40} A{R_IN-40},{R_IN-40} 0 0 1 {LX-20},{LY-R_IN+34}",
       "Glass highlight", fill=NONE, stroke="#FFFFFF", strokeWidth=18, opacity=45, cap="round")
d.shape("ellipse", "Glass lowlight", x=LX-R_IN+30, y=LY+R_IN-90, width=(R_IN-30)*2, height=44,
        fill="#A9845A", opacity=20, stroke=NONE)

# gold rim band over the glass edge, ink rings on both edges
d.shape("ellipse", "Rim", x=LX-R_MID, y=LY-R_MID, width=R_MID*2, height=R_MID*2,
        fill=NONE, stroke=GOLD_GRAD, strokeWidth=R_OUT-R_IN)
d.shape("ellipse", "Rim outer ink", x=LX-R_OUT, y=LY-R_OUT, width=R_OUT*2, height=R_OUT*2,
        fill=NONE, stroke=INK, strokeWidth=7)
d.shape("ellipse", "Rim inner ink", x=LX-R_IN, y=LY-R_IN, width=R_IN*2, height=R_IN*2,
        fill=NONE, stroke=INK, strokeWidth=5)

# --- handle: down-right at 40deg, collar + diamond rivet ----------------------
ANG = math.radians(40)
ux, uy = math.cos(ANG), math.sin(ANG)
hx0, hy0 = LX + (R_MID+8)*ux, LY + (R_MID+8)*uy      # at the rim
hx1, hy1 = hx0 + 150*ux, hy0 + 150*uy                # handle tip
assert on_disc(hx1, hy1, 30), (hx1, hy1)
# shadow then body then collar
d.path(f"M{hx0+8:.1f},{hy0+14:.1f} L{hx1+8:.1f},{hy1+14:.1f}", "Handle shadow",
       fill=NONE, stroke="#3A2418", strokeWidth=40, opacity=18, cap="round")
d.path(f"M{hx0:.1f},{hy0:.1f} L{hx1:.1f},{hy1:.1f}", "Handle",
       fill=NONE, stroke=GOLD_GRAD, strokeWidth=42, cap="round")
d.shape("ellipse", "Handle endcap", x=hx1-24, y=hy1-24, width=48, height=48,
        fill=GOLD_GRAD, stroke=INK, strokeWidth=6)
# handle outline: two side strokes for a clean edge
nx, ny = -uy, ux
d.path(f"M{hx0+nx*21:.1f},{hy0+ny*21:.1f} L{hx1+nx*21:.1f},{hy1+ny*21:.1f}", "Handle edge L",
       fill=NONE, stroke=INK, strokeWidth=6, cap="round")
d.path(f"M{hx0-nx*21:.1f},{hy0-ny*21:.1f} L{hx1-nx*21:.1f},{hy1-ny*21:.1f}", "Handle edge R",
       fill=NONE, stroke=INK, strokeWidth=6, cap="round")
# collar where handle meets rim
d.shape("ellipse", "Collar", x=hx0-34, y=hy0-34, width=68, height=68,
        fill=GOLD_GRAD, stroke=INK, strokeWidth=7)
d.path(diamond(hx0, hy0, 13), "Collar rivet", fill=CORE_GRAD, stroke="#F0C96A",
       strokeWidth=2.5, join="round")

# --- name + role ------------------------------------------------------------------
d.text("SEARCH ICON", "Name", x=500, y=930, size=58, font="Virelai Sans",
       color="#F0E2C4", justify="center")
d.text(" ".join("SEARCH THE ARCHIVE"), "Role", x=500, y=968, size=23, font="Virelai Sans",
       color="#C6A472", justify="center")

d.finish("site-search-icon-V1R00")
