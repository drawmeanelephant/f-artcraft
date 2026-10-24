#!/usr/bin/env python3
"""LIM-0443 Proctor Paul — limerick plate V1R00. Keystrokes logged as a
bio: Paul sweeps red scanner beams over the keystroke log where one wide
gap — the pause — is flagged as vice, the keyboard keeps firing event
dots into the record, and the pace score insists he's learning too slow.
Navy surveillance palette, amber alerts. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("LIM-0443 Proctor Paul — Limerick Plate", 1000, 1000)

INK = "#332A33"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#0E1626"}, {"offset": 1, "color": "#060A14"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4A5C84"}, {"offset": 0.7, "color": "#32406A"},
    {"offset": 1, "color": "#1A2240"}]}}
PAUL = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E8D9C4"}, {"offset": 0.7, "color": "#C4A98C"},
    {"offset": 1, "color": "#9A7E62"}]}}
BOARD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3E4A70"}, {"offset": 1, "color": "#1E2746"}]}}
PANEL = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#141E32"}, {"offset": 1, "color": "#0C1220"}]}}
KEYCAP = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#9AA8CC"}, {"offset": 1, "color": "#5E6C96"}]}}
ICE = "#D8E0F4"
SOFT = "#8FA8D8"
RED = "#E85A4E"
AMBER = "#F0C878"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#6E84B4", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C9D4EE", strokeWidth=3, opacity=50)
for i, (x, y, w) in enumerate([(190, 220, 8), (790, 200, 7), (150, 480, 9),
                               (845, 560, 8), (220, 800, 7), (790, 780, 9),
                               (140, 340, 6), (860, 380, 7), (400, 110, 7),
                               (600, 105, 8)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#3E5078", opacity=45, stroke=NONE)
# surveillance glow behind the log
d.shape("ellipse", "Log glow", x=160, y=170, width=330, height=250,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#7E94D4", "opacity": 0.14},
            {"offset": 1, "color": "#7E94D4", "opacity": 0}]}},
        stroke=NONE)

# --- keystroke log panel, upper left -------------------------------------------
d.shape("rectangle", "Log panel", x=150, y=185, width=300, height=205,
        radius=10, fill=PANEL, stroke="#4A5E8E", strokeWidth=4)
d.shape("rectangle", "Log header", x=150, y=185, width=300, height=28,
        radius=10, fill="#1E2A44", stroke="#4A5E8E", strokeWidth=3)
for i, dx in enumerate([164, 178, 192]):
    d.shape("ellipse", f"Header dot {i+1}", x=dx, y=194, width=8, height=8,
            fill="#3E5078", stroke=NONE)
d.text("KEYSTROKE LOG", "Log title", x=300, y=205, size=12,
       font="Virelai Sans", color=SOFT, justify="center")
# logged rows: little keystroke ticks; row 3 has THE PAUSE — a wide gap
ROWS = [
    [(176, 232, 26), (208, 232, 20), (234, 232, 30), (270, 232, 22),
     (298, 232, 26), (330, 232, 18), (354, 232, 24), (384, 232, 20),
     (410, 232, 24)],
    [(176, 262, 22), (204, 262, 28), (238, 262, 20), (264, 262, 26),
     (296, 262, 22), (324, 262, 30), (360, 262, 20), (386, 262, 26)],
    [(176, 292, 24), (206, 292, 20), (310, 292, 26), (342, 292, 20),
     (368, 292, 28), (402, 292, 22)],
    [(176, 322, 28), (210, 322, 22), (238, 322, 26), (270, 322, 20),
     (296, 322, 24), (326, 322, 28), (360, 322, 20), (386, 322, 26),
     (418, 322, 18)],
    [(176, 352, 20), (202, 352, 26), (234, 352, 22), (262, 352, 28),
     (296, 352, 20), (322, 352, 24), (352, 352, 22), (380, 352, 26),
     (412, 352, 20)],
]
for r_i, row in enumerate(ROWS):
    for k_i, (kx, ky, kw) in enumerate(row):
        d.shape("rectangle", f"Tick {r_i+1}-{k_i+1}", x=kx, y=ky,
                width=kw, height=10, radius=2, fill="#5E6C96",
                opacity=80, stroke=NONE)
# the pause: bracketed gap in row 3, flagged as vice
d.path("M238,286 L238,310 M238,310 L300,310 M300,310 L300,286",
       "Pause bracket", fill=NONE, stroke=RED, strokeWidth=3,
       cap="round", join="round")
d.path("M254,282 L254,266 L282,272 Z", "Pause flag", fill=RED,
       stroke=NONE)
d.text("PAUSE", "Pause label", x=269, y=342, size=11,
       font="Virelai Sans", color=RED, justify="center")
d.text("NOTED AS VICE", "Vice note", x=356, y=380, size=10,
       font="Virelai Sans", color="#C98A9A", justify="center")

# --- the reread page: the same line twice is its own offense -------------------------
book_ids = []
def book_add(res):
    if res and res.get("id"):
        book_ids.append(res["id"])
book_add(d.path("M330,472 L394,460 L394,516 L330,528 Z", "Book page L",
                fill="#EDE6D4", stroke=INK, strokeWidth=3, join="round"))
book_add(d.path("M394,460 L458,472 L458,528 L394,516 Z", "Book page R",
                fill="#DCD2B8", stroke=INK, strokeWidth=3, join="round"))
for i, lw in enumerate([46, 40]):
    book_add(d.shape("rectangle", f"Page line L{i+1}", x=340,
                     y=482 + i * 14, width=lw, height=5, radius=2,
                     fill="#6E5F4A", opacity=70, stroke=NONE))
# the same line, read twice — struck twice in red
book_add(d.path("M404,478 L448,486 M404,492 L448,500", "Reread strikes",
               fill=NONE, stroke=RED, strokeWidth=3, cap="round"))
book_add(d.path("M452,494 L452,478 L476,483 Z", "Reread flag", fill=RED,
                stroke=NONE))
if book_ids:
    d.call("transform", {"ids": book_ids, "rotate": -6,
                         "origin": [394, 494]}, "tilt book")
d.text("REREAD", "Reread label", x=398, y=560, size=11,
       font="Virelai Sans", color=RED, justify="center")

# --- pace score tile, upper right ----------------------------------------------
d.shape("rectangle", "Score tile", x=615, y=195, width=185, height=112,
        radius=10, fill=PANEL, stroke="#4A5E8E", strokeWidth=4)
d.text("PACE SCORE", "Score label", x=707, y=216, size=12,
       font="Virelai Sans", color=SOFT, justify="center")
# gauge: arc with needle parked low
d.path("M650,284 A58,58 0 0 1 766,284", "Gauge arc", fill=NONE,
       stroke="#3E5078", strokeWidth=7, cap="round")
d.path("M650,284 A58,58 0 0 1 682,240", "Gauge low", fill=NONE,
       stroke=RED, strokeWidth=7, cap="round")
d.path("M708,284 L678,252", "Needle", fill=NONE, stroke=ICE,
       strokeWidth=5, cap="round")
d.shape("ellipse", "Needle hub", x=701, y=277, width=14, height=14,
        fill=ICE, stroke=INK, strokeWidth=2)
d.text("TOO SLOW", "Score readout", x=707, y=300, size=13,
       font="Virelai Sans", color=AMBER, justify="center")

# --- floor ----------------------------------------------------------------------
d.shape("ellipse", "Floor", x=170, y=700, width=660, height=120,
        fill="#1C2544", opacity=90, stroke=NONE)
d.shape("ellipse", "Keyboard shadow", x=180, y=748, width=330, height=26,
        fill="#060A16", opacity=55, stroke=NONE)
d.shape("ellipse", "Paul shadow", x=560, y=800, width=210, height=28,
        fill="#060A16", opacity=55, stroke=NONE)

# --- the keyboard, still firing --------------------------------------------------
kb_ids = []
def kb_add(res):
    if res and res.get("id"):
        kb_ids.append(res["id"])

kb_add(d.path("M190,660 L500,660 L512,742 L178,742 Z", "Keyboard base",
              fill=BOARD, stroke=INK, strokeWidth=5, join="round"))
for r_i, (ky, kn, kw) in enumerate([(672, 8, 40), (700, 7, 44)]):
    total = kn * kw + (kn - 1) * 8
    kx = 345 - total / 2
    for k_i in range(kn):
        kb_add(d.shape("rectangle", f"Key {r_i+1}-{k_i+1}", x=kx, y=ky,
                       width=kw, height=20, radius=4, fill=KEYCAP,
                       stroke=INK, strokeWidth=2))
        kx += kw + 8
kb_add(d.shape("rectangle", "Spacebar", x=270, y=728, width=150,
               height=12, radius=4, fill=KEYCAP, stroke=INK,
               strokeWidth=2))
# the freshly pressed key, lit with a tell
d.shape("ellipse", "Key glow", x=380, y=692, width=56, height=40,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#8FB4E8", "opacity": 0.5},
            {"offset": 1, "color": "#8FB4E8", "opacity": 0}]}},
        stroke=NONE)
kb_add(d.shape("rectangle", "Pressed key", x=392, y=700, width=44,
               height=20, radius=4, fill="#C9D4EE", stroke=INK,
               strokeWidth=2))
if kb_ids:
    d.call("transform", {"ids": kb_ids, "rotate": -3,
                         "origin": [345, 700]}, "tilt keyboard")

# --- event dots: every keystroke flies into the log -------------------------------
for i, (ex, ey, ew, op) in enumerate([(356, 620, 9, 85), (330, 566, 8, 75),
                                      (312, 512, 8, 65), (300, 458, 7, 55),
                                      (296, 408, 7, 45)]):
    d.shape("ellipse", f"Event dot {i+1}", x=ex, y=ey, width=ew,
            height=ew, fill="#8FB4E8", opacity=op, stroke=NONE)
d.path("M362,628 C330,540 302,460 298,398", "Event trail", fill=NONE,
       stroke="#8FB4E8", strokeWidth=2.5, dash=[2, 9], opacity=50,
       cap="round")

# --- Paul: capsule body, visor, scanner beams, clipboard ---------------------------
# body
d.path("M580,540 C580,468 608,436 666,436 C724,436 752,468 752,540 "
       "L752,706 C752,772 722,802 666,802 C610,802 580,772 580,706 Z",
       "Paul body", fill=PAUL, stroke=INK, strokeWidth=5, join="round")
d.path("M598,560 C598,500 612,472 640,458", "Body sheen", fill=NONE,
       stroke="#F4E8D4", strokeWidth=8, opacity=30, cap="round")
# brown monitor cap
d.path("M592,470 C600,428 732,428 740,470 L740,482 L592,482 Z",
       "Paul cap", fill={"gradient": {"kind": "linear", "stops": [
           {"offset": 0, "color": "#5E4A56"},
           {"offset": 1, "color": "#382C3A"}]}},
       stroke=INK, strokeWidth=4, join="round")
d.shape("ellipse", "Cap nub", x=658, y=424, width=16, height=10,
        fill="#5E4A56", stroke=INK, strokeWidth=2)
# stern brows over the visor
d.path("M612,500 L644,508", "Brow L", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
d.path("M720,500 L688,508", "Brow R", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
# dark visor with the red scan slit
d.path("M596,516 L736,516 L726,572 L606,572 Z", "Paul visor",
       fill={"gradient": {"kind": "linear", "stops": [
           {"offset": 0, "color": "#46344E"},
           {"offset": 1, "color": "#241C2E"}]}},
       stroke=INK, strokeWidth=4, join="round")
d.path("M628,534 L666,540 L704,534", "Scan slit", fill=NONE,
       stroke=RED, strokeWidth=6, cap="round", join="round")
d.path("M640,548 L666,552 L692,548", "Scan slit 2", fill=NONE,
       stroke=RED, strokeWidth=3, opacity=70, cap="round")
# cheeks flushed with alertness
d.shape("ellipse", "Cheek L", x=606, y=580, width=20, height=12,
        fill="#C98A9A", opacity=45, stroke=NONE)
d.shape("ellipse", "Cheek R", x=706, y=580, width=20, height=12,
        fill="#C98A9A", opacity=45, stroke=NONE)
# scanner beams lancing left at the log + keyboard
d.path("M596,532 L468,330", "Beam 1", fill=NONE, stroke=RED,
       strokeWidth=4, opacity=80, cap="round")
d.path("M596,548 L470,352", "Beam 2", fill=NONE, stroke=RED,
       strokeWidth=3, opacity=60, cap="round")
d.shape("ellipse", "Scan spot", x=448, y=318, width=44, height=56,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#E85A4E", "opacity": 0.35},
            {"offset": 1, "color": "#E85A4E", "opacity": 0}]}},
        stroke=NONE)
# clipboard: the bio made of keystrokes
clip_ids = []
def clip_add(res):
    if res and res.get("id"):
        clip_ids.append(res["id"])
clip_add(d.shape("rectangle", "Clipboard", x=628, y=612, width=96,
                 height=120, radius=6, fill={"gradient": {"kind": "linear",
                 "stops": [{"offset": 0, "color": "#EDE6D4"},
                           {"offset": 1, "color": "#C4B898"}]}},
                 stroke=INK, strokeWidth=4))
clip_add(d.shape("rectangle", "Clip top", x=654, y=604, width=44,
                 height=16, radius=6, fill="#8A7E68", stroke=INK,
                 strokeWidth=3))
for i, lw in enumerate([64, 56, 62, 40]):
    clip_add(d.shape("rectangle", f"Clip line {i+1}", x=640,
                     y=636 + i * 18, width=lw, height=6, radius=2,
                     fill="#6E5F4A", opacity=75, stroke=NONE))
clip_add(d.path("M640,706 L676,706", "Clip strike", fill=NONE,
                stroke=RED, strokeWidth=4, cap="round"))
clip_add(d.text("!", "Clip bang", x=706, y=712, size=18,
                font="Virelai Sans", color=RED, justify="center"))
if clip_ids:
    d.call("transform", {"ids": clip_ids, "rotate": 4,
                         "origin": [676, 672]}, "tilt clipboard")
# arms cradling the clipboard
d.path("M586,640 C610,664 630,676 652,682", "Arm L", fill=NONE,
       stroke="#C4A98C", strokeWidth=18, cap="round")
d.path("M748,646 C740,674 730,688 716,696", "Arm R", fill=NONE,
       stroke="#C4A98C", strokeWidth=18, cap="round")
# stub legs
d.path("M630,802 L628,826 M700,802 L702,826", "Legs", fill=NONE,
       stroke="#9A7E62", strokeWidth=14, cap="round")
d.shape("ellipse", "Foot L", x=614, y=824, width=30, height=12,
        fill="#5E4A56", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Foot R", x=688, y=824, width=30, height=12,
        fill="#5E4A56", stroke=INK, strokeWidth=3)

# --- name + key line + role ------------------------------------------------------
r = d.text("THE PAUSE IS A SIGNAL OF WOE", "Key line", x=500, y=899,
           size=22, font="Virelai Sans", color=SOFT, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "key tracking", ids=[r["id"]], tracking=150)
d.text("PROCTOR PAUL", "Name", x=500, y=945, size=56,
       font="Virelai Sans", color=ICE, justify="center")
r = d.text("KEYSTROKES LOGGED AS BIO", "Role", x=500, y=977,
           size=19, font="Virelai Sans", color="#7484AC",
           justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=170)

d.finish("lim-0443-proctor-paul-V1R00")
