## Friesian V1R00 — the mane lives on the crest, not under the jaw

- Kind: analysis
- Source: issue #1520; `work/horse-breeds/draw_friesian.py`,
  `art/horse-breeds/friesian/friesian-V1R00.{vectorcraft,svg}`,
  proof `work/out/friesian-V1R00@2x.png`
- Applies to: horse-breeds milestone cards; any crested-maned subject
- Status: pending

### Evidence

Two render-and-critique loops before shipping. All-black baroque horse
on a moonlit slate disc — coat is a warm-dark ramp plus two cold sheens,
the silhouette does the work as the brief demands.

What worked:

- High-stepping read needs the carpus lifted to near-horizontal:
  `leg((430,546),(514,540),(486,608))` puts the fold at chest height
  with the cannon hanging folded — first draft kept the carpus low and
  read as standing. Pair it with the opposite hind lifted under the
  belly for the diagonal-pair trot.
- Fetlock feathers as small wavy hoods over each hoof read correctly
  at plate scale in near-black.
- Tail as a single heavy sweep reaching toward the floor, curling at
  the tip — extravagant without strokes.

What failed and got fixed:

- Mane drawn hanging below the throat line reads as a BEARD. The fall
  must sit on the crest: top edge IS the neck's top silhouette, hem
  kept ~30pt inside the throat edge. Even then its leading edge can
  swallow the eye — keep the face clear to the left of the mane's
  bottom-left corner.
- A pale "sheen" patch on the quarter read as a grey sticker on a
  black horse; on near-black coats keep sheens to thin strokes along
  silhouette edges (topline, crest), never interior patches.
- Draw far legs BEFORE the body so their roots tuck under the barrel —
  drawn after, the tops print over the flank.

### Proposed change

Fold into the horse-breeds card note: mane hem inside the throat edge;
high-step = horizontal forearm; sheens stay on the silhouette edge.
Destination `prompts/series/` at consolidation.
