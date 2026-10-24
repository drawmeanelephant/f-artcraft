import copy
import json
import unittest
from datetime import datetime, timezone
from unittest.mock import patch

from issue_claim import ClaimError, active_claim, claim_issue, status, update_claim

A = "a" * 32
B = "b" * 32
C = "c" * 32


def comment(number, action, token=A, owner="worker/a", when=None, association="OWNER"):
    event = {"action": action, "token": token}
    if action == "claim":
        event.update(owner=owner, branch="plate/test")
    return {
        "id": number, "author_association": association,
        "created_at": when or f"2026-10-24T12:00:{number:02d}Z",
        "html_url": f"https://example.test/comments/{number}",
        "body": "<!-- f-artcraft-claim-v1 " + json.dumps(event) + " -->",
    }


class FakeGitHub:
    def __init__(self, comments=None, labels=None):
        self.comments = comments or []
        self.issue = {
            "state": "open", "title": "Field plate: test",
            "html_url": "https://example.test/issues/1",
            "labels": [{"name": label} for label in (labels or [])],
            "assignees": [],
        }
        self.closed_at = None
        self.label_writes = []
        self.rival_on_claim = False
        self.rival_on_remove = False

    def snapshot(self, number):
        return copy.deepcopy(self.issue), active_claim(self.comments, self.closed_at)

    def append(self, number, event, note=""):
        if self.rival_on_claim and event["action"] == "claim":
            self.rival_on_claim = False
            self.comments.append(comment(len(self.comments) + 1, "claim", B, "worker/b"))
        self.comments.append(comment(
            len(self.comments) + 1, event["action"], event["token"],
            event.get("owner", "worker/a"),
        ))

    def label(self, number, present):
        self.label_writes.append(present)
        if not present and self.rival_on_remove:
            # A new worker acquires ownership and adds its label just before
            # the old worker's late label removal arrives.
            self.rival_on_remove = False
            self.comments.append(comment(len(self.comments) + 1, "claim", B, "worker/b"))
        labels = [label for label in self.issue["labels"] if label["name"] != "claimed"]
        if present:
            labels.append({"name": "claimed"})
        self.issue["labels"] = labels


class ClaimLogTests(unittest.TestCase):
    def test_empty_log(self):
        self.assertIsNone(active_claim([]))

    def test_first_request_wins_even_with_equal_timestamps(self):
        first = comment(1, "claim", when="2026-10-24T12:00:00Z")
        second = comment(2, "claim", B, "worker/b", when="2026-10-24T12:00:00Z")
        self.assertEqual(active_claim([second, first])["token"], A)

    def test_losing_request_is_not_a_future_reservation(self):
        log = [comment(1, "claim"), comment(2, "claim", B, "worker/b"),
               comment(3, "release")]
        self.assertIsNone(active_claim(log))
        log.append(comment(4, "claim", C, "worker/c"))
        self.assertEqual(active_claim(log)["token"], C)

    def test_wrong_token_cannot_heartbeat_or_release(self):
        log = [comment(1, "claim"), comment(2, "heartbeat", B), comment(3, "release", B)]
        current = active_claim(log)
        self.assertEqual(current["token"], A)
        self.assertEqual(current["heartbeat_at"], log[0]["created_at"])

    def test_heartbeat_preserves_owner_and_updates_activity(self):
        log = [comment(1, "claim"), comment(2, "heartbeat")]
        current = active_claim(log)
        self.assertEqual(current["owner"], "worker/a")
        self.assertEqual(current["heartbeat_at"], log[1]["created_at"])

    def test_public_comment_cannot_release_or_claim(self):
        log = [comment(1, "claim"), comment(2, "release", association="NONE"),
               comment(3, "claim", B, association="CONTRIBUTOR")]
        self.assertEqual(active_claim(log)["token"], A)
        self.assertIsNone(active_claim([comment(1, "claim", association="NONE")]))

    def test_malformed_events_do_not_change_ownership(self):
        for payload in ("{}", "[]", '{"action":"claim","token":7}', "{bad}"):
            malformed = comment(2, "claim", B)
            malformed["body"] = "<!-- f-artcraft-claim-v1 " + payload + " -->"
            with self.subTest(payload=payload):
                self.assertEqual(active_claim([comment(1, "claim"), malformed])["token"], A)

    def test_double_markers_do_not_change_ownership(self):
        malformed = comment(2, "release")
        malformed["body"] += malformed["body"]
        self.assertEqual(active_claim([comment(1, "claim"), malformed])["token"], A)

    def test_issue_closure_ends_old_claim_on_reopening(self):
        log = [comment(1, "claim"), comment(3, "claim", B, "worker/b")]
        self.assertIsNone(active_claim(log[:1], "2026-10-24T12:00:02Z"))
        self.assertEqual(active_claim(log, "2026-10-24T12:00:02Z")["token"], B)


