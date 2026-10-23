#!/usr/bin/env python3
"""Four-poster bed — field plate V1R00. Near-side three-quarter view of a
mahogany bed: four vase-and-ring turned posts carrying a tester frame, a sheer
canopy, swagged valance and tied-back curtains in translucent voile so the
night backdrop reads through. Headboard at the far (left) end, low footboard
at the near end. Dark plum plate. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Four-Poster Bed — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#2A1210"   # warm dark umber, not black

def on_disc(x, y, pad):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

def disc_x(y, side):
    return PCX + side * math.sqrt(PR**2 - (y - PCY)**2)

def lin(c0, c1, start=None, end=None, o0=None, o1=None):
    s0 = {"offset": 0, "color": c0}; s1 = {"offset": 1, "color": c1}
    if o0 is not None: s0["opacity"] = o0
    if o1 is not None: s1["opacity"] = o1
    g = {"kind": "linear", "stops": [s0, s1]}
    if start: g["start"], g["end"] = start, end
    return {"gradient": g}

def rad(*stops):
    n = len(stops) - 1
    return {"gradient": {"kind": "radial", "stops": [
        {"offset": round(i / n, 3), "color": c} for i, c in enumerate(stops)]}}

def glow(color, o):
    return {"gradient": {"kind": "radial", "stops": [
        {"offset": 0, "color": color, "opacity": o}, {"offset": 1, "color": color, "opacity": 0}]}}

def smooth(pts, closed=True, k=1.0):
    """Catmull-Rom through pts as cubic Beziers."""
    n = len(pts)
    s = "M%.1f,%.1f" % pts[0]
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        p0 = pts[(i - 1) % n] if (closed or i > 0) else pts[0]
        p1, p2 = pts[i], pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (closed or i + 2 < n) else pts[-1]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6 * k, p1[1] + (p2[1] - p0[1]) / 6 * k)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6 * k, p2[1] - (p3[1] - p1[1]) / 6 * k)
        s += " C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (c1 + c2 + p2)
    return s + (" Z" if closed else "")

def poly(pts):
    return "M" + " L".join("%.1f,%.1f" % p for p in pts) + " Z"

# --- geometry -------------------------------------------------------------------------------
FL, FR = 286, 658            # front posts (head end left, foot end right)
DX, DY = 76, 48              # depth recedes up and to the right
YF = 770                     # floor under the front posts
YT = 232                     # tester rail, front
YM = 548                     # mattress top, front edge
YR0, YR1 = 600, 650          # bed rail
for x, y in [(FL - 34, YF - 14), (FR + DX + 16, YT - DY - 26), (FL - 22, YT - 20), (FR + 34, YF - 14)]:
    assert on_disc(x, y, 20), (x, y)

VOILE = "#F4EEE4"
WOOD = lambda x0, x1: lin("#B0583A", "#4E1C12", [x0, 0], [x1, 0])

# --- backdrop + plate ---------------------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin("#1E1424", "#08050C", [0, 0], [0, 1000]), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876, fill="#9A86B8", opacity=7, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad("#4C3E66", "#30264A", "#18122A"), stroke=NONE)
# tall moonlit window on the far wall, softened to a glow
d.shape("ellipse", "Moon glow", x=360, y=70, width=440, height=440, fill=glow("#D8D4F4", 0.30), stroke=NONE)
WIN = [(452, 120), (640, 120), (640, 420), (452, 420)]
for x, y in WIN:
    assert on_disc(x, y, 30)
d.path(poly(WIN), "Window", fill=lin("#C8C6EE", "#7A70A8", [0, 120], [0, 420], 0.32, 0.08), stroke=NONE)
d.path("M546,120 L546,420 M452,270 L640,270", "Window bars", fill=NONE, stroke="#2A2040", strokeWidth=6, opacity=50)
# floor closed on the disc arc
FY = 712
d.path(f"M{disc_x(FY,-1):.1f},{FY} L{disc_x(FY,1):.1f},{FY} A420,420 0 0 1 {disc_x(FY,-1):.1f},{FY} Z",
       "Floor", fill=lin("#3A2C48", "#140E1E", [0, FY], [0, 880]), stroke=NONE, opacity=90)
d.path(f"M{disc_x(FY,-1):.1f},{FY} L{disc_x(FY,1):.1f},{FY}", "Skirting light",
       fill=NONE, stroke="#B8A8D8", strokeWidth=3, opacity=25, cap="round")
# moonlight laid on the floor through the window
POOL = [(480, 722), (632, 722), (664, 820), (456, 820)]
for x, y in POOL:
    assert on_disc(x, y, 16), (x, y)
d.path(poly(POOL), "Window pool", fill=lin("#D8D4F4", "#D8D4F4", [0, 722], [0, 820], 0.14, 0.02), stroke=NONE)
d.shape("ellipse", "Shadow", x=236, y=700, width=560, height=110, fill=glow("#06040A", 0.8), stroke=NONE)

# --- turned posts -------------------------------------------------------------------------------------
PROFILE = [(0.00, 1.25), (0.025, 0.80), (0.05, 1.15), (0.10, 1.40), (0.17, 1.30), (0.24, 0.80),
           (0.27, 1.10), (0.30, 0.75), (0.40, 0.70), (0.62, 0.62), (0.84, 0.55), (0.88, 0.85),
           (0.91, 0.60), (0.95, 0.68), (1.00, 0.70)]

def post(name, cx, ytop, ybot, yblock, w, dim=False):
    """Square block leg from ybot up to yblock, vase-and-ring turned shaft above it."""
    g = lin("#C8704C", "#3E160E", [cx - 2 * w, 0], [cx + 2 * w, 0]) if not dim else lin("#7A3A26", "#2E100A", [cx - 2 * w, 0], [cx + 2 * w, 0])
    bw = w * 1.5
    d.shape("rectangle", f"{name} block", x=cx - bw, y=yblock, width=2 * bw, height=ybot - yblock - 10,
            fill=g, stroke=INK, strokeWidth=3)
    d.path(f"M{cx-bw},{ybot-10} L{cx+bw},{ybot-10} L{cx+bw-3},{ybot} L{cx-bw+3},{ybot} Z", f"{name} foot",
           fill=g, stroke=INK, strokeWidth=3)
    d.path(f"M{cx-bw+4},{yblock+4} L{cx-bw+4},{ybot-14}", f"{name} block light", fill=NONE,
           stroke="#FFC8A4", strokeWidth=3, opacity=20 if dim else 40, cap="round")
    h = yblock - ytop
    right = [(cx + w * hw, yblock - h * t) for t, hw in PROFILE]
    left = [(cx - w * hw, yblock - h * t) for t, hw in reversed(PROFILE)]
    d.path(smooth(right + left, k=0.6), name, fill=g, stroke=INK, strokeWidth=3)
    # rings catch the light; reeding runs up the long taper
    for t, hw in PROFILE:
        if hw >= 1.1 or t in (0.88,):
            y = yblock - h * t
            d.path(f"M{cx - w*hw*0.8:.1f},{y:.1f} L{cx + w*hw*0.5:.1f},{y:.1f}", f"{name} ring {t}",
                   fill=NONE, stroke="#FFD0AC", strokeWidth=3, opacity=18 if dim else 38, cap="round")
    d.path(f"M{cx - w*0.25:.1f},{yblock - h*0.32:.1f} L{cx - w*0.2:.1f},{yblock - h*0.86:.1f}", f"{name} reed light",
           fill=NONE, stroke="#FFD0AC", strokeWidth=3, opacity=20 if dim else 42, cap="round")
    d.path(f"M{cx + w*0.3:.1f},{yblock - h*0.32:.1f} L{cx + w*0.25:.1f},{yblock - h*0.86:.1f}", f"{name} reed shade",
           fill=NONE, stroke="#1A0806", strokeWidth=3, opacity=35, cap="round")

def finial(name, cx, y, w):
    d.path(smooth([(cx - w * 0.6, y), (cx - w * 1.1, y - 10), (cx - w * 0.5, y - 20), (cx, y - 30),
                   (cx + w * 0.5, y - 20), (cx + w * 1.1, y - 10), (cx + w * 0.6, y)]),
           name, fill=lin("#D07A54", "#4E1C12", [cx - w, 0], [cx + w, 0]), stroke=INK, strokeWidth=3)

def swag_hem(x0, y0, x1, y1, n, drop):
    """Hem from (x1,y1) back to (x0,y0) as n downward swags."""
    s = ""
    for i in range(n, 0, -1):
        ax, ay = x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n
        bx, by = x0 + (x1 - x0) * (i - 1) / n, y0 + (y1 - y0) * (i - 1) / n
        s += f" Q{(ax + bx) / 2:.1f},{(ay + by) / 2 + drop * 2:.1f} {bx:.1f},{by:.1f}"
    return s

# --- back of the room inside the room ---------------------------------------------------------------
BL, BR = FL + DX, FR + DX
# sheer curtain hung along the back rail
d.path(f"M{BL},{YT-DY} L{BR},{YT-DY} L{BR},{YF-DY-30} C{BR-120},{YF-DY-18} {BL+120},{YF-DY-18} {BL},{YF-DY-30} Z",
       "Back sheer", fill=lin(VOILE, "#C8BEE0", [0, YT - DY], [0, YF - DY], 0.30, 0.14), stroke=NONE)
for i in range(1, 10):
    x = BL + (BR - BL) * i / 10
    d.path(f"M{x:.1f},{YT-DY+8} C{x+6:.1f},{YT+120} {x-6:.1f},{YT+300} {x+4:.1f},{YF-DY-28}", f"Back sheer fold {i}",
           fill=NONE, stroke="#FFFFFF", strokeWidth=4, opacity=12 if i % 2 else 7, cap="round")
post("Post back left", BL, YT - DY, YF - DY, YR1 - DY - 10, 9, dim=True)
post("Post back right", BR, YT - DY, YF - DY, YR1 - DY - 10, 9, dim=True)

# tester: back and side rails, then the canopy laid over the frame
def rail(name, p0, p1, h=12, dim=True):
    g = lin("#8A3E28", "#3A140C", [0, p0[1] - h], [0, p0[1] + h]) if dim else lin("#D07A54", "#5A2214", [0, p0[1] - h], [0, p0[1] + h])
    d.path(poly([(p0[0], p0[1] - h / 2), (p1[0], p1[1] - h / 2), (p1[0], p1[1] + h / 2), (p0[0], p0[1] + h / 2)]),
           name, fill=g, stroke=INK, strokeWidth=3)
rail("Tester back rail", (BL - 8, YT - DY), (BR + 8, YT - DY))
rail("Tester head rail", (FL, YT), (BL, YT - DY))
rail("Tester foot rail", (FR, YT), (BR, YT - DY))
d.path(f"M{FL},{YT} L{FR},{YT} L{BR},{YT-DY} L{BL},{YT-DY} Z", "Canopy",
       fill=lin(VOILE, "#D8CEEA", [FL, YT - DY], [FR, YT], 0.42, 0.24), stroke=NONE)
d.path(f"M{FL+30},{YT-6} C{FL+160},{YT-24} {FR-140},{YT-30} {BR-30},{YT-DY+6}", "Canopy sag light",
       fill=NONE, stroke="#FFFFFF", strokeWidth=5, opacity=22, cap="round")

# --- headboard at the far end, seen from inside ----------------------------------------------------
HT = 404
head = (f"M{FL},{YM} L{FL},{HT} C{FL+20},{HT-30} {FL+56},{HT-62} {BL},{HT-DY} "
        f"L{BL},{YM-DY} Z")
d.path(head, "Headboard", fill=lin("#A24C30", "#4E1C12", [FL, HT], [BL, YM]), stroke=INK, strokeWidth=4)
d.path(f"M{FL+12},{YM-14} L{FL+12},{HT+6} C{FL+28},{HT-18} {FL+54},{HT-44} {BL-12},{HT-DY+16} L{BL-12},{YM-DY-6} Z",
       "Headboard panel", fill=lin("#C46A48", "#6A2818", [FL, HT], [BL, YM]), stroke="#3A1810", strokeWidth=3, opacity=90)
d.path(f"M{FL+16},{HT+2} C{FL+30},{HT-20} {FL+54},{HT-44} {BL-14},{HT-DY+14}", "Headboard crest light",
       fill=NONE, stroke="#FFC8A4", strokeWidth=3, opacity=45, cap="round")

# --- mattress and bedding --------------------------------------------------------------------------------
MT = [(FL + 8, YM), (FR - 8, YM), (FR - 8 + DX, YM - DY), (FL + 8 + DX, YM - DY)]
d.path(poly([(FL, YR0), (FR, YR0), (BR, YR0 - DY), (BL, YR0 - DY)]), "Bed frame top",
       fill=lin("#6A2A1A", "#3A140C"), stroke=INK, strokeWidth=3)
d.path(poly(MT), "Mattress top", fill=lin("#F6F0E6", "#C8C0D8", [FL, YM - DY], [FR, YM]), stroke="#6A5E78", strokeWidth=3)
# pillows against the headboard, lying across the width
for i, (cx, cy) in enumerate([(FL + 70, YM - 34), (FL + 46, YM - 16)]):
    pts = [(cx - 34, cy + 22), (cx - 40, cy + 6), (cx - 6, cy - 22), (cx + 30, cy - 34),
           (cx + 44, cy - 20), (cx + 18, cy + 8), (cx - 10, cy + 26)]
    d.path(smooth(pts), f"Pillow {i+1}", fill=rad("#FFFFFF", "#EEE8F2", "#B8B0CC"), stroke="#6A5E78", strokeWidth=3)
    d.path(smooth([(cx - 24, cy + 6), (cx + 2, cy - 14), (cx + 26, cy - 22)], closed=False), f"Pillow {i+1} crease",
           fill=NONE, stroke="#8C82A4", strokeWidth=3, opacity=40, cap="round")
# coverlet: turned-down sheet band, then the quilt over the top and down the near side
CX0 = FL + 132
cov_top = [(CX0, YM), (FR - 8, YM), (FR - 8 + DX, YM - DY), (CX0 + DX, YM - DY)]
d.path(poly([(CX0 - 26, YM), (CX0 + 4, YM), (CX0 + 4 + DX, YM - DY), (CX0 - 26 + DX, YM - DY)]), "Turned sheet",
       fill=lin("#FFFFFF", "#D8D2E4"), stroke="#6A5E78", strokeWidth=3)
COV = lin("#8A6AA8", "#4A3468", [FL, YM - DY], [FR, YR1])
d.path(poly(cov_top), "Coverlet top", fill=COV, stroke="#2A1C3A", strokeWidth=3)
# side rail of the frame
d.shape("rectangle", "Bed rail", x=FL, y=YR0, width=FR - FL, height=YR1 - YR0,
        fill=lin("#B4603E", "#4E1C12", [0, YR0], [0, YR1]), stroke=INK, strokeWidth=4)
d.path(f"M{FL+6},{YR0+5} L{FR-6},{YR0+5}", "Bed rail bead", fill=NONE, stroke="#FFC8A4", strokeWidth=3, opacity=40, cap="round")
hem = "".join(f" Q{x - 22:.1f},{YR1 + 6 + (6 if j % 2 else 0)} {x - 44:.1f},{YR1 - 6}"
              for j, x in enumerate(range(FR - 8, CX0, -44)))
d.path(f"M{CX0},{YM} L{FR - 8},{YM} L{FR - 8},{YR1 - 6}{hem} L{CX0},{YR1 - 6} Z", "Coverlet drop",
       fill=lin("#7A5A98", "#3A2654", [0, YM], [0, YR1]), stroke="#2A1C3A", strokeWidth=3)
d.path(f"M{FL+8},{YM} L{CX0},{YM} L{CX0},{YR0} L{FL+8},{YR0} Z", "Mattress side",
       fill=lin("#EEE8F0", "#B0A8C4", [0, YM], [0, YR0]), stroke="#6A5E78", strokeWidth=3)
# quilting: diamond stitch lines in the coverlet
for i in range(1, 7):
    x = CX0 + (FR - 8 - CX0) * i / 7
    d.path(f"M{x:.1f},{YM + 2} L{x + DX * 0.96:.1f},{YM - DY + 2}", f"Quilt seam {i}",
           fill=NONE, stroke="#C8B4E0", strokeWidth=3, opacity=30, cap="round")
    d.path(f"M{x:.1f},{YM + 4} L{x:.1f},{YR1 - 10}", f"Quilt drop seam {i}",
           fill=NONE, stroke="#C8B4E0", strokeWidth=3, opacity=22, cap="round")
d.path(f"M{CX0 + 0.5 * DX},{YM - DY / 2} L{FR - 8 + 0.5 * DX},{YM - DY / 2}", "Quilt seam cross",
       fill=NONE, stroke="#C8B4E0", strokeWidth=3, opacity=26, cap="round")
d.path(f"M{CX0+4},{YM+2} L{FR-12},{YM+2}", "Coverlet edge light", fill=NONE, stroke="#E8DCF8",
       strokeWidth=4, opacity=45, cap="round")
d.path(f"M{CX0},{YM + 30} C{CX0 + 120},{YM + 42} {FR - 120},{YM + 40} {FR - 8},{YM + 28}", "Coverlet drop shade",
       fill=NONE, stroke="#1E1230", strokeWidth=8, opacity=22, cap="round")

# --- footboard at the near end, seen from outside ----------------------------------------------------------
FT = 512
foot = f"M{FR},{YR1} L{FR},{FT} C{FR+24},{FT-22} {FR+56},{FT-44} {BR},{FT-DY} L{BR},{YR1-DY} Z"
d.path(foot, "Footboard", fill=lin("#6E2C1C", "#3A140C", [FR, FT], [BR, YR1]), stroke=INK, strokeWidth=4)
d.path(f"M{FR+12},{YR1-14} L{FR+12},{FT+12} C{FR+30},{FT-6} {FR+52},{FT-24} {BR-12},{FT-DY+20} L{BR-12},{YR1-DY-6} Z",
       "Footboard panel", fill=lin("#8A3E28", "#4A1A10", [FR, FT], [BR, YR1]), stroke="#2A100A", strokeWidth=3, opacity=90)
d.path(f"M{FR+4},{FT+2} C{FR+26},{FT-18} {FR+56},{FT-40} {BR-4},{FT-DY+2}", "Footboard crest light",
       fill=NONE, stroke="#FFB890", strokeWidth=3, opacity=35, cap="round")

# --- front posts and the front tester rail ---------------------------------------------------------------------
post("Post front left", FL, YT, YF, YR1 - 10, 11)
post("Post front right", FR, YT, YF, YR1 - 10, 11)
rail("Tester front rail", (FL - 14, YT), (FR + 14, YT), h=16, dim=False)
d.path(f"M{FL-12},{YT-5} L{FR+12},{YT-5}", "Tester front rail light", fill=NONE, stroke="#FFD0AC",
       strokeWidth=3, opacity=50, cap="round")
for nm, (cx, y, w) in {"left": (FL, YT - 8, 12), "right": (FR, YT - 8, 12),
                       "back left": (BL, YT - DY - 6, 9), "back right": (BR, YT - DY - 6, 9)}.items():
    finial(f"Finial {nm}", cx, y, w)

# --- voile: valances and tied-back curtains ----------------------------------------------------------------------
VD = 34
d.path(f"M{FL},{YT+8} L{FR},{YT+8}" + swag_hem(FL, YT + 8, FR, YT + 8, 4, VD) + " Z", "Front valance",
       fill=lin(VOILE, "#D8CCEA", [0, YT], [0, YT + 3 * VD], 0.62, 0.34), stroke="#FFFFFF", strokeWidth=3, opacity=80)
d.path(f"M{FR},{YT+8} L{BR},{YT-DY+8}" + swag_hem(FR, YT + 8, BR, YT - DY + 8, 1, VD) + " Z", "Side valance",
       fill=lin(VOILE, "#B8ACD0", [0, YT - DY], [0, YT + 2 * VD], 0.45, 0.22), stroke="#FFFFFF", strokeWidth=3, opacity=70)
for i in range(4):
    x = FL + (FR - FL) * (i + 0.5) / 4
    d.path(f"M{x:.1f},{YT+12} L{x:.1f},{YT+8+VD*1.4:.1f}", f"Valance pleat {i+1}", fill=NONE,
           stroke="#FFFFFF", strokeWidth=3, opacity=30, cap="round")
for i, x in enumerate([FL + (FR - FL) * j / 4 for j in range(1, 4)]):
    d.path(f"M{x:.1f},{YT+10} L{x:.1f},{YT+24}", f"Tassel cord {i+1}", fill=NONE, stroke="#E2C470", strokeWidth=3, cap="round")
    d.path(f"M{x-5:.1f},{YT+24} L{x+5:.1f},{YT+24} L{x+7:.1f},{YT+40} L{x-7:.1f},{YT+40} Z", f"Tassel {i+1}",
           fill=lin("#F4DC8C", "#A8822C"), stroke="#6A5014", strokeWidth=2)

def curtain(name, px, sgn):
    """Gathered at the post at tie height, falling outside the post to the floor; sgn = side it opens toward."""
    tie = 470
    top0, top1 = px - sgn * 8, px + sgn * 64
    pts = (f"M{top0},{YT+10} L{top1},{YT+10} C{top1},{YT+120} {px+sgn*16},{tie-60} {px+sgn*10},{tie} "
           f"C{px+sgn*6},{tie+80} {px-sgn*10},{YF-80} {px-sgn*34},{YF-14} "
           f"Q{px-sgn*6},{YF-4} {px+sgn*22},{YF-16} "
           f"C{px+sgn*14},{YF-90} {px+sgn*4},{tie+60} {px-sgn*10},{tie} "
           f"C{px-sgn*14},{tie-80} {top0-sgn*6},{YT+100} {top0},{YT+10} Z")
    d.path(pts, name, fill=lin(VOILE, "#C8BCE0", [0, YT], [0, YF], 0.50, 0.30), stroke="#FFFFFF", strokeWidth=3, opacity=75)
    for j, f in enumerate([0.25, 0.55, 0.85]):
        xt = top0 + (top1 - top0) * f
        d.path(f"M{xt:.1f},{YT+14} C{xt:.1f},{YT+120} {px+sgn*8},{tie-50} {px+sgn*2},{tie-6}", f"{name} fold {j+1}",
               fill=NONE, stroke="#FFFFFF", strokeWidth=3, opacity=28, cap="round")
        d.path(f"M{px+sgn*2},{tie+8} C{px-sgn*(2+6*j)},{tie+120} {px-sgn*(6+10*j)},{YF-120} {px-sgn*(20-12*j)},{YF-16}",
               f"{name} fall fold {j+1}", fill=NONE, stroke="#FFFFFF", strokeWidth=3, opacity=24, cap="round")
    d.shape("ellipse", f"{name} tieback", x=px - 16, y=tie - 7, width=32, height=14,
            fill=lin("#F4DC8C", "#A8822C"), stroke="#6A5014", strokeWidth=2)
    d.path(f"M{px+sgn*12},{tie+4} L{px+sgn*18},{tie+34}", f"{name} tieback tassel", fill=NONE,
           stroke="#E2C470", strokeWidth=5, cap="round")

curtain("Curtain head", FL, 1)
curtain("Curtain foot", FR, -1)

# plate rim drawn last so everything inside closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840, fill=NONE, stroke="#0E0A16", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8CCF0", strokeWidth=3, opacity=24)

# --- name + second line -----------------------------------------------------------------------------------------
d.text("FOUR-POSTER BED", "Name", x=500, y=940, size=58, font="Virelai Sans", color="#E8E0F4", justify="center")
LINE2, SZ2, TRK = "MAHOGANY · LINEN · VOILE", 22, 200
r = d.text(LINE2, "Second line", x=500, y=975, size=SZ2, font="Virelai Sans", color="#B4A6CE", justify="center")
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

d.finish("four-poster-bed-V1R00")
