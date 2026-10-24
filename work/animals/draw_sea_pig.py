#!/usr/bin/env python3
"""Sea pig — field-guide plate V1R00. Scotoplanes, the translucent pink
sea cucumber of the abyssal plain: a plump gelatinous body strolling the
sediment on leg-like tube feet, long dorsal papillae waving overhead, a
crown of stubby feeding tentacles sweeping the ooze at the mouth. Pale
rose body glowing faintly against a pure black deep. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Sea Pig — Field Plate", 1000, 1000)

INK = "#5C2E40"   # deep wine, not black
BG_GRAD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000], "stops": [
    {"offset": 0, "color": "#05070C"}, {"offset": 1, "color": "#000000"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#18222E"}, {"offset": 0.55, "color": "#0A1018"},
    {"offset": 1, "color": "#030509"}]}}
SED_GRAD = {"gradient": {"kind": "linear", "start": [0, 780], "end": [0, 880], "stops": [
    {"offset": 0, "color": "#2E3A46"}, {"offset": 1, "color": "#12181F"}]}}
BODY_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F9D3DC"}, {"offset": 0.55, "color": "#E7A0B4"},
    {"offset": 1, "color": "#BC6E86"}]}}
LEG_GRAD = {"gradient": {"kind": "linear", "start": [0, 640], "end": [0, 800], "stops": [
    {"offset": 0, "color": "#E9A8B8"}, {"offset": 1, "color": "#B96E82"}]}}
PAP_GRAD = {"gradient": {"kind": "linear", "start": [0, 330], "end": [0, 520], "stops": [
    {"offset": 0, "color": "#F2BEC9"}, {"offset": 1, "color": "#C47A90"}]}}
TENT_GRAD = {"gradient": {"kind": "linear", "start": [0, 660], "end": [0, 800], "stops": [
    {"offset": 0, "color": "#EFB4C2"}, {"offset": 1, "color": "#C87E92"}]}}

PCX, PCY, PR = 500, 460, 420

def on_disc(x, y, pad):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

# --- backdrop + plate ------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#232E3C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#54687C", strokeWidth=3, opacity=35)
# the animal's own faint rose glow hanging in the dark
d.shape("ellipse", "Body glow", x=250, y=470, width=500, height=300,
        fill="#B96E82", opacity=9, stroke=NONE)
d.shape("ellipse", "Body glow core", x=320, y=520, width=340, height=200,
        fill="#D98CA0", opacity=8, stroke=NONE)
# marine snow, sparse in the black
for i, (x, y, w) in enumerate([(200,300,6),(790,270,5),(170,480,7),(835,470,6),(250,700,5),
                               (760,700,6),(150,590,4),(850,580,5),(420,120,5),(620,115,6),
                               (310,180,4),(700,190,5),(480,95,4),(220,380,4),(810,360,4),
                               (340,830,4),(660,830,4),(560,140,4)]):
    assert on_disc(x, y, 10), (x, y)
    d.shape("ellipse", f"Marine snow {i+1}", x=x, y=y, width=w, height=w,
            fill="#E8F0F6", opacity=42, stroke=NONE)

# --- abyssal sediment: top edge wavy, closing on the disc's own arc -----------------
d.path("M253,800 C360,782 470,794 560,788 C640,783 700,792 747,800 "
       "A420,420 0 0 1 253,800 Z",
       "Sediment", fill=SED_GRAD, stroke="#3E4C5A", strokeWidth=4)
d.path("M270,804 C380,790 620,790 730,806", "Sediment sheen",
       fill=NONE, stroke="#7A8C9C", strokeWidth=4, opacity=35, cap="round")
for i, (x, y, w, h) in enumerate([(300,806,26,10),(430,800,18,8),(590,798,22,9),(690,806,16,7),
                                  (380,812,14,6),(530,806,18,7)]):
    d.shape("ellipse", f"Ooze lump {i+1}", x=x, y=y, width=w, height=h,
            fill="#414F5C", opacity=50, stroke=NONE)
# contact shadow under the feet
d.shape("ellipse", "Body shadow", x=320, y=776, width=340, height=26,
        fill="#000000", opacity=45, stroke=NONE)

# --- far-side legs (darker, behind the body) -----------------------------------------
def leg(label, root, knee, foot, w0, w1, fill, opacity, outline=INK):
    """Tapered tube foot: two quad edges meeting at a rounded toe."""
    x0, y0 = root; x1, y1 = knee; x2, y2 = foot
    d.path(f"M{x0-4},{y0} Q{x1-8},{y1} {x2-w1:.0f},{y2-6} "
           f"Q{x2-w1:.0f},{y2+2} {x2},{y2+2} "
           f"Q{x2+w1:.0f},{y2+2} {x2+w1:.0f},{y2-6} "
           f"Q{x1+8},{y1} {x0+4},{y0} Z",
           label, fill=fill, stroke=outline, strokeWidth=3, opacity=opacity)

for i, (rx, kx, fx, fy) in enumerate([(420, 408, 396, 788), (500, 494, 482, 792),
                                      (576, 568, 556, 790)]):
    leg(f"Leg far {i+1}", (rx, 668), (kx, 724), (fx, fy), 11, 8,
        "#9A5A6E", 75, outline="#5C2E40")

# --- near-side legs mid-stride ---------------------------------------------------------
for i, (rx, kx, fx, fy) in enumerate([(368, 344, 330, 792), (436, 424, 424, 752),
                                      (500, 508, 506, 790), (564, 582, 606, 788),
                                      (622, 640, 654, 784)]):
    leg(f"Leg {i+1}", (rx, 672), (kx, (672+fy)//2+16), (fx, fy), 14, 10,
        LEG_GRAD, 92)
    # knee crease
    d.path(f"M{rx+2},{(672+fy)//2+6} L{(rx+fx)//2+4},{(672+fy)//2+16}",
           f"Leg {i+1} crease", fill=NONE, stroke="#8E4A5E",
           strokeWidth=3, opacity=40, cap="round")
# toe pads: planted feet flat, the lifted one points its toe down
for i, (fx, fy, w, h) in enumerate([(330, 792, 18, 7), (424, 752, 12, 9), (506, 790, 18, 7),
                                    (606, 788, 18, 7), (654, 784, 18, 7)]):
    d.shape("ellipse", f"Toe pad {i+1}", x=fx-w//2, y=fy-3, width=w, height=h,
            fill="#D98CA0", opacity=60, stroke=NONE)

# --- dorsal papillae: a row of long tube feet waving off the back -----------------------
def papilla(i, root, ctrl, tip, w0, w1):
    """Slender tapered stalk + knob tip."""
    n = 16
    def quad(t):
        u = 1 - t
        x = u*u*root[0] + 2*u*t*ctrl[0] + t*t*tip[0]
        y = u*u*root[1] + 2*u*t*ctrl[1] + t*t*tip[1]
        dx = 2*u*(ctrl[0]-root[0]) + 2*t*(tip[0]-ctrl[0])
        dy = 2*u*(ctrl[1]-root[1]) + 2*t*(tip[1]-ctrl[1])
        return x, y, dx, dy
    L, R = [], []
    for k in range(n + 1):
        t = k / n
        x, y, dx, dy = quad(t)
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy/ln, dx/ln
        w = (w0 + (w1 - w0) * t) / 2
        L.append((x + nx*w, y + ny*w)); R.append((x - nx*w, y - ny*w))
    dd = "M%.1f,%.1f " % L[0] + " ".join("L%.1f,%.1f" % p for p in L[1:])
    dd += " " + " ".join("L%.1f,%.1f" % p for p in reversed(R)) + " Z"
    d.path(dd, f"Papilla {i}", fill=PAP_GRAD, stroke=INK, strokeWidth=3, opacity=90)
    d.shape("ellipse", f"Papilla {i} tip", x=round(tip[0]-5), y=round(tip[1]-6),
            width=10, height=12, fill="#F2BEC9", stroke=INK, strokeWidth=2, opacity=90)
    assert on_disc(tip[0], tip[1], 24), tip

# rear pair droops back, middle two stand tall with waving tips, front pair leans on
papilla(1, (352, 520), (316, 468), (272, 428), 13, 5)
papilla(2, (420, 498), (390, 432), (374, 366), 14, 5)
papilla(3, (490, 490), (500, 412), (534, 348), 15, 5)
papilla(4, (560, 496), (590, 428), (632, 376), 14, 5)
papilla(5, (622, 514), (664, 460), (700, 420), 13, 5)
# stubby dorsal bumps between the tall stalks
for i, (x, y) in enumerate([(385, 505), (455, 488), (525, 486), (592, 502)]):
    d.shape("ellipse", f"Dorsal bump {i+1}", x=x-7, y=y-16, width=14, height=20,
            fill="#C97A90", stroke=INK, strokeWidth=2, opacity=80)

# --- body: translucent gelatinous sac ---------------------------------------------------
d.path("M310,600 "
       "C302,556 326,522 366,506 "
       "C420,484 560,484 622,512 "
       "C664,530 682,570 672,614 "
       "C662,654 620,682 540,690 "
       "C460,698 360,688 328,656 "
       "C312,640 306,620 310,600 Z",
       "Body", fill=BODY_GRAD, stroke=INK, strokeWidth=6, opacity=94)
# translucent inner anatomy: a faint gut coil + darker dorsal wash, low opacity
d.path("M390,606 C430,590 520,590 580,608 C600,616 600,632 580,640 "
       "C510,652 430,648 396,632 C380,624 378,612 390,606 Z",
       "Gut hint", fill="#A85A72", opacity=12, stroke=NONE)
d.shape("ellipse", "Dorsal wash", x=370, y=505, width=270, height=70,
        fill="#8E4A62", opacity=12, stroke=NONE)
# gelatin sheen along the crown
d.shape("ellipse", "Crown sheen", x=390, y=498, width=200, height=44,
        fill="#FFFFFF", opacity=22, stroke=NONE)
d.shape("ellipse", "Crown sheen hot", x=440, y=506, width=80, height=16,
        fill="#FFFFFF", opacity=36, stroke=NONE)
# rim light: the faintest cold edge catching the top of the sac
d.path("M330,548 C380,506 560,492 640,526", "Rim light",
       fill=NONE, stroke="#FFE8EE", strokeWidth=5, opacity=50, cap="round")
# ventral translucency: the far legs faintly glowing through the body wall
d.shape("ellipse", "Ventral glow", x=400, y=648, width=200, height=30,
        fill="#F9D3DC", opacity=14, stroke=NONE)
# skin speckles
for i, (x, y, w) in enumerate([(380,560,5),(440,540,4),(520,536,5),(590,552,4),(350,600,4),
                               (640,590,5),(430,650,4),(560,648,4),(490,520,4),(620,540,4)]):
    d.shape("ellipse", f"Speckle {i+1}", x=x, y=y, width=w, height=w,
            fill="#A85A72", opacity=40, stroke=NONE)

# --- mouth: puckered lobe low on the front + feeding tentacles draped over it -----------
d.shape("ellipse", "Mouth lobe", x=308, y=648, width=52, height=36,
        fill="#D98CA0", stroke=INK, strokeWidth=4, opacity=85)
d.path("M316,666 C324,673 338,674 348,669", "Mouth line",
       fill=NONE, stroke=INK, strokeWidth=4, opacity=55, cap="round")
# stubby feeding tentacles sweeping the ooze in front of the mouth
for i, (x0, cx, tx, ty) in enumerate([(314, 292, 280, 784), (326, 312, 298, 794),
                                      (340, 336, 322, 798), (352, 360, 348, 796),
                                      (362, 382, 376, 790)]):
    d.path(f"M{x0},678 Q{cx},{(678+ty)//2+10} {tx},{ty}",
           f"Feed tentacle {i+1}", fill=NONE, stroke=TENT_GRAD,
           strokeWidth=8, opacity=90, cap="round")
    d.shape("ellipse", f"Feed tip {i+1}", x=tx-5, y=ty-4, width=10, height=8,
            fill="#EFB4C2", opacity=90, stroke=NONE)

# --- name --------------------------------------------------------------------------------
d.text("SEA PIG", "Name", x=500, y=962, size=60, font="Virelai Sans",
       color="#E4BCC8", justify="center")

d.finish("sea-pig-V1R00")
