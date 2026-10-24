## brand plates V1R00 — a shared sexiburger module beats twin draws

- Kind: lesson
- Source: #1254 · `work/virelai/sexiburger.py` ·
  `work/virelai/draw_brand_boot_plate.py` ·
  `work/virelai/draw_brand_about_emblem.py` ·
  `art/virelai/brand-{boot-plate,about-emblem}/…-V1R00.*`
- Applies to: virelai mascot work (#1250 poses, spots, wallpapers)
- Status: pending

### Evidence

Both brand pieces draw the sexiburger from one parametric builder
(`sexiburger.mascot(d, cx, top, h, arms=…, detail=…)`, 160×230 unit frame):
bun dome + seeds, lettuce/tomato/cheese/patty bands, bun-colored body,
tapered quad limbs, cartoon eyes, polka-dot bow tie, white gloves.
Palette is vkit's sampled values; outlines INK at ~4u.

What worked: the fixture doesn't show a face — the alive presentation
(eyes, gloves, bow tie) comes from WALLPAPER.QOI, which is the right
source for a *welcoming* brand moment. Arms-up presents the wordmark on
the boot plate; arms-out fits the roundel's width on the emblem. The
emblem's wordmark had to grow to 24 px and its rings strengthen (Border
4 px + cream inner ring) before the 64 px gate passed on dark chrome —
the navy field otherwise merges into `#11171C`.

Gotchas confirmed: `backgroundContents: "transparent"` on `file.new`
yields a real RGBA export (the emblem is a roundel, must sit on both
surfaces); `text.setStyle tracking` works; `draw_shape` has no rounded
rect (paths); `line` takes `cap`.

### Proposed change

Keep `sexiburger.py` as the single source for the character — #1250's six
poses should extend it (pose rig, not redraws) so the mascot can't drift
between pieces. Candidate rule for `virelai/notes/style-bible.md`: *brand
emblems on navy must prove the ring on `#11171C` chrome — navy-on-chrome
needs the Border ring plus a light inner rim to read at 64 px.*
