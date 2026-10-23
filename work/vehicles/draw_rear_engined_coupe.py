#!/usr/bin/env python3
"""Rear-engined coupe — field plate V1R00. Near-profile of a low fastback
coupe heading right: long sloping nose with a round headlamp on the fender
crest, one unbroken roof-to-tail curve, vents cut into the decklid, chrome
bumpers as gradients, Fuchs-style five-leaf wheels. Silver-blue plate with
one road line. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420; wheels grounded on the chord y=700."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Rear-Engined Coupe — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
GROUND = 700
INK = "#1E1A18"

def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

def lin(angle, *stops):
    return {"gradient": {"kind": "linear", "angle": angle, "stops": [
        dict(offset=s[0], color=s[1], **({"opacity": s[2]} if len(s) > 2 else {})) for s in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial", "stops": [
        dict(offset=s[0], color=s[1], **({"opacity": s[2]} if len(s) > 2 else {})) for s in stops]}}

def chord(y):
    h = math.sqrt(max(PR**2 - (y - PCY)**2, 0))
    return PCX - h, PCX + h

def ell(name, cx, cy, rx, ry, **kw):
    return d.shape("ellipse", name, x=round(cx - rx, 1), y=round(cy - ry, 1),
                   width=round(2 * rx, 1), height=round(2 * ry, 1), **kw)

def line(name, x0, y0, x1, y1, w, color, **kw):
    return d.path(f"M{x0:.1f},{y0:.1f} L{x1:.1f},{y1:.1f}", name, fill=NONE, stroke=color,
                  strokeWidth=w, cap="round", **kw)

def rrect(x, y, w, h, r):
    return (f"M{x+r},{y} L{x+w-r},{y} Q{x+w},{y} {x+w},{y+r} L{x+w},{y+h-r} "
            f"Q{x+w},{y+h} {x+w-r},{y+h} L{x+r},{y+h} Q{x},{y+h} {x},{y+h-r} "
            f"L{x},{y+r} Q{x},{y} {x+r},{y} Z")

def chrome(x0, y0, x1, y1):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": 0, "color": "#FFFFFF"}, {"offset": 0.3, "color": "#C9D2D6"},
                      {"offset": 0.55, "color": "#6E7A80"}, {"offset": 0.75, "color": "#E4EAEC"},
                      {"offset": 1, "color": "#8A949A"}]}}

def paint(y0, y1):
    return lin(-90, (0, "#B9CDD8"), (0.42, "#64849A"), (1, "#24384A"))

# --- backdrop + silver-blue plate ------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin(-90, (0, "#1B2430"), (1, "#090D12")), stroke=NONE)
for i, (x, y, w) in enumerate([(90, 130, 4), (905, 110, 5), (42, 555, 3), (950, 505, 4),
                               (125, 912, 4), (870, 918, 3), (955, 770, 4), (45, 305, 3)]):
    d.shape("ellipse", f"Backdrop fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#C8D8E2", opacity=20, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880, fill="#A8C8D8", opacity=7, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=lin(-90, (0, "#4A6A82"), (0.38, "#88A6B8"), (0.72, "#C6D6DF"), (1, "#E6EDF1")),
        stroke="#12202C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F2FAFC", strokeWidth=3, opacity=35)

# soft light high on the right, behind the nose — one soft radial pool, no banding
ell("Sky glow", 680, 250, 160, 120, fill=rad((0, "#FFFFFF", 0.4), (1, "#FFFFFF", 0)),
    stroke=NONE, opacity=70)
# a few thin high cirrus strokes
for i, (x, y, w) in enumerate([(220, 210, 200), (480, 160, 240), (640, 330, 170), (180, 360, 140)]):
    d.path(rrect(x, y, w, 7, 3.5), f"Cirrus {i+1}",
           fill=lin(0, (0, "#FFFFFF", 0), (0.5, "#FFFFFF", 0.7), (1, "#FFFFFF", 0)),
           opacity=45, stroke=NONE)

# --- the one road line, road wash closing on the disc arc ---------------------------------
L, R = chord(GROUND)
d.path(f"M{L:.1f},{GROUND} L{R:.1f},{GROUND} A{PR},{PR} 0 0 1 {L:.1f},{GROUND} Z", "Road wash",
       fill=lin(-90, (0, "#3A4A58", 0.55), (1, "#141E28", 0.8)), stroke=NONE)
line("Road line", L + 6, GROUND + 1, R - 6, GROUND + 1, 4, "#E8F2F6", opacity=70)
line("Road shade", L + 30, GROUND + 14, R - 30, GROUND + 14, 3, "#0C141C", opacity=30)
ell("Coupe shadow", 505, 700, 310, 11, fill="#0A1218", opacity=45, stroke=NONE)

# --- wheels --------------------------------------------------------------------------------
RWX, FWX, WY, WR = 330, 700, 652, 48
for cx, tag in [(RWX, "Rear"), (FWX, "Front")]:
    ell(f"{tag} wheel well", cx, WY - 6, 57, 55,
        fill=lin(-90, (0, "#06090C"), (1, "#1C2830")), stroke=NONE)

def wheel(cx, tag):
    ell(f"{tag} tyre", cx, WY, WR, WR, fill=NONE,
        stroke=lin(-90, (0, "#3E3A36"), (1, "#0E0C0A")), strokeWidth=15)
    d.path(f"M{cx - WR + 6},{WY - 8} A{WR - 6},{WR - 6} 0 0 1 {cx - 8},{WY - WR + 6}",
           f"{tag} tyre light", fill=NONE, stroke="#8A8078", strokeWidth=3, opacity=35, cap="round")
    ell(f"{tag} rim", cx, WY, WR - 17, WR - 17,
        fill=rad((0, "#E8ECEE"), (0.7, "#B4BEC4"), (1, "#5A646C")))
    # five petal cutouts — the Fuchs look
    for k in range(5):
        a = math.radians(k * 72 - 90)
        px, py = cx + 17*math.cos(a), WY + 17*math.sin(a)
        d.path(rot_rect_path(px, py, 11, 17, math.degrees(a) + 90),
               f"{tag} petal {k+1}", fill="#232A30", opacity=90, stroke=NONE)
    ell(f"{tag} hub", cx, WY, 10, 10, fill=chrome(cx - 10, WY - 10, cx + 10, WY + 10),
        stroke=INK, strokeWidth=2)
    ell(f"{tag} hub glint", cx - 3, WY - 4, 2.5, 2.5, fill="#FFFFFF", opacity=85, stroke=NONE)

wheel(RWX, "Rear")
wheel(FWX, "Front")

# --- body: one unbroken fastback curve ----------------------------------------------------
BODY = ("M218,622 L213,586 Q212,568 230,560 L298,550 "
        "C420,536 468,452 556,442 C600,437 640,468 664,504 "
        "L772,558 Q806,566 810,586 L812,604 Q812,620 796,622 "
        "L758,622 A58,58 0 0 0 642,622 L388,622 A58,58 0 0 0 272,622 Z")
d.path(BODY, "Body", fill=paint(437, 622), stroke=INK, strokeWidth=4)
# shoulder highlight + rocker shade
d.path("M300,552 C420,540 466,460 554,449", "Flank light", fill=NONE, stroke="#E8F2F8",
       strokeWidth=5, opacity=45, cap="round")
line("Beltline light", 240, 566, 660, 528, 3, "#E8F2F8", opacity=35)
d.path("M388,608 L642,608 L642,618 L388,618 Z", "Rocker shade", fill="#101C26", opacity=45, stroke=NONE)
line("Sill trim", 390, 622, 640, 622, 4, "#A8BCC8", opacity=70)

# glazing: long door window + rear quarter pane, chrome surround
GLASS = ("M428,538 Q430,500 470,476 Q504,453 552,448 Q592,445 608,458 L646,506 "
         "Q652,514 640,516 L432,542 Z")
d.path(GLASS, "Glasshouse", fill=lin(-90, (0, "#F2FBFF", 0.5), (1, "#33505F", 0.75)),
       stroke=chrome(428, 445, 652, 542), strokeWidth=4)
line("B pillar", 480, 470, 476, 540, 9, INK)
d.path("M560,512 C560,496 574,488 588,490", "Steering wheel", fill=NONE, stroke="#10181C",
       strokeWidth=5, opacity=55, cap="round")
line("Glass glint 1", 500, 480, 536, 458, 3, "#FFFFFF", opacity=50)
line("Glass glint 2", 585, 470, 612, 452, 3, "#FFFFFF", opacity=40)
# wiper parked on the windshield base
line("Wiper", 608, 506, 644, 512, 4, "#18222A", opacity=70)

# door shut lines + handle + lock
line("Door front seam", 640, 522, 634, 618, 3, "#16222C", opacity=55)
line("Door rear seam", 486, 546, 490, 618, 3, "#16222C", opacity=55)
d.path(rrect(540, 548, 22, 7, 3.5), "Door handle", fill=chrome(540, 548, 562, 555),
       stroke=INK, strokeWidth=1.5)
line("Handle glint", 546, 548, 556, 548, 3, "#FFFFFF", opacity=80)

# --- tail: decklid vents, lamp band, reflector ----------------------------------------------
d.path("M224,562 L312,552 L318,566 L228,578 Z", "Decklid grille",
       fill=lin(-90, (0, "#131C24"), (1, "#060A0E")), stroke=INK, strokeWidth=2.5)
for i in range(4):
    x0 = 234 + i * 2
    y = 558 + i * 4.5
    line(f"Decklid vent {i+1}", x0, y, x0 + 72, y - 8, 4, "#46545E", opacity=80)
d.path("M216,566 L236,563 L238,584 L218,586 Z", "Tail lamp",
       fill=lin(0, (0, "#FF7A5A"), (1, "#8A1E14")), stroke=INK, strokeWidth=2)
ell("Rear reflector", 222, 592, 4, 4, fill=rad((0, "#FFB8A0"), (1, "#A82818")), stroke=NONE)
# number-plate recess (blank) + exhaust tip
d.path(rrect(232, 588, 30, 18, 3), "Plate recess", fill=lin(-90, (0, "#2A3A46"), (1, "#121A22")),
       stroke=INK, strokeWidth=2, opacity=90)
d.path(rrect(226, 614, 24, 8, 4), "Exhaust tip", fill=chrome(226, 614, 250, 622), stroke=INK,
       strokeWidth=2)
ell("Exhaust bore", 250, 618, 3, 4, fill="#0C0A08", stroke=NONE)

# --- nose: round headlamp on the fender crest, indicator, filler flap -----------------------
ell("Headlamp bezel", 746, 526, 17, 18, fill=chrome(729, 508, 763, 544), stroke=INK, strokeWidth=2)
ell("Headlamp lens", 748, 527, 12, 13,
    fill=rad((0, "#FFFFF6"), (0.6, "#E8F2F4"), (1, "#8FAAB8")), stroke=NONE)
ell("Lens glint", 744, 522, 4, 4, fill="#FFFFFF", opacity=85, stroke=NONE)
d.path(rrect(782, 552, 18, 8, 4), "Indicator", fill=rad((0, "#FFD89A"), (1, "#D88A20")),
       stroke=INK, strokeWidth=1.5)
# bonnet seam + fuel flap on the front fender
line("Bonnet seam", 668, 514, 788, 566, 3, "#16222C", opacity=50)
ell("Fuel flap", 694, 540, 9, 9, fill=NONE, stroke="#16222C", strokeWidth=3, opacity=60)
line("Fuel flap top", 687, 536, 701, 536, 3, "#E8F2F8", opacity=45)
# badge recess on the nose (blank crest shape, no marque)
d.path(rrect(806, 578, 8, 20, 4), "Nose badge", fill=chrome(806, 578, 814, 598), stroke=INK,
       strokeWidth=1.5)

# bumpers + overriders
d.path(rrect(796, 606, 36, 15, 7), "Front bumper", fill=chrome(796, 606, 832, 621), stroke=INK,
       strokeWidth=2)
d.path(rrect(190, 600, 34, 15, 7), "Rear bumper", fill=chrome(190, 600, 224, 615), stroke=INK,
       strokeWidth=2)
for i, x in enumerate([800, 200]):
    d.path(rrect(x, 594 if i == 0 else 588, 10, 26, 4), f"Overrider {i+1}",
           fill=chrome(x, 588, x + 10, 620), stroke=INK, strokeWidth=1.5)

# mirror on the door, low and forward
line("Mirror stalk", 634, 512, 648, 496, 3, INK)
d.path("M648,496 L668,490 L672,504 L652,510 Z", "Mirror", fill=chrome(648, 490, 672, 510),
       stroke=INK, strokeWidth=2)

# --- caption --------------------------------------------------------------------------------
d.text("REAR-ENGINED COUPE", "Name", x=500, y=934, size=56, font="Virelai Sans", color="#EAF2F6",
       justify="center")
LINE2, SZ2, TRK = "1968 · AIR-COOLED FLAT-SIX", 22, 200
r = d.text(LINE2, "Second line", x=500, y=975, size=SZ2, font="Virelai Sans", color="#A8C2D0",
           justify="center")
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

for (x, y, p) in [(832, 613, 6), (190, 607, 4), (672, 490, 4), (R - 6, 701, 2), (L + 6, 701, 2)]:
    assert on_disc(x, y, p), (x, y)

d.finish("rear-engined-coupe-V1R00")
