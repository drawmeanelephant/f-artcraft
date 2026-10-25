## Labrador retriever V1R00 — the muzzle must be part of the head silhouette

- Kind: analysis
- Source: issue #1500; `work/dog-breeds/draw_labrador_retriever.py`,
  `art/dog-breeds/labrador-retriever/labrador-retriever-V1R00.{vectorcraft,svg}`,
  proof `work/out/labrador-retriever-V1R00@2x.png` (`check_rim.py`: clean)
- Applies to: dog-breeds milestone cards; any bust/portrait head
- Status: pending

### Evidence

Three loops. Draft 1 built the lifted muzzle as a separate blob offset
left of the skull — same coat colour but disconnected from the brow
line — and it read as a flipper or a raised wing, with the skull behind
it a featureless ball on a stacked neck (the snowman problem). Draft 2
drew the head as ONE silhouette — nose tip → muzzle top → brow → crown →
far cheek → jaw → under-muzzle back to the nose — and the lab arrived at
once. The stop, flew and mouth are just strokes inside that silhouette.

Also removed: a low-opacity arc under the jaw meant as a dewlap that
read as a second smile mid-neck — any horizontal curve on the neck of a
bust reads as a mouth; keep the neck's only cross-lines as sheen strokes
at ≤25% opacity or nothing.

What works in the shipped card: lifted nose-up muzzle marking the fall,
kind level-lidded amber eyes with pupils nudged up-left, both drop ears,
otter tail curling up behind the right shoulder, reed strokes + water
band + mist for the marsh, black coat carried by sheen gradients and
strokes rather than flat black. Portrait bust sides land inside the rim
and the bottom tucks under it — no leaks.

### Proposed change

Fold into the milestone-cards grammar at consolidation: *in a bust or
portrait, skull+muzzle is one closed silhouette — never a muzzle blob
beside a head blob — and the neck carries no horizontal arcs near the
chin, they all read as a second mouth.*
