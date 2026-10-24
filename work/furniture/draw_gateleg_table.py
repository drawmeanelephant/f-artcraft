#!/usr/bin/env python3
"""Gateleg table — field plate V1R00. Both leaves up, the two gate frames
swung out beneath them on legs of their own; turned-oak balusters, a small
drawer in the apron, candlelit small-rooms mood on a deep green disc.
Near-side view, 1000x1000. House style: gradients + translucent shading,
never flat. Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Gateleg Table — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#241608"
DOWN = -90

def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

def _stops(stops):
    return [dict(offset=s[0], color=s[1], **({"opacity": s[2]} if len(s) > 2 else {})) for s in stops]

def lin(stops, angle=None):
    g = {"kind": "linear", "stops": _stops(stops)}
    if angle is not None:
        g["angle"] = angle
    return {"gradient": g}

def rad(stops):
    return {"gradient": {"kind": "radial", "stops": _stops(stops)}}

def ell(name, cx, cy, rx, ry, **kw):
    return d.shape("ellipse", name, x=round(cx - rx, 1), y=round(cy - ry, 1),
                   width=round(2 * rx, 1), height=round(2 * ry, 1), **kw)

def line(name, x0, y0, x1, y1, w, color, **kw):
    return d.path(f"M{x0:.1f},{y0:.1f} L{x1:.1f},{y1:.1f}", name, fill=NONE, stroke=color,
                  strokeWidth=w, cap="round", **kw)

def smooth_chain(pts):
    """Path through pts, quadratic-smoothed: vertices at midpoints, controls at pts."""
    seg = f"M{pts[0][0]:.1f},{pts[0][1]:.1f} "
    for i in range(1, len(pts) - 1):
        mx, my = (pts[i][0] + pts[i + 1][0]) / 2, (pts[i][1] + pts[i + 1][1]) / 2
        seg += f"Q{pts[i][0]:.1f},{pts[i][1]:.1f} {mx:.1f},{my:.1f} "
    seg += f"L{pts[-1][0]:.1f},{pts[-1][1]:.1f}"
    return seg

# wood gradients: honey oak lit from the left, warm dark to the right
OAK     = lin([(0, "#B8834C"), (0.4, "#8A5A2E"), (0.75, "#5C3A1C"), (1, "#3A2210")], 0)
OAK_TOP = lin([(0, "#DBA865"), (0.55, "#B07B42"), (1, "#6E4522")], DOWN)
OAK_DK  = lin([(0, "#5C3A1E"), (1, "#2A1708")], DOWN)
OAK_FAR = lin([(0, "#6E4A28"), (1, "#331D0C")], DOWN)

FIT = []
def note(*pts):
    FIT.extend(pts)

# --- backdrop + plate ------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin([(0, "#12100A"), (1, "#050403")], DOWN), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876, fill="#5A6E42", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad([(0, "#3E5C3C"), (0.55, "#2A4230"), (1, "#0E1C14")]),
        stroke="#060C08", strokeWidth=6)
d.shape("ellipse", "Plate vignette", x=80, y=40, width=840, height=840,
        fill=rad([(0, "#000000", 0), (0.72, "#000000", 0), (1, "#04100A", 0.5)]), stroke=NONE)
# candlelit warmth high on the plate, left of center
ell("Lamplight", 400, 210, 300, 200,
    fill=rad([(0, "#F4D08A", 0.22), (0.6, "#C89A58", 0.08), (1, "#C89A58", 0)]), stroke=NONE)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#BCCFA8", strokeWidth=3, opacity=30)
for i, (x, y, w) in enumerate([(210, 230, 6), (770, 250, 7), (172, 600, 6), (820, 575, 7),
                               (430, 108, 6), (630, 112, 7), (158, 420, 6), (848, 400, 6)]):
    ell(f"Plate fleck {i+1}", x, y, w / 2, w / 2, fill="#8AA078", opacity=30, stroke=NONE)

# --- floor + contact shadow --------------------------------------------------------
HZN = 748
hx = math.sqrt(PR ** 2 - (HZN - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{HZN} L{PCX + hx:.1f},{HZN} A420,420 0 0 1 {PCX - hx:.1f},{HZN} Z", "Floor",
       fill=lin([(0, "#241C10", 0.6), (1, "#0C0806", 0.9)], DOWN), stroke=NONE)
ell("Table shadow", 500, 750, 252, 30,
    fill=rad([(0, "#040604", 0.68), (0.6, "#040604", 0.32), (1, "#040604", 0)]), stroke=NONE)
note((252, 748), (748, 748))

# --- the table -----------------------------------------------------------------------
TX, TY, TRX, TRY = 500, 384, 255, 62     # open oval top
FX0, FX1 = 415, 585                     # fixed frame edges / leaf seams

# back legs first — shorter, darker, tucked under the rear of the frame
def turned_leg(name, cx, ytop, ybot, w, fill, sheen="#E8BC80", sheen_op=40):
    """Symmetric baluster silhouette; prof = (t, half-width multiplier)."""
    prof = [(0.00, 0.60), (0.05, 0.74), (0.12, 1.00), (0.22, 0.86), (0.30, 0.56),
            (0.38, 0.50), (0.46, 0.74), (0.53, 0.56), (0.66, 0.48), (0.80, 0.56),
            (0.90, 0.70), (1.00, 0.62)]
    h = ybot - ytop
    r_pts = [(cx + w * m, ytop + t * h) for t, m in prof]
    l_pts = [(2 * cx - x, y) for x, y in reversed(r_pts)]
    seg_l = ""
    for i in range(1, len(l_pts) - 1):
        mx, my = (l_pts[i][0] + l_pts[i + 1][0]) / 2, (l_pts[i][1] + l_pts[i + 1][1]) / 2
        seg_l += f"Q{l_pts[i][0]:.1f},{l_pts[i][1]:.1f} {mx:.1f},{my:.1f} "
    path = smooth_chain(r_pts) + f" L{l_pts[0][0]:.1f},{l_pts[0][1]:.1f} " + seg_l + " Z"
    g = {"gradient": {"kind": "linear",
                      "start": [round(cx - w, 1), 0], "end": [round(cx + w, 1), 0],
                      "stops": [{"offset": 0, "color": "#D49A5C"}, {"offset": 0.45, "color": "#8A5A2E"},
                                {"offset": 1, "color": "#38200E"}]}} if fill == "oak" else fill
    d.path(path, name, fill=g, stroke=INK, strokeWidth=2.5)
    if sheen:
        line(f"{name} sheen", cx - w * 0.5, ytop + h * 0.16, cx - w * 0.44, ybot - h * 0.12,
             max(w * 0.3, 3), sheen, opacity=sheen_op)
    note((cx - w, ybot), (cx + w, ybot), (cx - w, ytop), (cx + w, ytop))

# rear pair — partially hidden, drawn into shadow
turned_leg("Rear left leg", 452, 452, 690, 7, OAK_FAR, sheen=None)
turned_leg("Rear right leg", 548, 452, 690, 7, OAK_FAR, sheen=None)

# rear stretcher between the back legs
d.path("M452,640 L548,638 L548,649 L452,651 Z", "Rear stretcher", fill=OAK_FAR, stroke=INK, strokeWidth=2)

# side stretchers: front leg -> back leg, angled away
d.path("M420,652 L452,642 L452,653 L420,663 Z", "Left side stretcher", fill=OAK_DK, stroke=INK, strokeWidth=2)
d.path("M580,652 L548,642 L548,653 L580,663 Z", "Right side stretcher", fill=OAK_DK, stroke=INK, strokeWidth=2)

# front stretcher between the front frame legs
d.path("M424,648 L576,648 L576,660 L424,660 Z", "Front stretcher", fill=OAK_DK, stroke=INK, strokeWidth=2.5)
line("Front stretcher light", 428, 651, 572, 651, 3, "#D8A468", opacity=45)

# the two gates: top rail + bottom rail swung out under each leaf, pivoting at the frame edge
def gate(side):
    """side: -1 left, +1 right. Outer gate leg position and rail quads."""
    gx = 300 if side < 0 else 700
    fx = FX0 if side < 0 else FX1
    tag = "Left" if side < 0 else "Right"
    # top rail angles down toward the swung-out gate leg
    d.path(f"M{gx},{478} L{fx},{464} L{fx},{476} L{gx},{490} Z",
           f"{tag} gate top rail", fill=OAK, stroke=INK, strokeWidth=2)
    # bottom rail
    d.path(f"M{gx},{652} L{fx},{644} L{fx},{655} L{gx},{663} Z",
           f"{tag} gate bottom rail", fill=OAK_DK, stroke=INK, strokeWidth=2)
    # pivot pegs where the rails meet the frame
    ell(f"{tag} pivot hi", fx, 470, 4, 4, fill="#2A1708", stroke=NONE, opacity=85)
    ell(f"{tag} pivot lo", fx, 649, 4, 4, fill="#2A1708", stroke=NONE, opacity=85)

gate(-1)
gate(1)

# gate legs: the swung-out legs under the leaf tips, slightly nearer the viewer
turned_leg("Left gate leg", 300, 474, 746, 9, "oak")
turned_leg("Right gate leg", 700, 474, 746, 9, "oak")

# front frame legs
turned_leg("Front left leg", 425, 462, 738, 10, "oak")
turned_leg("Front right leg", 575, 462, 738, 10, "oak")

# apron + drawer under the fixed centre top; top edge band overlaps the apron's head
d.path("M412,446 L588,446 L588,488 L412,488 Z", "Apron", fill=OAK, stroke=INK, strokeWidth=2.5)
d.path("M436,462 L564,462 L564,484 L436,484 Z", "Drawer front", fill=OAK_TOP, stroke=INK, strokeWidth=2)
ell("Drawer knob", 500, 473, 5.5, 5.5, fill=rad([(0, "#3A2410"), (1, "#120A04")]), stroke="#0E0803", strokeWidth=1.2)
ell("Drawer knob glint", 498, 471, 1.6, 1.6, fill="#F0D8B0", opacity=90, stroke=NONE)
# apron bottom shade
d.path("M412,480 L588,480 L588,488 L412,488 Z", "Apron shade", fill="#1E1206", opacity=45, stroke=NONE)

# top edge band (thickness of the oval)
d.shape("ellipse", "Top edge band", x=TX - TRX, y=TY - TRY + 12, width=2 * TRX, height=2 * TRY,
        fill=lin([(0, "#A5713C"), (0.5, "#7A4E26"), (1, "#452812")], DOWN),
        stroke=INK, strokeWidth=3)
# leaf underside: shadow weight along the band's lower rim under each leaf
d.path(f"M{TX - 44},{TY + 73} A{TRX},{TRY} 0 0 1 {TX - 240},{TY + 33}",
       "Left leaf underside", fill=NONE, stroke="#140C04", strokeWidth=12, opacity=45, cap="round")
d.path(f"M{TX + 44},{TY + 73} A{TRX},{TRY} 0 0 0 {TX + 240},{TY + 33}",
       "Right leaf underside", fill=NONE, stroke="#140C04", strokeWidth=12, opacity=45, cap="round")
# lit top surface
d.shape("ellipse", "Top surface", x=TX - TRX + 5, y=TY - TRY - 2, width=2 * (TRX - 5), height=2 * (TRY - 3),
        fill=rad([(0, "#E4B878"), (0.5, "#C08A50"), (0.85, "#8A5A2C"), (1, "#5E3A1C")]),
        stroke="#3E2410", strokeWidth=2.5)
note((TX - TRX, TY), (TX + TRX, TY), (TX, TY - TRY), (TX, TY + TRY))

# leaf seams across the top at the frame edges, bowed with the surface
for x, bow in [(FX0, -5), (FX1, 5)]:
    t = (x - TX) / TRX
    ey = TRY * math.sqrt(1 - t * t)
    d.path(f"M{x},{TY - ey + 4:.0f} Q{x + bow},{TY} {x},{TY + ey - 6:.0f}",
           f"Leaf seam {'L' if x < TX else 'R'}", fill=NONE, stroke="#2A1808", strokeWidth=4.5, opacity=75)
    d.path(f"M{x - 4},{TY - ey + 8:.0f} Q{x + bow - 4},{TY} {x - 4},{TY + ey - 10:.0f}",
           f"Leaf seam {'L' if x < TX else 'R'} light", fill=NONE, stroke="#F0CE94",
           strokeWidth=2, opacity=40)

# grain arcs following the top's curvature + a warm sheen pool
for i, (dy, op) in enumerate([(-24, 22), (-6, 18), (14, 20), (30, 16)]):
    d.path(f"M{TX - TRX + 26},{TY + dy} Q{TX},{TY + dy - 26} {TX + TRX - 26},{TY + dy - 4}",
           f"Grain {i+1}", fill=NONE, stroke="#3A2410", strokeWidth=2, opacity=op)
ell("Top sheen", TX - 90, TY - 26, 130, 26,
    fill=rad([(0, "#FFE8BC", 0.5), (1, "#FFE8BC", 0)]), stroke=NONE)
# lit front-left rim of the top
d.path(f"M{TX - TRX + 12},{TY + 8} A{TRX - 8},{TRY - 6} 0 0 0 {TX - 60},{TY + TRY - 8}",
       "Top lit edge", fill=NONE, stroke="#F6DCA8", strokeWidth=5, cap="round", opacity=70)

# --- sanity: the whole piece inside the disc ------------------------------------------
worst = min(PR - math.hypot(x - PCX, y - PCY) for x, y in FIT)
print("min clearance to rim: %.1f" % worst)
assert worst > 24, worst

# --- rim + captions ---------------------------------------------------------------------
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840, fill=NONE, stroke="#050A06", strokeWidth=6)
d.shape("ellipse", "Plate inner edge", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C8D8B4", strokeWidth=3, opacity=26)

r1 = d.text("GATELEG TABLE", "Name", x=500, y=936, size=58, font="Virelai Sans",
            color="#F0E6CC", justify="center")
LINE2, SZ2, TRK = "TURNED OAK", 22, 300
r2 = d.text(LINE2, "Second line", x=500, y=972, size=SZ2, font="Virelai Sans",
            color="#B8C8A4", justify="center")
d.cmd("text.setStyle", "Second line tracking", id=r2["id"], tracking=TRK)

def find(o, oid):
    if isinstance(o, dict):
        if o.get("id") == oid and "bounds" in o: return o
        o = list(o.values())
    if isinstance(o, list):
        for v in o:
            hit = find(v, oid)
            if hit: return hit

layers = d.call("inspect_document", {}, "inspect")["layers"]
for label, rr in [("name", r1), ("second line", r2)]:
    b = find(layers, rr["id"])["bounds"]
    print(label, "bounds", {k: round(v) for k, v in b.items()})
    assert b["width"] <= 780 and b["x"] >= 96 and b["y"] + b["height"] <= 990, b

d.finish("gateleg-table-V1R00")
