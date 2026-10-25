#!/usr/bin/env python3
"""Katherine Johnson — milestone card V1R00. Standing three-quarter at a
chalkboard-dark plate, chalk raised mid-stroke on an orbital arc, a sheaf
of trajectory figures in the other hand. 1960s NASA-era dress, cat-eye
glasses, short dark hair, composed smile. The equations are the backdrop
texture — orbit arcs, a dotted transfer, one ghosted conic formula. She
stands on a floor band closed on the disc's own arc. 1000x1000. House
style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Katherine Johnson — Milestone Card", 1000, 1000)

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


BG_GRAD = lin(0, 0, 0, 1000, (0, "#131A18"), (1, "#060908"))
PLATE_GRAD = rad((0, "#5E7060"), (0.5, "#3A4A42"), (1, "#1B2420"))
SKIN_GRAD = lin(440, 300, 540, 560, (0, "#B98A66"), (0.55, "#96684C"), (1, "#64462F"))
SKIN_DIM = lin(440, 300, 540, 560, (0, "#9A7154"), (1, "#5A3E2C"))
STOCK_GRAD = lin(0, 705, 0, 790, (0, "#A87C60"), (1, "#74543E"))
HAIR_GRAD = lin(430, 230, 570, 420, (0, "#4A3628"), (0.5, "#2A1C12"), (1, "#120A06"))
DRESS_GRAD = lin(380, 500, 620, 720, (0, "#4E6663"), (0.5, "#2C3E3B"), (1, "#131C1A"))
DRESS_DIM = lin(380, 500, 620, 720, (0, "#3A504D"), (1, "#101817"))
FLOOR_GRAD = lin(0, 792, 0, 880, (0, "#3C342A"), (0.55, "#241E16"), (1, "#100C08"))
PAPER_GRAD = lin(615, 620, 668, 672, (0, "#D8CCAE"), (1, "#94876C"))
CHALK = "#DCE6DC"

# --- backdrop + chalkboard plate -------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#2B352F", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8E4DA", strokeWidth=3, opacity=34)

# thin light pooling upper-left
d.shape("ellipse", "Light pool", x=245, y=145, width=390, height=225,
        fill="#E0EADD", opacity=11, stroke=NONE)
# mist lenses — kept clear of the face zone
for i, (x, y, w) in enumerate([(285, 520, 66), (705, 315, 78), (250, 645, 60),
                               (735, 520, 70), (430, 615, 58)]):
    assert on_disc(x, y, 18), i
    d.shape("ellipse", f"Mist {i+1}", x=x - w / 2, y=y - w / 5, width=w,
            height=w * 0.4, fill="#DCE8DC", opacity=10, stroke=NONE)

# --- the board: orbital arcs + ghosted figures, all faint -------------------------
# orbit arc she is working — the raised chalk meets its lower-left leg
d.path("M296,358 C320,282 430,238 545,258 C605,269 633,306 620,348",
       "Orbit arc", fill=NONE, stroke=CHALK, strokeWidth=3.5, opacity=18,
       cap="round")
# a second, higher transfer ellipse, dotted
d.path("M368,300 C430,228 558,192 668,232", "Transfer arc", fill=NONE,
       stroke=CHALK, strokeWidth=3, opacity=14, cap="round", dash=[7, 9])
# Earth — the small body the arcs swing around
d.shape("ellipse", "Earth", x=358, y=290, width=20, height=20,
        fill=CHALK, opacity=22, stroke=CHALK, strokeWidth=3)
# a higher chalk arc upper-right with a capsule dot riding it
d.path("M598,208 C668,182 756,198 778,252", "Orbit high", fill=NONE,
       stroke=CHALK, strokeWidth=3.5, opacity=15, cap="round")
d.shape("ellipse", "Capsule", x=770, y=243, width=12, height=12,
        fill=CHALK, opacity=35, stroke=NONE)
# ghosted conic formula + worked figures, Source Sans 3 (digits live here)
r = d.text("x²/a² + y²/b² = 1", "Chalk formula", x=650, y=205, size=20,
           font=SS3, color=CHALK, justify="center")
d.cmd("object.setProps", "Chalk formula fade", id=r["id"], opacity=15)
for i, (x1, y1, x2, y2) in enumerate([(618, 258, 668, 254), (684, 262, 716, 258),
                                      (252, 415, 300, 410), (258, 440, 288, 436)]):
    assert on_disc(x1, y1, 12) and on_disc(x2, y2, 12), i
    d.path(f"M{x1},{y1} L{x2},{y2}", f"Chalk dash {i+1}", fill=NONE,
           stroke=CHALK, strokeWidth=3, opacity=12, cap="round")

# --- floor band she stands on — closes on the disc's own arc ----------------------
fy = 800
fl, fr = rim_x(fy, -1), rim_x(fy, 1)
d.path(f"M{fl:.1f},{fy} C350,786 650,786 {fr:.1f},{fy} "
       f"A{PR},{PR} 0 0 1 {fl:.1f},{fy} Z", "Floor", fill=FLOOR_GRAD,
       stroke=NONE)
d.path(f"M{fl + 8:.0f},{fy} C350,786 650,786 {fr - 8:.0f},{fy}",
       "Floor crest", fill=NONE, stroke="#7A6A50", strokeWidth=5,
       opacity=38, cap="round")

# contact shadow under the shoes
d.shape("ellipse", "Shoe shadow", x=432, y=788, width=140, height=22,
        fill="#0E0B08", opacity=45, stroke=NONE)

# --- legs + shoes ------------------------------------------------------------------
# stockinged calves under the knee hem
d.path(smooth([(458, 700), (454, 738), (452, 766), (458, 782), (476, 782),
               (480, 748), (484, 700)], k=0.8), "Calf L",
       fill=STOCK_GRAD, stroke=INK, strokeWidth=3.5)
d.path(smooth([(516, 700), (518, 748), (522, 782), (540, 782), (546, 766),
               (544, 738), (540, 700)], k=0.8), "Calf R",
       fill=STOCK_GRAD, stroke=INK, strokeWidth=3.5)
# low 1960s pumps
d.path(smooth([(448, 780), (444, 792), (452, 800), (482, 800), (490, 792),
               (486, 780), (468, 776)], k=0.9), "Shoe L",
       fill="#241A12", stroke=INK, strokeWidth=3)
d.path(smooth([(514, 780), (516, 792), (522, 800), (552, 800), (560, 792),
               (556, 780), (532, 776)], k=0.9), "Shoe R",
       fill="#241A12", stroke=INK, strokeWidth=3)

# --- the dress — knee-length A-line, short sleeves ---------------------------------
d.path(smooth([(398, 708), (416, 646), (436, 592), (426, 548), (408, 505),
               (446, 490), (554, 490), (592, 505), (574, 548), (564, 592),
               (584, 646), (602, 708), (500, 718)], k=0.9), "Dress",
       fill=DRESS_GRAD, stroke=INK, strokeWidth=5)
# sleeve caps
d.path(smooth([(408, 505), (396, 520), (392, 545), (400, 562), (418, 560),
               (428, 540), (430, 518)], k=0.9), "Sleeve L",
       fill=DRESS_DIM, stroke=INK, strokeWidth=4)
# waist seam + skirt folds
d.path("M434,596 C478,606 522,606 566,596", "Waist seam", fill=NONE,
       stroke="#101817", strokeWidth=4, opacity=50, cap="round")
for i, dd in enumerate([
        "M452,610 C448,644 444,676 442,704",
        "M500,614 C500,648 500,680 500,708",
        "M548,610 C552,644 556,676 558,704"]):
    d.path(dd, f"Skirt fold {i+1}", fill=NONE, stroke="#101817",
           strokeWidth=4, opacity=42, cap="round")
d.path("M414,512 C452,496 548,496 586,512", "Shoulder sheen", fill=NONE,
       stroke="#7E9490", strokeWidth=5, opacity=30, cap="round")

# neck + peter-pan collar + button placket
d.path("M484,446 L484,500 C492,507 508,507 516,500 L516,446 Z", "Neck",
       fill=SKIN_DIM, stroke=INK, strokeWidth=3.5)
d.path(smooth([(462, 502), (482, 491), (500, 497), (518, 491), (538, 502),
               (532, 524), (500, 515), (468, 524)], k=0.9), "Collar",
       fill=lin(462, 491, 538, 524, (0, "#D8CCB0"), (1, "#968A6E")),
       stroke=INK, strokeWidth=3.5)
d.path("M500,524 L500,592", "Placket", fill=NONE, stroke="#101817",
       strokeWidth=3, opacity=55, cap="round")
for i, yy in enumerate([536, 558, 580]):
    d.shape("ellipse", f"Button {i+1}", x=497.5, y=yy, width=5, height=5,
            fill="#C8BC9E", opacity=85, stroke=NONE)

# --- raised right arm — chalk to the board -----------------------------------------
# short sleeve over the shoulder, then the bare forearm lifting to the arc
d.path(smooth([(412, 500), (386, 478), (362, 462), (346, 458), (338, 470),
               (348, 488), (376, 510), (402, 522)], k=0.9),
       "Sleeve raised", fill=DRESS_GRAD, stroke=INK, strokeWidth=4)
d.path(smooth([(342, 474), (326, 448), (314, 420), (310, 402), (322, 392),
               (336, 404), (348, 432), (358, 458)], k=0.9), "Forearm",
       fill=SKIN_GRAD, stroke=INK, strokeWidth=3.5)
# fist around the chalk stick
d.path(smooth([(306, 398), (302, 382), (310, 368), (324, 366), (334, 376),
               (334, 392), (326, 402), (314, 402)], k=0.9), "Hand raised",
       fill=SKIN_GRAD, stroke=INK, strokeWidth=3.5)
for i, xx in enumerate([312, 321]):
    d.path(f"M{xx},380 C{xx + 1},387 {xx + 1},393 {xx},398",
           f"Grip finger {i+1}", fill=NONE, stroke="#7A5238",
           strokeWidth=2.5, opacity=70, cap="round")
# the chalk stick, tip meeting the orbit arc; the fresh stroke is brighter
d.path("M310,378 L296,358", "Chalk stick", fill=NONE, stroke="#F2F6F0",
       strokeWidth=4, opacity=95, cap="round")
d.path("M296,358 C306,346 318,336 332,328", "Fresh chalk", fill=NONE,
       stroke=CHALK, strokeWidth=4, opacity=50, cap="round")
d.shape("ellipse", "Chalk dust", x=291, y=352, width=10, height=10,
        fill=CHALK, opacity=30, stroke=NONE)

# --- lowered left arm — sheaf of figures at the hip ---------------------------------
d.path(smooth([(590, 502), (606, 524), (618, 556), (626, 586), (620, 600),
               (606, 596), (596, 566), (588, 534)], k=0.9), "Sleeve low",
       fill=DRESS_DIM, stroke=INK, strokeWidth=4)
d.path(smooth([(618, 592), (622, 616), (626, 638), (636, 646), (646, 640),
               (642, 618), (636, 596)], k=0.9), "Forearm low",
       fill=SKIN_DIM, stroke=INK, strokeWidth=3.5)
# papers — a small sheaf of hand-computed tables
d.path("M622,624 L672,634 L664,676 L614,666 Z", "Papers back",
       fill=PAPER_GRAD, stroke=INK, strokeWidth=3)
d.path("M626,618 L676,628 L668,670 L618,660 Z", "Papers front",
       fill=lin(618, 618, 676, 670, (0, "#E4D8B8"), (1, "#A89A78")),
       stroke=INK, strokeWidth=3)
for i, (y1, y2) in enumerate([(634, 640), (644, 650), (654, 660)]):
    d.path(f"M632,{y1} L662,{y2}", f"Table line {i+1}", fill=NONE,
           stroke="#6A5E48", strokeWidth=2.5, opacity=60, cap="round")
# hand curled over the sheaf's top edge
d.path(smooth([(630, 622), (640, 616), (652, 618), (656, 628), (650, 636),
               (638, 634), (630, 630)], k=0.9), "Hand low",
       fill=SKIN_GRAD, stroke=INK, strokeWidth=3.5)

# --- head -----------------------------------------------------------------------------
# hair mass — short, neat 1960s cap with a slight flip at the sides
d.path(smooth([(444, 394), (426, 354), (428, 300), (444, 258), (480, 234),
               (522, 234), (556, 256), (572, 298), (574, 352), (556, 394),
               (548, 384), (452, 384)], k=0.9), "Hair mass",
       fill=HAIR_GRAD, stroke=INK, strokeWidth=4)
# face — broad forehead, soft round cheeks, composed
d.path(smooth([(500, 292), (548, 312), (558, 368), (542, 420), (500, 450),
               (458, 420), (442, 368), (452, 312)], k=0.85), "Face",
       fill=SKIN_GRAD, stroke=INK, strokeWidth=4)
# ears — small bumps peeking from the hair
d.path("M438,352 C430,358 430,374 440,380", "Ear L", fill=NONE,
       stroke=INK, strokeWidth=3.5, cap="round")
d.path("M562,352 C570,358 570,374 560,380", "Ear R", fill=NONE,
       stroke=INK, strokeWidth=3.5, cap="round")
# hairline — side-parted band over the forehead
d.path("M450,340 C456,300 478,282 500,282 C526,282 546,302 550,342 "
       "C540,312 522,298 500,297 C478,298 460,314 450,340 Z",
       "Hairline", fill=HAIR_GRAD, stroke=NONE)
for i, dd in enumerate(["M482,288 C468,296 456,310 450,326",
                        "M486,286 C506,292 524,306 536,324",
                        "M540,300 C548,312 552,324 554,336"]):
    d.path(dd, f"Hair wave {i+1}", fill=NONE, stroke="#6E5240",
           strokeWidth=3.5, opacity=50, cap="round")
# soft cheek shades
d.path("M452,398 C456,416 464,430 476,438", "Cheek shade L", fill=NONE,
       stroke="#7A5238", strokeWidth=5, opacity=25, cap="round")
d.path("M548,398 C544,416 536,430 524,438", "Cheek shade R", fill=NONE,
       stroke="#7A5238", strokeWidth=5, opacity=25, cap="round")

# brows — level, attentive, just above the frames
d.path("M456,346 C466,340 480,340 488,345", "Brow L", fill=NONE,
       stroke="#2E2015", strokeWidth=4, opacity=75, cap="round")
d.path("M512,345 C520,340 534,340 544,346", "Brow R", fill=NONE,
       stroke="#2E2015", strokeWidth=4, opacity=75, cap="round")
# cat-eye glasses — the iconic frames, upswept at the outer corners
d.path(smooth([(452, 358), (466, 348), (490, 352), (497, 361), (495, 375),
               (479, 384), (461, 380)], k=0.85), "Frame L", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.path(smooth([(548, 358), (534, 348), (510, 352), (503, 361), (505, 375),
               (521, 384), (539, 380)], k=0.85), "Frame R", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.path("M496,362 C498,359 502,359 504,362", "Bridge", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.path("M452,358 L440,352", "Temple L", fill=NONE, stroke=INK,
       strokeWidth=3.5, cap="round")
d.path("M548,358 L560,352", "Temple R", fill=NONE, stroke=INK,
       strokeWidth=3.5, cap="round")
d.path("M460,360 L470,355", "Lens sheen L", fill=NONE, stroke="#F2F6F0",
       strokeWidth=3, opacity=30, cap="round")
d.path("M512,360 L522,355", "Lens sheen R", fill=NONE, stroke="#F2F6F0",
       strokeWidth=3, opacity=30, cap="round")
# eyes behind the lenses
d.path("M462,370 C468,364 480,364 486,370 C480,376 468,376 462,370 Z",
       "Eye L", fill="#EFE0C8", stroke=INK, strokeWidth=3)
d.path("M514,370 C520,364 532,364 538,370 C532,376 520,376 514,370 Z",
       "Eye R", fill="#EFE0C8", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Iris L", x=470, y=365, width=10, height=11,
        fill="#2A1B10", stroke=NONE)
d.shape("ellipse", "Iris R", x=520, y=365, width=10, height=11,
        fill="#2A1B10", stroke=NONE)
d.shape("ellipse", "Glint L", x=472.5, y=367, width=3, height=3,
        fill="#FFF4DC", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=522.5, y=367, width=3, height=3,
        fill="#FFF4DC", opacity=90, stroke=NONE)
# nose + the small composed smile
d.path("M503,380 C507,394 507,406 500,414", "Nose shade", fill=NONE,
       stroke="#8A5E42", strokeWidth=3.5, opacity=45, cap="round")
d.path("M493,415 C498,418 505,418 510,415", "Nose base", fill=NONE,
       stroke="#7A4E36", strokeWidth=3, opacity=55, cap="round")
d.path("M474,426 C488,434 512,434 526,425", "Mouth", fill=NONE,
       stroke="#7A4436", strokeWidth=4.5, opacity=85, cap="round")
d.path("M482,436 C492,440 508,440 518,436", "Lip shade", fill=NONE,
       stroke="#9A5C48", strokeWidth=3, opacity=40, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#26302A", strokeWidth=6)

# --- captions ----------------------------------------------------------------------
d.text("KATHERINE JOHNSON", "Name", x=500, y=934, size=56,
       font="Virelai Sans", color="#E4ECE0", justify="center")
LINE2, SZ2, TRK = "ORBITAL MATH · 1962", 22, 500
r = d.text(LINE2, "Milestone", x=500, y=970, size=SZ2, font=SS3,
           color="#BCCABB", justify="center")
d.cmd("text.setStyle", "Milestone tracking", id=r["id"], tracking=TRK)

b = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("milestone bounds", {k: round(v) for k, v in b.items()})
nearest = (min(max(PCX, b["x"]), b["x"] + b["width"]),
           min(max(PCY, b["y"]), b["y"] + b["height"]))
clear = math.hypot(nearest[0] - PCX, nearest[1] - PCY) - (PR + 3)
print("clears rim by %.1f" % clear)
assert clear > 0 and b["width"] <= 760 and b["x"] >= 10 and b["x"] + b["width"] <= 990, b

d.finish("katherine-johnson-V1R00")
