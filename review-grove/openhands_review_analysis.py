#!/usr/bin/env python3
"""Analyze OpenHands PR review volume by reviewer and PR author category.

This script intentionally uses only the Python standard library. It reads the
same reviewer/author classification inputs used by OpenHands/community-pr-dashboard
where possible, then fetches PR reviews from GitHub GraphQL.

Environment:
  SMOLPAWS_TOKEN or GITHUB_TOKEN - GitHub token with access to public repo data;
                                  org membership visibility improves employee detection.

Outputs are written to --output-dir:
  review_analysis_data.json      aggregate data used by the report
  review_events.json             counted review-event rows for target reviewers
  REVIEW_ANALYSIS.md             markdown report with month-over-month graphs/tables
"""

from __future__ import annotations

import argparse
import calendar
import collections
import datetime as dt
import html
import json
import os
import pathlib
import statistics
import sys
import time
import urllib.error
import urllib.request
from typing import Any

API_URL = "https://api.github.com/graphql"
REST_API_URL = "https://api.github.com"
START_MONTH = "2024-03"
START_DATE = "2024-03-01T00:00:00Z"

# Target repositories requested by the user. The public SDK repository is named
# software-agent-sdk; it is the repository referred to as agent-sdk in OpenHands docs.
TARGET_REPOS = [
    "OpenHands/OpenHands",
    "OpenHands/OpenHands-CLI",
    "OpenHands/software-agent-sdk",
    "OpenHands/extensions",
]

# Copied from OpenHands/community-pr-dashboard/config/maintainers.json on 2026-06-01.
DASHBOARD_MAINTAINERS = [
    "malhotra5",
    "rbren",
    "xingyaoww",
    "neubig",
    "csmith49",
    "hieptl",
    "enyst",
    "mamoodi",
    "li-boxuan",
    "raymyers",
    "jpshackelford",
    "tobitege",
]

# Copied from OpenHands/community-pr-dashboard/config/employees.json on 2026-06-01.
DASHBOARD_EMPLOYEE_ALLOWLIST = ["openhands"]
DASHBOARD_EMPLOYEE_DENYLIST: list[str] = []
DASHBOARD_ORGS = ["all-hands-ai", "openhands"]

# User-provided corrections for this analysis.
# csmith49 is also a maintainer, so role display still prefers maintainer.
USER_EMPLOYEE_OVERRIDES = ["tofarr", "csmith49", "aivong-openhands", "juanmichelini"]
# Current org/member signals should not make these authors' PRs org PRs.
AUTHOR_COMMUNITY_OVERRIDES = ["tobitege", "li-boxuan"]
# These authors' PRs should be treated as org PRs even if current membership
# lookup or authorAssociation does not identify them as org members.
AUTHOR_ORG_OVERRIDES = ["enyst", "amanape", "saurya", "hieptl", "raymyers", "chuckbutkus", "mamoodi", "csmith49", "aivong-openhands", "juanmichelini"]

COUNTED_REVIEW_STATES = {"APPROVED", "CHANGES_REQUESTED", "COMMENTED"}
KNOWN_BOT_LOGINS = {"openhands-agent"}


def is_bot_login(login: str | None) -> bool:
    if not login:
        return False
    normalized = login.lower()
    return (
        normalized in KNOWN_BOT_LOGINS
        or "[bot]" in normalized
        or normalized.endswith("-bot")
        or normalized.endswith("_bot")
        or normalized == "dependabot"
    )


def month_key(iso_timestamp: str) -> str:
    return iso_timestamp[:7]


def parse_iso(iso_timestamp: str) -> dt.datetime:
    return dt.datetime.fromisoformat(iso_timestamp.replace("Z", "+00:00"))


def months_between(start_month: str, end_month: str) -> list[str]:
    year, month = map(int, start_month.split("-"))
    end_year, end_m = map(int, end_month.split("-"))
    out = []
    while (year, month) <= (end_year, end_m):
        out.append(f"{year:04d}-{month:02d}")
        month += 1
        if month == 13:
            year += 1
            month = 1
    return out


def now_iso() -> str:
    return dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


