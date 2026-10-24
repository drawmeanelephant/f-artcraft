import unittest

from task_labels import backfill_plan, catalogue, infer_type


class TaskLabelTests(unittest.TestCase):
    def test_established_plate_titles_are_illustrations(self):
        for title in (
            "Animal — field plate: jaguar", "Furniture — field plate: library globe",
            "Insect — field plate: glasswing", "Watercraft — field plate: paopao",
            "Holiday seal: diwali (religious)", "Field plate: blue morpho",
            "Mascot portrait: A clerk",
        ):
            with self.subTest(title=title):
                self.assertEqual(infer_type(title), "illustration")

    def test_tracking_index_is_not_a_leaf_art_task(self):
        self.assertEqual(infer_type("Animals — field plates, wave 7"), "tracking")

    def test_current_os_request_types(self):
        cases = {
            "VirelaiOS — figcraft sheet: design tokens + primitives": "design-system",
            "VirelaiOS — figcraft sheet: key app screens": "ui",
            "VirelaiOS — figcraft sheet: the seat shell": "ui",
            "VirelaiOS — app-icon set (31 icons)": "icons",
            "VirelaiOS — file-type icon family (9 icons for GOFILES)": "icons",
            "VirelaiOS — cursor set (arrow refresh + 8 context cursors)": "icons",
            "VirelaiOS — spinner sprite (8-12 frames)": "motion",
            "VirelaiOS — wallpaper set (re-render + 3 variants)": "illustration",
            "VirelaiOS — sexiburger mascot pose set (6 poses)": "illustration",
        }
        for title, kind in cases.items():
            with self.subTest(title=title):
                self.assertEqual(infer_type(title), kind)

    def test_unknown_titles_require_review(self):
        for title in ("Fix the icon exporter", "UI experiment", "A field plate indexer"):
            with self.subTest(title=title):
                self.assertIsNone(infer_type(title))

    def test_existing_type_is_preserved_even_if_unrecognized_or_conflicting(self):
        for labels in (["type:custom"], ["type:icons"], ["type:icons", "type:ui"]):
            with self.subTest(labels=labels):
                issue = {"number": 1, "title": "Animal — field plate: jaguar",
                         "labels": [{"name": label} for label in labels]}
                result = backfill_plan([issue])
                self.assertEqual(result["add"], [])
                self.assertEqual(result["preserved"][0]["labels"], sorted(labels))

    def test_plan_never_changes_claims_or_infers_work_intent(self):
        issue = {"number": 1, "title": "VirelaiOS — wallpaper set (re-render + 3 variants)",
                 "labels": [{"name": "claimed"}, {"name": "work:refinement"}]}
        original_labels = list(issue["labels"])
        result = backfill_plan([issue])
        self.assertEqual(result["add"][0]["label"], "type:illustration")
        self.assertEqual(issue["labels"], original_labels)
        self.assertNotIn("work:", str(result))
        self.assertNotIn("claimed", str(result))

    def test_catalogue_is_small_unique_and_contains_no_model_rankings(self):
        labels = catalogue()
        names = [label["name"] for label in labels]
        self.assertEqual(len(names), len(set(names)))
        self.assertEqual(len(names), 11)
        self.assertNotIn("claimed", names)
        for label in labels:
            self.assertTrue(label["name"].startswith(("type:", "work:")))
            self.assertNotIn("cheap", label["name"])
            self.assertLessEqual(len(label["description"]), 100)


if __name__ == "__main__":
    unittest.main()
