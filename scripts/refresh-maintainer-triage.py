#!/usr/bin/env python3
"""Refresh the fixed maintainer PR queue from official GitHub metadata.

Preserves the original cohort, audit assessments and evidence. Reads PR states,
reviews, current-head checks, and complete linked-issue timelines; never submits
GitHub reviews, comments, closures or merges. Run build-maintainer-reports.py
--only triage afterwards to render the updated snapshot.
"""
import argparse
import concurrent.futures
import copy
import datetime as dt
import json
import os
from pathlib import Path
import time
import urllib.error
import urllib.request
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
SOURCE_FIELDS = """number title url state isDraft mergedAt closedAt updatedAt
author{login} repository{nameWithOwner}"""
REVIEW_FIELDS = """url state submittedAt author{login} commit{oid}"""
CHECK_FIELDS = """__typename ...on CheckRun{name status conclusion startedAt
completedAt detailsUrl checkSuite{app{id slug} workflowRun{workflow{databaseId}}}}
...on StatusContext{context state createdAt targetUrl}"""
PR_FIELDS = SOURCE_FIELDS + """ createdAt headRefOid baseRefOid mergeable
mergeStateStatus reviewDecision mergedBy{login}
reviews(first:100){pageInfo{hasNextPage endCursor}nodes{%s}}
commits(last:1){nodes{commit{oid statusCheckRollup{state
contexts(first:100){pageInfo{hasNextPage endCursor}nodes{%s}}}}}}
""" % (REVIEW_FIELDS, CHECK_FIELDS)
EVENT_FIELDS = """__typename ...on ClosedEvent{createdAt closer{__typename
...on PullRequest{%s}}} ...on ReopenedEvent{createdAt}
...on CrossReferencedEvent{createdAt source{__typename ...on PullRequest{%s}}}
""" % (SOURCE_FIELDS, SOURCE_FIELDS)
ISSUE_FIELDS = """number title url state stateReason closedAt updatedAt author{login}
timelineItems(first:100,itemTypes:[CLOSED_EVENT,REOPENED_EVENT,CROSS_REFERENCED_EVENT]){
pageInfo{hasNextPage endCursor}nodes{%s}}
""" % EVENT_FIELDS


