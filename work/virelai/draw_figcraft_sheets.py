#!/usr/bin/env python3
"""Generate VirelaiOS figcraft design templates.

Emits three .figcraft documents (zip of document.json):
  seat-shell.figcraft  - seat chrome: desktop, anatomy, menus, notify, lock, tour
  apps.figcraft        - one window frame per app in image/apps.txt (31)
  tokens.figcraft      - colors / type / geometry / components / variables

Token truth: user/go/theme/theme.go (Dark = boot default, Light, DarkHC,
LightHC) and docs/ui-primitives.md (v2 contract: radii 4/8/pill, spacing
2/4/8/16, BorderW 1, FocusW 2, titlebar 28, rail 22, shadow dy4 blur16
a=0x40). Layout truth: user/go/<app> declare blocks (natW/natH) and
paint code, surveyed 2026-10-24.
"""

import json
import math
import os
import zipfile

# ---------------------------------------------------------------- theme

DARK = dict(
    Bg=0x182026, Surface=0x222D35, Border=0x334155, Text=0xFFFFFF,
    Muted=0x94A3B8, Accent=0x3B82F6, BtnIdle=0x2D3748, BtnHover=0x4A5568,
    BtnPressed=0x1A202C, Success=0x22C55E, Danger=0xEF4444, Warning=0xF59E0B,
    OnAccent=0xFFFFFF, Caret=0x3B82F6, Selection=0x2A4460, Gutter=0x0B0E11,
    Ink=0xE6EDF3, InkMuted=0x8B98A5, ChromeBg=0x11171C, Rule=0x2E3A44,
    Ok=0x3FB950, Shadow=0x000000, WallpaperTop=0x1A1A2E, WallpaperBot=0x0A0A14,
)
LIGHT = dict(
    Bg=0xF1F5F9, Surface=0xFFFFFF, Border=0xCBD5E1, Text=0x0F172A,
    Muted=0x64748B, Accent=0x2563EB, BtnIdle=0xE2E8F0, BtnHover=0xCBD5E1,
    BtnPressed=0x94A3B8, Success=0x16A34A, Danger=0xDC2626, Warning=0xD97706,
    OnAccent=0xFFFFFF, Caret=0x2563EB, Selection=0xBFDBFE, Gutter=0xE5E7EB,
    Ink=0x0F172A, InkMuted=0x64748B, ChromeBg=0xE2E8F0, Rule=0xCBD5E1,
    Ok=0x16A34A, Shadow=0x0F172A, WallpaperTop=0xF1F5F9, WallpaperBot=0xE2E8F0,
)
DARKHC = dict(
    Bg=0x000000, Surface=0x0D1117, Border=0x8B949E, Text=0xFFFFFF,
    Muted=0xB1BAC4, Accent=0x58A6FF, BtnIdle=0x1C2128, BtnHover=0x30363D,
    BtnPressed=0x000000, Success=0x3FB950, Danger=0xFF7B72, Warning=0xD29922,
    OnAccent=0xFFFFFF, Caret=0x58A6FF, Selection=0x1F3A5F, Gutter=0x000000,
    Ink=0xFFFFFF, InkMuted=0xB1BAC4, ChromeBg=0x000000, Rule=0x30363D,
    Ok=0x3FB950, Shadow=0x000000, WallpaperTop=0x0A0A14, WallpaperBot=0x000000,
)
LIGHTHC = dict(
    Bg=0xFFFFFF, Surface=0xF6F8FA, Border=0x24292F, Text=0x000000,
    Muted=0x3D444D, Accent=0x0550AE, BtnIdle=0xE8EBF0, BtnHover=0xD0D7DE,
    BtnPressed=0x8C959F, Success=0x116329, Danger=0xA40E26, Warning=0x744500,
    OnAccent=0xFFFFFF, Caret=0x0550AE, Selection=0xADD6FF, Gutter=0xE8EBF0,
    Ink=0x000000, InkMuted=0x3D444D, ChromeBg=0xFFFFFF, Rule=0x24292F,
    Ok=0x116329, Shadow=0x0F172A, WallpaperTop=0xFFFFFF, WallpaperBot=0xE8EBF0,
)

TOKEN_ORDER = [
    "Bg", "Surface", "Border", "Text", "Muted", "Accent",
    "BtnIdle", "BtnHover", "BtnPressed", "Success", "Danger", "Warning",
    "OnAccent", "Caret", "Selection", "Gutter", "Ink", "InkMuted",
    "ChromeBg", "Rule", "Ok", "Shadow", "WallpaperTop", "WallpaperBot",
]

T = DARK  # templates paint the boot-default dark table

UI = "Inter"
MONO = "Fira Code"


def c(hexv, a=1.0):
    return {"r": ((hexv >> 16) & 0xFF) / 255.0,
            "g": ((hexv >> 8) & 0xFF) / 255.0,
            "b": (hexv & 0xFF) / 255.0, "a": a}


def solid(hexv, a=1.0):
    return {"type": "solid", "color": c(hexv, a),
            "opacity": 1.0, "visible": True, "blend": "normal"}


def vgrad(top, bot):
    return {"type": "gradient", "kind": "linear",
            "stops": [{"position": 0.0, "color": c(top)},
                      {"position": 1.0, "color": c(bot)}],
            "from": [0.5, 0.0], "to": [0.5, 1.0], "width": [0.0, 0.0],
            "opacity": 1.0, "visible": True, "blend": "normal"}


class Doc:
    def __init__(self, name, page_name, bg_hex):
        self.name = name
        self.next_id = 2
        self.nodes = {}
        self.nodes[1] = {
            "id": 1, "name": page_name, "type": "page",
            "background": c(bg_hex), "flows": [],
            "prototype": {"device": "None", "background": c(bg_hex),
                          "rotation": "portrait"},
            "guides": [], "children": [], "width": 0.0, "height": 0.0}
        self.var_ids = {}      # hex -> VariableID  (dark-mode values)
        self.variables = {"collections": [], "variables": []}

    def _id(self):
        i = self.next_id
        self.next_id += 1
        return i

    def _node(self, parent, x, y, w, h, name, typ, extra):
        i = self._id()
        n = {"id": i, "name": name, "type": typ, "parent": parent,
             "blend": "normal",
             "transform": [1.0, 0.0, 0.0, 1.0, float(x), float(y)],
             "width": float(w), "height": float(h)}
        n.update(extra)
        self.nodes[i] = n
        if parent in self.nodes:
            self.nodes[parent].setdefault("children", []).append(i)
        return i

    def frame(self, parent, x, y, w, h, name, fills=None, radius=None,
              stroke_hex=None, stroke_w=1, clip=True):
        extra = {"children": [], "clip": clip}
        if fills is not None:
            extra["fills"] = fills
        if radius is not None:
            extra["corners"] = {"radii": [radius] * 4, "smoothing": 0.0}
        if stroke_hex is not None:
            extra["strokes"] = [solid(stroke_hex)]
            extra["stroke"] = {"weight": float(stroke_w), "align": "inside",
                               "sides": None, "cap_start": "none",
                               "cap_end": "none", "join": "miter",
                               "miter_limit": 4.0, "dashes": []}
        return self._node(parent, x, y, w, h, name, "frame", extra)

    def rect(self, parent, x, y, w, h, name, fill_hex=None, fills=None,
             radius=None, stroke_hex=None, stroke_w=1, bound=None):
        extra = {}
        if fills is not None:
            extra["fills"] = fills
        elif fill_hex is not None:
            extra["fills"] = [solid(fill_hex)]
        if radius is not None:
            extra["corners"] = {"radii": [radius] * 4, "smoothing": 0.0}
        if stroke_hex is not None:
            extra["strokes"] = [solid(stroke_hex)]
            extra["stroke"] = {"weight": float(stroke_w), "align": "inside",
                               "sides": None, "cap_start": "none",
                               "cap_end": "none", "join": "miter",
                               "miter_limit": 4.0, "dashes": []}
        if bound is not None:
            extra["bound"] = bound
        return self._node(parent, x, y, w, h, name, "rectangle", extra)

    def ellipse(self, parent, x, y, w, h, name, fill_hex=None, fills=None,
                stroke_hex=None, stroke_w=1):
        extra = {"start": 0.0, "sweep": math.tau, "inner": 0.0}
        if fills is not None:
            extra["fills"] = fills
        elif fill_hex is not None:
            extra["fills"] = [solid(fill_hex)]
        if stroke_hex is not None:
            extra["strokes"] = [solid(stroke_hex)]
            extra["stroke"] = {"weight": float(stroke_w), "align": "inside",
                               "sides": None, "cap_start": "none",
                               "cap_end": "none", "join": "miter",
                               "miter_limit": 4.0, "dashes": []}
        return self._node(parent, x, y, w, h, name, "ellipse", extra)

    def text(self, parent, x, y, w, h, name, chars, size=13.0, fill_hex=None,
             family=UI, style="Regular", bound=None):
        st = {"font_family": family, "font_style": style,
              "font_size": float(size),
              "line_height": {"unit": "percent", "value": 140.0},
              "letter_spacing": {"unit": "percent", "value": 0.0},
              "decoration": "none", "case": "original",
              "fills": None, "link": None}
        extra = {"characters": chars, "style": st,
                 "fills": [solid(fill_hex if fill_hex is not None
                                 else T["Ink"])]}
        if bound is not None:
            extra["bound"] = bound
        return self._node(parent, x, y, w, h, name, "text", extra)

    def section(self, x, y, w, h, name):
        i = self._id()
        n = {"id": i, "name": name, "type": "section",
             "contents_hidden": False, "parent": 1,
             "children": [],
             "transform": [1.0, 0.0, 0.0, 1.0, float(x), float(y)],
             "width": float(w), "height": float(h),
             "fills": [solid(0xFFFFFF, 0.0)]}
        self.nodes[i] = n
        self.nodes[1]["children"].append(i)
        return i

    def variable_collection(self, name, modes, var_defs):
        """var_defs: [(var_name, resolved_type, {mode: value}), ...]"""
        cid = f"VariableCollectionId:{len(self.variables['collections']) + 1}"
        mode_objs = [{"id": f"{cid}/mode{i+1}", "name": m}
                     for i, m in enumerate(modes)]
        self.variables["collections"].append(
            {"id": cid, "name": name, "modes": mode_objs})
        base = len(self.variables["variables"])
        for k, (vname, rtype, values) in enumerate(var_defs):
            vid = f"VariableID:{base + k + 1}"
            vals = {}
            for i, m in enumerate(modes):
                v = values[i] if isinstance(values, (list, tuple)) \
                    else values.get(m)
                if rtype == "color":
                    vals[f"{cid}/mode{i+1}"] = {"type": "color",
                                                "value": c(v)}
                else:
                    vals[f"{cid}/mode{i+1}"] = {"type": rtype, "value": v}
            self.variables["variables"].append(
                {"id": vid, "name": vname, "collection": cid,
                 "resolvedType": rtype, "values": vals, "description": ""})
            if rtype == "color":
                # remember dark (mode 0) hex for binding
                v0 = values[0] if isinstance(values, (list, tuple)) \
                    else values.get(modes[0])
                self.var_ids[v0] = vid

    def dump(self):
        return {"format": "figcraft", "version": 1, "imageIndex": [],
                "name": self.name, "pages": [1],
                "nodes": self.nodes, "next_id": self.next_id,
                "styles": [], "variables": self.variables,
                "current_page": 1, "document_colors": [], "comments": []}


def save_figcraft(doc, path):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("document.json", json.dumps(doc.dump(), indent=1))


# ------------------------------------------------------------ seat bits

RAIL_H = 22
TITLE_H = 28


