#!/usr/bin/env python3
"""Hercules beetle — field plate V1R00. Three-quarter dorsal, head to the upper
right: the long thoracic horn arcing forward over the upturned head horn like
a pincer, olive-gold elytra with a dark saddle, red-brown horn tips, on a
humid green plate. Drawn head-up, then the whole animal is rotated.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Hercules Beetle — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420
INK = "#22171A"

def lin(angle, *stops):
    return {"gradient": {"kind": "linear", "angle": angle, "stops": [
        {"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial", "stops": [
        {"offset": o, "color": c} for o, c in stops]}}

def disc_pt(deg, r=R):
    a = math.radians(deg)
    return (CX + r * math.cos(a), CY + r * math.sin(a))

def cubic(p, t):
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = p
    mt = 1 - t
    x = mt**3*x0 + 3*mt*mt*t*x1 + 3*mt*t*t*x2 + t**3*x3
    y = mt**3*y0 + 3*mt*mt*t*y1 + 3*mt*t*t*y2 + t**3*y3
    tx = 3*mt*mt*(x1-x0) + 6*mt*t*(x2-x1) + 3*t*t*(x3-x2)
    ty = 3*mt*mt*(y1-y0) + 6*mt*t*(y2-y1) + 3*t*t*(y3-y2)
    return x, y, tx, ty

def ribbon(p, widths, n=32):
    """Closed outline of a tapering tube along cubic p, ending in a point
    when the last width is 0."""
    left, right = [], []
    k = len(widths) - 1
    for i in range(n + 1):
        t = i / n
        x, y, tx, ty = cubic(p, t)
        ln = math.hypot(tx, ty) or 1
        nx, ny = -ty / ln, tx / ln
        s = t * k; j = min(int(s), k - 1); f = s - j
        w = (widths[j] * (1 - f) + widths[j + 1] * f) / 2
        left.append((x + nx * w, y + ny * w))
        right.append((x - nx * w, y - ny * w))
    pts = left + right[::-1]
    return f"M{pts[0][0]:.1f},{pts[0][1]:.1f} " + " ".join(
        f"L{x:.1f},{y:.1f}" for x, y in pts[1:]) + " Z"

def polyline(pts):
    return f"M{pts[0][0]},{pts[0][1]} " + " ".join(f"L{x},{y}" for x, y in pts[1:])

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin(-90, (0, "#10291F"), (1, "#04100B")), stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#D6EED6"), (0.65, "#9FCEA8"), (1, "#5C9670")),
        stroke="#3F7556", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E6F6E8", strokeWidth=3, opacity=55)
d.shape("ellipse", "Humid haze 1", x=150, y=150, width=320, height=200,
        fill="#F2FFF4", opacity=18, stroke=NONE)
d.shape("ellipse", "Humid haze 2", x=560, y=520, width=280, height=180,
        fill="#86BE94", opacity=20, stroke=NONE)
# broad-leaf silhouettes behind the animal
for i, (p, op) in enumerate([("M140,520 C200,400 300,330 420,300 C360,380 260,470 140,520 Z", 22),
                             ("M860,330 C800,260 700,220 600,220 C680,270 770,320 860,330 Z", 20),
                             ("M820,560 C760,470 700,440 640,430 C690,500 750,550 820,560 Z", 16)]):
    d.path(p, f"Back leaf {i+1}", fill=lin(0, (0, "#4E9464"), (1, "#2F6E48")),
           stroke=NONE, opacity=op)
# condensation droplets on the plate
for i, (x, y, w) in enumerate([(190, 300, 22), (232, 260, 12), (770, 250, 18), (812, 300, 10),
                               (700, 160, 14), (300, 150, 10), (850, 430, 16), (150, 430, 12),
                               (420, 110, 12), (620, 110, 9)]):
    d.shape("ellipse", f"Droplet {i+1}", x=x, y=y, width=w, height=w * 1.1,
            fill=rad((0, "#FFFFFF"), (0.6, "#D8F2DE"), (1, "#7FB892")),
            stroke="#5C9670", strokeWidth=1.5, opacity=55)
    d.shape("ellipse", f"Droplet glint {i+1}", x=x + w * 0.22, y=y + w * 0.18,
            width=w * 0.3, height=w * 0.3, fill="#FFFFFF", opacity=80, stroke=NONE)

# mossy ground along the lower rim (closes on the disc arc)
a0, a1 = disc_pt(146), disc_pt(34)
d.path(f"M{a0[0]:.1f},{a0[1]:.1f} C260,700 380,740 500,732 C640,724 760,690 "
       f"{a1[0]:.1f},{a1[1]:.1f} A420,420 0 0 1 {a0[0]:.1f},{a0[1]:.1f} Z", "Mossy log",
       fill=lin(-90, (0, "#6E8E4A"), (0.35, "#4E6E36"), (1, "#2E4A24")),
       stroke="#26401E", strokeWidth=5)
for i, (x, y, w, h) in enumerate([(170, 700, 90, 34), (270, 716, 110, 36), (400, 728, 120, 34),
                                  (540, 724, 120, 34), (670, 704, 110, 34), (770, 680, 80, 28)]):
    d.shape("ellipse", f"Moss tuft {i+1}", x=x, y=y, width=w, height=h,
            fill=rad((0, "#B5D67A"), (1, "#5E8A3A")), opacity=70, stroke=NONE)
for i, (x0, y0, x1, y1) in enumerate([(220, 780, 380, 800), (420, 806, 600, 806),
                                      (640, 790, 760, 760), (300, 840, 460, 856)]):
    d.path(f"M{x0},{y0} Q{(x0+x1)/2},{max(y0,y1)+14} {x1},{y1}", f"Bark ridge {i+1}",
           fill=NONE, stroke="#1E3418", strokeWidth=4, opacity=45, cap="round")
d.shape("ellipse", "Beetle shadow", x=300, y=640, width=440, height=110,
        fill="#1C3A26", opacity=24, stroke=NONE)

# --- the beetle, drawn head-up around (500, 560) ------------------------------------
B = []
def bp(dd, name, **kw):
    r = d.path(dd, name, **kw)
    if r and "id" in r: B.append(r["id"])
def bs(shape, name, **kw):
    r = d.shape(shape, name, **kw)
    if r and "id" in r: B.append(r["id"])

LEG = "#3A2A2C"
def leg(name, pts, far=False):
    coxa, knee, ankle, foot = pts
    col = "#1C1214" if far else LEG
    op = 92 if far else 100
    fx, fy = coxa; kx, ky = knee
    bp(ribbon(((fx, fy), (fx + (kx-fx)/3, fy + (ky-fy)/3),
               (fx + 2*(kx-fx)/3, fy + 2*(ky-fy)/3), (kx, ky)), [14, 20, 12]),
       f"{name} femur", fill=lin(0, (0, "#5A4448"), (1, col)), stroke=INK,
       strokeWidth=3, opacity=op)
    bp(polyline([knee, ankle]), f"{name} tibia ink", fill=NONE, stroke=INK,
       strokeWidth=14, cap="round", opacity=op)
    bp(polyline([knee, ankle]), f"{name} tibia", fill=NONE, stroke=col,
       strokeWidth=9, cap="round", opacity=op)
    ax, ay = ankle
    ln = math.hypot(ax-kx, ay-ky); ux, uy = (ax-kx)/ln, (ay-ky)/ln
    for j, t in enumerate([0.35, 0.6, 0.85]):
        sx, sy = kx + (ax-kx)*t, ky + (ay-ky)*t
        bp(f"M{sx-uy*5:.0f},{sy+ux*5:.0f} L{sx-uy*14+ux*6:.0f},{sy+ux*14+uy*6:.0f}",
           f"{name} spine {j+1}", fill=NONE, stroke=INK, strokeWidth=3.5, cap="round",
           opacity=op)
    bp(polyline([ankle, foot]), f"{name} tarsus ink", fill=NONE, stroke=INK,
       strokeWidth=10, cap="round", opacity=op)
    bp(polyline([ankle, foot]), f"{name} tarsus", fill=NONE, stroke="#4A3434" if not far else col,
       strokeWidth=6, cap="round", opacity=op)
    px, py = foot
    ln = math.hypot(px-ax, py-ay); ux, uy = (px-ax)/ln, (py-ay)/ln
    for j, t in enumerate([0.25, 0.5, 0.75]):
        sx, sy = ax + (px-ax)*t, ay + (py-ay)*t
        bp(f"M{sx-uy*5:.0f},{sy+ux*5:.0f} L{sx+uy*5:.0f},{sy-ux*5:.0f}",
           f"{name} tarsal joint {j+1}", fill=NONE, stroke=INK, strokeWidth=3,
           opacity=op * 0.7)
    for s in (1, -1):
        bp(f"M{px:.0f},{py:.0f} Q{px+ux*10-uy*6*s:.0f},{py+uy*10+ux*6*s:.0f} "
           f"{px+ux*8-uy*12*s:.0f},{py+uy*8+ux*12*s:.0f}",
           f"{name} claw {'a' if s > 0 else 'b'}", fill=NONE, stroke=INK,
           strokeWidth=3, cap="round", opacity=op)
    if not far:
        bp(polyline([(fx + (kx-fx)*0.2, fy + (ky-fy)*0.2), (fx + (kx-fx)*0.8, fy + (ky-fy)*0.8)]),
           f"{name} femur sheen", fill=NONE, stroke="#C8B8BC", strokeWidth=3,
           opacity=40, cap="round")

# far-side legs (the beetle's right; the viewer sees its left flank) tuck under
leg("Far fore leg", [(420, 500), (342, 470), (300, 388), (290, 312)], far=True)
leg("Far mid leg", [(420, 584), (326, 604), (276, 662), (238, 702)], far=True)
leg("Far hind leg", [(432, 664), (356, 722), (336, 798), (310, 850)], far=True)
# near-side legs come out from under the flank
leg("Fore leg", [(580, 500), (660, 468), (706, 384), (720, 306)])
leg("Mid leg", [(588, 586), (684, 600), (736, 656), (776, 698)])
leg("Hind leg", [(572, 666), (652, 716), (668, 786), (660, 840)])

# flank band on the viewer side
bp("M606,520 C628,530 640,620 634,700 C628,760 596,798 546,806 "
   "C576,792 608,756 614,700 C622,640 620,560 606,520 Z", "Elytra flank",
   fill=lin(0, (0, "#6E5E22"), (1, "#3E3412")), stroke=INK, strokeWidth=4)

# elytra
ELY = rad((0, "#EEDD8A"), (0.5, "#C4AF52"), (1, "#80702C"))
bp("M382,532 C380,520 392,512 412,512 L500,512 L500,808 C478,808 444,800 420,770 "
   "C384,722 376,622 382,532 Z", "Elytron L", fill=ELY, stroke=INK, strokeWidth=5)
bp("M618,532 C620,520 608,512 588,512 L500,512 L500,808 C522,808 556,800 580,770 "
   "C616,722 624,622 618,532 Z", "Elytron R", fill=ELY, stroke=INK, strokeWidth=5)
# dark saddle + scattered spots, translucent so the gold reads through
bp("M384,600 C430,620 470,612 500,628 C530,612 570,620 616,600 C620,640 618,676 612,700 "
   "C570,690 532,700 500,684 C468,700 430,690 388,700 C382,668 382,632 384,600 Z",
   "Elytra saddle", fill=lin(-90, (0, "#2A1E10"), (1, "#4A3818")), stroke=NONE, opacity=55)
for i, (x, y, w, h) in enumerate([(410, 545, 18, 14), (560, 552, 16, 13), (452, 740, 20, 16),
                                  (540, 732, 16, 14), (420, 720, 12, 10), (576, 712, 14, 11),
                                  (468, 560, 10, 9), (522, 770, 12, 10)]):
    bs("ellipse", f"Elytra spot {i+1}", x=x, y=y, width=w, height=h,
       fill="#2A1E10", opacity=65, stroke=NONE)
for i, x in enumerate([428, 456, 544, 572]):
    bp(f"M{x},{526} C{x - (500-x)*0.05:.0f},640 {x + (500-x)*0.25:.0f},740 {500 + (x-500)*0.55:.0f},790",
       f"Elytra stria {i+1}", fill=NONE, stroke="#5E4E1C", strokeWidth=3, opacity=35, cap="round")
bp("M500,514 L500,806", "Suture", fill=NONE, stroke=INK, strokeWidth=4)
bp("M406,540 C400,600 404,660 416,710", "Elytron L sheen", fill=NONE,
   stroke="#FFF6C8", strokeWidth=10, opacity=45, cap="round")
bp("M586,536 C596,590 598,650 590,706", "Elytron R sheen", fill=NONE,
   stroke="#FFF6C8", strokeWidth=6, opacity=35, cap="round")
bp("M412,560 C414,540 428,528 448,526", "Shoulder specular", fill=NONE,
   stroke="#FFFFFF", strokeWidth=4, opacity=70, cap="round")
bp("M424,772 C450,800 550,800 576,772", "Elytra apex shade", fill=NONE,
   stroke="#3E3412", strokeWidth=10, opacity=30, cap="round")


# head (mostly under the horns) + lamellate antennae
bs("ellipse", "Head", x=470, y=376, width=64, height=46,
   fill=rad((0, "#4A3A3E"), (1, "#140C0E")), stroke=INK, strokeWidth=4)
for s, x0 in ((-1, 476), (1, 528)):
    bp(f"M{x0},392 L{x0 + s*24},376", f"Antenna {'L' if s < 0 else 'R'}", fill=NONE,
       stroke=INK, strokeWidth=3.5, cap="round")
    for j in range(3):
        bs("ellipse", f"Antenna {'L' if s < 0 else 'R'} lamella {j+1}",
           x=x0 + s*24 - 4 + s*j*3, y=366 + j*4, width=9, height=6,
           fill="#8A5A34", stroke=INK, strokeWidth=1.5)

# horns: cephalic horn below (bows toward the viewer), thoracic horn above
HORN = lin(90, (0, "#1E1416"), (0.55, "#2C1C1A"), (0.85, "#6E2E1C"), (1, "#A2492A"))
ceph = ((516, 398), (548, 330), (552, 250), (516, 196))
bp(ribbon(ceph, [30, 22, 14, 0]), "Cephalic horn", fill=HORN, stroke=INK, strokeWidth=4)
for j, t in enumerate([0.28, 0.45, 0.62]):
    x, y, tx, ty = cubic(ceph, t)
    ln = math.hypot(tx, ty); nx, ny = -ty/ln, tx/ln
    w = 15 - j * 3
    bp(f"M{x+nx*w:.0f},{y+ny*w:.0f} L{x+nx*(w+11)+tx/ln*4:.0f},{y+ny*(w+11)+ty/ln*4:.0f} "
       f"L{x+nx*w+tx/ln*10:.0f},{y+ny*w+ty/ln*10:.0f} Z",
       f"Cephalic tooth {j+1}", fill="#2C1C1A", stroke=INK, strokeWidth=3)
bp("M528,370 C544,320 546,262 524,214", "Cephalic horn sheen", fill=NONE,
   stroke="#E8B89A", strokeWidth=4, opacity=45, cap="round")

thor = ((490, 446), (436, 340), (450, 220), (522, 168))
bp(ribbon(thor, [56, 34, 20, 6]), "Thoracic horn", fill=HORN, stroke=INK, strokeWidth=5)
# down-hooked tip and paired lateral teeth
bp("M512,160 C530,160 540,170 536,188 C530,180 522,176 514,176 Z", "Thoracic horn hook",
   fill="#A2492A", stroke=INK, strokeWidth=3)
for s, (x, y) in ((-1, (442, 318)), (1, (470, 312))):
    bp(f"M{x},{y} L{x + s*16},{y - 10} L{x + s*2},{y - 14} Z",
       f"Thoracic tooth {'L' if s < 0 else 'R'}", fill="#2C1C1A", stroke=INK, strokeWidth=3)
# golden setae brush on the underside of the thoracic horn
for j in range(9):
    t = 0.38 + j * 0.065
    x, y, tx, ty = cubic(thor, t)
    ln = math.hypot(tx, ty); nx, ny = -ty/ln, tx/ln
    w = (32 - (t - 0.33) * 28) / 2
    bp(f"M{x-nx*w*0.6:.0f},{y-ny*w*0.6:.0f} L{x-nx*(w+8):.0f},{y-ny*(w+8):.0f}",
       f"Horn setae {j+1}", fill=NONE, stroke="#D8A04A", strokeWidth=3,
       opacity=85, cap="round")
bp("M470,404 C440,350 438,280 470,222", "Thoracic horn sheen", fill=NONE,
   stroke="#F2C8AE", strokeWidth=5, opacity=50, cap="round")
bp("M478,386 C458,350 454,300 466,262", "Thoracic horn specular", fill=NONE,
   stroke="#FFFFFF", strokeWidth=2.5, opacity=60, cap="round")

# pronotum last, so the horn roots tuck under its front edge
bp("M600,430 C618,460 624,500 610,528 C618,500 614,462 596,436 Z", "Pronotum flank",
   fill="#140C0E", stroke=INK, strokeWidth=3)
bp("M388,520 C380,470 402,424 448,406 C480,396 520,396 552,406 "
   "C598,424 620,470 612,520 C570,534 430,534 388,520 Z", "Pronotum",
   fill=rad((0, "#6A585E"), (0.45, "#2E2226"), (1, "#110B0D")), stroke=INK, strokeWidth=5)
bs("ellipse", "Pronotum glow", x=414, y=420, width=110, height=56,
   fill="#B4A8D0", opacity=22, stroke=NONE)
bp("M414,488 C412,456 430,430 462,420", "Pronotum specular", fill=NONE,
   stroke="#FFFFFF", strokeWidth=5, opacity=65, cap="round")
bp("M572,428 C590,444 598,468 598,494", "Pronotum rim light", fill=NONE,
   stroke="#E8D8DC", strokeWidth=3, opacity=40, cap="round")

d.call("transform", {"ids": B, "rotate": -28, "origin": [500, 560]}, "rotate beetle")
d.call("transform", {"ids": B, "scale": 90, "origin": [500, 560]}, "scale beetle")
d.call("transform", {"ids": B, "dx": -10, "dy": -36}, "settle beetle")

# --- caption --------------------------------------------------------------------------
d.text("HERCULES BEETLE", "Name", x=500, y=940, size=52, font="Virelai Sans",
       color="#D6EEDC", justify="center")
o = d.text("COLEOPTERA", "Order", x=500, y=975, size=22, font="Virelai Sans",
           color="#9CC8A8", justify="center")
if o and "id" in o:
    d.cmd("text.setStyle", "Order tracking", ids=[o["id"]], tracking=400)

d.finish("hercules-beetle-V1R00")
