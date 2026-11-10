#!/usr/bin/env python3
"""One-time import of approved public community Ideas into GitHub Discussions.

This intentionally does NOT create Issues or modify production code.
Requires repo Discussions enabled and GITHUB_TOKEN with discussions: write.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import re
import subprocess
import sys
from urllib.error import HTTPError
from urllib.request import Request, urlopen

API_URL = "https://api.github.com/graphql"

QUERY_REPO = """
query($owner: String!, $name: String!) {
  repository(owner: $owner, name: $name) {
    id
    discussionCategories(first: 100) { nodes { id name slug } }
  }
}
"""

QUERY_DISCUSSIONS = """
query($owner: String!, $name: String!, $category: ID!, $cursor: String) {
  repository(owner: $owner, name: $name) {
    discussions(first: 100, categoryId: $category, after: $cursor) {
      nodes { url body }
      pageInfo { hasNextPage endCursor }
    }
  }
}
"""

MUTATION_CREATE = """
mutation($input: CreateDiscussionInput!) {
  createDiscussion(input: $input) {
    discussion { url number title }
  }
}
"""


def graphql(query: str, variables: dict) -> dict:
    token = os.environ.get("GH_TOKEN")
    if not token:
        raise RuntimeError("GH_TOKEN missing")
    payload = json.dumps({"query": query, "variables": variables}).encode("utf-8")
    request = Request(
        API_URL,
        payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "User-Agent": "streamen-public-feedback-ideas",
        },
    )
    try:
        with urlopen(request, timeout=30) as response:
            result = json.load(response)
    except HTTPError as error:
        raise RuntimeError(f"GitHub GraphQL HTTP {error.code}") from error
    if result.get("errors"):
        raise RuntimeError("GitHub GraphQL errors: " + str(result["errors"]))
    return result["data"]


def get_new_files() -> list[Path]:
    before = os.environ["BEFORE_SHA"]
    after = os.environ["GITHUB_SHA"]
    if not re.fullmatch(r"[0-9a-fA-F]{40}", before) or not re.fullmatch(r"[0-9a-fA-F]{40}", after):
        raise RuntimeError("Invalid git SHA in event")
    completed = subprocess.run(
        ["git", "diff", "--diff-filter=A", "--name-only", before, after, "--", "ideas/inbox/"],
        check=True, capture_output=True, text=True,
    )
    paths = []
    for line in completed.stdout.splitlines():
        path = Path(line)
        if path.parent != Path("ideas/inbox") or path.suffix.lower() != ".md":
            continue
        if not path.is_file() or path.is_symlink():
            continue
        paths.append(path)
    return sorted(paths)


def parse_idea(path: Path) -> tuple[str, str, str]:
    if path.stat().st_size > 20_000:
        raise ValueError(f"Idea file too large: {path}")
    text = path.read_text(encoding="utf-8-sig")
    lines = text.splitlines()
    if len(lines) < 3:
        raise ValueError(f"Missing idea content: {path}")
    match = re.fullmatch(r"# \[OFFEN\] (.+)", lines[0].strip())
    if not match:
        raise ValueError(f"Missing required [OFFEN] heading: {path}")
    if lines[1].strip() != "**Dokument-/Archivstatus:** [OFFEN]":
        raise ValueError(f"Missing required document status: {path}")
    title = match.group(1).strip()
    if not title or len(title) > 200:
        raise ValueError(f"Invalid idea title: {path}")
    body = "\n".join(lines[2:]).strip()
    if len(body) < 20:
        raise ValueError(f"Idea description too short: {path}")
    marker = f"<!-- streamen-idea-source: {path.as_posix()} -->"
    body = body + "\n\n---\n" + marker
    return title, body, marker


def already_exists(owner: str, name: str, category_id: str, marker: str) -> str | None:
    cursor = None
    while True:
        data = graphql(
            QUERY_DISCUSSIONS,
            {"owner": owner, "name": name, "category": category_id, "cursor": cursor},
        )["repository"]["discussions"]
        for node in data["nodes"]:
            if marker in (node.get("body") or ""):
                return node["url"]
        if not data["pageInfo"]["hasNextPage"]:
            return None
        cursor = data["pageInfo"]["endCursor"]


def summary(line: str) -> None:
    print(line)
    filename = os.environ.get("GITHUB_STEP_SUMMARY")
    if filename:
        with open(filename, "a", encoding="utf-8") as output:
            output.write(line + "\n")


def main() -> int:
    repository = os.environ["GITHUB_REPOSITORY"]
    owner, name = repository.split("/", 1)
    paths = get_new_files()
    if not paths:
        summary("No newly added ideas to publish.")
        return 0

    repo = graphql(QUERY_REPO, {"owner": owner, "name": name})["repository"]
    if not repo:
        raise RuntimeError("Repository not found/authorized")
    categories = repo["discussionCategories"]["nodes"]
    category = next(
        (c for c in categories if c["name"].casefold() == "ideas" or c["slug"].casefold() == "ideas"),
        None,
    )
    if not category:
        raise RuntimeError("GitHub Discussions category 'Ideas' does not exist; enable Discussions/create category first.")

    summary("## STREAMEN – neue Ideas-Discussions")
    for path in paths:
        title, body, marker = parse_idea(path)
        existing_url = already_exists(owner, name, category["id"], marker)
        if existing_url:
            summary(f"- Bereits vorhanden: [{title}]({existing_url})")
            continue
        result = graphql(
            MUTATION_CREATE,
            {"input": {"repositoryId": repo["id"], "categoryId": category["id"], "title": title, "body": body}},
        )
        discussion = result["createDiscussion"]["discussion"]
        summary(f"- Neu erstellt: [{discussion['title']}]({discussion['url']})")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
