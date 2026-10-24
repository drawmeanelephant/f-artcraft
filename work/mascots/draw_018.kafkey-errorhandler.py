#!/usr/bin/env python3
"""Kafkey Errorhandler — mascot portrait V1R00. Event Stream Overthinker:
a tuxedo'd mourner extending a lit taper toward the candles of the
dead-letter shrine — a leaning choir of annotated failed envelopes on a
stone step, each one mourned, footnoted and marked undeliverable.
Candle-gold on a deep plum plate. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Kafkey Errorhandler — Mascot Plate", 1000, 1000)

INK = "#261E28"   # warm dark ink, never black
BG_GRAD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000], "stops": [
    {"offset": 0, "color": "#191020"}, {"offset": 1, "color": "#080510"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#A89490"}, {"offset": 0.62, "color": "#6E5658"},
    {"offset": 1, "color": "#3C2E38"}]}}
TUX_GRAD = {"gradient": {"kind": "linear", "start": [0, 380], "end": [0, 720], "stops": [
    {"offset": 0, "color": "#463E4E"}, {"offset": 0.55, "color": "#322C3A"},
    {"offset": 1, "color": "#1E1A24"}]}}
PAPER_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E8DCBC"}, {"offset": 1, "color": "#C4B48E"}]}}
WAX_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F0E4C4"}, {"offset": 1, "color": "#C8B48C"}]}}
FLAME_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#FBE9A8"}, {"offset": 0.55, "color": "#F2B84E"},
    {"offset": 1, "color": "#D06E28"}]}}

PCX, PCY, PR = 500, 460, 420

def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

def candle(x, y, h, w, tag):
    """Wax cylinder at (x,y) top-left, h tall, w wide, with flame + halo."""
    d.shape("ellipse", f"Halo {tag}", x=x - 26, y=y - 44, width=w + 52,
            height=h * 0.5 + 70, fill="#F2B84E", opacity=13, stroke=NONE)
    d.shape("rectangle", f"Wax {tag}", x=x, y=y, width=w, height=h,
            radius=w * 0.28, fill=WAX_GRAD, stroke=INK, strokeWidth=3.5)
    # drip
    d.path("M%.0f,%.0f C%.0f,%.0f %.0f,%.0f %.0f,%.0f" % (
        x + w * 0.72, y + 4, x + w * 0.86, y + 8, x + w * 0.84, y + 22,
        x + w * 0.78, y + 26), f"Drip {tag}", fill=NONE,
        stroke="#A89070", strokeWidth=3, cap="round")
    # wick + flame
    fx = x + w / 2
    d.path("M%.0f,%.0f L%.0f,%.0f" % (fx, y + 2, fx, y - 6), f"Wick {tag}",
           fill=NONE, stroke=INK, strokeWidth=2.5, cap="round")
    d.path("M%.0f,%.0f C%.0f,%.0f %.0f,%.0f %.0f,%.0f "
           "C%.0f,%.0f %.0f,%.0f %.0f,%.0f Z" % (
        fx, y - 34, fx + 11, y - 20, fx + 10, y - 8, fx, y - 6,
        fx - 10, y - 8, fx - 11, y - 20, fx, y - 34),
        f"Flame {tag}", fill=FLAME_GRAD, stroke=NONE)
    d.shape("ellipse", f"Flame core {tag}", x=fx - 4, y=y - 20, width=8,
            height=12, fill="#FDF3C8", opacity=90, stroke=NONE)

# --- backdrop + plate --------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#9A8288", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#1C141E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8C6BC", strokeWidth=3, opacity=38)
# candle-smoke patina
d.shape("ellipse", "Patina 1", x=180, y=150, width=250, height=150,
        fill="#BCA8A4", opacity=15, stroke=NONE)
d.shape("ellipse", "Patina 2", x=560, y=160, width=230, height=130,
        fill="#8E7268", opacity=18, stroke=NONE)
for i, (x, y, w) in enumerate([(200,335,6),(812,325,5),(172,540,7),(846,548,6),
                               (252,758,5),(738,762,6),(146,438,5),(862,614,5),
                               (432,114,5),(612,136,6),(322,152,4),(706,208,5),
                               (216,648,4),(876,448,4)]):
    assert on_disc(x, y, 12), (x, y)
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#EDE2D4", opacity=40, stroke=NONE)
# faint ghost arcs on the dark backdrop
d.path("M60,148 A95,95 0 0 1 155,60", "Ghost arc TL",
       fill=NONE, stroke="#5C4A58", strokeWidth=14, opacity=10, cap="round")
d.path("M942,762 A110,110 0 0 1 850,876", "Ghost arc BR",
       fill=NONE, stroke="#5C4A58", strokeWidth=10, opacity=8, cap="round")

# --- the dead-letter shrine -----------------------------------------------------------
# ambient candle-wash over the whole shrine corner first
d.shape("ellipse", "Shrine glow", x=560, y=430, width=300, height=280,
        fill="#F2B84E", opacity=10, stroke=NONE)
# candles behind the letters
candle(600, 470, 128, 30, "tall L")
candle(648, 510, 88, 26, "mid L")
candle(778, 452, 140, 32, "tall R")
candle(828, 522, 76, 24, "mid R")
# the stone step the queue stands on
d.shape("rectangle", "Shrine step", x=556, y=638, width=290, height=56,
        radius=10, fill="#463C44", stroke=INK, strokeWidth=5)
d.shape("rectangle", "Step top edge", x=556, y=638, width=290, height=14,
        radius=7, fill="#5A4E56", opacity=80, stroke=NONE)
d.text("D L Q", "Step plaque", x=762, y=678, size=20, font="Virelai Sans",
       color="#C8B4A0", justify="center")
for x, y in [(556, 638), (846, 638), (846, 694), (556, 694)]:
    assert on_disc(x, y, 0), (x, y)

# the queue: five failed envelopes leaning on the step, each annotated
def envelope(x, y, w, h, ang, tag, marks):
    parts = []
    r = d.shape("rectangle", f"Env {tag}", x=x, y=y, width=w, height=h,
                radius=5, fill=PAPER_GRAD, stroke=INK, strokeWidth=3.5)
    parts.append((r, x + w / 2, y + h / 2))
    # flap
    r = d.path("M%.0f,%.0f L%.0f,%.0f L%.0f,%.0f" % (x + 4, y + 4,
               x + w / 2, y + h * 0.55, x + w - 4, y + 4), f"Flap {tag}",
               fill=NONE, stroke="#8E7A5C", strokeWidth=3, join="round")
    parts.append((r, x + w / 2, y + h / 2))
    # annotation scribbles in mourning red
    for j, (mx, my, mx2, my2) in enumerate(marks):
        r = d.path("M%.0f,%.0f C%.0f,%.0f %.0f,%.0f %.0f,%.0f" % (
            x + mx, y + my, x + mx + 6, y + my - 5, x + mx2 - 6,
            y + my2 + 4, x + mx2, y + my2), f"Note {tag} {j+1}",
            fill=NONE, stroke="#A83A3A", strokeWidth=2.5, opacity=85,
            cap="round")
        parts.append((r, x + w / 2, y + h / 2))
    for r, cx_, cy_ in parts:
        if r and r.get("id"):
            d.cmd("object.rotate", f"env rot {r['id']}", ids=[r["id"]],
                  angle=ang, origin=[cx_, cy_])

envelope(586, 566, 74, 92, -12, "a", [(14, 62, 44, 58), (18, 72, 50, 70)])
envelope(644, 548, 78, 96, -4, "b", [(16, 64, 52, 60), (12, 76, 34, 74),
                                      (40, 76, 60, 72)])
envelope(706, 560, 72, 90, 5, "c", [(14, 60, 46, 56), (20, 72, 54, 68)])
envelope(764, 570, 68, 84, 12, "d", [(14, 56, 42, 52)])
# one slid flat at the base, face down, beyond annotation
flat = d.shape("rectangle", "Env flat", x=618, y=668, width=96, height=60,
               radius=5, fill="#D8CCA8", stroke=INK, strokeWidth=3.5)
if flat and flat.get("id"):
    d.cmd("object.rotate", "flat rot", ids=[flat["id"]], angle=-7,
          origin=[666, 698])

# --- ground shadow ---------------------------------------------------------------------
d.shape("ellipse", "Ground shadow", x=190, y=692, width=290, height=28,
        fill="#161018", opacity=30, stroke=NONE)

# --- Kafkey: the tuxedo'd mourner ---------------------------------------------------------
KX, KY = 320, 560

def body_path(cx, cy):
    return ("M%.0f,%.0f "
            "C%.0f,%.0f %.0f,%.0f %.0f,%.0f "
            "C%.0f,%.0f %.0f,%.0f %.0f,%.0f "
            "C%.0f,%.0f %.0f,%.0f %.0f,%.0f "
            "C%.0f,%.0f %.0f,%.0f %.0f,%.0f Z" % (
        cx,      cy - 158,
        cx + 112, cy - 158, cx + 148, cy - 82, cx + 140, cy - 4,
        cx + 132, cy + 92,  cx + 90,  cy + 142, cx,       cy + 142,
        cx - 94,  cy + 142, cx - 134, cy + 92,  cx - 142, cy + 0,
        cx - 152, cy - 80,  cx - 114, cy - 158, cx,       cy - 158))

# tailcoat shadow on the ground side
d.path(body_path(KX, KY), "Tux body", fill=TUX_GRAD, stroke=INK, strokeWidth=6)
# head sheen — the only light he gets is candlelight
d.shape("ellipse", "Head sheen", x=246, y=412, width=170, height=58,
        fill="#F2B84E", opacity=12, stroke=NONE)
d.shape("ellipse", "Head sheen 2", x=250, y=414, width=150, height=52,
        fill="#FFFFFF", opacity=10, stroke=NONE)

# shirtfront: crisp white bib tapering into the waist
d.path("M296,470 L344,470 L356,640 C340,660 300,660 284,640 Z",
       "Shirtfront", fill="#F0E8D4", stroke=INK, strokeWidth=4, join="round")
# three studs
for i in range(3):
    d.shape("ellipse", f"Stud {i+1}", x=315, y=512 + i * 34, width=10,
            height=10, fill="#3A3440", stroke=NONE)
# lapels
d.path("M296,470 L268,520 L288,566 L296,470 Z", "Lapel L",
       fill="#4A4254", stroke=INK, strokeWidth=3.5, join="round")
d.path("M344,470 L374,520 L352,566 L344,470 Z", "Lapel R",
       fill="#4A4254", stroke=INK, strokeWidth=3.5, join="round")
# pocket square, starched into mourning points
d.path("M394,572 L420,572 L407,546 Z", "Pocket square",
       fill="#F0E8D4", stroke=INK, strokeWidth=3, join="round")
# bowtie: deep funeral red
d.path("M292,464 L320,478 L292,492 Z", "Bow L",
       fill="#8E2E3C", stroke=INK, strokeWidth=3.5, join="round")
d.path("M348,464 L320,478 L348,492 Z", "Bow R",
       fill="#8E2E3C", stroke=INK, strokeWidth=3.5, join="round")
d.shape("ellipse", "Bow knot", x=313, y=471, width=14, height=14,
        fill="#6E2230", stroke=INK, strokeWidth=3)

# arms: right extends the taper to the candles, left holds the eulogy card
d.path("M442,540 C486,534 520,522 552,506", "Arm R",
       fill=NONE, stroke="#322C3A", strokeWidth=26, cap="round")
d.shape("ellipse", "Paw R", x=540, y=490, width=32, height=30,
        fill="#463E4E", stroke=INK, strokeWidth=4)
# the taper: thin candle angled toward the shrine, already lit
tp = []
r = d.shape("rectangle", "Taper", x=560, y=462, width=9, height=58, radius=4,
            fill=WAX_GRAD, stroke=INK, strokeWidth=3)
tp.append(r)
r = d.path("M564,462 C575,450 575,438 564,428 C553,438 553,450 564,462 Z",
           "Taper flame", fill=FLAME_GRAD, stroke=NONE)
tp.append(r)
r = d.shape("ellipse", "Taper halo", x=540, y=414, width=50, height=58,
            fill="#F2B84E", opacity=16, stroke=NONE)
tp.append(r)
for r in tp:
    if r and r.get("id"):
        d.cmd("object.rotate", f"taper rot {r['id']}", ids=[r["id"]],
              angle=16, origin=[564, 500])
d.path("M204,560 C184,578 180,606 194,624", "Arm L",
       fill=NONE, stroke="#322C3A", strokeWidth=26, cap="round")
# eulogy card in the left paw
ec = []
r = d.shape("rectangle", "Eulogy card", x=176, y=596, width=62, height=76,
            radius=5, fill=PAPER_GRAD, stroke=INK, strokeWidth=3.5)
ec.append(r)
for i, w in enumerate([42, 34, 40, 22]):
    r = d.shape("rectangle", f"Eulogy line {i+1}", x=186, y=612 + i * 13,
                width=w, height=4, radius=2, fill="#8E7A5C", opacity=80,
                stroke=NONE)
    ec.append(r)
for r in ec:
    if r and r.get("id"):
        d.cmd("object.rotate", f"eulogy rot {r['id']}", ids=[r["id"]],
              angle=-10, origin=[207, 634])

# feet: polished dress stubs
d.shape("ellipse", "Foot L", x=236, y=690, width=72, height=30,
        fill="#1C1822", stroke=INK, strokeWidth=5)
d.shape("ellipse", "Foot R", x=332, y=690, width=72, height=30,
        fill="#1C1822", stroke=INK, strokeWidth=5)
d.path("M250,700 L294,700 M346,700 L390,700", "Shoe shine",
       fill=NONE, stroke="#6E5E78", strokeWidth=3, opacity=70, cap="round")

# face: solemn, heavy-lidded, brows peaked in condolence
for cx in (282, 366):
    d.shape("ellipse", f"Eye white {cx}", x=cx - 23, y=472, width=46,
            height=42, fill="#F4EFE4", stroke=INK, strokeWidth=4)
    d.shape("ellipse", f"Pupil {cx}", x=cx - 8, y=486, width=16, height=16,
            fill="#2A2228", stroke=NONE)
    d.shape("ellipse", f"Glint {cx}", x=cx - 4, y=489, width=5, height=5,
            fill="#FFFFFF", opacity=85, stroke=NONE)
    # mourning lid over the upper eye
    d.shape("ellipse", f"Lid {cx}", x=cx - 26, y=462, width=52, height=24,
            fill="#3A3342", stroke=NONE)
    d.path("M%.0f,%.0f C%.0f,%.0f %.0f,%.0f %.0f,%.0f" % (
        cx - 22, 480, cx - 6, 486, cx + 8, 486, cx + 22, 480),
        f"Lid crease {cx}", fill=NONE, stroke=INK, strokeWidth=3,
        opacity=70, cap="round")
# brows lifted at the center — the geometry of grief
d.path("M272,456 C284,446 300,442 312,448", "Brow L",
       fill=NONE, stroke=INK, strokeWidth=5, cap="round")
d.path("M332,448 C346,442 362,446 374,456", "Brow R",
       fill=NONE, stroke=INK, strokeWidth=5, cap="round")
# small downturned officiant mouth
d.path("M296,566 C312,558 336,558 350,568", "Mouth",
       fill=NONE, stroke=INK, strokeWidth=5, cap="round")

# --- name + role --------------------------------------------------------------------------
d.text("KAFKEY ERRORHANDLER", "Name", x=500, y=930, size=50,
       font="Virelai Sans", color="#E4D6C8", justify="center")
r = d.text("EVENT STREAM OVERTHINKER", "Role", x=500, y=968, size=22,
           font="Virelai Sans", color="#B09A96", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=170)

d.finish("018.kafkey-errorhandler-V1R00")
