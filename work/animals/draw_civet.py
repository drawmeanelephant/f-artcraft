#!/usr/bin/env python3
"""Civet — field-guide plate V1R00. Full-body profile facing left, head low
in forage-sniff pose: bandit mask with warm amber eye, black dorsal crest
stripe over a rosette-spotted grey coat, bushy ringed tail sweeping behind.
Cool midnight-blue plate, leaf-litter floor closing on the disc's own arc.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Civet — Field Plate", 1000, 1000)

INK = "#16141E"
CX, CY, R = 500, 460, 420
BG_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#16203A"}, {"offset": 1, "color": "#060A14"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#93A9CC"}, {"offset": 0.62, "color": "#546E9E"},
    {"offset": 1, "color": "#28395C"}]}}
GROUND_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#39466A"}, {"offset": 1, "color": "#1A2238"}]}}
COAT_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#B8AE9E"}, {"offset": 0.55, "color": "#8E8674"},
    {"offset": 1, "color": "#5E584A"}]}}
FAR_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#6E6656"}, {"offset": 1, "color": "#46402F"}]}}
HEAD_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#C2B8A6"}, {"offset": 0.7, "color": "#968C76"},
    {"offset": 1, "color": "#66604E"}]}}
TAIL_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#CFC6B4"}, {"offset": 1, "color": "#8A8272"}]}}
LEAF_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#5E6E54"}, {"offset": 1, "color": "#38422E"}]}}

def chord_x(y, r=R):
    h = math.sqrt(r*r - (y - CY)**2)
    return CX - h, CX + h

def clamp(x, y, r=404):
    dx, dy = x - CX, y - CY
    k = math.hypot(dx, dy)
    return (x, y) if k <= r else (CX + dx*r/k, CY + dy*r/k)

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#5E7CAE", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8E4F6", strokeWidth=3, opacity=55)
# moonlight dapple + drifting night flecks
for i, (x, y, w, h, o) in enumerate([(300,150,150,80,20),(560,110,110,60,16),
                                     (680,240,130,70,14),(220,320,90,56,12)]):
    d.shape("ellipse", f"Moon dapple {i+1}", x=x, y=y, width=w, height=h,
            fill="#E8F0FF", opacity=o, stroke=NONE)
for i, (x, y, w) in enumerate([(200,240,6),(790,300,7),(170,470,6),(840,500,7),
                               (330,110,6),(650,150,6),(250,640,5),(760,650,6)]):
    d.shape("ellipse", f"Night fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#BFD0EE", opacity=35, stroke=NONE)
# a small pale moon near the top of the disc
d.shape("ellipse", "Moon", x=452, y=104, width=64, height=64,
        fill="#E9EFFA", opacity=85, stroke=NONE)
d.shape("ellipse", "Moon shade", x=470, y=112, width=44, height=44,
        fill="#546E9E", opacity=30, stroke=NONE)

# --- leaf-litter floor: closes on the disc's own arc ----------------------------
gl, gr = chord_x(716)
d.path(f"M{gl:.1f},716 C340,702 660,702 {gr:.1f},716 A420,420 0 0 1 {gl:.1f},716 Z",
       "Litter floor", fill=GROUND_GRAD, stroke=NONE)
d.path(f"M{gl+20:.1f},714 C350,704 650,704 {gr-20:.1f},714", "Floor light",
       fill=NONE, stroke="#9FB4DC", strokeWidth=4, opacity=30, cap="round")
# fallen leaves resting on the floor
for i, (x, y, ang, L) in enumerate([(250,760,-20,64),(330,800,30,54),(560,782,80,60),
                                    (650,818,-40,52),(720,768,20,58),(420,832,-70,48)]):
    a = math.radians(ang)
    tx, ty = x + math.cos(a)*L, y + math.sin(a)*L*0.4
    nx, ny = -math.sin(a)*L*0.24, math.cos(a)*L*0.10
    mx, my = (x + tx)/2, (y + ty)/2
    d.path(f"M{x:.0f},{y:.0f} Q{mx+nx:.0f},{my+ny:.0f} {tx:.0f},{ty:.0f} "
           f"Q{mx-nx:.0f},{my-ny:.0f} {x:.0f},{y:.0f} Z",
           f"Fallen leaf {i+1}", fill=LEAF_GRAD, opacity=70, stroke=NONE)
    d.path(f"M{x:.0f},{y:.0f} L{tx:.0f},{ty:.0f}", f"Leaf {i+1} rib",
           fill=NONE, stroke="#2C3422", strokeWidth=2, opacity=50, cap="round")
for i, (x, y, w) in enumerate([(300,742,26),(480,736,34),(620,748,24),(390,760,20),(700,736,22)]):
    d.shape("ellipse", f"Litter pebble {i+1}", x=x, y=y, width=w, height=w*0.35,
            fill="#141B30", opacity=50, stroke=NONE)
# re-stroke the rim so the plate edge stays continuous over the floor
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#5E7CAE", strokeWidth=6)
d.shape("ellipse", "Plate inner ring over floor", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8E4F6", strokeWidth=3, opacity=35)
d.shape("ellipse", "Civet shadow", x=240, y=700, width=420, height=26,
        fill="#0A0E1E", opacity=40, stroke=NONE)

# --- ringed tail: tapered ribbon along a Catmull-Rom spine, drawn under the body --
def catmull(pts, samples_per=10):
    out = []
    P = [pts[0]] + pts + [pts[-1]]
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i-1], P[i], P[i+1], P[i+2]
        for s in range(samples_per):
            t = s / samples_per
            t2, t3 = t*t, t*t*t
            x = 0.5*((2*p1[0]) + (-p0[0]+p2[0])*t + (2*p0[0]-5*p1[0]+4*p2[0]-p3[0])*t2 + (-p0[0]+3*p1[0]-3*p2[0]+p3[0])*t3)
            y = 0.5*((2*p1[1]) + (-p0[1]+p2[1])*t + (2*p0[1]-5*p1[1]+4*p2[1]-p3[1])*t2 + (-p0[1]+3*p1[1]-3*p2[1]+p3[1])*t3)
            out.append((x, y))
    out.append(pts[-1])
    return out

spine = catmull([(648,486),(726,492),(782,536),(800,600),(778,664),(716,700),(652,694)])
N = len(spine)
L, Rr, mid = [], [], []
for i, (x, y) in enumerate(spine):
    a = spine[max(i-1, 0)]; b = spine[min(i+1, N-1)]
    dx, dy = b[0]-a[0], b[1]-a[1]
    ln = math.hypot(dx, dy) or 1
    nx, ny = -dy/ln, dx/ln
    t = i / (N - 1)
    w = (52 - 26*t) / 2
    mid.append((x, y, nx, ny, w))
    L.append((x + nx*w, y + ny*w)); Rr.append((x - nx*w, y - ny*w))
td = "M%.1f,%.1f " % L[0] + " ".join("L%.1f,%.1f" % p for p in L[1:])
td += " " + " ".join("L%.1f,%.1f" % p for p in reversed(Rr)) + " Z"
d.path(td, "Tail", fill=TAIL_GRAD, stroke=INK, strokeWidth=6)
# dark rings across the ribbon width
for j in range(6):
    i0 = 6 + j*10
    x, y, nx, ny, w = mid[min(i0, N-1)]
    d.path(f"M{x + nx*w*0.92:.1f},{y + ny*w*0.92:.1f} L{x - nx*w*0.92:.1f},{y - ny*w*0.92:.1f}",
           f"Tail ring {j+1}", fill=NONE, stroke="#201E28", strokeWidth=13,
           opacity=90, cap="butt")
# tail sheen along the upper edge
sheen = [(m[0] + m[2]*m[4]*-0.55, m[1] + m[3]*m[4]*-0.55) for m in mid[2:N-6]]
d.path("M%.1f,%.1f " % sheen[0] + " ".join("L%.1f,%.1f" % p for p in sheen[1:]),
       "Tail sheen", fill=NONE, stroke="#EDE6D4", strokeWidth=5, opacity=35, cap="round")

# --- legs: short, drawn before the body ------------------------------------------
def leg(label, sx, px, ws, wp, fill, paw_fill):
    sy, py = 556, 700
    d.path(f"M{sx-ws/2},{sy} C{sx-ws/2+2},{sy+44} {px-wp/2-4},{py-30:.1f} {px-wp/2},{py-4:.1f} "
           f"Q{px},{py+5:.1f} {px+wp/2},{py-4:.1f} C{px+wp/2+2},{py-24:.1f} {sx+ws/2-2},{sy+36} {sx+ws/2},{sy} Z",
           label, fill=fill, stroke=INK, strokeWidth=5)
    d.shape("ellipse", f"{label} paw", x=px-(wp+16)/2-4, y=py-11, width=wp+16, height=15,
            fill=paw_fill, stroke=INK, strokeWidth=4)
    return px - 4, py

leg("Far foreleg", 330, 342, 30, 17, FAR_GRAD, "#4A4434")
leg("Far hindleg", 596, 610, 32, 17, FAR_GRAD, "#4A4434")
paws = [leg("Near foreleg", 306, 296, 40, 20, COAT_GRAD, "#5A5442"),
        leg("Near hindleg", 566, 556, 44, 20, COAT_GRAD, "#5A5442")]

# --- body: long low torso ---------------------------------------------------------
d.path("M268,486 C300,448 372,428 460,426 C552,424 640,438 686,470 "
       "C716,492 718,532 692,556 C652,586 560,596 460,592 "
       "C376,588 306,568 280,540 C264,522 260,504 268,486 Z",
       "Body", fill=COAT_GRAD, stroke=INK, strokeWidth=7)
# black dorsal crest stripe along the spine, serrated crest hairs on top
d.path("M330,452 C380,434 470,428 560,432 C620,436 668,452 690,472 "
       "C660,458 600,446 540,444 C460,440 380,444 330,452 Z",
       "Dorsal stripe", fill="#14121C", opacity=92, stroke=NONE)
for i in range(14):
    x = 336 + i*24
    y = 448 - abs(x - 500)*0.045
    d.path(f"M{x},{y+4:.0f} L{x+6},{y-14:.0f} L{x+12},{y+2:.0f}",
           f"Crest hair {i+1}", fill="#14121C", opacity=80, stroke=NONE)
# rosette spots: broken dark rings + solid dots over the flank
for i, (x, y, w, h) in enumerate([(380,492,26,18),(440,506,30,20),(506,498,26,18),
                                   (572,506,30,20),(634,516,24,16),(356,536,24,16),
                                   (420,548,30,20),(488,542,26,18),(556,552,30,18),
                                   (622,556,24,16),(300,512,22,16),(668,534,20,14)]):
    d.shape("ellipse", f"Rosette {i+1}", x=x, y=y, width=w, height=h,
            fill=NONE, stroke="#26222E", strokeWidth=4, opacity=70)
for i, (x, y, w) in enumerate([(404,530,9),(530,522,9),(596,530,8),(336,500,8),
                               (460,566,9),(584,570,8),(654,502,8),(516,486,7)]):
    d.shape("ellipse", f"Spot dot {i+1}", x=x, y=y, width=w, height=w*0.8,
            fill="#26222E", opacity=75, stroke=NONE)
# shading + sheen
d.path("M300,470 C360,446 450,438 540,440", "Back sheen", fill=NONE,
       stroke="#EDE4D2", strokeWidth=10, opacity=30, cap="round")
d.path("M320,566 C400,584 540,588 640,566", "Belly shade", fill=NONE,
       stroke="#3E3A2E", strokeWidth=12, opacity=30, cap="round")
d.path("M296,540 C340,566 400,578 470,580", "Belly light", fill=NONE,
       stroke="#DAD2BE", strokeWidth=10, opacity=22, cap="round")
for (px, py) in paws:
    for k in (-7, 0, 7):
        d.path(f"M{px+k:.0f},{py-8:.0f} L{px+k:.0f},{py-3:.0f}", "Toe", fill=NONE,
               stroke=INK, strokeWidth=2.5, opacity=55, cap="round")

# --- neck + head: low forage pose, pointed muzzle ---------------------------------
d.path("M268,486 C252,462 248,440 258,420 C268,398 292,386 318,388 "
       "C348,390 368,410 372,438 C374,462 366,482 348,494 "
       "C322,508 288,504 268,486 Z",
       "Head", fill=HEAD_GRAD, stroke=INK, strokeWidth=7)
# muzzle extension down-left (sniffing)
d.path("M258,452 C236,458 216,472 206,492 C202,502 206,512 218,514 "
       "C238,516 260,508 272,492 C280,478 274,460 258,452 Z",
       "Muzzle", fill=HEAD_GRAD, stroke=INK, strokeWidth=6)
d.shape("ellipse", "Nose", x=200, y=496, width=22, height=16, fill="#17121A", stroke=NONE)
d.path("M222,514 C234,522 252,522 266,512", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
# ears: two rounded triangles on the crown
d.path("M296,392 C288,370 296,352 314,350 C330,350 338,366 332,384 Z",
       "Ear far", fill=FAR_GRAD, stroke=INK, strokeWidth=4)
d.path("M330,394 C326,368 338,350 358,352 C376,354 384,372 376,392 Z",
       "Ear near", fill=HEAD_GRAD, stroke=INK, strokeWidth=5)
d.path("M338,388 C336,372 342,362 354,362 C366,364 370,376 366,390 Z",
       "Inner ear", fill="#3A332A", opacity=60, stroke=NONE)
# the bandit mask: black band through the eye, pale brow + cheek framing it
d.path("M282,428 C302,418 330,416 352,424 C350,444 340,462 322,472 "
       "C304,478 288,472 282,456 C278,446 278,436 282,428 Z",
       "Mask", fill="#18151F", opacity=92, stroke=NONE)
d.path("M286,420 C306,410 332,408 352,416", "Mask brow light", fill=NONE,
       stroke="#EDE0C4", strokeWidth=6, opacity=70, cap="round")
d.path("M290,470 C300,482 318,486 334,480", "Mask cheek light", fill=NONE,
       stroke="#DCCFAF", strokeWidth=6, opacity=55, cap="round")
# warm amber eye inside the mask
d.shape("ellipse", "Iris", x=306, y=436, width=24, height=22,
        fill="#C8862E", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Pupil", x=313, y=439, width=9, height=16, fill="#0E0A10", stroke=NONE)
d.shape("ellipse", "Glint", x=309, y=439, width=5, height=5, fill="#FFFFFF", opacity=90, stroke=NONE)
d.path("M300,434 C310,426 326,426 336,434", "Upper lid", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
# pale chin + throat
d.path("M250,498 C264,512 288,518 310,514 C296,524 270,524 252,514 Z",
       "Chin pale", fill="#D8D0BC", opacity=80, stroke=NONE)
# whiskers
for i, dd in enumerate(["M238,486 C216,478 196,478 180,484",
                        "M240,494 C218,494 198,500 182,510",
                        "M244,502 C224,508 208,516 196,528"]):
    d.path(dd, f"Whisker {i+1}", fill=NONE, stroke="#E8E0CC", strokeWidth=2.5, opacity=65, cap="round")

# --- name ----------------------------------------------------------------------
d.text("CIVET", "Name", x=500, y=962, size=60, font="Virelai Sans",
       color="#CBD8EE", justify="center")

d.finish("civet-V1R00")