def utcnow():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def graphql(query):
    token = os.environ.get("GITHUB_TOKEN_ENYST") or os.environ.get("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("Set GITHUB_TOKEN_ENYST or GITHUB_TOKEN; credentials are never printed.")
    request = urllib.request.Request("https://api.github.com/graphql",
        data=json.dumps({"query": query}).encode(), headers={
            "Authorization": "Bearer " + token, "Content-Type": "application/json",
            "User-Agent": "maintainer-triage-refresh"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                result = json.load(response)
            if result.get("errors"):
                raise RuntimeError("GraphQL response errors: " + json.dumps(result["errors"]))
            return result["data"]
        except (urllib.error.URLError, TimeoutError) as error:
            if attempt == 3:
                raise RuntimeError("GitHub metadata fetch failed: " + str(error)) from error
            time.sleep(2 ** attempt)


def repo_query(repo, selection):
    owner, name = repo.split("/")
    return "{repository(owner:%s,name:%s){%s}}" % (json.dumps(owner), json.dumps(name), selection)


def paginate(repo, number, kind, field, connection, fields, extra=""):
    nodes = list(connection["nodes"])
    while connection["pageInfo"]["hasNextPage"]:
        after = json.dumps(connection["pageInfo"]["endCursor"])
        selection = "%s(number:%d){%s(first:100,after:%s%s){pageInfo{hasNextPage endCursor}nodes{%s}}}" % (
            kind, number, field, after, extra, fields)
        connection = graphql(repo_query(repo, selection))["repository"][kind][field]
        nodes.extend(connection["nodes"])
    return {"pageInfo": connection["pageInfo"], "nodes": nodes}


def fetch_objects(repo, numbers, kind):
    numbers = sorted(set(numbers))
    fields = ISSUE_FIELDS if kind == "issue" else PR_FIELDS
    batches = [numbers[i:i + 6] for i in range(0, len(numbers), 6)]

    def fetch_batch(batch):
        selection = " ".join("item%d:%s(number:%d){%s}" % (n, kind, n, fields) for n in batch)
        result = graphql(repo_query(repo, selection))["repository"]
        if any(value is None for value in result.values()):
            raise RuntimeError("A tracked GitHub object is unavailable; dataset was not updated.")
        return list(result.values())

    values = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        for batch in executor.map(fetch_batch, batches):
            values.extend(batch)

    for value in values:
        number = value["number"]
        if kind == "issue":
            value["timelineItems"] = paginate(repo, number, kind, "timelineItems", value["timelineItems"],
                EVENT_FIELDS, ",itemTypes:[CLOSED_EVENT,REOPENED_EVENT,CROSS_REFERENCED_EVENT]")
        else:
            value["reviews"] = paginate(repo, number, kind, "reviews", value["reviews"], REVIEW_FIELDS)
            commits = value["commits"]["nodes"]
            if not commits:
                raise RuntimeError("Tracked PR #%d has no current commit." % number)
            if commits[0]["commit"]["oid"] != value["headRefOid"]:
                raise RuntimeError("Head changed while reading PR #%d; rerun the refresh." % number)
            rollup = commits[0]["commit"]["statusCheckRollup"]
            if rollup:
                connection = rollup["contexts"]
                nodes = list(connection["nodes"])
                while connection["pageInfo"]["hasNextPage"]:
                    after = json.dumps(connection["pageInfo"]["endCursor"])
                    query = "pullRequest(number:%d){headRefOid commits(last:1){nodes{commit{statusCheckRollup{contexts(first:100,after:%s){pageInfo{hasNextPage endCursor}nodes{%s}}}}}}}" % (number, after, CHECK_FIELDS)
                    page = graphql(repo_query(repo, query))["repository"]["pullRequest"]
                    if page["headRefOid"] != value["headRefOid"]:
                        raise RuntimeError("Head changed during check pagination for #%d." % number)
                    connection = page["commits"]["nodes"][0]["commit"]["statusCheckRollup"]["contexts"]
                    nodes.extend(connection["nodes"])
                rollup["contexts"] = {"pageInfo": connection["pageInfo"], "nodes": nodes}
    return {value["number"]: value for value in values}


def simple_pr(pr):
    return {"number": pr["number"], "title": pr["title"], "url": pr["url"],
        "state": pr["state"].lower(), "draft": pr["isDraft"],
        "author": (pr.get("author") or {}).get("login", "deleted"),
        "merged_at": pr["mergedAt"], "closed_at": pr["closedAt"],
        "repository": pr["repository"]["nameWithOwner"]}


def closing_and_reference_prs(issue):
    closers, referenced = [], {}
    last_transition = None
    for event in issue["timelineItems"]["nodes"]:
        if event["__typename"] in ("ClosedEvent", "ReopenedEvent"):
            last_transition = event
        source = event.get("closer") or event.get("source")
        if source and source.get("__typename") == "PullRequest":
            item = simple_pr(source)
            referenced[(item["repository"], item["number"])] = item
    if issue["state"] == "CLOSED" and last_transition and last_transition["__typename"] == "ClosedEvent":
        closer = last_transition.get("closer")
        if closer and closer.get("__typename") == "PullRequest" and closer["state"] == "MERGED":
            closers = [simple_pr(closer)]
    return closers, list(referenced.values())


def checked_ci(pr, checked_at):
    rollup = pr["commits"]["nodes"][0]["commit"]["statusCheckRollup"]
    latest = {}
    for check in rollup["contexts"]["nodes"] if rollup else []:
        if check["__typename"] == "CheckRun":
            suite = check.get("checkSuite") or {}
            app = suite.get("app") or {}
            workflow = (suite.get("workflowRun") or {}).get("workflow") or {}
            key = ("run", app.get("id"), workflow.get("databaseId"), check["name"])
            timestamp = check.get("startedAt") or check.get("completedAt") or ""
        else:
            key = ("context", check["context"])
            timestamp = check.get("createdAt") or ""
        if key not in latest or timestamp >= latest[key][0]:
            latest[key] = (timestamp, check)
    failures, pending, cancelled, checks = [], False, False, []
    for timestamp, check in latest.values():
        is_run = check["__typename"] == "CheckRun"
        name = check["name"] if is_run else check["context"]
        state = check.get("conclusion") if is_run else check["state"]
        if is_run and check["status"] != "COMPLETED" or not is_run and state in ("PENDING", "EXPECTED"):
            pending = True
        elif state in ("FAILURE", "ERROR", "TIMED_OUT", "ACTION_REQUIRED", "STALE"):
            failures.append(name)
        elif state == "CANCELLED":
            cancelled = True
        suite = check.get("checkSuite") or {}
        checks.append({"name": name, "state": state, "status": check.get("status"), "time": timestamp,
            "workflow_id": ((suite.get("workflowRun") or {}).get("workflow") or {}).get("databaseId"),
            "app": (suite.get("app") or {}).get("slug"),
            "url": check.get("detailsUrl") or check.get("targetUrl")})
    state = "FAILURE" if failures else "PENDING" if pending else "CANCELLED" if cancelled else "SUCCESS" if latest else None
    metadata_names = ("validate pr description", "cleanup-on-approval", "agentcanvas-status-sync", "label", "claude", "review", "copilot")
    metadata_only = bool(checks) and all(any(token in c["name"].lower() for token in metadata_names) for c in checks)
    result = {"state": state, "github_rollup": rollup["state"] if rollup else None,
        "head_sha": pr["headRefOid"], "failed": sorted(set(failures)), "checked_at": checked_at,
        "metadata_only": metadata_only, "latest_checks": checks}
    if failures and all(name == "Validate PR description" for name in failures):
        result["detail"] = "PR-description validation."
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit-output", default="/workspace/maintainer-triage-refresh-summary.json")
    parser.add_argument("--cache-output", default="/workspace/maintainer-triage-refresh-api.json")
    args = parser.parse_args()
    path = ROOT / "assets/openhands-maintainer-reports/triage.json"
    before = json.loads(path.read_text())
    data = copy.deepcopy(before)
    records = data["records"]
    numbers = {r["pr"] for r in records}
    if len(numbers) != len(records):
        raise RuntimeError("Duplicate PR in the frozen queue.")
    repo = data["repository"]
    started = utcnow()
    prs = fetch_objects(repo, numbers, "pullRequest")
    print("Fetched tracked PR metadata, reviews and current-head checks:", len(prs), flush=True)
    issues = fetch_objects(repo, {r["issue"] for r in records}, "issue")
    print("Fetched linked issues and complete timelines:", len(issues), flush=True)
    alternatives = {r["alternative"]["number"] for r in records if r.get("alternative")} - numbers
    extra_prs = fetch_objects(repo, alternatives, "pullRequest") if alternatives else {}
    finished = utcnow()
    pr_changes, issue_changes, head_changes, superseded = [], {}, [], []
    all_prs = {**prs, **extra_prs}
    for row, old in zip(records, before["records"]):
        pr = prs[row["pr"]]
        issue = issues[row["issue"]]
        state = pr["state"].lower()
        row.setdefault("original_decision", old["decision"])
        row.setdefault("original_group", old["group"])
        row.setdefault("original_reason", old["reason"])
        row.setdefault("original_audit_head_sha", old.get("head_sha"))
        row.setdefault("retained_assessment_reason", old["reason"])
        row.setdefault("original_audit_caveats", old.get("audit_caveats", []))
        row.setdefault("assessment_source_at", before.get("original_audit_prepared_at"))
        if old["state"] != state:
            pr_changes.append({"pr": row["pr"], "before": old["state"], "after": state})
        if old["issue_state"] != issue["state"].lower():
            issue_changes[row["issue"]] = {"issue": row["issue"], "before": old["issue_state"], "after": issue["state"].lower()}
        if old["head_sha"] != pr["headRefOid"]:
            head_changes.append({"pr": row["pr"], "before": old["head_sha"], "after": pr["headRefOid"]})
        row.update(pr_author=(pr.get("author") or {}).get("login", "deleted"), pr_title=pr["title"],
            pr_url=pr["url"], state=state, draft=pr["isDraft"], head_sha=pr["headRefOid"],
            base_sha=pr["baseRefOid"], created_at=pr["createdAt"], updated_at=pr["updatedAt"],
            merged_at=pr["mergedAt"], closed_at=pr["closedAt"],
            merged_by=(pr.get("mergedBy") or {}).get("login"), metadata_checked_at=finished,
            head_matches_original_audit=pr["headRefOid"] == row["original_audit_head_sha"],
            head_matches_previous_snapshot=pr["headRefOid"] == old["head_sha"],
            mergeable={"MERGEABLE": True, "CONFLICTING": False}.get(pr["mergeable"]),
            mergeable_state=pr["mergeStateStatus"].lower() if pr["mergeStateStatus"] else "unknown",
            review_decision=pr["reviewDecision"], ci=checked_ci(pr, finished),
            issue_author=(issue.get("author") or {}).get("login", "deleted"),
            issue_title=issue["title"], issue_url=issue["url"], issue_state=issue["state"].lower(),
            issue_state_reason=issue["stateReason"], issue_closed_at=issue["closedAt"],
            issue_metadata_checked_at=finished)
        reviews = [{"url": r["url"], "state": r["state"],
            "author": (r.get("author") or {}).get("login", "deleted"), "submitted_at": r["submittedAt"],
            "head_sha": (r.get("commit") or {}).get("oid"),
            "on_current_head": (r.get("commit") or {}).get("oid") == pr["headRefOid"]}
            for r in pr["reviews"]["nodes"]]
        row["reviews"] = reviews
        row["current_head_reviews"] = [r for r in reviews if r["on_current_head"]]
        closers, referenced = closing_and_reference_prs(issue)
        row["issue_closing_prs"] = closers
        row["issue_referenced_prs"] = referenced
        if row.get("alternative"):
            row["alternative"] = simple_pr(all_prs[row["alternative"]["number"]])
        if state != "open":
            row["decision"] = "archive"
            row["group"] = "merged" if state == "merged" else "already-closed"
            row["reason_label"] = "Archive status"
            row["reason"] = ("Merged on %s." % pr["mergedAt"] if state == "merged" else "Closed without merge on %s." % pr["closedAt"]) + " Linked issue #%d is %s." % (row["issue"], row["issue_state"])
            row["refresh_note"] = "Archived using current GitHub state; the earlier decision and source/evidence assessments remain in the dataset."
        else:
            row["decision"] = row["original_decision"]
            row["group"] = row["original_group"]
            row["reason_label"] = "Why keep" if row["decision"] == "keep" else "Closure reason"
            if row["decision"] == "close" and closers and closers[0]["number"] != row["pr"]:
                closer = closers[0]
                row["reason"] = "Linked issue #%d is closed by merged PR #%d (%s). This still-open proposal is superseded; close without merge. No changes from this proposal will be reused." % (row["issue"], closer["number"], closer["author"])
                row["alternative"] = closer
                row["preserve_pr"] = closer["number"]
                row["refresh_note"] = "GitHub’s latest issue-closing event identifies merged PR #%d as the closer. The original audit and evidence remain historical; this refresh did not verify product behavior or submit a closure." % closer["number"]
                superseded.append({"pr": row["pr"], "issue": row["issue"], "closing_pr": closer["number"]})
            else:
                # Retain existing technical findings; only remove stale assertions of
                # unchanged GitHub heads/states from prior metadata refresh prose.
                row["refresh_note"] = "The earlier audit recommendation and its evidence limits are retained. Current issue/PR state, reviews and checks were read from GitHub; no code or runtime verification was performed."
                if row.get("independent_verification"):
                    finding = row["independent_verification"]
                    row["refresh_note"] += " The earlier independent verdict %s applies to head %s; current GitHub review decision is %s." % (finding.get("verdict", "recorded"), finding.get("head_sha", "unrecorded"), pr["reviewDecision"] or "unrecorded")
        if not row["head_matches_original_audit"]:
            row["refresh_note"] += " The current head differs from the originally audited head and is independently unverified by this metadata refresh."
            if state == "open" and not (row["decision"] == "close" and closers):
                row["reason"] = "Historical assessment at head %s: %s Current head %s has not been independently reviewed by this metadata refresh." % (
                    row["original_audit_head_sha"], row["retained_assessment_reason"], row["head_sha"])
            row["audit_caveats"] = [
                "The following source and runtime assessment limits belong to the originally audited head, not a fresh verification of the current head."
            ] + [text.replace("current ", "then-current ").replace("Current ", "Then-current ")
                 for text in row["original_audit_caveats"]]
            if row.get("independent_verification"):
                row["review_status"] = "unverified-changed-head"
    assert {r["pr"] for r in records} == numbers
    assert len(records) == len(before["records"])
    assert all(r["original_decision"] == old.get("original_decision", old["decision"]) for r, old in zip(records, before["records"]))
    assert all(r.get("evidence_urls") == old.get("evidence_urls") for r, old in zip(records, before["records"]))
    keep = sum(r["state"] == "open" and r["decision"] == "keep" for r in records)
    close = sum(r["state"] == "open" and r["decision"] == "close" for r in records)
    merged = sum(r["state"] == "merged" for r in records)
    closed = sum(r["state"] == "closed" for r in records)
    data["counts"] = {"keep": keep, "close": close, "merged": merged, "already_closed": closed,
        "total_open": keep + close, "total_original": len(records)}
    assert keep + close + merged + closed == len(records)
    data["group_counts"] = dict(Counter(r["group"] for r in records))
    issue_states = {r["issue"]: r["issue_state"] for r in records}
    data["issue_counts"] = {"distinct_closed_issues": sum(s == "closed" for s in issue_states.values()),
        "distinct_open_issues": sum(s == "open" for s in issue_states.values())}
    data["open_pr_issue_states"] = {"linked_issue_closed": sum(r["state"] == "open" and r["issue_state"] == "closed" for r in records),
        "linked_issue_open": sum(r["state"] == "open" and r["issue_state"] == "open" for r in records)}
    data["heads_changed"] = sum(not r["head_matches_original_audit"] for r in records)
    data.update(previous_snapshot_observed_at=before.get("observed_at"), snapshot_anchor=finished,
        observed_at=finished, metadata_observed_from=started, metadata_observed_until=finished,
        github_actions_taken=False)
    data["method"] = "Refreshed every PR in the original fixed cohort and every distinct linked issue through official GitHub GraphQL: current state/draft/head/dates, complete formal reviews with commit identity, latest current-head CI contexts, and fully paginated issue reference, closure and reopening events. Original audit decisions, reasons, dates and evidence are retained; changed heads are explicitly unverified. No code or runtime behavior was exercised, and no GitHub comments, reviews, closures or merges were submitted."
    update = "Official API recheck of the original %d-PR queue: %d Keep, %d Close, %d merged and %d closed without merge. %d PR state changes, %d linked-issue state changes and %d head changes since the previous snapshot. Original evidence and audit decisions are retained; the Close policy remains independent replacement with no reuse." % (len(records), keep, close, merged, closed, len(pr_changes), len(issue_changes), len(head_changes))
    data.setdefault("updates", []).append({"at": finished, "text": update})
    summary = {"fetch_started_at": started, "fetch_finished_at": finished, "counts": data["counts"],
        "issue_counts": data["issue_counts"], "open_pr_issue_states": data["open_pr_issue_states"],
        "heads_different_from_original_audit": data["heads_changed"], "pr_state_changes": pr_changes,
        "issue_state_changes": list(issue_changes.values()), "head_changes": head_changes,
        "superseded_open_proposals": superseded, "cohort_and_original_evidence_preserved": True,
        "github_actions_taken": False, "prose_review_required": True}
    Path(args.cache_output).write_text(json.dumps({"fetch_started_at": started, "fetch_finished_at": finished,
        "prs": list(prs.values()), "issues": list(issues.values()), "additional_alternative_prs": list(extra_prs.values())}, indent=2) + "\n")
    Path(args.audit_output).write_text(json.dumps(summary, indent=2) + "\n")
    temporary = path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    temporary.replace(path)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
