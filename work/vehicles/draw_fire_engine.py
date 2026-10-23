#!/usr/bin/env python3
"""Fire engine — field plate V1R00. Profile of a 1920s open-cab pumper heading
right: ladder and hose reel stacked over the red body, brass bell, radiator and
headlamp, gold-leaf line on the panels. Dusk street plate with a firehouse
skyline. 1000x1000. House style: gradients + translucent shading, never flat."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Fire Engine — Field Plate", 1000, 1000)

INK = "#24140F"
CX, CY, R = 500, 460, 420
GROUND = 700
FAR = [0.0]


def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}


def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}


def brass(x0, y0, x1, y1):
    return lin(x0, y0, x1, y1, (0, "#FFF2BE"), (0.35, "#E9B94E"), (0.7, "#A86F22"), (1, "#6A4214"))


def red(y0, y1):
    return lin(0, y0, 0, y1, (0, "#E2503A"), (0.45, "#B8291C"), (1, "#6E1510"))


def track(*pts):
    for x, y in pts:
        FAR[0] = max(FAR[0], math.hypot(x - CX, y - CY))


def chord_x(y):
    return math.sqrt(R*R - (y - CY)**2)


def ell(cx, cy, rx, ry):
    k = 0.5523
    return (f"M{cx+rx},{cy} C{cx+rx},{cy+ry*k} {cx+rx*k},{cy+ry} {cx},{cy+ry} "
            f"C{cx-rx*k},{cy+ry} {cx-rx},{cy+ry*k} {cx-rx},{cy} "
            f"C{cx-rx},{cy-ry*k} {cx-rx*k},{cy-ry} {cx},{cy-ry} "
            f"C{cx+rx*k},{cy-ry} {cx+rx},{cy-ry*k} {cx+rx},{cy} Z")


def rrect(x, y, w, h, r):
    return (f"M{x+r},{y} L{x+w-r},{y} Q{x+w},{y} {x+w},{y+r} L{x+w},{y+h-r} "
            f"Q{x+w},{y+h} {x+w-r},{y+h} L{x+r},{y+h} Q{x},{y+h} {x},{y+h-r} "
            f"L{x},{y+r} Q{x},{y} {x+r},{y} Z")


def circle(cx, cy, r, label, **kw):
    kw.setdefault("stroke", NONE)
    track((cx - r, cy - r), (cx + r, cy + r))
    d.shape("ellipse", label, x=cx - r, y=cy - r, width=2*r, height=2*r, **kw)


def line(x0, y0, x1, y1, label, stroke, w, **kw):
    track((x0, y0), (x1, y1))
    d.path(f"M{x0:.1f},{y0:.1f} L{x1:.1f},{y1:.1f}", label, fill=NONE, stroke=stroke,
           strokeWidth=w, cap=kw.pop("cap", "round"), **kw)


# --- backdrop + dusk plate ------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin(0, 0, 0, 1000, (0, "#1E1418"), (1, "#0A0607")), stroke=NONE)
for i, (x, y, w) in enumerate([(90, 120, 4), (900, 90, 5), (40, 520, 3), (955, 470, 4),
                               (110, 900, 4), (880, 910, 3), (960, 760, 4), (30, 300, 3)]):
    d.shape("ellipse", f"Backdrop fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#F3D9B0", opacity=28, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=lin(500, 40, 500, 720, (0, "#1D3446"), (0.45, "#5E4A5C"), (0.78, "#C9784C"), (1, "#F4C47C")),
        stroke="#5A2A1E", strokeWidth=6)

# low sun hanging over the street, above the ladder line
for i, (r, op) in enumerate([(150, 8), (118, 12), (92, 18)]):
    circle(520, 330, r, f"Sun glow {i+1}", fill="#FFD890", opacity=op)
circle(520, 330, 66, "Sun", fill=rad((0, "#FFF4D2"), (0.7, "#FFD68A"), (1, "#F2A95E")), opacity=85)
# a few dusk clouds as translucent streaks
for i, (x, y, w, h, op) in enumerate([(170, 300, 260, 22, 22), (560, 250, 240, 18, 18),
                                      (300, 380, 220, 16, 16), (620, 420, 200, 14, 20)]):
    d.path(rrect(x, y, w, h, h/2), f"Cloud {i+1}", fill=lin(x, 0, x + w, 0, (0, "#F7D2A8"), (1, "#C98A78")),
           opacity=op, stroke=NONE)

# far skyline: rooftops, water tank, the firehouse hose tower
L, Rr = CX - chord_x(GROUND), CX + chord_x(GROUND)
far = (f"M{L:.1f},{GROUND} L{L:.1f},620 L196,620 L196,596 L238,596 L238,612 L286,612 L286,560 "
       f"L300,546 L314,560 L314,604 L360,604 L360,582 L420,582 L420,612 L470,612 L470,574 L530,574 "
       f"L530,600 L600,600 L600,566 L612,566 L612,520 L620,520 L620,566 L660,566 L660,594 L720,594 "
       f"L720,576 L770,576 L770,610 L820,610 L820,630 L{Rr:.1f},630 L{Rr:.1f},{GROUND} Z")
d.path(far, "Skyline far", fill=lin(0, 520, 0, GROUND, (0, "#7C4E52"), (1, "#5A3640")), opacity=55, stroke=NONE)
near = (f"M{L:.1f},{GROUND} L{L+6:.1f},640 L200,640 L200,520 L212,500 L224,520 L224,640 "
        f"L250,640 L250,612 L330,612 L330,650 L700,650 L700,604 L716,604 L716,588 L750,588 L750,604 "
        f"L770,604 L770,622 L830,622 L830,652 L{Rr-6:.1f},652 L{Rr:.1f},{GROUND} Z")
d.path(near, "Skyline near", fill=lin(0, 500, 0, GROUND, (0, "#4A2C34"), (1, "#2E1A20")), opacity=75, stroke=NONE)
# water tank on stilts
for x in (722, 744):
    line(x, 588, x, 566, f"Tank leg {x}", "#3A2228", 4, opacity=80)
d.path(rrect(714, 538, 40, 30, 6), "Water tank", fill=lin(714, 0, 754, 0, (0, "#5A3842"), (1, "#2E1A20")),
       opacity=85, stroke=NONE)
d.path("M712,540 L734,526 L756,540 Z", "Tank roof", fill="#2E1A20", opacity=85, stroke=NONE)
# lit windows
for i, (x, y) in enumerate([(206, 560), (206, 590), (264, 624), (296, 624), (726, 610), (790, 632)]):
    d.path(rrect(x, y, 10, 12, 2), f"Window glow {i+1}", fill=lin(0, y, 0, y + 12, (0, "#FFE2A0"), (1, "#E89A4E")),
           opacity=70, stroke=NONE)

# --- street band closing on the disc arc ------------------------------------------------
d.path(f"M{L:.1f},{GROUND} L{Rr:.1f},{GROUND} A{R},{R} 0 0 1 {L:.1f},{GROUND} Z", "Street",
       fill=lin(0, GROUND, 0, 880, (0, "#5A403A"), (0.5, "#3A2824"), (1, "#22161A")), stroke=NONE)
line(L + 8, GROUND + 1, Rr - 8, GROUND + 1, "Kerb light", "#F5C886", 3, opacity=45)
# cobbles: rows of soft lozenges, kept clear of the rim
n = 0
for row, y in enumerate([722, 752, 786, 822]):
    half = chord_x(y + 10) - 26
    x = CX - half + (row % 2)*18
    while x + 34 < CX + half:
        n += 1
        d.path(rrect(x, y, 30, 12, 6), f"Cobble {n}", fill=lin(0, y, 0, y + 12, (0, "#7A5A50"), (1, "#3A2824")),
               opacity=34, stroke=NONE)
        x += 40
d.shape("ellipse", "Engine shadow", x=190, y=690, width=620, height=26, fill="#120A08", opacity=45, stroke=NONE)

# --- ladder supports + ladder (drawn first, the body overlaps the post feet) ------------
for i, x in enumerate([226, 452, 628]):
    line(x, 432, x, 512, f"Ladder post {i+1}", brass(x - 3, 0, x + 3, 0), 6)

# --- chassis ---------------------------------------------------------------------------
d.path(rrect(214, 588, 578, 16, 4), "Frame rail", fill=lin(0, 588, 0, 604, (0, "#5A3A30"), (1, "#24140F")),
       stroke=NONE)

# --- rear body -------------------------------------------------------------------------
BODY = "M210,506 L506,506 L506,594 L222,594 Q210,594 210,582 Z"
d.path(BODY, "Body", fill=red(506, 594), stroke=INK, strokeWidth=4)
d.path("M214,510 L502,510 L502,524 L214,524 Z", "Body top light", fill="#FFD8C8", opacity=18, stroke=NONE)
d.path("M214,574 L502,574 L502,590 L222,590 Q214,590 214,582 Z", "Body underside shade",
       fill="#3A0806", opacity=30, stroke=NONE)
# compartment doors with gold-leaf line
for i, (x, w) in enumerate([(222, 128), (360, 132)]):
    d.path(rrect(x, 520, w, 62, 8), f"Panel {i+1} shade", fill="#5A0E0A", opacity=18, stroke=NONE)
    d.path(rrect(x + 6, 526, w - 12, 50, 6), f"Gold leaf {i+1}", fill=NONE, stroke="#EBC45E", strokeWidth=3)
    cx, cy = x + w/2, 551
    d.path(f"M{cx-14},{cy} Q{cx-7},{cy-10} {cx},{cy} Q{cx+7},{cy+10} {cx+14},{cy}", f"Gold scroll {i+1}",
           fill=NONE, stroke="#EBC45E", strokeWidth=3, cap="round")
    circle(cx - 20, cy, 3, f"Gold dot {i+1}a", fill="#F4D27A")
    circle(cx + 20, cy, 3, f"Gold dot {i+1}b", fill="#F4D27A")
# brass grab rail along the body
line(222, 512, 496, 512, "Body grab rail", brass(0, 508, 0, 516), 5)
for i, x in enumerate([232, 364, 486]):
    circle(x, 512, 4, f"Rail stanchion {i+1}", fill=brass(x - 4, 508, x + 4, 516))
# rear step, grab bar and tail lamp
d.path(rrect(194, 590, 24, 9, 3), "Rear step", fill=lin(0, 590, 0, 599, (0, "#7A5040"), (1, "#2E1A12")), stroke=NONE)
line(204, 506, 204, 452, "Rear grab bar", brass(201, 0, 207, 0), 5)
circle(208, 532, 8, "Tail lamp", fill=rad((0, "#FFB08A"), (0.6, "#D23A22"), (1, "#6A100A")), stroke=INK, strokeWidth=2)

# --- hose reel on top of the body -----------------------------------------------------
HX, HY = 312, 462
line(HX - 30, 506, HX, HY, "Reel stand rear", brass(0, HY, 0, 506), 6)
line(HX + 30, 506, HX, HY, "Reel stand front", brass(0, HY, 0, 506), 6)
circle(HX, HY, 40, "Hose coil", fill=rad((0, "#F0E0B8"), (0.7, "#D6BE8A"), (1, "#9C8250")))
for i, r in enumerate([32, 24, 16]):
    circle(HX, HY, r, f"Coil ring {i+1}", fill=NONE, stroke="#6E5630", strokeWidth=3, opacity=45)
for k in range(6):
    a = math.radians(k*60 + 15)
    line(HX + 9*math.cos(a), HY + 9*math.sin(a), HX + 38*math.cos(a), HY + 38*math.sin(a),
         f"Reel spoke {k+1}", brass(HX - 30, HY - 30, HX + 30, HY + 30), 5)
circle(HX, HY, 40, "Reel flange", fill=NONE, stroke=brass(HX - 40, HY - 40, HX + 40, HY + 40), strokeWidth=7)
circle(HX, HY, 10, "Reel hub", fill=rad((0, "#FFF2BE"), (0.6, "#D9A441"), (1, "#7A4A16")), stroke=INK, strokeWidth=2)
# hose end draping off the back with its nozzle
d.path(f"M{HX-6},{HY+40} C{HX-30},{HY+56} 250,520 228,540 C214,552 206,566 214,578", "Hose drape",
       fill=NONE, stroke="#C9AE78", strokeWidth=9, cap="round")
d.path(f"M{HX-6},{HY+40} C{HX-30},{HY+56} 250,520 228,540", "Hose drape light",
       fill=NONE, stroke="#F4E6C2", strokeWidth=3, opacity=50, cap="round")
d.path("M210,574 L218,574 L222,592 L206,592 Z", "Hose nozzle", fill=brass(206, 0, 222, 0), stroke=INK, strokeWidth=2)

# --- pump behind the seat ---------------------------------------------------------------
d.path(rrect(458, 482, 46, 110, 14), "Pump barrel", fill=brass(458, 0, 504, 0), stroke=INK, strokeWidth=3)
for i, y in enumerate([500, 538, 574]):
    d.path(rrect(456, y, 50, 8, 3), f"Pump band {i+1}", fill=lin(0, y, 0, y + 8, (0, "#FFE7A0"), (1, "#8C5A1A")),
           stroke=NONE)
for i, y in enumerate([516, 556]):
    circle(481, y, 10, f"Pump gauge {i+1}", fill=rad((0, "#FFFBEA"), (0.8, "#EDE2C4"), (1, "#B49A6A")),
           stroke="#7A4A16", strokeWidth=3)
    line(481, y, 487, y - 6, f"Gauge needle {i+1}", "#3A1A10", 3)
circle(452, 584, 9, "Outlet cap", fill=brass(443, 575, 461, 593), stroke=INK, strokeWidth=2)

# --- open cab: seat, cowl, windscreen, steering wheel -----------------------------------
d.path("M514,560 C512,530 514,504 520,488 C524,480 536,482 536,492 L536,560 Z", "Seat back",
       fill=lin(514, 0, 536, 0, (0, "#8A4A2C"), (1, "#3E1C10")), stroke=INK, strokeWidth=3)
for i, y in enumerate([502, 522, 542]):
    circle(526, y, 3, f"Seat tuft {i+1}", fill="#2A120A", opacity=60)
d.path("M520,548 L598,548 Q606,548 606,556 L606,566 L520,566 Z", "Seat cushion",
       fill=lin(0, 548, 0, 566, (0, "#9A5634"), (1, "#4A2214")), stroke=INK, strokeWidth=3)
d.path("M506,566 L606,566 L606,594 L506,594 Z", "Seat box", fill=red(566, 594), stroke=INK, strokeWidth=3)
COWL = "M606,594 L606,520 C612,504 632,500 646,528 L646,594 Z"
d.path(COWL, "Cowl", fill=red(500, 594), stroke=INK, strokeWidth=4)
d.path("M612,522 C618,510 630,508 638,522", "Cowl light", fill=NONE, stroke="#FFC8B4",
       strokeWidth=4, opacity=40, cap="round")
d.path("M618,446 L632,446 L644,506 L630,508 Z", "Windscreen",
       fill=lin(618, 446, 644, 506, (0, "#DDEEF4"), (1, "#7FA6B6")), opacity=38, stroke=brass(618, 0, 644, 0),
       strokeWidth=4)
line(622, 452, 634, 500, "Windscreen glint", "#FFFFFF", 3, opacity=55)
line(604, 560, 586, 482, "Steering column", lin(0, 482, 0, 560, (0, "#5A3A2A"), (1, "#24140F")), 6)
d.path("M562,486 C566,474 600,466 610,472 C614,478 582,488 566,490 Z", "Steering wheel",
       fill=NONE, stroke=lin(562, 0, 610, 0, (0, "#8A5A34"), (1, "#3A2010")), strokeWidth=5)

# --- hood, radiator, bell, headlamp -----------------------------------------------------
HOOD = "M646,528 L764,532 Q772,533 772,542 L772,594 L646,594 Z"
d.path(HOOD, "Hood", fill=red(528, 594), stroke=INK, strokeWidth=4)
line(648, 530, 768, 534, "Hood hinge", brass(0, 528, 0, 536), 4)
for i in range(6):
    x = 672 + i*15
    line(x, 550, x + 4, 578, f"Louvre {i+1}", "#4A0A06", 4, opacity=55)
    line(x + 3, 550, x + 7, 578, f"Louvre light {i+1}", "#FF9A80", 3, opacity=35)
d.path("M650,584 L768,584 L768,592 L650,592 Z", "Hood shade", fill="#3A0806", opacity=30, stroke=NONE)
d.path(rrect(770, 512, 26, 90, 6), "Radiator", fill=brass(770, 0, 796, 0), stroke=INK, strokeWidth=3)
for i in range(7):
    y = 524 + i*10
    line(774, y, 792, y, f"Radiator fin {i+1}", "#7A4A16", 3, opacity=40)
d.path(rrect(776, 500, 14, 14, 4), "Radiator cap", fill=brass(776, 0, 790, 0), stroke=INK, strokeWidth=2)
# bell on its yoke above the hood
line(668, 530, 668, 496, "Bell post", brass(665, 0, 671, 0), 5)
d.path("M654,494 Q668,484 682,494", "Bell yoke", fill=NONE, stroke=brass(654, 0, 682, 0), strokeWidth=5, cap="round")
d.path("M660,476 C660,468 676,468 676,476 C678,492 683,502 690,508 L646,508 C653,502 658,492 660,476 Z",
       "Bell", fill=brass(646, 470, 690, 508), stroke=INK, strokeWidth=3)
d.path("M664,478 C663,490 659,500 654,505", "Bell glint", fill=NONE, stroke="#FFFBE6",
       strokeWidth=3, opacity=70, cap="round")
d.path(ell(668, 508, 23, 4), "Bell lip", fill=lin(645, 0, 691, 0, (0, "#C98A2E"), (1, "#5A3410")), stroke=INK,
       strokeWidth=2)
circle(668, 516, 4, "Bell clapper", fill=rad((0, "#A87A3A"), (1, "#3A2010")))
circle(668, 467, 4, "Bell crown", fill=brass(664, 463, 672, 471))
# headlamp on its bracket with a soft beam
d.path("M826,512 L888,492 L888,552 L826,532 Z", "Headlamp beam",
       fill=lin(826, 0, 888, 0, (0, "#FFF0B8"), (1, "#FFD68A")), opacity=20, stroke=NONE)
track((888, 492), (888, 552))
line(792, 566, 806, 538, "Lamp bracket", brass(0, 538, 0, 566), 5)
d.path(rrect(792, 506, 30, 32, 8), "Headlamp drum", fill=brass(792, 506, 822, 538), stroke=INK, strokeWidth=3)
d.path(ell(822, 522, 6, 15), "Headlamp lens", fill=rad((0, "#FFFFF0"), (0.6, "#FFE9A6"), (1, "#E0A84E")),
       stroke="#7A4A16", strokeWidth=3)
d.path("M800,512 L800,530", "Drum glint", fill=NONE, stroke="#FFFBE6", strokeWidth=3, opacity=60, cap="round")
circle(806, 502, 4, "Lamp finial", fill=brass(802, 498, 810, 506))

# --- ladder over everything above the body ----------------------------------------------
LX0, LX1, LY0, LY1 = 184, 784, 404, 434
d.path(rrect(LX0 + 6, LY1 + 4, LX1 - LX0, 6, 3), "Ladder shadow", fill="#120A08", opacity=25, stroke=NONE)
x = LX0 + 14
k = 0
while x < LX1 - 6:
    k += 1
    line(x, LY0, x, LY1, f"Ladder rung {k}", lin(0, LY0, 0, LY1, (0, "#E8C890"), (1, "#8A6232")), 4, cap="butt")
    x += 24
for i, y in enumerate([LY0, LY1]):
    d.path(rrect(LX0, y - 4, LX1 - LX0, 8, 4), f"Ladder rail {i+1}",
           fill=lin(0, y - 4, 0, y + 4, (0, "#F2D8A2"), (0.5, "#C0904E"), (1, "#7A5226")), stroke=INK, strokeWidth=2)
for i, x in enumerate([LX0, LX1 - 10]):
    d.path(rrect(x, LY0 - 6, 10, LY1 - LY0 + 12, 3), f"Ladder cap {i+1}", fill=brass(x, 0, x + 10, 0),
           stroke=INK, strokeWidth=2)
track((LX0, LY0 - 6), (LX1, LY0 - 6))

# --- wheels ---------------------------------------------------------------------------
def wheel(cx, cy, r, tag):
    circle(cx, cy, r - 7, f"{tag} tyre", fill=NONE,
           stroke=lin(0, cy - r, 0, cy + r, (0, "#4E3E36"), (1, "#140E0C")), strokeWidth=14)
    d.path(f"M{cx - r + 4},{cy - 6} A{r - 4},{r - 4} 0 0 1 {cx - 6},{cy - r + 4}", f"{tag} tyre light",
           fill=NONE, stroke="#B49E90", strokeWidth=3, opacity=35, cap="round")
    circle(cx, cy, r - 19, f"{tag} felloe", fill=NONE, stroke=red(cy - r, cy + r), strokeWidth=10)
    for k in range(12):
        a = math.radians(k*30 + 8)
        line(cx + 12*math.cos(a), cy + 12*math.sin(a), cx + (r - 22)*math.cos(a), cy + (r - 22)*math.sin(a),
             f"{tag} spoke {k+1}", lin(cx - r, cy - r, cx + r, cy + r, (0, "#E0503A"), (1, "#7A1610")), 7, cap="butt")
    circle(cx, cy, r - 19, f"{tag} pinstripe", fill=NONE, stroke="#EBC45E", strokeWidth=3, opacity=80)
    circle(cx, cy, 15, f"{tag} hub", fill=rad((0, "#FFF2BE"), (0.6, "#D9A441"), (1, "#6A4214")),
           stroke=INK, strokeWidth=3)
    circle(cx - 4, cy - 4, 4, f"{tag} hub glint", fill="#FFFBE6", opacity=70)

WR, WY = 58, GROUND - 58
wheel(330, WY, WR, "Rear wheel")
wheel(692, WY, WR, "Front wheel")

# --- fenders + running board ------------------------------------------------------------
d.path(f"M{330-72},{WY+2} A72,72 0 0 1 {330+72},{WY+2} L{330+60},{WY+2} A60,60 0 0 0 {330-60},{WY+2} Z",
       "Rear fender", fill=red(WY - 72, WY), stroke=INK, strokeWidth=3)
d.path("M616,612 C632,588 654,572 692,572 C744,572 770,604 780,644 L766,644 C756,612 734,586 692,586 "
       "C662,586 642,598 628,616 Z", "Front fender", fill=red(572, 644), stroke=INK, strokeWidth=3)
d.path(f"M{330+70},604 L620,604 L626,616 L{330+66},616 Z", "Running board",
       fill=lin(0, 604, 0, 616, (0, "#7A5040"), (1, "#2E1A12")), stroke=INK, strokeWidth=2)
line(402, 605, 620, 605, "Running board edge", brass(0, 603, 0, 607), 3)
d.path(f"M{330-70},{WY-4} A70,70 0 0 1 {330-20},{WY-66}", "Rear fender light", fill=NONE, stroke="#FFB8A0",
       strokeWidth=3, opacity=45, cap="round")
d.path("M640,590 C654,580 670,576 690,575", "Front fender light", fill=NONE, stroke="#FFB8A0",
       strokeWidth=3, opacity=45, cap="round")

# plate rim + inner ring on top so every edge closes cleanly
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F6D8A8", strokeWidth=3, opacity=30)
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840, fill=NONE, stroke="#5A2A1E", strokeWidth=6)

print(f"fire engine max radius from disc centre: {FAR[0]:.1f} (rim {R})")

# --- caption ----------------------------------------------------------------------------
def caption(txt, label, y, size, color, tracking=0):
    r = d.text(txt, label, x=500, y=y, size=size, font="Virelai Sans", color=color, justify="center")
    if tracking and r and r.get("id") is not None:
        d.cmd("text.setStyle", f"{label} tracking", id=r["id"], tracking=tracking)
    print(label, "->", r)

caption("FIRE ENGINE", "Name", 934, 56, "#F4DCC0")
caption("1924 · PETROL INLINE-SIX", "Spec", 976, 24, "#D9A88A", tracking=280)

d.finish("fire-engine-V1R00")
