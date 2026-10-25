#!/usr/bin/env python3
"""Nikola Tesla — milestone card V1R00. Tall, thin, sharp-mustached
inventor in a dark lab; a working coil stands at the plate's right edge
and throws faint blue arc-light across his face — contained sparks, not
a storm. Slicked dark hair, high starched collar, dark suit. The bust
closes on the disc's own lower arc. 1000x1000. House style: gradients +
translucent shading, never flat fills. Plate = circle center (500,460)
r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Nikola Tesla — Milestone Card", 1000, 1000)

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


def zig(p0, p1, n, amp):
    """Jagged polyline p0->p1: n segments, perpendicular jitter amp."""
    ax, ay = p1[0] - p0[0], p1[1] - p0[1]
    al = math.hypot(ax, ay)
    ux, uy = ax / al, ay / al
    vx, vy = -uy, ux
    pts = [p0]
    for i in range(1, n):
        t = i / n
        s = amp * (1 if i % 2 else -1) * (0.55 + 0.45 * math.sin(i * 2.3))
        pts.append((p0[0] + ax * t + vx * s, p0[1] + ay * t + vy * s))
    pts.append(p1)
    return "M" + " L".join("%.1f,%.1f" % p for p in pts)


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


ARC = "#9FDCF8"                    # contained arc blue
BG_GRAD = lin(0, 0, 0, 1000, (0, "#10141E"), (1, "#04060B"))
PLATE_GRAD = rad((0, "#5E7089"), (0.5, "#35425A"), (1, "#131A28"))
SKIN_GRAD = lin(400, 300, 500, 540, (0, "#DCC0A0"), (0.55, "#B89478"), (1, "#7E5E48"))
SKIN_DIM = lin(400, 300, 500, 540, (0, "#BC9C7E"), (1, "#74563F"))
HAIR_GRAD = lin(390, 270, 510, 460, (0, "#4A3826"), (0.5, "#2A1D12"), (1, "#120C07"))
SUIT_GRAD = lin(300, 560, 660, 850, (0, "#302B26"), (0.5, "#1B1712"), (1, "#0D0A07"))
SHIRT_GRAD = lin(430, 550, 500, 760, (0, "#E4DCC6"), (1, "#9A9078"))
COPPER_GRAD = lin(660, 430, 780, 720, (0, "#9A6A3E"), (0.5, "#6E4526"), (1, "#34200F"))
IRON_GRAD = lin(640, 340, 800, 760, (0, "#5E646E"), (0.5, "#3A3E48"), (1, "#181A20"))

# --- backdrop + slate-night lab plate ------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#26303F", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D4DCE8", strokeWidth=3, opacity=34)

# cool light pooling upper-left, faint
d.shape("ellipse", "Light pool", x=235, y=150, width=380, height=220,
        fill="#DEE6F2", opacity=9, stroke=NONE)

# --- the coil's blue light is the plate's second key -----------------------------
TX, TY = 716, 332                  # toroid terminal centre
d.shape("ellipse", "Arc wash", x=TX - 205, y=TY - 135, width=360,
        height=300, fill=rad((0, ARC, 16), (0.6, ARC, 7), (1, ARC, 0)),
        stroke=NONE)
d.shape("ellipse", "Arc halo", x=TX - 100, y=TY - 88, width=200,
        height=176, fill=rad((0, "#D8F0FF", 40), (0.55, ARC, 18),
        (1, ARC, 0)), stroke=NONE)

# --- lab floor: a chord band closed on the disc's own arc -----------------------
fj = 790
jl, jr = rim_x(fj, -1), rim_x(fj, 1)
d.path(f"M{jl:.1f},{fj} C360,776 640,776 {jr:.1f},{fj} "
       f"A{PR},{PR} 0 0 1 {jl:.1f},{fj} Z", "Lab floor",
       fill=lin(0, 770, 0, 880, (0, "#3A3630"), (0.55, "#221E19"),
                (1, "#0F0C09")), stroke=INK, strokeWidth=4)
# the coil's light pooling on the floorboards — kept inside the rim
d.shape("ellipse", "Floor glow", x=TX - 60, y=786, width=96, height=24,
        fill=rad((0, ARC, 22), (1, ARC, 0)), stroke=NONE)

# --- the coil — one vertical axis, every fitting derived -------------------------
CX = 716                           # coil axis
TOP, BOT = 368, 718                # secondary top / base of windings
CW = 62                            # secondary diameter

# plinth on the floor — corners kept inside the rim
d.path("M654,724 L766,724 L776,764 L648,764 Z", "Coil plinth",
       fill=IRON_GRAD, stroke=INK, strokeWidth=4)
# secondary winding cylinder — tapered slightly, narrower at the top
d.path(smooth([(CX - CW / 2, BOT), (CX - CW / 2 - 4, (TOP + BOT) / 2),
               (CX - CW / 2 + 2, TOP), (CX + CW / 2 - 2, TOP),
               (CX + CW / 2 + 4, (TOP + BOT) / 2), (CX + CW / 2, BOT)],
              k=0.9), "Secondary", fill=COPPER_GRAD, stroke=INK,
       strokeWidth=4.5)
# helix windings — diagonal strokes marching up the cylinder
for i, y in enumerate(range(BOT - 14, TOP + 8, -19)):
    t = (y - TOP) / (BOT - TOP)
    hw = CW / 2 + 3 * math.sin(t * math.pi)
    d.path(f"M{CX - hw:.1f},{y:.1f} L{CX + hw:.1f},{y - 11:.1f}",
           f"Winding {i+1}", fill=NONE,
           stroke="#B8824E" if i % 3 else "#3A2410",
           strokeWidth=3, opacity=70 if i % 3 else 55, cap="round")
# primary base turns — three fat rings at the foot
for i, (w, y) in enumerate([(108, 730), (96, 744), (84, 758)]):
    d.shape("ellipse", f"Primary {i+1}", x=CX - w / 2, y=y - 9, width=w,
            height=18, fill=NONE, stroke="#8A5C34", strokeWidth=5,
            opacity=85)

# toroid terminal — an aluminium donut on the axis
TW2, TH2 = 96, 34
d.shape("ellipse", "Toroid", x=TX - TW2 / 2, y=TY - TH2 / 2, width=TW2,
        height=TH2,
        fill=lin(TX - 48, TY - 17, TX + 48, TY + 17,
                 (0, "#D8DCE2"), (0.5, "#8A929E"), (1, "#424854")),
        stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Toroid hole", x=TX - 26, y=TY - 8, width=52,
        height=16, fill="#1A1E26", stroke=INK, strokeWidth=3)
# short stem joining toroid to secondary
d.path("M700,352 L732,352 L726,372 L706,372 Z", "Terminal stem",
       fill="#4A505C", stroke=INK, strokeWidth=3)

# discharge ball on a thin insulated stand — the arcs' target
DX, DY = 806, 470
d.path(f"M{DX - 4},{DY + 12} L{DX + 4},{DY + 12} L{DX + 6},718 "
       f"L{DX - 6},718 Z", "Stand", fill="#2A2E36", stroke=INK,
       strokeWidth=3)
d.shape("ellipse", "Discharge ball", x=DX - 13, y=DY - 13, width=26,
        height=26, fill=rad((0, "#C2C8D2"), (1, "#565E6A")), stroke=INK,
       strokeWidth=3)
assert on_disc(DX + 13, DY, 8) and on_disc(DX + 6, 718, 8)

# contained arcs — toroid to ball, and a short leader off the toroid top
for i, (p0, p1, n, amp) in enumerate([
        ((TX + 42, TY + 6), (DX - 12, DY - 6), 5, 14),
        ((TX + 30, TY - 10), (DX - 10, DY + 6), 4, 10),
        ((TX - 8, TY - 18), (TX - 52, TY - 74), 4, 12)]):
    dd = zig(p0, p1, n, amp)
    d.path(dd, f"Arc halo {i+1}", fill=NONE, stroke=ARC, strokeWidth=9,
           opacity=22, cap="round", join="round")
    d.path(dd, f"Arc {i+1}", fill=NONE, stroke="#E4F4FF", strokeWidth=3.5,
           opacity=90, cap="round", join="round")

# --- Tesla's bust — tall suit mass closing on the disc's arc ---------------------
# placed left of centre so the coil owns the right third
fj2 = 804
kl, kr = rim_x(fj2, -1), rim_x(fj2, 1)
d.path(f"M{kl:.1f},{fj2} C296,726 316,652 352,606 C382,572 416,560 442,554 "
       f"L486,554 C528,562 566,584 592,622 C620,662 640,730 {kr:.1f},{fj2} "
       f"A{PR},{PR} 0 0 1 {kl:.1f},{fj2} Z", "Suit",
       fill=SUIT_GRAD, stroke=INK, strokeWidth=5)
# lapels — the jacket's V over the shirt
d.path("M406,560 L452,560 L470,600 L458,716 L430,660 Z", "Lapel L",
       fill=lin(406, 560, 458, 716, (0, "#26211C"), (1, "#100D0A")),
       stroke=INK, strokeWidth=4)
d.path("M486,560 L516,568 L508,700 L472,604 Z", "Lapel R",
       fill=lin(486, 560, 508, 700, (0, "#221D18"), (1, "#0E0B08")),
       stroke=INK, strokeWidth=4)
# shirt front — a narrow white wedge between the lapels
d.path("M452,566 L488,566 L474,700 L458,700 Z", "Shirt front",
       fill=SHIRT_GRAD, stroke=INK, strokeWidth=3.5)
# dark cravat at the throat
d.path(smooth([(452, 562), (470, 556), (490, 562), (486, 584), (470, 592),
               (456, 584)]), "Cravat",
       fill=lin(452, 556, 490, 592, (0, "#2E2830"), (1, "#14101A")),
       stroke=INK, strokeWidth=3.5)
d.path("M470,592 L462,648 L474,676 L482,646 Z", "Cravat tail",
       fill="#1A1420", stroke=INK, strokeWidth=3, opacity=85)
# shoulder sheen — faint blue kiss of the arc light on the right side
d.path("M574,612 C604,652 620,706 630,762", "Shoulder sheen",
       fill=NONE, stroke=ARC, strokeWidth=7, opacity=18, cap="round")

# stiff starched collar — two white wings at the neck
d.path("M424,540 L456,532 L470,556 L452,574 L428,566 Z", "Collar L",
       fill=SHIRT_GRAD, stroke=INK, strokeWidth=3.5)
d.path("M470,556 L484,532 L512,540 L508,566 L488,574 Z", "Collar R",
       fill=SHIRT_GRAD, stroke=INK, strokeWidth=3.5)
# neck
d.path("M448,498 L448,542 C458,550 480,550 488,542 L488,498 Z", "Neck",
       fill=SKIN_DIM, stroke=INK, strokeWidth=3.5)

# --- head: high forehead, slicked hair, thin sharp moustache ---------------------
# hair — combed straight back off a high hairline; dark mass hugging the skull
d.path(smooth([(400, 436), (388, 388), (390, 336), (406, 296), (438, 272),
               (476, 278), (498, 306), (504, 352), (500, 404), (494, 432),
               (486, 412), (490, 366), (486, 326), (470, 300), (448, 294),
               (424, 302), (408, 330), (402, 372), (404, 414)], k=0.85),
       "Hair", fill=HAIR_GRAD, stroke=INK, strokeWidth=3.5)
# swept-back sheen bands in the hair
for i, dd in enumerate(["M412,330 C426,308 448,296 470,300",
                        "M406,366 C420,338 444,322 472,326",
                        "M404,400 C416,372 438,354 466,356"]):
    d.path(dd, f"Hair sweep {i+1}", fill=NONE, stroke="#6A5238",
           strokeWidth=3, opacity=45, cap="round")

# face — long and narrow, tapering to the chin
d.path(smooth([(448, 308), (486, 326), (492, 384), (486, 440), (474, 488),
               (458, 514), (446, 520), (434, 514), (416, 488), (404, 440),
               (398, 384), (404, 326)], k=0.85), "Face",
       fill=SKIN_GRAD, stroke=INK, strokeWidth=4)
# arc-light rim on the right cheek and temple — the coil's kiss
d.path("M490,330 C496,380 494,432 484,478", "Rim light cheek",
       fill=NONE, stroke=ARC, strokeWidth=4, opacity=38, cap="round")

# ears — small, tight to the skull
d.path("M396,400 C390,404 388,418 394,430 C398,436 404,434 406,426",
       "Ear L", fill=SKIN_DIM, stroke=INK, strokeWidth=3)
d.path("M494,404 C500,408 502,422 496,432", "Ear R", fill=SKIN_DIM,
       stroke=INK, strokeWidth=3, opacity=90)

# features — deep-set eyes under a straight brow, intent sideways gaze
d.path("M408,392 C419,386 434,385 444,391", "Brow L", fill=NONE,
       stroke="#3E2E20", strokeWidth=4.5, opacity=80, cap="round")
d.path("M452,391 C463,385 477,386 486,393", "Brow R", fill=NONE,
       stroke="#3E2E20", strokeWidth=4.5, opacity=80, cap="round")
# under-brow shadow — the deep set
d.path("M410,404 C420,398 436,398 444,403", "Eye shade L", fill=NONE,
       stroke="#8A6248", strokeWidth=4, opacity=35, cap="round")
d.path("M454,403 C464,398 478,399 485,405", "Eye shade R", fill=NONE,
       stroke="#8A6248", strokeWidth=4, opacity=35, cap="round")
d.path("M412,416 C419,409 434,409 441,415 C434,422 419,422 412,416 Z",
       "Eye L", fill="#EFE4D0", stroke=INK, strokeWidth=3)
d.path("M455,415 C462,408 476,408 483,414 C476,421 462,421 455,415 Z",
       "Eye R", fill="#EFE4D0", stroke=INK, strokeWidth=3)
# gaze angled right — toward the coil
d.shape("ellipse", "Iris L", x=426, y=410, width=10, height=12,
        fill="#2E221A", stroke=NONE)
d.shape("ellipse", "Iris R", x=468, y=409, width=10, height=12,
        fill="#2E221A", stroke=NONE)
d.shape("ellipse", "Glint L", x=430, y=412, width=3.4, height=3.4,
        fill="#D8F0FF", opacity=95, stroke=NONE)
d.shape("ellipse", "Glint R", x=472, y=411, width=3.4, height=3.4,
        fill="#D8F0FF", opacity=95, stroke=NONE)
# nose — long and straight
d.path("M447,414 C452,432 453,450 448,464", "Nose shade", fill=NONE,
       stroke="#9A7658", strokeWidth=3.5, opacity=45, cap="round")
d.path("M440,466 C447,471 457,471 463,466", "Nose base", fill=NONE,
       stroke="#8A6248", strokeWidth=3, opacity=55, cap="round")
# cheek hollows — the thin face
d.path("M404,428 C408,450 414,468 424,480", "Cheek shade L", fill=NONE,
       stroke="#9A7658", strokeWidth=5, opacity=24, cap="round")

# the sharp moustache — a narrow, lip-width bar, slightly level ends
d.path(smooth([(418, 480), (434, 476), (446, 475), (458, 476), (474, 480),
               (472, 487), (457, 489), (446, 489), (435, 489), (420, 487)],
              k=0.9), "Moustache", fill="#38281C", stroke=INK,
       strokeWidth=2.5)
d.path("M434,499 C441,503 451,503 458,499", "Mouth", fill=NONE,
       stroke="#6E4638", strokeWidth=3.5, opacity=70, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#242E3C", strokeWidth=6)

# --- captions ---------------------------------------------------------------------
d.text("NIKOLA TESLA", "Name", x=500, y=934, size=56, font="Virelai Sans",
       color="#E8ECE8", justify="center")
LINE2, SZ2, TRK = "ALTERNATING CURRENT · 1888", 22, 460
r = d.text(LINE2, "Milestone", x=500, y=970, size=SZ2, font=SS3,
           color="#BCC6CC", justify="center")
d.cmd("text.setStyle", "Milestone tracking", id=r["id"], tracking=TRK)

b = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("milestone bounds", {k: round(v) for k, v in b.items()})
nearest = (min(max(PCX, b["x"]), b["x"] + b["width"]),
           min(max(PCY, b["y"]), b["y"] + b["height"]))
clear = math.hypot(nearest[0] - PCX, nearest[1] - PCY) - (PR + 3)
print("clears rim by %.1f" % clear)
assert clear > 0 and b["width"] <= 760 and b["x"] >= 10 and b["x"] + b["width"] <= 990, b

d.finish("nikola-tesla-V1R00")
