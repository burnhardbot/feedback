#!/usr/bin/env python3
"""Publish prepared public changelogs and append to ONE permanent test issue.

GitHub-only: this script never deploys or claims that a build runs on Win10.
Its GitHub token must have contents:write and issues:write in the public repo.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
from pathlib import Path
import urllib.error
import urllib.parse
import urllib.request

from continuous_tests import (
    merge_continuous_checklist,
    merge_release_index,
    render_changelog,
    validate_manifest,
)


REPO = "burnhardbot/feedback"
ISSUE = 16
CHECKLIST = f"https://github.com/{REPO}/issues/{ISSUE}"
INDEX = "docs/updates/README.md"


class GitHub:
    def __init__(self, token: str):
        if not token:
            raise ValueError("GITHUB_TOKEN is required")
        self.token = token

    def request(self, method: str, route: str, payload: dict | None = None) -> dict:
        url = "https://api.github.com/repos/" + REPO + route
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": "Bearer " + self.token,
            "User-Agent": "streamen-continuous-manual-tests",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        data = None
        if payload is not None:
            data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            headers["Content-Type"] = "application/json"
        request = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            # Do not log GitHub response bodies, which could contain sensitive data.
            raise RuntimeError(f"GitHub API {method} {route} returned HTTP {exc.code}") from exc

    def file(self, path: str) -> tuple[str, str] | None:
        route = "/contents/" + urllib.parse.quote(path, safe="/")
        try:
            result = self.request("GET", route)
        except RuntimeError as exc:
            if str(exc).endswith("HTTP 404"):
                return None
            raise
        if result.get("encoding") != "base64":
            raise ValueError(f"cannot safely read {path}")
        content = base64.b64decode(result["content"]).decode("utf-8")
        return content, result["sha"]

    def put_file(self, path: str, content: str, message: str, sha: str | None = None) -> None:
        payload: dict = {
            "message": message,
            "content": base64.b64encode(content.encode("utf-8")).decode("ascii"),
            "branch": "main",
        }
        if sha:
            payload["sha"] = sha
        self.request("PUT", "/contents/" + urllib.parse.quote(path, safe="/"), payload)


def publish(github: GitHub, manifest: dict) -> list[str]:
    info = validate_manifest(manifest)
    changelog_path = f"docs/updates/{info['version']}-changelog.md"

    # All three resources are inspected before a single write. An existing
    # changelog with different content is never silently overwritten.
    issue = github.request("GET", f"/issues/{ISSUE}")
    if issue.get("state") != "open":
        raise ValueError("permanent test issue is closed")
    old_body = issue["body"]
    old_index = github.file(INDEX)
    if old_index is None:
        raise ValueError("release index is missing")
    old_changelog = github.file(changelog_path)

    new_body = merge_continuous_checklist(old_body, info)
    new_index = merge_release_index(old_index[0], info, CHECKLIST)
    new_changelog = render_changelog(info, CHECKLIST)
    if old_changelog is not None and old_changelog[0] != new_changelog:
        raise ValueError("existing changelog differs: do not overwrite published history")

    registry_path = "docs/updates/build-registry.json"
    old_registry = github.file(registry_path) if info.get("package_sha256") else None
    registry_content = None
    if info.get("package_sha256"):
        registry = json.loads(old_registry[0]) if old_registry else {"schema":1,"builds":[]}
        if registry.get("schema") != 1 or not isinstance(registry.get("builds"),list):
            raise ValueError("invalid build registry")
        matching = [b for b in registry["builds"] if b["version"]==info["version"] and b["buildId"]==info["build_id"]]
        if matching and (len(matching)!=1 or matching[0]["packageSha256"]!=info["package_sha256"]):
            raise ValueError("immutable build/package collision")
        if not matching:
            registry["builds"].insert(0,{"version":info["version"],"buildId":info["build_id"],"packageSha256":info["package_sha256"],"status":"prepared"})
            registry_content=json.dumps(registry,ensure_ascii=False,indent=2)+"\n"
    changes = []
    if old_changelog is None:
        github.put_file(changelog_path, new_changelog, f"docs: prepared changelog {info['version']}")
        changes.append("changelog created")
    # Re-fetch the issue immediately before any mutation to carry forward the
    # most recent manual checkmarks, even if someone checked a box meanwhile.
    if new_body != old_body:
        latest = github.request("GET", f"/issues/{ISSUE}")
        new_body = merge_continuous_checklist(latest["body"], info)
        if new_body != latest["body"]:
            github.request("PATCH", f"/issues/{ISSUE}", {"body": new_body})
            changes.append("new tests appended to permanent issue")
    if new_index != old_index[0]:
        # A SHA precondition prevents silently overwriting concurrent index edits.
        github.put_file(
            INDEX,
            new_index,
            f"docs: link prepared {info['version']} to permanent test backlog",
            old_index[1],
        )
        changes.append("release index updated")
    if registry_content is not None:
        github.put_file(registry_path,registry_content,"docs: exact prepared build/package registry",old_registry[1] if old_registry else None)
        changes.append("exact build registered")
    return changes


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", help="checked-in docs/updates/manifests/vX.Y.Z.json")
    args = parser.parse_args()
    path = Path(args.manifest)
    expected = Path("docs/updates/manifests")
    if path.parent != expected or not path.name.endswith(".json"):
        parser.error("use a checked-in path under docs/updates/manifests/")
    info = validate_manifest(json.loads(path.read_text(encoding="utf-8")))
    if not info.get("package_sha256"):
        parser.error("new public publication requires the actual package SHA256")
    if path.stem != info["version"]:
        parser.error("manifest filename must equal its version")
    if os.environ.get("GITHUB_REPOSITORY") != REPO:
        parser.error("this publisher runs only in the public feedback repository")
    result = publish(GitHub(os.environ.get("GITHUB_TOKEN", "")), info)
    print(f"Prepared public metadata for {info['version']}; " + (", ".join(result) or "already current"))
    print("NO server deployment was performed. Permanent test list: " + CHECKLIST)


if __name__ == "__main__":
    main()
