#!/usr/bin/env python3
"""bunny-avatar-V2R00 — the ERROR badge gone noir: dark coin, thin gold ring,
one lamp from the upper-left, the red of the stamp doing all the talking.
1000x1000, riffing on bunny-avatar-V1R01."""
from vc import Draw, NONE
from v2style import backdrop, glow, vignette, ship

d = Draw()
d.new_doc("Bunny Avatar V2R00", 1000, 1000)
CX = 500

backdrop(d, 1000, 1000, top="#141020", mid="#1e1830", bottom="#090614")

# badge: dark coin + gold ring
d.shape("ellipse", "Badge", x=70, y=70, width=860, height=860,
        stroke=NONE, fill={"gradient": {"kind": "radial", "start": [360, 300], "end": [560, 640],
            "stops": [{"offset": 0, "color": "#3d3227"},
                      {"offset": 0.7, "color": "#241d14"},
                      {"offset": 1, "color": "#171208"}]}})
d.shape("ellipse", "Ring", x=70, y=70, width=860, height=860,
        fill=NONE, stroke="#c9a25a", strokeWidth=5)
d.shape("ellipse", "Inner ring", x=96, y=96, width=808, height=808,
        fill=NONE, stroke="#7a6238", strokeWidth=2)
glow(d, "Lamp", 370, 320, 300, "#ffcf8a", 30)

# --- ears --------------------------------------------------------------------------
for i, (ex, tilt) in enumerate([(436, -8), (564, 8)]):
    d.shape("ellipse", f"Ear {i}", x=ex - 42, y=150, width=84, height=270,
            rotation=tilt, stroke=NONE,
            fill={"gradient": {"kind": "linear", "start": [ex, 150], "end": [ex, 430],
                  "stops": [{"offset": 0, "color": "#a89b82"},
                            {"offset": 1, "color": "#5e5340"}]}})
    d.shape("ellipse", f"Inner ear {i}", x=ex - 24, y=185, width=48, height=200,
            rotation=tilt, fill="#3a3024", stroke=NONE, opacity=70)

# --- head: radial-lit from the lamp side ----------------------------------------------
d.shape("ellipse", "Head", x=310, y=380, width=380, height=360,
        stroke=NONE, fill={"gradient": {"kind": "radial", "start": [400, 460], "end": [560, 660],
            "stops": [{"offset": 0, "color": "#b8ab90"},
                      {"offset": 0.75, "color": "#7a6e58"},
                      {"offset": 1, "color": "#4e4534"}]}})

# heavy-lidded eyes
for i, ex in enumerate([430, 570]):
    d.shape("ellipse", f"Eye {i}", x=ex - 30, y=520, width=60, height=62,
            fill="#241c10", stroke=NONE)
    d.shape("ellipse", f"Glint {i}", x=ex - 14, y=532, width=12, height=12,
            fill="#e8d8b8", stroke=NONE, opacity=70)
    d.path(f"M{ex-38},526 C{ex-18},508 {ex+18},508 {ex+38},526",
           f"Lid {i}", fill=NONE, stroke="#3a3024", strokeWidth=8, cap="round")
# frown
d.path("M455,668 C480,652 520,652 545,668", "Frown", fill=NONE,
       stroke="#3a3024", strokeWidth=7, cap="round")
# whiskers
for side, sgn in [("L", -1), ("R", 1)]:
    for j, (dy, tilt) in enumerate([(-8, -6), (12, 0), (32, 6)]):
        x0 = CX + sgn * 185
        x1 = CX + sgn * 285
        d.path(f"M{x0},{600+dy} L{x1},{600+dy+tilt*sgn}", f"Whisker {side}{j}",
               fill=NONE, stroke="#4e4534", strokeWidth=4, cap="round", opacity=75)

# --- bowtie ----------------------------------------------------------------------------
d.path("M452,762 L502,744 L502,790 Z M548,762 L498,744 L498,790 Z", "Bowtie",
       fill="#171210", stroke=NONE)
d.shape("ellipse", "Knot", x=490, y=754, width=20, height=24, fill="#2a2018", stroke=NONE)

# --- ERROR: the only warm thing in the room ----------------------------------------------
glow(d, "Stamp glow", CX, 900, 190, "#d43a2e", 22, aspect=0.35)
d.text("ERROR", "ERROR", x=CX, y=918, size=64, font="Source Sans 3",
       color="#d43a2e", justify="center")

vignette(d, 1000, 1000, opacity=45)
ship(d, "bunny-avatar", "V2R00")
