#!/usr/bin/env python3
"""Isaac Newton — milestone card V1R00. Baroque periwig — centre-parted
masses of curls to the shoulders — white cravat, dark velvet robe, seated
beside a small table where a single apple rests. A faint prism ray
splits in the upper dark. Sepia plate. Bust closes on the disc's own
lower arc; the table stands beside the robe. 1000x1000. House style:
gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Isaac Newton — Milestone Card", 1000, 1000)

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


BG_GRAD = lin(0, 0, 0, 1000, (0, "#171410"), (1, "#080604"))
PLATE_GRAD = rad((0, "#8A7E6A"), (0.5, "#524838"), (1, "#241D15"))
SKIN_GRAD = lin(420, 340, 500, 550, (0, "#E2C3A2"), (0.55, "#C29E80"), (1, "#906E54"))
SKIN_DIM = lin(420, 340, 500, 550, (0, "#C09E80"), (1, "#7E5E48"))
WIG_GRAD = lin(340, 270, 560, 620, (0, "#D4CFC0"), (0.5, "#9A9484"), (1, "#5C5648"))
WIG_LO = "#4C463C"
ROBE_GRAD = lin(300, 560, 700, 850, (0, "#4A3530"), (0.5, "#2A1B18"), (1, "#120B09"))
LINEN = lin(440, 560, 480, 640, (0, "#DCCFAE"), (1, "#968A6C"))

# --- backdrop + sepia plate ------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#382F24", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E4DAC0", strokeWidth=3, opacity=34)

# thin light pooling upper-left
d.shape("ellipse", "Light pool", x=230, y=150, width=380, height=220,
        fill="#F0E6CC", opacity=11, stroke=NONE)

# --- a faint prism ray splitting in the upper dark ---------------------------------
# the incident beam
d.path("M210,255 L634,238", "Prism beam in", fill=NONE, stroke="#F0EEDC",
       strokeWidth=4, opacity=16, cap="round")
# the little glass prism
d.path("M636,214 L666,258 L608,258 Z", "Prism", fill="#C8D8D8", opacity=30,
       stroke="#E8F0E8", strokeWidth=2.5)
# spectral fan off the far side
for i, (x1, y1, x2, y2, c, op) in enumerate([
        (655, 234, 792, 196, "#D88A6E", 14),
        (657, 240, 800, 224, "#D8C88A", 12),
        (658, 246, 796, 254, "#8AAE8E", 11)]):
    assert on_disc(x2, y2, 14), i
    d.path(f"M{x1},{y1} L{x2},{y2}", f"Spectrum {i+1}", fill=NONE,
           stroke=c, strokeWidth=4, opacity=op, cap="round")

# --- the robe — bust silhouette closing on the disc's arc ---------------------------
fj = 802
jl, jr = rim_x(fj, -1), rim_x(fj, 1)
d.path(f"M{jl:.1f},{fj} C275,730 292,660 340,612 C380,578 418,566 444,560 "
       f"L500,560 C546,568 592,582 628,616 C668,656 694,724 {jr:.1f},{fj} "
       f"A{PR},{PR} 0 0 1 {jl:.1f},{fj} Z", "Robe",
       fill=ROBE_GRAD, stroke=INK, strokeWidth=5)

# neck + the white cravat
d.path("M440,510 L440,562 C452,572 486,572 498,562 L498,510 Z", "Neck",
       fill=SKIN_DIM, stroke=INK, strokeWidth=3.5)
d.path(smooth([(446, 556), (458, 548), (482, 548), (494, 556), (492, 590),
               (484, 622), (470, 634), (456, 622), (448, 590)]), "Cravat",
       fill=LINEN, stroke=INK, strokeWidth=3.5)
d.path("M452,580 C460,584 480,584 488,580", "Cravat fold", fill=NONE,
       stroke="#968A6C", strokeWidth=3, opacity=55, cap="round")
# robe folds + shoulder sheen
for i, dd in enumerate(["M370,630 C360,690 356,744 364,796",
                        "M560,628 C574,686 584,740 588,792"]):
    d.path(dd, f"Robe fold {i+1}", fill=NONE, stroke="#140D0B",
           strokeWidth=4, opacity=45, cap="round")
d.path("M316,662 C350,622 396,592 436,578", "Shoulder sheen", fill=NONE,
       stroke="#8A7260", strokeWidth=5, opacity=30, cap="round")

# --- the periwig — centre part, curls to the shoulders ------------------------------
# back mass: crown plus two long falls framing the face
d.path(smooth([(356, 560), (336, 480), (340, 390), (368, 320), (412, 282),
               (452, 268), (492, 270), (530, 288), (556, 330), (570, 396),
               (572, 478), (560, 560), (530, 590), (506, 566), (508, 500),
               (500, 400), (438, 400), (432, 500), (432, 560), (404, 590),
               (372, 566)], k=0.85), "Wig mass", fill=WIG_GRAD,
       stroke=INK, strokeWidth=4.5)
# centre part at the crown
d.path("M465,272 C463,296 462,318 464,340", "Wig part", fill=NONE,
       stroke=WIG_LO, strokeWidth=4, opacity=70, cap="round")

# face — long, composed, clean-shaven
d.path(smooth([(465, 342), (516, 356), (521, 414), (508, 470), (490, 512),
               (465, 534), (440, 512), (422, 470), (409, 414), (414, 356)],
              k=0.85), "Face", fill=SKIN_GRAD, stroke=INK, strokeWidth=4)
# wig hairline over the high forehead
d.path("M410,392 C420,356 444,340 465,338 C488,340 512,358 521,394 "
       "C508,364 488,350 465,348 C442,350 420,364 410,392 Z",
       "Wig hairline", fill=WIG_GRAD, stroke=NONE)
# front lock tumbling over the right shoulder
d.path(smooth([(506, 380), (534, 420), (548, 480), (552, 540), (546, 586),
               (530, 606), (512, 596), (506, 550), (504, 490), (498, 430)],
              k=0.9), "Front lock", fill=WIG_GRAD, stroke=INK,
       strokeWidth=4)
# ringlet texture — C-curves along the falls
for i, (x, y, flip) in enumerate([
        (356, 420, 1), (352, 470, 1), (358, 520, 1), (378, 350, 1),
        (555, 425, -1), (560, 475, -1), (555, 525, -1), (540, 340, -1),
        (520, 585, -1), (382, 575, 1), (420, 300, 1), (505, 300, -1)]):
    s = 22 * flip
    d.path(f"M{x},{y} c{s * 0.4:.0f},{-14} {s:.0f},{-4} {s * 0.9:.0f},{10}",
           f"Curl {i+1}", fill=NONE, stroke="#E8E2D0", strokeWidth=3.5,
           opacity=45, cap="round")
# deeper grooves between the falls
for i, dd in enumerate(["M372,400 C362,460 364,520 376,566",
                        "M545,405 C553,462 552,520 542,562"]):
    d.path(dd, f"Wig groove {i+1}", fill=NONE, stroke=WIG_LO,
           strokeWidth=4, opacity=50, cap="round")

# features — level, composed
d.path("M425,402 C436,396 450,396 458,401", "Brow L", fill=NONE,
       stroke="#4C4034", strokeWidth=4.5, opacity=75, cap="round")
d.path("M476,401 C486,396 499,396 508,402", "Brow R", fill=NONE,
       stroke="#4C4034", strokeWidth=4.5, opacity=75, cap="round")
d.path("M427,418 C434,411 449,411 456,418 C449,425 434,425 427,418 Z",
       "Eye L", fill="#EFE4D0", stroke=INK, strokeWidth=3)
d.path("M478,418 C485,411 500,411 507,418 C500,425 485,425 478,418 Z",
       "Eye R", fill="#EFE4D0", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Iris L", x=438, y=412, width=11, height=12,
        fill="#2E221A", stroke=NONE)
d.shape("ellipse", "Iris R", x=489, y=412, width=11, height=12,
        fill="#2E221A", stroke=NONE)
d.shape("ellipse", "Glint L", x=441, y=414, width=3.5, height=3.5,
        fill="#FFF4DC", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=492, y=414, width=3.5, height=3.5,
        fill="#FFF4DC", opacity=90, stroke=NONE)
# long nose, level mouth
d.path("M468,426 C473,442 473,458 466,470", "Nose shade", fill=NONE,
       stroke="#9A7658", strokeWidth=3.5, opacity=45, cap="round")
d.path("M458,472 C464,476 474,476 480,471", "Nose base", fill=NONE,
       stroke="#8A6248", strokeWidth=3, opacity=55, cap="round")
d.path("M446,490 C456,495 476,495 486,490", "Mouth", fill=NONE,
       stroke="#7A4A3A", strokeWidth=4, opacity=75, cap="round")
d.path("M452,502 C462,506 472,506 480,502", "Lip shade", fill=NONE,
       stroke="#9A6248", strokeWidth=3, opacity=38, cap="round")
d.path("M416,440 C419,460 427,478 439,488", "Cheek shade", fill=NONE,
       stroke="#9A7658", strokeWidth=5, opacity=22, cap="round")

# --- the side table + one apple ------------------------------------------------------
# tabletop bar + one leg, beside the robe's right edge
d.path("M610,742 L742,742 L736,757 L614,757 Z", "Tabletop",
       fill=lin(610, 742, 742, 757, (0, "#5C4A32"), (1, "#241A10")),
       stroke=INK, strokeWidth=3.5)
d.path("M616,744 L738,744", "Table sheen", fill=NONE, stroke="#8A724E",
       strokeWidth=2.5, opacity=50, cap="round")
d.path("M668,757 L684,757 L680,812 L672,812 Z", "Table leg",
       fill="#2A1F14", stroke=INK, strokeWidth=3)
assert on_disc(680, 812, 6)
# the apple — single, honest, sitting on the top
d.path(smooth([(674, 700), (660, 694), (650, 704), (652, 720), (662, 732),
               (676, 736), (688, 730), (694, 718), (692, 702), (682, 694)]),
       "Apple", fill=rad((0, "#C05A44"), (0.65, "#8A3626"), (1, "#521E14")),
       stroke=INK, strokeWidth=3.5)
d.path("M674,700 C673,694 674,689 677,685", "Stem", fill=NONE,
       stroke="#3A2A1A", strokeWidth=3.5, cap="round")
d.path("M677,690 C686,684 694,684 700,690 C692,694 684,694 677,690 Z",
       "Leaf", fill="#5E6E42", stroke=INK, strokeWidth=2.5)
d.path("M660,706 C664,700 672,697 678,698", "Apple sheen", fill=NONE,
       stroke="#E8A88E", strokeWidth=3, opacity=55, cap="round")
# apple shadow on the table
d.shape("ellipse", "Apple shadow", x=656, y=730, width=44, height=8,
        fill="#120C08", opacity=45, stroke=NONE)

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#322A20", strokeWidth=6)

# --- captions -----------------------------------------------------------------------
d.text("ISAAC NEWTON", "Name", x=500, y=934, size=56, font="Virelai Sans",
       color="#EDE6D4", justify="center")
LINE2, SZ2, TRK = "PRINCIPIA · 1687", 22, 520
r = d.text(LINE2, "Milestone", x=500, y=970, size=SZ2, font=SS3,
           color="#C4BBA4", justify="center")
d.cmd("text.setStyle", "Milestone tracking", id=r["id"], tracking=TRK)

b = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("milestone bounds", {k: round(v) for k, v in b.items()})
nearest = (min(max(PCX, b["x"]), b["x"] + b["width"]),
           min(max(PCY, b["y"]), b["y"] + b["height"]))
clear = math.hypot(nearest[0] - PCX, nearest[1] - PCY) - (PR + 3)
print("clears rim by %.1f" % clear)
assert clear > 0 and b["width"] <= 760 and b["x"] >= 10 and b["x"] + b["width"] <= 990, b

d.finish("isaac-newton-V1R00")
