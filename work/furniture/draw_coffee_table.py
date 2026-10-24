#!/usr/bin/env python3
"""Coffee table — field plate V1R00. Low and central: a rounded teak top on
four splayed peg legs with brass ferrules, a magazine shelf slung between
them, a mug and a small stack of magazines staging the surface. Warm
living-room dark on a burnt-umber disc, rug underfoot. Near-side view,
1000x1000. House style: gradients + translucent shading, never flat.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Coffee Table — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#1C0E04"
DOWN = -90

def _stops(stops):
    return [dict(offset=s[0], color=s[1], **({"opacity": s[2]} if len(s) > 2 else {})) for s in stops]

def lin(stops, angle=None):
    g = {"kind": "linear", "stops": _stops(stops)}
    if angle is not None:
        g["angle"] = angle
    return {"gradient": g}

def lin_pts(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [round(x0, 1), round(y0, 1)],
            "end": [round(x1, 1), round(y1, 1)], "stops": _stops(stops)}}

def rad(stops):
    return {"gradient": {"kind": "radial", "stops": _stops(stops)}}

def ell(name, cx, cy, rx, ry, **kw):
    return d.shape("ellipse", name, x=round(cx - rx, 1), y=round(cy - ry, 1),
                   width=round(2 * rx, 1), height=round(2 * ry, 1), **kw)

def line(name, x0, y0, x1, y1, w, color, **kw):
    return d.path(f"M{x0:.1f},{y0:.1f} L{x1:.1f},{y1:.1f}", name, fill=NONE, stroke=color,
                  strokeWidth=w, cap="round", **kw)

TEAK    = lin_pts(500, 462, 500, 560, (0, "#D89A58"), (0.5, "#B87E44"), (1, "#8A5426"))
TEAK_D  = lin([(0, "#6E4520"), (1, "#36200C")], DOWN)
TEAK_F  = lin([(0, "#54371A"), (1, "#2A1808")], DOWN)      # far/dimmer wood
BRASS   = lin([(0, "#E8BC62"), (0.6, "#A87E34"), (1, "#5C3E10")], DOWN)
GLAZE   = lin([(0, "#F0E4D2"), (0.6, "#C8AE94"), (1, "#8A6E52")], DOWN)

FIT = []
def note(*pts):
    FIT.extend(pts)

# --- backdrop + plate ------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin([(0, "#140E08"), (1, "#060403")], DOWN), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876, fill="#7A5A3E", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad([(0, "#5E3E26"), (0.55, "#3A2414"), (1, "#140A06")]),
        stroke="#0A0503", strokeWidth=6)
d.shape("ellipse", "Plate vignette", x=80, y=40, width=840, height=840,
        fill=rad([(0, "#000000", 0), (0.72, "#000000", 0), (1, "#0A0503", 0.5)]), stroke=NONE)
# evening lamp glow, upper left
ell("Lamplight", 385, 215, 310, 210,
    fill=rad([(0, "#F4CE8A", 0.24), (0.6, "#C89250", 0.08), (1, "#C89250", 0)]), stroke=NONE)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8C4A2", strokeWidth=3, opacity=30)
for i, (x, y, w) in enumerate([(214, 238, 6), (766, 254, 7), (176, 608, 6), (816, 582, 7),
                               (434, 111, 6), (622, 114, 7), (163, 423, 6), (840, 407, 6)]):
    ell(f"Plate fleck {i+1}", x, y, w / 2, w / 2, fill="#A8845C", opacity=30, stroke=NONE)

# --- floor + rug + contact shadow --------------------------------------------------
HZN = 762
hx = math.sqrt(PR ** 2 - (HZN - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{HZN} L{PCX + hx:.1f},{HZN} A420,420 0 0 1 {PCX - hx:.1f},{HZN} Z", "Floor",
       fill=lin([(0, "#241A10", 0.6), (1, "#0C0805", 0.92)], DOWN), stroke=NONE)
# low rug under the piece — a wide flat ellipse with a border ring
ell("Rug", 500, 772, 238, 34, fill="#6E3C28", opacity=40, stroke=NONE)
ell("Rug border", 500, 772, 214, 28, fill=NONE, stroke="#C89258", strokeWidth=3, opacity=28)
ell("Table shadow", 500, 762, 205, 22,
    fill=rad([(0, "#060404", 0.65), (0.6, "#060404", 0.3), (1, "#060404", 0)]), stroke=NONE)
note((262, 772), (738, 772))

# --- legs ---------------------------------------------------------------------------
# rear pair first: shorter read, dimmer wood, feet land higher (farther)
def peg_leg(tag, x_top, y_top, x_bot, y_bot, w_top, far=False):
    w_bot = w_top * 0.55
    fill = TEAK_F if far else TEAK_D
    d.path(f"M{x_top - w_top},{y_top} L{x_top + w_top},{y_top} "
           f"L{x_bot + w_bot},{y_bot - 16} L{x_bot - w_bot},{y_bot - 16} Z",
           tag, fill=fill, stroke=INK, strokeWidth=2.5)
    if not far:
        line(f"{tag} sheen", x_top - w_top * 0.45, y_top + 10, x_bot - w_bot * 0.45, y_bot - 24,
             3, "#D8A468", opacity=45)
    # brass ferrule cap
    d.path(f"M{x_bot - w_bot - 1.5},{y_bot - 16} L{x_bot + w_bot + 1.5},{y_bot - 16} "
           f"L{x_bot + w_bot - 1},{y_bot} L{x_bot - w_bot + 1},{y_bot} Z",
           f"{tag} ferrule", fill=BRASS, stroke="#2E1E08", strokeWidth=1.8)
    note((x_bot - w_bot - 4, y_bot), (x_bot + w_bot + 4, y_bot))

peg_leg("Rear left leg", 428, 576, 408, 700, 8, far=True)
peg_leg("Rear right leg", 572, 576, 592, 700, 8, far=True)

# magazine shelf slung between the legs
d.path("M376,660 L624,660 L612,690 L388,690 Z", "Magazine shelf", fill=TEAK_F,
       stroke=INK, strokeWidth=2.5)
line("Shelf light", 384, 663, 616, 663, 3, "#B8864C", opacity=50)
# two magazines on the shelf
d.path("M420,668 L512,664 L516,674 L424,678 Z", "Shelf mag 1", fill="#4E3A56",
       stroke=INK, strokeWidth=1.5, opacity=90)
d.path("M438,676 L540,672 L544,682 L442,686 Z", "Shelf mag 2", fill="#7A3A2E",
       stroke=INK, strokeWidth=1.5, opacity=90)

# apron under the top
d.path("M344,566 L656,566 L640,590 L360,590 Z", "Apron", fill=TEAK_D, stroke=INK, strokeWidth=2.5)

peg_leg("Front left leg", 372, 588, 342, 748, 9.5)
peg_leg("Front right leg", 628, 588, 660, 748, 9.5)

# --- the top --------------------------------------------------------------------------
TOP = "M310,558 L690,558 Q706,558 704,540 L660,470 Q656,462 644,462 " \
      "L356,462 Q344,462 340,470 L296,540 Q294,558 310,558 Z"
# edge band: same silhouette dropped 12pt
TOPB = "M310,570 L690,570 Q706,570 704,552 L660,482 Q656,474 644,474 " \
       "L356,474 Q344,474 340,482 L296,552 Q294,570 310,570 Z"
d.path(TOPB, "Top edge band", fill=TEAK_D, stroke=INK, strokeWidth=2.5)
d.path(TOP, "Top surface", fill=TEAK, stroke=INK, strokeWidth=3)
note((296, 540), (704, 540), (356, 462), (644, 462), (310, 558), (690, 558))
# grain streaks following the top's perspective
for i, (t, op) in enumerate([(0.25, 16), (0.45, 20), (0.65, 16)]):
    x_far = 356 + (644 - 356) * t
    x_near = 310 + (690 - 310) * t
    line(f"Top grain {i+1}", x_near - 14, 552, x_far + 10, 468, 2, "#5C3414", opacity=op)
ell("Top sheen", 440, 496, 130, 24, fill=rad([(0, "#FFE4B0", 0.4), (1, "#FFE4B0", 0)]), stroke=NONE)
# lit near edge
line("Top lit edge", 316, 556, 684, 556, 4, "#F0C88E", opacity=60)

# mug, left of centre on the top
MX, MY = 398, 522          # base centre
d.path(f"M{MX - 16},{MY - 30} L{MX + 16},{MY - 30} L{MX + 13},{MY} L{MX - 13},{MY} Z",
       "Mug body", fill=GLAZE, stroke=INK, strokeWidth=2)
ell("Mug rim", MX, MY - 30, 16, 6.5, fill="#E8DAC4", stroke=INK, strokeWidth=2)
ell("Coffee", MX, MY - 30, 11.5, 4, fill="#2A1406", stroke=NONE)
d.path(f"M{MX + 14},{MY - 26} Q{MX + 30},{MY - 24} {MX + 27},{MY - 14} "
       f"Q{MX + 24},{MY - 5} {MX + 12},{MY - 8}", "Mug handle",
       fill=NONE, stroke="#B89A7E", strokeWidth=5, cap="round")
d.path(f"M{MX - 3},{MY - 40} Q{MX + 5},{MY - 48} {MX - 1},{MY - 56}",
       "Steam", fill=NONE, stroke="#F4E8D4", strokeWidth=3, cap="round", opacity=30)
note((MX + 30, MY - 24), (MX, MY - 56))

# small magazine stack, right of centre
d.path("M540,516 L648,510 L652,519 L544,525 Z", "Top mag 1", fill="#3E4A5C",
       stroke=INK, strokeWidth=1.5)
d.path("M550,506 L646,501 L650,510 L554,515 Z", "Top mag 2", fill="#8A4A34",
       stroke=INK, strokeWidth=1.5)
line("Mag 2 masthead", 560, 507.5, 610, 505.5, 3, "#D8C8B0", opacity=60)

# --- sanity: the whole piece inside the disc ------------------------------------------
worst = min(PR - math.hypot(x - PCX, y - PCY) for x, y in FIT)
print("min clearance to rim: %.1f" % worst)
assert worst > 24, worst

# --- rim + captions ---------------------------------------------------------------------
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840, fill=NONE, stroke="#080403", strokeWidth=6)
d.shape("ellipse", "Plate inner edge", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#DCC8AA", strokeWidth=3, opacity=26)

r1 = d.text("COFFEE TABLE", "Name", x=500, y=936, size=58, font="Virelai Sans",
            color="#F2E4CC", justify="center")
LINE2, SZ2, TRK = "TEAK · BRASS", 22, 280
r2 = d.text(LINE2, "Second line", x=500, y=972, size=SZ2, font="Virelai Sans",
            color="#C8A884", justify="center")
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

d.finish("coffee-table-V1R00")
