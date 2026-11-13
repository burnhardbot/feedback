"""Exact package attribution for NEW manual reports; old comments stay historical."""
from __future__ import annotations
import json
import re
from pathlib import Path
from process_test_comment import apply_report, parse_command, allowed_logins, is_valid_event
from continuous_tests import existing_tests, merge_continuous_checklist, BEGIN, END
from publish_github import ISSUE

BUILD = re.compile(r"\bbuild:([A-Za-z0-9._-]{3,120})\s+sha256:([a-f0-9]{64})(?=\s|$)")

def bound_command(body: str, registry: dict) -> dict:
    parsed = parse_command(body)
    match = BUILD.search(body)
    detail = body.split(" – ", 1)[-1] if " – " in body else ""
    if not parsed or not match or len(detail.strip()) < 12:
        raise ValueError("exact build, SHA256 and actual observation required")
    builds = registry.get("builds") if registry.get("schema") == 1 else None
    if not isinstance(builds, list):
        raise ValueError("build registry unavailable")
    candidates = [b for b in builds if b.get("version") == parsed["version"] and b.get("buildId") == match[1] and b.get("packageSha256") == match[2]]
    if len(candidates) != 1:
        raise ValueError("unknown or ambiguous release/build/package")
    return {**parsed, "buildId": match[1], "packageSha256": match[2]}

def apply_bound_report(github, event: dict, roles: dict, registry: dict) -> str:
    if not is_valid_event(event) or event["comment"]["user"]["login"].casefold() not in allowed_logins(roles):
        return "ignored: unauthorized event"
    command = bound_command(event["comment"]["body"], registry)
    # Verify the full current comment, including evidence, build and screenshots.
    from process_test_comment import get_all_comments
    history = get_all_comments(github)
    exact = [c for c in history if c.get("id") == event["comment"]["id"]]
    if len(exact) != 1 or exact[0].get("body", "").strip() != event["comment"]["body"].strip():
        return "ignored: comment edited or not visible"
    applicable=[]
    for other in history:
        if (other.get("user") or {}).get("login", "").casefold() not in allowed_logins(roles):
            continue
        try:
            if bound_command(other.get("body", ""),registry)["id"]==command["id"]:
                applicable.append(other)
        except ValueError:
            continue
    if max(applicable,key=lambda c:(c.get("created_at", ""),c.get("id",0)))["id"]!=event["comment"]["id"]:
        return "ignored: superseded by newer bound report"
    issue = github.request("GET", f"/issues/{ISSUE}")
    if issue.get("state") != "open":
        raise ValueError("canonical checklist is closed")
    old = existing_tests(issue["body"])
    if command["id"] not in old:
        raise ValueError("unknown test ID")
    if command["status"] == "BLOCKIERT" and old[command["id"]][1]:
        return "historical PASS retained: current build not confirmed"
    if command["status"] != "FAIL" or not old[command["id"]][1]:
        return apply_report(github, event, roles)
    # A regression AFTER PASS gets a new stable ID; historical PASS survives.
    marker = f"<!-- STREAMEN_REGRESSION_COMMENT_{event['comment']['id']}:"
    if marker in issue["body"]:
        return "already current: regression appended"
    origin=f"<!-- STREAMEN_REGRESSION_ORIGIN_{command['id']}_{command['packageSha256']}:"
    linked=re.findall(re.escape(origin)+r"(T[0-9]{2,4}) -->",issue["body"])
    if any(ident in old and not old[ident][1] for ident in linked):
        return "already current: existing open regression"
    number = max(int(key[1:]) for key in old) + 1
    if number > 9999:
        raise ValueError("test ID space exhausted")
    ident = f"T{number:02d}"
    manifest = {"version": command["version"], "manual_tests": [{"id": ident, "title": "Regression zu " + command["id"], "description": "Erneuter Fehler nach bestandenem Test. Nachweis: GitHub-Kommentar " + str(event["comment"]["id"]) + "."}]}
    changed = merge_continuous_checklist(issue["body"], manifest)
    changed = changed.replace(END, marker + ident + " -->\n" + origin + ident + " -->\n" + END)
    github.request("PATCH", f"/issues/{ISSUE}", {"body": changed})
    return "updated: appended regression " + ident

def main():
    import os
    from publish_github import GitHub, REPO
    if os.environ.get("GITHUB_REPOSITORY") != REPO:
        raise SystemExit("wrong repository")
    event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text(encoding="utf-8"))
    roles = json.loads(Path("docs/updates/tester-roles.json").read_text(encoding="utf-8"))
    registry = json.loads(Path("docs/updates/build-registry.json").read_text(encoding="utf-8"))
    print(apply_bound_report(GitHub(os.environ.get("GITHUB_TOKEN", "")), event, roles, registry))

if __name__ == "__main__":
    main()
