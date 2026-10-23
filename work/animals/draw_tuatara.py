#!/usr/bin/env python3
"""Tuatara — field-guide plate V1R00. Full-body side profile facing left,
perched on a mossy stone: the spiny crest of soft pale spines running from the
nape down the back and onto the tail, big dark eye, beaked upper jaw, throat
folds. Olive-green hide with pale speckles; tree-fern fronds behind for an
ancient, Gondwanan mood.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Tuatara — Field Plate", 1000, 1000)

INK = "#1F2412"
CX, CY = 500, 460                  # plate disc centre
DOWN = -90                         # linear gradient angle: top -> bottom
BG_GRAD = {"gradient": {"kind": "linear", "angle": DOWN, "stops": [
    {"offset": 0, "color": "#1C2319"}, {"offset": 1, "color": "#080A07"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E4E3CC"}, {"offset": 0.7, "color": "#B9BB98"},
    {"offset": 1, "color": "#7C805E"}]}}
BODY_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#8E9654"}, {"offset": 0.7, "color": "#646F38"},
    {"offset": 1, "color": "#3E4722"}]}}
HEAD_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#949B5A"}, {"offset": 0.7, "color": "#68723B"},
    {"offset": 1, "color": "#424B24"}]}}
NAPE_GRAD = {"gradient": {"kind": "linear", "angle": DOWN, "stops": [
    {"offset": 0, "color": "#727D42"}, {"offset": 1, "color": "#5E6934"}]}}
TAIL_GRAD = {"gradient": {"kind": "linear", "angle": DOWN, "stops": [
    {"offset": 0, "color": "#7E874A"}, {"offset": 1, "color": "#454F28"}]}}
LEG_GRAD = {"gradient": {"kind": "linear", "angle": DOWN, "stops": [
    {"offset": 0, "color": "#7A8448"}, {"offset": 1, "color": "#4A5428"}]}}
LEG_FAR_GRAD = {"gradient": {"kind": "linear", "angle": DOWN, "stops": [
    {"offset": 0, "color": "#525C2E"}, {"offset": 1, "color": "#323A1A"}]}}
CREST_GRAD = {"gradient": {"kind": "linear", "angle": DOWN, "stops": [
    {"offset": 0, "color": "#F2EFD2"}, {"offset": 1, "color": "#B6B583"}]}}
ROCK_GRAD = {"gradient": {"kind": "linear", "angle": DOWN, "stops": [
    {"offset": 0, "color": "#97957A"}, {"offset": 0.45, "color": "#66654F"},
    {"offset": 1, "color": "#2E2E24"}]}}
IRIS_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#7A5A30"}, {"offset": 0.7, "color": "#4E3818"},
    {"offset": 1, "color": "#24180A"}]}}
FERN_GRAD = {"gradient": {"kind": "linear", "angle": DOWN, "stops": [
    {"offset": 0, "color": "#7F8A60"}, {"offset": 1, "color": "#56603E"}]}}

def inside(x, y, r=392):
    dx, dy = x - CX, y - CY
    k = math.hypot(dx, dy)
    return (x, y) if k <= r else (CX + dx*r/k, CY + dy*r/k)

def chord_x(y, r):
    h = math.sqrt(r*r - (y - CY)**2)
    return CX - h, CX + h

def cubic(p0, p1, p2, p3, t):
    u = 1 - t
    x = u**3*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t**3*p3[0]
    y = u**3*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t**3*p3[1]
    dx = 3*u*u*(p1[0]-p0[0]) + 6*u*t*(p2[0]-p1[0]) + 3*t*t*(p3[0]-p2[0])
    dy = 3*u*u*(p1[1]-p0[1]) + 6*u*t*(p2[1]-p1[1]) + 3*t*t*(p3[1]-p2[1])
    return (x, y), (dx, dy)

def sample(segs, n):
    """Points + unit tangents along a chain of cubic segments, t in [0,1]."""
    out = []
    for i in range(n + 1):
        g = i / n * len(segs)
        k = min(int(g), len(segs) - 1)
        (x, y), (dx, dy) = cubic(*segs[k], g - k)
        ln = math.hypot(dx, dy) or 1
        out.append((x, y, dx/ln, dy/ln))
    return out

def limb(segs, w0, w1, w2, label, fill, n=24):
    """Tapered ribbon over a two-segment cubic chain (shoulder->elbow->wrist);
    width eases w0 -> w1 at the joint -> w2 at the end."""
    left, right = [], []
    for i, (x, y, tx, ty) in enumerate(sample(segs, n)):
        t = i / n
        w = (w0 + (w1 - w0)*t*2 if t <= 0.5 else w1 + (w2 - w1)*(t - 0.5)*2) / 2
        left.append((x - ty*w, y + tx*w)); right.append((x + ty*w, y - tx*w))
    dd = "M%.1f,%.1f " % left[0] + " ".join("L%.1f,%.1f" % p for p in left[1:])
    dd += " " + " ".join("L%.1f,%.1f" % p for p in reversed(right)) + " Z"
    d.path(dd, label, fill=fill, stroke=INK, strokeWidth=6)

def spine(bx, by, tx, ty, nx, ny, h, label):
    """Soft triangular crest spine standing on (bx,by), tangent (tx,ty),
    outward normal (nx,ny), leaning back along the tangent."""
    b = max(7, h * 0.5)
    l = (bx - tx*b, by - ty*b); r = (bx + tx*b, by + ty*b)
    tip = (bx + nx*h + tx*h*0.34, by + ny*h + ty*h*0.34)
    c1 = (bx - tx*b*0.55 + nx*h*0.62, by - ty*b*0.55 + ny*h*0.62)
    c2 = (bx + tx*b*0.75 + nx*h*0.42, by + ty*b*0.75 + ny*h*0.42)
    d.path(f"M{l[0]:.1f},{l[1]:.1f} Q{c1[0]:.1f},{c1[1]:.1f} {tip[0]:.1f},{tip[1]:.1f} "
           f"Q{c2[0]:.1f},{c2[1]:.1f} {r[0]:.1f},{r[1]:.1f} Z",
           label, fill=CREST_GRAD, stroke=INK, strokeWidth=3)

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#62664A", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F1F1DE", strokeWidth=3, opacity=55)
d.shape("ellipse", "Patina 1", x=170, y=170, width=240, height=150, fill="#A2A482", opacity=22, stroke=NONE)
d.shape("ellipse", "Patina 2", x=600, y=180, width=230, height=130, fill="#A2A482", opacity=18, stroke=NONE)
for i, (x, y, w) in enumerate([(210,300,8),(780,290,7),(150,430,6),(860,420,7),(400,120,7),
                               (610,115,8),(270,200,6),(720,190,7),(480,260,6),(560,330,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w, fill="#767A58", opacity=40, stroke=NONE)

# tree-fern fronds behind the animal: arched rachis + paired pinnae, clamped inside
def frond(base, ctrl, tip, n, length, label, op):
    segs = [(base, ctrl, ctrl, tip)]
    d.path(f"M{base[0]},{base[1]} Q{ctrl[0]},{ctrl[1]} {tip[0]},{tip[1]}", f"{label} rachis",
           fill=NONE, stroke=FERN_GRAD, strokeWidth=5, opacity=op, cap="round")
    for k, (x, y, tx, ty) in enumerate(sample(segs, n + 1)[1:-1]):
        L = length * (1 - 0.75 * k / n)
        for s in (1, -1):
            nx, ny = -ty * s, tx * s
            ex, ey = inside(x + (nx*0.85 + tx*0.5)*L, y + (ny*0.85 + ty*0.5)*L)
            mx, my = x + nx*L*0.5 + tx*L*0.15, y + ny*L*0.5 + ty*L*0.15 - 4
            d.path(f"M{x:.0f},{y:.0f} Q{mx:.0f},{my:.0f} {ex:.0f},{ey:.0f}",
                   f"{label} pinna {k+1}{'ab'[s < 0]}", fill=NONE, stroke=FERN_GRAD,
                   strokeWidth=7, opacity=op, cap="round")

frond((250, 640), (150, 420), (300, 170), 11, 62, "Fern L", 32)
frond((760, 640), (880, 420), (680, 160), 11, 62, "Fern R", 32)
frond((470, 610), (420, 360), (560, 170), 9, 46, "Fern M", 18)

# --- mossy stone, closed on the disc's own arc -------------------------------------
rr = 414
sl, sr = chord_x(700, rr)
d.path(f"M{sl:.1f},700 C200,650 300,618 420,616 C540,614 660,628 740,660 "
       f"C790,680 816,692 {sr:.1f},700 A{rr},{rr} 0 0 1 {sl:.1f},700 Z",
       "Stone", fill=ROCK_GRAD, stroke=INK, strokeWidth=6)
d.path("M210,660 C290,630 380,622 460,622 C560,622 650,634 720,658", "Stone top light",
       fill=NONE, stroke="#D8D7BC", strokeWidth=6, opacity=30, cap="round")
for i, (x, y, w, h) in enumerate([(230,646,120,26),(470,618,150,22),(640,640,110,24),
                                  (300,700,90,20),(560,720,120,22)]):
    d.shape("ellipse", f"Moss {i+1}", x=x, y=y, width=w, height=h, fill="#6E8040", opacity=40, stroke=NONE)
for i, (x0, y0, x1, y1) in enumerate([(260,740,330,760),(450,780,540,770),(620,750,700,770),(380,820,460,830)]):
    d.path(f"M{x0},{y0} L{x1},{y1}", f"Stone crack {i+1}", fill=NONE,
           stroke="#2A2A20", strokeWidth=3, opacity=40, cap="round")
d.shape("ellipse", "Cast shadow", x=300, y=606, width=420, height=34, fill="#151810", opacity=40, stroke=NONE)

# --- far-side legs (behind body) -----------------------------------------------------
limb([((452, 518), (456, 542), (466, 556), (474, 570)),
      ((474, 570), (478, 588), (462, 600), (444, 606))], 40, 22, 16, "Front leg far", LEG_FAR_GRAD)
limb([((660, 510), (650, 542), (640, 562), (636, 576)),
      ((636, 576), (634, 596), (648, 610), (664, 614))], 46, 24, 16, "Hind leg far", LEG_FAR_GRAD)
for i, (x0, y0, x1, y1) in enumerate([(440,606,422,612),(446,608,432,620),(662,614,644,618),(668,614,656,624)]):
    d.path(f"M{x0},{y0} L{x1},{y1}", f"Far toe {i+1}", fill=NONE, stroke="#323A1A", strokeWidth=6, cap="round")

# --- tail: tapered ribbon along a two-segment spine --------------------------------------
TAIL = [((636, 500), (730, 492), (796, 536), (806, 604)),
        ((806, 604), (814, 672), (770, 724), (708, 722))]
pts = sample(TAIL, 40)
outer, inner = [], []
for i, (x, y, tx, ty) in enumerate(pts):
    w = (84 + (2 - 84) * (i / 40)) / 2
    nx, ny = -ty, tx                  # points toward the inside of the curl
    inner.append((x + nx*w, y + ny*w)); outer.append((x - nx*w, y - ny*w))
dd = "M%.1f,%.1f " % outer[0] + " ".join("L%.1f,%.1f" % p for p in outer[1:])
dd += " " + " ".join("L%.1f,%.1f" % p for p in reversed(inner)) + " Z"
d.path(dd, "Tail", fill=TAIL_GRAD, stroke=INK, strokeWidth=6, join="round")
# tail crest: small spines along the outer edge, fading toward the tip
for k, i in enumerate(range(4, 30, 3)):
    x, y, tx, ty = pts[i]
    ox, oy = outer[i]
    spine(ox, oy, tx, ty, ty, -tx, 18 - k * 1.5, f"Tail spine {k+1}")
# tail banding + underside shade
for k, i in enumerate(range(8, 38, 5)):
    (ax, ay), (bx, by) = outer[i], inner[i]
    d.path(f"M{ax:.0f},{ay:.0f} L{bx:.0f},{by:.0f}", f"Tail band {k+1}", fill=NONE,
           stroke="#3A4320", strokeWidth=9 - k, opacity=30, cap="round")
d.path("M" + " L".join("%.0f,%.0f" % ((ix*0.75 + x*0.25), (iy*0.75 + y*0.25))
                        for (ix, iy), (x, y, _, _) in zip(inner[4:34], pts[4:34])),
       "Tail underside shade", fill=NONE, stroke="#2E3518", strokeWidth=10, opacity=30, cap="round")

# --- body ------------------------------------------------------------------------
BACK = [((318, 432), (370, 414), (440, 408), (500, 410)),
        ((500, 410), (570, 412), (630, 428), (672, 468))]
d.path("M318,432 C370,414 440,408 500,410 C570,412 630,428 672,468 "
       "C694,494 690,528 660,546 C590,566 480,566 420,552 C380,542 346,528 322,512 Z",
       "Body", fill=BODY_GRAD, stroke=INK, strokeWidth=7)
d.path("M360,540 C440,560 560,562 650,544", "Belly light", fill=NONE,
       stroke="#C9C994", strokeWidth=14, opacity=30, cap="round")
d.path("M352,432 C420,416 520,414 600,430", "Back light", fill=NONE,
       stroke="#E2E4B4", strokeWidth=8, opacity=20, cap="round")
# dark dorsal saddles
for i, (x, y, w, h) in enumerate([(400,424,46,40),(470,418,50,44),(545,422,50,44),(615,438,44,40)]):
    d.shape("ellipse", f"Saddle {i+1}", x=x, y=y, width=w, height=h, fill="#2F381A", opacity=22, stroke=NONE)
# lateral skin fold
d.path("M380,500 C450,512 540,514 640,500", "Lateral fold", fill=NONE,
       stroke="#3A4320", strokeWidth=4, opacity=40, cap="round")

# crest along nape + back: tall nuchal spines, a short gap, then the dorsal run
bp = sample(BACK, 48)
for k, (i, h) in enumerate([(2, 34), (5, 42), (8, 44), (11, 40), (14, 32),
                            (19, 22), (23, 25), (27, 25), (31, 23), (35, 21),
                            (39, 19), (43, 17)]):
    x, y, tx, ty = bp[i]
    spine(x, y + 3, tx, ty, ty, -tx, h, f"Crest spine {k+1}")

# --- near legs ----------------------------------------------------------------------
# front: upper arm swings back to the elbow, forearm plants forward
limb([((392, 512), (398, 540), (412, 558), (424, 574)),
      ((424, 574), (432, 592), (408, 606), (382, 612))], 50, 28, 20, "Front leg", LEG_GRAD)
# hind: thigh drives forward to the knee, shin kicks back to the ankle
limb([((622, 512), (604, 546), (588, 566), (584, 584)),
      ((584, 584), (582, 606), (604, 620), (626, 624))], 60, 30, 20, "Hind leg", LEG_GRAD)
d.path("M612,526 C598,546 590,564 588,580", "Thigh light", fill=NONE,
       stroke="#C9CC92", strokeWidth=7, opacity=30, cap="round")
d.path("M400,524 C406,542 414,556 422,566", "Arm light", fill=NONE,
       stroke="#C9CC92", strokeWidth=6, opacity=30, cap="round")
# toes with pale claws, splayed on the stone
for i, (x0, y0, x1, y1) in enumerate([(378,608,350,614),(380,614,356,626),(386,618,372,632),(392,616,404,630),
                                      (622,618,596,622),(626,624,606,636),(632,626,624,640),(640,622,652,634)]):
    d.path(f"M{x0},{y0} L{x1},{y1}", f"Toe {i+1}", fill=NONE, stroke="#46502A", strokeWidth=7, cap="round")
    d.path(f"M{x1 + (x1-x0)*0.05:.0f},{y1 + (y1-y0)*0.05:.0f} L{x1 + (x1-x0)*0.3:.0f},{y1 + (y1-y0)*0.3:.0f}",
           f"Claw {i+1}", fill=NONE, stroke="#E6E1C4", strokeWidth=3, cap="round")

# --- head (profile facing left) ------------------------------------------------------
d.path("M326,430 C296,414 254,410 222,418 C194,426 176,446 170,466 "
       "C166,480 170,490 182,494 C210,504 262,516 314,514 "
       "C342,512 362,500 374,484 C382,462 364,440 326,430 Z",
       "Head", fill=HEAD_GRAD, stroke=INK, strokeWidth=7)
# blend the back of the skull into the neck so the head doesn't sit on like a cap
d.path("M336,436 C368,444 392,464 386,492 L366,498 C372,472 358,452 330,446 Z",
       "Nape blend", fill=NAPE_GRAD, stroke=NONE)
d.path("M196,432 C230,418 280,416 320,428", "Crown light", fill=NONE,
       stroke="#E2E4B4", strokeWidth=7, opacity=30, cap="round")
# beaked upper jaw + mouth line with the faint tuatara smile
d.path("M174,484 C180,492 184,496 186,500", "Beak tip", fill=NONE, stroke=INK, strokeWidth=5, cap="round")
d.path("M184,492 C214,496 252,496 290,498 C312,500 330,502 344,498", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
d.path("M196,500 C240,510 290,514 330,510", "Lower jaw light", fill=NONE,
       stroke="#CFCF9A", strokeWidth=6, opacity=30, cap="round")
# throat folds where head meets neck
for i, dd in enumerate(["M318,514 C334,524 350,530 368,528", "M330,524 C346,536 364,540 382,536",
                        "M344,532 C360,544 378,548 394,544"]):
    d.path(dd, f"Throat fold {i+1}", fill=NONE, stroke="#323A1A", strokeWidth=4, opacity=45, cap="round")
d.path("M352,452 C360,468 362,486 356,502", "Neck fold", fill=NONE,
       stroke="#323A1A", strokeWidth=4, opacity=40, cap="round")
# big dark eye with vertical pupil
d.shape("ellipse", "Eye socket", x=236, y=424, width=58, height=48, fill="#2F381A", opacity=35, stroke=NONE)
d.shape("ellipse", "Eye", x=244, y=430, width=42, height=36, fill=IRIS_GRAD, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Pupil", x=261, y=432, width=8, height=32, fill="#0A0804", stroke=NONE)
d.shape("ellipse", "Glint", x=252, y=436, width=8, height=7, fill="#FFFFFF", opacity=85, stroke=NONE)
d.path("M238,436 C252,420 280,420 294,436", "Brow", fill=NONE, stroke=INK, strokeWidth=6, cap="round")
d.path("M246,470 C258,476 274,476 286,470", "Lower lid", fill=NONE,
       stroke="#C9CC92", strokeWidth=3, opacity=50, cap="round")
d.shape("ellipse", "Nostril", x=180, y=456, width=10, height=8, fill="#151A0A", opacity=80, stroke=NONE)

# --- pale speckles across the hide --------------------------------------------------
rnd = random.Random(30)
n = 0
def speck(x, y, s):
    global n
    n += 1
    d.shape("ellipse", f"Speckle {n}", x=x - s/2, y=y - s/2, width=s, height=s*0.85,
            fill="#E8E6BE", opacity=55, stroke=NONE)
for _ in range(60):
    a, r = rnd.uniform(0, 2*math.pi), math.sqrt(rnd.random())
    x, y = 500 + 150*r*math.cos(a), 484 + 46*r*math.sin(a)
    speck(x, y, rnd.uniform(3, 7))
for i in range(4, 34, 2):
    x, y, tx, ty = pts[i]
    w = (84 + (2 - 84) * (i / 40)) / 2
    o = rnd.uniform(-0.5, 0.5) * w
    speck(x - ty*o, y + tx*o, rnd.uniform(2.5, 5.5))
for x, y, s in [(206,448,4),(222,474,5),(300,450,4),(320,474,5),(336,494,4),(300,486,3),(214,460,3)]:
    speck(x, y, s)
for x, y, s in [(376,568,4),(366,590,3),(610,560,4),(598,580,3),(616,600,4)]:
    speck(x, y, s)

# --- name ----------------------------------------------------------------------
d.text("TUATARA", "Name", x=500, y=962, size=60, font="Virelai Sans",
       color="#E1E2CC", justify="center")

d.finish("tuatara-V1R00")
