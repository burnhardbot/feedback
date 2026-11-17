import unittest

from process_test_comment import apply_report, allowed_logins, parse_command


ROLES = {"authorized_testers": ["laberfeuer"]}


def event(comment_id=100, login="laberfeuer", body="/test T03 PASS v1.3 – geprüft am 13.11.2026 mit OBS"):
    return {
        "action": "created",
        "repository": {"full_name": "burnhardbot/feedback"},
        "issue": {"number": 16, "state": "open"},
        "sender": {"login": login},
        "comment": {"id": comment_id, "user": {"login": login}, "body": body, "created_at": "2026-11-13T14:00:00Z"},
    }


class FakeGitHub:
    def __init__(self, comments=None):
        self.body = "# Dauerhafte Testliste\n- [ ] **T03 – Kamerabild**: prüfen\n- [x] **T04 – Ton**: prüfen\n"
        self.comments = comments or []
        self.patches = []

    def request(self, method, route, payload=None):
        if method == "GET" and route.startswith("/issues/16/comments"):
            page = int(route.split("page=")[-1])
            return self.comments if page == 1 else []
        if method == "GET" and route == "/issues/16":
            return {"state": "open", "body": self.body}
        if method == "PATCH" and route == "/issues/16":
            self.body = payload["body"]
            self.patches.append(payload)
            return {"state": "open", "body": self.body}
        raise AssertionError((method, route))


def comments(*events):
    return [e["comment"] for e in events]


class CommentTests(unittest.TestCase):
    def test_parse_requires_actual_details_not_placeholder(self):
        self.assertEqual(parse_command("/test T03 PASS v1.3 – geprüft am 13.11.2026 in OBS")["status"], "PASS")
        self.assertIsNone(parse_command("/test T03 PASS v1.3"))
        self.assertIsNone(parse_command("/test T03 PASS v1.3 – [Name]"))
        self.assertIsNone(parse_command("/test T03 OK v1.3 – irgendwas"))

    def test_only_configured_user_is_allowed(self):
        e = event(login="internet-besucher")
        gh = FakeGitHub(comments(e))
        self.assertIn("not authorized", apply_report(gh, e, ROLES))
        self.assertEqual(gh.patches, [])
        self.assertEqual(allowed_logins(ROLES), {"laberfeuer"})

    def test_real_pass_sets_only_requested_checkbox(self):
        e = event()
        gh = FakeGitHub(comments(e))
        self.assertIn("updated", apply_report(gh, e, ROLES))
        self.assertIn("- [x] **T03", gh.body)
        self.assertIn("- [x] **T04", gh.body)

    def test_fail_reopens_checked_test(self):
        e = event(body="/test T04 FAIL v1.3 – in OBS wird kein Ton übertragen")
        gh = FakeGitHub(comments(e))
        self.assertIn("updated", apply_report(gh, e, ROLES))
        self.assertIn("- [ ] **T04", gh.body)
        self.assertIn("- [ ] **T03", gh.body)

    def test_old_event_cannot_override_newer_status(self):
        old = event(comment_id=100)
        new = event(comment_id=101, body="/test T03 FAIL v1.3.1 – Kamerabild ist weiterhin eingefroren")
        new["comment"]["created_at"] = "2026-11-13T14:05:00Z"
        gh = FakeGitHub(comments(old, new))
        self.assertIn("superseded", apply_report(gh, old, ROLES))
        self.assertEqual(gh.patches, [])
        self.assertIn("already current", apply_report(gh, new, ROLES))

    def test_wrong_issue_rejected(self):
        e = event()
        e["issue"]["number"] = 8
        gh = FakeGitHub(comments(e))
        self.assertIn("ignored", apply_report(gh, e, ROLES))
        self.assertEqual(gh.patches, [])

    def test_spoofed_sender_rejected(self):
        e = event()
        e["sender"]["login"] = "fake-user"
        gh = FakeGitHub(comments(e))
        self.assertIn("ignored", apply_report(gh, e, ROLES))
        self.assertEqual(gh.patches, [])

    def test_unknown_id_refused(self):
        e = event(body="/test T99 PASS v1.3 – geprüft am 13.11.2026 in OBS")
        gh = FakeGitHub(comments(e))
        with self.assertRaises(ValueError):
            apply_report(gh, e, ROLES)
        self.assertEqual(gh.patches, [])

    def test_edited_comment_does_not_apply_old_event(self):
        original = event()
        changed = event(body="/test T03 FAIL v1.3 – sichtbarer Hänger in OBS")
        gh = FakeGitHub(comments(changed))
        self.assertIn("edited", apply_report(gh, original, ROLES))
        self.assertEqual(gh.patches, [])


if __name__ == "__main__":
    unittest.main()
