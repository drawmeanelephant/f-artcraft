#!/usr/bin/env python3
"""Loch Ness monster — field-guide plate V1R00. The classic read: a long neck
out of peat-dark water, two humps behind it, ring ripples spreading. Highland
dusk: low hills and a ruined tower on the far shore, mist on the water,
the loch floor closing on the disc's own arc. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Loch Ness Monster — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420          # plate disc centre + radius
INK = "#141A12"

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [dict({"offset": o, "color": c},
                           **({"opacity": p[0]} if p and p[0] is not None else {}))
                      for o, c, *p in stops]}}

def on_disc(x, y, pad=0):
    return math.hypot(x - CX, y - CY) <= R - pad

BG_GRAD = lin(0, 0, 0, 1000, (0, "#0E1610"), (1, "#040704"))
PLATE_GRAD = rad((0, "#9A9C6E", None), (0.55, "#62683F", None), (1, "#2C311E", None))
HIDE_GRAD = lin(0, 290, 0, 740, (0, "#57604C"), (0.55, "#39412F"), (1, "#1F2519"))
HIDE_DARK = lin(0, 300, 0, 600, (0, "#333B29"), (1, "#1C2216"))
WATER_GRAD = lin(0, 640, 0, 880, (0, "#4A4A2E"), (0.5, "#2E2E1C"), (1, "#14140C"))

# --- backdrop + peat-dusk plate --------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#1C2414", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E0E2C2", strokeWidth=3, opacity=40)

# far shore: low highland hills under the water line
d.path("M140,664 C220,606 300,588 380,608 C440,622 470,644 500,660 "
       "C430,668 320,672 240,670 C190,668 155,666 140,664 Z",
       "Hill L", fill="#26301F", opacity=85, stroke=NONE)
d.path("M520,662 C590,614 670,596 750,610 C810,620 850,644 860,662 "
       "C780,670 660,672 580,668 C550,666 530,664 520,662 Z",
       "Hill R", fill="#222B1B", opacity=80, stroke=NONE)
# ruined tower on the left shore — Urquhart keep
d.path("M216,662 L216,596 L226,596 L226,586 L240,586 L240,596 L248,596 L248,662 Z",
       "Ruin", fill="#1A2215", opacity=85, stroke=NONE)
d.path("M226,620 L240,620 L240,634 L226,634 Z", "Ruin window", fill="#9A9C6E", opacity=30, stroke=NONE)
# mist lying on the water
for i, (y, op, w_) in enumerate([(590, 20, 9), (622, 15, 6), (646, 12, 4)]):
    d.path(f"M160,{y} C300,{y-12} 470,{y+8} 640,{y-4} C730,{y-10} 800,{y-4} 845,{y+2}",
           f"Mist {i+1}", fill=NONE, stroke="#E0E2C2", strokeWidth=w_, opacity=op, cap="round")
# midges over the loch
for i, (x, y, w) in enumerate([(240,380,4),(330,300,5),(460,240,4),(640,220,5),(760,330,4),
                               (840,460,4),(180,520,5),(280,470,3),(560,180,3),(700,270,3)]):
    assert on_disc(x, y, 12), (x, y)
    d.shape("ellipse", f"Midge {i+1}", x=x, y=y, width=w, height=w, fill="#D8DAB0", opacity=40, stroke=NONE)

# --- the loch: surface swells slightly, floor closes on the disc arc -------------
ly = 668
ldx = math.sqrt(R * R - (ly - CY) ** 2)
d.path(f"M{CX-ldx:.1f},{ly} C330,652 460,662 570,656 C670,650 760,660 {CX+ldx:.1f},{ly} "
       f"A{R},{R} 0 0 1 {CX-ldx:.1f},{ly} Z", "Loch water", fill=WATER_GRAD, stroke=NONE)
# surface sheen
d.path(f"M{CX-ldx+8:.1f},{ly-4} C330,650 460,658 570,652 C670,646 760,656 {CX+ldx-10:.1f},{ly-4}",
       "Water sheen", fill=NONE, stroke="#C9CC9E", strokeWidth=4, opacity=30, cap="round")
# a drowned log drifting, right of centre
d.path("M700,702 C730,694 764,694 790,702 C764,710 730,710 700,702 Z",
       "Log", fill="#2E2E1C", opacity=70, stroke=NONE)

# --- the humps: two dark shoulders breaking the surface ---------------------------
d.path("M598,704 C604,662 636,640 676,642 C712,644 736,670 740,708 "
       "C700,714 640,714 598,704 Z",
       "Hump 1", fill=HIDE_GRAD, stroke=INK, strokeWidth=5)
d.path("M722,718 C726,692 748,678 774,680 C798,682 812,698 814,720 "
       "C784,728 748,728 722,718 Z",
       "Hump 2", fill=HIDE_DARK, opacity=90, stroke=INK, strokeWidth=5)
# wet gleam along the hump crowns
d.path("M622,678 C640,660 668,654 692,660", "Hump gleam 1",
       fill=NONE, stroke="#A8AC7E", strokeWidth=4, opacity=45, cap="round")
d.path("M742,696 C754,686 772,684 786,690", "Hump gleam 2",
       fill=NONE, stroke="#A8AC7E", strokeWidth=3, opacity=35, cap="round")

# --- the neck: one curve from the water up to a small wary head --------------------
NECK = ("M505,735 C500,680 506,612 518,546 C528,490 536,440 534,398 "
        "C530,372 514,354 492,346 C470,338 448,340 434,352 "
        "C424,360 420,372 424,382 C432,392 448,396 464,392 "
        "C478,388 486,378 488,366 C492,398 488,438 478,486 "
        "C466,544 458,610 460,668 C461,694 464,716 470,735 Z")
d.path(NECK, "Neck", fill=HIDE_GRAD, stroke=INK, strokeWidth=6)
# head plane: brow, eye, nostril, the slight smile
d.path("M440,352 C448,344 462,342 474,346 C470,356 458,362 446,360 "
       "C440,358 438,354 440,352 Z", "Brow", fill=HIDE_DARK, opacity=60, stroke=NONE)
d.shape("ellipse", "Eye", x=452, y=352, width=13, height=15, fill="#0C100A", stroke=NONE)
d.shape("ellipse", "Eye glint", x=455, y=355, width=4, height=4, fill="#FFFFFF", opacity=85, stroke=NONE)
d.shape("ellipse", "Nostril", x=430, y=372, width=7, height=5, fill="#0C100A", opacity=70, stroke=NONE)
d.path("M428,382 C440,388 456,388 468,384", "Mouth",
       fill=NONE, stroke=INK, strokeWidth=3.5, cap="round")
# neck shading: pale throat ribbon + ridge bumps along the spine
d.path("M492,380 C494,420 488,466 478,512 C468,558 464,616 466,664",
       "Throat light", fill=NONE, stroke="#8A905C", strokeWidth=10, opacity=35, cap="round")
for i, (x, y) in enumerate([(528, 420), (526, 470), (520, 520), (512, 570), (506, 620)]):
    d.shape("ellipse", f"Ridge {i+1}", x=x, y=y, width=10, height=7, fill="#57604C", opacity=60, stroke=NONE)
# waterline wake where the neck breaks the surface
d.path("M452,736 C470,726 506,722 534,728 C556,733 566,740 566,746 "
       "C540,752 496,752 468,748 C456,744 450,740 452,736 Z",
       "Neck wake", fill="#5A5A38", opacity=70, stroke=NONE)

# --- ripple rings: concentric arcs off neck + humps --------------------------------
def ripple(cx, cy, rx, ry, label, op):
    for sx in (cx - rx, cx + rx):
        assert on_disc(sx, cy + ry, 6), (sx, cy + ry)
    d.path(f"M{cx-rx},{cy} A{rx},{ry} 0 0 0 {cx+rx},{cy}",
           label, fill=NONE, stroke="#D8DAB0", strokeWidth=3, opacity=op, cap="round")

ripple(500, 738, 96, 16, "Ripple N1", 45)
ripple(500, 744, 140, 24, "Ripple N2", 30)
ripple(668, 710, 100, 16, "Ripple H1a", 40)
ripple(668, 716, 118, 20, "Ripple H1b", 26)
ripple(748, 722, 50, 11, "Ripple H2a", 35)
# long fetch ripples travelling left
d.path("M170,700 C240,694 320,694 390,700", "Fetch 1",
       fill=NONE, stroke="#D8DAB0", strokeWidth=3, opacity=25, cap="round")
d.path("M210,724 C290,718 380,718 450,724", "Fetch 2",
       fill=NONE, stroke="#D8DAB0", strokeWidth=3, opacity=18, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#0A0E08", strokeWidth=6)

# --- name ----------------------------------------------------------------------
d.text("LOCH NESS MONSTER", "Name", x=500, y=960, size=44, font="Virelai Sans",
       color="#E4E2C8", justify="center")

d.finish("loch-ness-monster-V1R00")
