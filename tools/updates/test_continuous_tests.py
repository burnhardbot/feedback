import unittest

from continuous_tests import (
    BEGIN,
    END,
    INDEX_BEGIN,
    INDEX_END,
    existing_tests,
    merge_continuous_checklist,
    merge_release_index,
    render_changelog,
    set_test_result,
    validate_manifest,
)


CHECKLIST = (
    "# Fortlaufende Tests\n"
    "- [x] **T01 – OBS**: geprüft\n"
    "- [ ] **T02 – Twitch**: noch offen\n"
    + BEGIN
    + "\n<!-- Nur neue Fälle hier -->\n"
    + END
    + "\n## Kommentare\nbleiben erhalten\n"
)
INDEX = (
    "| Version | Changelog | Testliste | Status |\n"
    "| --- | --- | --- | --- |\n"
    + INDEX_BEGIN
    + "\n| **v1.3** | [Änderungen](v1.3-changelog.md) | [Tests](#) | Vorbereitung |\n"
    + INDEX_END
    + "\nHistorie bleibt\n"
)


def manifest(version, tests):
    return validate_manifest(
        {
            "version": version,
            "build_id": "release-sha-abc123",
            "status": "prepared",
            "changes": ["Verbesserter Status auf der Übersicht"],
            "manual_tests": [
                {"id": test_id, "title": title, "description": "Manuell in OBS prüfen"}
                for test_id, title in tests
            ],
        }
    )


class ContinuousChecklistTests(unittest.TestCase):
    def test_unchecked_survives_multiple_updates(self):
        first = merge_continuous_checklist(
            CHECKLIST, manifest("v1.3.1", [("T03", "Minigame")])
        )
        second = merge_continuous_checklist(
            first, manifest("v1.3.2", [("T04", "Panorama")])
        )
        self.assertIn("- [ ] **T02 – Twitch**: noch offen", second)
        self.assertIn("- [x] **T01 – OBS**: geprüft", second)
        self.assertIn("- [ ] **T03 – Minigame**", second)
        self.assertIn("- [ ] **T04 – Panorama**", second)
        self.assertEqual(second.count("**T03 –"), 1)
        self.assertTrue(second.endswith("## Kommentare\nbleiben erhalten\n"))

    def test_no_duplicate_after_retry(self):
        m = manifest("v1.3.1", [("T03", "Minigame")])
        first = merge_continuous_checklist(CHECKLIST, m)
        self.assertEqual(merge_continuous_checklist(first, m), first)

    def test_collision_needs_new_id(self):
        with self.assertRaisesRegex(ValueError, "already means something else"):
            merge_continuous_checklist(CHECKLIST, manifest("v1.3.1", [("T02", "OBS")]))

    def test_manual_result_updates_exactly_one_item(self):
        passed = set_test_result(CHECKLIST, "T02", "PASS")
        self.assertIn("- [x] **T02 – Twitch**", passed)
        self.assertIn("- [x] **T01 – OBS**", passed)
        failed = set_test_result(passed, "T02", "FAIL")
        self.assertIn("- [ ] **T02 – Twitch**", failed)
        self.assertIn("- [x] **T01 – OBS**", failed)

    def test_unknown_result_refused(self):
        with self.assertRaisesRegex(ValueError, "unknown test ID"):
            set_test_result(CHECKLIST, "T99", "PASS")

    def test_duplicate_existing_id_refused(self):
        broken = CHECKLIST.replace(END, "- [ ] **T02 – Dublette**\n" + END)
        with self.assertRaisesRegex(ValueError, "duplicate existing"):
            existing_tests(broken)

    def test_missing_markers_do_not_overwrite(self):
        with self.assertRaisesRegex(ValueError, "managed checklist section"):
            merge_continuous_checklist("- [ ] **T01 – A**", manifest("v1.3.1", []))

    def test_changelog_is_prepared_not_installed(self):
        page = render_changelog(manifest("v1.3.1", []), "https://example.org/tests")
        self.assertIn("NICHT ALS INSTALLIERT BESTÄTIGT", page)
        self.assertIn("fortlaufende öffentliche Testliste", page)

    def test_index_preserves_old_versions_and_is_idempotent(self):
        m = manifest("v1.3.1", [])
        next_index = merge_release_index(INDEX, m, "https://example.org/tests")
        self.assertIn("v1.3-changelog.md", next_index)
        self.assertIn("v1.3.1-changelog.md", next_index)
        self.assertEqual(merge_release_index(next_index, m, "https://example.org/tests"), next_index)

    def test_unsafe_or_fake_deployment_manifest_rejected(self):
        with self.assertRaises(ValueError):
            validate_manifest(
                {"version": "v1.3.1", "build_id": "abc", "status": "installed", "changes": ["OK"], "manual_tests": []}
            )
        with self.assertRaises(ValueError):
            manifest("v1.3.1", [("T03", "[private](https://github.com/burnhardbot/stream)")])


if __name__ == "__main__":
    unittest.main()
