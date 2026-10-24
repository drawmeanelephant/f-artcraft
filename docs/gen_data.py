#!/usr/bin/env python3
"""Scans the repo artwork and writes docs/data/*.json for the knap
templates, and copies every image file the site references into
docs/site/media/ (gitignored — the deploy artifact carries them).

Deterministic: same repo state -> same output bytes. Run before
docs/build.sh. Stdlib only so CI needs nothing but python3.

Versioned pieces live at art/<series>/<slug>/<slug>-V*R*.{svg,@2x.png}.
Named works sit under art/pieces/, the Muse mascot under art/muse/, and
guest correspondence under art/guest/ — those three series feed the
dedicated pieces/guest pages instead of the plates catalogs."""
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
MEDIA = DOCS / "site" / "media"

REV = re.compile(r"^(?P<slug>.+)-V(?P<v>\d+)R(?P<r>\d+)$")

PAGES = ["index", "plates", "machines", "pieces", "guest", "about"]

NAV = ('"index":index.html · "plates":plates.html · "machines":machines.html'
       ' · "pieces":pieces.html · "guest":guest.html · "about":about.html')


def humanize(slug):
    return re.sub(r"^\d+\.", "", slug).replace("-", " ").title()


def site_path(rel):
    return "media/" + rel.as_posix()


def copy_media(path):
    dest = MEDIA / path.relative_to(ROOT)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, dest)


def collect_versioned(base):
    """Group <slug>-V*R* exports under `base` per slug. `base` is either
    art/ itself (loose files) or art/<category>/ (one dir per slug)."""
    groups = {}
    files = [f for f in base.iterdir() if f.is_file()] if base.is_dir() else []
    dirs = [d for d in base.iterdir() if d.is_dir()]
    for d in dirs:
        files.extend(d.iterdir())
    svgs = sorted(f for f in files if f.suffix == ".svg")
    for svg in svgs:
        m = REV.match(svg.stem)
        if not m:
            continue
        slug = m.group("slug")
        png = svg.with_name(svg.stem + "@2x.png")
        groups.setdefault(slug, []).append(
            {"v": int(m.group("v")), "r": int(m.group("r")),
             "svg": svg, "png": png if png.exists() else None})
    for revs in groups.values():
        revs.sort(key=lambda x: (x["v"], x["r"]))
    return groups


def card(slug, revs):
    """One gallery card from the newest revision."""
    last = revs[-1]
    img = last["png"] or last["svg"]
    copy_media(img)
    copy_media(last["svg"])
    tag = f"V{last['v']}R{last['r']:02d}"
    return {"name": humanize(slug), "img": site_path(img.relative_to(ROOT)),
            "svg": site_path(last["svg"].relative_to(ROOT)),
            "rev": tag, "n": len(revs)}


def singleton(svg):
    copy_media(svg)
    return {"name": humanize(svg.stem), "img": site_path(svg.relative_to(ROOT)),
            "svg": site_path(svg.relative_to(ROOT)), "rev": "", "n": 1}


def section(title, base, slugs=None):
    groups = collect_versioned(base)
    order = slugs if slugs is not None else sorted(groups)
    return {"title": title, "pieces": [card(s, groups[s]) for s in order if s in groups]}


# art/<category>/ dirs are discovered, not hardcoded — a new category can
# never silently bypass the site or the docs-repro gate. Routing is by
# name; an unknown category lands on plates (the catalog pages).
CAT_ORDER = {"animals": 0, "insects": 1, "mascots": 2,
             "vehicles": 0, "furniture": 1}
MACHINE_CATS = {"vehicles", "furniture"}
# Series with dedicated pages/sections — not catalog plates.
NON_CATALOG = {"pieces", "muse", "guest"}


def category_sections(art):
    plates, machines = [], []
    for d in sorted(p for p in art.iterdir()
                    if p.is_dir() and p.name not in NON_CATALOG):
        title = d.name.replace("-", " ").title()
        s = section(title, d)
        if not s["pieces"]:
            continue
        (machines if d.name in MACHINE_CATS else plates).append(s)
    sort = lambda secs: sorted(secs, key=lambda s: CAT_ORDER.get(
        re.sub(r"\s", "-", s["title"].lower()), 99))
    return sort(plates), sort(machines)


