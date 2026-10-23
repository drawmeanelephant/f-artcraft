#!/usr/bin/env python3
"""Streetcar — field plate V1R00. Side profile of a single-truck city streetcar
at dusk, moving right on grooved rails set in cobbles: cream window band over
maroon panels, warm translucent saloon windows with seat backs and straps
showing through, a blank lit destination blind, and the trolley pole trailing
up to the overhead wire with a spark at the contact. Dusk-blue plate with a
translucent skyline. 1000x1000. House style: gradients + translucent shading,
never flat fills. Plate = circle center (500,460) r420; rail head on y=650."""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Streetcar — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
GY = 650
INK = "#2A1C22"
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

CREAM = lin([(0, "#FFF6DE"), (0.5, "#EEDDB4"), (1, "#C8B088")], DOWN)
MAROON = lin([(0, "#B0443A"), (0.35, "#8A2A28"), (1, "#4E1416")], DOWN)
ROOF = lin([(0, "#7A7480"), (0.4, "#4A4450"), (1, "#26222A")], DOWN)
GOLD = lin([(0, "#FFF0B8"), (0.45, "#E0B45A"), (1, "#8A6224")], DOWN)
STEEL = lin([(0, "#E8E2DC"), (0.5, "#A49A94"), (1, "#5A504C")], DOWN)
DARK = lin([(0, "#3A3238"), (1, "#141012")], DOWN)
WARM_GLASS = lin([(0, "#FFE7A8", 0.82), (0.6, "#FFC46A", 0.7), (1, "#E88A3C", 0.6)], DOWN)

# --- backdrop + plate ---------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin([(0, "#121626"), (1, "#06070E")], DOWN), stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880, fill="#4A6A9A", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=lin([(0, "#2A3C6A"), (0.45, "#4A6A9E"), (0.72, "#8A90B4"), (0.86, "#D8A6A0"), (1, "#3A2E44")], DOWN),
        stroke="#0E1426", strokeWidth=6)
d.shape("ellipse", "Plate vignette", x=80, y=40, width=840, height=840,
        fill=rad([(0, "#000000", 0), (0.75, "#000000", 0), (1, "#0A0E1E", 0.55)]), stroke=NONE)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C8D8F0", strokeWidth=3, opacity=35)
# first stars + a thin moon
for i, (x, y, r) in enumerate([(250, 160, 2.5), (330, 120, 2), (640, 110, 2.5), (720, 170, 2), (190, 260, 2),
                               (820, 280, 2.2), (560, 150, 1.8), (430, 96, 2)]):
    assert on_disc(x, y, 12)
    ell(f"Star {i+1}", x, y, r, r, fill="#FFF8E8", opacity=80, stroke=NONE)
    ell(f"Star {i+1} glow", x, y, r * 3, r * 3, fill=rad([(0, "#FFF8E8", 0.5), (1, "#FFF8E8", 0)]), stroke=NONE)
d.path("M748,236 A34,34 0 1 1 712,282 A28,28 0 1 0 748,236 Z", "Moon",
       fill=lin([(0, "#FFF8E0"), (1, "#E8D8B0")], DOWN), stroke=NONE, opacity=90)
ell("Moon glow", 728, 262, 60, 60, fill=rad([(0, "#FFF4D8", 0.3), (1, "#FFF4D8", 0)]), stroke=NONE)

# --- skyline (translucent, behind the car) ---------------------------------------------
L0, R0 = chord(GY)
blds = [(L0, GY), (148, 590), (148, 520), (196, 520), (196, 470), (238, 470), (238, 430), (262, 410), (286, 430),
        (286, 500), (330, 500), (330, 446), (392, 446), (392, 520), (430, 520), (430, 400), (470, 400),
        (470, 380), (500, 380), (500, 400), (540, 400), (540, 488), (582, 488), (582, 430), (640, 430),
        (640, 470), (676, 470), (676, 414), (726, 414), (726, 506), (770, 506), (770, 452), (820, 452),
        (820, 540), (852, 540), (852, 600), (R0, GY)]
for x, y in blds[1:-1]:
    assert on_disc(x, y, 8), (x, y)
