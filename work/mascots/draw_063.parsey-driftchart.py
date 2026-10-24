#!/usr/bin/env python3
"""Parsey Driftchart — mascot portrait V1R00.
Designated custodian of TikiWiki Realms: hooded figure in a cloak
quilted from broken translation strings, one eye patched (the one that
saw the plugin stack loop into itself), patching a tracker form with a
pencil. Tokens drift loose into the admin void.
1000x1000. Gradients + translucent shading, never flat fills.
Cloak tokens are set in Source Sans 3 (Virelai carries no braces/digits)."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Parsey Driftchart — Mascot Portrait", 1000, 1000)

INK = "#1E1A24"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#0D0E16"}, {"offset": 1, "color": "#07070C"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#38344E"}, {"offset": 0.7, "color": "#232036"},
    {"offset": 1, "color": "#131020"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1E1C2E"}, {"offset": 1, "color": "#100E1A"}]}}
HOOD_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4A5678"}, {"offset": 1, "color": "#2A3048"}]}}
FORM_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3E4458"}, {"offset": 1, "color": "#262A3A"}]}}
FIELD_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4A5168"}, {"offset": 1, "color": "#343A4E"}]}}
SEAM = "#0E0C16"
STITCH = "#9A92B4"
CHALK = "#C8CCE0"
QUILT = ["#4E5A7A", "#6A5A72", "#566E62", "#74584E", "#5A6480",
         "#6E6248", "#525E70", "#6A4E5E", "#4E6A6A", "#5E5A4E"]

def rp(cx, cy, x, y, deg):
    a = math.radians(deg); c, s = math.cos(a), math.sin(a)
    return (cx + (x - cx) * c - (y - cy) * s,
            cy + (x - cx) * s + (y - cy) * c)

# --- backdrop + plate -----------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#8E86B8", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C6C2E0", strokeWidth=3, opacity=40)
for i, (x, y, w) in enumerate([(188,240,8),(804,232,7),(150,520,9),(844,538,8),
                               (252,766,7),(750,752,9),(130,390,6),(864,398,7),
                               (390,110,7),(618,112,8),(338,820,6),(666,822,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#2C2844", opacity=55, stroke=NONE)

# --- strings drifting loose into the void ------------------------------------------
for i, (txt, x, y, sz, o) in enumerate([("{tr}", 596, 300, 16, 45),
                                        ("%%", 668, 238, 15, 32),
                                        ("…", 736, 190, 20, 24)]):
    t = d.text(txt, f"Drift {i+1}", x=x, y=y, size=sz,
               font="Source Sans 3", color=CHALK, justify="center")
    if t and t.get("id"):
        d.cmd("object.setProps", f"drift {i+1} fade", ids=[t["id"]],
              opacity=o)

# --- floor ----------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0A0812",
       strokeWidth=4, opacity=70)
d.shape("ellipse", "Figure shadow", x=270, y=700, width=320, height=26,
        fill="#05040A", opacity=60, stroke=NONE)

# --- the tracker form, mid-render ------------------------------------------------
FX, FY, FD = 730, 430, 6
d.path(rot_rect_path(FX, FY, 204, 244, FD), "Tracker form",
       fill=FORM_GRAD, stroke=INK, strokeWidth=5, join="round")
hx, hy = rp(FX, FY, FX, FY - 104, FD)
t = d.text("TRACKER", "Form title", x=hx, y=hy + 4, size=13,
           font="Virelai Sans", color=CHALK, justify="center")
if t and t.get("id"):
    d.cmd("object.rotate", "form title tilt", ids=[t["id"]], angle=-FD,
          origin=[hx, hy])
# three field rows: label squiggle + field box
for i, fy in enumerate([FY - 62, FY - 10, FY + 42]):
    lx, ly = rp(FX, FY, FX - 62, fy, FD)
    d.path(rot_rect_path(lx, ly, 44, 9, FD), f"Field label {i+1}",
           fill="#5A6278", opacity=80, stroke=NONE)
    bx, by = rp(FX, FY, FX + 24, fy, FD)
    d.path(rot_rect_path(bx, by, 96, 26, FD), f"Field box {i+1}",
           fill=FIELD_GRAD, stroke=INK, strokeWidth=2.5)
# the middle field is being patched: pencil scribbles + a tape strip
z0 = rp(FX, FY, FX - 8, FY - 10, FD); z1 = rp(FX, FY, FX + 18, FY - 16, FD)
z2 = rp(FX, FY, FX + 34, FY - 4, FD);  z3 = rp(FX, FY, FX + 52, FY - 12, FD)
d.path(f"M{z0[0]:.0f},{z0[1]:.0f} L{z1[0]:.0f},{z1[1]:.0f} "
       f"L{z2[0]:.0f},{z2[1]:.0f} L{z3[0]:.0f},{z3[1]:.0f}",
       "Pencil patch", fill=NONE, stroke="#B8BCCE", strokeWidth=2.5,
       cap="round", join="round", opacity=80)
tx, ty = rp(FX, FY, FX + 62, FY - 22, FD)
d.path(rot_rect_path(tx, ty, 44, 16, FD - 14), "Tape patch",
       fill="#D8C89A", opacity=55, stroke=NONE)
# a submit button that will never fire
sx, sy = rp(FX, FY, FX + 30, FY + 90, FD)
d.path(rot_rect_path(sx, sy, 88, 28, FD), "Save button",
       fill="#2E3444", stroke="#5A6278", strokeWidth=2, dash=[5, 4])
st = d.text("SAVE", "Save label", x=sx, y=sy + 4, size=11,
            font="Virelai Sans", color="#8A90A8", justify="center")
if st and st.get("id"):
    d.cmd("object.rotate", "save tilt", ids=[st["id"]], angle=-FD,
          origin=[sx, sy])

# --- cloak underlayer: the dark between the seams ----------------------------------
d.path("M352,394 C300,480 278,580 272,700 C390,716 470,716 588,700 "
       "C582,580 560,480 508,394 Z", "Cloak seams",
       fill=SEAM, stroke=INK, strokeWidth=5)

# --- the quilted cloak -------------------------------------------------------------
def cloak_l(y): return 352 - (y - 394) * (64 / 306)
def cloak_r(y): return 508 + (y - 394) * (64 / 306)

rows = [(398, 474), (478, 550), (554, 626), (630, 692)]
colsets = [[(0.0, 0.55), (0.55, 1.0)],
           [(0.0, 0.34), (0.34, 0.67), (0.67, 1.0)],
           [(0.0, 0.40), (0.40, 0.72), (0.72, 1.0)],
           [(0.0, 0.45), (0.45, 1.0)]]
tokens = {(0, 1): "%%SIG%%", (1, 0): "{tr}", (1, 2): "NULL",
          (2, 1): "{/tr}", (2, 2): "LANG?", (3, 0): "%s"}
pi = 0
for ri, (y0, y1) in enumerate(rows):
    for ci, (f0, f1) in enumerate(colsets[ri]):
        w0 = cloak_r(y0) - cloak_l(y0); w1 = cloak_r(y1) - cloak_l(y1)
        x0t = cloak_l(y0) + f0 * w0 + 3; x1t = cloak_l(y0) + f1 * w0 - 3
        x0b = cloak_l(y1) + f0 * w1 + 3; x1b = cloak_l(y1) + f1 * w1 - 3
        col = QUILT[pi % len(QUILT)]
        d.path(f"M{x0t:.0f},{y0+3} L{x1t:.0f},{y0+3} L{x1b:.0f},{y1-3} "
               f"L{x0b:.0f},{y1-3} Z", f"Panel {ri+1}-{ci+1}",
               fill=col, stroke=STITCH, strokeWidth=2, dash=[5, 4],
               join="round")
        # soft top-light on each patch
        d.path(f"M{x0t+4:.0f},{y0+8} L{x1t-4:.0f},{y0+8} L{x1b-6:.0f},{y0+20} "
               f"L{x0b+6:.0f},{y0+20} Z", f"Panel hi {ri+1}-{ci+1}",
               fill="#FFFFFF", opacity=7, stroke=NONE)
        tok = tokens.get((ri, ci))
        if tok:
            cx_ = (x0t + x1t + x0b + x1b) / 4
            cy_ = (y0 + y1) / 2 + 5
            t = d.text(tok, f"Token {ri+1}-{ci+1}", x=cx_, y=cy_, size=15,
                       font="Source Sans 3", color="#DAD6EA",
                       justify="center")
            if t and t.get("id"):
                ang = [-6, 5, -4, 6, -5, 4][pi % 6]
                d.cmd("object.rotate", f"token tilt {ri+1}-{ci+1}",
                      ids=[t["id"]], angle=ang, origin=[cx_, cy_])
                d.cmd("object.setProps", f"token fade {ri+1}-{ci+1}",
                      ids=[t["id"]], opacity=88)
        elif (ri + ci) % 2 == 0:
            # a darned X on the plain panels
            cx_ = (x0t + x1t + x0b + x1b) / 4
            cy_ = (y0 + y1) / 2
            d.path(f"M{cx_-7:.0f},{cy_-7:.0f} L{cx_+7:.0f},{cy_+7:.0f} "
                   f"M{cx_+7:.0f},{cy_-7:.0f} L{cx_-7:.0f},{cy_+7:.0f}",
                   f"Darn {ri+1}-{ci+1}", fill=NONE, stroke=STITCH,
                   strokeWidth=3, cap="round", opacity=60)
        pi += 1

# --- hood + face ----------------------------------------------------------------------
d.path("M352,404 C344,300 384,236 432,234 C484,232 520,302 510,404 "
       "C470,426 392,426 352,404 Z", "Hood",
       fill=HOOD_GRAD, stroke=INK, strokeWidth=6, join="round")
d.path("M368,392 C366,318 396,262 432,258", "Hood hi", fill=NONE,
       stroke="#8A94BC", strokeWidth=4, cap="round", opacity=55)
d.shape("ellipse", "Face void", x=376, y=282, width=112, height=118,
        fill="#171320", stroke=INK, strokeWidth=4)
# patch strap sweeps across where the other eye would be
d.path("M380,344 C412,332 468,328 492,340", "Patch strap", fill=NONE,
       stroke="#5A4E7E", strokeWidth=5, cap="round")
# the one good eye, softly glowing in the dark
d.shape("ellipse", "Eye halo", x=392, y=322, width=34, height=34,
        fill="#B8B4E0", opacity=25, stroke=NONE)
d.shape("ellipse", "Eye", x=399, y=328, width=20, height=22,
        fill="#DCD6F0", stroke=NONE)
d.shape("ellipse", "Pupil", x=404, y=333, width=10, height=12,
        fill="#1A1424", stroke=NONE)
d.shape("ellipse", "Eye glint", x=406, y=335, width=4, height=4,
        fill="#F2F0FA", stroke=NONE)
# the patch itself: the eye that saw the plugin stack loop
d.shape("ellipse", "Eye patch", x=438, y=316, width=38, height=42,
        fill="#0F0B14", stroke="#5A4E7E", strokeWidth=4)
d.shape("ellipse", "Patch sheen", x=444, y=322, width=14, height=10,
        fill="#4A4060", opacity=50, stroke=NONE)
# a resigned little mouth under the one remaining eye
d.path("M412,372 C420,377 430,377 438,371", "Mouth", fill=NONE,
       stroke="#6E6890", strokeWidth=3, cap="round", opacity=75)
# a sigh, escaping
t = d.text("…", "Sigh", x=516, y=292, size=22, font="Source Sans 3",
           color=CHALK, justify="center")
if t and t.get("id"):
    d.cmd("object.setProps", "sigh fade", ids=[t["id"]], opacity=45)

# --- sleeve + pencil ---------------------------------------------------------------
d.path("M498,448 C540,448 584,456 618,466 L612,498 C576,492 540,488 508,492 Z",
       "Sleeve", fill="#3A4462", stroke=INK, strokeWidth=5, join="round")
d.path("M520,462 L600,472", "Sleeve seam", fill=NONE, stroke=STITCH,
       strokeWidth=2.5, dash=[5, 4], opacity=70)
d.shape("ellipse", "Hand", x=600, y=464, width=34, height=32,
        fill="#262036", stroke=INK, strokeWidth=4)
# the pencil: ancient .tpl syntax delivery device
PX, PY, PA = 656, 452, -26
d.path(rot_rect_path(PX, PY, 74, 9, PA), "Pencil body",
       fill="#D8A83E", stroke=INK, strokeWidth=2.5)
tp0 = rp(PX, PY, PX + 37, PY - 4.5, PA)
tp1 = rp(PX, PY, PX + 50, PY, PA)
tp2 = rp(PX, PY, PX + 37, PY + 4.5, PA)
d.path(f"M{tp0[0]:.0f},{tp0[1]:.0f} L{tp1[0]:.0f},{tp1[1]:.0f} "
       f"L{tp2[0]:.0f},{tp2[1]:.0f} Z", "Pencil tip",
       fill="#E8D8B8", stroke=INK, strokeWidth=2.5, join="round")
gp = rp(PX, PY, PX + 47, PY, PA)
d.shape("ellipse", "Graphite", x=gp[0] - 3, y=gp[1] - 3, width=6, height=6,
        fill="#2A2630", stroke=NONE)
ex, ey = rp(PX, PY, PX - 40, PY, PA)
d.path(rot_rect_path(ex, ey, 10, 9, PA), "Eraser",
       fill="#C47A8A", stroke=INK, strokeWidth=2)

# --- captions ----------------------------------------------------------------------
d.text("PARSEY DRIFTCHART", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#E8E4F6", justify="center")
r = d.text("CUSTODIAN OF TIKIWIKI REALMS", "Role", x=500, y=968, size=22,
           font="Virelai Sans", color="#AAA6CE", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=160)

d.finish("063.parsey-driftchart-V1R00")
