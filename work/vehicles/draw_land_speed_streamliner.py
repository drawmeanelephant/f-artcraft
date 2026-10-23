#!/usr/bin/env python3
"""Land-speed streamliner — field plate V1R00. Profile, moving right: a long
teardrop body on the salt, translucent canopy bubble, wheels faired in under
skirts, a tail fin, speed lines trailing off the tail. White salt plate with
faint tyre tracks. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Land-Speed Streamliner — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420
INK = "#2A1A1C"

def lin(angle, *stops):
    return {"gradient": {"kind": "linear", "angle": angle, "stops": [
        {"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial", "stops": [
        {"offset": o, "color": c} for o, c in stops]}}

def chord_x(y, r=R):
    dx = math.sqrt(max(r * r - (y - CY) ** 2, 0))
    return CX - dx, CX + dx

def arc_band(y, label, **kw):
    """Region below the horizontal chord at y, closed on the disc's own arc."""
    xl, xr = chord_x(y)
    d.path(f"M{xl:.1f},{y} L{xr:.1f},{y} A420,420 0 0 1 {xl:.1f},{y} Z", label, **kw)

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin(-90, (0, "#1E2433"), (1, "#0B0E16")), stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=lin(-90, (0, "#9FBBD0"), (0.6, "#DCE6EC"), (1, "#F6F3EC")),
        stroke="#7E8A96", strokeWidth=6)

HORIZON = 572
# far ranges, hazy and translucent
d.path("M96,572 L170,548 L232,532 L300,546 L352,522 L420,540 L470,530 L520,550 "
       "L560,572 Z", "Far range left", fill=lin(-90, (0, "#8FA3B6"), (1, "#C9D4DC")),
       stroke=NONE, opacity=55)
d.path("M520,572 L600,540 L660,512 L716,530 L770,516 L832,540 L904,572 Z",
       "Far range right", fill=lin(-90, (0, "#8FA3B6"), (1, "#C9D4DC")),
       stroke=NONE, opacity=45)
d.path("M300,546 L352,522 L372,530 M660,512 L716,530", "Range ridge light", fill=NONE,
       stroke="#F2F5F7", strokeWidth=3, opacity=50, cap="round")

# salt flat
arc_band(HORIZON, "Salt flat", fill=lin(-90, (0, "#E9ECEC"), (0.4, "#F8F7F2"), (1, "#E2DDD2")),
         stroke=NONE)
d.path(f"M{chord_x(HORIZON)[0]:.1f},{HORIZON} L{chord_x(HORIZON)[1]:.1f},{HORIZON}",
       "Horizon haze", fill=NONE, stroke="#FFFFFF", strokeWidth=6, opacity=70)
# mirage shimmer on the far salt
for i, (x, y, w) in enumerate([(160, 584, 180), (420, 590, 140), (640, 586, 200)]):
    d.shape("ellipse", f"Mirage {i+1}", x=x, y=y, width=w, height=8,
            fill="#B9CEDD", opacity=30, stroke=NONE)

# salt polygon cracks in the foreground, clipped to stay inside the inner rim
crack_pts = [(150, 720), (240, 700), (330, 728), (420, 708), (520, 730), (610, 706),
             (700, 726), (800, 704), (860, 720)]
def inside(p, r=396):
    return math.hypot(p[0] - CX, p[1] - CY) <= r
segs = []
for (a, b) in zip(crack_pts, crack_pts[1:]):
    segs.append((a, b))
for i, (x, y) in enumerate(crack_pts[1:-1]):
    segs.append(((x, y), (x + (-24 if i % 2 else 22), y + 74)))
row2 = [(210, 800), (300, 788), (400, 806), (500, 790), (600, 808), (700, 790), (780, 800)]
for (a, b) in zip(row2, row2[1:]):
    segs.append((a, b))
for i, (x, y) in enumerate(row2[1:-1]):
    segs.append(((x, y), (x + (18 if i % 2 else -16), y + 46)))
n = 0
for a, b in segs:
    if inside(a) and inside(b):
        n += 1
        d.path(f"M{a[0]},{a[1]} L{b[0]},{b[1]}", f"Salt crack {n}", fill=NONE,
               stroke="#B7AE9C", strokeWidth=3, opacity=45, cap="round")
        d.path(f"M{a[0]},{a[1]+3} L{b[0]},{b[1]+3}", f"Salt crack ridge {n}", fill=NONE,
               stroke="#FFFFFF", strokeWidth=3, opacity=70, cap="round")

