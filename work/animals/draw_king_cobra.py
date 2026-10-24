#!/usr/bin/env python3
"""King cobra — field-guide plate V1R00. Front-on rear: the snake rises out of
its coils to eye level, narrow hood flared, two dark chevrons low on the
ventral shield. Coils stacked on a wet stone floor that closes on the disc's
own arc, monsoon rain needling down the dark. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math, re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("King Cobra — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420          # plate disc centre + radius
INK = "#1C1408"

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def on_disc(x, y, pad=0):
    return math.hypot(x - CX, y - CY) <= R - pad

def mirror(dd):
    out, toks, ex = [], re.findall(r"[A-Za-z]|-?\d*\.?\d+", dd), True
    for t in toks:
        if t.isalpha():
            out.append(t); ex = True
        elif ex:
            out.append(f"{1000 - float(t):g},"); ex = False
        else:
            out[-1] += f"{float(t):g}"; ex = True
    return " ".join(out)

def pair(dd, label, **kw):
    d.path(dd, f"{label} L", **kw)
    d.path(mirror(dd), f"{label} R", **kw)

BG_GRAD = lin(0, 0, 0, 1000, (0, "#0B0F0B"), (1, "#020403"))
PLATE_GRAD = rad((0, "#4E5E46"), (0.55, "#2E3C2C"), (1, "#131B13"))
FLOOR_GRAD = lin(0, 700, 0, 880, (0, "#3E4438"), (1, "#171B14"))
BODY_GRAD = lin(0, 460, 0, 800, (0, "#9A8256"), (0.5, "#6E5C38"), (1, "#3E341E"))
HOOD_GRAD = rad((0, "#E0CB9A"), (0.55, "#B49866"), (1, "#6E5836"))
HEAD_GRAD = rad((0, "#C9B078"), (0.6, "#9A7E4E"), (1, "#5C482A"))
COIL_GRAD = lin(0, 650, 0, 800, (0, "#8A7448"), (1, "#463A22"))

# --- backdrop + plate ------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#5E7054", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#1E2A1C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C4CEB4", strokeWidth=3, opacity=35)
# shrine glow behind the hood
d.shape("ellipse", "Shrine glow", x=330, y=180, width=340, height=360,
        fill=rad((0, "#B8A268"), (1, "#B8A268")), opacity=8, stroke=NONE)
# monsoon rain: fine diagonal needles, all inside the disc
for i, (x, y, ln) in enumerate([(240,170,90),(310,140,70),(390,90,80),(500,80,70),(610,95,85),
                                (680,140,75),(770,190,70),(160,300,80),(840,290,85),(240,420,70),
                                (770,430,80),(180,540,75),(830,540,70),(350,140,60),(660,170,65)]):
    assert on_disc(x, y, 30) and on_disc(x + ln*0.28, y + ln, 30), (x, y)
    d.path(f"M{x},{y} L{x + ln*0.28:.0f},{y + ln}", f"Rain {i+1}",
           fill=NONE, stroke="#C9D8CE", strokeWidth=1.6, opacity=14, cap="round")
# drifting motes
for i, (x, y, w) in enumerate([(230,220,5),(760,240,5),(180,470,6),(830,460,6),(310,140,5),
                               (690,130,5),(420,120,4),(580,150,5)]):
    assert on_disc(x + w/2, y + w/2, 8), (x, y)
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#E2E8D6", opacity=40, stroke=NONE)

# --- wet stone floor, closing on the disc's own arc --------------------------------
fy = 700
fdx = math.sqrt(R * R - (fy - CY) ** 2)
x0, x1 = CX - fdx, CX + fdx
d.path(f"M{x0:.1f},{fy} C330,692 670,692 {x1:.1f},{fy} "
       f"A{R},{R} 0 0 1 {x0:.1f},{fy} Z", "Floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{x0 + 4:.1f},{fy} C330,692 670,692 {x1 - 4:.1f},{fy}",
       "Floor sheen", fill=NONE, stroke="#B8C4AE", strokeWidth=3, opacity=30, cap="round")
# a stepped plinth silhouette, temple-dark
d.path(f"M{x0 + 60:.0f},{fy - 26} L{x0 + 60:.0f},{fy} M{x0 + 60:.0f},{fy - 26} "
       f"L{x1 - 60:.0f},{fy - 26} L{x1 - 60:.0f},{fy}",
       "Plinth edge", fill=NONE, stroke="#0E1410", strokeWidth=4, opacity=35)
for i, dd in enumerate(["M240,770 C340,764 430,766 500,770", "M560,790 C650,784 730,786 790,792",
                        "M300,830 C420,824 560,826 660,832"]):
    d.path(dd, f"Floor crack {i+1}", fill=NONE, stroke="#0E130E",
           strokeWidth=3, opacity=35, cap="round")
# rain pooling: a few bright pinpricks on the stone
for i, (x, y) in enumerate([(250,730),(390,745),(640,735),(760,725),(480,760),(700,770)]):
    d.shape("ellipse", f"Rain glint {i+1}", x=x - 4, y=y - 2, width=8, height=4,
            fill="#D6E2DA", opacity=35, stroke=NONE)

# --- coils: three stacked bands ---------------------------------------------------
def coil(cx, cy, rx, ry, label, grad):
    d.shape("ellipse", label, x=cx - rx, y=cy - ry, width=rx*2, height=ry*2,
            fill=grad, stroke=INK, strokeWidth=5)
    d.path(f"M{cx - rx + 26},{cy - ry*0.15} C{cx - rx*0.4},{cy + ry*0.5} "
           f"{cx + rx*0.4},{cy + ry*0.5} {cx + rx - 26},{cy - ry*0.15}",
           f"{label} under-shade", fill=NONE, stroke="#241C0C",
           strokeWidth=7, opacity=30, cap="round")

coil(500, 742, 218, 62, "Coil base", COIL_GRAD)
coil(478, 690, 168, 52, "Coil mid", COIL_GRAD)
# scale arcs across the base coil
for i, a in enumerate(range(200, 341, 28)):
    t = math.radians(a)
    x, y = 500 + 196 * math.cos(t), 742 + 48 * math.sin(t)
    d.path(f"M{x - 8:.0f},{y:.0f} A8,6 0 0 1 {x + 8:.0f},{y:.0f}",
           f"Coil scale {i+1}", fill=NONE, stroke="#2E2410", strokeWidth=2, opacity=35)

# --- the rising column: tube built on a curving spine --------------------------------
def cubic(p0, p1, p2, p3, t):
    u = 1 - t
    return (u**3*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t**3*p3[0],
            u**3*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t**3*p3[1])

spine = [cubic((498,690), (486,600), (522,540), (506,478), i/16) for i in range(17)]
Lp, Rp = [], []
n = len(spine)
for i, (x, y) in enumerate(spine):
    ax, ay = spine[max(i - 1, 0)]; bx, by = spine[min(i + 1, n - 1)]
    dx, dy = bx - ax, by - ay
    ln = math.hypot(dx, dy) or 1
    nx, ny = -dy/ln, dx/ln
    w = (92 - 30 * i / (n - 1)) / 2
    Lp.append((x + nx*w, y + ny*w)); Rp.append((x - nx*w, y - ny*w))
dd = "M%.1f,%.1f " % Lp[0] + " ".join("L%.1f,%.1f" % p for p in Lp[1:])
dd += " " + " ".join("L%.1f,%.1f" % p for p in reversed(Rp)) + " Z"
d.path(dd, "Neck column", fill=BODY_GRAD, stroke=INK, strokeWidth=5)
# ventral scutes: faint horizontal bars up the front of the column
for j, i in enumerate(range(2, 15, 2)):
    x, y = spine[i]
    t = i / (n - 1)
    hw = (92 - 30 * t) / 2 - 6
    d.path(f"M{x - hw:.0f},{y:.0f} C{x - hw*0.3:.0f},{y + 4:.0f} "
           f"{x + hw*0.3:.0f},{y + 4:.0f} {x + hw:.0f},{y:.0f}",
           f"Ventral scute {j+1}", fill=NONE, stroke="#3A2E14", strokeWidth=2.5, opacity=40)
# sheen down the column's left flank
d.path("M470,660 C466,600 478,540 492,492", "Column sheen",
       fill=NONE, stroke="#E8D6A2", strokeWidth=8, opacity=18, cap="round")
# top coil laps over the column's foot, seating the rise
coil(512, 644, 118, 44, "Coil top", COIL_GRAD)

# --- hood: the narrow flare of the king ---------------------------------------------
# a tall kite of neck skin: wraps the head's jaw corners, widest low, runs into the column
HOOD = ("M500,272 C448,272 410,282 392,306 C370,336 362,368 372,398 "
        "C380,436 400,470 424,496 C444,516 460,526 470,530 "
        "C478,534 490,536 500,536 C510,536 522,534 530,530 "
        "C540,526 556,516 576,496 C600,470 620,436 628,398 "
        "C638,368 630,336 608,306 C590,282 552,272 500,272 Z")
d.path(HOOD, "Hood", fill=HOOD_GRAD, stroke=INK, strokeWidth=6)
# hood rim shading: darker along the flared edges
pair("M392,306 C370,336 362,368 372,398 C380,432 398,462 420,486",
     "Hood edge shade", fill=NONE, stroke="#5C4822", strokeWidth=10, opacity=30, cap="round")
# fine rib lines fanning from the throat outward — the hood's bones
for i, (x2, y2) in enumerate([(390,318),(372,356),(372,398),(388,438),(416,472),(446,500)]):
    d.path(f"M499,{318 + i*4} Q{(499 + x2)/2 - 14:.0f},{(318 + y2)/2:.0f} {x2},{y2}",
           f"Hood rib {i+1}", fill=NONE, stroke="#7A6034", strokeWidth=2, opacity=28)
    d.path(mirror(f"M499,{318 + i*4} Q{(499 + x2)/2 - 14:.0f},{(318 + y2)/2:.0f} {x2},{y2}"),
           f"Hood rib R{i+1}", fill=NONE, stroke="#7A6034", strokeWidth=2, opacity=28)
# the twin chevrons low on the shield — oblique bars meeting near the midline
pair("M490,488 L438,456 M490,488 L442,472", "Chevron",
     fill=NONE, stroke="#4A3A18", strokeWidth=6, opacity=55, cap="round")
pair("M492,506 L452,486", "Chevron 2",
     fill=NONE, stroke="#4A3A18", strokeWidth=4.5, opacity=40, cap="round")
# wet sheen across the hood crown
d.path("M430,300 C474,288 530,288 574,302", "Hood sheen",
       fill=NONE, stroke="#F4E8C4", strokeWidth=9, opacity=20, cap="round")

# --- head ------------------------------------------------------------------------------
HEAD = ("M500,222 C536,222 564,240 570,268 C575,292 566,316 542,328 "
        "C528,336 512,340 500,340 C488,340 472,336 458,328 "
        "C434,316 425,292 430,268 C436,240 464,222 500,222 Z")
d.path(HEAD, "Head", fill=HEAD_GRAD, stroke=INK, strokeWidth=5)
d.shape("ellipse", "Brow light", x=462, y=230, width=76, height=22,
        fill="#F2E2B4", opacity=22, stroke=NONE)
# crown shield seams traced in ink: frontal plate + parietals + midline suture
d.path("M486,238 L500,232 L514,238 L514,252 L500,258 L486,252 Z",
       "Frontal shield seam", fill=NONE, stroke="#6A5426", strokeWidth=2, opacity=55)
pair("M470,258 C464,252 460,244 462,238 C470,240 476,246 478,254 Z",
     "Parietal seam", fill=NONE, stroke="#6A5426", strokeWidth=2, opacity=50)
d.path("M500,222 L500,232", "Midline suture", fill=NONE, stroke="#6A5426",
       strokeWidth=2, opacity=50)
# eyes: dark beads under a heavy brow — the level stare
for sgn in (-1, 1):
    ex = 500 + sgn * 39
    d.shape("ellipse", f"Eye {'L' if sgn < 0 else 'R'}", x=ex - 10, y=260, width=20, height=17,
            fill="#14100A", stroke=INK, strokeWidth=2)
    d.shape("ellipse", f"Eye glint {'L' if sgn < 0 else 'R'}", x=ex - 6, y=263, width=4.5, height=4.5,
            fill="#F4ECD4", opacity=80, stroke=NONE)
    d.path("M444,262 C452,252 464,248 476,252" if sgn < 0 else
           mirror("M444,262 C452,252 464,248 476,252"),
           f"Supraocular {'L' if sgn < 0 else 'R'}", fill=NONE, stroke=INK,
           strokeWidth=5, opacity=70, cap="round")
# snout: rostral cap, nostrils, mouth seam
d.path("M484,300 C488,292 512,292 516,300 C516,310 508,314 500,314 C492,314 484,310 484,300 Z",
       "Rostral", fill="#B89C68", stroke=INK, strokeWidth=2.5)
d.shape("ellipse", "Nostril L", x=474, y=298, width=6, height=5, fill="#1A1408", stroke=NONE)
d.shape("ellipse", "Nostril R", x=520, y=298, width=6, height=5, fill="#1A1408", stroke=NONE)
d.path("M462,308 C480,318 520,318 538,308", "Mouth seam",
       fill=NONE, stroke=INK, strokeWidth=3, opacity=55, cap="round")
# jaw-edge sheen
pair("M444,282 C446,296 452,308 462,316", "Jaw sheen",
     fill=NONE, stroke="#F0E2B6", strokeWidth=4, opacity=30, cap="round")

# --- caption ---------------------------------------------------------------------------
r1 = d.text("KING COBRA", "Name", x=500, y=938, size=60, font="Virelai Sans",
            color="#E8DCB4", justify="center")
LINE2, SZ2, TRK = "OPHIOPHAGUS HANNAH", 22, 300
r = d.text(LINE2, "Second line", x=500, y=974, size=SZ2, font="Virelai Sans",
           color="#B0A074", justify="center")
d.cmd("text.setStyle", "Second line tracking", id=r["id"], tracking=TRK)

def find(o, oid):
    if isinstance(o, dict):
        if o.get("id") == oid and "bounds" in o: return o
        o = list(o.values())
    if isinstance(o, list):
        for v in o:
            hit = find(v, oid)
            if hit: return hit
layers = d.call("inspect_document", {}, "inspect")["layers"]
for rr, lim in ((r1, 800), (r, 760)):
    b = find(layers, rr["id"])["bounds"]
    print("caption bounds", {k: round(v) for k, v in b.items()})
    assert b["width"] <= lim and b["x"] >= 100 and b["y"] + b["height"] <= 990, b

d.finish("king-cobra-V1R00")
