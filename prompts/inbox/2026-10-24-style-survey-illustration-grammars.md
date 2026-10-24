## Style survey — illustration grammars across f-artcraft

- Kind: lesson / analysis
- Source: repo-wide survey of `art/`, `work/`, `test/glm-flash/`, `virelai/`, `docs/`
- Applies to: shared rule (style selection), all series
- Status: pending

### Evidence

A full inventory of the drawing grammars in the repo, each with its own
canvas, grammar, paint rules, type, and reference pieces:

1. **House style — field plates** (`art/animals/`, `art/insects/`, `art/furniture/`, `art/vehicles/`): 1000×1000, disc centre 500,460 r420, gradients + translucent shading, never flat fills, warm dark ink, Virelai Sans, V2 renditions supported.
2. **Spot-flat / GLM-Flash** (`test/glm-flash/`, `art/animals/fennec-fox/V2R00`): flat silhouettes, spot circle hub, minimal face (paper ring + vermilion dot), no gradients/outlines/translucency (deliberate break of house rule #1), 3-colour palette keyed to subject.
3. **Guest styles** (`art/guest/`): whale-flat, whale-sticker, whale-neon, whale-doodle, whale-sunset, whale-pixel, dusk-poster — received with appreciation, not critique.
4. **Orient series** (`art/zodiac/`, `art/holidays/`, `art/indian-symbols/`): plate grammar + vermilion seal chop, element palettes, cultural guardrails (no flags/maps/political symbols, objects not worshippers).
5. **Companion plates** (`art/mascots/`, `art/lorelog/`, `art/poetry/`, `art/site/`): same disc/caption stack, second line is role/epithet not spec.
6. **Named pieces** (`art/pieces/`): one-offs — Fart Knocker portrait (style anchor), crest, bunny set, golly, ember-dusk, empathegy.
7. **VirelaiOS assets** (`art/virelai/`, `virelai/`): chrome register (flat, 1px borders) vs asset register (cel shading, thick outlines); icons, cursors, mascots, wallpapers, spots, filetypes, brand; read-at-size gate at smallest target.

### Proposed change

Add `STYLES.md` at repo root as a consolidated style survey so new artists can
pick a grammar without reverse-engineering existing drivers. Add a
"Illustration styles" section to `README.md` pointing at it. This is a
reference document only — it does not change any house rule or series
grammar.
