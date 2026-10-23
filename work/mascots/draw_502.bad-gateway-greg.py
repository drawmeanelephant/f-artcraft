#!/usr/bin/env python3
"""Bad Gateway Greg — mascot portrait V1R00.
RJ45-headed mascot beside a proxy relay with crossed patch cables; the
forwarded response is stamped 502. 1000x1000. Gradients + translucent
shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Bad Gateway Greg — Mascot Portrait", 1000, 1000)

INK = "#241F2C"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#0E1420"}, {"offset": 1, "color": "#06080E"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#3A4E6E"}, {"offset": 0.7, "color": "#25344E"},
    {"offset": 1, "color": "#151F30"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#202E48"}, {"offset": 1, "color": "#0F1728"}]}}
RELAY = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#54607A"}, {"offset": 1, "color": "#2E3648"}]}}
GREG = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#8A94AC"}, {"offset": 0.75, "color": "#5E6A82"},
    {"offset": 1, "color": "#3E475E"}]}}
PLUG = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7E8AA2"}, {"offset": 1, "color": "#4A5468"}]}}
CABLE_A = "#4EC0B0"
CABLE_B = "#E0705E"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#56709A", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C4D4EC", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(192,235,8),(802,230,7),(158,522,9),(836,545,8),
                               (248,766,7),(752,750,9),(133,392,6),(864,392,7),
                               (392,113,7),(614,110,8),(333,823,6),(666,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#44587E", opacity=45, stroke=NONE)

# --- floor: bottom segment closed on the disc's own arc -----------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0C1322",
       strokeWidth=4, opacity=70)

# --- the forwarded response: a packet stamped 502, mid-flight -------------------
d.path("M300,300 C380,255 470,240 560,252", "Packet trail", fill=NONE,
       stroke="#8FA4C8", strokeWidth=4, dash=[10,9], cap="round", opacity=60)
d.shape("ellipse", "Packet glow", x=560, y=195, width=150, height=110,
        fill="#E0705E", opacity=14, stroke=NONE)
d.path("M578,218 L688,218 L688,288 L578,288 Z", "Packet",
       fill="#D8C9A8", stroke=INK, strokeWidth=5, join="round")
d.path("M578,218 L633,258 L688,218", "Packet flap", fill=NONE, stroke="#8A744E",
       strokeWidth=4)
# the stamp
d.shape("rectangle", "Stamp 502", x=600, y=255, width=66, height=26,
        fill="#B8452E", opacity=90, stroke=INK, strokeWidth=3, radius=4)
d.text("502", "Stamp text", x=616, y=275, size=17, font="Virelai Sans",
       color="#F4E4D8", justify="left")

# --- proxy relay box --------------------------------------------------------------
d.shape("ellipse", "Relay shadow", x=560, y=665, width=270, height=30,
        fill="#0A1020", opacity=45, stroke=NONE)
d.shape("rectangle", "Relay", x=555, y=370, width=275, height=305,
        fill=RELAY, stroke=INK, strokeWidth=6, radius=12)
d.shape("rectangle", "Face plate", x=572, y=390, width=241, height=170,
        fill="#2A3244", stroke=INK, strokeWidth=4, radius=8)
# port row: four jacks
for i in range(4):
    x = 592 + i*56
    d.shape("rectangle", f"Port {i+1}", x=x, y=430, width=42, height=36,
            fill="#161C28", stroke=INK, strokeWidth=3, radius=4)
    d.shape("ellipse", f"Port LED {i+1}", x=x+15, y=414, width=10, height=10,
            fill="#E0705E" if i in (0, 3) else "#5E8A6E",
            stroke=NONE, opacity=90)
# label + vents + status line
d.text("RELAY-7", "Relay label", x=580, y=545, size=14, font="Virelai Sans",
       color="#9AAEC8", justify="left")
for i in range(3):
    d.shape("rectangle", f"Vent {i+1}", x=700, y=510+i*16, width=95, height=7,
            fill="#161C28", opacity=70, stroke=NONE, radius=3)
d.shape("rectangle", "Status strip", x=580, y=580, width=220, height=46,
        fill="#121A26", stroke=INK, strokeWidth=3, radius=6)
d.text("FWD RESPONSE →", "Status line 1", x=592, y=598, size=12,
       font="Virelai Sans", color="#7E94B0", justify="left")
d.text("ACK_FAILURE: apology rejected", "Status line 2", x=592, y=616, size=11,
       font="Virelai Sans", color="#E0705E", justify="left")
d.shape("ellipse", "Status LED", x=795, y=590, width=12, height=12,
        fill="#E0705E", stroke=NONE)
# feet
d.shape("rectangle", "Foot L", x=585, y=675, width=34, height=22,
        fill="#2E3648", stroke=INK, strokeWidth=4, radius=5)
d.shape("rectangle", "Foot R", x=765, y=675, width=34, height=22,
        fill="#2E3648", stroke=INK, strokeWidth=4, radius=5)

# --- crossed patch cables: an X of misrouting -------------------------------------
# teal cable: port 1 (upper-left) dives to port 4 zone then loops OUT of frame of
# the faceplate down to a dangling end
d.path(f"M613,466 C640,540 700,560 770,505 C800,480 810,452 812,468",
       "Cable teal", fill=NONE, stroke=CABLE_A, strokeWidth=11, cap="round")
d.path(f"M613,466 C640,540 700,560 770,505", "Cable teal hi", fill=NONE,
       stroke="#8FE0D4", strokeWidth=3, cap="round", opacity=60)
# coral cable: port 4 (right) sweeps left-down across the teal run to a plug end
d.path(f"M791,466 C760,545 690,585 610,575 C575,570 555,585 552,605",
       "Cable coral", fill=NONE, stroke=CABLE_B, strokeWidth=11, cap="round")
d.path(f"M791,466 C760,545 690,585 610,575", "Cable coral hi", fill=NONE,
       stroke="#F4A496", strokeWidth=3, cap="round", opacity=60)
# connector heads on the dangling ends
d.shape("rectangle", "Teal plug end", x=800, y=455, width=26, height=22,
        fill=CABLE_A, stroke=INK, strokeWidth=4, radius=4)
d.shape("rectangle", "Coral plug end", x=538, y=598, width=26, height=22,
        fill=CABLE_B, stroke=INK, strokeWidth=4, radius=4)

# --- Greg: RJ45-headed little relay, guilty ----------------------------------------
d.shape("ellipse", "Greg shadow", x=265, y=672, width=230, height=30,
        fill="#0A1020", opacity=45, stroke=NONE)
# body
d.path("M380,470 C455,470 495,545 495,620 C495,680 450,705 380,705 "
       "C310,705 265,680 265,620 C265,545 305,470 380,470 Z",
       "Greg body", fill=GREG, stroke=INK, strokeWidth=6)
# body highlight + seam
d.shape("ellipse", "Body hi", x=320, y=500, width=110, height=50,
        fill="#FFFFFF", opacity=12, stroke=NONE)
# guilty shrug arms
d.path("M270,565 C240,550 225,530 228,505", "Arm L", fill=NONE,
       stroke="#5E6A82", strokeWidth=17, cap="round")
d.shape("ellipse", "Palm L", x=218, y=488, width=26, height=22,
        fill="#7E8AA2", stroke=INK, strokeWidth=4)
d.path("M490,565 C520,550 535,530 532,505", "Arm R", fill=NONE,
       stroke="#5E6A82", strokeWidth=17, cap="round")
d.shape("ellipse", "Palm R", x=520, y=488, width=26, height=22,
        fill="#7E8AA2", stroke=INK, strokeWidth=4)
# head: the connector
d.shape("rectangle", "Plug head", x=315, y=345, width=130, height=125,
        fill=PLUG, stroke=INK, strokeWidth=6, radius=10)
# gold contacts along the top
for i in range(8):
    x = 328 + i*14
    d.shape("rectangle", f"Contact {i+1}", x=x, y=352, width=8, height=20,
            fill="#E8C25E", stroke=INK, strokeWidth=2, radius=1)
# latch tab
d.path("M355,345 L355,325 L405,325 L405,345", "Latch", fill="#5A6478",
       stroke=INK, strokeWidth=4, join="round")
# face: guilty eyes, small wavy sorry mouth
d.path("M345,415 C352,423 362,423 369,415", "Eye L", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
d.path("M391,415 C398,423 408,423 415,415", "Eye R", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
d.path("M358,448 C366,442 374,448 382,448 C390,448 398,442 404,448",
       "Sorry mouth", fill=NONE, stroke=INK, strokeWidth=5, cap="round")
# blush of guilt
d.shape("ellipse", "Blush L", x=330, y=432, width=22, height=12,
        fill="#E0705E", opacity=45, stroke=NONE)
d.shape("ellipse", "Blush R", x=410, y=432, width=22, height=12,
        fill="#E0705E", opacity=45, stroke=NONE)
# the intact apology note in his left palm
d.path("M196,462 L244,462 L244,492 L196,492 Z", "Sorry note",
       fill="#E8DCC0", stroke=INK, strokeWidth=3, join="round")
d.text("sorry", "Note text", x=204, y=483, size=13, font="Virelai Sans",
       color="#6A5A40", justify="left")

# --- captions ------------------------------------------------------------------
d.text("BAD GATEWAY GREG", "Name", x=500, y=930, size=54, font="Virelai Sans",
       color="#C4D4EC", justify="center")
r = d.text("PROTOCOL MISALIGNMENT MANAGER", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#8CA0C4", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("502.bad-gateway-greg-V1R00")
