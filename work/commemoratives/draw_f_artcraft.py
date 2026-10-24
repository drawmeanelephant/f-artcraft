#!/usr/bin/env python3
"""f-artcraft — commemorative plate V1R00. The Ouroboros Loop: the loop drawn
as a machine eating its own tail — a riveted ring of four stations (prompt,
build, proof, critique) around a hub holding Fart Knocker's filing cabinet
in miniature, one drawer open, and a pen nib drawing the circle it stands
on. 1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("f-artcraft — Commemorative Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#1E140C"              # warm dark, never pure black
BRASS = "#C8A45E"
CREAM = "#E8DCB8"

def on_disc(x, y, pad):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

def lin(c0, c1, start=None, end=None, extra=None):
    stops = [{"offset": 0, "color": c0}]
    if extra: stops += extra
    stops.append({"offset": 1, "color": c1})
    g = {"kind": "linear", "stops": stops}
    if start: g["start"], g["end"] = [round(v, 1) for v in start], [round(v, 1) for v in end]
    return {"gradient": g}

def rad(*stops):
    return {"gradient": {"kind": "radial", "stops": stops}}

def pol(r, deg, cx=PCX, cy=PCY):
    """Point on a circle r around the hub, deg measured with +y down."""
    t = math.radians(deg)
    return (cx + r * math.cos(t), cy + r * math.sin(t))

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin("#0E1416", "#040607", (500, 0), (500, 1000)), stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad({"offset": 0, "color": "#37443E"},
                 {"offset": 0.66, "color": "#1C2622"},
                 {"offset": 1, "color": "#0C1210"}),
        stroke="#8A7A4E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8C890", strokeWidth=3, opacity=24)
for i, (x, y, w) in enumerate([(214,238,4),(790,242,5),(160,466,4),(846,452,4),
                               (252,706,4),(744,736,5),(352,124,4),(648,118,4),
                               (150,606,3),(856,596,4),(436,810,3),(584,814,4)]):
    assert on_disc(x, y, 12)
    d.shape("ellipse", f"Fleck {i+1}", x=x-w/2, y=y-w/2, width=w, height=w,
            fill="#D8C890", opacity=16, stroke=NONE)

# --- the machine ring ----------------------------------------------------------
RB = 250                                   # band centerline radius
TAIL_DEG, HEAD_DEG = 233, 217              # the gap at top-left
tx, ty = pol(RB, TAIL_DEG)
hx, hy = pol(RB, HEAD_DEG)
# band: riveted belt, clockwise from the tail end around to the head end
d.path(f"M{tx:.1f},{ty:.1f} A{RB},{RB} 0 1 1 {hx:.1f},{hy:.1f}", "Band",
       fill=NONE, stroke=lin("#5E6E68", "#323E3A", (260, 240), (740, 700)),
       strokeWidth=42)
# band edge lines
for rr, lbl in ((RB + 21, "Band edge out"), (RB - 21, "Band edge in")):
    ex0, ey0 = pol(rr, TAIL_DEG)
    ex1, ey1 = pol(rr, HEAD_DEG)
    d.path(f"M{ex0:.1f},{ey0:.1f} A{rr},{rr} 0 1 1 {ex1:.1f},{ey1:.1f}", lbl,
           fill=NONE, stroke="#1E2824", strokeWidth=3, opacity=60)
# band highlight, upper run
hx2, hy2 = pol(RB - 12, 232)
hx3, hy3 = pol(RB - 12, 296)
d.path(f"M{hx2:.1f},{hy2:.1f} A{RB-12},{RB-12} 0 0 1 {hx3:.1f},{hy3:.1f}",
       "Band sheen", fill=NONE, stroke="#9AAEA6", strokeWidth=5,
       opacity=30, cap="round")
# rivets every 12 deg, skipping stations (0,90,180,270) and the gap
for i, adeg in enumerate(range(236, 578, 12)):
    a = adeg % 360
    if min(abs(a - s) for s in (0, 90, 180, 270)) < 14:
        continue
    x, y = pol(RB, a)
    d.shape("ellipse", f"Rivet {i+1}", x=x-3, y=y-3, width=6, height=6,
            fill=BRASS, opacity=65, stroke=NONE)

# flow chevrons between stations, pointing clockwise
for i, adeg in enumerate((315, 45, 135)):
    cx, cy = pol(RB, adeg)
    t = math.radians(adeg)
    ux, uy = -math.sin(t), math.cos(t)      # clockwise tangent
    nx, ny = -uy, ux
    tipx, tipy = cx + ux * 13, cy + uy * 13
    b1x, b1y = cx - ux * 9 + nx * 9, cy - uy * 9 + ny * 9
    b2x, b2y = cx - ux * 9 - nx * 9, cy - uy * 9 - ny * 9
    d.path(f"M{tipx:.0f},{tipy:.0f} L{b1x:.0f},{b1y:.0f} L{b2x:.0f},{b2y:.0f} Z",
           f"Flow arrow {i+1}", fill=BRASS, opacity=80, stroke=NONE)

# --- the head, biting back at the band's tail end ----------------------------------
HC = (303, 300)                            # head centre on the band's leading end
d.shape("ellipse", "Head", x=HC[0]-34, y=HC[1]-34, width=68, height=68,
        fill=lin("#5E6E68", "#2A3430", (HC[0]-20, HC[1]-30), (HC[0]+20, HC[1]+30)),
        stroke=INK, strokeWidth=4)
# mouth: a notch cut into the disc, opening toward the tail (dir ~-44 deg)
j1 = (HC[0] + 38 * math.cos(math.radians(-26)),
      HC[1] + 38 * math.sin(math.radians(-26)))
j2 = (HC[0] + 38 * math.cos(math.radians(-62)),
      HC[1] + 38 * math.sin(math.radians(-62)))
d.path(f"M{HC[0]},{HC[1]} L{j1[0]:.0f},{j1[1]:.0f} L{j2[0]:.0f},{j2[1]:.0f} Z",
       "Mouth", fill="#0A0F0E", stroke=NONE)
# jaw edge lines
d.path(f"M{HC[0]},{HC[1]} L{j1[0]:.0f},{j1[1]:.0f}", "Jaw upper", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.path(f"M{HC[0]},{HC[1]} L{j2[0]:.0f},{j2[1]:.0f}", "Jaw lower", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
# teeth on the jaws
for k, (ja, jr) in enumerate(((-33, 30), (-55, 30))):
    px = HC[0] + jr * math.cos(math.radians(ja))
    py = HC[1] + jr * math.sin(math.radians(ja))
    qx = HC[0] + (jr - 9) * math.cos(math.radians(ja - 8))
    qy = HC[1] + (jr - 9) * math.sin(math.radians(ja - 8))
    rx = HC[0] + (jr - 9) * math.cos(math.radians(ja + 8))
    ry = HC[1] + (jr - 9) * math.sin(math.radians(ja + 8))
    d.path(f"M{px:.0f},{py:.0f} L{qx:.0f},{qy:.0f} L{rx:.0f},{ry:.0f} Z",
           f"Tooth {k+1}", fill="#D8DCCE", stroke=NONE)
# the tail tip, reaching in between the jaws
apex = (HC[0] + 20 * math.cos(math.radians(-44)),
        HC[1] + 20 * math.sin(math.radians(-44)))
tdir = (apex[0] - tx, apex[1] - ty)
tl = math.hypot(*tdir)
pn = (-tdir[1] / tl, tdir[0] / tl)
b1 = (tx + pn[0] * 19, ty + pn[1] * 19)
b2 = (tx - pn[0] * 19, ty - pn[1] * 19)
d.path(f"M{apex[0]:.0f},{apex[1]:.0f} L{b1[0]:.0f},{b1[1]:.0f} "
       f"L{b2[0]:.0f},{b2[1]:.0f} Z", "Tail tip",
       fill=lin("#7A8A84", "#3A4642", (tx, ty), (apex[0], apex[1])),
       stroke=INK, strokeWidth=3)
# a brass rivet eye + plating seam
d.shape("ellipse", "Eye", x=HC[0]-13, y=HC[1]-20, width=16, height=16,
        fill=BRASS, stroke=INK, strokeWidth=2.5)
d.shape("ellipse", "Eye hole", x=HC[0]-8, y=HC[1]-15, width=6, height=6,
        fill="#141C18", stroke=NONE)
d.path(f"M{HC[0]-30},{HC[1]+16} Q{HC[0]},{HC[1]+26} {HC[0]+30},{HC[1]+16}",
       "Head seam", fill=NONE, stroke="#1E2824", strokeWidth=2.5, opacity=70)

# --- four station medallions on the ring --------------------------------------------
def medallion(deg, label):
    cx, cy = pol(RB, deg)
    d.shape("ellipse", f"{label} medallion", x=cx-46, y=cy-46, width=92, height=92,
            fill=rad({"offset": 0, "color": "#4E5E58"},
                     {"offset": 0.7, "color": "#2C3833"},
                     {"offset": 1, "color": "#1A2420"}),
            stroke=BRASS, strokeWidth=4)
    d.shape("ellipse", f"{label} ring", x=cx-36, y=cy-36, width=72, height=72,
            fill=NONE, stroke="#9AAEA6", strokeWidth=2, opacity=35)
    return cx, cy

def st_label(cx, cy, word):
    d.text(word, f"{word} tag", x=cx, y=cy + 30, size=9.5,
           font="Source Sans 3", color="#C8B88E", justify="center")

# PROMPT — top: a terminal chevron and cursor
cx, cy = medallion(270, "Prompt")
d.path(f"M{cx-16},{cy-16} L{cx-2},{cy-4} L{cx-16},{cy+8}", "Prompt chevron",
       fill=NONE, stroke=CREAM, strokeWidth=5, cap="round")
d.path(f"M{cx+2},{cy+8} L{cx+18},{cy+8}", "Prompt cursor", fill=NONE,
       stroke=CREAM, strokeWidth=5, cap="round")
st_label(cx, cy, "PROMPT")

# BUILD — right: a gear
cx, cy = medallion(0, "Build")
for k in range(8):
    a = k * 45
    gx, gy = cx + 16 * math.cos(math.radians(a)), cy + 16 * math.sin(math.radians(a))
    d.path(rot_rect_path(gx, gy, 9, 7, a + 90), f"Gear tooth {k+1}",
           fill=CREAM, opacity=90, stroke=NONE)
d.shape("ellipse", "Gear body", x=cx-14, y=cy-14, width=28, height=28,
        fill=CREAM, stroke=NONE)
d.shape("ellipse", "Gear hole", x=cx-6, y=cy-6, width=12, height=12,
        fill="#2C3833", stroke=NONE)
st_label(cx, cy, "BUILD")

# PROOF — bottom: a document with a check
cx, cy = medallion(90, "Proof")
d.path(f"M{cx-13},{cy-16} L{cx+8},{cy-16} L{cx+14},{cy-10} L{cx+14},{cy+10} "
       f"L{cx-13},{cy+10} Z", "Proof doc", fill=CREAM, opacity=92,
       stroke=NONE)
d.path(f"M{cx+8},{cy-16} L{cx+8},{cy-10} L{cx+14},{cy-10}", "Proof fold",
       fill=NONE, stroke="#2C3833", strokeWidth=2)
d.path(f"M{cx-8},{cy-2} L{cx-3},{cy+4} L{cx+8},{cy-8}", "Proof check",
       fill=NONE, stroke="#8A4E20", strokeWidth=4, cap="round")
st_label(cx, cy, "PROOF")

# CRITIQUE — left: the red pencil
cx, cy = medallion(180, "Critique")
d.path(rot_rect_path(cx - 2, cy - 4, 34, 10, -35), "Pencil body",
       fill=lin("#C0381E", "#7A1E0E", (cx - 18, cy - 16), (cx + 14, cy + 8)),
       stroke=INK, strokeWidth=2.5)
# tip: wood cone + graphite
p0 = (cx - 2 + 17 * math.cos(math.radians(-35)),
      cy - 4 + 17 * math.sin(math.radians(-35)))
d.path(f"M{p0[0]:.0f},{p0[1]-5:.0f} L{p0[0]+13:.0f},{p0[1]-1:.0f} "
       f"L{p0[0]:.0f},{p0[1]+5:.0f} Z", "Pencil wood",
       fill="#E8D8B0", stroke=INK, strokeWidth=2)
d.path(f"M{p0[0]+9:.0f},{p0[1]-2:.0f} L{p0[0]+13:.0f},{p0[1]-1:.0f} "
       f"L{p0[0]+9:.0f},{p0[1]+1:.0f} Z", "Graphite", fill="#2E2820",
       stroke=NONE)
st_label(cx, cy, "CRITIQUE")

# --- the hub: filing cabinet miniature + the nib drawing its circle -------------------
# shadow under hub
d.shape("ellipse", "Hub shadow", x=415, y=540, width=170, height=24,
        fill="#080D0B", opacity=55, stroke=NONE)
# ink circle being drawn around the cabinet: 300deg drawn, gap top-left
a0 = pol(100, 195); a1 = pol(100, 135)
d.path(f"M{a0[0]:.1f},{a0[1]:.1f} A100,100 0 1 1 {a1[0]:.1f},{a1[1]:.1f}",
       "Ink circle", fill=NONE, stroke="#201408", strokeWidth=5, cap="round")
# wet-ink sheen on a short fresh stretch near the nib
b0 = pol(100, 105); b1 = pol(100, 135)
d.path(f"M{b0[0]:.1f},{b0[1]:.1f} A100,100 0 0 1 {b1[0]:.1f},{b1[1]:.1f}",
       "Wet ink", fill=NONE, stroke="#5E4420", strokeWidth=3, opacity=60,
       cap="round")

# the cabinet: body, three drawers, middle one open and glowing
CX0, CX1, CY0, CY1 = 452, 548, 398, 536
d.path(f"M{CX0},{CY0+8} Q{CX0},{CY0} {CX0+10},{CY0} L{CX1-10},{CY0} "
       f"Q{CX1},{CY0} {CX1},{CY0+8} L{CX1},{CY1} L{CX0},{CY1} Z", "Cabinet",
       fill=lin("#5A684E", "#2A3224", (CX0, CY0), (CX1, CY1)),
       stroke=INK, strokeWidth=4)
d.shape("ellipse", "Cabinet sheen", x=458, y=402, width=30, height=128,
        fill="#FFFFFF", opacity=8, stroke=NONE)
# top drawer (closed)
d.path(f"M{CX0+9},{CY0+14} L{CX1-9},{CY0+14} L{CX1-9},{CY0+52} L{CX0+9},{CY0+52} Z",
       "Drawer top", fill=lin("#66755A", "#38412E", (CX0, CY0+14), (CX1, CY0+52)),
       stroke="#1E2418", strokeWidth=2.5)
# bottom drawer (closed)
d.path(f"M{CX0+9},{CY0+98} L{CX1-9},{CY0+98} L{CX1-9},{CY1-12} L{CX0+9},{CY1-12} Z",
       "Drawer bottom", fill=lin("#66755A", "#38412E", (CX0, CY0+98), (CX1, CY1-12)),
       stroke="#1E2418", strokeWidth=2.5)
# middle drawer: open — glowing slot + pulled-out front below
d.path(f"M{CX0+9},{CY0+58} L{CX1-9},{CY0+58} L{CX1-9},{CY0+92} L{CX0+9},{CY0+92} Z",
       "Open slot", fill="#10150C", stroke="#1E2418", strokeWidth=2.5)
d.shape("ellipse", "Drawer glow", x=CX0+16, y=CY0+60, width=64, height=30,
        fill=rad({"offset": 0, "color": "#FFC878", "opacity": 0.5},
                 {"offset": 1, "color": "#FFC878", "opacity": 0}), stroke=NONE)
# papers peeking from the slot
d.path(f"M{CX0+26},{CY0+88} L{CX0+30},{CY0+68} L{CX0+44},{CY0+72} "
       f"L{CX0+40},{CY0+88} Z", "Paper 1", fill="#E8DCB8", opacity=90,
       stroke="#8A7A5A", strokeWidth=1.5)
d.path(f"M{CX0+52},{CY0+88} L{CX0+50},{CY0+70} L{CX0+62},{CY0+66} "
       f"L{CX0+64},{CY0+88} Z", "Paper 2", fill="#D8CCAA", opacity=90,
       stroke="#8A7A5A", strokeWidth=1.5)
# the pulled drawer front, swung down-out
d.path(f"M{CX0+15},{CY0+94} L{CX1-15},{CY0+94} L{CX1-21},{CY0+120} "
       f"L{CX0+21},{CY0+120} Z", "Drawer front",
       fill=lin("#5C6A50", "#303A28", (CX0, CY0+94), (CX1, CY0+120)),
       stroke=INK, strokeWidth=3)
# drawer pulls
for i, yy in enumerate((CY0+33, CY0+107)):
    d.shape("rectangle", f"Pull {i+1}", x=CX0+40, y=yy, width=16, height=6,
            fill=BRASS, stroke="#4E3E18", strokeWidth=1.5)
d.shape("rectangle", "Pull open", x=CX0+44, y=CY0+104, width=16, height=6,
        fill=BRASS, stroke="#4E3E18", strokeWidth=1.5)
# tiny label frame on the top drawer: the commit log
d.shape("rectangle", "Label frame", x=CX0+34, y=CY0+20, width=28, height=12,
        fill="#D8CCAA", opacity=80, stroke="#4E3E18", strokeWidth=1.5)
d.text("LOG", "Drawer label", x=CX0+48, y=CY0+29, size=7,
       font="Source Sans 3", color="#3A2E14", justify="center")
# feet
d.shape("rectangle", "Foot L", x=CX0+8, y=CY1, width=16, height=10, fill="#232B1E",
        stroke=INK, strokeWidth=2)
d.shape("rectangle", "Foot R", x=CX1-24, y=CY1, width=16, height=10, fill="#232B1E",
        stroke=INK, strokeWidth=2)

# --- the pen nib, standing on the ink circle it is drawing ----------------------------
TIP = pol(100, 135)                       # nib tip rests on the arc's end
tt = math.radians(135)
ux, uy = -math.sin(tt), math.cos(tt)      # nib extends along the draw tangent
nx, ny = -uy, ux
def np_(dist, off):
    return (TIP[0] + ux * dist + nx * off, TIP[1] + uy * dist + ny * off)
p_l = np_(30, 10); p_r = np_(30, -10)
s_l = np_(44, 12); s_r = np_(44, -12)
tail = np_(56, 0)
d.path(f"M{TIP[0]:.0f},{TIP[1]:.0f} L{p_l[0]:.0f},{p_l[1]:.0f} "
       f"Q{s_l[0]:.0f},{s_l[1]:.0f} {tail[0]:.0f},{tail[1]:.0f} "
       f"Q{s_r[0]:.0f},{s_r[1]:.0f} {p_r[0]:.0f},{p_r[1]:.0f} Z", "Pen nib",
       fill=lin("#E8C860", "#A8802E", (TIP[0], TIP[1]), (tail[0], tail[1]),
                extra=[{"offset": 0.55, "color": "#F0D878"}]),
       stroke=INK, strokeWidth=3)
# slit + breather hole
sl = np_(30, 0)
d.path(f"M{TIP[0]:.0f},{TIP[1]:.0f} L{sl[0]:.0f},{sl[1]:.0f}", "Nib slit",
       fill=NONE, stroke="#5E4410", strokeWidth=2.5)
bh = np_(36, 0)
d.shape("ellipse", "Breather", x=bh[0]-3.5, y=bh[1]-3.5, width=7, height=7,
        fill="#5E4410", stroke=NONE)
# a wet blob of ink right at the tip
d.shape("ellipse", "Ink blob", x=TIP[0]-4, y=TIP[1]-4, width=8, height=8,
        fill="#201408", opacity=85, stroke=NONE)

# --- name + role ------------------------------------------------------------------
d.text("F-ARTCRAFT", "Name", x=500, y=930, size=58, font="Virelai Sans",
       color="#E4E8D8", justify="center")
LINE2, SZ2, TRK = "PROMPT BUILD PROOF CRITIQUE", 22, 260
r = d.text(LINE2, "Second line", x=500, y=968, size=SZ2, font="Virelai Sans",
           color="#C8A45E", justify="center")
d.cmd("text.setStyle", "Second line tracking", ids=[r["id"]], tracking=TRK)
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

d.finish("f-artcraft-V1R00")
