#!/usr/bin/env python3
"""LIM-0048 Boily McPlaterton — limerick plate V1R00. A twelve-stanza
limerick as a western wanted poster: aged parchment on the plate, Boily's
portrait in the frame, scorch marks, smoke and sparks. Thermal palette.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("LIM-0048 Boily McPlaterton — Limerick Plate", 1000, 1000)

INK = "#3A1E0E"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#241209"}, {"offset": 1, "color": "#0E0603"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#5E3418"}, {"offset": 0.7, "color": "#3A1E0E"},
    {"offset": 1, "color": "#1C0D06"}]}}
PARCH = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#EBD3A4"}, {"offset": 0.6, "color": "#D4B57E"},
    {"offset": 1, "color": "#A8824C"}]}}
CASE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E8985E"}, {"offset": 0.6, "color": "#C46838"},
    {"offset": 1, "color": "#8A3A22"}]}}
CORE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#FFE8B0"}, {"offset": 0.5, "color": "#F09A4E"},
    {"offset": 1, "color": "#C43A1E"}]}}
SEPIA = "#4A2410"
CREAM = "#F2D4B0"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#6E4020", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8B87A", strokeWidth=3, opacity=45)
# ember flecks on the plate
for i, (x, y, w) in enumerate([(180, 220, 8), (820, 240, 7), (150, 520, 9),
                               (845, 540, 8), (250, 780, 7), (745, 760, 9),
                               (140, 400, 6), (858, 390, 7)]):
    d.shape("ellipse", f"Ember {i+1}", x=x, y=y, width=w, height=w,
            fill="#E86A3A", opacity=45, stroke=NONE)

# --- the wanted poster: ragged parchment ---------------------------------------
# poster body, hand-torn silhouette
d.path("M292,146 L706,138 L714,300 L708,468 L716,620 L710,764 "
       "L560,772 L420,766 L288,772 L296,610 L290,440 L296,300 Z",
       "Poster", fill=PARCH, stroke=SEPIA, strokeWidth=5, join="round")
# poster shadow cast on the plate
d.path("M306,764 L560,772 L710,764", "Poster drop", fill=NONE,
       stroke="#160A04", strokeWidth=10, opacity=30, cap="round")
# scorch marks at the corners/edges — translucent char
d.shape("ellipse", "Scorch TL", x=280, y=132, width=70, height=44,
        fill="#2A1408", opacity=45, stroke=NONE)
d.shape("ellipse", "Scorch TR", x=664, y=126, width=62, height=40,
        fill="#2A1408", opacity=40, stroke=NONE)
d.shape("ellipse", "Scorch BR", x=664, y=720, width=66, height=50,
        fill="#2A1408", opacity=42, stroke=NONE)
d.shape("ellipse", "Edge char", x=292, y=560, width=36, height=90,
        fill="#3A1E0E", opacity=35, stroke=NONE)
# nail holes pinning the corners
for i, (nx, ny) in enumerate([(308, 160), (692, 152), (304, 748),
                              (696, 742)]):
    d.shape("ellipse", f"Nail {i+1}", x=nx, y=ny, width=13, height=13,
            fill="#2A1408", stroke=SEPIA, strokeWidth=2)
    d.shape("ellipse", f"Nail glint {i+1}", x=nx + 3, y=ny + 3, width=4,
            height=4, fill="#EBD3A4", opacity=70, stroke=NONE)

# --- poster type -----------------------------------------------------------------
r = d.text("WANTED", "Wanted", x=500, y=224, size=64, font="Virelai Sans",
           color=SEPIA, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "wanted tracking", ids=[r["id"]], tracking=120)
d.text("FOR CRIMES AGAINST COOLING", "Charge", x=500, y=258, size=17,
       font="Virelai Sans", color="#6B3A1A", justify="center")
d.path("M340,278 L660,278", "Rule 1", fill=NONE, stroke=SEPIA,
       strokeWidth=2.5, opacity=70)

# --- Boily's portrait in the frame --------------------------------------------------
# scorched oval vignette
d.shape("ellipse", "Portrait glow", x=372, y=296, width=256, height=250,
        fill=CORE_GRAD, opacity=35, stroke=NONE)
d.shape("ellipse", "Portrait frame", x=384, y=304, width=232, height=232,
        fill="#3A1E0E", opacity=22, stroke=SEPIA, strokeWidth=6)
# Boily's casing bust inside the frame
d.shape("rectangle", "Boily bust", x=430, y=380, width=140, height=170,
        radius=14, fill=CASE_GRAD, stroke=INK, strokeWidth=5)
# the infamous crack, glowing
d.path("M496,384 L508,426 L492,470 L510,514 L498,548", "Crack",
       fill=NONE, stroke="#2A0E06", strokeWidth=8, cap="round")
d.path("M498,388 L506,426 L494,468 L506,510 L500,544", "Crack glow",
       fill=NONE, stroke="#FFD98A", strokeWidth=2.5, opacity=85,
       cap="round")
# defiant face
d.shape("ellipse", "Eye L", x=452, y=428, width=15, height=20,
        fill="#2A0E06", stroke=NONE)
d.shape("ellipse", "Eye R", x=534, y=428, width=15, height=20,
        fill="#2A0E06", stroke=NONE)
d.shape("ellipse", "Glint L", x=456, y=432, width=4, height=4,
        fill="#FFFFFF", opacity=80, stroke=NONE)
d.shape("ellipse", "Glint R", x=538, y=432, width=4, height=4,
        fill="#FFFFFF", opacity=80, stroke=NONE)
# flat unrepentant mouth
d.path("M470,478 L530,478", "Mouth", fill=NONE, stroke="#2A0E06",
       strokeWidth=6, cap="round")
d.path("M448,414 Q458,408 468,412", "Brow L", fill=NONE,
       stroke="#2A0E06", strokeWidth=4, cap="round")
d.path("M532,412 Q542,408 552,414", "Brow R", fill=NONE,
       stroke="#2A0E06", strokeWidth=4, cap="round")
# heat shimmer rising off the bust, inside the frame
d.shape("ellipse", "Shimmer", x=452, y=336, width=100, height=30,
        fill="#FFD98A", opacity=25, stroke=NONE)

# --- poster fine print --------------------------------------------------------------
d.path("M340,568 L660,568", "Rule 2", fill=NONE, stroke=SEPIA,
       strokeWidth=2.5, opacity=70)
d.text("THERMAL PASTE: NEVER APPLIED", "Detail 1", x=500, y=600, size=16,
       font="Virelai Sans", color=SEPIA, justify="center")
d.text("COMBUSTS LIKE A FRYING-PAN PLAN", "Detail 2", x=500, y=630,
       size=16, font="Virelai Sans", color=SEPIA, justify="center")
d.text("LAST SEEN FILING FORM 88-B", "Detail 3", x=500, y=660, size=16,
       font="Virelai Sans", color=SEPIA, justify="center")
d.text("REWARD: ONE (1) BOTTLE OF COOLANT", "Reward", x=500, y=710,
       size=16.5, font="Virelai Sans", color="#8A2418", justify="center")
d.text("TWELVE VERSES STRONG", "Stanzas", x=500, y=740, size=13,
       font="Virelai Sans", color="#6B3A1A", justify="center")

# --- smoke and sparks escaping the poster -------------------------------------------
for i, (sx, sy, sw, sh, op) in enumerate([(690, 240, 56, 34, 30),
                                          (712, 204, 70, 42, 24),
                                          (684, 168, 84, 48, 17)]):
    d.shape("ellipse", f"Smoke {i+1}", x=sx, y=sy, width=sw, height=sh,
            fill="#C9B6A4", opacity=op, stroke=NONE)
for i, (sx, sy, sr) in enumerate([(300, 330, 6), (704, 560, 5),
                                   (296, 680, 5)]):
    d.path(f"M{sx},{sy-sr} L{sx+sr*0.3},{sy-sr*0.3} L{sx+sr},{sy} "
           f"L{sx+sr*0.3},{sy+sr*0.3} L{sx},{sy+sr} L{sx-sr*0.3},{sy+sr*0.3} "
           f"L{sx-sr},{sy} L{sx-sr*0.3},{sy-sr*0.3} Z",
           f"Spark {i+1}", fill="#FFD98A", opacity=80, stroke=NONE)

# --- name + role ------------------------------------------------------------------
d.text("BOILY MCPLATERTON", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color=CREAM, justify="center")
r = d.text("LIM-0048 BOILY MCPLATERTON", "Role", x=500, y=968, size=20,
           font="Virelai Sans", color="#C9906A", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=170)

d.finish("lim-0048-boily-mcplaterton-V1R00")
