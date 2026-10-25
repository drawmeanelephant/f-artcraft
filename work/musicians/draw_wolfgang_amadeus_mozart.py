#!/usr/bin/env python3
"""Wolfgang Amadeus Mozart — milestone card V1R00. Half-figure at a writing
desk: boyish young face under a powdered wig, red coat, quill held over a
manuscript sheet, candlelit warmth. Desk floor closing on the disc's arc.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Mozart — Milestone Card", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#241A12"                    # warm dark ink, never pure black


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


def find(o, oid):
    if isinstance(o, dict):
        if o.get("id") == oid and "bounds" in o: return o
        o = list(o.values())
    if isinstance(o, list):
        for v in o:
            hit = find(v, oid)
            if hit: return hit


BG_GRAD = lin(0, 0, 0, 1000, (0, "#181310"), (1, "#090706"))
PLATE_GRAD = rad((0, "#C2A878"), (0.55, "#8A6F48"), (1, "#4A3B24"))
COAT_GRAD = lin(360, 560, 620, 800, (0, "#A8402E"), (0.55, "#7E2A20"), (1, "#4E1810"))
COAT_DIM = lin(360, 560, 620, 800, (0, "#7E2E22"), (1, "#421410"))
SKIN_GRAD = rad((0, "#F2D2AC"), (0.6, "#DDB48C"), (1, "#B0805C"))
WIG_GRAD = lin(400, 340, 560, 520, (0, "#EFE7D6"), (0.55, "#CFC3AC"), (1, "#9C8E74"))
FLOOR_GRAD = lin(0, 745, 0, 880, (0, "#6B5236"), (0.55, "#4A3823"), (1, "#241A10"))
PAPER_GRAD = lin(560, 720, 720, 800, (0, "#F4EBD4"), (1, "#CBBD9C"))

# --- backdrop + candlelit plate ---------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#3E3018", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F0E4C4", strokeWidth=3, opacity=40)

# candlelit pooling upper-left + drifting warm haze
d.shape("ellipse", "Light pool", x=235, y=140, width=420, height=240,
        fill="#F4E2B4", opacity=14, stroke=NONE)
for i, (x, y, w) in enumerate([(330, 320, 90), (585, 240, 70), (720, 350, 80),
                               (255, 470, 60), (745, 490, 64), (465, 190, 55)]):
    assert on_disc(x, y, 20), i
    d.shape("ellipse", f"Haze {i+1}", x=x - w / 2, y=y - w / 5, width=w, height=w * 0.4,
            fill="#F2E4BC", opacity=11, stroke=NONE)

# --- desk floor, closing on the disc arc ------------------------------------------
fy = 790
fl, fr = rim_x(fy, -1), rim_x(fy, 1)
d.path(f"M{fl:.1f},{fy} C330,776 420,798 500,789 C580,780 670,786 {fr:.1f},{fy} "
       f"A{PR},{PR} 0 0 1 {fl:.1f},{fy} Z", "Desk", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{fl + 8:.0f},{fy} C330,776 420,798 500,789 C580,780 670,786 {fr - 8:.0f},{fy}",
       "Desk sheen", fill=NONE, stroke="#A8895C", strokeWidth=5, opacity=42, cap="round")

# soft shadow under the figure
d.shape("ellipse", "Figure shadow", x=330, y=760, width=380, height=30,
        fill="#120C06", opacity=32, stroke=NONE)

# --- desk props: manuscript sheet, inkwell, candle --------------------------------
# manuscript — a tilted sheet with two staff systems and scattered notes
ms = [(566, 742), (754, 724), (770, 766), (584, 796)]
for cx, cy in ms: assert on_disc(cx, cy, 6), (cx, cy)
d.path("M%.0f,%.0f L%.0f,%.0f L%.0f,%.0f L%.0f,%.0f Z" % tuple(sum(ms, ())),
       "Manuscript", fill=PAPER_GRAD, stroke=INK, strokeWidth=3)
for row in range(2):
    y0 = 750 + row * 20
    for ln in range(5):
        yy = y0 + ln * 3.0
        x0 = 596 + (yy - 750) * 0.35
        x1 = 742 - (yy - 750) * 0.30
        d.path(f"M{x0:.0f},{yy:.0f} L{x1:.0f},{yy - 9:.0f}",
               f"Staff {row}-{ln}", fill=NONE, stroke="#6E5C40", strokeWidth=1.6,
               opacity=55, cap="round")
for i, (nx, ny) in enumerate([(630, 752), (668, 749), (706, 746), (620, 773),
                              (660, 770), (700, 767)]):
    d.shape("ellipse", f"Note {i+1}", x=nx, y=ny, width=7, height=5,
            fill="#4E3E28", opacity=75, stroke=NONE)
# inkwell — small dark pot
d.shape("ellipse", "Inkwell", x=512, y=742, width=34, height=22,
        fill=rad((0, "#4E4234"), (1, "#1C140C")), stroke=INK, strokeWidth=3)
d.shape("ellipse", "Ink", x=520, y=744, width=18, height=9, fill="#0E0A06", stroke=NONE)

# candle — brass dish, cream stick, teardrop flame, warm glow
d.shape("ellipse", "Candle dish", x=256, y=742, width=84, height=20,
        fill=lin(260, 740, 336, 760, (0, "#A8873E"), (1, "#5C4518")),
        stroke=INK, strokeWidth=3)
d.path("M292,744 C288,720 288,690 290,664 C290,656 302,656 303,664 "
       "C306,690 306,720 303,744 Z", "Candle", fill=lin(290, 660, 300, 744,
       (0, "#F6EDD2"), (1, "#C9B88E")), stroke=INK, strokeWidth=3)
d.path("M296,664 C296,656 297,650 298,646", "Wick", fill=NONE,
       stroke="#3A2C1A", strokeWidth=2.5, cap="round")
d.path("M298,646 C289,632 291,614 299,604 C308,615 309,633 300,646 Z", "Flame",
       fill=rad((0, "#FFF4C4"), (0.55, "#F2B94E"), (1, "#C96A1E")),
       stroke=NONE, opacity=95)
d.shape("ellipse", "Candle glow", x=232, y=560, width=140, height=140,
        fill=rad((0, "#F6D488"), (1, "#F6D488")), stroke=NONE, opacity=14)
assert on_disc(302, 700, 30)

# --- Mozart: half-figure, three-quarter toward the desk ------------------------------
# torso — red court coat, seated, widening to the desk line
d.path(smooth([(356, 606), (330, 660), (338, 726), (352, 788),
               (648, 788), (656, 716), (642, 648), (606, 602),
               (556, 572), (468, 566), (410, 582)]),
       "Coat", fill=COAT_GRAD, stroke=INK, strokeWidth=6)
# right-side shade so the torso turns
d.path(smooth([(560, 576), (606, 604), (640, 652), (652, 720),
               (644, 786), (560, 788), (556, 700), (548, 628)]),
       "Coat shade", fill=COAT_DIM, opacity=55, stroke=NONE)
# coat front opening + brass buttons
d.path("M468,576 C500,616 520,690 528,782", "Coat front", fill=NONE,
       stroke="#3E140C", strokeWidth=4, opacity=70, cap="round")
for i, yy in enumerate(range(640, 770, 26)):
    d.shape("ellipse", f"Button {i+1}", x=518 + (yy - 640) * 0.02, y=yy,
            width=11, height=11,
            fill=rad((0, "#E8C878"), (1, "#7E5E22")), stroke=INK, strokeWidth=2)
# lace jabot at the throat
d.path(smooth([(452, 566), (470, 590), (478, 618), (470, 648),
               (452, 660), (434, 646), (428, 616), (432, 588)]),
       "Jabot", fill=lin(440, 570, 470, 660, (0, "#F6EFDC"), (1, "#CFC2A4")),
       stroke=INK, strokeWidth=3.5)
for i, yy in enumerate(range(588, 650, 16)):
    d.path(f"M436,{yy} C448,{yy + 6} 460,{yy + 6} 470,{yy}", f"Jabot ruffle {i+1}",
           fill=NONE, stroke="#A89C80", strokeWidth=2.5, opacity=60, cap="round")

# left forearm resting on the desk toward the manuscript
d.path(smooth([(372, 668), (400, 712), (436, 748), (472, 766),
               (504, 770), (512, 758), (500, 746), (466, 730),
               (430, 704), (400, 668)]),
       "Forearm", fill=COAT_GRAD, stroke=INK, strokeWidth=5)
# cuff + resting hand on the desk edge
d.path("M494,744 C508,742 520,750 520,762 C516,774 500,778 488,772 "
       "C480,762 482,750 494,744 Z", "Resting hand", fill=SKIN_GRAD,
       stroke=INK, strokeWidth=3.5)
d.path("M486,738 C496,736 506,740 512,746", "Cuff", fill=NONE,
       stroke="#F6EFDC", strokeWidth=7, opacity=90, cap="round")

# right upper arm reaching to the quill — sleeve from shoulder to raised hand
d.path(smooth([(614, 622), (648, 656), (666, 694), (670, 724),
               (658, 744), (636, 742), (624, 716), (612, 682),
               (600, 650), (598, 630)]),
       "Sleeve", fill=COAT_GRAD, stroke=INK, strokeWidth=5)
d.path("M632,712 C646,706 660,710 666,720", "Sleeve cuff", fill=NONE,
       stroke="#F6EFDC", strokeWidth=8, opacity=90, cap="round")
# writing hand — one clean mitten closed on the quill shaft
d.path("M648,712 C662,706 676,712 678,724 C676,738 662,744 650,738 "
       "C642,730 641,720 648,712 Z", "Writing hand", fill=SKIN_GRAD,
       stroke=INK, strokeWidth=3.5)
d.path("M652,722 C660,718 668,720 672,726", "Knuckle line", fill=NONE,
       stroke="#8A6242", strokeWidth=2.5, opacity=60, cap="round")

# quill — shaft up-right out of the hand, feather vane above
d.path("M664,722 C678,696 694,668 708,642", "Quill shaft", fill=NONE,
       stroke="#E8DCC0", strokeWidth=4, cap="round")
d.path(smooth([(702, 644), (714, 618), (728, 592), (736, 568),
               (744, 580), (738, 608), (726, 636), (712, 652)]),
       "Quill feather", fill=lin(708, 646, 742, 576, (0, "#F2EAD6"), (1, "#B8A888")),
       stroke=INK, strokeWidth=3)
d.path("M710,640 C720,618 730,596 738,576", "Quill rib", fill=NONE,
       stroke="#8A7A60", strokeWidth=2, opacity=70, cap="round")

# neck — short, mostly hidden behind the jabot
d.path("M460,524 C460,540 458,552 454,564 C466,574 490,574 502,562 "
       "C498,548 496,536 496,522 Z", "Neck", fill=lin(458, 524, 498, 574,
       (0, "#E4BE98"), (1, "#B98A64")), stroke=INK, strokeWidth=3.5)

# head — boyish oval, chin soft, turned a touch left
d.path(smooth([(424, 414), (420, 454), (424, 494), (441, 524),
               (464, 540), (490, 538), (512, 521), (525, 491),
               (529, 452), (522, 414), (503, 388), (476, 380),
               (448, 384)]),
       "Head", fill=SKIN_GRAD, stroke=INK, strokeWidth=5)
# cheek shading under the left cheekbone and along the jaw
d.path("M428,468 C430,495 443,518 462,531 C441,523 427,500 424,475 Z",
       "Cheek shade", fill="#B0805C", opacity=45, stroke=NONE)

# powdered wig — cap over the crown, side-roll stacks beside the cheeks,
# little tied queue at the nape
d.path(smooth([(418, 428), (416, 390), (432, 352), (462, 330),
               (494, 324), (524, 336), (544, 364), (552, 400),
               (548, 430), (538, 444), (530, 428), (524, 404),
               (508, 388), (482, 382), (456, 388), (434, 404),
               (426, 428)]),
       "Wig crown", fill=WIG_GRAD, stroke=INK, strokeWidth=5)
# hairline where the wig meets the forehead
d.path("M434,404 C456,388 482,382 508,388 C522,398 528,412 530,428",
       "Hairline", fill=NONE, stroke="#8A7C62", strokeWidth=3,
       opacity=55, cap="round")
# wig shading on the crown's right
d.path("M508,332 C532,346 548,372 550,400 C538,378 520,360 498,350 "
       "C502,344 505,338 508,332 Z", "Wig shade", fill="#9C8E74",
       opacity=38, stroke=NONE)
# side rolls — a short stack of horizontal curls hugging each cheek
for i, (yy, w, h) in enumerate([(452, 36, 21), (477, 38, 22), (502, 34, 20)]):
    d.shape("ellipse", f"Roll L{i+1}", x=392, y=yy - h / 2, width=w, height=h,
            fill=WIG_GRAD, stroke=INK, strokeWidth=3.5)
    d.path(f"M396,{yy - 4} C410,{yy - 8} 410,{yy + 8} 424,{yy + 4}",
           f"Roll curl L{i+1}", fill=NONE, stroke="#8A7C62", strokeWidth=2.5,
           opacity=60, cap="round")
for i, (yy, w, h) in enumerate([(452, 36, 21), (477, 38, 22), (502, 34, 20)]):
    d.shape("ellipse", f"Roll R{i+1}", x=536, y=yy - h / 2, width=w, height=h,
            fill=WIG_GRAD, stroke=INK, strokeWidth=3.5)
    d.path(f"M540,{yy - 4} C554,{yy - 8} 554,{yy + 8} 568,{yy + 4}",
           f"Roll curl R{i+1}", fill=NONE, stroke="#8A7C62", strokeWidth=2.5,
           opacity=60, cap="round")
# queue — little tied tail at the nape's right with a dark bow
d.path("M548,462 C564,472 574,490 574,512 C564,506 554,494 546,480 Z",
       "Queue", fill=WIG_GRAD, stroke=INK, strokeWidth=3.5)
d.path("M554,470 C562,464 570,464 576,470 C572,478 562,480 554,476 Z",
       "Queue bow", fill="#2E2018", stroke=INK, strokeWidth=2.5)

# face — young, soft, eyes down toward the manuscript (lower-left gaze)
# brows
d.path("M438,436 C450,430 464,428 476,432", "Brow L", fill=NONE,
       stroke="#6E5238", strokeWidth=4.5, opacity=75, cap="round")
d.path("M492,432 C504,428 516,428 526,432", "Brow R", fill=NONE,
       stroke="#6E5238", strokeWidth=4.5, opacity=75, cap="round")
# eyes — almond, lids lowered in concentration, gaze down-left
d.path("M438,452 C448,445 462,445 470,452 C466,462 452,464 443,459 Z",
       "Eye L", fill="#F6EFE2", stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Pupil L", x=445, y=450, width=9, height=10,
        fill="#2E1C10", stroke=NONE)
d.path("M492,450 C502,444 514,444 521,450 C517,460 505,462 497,457 Z",
       "Eye R", fill="#F6EFE2", stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Pupil R", x=498, y=448, width=9, height=10,
        fill="#2E1C10", stroke=NONE)
# nose — small, a touch upturned
d.path("M481,458 C477,471 473,484 471,492 C475,498 483,498 487,494",
       "Nose", fill=NONE, stroke="#8A6242", strokeWidth=3.5,
       opacity=80, cap="round")
# mouth — small boyish near-smile
d.path("M456,512 C466,518 480,520 492,516", "Mouth", fill=NONE,
       stroke="#8A4A38", strokeWidth=4, opacity=85, cap="round")
d.path("M460,516 C468,526 482,528 490,520", "Lower lip", fill=NONE,
       stroke="#B0805C", strokeWidth=2.5, opacity=50, cap="round")
# cheek blush, faint
d.shape("ellipse", "Blush L", x=432, y=486, width=22, height=12,
        fill="#C97A5C", opacity=22, stroke=NONE)
d.shape("ellipse", "Blush R", x=502, y=482, width=20, height=11,
        fill="#C97A5C", opacity=20, stroke=NONE)

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#38300F", strokeWidth=6)

# --- captions -------------------------------------------------------------------
d.text("MOZART", "Name", x=500, y=934, size=56, font="Virelai Sans",
       color="#F2E7CC", justify="center")
LINE2, YEAR, SZ2, TRK = "REQUIEM · 1791", "1791", 22, 280
r = d.text(LINE2, "Milestone", x=500, y=970, size=SZ2, font="Virelai Sans",
           color="#D8C49A", justify="center")
d.cmd("text.setStyle", "Milestone tracking", id=r["id"], tracking=TRK)
# Virelai Sans has no digit glyphs — set the year in Source Sans 3
off = len(LINE2[:LINE2.index(YEAR)].encode("utf-8"))
d.cmd("text.setRangeStyle", "Year digits font", id=r["id"], start=off,
      end=off + len(YEAR), font="Source Sans 3")

b = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("milestone bounds", {k: round(v) for k, v in b.items()})
nearest = (min(max(PCX, b["x"]), b["x"] + b["width"]),
           min(max(PCY, b["y"]), b["y"] + b["height"]))
clear = math.hypot(nearest[0] - PCX, nearest[1] - PCY) - (PR + 3)
print("clears rim by %.1f" % clear)
assert clear > 0 and b["width"] <= 760 and b["x"] >= 10 and b["x"] + b["width"] <= 990, b

d.finish("wolfgang-amadeus-mozart-V1R00")