def paint_rail(d, parent, x, y, w, cells, active=1, badge=-1, pills=None):
    """The gotabwm top tab rail: cells split the width (min 48), close-x
    on the right of each, spaces pills right-aligned. cells: [labels]."""
    d.rect(parent, x, y, w, RAIL_H, "rail band", fill_hex=T["ChromeBg"])
    d.rect(parent, x, y + RAIL_H - 1, w, 1, "rail rule", fill_hex=T["Rule"])
    n = max(1, len(cells))
    pill_w = 0
    if pills:
        pill_w = sum(d_textw(p) + 8 + 4 for p in pills) + 8
    cell_w = max(48, (w - pill_w) // n)
    for i, label in enumerate(cells):
        cx = x + i * cell_w
        focused = (i == active)
        face = T["Surface"] if focused else T["ChromeBg"]
        d.rect(parent, cx, y, cell_w - 1, RAIL_H - 1,
               f"tab/{label}", fill_hex=face)
        if focused:
            d.rect(parent, cx, y, 3, RAIL_H - 1, "focus edge",
                   fill_hex=T["Accent"])
        d.text(parent, cx + 8, y + 5, cell_w - 24, 12, f"tab label {label}",
               label, size=11.0,
               fill_hex=T["Ink"] if focused else T["InkMuted"])
        d.text(parent, cx + cell_w - 14, y + 5, 10, 12, "close x", "x",
               size=11.0, fill_hex=T["InkMuted"])
        if i == badge:
            d.rect(parent, cx + cell_w - 5, y + 4, 4, 14, "frozen badge",
                   fill_hex=T["Warning"])
    if pills:
        px = x + w - 8
        for p in reversed(pills):
            pw = d_textw(p) + 8
            px -= pw
            d.rect(parent, px, y + 3, pw, RAIL_H - 6, f"space/{p}",
                   fill_hex=T["Surface"], radius=8)
            d.text(parent, px + 4, y + 6, pw, 10, f"space label {p}", p,
                   size=11.0, fill_hex=T["InkMuted"])
            px -= 4


def d_textw(s, size=11.0):
    return int(len(s) * size * 0.55) + 2


def paint_bottom_chrome(d, parent, x, y, w, h, toast=None):
    """Bottom band: toasts bottom-left, Apps god button, PWR, focus badge,
    clock panel bottom-right. y = bottom band top."""
    by = y + h - 8 - 20
    # toast
    if toast:
        d.frame(parent, x + 8, by - 4, 208, 28, "toast", fills=[solid(T["Surface"])],
                radius=8, stroke_hex=T["Border"])
        d.text(parent, x + 8 + 10, by + 4, 188, 14, "toast text", toast,
               size=11.0, fill_hex=T["Ink"])
        d.rect(parent, x + 8, by - 4, 2, 28, "toast edge", fill_hex=T["Accent"])
    # clock panel (148x20)
    cxx = x + w - 8 - 148
    d.frame(parent, cxx, by, 148, 20, "clock panel", fills=[solid(T["ChromeBg"])],
            radius=8, stroke_hex=T["Rule"])
    d.rect(parent, cxx, by, 2, 20, "accent rule", fill_hex=T["Accent"])
    d.text(parent, cxx + 6, by + 4, 70, 12, "clock", "21:47:03", size=11.0,
           family=MONO, fill_hex=T["Ink"])
    d.text(parent, cxx + 78, by + 6, 60, 10, "seat label", "GOTABWM",
           size=8.0, fill_hex=T["Muted"])
    # focus badge (216x20) flush left of clock
    fx = cxx - 4 - 216
    d.frame(parent, fx, by, 216, 20, "focus badge", fills=[solid(T["Surface"])],
            radius=8, stroke_hex=T["Rule"])
    d.rect(parent, fx, by, 2, 20, "accent rule", fill_hex=T["Accent"])
    d.text(parent, fx + 8, by + 4, 150, 12, "focus title", "Term",
           size=11.0, fill_hex=T["Ink"])
    d.rect(parent, fx + 216 - 6 - 46, by + 3, 46, 14, "scope chip",
           fill_hex=T["ChromeBg"], radius=7)
    d.text(parent, fx + 216 - 6 - 42, by + 6, 40, 9, "scope text", "app",
           size=8.0, fill_hex=T["InkMuted"])
    # Apps god button (96x20)
    gx = x + 8 + 208 + 8
    d.frame(parent, gx, by, 96, 20, "apps button", fills=[solid(T["ChromeBg"])],
            radius=4, stroke_hex=T["Rule"])
    d.rect(parent, gx, by, 2, 20, "accent rule", fill_hex=T["Accent"])
    d.ellipse(parent, gx + 4, by + 2, 16, 16, "emblem", fill_hex=T["Warning"])
    d.text(parent, gx + 24, by + 4, 60, 12, "apps label", "Apps",
           size=11.0, fill_hex=T["Ink"])
    # PWR button right of Apps
    px = gx + 96 + 8
    d.frame(parent, px, by, 56, 20, "power button", fills=[solid(T["ChromeBg"])],
            radius=4, stroke_hex=T["Rule"])
    d.rect(parent, px, by, 2, 20, "accent rule", fill_hex=T["Accent"])
    d.text(parent, px + 8, by + 4, 40, 12, "pwr label", "PWR",
           size=11.0, fill_hex=T["InkMuted"])


def titlebar(d, parent, x, y, w, title):
    """28px floating-window titlebar per ui-primitives 2.2/2.4."""
    d.rect(parent, x, y, w, TITLE_H, "titlebar", fill_hex=T["Surface"])
    d.rect(parent, x, y + TITLE_H - 1, w, 1, "title rule", fill_hex=T["Border"])
    d.text(parent, x + 8, y + 7, w - 90, 14, "window title", title,
           size=13.0, fill_hex=T["Text"])
    for i, glyph in enumerate(["_", "[]", "x"]):
        bx = x + w - 8 - (3 - i) * 20
        d.frame(parent, bx, y + 6, 16, 16, f"ctl {glyph}",
                fills=[solid(T["BtnIdle"])], radius=4)
        d.text(parent, bx + 4, y + 8, 12, 12, f"ctl glyph {glyph}", glyph,
               size=9.0, family=MONO,
               fill_hex=T["Danger"] if glyph == "x" else T["InkMuted"])


def window_frame(d, parent, x, y, w, content_h, title):
    """Windowed template frame: 28px spec titlebar + content region.
    Returns (frame_id, content_y)."""
    h = content_h + TITLE_H
    f = d.frame(parent, x, y, w, h, f"window/{title}",
                fills=[solid(T["Bg"])], radius=8, stroke_hex=T["Border"])
    titlebar(d, f, 0, 0, w, title)
    return f, TITLE_H


def wallpaper(d, parent, x, y, w, h):
    d.rect(parent, x, y, w, h, "wallpaper",
           fills=[vgrad(T["WallpaperTop"], T["WallpaperBot"])])


def btn(d, parent, x, y, w, h, label, face=None, fg=None, accent=False,
        focus=False, muted=False):
    face = T["BtnIdle"] if face is None else face
    fg = T["Ink"] if fg is None else fg
    if muted:
        fg = T["Muted"]
    if accent:
        d.frame(parent, x, y, w, h, f"btn/{label}", fills=[solid(face)],
                radius=4, stroke_hex=T["Accent"])
    elif focus:
        d.frame(parent, x, y, w, h, f"btn/{label}", fills=[solid(face)],
                radius=4, stroke_hex=T["Accent"], stroke_w=2)
    else:
        d.frame(parent, x, y, w, h, f"btn/{label}", fills=[solid(face)],
                radius=4, stroke_hex=T["Border"])
    d.text(parent, x, y + h // 2 - 6, w, 12, f"btn label {label}", label,
           size=11.0, fill_hex=T["OnAccent"] if accent else fg)


def listrows(d, parent, x, y, w, rows, selected=1, row_h=18, sel_marker=True):
    for i, r in enumerate(rows):
        ry = y + i * row_h
        if i == selected:
            d.rect(parent, x, ry, w, row_h, f"row sel/{r}",
                   fill_hex=T["Selection"])
            if sel_marker:
                d.rect(parent, x, ry, 3, row_h, "sel edge",
                       fill_hex=T["Accent"])
            fg = T["Ink"]
        else:
            fg = T["Ink"] if i % 2 == 0 else T["InkMuted"]
        d.text(parent, x + 8, ry + 3, w - 16, row_h - 4, f"row/{r}", r,
               size=11.0, fill_hex=fg)


def textgrid(d, parent, x, y, lines, size=13.0, line_h=16, fg=None, dim_from=-1):
    fg = T["Ink"] if fg is None else fg
    for i, ln in enumerate(lines):
        f = T["InkMuted"] if dim_from >= 0 and i >= dim_from else fg
        d.text(parent, x, y + i * line_h, 8 + 8 * len(ln), line_h - 2,
               f"line {i}", ln, size=size, family=MONO, fill_hex=f)


# ============================================================== TOKENS DOC


def build_tokens(path):
    d = Doc("VirelaiOS design tokens", "Tokens", 0x101418)
    # variables: one collection "Virelai Theme", modes dark/light/dark-hc/light-hc
    var_defs = []
    for tok in TOKEN_ORDER:
        var_defs.append((f"color/{tok.lower()}", "color",
                         [DARK[tok], LIGHT[tok], DARKHC[tok], LIGHTHC[tok]]))
    for name, vals in [("space/xs", 2), ("space/sm", 4), ("space/md", 8),
                       ("space/lg", 16), ("radius/control", 4),
                       ("radius/window", 8), ("stroke/border", 1),
                       ("stroke/focus", 2)]:
        var_defs.append((name, "number", [vals] * 4))
    d.variable_collection("Virelai Theme",
                          ["Dark", "Light", "Dark HC", "Light HC"], var_defs)
    bind = lambda hexv: {"fill": d.var_ids.get(hexv)} if d.var_ids.get(hexv) else None

    # ---- colors section -------------------------------------------------
    sec = d.frame(1, 0, 0, 1180, 760, "tokens/colors", fills=[solid(0x101418)])
    d.text(sec, 24, 16, 600, 22, "h1", "Color roles — theme.Tokens",
           size=17.0, style="Semi Bold", fill_hex=T["Ink"])
    d.text(sec, 24, 40, 900, 14, "h1sub",
           "Swatches bound to the Virelai Theme collection; switch the page "
           "mode to preview Light / Dark HC / Light HC.", size=11.0,
           fill_hex=T["Muted"])
    colw = 150
    for i, tok in enumerate(TOKEN_ORDER):
        col = i // 12
        row = i % 12
        sx = 24 + col * (colw * 2 + 40)
        sy = 68 + row * 56
        def lum(hexv):
            return (0.299 * ((hexv >> 16) & 0xFF) +
                    0.587 * ((hexv >> 8) & 0xFF) +
                    0.114 * (hexv & 0xFF)) / 255.0
        dark_sw = lum(DARK[tok]) < 0.5
        name_fg = T["Text"] if dark_sw else T["Bg"]
        hex_fg = T["Muted"] if dark_sw else T["Surface"]
        d.rect(sec, sx, sy, colw, 44, f"swatch/{tok}",
               fills=[solid(DARK[tok])], radius=4,
               stroke_hex=T["Border"], bound=bind(DARK[tok]))
        d.text(sec, sx + 6, sy + 6, colw - 12, 12, f"tokname/{tok}", tok,
               size=11.0, style="Medium", fill_hex=name_fg)
        d.text(sec, sx + 6, sy + 22, colw - 12, 12, f"tokhex/{tok}",
               f"#{DARK[tok]:06x}", size=9.0, family=MONO, fill_hex=hex_fg)
        # light + HC chips
        for j, tbl in enumerate((LIGHT, DARKHC, LIGHTHC)):
            d.rect(sec, sx + colw + 8 + j * 16, sy, 14, 44,
                   f"swatch/{tok}/{'light' if j == 0 else ('darkhc' if j == 1 else 'lighthc')}",
                   fills=[solid(tbl[tok])], stroke_hex=T["Border"])
    lx = 24 + 2 * (colw * 2 + 40)
    for j, nm in enumerate(("Light", "Dark HC", "Light HC")):
        d.text(sec, lx - colw - 8 + 8 + j * 16 + 6, 40, 40, 10,
               f"mode label {nm}", nm[:2].upper() if j else "LT",
               size=8.0, fill_hex=T["Muted"])

    # ---- type section ---------------------------------------------------
    sec = d.frame(1, 0, 800, 1180, 360, "tokens/type", fills=[solid(0x101418)])
    d.text(sec, 24, 16, 600, 22, "h2", "Type — Inter UI, Fira Code mono",
           size=17.0, style="Semi Bold", fill_hex=T["Ink"])
    samples = [
        ("ui/11 — seat labels, rail tabs, list rows", 11, UI, "Regular",
         "The quick brown fox jumps over the lazy dog 0123456789"),
        ("ui/13 — chrome labels, window titles, body", 13, UI, "Regular",
         "The quick brown fox jumps over the lazy dog 0123456789"),
        ("ui/15 — dialog headlines, tour steps", 15, UI, "Medium",
         "The quick brown fox jumps over the lazy dog"),
        ("ui/17 — section heads, empty states", 17, UI, "Semi Bold",
         "The quick brown fox jumps over the lazy dog"),
    ]
    y = 52
    for name, size, fam, sty, s in samples:
        d.text(sec, 24, y, 260, 12, f"type label {size}", name, size=9.0,
               fill_hex=T["Muted"])
        d.text(sec, 300, y - 4, 800, int(size * 1.5), f"type sample {size}",
               s, size=float(size), family=fam, style=sty, fill_hex=T["Ink"])
        y += int(size * 1.5) + 18
    d.text(sec, 24, y + 8, 260, 12, "type label mono",
           "mono/13 — Fira Code, terminal + editor", size=9.0,
           fill_hex=T["Muted"])
    d.text(sec, 300, y + 4, 800, 18, "type sample mono",
           "gosh$ exec GOTERM.ELF  # cell grid, selection, caret",
           size=13.0, family=MONO, fill_hex=T["Ok"])

    # ---- geometry section ------------------------------------------------
    sec = d.frame(1, 0, 1200, 1180, 300, "tokens/geometry", fills=[solid(0x101418)])
    d.text(sec, 24, 16, 600, 22, "h3", "Geometry — spacing, radii, strokes, depth",
           size=17.0, style="Semi Bold", fill_hex=T["Ink"])
    x = 24
    for nm, v in [("PadXS 2", 2), ("PadSM 4", 4), ("PadMD 8", 8), ("PadLG 16", 16)]:
        d.rect(sec, x, 60, v + 16, 32, f"space/{nm}", fill_hex=T["Surface"],
               stroke_hex=T["Border"])
        d.text(sec, x, 96, 80, 12, f"space label {nm}", nm, size=9.0,
               fill_hex=T["Muted"])
        x += 90
    x += 20
    for nm, r in [("radiusControl 4", 4), ("radiusWindow 8", 8), ("radiusPill h/2", 16)]:
        d.rect(sec, x, 56, 96, 40, f"radius/{nm}", fill_hex=T["BtnIdle"],
               radius=r, stroke_hex=T["Border"])
        d.text(sec, x, 100, 110, 12, f"radius label {nm}", nm, size=9.0,
               fill_hex=T["Muted"])
        x += 116
    x += 20
    for nm, wgt in [("BorderW 1", 1), ("FocusW 2 (inside)", 2)]:
        d.rect(sec, x, 56, 96, 40, f"stroke/{nm}", fill_hex=T["Surface"],
               stroke_hex=T["Accent"] if wgt == 2 else T["Border"],
               stroke_w=wgt)
        d.text(sec, x, 100, 110, 12, f"stroke label {nm}", nm, size=9.0,
               fill_hex=T["Muted"])
        x += 116
    x += 20
    # shadow spec: dy=4 blur=16 ink Shadow @0x40
    d.ellipse(sec, x, 60, 10, 10, "shadow dot", fill_hex=T["Shadow"])
    d.text(sec, x + 16, 58, 220, 40, "shadow spec",
           "shadow: dy=4, blur=16, ink Shadow\npeak alpha 0x40 (25%) — floating\nplates only, never content",
           size=9.0, fill_hex=T["Muted"])

    # ---- components section ----------------------------------------------
    sec = d.frame(1, 1240, 0, 900, 700, "tokens/components", fills=[solid(0x101418)])
    d.text(sec, 24, 16, 700, 22, "h4",
           "Primitives — 2.3 states: default hover pressed disabled "
           "focused selected", size=15.0, style="Semi Bold", fill_hex=T["Ink"])
    y = 56
    # buttons
    d.text(sec, 24, y, 140, 12, "lbl btn", "Button", size=11.0,
           style="Medium", fill_hex=T["InkMuted"])
    btn(d, sec, 160, y - 4, 88, 24, "Default", face=T["BtnIdle"])
    btn(d, sec, 256, y - 4, 88, 24, "Hover", face=T["BtnHover"])
    btn(d, sec, 352, y - 4, 88, 24, "Pressed", face=T["BtnPressed"])
    btn(d, sec, 448, y - 4, 88, 24, "Disabled", muted=True)
    btn(d, sec, 544, y - 4, 88, 24, "Focused", focus=True)
    btn(d, sec, 640, y - 4, 96, 24, "Default", accent=True)
    y += 44
    # text field
    d.text(sec, 24, y, 140, 12, "lbl field", "Text field", size=11.0,
           style="Medium", fill_hex=T["InkMuted"])
    d.frame(sec, 160, y - 4, 220, 24, "field", fills=[solid(T["Bg"])],
            radius=4, stroke_hex=T["Accent"], stroke_w=2)
    d.text(sec, 168, y + 2, 140, 12, "field text", "passphrase",
           size=11.0, fill_hex=T["Ink"])
    d.rect(sec, 168 + 8 * len("passphrase") + 2, y + 2, 1, 12, "caret",
           fill_hex=T["Caret"])
    d.frame(sec, 396, y - 4, 220, 24, "field disabled", fills=[solid(T["Bg"])],
            radius=4, stroke_hex=T["Border"])
    d.text(sec, 404, y + 2, 140, 12, "field ph", "placeholder",
           size=11.0, fill_hex=T["Muted"])
    y += 44
    # toggle
    d.text(sec, 24, y, 140, 12, "lbl tog", "Toggle", size=11.0,
           style="Medium", fill_hex=T["InkMuted"])
    d.frame(sec, 160, y - 4, 40, 20, "toggle on", fills=[solid(T["Accent"])],
            radius=10)
    d.ellipse(sec, 182, y - 2, 16, 16, "knob on", fill_hex=T["OnAccent"])
    d.frame(sec, 216, y - 4, 40, 20, "toggle off", fills=[solid(T["BtnIdle"])],
            radius=10, stroke_hex=T["Border"])
    d.ellipse(sec, 218, y - 2, 16, 16, "knob off", fill_hex=T["Muted"])
    y += 40
    # menu rows
    d.text(sec, 24, y, 140, 12, "lbl menu", "Menu row (24h)", size=11.0,
           style="Medium", fill_hex=T["InkMuted"])
    mrows = [("New Tab        Ctrl+T", False, False),
             ("Find           Ctrl+F", True, False),
             ("Paste As…            ", False, True)]
    for i, (lbl, hov, dis) in enumerate(mrows):
        ry = y + i * 24
        if hov:
            d.rect(sec, 160, ry, 220, 24, f"menurow hover", fill_hex=T["Selection"])
        d.text(sec, 168, ry + 6, 200, 12, f"menurow/{i}", lbl,
               size=11.0, family=MONO,
               fill_hex=T["Muted"] if dis else T["Ink"])
    y += 3 * 24 + 20
    # rail tab states
    d.text(sec, 24, y, 140, 12, "lbl tab", "Rail tab", size=11.0,
           style="Medium", fill_hex=T["InkMuted"])
    for i, (lbl, foc) in enumerate([("Files", False), ("Term", True), ("Edit", False)]):
        tx = 160 + i * 96
        d.rect(sec, tx, y, 92, 22, f"railtab/{lbl}",
               fill_hex=T["Surface"] if foc else T["ChromeBg"])
        if foc:
            d.rect(sec, tx, y, 3, 22, "tab focus edge", fill_hex=T["Accent"])
        d.text(sec, tx + 8, y + 5, 60, 12, f"railtab label {lbl}", lbl,
               size=11.0, fill_hex=T["Ink"] if foc else T["InkMuted"])
        d.text(sec, tx + 78, y + 5, 10, 12, "railtab x", "x", size=11.0,
               fill_hex=T["InkMuted"])
    y += 40
    # badge + toast
    d.text(sec, 24, y, 140, 12, "lbl badge", "Badge / toast", size=11.0,
           style="Medium", fill_hex=T["InkMuted"])
    d.rect(sec, 160, y - 2, 4, 14, "frozen badge", fill_hex=T["Warning"])
    d.ellipse(sec, 172, y, 8, 8, "dot", fill_hex=T["Danger"])
    d.frame(sec, 200, y - 6, 208, 26, "toast card", fills=[solid(T["Surface"])],
            radius=8, stroke_hex=T["Border"])
    d.rect(sec, 200, y - 6, 2, 26, "toast edge", fill_hex=T["Accent"])
    d.text(sec, 210, y + 1, 190, 12, "toast txt", "build finished (3.2s)",
           size=11.0, fill_hex=T["Ink"])
    y += 40
    # list row selected (3px accent marker)
    d.text(sec, 24, y, 140, 12, "lbl row", "List row (24h)", size=11.0,
           style="Medium", fill_hex=T["InkMuted"])
    d.rect(sec, 160, y, 220, 24, "row sel", fill_hex=T["Selection"])
    d.rect(sec, 160, y, 3, 24, "row sel edge", fill_hex=T["Accent"])
    d.text(sec, 168, y + 6, 200, 12, "row txt", "selected row",
           size=11.0, fill_hex=T["Ink"])
    d.text(sec, 168, y + 24 + 6, 200, 12, "row txt2", "normal row",
           size=11.0, fill_hex=T["InkMuted"])

    # ---- settings variables section ---------------------------------------
    sec = d.frame(1, 1240, 740, 900, 260, "tokens/settings-keys", fills=[solid(0x101418)])
    d.text(sec, 24, 16, 700, 22, "h5", "Settings keys (SETTINGS.TXT)",
           size=15.0, style="Semi Bold", fill_hex=T["Ink"])
    rows = [
        "theme=dark|light            base palette (boot default: dark)",
        "a11y.contrast=off|high      high-contrast variant (7:1 floor)",
        "a11y.text_scale=<n>         UI text scale",
        "a11y.reduce_motion=off|on   reduce motion",
        "prompt=<fmt>               gosh prompt",
        "term_restart=…             term close behaviour",
    ]
    for i, r in enumerate(rows):
        d.text(sec, 24, 52 + i * 18, 700, 14, f"setrow/{i}", r,
               size=11.0, family=MONO, fill_hex=T["InkMuted"])
    d.text(sec, 24, 52 + len(rows) * 18 + 10, 800, 14, "varnote",
           "Colors/numbers above are figcraft variables (Virelai Theme, 4 "
           "modes); bind fills to iterate themes.", size=9.0,
           fill_hex=T["Muted"])
    save_figcraft(d, path)


# =========================================================== SEAT-SHELL

DESK_W, DESK_H = 1280, 720


def build_shell(path):
    d = Doc("VirelaiOS seat shell", "Shell", 0x101418)

    # ---- desktop at rest ---------------------------------------------------
    sec = d.frame(1, 0, 0, DESK_W + 80, DESK_H + 80, "shell/desktop-rest", fills=[solid(0x101418)])
    f = d.frame(sec, 40, 40, DESK_W, DESK_H, "desktop 1280x720",
                fills=None, clip=True)
    wallpaper(d, f, 0, 0, DESK_W, DESK_H)
    paint_rail(d, f, 0, 0, DESK_W, ["Files", "Term", "Edit", "Web"],
               active=1, badge=3, pills=["1", "2", "3"])
    # active tab content: a terminal text grid (full-viewport tab)
    textgrid(d, f, 16, 40,
             ["gosh$ exec GOCALC.ELF", "gocalc: open id=4",
              "gocalc: declare accepted", "gosh$ ls /host",
              "APPS.TXT  CALC/  DOCUMENTS/  GOMAIL.TXT  SNAPSHOTS/",
              "gosh$ "],
             line_h=18)
    paint_bottom_chrome(d, f, 0, 0, DESK_W, DESK_H,
                        toast="gocalc: result 42")
    d.text(sec, 40, DESK_H + 52, 900, 14, "cap desktop",
           "Desktop at rest — top rail (22px) of live tabs + space pills, "
           "wallpaper gradient, bottom chrome: toasts, Apps, PWR, focus "
           "badge, clock panel. Windows are full-viewport tabs.",
           size=11.0, fill_hex=T["Muted"])

    # ---- chrome anatomy ----------------------------------------------------
    sec = d.frame(1, 0, DESK_H + 140, DESK_W + 80, 560, "shell/chrome-anatomy", fills=[solid(0x101418)])
    d.text(sec, 40, 8, 900, 22, "anat h", "Window chrome anatomy",
           size=17.0, style="Semi Bold", fill_hex=T["Ink"])
    d.text(sec, 40, 34, 1100, 14, "anat sub",
           "Under gotabwm a window is a full-viewport tab — the rail cell "
           "IS its identity; the 28px bar below is the floating-window spec "
           "(ui-primitives 2.2/2.4): dialogs, popovers, the wnd path.",
           size=11.0, fill_hex=T["Muted"])
    # focused window
    f, cy = window_frame(d, sec, 40, 70, 460, 220, "GOEDIT — focused")
    d.frame(f, -2, -2, 464, 252, "focus ring", fills=[solid(0, 0)],
            radius=10, stroke_hex=T["Accent"], stroke_w=2, clip=False)
    textgrid(d, f, 12, cy + 12,
             [" 1  // focused window", " 2  package main",
              " 3  func main() {", " 4  }"], line_h=17)
    for lbl, lx in [("title, left at PadMD", 96),
                    ("16x16 controls: min max close", 366)]:
        d.text(f, lx, 8, 200, 12, f"ann {lbl}", lbl, size=8.0,
               fill_hex=T["Muted"])
    # unfocused
    f, cy = window_frame(d, sec, 560, 70, 460, 220, "GOEDIT — unfocused")
    textgrid(d, f, 12, cy + 12,
             [" 1  // ring off, ink muted", " 2  package main"], line_h=17)
    # snap guide hint
    d.text(sec, 40, 320, 1100, 14, "anat note",
           "Focus = the 2px Accent ring inside bounds (ADR 0008 D4) + the "
           "rail cell's 3px accent edge. Split: sash drags against tile "
           "zones (SplitVert/SplitHoriz) with the sash gutter centered "
           "below the rail.", size=11.0, fill_hex=T["Muted"])
    # floating plates: dialog + menu on one canvas
    d.frame(sec, 40, 360, 360, 140, "dialog plate",
            fills=[solid(T["Surface"])], radius=8, stroke_hex=T["Border"])
    d.text(sec, 60, 376, 300, 14, "dlg title", "Unsaved changes",
           size=13.0, style="Medium", fill_hex=T["Text"])
    d.text(sec, 60, 398, 300, 14, "dlg msg",
           "DOCUMENT.TXT has unsaved changes.", size=11.0, fill_hex=T["Muted"])
    btn(d, sec, 60, 460, 80, 24, "Discard")
    btn(d, sec, 148, 460, 80, 24, "Cancel")
    btn(d, sec, 236, 460, 80, 24, "Save", accent=True)
    d.frame(sec, 460, 360, 220, 140, "menu plate",
            fills=[solid(T["Surface"])], radius=8, stroke_hex=T["Border"])
    for i, it in enumerate(["New Window", "Open…        Ctrl+O",
                            "Save         Ctrl+S", "Close        Ctrl+W"]):
        ry = 360 + 8 + i * 30
        if i == 1:
            d.rect(sec, 468, ry - 2, 204, 24, "menurow hover",
                   fill_hex=T["Selection"])
        d.text(sec, 476, ry + 4, 190, 12, f"menuitem {it}", it,
               size=11.0, family=MONO,
               fill_hex=T["Muted"] if i == 3 else T["Ink"])
    d.text(sec, 460, 510, 400, 14, "dlg cap",
           "Floating plates: radiusWindow + BorderW + the shared shadow "
           "(dy 4, blur 16, 25% ink).", size=9.0, fill_hex=T["Muted"])

    # ---- menubar + open menu ------------------------------------------------
    sec = d.frame(1, 0, DESK_H + 760, DESK_W + 80, 320, "shell/menubar", fills=[solid(0x101418)])
    d.text(sec, 40, 8, 900, 22, "mb h", "App menubar (appkit)",
           size=17.0, style="Semi Bold", fill_hex=T["Ink"])
    f = d.frame(sec, 40, 48, 672, 200, "menubar demo", fills=[solid(T["Bg"])],
                radius=8, stroke_hex=T["Border"])
    d.rect(f, 0, 0, 672, 24, "menubar", fill_hex=T["Surface"])
    d.rect(f, 0, 23, 672, 1, "menubar rule", fill_hex=T["Rule"])
    for i, t in enumerate(["File", "Edit", "Format", "View"]):
        tx = 8 + i * 64
        if i == 2:
            d.rect(f, tx - 4, 2, 56, 20, "mb hover", fill_hex=T["Selection"],
                   radius=4)
        d.text(f, tx, 6, 56, 12, f"mb title {t}", t, size=11.0,
               fill_hex=T["Ink"])
    # open menu under Format
    d.frame(f, 132, 24, 200, 130, "open menu", fills=[solid(T["Surface"])],
            radius=8, stroke_hex=T["Border"])
    items = [("Number format…     ", False, False),
             ("Fill right         ", False, False),
             ("Fill down          ", False, False),
             ("Column width…      ", True, False),
             ("Undo fill          ", False, True)]
    for i, (lbl, hov, dis) in enumerate(items):
        ry = 32 + i * 24
        if hov:
            d.rect(f, 140, ry - 4, 184, 22, "menurow hov",
                   fill_hex=T["Selection"])
        d.text(f, 148, ry, 176, 12, f"mi {i}", lbl, size=11.0, family=MONO,
               fill_hex=T["Muted"] if dis else T["Ink"])
    textgrid(d, f, 12, 170, ["Edit  Format   ← GOSHEET's real menubar"],
             size=10.0, line_h=14)

    # ---- notifications ------------------------------------------------------
    sec = d.frame(1, 0, DESK_H + 1140, DESK_W + 80, DESK_H + 80, "shell/notify", fills=[solid(0x101418)])
    f = d.frame(sec, 40, 40, DESK_W, DESK_H, "notify canvas",
                fills=None, clip=True)
    wallpaper(d, f, 0, 0, DESK_W, DESK_H)
    paint_rail(d, f, 0, 0, DESK_W, ["Files", "Term", "Edit", "Web"],
               active=1, badge=1, pills=["1", "2"])
    # notification center panel (over right side)
    ncw, nch = 300, 420
    d.frame(f, DESK_W - 8 - ncw, RAIL_H + 8, ncw, nch,
            "notification center", fills=[solid(T["Surface"])], radius=8,
            stroke_hex=T["Border"])
    d.text(f, DESK_W - 8 - ncw + 12, RAIL_H + 20, 200, 14, "nc title",
           "NOTIFICATIONS", size=13.0, style="Medium", fill_hex=T["Text"])
    cards = [("gotabwm", "build finished", "3.2s", T["Ok"]),
             ("goirc", "#virelai: mention", "now", T["Accent"]),
             ("gorec", "capture saved 12.0s", "1m", T["Muted"])]
    for i, (app, msg, age, edge) in enumerate(cards):
        cy = RAIL_H + 48 + i * 64
        d.frame(f, DESK_W - 8 - ncw + 12, cy, ncw - 24, 56,
                f"nc card {app}", fills=[solid(T["ChromeBg"])], radius=8,
                stroke_hex=T["Rule"])
        d.rect(f, DESK_W - 8 - ncw + 12, cy, 3, 56, "nc edge",
               fill_hex=edge)
        d.text(f, DESK_W - 8 - ncw + 24, cy + 8, 200, 12, f"nc app {app}",
               app, size=9.0, fill_hex=T["Muted"])
        d.text(f, DESK_W - 8 - ncw + 24, cy + 24, 230, 12, f"nc msg {i}",
               msg, size=11.0, fill_hex=T["Ink"])
        d.text(f, DESK_W - 8 - ncw + 24, cy + 40, 100, 10, f"nc age {i}",
               age, size=8.0, fill_hex=T["Muted"])
    # toasts bottom-left stack
    for i, msg in enumerate(["gocalc: result 42", "gosnap: save BASE ok",
                             "clip: host paste"]):
        ty = DESK_H - 8 - 20 - 24 - (2 - i) * 32
        d.frame(f, 8, ty, 208, 26, f"toast {i}", fills=[solid(T["Surface"])],
                radius=8, stroke_hex=T["Border"])
        d.rect(f, 8, ty, 2, 26, "toast edge", fill_hex=T["Accent"])
        d.text(f, 18, ty + 7, 190, 12, f"toast txt {i}", msg, size=11.0,
               family=MONO, fill_hex=T["Ink"])
    paint_bottom_chrome(d, f, 0, 0, DESK_W, DESK_H)
    d.text(sec, 40, DESK_H + 52, 900, 14, "cap notify",
           "Toasts bottom-left (208w, 20h + gap), history in the center "
           "panel off the clock; the >5s command-finished rule posts here.",
           size=11.0, fill_hex=T["Muted"])

    # ---- lock curtain -------------------------------------------------------
    sec = d.frame(1, 0, 2 * DESK_H + 1520, DESK_W + 80, DESK_H + 80, "shell/lock", fills=[solid(0x101418)])
    f = d.frame(sec, 40, 40, DESK_W, DESK_H, "lock curtain",
                fills=None, clip=True)
    wallpaper(d, f, 0, 0, DESK_W, DESK_H)
    paint_rail(d, f, 0, 0, DESK_W, ["Files", "Term"], active=1)
    d.rect(f, 0, 0, DESK_W, DESK_H, "curtain", fills=[solid(T["ChromeBg"], 0.92)])
    lw, lh = 288, 96
    lx, ly = (DESK_W - lw) // 2, (DESK_H - lh) // 2
    d.frame(f, lx, ly, lw, lh, "lock plate", fills=[solid(T["Surface"])],
            radius=8, stroke_hex=T["Accent"])
    d.text(f, lx + 12, ly + 10, 120, 14, "lock title", "LOCKED",
           size=13.0, fill_hex=T["Ink"])
    d.rect(f, lx + 12, ly + 32, lw - 24, 20, "pass field",
           fill_hex=T["Bg"], stroke_hex=T["Border"])
    d.text(f, lx + 16, ly + 37, 120, 12, "pass mask", "********",
           size=13.0, family=MONO, fill_hex=T["Ink"])
    d.text(f, lx + 12, ly + lh - 18, 260, 12, "lock hint",
           "vault passphrase unlocks", size=11.0, fill_hex=T["InkMuted"])
    d.text(sec, 40, DESK_H + 52, 900, 14, "cap lock",
           "Ctrl+Shift+L: full-opacity ChromeBg veil over the desk, one "
           "288x96 plate — bullets only, never bytes.",
           size=11.0, fill_hex=T["Muted"])

    # ---- welcome tour -------------------------------------------------------
    sec = d.frame(1, 0, 3 * DESK_H + 1880, DESK_W + 80, DESK_H + 80, "shell/tour", fills=[solid(0x101418)])
    f = d.frame(sec, 40, 40, DESK_W, DESK_H, "tour canvas",
                fills=None, clip=True)
    wallpaper(d, f, 0, 0, DESK_W, DESK_H)
    paint_rail(d, f, 0, 0, DESK_W, ["Welcome"], active=0)
    wf, cy = window_frame(d, f, (DESK_W - 512) // 2, 90, 512, 384,
                          "GOWELCOME — first-boot tour")
    d.text(wf, 16, cy + 12, 400, 18, "tour title", "Welcome to VirelaiOS",
           size=17.0, style="Semi Bold", fill_hex=T["Ink"])
    gestures = [("Ctrl+T", "open the app launcher"),
                ("Alt+Tab", "cycle focused window"),
                ("Ctrl+Shift+L", "lock the seat"),
                ("Ctrl+Shift+G", "find in the focused app"),
                ("middle-click", "paste the primary selection")]
    for i, (chip, desc) in enumerate(gestures):
        gy = cy + 48 + i * 34
        d.frame(wf, 16, gy, 128, 24, f"chip {chip}",
                fills=[solid(T["ChromeBg"])], radius=4,
                stroke_hex=T["Border"])
        d.text(wf, 24, gy + 6, 116, 12, f"chip txt {i}", chip,
               size=11.0, family=MONO, fill_hex=T["Accent"])
        d.text(wf, 156, gy + 6, 330, 12, f"gest {i}", desc,
               size=11.0, fill_hex=T["Ink"])
    for i, lbl in enumerate(["Files", "Terminal", "Help"]):
        btn(d, wf, 16 + i * 110, cy + 384 - 46, 100, 26, lbl)
    d.text(sec, 40, DESK_H + 52, 900, 14, "cap tour",
           "The 5-gesture tour GOWELCOME paints on first boot — key chips "
           "pulled from the seat's own chords registry, one-click launch "
           "buttons below.", size=11.0, fill_hex=T["Muted"])

    save_figcraft(d, path)


# =============================================================== APPS DOC

def app_window(d, parent, x, y, name, title, w, h, body):
    f = d.frame(parent, x, y, w, h + TITLE_H, f"apps/{name}",
                fills=[solid(T["Bg"])], radius=8, stroke_hex=T["Border"])
    titlebar(d, f, 0, 0, w, title)
    body(d, f, TITLE_H, w, h)
    return f


def b_console(d, f, ty, w, h, lines):
    textgrid(d, f, 10, ty + 10, lines, line_h=17)


def b_calc(d, f, ty, w, h):
    d.text(f, 8, ty + 8, w - 16, 20, "hist", "12*3.5", size=11.0,
           fill_hex=T["InkMuted"])
    d.frame(f, 8, ty + 32, w - 16, 44, "display", fills=[solid(T["Surface"])])
    d.text(f, w - 160, ty + 42, 140, 24, "disp", "42", size=17.0,
           family=MONO, fill_hex=T["Ink"])
    pad = [["C", "±", "%", "/"], ["7", "8", "9", "*"], ["4", "5", "6", "-"],
           ["1", "2", "3", "+"], ["P", "0", ".", "="]]
    y0, gap = ty + 84, 8
    bw = (w - 16 - 3 * gap) // 4
    bh = (h - 84 - 8 - 4 * gap) // 5
    for r, row in enumerate(pad):
        for cix, lbl in enumerate(row):
            face = T["Surface"] if lbl in ("=",) else T["BtnIdle"]
            btn(d, f, 8 + cix * (bw + gap), y0 + r * (bh + gap), bw, bh, lbl,
                face=face)


def b_note(d, f, ty, w, h):
    textgrid(d, f, 10, ty + 10,
             ["Meeting notes — 2026-10-24", "",
              "- seat rail hover needs a tooltip", "- quicklook .vcf card",
              "- calc tape export to NOTE", "", "~"], line_h=18)
    d.frame(f, 0, ty + h - 24, w, 24, "find bar", fills=[solid(T["Surface"])])
    d.text(f, 10, ty + h - 18, 90, 12, "find lbl", "find:", size=11.0,
           family=MONO, fill_hex=T["Muted"])
    d.text(f, 60, ty + h - 18, 200, 12, "find q", "quicklook",
           size=11.0, family=MONO, fill_hex=T["Ink"])
    d.text(f, w - 90, ty + h - 18, 80, 12, "find n", "2/3", size=11.0,
           family=MONO, fill_hex=T["Muted"])


def b_edit(d, f, ty, w, h):
    d.rect(f, 0, ty, w, 24, "menubar", fill_hex=T["Surface"])
    for i, t in enumerate(["File", "Edit", "View", "Go"]):
        d.text(f, 8 + i * 56, ty + 6, 52, 12, f"mb {t}", t, size=11.0,
               fill_hex=T["Ink"])
    gutter_w = 44
    d.rect(f, 0, ty + 24, gutter_w, h - 24 - 20, "gutter",
           fill_hex=T["Gutter"])
    code = ["package main", "", "import \"virelai/vi\"", "",
            "func main() {", "\tvi.ConsoleLine(\"hi\")", "}"]
    for i, ln in enumerate(code):
        ly = ty + 32 + i * 17
        d.text(f, 6, ly, 34, 12, f"ln{i}", str(i + 1), size=10.0,
               family=MONO, fill_hex=T["InkMuted"])
        d.text(f, gutter_w + 8, ly, w - gutter_w - 20, 12, f"code{i}", ln,
               size=11.0, family=MONO,
               fill_hex=T["Ink"] if i != 5 else T["Accent"])
    d.rect(f, gutter_w - 4, ty + 24, 4, h - 24 - 20, "heat gutter",
           fill_hex=T["Warning"])
    d.rect(f, 0, ty + h - 20, w, 20, "status", fill_hex=T["ChromeBg"])
    d.text(f, 8, ty + h - 16, 300, 12, "status txt",
           "main.go  Ln 6, Col 2  utf-8  go", size=10.0, family=MONO,
           fill_hex=T["InkMuted"])


def b_files(d, f, ty, w, h):
    # TUI: two panes + status line (text grid look, mono)
    pane_w = w * 3 // 5
    d.rect(f, 0, ty, pane_w, h - 20, "list pane", fill_hex=T["ChromeBg"])
    d.text(f, 8, ty + 6, pane_w - 16, 12, "path", "/host/DOCUMENTS",
           size=11.0, family=MONO, fill_hex=T["Accent"])
    rows = ["..", "CONTRACT.TXT", "INVOICE.PDF", "MAP.QOI",
            "NOTES/", "PACKING.TXT", "VCARD.VCF"]
    for i, r in enumerate(rows):
        ry = ty + 26 + i * 16
        if i == 6:
            d.rect(f, 0, ry - 2, pane_w, 16, "sel", fill_hex=T["Selection"])
        d.text(f, 10, ry, pane_w - 20, 12, f"frow {r}", r, size=11.0,
               family=MONO, fill_hex=T["Ink"])
    d.rect(f, pane_w, ty, 1, h - 20, "pane rule", fill_hex=T["Rule"])
    # quicklook pane: a vcf card
    d.text(f, pane_w + 12, ty + 8, w - pane_w - 24, 12, "ql title",
           "VCARD.VCF — contact", size=11.0, fill_hex=T["Muted"])
    d.frame(f, pane_w + 16, ty + 32, w - pane_w - 32, 120, "vcf card",
            fills=[solid(T["Surface"])], radius=8, stroke_hex=T["Border"])
    d.ellipse(f, pane_w + 28, ty + 44, 40, 40, "avatar", fill_hex=T["Accent"])
    d.text(f, pane_w + 80, ty + 48, 140, 14, "vc name", "Ada Virel",
           size=13.0, style="Medium", fill_hex=T["Ink"])
    d.text(f, pane_w + 80, ty + 68, 140, 12, "vc mail", "ada@virelai.os",
           size=10.0, fill_hex=T["Muted"])
    d.text(f, pane_w + 28, ty + 96, 220, 40, "vc body",
           "TEL +1-555-0123\nORG Storytold Systems\nNOTE art pipeline liaison",
           size=10.0, fill_hex=T["InkMuted"])
    d.rect(f, 0, ty + h - 20, w, 20, "status", fill_hex=T["ChromeBg"])
    d.text(f, 8, ty + h - 16, w - 16, 12, "status txt",
           "7 items · sort name · ^Q quicklook · / filter", size=10.0,
           family=MONO, fill_hex=T["InkMuted"])


def b_term(d, f, ty, w, h):
    textgrid(d, f, 10, ty + 10,
             ["goterm: ready", "gosh$ exec GOTOP.ELF", "gotop: open id=7",
              "gosh$ uname -a", "VirelaiOS sexiburger aarch64-virt",
              "gosh$ |"], line_h=17)


def b_browser(d, f, ty, w, h):
    d.rect(f, 0, ty, w, 16, "kernel band", fill_hex=T["ChromeBg"])
    # nav row at kernelBand+.. : chips + url field (urlRowY)
    d.frame(f, 6, ty + 18, 16, 14, "back", fills=[solid(T["BtnIdle"])],
            radius=4)
    d.text(f, 10, ty + 20, 12, 10, "back g", "<", size=9.0, fill_hex=T["Ink"])
    d.frame(f, 26, ty + 18, 16, 14, "fwd", fills=[solid(T["BtnIdle"])],
            radius=4)
    d.text(f, 30, ty + 20, 12, 10, "fwd g", ">", size=9.0, fill_hex=T["Ink"])
    d.frame(f, 46, ty + 18, 16, 14, "reload", fills=[solid(T["BtnIdle"])],
            radius=4)
    d.text(f, 50, ty + 20, 12, 10, "rl g", "R", size=9.0, fill_hex=T["Ink"])
    d.frame(f, 70, ty + 18, w - 76, 14, "url field",
            fills=[solid(T["Surface"])])
    d.text(f, 76, ty + 20, w - 90, 11, "url", "http://10.0.0.2/docs/",
           size=9.0, family=MONO, fill_hex=T["Ink"])
    # page content
    d.rect(f, 0, ty + 32, w, h - 32 - 16, "page", fill_hex=T["ChromeBg"])
    d.text(f, 24, ty + 48, w - 48, 18, "h1", "VirelaiOS documentation",
           size=15.0, style="Semi Bold", fill_hex=T["Ink"])
    for i, ln in enumerate(["The desktop is a tab rail — one row of live",
                            "apps. Click a cell, or Ctrl+T for the",
                            "launcher. Every app is a full-viewport tab."]):
        d.text(f, 24, ty + 76 + i * 15, w - 48, 12, f"para{i}", ln,
               size=10.0, fill_hex=T["InkMuted"])
    d.text(f, 24, ty + 126, 200, 12, "link", "» desktop.md",
           size=10.0, fill_hex=T["Accent"])
    d.rect(f, 0, ty + h - 16, w, 16, "status", fill_hex=T["ChromeBg"])
    d.text(f, 8, ty + h - 13, w - 60, 10, "status",
           "200 · 4.1 KB · webrender", size=9.0, family=MONO,
           fill_hex=T["Muted"])


def b_pulse(d, f, ty, w, h):
    d.rect(f, 0, ty, w, 22, "tab bar", fill_hex=T["Surface"])
    for i, t in enumerate(["1 procs", "2 net", "3 storage"]):
        tx = 8 + i * 84
        if i == 0:
            d.rect(f, tx - 4, ty + 2, 76, 18, "tab sel",
                   fill_hex=T["Selection"], radius=4)
        d.text(f, tx, ty + 5, 76, 12, f"ptab {t}", t, size=11.0,
               family=MONO, fill_hex=T["Ink"])
    d.text(f, 12, ty + 34, 300, 12, "uptime", "up 3h12m · 4 tasks running",
           size=10.0, family=MONO, fill_hex=T["Muted"])
    for i, (lbl, pct, col) in enumerate(
            [("cpu", 62, T["Accent"]), ("mem", 41, T["Ok"]),
             ("gpu", 8, T["Warning"])]):
        by = ty + 56 + i * 22
        d.text(f, 12, by, 44, 12, f"lbl {lbl}", lbl, size=10.0,
               family=MONO, fill_hex=T["InkMuted"])
        d.rect(f, 60, by + 2, w - 140, 10, f"barbg {lbl}",
               fill_hex=T["BtnIdle"])
        d.rect(f, 60, by + 2, int((w - 140) * pct / 100), 10,
               f"bar {lbl}", fill_hex=col)
        d.text(f, w - 70, by, 50, 12, f"pct {lbl}", f"{pct}%",
               size=10.0, family=MONO, fill_hex=T["Ink"])
    rows = ["PID  NAME      STATE   CPU%   MEM",
            "  1  init      run     0.1   2.1M",
            "  7  gotop     run     3.4   1.2M",
            "  4  gocalc    sleep   0.0   0.9M",
            "  5  goterm    run     0.2   1.1M"]
    textgrid(d, f, 12, ty + 140, rows, size=10.0, line_h=15)
    d.text(f, 12, ty + h - 18, w - 24, 12, "keys",
           "1-4 tabs · j/k move · / filter · s sort · x kill · q quit",
           size=9.0, family=MONO, fill_hex=T["Muted"])


def b_help(d, f, ty, w, h):
    d.text(f, 10, ty + 8, w - 20, 14, "help title", "VirelaiOS Help",
           size=13.0, style="Medium", fill_hex=T["Accent"])
    topics = ["getting-started   the rail, tabs, chords",
              "apps.txt          the 31-app manifest",
              "chords            every bound gesture",
              "files             quicklook, batch ops",
              "settings          SETTINGS.TXT keys",
              "store             signed app channels"]
    for i, t in enumerate(topics):
        d.text(f, 14, ty + 34 + i * 18, w - 28, 14, f"topic {i}", t,
               size=11.0, family=MONO,
               fill_hex=T["Ink"] if i == 0 else T["InkMuted"])
    d.text(f, 10, ty + h - 22, w - 20, 12, "keys",
           "j/k move · enter open · / search · q quit", size=9.0,
           family=MONO, fill_hex=T["Muted"])


def b_welcome(d, f, ty, w, h):
    d.text(f, 16, ty + 10, w - 32, 18, "w title", "Welcome to VirelaiOS",
           size=17.0, style="Semi Bold", fill_hex=T["Ink"])
    gestures = [("Ctrl+T", "open the app launcher"),
                ("Alt+Tab", "cycle focused window"),
                ("Ctrl+Shift+L", "lock the seat"),
                ("Ctrl+Shift+G", "find in the focused app"),
                ("middle-click", "paste the primary selection")]
    for i, (chip, desc) in enumerate(gestures):
        gy = ty + 44 + i * 34
        d.frame(f, 16, gy, 128, 24, f"chip {i}", fills=[solid(T["ChromeBg"])],
                radius=4, stroke_hex=T["Border"])
        d.text(f, 24, gy + 6, 116, 12, f"chip t {i}", chip, size=11.0,
               family=MONO, fill_hex=T["Accent"])
        d.text(f, 156, gy + 6, w - 170, 12, f"gest {i}", desc, size=11.0,
               fill_hex=T["Ink"])
    for i, lbl in enumerate(["Files", "Terminal", "Help"]):
        btn(d, f, 16 + i * 110, ty + h - 44, 100, 26, lbl)


def b_top(d, f, ty, w, h):
    hdr = ["PID", "NAME", "STATE", "EXIT", "CPU%", "MEM"]
    colx = [8, 60, 170, 250, 330, 400]
    d.rect(f, 0, ty, w, 22, "hdr", fill_hex=T["Surface"])
    for i, t in enumerate(hdr):
        d.text(f, colx[i], ty + 5, 90, 12, f"hdr {t}", t, size=10.0,
               family=MONO, fill_hex=T["InkMuted"])
    procs = [(1, "init", "run", "-", "0.1", "2.1M"),
             (4, "gocalc", "sleep", "-", "0.0", "0.9M"),
             (5, "goterm", "run", "-", "0.2", "1.1M"),
             (6, "goirc", "run", "-", "0.4", "1.6M"),
             (7, "gotop", "run", "-", "3.4", "1.2M")]
    for i, row in enumerate(procs):
        ry = ty + 26 + i * 18
        if i == 4:
            d.rect(f, 0, ry - 2, w, 18, "sel", fill_hex=T["Selection"])
        for j, val in enumerate(row):
            d.text(f, colx[j], ry + 2, 90, 12, f"r{i}c{j}", str(val),
                   size=10.0, family=MONO, fill_hex=T["Ink"])
    d.text(f, 8, ty + h - 22, w - 16, 12, "keys",
           "click column sorts · click row arms kill · n net counters",
           size=9.0, family=MONO, fill_hex=T["Muted"])


def b_goset(d, f, ty, w, h):
    nav_w = 130
    d.rect(f, 0, ty, nav_w, h, "nav", fill_hex=T["ChromeBg"])
    for i, sec in enumerate(["General", "Theme", "Input", "Audio", "A11y"]):
        ry = ty + 8 + i * 24
        if i == 1:
            d.rect(f, 0, ry - 3, nav_w, 24, "navsel",
                   fill_hex=T["Selection"])
            d.rect(f, 0, ry - 3, 3, 24, "navsel edge", fill_hex=T["Accent"])
        d.text(f, 10, ry, nav_w - 16, 12, f"nav {sec}", sec, size=11.0,
               fill_hex=T["Ink"])
    d.rect(f, nav_w, ty, 1, h, "nav rule", fill_hex=T["Rule"])
    x = nav_w + 16
    d.text(f, x, ty + 10, 200, 14, "sect t", "Theme", size=13.0,
           style="Medium", fill_hex=T["Ink"])
    rows = [("theme", "dark  light", "dropdown"),
            ("a11y.contrast", "off", "toggle"),
            ("a11y.text_scale", "1.0", "slider"),
            ("a11y.reduce_motion", "on", "toggle")]
    for i, (k, v, kind) in enumerate(rows):
        ry = ty + 40 + i * 34
        d.text(f, x, ry + 4, 180, 12, f"key {k}", k, size=11.0,
               family=MONO, fill_hex=T["Ink"])
        if kind == "dropdown":
            d.frame(f, x + 200, ry - 2, 130, 22, f"dd {k}",
                    fills=[solid(T["Surface"])], radius=4,
                    stroke_hex=T["Border"])
            d.text(f, x + 208, ry + 3, 100, 12, f"ddv {k}", v, size=10.0,
                   fill_hex=T["Ink"])
            d.text(f, x + 316, ry + 3, 12, 10, f"ddc {k}", "v", size=9.0,
                   fill_hex=T["Muted"])
        elif kind == "toggle":
            on = v == "on"
            d.frame(f, x + 200, ry - 2, 40, 20, f"tg {k}",
                    fills=[solid(T["Accent"] if on else T["BtnIdle"])],
                    radius=10, stroke_hex=None if on else T["Border"])
            d.ellipse(f, x + (222 if on else 202), ry, 16, 16,
                      f"tgk {k}", fill_hex=T["OnAccent"] if on else T["Muted"])
            d.text(f, x + 250, ry + 3, 60, 12, f"tgv {k}", v, size=10.0,
                   family=MONO, fill_hex=T["Muted"])
        else:
            d.rect(f, x + 200, ry + 7, 100, 4, f"slbg {k}",
                   fill_hex=T["BtnIdle"], radius=2)
            d.ellipse(f, x + 240, ry + 1, 14, 14, f"slk {k}",
                      fill_hex=T["Accent"])
            d.text(f, x + 310, ry + 3, 40, 12, f"slv {k}", v, size=10.0,
                   family=MONO, fill_hex=T["Muted"])
    # palette band
    for i, tok in enumerate(["Bg", "Surface", "Border", "Accent", "Text"]):
        d.rect(f, x + i * 36, ty + h - 44, 32, 24, f"pal {tok}",
               fill_hex=T[tok], stroke_hex=T["Border"])
    d.text(f, x, ty + h - 16, 300, 10, "pal lbl",
           "live palette preview", size=8.0, fill_hex=T["Muted"])


def b_view(d, f, ty, w, h):
    d.rect(f, 8, ty + 8, w - 16, h - 52, "canvas", fill_hex=T["ChromeBg"])
    # checkerboard hint + image block
    d.rect(f, 80, ty + 40, w - 160, h - 140, "image",
           fills=[vgrad(0x3B82F6, 0x1A1A2E)], radius=4)
    d.text(f, 90, ty + 48, w - 180, 12, "img ann",
           "MAP.QOI 160x120 — blit scaled", size=9.0, fill_hex=T["OnAccent"])
    d.rect(f, 0, ty + h - 20, w, 20, "status", fill_hex=T["ChromeBg"])
    d.text(f, 8, ty + h - 16, w - 16, 12, "status",
           "map.qoi  160x120 qoi  zoom 200%  +/-  fit", size=9.0,
           family=MONO, fill_hex=T["InkMuted"])


def b_sound(d, f, ty, w, h):
    d.text(f, 12, ty + 8, w - 24, 14, "track", "chime.wav — 0:07 / 0:12",
           size=13.0, style="Medium", fill_hex=T["Ink"])
    # progress ring (StrokeArc look: circle + arc hint)
    d.ellipse(f, w // 2 - 30, ty + 30, 60, 60, "ring bg",
              stroke_hex=T["ChromeBg"], stroke_w=6)
    d.ellipse(f, w // 2 - 30, ty + 30, 60, 60, "ring arc",
              stroke_hex=T["Accent"], stroke_w=6)
    d.text(f, w // 2 - 18, ty + 52, 40, 14, "pp", "||", size=15.0,
           family=MONO, fill_hex=T["Ink"])
    d.rect(f, 12, ty + h - 32, w - 24, 4, "seek", fill_hex=T["BtnIdle"],
           radius=2)
    d.rect(f, 12, ty + h - 32, (w - 24) * 7 // 12, 4, "seek fill",
           fill_hex=T["Accent"], radius=2)
    d.text(f, 12, ty + h - 20, w - 24, 10, "hint",
           "space play/pause · arrows seek", size=8.0, fill_hex=T["Muted"])


def b_tabwm(d, f, ty, w, h):
    # Zig fallback seat: a mini desktop — tab bar + one window inside
    d.rect(f, 0, ty, w, 18, "zig tabbar", fill_hex=T["ChromeBg"])
    for i, t in enumerate(["TERM", "CALC", "NOTEPAD"]):
        tx = 4 + i * 76
        if i == 0:
            d.rect(f, tx - 2, ty + 2, 72, 14, "ztab sel",
                   fill_hex=T["Surface"])
        d.text(f, tx, ty + 4, 68, 10, f"ztab {t}", t, size=8.0,
               family=MONO, fill_hex=T["Ink"])
    d.frame(f, 60, ty + 60, w - 140, h - 130, "zig window",
            fills=[solid(T["Bg"])], stroke_hex=T["Border"])
    d.rect(f, 60, ty + 60, w - 140, 16, "zig titlebar",
           fill_hex=T["Surface"])
    d.text(f, 66, ty + 63, 200, 10, "zig title", "TERM.BIN",
           size=9.0, family=MONO, fill_hex=T["Ink"])
    textgrid(d, f, 66, ty + 84, ["$ ls", "APPS.TXT  DOCUMENTS/"], size=10.0,
             line_h=14)
    d.text(f, 8, ty + h - 20, w - 16, 12, "znote",
           "TABWM.BIN — the Zig fallback seat (ADR 0034): windowed tabs, "
           "not the Go rail", size=9.0, fill_hex=T["Muted"])


def b_store(d, f, ty, w, h):
    d.rect(f, 0, ty, w, 20, "hdr", fill_hex=T["Surface"])
    d.text(f, 8, ty + 4, 300, 12, "hdr t",
           "store — channel: flintd — 6 signed", size=10.0, family=MONO,
           fill_hex=T["Ink"])
    d.frame(f, 8, ty + 28, w - 16, 18, "search", fills=[solid(T["ChromeBg"])],
            radius=4)
    d.text(f, 14, ty + 32, 200, 10, "sq", "/calc", size=10.0, family=MONO,
           fill_hex=T["InkMuted"])
    rows = [("GOCALC        1.4  installed", False),
            ("GOPAINT       0.9  update 1.1", True),
            ("GOCHORDS      1.0  available", False),
            ("GOGIT         2.1  pinned 2.0", False)]
    for i, (r, sel) in enumerate(rows):
        ry = ty + 54 + i * 14
        if sel:
            d.rect(f, 4, ry - 2, w - 8, 14, "sel", fill_hex=T["Selection"])
        d.text(f, 10, ry, w - 20, 11, f"srow {i}", r, size=10.0,
               family=MONO, fill_hex=T["Ink"])
    d.frame(f, 8, ty + 116, w - 16, 90, "detail", fills=[solid(T["Surface"])],
            radius=4, stroke_hex=T["Border"])
    d.text(f, 16, ty + 124, 300, 12, "det t", "GOPAINT 0.9 -> 1.1",
           size=11.0, style="Medium", fill_hex=T["Ink"])
    d.text(f, 16, ty + 142, w - 40, 52, "det b",
           "sig ok · sha256 9f2c… · channel stable\n"
           "i install · u update · r remove · p pin prev",
           size=10.0, family=MONO, fill_hex=T["InkMuted"])
    d.text(f, 8, ty + h - 18, w - 16, 12, "log",
           "j/k move · enter detail · / search · l reload · q quit",
           size=9.0, family=MONO, fill_hex=T["Muted"])


def b_infer(d, f, ty, w, h):
    d.text(f, 8, ty + 8, w - 16, 18, "st1", "model: stub (PRNG weights)",
           size=11.0, family=MONO, fill_hex=T["Ink"])
    d.text(f, 8, ty + 26, w - 16, 14, "st2",
           "session: available · sys_gpucomp", size=10.0, family=MONO,
           fill_hex=T["InkMuted"])
    btn(d, f, 8, ty + 44, 96, 24, "Run stub")
    btn(d, f, 112, ty + 44, 110, 24, "Run model")
    d.rect(f, 0, ty + 80, w, h - 80, "log", fill_hex=T["ChromeBg"])
    textgrid(d, f, 10, ty + 88,
             ["goinfer: licence ok", "goinfer: session open",
              "goinfer: prompt 12 tokens", "goinfer: the seat is a rail —"],
             size=10.0, line_h=15)


def b_rec(d, f, ty, w, h):
    d.text(f, 8, ty + 8, w - 16, 18, "cap",
           "capture: 48000 Hz s16 mono", size=11.0, family=MONO,
           fill_hex=T["Ink"])
    d.text(f, 8, ty + 26, w - 16, 14, "dest", "out: /host/REC.WAV",
           size=10.0, family=MONO, fill_hex=T["InkMuted"])
    btn(d, f, 8, ty + 44, 96, 24, "Record")
    d.rect(f, 0, ty + 80, w, h - 80, "log", fill_hex=T["ChromeBg"])
    textgrid(d, f, 10, ty + 88,
             ["gorec: cap ok 48000 s16 mono", "gorec: write REC.WAV",
              "gorec: 12.0s 1152000B"], size=10.0, line_h=15)


def b_snap(d, f, ty, w, h):
    rows = ["BASE        2026-10-20", "PRE-M165    2026-10-22",
            "DEMO        2026-10-23"]
    listrows(d, f, 8, ty + 8, w - 16, rows, selected=0, row_h=20)
    d.frame(f, 8, ty + 76, w - 16, 20, "name field",
            fills=[solid(T["ChromeBg"])], radius=4,
            stroke_hex=T["Border"])
    d.text(f, 14, ty + 81, 200, 10, "nf ph", "snapshot name…",
           size=10.0, family=MONO, fill_hex=T["Muted"])
    btn(d, f, 8, ty + 104, 70, 24, "Save")
    btn(d, f, 86, ty + 104, 80, 24, "Restore")
    btn(d, f, 174, ty + 104, 76, 24, "Delete")
    d.text(f, 8, ty + 140, w - 16, 12, "hint",
           "Restore/Delete arm first: 'Confirm?' is the consent twin",
           size=9.0, family=MONO, fill_hex=T["Muted"])
    d.rect(f, 0, ty + 160, w, h - 160, "log", fill_hex=T["ChromeBg"])
    textgrid(d, f, 10, ty + 166,
             ["gosnap: save BASE ok", "gosnap: consent restore BASE"],
             size=10.0, line_h=15)


def b_assist(d, f, ty, w, h):
    side_w = 168
    d.rect(f, 0, ty, side_w, h, "conv rail", fill_hex=T["ChromeBg"])
    convs = ["design loop", "boot order", "gate triage", "+ new"]
    for i, cv in enumerate(convs):
        ry = ty + 8 + i * 22
        if i == 0:
            d.rect(f, 0, ry - 3, side_w, 22, "convsel",
                   fill_hex=T["Selection"])
            d.rect(f, 0, ry - 3, 3, 22, "convsel edge", fill_hex=T["Accent"])
        d.text(f, 10, ry + 2, side_w - 16, 12, f"conv {i}", cv,
               size=11.0, fill_hex=T["Ink"])
    x = side_w + 8
    msgs = [("you", "what does the rail badge mean?", T["Surface"]),
            ("assistant", "a Warning block on a frozen tab — the app "
             "stopped answering.", T["ChromeBg"]),
            ("you", "and the scope chip?", T["Surface"])]
    my = ty + 10
    for who, msg, face in msgs:
        bw = min(w - x - 16, 60 + 7 * len(msg))
        d.frame(f, x, my, bw, 34, f"msg {who}", fills=[solid(face)],
                radius=8)
        d.text(f, x + 8, my + 5, bw - 16, 24, f"msgt {who}", msg,
               size=10.0, fill_hex=T["Ink"])
        my += 42
    d.frame(f, x, ty + h - 40, w - x - 12, 28, "prompt",
            fills=[solid(T["ChromeBg"])], radius=4,
            stroke_hex=T["Accent"], stroke_w=2)
    d.text(f, x + 8, ty + h - 32, w - x - 40, 12, "prompt ph",
           "message assistant…", size=11.0, fill_hex=T["Muted"])


def b_sheet(d, f, ty, w, h):
    d.rect(f, 0, ty, w, 24, "menubar", fill_hex=T["Surface"])
    for i, t in enumerate(["Edit", "Format"]):
        d.text(f, 8 + i * 64, ty + 6, 60, 12, f"mb {t}", t, size=11.0,
               fill_hex=T["Ink"])
    d.frame(f, 8, ty + 28, 40, 20, "cell ref", fills=[solid(T["ChromeBg"])])
    d.text(f, 16, ty + 33, 30, 10, "ref", "A1", size=10.0, family=MONO,
           fill_hex=T["Ink"])
    d.frame(f, 56, ty + 28, w - 64, 20, "editline",
            fills=[solid(T["ChromeBg"])])
    d.text(f, 62, ty + 33, w - 80, 10, "el", "=SUM(B2:B9)", size=10.0,
           family=MONO, fill_hex=T["Ink"])
    # grid
    cols, rows = 8, 8
    cw, chh = (w - 60) // cols, 18
    gx, gy = 8, ty + 56
    for ci in range(cols):
        d.rect(f, gx + 24 + ci * cw, gy, cw, 16, f"ch {ci}",
               fill_hex=T["Surface"])
        d.text(f, gx + 24 + ci * cw + 4, gy + 3, cw - 8, 10, f"cl {ci}",
               chr(65 + ci), size=9.0, family=MONO, fill_hex=T["Muted"])
    for ri in range(rows):
        yy = gy + 16 + ri * chh
        d.rect(f, gx, yy, 24, chh, f"rh {ri}", fill_hex=T["Surface"])
        d.text(f, gx + 8, yy + 4, 14, 10, f"rl {ri}", str(ri + 1),
               size=9.0, family=MONO, fill_hex=T["Muted"])
        for ci in range(cols):
            sel = (ri == 0 and ci == 0)
            d.rect(f, gx + 24 + ci * cw, yy, cw, chh, f"c{ri},{ci}",
                   fill_hex=T["Bg"], stroke_hex=T["Rule"])
            if sel:
                d.rect(f, gx + 24 + ci * cw, yy, cw, chh, "cellsel",
                       fills=[solid(0, 0)], stroke_hex=T["Accent"],
                       stroke_w=2)
    vals = {(0, 1): "Q3", (0, 2): "14.2", (1, 1): "Q4", (1, 2): "16.8",
            (2, 1): "total", (2, 2): "31.0"}
    for (ri, ci), v in vals.items():
        d.text(f, gx + 24 + ci * cw + 4, gy + 16 + ri * chh + 4, cw - 8,
               10, f"v{ri}{ci}", v, size=9.0, family=MONO,
               fill_hex=T["Ink"])
    d.rect(f, 0, ty + h - 20, w, 20, "status", fill_hex=T["ChromeBg"])
    d.text(f, 8, ty + h - 16, w - 16, 12, "st",
           "A1 · =SUM(B2:B9) · fill 0 · utf-8 csv", size=9.0, family=MONO,
           fill_hex=T["InkMuted"])


def b_reader(d, f, ty, w, h):
    d.rect(f, 0, ty, w, 24, "nav bar", fill_hex=T["Surface"])
    for i, t in enumerate(["<", "3 / 12", ">", "-", "150%", "+"]):
        d.text(f, 12 + i * 66, ty + 6, 60, 12, f"nav {t}", t, size=11.0,
               family=MONO, fill_hex=T["Ink"])
    # page bitmap on chrome bg
    pw, ph = 320, 420
    px = (w - pw) // 2
    d.rect(f, 0, ty + 24, w, h - 24 - 24, "reader bg",
           fill_hex=T["ChromeBg"])
    d.rect(f, px, ty + 34, pw, ph, "page", fill_hex=0xF8F8F4)
    d.text(f, px + 20, ty + 52, pw - 40, 16, "doc h",
           "VirelaiOS — operator notes", size=13.0, style="Semi Bold",
           fill_hex=0x1A1A22)
    for i in range(12):
        d.rect(f, px + 20, ty + 84 + i * 14, pw - 40 - (i % 4) * 30, 6,
               f"docline {i}", fill_hex=0xC8C8C0)
    d.rect(f, 0, ty + h - 24, w, 24, "find", fill_hex=T["Surface"])
    d.text(f, 10, ty + h - 18, 300, 12, "find b",
           "find: seat   —   4/9 hits", size=10.0, family=MONO,
           fill_hex=T["Muted"])


def b_clock(d, f, ty, w, h):
    d.rect(f, 0, ty, w, 26, "tab strip", fill_hex=T["Surface"])
    for i, t in enumerate(["World", "Stopwatch", "Timer", "Alarm"]):
        tx = 8 + i * 90
        if i == 1:
            d.rect(f, tx - 4, ty + 3, 84, 20, "ctab sel",
                   fill_hex=T["Selection"], radius=10)
        d.text(f, tx + 8, ty + 7, 76, 12, f"ctab {t}", t, size=11.0,
               fill_hex=T["Ink"])
    d.text(f, 0, ty + 70, w, 56, "sw digits", "04:59.31", size=44.0,
           family=MONO, fill_hex=T["Ink"])
    for i, lbl in enumerate(["Lap", "Reset", "Start"]):
        btn(d, f, w // 2 - 130 + i * 90, ty + 150, 80, 26, lbl)
    laps = ["lap 3   00:58.20", "lap 2   00:59.84", "lap 1   01:00.12"]
    for i, l in enumerate(laps):
        d.text(f, w // 2 - 70, ty + 196 + i * 18, 140, 12, f"lap {i}", l,
               size=10.0, family=MONO, fill_hex=T["InkMuted"])
    d.text(f, 8, ty + h - 20, w - 16, 12, "tz",
           "world: UTC  local  —  timer presets 1/3/5/10/25",
           size=9.0, family=MONO, fill_hex=T["Muted"])


def b_mine(d, f, ty, w, h):
    d.text(f, 12, ty + 10, 200, 14, "hd",
           "mines 40   time 01:12   reset(R)", size=11.0, family=MONO,
           fill_hex=T["Ink"])
    cells, cell = 16, 24
    gw = cells * cell
    gx, gy = (w - gw) // 2, ty + 36
    revealed = {(2, 3): "1", (3, 3): "2", (4, 3): "", (5, 4): "1",
                (2, 4): "", (3, 4): "1", (7, 8): "3", (8, 8): "2"}
    flagged = {(1, 1), (6, 6), (10, 11), (12, 3)}
    blown = (9, 2)
    for ry in range(10):
        for cx in range(cells):
            xx, yy = gx + cx * cell, gy + ry * cell
            if (cx, ry) == blown:
                d.rect(f, xx, yy, cell - 1, cell - 1, f"m{cx},{ry}",
                       fill_hex=T["Danger"])
            elif (cx, ry) in revealed:
                d.rect(f, xx, yy, cell - 1, cell - 1, f"m{cx},{ry}",
                       fill_hex=T["ChromeBg"], stroke_hex=T["Rule"])
                v = revealed[(cx, ry)]
                if v:
                    d.text(f, xx + 8, yy + 5, 10, 10, f"mn{cx},{ry}", v,
                           size=10.0, family=MONO,
                           fill_hex=T["Accent"] if v == "1" else
                           (T["Ok"] if v == "2" else T["Danger"]))
            else:
                d.rect(f, xx, yy, cell - 1, cell - 1, f"m{cx},{ry}",
                       fill_hex=T["BtnIdle"], stroke_hex=T["Rule"])
                if (cx, ry) in flagged:
                    d.text(f, xx + 7, yy + 4, 10, 10, f"mf{cx},{ry}", "F",
                           size=10.0, family=MONO, fill_hex=T["Warning"])
    d.text(f, 12, ty + h - 20, w - 24, 12, "keys",
           "left reveal · right flag · chord on satisfied number",
           size=9.0, family=MONO, fill_hex=T["Muted"])


def b_sol(d, f, ty, w, h):
    cw, chh, gap = 52, 72, 10
    x0, y0 = 20, ty + 12
    labels = ["stock", "waste", "", "A", "A", "A", "A"]
    for i in range(7):
        xx = x0 + i * (cw + gap)
        if i == 2:
            continue
        face = T["ChromeBg"] if i >= 3 else T["Surface"]
        d.frame(f, xx, y0, cw, chh, labels[i] or f"fd{i}",
                fills=[solid(face)], radius=4, stroke_hex=T["Rule"])
        if i == 0:
            d.text(f, xx + 12, y0 + 28, 30, 12, "stock bk", "SB",
                   size=10.0, family=MONO, fill_hex=T["Muted"])
        if i == 1:
            card(d, f, xx, y0, cw, chh, "7h")
        if i >= 3:
            card(d, f, xx, y0, cw, chh, ["AS", "KH", "QD", "JC"][i - 3])
    ty0 = y0 + chh + 14
    heights = [1, 2, 3, 4, 5, 6, 7]
    for i in range(7):
        xx = x0 + i * (cw + gap)
        for j in range(min(heights[i], 4)):
            faceup = j == min(heights[i], 4) - 1
            yy = ty0 + j * 16
            if faceup:
                card(d, f, xx, yy, cw, chh, "9s" if i % 2 else "4d")
            else:
                d.frame(f, xx, yy, cw, 16, f"back{i},{j}",
                        fills=[solid(T["BtnIdle"])], radius=3,
                        stroke_hex=T["Rule"])
    d.text(f, 20, ty + h - 20, w - 40, 12, "keys",
           "draw-1 · drag to move · dbl-click foundation · u undo",
           size=9.0, family=MONO, fill_hex=T["Muted"])


def card(d, f, x, y, w, h, label):
    d.frame(f, x, y, w, h, f"card {label}", fills=[solid(0xF4F4F0)],
            radius=4, stroke_hex=T["Border"])
    red = label.endswith("h") or label.endswith("d")
    d.text(f, x + 4, y + 4, w - 8, 12, f"cardt {label}", label, size=11.0,
           style="Medium", family=MONO,
           fill_hex=0xC0262C if red else 0x1A1A22)


def b_emoji(d, f, ty, w, h):
    d.rect(f, 0, ty, w, 24, "tab strip", fill_hex=T["Surface"])
    for i, t in enumerate(["Emoji", "Compose", "Kaomoji"]):
        tx = 8 + i * 80
        if i == 0:
            d.rect(f, tx - 4, ty + 3, 74, 18, "esel", fill_hex=T["Selection"],
                   radius=9)
        d.text(f, tx + 6, ty + 6, 70, 12, f"etab {t}", t, size=11.0,
               fill_hex=T["Ink"])
    d.frame(f, 8, ty + 30, w - 16, 20, "search", fills=[solid(T["ChromeBg"])],
            radius=4, stroke_hex=T["Border"])
    d.text(f, 14, ty + 35, 200, 10, "sq", "burger", size=10.0,
           family=MONO, fill_hex=T["InkMuted"])
    d.text(f, 10, ty + 56, 200, 10, "shelf", "pinned", size=8.0,
           fill_hex=T["Muted"])
    cells = 8
    for i in range(16):
        cx = 12 + (i % cells) * 44
        cy = ty + 70 + (i // cells) * 44
        sel = i == 3
        d.frame(f, cx, cy, 40, 40, f"ecell {i}",
                fills=[solid(T["Selection"] if sel else T["Surface"])],
                radius=4, stroke_hex=T["Accent"] if sel else None,
                stroke_w=2)
        d.text(f, cx + 8, cy + 8, 24, 20, f"eg {i}",
               "SB" if i == 3 else chr(65 + i), size=15.0, family=MONO,
               fill_hex=T["Ink"])
    d.rect(f, 0, ty + h - 20, w, 20, "status", fill_hex=T["ChromeBg"])
    d.text(f, 8, ty + h - 16, w - 16, 12, "st",
           "U+1F354 · enter picks · F10 pins · esc closes", size=9.0,
           family=MONO, fill_hex=T["InkMuted"])


def b_irc(d, f, ty, w, h):
    rail_w = 130
    d.rect(f, 0, ty, rail_w, h, "chan rail", fill_hex=T["ChromeBg"])
    for i, ch in enumerate(["#virelai", "#art", "#gates", "*server"]):
        ry = ty + 8 + i * 22
        if i == 0:
            d.rect(f, 0, ry - 3, rail_w, 22, "chsel",
                   fill_hex=T["Selection"])
            d.rect(f, 0, ry - 3, 3, 22, "chsel edge", fill_hex=T["Accent"])
        d.text(f, 10, ry + 3, rail_w - 16, 12, f"ch {ch}", ch,
               size=11.0, family=MONO, fill_hex=T["Ink"])
    x = rail_w + 10
    log = ["<ada> the rail badge landed", "<bob> gates green on ref host",
           "<ada> goirc: connected 10.0.0.2:6667",
           "* you were mentioned in #virelai", "<carol> push the sheet?"]
    textgrid(d, f, x, ty + 10, log, size=10.0, line_h=18)
    d.frame(f, x, ty + h - 32, w - x - 10, 24, "input",
            fills=[solid(T["ChromeBg"])], radius=4,
            stroke_hex=T["Border"])
    d.text(f, x + 8, ty + h - 26, w - x - 30, 12, "in",
           "#virelai: lgtm, ship it_", size=10.0, family=MONO,
           fill_hex=T["Ink"])


def b_vault(d, f, ty, w, h):
    d.frame(f, 8, ty + 8, w - 16, 20, "pass field",
            fills=[solid(T["ChromeBg"])], radius=4,
            stroke_hex=T["Accent"], stroke_w=2)
    d.text(f, 14, ty + 13, 200, 10, "pm", "************", size=10.0,
           family=MONO, fill_hex=T["Ink"])
    rows = ["api.flintd        token    ••••  TOTP",
            "mail@virelai.os   login    ••••",
            "backup.key        secret   ••••",
            "receipts.txt      file     read-only"]
    for i, r in enumerate(rows):
        ry = ty + 40 + i * 20
        if i == 0:
            d.rect(f, 4, ry - 3, w - 8, 20, "sel",
                   fill_hex=T["Selection"])
            d.rect(f, 4, ry - 3, 3, 20, "sel edge", fill_hex=T["Accent"])
        d.text(f, 10, ry, w - 20, 12, f"vrow {i}", r, size=10.0,
               family=MONO, fill_hex=T["Ink"])
    d.text(f, 8, ty + 140, w - 16, 12, "hint",
           "enter reveals 30s · c copies, expires · idle locks",
           size=9.0, family=MONO, fill_hex=T["Muted"])
    d.frame(f, 8, ty + 160, w - 16, 60, "detail", fills=[solid(T["Surface"])],
            radius=4, stroke_hex=T["Border"])
    d.text(f, 16, ty + 168, w - 40, 44, "det",
           "api.flintd\nuser: agent — pass: ******** (enter to reveal)\n"
           "totp: 482 913", size=10.0, family=MONO, fill_hex=T["InkMuted"])


def b_a11y(d, f, ty, w, h):
    d.text(f, 10, ty + 8, w - 20, 14, "a title",
           "Focused window: GOFILES (win=5)", size=11.0, family=MONO,
           fill_hex=T["Ink"])
    tree = ["window  GOFILES — Files", "  pane    file list",
            "    row   VCARD.VCF (selected)", "  pane    quicklook",
            "    card  contact preview", "  status  7 items"]
    for i, t in enumerate(tree):
        d.text(f, 14, ty + 34 + i * 18, w - 28, 14, f"tree {i}", t,
               size=11.0, family=MONO,
               fill_hex=T["Accent"] if "selected" in t else T["InkMuted"])
    d.text(f, 10, ty + h - 24, w - 20, 12, "poll",
           "WINDOWS_QUERY every 500ms · outline /host/A11Y.<win>",
           size=9.0, family=MONO, fill_hex=T["Muted"])


CONSOLE_SCRIPTS = {
    "GOSH.ELF": ["gosh$ ls /host", "APPS.TXT  DOCUMENTS/  MAIL/",
                 "gosh$ exec GOTOP.ELF &", "gotop: open id=7",
                 "gosh$ echo $PROMPT", "gosh$ "],
    "GOSTALGIA.ELF": ["argv: shell --root /host/GS", "gs: mount /GS",
                      "gs> catalog", "SYSTEM/  GAMES/  DESKTOP.ACCS/",
                      "gs> run GSOS.SYS16", "(gsport tty — console app)"],
    "GOMAIL.ELF": ["gomail: account /host/GOMAIL.TXT",
                   "gomail: dial mail.example 993 tls",
                   "gomail: imap ready", "gomail: login ada",
                   "gomail: use INBOX exists=12",
                   "  12  carol@…  Re: art drop",
                   "  11  bob@…    gate results",
                   "gomail: body 12 text/plain bytes=1840"],
}


def build_apps(path):
    d = Doc("VirelaiOS app fleet", "Apps", 0x101418)
    apps = [
        ("GOCALC.ELF", "64-bit Calc", 512, 384, b_calc),
        ("NOTE.ELF", "Text Editor", 512, 384, b_note),
        ("GOEDIT.ELF", "Code Editor", 512, 384, b_edit),
        ("GOFILES.ELF", "Files", 512, 384, b_files),
        ("GOTERM.ELF", "Terminal", 640, 400, b_term),
        ("WEB.ELF", "Web", 512, 384, b_browser),
        ("PULSE.ELF", "Pulse", 640, 400, b_pulse),
        ("GOSH.ELF", "Shell", 512, 384,
         lambda d, f, t, w, h: b_console(d, f, t, w, h, CONSOLE_SCRIPTS["GOSH.ELF"])),
        ("GOHELP.ELF", "Help", 512, 384, b_help),
        ("GOWELCOME.ELF", "Welcome", 512, 384, b_welcome),
        ("GOTOP.ELF", "Top", 512, 384, b_top),
        ("GOSET.ELF", "Settings", 560, 360, b_goset),
        ("GOVIEW.ELF", "Image Viewer", 512, 384, b_view),
        ("GOSOUND.ELF", "Sound", 344, 152, b_sound),
        ("TABWM.BIN", "Tabbed Desktop", 640, 360, b_tabwm),
        ("GOSTALGIA.ELF", "Gostalgia", 512, 384,
         lambda d, f, t, w, h: b_console(d, f, t, w, h, CONSOLE_SCRIPTS["GOSTALGIA.ELF"])),
        ("GOSTORE.ELF", "Store", 640, 480, b_store),
        ("GOINFER.ELF", "LLM Infer", 560, 340, b_infer),
        ("GOREC.ELF", "Recorder", 480, 320, b_rec),
        ("GOSNAP.ELF", "Snapshots", 480, 300, b_snap),
        ("GOASSIST.ELF", "Assistant", 640, 420, b_assist),
        ("GOSHEET.ELF", "Sheet", 672, 420, b_sheet),
        ("GOREADER.ELF", "Reader", 760, 560, b_reader),
        ("GOCLOCK.ELF", "Clock", 640, 400, b_clock),
        ("GOMINE.ELF", "Mines", 720, 560, b_mine),
        ("GOSOL.ELF", "Solitaire", 512, 384, b_sol),
        ("GOEMOJI.ELF", "Emoji", 512, 384, b_emoji),
        ("GOIRC.ELF", "IRC", 640, 400, b_irc),
        ("GOVAULT.ELF", "Vault", 512, 384, b_vault),
        ("GOMAIL.ELF", "Mail", 512, 384,
         lambda d, f, t, w, h: b_console(d, f, t, w, h, CONSOLE_SCRIPTS["GOMAIL.ELF"])),
        ("GOA11Y.ELF", "Accessibility", 512, 384, b_a11y),
    ]
    # layout: 4 columns; each row's height follows its tallest app
    cols, gapx, gapy = 4, 64, 72
    maxw = max(w for _, _, w, _, _ in apps)
    cellw = maxw + 40
    nrows = (len(apps) + cols - 1) // cols
    row_hs = [max(h + TITLE_H + 40
                  for _, _, _, h, _ in apps[r * cols:(r + 1) * cols])
              for r in range(nrows)]
    row_ys = [60]
    for rh in row_hs[:-1]:
        row_ys.append(row_ys[-1] + rh + gapy)
    d.text(1, 40, 20, 1400, 20, "fleet note",
           "The 31-app fleet — windows at their declared natural size "
           "(user/go/<app> declare block), the 28px floating titlebar "
           "spec on top. Under gotabwm each is a full-viewport tab.",
           size=11.0, fill_hex=T["Muted"])
    for i, (name, title, w, h, body) in enumerate(apps):
        col, row = i % cols, i // cols
        x = 40 + col * (cellw + gapx)
        y = row_ys[row]
        app_window(d, 1, x, y, name, f"{title} — {name}", w, h, body)
        d.text(1, x, y + h + TITLE_H + 8, w + 80, 12, f"cap {name}",
               f"{name} · {w}x{h} natural", size=9.0,
               family=MONO, fill_hex=T["Muted"])
    save_figcraft(d, path)


if __name__ == "__main__":
    out = "/tmp/virelai-figcraft"
    os.makedirs(out, exist_ok=True)
    build_tokens(f"{out}/tokens.figcraft")
    build_shell(f"{out}/seat-shell.figcraft")
    build_apps(f"{out}/apps.figcraft")
    for f in sorted(os.listdir(out)):
        print(f, os.path.getsize(f"{out}/{f}"))
