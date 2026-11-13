"""Pure, intentionally conservative GitHub release/checklist transformations.

The canonical manual-test state lives in one public GitHub Issue.  A new release
may add test cases, but it must never replace existing lines or reset checkboxes.
"""

from __future__ import annotations

import re
from typing import Any


BEGIN = "<!-- STREAMEN_TEST_BACKLOG_BEGIN -->"
END = "<!-- STREAMEN_TEST_BACKLOG_END -->"
INDEX_BEGIN = "<!-- STREAMEN_RELEASE_ROWS_BEGIN -->"
INDEX_END = "<!-- STREAMEN_RELEASE_ROWS_END -->"
TEST_ID = re.compile(r"^T[0-9]{2,4}$")
VERSION = re.compile(r"^v[0-9]+\.[0-9]+(?:\.[0-9]+)?(?:-[A-Za-z0-9.-]+)?$")
TEST_LINE = re.compile(
    r"^- \[(?P<checked>[ xX])\] \*\*(?P<id>T[0-9]{2,4}) – (?P<title>[^*]+)\*\*",
    re.MULTILINE,
)


def _public_text(value: Any, name: str, limit: int = 500) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{name} must be text")
    value = " ".join(value.split())
    if not value or len(value) > limit or any(c in value for c in "<>\r\n"):
        raise ValueError(f"invalid {name}")
    # No Markdown/HTML injection into the automatically published public text.
    if any(c in value for c in "[]*`|\\"):
        raise ValueError(f"unsafe Markdown in {name}")
    if "github.com/burnhardbot/stream" in value.lower():
        raise ValueError(f"private issue link in {name}")
    return value


def validate_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(manifest, dict):
        raise ValueError("manifest must be an object")
    version = manifest.get("version")
    if not isinstance(version, str) or not VERSION.fullmatch(version):
        raise ValueError("invalid release version")
    build_id = _public_text(manifest.get("build_id"), "build_id", 100)
    status = manifest.get("status")
    if status != "prepared":
        raise ValueError("GitHub-only publication must remain prepared, not installed")
    changes = manifest.get("changes")
    if not isinstance(changes, list) or not changes or len(changes) > 100:
        raise ValueError("changes must be a nonempty list")
    clean_changes = [_public_text(c, "change", 250) for c in changes]
    tests = manifest.get("manual_tests")
    if not isinstance(tests, list) or len(tests) > 200:
        raise ValueError("manual_tests must be a list")
    seen = set()
    clean_tests = []
    for item in tests:
        if not isinstance(item, dict):
            raise ValueError("test case must be an object")
        ident = item.get("id")
        if not isinstance(ident, str) or not TEST_ID.fullmatch(ident) or ident in seen:
            raise ValueError("invalid or duplicate test ID")
        seen.add(ident)
        clean_tests.append(
            {
                "id": ident,
                "title": _public_text(item.get("title"), f"{ident}.title", 100),
                "description": _public_text(
                    item.get("description"), f"{ident}.description", 500
                ),
            }
        )
    return {
        "version": version,
        "build_id": build_id,
        "status": status,
        "changes": clean_changes,
        "manual_tests": clean_tests,
    }


def existing_tests(issue_body: str) -> dict[str, tuple[str, bool]]:
    if not isinstance(issue_body, str):
        raise ValueError("issue body missing")
    found: dict[str, tuple[str, bool]] = {}
    for match in TEST_LINE.finditer(issue_body):
        ident = match.group("id")
        if ident in found:
            raise ValueError(f"duplicate existing test ID: {ident}")
        found[ident] = (match.group("title").strip(), match.group("checked").lower() == "x")
    return found


def merge_continuous_checklist(issue_body: str, manifest: dict[str, Any]) -> str:
    """Append new test IDs; preserve EVERY old line, unchecked item and status."""
    if issue_body.count(BEGIN) != 1 or issue_body.count(END) != 1:
        raise ValueError("expected exactly one managed checklist section")
    start = issue_body.index(BEGIN) + len(BEGIN)
    end = issue_body.index(END)
    if end <= start:
        raise ValueError("malformed checklist marker order")
    old = existing_tests(issue_body)
    additions: list[str] = []
    for test in manifest["manual_tests"]:
        ident, title = test["id"], test["title"]
        if ident in old:
            if old[ident][0] != title:
                raise ValueError(f"{ident} already means something else; choose a new ID")
            continue
        additions.append(
            f"- [ ] **{ident} – {title}**: {test['description']} "
            f"_(hinzugefügt für {manifest['version']})_"
        )
    if not additions:
        return issue_body
    managed = issue_body[start:end].rstrip()
    managed += "\n" + "\n".join(additions) + "\n"
    return issue_body[:start] + managed + issue_body[end:]


def set_test_result(issue_body: str, test_id: str, status: str) -> str:
    """Apply only one manually authorized result; all other checkboxes survive."""
    if not TEST_ID.fullmatch(test_id) or status not in {"PASS", "FAIL", "BLOCKIERT"}:
        raise ValueError("invalid test result")
    found = existing_tests(issue_body)
    if test_id not in found:
        raise ValueError("unknown test ID")
    pattern = re.compile(
        rf"^- \[[ xX]\] (?=\*\*{re.escape(test_id)} – )", re.MULTILINE
    )
    replacement = "- [x] " if status == "PASS" else "- [ ] "
    updated, count = pattern.subn(replacement, issue_body)
    if count != 1:
        raise ValueError("test checkbox not found exactly once")
    return updated


def render_changelog(manifest: dict[str, Any], checklist_url: str) -> str:
    lines = [
        f"# STREAMEN {manifest['version']} – Changelog",
        "",
        "> 🟡 **VORBEREITET, NOCH NICHT ALS INSTALLIERT BESTÄTIGT.**",
        "",
        f"**Version:** {manifest['version']}  ",
        f"**Build-ID:** {manifest['build_id']}  ",
        "**Installationsstatus:** Nicht durch Win10-Readback bestätigt",
        "",
        "## Änderungen",
        "",
    ]
    lines.extend(f"- {change}" for change in manifest["changes"])
    lines.extend(
        [
            "",
            "## Manuelle Abnahme",
            "",
            f"Die [fortlaufende öffentliche Testliste]({checklist_url}) enthält "
            "auch alle aus früheren Updates noch offenen Prüfungen.",
            "Neue Prüfungen aus diesem Release werden ergänzend dort eingetragen; "
            "kein alter Haken wird still überschrieben.",
            "",
            "**Automatische Tests und echte Installation sind separat nachzuweisen.**",
            "",
        ]
    )
    return "\n".join(lines)


def merge_release_index(index_body: str, manifest: dict[str, Any], checklist_url: str) -> str:
    if index_body.count(INDEX_BEGIN) != 1 or index_body.count(INDEX_END) != 1:
        raise ValueError("expected exactly one release-index marker pair")
    start = index_body.index(INDEX_BEGIN) + len(INDEX_BEGIN)
    end = index_body.index(INDEX_END)
    if end <= start:
        raise ValueError("bad index marker order")
    changelog = f"{manifest['version']}-changelog.md"
    if changelog in index_body:
        return index_body  # idempotent rerun, preserving existing rows
    row = (
        f"| **{manifest['version']}** | [Änderungen]({changelog}) | "
        f"[Fortlaufende Tests]({checklist_url}) | 🟡 Vorbereitet |"
    )
    return index_body[:start] + "\n" + row + index_body[start:]
