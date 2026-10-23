#!/usr/bin/env python3
"""Giraffe weevil — field plate V1R00. Side view, facing right: the long red
neck angled up and forward, warm-black body, elytra with a faint blue sheen,
standing on a leaf with the rolled leaf nest behind. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Giraffe Weevil — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420
INK = "#24171B"

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

def ribbon(p, widths, n=28, edges=False):
    """Closed outline of a tapering tube along cubic p; widths sampled
    piecewise-linearly over t. edges=True also returns the two side lines."""
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
    outline = f"M{pts[0][0]:.1f},{pts[0][1]:.1f} " + " ".join(
        f"L{x:.1f},{y:.1f}" for x, y in pts[1:]) + " Z"
    if not edges:
        return outline
    side = lambda q: f"M{q[0][0]:.1f},{q[0][1]:.1f} " + " ".join(
        f"L{x:.1f},{y:.1f}" for x, y in q[1:])
    return outline, side(left), side(right)

def polyline(pts):
    return f"M{pts[0][0]},{pts[0][1]} " + " ".join(f"L{x},{y}" for x, y in pts[1:])

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin(-90, (0, "#17301F"), (1, "#07130B")), stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#E0F0CC"), (0.7, "#ADD292"), (1, "#73A25B")),
        stroke="#4B7A3D", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#EEF8E2", strokeWidth=3, opacity=55)
d.shape("ellipse", "Patina 1", x=330, y=110, width=260, height=130,
        fill="#93C27A", opacity=22, stroke=NONE)
d.shape("ellipse", "Patina 2", x=560, y=430, width=230, height=150,
        fill="#93C27A", opacity=20, stroke=NONE)
for i, (x, y, w) in enumerate([(300, 250, 8), (430, 300, 6), (560, 160, 7), (820, 360, 7),
                               (170, 470, 7), (850, 470, 8), (400, 120, 6), (610, 300, 6)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#5E8F4C", opacity=40, stroke=NONE)

# faint fern frond behind, upper right
fern = ((862, 560), (870, 420), (830, 260), (770, 160))
d.path("M862,560 C870,420 830,260 770,160", "Fern rachis", fill=NONE,
       stroke="#4F8A40", strokeWidth=5, opacity=30, cap="round")
for i in range(1, 13):
    t = i / 13
    x, y, tx, ty = cubic(fern, t)
    ln = math.hypot(tx, ty); nx, ny = -ty / ln, tx / ln
    L = 58 * (1 - t) + 14
    for side in (1, -1):
        ex, ey = x + nx * L * side + tx / ln * 14, y + ny * L * side + ty / ln * 14
        # keep the right-hand leaflets inside the inner ring
        if math.hypot(ex - CX, ey - CY) > 388:
            sc = 388 / math.hypot(ex - CX, ey - CY)
            ex, ey = CX + (ex - CX) * sc, CY + (ey - CY) * sc
        mx, my = (x + ex) / 2 - tx / ln * 8 + nx * 6 * side, (y + ey) / 2 - ty / ln * 8 + ny * 6 * side
        d.path(f"M{x:.0f},{y:.0f} Q{mx:.0f},{my:.0f} {ex:.0f},{ey:.0f}",
               f"Fern pinna {i}{'a' if side > 0 else 'b'}", fill=NONE,
               stroke="#5C9A4A", strokeWidth=9 - 4 * t, opacity=24, cap="round")

# --- rolled leaf nest, behind at left ------------------------------------------
ROLL = lin(0, (0, "#B8DB8C"), (0.35, "#86B95E"), (0.8, "#4F8538"), (1, "#3A6A2A"))
d.path("M150,322 L150,646 C170,668 242,668 262,646 L262,322 Z", "Leaf roll body",
       fill=ROLL, stroke="#2F5223", strokeWidth=5)
d.path("M152,612 C176,540 214,450 260,372 L260,646 C240,664 174,666 152,646 Z",
       "Roll outer layer", fill=lin(0, (0, "#C6E49E"), (0.5, "#93C46A"), (1, "#4A7E34")),
       stroke=NONE, opacity=85)
d.path("M152,612 C176,540 214,450 260,372", "Roll outer margin", fill=NONE,
       stroke="#2F5223", strokeWidth=4, cap="round")
d.path("M158,616 C182,546 218,458 262,382", "Roll margin light", fill=NONE,
       stroke="#F0FADF", strokeWidth=3, opacity=50, cap="round")
for i, (x, y) in enumerate([(176, 560), (196, 508), (220, 456), (236, 600), (240, 520)]):
    d.path(f"M{x},{y} C{x+12},{y-4} {x+24},{y-14} {x+30},{y-26}", f"Roll vein {i+1}",
           fill=NONE, stroke="#2F5223", strokeWidth=3, opacity=30, cap="round")
d.path("M182,330 L182,640", "Roll highlight", fill=NONE, stroke="#F0FADF",
       strokeWidth=8, opacity=30, cap="round")
d.shape("ellipse", "Roll top", x=150, y=304, width=112, height=36,
        fill=rad((0, "#2C4C20"), (0.7, "#4E8238"), (1, "#7DB05A")),
        stroke="#2F5223", strokeWidth=5)
d.path("M206,322 C222,322 226,312 212,310 C194,308 186,322 200,330 "
       "C220,338 244,326 236,312", "Roll spiral", fill=NONE,
       stroke="#A9D282", strokeWidth=3, opacity=70, cap="round")
# loose leaf tip curling off the top of the roll
d.path("M240,316 C270,280 300,250 322,214 C300,226 268,236 248,262 "
       "C238,278 234,298 240,316 Z", "Leaf tip flap",
       fill=lin(90, (0, "#5E9844"), (1, "#A8D27E")), stroke="#2F5223", strokeWidth=4)
d.path("M244,300 C264,272 290,244 318,218", "Leaf tip midrib", fill=NONE,
       stroke="#E2F4C8", strokeWidth=3, opacity=55, cap="round")

# --- leaf the weevil stands on (closes on the disc arc) ------------------------
a0, a1 = disc_pt(150), disc_pt(28)
d.path(f"M{a0[0]:.1f},{a0[1]:.1f} C300,728 650,728 {a1[0]:.1f},{a1[1]:.1f} "
       f"A420,420 0 0 1 {a0[0]:.1f},{a0[1]:.1f} Z", "Leaf blade",
       fill=lin(-90, (0, "#8CC46C"), (0.45, "#5B9846"), (1, "#356B2C")),
       stroke="#2F5223", strokeWidth=5)
d.path(f"M{a0[0]+30:.0f},{a0[1]+40:.0f} C320,776 640,776 {a1[0]-30:.0f},{a1[1]+44:.0f}",
       "Leaf midrib", fill=NONE, stroke="#D8EFB8", strokeWidth=6, opacity=55, cap="round")
for i, (x0, y0, x1, y1) in enumerate([(230, 730, 270, 702), (340, 752, 390, 712),
                                      (460, 760, 510, 716), (580, 758, 630, 712),
                                      (700, 744, 750, 698), (300, 746, 280, 800),
                                      (440, 760, 430, 830), (600, 756, 610, 830),
                                      (740, 732, 760, 790)]):
    d.path(f"M{x0},{y0} Q{(x0+x1)/2+8},{(y0+y1)/2} {x1},{y1}", f"Leaf vein {i+1}",
           fill=NONE, stroke="#CBE8A8", strokeWidth=3, opacity=40, cap="round")
d.path(f"M{a0[0]+6:.0f},{a0[1]+4:.0f} C300,732 650,732 {a1[0]-6:.0f},{a1[1]+4:.0f}",
       "Leaf edge light", fill=NONE, stroke="#E8F7D0", strokeWidth=4, opacity=50, cap="round")
d.shape("ellipse", "Weevil shadow", x=290, y=694, width=420, height=26,
        fill="#1F3F1A", opacity=30, stroke=NONE)

# --- legs -------------------------------------------------------------------------
LEG = "#3A2C33"
def leg(name, coxa, knee, ankle, foot, far=False):
    col = "#1D1418" if far else LEG
    op = 90 if far else 100
    # clubbed femur
    fx, fy = coxa; kx, ky = knee
    d.path(ribbon(((fx, fy), (fx + (kx-fx)*0.33, fy + (ky-fy)*0.33),
                   (fx + (kx-fx)*0.66, fy + (ky-fy)*0.66), (kx, ky)), [10, 21, 12]),
           f"{name} femur", fill=lin(90, (0, col), (1, "#5A4A58" if not far else "#2A2026")),
           stroke=INK, strokeWidth=3, opacity=op)
    d.path(polyline([knee, ankle]), f"{name} tibia ink", fill=NONE, stroke=INK,
           strokeWidth=13, cap="round", opacity=op)
    d.path(polyline([knee, ankle]), f"{name} tibia", fill=NONE, stroke=col,
           strokeWidth=8, cap="round", opacity=op)
    d.path(polyline([ankle, foot]), f"{name} tarsus ink", fill=NONE, stroke=INK,
           strokeWidth=9, cap="round", opacity=op)
    d.path(polyline([ankle, foot]), f"{name} tarsus", fill=NONE, stroke=col,
           strokeWidth=5, cap="round", opacity=op)
    if not far:
        d.path(polyline([(fx + (kx-fx)*0.2, fy + (ky-fy)*0.2 - 3), (kx, ky - 3)]),
               f"{name} femur sheen", fill=NONE, stroke="#B8BEE6", strokeWidth=3,
               opacity=45, cap="round")
        # tarsal pads
        ax, ay = ankle; px, py = foot
        for j, t in enumerate([0.35, 0.7]):
            d.shape("ellipse", f"{name} pad {j+1}", x=ax + (px-ax)*t - 4,
                    y=ay + (py-ay)*t - 1, width=8, height=6, fill="#6E5A40",
                    opacity=80, stroke=NONE)
    # claw
    px, py = foot; ax, ay = ankle
    ln = math.hypot(px-ax, py-ay) or 1; ux, uy = (px-ax)/ln, (py-ay)/ln
    d.path(f"M{px:.0f},{py:.0f} Q{px+ux*8:.0f},{py+uy*8-2:.0f} {px+ux*10+3:.0f},{py+uy*10+5:.0f}",
           f"{name} claw", fill=NONE, stroke=INK, strokeWidth=3, cap="round", opacity=op)

# far-side legs first
leg("Far fore leg", (586, 600), (646, 630), (674, 692), (702, 696), far=True)
leg("Far mid leg", (500, 628), (532, 664), (546, 706), (572, 710), far=True)
leg("Far hind leg", (420, 630), (372, 656), (356, 700), (332, 704), far=True)

# --- elytra + abdomen --------------------------------------------------------------
d.path("M262,596 C280,640 340,654 410,654 C470,654 516,640 532,606 Z", "Abdomen underside",
       fill=lin(-90, (0, "#2E2328"), (1, "#140D10")), stroke=INK, strokeWidth=4)
ELY = rad((0, "#4E4048"), (0.55, "#2C2127"), (1, "#140D11"))
d.path("M250,572 C248,502 310,466 400,464 C480,463 532,498 538,554 "
       "C544,610 500,638 410,640 C320,642 252,628 250,572 Z", "Elytra",
       fill=ELY, stroke=INK, strokeWidth=6)
# striae following the dome
for i, off in enumerate([22, 44, 66, 88]):
    d.path(f"M{268+off*0.4:.0f},{575-off*0.1:.0f} C{272+off*0.3:.0f},{520+off*0.55:.0f} "
           f"{330:.0f},{486+off:.0f} {400:.0f},{485+off:.0f} "
           f"C{470:.0f},{485+off:.0f} {512-off*0.2:.0f},{510+off*0.7:.0f} {518-off*0.3:.0f},{556+off*0.2:.0f}",
           f"Elytra stria {i+1}", fill=NONE, stroke="#0E080B", strokeWidth=3,
           opacity=45, cap="round")
# faint sheen: broad cool glow + crisp specular arc
d.shape("ellipse", "Elytra sheen glow", x=300, y=476, width=200, height=64,
        fill="#8E9CD6", opacity=20, stroke=NONE)
d.path("M292,540 C300,500 346,478 402,476 C450,475 488,488 508,512", "Elytra specular",
       fill=NONE, stroke="#DCE2FF", strokeWidth=5, opacity=50, cap="round")
d.path("M300,556 C310,522 344,500 384,494", "Elytra specular short",
       fill=NONE, stroke="#FFFFFF", strokeWidth=3, opacity=45, cap="round")
d.path("M270,600 C310,628 400,636 480,626", "Elytra rim shade", fill=NONE,
       stroke="#000000", strokeWidth=8, opacity=22, cap="round")
d.shape("ellipse", "Humeral bump", x=470, y=486, width=46, height=30,
        fill="#5C4E5A", opacity=35, stroke=NONE)

# --- neck: pronotum tube + elongated head ------------------------------------------
NECK = lin(0, (0, "#F57A68"), (0.42, "#D8352B"), (1, "#7A1511"))
neck_lo = ((560, 548), (584, 476), (608, 414), (636, 358))
neck_hi = ((636, 360), (652, 318), (676, 258), (696, 218))
d.path("M526,566 C522,526 540,504 566,504 C594,504 606,530 604,562 "
       "C602,590 584,606 564,606 C542,606 528,590 526,566 Z", "Pronotum collar",
       fill=rad((0, "#E8604F"), (0.6, "#B82A22"), (1, "#5E100C")), stroke=INK, strokeWidth=5)
d.path("M540,594 C556,604 580,602 596,584", "Collar shade", fill=NONE,
       stroke="#3A0806", strokeWidth=7, opacity=35, cap="round")
lo_fill, lo_l, lo_r = ribbon(neck_lo, [62, 42, 32, 28], edges=True)
d.path(lo_fill, "Neck lower (prothorax)", fill=NECK, stroke=NONE)
d.path(lo_l, "Neck lower edge L", fill=NONE, stroke=INK, strokeWidth=5, cap="round")
d.path(lo_r, "Neck lower edge R", fill=NONE, stroke=INK, strokeWidth=5, cap="round")
d.path("M536,530 C544,514 556,508 570,508", "Collar sheen", fill=NONE,
       stroke="#FFC2B6", strokeWidth=4, opacity=55, cap="round")
d.path(ribbon(neck_hi, [24, 22, 21, 22]), "Neck upper (head)", fill=NECK,
       stroke=INK, strokeWidth=4)
d.shape("ellipse", "Neck joint", x=622, y=346, width=30, height=24,
        fill=lin(0, (0, "#B82A22"), (1, "#5E100C")), stroke=INK, strokeWidth=4)
# sheen down the lit side of the neck + translucent shading on the shadow side
d.path("M556,520 C574,470 598,414 626,366", "Neck lower sheen", fill=NONE,
       stroke="#FFC2B6", strokeWidth=6, opacity=55, cap="round")
d.path("M636,350 C652,312 670,268 688,230", "Neck upper sheen", fill=NONE,
       stroke="#FFC2B6", strokeWidth=4, opacity=55, cap="round")
for i, (x, y) in enumerate([(566, 500), (582, 470), (596, 440), (608, 412)]):
    d.shape("ellipse", f"Neck puncture {i+1}", x=x, y=y, width=5, height=4,
            fill="#5E100C", opacity=50, stroke=NONE)
# head knob, eye and snout
d.shape("ellipse", "Head", x=678, y=188, width=52, height=42,
        fill=rad((0, "#F2705E"), (0.6, "#C92E25"), (1, "#7A1511")),
        stroke=INK, strokeWidth=4)
d.path("M716,202 C732,208 746,224 754,242 C756,250 748,254 743,249 "
       "C734,238 722,230 708,226 Z", "Snout",
       fill=lin(-90, (0, "#E04A3C"), (1, "#7A1511")), stroke=INK, strokeWidth=3)
d.path("M750,248 L755,255 M750,248 L758,247", "Mandibles", fill=NONE, stroke=INK,
       strokeWidth=3, cap="round")
d.shape("ellipse", "Eye", x=702, y=199, width=15, height=15,
        fill=rad((0, "#5A4048"), (1, "#1A1013")), stroke=INK, strokeWidth=2)
d.shape("ellipse", "Eye glint", x=706, y=202, width=5, height=5,
        fill="#FFFFFF", opacity=85, stroke=NONE)
d.path("M690,202 C698,194 710,192 720,196", "Head sheen", fill=NONE,
       stroke="#FFD0C6", strokeWidth=3, opacity=60, cap="round")
# elbowed antenna with a club
d.path("M734,232 L764,210", "Antenna scape", fill=NONE, stroke=INK,
       strokeWidth=4, cap="round")
d.path("M764,210 C776,222 782,238 784,254", "Antenna funicle", fill=NONE,
       stroke=INK, strokeWidth=3.5, cap="round")
d.shape("ellipse", "Antenna club", x=777, y=250, width=14, height=22,
        fill=rad((0, "#6A4A50"), (1, "#24171B")), stroke=INK, strokeWidth=2)

# --- near legs ------------------------------------------------------------------------
leg("Hind leg", (402, 630), (342, 662), (318, 700), (292, 706))
leg("Mid leg", (482, 630), (446, 668), (466, 708), (494, 712))
leg("Fore leg", (560, 606), (612, 640), (628, 696), (656, 702))

# --- caption --------------------------------------------------------------------------
d.text("GIRAFFE WEEVIL", "Name", x=500, y=940, size=54, font="Virelai Sans",
       color="#D9EDCB", justify="center")
o = d.text("COLEOPTERA", "Order", x=500, y=975, size=22, font="Virelai Sans",
           color="#9EC08A", justify="center")
if o and "id" in o:
    d.cmd("text.setStyle", "Order tracking", ids=[o["id"]], tracking=400)

d.finish("giraffe-weevil-V1R00")
