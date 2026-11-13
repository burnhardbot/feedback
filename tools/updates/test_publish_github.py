"""No network calls: verify end-to-end publication and cumulative manual checks."""

import unittest

from publish_github import CHECKLIST, INDEX, publish
from continuous_tests import BEGIN, END, INDEX_BEGIN, INDEX_END


class FakeGitHub:
    def __init__(self):
        self.issue = {
            "state": "open",
            "body": f"# Dauerhafte Liste\n- [ ] **T01 – Alt**: offen\n{BEGIN}\n{END}\n",
        }
        self.files = {INDEX: (f"# Updates\n{INDEX_BEGIN}\n{INDEX_END}\n", "sha-initial")}
        self.calls = []

    def request(self, method, route, payload=None):
        self.calls.append((method, route))
        if method == "GET" and route == "/issues/16":
            return dict(self.issue)
        if method == "PATCH" and route == "/issues/16":
            self.issue["body"] = payload["body"]
            return dict(self.issue)
        raise AssertionError(f"unexpected {method} {route}")

    def file(self, path):
        return self.files.get(path)

    def put_file(self, path, content, message, sha=None):
        original = self.files.get(path)
        if original and original[1] != sha:
            raise ValueError("stale SHA")
        self.files[path] = (content, f"new-sha-{len(self.calls)}")


def manifest(version, ident):
    return {
        "version": version,
        "build_id": "prepared-not-installed",
        "status": "prepared",
        "changes": ["Neuer öffentlicher Testlauf vorbereitet."],
        "manual_tests": [
            {"id": ident, "title": "Bildprüfung", "description": "Bild im OBS live prüfen."}
        ],
    }


class PublicationTests(unittest.TestCase):
    def test_unchecked_survives_multiple_releases_and_reruns(self):
        gh = FakeGitHub()
        publish(gh, manifest("v1.3.1", "T11"))
        self.assertIn("- [ ] **T01 – Alt**", gh.issue["body"])
        self.assertIn("- [ ] **T11 – Bildprüfung**", gh.issue["body"])
        gh.issue["body"] = gh.issue["body"].replace("- [ ] **T11", "- [x] **T11")
        publish(gh, manifest("v1.3.2", "T12"))
        publish(gh, manifest("v1.3.2", "T12"))
        body = gh.issue["body"]
        self.assertEqual(body.count("**T11 –"), 1)
        self.assertEqual(body.count("**T12 –"), 1)
        self.assertIn("- [ ] **T01 – Alt**", body)
        self.assertIn("- [x] **T11 – Bildprüfung**", body)
        self.assertIn("- [ ] **T12 – Bildprüfung**", body)
        self.assertIn(CHECKLIST, gh.files[INDEX][0])

    def test_changelog_collision_refuses_to_touch_issue(self):
        gh = FakeGitHub()
        prior = manifest("v1.3.1", "T11")
        publish(gh, prior)
        before = gh.issue["body"]
        modified = manifest("v1.3.1", "T12")
        with self.assertRaises(ValueError):
            publish(gh, modified)
        self.assertEqual(gh.issue["body"], before)

    def test_closed_permanent_issue_blocks_publishing(self):
        gh = FakeGitHub()
        gh.issue["state"] = "closed"
        with self.assertRaises(ValueError):
            publish(gh, manifest("v1.3.1", "T11"))
        self.assertEqual(len(gh.files), 1)


if __name__ == "__main__":
    unittest.main()
