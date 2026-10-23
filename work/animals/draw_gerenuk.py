#!/usr/bin/env python3
"""Gerenuk — field-guide plate V1R00. Head + long neck profile facing left,
muzzle tilted up to nibble an acacia sprig: huge ears, huge ringed eyes,
chestnut saddle running down the nape. The neck closes on the disc's own arc.
Acacia-tan palette. 1000x1000. House style: gradients + translucent shading,
never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Gerenuk — Field Plate", 1000, 1000)

INK = "#3E2A1C"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2E2118"}, {"offset": 1, "color": "#110B07"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#FBEDD0"}, {"offset": 0.68, "color": "#E9C893"},
    {"offset": 1, "color": "#B98B55"}]}}
COAT_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E0B37A"}, {"offset": 0.7, "color": "#C49058"},
    {"offset": 1, "color": "#9C6B3C"}]}}
NECK_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#DDB07A"}, {"offset": 1, "color": "#A8743F"}]}}
SADDLE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#A8662F"}, {"offset": 1, "color": "#7A4620"}]}}
EAR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#D6A46C"}, {"offset": 1, "color": "#9E6C3C"}]}}
EAR_FAR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#AE7E4C"}, {"offset": 1, "color": "#7E552F"}]}}
INNER_EAR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F6E4CC"}, {"offset": 1, "color": "#E2B9A0"}]}}
EYE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4A3022"}, {"offset": 1, "color": "#160D08"}]}}
LEAF_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#9DB062"}, {"offset": 1, "color": "#5F7438"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#8A6438", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#FFF6E2", strokeWidth=3, opacity=55)
d.shape("ellipse", "Patina 1", x=600, y=170, width=230, height=130, fill="#D9B47E", opacity=24, stroke=NONE)
d.shape("ellipse", "Patina 2", x=170, y=470, width=200, height=120, fill="#D9B47E", opacity=20, stroke=NONE)
for i, (x, y, w) in enumerate([(770,320,7),(820,470,8),(200,350,6),(160,520,8),(250,760,7),(740,700,8),
                               (860,560,6),(400,110,7),(600,115,6),(330,820,6),(700,250,5),(140,420,6)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w, fill="#A47A48", opacity=40, stroke=NONE)

# faint savanna: flat-topped acacia + horizon, low-left (all vertices inside the disc)
d.path("M150,690 C240,676 330,672 430,680", "Horizon", fill=NONE,
       stroke="#A88256", strokeWidth=4, opacity=30, cap="round")
d.path("M262,688 L270,640 L254,612 M270,640 L292,610", "Acacia trunk", fill=NONE,
       stroke="#8E6A44", strokeWidth=7, opacity=30, cap="round")
d.path("M180,616 C200,588 250,580 290,584 C330,580 370,590 384,612 "
       "C350,622 230,624 180,616 Z", "Acacia canopy", fill="#8E6A44", opacity=26, stroke=NONE)

# --- head frame: local coords facing left, rotated so the muzzle reaches up ------
HX, HY, ANG, S = 470, 330, math.radians(25), 1.15
CA, SA = math.cos(ANG), math.sin(ANG)

def T(x, y):
    return (HX + S*(x*CA - y*SA), HY + S*(x*SA + y*CA))

def tp(spec):
    out = []
    for op, pts in spec:
        out.append(op + " ".join("%.1f,%.1f" % T(*p) for p in pts))
    return " ".join(out)

def ell(label, cx, cy, w, h, **kw):
    x, y = T(cx, cy)
    w, h = round(w*S), round(h*S)
    d.shape("ellipse", label, x=round(x - w/2), y=round(y - h/2), width=w, height=h, **kw)

# --- acacia sprig the gerenuk is reaching for (behind the muzzle) -----------------
d.path("M196,236 C240,214 288,190 336,166 C364,152 392,144 418,142", "Sprig branch",
       fill=NONE, stroke="#6E4E30", strokeWidth=8, cap="round")
d.path("M262,206 C256,230 248,252 238,270", "Sprig twig", fill=NONE,
       stroke="#6E4E30", strokeWidth=5, cap="round")
for i, (x, y, a) in enumerate([(232,226,-60),(312,178,-70),(380,148,-80)]):
    t = math.radians(a)
    d.path("M%d,%d L%.0f,%.0f" % (x, y, x + 18*math.cos(t), y + 18*math.sin(t)),
           f"Thorn {i+1}", fill=NONE, stroke="#F2E6CE", strokeWidth=3, cap="round")
# feathery bipinnate leaf clusters: rows of small leaflets
for c, (cx, cy) in enumerate([(220,246),(290,188),(214,288),(360,158),(408,128)]):
    for k in range(6):
        for s in (-1, 1):
            lx = cx + (k - 2.5) * 9
            ly = cy + s * 10 - k * 2
            d.shape("ellipse", f"Leaflet {c+1}.{k+1}{'ab'[s>0]}", x=round(lx - 5), y=round(ly - 4),
                    width=10, height=8, fill=LEAF_GRAD, opacity=88, stroke=NONE)
# a few golden puffball blossoms
for i, (x, y) in enumerate([(204,224),(350,138),(276,166)]):
    d.shape("ellipse", f"Blossom {i+1}", x=x - 9, y=y - 9, width=18, height=18,
            fill="#F2C440", stroke="#C8962A", strokeWidth=2, opacity=95)

# --- far ear (behind everything on the head) --------------------------------------
d.path(tp([("M", [(-24,-36)]), ("C", [(-36,-130),(-6,-214),(60,-240)]),
           ("C", [(92,-208),(76,-114),(16,-30)]), ("Z", [])]),
       "Ear far", fill=EAR_FAR_GRAD, stroke=INK, strokeWidth=5)

# --- long neck, closing on the disc arc ----------------------------------------
# nape and throat tuck under the head; the base widens into the shoulder and ends on the rim.
NECK = ("M506,326 C540,400 570,480 600,560 C630,640 700,700 820,732 "
        "A420,420 0 0 1 440,875 "
        "C452,800 470,720 462,640 C452,560 430,470 403,382 Z")
d.path(NECK, "Neck", fill=NECK_GRAD, stroke=INK, strokeWidth=7)
# chestnut saddle down the nape, also closed on the arc
d.path("M512,342 C546,410 576,488 604,566 C636,646 704,704 820,732 "
       "A420,420 0 0 1 700,829 "
       "C650,760 600,700 570,620 C545,540 525,440 512,342 Z",
       "Saddle", fill=SADDLE_GRAD, opacity=70, stroke=NONE)
# pale throat stripe
d.path("M412,396 C436,480 458,566 466,644 C474,720 458,800 446,876 "
       "A420,420 0 0 0 478,879 C486,800 496,720 490,640 C482,560 462,470 432,392 Z",
       "Throat pale", fill="#F6E8CC", opacity=55, stroke=NONE)
# neck sheen + muscle shading
d.path("M440,440 C462,540 478,640 488,740", "Neck sheen", fill=NONE,
       stroke="#FFF2DA", strokeWidth=12, opacity=22, cap="round")
d.path("M530,470 C556,560 590,640 650,700", "Neck shade", fill=NONE,
       stroke="#7A4E28", strokeWidth=14, opacity=18, cap="round")
d.path("M610,650 C660,694 724,720 796,736", "Shoulder light", fill=NONE,
       stroke="#FFF2DA", strokeWidth=10, opacity=24, cap="round")

# --- head ------------------------------------------------------------------------
d.path(tp([("M", [(4,-42)]), ("C", [(-40,-54),(-100,-44),(-150,-14)]),
           ("C", [(-180,2),(-200,18),(-198,38)]),
           ("C", [(-196,58),(-178,68),(-150,68)]),
           ("C", [(-110,70),(-60,76),(-20,70)]),
           ("C", [(14,62),(34,40),(34,8)]),
           ("C", [(34,-20),(24,-38),(4,-42)]), ("Z", [])]),
       "Head", fill=COAT_GRAD, stroke=INK, strokeWidth=7)
# forehead light + jaw shadow
d.path(tp([("M", [(-140,-16)]), ("C", [(-100,-40),(-40,-48),(0,-38)])]),
       "Bridge light", fill=NONE, stroke="#FFF0D6", strokeWidth=14, opacity=26, cap="round")
d.path(tp([("M", [(-140,62)]), ("C", [(-100,66),(-50,70),(-14,64)])]),
       "Jaw shadow", fill=NONE, stroke="#7A4E28", strokeWidth=12, opacity=30, cap="round")
# white chin + muzzle patch
d.path(tp([("M", [(-194,44)]), ("C", [(-190,60),(-172,68),(-150,68)]),
           ("C", [(-130,68),(-116,62),(-112,54)]), ("C", [(-140,56),(-170,54),(-194,44)]), ("Z", [])]),
       "Chin white", fill="#F8EEDC", opacity=80, stroke=NONE)
# dark nose tip
d.path(tp([("M", [(-186,8)]), ("C", [(-198,18),(-202,34),(-196,44)]),
           ("C", [(-188,40),(-180,30),(-178,18)]), ("Z", [])]),
       "Nose tip", fill="#3A281C", opacity=80, stroke=NONE)
ell("Nostril", -186, 24, 12, 9, fill="#1E140D", stroke=NONE)
d.path(tp([("M", [(-194,48)]), ("C", [(-182,54),(-168,56),(-156,54)])]),
       "Mouth", fill=NONE, stroke=INK, strokeWidth=5, cap="round")
# pale brow stripe running from the eye toward the nose
d.path(tp([("M", [(-92,-22)]), ("C", [(-120,-14),(-146,-2),(-168,10)])]),
       "Brow stripe", fill=NONE, stroke="#F8EEDC", strokeWidth=9, opacity=70, cap="round")

# --- the huge eye ------------------------------------------------------------------
ell("Eye ring", -70, -6, 66, 60, fill="#FBF3E2", opacity=88, stroke=NONE)
ell("Eye", -70, -6, 46, 42, fill=EYE_GRAD, stroke=INK, strokeWidth=4)
ell("Eye glint", -78, -14, 13, 13, fill="#FFFFFF", opacity=92, stroke=NONE)
ell("Eye glint small", -58, 4, 6, 6, fill="#FFFFFF", opacity=70, stroke=NONE)
d.path(tp([("M", [(-98,-22)]), ("C", [(-82,-38),(-56,-38),(-42,-22)])]),
       "Upper lid", fill=NONE, stroke=INK, strokeWidth=5, cap="round")
for i, (a, b) in enumerate([((-96,-28),(-104,-38)), ((-84,-35),(-88,-46)), ((-70,-37),(-70,-49))]):
    d.path(tp([("M", [a]), ("L", [b])]), f"Lash {i+1}", fill=NONE, stroke=INK, strokeWidth=3, cap="round")

# --- near ear: huge, broad, swept back ------------------------------------------------
d.path(tp([("M", [(-4,-34)]), ("C", [(4,-120),(60,-206),(136,-214)]),
           ("C", [(162,-176),(134,-88),(40,-16)]), ("Z", [])]),
       "Ear near", fill=EAR_GRAD, stroke=INK, strokeWidth=6)
d.path(tp([("M", [(10,-42)]), ("C", [(20,-118),(66,-188),(126,-198)]),
           ("C", [(140,-164),(116,-90),(40,-32)]), ("Z", [])]),
       "Inner ear", fill=INNER_EAR_GRAD, opacity=92, stroke=NONE)
# dark inner-ear markings + rim
for i, spec in enumerate([[(24,-56),(54,-116),(100,-170)], [(38,-48),(72,-100),(116,-148)]]):
    d.path(tp([("M", [spec[0]]), ("Q", [spec[1], spec[2]])]), f"Ear marking {i+1}",
           fill=NONE, stroke="#6E4A30", strokeWidth=4, opacity=55, cap="round")
d.path(tp([("M", [(2,-62)]), ("C", [(16,-130),(66,-200),(132,-212)])]),
       "Ear rim light", fill=NONE, stroke="#F6DDB6", strokeWidth=5, opacity=45, cap="round")

# --- rim redrawn over the neck so the plate edge stays crisp ---------------------------
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#8A6438", strokeWidth=6)

# --- name ----------------------------------------------------------------------------
d.text("GERENUK", "Name", x=500, y=962, size=60, font="Virelai Sans",
       color="#EEDDBE", justify="center")

d.finish("gerenuk-V1R00")