class GitHubClient:
    def __init__(
        self,
        token: str,
        cache_dir: pathlib.Path | None = None,
        use_cache: bool = True,
        request_delay_seconds: float = 0.35,
    ) -> None:
        if not token:
            raise RuntimeError("Set SMOLPAWS_TOKEN or GITHUB_TOKEN before running this script")
        self.token = token
        self.cache_dir = cache_dir
        self.use_cache = use_cache
        self.request_delay_seconds = request_delay_seconds
        if self.cache_dir:
            self.cache_dir.mkdir(parents=True, exist_ok=True)

    def graphql(self, query: str, variables: dict[str, Any], cache_key: str | None = None) -> dict[str, Any]:
        cache_path = None
        if self.cache_dir and cache_key:
            cache_path = self.cache_dir / f"{cache_key}.json"
            if self.use_cache and cache_path.exists():
                return json.loads(cache_path.read_text())

        payload = json.dumps({"query": query, "variables": variables}).encode()
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "User-Agent": "OpenHands-review-analysis/1.0",
        }
        for attempt in range(7):
            req = urllib.request.Request(API_URL, data=payload, headers=headers)
            try:
                with urllib.request.urlopen(req, timeout=60) as resp:
                    data = json.loads(resp.read())
            except urllib.error.HTTPError as exc:
                body = exc.read().decode("utf-8", errors="replace")
                secondary_limit = exc.code in {403, 429} and "secondary rate limit" in body.lower()
                if secondary_limit and attempt < 6:
                    sleep_seconds = 60 + attempt * 30
                    print(f"Secondary rate limit hit; sleeping {sleep_seconds}s", file=sys.stderr)
                    time.sleep(sleep_seconds)
                    continue
                if exc.code in {403, 429, 502, 503, 504} and attempt < 6:
                    time.sleep(2**attempt)
                    continue
                raise RuntimeError(f"GitHub GraphQL HTTP {exc.code}: {body[:500]}") from exc
            except Exception:
                if attempt < 6:
                    time.sleep(2**attempt)
                    continue
                raise

            if data.get("errors"):
                messages = "; ".join(err.get("message", str(err)) for err in data["errors"])
                # Retry transient/rate-limit-ish failures.
                if any(s in messages.lower() for s in ["timeout", "rate limit", "something went wrong"]) and attempt < 6:
                    time.sleep(60 if "rate limit" in messages.lower() else 2**attempt)
                    continue
                raise RuntimeError(f"GitHub GraphQL errors: {messages}")

            if cache_path:
                cache_path.write_text(json.dumps(data, indent=2, sort_keys=True))
            if self.request_delay_seconds:
                time.sleep(self.request_delay_seconds)
            return data
        raise RuntimeError("unreachable")


def fetch_org_members(client: GitHubClient, orgs: list[str]) -> tuple[set[str], dict[str, Any]]:
    query = """
    query OrgMembers($org: String!, $cursor: String) {
      organization(login: $org) {
        membersWithRole(first: 100, after: $cursor) {
          totalCount
          pageInfo { hasNextPage endCursor }
          nodes { login }
        }
      }
      rateLimit { remaining cost resetAt }
    }
    """
    members: set[str] = set()
    debug: dict[str, Any] = {}
    for org in orgs:
        org_members: list[str] = []
        cursor = None
        page = 0
        while True:
            data = client.graphql(query, {"org": org, "cursor": cursor}, cache_key=f"org_members_{org}_{page}")
            org_data = data.get("data", {}).get("organization")
            if not org_data:
                debug[org] = {"error": "organization not returned or inaccessible"}
                break
            conn = org_data["membersWithRole"]
            org_members.extend(node["login"] for node in conn["nodes"] if node.get("login"))
            if not conn["pageInfo"]["hasNextPage"]:
                debug[org] = {"totalCount": conn.get("totalCount"), "members": org_members}
                break
            cursor = conn["pageInfo"]["endCursor"]
            page += 1
    for details in debug.values():
        members.update(details.get("members", []))
    return members, debug


def build_reviewer_sets(client: GitHubClient) -> dict[str, Any]:
    org_members, org_debug = fetch_org_members(client, DASHBOARD_ORGS)
    employees = set(org_members)
    employees.update(DASHBOARD_EMPLOYEE_ALLOWLIST)
    employees.update(USER_EMPLOYEE_OVERRIDES)
    for login in DASHBOARD_EMPLOYEE_DENYLIST:
        employees.discard(login)

    maintainers = set(DASHBOARD_MAINTAINERS)
    # Tofarr is explicitly not a maintainer per user note.
    maintainers.discard("tofarr")

    reviewers = sorted((employees | maintainers) - {login for login in employees | maintainers if is_bot_login(login)})
    roles = {}
    for login in reviewers:
        if login in maintainers:
            role = "maintainer"
        elif login in employees:
            role = "employee"
        else:
            role = "unknown"
        roles[login] = role

    return {
        "employees": sorted(employees),
        "maintainers": sorted(maintainers),
        "target_reviewers": reviewers,
        "reviewer_roles": roles,
        "org_members_debug": org_debug,
    }


PR_PAGE_QUERY = """
query PRPage($owner: String!, $name: String!, $cursor: String) {
  repository(owner: $owner, name: $name) {
    nameWithOwner
    createdAt
    pullRequests(states: [OPEN, CLOSED, MERGED], first: 100, after: $cursor, orderBy: {field: CREATED_AT, direction: ASC}) {
      totalCount
      pageInfo { hasNextPage endCursor }
      nodes {
        id
        number
        title
        url
        state
        createdAt
        mergedAt
        authorAssociation
        author { login }
        reviews(first: 100) {
          totalCount
          pageInfo { hasNextPage endCursor }
          nodes {
            author { login }
            authorAssociation
            state
            submittedAt
            url
          }
        }
      }
    }
  }
  rateLimit { remaining cost resetAt }
}
"""

