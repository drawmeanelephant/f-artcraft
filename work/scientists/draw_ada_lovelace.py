#!/usr/bin/env python3
"""Ada Lovelace — milestone card V1R00. 1840s dress and curled hair,
gaze lowered on a punched-card chain draped between her hands — the
Bernoulli cards, warm scholarly lamplight. Faint analytical-engine gear
rings in the upper dark. The bust closes on the disc's own lower arc.
1000x1000. House style: gradients + translucent shading, never flat
fills. Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Ada Lovelace — Milestone Card", 1000, 1000)

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


def qbez(t, p0, p1, p2):
    u = 1 - t
    return (u * u * p0[0] + 2 * u * t * p1[0] + t * t * p2[0],
            u * u * p0[1] + 2 * u * t * p1[1] + t * t * p2[1])


def qbez_tan(t, p0, p1, p2):
    return (2 * (1 - t) * (p1[0] - p0[0]) + 2 * t * (p2[0] - p1[0]),
            2 * (1 - t) * (p1[1] - p0[1]) + 2 * t * (p2[1] - p1[1]))


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


BG_GRAD = lin(0, 0, 0, 1000, (0, "#171208"), (1, "#070503"))
PLATE_GRAD = rad((0, "#8A7A5C"), (0.5, "#4E4230"), (1, "#1E1810"))
SKIN_GRAD = lin(430, 320, 500, 540, (0, "#EDD0AC"), (0.55, "#CBA684"), (1, "#98745C"))
SKIN_DIM = lin(430, 320, 500, 540, (0, "#C8A484"), (1, "#84644C"))
HAIR_GRAD = lin(400, 280, 520, 540, (0, "#4A3420"), (0.5, "#2A1C10"), (1, "#120C06"))
DRESS_GRAD = lin(320, 560, 680, 850, (0, "#54303C"), (0.5, "#2E1A22"), (1, "#150C11"))
LACE_GRAD = lin(420, 540, 520, 620, (0, "#EFE4CC"), (1, "#A89878"))
CARD_GRAD = lin(0, 620, 0, 800, (0, "#DCCFAE"), (1, "#A89676"))
GEAR = "#D8C89E"

# --- backdrop + lamplit amber plate --------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#3A3226", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8DEC8", strokeWidth=3, opacity=34)

# warm lamp pool upper-left
d.shape("ellipse", "Light pool", x=225, y=140, width=400, height=240,
        fill="#F0E4C4", opacity=12, stroke=NONE)

# --- the engine in the dark — two faint gear rings, upper left -------------------
for gi, (gx, gy, gr, op) in enumerate([(306, 218, 88, 16),
                                      (226, 316, 54, 13)]):
    assert on_disc(gx - gr - 8, gy, 8) and on_disc(gx, gy - gr - 8, 8)
    d.shape("ellipse", f"Gear {gi+1}", x=gx - gr, y=gy - gr, width=gr * 2,
            height=gr * 2, fill=NONE, stroke=GEAR, strokeWidth=3,
            opacity=op)
    d.shape("ellipse", f"Gear hub {gi+1}", x=gx - gr * 0.3, y=gy - gr * 0.3,
            width=gr * 0.6, height=gr * 0.6, fill=NONE, stroke=GEAR,
            strokeWidth=2.5, opacity=op)
    for ti in range(12):
        a = math.radians(ti * 30 + gi * 15)
        x0, y0 = gx + (gr + 1) * math.cos(a), gy + (gr + 1) * math.sin(a)
        x1, y1 = gx + (gr + 11) * math.cos(a), gy + (gr + 11) * math.sin(a)
        d.path(f"M{x0:.0f},{y0:.0f} L{x1:.0f},{y1:.0f}",
               f"Gear {gi+1} tooth {ti+1}", fill=NONE, stroke=GEAR,
               strokeWidth=3.5, opacity=op, cap="round")

# --- the dress — 1840s bust closing on the disc's lower arc -----------------------
fj = 804
jl, jr = rim_x(fj, -1), rim_x(fj, 1)
d.path(f"M{jl:.1f},{fj} C300,720 318,648 356,602 C390,568 428,558 452,552 "
       f"L494,552 C536,560 574,584 600,622 C628,662 648,730 {jr:.1f},{fj} "
       f"A{PR},{PR} 0 0 1 {jl:.1f},{fj} Z", "Dress",
       fill=DRESS_GRAD, stroke=INK, strokeWidth=5)
# bodice shading — a soft V from the waist
d.path("M430,690 C448,720 492,720 512,688", "Bodice shade", fill=NONE,
       stroke="#180D12", strokeWidth=5, opacity=40, cap="round")

# lace berthe — the wide white collar lying over the shoulders
d.path(smooth([(386, 580), (420, 542), (470, 532), (522, 542), (556, 580),
               (538, 610), (470, 620), (404, 610)], k=0.9), "Berthe",
       fill=LACE_GRAD, stroke=INK, strokeWidth=4)
# scalloped hem of the lace
for i in range(7):
    x = 404 + i * 22
    d.path(f"M{x},{612 - abs(i - 3) * 3} C{x + 6},{620 - abs(i - 3) * 3} "
           f"{x + 10},{616 - abs(i - 3) * 2} {x + 16},{610 - abs(i - 3) * 2}",
           f"Lace scallop {i+1}", fill=NONE, stroke="#8A7C60",
           strokeWidth=2.5, opacity=60, cap="round")
# lace stitch dots
for i, (x, y) in enumerate([(426, 576), (452, 566), (480, 566), (506, 576),
                            (440, 596), (470, 600), (500, 596)]):
    d.shape("ellipse", f"Lace dot {i+1}", x=x - 2.5, y=y - 2.5, width=5,
            height=5, fill=NONE, stroke="#8A7C60", strokeWidth=2,
            opacity=55)

# full 1840s sleeves — puffed upper arm narrowing to the wrist
d.path(smooth([(360, 600), (336, 636), (340, 668), (364, 688), (392, 686),
               (404, 664), (402, 636), (388, 608)], k=0.9), "Sleeve L",
       fill=DRESS_GRAD, stroke=INK, strokeWidth=4)
d.path(smooth([(556, 600), (584, 632), (588, 664), (568, 686), (540, 686),
               (528, 664), (530, 634), (542, 606)], k=0.9), "Sleeve R",
       fill=DRESS_GRAD, stroke=INK, strokeWidth=4)

# neck
d.path("M452,498 L452,544 C460,552 482,552 490,544 L490,498 Z", "Neck",
       fill=SKIN_DIM, stroke=INK, strokeWidth=3.5)

# --- head: centre part + cheek ringlets -------------------------------------------
# back hair mass
d.path(smooth([(402, 428), (392, 372), (398, 318), (424, 284), (466, 272),
               (508, 284), (534, 318), (540, 372), (530, 428), (516, 446),
               (506, 416), (510, 360), (502, 318), (484, 296), (466, 292),
               (448, 296), (430, 318), (422, 360), (426, 416)], k=0.85),
       "Hair mass", fill=HAIR_GRAD, stroke=INK, strokeWidth=3.5)

# face — gentle oval, tipped a touch down
d.path(smooth([(466, 304), (506, 322), (514, 380), (508, 436), (494, 484),
               (478, 508), (464, 514), (450, 508), (434, 484), (420, 436),
               (414, 380), (422, 322)], k=0.85), "Face",
       fill=SKIN_GRAD, stroke=INK, strokeWidth=4)
# centre part
d.path("M466,286 L464,320", "Parting", fill=NONE, stroke="#140C06",
       strokeWidth=3, opacity=70, cap="round")

# ringlets — one lumpy mass per side hugging the face edge, the 1840s
# signature; separate balls read as beads, not hair
d.path(smooth([(518, 402), (548, 416), (558, 452), (548, 486), (554, 520),
               (540, 552), (520, 548), (510, 516), (514, 478), (508, 442)],
              k=0.95), "Ringlets R", fill=HAIR_GRAD, stroke=INK,
       strokeWidth=3.5)
d.path(smooth([(414, 402), (384, 416), (374, 452), (384, 486), (378, 520),
               (392, 552), (412, 548), (422, 516), (418, 478), (424, 442)],
              k=0.95), "Ringlets L", fill=HAIR_GRAD, stroke=INK,
       strokeWidth=3.5)
# curl separations — short C-strokes inside each mass
for si, cx in ((-1, 398), (1, 534)):
    for ci, cy in enumerate((440, 484, 524)):
        d.path(f"M{cx - 14},{cy - 8} C{cx},{cy - 16} {cx + 14},{cy - 8} "
               f"{cx + 10},{cy + 8}", f"Curl sep {'L' if si < 0 else 'R'} {ci+1}",
               fill=NONE, stroke="#7A5C38", strokeWidth=3, opacity=55,
               cap="round")

# features — downcast eyes, studying the cards
d.path("M424,392 C434,386 447,385 456,391", "Brow L", fill=NONE,
       stroke="#3E2C1C", strokeWidth=4, opacity=75, cap="round")
d.path("M476,391 C486,385 499,386 508,392", "Brow R", fill=NONE,
       stroke="#3E2C1C", strokeWidth=4, opacity=75, cap="round")
# lowered lids — lid arcs with short lashes, no open eye
d.path("M426,414 C434,421 448,421 455,415", "Lid L", fill=NONE,
       stroke="#6E4A34", strokeWidth=3.5, opacity=85, cap="round")
d.path("M477,415 C484,421 498,421 505,414", "Lid R", fill=NONE,
       stroke="#6E4A34", strokeWidth=3.5, opacity=85, cap="round")
for i, (x0, y0, x1, y1) in enumerate([(429, 415, 426, 420),
                                      (452, 416, 455, 421),
                                      (480, 416, 477, 421),
                                      (503, 415, 506, 420)]):
    d.path(f"M{x0},{y0} L{x1},{y1}", f"Lash {i+1}", fill=NONE,
           stroke="#4A3220", strokeWidth=2.5, opacity=70, cap="round")
# nose + mouth
d.path("M466,416 C471,432 472,450 467,462", "Nose shade", fill=NONE,
       stroke="#9A7658", strokeWidth=3.5, opacity=45, cap="round")
d.path("M459,464 C465,468 475,468 481,463", "Nose base", fill=NONE,
       stroke="#8A6248", strokeWidth=3, opacity=55, cap="round")
d.path("M452,486 C460,491 472,491 480,486", "Mouth", fill=NONE,
       stroke="#7E4C3E", strokeWidth=3.5, opacity=75, cap="round")
# cheek warmth from the lamplight
d.shape("ellipse", "Cheek warm L", x=414, y=440, width=30, height=18,
        fill=rad((0, "#E8A880", 25), (1, "#E8A880", 0)), stroke=NONE)
d.shape("ellipse", "Cheek warm R", x=488, y=440, width=30, height=18,
        fill=rad((0, "#E8A880", 22), (1, "#E8A880", 0)), stroke=NONE)

# --- the punched-card chain — cards on a curve, punched two per --------------------
HAND_L, HAND_R = (398, 662), (546, 662)


def card_run(pts, p0, p1, p2, tag, start=0):
    """Lay punched cards along a quadratic bezier."""
    n = 0
    acc = 0.0
    prev = qbez(0, p0, p1, p2)
    for i in range(1, 200):
        t = i / 199
        pt = qbez(t, p0, p1, p2)
        acc += math.hypot(pt[0] - prev[0], pt[1] - prev[1])
        prev = pt
        if acc < 33:
            continue
        acc = 0.0
        tan = qbez_tan(t, p0, p1, p2)
        deg = math.degrees(math.atan2(tan[1], tan[0]))
        n += 1
        assert on_disc(pt[0], pt[1], 12), (tag, n)
        d.path(rot_rect_path(pt[0], pt[1], 30, 20, deg),
               f"{tag} card {start + n}", fill=CARD_GRAD, stroke=INK,
               strokeWidth=2.5)
        ux, uy = tan[0] / math.hypot(*tan), tan[1] / math.hypot(*tan)
        for s in (-7, 0, 7):
            d.shape("ellipse", f"{tag} hole {start + n}",
                    x=pt[0] + ux * s - 1.8, y=pt[1] + uy * s - 1.8,
                    width=3.6, height=3.6, fill="#3A2E1C", stroke=NONE)
    return n


n1 = card_run(None, HAND_L, (472, 788), HAND_R, "Chain")
card_run(None, HAND_R, (618, 700), (606, 796), "Tail", start=n1)

# hands — small fists set a step along the curve so the chain visibly
# enters each grip
GRIP_L = qbez(0.05, HAND_L, (472, 788), HAND_R)
GRIP_R = qbez(0.95, HAND_L, (472, 788), HAND_R)
for lbl, (hx, hy) in (("Hand L", GRIP_L), ("Hand R", GRIP_R)):
    d.path(smooth([(hx - 14, hy - 12), (hx - 4, hy - 22), (hx + 12, hy - 20),
                   (hx + 18, hy - 8), (hx + 14, hy + 8), (hx - 2, hy + 12),
                   (hx - 14, hy + 6)]), lbl, fill=SKIN_GRAD, stroke=INK,
           strokeWidth=3.5)

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#342C22", strokeWidth=6)

# --- captions ---------------------------------------------------------------------
d.text("ADA LOVELACE", "Name", x=500, y=934, size=56, font="Virelai Sans",
       color="#EDE8DC", justify="center")
LINE2, SZ2, TRK = "FIRST ALGORITHM · 1843", 22, 480
r = d.text(LINE2, "Milestone", x=500, y=970, size=SZ2, font=SS3,
           color="#C4BCAC", justify="center")
d.cmd("text.setStyle", "Milestone tracking", id=r["id"], tracking=TRK)

b = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("milestone bounds", {k: round(v) for k, v in b.items()})
nearest = (min(max(PCX, b["x"]), b["x"] + b["width"]),
           min(max(PCY, b["y"]), b["y"] + b["height"]))
clear = math.hypot(nearest[0] - PCX, nearest[1] - PCY) - (PR + 3)
print("clears rim by %.1f" % clear)
assert clear > 0 and b["width"] <= 760 and b["x"] >= 10 and b["x"] + b["width"] <= 990, b

d.finish("ada-lovelace-V1R00")
