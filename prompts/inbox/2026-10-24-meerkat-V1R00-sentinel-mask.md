## Meerkat V1R00 — the mask is the species, the pose is the story

- Kind: analysis
- Source: issue #1040; `work/animals/draw_meerkat.py`, `art/animals/meerkat/meerkat-V1R00.*`
- Applies to: animals field plates; small-mammal portraits
- Status: pending

### Evidence

Proof `work/out/meerkat-V1R00@2x.png`. Sentinel column on hind legs,
forepaws folded, tail trailing as the third leg of the tripod — the pose
carries "on duty" before the face does. What actually makes it a meerkat
and not a generic upright rodent is the eye mask: first pass had two
small dark patches sitting on a big pale face plane and it read
teddy-bear. The fix was inverted emphasis — large teardrop patches
angled brow-to-cheek at opacity 95, pale restricted to a thin brow band
and the muzzle wedge. Small dark ears seated low inside the skull line
stop reading as pom-poms only when ~half buried and well below the crown
(fourth confirmation of the ear-seating rule).

Dawn tell that worked: sun disc ~50pt clear of the floor line with a
per-stop-opacity glow reads as horizon-low; the same disc sitting
*on* the floor read as a ball resting on sand. Long translucent cast
shadow (opacity 25) is cheap and does more for "dawn" than any sky work.

What still grates: the folded forearms render as two dark bars with a
pale stripe between — readable, but the "hands clasped" beat could be
sold harder with a shared shadow under the paws.

### Proposed change

For `prompts/series/20-field-plates.md`: for masked species (meerkat,
raccoon, badger) the mask must *dominate* the face — draw the pale
areas as islands (brow, muzzle) inside the fur, never the face as a
pale field with dark accents. Also note for the trap list: a horizon
object needs clear air between its base and the floor crest line or it
reads as an object on the ground.
