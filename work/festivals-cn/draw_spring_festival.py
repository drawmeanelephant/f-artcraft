#!/usr/bin/env python3
"""Spring Festival — Festival Seal V1R00. The first of the Chinese-festival
series: two hanging lanterns under a silk cord, a fu-diamond at the centre,
plum branch in from the lower left, a red envelope spilling coins at the
lower right, fireworks behind. Vermilion and gold on deep ink. 1000x1000."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from orient.plate import (Plate, PCX, PCY, PR, NONE, INK, GOLD, GOLD_HI, GOLD_LO,
                          PAPER, LATIN, CJK, lin, rad, gold_lin, smooth, ribbon,
                          blossom, cloud, coin, blend)

SLUG = "spring-festival-V1R00"
VERM = "#D9433B"
VERM_HI = "#F2705A"
VERM_LO = "#8E1F1E"
VERM_DEEP = "#5C1216"
CORD = "#B8342C"

p = Plate("Spring Festival — Festival Seal", 1000, 1000)
d = p.d


# --- local helpers -----------------------------------------------------------
def inside(x, y, pad=0, label=""):
    if math.hypot(x - PCX, y - PCY) > PR - pad:
        raise AssertionError(f"outside disc: {label} ({x:.0f},{y:.0f})")
    return (x, y)


def poly(pts, label, **kw):
    return d.path("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z",
                  label, **kw)


def rotpts(pts, cx, cy, deg):
    a = math.radians(deg); c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s,
             cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def firework(cx, cy, r, label, seed=5, n=11, op=52):
    """Willow burst: curved trails that droop, plus falling embers."""
    d.shape("ellipse", f"{label} glow", x=cx - r * 1.05, y=cy - r * 1.05,
            width=2.1 * r, height=2.1 * r,
            fill=rad((0, "#FFC97E", 12), (0.55, "#E8663A", 5), (1, "#E8663A", 0)),
            stroke=NONE)
    s = seed
    for i in range(n):
        s = (1103515245 * s + 12345) % (2 ** 31)
        a = math.radians(i * 360 / n + (s % 100) / 100 * 8 - 4)
        s = (1103515245 * s + 12345) % (2 ** 31)
        rr = r * (0.72 + (s % 100) / 100 * 0.30)
        dx, dy = math.cos(a), math.sin(a)
        x0, y0 = cx + dx * r * 0.14, cy + dy * r * 0.14
        x1, y1 = cx + dx * rr, cy + dy * rr + rr * 0.16
        mx, my = (x0 + x1) / 2 - dy * rr * 0.10, (y0 + y1) / 2 + dx * rr * 0.10
        d.path(f"M{x0:.1f},{y0:.1f} Q{mx:.1f},{my:.1f} {x1:.1f},{y1:.1f}",
               f"{label} trail {i+1}", fill=NONE, stroke=GOLD, strokeWidth=2.2,
               opacity=op, cap="round")
        d.path(f"M{mx:.1f},{my:.1f} Q{(mx+x1)/2:.1f},{(my+y1)/2:.1f} {x1:.1f},{y1:.1f}",
               f"{label} trail tip {i+1}", fill=NONE, stroke=VERM_HI,
               strokeWidth=1.5, opacity=max(12, op - 22), cap="round")
        d.shape("ellipse", f"{label} tip {i+1}", x=x1 - 2.6, y=y1 - 2.6,
                width=5.2, height=5.2, fill=GOLD_HI, opacity=min(92, op + 20),
                stroke=NONE)
    for j in range(9):
        s = (1103515245 * s + 12345) % (2 ** 31)
        fa = math.radians(20 + (s % 100) / 100 * 140)
        fr = r * (1.05 + (s % 100) / 100 * 0.45)
        ex, ey = cx + math.cos(fa) * fr, cy + math.sin(fa) * fr * 1.15
        d.shape("ellipse", f"{label} ember {j+1}", x=ex - 1.4, y=ey - 1.4,
                width=2.8, height=2.8, fill="#FFD08A", opacity=40, stroke=NONE)
    d.shape("ellipse", f"{label} core halo", x=cx - 16, y=cy - 16, width=32,
            height=32, fill=rad((0, "#FFF3D0", 70), (1, "#FFC46B", 0)), stroke=NONE)
    d.shape("ellipse", f"{label} core", x=cx - 5, y=cy - 5, width=10, height=10,
            fill="#FFF8E0", opacity=90, stroke=NONE)


def cord(x0, y0, x1, y1, sag, label, sw=5):
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2 + sag
    d.path(f"M{x0:.1f},{y0:.1f} Q{mx:.1f},{my:.1f} {x1:.1f},{y1:.1f}", label,
           fill=NONE, stroke="#4A0E10", strokeWidth=sw + 2.4, cap="round")
    d.path(f"M{x0:.1f},{y0:.1f} Q{mx:.1f},{my:.1f} {x1:.1f},{y1:.1f}",
           f"{label} silk", fill=NONE, stroke=CORD, strokeWidth=sw, opacity=92,
           cap="round")
    d.path(f"M{x0:.1f},{y0 - 1:.1f} Q{mx:.1f},{my - 1:.1f} {x1:.1f},{y1 - 1:.1f}",
           f"{label} light", fill=NONE, stroke="#F2907A", strokeWidth=1.1,
           opacity=50, cap="round")


def hanging_lantern(cx, cy, w, h, ch, label):
    a, b = w / 2, h / 2
    d.shape("ellipse", f"{label} glow", x=cx - w * 0.95, y=cy - h * 0.82,
            width=w * 1.9, height=h * 1.66,
            fill=rad((0, "#FFB874", 20), (0.5, "#D9433B", 7), (1, "#D9433B", 0)),
            stroke=NONE)
    # body
    d.shape("ellipse", label, x=cx - a, y=cy - b, width=w, height=h,
            fill=lin((cx, cy - b), (cx, cy + b), (0, "#E85A42"), (0.45, "#C9372C"),
                     (1, "#7A1718")), stroke=INK, strokeWidth=4.5)
    # volume: offset sheen + bottom shade
    d.shape("ellipse", f"{label} sheen", x=cx - a * 0.66, y=cy - b * 0.72,
            width=a * 1.02, height=b * 1.24,
            fill=rad((0, "#FFD9B4", 30), (0.6, "#FF9E72", 10), (1, "#FF9E72", 0)),
            stroke=NONE)
    d.path(f"M{cx - a*0.92:.1f},{cy + b*0.24:.1f} C{cx - a*0.72:.1f},{cy + b*0.78:.1f} "
           f"{cx + a*0.72:.1f},{cy + b*0.78:.1f} {cx + a*0.92:.1f},{cy + b*0.24:.1f} "
           f"C{cx + a*0.6:.1f},{cy + b*0.9:.1f} {cx - a*0.6:.1f},{cy + b*0.9:.1f} "
           f"{cx - a*0.92:.1f},{cy + b*0.24:.1f} Z", f"{label} bottom shade",
           fill="#4A0A0C", opacity=30, stroke=NONE)
    # ribs, all inside the silhouette
    for k in (-0.72, -0.54, -0.36, -0.18, 0.0, 0.18, 0.36, 0.54, 0.72):
        dx = k * a
        s = math.sqrt(max(0.0, 1 - k * k))
        y0, y1 = cy - b * s * 0.985, cy + b * s * 0.985
        bulge = (1 if k >= 0 else -1) * 0.06 * w * (1 - abs(k))
        d.path(f"M{cx + dx:.1f},{y0:.1f} Q{cx + dx + bulge:.1f},{cy:.1f} "
               f"{cx + dx:.1f},{y1:.1f}", f"{label} rib {k}",
               fill=NONE, stroke="#F6B07A", strokeWidth=1.7, opacity=34, cap="round")
    # gold collars
    for sy, sw_, op in ((-0.40, 4.2, 92), (0.40, 4.2, 92)):
        yy = cy + sy * h
        d.path(f"M{cx - a*0.90:.1f},{yy - 4:.1f} Q{cx:.1f},{yy + 9:.1f} "
               f"{cx + a*0.90:.1f},{yy - 4:.1f}", f"{label} collar {sy}",
               fill=NONE, stroke=gold_lin(cy - b, cy + b), strokeWidth=sw_,
               opacity=op, cap="round")
    # caps
    for yy, lab2 in ((cy - b - 10, "top"), (cy + b - 2, "bottom")):
        d.shape("rectangle", f"{label} cap {lab2}", x=cx - w * 0.31, y=yy,
                width=w * 0.62, height=12, radius=3,
                fill=gold_lin(yy, yy + 12), stroke=INK, strokeWidth=2)
        d.shape("rectangle", f"{label} cap lip {lab2}", x=cx - w * 0.22, y=yy + 10,
                width=w * 0.44, height=4, radius=2, fill=GOLD_HI, opacity=55,
                stroke=NONE)
    # hanging loop
    d.path(f"M{cx:.1f},{cy - b - 10:.1f} C{cx - 7:.1f},{cy - b - 34:.1f} "
           f"{cx + 16:.1f},{cy - b - 40:.1f} {cx + 21:.1f},{cy - b - 22:.1f}",
           f"{label} loop", fill=NONE, stroke=INK, strokeWidth=3.4, cap="round")
    d.path(f"M{cx:.1f},{cy - b - 10:.1f} C{cx - 7:.1f},{cy - b - 34:.1f} "
           f"{cx + 16:.1f},{cy - b - 40:.1f} {cx + 21:.1f},{cy - b - 22:.1f}",
           f"{label} loop glint", fill=NONE, stroke=GOLD, strokeWidth=1.4,
           opacity=70, cap="round")
    # character
    d.shape("ellipse", f"{label} panel", x=cx - w * 0.26, y=cy - h * 0.27,
            width=w * 0.52, height=h * 0.54,
            fill=rad((0, "#FFCF96", 18), (1, "#C25A32", 4)), stroke=NONE)
    d.text(ch, f"{label} glyph", x=cx, y=cy + 17, size=w * 0.335, font=CJK,
           color="#FBE6B4", justify="center")
    # tassel
    ty = cy + b + 12
    d.shape("rectangle", f"{label} tassel knot", x=cx - 7, y=ty, width=14, height=13,
            radius=3, fill=gold_lin(ty, ty + 13), stroke=INK, strokeWidth=1.6)
    d.shape("ellipse", f"{label} tassel ring", x=cx - 9, y=ty + 11, width=18,
            height=9, fill=NONE, stroke=GOLD, strokeWidth=2, opacity=80)
    for i, dx in enumerate((-19, -13, -7, 0, 7, 13, 19)):
        endx = cx + dx * 1.5
        endy = ty + 62 + abs(dx) * 1.1
        d.path(f"M{cx + dx*0.35:.1f},{ty + 18:.1f} C{cx + dx*0.9:.1f},{ty + 34:.1f} "
               f"{endx:.1f},{endy - 14:.1f} {endx:.1f},{endy:.1f}",
               f"{label} tassel {i+1}", fill=NONE, stroke="#C0392E",
               strokeWidth=3.2 if i % 2 else 2.6, opacity=92, cap="round")
    d.path(f"M{cx:.1f},{ty + 18:.1f} L{cx:.1f},{ty + 70:.1f}", f"{label} tassel core",
           fill=NONE, stroke="#F2A08C", strokeWidth=1.4, opacity=55, cap="round")


# --- field ------------------------------------------------------------------
p.backdrop(top="#171014", bottom="#050408", glow=("#8E2A1E", 11))
p.disc("#3A1418", "#0C0507", rim="#D8A24E", rim2="#5A2A12")
d.shape("ellipse", "Vignette", x=80, y=40, width=840, height=840,
        fill=rad((0, "#000000", 0), (0.58, "#000000", 0), (1, "#000000", 66)),
        stroke=NONE)
d.shape("ellipse", "Rim relight", x=86, y=46, width=828, height=828, fill=NONE,
        stroke=lin((86, 46), (914, 874), (0, "#F0C078"), (0.5, "#B9853A"),
                   (1, "#E8BE76")), strokeWidth=4)
d.shape("ellipse", "Warm aura", x=120, y=20, width=760, height=660,
        fill=rad((0, "#C25A32", 20), (0.55, "#8E2A1E", 8), (1, "#8E2A1E", 0)),
        stroke=NONE)
p.ring_ticks(n=24, color="#C79A46", r_in=378, r_out=396, width=2.4)
for ang in (-135, -45, 45, 135):
    a = math.radians(ang)
    x, y = PCX + 399 * math.cos(a), PCY + 399 * math.sin(a)
    poly([(x, y - 7), (x + 7, y), (x, y + 7), (x - 7, y)], f"Ring diamond {ang}",
         fill=GOLD, opacity=70, stroke=NONE)

# --- air: fireworks + clouds -------------------------------------------------
firework(282, 210, 62, "Firework TL", seed=11, op=52)
firework(772, 356, 44, "Firework R", seed=29, op=44, n=9)
firework(196, 330, 32, "Firework L", seed=47, op=36, n=8)
cloud(d, 300, 700, 1.0, "Cloud BL", fill="#E8B06A", opacity=7)
cloud(d, 744, 626, 0.82, "Cloud BR", fill="#E8B06A", opacity=6)
cloud(d, 646, 820, 0.66, "Cloud B", fill="#E8B06A", opacity=5)

# --- silk cord + lanterns ----------------------------------------------------
inside(330, 96, 14, "cord L")
inside(670, 96, 14, "cord R")
cord(330, 96, 670, 96, 36, "Cord")
for x, y in ((330, 96), (670, 96)):
    d.shape("ellipse", f"Cord knot {x}", x=x - 6, y=y - 6, width=12, height=12,
            fill=gold_lin(y - 6, y + 6), stroke=INK, strokeWidth=1.5)
    d.path(f"M{x:.1f},{y + 6:.1f} L{x:.1f},{y + 22:.1f}", f"Cord tail {x}",
           fill=NONE, stroke=CORD, strokeWidth=3, cap="round")
    d.shape("ellipse", f"Cord tail bead {x}", x=x - 4, y=y + 20, width=8, height=8,
            fill=GOLD, stroke=INK, strokeWidth=1)

LANTERNS = ((366, 306, 150, 180, "春", "Lantern L"),
            (634, 330, 154, 184, "節", "Lantern R"))
for cx, cy, w, h, ch, lab in LANTERNS:
    inside(cx - w / 2, cy, 12, lab)
    inside(cx + w / 2, cy, 12, lab)
    inside(cx, cy + h / 2 + 100, 12, f"{lab} tassel")
    cord(cx, 116 if cx < 500 else 112, cx, cy - h / 2 - 34, 5, f"{lab} cord", sw=4)
    hanging_lantern(cx, cy, w, h, ch, lab)

# --- plum branch -------------------------------------------------------------
SPINE = [(218, 742), (243, 700), (222, 646), (256, 592), (240, 536), (268, 488),
         (298, 446)]
WIDTHS = [17, 14.5, 12.5, 11, 9, 7.5, 5]
bd, _, _, _ = ribbon(SPINE, WIDTHS)
d.path(bd, "Plum branch", fill=lin((218, 742), (298, 446), (0, "#7A4536"),
                                   (0.55, "#3A1C18"), (1, "#24100F")),
       stroke="#160A0B", strokeWidth=3)
d.path(smooth(SPINE), "Plum branch light", fill=NONE, stroke="#B07850",
       strokeWidth=2.6, opacity=40, cap="round")
TWIGS = [((243, 700), (288, 674)), ((222, 646), (184, 616)),
         ((256, 592), (296, 566)), ((240, 536), (202, 510)),
         ((268, 488), (304, 468)), ((232, 716), (204, 698)),
         ((240, 742), (272, 776)), ((300, 430), (330, 414))]
for i, (a, b) in enumerate(TWIGS):
    d.path(f"M{a[0]},{a[1]} Q{(a[0]+b[0])/2+4:.1f},{(a[1]+b[1])/2-8:.1f} {b[0]},{b[1]}",
           f"Twig {i+1}", fill=NONE, stroke="#4A2420", strokeWidth=4.4, cap="round")
    d.path(f"M{a[0]},{a[1]} Q{(a[0]+b[0])/2+4:.1f},{(a[1]+b[1])/2-8:.1f} {b[0]},{b[1]}",
           f"Twig light {i+1}", fill=NONE, stroke="#A06E50", strokeWidth=1.5,
           opacity=45, cap="round")

BLOSSOMS = [(288, 672, 22, -90), (184, 614, 19, -60), (298, 564, 18, 20),
            (201, 508, 18, -110), (306, 466, 16, 60), (232, 712, 12, -30),
            (260, 604, 11, 100), (272, 776, 14, 10), (330, 414, 13, -20),
            (206, 696, 10, 45)]
for i, (bx, by, br, rot) in enumerate(BLOSSOMS):
    inside(bx, by, br + 8, f"blossom {i}")
    blossom(d, bx, by, br, label=f"Plum blossom {i+1}", fill="#F6C6D0",
            core="#C2455A", rot=rot, opacity=94)
for i, (bx, by, br, rot) in enumerate([(212, 690, 9, -20), (274, 470, 8, 30),
                                       (246, 630, 7, 70), (300, 690, 8, 15)]):
    d.shape("ellipse", f"Bud {i+1}", x=bx - br * 0.55, y=by - br,
            width=br * 1.1, height=br * 1.9, fill="#B8455C",
            stroke="#5E1A24", strokeWidth=1.2, rotation=rot, opacity=92)

# --- fu diamond --------------------------------------------------------------
DCX, DCY, DR = 500, 570, 138
d.shape("ellipse", "Fu glow", x=DCX - 215, y=DCY - 215, width=430, height=430,
        fill=rad((0, "#FF9A5A", 26), (0.55, "#D9433B", 10), (1, "#D9433B", 0)),
        stroke=NONE)
FU = (f"M{DCX},{DCY-DR} C{DCX+50},{DCY-DR+50} {DCX+DR-50},{DCY-50} {DCX+DR},{DCY} "
      f"C{DCX+DR-50},{DCY+50} {DCX+50},{DCY+DR-50} {DCX},{DCY+DR} "
      f"C{DCX-50},{DCY+DR-50} {DCX-DR+50},{DCY+50} {DCX-DR},{DCY} "
      f"C{DCX-DR+50},{DCY-50} {DCX-50},{DCY-DR+50} {DCX},{DCY-DR} Z")
inside(DCX, DCY + DR + 4, 10, "fu bottom")
inside(DCX + DR + 4, DCY, 10, "fu right")
d.path(FU, "Fu paper", fill=lin((DCX - DR, DCY - DR), (DCX + DR, DCY + DR),
                                (0, "#F07A5A"), (0.28, "#D9433B"),
                                (0.72, "#A8282A"), (1, "#6E1418")),
       stroke=INK, strokeWidth=5)
poly([(DCX, DCY - DR + 10), (DCX + DR - 26, DCY - 10), (DCX - 10, DCY - DR + 76)],
     "Fu paper sheen", fill=lin((DCX, DCY - DR), (DCX + DR, DCY),
                                (0, "#FFC0A0", 22), (1, "#FFC0A0", 0)), stroke=NONE)
for scale, sw, op in ((0.885, 2.6, 88), (0.80, 1.3, 45)):
    o = DR * scale
    poly([(DCX, DCY - o), (DCX + o, DCY), (DCX, DCY + o), (DCX - o, DCY)],
         f"Fu border {scale}", fill=NONE, stroke=GOLD, strokeWidth=sw, opacity=op)
for ang in (-90, 0, 90, 180):
    a = math.radians(ang)
    x, y = DCX + (DR * 0.945) * math.cos(a), DCY + (DR * 0.945) * math.sin(a)
    poly([(x, y - 6), (x + 6, y), (x, y + 6), (x - 6, y)], f"Fu stud {ang}",
         fill=GOLD_HI, opacity=80, stroke=NONE)
d.text("福", "Fu shadow", x=DCX + 5, y=DCY + 62, size=152, font=CJK,
       color="#5A0F12", justify="center")
d.text("福", "Fu glyph", x=DCX, y=DCY + 57, size=152, font=CJK,
       color="#FBE6B4", justify="center")

# --- red envelope + coins ----------------------------------------------------
ECX, ECY, EW, EH, ER = 648, 686, 118, 170, -14
body = rotpts([(ECX - EW / 2, ECY - EH / 2), (ECX + EW / 2, ECY - EH / 2),
               (ECX + EW / 2, ECY + EH / 2), (ECX - EW / 2, ECY + EH / 2)],
              ECX, ECY, ER)
inside(*body[2], 12, "envelope corner")
d.shape("rectangle", "Envelope shadow", x=ECX - EW / 2 - 2, y=ECY - EH / 2 + 6,
        width=EW, height=EH, radius=4, fill="#000000", opacity=38, rotation=ER,
        stroke=NONE)
poly(body, "Envelope", fill=lin((ECX - EW, ECY - EH / 2), (ECX + EW, ECY + EH / 2),
                                (0, "#EE5945"), (0.45, "#C0332C"), (1, "#7A1718")),
     stroke=INK, strokeWidth=4)
flap = rotpts([(ECX - EW / 2, ECY - EH / 2), (ECX + EW / 2, ECY - EH / 2),
               (ECX, ECY - EH / 2 + 76)], ECX, ECY, ER)
poly(flap, "Envelope flap", fill=lin((ECX, ECY - EH / 2), (ECX, ECY - EH / 2 + 76),
                                     (0, "#F99073"), (1, "#C4402F")),
     stroke="#6E1418", strokeWidth=2.5)
d.path("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in flap[:2]) +
       f" L{flap[2][0]:.1f},{flap[2][1]:.1f}", "Envelope flap edge", fill=NONE,
       stroke="#FFC3A8", strokeWidth=1.2, opacity=45)
band = rotpts([(ECX - EW / 2 + 6, ECY + 20), (ECX + EW / 2 - 6, ECY + 20),
               (ECX + EW / 2 - 6, ECY + 48), (ECX - EW / 2 + 6, ECY + 48)],
              ECX, ECY, ER)
poly(band, "Envelope gold band", fill=lin((ECX, ECY + 20), (ECX, ECY + 48),
                                          (0, "#FBE6B4"), (0.5, "#D8A24E"),
                                          (1, "#8E5A1E")),
     stroke="#6E4A1A", strokeWidth=1.6)
for i, (dx, dy) in enumerate([(-34, 34), (-11, 34), (11, 34), (34, 34)]):
    p0 = rotpts([(ECX + dx, ECY + dy - 6), (ECX + dx + 6, ECY + dy),
                 (ECX + dx, ECY + dy + 6), (ECX + dx - 6, ECY + dy)],
                ECX, ECY, ER)
    poly(p0, f"Envelope band stud {i+1}", fill="#7A1718", opacity=55, stroke=NONE)
coin(d, ECX + 3, ECY - EH / 2 + 76, 22, "Envelope coin", sw=3)
d.text("福", "Envelope coin glyph", x=ECX + 3, y=ECY - EH / 2 + 84, size=22,
       font=CJK, color="#7A1718", justify="center")

# ground shadow under the fu + envelope
d.shape("ellipse", "Ground shadow", x=352, y=700, width=380, height=90,
        fill=rad((0, "#000000", 45), (0.6, "#000000", 20), (1, "#000000", 0)),
        stroke=NONE)
COINS = [(596, 790, 25, 8), (650, 806, 21, -14), (706, 776, 17, 24),
         (566, 820, 16, 30)]
for i, (x, y, r, rot) in enumerate(COINS):
    inside(x + r, y + r, 12, f"coin {i}")
    d.shape("ellipse", f"Coin shadow {i+1}", x=x - r * 0.9, y=y + r * 0.55,
            width=r * 1.9, height=r * 0.5, fill="#000000", opacity=30, stroke=NONE)
    coin(d, x, y, r, f"Coin {i+1}", sw=3)

# --- sparks and petals -------------------------------------------------------
SPARKS = [(322, 420, 2.6), (700, 470, 2.2), (412, 336, 2.0), (586, 214, 1.8),
          (246, 400, 1.8), (742, 600, 2.0), (356, 800, 1.8), (250, 560, 1.6),
          (770, 520, 1.6), (196, 500, 1.5)]
for i, (x, y, r) in enumerate(SPARKS):
    d.shape("ellipse", f"Spark halo {i+1}", x=x - r * 3, y=y - r * 3,
            width=r * 6, height=r * 6, fill=rad((0, "#FFD98E", 30), (1, "#FFD98E", 0)),
            stroke=NONE)
    d.shape("ellipse", f"Spark {i+1}", x=x - r / 2, y=y - r / 2, width=r, height=r,
            fill=GOLD_HI, stroke=NONE)
PETALS = [(360, 760, 9, -25), (300, 812, 8, 40), (404, 680, 7, 70),
          (330, 466, 7, 15), (250, 766, 7, -55), (466, 800, 6, 10)]
for i, (x, y, r, rot) in enumerate(PETALS):
    d.shape("ellipse", f"Petal {i+1}", x=x - r, y=y - r * 0.6, width=2 * r,
            height=r * 1.2, fill="#F2B4C2", opacity=50, stroke=NONE, rotation=rot)

# --- seal + caption ----------------------------------------------------------
CHX, CHY, CHW, CHH = 714, 148, 50, 136
inside(CHX + CHW, CHY, 6, "chop TR")
inside(CHX + CHW, CHY + CHH, 6, "chop BR")
d.shape("rectangle", "Chop shadow", x=CHX + 3, y=CHY + 4, width=CHW, height=CHH,
        radius=4, fill="#000000", opacity=30, stroke=NONE)
p.chop("春节", x=CHX, y=CHY, w=CHW, h=CHH, size=27)

p.caption("SPRING FESTIVAL", "春節 · LUNAR NEW YEAR · DAY 1",
          name_color="#F6E8CC", sub_color="#D2A45E",
          name_size=52, sub_size=20, tracking_name=62, tracking_sub=190)
p.finish(SLUG)
