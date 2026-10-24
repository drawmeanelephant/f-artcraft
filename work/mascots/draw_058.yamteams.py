#!/usr/bin/env python3
"""YamTeams(tm) ProLink Enterprise Suite 365(tm) — mascot portrait V1R00.
Compliance parasite of the forced Yammer/Teams/LinkedIn merger, dead-eyed
behind a headset amid duplicated communication surfaces and ghost invites,
persistent sidebar contact: Brad. 1000x1000.
Gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("YamTeams ProLink — Mascot Portrait", 1000, 1000)

INK = "#221C24"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#0E1220"}, {"offset": 1, "color": "#080A12"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#3E4A70"}, {"offset": 0.7, "color": "#28304E"},
    {"offset": 1, "color": "#171B2E"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#252C46"}, {"offset": 1, "color": "#12141F"}]}}
WIN_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#222A44"}, {"offset": 1, "color": "#151A2C"}]}}
BODY_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#CCC8E0"}, {"offset": 0.7, "color": "#9C94B8"},
    {"offset": 1, "color": "#6E668C"}]}}
PURPLE = "#7B83EB"
BLUE = "#5FA8E0"
DEEPBLUE = "#4E9BD4"
AMBER = "#E8B86A"
RED = "#D0485E"
GHOST = "#AAB8E8"

def rot_pt(cx, cy, x, y, deg):
    a = math.radians(deg); c, s = math.cos(a), math.sin(a)
    return (cx + (x - cx) * c - (y - cy) * s,
            cy + (x - cx) * s + (y - cy) * c)

def window(cx, cy, w, h, deg, label, op=100, ghost=False):
    """A communication surface: frame + titlebar + dots + sidebar + chat lines."""
    fill_op = op * 0.55 if ghost else op
    d.path(rot_rect_path(cx, cy, w, h, deg), f"{label} frame",
           fill=WIN_GRAD, stroke=INK, strokeWidth=5, join="round",
           opacity=fill_op)
    # titlebar
    bx, by = rot_pt(cx, cy, cx, cy - h / 2 + 15, deg)
    d.path(rot_rect_path(bx, by, w - 14, 22, deg), f"{label} bar",
           fill="#2E3656", opacity=op, stroke=NONE)
    for i in range(3):
        px, py = rot_pt(cx, cy, cx - w / 2 + 22 + i * 16, cy - h / 2 + 15, deg)
        d.shape("ellipse", f"{label} dot {i+1}", x=px - 4, y=py - 4,
                width=8, height=8, fill="#56648E", opacity=op, stroke=NONE)
    # sidebar strip (where Brad lives)
    sx, sy = rot_pt(cx, cy, cx - w / 2 + 22, cy + 12, deg)
    d.path(rot_rect_path(sx, sy, 30, h - 52, deg), f"{label} sidebar",
           fill="#2A3250", opacity=op, stroke=NONE)
    # chat lines
    for i in range(3):
        lx, ly = rot_pt(cx, cy, cx + w / 2 - 58,
                        cy - h / 2 + 52 + i * 26, deg)
        d.path(rot_rect_path(lx, ly, w - 116 - i * 22, 9, deg),
               f"{label} msg {i+1}", fill="#8E9AC4", opacity=op * 0.6,
               stroke=NONE)
        ax, ay = rot_pt(cx, cy, cx - w / 2 + 58,
                        cy - h / 2 + 52 + i * 26, deg)
        d.shape("ellipse", f"{label} av {i+1}", x=ax - 7, y=ay - 7,
                width=14, height=14, fill="#6A76A8", opacity=op,
                stroke=NONE)

# --- backdrop + plate ------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#7E8CC8", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C4D0F0", strokeWidth=3, opacity=40)
for i, (x, y, w) in enumerate([(186,236,8),(806,240,7),(148,516,9),(848,546,8),
                               (260,764,7),(742,760,9),(136,392,6),(862,404,7),
                               (388,112,7),(614,110,8),(344,818,6),(660,826,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#39456C", opacity=50, stroke=NONE)

# --- floor -----------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0E1020",
       strokeWidth=4, opacity=70)

# --- duplicated communication surfaces ----------------------------------------------
window(268, 352, 300, 204, -7, "W1 ghost", op=42, ghost=True)
window(246, 330, 300, 204, -7, "W1")
window(662, 300, 262, 182, 6, "W2")
window(478, 168, 236, 138, -3, "W3")
# W1 titlebar text + resurrected thread stamp
t = d.text("GENERAL", "W1 title", x=246, y=241, size=11,
           font="Virelai Sans", color="#AEB8DC", justify="center")
if t and t.get("id"):
    d.cmd("object.rotate", "w1 title tilt", ids=[t["id"]], angle=7,
          origin=[246, 241])
d.path(rot_rect_path(258, 368, 128, 30, -7), "Resolved stamp",
       fill=NONE, stroke=RED, strokeWidth=3, opacity=60)
t = d.text("RESOLVED", "Resolved text", x=258, y=376, size=13,
           font="Virelai Sans", color=RED, justify="center")
if t and t.get("id"):
    d.cmd("object.rotate", "resolved tilt", ids=[t["id"]], angle=7,
          origin=[258, 376])
    d.call("run_command", {"command": "object.setProps",
           "params": {"id": t["id"], "opacity": 60}}, "resolved ghosting")
# W2: the resurrected thread that would not die
t = d.text("RE: RE: RE:", "W2 thread", x=662, y=296, size=13,
           font="Virelai Sans", color="#9EB4E8", justify="center")
if t and t.get("id"):
    d.cmd("object.rotate", "w2 text tilt", ids=[t["id"]], angle=-6,
          origin=[662, 296])
t = d.text("THREADS", "W3 title", x=478, y=134, size=10,
           font="Virelai Sans", color="#AEB8DC", justify="center")
if t and t.get("id"):
    d.cmd("object.rotate", "w3 title tilt", ids=[t["id"]], angle=3,
          origin=[478, 134])

# --- ghost invites drifting through ----------------------------------------------------
for i, (cx, cy, deg) in enumerate([(178, 496, -10), (772, 172, 8)]):
    d.path(rot_rect_path(cx, cy, 132, 86, deg), f"Invite {i+1}",
           fill=GHOST, stroke=GHOST, strokeWidth=2, join="round",
           opacity=34)
    hx, hy = rot_pt(cx, cy, cx, cy - 24, deg)
    d.path(rot_rect_path(hx, hy, 116, 16, deg), f"Invite {i+1} bar",
           fill=GHOST, opacity=40, stroke=NONE)
    t = d.text("INVITE", f"Invite {i+1} text", x=cx, y=cy + 8, size=11,
               font="Virelai Sans", color=GHOST, justify="center")
    if t and t.get("id"):
        d.cmd("object.rotate", f"invite {i+1} tilt", ids=[t["id"]],
              angle=-deg, origin=[cx, cy])
        d.call("run_command", {"command": "object.setProps",
               "params": {"id": t["id"], "opacity": 55}},
               f"invite {i+1} text op")

# --- Brad: the persistent sidebar contact ----------------------------------------------
d.path(rot_rect_path(792, 488, 138, 224, 3), "Brad card",
       fill="#242C48", stroke=INK, strokeWidth=5, join="round")
ax, ay = rot_pt(792, 488, 792, 428, 3)
d.shape("ellipse", "Brad avatar", x=ax - 26, y=ay - 26, width=52, height=52,
        fill="#4A5480", stroke="#8E9AC4", strokeWidth=3)
d.shape("ellipse", "Brad face", x=ax - 12, y=ay - 10, width=24, height=20,
        fill="#8E9AC4", opacity=60, stroke=NONE)
tx, ty = rot_pt(792, 488, 792, 470, 3)
t = d.text("BRAD", "Brad name", x=tx, y=ty, size=16,
           font="Virelai Sans", color="#DCE2F4", justify="center")
if t and t.get("id"):
    d.cmd("object.rotate", "brad tilt", ids=[t["id"]], angle=-3,
          origin=[tx, ty])
for j, (ly, w) in enumerate([(494, 92), (514, 92)]):
    lx, lyy = rot_pt(792, 488, 792, ly, 3)
    d.path(rot_rect_path(lx, lyy, w, 8, 3), f"Brad sub {j+1}",
           fill="#8E9AC4", opacity=55, stroke=NONE)
t = d.text("SUGGESTED", "Brad sub t", x=tx, y=ty + 26, size=8,
           font="Virelai Sans", color="#8E9AC4", justify="center")
t2 = d.text("CONNECTION", "Brad sub t2", x=tx, y=ty + 44, size=8,
            font="Virelai Sans", color="#8E9AC4", justify="center")
for tt in (t, t2):
    if tt and tt.get("id"):
        d.cmd("object.rotate", "brad sub tilt", ids=[tt["id"]], angle=-3,
              origin=[tx, ty])
bx, by = rot_pt(792, 488, 792, 566, 3)
d.path(rot_rect_path(bx, by, 96, 26, 3), "Connect btn",
       fill=PURPLE, stroke=NONE, join="round")
t = d.text("CONNECT", "Connect label", x=bx, y=by + 5, size=10,
           font="Virelai Sans", color="#F0F2FC", justify="center")
if t and t.get("id"):
    d.cmd("object.rotate", "connect tilt", ids=[t["id"]], angle=-3,
          origin=[bx, by])

# --- YamTeams: dead-eyed parasite with a headset -----------------------------------
d.shape("ellipse", "YT shadow", x=372, y=686, width=230, height=22,
        fill="#06070E", opacity=55, stroke=NONE)
# headset band behind the head
d.path("M414,462 C428,406 532,406 548,462", "Headset band", fill=NONE,
       stroke=INK, strokeWidth=12, cap="round")
d.path("M414,462 C428,406 532,406 548,462", "Headset band hi", fill=NONE,
       stroke="#4A5480", strokeWidth=7, cap="round")
# body
d.path("M480,445 C556,445 594,512 594,582 C594,656 546,698 480,698 "
       "C414,698 366,656 366,582 C366,512 404,445 480,445 Z",
       "YT body", fill=BODY_GRAD, stroke=INK, strokeWidth=6)
d.shape("ellipse", "Body hi", x=412, y=486, width=96, height=50,
        fill="#FFFFFF", opacity=12, stroke=NONE)
# earcups + mic boom
d.shape("ellipse", "Cup L", x=398, y=452, width=30, height=44,
        fill="#3A4266", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Cup R", x=532, y=452, width=30, height=44,
        fill="#3A4266", stroke=INK, strokeWidth=4)
d.path("M552,492 C570,512 574,538 562,556", "Mic boom", fill=NONE,
       stroke=INK, strokeWidth=7, cap="round")
d.shape("ellipse", "Mic", x=552, y=548, width=20, height=16,
        fill="#4A5480", stroke=INK, strokeWidth=3)
# the eyes of the compliance parasite: half-lidded, unimpressed, online
d.shape("ellipse", "Eye L", x=424, y=502, width=34, height=32,
        fill="#2A2030", stroke=NONE)
d.shape("ellipse", "Eye R", x=508, y=502, width=34, height=32,
        fill="#2A2030", stroke=NONE)
d.path("M422,504 L460,504 M506,504 L544,504", "Lids", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.shape("ellipse", "Glint L", x=430, y=512, width=7, height=7,
        fill=BLUE, opacity=80, stroke=NONE)
d.shape("ellipse", "Glint R", x=514, y=512, width=7, height=7,
        fill=BLUE, opacity=80, stroke=NONE)
# the fixed customer-service smile
d.path("M438,568 C468,586 506,586 534,566", "Smile", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
d.shape("ellipse", "Cheek L", x=412, y=546, width=24, height=12,
        fill="#8A7ED0", opacity=40, stroke=NONE)
d.shape("ellipse", "Cheek R", x=528, y=546, width=24, height=12,
        fill="#8A7ED0", opacity=40, stroke=NONE)
# feet
d.shape("ellipse", "Foot L", x=424, y=688, width=40, height=18,
        fill="#6E668C", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Foot R", x=500, y=688, width=40, height=18,
        fill="#6E668C", stroke=INK, strokeWidth=3)
# lanyard: the forced merger worn as three fused badges
d.path("M448,632 L480,672 M512,632 L480,672", "Lanyard", fill=NONE,
       stroke="#5A5478", strokeWidth=5, cap="round")
for i, (bx, by, deg, col, glyph) in enumerate([
        (454, 680, -12, BLUE, "Y"), (482, 684, 0, PURPLE, "T"),
        (510, 680, 12, DEEPBLUE, "IN")]):
    d.path(rot_rect_path(bx, by, 36, 26, deg), f"Badge {i+1}",
           fill=col, stroke=INK, strokeWidth=3, join="round")
    t = d.text(glyph, f"Badge glyph {i+1}", x=bx, y=by + 7, size=13,
               font="Virelai Sans", color="#F4F6FC", justify="center")
    if t and t.get("id"):
        d.cmd("object.rotate", f"badge {i+1} tilt", ids=[t["id"]],
              angle=-deg, origin=[bx, by])

# --- notification bell: always at least 99+ ------------------------------------------
d.shape("ellipse", "Bell", x=576, y=352, width=30, height=32,
        fill="#3E4668", stroke=INK, strokeWidth=4)
d.path("M591,384 L591,392", "Bell clapper", fill=NONE, stroke=INK,
       strokeWidth=4, cap="round")
d.shape("ellipse", "Bell badge", x=598, y=342, width=34, height=26,
        fill=RED, stroke=INK, strokeWidth=3)
d.text("99+", "Bell count", x=615, y=360, size=12,
       font="Source Sans 3", color="#FCF0F2", justify="center")

# --- stray notification toasts ----------------------------------------------------------
for i, (cx, cy, deg) in enumerate([(300, 560, -6), (640, 520, 5)]):
    d.path(rot_rect_path(cx, cy, 96, 30, deg), f"Toast {i+1}",
           fill="#3A4468", stroke=INK, strokeWidth=3, join="round",
           opacity=85)
    d.shape("ellipse", f"Toast dot {i+1}", x=cx - 36, y=cy - 5,
            width=10, height=10, fill=RED, stroke=NONE)

# --- captions ----------------------------------------------------------------------
# Virelai Sans has no digits or trademark glyphs: "365" and both "TM" marks
# fall back to Source Sans 3 via byte ranges.
n = d.text("YAMTEAMS™ PROLINK ENTERPRISE SUITE 365™", "Name",
           x=500, y=930, size=31, font="Virelai Sans", color="#DCE4F8",
           justify="center")
if n and n.get("id"):
    for s_, e_ in [(8, 9), (35, 38), (38, 39)]:
        d.cmd("text.setStyle", "name fallback", ids=[n["id"]],
              start=s_, end=e_, font="Source Sans 3")
r = d.text("COMPLIANCE PARASITE", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#A8B4E0", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("058.yamteams-V1R00")
