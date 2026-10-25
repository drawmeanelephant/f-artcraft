#!/usr/bin/env python3
"""Golden Week — Festival Seal V1R00.

Koinobori: carp streamers flying from a spring mast. One taut line runs from
the pole top to a low anchor; three carps — black magoi, red higoi, a small
blue child — pin their mouths to the line and stream right on the wind, each
body a single flowing path with a forked tail. Fresh-sky disc, green hills
hugging the bottom, a pinwheel (yaguruma) at the masthead, gold rim, vermilion
chop with a koi mark. 1000x1000.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from orient.plate import (Plate, PCX, PCY, PR, NONE, INK, GOLD, GOLD_HI,
                          GOLD_LO, PAPER, LATIN, CJK, lin, rad, gold_lin,
                          smooth, blend)
from festival_kit import seal_disc, glow, dust, ring_dots, caption

SLUG = "golden-week-V1R00"
SERIF = "Source Sans 3"          # Virelai Sans has no digits -> dates use this

SKY_HI = "#5FA4D2"
SKY_LO = "#DCEAD8"
HILL = "#3E6B42"
HILL_LO = "#1E3A26"
CREAM = "#F6EBD0"

p = Plate("Golden Week — Festival Seal", 1000, 1000)
d = p.d


# --- local helpers -----------------------------------------------------------
def inside(x, y, pad=0, label=""):
    if math.hypot(x - PCX, y - PCY) > PR - pad:
        raise AssertionError(f"outside disc: {label} ({x:.0f},{y:.0f})")
    return (x, y)


def streamer(spine, widths, tail_len, tail_spread, fill, label,
             stroke=INK, sw=3.0):
    """Carp body as ONE closed path: spine + widths -> ribbon, forked tail.

    Returns (left_pts, right_pts, normals) so scale arcs can be laid on.
    """
    n = len(spine)
    L, R = [], []
    for i, (x, y) in enumerate(spine):
        ax, ay = spine[max(i - 1, 0)]
        bx, by = spine[min(i + 1, n - 1)]
        dx, dy = bx - ax, by - ay
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy / ln, dx / ln
        w = widths[i] / 2
        L.append((x + nx * w, y + ny * w))
        R.append((x - nx * w, y - ny * w))
    # tail fork: two tips past the spine end, notch between
    dx = spine[-1][0] - spine[-2][0]
    dy = spine[-1][1] - spine[-2][1]
    ln = math.hypot(dx, dy) or 1
    ux, uy = dx / ln, dy / ln
    nx, ny = -uy, ux
    tx, ty = spine[-1]
    t_up = (tx + ux * tail_len + nx * tail_spread,
            ty + uy * tail_len + ny * tail_spread)
    t_lo = (tx + ux * tail_len - nx * tail_spread,
            ty + uy * tail_len - ny * tail_spread)
    notch = (tx + ux * tail_len * 0.38, ty + uy * tail_len * 0.38)
    body = smooth(L + [t_up])
    body += f" L{notch[0]:.1f},{notch[1]:.1f} L{t_lo[0]:.1f},{t_lo[1]:.1f}"
    body += smooth([t_lo] + list(reversed(R)), move=False)
    hx, hy = spine[0]
    body += (f" Q{hx - ux * widths[0] * 0.34:.1f},{hy - uy * widths[0] * 0.34:.1f} "
             f"{L[0][0]:.1f},{L[0][1]:.1f} Z")
    inside(t_up[0], t_up[1], 12, f"{label} tail up")
    inside(t_lo[0], t_lo[1], 12, f"{label} tail lo")
    d.path(body, f"{label} body", fill=fill, stroke=stroke, strokeWidth=sw)
    return L, R


def spine_eval(spine, widths, t):
    """Point + normal + local half-width at parameter t along the spine."""
    n = len(spine)
    f = t * (n - 1)
    i = min(n - 2, int(f))
    u = f - i
    x = spine[i][0] + (spine[i + 1][0] - spine[i][0]) * u
    y = spine[i][1] + (spine[i + 1][1] - spine[i][1]) * u
    w = widths[i] + (widths[i + 1] - widths[i]) * u
    dx = spine[i + 1][0] - spine[i][0]
    dy = spine[i + 1][1] - spine[i][1]
    ln = math.hypot(dx, dy) or 1
    return (x, y), (-dy / ln, dx / ln), (dx / ln, dy / ln), w / 2


def scales(spine, widths, t0, t1, step, col, label, op=55, sw=2.2):
    """Scallop arcs bulging toward the tail — the classic koinobori scale rows."""
    k = 0
    t = t0
    while t <= t1 + 1e-6:
        (x, y), (nx, ny), (ux, uy), hw = spine_eval(spine, widths, t)
        r = hw * 0.82
        sx_, sy_ = x - nx * r, y - ny * r
        ex, ey = x + nx * r, y + ny * r
        bx, by = x + ux * r * 1.15, y + uy * r * 1.15
        d.path(f"M{sx_:.1f},{sy_:.1f} Q{bx:.1f},{by:.1f} {ex:.1f},{ey:.1f}",
               f"{label} scale {k+1}", fill=NONE, stroke=col, strokeWidth=sw,
               opacity=op, cap="round")
        k += 1
        t += step


def carp(spine, widths, tail_len, tail_spread, body_fill, scale_col,
         fin_col, label):
    """Whole streamer: body path, belly band, scales, fin, mouth ring, eye."""
    L, R = streamer(spine, widths, tail_len, tail_spread, body_fill, label)
    # belly band: lighter ribbon along the lower edge
    belly = []
    for i in range(1, len(spine)):
        (x, y), (nx, ny), _, hw = spine_eval(spine, widths,
                                             i / (len(spine) - 1))
        belly.append((x - nx * hw * 0.72, y - ny * hw * 0.72))
    d.path(smooth(belly), f"{label} belly", fill=NONE, stroke=CREAM,
           strokeWidth=4.2, opacity=42, cap="round")
    # scale arcs
    scales(spine, widths, 0.16, 0.86, 0.115, scale_col, label)
    # pectoral fin, low near the head
    (fx, fy), (fnx, fny), (fux, fuy), _ = spine_eval(spine, widths, 0.14)
    bx = fx - fnx * 20
    by = fy - fny * 20
    d.path(f"M{bx:.1f},{by:.1f} Q{bx - fnx*26 + fux*10:.1f},{by - fny*26 + fuy*10:.1f} "
           f"{bx - fnx*34 + fux*30:.1f},{by - fny*34 + fuy*30:.1f} "
           f"Q{bx - fnx*12 + fux*30:.1f},{by - fny*12 + fuy*30:.1f} "
           f"{bx + fux*16:.1f},{by + fuy*16:.1f} Z",
           f"{label} fin", fill=fin_col, opacity=82, stroke=INK, strokeWidth=1.6)
    # mouth ring: the open windsock mouth, facing upwind (back along spine)
    mx, my = spine[0]
    ux = spine[0][0] - spine[1][0]
    uy = spine[0][1] - spine[1][1]
    ln = math.hypot(ux, uy) or 1
    ux, uy = ux / ln, uy / ln
    cx_, cy_ = mx + ux * widths[0] * 0.10, my + uy * widths[0] * 0.10
    ring_w = widths[0] * 0.62
    d.shape("ellipse", f"{label} mouth", x=cx_ - ring_w / 2, y=cy_ - ring_w * 0.42,
            width=ring_w, height=ring_w * 0.84, fill="#26150E",
            stroke="#F6EBD0", strokeWidth=3.2,
            rotation=round(math.degrees(math.atan2(uy, ux)) + 90, 1))
    # eye: bold ringed eye high on the head
    ex, ey = mx + ux * 12 - (-uy) * widths[0] * 0.20, \
             my + uy * 12 - (ux) * widths[0] * 0.20
    d.shape("ellipse", f"{label} eye ring", x=ex - 8.5, y=ey - 8.5,
            width=17, height=17, fill="#F6EBD0", stroke=INK, strokeWidth=1.8)
    d.shape("ellipse", f"{label} eye", x=ex - 3.4, y=ey - 3.4,
            width=6.8, height=6.8, fill=INK, stroke=NONE)


def cloud(cx, cy, s, label, op=70):
    """Small flat-bottomed puffy cloud."""
    for i, (dx, dy, r) in enumerate(
            [(-34, 2, 20), (-12, -8, 26), (14, -6, 24), (32, 2, 16)]):
        d.shape("ellipse", f"{label} puff {i+1}", x=cx + dx * s - r * s,
                y=cy + dy * s - r * s, width=2 * r * s, height=2 * r * s,
                fill=rad((0, "#FFFFFF", op), (0.65, "#FFFFFF", op * 0.8),
                         (1, "#FFFFFF", op * 0.25)), stroke=NONE)
    d.shape("ellipse", f"{label} base", x=cx - 40 * s, y=cy - 2 * s,
            width=80 * s, height=14 * s, fill="#FFFFFF", opacity=op * 0.5,
            stroke=NONE)


def seal_chop(cx=744, cy=214, s=62):
    """Vermilion chop inside the disc, top right; koi character."""
    x, y = cx - s / 2, cy - s / 2
    inside(cx + s / 2, cy + s / 2, 8, "chop BR")
    d.shape("ellipse", "Chop shadow", x=x + 3, y=y + 5, width=s, height=s,
            fill=INK, opacity=28, stroke=NONE)
    d.shape("rectangle", "Chop", x=x, y=y, width=s, height=s, radius=5,
            fill=lin((x, y), (x + s, y + s), (0, "#C0473A"), (1, "#7E1F1B")),
            stroke="#4E100E", strokeWidth=2.2)
    d.shape("rectangle", "Chop inner", x=x + 4.5, y=y + 4.5, width=s - 9,
            height=s - 9, radius=2.5, fill=NONE, stroke="#F6D9A0",
            strokeWidth=1.4, opacity=78)
    d.text("鯉", "Chop glyph", x=cx, y=cy + 11, size=30, font=CJK,
           color="#FBE6B4", justify="center")


# --- field -------------------------------------------------------------------
p.backdrop(top="#0B1826", bottom="#040810", glow=("#2A5A84", 14))
dust(d, n=44, r=402, colors=("#F6E3B8", "#C8DCE8"), seed=29, smin=1.0,
     smax=2.4, opmin=8, opmax=22, label="Backdrop dust")
seal_disc(p, SKY_HI, SKY_LO, rim=GOLD, rim2="#5E3A16")
# spring sun glow, high centre-right
glow(d, 560, 300, 300, "#FFF4C8", a=20, label="Sun glow")
glow(d, 560, 300, 130, "#FFF8DC", a=22, label="Sun core")
ring_dots(d, r=397, n=56, size=2.4, color=GOLD, opacity=30)

# --- green hills hugging the disc floor --------------------------------------
def rim_hill(a0, a1, depth_mid, wob, phase, fill, label, n=30, r=PR - 4):
    """Closed band inside the disc: inner rim arc a0..a1 + wavy crest back."""
    arc = [(PCX + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
            PCY + r * math.sin(math.radians(a0 + (a1 - a0) * i / n)))
           for i in range(n + 1)]
    top = []
    for i in range(n + 1):
        a = math.radians(a1 - (a1 - a0) * i / n)
        t = i / n
        dep = depth_mid * (math.sin(math.pi * t) ** 0.8)
        dep *= 1 + wob * math.sin(phase + i * 0.85)
        rr = r - dep
        top.append((PCX + rr * math.cos(a), PCY + rr * math.sin(a)))
    d.path(smooth(arc) + smooth(top, move=False) + " Z", label,
           fill=fill, stroke=NONE)


rim_hill(18, 162, 132, 0.10, 0.0,
         lin((0, 640), (0, 890), (0, "#5E8A50"), (1, HILL_LO)),
         "Hills far")
rim_hill(32, 148, 196, 0.07, 1.9,
         lin((0, 700), (0, 890), (0, HILL), (1, "#142A18")),
         "Hills near")

# --- mast --------------------------------------------------------------------
# taut flying line first (carps pin to it); pole drawn after, in front
POLE_X = 292
inside(POLE_X, 152, 10, "pole top")
inside(POLE_X, 790, 10, "pole base")
LINE_TOP = (POLE_X + 8, 158)
LINE_BOT = (694, 706)
inside(*LINE_BOT, 8, "line anchor")
d.path(f"M{LINE_TOP[0]:.1f},{LINE_TOP[1]:.1f} "
       f"Q{(LINE_TOP[0]+LINE_BOT[0])/2 + 30:.1f},{(LINE_TOP[1]+LINE_BOT[1])/2:.1f} "
       f"{LINE_BOT[0]:.1f},{LINE_BOT[1]:.1f}",
       "Flying line", fill=NONE, stroke="#4A3418", strokeWidth=3.0,
       cap="round")
# anchor peg + short tie at the bottom of the line
d.path(f"M{LINE_BOT[0]:.1f},{LINE_BOT[1]:.1f} L{LINE_BOT[0]+26:.1f},{LINE_BOT[1]+34:.1f}",
       "Line tie", fill=NONE, stroke="#4A3418", strokeWidth=2.4, cap="round")

# bamboo mast: tapered ribbon + node rings + yaguruma pinwheel
d.path(f"M{POLE_X - 7:.1f},792 L{POLE_X - 4.5:.1f},150 L{POLE_X + 4.5:.1f},150 "
       f"L{POLE_X + 7:.1f},792 Z",
       "Mast", fill=lin((POLE_X - 7, 0), (POLE_X + 7, 0),
                        (0, "#8A6A34"), (0.55, "#C9A45C"), (1, "#7A5222")),
       stroke=INK, strokeWidth=2.6)
for i, ny in enumerate((330, 500, 668)):
    d.shape("rectangle", f"Mast node {i+1}", x=POLE_X - 6.5, y=ny, width=13,
            height=7, radius=3, fill="#5E3A16", stroke=NONE, opacity=85)
# mast base footing
d.shape("ellipse", "Mast foot", x=POLE_X - 22, y=782, width=44, height=14,
        fill=rad((0, "#2A1A0E", 60), (1, "#2A1A0E", 0)), stroke=NONE)
# yaguruma pinwheel at the masthead
WCX, WCY, WR = POLE_X, 132, 24
d.shape("ellipse", "Wheel rim", x=WCX - WR, y=WCY - WR, width=2 * WR,
        height=2 * WR, fill=NONE, stroke=GOLD, strokeWidth=3.4)
for i in range(6):
    a = math.radians(i * 60 - 90)
    d.shape("line", f"Wheel spoke {i+1}", x1=round(WCX, 1), y1=round(WCY, 1),
            x2=round(WCX + WR * 0.94 * math.cos(a), 1),
            y2=round(WCY + WR * 0.94 * math.sin(a), 1), stroke=GOLD,
            strokeWidth=2.4, opacity=85, cap="round")
d.shape("ellipse", "Wheel hub", x=WCX - 4.5, y=WCY - 4.5, width=9, height=9,
        fill=GOLD_HI, stroke=INK, strokeWidth=1.4)

# --- point on the flying line ------------------------------------------------
def line_pt(t):
    """Quadratic bezier LINE_TOP -> ctrl -> LINE_BOT at parameter t."""
    cxq = (LINE_TOP[0] + LINE_BOT[0]) / 2 + 30
    cyq = (LINE_TOP[1] + LINE_BOT[1]) / 2
    mt = 1 - t
    x = mt * mt * LINE_TOP[0] + 2 * mt * t * cxq + t * t * LINE_BOT[0]
    y = mt * mt * LINE_TOP[1] + 2 * mt * t * cyq + t * t * LINE_BOT[1]
    return (x, y)


# --- the carps -----------------------------------------------------------------
# black magoi (father) — largest, highest
S1 = [line_pt(0.10), (line_pt(0.10)[0] + 96, line_pt(0.10)[1] - 38),
      (line_pt(0.10)[0] + 196, line_pt(0.10)[1] - 6),
      (line_pt(0.10)[0] + 282, line_pt(0.10)[1] - 44)]
W1 = [62, 56, 40, 18]
carp(S1, W1, 46, 30, lin((S1[0][0], S1[0][1]), (S1[-1][0], S1[-1][1]),
                          (0, "#3E5468"), (0.5, "#22303E"), (1, "#121C26")),
     "#9FC0D8", "#C0392B", "Magoi")

# red higoi (mother) — middle
S2 = [line_pt(0.44), (line_pt(0.44)[0] + 82, line_pt(0.44)[1] - 30),
      (line_pt(0.44)[0] + 166, line_pt(0.44)[1] - 2),
      (line_pt(0.44)[0] + 236, line_pt(0.44)[1] - 34)]
W2 = [52, 47, 34, 15]
carp(S2, W2, 38, 25, lin((S2[0][0], S2[0][1]), (S2[-1][0], S2[-1][1]),
                          (0, "#E86A4A"), (0.5, "#C0392B"), (1, "#7E1F1B")),
     "#FBD2A8", "#F2A33C", "Higoi")

# blue child — smallest, lowest
S3 = [line_pt(0.70), (line_pt(0.70)[0] + 66, line_pt(0.70)[1] - 22),
      (line_pt(0.70)[0] + 132, line_pt(0.70)[1] + 0),
      (line_pt(0.70)[0] + 188, line_pt(0.70)[1] - 26)]
W3 = [42, 38, 27, 12]
carp(S3, W3, 30, 20, lin((S3[0][0], S3[0][1]), (S3[-1][0], S3[-1][1]),
                          (0, "#5FA4D2"), (0.5, "#2E6EAE"), (1, "#173E66")),
     "#C8E4F2", "#E8791F", "Kodomo")

# --- clouds + wind ---------------------------------------------------------------
cloud(430, 596, 0.8, "Cloud low", op=55)
cloud(642, 148, 0.62, "Cloud high", op=48)
cloud(408, 322, 0.5, "Cloud mid", op=42)
# wind streaks: thin pale arcs sweeping right
for i, (x0, y0, x1, y1, cq) in enumerate([
        (180, 420, 330, 404, 22), (700, 470, 812, 452, 18),
        (240, 300, 360, 282, 16), (560, 660, 690, 646, 20)]):
    d.path(f"M{x0},{y0} Q{(x0 + x1) / 2:.0f},{(y0 + y1) / 2 - cq} {x1},{y1}",
           f"Wind {i+1}", fill=NONE, stroke="#FFFFFF", strokeWidth=2.6,
           opacity=26, cap="round")

# --- seal + caption --------------------------------------------------------------
seal_chop()
caption(p, "GOLDEN WEEK", "29 APRIL – 6 MAY · KOINOBORI",
        name_color="#F4EBD4", sub_color="#C9A46A",
        name_size=52, tracking_name=82, sub_size=21, tracking_sub=46,
        sub_font=SERIF)
p.finish(SLUG)
