## Atlantic puffin V1R00 — held objects must tuck under the holder's silhouette

- Kind: analysis
- Source: issue #1046; `work/animals/draw_atlantic_puffin.py`,
  `art/animals/atlantic-puffin/atlantic-puffin-V1R00.*`
- Applies to: animal field plates with props (prey, nesting material, tools)
- Status: pending

### Evidence

First pass had two prop failures visible on the proof. The sand eels were
drawn after the bill and started below its edge: they read as noodles
hanging from thin air. Moving them earlier in the stack — heads inside the
bill silhouette, bodies and forked tails emerging under the gape — sold the
"bill full of silver" immediately. The feet sat at the body's bottom edge
and were swallowed by it; dropping them ~15pt lower let both orange webs
read as planted. Small scallop marks on the breast's black-white seam read
as stray punctuation, not feathering — replaced by one soft seam stroke.
Floor/ledge closes on the `A420,420` arc; sea band uses the same
arc-closure trick from its own horizon chord. Name fits.

### Proposed change

When a subject holds something, draw the held object's hidden end *before*
the holder's shape so it emerges from inside the silhouette; a prop drawn
after the holder always reads as pasted on. Feet and other edge-contact
parts need a visible span below the body's lowest curve, not a flush join.
