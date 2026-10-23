#!/usr/bin/env python3
"""Flying boat — field plate V1R00. Profile of a four-engined flying boat
resting on a calm morning sea, moving right: deep two-tone hull with the
planing step at the waterline, a sponson (sea-wing) at the waterline, a high
wing carrying four radials whose propellers read as translucent discs, a
near-side wingtip float on struts, single fin. Reflection and translucent
water over the submerged keel. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420; waterline on the chord y=612."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Flying Boat — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
WL = 612
INK = "#22202A"

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

def P(cmds, dx=0, dy=0, flip=False):
    """Path from ('M', x, y, ...) tuples; flip mirrors about the waterline."""
    out = []
    for c in cmds:
        op, v = c[0], c[1:]
        if op == "Z":
            out.append("Z"); continue
        pts = []
        for i in range(0, len(v), 2):
            x, y = v[i] + dx, v[i + 1] + dy
            if flip: y = WL + (WL - y) * 0.5
            pts.append(f"{x:.1f},{y:.1f}")
        out.append(op + " ".join(pts))
    return " ".join(out)

def ell(name, cx, cy, rx, ry, **kw):
    return d.shape("ellipse", name, x=round(cx - rx, 1), y=round(cy - ry, 1),
                   width=round(2 * rx, 1), height=round(2 * ry, 1), **kw)

def line(name, x0, y0, x1, y1, w, color, **kw):
    return d.path(f"M{x0:.1f},{y0:.1f} L{x1:.1f},{y1:.1f}", name, fill=NONE, stroke=color,
                  strokeWidth=w, cap="round", **kw)

# --- geometry (canvas coordinates) --------------------------------------------------
HULL = [("M", 848, 590), ("C", 852, 546, 826, 492, 770, 482), ("L", 670, 476),
        ("C", 630, 466, 540, 464, 480, 472), ("L", 400, 482),
        ("C", 330, 482, 262, 468, 206, 446), ("L", 188, 444), ("L", 192, 468),
        ("C", 252, 520, 362, 584, 500, 606), ("L", 506, 606), ("L", 506, 626),
        ("L", 796, 628), ("C", 828, 626, 846, 610, 848, 590), ("Z",)]
LOWER = [("M", 846, 572), ("L", 506, 580), ("C", 400, 570, 300, 538, 214, 484),
         ("L", 192, 468), ("C", 252, 520, 362, 584, 500, 606), ("L", 506, 606), ("L", 506, 626),
         ("L", 796, 628), ("C", 828, 626, 846, 610, 848, 590), ("Z",)]
FIN = [("M", 196, 450), ("L", 166, 318), ("C", 168, 306, 196, 302, 214, 310),
       ("L", 292, 470), ("Z",)]
STAB = [("M", 138, 446), ("C", 150, 438, 250, 436, 300, 446), ("L", 300, 454),
        ("C", 250, 458, 150, 456, 138, 450), ("Z",)]
WING = [("M", 654, 452), ("C", 654, 438, 640, 432, 612, 432), ("L", 470, 440),
        ("C", 450, 442, 436, 446, 428, 450), ("C", 436, 454, 450, 458, 470, 460),
        ("L", 612, 468), ("C", 640, 468, 654, 464, 654, 452), ("Z",)]
WING_ROOT = [("M", 440, 478), ("C", 470, 460, 510, 456, 560, 456), ("L", 650, 460),
             ("C", 674, 466, 692, 474, 708, 479), ("Z",)]
SPONSON = [("M", 556, 598), ("C", 580, 584, 640, 580, 690, 588), ("C", 700, 590, 702, 598, 690, 602),
           ("C", 640, 608, 590, 608, 556, 604), ("Z",)]
FLOAT = [("M", 440, 572), ("C", 452, 560, 520, 558, 552, 566), ("C", 560, 568, 560, 576, 550, 580),
         ("L", 520, 584), ("L", 516, 588), ("C", 480, 590, 450, 586, 440, 578), ("Z",)]

ENGINES = []   # (s, cx, cy, k): spanwise station, nacelle centre, scale
for s in (2, 1, -1, -2):
    ENGINES.append((s, 630 + 20 * s, 450 - 5 * abs(s), 1 - 0.05 * s))

for cmds in (HULL, FIN, STAB, WING):
    for c in cmds:
        for i in range(1, len(c) - 1, 2):
            assert on_disc(c[i], c[i + 1], 14), (c, c[i], c[i + 1])

# --- backdrop + plate ----------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin(-90, (0, "#14202C"), (1, "#070B10")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880, fill="#F6D6A0", opacity=7, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=lin(-90, (0, "#6E9CB8"), (0.45, "#B8D0D8"), (0.72, "#F6DEB4"), (1, "#F2C890")),
        stroke="#0E1A24", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#FFF4DC", strokeWidth=3, opacity=40)

# morning sun low on the left, behind the tail
ell("Sun glow", 300, 470, 170, 150, fill=rad((0, "#FFF6DA", 0.75), (1, "#FFE0A8", 0)), stroke=NONE)
ell("Sun", 300, 500, 54, 54, fill=rad((0, "#FFFDF2"), (0.7, "#FFF0C8"), (1, "#FFD890")), stroke=NONE,
    opacity=90)

# high cloud streaks, translucent
for i, (cx, cy, rx, ry, op) in enumerate([(380, 170, 150, 18, 45), (560, 150, 120, 12, 35),
                                          (640, 236, 140, 20, 40), (260, 270, 110, 12, 30),
                                          (520, 300, 190, 14, 30), (760, 360, 90, 10, 30)]):
    for a in range(0, 360, 30):
        assert on_disc(cx + rx * math.cos(math.radians(a)), cy + ry * math.sin(math.radians(a)), 20), i
    ell(f"Cloud {i+1} shade", cx + 10, cy + 6, rx, ry, fill=rad((0, "#C89A8A", 0.5), (1, "#C89A8A", 0)),
        stroke=NONE, opacity=op)
    ell(f"Cloud {i+1}", cx, cy, rx, ry, fill=rad((0, "#FFFFFF", 0.9), (0.7, "#FFF4E6", 0.5), (1, "#FFF4E6", 0)),
        stroke=NONE, opacity=op + 20)

# gulls, ≥3pt strokes
for i, (x, y, s) in enumerate([(700, 300, 1.0), (744, 322, 0.75), (230, 230, 0.8)]):
    d.path(f"M{x - 18*s:.1f},{y:.1f} Q{x - 9*s:.1f},{y - 10*s:.1f} {x:.1f},{y:.1f} "
           f"Q{x + 9*s:.1f},{y - 10*s:.1f} {x + 18*s:.1f},{y:.1f}", f"Gull {i+1}",
           fill=NONE, stroke="#3A3A48", strokeWidth=3.5, opacity=75, cap="round")

# headland on the horizon, hazy
hl, hr = chord(WL)
d.path(f"M{hl:.1f},{WL} L{hl + 4:.1f},596 C150,586 182,566 220,570 C262,574 280,590 330,594 "
       f"C380,598 420,604 470,{WL} Z", "Headland", fill=lin(-90, (0, "#7E8EA0", 0.8), (1, "#A9B4BE", 0.6)),
       stroke=NONE)
d.path(f"M{hr:.1f},{WL} L{hr - 4:.1f},604 C850,600 820,598 790,604 C760,608 740,610 720,{WL} Z",
       "Far point", fill=lin(-90, (0, "#8E9CAA", 0.6), (1, "#B6C0C8", 0.4)), stroke=NONE)

# --- sea ----------------------------------------------------------------------------
d.path(f"M{hl:.1f},{WL} L{hr:.1f},{WL} A420,420 0 0 1 {hl:.1f},{WL} Z", "Sea",
       fill=lin(-90, (0, "#9EC0C8"), (0.15, "#5E8EA0"), (0.6, "#2E5A70"), (1, "#163246")), stroke=NONE)
# sun glitter column
for i, (y, w, op) in enumerate([(622, 120, 70), (636, 96, 60), (652, 140, 45), (672, 80, 40),
                                (694, 110, 32), (720, 70, 26), (750, 90, 20)]):
    ell(f"Glitter {i+1}", 300, y, w / 2, 3, fill=lin(0, (0, "#FFF4D0", 0), (0.5, "#FFF4D0"), (1, "#FFF4D0", 0)),
        stroke=NONE, opacity=op)

# reflection of the aircraft (mirrored about the waterline, faint)
REF = dict(stroke=NONE)
for cmds in (HULL, WING):
    for c in cmds:
        for i in range(1, len(c) - 1, 2):
            assert on_disc(c[i], WL + (WL - c[i + 1]) * 0.5, 14), ("reflection", c)
d.path(P(HULL, flip=True), "Hull reflection", fill=lin(-90, (0, "#DDE6EA", 0.5), (1, "#DDE6EA", 0.05)), **REF)
d.path(P(WING, flip=True), "Wing reflection", fill="#E8EEF0", opacity=16, **REF)
for i, (y, x0, x1) in enumerate([(640, 220, 760), (660, 260, 720), (684, 300, 700), (712, 360, 640),
                                 (744, 400, 600), (780, 420, 560)]):
    l, r = chord(y)
    x0, x1 = max(x0, l + 30), min(x1, r - 30)
    d.path(f"M{x0},{y} Q{(x0 + x1) / 2},{y - 4} {x1},{y}", f"Ripple {i+1}", fill=NONE,
           stroke="#E6F2F4", strokeWidth=3, opacity=34 - i * 4, cap="round")

# --- far-side engines (behind the wing) -----------------------------------------------
def engine(s, cx, cy, k, far):
    tag = f"Engine {'far' if far else 'near'} {abs(s)}"
    L, h = 96 * k, 15 * k
    nose = cx + 48 * k
    d.path(f"M{cx - L / 2:.1f},{cy - h * 0.6:.1f} C{cx - 10:.1f},{cy - h:.1f} {nose - 20:.1f},{cy - h:.1f} "
           f"{nose:.1f},{cy - h * 0.9:.1f} L{nose:.1f},{cy + h * 0.9:.1f} "
           f"C{nose - 20:.1f},{cy + h:.1f} {cx - 10:.1f},{cy + h:.1f} {cx - L / 2:.1f},{cy + h * 0.6:.1f} Z",
           f"{tag} nacelle",
           fill=lin(-90, (0, "#F4F6F8"), (0.4, "#B8C4CE"), (1, "#5E6C7A")) if not far else
           lin(-90, (0, "#C8D0D8"), (0.5, "#8A98A6"), (1, "#4A5664")),
           stroke=INK, strokeWidth=2)
    d.shape("rectangle", f"{tag} cowl ring", x=round(nose - 10 * k, 1), y=round(cy - h * 0.95, 1),
            width=round(10 * k, 1), height=round(1.9 * h, 1), radius=3,
            fill=lin(-90, (0, "#E8C878"), (0.5, "#B08A3A"), (1, "#6A4E1E")), stroke=NONE)
    line(f"{tag} exhaust", cx - 4, cy + h * 0.7, cx - L / 2 + 6, cy + h * 0.5, 3, "#3A3438", opacity=35)
    pr = 56 * k
    ell(f"{tag} prop disc", nose + 7 * k, cy, 7 * k, pr,
        fill=rad((0, "#FFFFFF", 0.55), (0.75, "#DDE6EC", 0.32), (1, "#9AA8B4", 0.12)),
        stroke="#5A6470", strokeWidth=1.2, opacity=80 if not far else 55)
    d.path(f"M{nose + 7 * k:.1f},{cy - pr * 0.94:.1f} L{nose + 7 * k:.1f},{cy + pr * 0.94:.1f}",
           f"{tag} blade blur", fill=NONE, stroke="#4A5260", strokeWidth=3, opacity=18, cap="round")
    ell(f"{tag} spinner", nose + 6 * k, cy, 7 * k, 8 * k,
        fill=rad((0, "#FFFFFF"), (0.6, "#C8D0D8"), (1, "#6A7682")), stroke=INK, strokeWidth=1.2)
    for yy in (cy - pr, cy + pr):
        assert on_disc(nose + 7 * k, yy, 14), (s, yy)

for s, cx, cy, k in ENGINES[:2]:
    engine(s, cx, cy, k, True)

# --- tail ----------------------------------------------------------------------------
d.path(P(STAB), "Far tailplane", fill=lin(-90, (0, "#C2CCD4"), (1, "#7A8896")), stroke=INK, strokeWidth=2,
       opacity=80)
d.path(P(FIN), "Fin", fill=lin(0, (0, "#C8D2DA"), (0.5, "#F2F5F7"), (1, "#C0CCD6")), stroke=INK, strokeWidth=3)
d.path("M196,450 L170,330", "Rudder hinge", fill=NONE, stroke="#6A7682", strokeWidth=2.5, opacity=60)
d.path(P([("M", 172, 340), ("L", 208, 326), ("L", 214, 352), ("L", 180, 366), ("Z",)]), "Fin band",
       fill=lin(-90, (0, "#2E5A8A"), (1, "#163A62")), stroke=NONE, opacity=90)
d.path("M206,318 L270,458", "Fin sheen", fill=NONE, stroke="#FFFFFF", strokeWidth=4, opacity=40, cap="round")

# --- hull -----------------------------------------------------------------------------
d.path(P(HULL), "Hull", fill=lin(-90, (0, "#FFFFFF"), (0.35, "#E6ECF0"), (0.75, "#B6C2CC"), (1, "#7E8C98")),
       stroke=NONE)
d.path(P(LOWER), "Lower hull", fill=lin(-90, (0, "#2E5A8A"), (0.5, "#1C3E66"), (1, "#0E2440")), stroke=NONE)
d.path("M846,573 L506,581 C400,571 300,539 214,485", "Cheat line", fill=NONE, stroke="#E8B860",
       strokeWidth=4, cap="round")
d.path("M836,560 L506,566 C410,556 330,530 250,488", "Cheat line light", fill=NONE, stroke="#2E5A8A",
       strokeWidth=3, opacity=55, cap="round")
# step: the notch where the planing bottom breaks
d.path("M506,606 L506,626", "Step face", fill=NONE, stroke="#0A1626", strokeWidth=3.5)
d.path("M510,624 L790,626", "Keel sheen", fill=NONE, stroke="#6A9ACA", strokeWidth=3, opacity=45, cap="round")
d.path("M500,604 C380,586 280,540 210,480", "Afterbody chine light", fill=NONE, stroke="#5A86B6",
       strokeWidth=3, opacity=50, cap="round")
# volume
d.path("M760,490 L420,490 C350,490 280,476 220,456", "Deck sheen", fill=NONE, stroke="#FFFFFF",
       strokeWidth=6, opacity=60, cap="round")
d.path(P([("M", 840, 578), ("L", 506, 586), ("C", 400, 576, 300, 544, 214, 490), ("L", 206, 482),
          ("C", 300, 548, 400, 586, 506, 600), ("L", 846, 596), ("Z",)]), "Lower hull shade",
       fill="#060E1A", opacity=25, stroke=NONE)
for i, x in enumerate([300, 380, 460, 560, 660, 740]):
    y0 = 484 if x > 400 else 482 - (400 - x) * 0.18
    d.path(f"M{x},{y0 + 6:.1f} L{x},{570 - (420 - x) * 0.12 if x < 420 else 570:.1f}", f"Panel line {i+1}",
           fill=NONE, stroke="#7A8896", strokeWidth=1.5, opacity=30)
# portholes
for i, x in enumerate(range(366, 736, 30)):
    if 500 <= x <= 530:
        continue
    y = 522 if x > 420 else 522 - (420 - x) * 0.16
    d.shape("rectangle", f"Porthole {i+1}", x=x, y=round(y, 1), width=14, height=17, radius=6,
            fill=rad((0, "#E8F4FA", 0.55), (1, "#4E7A96", 0.75)), stroke="#3A4A5A", strokeWidth=1.5)
    line(f"Porthole {i+1} glint", x + 4, y + 12, x + 8, y + 4, 2, "#FFFFFF", opacity=60)
# boarding door
d.shape("rectangle", "Door", x=504, y=510, width=26, height=52, radius=5, fill=NONE,
        stroke="#5A6A7A", strokeWidth=2.5, opacity=70)
line("Door handle", 524, 536, 524, 542, 3, "#5A6A7A", opacity=70)
# flight deck glazing at the nose
d.path(P([("M", 758, 486), ("L", 790, 488), ("C", 806, 494, 818, 504, 824, 514), ("L", 770, 514), ("Z",)]),
       "Cockpit glazing", fill=lin(-90, (0, "#DCEEF6", 0.55), (1, "#3E6E8E", 0.8)), stroke=INK, strokeWidth=2)
line("Cockpit frame 1", 782, 488, 786, 514, 2.5, INK, opacity=80)
line("Cockpit frame 2", 804, 494, 802, 514, 2.5, INK, opacity=80)
line("Cockpit glint", 764, 506, 774, 492, 2.5, "#FFFFFF", opacity=70)
ell("Bow light", 842, 566, 3.5, 3.5, fill=rad((0, "#FFFFFF"), (1, "#E8D0A0")), stroke=NONE)
line("Mooring cleat", 828, 530, 840, 530, 3, "#5A6470", opacity=80)

# wing root fairing on the hull top
d.path(P(WING_ROOT), "Wing root fairing", fill=lin(-90, (0, "#F4F7F9"), (1, "#B4C0CA")), stroke=INK,
       strokeWidth=2)

# --- wing ----------------------------------------------------------------------------
d.path(P(WING), "Wing", fill=lin(-90, (0, "#FFFFFF"), (0.45, "#D4DCE2"), (1, "#7E8C98")), stroke=INK,
       strokeWidth=3)
d.path("M470,444 L610,439", "Wing sheen", fill=NONE, stroke="#FFFFFF", strokeWidth=4, opacity=70, cap="round")
d.path("M440,454 L610,464", "Wing underside shade", fill=NONE, stroke="#4A5866", strokeWidth=3, opacity=40,
       cap="round")
d.path("M486,441 L486,460", "Aileron hinge", fill=NONE, stroke="#6A7682", strokeWidth=2, opacity=55)

# near-side engines in front of the wing
for s, cx, cy, k in ENGINES[2:]:
    engine(s, cx, cy, k, False)

# --- sponson at the waterline ---------------------------------------------------------
d.path(P(SPONSON), "Sponson", fill=lin(-90, (0, "#F4F7F9"), (0.5, "#B8C4CE"), (1, "#5E6C7A")), stroke=INK,
       strokeWidth=2.5)
d.path("M570,592 C610,586 650,584 684,590", "Sponson sheen", fill=NONE, stroke="#FFFFFF", strokeWidth=3,
       opacity=70, cap="round")
d.path(P([("M", 560, 604), ("C", 600, 610, 650, 610, 690, 604), ("L", 690, 612), ("L", 560, 612), ("Z",)]),
       "Sponson shadow", fill="#0A1626", opacity=30, stroke=NONE)

# --- near wingtip float on struts -----------------------------------------------------
line("Float strut front", 530, 458, 538, 564, 3.5, "#3A4654")
line("Float strut rear", 470, 452, 480, 562, 3.5, "#3A4654")
line("Float strut brace", 470, 456, 538, 562, 3, "#3A4654", opacity=70)
d.path(P(FLOAT), "Wingtip float", fill=lin(-90, (0, "#FFFFFF"), (0.45, "#C4CED6"), (1, "#2E5A8A")),
       stroke=INK, strokeWidth=2.5)
d.path("M452,568 C480,562 520,562 544,568", "Float sheen", fill=NONE, stroke="#FFFFFF", strokeWidth=3,
       opacity=75, cap="round")

# --- translucent water over the submerged keel, closing on the disc arc ----------------
y2 = WL + 26
l1, r1 = chord(WL); l2, r2 = chord(y2)
d.path(f"M{l1:.1f},{WL} L{r1:.1f},{WL} A420,420 0 0 1 {r2:.1f},{y2} L{l2:.1f},{y2} "
       f"A420,420 0 0 1 {l1:.1f},{WL} Z", "Surface water",
       fill=lin(-90, (0, "#9EC0C8", 0.75), (1, "#4E7E92", 0.95)), stroke=NONE)
d.path(f"M{l1 + 6:.1f},{WL} L{r1 - 6:.1f},{WL}", "Waterline glint", fill=NONE, stroke="#FFF6E0",
       strokeWidth=3, opacity=60, cap="round")
# foam where hull and sponson meet the water
for i, (cx, w, op) in enumerate([(530, 70, 70), (622, 90, 65), (700, 70, 55), (820, 50, 60), (420, 60, 40)]):
    ell(f"Foam {i+1}", cx, WL + 2, w / 2, 5, fill=rad((0, "#FFFFFF", 0.9), (1, "#FFFFFF", 0)), stroke=NONE,
        opacity=op)

# --- caption --------------------------------------------------------------------------
d.text("FLYING BOAT", "Name", x=500, y=940, size=56, font="Virelai Sans", color="#F2E6D2", justify="center")
LINE2, SZ2, TRK = "1938 · FOUR 1,600 HP RADIALS", 22, 200
r = d.text(LINE2, "Second line", x=500, y=975, size=SZ2, font="Virelai Sans", color="#C8A878", justify="center")
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