d.path("M" + " L".join(f"{x:.1f},{y}" for x, y in blds) + " Z", "Skyline",
       fill=lin([(0, "#2A3458", 0.75), (1, "#1A2038", 0.9)], DOWN), stroke=NONE)
rng = random.Random(106)
tops = {}
for (xa, ya), (xb, yb) in zip(blds, blds[1:]):
    if ya == yb and xb > xa:
        for x in range(int(xa) + 8, int(xb) - 8, 14):
            tops[x] = ya
n = 0
for x, top in sorted(tops.items()):
    for y in range(int(top) + 14, GY - 30, 18):
        if rng.random() < 0.32 and on_disc(x + 3, y + 5, 10):
            n += 1
            rect(f"Lit window {n}", x, y, 6, 9, fill=lin([(0, "#FFE6A0"), (1, "#F0A850")], DOWN),
                 opacity=rng.choice([35, 50, 65]), stroke=NONE)
# dusk haze sitting on the street
d.path(f"M{L0:.1f},{GY} C300,600 700,600 {R0:.1f},{GY} Z", "Street haze",
       fill=lin([(0, "#E8A890", 0), (1, "#E8A890", 0.28)], DOWN), stroke=NONE)

# --- street: cobbles + grooved rails, closing on the disc arc ------------------------------
sl, sr = chord(GY + 4)
d.path(f"M{sl:.1f},{GY + 4} L{sr:.1f},{GY + 4} A420,420 0 0 1 {sl:.1f},{GY + 4} Z", "Street",
       fill=lin([(0, "#4E4658"), (0.3, "#34303E"), (1, "#16141C")], DOWN), stroke=NONE)
row = 0
for y, h, w, op in [(662, 7, 18, 40), (674, 8, 22, 34), (688, 10, 26, 28), (704, 11, 30, 22), (722, 13, 36, 17),
                    (744, 15, 42, 12)]:
    row += 1
    off = (row % 2) * w / 2
    l, r_ = chord(y + h)
    x = l + 14 + off
    k = 0
    while x + w < r_ - 14:
        if on_disc(x, y + h, 8) and on_disc(x + w, y + h, 8):
            k += 1
            d.shape("rectangle", f"Cobble {row}.{k}", x=round(x, 1), y=y, width=round(w - 4, 1), height=h,
                    radius=3, fill=lin([(0, "#8A8098"), (1, "#4A4456")], DOWN), opacity=op, stroke=NONE)
        x += w
# wet-cobble reflections of the lit windows
for i, x in enumerate([250] + [325 + k * 70 for k in range(6)] + [750]):
    assert on_disc(x - 20, 760, 10) and on_disc(x + 20, 760, 10)
    d.path(f"M{x - 18},666 L{x + 18},666 L{x + 12},760 L{x - 12},760 Z", f"Window reflection {i+1}",
           fill=lin([(0, "#FFC878", 0.5), (1, "#FFC878", 0)], DOWN), stroke=NONE, opacity=45)
# warm window light spilled on the cobbles
ell("Window light pool", 500, 690, 230, 26, fill=rad([(0, "#FFC878", 0.45), (1, "#FFC878", 0)]), stroke=NONE)
for y0, nm in [(GY, "near"), (GY + 18, "far")]:
    l, r_ = chord(y0 + 6)
    rect(f"Rail {nm}", l + 6, y0, r_ - l - 12, 5, fill=lin([(0, "#F4ECE4"), (0.5, "#A8A0A0"), (1, "#4A4448")], DOWN),
         stroke=NONE, opacity=90 if nm == "near" else 55)
    line(f"Rail groove {nm}", l + 10, y0 + 6.5, r_ - 10, y0 + 6.5, 2.5, "#0E0C12", opacity=70)

# --- overhead wire ------------------------------------------------------------------------
WY = 196
wl, wr = chord(WY)
line("Span wire", wl + 10, WY - 34, wr - 10, WY - 30, 3, "#141A2C", opacity=45)
for i, x in enumerate([wl + 70, 500, wr - 70]):
    line(f"Hanger {i+1}", x, WY - 33, x, WY, 3, "#141A2C", opacity=55)
    rect(f"Hanger ear {i+1}", x - 6, WY - 3, 12, 5, fill=DARK, stroke=NONE, opacity=80)
