# Illustration styles — f-artcraft

A survey of every drawing grammar in the repo, what makes each one distinct,
and where it lives. Use this to pick a style for a new piece, or to decide
whether a new idiom deserves its own series.

---

## 1. House style — field plates

**Where:** `art/animals/`, `art/insects/`, `art/furniture/`, `art/vehicles/`
**Canvas:** 1000×1000
**Grammar:** dark moody backdrop → one large gradient plate disc (centre 500,460, r≈420) → the subject → name in Virelai Sans (~56–60pt) near the bottom → a second tracked line under it (~22–24pt) stating order/material/spec
**Paint:** gradients and translucent shading, never flat fills; warm dark ink, never pure black
**Type:** Virelai Sans for names and captions; Virelai Mascots glyphs (U+E002–E00A) as ornaments
**Rules:** ≥3pt for thin geometry (antennae, legs, spindles, spokes, rigging); subject inside the rim; name block clear of the disc arc; check proof edges before done
**Driver pattern:** `work/<series>/draw_<slug>.py` using `work/vc.py`
**Revisions:** `<slug>-V<V>R<RR>`; V2 renditions read the same subject in a new take (bump V, reset R)

**Reference pieces:** `axolotl-V1R00` (front portrait), `axolotl-V2R00` (full body, cold tank), `fennec-fox-V1R00` (base plate)

---

## 2. Spot-flat (GLM-Flash idiom)

