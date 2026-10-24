#!/usr/bin/env python3
"""banal — commemorative plate V1R00. The Heroic Sticky Note: a plain
yellow sticky note on a plain folder, rendered like a royal crest —
deliberately, defiantly ordinary, with one pencil line of Markdown on it.
Banal as heraldry: looks like Notes, files like Markdown. Yellow,
folder-kraft, and zero ambition beyond being correct. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("banal — Commemorative Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#241A0C"   # warm dark, never pure black

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

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin("#1A150C", "#060503", (500, 0), (500, 1000)), stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad({"offset": 0, "color": "#4A3E28"},
                 {"offset": 0.68, "color": "#2A2214"},
                 {"offset": 1, "color": "#120E07"}),
        stroke="#B08C46", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F0DDA8", strokeWidth=3, opacity=28)
# heraldic sunburst, faint, behind everything
for i in range(24):
    a = math.radians(i * 15 + 7)
    x0, y0 = 500 + 190 * math.cos(a), 460 + 190 * math.sin(a)
    x1, y1 = 500 + 400 * math.cos(a), 460 + 400 * math.sin(a)
    if on_disc(x1, y1, 6):
        d.path(f"M{x0:.0f},{y0:.0f} L{x1:.0f},{y1:.0f}", f"Ray {i+1}", fill=NONE,
               stroke="#F0DDA8", strokeWidth=3, opacity=8, cap="round")
# desk-patina flecks
for i, (x, y, w, o) in enumerate([(216,206,4,20),(792,200,5,22),(164,450,4,18),
                                  (846,424,4,20),(250,746,4,16),(736,780,5,18),
                                  (350,110,3,20),(652,106,4,20),(142,598,3,16),
                                  (858,588,4,18)]):
    assert on_disc(x, y, 12)
    d.shape("ellipse", f"Fleck {i+1}", x=x-w/2, y=y-w/2, width=w, height=w,
            fill="#F0DDA8", opacity=o, stroke=NONE)
# warm glow on the escutcheon
d.shape("ellipse", "Crest glow", x=310, y=200, width=380, height=420,
        fill=rad({"offset": 0, "color": "#F0DDA8", "opacity": 0.10},
                 {"offset": 1, "color": "#F0DDA8", "opacity": 0}), stroke=NONE)

# --- the plinth the crest rests on, closing on the disc's arc --------------------
d.path("M206.1,764 Q500,694 793.9,764 A420,420 0 0 1 206.1,764 Z", "Plinth",
       fill=lin("#221B10", "#0B0805", (500, 704), (500, 880)), stroke=NONE)
d.shape("ellipse", "Crest shadow", x=330, y=694, width=340, height=48,
        fill=rad({"offset": 0, "color": "#000000", "opacity": 0.55},
                 {"offset": 1, "color": "#000000", "opacity": 0}), stroke=NONE)

# --- laurel sprigs flanking the escutcheon ------------------------------------------
for side, sgn in (("L", -1), ("R", 1)):
    base_x, mid_x = 500 + sgn * 168, 500 + sgn * 208
    d.path(f"M{base_x},656 C{mid_x + sgn*18},580 {mid_x + sgn*14},480 "
           f"{base_x + sgn*6},392", f"Laurel stem {side}", fill=NONE,
           stroke="#7A6838", strokeWidth=4, cap="round")
    # leaflets along the stem, alternating outward/inward
    for j in range(6):
        t = j / 5.0
        lx = (1-t)**2 * base_x + 2*(1-t)*t * (mid_x+18) + t**2 * (base_x + sgn*6)
        ly = (1-t)**2 * 656 + 2*(1-t)*t * 480 + t**2 * 392
        for k, off in enumerate((-1, 1)):
            leaf_cx = lx + sgn * (12 + 14 * k * 0) * (1 if off > 0 else -0.7)
            leaf_cy = ly - 4 + off * 3
            ang = sgn * (38 - 10 * t) * off
            leaf = (f"M{leaf_cx},{leaf_cy} "
                    f"Q{leaf_cx + sgn*16},{leaf_cy - 8} {leaf_cx + sgn*26},{leaf_cy + off*10} "
                    f"Q{leaf_cx + sgn*12},{leaf_cy + off*10 + 8} {leaf_cx},{leaf_cy} Z")
            d.path(leaf, f"Leaf {side}{j}{k}", fill="#9A8548",
                   opacity=75 - j * 6, stroke="#5E4E28", strokeWidth=1.5)

# --- the folder: the escutcheon's field ---------------------------------------------
FX0, FY0, FX1, FY1 = 372, 398, 628, 668
d.path(f"M{FX0},{FY0+18} L{FX0},{FY1} L{FX1},{FY1} L{FX1},{FY0+18} "
       f"L{FX0+96},{FY0+18} L{FX0+76},{FY0} L{FX0},{FY0} Z", "Folder back",
       fill=lin("#C9A878", "#96764A", (FX0, FY0), (FX1, FY1)),
       stroke=INK, strokeWidth=4)
# papers peeking out of the folder
d.path(f"M{FX0+18},{FY0+24} L{FX1-24},{FY0+30} L{FX1-24},{FY0+44} "
       f"L{FX0+18},{FY0+38} Z", "Papers", fill=lin("#EFE8D8", "#C9BCA0",
       (FX0, FY0+24), (FX1, FY0+44)), stroke="#8A7A5A", strokeWidth=2)
# folder front flap
d.path(f"M{FX0-10},{FY0+52} L{FX1+10},{FY0+52} L{FX1-4},{FY1} L{FX0+4},{FY1} Z",
       "Folder front", fill=lin("#D8B888", "#A8815A", (FX0, FY0+52),
       (FX1, FY1), extra=[{"offset": 0.4, "color": "#E0C494"}]),
       stroke=INK, strokeWidth=4)
# kraft shading + crease
d.path(f"M{FX0-10},{FY0+52} L{FX1+10},{FY0+52}", "Flap edge", fill=NONE,
       stroke="#F0DCA8", strokeWidth=3, opacity=60, cap="round")
d.path(f"M{FX0+30},{FY0+90} L{FX0+22},{FY1-24}", "Crease", fill=NONE,
       stroke="#7A5E38", strokeWidth=3, opacity=30, cap="round")

# --- the crown above: plain, three-point, a little crooked ---------------------------
CX, CY = 500, 296
d.path(f"M{CX-58},{CY+30} L{CX-52},{CY-18} L{CX-22},{CY+8} L{CX},{CY-30} "
       f"L{CX+22},{CY+8} L{CX+52},{CY-18} L{CX+58},{CY+30} Z", "Crown",
       fill=lin("#E8C860", "#A8802E", (CX-58, CY-30), (CX+58, CY+30),
                extra=[{"offset": 0.5, "color": "#F5D978"}]),
       stroke=INK, strokeWidth=4)
d.path(f"M{CX-58},{CY+30} L{CX+58},{CY+30} L{CX+56},{CY+44} L{CX-56},{CY+44} Z",
       "Crown band", fill=lin("#D8B44E", "#96702A", (CX, CY+30), (CX, CY+44)),
       stroke=INK, strokeWidth=3)
for i, dx in enumerate((-52, 0, 52)):
    d.shape("ellipse", f"Crown jewel {i+1}", x=CX+dx-6, y=CY+14+(0 if dx else -14),
            width=12, height=12,
            fill=rad({"offset": 0, "color": "#FFF0C0"},
                     {"offset": 1, "color": "#C89840"}),
            stroke=INK, strokeWidth=2)
d.path(f"M{CX-40},{CY+36} L{CX+40},{CY+36}", "Band etch", fill=NONE,
       stroke="#7A5E20", strokeWidth=2, opacity=60)

# --- the sticky note: the charge, dead centre -----------------------------------------
NX, NY, NW, NH = 424, 356, 152, 152          # note box (slight -4deg tilt drawn in-path)
TILT = -3.5
tr = math.radians(TILT)
ncx, ncy = NX + NW/2, NY + NH/2
def rot(x, y):
    dx, dy = x - ncx, y - ncy
    return (ncx + dx*math.cos(tr) - dy*math.sin(tr),
            ncy + dx*math.sin(tr) + dy*math.cos(tr))
c = [rot(NX, NY), rot(NX+NW, NY), rot(NX+NW, NY+NH), rot(NX, NY+NH)]
# cast shadow on the folder
sc = [(x + 12, y + 14) for x, y in c]
d.path("M%.0f,%.0f L%.0f,%.0f L%.0f,%.0f L%.0f,%.0f Z" % tuple(sum(sc, ())),
       "Note shadow", fill="#241A0C", opacity=45, stroke=NONE)
# the note body, bottom-right corner left for the curl
b = [rot(NX, NY), rot(NX+NW, NY), rot(NX+NW-26, NY+NH), rot(NX, NY+NH)]
d.path("M%.0f,%.0f L%.0f,%.0f L%.0f,%.0f L%.0f,%.0f Z" % tuple(sum(b, ())),
       "Sticky note", fill=lin("#F5DC62", "#D8B83E", (ncx, NY), (ncx, NY+NH),
       extra=[{"offset": 0.55, "color": "#EFD24E"}]),
       stroke=INK, strokeWidth=3.5)
# peeled corner: the curl triangle + its shadow on the note
cc = [rot(NX+NW-26, NY+NH), rot(NX+NW, NY+NH), rot(NX+NW, NY+NH-30)]
d.path("M%.0f,%.0f L%.0f,%.0f L%.0f,%.0f Z" % tuple(sum(cc, ())),
       "Note curl", fill=lin("#C8A82E", "#8A7018", (ncx, NY+NH-30), (ncx, NY+NH)),
       stroke=INK, strokeWidth=3)
d.path("M%.0f,%.0f L%.0f,%.0f" % (cc[0] + cc[1]),
       "Curl shade", fill=NONE, stroke="#6E5814", strokeWidth=3, opacity=50)
# adhesive strip shading across the top
t0, t1 = rot(NX+6, NY), rot(NX+NW-6, NY)
d.path("M%.0f,%.0f L%.0f,%.0f" % (t0 + t1), "Adhesive", fill=NONE,
       stroke="#C8A82E", strokeWidth=8, opacity=45, cap="round")
# sheen
s0, s1 = rot(NX+14, NY+18), rot(NX+70, NY+18)
d.path("M%.0f,%.0f L%.0f,%.0f" % (s0 + s1), "Note sheen", fill=NONE,
       stroke="#FFF6C8", strokeWidth=10, opacity=35, cap="round")
# the one pencil line of Markdown — set in Source Sans 3 like all in-art text
ln0, ln1 = rot(NX+22, NY+62), rot(NX+130, NY+62)
d.text("- [ ] buy milk", "Markdown line", x=(ln0[0]+ln1[0])/2-38,
       y=(ln0[1]+ln1[1])/2, size=13, font="Source Sans 3",
       color="#5E5238", justify="center")
# a faint second ruled line — the note has lines, the note has one line
for j in (1, 2):
    p0, p1 = rot(NX+20, NY+62+j*26), rot(NX+NW-20, NY+62+j*26)
    d.path("M%.0f,%.0f L%.0f,%.0f" % (p0 + p1), f"Rule {j}", fill=NONE,
           stroke="#C8A82E", strokeWidth=2, opacity=50, cap="round")

# --- the pencil, resting on the folder's front -------------------------------------------
PX0, PY0 = 512, 636
d.shape("ellipse", "Pencil shadow", x=PX0-16, y=PY0+2, width=120, height=12,
        fill="#241A0C", opacity=40, stroke=NONE)
pd_ = [rot(PX0, PY0), rot(PX0+96, PY0-14)]
pencil_body = smooth([(pd_[0][0], pd_[0][1]-5), (pd_[1][0]-14, pd_[1][1]-7),
                      (pd_[1][0]-14, pd_[1][1]+3), (pd_[0][0], pd_[0][1]+5)],
                     closed=True, k=0.9)
d.path(pencil_body, "Pencil", fill=lin("#E8A83E", "#B8781E",
       (pd_[0][0], pd_[0][1]), (pd_[1][0], pd_[1][1])), stroke=INK, strokeWidth=2.5)
# tip: wood cone + graphite point
d.path(f"M{pd_[1][0]-14},{pd_[1][1]-7} L{pd_[1][0]+6},{pd_[1][1]-1} "
       f"L{pd_[1][0]-14},{pd_[1][1]+3} Z", "Pencil wood",
       fill=lin("#E8D8B0", "#C0A878", (pd_[1][0]-14, pd_[1][1]), (pd_[1][0]+6, pd_[1][1])), stroke=INK,
       strokeWidth=2)
d.path(f"M{pd_[1][0]+1},{pd_[1][1]-2.4} L{pd_[1][0]+6},{pd_[1][1]-1} "
       f"L{pd_[1][0]+1},{pd_[1][1]+0.6} Z", "Graphite", fill="#3A3226",
       stroke=NONE)
# eraser end
d.path(f"M{pd_[0][0]},{pd_[0][1]-5} L{pd_[0][0]-9},{pd_[0][1]-4} "
       f"L{pd_[0][0]-9},{pd_[0][1]+4} L{pd_[0][0]},{pd_[0][1]+5} Z",
       "Eraser", fill="#B86A6A", stroke=INK, strokeWidth=2)

# --- the motto ribbon under the folder --------------------------------------------------
RY = 704
d.path(f"M348,{RY} L652,{RY} L640,{RY+34} L360,{RY+34} Z", "Motto ribbon",
       fill=lin("#5E4E2E", "#3A3018", (348, RY), (652, RY+34)),
       stroke="#8A7648", strokeWidth=3)
d.path(f"M348,{RY} L318,{RY+6} L330,{RY+17} L318,{RY+28} L360,{RY+34} Z",
       "Ribbon fold L", fill="#2E2410", stroke="#8A7648", strokeWidth=2.5)
d.path(f"M652,{RY} L682,{RY+6} L670,{RY+17} L682,{RY+28} L640,{RY+34} Z",
       "Ribbon fold R", fill="#2E2410", stroke="#8A7648", strokeWidth=2.5)
d.text("BANALIS SED RECTA", "Motto", x=500, y=RY+24, size=14,
       font="Source Sans 3", color="#E8D8A8", justify="center")

# --- name + role ------------------------------------------------------------------
d.text("BANAL", "Name", x=500, y=930, size=60, font="Virelai Sans",
       color="#F0E4BC", justify="center")
LINE2, SZ2, TRK = "JUST A NOTES APP", 24, 320
r = d.text(LINE2, "Second line", x=500, y=968, size=SZ2, font="Virelai Sans",
           color="#B09A62", justify="center")
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

d.finish("banal-V1R00")
