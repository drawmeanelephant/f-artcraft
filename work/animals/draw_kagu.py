#!/usr/bin/env python3
"""Kagu — field plate V1R00. Rhynochetos jubatus pausing on a shadowed
forest floor: pale powder-grey body lifted on red-orange legs, crest
partly raised, folded wing plain (no display pattern). A grounded
flightless bird among leaf litter. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Kagu — Field Plate", 1000, 1000)

INK = "#26201C"
CX, CY, R = 500, 460, 420

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

BG_GRAD    = lin(0, 0, 0, 1000, (0, "#151A12"), (1, "#070A06"))
PLATE_GRAD = rad((0, "#B2AB90"), (0.62, "#79735C"), (1, "#453F2C"))
BODY_GRAD  = rad((0, "#E4E9EE"), (0.55, "#BCC5CE"), (1, "#87919D"))
WING_GRAD  = lin(470, 470, 560, 620, (0, "#AEB8C2"), (1, "#6E7987"))
LEG_GRAD   = lin(520, 610, 520, 745, (0, "#D85830"), (1, "#8E2E18"))
BILL_GRAD  = lin(300, 440, 375, 460, (0, "#E06838"), (1, "#96301A"))
FLOOR_GRAD = lin(0, 715, 0, 880, (0, "#6E6850"), (1, "#322D1C"))

def on_disc(x, y, pad=10):
    return math.hypot(x - CX, y - CY) <= R - pad

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#2A2A1C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#DCD8BC", strokeWidth=3, opacity=26)
for i, (x, y, w, o) in enumerate([(200, 250, 9, 34), (770, 230, 7, 32), (165, 490, 8, 30),
                                  (825, 600, 9, 34), (310, 180, 7, 30), (640, 155, 8, 32),
                                  (235, 680, 7, 30), (770, 710, 8, 28), (430, 135, 6, 28),
                                  (150, 610, 6, 28), (855, 390, 7, 30), (560, 805, 7, 28)]):
    assert on_disc(x + w / 2, y + w / 2), (x, y)
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#4A4630", opacity=o, stroke=NONE)
# faint canopy light pool, upper left
d.shape("ellipse", "Light pool", x=190, y=150, width=380, height=190,
        fill="#E4E0C4", opacity=10, stroke=NONE)

# --- forest floor: leaf-litter chord closing on the disc arc --------------------
gy = 738
gdx = math.sqrt(R * R - (gy - CY) ** 2)
d.path(f"M{CX-gdx:.1f},{gy} C300,726 420,734 520,730 C620,726 715,732 {CX+gdx:.1f},{gy} "
       f"A{R},{R} 0 0 1 {CX-gdx:.1f},{gy} Z", "Forest floor", fill=FLOOR_GRAD, stroke=NONE)
# leaf litter: fallen leaves, husks, twigs — all small, inside the disc
leaves = [(268, 730, 24, -30, "#7A6248"), (336, 744, 18, 15, "#8E7A54"),
          (452, 748, 22, -10, "#6E5438"), (584, 746, 20, 25, "#8E7A54"),
          (668, 738, 24, -20, "#7A6248"), (740, 730, 18, 10, "#A88E5E"),
          (398, 726, 14, 40, "#A88E5E"), (508, 754, 16, -35, "#7A6248")]
for i, (x, y, w, rot, c) in enumerate(leaves):
    a = math.radians(rot)
    dx, dy = math.cos(a) * w / 2, math.sin(a) * w / 2
    nx, ny = -math.sin(a) * w / 6, math.cos(a) * w / 6
    d.path(f"M{x-dx:.0f},{y-dy:.0f} Q{x+nx:.0f},{y+ny:.0f} {x+dx:.0f},{y+dy:.0f} "
           f"Q{x-nx:.0f},{y-ny:.0f} {x-dx:.0f},{y-dy:.0f} Z",
           f"Fallen leaf {i+1}", fill=c, opacity=85, stroke=NONE)
for i, (x0, y0, x1, y1) in enumerate([(240, 748, 300, 736), (620, 752, 690, 744),
                                      (420, 736, 470, 730)]):
    d.path(f"M{x0},{y0} L{x1},{y1}", f"Twig {i+1}", fill=NONE, stroke="#3A2E1E",
           strokeWidth=4, opacity=80, cap="round")
d.shape("ellipse", "Kagu shadow", x=400, y=730, width=300, height=20,
        fill="#1C1A10", opacity=45, stroke=NONE)

# --- limbs --------------------------------------------------------------------
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

def toes(cx, y, label, color):
    """Grounded bird foot: three toes forward, one back, ≥4pt."""
    d.path(f"M{cx},{y-6} L{cx-26},{y+4} M{cx},{y-6} L{cx-14},{y+8} "
           f"M{cx},{y-6} L{cx-2},{y+9} M{cx+2},{y-6} L{cx+18},{y+2}",
           label, fill=NONE, stroke=color, strokeWidth=4.5, cap="round")

# far leg (behind the body, dimmer)
limb("Leg far", [(556, 596), (560, 655), (564, 700), (566, 726)], [18, 13, 10, 9],
     lin(520, 610, 520, 745, (0, "#96381E"), (1, "#60200F")),
     stroke=INK, strokeWidth=3)
toes(566, 732, "Toes far", "#8E2E18")

# short folded tail at the rear
d.path("M648,520 C672,536 686,560 688,586 C672,578 654,560 644,540 Z",
       "Tail", fill=WING_GRAD, stroke=INK, strokeWidth=4)

# --- body ----------------------------------------------------------------------
d.path("M430,520 C450,485 502,465 562,468 C612,470 646,490 655,522 "
       "C660,547 650,572 628,586 C588,610 520,620 470,610 "
       "C440,605 424,580 424,556 C424,540 426,528 430,520 Z",
       "Body", fill=BODY_GRAD, stroke=INK, strokeWidth=6)
# folded wing: plain closed wing, no display pattern
d.path("M470,500 C516,486 580,490 622,514 C636,524 640,540 632,554 "
       "C600,574 534,580 486,568 C462,552 458,524 470,500 Z",
       "Folded wing", fill=WING_GRAD, opacity=85, stroke=NONE)
d.path("M472,502 C518,488 578,492 618,514", "Wing edge light", fill=NONE,
       stroke="#DEE4EA", strokeWidth=4, opacity=50, cap="round")
d.path("M486,566 C532,576 596,572 630,556", "Wing lower edge", fill=NONE,
       stroke="#525E6C", strokeWidth=4, opacity=45, cap="round")
# breast fluff under the neck
d.path("M424,548 C420,572 428,594 446,606", "Breast edge", fill=NONE,
       stroke=INK, strokeWidth=4, opacity=40, cap="round")
d.path("M438,470 C478,460 534,458 580,466", "Back light", fill=NONE,
       stroke="#F0F4F8", strokeWidth=5, opacity=45, cap="round")

# --- near leg + toes ---------------------------------------------------------------
limb("Leg near", [(504, 596), (502, 655), (500, 702), (498, 728)], [20, 14, 10, 9],
     LEG_GRAD, stroke=INK, strokeWidth=3.5)
toes(498, 734, "Toes near", "#A83C20")
# leg feathering at the joint tops
d.path("M492,600 C498,624 500,648 498,672", "Near leg feather edge", fill=NONE,
       stroke="#8A94A0", strokeWidth=5, opacity=55, cap="round")

# --- neck + head ----------------------------------------------------------------------
d.path("M430,530 C414,512 402,486 396,458 C392,440 392,424 398,412 "
       "C404,400 416,392 430,390 C446,388 460,394 468,406 "
       "C476,418 476,434 470,448 C462,470 452,496 444,522 "
       "C439,534 433,536 430,530 Z",
       "Neck and head", fill=BODY_GRAD, stroke=INK, strokeWidth=5)

# --- crest: partly raised, loose fan of feathers swept back ----------------------------
CREST_B = (440, 402)
for i, ang in enumerate([-8, -26, -44, -62, -80]):
    a = math.radians(ang)
    ln = 78 - abs(i - 2) * 6
    tip = (CREST_B[0] + math.cos(a) * ln, CREST_B[1] + math.sin(a) * ln)
    mid = (CREST_B[0] + math.cos(a) * ln * 0.5, CREST_B[1] + math.sin(a) * ln * 0.55 - 8)
    d.path(f"M{CREST_B[0]},{CREST_B[1]} Q{mid[0]:.0f},{mid[1]:.0f} {tip[0]:.0f},{tip[1]:.0f}",
           f"Crest feather {i+1}", fill=NONE, stroke="#C4CCD6", strokeWidth=9,
           cap="round")
    d.path(f"M{CREST_B[0]},{CREST_B[1]} Q{mid[0]:.0f},{mid[1]:.0f} {tip[0]:.0f},{tip[1]:.0f}",
           f"Crest shaft {i+1}", fill=NONE, stroke="#6E7A88", strokeWidth=3.5,
           opacity=60, cap="round")

# --- bill + face ------------------------------------------------------------------------
# long, pointed, gently decurved orange-red bill
d.path("M398,418 C374,424 346,436 322,452 C312,459 306,464 304,470 "
       "C316,468 330,464 344,458 C362,450 380,440 396,432 Z",
       "Bill", fill=BILL_GRAD, stroke=INK, strokeWidth=4)
d.path("M398,428 C372,438 348,450 324,462", "Bill ridge", fill=NONE,
       stroke="#F08A58", strokeWidth=3.5, opacity=60, cap="round")
d.shape("ellipse", "Nostril", x=352, y=439, width=8, height=4, fill="#4E1A0E",
        opacity=70, stroke=NONE)
# eye: dark, alert, pale lore trace
d.shape("ellipse", "Eye", x=408, y=418, width=18, height=18, fill="#1E1410",
        stroke=INK, strokeWidth=2)
d.shape("ellipse", "Eye glint", x=412, y=421, width=5, height=5, fill="#F4EAD8",
        opacity=90, stroke=NONE)
d.path("M402,424 C398,428 396,432 396,436", "Lore shade", fill=NONE,
       stroke="#8A94A0", strokeWidth=4, opacity=50, cap="round")

# plate rim on top
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840, fill=NONE,
        stroke="#1E1E10", strokeWidth=6)

# --- name + second line --------------------------------------------------------
d.text("KAGU", "Name", x=500, y=934, size=60, font="Virelai Sans",
       color="#E4E2CE", justify="center")
LINE2, SZ2, TRK = "RHYNOCHETOS JUBATUS", 22, 240
r = d.text(LINE2, "Second line", x=500, y=968, size=SZ2, font="Virelai Sans",
           color="#AEA884", justify="center")
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

d.finish("kagu-V1R00")
