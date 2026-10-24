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
It bumps `V` and resets `R`, and the revision it reads from is left alone. A
refinement of a rendition bumps `R` only and starts from that rendition's own
newest native. So far: axolotl V2 (dark tank, full body; R01 gives the tail
fin mass and a point) · aye-aye V2 (moonlit branch, mid-tap) · binturong V2
(moonlit canopy, tail-wrapped) · monarch V2 (dusk, backlit on milkweed) ·
windsor chair V2 (walnut, low sun, cast shadow; R01 rebuilds the seat as a
dished plank) · city taxi V2 (dawn, mist).

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
- wave 4 (shipped): glass frog · thorny devil · harpy eagle · kiwi · tarsier ·
  emperor tamarin · proboscis monkey · binturong · colugo · pink fairy armadillo ·
  wombat · musk ox · bongo · babirusa · leafy seadragon · ocean sunfish
- wave 5 (shipped): dik-dik · pudu · serval · oryx · scarlet ibis · civet ·
  dugong · leaf insect · Pallas's cat · addax · tawny frogmouth ·
  resplendent quetzal · hellbender · goblin shark · vampire squid
- wave 6 (shipped): elephant · tufted deer · barreleye · sea pig ·
  giant isopod · takin · quoll · kea · coelacanth · solenodon · lyrebird ·
  spider crab · nine-banded armadillo

Pool for later agents: pangolin full body · saiga herd scene — the rest of
the old pool shipped in wave 5.

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

## Companion plates — mascots, lorelog, poetry, site

Same disc, same caption stack (name ~54–58pt at y≈930, a second tracked line
under it at y≈968), but the subjects aren't specimens and the second line is
a role or epithet, not a spec. Living in `art/<series>/<slug>/`, scripts in
`work/<series>/`.

### Mascots (`art/mascots/`)

Portrait plates for the archive's numbered cast — the slug is
`<number>.<name>`, the number being the code the mascot answers to (418 is,
of course, a teapot). The second line is the mascot's office
("KEEPER OF THE GOLDEN TALLY"). Roster so far:

- 326 coverage ledger cherub · 408 the half-held breath · 409 ledger snag ·
  410 vacancy notice · 411 inchkeeper bale · 412 red pencil mercy ·
  413 barrelbody · 414 ribbon mile · 415 jarlabel stranger ·
  416 shelfmark hollow · 418 teapotta protocol · 421 wrong-door finch ·
  422 form-sister pale · 423 keyholder null · 424 the second domino ·
  425 dawnstamp · 426 old-wire pilgrim · 428 safekeeping clause ·
  429 queue matron · 431 paper crown · 432 afterimage clerk ·
  433 sidecar-conflict porter · 434 obsolescence steward ·
  435 driftlocked policy box · 436 jiggler jimmy · 437 manager mike ·
  438 mod maria · 439 ring rita · 444 bureau bob · 445 deepfake dave ·
  446 climate cliff · 451 the quiet injunction · 502 bad-gateway greg ·
  503 servicey unavailabelle · 504 unanswered knock · 672 map-72 absentia ·
  937 blinko chompframe

### Lorelog (`art/lorelog/`)

The archive's incident log, illustrated: one plate per log entry, slugged
`llg-<NNNN>-<slug>`. Forms file themselves, protocols get invoked, the red
pencil is a recurring character. The second line names the protocol or
form. Roster so far:

- llg-0051 emotional verification deadlock · llg-0088 boily thermal
  conscience · llg-0350 doge charter · llg-0375 breeding program anomaly ·
  llg-0451 jiggler empathegy bridge · llg-0453 mascot character arc map

### Poetry (`art/poetry/`)

Verse plates: the poem is the plate — stanzas set around a central
vignette, or the whole thing dressed as a wanted poster. `hai-` is a
haiku set, `lim-` a limerick; the second line carries the catalogue
number. Roster so far:

- hai-004 boily mcplaterton · hai-019 kindy mcexistentialcrisis ·
  hai-046 svgon the line · lim-0048 boily mcplaterton ·
  lim-0194 semantic seymour

### Site (`art/site/`)

Site equity: the marks the generated gallery actually runs on — the ◈
brand mark, the collection map, the search icon, an ornament. The second
line says what the piece is for. Roster so far:

- site-brand-mark · site-collection-map · site-search-icon ·
  site-verse-residue-ornament

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
  line. Shipped: spring-festival · lantern-festival · dragon-boat. Still
  open: qingming · qixi · mid-autumn.
- **`indian-festivals/` — Festival Seals.** Diya, rangoli, torana and
  marigold vocabulary; no deities in scene, no flags. Shipped: diwali.
  Still open: holi · navratri · ganesh-chaturthi · raksha-bandhan · onam.
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
