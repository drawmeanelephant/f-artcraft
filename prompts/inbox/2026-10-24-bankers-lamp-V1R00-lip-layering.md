## Banker's lamp V1R00 — the mouth is a layer sandwich, and Virelai's apostrophe

- Kind: lesson
- Source: #1174, `work/furniture/draw_bankers_lamp.py`, `art/furniture/bankers-lamp/bankers-lamp-V1R00.{vectorcraft,svg,@2x.png}`
- Applies to: furniture field plates, caption lettering
- Status: pending

### Evidence

The cased-glass mouth only reads lit when its parts are ordered:
mouth band first (below the lip curve, mostly covered by the shell),
shell second, bulbs third *inside* the mouth region, then the front
lip redrawn as a stroke over the bulb tops. Bulbs drawn before the
shell vanish entirely; drawn after without the lip re-stroke they
float over the rim. Also: Virelai Sans's U+2019 apostrophe renders as
a small raised ring that reads as a stray ornament at 56pt — the
caption shipped as `BANKERS LAMP`.

### Proposed change

For `prompts/series/20-field-plates.md` known traps: interior glows
belong *below* the silhouette's bottom edge — draw the shell, the
bulbs, then re-stroke the rim so light sources tuck under it. And
avoid apostrophes in Virelai name lines; prefer the unmarked form.
