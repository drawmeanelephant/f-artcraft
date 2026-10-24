#!/usr/bin/env python3
"""Clouded leopard — field plate V1R00. The cat that climbs down trees
headfirst: portrait high on a mossy bough, forearms draped over the top
edge, big paws hooked round the bark, the long tail flipped over the
bough's right end. Signature face: double cheek bars, crown stripe fan,
sabre-long canine tips under the upper lip. Montane mist plate —
cloud-forest ridges and hanging moss inside a pale jade disc.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math, re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Clouded Leopard — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#241A10"                    # warm dark ink, never pure black
CLOUD = "#2E2010"                  # the near-black of the cloud markings


def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}


def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}


def smooth(pts, closed=True, k=1.0):
    n = len(pts)
    s = "M%.1f,%.1f" % pts[0]
    for i in (range(n) if closed else range(n - 1)):
        p0 = pts[(i - 1) % n] if (closed or i > 0) else pts[0]
        p1, p2 = pts[i], pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (closed or i + 2 < n) else pts[-1]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6 * k, p1[1] + (p2[1] - p0[1]) / 6 * k)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6 * k, p2[1] - (p3[1] - p1[1]) / 6 * k)
        s += " C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (c1 + c2 + p2)
    return s + (" Z" if closed else "")


def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad


def rim_x(y, side=-1):
    return PCX + side * math.sqrt(PR * PR - (y - PCY) ** 2)


def mirror(dd):
    out, toks, ex = [], re.findall(r"[A-Za-z]|-?\d*\.?\d+", dd), True
    for t in toks:
        if t.isalpha():
            out.append(t); ex = True
        elif ex:
            out.append(f"{1000 - float(t):g},"); ex = False
        else:
            out[-1] += f"{float(t):g}"; ex = True
    return " ".join(out)


def pair(dd, label, **kw):
    d.path(dd, f"{label} L", **kw)
    d.path(mirror(dd), f"{label} R", **kw)


def cloud(cx, cy, r, label, rot=0.0, op=82):
    """Irregular dark blotch with a tawny-lit core — the namesake clouds."""
    t = math.radians(rot)
    pts = []
    for k, (a, f) in enumerate([(15, 1.05), (75, 0.9), (140, 1.15),
                              (200, 0.85), (262, 1.1), (330, 0.92)]):
        ar = math.radians(a)
        ex, ey = r * f * math.cos(ar), r * 0.78 * f * math.sin(ar)
        pts.append((cx + ex * math.cos(t) - ey * math.sin(t),
                    cy + ex * math.sin(t) + ey * math.cos(t)))
    d.path(smooth(pts), f"{label}", fill=CLOUD, opacity=op, stroke=NONE)
    d.path(smooth([(cx + (px - cx) * 0.55, cy + (py - cy) * 0.55)
                   for px, py in pts]),
           f"{label} core", fill="#4A3520", opacity=45, stroke=NONE)


BG_GRAD = lin(0, 0, 0, 1000, (0, "#12201A"), (1, "#040907"))
PLATE_GRAD = rad((0, "#C4DACB"), (0.55, "#8FB09C"), (1, "#54786A"))
RIDGE_FAR = lin(0, 300, 0, 460, (0, "#5E8272"), (1, "#7A9A88"))
RIDGE_NEAR = lin(0, 360, 0, 520, (0, "#40604F"), (1, "#56786A"))
BARK_GRAD = lin(0, 720, 0, 880, (0, "#6B5236"), (0.5, "#4A3624"), (1, "#2A1E12"))
MOSS_GRAD = lin(0, 715, 0, 760, (0, "#8AA86A"), (1, "#55703E"))
COAT_GRAD = rad((0, "#DDBE8C"), (0.6, "#B98F5C"), (1, "#7E5C38"))
PALE_GRAD = rad((0, "#F6EFDD"), (1, "#DFD0B0"))
IRIS_GRAD = rad((0, "#DCC072"), (0.65, "#9A7E40"), (1, "#5E4A24"))
EAR_GRAD = lin(0, 250, 0, 340, (0, "#3A2E1E"), (1, "#6B5638"))

# --- backdrop + montane plate ------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=58, y=18, width=884, height=884, fill="#7FA890", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#2A4638", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E4F2E8", strokeWidth=3, opacity=40)

# mist bands drifting through the canopy
for i, (x, y, w, h, op) in enumerate([(150, 240, 340, 46, 20), (560, 300, 300, 40, 16),
                                      (240, 480, 260, 36, 14), (620, 540, 240, 34, 15)]):
    assert on_disc(x + w / 2, y + h / 2, 60), i
    d.shape("ellipse", f"Mist band {i+1}", x=x, y=y, width=w, height=h,
            fill="#E8F2EA", opacity=op, stroke=NONE)

# two cloud-forest ridges, floating in haze, wholly inside the disc
d.path("M170,470 L235,398 L285,432 L345,362 L405,426 L470,382 L535,438 "
       "L600,370 L665,430 L725,392 L800,456 L830,470 Z",
       "Ridge far", fill=RIDGE_FAR, opacity=40, stroke=NONE)
d.path("M200,540 L270,470 L330,512 L395,452 L460,506 L525,462 L590,518 "
       "L655,468 L715,516 L790,540 Z",
       "Ridge near", fill=RIDGE_NEAR, opacity=45, stroke=NONE)

# hanging moss + lianas draping over the top rim, canopy above the cat
for i, (x, y0, y1, sway) in enumerate([(240, 78, 300, 26), (300, 62, 225, -20),
                                       (705, 66, 268, 22), (762, 84, 210, -16)]):
    d.path(f"M{x},{y0} C{x + sway},{(y0 + y1) / 2 - 28} {x - sway},{(y0 + y1) / 2 + 28} {x + sway // 2},{y1}",
           f"Liana {i+1}", fill=NONE, stroke="#15281C", strokeWidth=6, opacity=70, cap="round")
    for j in range(2, int((y1 - y0) / 46) + 2):
        yy = y0 + j * 46 - 20
        xx = x + sway * math.sin(j * 1.7) * 0.5
        d.path(f"M{xx:.0f},{yy:.0f} q{12},{3} {22},{16} q{-14},{2} {-22},{-16} Z",
               f"Liana {i+1} leaf {j}", fill="#24402C", opacity=75, stroke=NONE)

# epiphyte tufts on the rim crest
for i, (x, y) in enumerate([(420, 62), (452, 58), (560, 58), (592, 64)]):
    d.path(f"M{x},{y + 34} C{x - 8},{y + 10} {x - 4},{y} {x},{y - 8} "
           f"C{x + 4},{y} {x + 8},{y + 10} {x},{y + 34} Z",
           f"Moss tuft {i+1}", fill="#3A5A42", opacity=60, stroke=NONE)

# --- shoulders + chest, mostly swallowed by the bough -------------------------
BODY = smooth([(368, 545), (330, 590), (305, 650), (295, 720), (295, 760),
               (705, 760), (705, 720), (695, 650), (670, 590), (632, 545),
               (585, 565), (500, 585), (415, 565)])
d.path(BODY, "Shoulders", fill=COAT_GRAD, stroke=INK, strokeWidth=6)
# shoulder cloud markings — the plate's namesake
cloud(348, 640, 34, "Cloud L1", rot=-15)
cloud(390, 700, 26, "Cloud L2", rot=25)
cloud(652, 640, 34, "Cloud R1", rot=15)
cloud(610, 700, 26, "Cloud R2", rot=-25)
cloud(315, 590, 22, "Cloud L3", rot=40)
cloud(685, 590, 22, "Cloud R3", rot=-40)
# nape stripes spilling off the crown down the shoulders
pair("M392,548 C360,570 340,600 330,640", "Nape stripe", fill=NONE,
     stroke=CLOUD, strokeWidth=9, opacity=80, cap="round")
# pale chest wedge between the forelegs
d.path("M445,600 C438,650 442,700 460,735 L540,735 C558,700 562,650 555,600 "
       "C530,615 470,615 445,600 Z", "Chest ruff", fill=PALE_GRAD, opacity=80, stroke=NONE)
for i, dd in enumerate(["M470,640 C474,665 478,690 484,712",
                        "M530,640 C526,665 522,690 516,712"]):
    d.path(dd, f"Chest fur {i+1}", fill=NONE, stroke="#B09A74", strokeWidth=4, opacity=40, cap="round")

# --- the mossy bough, closing on the disc arc ---------------------------------
by = 745
bl, br = rim_x(by, -1), rim_x(by, 1)
BOUGH = [(bl, by), (250, 726), (330, 738), (420, 722), (500, 734),
         (585, 720), (665, 736), (745, 724), (br, by)]
for x, y in (BOUGH[0], BOUGH[-1]):
    assert abs(math.hypot(x - PCX, y - PCY) - PR) < 1.5
d.path(smooth(BOUGH, closed=False) + f" A{PR},{PR} 0 0 1 {bl:.1f},{by:.1f} Z",
       "Bough", fill=BARK_GRAD, stroke=NONE)
# moss riding the top edge
d.path(smooth([(x, y - 4) for x, y in BOUGH], closed=False) +
       f" L{br - 30},{by + 14} C700,{by + 30} 560,{by + 26} 470,{by + 22} "
       f"C380,{by + 18} 280,{by + 26} {bl + 26},{by + 12} Z",
       "Moss cap", fill=MOSS_GRAD, opacity=85, stroke=NONE)
# bark fissures + a bracket fungus on the near face
for i, dd in enumerate(["M250,790 C300,782 340,786 380,794",
                        "M560,806 C620,796 680,798 730,808",
                        "M420,842 C480,834 540,836 600,844"]):
    d.path(dd, f"Bark fissure {i+1}", fill=NONE, stroke="#1E140A",
           strokeWidth=4, opacity=55, cap="round")
d.path("M640,796 C640,780 668,774 686,784 C700,792 698,808 682,812 "
       "C664,816 640,810 640,796 Z", "Bracket fungus", fill="#C8B088",
       opacity=70, stroke="#4A3624", strokeWidth=3)
# lichen rosettes on the bark
for i, (x, y, r) in enumerate([(300, 810, 12), (470, 800, 10), (700, 850, 11),
                               (380, 858, 9), (560, 862, 10)]):
    d.path(smooth([(x + r * math.cos(a), y + r * 0.7 * math.sin(a))
                   for a in [math.radians(t) for t in range(0, 360, 45)]]),
           f"Lichen {i+1}", fill="#9DB87E", opacity=40, stroke=NONE)

# --- the tail flipped over the bough's right end ------------------------------
spine = []
for i in range(17):
    t = i / 16
    u = 1 - t
    x = u * u * 716 + 2 * u * t * 756 + t * t * 704
    y = u * u * 696 + 2 * u * t * 770 + t * t * 806
    spine.append((x, y))
for i in range(1, 11):
    t = i / 10
    u = 1 - t
    x = u * u * 704 + 2 * u * t * 672 + t * t * 676
    y = u * u * 806 + 2 * u * t * 844 + t * t * 800
    spine.append((x, y))
Lp, Rp = [], []
n = len(spine)
for i, (x, y) in enumerate(spine):
    ax, ay = spine[max(i - 1, 0)]; bx, byy = spine[min(i + 1, n - 1)]
    dx, dy = bx - ax, byy - ay
    ln = math.hypot(dx, dy) or 1
    nx, ny = -dy / ln, dx / ln
    w = (46 - 16 * i / (n - 1)) / 2
    Lp.append((x + nx * w, y + ny * w)); Rp.append((x - nx * w, y - ny * w))
dd = "M%.1f,%.1f " % Lp[0] + " ".join("L%.1f,%.1f" % p for p in Lp[1:])
dd += " A%.1f,%.1f 0 0 0 %.1f,%.1f " % (w, w, Rp[-1][0], Rp[-1][1])
dd += " ".join("L%.1f,%.1f" % p for p in reversed(Rp[:-1])) + " Z"
d.path(dd, "Tail", fill=lin(760, 700, 780, 850, (0, "#B98F5C"), (1, "#7E5C38")),
       stroke=INK, strokeWidth=5)
# dark tail rings, unevenly spaced
for i, j in enumerate([4, 9, 14, 19, 23]):
    (x, y) = spine[j]
    ax, ay = spine[j - 1]; bx, byy = spine[j + 1]
    dx, dy = bx - ax, byy - ay
    ln = math.hypot(dx, dy) or 1
    nx, ny = -dy / ln, dx / ln
    w = (46 - 16 * j / (n - 1)) / 2
    d.path(f"M{x + nx * w:.1f},{y + ny * w:.1f} L{x - nx * w:.1f},{y - ny * w:.1f}",
           f"Tail ring {i+1}", fill=NONE, stroke=CLOUD, strokeWidth=8,
           opacity=75, cap="round")

# --- forearms draped over the bough + the great hooked paws -------------------
pair("M352,624 C340,668 334,712 342,752 C346,772 350,786 354,796 "
     "C382,806 404,798 410,776 C414,730 412,682 404,636 C388,626 368,622 352,624 Z",
     "Foreleg", fill=COAT_GRAD, stroke=INK, strokeWidth=5)
pair("M358,636 C350,678 346,716 352,750", "Foreleg sheen", fill=NONE,
     stroke="#F0E2C4", strokeWidth=6, opacity=30, cap="round")
# paws: knuckle row cresting above the bough edge, toes hanging down the face
PAW = smooth([(318, 748), (326, 722), (350, 706), (382, 702), (412, 712),
              (424, 734), (424, 760), (416, 784), (392, 800), (356, 802),
              (330, 788), (318, 766)])
pair(PAW, "Paw", fill=PALE_GRAD, stroke=INK, strokeWidth=5)
for j, x in enumerate([352, 380, 406]):
    pair(f"M{x},{712} C{x - 4},{726} {x - 4},{742} {x - 2},{756}",
         f"Knuckle dip {j+1}", fill=NONE, stroke=INK, strokeWidth=4,
         opacity=55, cap="round")
for j, x in enumerate([346, 372, 398]):
    pair(f"M{x},{790} L{x - 2},{774}", f"Toe line {j+1}", fill=NONE,
         stroke=INK, strokeWidth=3.5, opacity=60, cap="round")
# claws hooked over the bark — small dark ticks on the crest
for j, x in enumerate([340, 366, 392]):
    pair(f"M{x},{704} C{x - 2},{712} {x - 2},{716} {x + 2},{720}",
         f"Claw {j+1}", fill=NONE, stroke="#14100A", strokeWidth=5, cap="round")
# foreleg cloud spots
cloud(376, 668, 15, "Leg cloud L", rot=30)
cloud(624, 668, 15, "Leg cloud R", rot=-30)

# --- head ---------------------------------------------------------------------
EAR = smooth([(352, 320), (340, 288), (350, 258), (378, 244), (408, 250),
              (424, 272), (424, 300), (400, 318)])
pair(EAR, "Ear", fill=EAR_GRAD, stroke=INK, strokeWidth=5)
pair("M364,306 C358,286 364,266 382,260 C400,254 414,268 416,288 "
     "C404,280 388,280 378,290 C372,296 368,302 364,306 Z",
     "Inner ear", fill="#8A6F4C", opacity=75, stroke=NONE)

HEAD = smooth([(500, 282), (576, 284), (636, 316), (662, 378), (662, 442),
               (640, 500), (600, 556), (560, 596), (530, 622), (500, 630),
               (470, 622), (440, 596), (400, 556), (360, 500), (338, 442),
               (338, 378), (364, 316), (424, 284)])
d.path(HEAD, "Head", fill=COAT_GRAD, stroke=INK, strokeWidth=7)
d.shape("ellipse", "Brow light", x=420, y=296, width=160, height=52,
        fill="#F6EACC", opacity=22, stroke=NONE)

# crown stripe fan: dark stripes running back from between the eyes
for i, dd in enumerate(["M500,330 C498,356 498,382 500,408",
                        "M462,334 C466,360 472,384 482,406",
                        "M538,334 C534,360 528,384 518,406",
                        "M428,346 C438,370 450,392 464,410",
                        "M572,346 C562,370 550,392 536,410"]):
    d.path(dd, f"Crown stripe {i+1}", fill=NONE, stroke=CLOUD,
           strokeWidth=6, opacity=75, cap="round")
# small spots flanking the fan
for i, (x, y, w) in enumerate([(438, 322, 9), (562, 322, 9), (414, 340, 7),
                               (586, 340, 7), (456, 316, 7), (544, 316, 7)]):
    d.shape("ellipse", f"Crown spot {i+1}", x=x, y=y, width=w, height=w * 0.8,
            fill=CLOUD, opacity=75, stroke=NONE)

# --- eyes: big, amber, heavy-lidded -------------------------------------------
EYE = smooth([(394, 428), (410, 404), (440, 396), (468, 404), (482, 424),
              (462, 444), (426, 446), (402, 440)])
pair(EYE, "Eye", fill=IRIS_GRAD, stroke=INK, strokeWidth=5)
d.shape("ellipse", "Pupil L", x=432, y=410, width=13, height=20, fill="#14100A", stroke=NONE)
d.shape("ellipse", "Pupil R", x=555, y=410, width=13, height=20, fill="#14100A", stroke=NONE)
d.shape("ellipse", "Glint L", x=436, y=413, width=6, height=6, fill="#FFFFFF", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=559, y=413, width=6, height=6, fill="#FFFFFF", opacity=90, stroke=NONE)
pair("M392,424 C410,400 444,392 480,414", "Upper lid", fill=NONE,
     stroke=INK, strokeWidth=7, cap="round")
pair("M404,394 C426,380 456,378 478,388", "Brow shade", fill=NONE,
     stroke="#7E5C38", strokeWidth=9, opacity=25, cap="round")
pair("M408,444 C430,452 456,450 474,438", "Eye rim light", fill=NONE,
     stroke="#F6EFDD", strokeWidth=4, opacity=55, cap="round")

# --- the signature double cheek bars, converging to the jaw --------------------
pair(smooth([(398, 444), (382, 478), (378, 512), (388, 540),
             (380, 542), (370, 510), (374, 476), (390, 440)]),
     "Cheek bar outer", fill=CLOUD, opacity=85, stroke=NONE)
pair(smooth([(420, 452), (408, 488), (406, 520), (416, 546),
             (408, 546), (398, 518), (400, 486), (412, 448)]),
     "Cheek bar inner", fill=CLOUD, opacity=80, stroke=NONE)
# small cheek spots between the bars and the jaw
for i, (x, y, w) in enumerate([(372, 478, 7), (390, 508, 6), (420, 476, 6)]):
    d.shape("ellipse", f"Cheek spot L{i+1}", x=x, y=y, width=w, height=w,
            fill=CLOUD, opacity=70, stroke=NONE)
    d.shape("ellipse", f"Cheek spot R{i+1}", x=1000 - x - w, y=y, width=w, height=w,
            fill=CLOUD, opacity=70, stroke=NONE)

# --- muzzle -------------------------------------------------------------------
d.path("M500,440 C522,440 534,462 544,480 C574,486 598,506 598,532 "
       "C596,560 556,576 500,576 C444,576 404,560 402,532 "
       "C402,506 426,486 456,480 C466,462 478,440 500,440 Z",
       "Muzzle pale", fill=PALE_GRAD, opacity=92, stroke=NONE)
# dark nose bridge running up between the eyes
d.path("M500,412 C492,428 488,448 490,466 L510,466 C512,448 508,428 500,412 Z",
       "Nose bridge", fill="#5E4228", opacity=60, stroke=NONE)
d.path("M472,474 C488,466 512,466 528,474 C528,492 514,504 500,506 "
       "C486,504 472,492 472,474 Z",
       "Nose", fill=lin(0, 468, 0, 506, (0, "#B0785C"), (1, "#7A4A3C")),
       stroke=INK, strokeWidth=4)
d.shape("ellipse", "Nose glint", x=484, y=474, width=11, height=5,
        fill="#FFFFFF", opacity=45, stroke=NONE)
d.path("M500,506 L500,522", "Philtrum", fill=NONE, stroke=INK, strokeWidth=4, cap="round")
# level mouth, corners ticked down — a cat's sulk, not a smile
pair("M500,524 C488,530 472,532 458,530", "Mouth", fill=NONE,
     stroke=INK, strokeWidth=4.5, cap="round")
pair("M458,530 C452,536 450,542 452,548", "Mouth corner", fill=NONE,
     stroke=INK, strokeWidth=4, opacity=80, cap="round")
# sabre-canine hints below the upper lip — the longest canines of any cat
pair("M462,532 C460,544 462,554 468,558 C472,552 472,540 468,532 Z",
     "Canine hint", fill="#F2EAD6", stroke=INK, strokeWidth=2.5, opacity=95)
d.path("M462,556 C482,566 518,566 538,556", "Chin shade", fill=NONE,
       stroke="#9A825E", strokeWidth=8, opacity=25, cap="round")
# whisker dots + the famously long whiskers
for j, (x, y) in enumerate([(446, 512), (458, 520), (444, 524), (460, 508)]):
    d.shape("ellipse", f"Whisker dot L{j+1}", x=x, y=y, width=4, height=4,
            fill=CLOUD, opacity=55, stroke=NONE)
    d.shape("ellipse", f"Whisker dot R{j+1}", x=1000 - x - 4, y=y, width=4, height=4,
            fill=CLOUD, opacity=55, stroke=NONE)
for j, (x1, y1, x2, y2) in enumerate([(438, 508, 296, 478), (438, 518, 288, 514),
                                      (442, 528, 302, 552), (446, 536, 320, 588),
                                      (434, 498, 310, 446)]):
    pair(f"M{x1},{y1} Q{(x1 + x2) / 2},{min(y1, y2) - 8} {x2},{y2}",
         f"Whisker {j+1}", fill=NONE, stroke="#F8F2E4",
         strokeWidth=2.5, opacity=75, cap="round")

# --- name ----------------------------------------------------------------------
d.text("CLOUDED LEOPARD", "Name", x=500, y=962, size=54, font="Virelai Sans",
       color="#D4E6D8", justify="center")

d.finish("clouded-leopard-V1R00")
