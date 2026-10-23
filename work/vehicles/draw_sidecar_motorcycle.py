#!/usr/bin/env python3
"""Sidecar motorcycle — field plate V1R00. Profile of a V-twin outfit heading
right: the chair rides on the far side, so only its deck line, nose lip and
wheel clear the bike's silhouette. Goggles rest on the tank, wheels spoked at
3pt, deep valanced mudguards, low fishtail exhaust. Olive plate, dirt road,
treeline horizon. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420; wheels grounded on the chord y=700."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Sidecar Motorcycle — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
GROUND = 700
INK = "#202214"

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

def olive(y0, y1):
    return lin(-90, (0, "#6B7A50"), (0.5, "#45522F"), (1, "#212B16"))

def olive_far(y0, y1):
    return lin(-90, (0, "#82895E"), (0.5, "#5A6340"), (1, "#333C22"))

# --- backdrop + olive plate --------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin(-90, (0, "#1E2418"), (1, "#090B05")), stroke=NONE)
for i, (x, y, w) in enumerate([(86, 140, 4), (908, 105, 5), (40, 560, 3), (952, 505, 4),
                               (118, 915, 4), (872, 922, 3), (957, 775, 4), (42, 310, 3)]):
    d.shape("ellipse", f"Backdrop fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#DAD8B0", opacity=20, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880, fill="#C8CC90", opacity=6, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=lin(-90, (0, "#576244"), (0.38, "#828A5E"), (0.72, "#B4B588"), (1, "#DBD7AC")),
        stroke="#161A0E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F4F2DC", strokeWidth=3, opacity=35)

# pale sun + two birds
ell("Sun glow", 640, 210, 120, 90, fill=rad((0, "#FFF8DC", 0.5), (1, "#FFF8DC", 0)),
    stroke=NONE, opacity=70)
ell("Sun", 640, 210, 42, 42, fill=rad((0, "#FFFDF0"), (0.75, "#F8ECC0"), (1, "#E0CC90")),
    stroke=NONE, opacity=85)
for i, (x, y, s) in enumerate([(320, 240, 1.0), (365, 262, 0.7)]):
    d.path(f"M{x - 16*s:.1f},{y:.1f} Q{x - 8*s:.1f},{y - 9*s:.1f} {x:.1f},{y:.1f} "
           f"Q{x + 8*s:.1f},{y - 9*s:.1f} {x + 16*s:.1f},{y:.1f}", f"Bird {i+1}",
           fill=NONE, stroke="#3A4028", strokeWidth=3, opacity=60, cap="round")

# distant treeline along the horizon, then the dirt road closing on the disc arc
L, R = chord(GROUND)
tree = [f"M{L:.1f},{GROUND}"]
for x, ty, tw in [(L + 20, 668, 40), (L + 70, 648, 55), (L + 140, 672, 45), (R - 180, 660, 50),
                  (R - 120, 644, 45), (R - 60, 670, 40)]:
    tree.append(f"Q{x + tw/2:.0f},{ty} {x + tw:.0f},{GROUND}")
tree.append(f"L{R:.1f},{GROUND} Z")
d.path(" ".join(tree), "Treeline", fill=lin(-90, (0, "#4A5434"), (1, "#2C331E")), opacity=85,
       stroke=NONE)
d.path(f"M{L:.1f},{GROUND} L{R:.1f},{GROUND} A{PR},{PR} 0 0 1 {L:.1f},{GROUND} Z", "Dirt road",
       fill=lin(-90, (0, "#7A6A46"), (0.5, "#54482E"), (1, "#2E2716")), stroke=NONE)
line("Road crown light", L + 12, GROUND + 2, R - 12, GROUND + 2, 3, "#D8CE9E", opacity=40)
for i, (y, op) in enumerate([(726, 28), (758, 22), (796, 16)]):
    h = chord(y)[1] - chord(y)[0] - 80
    line(f"Track {i+1}", PCX - h/2, y, PCX + h/2, y, 4, "#241F10", opacity=op)
    line(f"Track light {i+1}", PCX - h/2 + 24, y + 4, PCX + h/2 - 24, y + 4, 3, "#C8BC8E",
         opacity=op)
for i, (x, y) in enumerate([(250, 690), (700, 692), (430, 696)]):
    d.path(f"M{x - 4},{y} Q{x},{y - 14} {x + 2},{y} M{x + 2},{y} Q{x + 8},{y - 10} {x + 9},{y}",
           f"Grass {i+1}", fill=NONE, stroke="#4A5434", strokeWidth=3, opacity=70, cap="round")
ell("Rig shadow", 500, 700, 330, 12, fill="#141106", opacity=50, stroke=NONE)

# --- sidecar (far side): drawn first so the bike occludes its middle -----------------------
# its wheel just clears the silhouette behind the rear wheel
SCX, SCY, SCR = 232, 666, 34
d.path("M200,646 Q192,580 244,556 Q296,534 366,536 L520,524 Q576,518 600,542 "
       "Q612,556 606,576 Q596,602 540,620 L400,636 Q260,650 200,646 Z",
       "Sidecar body", fill=olive_far(518, 650), stroke=INK, strokeWidth=3.5, opacity=95)
d.path("M224,580 Q300,552 400,548", "Sidecar deck light", fill=NONE, stroke="#E8E6C4",
       strokeWidth=4, opacity=35, cap="round")
# cockpit opening + screen lip peeking above the deck
d.path("M330,540 Q390,528 460,530 L462,542 Q395,538 336,548 Z", "Cockpit",
       fill=lin(-90, (0, "#10160C"), (1, "#2A3018")), opacity=90, stroke=NONE)
d.path("M540,526 Q558,492 592,486 L596,494 Q566,500 552,530 Z", "Screen lip",
       fill=lin(-90, (0, "#F4F8EC", 0.7), (1, "#8AA0A8", 0.7)), stroke=INK, strokeWidth=2.5,
       opacity=85)
# mudguard over the sidecar wheel + its lamp
d.path(f"M{SCX - 42},{SCY - 6} A{SCR + 8},{SCR + 8} 0 0 1 {SCX + 42},{SCY - 8} "
       f"L{SCX + 34},{SCY + 2} A{SCR - 2},{SCR - 2} 0 0 0 {SCX - 34},{SCY + 2} Z",
       "Sidecar mudguard", fill=olive_far(SCY - 44, SCY), stroke=INK, strokeWidth=3, opacity=95)
ell("Sidecar lamp", 196, 600, 5, 6, fill=rad((0, "#FFD8B0"), (1, "#B03020")), stroke=INK,
    strokeWidth=1.5, opacity=90)
# sidecar wheel, spoked like the bike's
def spoked(cx, cy, r, tag, n=14, rr=17):
    ell(f"{tag} tyre", cx, cy, r, r, fill=NONE,
        stroke=lin(-90, (0, "#4A4638"), (1, "#100E08")), strokeWidth=13)
    d.path(f"M{cx - r + 5},{cy - 6} A{r - 5},{r - 5} 0 0 1 {cx - 7},{cy - r + 5}",
           f"{tag} tyre light", fill=NONE, stroke="#9A9078", strokeWidth=3, opacity=35, cap="round")
    ell(f"{tag} rim", cx, cy, r - rr, r - rr, fill=NONE, stroke=chrome(cx - r, cy - r, cx + r, cy + r),
        strokeWidth=4)
    for k in range(n):
        a = math.radians(k * 360 / n)
        line(f"{tag} spoke {k+1}", cx + 7*math.cos(a + 0.35), cy + 7*math.sin(a + 0.35),
             cx + (r - rr)*math.cos(a), cy + (r - rr)*math.sin(a), 3, "#8A8474", opacity=85)
    ell(f"{tag} hub", cx, cy, 8, 8, fill=chrome(cx - 8, cy - 8, cx + 8, cy + 8), stroke=INK,
        strokeWidth=2)

spoked(SCX, SCY, SCR, "Sidecar wheel", n=12, rr=14)
# attachment struts stubbing toward the far side, under the frame
line("Sidecar strut front", 480, 606, 350, 656, 5, "#2A2E1C")
line("Sidecar strut rear", 370, 620, 280, 658, 5, "#2A2E1C")

# --- the bike -------------------------------------------------------------------------------
RWX, FWX, WY, WR = 335, 680, 648, 52

# rear chain run + primary case behind the wheels' line
line("Chain top", 468, 596, 335, 636, 6, "#181A10")
line("Chain bottom", 468, 610, 335, 650, 6, "#24261A")
d.path("M410,566 Q462,556 486,578 Q500,596 488,612 Q462,630 414,624 Q386,616 390,592 "
       "Q392,572 410,566 Z", "Primary case", fill=lin(-90, (0, "#5A5648"), (1, "#24241A")),
       stroke=INK, strokeWidth=3)

# wheels
for cx, tag in [(RWX, "Rear"), (FWX, "Front")]:
    spoked(cx, WY, WR, tag + " wheel", n=14, rr=16)

# deep valanced mudguards
d.path("M255,634 A80,80 0 0 1 415,628 L406,644 A62,62 0 0 0 264,648 Z", "Rear mudguard",
       fill=olive(560, 648), stroke=INK, strokeWidth=3.5)
d.path("M252,632 Q246,662 268,678 L286,668 Q272,650 278,634 Z", "Rear valance",
       fill=olive(632, 678), stroke=INK, strokeWidth=3)
ell("Tail lamp", 256, 618, 6, 7, fill=rad((0, "#FF9A80"), (0.6, "#C03020"), (1, "#581208")),
    stroke=INK, strokeWidth=2)
d.path("M608,632 A76,76 0 0 1 752,626 L744,642 A58,58 0 0 0 616,646 Z", "Front mudguard",
       fill=olive(566, 646), stroke=INK, strokeWidth=3.5)
line("Front guard tip light", 700, 584, 742, 622, 3, "#E8E6C4", opacity=45)

# frame: top tube under the tank, down tube, seat tube
line("Top tube", 600, 434, 424, 470, 9, "#1A1C10")
line("Down tube", 606, 440, 478, 598, 9, "#1A1C10")
line("Seat tube", 424, 470, 412, 600, 9, "#1A1C10")
line("Rear stays", 410, 486, 335, 640, 7, "#1A1C10")

# V-twin engine: cylinders + finning + crankcase
d.path("M474,564 Q512,552 526,570 Q540,592 524,612 Q500,632 468,626 Q442,620 440,596 "
       "Q440,574 474,564 Z", "Crankcase", fill=lin(-90, (0, "#8A8672"), (0.6, "#55523F"),
       (1, "#23231A")), stroke=INK, strokeWidth=3)
d.path(rot := "M500,560 L556,510 L576,528 L522,580 Z", "Front cylinder",
       fill=lin(-45, (0, "#7A7662"), (1, "#2A2A1E")), stroke=INK, strokeWidth=3)
d.path("M452,560 L442,500 L468,494 L480,556 Z", "Rear cylinder",
       fill=lin(-90, (0, "#7A7662"), (1, "#2A2A1E")), stroke=INK, strokeWidth=3)
for i, (x0, y0, x1, y1) in enumerate([(510,554,566,506),(516,566,572,516),(522,574,576,524),
                                      (448,552,438,506),(456,556,446,504),(464,556,454,508)]):
    line(f"Fin {i+1}", x0, y0, x1, y1, 3, "#15170C", opacity=55)
# rocker boxes + pushrod tubes
ell("Front rocker", 560, 512, 13, 9, fill=chrome(547, 503, 573, 521), stroke=INK, strokeWidth=2)
ell("Rear rocker", 456, 494, 12, 9, fill=chrome(444, 485, 468, 503), stroke=INK, strokeWidth=2)
line("Pushrod 1", 528, 574, 556, 528, 3, "#C8C2AC", opacity=80)
line("Pushrod 2", 452, 556, 458, 514, 3, "#C8C2AC", opacity=80)

# exhaust: down from the front cylinder, back along the bottom to a fishtail
d.path("M552,540 Q580,570 576,600 L560,612 Q560,580 536,556 Z", "Exhaust header",
       fill=chrome(536, 540, 580, 612), stroke=INK, strokeWidth=2)
line("Exhaust pipe", 566, 606, 300, 636, 11, "#3A362A")
d.path(rrect(232, 626, 96, 16, 8), "Muffler", fill=chrome(232, 626, 328, 642), stroke=INK,
       strokeWidth=2)
d.path("M224,630 L232,630 L232,640 L220,644 Q212,637 224,630 Z", "Fishtail",
       fill=chrome(212, 630, 232, 644), stroke=INK, strokeWidth=2)
for i, (x, y, r, op) in enumerate([(200, 634, 12, 22), (182, 628, 9, 16), (168, 622, 7, 12)]):
    ell(f"Exhaust puff {i+1}", x, y, r, r * 0.7, fill=rad((0, "#F0F0E0", 0.6), (1, "#F0F0E0", 0)),
        stroke=NONE, opacity=op)

# footboard
d.path(rrect(436, 610, 66, 10, 4), "Footboard", fill=lin(-90, (0, "#4A4434"), (1, "#1C1A10")),
       stroke=INK, strokeWidth=2)

# seat: sprung leather solo saddle
line("Seat spring 1", 382, 506, 380, 528, 5, "#2A2C1A")
line("Seat spring 2", 404, 506, 402, 528, 5, "#2A2C1A")
d.path("M348,484 Q366,468 400,470 Q418,472 416,488 Q402,500 366,498 Q346,494 348,484 Z",
       "Saddle", fill=lin(-90, (0, "#8A5E36"), (0.6, "#5C3C20"), (1, "#2E1E0E")),
       stroke=INK, strokeWidth=3)
line("Saddle sheen", 356, 480, 402, 474, 3, "#D8A86A", opacity=50)

# tank: teardrop, pinstripe panel, filler cap — and the goggles resting on it
TANK = ("M458,472 Q470,446 516,442 Q562,438 588,452 Q600,460 592,470 Q560,486 498,484 "
        "Q456,482 458,472 Z")
d.path(TANK, "Tank", fill=olive(438, 484), stroke=INK, strokeWidth=3.5)
d.path("M468,466 Q500,452 556,452", "Tank light", fill=NONE, stroke="#E4E2BE", strokeWidth=4,
       opacity=40, cap="round")
d.path("M472,470 Q510,458 568,460 Q560,472 508,476 Q480,476 472,470 Z", "Tank panel",
       fill="#E4DFC0", opacity=22, stroke="#E4DFC0", strokeWidth=3)
ell("Filler cap", 522, 442, 7, 4.5, fill=chrome(515, 437, 529, 447), stroke=INK, strokeWidth=1.5)
# goggles: strap + two rimmed lenses
d.path("M486,438 Q522,428 562,434", "Goggle strap", fill=NONE, stroke="#3A2C1A", strokeWidth=5,
       cap="round")
for i, cx in enumerate([512, 538]):
    ell(f"Goggle lens {i+1}", cx, 432, 12, 10, fill=rad((0, "#C8D8DC", 0.9), (1, "#2C3E44")),
        stroke=chrome(cx - 12, 422, cx + 12, 442), strokeWidth=4)
    ell(f"Goggle glint {i+1}", cx - 4, 428, 3, 3, fill="#FFFFFF", opacity=80, stroke=NONE)
d.path("M524,432 L526,432", "Goggle bridge", fill=NONE, stroke="#3A2C1A", strokeWidth=4, cap="round")

# fork: raked springer — two legs, links, coil spring hint
line("Fork leg L", 608, 438, 672, 642, 8, "#26281A")
line("Fork leg R", 620, 440, 686, 642, 8, "#1A1C10")
line("Fork crown", 600, 436, 628, 442, 9, "#1A1C10")
for i, y in enumerate([560, 572, 584]):
    line(f"Spring coil {i+1}", 634, y, 660, y + 6, 4, "#8A8474", opacity=80)
line("Spring link", 640, 596, 668, 640, 4, "#2A2C1A")

# steering head + bars + grips + mirror
line("Steering head", 600, 420, 614, 448, 11, "#1A1C10")
d.path("M604,424 Q600,404 586,398 L566,394", "Handlebar", fill=NONE, stroke="#26281A",
       strokeWidth=7, cap="round")
d.path("M566,394 L548,392", "Grip", fill=NONE, stroke="#3A2C1A", strokeWidth=9, cap="round")
line("Lever", 566, 392, 556, 404, 3, "#8A8474", opacity=80)
line("Mirror stalk", 588, 400, 576, 372, 3.5, "#26281A")
ell("Mirror", 572, 368, 9, 11, fill=chrome(563, 357, 581, 379), stroke=INK, strokeWidth=2)
ell("Mirror glint", 569, 363, 2.5, 3, fill="#FFFFFF", opacity=80, stroke=NONE)

# headlamp on the fork, chrome bucket, warm lens
d.path("M618,470 Q616,450 636,446 Q658,442 664,460 Q668,476 652,484 Q632,490 622,482 Z",
       "Headlamp bucket", fill=chrome(616, 442, 668, 490), stroke=INK, strokeWidth=3)
ell("Headlamp lens", 650, 466, 10, 13, fill=rad((0, "#FFFCE8"), (0.6, "#F0E2B0"), (1, "#B0905A")),
    stroke=INK, strokeWidth=2)
ell("Lens glint", 647, 461, 3, 3, fill="#FFFFFF", opacity=90, stroke=NONE)
d.path(rrect(634, 492, 20, 7, 3), "Number tab", fill=lin(-90, (0, "#E4DFC0"), (1, "#B0A888")),
       stroke=INK, strokeWidth=2)

# --- caption -------------------------------------------------------------------------------
d.text("SIDECAR MOTORCYCLE", "Name", x=500, y=934, size=56, font="Virelai Sans", color="#F2EECC",
       justify="center")
LINE2, SZ2, TRK = "1941 · FLATHEAD V-TWIN", 22, 200
r = d.text(LINE2, "Second line", x=500, y=975, size=SZ2, font="Virelai Sans", color="#C9C498",
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

for (x, y, p) in [(SCX - SCR, SCY, 4), (FWX + WR, WY, 6), (762, 566, 4), (168, 622, 4),
                  (640, 168, 6), (576, 372, 4)]:
    assert on_disc(x, y, p), (x, y)

d.finish("sidecar-motorcycle-V1R00")
