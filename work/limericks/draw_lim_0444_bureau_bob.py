#!/usr/bin/env python3
"""LIM-0444 Bureau Bob — limerick plate V1R00. The system has no record:
Bob raises a queue ticket that leads nowhere, the NOW SERVING board reads
all zeros, the appeal portal is down for good, the helpbot wears a clown
nose, and the statute book is weighed against a shoe. Institutional
green-slate, manila folder, red tape. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("LIM-0444 Bureau Bob — Limerick Plate", 1000, 1000)

INK = "#242A26"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#101A18"}, {"offset": 1, "color": "#060B0A"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#47605A"}, {"offset": 0.7, "color": "#2C423E"},
    {"offset": 1, "color": "#141F1E"}]}}
MANILA = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#EED9A8"}, {"offset": 0.6, "color": "#D4B87E"},
    {"offset": 1, "color": "#A8895A"}]}}
BODY = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#6E7E92"}, {"offset": 0.7, "color": "#46536A"},
    {"offset": 1, "color": "#2A3244"}]}}
SCREEN_OFF = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3A4444"}, {"offset": 1, "color": "#1E2626"}]}}
ICE = "#E4EAE2"
SOFT = "#9FB8AE"
RED = "#D8574A"
AMBER = "#E8C878"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#7EA8A0", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8E4DC", strokeWidth=3, opacity=50)
for i, (x, y, w) in enumerate([(200, 200, 8), (800, 210, 7), (150, 500, 9),
                               (845, 540, 8), (230, 790, 7), (780, 770, 9),
                               (145, 360, 6), (858, 370, 7), (390, 105, 7),
                               (610, 108, 8)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#3E5650", opacity=45, stroke=NONE)

# --- NOW SERVING board, hung high left ------------------------------------------
d.path("M260,150 L270,196 M420,150 L410,196", "Board wires", fill=NONE,
       stroke="#3E5650", strokeWidth=3, opacity=80)
d.shape("rectangle", "Serving board", x=222, y=196, width=240, height=86,
        radius=8, fill="#141F1E", stroke="#5E7A72", strokeWidth=4)
d.text("NOW SERVING", "Serving label", x=342, y=222, size=13,
       font="Virelai Sans", color=SOFT, justify="center")
# three digit cells, all zeros — the system has no record
for i in range(3):
    d.shape("rectangle", f"Digit cell {i+1}", x=262 + i * 58, y=238,
            width=44, height=32, radius=4, fill="#0A1210",
            stroke="#3E5650", strokeWidth=2)
    d.text("0", f"Zero {i+1}", x=284 + i * 58, y=263, size=22,
           font="Source Sans 3", color="#5E7A72", justify="center")

# --- appeal portal terminal, left, down for good ----------------------------------
term_ids = []
def term_add(res):
    if res and res.get("id"):
        term_ids.append(res["id"])
term_add(d.path("M268,470 L268,560", "Terminal pole", fill=NONE,
                stroke=INK, strokeWidth=10, cap="round"))
term_add(d.path("M240,560 L296,560 L306,578 L230,578 Z", "Terminal foot",
                fill="#2A3432", stroke=INK, strokeWidth=3, join="round"))
term_add(d.shape("rectangle", "Terminal", x=164, y=330, width=208,
                 height=142, radius=8, fill="#2A3432", stroke=INK,
                 strokeWidth=5))
term_add(d.shape("rectangle", "Terminal screen", x=178, y=344, width=180,
                 height=114, radius=4, fill=SCREEN_OFF, stroke=NONE))
term_add(d.text("APPEAL PORTAL", "Portal label", x=268, y=372, size=12,
                font="Virelai Sans", color="#7A9088", justify="center"))
term_add(d.text("DOWN", "Portal down", x=268, y=412, size=30,
                font="Virelai Sans", color=RED, justify="center"))
term_add(d.path("M300,432 L336,432", "Portal slash", fill=NONE,
                stroke=RED, strokeWidth=4, cap="round", opacity=70))
# cobwebs in the corner — nobody home
term_add(d.path("M178,344 C196,350 208,362 214,378", "Cobweb 1",
                fill=NONE, stroke="#7A9088", strokeWidth=1.5, opacity=45))
term_add(d.path("M178,344 C200,346 218,356 230,372", "Cobweb 2",
                fill=NONE, stroke="#7A9088", strokeWidth=1.5, opacity=35))
if term_ids:
    d.call("transform", {"ids": term_ids, "rotate": -4,
                         "origin": [268, 450]}, "tilt terminal")

# --- helpbot chat window, right — the clown ---------------------------------------
chat_ids = []
def chat_add(res):
    if res and res.get("id"):
        chat_ids.append(res["id"])
chat_add(d.shape("rectangle", "Chat window", x=640, y=318, width=190,
                 height=160, radius=12, fill="#141F1E",
                 stroke="#5E7A72", strokeWidth=4))
chat_add(d.shape("rectangle", "Chat header", x=640, y=318, width=190,
                 height=26, radius=12, fill="#1E2E2A", stroke="#5E7A72",
                 strokeWidth=3))
chat_add(d.text("HELPBOT", "Chat title", x=735, y=337, size=12,
                font="Virelai Sans", color=SOFT, justify="center"))
# clown face in the reply bubble
chat_add(d.shape("ellipse", "Clown face", x=688, y=356, width=66,
                 height=62, fill="#EDE6D4", stroke=INK, strokeWidth=3))
# rainbow tufts
chat_add(d.shape("ellipse", "Tuft L", x=678, y=372, width=14, height=20,
                 fill=RED, opacity=85, stroke=NONE))
chat_add(d.shape("ellipse", "Tuft R", x=750, y=372, width=14, height=20,
                 fill=RED, opacity=85, stroke=NONE))
# eyes squeezed shut, painted grin, red nose
chat_add(d.path("M702,384 q5,-5 10,0", "Clown eye L", fill=NONE,
                stroke=INK, strokeWidth=3, cap="round"))
chat_add(d.path("M732,384 q5,-5 10,0", "Clown eye R", fill=NONE,
                stroke=INK, strokeWidth=3, cap="round"))
chat_add(d.shape("ellipse", "Clown nose", x=715, y=390, width=14,
                 height=14, fill=RED, stroke=INK, strokeWidth=2))
chat_add(d.path("M706,408 Q722,420 738,408", "Painted grin", fill=NONE,
                stroke=INK, strokeWidth=3.5, cap="round"))
# ruffle collar
chat_add(d.path("M694,420 l8,10 l8,-10 l8,10 l8,-10 l8,10 l8,-10",
                "Ruffle", fill=NONE, stroke="#7EA8A0", strokeWidth=3,
                join="round"))
chat_add(d.text("HOW CAN I HELP?", "Chat bubble text", x=735, y=462,
                size=11, font="Virelai Sans", color="#7A9088",
                justify="center"))
if chat_ids:
    d.call("transform", {"ids": chat_ids, "rotate": 5,
                         "origin": [735, 398]}, "tilt chat")

# --- floor ----------------------------------------------------------------------
d.shape("ellipse", "Floor", x=240, y=700, width=560, height=120,
        fill="#1E2E2A", opacity=85, stroke=NONE)

# --- the statute, weighed against a shoe ------------------------------------------
d.shape("ellipse", "Scale glow", x=140, y=600, width=300, height=160,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#8FB8AC", "opacity": 0.16},
            {"offset": 1, "color": "#8FB8AC", "opacity": 0}]}},
        stroke=NONE)
d.shape("ellipse", "Scale shadow", x=160, y=718, width=260, height=20,
        fill="#060B0A", opacity=50, stroke=NONE)
# law book lying flat
book_ids = []
def book_add(res):
    if res and res.get("id"):
        book_ids.append(res["id"])
book_add(d.shape("rectangle", "Statute book", x=170, y=664, width=112,
                 height=50, radius=5, fill={"gradient": {"kind": "linear",
                 "stops": [{"offset": 0, "color": "#7A6248"},
                           {"offset": 1, "color": "#463A2C"}]}},
                 stroke=INK, strokeWidth=4))
book_add(d.path("M180,680 L266,680 M180,694 L266,694", "Book pages",
                fill=NONE, stroke="#D4C8A8", strokeWidth=2.5, opacity=75))
book_add(d.path("M282,664 L282,714", "Book spine", fill=NONE,
                stroke="#2A2118", strokeWidth=6))
book_add(d.text("STATUTE", "Book cover", x=226, y=692, size=11,
                font="Virelai Sans", color="#E8D5A0", justify="center"))
if book_ids:
    d.call("transform", {"ids": book_ids, "rotate": -3,
                         "origin": [226, 690]}, "tilt book")
d.text("=", "Equals", x=310, y=706, size=26, font="Virelai Sans",
       color=AMBER, justify="center")
# the shoe — worth exactly as much
d.path("M340,708 C340,692 354,682 366,688 C376,678 394,678 402,688 "
       "L414,696 C422,700 422,714 414,716 L352,716 C344,716 340,714 "
       "340,708 Z",
       "Shoe", fill={"gradient": {"kind": "linear", "stops": [
           {"offset": 0, "color": "#9A8868"},
           {"offset": 1, "color": "#4E4238"}]}},
       stroke=INK, strokeWidth=4, join="round")
d.path("M340,710 L416,710", "Sole", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
d.path("M360,688 C364,696 364,704 360,712", "Shoe lace curve", fill=NONE,
       stroke="#2A2118", strokeWidth=2.5, opacity=70)

d.shape("ellipse", "Bob shadow", x=400, y=792, width=200, height=26,
        fill="#060B0A", opacity=55, stroke=NONE)

# --- Bob: folder head, round body, ticket high ------------------------------------
# body
d.shape("ellipse", "Bob body", x=412, y=548, width=190, height=250,
        fill=BODY, stroke=INK, strokeWidth=5)
# collar + tie
d.path("M470,566 L500,596 L530,566", "Collar", fill=NONE,
       stroke="#EDE6D4", strokeWidth=7, join="round")
d.path("M500,596 L490,640 L500,668 L510,640 Z", "Tie", fill=RED,
       stroke=INK, strokeWidth=2.5, join="round")
# arms: left raised with the ticket, right shrugging out
d.path("M430,600 C396,570 384,540 386,506", "Arm L", fill=NONE,
       stroke="#46536A", strokeWidth=17, cap="round")
d.shape("ellipse", "Hand L", x=372, y=488, width=26, height=24,
        fill="#6E7E92", stroke=INK, strokeWidth=3.5)
d.path("M592,610 C626,624 644,646 648,672", "Arm R", fill=NONE,
       stroke="#46536A", strokeWidth=17, cap="round")
d.shape("ellipse", "Hand R", x=638, y=664, width=24, height=22,
        fill="#6E7E92", stroke=INK, strokeWidth=3.5)
# the ticket: number to nowhere
tick_ids = []
def tick_add(res):
    if res and res.get("id"):
        tick_ids.append(res["id"])
tick_add(d.path("M352,452 L424,448 L426,468 L418,470 L426,472 L428,492 "
                "L356,496 L354,476 L362,474 L354,472 Z", "Ticket",
                fill="#EDE6D4", stroke=INK, strokeWidth=3, join="round"))
tick_add(d.text("404", "Ticket number", x=390, y=477, size=17,
                font="Source Sans 3", color=RED, justify="center"))
if tick_ids:
    d.call("transform", {"ids": tick_ids, "rotate": -8,
                         "origin": [390, 472]}, "tilt ticket")
# folder head: manila file folder, tab up-left
d.path("M428,392 L486,392 L494,404 L566,404 L566,512 L428,512 Z",
       "Folder head", fill=MANILA, stroke=INK, strokeWidth=5,
       join="round")
d.path("M428,404 L428,512", "Folder fold", fill=NONE, stroke="#8A7048",
       strokeWidth=2, opacity=50)
# red tape strip sealing the corner
d.path("M566,486 L566,512 L534,512 Z", "Tape", fill=RED, opacity=80,
       stroke=NONE)
# glasses + unimpressed half-lids
d.shape("ellipse", "Lens L", x=448, y=432, width=40, height=40,
        fill=NONE, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Lens R", x=506, y=432, width=40, height=40,
        fill=NONE, stroke=INK, strokeWidth=4)
d.path("M488,450 L506,450", "Bridge", fill=NONE, stroke=INK,
       strokeWidth=4, cap="round")
d.path("M448,448 L434,442 M546,448 L560,442", "Temples", fill=NONE,
       stroke=INK, strokeWidth=3.5, cap="round")
d.path("M454,452 q7,8 14,0", "Eye L", fill=NONE, stroke=INK,
       strokeWidth=3.5, cap="round")
d.path("M512,452 q7,8 14,0", "Eye R", fill=NONE, stroke=INK,
       strokeWidth=3.5, cap="round")
# flat bureaucratic mouth
d.path("M478,492 L520,492", "Mouth", fill=NONE, stroke=INK,
       strokeWidth=4.5, cap="round")
# feet
d.shape("ellipse", "Foot L", x=448, y=790, width=32, height=14,
        fill="#2A3244", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Foot R", x=534, y=790, width=32, height=14,
        fill="#2A3244", stroke=INK, strokeWidth=3)

# --- name + key line + role ------------------------------------------------------
r = d.text("THE STATUTE'S AS GOOD AS A SHOE", "Key line", x=500, y=899,
           size=22, font="Virelai Sans", color=SOFT, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "key tracking", ids=[r["id"]], tracking=140)
d.text("BUREAU BOB", "Name", x=500, y=945, size=56,
       font="Virelai Sans", color=ICE, justify="center")
r = d.text("RIGHTS IN STATUTE NOT SOFTWARE", "Role", x=500, y=977,
           size=19, font="Virelai Sans", color="#7A9088",
           justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=170)

d.finish("lim-0444-bureau-bob-V1R00")
