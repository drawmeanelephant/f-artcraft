#!/usr/bin/env python3
"""Camper van — field plate V1R00. Profile of a late-1950s split-window microbus
heading right with the pop-top raised: translucent windows with curtain edges,
cream-over-coral paint split by a chrome band, a bicycle on the rear rack.
Coastal dusk plate. 1000x1000. House style: gradients + translucent shading."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Camper Van — Field Plate", 1000, 1000)

INK = "#2A1812"
CX, CY, R = 500, 460, 420
GROUND = 700
FAR = [0.0]


def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}


def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}


def chrome(x0, y0, x1, y1):
    return lin(x0, y0, x1, y1, (0, "#FFFFFF"), (0.3, "#CDD5D8"), (0.55, "#6E7A80"),
               (0.75, "#E6ECEE"), (1, "#8A949A"))


def coral(y0, y1):
    return lin(0, y0, 0, y1, (0, "#F08A6C"), (0.45, "#C64E36"), (1, "#7A2418"))


def cream(y0, y1):
    return lin(0, y0, 0, y1, (0, "#FFF8E8"), (0.6, "#EEDDB8"), (1, "#C8B28A"))


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
    track((cx, cy - r), (cx, cy + r), (cx - r, cy), (cx + r, cy))
    d.shape("ellipse", label, x=cx - r, y=cy - r, width=2*r, height=2*r, **kw)


def line(x0, y0, x1, y1, label, stroke, w, **kw):
    track((x0, y0), (x1, y1))
    d.path(f"M{x0:.1f},{y0:.1f} L{x1:.1f},{y1:.1f}", label, fill=NONE, stroke=stroke,
           strokeWidth=w, cap=kw.pop("cap", "round"), **kw)


# --- backdrop + coastal dusk plate --------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin(0, 0, 0, 1000, (0, "#161A22"), (1, "#07080C")), stroke=NONE)
for i, (x, y, w) in enumerate([(84, 130, 4), (906, 96, 5), (40, 540, 3), (956, 480, 4),
                               (116, 906, 4), (874, 916, 3), (960, 770, 4), (36, 310, 3)]):
    d.shape("ellipse", f"Backdrop fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#F2DCC8", opacity=26, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=lin(500, 40, 500, 700, (0, "#24405E"), (0.5, "#8A6A8A"), (0.8, "#E89E7A"), (1, "#F8CC9C")),
        stroke="#3A2A30", strokeWidth=6)
for i, (r, op) in enumerate([(120, 9), (92, 13), (72, 18)]):
    circle(300, 286, r, f"Sun glow {i+1}", fill="#FFE8C8", opacity=op)
circle(300, 286, 52, "Sun", fill=rad((0, "#FFFCEC"), (0.7, "#FFE0B0"), (1, "#F4B07E")), opacity=90)
for i, (x, y, w, h, op) in enumerate([(520, 230, 250, 18, 20), (180, 380, 220, 14, 16), (600, 330, 200, 14, 18)]):
    d.path(rrect(x, y, w, h, h/2), f"Cloud {i+1}", fill=lin(x, 0, x + w, 0, (0, "#FCE0C8"), (1, "#C88A9A")),
           opacity=op, stroke=NONE)
for i, (x, y, s) in enumerate([(640, 280, 14), (676, 300, 10), (440, 220, 9)]):
    d.path(f"M{x-s},{y-s*0.3} Q{x-s*0.5},{y-s*0.7} {x},{y} Q{x+s*0.5},{y-s*0.7} {x+s},{y-s*0.3}",
           f"Gull {i+1}", fill=NONE, stroke="#3A2A36", strokeWidth=3, opacity=70, cap="round")

# sea between the disc walls, headland and pines on the shore
SEA = 612
sl, sr = CX - chord_x(SEA), CX + chord_x(SEA)
L, Rr = CX - chord_x(GROUND), CX + chord_x(GROUND)
d.path(f"M{sl:.1f},{SEA} L{sr:.1f},{SEA} A{R},{R} 0 0 1 {Rr:.1f},{GROUND} L{L:.1f},{GROUND} "
       f"A{R},{R} 0 0 1 {sl:.1f},{SEA} Z", "Sea",
       fill=lin(0, SEA, 0, GROUND, (0, "#5A8A9A"), (1, "#2A4E5E")), opacity=85, stroke=NONE)
line(sl + 10, SEA + 1, sr - 10, SEA + 1, "Horizon light", "#FFE6C8", 3, opacity=50)
for i, (x, y, w, op) in enumerate([(230, 630, 60, 35), (300, 646, 44, 30), (250, 664, 70, 24), (320, 680, 40, 20),
                                   (820, 640, 30, 30), (790, 664, 44, 22)]):
    line(x - w/2, y, x + w/2, y, f"Sea glint {i+1}", "#FFE8C8", 3, opacity=op)
d.path(f"M790,{SEA} C810,586 836,566 862,562 C876,560 886,570 {sr - 6:.1f},590 L{sr:.1f},{SEA} Z", "Headland",
       fill=lin(0, 560, 0, SEA, (0, "#5A4458"), (1, "#3A2E40")), opacity=85, stroke=NONE)
for i, (x, h) in enumerate([(132, 70), (156, 92), (182, 64)]):
    base = SEA + 4
    d.path(f"M{x},{base-h} L{x+16},{base} L{x-16},{base} Z", f"Pine {i+1}",
           fill=lin(0, base - h, 0, base, (0, "#3A3446"), (1, "#22202E")), opacity=85, stroke=NONE)
    track((x - 16, base))

# --- road closing on the disc arc ----------------------------------------------------------
d.path(f"M{L:.1f},{GROUND} L{Rr:.1f},{GROUND} A{R},{R} 0 0 1 {L:.1f},{GROUND} Z", "Road",
       fill=lin(0, GROUND, 0, 880, (0, "#6A5A5A"), (0.5, "#443838"), (1, "#261E22")), stroke=NONE)
line(L + 8, GROUND + 1, Rr - 8, GROUND + 1, "Road edge light", "#F8D2A8", 3, opacity=45)
half = chord_x(768) - 50
x = CX - half
k = 0
while x + 40 < CX + half:
    k += 1
    d.path(rrect(x, 764, 40, 8, 4), f"Centre dash {k}", fill=lin(x, 0, x + 40, 0, (0, "#F8E2B8"), (1, "#D8B880")),
           opacity=60, stroke=NONE)
    x += 72
for i, (y, op) in enumerate([(812, 18), (846, 14)]):
    hw = chord_x(y) - 40
    line(CX - hw, y, CX + hw, y, f"Road seam {i+1}", "#140E10", 3, opacity=op)
d.shape("ellipse", "Van shadow", x=180, y=690, width=640, height=24, fill="#0E0A0C", opacity=45, stroke=NONE)

# --- pop-top: canvas walls then the lifted roof cap ---------------------------------------
d.path("M396,474 L404,420 L644,420 L652,474 Z", "Pop-top canvas",
       fill=lin(0, 420, 0, 474, (0, "#F6C88A"), (1, "#D8904E")), stroke=INK, strokeWidth=3)
for i, x in enumerate(range(416, 640, 18)):
    line(x, 424, x - 1, 470, f"Canvas stripe {i+1}", "#B86A30", 3, opacity=30)
d.path(rrect(470, 432, 104, 30, 8), "Canvas mesh window", fill=lin(470, 432, 574, 462, (0, "#3A2E30"),
       (1, "#5A4446")), opacity=45, stroke="#8A5A30", strokeWidth=3)
for i, x in enumerate(range(480, 570, 10)):
    line(x, 436, x, 458, f"Mesh line {i+1}", "#F6D8A8", 3, opacity=18)
line(404, 424, 408, 470, "Canvas fold shade", "#7A4420", 4, opacity=30)
d.path("M372,422 C372,410 386,404 404,404 L648,404 C664,404 676,410 676,422 Z", "Pop-top cap",
       fill=cream(404, 422), stroke=INK, strokeWidth=3)
line(392, 409, 652, 409, "Cap light", "#FFFFFF", 3, opacity=55)
for i, (x0, x1) in enumerate([(412, 400), (636, 648)]):
    line(x0, 424, x1, 470, f"Pop-top strut {i+1}", chrome(min(x0, x1), 424, max(x0, x1), 470), 3)
track((372, 404), (676, 404))

# --- body: coral lower, cream upper, chrome band ------------------------------------------
BODY = ("M290,642 C276,642 270,632 270,618 L270,504 C270,482 284,470 306,470 L730,470 "
        "C766,470 786,490 790,524 L796,604 C798,628 790,642 772,642 Z")
UPPER = ("M270,562 L270,504 C270,482 284,470 306,470 L730,470 C766,470 786,490 790,524 "
         "L795,590 C760,584 728,566 696,562 Z")
d.path(BODY, "Body", fill=coral(470, 642), stroke=NONE)
d.path(UPPER, "Body upper", fill=cream(470, 590), stroke=NONE)
d.path("M276,632 L790,632 C790,638 784,642 772,642 L290,642 C282,642 276,638 276,632 Z", "Rocker shade",
       fill="#3A0E08", opacity=35, stroke=NONE)
d.path("M282,480 C300,474 320,474 340,474 L724,474 C750,474 770,484 780,500", "Roof light",
       fill=NONE, stroke="#FFFFFF", strokeWidth=5, opacity=40, cap="round")
d.path("M272,562 L696,562 C728,566 760,584 795,590", "Chrome band", fill=NONE,
       stroke=chrome(0, 556, 0, 568), strokeWidth=8, cap="round")
d.path(BODY, "Body outline", fill=NONE, stroke=INK, strokeWidth=4)
line(278, 480, 758, 480, "Rain gutter", chrome(0, 478, 0, 482), 3, opacity=80)

# engine louvres on the rear quarter
for i in range(7):
    y = 492 + i*7
    line(296, y, 336, y, f"Louvre {i+1}", "#7A6440", 3, opacity=55)
    line(296, y + 2, 336, y + 2, f"Louvre light {i+1}", "#FFFFFF", 3, opacity=25)

# side windows with gathered curtains: the plate reads through the glass
def window(x0, x1, tag, curtains=True):
    dd = rrect(x0, 488, x1 - x0, 54, 8)
    d.path(dd, f"{tag} glass", fill=lin(x0, 488, x1, 542, (0, "#FFF4E0"), (1, "#7AA6B4")), opacity=40, stroke=NONE)
    if curtains:
        for side, xs in enumerate([x0 + 2, x1 - 2]):
            sgn = 1 if side == 0 else -1
            w = 18
            edge = " ".join(f"Q{xs + sgn*(w + (5 if j % 2 else -2))},{494 + j*9 + 4.5} {xs + sgn*w},{494 + (j+1)*9}"
                            for j in range(5))
            d.path(f"M{xs},{492} L{xs + sgn*w},{492} {edge} L{xs},{539} Z", f"{tag} curtain {side+1}",
                   fill=lin(xs, 0, xs + sgn*w, 0, (0, "#F4E8C8"), (1, "#E0C890")), opacity=78, stroke=NONE)
            for j in (6, 12):
                line(xs + sgn*j, 496, xs + sgn*j, 536, f"{tag} pleat {side+1}-{j}", "#A88A50", 3, opacity=40)
        line(x0 + 4, 492, x1 - 4, 492, f"{tag} curtain rod", "#8A6A3A", 3, opacity=60)
    line(x0 + 26, 500, x0 + 44, 520, f"{tag} glint", "#FFFFFF", 3, opacity=45)
    d.path(dd, f"{tag} frame", fill=NONE, stroke=chrome(x0, 488, x1, 542), strokeWidth=4)


window(352, 432, "Window 1")
window(446, 526, "Window 2")
window(540, 620, "Window 3")
d.path("M668,488 L734,488 C754,488 766,498 772,514 L780,542 L668,542 Z", "Cab glass",
       fill=lin(668, 488, 780, 542, (0, "#FFF4E0"), (1, "#7AA6B4")), opacity=40, stroke=NONE)
d.path("M690,542 C690,524 708,514 724,516", "Steering wheel through glass", fill=NONE, stroke="#2A2A30",
       strokeWidth=5, opacity=40, cap="round")
line(690, 498, 712, 522, "Cab glint", "#FFFFFF", 3, opacity=45)
d.path("M668,488 L734,488 C754,488 766,498 772,514 L780,542 L668,542 Z", "Cab frame", fill=NONE,
       stroke=chrome(668, 488, 780, 542), strokeWidth=4)
line(700, 488, 700, 542, "Vent window post", chrome(697, 0, 703, 0), 3)

# doors, seams and handles
d.path("M442,482 L626,482 L626,632 L442,632 Z", "Cargo door seam", fill=NONE, stroke="#5A2A1A", strokeWidth=3,
       opacity=40)
line(534, 482, 534, 632, "Cargo door centre seam", "#5A2A1A", 3, opacity=40)
d.path("M662,482 L662,632 M662,632 L784,632", "Cab door seam", fill=NONE, stroke="#5A2A1A", strokeWidth=3,
       opacity=40)
for i, x in enumerate([514, 548, 674]):
    d.path(rrect(x, 576, 18, 6, 3), f"Door handle {i+1}", fill=chrome(x, 576, x + 18, 582), stroke=INK,
           strokeWidth=1)
# nose lamps + bumpers
d.path(ell(796, 606, 6, 14), "Headlamp bezel", fill=chrome(790, 592, 802, 620), stroke=INK, strokeWidth=2)
d.path(ell(799, 606, 3, 10), "Headlamp lens", fill=rad((0, "#FFFFF4"), (1, "#F2D08A")), stroke=NONE)
circle(791, 574, 4, "Indicator", fill=rad((0, "#FFE0A0"), (1, "#E08A30")))
d.path(rrect(782, 624, 30, 12, 5), "Front bumper", fill=chrome(0, 624, 0, 636), stroke=INK, strokeWidth=2)
d.path(rrect(254, 622, 28, 12, 5), "Rear bumper", fill=chrome(0, 622, 0, 634), stroke=INK, strokeWidth=2)
track((812, 636))

# --- wheel wells + wheels -------------------------------------------------------------------
WR, WY = 44, GROUND - 44
for cx in (370, 700):
    dx = math.sqrt(52**2 - (642 - WY)**2)
    d.path(f"M{cx - dx:.1f},642 A52,52 0 0 1 {cx + dx:.1f},642 Z", f"Wheel well {cx}",
           fill=lin(0, WY - 52, 0, 642, (0, "#0A0604"), (1, "#2A1410")), stroke=NONE)


def wheel(cx, cy, r, tag):
    circle(cx, cy, r - 7, f"{tag} tyre", fill=NONE,
           stroke=lin(0, cy - r, 0, cy + r, (0, "#4A3C38"), (1, "#120C0C")), strokeWidth=14)
    d.path(f"M{cx - r + 5},{cy - 6} A{r - 5},{r - 5} 0 0 1 {cx - 6},{cy - r + 5}", f"{tag} tyre light",
           fill=NONE, stroke="#A89088", strokeWidth=3, opacity=40, cap="round")
    circle(cx, cy, r - 14, f"{tag} rim", fill=cream(cy - r, cy + r))
    for k in range(5):
        a = math.radians(k*72 - 90)
        circle(cx + 21*math.cos(a), cy + 21*math.sin(a), 2.5, f"{tag} lug {k+1}", fill="#7A6A4A", opacity=70)
    circle(cx, cy, 15, f"{tag} hubcap", fill=chrome(cx - 15, cy - 15, cx + 15, cy + 15), stroke=INK, strokeWidth=2)
    circle(cx - 4, cy - 5, 3, f"{tag} hubcap glint", fill="#FFFFFF", opacity=80)


wheel(370, WY, WR, "Rear wheel")
wheel(700, WY, WR, "Front wheel")

# --- rear rack and bicycle --------------------------------------------------------------------
line(272, 548, 182, 548, "Rack top bar", chrome(0, 545, 0, 551), 5)
line(272, 636, 150, 636, "Rack tray", chrome(0, 633, 0, 639), 5)
line(186, 548, 186, 636, "Rack post", chrome(183, 0, 189, 0), 5)
BW = 34
BRX, BFX, BY = 166, 268, 600
FRAME = lin(160, 540, 270, 610, (0, "#9AD8C8"), (1, "#3A8A7A"))


def bike_wheel(cx, cy, tag):
    for k in range(12):
        a = math.radians(k*30)
        line(cx, cy, cx + (BW - 4)*math.cos(a), cy + (BW - 4)*math.sin(a), f"{tag} spoke {k+1}",
             "#E8ECEE", 3, opacity=55, cap="butt")
    circle(cx, cy, BW - 3, f"{tag} rim", fill=NONE, stroke=chrome(cx - BW, cy - BW, cx + BW, cy + BW), strokeWidth=3)
    circle(cx, cy, BW, f"{tag} tyre", fill=NONE, stroke="#1E1614", strokeWidth=5)
    circle(cx, cy, 5, f"{tag} hub", fill=chrome(cx - 5, cy - 5, cx + 5, cy + 5))


bike_wheel(BRX, BY, "Bike rear wheel")
bike_wheel(BFX, BY, "Bike front wheel")
BB, ST, HT, HB = (210, 606), (196, 552), (252, 554), (256, 570)
for i, (a, b) in enumerate([(BB, ST), (ST, HT), (BB, HB), (BB, (BRX, BY)), (ST, (BRX, BY))]):
    line(*a, *b, f"Bike tube {i+1}", FRAME, 5)
line(*HT, *HB, "Bike head tube", FRAME, 6)
line(*HB, BFX, BY, "Bike fork", chrome(256, 570, 268, 600), 4)
d.path(f"M{HT[0]},{HT[1]} L{HT[0]-4},{HT[1]-14} Q{HT[0]+6},{HT[1]-20} {HT[0]+14},{HT[1]-12}", "Bike handlebar",
       fill=NONE, stroke=chrome(240, 530, 270, 556), strokeWidth=4, cap="round")
line(ST[0], ST[1], ST[0] - 4, ST[1] - 8, "Bike seat post", chrome(190, 540, 198, 552), 3)
d.path(f"M{ST[0]-18},{ST[1]-10} C{ST[0]-12},{ST[1]-16} {ST[0]+6},{ST[1]-15} {ST[0]+10},{ST[1]-10} "
       f"L{ST[0]-18},{ST[1]-8} Z", "Bike saddle", fill=lin(0, ST[1] - 16, 0, ST[1] - 8, (0, "#6A4A3A"), (1, "#2A1A14")),
       stroke=NONE)
circle(BB[0], BB[1], 8, "Bike chainring", fill=NONE, stroke=chrome(BB[0] - 8, BB[1] - 8, BB[0] + 8, BB[1] + 8),
       strokeWidth=3)
line(BB[0], BB[1], BB[0] + 8, BB[1] + 10, "Bike crank", "#2A2A30", 3)
line(186, 552, 198, 552, "Rack hook", chrome(0, 549, 0, 555), 4)

d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#FFE2C8", strokeWidth=3, opacity=30)
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840, fill=NONE, stroke="#3A2A30", strokeWidth=6)

print(f"camper max radius from disc centre: {FAR[0]:.1f} (rim {R})")


def caption(txt, label, y, size, color, tracking=0):
    r = d.text(txt, label, x=500, y=y, size=size, font="Virelai Sans", color=color, justify="center")
    if tracking and r and r.get("id") is not None:
        d.cmd("text.setStyle", f"{label} tracking", id=r["id"], tracking=tracking)


caption("CAMPER VAN", "Name", 934, 56, "#F8E2CC")
caption("1958 · AIR-COOLED FLAT-FOUR", "Spec", 976, 24, "#E0A890", tracking=280)

d.finish("camper-van-V1R00")
