#!/usr/bin/env python3
"""LLG-0350 DOGE Charter — V1R00. Bureaucratic charter seal for the Department
of Genuine Experiences: rubber stamp mid-impression on a document, canonical
tests (Origin, Agency, Residue) as checkboxes, glowing algorithmic feed marked
'reduced weight' off to the side. Seal green, rim lettering. 1000x1000."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("LLG-0350 DOGE Charter", 1000, 1000)

INK = "#33271E"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1E2420"}, {"offset": 1, "color": "#0C110E"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#D9C9A4"}, {"offset": 0.72, "color": "#A8916B"},
    {"offset": 1, "color": "#6E5B40"}]}}
DOC_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F2EAD2"}, {"offset": 1, "color": "#D8CBA8"}]}}
SEAL_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#3E8A66"}, {"offset": 0.75, "color": "#2A6B4C"},
    {"offset": 1, "color": "#1A4A34"}]}}
SCR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#233B2E"}, {"offset": 1, "color": "#12201A"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#54462E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#EFE3C4", strokeWidth=3, opacity=55)
d.shape("ellipse", "Patina 1", x=180, y=160, width=230, height=150,
        fill="#8C7852", opacity=25, stroke=NONE)
d.shape("ellipse", "Patina 2", x=580, y=700, width=250, height=140,
        fill="#8C7852", opacity=22, stroke=NONE)
for i, (x, y, w) in enumerate([(200,320,8),(790,240,7),(150,560,9),(830,560,8),
                               (250,790,7),(740,770,9),(130,430,6),(870,420,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#6E5A3C", opacity=40, stroke=NONE)

# --- glowing screen: the algorithmic feed, reduced weight ---------------------
d.shape("ellipse", "Screen halo", x=640, y=230, width=290, height=210,
        fill="#5FC98A", opacity=14, stroke=NONE)
d.shape("rectangle", "Screen", x=668, y=252, width=216, height=140,
        radius=10, fill=SCR_GRAD, stroke=INK, strokeWidth=5)
# feed bars, dim and short — the feed carries reduced weight
for i, (fy, fw, op) in enumerate([(272, 160, 55), (290, 120, 40),
                                   (308, 150, 32), (326, 90, 25)]):
    d.shape("rectangle", f"Feed line {i+1}", x=684, y=fy, width=fw, height=8,
            fill="#7ED9A2", opacity=op, stroke=NONE)
d.shape("rectangle", "Feed bar", x=684, y=350, width=60, height=18,
        radius=3, fill="#5FC98A", opacity=40, stroke=NONE)
d.shape("rectangle", "Screen stand", x=764, y=392, width=24, height=20,
        fill="#2E2620", stroke=NONE)
d.text("R E D U C E D   W E I G H T", "Screen caption", x=776, y=436,
       size=13, font="Virelai Sans", color="#7ED9A2", justify="center")

# --- the charter document -------------------------------------------------------
d.shape("rectangle", "Document", x=250, y=270, width=360, height=440,
        radius=8, fill=DOC_GRAD, stroke=INK, strokeWidth=4)
d.shape("rectangle", "Doc fold", x=560, y=270, width=50, height=50,
        fill="#C9BA96", stroke=INK, strokeWidth=3)
# masthead
d.text("DEPARTMENT OF", "Doc mast 1", x=430, y=310, size=15,
       font="Virelai Sans", color="#8A7A5E", justify="center")
d.text("GENUINE EXPERIENCES", "Doc mast 2", x=430, y=336, size=20,
       font="Virelai Sans", color=INK, justify="center")
d.path("M280,352 L580,352", "Doc rule", fill=NONE, stroke="#8A7A5E",
       strokeWidth=2)
# body lines
for i, (ly, lw) in enumerate([(372, 280), (388, 260), (404, 280),
                               (420, 200), (444, 280), (460, 240)]):
    d.shape("rectangle", f"Doc line {i+1}", x=290, y=ly, width=lw, height=6,
            fill="#9A8A68", opacity=65, stroke=NONE)
# canonical tests — checkboxes
d.text("CANONICAL TESTS", "Tests head", x=430, y=500, size=15,
       font="Virelai Sans", color="#8A7A5E", justify="center")
for i, name in enumerate(["ORIGIN", "AGENCY", "RESIDUE"]):
    ty = 520 + i * 44
    d.shape("rectangle", f"Test box {i+1}", x=310, y=ty, width=24, height=24,
            fill=NONE, stroke=INK, strokeWidth=3)
    d.path(f"M315,{ty+13} L322,{ty+20} L332,{ty+5}", f"Test check {i+1}",
           fill=NONE, stroke="#2A6B4C", strokeWidth=5, cap="round")
    d.text(name, f"Test name {i+1}", x=348, y=ty+19, size=17,
           font="Virelai Sans", color=INK)

# --- the seal: green, DOGE CERTIFIED PROVENANCE around the rim ------------------
SCX, SCY, SR = 640, 610, 158
# impression shadow — the stamp still landing
d.shape("ellipse", "Seal ghost", x=SCX-SR+14, y=SCY-SR+10, width=2*SR,
        height=2*SR, fill="#2A6B4C", opacity=18, stroke=NONE)
d.shape("ellipse", "Seal outer", x=SCX-SR, y=SCY-SR, width=2*SR, height=2*SR,
        fill=SEAL_GRAD, stroke=INK, strokeWidth=5)
d.shape("ellipse", "Seal ring outer", x=SCX-SR+16, y=SCY-SR+16,
        width=2*(SR-16), height=2*(SR-16), fill=NONE, stroke="#D9C9A4",
        strokeWidth=3, opacity=80)
d.shape("ellipse", "Seal ring inner", x=SCX-88, y=SCY-88, width=176,
        height=176, fill=NONE, stroke="#D9C9A4", strokeWidth=3, opacity=80)

# rim lettering, hand-placed + rotated tangent to the circle
RIM = "DOGE CERTIFIED PROVENANCE"
for i, ch in enumerate(RIM):
    if ch == " ":
        continue
    ang = math.radians(-90 + i * 360.0 / len(RIM))
    x = SCX + 120 * math.cos(ang)
    y = SCY + 120 * math.sin(ang)
    r = d.text(ch, f"Rim {i}", x=round(x, 1), y=round(y, 1), size=21,
               font="Virelai Sans", color="#EFE3C4", justify="center")
    tid = (r or {}).get("id")
    if tid:
        d.call("transform", {"ids": [tid],
                             "rotate": round(i * 360.0 / len(RIM), 1),
                             "origin": [round(x, 1), round(y, 1)]},
               f"Rim rot {i}")

# seal core: five-point star over a stamped D — keep it iconic
def star(cx, cy, ro, ri):
    pts = []
    for k in range(10):
        r = ro if k % 2 == 0 else ri
        a = math.radians(-90 + k * 36)
        pts.append(f"{'M' if k == 0 else 'L'}{cx + r*math.cos(a):.1f},{cy + r*math.sin(a):.1f}")
    return " ".join(pts) + " Z"
d.path(star(SCX, SCY, 62, 26), "Seal star", fill="#EFE3C4", stroke=INK,
       strokeWidth=4)
d.path(star(SCX, SCY, 30, 13), "Seal star core", fill="#2A6B4C", stroke=NONE)

# --- the rubber stamp, mid-impression ------------------------------------------
# handle descends onto the seal's upper edge
d.path("M640,452 L640,330", "Stamp neck", fill=NONE, stroke="#4A3524",
       strokeWidth=34, cap="round")
d.shape("ellipse", "Stamp base", x=560, y=430, width=160, height=42,
        fill="#4A3524", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Stamp knob", x=598, y=272, width=84, height=84,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#8A6A48"}, {"offset": 1, "color": "#5A4230"}]}},
        stroke=INK, strokeWidth=4)
d.shape("ellipse", "Knob shine", x=612, y=284, width=28, height=20,
        fill="#E8DCC0", opacity=40, stroke=NONE)
# pressure shadow under the stamp base — it is mid-impression
d.shape("ellipse", "Stamp pressure", x=572, y=456, width=136, height=18,
        fill="#1A4A34", opacity=30, stroke=NONE)

# --- name + role -----------------------------------------------------------------
d.text("DOGE CHARTER", "Name", x=500, y=930, size=56, font="Virelai Sans",
       color="#EFE3C4", justify="center")
d.text("P R O V E N A N C E   J U R I S D I C T I O N", "Role", x=500,
       y=968, size=20, font="Virelai Sans", color="#B8A67E", justify="center")

d.finish("llg-0350-doge-charter-V1R00")
