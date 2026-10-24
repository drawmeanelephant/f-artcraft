#!/usr/bin/env python3
"""APH-030 Holy DOSwell — motivational-poster aphorism plate V1R00.
A VGA-mode HEAVEN poster: inside the gilt card, a stained-glass window
of the sixteen hallowed colors, and at its heart the C:\\ prompt burning
inside a halo ring, cursor block pulsing like a heartbeat. Condemnation
seals in the side margins mark the suppressed heresy of high resolution.
Indigo night, jewel glass, gold light. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("APH-030 Holy DOSwell — Motivational Poster", 1000, 1000)

INK = "#120C1E"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1E1630"}, {"offset": 1, "color": "#0A0714"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#3E3060"}, {"offset": 0.7, "color": "#221A3E"},
    {"offset": 1, "color": "#120C24"}]}}
POSTER_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#221A30"}, {"offset": 1, "color": "#0E0A16"}]}}
LEAD = "#161020"
SEAL_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#C04858"}, {"offset": 1, "color": "#6E1E2E"}]}}
GOLD = "#D8B868"
FRAME = "#C0B088"
HEAD = "#F0EAD8"
PUNCH = "#DACFA8"
CREAM = "#F0EAD8"
FAINT = "#9888B8"
HALO = "#F0D890"
PROMPT = "#EAF8FF"
HERESY = "#C05862"

# the sixteen hallowed colors (CGA liturgy, gently warmed)
GLASS = ["#241C16", "#4448C8", "#44A848", "#48A8A8",
         "#B04840", "#A848A8", "#A86A40", "#A8A8A0",
         "#585850", "#6868E8", "#68D868", "#68D8D8",
         "#E06858", "#E068D8", "#E0D458", "#F4ECDC"]

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#5A4E8A", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C0B0E0", strokeWidth=3, opacity=35)
d.shape("ellipse", "Patina 1", x=200, y=170, width=200, height=110,
        fill="#4A3E70", opacity=20, stroke=NONE)
d.shape("ellipse", "Patina 2", x=620, y=620, width=200, height=110,
        fill="#4A3E70", opacity=16, stroke=NONE)
for i, (x, y, w) in enumerate([(215, 280, 7), (790, 255, 8), (165, 480, 6),
                               (838, 475, 7), (250, 655, 6), (755, 665, 7)]):
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#6A5C9A", opacity=35, stroke=NONE)

# --- the poster card -------------------------------------------------------------
PX, PY, PW, PH = 220, 150, 560, 440
d.shape("rectangle", "Poster shadow", x=PX + 8, y=PY + 10, width=PW,
        height=PH, fill="#000000", opacity=35, stroke=NONE)
d.shape("rectangle", "Poster", x=PX, y=PY, width=PW, height=PH,
        fill=POSTER_GRAD, stroke="#33284A", strokeWidth=4)
d.shape("rectangle", "Frame outer", x=PX + 16, y=PY + 16,
        width=PW - 32, height=PH - 32, fill=NONE, stroke=FRAME,
        strokeWidth=2, opacity=80)
d.shape("rectangle", "Frame inner", x=PX + 24, y=PY + 24,
        width=PW - 48, height=PH - 48, fill=NONE, stroke=GOLD,
        strokeWidth=1.5, opacity=60)

# headline
r = d.text("DIVINE SEGMENTATION", "Headline", x=500, y=PY + 62,
           size=30, font="Virelai Sans", color=HEAD, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "headline tracking", ids=[r["id"]], tracking=55)
d.path("M345,243 L472,243 M528,243 L655,243", "Headline rules", fill=NONE,
       stroke=GOLD, strokeWidth=2, opacity=80)
d.path(rot_rect_path(500, 243, 10, 10, 45), "Headline diamond",
       fill=GOLD, opacity=85, stroke=NONE)

# --- divine glow behind the window -----------------------------------------------------
d.shape("ellipse", "Aureole", x=350, y=295, width=300, height=240,
        fill=HALO, opacity=10, stroke=NONE)
d.shape("ellipse", "Aureole core", x=400, y=330, width=200, height=170,
        fill=HALO, opacity=14, stroke=NONE)

# --- the stained-glass window: sixteen panes under a flattened arch ----------------------
WX0, WX1 = 390, 610          # window sides
WTOP, WBOT = 342, 508        # sill top of body / bottom
d.path(f"M{WX0},{WBOT} L{WX0},{WTOP} "
       f"Q{WX0},286 500,278 Q{WX1},286 {WX1},{WTOP} L{WX1},{WBOT} Z",
       "Window", fill="#0C0814", stroke=GOLD, strokeWidth=3)
# dome panes: a small rosette of warm glass in the arch cap
for i, (cx, cy, c) in enumerate([(500, 300, "#E0D458"),
                                 (462, 314, "#B04840"),
                                 (538, 314, "#4448C8")]):
    d.shape("ellipse", f"Dome pane {i+1}", x=cx - 14, y=cy - 14,
            width=28, height=28, fill=c, opacity=85, stroke=LEAD,
            strokeWidth=2)
d.shape("ellipse", "Dome boss", x=488, y=296, width=24, height=24,
        fill=NONE, stroke=LEAD, strokeWidth=2, opacity=80)
# the 4x4 grid of the sixteen colors
PGX, PGY, PGN, PGW, PGH = 398, 352, 4, 47, 30
for i, c in enumerate(GLASS):
    gx = PGX + (i % PGN) * (PGW + 4)
    gy = PGY + (i // PGN) * (PGH + 4)
    d.shape("rectangle", f"Pane {i+1}", x=gx, y=gy, width=PGW,
            height=PGH, radius=2, fill=c, opacity=88, stroke=LEAD,
            strokeWidth=2)

# --- the sacrament: C:\> burning in its halo --------------------------------------------
MX, MY = 500, 414          # medallion center over the glass
d.shape("ellipse", "Medallion", x=MX - 58, y=MY - 46, width=116,
        height=92, fill="#0C0814", opacity=72, stroke=NONE)
d.shape("ellipse", "Halo glow", x=MX - 62, y=MY - 50, width=124,
        height=100, fill=NONE, stroke=HALO, strokeWidth=6, opacity=22)
d.shape("ellipse", "Halo", x=MX - 62, y=MY - 50, width=124, height=100,
        fill=NONE, stroke=HALO, strokeWidth=2.5, opacity=90)
# halo light-ticks, like a saint's nimbus gone phosphor
for i in range(12):
    a = math.radians(i * 30)
    x1 = MX + 68 * math.cos(a); y1 = MY + 55 * math.sin(a)
    x2 = MX + 76 * math.cos(a); y2 = MY + 63 * math.sin(a)
    d.path(f"M{x1:.0f},{y1:.0f} L{x2:.0f},{y2:.0f}", f"Nimbus {i+1}",
           fill=NONE, stroke=HALO, strokeWidth=2, opacity=45)
d.text("C:\\>", "Prompt", x=MX - 4, y=MY - 4, size=27,
       font="Source Sans 3", color=PROMPT, justify="center")
# cursor block mid-blink + its ghost
d.shape("rectangle", "Cursor", x=MX + 22, y=MY - 20, width=14,
        height=20, fill=PROMPT, opacity=90, stroke=NONE)
d.shape("rectangle", "Cursor ghost", x=MX + 40, y=MY - 18, width=10,
        height=16, fill=PROMPT, opacity=25, stroke=NONE)
# the heartbeat: a little ECG under the prompt
d.path(f"M{MX - 40},{MY + 26} L{MX - 22},{MY + 26} L{MX - 15},{MY + 16} "
       f"L{MX - 8},{MY + 34} L{MX - 2},{MY + 26} L{MX + 40},{MY + 26}",
       "Heartbeat", fill=NONE, stroke=PROMPT, strokeWidth=2,
       cap="round", opacity=70)

# --- the margins: heresy, suppressed ------------------------------------------------------
for i, sx in enumerate([308, 692]):
    d.shape("ellipse", f"Seal {i+1}", x=sx - 17, y=394, width=34,
            height=34, fill=SEAL_GRAD, stroke="#3E1220",
            strokeWidth=2.5)
    d.path(f"M{sx - 9},403 L{sx + 9},419", f"Seal slash {i+1}",
           fill=NONE, stroke="#3E1220", strokeWidth=3, cap="round")
    d.shape("ellipse", f"Seal ring {i+1}", x=sx - 11, y=400,
            width=22, height=22, fill=NONE, stroke="#E09098",
            strokeWidth=1, opacity=50)
    d.text("HERESY", f"Seal text {i+1}", x=sx, y=446, size=8,
           font="Source Sans 3", color=HERESY, justify="center")

# --- punchline sub-caption -------------------------------------------------------------
r = d.text("SACRAMENT OF THE C:\\ PROMPT VALIDATED.", "Punchline", x=500,
           y=PY + PH - 34, size=19, font="Virelai Sans", color=PUNCH,
           justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "punch tracking", ids=[r["id"]], tracking=40)

# --- flourish on the plate below the poster ----------------------------------------------
d.path("M415,668 L485,668 M515,668 L585,668", "Flourish rules", fill=NONE,
       stroke=GOLD, strokeWidth=2, opacity=55)
d.path(rot_rect_path(500, 668, 9, 9, 45), "Flourish diamond", fill=GOLD,
       opacity=60, stroke=NONE)

# --- name + role ----------------------------------------------------------------------
d.text("HOLY DOSWELL", "Name", x=500, y=905, size=56,
       font="Virelai Sans", color=CREAM, justify="center")
r = d.text("DIVINE SEGMENTATION", "Role", x=500, y=950, size=18,
           font="Virelai Sans", color=FAINT, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=160)

d.finish("aph-030-holy-doswell-V1R00")
