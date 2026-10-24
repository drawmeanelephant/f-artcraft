#!/usr/bin/env python3
"""APH-004 Boily McPlaterton — aphorism plate V1R00. Boily's warped chassis
glowing at the seams, crack lit from inside, a fan that spins but does not
cool, one bowtie wing drooping with its dignity. Thermal palette: glowing
reds and oranges over deep black, translucent heat haze. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("APH-004 Boily McPlaterton — Aphorism Plate", 1000, 1000)

INK = "#2A0E06"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1E0D08"}, {"offset": 1, "color": "#0A0403"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#56240F"}, {"offset": 0.65, "color": "#33130A"},
    {"offset": 1, "color": "#180804"}]}}
CASE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E8985E"}, {"offset": 0.55, "color": "#C05E30"},
    {"offset": 1, "color": "#7E2E1A"}]}}
CORE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#FFE8B0"}, {"offset": 0.5, "color": "#F09A4E"},
    {"offset": 1, "color": "#C43A1E"}]}}
CREAM = "#F2D4B0"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#8A4A26", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F0A05A", strokeWidth=3, opacity=40)
# ember flecks on the plate
for i, (x, y, w) in enumerate([(190, 230, 8), (815, 250, 7), (155, 520, 9),
                               (840, 545, 8), (240, 720, 7), (755, 730, 9),
                               (140, 395, 6), (855, 390, 7)]):
    d.shape("ellipse", f"Ember {i+1}", x=x, y=y, width=w, height=w,
            fill="#E86A3A", opacity=45, stroke=NONE)
# heat glow pool under the chassis
d.shape("ellipse", "Glow pool", x=270, y=560, width=460, height=140,
        fill=CORE_GRAD, opacity=30, stroke=NONE)
d.shape("ellipse", "Chassis shadow", x=330, y=640, width=340, height=40,
        fill="#000000", opacity=40, stroke=NONE)

# --- Boily's warped chassis ------------------------------------------------------
# casing bows at the top seam, slumps on the right — held, but warped
d.path("M345,320 Q500,268 655,315 L668,585 Q650,632 600,638 "
       "L400,638 Q352,630 336,588 Z",
       "Chassis", fill=CASE_GRAD, stroke=INK, strokeWidth=6)
# molten glow leaking along the warped top seam
d.path("M360,318 Q500,272 642,314", "Seam glow", fill=NONE,
       stroke="#FFD98A", strokeWidth=6, opacity=70, cap="round")
d.path("M360,322 Q500,278 642,318", "Seam bleed", fill=NONE,
       stroke="#C43A1E", strokeWidth=12, opacity=35, cap="round")
# edge glow: casing radiating heat at the silhouettes
d.path("M340,330 L340,580", "Edge glow L", fill=NONE, stroke="#F09A4E",
       strokeWidth=10, opacity=35, cap="round")
d.path("M664,330 L664,580", "Edge glow R", fill=NONE, stroke="#F09A4E",
       strokeWidth=10, opacity=35, cap="round")
# chassis sheen
d.shape("ellipse", "Case sheen", x=380, y=330, width=180, height=90,
        fill="#F2C088", opacity=30, stroke=NONE)

# the infamous crack, lit from inside
d.path("M488,330 L506,390 L484,452 L512,516 L492,580 L502,632",
       "Crack", fill=NONE, stroke="#2A0E06", strokeWidth=9, cap="round")
d.path("M492,334 L504,390 L488,452 L508,514 L496,578 L502,626",
       "Crack glow", fill=NONE, stroke="#FFD98A", strokeWidth=3,
       opacity=85, cap="round")

# --- face: thermal regret -----------------------------------------------------------
d.shape("ellipse", "Eye L", x=405, y=400, width=17, height=22,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Eye R", x=578, y=400, width=17, height=22,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Glint L", x=409, y=404, width=5, height=5,
        fill="#FFFFFF", opacity=80, stroke=NONE)
d.shape("ellipse", "Glint R", x=582, y=404, width=5, height=5,
        fill="#FFFFFF", opacity=80, stroke=NONE)
# heavy lids — the regret half of the face
d.path("M402,398 Q413,392 424,397", "Lid L", fill=NONE, stroke=INK,
       strokeWidth=4, cap="round")
d.path("M576,397 Q587,392 598,398", "Lid R", fill=NONE, stroke=INK,
       strokeWidth=4, cap="round")
# small flat mouth, holding
d.path("M462,470 Q500,476 538,470", "Mouth", fill=NONE, stroke=INK,
       strokeWidth=6, cap="round")
# cheeks hot
d.shape("ellipse", "Flush L", x=398, y=440, width=44, height=20,
        fill="#E86A3A", opacity=40, stroke=NONE)
d.shape("ellipse", "Flush R", x=558, y=440, width=44, height=20,
        fill="#E86A3A", opacity=40, stroke=NONE)

# --- the bowtie: dignity, drooping ------------------------------------------------------
d.path("M486,494 L452,478 L452,514 Z", "Bow L", fill="#8A2418",
       stroke=INK, strokeWidth=3)
# right wing sags — dignity did not hold
d.path("M514,494 L548,482 L546,528 Q532,532 522,522 Z", "Bow R droop",
       fill="#8A2418", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Bow knot", x=486, y=484, width=28, height=22,
        fill="#6E1A10", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Knot glint", x=493, y=488, width=8, height=5,
        fill="#E86A3A", opacity=70, stroke=NONE)

# --- the fan: it spins; it does not cool ---------------------------------------------
d.shape("ellipse", "Fan ring", x=442, y=540, width=116, height=116,
        fill="#3A1A10", stroke=INK, strokeWidth=4)
for i, ang in enumerate([0, 60, 120, 180, 240, 300]):
    a1 = math.radians(ang + 18)
    a2 = math.radians(ang + 54)
    x1 = 500 + math.cos(a1) * 40
    y1 = 598 + math.sin(a1) * 40
    x2 = 500 + math.cos(a2) * 22
    y2 = 598 + math.sin(a2) * 22
    d.path(f"M500,598 L{x2:.0f},{y2:.0f} L{x1:.0f},{y1:.0f} Z",
           f"Fan blade {i+1}", fill="#C9B68E", opacity=85, stroke=NONE)
d.shape("ellipse", "Fan hub", x=488, y=586, width=24, height=24,
        fill=CORE_GRAD, stroke=INK, strokeWidth=2)
# spin arcs — furious, useless
d.path("M432,556 A74,74 0 0 1 540,548", "Spin arc 1", fill=NONE,
       stroke=CREAM, strokeWidth=3, opacity=50, cap="round")
d.path("M436,652 A74,74 0 0 0 544,644", "Spin arc 2", fill=NONE,
       stroke=CREAM, strokeWidth=3, opacity=50, cap="round")
# ...and the haze it fails to move, drifting straight up through the blades
d.shape("ellipse", "Fan haze", x=455, y=522, width=90, height=22,
        fill="#FFD98A", opacity=22, stroke=NONE)

# --- temperature gauge pinned in the red ---------------------------------------------
d.shape("ellipse", "Gauge", x=586, y=536, width=64, height=64,
        fill="#E8D6B0", stroke=INK, strokeWidth=4)
d.path("M598,596 A20,20 0 0 1 638,566", "Gauge red zone", fill=NONE,
       stroke="#C43A1E", strokeWidth=6, opacity=80, cap="round")
d.path("M618,568 L634,554", "Gauge needle", fill=NONE, stroke=INK,
       strokeWidth=4, cap="round")
d.shape("ellipse", "Gauge pin", x=614, y=564, width=8, height=8,
        fill=INK, stroke=NONE)

# --- sticker + feet ------------------------------------------------------------------
d.path(rot_rect_path(390, 560, 112, 30, -5), "Cooling sticker",
       fill="#E8D6B0", stroke=INK, strokeWidth=2.5, opacity=92)
d.text("COOLING PENDING", "Sticker text", x=390, y=568, size=10,
       font="Virelai Sans", color=INK, justify="center")
# little feet, right one slumping
d.shape("rectangle", "Foot L", x=390, y=636, width=44, height=16, radius=5,
        fill="#54301C", stroke=INK, strokeWidth=3)
d.path("M566,636 L614,636 L610,654 Q588,658 570,652 Z", "Foot R melt",
       fill="#54301C", stroke=INK, strokeWidth=3)

# --- heat haze + smoke rising ---------------------------------------------------------
for i, (sx, sy, sw, sh, op) in enumerate([(455, 250, 70, 40, 40),
                                          (420, 208, 88, 50, 32),
                                          (480, 162, 104, 58, 24),
                                          (435, 118, 120, 64, 17)]):
    d.shape("ellipse", f"Steam {i+1}", x=sx, y=sy, width=sw, height=sh,
            fill="#F2D4B0", opacity=op, stroke=NONE)
# wavy shimmer columns off the casing edges
for i, (hx, flip) in enumerate([(330, 1), (660, -1)]):
    d.path(f"M{hx},560 Q{hx + 14*flip},520 {hx},480 Q{hx - 14*flip},440 "
           f"{hx},400 Q{hx + 14*flip},360 {hx},330",
           f"Haze {i+1}", fill=NONE, stroke="#FFD98A", strokeWidth=4,
           opacity=25, cap="round")
# sparks off the casing
for i, (sx, sy, sr) in enumerate([(360, 350, 6), (652, 380, 5),
                                   (348, 500, 5), (658, 520, 6)]):
    d.path(f"M{sx},{sy-sr} L{sx+sr*0.3},{sy-sr*0.3} L{sx+sr},{sy} "
           f"L{sx+sr*0.3},{sy+sr*0.3} L{sx},{sy+sr} L{sx-sr*0.3},{sy+sr*0.3} "
           f"L{sx-sr},{sy} L{sx-sr*0.3},{sy-sr*0.3} Z",
           f"Spark {i+1}", fill="#FFD98A", opacity=85, stroke=NONE)

# --- aphorism line + name + role ----------------------------------------------------
r = d.text("ITS DIGNITY DID NOT.", "Key line", x=500, y=762, size=26,
           font="Virelai Sans", color="#F0C088", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "key tracking", ids=[r["id"]], tracking=140)

d.text("BOILY MCPLATERTON", "Name", x=500, y=905, size=56,
       font="Virelai Sans", color=CREAM, justify="center")
r = d.text("THERMAL REGRET LINGERS", "Role", x=500, y=950, size=18,
           font="Virelai Sans", color="#C9906A", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=160)

d.finish("aph-004-boily-mcplaterton-V1R00")
