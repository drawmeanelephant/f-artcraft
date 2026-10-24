#!/usr/bin/env python3
"""app-screens figcraft sheet V1R00 — issue #1263.

The six highest-traffic VirelaiOS app screens drawn as windows at their
declare-block natural sizes (user/go/<app>/main.go, surveyed in the fleet
sheet) in the shipped layout language — tokens from vkit/DARK, chrome per
docs/ui-primitives.md v2 (titlebar 28, spacing 2/4/8/16, BorderW 1,
FocusW 2, radius 4/8/pill). This is a design-iteration doc under
virelai/design/, not delivered art.

Type truth: UI text Inter, code/terminal Fira Code, captions/digits
Source Sans 3 (Virelai Sans has no digit glyphs), sheet title Virelai Sans.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE
from virelai.vkit import DARK, TITLEBAR_H, ROW_H, RADIUS_CONTROL, RADIUS_WINDOW

T = DARK
UI, MONO, DISP, DIG = "Inter", "Fira Code", "Virelai Sans", "Source Sans 3"
CANVAS = "#101418"      # sheet field, matches the fleet doc
TITLE_H = TITLEBAR_H    # 28
RAIL_H = 22             # gotabwm tab rail

d = Draw()
d.new_doc("VirelaiOS — key app screens", 1864, 1152)
R_ = lambda x, y, w, h, n, f, **kw: d.shape("rectangle", n, x=x, y=y,
                                             width=w, height=h, fill=f, **kw)
R_(0, 0, 1864, 1152, "sheet field", CANVAS, stroke=NONE)


# ---------------------------------------------------------------- helpers
def R(x, y, w, h, name, fill, stroke=NONE, sw=1, op=None):
    kw = dict(x=x, y=y, width=w, height=h, fill=fill, stroke=stroke, strokeWidth=sw)
    if op is not None:
        kw["opacity"] = op
    return d.shape("rectangle", name, **kw)


def E(x, y, w, h, name, fill, stroke=NONE, sw=1, op=None):
    kw = dict(x=x, y=y, width=w, height=h, fill=fill, stroke=stroke, strokeWidth=sw)
    if op is not None:
        kw["opacity"] = op
    return d.shape("ellipse", name, **kw)


def RR(x, y, w, h, r, name, fill, stroke=NONE, sw=1):
    r = min(r, w / 2, h / 2)
    p = (f"M{x+r},{y} L{x+w-r},{y} Q{x+w},{y} {x+w},{y+r} L{x+w},{y+h-r} "
         f"Q{x+w},{y+h} {x+w-r},{y+h} L{x+r},{y+h} Q{x},{y+h} {x},{y+h-r} "
         f"L{x},{y+r} Q{x},{y} {x+r},{y} Z")
    return d.path(p, name, fill=fill, stroke=stroke, strokeWidth=sw)


def TXT(s, name, x, y, size=11.0, font=UI, color=None, justify=None, trk=None):
    kw = dict(x=x, y=y, size=size, font=font, color=color or T["Ink"])
    if justify:
        kw["justify"] = justify
    r = d.text(s, name, **kw)
    if trk and r:
        d.cmd("text.setStyle", f"{name} tracking", id=r["id"], tracking=trk)
    return r


def window(x, y, w, h, title):
    """Floating-window frame: 8-radius plate, 28px titlebar, Border stroke."""
    RR(x, y, w, h + TITLE_H, RADIUS_WINDOW, f"win/{title}", T["Bg"], T["Border"], 1)
    d.path(f"M{x+8},{y} L{x+w-8},{y} Q{x+w},{y} {x+w},{y+8} L{x+w},{y+TITLE_H} "
           f"L{x},{y+TITLE_H} L{x},{y+8} Q{x},{y} {x+8},{y} Z",
           f"titlebar/{title}", fill=T["Surface"], stroke=NONE)
    R(x, y + TITLE_H - 1, w, 1, f"title rule/{title}", T["Border"])
    TXT(title, f"wtitle/{title}", x + 10, y + 8, 13, UI, T["Text"])
    for i, g in enumerate(["_", "[]", "x"]):
        bx = x + w - 10 - (3 - i) * 22
        RR(bx, y + 6, 16, 16, RADIUS_CONTROL, f"ctl{i}/{title}", T["BtnIdle"])
        TXT(g, f"ctlg{i}/{title}", bx + 8, y + 8, 9, MONO,
            T["Danger"] if g == "x" else T["InkMuted"], justify="center")
    return y + TITLE_H


def rail(x, y, w, cells, active=0, name="rail"):
    """Tab rail in the gotabwm idiom: cells split the width, close-x right,
    accent leading edge on the focused cell. App tab strips reuse it."""
    R(x, y, w, RAIL_H, name, T["ChromeBg"])
    R(x, y + RAIL_H - 1, w, 1, f"{name} rule", T["Rule"])
    n = max(1, len(cells))
    cw = w // n
    for i, label in enumerate(cells):
        cx, foc = x + i * cw, i == active
        R(cx, y, cw - 1, RAIL_H - 1, f"{name} tab/{label}",
          T["Surface"] if foc else T["ChromeBg"])
        if foc:
            R(cx, y, 3, RAIL_H - 1, f"{name} edge/{label}", T["Accent"])
        TXT(label, f"{name} lbl/{label}", cx + 8, y + 5, 11, UI,
            T["Ink"] if foc else T["InkMuted"])
        TXT("x", f"{name} x/{label}", cx + cw - 12, y + 5, 10, UI, T["InkMuted"])
    return y + RAIL_H


def dockband(x, y, w, h=20, name="band"):
    """Bottom band: status bars, find bars — ChromeBg strip + top rule."""
    R(x, y, w, h, name, T["ChromeBg"])
    R(x, y, w, 1, f"{name} rule", T["Rule"])
    return y


def toast(x, y, w, msg, name="toast"):
    """Floating toast: Surface card r8, accent left edge, 11px label."""
    RR(x, y, w, 28, RADIUS_WINDOW, name, T["Surface"], T["Border"], 1)
    R(x, y, 2, 28, f"{name} edge", T["Accent"])
    TXT(msg, f"{name} msg", x + 12, y + 8, 11, UI, T["Ink"])


def btn(x, y, w, h, label, name, face=None, fg=None, mono=True):
    RR(x, y, w, h, RADIUS_CONTROL, name, face or T["BtnIdle"])
    TXT(label, f"{name} lbl", x + w / 2, y + h / 2 - 6, 10,
        MONO if mono else UI, fg or T["Ink"], justify="center")


def findbar(x, y, w, query, count, name="find", hint="^G"):
    """Open find/goto bar: ChromeBg band, accent-edged query field, match
    count, chord hint at right."""
    dockband(x, y, w, 28, name)
    TXT(name, f"{name} lbl", x + 10, y + 8, 11, MONO, T["Muted"])
    qx = x + 10 + (len(name) + 1) * 7
    RR(qx, y + 4, 168, 20, RADIUS_CONTROL, f"{name} field", T["Surface"], T["Accent"], 2)
    TXT(query, f"{name} q", qx + 8, y + 8, 11, MONO, T["Ink"])
    R(qx + 8 + len(query) * 7, y + 7, 2, 14, f"{name} caret", T["Accent"])
    TXT(count, f"{name} n", qx + 176, y + 8, 11, MONO, T["Muted"])
    TXT(hint, f"{name} hint", x + w - 10, y + 8, 10, MONO, T["Muted"], justify="right")


def statusbar(x, y, w, msg, name="status"):
    dockband(x, y, w, 20, name)
    TXT(msg, f"{name} txt", x + 8, y + 4, 10, MONO, T["InkMuted"])


def caption(x, y, app, title, w, h, feats):
    TXT(f"{app} — {title}", f"cap/{app}", x, y, 12, UI, T["Ink"])
    TXT(f"{w}x{h} natural (declare block) · {feats}", f"capsub/{app}",
        x, y + 18, 10, DIG, T["Muted"])


# ---------------------------------------------------------------- sheet head
TXT("VIRELAIOS", "eyebrow", 48, 30, 15, DISP, T["Muted"], trk=360)
TXT("KEY APP SCREENS", "title", 48, 54, 26, DISP, T["Text"], trk=140)
TXT("the six highest-traffic apps at their declare-block window sizes — "
    "design-iteration sheet · chrome per docs/ui-primitives.md v2 · "
    "tokens theme.go dark (boot default) · #1263",
    "subtitle", 48, 92, 12, UI, T["Muted"])

COL, ROWY = [48, 664, 1280], [130, 672]
CELL_W = 568


def cell(col, row, w):
    return COL[col] + (CELL_W - w) / 2, ROWY[row]


# ================================================================ GOSH 512x384
def gosh(x, y):
    W, H = 512, 384
    y0 = window(x, y, W, H, "Shell — GOSH.ELF")
    lines = [
        "gosh$ uname -a", "VirelaiOS sexiburger aarch64-virt",
        "gosh$ ls /host", "APPS.TXT  DOCUMENTS/  GOMAIL.TXT  SNAPSHOTS/",
        "gosh$ exec GOTOP.ELF &", "gotop: open id=7",
        "gosh$ ./deploy.sh --check", "deploy: dry run ok · 14 steps",
    ]
    ly = y0 + 10
    for i, ln in enumerate(lines):
        if i == 1:
            R(x + 6, ly - 2, 288, 16, "sel", T["Selection"])  # drag selection
        TXT(ln, f"gosh{i}", x + 10, ly, 11, MONO, T["Ink"])
        ly += 17
    TXT("gosh$ ", "prompt", x + 10, ly, 11, MONO, T["Ink"])
    R(x + 52, ly + 2, 7, 12, "caret", T["Accent"])            # block caret
    findbar(x, y0 + H - 28, W, "sexiburger", "1/1", "find", "ctrl+shift+g")
    return y + TITLE_H + H


# ================================================================ GOEDIT 512x384
def goedit(x, y):
    W, H = 512, 384
    y0 = window(x, y, W, H, "Code Editor — GOEDIT.ELF")
    R(x, y0, W, 24, "menubar", T["Surface"])
    R(x, y0 + 23, W, 1, "menu rule", T["Rule"])
    for i, m in enumerate(["File", "Edit", "View", "Go", "Prof"]):
        TXT(m, f"mb{i}", x + 8 + i * 48, y0 + 6, 11, UI, T["Ink"])
    ty = rail(x, y0 + 24, W, ["main.go", "util.go", "prof.out"], 0, "doctabs")
    code = ["package main", "", 'import "virelai/vi"', "",
            "func main() {", "\tapp := vi.Open(\"GOEDIT.ELF\")",
            "\tapp.Declare(512, 384)", "\tfor app.Poll() {", "\t\tapp.Paint()",
            "\t}", "}", "", "func render(f *Frame) {", "\tf.Tab(main.go)",
            "\tf.Gutter(heat(prof.out))", "}"]
    # heat gutter: per-function profile segments (--prof=prof.out)
    heats = [0.05, 0.05, 0.1, 0.1, 0.9, 0.9, 0.7, 0.55, 0.3, 0.2, 0.2,
             0.0, 0.85, 0.6, 0.4, 0.3]
    def heat_col(v):
        return T["Danger"] if v > 0.75 else T["Warning"] if v > 0.4 else \
            T["BtnIdle"] if v > 0 else T["Gutter"]
    gy, gw, lh = ty + 4, 44, 16
    for i, ln in enumerate(code):
        ry = gy + i * lh
        if i == 5:
            R(x + gw, ry - 1, W - gw, lh, "curln", T["Selection"])
        R(x + gw - 4, ry, 4, lh - 2, f"heat{i}", heat_col(heats[i]))
        TXT(str(i + 1), f"ln{i}", x + gw - 10, ry + 2, 10, MONO,
            T["InkMuted"], justify="right")
        TXT(ln.replace("\t", "    "), f"code{i}", x + gw + 8, ry + 2, 11,
            MONO, T["Muted"] if ln.startswith("package") or ln.startswith("import") else T["Ink"])
    TXT("heat ← --prof=prof.out", "heatlbl", x + gw + 8,
        y0 + H - 28 - 50, 9, DIG, T["Warning"])
    findbar(x, y0 + H - 52, W, "Paint", "3/7", "find", "ctrl+g goto")
    statusbar(x, y0 + H - 20, W,
              "main.go · Ln 6, Col 5 · utf-8 · go · prof.out loaded")
    return y + TITLE_H + H


# ================================================================ GOFILES 512x384
def gofiles(x, y):
    W, H = 512, 384
    y0 = window(x, y, W, H, "Files — GOFILES.ELF")
    # toolbar
    R(x, y0, W, 28, "toolbar", T["Surface"])
    R(x, y0 + 27, W, 1, "tb rule", T["Rule"])
    for i, g in enumerate(["<", ">", "^"]):
        btn(x + 6 + i * 24, y0 + 4, 20, 20, g, f"nav{i}")
    for i, a in enumerate(["mkdir", "copy", "paste"]):
        TXT(a, f"act{i}", x + 92 + i * 44, y0 + 9, 10, UI, T["InkMuted"])
    # path bar
    dockband(x, y0 + 28, W, 22, "pathbar")
    TXT("/host", "crumb0", x + 10, y0 + 33, 11, MONO, T["InkMuted"])
    TXT("/ DOCUMENTS", "crumb1", x + 52, y0 + 33, 11, MONO, T["Accent"])
    # list pane
    lw = 296
    R(x, y0 + 50, lw, H - 50 - 20, "listpane", T["ChromeBg"])
    rows = ["..", "CONTRACT.TXT", "INVOICE.PDF", "MAP.QOI",
            "NOTES/", "PACKING.TXT", "VCARD.VCF"]
    for i, r in enumerate(rows):
        ry = y0 + 58 + i * 19
        if r == "VCARD.VCF":
            R(x + 2, ry - 2, lw - 4, 18, "sel", T["Selection"])
            R(x + 2, ry - 2, 3, 18, "sel edge", T["Accent"])
        TXT(r, f"f{i}", x + 12, ry, 11, MONO,
            T["Ink"] if r != ".." else T["InkMuted"])
    R(x + lw, y0 + 50, 1, H - 50 - 20, "pane rule", T["Rule"])
    # quicklook pane — .vcf contact card
    qx = x + lw + 1
    TXT("VCARD.VCF — contact", "ql t", qx + 14, y0 + 60, 10,
        UI, T["Muted"])
    RR(qx + 12, y0 + 82, W - lw - 25, 148, RADIUS_WINDOW, "vcf card",
       T["Surface"], T["Border"], 1)
    E(qx + 24, y0 + 94, 44, 44, "avatar", T["Accent"])
    TXT("AV", "av in", qx + 46, y0 + 107, 14, UI, T["OnAccent"], justify="center")
    TXT("Ada Virel", "vc name", qx + 78, y0 + 98, 13, UI, T["Ink"])
    TXT("ada@virelai.os", "vc mail", qx + 78, y0 + 116, 10, UI, T["Muted"])
    for i, (k, v) in enumerate([("TEL", "+1-555-0123"),
                                ("ORG", "Storytold Systems"),
                                ("NOTE", "art pipeline liaison")]):
        TXT(k, f"vck{i}", qx + 24, y0 + 152 + i * 18, 9, MONO, T["Muted"])
        TXT(v, f"vcv{i}", qx + 64, y0 + 152 + i * 18, 10, UI, T["InkMuted"])
    toast(x + 10, y0 + H - 62, 190, "path copied to clipboard")
    statusbar(x, y0 + H - 20, W,
              "7 items · sort name · ^Q quicklook · / filter")
    return y + TITLE_H + H


# ================================================================ WEB 512x384
def web(x, y):
    W, H = 512, 384
    y0 = window(x, y, W, H, "Web — WEB.ELF")
    ty = rail(x, y0, W, ["10.0.0.2 — docs", "apps.txt"], 0, "tabs")
    # address row
    for i, g in enumerate(["<", ">", "R"]):
        btn(x + 6 + i * 24, ty + 5, 20, 20, g, f"webnav{i}")
    RR(x + 82, ty + 4, W - 90, 22, RADIUS_CONTROL, "url field",
       T["Surface"], T["Accent"], 2)
    TXT("http://10.0.0.2/docs/", "url", x + 90, ty + 9, 10, MONO, T["Ink"])
    py = ty + 30
    R(x, py, W, H - (py - y0) - 18, "page", T["ChromeBg"])
    TXT("VirelaiOS documentation", "h1", x + 24, py + 18, 16, UI, T["Ink"])
    paras = ["The desktop is a tab rail — one row of live apps.",
             "Click a cell, or Ctrl+T for the launcher. Every",
             "app is a full-viewport tab; windows keep their",
             "declare-block natural size in the floating layer."]
    for i, p in enumerate(paras):
        TXT(p, f"para{i}", x + 24, py + 46 + i * 16, 11, UI, T["InkMuted"])
    TXT("» desktop.md   » ui-primitives.md", "links", x + 24,
        py + 46 + 4 * 16 + 8, 11, UI, T["Accent"])
    RR(x + 24, py + 150, 200, 110, RADIUS_CONTROL, "figure", T["Surface"],
       T["Border"], 1)
    E(x + 44, py + 170, 40, 40, "fig dot", T["Accent"])
    TXT("WALLPAPER.QOI", "fig cap", x + 96, py + 184, 9, MONO, T["InkMuted"])
    TXT("figure: the shipped wallpaper fixture", "fig note", x + 32,
        py + 268, 9, UI, T["Muted"])
    statusbar(x, y0 + H - 18, W, "200 · 4.1 KB · webrender · idle")
    return y + TITLE_H + H


# ================================================================ GOCALC 512x384
def gocalc(x, y):
    W, H = 512, 384
    y0 = window(x, y, W, H, "64-bit Calc — GOCALC.ELF")
    # mode chips
    for i, m in enumerate(["DEC", "HEX", "OCT", "BIN"]):
        cx = x + 8 + i * 54
        on = m == "HEX"
        RR(cx, y0 + 8, 48, 20, 10, f"mode {m}",
           T["Accent"] if on else T["BtnIdle"])
        TXT(m, f"modelbl {m}", cx + 24, y0 + 13, 10, MONO,
            T["OnAccent"] if on else T["InkMuted"], justify="center")
    RR(x + W - 62, y0 + 8, 54, 20, 10, "prog chip", T["Surface"])
    TXT("prog", "prog lbl", x + W - 35, y0 + 13, 10, MONO, T["InkMuted"],
        justify="center")
    # display
    TXT("0xFF & 0x0F", "hist", x + 10, y0 + 36, 10, MONO, T["InkMuted"])
    RR(x + 8, y0 + 52, W - 16, 46, RADIUS_CONTROL, "display", T["Surface"])
    TXT("0x0F", "disp", x + W - 20, y0 + 62, 18, MONO, T["Ink"], justify="right")
    TXT("= 15", "disp dec", x + W - 20, y0 + 84, 10, DIG, T["Muted"], justify="right")
    # tape pane (left) + keypad (right)
    ty, th = y0 + 106, H - 106 - 8
    R(x + 8, ty, 172, th, "tape", T["ChromeBg"])
    TXT("TAPE", "tape t", x + 16, ty + 8, 9, UI, T["Muted"], trk=180)
    tape = ["12 * 3.5", "  = 42", "0xFF & 0x0F", "  = 0x0F", "1 << 8",
            "  = 256", "0x2A | 0x10", "  = 0x3A"]
    for i, ln in enumerate(tape):
        TXT(ln, f"tape{i}", x + 16, ty + 30 + i * 16, 10, MONO,
            T["Muted"] if ln.startswith(" ") else T["Ink"])
    pad = [["A", "B", "C", "/"], ["D", "E", "F", "*"], ["7", "8", "9", "-"],
           ["4", "5", "6", "+"], ["1", "2", "3", "="], ["0", "<<", ">>", "&"]]
    kx, kw = x + 188, W - 188 - 8
    bw = (kw - 3 * 8) // 4
    bh = (th - 5 * 6) // 6
    for r, row in enumerate(pad):
        for ci, lbl in enumerate(row):
            face = T["Surface"] if lbl == "=" else T["BtnIdle"]
            btn(kx + ci * (bw + 8), ty + r * (bh + 6), bw, bh, lbl,
                f"k{r}{ci}", face=face)
    return y + TITLE_H + H


# ================================================================ GOSET 560x360
def goset(x, y):
    W, H = 560, 360
    y0 = window(x, y, W, H, "Settings — GOSET.ELF")
    nav = 132
    R(x, y0, nav, H - 20, "schema nav", T["ChromeBg"])
    TXT("SETTINGS.TXT", "nav hdr", x + 10, y0 + 10, 9, MONO, T["Muted"])
    for i, s in enumerate(["GENERAL", "THEME", "INPUT", "AUDIO", "A11Y"]):
        ry = y0 + 34 + i * 26
        if s == "THEME":
            R(x + 2, ry - 4, nav - 4, 24, "navsel", T["Selection"])
            R(x + 2, ry - 4, 3, 24, "navsel edge", T["Accent"])
        TXT(s, f"nav {s}", x + 12, ry, 11, UI,
            T["Ink"] if s == "THEME" else T["InkMuted"])
    R(x + nav, y0, 1, H - 20, "nav rule", T["Rule"])
    # edit pane
    ex = x + nav + 16
    TXT("theme — 4 keys", "sect t", ex, y0 + 12, 13, UI, T["Ink"])
    rows = [("theme", "dark", "dd"), ("a11y.contrast", "off", "tg"),
            ("a11y.text_scale", "1.0", "sl"), ("a11y.reduce_motion", "on", "tg")]
    for i, (k, v, kind) in enumerate(rows):
        ry = y0 + 46 + i * 40
        TXT(k, f"key{i}", ex, ry + 5, 11, MONO, T["Ink"])
        if kind == "dd":
            RR(ex + 190, ry - 2, 140, 24, RADIUS_CONTROL, "dd", T["Surface"],
               T["Border"], 1)
            TXT(v, "ddv", ex + 198, ry + 3, 11, UI, T["Ink"])
            TXT("v", "ddc", ex + 318, ry + 5, 9, UI, T["Muted"])
        elif kind == "tg":
            on = v == "on"
            RR(ex + 190, ry, 40, 20, 10, "tg",
               T["Accent"] if on else T["BtnIdle"])
            E(ex + (212 if on else 192), ry + 2, 16, 16, "tgk",
              T["OnAccent"] if on else T["Muted"])
            TXT(v, "tgv", ex + 240, ry + 4, 10, MONO, T["Muted"])
        else:
            RR(ex + 190, ry + 8, 110, 6, 3, "slbg", T["BtnIdle"])
            E(ex + 248, ry + 3, 16, 16, "slk", T["Accent"])
            TXT(v, "slv", ex + 312, ry + 5, 10, DIG, T["Muted"])
    # live palette preview
    for i, tok in enumerate(["Bg", "Surface", "Border", "Accent", "Text"]):
        R(ex + i * 36, y0 + H - 64, 32, 22, f"pal {tok}", T[tok],
          T["Border"], 1)
    TXT("live palette preview", "pal lbl", ex, y0 + H - 36, 9, UI, T["Muted"])
    statusbar(x, y0 + H - 20, W, "SETTINGS.TXT · 4 keys · autosave on")
    return y + TITLE_H + H


# ---------------------------------------------------------------- layout
APPS = [
    ("GOSH.ELF", "Shell", 512, 384, gosh,
     "prompt + scrollback · find bar open (ctrl+shift+g) · selection"),
    ("GOEDIT.ELF", "Code Editor", 512, 384, goedit,
     "doc tabs · gutter + per-function heat (--prof=) · find/goto bar"),
    ("GOFILES.ELF", "Files", 512, 384, gofiles,
     "list + QuickLook .vcf card · toolbar · path bar · toast"),
    ("WEB.ELF", "Web", 512, 384, web,
     "tab strip · address row (focused) · rendered page"),
    ("GOCALC.ELF", "64-bit Calc", 512, 384, gocalc,
     "programmer mode · tape pane · hex pad"),
    ("GOSET.ELF", "Settings", 560, 360, goset,
     "schema list · edit pane · live palette"),
]
for i, (app, title, w, h, fn, feats) in enumerate(APPS):
    cx, cy = cell(i % 3, i // 3, w)
    fn(cx, cy)
    caption(cx, cy + TITLE_H + h + 14, app, title, w, h, feats)

r = d.finish("app-screens-V1R00")
