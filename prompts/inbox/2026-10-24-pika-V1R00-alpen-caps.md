# American pika V1R00 — lit summit caps need a shaded face, and round ears need crown overlap

- Kind: lesson
- Source: issue #1105; `work/animals/draw_american_pika.py`,
  `art/animals/american-pika/american-pika-V1R00.{vectorcraft,svg,@2x.png}`
- Applies to: animals field plates; alpenglow/snowcap backgrounds; round-eared subjects
- Status: pending

### Evidence

Proof `work/out/american-pika-V1R00@2x.png`. Findings:

1. Alpenglow caps drawn as uniform pink triangles read as pennants/tents,
   not snow. Two fixes did it: seat each cap wide over the ridge vertex
   (base 60+ pt below the apex, past the saddle) and split a darker lee
   face (~55 opacity, same hue family) off the summit — the light/shade
   pair reads as a lit cap instantly.
2. Round ears drawn as two identical circles sitting on the head's
   outline read as goggles on a stalk. Dropping the ear centers 20 pt
   into the crown so the strokes overlap the head silhouette restores
   the species read — the ears must pierce the outline, not perch on it.
3. Loose angular shards near the plate's lower corners are a silent rim
   leak: at y≈830 the disc is only ±180 wide. Any scatter loop below the
   floor crest wants an `on_disc` assert on the shape's top point, not
   its centre.
4. A mouthful-of-hay prop reads best when the stem fan starts INSIDE the
   mouth line and the nose tip overlaps the bundle's root — stems simply
   ending at the lips read as spray, not a held bundle.

### Proposed change

For `prompts/series/20-field-plates.md` known-traps: *lit summit caps
are a light+lee pair seated over the vertex — a uniform triangle is a
pennant. Round ears overlap the crown line. Assert disc membership on
every scattered shard's extremity, not its centre.*
