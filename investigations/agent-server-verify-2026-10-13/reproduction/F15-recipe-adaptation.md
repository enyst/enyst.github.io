# F15 recovery recipe adaptations

Frozen product checkout: `acca181af1f353975965bcf6486e1d0a58f444c0`.

The copied skill lives under `f15-f21-harness/.agents/skills/verify-agent-server/`.
The original checkout is unchanged; every adapted map run explicitly passes
`--checkout /workspace/agent-sdk-verify`.

The commit-history timestamp regex accepts both ISO 8601 UTC `Z` and a numeric
timezone offset. The original recipe incorrectly rejected the valid `Z` shape
before its remaining history assertions ran.

The commit-history recipe declares `Requires: F15.changes-base`, which creates
the feature-branch fixture used by its history check. The frozen map omitted
this selective-run prerequisite. The first supplemental history attempt before
this correction reached a missing branch directory and is a harness result.

The two repository-search error recipes warm `/openapi.json` with a 60-second
CLI request before running the unchanged doctor. Under initial shared CPU load,
the cold schema build exceeded doctor's fixed 10-second request timeout even
though the feature's API assertions passed.

The silent loopback proxy fixture is owned by `helper start` and lives for ten
minutes rather than 90 seconds. This prevents a slow server restart from using
up the fixture's lifetime before the timeout check. The server's own 15-second
request timeout and the recipe's 30-second upper bound stay unchanged.

The special-name and whitespace recipes retain a failed-assertion flag and
continue through their sibling cases before failing the bullet at the end.
This saves evidence for the non-ASCII filename and trailing-blank-line branches
that the original recipes skipped after their first known failure. Each
individual expected result is unchanged.

The adapted map is checked with `control-agent-server map check`; its saved
result is `family-results/f15-f21-adapted-map-check.json`.