GROUND = 662
# faint tyre tracks running back from the wheels (near + far pair)
for i, (y, op) in enumerate([(GROUND - 4, 22), (GROUND + 2, 30)]):
    x0 = chord_x(y, 400)[0]
    d.path(f"M{x0:.0f},{y} L330,{y}", f"Tyre track {i+1}", fill=NONE,
           stroke="#8E8676", strokeWidth=4, opacity=op, cap="round")
for i, (y, op) in enumerate([(GROUND + 12, 18), (GROUND + 20, 14)]):
    x0 = chord_x(y, 400)[0]
    d.path(f"M{x0:.0f},{y} L300,{y}", f"Old track {i+1}", fill=NONE,
           stroke="#8E8676", strokeWidth=3, opacity=op, cap="round")

# --- speed lines (behind the car) ----------------------------------------------
SPEED = [(250, 470, 120, 4, 40), (196, 500, 160, 5, 45), (140, 530, 200, 4, 50),
         (200, 560, 120, 3, 40), (130, 600, 150, 6, 45), (160, 630, 110, 4, 40),
         (300, 448, 80, 3, 30), (340, 494, 60, 3, 30), (120, 660, 170, 4, 35),
         (230, 410, 140, 3, 30), (180, 440, 90, 4, 35), (330, 524, 90, 3, 35),
         (360, 420, 70, 3, 25), (110, 570, 90, 3, 40)]
for i, (x, y, L, w, op) in enumerate(SPEED):
    xl = max(x, chord_x(y, 396)[0])
    d.path(f"M{xl:.0f},{y} L{x+L},{y}", f"Speed line {i+1}", fill=NONE,
           stroke=lin(0, (0, "#5F7487"), (1, "#5F7487")), strokeWidth=w,
           opacity=op, cap="round")

# salt spray kicked up behind the rear wheel
for i, (x, y, w, h, op) in enumerate([(150, 628, 120, 36, 40), (200, 612, 110, 44, 45),
                                      (250, 624, 90, 36, 50), (120, 642, 80, 22, 30)]):
    d.shape("ellipse", f"Salt spray {i+1}", x=x, y=y, width=w, height=h,
            fill=rad((0, "#FFFFFF"), (1, "#E6E2D8")), opacity=op, stroke=NONE)

# --- shadow + wheels -------------------------------------------------------------
d.shape("ellipse", "Car shadow", x=210, y=GROUND - 10, width=620, height=24,
        fill=rad((0, "#6C665A"), (1, "#C8C2B4")), opacity=45, stroke=NONE)
TYRE = rad((0, "#4A3E3E"), (0.7, "#2E2526"), (1, "#1A1314"))
for nm, cx in [("Rear", 330), ("Front", 712)]:
    d.shape("ellipse", f"{nm} tyre", x=cx - 40, y=GROUND - 80, width=80, height=80,
            fill=TYRE, stroke=INK, strokeWidth=4)
    d.shape("ellipse", f"{nm} disc wheel", x=cx - 26, y=GROUND - 66, width=52, height=52,
            fill=rad((0, "#F2F2F0"), (0.6, "#B8BCC2"), (1, "#6C727A")), stroke=INK, strokeWidth=3)

# --- body ------------------------------------------------------------------------
BODY = lin(-90, (0, "#F0624A"), (0.45, "#C8301F"), (1, "#6E140C"))
body = ("M812,600 C812,552 744,512 640,508 C500,502 330,540 214,584 "
        "C190,592 186,616 206,622 L270,640 L760,640 C796,640 812,626 812,600 Z")
d.path(body, "Body", fill=BODY, stroke=INK, strokeWidth=6)
# lower skirt shading, translucent
d.path("M206,622 L270,640 L760,640 C796,640 812,626 812,600 "
       "C790,618 760,624 700,624 L280,626 C250,626 228,622 206,622 Z",
       "Skirt shade", fill="#3A0A06", opacity=35, stroke=NONE)
# white stripe along the flank
d.path("M800,590 C760,578 700,572 620,570 C480,568 340,584 230,604 "
       "L234,614 C344,596 484,582 622,584 C702,586 764,592 806,606 Z",
       "Flank stripe", fill=lin(-90, (0, "#FFFFFF"), (1, "#D9D4CC")), stroke=NONE, opacity=92)
# wheel fairing seams
for nm, cx in [("Rear", 330), ("Front", 712)]:
    d.path(f"M{cx-52},640 C{cx-50},606 {cx+50},606 {cx+52},640", f"{nm} fairing seam",
           fill=NONE, stroke=INK, strokeWidth=3, opacity=55, cap="round")
    d.path(f"M{cx-46},636 C{cx-44},612 {cx+44},612 {cx+46},636", f"{nm} fairing light",
           fill=NONE, stroke="#FFB4A6", strokeWidth=3, opacity=40, cap="round")
