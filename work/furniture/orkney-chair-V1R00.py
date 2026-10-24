#!/usr/bin/env python3
"""Orkney chair — field plate V1R00. Three-quarter view of the documented
Orkney form: a low timber chair whose tall back is coiled oat-straw bound in
horizontal courses, the back curving around the sitter's space with small
forward wings at the lower sides (no hood, drawer or tartan). Honey straw,
dark wood, cold North Atlantic blue disc. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Orkney Chair — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#33241A"
DOWN = -90                    # linear gradient angle: first stop at the top

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

def quad(p0, p1, p2, t):
    x = (1-t)**2*p0[0] + 2*(1-t)*t*p1[0] + t*t*p2[0]
    y = (1-t)**2*p0[1] + 2*(1-t)*t*p1[1] + t*t*p2[1]
    return (x, y)

STRAW = lin([(0, "#E4C27C"), (0.5, "#BE9A54"), (1, "#7E5C2C")], DOWN)
STRAW_SIDE = lin([(0, "#A8844A"), (1, "#5E421F")], DOWN)
WOOD = lin([(0, "#6B4E30"), (0.55, "#4A3220"), (1, "#2A1B10")], DOWN)
WOOD_DK = lin([(0, "#3A2818"), (1, "#1C120A")], DOWN)

# --- backdrop + plate -------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin([(0, "#0C141C"), (1, "#05080C")], DOWN), stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880, fill="#5A7A92", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=lin([(0, "#2A4054"), (0.5, "#3E5E74"), (0.78, "#5E7E8C"), (1, "#222C3A")], DOWN),
        stroke="#0A1018", strokeWidth=6)
d.shape("ellipse", "Plate vignette", x=80, y=40, width=840, height=840,
        fill=rad([(0, "#000000", 0), (0.75, "#000000", 0), (1, "#0A1018", 0.5)]), stroke=NONE)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C9D8E2", strokeWidth=3, opacity=35)
# cold pale glow, upper right — flat North Atlantic light
ell("Sky glow", 660, 250, 190, 150, fill=rad([(0, "#DDE8EC", 0.35), (0.55, "#A8BEC8", 0.14), (1, "#A8BEC8", 0)]),
    stroke=NONE)

# --- straw back: right return (thickness), front face, wrap wings -------------------
# right side return — the panel's edge seen in three-quarter
d.path("M592,318 Q602,444 612,592 L650,584 Q638,436 626,326 Q610,312 592,318 Z",
       "Back return", fill=STRAW_SIDE, stroke=INK, strokeWidth=3)
# front face: tapered panel, shallow arched top, sides curving down-out;
# bottom edge drops behind the seat slab so back and seat join
d.path("M388,606 Q382,460 398,336 Q497,304 592,318 Q602,444 612,592 Q500,612 388,606 Z",
       "Back front", fill=STRAW, stroke=INK, strokeWidth=3.5)
# low side walls: the straw back wraps forward along the seat's sides
d.path("M392,552 Q364,566 348,584 Q336,598 340,612 Q346,624 360,620 Q378,612 394,596 Z",
       "Left wing", fill=STRAW_SIDE, stroke=INK, strokeWidth=3)
d.path("M610,548 Q638,560 656,574 Q668,586 665,600 Q660,612 646,608 Q628,600 612,586 Z",
       "Right wing", fill=STRAW_SIDE, stroke=INK, strokeWidth=3)
# a couple of coil courses on each wing so they read as straw, not flippers
d.path("M384,566 Q366,576 354,590", "Left wing coil 1", fill=NONE, stroke="#6E4E22",
       strokeWidth=2.5, cap="round", opacity=70)
d.path("M388,584 Q374,594 362,606", "Left wing coil 2", fill=NONE, stroke="#96732F",
       strokeWidth=2.5, cap="round", opacity=60)
d.path("M618,562 Q638,572 652,584", "Right wing coil 1", fill=NONE, stroke="#6E4E22",
       strokeWidth=2.5, cap="round", opacity=70)
d.path("M620,580 Q634,590 646,600", "Right wing coil 2", fill=NONE, stroke="#96732F",
       strokeWidth=2.5, cap="round", opacity=60)

# coiled courses across the front face, following its arched top and curved sides
LEFT = [(398, 336), (383, 462), (388, 592)]
RIGHT = [(592, 318), (601, 448), (612, 578)]
for i in range(15):
    t = (i + 0.7) / 15.5
    lx, ly = quad(*[tuple(p) for p in LEFT], t)
    rx, ry = quad(*[tuple(p) for p in RIGHT], t)
    y = (ly + ry) / 2
    tone = "#96732F" if i % 2 == 0 else "#6E4E22"
    d.path(f"M{lx:.0f},{ly:.0f} Q{(lx + rx) / 2:.0f},{y + 9:.0f} {rx:.0f},{ry:.0f}",
           f"Course {i+1}", fill=NONE, stroke=tone, strokeWidth=3, cap="round", opacity=70)
# binding stitches: dashed verticals pinning the courses
for i, f in enumerate([0.28, 0.5, 0.72]):
    lx, ly = quad(*[tuple(p) for p in LEFT], 0.06)
    rx, ry = quad(*[tuple(p) for p in RIGHT], 0.06)
    x0 = lx + (rx - lx) * f
    lx2, ly2 = quad(*[tuple(p) for p in LEFT], 0.96)
    rx2, ry2 = quad(*[tuple(p) for p in RIGHT], 0.96)
    x1 = lx2 + (rx2 - lx2) * f
    d.path(f"M{x0:.0f},{(ly + ry) / 2 + 6:.0f} L{x1:.0f},{(ly2 + ry2) / 2 - 8:.0f}",
           f"Binding {i+1}", fill=NONE, stroke="#5C4020", strokeWidth=2.5,
           dash=[9, 9], cap="round", opacity=60)
# soft concave shading inside the side edges
d.path("M398,340 Q390,460 394,600 L404,600 Q399,462 406,344 Z", "Left edge shade",
       fill="#3A2810", opacity=25, stroke=NONE)
d.path("M586,322 Q598,448 608,588 L598,590 Q589,450 578,326 Z", "Right edge shade",
       fill="#3A2810", opacity=25, stroke=NONE)

# --- rear legs (behind seat) ----------------------------------------------------------
d.path("M396,600 L412,598 L406,692 L392,694 Z", "Rear left leg", fill=WOOD_DK, stroke=INK, strokeWidth=2.5)
d.path("M600,602 L616,600 L622,686 L608,688 Z", "Rear right leg", fill=WOOD_DK, stroke=INK, strokeWidth=2.5)

# --- seat slab -------------------------------------------------------------------------
d.path("M346,650 L634,632 L614,588 L390,602 Z", "Seat top",
       fill=lin([(0, "#7A5A38"), (0.6, "#54371F"), (1, "#382412")], DOWN), stroke=INK, strokeWidth=3)
d.path("M346,650 L634,632 L634,650 L346,668 Z", "Front apron", fill=WOOD, stroke=INK, strokeWidth=3)
d.path("M634,632 L614,588 L614,606 L634,650 Z", "Side apron", fill=WOOD_DK, stroke=INK, strokeWidth=2.5)

# --- ground shadow ----------------------------------------------------------------------
ell("Chair shadow", 496, 726, 205, 32, fill=rad([(0, "#05070A", 0.7), (0.6, "#05070A", 0.34), (1, "#05070A", 0)]),
    stroke=NONE)

# --- front legs + stretcher --------------------------------------------------------------
d.path("M348,668 L368,666 L354,730 L338,726 Z", "Front left leg", fill=WOOD, stroke=INK, strokeWidth=3)
d.path("M610,650 L630,648 L642,712 L626,714 Z", "Front right leg", fill=WOOD, stroke=INK, strokeWidth=3)
line("Front stretcher", 352, 700, 630, 690, 5, "#3A2818")
for i, (fx, fy) in enumerate([(346, 728), (634, 714)]):
    ell(f"Foot shadow {i+1}", fx, fy, 16, 5, fill="#05070A", opacity=45, stroke=NONE)

# --- sanity: everything stays inside the plate ---------------------------------------------
for x, y in [(388, 592), (398, 336), (497, 304), (592, 318), (650, 570), (331, 575),
             (671, 562), (338, 726), (642, 712), (392, 694), (496, 758), (291, 726), (701, 726)]:
    assert on_disc(x, y, 6), (x, y)

# --- name -----------------------------------------------------------------------------------
r1 = d.text("ORKNEY CHAIR", "Name", x=500, y=930, size=56, font="Virelai Sans",
            color="#F0E2C4", justify="center")
d.cmd("text.setStyle", "Name tracking", id=r1["id"], tracking=60)
LINE2, SZ2, TRK = "WOOD · STRAW", 22, 260
r2 = d.text(LINE2, "Second line", x=500, y=968, size=SZ2, font="Virelai Sans",
            color="#BCC8D2", justify="center")
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

d.finish("orkney-chair-V1R00")