class ClaimLifecycleTests(unittest.TestCase):
    def test_successful_claim_is_verified_and_labeled(self):
        api = FakeGitHub(labels=["enhancement"])
        result = claim_issue(api, 1, "t3/thread-123", "plate/test")
        self.assertEqual(result["claim"]["owner"], "t3/thread-123")
        self.assertTrue(result["claimed_label"])
        self.assertIn({"name": "enhancement"}, api.issue["labels"])

    def test_busy_claim_writes_nothing(self):
        api = FakeGitHub([comment(1, "claim")], ["claimed"])
        with self.assertRaisesRegex(ClaimError, "Already claimed"):
            claim_issue(api, 1, "worker/b")
        self.assertEqual(len(api.comments), 1)
        self.assertEqual(api.label_writes, [])

    def test_manual_label_is_not_stolen(self):
        api = FakeGitHub(labels=["claimed"])
        with self.assertRaisesRegex(ClaimError, "Manual/legacy"):
            claim_issue(api, 1, "worker/b")
        self.assertEqual(api.comments, [])
        self.assertEqual(api.label_writes, [])

    def test_closed_assigned_and_wave_issues_are_not_claimed(self):
        cases = [
            ("state", "closed"),
            ("assignees", [{"login": "human"}]),
            ("title", "Animals — field plates, wave 9"),
        ]
        for key, value in cases:
            with self.subTest(key=key):
                api = FakeGitHub()
                api.issue[key] = value
                with self.assertRaises(ClaimError):
                    claim_issue(api, 1, "worker/b")
                self.assertEqual(api.comments, [])

    def test_concurrent_loser_does_not_start(self):
        api = FakeGitHub()
        api.rival_on_claim = True
        with self.assertRaisesRegex(ClaimError, "another worker won"):
            claim_issue(api, 1, "worker/a")
        self.assertEqual(status(api, 1)["claim"]["token"], B)
        self.assertTrue(status(api, 1)["claimed_label"])

    def test_last_status_read_cannot_return_another_workers_token(self):
        cases = [
            {"state": "open", "claimed_label": True, "claim": {"token": B}},
            {"state": "closed", "claimed_label": False, "claim": None},
            {"state": "open", "claimed_label": False, "claim": {"token": A}},
        ]
        for replacement in cases:
            with self.subTest(replacement=replacement):
                with patch("issue_claim.status", return_value=replacement):
                    with self.assertRaisesRegex(ClaimError, "changed before confirmation"):
                        claim_issue(FakeGitHub(), 1, "worker/a")

    def test_heartbeat_cannot_report_a_replacement_as_its_own_claim(self):
        api = FakeGitHub([comment(1, "claim")], ["claimed"])
        with patch("issue_claim.status", return_value={"state": "open", "claim": {"token": B}}):
            with self.assertRaisesRegex(ClaimError, "changed during heartbeat"):
                update_claim(api, 1, A, "heartbeat")

    def test_release_preserves_unrelated_labels(self):
        api = FakeGitHub([comment(1, "claim")], ["claimed", "help wanted"])
        result = update_claim(api, 1, A, "release", "Preserved partial work on plate/test")
        self.assertIsNone(result["claim"])
        self.assertFalse(result["claimed_label"])
        self.assertEqual(api.issue["labels"], [{"name": "help wanted"}])

    def test_old_token_cannot_clear_replacement_claim(self):
        api = FakeGitHub(
            [comment(1, "claim"), comment(2, "release"), comment(3, "claim", B, "worker/b")],
            ["claimed"],
        )
        with self.assertRaisesRegex(ClaimError, "does not own"):
            update_claim(api, 1, A, "release")
        self.assertEqual(api.label_writes, [])
        self.assertEqual(len(api.comments), 3)

    def test_late_release_reconciles_a_new_workers_label(self):
        api = FakeGitHub([comment(1, "claim")], ["claimed"])
        api.rival_on_remove = True
        result = update_claim(api, 1, A, "release", "Handed back")
        self.assertEqual(result["claim"]["token"], B)
        self.assertTrue(result["claimed_label"])
        self.assertEqual(api.label_writes, [False, True])

    def test_staleness_is_only_a_flag_not_a_release(self):
        api = FakeGitHub([comment(1, "claim")], ["claimed"])
        result = status(api, 1, datetime(2026, 10, 24, 19, tzinfo=timezone.utc))
        self.assertTrue(result["stale"])
        self.assertTrue(result["claimed_label"])
        self.assertEqual(result["claim"]["token"], A)
        self.assertEqual(api.label_writes, [])

    def test_bad_owner_cannot_write(self):
        api = FakeGitHub()
        with self.assertRaises(ClaimError):
            claim_issue(api, 1, "worker\nwith-markup")
        self.assertEqual(api.comments, [])


if __name__ == "__main__":
    unittest.main()
