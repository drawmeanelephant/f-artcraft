#!/usr/bin/env python3
"""Binturong — field-guide plate V2R00. Second interpretation: where V1 is a
day-lit profile walking a branch, this is a bear-shaped question mark in a
tree — full body hunched and shaggy, prehensile tail wrapped twice around
the wood with its tip curled under, tufted white-rimmed ears, coarse black
fur with a grizzled mask, one musk-yellow eye. Dusky moonlit canopy plate;
branch and leaf masses close on the disc's own arc.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Binturong — Field Plate", 1000, 1000)

INK = "#0C0B0A"
MOON = "#F4F0D8"
GRIZ = "#C8C2B0"
CX, CY, R = 500, 460, 420          # plate disc centre + radius
ARC = f"A{R},{R} 0 0 1"
rng = random.Random(59)

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def on_disc(deg):
    t = math.radians(deg)
    return CX + R*math.cos(t), CY + R*math.sin(t)

def P(deg):
    return "%.1f,%.1f" % on_disc(deg)

def cubic(p0, p1, p2, p3, t):
    u = 1 - t
    return (u**3*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t**3*p3[0],
            u**3*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t**3*p3[1])

def spine_of(segs, n=14):
    pts = []
    for k, seg in enumerate(segs):
        pts += [cubic(*seg, i/n) for i in range(0 if k == 0 else 1, n + 1)]
    return pts

def normals(pts):
    out, n = [], len(pts)
    for i in range(n):
        ax, ay = pts[max(i - 1, 0)]; bx, by = pts[min(i + 1, n - 1)]
        ln = math.hypot(bx - ax, by - ay) or 1
        out.append((-(by - ay)/ln, (bx - ax)/ln))
    return out

def ribbon(pts, nn, ws, cap_end=True):
    L = [(x + nx*w/2, y + ny*w/2) for (x, y), (nx, ny), w in zip(pts, nn, ws)]
    Rr = [(x - nx*w/2, y - ny*w/2) for (x, y), (nx, ny), w in zip(pts, nn, ws)]
    dd = "M%.1f,%.1f " % L[0] + " ".join("L%.1f,%.1f" % p for p in L[1:])
    dd += (" A%.1f,%.1f 0 0 0 %.1f,%.1f " % (ws[-1]/2, ws[-1]/2, *Rr[-1])) if cap_end else " L%.1f,%.1f " % Rr[-1]
    return dd + " ".join("L%.1f,%.1f" % p for p in reversed(Rr[:-1])) + " Z"

def shaggy(pts, amp):
    """Spiky fur edge: a tuft point outward between each pair (clockwise traversal)."""
    out = [pts[0]]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        dx, dy = x1 - x0, y1 - y0
        ln = math.hypot(dx, dy) or 1
        a = amp*rng.uniform(0.35, 1.3)
        out.append(((x0 + x1)/2 + dy/ln*a, (y0 + y1)/2 - dx/ln*a))
        out.append((x1, y1))
    return out

BG_GRAD = lin(0, 0, 0, 1000, (0, "#1C1F18"), (1, "#070806"))
PLATE_GRAD = rad((0, "#DCD8B4"), (0.6, "#A8A684"), (1, "#5E6248"))
FUR_GRAD = lin(0, 380, 0, 600, (0, "#4E4A44"), (0.5, "#2A2826"), (1, "#141312"))
TAIL_GRAD = lin(560, 0, 820, 0, (0, "#3E3A36"), (1, "#1A1816"))
BARK_GRAD = lin(0, 580, 0, 660, (0, "#9A7A52"), (0.5, "#6E5236"), (1, "#3E2C1C"))
LEAF_GRAD = lin(0, 40, 0, 360, (0, "#4E6238"), (1, "#2A3820"))
IRIS_GRAD = rad((0, "#FFE680"), (0.6, "#E2AE2A"), (1, "#7A5410"))

# --- backdrop + moonlit canopy plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
for i, (x, y, w, o) in enumerate([(60,110,5,40),(150,40,4,30),(40,420,5,35),(930,80,6,40),
                                  (955,400,4,30),(60,840,5,30),(940,820,5,30)]):
    d.shape("ellipse", f"Star {i+1}", x=x, y=y, width=w, height=w, fill="#E8E4CC", opacity=o, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#2E3224", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F4F2DE", strokeWidth=3, opacity=45)
for k, (r, op) in enumerate([(110, 10), (80, 14), (56, 24), (38, 70)]):
    d.shape("ellipse", f"Moon {k+1}", x=600 - r, y=220 - r, width=2*r, height=2*r,
            fill=MOON, opacity=op, stroke=NONE)
d.shape("ellipse", "Moon mare", x=576, y=206, width=22, height=14, fill="#C8C4A8", opacity=50, stroke=NONE)
# canopy leaf masses hanging into the top of the disc, closing on the arc
d.path(f"M{P(258)} Q440,120 400,150 Q420,190 370,200 Q380,250 320,246 Q320,300 262,290 "
       f"Q250,340 200,322 Q180,350 {P(196)} {ARC} {P(258)} Z", "Canopy L", fill=LEAF_GRAD, opacity=88, stroke=NONE)
d.path(f"M{P(292)} Q700,110 720,150 Q760,150 760,196 Q810,200 800,250 Q850,262 830,300 "
       f"Q880,320 {P(348)} {ARC} {P(292)} Z", "Canopy R", fill=LEAF_GRAD, opacity=80, stroke=NONE)
for i, dd in enumerate(["M150,300 Q230,250 300,240", "M210,200 Q290,180 360,190", "M330,110 Q370,130 396,150",
                        "M870,300 Q820,260 790,250", "M820,190 Q780,170 740,160"]):
    d.path(dd, f"Leaf vein {i+1}", fill=NONE, stroke="#8AA062", strokeWidth=3, opacity=40, cap="round")
for i, (x, y, w) in enumerate([(470,330,6),(700,380,5),(160,430,5),(830,430,6),(420,250,4),(760,300,5)]):
    d.shape("ellipse", f"Firefly {i+1}", x=x, y=y, width=w, height=w, fill="#F6E890", opacity=65, stroke=NONE)

# --- tail, full pass (the coils behind the branch show only above/below it) -------------------
tail = spine_of([((596,470), (650,486), (668,548), (652,592)),     # rump down to the branch top
                 ((652,592), (660,620), (676,640), (690,654)),     # front pass 1
                 ((690,654), (704,684), (738,684), (730,650)),     # under-loop
                 ((730,650), (726,620), (708,596), (712,586)),     # behind the branch
                 ((712,586), (718,566), (744,566), (748,590)),     # over the top
                 ((748,590), (756,620), (768,640), (780,656)),     # front pass 2
                 ((780,656), (806,694), (790,742), (756,742)),     # tip hangs below...
                 ((756,742), (728,742), (722,712), (744,706))])    # ...and curls: the question mark
tn = normals(tail)
tw = [max(18, 72 - 54*i/(len(tail) - 1)) for i in range(len(tail))]
d.path(ribbon(tail, tn, tw), "Tail", fill=TAIL_GRAD, stroke=INK, strokeWidth=5)

# --- the branch, both ends closing on the disc arc -------------------------------------------
d.path(f"M{P(160)} C330,586 640,604 {P(18)} {ARC} {P(25)} C650,652 340,642 {P(153)} {ARC} {P(160)} Z",
       "Branch", fill=BARK_GRAD, stroke=INK, strokeWidth=5)
d.path("M130,612 C330,594 640,610 880,598", "Branch moonlit top", fill=NONE, stroke="#E8D8B0",
       strokeWidth=5, opacity=40, cap="round")
for i, dd in enumerate(["M160,628 C220,624 260,628 300,632", "M420,628 C470,626 520,630 560,634",
                        "M800,622 C830,620 860,622 880,624", "M220,640 C250,642 280,640 300,642"]):
    d.path(dd, f"Bark grain {i+1}", fill=NONE, stroke="#2E2014", strokeWidth=3, opacity=55, cap="round")
for i, (x, y, w, h) in enumerate([(380,600,60,16),(560,606,44,14),(820,598,40,12)]):
    d.shape("ellipse", f"Moss {i+1}", x=x, y=y, width=w, height=h, fill="#7E9450", opacity=60, stroke=NONE)
# twig with leaves rising off the right end
d.path("M850,600 C852,570 846,540 834,516", "Twig", fill=NONE, stroke="#5E4630", strokeWidth=6, cap="round")
for i, (bx, by, tx, ty, s) in enumerate([(846,560,800,530,1), (840,532,872,500,-1), (834,516,820,474,1)]):
    mx, my = (bx + tx)/2, (by + ty)/2
    nx, ny = -(ty - by)*0.3*s, (tx - bx)*0.3*s
    d.path(f"M{bx},{by} Q{mx + nx:.1f},{my + ny:.1f} {tx},{ty} Q{mx - nx:.1f},{my - ny:.1f} {bx},{by} Z",
           f"Twig leaf {i+1}", fill=lin(0, ty, 0, by, (0, "#7E9A50"), (1, "#3E5228")), stroke=INK, strokeWidth=3)

# --- front passes of the coils, over the branch -----------------------------------------------
for k, (a, b) in enumerate([(14, 29), (70, 85)]):
    seg, sn, sw = tail[a:b], tn[a:b], tw[a:b]
    d.path(ribbon(seg, sn, sw, cap_end=False), f"Tail coil {k+1}", fill=TAIL_GRAD, stroke=INK, strokeWidth=5)
    d.path("M" + " L".join("%.1f,%.1f" % (x + nx*w*0.25, y + ny*w*0.25) for (x, y), (nx, ny), w in zip(seg, sn, sw)),
           f"Tail coil sheen {k+1}", fill=NONE, stroke=GRIZ, strokeWidth=4, opacity=35, cap="round")
for k in range(3, len(tail) - 6, 5):
    (x, y), (nx, ny), w = tail[k], tn[k], tw[k]
    if 600 < y < 650 and 640 < x < 790:
        continue
    d.path(f"M{x + nx*w*0.4:.1f},{y + ny*w*0.4:.1f} L{x + nx*w*0.1 + 4:.1f},{y + ny*w*0.1 + 4:.1f}",
           f"Tail grizzle {k}", fill=NONE, stroke=GRIZ, strokeWidth=3, opacity=40, cap="round")

# --- far legs, behind the body ---------------------------------------------------------------
d.path("M336,500 C334,540 340,570 346,598 L392,598 C388,570 390,536 392,500 Z", "Far foreleg",
       fill=lin(0, 500, 0, 600, (0, "#1E1C1A"), (1, "#0E0D0C")), stroke=INK, strokeWidth=4)
d.path("M500,500 C500,540 506,572 512,598 L556,598 C552,570 552,536 552,500 Z", "Far hindleg",
       fill=lin(0, 500, 0, 600, (0, "#1E1C1A"), (1, "#0E0D0C")), stroke=INK, strokeWidth=4)

# --- body: hunched, shaggy -------------------------------------------------------------------
back = spine_of([((250,470), (270,420), (340,396), (440,392)),
                 ((440,392), (540,388), (610,420), (624,490))], 18)
under = spine_of([((624,490), (632,540), (608,576), (560,580)),
                  ((560,580), (470,588), (370,588), (310,574)),
                  ((310,574), (262,562), (240,520), (250,470))], 6)
body = shaggy(back, 9) + shaggy(under[1:], 5)[1:]
d.path("M" + " L".join("%.1f,%.1f" % p for p in body) + " Z", "Body", fill=FUR_GRAD, stroke=INK, strokeWidth=5)
for i in range(40):
    t = rng.uniform(0.05, 0.95)
    x, y = back[int(t*(len(back) - 1))]
    y += rng.uniform(8, 50); x += rng.uniform(-8, 8)
    ang = rng.uniform(-0.6, 0.6) - math.pi/2
    d.path(f"M{x:.1f},{y:.1f} L{x + 14*math.cos(ang):.1f},{y + 14*math.sin(ang):.1f}", f"Back grizzle {i+1}",
           fill=NONE, stroke=GRIZ, strokeWidth=3, opacity=rng.choice([30, 40, 50]), cap="round")
d.path("M300,420 C360,398 440,392 520,396", "Back moon rim", fill=NONE, stroke=MOON,
       strokeWidth=6, opacity=30, cap="round")

# --- near legs + paws gripping the branch ----------------------------------------------------
PAW = lin(0, 580, 0, 614, (0, "#3A3632"), (1, "#141210"))
d.path("M270,500 C264,540 270,572 276,596 L334,596 C330,566 332,532 336,500 Z", "Near foreleg",
       fill=FUR_GRAD, stroke=INK, strokeWidth=5)
d.path("M260,604 C256,586 272,578 304,578 C334,578 348,590 344,606 C340,616 270,618 260,604 Z",
       "Near forepaw", fill=PAW, stroke=INK, strokeWidth=4)
d.path("M562,476 C612,486 632,546 614,598 L558,598 C552,566 538,542 532,518 C530,494 544,478 562,476 Z", "Near thigh",
       fill=FUR_GRAD, stroke=INK, strokeWidth=5)
d.path("M544,604 C540,588 556,580 586,580 C614,580 628,592 624,606 C620,616 554,618 544,604 Z",
       "Near hindpaw", fill=PAW, stroke=INK, strokeWidth=4)
for k, x in enumerate([272, 290, 308, 326, 556, 574, 592, 610]):
    d.path(f"M{x},{606} C{x - 2},{614} {x + 2},{620} {x + 6},{622}", f"Claw {k+1}", fill=NONE,
           stroke="#D8CCB0", strokeWidth=3, opacity=70, cap="round")
d.path("M600,500 C618,530 620,566 610,592", "Thigh grizzle", fill=NONE, stroke=GRIZ, strokeWidth=4, opacity=35, cap="round")

# --- ears: rounded, white-rimmed, long tufts -------------------------------------------------
def ear(cx, cy, label, shade):
    # tapered, gently curved tufts streaming back off the ear tip
    for j, (dx, h, lean, w) in enumerate([(-6, 40, 14, 12), (2, 52, 22, 14), (10, 44, 30, 12)]):
        x0, y0 = cx + dx, cy - 14
        tx, ty = x0 + lean, y0 - h
        d.path(f"M{x0 - w/2:.1f},{y0} Q{x0 - w/2 + lean*0.2:.1f},{y0 - h*0.7:.1f} {tx:.1f},{ty:.1f} "
               f"Q{x0 + w/2 + lean*0.5:.1f},{y0 - h*0.4:.1f} {x0 + w/2:.1f},{y0} Z",
               f"{label} tuft {j+1}", fill=lin(0, ty, 0, y0, (0, "#6A665C"), (0.4, shade), (1, shade)),
               stroke=INK, strokeWidth=3)
    d.shape("ellipse", label, x=cx - 24, y=cy - 24, width=48, height=48, fill=shade, stroke=INK, strokeWidth=4)
    d.path(f"M{cx - 20},{cy - 6} C{cx - 16},{cy - 22} {cx + 4},{cy - 28} {cx + 20},{cy - 14}", f"{label} white rim",
           fill=NONE, stroke="#F2EEDC", strokeWidth=4, opacity=70, cap="round")

ear(312, 408, "Far ear", "#1A1816")

# --- head: three-quarter to the viewer's left, grizzled mask ----------------------------------
HEAD = ("M300,404 C344,414 356,466 342,508 C330,542 294,560 252,556 "
        "C220,554 194,540 176,524 C160,512 160,494 176,486 "
        "C198,474 206,448 222,428 C244,404 272,396 300,404 Z")
d.path(HEAD, "Head", fill=rad((0, "#5A5650"), (0.7, "#2E2C28"), (1, "#141312")), stroke=INK, strokeWidth=6)
ear(262, 404, "Near ear", "#24221F")
d.path("M236,436 C210,456 196,482 190,500 C200,520 230,536 262,540 C300,540 324,520 330,490 "
       "C300,470 270,450 236,436 Z", "Grizzled mask", fill=rad((0, "#A8A294"), (1, "#5A564E")), opacity=60, stroke=NONE)
for i in range(46):
    x, y = rng.uniform(180, 340), rng.uniform(420, 552)
    if ((x - 262)/80)**2 + ((y - 488)/66)**2 > 1:
        continue
    ang = rng.uniform(0, math.pi)
    d.path(f"M{x:.1f},{y:.1f} L{x + 7*math.cos(ang):.1f},{y + 7*math.sin(ang):.1f}", f"Mask grizzle {i+1}",
           fill=NONE, stroke=rng.choice([GRIZ, "#E8E4D4", "#2A2826"]), strokeWidth=3, opacity=55, cap="round")
# brow patch + the one musk-yellow eye
d.path("M212,452 C224,440 246,438 262,446", "Brow", fill=NONE, stroke="#E8E4D4", strokeWidth=6, opacity=70, cap="round")
d.shape("ellipse", "Eye glow", x=206, y=446, width=56, height=46, fill="#F2C440", opacity=18, stroke=NONE)
d.path("M216,468 C224,456 246,454 256,466 C248,480 226,482 216,468 Z", "Eye", fill=IRIS_GRAD, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Pupil", x=233, y=460, width=8, height=14, fill="#0A0804", stroke=NONE)
d.shape("ellipse", "Glint", x=236, y=461, width=5, height=5, fill="#FFFFFF", opacity=92, stroke=NONE)
d.path("M300,456 C304,470 304,486 298,498", "Far eye socket", fill=NONE, stroke=INK, strokeWidth=5, opacity=60, cap="round")
# muzzle, nose, mouth
d.path("M160,500 C160,488 176,482 190,488 C198,494 196,510 186,514 C174,518 160,512 160,500 Z", "Nose",
       fill=lin(0, 484, 0, 516, (0, "#3E3A36"), (1, "#0E0C0A")), stroke=INK, strokeWidth=3)
d.shape("ellipse", "Nose glint", x=168, y=490, width=10, height=5, fill="#FFFFFF", opacity=45, stroke=NONE)
d.path("M184,518 C196,530 214,534 232,530", "Mouth", fill=NONE, stroke=INK, strokeWidth=4, cap="round")
# long white whiskers
for j, (x1, y1, x2, y2) in enumerate([(196,500,110,470),(198,508,104,500),(202,516,112,534),
                                      (206,522,128,560),(212,526,150,578)]):
    d.path(f"M{x1},{y1} Q{(x1 + x2)/2},{min(y1, y2) - 8} {x2},{y2}", f"Whisker {j+1}", fill=NONE,
           stroke="#F4F0E0", strokeWidth=3, opacity=80, cap="round")
d.path("M226,428 C256,408 290,404 316,416", "Head moon rim", fill=NONE, stroke=MOON,
       strokeWidth=5, opacity=35, cap="round")

# --- name ------------------------------------------------------------------------------------
d.text("BINTURONG", "Name", x=500, y=962, size=58, font="Virelai Sans",
       color="#E2E0C8", justify="center")

d.finish("binturong-V2R00")
