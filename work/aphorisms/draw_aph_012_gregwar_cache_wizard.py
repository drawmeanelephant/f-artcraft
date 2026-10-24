#!/usr/bin/env python3
"""APH-012 Gregwar Cache Wizard — aphorism plate V1R00. A breadbox cache
wearing the wizard hat, serving an older truth (a stale loaf) because it
was closer at hand; the fresh loaf glows unreachable under a sealed glass
cloche. Invalidation sigils filed as folklore wax seals. Warm amber plate,
one cold blue rumor behind glass. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("APH-012 Gregwar Cache Wizard — Aphorism Plate", 1000, 1000)

INK = "#2E2010"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1E140A"}, {"offset": 1, "color": "#0B0703"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4A3518"}, {"offset": 0.7, "color": "#2A1D0C"},
    {"offset": 1, "color": "#140D05"}]}}
BOX_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#B8862E"}, {"offset": 0.6, "color": "#7E5A1E"},
    {"offset": 1, "color": "#4A3410"}]}}
HAT_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6E70A8"}, {"offset": 0.6, "color": "#464E80"},
    {"offset": 1, "color": "#282E52"}]}}
STALE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#C89A5A"}, {"offset": 0.7, "color": "#9A7138"},
    {"offset": 1, "color": "#6E4E22"}]}}
FRESH_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#EAF6F4"}, {"offset": 0.7, "color": "#A8D8D0"},
    {"offset": 1, "color": "#6AA89E"}]}}
GLASS_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#B8D8D4"}, {"offset": 0.75, "color": "#7EA8A4"},
    {"offset": 1, "color": "#4E7470"}]}}
WOOD_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#8A6228"}, {"offset": 1, "color": "#54380F"}]}}
CREAM = "#EEE0BE"
GOLD = "#E8CC90"
FAINT = "#8A7040"
FROST = "#A8D8D0"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#A87A34", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8CC90", strokeWidth=3, opacity=40)
for i, (x, y, w) in enumerate([(200, 215, 7), (795, 210, 8), (160, 500, 6),
                               (845, 495, 7), (240, 745, 6), (760, 735, 7)]):
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#8A7040", opacity=35, stroke=NONE)

# floor glows: warm under the cache, cold under the dome
d.shape("ellipse", "Floor glow cache", x=230, y=606, width=270, height=56,
        fill="#C4943E", opacity=28, stroke=NONE)
d.shape("ellipse", "Floor glow dome", x=565, y=612, width=230, height=50,
        fill="#6AA8A0", opacity=25, stroke=NONE)

# --- the cache wizard (left) --------------------------------------------------
# breadbox body
d.shape("rectangle", "Cache box", x=255, y=390, width=210, height=195,
        radius=18, fill=BOX_GRAD, stroke=INK, strokeWidth=4)
d.shape("rectangle", "Box sheen", x=268, y=398, width=184, height=20,
        radius=9, fill="#E8C060", opacity=40, stroke=NONE)
# brass name plate: /static — the folder that cannot verify freshness
d.shape("rectangle", "Plaque", x=292, y=404, width=132, height=30,
        radius=4, fill="#3A2A10", stroke="#C9A868", strokeWidth=2)
r = d.text("/static/", "Plaque text", x=358, y=424, size=14,
           font="Virelai Sans", color=GOLD, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "plaque tracking", ids=[r["id"]], tracking=40)
# door, ajar — warmth leaking out
d.shape("ellipse", "Door glow", x=296, y=452, width=110, height=110,
        fill="#F4C06A", opacity=30, stroke=NONE)
d.shape("rectangle", "Cache door", x=290, y=446, width=96, height=124,
        radius=10, fill="#2A1C08", stroke="#C9A868", strokeWidth=3)
d.shape("rectangle", "Door sliver", x=372, y=452, width=12, height=112,
        radius=5, fill="#F4C06A", opacity=85, stroke=NONE)
d.shape("ellipse", "Door knob", x=300, y=502, width=12, height=12,
        fill="#C9A868", stroke=INK, strokeWidth=2)
# feet
d.shape("rectangle", "Box foot L", x=275, y=585, width=34, height=16,
        radius=4, fill="#4A3410", stroke=INK, strokeWidth=3)
d.shape("rectangle", "Box foot R", x=405, y=585, width=34, height=16,
        radius=4, fill="#4A3410", stroke=INK, strokeWidth=3)

# wizard hat: brim + cone with filed sigil stars
d.shape("ellipse", "Hat brim", x=242, y=368, width=236, height=36,
        fill=HAT_GRAD, stroke=INK, strokeWidth=4)
d.path("M292,378 Q306,300 352,236 Q396,304 420,382 Q356,398 292,378 Z",
       "Hat cone", fill=HAT_GRAD, stroke=INK, strokeWidth=4)
d.path("M330,290 Q352,272 374,288", "Hat band", fill=NONE,
       stroke="#C9A868", strokeWidth=6, opacity=80, cap="round")
# invalidation sigils sewn on the hat — filed as folklore
for i, (sx, sy, sr) in enumerate([(340, 330, 9), (368, 348, 7), (350, 262, 6)]):
    for a in (0, 45, 90, 135):
        r_ = math.radians(a)
        d.path(f"M{sx - math.cos(r_) * sr:.0f},{sy - math.sin(r_) * sr:.0f} "
               f"L{sx + math.cos(r_) * sr:.0f},{sy + math.sin(r_) * sr:.0f}",
               f"Sigil {i+1}.{a}", fill=NONE, stroke=GOLD, strokeWidth=2,
               opacity=75, cap="round")

# the served loaf: an older truth on a small plate
d.shape("ellipse", "Serving plate", x=448, y=566, width=130, height=26,
        fill="#8A7040", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Plate sheen", x=460, y=570, width=80, height=10,
        fill="#C9A868", opacity=50, stroke=NONE)
d.path("M462,566 Q462,532 496,530 Q545,528 556,552 Q560,566 552,566 Z",
       "Stale loaf", fill=STALE_GRAD, stroke=INK, strokeWidth=3)
for i, (cx, cy) in enumerate([(485, 542), (512, 538), (536, 548)]):
    d.path(f"M{cx},{cy} L{cx + 12},{cy - 6}", f"Crust crack {i+1}",
           fill=NONE, stroke="#5E421C", strokeWidth=2, opacity=80,
           cap="round")
# one cold wisp — it stopped steaming long ago
d.path("M508,516 Q500,498 510,484 Q518,472 510,458", "Cold wisp",
       fill=NONE, stroke=CREAM, strokeWidth=2.5, opacity=30, dash=[5, 7],
       cap="round")

# --- the fresh loaf, locked behind glass (right) --------------------------------
# pedestal
d.shape("ellipse", "Pedestal", x=560, y=594, width=220, height=34,
        fill=WOOD_GRAD, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Pedestal sheen", x=580, y=598, width=140, height=10,
        fill="#B8873E", opacity=50, stroke=NONE)
# cloche dome
d.path("M575,596 C575,470 620,392 670,392 C720,392 765,470 765,596 Z",
       "Cloche", fill=GLASS_GRAD, stroke="#9EC4C0", strokeWidth=4, opacity=90)
d.path("M598,560 Q600,480 646,430", "Cloche sheen", fill=NONE,
       stroke="#EAF6F4", strokeWidth=8, opacity=30, cap="round")
d.shape("ellipse", "Cloche knob", x=658, y=380, width=24, height=16,
        fill="#9EC4C0", stroke=INK, strokeWidth=3)
# the rumor inside: a fresh loaf, glowing, theoretical
d.shape("ellipse", "Fresh halo", x=606, y=500, width=128, height=72,
        fill="#B8E4DC", opacity=30, stroke=NONE)
d.path("M618,560 Q618,522 656,520 Q706,518 720,544 Q726,560 716,560 Z",
       "Fresh loaf", fill=FRESH_GRAD, stroke="#3E6A64", strokeWidth=3)
for i, (sx, sy) in enumerate([(640, 508), (700, 512), (668, 494)]):
    d.path(f"M{sx},{sy - 8} L{sx},{sy + 8} M{sx - 8},{sy} L{sx + 8},{sy}",
           f"Sparkle {i+1}", fill=NONE, stroke="#EAF6F4", strokeWidth=2.5,
           opacity=80, cap="round")
# wax-seal lock at the dome's lip — sealed, unverifiable
d.path("M660,596 Q660,576 670,576 Q680,576 680,596", "Seal shackle",
       fill=NONE, stroke="#C9A868", strokeWidth=4, cap="round")
d.shape("ellipse", "Seal", x=652, y=592, width=36, height=30,
        fill="#8A2E24", stroke=INK, strokeWidth=3)
for a in (20, 110, 200, 290):
    r_ = math.radians(a)
    d.path(f"M{670 - math.cos(r_) * 7:.0f},{606 - math.sin(r_) * 7:.0f} "
           f"L{670 + math.cos(r_) * 7:.0f},{606 + math.sin(r_) * 7:.0f}",
           f"Seal mark {a}", fill=NONE, stroke="#E8B090", strokeWidth=1.5,
           opacity=80, cap="round")
# cobweb in the dome's top-right — nothing has reached in for a while
for ang in [-72, -40, -8]:
    a = math.radians(ang)
    d.path(f"M752,428 L{752 + math.cos(a) * 52:.0f},{428 + math.sin(a) * 52:.0f}",
           f"Web spoke {ang}", fill=NONE, stroke=CREAM, strokeWidth=1.5,
           opacity=40)
d.path("M736,442 Q748,450 760,444", "Web arc", fill=NONE, stroke=CREAM,
       strokeWidth=2, opacity=45)

# --- filed sigils: folklore between them ---------------------------------------
for i, (sx, sy, srot) in enumerate([(505, 634, -8), (545, 640, 6)]):
    d.path(rot_rect_path(sx, sy, 30, 36, srot), f"Filed tag {i+1}",
           fill="#5E4418", stroke="#8A7040", strokeWidth=2, opacity=80)
    d.shape("ellipse", f"Filed seal {i+1}", x=sx - 8, y=sy - 8, width=16,
            height=16, fill="#8A2E24", stroke=INK, strokeWidth=2,
            opacity=80)
d.path("M498,668 Q520,676 552,670", "Filed dust", fill=NONE,
       stroke=CREAM, strokeWidth=2, opacity=30, dash=[3, 6], cap="round")

# --- aphorism line + name + role -------------------------------------------------
r = d.text("FRESHNESS IS A RUMOR", "Key line 1", x=500, y=722,
           size=22, font="Virelai Sans", color="#E8CC90", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "key1 tracking", ids=[r["id"]], tracking=100)
r = d.text("THE STATIC FOLDER CANNOT VERIFY.", "Key line 2", x=500, y=756,
           size=22, font="Virelai Sans", color="#E8CC90", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "key2 tracking", ids=[r["id"]], tracking=90)

d.text("GREGWAR CACHE WIZARD", "Name", x=500, y=905, size=52,
       font="Virelai Sans", color=CREAM, justify="center")
r = d.text("FRESHNESS IS A RUMOR", "Role", x=500, y=950, size=18,
           font="Virelai Sans", color="#C9A868", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=160)

d.finish("aph-012-gregwar-cache-wizard-V1R00")
