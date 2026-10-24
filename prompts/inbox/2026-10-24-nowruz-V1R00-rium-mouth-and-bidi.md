## nowruz-V1R00 — bowl-mouth placement and mixed-script captions

- Kind: lesson
- Source: issue #983; `work/holidays/draw_nowruz.py`;
  `art/holidays/nowruz/nowruz-V1R00.{vectorcraft,svg}`; proof
  `work/out/nowruz-V1R00@2x.png`
- Applies to: holidays / Festival Seals (and any plate with script mixing)
- Status: pending

### Evidence

First pass drew the fishbowl's mouth ellipse 16px above the sphere's top
edge; the render showed a floating halo ring over the glass. Moving the
mouth down so it overlaps the sphere outline (rim centre ≈ sphere top + 7)
turned it into a readable opening; the water surface sits 30px below it.

Sabzeh needs ~38 blades at strokeWidth 4–6 to read as sprouted wheatgrass —
26 sparser blades read as separate straws. Hyacinth florets must stay in a
cone (max spread ~30) or they drift into a lavender bouquet.

The second caption line mixes `نوروز` with Latin in one `add_text` call:
the renderer lays out bidi correctly and moves the RTL run to the visual
right — "PERSIAN NEW YEAR · MAR 20 · نوروز" reads naturally. Bidi text is
outlined to paths in SVG export (harmless for a print proof). Digits in the
date came from Source Sans 3 (Virelai Sans still substitutes wrong glyphs).

### Proposed change

For plate captions: a non-Latin script run may share the second line with
Latin + digits if the base font covers digits (Source Sans 3) and the
native run is placed at the logical start so it lands at the visual right.
Candidate for `prompts/series/` holiday grammar notes at consolidation.