**Where:** `test/glm-flash/` (experiment), `art/animals/fennec-fox/` (V2R00 adoption)
**Canvas:** 1000×1000
**Grammar:** one spot circle as the compositional hub → flat silhouettes → minimal face (paper ring + vermilion dot) → thin-line dressing (bubbles, dashes, whisker ticks)
**Paint:** flat fills only — **no gradients, no outlines, no translucent shading** (a deliberate break of house rule #1, that is the point of the style)
**Palette:** three colours max, keyed to the subject (paper + body + accent)
**Type:** Virelai Sans name line, mirrored position (centred at the bottom)
**Lesson from the pilot:** in flat abstraction the silhouette code carries the species — decoration is cheap, the outline is the work. Subjects with constructible geometry (octopus spirals, snail shells, fluke-on-a-stem whales) are where this style is strongest.

**Reference pieces:** `spot-whale-V1R00…V1R03` (revision trail, fish→whale anatomy fix), `fennec-fox-V2R00` (spot-flat rendition of a plate subject), `study-harper-octopus-V1R01` (strongest of the three octopus studies)

---

## 3. Guest styles

**Where:** `art/guest/`
**Source:** Freebuff — six whale renderings for DeepSeek + a dusk poster, drawn headless through VectorCraft's MCP
**Styles:**
| File | What it is |
|---|---|
| `whale-flat.svg` | flat mascot: halo, sparkles, bubbles, soft ground shadow |
| `whale-sticker.svg` | 20px white outline, drop shadow, peach starburst, wordmark |
| `whale-neon.svg` | stroke-only whale, two stacked outer glows, teal spout, grid |
| `whale-doodle.svg` | 13px navy outline, pastel fills, confetti, "hello, ocean" |
| `whale-sunset.svg` | same path rotated −8°, scaled 0.62, over a gradient sky and glowing sun |
| `whale-pixel.svg` | 68 rectangles from a 40×40 grid sampled off a clean render |
| `dusk-poster.svg` | 1080×1350: gradient sky, glowing sun, three ridges with rim light, pines, live type |

**Note:** Guest work is received with appreciation, not critique — no red pen. The whale is one shape (seven cubic body segments, two-lobed fluke, belly derived by sampling and insetting 26px); each style recomposes that geometry.

**Driver:** `work/guest/guest-vcmcp.mjs` (raw JSON-RPC client), `guest-whale-styles.py`, `guest-whale-pixel.py`, `guest-dusk-poster.py`

---

## 4. Orient series — zodiac, holidays, indian-symbols

**Where:** `art/zodiac/`, `art/holidays/`, `art/indian-symbols/`
**Canvas:** 1000×1000, same plate grammar as field plates (disc centre 500,460 r420, name baseline 934, second line 970)
**Dressings:** small vermilion seal chop at top right, outside the disc (deliberate exception to the rim rule); element palettes (Wood green, Fire red, Earth ochre, Metal silver, Water blue); ring of twelve earthly branches inside the rim
**Shared rules:** warm ink, gradients + translucent shading; objects and settings, not worshippers; no national flags, maps or political symbols; traditional characters for zodiac seals
**Drivers:** `work/orient/plate.py` (canvas grammar, motifs, caption/chop), `work/orient/zodiac.py` (element palettes, branch ring, beast parts), `work/holidays/cn_kit.py`, `work/holidays/festival_kit.py`

---

## 5. Companion plates

**Where:** `art/mascots/`, `art/lorelog/`, `art/poetry/`, `art/site/`
**Canvas:** 1000×1000, same disc and caption stack (name ~54–58pt at y≈930, second tracked line at y≈968)
**Second line:** role or epithet (not a spec) — mascot's office, protocol/form name, catalogue number, or what the piece is for
**Mas:** portrait plates for the numbered cast (`<number>.<name>`, e.g. `418.teapotta-protocol`)
**Lorelog:** one plate per incident log entry (`llg-<NNNN>-<slug>`)
**Poetry:** verse plates — stanzas around a vignette or dressed as wanted posters (`hai-` haiku, `lim-` limerick)
**Site:** the marks the gallery runs on — brand mark, collection map, search icon, ornament

---

## 6. Named pieces

**Where:** `art/pieces/`
**Contents:** Fart Knocker self-portrait, fart-knocker-crest, bunny-avatar, bunny-banner, golly, ember-dusk, empathegy-brochure
**Note:** These are one-off works, not series plates. The fart-knocker portrait is the house style anchor (monocle-and-glint, heavy shading).

---

## 7. VirelaiOS assets

**Where:** `art/virelai/`, `virelai/` (design sheets), `work/virelai/`
**Two visual registers:**
- **Chrome register** — OS widgets: flat face + 1px Border, no gradients on control faces, geometric filled silhouettes on a 16px em, rounded terminals, readable at 12px (PUA U+E000–U+E01D)
- **Asset register** — our art: cel shading, thick warm-dark outlines, the mascot's world

**Families:**
| Prefix | Master size | Must also read at | Count |
|---|---|---|---|
| `icon-` | 64×64 | 24, 16 | 31 app icons |
| `cursor-` | 32×48 | 16×24 mono mask | cursors (record hotspot) |
| `mascot-` | 64×64 | 24 | 6 poses, same character |
| `wallpaper-` | 2560×1440 | — | centre-weighted, clear of seat chrome |
| `spot-` | 160×120 | 80×60 | reads on dark AND light |
| `brand-` | 800×450 / 256×256 | 64 (emblem) | boot plate + about emblem |
| `filetype-` | 32×32 | 16–20 | flatter than icons, one accent hue |
| `sheet-` | review aid | — | contact sheets as their own piece |

**Rules:** transparent backgrounds for anything painting on chrome; read-at-size gate at the smallest target; digits in Source Sans 3 (Virelai Sans has no digits); `add_text` takes no opacity/style kwargs; every task lands one `prompts/inbox/` note

**Reference:** `virelai/README.md` (conventions), `virelai/notes/style-bible.md` (taste rules, palette tokens from VirelaiOS `theme.go`)

---

## 8. Aphorisms, haikus, limericks, commemoratives, necropolis

**Where:** `art/aphorisms/`, `art/haikus/`, `art/limericks/`, `art/commemoratives/`, `art/necropolis/`
**Note:** Inspect current drivers and proofs for each folder's specific vocabulary. Do not invent archive facts to fill gaps.

---

## Choosing a style

| If you want… | Use |
|---|---|
| A specimen plate (animal, insect, furniture, vehicle) | House field plate |
| A second take on an existing plate subject | V2 rendition (house grammar) or spot-flat rendition (breaks rule #1 deliberately) |
| Something flat, geometric, mid-century | Spot-flat (GLM-Flash) |
| A scene/vignette in the bureaucratic spirit | Bureau scene (landscape 1500×1000, no mandatory disc) |
| OS interface art (icons, cursors, etc.) | VirelaiOS asset register |
| A holiday or zodiac emblem | Orient series |
| A mascot portrait or incident log plate | Companion plates |
| Guest or outside work | `art/guest/` (appreciation, not critique) |

**Cross-cutting house rules (apply everywhere unless a style deliberately opts out):**
- Gradients and translucent shading, never flat fills — except spot-flat, which opts out by design
- Check the proof render before calling it finished: arcs in frame, no leaked shapes past badges/rims, no overset, nothing clipped at canvas edges
- Lettering in Virelai Sans; ornaments from Virelai Mascots glyphs
- Never overwrite a piece: revisions are `<slug>-V<V>R<RR>`
