#!/usr/bin/env python3
"""bunny-banner-V2R00 — the office after hours: cabinet rows as dark masses,
one cone of lamplight on the bunny and its one piece of paper, the ERROR
stamp glowing like a sign. 1500x500, riffing on bunny-banner-V1R01."""
from vc import Draw, NONE
from v2style import backdrop, glow, vignette, ship

d = Draw()
d.new_doc("Bunny Banner V2R00", 1500, 500)

backdrop(d, 1500, 500, top="#1a1410", mid="#241c12", bottom="#0a0705")

# --- cabinet silhouettes: two dim rows -------------------------------------------
for row, y in enumerate([40, 260]):
    for col, x in enumerate([60, 380, 700]):
        d.shape("rectangle", f"Cabinet {row}-{col}", x=x, y=y, width=280, height=200,
                radius=6, fill="#241d12", stroke=NONE)
        d.shape("rectangle", f"Pull {row}-{col}", x=x + 95, y=y + 26, width=90, height=30,
                radius=5, fill="#3d3324", stroke=NONE, opacity=80)

# warm cone over the bunny
glow(d, "Lamp", 1050, 240, 300, "#ffcf8a", 40)
glow(d, "Floor pool", 1050, 480, 260, "#ffb35c", 20, aspect=0.25)

# --- bunny, seated with the paper ---------------------------------------------------
# ears
for i, (ex, tilt) in enumerate([(1010, -8), (1064, 8)]):
    d.shape("ellipse", f"Ear {i}", x=ex - 24, y=60, width=48, height=130,
            rotation=tilt, stroke=NONE,
            fill={"gradient": {"kind": "linear", "start": [ex, 60], "end": [ex, 190],
                  "stops": [{"offset": 0, "color": "#9a8d74"}, {"offset": 1, "color": "#554a38"}]}})
# body
d.shape("ellipse", "Body", x=930, y=300, width=240, height=180,
        stroke=NONE, fill={"gradient": {"kind": "radial", "start": [990, 340], "end": [1100, 460],
            "stops": [{"offset": 0, "color": "#b0a488"}, {"offset": 1, "color": "#544a38"}]}})
# head
d.shape("ellipse", "Head", x=950, y=150, width=190, height=170,
        stroke=NONE, fill={"gradient": {"kind": "radial", "start": [1000, 200], "end": [1080, 300],
            "stops": [{"offset": 0, "color": "#b8ab90"}, {"offset": 1, "color": "#5e5340"}]}})
# sad eyes + frown
for i, ex in enumerate([1005, 1065]):
    d.shape("ellipse", f"Eye {i}", x=ex - 14, y=220, width=28, height=34,
            fill="#20180e", stroke=NONE)
d.path("M1020,296 C1035,288 1055,288 1070,296", "Frown", fill=NONE,
       stroke="#3a3024", strokeWidth=5, cap="round")
# feet
d.shape("ellipse", "Foot L", x=920, y=452, width=90, height=30, fill="#3f3626", stroke=NONE)
d.shape("ellipse", "Foot R", x=1090, y=452, width=90, height=30, fill="#3f3626", stroke=NONE)

# the paper — the one bright thing it still holds
d.path("M985,330 L1095,318 L1105,430 L995,442 Z", "Paper",
       fill="#f2e8d0", stroke=NONE)
for i, yy in enumerate([345, 365, 385]):
    d.path(f"M1005,{yy} L1080,{yy-8}", f"Line {i}", fill=NONE,
           stroke="#8a7f6a", strokeWidth=4, cap="round", opacity=70)

# --- ERROR stamp, lit like a sign ----------------------------------------------------
glow(d, "Stamp glow", 1310, 170, 180, "#d43a2e", 30, aspect=0.5)
d.shape("rectangle", "Stamp box", x=1180, y=110, width=270, height=110, radius=14,
        fill=NONE, stroke="#d43a2e", strokeWidth=7)
d.shape("rectangle", "Stamp box inner", x=1192, y=122, width=246, height=86, radius=9,
        fill=NONE, stroke="#d43a2e", strokeWidth=3, opacity=70)
d.text("ERROR", "Stamp text", x=1315, y=195, size=56, font="Source Sans 3",
       color="#d43a2e", justify="center")

vignette(d, 1500, 500, opacity=42)
ship(d, "bunny-banner", "V2R00")
