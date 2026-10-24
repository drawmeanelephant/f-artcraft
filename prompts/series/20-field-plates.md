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

**Inventory note:** the rosters below are historical notes retained from the
original bank, not a live catalogue or work queue. Inspect `art/` and current
issues before choosing a subject. Do not update these lists on art branches.

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

Historical roster:

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
