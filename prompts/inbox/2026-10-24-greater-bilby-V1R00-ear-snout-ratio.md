# Greater bilby V1R00 — ears alone make a rabbit; the snout must counter it

- Kind: lesson
- Source: issue #1071; `work/animals/draw_greater_bilby.py`,
  `art/animals/greater-bilby/greater-bilby-V1R00.{vectorcraft,svg,@2x.png}`
- Applies to: animals field plates; big-eared small mammals (bilby, jerboa,
  fennec, bat-eared fox)
- Status: pending

### Evidence

Proof `work/out/greater-bilby-V1R00@2x.png`. First pass gave huge erect
ears on a hunched body and the plate read RABBIT instantly — ears that
large are not neutral, they actively claim the species. The fix was not
smaller ears (they are the bilby's signature) but a longer, lower,
pointed possum snout protruding ~25pt further with a visible mouth line;
the ears stopped reading as rabbit once the face said possum. Second
note: a sitting-on-haunches silhouette wants a big hind foot stretched
forward on the ground — without it the body is a featureless egg and
the haunch geometry can't be inferred.

### Proposed change

For `prompts/series/20-field-plates.md` known-traps: *when one feature
is disproportionately huge (bilby ears, elephant ears), the silhouette
code must come from a second feature — pair the signature with its
counterweight (snout, trunk, crest) or the huge feature hijacks the
species read.*
