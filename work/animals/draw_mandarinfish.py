#!/usr/bin/env python3
"""Mandarinfish — field plate V1R00. Synchiropus splendidus rising off a
coral head at mating dusk: six centimetres of psychedelia — ember-orange
flank wrapped in cobalt-and-green swirl bands, a male's filamented first
dorsal, fan pectoral and pelvic fins, everything translucent over the
deep indigo water. Coral-head plate, dusk mood — reef mass closing on
the disc arc, last-light glow behind, a few rising bubbles. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Mandarinfish — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420          # plate disc centre + radius
INK = "#1C1210"                    # warm dark ink, never pure black

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    ss = []
    for s in stops:
        st = {"offset": s[0], "color": s[1]}
        if len(s) > 2: st["opacity"] = s[2]
        ss.append(st)
    return {"gradient": {"kind": "radial", "stops": ss}}

def on_disc(x, y, pad=0):
    return math.hypot(x - CX, y - CY) <= R - pad

def disc_x(y, side):
    return CX + side * math.sqrt(R * R - (y - CY) ** 2)

BG_GRAD   = lin(0, 0, 0, 1000, (0, "#0A0C1A"), (1, "#04060E"))
PLATE_GRAD = rad((0, "#3E545C"), (0.5, "#223640"), (1, "#0E1218"))
BODY_GR  = rad((0, "#E08C40"), (0.5, "#B85A2C"), (1, "#5E2E1E"))
CORAL_GR = lin(0, 700, 0, 870, (0, "#5E3A50"), (0.6, "#3E2A3C"), (1, "#1C1620"))
FIN_GR   = lin(0, 0, 0, 60, (0, "#E8A050"), (1, "#8E4424"))

# --- backdrop + dusk-water plate -----------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
for i, (x, y, w) in enumerate([(148,116,4),(854,118,5),(116,446,3),(874,502,4),
                               (180,736,4),(854,756,4),(264,148,3)]):
    d.shape("ellipse", f"Sky fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#C4D4DC", opacity=24, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#3E545C", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#18222A", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C4D4DA", strokeWidth=3, opacity=34)

# last-light glow: the dusk sun through the water column, behind the fish
d.shape("ellipse", "Dusk glow", x=300, y=260, width=420, height=320,
        fill=rad((0, "#E8A860", 30), (0.55, "#E8A860", 10), (1, "#E8A860", 0)),
        stroke=NONE)
# plankton motes + patina flecks
for i, (x, y, w) in enumerate([(308,178,4),(452,142,5),(592,170,4),(226,268,3),
                               (370,222,4),(524,194,3),(690,150,4),(250,418,3),
                               (750,432,4),(206,560,3)]):
    assert on_disc(x, y, 15), (x, y)
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#D0DCD8", opacity=38, stroke=NONE)
# a few bubbles rising off the coral
for i, (x, y, w) in enumerate([(660, 620, 8), (678, 566, 6), (648, 510, 5),
                               (690, 470, 4)]):
    d.shape("ellipse", f"Bubble {i+1}", x=x, y=y, width=w, height=w,
            fill=NONE, stroke="#A8C8CC", strokeWidth=2.5, opacity=55)

# --- the coral head: a branching mass closing on the disc arc ------------------------
cy = 778
cl, cr = disc_x(cy, -1), disc_x(cy, 1)
d.path(f"M{cl:.1f},{cy} L{cr:.1f},{cy} A{R},{R} 0 0 1 {cl:.1f},{cy} Z",
       "Reef floor", fill=CORAL_GR, stroke=NONE)
# coral branches rising from the floor
for i, (bx, by, bw, bh, lean) in enumerate([(300, 778, 90, 110, -18),
                                           (430, 778, 120, 140, 6),
                                           (560, 778, 100, 120, 14),
                                           (680, 778, 80, 96, 24)]):
    d.path(f"M{bx},{by} C{bx - bw*0.2},{by - bh*0.5} {bx + lean*0.4 - bw*0.3},{by - bh*0.8} {bx + lean},{by - bh} "
           f"C{bx + lean + bw*0.35},{by - bh*0.8} {bx + bw*0.3},{by - bh*0.4} {bx + bw*0.4},{by} "
           f"L{bx + bw*0.15},{by} C{bx + bw*0.1},{by - bh*0.3} {bx + bw*0.05},{by - bh*0.1} {bx},{by} Z",
           f"Coral {i+1}", fill=lin(bx, by - bh, bx, by,
           (0, "#6E4458"), (1, "#241C28")), stroke=INK, strokeWidth=3.5)
    # lit branch tips
    d.path(f"M{bx + lean - 6},{by - bh + 2} C{bx + lean},{by - bh - 4} {bx + lean + 6},{by - bh - 4} {bx + lean + 8},{by - bh + 4} "
           f"C{bx + lean + 4},{by - bh + 10} {bx + lean - 2},{by - bh + 10} {bx + lean - 6},{by - bh + 2} Z",
           f"Coral tip {i+1}", fill="#C87888", opacity=80, stroke=NONE)
# coral shadow under the hovering fish
d.shape("ellipse", "Fish shadow", x=380, y=740, width=260, height=34,
        fill="#06060C", opacity=45, stroke=NONE)

# === fins behind the body: tail fan, dorsal, anal =====================================
# tail fan
d.path("M676,478 C716,452 756,446 782,456 C796,462 800,474 792,486 "
       "C802,496 800,510 788,518 C758,538 716,540 678,530 Z",
       "Tail fin", fill=rad((0, "#D88038"), (0.6, "#A0502A"), (1, "#5E2E1E", 70)),
       stroke=INK, strokeWidth=4)
for k in range(3):
    d.path(f"M688,{486 + k*14} C720,{478 + k*16} 752,{472 + k*16} 780,{474 + k*14}",
           f"Tail ray {k+1}", fill=NONE, stroke="#5E2E1E", strokeWidth=3,
           opacity=60, cap="round")
# second dorsal: low long fin along the back
d.path("M470,412 C530,392 596,390 650,412 C662,418 664,428 656,434 "
       "C600,416 534,416 478,432 C468,428 464,420 470,412 Z",
       "Dorsal fin", fill=FIN_GR, stroke=INK, strokeWidth=3.5)
# male's filamented first dorsal spine — the erectile display spike
d.path("M452,424 C442,382 442,342 458,306 C466,288 476,278 484,274 "
       "C480,296 478,324 480,352 C482,382 478,408 470,426 Z",
       "Dorsal filament", fill=lin(455, 280, 475, 425, (0, "#F0B060"),
       (1, "#8E4424")), stroke=INK, strokeWidth=3.5)
# anal fin along the lower rear body, rooted on the belly edge
d.path("M560,548 C610,560 652,584 674,614 C678,622 672,628 662,624 "
       "C624,606 588,582 562,558 Z",
       "Anal fin", fill=rad((0, "#C86C30"), (1, "#6E3420", 80)),
       stroke=INK, strokeWidth=3.5)
# pelvic fins: the long fingers under the throat — signature of the species
for sgn, lab in ((-1, "near"), (1, "far")):
    px = 430 + (0 if sgn < 0 else 26)
    op = 95 if sgn < 0 else 55
    d.path(f"M{px},560 C{px-8},{590} {px-6},{624} {px+6},{652} "
           f"C{px+10},{658} {px+16},{654} {px+16},{644} "
           f"C{px+12},{620} {px+12},{590} {px+16},{566} Z",
           f"Pelvic fin {lab}", fill=lin(px, 560, px, 654,
           (0, "#D88038"), (1, "#6E3420")), stroke=INK, strokeWidth=3,
           opacity=op)

# === the body: elongate, ember-orange ================================================
d.path("M344,470 "                                   # mouth point
       "C368,442 410,424 456,418 "                   # forehead/nape
       "C510,410 570,414 620,428 "                   # back line
       "C656,438 678,454 688,474 "                   # into the tail stock
       "C690,490 684,506 668,516 "                   # caudal peduncle
       "C630,540 570,552 514,550 "                   # belly line back
       "C462,548 414,534 384,512 "                   # throat
       "C360,494 346,480 344,470 Z",
       "Body", fill=BODY_GR, stroke=INK, strokeWidth=5.5)

# === the psychedelia: cobalt + green swirl bands over the orange =====================
# wavy transverse bands contained to the flank — each ends at the local
# belly line, never dangling into open water
for i, (bx, yt, yb, col) in enumerate([(424, 442, 526, "#2E8EAC"),
                                       (470, 426, 542, "#3E9E62"),
                                       (520, 424, 544, "#2E8EAC"),
                                       (570, 428, 540, "#3E9E62"),
                                       (618, 440, 524, "#2E8EAC"),
                                       (658, 452, 508, "#3E9E62")]):
    ym = (yt + yb) / 2
    d.path(f"M{bx},{yt} C{bx - 16},{ym - 26} {bx + 14},{ym - 8} {bx - 4},{ym + 14} "
           f"C{bx - 12},{ym + 28} {bx - 2},{yb - 8} {bx + 5},{yb}",
           f"Swirl band {i+1}", fill=NONE, stroke=col, strokeWidth=14,
           opacity=85, cap="round")
    # the thin ember-orange keyline hugging each band
    d.path(f"M{bx + 11},{yt + 6} C{bx + 1},{ym - 14} {bx + 24},{ym + 2} {bx + 9},{ym + 24}",
           f"Swirl keyline {i+1}", fill=NONE, stroke="#F0B060", strokeWidth=4,
           opacity=70, cap="round")
# flank spots between the bands
for i, (x, y, w) in enumerate([(448, 530, 10), (500, 470, 8), (548, 528, 9),
                               (596, 480, 8), (644, 520, 7)]):
    d.shape("ellipse", f"Flank spot {i+1}", x=x, y=y, width=w, height=w*0.8,
            fill="#1E5E44", opacity=80, stroke=NONE)
# maze stripes on the cheek
for i, (y0, bow) in enumerate([(452, -10), (468, 4), (484, 12)]):
    d.path(f"M370,{y0} C398,{y0 + bow} 420,{y0 + bow + 6} 438,{y0 + 4}",
           f"Cheek maze {i+1}", fill=NONE, stroke="#2E8EAC", strokeWidth=5,
           opacity=85, cap="round")
# belly sheen
d.path("M390,512 C440,536 510,548 570,542 C520,556 444,552 398,528 Z",
       "Belly sheen", fill="#F0C080", opacity=45, stroke=NONE)

# pectoral fan: translucent amber fan behind the gill, mid flank
d.path("M492,496 C464,506 448,534 450,564 C452,588 466,602 486,604 "
       "C510,606 528,588 534,560 C538,534 528,508 510,498 "
       "C504,494 497,493 492,496 Z",
       "Pectoral fin", fill=rad((0, "#E89A4E", 80), (1, "#8E4424", 55)),
       stroke=INK, strokeWidth=3.5)
for k in range(4):
    a = math.radians(-40 + k * 26)
    d.path(f"M500,548 L{500 + 40*math.cos(a):.0f},{548 + 40*math.sin(a):.0f}",
           f"Fan ray {k+1}", fill=NONE, stroke="#7E3C20", strokeWidth=2.5,
           opacity=70, cap="round")

# === head details ====================================================================
# big high-set eye with a gold iris
d.shape("ellipse", "Eye", x=368, y=440, width=34, height=34,
        fill=rad((0, "#F0C060"), (0.7, "#C08030"), (1, "#6E4018")),
        stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Pupil", x=377, y=449, width=16, height=16,
        fill="#14100C", stroke=NONE)
d.shape("ellipse", "Glint", x=380, y=448, width=7, height=7,
        fill="#FFFFFF", opacity=90, stroke=NONE)
# mouth — the small pursed terminal mouth
d.path("M344,468 C350,464 358,464 362,470 C356,474 350,476 344,474 Z",
       "Mouth", fill="#5E2E1E", stroke=NONE)
# gill slit
d.path("M414,452 C406,472 404,494 408,514", "Gill slit", fill=NONE,
       stroke="#5E2E1E", strokeWidth=3.5, opacity=80, cap="round")
# warm rim light along the back from the dusk glow
d.path("M400,428 C470,408 560,410 632,432", "Back rim", fill=NONE,
       stroke="#F0C080", strokeWidth=5, opacity=32, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#0C1218", strokeWidth=6)

# --- captions -----------------------------------------------------------------------
r1 = d.text("MANDARINFISH", "Name", x=500, y=930, size=58,
            font="Virelai Sans", color="#C4D4DA", justify="center")
r2 = d.text("SYNCHIROPUS SPLENDIDUS", "Second line", x=500, y=968, size=22,
            font="Virelai Sans", color="#8FA8AC", justify="center")
d.cmd("text.setStyle", "Second line tracking", id=r2["id"], tracking=280)

def find(o, oid):
    if isinstance(o, dict):
        if o.get("id") == oid and "bounds" in o: return o
        o = list(o.values())
    if isinstance(o, list):
        for v in o:
            hit = find(v, oid)
            if hit: return hit
layers = d.call("inspect_document", {}, "inspect")["layers"]
for r, lab, wmax in [(r1, "name", 800), (r2, "line2", 760)]:
    b = find(layers, r["id"])["bounds"]
    print(lab, "bounds", {k: round(v) for k, v in b.items()})
    assert b["width"] <= wmax and b["x"] >= 100 and b["y"] + b["height"] <= 990, b

d.finish("mandarinfish-V1R00")
