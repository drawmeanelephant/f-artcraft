#!/usr/bin/env python3
"""Saiga — field plate V2R00, a rendition of V1R00 (herd scene).

V1 was a single bust. This take is the species as it lives: a small herd
on the steppe at cold dawn, the hero in full profile walking into the
low sun, two figures hazier behind it in the morning haze. The bulbous
nose carries the species code — everything else is steppe.
1000x1000. House style: gradients + translucent shading, never flat fills.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ORIENT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "orient")
sys.path.insert(0, ORIENT)
from vc import Draw, NONE            # noqa: E402
from plate import smooth, ribbon, blend, PCX, PCY, PR  # noqa: E402

d = Draw()
d.new_doc("Saiga — Field Plate V2", 1000, 1000)

INK = "#2E2418"

# --- backdrop ----------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill={"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000],
                           "stops": [{"offset": 0, "color": "#131A2E"},
                                     {"offset": 0.5, "color": "#0C1120"},
                                     {"offset": 1, "color": "#070A14"}]}},
        stroke=NONE)

# seeded stars, kept outside the disc
s = 17
for i in range(12):
    s = (1103515245 * s + 12345) % (2**31)
    x = 30 + (s % 10000) / 10000 * 940
    s = (1103515245 * s + 12345) % (2**31)
    y = 30 + (s % 10000) / 10000 * 860
    if math.hypot(x - PCX, y - PCY) < PR - 14:
        continue
    r = 0.7 + (s % 600) / 1000 * 1.6
    d.shape("ellipse", f"Star {i+1}", x=round(x, 1), y=round(y, 1),
            width=round(r, 1), height=round(r, 1), fill="#F4E7CE",
            opacity=26 + (s % 30), stroke=NONE)

# --- plate -------------------------------------------------------------------
d.shape("ellipse", "Plate shadow", x=72, y=32, width=856, height=856,
        fill="#000000", opacity=30, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill={"gradient": {"kind": "linear", "start": [0, 60], "end": [0, 680],
                           "stops": [{"offset": 0, "color": "#232E4E"},
                                     {"offset": 0.55, "color": "#54486A"},
                                     {"offset": 0.82, "color": "#B87A54"},
                                     {"offset": 1, "color": "#E0A066"}]}},
        stroke="#241408", strokeWidth=10)
d.shape("ellipse", "Plate rim", x=86, y=46, width=828, height=828,
        fill=NONE, stroke="#C79A46", strokeWidth=4)
d.shape("ellipse", "Plate inner ring", x=110, y=70, width=780, height=780,
        fill=NONE, stroke="#C79A46", strokeWidth=2, opacity=50)

# low sun in the haze, left horizon, in the open sky ahead of the herd
d.shape("ellipse", "Sun glow", x=60, y=400, width=360, height=290,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#F6D9A0", "opacity": 55},
            {"offset": 1, "color": "#F6D9A0", "opacity": 0}]}}, stroke=NONE)
d.shape("ellipse", "Sun", x=134, y=596, width=64, height=64,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#FBE9C0"}, {"offset": 1, "color": "#E8B878"}]}},
        stroke=NONE, opacity=92)
d.shape("ellipse", "Sun kiss", x=120, y=640, width=92, height=26,
        fill="#F6D9A0", opacity=38, stroke=NONE)

# --- ground ------------------------------------------------------------------
# steppe band across the disc's lower chord
g = ["M149,690"]
wave = [(149, 690), (300, 680), (450, 686), (600, 678), (740, 684), (851, 690)]
g.append("L" + " ".join(f"{x},{y}" for x, y in wave[1:]))
for i in range(21):
    a = math.radians(33.2 + (146.8 - 33.2) * i / 20)
    g.append(f"L{PCX + PR * math.cos(a):.1f},{PCY + PR * math.sin(a):.1f}")
d.path(" ".join(g) + " Z", "Steppe",
       fill={"gradient": {"kind": "linear", "start": [0, 678], "end": [0, 880],
                          "stops": [{"offset": 0, "color": "#7A6038"},
                                    {"offset": 0.3, "color": "#4A3A22"},
                                    {"offset": 1, "color": "#241A0E"}]}},
       stroke="#E0A066", strokeWidth=2, opacity=94)
# haze band where ground meets sky
d.path(smooth([(180, 688), (400, 682), (620, 684), (830, 690)]), "Dawn haze",
       fill=NONE, stroke="#E8B878", strokeWidth=5, opacity=38, cap="round")

s = 41
for i in range(34):
    s = (1103515245 * s + 12345) % (2**31)
    x = 180 + (s % 10000) / 10000 * 640
    s = (1103515245 * s + 12345) % (2**31)
    h = 7 + (s % 1000) / 1000 * 13
    lean = ((s % 200) / 1000 - 0.1) * 12
    d.shape("line", f"Grass {i+1}", x1=round(x, 1), y1=768,
            x2=round(x + lean, 1), y2=round(768 - h, 1),
            stroke="#D9B98A", strokeWidth=1.5, opacity=26, cap="round")

# --- the saiga ---------------------------------------------------------------
def saiga(ox, oy, sc, haze, label, hero=False):
    """Herd figure facing left. haze 0..1 blends the coat into the dawn."""
    # palette, hazened
    coat_hi = blend("#D9B98A", "#E0A066", haze * 0.85)
    coat_mid = blend("#B08A56", "#C89B62", haze * 0.8)
    coat_lo = blend("#7A5A32", "#9A7A4A", haze * 0.7)
    hoof = blend("#241A0E", "#4A3A22", haze * 0.6)
    sw = 2.0 * sc if hero else 1.2
    op = 97 - haze * 25

    def P(pts):  # scale+translate local -> canvas
        return [(ox + x * sc, oy + y * sc) for x, y in pts]

    # far legs first
    for k, lx in enumerate([176, 336, 148, 306]):
        far = k < 2
        foot = [(lx, 18), (lx - 3, 52), (lx + 3, 80), (lx - 5, 100)]
        tone0 = blend(coat_lo, "#241A0E", 0.35) if far else coat_mid
        d.path(ribbon(P(foot), [15, 11, 8, 6])[0], f"{label} leg {k+1}",
               fill={"gradient": {"kind": "linear", "start": [round(ox, 1), round(oy, 1)],
                                  "end": [round(ox, 1), round(oy + 100 * sc, 1)],
                                  "stops": [{"offset": 0, "color": tone0},
                                            {"offset": 1, "color": hoof}]}},
               stroke=INK, strokeWidth=1.6 * sc, opacity=op - (14 if far else 0))
        d.shape("rectangle", f"{label} hoof {k+1}", x=ox + (lx - 8) * sc,
                y=oy + 96 * sc, width=15 * sc, height=9 * sc, radius=2.5 * sc,
                fill=hoof, stroke=NONE, opacity=88)

    # body+neck as ONE spine: head base -> neck -> chest -> back -> rump
    spine = [(56, -80), (78, -50), (98, -22), (122, 4), (158, -8),
             (196, -18), (238, -22), (278, -14), (312, 2), (336, 20)]
    widths = [26, 38, 56, 80, 102, 112, 114, 108, 88, 56]
    bd, L, R, norms = ribbon(P(spine), [w * sc for w in widths])
    d.path(bd, f"{label} body",
           fill={"gradient": {"kind": "linear", "start": [round(ox, 1), round(oy - 90 * sc, 1)],
                              "end": [round(ox, 1), round(oy + 70 * sc, 1)],
                              "stops": [{"offset": 0, "color": coat_hi},
                                        {"offset": 0.45, "color": coat_mid},
                                        {"offset": 1, "color": coat_lo}]}},
           stroke=INK, strokeWidth=sw, opacity=op)

    # head + bulbous nose as ONE silhouette: the bulb droops over the mouth
    hx, hy = ox + 40 * sc, oy - 84 * sc
    head_pts = [(2, -22), (-18, -22), (-36, -16), (-50, -6), (-58, 6),
                (-59, 17), (-50, 26), (-38, 24), (-28, 17), (-14, 22),
                (2, 24), (14, 12), (16, -6)]
    d.path(smooth([(hx + x * sc, hy + y * sc) for x, y in head_pts], closed=True),
           f"{label} head",
           fill={"gradient": {"kind": "linear", "start": [round(hx, 1), round(hy - 24 * sc, 1)],
                              "end": [round(hx, 1), round(hy + 26 * sc, 1)],
                              "stops": [{"offset": 0, "color": coat_hi},
                                        {"offset": 0.55, "color": coat_mid},
                                        {"offset": 1, "color": coat_lo}]}},
           stroke=INK, strokeWidth=sw, opacity=op)
    d.path(smooth([(hx - 46 * sc, hy + 20 * sc), (hx - 36 * sc, hy + 26 * sc),
                   (hx - 24 * sc, hy + 21 * sc)]), f"{label} mouth",
           fill=NONE, stroke=INK, strokeWidth=1.5 * sc, opacity=60, cap="round")

    # horn: single near-side horn, ringed (the far one dropped — it read as a fork)
    hb = [(4, -18), (-2, -58), (4, -92), (14, -106)]
    d.path(ribbon([(hx + x * sc, hy + y * sc) for x, y in hb],
                  [15, 12, 9, 6])[0], f"{label} horn",
           fill={"gradient": {"kind": "linear", "start": [round(hx, 1), round(hy - 106 * sc, 1)],
                              "end": [round(hx, 1), round(hy - 18 * sc, 1)],
                              "stops": [{"offset": 0, "color": "#E8D5B0"},
                                        {"offset": 0.5, "color": "#C8A870"},
                                        {"offset": 1, "color": "#8A6A3A"}]}},
           stroke=INK, strokeWidth=1.4 * sc, opacity=92 - haze * 22)
    if hero:
        for j in range(6):
            yy = hy + (-26 - j * 13) * sc
            d.shape("line", f"{label} horn ring {j+1}",
                    x1=round(hx + (1) * sc), y1=round(yy),
                    x2=round(hx + (14) * sc), y2=round(yy),
                    stroke="#6A4E28", strokeWidth=1.3 * sc, opacity=45, cap="round")

    # ear behind the horn base + eye
    d.shape("ellipse", f"{label} ear", x=hx + 16 * sc, y=hy - 34 * sc,
            width=26 * sc, height=13 * sc, fill=coat_lo, stroke=INK,
            strokeWidth=1.3 * sc, rotation=-38, opacity=op)
    if hero:
        d.shape("ellipse", f"{label} eye", x=hx - 20 * sc, y=hy - 14 * sc,
                width=10 * sc, height=10 * sc, fill="#181008", stroke=NONE)
        d.shape("ellipse", f"{label} eye catch", x=hx - 18 * sc, y=hy - 12 * sc,
                width=3.4 * sc, height=3.4 * sc, fill="#F6E3B8", opacity=80, stroke=NONE)
        # dawn rim light on the body's actual top edge (R, stations 2..7)
        d.path(smooth(R[2:8]), f"{label} rim light", fill=NONE, stroke="#F6E3B8",
               strokeWidth=2.6 * sc, opacity=50, cap="round")

# far figures first, hero last (walking into the sun, left)
saiga(560, 560, 0.56, 0.85, "Herd far")
saiga(430, 548, 0.72, 0.6, "Herd mid")
saiga(150, 540, 1.0, 0.0, "Saiga", hero=True)

# --- rim redrawn so nothing leaks past the disc ---------------------------------
d.shape("ellipse", "Backdrop mask", x=-200, y=-240, width=1400, height=1400,
        fill=NONE, stroke={"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000],
                                        "stops": [{"offset": 0, "color": "#131A2E"},
                                                  {"offset": 0.5, "color": "#0C1120"},
                                                  {"offset": 1, "color": "#070A14"}]}},
        strokeWidth=560)
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#241408", strokeWidth=6)
d.shape("ellipse", "Rim highlight", x=88, y=48, width=824, height=824,
        fill=NONE, stroke="#C79A46", strokeWidth=2, opacity=22)

# --- caption -----------------------------------------------------------------
n = d.text("SAIGA", "Name", x=500, y=962, size=60, font="Virelai Sans",
           color="#F2E3C8", justify="center")
d.cmd("text.setStyle", "Name tracking", ids=[n["id"]], tracking=34)

d.finish("saiga-V2R00")
