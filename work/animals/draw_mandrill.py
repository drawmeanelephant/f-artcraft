#!/usr/bin/env python3
"""Mandrill — field plate V1R00. The most colorful face in the monkey
house, and it knows it: chin up, direct stare under a heavy brow. The
flagship muzzle — vermillion stripe down the nose flanked by violet-blue
ridged swellings, golden beard framing the jaw, olive crown. Rainforest
plate, equatorial mood: emerald dusk, leaf fronds, dapple. Undergrowth
floor closes on the disc's own arc. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math, re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Mandrill — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#20180E"                    # warm dark ink, never pure black


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


BG_GRAD = lin(0, 0, 0, 1000, (0, "#101E12"), (1, "#040A06"))
PLATE_GRAD = rad((0, "#A8C8A0"), (0.5, "#5E8A62"), (1, "#2A4636"))
FUR_GRAD = rad((0, "#8A7A56"), (0.6, "#6B5E40"), (1, "#453B28"))
BEARD_GRAD = lin(0, 420, 0, 700, (0, "#D8B45C"), (0.55, "#B08A3C"), (1, "#6E5424"))
RIDGE_GRAD = lin(430, 400, 430, 600, (0, "#7E9CC8"), (0.5, "#5470B0"), (1, "#34487E"))
MUZZLE_RED = lin(0, 390, 0, 580, (0, "#D8482E"), (0.7, "#B02E20"), (1, "#7E1E14"))
FLOOR_GRAD = lin(0, 770, 0, 880, (0, "#3E5636"), (0.55, "#28381F"), (1, "#141E10"))

# --- backdrop + rainforest plate -------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=58, y=18, width=884, height=884, fill="#7EA87E", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#1E3226", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8EBD8", strokeWidth=3, opacity=38)

# equatorial light pooling high in the canopy
d.shape("ellipse", "Canopy light", x=310, y=120, width=340, height=200,
        fill="#F0E8B8", opacity=14, stroke=NONE)
# broad fronds leaning in from the upper corners, wholly inside the disc
for i, (cx, cy, ang, L, wd, col, op) in enumerate([
        (196, 210, 35, 200, 34, "#2E5238", 55), (270, 160, 55, 150, 26, "#3A6242", 45),
        (806, 215, 145, 200, 34, "#2E5238", 55), (736, 160, 125, 150, 26, "#3A6242", 45)]):
    t = math.radians(ang); c_, s_ = math.cos(t), math.sin(t)
    mid = (cx + c_ * L * 0.5, cy + s_ * L * 0.5)
    tip = (cx + c_ * L, cy + s_ * L)
    for p in [(cx, cy), mid, tip]:
        assert on_disc(*p, 8), (i, p)
    d.path(f"M{cx},{cy} "
           f"Q{mid[0] - s_ * wd:.0f},{mid[1] + c_ * wd:.0f} {tip[0]:.0f},{tip[1]:.0f} "
           f"Q{mid[0] + s_ * wd:.0f},{mid[1] - c_ * wd:.0f} {cx},{cy} Z",
           f"Frond {i+1}", fill=col, opacity=op, stroke=NONE)
    # midrib
    d.path(f"M{cx},{cy} L{tip[0]:.0f},{tip[1]:.0f}", f"Frond {i+1} rib",
           fill=NONE, stroke="#1E3226", strokeWidth=3, opacity=45, cap="round")
# drifting dapple
for i, (x, y, w) in enumerate([(350, 220, 18), (630, 190, 22), (240, 420, 16),
                               (780, 400, 18), (180, 560, 14), (830, 560, 16)]):
    assert on_disc(x, y, 16), i
    d.shape("ellipse", f"Dapple {i+1}", x=x - w / 2, y=y - w / 3,
            width=w, height=w * 0.66, fill="#F0E8B8", opacity=15, stroke=NONE)

# --- undergrowth floor, closing on the disc arc ------------------------------------
fy = 782
fl, fr = rim_x(fy, -1), rim_x(fy, 1)
d.path(f"M{fl:.1f},{fy} C320,768 420,786 500,780 C580,774 680,778 {fr:.1f},{fy} "
       f"A{PR},{PR} 0 0 1 {fl:.1f},{fy} Z", "Floor", fill=FLOOR_GRAD, stroke=NONE)
# seedling spears + fallen fruit
for i, (x, y) in enumerate([(268, 786), (332, 796), (668, 790), (728, 784)]):
    d.path(f"M{x},{y} C{x - 6},{y - 18} {x - 2},{y - 32} {x + 4},{y - 40} "
           f"M{x},{y} C{x + 8},{y - 16} {x + 10},{y - 28} {x + 6},{y - 38}",
           f"Seedling {i+1}", fill=NONE, stroke="#4E6E42", strokeWidth=3.5,
           opacity=65, cap="round")
d.shape("ellipse", "Fallen fruit", x=580, y=800, width=26, height=22,
        fill="#C88030", opacity=80, stroke="#5E4018", strokeWidth=3)
d.path("M592,800 L596,792", "Fruit stem", fill=NONE, stroke="#4E3818",
       strokeWidth=3, cap="round")

# --- shoulders: a dark wedge of chest, head does the talking -----------------------
d.path(smooth([(370, 620), (330, 665), (315, 730), (312, 770), (315, 782),
               (685, 782), (688, 770), (685, 730), (670, 665), (630, 620),
               (575, 645), (500, 656), (425, 645)]),
       "Shoulders", fill=FUR_GRAD, stroke=INK, strokeWidth=6)
for i, dd in enumerate(["M400,660 C396,690 398,720 404,748",
                        "M600,660 C604,690 602,720 596,748",
                        "M500,668 L500,752"]):
    d.path(dd, f"Chest fur {i+1}", fill=NONE, stroke="#3E3424",
           strokeWidth=5, opacity=45, cap="round")

# --- the golden beard mane framing the face -----------------------------------------
BEARD = smooth([(500, 640), (424, 620), (362, 580), (322, 520), (308, 452),
                (306, 400), (318, 352), (348, 318), (652, 318), (682, 352),
                (694, 400), (692, 452), (678, 520), (638, 580), (576, 620)])
d.path(BEARD, "Beard", fill=BEARD_GRAD, stroke=INK, strokeWidth=5)
# beard scallops — coarse hair tips along its lower rim
for i, (x0, y0, x1, y1, x2, y2) in enumerate([
        (330, 520, 344, 548, 318, 556), (322, 458, 338, 482, 310, 492),
        (356, 586, 376, 608, 350, 622), (420, 622, 444, 638, 424, 654),
        (500, 640, 524, 636, 512, 664), (580, 622, 560, 640, 588, 654),
        (644, 586, 624, 608, 652, 620), (678, 520, 656, 548, 684, 556),
        (692, 458, 664, 480, 692, 494)]):
    d.path(f"M{x0},{y0} Q{x1},{y1} {x2},{y2}", f"Beard tip {i+1}",
           fill=NONE, stroke="#8A6C2E", strokeWidth=5, opacity=65, cap="round")
# beard parting strokes — the mane falls in locks
for i, dd in enumerate(["M330,430 C350,480 372,530 400,570",
                        "M300,420 C324,474 350,524 384,568",
                        "M670,430 C650,480 628,530 600,570",
                        "M700,420 C676,474 650,524 616,568"]):
    d.path(dd, f"Beard lock {i+1}", fill=NONE, stroke="#7E6228",
           strokeWidth=6, opacity=40, cap="round")

# --- ears: small, dark, half-buried in the mane --------------------------------------
pair("M316,392 C302,376 302,352 320,342 C338,332 356,342 360,362 "
     "C346,362 332,372 328,388 C324,394 318,396 316,392 Z",
     "Ear", fill="#2E2418", stroke=INK, strokeWidth=4, opacity=90)

# --- head: olive crown over the flag --------------------------------------------------
HEAD = smooth([(500, 268), (580, 272), (644, 306), (672, 366), (668, 430),
               (640, 480), (592, 520), (548, 542), (500, 548), (452, 542),
               (408, 520), (360, 480), (332, 430), (328, 366), (356, 306),
               (420, 272)])
d.path(HEAD, "Head", fill=FUR_GRAD, stroke=INK, strokeWidth=7)
# crown fur strokes + a centre part
for i, dd in enumerate(["M500,282 C496,310 496,340 500,366",
                        "M440,290 C428,318 424,348 428,374",
                        "M560,290 C572,318 576,348 572,374",
                        "M390,310 C384,338 384,364 390,388",
                        "M610,310 C616,338 616,364 610,388"]):
    d.path(dd, f"Crown fur {i+1}", fill=NONE, stroke="#3E3424",
           strokeWidth=5, opacity=45, cap="round")
d.shape("ellipse", "Crown light", x=430, y=278, width=150, height=50,
        fill="#D8D0A8", opacity=18, stroke=NONE)

# --- the muzzle flag ------------------------------------------------------------------
# violet-blue ridged swellings flanking the red stripe
RIDGE = smooth([(452, 420), (436, 470), (432, 530), (440, 585), (452, 616),
                (466, 610), (472, 560), (476, 500), (474, 450), (466, 420)])
pair(RIDGE, "Muzzle ridge", fill=RIDGE_GRAD, stroke=INK, strokeWidth=4)
# ridge grooves — the corrugation that catches light
for j, (x0, y0, x1, y1) in enumerate([(446, 440, 442, 570), (454, 470, 452, 590),
                                      (460, 430, 462, 560)]):
    pair(f"M{x0},{y0} C{x0 - 2},{(y0 + y1) / 2} {x1 - 2},{(y0 + y1) / 2} {x1},{y1}",
         f"Ridge groove {j+1}", fill=NONE, stroke="#2A3C6E",
         strokeWidth=3.5, opacity=55, cap="round")
# ridge highlight down the outside face
pair("M444,430 C438,480 438,540 446,590", "Ridge light", fill=NONE,
     stroke="#A8C4E8", strokeWidth=4, opacity=40, cap="round")

# the vermillion stripe from brow to nose tip
d.path(smooth([(500, 390), (484, 400), (478, 448), (476, 500), (480, 540),
               (488, 566), (500, 576), (512, 566), (520, 540), (524, 500),
               (522, 448), (516, 400)]),
       "Nose stripe", fill=MUZZLE_RED, stroke=INK, strokeWidth=4)
d.path("M492,400 C486,450 484,505 488,548", "Stripe light", fill=NONE,
       stroke="#F08060", strokeWidth=4, opacity=50, cap="round")
# nose tip — broad red, nostrils like black wings
d.path("M474,540 C484,528 516,528 526,540 C532,556 524,570 500,572 "
       "C476,570 468,556 474,540 Z", "Nose tip", fill="#C23A26",
       stroke=INK, strokeWidth=4)
d.path("M478,548 C486,542 494,542 498,548 C494,556 484,556 478,548 Z",
       "Nostril L", fill="#1E0E08", stroke=NONE)
d.path("M522,548 C514,542 506,542 502,548 C506,556 516,556 522,548 Z",
       "Nostril R", fill="#1E0E08", stroke=NONE)
# red philtrum + the flat, knowing mouth
d.path("M500,572 L500,586", "Philtrum", fill=NONE, stroke="#7E1E14",
       strokeWidth=4, cap="round")
pair("M500,588 C486,592 470,592 456,588", "Mouth", fill=NONE,
     stroke=INK, strokeWidth=4.5, cap="round")
pair("M456,588 C450,590 446,594 444,598", "Mouth corner", fill=NONE,
     stroke=INK, strokeWidth=3.5, opacity=70, cap="round")
# red chin badge below the mouth — kept small so it reads as lip, not tongue
d.path("M486,600 C494,596 506,596 514,600 C510,610 504,613 500,613 "
       "C496,613 490,610 486,600 Z", "Chin badge", fill="#B02E20",
       opacity=70, stroke=NONE)

# --- eyes: deep-set amber under the brow shelf -----------------------------------------
# heavy brow shelf across both eyes
d.path("M400,382 C440,364 560,364 600,382 C596,398 560,406 500,406 "
       "C440,406 404,398 400,382 Z", "Brow shelf", fill="#3E3424",
       opacity=90, stroke=NONE)
EYE = smooth([(420, 420), (436, 408), (460, 406), (476, 416), (470, 432),
              (448, 438), (428, 432)])
pair(EYE, "Eye", fill=rad((0, "#D8A44E"), (0.65, "#9A7028"), (1, "#5E4612")),
     stroke=INK, strokeWidth=4.5)
d.shape("ellipse", "Pupil L", x=446, y=414, width=10, height=13, fill="#140C04", stroke=NONE)
d.shape("ellipse", "Pupil R", x=544, y=414, width=10, height=13, fill="#140C04", stroke=NONE)
d.shape("ellipse", "Glint L", x=449, y=416, width=4.5, height=4.5, fill="#FFFFFF", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=547, y=416, width=4.5, height=4.5, fill="#FFFFFF", opacity=90, stroke=NONE)
# under-eye shadow — the stare's weight
pair("M424,440 C442,448 464,446 478,436", "Under-eye", fill=NONE,
     stroke="#3E3424", strokeWidth=5, opacity=45, cap="round")

# --- name ---------------------------------------------------------------------------------
d.text("MANDRILL", "Name", x=500, y=962, size=60, font="Virelai Sans",
       color="#DEE8D0", justify="center")

d.finish("mandrill-V1R00")
