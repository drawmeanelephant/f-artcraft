#!/usr/bin/env python3
"""Standard poodle — milestone card V1R00. Continental clip in profile,
show stack facing left: clipped muzzle and barrel, the fluffy jacket over
neck and chest, ankle bracelets, hip rosette, tail pom and the long
proud neck under a rounded topknot. Apricot on a cool slate disc so the
clip contrast — smooth shaved curves vs the rosettes — is the drawing.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Standard Poodle — Milestone Card", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#241C18"                    # warm dark ink, never pure black


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


def puff(cx, cy, r, squash=1.0, seed=0.0):
    """A fluffy rosette — a lumpy blob, alternating radii read as curls."""
    pts = []
    for i in range(10):
        a = math.radians(seed + i * 36)
        rr = r * (1.0 if i % 2 == 0 else 0.80)
        pts.append((cx + rr * math.cos(a), cy + rr * squash * math.sin(a)))
    return smooth(pts)


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


BG_GRAD = lin(0, 0, 0, 1000, (0, "#131722"), (1, "#06080D"))
PLATE_GRAD = rad((0, "#A8B0BC"), (0.55, "#6E7886"), (1, "#3A434E"))
COAT_GRAD = lin(320, 380, 640, 780, (0, "#DCA45E"), (0.5, "#B87F3E"), (1, "#7C4C1E"))
CLIP_GRAD = lin(320, 380, 640, 780, (0, "#E9CB9C"), (0.6, "#D0A871"), (1, "#A87C46"))
DIM_GRAD = lin(320, 380, 640, 780, (0, "#9A6C36"), (1, "#54350F"))
DIMCLIP_GRAD = lin(320, 380, 640, 780, (0, "#B08A56"), (1, "#7A5A30"))
FLOOR_GRAD = lin(0, 750, 0, 880, (0, "#5C6074"), (0.55, "#40445A"), (1, "#21242F"))

# --- backdrop + slate plate ----------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#2C3540", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#DEE4EA", strokeWidth=3, opacity=38)

# cool light pooling upper-left
d.shape("ellipse", "Light pool", x=245, y=145, width=400, height=230,
        fill="#E4EAF4", opacity=13, stroke=NONE)
# thin mist lenses drifting across the disc
for i, (x, y, w) in enumerate([(330, 320, 90), (575, 240, 70), (715, 355, 80),
                               (255, 465, 60), (748, 485, 64), (455, 190, 55)]):
    assert on_disc(x, y, 20), i
    d.shape("ellipse", f"Mist {i+1}", x=x - w / 2, y=y - w / 5, width=w, height=w * 0.4,
            fill="#DCE2EA", opacity=12, stroke=NONE)

# --- show-ring floor, closing on the disc arc ----------------------------------
fy = 780
fl, fr = rim_x(fy, -1), rim_x(fy, 1)
d.path(f"M{fl:.1f},{fy} C300,768 400,790 500,780 C600,770 700,776 {fr:.1f},{fy} "
       f"A{PR},{PR} 0 0 1 {fl:.1f},{fy} Z", "Floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{fl + 8:.0f},{fy} C300,768 400,790 500,780 C600,770 700,776 {fr - 8:.0f},{fy}",
       "Floor crest", fill=NONE, stroke="#8A8EA6", strokeWidth=5, opacity=42, cap="round")
# clipped curls shed on the carpet — little comma tufts on the crest
for i, (x, y) in enumerate([(352, 806), (450, 828), (560, 834), (640, 816)]):
    assert on_disc(x, y + 6, 16), i
    d.path(f"M{x - 8:.0f},{y + 6} C{x - 10:.0f},{y - 4} {x + 2:.0f},{y - 8} "
           f"{x + 8:.0f},{y - 2} C{x + 12:.0f},{y + 3} {x + 4:.0f},{y + 9} {x - 2:.0f},{y + 8}",
           f"Curl {i+1}", fill=NONE, stroke="#8F7448", strokeWidth=4, opacity=62, cap="round")

# soft shadow the dog stands over
d.shape("ellipse", "Dog shadow", x=310, y=758, width=430, height=32,
        fill="#14101C", opacity=32, stroke=NONE)

# --- the poodle, continental clip, profile facing left -------------------------
# tail — docked short stem angled up off the rump, pom on the tip
d.path("M664,486 C678,462 690,440 700,420 C704,414 712,414 714,420 "
       "C708,444 696,468 682,490 C676,496 666,494 664,486 Z",
       "Tail stem", fill=CLIP_GRAD, stroke=INK, strokeWidth=4)
d.path(puff(716, 402, 34, seed=18), "Tail pom", fill=COAT_GRAD,
       stroke=INK, strokeWidth=4.5)

# far-side legs — dimmer, clipped shafts with small poms
# far front leg, set a little back
d.path(smooth([(452, 620), (458, 656), (456, 690), (448, 700), (436, 692),
               (436, 652), (440, 622)]),
       "Front leg far", fill=DIMCLIP_GRAD, stroke=INK, strokeWidth=4)
d.path(puff(446, 712, 26, seed=40), "Front pom far", fill=DIM_GRAD,
       stroke=INK, strokeWidth=4)
d.path("M428,730 C446,724 464,728 466,740 C462,754 448,762 432,758 "
       "C424,750 422,738 428,730 Z", "Front foot far", fill=DIMCLIP_GRAD,
       stroke=INK, strokeWidth=4)
# far hind leg, behind the near hind
d.path(smooth([(604, 622), (626, 660), (632, 696), (624, 706), (610, 698),
               (596, 664), (592, 636)]),
       "Hind leg far", fill=DIMCLIP_GRAD, stroke=INK, strokeWidth=4)
d.path(puff(626, 720, 26, seed=75), "Hind pom far", fill=DIM_GRAD,
       stroke=INK, strokeWidth=4)
d.path("M608,738 C626,732 644,736 646,748 C642,762 628,770 612,766 "
       "C604,758 602,746 608,738 Z", "Hind foot far", fill=DIMCLIP_GRAD,
       stroke=INK, strokeWidth=4)

# clipped barrel — the shaved rear body, loin to belly
d.path(smooth([(540, 500), (590, 478), (640, 474), (676, 490), (688, 522),
               (680, 566), (656, 606), (618, 636), (576, 646), (548, 626),
               (536, 566)]),
       "Barrel", fill=CLIP_GRAD, stroke=INK, strokeWidth=5.5)
# clip-line shadow where the jacket's fluff ends over the barrel
d.path("M540,506 C552,542 552,586 544,622 C534,588 534,542 540,506 Z",
       "Clip edge shade", fill="#8A6434", opacity=45, stroke=NONE)
# hip rosette — the round fluff patch riding the hip
d.path(puff(648, 522, 46, squash=0.92, seed=10), "Hip rosette",
       fill=COAT_GRAD, stroke=INK, strokeWidth=5)

# near hind leg — shaved shaft in two pieces so the hock reads as a bend,
# not a sausage: thigh to the stifle, gaskin back down to the ankle pom
d.path(smooth([(628, 590), (658, 618), (670, 652), (664, 684), (646, 694),
               (624, 684), (610, 650), (608, 616), (616, 596)]),
       "Hind thigh near", fill=CLIP_GRAD, stroke=INK, strokeWidth=5)
d.path(smooth([(646, 672), (662, 692), (656, 716), (638, 718), (626, 704),
               (630, 684)]),
       "Hind gaskin near", fill=CLIP_GRAD, stroke=INK, strokeWidth=4.5)
d.path(puff(654, 718, 29, seed=55), "Hind pom near", fill=COAT_GRAD,
       stroke=INK, strokeWidth=5)
d.path("M636,736 C654,728 674,732 676,746 C672,762 656,772 638,768 "
       "C630,758 628,744 636,736 Z", "Hind foot near", fill=CLIP_GRAD,
       stroke=INK, strokeWidth=4.5)

# near front leg — straight shaved column under the jacket, pom at the wrist
d.path(smooth([(382, 612), (392, 650), (390, 690), (382, 702), (368, 694),
               (366, 652), (370, 616)]),
       "Front leg near", fill=CLIP_GRAD, stroke=INK, strokeWidth=5)
d.path(puff(384, 714, 29, seed=0), "Front pom near", fill=COAT_GRAD,
       stroke=INK, strokeWidth=5)
d.path("M364,732 C382,724 402,728 404,742 C400,758 384,768 366,764 "
       "C358,754 356,740 364,732 Z", "Front foot near", fill=CLIP_GRAD,
       stroke=INK, strokeWidth=4.5)

# forebody — one fluffy mass: the long arched neck rising off the chest
# into the poll, deep brisket, ribcage back to the clip waistline.
d.path(smooth([(306, 396), (310, 450), (322, 520), (338, 590), (356, 645),
               (404, 662), (470, 650), (522, 622), (544, 570), (536, 510),
               (500, 462), (452, 436), (398, 408), (360, 386), (322, 384)]),
       "Neck + jacket", fill=COAT_GRAD, stroke=INK, strokeWidth=6)
# sheen — cold light down the neck arch and over the ribs
d.path("M330,410 C390,400 450,424 494,466 C448,436 388,418 330,426 Z",
       "Neck sheen", fill="#F4D9A8", opacity=35, stroke=NONE)

# ear leather — the long fluffy drop hanging over the crest, leaving the
# front of the neck clean so its length reads
d.path(smooth([(368, 384), (396, 394), (410, 432), (412, 482), (402, 526),
               (384, 546), (364, 536), (356, 494), (356, 446), (360, 406)]),
       "Ear leather", fill=lin(355, 390, 415, 550, (0, "#C08A44"), (1, "#7C4C1E")),
       stroke=INK, strokeWidth=5)

# head — clipped muzzle, straight profile, slight stop under the topknot
d.path(smooth([(326, 396), (298, 402), (270, 412), (250, 426), (246, 442),
               (256, 456), (276, 462), (304, 462), (328, 452), (342, 432),
               (340, 408)]),
       "Muzzle + skull", fill=CLIP_GRAD, stroke=INK, strokeWidth=5)
# nose — dark leather on the clipped muzzle tip
d.path("M248,430 C240,432 236,440 240,448 C246,454 256,452 260,444 "
       "C260,436 256,430 248,430 Z", "Nose", fill="#17100C",
       stroke=INK, strokeWidth=3)
d.path("M242,440 C246,436 252,435 256,437", "Nose sheen", fill=NONE,
       stroke="#5E5046", strokeWidth=2.5, opacity=70, cap="round")
# eye — small dark almond, calm and level
d.path("M314,418 C322,412 334,412 340,418 C338,428 326,432 318,428 "
       "C312,424 310,422 314,418 Z", "Eye",
       fill=rad((0, "#5E4020"), (0.7, "#3A2410"), (1, "#1E1006")),
       stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Pupil", x=324, y=418, width=9, height=10, fill="#0E0806", stroke=NONE)
d.shape("ellipse", "Glint", x=327, y=420, width=4.5, height=4.5, fill="#FFF4D8",
        opacity=90, stroke=NONE)

# topknot — the rounded ball of fluff crowning the skull into the ear
d.path(puff(346, 358, 58, squash=0.88, seed=8), "Topknot",
       fill=COAT_GRAD, stroke=INK, strokeWidth=5.5)
d.path("M312,332 C330,318 360,316 380,330 C360,322 334,324 312,332 Z",
       "Topknot sheen", fill="#F4D9A8", opacity=40, stroke=NONE)

# curl ticks — short strokes on the fluff edges, >=3pt
for i, dd in enumerate(["M330,540 C322,548 318,560 320,572",
                        "M348,596 C342,606 342,616 348,626",
                        "M414,640 C408,648 406,656 410,662",
                        "M478,642 C484,650 486,658 484,664"]):
    d.path(dd, f"Jacket curl {i+1}", fill=NONE, stroke="#6E4318",
           strokeWidth=3.5, opacity=55, cap="round")
for i, dd in enumerate(["M676,500 C684,506 688,516 686,526",
                        "M648,560 C656,566 660,574 658,582",
                        "M622,502 C616,510 616,520 620,528"]):
    d.path(dd, f"Rosette curl {i+1}", fill=NONE, stroke="#6E4318",
           strokeWidth=3.5, opacity=55, cap="round")
for i, dd in enumerate(["M368,478 C372,492 372,508 366,522",
                        "M384,486 C388,502 388,520 382,534"]):
    d.path(dd, f"Ear curl {i+1}", fill=NONE, stroke="#5E3A12",
           strokeWidth=3, opacity=50, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#26303C", strokeWidth=6)

# --- captions -------------------------------------------------------------------
d.text("STANDARD POODLE", "Name", x=500, y=934, size=56, font="Virelai Sans",
       color="#EAEDF0", justify="center")
LINE2, SZ2, TRK = "NON-SPORTING · GERMANY", 22, 280
r = d.text(LINE2, "Milestone", x=500, y=970, size=SZ2, font="Virelai Sans",
           color="#BEC6CE", justify="center")
d.cmd("text.setStyle", "Milestone tracking", id=r["id"], tracking=TRK)

b = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("milestone bounds", {k: round(v) for k, v in b.items()})
nearest = (min(max(PCX, b["x"]), b["x"] + b["width"]),
           min(max(PCY, b["y"]), b["y"] + b["height"]))
clear = math.hypot(nearest[0] - PCX, nearest[1] - PCY) - (PR + 3)
print("clears rim by %.1f" % clear)
assert clear > 0 and b["width"] <= 760 and b["x"] >= 10 and b["x"] + b["width"] <= 990, b

d.finish("standard-poodle-V1R00")
