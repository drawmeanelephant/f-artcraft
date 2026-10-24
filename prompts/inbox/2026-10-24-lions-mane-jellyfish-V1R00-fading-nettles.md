## Lion's mane jellyfish V1R00 — gradient-faded strokes sell the nettle mass

- Kind: lesson
- Source: issue #1053; `work/animals/draw_lions_mane_jellyfish.py`, `art/animals/lions-mane-jellyfish/lions-mane-jellyfish-V1R00.*`
- Applies to: animals field plates; translucent/deep-sea subjects
- Status: pending

### Evidence

Proof `work/out/lions-mane-jellyfish-V1R00@2x.png`. The "hundred feet of
nettle" is the species tell and it is cheap: ~34 fine cubic strokes plus 5
heavier ropes, every stroke carrying a *linear gradient on the stroke
itself* — opaque at the bell margin, fading to opacity 0 at the tip. The
fade keeps every tentacle inside the disc without clipping, and the mass
reads as countless strands rather than 39 lines. Oral arms are four wavy
ribbon fills with a lighter centre-frill stroke; placed in front of the
nettle curtain they read as the ruffled curtain without any extra work.

Working notes: the bell's scalloped margin is built into the dome path
itself (alternating shallow C-bumps along the bottom edge) — cheaper and
cleaner than a separate scallop band. A dark "abyss band" closing on the
`A420,420` arc at fy≈792 gives the deep somewhere to go; tentacle fades
land inside it. Long names: `LION'S MANE JELLYFISH` fits at 46pt —
the ~56-60pt convention only survives to about 14 characters.

### Proposed change

For `prompts/series/20-field-plates.md`: strokes accept gradients —
per-stop opacity on a linear stroke gradient is the way to fade trailing
geometry (tentacles, whiskers, roots) before it reaches the rim instead
of cutting it. Also worth stating the name-size ceiling: >14 glyphs wants
~40-48pt, not 60.
