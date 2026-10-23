#!/usr/bin/env python3
"""Platypus — field-guide plate V1R00. Front-quarter view, floating at the
surface and heading left toward the viewer: broad flat slate-blue bill out
front (top plane + lip edge so it reads as a paddle), wet chocolate fur,
beaver-paddle tail behind, webbed feet glimpsed through the water, a dragonfly
for it to eye. Billabong dusk palette; the water band closes on the disc's
own arc. 1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Platypus — Field Plate", 1000, 1000)

INK = "#2A1A12"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#12303A"}, {"offset": 1, "color": "#050F14"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F4EBD2"}, {"offset": 0.6, "color": "#BCCFC2"},
    {"offset": 1, "color": "#5F8682"}]}}
WATER_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4F8C93"}, {"offset": 1, "color": "#1E4A56"}]}}
FUR_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#A0704A"}, {"offset": 0.62, "color": "#6A4228"},
    {"offset": 1, "color": "#3A2214"}]}}
TAIL_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7A5034"}, {"offset": 1, "color": "#3E2416"}]}}
BILL_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#AEBFCE"}, {"offset": 0.6, "color": "#7A8EA4"},
    {"offset": 1, "color": "#50627A"}]}}
LIP_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4E5E72"}, {"offset": 1, "color": "#2A3646"}]}}
FOOT_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6A5A50"}, {"offset": 1, "color": "#3A2E28"}]}}
REED_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7E9C84"}, {"offset": 1, "color": "#4E6E5E"}]}}
WING_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#FFFFFF"}, {"offset": 1, "color": "#BFE0E4"}]}}

WATER_Y = 610
CX, CY, R = 500, 460, 420
def disc_x(y):
    return math.sqrt(R*R - (y - CY)**2)

# --- backdrop + plate -------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#3E5E5C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F6F2E2", strokeWidth=3, opacity=50)
# low dusk sun over the billabong
d.shape("ellipse", "Sun glow", x=420, y=150, width=300, height=300, fill="#FFF0CC", opacity=26, stroke=NONE)
d.shape("ellipse", "Sun", x=500, y=230, width=140, height=140, fill="#FFF4DA", opacity=55, stroke=NONE)
d.shape("ellipse", "Dusk haze", x=160, y=180, width=260, height=110, fill="#FFF6E0", opacity=18, stroke=NONE)
for i, (x, y, w) in enumerate([(200,300,7),(780,250,6),(170,420,8),(400,120,6),(640,110,7),
                               (300,170,5),(720,180,6),(860,380,5),(150,500,5)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w, fill="#6E918A", opacity=35, stroke=NONE)

# far bank: faint gum crowns + reeds behind the tail (all inside the disc)
for i, (x, y, w, h) in enumerate([(700, 470, 120, 80), (770, 430, 110, 90), (810, 500, 70, 60)]):
    d.shape("ellipse", f"Gum crown {i+1}", x=x, y=y, width=w, height=h, fill="#6E8E80", opacity=26, stroke=NONE)
d.path("M790,610 C792,580 786,540 796,500", "Gum trunk", fill=NONE,
       stroke="#5E7468", strokeWidth=8, opacity=30, cap="round")
for i, (x, top, lean) in enumerate([(740, 360, -10), (770, 330, 6), (846, 400, 14), (720, 420, -16)]):
    d.path(f"M{x},{WATER_Y} Q{x + lean*0.3},{(WATER_Y + top)/2} {x + lean},{top}",
           f"Reed {i+1}", fill=NONE, stroke=REED_GRAD, strokeWidth=5, opacity=50, cap="round")
for i, (x, y) in enumerate([(766, 326), (856, 396)]):
    d.shape("ellipse", f"Cattail {i+1}", x=x - 6, y=y - 4, width=12, height=44,
            fill="#6E5A44", opacity=50, stroke=NONE)

# --- dragonfly above the bill --------------------------------------------------------
DX, DY = 236, 300
for i, dd in enumerate([f"M{DX},{DY} C{DX-30},{DY-40} {DX-78},{DY-44} {DX-84},{DY-26} C{DX-80},{DY-12} {DX-36},{DY-4} {DX},{DY} Z",
                        f"M{DX},{DY} C{DX+30},{DY-40} {DX+78},{DY-44} {DX+84},{DY-26} C{DX+80},{DY-12} {DX+36},{DY-4} {DX},{DY} Z",
                        f"M{DX},{DY+4} C{DX-28},{DY+4} {DX-70},{DY+14} {DX-72},{DY+28} C{DX-64},{DY+38} {DX-26},{DY+20} {DX},{DY+4} Z",
                        f"M{DX},{DY+4} C{DX+28},{DY+4} {DX+70},{DY+14} {DX+72},{DY+28} C{DX+64},{DY+38} {DX+26},{DY+20} {DX},{DY+4} Z"]):
    d.path(dd, f"Dragonfly wing {i+1}", fill=WING_GRAD, opacity=45, stroke="#5E7E86", strokeWidth=2)
d.path(f"M{DX},{DY - 6} L{DX + 4},{DY + 78}", "Dragonfly abdomen", fill=NONE,
       stroke="#3E6E8A", strokeWidth=6, cap="round")
d.shape("ellipse", "Dragonfly thorax", x=DX - 7, y=DY - 10, width=14, height=22, fill="#4E86A2", stroke=NONE)
d.shape("ellipse", "Dragonfly head", x=DX - 8, y=DY - 22, width=16, height=14, fill="#2E5A70", stroke=NONE)

# --- webbed feet + forelimb, under the water (drawn before the water band) ------------------
def foot(label, cx, cy, s=1.0, rot=0):
    c, sn = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    def T(dx, dy):
        return cx + (dx*c - dy*sn)*s, cy + (dx*sn + dy*c)*s
    P = lambda dx, dy: "%.1f,%.1f" % T(dx, dy)
    dd = (f"M{P(-14,-10)} C{P(-30,0)} {P(-44,18)} {P(-40,34)} "
          f"Q{P(-30,28)} {P(-22,40)} Q{P(-12,32)} {P(-2,44)} Q{P(8,34)} {P(18,42)} "
          f"Q{P(26,30)} {P(36,34)} C{P(40,16)} {P(28,0)} {P(14,-10)} Z")
    d.path(dd, label, fill=FOOT_GRAD, stroke=INK, strokeWidth=3)
    for k, (tx, ty) in enumerate([(-40,34), (-22,40), (-2,44), (18,42), (36,34)]):
        px, py = T(tx, ty)
        d.shape("ellipse", f"{label} claw {k+1}", x=round(px - 3), y=round(py - 3),
                width=6, height=7, fill="#E8DCC8", opacity=70, stroke=NONE)

d.path("M376,626 C362,642 348,654 334,662", "Forelimb far", fill=NONE,
       stroke="#4A2E1C", strokeWidth=24, cap="round")
foot("Foot far front", 330, 664, 0.8, rot=70)
d.path("M690,636 C698,650 706,660 714,668", "Hindlimb", fill=NONE,
       stroke="#4A2E1C", strokeWidth=28, cap="round")
foot("Foot hind", 716, 670, 0.95, rot=-35)

# --- tail: beaver paddle behind the body ----------------------------------------------
d.path("M760,452 C800,430 852,438 870,474 C884,508 866,550 826,566 "
       "C800,576 776,572 760,562 Z", "Tail", fill=TAIL_GRAD, stroke=INK, strokeWidth=5)
for i, dd in enumerate(["M786,466 C816,456 842,462 858,480", "M790,500 C822,494 850,500 866,512",
                        "M788,534 C816,536 838,538 852,544"]):
    d.path(dd, f"Tail fur {i+1}", fill=NONE, stroke="#2E1A10", strokeWidth=4, opacity=35, cap="round")
d.path("M792,450 C820,442 846,448 860,464", "Tail sheen", fill=NONE,
       stroke="#F2E4D0", strokeWidth=6, opacity=32, cap="round")

# --- body + head silhouette (one shape, facing left) -----------------------------------
d.path("M330,470 C342,424 380,398 428,396 C480,380 540,366 610,368 "
       "C700,372 770,410 796,466 C820,520 806,590 760,630 "
       "C710,672 590,690 490,684 C410,680 356,650 338,606 C324,570 322,520 330,470 Z",
       "Body", fill=FUR_GRAD, stroke=INK, strokeWidth=7)
d.shape("ellipse", "Head light", x=336, y=404, width=150, height=150, fill="#B48660", opacity=32, stroke=NONE)
d.path("M350,610 C430,660 600,676 760,624 C660,650 480,652 350,610 Z",
       "Belly shade", fill="#22120A", opacity=38, stroke=NONE)
d.path("M440,394 C520,372 650,368 760,420", "Back sheen", fill=NONE,
       stroke="#FFF2E0", strokeWidth=14, opacity=22, cap="round")
d.path("M480,394 C560,378 650,380 730,412", "Back sheen bright", fill=NONE,
       stroke="#FFFFFF", strokeWidth=4, opacity=50, cap="round")
d.path("M462,404 C482,452 484,540 456,612", "Neck crease", fill=NONE,
       stroke="#2A160C", strokeWidth=10, opacity=24, cap="round")
d.path("M472,412 C490,456 492,530 470,596", "Neck crease light", fill=NONE,
       stroke="#FFE6C8", strokeWidth=4, opacity=22, cap="round")
for i, (x, y) in enumerate([(394,500),(412,526),(430,500),(404,554),(436,540)]):
    d.path(f"M{x},{y} Q{x + 8},{y + 4} {x + 14},{y + 12}", f"Head fur {i+1}", fill=NONE,
           stroke="#3A2214", strokeWidth=4, opacity=34, cap="round")
d.path("M372,412 C392,402 414,398 434,400", "Crown sheen", fill=NONE,
       stroke="#FFFFFF", strokeWidth=4, opacity=42, cap="round")
d.path("M790,470 C808,520 800,574 768,612", "Rump rim light", fill=NONE,
       stroke="#FFE6C8", strokeWidth=5, opacity=26, cap="round")
# wet fur clumps: short tapered strokes + glints
for i, (x, y, dx, dy) in enumerate([(520,430,30,10),(590,436,32,8),(660,452,28,14),(726,486,18,24),
                                     (560,500,32,10),(640,512,28,16),(480,470,30,8),(710,556,16,24),
                                     (450,520,28,10),(580,566,30,10),(500,600,30,6),(660,590,26,14)]):
    d.path(f"M{x},{y} Q{x + dx*0.5},{y + dy*0.2} {x + dx},{y + dy}", f"Fur clump {i+1}", fill=NONE,
           stroke="#2A160C", strokeWidth=5, opacity=40, cap="round")
    d.path(f"M{x - 4},{y - 6} Q{x - 4 + dx*0.4},{y - 6 + dy*0.1} {x - 4 + dx*0.7:.0f},{y - 6 + dy*0.6:.0f}",
           f"Fur glint {i+1}", fill=NONE, stroke="#FFF4E4", strokeWidth=3, opacity=34, cap="round")
for i, (x, y, w) in enumerate([(560,388,6),(620,386,5),(690,398,6),(500,396,5),(410,404,5),(740,430,5)]):
    d.shape("ellipse", f"Droplet glint {i+1}", x=x, y=y, width=w, height=w,
            fill="#FFFFFF", opacity=78, stroke=NONE)

# near forelimb + foot reaching forward under the chin
d.path("M450,640 C438,656 422,670 404,680", "Forelimb near", fill=NONE,
       stroke="#4A2E1C", strokeWidth=28, cap="round")
foot("Foot near front", 400, 682, 1.05, rot=58)

# --- bill: a flat paddle, top plane over a darker lip edge ----------------------------------
d.path("M136,548 C138,574 166,588 204,586 C256,582 304,570 338,560 "
       "L340,580 C300,592 252,604 202,606 C160,608 134,592 136,548 Z",
       "Bill lip", fill=LIP_GRAD, stroke=INK, strokeWidth=4)
d.path("M334,464 C300,454 250,458 204,474 C164,488 136,514 136,546 "
       "C138,570 164,582 204,580 C256,576 304,566 338,556 Z",
       "Bill", fill=BILL_GRAD, stroke=INK, strokeWidth=6)
d.shape("ellipse", "Bill sheen", x=190, y=482, width=110, height=34, fill="#FFFFFF", opacity=28, stroke=NONE)
d.path("M180,494 C214,476 262,466 312,466", "Bill rim light", fill=NONE,
       stroke="#EEF4FA", strokeWidth=4, opacity=55, cap="round")
d.path("M146,560 C166,576 204,578 250,572", "Bill edge shade", fill=NONE,
       stroke="#34424F", strokeWidth=5, opacity=40, cap="round")
d.path("M150,586 C176,600 232,598 300,582", "Lip sheen", fill=NONE,
       stroke="#9AAABC", strokeWidth=3, opacity=45, cap="round")
d.shape("ellipse", "Nostril L", x=166, y=516, width=15, height=8, fill="#2A3646", stroke=NONE)
d.shape("ellipse", "Nostril R", x=192, y=502, width=15, height=8, fill="#2A3646", stroke=NONE)
for i, (x, y) in enumerate([(180,540),(204,530),(230,522),(258,516),(286,512),(312,510),
                            (196,558),(222,550),(250,544),(278,538),(306,534),(232,500),(262,494)]):
    d.shape("ellipse", f"Bill pore {i+1}", x=x, y=y, width=4, height=4, fill="#3E4E62", opacity=38, stroke=NONE)
# frontal shield: skin collar where the bill meets the face
d.path("M338,456 C320,490 320,548 342,578", "Bill shield", fill=NONE,
       stroke="#8C9EB2", strokeWidth=16, cap="round")
d.path("M347,458 C330,490 330,546 350,574", "Bill shield edge", fill=NONE,
       stroke=INK, strokeWidth=4, opacity=70, cap="round")

# --- eye in its pale facial groove -------------------------------------------------------
d.path("M362,448 C378,440 404,440 420,450 C406,460 378,462 362,448 Z",
       "Eye groove", fill="#D8B890", opacity=45, stroke=NONE)
d.shape("ellipse", "Eye", x=378, y=442, width=16, height=13, fill="#140C08", stroke=NONE)
d.shape("ellipse", "Eye glint", x=382, y=444, width=5, height=5, fill="#FFFFFF", opacity=90, stroke=NONE)
d.shape("ellipse", "Cheek patch", x=362, y=474, width=42, height=22, fill="#D8B890", opacity=22, stroke=NONE)

# --- water band: closes on the disc's own arc ---------------------------------------------
xl, xr = CX - disc_x(WATER_Y), CX + disc_x(WATER_Y)
wave = f"M{xl:.1f},{WATER_Y}"
xs = [xl + (xr - xl) * k / 10 for k in range(11)]
for k in range(10):
    mx = (xs[k] + xs[k + 1]) / 2
    wave += f" Q{mx:.1f},{WATER_Y + (5 if k % 2 else -5)} {xs[k + 1]:.1f},{WATER_Y}"
d.path(wave + f" A{R},{R} 0 0 1 {xl:.1f},{WATER_Y} Z", "Water",
       fill=WATER_GRAD, opacity=72, stroke=NONE)
d.path(wave, "Waterline light", fill=NONE, stroke="#E6F4F2", strokeWidth=3, opacity=55, cap="round")
# reflections
d.shape("ellipse", "Body reflection", x=330, y=700, width=470, height=70, fill="#2A1A12", opacity=16, stroke=NONE)
d.shape("ellipse", "Bill reflection", x=140, y=618, width=200, height=30, fill="#50627A", opacity=24, stroke=NONE)
d.shape("ellipse", "Sun reflection", x=540, y=760, width=80, height=12, fill="#FFF4DA", opacity=30, stroke=NONE)
d.shape("ellipse", "Sun reflection 2", x=556, y=786, width=50, height=8, fill="#FFF4DA", opacity=22, stroke=NONE)
# meniscus where the body breaks the surface
d.path("M336,612 C420,630 640,632 790,604", "Body meniscus", fill=NONE,
       stroke="#F4FBFA", strokeWidth=4, opacity=58, cap="round")
for i, (x, y, w, h, o) in enumerate([(270, 598, 560, 34, 42), (220, 592, 630, 52, 24)]):
    d.shape("ellipse", f"Ripple {i+1}", x=x, y=y, width=w, height=h, fill=NONE,
            stroke="#EAF6F4", strokeWidth=3, opacity=o)
d.shape("ellipse", "Drip ripple", x=124, y=606, width=70, height=14, fill=NONE,
        stroke="#EAF6F4", strokeWidth=2, opacity=50)
for i, (x, y, w, h) in enumerate([(150, 594, 7, 10), (146, 578, 4, 6)]):
    d.shape("ellipse", f"Drip {i+1}", x=x, y=y, width=w, height=h, fill="#E6F4F2", opacity=72, stroke=NONE)
for i, (x, y, w) in enumerate([(476, 738, 10), (492, 762, 7), (468, 790, 12), (620, 742, 8), (290, 744, 9)]):
    d.shape("ellipse", f"Bubble {i+1}", x=x, y=y, width=w, height=w, fill="#E6F4F2", opacity=35, stroke=NONE)
for i, (x, y, w) in enumerate([(220, 720, 110), (380, 820, 140), (640, 810, 110), (680, 720, 100)]):
    d.path(f"M{x},{y} Q{x + w/4},{y - 8} {x + w/2},{y} T{x + w},{y}", f"Caustic {i+1}", fill=NONE,
           stroke="#A8D4D4", strokeWidth=3, opacity=28, cap="round")

# --- name -------------------------------------------------------------------------------
d.text("PLATYPUS", "Name", x=500, y=962, size=60, font="Virelai Sans",
       color="#D8ECE6", justify="center")

d.finish("platypus-V1R00")
