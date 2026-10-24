#!/usr/bin/env python3
"""Spotted hyena — field plate V1R00. The laugh that is not a laugh:
head-on, low brow, ears set wide, mouth pulled back in the grimace with
carnassial tips showing — the jaws that crack bone. In front, on the
dust line, the snapped marrow bone it just opened. Savanna-night plate:
moon, acacia, star flecks. 1000x1000. House style: gradients +
translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math, re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Spotted Hyena — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#1E150E"                    # warm dark ink, never pure black
SPOT = "#352A1C"


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


def spot(x, y, w, h, label, op=70):
    d.shape("ellipse", label, x=x - w / 2, y=y - h / 2, width=w, height=h,
            fill=SPOT, opacity=op, stroke=NONE)


BG_GRAD = lin(0, 0, 0, 1000, (0, "#101624"), (1, "#04060C"))
PLATE_GRAD = rad((0, "#A8B4C8"), (0.55, "#687896"), (1, "#33405C"))
COAT_GRAD = rad((0, "#9C8A6E"), (0.6, "#7A6850"), (1, "#4E4232"))
MUZZLE_GRAD = lin(0, 470, 0, 590, (0, "#4E4234"), (1, "#2E2418"))
EAR_GRAD = lin(0, 240, 0, 360, (0, "#3A2E1E"), (1, "#6B5A40"))
GROUND_GRAD = lin(0, 760, 0, 880, (0, "#6E5E44"), (0.6, "#453826"), (1, "#241C10"))

# --- backdrop + night plate ----------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=58, y=18, width=884, height=884, fill="#7E8EAC", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#222E44", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C4D0E4", strokeWidth=3, opacity=35)

# the moon and its halo, upper right
d.shape("ellipse", "Moon halo", x=520, y=110, width=260, height=260,
        fill="#DCE6F4", opacity=14, stroke=NONE)
d.shape("ellipse", "Moon", x=586, y=156, width=128, height=128,
        fill=rad((0, "#F2F4F6"), (0.8, "#D8DEE8"), (1, "#B0BACA")),
        opacity=95, stroke=NONE)
for i, (x, y, w) in enumerate([(620, 190, 20), (664, 236, 14), (636, 246, 10)]):
    d.shape("ellipse", f"Moon mare {i+1}", x=x, y=y, width=w, height=w * 0.7,
            fill="#AAB4C8", opacity=35, stroke=NONE)

# star flecks inside the disc
for i, (x, y, w) in enumerate([(220, 200, 5), (330, 130, 4), (170, 330, 4),
                               (430, 110, 5), (740, 140, 4), (830, 250, 5),
                               (150, 480, 4), (860, 420, 4), (270, 140, 3)]):
    assert on_disc(x, y, 6), i
    d.shape("ellipse", f"Star {i+1}", x=x - w / 2, y=y - w / 2, width=w, height=w,
            fill="#E8EEF8", opacity=65, stroke=NONE)

# acacia silhouettes on the night horizon, wholly inside the disc
for i, (cx, ty, w, h) in enumerate([(250, 560, 150, 110), (800, 590, 120, 85)]):
    d.path(f"M{cx},{ty + h} L{cx - 3},{ty + h * 0.55} L{cx - w * 0.35},{ty + h * 0.5} "
           f"C{cx - w * 0.5},{ty + h * 0.35} {cx - w * 0.42},{ty + h * 0.12} {cx - w * 0.25},{ty + h * 0.14} "
           f"C{cx - w * 0.3},{ty} {cx + w * 0.3},{ty} {cx + w * 0.25},{ty + h * 0.14} "
           f"C{cx + w * 0.42},{ty + h * 0.12} {cx + w * 0.5},{ty + h * 0.35} {cx + w * 0.35},{ty + h * 0.5} "
           f"L{cx + 3},{ty + h * 0.55} L{cx + 2},{ty + h} Z",
           f"Acacia {i+1}", fill="#1C2434", opacity=75, stroke=NONE)

# --- dust floor, closing on the disc arc ----------------------------------------
fy = 770
fl, fr = rim_x(fy, -1), rim_x(fy, 1)
d.path(f"M{fl:.1f},{fy} C300,758 400,774 500,768 C600,762 700,766 {fr:.1f},{fy} "
       f"A{PR},{PR} 0 0 1 {fl:.1f},{fy} Z", "Dust floor", fill=GROUND_GRAD, stroke=NONE)
d.path(f"M{fl + 8:.0f},{fy} C300,758 400,774 500,768 C600,762 700,766 {fr - 8:.0f},{fy}",
       "Floor crest", fill=NONE, stroke="#A89468", strokeWidth=5, opacity=40, cap="round")
# dry grass tufts
for i, (x, y, s) in enumerate([(260, 782, 1), (350, 792, -1), (640, 786, 1), (730, 780, -1)]):
    for j, (dx, dy) in enumerate([(-6, -20), (0, -26), (6, -18)]):
        d.path(f"M{x},{y} Q{x + dx * 0.5},{y + dy * 0.6} {x + dx + s * j * 3},{y + dy}",
               f"Grass {i+1}.{j+1}", fill=NONE, stroke="#8A7A50",
               strokeWidth=3, opacity=55, cap="round")
# bone chips strewn near the paws — previous dinners
for i, (x, y, a) in enumerate([(330, 806, 20), (676, 812, -30), (390, 826, 65)]):
    t = math.radians(a); c_, s_ = math.cos(t), math.sin(t)
    d.path(f"M{x},{y} q{7 * c_:.0f},{7 * s_:.0f} {16 * c_:.0f},{16 * s_:.0f} "
           f"q{-6 * c_ + 3 * s_:.0f},{-6 * s_ - 3 * c_:.0f} {-16 * c_:.0f},{-16 * s_:.0f} Z",
           f"Bone chip {i+1}", fill="#D8D0B8", opacity=70, stroke=NONE)

# --- shoulders + forelegs, head carried low -------------------------------------
BODY = smooth([(360, 560), (320, 610), (300, 680), (300, 750), (305, 770),
               (695, 770), (700, 750), (700, 680), (680, 610), (640, 560),
               (585, 580), (500, 596), (415, 580)])
d.path(BODY, "Shoulders", fill=COAT_GRAD, stroke=INK, strokeWidth=6)
# the sloped-back hint: shoulders highest at the withers, dropping behind
d.path("M340,600 C320,650 312,700 314,748", "Shoulder edge L", fill=NONE,
       stroke=INK, strokeWidth=4, opacity=45, cap="round")
d.path("M660,600 C680,650 688,700 686,748", "Shoulder edge R", fill=NONE,
       stroke=INK, strokeWidth=4, opacity=45, cap="round")
# mane bristles along the withers
for i, (x0, y0, x1, y1) in enumerate([(370, 578, 352, 556), (400, 568, 384, 546),
                                      (600, 568, 616, 546), (630, 578, 648, 556)]):
    d.path(f"M{x0},{y0} L{x1},{y1}", f"Mane {i+1}", fill=NONE,
           stroke="#3A2E1E", strokeWidth=7, opacity=70, cap="round")
# body spots
for i, (x, y, w, h) in enumerate([(345, 640, 22, 16), (385, 700, 18, 14),
                                  (655, 640, 22, 16), (615, 700, 18, 14),
                                  (330, 720, 16, 12), (670, 720, 16, 12),
                                  (415, 645, 15, 12), (585, 645, 15, 12)]):
    spot(x, y, w, h, f"Body spot {i+1}")
# chest shadow wedge
d.path("M448,610 C444,660 448,712 462,752 L538,752 C552,712 556,660 552,610 "
       "C528,620 472,620 448,610 Z", "Chest shade", fill="#3E3424", opacity=50, stroke=NONE)

# forelegs to the paws pinning the bone
pair("M368,700 C360,724 356,748 360,768 C378,776 404,776 418,766 "
     "C420,744 418,722 412,702 Z", "Foreleg", fill=COAT_GRAD, stroke=INK, strokeWidth=4)
# paws splayed over the bone ends
pair("M336,762 C334,742 352,730 378,732 C404,734 420,746 418,764 "
     "C416,782 394,792 370,790 C350,788 338,778 336,762 Z",
     "Paw", fill=lin(0, 730, 0, 792, (0, "#8A7860"), (1, "#5E4E38")),
     stroke=INK, strokeWidth=4.5)
for j, x in enumerate([360, 382, 402]):
    pair(f"M{x},{738} C{x - 3},{750} {x - 3},{762} {x - 1},{772}",
         f"Toe {j+1}", fill=NONE, stroke=INK, strokeWidth=3.5, opacity=55, cap="round")

# --- the cracked marrow bone between the paws -----------------------------------
# left half — snapped end jagged at the middle
d.path("M428,758 C428,744 442,736 458,738 L486,742 L476,752 L488,760 "
       "L478,768 L486,776 L460,780 C444,782 428,772 428,758 Z",
       "Bone left", fill=rad((0, "#F0E8D2"), (1, "#B8AE92")),
       stroke="#6E6250", strokeWidth=3)
# right half — the matching jagged break
d.path("M572,758 C572,744 558,736 542,738 L514,742 L524,752 L512,760 "
       "L522,768 L514,776 L540,780 C556,782 572,772 572,758 Z",
       "Bone right", fill=rad((0, "#F0E8D2"), (1, "#B8AE92")),
       stroke="#6E6250", strokeWidth=3)
# the dark marrow line, freshly opened
d.path("M446,756 L482,760 M518,760 L554,756", "Marrow", fill=NONE,
       stroke="#5A4030", strokeWidth=4, opacity=80, cap="round")
# two flying splinters above the break
d.path("M492,724 L500,712 L505,726 Z", "Splinter 1", fill="#E8E0CC",
       opacity=80, stroke=NONE)
d.path("M508,732 L520,722 L518,736 Z", "Splinter 2", fill="#E8E0CC",
       opacity=65, stroke=NONE)

# --- ears: big, round, set wide — the head's own satellite dishes ---------------
EAR = smooth([(330, 360), (300, 330), (296, 292), (316, 262), (350, 254),
              (380, 264), (392, 292), (388, 326), (368, 352)])
pair(EAR, "Ear", fill=EAR_GRAD, stroke=INK, strokeWidth=5)
pair("M320,330 C312,308 318,286 338,278 C358,270 376,282 378,304 "
     "C364,296 344,300 332,314 C328,320 324,326 320,330 Z",
     "Inner ear", fill="#241C12", opacity=80, stroke=NONE)

# --- head: massive brow, low carried --------------------------------------------
HEAD = smooth([(500, 300), (580, 300), (648, 336), (676, 398), (670, 462),
               (636, 524), (586, 566), (540, 592), (500, 598), (460, 592),
               (414, 566), (364, 524), (330, 462), (324, 398), (352, 336),
               (420, 300)])
d.path(HEAD, "Head", fill=COAT_GRAD, stroke=INK, strokeWidth=7)
# head-top light pooling from the moon
d.shape("ellipse", "Brow light", x=430, y=312, width=170, height=56,
        fill="#C0C8D8", opacity=18, stroke=NONE)
# the dark mask — muzzle and eye surrounds
d.path("M420,410 C450,386 550,386 580,410 C600,436 606,478 596,514 "
       "C576,548 540,566 500,566 C460,566 424,548 404,514 "
       "C394,478 400,436 420,410 Z", "Mask", fill=MUZZLE_GRAD, opacity=78, stroke=NONE)
# forehead furrow — the worried wrinkle above the grimace
d.path("M500,336 C498,366 498,392 500,414", "Furrow", fill=NONE,
       stroke="#3A2E1E", strokeWidth=6, opacity=60, cap="round")
pair("M432,362 C452,352 476,348 496,350", "Brow crease", fill=NONE,
     stroke="#3A2E1E", strokeWidth=5, opacity=45, cap="round")
# head spots
for i, (x, y, w) in enumerate([(452, 322, 13), (548, 322, 13), (412, 340, 11),
                               (588, 340, 11), (500, 320, 12), (468, 344, 9),
                               (532, 344, 9), (380, 372, 10), (620, 372, 10)]):
    spot(x, y, w, w * 0.8, f"Head spot {i+1}", op=75)

# --- eyes: small, hard, catching the moon -----------------------------------------
EYE = smooth([(414, 396), (430, 382), (452, 380), (468, 390), (462, 406),
              (442, 412), (422, 408)])
pair(EYE, "Eye", fill=rad((0, "#C89A4A"), (0.7, "#8A6A28"), (1, "#54400F")),
     stroke=INK, strokeWidth=4.5)
d.shape("ellipse", "Pupil L", x=438, y=388, width=9, height=12, fill="#120C06", stroke=NONE)
d.shape("ellipse", "Pupil R", x=553, y=388, width=9, height=12, fill="#120C06", stroke=NONE)
d.shape("ellipse", "Glint L", x=440, y=390, width=4.5, height=4.5, fill="#FFFFFF", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=555, y=390, width=4.5, height=4.5, fill="#FFFFFF", opacity=90, stroke=NONE)
pair("M410,392 C428,376 456,374 474,386", "Upper lid", fill=NONE,
     stroke=INK, strokeWidth=6, cap="round")

# --- muzzle + the grimace ---------------------------------------------------------
# broad dark nose
d.path("M466,478 C480,468 520,468 534,478 C540,494 530,506 500,508 "
       "C470,506 460,494 466,478 Z", "Nose", fill="#1E140C",
       stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Nose glint", x=480, y=478, width=14, height=6,
        fill="#8A94A8", opacity=40, stroke=NONE)
d.path("M500,508 L500,524", "Philtrum", fill=NONE, stroke=INK, strokeWidth=4, cap="round")
# the laugh that is not a laugh: lip pulled wide, corners hard back,
# mouth dark behind the carnassial tips
pair("M500,524 C478,530 452,532 424,524", "Grimace", fill=NONE,
     stroke=INK, strokeWidth=6, cap="round")
pair("M424,524 C414,526 406,530 400,538", "Grimace corner", fill=NONE,
     stroke=INK, strokeWidth=4.5, cap="round")
d.path("M424,528 C452,536 548,536 576,528 C560,548 530,556 500,556 "
       "C470,556 440,548 424,528 Z", "Mouth dark", fill="#200E08",
       opacity=85, stroke=NONE)
# carnassial tips — the tools in the grin
pair("M430,528 C428,540 432,550 440,554 C446,546 446,534 440,526 Z",
     "Carnassial", fill="#F2EAD2", stroke=INK, strokeWidth=2.5)
pair("M452,532 C452,540 454,546 458,550 C462,544 462,536 460,530 Z",
     "Incisor hint", fill="#E8E0CC", stroke=NONE, opacity=90)
# lower lip + chin in moon shadow
d.path("M452,562 C478,574 522,574 548,562", "Lower lip", fill=NONE,
       stroke="#4E4234", strokeWidth=7, opacity=60, cap="round")
# whisker stubs — hyenas keep them short
for j, (x1, y1, x2, y2) in enumerate([(430, 500, 372, 492), (432, 510, 376, 512)]):
    pair(f"M{x1},{y1} Q{(x1 + x2) / 2},{min(y1, y2) - 4} {x2},{y2}",
         f"Whisker {j+1}", fill=NONE, stroke="#D8D0BC",
         strokeWidth=2.5, opacity=50, cap="round")
for j, (x, y) in enumerate([(442, 512), (454, 520), (446, 528)]):
    spot(x, y, 4, 4, f"Whisker dot L{j+1}", op=55)
    spot(1000 - x, y, 4, 4, f"Whisker dot R{j+1}", op=55)

# --- name -------------------------------------------------------------------------
d.text("SPOTTED HYENA", "Name", x=500, y=962, size=54, font="Virelai Sans",
       color="#C8D2E4", justify="center")

d.finish("spotted-hyena-V1R00")
