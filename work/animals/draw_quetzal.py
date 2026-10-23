#!/usr/bin/env python3
"""Resplendent quetzal — field-guide plate V1R00. Perched profile facing left:
emerald helmet crest, crimson breast, and the absurd twin tail streamers
cascading off the branch in slow S-curves. Cloud-forest teal plate, mist wisps,
iridescence from layered translucent gradients. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Resplendent Quetzal — Field Plate", 1000, 1000)

INK = "#12261E"
CX, CY, R = 500, 460, 420

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def disc_x(y, side, r=420):
    return CX + side*math.sqrt(r*r - (y - CY)**2)

def cubic(p0, p1, p2, p3, t):
    u = 1 - t
    return (u**3*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t**3*p3[0],
            u**3*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t**3*p3[1])

BG_GRAD    = lin(0, 0, 0, 1000, (0, "#122A24"), (1, "#040D0B"))
PLATE_GRAD = rad((0, "#C4DCC9"), (0.62, "#6FA08C"), (1, "#2E5246"))
BODY_GRAD  = rad((0, "#5CE0A4"), (0.55, "#1FA870"), (1, "#0B6B45"))
HEAD_GRAD  = rad((0, "#74ECB4"), (0.6, "#25B478"), (1, "#0E7549"))
CREST_GRAD = rad((0, "#8AF4C0"), (0.6, "#2CC084"), (1, "#127A4E"))
BREAST_GRAD = rad((0, "#F0556A"), (0.6, "#C22A40"), (1, "#7E1424"))
WING_GRAD  = lin(0, 400, 0, 640, (0, "#18A068"), (1, "#0A5A3A"))
STREAM_GRAD = lin(560, 600, 700, 870, (0, "#3ED898"), (0.55, "#18A86B"), (1, "#0B6B45"))
STREAM_GRAD_B = lin(580, 600, 560, 850, (0, "#4CE0A4"), (0.55, "#22B478"), (1, "#0E7549"))
BRANCH_GRAD = lin(0, 640, 0, 720, (0, "#64784E"), (1, "#33402A"))

def ribbon(pts, w0, w1, label, fill, sw=5):
    """Tapered ribbon along a sampled spine, round cap at the tip."""
    n = len(pts)
    L, Rp, norms = [], [], []
    for i, (x, y) in enumerate(pts):
        ax, ay = pts[max(i-1, 0)]; bx, by = pts[min(i+1, n-1)]
        dx, dy = bx-ax, by-ay
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy/ln, dx/ln
        w = (w0 + (w1 - w0)*i/(n-1)) / 2
        norms.append((nx, ny, w))
        L.append((x + nx*w, y + ny*w)); Rp.append((x - nx*w, y - ny*w))
    tw = max(w1/2, 2)
    dd = "M%.1f,%.1f " % L[0] + " ".join("L%.1f,%.1f" % p for p in L[1:])
    dd += " A%.1f,%.1f 0 0 0 %.1f,%.1f " % (tw, tw, Rp[-1][0], Rp[-1][1])
    dd += " ".join("L%.1f,%.1f" % p for p in reversed(Rp[:-1])) + " Z"
    d.path(dd, label, fill=fill, stroke=INK, strokeWidth=sw)
    return pts, norms

def spine_chain(segs, per=16):
    pts = []
    for s in segs:
        pts += [cubic(*s, i/per) for i in range(per)]
    pts.append(segs[-1][3])
    return pts

# --- backdrop + cloud-forest plate ----------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
for i, (x, y, w) in enumerate([(110,130,4),(210,70,3),(70,330,4),(920,100,4),(870,220,3),
                               (945,450,4),(80,600,3),(150,850,4),(860,860,4),(940,660,3)]):
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#9AD8B8", opacity=35, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#1F4438", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8EAE0", strokeWidth=3, opacity=50)
# mist wisps drifting behind the bird
for i, (x, y, w, h, o) in enumerate([(150,180,340,54,20),(480,130,300,44,16),(180,470,260,40,14),
                                     (620,360,240,38,14),(240,720,220,36,12)]):
    d.shape("ellipse", f"Mist {i+1}", x=x, y=y, width=w, height=h,
            fill="#E4F0E8", opacity=o, stroke=NONE)
for i, (x, y, w) in enumerate([(220,290,7),(790,260,6),(160,430,7),(840,430,7),(320,150,6),
                               (650,140,6),(260,640,6),(790,630,6),(430,120,5),(560,110,5)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#2E5246", opacity=38, stroke=NONE)

# --- the mossy perch, both ends closing on the disc arc ----------------------------
xL, xR = disc_x(690, -1), disc_x(686, 1)
bL, bR = disc_x(742, -1), disc_x(744, 1)
d.path(f"M{xL:.1f},690 C340,676 460,684 560,678 C660,672 760,676 {xR:.1f},686 "
       f"A{R},{R} 0 0 1 {bR:.1f},744 C620,736 380,730 {bL:.1f},742 "
       f"A{R},{R} 0 0 1 {xL:.1f},690 Z",
       "Perch", fill=BRANCH_GRAD, stroke=INK, strokeWidth=5)
d.path(f"M{xL+8:.1f},688 C340,674 460,682 560,676 C660,670 760,674 {xR-8:.1f},684",
       "Perch moss light", fill=NONE, stroke="#A8C078", strokeWidth=6, opacity=50, cap="round")
# moss pads + dangling strands
d.shape("ellipse", "Moss pad 1", x=250, y=676, width=90, height=22, fill="#8FB46A", opacity=55, stroke=NONE)
d.shape("ellipse", "Moss pad 2", x=640, y=670, width=110, height=24, fill="#8FB46A", opacity=50, stroke=NONE)
for i, (x0, y0, x1, y1) in enumerate([(268,700,258,756),(284,702,282,744),(742,692,748,740),(724,694,722,734)]):
    d.path(f"M{x0},{y0} C{x0-4},{(y0+y1)/2} {x1+4},{(y0+y1)/2} {x1},{y1}",
           f"Moss strand {i+1}", fill=NONE, stroke="#7A9C58", strokeWidth=3, opacity=55, cap="round")

# --- tail streamers: drawn before the body so the rump sits over their roots --------
# short true tail under the rump, bridging body to streamers
st = spine_chain([((580,580),(640,610),(664,650),(670,690))], per=10)
ribbon(st, 34, 14, "Tail base", WING_GRAD, sw=5)
# outer streamer — the long one, swings right then curls back in
sa = spine_chain([((576,560),(690,610),(736,676),(734,752)),
                  ((734,752),(730,820),(668,844),(640,830))], per=15)
pts, nrm = ribbon(sa, 44, 15, "Streamer outer", STREAM_GRAD, sw=5)
# inner streamer — drifts down-left of the outer
sb = spine_chain([((558,575),(618,660),(560,730),(548,794)),
                  ((548,794),(542,838),(594,854),(618,838))], per=15)
ptsb, nrmb = ribbon(sb, 38, 13, "Streamer inner", STREAM_GRAD_B, sw=5)
# sheen threads along each streamer's lit edge
d.path("M" + " L".join("%.1f,%.1f" % (x + nx*w*0.5, y + ny*w*0.5)
       for (x, y), (nx, ny, w) in zip(pts[3:-3], nrm[3:-3])),
       "Streamer outer sheen", fill=NONE, stroke="#B8F4D4", strokeWidth=4, opacity=40, cap="round")
d.path("M" + " L".join("%.1f,%.1f" % (x + nx*w*0.5, y + ny*w*0.5)
       for (x, y), (nx, ny, w) in zip(ptsb[3:-3], nrmb[3:-3])),
       "Streamer inner sheen", fill=NONE, stroke="#D0F8E2", strokeWidth=4, opacity=35, cap="round")
# short covert feathers fanning at the tail root
for i, (x1, y1, x2, y2) in enumerate([(560,590,640,660),(575,585,662,646),(585,600,678,668)]):
    d.path(f"M{x1},{y1} C{x1+30},{y1+20} {x2-20},{y2-16} {x2},{y2}",
           f"Covert {i+1}", fill=NONE, stroke="#0E6B45", strokeWidth=9, opacity=80, cap="round")

# --- body: plump emerald body, crimson front ----------------------------------------
d.path("M452,296 C506,290 552,330 568,392 C586,456 600,530 596,592 "
       "C594,634 566,652 530,648 C488,664 424,660 386,624 "
       "C352,592 342,540 350,486 C358,432 380,386 408,344 "
       "C420,326 434,304 452,296 Z",
       "Body", fill=BODY_GRAD, stroke=INK, strokeWidth=7)
# crimson breast + belly sweeping up the front
d.path("M408,432 C376,460 358,506 360,552 C362,604 394,644 444,652 "
       "C478,657 512,652 536,640 C508,624 488,592 482,552 "
       "C476,510 452,466 408,432 Z",
       "Breast", fill=BREAST_GRAD, stroke=INK, strokeWidth=4)
# iridescent sheen along the breast's upper edge + belly shadow
d.path("M408,432 C444,464 470,510 480,556", "Breast sheen", fill=NONE,
       stroke="#FF9EAC", strokeWidth=7, opacity=35, cap="round")
d.path("M530,642 C500,654 460,654 432,644", "Belly shade", fill=NONE,
       stroke="#6E0E1C", strokeWidth=8, opacity=40, cap="round")

# folded wing over the back
d.path("M486,404 C540,404 584,448 592,512 C596,560 588,606 566,636 "
       "C552,616 542,580 538,540 C532,480 516,436 486,404 Z",
       "Wing", fill=WING_GRAD, stroke=INK, strokeWidth=4)
for i, (x0, y0, x1, y1) in enumerate([(512,430,576,520),(520,452,584,540),(528,476,586,566)]):
    d.path(f"M{x0},{y0} C{x0+22},{y0+16} {x1-16},{y1-14} {x1},{y1}",
           f"Wing bar {i+1}", fill=NONE, stroke="#073D28", strokeWidth=4, opacity=50, cap="round")
d.path("M492,412 C534,414 566,448 578,496", "Wing sheen", fill=NONE,
       stroke="#8AF0C4", strokeWidth=5, opacity=35, cap="round")

# tiny feet gripping the moss (quetzal feet are famously feeble)
d.path("M412,648 C416,660 428,666 440,662 M438,650 C442,660 452,664 460,660",
       "Toes", fill=NONE, stroke=INK, strokeWidth=4, cap="round")

# --- head + helmet crest ------------------------------------------------------------
d.path("M444,288 C494,282 528,312 536,352 C542,384 528,410 500,420 "
       "C466,430 424,424 398,400 C376,380 370,352 382,326 "
       "C394,302 416,292 444,288 Z",
       "Head", fill=HEAD_GRAD, stroke=INK, strokeWidth=6)
# the crest: a rounded helmet sliding over the nape
d.path("M398,332 C404,296 436,272 478,272 C522,272 552,300 556,336 "
       "C558,362 548,384 528,396 C532,368 522,344 500,330 "
       "C474,314 434,314 398,332 Z",
       "Crest", fill=CREST_GRAD, stroke=INK, strokeWidth=5)
d.path("M420,300 C446,284 492,282 522,296", "Crest sheen", fill=NONE,
       stroke="#C8FAE0", strokeWidth=7, opacity=50, cap="round")
# iridescent glow over the crown
d.shape("ellipse", "Crown glow", x=420, y=296, width=90, height=50,
        fill="#C8FAE0", opacity=20, stroke=NONE)

# face: dark cheek shadow under the eye
d.shape("ellipse", "Cheek shade", x=428, y=368, width=80, height=44,
        fill="#0A5A38", opacity=35, stroke=NONE)
# eye — dark bead with a thin pale ring
d.shape("ellipse", "Eye ring", x=404, y=344, width=36, height=36,
        fill="#0A4A30", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Pupil", x=413, y=353, width=18, height=18, fill="#101410", stroke=NONE)
d.shape("ellipse", "Glint", x=416, y=355, width=6, height=6, fill="#FFFFFF", opacity=90, stroke=NONE)
d.path("M404,344 C412,336 428,334 438,340", "Upper lid", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
# small yellow decurved beak
d.path("M398,356 C376,352 358,358 348,372 C356,384 376,390 394,384 "
       "C402,376 402,366 398,356 Z",
       "Beak", fill=lin(348, 356, 400, 384, (0, "#F4D04E"), (1, "#C8981E")),
       stroke=INK, strokeWidth=4)
d.path("M358,370 C370,364 386,362 396,366", "Beak light", fill=NONE,
       stroke="#FCEFA8", strokeWidth=3, opacity=70, cap="round")

# --- name ------------------------------------------------------------------------------
d.text("RESPLENDENT QUETZAL", "Name", x=500, y=962, size=42, font="Virelai Sans",
       color="#C8E4D4", justify="center")

d.finish("quetzal-V1R00")
