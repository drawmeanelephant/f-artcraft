#!/usr/bin/env python3
"""VirelaiOS shared tokens for virelai-series drivers.

Theme hexes are the shipped values copied from drawmeanelephant/VirelaiOS
`user/go/theme/theme.go` (dark is the boot default) and the geometry contract
is `docs/ui-primitives.md` v2. Mascot and navy-field colors are sampled off
the shipped QOI fixtures (mascot_64x64.qoi, WALLPAPER.QOI). The rules behind
the numbers live in virelai/notes/style-bible.md — cite it, import this.

Usage (after the usual `sys.path.insert(0, <repo>/work)` bootstrap):
    from virelai.vkit import DARK, INK, NAVY, BUN, SIZE
"""

# --- warm dark ink: never pure black -----------------------------------------
INK = "#503139"        # house ink; the fixture outline family is below
INK_LO = "#634B48"     # mascot_64x64.qoi outline, dark end
INK_HI = "#7B5E5A"     # outline, warm light end

# --- navy field ----------------------------------------------------------------
NAVY = "#1E1E2E"       # WALLPAPER.QOI dominant field (93% of the canvas)
WALL_TOP = "#1A1A2E"   # seat desktop gradient top  (theme: WallpaperTop)
WALL_BOT = "#0A0A14"   # seat desktop gradient bottom (WallpaperBot)

# --- mascot (sexiburger), sampled ----------------------------------------------
BUN = "#FDB845"        # bun/body, lit — the character's dominant color
BUN_MID = "#F5AC3C"
BUN_SHADE = "#DA761E"  # WALLPAPER.QOI render, shadow side
BUN_DEEP = "#9D4A0D"
GLOVE = "#FFFFFF"      # white-glove hands

# --- shipped theme tokens -------------------------------------------------------
# Dark = boot default (byte-identical to Zig THEME_DARK); Light = shipped alt.
DARK = {
    "Bg": "#182026", "Surface": "#222D35", "Border": "#334155",
    "Text": "#FFFFFF", "Muted": "#94A3B8", "Accent": "#3B82F6",
    "BtnIdle": "#2D3748", "BtnHover": "#4A5568", "BtnPressed": "#1A202C",
    "Success": "#22C55E", "Danger": "#EF4444", "Warning": "#F59E0B",
    "OnAccent": "#FFFFFF", "Caret": "#3B82F6", "Selection": "#2A4460",
    "Gutter": "#0B0E11", "Ink": "#E6EDF3", "InkMuted": "#8B98A5",
    "ChromeBg": "#11171C", "Rule": "#2E3A44", "Ok": "#3FB950",
    "Shadow": "#000000", "WallpaperTop": WALL_TOP, "WallpaperBot": WALL_BOT,
}
LIGHT = {
    "Bg": "#F1F5F9", "Surface": "#FFFFFF", "Border": "#CBD5E1",
    "Text": "#0F172A", "Muted": "#64748B", "Accent": "#2563EB",
    "BtnIdle": "#E2E8F0", "BtnHover": "#CBD5E1", "BtnPressed": "#94A3B8",
    "Success": "#16A34A", "Danger": "#DC2626", "Warning": "#D97706",
    "OnAccent": "#FFFFFF", "Caret": "#2563EB", "Selection": "#BFDBFE",
    "Gutter": "#E5E7EB", "Ink": "#0F172A", "InkMuted": "#64748B",
    "ChromeBg": "#E2E8F0", "Rule": "#CBD5E1", "Ok": "#16A34A",
    "Shadow": "#0F172A", "WallpaperTop": "#F1F5F9", "WallpaperBot": "#E2E8F0",
}

# --- geometry + strokes (ui-primitives §2.2–2.5) --------------------------------
PAD_XS, PAD_SM, PAD_MD, PAD_LG = 2, 4, 8, 16
RADIUS_CONTROL, RADIUS_WINDOW = 4, 8     # pills: h/2; clamp to min(w,h)/2
BORDER_W, FOCUS_W = 1, 2                 # focus ring inside the bounds
TITLEBAR_H, ROW_H = 28, 24
GLYPH_EM = 16                            # VirelaiChrome grid; must read at 12
SHADOW_DY, SHADOW_BLUR, SHADOW_ALPHA = 4, 16, 0x40   # floating plates only

# --- master canvas sizes per family (virelai/README.md is the authority) ---------
SIZE = {
    "icon": (64, 64),           # reads at 24 and 16
    "cursor": (32, 48),         # 2x of the shipping 16x24; mono-mask safe
    "mascot": (64, 64),         # reads at 24
    "wallpaper": (2560, 1440),  # center-weighted; chrome eats top ~80 + rails
    "spot": (160, 120),         # reads at 80x60, on dark AND light
    "brand_boot": (800, 450),   # 16:9, letterboxed boot surface
    "brand_emblem": (256, 256), # reads at 64
    "spinner": (32, 32),        # per frame; reads at 16
    "filetype": (32, 32),       # reads at 16-20 in list rows
    "seat": (1280, 720),        # seat-shell + figcraft frames
}
