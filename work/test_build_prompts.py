import tempfile
import unittest
from pathlib import Path, PurePosixPath
from urllib.parse import urlsplit

from build_prompts import LINK, ROOT, build, rebase_links


class PromptBuilderTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for group in ("core", "banks", "series", "analysis"):
            self.write(f"{group}/00-base.md", f"## {group}\n\nOriginal material.\n")

    def write(self, path, body):
        file = self.root / "prompts" / path
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(body, encoding="utf-8")

    def test_groups_and_paths_have_deterministic_order(self):
        self.write("themes/z-last.md", "## Last\n")
        self.write("themes/a-first.md", "## First\n")
        result = build(self.root)
        self.assertEqual(result, build(self.root))
        self.assertLess(result.index("## core"), result.index("## banks"))
        self.assertLess(result.index("## analysis"), result.index("## First"))
        self.assertLess(result.index("## First"), result.index("## Last"))
        self.assertIn("<!-- Source: prompts/themes/a-first.md -->", result)
        self.assertTrue(result.endswith("\n"))

    def test_pending_notes_are_marked_as_proposals(self):
        self.write("inbox/task.md", "## New finding\n\nEvidence.\n")
        result = build(self.root)
        self.assertLess(result.index("## Pending task notes"), result.index("## New finding"))
        self.assertIn("not adopted rules", result)

    def test_templates_drafts_and_archives_are_not_compiled(self):
        for group in ("templates", "issues", "archive"):
            self.write(f"{group}/example.md", "# Not a source fragment\n")
        self.assertNotIn("Not a source fragment", build(self.root))

    def test_preview_leaves_the_committed_snapshot_alone(self):
        snapshot = self.root / "PROMPTS.md"
        snapshot.write_text("An intentionally older snapshot.\n", encoding="utf-8")
        build(self.root)
        self.assertEqual(
            snapshot.read_text(encoding="utf-8"),
            "An intentionally older snapshot.\n",
        )

    def test_missing_required_group_is_an_error(self):
        (self.root / "prompts/core/00-base.md").unlink()
        with self.assertRaisesRegex(ValueError, "Missing prompt sources: prompts/core"):
            build(self.root)

    def test_empty_or_top_level_fragments_are_errors(self):
        for body in ("", "# Wrong heading\n"):
            with self.subTest(body=body):
                self.write("themes/bad.md", body)
                with self.assertRaisesRegex(ValueError, "must start with a ## heading"):
                    build(self.root)

    def test_local_links_are_rebased(self):
        body = "[Rules](../../AGENTS.md#revision) ![Proof](../../art/proof.png)"
        self.assertEqual(
            rebase_links(body, PurePosixPath("prompts/core")),
            "[Rules](AGENTS.md#revision) ![Proof](art/proof.png)",
        )

    def test_external_absolute_and_anchor_links_are_unchanged(self):
        body = "[Web](https://example.com/a?q=b#c) [Here](#rules) [Root](/a) [Mail](mailto:a@b)"
        self.assertEqual(rebase_links(body, PurePosixPath("prompts/core")), body)

    def test_real_sources_compile_without_requiring_a_fresh_snapshot(self):
        result = build(ROOT)
        self.assertIn("FK-01", result)
        self.assertIn("JM-04", result)
        self.assertIn("no deities in scene", result)
        self.assertIn("not critique", result)
        self.assertIn("[AGENTS.md](AGENTS.md)", result)

    def test_workshop_and_compiled_local_links_exist(self):
        documents = [
            (path.parent, path.read_text(encoding="utf-8"))
            for path in (ROOT / "prompts").rglob("*.md")
        ]
        documents.append((ROOT, build(ROOT)))
        for parent, body in documents:
            for match in LINK.finditer(body):
                target = urlsplit(match.group(2))
                if target.scheme or target.netloc or not target.path or target.path.startswith("/"):
                    continue
                with self.subTest(parent=parent, target=target.path):
                    self.assertTrue((parent / target.path).exists())


if __name__ == "__main__":
    unittest.main()
