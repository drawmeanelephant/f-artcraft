#!/usr/bin/env python3
"""Gentleman's chest — field plate V1R00. Near-side three-quarter view of a
campaign-style bachelor chest: a mahogany two-part case. Upper half — a
fielded wardrobe door on the left and a column of four small drawers on the
right; lower half — two long deep drawers across the full width. Brass
corner strapping, flush ring pulls and a leather carry loop on the side;
field binoculars and a folded map on the top. Mahogany plate, campaign
mood. 1000x1000. Screen-space front elevation plus a (DX,-DY) recede for
the right side and top, like the other case pieces.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Gentleman's Chest — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#241008"   # warm dark, not black


def on_disc(x, y, pad):
    return math.hypot(x - PCX, y - PCY) <= PR - pad


def disc_x(y, side):
    return PCX + side * math.sqrt(PR ** 2 - (y - PCY) ** 2)


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
        {"offset": 0, "color": color, "opacity": o},
        {"offset": 1, "color": color, "opacity": 0}]}}


def smooth(pts, closed=True, k=1.0):
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


# --- geometry -------------------------------------------------------------------------
DX, DY = 46, 20                     # side face recedes up and to the right
L0, L1 = 314, 646                   # case fronts
T0, T1 = 304, 656                   # cornice overhang
Y_CT, Y_CB = 230, 256               # cornice top / bottom
Y_UB = 478                          # upper case bottom
Y_MB = 494                          # waist moulding bottom
Y_LB = 648                          # lower case bottom
Y_PB = 664                          # plinth bottom
Y_FT = 688                          # floor under the feet

for x, y in [(T1 + DX, Y_CT - DY), (T0 - 4, Y_CT), (L0 - 12, Y_FT), (L1 + DX + 12, Y_FT - DY)]:
    assert on_disc(x, y, 14), (x, y)

MH_FRONT = lin("#8A4A30", "#4A1E12", [L0, 240], [L1, 680])   # mahogany front
MH_SIDE = lin("#4A2014", "#28100A", [L1, 240], [L1 + DX, 680])
MH_TOP = lin("#A8603E", "#6E3018")
MH_DRAWER = lin("#96522F", "#5A2414")
BRASS = rad("#FFF0B0", "#DFAF4E", "#9A6C1E")
BRASS_FLAT = lin("#E2B656", "#A4741E")
BRASS_LINE = "#6E4C12"
LEATHER = lin("#6E4020", "#3A1E0C")

# --- backdrop + plate ------------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin("#12140C", "#070804", [0, 0], [0, 1000]), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#A08A58", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad("#5E4C30", "#3A2C18", "#181106"), stroke="#120D05", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8C49A", strokeWidth=3, opacity=24)
# tent canvas seams on the backdrop + a lantern glow low on the right
d.path(f"M{disc_x(150,-1):.1f},150 L400,470", "Tent seam L",
       fill=NONE, stroke="#8A7448", strokeWidth=3, opacity=16, cap="round")
d.path(f"M{disc_x(170,1):.1f},170 L610,480", "Tent seam R",
       fill=NONE, stroke="#8A7448", strokeWidth=3, opacity=14, cap="round")
d.shape("ellipse", "Lantern glow", x=560, y=520, width=340, height=300,
        fill=glow("#FFB86A", 0.20), stroke=NONE)
FY = 668
d.path(f"M{disc_x(FY,-1):.1f},{FY} L{disc_x(FY,1):.1f},{FY} A420,420 0 0 1 {disc_x(FY,-1):.1f},{FY} Z",
       "Floor", fill=lin("#423014", "#170E04", [0, FY], [0, 880]), stroke=NONE, opacity=85)
for i, y in enumerate([706, 752, 800]):
    d.path(f"M{disc_x(y,-1)+8:.1f},{y} L{disc_x(y,1)-8:.1f},{y}", f"Floorboard seam {i+1}",
           fill=NONE, stroke="#2A1C0A", strokeWidth=3, opacity=35, cap="round")
d.shape("ellipse", "Shadow", x=290, y=664, width=440, height=60,
        fill=glow("#0C0602", 0.72), stroke=NONE)
d.shape("ellipse", "Shadow core", x=330, y=680, width=390, height=28,
        fill=glow("#080401", 0.6), stroke=NONE)

# --- hardware helpers --------------------------------------------------------------------
def ring_pull(name, cx, cy):
    """Flush campaign pull: brass bezel, dark recess, a hanging ring."""
    d.shape("rectangle", f"{name} bezel", x=cx - 11, y=cy - 11, width=22, height=22,
            fill=BRASS, stroke=BRASS_LINE, strokeWidth=1.6)
    d.shape("ellipse", f"{name} recess", x=cx - 7.5, y=cy - 7.5, width=15, height=15,
            fill="#1A0C05", stroke=NONE)
    d.path(f"M{cx-5},{cy-3} A5.5,5.5 0 1 0 {cx+5},{cy-3} L{cx+5},{cy+2} "
           f"A6.5,6.5 0 0 1 {cx-5},{cy+2} Z", f"{name} ring",
           fill=NONE, stroke=lin("#FFE6A0", "#9A6A1C"), strokeWidth=2.6, cap="round")
    d.shape("ellipse", f"{name} pivot", x=cx - 3, y=cy - 7, width=6, height=6,
            fill="#FFF2C0", stroke=BRASS_LINE, strokeWidth=1.2)


def corner_plate(name, x, y, ax, ay):
    """Brass L at a case corner: 6pt arms of length w running +ax and +ay."""
    w = 24
    pts = [(x, y), (x + w * ax, y), (x + w * ax, y + 6 * ay),
           (x + 6 * ax, y + 6 * ay), (x + 6 * ax, y + w * ay), (x, y + w * ay)]
    d.path(poly(pts), name, fill=BRASS_FLAT, stroke=BRASS_LINE, strokeWidth=1.4)


def drawer(name, x0, y0, x1, y1, pulls=2):
    d.shape("rectangle", f"{name} recess", x=x0 - 3, y=y0 - 3, width=x1 - x0 + 6,
            height=y1 - y0 + 6, fill="#1A0A04", opacity=55, stroke=NONE)
    d.shape("rectangle", name, x=x0, y=y0, width=x1 - x0, height=y1 - y0,
            fill=lin("#96522F", "#542210", [x0, y0], [x1, y1]), stroke=INK, strokeWidth=3)
    d.path(f"M{x0+3},{y1-3} L{x0+3},{y0+3} L{x1-3},{y0+3}", f"{name} lip light",
           fill=NONE, stroke="#E8A870", strokeWidth=3, opacity=45, cap="round")
    d.path(f"M{x0+3},{y1-3} L{x1-3},{y1-3} L{x1-3},{y0+3}", f"{name} lip shade",
           fill=NONE, stroke="#180A04", strokeWidth=3, opacity=40, cap="round")
    h = y1 - y0
    for j in range(2 if h < 60 else 3):
        yy = y0 + h * (0.3 + 0.28 * j)
        amp = 3 + j
        d.path(f"M{x0+8},{yy:.1f} C{x0+(x1-x0)*0.3:.1f},{yy-amp:.1f} "
               f"{x0+(x1-x0)*0.6:.1f},{yy+amp:.1f} {x1-8},{yy-1:.1f}",
               f"{name} grain {j+1}", fill=NONE, stroke="#3A1408", strokeWidth=2.5,
               opacity=24, cap="round")
    cy = (y0 + y1) / 2
    for k, cx in enumerate([x0 + (x1 - x0) * f
                            for f in ([0.5] if pulls == 1 else [0.24, 0.76])]):
        ring_pull(f"{name} pull {k+1}", cx, cy)
    if pulls == 2:
        kx = (x0 + x1) / 2
        d.shape("ellipse", f"{name} escutcheon", x=kx - 6, y=cy - 12, width=12, height=18,
                fill=BRASS, stroke=BRASS_LINE, strokeWidth=1.6)
        d.path(f"M{kx},{cy-7} L{kx},{cy+2}", f"{name} keyhole", fill=NONE,
               stroke="#180C04", strokeWidth=2.6, cap="round")


# --- cornice and right side -----------------------------------------------------------------
d.path(poly([(T0, Y_CT), (T1, Y_CT), (T1 + DX, Y_CT - DY), (T0 + DX, Y_CT - DY)]),
       "Cornice top", fill=MH_TOP, stroke=INK, strokeWidth=4, join="round")
d.path(poly([(T0, Y_CT), (T1, Y_CT), (T1, Y_CB), (T0, Y_CB)]),
       "Cornice front", fill=lin("#7E3C24", "#4A1A0E", [0, Y_CT], [0, Y_CB]),
       stroke=INK, strokeWidth=3)
d.path(poly([(T1, Y_CT), (T1 + DX, Y_CT - DY), (T1 + DX, Y_CB - DY), (T1, Y_CB)]),
       "Cornice side", fill=lin("#5A2414", "#2E120A", [0, Y_CT - DY], [0, Y_CB - DY]),
       stroke=INK, strokeWidth=3)
d.path(f"M{T0+6},{Y_CT+8} L{T1-6},{Y_CT+8}", "Cornice bead light",
       fill=NONE, stroke="#E8A870", strokeWidth=2.5, opacity=45, cap="round")

# right side face of the whole case (behind the front face)
d.path(poly([(L1, Y_CB), (L1 + DX, Y_CB - DY), (L1 + DX, Y_LB - DY), (L1, Y_LB)]),
       "Case side", fill=MH_SIDE, stroke=INK, strokeWidth=4)
# waist seam continuing around the side
d.path(f"M{L1},{Y_UB} L{L1+DX},{Y_UB-DY}", "Side waist seam",
       fill=NONE, stroke="#140A04", strokeWidth=3, opacity=55)
# leather carry loop strapped to the side face
hx0, hy0 = L1 + 12, (Y_UB + Y_LB) / 2 - 60          # upper brass mount on the side
slope = -DY / DX
m0 = (hx0, hy0); m1 = (hx0 + 30, hy0 + 30 * slope)
d.path(f"M{m0[0]-4},{m0[1]-4} L{m0[0]+8},{m0[1]-4} L{m0[0]+8},{m0[1]+6} L{m0[0]-4},{m0[1]+6} Z",
       "Handle mount A", fill=BRASS_FLAT, stroke=BRASS_LINE, strokeWidth=1.4)
d.path(f"M{m1[0]-4},{m1[1]-4} L{m1[0]+8},{m1[1]-4} L{m1[0]+8},{m1[1]+6} L{m1[0]-4},{m1[1]+6} Z",
       "Handle mount B", fill=BRASS_FLAT, stroke=BRASS_LINE, strokeWidth=1.4)
d.path(smooth([m0, ((m0[0]+m1[0])/2 - 6, m0[1] + 34), m1], closed=False),
       "Handle loop", fill=NONE, stroke="#4A2A12", strokeWidth=7, cap="round")
d.path(smooth([m0, ((m0[0]+m1[0])/2 - 6, m0[1] + 32), m1], closed=False),
       "Handle loop light", fill=NONE, stroke="#8A5A2E", strokeWidth=2.5,
       opacity=60, cap="round")

# --- upper case front -------------------------------------------------------------------------
d.shape("rectangle", "Upper case front", x=L0, y=Y_CB, width=L1 - L0, height=Y_UB - Y_CB,
        fill=MH_FRONT, stroke=INK, strokeWidth=5)
# wardrobe door on the left: frame + fielded raised panel
DR0, DR1, DT, DB = L0 + 10, 446, Y_CB + 8, Y_UB - 8
d.shape("rectangle", "Wardrobe door", x=DR0, y=DT, width=DR1 - DR0, height=DB - DT,
        fill=lin("#8A4A30", "#542410", [DR0, DT], [DR1, DB]), stroke=INK, strokeWidth=3.5)
# fielded panel: bevel step + raised field
PB = 16
d.shape("rectangle", "Door bevel", x=DR0 + PB, y=DT + PB, width=DR1 - DR0 - 2 * PB,
        height=DB - DT - 2 * PB, fill=lin("#7A3C22", "#481C0E", [DR0, DT], [DR1, DB]),
        stroke=INK, strokeWidth=2.5)
d.shape("rectangle", "Door field", x=DR0 + PB + 9, y=DT + PB + 9,
        width=DR1 - DR0 - 2 * (PB + 9), height=DB - DT - 2 * (PB + 9),
        fill=lin("#9A5634", "#5C2614", [DR0, DT], [DR1, DB]), stroke=INK, strokeWidth=2)
d.path(f"M{DR0+PB+2},{DT+PB+2} L{DR1-PB-2},{DT+PB+2}", "Door bevel light",
       fill=NONE, stroke="#E8A870", strokeWidth=2.4, opacity=45, cap="round")
d.path(f"M{DR0+PB+2},{DB-PB-2} L{DR1-PB-2},{DB-PB-2}", "Door bevel shade",
       fill=NONE, stroke="#180A04", strokeWidth=2.4, opacity=45, cap="round")
# hinges on the door's left edge, ring pull + escutcheon on the right
for i, hy in enumerate([DT + 30, DB - 30]):
    d.shape("rectangle", f"Door hinge {i+1}", x=DR0 + 2, y=hy - 7, width=8, height=14,
            fill=BRASS_FLAT, stroke=BRASS_LINE, strokeWidth=1.4)
ring_pull("Door pull", DR1 - 20, (DT + DB) / 2)
d.shape("ellipse", "Door escutcheon", x=DR1 - 26, y=(DT + DB) / 2 - 34, width=12, height=18,
        fill=BRASS, stroke=BRASS_LINE, strokeWidth=1.6)
d.path(f"M{DR1-20},{(DT+DB)/2-29} L{DR1-20},{(DT+DB)/2-20}", "Door keyhole",
       fill=NONE, stroke="#180C04", strokeWidth=2.4, cap="round")

# right-hand column of four small drawers
CX0, CX1 = DR1 + 12, L1 - 10
row_y = Y_CB + 8
row_h = 46
for i in range(4):
    drawer(f"Upper drawer {i+1}", CX0, row_y, CX1, row_y + row_h, pulls=1)
    row_y += row_h + 5

# --- waist moulding ----------------------------------------------------------------------------
d.shape("rectangle", "Waist", x=L0 - 4, y=Y_UB, width=L1 - L0 + 8, height=Y_MB - Y_UB,
        fill=lin("#8A4A30", "#481C0E", [0, Y_UB], [0, Y_MB]), stroke=INK, strokeWidth=3)
d.path(f"M{L0-2},{Y_UB+3} L{L1+2},{Y_UB+3}", "Waist light",
       fill=NONE, stroke="#E8A870", strokeWidth=2.2, opacity=45, cap="round")

# --- lower case front ---------------------------------------------------------------------------
d.shape("rectangle", "Lower case front", x=L0, y=Y_MB, width=L1 - L0, height=Y_LB - Y_MB,
        fill=MH_FRONT, stroke=INK, strokeWidth=5)
ly = Y_MB + 10
drawer("Lower drawer top", L0 + 10, ly, L1 - 10, ly + 58)
ly += 58 + 7
drawer("Lower drawer deep", L0 + 10, ly, L1 - 10, ly + 68)

# --- brass corner strapping ----------------------------------------------------------------------
for i, (x, y, ax, ay) in enumerate([
        (L0 + 4, Y_CB + 4, 1, 1), (L1 - 4, Y_CB + 4, -1, 1),
        (L0 + 4, Y_UB - 4, 1, -1), (L1 - 4, Y_UB - 4, -1, -1),
        (L0 + 4, Y_MB + 4, 1, 1), (L1 - 4, Y_MB + 4, -1, 1),
        (L0 + 4, Y_LB - 4, 1, -1), (L1 - 4, Y_LB - 4, -1, -1)]):
    corner_plate(f"Corner strap {i+1}", x, y, ax, ay)

# --- plinth and bracket feet ----------------------------------------------------------------------
d.shape("rectangle", "Plinth", x=L0 - 2, y=Y_LB, width=L1 - L0 + 4, height=Y_PB - Y_LB,
        fill=lin("#4A1E12", "#28100A", [0, Y_LB], [0, Y_PB]), stroke=INK, strokeWidth=3)
for i, (fx, s) in enumerate([(L0 + 8, 1), (L1 - 8, -1)]):
    d.path(smooth([(fx, Y_PB - 2), (fx + s * 2, Y_FT - 18), (fx + s * 14, Y_FT - 8),
                   (fx + s * 26, Y_FT - 8), (fx + s * 30, Y_FT - 4),
                   (fx + s * 30, Y_FT - 16), (fx + s * 34, Y_PB - 2)]),
           f"Bracket foot {i+1}", fill=lin("#7E3C24", "#3A1408"), stroke=INK, strokeWidth=3)
# rear-right foot behind the side
rf = L1 + DX - 10
d.shape("ellipse", "Rear foot", x=rf - 14, y=Y_FT - DY - 10, width=34, height=14,
        fill=lin("#4A2014", "#28100A"), stroke=INK, strokeWidth=2.5)

# --- props on the cornice top -------------------------------------------------------------------
# folded map lying on the surface, left of centre
d.path(poly([(346, 220), (430, 215), (446, 226), (360, 231)]),
       "Map", fill=lin("#E8D8B0", "#C4AE84", [346, 215], [446, 231]),
       stroke="#6A5A38", strokeWidth=1.6, join="round")
for t in (0.35, 0.68):
    d.path(f"M{346 + 100 * t:.0f},{220 - 5 * t:.0f} L{362 + 100 * t:.0f},{231 - 5 * t:.0f}",
           f"Map fold {t}", fill=NONE, stroke="#8A7A55", strokeWidth=1.4, opacity=60)
# binoculars standing at the right end of the top: two joined barrels
for i, bx in enumerate((588, 610)):
    d.path(f"M{bx - 8},236 L{bx - 8},210 C{bx - 8},205 {bx + 8},205 {bx + 8},210 "
           f"L{bx + 8},236 Z", f"Bino barrel {i+1}",
           fill=lin("#3A3428", "#181410", [bx - 8, 0], [bx + 8, 0]),
           stroke=INK, strokeWidth=1.6)
    d.shape("ellipse", f"Bino objective {i+1}", x=bx - 7.5, y=232, width=15, height=7,
            fill=rad("#6A5230", "#2A2010"), stroke=INK, strokeWidth=1.2)
    d.shape("ellipse", f"Bino eyepiece {i+1}", x=bx - 4.5, y=203, width=9, height=5,
            fill="#0E0A06", stroke="#4A4028", strokeWidth=1.2)
d.shape("rectangle", "Bino bridge", x=586, y=214, width=26, height=6,
        fill="#241E14", stroke=INK, strokeWidth=1.2)
d.shape("ellipse", "Bino focus wheel", x=596, y=209, width=6, height=6,
        fill="#0E0A06", stroke="#4A4028", strokeWidth=1.0)

# --- extent check --------------------------------------------------------------------------------
for x, y in [(346, 215), (618, 203), (MID := (L0 + L1) / 2, Y_UB), (rf + 20, Y_FT - DY)]:
    assert on_disc(x, y, 12), (x, y)


# --- caption --------------------------------------------------------------------------------------
def find(node, oid):
    if isinstance(node, dict):
        if node.get("id") == oid and "bounds" in node:
            return node["bounds"]
        for v in node.values():
            r = find(v, oid)
            if r:
                return r
    elif isinstance(node, list):
        for v in node:
            r = find(v, oid)
            if r:
                return r
    return None


def caption(name, mats):
    n = d.text(name, "Name", x=500, y=934, size=56, font="Virelai Sans",
               color="#F0E4C8", justify="center")
    m = d.text(mats, "Materials", x=500, y=970, size=22, font="Virelai Sans",
               color="#CBB08A", justify="center")
    d.cmd("text.setStyle", "Name tracking", ids=[n["id"]], tracking=60)
    d.cmd("text.setStyle", "Materials tracking", ids=[m["id"]], tracking=260)
    doc = d.m.call("doc_inspect", {})
    for oid, label in ((n["id"], "name"), (m["id"], "materials")):
        b = find(doc, oid)
        nearest = (min(max(PCX, b["x"]), b["x"] + b["width"]),
                   min(max(PCY, b["y"]), b["y"] + b["height"]))
        clear = math.hypot(nearest[0] - PCX, nearest[1] - PCY) - (PR + 3)
        print("%s: %.0fx%.0f at y %.0f, clears rim by %.1f" %
              (label, b["width"], b["height"], b["y"], clear))
        assert clear > 0 and b["x"] >= 10 and b["x"] + b["width"] <= 990, label
        if label == "materials":
            assert b["width"] <= 760, b["width"]


caption("GENTLEMANS CHEST", "MAHOGANY · BRASS · LEATHER")
d.finish("gentlemans-chest-V1R00")