REVIEW_PAGE_QUERY = """
query ReviewPage($id: ID!, $cursor: String) {
  node(id: $id) {
    ... on PullRequest {
      reviews(first: 100, after: $cursor) {
        pageInfo { hasNextPage endCursor }
        nodes {
          author { login }
          authorAssociation
          state
          submittedAt
          url
        }
      }
    }
  }
  rateLimit { remaining cost resetAt }
}
"""


def fetch_all_prs(client: GitHubClient, repo_full_name: str) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    owner, name = repo_full_name.split("/", 1)
    prs: list[dict[str, Any]] = []
    cursor = None
    page = 0
    repo_created_at = None
    total_count = None
    extra_review_pages = 0

    while True:
        print(f"Fetching {repo_full_name} PR page {page + 1}", file=sys.stderr)
        data = client.graphql(
            PR_PAGE_QUERY,
            {"owner": owner, "name": name, "cursor": cursor},
            cache_key=f"prs_{owner}_{name}_{page}",
        )
        repo = data["data"]["repository"]
        repo_created_at = repo["createdAt"]
        conn = repo["pullRequests"]
        total_count = conn["totalCount"]
        for pr in conn["nodes"]:
            reviews_conn = pr["reviews"]
            reviews = list(reviews_conn["nodes"])
            review_cursor = reviews_conn["pageInfo"]["endCursor"]
            review_page = 0
            while reviews_conn["pageInfo"]["hasNextPage"]:
                extra_review_pages += 1
                review_page += 1
                review_data = client.graphql(
                    REVIEW_PAGE_QUERY,
                    {"id": pr["id"], "cursor": review_cursor},
                    cache_key=f"reviews_{owner}_{name}_{pr['number']}_{review_page}",
                )
                reviews_conn = review_data["data"]["node"]["reviews"]
                reviews.extend(reviews_conn["nodes"])
                review_cursor = reviews_conn["pageInfo"]["endCursor"]
            pr["reviews"] = reviews
            prs.append(pr)
        if not conn["pageInfo"]["hasNextPage"]:
            break
        cursor = conn["pageInfo"]["endCursor"]
        page += 1

    meta = {
        "repo": repo_full_name,
        "repo_created_at": repo_created_at,
        "pull_request_total_count": total_count,
        "pull_requests_fetched": len(prs),
        "extra_review_pages": extra_review_pages,
    }
    return prs, meta


def classify_pr_author(pr: dict[str, Any], employees: set[str]) -> str:
    author = (pr.get("author") or {}).get("login")
    association = pr.get("authorAssociation") or "NONE"
    if not author:
        return "unknown"
    if is_bot_login(author):
        return "bot"
    if author in AUTHOR_COMMUNITY_OVERRIDES:
        return "community"
    if author in AUTHOR_ORG_OVERRIDES:
        return "org"
    # Corrected rule for this analysis: collaborator-only PR authors are still
    # community unless included in an explicit override above.
    if author in employees or association in {"MEMBER", "OWNER"}:
        return "org"
    return "community"


def empty_month_counts(months: list[str]) -> dict[str, int]:
    return {m: 0 for m in months}


