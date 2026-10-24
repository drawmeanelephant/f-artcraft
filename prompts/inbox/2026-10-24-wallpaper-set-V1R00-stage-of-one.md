## wallpaper set V1R00 — one actor per stage, props carry the mood

- Kind: lesson / analysis
- Source: issue #1251 · `work/virelai/draw_wallpaper_{guillotine,night-watch,workshop,quiet-field}.py` · `art/virelai/wallpaper-{guillotine,night-watch,workshop,quiet-field}/…-V1R00.*` (proofs in `work/out/`)
- Applies to: virelai `wallpaper-` family, any future large-canvas scene work
- Status: pending

### Evidence

Four 2560×1440 masters, all stage-with-one-actor:

- `wallpaper-guillotine` re-renders WALLPAPER.QOI's joke: flat `#1E1E2E`
  field + radial stage glow, wood-gradient posts (#A5733F→#5A371C),
  trapezoid steel blade with a bevel-glint line, rope over a crossbar
  pulley tied off on the right post, lunette board hinged open on the left
  post, mascot waving (`POSES["wave"]`, h=330) on the platform. The lunette
  board is the detail that sells "guillotine" over "frame"; keep it.
- `wallpaper-night-watch` puts him on a crenellated parapet (STONE
  #4A5468→#232A38, dark enough to sit in the navy family) reaching toward
  the vigil candle — the #595 flame recipe (`#FFD98A→#D95E14` radial,
  `#FFF6D2→#FFC65E` core) scaled up, plus ember motes. A translucent
  "candle kiss" glaze over his right side warms the rim cheaply.
- `wallpaper-workshop` is the busiest: bench, bent-arm lamp (the light
  source is *inside* the scene, pool centered on it), gear train, wind-up
  bot cameo, pinned blueprint, pegboard tools. Held prop trick that works:
  a scaled `gear()` dropped at the glove tip reads as held, no rig change.
- `wallpaper-quiet-field` is three `ridge()` sine-bump silhouettes + a 150px
  cameo (`eyes="happy"`, `detail=False`, `arms="down"`). At mascot ≤160 px
  pass `detail=False` — half the seeds drop, the dome stays clean.

Survives its own critique: all four keep the subject inside
x≈800–1900/y≈250–1200, clear of seat chrome; mood sits behind windows.
The screwdriver needed a real handle silhouette (first pass read as a
down-arrow); pegboard props want object silhouettes, not symbols.

Adoption-side 8.3 names (OS build renames to QOI): `WALLGUIL.QOI`,
`WALLWTCH.QOI`, `WALLSHOP.QOI`, `WALLCALM.QOI`.

### Proposed change

Candidate rule for `virelai/notes/style-bible.md`: *wallpapers light their
own stage — pick one in-scene light source (blade glint excluded: moonlight
glow, candle pool, bench lamp, horizon) and center the subject inside its
falloff; a second source flattens the mood.* Destination: the bible's
motif-rules section.
