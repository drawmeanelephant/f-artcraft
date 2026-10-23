#!/usr/bin/env python3
"""Paddle steamer — field plate V1R00. Profile of a side-wheel river steamer,
bow right: long low hull, the big paddle wheel half covered by its box at
mid-plate, two raked funnels flanking it, two open decks with rails and
rigging as fine lines, pilothouse forward, water at the hull line in a
river-gold sunset. 1000x1000. House style: gradients + translucent shading,
never flat fills. Plate = circle center (500,460) r420; waterline y=670."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Paddle Steamer — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
WL = 670                      # waterline
INK = "#2A1A10"
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

HULL = lin([(0, "#5E4630"), (0.5, "#3A2A1A"), (1, "#1C120A")], DOWN)
CABIN = lin([(0, "#FBF2DC"), (0.55, "#E4D4B4"), (1, "#B4A184")], DOWN)
STACK = lin([(0, "#E8B95E"), (0.5, "#B07830"), (1, "#5E3814")], DOWN)
STACK_BAND = lin([(0, "#3A2A20"), (1, "#17100C")], DOWN)
GLASS = lin([(0, "#FFE9B4", 0.9), (0.6, "#E8B45E", 0.75), (1, "#B0722E", 0.6)], DOWN)
BOX = lin([(0, "#9A5E3C"), (0.55, "#6E3E26"), (1, "#3A2012")], DOWN)
WHEEL = lin([(0, "#8A5E38"), (1, "#3A2410")], DOWN)
RIVER = lin([(0, "#7A5630"), (0.35, "#3E3320"), (1, "#141812")], DOWN)

# --- backdrop + plate ---------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin([(0, "#181008"), (1, "#0A0705")], DOWN), stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880, fill="#D89850", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=lin([(0, "#4A2840"), (0.35, "#8A4A3E"), (0.6, "#C88244"), (0.78, "#E8B866"), (1, "#4A3220")], DOWN),
        stroke="#140D08", strokeWidth=6)
d.shape("ellipse", "Plate vignette", x=80, y=40, width=840, height=840,
        fill=rad([(0, "#000000", 0), (0.75, "#000000", 0), (1, "#140A04", 0.5)]), stroke=NONE)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F2DCA8", strokeWidth=3, opacity=35)
# low river sun, dead astern
ell("Sun glow", 296, 596, 170, 140, fill=rad([(0, "#FFDE9A", 0.6), (0.5, "#E89A4E", 0.3), (1, "#E89A4E", 0)]),
    stroke=NONE)
ell("Sun", 292, 600, 30, 30, fill=rad([(0, "#FFF6D8"), (1, "#F0AC58")]), stroke=NONE, opacity=95)
# warm clouds
for i, (cx, cy, rx, ry, op) in enumerate([(380, 200, 150, 24, 32), (660, 170, 110, 18, 26),
                                         (740, 300, 90, 15, 24), (220, 330, 90, 16, 22)]):
    assert on_disc(cx - rx, cy, 8) and on_disc(cx + rx, cy, 8), (cx, cy)
    ell(f"Cloud {i+1}", cx, cy, rx, ry, fill=lin([(0, "#F0C896"), (1, "#8A5648")], DOWN),
        opacity=op, stroke=NONE)
# riverside willows, both banks, behind the river band
l, r_ = chord(630)
d.path(f"M{l:.1f},{WL + 4} L{l:.1f},636 Q160,616 190,584 Q196,600 210,594 Q204,566 236,560 "
       f"Q230,592 250,588 Q246,560 276,564 Q262,596 290,600 Q300,580 330,592 Q340,610 340,636 "
       f"L340,{WL + 4} Z", "Willow left", fill="#241A10", opacity=75, stroke=NONE)
d.path(f"M{r_:.1f},{WL + 4} L{r_:.1f},630 Q836,610 806,578 Q800,596 786,590 Q794,560 762,556 "
       f"Q768,588 748,586 Q754,558 722,562 Q736,592 710,598 Q700,580 668,592 Q660,610 660,634 "
       f"L660,{WL + 4} Z", "Willow right", fill="#241A10", opacity=75, stroke=NONE)

# --- river ----------------------------------------------------------------------------
sl, sr = chord(WL + 4)
d.path(f"M{sl:.1f},{WL + 4} L{sr:.1f},{WL + 4} A420,420 0 0 1 {sl:.1f},{WL + 4} Z", "River",
       fill=RIVER, stroke=NONE)
line("Waterline light", sl + 8, WL + 3, sr - 8, WL + 3, 3, "#F0C880", opacity=60)
for i, (y, op) in enumerate([(700, 40), (730, 32), (766, 26), (806, 20), (848, 15)]):
    l, r_ = chord(y)
    line(f"Swell {i+1}", l + 20, y, r_ - 20, y, 3, "#A87E46", opacity=op)
# gold glitter path under the sun
for i, (x, y, w) in enumerate([(290, 690, 70), (262, 712, 54), (306, 730, 60), (278, 754, 40),
                               (312, 782, 30), (300, 800, 18)]):
    assert on_disc(x - w / 2, y, 6) and on_disc(x + w / 2, y, 6)
    line(f"Glitter {i+1}", x - w / 2, y, x + w / 2, y, 4, "#FFD894", opacity=50)

# --- far-side paddle wheel, a shade darker, peeking above the box --------------------------
WCX, WCY, WR = 490, 636, 104
ell("Far wheel", WCX - 14, WCY - 6, WR * 0.94, WR * 0.94,
    fill=rad([(0, "#5E3E22"), (1, "#2A1A0C")]), stroke=INK, strokeWidth=2.5, opacity=85)

# --- hull --------------------------------------------------------------------------------
# long low river hull: raked bow right, soft counter stern left
d.path("M214,598 L760,598 Q806,604 816,640 Q818,668 780,690 L300,714 "
       "Q232,706 218,660 Q210,626 214,598 Z", "Hull", fill=HULL, stroke=INK, strokeWidth=3.5)
# guard + sheer line
d.path("M214,598 L760,598 Q802,604 812,634 L812,646 Q794,620 760,616 L218,616 Q212,608 214,598 Z",
       "Guard", fill=lin([(0, "#7A5636"), (1, "#3A2812")], DOWN), stroke=INK, strokeWidth=2)
line("Sheer light", 224, 596, 756, 596, 3, "#F0D09A", opacity=40)
# hull shading low + splash strake
d.path("M228,660 Q500,700 780,662 L774,676 Q500,720 300,706 Q244,700 232,676 Z",
       "Hull low shade", fill="#120A04", opacity=50, stroke=NONE)
# portholes along the hull
for i, x in enumerate(range(270, 770, 62)):
    ell(f"Porthole {i+1}", x, 644, 6.5, 6.5, fill=GLASS, stroke="#241608", strokeWidth=2)
# paddle-wheel sponson sweep: the hull swells around the wheel
d.path("M382,616 Q490,606 598,616 L596,630 Q490,620 384,630 Z", "Sponson",
       fill=lin([(0, "#8A6238"), (1, "#4A3016")], DOWN), stroke=INK, strokeWidth=2)

# --- paddle wheel at mid-plate --------------------------------------------------------------
# blades: 10 radial paddles, only the lower half fully visible
for k in range(10):
    a = k / 10 * 2 * math.pi + 0.31
    x0, y0 = WCX + 14 * math.cos(a), WCY + 14 * math.sin(a)
    x1, y1 = WCX + (WR - 8) * math.cos(a), WCY + (WR - 8) * math.sin(a)
    line(f"Blade arm {k+1}", x0, y0, x1, y1, 5, "#5E3E22")
    bx, by = WCX + (WR - 12) * math.cos(a), WCY + (WR - 12) * math.sin(a)
    # paddle board: wide slat perpendicular to the arm
    tx, ty = -(y1 - y0), (x1 - x0)
    tl = math.hypot(tx, ty)
    tx, ty = tx / tl * 22, ty / tl * 22
    d.path(f"M{bx - tx:.1f},{by - ty:.1f} L{bx + tx:.1f},{by + ty:.1f} "
           f"L{bx + tx + (x1 - x0) * 0.16:.1f},{by + ty + (y1 - y0) * 0.16:.1f} "
           f"L{bx - tx + (x1 - x0) * 0.16:.1f},{by - ty + (y1 - y0) * 0.16:.1f} Z",
           f"Paddle board {k+1}", fill=WHEEL, stroke=INK, strokeWidth=1.5)
# rims
ell("Wheel rim outer", WCX, WCY, WR - 4, WR - 4, fill=NONE, stroke="#6E4622", strokeWidth=4)
ell("Wheel rim inner", WCX, WCY, WR * 0.55, WR * 0.55, fill=NONE, stroke="#54341A", strokeWidth=3.5)
ell("Wheel hub", WCX, WCY, 16, 16, fill=rad([(0, "#D8B878"), (1, "#6E4622")]), stroke=INK, strokeWidth=2.5)
line("Hub key", WCX - 8, WCY, WCX + 8, WCY, 3, "#2A1A0C")
# spray flung off the wheel's trailing edge
for i, (dx, dy, r) in enumerate([(-96, 24, 8), (-112, 2, 6), (-84, 44, 5), (-120, 30, 4)]):
    ell(f"Spray {i+1}", WCX + dx, WCY + dy, r, r * 0.7, fill="#F4E8C8", opacity=60, stroke=NONE)
ell("Wheel froth", WCX - 60, WCY + 74, 60, 12, fill=rad([(0, "#F4EAD0", 0.65), (1, "#F4EAD0", 0)]),
    stroke=NONE)

# --- decks --------------------------------------------------------------------------------
# main saloon deck over the hull
rect("Saloon deck", 250, 542, 520, 56, fill=CABIN, stroke=INK, strokeWidth=3, radius=6)
for i, x in enumerate(range(268, 750, 40)):
    rect(f"Saloon window {i+1}", x, 556, 24, 26, fill=GLASS, stroke="#5A4020", strokeWidth=2, radius=3)
    line(f"Saloon mullion {i+1}", x + 12, 556, x + 12, 582, 2.5, "#5A4020", opacity=70)
line("Saloon deck sheen", 258, 546, 762, 546, 3, "#FFFFFF", opacity=45)
# promenade deck
rect("Promenade", 300, 490, 420, 50, fill=CABIN, stroke=INK, strokeWidth=3, radius=6)
for i, x in enumerate(range(316, 700, 38)):
    ell(f"Promenade arch {i+1}", x, 508, 9, 12, fill=GLASS, stroke="#5A4020", strokeWidth=2)
line("Promenade sheen", 308, 494, 712, 494, 3, "#FFFFFF", opacity=45)
# railings on both decks: top rail + stanchions, thin but >=3pt
for deck, (x0, x1, y) in [("saloon", (252, 768, 540)), ("promenade", (302, 718, 488))]:
    line(f"{deck} rail", x0, y - 2, x1, y - 2, 3.5, "#3A2814")
    for i, x in enumerate(range(x0 + 6, x1 - 4, 26)):
        line(f"{deck} stanchion {i+1}", x, y - 2, x, y + 4, 3, "#3A2814")
# pilothouse forward on the promenade
rect("Pilothouse", 640, 428, 96, 62, fill=CABIN, stroke=INK, strokeWidth=3, radius=8)
rect("Pilothouse glass", 648, 438, 80, 26, fill=GLASS, stroke="#5A4020", strokeWidth=2.5, radius=4)
for i, x in enumerate([670, 692]):
    line(f"Pilot mullion {i+1}", x, 438, x, 464, 3, "#5A4020", opacity=80)
line("Pilot glint", 654, 460, 716, 442, 3, "#FFFFFF", opacity=45)
rect("Pilothouse roof", 634, 420, 108, 12, fill=STACK_BAND, stroke=INK, strokeWidth=2.5, radius=6)
# stovepipe vent + whistle on the texas deck
rect("Vent cowl", 330, 466, 20, 26, fill=STACK_BAND, stroke=INK, strokeWidth=2, radius=5)
ell("Vent mouth", 340, 466, 11, 6, fill="#0E0A06", stroke=INK, strokeWidth=2)
rect("Whistle", 380, 470, 9, 20, fill=lin([(0, "#E8C880"), (1, "#8A6428")], DOWN), stroke=INK,
     strokeWidth=1.5, radius=3)

# --- paddle box: solid hood over the wheel's upper half, proud of the decks --------------------
d.path(f"M{WCX - WR - 20},{WCY + 10} A{WR + 20},{WR + 20} 0 0 1 {WCX + WR + 20},{WCY + 10} Z",
       "Paddle box", fill=BOX, stroke=INK, strokeWidth=3.5)
# decorative arch band following the hood rim
d.path(f"M{WCX - WR - 8},{WCY + 8} A{WR + 8},{WR + 8} 0 0 1 {WCX + WR + 8},{WCY + 8}",
       "Box fascia line", fill=NONE, stroke="#E8B266", strokeWidth=3, opacity=75)
d.path(f"M{WCX - WR + 14},{WCY + 6} A{WR - 14},{WR - 14} 0 0 1 {WCX + WR - 14},{WCY + 6}",
       "Box fascia line 2", fill=NONE, stroke="#8A5228", strokeWidth=2.5, opacity=70)
# fascia: two fielded panels + a roundel on the hood face
for i, xx in enumerate([WCX - 84, WCX + 40]):
    rect(f"Box panel {i+1}", xx, WCY - 76, 42, 34, fill=NONE, stroke="#E8B266", strokeWidth=2.5,
         opacity=70, radius=6)
ell("Box roundel", WCX, WCY - 66, 22, 22, fill=rad([(0, "#F0C884"), (1, "#8A5228")]),
    stroke=INK, strokeWidth=2)
d.path(f"M{WCX - 10},{WCY - 66} L{WCX},{WCY - 76} L{WCX + 10},{WCY - 66} L{WCX},{WCY - 56} Z",
       "Roundel star", fill="#3A2010", stroke=NONE)
line("Box top sheen", WCX - WR + 10, WCY - 56, WCX + WR - 10, WCY - 56, 3, "#F2DCA8", opacity=30)
# small covered steps where the box meets the deck
rect("Box step aft", WCX - WR - 30, WCY - 4, 22, 14, fill=BOX, stroke=INK, strokeWidth=2)
rect("Box step fore", WCX + WR + 8, WCY - 4, 22, 14, fill=BOX, stroke=INK, strokeWidth=2)

# --- twin funnels flanking the wheel ----------------------------------------------------------
def funnel(name, cx, lean):
    d.path(f"M{cx - 20},542 L{cx - 16 + lean},394 Q{cx - 16 + lean},380 {cx - 2 + lean},378 "
           f"L{cx + 18 + lean},378 Q{cx + 34 + lean},380 {cx + 34 + lean},394 L{cx + 38},542 Z",
           name, fill=STACK, stroke=INK, strokeWidth=3)
    rect(f"{name} cap", cx - 20 + lean, 372, 58, 20, fill=STACK_BAND, stroke=INK,
         strokeWidth=2.5, radius=8)
    line(f"{name} sheen", cx - 8 + lean * 0.5, 398, cx - 8, 534, 4, "#FFE9B4", opacity=40)
    rect(f"{name} band", cx - 18 + lean * 0.55, 440, 54, 9, fill="#2E1808", opacity=75, stroke=NONE)
    # lazy smoke
    d.path(f"M{cx + 8 + lean},368 Q{cx + lean - 12},340 {cx + 4 + lean},316 "
           f"Q{cx + lean + 16},292 {cx + 2 + lean},268", f"{name} smoke",
           fill=NONE, stroke="#E8D8C0", strokeWidth=6, opacity=30, cap="round")
    d.path(f"M{cx + 20 + lean},364 Q{cx + lean + 38},344 {cx + 26 + lean},314",
           f"{name} smoke 2", fill=NONE, stroke="#E8D8C0", strokeWidth=4.5, opacity=22, cap="round")

funnel("Stack aft", 380, -14)
funnel("Stack fore", 616, 14)
# stays from the stack tops to the deck ends — rigging as fine lines
line("Stay aft 1", 366, 380, 226, 596, 3, "#2A1A10", opacity=65)
line("Stay aft 2", 392, 378, 308, 542, 3, "#2A1A10", opacity=55)
line("Stay fore 1", 636, 380, 806, 606, 3, "#2A1A10", opacity=65)
line("Stay fore 2", 620, 378, 520, 380, 3, "#2A1A10", opacity=45)
# flag staffs
line("Jack staff", 806, 606, 826, 520, 3.5, "#3A2814")
d.path("M826,522 L856,532 L826,542 Z", "Jack pennant", fill=lin([(0, "#E8B45E"), (1, "#A84A28")], 0),
       stroke=INK, strokeWidth=1.5)
line("Ensign staff", 216, 598, 204, 536, 3.5, "#3A2814")
d.path("M204,538 L182,548 L204,558 Z", "Ensign", fill=lin([(0, "#B04A34"), (1, "#6E2418")], 180),
       stroke=INK, strokeWidth=1.5)

# --- water dressing ---------------------------------------------------------------------------
# churn where the wheel bites + foam wake astern
ell("Wheel churn", WCX - 30, 706, 110, 16, fill=rad([(0, "#F4EAD0", 0.55), (1, "#F4EAD0", 0)]),
    stroke=NONE)
for i, (x, y, w, op) in enumerate([(240, 690, 80, 50), (200, 710, 96, 40), (170, 736, 100, 30),
                                   (156, 766, 88, 22)]):
    if on_disc(x - w / 2, y, 4) and on_disc(x + w / 2, y, 4):
        ell(f"Wake sheet {i+1}", x, y, w / 2, 6 + i, fill=rad([(0, "#F0E6CC", 0.6), (1, "#F0E6CC", 0)]),
            stroke=NONE, opacity=op)
        line(f"Wake crest {i+1}", x - w / 2 + 6, y - 3, x + w / 2 - 10, y - 3, 3, "#FFF8E8", opacity=op)
ell("Bow wash", 796, 674, 40, 11, fill=rad([(0, "#F4EAD0", 0.55), (1, "#F4EAD0", 0)]), stroke=NONE)
# long reflections
ell("Hull reflection", 480, 726, 220, 16, fill=rad([(0, "#8A5E36", 0.35), (1, "#8A5E36", 0)]), stroke=NONE)
ell("Stack reflection", 616, 700, 30, 8, fill=rad([(0, "#E8B95E", 0.4), (1, "#E8B95E", 0)]), stroke=NONE)
ell("Stack reflection aft", 380, 700, 30, 8, fill=rad([(0, "#E8B95E", 0.4), (1, "#E8B95E", 0)]), stroke=NONE)

# --- sanity: everything stays inside the plate ------------------------------------------------
for x, y in [(214, 598), (816, 640), (300, 714), (WCX - WR - 22, WCY - 60), (616 + 14 + 34, 378),
             (380 - 14 - 16, 378), (826, 520), (204, 536), (380, 268), (616, 268)]:
    assert on_disc(x, y, 8), (x, y)

# --- name -------------------------------------------------------------------------------------
d.text("PADDLE STEAMER", "Name", x=500, y=940, size=58, font="Virelai Sans", color="#F6E8CC", justify="center")
LINE2, SZ2, TRK = "1896 · SIDE-LEVER STEAM", 22, 200
r = d.text(LINE2, "Second line", x=500, y=975, size=SZ2, font="Virelai Sans", color="#D8BA8E", justify="center")
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

d.finish("paddle-steamer-V1R00")
