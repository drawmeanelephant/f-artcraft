## Porcupinefish V1R00 — front-on is the pose when the animal is a ball

- Kind: analysis
- Source: issue #1050; `work/animals/draw_porcupinefish.py`, `art/animals/porcupinefish/porcupinefish-V1R00.*`
- Applies to: animals field plates; radial subjects; face placement
- Status: pending

### Evidence

Proof `work/out/porcupinefish-V1R00@2x.png`. A puffed porcupinefish has no
profile worth drawing — the inflated ball IS the animal — so the plate goes
three-quarter face-on: two huge eyes, a pursed beak, spines radiating on
every bearing. It reads instantly and is the cutest plate in the series
without breaking the house mood. The pale belly band low across the ball
doubles as a smile; that accident is worth keeping on purpose.

Working notes: spines are tapered triangle paths placed by polar sweep —
base point at `r·(cos a, sin a·0.96)`, tip at the next radius out, half-width
perpendicular. The 0.96 elliptical squash keeps the ring following the
ball's edge instead of floating rounder than the body. Spine-root dots at
each base seat them into the skin. Sparse the face sector (a real Diodon's
muzzle is bare); two stray long spines at 70°/85° keep the silhouette
honest. Watch prop placement: the bubble trail's first draft landed inside
the ball silhouette — particles must be checked against the SUBJECT's
footprint too, not only `on_disc`.

### Proposed change

For `prompts/series/20-field-plates.md`: radial/ball subjects (puffers,
pincushion urchins, hedgehogs balled) should go near-frontal — the eyes
carry the fish-ness that the silhouette has lost. And a sanity rule worth
formalising: decor passes assert `on_disc`; props near the subject should
also clear the subject's own bounds or read as stuck ON it.
