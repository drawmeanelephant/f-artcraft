#!/usr/bin/env python3
"""Appeal Feather — mascot portrait V1R00.
A feather mascot riding the air-conditioning updraft above the cubicle
tops, banking down through the corridor toward the bright slit under the
manager's door — the route objections are not watched on. 1000x1000.
Gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Appeal Feather — Mascot Portrait", 1000, 1000)

INK = "#2C1E14"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#131810"}, {"offset": 1, "color": "#070A06"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#626652"}, {"offset": 0.7, "color": "#4A4C3E"},
    {"offset": 1, "color": "#2A2C22"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#40423A"}, {"offset": 1, "color": "#1E201A"}]}}
CUBE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6E7260"}, {"offset": 1, "color": "#4A4E42"}]}}
CUBE_TOP = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#8A8E78"}, {"offset": 1, "color": "#5C6050"}]}}
DOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#54402C"}, {"offset": 1, "color": "#2E2016"}]}}
FEATHER_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F4EDD8"}, {"offset": 1, "color": "#C9BC96"}]}}
AIR = "#BCD0D6"
SLIT = "#F0D494"

# --- feather geometry: built in feather space, rotated into place -------------
# feather space: tip (0,-165), calamus (0,150), vane ~84 wide at y~-30.
TILT = 125           # degrees clockwise from vertical: swooping down-right
FCX, FCY = 560, 575  # feather-space origin on canvas

def fx(px, py, tilt=TILT, cx=FCX, cy=FCY, s=1.0):
    t = math.radians(tilt); c, sn = math.cos(t), math.sin(t)
    x, y = px * s, py * s
    return (cx + x * c - y * sn, cy + x * sn + y * c)

def fpath(cmds, tilt=TILT, cx=FCX, cy=FCY, s=1.0):
    """cmds: list of (cmd, [pts...]) in feather space -> transformed d string."""
    out = []
    for cmd, pts in cmds:
        xy = [f"{v:.1f}" for p in pts for v in fx(*p, tilt, cx, cy, s)]
        out.append(cmd + ",".join(xy))
    return " ".join(out)

VANE = [("M", [(0, 150)]),
        ("C", [(-6, 120), (-8, 90), (-14, 60)]),
        ("C", [(-30, 20), (-46, -10), (-42, -60)]),
        ("C", [(-38, -110), (-22, -140), (0, -165)]),
        ("C", [(22, -140), (38, -110), (42, -60)]),
        ("C", [(46, -10), (30, 20), (14, 60)]),
        ("C", [(8, 90), (6, 120), (0, 150)]), ("Z", [])]

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#8E9078", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#DDD8BC", strokeWidth=3, opacity=50)
for i, (x, y, w) in enumerate([(193,234,8),(801,229,7),(157,526,9),(837,544,8),
                               (246,766,7),(754,748,9),(133,394,6),(865,389,7),
                               (391,112,7),(613,109,8),(333,824,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#4E5240", opacity=45, stroke=NONE)

# --- floor ---------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#12140E",
       strokeWidth=4, opacity=70)

# --- AC vent, high left; the updraft nobody watches ------------------------------
d.shape("rectangle", "Vent", x=185, y=252, width=118, height=44,
        fill="#3A4038", stroke=INK, strokeWidth=3.5, radius=5)
for i in range(4):
    y = 261 + i * 8
    d.path(f"M195,{y} L293,{y}", f"Vent slat {i+1}", fill=NONE,
           stroke="#20241E", strokeWidth=3.5, opacity=80)
d.shape("ellipse", "Cool haze", x=170, y=225, width=160, height=90,
        fill=AIR, opacity=8, stroke=NONE)
for i, (x0, c1, c2, e) in enumerate([
        (212, (226, 200), (262, 182), (302, 168)),
        (246, (262, 198), (314, 178), (358, 162)),
        (280, (302, 202), (364, 188), (414, 178))]):
    d.path(f"M{x0},250 C{c1[0]},{c1[1]} {c2[0]},{c2[1]} {e[0]},{e[1]}",
           f"Updraft {i+1}", fill=NONE, stroke=AIR, strokeWidth=4,
           cap="round", opacity=20)

# --- the cubicle row --------------------------------------------------------------
# panel A, left
d.shape("rectangle", "Cube A front", x=150, y=580, width=200, height=120,
        fill=CUBE_GRAD, stroke=INK, strokeWidth=4)
d.shape("rectangle", "Cube A top", x=150, y=580, width=200, height=16,
        fill=CUBE_TOP, stroke=INK, strokeWidth=3)
for i, y in enumerate([620, 655]):
    d.path(f"M158,{y} L342,{y}", f"Cube A seam {i+1}", fill=NONE,
           stroke="#3C4034", strokeWidth=2.5, opacity=60)
# a task lamp still on inside A
d.shape("ellipse", "Lamp glow A", x=205, y=520, width=90, height=70,
        fill="#F0D494", opacity=10, stroke=NONE)
d.shape("ellipse", "Lamp A", x=242, y=566, width=16, height=14,
        fill="#F0D494", stroke=INK, strokeWidth=2.5)
# panel B, center — a touch taller, a touch nearer
d.shape("rectangle", "Cube B front", x=380, y=560, width=185, height=140,
        fill=CUBE_GRAD, stroke=INK, strokeWidth=4)
d.shape("rectangle", "Cube B top", x=380, y=560, width=185, height=16,
        fill=CUBE_TOP, stroke=INK, strokeWidth=3)
for i, y in enumerate([605, 650]):
    d.path(f"M388,{y} L557,{y}", f"Cube B seam {i+1}", fill=NONE,
           stroke="#3C4034", strokeWidth=2.5, opacity=60)
# monitor glowing inside B, face to the wall
d.shape("ellipse", "Screen glow", x=425, y=470, width=110, height=80,
        fill="#8FB4BC", opacity=10, stroke=NONE)
d.shape("rectangle", "Monitor", x=448, y=505, width=64, height=48,
        fill="#232A2E", stroke=INK, strokeWidth=3, radius=4)
d.path("M454,512 L506,512 L506,546 L454,546 Z", "Screen", fill="#5E7E86",
       opacity=55, stroke=NONE)
# a shed feather resting on B's ledge — molted toward the authority
d.path(fpath(VANE, tilt=74, cx=472, cy=553, s=0.16), "Shed feather",
       fill="#D8CCA8", stroke=INK, strokeWidth=2.5)
d.path(fpath([("M", [(0, 150)]), ("L", [(0, -150)])],
             tilt=74, cx=472, cy=553, s=0.16), "Shed quill",
       fill=NONE, stroke="#A89A76", strokeWidth=2)

# --- the door, right; its slit is the route -----------------------------------------
d.shape("rectangle", "Door frame", x=692, y=327, width=150, height=373,
        fill="#221A12", stroke=INK, strokeWidth=4)
d.shape("rectangle", "Door", x=700, y=335, width=134, height=365,
        fill=DOOR_GRAD, stroke=INK, strokeWidth=4)
d.shape("rectangle", "Door panel top", x=720, y=362, width=96, height=120,
        fill="#3E2E1E", stroke="#241A10", strokeWidth=3, radius=4)
d.shape("rectangle", "Door panel low", x=720, y=510, width=96, height=140,
        fill="#3E2E1E", stroke="#241A10", strokeWidth=3, radius=4)
d.shape("ellipse", "Knob", x=712, y=548, width=16, height=16,
        fill="#A8842E", stroke=INK, strokeWidth=3)
# the slit of light underneath
d.shape("rectangle", "Door slit", x=700, y=688, width=134, height=12,
        fill={"gradient": {"kind": "linear", "stops": [
            {"offset": 0, "color": "#F4DC9C"}, {"offset": 1, "color": "#D8B464"}]}},
        stroke=NONE)
d.path("M700,700 L834,700 L780,754 L645,748 Z", "Slit spill",
       fill=SLIT, opacity=12, stroke=NONE)

# --- the flight path, faint, off the watched routes ---------------------------------
d.path("M414,178 C540,168 648,260 628,400 C616,478 566,516 500,520",
       "Flight path", fill=NONE, stroke=AIR, strokeWidth=3,
       cap="round", opacity=16)

# --- the feather mascot, mid-slip ---------------------------------------------------
ex, ey = fx(0, 150)   # calamus position for the drop shadow below
d.shape("ellipse", "Feather shadow", x=ex-70, y=676, width=150, height=14,
        fill="#0E0A06", opacity=30, stroke=NONE)
d.path(fpath(VANE), "Vane", fill=FEATHER_GRAD, stroke=INK, strokeWidth=4)
# rachis: quill line with a bare calamus tail
d.path(fpath([("M", [(0, 178)]), ("L", [(0, -150)])]), "Rachis",
       fill=NONE, stroke="#A89A76", strokeWidth=5, cap="round")
# a few barb separations
for i, (x0, y0, x1, y1) in enumerate([(-30, -40, -6, -18), (30, -46, 6, -22),
                                      (-34, 6, -8, 24), (34, 0, 8, 22)]):
    p0 = fx(x0, y0); p1 = fx(x1, y1)
    d.path(f"M{p0[0]:.1f},{p0[1]:.1f} L{p1[0]:.1f},{p1[1]:.1f}",
           f"Barb {i+1}", fill=NONE, stroke="#B4A884", strokeWidth=2.5,
           opacity=70)
# face near the tip: calm, deniable
e1 = fx(-12, -96); e2 = fx(13, -98)
d.shape("ellipse", "Eye L", x=e1[0]-6, y=e1[1]-6, width=12, height=12,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Eye R", x=e2[0]-6, y=e2[1]-6, width=12, height=12,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Glint L", x=e1[0]-4, y=e1[1]-4, width=3.5, height=3.5,
        fill="#F8F2DC", stroke=NONE)
d.shape("ellipse", "Glint R", x=e2[0]-4, y=e2[1]-4, width=3.5, height=3.5,
        fill="#F8F2DC", stroke=NONE)
m0 = fx(-10, -72); m1 = fx(10, -74)
d.path(f"M{m0[0]:.1f},{m0[1]:.1f} C{fx(-3,-66)[0]:.1f},{fx(-3,-66)[1]:.1f} "
       f"{fx(4,-66)[0]:.1f},{fx(4,-66)[1]:.1f} {m1[0]:.1f},{m1[1]:.1f}",
       "Mouth", fill=NONE, stroke=INK, strokeWidth=3.5, cap="round")
# motion ticks off the calamus
for i, (x0, y0, x1, y1) in enumerate([(-14, 168, -20, 196), (6, 172, 8, 200),
                                      (-30, 160, -40, 184)]):
    p0 = fx(x0, y0); p1 = fx(x1, y1)
    d.path(f"M{p0[0]:.1f},{p0[1]:.1f} L{p1[0]:.1f},{p1[1]:.1f}",
           f"Slip tick {i+1}", fill=NONE, stroke="#EAE0C8", strokeWidth=3,
           cap="round", opacity=55)

# --- captions -------------------------------------------------------------------------
d.text("APPEAL FEATHER", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#EDE8D0", justify="center")
r = d.text("THE SPEED OF DENIABILITY", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#BCC2A4", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("268.appeal-feather-V1R00")
