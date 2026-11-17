#!/usr/bin/env python3
"""Apply authenticated /test results from public GitHub Issue #16 comments.

Users write comments through GitHub's normal authenticated UI. The dashboard
never handles access tokens. Only explicitly allowlisted GitHub logins may
change checkboxes, and an older event cannot override a newer report.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
import re

from continuous_tests import existing_tests, set_test_result
from publish_github import GitHub, ISSUE, REPO


ROLES_FILE = Path("docs/updates/tester-roles.json")
COMMAND = re.compile(
    r"\A/test\s+(T[0-9]{2,4})\s+(PASS|FAIL|BLOCKIERT)\s+"
    r"(v[0-9]+\.[0-9]+(?:\.[0-9]+)?(?:-[A-Za-z0-9.-]+)?)"
    r"(?=\s|\Z)(.*)\Z",
    flags=re.IGNORECASE | re.DOTALL,
)


def parse_command(body: str) -> dict[str, str] | None:
    if not isinstance(body, str):
        return None
    match = COMMAND.fullmatch(body.strip())
    if not match:
        return None
    detail = match.group(4).strip()
    # No empty or unreplaced dashboard placeholders as "confirmed" evidence.
    if len(detail) < 12 or re.search(r"\[(?:Name|Datum|Gerät/OBS|Beschreibung/Grund)\]", detail, re.IGNORECASE):
        return None
    return {
        "id": match.group(1).upper(),
        "status": match.group(2).upper(),
        "version": match.group(3),
    }


def allowed_logins(roles: dict) -> set[str]:
    candidates = roles.get("authorized_testers")
    if not isinstance(candidates, list) or not candidates or len(candidates) > 20:
        raise ValueError("authorized_testers must be a nonempty list")
    result = set()
    for login in candidates:
        if not isinstance(login, str) or not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?", login):
            raise ValueError("invalid GitHub username")
        result.add(login.casefold())
    return result


def is_valid_event(event: dict) -> bool:
    issue = event.get("issue") or {}
    comment = event.get("comment") or {}
    sender = event.get("sender") or {}
    return (
        event.get("action") == "created"
        and (event.get("repository") or {}).get("full_name") == REPO
        and issue.get("number") == ISSUE
        and "pull_request" not in issue
        and issue.get("state") == "open"
        and isinstance(comment.get("id"), int)
        and isinstance(comment.get("user"), dict)
        and sender.get("login") == comment["user"].get("login")
        and isinstance(comment.get("body"), str)
    )


def get_all_comments(github: GitHub) -> list[dict]:
    comments = []
    for page in range(1, 21):
        current = github.request("GET", f"/issues/{ISSUE}/comments?per_page=100&page={page}")
        if not isinstance(current, list):
            raise ValueError("bad GitHub comments response")
        comments.extend(current)
        if len(current) < 100:
            return comments
    raise RuntimeError("comment history exceeds safe scan limit; no checkbox changed")


def apply_report(github: GitHub, event: dict, roles: dict) -> str:
    if not is_valid_event(event):
        return "ignored: not a created comment on public issue #16"
    authorized = allowed_logins(roles)
    comment = event["comment"]
    username = comment["user"]["login"]
    if username.casefold() not in authorized:
        return "ignored: commenter not authorized for manual test results"
    command = parse_command(comment["body"])
    if command is None:
        return "ignored: no valid /test result with details"

    # Old workflows can finish after new comments arrive; let the latest valid
    # report from an authorized GitHub account decide the test checkbox.
    history = get_all_comments(github)
    applicable = [
        other
        for other in history
        if (other.get("user") or {}).get("login", "").casefold() in authorized
        and (parsed := parse_command(other.get("body", ""))) is not None
        and parsed["id"] == command["id"]
    ]
    if not applicable:
        raise RuntimeError("incoming authorized comment not visible in GitHub history")
    latest = max(applicable, key=lambda c: (c.get("created_at", ""), c.get("id", 0)))
    if latest.get("id") != comment["id"]:
        return "ignored: superseded by newer authorized report"
    if parse_command(latest.get("body", "")) != command:
        return "ignored: GitHub comment was edited after event; post a fresh result"

    issue = github.request("GET", f"/issues/{ISSUE}")
    if issue.get("state") != "open":
        raise ValueError("the canonical test issue was closed")
    body = issue.get("body", "")
    if command["id"] not in existing_tests(body):
        raise ValueError("test ID is unknown; refuse to create or alter other items")
    changed = set_test_result(body, command["id"], command["status"])
    if changed == body:
        return f"already current: {command['id']} {command['status']}"
    github.request("PATCH", f"/issues/{ISSUE}", {"body": changed})
    return f"updated canonical checkbox: {command['id']} {command['status']}"


def main() -> None:
    if os.environ.get("GITHUB_REPOSITORY") != REPO:
        raise SystemExit("wrong GitHub repository")
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    if not event_path:
        raise SystemExit("GitHub Actions event path required")
    event = json.loads(Path(event_path).read_text(encoding="utf-8"))
    roles = json.loads(ROLES_FILE.read_text(encoding="utf-8"))
    print(apply_report(GitHub(os.environ.get("GITHUB_TOKEN", "")), event, roles))


if __name__ == "__main__":
    main()
