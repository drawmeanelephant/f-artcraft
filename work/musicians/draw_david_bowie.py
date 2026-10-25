#!/usr/bin/env python3
"""David Bowie — milestone card V1R00. Glam-era Ziggy: spiky red mullet,
pale androgynous face, cheekbones doing the likeness, asymmetric costume —
one bare shoulder, one draped knit shoulder under a swept-up collar.
Never a straight portrait. Deep aubergine plate. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("David Bowie — Milestone Card", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#1E1216"                    # warm dark ink, never pure black


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


BG_GRAD = lin(0, 0, 0, 1000, (0, "#160E18"), (1, "#070508"))
PLATE_GRAD = rad((0, "#8E5A72"), (0.5, "#553A4E"), (1, "#201624"))
SUIT_GRAD = lin(350, 580, 660, 800, (0, "#7E3038"), (0.55, "#4C1E26"), (1, "#1A0D10"))
SUIT_DIM = lin(350, 580, 660, 800, (0, "#56222C"), (1, "#140A0D"))
SKIN_GRAD = rad((0, "#EFCBAE"), (0.6, "#C69570"), (1, "#7E5434"))
HAIR_GRAD = lin(400, 300, 580, 540, (0, "#C8502E"), (0.55, "#8C3218"), (1, "#481608"))
FLOOR_GRAD = lin(0, 745, 0, 880, (0, "#574452"), (0.55, "#382C38"), (1, "#15111A"))
GOLD = "#D8A44C"

# --- backdrop + aubergine glam plate --------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#3E2C40", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E4C4D4", strokeWidth=3, opacity=38)

# magenta light pool high left + sparse haze
d.shape("ellipse", "Light pool", x=262, y=142, width=430, height=255,
        fill="#F0D4E0", opacity=13, stroke=NONE)
for i, (x, y, w) in enumerate([(352, 318, 90), (596, 244, 70), (724, 350, 80),
                               (266, 472, 60), (744, 496, 64), (480, 196, 55)]):
    assert on_disc(x, y, 20), i
    d.shape("ellipse", f"Haze {i+1}", x=x - w / 2, y=y - w / 5, width=w, height=w * 0.4,
            fill="#E8CEDA", opacity=9, stroke=NONE)

# --- floor chord, closing on the disc arc --------------------------------------------
fy = 790
fl, fr = rim_x(fy, -1), rim_x(fy, 1)
d.path(f"M{fl:.1f},{fy} C330,776 420,798 500,789 C580,780 670,786 {fr:.1f},{fy} "
       f"A{PR},{PR} 0 0 1 {fl:.1f},{fy} Z", "Floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{fl + 8:.0f},{fy} C330,776 420,798 500,789 C580,780 670,786 {fr - 8:.0f},{fy}",
       "Floor sheen", fill=NONE, stroke="#9A8298", strokeWidth=5, opacity=36, cap="round")

# soft shadow under the figure
d.shape("ellipse", "Figure shadow", x=330, y=758, width=380, height=30,
        fill="#0B0709", opacity=34, stroke=NONE)

# --- Bowie: asymmetric bust, head tipped, cheekbones carrying it -----------------------
# torso — viewer's LEFT bare (skin), viewer's RIGHT the draped knit suit.
# bare shoulder+chest first, then the suit drawn over the right half.
d.path(smooth([(352, 640), (328, 690), (340, 744), (356, 790),
               (656, 790), (664, 726), (650, 666), (616, 626),
               (566, 596), (470, 592), (412, 606)]),
       "Torso base", fill=SKIN_GRAD, stroke=INK, strokeWidth=6)
# chest shading under the bare shoulder
d.path(smooth([(360, 660), (380, 700), (420, 730), (470, 742),
               (460, 780), (400, 780), (356, 742), (342, 700)]),
       "Chest shade", fill="#7E5434", opacity=30, stroke=NONE)
# the knit suit — covers the right half, its neckline rising to a peaked
# collar point beside the jaw (the asymmetry is built into the suit edge,
# not a floating wing)
d.path(smooth([(492, 592), (528, 566), (566, 542), (596, 536),
               (614, 556), (626, 594), (644, 636), (656, 690),
               (660, 740), (656, 790), (470, 790), (480, 720),
               (488, 656), (490, 620)]),
       "Suit", fill=SUIT_GRAD, stroke=INK, strokeWidth=5)
# suit's diagonal neckline from the bare chest up to the collar point
d.path("M492,600 C500,640 506,690 512,738 C514,758 516,774 518,790",
       "Suit edge", fill=NONE, stroke=INK, strokeWidth=4, cap="round")
# collar fold under the peak
d.path("M566,566 C584,560 600,560 612,568", "Collar fold", fill=NONE,
       stroke="#2A1216", strokeWidth=3.5, opacity=70, cap="round")
d.path("M556,556 C576,544 596,540 610,544", "Collar sheen", fill=NONE,
       stroke="#C86A5E", strokeWidth=3.5, opacity=55, cap="round")
# knit stripes across the draped shoulder — the Ziggy knit read
for i in range(4):
    yy = 620 + i * 38
    d.path(f"M{548 + i * 8},{yy} C{590 + i * 4},{yy - 14} {626},{yy - 6} {648},{yy + 8}",
           f"Knit stripe {i+1}", fill=NONE, stroke=GOLD, strokeWidth=4,
           opacity=55, cap="round")
# suit right-side shade
d.path(smooth([(600, 610), (636, 640), (656, 690), (660, 750),
               (656, 788), (590, 790), (584, 720), (576, 656)]),
       "Suit shade", fill=SUIT_DIM, opacity=55, stroke=NONE)

# nape fall — the mullet's back length, drawn BEFORE the head as narrow
# slivers starting under the jaw, tucking out onto the shoulders
d.path(smooth([(436, 540), (430, 570), (434, 600), (444, 622),
               (452, 610), (450, 578), (450, 552)]),
       "Nape fall L", fill=HAIR_GRAD, stroke=INK, strokeWidth=3.5)
d.path(smooth([(520, 536), (526, 568), (524, 598), (514, 620),
               (506, 608), (508, 576), (508, 550)]),
       "Nape fall R", fill=HAIR_GRAD, stroke=INK, strokeWidth=3.5)

# neck — long, bare on the left, disappearing under the collar right
d.path("M462,532 C462,548 460,562 456,578 C468,588 492,588 504,576 "
       "C500,562 498,546 498,530 Z", "Neck", fill=lin(460, 530, 500, 588,
       (0, "#D0A276"), (1, "#96673E")), stroke=INK, strokeWidth=3.5)

# head — narrow, tipped a few degrees, chin slightly raised
d.path(smooth([(436, 422), (432, 458), (438, 496), (456, 526),
               (478, 542), (502, 540), (520, 522), (532, 492),
               (534, 452), (526, 414), (508, 388), (484, 380),
               (458, 386)]),
       "Head", fill=SKIN_GRAD, stroke=INK, strokeWidth=5)
# hollow cheeks — the glam gauntness: shade wedges under each cheekbone
d.path(smooth([(440, 476), (452, 470), (468, 472), (474, 484),
               (466, 500), (452, 506), (442, 496)]),
       "Hollow L", fill="#96673E", opacity=32, stroke=NONE)
d.path(smooth([(500, 478), (512, 472), (526, 474), (532, 486),
               (524, 500), (510, 504), (502, 494)]),
       "Hollow R", fill="#96673E", opacity=30, stroke=NONE)
# cheekbone blades — sharp light strokes ABOVE the hollows; this pair is
# the likeness
d.path("M438,472 C452,464 468,462 480,468", "Cheekbone L", fill=NONE,
       stroke="#F2D8B8", strokeWidth=4.5, opacity=75, cap="round")
d.path("M498,468 C512,462 526,462 536,468", "Cheekbone R", fill=NONE,
       stroke="#F2D8B8", strokeWidth=4.5, opacity=70, cap="round")

# the mullet — spiky choppy crown (out/in pairs), cropped SHORT at the
# sides ending above the jaw; the back length is a separate fall behind
# the neck, drawn after so it peeks out under the ears
mullet = [(428, 498), (422, 470), (416, 442), (412, 416), (404, 398),
          (412, 380), (404, 364), (418, 348), (412, 330), (430, 322),
          (434, 300), (454, 306), (462, 284), (480, 300), (498, 282),
          (512, 302), (532, 290), (544, 312), (562, 310), (570, 332),
          (568, 352), (556, 372), (560, 396), (552, 424), (556, 458),
          (552, 490), (540, 504), (530, 478), (534, 440), (534, 408),
          (520, 386), (498, 376), (474, 378), (454, 390), (442, 408),
          (436, 434), (436, 462)]
d.path(smooth(mullet), "Mullet", fill=HAIR_GRAD, stroke=INK, strokeWidth=5)
# spike texture inside the crown — short flicks following the spikes
for i, (x0, y0, x2, y2) in enumerate([(436, 360, 428, 330), (462, 352, 458, 318),
                                      (492, 348, 494, 312), (520, 352, 528, 318),
                                      (546, 366, 554, 336)]):
    d.path(f"M{x0},{y0} C{x0},{y0 - 12} {x2},{y2 + 12} {x2},{y2}",
           f"Spike {i+1}", fill=NONE, stroke="#5E2410", strokeWidth=3.5,
           opacity=65, cap="round")
# nape fall — the mullet's back length, one strand flick each side
d.path("M432,540 C428,566 430,590 438,610", "Nape flick L", fill=NONE,
       stroke="#8C3218", strokeWidth=4, opacity=70, cap="round")
d.path("M540,548 C544,572 542,594 534,612", "Nape flick R", fill=NONE,
       stroke="#8C3218", strokeWidth=4, opacity=70, cap="round")

# face — thin angled brows, heavy-lidded eyes, small poised mouth
d.path("M446,436 C458,428 472,426 482,432", "Brow L", fill=NONE,
       stroke="#4A2410", strokeWidth=4.5, opacity=85, cap="round")
d.path("M500,430 C512,424 524,424 534,432", "Brow R", fill=NONE,
       stroke="#4A2410", strokeWidth=4.5, opacity=85, cap="round")
# eyes — heavy lids half-lowered, the famous languid gaze; the right is
# set a touch wider (the asymmetric read, subtle)
d.path("M446,454 C456,448 470,446 480,452", "Lid L", fill=NONE,
       stroke=INK, strokeWidth=4.5, cap="round")
d.shape("ellipse", "Iris L", x=460, y=450, width=9, height=10,
        fill="#1E1410", stroke=NONE)
d.path("M498,452 C510,446 524,446 534,452", "Lid R", fill=NONE,
       stroke=INK, strokeWidth=4.5, cap="round")
d.shape("ellipse", "Iris R", x=512, y=449, width=9, height=10,
        fill="#1E1410", stroke=NONE)
# glam liner — a darker tick under each lower lid
d.path("M452,462 C462,466 474,466 480,460", "Liner L", fill=NONE,
       stroke="#6E3226", strokeWidth=3, opacity=70, cap="round")
d.path("M504,460 C514,464 526,464 532,458", "Liner R", fill=NONE,
       stroke="#6E3226", strokeWidth=3, opacity=70, cap="round")
# nose — straight and fine
d.path("M486,458 C483,472 479,486 476,494 C481,500 490,500 494,495",
       "Nose", fill=NONE, stroke="#96673E", strokeWidth=3.5,
       opacity=80, cap="round")
# mouth — small, full-lipped, set level and unsmiling
d.path("M464,518 C476,520 492,520 504,517", "Mouth", fill=NONE,
       stroke="#8E3C32", strokeWidth=5, opacity=90, cap="round")
d.path("M470,521 C478,527 490,527 498,521", "Lower lip", fill=NONE,
       stroke="#B06050", strokeWidth=2.5, opacity=50, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#332435", strokeWidth=6)

# --- captions -------------------------------------------------------------------
d.text("DAVID BOWIE", "Name", x=500, y=934, size=56, font="Virelai Sans",
       color="#F0DEE4", justify="center")
LINE2, YEAR, SZ2, TRK = "ZIGGY STARDUST · 1972", "1972", 22, 280
r = d.text(LINE2, "Milestone", x=500, y=970, size=SZ2, font="Virelai Sans",
           color="#C8A4B4", justify="center")
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

d.finish("david-bowie-V1R00")