# top highlight + specular
d.path("M790,560 C740,528 680,518 620,516 C500,514 360,546 250,586",
       "Body highlight", fill=NONE, stroke="#FFD2C6", strokeWidth=10, opacity=35, cap="round")
d.path("M760,544 C720,528 680,522 640,522", "Body specular", fill=NONE,
       stroke="#FFFFFF", strokeWidth=4, opacity=70, cap="round")
# chrome nose ring
d.path("M806,578 C816,592 816,612 806,626", "Nose chrome", fill=NONE,
       stroke=lin(-90, (0, "#FFFFFF"), (0.5, "#9AA2AC"), (1, "#E8ECF0")),
       strokeWidth=7, cap="round")
d.path("M790,602 L812,602", "Nose intake", fill=NONE, stroke=INK, strokeWidth=4,
       opacity=60, cap="round")
# blank generic roundel
d.shape("ellipse", "Roundel", x=440, y=566, width=56, height=56,
        fill=rad((0, "#FFFFFF"), (1, "#E2DCD2")), stroke=INK, strokeWidth=3)
d.shape("ellipse", "Roundel ring", x=448, y=574, width=40, height=40,
        fill=NONE, stroke="#C8301F", strokeWidth=3, opacity=80)
# engine louvres + exhaust
for i in range(5):
    x = 330 + i * 18
    d.path(f"M{x},{562-i*2} L{x+12},{560-i*2}", f"Louvre {i+1}", fill=NONE,
           stroke=INK, strokeWidth=3, opacity=55, cap="round")
d.path("M262,598 L232,598", "Exhaust stub", fill=NONE,
       stroke=lin(-90, (0, "#E8ECF0"), (1, "#6C727A")), strokeWidth=7, cap="round")

# tail fin
d.path("M214,584 C230,578 252,572 276,566 C266,540 254,500 246,466 "
       "C234,462 222,466 216,474 C214,520 212,556 206,588 Z", "Tail fin",
       fill=lin(0, (0, "#7E180E"), (0.5, "#D23A26"), (1, "#F27058")),
       stroke=INK, strokeWidth=5)
d.path("M226,560 C228,530 230,500 232,476", "Fin highlight", fill=NONE,
       stroke="#FFD2C6", strokeWidth=4, opacity=50, cap="round")
d.path("M246,466 C234,462 222,466 216,474", "Fin chrome cap", fill=NONE,
       stroke=lin(0, (0, "#E8ECF0"), (1, "#8A929C")), strokeWidth=6, cap="round")

# canopy bubble, translucent
d.path("M556,512 C570,470 648,464 680,508 Z", "Canopy",
       fill=lin(-90, (0, "#E8F4FC"), (1, "#6F95B4")), opacity=50,
       stroke=INK, strokeWidth=4)
d.path("M596,510 C596,488 618,482 630,494 C636,500 636,508 634,510 Z", "Driver helmet",
       fill=rad((0, "#FFF2D0"), (1, "#D8A440")), stroke=INK, strokeWidth=3, opacity=85)
d.path("M622,496 L636,500", "Helmet visor", fill=NONE, stroke=INK, strokeWidth=4,
       opacity=70, cap="round")
d.path("M574,500 C586,482 612,474 640,476", "Canopy glint", fill=NONE,
       stroke="#FFFFFF", strokeWidth=4, opacity=85, cap="round")

# speed lines over the tail, pulling off the body
for i, (x0, x1, y, w, op) in enumerate([(150, 212, 594, 4, 55), (170, 230, 612, 3, 45),
                                        (176, 238, 488, 3, 40), (160, 206, 520, 4, 45)]):
    d.path(f"M{x0},{y} L{x1},{y}", f"Tail speed line {i+1}", fill=NONE,
           stroke="#5F7487", strokeWidth=w, opacity=op, cap="round")

# --- caption --------------------------------------------------------------------
d.text("LAND-SPEED STREAMLINER", "Name", x=500, y=940, size=48, font="Virelai Sans",
       color="#E8ECEE", justify="center")
o = d.text("1959 · TWIN SUPERCHARGED V8", "Spec", x=500, y=975, size=22,
           font="Virelai Sans", color="#9AA8B6", justify="center")
if o and "id" in o:
    d.cmd("text.setStyle", "Spec tracking", ids=[o["id"]], tracking=300)

d.finish("land-speed-streamliner-V1R00")
