# Lorelog — wave 2 proposal

Status: draft, not posted. Expansion proposal for `art/lorelog/`. Each
row below is a **separate leaf-issue candidate**, not one task — the
wave splits into individual `Lorelog graphic: <Entry>` issues when
approved.

## Format reminder (from shipped pieces)

Per `work/lorelog/draw_llg_0051_emotional_verification_deadlock.py` and
siblings:

- Canvas 1000×1000. Dark backdrop gradient, plate ellipse `x=80 y=40
  w=840 h=840` (centre 500,460, r≈420), ~6pt rim stroke. The plate may
  carry the document's own palette — llg-0051's disc is parchment-toned,
  not the usual dark glass.
- One plate per log entry: the incident drawn as its own paperwork.
  Forms file themselves, ruled lines recede, stamps read `PREPARED /
  AMBIVALENT / UNFIT`, and a stamp group may tilt via `transform`
  rotate. The red pencil is a recurring character; small cast cameos
  (Kindy watching from a distance) are precedent.
- Caption stack: the entry/document name ~58pt at y≈930 (e.g.
  `FORM 51-E`); the second line at y≈968 names the protocol or form,
  often fully spaced (`F E E L I N G S   A B O U T   F E E L I N G S`,
  ~20pt).
- Slug is `llg-NNNN-<slug>`, NNNN the log entry number — the archive's
  own filing order, not a mascot number.
- Driver `work/lorelog/draw_<slug>.py` → `d.finish("<slug>-V1R00")`;
  commit `.vectorcraft`, `.svg`, `@2x.png`.

## Leaf briefs

Six entries shipped (llg-0051, 0088, 0350, 0375, 0451, 0453 — incident
report, thermal conscience, charter, anomaly, bridge, arc map). Wave 2
widens the document genres the log is willing to file.

| Slug | Subject | Mood / the drawing's job |
| --- | --- | --- |
| `llg-0060-epitaph-for-a-deprecated-field` | Epitaph | Granite tenderness; a small tombstone inside the plate, `FIELD STATUS: NULL`, one flower in a specimen jar — distinct from `art/necropolis/` tombstones: this is the *log entry* about the burial, not the crypt scene |
| `llg-0102-minutes-of-the-unmeeting` | Meeting minutes | Procedural zen; minutes recording, in triplicate, that the meeting was not held |
| `llg-0121-memo-that-answers-itself` | Interdepartmental memo | Bureaucratic soliloquy; a memo thread folding into a single sheet replying to itself |
| `llg-0140-indoor-weather-bulletin` | Climate bulletin | Institutional meteorology; a posted forecast for Corridor C — fog, intermittent stapling |
| `llg-0176-audit-trail-of-the-absent-auditor` | Audit record | Forensic quiet; footprints through dust to a desk and back, the auditor never seen |
| `llg-0204-charter-of-unclaimed-property` | Charter amendment | Custodial grandeur; an annex granting permanent custody of everything nobody claimed |
| `llg-0222-obituary-of-form-51-b` | Obituary notice | Predecessor grief; the notice page for the form 51-E replaced, mourners listed as checkboxes |
| `llg-0264-corridor-heat-notice` | Maintenance circular | Warm resignation; a notice that the corridor is warm again, posted under the previous identical notice |
| `llg-0310-census-of-rubber-stamps` | Census return | Enumerative pride; every stamp counted in rows, one box marked `UNACCOUNTED` |
| `llg-0333-maintenance-log-of-the-unmet-bell` | Service log | Diligent futility; decades of service entries for a bell that has never rung — a cameo of M-417 is allowed, its silhouette only |
| `llg-0417-request-for-identical-replacement` | Change request | Approved tautology; an RFC swapping a form for itself, stamped `APPROVED AS SUBMITTED` |
| `llg-0999-closing-time-notice` | Posted notice | Eternal almost; the notice that the archive closes at an hour that never arrives, edges gone soft with age |

## Guardrails

- Recheck `art/lorelog/`, `art/necropolis/` (tombstone-adjacent), open/
  closed issues and open PRs before writing any leaf issue or claiming.
- Log numbers are the archive's filing order — invented, but keep them
  plausible neighbours of shipped entries and never reuse a shipped
  number.
- A mascot cameo may borrow an existing plate's silhouette; lorelog
  entries document the cast, they do not redesign it.
- Epitaph/obituary briefs stay in the log's voice — the paperwork of
  grief — and keep clear of `art/necropolis/`'s crypt-scene grammar.
- Labels per `.github/LABELS.md`: `type:*` for the deliverable plus an
  explicit `work:*` intent per leaf.
