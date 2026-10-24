#!/usr/bin/env python3
"""fart-knocker-V2R00 — the self-portrait reconsidered: same burger crown,
monocle and bowtied tentacles, but under one amber spot on a noir field.
800x1000, riffing on fart-knocker-V1R00."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE
from tools.v2style import backdrop, glow, vignette, sparkle, ship

d = Draw()
d.new_doc("Fart Knocker V2R00", 800, 1000)
CX = 400

backdrop(d, 800, 1000)
glow(d, "Spot", CX, 430, 340, "#ff9a3d", 50)
for i, (x, y, r) in enumerate([(120, 140, 9), (660, 200, 7), (710, 90, 5),
                               (85, 330, 5), (620, 330, 4), (180, 60, 4)]):
    sparkle(d, f"Spark {i}", x, y, r)
for i, (x, y) in enumerate([(240, 200), (540, 120), (150, 420), (700, 430), (60, 220)]):
    d.shape("ellipse", f"Mote {i}", x=x - 2, y=y - 2, width=4, height=4,
            fill="#ffe9b0", stroke=NONE, opacity=55)

# --- title / footer ----------------------------------------------------------
d.text("F A R T   K N O C K E R", "Title", x=CX, y=72, size=38,
       font="Source Sans 3", color="#e8c98a", justify="center")
d.text("A  P O R T R A I T ,  R E C O N S I D E R E D", "Footer", x=CX, y=962,
       size=13, font="Source Sans 3", color="#8a7658", justify="center")

# --- burger crown --------------------------------------------------------------
d.path("M255,300 C255,168 545,168 545,300 L545,300 Z", "Bun",
       stroke=NONE, fill={"gradient": {"kind": "linear", "start": [400, 160], "end": [400, 305],
           "stops": [{"offset": 0, "color": "#e8a84c"},
                     {"offset": 1, "color": "#a8641f"}]}})
d.path("M300,215 C320,185 480,185 500,215 C480,200 320,200 300,215 Z",
       "Bun sheen", fill="#f7d28e", stroke=NONE, opacity=45)
for i, (x, y, rx) in enumerate([(300, 240, 8), (350, 210, 7), (400, 235, 8), (450, 205, 7),
                                (500, 240, 8), (330, 265, 7), (430, 270, 7), (480, 255, 6),
                                (370, 255, 6), (520, 268, 6), (280, 268, 6)]):
    d.shape("ellipse", f"Sesame {i}", x=x - rx, y=y - rx * 0.6, width=2 * rx, height=rx * 1.2,
            fill="#f7dd9a", stroke=NONE, opacity=80, rotation=(i * 37) % 50 - 25)

# lettuce ruffle: band + scallops
d.shape("rectangle", "Lettuce", x=246, y=298, width=308, height=26,
        stroke=NONE, fill={"gradient": {"kind": "linear", "start": [0, 298], "end": [0, 340],
            "stops": [{"offset": 0, "color": "#6f9a42"}, {"offset": 1, "color": "#3d6128"}]}})
for i in range(6):
    d.shape("ellipse", f"Lettuce wave {i}", x=246 + i * 51, y=315, width=56, height=30,
            fill="#4e7530", stroke=NONE)

# tomato band
d.shape("rectangle", "Tomato", x=252, y=342, width=296, height=26, radius=8,
        stroke=NONE, fill={"gradient": {"kind": "linear", "start": [0, 342], "end": [0, 370],
            "stops": [{"offset": 0, "color": "#c9402f"}, {"offset": 1, "color": "#8e2318"}]}})

# cheese with drips
d.path("M248,368 L552,368 L552,380 L520,380 L520,398 L486,398 L486,380 "
       "L446,380 L446,392 L404,392 L404,380 L366,380 L366,404 L330,404 L330,380 "
       "L292,380 L292,392 L262,392 L262,380 L248,380 Z", "Cheese",
       stroke=NONE, fill={"gradient": {"kind": "linear", "start": [0, 368], "end": [0, 404],
           "stops": [{"offset": 0, "color": "#f0b840"}, {"offset": 1, "color": "#cf8a20"}]}})

# patty
d.shape("rectangle", "Patty", x=258, y=404, width=284, height=30, radius=14,
        stroke=NONE, fill={"gradient": {"kind": "linear", "start": [0, 404], "end": [0, 434],
            "stops": [{"offset": 0, "color": "#5e3d28"}, {"offset": 1, "color": "#38210f"}]}})

# --- face ----------------------------------------------------------------------
d.shape("rectangle", "Face", x=302, y=432, width=196, height=118, radius=46,
        stroke=NONE, fill={"gradient": {"kind": "radial", "start": [370, 460], "end": [430, 530],
            "stops": [{"offset": 0, "color": "#f2a55c"}, {"offset": 1, "color": "#cf7038"}]}})
# eye
d.shape("ellipse", "Eye", x=428, y=458, width=24, height=30, fill="#241408", stroke=NONE)
d.shape("ellipse", "Eye glint", x=432, y=462, width=8, height=8, fill="#fff6e8", stroke=NONE)
# smile
d.path("M420,512 C436,522 452,522 466,512", "Smile", fill=NONE,
       stroke="#7a3c1c", strokeWidth=4, cap="round")
# monocle: rim + lens + glint + dotted chain
d.shape("ellipse", "Monocle lens", x=318, y=440, width=66, height=66,
        fill="#fff2d8", stroke=NONE, opacity=18)
d.shape("ellipse", "Monocle rim", x=318, y=440, width=66, height=66,
        fill=NONE, stroke="#d4a24a", strokeWidth=4.5)
d.path("M330,458 C334,448 342,443 350,443", "Monocle glint", fill=NONE,
       stroke="#fff6e8", strokeWidth=4, cap="round", opacity=85)
d.path("M351,506 C352,540 344,565 348,595", "Monocle chain", fill=NONE,
       stroke="#d4a24a", strokeWidth=2.5, dash=[0.5, 6], cap="round")

# bowtie
d.path("M368,584 L398,572 L398,604 Z M432,584 L402,572 L402,604 Z",
       "Bowtie", fill="#241022", stroke=NONE)
d.shape("ellipse", "Bowtie knot", x=392, y=578, width=16, height=20, fill="#3a1a30", stroke=NONE)

# --- tentacle body: overlapping lobes -------------------------------------------
for i, (lx, ly, lw, lh) in enumerate([(176, 690, 150, 300), (290, 720, 140, 280),
                                      (372, 720, 140, 280), (478, 690, 150, 300)]):
    d.shape("ellipse", f"Lobe {i}", x=lx, y=ly, width=lw, height=lh,
            stroke=NONE, fill={"gradient": {"kind": "radial",
                "start": [lx + lw * 0.35, ly + lh * 0.3], "end": [lx + lw * 0.7, ly + lh * 0.8],
                "stops": [{"offset": 0, "color": "#c25a33"}, {"offset": 1, "color": "#782c17"}]}})
d.shape("ellipse", "Shoulders", x=200, y=590, width=400, height=160,
        stroke=NONE, fill={"gradient": {"kind": "radial", "start": [330, 620], "end": [460, 730],
            "stops": [{"offset": 0, "color": "#c25a33"}, {"offset": 1, "color": "#782c17"}]}})
# suction cups
for i, (x, y, r) in enumerate([(232, 780, 8), (252, 850, 7), (330, 800, 8), (348, 868, 7),
                               (452, 800, 8), (434, 868, 7), (560, 780, 8), (540, 850, 7)]):
    d.shape("ellipse", f"Cup {i}", x=x - r, y=y - r, width=2 * r, height=2 * r,
            fill="#f0a875", stroke=NONE, opacity=60)
# floor shadow
d.shape("ellipse", "Shadow", x=210, y=952, width=380, height=28, fill="#050308",
        stroke=NONE, opacity=55)

vignette(d, 800, 1000)
ship(d, "fart-knocker", "V2R00")
