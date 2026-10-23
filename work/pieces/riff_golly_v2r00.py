#!/usr/bin/env python3
"""golly-V2R00 — the cheerful guillotine under lamplight: deep plum field,
one warm cone from above, wood in layered browns, the blade catching light.
900x1100, riffing on golly-V1R00."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE
from v2style import backdrop, glow, vignette, sparkle, ship

d = Draw()
d.new_doc("Golly V2R00", 900, 1100)
CX = 450

backdrop(d, 900, 1100, top="#1c1230", mid="#2a1a3e", bottom="#0d0816")
glow(d, "Lamplight", CX, 320, 330, "#ffb35c", 42)
glow(d, "Floor pool", CX, 950, 340, "#ffb35c", 18, aspect=0.3)
for i, (x, y, r) in enumerate([(120, 120, 6), (780, 150, 5), (830, 60, 4), (70, 300, 4)]):
    sparkle(d, f"Spark {i}", x, y, r)

WOOD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [80, 0],
         "stops": [{"offset": 0, "color": "#9a6f3e"},
                   {"offset": 0.5, "color": "#7a5430"},
                   {"offset": 1, "color": "#4e3016"}]}}
WOOD_TOP = {"gradient": {"kind": "linear", "start": [0, 90], "end": [0, 175],
            "stops": [{"offset": 0, "color": "#a87945"}, {"offset": 1, "color": "#6b4525"}]}}

# --- posts ---------------------------------------------------------------------
d.shape("rectangle", "Post L", x=290, y=160, width=56, height=620, radius=10,
        fill=WOOD, stroke=NONE)
d.shape("rectangle", "Post R", x=554, y=160, width=56, height=620, radius=10,
        fill=WOOD, stroke=NONE)
for i, (x, y) in enumerate([(318, 200), (318, 720), (582, 200), (582, 720)]):
    d.shape("ellipse", f"Bolt {i}", x=x - 7, y=y - 7, width=14, height=14,
            fill="#d4a24a", stroke=NONE)

# --- top beam + knob -------------------------------------------------------------
d.shape("rectangle", "Beam", x=262, y=90, width=376, height=86, radius=40,
        fill=WOOD_TOP, stroke=NONE)
d.shape("ellipse", "Knob", x=CX - 26, y=40, width=52, height=52,
        fill={"gradient": {"kind": "radial", "start": [440, 52], "end": [470, 90],
              "stops": [{"offset": 0, "color": "#e8bc6a"}, {"offset": 1, "color": "#8a5c22"}]}},
        stroke=NONE)

# --- blade: steel trapezoid, edge catching the lamp --------------------------------
d.path("M356,190 L544,190 L544,238 L356,368 Z", "Blade",
       stroke=NONE, fill={"gradient": {"kind": "linear", "start": [356, 190], "end": [430, 368],
           "stops": [{"offset": 0, "color": "#cfd8e4"},
                     {"offset": 0.55, "color": "#8a97ab"},
                     {"offset": 1, "color": "#4e5a70"}]}})
d.path("M356,340 L356,368 L544,238 L544,230 Z", "Blade edge",
       fill="#e8f0fa", stroke=NONE, opacity=80)
d.path("M380,200 L500,200 L420,290 Z", "Blade sheen", fill="#f5f9ff", stroke=NONE, opacity=30)
# blade carriage bar
d.shape("rectangle", "Carriage", x=346, y=170, width=208, height=34, radius=8,
        fill={"gradient": {"kind": "linear", "start": [0, 170], "end": [0, 204],
              "stops": [{"offset": 0, "color": "#5e3d28"}, {"offset": 1, "color": "#38210f"}]}},
        stroke=NONE)

# --- rope hanging right ---------------------------------------------------------
d.path("M640,176 C664,300 664,420 652,500", "Rope", fill=NONE,
       stroke="#c9a25a", strokeWidth=6, cap="round")
d.path("M652,500 C640,540 646,575 660,600 L646,606 C628,578 624,540 638,502 Z",
       "Tassel", fill="#c9a25a", stroke=NONE)

# --- base + face panel ------------------------------------------------------------
d.shape("rectangle", "Base", x=270, y=760, width=360, height=200, radius=24,
        fill={"gradient": {"kind": "linear", "start": [0, 760], "end": [0, 960],
              "stops": [{"offset": 0, "color": "#8a5f36"}, {"offset": 1, "color": "#4e3016"}]}},
        stroke=NONE)
d.shape("rectangle", "Face panel", x=336, y=800, width=228, height=140, radius=20,
        fill={"gradient": {"kind": "radial", "start": [420, 830], "end": [480, 920],
              "stops": [{"offset": 0, "color": "#6b4a2c"}, {"offset": 1, "color": "#3a2412"}]}},
        stroke=NONE)

# face: big eyes looking up-left, open grin
for i, ex in enumerate([408, 492]):
    d.shape("ellipse", f"Eye {i}", x=ex - 26, y=822, width=52, height=56,
            fill="#f5ead0", stroke=NONE)
    d.shape("ellipse", f"Pupil {i}", x=ex - 16, y=836, width=24, height=28,
            fill="#1c1208", stroke=NONE)
    d.shape("ellipse", f"Glint {i}", x=ex - 10, y=840, width=8, height=8,
            fill="#fff6e8", stroke=NONE)
d.path("M372,816 C384,808 398,806 410,810 M490,810 C502,806 516,808 528,816",
       "Brows", fill=NONE, stroke="#2a1a0c", strokeWidth=5, cap="round")
d.shape("ellipse", "Mouth", x=412, y=892, width=76, height=40, fill="#4a1420", stroke=NONE)
d.shape("ellipse", "Tongue", x=430, y=908, width=40, height=20, fill="#c96a6a", stroke=NONE)

# --- waving paw (left) ---------------------------------------------------------------
d.path("M290,540 C230,540 190,500 186,448", "Arm L", fill=NONE,
       stroke="#7a5430", strokeWidth=26, cap="round")
d.shape("ellipse", "Paw", x=140, y=390, width=96, height=86,
        fill="#f5ead0", stroke=NONE)
for i, fx in enumerate([152, 178, 204]):
    d.shape("ellipse", f"Finger {i}", x=fx, y=368, width=24, height=34, radius=10,
            fill="#f5ead0", stroke=NONE)

# --- bowtie -------------------------------------------------------------------------
d.path("M400,958 L440,946 L440,978 Z M500,958 L460,946 L460,978 Z", "Bowtie",
       fill="#e85a80", stroke=NONE)
d.shape("ellipse", "Knot", x=442, y=952, width=16, height=18, fill="#c94a6e", stroke=NONE)
for i, (x, y) in enumerate([(412, 962), (488, 962), (428, 968), (472, 968)]):
    d.shape("ellipse", f"Bowtie dot {i}", x=x - 3, y=y - 3, width=6, height=6,
            fill="#8a2a50", stroke=NONE)

# --- feet ------------------------------------------------------------------------------
d.shape("rectangle", "Foot L", x=320, y=960, width=90, height=52, radius=22,
        fill="#3a2412", stroke=NONE)
d.shape("rectangle", "Foot R", x=490, y=960, width=90, height=52, radius=22,
        fill="#3a2412", stroke=NONE)
d.shape("ellipse", "Shadow", x=280, y=1020, width=340, height=24, fill="#050308",
        stroke=NONE, opacity=55)

vignette(d, 900, 1100)
ship(d, "golly", "V2R00")