def aggregate(prs_by_repo: dict[str, list[dict[str, Any]]], reviewer_info: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    employees = set(reviewer_info["employees"])
    target_reviewers = set(reviewer_info["target_reviewers"])
    reviewer_roles = reviewer_info["reviewer_roles"]

    max_month = dt.datetime.now(dt.UTC).strftime("%Y-%m")
    months = months_between(START_MONTH, max_month)

    by_reviewer = {
        login: {
            "reviewer": login,
            "role": reviewer_roles[login],
            "total_reviews": 0,
            "community_pr_reviews": 0,
            "org_pr_reviews": 0,
            "bot_pr_reviews": 0,
            "unknown_pr_reviews": 0,
            "unique_prs_reviewed": 0,
            "community_prs_reviewed": 0,
            "org_prs_reviewed": 0,
            "bot_prs_reviewed": 0,
            "by_repo": {},
            "by_month": {m: {"total": 0, "community": 0, "org": 0, "bot": 0, "unknown": 0} for m in months},
        }
        for login in sorted(target_reviewers)
    }
    by_repo = {repo: {"total": 0, "community": 0, "org": 0, "bot": 0, "unknown": 0} for repo in prs_by_repo}
    by_month = {m: {"total": 0, "community": 0, "org": 0, "bot": 0, "unknown": 0} for m in months}
    pr_author_category_counts = {"community": 0, "org": 0, "bot": 0, "unknown": 0}
    counted_events: list[dict[str, Any]] = []
    unique_pairs: dict[tuple[str, str, int], dict[str, Any]] = {}

    start_dt = parse_iso(START_DATE)
    for repo, prs in prs_by_repo.items():
        for pr in prs:
            pr_category = classify_pr_author(pr, employees)
            if pr_category in pr_author_category_counts:
                pr_author_category_counts[pr_category] += 1
            else:
                pr_author_category_counts["unknown"] += 1
            pr_author = (pr.get("author") or {}).get("login")
            pr_author_assoc = pr.get("authorAssociation") or "NONE"

            for review in pr.get("reviews", []):
                reviewer = (review.get("author") or {}).get("login")
                submitted_at = review.get("submittedAt")
                state = review.get("state")
                if not reviewer or reviewer not in target_reviewers or is_bot_login(reviewer):
                    continue
                if state not in COUNTED_REVIEW_STATES or not submitted_at:
                    continue
                if parse_iso(submitted_at) < start_dt:
                    continue
                m = month_key(submitted_at)
                if m not in by_month:
                    # In case the host clock lags behind GitHub data.
                    months.append(m)
                    by_month[m] = {"total": 0, "community": 0, "org": 0, "bot": 0, "unknown": 0}
                    for payload in by_reviewer.values():
                        payload["by_month"][m] = {"total": 0, "community": 0, "org": 0, "bot": 0, "unknown": 0}
                category_key = pr_category if pr_category in {"community", "org", "bot"} else "unknown"

                row = {
                    "repo": repo,
                    "pr_number": pr["number"],
                    "pr_url": pr["url"],
                    "pr_author": pr_author,
                    "pr_author_association": pr_author_assoc,
                    "pr_author_category": category_key,
                    "reviewer": reviewer,
                    "reviewer_role": reviewer_roles[reviewer],
                    "review_state": state,
                    "submitted_at": submitted_at,
                    "month": m,
                    "review_url": review.get("url"),
                }
                if reviewer == pr_author:
                    continue

                counted_events.append(row)

                stats = by_reviewer[reviewer]
                stats["total_reviews"] += 1
                stats[f"{category_key}_pr_reviews"] += 1
                stats["by_month"][m]["total"] += 1
                stats["by_month"][m][category_key] += 1
                repo_stats = stats["by_repo"].setdefault(repo, {"total": 0, "community": 0, "org": 0, "bot": 0, "unknown": 0})
                repo_stats["total"] += 1
                repo_stats[category_key] += 1
                by_repo[repo]["total"] += 1
                by_repo[repo][category_key] += 1
                by_month[m]["total"] += 1
                by_month[m][category_key] += 1

                pair_key = (repo, reviewer, pr["number"])
                existing = unique_pairs.get(pair_key)
                if existing is None or submitted_at < existing["submitted_at"]:
                    unique_pairs[pair_key] = row

    for row in unique_pairs.values():
        stats = by_reviewer[row["reviewer"]]
        stats["unique_prs_reviewed"] += 1
        stats[f"{row['pr_author_category']}_prs_reviewed"] += 1

    reviewer_totals = sorted(by_reviewer.values(), key=lambda r: (-r["total_reviews"], r["reviewer"]))

    data = {
        "generated_at": now_iso(),
        "methodology": {
            "start_date": START_DATE,
            "target_repos": TARGET_REPOS,
            "review_states_counted": sorted(COUNTED_REVIEW_STATES),
            "primary_metric": "completed GitHub PR review events by target reviewers, excluding self-reviews",
            "secondary_metric": "unique PRs reviewed, counting each reviewer once per PR at their first counted review",
            "classification_source": "OpenHands/community-pr-dashboard employee/maintainer config and PR category criteria",
            "pr_category_rule": "bot authors -> bot (openhands-agent is explicitly a bot); tobitege/li-boxuan author overrides -> community; enyst/amanape/saurya/hieptl/raymyers/chuckbutkus/mamoodi/csmith49/aivong-openhands/juanmichelini author overrides -> org; otherwise employee or authorAssociation in MEMBER/OWNER -> org; collaborator-only and other human authors -> community",
            "user_overrides": {
                "employee_overrides": USER_EMPLOYEE_OVERRIDES,
                "author_community_overrides": AUTHOR_COMMUNITY_OVERRIDES,
                "author_org_overrides": AUTHOR_ORG_OVERRIDES,
            },
        },
        "reviewer_cohort": reviewer_info,
        "months": sorted(months),
        "totals": {
            "review_events": len(counted_events),
            "community_pr_review_events": sum(r["community_pr_reviews"] for r in reviewer_totals),
            "org_pr_review_events": sum(r["org_pr_reviews"] for r in reviewer_totals),
            "bot_pr_review_events": sum(r["bot_pr_reviews"] for r in reviewer_totals),
            "unknown_pr_review_events": sum(r["unknown_pr_reviews"] for r in reviewer_totals),
            "unique_pr_reviewer_pairs": len(unique_pairs),
        },
        "pr_author_category_counts_all_prs_fetched": pr_author_category_counts,
        "by_repo": by_repo,
        "by_month": by_month,
        "reviewers": reviewer_totals,
    }
    return data, counted_events


def sparkline(values: list[int]) -> str:
    ticks = "▁▂▃▄▅▆▇█"
    if not values:
        return ""
    max_v = max(values)
    if max_v <= 0:
        return "·" * len(values)
    return "".join(ticks[round((v / max_v) * (len(ticks) - 1))] if v else "·" for v in values)


def markdown_table(headers: list[str], rows: list[list[Any]]) -> str:
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        out.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return "\n".join(out)


def mermaid_xy(title: str, x_labels: list[str], series: dict[str, list[int]]) -> str:
    # Keep charts readable in GitHub by showing every month but short labels.
    max_y = max([0] + [v for vals in series.values() for v in vals])
    y_top = max(1, int(max_y * 1.1) + 1)
    lines = ["```mermaid", "xychart-beta", f'    title "{title}"']
    lines.append("    x-axis [" + ", ".join(f'"{label}"' for label in x_labels) + "]")
    lines.append(f"    y-axis \"reviews\" 0 --> {y_top}")
    for name, values in series.items():
        lines.append(f"    line \"{name}\" [" + ", ".join(str(v) for v in values) + "]")
    lines.append("```")
    return "\n".join(lines)


def pct(part: int, total: int) -> str:
    return "0.0%" if total == 0 else f"{part / total * 100:.1f}%"


TOP_REVIEWER_COLORS = [
    "#b8b8ff",  # light lavender
    "#64748b",  # slate blue-gray
    "#ff7f0e",  # orange
    "#7bd85a",  # green
    "#b8bec8",  # gray
    "#b87922",  # brown/gold
    "#8fb3ff",  # light blue
    "#ff7b93",  # pink/red
]
TOP_REVIEWER_MARKERS = ["🟪", "🔵", "🟧", "🟩", "⬜", "🟫", "🟦", "🟥"]
CATEGORY_MARKERS = {"community PRs": "🟪", "org PRs": "🔵", "bot PRs": "🟧"}


def get_top_reviewer_color_map(data: dict[str, Any]) -> list[tuple[str, str]]:
    top_reviewers = [r for r in data["reviewers"] if r["total_reviews"] > 0][:8]
    return [(r["reviewer"], TOP_REVIEWER_COLORS[i % len(TOP_REVIEWER_COLORS)]) for i, r in enumerate(top_reviewers)]


def write_top_reviewers_svg(data: dict[str, Any], output_path: pathlib.Path) -> list[tuple[str, str]]:
    """Write an SVG line chart with an in-chart color legend.

    Mermaid's xychart renderer does not expose stable line colors in Markdown,
    so this chart uses explicit colors and prints reviewer names in those exact
    colors below the plot.
    """
    months = data["months"]
    top_reviewers = [r for r in data["reviewers"] if r["total_reviews"] > 0][:8]
    if not top_reviewers:
        output_path.write_text("")
        return []

    series = [(r["reviewer"], [r["by_month"][m]["total"] for m in months]) for r in top_reviewers]
    color_map = [(name, TOP_REVIEWER_COLORS[i % len(TOP_REVIEWER_COLORS)]) for i, (name, _) in enumerate(series)]

    width, height = 1480, 860
    left, right, top, bottom = 80, 40, 70, 230
    plot_w = width - left - right
    plot_h = height - top - bottom
    max_y = max([1] + [value for _, values in series for value in values])
    y_top = max(1, int(max_y * 1.1) + 1)

    def x_pos(index: int) -> float:
        return left + (plot_w * index / max(1, len(months) - 1))

    def y_pos(value: int) -> float:
        return top + plot_h - (plot_h * value / y_top)

    y_ticks = 5
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Top reviewers by monthly review events">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<style>text{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}.title{font-size:24px;font-weight:700}.axis{font-size:12px;fill:#475569}.legend{font-size:17px;font-weight:700}.grid{stroke:#e2e8f0;stroke-width:1}.axis-line{stroke:#64748b;stroke-width:1.2}.line{fill:none;stroke-width:3.2;stroke-linecap:round;stroke-linejoin:round}.dot{stroke:white;stroke-width:1.5}</style>',
        '<text x="80" y="38" class="title" fill="#0f172a">Top reviewers by monthly review events</text>',
    ]

    for tick in range(y_ticks + 1):
        value = round(y_top * tick / y_ticks)
        y = y_pos(value)
        parts.append(f'<line x1="{left}" y1="{y:.1f}" x2="{width-right}" y2="{y:.1f}" class="grid"/>')
        parts.append(f'<text x="{left-12}" y="{y+4:.1f}" class="axis" text-anchor="end">{value}</text>')
    parts.append(f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top+plot_h}" class="axis-line"/>')
    parts.append(f'<line x1="{left}" y1="{top+plot_h}" x2="{width-right}" y2="{top+plot_h}" class="axis-line"/>')
    parts.append(f'<text x="18" y="{top+plot_h/2:.1f}" class="axis" transform="rotate(-90 18 {top+plot_h/2:.1f})" text-anchor="middle">reviews</text>')

    for i, month in enumerate(months):
        x = x_pos(i)
        parts.append(f'<text x="{x:.1f}" y="{top+plot_h+28}" class="axis" text-anchor="end" transform="rotate(-55 {x:.1f} {top+plot_h+28})">{html.escape(month)}</text>')

    for idx, (name, values) in enumerate(series):
        color = TOP_REVIEWER_COLORS[idx % len(TOP_REVIEWER_COLORS)]
        points = " ".join(f"{x_pos(i):.1f},{y_pos(value):.1f}" for i, value in enumerate(values))
        parts.append(f'<polyline class="line" stroke="{color}" points="{points}"/>')
        for i, value in enumerate(values):
            if value:
                parts.append(f'<circle class="dot" cx="{x_pos(i):.1f}" cy="{y_pos(value):.1f}" r="3.4" fill="{color}"/>')

    legend_y = height - 105
    parts.append(f'<text x="{left}" y="{legend_y-34}" class="axis" fill="#334155">Legend: reviewer names are colored with the same fixed colors as their lines.</text>')
    col_w = 330
    for idx, (name, color) in enumerate(color_map):
        col = idx % 4
        row = idx // 4
        x = left + col * col_w
        y = legend_y + row * 42
        safe_name = html.escape(name)
        parts.append(f'<line x1="{x}" y1="{y-6}" x2="{x+38}" y2="{y-6}" stroke="{color}" stroke-width="4" stroke-linecap="round"/>')
        parts.append(f'<circle cx="{x+19}" cy="{y-6}" r="4" fill="{color}" stroke="white" stroke-width="1.5"/>')
        parts.append(f'<text x="{x+50}" y="{y}" class="legend" fill="{color}">{safe_name}</text>')

    parts.append("</svg>")
    output_path.write_text("\n".join(parts) + "\n")
    return color_map


