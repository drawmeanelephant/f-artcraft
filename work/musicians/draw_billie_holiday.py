#!/usr/bin/env python3
"""Billie Holiday — milestone card V1R00. Head and shoulders at a round
vintage mic, gardenia over the ear, eyes lowered — 1940s spotlit hush,
high collar and pearls. Cool smoky plate, one spotlight shaft.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Billie Holiday — Milestone Card", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#1C1618"                    # warm dark ink, never pure black


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


BG_GRAD = lin(0, 0, 0, 1000, (0, "#131720"), (1, "#06080C"))
PLATE_GRAD = rad((0, "#93A0B4"), (0.5, "#5C6A80"), (1, "#2A3140"))
DRESS_GRAD = lin(360, 580, 660, 800, (0, "#2E3242"), (0.55, "#1C1E2A"), (1, "#0E1016"))
SKIN_GRAD = rad((0, "#A66E44"), (0.6, "#7E4E2C"), (1, "#502E18"))
HAIR_GRAD = lin(420, 340, 560, 520, (0, "#342620"), (0.6, "#1A1210"), (1, "#0A0706"))
FLOOR_GRAD = lin(0, 745, 0, 880, (0, "#424A58"), (0.55, "#2C3240"), (1, "#141820"))
PEARL = "#EAE4D2"

# --- backdrop + smoky spotlit plate ---------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#2E3648", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8E2F0", strokeWidth=3, opacity=40)

# one spotlight shaft from upper-left, fading as it falls, bounded in the disc
spot = [(400, 66), (560, 66), (700, 748), (500, 748)]
for cx, cy in spot: assert on_disc(cx, cy, 8), (cx, cy)
d.path("M%.0f,%.0f L%.0f,%.0f L%.0f,%.0f L%.0f,%.0f Z" % tuple(sum(spot, ())),
       "Spot shaft",
       fill={"gradient": {"kind": "linear", "start": [460, 60], "end": [610, 760],
             "stops": [{"offset": 0, "color": "#E8ECF4", "opacity": 0.30},
                       {"offset": 0.7, "color": "#E8ECF4", "opacity": 0.10},
                       {"offset": 1, "color": "#E8ECF4", "opacity": 0}]}},
       stroke=NONE)
d.shape("ellipse", "Light pool", x=270, y=140, width=430, height=250,
        fill="#E4EAF4", opacity=15, stroke=NONE)
for i, (x, y, w) in enumerate([(360, 320, 90), (600, 240, 70), (725, 350, 80),
                               (265, 470, 60), (745, 495, 64), (480, 190, 55)]):
    assert on_disc(x, y, 20), i
    d.shape("ellipse", f"Haze {i+1}", x=x - w / 2, y=y - w / 5, width=w, height=w * 0.4,
            fill="#DCE4F0", opacity=10, stroke=NONE)

# --- floor chord, closing on the disc arc --------------------------------------------
fy = 790
fl, fr = rim_x(fy, -1), rim_x(fy, 1)
d.path(f"M{fl:.1f},{fy} C330,776 420,798 500,789 C580,780 670,786 {fr:.1f},{fy} "
       f"A{PR},{PR} 0 0 1 {fl:.1f},{fy} Z", "Floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{fl + 8:.0f},{fy} C330,776 420,798 500,789 C580,780 670,786 {fr - 8:.0f},{fy}",
       "Floor sheen", fill=NONE, stroke="#8A98AC", strokeWidth=5, opacity=38, cap="round")

# soft shadow under the figure
d.shape("ellipse", "Figure shadow", x=330, y=758, width=380, height=30,
        fill="#0A0C10", opacity=34, stroke=NONE)

# --- Billie Holiday: head & shoulders, eyes lowered at the mic -------------------------
# torso — dark high-collared dress, widening to the floor
d.path(smooth([(356, 636), (330, 686), (340, 742), (356, 790),
               (656, 790), (664, 724), (650, 664), (614, 626),
               (562, 596), (468, 592), (410, 606)]),
       "Dress", fill=DRESS_GRAD, stroke=INK, strokeWidth=6)
# right-side shade so the torso turns
d.path(smooth([(566, 598), (614, 628), (648, 672), (658, 734),
               (650, 788), (566, 790), (560, 712), (552, 644)]),
       "Dress shade", fill="#0C0E14", opacity=55, stroke=NONE)
# high collar — a band rising to the jawline, wings folding at the front
d.path(smooth([(438, 566), (446, 592), (470, 606), (498, 608),
               (524, 596), (532, 570), (524, 550), (500, 542),
               (472, 544), (450, 552)]),
       "Collar", fill=lin(450, 540, 530, 608, (0, "#3A4054"), (1, "#1A1C26")),
       stroke=INK, strokeWidth=3.5)
# collar edge catching the spot
d.path("M444,562 C462,548 498,542 522,550", "Collar light", fill=NONE,
       stroke="#5A6478", strokeWidth=3.5, opacity=65, cap="round")
# pearls — two strands of small beads over the collar band
for strand, (y0, drop, xr) in enumerate([(588, 14, (452, 522)),
                                          (596, 26, (448, 526))]):
    x0, x1 = xr
    for j in range(9):
        t = j / 8
        px = x0 + (x1 - x0) * t
        py = y0 + drop * math.sin(math.pi * t)
        d.shape("ellipse", f"Pearl {strand}-{j}", x=px - 4.4, y=py - 4.4,
                width=8.8, height=8.8,
                fill=rad((0, "#F8F4E4"), (1, "#B8AE94")),
                stroke=INK, strokeWidth=1.6)

# neck — short, mostly behind the collar
d.path("M458,522 C458,538 456,550 452,564 C464,574 488,574 500,562 "
       "C496,548 494,534 494,520 Z", "Neck", fill=lin(456, 522, 496, 574,
       (0, "#96623C"), (1, "#6E4524")), stroke=INK, strokeWidth=3.5)

# low bun at the nape, tucked behind the jaw (drawn before the head)
d.path("M418,486 C402,492 394,508 398,526 C402,540 418,546 430,538 "
       "C438,526 438,504 428,490 Z", "Bun", fill=HAIR_GRAD,
       stroke=INK, strokeWidth=3.5)
d.path("M406,502 C412,510 422,514 432,512", "Bun sheen", fill=NONE,
       stroke="#4A382E", strokeWidth=3, opacity=60, cap="round")

# head — three-quarter facing the mic (right), chin dipped a touch
d.path(smooth([(424, 414), (420, 454), (426, 494), (444, 524),
               (468, 540), (494, 538), (516, 520), (528, 490),
               (530, 450), (522, 412), (502, 386), (476, 378),
               (448, 383)]),
       "Head", fill=SKIN_GRAD, stroke=INK, strokeWidth=5)
d.path("M426,468 C429,495 443,518 464,530 C442,522 427,499 425,474 Z",
       "Cheek shade", fill="#502E18", opacity=40, stroke=NONE)

# hair — dark, waved close to the skull and pulled low at the nape
d.path(smooth([(418, 430), (410, 390), (424, 350), (456, 328),
               (494, 322), (526, 334), (546, 362), (554, 398),
               (550, 428), (542, 442), (534, 428), (528, 402),
               (512, 384), (486, 378), (460, 382), (438, 396),
               (426, 424)]),
       "Hair", fill=HAIR_GRAD, stroke=INK, strokeWidth=5)
# finger-wave ridges across the crown
d.path("M436,392 C458,376 488,370 514,378", "Wave 1", fill=NONE,
       stroke="#4A382E", strokeWidth=4, opacity=70, cap="round")
d.path("M432,410 C452,394 480,388 506,394", "Wave 2", fill=NONE,
       stroke="#4A382E", strokeWidth=3.5, opacity=55, cap="round")
# gardenia over the left ear — layered cream petals
gx, gy = 415, 415
for i, (dx, dy, w, h) in enumerate([(-26, -6, 30, 18), (-16, -24, 26, 18),
                                    (4, -28, 28, 18), (22, -16, 26, 18),
                                    (26, 4, 24, 17), (14, 22, 26, 17),
                                    (-8, 26, 26, 17), (-26, 14, 24, 16)]):
    d.shape("ellipse", f"Petal {i+1}", x=gx + dx - w / 2, y=gy + dy - h / 2,
            width=w, height=h,
            fill=rad((0, "#FAF6E8"), (1, "#CFC2A0")),
            stroke=INK, strokeWidth=2.5)
d.shape("ellipse", "Gardenia heart", x=gx - 10, y=gy - 9, width=20, height=18,
        fill=rad((0, "#F2E4B4"), (1, "#C8A86A")), stroke=INK, strokeWidth=2.5)

# face — eyes lowered, small closed mouth; the hush is in the lids
d.path("M440,438 C452,432 466,430 478,434", "Brow L", fill=NONE,
       stroke="#2A1A12", strokeWidth=4.5, opacity=80, cap="round")
d.path("M496,434 C508,430 520,430 530,434", "Brow R", fill=NONE,
       stroke="#2A1A12", strokeWidth=4.5, opacity=80, cap="round")
# lowered lids — downward-curving arcs with lash ticks
d.path("M440,456 C450,464 464,466 474,460", "Lid L", fill=NONE,
       stroke=INK, strokeWidth=4.5, cap="round")
d.path("M494,454 C504,462 516,464 526,458", "Lid R", fill=NONE,
       stroke=INK, strokeWidth=4.5, cap="round")
for i in range(3):
    d.path(f"M{444 + i * 9},{462 + i} l-3,6", f"Lash L{i+1}", fill=NONE,
           stroke=INK, strokeWidth=2.5, cap="round")
for i in range(3):
    d.path(f"M{498 + i * 9},{460 + i} l-3,6", f"Lash R{i+1}", fill=NONE,
           stroke=INK, strokeWidth=2.5, cap="round")
# nose — soft, pointing toward the mic
d.path("M484,458 C481,472 477,486 474,494 C479,500 488,500 492,495",
       "Nose", fill=NONE, stroke="#5C341C", strokeWidth=3.5,
       opacity=80, cap="round")
# mouth — small, dark red, nearly closed
d.path("M458,512 C470,518 486,519 498,514", "Mouth", fill=NONE,
       stroke="#6E2A20", strokeWidth=5, opacity=90, cap="round")
d.path("M464,517 C472,525 486,526 494,519", "Lower lip", fill=NONE,
       stroke="#96522E", strokeWidth=2.5, opacity=50, cap="round")
# faint cheek warmth in the spotlight
d.shape("ellipse", "Blush L", x=434, y=488, width=22, height=12,
        fill="#B85C40", opacity=18, stroke=NONE)

# --- the round vintage mic on its stand, right of her face -----------------------------
# stand — slim pole from the floor to the mic yoke
d.path("M654,560 L662,560 L660,790 L650,790 Z", "Mic stand",
       fill=lin(652, 560, 660, 790, (0, "#3E4654"), (1, "#141820")),
       stroke=INK, strokeWidth=2.5)
# yoke arms cradling the mic head
d.path("M642,556 C636,540 638,522 648,510", "Yoke L", fill=NONE,
       stroke="#3E4654", strokeWidth=6, cap="round")
d.path("M672,556 C678,540 676,522 666,510", "Yoke R", fill=NONE,
       stroke="#3E4654", strokeWidth=6, cap="round")
# the mic head — a round grill capsule
d.shape("ellipse", "Mic head", x=620, y=462, width=62, height=62,
        fill=rad((0, "#6E7A8E"), (0.6, "#464E5E"), (1, "#22262E")),
        stroke=INK, strokeWidth=4)
for i, yy in enumerate(range(472, 516, 10)):
    wch = math.sqrt(max(0, 30 ** 2 - (yy + 4 - 493) ** 2)) * 0.86
    d.path(f"M{651 - wch:.0f},{yy} C{651 - wch / 2:.0f},{yy - 3} "
           f"{651 + wch / 2:.0f},{yy - 3} {651 + wch:.0f},{yy}",
           f"Grill {i+1}", fill=NONE, stroke="#AAB4C4", strokeWidth=2.5,
           opacity=75, cap="round")
# mic catching the spot — rim light on the left edge
d.path("M626,478 C622,488 622,500 627,510", "Mic rim light", fill=NONE,
       stroke="#E4EAF4", strokeWidth=3.5, opacity=70, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#262C3A", strokeWidth=6)

# --- captions -------------------------------------------------------------------
d.text("BILLIE HOLIDAY", "Name", x=500, y=934, size=56, font="Virelai Sans",
       color="#EAEEF4", justify="center")
LINE2, YEAR, SZ2, TRK = "STRANGE FRUIT · 1939", "1939", 22, 280
r = d.text(LINE2, "Milestone", x=500, y=970, size=SZ2, font="Virelai Sans",
           color="#B8C2D2", justify="center")
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

d.finish("billie-holiday-V1R00")
