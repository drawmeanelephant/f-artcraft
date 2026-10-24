#!/usr/bin/env python3
"""Hover Parish — mascot portrait V1R00.
A dark page of primary text; the truth lives one layer down. A cursor is
held perfectly still over an asterisk, and in the little black tooltip the
parish is in session: four hooded congregants at their tiny backs, one
officiant at the altar, two candles lit. Attendance is perfect in a sense
the record does not define. Hold still.
1000x1000. Gradients + translucent shading, no flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Hover Parish — Mascot Portrait", 1000, 1000)

INK = "#2A2118"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#10141A"}, {"offset": 1, "color": "#05070B"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#333C46"}, {"offset": 0.7, "color": "#20262E"},
    {"offset": 1, "color": "#11161C"}]}}
TIP_GLOW = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E8B25C", "opacity": 0.16},
    {"offset": 0.6, "color": "#E8B25C", "opacity": 0.06},
    {"offset": 1, "color": "#E8B25C", "opacity": 0}]}}
ALTAR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5E472E"}, {"offset": 1, "color": "#3A2C1C"}]}}

PCX, PCY, PR = 500, 460, 420
def on_disc(x, y, pad):
    assert math.hypot(x - PCX, y - PCY) <= PR - pad, (x, y)

def rrect(x, y, w, h, r):
    return (f"M{x+r},{y} L{x+w-r},{y} Q{x+w},{y} {x+w},{y+r} "
            f"L{x+w},{y+h-r} Q{x+w},{y+h} {x+w-r},{y+h} "
            f"L{x+r},{y+h} Q{x},{y+h} {x},{y+h-r} "
            f"L{x},{y+r} Q{x},{y} {x+r},{y} Z")

def asterisk(cx, cy, r, label, color, wdt, op):
    for dx, dy in [(0, 1), (-0.87, 0.5), (0.87, 0.5)]:
        d.path(f"M{cx - dx*r},{cy - dy*r} L{cx + dx*r},{cy + dy*r}",
               f"{label}", fill=NONE, stroke=color, strokeWidth=wdt,
               cap="round", opacity=op)

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#333C46", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#5E6E7E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#B8C8D4", strokeWidth=3, opacity=40)
for i, (x, y, w) in enumerate([(200,252,7),(802,246,8),(162,472,8),(838,484,7),
                               (266,768,6),(734,772,7),(136,364,6),(862,354,6),
                               (398,108,7),(604,104,8),(326,152,5),(688,148,6)]):
    on_disc(x + w / 2, y + w / 2, 8)
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#4E5A66", opacity=45, stroke=NONE)

# --- the primary text: it is a lie ----------------------------------------------
LINE = "#5A6A74"
for i, (x0, x1, y) in enumerate([(262, 742, 176), (262, 700, 204),
                                 (262, 640, 232), (672, 758, 232),
                                 (262, 520, 260), (262, 380, 288),
                                 (224, 560, 406), (224, 368, 458),
                                 (398, 690, 458), (224, 380, 510),
                                 (224, 304, 538), (224, 560, 566),
                                 (224, 640, 594), (224, 480, 622),
                                 (224, 520, 650), (224, 360, 678)]):
    d.path(f"M{x0},{y} L{x1},{y}", f"Body copy {i+1}", fill=NONE,
           stroke=LINE, strokeWidth=5, cap="round", opacity=32)
# the asterisk that is worshipped, mid-sentence
asterisk(383, 458, 10, "The asterisk", "#E8C060", 3.5, 95)
# its worn-smooth twin, far away and unvisited
asterisk(656, 232, 9, "Dead asterisk", "#6A7684", 3, 45)
# hover ring, faint
d.shape("ellipse", "Hover ring", x=366, y=441, width=34, height=34,
        fill=NONE, stroke="#E8C060", strokeWidth=2, opacity=30)

# --- the cursor, held still -------------------------------------------------------
d.path("M382,458 L382,492 L390,485 L395,498 L401,495 L396,482 L407,482 Z",
       "Cursor", fill="#F2EEE0", stroke="#181410", strokeWidth=2.5,
       join="round")
# held-still shimmer ticks around the point
for i, (x, y) in enumerate([(370, 444), (398, 444)]):
    d.path(f"M{x},{y} L{x + 4},{y - 4}", f"Still tick {i+1}", fill=NONE,
           stroke="#E8C060", strokeWidth=2.5, cap="round", opacity=60)

# --- the little black box: either a sanctuary or a margin ---------------------------
d.path(rrect(343, 262, 300, 168, 12), "Tip shadow", fill="#000000",
       opacity=45, stroke=NONE)
d.path(rrect(335, 254, 300, 168, 12), "Tooltip", fill="#0B0D12",
       stroke="#D8D4C4", strokeWidth=2.5)
# the tail, pointed at the verse
d.path("M400,420 L436,420 L390,452 Z", "Tip tail", fill="#0B0D12",
       stroke="#D8D4C4", strokeWidth=2.5, join="round")
d.path("M403,417 L433,417", "Tail join", fill=NONE, stroke="#0B0D12",
       strokeWidth=4, cap="round")

# --- inside: the parish is in session ------------------------------------------------
d.shape("ellipse", "Chapel glow", x=375, y=285, width=220, height=125,
        fill=TIP_GLOW, stroke=NONE)
# a line of liturgy no one has finished reading
d.path("M400,278 L430,278 M540,278 L570,278", "Liturgy stubs", fill=NONE,
       stroke="#6A7684", strokeWidth=3.5, cap="round", opacity=50)

# officiant behind the altar, mid-utterance
d.path("M472,344 C470,330 468,318 470,308 C472,296 482,292 485,292 "
       "C488,292 498,296 500,308 C502,318 500,330 498,344 Z",
       "Officiant robe", fill="#2E2438", stroke="#1A1420", strokeWidth=2.5)
d.shape("ellipse", "Officiant face", x=476, y=298, width=18, height=16,
        fill="#E8D8BC", stroke=NONE)
d.shape("ellipse", "Officiant eye L", x=479, y=303, width=3, height=4,
        fill="#1A1420", stroke=NONE)
d.shape("ellipse", "Officiant eye R", x=488, y=303, width=3, height=4,
        fill="#1A1420", stroke=NONE)
d.shape("ellipse", "Officiant mouth", x=483, y=309, width=4, height=3,
        fill="#1A1420", opacity=70, stroke=NONE)
# arms raised in the two-word liturgy
d.path("M470,332 C462,328 456,322 452,314", "Officiant arm L", fill=NONE,
       stroke="#2E2438", strokeWidth=8, cap="round")
d.path("M500,332 C508,328 514,322 518,314", "Officiant arm R", fill=NONE,
       stroke="#2E2438", strokeWidth=8, cap="round")
# the stole, a sliver of gold
d.path("M480,320 L479,340 M490,320 L491,340", "Stole", fill=NONE,
       stroke="#C9A44E", strokeWidth=2, opacity=80)

# altar + the open secondary text
d.path(rrect(452, 378, 66, 32, 4), "Altar", fill=ALTAR_GRAD,
       stroke="#1A1208", strokeWidth=2.5)
d.path("M466,372 C472,368 480,368 485,372 C490,368 498,368 504,372 "
       "L504,380 C498,376 490,376 485,380 C480,376 472,376 466,380 Z",
       "Open text", fill="#EDE6D2", stroke="#8A8474", strokeWidth=1.5)
d.path("M485,372 L485,379", "Spine fold", fill=NONE, stroke="#8A8474",
       strokeWidth=1.5, opacity=70)

# two candles, two flames, no wind
for i, cx in enumerate([438, 536]):
    d.shape("ellipse", f"Candle {i+1} glow", x=cx - 12, y=352, width=24,
            height=30, fill="#E8B25C", opacity=18, stroke=NONE)
    d.path(rrect(cx - 3, 372, 6, 18, 2), f"Candle {i+1}", fill="#E8DFC8",
           stroke="#9A8F72", strokeWidth=1.5)
    d.path(f"M{cx},360 C{cx + 4},366 {cx + 4},370 {cx},372 "
           f"C{cx - 4},370 {cx - 4},366 {cx},360 Z", f"Flame {i+1}",
           fill="#F0C060", stroke=NONE)

# the congregation, from behind — attendance is perfect
def congregant(cx, base, w, robe, tag, op=95):
    d.path(f"M{cx - w/2},{base} C{cx - w/2 - 2},{base - 24} {cx - w/4},{base - 40} "
           f"{cx},{base - 44} C{cx + w/4},{base - 40} {cx + w/2 + 2},{base - 24} "
           f"{cx + w/2},{base} Z", f"Congregant {tag}",
           fill=robe, stroke="#14101A", strokeWidth=2.5, opacity=op)
    # hood fold
    d.path(f"M{cx},{base - 40} L{cx},{base - 18}", f"Hood fold {tag}",
           fill=NONE, stroke="#14101A", strokeWidth=2, opacity=60 * op / 100,
           cap="round")

congregant(390, 410, 34, "#4A3A52", "1")
congregant(450, 410, 36, "#3E4A3C", "2")
congregant(525, 410, 36, "#523A32", "3")
# the fourth is dispersing mid-sentence; it resumes at the same word next hover
congregant(585, 410, 34, "#3A4252", "4", op=40)

# --- motes drifting in the held air ----------------------------------------------------
for i, (x, y, w) in enumerate([(250,330,5),(760,320,5),(200,560,4),(790,580,4),
                               (440,140,4),(600,150,5),(700,420,4)]):
    on_disc(x + w / 2, y + w / 2, 8)
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#B8C8D4", opacity=30, stroke=NONE)

# --- captions ---------------------------------------------------------------------------
d.text("HOVER PARISH", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#E4EAF0", justify="center")
r = d.text("ATTENTION IS PRAYER", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#9DB0C0", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("290.hover-parish-V1R00")
