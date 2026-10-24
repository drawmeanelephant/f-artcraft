## Peregrine falcon V1R00 — scenery at the rim closes on the disc arc too

- Kind: analysis
- Source: issue #1047; `work/animals/draw_peregrine_falcon.py`,
  `art/animals/peregrine-falcon/peregrine-falcon-V1R00.*`
- Applies to: field plates with rim-touching scenery (cliffs, trunks, banks)
- Status: pending

### Evidence

The stoop pose itself shipped on the first pass — the teardrop body, swept
wings, closed tail, hood/malar/cheek read at plate scale. The scenery needed
two rounds. A free-standing "crag" inside the disc read as a surfboard in
both a rounded and an angular variant: an isolated upright slab has no
referent. The fix was treating the cliff like the floor: a wall whose outer
edge IS the disc's own rim arc (`A420,420 0 0 0` between two chord points on
the right side — note the sweep flag flips vs the floor's `0 0 1` because
the traversal runs bottom-to-top on the right). With the rim as its right
edge, the jagged left boundary, strata and crack finally read as rock.
Also: bird at ~330pt span looked lost in the 840pt disc; scaling the whole
bird block 1.28x about a pivot fixed the plate's figure-ground balance.

### Proposed change

Scenery touching the rim should close on the disc arc from whichever chord
points it occupies — `0 0 1` swept along the rim direction of travel, not
always the floor's flag. A free-standing vertical landmark inside the disc
keeps reading as a monument; attach it to the rim or leave it out.
