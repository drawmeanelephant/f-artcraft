#!/usr/bin/env python3
"""rc-oliver-adapter.sh — The Emissary. Necropolis plate V1R00.
A herald in half-mourning livery carrying sealed dispatches between two
courts — the Bash necropolis on one side, the Oliver engine's strange
bright chapel on the other — translating frontmatter, meta, render, and
wrap between realms that share no tongue. Pure Bash; zero Python required
for diplomacy. 1000x1000. Gradients + translucent shading, never flat."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("RC-Oliver-Adapter — Necropolis Plate", 1000, 1000)

INK = "#1E1C24"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#14101C"}, {"offset": 1, "color": "#080610"}]}}
PLATE_DK = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4A4258"}, {"offset": 0.7, "color": "#2A2438"},
    {"offset": 1, "color": "#121018"}]}}
PLATE_LT = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#8A7E60"}, {"offset": 0.7, "color": "#5A5040"},
    {"offset": 1, "color": "#2A2418"}]}}
FLOOR_DK = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#262032"}, {"offset": 1, "color": "#100E16"}]}}
FLOOR_LT = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5C5240"}, {"offset": 1, "color": "#262016"}]}}
CHAPEL = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#C8BC98"}, {"offset": 1, "color": "#847A5E"}]}}
GOLD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E8C56A"}, {"offset": 1, "color": "#9A7428"}]}}
DARK_LIVERY = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3A3A4E"}, {"offset": 1, "color": "#1C1C2A"}]}}
PARCH = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E4D6B4"}, {"offset": 1, "color": "#B8A67E"}]}}
WAX = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#A03228"}, {"offset": 1, "color": "#5C140F"}]}}
SKIN = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E0BE96"}, {"offset": 1, "color": "#A8805C"}]}}

# --- backdrop + plate: two realms ----------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate crypt half", x=80, y=40, width=840, height=840,
        fill=PLATE_DK, stroke=NONE)
# the bright chapel half of the disc, right semicircle clipped to the rim arc
d.path("M500,40 A420,420 0 0 1 500,880 Z", "Plate chapel half",
       fill=PLATE_LT, stroke=NONE)
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#8A7E5C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#DCD6C8", strokeWidth=3, opacity=45)
# the seam between realms
d.path("M500,52 L500,868", "Realm seam", fill=NONE, stroke="#0E0C14",
       strokeWidth=4, opacity=60)
for i, (x, y, w, c) in enumerate([(193,233,8,"#564E6E"),(801,230,7,"#7A7052"),
                                  (157,524,9,"#564E6E"),(837,544,8,"#7A7052"),
                                  (247,766,7,"#564E6E"),(753,749,9,"#7A7052"),
                                  (133,393,6,"#564E6E"),(864,391,7,"#7A7052"),
                                  (391,113,7,"#564E6E"),(613,110,8,"#7A7052"),
                                  (333,823,6,"#564E6E"),(665,821,7,"#7A7052")]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill=c, opacity=35, stroke=NONE)

# --- left realm: the Bash crypt gate ----------------------------------------------
d.shape("ellipse", "Crypt gloom", x=190, y=300, width=230, height=280,
        fill="#0A0810", opacity=45, stroke=NONE)
d.path("M262,650 L262,420 C262,345 358,345 358,420 L358,650 Z", "Crypt gate",
       fill="#0E0C16", stroke=INK, strokeWidth=5, join="round")
d.path("M262,420 C262,345 358,345 358,420", "Gate arch", fill=NONE,
       stroke="#4A4258", strokeWidth=7, opacity=85)
for i, gx in enumerate([286, 310, 334]):
    d.path(f"M{gx},420 L{gx},650", f"Gate bar {i+1}", fill=NONE,
           stroke="#3A3A48", strokeWidth=5, opacity=90)
d.path("M270,500 L350,500 M270,575 L350,575", "Gate crossbars", fill=NONE,
       stroke="#3A3A48", strokeWidth=5, opacity=90)
d.shape("ellipse", "Gate lock", x=298, y=530, width=24, height=28,
        fill="#2A2838", stroke=INK, strokeWidth=3)

# --- right realm: the Oliver chapel -----------------------------------------------
d.shape("ellipse", "Chapel glow", x=580, y=240, width=260, height=260,
        fill="#E8C56A", opacity=14, stroke=NONE)
# pointed arch window
d.path("M640,650 L640,430 C640,385 665,355 700,330 C735,355 760,385 760,430 "
       "L760,650 Z", "Chapel window", fill="#2A2418", stroke=INK,
       strokeWidth=5, join="round")
d.path("M650,650 L650,435 C650,395 672,368 700,346 C728,368 750,395 750,435 "
       "L750,650 Z", "Chapel light", fill=CHAPEL, stroke="#8A7E5C",
       strokeWidth=3)
# rose window with the engine's cog heart
d.shape("ellipse", "Rose window", x=668, y=380, width=64, height=64,
        fill="#F0D9A0", stroke=INK, strokeWidth=4)
for i in range(8):
    import math
    a = math.radians(i * 45)
    tx = 700 + 34 * math.cos(a); ty = 412 + 34 * math.sin(a)
    d.shape("rectangle", f"Cog tooth {i+1}", x=tx-5, y=ty-5, width=10,
            height=10, fill=GOLD, stroke=INK, strokeWidth=2, radius=2)
d.shape("ellipse", "Cog heart", x=688, y=400, width=24, height=24,
        fill=GOLD, stroke=INK, strokeWidth=3)
d.shape("ellipse", "Cog bore", x=696, y=408, width=8, height=8,
        fill="#4A3A18", stroke=INK, strokeWidth=2)
# mullions
d.path("M700,452 L700,650 M668,520 L732,520", "Mullions", fill=NONE,
       stroke="#6A6046", strokeWidth=5)

# --- floor ----------------------------------------------------------------------
d.path("M156,700 L500,700 L500,790 A420,420 0 0 1 156,700 Z", "Crypt floor",
       fill=FLOOR_DK, stroke=NONE)
d.path("M500,700 L844,700 A420,420 0 0 1 500,790 Z", "Chapel floor",
       fill=FLOOR_LT, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0C0A10",
       strokeWidth=4, opacity=70)
d.shape("ellipse", "Herald shadow", x=420, y=682, width=160, height=18,
        fill="#050308", opacity=55, stroke=NONE)

# --- the herald in half-mourning livery ---------------------------------------------
# legs + boots
d.path("M482,690 L484,636 L498,636 L500,690 Z", "Leg L", fill="#2A2430",
       stroke=INK, strokeWidth=4, join="round")
d.path("M502,690 L504,636 L518,636 L520,690 Z", "Leg R", fill="#6A5A34",
       stroke=INK, strokeWidth=4, join="round")
d.path("M474,684 L504,684 L504,694 L474,694 Z", "Boot L", fill="#1C1814",
       stroke=INK, strokeWidth=3, join="round")
d.path("M498,684 L528,684 L528,694 L498,694 Z", "Boot R", fill="#3E3020",
       stroke=INK, strokeWidth=3, join="round")
# tabard: dark mourning on the crypt side, gold on the chapel side
d.path("M500,462 L466,470 L462,560 L468,640 L500,640 Z", "Tabard dark",
       fill=DARK_LIVERY, stroke=INK, strokeWidth=4, join="round")
d.path("M500,462 L534,470 L538,560 L532,640 L500,640 Z", "Tabard gold",
       fill=GOLD, stroke=INK, strokeWidth=4, join="round")
d.path("M466,556 L534,556 L534,572 L466,572 Z", "Belt", fill="#241E18",
       stroke=INK, strokeWidth=3, join="round")
d.shape("ellipse", "Buckle", x=492, y=556, width=16, height=16,
        fill=NONE, stroke="#C8B060", strokeWidth=3)
# mourning sash, crypt shoulder to chapel hip
d.path("M478,470 L522,556", "Mourning sash", fill=NONE, stroke="#101018",
       strokeWidth=10, opacity=85, cap="round")
# head + split cap
d.shape("ellipse", "Head", x=482, y=412, width=36, height=40,
        fill=SKIN, stroke=INK, strokeWidth=4)
d.path("M480,428 C480,408 520,408 520,428 L520,434 L480,434 Z", "Cap base",
       fill=DARK_LIVERY, stroke=INK, strokeWidth=3, join="round")
d.path("M500,408 C514,408 520,418 520,428 L520,434 L500,434 Z", "Cap bright",
       fill=GOLD, stroke=INK, strokeWidth=3, join="round")
d.shape("ellipse", "Eye", x=489, y=438, width=5, height=5,
        fill="#241812", stroke=NONE)

# left arm to the crypt — dark sleeve, dark-sealed scroll
d.path("M468,500 C445,510 425,520 406,532", "Arm crypt", fill=NONE,
       stroke="#3A3A4E", strokeWidth=12, cap="round")
d.shape("ellipse", "Hand crypt", x=392, y=526, width=18, height=16,
        fill=SKIN, stroke=INK, strokeWidth=3)
d.path("M356,528 L406,528", "Scroll crypt", fill=NONE, stroke="#C9B890",
       strokeWidth=16, cap="round")
d.shape("ellipse", "Scroll end L1", x=354, y=522, width=12, height=12,
        fill=PARCH, stroke=INK, strokeWidth=3)
d.shape("ellipse", "Seal crypt", x=376, y=534, width=14, height=14,
        fill=WAX, stroke=INK, strokeWidth=2)
d.path("M381,534 L381,548", "Seal ribbon L", fill=NONE, stroke="#7A1F18",
       strokeWidth=5)

# right arm to the chapel — gold sleeve, gold-sealed scroll
d.path("M532,500 C555,510 575,520 594,532", "Arm chapel", fill=NONE,
       stroke="#C8A44E", strokeWidth=12, cap="round")
d.shape("ellipse", "Hand chapel", x=590, y=526, width=18, height=16,
        fill=SKIN, stroke=INK, strokeWidth=3)
d.path("M594,528 L644,528", "Scroll chapel", fill=NONE, stroke="#E8DCC0",
       strokeWidth=16, cap="round")
d.shape("ellipse", "Scroll end R1", x=634, y=522, width=12, height=12,
        fill=PARCH, stroke=INK, strokeWidth=3)
d.shape("ellipse", "Seal chapel", x=610, y=534, width=14, height=14,
        fill=GOLD, stroke=INK, strokeWidth=2)
d.path("M615,534 L615,548", "Seal ribbon R", fill=NONE, stroke="#8A6420",
       strokeWidth=5)

# --- captions ------------------------------------------------------------------
d.text("RC-OLIVER-ADAPTER", "Name", x=500, y=930, size=56, font="Virelai Sans",
       color="#E6E2DA", justify="center")
r = d.text("ENVOY TO THE ENGINE", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#B0A88E", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("rk-oliver-adapter-V1R00")
