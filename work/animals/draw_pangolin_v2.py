#!/usr/bin/env python3
"""Pangolin — field plate V2R00, a rendition of V1R00 (full body).

V1 was a head-and-shoulders bust. This take is the animal whole: the
classic ground-pangolin walk, head low and sniffing, back arched into a
scale cape that runs unbroken down the tail. Moonlit night — indigo sky,
one pale moon, grass ticks on the lower arc. The cape is one continuous
silhouette over the back with three shingled rows laid inside it, pale
at the moonlit outer edge and warm beneath.
1000x1000. House style: gradients + translucent shading, never flat fills.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ORIENT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "orient")
sys.path.insert(0, ORIENT)
from vc import Draw, NONE            # noqa: E402
from plate import smooth, ribbon, PCX, PCY, PR  # noqa: E402

d = Draw()
d.new_doc("Pangolin — Field Plate V2", 1000, 1000)

INK = "#3A2230"

# --- backdrop ----------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill={"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000],
                           "stops": [{"offset": 0, "color": "#0B1226"},
                                     {"offset": 0.6, "color": "#060B1A"},
                                     {"offset": 1, "color": "#030610"}]}},
        stroke=NONE)

# seeded stars, kept outside the disc
s = 11
for i in range(14):
    s = (1103515245 * s + 12345) % (2**31)
    x = 30 + (s % 10000) / 10000 * 940
    s = (1103515245 * s + 12345) % (2**31)
    y = 30 + (s % 10000) / 10000 * 860
    if math.hypot(x - PCX, y - PCY) < PR - 14:
        continue
    r = 0.8 + (s % 700) / 1000 * 1.8
    d.shape("ellipse", f"Star {i+1}", x=round(x, 1), y=round(y, 1),
            width=round(r, 1), height=round(r, 1), fill="#F4E7CE",
            opacity=30 + (s % 35), stroke=NONE)

# --- plate -------------------------------------------------------------------
d.shape("ellipse", "Plate shadow", x=72, y=32, width=856, height=856,
        fill="#000000", opacity=30, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#1E3450"},
            {"offset": 0.55, "color": "#122338"},
            {"offset": 1, "color": "#081222"}]}},
        stroke="#0A1926", strokeWidth=10)
d.shape("ellipse", "Plate rim", x=86, y=46, width=828, height=828,
        fill=NONE, stroke="#C79A46", strokeWidth=4)
d.shape("ellipse", "Plate inner ring", x=110, y=70, width=780, height=780,
        fill=NONE, stroke="#C79A46", strokeWidth=2, opacity=50)

# moon + halo
d.shape("ellipse", "Moon glow", x=210, y=115, width=320, height=320,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#F4E7CE", "opacity": 34},
            {"offset": 1, "color": "#F4E7CE", "opacity": 0}]}}, stroke=NONE)
d.shape("ellipse", "Moon", x=294, y=199, width=152, height=152,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#FBF2DE"}, {"offset": 0.8, "color": "#F0DFBC"},
            {"offset": 1, "color": "#D8C094"}]}}, stroke=NONE, strokeWidth=0)
d.shape("ellipse", "Moon crater 1", x=326, y=232, width=22, height=22,
        fill="#D8C094", opacity=55, stroke=NONE)
d.shape("ellipse", "Moon crater 2", x=366, y=272, width=14, height=14,
        fill="#D8C094", opacity=45, stroke=NONE)
d.shape("ellipse", "Moon crater 3", x=352, y=214, width=10, height=10,
        fill="#D8C094", opacity=40, stroke=NONE)

# --- ground ------------------------------------------------------------------
g = [f"M149,690"]
wave = [(149, 690), (280, 678), (430, 684), (580, 676), (720, 682), (851, 690)]
g.append("L" + " ".join(f"{x},{y}" for x, y in wave[1:]))
arc = []
for i in range(21):
    a = math.radians(33.2 + (146.8 - 33.2) * i / 20)
    arc.append((PCX + PR * math.cos(a), PCY + PR * math.sin(a)))
g.append("L" + " ".join(f"{x:.1f},{y:.1f}" for x, y in arc))
d.path(" ".join(g) + " Z", "Ground",
       fill={"gradient": {"kind": "linear", "start": [0, 676], "end": [0, 880],
                          "stops": [{"offset": 0, "color": "#1A2A3E"},
                                    {"offset": 0.35, "color": "#0E1B2C"},
                                    {"offset": 1, "color": "#060D18"}]}},
       stroke="#3E5A78", strokeWidth=2, opacity=92)
d.path(smooth([(280, 679), (430, 685), (580, 677), (720, 683)]), "Ground moonlight",
       fill=NONE, stroke="#9FB3C8", strokeWidth=2, opacity=42, cap="round")

s = 29
for i in range(26):
    s = (1103515245 * s + 12345) % (2**31)
    x = 210 + (s % 10000) / 10000 * 580
    s = (1103515245 * s + 12345) % (2**31)
    h = 8 + (s % 1000) / 1000 * 14
    lean = ((s % 200) / 1000 - 0.1) * 14
    d.shape("line", f"Grass {i+1}", x1=round(x, 1), y1=760,
            x2=round(x + lean, 1), y2=round(760 - h, 1),
            stroke="#9FB3C8", strokeWidth=1.6, opacity=30, cap="round")

# --- pangolin ----------------------------------------------------------------
# spine nose -> head -> back -> rump -> tail tip: long and low, the thick
# tail continuing the back curve (a pangolin's tail is half the animal)
spine = [(258, 596), (300, 552), (368, 514), (452, 492), (540, 496),
         (630, 526), (712, 566), (788, 604), (846, 632), (858, 636)]
widths = [26, 54, 120, 172, 180, 170, 132, 86, 40, 14]
bd, L, R, norms = ribbon(spine, widths)

d.shape("ellipse", "Body shadow", x=280, y=664, width=380, height=30,
        fill="#04070F", opacity=32, stroke=NONE)

# far legs, darker, behind the body
def leg(x, y, h, w, label, tone=("#6B4426", "#4A2E18"), claw="#D9C29A", op=100):
    pts = [(x, y - h), (x + 6, y - h * 0.45), (x + 2, y - 6), (x - 16, y - 4)]
    pts2 = [(x - w * 0.5, y - h + 8), (x - 4, y - h * 0.4), (x - 20, y - 2)]
    d.path(smooth(pts + pts2[::-1], closed=True), label,
           fill={"gradient": {"kind": "linear", "start": [0, y - h], "end": [0, y],
                              "stops": [{"offset": 0, "color": tone[0]},
                                        {"offset": 1, "color": tone[1]}]}},
           stroke=INK, strokeWidth=2, opacity=op)
    for k in range(3):
        d.shape("line", f"{label} claw {k+1}", x1=x - 14 + k * 6, y1=y - 6,
                x2=x - 20 + k * 7, y2=y + 2, stroke=claw,
                strokeWidth=2.4, opacity=int(85 * op / 100), cap="round")

leg(404, 666, 70, 28, "Front leg far", tone=("#4A2E18", "#33200F"), claw="#B49A72", op=88)
leg(646, 668, 76, 30, "Rear leg far", tone=("#4A2E18", "#33200F"), claw="#B49A72", op=88)

# body base under the cape
d.path(bd, "Body",
       fill={"gradient": {"kind": "linear", "start": [0, 470], "end": [0, 640],
                          "stops": [{"offset": 0, "color": "#8A5A2C"},
                                    {"offset": 0.5, "color": "#6B4426"},
                                    {"offset": 1, "color": "#4A2E18"}]}},
       stroke=INK, strokeWidth=2.4)

leg(430, 668, 74, 30, "Front leg near")
leg(612, 670, 80, 32, "Rear leg near")

# --- the scale cape ----------------------------------------------------------
# one continuous armour silhouette over the back: bottom edge = the body's
# top edge (R stations 2..8), outer edge = an arc rising ~110 over the
# shoulders and tapering into the tail
top_in = [(316, 548), (368, 514), (452, 490), (540, 494), (630, 524),
          (712, 564), (790, 602), (848, 630)]          # follows R, head to tail
cape_out = [(320, 524), (380, 456), (470, 420), (560, 428), (648, 470),
            (730, 528), (806, 588), (852, 620)]        # low long arc into the tail
cape = smooth(cape_out + top_in[::-1], closed=True)
d.path(cape, "Scale cape",
       fill={"gradient": {"kind": "linear", "start": [0, 400], "end": [0, 640],
                          "stops": [{"offset": 0, "color": "#C08A4A"},
                                    {"offset": 0.55, "color": "#8A5A2C"},
                                    {"offset": 1, "color": "#5A3A22"}]}},
       stroke=INK, strokeWidth=2.4)

# shingled rows laid along the outer arc, resampled by arc length
def resample(pts, step):
    out = [pts[0]]
    acc = 0.0
    for i in range(1, len(pts)):
        ax, ay = out[-1]
        bx, by = pts[i]
        seg = math.hypot(bx - ax, by - ay)
        acc += seg
        while acc >= step:
            t = 1 - (acc - step) / seg
            out.append((ax + (bx - ax) * t, ay + (by - ay) * t))
            acc -= step
            ax, ay = out[-1]
            bx, by = pts[i]
            seg = math.hypot(bx - ax, by - ay)
        # keep walking
    return out

def normal_at(pts, i):
    ax, ay = pts[max(i - 1, 0)]
    bx, by = pts[min(i + 1, len(pts) - 1)]
    dx, dy = bx - ax, by - ay
    ln = math.hypot(dx, dy) or 1
    return -dy / ln, dx / ln

def tile(cx, cy, s, ang):
    """Rounded diamond plate, wider than tall — lies flat on the surface."""
    a = math.radians(ang)
    pts = []
    for px, py in [(0, -0.40), (0.52, 0), (0, 0.40), (-0.52, 0)]:
        rx = px * s * math.cos(a) - py * s * math.sin(a)
        ry = px * s * math.sin(a) + py * s * math.cos(a)
        pts.append((cx + rx, cy + ry))
    return pts

def row(base_pts, inset_mult, sz, tone, label, start=0, skip_tail=2):
    inset = inset_mult * sz
    pts = resample(base_pts, sz * 0.60)   # dense overlap, no gaps
    for i in range(start, len(pts) - skip_tail):
        x, y = pts[i]
        nx, ny = normal_at(pts, i)
        cx, cy = x - nx * inset, y - ny * inset
        frac = i / max(len(pts) - 1, 1)
        szi = sz * (1.0 - 0.42 * max(0.0, frac - 0.5) / 0.5)
        if szi < 12:
            continue
        ang = math.degrees(math.atan2(ny, nx)) + ((i % 2) * 2 - 1) * 3
        fill = {"gradient": {"kind": "linear", "start": [0, cy - szi], "end": [0, cy + szi],
                             "stops": [{"offset": 0, "color": tone[0]},
                                       {"offset": 0.45, "color": tone[1]},
                                       {"offset": 1, "color": tone[2]}]}}
        d.path(smooth(tile(cx, cy, szi, ang), closed=True), f"{label} {i}",
               fill=fill, stroke=INK, strokeWidth=1.2, opacity=92)

# three shingled rows: outer row's tips kiss the cape edge, deeper rows
# tuck underneath it — dark seams between plates carry the armour read
row(cape_out, 0.42, 58, ("#F6E7C2", "#D9A05E", "#7A4E2E"), "Scale edge")
row(cape_out, 0.90, 54, ("#E8C88E", "#C08A4A", "#6B4426"), "Scale mid")
row(cape_out, 1.38, 48, ("#C89B62", "#8A5A2C", "#5A3A22"), "Scale deep")

# head crown plates easing the cape into the naked snout
for k, (hx, hy, hs) in enumerate([(330, 528, 34), (352, 512, 30), (376, 500, 26)]):
    d.path(smooth(tile(hx, hy, hs, -38 + k * 8), closed=True), f"Head plate {k+1}",
           fill={"gradient": {"kind": "linear", "start": [0, hy - hs], "end": [0, hy + hs],
                              "stops": [{"offset": 0, "color": "#F6E7C2"},
                                        {"offset": 0.5, "color": "#D9A05E"},
                                        {"offset": 1, "color": "#7A4E2E"}]}},
           stroke=INK, strokeWidth=1.2, opacity=92)

# head: small scaled crown, eye, ear
d.shape("ellipse", "Eye", x=278, y=566, width=9, height=9, fill="#141019",
        stroke=NONE)
d.shape("ellipse", "Eye catch", x=280, y=567, width=3, height=3,
        fill="#F4E7CE", opacity=80, stroke=NONE)
d.shape("ellipse", "Ear", x=318, y=540, width=13, height=16,
        fill="#4A2E18", stroke=INK, strokeWidth=1.6, rotation=18)
d.path(smooth([(262, 606), (272, 612), (284, 608)]), "Snout line",
       fill=NONE, stroke=INK, strokeWidth=2, opacity=70, cap="round")

# tail tip pale tuft
d.shape("ellipse", "Tail tuft", x=838, y=624, width=26, height=18,
        fill="#E8D5B0", opacity=85, stroke=NONE, rotation=24)

# grass sprigs in front of the nose
for k, (gx, gh) in enumerate([(240, 22), (262, 30), (284, 18)]):
    d.shape("line", f"Nose grass {k+1}", x1=gx, y1=690, x2=gx + 6, y2=690 - gh,
            stroke="#9FB3C8", strokeWidth=1.8, opacity=40, cap="round")

# --- rim redrawn so nothing leaks past the disc ---------------------------------
d.shape("ellipse", "Backdrop mask", x=-200, y=-240, width=1400, height=1400,
        fill=NONE, stroke={"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000],
                                        "stops": [{"offset": 0, "color": "#0B1226"},
                                                  {"offset": 0.6, "color": "#060B1A"},
                                                  {"offset": 1, "color": "#030610"}]}},
        strokeWidth=560)
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#0A1926", strokeWidth=6)
d.shape("ellipse", "Rim highlight", x=88, y=48, width=824, height=824,
        fill=NONE, stroke="#C79A46", strokeWidth=2, opacity=22)

# --- caption -----------------------------------------------------------------
n = d.text("PANGOLIN", "Name", x=500, y=962, size=60, font="Virelai Sans",
           color="#E9EDF2", justify="center")
d.cmd("text.setStyle", "Name tracking", ids=[n["id"]], tracking=34)

d.finish("pangolin-V2R00")
