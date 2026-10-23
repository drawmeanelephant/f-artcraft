#!/usr/bin/env python3
"""Biplane — field plate V1R00. Three-quarter from below and ahead: the rotary
cowl face reads, both staggered wings show their doped-linen undersides
translucent against the sky, interplane struts cross-braced with 3pt wires,
blurred prop disc, fixed gear. Cloud deck below closing on the disc arc.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420; aircraft aloft over a cloud floor."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Biplane — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#241E18"

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

LINEN = lin(-90, (0, "#F4E6C2", 0.9), (0.6, "#DCC294", 0.92), (1, "#A88E5E", 0.95))
LINEN_UNDER = lin(-90, (0, "#C8AE80", 0.85), (1, "#8E744A", 0.92))
FUSE = lin(-90, (0, "#8FA08E"), (0.45, "#5E7263"), (1, "#2E3E32"))

# --- backdrop + sky plate ------------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin(-90, (0, "#101C26"), (1, "#05080C")), stroke=NONE)
for i, (x, y, w) in enumerate([(88, 132, 4), (908, 100, 5), (40, 555, 3), (953, 500, 4),
                               (115, 910, 4), (875, 918, 3), (958, 770, 4), (44, 305, 3)]):
    d.shape("ellipse", f"Backdrop fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#C8D8E4", opacity=20, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880, fill="#BCD8E8", opacity=7,
        stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=lin(-90, (0, "#40759B"), (0.35, "#7FA8C6"), (0.7, "#C2DCEA"), (1, "#EAF2F4")),
        stroke="#0E1C26", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F4FAFC", strokeWidth=3, opacity=35)

# sun high left + soft glow
ell("Sun glow", 270, 190, 110, 95, fill=rad((0, "#FFF8E0", 0.5), (1, "#FFF8E0", 0)),
    stroke=NONE, opacity=70)
ell("Sun", 270, 190, 36, 36, fill=rad((0, "#FFFDF4"), (0.75, "#FFF0C0"), (1, "#EED49A")),
    stroke=NONE, opacity=90)
# scattered clouds
for i, (cx, cy, rx, ry, op) in enumerate([(390, 200, 130, 15, 45), (620, 160, 110, 11, 35),
                                          (700, 300, 120, 16, 40), (240, 340, 100, 11, 30),
                                          (830, 480, 70, 10, 28), (180, 500, 80, 10, 26)]):
    ell(f"Cloud {i+1} shade", cx + 8, cy + 5, rx, ry,
        fill=rad((0, "#8AA0B4", 0.4), (1, "#8AA0B4", 0)), stroke=NONE, opacity=op)
    ell(f"Cloud {i+1}", cx, cy, rx, ry,
        fill=rad((0, "#FFFFFF", 0.85), (0.7, "#F8FCFE", 0.45), (1, "#F8FCFE", 0)),
        stroke=NONE, opacity=op + 20)

# cloud deck across the bottom, closing on the disc arc
CL, CR = chord(706)
d.path(f"M{CL:.1f},706 L{CR:.1f},706 A{PR},{PR} 0 0 1 {CL:.1f},706 Z", "Cloud floor",
       fill=lin(-90, (0, "#A8BECA", 0.55), (0.4, "#8AA2B4", 0.8), (1, "#4E687C", 0.95)),
       stroke=NONE)
for i, (cx, cy, rx, ry) in enumerate([(280, 706, 120, 26), (430, 712, 150, 30), (600, 704, 130, 24),
                                      (730, 716, 110, 26), (350, 742, 140, 26), (560, 748, 160, 28),
                                      (700, 756, 120, 24), (240, 740, 90, 20)]):
    ell(f"Deck puff {i+1}", cx, cy, rx, ry,
        fill=rad((0, "#FFFFFF", 0.8), (0.6, "#E8F0F2", 0.5), (1, "#C4D4DC", 0)),
        stroke=NONE, opacity=80)
# two birds working the lift
for i, (x, y, s) in enumerate([(760, 560, 0.9), (800, 585, 0.6)]):
    d.path(f"M{x - 15*s:.1f},{y:.1f} Q{x - 7*s:.1f},{y - 8*s:.1f} {x:.1f},{y:.1f} "
           f"Q{x + 7*s:.1f},{y - 8*s:.1f} {x + 15*s:.1f},{y:.1f}", f"Bird {i+1}",
           fill=NONE, stroke="#3A4A58", strokeWidth=3, opacity=55, cap="round")

# --- empennage: tailplane, fin, rudder, skid ------------------------------------------------
d.path("M262,502 L196,514 Q184,517 194,524 L270,528 L276,512 Z", "Tailplane",
       fill=LINEN_UNDER, stroke=INK, strokeWidth=3)
d.path("M254,484 Q236,436 252,398 Q262,388 272,398 L300,470 L290,486 Z", "Fin + rudder",
       fill=LINEN, stroke=INK, strokeWidth=3)
line("Rudder hinge", 284, 472, 262, 404, 3, "#6E5C3C", opacity=70)
line("Tail skid", 246, 520, 232, 540, 4, "#3A3226")
ell("Skid shoe", 231, 542, 6, 4, fill="#2A241A", stroke=NONE)

# --- fuselage ---------------------------------------------------------------------------------
d.path("M246,486 Q250,470 300,462 Q460,442 620,456 Q680,462 700,470 L700,514 "
       "Q660,526 520,528 Q360,532 268,514 Q244,504 246,486 Z", "Fuselage",
       fill=FUSE, stroke=INK, strokeWidth=3.5)
# fabric sheen along the spine + belly shade
d.path("M280,472 Q440,452 640,462", "Spine light", fill=NONE, stroke="#D8E4D4", strokeWidth=4,
       opacity=45, cap="round")
d.path("M270,508 Q420,524 660,512 L660,522 Q430,534 276,518 Z", "Belly shade",
       fill="#16241C", opacity=35, stroke=NONE)
# stitched panels aft
for i, x in enumerate([300, 350, 400, 450]):
    line(f"Panel seam {i+1}", x, 462 - (x - 300) * 0.03, x - 4, 522 - (x - 300) * 0.02,
         3, "#2A3A30", opacity=35)
# fuselage band — plain, no codes
d.path("M508,450 L540,448 L544,528 L512,529 Z", "Fuselage band",
       fill=lin(-90, (0, "#F0E6C8"), (1, "#C8B48A")), opacity=85, stroke=NONE)

# cockpit: dark opening, coaming, little screen, headrest
d.path("M448,462 Q470,448 502,450 Q514,452 512,460 Q500,468 470,470 Q452,470 448,462 Z",
       "Cockpit opening", fill=lin(-90, (0, "#101810"), (1, "#28322A")), stroke=INK,
       strokeWidth=2)
d.path("M500,450 Q512,438 522,442 L520,452 Q510,448 500,452 Z", "Windscreen",
       fill=lin(-90, (0, "#F2FAFC", 0.8), (1, "#6E8A96", 0.8)), stroke=INK, strokeWidth=2)
ell("Headrest", 438, 458, 12, 9, fill=lin(-90, (0, "#6A4E30"), (1, "#33220F")), stroke=INK,
    strokeWidth=2)

# --- landing gear ----------------------------------------------------------------------
line("Gear leg front", 620, 520, 664, 588, 7, "#2E382C")
line("Gear leg rear", 566, 524, 600, 588, 7, "#2E382C")
line("Axle spreader", 596, 590, 668, 588, 6, "#222A22")
line("Bungee", 640, 560, 632, 590, 4, "#4A4436")
for cx, tag in [(600, "Gear L"), (668, "Gear R")]:
    ell(f"{tag} tyre", cx, 596, 22, 22, fill=NONE,
        stroke=lin(-90, (0, "#4A4238"), (1, "#100E0A")), strokeWidth=11)
    for k in range(8):
        a = math.radians(k * 45)
        line(f"{tag} spoke {k+1}", cx + 4*math.cos(a), 596 + 4*math.sin(a),
             cx + 16*math.cos(a), 596 + 16*math.sin(a), 3, "#8A8474", opacity=85)
    ell(f"{tag} hub", cx, 596, 6, 6, fill=chrome(cx - 6, 590, cx + 6, 602), stroke=INK,
        strokeWidth=1.5)

# --- lower wing (shorter, staggered aft) -------------------------------------------------
LOWER = ("M398,524 Q408,510 444,508 L700,520 Q724,522 730,532 Q722,544 700,544 "
         "L428,538 Q404,534 398,524 Z")
d.path(LOWER, "Lower wing", fill=LINEN_UNDER, stroke=INK, strokeWidth=3)
for i, x in enumerate(range(440, 700, 40)):
    line(f"Lower rib {i+1}", x, 512 + (x - 440) * 0.045, x - 2, 538 + (x - 440) * 0.02,
         3, "#7A6440", opacity=30)
line("Lower leading light", 416, 516, 700, 526, 3, "#FFF6DC", opacity=50)

# --- interplane struts + wire bracing ----------------------------------------------------
for i, ((xt, yt), (xb, yb)) in enumerate([((478, 408), (468, 512)), ((654, 414), (644, 516))]):
    line(f"Strut {i+1} fore", xt, yt, xb, yb, 7, "#6B5232")
    line(f"Strut {i+1} aft", xt + 14, yt + 2, xb + 12, yb + 2, 6, "#54401F")
# X-bracing in the bay + landing wires down to the axle
line("Flying wire A", 492, 412, 656, 516, 3, "#4A4638", opacity=75)
line("Flying wire B", 640, 418, 480, 512, 3, "#4A4638", opacity=75)
line("Landing wire L", 468, 514, 596, 590, 3, "#4A4638", opacity=70)
line("Landing wire R", 656, 518, 668, 588, 3, "#4A4638", opacity=70)
line("Centre wire", 560, 524, 600, 590, 3, "#4A4638", opacity=60)
# cabane struts fuselage to top wing
line("Cabane L", 566, 452, 574, 414, 6, "#5A4A2E")
line("Cabane R", 616, 452, 634, 416, 6, "#5A4A2E")
line("Cabane wire", 574, 416, 616, 452, 3, "#4A4638", opacity=60)

# --- upper wing: full span, translucent linen ----------------------------------------------
UPPER = ("M336,398 Q348,382 388,380 L786,396 Q816,399 822,411 Q814,422 784,424 "
         "L376,414 Q344,410 336,398 Z")
d.path(UPPER, "Upper wing", fill=LINEN, stroke=INK, strokeWidth=3)
for i, x in enumerate(range(390, 780, 42)):
    line(f"Upper rib {i+1}", x, 382 + (x - 390) * 0.04, x - 2, 414 + (x - 390) * 0.028,
         3, "#7A6440", opacity=28)
line("Upper leading light", 356, 390, 788, 406, 4, "#FFF8E0", opacity=55)
line("Upper trailing shade", 368, 412, 780, 422, 3, "#6E5A38", opacity=35)

# --- rotary cowl + cylinders + prop --------------------------------------------------------
# cylinder bulges peeking below the cowl rim
for k in range(5):
    a = math.radians(60 + k * 36)
    cx, cy = 726 + 30*math.cos(a), 496 + 30*math.sin(a)
    d.path(rot_rect_path(cx, cy, 11, 15, math.degrees(a) + 90), f"Cylinder {k+1}",
           fill=lin(-90, (0, "#6E6A5E"), (1, "#2C2A22")), stroke=INK, strokeWidth=2)
ell("Cowl", 726, 492, 32, 32,
    fill=rad((0, "#C9CDD2"), (0.55, "#7A838C"), (0.85, "#3E464E"), (1, "#22282E")),
    stroke=INK, strokeWidth=3)
# crescent intakes around the hub
for k in range(3):
    a0 = math.radians(200 + k * 40)
    x, y = 726 + 18*math.cos(a0), 492 + 18*math.sin(a0)
    d.path(f"M{x-7},{y-7} A10,10 0 0 0 {x+7},{y+7} Z", f"Intake {k+1}",
           fill="#141A20", opacity=80, stroke=NONE)
ell("Cowl hub", 726, 492, 9, 9, fill=chrome(717, 483, 735, 501), stroke=INK, strokeWidth=2)
ell("Cowl sheen", 716, 480, 10, 7, fill="#FFFFFF", opacity=35, stroke=NONE)
# prop shaft + blurred disc + two blade flashes
line("Prop shaft", 758, 492, 726, 492, 7, "#5A5E66")
ell("Prop disc", 762, 492, 14, 96,
    fill=lin(90, (0, "#FFFFFF", 0), (0.5, "#E8F0F2", 0.35), (1, "#FFFFFF", 0)),
    stroke="#D8E4E8", strokeWidth=2, opacity=85)
d.path("M756,420 Q770,410 776,424 L772,486 L760,486 Z", "Prop blade up",
       fill=lin(-90, (0, "#8A6E4A", 0.85), (1, "#4A3A24", 0.85)), stroke=INK, strokeWidth=2,
       opacity=90)
d.path("M768,564 Q754,574 748,560 L752,498 L764,498 Z", "Prop blade down",
       fill=lin(-90, (1, "#8A6E4A", 0.85), (0, "#4A3A24", 0.85)), stroke=INK, strokeWidth=2,
       opacity=90)
ell("Prop boss", 762, 492, 8, 11, fill=chrome(754, 481, 770, 503), stroke=INK, strokeWidth=2)

# --- caption -----------------------------------------------------------------------------------
d.text("BIPLANE", "Name", x=500, y=934, size=56, font="Virelai Sans", color="#EAF2F6",
       justify="center")
LINE2, SZ2, TRK = "1917 · 130 HP ROTARY", 22, 200
r = d.text(LINE2, "Second line", x=500, y=975, size=SZ2, font="Virelai Sans", color="#9FC2D6",
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

for (x, y, p) in [(822, 411, 6), (336, 398, 4), (762, 396, 4), (196, 514, 4), (252, 398, 6),
                  (690, 618, 8), (231, 546, 4), (776, 424, 4)]:
    assert on_disc(x, y, p), (x, y)

d.finish("biplane-V1R00")
