#!/usr/bin/env python3
"""Friendship Preamble — mascot portrait V1R00.
A slate clerk with a smile two sizes too warm, mid-keystroke on a floating
compose card: HI FRIEND, a sticker emoji, and the invoice already attached.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Friendship Preamble — Mascot Portrait", 1000, 1000)

INK = "#2A2028"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#11151B"}, {"offset": 1, "color": "#07090C"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#31404E"}, {"offset": 0.7, "color": "#1D2831"},
    {"offset": 1, "color": "#0F151B"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#222B33"}, {"offset": 1, "color": "#0F1417"}]}}
BODY_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#A9B6D4"}, {"offset": 0.72, "color": "#7E8CAA"},
    {"offset": 1, "color": "#55617E"}]}}
DESK_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3C4652"}, {"offset": 1, "color": "#21282E"}]}}
CARD_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#EFE6D0"}, {"offset": 1, "color": "#D8CCB0"}]}}
EMOJI_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F4D47C"}, {"offset": 0.7, "color": "#E2B354"},
    {"offset": 1, "color": "#B8862E"}]}}
WARM = "#E2C07C"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#5E7284", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#B8C8D8", strokeWidth=3, opacity=50)
for i, (x, y, w) in enumerate([(193,233,8),(801,230,7),(157,524,9),(837,544,8),
                               (247,766,7),(753,749,9),(133,393,6),(864,391,7),
                               (391,113,7),(613,110,8),(333,823,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#3C4A58", opacity=45, stroke=NONE)

# --- floor ----------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0B0E10",
       strokeWidth=4, opacity=70)

# --- the compose card, floating, tilted like good intentions -----------------------
cx, cy, ang = 668, 372, -4
d.path(rot_rect_path(cx + 10, cy + 14, 268, 236, ang), "Card shadow",
       fill="#06080A", opacity=45, stroke=NONE)
d.path(rot_rect_path(cx, cy, 268, 236, ang), "Email card",
       fill=CARD_GRAD, stroke=INK, strokeWidth=5, join="round")
# header bar built on the card's own frame so the tilt stays true
_t = math.radians(ang); _c, _s = math.cos(_t), math.sin(_t)
def _corner(dx, dy):
    return (cx + dx * _c - dy * _s, cy + dx * _s + dy * _c)
_tl = _corner(-134, -118); _tr = _corner(134, -118); _bl = _corner(-134, 118)
_ux = ((_tr[0] - _tl[0]) / 268, (_tr[1] - _tl[1]) / 268)
_uy = ((_bl[0] - _tl[0]) / 236, (_bl[1] - _tl[1]) / 236)
d.path("M%.1f,%.1f L%.1f,%.1f L%.1f,%.1f L%.1f,%.1f Z" % (
    _tl[0], _tl[1], _tr[0], _tr[1],
    _tr[0] + _uy[0] * 36, _tr[1] + _uy[1] * 36,
    _tl[0] + _uy[0] * 36, _tl[1] + _uy[1] * 36), "Card header",
    fill="#3A4656", stroke=INK, strokeWidth=4, join="round")
for i, c in enumerate(["#8E4A42", "#C9A24C", "#6E8468"]):
    px = _tl[0] + _ux[0] * (26 + i * 18) + _uy[0] * 18
    py = _tl[1] + _ux[1] * (26 + i * 18) + _uy[1] * 18
    d.shape("ellipse", f"Window dot {i+1}", x=px - 5, y=py - 5,
            width=10, height=10, fill=c, stroke=INK, strokeWidth=2)
# the greeting, warm type on the card
d.text("HI FRIEND", "Greeting", x=cx - 104, y=cy - 62, size=20,
       font="Virelai Sans", color="#4A3A30", justify="left")
d.text("HOW WAS THE WEEKEND", "Small talk", x=cx - 104, y=cy - 38,
       size=9, font="Virelai Sans", color="#8A7A64", justify="left")
# the emoji: a sticker face, applied with intent
ex, ey = cx - 60, cy + 34
d.shape("ellipse", "Emoji sticker edge", x=ex - 42, y=ey - 42, width=84,
        height=84, fill="#F8F2E2", stroke=NONE, opacity=90)
d.shape("ellipse", "Emoji", x=ex - 36, y=ey - 36, width=72, height=72,
        fill=EMOJI_GRAD, stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Emoji eye L", x=ex - 17, y=ey - 16, width=9, height=12,
        fill="#241A18", stroke=NONE)
d.shape("ellipse", "Emoji eye R", x=ex + 8, y=ey - 16, width=9, height=12,
        fill="#241A18", stroke=NONE)
d.path(f"M{ex-18},{ey+8} C{ex-8},{ey+22} {ex+8},{ey+22} {ex+18},{ey+8}",
       "Emoji smile", fill=NONE, stroke="#241A18", strokeWidth=4, cap="round")
# sticker corner lifting already
d.path(f"M{ex+30},{ey-38} C{ex+42},{ey-30} {ex+42},{ey-16} {ex+38},{ey-8}",
       "Sticker peel", fill=NONE, stroke="#F8F2E2", strokeWidth=3,
       opacity=80, cap="round")
# the send button, patient, already lit
d.shape("rectangle", "Send pill", x=cx - 104, y=cy + 66, width=74, height=30,
        fill="#6E8468", stroke=INK, strokeWidth=3, radius=14)
d.text("SEND", "Send label", x=cx - 67, y=cy + 87, size=11,
       font="Virelai Sans", color="#E8EFD8", justify="center")

# the warmth, adrift between composer and card
d.path("M486,276 C478,262 456,264 454,282 C452,298 472,310 486,320 "
       "C500,310 520,298 518,282 C516,264 494,262 486,276 Z",
       "Heart", fill={"gradient": {"kind": "radial", "stops": [
           {"offset": 0, "color": "#E8927C"}, {"offset": 1, "color": "#B05A48"}]}},
       stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Heart sheen", x=462, y=272, width=14, height=10,
        fill="#FFFFFF", opacity=40, stroke=NONE)
# two unread badges trailing the card — the ask, queueing
d.shape("ellipse", "Badge 1", x=810, y=240, width=18, height=18,
        fill="#8E4A42", stroke=INK, strokeWidth=2.5, opacity=85)
d.shape("ellipse", "Badge 2", x=836, y=270, width=12, height=12,
        fill="#8E4A42", stroke=INK, strokeWidth=2.5, opacity=65)

# the invoice, attached before the warmth could be answered
ax, ay = cx + 62, cy + 78
d.shape("ellipse", "Attach shadow", x=ax - 74, y=ay + 16, width=150, height=14,
        fill="#0A0E12", opacity=35, stroke=NONE)
d.shape("rectangle", "Attach chip", x=ax - 80, y=ay - 16, width=156,
        height=34, fill="#C4CCDA", stroke=INK, strokeWidth=3.5, radius=16)
# paperclip: one honest loop
d.path(f"M{ax-56},{ay+6} L{ax-56},{ay-8} C{ax-56},{ay-16} {ax-44},{ay-16} "
       f"{ax-44},{ay-8} L{ax-44},{ay+4} C{ax-44},{ay+10} {ax-52},{ay+10} "
       f"{ax-52},{ay+4} L{ax-52},{ay-6}", "Paperclip", fill=NONE,
       stroke="#4A5668", strokeWidth=3, cap="round")
d.text("INVOICE", "Attach label", x=ax - 34, y=ay + 7, size=11,
       font="Virelai Sans", color="#3A4656", justify="left")

# --- the mascot: warmth, rendered ------------------------------------------------------------------
d.shape("ellipse", "Body shadow", x=262, y=682, width=220, height=24,
        fill="#080606", opacity=55, stroke=NONE)
d.path("M384,352 C482,352 534,438 532,548 C530,642 472,700 384,700 "
       "C296,700 240,642 238,548 C236,438 286,352 384,352 Z",
       "Body", fill=BODY_GRAD, stroke=INK, strokeWidth=7)
d.shape("ellipse", "Belly light", x=306, y=530, width=160, height=140,
        fill="#D8E2F4", opacity=20, stroke=NONE)
d.path("M264,470 C250,540 258,616 294,664", "Flank shade", fill=NONE,
       stroke="#4A5670", strokeWidth=16, opacity=30, cap="round")
d.shape("ellipse", "Head sheen", x=296, y=376, width=180, height=58,
        fill="#FFFFFF", opacity=12, stroke=NONE)

# typing hands coming down to the keyboard
d.path("M462,545 C492,558 502,580 500,604", "Arm R", fill=NONE,
       stroke="#7E8CAA", strokeWidth=26, cap="round")
d.shape("ellipse", "Hand R", x=478, y=596, width=44, height=30,
        fill="#94A2C0", stroke=INK, strokeWidth=4)
d.path("M318,560 C304,576 300,592 306,608", "Arm L", fill=NONE,
       stroke="#7E8CAA", strokeWidth=24, cap="round")
d.shape("ellipse", "Hand L", x=286, y=598, width=42, height=30,
        fill="#94A2C0", stroke=INK, strokeWidth=4)

# the face: eyes bright, the smile wider than the situation
for i, cx2 in enumerate([346, 426]):
    d.shape("ellipse", f"Eye {i+1}", x=cx2 - 14, y=452, width=28, height=30,
            fill="#1E161C", stroke=NONE)
    d.shape("ellipse", f"Glint {i+1}", x=cx2 - 7, y=458, width=8, height=8,
            fill="#FFFFFF", opacity=90, stroke=NONE)
    d.shape("ellipse", f"Glint2 {i+1}", x=cx2 + 4, y=466, width=4, height=4,
            fill="#FFFFFF", opacity=60, stroke=NONE)
# grin: open crescent with a tooth line — professionally warm
d.path("M340,514 C366,548 408,548 434,514 C430,544 408,558 387,558 "
       "C364,558 344,544 340,514 Z", "Grin", fill="#3A2A30",
       stroke=INK, strokeWidth=5, join="round")
d.path("M352,522 C372,534 404,534 422,522", "Tooth line", fill=NONE,
       stroke="#E8DCC8", strokeWidth=6, cap="round", opacity=90)

# --- desk: the counter the warmth is conducted across -----------------------------------------------
d.shape("rectangle", "Desk top", x=210, y=636, width=580, height=30,
        fill=DESK_GRAD, stroke=INK, strokeWidth=5, radius=8)
d.shape("rectangle", "Desk front", x=228, y=666, width=544, height=40,
        fill={"gradient": {"kind": "linear", "stops": [
            {"offset": 0, "color": "#2C3540"}, {"offset": 1, "color": "#161C22"}]}},
        stroke=INK, strokeWidth=5, radius=6)

# the keyboard the greeting is typed on
d.path(rot_rect_path(392, 624, 180, 22, -2), "Keyboard",
       fill="#2C3540", stroke=INK, strokeWidth=3.5, join="round")
for i, y in enumerate([620, 628]):
    for j in range(6):
        d.path(f"M{330+j*22},{y} L{342+j*22},{y}", f"Key {i+1}-{j+1}",
               fill=NONE, stroke="#5A6878", strokeWidth=2, opacity=80)

# a mug left cold on the desk
d.shape("ellipse", "Mug shadow", x=250, y=630, width=60, height=10,
        fill="#0A0E12", opacity=40, stroke=NONE)
d.path("M254,576 L304,576 L300,628 C300,636 258,636 258,628 Z", "Mug",
       fill="#6E4A42", stroke=INK, strokeWidth=4, join="round")
d.path("M304,586 C320,586 320,606 302,608", "Mug handle", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.path("M270,560 C264,550 274,542 268,532", "Cold steam", fill=NONE,
       stroke="#B8C8D8", strokeWidth=3, opacity=30, cap="round")

# --- captions -------------------------------------------------------------------------
d.text("FRIENDSHIP PREAMBLE", "Name", x=500, y=930, size=54,
       font="Virelai Sans", color="#E4E9F2", justify="center")
r = d.text("TRANSACTIONAL WARMTH PROTOCOL", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#9AA8C0", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("300.friendship-preamble-V1R00")