line("Contact wire", wl + 8, WY, wr - 8, WY, 3.5, lin([(0, "#3A4058"), (1, "#141828")], DOWN))
line("Wire glint", wl + 30, WY - 1.2, wr - 30, WY - 1.2, 1.2, "#C8D4F0", opacity=40)

# --- trolley pole (behind the roof) --------------------------------------------------------------
BASE = (582, 336)
TIP = (374, WY + 8)
line("Trolley pole", BASE[0], BASE[1], TIP[0] + 6, TIP[1] + 4, 6, STEEL)
line("Trolley pole shade", BASE[0], BASE[1] + 2, TIP[0] + 6, TIP[1] + 6, 2, "#2A2428", opacity=45)
d.path(f"M{TIP[0] - 4},{TIP[1] + 10} L{TIP[0]},{TIP[1]} L{TIP[0] + 14},{TIP[1] + 4} Z", "Trolley harp",
       fill=STEEL, stroke=INK, strokeWidth=1.5)
ell("Trolley wheel", TIP[0], TIP[1] - 1, 7, 7, fill=rad([(0, "#F0E8E0"), (1, "#6A6064")]), stroke=INK, strokeWidth=1.5)
ell("Spark glow", TIP[0], WY, 30, 22, fill=rad([(0, "#FFFFFF", 0.95), (0.25, "#BFE0FF", 0.7), (1, "#7AA8FF", 0)]),
    stroke=NONE)
for i, (dx, dy) in enumerate([(14, -8), (-12, -10), (10, 9), (-9, 8)]):
    line(f"Spark {i+1}", TIP[0], WY, TIP[0] + dx, WY + dy, 2, "#FFFFFF", opacity=75)
d.path(f"M{TIP[0] + 12},{TIP[1] + 6} Q260,330 236,520", "Retriever rope", fill=NONE,
       stroke="#1E1A22", strokeWidth=3, opacity=75, cap="round")

# --- truck + wheels -------------------------------------------------------------------------------------
WR = 32
for i, x in enumerate([440, 560]):
    cy = GY - WR
    ell(f"Wheel {i+1}", x, cy, WR, WR, fill=rad([(0, "#6A5E62"), (0.8, "#3A3236"), (1, "#1E181C")]),
        stroke=INK, strokeWidth=2.5)
    ell(f"Wheel {i+1} web", x, cy, WR * 0.78, WR * 0.78, fill=rad([(0, "#5A4E52"), (1, "#2E262A")]),
        stroke="#1A1418", strokeWidth=1.5)
    for k in range(8):
        a = k / 8 * 2 * math.pi
        line(f"Wheel {i+1} spoke {k+1}", x + 7 * math.cos(a), cy + 7 * math.sin(a),
             x + WR * 0.74 * math.cos(a), cy + WR * 0.74 * math.sin(a), 3.5, "#7A6A6E")
    ell(f"Wheel {i+1} hub", x, cy, 8, 8, fill=GOLD, stroke=INK, strokeWidth=1.5)
    d.path(f"M{x - WR*0.9:.1f},{cy - 8:.1f} A{WR*0.92:.1f},{WR*0.92:.1f} 0 0 1 {x - 8:.1f},{cy - WR*0.9:.1f}",
           f"Wheel {i+1} glint", fill=NONE, stroke="#FFFFFF", strokeWidth=2.5, opacity=30, cap="round")
rect("Truck side frame", 396, 598, 208, 16, fill=DARK, stroke=INK, strokeWidth=2, radius=4)
for i, x in enumerate([440, 560]):
    rect(f"Axle box {i+1}", x - 12, 606, 24, 18, fill=DARK, stroke=INK, strokeWidth=1.5, radius=3)
d.path("M478,598 L486,588 L494,598 L502,588 L510,598 L518,588 L526,598", "Truck spring",
       fill=NONE, stroke=STEEL, strokeWidth=3.5, cap="round")