def colored_reviewer_legend(color_map: list[tuple[str, str]]) -> str:
    if not color_map:
        return ""
    items = []
    for index, (name, color) in enumerate(color_map):
        safe_name = html.escape(name)
        marker = TOP_REVIEWER_MARKERS[index % len(TOP_REVIEWER_MARKERS)]
        # GitHub/Gist strips many HTML color attributes. The emoji marker is a
        # fallback that remains colored even if the span style is removed.
        items.append(f'<span style="color:{color}"><strong>{marker} {safe_name}</strong></span>')
    return "<p>" + " &nbsp;•&nbsp; ".join(items) + "</p>"


CATEGORY_COLORS = {
    "community PRs": "#2563eb",
    "org PRs": "#f97316",
    "bot PRs": "#16a34a",
}


def write_review_category_svg(data: dict[str, Any], output_path: pathlib.Path) -> list[tuple[str, str]]:
    months = data["months"]
    by_month = data["by_month"]
    series = {
        "community PRs": [by_month[m]["community"] for m in months],
        "org PRs": [by_month[m]["org"] for m in months],
        "bot PRs": [by_month[m]["bot"] for m in months],
    }
    width, height = 1480, 760
    left, right, top, bottom = 80, 40, 70, 185
    plot_w = width - left - right
    plot_h = height - top - bottom
    max_y = max([1] + [value for values in series.values() for value in values])
    y_top = max(1, int(max_y * 1.1) + 1)

    def x_pos(index: int) -> float:
        return left + (plot_w * index / max(1, len(months) - 1))

    def y_pos(value: int) -> float:
        return top + plot_h - (plot_h * value / y_top)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Review events by PR author category">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<style>text{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}.title{font-size:24px;font-weight:700}.axis{font-size:12px;fill:#475569}.legend{font-size:17px;font-weight:700}.grid{stroke:#e2e8f0;stroke-width:1}.axis-line{stroke:#64748b;stroke-width:1.2}.line{fill:none;stroke-width:3.2;stroke-linecap:round;stroke-linejoin:round}.dot{stroke:white;stroke-width:1.5}</style>',
        '<text x="80" y="38" class="title" fill="#0f172a">Review events by PR author category</text>',
    ]
    for tick in range(6):
        value = round(y_top * tick / 5)
        y = y_pos(value)
        parts.append(f'<line x1="{left}" y1="{y:.1f}" x2="{width-right}" y2="{y:.1f}" class="grid"/>')
        parts.append(f'<text x="{left-12}" y="{y+4:.1f}" class="axis" text-anchor="end">{value}</text>')
    parts.append(f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top+plot_h}" class="axis-line"/>')
    parts.append(f'<line x1="{left}" y1="{top+plot_h}" x2="{width-right}" y2="{top+plot_h}" class="axis-line"/>')
    parts.append(f'<text x="18" y="{top+plot_h/2:.1f}" class="axis" transform="rotate(-90 18 {top+plot_h/2:.1f})" text-anchor="middle">reviews</text>')
    for i, month in enumerate(months):
        x = x_pos(i)
        parts.append(f'<text x="{x:.1f}" y="{top+plot_h+28}" class="axis" text-anchor="end" transform="rotate(-55 {x:.1f} {top+plot_h+28})">{html.escape(month)}</text>')

    color_map = list(CATEGORY_COLORS.items())
    for name, color in color_map:
        values = series[name]
        points = " ".join(f"{x_pos(i):.1f},{y_pos(value):.1f}" for i, value in enumerate(values))
        parts.append(f'<polyline class="line" stroke="{color}" points="{points}"/>')
        for i, value in enumerate(values):
            if value:
                parts.append(f'<circle class="dot" cx="{x_pos(i):.1f}" cy="{y_pos(value):.1f}" r="3.4" fill="{color}"/>')

    legend_y = height - 82
    parts.append(f'<text x="{left}" y="{legend_y-34}" class="axis" fill="#334155">Legend: labels use the same fixed colors as the lines.</text>')
    x = left
    for name, color in color_map:
        safe_name = html.escape(name)
        parts.append(f'<line x1="{x}" y1="{legend_y-6}" x2="{x+38}" y2="{legend_y-6}" stroke="{color}" stroke-width="4" stroke-linecap="round"/>')
        parts.append(f'<circle cx="{x+19}" cy="{legend_y-6}" r="4" fill="{color}" stroke="white" stroke-width="1.5"/>')
        parts.append(f'<text x="{x+50}" y="{legend_y}" class="legend" fill="{color}">{safe_name}</text>')
        x += 280
    parts.append("</svg>")
    output_path.write_text("\n".join(parts) + "\n")
    return color_map



