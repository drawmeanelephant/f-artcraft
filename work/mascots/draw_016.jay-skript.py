#!/usr/bin/env python3
"""Jay Skript — mascot portrait V1R00. Client-Side Enabler:
a cheerfully overconfident little mascot mid "ta-da" beside a monitor
showing the blank white page, a tilted devtools console under it stuffed
with log lines that explain everything except what went wrong.
Warm amber mascot on a cold slate plate, console-glow accents. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Jay Skript — Mascot Plate", 1000, 1000)

INK = "#3A2E34"   # warm dark ink, never black
BG_GRAD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000], "stops": [
    {"offset": 0, "color": "#1A1620"}, {"offset": 1, "color": "#080609"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#A9B6C4"}, {"offset": 0.62, "color": "#74849A"},
    {"offset": 1, "color": "#42506A"}]}}
BODY_GRAD = {"gradient": {"kind": "linear", "start": [0, 390], "end": [0, 710], "stops": [
    {"offset": 0, "color": "#F5BC5C"}, {"offset": 0.55, "color": "#DE9438"},
    {"offset": 1, "color": "#A86428"}]}}
BELLY_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#FBDFA6"}, {"offset": 1, "color": "#E8B96C"}]}}
CASE_GRAD = {"gradient": {"kind": "linear", "start": [0, 230], "end": [0, 500], "stops": [
    {"offset": 0, "color": "#3E4550"}, {"offset": 1, "color": "#22272E"}]}}
SCR_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#FFFFFF"}, {"offset": 1, "color": "#E2E8EC"}]}}
CON_GRAD = {"gradient": {"kind": "linear", "start": [0, 480], "end": [0, 660], "stops": [
    {"offset": 0, "color": "#1E2A30"}, {"offset": 1, "color": "#121A20"}]}}

PCX, PCY, PR = 500, 460, 420

def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

# --- backdrop + plate -----------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#7E8FA2", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#1E222C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D6E0EA", strokeWidth=3, opacity=40)
# screen-burn patina
d.shape("ellipse", "Patina 1", x=180, y=150, width=250, height=160,
        fill="#B9C8D6", opacity=16, stroke=NONE)
d.shape("ellipse", "Patina 2", x=560, y=620, width=270, height=150,
        fill="#5C6E84", opacity=20, stroke=NONE)
for i, (x, y, w) in enumerate([(200,330,6),(815,320,5),(170,540,7),(845,545,6),
                               (240,755,5),(740,760,6),(140,430,5),(860,610,5),
                               (430,115,5),(615,135,6),(320,150,4),(700,210,5),
                               (215,640,4),(875,445,4)]):
    assert on_disc(x, y, 12), (x, y)
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#E4EDF4", opacity=45, stroke=NONE)
# faint window-ghost chrome on the backdrop corners
d.path("M60,150 A95,95 0 0 1 155,60", "Ghost arc TL",
       fill=NONE, stroke="#4A5E72", strokeWidth=16, opacity=10, cap="round")
d.path("M940,760 A110,110 0 0 1 850,875", "Ghost arc BR",
       fill=NONE, stroke="#4A5E72", strokeWidth=10, opacity=8, cap="round")

# --- monitor: the blank white page ----------------------------------------------
# stand + foot first
d.shape("rectangle", "Stand neck", x=676, y=482, width=48, height=48,
        fill="#2A2F38", stroke=INK, strokeWidth=4)
d.shape("rectangle", "Stand foot", x=632, y=524, width=136, height=18, radius=9,
        fill="#2A2F38", stroke=INK, strokeWidth=4)
# case
d.shape("rectangle", "Monitor case", x=550, y=248, width=300, height=234,
        radius=14, fill=CASE_GRAD, stroke=INK, strokeWidth=6)
# the white screen of death — blank, glowing, blameless
d.shape("rectangle", "White page", x=570, y=266, width=260, height=186,
        radius=6, fill=SCR_GRAD, stroke="#11161C", strokeWidth=4)
# faint reflected window-edge ghosts on the white (it loaded *something*)
d.shape("rectangle", "Ghost pane 1", x=586, y=282, width=110, height=60,
        radius=5, fill="#FFFFFF", opacity=55, stroke="#D4DCE2", strokeWidth=2)
d.shape("rectangle", "Ghost pane 2", x=710, y=282, width=100, height=20,
        radius=4, fill="#FFFFFF", opacity=40, stroke="#DDE4EA", strokeWidth=2)
# power LED, mockingly healthy
d.shape("ellipse", "Power LED", x=696, y=462, width=12, height=12,
        fill="#8AE07A", opacity=90, stroke=NONE)
# screen glow spilling toward Jay
d.shape("ellipse", "Screen glow", x=510, y=310, width=220, height=170,
        fill="#FFFFFF", opacity=13, stroke=NONE)
for x, y in [(550, 248), (850, 248), (850, 482), (550, 482)]:
    assert on_disc(x, y, 0), (x, y)

# --- devtools console, tilted, forty-seven log lines deep ------------------------
# built upright around a local origin, then rotated -6 deg
con_parts = []
def cshape(shape_, label, **kw):
    r = d.shape(shape_, label, **kw); con_parts.append(r); return r
def cpath(dd, label, **kw):
    r = d.path(dd, label, **kw); con_parts.append(r); return r
def ctext(t, label, **kw):
    r = d.text(t, label, **kw); con_parts.append(r); return r

CX0, CY0, CW, CH = 560, 500, 262, 150          # console rect (pre-rotation)
cshape("rectangle", "Console frame", x=CX0, y=CY0, width=CW, height=CH,
       radius=10, fill=CON_GRAD, stroke=INK, strokeWidth=5)
cshape("rectangle", "Console titlebar", x=CX0, y=CY0, width=CW, height=26,
       radius=10, fill="#2C3A42", stroke=NONE)
cshape("rectangle", "Titlebar mask", x=CX0, y=CY0+16, width=CW, height=12,
       fill="#2C3A42", stroke=NONE)
# traffic dots
for i, c in enumerate(["#E0604E", "#E8B44A", "#7FD06E"]):
    cshape("ellipse", f"Win dot {i+1}", x=CX0+14+i*20, y=CY0+7,
           width=12, height=12, fill=c, opacity=90, stroke=NONE)
ctext("console — 47 logs", "Console title", x=CX0+78, y=CY0+19, size=12,
      font="Source Sans 3", color="#9FB4BE", justify="left")
# log lines: a wall of explanations that explain nothing
log_cols = ["#7FD06E", "#C9D8E0", "#7FD06E", "#E8B44A", "#C9D8E0",
            "#E0604E", "#C9D8E0", "#7FD06E", "#C9D8E0", "#E8B44A",
            "#C9D8E0", "#C9D8E0", "#E0604E", "#7FD06E"]
log_w = [200, 150, 176, 108, 206, 132, 188, 96, 168, 120, 200, 142, 110, 178]
for i, (c, w) in enumerate(zip(log_cols, log_w)):
    y = CY0 + 38 + i * 8
    cshape("rectangle", f"Log line {i+1}", x=CX0+12, y=y, width=w,
           height=4, radius=2, fill=c, opacity=78, stroke=NONE)
# scrollbar, mid-scroll, nowhere near the bottom
cshape("rectangle", "Scroll track", x=CX0+CW-16, y=CY0+34, width=8,
       height=CH-44, radius=4, fill="#0C1418", stroke=NONE)
cshape("rectangle", "Scroll thumb", x=CX0+CW-16, y=CY0+58, width=8,
       height=26, radius=4, fill="#5E7482", stroke=NONE)
# rotate the whole console a touch — it's leaning on the monitor's bezel
for r in con_parts:
    if r and r.get("id"):
        d.cmd("object.rotate", f"tilt {r['id']}", ids=[r["id"]],
              angle=-6, origin=[CX0+CW/2, CY0+CH/2])

# --- ground shadow ---------------------------------------------------------------
d.shape("ellipse", "Ground shadow", x=190, y=690, width=300, height=28,
        fill="#1A2028", opacity=28, stroke=NONE)
d.shape("ellipse", "Console shadow", x=560, y=676, width=270, height=22,
        fill="#1A2028", opacity=22, stroke=NONE)

# --- Jay: the body ----------------------------------------------------------------
def body_path(cx, cy):
    return ("M%.0f,%.0f "
            "C%.0f,%.0f %.0f,%.0f %.0f,%.0f "
            "C%.0f,%.0f %.0f,%.0f %.0f,%.0f "
            "C%.0f,%.0f %.0f,%.0f %.0f,%.0f "
            "C%.0f,%.0f %.0f,%.0f %.0f,%.0f Z" % (
        cx,      cy - 160,
        cx + 118, cy - 160, cx + 150, cy - 84, cx + 138, cy - 6,
        cx + 130, cy + 90,  cx + 92,  cy + 142, cx,       cy + 142,
        cx - 96,  cy + 142, cx - 132, cy + 92,  cx - 140, cy + 2,
        cx - 152, cy - 80,  cx - 116, cy - 160, cx,       cy - 160))

JX, JY = 330, 556
d.path(body_path(JX, JY), "Body", fill=BODY_GRAD, stroke=INK, strokeWidth=6)
# belly
d.shape("ellipse", "Belly", x=252, y=566, width=158, height=116,
        fill=BELLY_GRAD, opacity=70, stroke=NONE)
# top-of-head sheen + lower shade
d.shape("ellipse", "Head sheen", x=240, y=408, width=190, height=62,
        fill="#FFFFFF", opacity=22, stroke=NONE)
d.path("M238,672 C300,700 360,700 424,672 C370,690 290,690 238,672 Z",
       "Base shade", fill="#7E4E20", opacity=35, stroke=NONE)
# monitor light kissing his right flank
d.shape("ellipse", "Flank glow", x=420, y=470, width=70, height=150,
        fill="#FFFFFF", opacity=14, stroke=NONE)

# cowlick: a jaunty little spark of confidence
d.path("M318,398 C310,368 322,350 344,342 C332,358 336,372 352,378 "
       "C338,382 332,392 336,404 Z",
       "Cowlick", fill="#D98A36", stroke=INK, strokeWidth=4, join="round")

# arms: left hand on hip-cocky, right flung up presenting the monitor
d.path("M206,560 C178,576 170,606 186,626", "Arm L",
       fill=NONE, stroke="#DE9438", strokeWidth=26, cap="round")
d.path("M456,500 C496,470 526,436 548,398", "Arm R",
       fill=NONE, stroke="#DE9438", strokeWidth=26, cap="round")
# little open paw at the end of the presenting arm
d.shape("ellipse", "Paw R", x=540, y=372, width=34, height=30,
        fill="#F0AE50", stroke=INK, strokeWidth=4)
d.path("M548,376 L556,364 M560,378 L572,370", "Paw fingers",
       fill=NONE, stroke=INK, strokeWidth=3, cap="round")

# feet: two smug little stubs
d.shape("ellipse", "Foot L", x=240, y=688, width=72, height=30,
        fill="#B06E2A", stroke=INK, strokeWidth=5)
d.shape("ellipse", "Foot R", x=352, y=688, width=72, height=30,
        fill="#B06E2A", stroke=INK, strokeWidth=5)

# face: bright confident eyes locked on the disaster, huge easy grin
for cx in (290, 382):
    d.shape("ellipse", f"Eye white {cx}", x=cx-24, y=470, width=48, height=46,
            fill="#FBF6EC", stroke=INK, strokeWidth=4)
    d.shape("ellipse", f"Pupil {cx}", x=cx-2, y=484, width=18, height=18,
            fill="#2C2622", stroke=NONE)
    d.shape("ellipse", f"Glint {cx}", x=cx+3, y=488, width=6, height=6,
            fill="#FFFFFF", opacity=90, stroke=NONE)
# raised optimistic brows
d.path("M266,456 C278,448 296,446 308,452", "Brow L",
       fill=NONE, stroke=INK, strokeWidth=5, cap="round")
d.path("M360,450 C374,442 392,442 404,450", "Brow R",
       fill=NONE, stroke=INK, strokeWidth=5, cap="round")
# the grin of a man who has not opened the console yet
d.path("M282,560 C306,596 366,600 398,566 C384,604 312,612 282,560 Z",
       "Grin", fill="#5C3222", stroke=INK, strokeWidth=5, join="round")
d.path("M300,568 C330,584 366,582 388,566", "Grin teeth",
       fill=NONE, stroke="#F8E8D0", strokeWidth=6, cap="round")
# one blush-mark of pure unbothered confidence
d.shape("ellipse", "Blush L", x=238, y=540, width=30, height=16,
        fill="#E07040", opacity=40, stroke=NONE)
d.shape("ellipse", "Blush R", x=404, y=534, width=30, height=16,
        fill="#E07040", opacity=40, stroke=NONE)

# --- a "ship it" sticky note on his chest -----------------------------------------
nt = d.shape("rectangle", "Sticky note", x=306, y=612, width=58, height=50,
             radius=4, fill="#F4E8B8", stroke=INK, strokeWidth=3)
if nt and nt.get("id"):
    d.cmd("object.rotate", "sticky tilt", ids=[nt["id"]], angle=-8,
          origin=[335, 637])
st = d.text("ship it", "Sticky text", x=335, y=646, size=15,
            font="Virelai Sans", color="#6A5230", justify="center")
if st and st.get("id"):
    d.cmd("object.rotate", "sticky text tilt", ids=[st["id"]], angle=-8,
          origin=[335, 637])

# --- name + role -------------------------------------------------------------------
d.text("JAY SKRIPT", "Name", x=500, y=930, size=58, font="Virelai Sans",
       color="#E4DAC6", justify="center")
r = d.text("CLIENT-SIDE ENABLER", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#9AAAC0", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=220)

d.finish("016.jay-skript-V1R00")
