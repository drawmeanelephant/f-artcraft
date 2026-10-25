# Dog breeds — milestone cards, wave 2 (proposal)

Status: draft proposal, not posted. One tracking issue plus twelve leaf
issues; each leaf is one new piece. Wave 1 shipped via #1560 (leaves
#1498–1513) — every leaf below is new.

## Wave 1 inventory (do not duplicate)

australian-shepherd · beagle · bernese-mountain-dog · border-collie ·
dachshund · dalmatian · german-shepherd · golden-retriever · greyhound ·
labrador-retriever · pembroke-welsh-corgi · pug · shiba-inu ·
siberian-husky · standard-poodle

Wave 1 covered HERDING ×4, HOUND ×3, WORKING ×3, NON-SPORTING ×3,
SPORTING ×2, TOY ×1 — and no terriers at all. Wave 2 fills the terrier
gap and broadens the silhouette vocabulary (cords, wrinkles, floor-length
coat, ridge).

## Format (milestone cards — field-plate chassis)

- 1000×1000 canvas: dark moody backdrop → large gradient plate disc
  (centre 500,460, r≈420) → subject → name in caps, Virelai Sans ~56–60pt
  at y≈930.
- The milestone line under the name in caps, Virelai Sans ~22–24pt, wide
  tracking, y≈968, ≤760pt wide — check it clears the disc's lower arc.
- Gradients and translucent shading, never flat fills. Warm dark ink,
  never pure black. Nothing crosses the rim; shapes near the lower edge
  close on the disc's own arc.
- Keep the breed-defining traits accurate to type (coat, ear set, tail
  carriage); thin essentials ≥3pt and the whole dog inside the rim. The
  milestone line is the kennel group and origin — `GROUP · ORIGIN`.
- First pass is `<slug>-V1R00`. Deliverables on main:
  `art/dog-breeds/<slug>/<slug>-V1R00.vectorcraft` + `.svg` and driver
  `work/dog-breeds/draw_<slug>.py`; the `@2x.png` proof goes to the
  `media` branch; the `.pdf` stays in `work/out/` (local only).

## Proposed leaves (12)

### afghan hound — `HOUND · AFGHANISTAN`

The aristocrat: floor-length silky coat, topknot, ringed tail carried
high. Standing profile in a light breeze so the coat streams; keep the
dog's underline clean so the body reads under all that hair.

### airedale terrier — `TERRIER · ENGLAND`

The king of terriers, wave 2's first TERRIER: black-and-tan wire coat,
rectangular skull, folded ears, alert stance. Render the wiry texture
with short hatch strokes ≥3pt; bearded muzzle toward the viewer.

### alaskan malamute — `WORKING · ALASKA`

The freighting heavyweight: broad head, plumed tail over the back,
grey/white cap-and-mask markings, snow at the feet. Bigger-boned than
the wave-1 husky — wider shoulders, denser coat, broader face; do not
redraw the husky with different markings.

### basenji — `HOUND · CONGO`

The barkless dog: chestnut coat, tightly curled tail, small erect ears.
The wrinkled forehead is the signature — draw it as layered creases, not
scars. Poised, alert, lightly built.

### basset hound — `HOUND · FRANCE`

The low rider: ear leather sweeping the floor, loose dewlap, mournful
eyes, stubby legs under a long body. Ground-hugging silhouette; the ears
may nearly touch the shadow ellipse but nothing crosses the rim.

### boxer — `WORKING · GERMANY`

The athlete: fawn or brindle with a black mask, undershot jaw, deep
chest, spring-loaded rear. Mid-bounce play bow or an alert sit; natural
ears.

### bulldog — `NON-SPORTING · ENGLAND`

The wall of wrinkles: wide stance, pushed-in face, rope nose fold,
underbite, rolling shoulders. Three-quarter head-on; jowls as
translucent layered folds, never hard hatch lines.

### chihuahua — `TOY · MEXICO`

The smallest dog in the series: apple-dome skull, huge erect ears, big
eyes. Proportion is the breed — oversized head, tiny body; ear edges
≥3pt so they survive plate scale.

### chow chow — `NON-SPORTING · CHINA`

The lion dog: dense red mane, deep-set eyes, straight hind legs giving
the stilted gait. The mane mass carries the silhouette; blue-black
tongue only if the mouth opens.

### irish setter — `SPORTING · IRELAND`

The mahogany blur: flowing chestnut coat, feathered ears, legs and tail,
lean and elegant. Standing turn with the coat in motion; the red needs
gradients or it goes flat.

### komondor — `WORKING · HUNGARY`

The mop dog: full white corded coat hiding the whole animal. The drawing
is the cords — layered hanging cords in translucent greys with warm
shadow between; keep a nose break or eyes peeking so it reads as a dog,
not a rug.

### rhodesian ridgeback — `HOUND · SOUTHERN AFRICA`

The ridge is the card: wheaten coat, athletic hound build, the dorsal
stripe of reverse-growing hair down the spine. Profile pose so the ridge
reads as a dark tapered band along the back.

## Alternates pool

saint-bernard · newfoundland · great-dane · doberman · rottweiler ·
samoyed · akita · cane-corso · mastiff · scottish-terrier ·
border-terrier · papillon · pomeranian · boston-terrier ·
french-bulldog · vizsla · weimaraner · whippet · bloodhound · saluki ·
old-english-sheepdog · shetland-sheepdog · chinese-crested

## Posting notes

When the user approves posting: one `type:tracking` parent issue titled
"Dog breeds — milestone cards, wave 2" with this format block and a
checklist of leaf issues; each leaf gets `type:illustration` +
`work:original`, inlines the format/delivery paragraph, and carries its
own brief, slug and milestone line. Claiming follows
`work/issue_claim.py`; see `.github/CLAIMS.md` and `.github/LABELS.md`.
