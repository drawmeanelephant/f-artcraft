## Victoria crowned pigeon V1R00 — lace crown as shaft + spatulate flag

- Kind: analysis
- Source: issue #1127, `work/animals/draw_victoria_crowned_pigeon.py`,
  `work/out/victoria-crowned-pigeon-V1R00@2x.png`
- Applies to: field plates / animals
- Status: pending

### Evidence

Goura victoria standing ceremony-upright on the litter chord, maroon
breast shield over the slate body, crest fanned in a 10-shaft arc. What
worked: each crest feather is a 4pt curved shaft plus a separate
spatulate flag placed at the tip along the shaft's own normal — the fan
stays even because the tips ride the same radius formula. First pass had
narrow 9pt flags that read as berries; widening the flag perpendicular
to ~13pt while keeping it short is what makes it lace. Long-name fit:
`VICTORIA CROWNED PIGEON` at the stock 58pt would run ~1000pt and break
the canvas bound; at 46pt with tracking 60 it lands at 797pt, clears the
rim, and still reads as the plate's name line.

### Proposed change

For `prompts/series/20-field-plates.md`: give the name line a fit rule —
scale down from 58pt toward ~44pt (tracking ~60) for names over ~20
chars rather than shortening the name. Crest/plume fans want tip flags
drawn perpendicular to each shaft, wider than long.
