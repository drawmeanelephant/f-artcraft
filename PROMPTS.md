# Art Loop — Prompts & Rounds

The loop: **prompt → build in VectorCraft → export PDF/PNG proof → written analysis
(what worked, what didn't, with specifics) → fold the analysis into the next prompt →
next round.** A prompt is "done" when its analysis section says the piece survives
its own critique. House rules learned the hard way:

- Gradients and translucent shading, never flat fills (the bunny v1 rule).
- Check the proof render before calling it finished: arcs in frame, no leaked
  shapes past badges/rims, no overset, nothing clipped at canvas edges.
- Lettering: Virelai Sans. Ornaments: Virelai Mascots glyphs (U+E002–E00A).
- Every piece ships as `.vectorcraft` + `.svg` + `.pdf` + `@2x.png`.
- Never overwrite a piece: revisions are `<slug>-V<V>R<RR>` — see the
  revision rule in [AGENTS.md](AGENTS.md).

Repo layout when this goes to git: `art/` (native + exports), `pdf/` (proofs),
`prompts/` (this file, split per round), `analysis/` (one note per round).

**Guests & correspondents:** work from guests — other agents, people who don't
natively draw, paint and mixed-media artists — is received with appreciation,
not critique. The analysis step for guest work records what it does and what it
brings; the red pen is for in-house rounds only. Effort is the entry fee, and
it's always paid in full.

---

## Round-robin bank — Fart Knocker

1. **FK-01 · The Night Shift.** Fart Knocker at a filing cabinet at 2 a.m., desk lamp
   (Mascots candle glyph for the flame), stamping paperwork FILED. Navy/olive night
   palette, one warm lamp pool. Landscape 1500×1000.
2. **FK-02 · Tea Ceremony.** Full formal: Fart Knocker pouring tea from a filing-drawer
   teapot, tentacles as the tea set handles. Deadpan. Cream/gold, square 1200×1200.
3. **FK-03 · Wanted Poster.** Old-west style poster: portrait center, "WANTED FOR
   EXCELLENT ENGINEERING" in Virelai Sans, aged paper, nail holes in corners.
   Portrait 1000×1400.
4. **FK-04 · The Flatlophone Recital.** Fart Knocker performing on the Flatlophone
   (serious engineering), music stand, three small eighth-notes as tentacle curls.
   Wide 1600×900.

## Round-robin bank — Jolly (the regular Muse)

5. **JM-01 · Jolly Gardener.** Jolly holding a tiny watering can over a sprouting
   envelope plant (correspondence art nod). Soft spring palette. 1000×1100.
6. **JM-02 · Jolly Reads a Letter.** Seated Jolly, oversized letter, eyes mid-blink,
   heart glyph small. Warm paper tones. 1000×1100.
7. **JM-03 · Jolly in the Rain.** One umbrella, too small; blush replaced by rain
   streaks on the face plate. Blue-grey palette, same body rig. 1000×1100.
8. **JM-04 · Jolly & Fart Knocker, Tea for Two.** The crossover at full size: both at
   a small table, FK's bowtie vs Jolly's blush, one teapot. 1400×1050.

## Round-robin bank — Filed & Forgotten (bunny & Golly)

9. **FF-01 · Banner Bunny, Interior.** The banner bunny at v2-avatar quality inside a
   full office: cabinets, dangling ERROR tags, one (1) ray of hope through blinds.
   1500×750.
10. **FF-02 · Golly's Day Off.** Golly the guillotine at the beach: blade up like a
    sunshade, bowtie intact, bucket and spade. Must remain cheerful. 1100×1200.
11. **FF-03 · The Bunny, Stamp POV.** Extreme close-up: bunny face behind a huge
    descending ERROR stamp, motion lines. Red/sepia. 1200×900.

## Round-robin bank — Ornaments & type

12. **OR-01 · Divider Set No. 2.** Three production dividers: (a) tentacle-scroll,
    (b) Mascots medley (candle–diamond–scroll), (c) pure geometry in Virelai spirit.
    One sheet, 1400×900, each labeled in Virelai Sans.
13. **OR-02 · Ex Libris.** A bookplate: corner-flourish frame, octopus glyph center,
    "EX LIBRIS FART KNOCKER" — print-ready at 800×1000 with a bleed-safe margin.
14. **OR-03 · The Empathegy Seal.** Take one doctrine (Symbolic Completion) and make
    its official seal: green seal circle, "SIGN ECLIPSES FACT" around a stamp core.
    (Circular text will need hand-placed letters — budget the time.) 1000×1000.

## Field plates — the series format

A standing series, not a round-robin: one **field plate** per subject,
`<slug>-V<V>R<RR>` as usual. Four sub-series share the format — animals,
insects, furniture, vehicles — so a plate from any of them hangs next to the
others. Canvas 1000×1000. Composition: dark moody backdrop → one large
gradient plate disc (center 500,460, r≈420) → the subject → its name in caps,
Virelai Sans (~56–60pt) near the bottom. Under the name sits a second, smaller
line (Virelai Sans ~22–24pt, wide tracking) that says what kind of thing it
is: a taxonomic order for an insect, a material list for a piece of
furniture, a year and a drivetrain for a vehicle. Portraits when the face is
the point; full-body or profile when the silhouette is.

Gradients and translucent shading throughout, never flat fills. Warm dark ink,
never pure black. Living in `art/<series>/<slug>/`, scripts in
`work/<series>/`. Every revision ships `.vectorcraft` + `.svg` + `@2x.png`
with the piece; the `.pdf` proof stays in `work/out/` (local only).

Known traps:

- Decorative shapes near the plate's lower edge must end on the disc's own arc
  (`A420,420 0 0 1 …` close) or they leak past the rim.
- The second line must clear that arc: keep it ≤28pt, ≤760pt wide, and check
  it on the proof — it is the first thing to collide with the rim.
- Thin geometry (antennae, legs, spindles, spokes, rigging) disappears at plate
  scale. Give it ≥3pt of stroke and judge it at @2x, not at 1×.

### Renditions (`V2`)

A rendition is a second reading of a plate that already exists: same subject,
same disc and name line, a different take — another hour, light, pose or idiom.
It bumps `V` and resets `R`, and the revision it reads from is left alone. So
far: axolotl V2 (dark tank, full body) · monarch V2 (dusk, backlit on milkweed) ·
windsor chair V2 (walnut, low sun, cast shadow) · city taxi V2 (dawn, mist).

### Animals (`art/animals/`)

Roster so far:

- base set (V1R00): axolotl · fennec fox · pangolin · aye-aye · narwhal · okapi ·
  tardigrade · mantis shrimp · quokka · markhor
- wave 2 (shipped): capybara · fossa · saiga · secretary bird · jerboa · kakapo ·
  tapir · sun bear · shoebill · dumbo octopus · gerenuk · maned wolf · blobfish ·
  potoo · vaquita · aye-aye V2
- wave 3 (shipped): platypus · echidna · numbat · caracal · wolverine ·
  snow leopard · manatee · cassowary · hoatzin · gharial · tuatara ·
  horseshoe crab · nautilus
- wave 4 (open in #51): glass frog · thorny devil · harpy eagle · kiwi · tarsier ·
  emperor tamarin · proboscis monkey · binturong · colugo · pink fairy armadillo ·
  wombat · musk ox · bongo · babirusa · leafy seadragon · ocean sunfish

Pool for later agents: dik-dik · pudu · serval · oryx · ibis · civet · dugong ·
pangolin full body · saiga herd scene.

### Insects (`art/insects/`)

Same disc, same name line; the second line is the taxonomic order in caps
(`COLEOPTERA`, `LEPIDOPTERA`, `ODONATA`, `HEMIPTERA`, `HYMENOPTERA`,
`MANTODEA`, `PHASMATODEA`, `MEGALOPTERA`, `BLATTODEA`). Pose is three-quarter
dorsal unless the silhouette is lateral (stick insect, dobsonfly, cicada);
keep the whole animal inside the disc, antennae and legs included.
Wings are translucent with visible venation over the backdrop, never an opaque
fill. Living specimens, not collected ones: no pins, no kill jars, no shadow
box — the insect is alive on the plate. Wave 1 roster: giraffe weevil ·
Hercules beetle · stag beetle · jewel beetle · atlas moth · orchid mantis ·
spotted lanternfly · periodical cicada · firefly · green darner · monarch ·
walking stick · dobsonfly · leafcutter ant · termite queen · planthopper nymph.

### Furniture (`art/furniture/`)

One piece per plate, in near-side view with a slight three-quarter so depth
reads, seated on a soft shadow ellipse that hugs the disc. The second line is
the material list in caps (`OAK · CANE · BRASS`, `WALNUT · LEATHER · STEEL`).
No manufacturer names, no badges, no designer attributions — generic type
names only, because the drawing is the specimen. Spindles, stretchers and
cane webbing are the thin-geometry trap: ≥3pt, and the piece must not touch
the rim. Wave 1 roster: wingback armchair · chesterfield sofa · plywood lounge
chair · bentwood café chair · Windsor chair · rocking chair · sling chair ·
pedestal table · nesting tables · roll-top desk · campaign chest · highboy
dresser · four-poster bed · chaise longue · arc floor lamp · coat stand.

### Vehicles (`art/vehicles/`)

Profile view, wheels or hull grounded on a chord of the disc, moving right
unless the design reads better the other way. The second line is the spec in
caps (`1929 · AIR-COOLED FLAT-SIX`, `DIESEL-ELECTRIC · 1,200 HP`). Keep
liveries and numbers generic: no real operator marks, no manufacturer badges,
no racing numbers of actual cars. Windows and glazing are translucent so the
backdrop reads through; chrome is a gradient, never a white bar. Wave 1
roster: steam locomotive · streetcar · double-decker bus · city taxi · vintage
fire engine · pickup truck · camper van · rear-engined coupe · land-speed
streamliner · cargo bike · sidecar motorcycle · biplane · flying boat · rigid
airship · tugboat · paddle steamer.

---

## The Orient series — zodiac, festivals, symbols

A second standing series, sharing the field-plate grammar (1000×1000, disc
centre 500,460 r420, name baseline 934, second line 970) but with its own
dressings. Every plate carries a small vermilion seal chop at the top right,
outside the disc; that chop is a deliberate exception to the rim rule, like
the name block.

Four sub-series live under `art/`:

- **`zodiac/` — Celestial Seals.** The twelve animals, one bust per seal,
  each on the disc of its fixed element (Wood green, Fire red, Earth ochre,
  Metal silver, Water blue). A ring of the twelve earthly branches runs
  inside the rim; the animal's branch character is stamped in the chop. The
  second line is the animal character and its current/next years.
  Shipped: rat · ox · tiger · rabbit · dragon · snake · horse · goat ·
  monkey · rooster · dog · pig.
- **`chinese-festivals/` — Festival Seals.** One emblem per festival, warm
  ink and a festival-specific palette, with the date line in the second
  line. Shipped: spring-festival · lantern-festival · dragon-boat ·
  qingming · qixi · mid-autumn. (Roster complete.)
- **`indian-festivals/` — Festival Seals.** Diya, rangoli, torana and
  marigold vocabulary; no deities in scene, no flags. Shipped: diwali ·
  holi · navratri · ganesh-chaturthi · raksha-bandhan · onam. (Roster
  complete.)
- **`indian-symbols/` — Yantra plates.** One symbol per plate on a deep
  field, gold geometry: om · mandala · lotus · peacock · kalash · rangoli.

Shared code: `work/orient/plate.py` (canvas grammar, motifs, caption/chop),
`work/orient/zodiac.py` (element palettes, branch ring, beast parts),
`work/festivals-cn/cn_kit.py`, `work/festivals-in/festival_kit.py`.
Drivers live in `work/zodiac/`, `work/festivals-cn/`, `work/festivals-in/`,
`work/symbols/` and follow the same revision rule as every other piece.

Cultural guardrails: traditional characters for the zodiac seals; festival
plates show objects and settings, not worshippers; Ganesh Chaturthi, when it
lands, is an iconic emblem, not caricature; no national flags, maps or
political symbols anywhere in the series.

## Analysis log

- **Round 0 — the existing body of work:** see `ANALYSIS-ROUND-0.md`.
  Baseline verdict: shading standard is set (portrait, bunny v2, Jolly set);
  recurring risks are clipped geometry at canvas edges and shapes reading
  flatter inside badges than in free compositions.
- **Orient festival roster completion (qingming · qixi · mid-autumn · holi ·
  navratri · ganesh-chaturthi · raksha-bandhan · onam):** per-piece notes in
  the commit messages; series-wide lessons: circles straddling a silhouette
  edge read as beads (umbrella scallops, mooncake) — build scalloped edges as
  single bump paths; the staged kit swallow/magpie needed redraws at plate
  scale (floating ears, penguin breasts); splash blobs must speak the same
  soft-puff language as the clouds around them; kit radial gradients take
  stop pairs only, no focus tuple. `inside()` guards caught two rim hangs,
  `check_rim.py` caught a third before any commit.
