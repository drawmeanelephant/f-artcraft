#!/usr/bin/env python3
"""Vicuna — field plate V1R00. Wild Vicugna vicugna standing in profile on
a sparse puna ledge, head turned slightly toward us. Long fine neck and
legs, tawny back over a pale bib and underside; dusk violet behind warm
wool highlights. Slender and alert, never shaggy. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Vicuna — Field Plate", 1000, 1000)

INK = "#241828"
CX, CY, R = 500, 460, 420

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

BG_GRAD    = lin(0, 0, 0, 1000, (0, "#1C1626"), (1, "#090613"))
PLATE_GRAD = rad((0, "#A89DB9"), (0.62, "#766A8C"), (1, "#443B54"))
COAT_GRAD  = lin(500, 300, 500, 575, (0, "#C08B52"), (0.55, "#96683A"), (1, "#654424"))
COAT_FAR   = lin(500, 300, 500, 575, (0, "#8E6238"), (1, "#4C321A"))
LEG_GRAD   = lin(430, 550, 430, 740, (0, "#966B3E"), (1, "#6E4B28"))
LEG_FAR    = lin(430, 550, 430, 740, (0, "#6E4E2C"), (1, "#453016"))
GROUND_GRAD = lin(0, 730, 0, 880, (0, "#867590"), (1, "#3E3246"))
PALE = "#EBDCC0"

def on_disc(x, y, pad=10):
    return math.hypot(x - CX, y - CY) <= R - pad

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#322A40", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E2DAEE", strokeWidth=3, opacity=26)
for i, (x, y, w, o) in enumerate([(200, 250, 9, 34), (770, 230, 7, 32), (165, 490, 8, 30),
                                  (825, 600, 9, 34), (310, 180, 7, 30), (640, 155, 8, 32),
                                  (235, 680, 7, 30), (770, 710, 8, 28), (430, 135, 6, 28),
                                  (150, 610, 6, 28), (855, 390, 7, 30), (560, 805, 7, 28)]):
    assert on_disc(x + w / 2, y + w / 2), (x, y)
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#4E4460", opacity=o, stroke=NONE)

# --- distant altiplano: low flat-topped ridge behind the legs -------------------
d.path("M150,660 L300,648 L340,656 L520,644 L560,652 L700,646 L850,654 L850,700 L150,700 Z",
       "Mesa ridge", fill="#4E4462", opacity=45, stroke=NONE)
# --- puna ledge: sparse chord closing on the disc arc ---------------------------
gy = 740
gdx = math.sqrt(R * R - (gy - CY) ** 2)
d.path(f"M{CX-gdx:.1f},{gy} C300,730 420,737 520,733 C620,729 715,735 {CX+gdx:.1f},{gy} "
       f"A{R},{R} 0 0 1 {CX-gdx:.1f},{gy} Z", "Puna ledge", fill=GROUND_GRAD, stroke=NONE)
# sparse ichu grass tufts — thin, pale straw
for i, (x, s) in enumerate([(235, 1), (315, -1), (545, 1), (690, -1), (775, 1)]):
    d.path(f"M{x},{gy-3} Q{x+3*s},{gy-20} {x+8*s},{gy-28} "
           f"M{x+7*s},{gy-3} Q{x+11*s},{gy-16} {x+16*s},{gy-22}",
           f"Ichu tuft {i+1}", fill=NONE, stroke="#B8A888", strokeWidth=4,
           opacity=55, cap="round")
d.shape("ellipse", "Vicuna shadow", x=340, y=732, width=340, height=20,
        fill="#241C2E", opacity=40, stroke=NONE)

# --- limbs ----------------------------------------------------------------------
def limb(label, pts, widths, fill, **kw):
    n = len(pts)
    L, Rr = [], []
    for i in range(n):
        ax, ay = pts[max(i - 1, 0)]
        bx, by = pts[min(i + 1, n - 1)]
        dx, dy = bx - ax, by - ay
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy / ln, dx / ln
        w = widths[i] / 2
        L.append((pts[i][0] + nx * w, pts[i][1] + ny * w))
        Rr.append((pts[i][0] - nx * w, pts[i][1] - ny * w))
    dd = "M%.1f,%.1f " % L[0]
    for i in range(1, n):
        mx, my = (L[i-1][0] + L[i][0]) / 2, (L[i-1][1] + L[i][1]) / 2
        dd += "Q%.1f,%.1f %.1f,%.1f " % (L[i-1][0], L[i-1][1], mx, my) if i > 1 else "L%.1f,%.1f " % (mx, my)
    dd += "L%.1f,%.1f L%.1f,%.1f " % (L[-1] + Rr[-1])
    for i in range(n - 2, -1, -1):
        dd += "L%.1f,%.1f " % Rr[i]
    d.path(dd + "Z", label, fill=fill, **kw)

def hoof(cx, y, label):
    d.path(f"M{cx-9},{y} L{cx+9},{y} L{cx+7},{y+7} C{cx+3},{y+9} {cx-3},{y+9} {cx-7},{y+7} Z",
           label, fill="#1E1216", stroke=NONE)

# far legs (behind the body, slightly offset)
limb("Leg far front", [(446, 545), (450, 620), (452, 690), (453, 726)], [22, 15, 12, 10],
     LEG_FAR, stroke=INK, strokeWidth=3)
limb("Leg far hind", [(612, 545), (608, 625), (604, 692), (602, 728)], [24, 16, 12, 10],
     LEG_FAR, stroke=INK, strokeWidth=3)
hoof(453, 726, "Hoof far front")
hoof(602, 728, "Hoof far hind")

# short tail tuft at the rump
d.path("M632,486 C650,492 658,506 656,522 C648,516 638,508 630,500 Z",
       "Tail", fill=COAT_FAR, stroke=INK, strokeWidth=3)

# --- torso ----------------------------------------------------------------------
d.path("M428,474 C480,462 552,462 602,470 C622,474 634,490 636,508 "
       "C638,524 632,538 620,546 C590,560 520,564 468,560 "
       "C444,558 426,552 416,540 C406,526 406,508 412,492 "
       "C416,482 421,477 428,474 Z",
       "Body", fill=COAT_GRAD, stroke=INK, strokeWidth=5)
# pale belly + inner-leg flash
d.path("M430,548 C480,556 560,556 610,548 C590,562 540,568 492,566 "
       "C462,564 442,558 430,548 Z",
       "Belly pale", fill=PALE, opacity=60, stroke=NONE)

# --- neck + head: one silhouette, long and slender -------------------------------
d.path("M352,312 "                                   # poll
       "C378,350 406,414 428,480 "                   # nape to withers
       "C422,502 414,524 406,544 "                   # into chest
       "C399,540 393,528 389,512 "                   # chest front
       "C383,478 373,440 359,402 "                   # throat rising
       "C351,380 341,366 331,356 "                   # to jaw
       "C319,349 307,348 297,351 "                   # jaw to muzzle underside
       "C289,352 285,355 285,358 "                   # muzzle tip
       "C285,351 287,346 293,341 "                   # tip top
       "C301,332 313,321 327,315 "                   # forehead
       "C335,310 345,309 352,312 Z",
       "Neck and head", fill=COAT_GRAD, stroke=INK, strokeWidth=5)

# cream bib: long apron hair on the chest front and throat underside
d.path("M340,372 C352,398 364,430 376,468 C386,500 394,524 400,544 "
       "C392,554 380,556 372,548 C362,530 354,500 346,468 "
       "C338,436 334,404 334,382 Z",
       "Chest bib", fill=PALE, opacity=70, stroke=NONE)
# bib hair fringe
for i, (x, y, ln) in enumerate([(368, 470, 26), (378, 505, 24), (386, 528, 20),
                                (356, 428, 22), (348, 400, 18)]):
    d.path(f"M{x},{y} Q{x-3},{y+ln/2} {x-4},{y+ln}", f"Bib fringe {i+1}",
           fill=NONE, stroke=PALE, strokeWidth=4, opacity=50, cap="round")

# --- near legs ----------------------------------------------------------------------
limb("Leg near front", [(424, 545), (422, 625), (420, 692), (419, 728)], [24, 17, 13, 11],
     LEG_GRAD, stroke=INK, strokeWidth=3.5)
limb("Leg near hind", [(588, 545), (584, 625), (580, 692), (578, 728)], [26, 17, 13, 11],
     LEG_GRAD, stroke=INK, strokeWidth=3.5)
# pale inner-leg flash
d.path("M426,600 L422,700", "Front leg pale", fill=NONE, stroke=PALE,
       strokeWidth=4, opacity=40, cap="round")
d.path("M584,600 L580,700", "Hind leg pale", fill=NONE, stroke=PALE,
       strokeWidth=4, opacity=40, cap="round")
hoof(419, 728, "Hoof near front")
hoof(578, 728, "Hoof near hind")

# --- ears + face (head turned slightly toward us) ------------------------------------
# far ear, smaller, peeking behind the poll
d.path("M366,318 C368,296 374,278 384,264 C388,282 386,300 378,318 Z",
       "Ear far", fill=COAT_FAR, stroke=INK, strokeWidth=3)
# near ear: long, pointed, upright
d.path("M344,312 C340,286 340,262 348,240 C358,258 362,282 358,310 Z",
       "Ear near", fill=COAT_GRAD, stroke=INK, strokeWidth=4)
d.path("M349,302 C347,284 348,268 352,256", "Ear near inner", fill=NONE,
       stroke="#4A3018", strokeWidth=4, opacity=60, cap="round")

# eye — near eye plus the faintest hint of the far one
d.shape("ellipse", "Eye near", x=322, y=330, width=15, height=14, fill="#1E1208",
        stroke=INK, strokeWidth=2)
d.shape("ellipse", "Eye glint", x=326, y=333, width=4, height=4, fill="#F4E8D2",
        opacity=90, stroke=NONE)
d.shape("ellipse", "Eye far", x=352, y=328, width=9, height=8, fill="#1E1208",
        opacity=70, stroke=NONE)
# nostril + mouth at the muzzle tip
d.shape("ellipse", "Nostril", x=287, y=349, width=7, height=5, fill="#160C06",
        opacity=80, stroke=NONE)
d.path("M286,356 C294,358 302,358 310,356", "Mouth", fill=NONE, stroke=INK,
       strokeWidth=4, opacity=60, cap="round")
# warm wool highlights
d.path("M356,318 C382,356 406,418 424,476", "Nape light", fill=NONE,
       stroke="#E4BC84", strokeWidth=5, opacity=45, cap="round")
d.path("M434,478 C486,468 552,468 600,476", "Back rim light", fill=NONE,
       stroke="#E4BC84", strokeWidth=5, opacity=40, cap="round")
d.path("M300,342 C310,332 322,322 334,316", "Face light", fill=NONE,
       stroke="#E4BC84", strokeWidth=4, opacity=40, cap="round")

# plate rim on top
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840, fill=NONE,
        stroke="#241C30", strokeWidth=6)

# --- name + second line --------------------------------------------------------
d.text("VICUÑA", "Name", x=500, y=942, size=58, font="Virelai Sans",
       color="#E4DEEE", justify="center")
LINE2, SZ2, TRK = "VICUGNA VICUGNA", 22, 260
r = d.text(LINE2, "Second line", x=500, y=968, size=SZ2, font="Virelai Sans",
           color="#A89CBC", justify="center")
d.cmd("text.setStyle", "Second line tracking", id=r["id"], tracking=TRK)
def find(o, oid):
    if isinstance(o, dict):
        if o.get("id") == oid and "bounds" in o: return o
        o = list(o.values())
    if isinstance(o, list):
        for v in o:
            hit = find(v, oid)
            if hit: return hit
b2 = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("second line bounds", {k: round(v) for k, v in b2.items()})
assert b2["width"] <= 760 and b2["x"] >= 100 and b2["y"] + b2["height"] <= 990, b2

d.finish("vicuna-V1R00")
