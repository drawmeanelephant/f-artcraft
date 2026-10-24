#!/usr/bin/env python3
"""k4o — commemorative plate V1R00. The Knapping: a flint core mid-strike —
one hammerstone blow and the flakes flying off are template braces
({{ }}, {{/each}}, {{/if}}), each flake landing as a clean line of Textile
and CommonMark on the ground below. Flint grey with spark-orange strike
points; knapping as compilation. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("k4o — Commemorative Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#1B212B"   # warm dark, never pure black

def on_disc(x, y, pad):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

def lin(c0, c1, start=None, end=None):
    g = {"kind": "linear", "stops": [{"offset": 0, "color": c0}, {"offset": 1, "color": c1}]}
    if start: g["start"], g["end"] = [round(v, 1) for v in start], [round(v, 1) for v in end]
    return {"gradient": g}

def rad(*stops):
    return {"gradient": {"kind": "radial", "stops": stops}}

CPX, CPY = 552, 418          # strike contact point on the core's upper-right rim

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin("#111722", "#05080D", (500, 0), (500, 1000)), stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad({"offset": 0, "color": "#3A4450"},
                 {"offset": 0.65, "color": "#1B222E"},
                 {"offset": 1, "color": "#0A0E15"}),
        stroke="#55606E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#A8B4C0", strokeWidth=3, opacity=26)
# flint strata: faint concentric arcs in the crescent left of the core
def arc_left(cx, cy, r, a0, a1, label):
    p0 = (cx + r*math.cos(math.radians(a0)), cy + r*math.sin(math.radians(a0)))
    p1 = (cx + r*math.cos(math.radians(a1)), cy + r*math.sin(math.radians(a1)))
    assert on_disc(*p0, 12) and on_disc(*p1, 12) and on_disc(cx - r, cy, 12)
    d.path(f"M{p0[0]:.0f},{p0[1]:.0f} A{r},{r} 0 0 1 {p1[0]:.0f},{p1[1]:.0f}",
           label, fill=NONE, stroke="#7A8898", strokeWidth=2.5,
           opacity=15, cap="round")

arc_left(290, 580, 110, 115, 245, "Strata 1")
arc_left(290, 580, 135, 112, 248, "Strata 2")
arc_left(290, 580, 158, 110, 250, "Strata 3")
# knapping dust + chips inside the disc
for i, (x, y, w, o) in enumerate([(215,200,5,30),(790,195,6,26),(165,455,5,24),
                                  (845,425,5,26),(255,745,5,22),(740,760,6,22),
                                  (340,110,4,26),(665,105,5,24),(140,595,4,22),(870,585,5,24)]):
    assert on_disc(x, y, 12)
    d.shape("ellipse", f"Dust {i+1}", x=x-w/2, y=y-w/2, width=w, height=w,
            fill="#A8B4C4", opacity=o, stroke=NONE)

# --- the ground: a dark mound closing on the disc's own arc --------------------
d.path("M206.1,760 Q500,682 793.9,760 A420,420 0 0 1 206.1,760 Z", "Mound",
       fill=lin("#161E2A", "#080C12", (500, 690), (500, 880)), stroke=NONE)
# debris chips resting on the mound — flakes struck before this blow
for i, (x, y, w, h, dg) in enumerate([(300, 745, 30, 14, -18), (352, 762, 24, 12, 10),
                                      (655, 752, 28, 13, 14), (610, 770, 20, 10, -8)]):
    t = math.radians(dg); c, s = math.cos(t), math.sin(t)
    pts = [(x + dx*c - dy*s, y + dx*s + dy*c)
           for dx, dy in [(-w/2, 0), (-w*0.1, -h), (w/2, -h*0.25), (w*0.15, h*0.5)]]
    d.path("M" + " L".join(f"{px:.1f},{py:.1f}" for px, py in pts) + " Z",
           f"Chip {i+1}", fill=lin("#5E6878", "#2E3744", (x, y-h), (x, y+h)),
           stroke="#1E2632", strokeWidth=2, opacity=85)

# --- the flint core -------------------------------------------------------------
d.shape("ellipse", "Core shadow", x=270, y=700, width=330, height=44,
        fill=rad({"offset": 0, "color": "#000000", "opacity": 0.5},
                 {"offset": 1, "color": "#000000", "opacity": 0}), stroke=NONE)
CORE = ("M430,378 C512,372 570,428 578,522 C585,620 545,712 452,732 "
        "C360,750 285,700 272,598 C260,500 300,384 430,378 Z")
d.path(CORE, "Core", fill=lin("#8A94A2", "#39424E", (330, 380), (520, 730)),
       stroke=INK, strokeWidth=6)
# top highlight where the core catches the light
d.shape("ellipse", "Core top light", x=340, y=395, width=160, height=60,
        fill="#C8D2DC", opacity=18, stroke=NONE)
# flake scars: angular facets, alternating light and dark, with ripple arcs
SCARS = [
    ("M365,455 L470,430 L505,490 L420,525 L370,500 Z", "#A8B2BE", 34),
    ("M330,540 L430,545 L455,620 L350,640 L318,590 Z", "#141C26", 30),
    ("M455,545 L545,540 L555,640 L470,685 L440,615 Z", "#98A4B0", 30),
    ("M380,650 L470,690 L430,725 L352,700 Z", "#1E2832", 32),
]
for i, (dstr, col, op) in enumerate(SCARS):
    d.path(dstr, f"Scar {i+1}", fill=col, opacity=op, stroke=NONE)
    # conchoidal ripple: one faint arc inside the facet
for i, (x0, y0, x1, y1, cx, cy) in enumerate([(380,470,480,445,430,500),
                                             (340,580,440,575,390,615),
                                             (465,585,545,575,505,635)]):
    d.path(f"M{x0},{y0} Q{cx},{cy} {x1},{y1}", f"Ripple {i+1}", fill=NONE,
           stroke="#C8D2DC", strokeWidth=2, opacity=22, cap="round")

# the fresh scar right under the strike — brightest facet, orange-rimmed
d.path("M508,384 L586,398 L572,462 L500,448 Z", "Fresh scar",
       fill=lin("#D8E0E8", "#8A96A4", (508, 384), (572, 462)),
       stroke="#C86A24", strokeWidth=3, opacity=95)
d.path("M512,392 L578,404", "Fresh scar glint", fill=NONE,
       stroke="#FFDFA8", strokeWidth=3, opacity=70, cap="round")

# --- the hammerstone, mid-blow from the upper right -----------------------------
# swing trails behind the cobble
d.path("M648,168 Q694,240 690,296", "Swing trail 1", fill=NONE,
       stroke="#A8B4C4", strokeWidth=5, opacity=22, cap="round")
d.path("M712,150 Q740,230 726,296", "Swing trail 2", fill=NONE,
       stroke="#A8B4C4", strokeWidth=4, opacity=16, cap="round")
d.path("M590,190 Q640,258 650,316", "Swing trail 3", fill=NONE,
       stroke="#FF9A3C", strokeWidth=3.5, opacity=30, cap="round")
# cobble: an off-round blob, warm grey-brown
d.path("M614,320 C604,286 630,256 668,251 C706,246 738,268 743,300 "
       "C748,334 726,362 688,369 C650,376 622,354 614,320 Z",
       "Hammerstone", fill=lin("#8A7A62", "#463B2C", (620, 255), (740, 365)),
       stroke="#2E2419", strokeWidth=4.5)
d.path("M630,300 C640,278 668,266 694,270", "Hammer facet hi", fill=NONE,
       stroke="#B8A888", strokeWidth=5, opacity=55, cap="round")
d.path("M700,340 C716,332 726,318 728,304", "Hammer facet lo", fill=NONE,
       stroke="#2E2419", strokeWidth=4, opacity=50, cap="round")

# --- the strike: spark burst at the contact point --------------------------------
d.shape("ellipse", "Strike glow", x=CPX-72, y=CPY-72, width=144, height=144,
        fill=rad({"offset": 0, "color": "#FFC76E", "opacity": 0.75},
                 {"offset": 0.5, "color": "#FF8A34", "opacity": 0.28},
                 {"offset": 1, "color": "#FF8A34", "opacity": 0}), stroke=NONE)
for i, (dx, dy, ln) in enumerate([(1, -0.3, 52), (0.9, 0.25, 44), (0.55, -0.85, 40),
                                  (0.25, 0.95, 34), (-0.2, -0.95, 30), (0.75, 0.65, 36)]):
    n = math.hypot(dx, dy)
    ux, uy = dx / n, dy / n
    d.path(f"M{CPX + ux*8:.0f},{CPY + uy*8:.0f} L{CPX + ux*ln:.0f},{CPY + uy*ln:.0f}",
           f"Spark {i+1}", fill=NONE, stroke="#FFE9B0", strokeWidth=3.5,
           opacity=90, cap="round")
    d.shape("ellipse", f"Spark tip {i+1}", x=CPX + ux*ln - 3, y=CPY + uy*ln - 3,
            width=6, height=6, fill="#FF9A3C", opacity=85, stroke=NONE)
# white-hot contact star
d.path(f"M{CPX-16},{CPY} L{CPX-4},{CPY-4} L{CPX},{CPY-16} L{CPX+4},{CPY-4} "
       f"L{CPX+16},{CPY} L{CPX+4},{CPY+4} L{CPX},{CPY+16} L{CPX-4},{CPY+4} Z",
       "Strike star", fill="#FFF6DA", stroke=NONE)

# --- the flakes: template braces mid-flight --------------------------------------
def flake(bx, by, ang, L, W, label, glyph, gsize):
    """A struck flake: bulb (rounded base) near the strike, tip flying away.
    ang = flight direction in degrees; glyph = brace text on the shard."""
    t = math.radians(ang); ux, uy = math.cos(t), math.sin(t)
    px, py = -uy, ux
    tip = (bx + ux*L, by + uy*L)
    assert on_disc(*tip, 14), tip
    s1 = (bx + ux*0.3*L + px*W/2, by + uy*0.3*L + py*W/2)
    s2 = (bx + ux*0.3*L - px*W/2, by + uy*0.3*L - py*W/2)
    bulb = (bx - ux*W*0.2, by - uy*W*0.2)
    d.path(f"M{tip[0]:.1f},{tip[1]:.1f} L{s1[0]:.1f},{s1[1]:.1f} "
           f"Q{bulb[0]:.1f},{bulb[1]:.1f} {s2[0]:.1f},{s2[1]:.1f} Z",
           label, fill=lin("#B8C2CE", "#4E5A68", (bx, by), tip),
           stroke=INK, strokeWidth=3.5)
    # leading-edge glint + conchoidal band inside the shard
    mx, my = bx + ux*0.62*L, by + uy*0.62*L
    d.path(f"M{s1[0]:.1f},{s1[1]:.1f} Q{bulb[0]:.1f},{bulb[1]:.1f} {s2[0]:.1f},{s2[1]:.1f}",
           f"{label} ripple", fill=NONE, stroke="#E8EEF4", strokeWidth=2,
           opacity=35, cap="round")
    # the brace glyph riding on the shard (Source Sans 3 — code syntax font;
    # also dodges any Virelai punctuation gaps)
    gx, gy = bx + ux*0.34*L, by + uy*0.34*L
    d.text(glyph, f"{label} glyph", x=gx, y=gy + gsize*0.34, size=gsize,
           font="Source Sans 3", color="#141A22", justify="center")
    # short speed streak behind the bulb
    d.path(f"M{bulb[0] - ux*6:.0f},{bulb[1] - uy*6:.0f} "
           f"L{bulb[0] - ux*(L*0.35):.0f},{bulb[1] - uy*(L*0.35):.0f}",
           f"{label} streak", fill=NONE, stroke="#FFB050", strokeWidth=3,
           opacity=40, cap="round")

flake(566, 396, -38, 128, 46, "Flake open",  "{{", 24)
flake(576, 420, -6, 168, 52, "Flake close", "}}", 24)
flake(566, 446, 26, 182, 62, "Flake each",  "{{/each}}", 16)
flake(548, 462, 52, 148, 50, "Flake if",    "{{/if}}", 17)

# --- landed lines: each flake settles as a clean line of markup ------------------
LX = 336                       # left edge of the typeset block
def mline(y, mark, x1, w, label):
    d.text(mark, f"{label} mark", x=LX, y=y + 6, size=19, font="Source Sans 3",
           color="#8FA0B4", justify="center")
    d.path(f"M{LX + 18},{y} L{x1},{y}", f"{label} line", fill=NONE,
           stroke="#C8D2DC", strokeWidth=w, opacity=82, cap="round")

mline(752, "#",  545, 7, "Heading")     # CommonMark heading, heavier
mline(780, ">",  640, 5, "Quote")       # blockquote line
mline(804, "-",  512, 5, "List item")   # list item
# one flake still landing: a shard half-settled at the stack's left edge
d.path("M300,786 L318,768 L334,790 L318,802 Z", "Landing flake",
       fill=lin("#98A4B0", "#46525F", (300, 768), (334, 802)),
       stroke=INK, strokeWidth=3)

# --- name + role ------------------------------------------------------------------
NAME = "K4O"
rn = d.text(NAME, "Name", x=500, y=930, size=60, font="Virelai Sans",
            color="#DCE4EC", justify="center")
# Virelai Sans has no digits — set "4" (bytes 1..2) in Source Sans 3
d.cmd("text.setStyle", "Name digit", id=rn["id"], font="Source Sans 3",
      start=1, end=2, size=62)
LINE2, SZ2, TRK = "KNAP TEMPLATE ENGINE", 23, 300
r = d.text(LINE2, "Second line", x=500, y=968, size=SZ2, font="Virelai Sans",
           color="#8FA0B4", justify="center")
d.cmd("text.setStyle", "Second line tracking", id=r["id"], tracking=TRK)
def find(o, oid):
    if isinstance(o, dict):
        if o.get("id") == oid and "bounds" in o: return o
        o = list(o.values())
    if isinstance(o, list):
        for v in o:
            hit = find(v, oid)
            if hit: return hit
b2 = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("second line bounds", {k: round(v) for k, v in b2.items()})
assert b2["width"] <= 760 and b2["x"] >= 100 and b2["y"] + b2["height"] <= 990, b2

d.finish("k4o-V1R00")
