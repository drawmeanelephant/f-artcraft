#!/usr/bin/env python3
"""Scans the repo artwork and writes docs/data/*.json for the knap
templates, and copies every image file the site references into
docs/site/media/ (gitignored — the deploy artifact carries them).

Deterministic: same repo state -> same output bytes. Run before
docs/build.sh. Stdlib only so CI needs nothing but python3.

Versioned pieces live at art/<category>/<slug>/<slug>-V*R*.{svg,@2x.png}
or art/<slug>-V*R*.{svg,@2x.png}; singletons are plain *.svg under
muse/, guest/, or the repo root."""
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
MEDIA = DOCS / "site" / "media"

REV = re.compile(r"^(?P<slug>.+)-V(?P<v>\d+)R(?P<r>\d+)$")

# twitter/*.svg and the root fart-knocker.svg are byte-identical to art/
# files — the set is shown once, from art/.
SKIP_DIRS = {"twitter"}

PAGES = ["index", "plates", "machines", "pieces", "guest", "about"]

NAV = ('"index":index.html · "plates":plates.html · "machines":machines.html'
       ' · "pieces":pieces.html · "guest":guest.html · "about":about.html')


def humanize(slug):
    return slug.replace("-", " ").title()


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


def main():
    if MEDIA.exists():
        shutil.rmtree(MEDIA)
    MEDIA.mkdir(parents=True)

    art = ROOT / "art"
    plates = [section("Animals", art / "animals"),
              section("Insects", art / "insects")]
    machines = [section("Vehicles", art / "vehicles"),
                section("Furniture", art / "furniture")]

    fk = collect_versioned(art).get("fart-knocker", [])
    fk_cards = [card("fart-knocker", fk)]
    crest = ROOT / "fart-knocker-crest.svg"
    if crest.exists():
        fk_cards.append(singleton(crest))
    faf = collect_versioned(art)
    pieces = [
        {"title": "Fart Knocker — self-portrait & crest", "pieces": fk_cards},
        {"title": "The Filed & Forgotten set", "pieces":
            [card(s, faf[s]) for s in ("bunny-avatar", "bunny-banner", "golly") if s in faf]},
        {"title": "Ember dusk", "pieces":
            [card(s, faf[s]) for s in sorted(faf) if s.startswith("ember-dusk")]},
        {"title": "Empathegy brochure", "pieces":
            [card(s, faf[s]) for s in sorted(faf) if s.startswith("empathegy")]},
        {"title": "Muse — Jolly", "pieces":
            [singleton(f) for f in sorted((ROOT / "muse").glob("*.svg"))]},
    ]

    guest_dir = ROOT / "guest" / "freebuff"
    guest_secs = [{"title": "Freebuff — DeepSeek, six styles + dusk poster",
                   "pieces": [singleton(f) for f in sorted(guest_dir.glob("*.svg"))]}]

    counts = {
        "animals": sum(len(s["pieces"]) for s in plates[:1]),
        "insects": sum(len(s["pieces"]) for s in plates[1:]),
        "vehicles": sum(len(s["pieces"]) for s in machines[:1]),
        "furniture": sum(len(s["pieces"]) for s in machines[1:]),
    }
    total = sum(counts.values()) + sum(len(s["pieces"]) for s in pieces)

    featured = []
    for label, slug, base in (
        ("Fart Knocker — self-portrait", "fart-knocker", art),
        ("Ember dusk", "ember-dusk", art),
        ("Golly — Filed & Forgotten", "golly", art),
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
            "counts": (f"{counts['animals']} animal plates · {counts['insects']} insect plates"
                       f" · {counts['vehicles']} vehicles · {counts['furniture']} furniture"
                       f" — {total} pieces in the gallery"),
            "featured": featured,
            "nav": NAV,
        },
        "plates": {
            "title": "Field plates",
            "intro": ("Natural-history-style specimen plates — gradients and "
                      "translucent shading, never flat fills. The full set, newest "
                      "revision of each."),
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

    for name, obj in data.items():
        (DOCS / "data" / f"{name}.json").write_text(json.dumps(obj, indent=2) + "\n")

    n_media = sum(1 for _ in MEDIA.rglob("*") if _.is_file())
    print(f"data: {', '.join(data)} | media files: {n_media} | total pieces: {total}")


if __name__ == "__main__":
    sys.exit(main())