rect("Motor case", 470, 610, 60, 18, fill=lin([(0, "#4A4248"), (1, "#1A1418")], DOWN), stroke=NONE, radius=6)

# --- body ---------------------------------------------------------------------------------------------------
X0, X1 = 222, 778
d.path(f"M{X0 + 10},592 L{X1 - 10},592 Q{X1 + 6},590 {X1 + 8},560 L{X1 + 8},404 "
       f"L{X0 - 8},404 L{X0 - 8},560 Q{X0 - 6},590 {X0 + 10},592 Z", "Lower body", fill=MAROON, stroke=INK, strokeWidth=3)
rect("Window band", X0 - 8, 404, X1 - X0 + 16, 100, fill=CREAM, stroke=INK, strokeWidth=2.5)
rect("Letterboard", X0 - 8, 368, X1 - X0 + 16, 36, fill=CREAM, stroke=INK, strokeWidth=2.5)
d.path(f"M{X0 - 18},370 Q500,322 {X1 + 18},370 L{X1 + 18},376 L{X0 - 18},376 Z", "Roof",
       fill=ROOF, stroke=INK, strokeWidth=2.5)
d.path("M330,350 Q500,330 670,350 L670,342 Q500,322 330,342 Z", "Clerestory", fill=ROOF, stroke=INK, strokeWidth=2)
for i, x in enumerate(range(360, 650, 48)):
    rect(f"Vent {i+1}", x, 340, 22, 6, fill=lin([(0, "#FFE0A0", 0.7), (1, "#E89848", 0.5)], DOWN),
         stroke=NONE, radius=2)
line("Roof sheen", X0 + 20, 366, X1 - 20, 366, 2.5, "#FFFFFF", opacity=25)
rect("Trolley base", BASE[0] - 22, 330, 44, 10, fill=DARK, stroke=INK, strokeWidth=1.5, radius=3)
d.path(f"M{BASE[0]-14},332 L{BASE[0]-8},322 L{BASE[0]-2},332 L{BASE[0]+4},322 L{BASE[0]+10},332",
       "Trolley base spring", fill=NONE, stroke=STEEL, strokeWidth=3, cap="round")
# blank destination blind, lit from behind
rect("Destination box", 430, 372, 140, 28, fill=DARK, stroke=INK, strokeWidth=2, radius=3)
rect("Destination blind", 436, 377, 128, 18, fill=lin([(0, "#FFF4D0", 0.95), (1, "#F0D090", 0.85)], DOWN),
     stroke=NONE, radius=2)
rect("Destination blind glow", 426, 368, 148, 36, fill=rad([(0, "#FFF0C0", 0.4), (1, "#FFF0C0", 0)]), stroke=NONE)
# letterboard lining
for i, (x, w) in enumerate([(X0, 196), (586, X1 - 586)]):
    d.shape("rectangle", f"Letterboard lining {i+1}", x=x, y=376, width=w, height=20, radius=4,
            fill=NONE, stroke="#B8862E", strokeWidth=2, opacity=60)

# windows: rear door vestibule, six saloon windows, front door vestibule
def window(name, x, y, w, h, seats=True):
    rect(f"{name}", x, y, w, h, fill=WARM_GLASS, stroke="#6A4A2A", strokeWidth=2.5, radius=5)
    if seats:
        d.path(f"M{x + 6},{y + h} L{x + 6},{y + h - 30} Q{x + w * 0.3},{y + h - 38} {x + w * 0.55},{y + h - 30} "
               f"L{x + w * 0.55},{y + h} Z", f"{name} seat back", fill="#7A3A1E", opacity=42, stroke=NONE)
        line(f"{name} strap", x + w * 0.7, y + 4, x + w * 0.7, y + 22, 3, "#6A4020", opacity=55)
        ell(f"{name} strap loop", x + w * 0.7, y + 26, 4, 5, fill=NONE, stroke="#6A4020", strokeWidth=2.5, opacity=55)
    line(f"{name} glint", x + 6, y + h * 0.55, x + w * 0.4, y + 6, 3, "#FFFFFF", opacity=35)

window("Rear door glass upper", X0 + 2, 412, 56, 80, seats=False)
for i in range(6):
    window(f"Saloon window {i+1}", 296 + i * 70, 412, 58, 80)
