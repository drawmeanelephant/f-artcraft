## Thylacine V1R00 — the tail carries the species; sepia is a mood not a palette swap

- Kind: analysis
- Source: issue #1055; `work/animals/draw_thylacine.py`, `art/animals/thylacine/thylacine-V1R00.*`
- Applies to: animals field plates; extinct subjects; sepia/photo idiom
- Status: pending

### Evidence

Proof `work/out/thylacine-V1R00@2x.png`. The thylacine read depends on two
moves: the tail is a straight stiff taper continuing the backline
(kangaroo-rigid, never the loose curve of a dog), and the rump bars are
slanted wedge fills hugging the topline — ~13 of them, longest at the hip,
shortest forward, plus two stragglers onto the tail root. Big rounded
ears and a long narrow muzzle finish the tell. For "last frame 1936" the
sepia plate does more than tint: a radial vignette (per-stop opacity, 0 at
0.62 → 55 at the edge), seeded grain flecks, two near-invisible film
scratches, and — the cheap storyteller — two fence posts with a sagging
wire behind the animal at opacity ~35. Enclosure, not wilderness.

Working notes: all props must clear the rim math — the scratch endpoints
and post bases were placed by `on_disc`/rim_x before drawing. Reused the
smilodon `limb()`/head-blob structure with no changes needed; the neck
mass seam patch is becoming boilerplate.

### Proposed change

For `prompts/series/20-field-plates.md`: extinct-subject plates want one
period prop (fence wire, glass, frame edge) at low opacity rather than a
museum label — the ghost-story mood lives in artifacts, not captions.
And a mechanical note: `limb()` + `paw()` have now served two plates;
promote them into `work/vc.py` on the next quadruped.
