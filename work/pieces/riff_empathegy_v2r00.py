#!/usr/bin/env python3
"""empathegy-brochure-V2R00 — the tri-fold's thesis as a poster: EMPATHET,
a heart processed through a form field and stamped FILED. Warm noir, one
gold seal. 800x1000, riffing on empathegy-brochure-V1R01."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE
from v2style import backdrop, glow, vignette, ship

d = Draw()
d.new_doc("Empathegy V2R00", 800, 1000)
CX = 400

backdrop(d, 800, 1000, top="#221812", mid="#2e2014", bottom="#100a06")
glow(d, "Seal light", CX, 480, 280, "#e8b25c", 35)

# --- masthead ------------------------------------------------------------------------
d.text("R E F E R E N C E   S E R I E S", "Series", x=CX, y=78, size=15,
       font="Source Sans 3", color="#9a7f56", justify="center")
d.path("M180,96 L620,96", "Rule top", fill=NONE, stroke="#6a5432", strokeWidth=1.5)
d.text("EMPATHET", "Title", x=CX, y=185, size=76, font="Source Sans 3",
       color="#e8cf9a", justify="center")
d.text("EMOTIONAL GOVERNANCE FOR INSTITUTIONS", "Sub 1", x=CX, y=228, size=16,
       font="Source Sans 3", color="#b09a70", justify="center")
d.text("THAT HAVE ALREADY FELT ENOUGH", "Sub 2", x=CX, y=252, size=16,
       font="Source Sans 3", color="#b09a70", justify="center")

# --- the form field --------------------------------------------------------------------
d.shape("rectangle", "Form", x=200, y=330, width=400, height=330, radius=8,
        fill="#1c130a", stroke="#7a6238", strokeWidth=2, dash=[8, 6])
d.text("FIELD 07 — AFFECT RECEIVED", "Field label", x=220, y=362, size=13,
       font="Source Sans 3", color="#8a6f48", justify="auto")

# heart: two lobes + point, gold
d.path("M400,560 C390,528 340,500 315,530 C290,560 315,600 400,650 "
       "C485,600 510,560 485,530 C460,500 410,528 400,560 Z", "Heart",
       stroke=NONE, fill={"gradient": {"kind": "radial", "start": [370, 540], "end": [430, 630],
           "stops": [{"offset": 0, "color": "#f0c87a"},
                     {"offset": 1, "color": "#9a6a28"}]}})

# checkbox rows under the field
for i, (label, w) in enumerate([("NOTED", 90), ("CATALOGUED", 130), ("RESOLVED", 110)]):
    y = 690 + i * 40
    d.shape("rectangle", f"Box {i}", x=230, y=y, width=20, height=20,
            fill=NONE, stroke="#7a6238", strokeWidth=2)
    d.text(label, f"Row {i}", x=262, y=y + 16, size=14,
           font="Source Sans 3", color="#8a6f48")

# --- the FILED stamp, rotated across the heart ------------------------------------------
r = d.shape("rectangle", "Stamp box", x=230, y=490, width=340, height=120, radius=10,
            fill=NONE, stroke="#d43a2e", strokeWidth=8)
box_id = (r or {}).get("id")
r = d.text("FILED", "Stamp text", x=400, y=575, size=72, font="Source Sans 3",
           color="#d43a2e", justify="center")
txt_id = (r or {}).get("id")
ids = [i for i in (box_id, txt_id) if i]
if ids:
    d.call("transform", {"ids": ids, "rotate": -14, "origin": [400, 550]}, "tilt stamp")
glow(d, "Stamp bleed", 400, 550, 150, "#d43a2e", 14, aspect=0.5)

# --- footer ------------------------------------------------------------------------------
d.path("M180,880 L620,880", "Rule bottom", fill=NONE, stroke="#6a5432", strokeWidth=1.5)
d.text("FILED & FORGOTTEN", "Footer", x=CX, y=915, size=15,
       font="Source Sans 3", color="#9a7f56", justify="center")

vignette(d, 800, 1000)
ship(d, "empathegy-brochure", "V2R00")
