#!/usr/bin/env python3
"""Neppy Sysdream — mascot portrait V1R00. Lost Login Spirit:
a translucent mascot suspended over a Neptune-era login screen, an
Activity Centers wireframe mockup and phantom .msstyles pages drifting
behind her. Windows Neptune build 5111 — the OS that never shipped:
aurora teal on an indigo-night backdrop. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Neppy Sysdream — Mascot Plate", 1000, 1000)

INK = "#26302E"   # warm dark ink, never black
BG_GRAD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000], "stops": [
    {"offset": 0, "color": "#0D1524"}, {"offset": 1, "color": "#050810"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#5E8E96"}, {"offset": 0.62, "color": "#33525E"},
    {"offset": 1, "color": "#16242E"}]}}
PANEL_GRAD = {"gradient": {"kind": "linear", "start": [0, 220], "end": [0, 540], "stops": [
    {"offset": 0, "color": "#E4EEF2"}, {"offset": 0.5, "color": "#B9CDD6"},
    {"offset": 1, "color": "#8AA4B2"}]}}
HEADER_GRAD = {"gradient": {"kind": "linear", "start": [0, 220], "end": [0, 262], "stops": [
    {"offset": 0, "color": "#5EA8B8"}, {"offset": 1, "color": "#2E7A8C"}]}}
NEPPY_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F0FAFD"}, {"offset": 0.55, "color": "#C4E0EA"},
    {"offset": 1, "color": "#8FB8C8"}]}}
HAIR_GRAD = {"gradient": {"kind": "linear", "start": [0, 300], "end": [0, 470], "stops": [
    {"offset": 0, "color": "#9AD0DC"}, {"offset": 1, "color": "#5E96A8"}]}}
GO_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#8FD06A"}, {"offset": 1, "color": "#4E9440"}]}}
MOCK = "#A8CDD8"

PCX, PCY, PR = 500, 460, 420

def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

# --- backdrop + plate ------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#6EA6B0", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#181C1A", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#BCDCE4", strokeWidth=3, opacity=30)
# aurora ribbons — the Whistler sky that never shipped
d.path("M200,665 C290,565 350,615 470,480 C600,340 700,360 810,255",
       "Aurora 1", fill=NONE, stroke="#4EC8B8", strokeWidth=70,
       opacity=10, cap="round")
d.path("M230,720 C320,630 390,690 510,560 C640,420 720,450 840,335",
       "Aurora 2", fill=NONE, stroke="#7AD0E8", strokeWidth=44,
       opacity=9, cap="round")
d.path("M180,300 C330,240 420,300 560,210 C660,148 710,160 750,180",
       "Aurora 3", fill=NONE, stroke="#9A8AE0", strokeWidth=30,
       opacity=8, cap="round")
# patina + flecks + starlight
d.shape("ellipse", "Patina 1", x=560, y=600, width=250, height=150,
        fill="#7AA4AE", opacity=14, stroke=NONE)
d.shape("ellipse", "Patina 2", x=180, y=200, width=230, height=140,
        fill="#24404C", opacity=20, stroke=NONE)
for i, (x, y, w) in enumerate([(214,342,5),(796,336,6),(180,546,5),(844,558,5),
                               (264,760,5),(726,764,6),(154,450,5),(856,624,5),
                               (434,120,5),(602,134,6),(340,156,4),(706,204,5),
                               (250,646,4),(668,720,5)]):
    assert on_disc(x, y, 12), (x, y)
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#E2F0F4", opacity=34, stroke=NONE)
# ghost arcs on the dark backdrop
d.path("M935,150 A105,105 0 0 0 845,60", "Ghost arc TR",
       fill=NONE, stroke="#3E6E7A", strokeWidth=14, opacity=10, cap="round")
d.path("M75,770 A120,120 0 0 0 185,875", "Ghost arc BL",
       fill=NONE, stroke="#3E6E7A", strokeWidth=10, opacity=8, cap="round")

# --- Activity Centers wireframe mockup, drifting behind -------------------------------
mx, my = 183, 235
d.path(rot_rect_path(mx + 102, my + 100, 204, 200, -3), "Mockup frame",
       fill="#16242E", opacity=45, stroke=MOCK, strokeWidth=2.5, dash=[7, 5])
d.path(rot_rect_path(mx + 102, my + 22, 196, 24, -3), "Mockup title",
       fill=NONE, stroke=MOCK, strokeWidth=2, dash=[7, 5], opacity=75)
d.path(rot_rect_path(mx + 52, my + 85, 76, 60, -3), "Mockup block 1",
       fill=NONE, stroke=MOCK, strokeWidth=2, dash=[5, 4], opacity=60)
d.path(rot_rect_path(mx + 149, my + 85, 76, 60, -3), "Mockup block 2",
       fill=NONE, stroke=MOCK, strokeWidth=2, dash=[5, 4], opacity=60)
d.path(rot_rect_path(mx + 102, my + 166, 168, 16, -3), "Mockup footer",
       fill=NONE, stroke=MOCK, strokeWidth=2, dash=[5, 4], opacity=50)
# placeholder glyphs inside the blocks — the panels nobody ever saw
d.path(rot_rect_path(mx + 52, my + 70, 38, 8, -3), "Mockup h1",
       fill=MOCK, opacity=45, stroke=NONE)
d.path(rot_rect_path(mx + 149, my + 70, 38, 8, -3), "Mockup h2",
       fill=MOCK, opacity=45, stroke=NONE)

# --- phantom .msstyles pages, right side ---------------------------------------------
def phantom_page(cx, cy, deg, label, op):
    """A dog-eared theme file, translucent — a theme that was never applied."""
    w, h = 64, 80
    d.path(rot_rect_path(cx, cy, w, h, deg), f"{label} page",
           fill="#BFD8E2", opacity=op, stroke="#DDEDF2", strokeWidth=2)
    # folded corner
    d.path(f"M{cx + w / 2 - 18},{cy - h / 2} L{cx + w / 2},{cy - h / 2 + 18} "
           f"L{cx + w / 2 - 18},{cy - h / 2 + 18} Z", f"{label} fold",
           fill="#8FB8C8", opacity=op + 10, stroke=NONE)
    # the theme swatch inside
    d.path(rot_rect_path(cx, cy + 6, w - 22, 10, deg), f"{label} swatch 1",
           fill="#7AD0E8", opacity=op + 15, stroke=NONE)
    d.path(rot_rect_path(cx, cy + 22, w - 22, 10, deg), f"{label} swatch 2",
           fill="#9A8AE0", opacity=op + 15, stroke=NONE)

phantom_page(742, 560, 8, "MSstyles 1", 28)
phantom_page(798, 470, -7, "MSstyles 2", 20)
d.text("MSSTYLES", "MSstyles label", x=742, y=584, size=11,
       font="Source Sans 3", color="#7A9AA8", justify="center")

# --- the login screen, suspended behind her -------------------------------------------
d.shape("rectangle", "Login shadow", x=296, y=228, width=384, height=300,
        radius=14, fill="#04101A", opacity=45, stroke=NONE)
d.shape("rectangle", "Login panel", x=290, y=220, width=384, height=300,
        radius=14, fill=PANEL_GRAD, stroke="#1E323C", strokeWidth=4)
d.shape("rectangle", "Login header", x=290, y=220, width=384, height=46,
        radius=14, fill=HEADER_GRAD, stroke=NONE)
d.path("M320,236 L322,250 M312,243 L330,243", "Header mark",
       fill=NONE, stroke="#E4F2F6", strokeWidth=4, cap="round", opacity=85)
d.path("M348,236 L420,236 M348,250 L400,250", "Header lines",
       fill=NONE, stroke="#C8E4EA", strokeWidth=4, cap="round", opacity=60)
# user tile with a person silhouette
d.shape("rectangle", "User tile", x=322, y=292, width=88, height=88,
        radius=10, fill={"gradient": {"kind": "linear", "stops": [
            {"offset": 0, "color": "#DDE8EC"}, {"offset": 1, "color": "#A9BEC8"}]}},
        stroke="#4A626E", strokeWidth=3)
d.shape("ellipse", "Tile head", x=352, y=310, width=28, height=28,
        fill="#5E7684", stroke=NONE)
d.path("M342,368 C346,352 356,344 366,344 C376,344 386,352 390,368 Z",
       "Tile shoulders", fill="#5E7684", stroke=NONE)
d.path("M332,398 L402,398", "Tile name line",
       fill=NONE, stroke="#7A8E98", strokeWidth=5, cap="round", opacity=60)
# password field + bullets + go button
d.shape("rectangle", "Password field", x=436, y=306, width=190, height=42,
        radius=8, fill="#F0F6F8", stroke="#4A626E", strokeWidth=3)
for j in range(5):
    d.shape("ellipse", f"Bullet {j+1}", x=452 + j * 30, y=320, width=12,
            height=12, fill="#3E545E", stroke=NONE)
d.shape("ellipse", "Go button", x=636, y=306, width=42, height=42,
        fill=GO_GRAD, stroke="#2E5E28", strokeWidth=3)
d.path("M648,327 L664,327 M658,319 L666,327 L658,335", "Go arrow",
       fill=NONE, stroke="#F0F6F0", strokeWidth=4, cap="round")
# status strip at the panel's foot — waiting forever
d.path("M322,486 L470,486", "Status line 1",
       fill=NONE, stroke="#5E7684", strokeWidth=5, cap="round", opacity=55)
d.path("M322,504 L410,504", "Status line 2",
       fill=NONE, stroke="#5E7684", strokeWidth=5, cap="round", opacity=40)
d.shape("ellipse", "Status spinner 1", x=640, y=484, width=10, height=10,
        fill="#7AD0E8", opacity=80, stroke=NONE)
d.shape("ellipse", "Status spinner 2", x=624, y=498, width=10, height=10,
        fill="#7AD0E8", opacity=50, stroke=NONE)
d.shape("ellipse", "Status spinner 3", x=654, y=500, width=10, height=10,
        fill="#7AD0E8", opacity=30, stroke=NONE)

# --- Neppy: the translucent spirit suspended over it ------------------------------------
# hover glow — the login backlight refracted through her
d.shape("ellipse", "Hover glow", x=380, y=620, width=250, height=70,
        fill="#7AD0E8", opacity=16, stroke=NONE)
d.shape("ellipse", "Hover glow core", x=430, y=636, width=150, height=36,
        fill="#A8E0EC", opacity=14, stroke=NONE)
# hair drifting weightless behind her shoulders
d.path("M500,330 C448,330 414,366 410,416 C380,404 364,384 362,352 "
       "C396,332 420,322 448,300 C470,284 530,284 552,300 "
       "C580,322 604,332 638,352 C636,384 620,404 590,416 "
       "C586,366 552,330 500,330 Z",
       "Hair mantle", fill=HAIR_GRAD, opacity=62, stroke="#8FC2D0",
       strokeWidth=2.5)
# body: nightgown tapering to a dreamtail
d.path("M500,440 C548,442 574,480 578,536 C582,600 570,660 540,700 "
       "C528,690 530,676 522,700 C514,718 505,722 498,708 "
       "C491,694 493,690 484,710 C474,726 462,716 460,698 "
       "C436,664 424,606 426,540 C428,482 452,442 500,440 Z",
       "Nightgown", fill=NEPPY_GRAD, opacity=68, stroke="#D6EEF4",
       strokeWidth=3)
# head
d.shape("ellipse", "Head", x=436, y=330, width=128, height=118,
        fill=NEPPY_GRAD, opacity=74, stroke="#D6EEF4", strokeWidth=3)
# face-framing bangs
d.path("M436,384 C444,342 470,322 500,322 C530,322 556,342 564,384 "
       "C548,364 534,352 520,352 C526,364 528,374 526,382 "
       "C514,362 494,354 478,358 C484,368 486,376 484,382 "
       "C470,366 452,368 436,384 Z",
       "Bangs", fill=HAIR_GRAD, opacity=78, stroke=NONE)
# dreaming face: closed eyes, long lashes, the softest smile
d.path("M456,404 Q468,414 482,404", "Eye L (dreaming)",
       fill=NONE, stroke="#2E4A52", strokeWidth=4, cap="round")
d.path("M518,404 Q532,414 546,404", "Eye R (dreaming)",
       fill=NONE, stroke="#2E4A52", strokeWidth=4, cap="round")
d.path("M458,404 L452,398 M544,404 L550,398", "Lashes",
       fill=NONE, stroke="#2E4A52", strokeWidth=3, cap="round", opacity=80)
d.path("M490,430 Q501,437 512,430", "Smile",
       fill=NONE, stroke="#2E4A52", strokeWidth=3.5, cap="round")
d.shape("ellipse", "Blush L", x=442, y=418, width=22, height=11,
        fill="#8FC8D8", opacity=30, stroke=NONE)
d.shape("ellipse", "Blush R", x=536, y=418, width=22, height=11,
        fill="#8FC8D8", opacity=30, stroke=NONE)
# inner light through her chest — a UI ghost still rendering
d.shape("ellipse", "Core light", x=468, y=500, width=64, height=80,
        fill="#FFFFFF", opacity=22, stroke=NONE)
# arms drifting outward, palms up — suspended
d.path("M438,500 C402,506 372,528 356,558 C362,570 378,572 388,564 "
       "C402,544 420,528 442,518 Z",
       "Arm L", fill=NEPPY_GRAD, opacity=66, stroke="#D6EEF4", strokeWidth=2.5)
d.shape("ellipse", "Hand L", x=346, y=552, width=30, height=22,
        fill=NEPPY_GRAD, opacity=70, stroke="#D6EEF4", strokeWidth=2.5)
d.path("M566,498 C598,492 626,502 646,524 C644,538 630,544 618,538 "
       "C602,522 584,514 562,514 Z",
       "Arm R", fill=NEPPY_GRAD, opacity=66, stroke="#D6EEF4", strokeWidth=2.5)
d.shape("ellipse", "Hand R", x=640, y=520, width=28, height=22,
        fill=NEPPY_GRAD, opacity=70, stroke="#D6EEF4", strokeWidth=2.5)
# sleep-motes rising off her hem
for i, (x, y, s, o) in enumerate([(468, 742, 8, 40), (540, 730, 6, 34),
                                  (506, 762, 7, 28), (430, 720, 5, 30)]):
    assert on_disc(x, y, 8), (x, y)
    d.shape("ellipse", f"Sleep mote {i+1}", x=x, y=y, width=s, height=s,
            fill="#C4E4EE", opacity=o, stroke=NONE)

# --- name + role ----------------------------------------------------------------------
d.text("NEPPY SYSDREAM", "Name", x=500, y=930, size=56, font="Virelai Sans",
       color="#DCECF2", justify="center")
r = d.text("LOST LOGIN SPIRIT", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#9FC4CC", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=220)

d.finish("032.neppy-sysdream-V1R00")