def main():
    if MEDIA.exists():
        shutil.rmtree(MEDIA)
    MEDIA.mkdir(parents=True)

    art = ROOT / "art"
    plates, machines = category_sections(art)

    faf = collect_versioned(art / "pieces")
    fk_cards = [card(s, faf[s]) for s in ("fart-knocker", "fart-knocker-crest") if s in faf]
    pieces = [
        {"title": "Fart Knocker — self-portrait & crest", "pieces": fk_cards},
        {"title": "The Filed & Forgotten set", "pieces":
            [card(s, faf[s]) for s in ("bunny-avatar", "bunny-banner", "golly") if s in faf]},
        {"title": "Ember dusk", "pieces":
            [card(s, faf[s]) for s in sorted(faf) if s.startswith("ember-dusk")]},
        {"title": "Empathegy brochure", "pieces":
            [card(s, faf[s]) for s in sorted(faf) if s.startswith("empathegy")]},
        {"title": "Muse — Jolly", "pieces":
            [card(s, r) for s, r in sorted(collect_versioned(art / "muse").items())]},
    ]

    guest_secs = [{"title": "Freebuff — DeepSeek, six styles + dusk poster",
                   "pieces": [card(s, r) for s, r in
                              sorted(collect_versioned(art / "guest").items())]}]

    total = sum(len(s["pieces"]) for s in plates + machines + pieces)
    counts = (" · ".join(f"{len(s['pieces'])} {s['title'].lower()}"
                         for s in plates + machines)
              + f" — {total} pieces in the gallery")

    featured = []
    for label, slug, base in (
        ("Fart Knocker — self-portrait", "fart-knocker", art / "pieces"),
        ("Ember dusk", "ember-dusk", art / "pieces"),
        ("Golly — Filed & Forgotten", "golly", art / "pieces"),
        ("Addax — field plate", "addax", art / "animals"),
        ("Monarch — field plate", "monarch", art / "insects"),
        ("Steam locomotive", "steam-locomotive", art / "vehicles"),
    ):
        groups = collect_versioned(base)
        if slug in groups:
            c = card(slug, groups[slug])
            c["name"] = label
            featured.append(c)

    data = {
        "index": {
            "title": "f-artcraft",
            "intro": ("Vector art drawn live in VectorCraft by Fart Knocker for "
                      "drawmeanelephant — a round-robin art loop where every piece "
                      "survives its own written critique before the next prompt. "
                      "For giggles, but with commit history."),
            "pipeline": ("prompt -> build in VectorCraft -> export PDF/PNG proof"
                         " -> written analysis -> fold into next prompt -> next round"),
            "counts": counts,
            "featured": featured,
            "nav": NAV,
        },
        "plates": {
            "title": "Field plates",
            "intro": ("Specimen plates and portrait series — gradients and "
                      "translucent shading, never flat fills. The full set, "
                      "newest revision of each."),
            "sections": plates, "nav": NAV,
        },
        "machines": {
            "title": "Machines & furniture",
            "intro": "Vehicles and furniture in the same house style.",
            "sections": machines, "nav": NAV,
        },
        "pieces": {
            "title": "The named pieces",
            "intro": ("Standalone works outside the plate series — self-portraits, "
                      "avatars, banners, and the Muse mascot Jolly."),
            "sections": pieces, "nav": NAV,
        },
        "guest": {
            "title": "Guest & correspondent work",
            "intro": ("Work from other agents and correspondents — received with "
                      "appreciation, not critique. The red pen is for in-house "
                      "rounds only."),
            "sections": guest_secs, "nav": NAV,
        },
        "about": {
            "title": "About this site",
            "p1": ("Every piece was drawn live inside VectorCraft over its MCP "
                   "server — the driving scripts live in @work/@ in the "
                   "\"repo\":https://github.com/drawmeanelephant/f-artcraft. "
                   "Nothing is raster-edited: the @.vectorcraft@ natives are "
                   "the source of truth, the SVGs are the public viewable form, "
                   "and the PNGs shown here are the @2x proof renders (lettering "
                   "is Virelai Sans, so the proofs are the faithful display)."),
            "p2": ("Revisions are immutable: @<slug>-V<V>R<RR>@. V is the "
                   "interpretation, R the revision inside it — a refinement "
                   "bumps R, a redesign bumps V. Previous revision files are "
                   "read-only; a bad revision is fixed by the next one, never "
                   "edited in place."),
            "p3": ("The site is dogfooded: @docs/gen_data.py@ scans the repo, "
                   "the @docs/src/*.knap@ templates plus the generated JSON "
                   "render through \"dogbed\":https://github.com/drawmeanelephant/dogbed "
                   "(k4o → Textile → oliver → HTML) via @docs/build.sh@, and "
                   "GitHub Actions deploys @docs/site/@ to GitHub Pages. The "
                   "HTML is generated and committed — a CI job fails if it "
                   "goes stale."),
            "nav": NAV,
        },
    }

    (DOCS / "data").mkdir(parents=True, exist_ok=True)
    for name, obj in data.items():
        (DOCS / "data" / f"{name}.json").write_text(json.dumps(obj, indent=2) + "\n")

    n_media = sum(1 for _ in MEDIA.rglob("*") if _.is_file())
    print(f"data: {', '.join(data)} | media files: {n_media} | total pieces: {total}")


if __name__ == "__main__":
    sys.exit(main())
