#!/usr/bin/env python3
"""Jennifer Doudna — milestone card V1R00. In a modern lab behind a steel
bench, holding a stylized double-helix segment up beside her face — a
clean break mid-strand where the edit lands, marked only by two
abstracted chevron ticks and a cool glow. Never literal cutlery. Dark
blazer over a light blouse, shoulder-length blonde hair, warm open
smile. Microfuge rack and a pipette sit dead-dark on the bench; a
ghosted sequence trace floats upper-right. Figure crops behind the
bench band closed on the disc's own arc. 1000x1000. House style:
gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Jennifer Doudna — Milestone Card", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#1E150F"                    # warm dark ink, never pure black
SS3 = "Source Sans 3"              # Virelai Sans has no digit glyphs


def _stops(*pairs):
    out = []
    for p in pairs:
        s = {"offset": p[0], "color": p[1]}
        if len(p) > 2:
            s["opacity"] = p[2]
        out.append(s)
    return out


def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": _stops(*stops)}}


def rad(*stops):
    return {"gradient": {"kind": "radial", "stops": _stops(*stops)}}


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


BG_GRAD = lin(0, 0, 0, 1000, (0, "#10161A"), (1, "#040608"))
PLATE_GRAD = rad((0, "#5E7E84"), (0.5, "#384E56"), (1, "#182228"))
SKIN_GRAD = lin(440, 300, 540, 560, (0, "#EACCA8"), (0.55, "#C8A686"), (1, "#967259"))
SKIN_DIM = lin(440, 300, 540, 560, (0, "#C6A686"), (1, "#866550"))
HAIR_GRAD = lin(430, 230, 575, 510, (0, "#C8A86E"), (0.5, "#9A7A4C"), (1, "#5E4426"))
BLAZER_GRAD = lin(380, 500, 620, 810, (0, "#3E4A5E"), (0.5, "#252C3C"), (1, "#10141C"))
BLAZER_DIM = lin(380, 500, 620, 810, (0, "#323C4E"), (1, "#0C1018"))
BLOUSE_GRAD = lin(470, 494, 530, 600, (0, "#DDD6C2"), (1, "#8E8672"))
BENCH_GRAD = lin(0, 792, 0, 880, (0, "#3A4048"), (0.55, "#20252C"), (1, "#0C0E12"))
STRAND_A = "#8FE0DA"
STRAND_B = "#4FA8A4"
GLOW = "#9FE8E0"

# --- backdrop + cool modern plate ------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#26333A", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D2E2E2", strokeWidth=3, opacity=32)

# cool light pooling upper-left
d.shape("ellipse", "Light pool", x=245, y=140, width=390, height=225,
        fill="#DDEAE6", opacity=11, stroke=NONE)
# drifting lab air — clear of the face zone
for i, (x, y, w) in enumerate([(290, 200, 70), (720, 300, 76), (255, 490, 62),
                               (745, 520, 68), (650, 620, 58)]):
    assert on_disc(x, y, 18), i
    d.shape("ellipse", f"Mist {i+1}", x=x - w / 2, y=y - w / 5, width=w,
            height=w * 0.4, fill="#D8E8E4", opacity=9, stroke=NONE)

# ghosted sequence trace upper-right — a chromatogram whisper
r = d.text("A T G C G T A", "Sequence", x=668, y=196, size=17, font=SS3,
           color="#D2E2E2", justify="center")
d.cmd("object.setProps", "Sequence fade", id=r["id"], opacity=15)
d.path("M610,242 C630,240 636,216 650,214 C664,212 668,238 684,240 "
       "C700,242 706,222 720,222 C734,222 740,240 756,240",
       "Chromatogram", fill=NONE, stroke="#D2E2E2", strokeWidth=3,
       opacity=14, cap="round")

# --- the blazer figure, cropped by the bench band later ----------------------------------
d.path(smooth([(378, 810), (384, 700), (380, 616), (374, 552), (392, 505),
               (446, 492), (554, 492), (608, 505), (626, 552), (620, 616),
               (616, 700), (622, 810)], k=0.9), "Blazer",
       fill=BLAZER_GRAD, stroke=INK, strokeWidth=5)
for i, dd in enumerate([
        "M424,560 C418,630 416,700 420,770",
        "M576,560 C582,630 584,700 580,770"]):
    d.path(dd, f"Blazer fold {i+1}", fill=NONE, stroke="#0C1018",
           strokeWidth=4, opacity=40, cap="round")
d.path("M400,514 C440,498 560,498 600,514", "Shoulder sheen", fill=NONE,
       stroke="#6E7E96", strokeWidth=5, opacity=32, cap="round")

# right sleeve — long, running down to the wrist at the bench
d.path(smooth([(608, 505), (634, 540), (650, 590), (660, 654), (662, 722),
               (658, 768), (638, 770), (632, 700), (626, 628), (618, 560),
               (598, 552)], k=0.9), "Sleeve R",
       fill=BLAZER_DIM, stroke=INK, strokeWidth=4)
# left sleeve — bent, forearm rising to hold the helix
d.path(smooth([(392, 505), (368, 478), (344, 460), (328, 456), (320, 468),
               (330, 486), (358, 508), (384, 522)], k=0.9), "Sleeve L",
       fill=BLAZER_GRAD, stroke=INK, strokeWidth=4)
# forearm sleeve to the wrist
d.path(smooth([(324, 472), (312, 496), (306, 522), (310, 542), (324, 548),
               (336, 534), (342, 508), (344, 484)], k=0.9),
       "Forearm sleeve", fill=BLAZER_DIM, stroke=INK, strokeWidth=3.5)

# neck + blouse under the blazer
d.path("M484,448 L484,502 C492,509 508,509 516,502 L516,448 Z", "Neck",
       fill=SKIN_DIM, stroke=INK, strokeWidth=3.5)
d.path("M470,494 L530,494 L500,598 Z", "Blouse",
       fill=BLOUSE_GRAD, stroke=INK, strokeWidth=3.5)
# collar band + slim lapel edges hugging the V
d.path(smooth([(456, 498), (478, 488), (522, 488), (544, 498), (538, 516),
               (500, 508), (462, 516)], k=0.9), "Collar band",
       fill=lin(456, 488, 544, 516, (0, "#56648A"), (1, "#2A3140")),
       stroke=INK, strokeWidth=3.5)
d.path("M470,496 L496,580", "Lapel edge L", fill=NONE, stroke="#0C1018",
       strokeWidth=3.5, opacity=55, cap="round")
d.path("M530,496 L504,580", "Lapel edge R", fill=NONE, stroke="#0C1018",
       strokeWidth=3.5, opacity=55, cap="round")

# --- the bench — steel band closing on the disc's own arc --------------------------------
fy = 795
fl, fr = rim_x(fy, -1), rim_x(fy, 1)
d.path(f"M{fl:.1f},{fy} C350,780 650,782 {fr:.1f},{fy} "
       f"A{PR},{PR} 0 0 1 {fl:.1f},{fy} Z", "Bench", fill=BENCH_GRAD,
       stroke=NONE)
d.path(f"M{fl + 8:.0f},{fy} C350,780 650,782 {fr - 8:.0f},{fy}",
       "Bench crest", fill=NONE, stroke="#5E7280", strokeWidth=5,
       opacity=40, cap="round")

# right hand resting on the bench edge
d.path(smooth([(656, 788), (658, 774), (666, 766), (684, 766), (694, 774),
               (692, 788), (676, 794)], k=0.9), "Hand bench",
       fill=SKIN_DIM, stroke=INK, strokeWidth=3.5)
for i, xx in enumerate([664, 672, 680]):
    d.path(f"M{xx},770 L{xx + 1},786", f"Rest finger {i+1}", fill=NONE,
           stroke="#8A6248", strokeWidth=2.5, opacity=65, cap="round")

# dead-dark props — a micropipette left, a microfuge rack right
assert on_disc(300, 760, 8)
d.path("M296,724 L312,724 L312,760 L318,772 L318,792 L290,792 L290,772 "
       "L296,760 Z", "Pipette", fill="#181C22", stroke=INK, strokeWidth=3.5)
d.path("M298,714 L310,714 L310,724 L298,724 Z", "Pipette button",
       fill="#242A34", stroke=INK, strokeWidth=2.5)
assert on_disc(676, 766, 8)
d.path("M640,762 L706,762 L702,792 L644,792 Z", "Tube rack",
       fill="#181C22", stroke=INK, strokeWidth=3.5)
for i, (x, cap) in enumerate([(652, "#6EC8C0"), (664, "#D8A862"),
                              (676, "#C87E8A"), (688, "#7FA8D8"),
                              (700, "#9EC87E")]):
    d.path(f"M{x - 4},742 L{x + 4},742 L{x + 4},762 L{x - 4},762 Z",
           f"Tube {i+1}", fill="#242A34", stroke=INK, strokeWidth=2.5)
    d.shape("ellipse", f"Tube cap {i+1}", x=x - 4.5, y=736, width=9,
            height=7, fill=cap, opacity=75, stroke=NONE)

# --- the helix — held up beside the face, broken mid-strand -------------------------------
HX, AMP, PER = 363, 21, 128


def helix_pts(y0, y1, phase):
    return [(HX + AMP * math.sin(phase + 2 * math.pi * y / PER), y)
            for y in range(y0, y1 + 1, 9)]


# soft glow on the edit site
d.shape("ellipse", "Edit glow", x=318, y=386, width=92, height=92,
        fill=rad((0, GLOW, 32), (1, GLOW, 0)), stroke=NONE)
# backbones — two sine strands, split at the break (y 412..446)
for i, (y0, y1, ph, col) in enumerate([
        (296, 414, 0, STRAND_A), (296, 414, math.pi, STRAND_B),
        (446, 560, 0, STRAND_A), (446, 560, math.pi, STRAND_B)]):
    d.path(smooth(helix_pts(y0, y1, ph), closed=False), f"Strand {i+1}",
           fill=NONE, stroke=col, strokeWidth=5, opacity=95, cap="round")
# rungs between the strands, alternating base-pair tones
for i, yy in enumerate(range(310, 551, 30)):
    if 412 < yy < 446:
        continue                      # the cut — no rung across the gap
    x1 = HX + AMP * math.sin(2 * math.pi * yy / PER)
    x2 = HX - AMP * math.sin(2 * math.pi * yy / PER)
    if abs(x1 - x2) < 10:
        continue                      # crossover — strands touch
    col = "#7FC8A8" if i % 2 else "#C8A87E"
    d.path(f"M{x1:.0f},{yy} L{x2:.0f},{yy}", f"Rung {i+1}", fill=NONE,
           stroke=col, strokeWidth=4, opacity=85, cap="round")
# the cut: blunt strand ends get tiny caps, two chevron ticks mark the site
for sgn, col in [(1, STRAND_A), (-1, STRAND_B)]:
    d.shape("ellipse", "Cut end top", x=HX + sgn * 6 - 3, y=408, width=7,
            height=7, fill=col, stroke=NONE)
    d.shape("ellipse", "Cut end bot", x=HX - sgn * 6 - 3, y=440, width=7,
            height=7, fill=col, stroke=NONE)
d.path("M394,410 L406,426 L394,442", "Chevron cut", fill=NONE,
       stroke=GLOW, strokeWidth=4, opacity=75, cap="round")
d.path("M332,442 L320,426 L332,410", "Chevron guide", fill=NONE,
       stroke=GLOW, strokeWidth=4, opacity=55, cap="round")
d.path("M355,388 L355,380 M367,388 L367,380", "Guide ticks", fill=NONE,
       stroke=GLOW, strokeWidth=3, opacity=40, cap="round")

# left hand gripping the helix foot
d.path(smooth([(322, 566), (316, 550), (324, 536), (338, 534), (348, 544),
               (348, 560), (340, 570), (328, 570)], k=0.9), "Hand helix",
       fill=SKIN_GRAD, stroke=INK, strokeWidth=3.5)
for i, xx in enumerate([326, 335]):
    d.path(f"M{xx},548 C{xx + 1},555 {xx + 1},561 {xx},566",
           f"Helix finger {i+1}", fill=NONE, stroke="#8A6248",
           strokeWidth=2.5, opacity=70, cap="round")

# --- head -------------------------------------------------------------------------------
# shoulder-length straight blonde hair, side part
d.path(smooth([(432, 508), (420, 408), (422, 308), (438, 258), (475, 234),
               (522, 234), (556, 256), (574, 300), (578, 404), (568, 508),
               (550, 500), (552, 400), (448, 400), (450, 500)], k=0.9),
       "Hair mass", fill=HAIR_GRAD, stroke=INK, strokeWidth=4)
# face — oval, open
d.path(smooth([(500, 296), (546, 314), (554, 368), (540, 420), (500, 452),
               (460, 420), (446, 368), (454, 314)], k=0.85), "Face",
       fill=SKIN_GRAD, stroke=INK, strokeWidth=4)
# side-parted hairline sweep
d.path("M452,338 C458,302 478,286 502,284 C526,284 544,302 550,336 "
       "C538,308 518,296 498,298 C478,300 462,316 452,338 Z",
       "Hairline", fill=HAIR_GRAD, stroke=NONE)
for i, dd in enumerate(["M470,296 C458,306 450,320 446,334",
                        "M508,290 C524,296 538,308 546,324",
                        "M444,360 C442,400 444,450 448,492",
                        "M556,360 C558,400 556,450 552,492"]):
    d.path(dd, f"Hair strand {i+1}", fill=NONE, stroke="#8A6E48",
           strokeWidth=3, opacity=45, cap="round")
# soft cheek shades
d.path("M456,398 C460,416 468,430 480,438", "Cheek shade L", fill=NONE,
       stroke="#B0805E", strokeWidth=5, opacity=25, cap="round")
d.path("M544,398 C540,416 532,430 520,438", "Cheek shade R", fill=NONE,
       stroke="#B0805E", strokeWidth=5, opacity=25, cap="round")

# blonde brows — light, level
d.path("M458,352 C468,347 482,347 490,352", "Brow L", fill=NONE,
       stroke="#8A6E48", strokeWidth=4, opacity=70, cap="round")
d.path("M510,352 C518,347 532,347 542,352", "Brow R", fill=NONE,
       stroke="#8A6E48", strokeWidth=4, opacity=70, cap="round")
# eyes — no glasses, direct
d.path("M460,368 C467,361 481,361 488,368 C481,375 467,375 460,368 Z",
       "Eye L", fill="#EFE4D0", stroke=INK, strokeWidth=3)
d.path("M512,368 C519,361 533,361 540,368 C533,375 519,375 512,368 Z",
       "Eye R", fill="#EFE4D0", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Iris L", x=470, y=363, width=10, height=11,
        fill="#2E3A4A", stroke=NONE)
d.shape("ellipse", "Iris R", x=520, y=363, width=10, height=11,
        fill="#2E3A4A", stroke=NONE)
d.shape("ellipse", "Glint L", x=472.5, y=365, width=3, height=3,
        fill="#FFF4DC", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=522.5, y=365, width=3, height=3,
        fill="#FFF4DC", opacity=90, stroke=NONE)
# nose + the open friendly smile
d.path("M503,382 C506,395 506,407 500,414", "Nose shade", fill=NONE,
       stroke="#B0805E", strokeWidth=3.5, opacity=45, cap="round")
d.path("M493,415 C498,418 505,418 510,415", "Nose base", fill=NONE,
       stroke="#9A6248", strokeWidth=3, opacity=55, cap="round")
d.path("M472,426 C486,437 514,437 528,425", "Mouth", fill=NONE,
       stroke="#7A4436", strokeWidth=4.5, opacity=85, cap="round")
d.path("M482,437 C492,441 508,441 518,437", "Lip shade", fill=NONE,
       stroke="#9A6248", strokeWidth=3, opacity=40, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#202C33", strokeWidth=6)

# --- captions ----------------------------------------------------------------------------
d.text("JENNIFER DOUDNA", "Name", x=500, y=934, size=56,
       font="Virelai Sans", color="#E4ECEC", justify="center")
LINE2, SZ2, TRK = "CRISPR · 2012", 22, 560
r = d.text(LINE2, "Milestone", x=500, y=970, size=SZ2, font=SS3,
           color="#BCC8C8", justify="center")
d.cmd("text.setStyle", "Milestone tracking", id=r["id"], tracking=TRK)

b = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("milestone bounds", {k: round(v) for k, v in b.items()})
nearest = (min(max(PCX, b["x"]), b["x"] + b["width"]),
           min(max(PCY, b["y"]), b["y"] + b["height"]))
clear = math.hypot(nearest[0] - PCX, nearest[1] - PCY) - (PR + 3)
print("clears rim by %.1f" % clear)
assert clear > 0 and b["width"] <= 760 and b["x"] >= 10 and b["x"] + b["width"] <= 990, b

d.finish("jennifer-doudna-V1R00")