def write_report(data: dict[str, Any], output_path: pathlib.Path, top_reviewer_color_map: list[tuple[str, str]] | None = None) -> None:
    months = data["months"]
    top_reviewer_color_map = top_reviewer_color_map or []
    by_month = data["by_month"]
    reviewer_rows = []
    for r in data["reviewers"]:
        vals = [r["by_month"][m]["total"] for m in months]
        reviewer_rows.append([
            r["reviewer"],
            r["role"],
            r["total_reviews"],
            r["community_pr_reviews"],
            r["org_pr_reviews"],
            r["bot_pr_reviews"],
            r["unique_prs_reviewed"],
            sparkline(vals),
        ])

    repo_rows = []
    for repo, s in data["by_repo"].items():
        repo_rows.append([repo, s["total"], s["community"], s["org"], s["bot"], s["unknown"]])

    monthly_rows = []
    for m in months:
        s = by_month[m]
        monthly_rows.append([m, s["total"], s["community"], s["org"], s["bot"], s["unknown"]])

    top_reviewers = [r for r in data["reviewers"] if r["total_reviews"] > 0][:8]
    top_series = {r["reviewer"]: [r["by_month"][m]["total"] for m in months] for r in top_reviewers}

    total_series = {
        "community PRs": [by_month[m]["community"] for m in months],
        "org PRs": [by_month[m]["org"] for m in months],
        "bot PRs": [by_month[m]["bot"] for m in months],
    }

    totals = data["totals"]
    employees = data["reviewer_cohort"]["employees"]
    maintainers = data["reviewer_cohort"]["maintainers"]
    target_reviewers = data["reviewer_cohort"]["target_reviewers"]

    lines = [
        "# OpenHands reviewer analysis",
        "",
        "_This report was created by an AI agent (OpenHands) on behalf of the user._",
        "",
        f"Generated at: `{data['generated_at']}`",
        "",
        "## Scope and methodology",
        "",
        "Repositories analyzed:",
        *[f"- `{repo}`" for repo in data["methodology"]["target_repos"]],
        "",
        f"Time range: reviews submitted on or after `{data['methodology']['start_date']}`.",
        "",
        "Primary metric: completed GitHub PR review events with state `APPROVED`, `CHANGES_REQUESTED`, or `COMMENTED`, excluding events where `reviewer == PR author`. "
        "Counts are review events, so multiple reviews by the same reviewer on one PR count multiple times. "
        "The report also includes `unique_prs_reviewed`, which counts each reviewer/PR pair once.",
        "",
        "Reviewer cohort: union of employees and maintainers from `OpenHands/community-pr-dashboard`, plus user-provided employee corrections (`tofarr`, `csmith49`, `aivong-openhands`, `juanmichelini`; `tofarr` is not a maintainer). "
        "If a login is both employee and maintainer, it is shown as `maintainer`.",
        "",
        "PR author category rule: bot authors are `bot` (`openhands-agent` is explicitly treated as a bot); PRs authored by `tobitege` or `li-boxuan` are forced to `community`; PRs authored by `enyst`, `amanape`, `saurya`, `hieptl`, `raymyers`, `chuckbutkus`, `mamoodi`, `csmith49`, `aivong-openhands`, or `juanmichelini` are forced to `org`; otherwise authors in the employee set or with `MEMBER` or `OWNER` author association are `org`; collaborator-only and other human authors are `community`.",
        "",
        f"Target reviewers ({len(target_reviewers)}): `{', '.join(target_reviewers)}`",
        "",
        f"Employees used ({len(employees)}): `{', '.join(employees)}`",
        "",
        f"Maintainers used ({len(maintainers)}): `{', '.join(maintainers)}`",
        "",
        "## Headline totals",
        "",
        markdown_table(
            ["Metric", "Count"],
            [
                ["Total counted review events", totals["review_events"]],
                ["Community PR review events", f"{totals['community_pr_review_events']} ({pct(totals['community_pr_review_events'], totals['review_events'])})"],
                ["Org PR review events", f"{totals['org_pr_review_events']} ({pct(totals['org_pr_review_events'], totals['review_events'])})"],
                ["Bot PR review events", f"{totals['bot_pr_review_events']} ({pct(totals['bot_pr_review_events'], totals['review_events'])})"],
                ["Unique reviewer/PR pairs", totals["unique_pr_reviewer_pairs"]],
            ],
        ),
        "",
        "## Reviews by reviewer",
        "",
        markdown_table(
            ["Reviewer", "Role", "Total reviews", "Community PR reviews", "Org PR reviews", "Bot PR reviews", "Unique PRs reviewed", "Monthly sparkline"],
            reviewer_rows,
        ),
        "",
        "## Reviews by repository",
        "",
        markdown_table(["Repository", "Total", "Community", "Org", "Bot", "Unknown"], repo_rows),
        "",
        "## Month-over-month totals",
        "",
        mermaid_xy("Review events by PR author category", months, total_series),
        "",
        '<p><span style="color:#b8b8ff"><strong>🟪 community PRs</strong></span> &nbsp;•&nbsp; <span style="color:#64748b"><strong>🔵 org PRs</strong></span> &nbsp;•&nbsp; <span style="color:#ff7f0e"><strong>🟧 bot PRs</strong></span></p>',
        "",
        markdown_table(["Month", "Total", "Community", "Org", "Bot", "Unknown"], monthly_rows),
        "",
        "## Month-over-month top reviewers",
        "",
        mermaid_xy("Top reviewers by monthly review events", months, top_series) if top_series else "No review activity.",
        "",
        "Legend, in series order (emoji marker remains colored if Gist strips HTML text color):",
        "",
        colored_reviewer_legend(top_reviewer_color_map) if top_reviewer_color_map else "",
        "",
    ]

    lines.extend([
        "## Reproducibility files",
        "",
        "- `openhands_review_analysis.py`: script used to fetch and aggregate the data.",
        "- `review_analysis_data.json`: aggregate JSON backing this report.",
        "- `review_events.json`: individual counted review-event rows for the target reviewer cohort.",
        "",
        "## Notes and caveats",
        "",
        "- GitHub's `authorAssociation` is used as returned by the API at analysis time, with explicit author overrides applied before membership/association checks.",
        "- `COLLABORATOR` author association is intentionally not treated as org membership in this corrected analysis.",
        "- The `all-hands-ai` organization returned no visible members to the token used here; the `openhands` organization returned visible members and dashboard allowlists/overrides were applied.",
        "- Bot-authored PRs are separated from community/org splits, but still shown in totals when target human reviewers reviewed them.",
    ])

    output_path.write_text("\n".join(lines) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="review_analysis_output", help="directory for generated artifacts")
    parser.add_argument("--no-cache", action="store_true", help="ignore existing cache files")
    args = parser.parse_args()

    output_dir = pathlib.Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    cache_dir = output_dir / ".cache"

    token = os.environ.get("SMOLPAWS_TOKEN") or os.environ.get("GITHUB_TOKEN")
    client = GitHubClient(token or "", cache_dir=cache_dir, use_cache=not args.no_cache)

    reviewer_info = build_reviewer_sets(client)
    prs_by_repo: dict[str, list[dict[str, Any]]] = {}
    repo_meta = []
    for repo in TARGET_REPOS:
        prs, meta = fetch_all_prs(client, repo)
        prs_by_repo[repo] = prs
        repo_meta.append(meta)

    data, counted_events = aggregate(prs_by_repo, reviewer_info)
    data["repository_fetch_metadata"] = repo_meta

    (output_dir / "review_analysis_data.json").write_text(json.dumps(data, indent=2, sort_keys=True))
    (output_dir / "review_events.json").write_text(json.dumps(counted_events, indent=2, sort_keys=True))
    top_reviewer_color_map = get_top_reviewer_color_map(data)
    write_report(data, output_dir / "REVIEW_ANALYSIS.md", top_reviewer_color_map)
    print(f"Wrote {output_dir}")
    print(json.dumps(data["totals"], indent=2))


if __name__ == "__main__":
    main()
