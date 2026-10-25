#!/usr/bin/env python3
"""Prince — milestone card V1R00. Purple Rain era: purple tailcoat over a
ruffled cream shirt, the cloud guitar held low, one arm thrown up in
mid-stage-command. Violet glow off the disc. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Prince — Milestone Card", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#1B121E"                    # warm dark ink, never pure black


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


BG_GRAD = lin(0, 0, 0, 1000, (0, "#150F1E"), (1, "#060408"))
PLATE_GRAD = rad((0, "#9A7CB4"), (0.5, "#5C4278"), (1, "#221830"))
COAT_GRAD = lin(350, 580, 660, 800, (0, "#7E44A0"), (0.55, "#4E2668"), (1, "#1E0F2C"))
COAT_DIM = lin(350, 580, 660, 800, (0, "#5C3276"), (1, "#170C22"))
SKIN_GRAD = rad((0, "#C09A68"), (0.6, "#94683C"), (1, "#5C3C20"))
HAIR_GRAD = lin(400, 320, 580, 540, (0, "#3A2430"), (0.6, "#221418"), (1, "#0E080C"))
FLOOR_GRAD = lin(0, 745, 0, 880, (0, "#524464"), (0.55, "#352A44"), (1, "#14101C"))
SHIRT_GRAD = lin(460, 580, 520, 780, (0, "#F2E8D4"), (0.6, "#CBBBA0"), (1, "#8E7E62"))
CLOUD_GRAD = rad((0, "#D4C6E4"), (0.6, "#9C86B4"), (1, "#544268"))

# --- backdrop + violet plate ----------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#3C2C50", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E0D0EE", strokeWidth=3, opacity=38)

# violet glow — light pool high-left + haze
d.shape("ellipse", "Light pool", x=262, y=142, width=430, height=255,
        fill="#EADCF4", opacity=14, stroke=NONE)
for i, (x, y, w) in enumerate([(352, 318, 90), (596, 244, 70), (724, 350, 80),
                               (266, 472, 60), (744, 496, 64), (480, 196, 55)]):
    assert on_disc(x, y, 20), i
    d.shape("ellipse", f"Haze {i+1}", x=x - w / 2, y=y - w / 5, width=w, height=w * 0.4,
            fill="#E2D2F0", opacity=9, stroke=NONE)

# --- floor chord, closing on the disc arc --------------------------------------------
fy = 790
fl, fr = rim_x(fy, -1), rim_x(fy, 1)
d.path(f"M{fl:.1f},{fy} C330,776 420,798 500,789 C580,780 670,786 {fr:.1f},{fy} "
       f"A{PR},{PR} 0 0 1 {fl:.1f},{fy} Z", "Floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{fl + 8:.0f},{fy} C330,776 420,798 500,789 C580,780 670,786 {fr - 8:.0f},{fy}",
       "Floor sheen", fill=NONE, stroke="#9A86B4", strokeWidth=5, opacity=36, cap="round")

# soft shadow under the figure
d.shape("ellipse", "Figure shadow", x=330, y=758, width=380, height=30,
        fill="#0A0710", opacity=34, stroke=NONE)

# --- Prince: tailcoat, ruffled shirt, cloud guitar, arm thrown up ----------------------
# raised arm FIRST (drawn under the coat's shoulder): a tapered sleeve
# sweeping up-right with a soft elbow — pointing, not flagpole-straight
d.path(smooth([(606, 616), (638, 556), (666, 496), (690, 438),
               (706, 384), (716, 350), (734, 342), (738, 360),
               (724, 420), (708, 478), (686, 538), (656, 596),
               (632, 622)]),
       "Arm up", fill=COAT_GRAD, stroke=INK, strokeWidth=5)
# shirt cuff at the wrist — the white flash under the purple sleeve
d.path("M712,352 C722,344 734,342 742,348 C740,358 732,366 722,366 "
       "C714,364 710,358 712,352 Z", "Cuff", fill=SHIRT_GRAD,
       stroke=INK, strokeWidth=2.5)
# the pointing hand — index extended straight up, the stage command
d.path(smooth([(706, 352), (700, 334), (702, 314), (710, 300),
               (722, 296), (732, 306), (736, 322), (734, 340),
               (726, 354)]),
       "Hand", fill=SKIN_GRAD, stroke=INK, strokeWidth=3.5)
d.path("M714,300 C714,288 716,276 718,266", "Index", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
d.path("M726,300 C728,290 730,280 731,272", "Finger 2", fill=NONE,
       stroke=INK, strokeWidth=3.5, opacity=85, cap="round")
d.path("M706,314 C704,306 703,298 703,292", "Finger 3", fill=NONE,
       stroke=INK, strokeWidth=3.5, opacity=80, cap="round")

# tailcoat torso — widening to the floor, swallow-tail points at the hem
d.path(smooth([(352, 640), (328, 690), (340, 744), (356, 790),
               (430, 790), (452, 758), (472, 780), (500, 752),
               (528, 782), (548, 756), (570, 790), (658, 790),
               (664, 726), (650, 666), (614, 626), (566, 596),
               (468, 592), (410, 606)]),
       "Tailcoat", fill=COAT_GRAD, stroke=INK, strokeWidth=6)
# right-side shade so the coat turns
d.path(smooth([(566, 596), (614, 626), (648, 670), (658, 732),
               (652, 788), (566, 790), (560, 712), (552, 644)]),
       "Coat shade", fill=COAT_DIM, opacity=55, stroke=NONE)
# the ruffled shirt front — a cream wedge at the chest with scallop rows
d.path(smooth([(452, 596), (478, 586), (506, 586), (528, 598),
               (534, 640), (530, 700), (522, 760), (514, 790),
               (462, 790), (452, 720), (446, 656), (446, 620)]),
       "Shirt front", fill=SHIRT_GRAD, stroke=INK, strokeWidth=3.5)
# ruffles — scallop rows across the chest, wide + shallow
for i in range(4):
    yy = 610 + i * 34
    pts = [(452, yy)]
    for j in range(1, 7):
        t = j / 6
        pts.append((452 + t * 70, yy + (8 if j % 2 else -4)))
    dd = f"M452,{yy} " + " ".join(f"C{x - 10},{y} {x - 4},{y} {x},{y}"
                                 for x, y in pts[1:])
    d.path(dd, f"Ruffle {i+1}", fill=NONE, stroke="#A89878",
           strokeWidth=3.5, opacity=65, cap="round")
# coat lapels framing the shirt wedge
d.path(smooth([(448, 592), (430, 614), (424, 660), (432, 700),
               (446, 690), (450, 644), (452, 610)]),
       "Lapel L", fill=lin(426, 592, 452, 700, (0, "#8E50B0"), (1, "#2A1638")),
       stroke=INK, strokeWidth=3.5)
d.path(smooth([(530, 594), (546, 616), (552, 662), (544, 702),
               (530, 690), (526, 644), (524, 610)]),
       "Lapel R", fill=lin(524, 594, 552, 702, (0, "#8E50B0"), (1, "#2A1638")),
       stroke=INK, strokeWidth=3.5)
# high collar horns at the jaw — the Purple Rain collar
d.path(smooth([(448, 570), (436, 552), (440, 532), (458, 524),
               (470, 540), (468, 564), (460, 580)]),
       "Collar L", fill=lin(438, 524, 470, 580, (0, "#7E44A0"), (1, "#241233")),
       stroke=INK, strokeWidth=3)
d.path(smooth([(516, 568), (526, 548), (522, 528), (506, 520),
               (494, 538), (496, 562), (504, 578)]),
       "Collar R", fill=lin(496, 520, 526, 578, (0, "#7E44A0"), (1, "#241233")),
       stroke=INK, strokeWidth=3)

# neck
d.path("M462,534 C462,550 460,562 456,576 C468,586 492,586 504,574 "
       "C500,560 498,546 498,532 Z", "Neck", fill=lin(460, 532, 500, 586,
       (0, "#A87C50"), (1, "#6E4A28")), stroke=INK, strokeWidth=3.5)

# head — compact, chin level, commanding
d.path(smooth([(438, 420), (434, 458), (440, 498), (458, 528),
               (482, 544), (506, 542), (524, 524), (536, 494),
               (538, 454), (530, 416), (510, 390), (486, 382),
               (460, 388)]),
       "Head", fill=SKIN_GRAD, stroke=INK, strokeWidth=5)
d.path("M440,472 C443,498 457,520 476,532 C456,524 441,501 439,478 Z",
       "Cheek shade", fill="#5C3C20", opacity=36, stroke=NONE)

# hair — the 1984 voluminous dark wave: high rounded mass, scalloped
# front edge, tucked behind the ears
hair = [(432, 520), (424, 486), (420, 448), (424, 410), (436, 378),
        (456, 356), (482, 346), (508, 346), (532, 356), (550, 378),
        (560, 410), (562, 446), (556, 486), (548, 520), (540, 498),
        (542, 462), (540, 430), (528, 406), (508, 396), (484, 394),
        (462, 402), (446, 420), (438, 444), (436, 478), (438, 504)]
d.path(smooth(hair), "Hair", fill=HAIR_GRAD, stroke=INK, strokeWidth=5)
# wave texture — a few long S-sweeps across the crown
for i, (x0, y0, x1, y1, x2, y2) in enumerate([
        (444, 400, 470, 384, 500, 382), (452, 428, 480, 410, 514, 408),
        (452, 456, 484, 438, 522, 434)]):
    d.path(f"M{x0},{y0} C{x1},{y1} {x1},{y1} {x2},{y2}", f"Wave {i+1}",
           fill=NONE, stroke="#4A3240", strokeWidth=4, opacity=70, cap="round")

# face — neat mustache, level eyes, the small confident mouth
d.path("M450,436 C462,430 474,428 484,432", "Brow L", fill=NONE,
       stroke="#241418", strokeWidth=4.5, opacity=85, cap="round")
d.path("M502,432 C514,428 526,428 536,434", "Brow R", fill=NONE,
       stroke="#241418", strokeWidth=4.5, opacity=85, cap="round")
d.path("M450,454 C460,448 474,446 484,452", "Lid L", fill=NONE,
       stroke=INK, strokeWidth=4.5, cap="round")
d.path("M456,461 C464,464 476,464 482,458", "Eye L", fill=NONE,
       stroke=INK, strokeWidth=3, opacity=85, cap="round")
d.path("M502,452 C512,446 526,446 534,452", "Lid R", fill=NONE,
       stroke=INK, strokeWidth=4.5, cap="round")
d.path("M506,459 C514,462 526,462 532,456", "Eye R", fill=NONE,
       stroke=INK, strokeWidth=3, opacity=85, cap="round")
# nose — straight
d.path("M488,456 C485,472 481,486 478,494 C483,500 492,500 496,495",
       "Nose", fill=NONE, stroke="#6E4A28", strokeWidth=3.5,
       opacity=80, cap="round")
# the pencil mustache — one thin bar over the lip
d.path("M464,506 C474,502 496,502 506,506", "Mustache", fill=NONE,
       stroke="#241418", strokeWidth=5, opacity=90, cap="round")
d.path("M468,516 C478,521 494,521 502,516", "Mouth", fill=NONE,
       stroke="#6E3228", strokeWidth=4.5, opacity=88, cap="round")

# --- the cloud guitar — lobed body slung low-left, neck across the body ----------------
# strap over the left shoulder
d.path("M436,604 C420,636 406,668 396,700", "Strap", fill=NONE,
       stroke="#221228", strokeWidth=7, opacity=80, cap="round")
# cloud body — the famous silhouette: rounded lobes, horn top-left
cloud = [(338, 700), (330, 672), (342, 646), (368, 636), (392, 628),
         (420, 632), (444, 646), (460, 668), (468, 694), (462, 722),
         (448, 746), (424, 758), (398, 758), (372, 750), (354, 734),
         (342, 718)]
d.path(smooth(cloud), "Cloud guitar", fill=CLOUD_GRAD, stroke=INK, strokeWidth=5)
# a second inner lobe echo — the cloud curl
d.path(smooth([(356, 690), (362, 668), (380, 656), (400, 654),
               (420, 662), (432, 678), (434, 700), (426, 720),
               (408, 730), (388, 728), (370, 716), (360, 702)]),
       "Cloud inner", fill=NONE, stroke="#6E5688", strokeWidth=3.5, opacity=65)
d.path("M348,664 C360,650 380,642 400,644", "Cloud sheen", fill=NONE,
       stroke="#E4D8F0", strokeWidth=4, opacity=60, cap="round")
# fretboard crossing the torso to the right
d.path("M452,660 L636,584 L648,598 L464,676 Z", "Fretboard",
       fill=lin(460, 656, 640, 590, (0, "#38284A"), (1, "#1A1226")),
       stroke=INK, strokeWidth=3.5)
# headstock tip
d.path(smooth([(638, 580), (656, 566), (672, 564), (678, 576),
               (668, 588), (650, 594), (640, 590)]),
       "Headstock", fill=lin(640, 564, 676, 592, (0, "#4E3A68"), (1, "#241836")),
       stroke=INK, strokeWidth=3)
# the fretting hand at the board's end
d.path(smooth([(626, 610), (622, 592), (632, 578), (648, 576),
               (660, 586), (662, 604), (652, 616), (636, 618)]),
       "Fret hand", fill=SKIN_GRAD, stroke=INK, strokeWidth=3.5)

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#2C2240", strokeWidth=6)

# --- captions -------------------------------------------------------------------
d.text("PRINCE", "Name", x=500, y=934, size=56, font="Virelai Sans",
       color="#EDE2F2", justify="center")
LINE2, YEAR, SZ2, TRK = "PURPLE RAIN · 1984", "1984", 22, 280
r = d.text(LINE2, "Milestone", x=500, y=970, size=SZ2, font="Virelai Sans",
           color="#C2ACD4", justify="center")
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

d.finish("prince-V1R00")
