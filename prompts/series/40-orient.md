## The Orient series — zodiac, holidays, symbols

A second standing series, sharing the field-plate grammar (1000×1000, disc
centre 500,460 r420, name baseline 934, second line 970) but with its own
dressings. Every plate carries a small vermilion seal chop at the top right,
outside the disc; that chop is a deliberate exception to the rim rule, like
the name block.

Three sub-series live under `art/`. These are historical rosters,
not a per-branch queue:

- **`zodiac/` — Celestial Seals.** The twelve animals, one bust per seal,
  each on the disc of its fixed element (Wood green, Fire red, Earth ochre,
  Metal silver, Water blue). A ring of the twelve earthly branches runs
  inside the rim; the animal's branch character is stamped in the chop. The
  second line is the animal character and its current/next years.
  Shipped: rat · ox · tiger · rabbit · dragon · snake · horse · goat ·
  monkey · rooster · dog · pig.
- **`holidays/` — Festival Seals.** One emblem per holiday, warm ink and a
  holiday-specific palette, with the date line in the second line. Chinese
  and Indian festival rosters now live here alongside a wider calendar
  of religious, government and food holidays. Shared rules: objects and
  settings, not worshippers; no national flags, maps or political symbols.
  - Chinese holidays: spring-festival · lantern-festival · dragon-boat ·
    qingming · qixi · mid-autumn. (Original roster shipped.)
  - Indian holidays: diwali · holi · navratri · ganesh-chaturthi ·
    raksha-bandhan · onam. (Original roster shipped.) Diya, rangoli,
    torana and marigold vocabulary; no deities in scene, no flags.
- **`indian-symbols/` — Yantra plates.** One symbol per plate on a deep
  field, gold geometry: om · mandala · lotus · peacock · kalash · rangoli.

The wider holiday calendar joins the same folder, one emblem per holiday,
same plate grammar. Planned roster retained from the holiday migration;
the issue tracker, not this snapshot, holds the live claimable list:

- Religious: christmas · easter · eid-al-fitr · eid-al-adha · hanukkah ·
  purim · passover · vesak · nowruz · obon · songkran · dia-de-los-muertos
- Government: bastille-day · guy-fawkes-night · juneteenth · canada-day ·
  golden-week · remembrance-day
- Food: pancake-day · oktoberfest · la-tomatina · thanksgiving

Shared code: `work/orient/plate.py` (canvas grammar, motifs, caption/chop),
`work/orient/zodiac.py` (element palettes, branch ring, beast parts),
`work/holidays/cn_kit.py`, `work/holidays/festival_kit.py`.
Drivers live in `work/zodiac/`, `work/holidays/`, `work/indian-symbols/`
and follow the same revision rule as every other piece.

Cultural guardrails: traditional characters for the zodiac seals; festival
plates show objects and settings, not worshippers; Ganesh Chaturthi, when it
lands, is an iconic emblem, not caricature; no national flags, maps or
political symbols anywhere in the series.
