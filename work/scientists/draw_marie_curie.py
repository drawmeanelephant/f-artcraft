#!/usr/bin/env python3
"""Marie Curie — milestone card V1R00. Portrait bust at a dark bench,
holding a faintly glowing vial up beside her face — the radium's
blue-green is the only bright accent on the plate. Black dress, hair
piled up, watchful. The bust crops on the disc's own lower arc; the
bench is the floor band closed on that same arc. 1000x1000. House
style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Marie Curie — Milestone Card", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#1E150F"                    # warm dark ink, never pure black


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


BG_GRAD = lin(0, 0, 0, 1000, (0, "#13191D"), (1, "#06090B"))
PLATE_GRAD = rad((0, "#87988E"), (0.5, "#52625A"), (1, "#242E2A"))
SKIN_GRAD = lin(430, 330, 500, 530, (0, "#E6C8A6"), (0.55, "#C6A182"), (1, "#93705A"))
SKIN_DIM = lin(430, 330, 500, 530, (0, "#C2A184"), (1, "#7E5E48"))
HAIR_GRAD = lin(420, 260, 540, 520, (0, "#6A5240"), (0.5, "#3E2E22"), (1, "#1C130C"))
DRESS_GRAD = lin(330, 560, 680, 860, (0, "#463A30"), (0.5, "#241B14"), (1, "#120D09"))
DRESS_DIM = lin(330, 560, 680, 860, (0, "#332A22"), (1, "#0F0B08"))
BENCH_GRAD = lin(0, 792, 0, 885, (0, "#4A3E30"), (0.55, "#2A221A"), (1, "#120E0A"))
GLOW = "#9FF0DC"

# --- backdrop + teal-slate plate -----------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#2E3833", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#DCE8DC", strokeWidth=3, opacity=36)

# thin light pooling upper-left
d.shape("ellipse", "Light pool", x=240, y=140, width=400, height=230,
        fill="#E4F0E4", opacity=12, stroke=NONE)
# drifting mist lenses — kept clear of the face zone
for i, (x, y, w) in enumerate([(300, 360, 80), (580, 250, 70), (720, 390, 80),
                               (250, 510, 60), (755, 520, 64)]):
    assert on_disc(x, y, 20), i
    d.shape("ellipse", f"Mist {i+1}", x=x - w / 2, y=y - w / 5, width=w,
            height=w * 0.4, fill="#DCE8DC", opacity=10, stroke=NONE)

# --- torso: the black dress, cropped by the bench band later --------------------
# neck
d.path("M446,498 L446,548 C455,557 480,557 488,548 L488,498 Z", "Neck",
       fill=SKIN_DIM, stroke=INK, strokeWidth=3.5)

# dress mass — left edge bulges into her hanging arm; bottom edge sits
# under the bench band, never seen
d.path(smooth([(310, 820), (336, 788), (318, 744), (300, 706), (290, 668),
               (300, 634), (330, 606), (382, 578), (416, 566), (514, 566),
               (560, 580), (612, 612), (652, 668), (688, 736), (700, 820)],
              k=0.9),
       "Dress", fill=DRESS_GRAD, stroke=INK, strokeWidth=5)
# sleeve seam shading the hanging arm off from the bodice
d.path("M340,610 C322,650 312,700 316,752", "Sleeve seam", fill=NONE,
       stroke="#0F0B08", strokeWidth=4, opacity=40, cap="round")

# high collar band + period fichu at the front
d.path(smooth([(430, 556), (446, 538), (490, 538), (506, 556), (500, 584),
               (436, 584)]), "Collar",
       fill=lin(430, 538, 505, 584, (0, "#3E342A"), (1, "#1C1510")),
       stroke=INK, strokeWidth=4)
d.path("M456,562 L480,562 L468,600 Z", "Fichu",
       fill=lin(456, 562, 468, 600, (0, "#C8BBA0"), (1, "#8A7E66")),
       opacity=85, stroke=INK, strokeWidth=3)
# collar top edge
d.path("M436,556 C454,548 482,548 502,556", "Collar edge", fill=NONE,
       stroke="#6A5A48", strokeWidth=3.5, opacity=60, cap="round")

# dress folds + shoulder sheen
for i, dd in enumerate([
        "M400,600 C390,660 388,720 396,772",
        "M470,620 C466,680 466,730 470,780",
        "M560,600 C580,660 596,720 606,772"]):
    d.path(dd, f"Dress fold {i+1}", fill=NONE, stroke="#0F0B08",
           strokeWidth=4, opacity=45, cap="round")
d.path("M336,606 C380,584 420,576 460,574", "Shoulder sheen", fill=NONE,
       stroke="#6E5C4A", strokeWidth=5, opacity=35, cap="round")

# --- the bench — floor band closing on the disc arc -----------------------------
fy = 795
fl, fr = rim_x(fy, -1), rim_x(fy, 1)
d.path(f"M{fl:.1f},{fy} C360,782 640,784 {fr:.1f},{fy} "
       f"A{PR},{PR} 0 0 1 {fl:.1f},{fy} Z", "Bench", fill=BENCH_GRAD,
       stroke=NONE)
d.path(f"M{fl + 8:.0f},{fy} C360,782 640,784 {fr - 8:.0f},{fy}",
       "Bench crest", fill=NONE, stroke="#8A785C", strokeWidth=5,
       opacity=40, cap="round")

# dead-dark props on the bench — nothing may rival the vial's glow
# erlenmeyer flask, left
for x, y in [(306, 740), (312, 740)]:
    assert on_disc(x, y, 8), (x, y)
d.path("M300,740 L300,758 L284,794 L332,794 L316,758 L316,740 Z", "Flask",
       fill="#1C1812", stroke=INK, strokeWidth=3.5)
d.path("M292,786 L324,786", "Flask content", fill=NONE, stroke="#2E3A32",
       strokeWidth=4, opacity=50, cap="round")
d.path("M300,746 L300,758", "Flask sheen", fill=NONE, stroke="#5C5444",
       strokeWidth=2.5, opacity=45, cap="round")
# two stacked notebooks, right
for x, y in [(688, 780), (700, 790)]:
    assert on_disc(x, y, 8), (x, y)
d.path("M664,782 L724,782 L722,790 L666,790 Z", "Notebook lower",
       fill="#241E16", stroke=INK, strokeWidth=3)
d.path("M670,772 L718,772 L722,782 L666,782 Z", "Notebook upper",
       fill="#2E2820", stroke=INK, strokeWidth=3)

# her left arm drops behind the bench edge — hand out of sight, as in the
# formal portraits

# --- radium glow washing the chest, under the head and raised arm ---------------
d.shape("ellipse", "Glow wide", x=503, y=352, width=240, height=240,
        fill=rad((0, GLOW, 16), (1, GLOW, 0)), stroke=NONE)

# --- head ----------------------------------------------------------------------
# bun dome on the crown, then the hair mass framing the face
d.shape("ellipse", "Bun", x=430, y=254, width=76, height=58,
        fill=HAIR_GRAD, stroke=INK, strokeWidth=4)
d.path("M440,278 C452,266 476,264 492,274", "Bun wave", fill=NONE,
       stroke="#7A604A", strokeWidth=3.5, opacity=50, cap="round")
d.path(smooth([(400, 430), (391, 396), (394, 338), (409, 298), (432, 273),
               (464, 265), (495, 270), (517, 292), (530, 328), (534, 378),
               (533, 424), (524, 450), (506, 458), (426, 448)]), "Hair mass",
       fill=HAIR_GRAD, stroke=INK, strokeWidth=4)

# face
d.path(smooth([(465, 336), (518, 350), (523, 412), (505, 470), (465, 512),
               (425, 470), (407, 412), (412, 350)], k=0.85), "Face",
       fill=SKIN_GRAD, stroke=INK, strokeWidth=4)
# hairline band over the forehead — centre-parted
d.path("M408,384 C414,342 444,320 465,318 C490,320 518,344 523,386 "
       "C512,354 492,338 465,336 C440,338 418,356 408,384 Z",
       "Hairline", fill=HAIR_GRAD, stroke=NONE)
# parted wave strokes
for i, dd in enumerate(["M465,322 C450,330 434,344 424,362",
                        "M465,322 C482,330 498,346 508,364",
                        "M438,330 C428,340 420,352 416,366"]):
    d.path(dd, f"Hair wave {i+1}", fill=NONE, stroke="#7A604A",
           strokeWidth=3.5, opacity=50, cap="round")

# cheek shades — soft, and a faint radium sheen on the vial side
d.path("M420,430 C424,452 434,468 448,478", "Cheek shade L", fill=NONE,
       stroke="#9A7658", strokeWidth=5, opacity=25, cap="round")
d.path("M508,428 C506,450 500,466 490,478", "Cheek sheen R", fill=NONE,
       stroke=GLOW, strokeWidth=6, opacity=16, cap="round")

# brows — level, attentive
d.path("M424,398 C434,392 448,392 456,397", "Brow L", fill=NONE,
       stroke="#3A2A1E", strokeWidth=4, opacity=75, cap="round")
d.path("M478,397 C488,392 500,392 508,398", "Brow R", fill=NONE,
       stroke="#3A2A1E", strokeWidth=4, opacity=75, cap="round")
# eyes — dark almond, iris, glint
d.path("M426,418 C432,410 448,410 455,418 C448,426 432,426 426,418 Z",
       "Eye L", fill="#EFE4D0", stroke=INK, strokeWidth=3)
d.path("M480,418 C487,410 502,410 509,418 C502,426 487,426 480,418 Z",
       "Eye R", fill="#EFE4D0", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Iris L", x=436, y=412, width=11, height=12,
        fill="#2A2018", stroke=NONE)
d.shape("ellipse", "Iris R", x=490, y=412, width=11, height=12,
        fill="#2A2018", stroke=NONE)
d.shape("ellipse", "Glint L", x=439, y=414, width=3.5, height=3.5,
        fill="#FFF4DC", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=493, y=414, width=3.5, height=3.5,
        fill="#FFF4DC", opacity=90, stroke=NONE)
# nose — one soft shadow stroke, nostril hint
d.path("M471,424 C475,438 475,452 469,461", "Nose shade", fill=NONE,
       stroke="#9A7658", strokeWidth=3.5, opacity=45, cap="round")
d.path("M462,462 C466,465 472,465 476,462", "Nose base", fill=NONE,
       stroke="#8A6248", strokeWidth=3, opacity=55, cap="round")
# mouth — small, level, watchful
d.path("M448,482 C458,487 474,487 484,481", "Mouth", fill=NONE,
       stroke="#7A4A3A", strokeWidth=4, opacity=80, cap="round")
d.path("M456,492 C464,495 472,495 478,492", "Lip shade", fill=NONE,
       stroke="#9A6248", strokeWidth=3, opacity=40, cap="round")

# --- raised arm + the vial --------------------------------------------------------
# sleeve — forearm lifted beside the face, tapering to the wrist
d.path(smooth([(592, 612), (622, 594), (646, 566), (656, 532), (652, 504),
               (632, 494), (615, 508), (606, 544), (597, 578), (584, 602)]),
       "Sleeve raised", fill=DRESS_GRAD, stroke=INK, strokeWidth=4.5)
# tight halo right around the vial
d.shape("ellipse", "Glow tight", x=578, y=427, width=92, height=92,
        fill=rad((0, GLOW, 42), (1, GLOW, 0)), stroke=NONE)
# vial glass + liquid + cork
d.path("M616,420 L616,494 Q616,505 624,505 Q632,505 632,494 L632,420 Z",
       "Vial glass", fill="#9FE8D0", opacity=28, stroke="#D8F8EC",
       strokeWidth=3)
d.path("M619,458 L619,493 Q624,499 629,493 L629,458 Z", "Vial liquid",
       fill=rad((0, "#E4FDF2"), (0.6, "#9FF0DC"), (1, "#5CC0A4")),
       opacity=95, stroke=NONE)
d.path("M619,412 L629,412 L629,421 L619,421 Z", "Vial cork",
       fill="#6A5238", stroke=INK, strokeWidth=2.5)
# hand wrapped around the vial's base
d.path(smooth([(610, 508), (606, 488), (614, 474), (628, 470), (640, 478),
               (642, 494), (636, 508), (624, 514), (614, 513)]),
       "Hand raised", fill=SKIN_GRAD, stroke=INK, strokeWidth=3.5)
for i, xx in enumerate([616, 626, 636]):
    d.path(f"M{xx},484 C{xx + 1},492 {xx + 1},500 {xx},506",
           f"Grip finger {i+1}", fill=NONE, stroke="#8A6248",
           strokeWidth=2.5, opacity=70, cap="round")
# radium sheen on the knuckles and cuff
d.path("M612,486 C618,478 630,476 638,480", "Knuckle sheen", fill=NONE,
       stroke=GLOW, strokeWidth=3, opacity=30, cap="round")
# two faint shimmer ticks off the vial tip
d.path("M604,404 C608,408 610,412 610,416", "Shimmer L", fill=NONE,
       stroke=GLOW, strokeWidth=3, opacity=45, cap="round")
d.path("M644,406 C641,410 640,414 640,418", "Shimmer R", fill=NONE,
       stroke=GLOW, strokeWidth=3, opacity=45, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#2A342E", strokeWidth=6)

# --- captions -------------------------------------------------------------------
d.text("MARIE CURIE", "Name", x=500, y=934, size=56, font="Virelai Sans",
       color="#E4ECE0", justify="center")
LINE2, SZ2, TRK = "RADIOACTIVITY · TWO NOBELS", 22, 280
r = d.text(LINE2, "Milestone", x=500, y=970, size=SZ2, font="Virelai Sans",
           color="#BCC8BC", justify="center")
d.cmd("text.setStyle", "Milestone tracking", id=r["id"], tracking=TRK)

b = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("milestone bounds", {k: round(v) for k, v in b.items()})
nearest = (min(max(PCX, b["x"]), b["x"] + b["width"]),
           min(max(PCY, b["y"]), b["y"] + b["height"]))
clear = math.hypot(nearest[0] - PCX, nearest[1] - PCY) - (PR + 3)
print("clears rim by %.1f" % clear)
assert clear > 0 and b["width"] <= 760 and b["x"] >= 10 and b["x"] + b["width"] <= 990, b

d.finish("marie-curie-V1R00")
