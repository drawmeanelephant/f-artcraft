#!/usr/bin/env python3
"""Galileo Galilei — milestone card V1R00. Millstone ruff over a dark
robe, receding hair and the pointed beard; one hand grips a small
brass-bound telescope angled upward at a cratered moon hanging in the
dark behind him. Slate-night plate. Bust closes on the disc's own lower
arc. 1000x1000. House style: gradients + translucent shading, never
flat fills. Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Galileo Galilei — Milestone Card", 1000, 1000)

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


BG_GRAD = lin(0, 0, 0, 1000, (0, "#12141C"), (1, "#05060A"))
PLATE_GRAD = rad((0, "#6E7A8E"), (0.5, "#3C4658"), (1, "#181E2A"))
SKIN_GRAD = lin(430, 320, 505, 540, (0, "#DFC09E"), (0.55, "#BD9A7C"), (1, "#8B6950"))
SKIN_DIM = lin(430, 320, 505, 540, (0, "#BC9A7C"), (1, "#7A5A44"))
HAIR_DARK = "#3E3022"
BEARD_GRAD = lin(440, 450, 500, 550, (0, "#B09A7E"), (1, "#5C4A36"))
RUFF_GRAD = lin(390, 525, 555, 620, (0, "#E8E0C8"), (0.55, "#B4AA8E"), (1, "#6E6550"))
ROBE_GRAD = lin(300, 560, 700, 850, (0, "#2E2A26"), (0.5, "#1B1712"), (1, "#0D0A07"))
BRASS_GRAD = lin(600, 560, 700, 450, (0, "#9A7E4C"), (0.5, "#6E5430"), (1, "#3E2E18"))
MOON = "#E4E0CE"

# --- backdrop + slate-night plate ---------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#28303E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D2D8E4", strokeWidth=3, opacity=34)

# thin light pooling upper-left
d.shape("ellipse", "Light pool", x=230, y=170, width=360, height=210,
        fill="#DEE4F0", opacity=10, stroke=NONE)

# --- the cratered moon in the upper dark ----------------------------------------------
MX, MY, MR = 705, 220, 62
d.shape("ellipse", "Moon halo", x=MX - MR * 1.7, y=MY - MR * 1.7,
        width=MR * 3.4, height=MR * 3.4,
        fill=rad((0, MOON, 14), (1, MOON, 0)), stroke=NONE)
d.shape("ellipse", "Moon", x=MX - MR, y=MY - MR, width=MR * 2, height=MR * 2,
        fill=rad((0, "#F0EADA"), (0.7, MOON), (1, "#A8A694")),
        stroke="#8A8878", strokeWidth=2.5)
# craters — muted rings, low contrast
for i, (cx, cy, r, op) in enumerate([(-20, -18, 11, 45), (18, -8, 8, 40),
                                     (-6, 22, 14, 38), (26, 24, 7, 42),
                                     (-30, 12, 6, 40), (6, -30, 6, 35)]):
    x, y = MX + cx, MY + cy
    assert on_disc(x, y + r, 10), i
    d.shape("ellipse", f"Crater {i+1}", x=x - r, y=y - r * 0.8, width=2 * r,
            height=1.6 * r, fill=NONE, stroke="#8A8878", strokeWidth=2.5,
            opacity=op)
# a few faint stars kept off the face zone
for i, (x, y, r) in enumerate([(300, 190, 3), (370, 140, 2.4), (590, 130, 2.6),
                               (245, 300, 2.2), (810, 330, 2.4)]):
    assert on_disc(x, y, 12), i
    d.shape("ellipse", f"Star {i+1}", x=x - r, y=y - r, width=2 * r,
            height=2 * r, fill="#E4E8DA", opacity=55, stroke=NONE)

# --- the robe — bust silhouette closing on the disc's arc ------------------------------
fj = 802
jl, jr = rim_x(fj, -1), rim_x(fj, 1)
d.path(f"M{jl:.1f},{fj} C275,730 292,660 340,612 C380,578 418,566 444,560 "
       f"L498,560 C544,568 590,582 626,616 C666,656 690,724 {jr:.1f},{fj} "
       f"A{PR},{PR} 0 0 1 {jl:.1f},{fj} Z", "Robe",
       fill=ROBE_GRAD, stroke=INK, strokeWidth=5)
# robe folds + shoulder sheen
for i, dd in enumerate(["M370,634 C360,692 356,744 364,794",
                        "M560,632 C574,688 584,742 588,792"]):
    d.path(dd, f"Robe fold {i+1}", fill=NONE, stroke="#0E0A07",
           strokeWidth=4, opacity=45, cap="round")
d.path("M316,664 C350,624 396,594 438,580", "Shoulder sheen", fill=NONE,
       stroke="#5C5648", strokeWidth=5, opacity=30, cap="round")

# --- the millstone ruff — a pleated ring at the neck ------------------------------------
# outer ring mass, then the shadowed throat opening, then the pleats
d.path(smooth([(388, 560), (398, 538), (430, 524), (470, 520), (512, 524),
               (544, 538), (554, 560), (548, 592), (522, 612), (482, 620),
               (438, 618), (404, 604), (390, 582)], k=0.9), "Ruff",
       fill=RUFF_GRAD, stroke=INK, strokeWidth=4)
# throat shadow inside the ring
d.shape("ellipse", "Ruff throat", x=438, y=544, width=64, height=44,
        fill="#241E16", stroke=INK, strokeWidth=3)
# radial pleat folds — alternating light ridge and dark valley
for i, a in enumerate(range(15, 346, 22)):
    t = math.radians(a)
    x0, y0 = 471 + 46 * math.cos(t), 572 + 33 * math.sin(t)
    x1, y1 = 471 + 82 * math.cos(t), 570 + 52 * math.sin(t)
    d.path(f"M{x0:.0f},{y0:.0f} L{x1:.0f},{y1:.0f}", f"Pleat {i+1}",
           fill=NONE,
           stroke="#8A8066" if i % 2 else "#F4EEDA",
           strokeWidth=3, opacity=45 if i % 2 else 55, cap="round")

# neck under the ruff
d.path("M448,502 L448,556 C458,565 484,565 494,556 L494,502 Z", "Neck",
       fill=SKIN_DIM, stroke=INK, strokeWidth=3.5)

# --- head: high dome, receding dark hair, pointed beard ---------------------------------
# receding hair — a dark band clinging to the back and sides of the skull
d.path(smooth([(412, 430), (404, 380), (412, 336), (436, 306), (470, 296),
               (506, 304), (524, 336), (528, 384), (522, 432), (512, 452),
               (502, 430), (508, 384), (504, 340), (486, 316), (470, 310),
               (452, 316), (436, 340), (428, 384), (426, 430)], k=0.85),
       "Hair", fill=HAIR_DARK, stroke=INK, strokeWidth=3.5)

# face — high forehead dome
d.path(smooth([(470, 316), (518, 330), (523, 392), (514, 448), (496, 492),
               (470, 512), (444, 492), (424, 448), (413, 392), (418, 330)],
              k=0.85), "Face", fill=SKIN_GRAD, stroke=INK, strokeWidth=4)

# the pointed beard — short, squared off the chin
d.path(smooth([(428, 452), (424, 486), (436, 514), (456, 534), (470, 542),
               (484, 534), (504, 514), (514, 486), (512, 452), (498, 462),
               (442, 462)]), "Beard", fill=BEARD_GRAD, stroke=INK,
       strokeWidth=3.5)
# moustache over the beard top
d.path(smooth([(440, 464), (452, 456), (464, 454), (470, 459), (476, 454),
               (488, 456), (500, 464), (498, 474), (484, 478), (470, 478),
               (456, 478), (442, 474)]), "Moustache", fill="#6E5840",
       stroke=INK, strokeWidth=3)
d.path("M454,486 C462,490 478,490 486,486", "Mouth", fill=NONE,
       stroke="#6E4638", strokeWidth=3.5, opacity=70, cap="round")
# beard strands
for i, dd in enumerate(["M442,478 C446,498 452,516 460,530",
                        "M470,482 C470,502 470,518 470,532",
                        "M500,478 C496,498 490,516 482,530"]):
    d.path(dd, f"Beard strand {i+1}", fill=NONE, stroke="#C8B696",
           strokeWidth=3, opacity=40, cap="round")

# features — intent, weighing
d.path("M428,392 C439,386 453,386 461,391", "Brow L", fill=NONE,
       stroke="#46382A", strokeWidth=4.5, opacity=75, cap="round")
d.path("M480,391 C490,386 503,386 511,392", "Brow R", fill=NONE,
       stroke="#46382A", strokeWidth=4.5, opacity=75, cap="round")
d.path("M431,410 C438,403 453,403 460,410 C453,417 438,417 431,410 Z",
       "Eye L", fill="#EFE4D0", stroke=INK, strokeWidth=3)
d.path("M480,410 C487,403 502,403 509,410 C502,417 487,417 480,410 Z",
       "Eye R", fill="#EFE4D0", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Iris L", x=442, y=404, width=11, height=12,
        fill="#2E221A", stroke=NONE)
d.shape("ellipse", "Iris R", x=491, y=404, width=11, height=12,
        fill="#2E221A", stroke=NONE)
d.shape("ellipse", "Glint L", x=445, y=406, width=3.5, height=3.5,
        fill="#FFF4DC", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=494, y=406, width=3.5, height=3.5,
        fill="#FFF4DC", opacity=90, stroke=NONE)
# nose — straight, a little long
d.path("M473,416 C478,432 478,448 471,460", "Nose shade", fill=NONE,
       stroke="#9A7658", strokeWidth=3.5, opacity=45, cap="round")
d.path("M461,462 C467,466 477,466 483,461", "Nose base", fill=NONE,
       stroke="#8A6248", strokeWidth=3, opacity=55, cap="round")
d.path("M420,428 C423,446 430,460 440,468", "Cheek shade", fill=NONE,
       stroke="#9A7658", strokeWidth=5, opacity=22, cap="round")

# --- raised arm + the telescope angled up at the moon ------------------------------------
# one axis: grip end GA to sky tip GB; every fitting is computed off it
GA, GB = (604, 574), (704, 436)
ax, ay = GB[0] - GA[0], GB[1] - GA[1]
al = math.hypot(ax, ay)
ux, uy = ax / al, ay / al          # along the tube, toward the sky
vx, vy = -uy, ux                   # across the tube
TW = 24

# forearm rising from the right shoulder to the grip
d.path(smooth([(588, 610), (616, 598), (640, 582), (652, 560), (646, 540),
               (628, 534), (614, 548), (606, 574), (596, 596), (586, 606)]),
       "Sleeve raised", fill=ROBE_GRAD, stroke=INK, strokeWidth=4.5)

# the tube itself — a tapered quad, wider at the objective
def tube_pt(t, off):
    w = TW / 2 * (1 + t * 0.25)      # widens slightly toward the sky end
    return (GA[0] + ax * t + vx * off * w,
            GA[1] + ay * t + vy * off * w)


p = [tube_pt(0, -1), tube_pt(1, -1), tube_pt(1, 1), tube_pt(0, 1)]
d.path("M%.1f,%.1f L%.1f,%.1f L%.1f,%.1f L%.1f,%.1f Z"
       % (p[0] + p[1] + p[2] + p[3]), "Telescope",
       fill=BRASS_GRAD, stroke=INK, strokeWidth=4)
# draw_shape can't rotate — bands and caps are strokes/quads off the axis
for i, t in enumerate([0.3, 0.55, 0.8]):
    c = (GA[0] + ax * t, GA[1] + ay * t)
    d.path("M%.1f,%.1f L%.1f,%.1f"
           % (c[0] - vx * TW * 0.62, c[1] - vy * TW * 0.62,
              c[0] + vx * TW * 0.62, c[1] + vy * TW * 0.62),
           f"Tube band {i+1}", fill=NONE, stroke="#C8A868",
           strokeWidth=3.5, opacity=85, cap="round")
# eyepiece cap at the grip end, objective ring at the sky end
ep = [(GA[0] - ux * 12 + vx * s * TW * 0.62, GA[1] - uy * 12 + vy * s * TW * 0.62)
      for s in (-1, 1)] + \
     [(GA[0] + vx * s * TW * 0.55, GA[1] + vy * s * TW * 0.55)
      for s in (1, -1)]
d.path("M%.1f,%.1f L%.1f,%.1f L%.1f,%.1f L%.1f,%.1f Z"
       % (ep[0] + ep[1] + ep[2] + ep[3]), "Eyepiece",
       fill="#3A2C16", stroke=INK, strokeWidth=3)
ob = [(GB[0] + vx * s * TW * 0.80, GB[1] + vy * s * TW * 0.80)
      for s in (-1, 1)] + \
     [(GB[0] + ux * 8 + vx * s * TW * 0.80, GB[1] + uy * 8 + vy * s * TW * 0.80)
      for s in (1, -1)]
d.path("M%.1f,%.1f L%.1f,%.1f L%.1f,%.1f L%.1f,%.1f Z"
       % (ob[0] + ob[1] + ob[2] + ob[3]), "Objective rim",
       fill="#5C4626", stroke=INK, strokeWidth=3)
# fist wrapped over the tube's lower third
gc = (GA[0] + ax * 0.12, GA[1] + ay * 0.12)
d.path(smooth([(gc[0] - 14, gc[1] - 20), (gc[0] - 4, gc[1] - 32),
               (gc[0] + 12, gc[1] - 30), (gc[0] + 20, gc[1] - 18),
               (gc[0] + 18, gc[1] - 4), (gc[0] + 6, gc[1] + 6),
               (gc[0] - 10, gc[1] + 4)]), "Hand grip",
       fill=SKIN_GRAD, stroke=INK, strokeWidth=3.5)
for i, t in enumerate([0.06, 0.15]):
    c = (GA[0] + ax * t, GA[1] + ay * t)
    d.path("M%.1f,%.1f L%.1f,%.1f"
           % (c[0] - vx * TW * 0.85, c[1] - vy * TW * 0.85,
              c[0] + vx * TW * 0.55, c[1] + vy * TW * 0.55),
           f"Grip line {i+1}", fill=NONE, stroke="#8A6248",
           strokeWidth=2.5, opacity=70, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#242C3A", strokeWidth=6)

# --- captions ----------------------------------------------------------------------------
d.text("GALILEO GALILEI", "Name", x=500, y=934, size=56, font="Virelai Sans",
       color="#E8ECE6", justify="center")
LINE2, SZ2, TRK = "STARRY MESSENGER · 1610", 22, 480
r = d.text(LINE2, "Milestone", x=500, y=970, size=SZ2, font=SS3,
           color="#BEC6C8", justify="center")
d.cmd("text.setStyle", "Milestone tracking", id=r["id"], tracking=TRK)

b = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("milestone bounds", {k: round(v) for k, v in b.items()})
nearest = (min(max(PCX, b["x"]), b["x"] + b["width"]),
           min(max(PCY, b["y"]), b["y"] + b["height"]))
clear = math.hypot(nearest[0] - PCX, nearest[1] - PCY) - (PR + 3)
print("clears rim by %.1f" % clear)
assert clear > 0 and b["width"] <= 760 and b["x"] >= 10 and b["x"] + b["width"] <= 990, b

d.finish("galileo-galilei-V1R00")
