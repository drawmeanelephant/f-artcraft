#!/usr/bin/env python3
"""Alan Turing — milestone card V1R00. A young man at a desk, a spool of
punched paper tape running through his hands; modest suit, abstracted
machine cabinets and dials in the dark behind. The desk slab is a chord
band; the under-desk wedge closes on the disc's own lower arc.
1000x1000. House style: gradients + translucent shading, never flat
fills. Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Alan Turing — Milestone Card", 1000, 1000)

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


BG_GRAD = lin(0, 0, 0, 1000, (0, "#0F131A"), (1, "#05070B"))
PLATE_GRAD = rad((0, "#66727F"), (0.5, "#3C4550"), (1, "#171D26"))
SKIN_GRAD = lin(420, 310, 510, 540, (0, "#E4C4A0"), (0.55, "#C09A78"), (1, "#8A6850"))
SKIN_DIM = lin(420, 310, 510, 540, (0, "#C09E80"), (1, "#7C5E46"))
HAIR_GRAD = lin(410, 270, 520, 420, (0, "#4C3822"), (0.5, "#2C1E10"), (1, "#140D07"))
SUIT_GRAD = lin(330, 560, 670, 760, (0, "#45423A"), (0.5, "#262219"), (1, "#12100C"))
SHIRT_GRAD = lin(440, 560, 500, 740, (0, "#E0D8C2"), (1, "#968C74"))
DESK_GRAD = lin(0, 730, 0, 790, (0, "#4E3E2A"), (0.6, "#2E2417"), (1, "#171208"))
TAPE = "#DCD0B0"
TAPE_DIM = "#B4A888"
MACHINE = "#A8B4BE"

# --- backdrop + steel-blue plate ------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#28303C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D2D9E2", strokeWidth=3, opacity=34)

# dim light pooling upper-left
d.shape("ellipse", "Light pool", x=230, y=150, width=380, height=220,
        fill="#E2E6EE", opacity=9, stroke=NONE)

# --- the machine in the dark — abstracted cabinets and dials ----------------------
# rounded cabinet masses behind his right shoulder
d.path("M612,206 L788,206 Q806,206 806,224 L806,420 Q806,438 788,438 "
       "L612,438 Q594,438 594,420 L594,224 Q594,206 612,206 Z",
       "Cabinet", fill=MACHINE, opacity=10, stroke=MACHINE,
       strokeWidth=3)
d.path("M560,150 L654,150 Q668,150 668,164 L668,340 Q668,354 654,354 "
       "L560,354 Q546,354 546,340 L546,164 Q546,150 560,150 Z",
       "Cabinet far", fill=MACHINE, opacity=8, stroke=MACHINE,
       strokeWidth=3)
# dials and a paper-tape loop hinted on the near cabinet
for i, (cx, cy, r) in enumerate([(672, 268, 26), (748, 262, 18),
                                 (700, 330, 14)]):
    assert on_disc(cx + r, cy, 10), i
    d.shape("ellipse", f"Dial {i+1}", x=cx - r, y=cy - r, width=r * 2,
            height=r * 2, fill=NONE, stroke=MACHINE, strokeWidth=3,
            opacity=16)
d.path("M676,262 L672,282", "Dial needle 1", fill=NONE, stroke=MACHINE,
       strokeWidth=2.5, opacity=18, cap="round")
d.path("M746,258 L756,268", "Dial needle 2", fill=NONE, stroke=MACHINE,
       strokeWidth=2.5, opacity=18, cap="round")
for i, (x, y) in enumerate([(632, 388), (664, 388), (696, 388), (728, 388),
                            (760, 388)]):
    d.shape("ellipse", f"Lamp {i+1}", x=x - 4, y=y - 4, width=8, height=8,
            fill=MACHINE, opacity=16, stroke=NONE)
# faint hanging tape-loop silhouette on the far cabinet
d.path("M588,180 C572,230 572,290 588,330 C598,300 598,210 588,180 Z",
       "Ghost tape", fill=MACHINE, opacity=10, stroke=NONE)

# --- the suit — modest, seated low behind the desk --------------------------------
d.path(smooth([(318, 760), (330, 690), (348, 626), (386, 588), (430, 566),
               (452, 558), (494, 558), (536, 570), (576, 598), (604, 646),
               (616, 700), (620, 760)], k=0.9), "Suit",
       fill=SUIT_GRAD, stroke=INK, strokeWidth=5)
# lapels + shirt + tie — the same grammar as the other cards
d.path("M408,562 L452,558 L470,600 L458,690 L428,640 Z", "Lapel L",
       fill=lin(408, 560, 458, 690, (0, "#38342C"), (1, "#16130E")),
       stroke=INK, strokeWidth=4)
d.path("M496,558 L530,568 L522,690 L484,600 Z", "Lapel R",
       fill=lin(496, 560, 522, 690, (0, "#332F27"), (1, "#14110C")),
       stroke=INK, strokeWidth=4)
d.path("M452,564 L492,564 L478,700 L462,700 Z", "Shirt front",
       fill=SHIRT_GRAD, stroke=INK, strokeWidth=3.5)
# dark tie — a slim 1930s knot and blade
d.path(smooth([(458, 560), (472, 554), (488, 560), (484, 578), (472, 584),
               (460, 578)]), "Tie knot",
       fill=lin(458, 554, 488, 584, (0, "#3A2E3E"), (1, "#181220")),
       stroke=INK, strokeWidth=3.5)
d.path("M466,584 L458,660 L474,692 L486,658 Z", "Tie blade",
       fill="#241C2C", stroke=INK, strokeWidth=3, opacity=90)
# soft collar wings
d.path("M430,548 L458,540 L472,560 L452,574 L432,566 Z", "Collar L",
       fill=SHIRT_GRAD, stroke=INK, strokeWidth=3.5)
d.path("M472,560 L486,540 L514,548 L512,566 L490,574 Z", "Collar R",
       fill=SHIRT_GRAD, stroke=INK, strokeWidth=3.5)
# neck
d.path("M452,500 L452,546 C460,554 482,554 490,546 L490,500 Z", "Neck",
       fill=SKIN_DIM, stroke=INK, strokeWidth=3.5)

# --- head: young, clean-shaven, side-parted short hair ------------------------------
# hair — neat crop, parted his right, close to the skull
d.path(smooth([(408, 430), (398, 380), (402, 332), (424, 298), (458, 282),
               (496, 290), (518, 318), (524, 364), (518, 416), (508, 438),
               (500, 412), (504, 366), (498, 326), (480, 302), (458, 296),
               (436, 304), (420, 330), (414, 372), (416, 414)], k=0.85),
       "Hair", fill=HAIR_GRAD, stroke=INK, strokeWidth=3.5)
# parting + comb lines off it
d.path("M486,298 C480,320 478,344 480,366", "Parting R", fill=NONE,
       stroke="#150D06", strokeWidth=3, opacity=70, cap="round")
for i, dd in enumerate(["M430,330 C444,312 462,302 480,300",
                        "M424,364 C438,340 458,326 478,324"]):
    d.path(dd, f"Comb {i+1}", fill=NONE, stroke="#6E5232",
           strokeWidth=3, opacity=45, cap="round")

# face — younger, fuller cheeks than the Tesla long-jaw
d.path(smooth([(460, 304), (502, 322), (510, 380), (504, 442), (490, 490),
               (472, 514), (458, 520), (444, 514), (426, 490), (412, 442),
               (406, 380), (414, 322)], k=0.85), "Face",
       fill=SKIN_GRAD, stroke=INK, strokeWidth=4)
# ears
d.path("M404,404 C398,408 396,422 402,434 C406,440 412,438 414,430",
       "Ear L", fill=SKIN_DIM, stroke=INK, strokeWidth=3)
d.path("M508,406 C514,410 516,424 510,434", "Ear R", fill=SKIN_DIM,
       stroke=INK, strokeWidth=3, opacity=90)

# features — open eyes dropped a touch toward the tape
d.path("M420,392 C431,386 445,385 455,391", "Brow L", fill=NONE,
       stroke="#40301E", strokeWidth=4.5, opacity=80, cap="round")
d.path("M465,391 C476,385 489,386 498,392", "Brow R", fill=NONE,
       stroke="#40301E", strokeWidth=4.5, opacity=80, cap="round")
d.path("M423,413 C430,406 445,406 452,412 C445,419 430,419 423,413 Z",
       "Eye L", fill="#EFE4D0", stroke=INK, strokeWidth=3)
d.path("M466,412 C473,405 487,405 494,411 C487,418 473,418 466,412 Z",
       "Eye R", fill="#EFE4D0", stroke=INK, strokeWidth=3)
# irises low — reading the tape below
d.shape("ellipse", "Iris L", x=437, y=410, width=10, height=10,
        fill="#2E221A", stroke=NONE)
d.shape("ellipse", "Iris R", x=480, y=409, width=10, height=10,
        fill="#2E221A", stroke=NONE)
d.shape("ellipse", "Glint L", x=440, y=412, width=3.2, height=3.2,
        fill="#FFF4DC", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=483, y=411, width=3.2, height=3.2,
        fill="#FFF4DC", opacity=90, stroke=NONE)
# nose — straight, younger, shorter
d.path("M460,414 C465,430 466,446 461,458", "Nose shade", fill=NONE,
       stroke="#9A7658", strokeWidth=3.5, opacity=45, cap="round")
d.path("M453,460 C459,464 469,464 475,459", "Nose base", fill=NONE,
       stroke="#8A6248", strokeWidth=3, opacity=55, cap="round")
d.path("M414,430 C418,450 424,466 434,478", "Cheek shade", fill=NONE,
       stroke="#9A7658", strokeWidth=5, opacity=22, cap="round")
# mouth — the slight asymmetric half-smile
d.path("M444,490 C454,496 470,496 480,489", "Mouth", fill=NONE,
       stroke="#6E4638", strokeWidth=3.5, opacity=75, cap="round")

# --- the desk — surface slab on a chord, shadow wedge closing on the arc -----------
fy1, fy2 = 736, 764
sl1, sr1 = rim_x(fy1, -1), rim_x(fy1, 1)
sl2, sr2 = rim_x(fy2, -1), rim_x(fy2, 1)
# desktop surface — the slab's top face seen edge-on
d.path(f"M{sl1:.1f},{fy1} C380,{fy1 - 14} 620,{fy1 - 14} {sr1:.1f},{fy1} "
       f"L{sr2:.1f},{fy2} C620,{fy2 - 12} 380,{fy2 - 12} {sl2:.1f},{fy2} Z",
       "Desktop", fill=DESK_GRAD, stroke=INK, strokeWidth=4)
# under-desk shadow wedge closing on the disc's arc
d.path(f"M{sl2:.1f},{fy2} C380,{fy2 - 12} 620,{fy2 - 12} {sr2:.1f},{fy2} "
       f"A{PR},{PR} 0 0 1 {sl2:.1f},{fy2} Z", "Under desk",
       fill=lin(0, fy2, 0, 880, (0, "#1C1710"), (1, "#0B0805")),
       stroke=NONE)

# --- the spool — a reel on a stand, feeding tape right -----------------------------
RX, RY, RR2 = 336, 668, 44
# stand strut to the desktop
d.path(f"M{RX - 5},{RY + RR2 - 6} L{RX + 5},{RY + RR2 - 6} L{RX + 8},736 "
       f"L{RX - 8},736 Z", "Reel stand", fill="#2A2620", stroke=INK,
       strokeWidth=3)
# reel — wound tape as concentric rings
d.shape("ellipse", "Reel", x=RX - RR2, y=RY - RR2, width=RR2 * 2,
        height=RR2 * 2,
        fill=rad((0, "#8A7C62"), (0.6, "#6A5E48"), (1, "#3E3626")),
        stroke=INK, strokeWidth=4)
for i, r in enumerate((33, 23)):
    d.shape("ellipse", f"Reel wound {i+1}", x=RX - r, y=RY - r,
            width=r * 2, height=r * 2, fill=NONE, stroke="#4E4634",
            strokeWidth=3, opacity=70)
d.shape("ellipse", "Reel hub", x=RX - 10, y=RY - 10, width=20, height=20,
        fill=rad((0, "#B08C50"), (1, "#5C4420")), stroke=INK,
        strokeWidth=3)

# --- the tape — punched band from reel through both hands, draping right -----------
# one parametric run: reel tangent -> grip L -> grip R -> drape off desk
def tape_seg(p0, p1, c0, c1, tag):
    d.path(f"M{p0[0]},{p0[1] - 11} C{c0[0]},{c0[1] - 11} {c1[0]},"
           f"{c1[1] - 11} {p1[0]},{p1[1] - 11} L{p1[0]},{p1[1] + 11} "
           f"C{c1[0]},{c1[1] + 11} {c0[0]},{c0[1] + 11} {p0[0]},"
           f"{p0[1] + 11} Z", tag, fill=TAPE, stroke=INK, strokeWidth=3)


GL_, GR_ = (432, 686), (576, 686)
# reel exit -> left hand
tape_seg((RX + 38, RY - 14), GL_, (RX + 60, RY - 30), (GL_[0] - 40, GL_[1] - 16),
         "Tape A")
# hand to hand — a shallow sag
tape_seg(GL_, GR_, (GL_[0] + 46, GL_[1] + 26), (GR_[0] - 46, GR_[1] + 26),
         "Tape B")
# right hand -> drape down over the desk
tape_seg(GR_, (690, 782), (GR_[0] + 52, GR_[1] + 10), (672, 726), "Tape C")
d.path("M690,771 C700,792 700,812 688,824 C682,806 682,788 690,771 Z",
       "Tape tail", fill=TAPE_DIM, stroke=INK, strokeWidth=3)

# punch marks — two rows of dots and square symbols along each segment
def marks(p0, p1, n, tag, phase=0):
    for i in range(1, n + 1):
        t = i / (n + 1)
        x = p0[0] + (p1[0] - p0[0]) * t
        y = p0[1] + (p1[1] - p0[1]) * t
        for s in (-5, 5):
            d.shape("ellipse", f"{tag} mark {i}",
                    x=x - 1.8, y=y + s - 1.8, width=3.6, height=3.6,
                    fill="#4A3C24", stroke=NONE)
        if (i + phase) % 3 == 0:
            d.path(f"M{x - 3},{y - 3} L{x + 3},{y - 3} L{x + 3},{y + 3} "
                   f"L{x - 3},{y + 3} Z", f"{tag} sym {i}", fill="#6A5836",
                   stroke=NONE)


marks((RX + 44, RY - 16), (GL_[0] - 4, GL_[1]), 3, "A")
marks((GL_[0] + 16, GL_[1] + 8), (GR_[0] - 16, GR_[1] + 8), 4, "B", 1)
marks((GR_[0] + 20, GR_[1] + 6), (676, 736), 3, "C", 2)

# hands — fists the tape visibly passes through
for lbl, (hx, hy) in (("Hand L", GL_), ("Hand R", GR_)):
    d.path(smooth([(hx - 16, hy - 10), (hx - 6, hy - 24),
                   (hx + 12, hy - 24), (hx + 20, hy - 12),
                   (hx + 18, hy + 10), (hx + 4, hy + 18),
                   (hx - 12, hy + 14)]), lbl, fill=SKIN_GRAD, stroke=INK,
           strokeWidth=3.5)
    d.path(f"M{hx - 8},{hy + 4} L{hx + 12},{hy + 1}", f"{lbl} knuckle",
           fill=NONE, stroke="#8A6248", strokeWidth=2.5, opacity=70,
           cap="round")

# cuffs — white shirt cuffs at each wrist
for i, (cx, cy) in enumerate([(GL_[0] - 6, GL_[1] + 24),
                              (GR_[0] - 4, GR_[1] + 24)]):
    d.path(f"M{cx - 16},{cy} L{cx + 16},{cy - 4} L{cx + 18},{cy + 8} "
           f"L{cx - 14},{cy + 12} Z", f"Cuff {i+1}", fill=SHIRT_GRAD,
           stroke=INK, strokeWidth=3)

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#242E3A", strokeWidth=6)

# --- captions ---------------------------------------------------------------------
d.text("ALAN TURING", "Name", x=500, y=934, size=56, font="Virelai Sans",
       color="#E8ECE8", justify="center")
LINE2, SZ2, TRK = "TURING MACHINE · 1936", 22, 480
r = d.text(LINE2, "Milestone", x=500, y=970, size=SZ2, font=SS3,
           color="#BCC4CC", justify="center")
d.cmd("text.setStyle", "Milestone tracking", id=r["id"], tracking=TRK)

b = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("milestone bounds", {k: round(v) for k, v in b.items()})
nearest = (min(max(PCX, b["x"]), b["x"] + b["width"]),
           min(max(PCY, b["y"]), b["y"] + b["height"]))
clear = math.hypot(nearest[0] - PCX, nearest[1] - PCY) - (PR + 3)
print("clears rim by %.1f" % clear)
assert clear > 0 and b["width"] <= 760 and b["x"] >= 10 and b["x"] + b["width"] <= 990, b

d.finish("alan-turing-V1R00")
