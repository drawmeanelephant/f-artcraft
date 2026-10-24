#!/usr/bin/env python3
"""solipsist — commemorative plate V1R00. The Three-Pane Reader: a solitary
figure at a writing desk inside a three-pane mail window — mailboxes
stacked left, a reading lamp in the middle pane, an inspector drawer ajar
at right. Radio UserLand's ghost in Mail's body. Lamp gold and midnight
blue; one reader, one harness. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("solipsist — Commemorative Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#0A0F18"   # warm dark, never pure black

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

def rrect(x, y, w, h, r):
    return (f"M{x+r},{y} L{x+w-r},{y} Q{x+w},{y} {x+w},{y+r} "
            f"L{x+w},{y+h-r} Q{x+w},{y+h} {x+w-r},{y+h} "
            f"L{x+r},{y+h} Q{x},{y+h} {x},{y+h-r} "
            f"L{x},{y+r} Q{x},{y} {x+r},{y} Z")

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin("#0E1522", "#04060C", (500, 0), (500, 1000)), stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad({"offset": 0, "color": "#26334A"},
                 {"offset": 0.68, "color": "#131D2E"},
                 {"offset": 1, "color": "#080D16"}),
        stroke="#6E7FA0", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8D2C0", strokeWidth=3, opacity=26)
# night dust
for i, (x, y, w, o) in enumerate([(216,206,4,22),(792,202,5,22),(164,448,4,20),
                                  (846,424,4,20),(250,746,4,18),(736,780,5,18),
                                  (350,110,3,22),(652,106,4,20),(142,598,3,18),
                                  (858,588,4,18)]):
    assert on_disc(x, y, 12)
    d.shape("ellipse", f"Dust {i+1}", x=x-w/2, y=y-w/2, width=w, height=w,
            fill="#D8D2C0", opacity=o, stroke=NONE)
# lamplight ambience in the disc
d.shape("ellipse", "Lamp ambience", x=330, y=330, width=400, height=420,
        fill=rad({"offset": 0, "color": "#F0C060", "opacity": 0.10},
                 {"offset": 1, "color": "#F0C060", "opacity": 0}), stroke=NONE)

# --- the floor the window floats over, closing on the disc's arc -----------------
d.path("M206.1,770 Q500,700 793.9,770 A420,420 0 0 1 206.1,770 Z", "Floor",
       fill=lin("#141B28", "#06090F", (500, 710), (500, 880)), stroke=NONE)
d.shape("ellipse", "Window shadow", x=280, y=740, width=440, height=50,
        fill=rad({"offset": 0, "color": "#000000", "opacity": 0.5},
                 {"offset": 1, "color": "#000000", "opacity": 0}), stroke=NONE)

# --- the three-pane window ----------------------------------------------------------
WX0, WY0, WX1, WY1 = 236, 196, 764, 712        # window frame
LPX = 366                                       # left pane edge
DPX = 600                                       # drawer (right pane) left edge
# frame
d.path(rrect(WX0, WY0, WX1-WX0, WY1-WY0, 14), "Window frame",
       fill=lin("#1A2434", "#0C1220", (WX0, WY0), (WX0, WY1)),
       stroke=INK, strokeWidth=5)
# title bar
d.path(rrect(WX0+3, WY0+3, WX1-WX0-6, 30, 11), "Title bar",
       fill=lin("#2A3850", "#1C2740", (WX0, WY0), (WX0, WY0+33)), stroke=NONE)
d.text("solipsist — Inbox (1 unread)", "Window title", x=(WX0+WX1)/2, y=WY0+21,
       size=11, font="Source Sans 3", color="#8FA0BC", justify="center")
for i, (cx, c) in enumerate([(WX0+20, "#8A4A44"), (WX0+38, "#8A7440"),
                             (WX0+56, "#4A7A50")]):
    d.shape("ellipse", f"Traffic {i+1}", x=cx-5, y=WY0+11, width=10, height=10,
            fill=rad({"offset": 0, "color": c}, {"offset": 1, "color": INK}),
            stroke=INK, strokeWidth=1.5)

PANE_TOP, PANE_BOT = WY0+36, WY1-8

# === left pane: stacked mailboxes ==============================================
d.path(f"M{WX0+4},{PANE_TOP} L{LPX},{PANE_TOP} L{LPX},{PANE_BOT} "
       f"L{WX0+4},{PANE_BOT} Z", "Mailbox pane",
       fill=lin("#162034", "#0E1626", (WX0, PANE_TOP), (WX0, PANE_BOT)),
       stroke=NONE)
ROWS = [("INBOX", 64, True), ("Sent", 56, False), ("Drafts", 66, False),
        ("Junk", 48, False), ("Trash", 54, False), ("Archive", 68, False),
        ("On This Day", 62, False), ("Outbox", 52, False)]
ry = PANE_TOP + 14
for i, (label, lw, sel) in enumerate(ROWS):
    if sel:
        d.path(rrect(WX0+10, ry-6, LPX-WX0-24, 36, 8), "Selected row",
               fill=lin("#33436A", "#263452", (WX0, ry), (WX0, ry+30)),
               stroke="#4A5E8A", strokeWidth=1.5)
    # inbox-tray icon
    ix = WX0 + 22
    d.path(f"M{ix},{ry+4} L{ix+20},{ry+4} L{ix+18},{ry+16} L{ix+2},{ry+16} Z",
           f"Tray {i+1}", fill=NONE, stroke="#8FA0BC", strokeWidth=2.5,
           opacity=90 if sel else 55)
    d.path(f"M{ix+6},{ry+9} L{ix+9},{ry+13} L{ix+11},{ry+13} L{ix+14},{ry+9}",
           f"Tray notch {i+1}", fill=NONE, stroke="#8FA0BC", strokeWidth=2,
           opacity=90 if sel else 55)
    # label lines (glyphs, not real text — keeps the pane quiet)
    d.path(f"M{ix+30},{ry+7} L{ix+30+lw},{ry+7}", f"Label {i+1}", fill=NONE,
           stroke="#C8D4E8" if sel else "#5E6E8A", strokeWidth=4,
           opacity=95 if sel else 55, cap="round")
    d.path(f"M{ix+30},{ry+16} L{ix+30+lw*0.55},{ry+16}", f"Sub {i+1}",
           fill=NONE, stroke="#5E6E8A", strokeWidth=3, opacity=40, cap="round")
    ry += 44
# RSS arcs — the UserLand ghost — bottom of the mailbox list
rx, ryy = WX0+26, ry+16
d.shape("ellipse", "RSS dot", x=rx-3, y=ryy+8, width=7, height=7,
        fill="#D8904A", opacity=80, stroke=NONE)
for i, rr in enumerate((10, 18)):
    d.path(f"M{rx},{ryy+11-rr} A{rr},{rr} 0 0 1 {rx+rr},{ryy+11}",
           f"RSS arc {i+1}", fill=NONE, stroke="#D8904A", strokeWidth=3,
           opacity=70, cap="round")
d.path(f"M{rx+30},{ryy+4} L{rx+92},{ryy+4}", "RSS label", fill=NONE,
       stroke="#5E6E8A", strokeWidth=4, opacity=45, cap="round")
# pane divider hairline
d.path(f"M{LPX},{PANE_TOP} L{LPX},{PANE_BOT}", "Divider L", fill=NONE,
       stroke="#05080E", strokeWidth=3)

# === middle pane: the reading room ==============================================
MPX0, MPX1 = LPX+2, DPX-4
d.path(f"M{MPX0},{PANE_TOP} L{MPX1},{PANE_TOP} L{MPX1},{PANE_BOT} "
       f"L{MPX0},{PANE_BOT} Z", "Reading pane",
       fill=lin("#0E1626", "#080D18", (MPX0, PANE_TOP), (MPX0, PANE_BOT)),
       stroke=NONE)
# the letter being read, dim and huge in the dark of the pane
ex0, ey0, ex1, ey1 = MPX0+52, PANE_TOP+38, MPX1-52, PANE_TOP+98
d.path(f"M{ex0},{ey0} L{ex1},{ey0} L{ex1},{ey1} L{ex0},{ey1} Z", "Big letter",
       fill="#1C2A44", opacity=60, stroke="#5E6E8A", strokeWidth=2.5)
d.path(f"M{ex0},{ey0} L{(ex0+ex1)/2},{(ey0+ey1)/2+6} L{ex1},{ey0}",
       "Letter flap", fill=NONE, stroke="#5E6E8A", strokeWidth=2.5, opacity=70)
for j in range(3):
    d.path(f"M{ex0+12},{ey1-14-j*9} L{ex1-12},{ey1-14-j*9}", f"Letter line {j+1}",
           fill=NONE, stroke="#5E6E8A", strokeWidth=2, opacity=35, cap="round")

# desk surface across the lower middle pane
d.path(f"M{MPX0+10},628 L{MPX1-10},628 L{MPX1-6},{PANE_BOT-8} "
       f"L{MPX0+6},{PANE_BOT-8} Z", "Desk",
       fill=lin("#2A2118", "#14100A", (MPX0, 628), (MPX0, PANE_BOT-8)),
       stroke=INK, strokeWidth=3)
d.path(f"M{MPX0+10},628 L{MPX1-10},628", "Desk edge", fill=NONE,
       stroke="#4A3A26", strokeWidth=3, opacity=70, cap="round")

# the desk lamp, left of the reader
lx, ly = MPX0+44, 622                       # lamp base point on desk
d.shape("ellipse", "Lamp base", x=lx-16, y=ly-8, width=32, height=12,
        fill=lin("#3A4456", "#161C28", (lx-16, ly-8), (lx+16, ly+4)),
        stroke=INK, strokeWidth=2.5)
d.path(f"M{lx},516 L{lx-4},{ly-6}", "Lamp stem", fill=NONE,
       stroke="#3A4456", strokeWidth=5, cap="round")
d.path(f"M{lx},516 L{lx+26},500", "Lamp arm", fill=NONE,
       stroke="#3A4456", strokeWidth=5, cap="round")
# shade: tilted trapezoid pouring light down-right
d.path(f"M{lx+16},498 L{lx+52},488 L{lx+58},508 L{lx+24},516 Z", "Lamp shade",
       fill=lin("#4A5670", "#1E2636", (lx+16, 488), (lx+58, 516)),
       stroke=INK, strokeWidth=3)
d.shape("ellipse", "Bulb", x=lx+40, y=504, width=10, height=10,
        fill=rad({"offset": 0, "color": "#FFE8B0"},
                 {"offset": 1, "color": "#D8904A"}), stroke=NONE)
# the light cone onto the desk and the letter on it
d.path(f"M{lx+44},510 L{MPX1-40},628 L{lx+2},628 Z", "Light cone",
       fill=rad({"offset": 0, "color": "#F0C060", "opacity": 0.30},
                 {"offset": 1, "color": "#F0C060", "opacity": 0.04}),
       stroke=NONE)
d.shape("ellipse", "Lamp halo", x=lx+18, y=486, width=58, height=50,
        fill=rad({"offset": 0, "color": "#FFE8B0", "opacity": 0.45},
                 {"offset": 1, "color": "#FFE8B0", "opacity": 0}), stroke=NONE)
# warm pool on the desk
d.shape("ellipse", "Desk pool", x=lx-8, y=616, width=150, height=20,
        fill=rad({"offset": 0, "color": "#F0C060", "opacity": 0.35},
                 {"offset": 1, "color": "#F0C060", "opacity": 0}), stroke=NONE)
# the letter on the desk, lit
d.path("M498,614 L556,608 L560,624 L502,630 Z", "Desk letter",
       fill=lin("#F0E8D4", "#C8B894", (498, 608), (560, 630)),
       stroke="#8A7A5A", strokeWidth=2)
for j in range(2):
    d.path(f"M{508+j*4},{616+j*5} L{548-j*4},{612+j*5}", f"Desk letter line {j+1}",
           fill=NONE, stroke="#8A7A5A", strokeWidth=1.8, opacity=70, cap="round")

# the solitary reader: silhouette at the desk, facing the lamp
fx = MPX1-58
d.path(f"M{fx-26},660 C{fx-30},612 {fx-22},576 {fx},570 "
       f"C{fx+22},576 {fx+30},612 {fx+28},660 Z", "Reader body",
       fill=lin("#1A2434", "#0A0F18", (fx, 570), (fx, 660)),
       stroke=INK, strokeWidth=3)
d.shape("ellipse", "Reader head", x=fx-15, y=536, width=30, height=34,
        fill=lin("#20293C", "#0E1420", (fx-15, 536), (fx+15, 570)),
        stroke=INK, strokeWidth=3)
# lamplight rim on the reader's turned cheek and shoulder
d.path(f"M{fx-14},550 C{fx-16},556 {fx-14},562 {fx-10},566", "Face rim",
       fill=NONE, stroke="#F0C060", strokeWidth=3, opacity=65, cap="round")
d.path(f"M{fx-24},586 C{fx-27},600 {fx-28},616 {fx-28},632", "Shoulder rim",
       fill=NONE, stroke="#F0C060", strokeWidth=3, opacity=45, cap="round")
# the writing arm reaching to the letter
d.path(f"M{fx-20},596 C{fx-36},604 {fx-52},612 {fx-66},616", "Reader arm",
       fill=NONE, stroke="#141C2A", strokeWidth=9, cap="round")
d.path(f"M{fx-20},594 C{fx-36},602 {fx-50},610 {fx-63},614", "Arm rim",
       fill=NONE, stroke="#F0C060", strokeWidth=2.5, opacity=40, cap="round")
# pen nib as one gold tick
d.path(f"M{fx-66},616 L{fx-72},622", "Pen", fill=NONE,
       stroke="#F0C060", strokeWidth=3, opacity=80, cap="round")

# === right: the inspector drawer, ajar ===========================================
# dark slot the drawer slides in
d.path(f"M{DPX-8},{PANE_TOP+8} L{DPX},{PANE_TOP+8} L{DPX},{PANE_BOT-8} "
       f"L{DPX-8},{PANE_BOT-8} Z", "Drawer slot", fill="#05080E", stroke=NONE)
# drawer body pulled out of the right edge of the window
DRX0, DRX1, DRY0, DRY1 = DPX, 762, PANE_TOP+10, PANE_BOT-10
d.path(f"M{DPX-14},{DRY0+6} L{DRX0},{DRY0} L{DRX1},{DRY0} L{DRX1},{DRY1} "
       f"L{DPX-14},{DRY1-6} Z", "Drawer shadow", fill="#04060A",
       opacity=70, stroke=NONE)
d.path(rrect(DRX0, DRY0, DRX1-DRX0, DRY1-DRY0, 8), "Inspector drawer",
       fill=lin("#1E2A40", "#101828", (DRX0, DRY0), (DRX1, DRY1)),
       stroke=INK, strokeWidth=4)
# grabber dots down the drawer's pulled edge
for j in range(6):
    d.shape("ellipse", f"Grab {j+1}", x=DRX0+7, y=DRY0+150+j*22,
            width=5, height=5, fill="#5E6E8A", opacity=70, stroke=NONE)
d.text("INSPECTOR", "Inspector title", x=(DRX0+DRX1)/2+6, y=DRY0+26,
       size=10, font="Source Sans 3", color="#8FA0BC", justify="center")
# inspector fields: label line + value bar
fy = DRY0 + 52
for i, (lw, vw) in enumerate([(60, 92), (48, 70), (66, 100)]):
    d.path(f"M{DRX0+22},{fy} L{DRX0+22+lw},{fy}", f"Field label {i+1}",
           fill=NONE, stroke="#5E6E8A", strokeWidth=3.5, opacity=60, cap="round")
    d.path(rrect(DRX0+22, fy+8, DRX1-DRX0-44, 16, 6), f"Field {i+1}",
           fill="#0E1626", stroke="#3A4864", strokeWidth=2)
    d.path(f"M{DRX0+28},{fy+16} L{DRX0+28+vw*0.8},{fy+16}", f"Field val {i+1}",
           fill=NONE, stroke="#8FA0BC", strokeWidth=3, opacity=55, cap="round")
    fy += 56
# a checkbox row + a slider
d.path(rrect(DRX0+22, fy, 16, 16, 4), "Checkbox", fill="#0E1626",
       stroke="#3A4864", strokeWidth=2)
d.path(f"M{DRX0+26},{fy+8} L{DRX0+30},{fy+12} L{DRX0+36},{fy+4}", "Check",
       fill=NONE, stroke="#D8904A", strokeWidth=2.5, cap="round")
d.path(f"M{DRX0+48},{fy+8} L{DRX0+110},{fy+8}", "Check label", fill=NONE,
       stroke="#5E6E8A", strokeWidth=3.5, opacity=60, cap="round")
fy += 44
d.path(f"M{DRX0+22},{fy+8} L{DRX1-22},{fy+8}", "Slider track", fill=NONE,
       stroke="#3A4864", strokeWidth=4, cap="round")
d.shape("ellipse", "Slider knob", x=DRX0+88, y=fy, width=16, height=16,
        fill=rad({"offset": 0, "color": "#C8D4E8"},
                 {"offset": 1, "color": "#5E6E8A"}),
        stroke=INK, strokeWidth=2)

# --- name + role ------------------------------------------------------------------
d.text("SOLIPSIST", "Name", x=500, y=930, size=58, font="Virelai Sans",
       color="#E8E4D8", justify="center")
LINE2, SZ2, TRK = "MACOS HARNESS FOR BORIS", 23, 300
r = d.text(LINE2, "Second line", x=500, y=968, size=SZ2, font="Virelai Sans",
           color="#8FA0BC", justify="center")
d.cmd("text.setStyle", "Second line tracking", id=r["id"], tracking=TRK)
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

d.finish("solipsist-V1R00")
