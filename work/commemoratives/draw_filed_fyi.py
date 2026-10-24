#!/usr/bin/env python3
"""filed-fyi — commemorative plate V1R00. The Archive Cathedral: a filing
cabinet built like a cathedral — drawer upon drawer rising in gothic bays
toward a rose window, one drawer near the bottom open and glowing, the
banner bunny very small at the great west door. Stone and lamplight.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("filed-fyi — Commemorative Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#1A130C"              # warm dark, never pure black
STONE_HI = "#8A8272"
STONE_LO = "#3E382C"
GLASS_A = "#C8862E"          # amber glass
GLASS_B = "#9A3A22"          # deep red glass
LAMP = "#FFC878"

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

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin("#101318", "#050608", (500, 0), (500, 1000)), stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad({"offset": 0, "color": "#3A3E44"},
                 {"offset": 0.64, "color": "#1E2226"},
                 {"offset": 1, "color": "#0C0E11"}),
        stroke="#7A7258", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D0C49A", strokeWidth=3, opacity=24)
# night sky: stars and a thin moon high left
d.shape("ellipse", "Moon", x=232, y=150, width=52, height=52,
        fill=rad({"offset": 0, "color": "#E0D6B8"},
                 {"offset": 1, "color": "#9A906E"}), opacity=75, stroke=NONE)
d.shape("ellipse", "Moon halo", x=200, y=118, width=116, height=116,
        fill=rad({"offset": 0, "color": "#E0D6B8", "opacity": 0.14},
                 {"offset": 1, "color": "#E0D6B8", "opacity": 0}), stroke=NONE)
for i, (x, y, w) in enumerate([(330,110,3.4),(420,140,2.6),(640,120,3.4),(740,190,3),
                               (820,300,3),(170,330,2.8),(850,470,3),(160,520,3),
                               (240,700,3),(780,690,3.4),(620,810,2.8),(400,820,3)]):
    assert on_disc(x, y, 12)
    d.shape("ellipse", f"Star {i+1}", x=x-w/2, y=y-w/2, width=w, height=w,
            fill="#D8D0B0", opacity=40, stroke=NONE)

# --- ground: dark floor closing on the disc arc -----------------------------------
d.path("M206.1,762 Q500,668 793.9,762 A420,420 0 0 1 206.1,762 Z", "Ground",
       fill=lin("#221E16", "#0C0A06", (500, 700), (500, 880)), stroke=NONE)
d.shape("ellipse", "Cathedral shadow", x=330, y=706, width=340, height=26,
        fill="#060504", opacity=55, stroke=NONE)

# --- the cathedral of drawers ----------------------------------------------------
# facade block
FX0, FX1, FY0, FY1 = 384, 616, 340, 706
d.path(f"M{FX0},{FY0} L{FX1},{FY0} L{FX1},{FY1} L{FX0},{FY1} Z", "Facade",
       fill=lin(STONE_HI, STONE_LO, (500, FY0), (500, FY1),
                extra=[{"offset": 0.45, "color": "#6E6858"}]),
       stroke=INK, strokeWidth=5)
# gable above the facade
d.path(f"M{FX0-6},{FY0+2} L500,212 L{FX1+6},{FY0+2} Z", "Gable",
       fill=lin("#7A7260", "#3E382C", (500, 212), (500, FY0)),
       stroke=INK, strokeWidth=5)
# gable edge trim
d.path(f"M{FX0-6},{FY0+2} L500,212 L{FX1+6},{FY0+2}", "Gable trim",
       fill=NONE, stroke="#B0A888", strokeWidth=3, opacity=50)
# finial on the gable point
d.path("M500,212 L500,192", "Spire", fill=NONE, stroke="#B0A888",
       strokeWidth=4, cap="round")
d.shape("ellipse", "Spire finial", x=496, y=184, width=8, height=8,
        fill="#B0A888", stroke=NONE)

# side towers with pinnacle caps
for side, (tx0, tx1) in (("L", (332, 380)), ("R", (620, 668))):
    d.path(f"M{tx0},330 L{tx1},330 L{tx1},706 L{tx0},706 Z", f"Tower {side}",
           fill=lin("#6E6858", "#362F24", (tx0, 330), (tx1, 706)),
           stroke=INK, strokeWidth=4)
    # pinnacle: sloped cap + ball
    mxt = (tx0 + tx1) / 2
    d.path(f"M{tx0-4},332 L{mxt},296 L{tx1+4},332 Z", f"Pinnacle {side}",
           fill=lin("#7A7260", "#3E382C", (mxt, 296), (mxt, 332)),
           stroke=INK, strokeWidth=4)
    d.shape("ellipse", f"Finial {side}", x=mxt-5, y=288, width=10, height=10,
            fill="#B0A888", stroke=INK, strokeWidth=2)

# --- the drawer grid: bays of little drawer fronts --------------------------------
# main facade: 3 bays x 3 columns of drawers, rows rising to the rose window
DW, DH, DG = 22, 17, 3
cols0 = FX0 + 12
drawer_cols = 8
drawer_rows = 14
top = 372
skip = {(c, r) for c in (2, 3, 4, 5) for r in (11, 12, 13)}   # behind the west door
open_cell = (1, 10)                       # one drawer open + glowing
n = 0
for r_i in range(drawer_rows):
    for c_i in range(drawer_cols):
        if (c_i, r_i) in skip:
            continue
        x = cols0 + c_i * (DW + DG)
        y = top + r_i * (DH + DG)
        if (c_i, r_i) == open_cell:
            continue                     # drawn separately below
        n += 1
        tone = "#6E6858" if (r_i + c_i) % 2 else "#625C4C"
        d.shape("rectangle", f"Drawer {n}", x=x, y=y, width=DW, height=DH,
                fill=tone, stroke="#2E2A20", strokeWidth=1.5, opacity=92)
        if (r_i * drawer_cols + c_i) % 3 == 0:
            d.shape("ellipse", f"Pull {n}", x=x+DW/2-1.5, y=y+DH/2-1.5,
                    width=3, height=3, fill="#B0A888", opacity=70, stroke=NONE)
# tower drawers: 2 columns each
for side, tx0 in (("L", 332), ("R", 620)):
    for r_i in range(8):
        for c_i in range(2):
            x = tx0 + 8 + c_i * 18
            y = 348 + r_i * 24
            d.shape("rectangle", f"Tower {side} dr {r_i}{c_i}", x=x, y=y,
                    width=15, height=20, fill="#5E5848" if (r_i + c_i) % 2 else "#544E3E",
                    stroke="#2E2A20", strokeWidth=1.5, opacity=92)
# bay pilasters dividing the grid
for i, x in enumerate((FX0 + 6, 469.5, 544.5, FX1 - 6)):
    d.path(f"M{x},{FY0+8} L{x},{FY1-6}", f"Pilaster {i+1}", fill=NONE,
           stroke="#4A4436", strokeWidth=4, opacity=80)
    d.path(f"M{x-1},{FY0+8} L{x-1},{FY1-6}", f"Pilaster lit {i+1}", fill=NONE,
           stroke="#8A8272", strokeWidth=1.5, opacity=45)
# pilaster capitals: little pointed arches at the top of each bay
for i, x in enumerate((430, 508, 584)):
    d.path(f"M{x-34},{top-6} Q{x},{top-30} {x+34},{top-6}", f"Bay arch {i+1}",
           fill=NONE, stroke="#4A4436", strokeWidth=3, opacity=70)

# --- the rose window -----------------------------------------------------------------
RX, RY, RR = 500, 318, 46
d.shape("ellipse", "Rose glow", x=RX-80, y=RY-80, width=160, height=160,
        fill=rad({"offset": 0, "color": "#D89A4E", "opacity": 0.18},
                 {"offset": 1, "color": "#D89A4E", "opacity": 0}), stroke=NONE)
d.shape("ellipse", "Rose rim", x=RX-RR, y=RY-RR, width=RR*2, height=RR*2,
        fill=rad({"offset": 0, "color": "#4A4438"},
                 {"offset": 1, "color": "#2A261E"}),
        stroke="#B0A888", strokeWidth=4)
# glass petals: alternating amber/red wedges between spokes
for k in range(8):
    a = math.radians(k * 45 - 90)
    px, py = RX + 26 * math.cos(a), RY + 26 * math.sin(a)
    d.shape("ellipse", f"Petal {k+1}", x=px-11, y=py-11, width=22, height=22,
            fill=rad({"offset": 0, "color": GLASS_A if k % 2 else GLASS_B},
                     {"offset": 1, "color": "#5E2E14"}),
            opacity=85, stroke="#241E14", strokeWidth=2)
# tracery spokes
for k in range(8):
    a = math.radians(k * 45 - 90 + 22.5)
    d.path(f"M{RX:.0f},{RY:.0f} L{RX + 42*math.cos(a):.0f},{RY + 42*math.sin(a):.0f}",
           f"Spoke {k+1}", fill=NONE, stroke="#241E14", strokeWidth=4)
# hub
d.shape("ellipse", "Rose hub", x=RX-10, y=RY-10, width=20, height=20,
        fill=rad({"offset": 0, "color": "#E8C878"},
                 {"offset": 1, "color": "#8A5A22"}),
        stroke="#241E14", strokeWidth=3)
# inner ring line
d.shape("ellipse", "Rose inner", x=RX-33, y=RY-33, width=66, height=66,
        fill=NONE, stroke="#241E14", strokeWidth=3, opacity=70)

# --- the open drawer, low left, glowing -----------------------------------------------
odx, ody = cols0 + open_cell[0] * (DW + DG), top + open_cell[1] * (DH + DG)
# light spill on the stone around it
d.shape("ellipse", "Drawer halo", x=odx-40, y=ody-30, width=110, height=90,
        fill=rad({"offset": 0, "color": LAMP, "opacity": 0.28},
                 {"offset": 1, "color": LAMP, "opacity": 0}), stroke=NONE)
# dark slot
d.shape("rectangle", "Open slot", x=odx, y=ody, width=DW, height=DH,
        fill="#12100A", stroke="#2E2A20", strokeWidth=1.5)
d.shape("rectangle", "Slot glow", x=odx+3, y=ody+4, width=DW-6, height=DH-8,
        fill=rad({"offset": 0, "color": LAMP, "opacity": 0.55},
                 {"offset": 1, "color": LAMP, "opacity": 0.1}), stroke=NONE)
# pulled-out drawer front, dropped forward and down
d.shape("rectangle", "Open drawer front", x=odx-4, y=ody+DH+5, width=DW+8,
        height=12,
        fill=lin("#7A7260", "#4A4436", (odx, ody+DH+5), (odx, ody+DH+17)),
        stroke=INK, strokeWidth=2)
d.shape("ellipse", "Open pull", x=odx+DW/2-2, y=ody+DH+8, width=4, height=4,
        fill="#D8CC9A", stroke=NONE)
# a slip of paper catching the light
d.path(f"M{odx+12},{ody+2} L{odx+17},{ody-8} L{odx+21},{ody+2} Z",
       "Lit paper", fill="#F4E4B8", opacity=95, stroke="#8A7A4E",
       strokeWidth=1)

# --- the great west door + the banner bunny, very small ------------------------------
DX0, DX1, DY = 466, 534, 706
d.path(f"M{DX0},{DY} L{DX0},652 Q{DX0},616 500,604 Q{DX1},616 {DX1},652 "
       f"L{DX1},{DY} Z", "West door",
       fill=lin("#1A1408", "#0A0804", (500, 604), (500, 706)),
       stroke="#B0A888", strokeWidth=4)
# lantern glow inside the door
d.shape("ellipse", "Door glow", x=472, y=636, width=56, height=64,
        fill=rad({"offset": 0, "color": LAMP, "opacity": 0.34},
                 {"offset": 1, "color": LAMP, "opacity": 0}), stroke=NONE)
# door tracery: a second inner arch
d.path(f"M{DX0+8},{DY} L{DX0+8},654 Q{DX0+8},626 500,616 Q{DX1-8},626 {DX1-8},654 "
       f"L{DX1-8},{DY}", "Door inner arch", fill=NONE, stroke="#5E5848",
       strokeWidth=2.5, opacity=70)
# engraved lintel: the drawer count in roman numerals
d.text("MMDLII", "Lintel", x=500, y=600, size=9, font="Source Sans 3",
       color="#B0A888", justify="center")

# the banner bunny at the threshold — silhouette, ~28px tall
BX = 500
d.shape("ellipse", "Bunny body", x=BX-8, y=676, width=16, height=22,
        fill="#0E0A06", stroke="#B0A888", strokeWidth=1.5)
d.shape("ellipse", "Bunny head", x=BX-6, y=666, width=12, height=12,
        fill="#0E0A06", stroke="#B0A888", strokeWidth=1.5)
# ears
d.path(f"M{BX-5},668 Q{BX-8},650 {BX-5},646 Q{BX-1},650 {BX-2},668 Z",
       "Ear L", fill="#0E0A06", stroke="#B0A888", strokeWidth=1.5)
d.path(f"M{BX+5},668 Q{BX+8},652 {BX+5},648 Q{BX+1},652 {BX+2},668 Z",
       "Ear R", fill="#0E0A06", stroke="#B0A888", strokeWidth=1.5)
# lit rim on the bunny's left flank (door lamp)
d.path(f"M{BX-8},684 Q{BX-9},690 {BX-7},696", "Bunny rim", fill=NONE,
       stroke=LAMP, strokeWidth=2, opacity=70, cap="round")
# doorstep
d.shape("rectangle", "Doorstep", x=DX0-10, y=706, width=88, height=8,
        fill="#4A4436", stroke=INK, strokeWidth=2)

# lamplight wash low across the facade
d.shape("ellipse", "Lamp wash", x=400, y=560, width=200, height=150,
        fill=rad({"offset": 0, "color": LAMP, "opacity": 0.10},
                 {"offset": 1, "color": LAMP, "opacity": 0}), stroke=NONE)

# --- name + role ------------------------------------------------------------------
d.text("FILED.FYI", "Name", x=500, y=930, size=60, font="Virelai Sans",
       color="#E4DCC0", justify="center")
LINE2, SZ2, TRK = "FILED & FORGOTTEN ARCHIVE", 23, 260
r = d.text(LINE2, "Second line", x=500, y=968, size=SZ2, font="Virelai Sans",
           color="#B09A62", justify="center")
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

d.finish("filed-fyi-V1R00")
