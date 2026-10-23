#!/usr/bin/env python3
"""golly-V2R01 — fix pass on V2R00: the paw fingers failed (ellipse has no
radius param); draw the three finger bumps over the paw. Also a second arm
stub on the right for symmetry. Opens V2R00, saves V2R01."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE
from v2style import ship

d = Draw()
ART = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "art")
d.open(f"{ART}/golly-V2R00.vectorcraft")

for i, fx in enumerate([148, 176, 204]):
    d.shape("ellipse", f"Finger {i}", x=fx, y=366, width=26, height=38,
            fill="#f5ead0", stroke=NONE)
# right arm stub resting on the frame
d.path("M610,560 C660,575 690,610 692,660", "Arm R", fill=NONE,
       stroke="#7a5430", strokeWidth=26, cap="round")
d.shape("ellipse", "Paw R", x=664, y=640, width=60, height=54,
        fill="#f5ead0", stroke=NONE)

ship(d, "golly", "V2R01")
