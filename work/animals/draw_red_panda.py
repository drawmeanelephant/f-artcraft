#!/usr/bin/env python3
"""Red panda — field-guide plate V1R00. Rust and cream on a mossy limb in the
cloud forest: the body a low loaf, the face front with its white mask, rust
tear-streaks and pale brow-spots, and the ringed tail swept forward along the
branch like a second scarf. Mist bands and bamboo at the rim. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Red Panda — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420          # plate disc centre + radius
INK = "#241108"

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def on_disc(x, y, pad=0):
    return math.hypot(x - CX, y - CY) <= R - pad

def quad(p0, p1, p2, t):
    u = 1 - t
    return (u*u*p0[0] + 2*u*t*p1[0] + t*t*p2[0],
            u*u*p0[1] + 2*u*t*p1[1] + t*t*p2[1])

def ribbon_pts(p0, p1, p2, w0, w1, n=20):
    """Edge points of a tapered strip along a quadratic."""
    L, Rr = [], []
    for k in range(n + 1):
        t = k / n
        x, y = quad(p0, p1, p2, t)
        x0, y0 = quad(p0, p1, p2, max(0, t - 0.01))
        x1, y1 = quad(p0, p1, p2, min(1, t + 0.01))
        dx, dy = x1 - x0, y1 - y0
        ln = math.hypot(dx, dy) or 1
        w = (w0 + (w1 - w0) * t) / 2
        L.append((x - dy/ln * w, y + dx/ln * w))
        Rr.append((x + dy/ln * w, y - dx/ln * w))
    return L, Rr

def ribbon(p0, p1, p2, w0, w1, label, n=20, **kw):
    L, Rr = ribbon_pts(p0, p1, p2, w0, w1, n)
    s = "M%.1f,%.1f " % L[0] + " ".join("L%.1f,%.1f" % p for p in L[1:])
    s += " " + " ".join("L%.1f,%.1f" % p for p in reversed(Rr)) + " Z"
    return d.path(s, label, **kw)

BG_GRAD = lin(0, 0, 0, 1000, (0, "#0C1A1C"), (1, "#04090A"))
PLATE_GRAD = rad((0, "#D4DED8"), (0.55, "#9CB0A6"), (1, "#557065"))
RUST = lin(500, 330, 520, 640, (0, "#C87238"), (0.5, "#A8521F"), (1, "#72300F"))
DARKFUR = "#3A2014"
BARK = lin(500, 580, 500, 720, (0, "#7A6248"), (1, "#46301E"))

# --- backdrop + cloud-forest plate ------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#9CB0A6", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#35493F", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E4EEE6", strokeWidth=3, opacity=45)

# deep foliage silhouettes at the rim's edge
d.shape("ellipse", "Foliage L", x=70, y=250, width=200, height=360,
        fill="#3E5648", opacity=32, stroke=NONE)
d.shape("ellipse", "Foliage R", x=770, y=300, width=170, height=330,
        fill="#3E5648", opacity=30, stroke=NONE)
# soft canopy glow behind the branch line
d.shape("ellipse", "Canopy glow", x=260, y=150, width=480, height=380,
        fill=rad((0, "#E9F0E8"), (1, "#E9F0E8")), opacity=38, stroke=NONE)
# mist bands drifting through
d.shape("ellipse", "Mist 1", x=150, y=430, width=700, height=80,
        fill="#EDF3EC", opacity=24, stroke=NONE)
d.shape("ellipse", "Mist 2", x=230, y=510, width=560, height=56,
        fill="#EDF3EC", opacity=17, stroke=NONE)

# --- bamboo at the rim ---------------------------------------------------------------
def bamboo_stalk(x, y0, y1, w, label):
    d.path(f"M{x},{y0} L{x + 8},{y1}", f"{label} stalk", fill=NONE,
           stroke="#4E6E50", strokeWidth=w, cap="round")
    n = max(2, int(abs(y1 - y0) / 110))
    for k in range(1, n + 1):
        yk = y0 + (y1 - y0) * k / (n + 1)
        xk = x + 8 * k / (n + 1)
        d.path(f"M{xk - w},{yk} L{xk + w + 2},{yk}", f"{label} node {k}",
               fill=NONE, stroke="#7A9A6C", strokeWidth=w * 0.5, cap="round")

def bamboo_leaf(cx, cy, ln, deg, label, color="#5C8060"):
    a = math.radians(deg)
    ux, uy = math.cos(a), math.sin(a)
    nx, ny = -uy, ux
    tip = (cx + ux * ln, cy + uy * ln)
    s = ("M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f Q%.1f,%.1f %.1f,%.1f Z" % (
        cx, cy, cx + ux*ln*0.5 + nx*ln*0.16, cy + uy*ln*0.5 + ny*ln*0.16,
        tip[0], tip[1], cx + ux*ln*0.5 - nx*ln*0.16, cy + uy*ln*0.5 - ny*ln*0.16, cx, cy))
    return d.path(s, label, fill=color, opacity=85, stroke=NONE)

bamboo_stalk(172, 120, 560, 9, "Bamboo L")
for k, (cx, cy, ln, deg) in enumerate([(172,150,58,160),(174,215,54,205),(176,285,60,150),
                                       (178,360,50,200),(180,430,55,150),(182,500,48,205)]):
    bamboo_leaf(cx, cy, ln, deg, f"Bamboo L leaf {k+1}")
bamboo_stalk(830, 150, 520, 8, "Bamboo R")
for k, (cx, cy, ln, deg) in enumerate([(832,180,52,25),(834,255,58,-15),(836,330,50,30),
                                       (837,410,46,-10),(838,480,42,30)]):
    bamboo_leaf(cx, cy, ln, deg, f"Bamboo R leaf {k+1}", color="#547860")

# --- the mossy limb -------------------------------------------------------------------
ribbon((132, 676), (505, 628), (908, 594), 84, 58, "Limb",
       fill=BARK, stroke=INK, strokeWidth=5)
# moss cushions riding the top edge of the bark
for i, (x, y, w) in enumerate([(230, 640, 60), (330, 632, 46), (640, 600, 55),
                               (760, 592, 44), (480, 616, 40)]):
    d.shape("ellipse", f"Moss {i+1}", x=x, y=y, width=w, height=w * 0.45,
            fill="#7A9E5C", opacity=75, stroke=NONE)
d.path("M240,672 C420,646 620,626 860,606", "Bark grain", fill=NONE,
       stroke="#5E4630", strokeWidth=4, opacity=45, cap="round")
# the sitter's shadow on the bark
d.shape("ellipse", "Loaf shadow", x=330, y=590, width=360, height=46,
        fill="#2E1E10", opacity=30, stroke=NONE)

# === the red panda ====================================================================
# --- the ringed tail swept forward like a scarf -----------------------------------------
TP0, TP1, TP2 = (648, 548), (722, 664), (424, 668)
TL, TR = ribbon_pts(TP0, TP1, TP2, 66, 42, n=24)
# base tail shape
s = "M%.1f,%.1f " % TL[0] + " ".join("L%.1f,%.1f" % p for p in TL[1:])
s += " " + " ".join("L%.1f,%.1f" % p for p in reversed(TR)) + " Z"
d.path(s, "Tail", fill=lin(648, 548, 424, 668, (0, "#B8602C"), (1, "#8A3E16")),
       stroke=INK, strokeWidth=5)
# dark rings across the tail — five bands stepping to the tip
for k, t in enumerate([0.14, 0.30, 0.46, 0.62, 0.78, 0.92]):
    i = round(t * 24)
    j = min(24, i + 2)
    band = "M%.1f,%.1f L%.1f,%.1f L%.1f,%.1f L%.1f,%.1f Z" % (
        TL[i][0], TL[i][1], TR[i][0], TR[i][1], TR[j][0], TR[j][1],
        TL[j][0], TL[j][1])
    d.path(band, f"Tail ring {k+1}", fill="#5E2810", opacity=80, stroke=NONE)
# pale guard hairs along the tail's outer sweep
d.path("M660,570 C700,626 640,676 560,684", "Tail rim light", fill=NONE,
       stroke="#E8C898", strokeWidth=6, opacity=40, cap="round")
# tail tip cream
tp = quad(TP0, TP1, TP2, 1.0)
d.shape("ellipse", "Tail tip", x=tp[0]-20, y=tp[1]-18, width=40, height=36,
        fill="#E8D4B0", opacity=85, stroke=INK, strokeWidth=3)
assert on_disc(722, 664, 20) and on_disc(424, 668, 20)

# --- body: the rust loaf on the limb ---------------------------------------------------
d.path("M392,470 C420,432 500,415 575,430 C640,443 685,470 700,505 "
       "C712,534 708,568 690,590 C670,612 620,624 555,626 "
       "C480,628 400,620 368,598 C342,580 336,548 348,520 "
       "C358,496 372,478 392,470 Z", "Body", fill=RUST, stroke=INK, strokeWidth=5)
# dark belly line along the branch
d.path("M370,588 C430,608 560,614 660,600 C630,620 480,630 400,612 "
       "C378,606 368,598 370,588 Z", "Belly dark", fill=DARKFUR, opacity=85, stroke=NONE)
# rust back highlight
d.path("M410,458 C470,432 560,430 630,452", "Back light", fill=NONE,
       stroke="#E8A060", strokeWidth=9, opacity=45, cap="round")
# flank mottle
for i, (x, y, w) in enumerate([(430,520,22),(500,540,18),(560,510,20),(610,540,16),(460,560,14)]):
    d.shape("ellipse", f"Flank fleck {i+1}", x=x, y=y, width=w, height=w * 0.7,
            fill="#7E3614", opacity=30, stroke=NONE)

# --- dangling forepaws over the bark's front edge ----------------------------------------
for i, (x, y, w) in enumerate([(430, 588, 34), (580, 596, 32)]):
    d.path(f"M{x},{y} C{x-4},{y+22} {x-2},{y+38} {x+6},{y+48} "
           f"C{x+12},{y+54} {x+22},{y+50} {x+24},{y+40} "
           f"C{x+26},{y+26} {x+22},{y+10} {x+18},{y-4} Z",
           f"Forepaw {i+1}", fill=DARKFUR, stroke=INK, strokeWidth=3)
    for j in range(3):
        d.path(f"M{x + 6 + j*6},{y + 44} l2,6", f"Paw {i+1} toe {j+1}", fill=NONE,
               stroke="#1A0E08", strokeWidth=2, cap="round")

# --- head: the white mask face, front -----------------------------------------------------
# ear triangles first so the head overlaps their base
def ear(cx, cy, r, lean, label):
    tipx = cx + lean
    d.path(f"M{cx - r},{cy + r*0.7} Q{cx - r},{cy - r*0.2} {tipx},{cy - r} "
           f"Q{cx + r},{cy - r*0.2} {cx + r},{cy + r*0.7} Z",
           f"{label} ear", fill=rad((0, "#C87238"), (1, "#7E3414")),
           stroke=INK, strokeWidth=5)
    d.path(f"M{cx - r*0.55},{cy + r*0.5} Q{cx - r*0.5},{cy} {tipx},{cy - r*0.5} "
           f"Q{cx + r*0.5},{cy} {cx + r*0.55},{cy + r*0.5} Z",
           f"{label} ear inner", fill="#F0E2CC", opacity=85, stroke=NONE)
ear(365, 322, 52, -10, "L")
ear(503, 326, 52, 10, "R")

# skull: broad wedge with a low chin
d.path("M434,318 C492,318 540,346 552,392 C562,432 552,468 520,486 "
       "C490,502 420,504 388,488 C352,470 336,436 342,398 "
       "C348,356 384,318 434,318 Z", "Head",
       fill=lin(445, 318, 445, 504, (0, "#B85A26"), (1, "#8A3E16")),
       stroke=INK, strokeWidth=5)
# the cream mask: cheeks, muzzle and brow field in one
d.path("M446,352 C492,352 522,376 528,412 C534,446 520,474 492,486 "
       "C464,496 418,494 392,480 C366,466 356,440 362,412 "
       "C368,382 402,352 446,352 Z", "Mask",
       fill=rad((0, "#F6EDDA"), (1, "#E2CEA8")), stroke=NONE)
# rust crown stripe flowing between the ears onto the mask top
d.path("M434,322 C460,318 496,322 518,340 C500,348 470,352 446,352 "
       "C424,352 404,348 392,342 C404,330 418,324 434,322 Z",
       "Crown", fill="#A8521F", opacity=85, stroke=NONE)
# tear streaks: rust trails from the inner eye corners down the cheeks
d.path("M428,410 C420,430 408,452 392,466", "Tear streak L", fill=NONE,
       stroke="#8A3E16", strokeWidth=12, opacity=75, cap="round")
d.path("M500,412 C508,432 518,452 530,466", "Tear streak R", fill=NONE,
       stroke="#8A3E16", strokeWidth=12, opacity=75, cap="round")
# cheek ruff scallops
d.path("M360,430 C352,450 356,470 372,482", "Cheek ruff L", fill=NONE,
       stroke="#E8D4B0", strokeWidth=8, opacity=60, cap="round")
d.path("M534,430 C540,452 534,472 520,484", "Cheek ruff R", fill=NONE,
       stroke="#E8D4B0", strokeWidth=8, opacity=60, cap="round")

# --- face details -----------------------------------------------------------------------
# pale brow spots above the eyes — the red panda's signature speckles
d.shape("ellipse", "Brow spot L", x=414, y=380, width=16, height=11,
        fill="#F6EDDA", opacity=90, stroke=NONE)
d.shape("ellipse", "Brow spot R", x=478, y=382, width=16, height=11,
        fill="#F6EDDA", opacity=90, stroke=NONE)
# eyes: deep amber, calm
d.shape("ellipse", "Eye L", x=416, y=398, width=20, height=22,
        fill=rad((0, "#4A2A14"), (1, "#180C04")), stroke=INK, strokeWidth=2.5)
d.shape("ellipse", "Eye R", x=482, y=400, width=20, height=22,
        fill=rad((0, "#4A2A14"), (1, "#180C04")), stroke=INK, strokeWidth=2.5)
d.shape("ellipse", "Glint L", x=421, y=402, width=6, height=6,
        fill="#FFFFFF", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=487, y=404, width=6, height=6,
        fill="#FFFFFF", opacity=90, stroke=NONE)
# nose + mouth
d.path("M450,442 C458,438 470,438 478,442 C480,452 474,460 464,461 "
       "C454,460 448,452 450,442 Z", "Nose", fill="#241512", stroke=INK, strokeWidth=3)
d.path("M464,461 L464,470", "Philtrum", fill=NONE, stroke=INK, strokeWidth=3, cap="round")
d.path("M464,470 C458,476 450,478 443,475 M464,470 C470,476 478,478 485,475",
       "Mouth", fill=NONE, stroke=INK, strokeWidth=3, cap="round")
# whiskers
for i, (x1, y1, x2, y2) in enumerate([(438,446,370,434),(440,455,368,458),(442,462,376,478),
                                      (488,448,552,440),(486,456,550,462),(484,463,544,482)]):
    d.path(f"M{x1},{y1} Q{(x1+x2)/2},{min(y1,y2)-6} {x2},{y2}", f"Whisker {i+1}",
           fill=NONE, stroke="#F2E4CC", strokeWidth=2, opacity=55, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#1E2E26", strokeWidth=6)

# --- caption ---------------------------------------------------------------------
d.text("RED PANDA", "Name", x=500, y=940, size=58, font="Virelai Sans",
       color="#E4EFE8", justify="center")
LINE2, SZ2, TRK = "AILURUS FULGENS", 22, 320
r = d.text(LINE2, "Second line", x=500, y=975, size=SZ2, font="Virelai Sans",
           color="#A0BCA8", justify="center")
if r and "id" in r:
    d.cmd("text.setStyle", "Second line tracking", id=r["id"], tracking=TRK)

def find(o, oid):
    if isinstance(o, dict):
        if o.get("id") == oid and "bounds" in o: return o
        o = list(o.values())
    if isinstance(o, list):
        for v in o:
            hit = find(v, oid)
            if hit: return hit
if r and "id" in r:
    b2 = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
    print("second line bounds", {k: round(v) for k, v in b2.items()})
    assert b2["width"] <= 760 and b2["x"] >= 100 and b2["y"] + b2["height"] <= 990, b2

d.finish("red-panda-V1R00")
