#!/usr/bin/env python3
"""Tugboat — field plate V1R00. Profile of a harbour tug working right, bow
to the right: squat hull with fat tire fenders, tall wheelhouse set well
forward, tall funnel abaft it, towing bitts aft with a tow line arcing off the
stern into the water, wake as translucent foam. Harbour skyline on the
horizon, a couple of gulls. 1000x1000. House style: gradients + translucent
shading, never flat fills. Plate = circle center (500,460) r420; water on
y=656."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Tugboat — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
WL = 656                      # waterline
INK = "#241C18"
DOWN = -90                    # linear gradient angle: first stop at the top

def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

def chord(y):
    h = math.sqrt(PR**2 - (y - PCY)**2)
    return PCX - h, PCX + h

def _stops(stops):
    return [dict(offset=s[0], color=s[1], **({"opacity": s[2]} if len(s) > 2 else {})) for s in stops]

def lin(stops, angle=None):
    g = {"kind": "linear", "stops": _stops(stops)}
    if angle is not None:
        g["angle"] = angle
    return {"gradient": g}

def rad(stops):
    return {"gradient": {"kind": "radial", "stops": _stops(stops)}}

def rect(name, x, y, w, h, **kw):
    return d.shape("rectangle", name, x=round(x, 1), y=round(y, 1), width=round(w, 1), height=round(h, 1), **kw)

def ell(name, cx, cy, rx, ry, **kw):
    return d.shape("ellipse", name, x=round(cx - rx, 1), y=round(cy - ry, 1),
                   width=round(2 * rx, 1), height=round(2 * ry, 1), **kw)

def line(name, x0, y0, x1, y1, w, color, **kw):
    return d.path(f"M{x0:.1f},{y0:.1f} L{x1:.1f},{y1:.1f}", name, fill=NONE, stroke=color,
                  strokeWidth=w, cap="round", **kw)

HULL = lin([(0, "#8A3A30"), (0.45, "#5E241E"), (1, "#2A0F0E")], DOWN)
HULL_TOP = lin([(0, "#3E4448"), (1, "#1C2024")], DOWN)
CABIN = lin([(0, "#F4EDE0"), (0.55, "#D8CCB6"), (1, "#A2947E")], DOWN)
STACK = lin([(0, "#B04A34"), (0.6, "#7E2E22"), (1, "#401410")], DOWN)
GLASS = lin([(0, "#CDE4EE", 0.85), (0.6, "#8FB4C8", 0.7), (1, "#5E8296", 0.55)], DOWN)
TIRE = rad([(0, "#4A4640"), (0.7, "#26221E"), (1, "#120F0C")])
SEA = lin([(0, "#345E66"), (0.4, "#1A3A44"), (1, "#0A161C")], DOWN)
WOOD = lin([(0, "#8A6A44"), (1, "#4A3420")], DOWN)

# --- backdrop + plate ---------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin([(0, "#101820"), (1, "#06090D")], DOWN), stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880, fill="#4E8A8A", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=lin([(0, "#26455E"), (0.45, "#4E7286"), (0.66, "#8A9690"), (0.78, "#C8A078"), (1, "#3A3450")], DOWN),
        stroke="#0B141C", strokeWidth=6)
d.shape("ellipse", "Plate vignette", x=80, y=40, width=840, height=840,
        fill=rad([(0, "#000000", 0), (0.75, "#000000", 0), (1, "#081018", 0.5)]), stroke=NONE)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8E4E0", strokeWidth=3, opacity=35)
# pale morning sun low over the harbour
ell("Sun glow", 240, 560, 160, 130, fill=rad([(0, "#FFE2A8", 0.5), (0.5, "#E8A860", 0.25), (1, "#E8A860", 0)]),
    stroke=NONE)
ell("Sun", 236, 566, 26, 26, fill=rad([(0, "#FFF4D4"), (1, "#F0B068")]), stroke=NONE, opacity=95)
# layered clouds
for i, (cx, cy, rx, ry, op) in enumerate([(330, 220, 130, 22, 30), (620, 190, 140, 26, 26),
                                         (760, 310, 80, 18, 24), (210, 350, 80, 16, 22)]):
    assert on_disc(cx - rx, cy, 8) and on_disc(cx + rx, cy, 8)
    ell(f"Cloud {i+1}", cx, cy, rx, ry, fill=lin([(0, "#E8D0B0"), (1, "#6A7080")], DOWN),
        opacity=op, stroke=NONE)
# harbour skyline on the horizon: cranes + sheds, both sides, behind the sea band
l, r_ = chord(616)
d.path(f"M{l:.1f},{WL + 4} L{l:.1f},640 L150,640 L150,600 L170,600 L170,568 L196,568 "
       f"L230,540 L238,544 L206,576 L206,640 L252,640 L252,616 L296,616 L296,640 L340,640 L340,{WL + 4} Z",
       "Harbour left", fill="#1A2836", opacity=70, stroke=NONE)
d.path(f"M{r_:.1f},{WL + 4} L{r_:.1f},630 L840,630 L840,592 L820,560 L812,562 L826,600 L782,600 "
       f"L782,632 L730,632 L730,{WL + 4} Z", "Harbour right", fill="#1A2836", opacity=70, stroke=NONE)
# crane silhouettes, thin but >=3pt
line("Crane jib L", 196, 568, 250, 530, 4, "#1A2836", opacity=70)
line("Crane leg L", 224, 540, 224, 640, 4, "#1A2836", opacity=70)
line("Crane jib R", 826, 566, 872, 540, 4, "#1A2836", opacity=70)
# gulls
d.path("M560,240 Q576,226 592,238 Q608,226 624,240", "Gull 1", fill=NONE, stroke="#2A3038",
       strokeWidth=3.5, cap="round", opacity=80)
d.path("M660,282 Q672,272 684,281 Q696,272 708,282", "Gull 2", fill=NONE, stroke="#2A3038",
       strokeWidth=3, cap="round", opacity=65)

# --- sea ---------------------------------------------------------------------------
sl, sr = chord(WL + 4)
d.path(f"M{sl:.1f},{WL + 4} L{sr:.1f},{WL + 4} A420,420 0 0 1 {sl:.1f},{WL + 4} Z", "Sea",
       fill=SEA, stroke=NONE)
line("Waterline light", sl + 8, WL + 3, sr - 8, WL + 3, 3, "#D8C9A0", opacity=50)
for i, (y, op) in enumerate([(682, 38), (710, 32), (744, 26), (786, 20), (836, 15)]):
    l, r_ = chord(y)
    line(f"Swell {i+1}", l + 20, y, r_ - 20, y, 3, "#6EA0A8", opacity=op)
# sun glitter left
for i, (x, y, w) in enumerate([(250, 676, 46), (228, 696, 34), (262, 714, 40), (240, 738, 26)]):
    assert on_disc(x - w / 2, y, 6) and on_disc(x + w / 2, y, 6)
    line(f"Glitter {i+1}", x - w / 2, y, x + w / 2, y, 4, "#FFD894", opacity=40)
# old pilings in the foreground right, bases ending on the disc arc
for i, (x, top, w) in enumerate([(760, 672, 14), (786, 684, 12), (810, 698, 10)]):
    bot = PCY + math.sqrt(PR**2 - (x + w / 2 - PCX)**2) - 6
    rect(f"Piling {i+1}", x, top, w, bot - top, fill=WOOD, stroke=INK, strokeWidth=2, opacity=90)
    d.path(f"M{x},{top + 4} L{x + w},{top + 4} L{x + w / 2},{top - 8} Z", f"Piling cap {i+1}",
           fill="#2A1E14", stroke=NONE)

# --- hull ------------------------------------------------------------------------------
# squat harbour-tug hull: bluff bow right, soft stern left, fender course at the waterline
d.path("M286,592 L676,592 Q714,598 718,640 Q716,670 676,686 L356,702 "
       "Q298,696 290,660 Q282,626 286,592 Z", "Hull", fill=HULL, stroke=INK, strokeWidth=3.5)
# boot-top + bulwark
d.path("M286,592 L676,592 Q712,598 716,632 L714,644 Q700,624 676,618 L290,618 L286,606 Z",
       "Bulwark", fill=HULL_TOP, stroke=INK, strokeWidth=2.5)
d.path("M288,606 L700,606 Q712,610 714,622 L292,624 Q286,616 288,606 Z", "Boot top",
       fill="#C8B89A", opacity=85, stroke=NONE)
line("Deck edge light", 292, 590, 670, 590, 3, "#F0D8B0", opacity=40)
# hull shading low
d.path("M296,650 Q500,690 700,650 L696,666 Q600,700 360,696 Q310,690 298,668 Z",
       "Hull low shade", fill="#1A0908", opacity=45, stroke=NONE)
# rubbing strake
d.path("M290,634 L710,634 L710,640 L292,640 Z", "Rubbing strake", fill="#18120E", stroke=NONE)
# portholes
for i, x in enumerate([360, 430, 610, 660]):
    ell(f"Porthole {i+1}", x, 668, 8, 8, fill=GLASS, stroke="#1C1410", strokeWidth=2.5)
    ell(f"Porthole {i+1} glint", x - 2, 666, 2, 2, fill="#FFFFFF", opacity=70, stroke=NONE)
# tire fenders hanging on the flank
for i, x in enumerate([330, 400, 470, 540, 610, 680]):
    line(f"Fender {i+1} line", x, 600, x + 2, 622, 3, "#1C1610", opacity=80)
    ell(f"Fender {i+1}", x + 2, 640, 15, 21, fill=TIRE, stroke=INK, strokeWidth=2.5)
    ell(f"Fender {i+1} hole", x + 2, 640, 5, 8, fill="#0A0806", stroke=NONE)
    d.path(f"M{x - 8},628 A13,16 0 0 1 {x + 2},620", f"Fender {i+1} glint",
           fill=NONE, stroke="#9A9284", strokeWidth=2.5, opacity=50, cap="round")

# --- towing bitts + tow line aft ----------------------------------------------------------
rect("Bitt base", 320, 574, 44, 20, fill=HULL_TOP, stroke=INK, strokeWidth=2, radius=4)
rect("Bitt L", 328, 560, 10, 18, fill="#1C1614", stroke=INK, strokeWidth=1.5, radius=3)
rect("Bitt R", 346, 560, 10, 18, fill="#1C1614", stroke=INK, strokeWidth=1.5, radius=3)
# tow line arcs off the stern quarter and dips to the water
d.path("M300,574 Q240,600 208,656 Q196,682 214,690", "Tow line", fill=NONE,
       stroke="#241C14", strokeWidth=4, cap="round")
ell("Tow line splash", 216, 692, 18, 7, fill=rad([(0, "#DCEEF0", 0.5), (1, "#DCEEF0", 0)]), stroke=NONE)

# --- funnel: tall stack abaft the wheelhouse -----------------------------------------------
d.path("M476,596 L478,430 Q478,414 496,412 L540,412 Q558,414 558,430 L560,596 Z",
       "Stack", fill=STACK, stroke=INK, strokeWidth=3)
rect("Stack cap band", 474, 406, 88, 22, fill=lin([(0, "#2E2A26"), (1, "#120E0C")], DOWN),
     stroke=INK, strokeWidth=2.5, radius=6)
line("Stack sheen", 490, 430, 488, 588, 4, "#FFD8B0", opacity=30)
line("Stack shade", 548, 434, 552, 590, 6, "#1A0806", opacity=40)
# band + mantle where the stack meets the deck
rect("Stack band", 476, 480, 84, 8, fill="#3A1008", opacity=70, stroke=NONE)
d.path("M470,580 L566,580 L560,596 L476,596 Z", "Stack mantle",
       fill=lin([(0, "#4A4640"), (1, "#1C1814")], DOWN), stroke=INK, strokeWidth=2)
# heat shimmer over the stack
for i, (x, op) in enumerate([(498, 30), (520, 26), (540, 22)]):
    d.path(f"M{x},400 Q{x - 6},376 {x + 2},352 Q{x + 8},330 {x},308", f"Heat haze {i+1}",
           fill=NONE, stroke="#D8C8B0", strokeWidth=3.5, opacity=op, cap="round")
# steam wisp
d.path("M500,404 Q470,380 486,352 Q500,326 480,306", "Steam wisp", fill=NONE,
       stroke="#E8E2D8", strokeWidth=5, opacity=35, cap="round")

# --- deckhouse + wheelhouse, set well forward ----------------------------------------------
# main cabin block
rect("Cabin", 566, 508, 108, 84, fill=CABIN, stroke=INK, strokeWidth=3, radius=8)
line("Cabin sheen", 574, 512, 666, 512, 3, "#FFFFFF", opacity=40)
for i, x in enumerate([584, 620, 652]):
    rect(f"Cabin window {i+1}", x, 540, 22, 26, fill=GLASS, stroke="#4A3E32", strokeWidth=2, radius=4)
    line(f"Cabin glint {i+1}", x + 4, 562, x + 16, 544, 2.5, "#FFFFFF", opacity=45)
# wheelhouse tier, tall with a wide window band
rect("Wheelhouse", 574, 452, 92, 58, fill=CABIN, stroke=INK, strokeWidth=3, radius=6)
rect("Wheelhouse windows", 582, 462, 76, 26, fill=GLASS, stroke="#4A3E32", strokeWidth=2.5, radius=4)
for i, x in enumerate([604, 628]):
    line(f"Wheel mullion {i+1}", x, 462, x, 488, 3, "#4A3E32", opacity=80)
line("Wheel sheen", 588, 466, 650, 466, 3, "#FFFFFF", opacity=50)
# visor over the window band + roof
d.path("M578,456 L654,456 L666,446 L566,446 Z", "Visor", fill=HULL_TOP, stroke=INK, strokeWidth=2)
rect("Wheelhouse roof", 570, 440, 100, 12, fill=HULL_TOP, stroke=INK, strokeWidth=2.5, radius=6)
# whistle + lamp on the roof
rect("Whistle", 594, 424, 8, 16, fill=lin([(0, "#E8C880"), (1, "#8A6428")], DOWN), stroke=INK,
     strokeWidth=1.5, radius=3)
ell("Roof lamp", 648, 434, 7, 8, fill=rad([(0, "#FFF6D8"), (1, "#E0A04A")]), stroke=INK, strokeWidth=2)
ell("Roof lamp glow", 648, 434, 16, 16, fill=rad([(0, "#FFE9B0", 0.5), (1, "#FFE9B0", 0)]), stroke=NONE)
# mast on the wheelhouse roof
line("Mast", 620, 442, 620, 372, 4, "#3A3026")
line("Mast yard", 596, 396, 644, 396, 3.5, "#3A3026")
line("Mast stay fore", 620, 376, 676, 592, 2.5, "#3A3026", opacity=70)
line("Mast stay aft", 620, 376, 556, 428, 2.5, "#3A3026", opacity=70)
ell("Masthead light", 620, 368, 6, 6, fill=rad([(0, "#FFF6D8"), (1, "#E8A84A")]), stroke=NONE)
ell("Masthead glow", 620, 368, 14, 14, fill=rad([(0, "#FFE9B0", 0.5), (1, "#FFE9B0", 0)]), stroke=NONE)
# name board, blank
rect("Name board", 590, 496, 62, 10, fill="#2A2018", stroke=INK, strokeWidth=1.5, radius=3)

# --- bow detail ----------------------------------------------------------------------------
# anchor + towing post forward
d.path("M690,600 Q700,594 706,604 L704,616 Q698,620 692,616 Z", "Anchor",
       fill="#1C1612", stroke=INK, strokeWidth=2, opacity=85)
rect("Bow post", 668, 566, 14, 28, fill=HULL_TOP, stroke=INK, strokeWidth=2, radius=4)
line("Bow rail", 660, 570, 706, 586, 3, "#241C14")

# --- water dressing -------------------------------------------------------------------------
# wake: translucent foam sheets peeling off the stern quarter
for i, (x, y, w, op) in enumerate([(280, 668, 90, 55), (236, 684, 110, 45), (196, 706, 120, 35),
                                   (170, 734, 110, 26)]):
    if on_disc(x - w / 2, y, 4) and on_disc(x + w / 2, y, 4):
        ell(f"Wake sheet {i+1}", x, y, w / 2, 7 + i, fill=rad([(0, "#EAF6F4", 0.6), (1, "#EAF6F4", 0)]),
            stroke=NONE, opacity=op)
        line(f"Wake crest {i+1}", x - w / 2 + 6, y - 4, x + w / 2 - 10, y - 4, 3, "#FFFFFF", opacity=op)
# bow wash
ell("Bow wash", 706, 660, 44, 12, fill=rad([(0, "#EAF6F4", 0.6), (1, "#EAF6F4", 0)]), stroke=NONE)
ell("Bow wash 2", 720, 672, 26, 8, fill=rad([(0, "#EAF6F4", 0.4), (1, "#EAF6F4", 0)]), stroke=NONE)
# hull reflection
ell("Hull reflection", 500, 716, 190, 18, fill=rad([(0, "#8A4638", 0.35), (1, "#8A4638", 0)]), stroke=NONE)
ell("Cabin reflection", 616, 700, 60, 10, fill=rad([(0, "#D8CCB6", 0.3), (1, "#D8CCB6", 0)]), stroke=NONE)

# --- sanity: everything stays inside the plate ----------------------------------------------
for x, y in [(286, 592), (718, 640), (356, 702), (620, 368), (540, 306), (214, 690),
             (760, 672), (150, 568), (815, 698)]:
    assert on_disc(x, y, 8), (x, y)

# --- name ------------------------------------------------------------------------------------
d.text("TUGBOAT", "Name", x=500, y=940, size=58, font="Virelai Sans", color="#EDE4D2", justify="center")
LINE2, SZ2, TRK = "1954 · DIESEL TWIN SCREW", 22, 200
r = d.text(LINE2, "Second line", x=500, y=975, size=SZ2, font="Virelai Sans", color="#C2AE94", justify="center")
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

d.finish("tugboat-V1R00")
