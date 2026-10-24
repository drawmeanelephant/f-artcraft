#!/usr/bin/env python3
"""China cabinet — field plate V1R00. A two-part heirloom: drawer-over-doors
base, waist moulding, and a glazed hutch where the good porcelain stands
behind mullioned doors. Seen from front-right, above. Mahogany plate,
heirloom mood. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("China Cabinet — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#1E0D08"

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [round(x0, 1), round(y0, 1)],
            "end": [round(x1, 1), round(y1, 1)],
            "stops": [dict(offset=s[0], color=s[1], **({"opacity": s[2]} if len(s) > 2 else {}))
                      for s in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial", "stops": [
        dict(offset=s[0], color=s[1], **({"opacity": s[2]} if len(s) > 2 else {})) for s in stops]}}

# --- projection: x right, y up, z toward the viewer; seen from front-right, above ---
TH = math.radians(28)
CT, ST = math.cos(TH), math.sin(TH)
K, VC = 0.40, 0.95

def proj(x, y, z):
    return (x * CT - z * ST, (x * ST + z * CT) * K - y * VC)

OPS = []

def poly(label, pts3, fill=None, stroke=INK, sw=2.5, opacity=None, g=None):
    OPS.append(("poly", label, [proj(*p) for p in pts3], fill, stroke, sw, opacity,
                None if g is None else (proj(*g[0]), proj(*g[1]), g[2])))

def line(label, pts3, stroke, sw, opacity=None):
    OPS.append(("line", label, [proj(*p) for p in pts3], NONE, stroke, sw, opacity, None))

def front(x0, x1, y0, y1, z):
    return [(x0, y1, z), (x1, y1, z), (x1, y0, z), (x0, y0, z)]

def side(x, z0, z1, y0, y1):
    return [(x, y1, z1), (x, y1, z0), (x, y0, z0), (x, y0, z1)]

def top(x0, x1, z0, z1, y):
    return [(x0, y, z0), (x1, y, z0), (x1, y, z1), (x0, y, z1)]

# mahogany + porcelain + glass palette
FRONT_ST = [(0, "#9A4A28"), (1, "#642A12")]
SIDE_ST  = [(0, "#602C18"), (1, "#321408")]
TOP_ST   = [(0, "#B86840"), (0.6, "#8E4422"), (1, "#5E2A14")]
DOOR_ST  = [(0, "#A05230"), (1, "#6E3018")]
INNER_ST = [(0, "#5E2C16"), (1, "#3A180A")]
BACK_ST  = [(0, "#D9C9A2"), (1, "#A8905E")]   # fabric-lined display back
PORC_D, PORC_L = "#C8BBA0", "#F6F0E2"         # porcelain
COBALT = "#2A4678"
BRASS    = [(0, "#F6DE96"), (0.5, "#CFA04A"), (1, "#8A6224")]
GLASS    = "#C4D8DC"

W, D = 300, 120            # case box
FOOT = 24                  # bracket feet
B0, B1 = FOOT, FOOT + 170  # base body
WM0, WM1 = B1, B1 + 14     # waist moulding
H0, H1 = WM1, WM1 + 300    # hutch
CORN = 20                  # cornice band
DZ = D                     # front plane

# --- hutch interior first: it must paint under the glass ------------------------------
# display back: warm fabric lining
poly("Display back", front(16, W - 16, H0 + 8, H1 - 10, 20), stroke=NONE,
     g=((16, H1 - 10, 20), (W - 16, H0 + 8, 20), BACK_ST))
# interior left wall (+x face shows through the left door's glass)
poly("Hutch left inner", side(16, 20, DZ, H0 + 8, H1 - 10), stroke=NONE,
     g=((16, H1 - 10, DZ), (16, H0 + 8, 20), [(0, "#6E3A20"), (1, "#3A1C0C")]))
# hutch floor (top of waist, interior) and ceiling shadow
poly("Hutch floor", top(16, W - 16, 20, DZ, H0 + 8), stroke=NONE,
     g=((16, H0 + 8, DZ), (W - 16, H0 + 8, 20), [(0, "#8A6238"), (1, "#523018")]))
poly("Hutch ceiling", top(16, W - 16, 20, DZ, H1 - 10), stroke=NONE, fill="#2A1408")

# three display shelves, pale front edges
SHELVES = [H0 + 96, H0 + 188]
poly("Shelf 1", top(18, W - 18, 22, DZ - 4, SHELVES[0]), sw=1.8,
     g=((18, SHELVES[0], DZ), (W - 18, SHELVES[0], 22), [(0, "#C9B184"), (1, "#8A6A40")]))
poly("Shelf 1 edge", front(18, W - 18, SHELVES[0] - 7, SHELVES[0], DZ - 4), sw=1.8,
     g=((18, SHELVES[0], DZ), (W - 18, SHELVES[0] - 7, DZ), [(0, "#A8845A"), (1, "#6E4E28")]))
poly("Shelf 2", top(18, W - 18, 22, DZ - 4, SHELVES[1]), sw=1.8,
     g=((18, SHELVES[1], DZ), (W - 18, SHELVES[1], 22), [(0, "#C9B184"), (1, "#8A6A40")]))
poly("Shelf 2 edge", front(18, W - 18, SHELVES[1] - 7, SHELVES[1], DZ - 4), sw=1.8,
     g=((18, SHELVES[1], DZ), (W - 18, SHELVES[1] - 7, DZ), [(0, "#A8845A"), (1, "#6E4E28")]))

# --- porcelain: discs in the x-y plane standing on each shelf ---------------------------
def plate_disc(nm, cx, base, r, z, rim=True):
    """Upright plate: decagon disc + cobalt rim ring + darker foot shadow."""
    pts = [(cx + r * math.cos(a), base + r * math.sin(a), z) for a in
           [i * math.tau / 14 for i in range(14)]]
    poly(nm, pts, sw=1.6, g=((cx - r, base + r, z), (cx + r, base - r, z),
                             [(0, PORC_L), (1, PORC_D)]))
    if rim:
        ring = [(cx + r * 0.87 * math.cos(a), base + r * 0.87 * math.sin(a), z + 0.5)
                for a in [i * math.tau / 14 for i in range(14)]]
        OPS.append(("ring", nm + " cobalt ring", [proj(*p) for p in ring],
                    NONE, COBALT, 3.4, 70, None))

def jug(nm, cx, base, w, h, z):
    """Lidded tureen / jug silhouette on a shelf."""
    pts = [(cx - w * 0.62, base, z), (cx - w * 0.78, base + h * 0.36, z),
           (cx - w * 0.66, base + h * 0.78, z), (cx - w * 0.30, base + h * 0.86, z),
           (cx + w * 0.30, base + h * 0.86, z), (cx + w * 0.66, base + h * 0.78, z),
           (cx + w * 0.78, base + h * 0.36, z), (cx + w * 0.62, base, z)]
    poly(nm, pts, sw=1.6, g=((cx - w, base + h, z), (cx + w, base, z),
                             [(0, PORC_L), (0.65, PORC_D), (1, "#A89878")]))
    # lid
    poly(nm + " lid", [(cx - w * 0.42, base + h * 0.86, z),
                       (cx - w * 0.30, base + h * 0.98, z),
                       (cx + w * 0.30, base + h * 0.98, z),
                       (cx + w * 0.42, base + h * 0.86, z)], sw=1.4,
         g=((cx - w * 0.4, base + h, z), (cx + w * 0.4, base + h * 0.86, z),
            [(0, "#EFE8D4"), (1, PORC_D)]))
    poly(nm + " knob", [(cx - 3, base + h * 0.98, z), (cx + 3, base + h * 0.98, z),
                        (cx + 2, base + h * 1.04, z), (cx - 2, base + h * 1.04, z)],
         sw=1.2, g=((cx, base + h * 1.04, z), (cx, base + h, z), BRASS))
    line(nm + " band", [(cx - w * 0.7, base + h * 0.3, z + 0.4),
                        (cx + w * 0.7, base + h * 0.3, z + 0.4)], COBALT, 2.6, 75)

def cup(nm, cx, base, w, h, z):
    """Teacup: open silhouette with a handle tick."""
    pts = [(cx - w / 2, base, z), (cx - w * 0.62, base + h, z),
           (cx + w * 0.62, base + h, z), (cx + w / 2, base, z)]
    poly(nm, pts, sw=1.5, g=((cx, base + h, z), (cx, base, z),
                             [(0, PORC_L), (1, PORC_D)]))
    line(nm + " rim", [(cx - w * 0.6, base + h - 1, z + 0.3),
                       (cx + w * 0.6, base + h - 1, z + 0.3)], COBALT, 2.2, 70)
    line(nm + " handle", [(cx + w * 0.6, base + h * 0.75, z),
                          (cx + w * 0.85, base + h * 0.6, z),
                          (cx + w * 0.6, base + h * 0.4, z)], "#B0A284", 2.6)

# shelf dressing: top shelf plates, mid shelf tureen + cups, floor plates
for i, cx in enumerate((60, 110, 200, 250)):
    plate_disc(f"Top plate {i+1}", cx, SHELVES[1] + 23, 22, 40)
jug("Tureen", 150, SHELVES[1] + 2, 30, 42, 55)
for i, cx in enumerate((70, 235)):
    plate_disc(f"Mid plate {i+1}", cx, SHELVES[0] + 21, 20, 42)
jug("Sugar bowl", 150, SHELVES[0] + 2, 24, 30, 50)
cup("Cup L", 105, SHELVES[0] + 2, 20, 20, 70)
cup("Cup R", 195, SHELVES[0] + 2, 20, 20, 70)
for i, cx in enumerate((85, 160, 230)):
    plate_disc(f"Low plate {i+1}", cx, H0 + 33, 24, 45)

# --- hutch shell: right side, face frame, cornice ---------------------------------------
poly("Hutch right side", side(W, 0, DZ, H0, H1), sw=2.5,
     g=((W, H1, DZ), (W, H0, 0), SIDE_ST))
poly("Hutch right top", top(W - 12, W, 0, DZ, H1), sw=2, stroke=NONE, fill="#3E1C0C")
# face frame stiles and rails around the two door openings
poly("Hutch left stile", front(0, 16, H0, H1, DZ + 1), sw=2.2,
     g=((0, H1, DZ), (16, H0, DZ), FRONT_ST))
poly("Hutch right stile", front(W - 16, W, H0, H1, DZ + 1), sw=2.2,
     g=((W - 16, H1, DZ), (W, H0, DZ), FRONT_ST))
poly("Hutch centre stile", front(W / 2 - 4, W / 2 + 4, H0, H1, DZ + 1), sw=2,
     g=((W / 2 - 4, H1, DZ), (W / 2 + 4, H0, DZ), FRONT_ST))
poly("Hutch top rail", front(0, W, H1 - 14, H1, DZ + 1), sw=2.2,
     g=((0, H1, DZ), (W, H1 - 14, DZ), FRONT_ST))
poly("Hutch bottom rail", front(0, W, H0, H0 + 12, DZ + 1), sw=2.2,
     g=((0, H0 + 12, DZ), (W, H0, DZ), FRONT_ST))

# glazed doors: glass sheet per door, then astragal bars, then a diagonal sheen
for nm, (gx0, gx1) in (("Left door", (16, W / 2 - 4)), ("Right door", (W / 2 + 4, W - 16))):
    gy0, gy1 = H0 + 12, H1 - 14
    poly(f"{nm} glass", front(gx0, gx1, gy0, gy1, DZ + 2), stroke="#E4F0F0", sw=1.4,
         opacity=None, g=((gx0, gy1, DZ), (gx1, gy0, DZ),
                          [(0, GLASS, 22), (0.5, GLASS, 10), (1, GLASS, 16)]))
    # astragal grid: 1 vertical + 2 horizontals -> six panes
    mx = (gx0 + gx1) / 2
    poly(f"{nm} mullion v", front(mx - 3, mx + 3, gy0, gy1, DZ + 3), sw=1.6,
         g=((mx - 3, gy1, DZ), (mx + 3, gy0, DZ), DOOR_ST))
    for j, my in enumerate((gy0 + (gy1 - gy0) / 3, gy0 + 2 * (gy1 - gy0) / 3)):
        poly(f"{nm} mullion h{j+1}", front(gx0, gx1, my - 3, my + 3, DZ + 3), sw=1.6,
             g=((gx0, my + 3, DZ), (gx1, my - 3, DZ), DOOR_ST))
    # door frame overlay: thin rails inside the opening edges
    poly(f"{nm} inner frame", front(gx0, gx1, gy0, gy1, DZ + 2), fill=NONE, sw=2.2,
         stroke="#3A180A")
    # diagonal sheen on the glass
    line(f"{nm} sheen", [(gx0 + (gx1 - gx0) * 0.22, gy0 + 8, DZ + 4),
                         (gx0 + (gx1 - gx0) * 0.55, gy1 - 10, DZ + 4)],
         "#F4FBFC", 7, 22)
    line(f"{nm} sheen 2", [(gx0 + (gx1 - gx0) * 0.34, gy0 + 8, DZ + 4),
                           (gx0 + (gx1 - gx0) * 0.62, gy1 - 10, DZ + 4)],
         "#F4FBFC", 3, 16)

# brass knobs on the meeting stile sides
for i, kx in enumerate((W / 2 - 12, W / 2 + 12)):
    poly(f"Knob {i+1}", [(kx + 4.4 * math.cos(a / 12 * math.tau),
                          H0 + 150 + 4.4 * math.sin(a / 12 * math.tau), DZ + 4)
                         for a in range(12)], sw=1.4,
         g=((kx - 4, H0 + 154, DZ), (kx + 4, H0 + 146, DZ), BRASS))

# cornice: crown band + a shallow pediment step at the centre
CX0, CX1, CZ0, CZ1 = -10, W + 10, -10, D + 10
poly("Cornice side", side(CX1, CZ0, CZ1, H1, H1 + CORN), sw=2.4,
     g=((CX1, H1 + CORN, CZ1), (CX1, H1, CZ0), SIDE_ST))
poly("Cornice front", front(CX0, CX1, H1, H1 + CORN, CZ1), sw=2.4,
     g=((CX0, H1 + CORN, CZ1), (CX1, H1, CZ1), FRONT_ST))
poly("Cornice top", top(CX0, CX1, CZ0, CZ1, H1 + CORN), sw=2.4,
     g=((CX0, H1 + CORN, CZ0), (CX1, H1 + CORN, CZ1), TOP_ST))
line("Cornice light", [(CX0 + 4, H1 + CORN - 3, CZ1 + 1), (CX1 - 4, H1 + CORN - 3, CZ1 + 1)],
     "#E8A870", 2.4, 55)
# pediment: low centre block on the cornice
PW = 46
poly("Pediment front", front(W / 2 - PW, W / 2 + PW, H1 + CORN, H1 + CORN + 22, CZ1),
     sw=2.2, g=((W / 2 - PW, H1 + CORN + 22, CZ1), (W / 2 + PW, H1 + CORN, CZ1), FRONT_ST))
poly("Pediment top", top(W / 2 - PW, W / 2 + PW, CZ0 + 30, CZ1, H1 + CORN + 22), sw=2,
     g=((W / 2 - PW, H1 + CORN + 22, CZ0 + 30), (W / 2 + PW, H1 + CORN + 22, CZ1), TOP_ST))
poly("Pediment side", side(W / 2 + PW, CZ0 + 30, CZ1, H1 + CORN, H1 + CORN + 22), sw=1.8,
     g=((W / 2 + PW, H1 + CORN + 22, CZ1), (W / 2 + PW, H1 + CORN, CZ0 + 30), SIDE_ST))

# --- waist moulding between hutch and base ----------------------------------------------
poly("Waist side", side(W + 6, -4, D + 4, WM0, WM1), sw=2.2,
     g=((W + 6, WM1, D + 4), (W + 6, WM0, -4), SIDE_ST))
poly("Waist front", front(-6, W + 6, WM0, WM1, D + 4), sw=2.4,
     g=((-6, WM1, D + 4), (W + 6, WM0, D + 4), [(0, "#A25430"), (1, "#702F16")]))

# --- base: right side, drawer, two fielded doors, feet -----------------------------------
poly("Base right side", side(W, 0, DZ, B0, B1), sw=2.5,
     g=((W, B1, DZ), (W, B0, 0), SIDE_ST))
# long drawer across the base top
DR0, DR1 = 12, W - 12
poly("Drawer", front(DR0, DR1, B1 - 52, B1 - 6, DZ + 1), sw=2.4,
     g=((DR0, B1 - 6, DZ), (DR1, B1 - 52, DZ), DOOR_ST))
line("Drawer bevel up", [(DR0 + 4, B1 - 10, DZ + 2), (DR1 - 4, B1 - 10, DZ + 2)],
     "#D88A5C", 2, 45)
for i, bx in enumerate((W * 0.32, W * 0.68)):
    poly(f"Drawer pull {i+1}", [(bx + 5 * math.cos(a / 12 * math.tau),
                                 B1 - 29 + 5 * math.sin(a / 12 * math.tau), DZ + 3)
                                for a in range(12)], sw=1.4,
         g=((bx - 5, B1 - 24, DZ), (bx + 5, B1 - 34, DZ), BRASS))
# two fielded-panel doors under the drawer
DB0, DB1 = B0 + 6, B1 - 56
for nm, (dx0, dx1) in (("Base door L", (14, W / 2 - 4)), ("Base door R", (W / 2 + 4, W - 14))):
    poly(nm, front(dx0, dx1, DB0, DB1, DZ + 1), sw=2.4,
         g=((dx0, DB1, DZ), (dx1, DB0, DZ), DOOR_ST))
    px0, px1 = dx0 + 10, dx1 - 10
    py0, py1 = DB0 + 10, DB1 - 10
    poly(nm + " field", front(px0, px1, py0, py1, DZ + 2), sw=1.8,
         g=((px0, py1, DZ), (px1, py0, DZ), [(0, "#8E4426"), (1, "#58240F")]))
    line(nm + " mould shade", [(px0 - 5, py1 + 5, DZ + 2), (px1 + 5, py1 + 5, DZ + 2),
                               (px1 + 5, py0 - 5, DZ + 2)], "#381606", 2.2, 65)
    line(nm + " mould light", [(px1 + 5, py0 - 5, DZ + 2), (px0 - 5, py0 - 5, DZ + 2),
                               (px0 - 5, py1 + 5, DZ + 2)], "#D88A5C", 2.2, 55)
# knobs on the meeting stiles + escutcheon on the drawer centre
for i, kx in enumerate((W / 2 - 12, W / 2 + 12)):
    poly(f"Base knob {i+1}", [(kx + 4.2 * math.cos(a / 12 * math.tau),
                               DB0 + (DB1 - DB0) / 2 + 4.2 * math.sin(a / 12 * math.tau), DZ + 3)
                              for a in range(12)], sw=1.4,
         g=((kx - 4, DB0 + (DB1 - DB0) / 2 + 4, DZ),
            (kx + 4, DB0 + (DB1 - DB0) / 2 - 4, DZ), BRASS))
# frame rails between drawer and doors, and centre stile of the base
poly("Base mid rail", front(0, W, B1 - 58, B1 - 50, DZ + 1), sw=2,
     g=((0, B1 - 50, DZ), (W, B1 - 58, DZ), FRONT_ST))
poly("Base centre stile", front(W / 2 - 4, W / 2 + 4, B0 + 6, B1 - 58, DZ + 1), sw=1.8,
     g=((W / 2 - 4, B1 - 58, DZ), (W / 2 + 4, B0 + 6, DZ), FRONT_ST))
poly("Base left stile", front(0, 14, B0 + 6, B1 - 58, DZ + 1), sw=2,
     g=((0, B1 - 58, DZ), (14, B0 + 6, DZ), FRONT_ST))
poly("Base right stile", front(W - 14, W, B0 + 6, B1 - 58, DZ + 1), sw=2,
     g=((W - 14, B1 - 58, DZ), (W, B0 + 6, DZ), FRONT_ST))

# bracket feet: stepped ogee blocks at both front corners + rear hint
for nm, fx in (("L", 0), ("R", W - 30)):
    poly(f"Foot {nm}", [(fx + 6, FOOT, DZ + 2), (fx + 24, FOOT, DZ + 2),
                        (fx + 26, FOOT + 10, DZ + 2), (fx + 16, FOOT + 16, DZ + 2),
                        (fx + 6, FOOT + 16, DZ + 2)], sw=2,
         g=((fx, FOOT + 16, DZ), (fx, FOOT, DZ), [(0, "#6E3018"), (1, "#361408")]))
poly("Rear foot hint", side(W, D - 40, D - 12, 0, FOOT), stroke=NONE, fill="#2A1208")
# apron line between the feet
line("Apron", [(8, B0 + 4, DZ + 1), (W - 8, B0 + 4, DZ + 1)], "#3A180A", 2.4, 60)
poly("Apron face", front(6, W - 6, B0, B0 + 8, DZ + 1), sw=2,
     g=((0, B0 + 8, DZ), (W, B0, DZ), [(0, "#7E3A20"), (1, "#4A1E0C")]))

# --- fit to the disc -----------------------------------------------------------------------
xs = [p[0] for op in OPS for p in op[2]]
ys = [p[1] for op in OPS for p in op[2]]
bw, bh = max(xs) - min(xs), max(ys) - min(ys)
SC = min(560 / bw, 560 / bh)
OX = 500 - SC * (min(xs) + max(xs)) / 2
OY = 480 - SC * (min(ys) + max(ys)) / 2

def S(p):
    return (OX + SC * p[0], OY + SC * p[1])

def path_of(pts, closed):
    q = [S(p) for p in pts]
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in q) + (" Z" if closed else "")

screen = [S(p) for op in OPS for p in op[2]]
for x, y in screen:
    assert math.hypot(x - PCX, y - PCY) <= PR - 26, (x, y)
FOOT_Y = max(y for _, y in screen)
print("fit: scale %.3f  bbox x %.0f..%.0f  y %.0f..%.0f" % (
    SC, min(s[0] for s in screen), max(s[0] for s in screen), min(s[1] for s in screen), FOOT_Y))

# --- backdrop + plate -------------------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin(0, 0, 0, 1000, (0, "#170C0C"), (1, "#070303")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#7A5A4A", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#5C2830"), (0.6, "#381620"), (1, "#150A0C")),
        stroke="#0F0506", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E0C6B4", strokeWidth=3, opacity=24)
d.shape("ellipse", "Cabinet light", x=210, y=110, width=580, height=560,
        fill=rad((0, "#FFC890", 0.14), (0.6, "#FFC890", 0.05), (1, "#FFC890", 0)), stroke=NONE)

HZN = 690
hx = math.sqrt(PR ** 2 - (HZN - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{HZN} L{PCX + hx:.1f},{HZN} A420,420 0 0 1 {PCX - hx:.1f},{HZN} Z", "Floor",
       fill=lin(0, HZN, 0, 880, (0, "#2C1C14", 0.55), (1, "#100806", 0.9)), stroke=NONE)
d.shape("ellipse", "Cabinet shadow", x=250, y=FOOT_Y - 34, width=520, height=88,
        fill=rad((0, "#060302", 0.65), (1, "#060302", 0)), stroke=NONE)

# --- the cabinet ---------------------------------------------------------------------------------
for kind, label, pts, fill, stroke, sw, op, g in OPS:
    kw = {}
    if g is not None and kind == "poly":
        s0, s1, stops_ = g
        a, b = S(s0), S(s1)
        if abs(a[0] - b[0]) + abs(a[1] - b[1]) < 1:
            b = (a[0], a[1] + 1)
        fill = lin(a[0], a[1], b[0], b[1], *stops_)
    if op is not None:
        kw["opacity"] = op
    if kind == "poly":
        d.path(path_of(pts, True), label, fill=fill, stroke=stroke,
               **({"strokeWidth": sw, "join": "round"} if stroke != NONE else {}), **kw)
    elif kind == "ring":
        q = pts + [pts[0]]
        d.path(path_of(q, False), label, fill=NONE, stroke=stroke, strokeWidth=sw,
               cap="round", join="round", **kw)
    else:
        d.path(path_of(pts, False), label, fill=NONE, stroke=stroke, strokeWidth=sw,
               cap="round", join="round", **kw)

d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840, fill=NONE, stroke="#0C0508", strokeWidth=6)

# --- captions --------------------------------------------------------------------------------------
d.text("CHINA CABINET", "Name", x=500, y=940, size=58, font="Virelai Sans",
       color="#F0E2D4", justify="center")
LINE2, SZ2, TRK = "MAHOGANY · GLASS · BRASS", 22, 300
r = d.text(LINE2, "Second line", x=500, y=975, size=SZ2, font="Virelai Sans",
           color="#C8A498", justify="center")
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

d.finish("china-cabinet-V1R00")
