#!/usr/bin/env python3
"""Rosalind Franklin — milestone card V1R00. 1950s lab coat, dark hair
tied back, holding a photographic plate up beside her face — Photo 51's
X-shaped diffraction cross, the plate its own dim light source in a
darkroom-green plate. A film strip hangs drying in the upper dark. The
bust closes on the disc's own lower arc. 1000x1000. House style:
gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Rosalind Franklin — Milestone Card", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#1E150F"                    # warm dark ink, never pure black
SS3 = "Source Sans 3"              # Virelai Sans has no digit glyphs


def _stops(*pairs):
    out = []
    for p in pairs:
        s = {"offset": p[0], "color": p[1]}
        if len(p) > 2:
            s["opacity"] = p[2]
        out.append(s)
    return out


def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": _stops(*stops)}}


def rad(*stops):
    return {"gradient": {"kind": "radial", "stops": _stops(*stops)}}


def smooth(pts, closed=True, k=1.0):
    n = len(pts)
    s = "M%.1f,%.1f" % pts[0]
    for i in (range(n) if closed else range(n - 1)):
        p0 = pts[(i - 1) % n] if (closed or i > 0) else pts[0]
        p1, p2 = pts[i], pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (closed or i + 2 < n) else pts[-1]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6 * k, p1[1] + (p2[1] - p0[1]) / 6 * k)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6 * k, p2[1] - (p3[1] - p1[1]) / 6 * k)
        s += " C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (c1 + c2 + p2)
    return s + (" Z" if closed else "")


def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad


def rim_x(y, side=-1):
    return PCX + side * math.sqrt(PR * PR - (y - PCY) ** 2)


def find(o, oid):
    if isinstance(o, dict):
        if o.get("id") == oid and "bounds" in o: return o
        o = list(o.values())
    if isinstance(o, list):
        for v in o:
            hit = find(v, oid)
            if hit: return hit


BG_GRAD = lin(0, 0, 0, 1000, (0, "#0E1410"), (1, "#040604"))
PLATE_GRAD = rad((0, "#6E7C72"), (0.5, "#3E4A42"), (1, "#161D19"))
SKIN_GRAD = lin(430, 310, 510, 540, (0, "#E6C6A2"), (0.55, "#C29C7A"), (1, "#8C6A50"))
SKIN_DIM = lin(430, 310, 510, 540, (0, "#C29E80"), (1, "#7C5E46"))
HAIR_GRAD = lin(400, 270, 530, 480, (0, "#3A281C"), (0.5, "#241812"), (1, "#0E0805"))
COAT_GRAD = lin(310, 560, 690, 860, (0, "#D8D2C0"), (0.5, "#A39C88"), (1, "#5E584A"))
COAT_DIM = lin(310, 560, 690, 860, (0, "#B0A890"), (1, "#4E483C"))
BLOUSE = "#241E28"
FILM = "#C8C2AE"
GLOWC = "#D2D8E6"

# --- backdrop + darkroom-green plate ---------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#2C362E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8E0D4", strokeWidth=3, opacity=34)

# thin light pooling upper-left
d.shape("ellipse", "Light pool", x=235, y=150, width=370, height=210,
        fill="#E4E8DC", opacity=10, stroke=NONE)

# --- a film strip hanging to dry in the upper dark ---------------------------------
d.path("M298,176 L348,170 L356,356 L306,362 Z", "Film strip",
       fill=FILM, opacity=14, stroke=FILM, strokeWidth=2)
for i in range(6):
    y = 190 + i * 28
    d.shape("ellipse", f"Sprocket {i+1}", x=304, y=y, width=7, height=7,
            fill="#0E120E", opacity=30, stroke=NONE)
    d.shape("ellipse", f"Sprocket r {i+1}", x=340, y=y - 6, width=7,
            height=7, fill="#0E120E", opacity=30, stroke=NONE)
# the peg
d.path("M316,158 L334,158 L330,178 L320,178 Z", "Peg", fill="#7A7260",
       opacity=50, stroke=INK, strokeWidth=2)

# --- the photographic plate she holds — its own dim light source --------------------
PX, PY, PW, PH, PDEG = 640, 372, 118, 140, -7
# halo behind the glass — kept inside the rim
d.shape("ellipse", "Plate glow", x=PX - 120, y=PY - 105, width=240,
        height=210, fill=rad((0, GLOWC, 30), (0.6, GLOWC, 12),
        (1, GLOWC, 0)), stroke=NONE)
# the glass plate — slightly tilted
d.path(rot_rect_path(PX, PY, PW, PH, PDEG), "Photo plate",
       fill=lin(PX - 50, PY - 70, PX + 50, PY + 70,
                (0, "#D8DCE4"), (0.5, "#9AA0AE"), (1, "#565E6C")),
       stroke=INK, strokeWidth=4)
# clipped frame line inside the glass
d.path(rot_rect_path(PX, PY, PW - 18, PH - 18, PDEG), "Plate inner",
       fill=NONE, stroke="#3A4048", strokeWidth=2.5, opacity=55)

# Photo 51 — the X diffraction cross, dark blobs on the luminous glass.
# Two blurred bands crossing, then spots bigger toward the arm ends.
tc, sc = math.cos(math.radians(PDEG)), math.sin(math.radians(PDEG))
for i, ang in enumerate((-32, 32)):
    a = math.radians(ang + PDEG)
    ux, uy = math.cos(a), math.sin(a)
    p0 = (PX - ux * 52, PY - uy * 52)
    p1 = (PX + ux * 52, PY + uy * 52)
    d.path(f"M{p0[0]:.1f},{p0[1]:.1f} L{p1[0]:.1f},{p1[1]:.1f}",
           f"X band {i+1}", fill=NONE, stroke="#3A3E4C", strokeWidth=16,
           opacity=38, cap="round")
    # spots along the arm — the ladder of the helix
    for si, t in enumerate((0.16, 0.36, 0.62, 0.84)):
        for sgn in (-1, 1):
            sx = PX + ux * 52 * t * sgn
            sy = PY + uy * 52 * t * sgn
            rr = 3.2 + 3.4 * t
            d.shape("ellipse", f"X spot {i+1}-{si}-{sgn}",
                    x=sx - rr, y=sy - rr * 0.9, width=rr * 2,
                    height=rr * 1.8, fill="#2E3240",
                    opacity=62, stroke=NONE)
# dense centre — the crossing
d.shape("ellipse", "X centre", x=PX - 9, y=PY - 8, width=18, height=16,
        fill="#262A38", opacity=70, stroke=NONE)
assert on_disc(PX + 70, PY - 60, 6) and on_disc(PX + 70, PY + 60, 6)

# --- the lab coat — white mass closing on the disc's arc -----------------------------
fj = 804
jl, jr = rim_x(fj, -1), rim_x(fj, 1)
d.path(f"M{jl:.1f},{fj} C296,726 316,652 354,606 C386,570 424,558 450,552 "
       f"L492,552 C534,560 572,584 598,622 C626,662 646,730 {jr:.1f},{fj} "
       f"A{PR},{PR} 0 0 1 {jl:.1f},{fj} Z", "Lab coat",
       fill=COAT_GRAD, stroke=INK, strokeWidth=5)
# dark blouse in the coat's V
d.path("M452,556 L496,556 L484,650 L464,650 Z", "Blouse",
       fill=BLOUSE, stroke=INK, strokeWidth=3.5)
# notched lab-coat lapels
d.path("M410,556 L452,552 L468,592 L452,690 L424,620 Z", "Lapel L",
       fill=COAT_DIM, stroke=INK, strokeWidth=4)
d.path("M496,552 L530,562 L522,664 L488,592 Z", "Lapel R",
       fill=COAT_DIM, stroke=INK, strokeWidth=4)
# coat seam + patch pocket
d.path("M470,660 L470,780", "Coat seam", fill=NONE, stroke="#5E584A",
       strokeWidth=3.5, opacity=50, cap="round")
d.path("M560,690 L614,690 L610,754 L556,754 Z", "Pocket", fill=NONE,
       stroke="#5E584A", strokeWidth=3.5, opacity=55)
# neck
d.path("M450,500 L450,546 C458,554 480,554 488,546 L488,500 Z", "Neck",
       fill=SKIN_DIM, stroke=INK, strokeWidth=3.5)

# --- the raised right arm, sleeve up to the plate ----------------------------------
d.path(smooth([(572, 634), (592, 580), (606, 530), (616, 494), (612, 466),
               (594, 456), (578, 476), (566, 522), (552, 572), (540, 612)],
              k=0.9), "Sleeve raised", fill=COAT_GRAD, stroke=INK,
       strokeWidth=4.5)
# hand pinching the plate's lower-left corner
d.path(smooth([(598, 470), (606, 452), (622, 446), (634, 456), (630, 474),
               (616, 484), (602, 482)]), "Hand", fill=SKIN_GRAD,
       stroke=INK, strokeWidth=3.5)
d.path("M606,470 L626,468", "Grip line", fill=NONE, stroke="#8A6248",
       strokeWidth=2.5, opacity=70, cap="round")

# --- head: dark hair pulled hard back to a low bun ------------------------------------
# tight hair cap — no loose mass, it follows the skull
d.path(smooth([(408, 428), (398, 378), (404, 330), (426, 296), (462, 282),
               (500, 292), (522, 322), (528, 370), (522, 422), (512, 444),
               (504, 418), (508, 370), (500, 328), (482, 304), (460, 298),
               (438, 306), (422, 332), (416, 374), (418, 416)], k=0.85),
       "Hair", fill=HAIR_GRAD, stroke=INK, strokeWidth=3.5)
# pulled-back strand lines converging on the bun
for i, dd in enumerate(["M424,336 C446,316 472,306 498,308",
                        "M418,376 C440,348 468,332 500,332",
                        "M420,414 C440,384 468,364 502,360"]):
    d.path(dd, f"Hairline {i+1}", fill=NONE, stroke="#58402A",
           strokeWidth=2.5, opacity=50, cap="round")
# low bun at the nape — tucked against the jaw, joined by a swept strand
d.path("M508,436 C518,448 524,462 526,478", "Bun strand", fill=NONE,
       stroke="#241812", strokeWidth=8, opacity=90, cap="round")
d.path(smooth([(508, 470), (528, 462), (544, 472), (546, 494), (534, 510),
               (512, 508), (500, 492)]), "Bun", fill=HAIR_GRAD,
       stroke=INK, strokeWidth=3.5)
d.path("M514,480 C524,476 534,480 538,490", "Bun coil", fill=NONE,
       stroke="#58402A", strokeWidth=2.5, opacity=60, cap="round")

# face — oval, serious, tipped a touch up toward the plate
d.path(smooth([(462, 302), (502, 320), (510, 378), (504, 438), (492, 486),
               (476, 512), (462, 518), (448, 512), (432, 486), (420, 438),
               (414, 378), (422, 320)], k=0.85), "Face",
       fill=SKIN_GRAD, stroke=INK, strokeWidth=4)
# ears — small, under the pulled hair
d.path("M412,404 C406,408 404,422 410,434 C414,440 420,438 422,430",
       "Ear L", fill=SKIN_DIM, stroke=INK, strokeWidth=3)

# features — dark brows, gaze lifted up-right to the plate
d.path("M424,392 C435,385 449,384 459,390", "Brow L", fill=NONE,
       stroke="#241812", strokeWidth=5, opacity=85, cap="round")
d.path("M470,390 C481,384 495,385 504,391", "Brow R", fill=NONE,
       stroke="#241812", strokeWidth=5, opacity=85, cap="round")
d.path("M427,412 C434,405 449,405 456,411 C449,418 434,418 427,412 Z",
       "Eye L", fill="#EFE4D0", stroke=INK, strokeWidth=3)
d.path("M471,411 C478,404 492,404 499,410 C492,417 478,417 471,411 Z",
       "Eye R", fill="#EFE4D0", stroke=INK, strokeWidth=3)
# irises up and right — reading the plate
d.shape("ellipse", "Iris L", x=442, y=406, width=10, height=11,
        fill="#241812", stroke=NONE)
d.shape("ellipse", "Iris R", x=487, y=405, width=10, height=11,
        fill="#241812", stroke=NONE)
d.shape("ellipse", "Glint L", x=446, y=407, width=3.4, height=3.4,
        fill="#E8F0FF", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=491, y=406, width=3.4, height=3.4,
        fill="#E8F0FF", opacity=90, stroke=NONE)
# nose, mouth — quiet, working
d.path("M464,414 C469,430 470,446 465,458", "Nose shade", fill=NONE,
       stroke="#9A7658", strokeWidth=3.5, opacity=45, cap="round")
d.path("M456,460 C462,464 472,464 478,459", "Nose base", fill=NONE,
       stroke="#8A6248", strokeWidth=3, opacity=55, cap="round")
d.path("M450,488 C458,492 470,492 478,487", "Mouth", fill=NONE,
       stroke="#7E4C3E", strokeWidth=3.5, opacity=75, cap="round")
# the plate's light catching her right cheek
d.path("M506,404 C510,432 508,458 500,480", "Plate light", fill=NONE,
       stroke=GLOWC, strokeWidth=4, opacity=30, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#262E2A", strokeWidth=6)

# --- captions ---------------------------------------------------------------------
d.text("ROSALIND FRANKLIN", "Name", x=500, y=934, size=56,
       font="Virelai Sans", color="#E8ECE4", justify="center")
LINE2, SZ2, TRK = "PHOTO 51 · 1952", 22, 500
r = d.text(LINE2, "Milestone", x=500, y=970, size=SZ2, font=SS3,
           color="#C0C8C0", justify="center")
d.cmd("text.setStyle", "Milestone tracking", id=r["id"], tracking=TRK)

b = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("milestone bounds", {k: round(v) for k, v in b.items()})
nearest = (min(max(PCX, b["x"]), b["x"] + b["width"]),
           min(max(PCY, b["y"]), b["y"] + b["height"]))
clear = math.hypot(nearest[0] - PCX, nearest[1] - PCY) - (PR + 3)
print("clears rim by %.1f" % clear)
assert clear > 0 and b["width"] <= 760 and b["x"] >= 10 and b["x"] + b["width"] <= 990, b

d.finish("rosalind-franklin-V1R00")
