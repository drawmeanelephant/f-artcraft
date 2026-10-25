#!/usr/bin/env python3
"""Antonio Vivaldi — milestone card V1R00. The red priest: half-figure in a
black cassock, auburn hair instead of a powdered wig, violin under the chin
with the bow raised, a curled manuscript sheet standing on the floor chord.
Candlelit Venetian warmth. 1000x1000. House style: gradients + translucent
shading, never flat fills. Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Vivaldi — Milestone Card", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#221A12"                    # warm dark ink, never pure black


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


BG_GRAD = lin(0, 0, 0, 1000, (0, "#14171A"), (1, "#07090B"))
PLATE_GRAD = rad((0, "#B9BFA6"), (0.55, "#7C876B"), (1, "#3C4534"))
ROBE_GRAD = lin(360, 560, 640, 800, (0, "#3E372E"), (0.55, "#26201A"), (1, "#12100C"))
ROBE_DIM = lin(360, 560, 640, 800, (0, "#2A241E"), (1, "#0E0B08"))
SKIN_GRAD = rad((0, "#EFCDA4"), (0.6, "#D9AC82"), (1, "#A87A56"))
HAIR_GRAD = lin(430, 330, 560, 540, (0, "#C07838"), (0.55, "#8F4A20"), (1, "#572511"))
FLOOR_GRAD = lin(0, 745, 0, 880, (0, "#5C5A48"), (0.55, "#403E30"), (1, "#1E1D14"))
PAPER_GRAD = lin(300, 640, 450, 790, (0, "#F4EBD4"), (1, "#CBBD9C"))
VIOLIN_GRAD = lin(520, 480, 660, 570, (0, "#C8863E"), (0.55, "#9A5822"), (1, "#5E2E12"))

# --- backdrop + Venetian sage plate -------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#333D2A", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8EED6", strokeWidth=3, opacity=40)

# candlelit pooling upper-left + drifting warm haze
d.shape("ellipse", "Light pool", x=240, y=145, width=410, height=235,
        fill="#F0E6C0", opacity=13, stroke=NONE)
for i, (x, y, w) in enumerate([(340, 315, 90), (580, 240, 70), (715, 350, 80),
                               (260, 470, 60), (745, 495, 64), (470, 190, 55)]):
    assert on_disc(x, y, 20), i
    d.shape("ellipse", f"Haze {i+1}", x=x - w / 2, y=y - w / 5, width=w, height=w * 0.4,
            fill="#EEE8C8", opacity=11, stroke=NONE)

# --- floor chord, closing on the disc arc -------------------------------------------
fy = 790
fl, fr = rim_x(fy, -1), rim_x(fy, 1)
d.path(f"M{fl:.1f},{fy} C330,776 420,798 500,789 C580,780 670,786 {fr:.1f},{fy} "
       f"A{PR},{PR} 0 0 1 {fl:.1f},{fy} Z", "Floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{fl + 8:.0f},{fy} C330,776 420,798 500,789 C580,780 670,786 {fr - 8:.0f},{fy}",
       "Floor sheen", fill=NONE, stroke="#9AA088", strokeWidth=5, opacity=40, cap="round")

# soft shadow under the figure
d.shape("ellipse", "Figure shadow", x=330, y=758, width=390, height=30,
        fill="#0E120A", opacity=32, stroke=NONE)

# --- floor props: standing manuscript (curling corner) + candle ----------------------
# sheet stands tilted on the floor, its top-right corner curling over
d.path("M268,676 L404,662 L416,796 L280,802 Z", "Sheet", fill=PAPER_GRAD,
       stroke=INK, strokeWidth=3)
d.path("M404,662 C426,668 428,692 412,704 C418,688 414,672 404,662 Z",
       "Sheet curl", fill=lin(404, 662, 426, 702, (0, "#E4D6B4"), (1, "#A8987A")),
       stroke=INK, strokeWidth=2.5)
for row in range(3):
    y0 = 700 + row * 26
    for ln in range(5):
        yy = y0 + ln * 3.0
        d.path(f"M284,{yy} L394,{yy - 6}", f"Staff {row}-{ln}", fill=NONE,
               stroke="#6E5C40", strokeWidth=1.6, opacity=55, cap="round")
for i, (nx, ny) in enumerate([(306, 716), (338, 713), (368, 710), (318, 743),
                              (352, 740), (306, 768), (342, 765)]):
    d.shape("ellipse", f"Note {i+1}", x=nx, y=ny, width=7, height=5,
            fill="#4E3E28", opacity=75, stroke=NONE)

# candle — brass dish, cream stick, teardrop flame, warm glow (left edge)
d.shape("ellipse", "Candle dish", x=214, y=746, width=80, height=19,
        fill=lin(218, 744, 290, 762, (0, "#A8873E"), (1, "#5C4518")),
        stroke=INK, strokeWidth=3)
d.path("M250,748 C246,724 246,696 248,670 C248,662 260,662 261,670 "
       "C264,696 264,724 261,748 Z", "Candle", fill=lin(248, 666, 258, 748,
       (0, "#F6EDD2"), (1, "#C9B88E")), stroke=INK, strokeWidth=3)
d.path("M254,668 C254,660 255,654 256,650", "Wick", fill=NONE,
       stroke="#3A2C1A", strokeWidth=2.5, cap="round")
d.path("M256,650 C247,636 249,618 257,608 C266,619 267,637 258,650 Z", "Flame",
       fill=rad((0, "#FFF4C4"), (0.55, "#F2B94E"), (1, "#C96A1E")),
       stroke=NONE, opacity=95)
d.shape("ellipse", "Candle glow", x=192, y=566, width=136, height=136,
        fill=rad((0, "#F6D488"), (1, "#F6D488")), stroke=NONE, opacity=14)

# --- Vivaldi: half-figure, chin down on the violin ----------------------------------
# torso — black priest's cassock, seated, widening to the floor
d.path(smooth([(356, 606), (330, 660), (338, 726), (352, 788),
               (656, 788), (662, 716), (648, 648), (612, 602),
               (560, 572), (468, 566), (410, 582)]),
       "Cassock", fill=ROBE_GRAD, stroke=INK, strokeWidth=6)
# right-side shade so the torso turns
d.path(smooth([(564, 576), (612, 604), (646, 652), (658, 720),
               (650, 786), (564, 788), (560, 700), (552, 628)]),
       "Cassock shade", fill=ROBE_DIM, opacity=55, stroke=NONE)
# cassock front seam + buttons
d.path("M478,576 C504,620 518,694 522,782", "Cassock front", fill=NONE,
       stroke="#0C0906", strokeWidth=4, opacity=70, cap="round")
for i, yy in enumerate(range(640, 770, 30)):
    d.shape("ellipse", f"Button {i+1}", x=517, y=yy, width=9, height=9,
            fill="#171310", stroke="#4E463C", strokeWidth=2)
# white clerical collar band + two short tabs
d.path("M440,566 C460,578 500,580 522,568 L524,586 C502,600 458,598 438,584 Z",
       "Collar band", fill=lin(444, 566, 520, 596, (0, "#F6F0E0"), (1, "#CFC6AE")),
       stroke=INK, strokeWidth=3)
d.path("M466,592 L492,594 L490,622 L468,620 Z", "Tab L",
       fill="#F2ECDC", stroke=INK, strokeWidth=2.5)
d.path("M496,594 L518,590 L520,614 L498,620 Z", "Tab R",
       fill="#EAE2CE", stroke=INK, strokeWidth=2.5)

# neck — short, tucked behind the collar
d.path("M458,522 C458,538 456,552 452,566 C464,576 490,576 502,562 "
       "C498,548 496,534 496,520 Z", "Neck", fill=lin(456, 522, 498, 576,
       (0, "#E2BC94"), (1, "#B38660")), stroke=INK, strokeWidth=3.5)

# head — oval tilted a touch toward the violin (viewer's right), chin down
d.path(smooth([(424, 416), (421, 456), (426, 496), (444, 526),
               (468, 542), (494, 540), (516, 522), (529, 490),
               (531, 450), (523, 414), (503, 388), (476, 380),
               (448, 385)]),
       "Head", fill=SKIN_GRAD, stroke=INK, strokeWidth=5)
d.path("M428,470 C431,497 445,520 465,532 C444,524 429,501 426,476 Z",
       "Cheek shade", fill="#A87A56", opacity=45, stroke=NONE)

# auburn hair — his own, no wig: center-parted waves to the jaw, small
# curls on the forehead, a dark ribbon tying the back
d.path(smooth([(420, 432), (412, 392), (428, 352), (460, 330),
               (496, 324), (528, 336), (548, 366), (555, 402),
               (552, 436), (544, 452), (534, 440), (529, 412),
               (514, 392), (490, 384), (462, 388), (440, 404),
               (428, 430)]),
       "Hair crown", fill=HAIR_GRAD, stroke=INK, strokeWidth=5)
# forehead curl wave — the parted front lock
d.path("M436,408 C452,392 474,384 496,386 C478,392 464,402 456,414 "
       "C450,408 442,406 436,408 Z", "Front wave", fill="#C07838",
       stroke=INK, strokeWidth=2.5, opacity=90)
# side waves framing the face, ending at the jaw
for side, xa, xb in [(-1, 416, 430), (1, 540, 554)]:
    d.path(smooth([(xa, 420), (xa - 6 if side < 0 else xa + 6, 452),
                   (xa - 4 if side < 0 else xa + 4, 488),
                   (xa + 4 if side < 0 else xa - 4, 514),
                   (xb + 4 if side < 0 else xb - 4, 524),
                   (xb + 6 if side < 0 else xb - 6, 500),
                   (xb, 462), (xa + 8 if side < 0 else xa - 8, 428)]),
           f"Side wave {'L' if side < 0 else 'R'}", fill=HAIR_GRAD,
           stroke=INK, strokeWidth=4)
# loose lock tips — two small curls below each jaw corner
d.path("M428,516 C420,528 420,542 428,552 C434,544 436,530 434,518 Z",
       "Lock L", fill=HAIR_GRAD, stroke=INK, strokeWidth=3)
d.path("M548,512 C556,524 556,538 548,548 C542,540 540,526 542,514 Z",
       "Lock R", fill=HAIR_GRAD, stroke=INK, strokeWidth=3)
# hair sheen on the crown
d.path("M446,354 C470,338 506,336 528,352", "Hair sheen", fill=NONE,
       stroke="#DCA05C", strokeWidth=5, opacity=55, cap="round")
# dark ribbon at the nape (left side, clear of the violin)
d.path("M414,486 C404,494 398,508 400,522 C410,516 418,504 420,490 Z",
       "Hair tie", fill="#241812", stroke=INK, strokeWidth=3)

# face — longer nose than Mozart's, gaze down the fingerboard (right)
d.path("M438,438 C450,432 464,430 476,434", "Brow L", fill=NONE,
       stroke="#5E3C22", strokeWidth=4.5, opacity=75, cap="round")
d.path("M494,434 C506,430 518,430 528,434", "Brow R", fill=NONE,
       stroke="#5E3C22", strokeWidth=4.5, opacity=75, cap="round")
d.path("M438,454 C448,447 462,447 470,454 C466,464 452,466 443,461 Z",
       "Eye L", fill="#F6EFE2", stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Pupil L", x=450, y=450, width=9, height=10,
        fill="#2E1C10", stroke=NONE)
d.path("M494,452 C504,446 516,446 523,452 C519,462 507,464 499,459 Z",
       "Eye R", fill="#F6EFE2", stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Pupil R", x=504, y=448, width=9, height=10,
        fill="#2E1C10", stroke=NONE)
# nose — longer, straighter
d.path("M482,456 C479,472 475,488 472,498 C477,504 486,504 490,499",
       "Nose", fill=NONE, stroke="#8A6242", strokeWidth=3.5,
       opacity=80, cap="round")
d.path("M456,514 C466,519 480,521 492,517", "Mouth", fill=NONE,
       stroke="#8A4A38", strokeWidth=4, opacity=85, cap="round")
d.path("M460,518 C468,528 482,530 490,522", "Lower lip", fill=NONE,
       stroke="#A87A56", strokeWidth=2.5, opacity=50, cap="round")
d.shape("ellipse", "Blush L", x=432, y=488, width=22, height=12,
        fill="#C97A5C", opacity=20, stroke=NONE)
d.shape("ellipse", "Blush R", x=504, y=484, width=20, height=11,
        fill="#C97A5C", opacity=18, stroke=NONE)

# left arm (viewer's right) — slim sleeve rising behind the violin to the neck
d.path(smooth([(636, 640), (660, 612), (676, 570), (676, 528),
               (668, 504), (652, 500), (640, 516), (630, 556),
               (624, 598), (624, 632)]),
       "Sleeve R", fill=ROBE_GRAD, stroke=INK, strokeWidth=5)
d.path("M648,504 C660,496 674,496 684,504", "Cuff R", fill=NONE,
       stroke="#F2ECDC", strokeWidth=7, opacity=85, cap="round")

# --- the violin under the chin -------------------------------------------------------
# body axis runs tailpiece (492,600) → scroll (756,470); a full-size body on
# the shoulder, neck rising right. Lower bout tucks under the jaw.
d.path(smooth([(492, 596), (506, 568), (538, 550), (578, 548),
               (604, 560), (610, 580), (604, 602), (578, 616),
               (544, 620), (512, 612)]),
       "Violin lower bout", fill=VIOLIN_GRAD, stroke=INK, strokeWidth=4.5)
d.path(smooth([(590, 552), (610, 528), (642, 518), (672, 520),
               (690, 536), (690, 560), (670, 574), (642, 574),
               (614, 570), (596, 564)]),
       "Violin upper bout", fill=VIOLIN_GRAD, stroke=INK, strokeWidth=4.5)
# waist shadow where the bouts pinch
d.path("M584,556 C598,550 612,550 624,556", "Waist shadow", fill=NONE,
       stroke="#6E3812", strokeWidth=3, opacity=60, cap="round")
# fingerboard — dark tapering strip over the upper bout to the neck
d.path("M632,540 L742,486 L750,498 L640,556 Z", "Fingerboard",
       fill="#1E1410", stroke=INK, strokeWidth=2.5)
# neck + pegbox + scroll circle at the far right
d.path("M738,482 L776,462 L786,476 L748,498 Z", "Violin neck",
       fill="#3A2412", stroke=INK, strokeWidth=2.5)
d.shape("ellipse", "Scroll", x=774, y=452, width=26, height=26,
        fill="#4E3018", stroke=INK, strokeWidth=3)
d.path("M781,466 C785,460 791,460 793,466 C791,472 785,472 781,468",
       "Scroll eye", fill=NONE, stroke="#C8863E", strokeWidth=2, cap="round")
# strings — two stylized runs along the axis, from scroll to tailpiece
d.path("M778,486 C730,506 660,536 524,584", "Strings A", fill=NONE,
       stroke="#E8DCC0", strokeWidth=3, opacity=85, cap="round")
d.path("M782,494 C734,514 664,544 530,590", "Strings B", fill=NONE,
       stroke="#CBBB9E", strokeWidth=3, opacity=70, cap="round")
# bridge + f-holes + tailpiece + chin rest under the jaw
d.path("M600,570 C605,561 614,557 623,559", "Bridge", fill=NONE,
       stroke="#D8A85E", strokeWidth=4, cap="round")
d.path("M556,560 C551,571 551,585 558,594", "f-hole L", fill=NONE,
       stroke="#20130A", strokeWidth=3.5, cap="round")
d.path("M592,548 C587,559 587,573 594,582", "f-hole R", fill=NONE,
       stroke="#20130A", strokeWidth=3.5, cap="round")
d.path("M492,592 C508,590 524,595 531,606 C522,616 504,615 495,606 Z",
       "Tailpiece", fill="#241812", stroke=INK, strokeWidth=2.5)
d.shape("ellipse", "Chin rest", x=478, y=578, width=30, height=18,
        fill="#1A100A", stroke=INK, strokeWidth=2.5)
# varnish sheen on the lower bout
d.path("M512,580 C532,566 560,562 582,568", "Violin sheen", fill=NONE,
       stroke="#ECB46A", strokeWidth=4, opacity=55, cap="round")

# fingering hand wrapped on the neck
d.path("M668,478 C682,470 698,474 704,486 C702,500 688,508 676,502 "
       "C668,494 664,486 668,478 Z", "Fingering hand", fill=SKIN_GRAD,
       stroke=INK, strokeWidth=3.5)
d.path("M676,486 C684,482 692,484 696,490", "Fingering knuckle", fill=NONE,
       stroke="#8A6242", strokeWidth=2.5, opacity=60, cap="round")

# right arm (viewer's left) — sleeve down to the bow hand
d.path(smooth([(370, 632), (390, 676), (414, 716), (442, 748),
               (466, 762), (480, 754), (474, 738), (450, 712),
               (424, 678), (402, 640)]),
       "Sleeve L", fill=ROBE_GRAD, stroke=INK, strokeWidth=5)
d.path("M462,742 C474,736 488,738 496,746", "Cuff L", fill=NONE,
       stroke="#F2ECDC", strokeWidth=7, opacity=85, cap="round")
# bow hand at the frog
d.path("M480,736 C494,730 508,736 510,748 C508,762 494,768 482,762 "
       "C474,754 473,744 480,736 Z", "Bow hand", fill=SKIN_GRAD,
       stroke=INK, strokeWidth=3.5)
# bow — one long tapering stick from the frog up across the strings
d.path("M498,738 L616,442 L623,447 L506,742 Z", "Bow stick",
       fill="#3A2C1A", stroke=INK, strokeWidth=2.5)
d.path("M500,742 C530,650 580,540 618,450", "Bow hair", fill=NONE,
       stroke="#E8DCC0", strokeWidth=3, opacity=85, cap="round")
d.path("M612,438 C620,432 628,434 630,442 C624,448 616,448 612,442 Z",
       "Bow tip", fill="#D8C8A8", stroke=INK, strokeWidth=2.5)

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#2E3624", strokeWidth=6)

# --- captions -------------------------------------------------------------------
d.text("VIVALDI", "Name", x=500, y=934, size=56, font="Virelai Sans",
       color="#EEF0DC", justify="center")
LINE2, YEAR, SZ2, TRK = "FOUR SEASONS · 1725", "1725", 22, 280
r = d.text(LINE2, "Milestone", x=500, y=970, size=SZ2, font="Virelai Sans",
           color="#CDD4B4", justify="center")
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

d.finish("antonio-vivaldi-V1R00")