window("Front door glass upper", X1 - 58, 412, 56, 80, seats=False)
for i, x in enumerate([X0 - 4, X0 + 62, X1 - 62, X1 + 4]):
    line(f"Door post {i+1}", x, 404, x, 590, 3.5, "#5A1A1A", opacity=70)
rect("Rear door lower glass", X0 + 4, 516, 52, 64, fill=lin([(0, "#FFD88A", 0.55), (1, "#C86A30", 0.45)], DOWN),
     stroke="#5A1A1A", strokeWidth=2, radius=4)
rect("Front door lower glass", X1 - 56, 516, 52, 64, fill=lin([(0, "#FFD88A", 0.55), (1, "#C86A30", 0.45)], DOWN),
     stroke="#5A1A1A", strokeWidth=2, radius=4)
rect("Belt rail", X0 - 8, 503, X1 - X0 + 16, 8, fill=GOLD, stroke=NONE)
line("Lower body sheen", X0 + 70, 524, X1 - 70, 524, 4, "#FFFFFF", opacity=18)
rect("Lower body shade", X0 + 64, 566, X1 - X0 - 128, 24, fill="#200608", opacity=30, stroke=NONE)
d.shape("rectangle", "Panel lining", x=X0 + 70, y=520, width=X1 - X0 - 140, height=56, radius=6,
        fill=NONE, stroke="#E0B45A", strokeWidth=2.5, opacity=70)
rect("Rocker", X0 - 6, 590, X1 - X0 + 12, 8, fill=DARK, stroke=NONE)
# steps, headlamp, fenders, grab rails
for i, x in enumerate([X0 + 4, X1 - 56]):
    rect(f"Step {i+1}", x, 600, 52, 6, fill=STEEL, stroke=INK, strokeWidth=1.5)
ell("Headlamp", X1 + 14, 470, 9, 13, fill=rad([(0, "#FFFBE0"), (1, "#FFC860")]), stroke=INK, strokeWidth=2)
ell("Headlamp glow", X1 + 18, 470, 26, 24, fill=rad([(0, "#FFF2C0", 0.6), (1, "#FFD890", 0)]), stroke=NONE)
ell("Tail lamp", X0 - 14, 540, 5, 7, fill=rad([(0, "#FFB0A0"), (1, "#C02A20")]), stroke=INK, strokeWidth=1.5)
ell("Tail lamp glow", X0 - 16, 540, 14, 14, fill=rad([(0, "#FF6A50", 0.5), (1, "#FF6A50", 0)]), stroke=NONE)
for side, (xa, xb) in [("front", (X1 + 4, X1 + 34)), ("rear", (X0 - 4, X0 - 34))]:
    d.path(f"M{xa},598 L{xb},606 L{xb},624 L{xa},624 Z", f"Lifeguard {side}",
           fill=lin([(0, "#3A3238"), (1, "#141012")], DOWN), stroke=INK, strokeWidth=1.5)
    for k, y in enumerate([608, 616]):
        line(f"Lifeguard {side} slat {k+1}", xa, y, xb, y, 3, STEEL, opacity=70)
line("Grab rail rear", X0 + 60, 520, X0 + 60, 586, 3.5, GOLD)
line("Grab rail front", X1 - 60, 520, X1 - 60, 586, 3.5, GOLD)
# check the car and the pole stay in the disc
for x, y in [(X0 - 34, 624), (X1 + 34, 624), (X0 - 18, 370), (X1 + 18, 370), (X1 + 44, 470),
             (TIP[0] - 30, WY - 22)]:
    assert on_disc(x, y, 10), (x, y)

# --- name ----------------------------------------------------------------------------------------------------
d.text("STREETCAR", "Name", x=500, y=940, size=58, font="Virelai Sans", color="#E4ECF8", justify="center")
LINE2, SZ2, TRK = "1916 · 600 V DC ELECTRIC", 22, 200
r = d.text(LINE2, "Second line", x=500, y=975, size=SZ2, font="Virelai Sans", color="#A8B8D8", justify="center")
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

d.finish("streetcar-V1R00")
