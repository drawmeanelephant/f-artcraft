## Keel-billed toucan V1R00 — bill as layered color zones

- Kind: analysis
- Source: issue #1126, `work/animals/draw_keel_billed_toucan.py`,
  `work/out/keel-billed-toucan-V1R00@2x.png`
- Applies to: field plates / animals
- Status: pending

### Evidence

Ramphastos sulfuratus perched three-quarter on a mossy diagonal branch,
bill in clean left profile. What worked: the bill reads as one volume but
carries the species' whole color map by layering four shapes on the base
green gradient — an orange culmen sliver hugging the top edge, a red tip
patch, a maroon basal patch, and the pale base line as a 4pt stroke.
Zone edges must be *inside* the bill outline or they bleed the rim of the
shape. The zygodactyl grip reads with 5pt toe strokes arcing over and
behind the branch lip; a white rump patch only reads as plumage when
tucked into the body's rear edge — floating beside the tail it read as an
egg on the branch (fixed). Yellow bib + red under-edge crescent separate
this species from toco at a glance.

### Proposed change

For `prompts/series/20-field-plates.md` animals notes: a big diagnostic
appendage (toucan bill, hornbill casque) wants its field marks as stacked
inset shapes, ordered base→tip, each kept ~2pt inside the parent outline.
