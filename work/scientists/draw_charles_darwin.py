#!/usr/bin/env python3
"""Charles Darwin — milestone card V1R00. The bearded elder: dark soft
hat over the dome, white fringe at the temples, the great beard flowing
over a dark coat; a small finch perched at the shoulder. Gentle and
observant, not a statue. Bust closes on the disc's own lower arc.
1000x1000. House style: gradients + translucent shading, never flat
fills. Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Charles Darwin — Milestone Card", 1000, 1000)

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


BG_GRAD = lin(0, 0, 0, 1000, (0, "#15150F"), (1, "#070705"))
PLATE_GRAD = rad((0, "#8B9078"), (0.5, "#505642"), (1, "#23271D"))
SKIN_GRAD = lin(425, 340, 505, 540, (0, "#E0C0A0"), (0.55, "#BE9A7C"), (1, "#8C6A50"))
SKIN_DIM = lin(425, 340, 505, 540, (0, "#BC9A7C"), (1, "#7A5A44"))
BEARD_GRAD = lin(430, 460, 520, 660, (0, "#EAE6D8"), (0.5, "#B6B09E"), (1, "#76705F"))
HAT_GRAD = lin(390, 230, 550, 360, (0, "#3E352A"), (0.55, "#241D15"), (1, "#110D09"))
COAT_GRAD = lin(300, 560, 700, 850, (0, "#413A2E"), (0.5, "#26201A"), (1, "#100C08"))
FINCH_GRAD = lin(560, 560, 630, 640, (0, "#C4A076"), (0.55, "#8E6C46"), (1, "#4C3824"))

# --- backdrop + sage plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#33382A", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E2E4CE", strokeWidth=3, opacity=34)

# thin light pooling upper-left
d.shape("ellipse", "Light pool", x=240, y=160, width=380, height=220,
        fill="#ECEFE0", opacity=11, stroke=NONE)
# a couple of mist lenses, kept out of the face zone
for i, (x, y, w) in enumerate([(680, 300, 80), (270, 560, 64), (740, 520, 60)]):
    assert on_disc(x, y, 20), i
    d.shape("ellipse", f"Mist {i+1}", x=x - w / 2, y=y - w / 5, width=w,
            height=w * 0.4, fill="#E0E4CE", opacity=10, stroke=NONE)

# --- the coat — bust silhouette closing on the disc's arc ----------------------------
fj = 802
jl, jr = rim_x(fj, -1), rim_x(fj, 1)
d.path(f"M{jl:.1f},{fj} C275,730 292,660 340,612 C380,578 418,566 444,560 "
       f"L496,560 C542,568 588,582 624,616 C664,656 690,724 {jr:.1f},{fj} "
       f"A{PR},{PR} 0 0 1 {jl:.1f},{fj} Z", "Coat",
       fill=COAT_GRAD, stroke=INK, strokeWidth=5)
# coat collar edges + lapel shadow
d.path("M436,564 L414,596 L448,612 Z", "Coat collar L",
       fill="#2C251C", stroke=INK, strokeWidth=3)
d.path("M504,564 L528,596 L494,612 Z", "Coat collar R",
       fill="#2C251C", stroke=INK, strokeWidth=3)
for i, dd in enumerate(["M368,634 C358,692 354,744 362,794",
                        "M566,632 C580,688 590,742 594,792"]):
    d.path(dd, f"Coat fold {i+1}", fill=NONE, stroke="#0E0A07",
           strokeWidth=4, opacity=45, cap="round")
d.path("M316,664 C350,624 396,594 438,580", "Shoulder sheen", fill=NONE,
       stroke="#6E6250", strokeWidth=5, opacity=30, cap="round")

# --- the beard — the signature, broad and full over the chest -------------------------
d.path(smooth([(406, 418), (412, 512), (420, 566), (430, 610), (442, 642),
               (460, 656), (480, 658), (498, 644), (510, 612), (518, 560),
               (521, 510), (526, 418), (514, 414), (486, 410), (446, 410),
               (416, 414)]), "Beard", fill=BEARD_GRAD, stroke=INK,
       strokeWidth=4)
# beard strand texture — long sweeps following the fall
for i, dd in enumerate([
        "M430,478 C434,530 444,580 456,620",
        "M466,470 C466,524 468,580 470,622",
        "M502,478 C500,530 492,580 482,618",
        "M418,520 C424,560 434,592 446,612",
        "M514,520 C510,558 502,590 492,610"]):
    d.path(dd, f"Beard strand {i+1}", fill=NONE, stroke="#F4F0E2",
           strokeWidth=3.5, opacity=40, cap="round")
# the mouth lives inside the beard: a soft shadow under the moustache
d.path("M448,478 C458,484 478,484 488,478", "Mouth shade", fill=NONE,
       stroke="#6E6252", strokeWidth=4, opacity=55, cap="round")

# --- head ---------------------------------------------------------------------------
# face under the hat brim — brow to upper cheeks, then the beard takes over
d.path(smooth([(468, 352), (518, 366), (523, 420), (512, 462), (494, 486),
               (468, 496), (442, 486), (424, 462), (413, 420), (418, 366)],
              k=0.85), "Face", fill=SKIN_GRAD, stroke=INK, strokeWidth=4)
# white temple locks — unstroked wedges bridging beard top to the brim,
# so they read as hair, not flaps
d.path("M402,358 L418,362 L420,424 L410,436 L398,428 L396,392 Z",
       "Temple lock L", fill="#B6B09E", stroke=NONE)
d.path("M534,358 L518,362 L516,424 L526,436 L538,428 L540,392 Z",
       "Temple lock R", fill="#B6B09E", stroke=NONE)

# the heavy brow ridge — one soft bar over both eyes
d.path("M424,404 C444,396 492,396 512,404 C494,412 442,412 424,404 Z",
       "Brow ridge", fill="#C4A284", opacity=55, stroke=NONE)
d.path("M426,400 C438,394 452,394 460,399", "Brow L", fill=NONE,
       stroke="#8A8478", strokeWidth=6, opacity=85, cap="round")
d.path("M478,399 C488,394 501,394 510,400", "Brow R", fill=NONE,
       stroke="#8A8478", strokeWidth=6, opacity=85, cap="round")
# deep-set gentle eyes
d.path("M430,418 C436,412 450,412 457,418 C450,424 436,424 430,418 Z",
       "Eye L", fill="#EDE2CC", stroke=INK, strokeWidth=3)
d.path("M481,418 C488,412 502,412 509,418 C502,424 488,424 481,418 Z",
       "Eye R", fill="#EDE2CC", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Iris L", x=440, y=412, width=10, height=11,
        fill="#33241A", stroke=NONE)
d.shape("ellipse", "Iris R", x=491, y=412, width=10, height=11,
        fill="#33241A", stroke=NONE)
d.shape("ellipse", "Glint L", x=443, y=414, width=3.2, height=3.2,
        fill="#FFF4DC", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=494, y=414, width=3.2, height=3.2,
        fill="#FFF4DC", opacity=90, stroke=NONE)
# socket shadows deepen the set
d.path("M428,430 C438,435 452,435 460,431", "Socket L", fill=NONE,
       stroke="#9A7658", strokeWidth=3, opacity=35, cap="round")
d.path("M480,431 C488,435 501,435 509,430", "Socket R", fill=NONE,
       stroke="#9A7658", strokeWidth=3, opacity=35, cap="round")
# broad elder nose
d.path("M470,424 C475,440 475,456 468,468", "Nose shade", fill=NONE,
       stroke="#9A7658", strokeWidth=4, opacity=45, cap="round")
d.path("M459,470 C465,474 475,474 481,469", "Nose base", fill=NONE,
       stroke="#8A6248", strokeWidth=3, opacity=55, cap="round")
# weathered cheek warm patch
d.shape("ellipse", "Cheek warm L", x=424, y=436, width=22, height=14,
        fill="#C08A6A", opacity=28, stroke=NONE)
d.shape("ellipse", "Cheek warm R", x=492, y=436, width=22, height=14,
        fill="#C08A6A", opacity=28, stroke=NONE)

# --- the hat — soft wide-awake, dark over the dome -----------------------------------
d.path("M398,338 C400,278 428,246 468,244 C508,246 536,280 538,338 Z",
       "Hat crown", fill=HAT_GRAD, stroke=INK, strokeWidth=4.5)
d.shape("ellipse", "Hat brim", x=348, y=320, width=244, height=38,
        fill=lin(348, 320, 592, 358, (0, "#3A3127"), (0.5, "#221B13"),
                 (1, "#120E0A")), stroke=INK, strokeWidth=4)
d.path("M360,336 C420,330 520,330 578,336", "Brim sheen", fill=NONE,
       stroke="#6E6250", strokeWidth=3, opacity=45, cap="round")

# --- the finch on his right shoulder --------------------------------------------------
# perched at the coat's right shoulder curve, facing him
d.path("M560,612 C566,600 584,594 598,600", "Perch shadow", fill=NONE,
       stroke="#0E0A07", strokeWidth=4, opacity=40, cap="round")
# body — plump oval tilted breast-forward
d.path(smooth([(586, 584), (566, 576), (552, 562), (548, 544), (556, 528),
               (572, 520), (588, 522), (600, 534), (602, 552), (598, 570)]),
       "Finch body", fill=FINCH_GRAD, stroke=INK, strokeWidth=3.5)
# wing patch + tail
d.path(smooth([(574, 540), (586, 534), (596, 542), (596, 558), (586, 568),
               (574, 562)]), "Finch wing", fill="#3E2E20", opacity=80,
       stroke=INK, strokeWidth=2.5)
d.path("M598,552 L624,566 L618,574 L594,564 Z", "Finch tail",
       fill="#4C3824", stroke=INK, strokeWidth=2.5)
# head + conical seed-eater beak
d.path(smooth([(548, 522), (560, 510), (574, 512), (582, 522), (580, 536),
               (570, 544), (556, 540), (548, 532)]), "Finch head",
       fill=lin(548, 510, 582, 544, (0, "#D0AA7E"), (1, "#7E5E3C")),
       stroke=INK, strokeWidth=3)
d.path("M548,526 L534,531 L548,536 Z", "Finch beak", fill="#3A2C1C",
       stroke=INK, strokeWidth=2.5)
d.shape("ellipse", "Finch eye", x=562, y=522, width=7, height=7,
        fill="#1E140E", stroke=NONE)
d.shape("ellipse", "Finch glint", x=564, y=523, width=2.5, height=2.5,
        fill="#FFF4DC", opacity=90, stroke=NONE)
# breast warm patch
d.path(smooth([(556, 544), (564, 540), (572, 546), (572, 558), (564, 566),
               (556, 560)]), "Finch breast", fill="#D8B184", opacity=70,
       stroke=NONE)
# two stick legs onto the shoulder
d.path("M568,584 L566,602 M580,586 L580,604", "Finch legs", fill=NONE,
       stroke="#3A2C1C", strokeWidth=3, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#2C3224", strokeWidth=6)

# --- captions -------------------------------------------------------------------------
d.text("CHARLES DARWIN", "Name", x=500, y=934, size=56, font="Virelai Sans",
       color="#ECEADB", justify="center")
LINE2, SZ2, TRK = "ORIGIN OF SPECIES · 1859", 22, 480
r = d.text(LINE2, "Milestone", x=500, y=970, size=SZ2, font=SS3,
           color="#C0C4AC", justify="center")
d.cmd("text.setStyle", "Milestone tracking", id=r["id"], tracking=TRK)

b = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("milestone bounds", {k: round(v) for k, v in b.items()})
nearest = (min(max(PCX, b["x"]), b["x"] + b["width"]),
           min(max(PCY, b["y"]), b["y"] + b["height"]))
clear = math.hypot(nearest[0] - PCX, nearest[1] - PCY) - (PR + 3)
print("clears rim by %.1f" % clear)
assert clear > 0 and b["width"] <= 760 and b["x"] >= 10 and b["x"] + b["width"] <= 990, b

d.finish("charles-darwin-V1R00")
