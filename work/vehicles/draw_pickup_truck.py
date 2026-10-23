#!/usr/bin/env python3
"""Pickup truck — field plate V1R00. Near-profile of a 1950s stepside pickup
heading right: rounded fenders over the wheels, wooden stake rails on the bed,
a crate loaded and strapped down, dust kicking up behind. Dust-orange desert
plate with mesas. 1000x1000. House style: gradients + translucent shading."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Pickup Truck — Field Plate", 1000, 1000)

INK = "#24160E"
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
    return lin(x0, y0, x1, y1, (0, "#FFFFFF"), (0.3, "#C9D2D6"), (0.55, "#6E7A80"),
               (0.75, "#E4EAEC"), (1, "#8A949A"))


def paint(y0, y1):
    return lin(0, y0, 0, y1, (0, "#8CC0B4"), (0.45, "#4F857A"), (1, "#1F423C"))


def wood(x0, y0, x1, y1):
    return lin(x0, y0, x1, y1, (0, "#E8C48A"), (0.5, "#B98A50"), (1, "#7A5428"))


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


# --- backdrop + dust-orange plate -----------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin(0, 0, 0, 1000, (0, "#22160E"), (1, "#0C0705")), stroke=NONE)
for i, (x, y, w) in enumerate([(80, 140, 4), (910, 100, 5), (36, 560, 3), (958, 500, 4),
                               (120, 910, 4), (870, 920, 3), (962, 780, 4), (40, 320, 3)]):
    d.shape("ellipse", f"Backdrop fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#F6D2A0", opacity=26, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=lin(500, 40, 500, 720, (0, "#B8603A"), (0.4, "#DE8A4E"), (0.8, "#F2B672"), (1, "#F8D49A")),
        stroke="#5A2E16", strokeWidth=6)

# high sun, heat haze bands
for i, (r, op) in enumerate([(140, 9), (108, 13), (84, 18)]):
    circle(660, 260, r, f"Sun glow {i+1}", fill="#FFF0C8", opacity=op)
circle(660, 260, 60, "Sun", fill=rad((0, "#FFFCEC"), (0.7, "#FFE6B0"), (1, "#F8C27E")), opacity=90)
for i, (y, w, op) in enumerate([(380, 300, 14), (430, 380, 12), (480, 440, 10)]):
    x = CX - w/2 + (i - 1)*40
    d.path(rrect(x, y, w, 10, 5), f"Haze band {i+1}", fill=lin(x, 0, x + w, 0, (0, "#FFE8C0"), (1, "#E8A060")),
           opacity=op, stroke=NONE)

# mesas: far range pale, near buttes darker, both closing on the ground chord
L, Rr = CX - chord_x(GROUND), CX + chord_x(GROUND)
far = (f"M{L:.1f},{GROUND} L{L:.1f},600 L148,596 L162,540 L236,536 L250,588 L330,584 L344,612 L420,616 "
       f"L436,600 L520,598 L534,622 L640,626 L654,572 L760,568 L770,530 L792,512 L870,510 L884,560 "
       f"L{Rr-4:.1f},600 L{Rr:.1f},{GROUND} Z")
d.path(far, "Mesas far", fill=lin(0, 500, 0, GROUND, (0, "#B8603A"), (1, "#9A4E30")), opacity=55, stroke=NONE)
for i, (x0, x1, y) in enumerate([(164, 234, 552), (794, 868, 526)]):
    line(x0 + 4, y, x1 - 4, y, f"Far strata {i+1}", "#F8C890", 3, opacity=30)
near = (f"M{L:.1f},{GROUND} L{L+4:.1f},660 L236,656 L250,614 L312,612 L326,648 L560,652 L700,654 "
        f"L716,626 L800,622 L812,650 L{Rr-4:.1f},654 L{Rr:.1f},{GROUND} Z")
d.path(near, "Mesas near", fill=lin(0, 610, 0, GROUND, (0, "#9A4E30"), (1, "#7A3A22")), opacity=75, stroke=NONE)
for i, (x0, x1, y) in enumerate([(250, 312, 622), (716, 800, 634)]):
    line(x0 + 4, y, x1 - 4, y, f"Butte strata {i+1}", "#F2B07A", 3, opacity=35)
# fence posts marching along the horizon
for i, x in enumerate(range(560, 840, 36)):
    line(x, 680, x, 666, f"Fence post {i+1}", "#5A2E1A", 3, opacity=60)
line(560, 670, 830, 670, "Fence wire", "#5A2E1A", 3, opacity=35)

# --- dirt road closing on the disc arc --------------------------------------------------
d.path(f"M{L:.1f},{GROUND} L{Rr:.1f},{GROUND} A{R},{R} 0 0 1 {L:.1f},{GROUND} Z", "Road",
       fill=lin(0, GROUND, 0, 880, (0, "#B8784A"), (0.5, "#8A5232"), (1, "#5A321E")), stroke=NONE)
line(L + 8, GROUND + 1, Rr - 8, GROUND + 1, "Road crown light", "#FFD8A0", 3, opacity=45)
for i, (y, op) in enumerate([(728, 30), (768, 24), (812, 18)]):
    half = chord_x(y) - 40
    line(CX - half, y, CX + half, y, f"Rut {i+1}", "#5A2E1A", 4, opacity=op)
    line(CX - half + 20, y + 5, CX + half - 20, y + 5, f"Rut light {i+1}", "#F2B880", 3, opacity=op - 6)
for i, (x, y, w) in enumerate([(300, 742, 10), (420, 790, 8), (620, 752, 12), (700, 800, 7), (250, 790, 6),
                               (540, 830, 9), (760, 740, 8), (380, 846, 6)]):
    d.path(ell(x, y, w, w*0.6), f"Pebble {i+1}", fill=rad((0, "#E8B07A"), (1, "#7A4428")), opacity=60, stroke=NONE)
d.shape("ellipse", "Truck shadow", x=200, y=690, width=610, height=24, fill="#2A1408", opacity=40, stroke=NONE)

# dust kicking up behind the rear wheel
for i, (x, y, r, op) in enumerate([(176, 640, 34, 16), (214, 668, 30, 22), (156, 600, 26, 12), (240, 690, 22, 26),
                                   (196, 618, 22, 18), (148, 660, 20, 14)]):
    circle(x, y, r, f"Dust {i+1}", fill=rad((0, "#FFF0D8"), (1, "#E0A878")), opacity=op + 10)

# --- bed: stake rails behind, then the box ----------------------------------------------
BX0, BX1, BTOP, BBOT = 218, 466, 566, 630
for i, x in enumerate([232, 300, 372, 444]):
    d.path(rrect(x, 506, 12, 62, 2), f"Stake {i+1}", fill=wood(x, 0, x + 12, 0), stroke=INK, strokeWidth=2)
for i, y in enumerate([512, 538]):
    d.path(rrect(BX0 + 4, y, BX1 - BX0 - 8, 14, 3), f"Rail board {i+1}", fill=wood(0, y, 0, y + 14),
           stroke=INK, strokeWidth=2)
    line(BX0 + 14, y + 7, BX1 - 14, y + 7, f"Rail grain {i+1}", "#7A5428", 3, opacity=30)
# crate riding in the bed, strapped down
CRX, CRY, CRW, CRH = 284, 462, 120, 104
d.path(rrect(CRX, CRY, CRW, CRH, 3), "Crate", fill=wood(CRX, CRY, CRX + CRW, CRY + CRH), stroke=INK, strokeWidth=3)
for i in range(1, 4):
    y = CRY + i*CRH/4
    line(CRX + 3, y, CRX + CRW - 3, y, f"Crate plank seam {i}", "#6A4420", 3, opacity=50)
d.path(f"M{CRX+6},{CRY+6} L{CRX+CRW-6},{CRY+CRH-6}", "Crate brace", fill=NONE,
       stroke=wood(CRX, 0, CRX + CRW, 0), strokeWidth=10, cap="butt")
d.path(f"M{CRX+6},{CRY+6} L{CRX+CRW-6},{CRY+CRH-6}", "Crate brace edge", fill=NONE,
       stroke="#5A3816", strokeWidth=3, opacity=40, cap="butt")
for i, x in enumerate([CRX, CRX + CRW - 10]):
    d.path(rrect(x, CRY, 10, CRH, 2), f"Crate corner post {i+1}", fill=wood(x, 0, x + 10, 0), stroke=INK,
           strokeWidth=2)
d.path(f"M{CRX},{CRY} L{CRX+CRW},{CRY} L{CRX+CRW},{CRY+12} L{CRX},{CRY+12} Z", "Crate top light",
       fill="#FFF0D0", opacity=22, stroke=NONE)
# stencilled up-arrows
for i, x in enumerate([CRX + 36, CRX + 60]):
    d.path(f"M{x},{CRY+40} L{x},{CRY+22} M{x-7},{CRY+29} L{x},{CRY+22} L{x+7},{CRY+29}", f"Stencil arrow {i+1}",
           fill=NONE, stroke="#4A2C14", strokeWidth=3, opacity=55, cap="round")
# straps over the crate down to the bed hooks
for i, (x0, x1) in enumerate([(CRX + 26, CRX - 8), (CRX + CRW - 26, CRX + CRW + 8)]):
    d.path(f"M{x0},{CRY-2} L{x1},{BTOP+2}", f"Strap {i+1}", fill=NONE,
           stroke=lin(0, CRY, 0, BTOP, (0, "#E8D2A0"), (1, "#A88A5A")), strokeWidth=7, cap="butt")
    track((x0, CRY - 2))
d.path(f"M{CRX+26},{CRY-2} L{CRX+CRW-26},{CRY-2}", "Strap over top", fill=NONE,
       stroke=lin(0, CRY - 6, 0, CRY + 2, (0, "#F2E0B4"), (1, "#B8985E")), strokeWidth=7, cap="butt")
for i, x in enumerate([CRX + 2, CRX + CRW - 2]):
    d.path(rrect(x - 6, 506, 12, 12, 2), f"Strap buckle {i+1}", fill=NONE, stroke=chrome(x - 6, 506, x + 6, 518),
           strokeWidth=3)

d.path(f"M{BX0},{BTOP} L{BX1},{BTOP} L{BX1},{BBOT} L{BX0+8},{BBOT} Q{BX0},{BBOT} {BX0},{BBOT-8} Z", "Bed side",
       fill=paint(BTOP, BBOT), stroke=INK, strokeWidth=4)
d.path(rrect(BX0, BTOP - 4, BX1 - BX0, 8, 3), "Bed cap rail", fill=chrome(0, BTOP - 4, 0, BTOP + 4),
       stroke=INK, strokeWidth=2)
d.path(f"M{BX0+6},{BBOT-14} L{BX1-4},{BBOT-14} L{BX1-4},{BBOT-4} L{BX0+6},{BBOT-4} Z", "Bed side shade",
       fill="#0E2420", opacity=30, stroke=NONE)
d.path(rrect(BX0 - 10, BTOP + 2, 12, BBOT - BTOP - 4, 3), "Tailgate", fill=paint(BTOP, BBOT), stroke=INK,
       strokeWidth=3)
d.path(f"M{BX0-4},{BTOP+8} Q{BX0+20},{BTOP+30} {BX0+4},{BTOP+46}", "Tailgate chain", fill=NONE,
       stroke=chrome(BX0 - 4, BTOP, BX0 + 20, BTOP + 46), strokeWidth=3, dash=[4, 3])
circle(BX0 + 4, BBOT - 30, 6, "Tail lamp", fill=rad((0, "#FFB090"), (0.6, "#C83020"), (1, "#5A0E08")),
       stroke=INK, strokeWidth=2)

# --- frame + running board --------------------------------------------------------------
d.path(rrect(220, 626, 556, 14, 4), "Frame rail", fill=lin(0, 626, 0, 640, (0, "#4A3428"), (1, "#1A100A")),
       stroke=NONE)
d.path(rrect(392, 632, 222, 12, 4), "Running board", fill=lin(0, 632, 0, 644, (0, "#5A4436"), (1, "#20140C")),
       stroke=INK, strokeWidth=2)
line(398, 633, 608, 633, "Running board edge", chrome(0, 631, 0, 635), 3)

# --- cab --------------------------------------------------------------------------------
CAB = ("M474,636 L474,486 C474,462 488,450 512,450 L566,450 C584,450 594,458 602,476 L620,530 "
       "L620,636 Z")
d.path(CAB, "Cab", fill=paint(450, 636), stroke=INK, strokeWidth=4)
d.path("M482,460 C490,454 500,454 512,454 L562,454 C576,454 586,460 592,470", "Roof light", fill=NONE,
       stroke="#DFF4EE", strokeWidth=5, opacity=40, cap="round")
# cab glazing: the plate reads through
d.path("M490,470 L574,470 C582,470 586,474 589,482 L603,526 L490,526 Z", "Side window",
       fill=lin(490, 470, 600, 526, (0, "#FFF2D8"), (1, "#7AA0A8")), opacity=42, stroke=chrome(490, 470, 600, 526),
       strokeWidth=4)
d.path("M540,526 C540,510 556,500 572,502", "Steering wheel through glass", fill=NONE, stroke="#1A2A28",
       strokeWidth=5, opacity=45, cap="round")
line(542, 470, 542, 526, "Vent window post", chrome(539, 0, 545, 0), 4)
line(500, 480, 520, 500, "Glass glint 1", "#FFFFFF", 3, opacity=50)
line(552, 478, 576, 502, "Glass glint 2", "#FFFFFF", 3, opacity=40)
d.path("M484,534 L612,534 L612,628 L484,628 Z", "Door panel", fill=NONE, stroke="#16302C", strokeWidth=3, opacity=55)
d.path(rrect(586, 548, 18, 6, 3), "Door handle", fill=chrome(586, 548, 604, 554), stroke=INK, strokeWidth=1)
line(480, 560, 616, 560, "Beltline crease light", "#C8EEE4", 3, opacity=40)
# mirror on its arm
line(604, 484, 624, 470, "Mirror arm", chrome(604, 470, 624, 484), 3)
d.path(ell(628, 466, 7, 10), "Mirror", fill=chrome(621, 456, 635, 476), stroke=INK, strokeWidth=2)

# --- hood, grille, bumper ---------------------------------------------------------------
HOOD = "M616,530 C664,520 724,522 762,540 C776,548 782,562 782,580 L782,636 L616,636 Z"
d.path(HOOD, "Hood", fill=paint(520, 636), stroke=INK, strokeWidth=4)
d.path("M624,532 C668,524 724,526 758,542", "Hood light", fill=NONE, stroke="#DFF4EE", strokeWidth=5,
       opacity=40, cap="round")
for i in range(3):
    x = 656 + i*20
    line(x, 566, x + 12, 566, f"Hood vent {i+1}", chrome(x, 563, x + 12, 569), 4)
d.path("M770,552 C780,556 788,566 790,580 L790,626 L776,626 L776,560 Z", "Grille",
       fill=chrome(770, 552, 790, 626), stroke=INK, strokeWidth=3)
for i in range(5):
    y = 570 + i*11
    line(778, y, 788, y, f"Grille bar {i+1}", "#3A4448", 3, opacity=55)

# --- fenders + wheels ---------------------------------------------------------------------
WR, WY = 50, GROUND - 50
RWX, FWX = 330, 690


def wheel(cx, cy, r, tag):
    circle(cx, cy, r - 8, f"{tag} tyre", fill=NONE,
           stroke=lin(0, cy - r, 0, cy + r, (0, "#4A3C34"), (1, "#120C08")), strokeWidth=16)
    d.path(f"M{cx - r + 5},{cy - 6} A{r - 5},{r - 5} 0 0 1 {cx - 6},{cy - r + 5}", f"{tag} tyre light",
           fill=NONE, stroke="#A89080", strokeWidth=3, opacity=40, cap="round")
    circle(cx, cy, r - 15, f"{tag} whitewall", fill=NONE, stroke=lin(0, cy - r, 0, cy + r, (0, "#FFFCF2"),
           (1, "#C8BEA8")), strokeWidth=6)
    circle(cx, cy, r - 18, f"{tag} rim", fill=rad((0, "#F2E8D0"), (0.7, "#D8C8A4"), (1, "#8A7A5A")))
    for k in range(5):
        a = math.radians(k*72 - 90)
        circle(cx + 11*math.cos(a), cy + 11*math.sin(a), 2.5, f"{tag} lug {k+1}", fill="#5A4A34", opacity=70)
    circle(cx, cy, 14, f"{tag} hubcap", fill=chrome(cx - 14, cy - 14, cx + 14, cy + 14), stroke=INK, strokeWidth=2)
    circle(cx - 4, cy - 5, 3, f"{tag} hubcap glint", fill="#FFFFFF", opacity=80)


def fender(cx, x0, x1, top, label, lip):
    dd = (f"M{x0},{WY + 4} C{x0},{top + 26} {cx - 40},{top} {cx},{top} "
          f"C{cx + 40},{top} {x1},{top + 26} {x1},{WY + 4} Z")
    d.path(dd, label, fill=paint(top, WY + 4), stroke=INK, strokeWidth=4)
    d.path(f"M{cx - 58},{WY + 4} A58,58 0 0 1 {cx + 58},{WY + 4} Z", f"{label} well",
           fill=lin(0, WY - 58, 0, WY, (0, "#0A0604"), (1, "#2A1A10")), stroke=NONE)
    d.path(f"M{x0 + 8},{WY - 10} C{x0 + 10},{top + 30} {cx - 36},{top + 6} {cx},{top + 6}", f"{label} light",
           fill=NONE, stroke="#DFF4EE", strokeWidth=4, opacity=lip, cap="round")
    track((cx, top), (x0, WY), (x1, WY))


fender(RWX, 262, 406, 578, "Rear fender", 40)
wheel(RWX, WY, WR, "Rear wheel")
fender(FWX, 604, 790, 570, "Front fender", 45)
wheel(FWX, WY, WR, "Front wheel")
# headlamp set into the nose of the front fender
d.path(ell(774, 596, 9, 18), "Headlamp bezel", fill=chrome(765, 578, 783, 614), stroke=INK, strokeWidth=2)
d.path(ell(778, 596, 5, 13), "Headlamp lens", fill=rad((0, "#FFFFF4"), (0.7, "#FFEAB0"), (1, "#D8A860")),
       stroke=NONE)
circle(758, 616, 4, "Parking lamp", fill=rad((0, "#FFF0C0"), (1, "#E09040")))
# bumpers
d.path(rrect(770, 630, 34, 14, 6), "Front bumper", fill=chrome(0, 630, 0, 644), stroke=INK, strokeWidth=2)
d.path(rrect(198, 628, 30, 12, 5), "Rear bumper", fill=chrome(0, 628, 0, 640), stroke=INK, strokeWidth=2)
track((804, 644), (198, 628))
# exhaust tip + puff
d.path(rrect(232, 640, 22, 6, 3), "Tailpipe", fill=chrome(0, 640, 0, 646), stroke=NONE)

d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#FFE2B8", strokeWidth=3, opacity=30)
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840, fill=NONE, stroke="#5A2E16", strokeWidth=6)

print(f"pickup max radius from disc centre: {FAR[0]:.1f} (rim {R})")


def caption(txt, label, y, size, color, tracking=0):
    r = d.text(txt, label, x=500, y=y, size=size, font="Virelai Sans", color=color, justify="center")
    if tracking and r and r.get("id") is not None:
        d.cmd("text.setStyle", f"{label} tracking", id=r["id"], tracking=tracking)


caption("PICKUP TRUCK", "Name", 934, 56, "#F8DEC0")
caption("1953 · INLINE-SIX · 3-SPEED", "Spec", 976, 24, "#E0A878", tracking=280)

d.finish("pickup-truck-V1R00")
