#!/usr/bin/env python3
"""City taxi — field plate V1R00. Near-profile of a boxy night cab, turned a
few degrees so the grille reads: checker stripe, lit roof sign, one door
handle catching the light. Night-amber plate, skyline behind, wet asphalt
reflection. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420; wheels grounded on the chord y=700."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("City Taxi — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
GROUND = 700
INK = "#221410"

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

def cab(y0, y1):
    return lin(-90, (0, "#F6CE56"), (0.5, "#D89F30"), (1, "#8A5E16"))

# --- backdrop + night-amber plate -----------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin(-90, (0, "#1A1226"), (1, "#060408")), stroke=NONE)
for i, (x, y, w) in enumerate([(84, 120, 4), (920, 90, 5), (40, 540, 3), (955, 480, 4),
                               (110, 905, 4), (880, 925, 3), (960, 760, 4), (36, 300, 3)]):
    d.shape("ellipse", f"Backdrop fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#E8D8B8", opacity=22, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880, fill="#F0B860", opacity=6, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=lin(-90, (0, "#242040"), (0.35, "#4E3324"), (0.68, "#9A6A2C"), (1, "#DDA44C")),
        stroke="#160E10", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#FFE8C0", strokeWidth=3, opacity=30)

# moon + stars
for i, (r, op) in enumerate([(56, 10), (44, 16), (34, 22)]):
    ell(f"Moon glow {i+1}", 258, 196, r, r, fill="#FFF2D0", opacity=op, stroke=NONE)
ell("Moon", 258, 196, 30, 30, fill=rad((0, "#FFFDF0"), (0.75, "#F8E8C0"), (1, "#E0C890")), stroke=NONE,
    opacity=95)
ell("Moon crater 1", 248, 188, 5, 5, fill="#D8BE98", opacity=50, stroke=NONE)
ell("Moon crater 2", 266, 204, 4, 4, fill="#D8BE98", opacity=45, stroke=NONE)
for i, (x, y, w) in enumerate([(160, 130, 3), (360, 100, 4), (700, 140, 3), (820, 220, 4), (540, 90, 3),
                               (880, 330, 3), (140, 320, 3)]):
    d.shape("ellipse", f"Star {i+1}", x=x, y=y, width=w, height=w, fill="#FFF4DC", opacity=55, stroke=NONE)

# skyline silhouette, bottoms buried under the road
BLDS = [(128, 640, 96, 700), (214, 420, 74, 700), (292, 330, 66, 700), (366, 470, 84, 700),
        (700, 380, 78, 700), (788, 300, 60, 700), (852, 460, 60, 700), (640, 520, 52, 700)]
for i, (x, top, w, bot) in enumerate(BLDS):
    d.path(f"M{x},{bot} L{x},{top} L{x+w},{top} L{x+w},{bot} Z", f"Block {i+1}",
           fill=lin(-90, (0, "#241C32"), (1, "#120C1A")), opacity=92, stroke=NONE)
    if i % 3 == 0:  # stepped parapet
        d.path(f"M{x+8},{top} L{x+8},{top-14} L{x+w-8},{top-14} L{x+w-8},{top}", f"Parapet {i+1}",
               fill="#241C32", opacity=92, stroke=NONE)
# lit windows, scattered
WINS = [(228, 448), (246, 448), (228, 490), (264, 470), (306, 360), (324, 360), (306, 400), (342, 380),
        (390, 500), (408, 530), (390, 560), (714, 410), (732, 410), (714, 450), (750, 430), (802, 330),
        (820, 330), (802, 370), (838, 350), (866, 490), (884, 520), (654, 550), (672, 580)]
for i, (x, y) in enumerate(WINS):
    d.shape("rectangle", f"Window {i+1}", x=x, y=y, width=9, height=13,
            fill=rad((0, "#FFDC8E"), (1, "#C8882E")), opacity=50 if i % 4 else 72, stroke=NONE)

# --- wet asphalt, closing on the disc arc ----------------------------------------------
L, R = chord(GROUND)
d.path(f"M{L:.1f},{GROUND} L{R:.1f},{GROUND} A{PR},{PR} 0 0 1 {L:.1f},{GROUND} Z", "Road",
       fill=lin(-90, (0, "#2E2434"), (0.4, "#1C1622"), (1, "#0A0710")), stroke=NONE)
line("Kerb light", L + 10, GROUND + 2, R - 10, GROUND + 2, 3, "#FFD890", opacity=40)
# wet sheen: broad amber pool under the cab + skyline reflections as short streaks
ell("Wet sheen", 500, 712, 330, 12, fill=rad((0, "#E8A848", 0.5), (1, "#E8A848", 0)), stroke=NONE,
    opacity=55)
for i, (x, y, h, op) in enumerate([(300, 706, 60, 30), (382, 704, 80, 24), (560, 705, 70, 26),
                                   (716, 706, 90, 30), (800, 704, 60, 22), (640, 708, 45, 18),
                                   (240, 708, 48, 20), (470, 703, 55, 20)]):
    d.path(f"M{x},{y} L{x + 6},{y} L{x + 3},{y + h} Z", f"Light streak {i+1}",
           fill=lin(-90, (0, "#FFCC70", 0.55), (1, "#FFCC70", 0)), opacity=op, stroke=NONE)
# cab reflection: squashed mirror smear fading down
d.path("M240,706 L780,706 L752,770 L268,770 Z", "Cab reflection",
       fill=lin(-90, (0, "#C89438", 0.4), (1, "#C89438", 0)), opacity=30, stroke=NONE)
d.path("M240,706 L780,706 L780,712 L240,712 Z", "Reflection bright edge", fill="#F6C468",
       opacity=32, stroke=NONE)
ell("Taxi shadow", 505, 700, 320, 13, fill="#080508", opacity=55, stroke=NONE)
# headlamp pool ahead of the car
ell("Headlamp pool", 796, 706, 40, 9, fill=rad((0, "#FFE4A0", 0.8), (1, "#FFE4A0", 0)),
    stroke=NONE, opacity=60)

# --- wheels ------------------------------------------------------------------------------
RWX, FWX, WY, WR = 320, 690, 654, 46
for cx, tag in [(RWX, "Rear"), (FWX, "Front")]:
    ell(f"{tag} wheel well", cx, WY - 4, 56, 56,
        fill=lin(-90, (0, "#080606"), (1, "#241A12")), stroke=NONE)

def wheel(cx, tag):
    ell(f"{tag} tyre", cx, WY, WR, WR, fill=NONE,
        stroke=lin(-90, (0, "#4A4038"), (1, "#100C0A")), strokeWidth=15)
    d.path(f"M{cx - WR + 6},{WY - 8} A{WR - 6},{WR - 6} 0 0 1 {cx - 8},{WY - WR + 6}",
           f"{tag} tyre light", fill=NONE, stroke="#9A8878", strokeWidth=3, opacity=40, cap="round")
    ell(f"{tag} rim", cx, WY, WR - 17, WR - 17,
        fill=rad((0, "#E8E4D8"), (0.7, "#B8B4A4"), (1, "#6A6458")))
    for k in range(6):
        a = math.radians(k * 60 - 90)
        ell(f"{tag} vent {k+1}", cx + 16*math.cos(a), WY + 16*math.sin(a), 4, 4,
            fill="#4A443C", opacity=75, stroke=NONE)
    ell(f"{tag} hubcap", cx, WY, 13, 13, fill=chrome(cx - 13, WY - 13, cx + 13, WY + 13),
        stroke=INK, strokeWidth=2)
    ell(f"{tag} hub glint", cx - 4, WY - 5, 3, 3, fill="#FFFFFF", opacity=85, stroke=NONE)

wheel(RWX, "Rear")
wheel(FWX, "Front")

# --- body: boxy sedan, nose turned a touch toward us --------------------------------------
BODY = ("M216,624 L213,590 Q212,570 230,564 L296,556 Q312,554 320,540 L340,472 "
        "Q346,452 368,450 L576,442 Q600,441 612,455 L650,538 Q657,554 676,556 "
        "L756,568 Q792,572 800,590 L806,600 Q812,612 808,622 L806,624 "
        "L748,624 A58,58 0 0 0 632,624 L378,624 A58,58 0 0 0 262,624 Z")
d.path(BODY, "Body", fill=cab(442, 624), stroke=INK, strokeWidth=4)
# rocker shadow + roof/beltline light
d.path("M262,606 L378,606 L632,606 L748,606 L748,616 L262,616 Z", "Rocker shade",
       fill="#5C3C0E", opacity=45, stroke=NONE)
line("Beltline light", 232, 560, 660, 548, 4, "#FFE89A", opacity=45)
line("Roof edge light", 372, 447, 586, 439, 4, "#FFF0B8", opacity=50)

# glazing: one glasshouse, pillars over it
GLASS = ("M358,534 L376,464 Q381,452 396,450 L588,444 Q602,444 610,454 L646,536 "
         "Q650,546 638,547 L366,541 Z")
d.path(GLASS, "Glasshouse", fill=lin(-90, (0, "#FFECC0", 0.5), (1, "#3E5A66", 0.7)),
       stroke=chrome(358, 444, 650, 547), strokeWidth=4)
line("A pillar", 612, 452, 652, 544, 12, INK)
line("B pillar", 494, 448, 490, 544, 10, INK)
line("C pillar", 374, 456, 342, 552, 13, INK)
# through the glass: bench seat + wheel
d.path("M400,520 L470,516 L470,530 L400,534 Z", "Seat shadow", fill="#1A2226", opacity=45, stroke=NONE)
d.path("M560,540 C560,522 576,512 592,514", "Steering wheel", fill=NONE, stroke="#141C1E",
       strokeWidth=6, opacity=55, cap="round")
line("Glass glint 1", 400, 480, 430, 460, 3, "#FFFFFF", opacity=45)
line("Glass glint 2", 560, 470, 596, 452, 3, "#FFFFFF", opacity=40)

# checker stripe: cream band + alternating dark checks, door height
d.path("M224,578 L788,578 L790,594 L222,594 Z", "Checker band",
       fill=lin(-90, (0, "#FFF6DC"), (1, "#E8CE9E")), stroke=NONE)
x = 224
i = 0
while x < 788:
    if i % 2 == 0:
        d.path(f"M{x},{578} L{min(x+14, 790)},{578} L{min(x+14, 790)},{594} L{x},{594} Z",
               f"Check {i//2 + 1}", fill="#241812", opacity=88, stroke=NONE)
    x += 14
    i += 1
line("Checker top edge", 224, 578, 788, 578, 3, "#8A6A34", opacity=50)

# door shut lines + the handle catching the light
line("Front door seam", 500, 556, 500, 618, 3, "#3A2810", opacity=60)
line("Rear door seam", 348, 556, 348, 618, 3, "#3A2810", opacity=60)
d.path(rrect(452, 566, 20, 7, 3.5), "Front door handle", fill=chrome(452, 566, 472, 573),
       stroke=INK, strokeWidth=1.5)
d.path("M450,562 L455,566 L450,570 L455,566 L460,562 L455,566 L460,570 L455,566 Z",
       "Handle glint", fill="#FFFFFF", opacity=90, stroke=NONE)
line("Handle spark", 455, 560, 455, 572, 3, "#FFFFFF", opacity=85)
d.path(rrect(306, 566, 20, 7, 3.5), "Rear door handle", fill=chrome(306, 566, 326, 573),
       stroke=INK, strokeWidth=1.5, opacity=85)

# trunk + hood seams, fuel flap
line("Trunk seam", 300, 556, 300, 612, 3, "#3A2810", opacity=55)
line("Hood seam", 664, 556, 800, 574, 3, "#3A2810", opacity=50)
d.path(ell.__name__ and "M0,0", 0, 0, 0, 0) if False else None
ell("Fuel flap", 262, 580, 9, 9, fill=NONE, stroke="#3A2810", strokeWidth=3, opacity=55)

# --- grille + lamps: front end turned slightly out ---------------------------------------
d.path("M792,572 Q812,574 818,592 L818,606 Q816,622 802,626 L792,626 Z", "Grille",
       fill=chrome(792, 572, 818, 626), stroke=INK, strokeWidth=3)
for i in range(4):
    y = 582 + i * 11
    line(f"Grille bar {i+1}", 796, y, 814, y + 1, 3, "#333C40", opacity=60)
# near headlamp big and lit; far lamp a sliver past the grille corner
ell("Far headlamp", 821, 590, 5, 11, fill=rad((0, "#FFF8DC"), (1, "#D8A050")), stroke=INK,
    strokeWidth=2, opacity=85)
ell("Headlamp bezel", 784, 592, 15, 17, fill=chrome(769, 575, 799, 609), stroke=INK, strokeWidth=2)
ell("Headlamp lens", 786, 592, 10, 12, fill=rad((0, "#FFFFF4"), (0.6, "#FFECAC"), (1, "#D89A40")),
    stroke=NONE)
for i, (r, op) in enumerate([(30, 18), (20, 26)]):
    ell(f"Lamp glow {i+1}", 788, 592, r, r, fill="#FFE8A8", opacity=op, stroke=NONE)
line("Amber marker", 806, 576, 816, 578, 4, "#FF9840", opacity=85)
line("Tail lamp", 214, 574, 226, 576, 6, "#D83828", opacity=85)
# bumpers wrapping the corners
d.path(rrect(796, 620, 40, 15, 7), "Front bumper", fill=chrome(796, 620, 836, 635), stroke=INK,
       strokeWidth=2)
d.path(rrect(190, 618, 34, 15, 7), "Rear bumper", fill=chrome(190, 618, 224, 633), stroke=INK,
       strokeWidth=2)
# headlamp beam to the kerb
d.path("M800,592 L834,700 L796,700 Z", "Headlamp beam", fill=lin(90, (0, "#FFE8A0", 0.35),
       (1, "#FFE8A0", 0)), opacity=55, stroke=NONE)

# --- rooftop sign, lit ---------------------------------------------------------------------
for i, (r, op) in enumerate([(64, 8), (46, 14), (34, 20)]):
    ell(f"Sign glow {i+1}", 500, 428, r, r * 0.7, fill="#FFD882", opacity=op, stroke=NONE)
d.path(rrect(462, 416, 76, 26, 6), "Roof sign", fill=rad((0, "#FFF6CE"), (0.65, "#FFCE62"),
       (1, "#D88A1E")), stroke=INK, strokeWidth=3)
d.path("M468,430 L532,430", "Sign inner shade", fill=NONE, stroke="#B87A1E", strokeWidth=3,
       opacity=50, cap="round")
for i, x in enumerate([474, 488, 502, 516]):
    d.path(rrect(x, 421, 8, 5, 1.5), f"Sign pip {i+1}", fill="#8A5A10", opacity=75, stroke=NONE)
d.path(rrect(468, 442, 64, 6, 2), "Sign base", fill=lin(-90, (0, "#5A4632"), (1, "#241A12")),
       stroke=INK, strokeWidth=2)
line("Sign spill", 380, 448, 620, 440, 5, "#FFE098", opacity=28)

# --- caption -----------------------------------------------------------------------------
d.text("CITY TAXI", "Name", x=500, y=934, size=56, font="Virelai Sans", color="#F6E4C4",
       justify="center")
LINE2, SZ2, TRK = "1987 · V8 · AUTOMATIC", 22, 200
r = d.text(LINE2, "Second line", x=500, y=975, size=SZ2, font="Virelai Sans", color="#D8A868",
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

# nothing pokes past the rim
for (x, y, p) in [(288, 196, 10), (228, 196, 10), (258, 156, 10), (836, 635, 8),
                  (188, 636, 4), (500, 412, 4), (834, 700, 2)]:
    assert on_disc(x, y, p), (x, y)

d.finish("city-taxi-V1R00")
