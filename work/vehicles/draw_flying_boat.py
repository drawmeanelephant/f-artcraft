#!/usr/bin/env python3
"""Flying boat — field plate V1R00. Side profile of a four-engine flying boat
resting on dusk water, facing right: boat hull with a visible planing step,
sponson on the flank above the waterline, high wing carrying four nacelles with
translucent propeller discs, wingtip floats on struts, tail fin and stabiliser.
Warm lagoon sky over a dark teal sea; hull reflections in the swell.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420; waterline on y=650."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Flying Boat — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
WL = 650                      # waterline
INK = "#241A20"
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

SILVER = lin([(0, "#F2EDE4"), (0.45, "#C4BDB2"), (1, "#7E776E")], DOWN)
HULL_DARK = lin([(0, "#8E867C"), (0.5, "#5E5850"), (1, "#322E2A")], DOWN)
CHEAT = lin([(0, "#2E5E7E"), (1, "#123046")], DOWN)
WING_GRAD = lin([(0, "#D8D2C4"), (0.5, "#9A9284"), (1, "#565049")], DOWN)
GLASS = lin([(0, "#FFE2A0", 0.85), (0.6, "#F0B45E", 0.7), (1, "#C87E36", 0.55)], DOWN)
SKY_GLASS = lin([(0, "#D8ECF4", 0.8), (1, "#7EACCA", 0.55)], DOWN)
SEA = lin([(0, "#2A5A66"), (0.4, "#16333E"), (1, "#081219")], DOWN)
PROP = rad([(0, "#EAF4FA", 0.5), (0.55, "#C8D8E4", 0.28), (1, "#A8BCC8", 0.08)])

# --- backdrop + plate ---------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin([(0, "#131A28"), (1, "#07090F")], DOWN), stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880, fill="#C88A5A", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=lin([(0, "#22385A"), (0.4, "#4A6E96"), (0.62, "#A8887C"), (0.72, "#E0A468"), (1, "#4A3448")], DOWN),
        stroke="#0C121E", strokeWidth=6)
d.shape("ellipse", "Plate vignette", x=80, y=40, width=840, height=840,
        fill=rad([(0, "#000000", 0), (0.75, "#000000", 0), (1, "#0A0E1C", 0.5)]), stroke=NONE)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F0E0C8", strokeWidth=3, opacity=35)
# low sun sinking just off the bow, sitting on the horizon
ell("Sun glow", 716, 624, 150, 120, fill=rad([(0, "#FFD894", 0.55), (0.5, "#E8965A", 0.28), (1, "#E8965A", 0)]),
    stroke=NONE)
d.path("M706,612 A22,22 0 0 1 738,640 L700,640 Q694,624 706,612 Z", "Sun",
       fill=rad([(0, "#FFF2CC"), (1, "#F0AC5E")]), stroke=NONE, opacity=95)
# early stars high in the plate
for i, (x, y, r) in enumerate([(250, 150, 2.2), (340, 116, 1.8), (620, 108, 2), (760, 180, 1.8),
                               (190, 240, 1.6), (830, 300, 1.6)]):
    assert on_disc(x, y, 12)
    ell(f"Star {i+1}", x, y, r, r, fill="#FFF6E4", opacity=70, stroke=NONE)
# soft clouds, kept inside the rim
for i, (cx, cy, rx, ry, op) in enumerate([(300, 300, 120, 26, 30), (640, 240, 150, 30, 26),
                                         (420, 200, 90, 18, 22), (760, 360, 90, 20, 24)]):
    assert on_disc(cx - rx, cy, 8) and on_disc(cx + rx, cy, 8)
    ell(f"Cloud {i+1}", cx, cy, rx, ry, fill=lin([(0, "#F4C9A0"), (1, "#8A6E78")], DOWN),
        opacity=op, stroke=NONE)

# --- sea: band from the waterline, closing on the disc arc -------------------------------
sl, sr = chord(WL + 4)
d.path(f"M{sl:.1f},{WL + 4} L{sr:.1f},{WL + 4} A420,420 0 0 1 {sl:.1f},{WL + 4} Z", "Sea",
       fill=SEA, stroke=NONE)
line("Waterline light", sl + 8, WL + 3, sr - 8, WL + 3, 3, "#F4C88E", opacity=55)
line("Waterline dark", sl + 6, WL + 8, sr - 6, WL + 8, 4, "#0A1E28", opacity=60)
# swell lines
for i, (y, op) in enumerate([(678, 40), (706, 32), (740, 26), (782, 20), (830, 15)]):
    l, r_ = chord(y)
    line(f"Swell {i+1}", l + 20, y, r_ - 20, y, 3, "#7AA8B4", opacity=op)
# sun path glitter on the water
for i, (x, y, w) in enumerate([(700, 668, 60), (672, 690, 44), (716, 706, 52), (690, 730, 34),
                               (724, 752, 28), (700, 778, 20)]):
    assert on_disc(x - w / 2, y, 6) and on_disc(x + w / 2, y, 6)
    line(f"Glitter {i+1}", x - w / 2, y, x + w / 2, y, 4, "#FFD894", opacity=45)
# faint far-shore silhouette, left
l, r_ = chord(612)
d.path(f"M{l:.1f},{WL + 4} L{l:.1f},626 Q200,614 250,610 Q300,606 330,614 L330,{WL + 4} Z",
       "Far shore", fill="#1A2E44", opacity=55, stroke=NONE)

# --- tail (drawn before the hull so the deck overlaps the fin root) -----------------------
d.path("M338,552 L322,446 Q318,412 362,404 Q402,398 418,426 L430,552 Z",
       "Fin", fill=WING_GRAD, stroke=INK, strokeWidth=3)
d.path("M340,546 L330,448 Q330,424 362,416 L372,416 L356,546 Z", "Fin light",
       fill="#F4EDE0", opacity=35, stroke=NONE)
line("Rudder hinge", 372, 420, 396, 550, 3, "#4A4440", opacity=60)
# rudder hinge dots
for i, y in enumerate([442, 470, 498, 526]):
    ell(f"Hinge dot {i+1}", 374 + (y - 420) * 0.18, y, 2.6, 2.6, fill=INK, opacity=70, stroke=NONE)
# horizontal stabiliser, low on the fin root
d.path("M232,510 L400,502 Q414,502 414,512 Q414,522 400,522 L244,526 Q230,524 232,516 Z",
       "Stabiliser", fill=WING_GRAD, stroke=INK, strokeWidth=2.5)
line("Stabiliser sheen", 254, 506, 392, 504, 2.5, "#FFFFFF", opacity=30)
# stabiliser struts to fin
line("Stab strut front", 336, 518, 378, 550, 3, "#3E3A36", opacity=80)
line("Stab strut rear", 260, 522, 306, 550, 3, "#3E3A36", opacity=80)

# --- wingtip floats (struts first, floats after the sea line reads behind them) ------------
for side, x in [("rear", 236), ("front", 792)]:
    line(f"Float strut {side} a", x - 8, 416, x - 14, 488, 4, "#4A4440")
    line(f"Float strut {side} b", x + 8, 416, x + 14, 488, 4, "#4A4440")
    d.path(f"M{x - 36},498 Q{x - 38},486 {x - 20},482 L{x + 22},482 Q{x + 38},486 {x + 36},498 "
           f"Q{x + 34},508 {x + 18},510 L{x - 20},510 Q{x - 34},508 {x - 36},498 Z",
           f"Wingtip float {side}", fill=HULL_DARK, stroke=INK, strokeWidth=2.5)
    line(f"Float sheen {side}", x - 26, 489, x + 24, 489, 2.5, "#FFFFFF", opacity=30)

# --- high wing ---------------------------------------------------------------------------
d.path("M196,398 Q198,382 244,379 L758,379 Q818,381 830,397 Q834,404 824,409 "
       "Q816,414 780,414 L224,414 Q198,412 196,403 Z", "Wing",
       fill=WING_GRAD, stroke=INK, strokeWidth=3)
d.path("M210,396 Q216,386 250,384 L750,384 Q800,385 816,396 L816,400 Q800,392 750,391 "
       "L250,391 Q218,392 210,400 Z", "Wing top light", fill="#FFFFFF", opacity=28, stroke=NONE)
# panel ribs along the span
for i, x in enumerate(range(250, 800, 44)):
    line(f"Wing rib {i+1}", x, 381, x, 413, 2.5, "#3A3530", opacity=35)
# navigation lamps at the tips
ell("Tip lamp port", 204, 397, 5, 4, fill=rad([(0, "#FFB0A0"), (1, "#C02818")]), stroke=NONE)
ell("Tip lamp port glow", 204, 397, 12, 10, fill=rad([(0, "#FF7A60", 0.5), (1, "#FF7A60", 0)]), stroke=NONE)
ell("Tip lamp stbd", 826, 397, 5, 4, fill=rad([(0, "#C0F0B0"), (1, "#3A9A40")]), stroke=NONE)
ell("Tip lamp stbd glow", 826, 397, 12, 10, fill=rad([(0, "#8AE070", 0.5), (1, "#8AE070", 0)]), stroke=NONE)

# --- four nacelles on the wing, propellers as translucent discs -----------------------------
for i, cx in enumerate([320, 460, 600, 740]):
    d.path(f"M{cx - 30},404 Q{cx - 32},394 {cx - 20},392 L{cx + 20},392 Q{cx + 34},394 {cx + 36},410 "
           f"Q{cx + 36},424 {cx + 24},430 L{cx - 16},430 Q{cx - 30},424 {cx - 30},404 Z",
           f"Nacelle {i+1}", fill=SILVER, stroke=INK, strokeWidth=2.5)
    line(f"Nacelle {i+1} sheen", cx - 22, 398, cx + 20, 398, 2.5, "#FFFFFF", opacity=35)
    rect(f"Nacelle {i+1} exhaust", cx - 26, 424, 14, 7, fill="#2A2422", stroke=NONE, radius=3)
    # prop disc ahead of the nacelle, translucent so the sky reads through
    ell(f"Prop disc {i+1}", cx + 44, 411, 13, 56, fill=PROP, stroke="#E8F2F8", strokeWidth=1.5,
        opacity=80)
    ell(f"Prop arc {i+1}", cx + 44, 411, 8, 48, fill=NONE, stroke="#FFFFFF", strokeWidth=2,
        opacity=45)
    ell(f"Prop hub {i+1}", cx + 42, 411, 7, 9, fill=rad([(0, "#F0EAE0"), (1, "#6A6058")]),
        stroke=INK, strokeWidth=2)
    # spinner streak
    line(f"Prop streak {i+1}", cx + 44, 372, cx + 44, 388, 2.5, "#FFFFFF", opacity=40)

# --- hull: boat body, step, sponson ---------------------------------------------------------
# deck houses behind the hull line
rect("Deckhouse", 420, 506, 170, 46, fill=SILVER, stroke=INK, strokeWidth=2.5, radius=10)
rect("Deckhouse glass", 432, 514, 146, 16, fill=SKY_GLASS, stroke="#5A4E44", strokeWidth=2, radius=6)
for i, x in enumerate(range(440, 570, 26)):
    line(f"Deckhouse mullion {i+1}", x, 514, x, 530, 2.5, "#5A4E44", opacity=70)
line("Deckhouse sheen", 428, 510, 582, 510, 2.5, "#FFFFFF", opacity=30)
# windshield at the bow
d.path("M676,548 L686,520 Q690,512 700,514 L724,522 Q732,526 730,536 L724,548 Z",
       "Windshield", fill=SKY_GLASS, stroke=INK, strokeWidth=2.5)
line("Windshield mullion", 706, 518, 704, 546, 2.5, "#5A4E44", opacity=75)
line("Windshield glint", 692, 522, 718, 528, 3, "#FFFFFF", opacity=50)
# main hull path: deck from stern to bow, rounded bow, keel, one planing step, rising afterbody
d.path("M318,548 L744,548 Q770,554 768,590 Q764,634 706,660 L560,690 L544,690 "
       "L550,644 L452,632 Q356,622 322,604 Q304,576 318,548 Z", "Hull",
       fill=SILVER, stroke=INK, strokeWidth=3.5)
# lower hull shading + cheatline
d.path("M318,584 L766,584 Q760,632 706,658 L560,688 L546,688 L552,644 L452,630 "
       "Q356,620 324,602 Q314,592 318,584 Z", "Hull shade", fill=HULL_DARK, opacity=45, stroke=NONE)
d.path("M320,592 L762,592 L758,606 L330,606 Q324,600 320,592 Z", "Cheatline",
       fill=CHEAT, opacity=90, stroke=NONE)
line("Deck sheen", 330, 552, 736, 552, 3, "#FFFFFF", opacity=35)
# step edge highlight + shadow so the step reads
d.path("M560,690 L544,690 L550,644 L562,646 Z", "Step notch", fill="#241F1C", opacity=65, stroke=NONE)
line("Step face", 550, 644, 544, 690, 4, "#141010", opacity=70)
line("Step lip", 452, 632, 552, 644, 2.5, "#F4EDE0", opacity=40)
# keel reflection hint below the hull
d.path("M340,664 Q500,700 700,664 L706,670 Q500,708 336,672 Z", "Keel shadow",
       fill="#0E222C", opacity=28, stroke=NONE)
# portholes
for i, x in enumerate(range(380, 660, 46)):
    ell(f"Porthole {i+1}", x, 574, 7, 7, fill=GLASS, stroke="#4A3E32", strokeWidth=2)
    ell(f"Porthole {i+1} glint", x - 2, 572, 2, 2, fill="#FFFFFF", opacity=70, stroke=NONE)
# bow hatch + mooring cleat
d.path("M660,552 L720,552 L716,564 L662,564 Z", "Bow hatch", fill=NONE, stroke="#6A5E52",
       strokeWidth=2.5, opacity=80)
rect("Cleat", 730, 540, 18, 6, fill=INK, stroke=NONE, radius=3)
# sponson: short sea-wing on the flank, above the waterline, tapering to a tip
d.path("M430,600 Q500,584 590,592 Q644,598 664,616 Q672,628 654,632 L520,640 "
       "Q456,638 436,620 Q428,608 430,600 Z", "Sponson",
       fill=WING_GRAD, stroke=INK, strokeWidth=3)
line("Sponson sheen", 450, 602, 640, 612, 3, "#FFFFFF", opacity=30)
line("Sponson rib 1", 480, 592, 482, 634, 2.5, "#3A3530", opacity=35)
line("Sponson rib 2", 540, 590, 544, 636, 2.5, "#3A3530", opacity=35)
line("Sponson rib 3", 600, 594, 606, 632, 2.5, "#3A3530", opacity=35)
# struts from hull/deckhouse up to the wing
for i, (xa, xb) in enumerate([(452, 428), (510, 512), (568, 590)]):
    line(f"Wing strut {i+1}", xa, 508, xb, 416, 5, "#5A5248")
    line(f"Wing strut {i+1} light", xa - 2, 508, xb - 2, 416, 2, "#D8D0C0", opacity=50)

# --- water dressing over the hull base -------------------------------------------------------
# bow wash + stern wake, translucent foam
ell("Bow wash", 736, 652, 52, 12, fill=rad([(0, "#EAF6F8", 0.6), (1, "#EAF6F8", 0)]), stroke=NONE)
ell("Bow wash 2", 760, 664, 30, 8, fill=rad([(0, "#EAF6F8", 0.4), (1, "#EAF6F8", 0)]), stroke=NONE)
for i, (x, w, op) in enumerate([(300, 70, 45), (250, 90, 35), (200, 110, 26), (150, 120, 18)]):
    if on_disc(x - w / 2, 664, 4) and on_disc(x + w / 2, 664, 4):
        line(f"Wake {i+1}", x - w / 2, 664, x + w / 2, 664, 5, "#C8E4EA", opacity=op)
        line(f"Wake foam {i+1}", x - w / 2 + 8, 670, x + w / 2 - 8, 670, 3, "#FFFFFF", opacity=op)
# hull reflection, soft
ell("Hull reflection", 520, 700, 200, 20, fill=rad([(0, "#C4BDB2", 0.3), (1, "#C4BDB2", 0)]), stroke=NONE)
# mooring line off the bow cleat to a buoy in the water ahead
line("Mooring line", 736, 548, 812, 672, 3, "#2A2018", opacity=70)
ell("Mooring buoy", 814, 680, 12, 9, fill=rad([(0, "#F0B060"), (1, "#A8481E")]), stroke=INK, strokeWidth=2)

# --- sanity: everything stays inside the plate ----------------------------------------------
for x, y in [(196, 398), (830, 397), (318, 404), (232, 510), (764, 640), (814, 680),
             (320, 684), (664, 632), (236, 510), (792, 510)]:
    assert on_disc(x, y, 8), (x, y)

# --- name ------------------------------------------------------------------------------------
d.text("FLYING BOAT", "Name", x=500, y=940, size=58, font="Virelai Sans", color="#F0E6D2", justify="center")
LINE2, SZ2, TRK = "1938 · FOUR RADIAL ENGINES", 22, 200
r = d.text(LINE2, "Second line", x=500, y=975, size=SZ2, font="Virelai Sans", color="#C8B49A", justify="center")
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

d.finish("flying-boat-V1R00")
