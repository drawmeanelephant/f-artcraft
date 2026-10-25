#!/usr/bin/env python3
"""Axolotl — psychedelic poster rendition V3R00. 60s concert-poster idiom:
radiating colour-wave bands out of the gills, vibrating pink/cyan on deep
purple, drips into the lower third, halo rings, warped display lettering.
Rendition rules: flat + gradient fills allowed, translucent overlays
encouraged, no plate disc, no house dark-ink backdrop. 1000x1000, all art
inside the 60pt safe margin; the field itself runs edge to edge."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Axolotl — Psychedelic Poster V3R00", 1000, 1000)

CX, CY = 500, 480          # radiation centre, behind the head
VIOLET = "#3A0A52"         # poster ink — deep violet, not warm dark ink
PINK   = "#FF2E9A"
PINK_L = "#FF8FC8"
CYAN   = "#1FD8E0"
CYAN_D = "#0FA8C8"
YELLOW = "#FFDE3A"
LIME   = "#A8F03A"

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def radO(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c, "opacity": a} for o, c, a in stops]}}

def wavy_ring(r0, amp, lobes, phase=0.0, steps=120):
    """Closed wobbly circle centred on (CX,CY) — a colour-wave band."""
    pts = []
    for i in range(steps):
        t = 2 * math.pi * i / steps
        r = r0 + amp * math.sin(lobes * t + phase)
        pts.append((CX + r * math.cos(t), CY + r * math.sin(t)))
    dd = "M%.1f,%.1f " % pts[0]
    # smooth it with quadratic segments through midpoints
    for i in range(steps):
        p = pts[(i + 1) % steps]
        q = pts[(i + 2) % steps]
        mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
        dd += "Q%.1f,%.1f %.1f,%.1f " % (p[0], p[1], mx, my)
    return dd + "Z"

# --- field: deep purple, hot core behind the head ------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin(0, 0, 1000, 1000, (0, "#2A0656"), (0.55, "#20043F"), (1, "#12022A")),
        stroke=NONE)
d.shape("ellipse", "Hot core", x=190, y=170, width=620, height=620,
        fill=radO((0, "#B4128C", 55), (0.5, "#6E0E78", 30), (1, "#6E0E78", 0)), stroke=NONE)

# radiating colour-wave bands — wavy rings pouring out of the gill centre;
# max radius 405 + 12 wobble keeps the band inside the 60pt margin
RING_COLS = [PINK, CYAN, YELLOW, "#B13AFF", PINK, CYAN, LIME, PINK, CYAN, YELLOW]
for i, r0 in enumerate(range(150, 406, 27)):
    d.path(wavy_ring(r0, 11, 8, i * 1.7), f"Wave band {i+1}", fill=NONE,
           stroke=RING_COLS[i % len(RING_COLS)], strokeWidth=21, opacity=88)

# halo rings circling the head, broken and hot
d.shape("ellipse", "Halo inner", x=280, y=260, width=440, height=440,
        fill=NONE, stroke=YELLOW, strokeWidth=6, dash=[26, 14], opacity=95)
d.shape("ellipse", "Halo outer", x=258, y=238, width=484, height=484,
        fill=NONE, stroke="#FFFFFF", strokeWidth=3, dash=[6, 18], opacity=70)

# sparkles flung off the bands, kept inside the margin
for i, (x, y, s, col) in enumerate([
        (108, 116, 16, YELLOW), (884, 108, 14, CYAN), (104, 872, 15, PINK),
        (890, 866, 17, YELLOW), (72, 500, 12, CYAN), (928, 486, 12, PINK),
        (180, 200, 9, "#FFFFFF"), (826, 208, 9, "#FFFFFF"),
        (170, 786, 10, LIME), (830, 780, 10, LIME)]):
    d.path(f"M{x},{y - s} L{x + s * 0.28},{y - s * 0.28} L{x + s},{y} "
           f"L{x + s * 0.28},{y + s * 0.28} L{x},{y + s} "
           f"L{x - s * 0.28},{y + s * 0.28} L{x - s},{y} "
           f"L{x - s * 0.28},{y - s * 0.28} Z",
           f"Sparkle {i+1}", fill=col, opacity=90, stroke=NONE)

# --- drips: paint sliding off the colour field into the lower third ------------
def drip(x, y0, y1, sway, w, col, label):
    xm = x + sway
    d.path(f"M{x},{y0} C{xm},{y0 + (y1 - y0) * 0.35} {x - sway},{y0 + (y1 - y0) * 0.7} {x + sway * 0.4:.1f},{y1}",
           f"{label} run", fill=NONE, stroke=col, strokeWidth=w, cap="round", opacity=92)
    d.shape("ellipse", f"{label} bulb", x=x + sway * 0.4 - w * 0.85, y=y1 - w * 0.55,
            width=w * 1.7, height=w * 1.5, fill=col, opacity=92, stroke=NONE)

for i, (x, y0, y1, sw, w, col) in enumerate([
        (262, 596, 812, 26, 15, CYAN), (330, 630, 760, -20, 12, PINK),
        (398, 660, 838, 22, 14, YELLOW), (462, 676, 800, -16, 11, "#B13AFF"),
        (545, 676, 832, 18, 13, CYAN), (612, 656, 768, -24, 12, PINK),
        (676, 622, 846, 20, 15, LIME), (742, 590, 788, -18, 12, YELLOW)]):
    drip(x, y0, y1, sw, w, col, f"Drip {i+1}")

# === the axolotl ================================================================
# gills: cyan stalks with hot-pink feathering, fanned wide — the explosion
# the colour bands seem to pour out of. Stalks stay nearly straight; the
# feathering does the work.
def quad_pt(p0, p1, p2, t):
    return ((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0],
            (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1])

def gill(bx, by, tipx, tipy, label):
    # gentle bow: control point nudged perpendicular to the stalk
    dx, dy = tipx - bx, tipy - by
    ln = math.hypot(dx, dy) or 1
    ux, uy = dx / ln, dy / ln          # along the stalk
    nx, ny = -uy, ux                   # normal
    mx, my = (bx + tipx) / 2 + nx * 18, (by + tipy) / 2 + ny * 18
    p0, p1, p2 = (bx, by), (mx, my), (tipx, tipy)
    d.path(f"M{bx},{by} Q{mx:.0f},{my:.0f} {tipx},{tipy}", f"{label} stalk",
           fill=NONE, stroke=lin(bx, by, tipx, tipy, (0, "#8FF4F4"), (1, CYAN_D)),
           strokeWidth=16, cap="round")
    # dense alternating feathering on both sides of the stalk
    for j in range(12):
        t = 0.10 + 0.82 * j / 11
        px, py = quad_pt(p0, p1, p2, t)
        side = 1 if j % 2 == 0 else -1
        L = 30 * (1 - 0.45 * t) + 4
        fx = px + (nx * side * 0.72 + ux * 0.62) * L
        fy = py + (ny * side * 0.72 + uy * 0.62) * L
        d.path(f"M{px:.1f},{py:.1f} L{fx:.1f},{fy:.1f}",
               f"{label} filament {j+1}", fill=NONE,
               stroke=PINK_L if j % 2 == 0 else "#FF5FAE",
               strokeWidth=4.6, cap="round", opacity=94)
    # hot tip bead — where the drip starts
    d.shape("ellipse", f"{label} tip", x=tipx - 9, y=tipy - 9, width=18, height=18,
            fill=PINK, stroke=NONE)

for bx, by, tx, ty, lab in [
        (336, 430, 222, 288, "Gill L1"), (316, 490, 176, 414, "Gill L2"),
        (316, 552, 188, 566, "Gill L3"), (340, 606, 244, 664, "Gill L4"),
        (664, 430, 778, 288, "Gill R1"), (684, 490, 824, 414, "Gill R2"),
        (684, 552, 812, 566, "Gill R3"), (660, 606, 756, 664, "Gill R4")]:
    gill(bx, by, tx, ty, lab)

# gill roots
d.shape("ellipse", "Gill base L", x=292, y=440, width=56, height=180,
        fill="#E85FA8", stroke=NONE)
d.shape("ellipse", "Gill base R", x=652, y=440, width=56, height=180,
        fill="#E85FA8", stroke=NONE)

# head: neon pink dome, violet outline
d.path("M500,382 C632,382 706,452 708,546 C710,626 640,672 500,672 "
       "C360,672 290,626 292,546 C294,452 368,382 500,382 Z",
       "Head", fill=lin(500, 382, 500, 672, (0, "#FFB3D9"), (0.55, "#FF5FAE"), (1, "#D82E88")),
       stroke=VIOLET, strokeWidth=8)
d.shape("ellipse", "Head glow", x=380, y=396, width=240, height=74,
        fill="#FFFFFF", opacity=20, stroke=NONE)
d.path("M384,634 C444,656 556,656 616,634 C556,646 444,646 384,634 Z",
       "Chin shade", fill="#B01270", opacity=45, stroke=NONE)
# neon speckles
for i, (x, y, w, col) in enumerate([(388, 448, 7, YELLOW), (458, 418, 6, CYAN),
                                    (562, 420, 7, YELLOW), (622, 458, 6, CYAN),
                                    (368, 562, 6, "#B13AFF"), (636, 558, 7, "#B13AFF"),
                                    (502, 432, 5, CYAN)]):
    d.shape("ellipse", f"Speckle {i+1}", x=x, y=y, width=w, height=w,
            fill=col, opacity=80, stroke=NONE)

# face: big vibrating eyes, the little smile
for lab, ex in (("L", 404), ("R", 584)):
    d.shape("ellipse", f"Eye ring {lab}", x=ex - 8, y=498, width=44, height=52,
            fill=CYAN, opacity=90, stroke=NONE)
    d.shape("ellipse", f"Eye {lab}", x=ex, y=505, width=28, height=36,
            fill="#2A0A3E", stroke=NONE)
    d.shape("ellipse", f"Glint {lab}", x=ex + 7, y=511, width=9, height=9,
            fill="#FFFFFF", opacity=95, stroke=NONE)
d.shape("ellipse", "Nostril L", x=458, y=584, width=9, height=7, fill="#8A2A60", opacity=75, stroke=NONE)
d.shape("ellipse", "Nostril R", x=533, y=584, width=9, height=7, fill="#8A2A60", opacity=75, stroke=NONE)
d.path("M404,600 C448,624 552,624 596,600", "Smile", fill=NONE, stroke=VIOLET,
       strokeWidth=8, cap="round")

# --- lettering -------------------------------------------------------------------
# "AXOLOTL" letter-by-letter along a top arc — each glyph placed on the
# baseline circle and rotated tangent to it. Virelai Sans fakes the
# psychedelic display face; a cyan ghost under each letter keeps the
# overprint vibrato without wrecking legibility.
def arc_text(word, cx, cy, radius, span_deg, size, font, label):
    n = len(word)
    for i, ch in enumerate(word):
        # screen coords: y down. -90deg is the arc's top; letters spread
        # symmetrically about it
        th = math.radians(-90 + (i - (n - 1) / 2) * span_deg)
        x = cx + radius * math.cos(th)
        y = cy + radius * math.sin(th)
        rot = math.degrees(th) + 90          # tangent, CCW-positive
        ghost = d.text(ch, f"{label} ghost {i+1}", x=x + 5, y=y + 5, size=size,
                       font=font, color=CYAN, justify="center")
        if ghost:
            d.cmd("object.rotate", f"{label} ghost rot {i+1}",
                  ids=[ghost["id"]], angle=rot, origin=[x + 5, y + 5])
        r = d.text(ch, f"{label} {i+1}", x=x, y=y, size=size, font=font,
                   color=YELLOW, justify="center")
        if r:
            d.call("set_paint", {"ids": [r["id"]], "stroke": PINK,
                                 "strokeWidth": 3.5}, f"{label} stroke {i+1}")
            d.cmd("object.rotate", f"{label} rot {i+1}",
                  ids=[r["id"]], angle=rot, origin=[x, y])

arc_text("AXOLOTL", 500, 780, 620, 8.2, 112, "Virelai Sans", "Title")

sub = d.text("AMBLYSTOMA MEXICANUM", "Subline", x=500, y=916, size=30,
             font="Source Sans 3", color="#BFEBF5", justify="center")
if sub:
    d.cmd("text.setStyle", "Subline tracking", ids=[sub["id"]], tracking=240)

d.finish("axolotl-V3R00")
