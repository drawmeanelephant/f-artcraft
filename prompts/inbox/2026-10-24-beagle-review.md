## Beagle V1R00 — a saddle marking must own the silhouette edge

- Kind: analysis
- Source: issue #1506; `work/dog-breeds/draw_beagle.py`,
  `art/dog-breeds/beagle/beagle-V1R00.{vectorcraft,svg}`,
  proof `work/out/beagle-V1R00@2x.png`
- Applies to: dog-breeds milestone series; any blanket/saddle marking
- Status: pending

### Evidence

Three render loops. The tricolor saddle defeated the "markings are
overlay shapes" rule as literally stated: a black blob drawn INSIDE the
tan body read as a bathtub/inlay no matter the edge treatment — a thin
tan sliver always survives between the blob and the body's ink topline.
The fix is inverted layering: draw the BODY in the saddle black, then
overlay the TAN underside/chest as one shape with a wavy top edge at
mid-ribs, held a few px inside the silhouette. The black then genuinely
is the topline and the marking reads as coat, not a vessel.

Other findings: (1) a drop ear on a lowered head must attach INSIDE the
combined head+neck silhouette — letting its top poke past the outline
reads as a horn, not a swung ear; (2) scent ticks near the nose sit at
the disc's lower-left where the rim curves away hard — two of mine
crossed r430 and tripped check_rim; keep gesture ticks at the nose
≤30px long there; (3) nose-to-ground pose wants the neck drawn as a
down-sloping wedge and the eye low on the skull — the head reads
"found the trail" when the nose nearly touches the floor crest.

### Proposed change

Milestone-cards note candidate: "blanket markings are drawn as the base
fill of the body silhouette; the base coat is the overlay." Generalizes
to dalmatian-adjacent patched breeds.
