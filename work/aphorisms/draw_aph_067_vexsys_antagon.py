#!/usr/bin/env python3
"""APH-067 Vexsys Antagon — aphorism plate V1R00. A dark editor card of
valid-looking JSON, green CI chip and all, whose bottom edge dissolves
into fragments spiraling down into a void; three tiny senior developers
are already in the accretion ring, and the merge clock froze at 03:12.
Deep indigo plate, code-green syntax, amber void glow. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("APH-067 Vexsys Antagon — Aphorism Plate", 1000, 1000)

INK = "#160F26"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1E1838"}, {"offset": 1, "color": "#0A0616"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#3E3660"}, {"offset": 0.7, "color": "#241C42"},
    {"offset": 1, "color": "#120D24"}]}}
CARD_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2A2440"}, {"offset": 1, "color": "#191430"}]}}
CHIP_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4CB868"}, {"offset": 1, "color": "#2A7A44"}]}}
VOID_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#050208"}, {"offset": 0.55, "color": "#0D0718"},
    {"offset": 0.8, "color": "#2A1840"}, {"offset": 1, "color": "#50306A"}]}}
KEY_C = "#9AD8F0"    # syntax: keys
VAL_C = "#B8E890"    # syntax: strings
PUNCT_C = "#8E84B8"  # syntax: braces/punctuation
CODE_GUTTER = "#6A6488"
AMBER = "#E8A850"
VIOLET = "#B8A8E0"
CREAM = "#E8E0F0"
FAINT = "#8E84B8"
KEY = "#C8BCE8"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#5A4E8A", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke=VIOLET, strokeWidth=3, opacity=35)
# plate patina
d.shape("ellipse", "Patina 1", x=190, y=160, width=210, height=120,
        fill="#4A3E70", opacity=20, stroke=NONE)
d.shape("ellipse", "Patina 2", x=610, y=620, width=220, height=130,
        fill="#4A3E70", opacity=16, stroke=NONE)
for i, (x, y, w) in enumerate([(215, 270, 7), (795, 240, 8), (160, 470, 6),
                               (845, 480, 7), (245, 660, 6), (760, 680, 7)]):
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#6A5C9A", opacity=35, stroke=NONE)
# faint static stars on the plate — the silent code
for i, (x, y) in enumerate([(255, 190), (700, 155), (820, 330), (185, 370),
                            (300, 530), (720, 545)]):
    d.shape("ellipse", f"Static {i+1}", x=x, y=y, width=3, height=3,
            fill=VIOLET, opacity=50, stroke=NONE)

# --- the merge clock, frozen at mismerge time ----------------------------------
d.shape("rectangle", "Clock chip", x=205, y=205, width=118, height=44,
        radius=8, fill=CARD_GRAD, stroke="#5A4E8A", strokeWidth=3)
d.text("MERGED", "Clock label", x=264, y=222, size=10, font="Source Sans 3",
       color=FAINT, justify="center")
d.text("03:12 AM", "Clock digits", x=264, y=241, size=15,
       font="Source Sans 3", color=AMBER, justify="center")
# two branch lines converge into one node, which feeds down to the card
d.path("M238,268 C250,292 268,300 292,302 M330,268 C330,290 312,300 292,302",
       "Merge branches", fill=NONE, stroke=PUNCT_C, strokeWidth=3,
       cap="round", opacity=70)
d.path("M292,302 C300,330 330,340 356,344", "Merge feed", fill=NONE,
       stroke=PUNCT_C, strokeWidth=3, cap="round", opacity=70)
d.shape("ellipse", "Merge node A", x=234, y=264, width=8, height=8,
        fill=NONE, stroke=PUNCT_C, strokeWidth=2.5, opacity=70)
d.shape("ellipse", "Merge node B", x=326, y=264, width=8, height=8,
        fill=NONE, stroke=PUNCT_C, strokeWidth=2.5, opacity=70)
d.shape("ellipse", "Merge node C", x=288, y=298, width=9, height=9,
        fill=PUNCT_C, opacity=80, stroke=NONE)

# --- the JSON editor card -------------------------------------------------------
CARD_X, CARD_Y, CARD_W, CARD_H = 350, 150, 300, 290
d.shape("rectangle", "Card shadow", x=CARD_X + 8, y=CARD_Y + 10,
        width=CARD_W, height=CARD_H, radius=10, fill="#000000",
        opacity=30, stroke=NONE)
d.shape("rectangle", "Editor card", x=CARD_X, y=CARD_Y, width=CARD_W,
        height=CARD_H, radius=10, fill=CARD_GRAD, stroke="#5A4E8A",
        strokeWidth=3)
# window chrome
for i, c in enumerate(["#C05A50", "#C89A4A", "#4CB868"]):
    d.shape("ellipse", f"Win dot {i+1}", x=CARD_X + 16 + i * 18,
            y=CARD_Y + 14, width=10, height=10, fill=c, opacity=85,
            stroke=NONE)
d.text("payload.json", "Card title", x=CARD_X + CARD_W - 14, y=CARD_Y + 25,
       size=12, font="Source Sans 3", color=FAINT, justify="right")
d.path(f"M{CARD_X},{CARD_Y + 40} L{CARD_X + CARD_W},{CARD_Y + 40}",
       "Titlebar rule", fill=NONE, stroke="#5A4E8A", strokeWidth=2,
       opacity=70)
# line-number gutter
for i, n in enumerate(["1", "2", "3", "4", "5", "6"]):
    d.text(n, f"Gutter {i+1}", x=CARD_X + 18, y=CARD_Y + 68 + i * 34,
           size=13, font="Source Sans 3", color=CODE_GUTTER, justify="left")
d.path(f"M{CARD_X + 34},{CARD_Y + 50} L{CARD_X + 34},{CARD_Y + CARD_H - 16}",
       "Gutter rule", fill=NONE, stroke="#5A4E8A", strokeWidth=1.5,
       opacity=60)

# the JSON — entirely legitimate
LX = CARD_X + 46          # code left edge
VX = LX + 92              # value column
LY = CARD_Y + 68          # first baseline
LH = 34                   # line height
d.text("{", "JSON open", x=LX, y=LY, size=16, font="Source Sans 3",
       color=PUNCT_C, justify="left")
for i, (k, v) in enumerate([('"status":', '"green"'), ('"merge":', '"clean",'),
                            ('"ci":', '"passed",'), ('"review":', '"ok"')]):
    yy = LY + (i + 1) * LH
    d.text(k, f"JSON key {i+1}", x=LX + 18, y=yy, size=16,
           font="Source Sans 3", color=KEY_C, justify="left")
    d.text(v, f"JSON val {i+1}", x=VX, y=yy, size=16,
           font="Source Sans 3", color=VAL_C, justify="left")
# the last line frays: key typed, value cursor blinking into nothing
yy = LY + 5 * LH
d.text('"deploy":', "JSON key 5", x=LX + 18, y=yy, size=16,
       font="Source Sans 3", color="#5A7A90", justify="left")
d.path(f"M{VX},{yy - 14} L{VX},{yy + 2}", "Cursor", fill=NONE,
       stroke=VAL_C, strokeWidth=3, opacity=80)
# the card's bottom edge is dissolving — bites taken out of the border
for i, (bx, bw) in enumerate([(CARD_X + 128, 20), (CARD_X + 158, 26),
                              (CARD_X + 192, 22)]):
    d.shape("rectangle", f"Edge bite {i+1}", x=bx, y=CARD_Y + CARD_H - 6,
            width=bw, height=12, fill="#191430", opacity=92, stroke=NONE)
# ragged edge stubs where the bites start
d.path(f"M{CARD_X + 128},{CARD_Y + CARD_H} L{CARD_X + 118},{CARD_Y + CARD_H - 10}",
       "Edge tear 1", fill=NONE, stroke="#5A4E8A", strokeWidth=2.5)
d.path(f"M{CARD_X + 214},{CARD_Y + CARD_H} L{CARD_X + 224},{CARD_Y + CARD_H - 9}",
       "Edge tear 2", fill=NONE, stroke="#5A4E8A", strokeWidth=2.5)

# --- green success signals -------------------------------------------------------
# CI chip riding high on the card corner
d.path(rot_rect_path(618, 148, 108, 34, 8), "CI chip",
       fill=CHIP_GRAD, stroke="#1E5A32", strokeWidth=3)
d.text("CI PASSED", "CI chip text", x=618, y=153, size=13,
       font="Source Sans 3", color="#EAF8E0", justify="center")
# a loose green check mid-fall, tumbling toward the void
d.path(rot_rect_path(618, 505, 44, 44, 24), "Check ghost",
       fill=CHIP_GRAD, stroke="#1E5A32", strokeWidth=2.5, opacity=45)
d.path("M604,505 L614,516 L634,494", "Check mark", fill=NONE,
       stroke="#EAF8E0", strokeWidth=5, cap="round", opacity=60)

# --- fragments falling from the card's open bottom -------------------------------
for i, (cx, cy, w, h, deg, op) in enumerate([
        (468, 462, 26, 10, -14, 75), (522, 472, 20, 9, 18, 70),
        (488, 496, 16, 8, -30, 60), (540, 508, 14, 7, 40, 55),
        (505, 528, 12, 6, -50, 50), (470, 540, 10, 6, 55, 45)]):
    d.path(rot_rect_path(cx, cy, w, h, deg), f"Fragment {i+1}",
           fill="#3A3260", opacity=op, stroke="#5A4E8A", strokeWidth=1.5)
# the closing brace, spiralling in — hand-drawn, one per orbit point
def brace(cx, cy, s, label, color, op):
    p = (f"M{cx},{cy} "
         f"C{cx + 9*s},{cy + 2*s} {cx + 11*s},{cy + 8*s} {cx + 11*s},{cy + 14*s} "
         f"C{cx + 11*s},{cy + 20*s} {cx + 15*s},{cy + 22*s} {cx + 19*s},{cy + 24*s} "
         f"C{cx + 15*s},{cy + 26*s} {cx + 11*s},{cy + 28*s} {cx + 11*s},{cy + 34*s} "
         f"C{cx + 11*s},{cy + 40*s} {cx + 9*s},{cy + 46*s} {cx},{cy + 48*s}")
    d.path(p, label, fill=NONE, stroke=color, strokeWidth=3.5,
           cap="round", opacity=op)

brace(452, 478, 0.55, "Brace fall 1", VAL_C, 70)
brace(556, 532, 0.42, "Brace fall 2", PUNCT_C, 55)
brace(430, 568, 0.34, "Brace fall 3", VAL_C, 45)

# --- the void ----------------------------------------------------------------------
VX0, VY0 = 500, 630       # void center
# accretion disc: tilted hot ring behind the hole
d.shape("ellipse", "Accretion glow", x=370, y=585, width=260, height=95,
        fill=NONE, stroke=AMBER, strokeWidth=10, opacity=30)
d.shape("ellipse", "Accretion ring", x=385, y=592, width=230, height=80,
        fill=NONE, stroke="#E8B870", strokeWidth=5, opacity=55)
# the hole itself
d.shape("ellipse", "Void", x=430, y=560, width=140, height=140,
        fill=VOID_GRAD, stroke="#8A5AC8", strokeWidth=4)
d.shape("ellipse", "Void core", x=462, y=592, width=76, height=76,
        fill="#050208", stroke=NONE)
# gravitational swirl: two arcs wrapping the hole
d.path("M392,596 C420,560 480,545 540,556 C590,565 622,590 626,615",
       "Swirl arm 1", fill=NONE, stroke=VIOLET, strokeWidth=4,
       cap="round", opacity=60)
d.path("M606,668 C575,700 505,712 448,698 C405,687 380,662 382,640",
       "Swirl arm 2", fill=NONE, stroke=VIOLET, strokeWidth=4,
       cap="round", opacity=45)
# spaghettified debris on the ring
for i, (cx, cy, w, h, deg) in enumerate([(398, 600, 18, 5, -28),
                                         (592, 614, 16, 5, 22),
                                         (436, 692, 14, 4, -12),
                                         (566, 685, 15, 4, 16)]):
    d.path(rot_rect_path(cx, cy, w, h, deg), f"Ring debris {i+1}",
           fill=VAL_C, opacity=45, stroke=NONE)

# --- three senior developers, already inside -------------------------------------
def dev(cx, cy, s, deg, label):
    # tiny falling figure: head, torso, flailing arms, trailing legs
    t = math.radians(deg); c, sn = math.cos(t), math.sin(t)
    def rot(px, py):
        return cx + px * c - py * sn, cy + px * sn + py * c
    d.shape("ellipse", f"{label} glow", x=cx - 14 * s, y=cy - 26 * s,
            width=34 * s, height=46 * s, fill=VIOLET, opacity=10,
            stroke=NONE)
    hx, hy = rot(0, -17 * s)
    d.shape("ellipse", f"{label} head", x=hx - 6 * s, y=hy - 6 * s,
            width=12 * s, height=12 * s, fill="#0E0818",
            stroke=VIOLET, strokeWidth=1.5)
    x1, y1 = rot(0, -8 * s); x2, y2 = rot(0, 9 * s)
    d.path(f"M{x1:.0f},{y1:.0f} L{x2:.0f},{y2:.0f}", f"{label} torso",
           fill=NONE, stroke="#0E0818", strokeWidth=7 * s, cap="round")
    for j, ((ax, ay), (bx, by)) in enumerate([
            ((-9 * s, -2 * s), (-15 * s, -9 * s)),
            ((9 * s, -2 * s), (16 * s, -7 * s)),
            ((-3 * s, 9 * s), (-8 * s, 17 * s)),
            ((3 * s, 9 * s), (9 * s, 15 * s))]):
        px, py = rot(ax, ay); qx, qy = rot(bx, by)
        d.path(f"M{px:.0f},{py:.0f} L{qx:.0f},{qy:.0f}",
               f"{label} limb {j+1}", fill=NONE, stroke="#0E0818",
               strokeWidth=4 * s, cap="round")

dev(392, 575, 1.0, -30, "Dev 1")
dev(600, 640, 0.85, 35, "Dev 2")
dev(505, 700, 0.7, -8, "Dev 3")

# faint scream-lines trailing the last dev in
d.path("M470,700 C460,695 452,686 448,676", "Dev3 trail 1", fill=NONE,
       stroke=VIOLET, strokeWidth=2, opacity=40, cap="round")
d.path("M540,706 C548,700 555,692 558,682", "Dev3 trail 2", fill=NONE,
       stroke=VIOLET, strokeWidth=2, opacity=40, cap="round")

# --- aphorism line + name + role ---------------------------------------------------
r = d.text("THE JSON APPEARED ENTIRELY LEGITIMATE", "Key line 1",
           x=500, y=762, size=22, font="Virelai Sans", color=KEY,
           justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "key1 tracking", ids=[r["id"]], tracking=100)
r = d.text("UNTIL IT WAS PARSED.", "Key line 2", x=500, y=795,
           size=22, font="Virelai Sans", color=KEY, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "key2 tracking", ids=[r["id"]], tracking=100)

d.text("VEXSYS ANTAGON", "Name", x=500, y=905, size=56,
       font="Virelai Sans", color=CREAM, justify="center")
r = d.text("THE CODE DOES NOT COMPILE BUT THE CHAOS IS OPERATIONAL",
           "Role", x=500, y=948, size=17, font="Virelai Sans",
           color=FAINT, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=110)

d.finish("aph-067-vexsys-antagon-V1R00")
