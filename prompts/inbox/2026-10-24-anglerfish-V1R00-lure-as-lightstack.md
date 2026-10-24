## Anglerfish V1R00 — the lantern is a layer stack under the fish, plus rim strokes on it

- Kind: lesson
- Source: issue #1083; `work/animals/draw_anglerfish.py`, `art/animals/anglerfish/anglerfish-V1R00.*`
- Applies to: animals field plates; abyss/bioluminescent scenes; any plate with a single in-frame light source
- Status: pending

### Evidence

Proof `work/out/anglerfish-V1R00@2x.png`. The esca reads as the only light
in the water because it is drawn as two systems: (1) four concentric
ellipses (r 150/100/58/34, op 6/10/15/22, #9FE8C4) laid UNDER the body so
the halo bleeds past the silhouette without whitening the fish, and
(2) rim-light strokes catching the edges the light would actually hit —
snout crown (#8FE0BC op 28), lip edge (op 35), throat (op 25). A glow that
only surrounds its bulb reads as a sticker; the same halo + edge response
reads as illumination.

Fangs are filled pointed paths (#DCE6DA, op 80–88), never strokes — a
4–5pt tooth stroke dies at plate scale, but a 7–12pt-wide triangle reads
at @2x. Mouth interior is a separate dark-wine radial laid inside the
gape, not an absence of fill, so the jaw edges keep their gradient.

Working notes: the open mouth is part of the body silhouette itself —
outline runs snout tip -> mouth floor -> jaw hinge -> jaw tip -> chin,
no separate mouth shape needed. Keep the esca out over open water (left
of the snout) so the halos show against plate darkness, not body.

### Proposed change

For `prompts/series/20-field-plates.md`: in-frame light sources ship as a
stack — halo veils under the subject + per-edge rim strokes at op 25–35
keyed to the light's side — never a glow object alone. Teeth/claws/spines
under ~15pt: fill a pointed path; do not stroke them.
