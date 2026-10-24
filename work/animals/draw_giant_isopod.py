#!/usr/bin/env python3
"""Giant isopod — field-guide plate V1R00. Bathynomus dorsal view, tilted a
few degrees: seven shingled pereonite armor bands with pointed epimera,
hooked walking legs poking under the margins, sessile compound eyes on the
head shield, two pairs of jointed antennae sweeping ahead, pleotelson fan
with uropods. Cold abyssal blue, a thin rim of light along the shell.
1000x1000. House style: gradients + translucent shading, never flat fills.
Drawn in a local frame (head up, y toward tail) and pushed through one
affine map so the tilt stays consistent. Plate = circle (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Giant Isopod — Field Plate", 1000, 1000)

INK = "#101C26"   # cold near-black blue
BG_GRAD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000], "stops": [
    {"offset": 0, "color": "#060B12"}, {"offset": 1, "color": "#000000"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#1B2B3A"}, {"offset": 0.55, "color": "#0C1620"},
    {"offset": 1, "color": "#04070B"}]}}
SED_GRAD = {"gradient": {"kind": "linear", "start": [0, 790], "end": [0, 880], "stops": [
    {"offset": 0, "color": "#26333E"}, {"offset": 1, "color": "#0E141A"}]}}
# one cold vertical gradient shared by every armor band: upper segments
# catch more of it than lower ones, which sells the domed back
SHELL_GRAD = {"gradient": {"kind": "linear", "start": [420, 300], "end": [560, 800], "stops": [
    {"offset": 0, "color": "#9DB8CC"}, {"offset": 0.5, "color": "#5F7A92"},
    {"offset": 1, "color": "#2E4252"}]}}
HEAD_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#8AA6BC"}, {"offset": 0.6, "color": "#546E84"},
    {"offset": 1, "color": "#31434F"}]}}
UNDER_GRAD = {"gradient": {"kind": "linear", "start": [0, 700], "end": [0, 860], "stops": [
    {"offset": 0, "color": "#4A6172"}, {"offset": 1, "color": "#22303C"}]}}
EYE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#3A4E5E"}, {"offset": 1, "color": "#0C141A"}]}}

PCX, PCY, PR = 500, 460, 420

# --- local frame -> canvas ---------------------------------------------------------
S, SQ, ANG = 0.88, 0.78, math.radians(-13)
ANCHOR_L, ANCHOR_C = (0, 100), (508, 502)
_ca, _sa = math.cos(ANG), math.sin(ANG)
FAR = []

def T(x, y):
    lx, ly = (x - ANCHOR_L[0]) * S, (y - ANCHOR_L[1]) * S * SQ
    X = lx * _ca - ly * _sa + ANCHOR_C[0]
    Y = lx * _sa + ly * _ca + ANCHOR_C[1]
    if math.hypot(X - PCX, Y - PCY) > PR - 24:
        FAR.append((round(X), round(Y)))
    return X, Y

def P(cmds):
    out = []
    for c in cmds:
        op, pts = c[0], c[1:]
        out.append(op + " ".join("%.1f,%.1f" % T(*p) for p in pts))
    return " ".join(out)

def on_disc(x, y, pad):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

# --- backdrop + plate ------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#23303E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#52687C", strokeWidth=3, opacity=35)
# marine snow
for i, (x, y, w) in enumerate([(205,290,6),(795,260,5),(168,470,7),(838,460,6),(255,700,5),
                               (755,690,6),(148,580,4),(855,570,5),(415,125,5),(625,115,6),
                               (315,185,4),(705,195,5),(480,98,4),(225,390,4),(812,350,4),
                               (345,828,4),(655,825,4)]):
    assert on_disc(x, y, 10), (x, y)
    d.shape("ellipse", f"Marine snow {i+1}", x=x, y=y, width=w, height=w,
            fill="#E6F0F8", opacity=40, stroke=NONE)

# --- abyssal sediment: closing on the disc's own arc --------------------------------
d.path("M160,706 C300,690 480,700 640,694 C720,690 800,700 840,706 "
       "A420,420 0 0 1 160,706 Z",
       "Sediment", fill=SED_GRAD, stroke="#36444F", strokeWidth=4)
d.path("M190,712 C340,698 620,696 810,712", "Sediment sheen",
       fill=NONE, stroke="#6E8292", strokeWidth=4, opacity=32, cap="round")
for i, (x, y, w, h) in enumerate([(240,716,26,10),(400,708,20,8),(560,704,24,9),
                                  (720,712,18,8),(640,720,14,6),(330,722,14,6)]):
    d.shape("ellipse", f"Ooze lump {i+1}", x=x, y=y, width=w, height=h,
            fill="#3B4A56", opacity=50, stroke=NONE)
# soft cast shadow under the body
d.shape("ellipse", "Body shadow", x=310, y=648, width=380, height=54,
        fill="#000000", opacity=40, stroke=NONE)

# --- the animal's geometry (local frame) ----------------------------------------------
# silhouette half-widths along the body axis (y: head top -160 -> tail tip +370)
# head: -160..-80 hw ~150 ; pereonites 1-7 ; pleonites 3 ; pleotelson
PEREO = [(-80, -42, 172), (-42, 4, 186), (4, 52, 192), (52, 100, 188),
         (100, 146, 178), (146, 188, 162), (188, 226, 140)]
PLEON = [(226, 252, 114), (252, 274, 98), (274, 294, 84)]
TELSON_Y0, TELSON_Y1, TELSON_HW = 294, 368, 84

def band(label, y0, y1, hw, tip_ext, fill=SHELL_GRAD, op=95):
    """Armor band: convex top edge tucked under the band ahead, sharp
    backward-pointing epimera at the posterior-lateral corners."""
    tp = hw + tip_ext           # epimeron tip
    y0u = y0 - 10               # top edge slides under the band in front
    d.path(P([("M", (-hw, y0u)),
              ("Q", (0, y0u - 8), (hw, y0u)),
              ("L", (hw + 6, (y0 + y1) / 2 - 8)),
              ("L", (tp, y1 - 2)),
              ("L", (hw - 12, y1)),
              ("Q", (0, y1 + 10), (-(hw - 12), y1)),
              ("L", (-tp, y1 - 2)),
              ("L", (-(hw + 6), (y0 + y1) / 2 - 8)),
              ("Z",)]),
           label, fill=fill, stroke=INK, strokeWidth=3, opacity=op)

# --- hooked walking legs poking past the margins (under the shell) -------------------
for i, (y0, y1, hw) in enumerate(PEREO):
    ym = (y0 + y1) / 2 + 6
    for s in (-1, 1):
        r0 = (s * (hw - 14), ym - 10)
        kn = (s * (hw + 26), ym + 12)
        ft = (s * (hw + 34), ym + 40)
        d.path(P([("M", r0),
                  ("Q", kn, ft)]),
               f"Leg {'L' if s < 0 else 'R'}{i+1}", fill=NONE, stroke=UNDER_GRAD,
               strokeWidth=13, cap="round")
        d.path(P([("M", r0),
                  ("Q", kn, ft)]),
               f"Leg {'L' if s < 0 else 'R'}{i+1} edge", fill=NONE, stroke=INK,
               strokeWidth=13, opacity=30, cap="round")
        # dactyl hook
        d.path(P([("M", ft), ("L", (ft[0] - s * 12, ft[1] + 12))]),
               f"Dactyl {'L' if s < 0 else 'R'}{i+1}", fill=NONE, stroke=INK,
               strokeWidth=7, cap="round")

# --- pleotelson + uropods (drawn first; everything else shingles over them) -----------
for s in (-1, 1):
    d.path(P([("M", (s * 64, 288)),
              ("C", (s * 108, 296), (s * 136, 320), (s * 128, 344)),
              ("C", (s * 120, 362), (s * 92, 366), (s * 74, 350)),
              ("C", (s * 62, 338), (s * 56, 314), (s * 58, 298)), ("Z",)]),
           f"Uropod {'L' if s < 0 else 'R'}", fill=UNDER_GRAD, stroke=INK, strokeWidth=3)
    d.path(P([("M", (s * 68, 302)), ("Q", (s * 104, 318), (s * 116, 342))]),
           f"Uropod rib {'L' if s < 0 else 'R'}", fill=NONE, stroke=INK,
           strokeWidth=2.5, opacity=45, cap="round")
# tail fan
d.path(P([("M", (-TELSON_HW, TELSON_Y0)),
          ("Q", (0, TELSON_Y0 - 10), (TELSON_HW, TELSON_Y0)),
          ("C", (TELSON_HW - 4, TELSON_Y0 + 44), (50, TELSON_Y1 - 8), (0, TELSON_Y1)),
          ("C", (-50, TELSON_Y1 - 8), (-(TELSON_HW - 4), TELSON_Y0 + 44), (-TELSON_HW, TELSON_Y0)),
          ("Z",)]),
       "Pleotelson", fill=SHELL_GRAD, stroke=INK, strokeWidth=4)
d.path(P([("M", (-52, TELSON_Y0 + 16)), ("Q", (0, TELSON_Y0 + 34), (52, TELSON_Y0 + 16))]),
       "Pleotelson ridge", fill=NONE, stroke=INK, strokeWidth=3, opacity=45, cap="round")
d.path(P([("M", (0, TELSON_Y0 + 8)), ("L", (0, TELSON_Y1 - 26))]),
       "Pleotelson keel", fill=NONE, stroke=INK, strokeWidth=4, opacity=40, cap="round")
d.path(P([("M", (-6, TELSON_Y0 + 12)), ("L", (-4, TELSON_Y1 - 34))]),
       "Pleotelson keel light", fill=NONE, stroke="#CFE2EE",
       strokeWidth=3, opacity=45, cap="round")

# --- pleonites then pereonites: tail-to-head so each band shingles over the last ------
for i, (y0, y1, hw) in enumerate(reversed(PLEON)):
    band(f"Pleonite {3 - i}", y0, y1, hw, 12)
for i, (y0, y1, hw) in enumerate(reversed(PEREO)):
    band(f"Pereonite {7 - i}", y0, y1, hw, 15)

# rim light: thin cold highlight along each segment's bottom edge
for i, (y0, y1, hw) in enumerate(PLEON + PEREO):
    d.path(P([("M", (-(hw - 22), y1 - 2)), ("Q", (0, y1 + 9), (hw - 22, y1 - 2))]),
           f"Rim light {i+1}", fill=NONE, stroke="#CFE2EE",
           strokeWidth=3, opacity=38, cap="round")
# per-band shadow: translucent dark crescent under each segment's bottom edge
for i, (y0, y1, hw) in enumerate(PEREO):
    d.path(P([("M", (-(hw - 30), y1 - 1)), ("Q", (0, y1 + 8), (hw - 30, y1 - 1))]),
           f"Band shade {i+1}", fill=NONE, stroke="#0E1A24",
           strokeWidth=7, opacity=30, cap="round")
# dorsal sheen on the mid-back
d.path(P([("M", (-58, -56)), ("C", (-84, 20), (-84, 120), (-56, 190))]),
       "Flank sheen L", fill=NONE, stroke="#D8EAF4", strokeWidth=10,
       opacity=18, cap="round")
d.path(P([("M", (-30, -60)), ("C", (-52, 24), (-52, 120), (-28, 188))]),
       "Flank sheen core", fill=NONE, stroke="#E8F4FA", strokeWidth=5,
       opacity=22, cap="round")
# faint transverse mottling across the mid segments
for i, (x, y, w, h) in enumerate([(-96, -20, 26, 10), (80, -30, 22, 9), (-70, 60, 24, 10),
                                  (96, 70, 20, 8), (-40, 140, 22, 9), (60, 150, 24, 10)]):
    d.shape("ellipse", f"Shell mottle {i+1}", x=round(T(x, y)[0] - w / 2),
            y=round(T(x, y)[1] - h / 2), width=w, height=h,
            fill="#1A2833", opacity=25, stroke=NONE)

# --- head shield -----------------------------------------------------------------------
d.path(P([("M", (-150, -80)),
          ("C", (-168, -116), (-146, -158), (-92, -172)),
          ("C", (-42, -182), (42, -182), (92, -172)),
          ("C", (146, -158), (168, -116), (150, -80)),
          ("Q", (0, -56), (-150, -80)), ("Z",)]),
       "Head", fill=HEAD_GRAD, stroke=INK, strokeWidth=4.5)
# head rim light along the front margin
d.path(P([("M", (-128, -118)), ("C", (-118, -150), (-78, -168), (-28, -172))]),
       "Head rim light", fill=NONE, stroke="#D8EAF4", strokeWidth=4,
       opacity=50, cap="round")
# frontal lobe crease + clypeus hint
d.path(P([("M", (-98, -88)), ("Q", (0, -72), (98, -88))]),
       "Head crease", fill=NONE, stroke=INK, strokeWidth=3, opacity=40, cap="round")
# sessile compound eyes: elongated dark patches on the dorsolateral head
for s in (-1, 1):
    d.path(P([("M", (s * 132, -152)),
              ("C", (s * 148, -142), (s * 152, -122), (s * 144, -106)),
              ("C", (s * 136, -94), (s * 118, -94), (s * 114, -108)),
              ("C", (s * 110, -128), (s * 116, -148), (s * 132, -152)), ("Z",)]),
           f"Eye {'L' if s < 0 else 'R'}", fill=EYE_GRAD, stroke=INK, strokeWidth=3)
    # facet glints
    d.path(P([("M", (s * 126, -144)), ("Q", (s * 138, -134), (s * 140, -118))]),
           f"Eye sheen {'L' if s < 0 else 'R'}", fill=NONE, stroke="#9FC0D4",
           strokeWidth=2.5, opacity=55, cap="round")

# --- antennae: long outer pair sweeping ahead, short inner pair -------------------------
def antenna(i, pts, w0, w1, fill="#7E97AA", op=92):
    """Jointed feeler: tapered ribbon through control points, knuckle dots."""
    n = 22
    # Catmull-Rom-ish: just polyline the quad chain for the ribbon edge
    L, R = [], []
    for k in range(n + 1):
        t = k / n
        seg = min(int(t * (len(pts) - 1)), len(pts) - 2)
        u = t * (len(pts) - 1) - seg
        x = pts[seg][0] + (pts[seg + 1][0] - pts[seg][0]) * u
        y = pts[seg][1] + (pts[seg + 1][1] - pts[seg][1]) * u
        dx = pts[seg + 1][0] - pts[seg][0]
        dy = pts[seg + 1][1] - pts[seg][1]
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy / ln, dx / ln
        w = (w0 + (w1 - w0) * t) / 2
        L.append((x + nx * w, y + ny * w)); R.append((x - nx * w, y - ny * w))
    dd = "M%.1f,%.1f " % T(*L[0])
    dd += " ".join("L%.1f,%.1f" % T(*p) for p in L[1:])
    dd += " " + " ".join("L%.1f,%.1f" % T(*p) for p in reversed(R)) + " Z"
    d.path(dd, f"Antenna {i}", fill=fill, stroke=INK, strokeWidth=3, opacity=op)
    # segment knuckles
    for j, p in enumerate(pts[1:-1]):
        d.shape("ellipse", f"Antenna {i} knuckle {j+1}", x=round(T(*p)[0] - 5),
                y=round(T(*p)[1] - 5), width=10, height=10,
                fill=fill, stroke=INK, strokeWidth=2, opacity=op)

# outer pair: from the head corners, sweeping up and out past the rim of the plate
antenna("outer L", [(-116, -146), (-172, -196), (-216, -252), (-232, -316), (-212, -364)], 12, 4)
antenna("outer R", [(116, -146), (172, -196), (216, -252), (232, -316), (212, -364)], 12, 4)
# inner pair: shorter, straighter, between the outer roots
antenna("inner L", [(-58, -158), (-76, -206), (-84, -252)], 9, 3)
antenna("inner R", [(58, -158), (76, -206), (84, -252)], 9, 3)

if FAR:
    print("WARN points near the rim:", FAR[:14])

# --- name --------------------------------------------------------------------------------
d.text("GIANT ISOPOD", "Name", x=500, y=960, size=54, font="Virelai Sans",
       color="#D6E4EE", justify="center")

d.finish("giant-isopod-V1R00")
