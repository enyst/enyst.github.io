"""Replay the catalog contrast review on the exact reviewed, disposable checkout.

Run npm ci --ignore-scripts and npm run make-i18n first, then execute this file
from a clean ff7cb14a8 checkout. It restores the three source files on exit.
"""
import json
import os
from pathlib import Path
import subprocess
import sys

head = "ff7cb14a8b3e7a0b75bde36ead162340d2cf4cf6"
if subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip() != head:
    raise SystemExit(f"Use a clean detached checkout of {head}")
subprocess.run(["git", "diff", "--quiet", "HEAD"], check=True)
root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd() / "catalog-contrast-report"
root.mkdir(parents=True, exist_ok=True)
test = Path("__tests__/themes/color-themes.test.tsx")
badge = Path("src/components/features/skills/build-skill-pills.tsx")
toggle = Path("src/components/shared/buttons/circle-plus-check-toggle.tsx")
originals = {p: p.read_bytes() for p in (test, badge, toggle)}

def replace(path, before, after):
    source = path.read_text()
    if source.count(before) != 1:
        raise RuntimeError(f"Expected one match in {path}: {before}")
    path.write_text(source.replace(before, after, 1))

def run(name, expected_success):
    report = root / f"{name}.jsonl"
    report.write_text("")
    env = dict(os.environ, CATALOG_CONTRAST_REPORT=str(report))
    with (root / f"{name}.log").open("w") as output:
        result = subprocess.run(
            ["node", "node_modules/vitest/vitest.mjs", "run", str(test)],
            env=env, stdout=output, stderr=subprocess.STDOUT,
        )
    if (result.returncode == 0) != expected_success:
        raise RuntimeError(f"Unexpected test result. Read {name}.log.")
    rows = [json.loads(line) for line in report.read_text().splitlines()]
    if not rows:
        raise RuntimeError(f"No observations in {name}.jsonl")
    print(name, len(rows), "observed", "exit", result.returncode, flush=True)
    return rows

try:
    replace(test, 'import { readFileSync } from "node:fs";', 'import { appendFileSync, readFileSync } from "node:fs";')
    replace(test, '          const ink = paint(sample.ink);\n', '''          const ink = paint(sample.ink);
          appendFileSync(process.env.CATALOG_CONTRAST_REPORT!, JSON.stringify({
            theme: _key,
            appearance: theme.appearance,
            surfaceRole,
            sample: sample.name,
            emittedInk: sample.ink,
            emittedBackground: sample.background,
            inkRgb: ink.color.map((channel) => channel * 255),
            tintRgb: background.color.map((channel) => channel * 255),
            tintAlpha: background.alpha,
            surfaceRgb: card.map((channel) => channel * 255),
            compositeRgb: surface.map((channel) => channel * 255),
            ratio: contrast(luminance(ink.color), luminance(surface)),
            threshold: sample.minimum,
          }) + "\\n");
''')
    baseline = run("as-reviewed", True)
    assert len({(x["theme"], x["surfaceRole"], x["sample"]) for x in baseline}) == 72
    assert sum(x["appearance"] == "dark" for x in baseline) == 36

    replace(badge, "dark:border-feedback-error/35 dark:bg-feedback-error/4 dark:text-feedback-error",
            "dark:border-[rgba(248,113,113,0.35)] dark:bg-[rgba(248,113,113,0.12)] dark:text-[#fca5a5]")
    replace(toggle, "dark:bg-feedback-error/14 dark:text-feedback-error dark:hover:bg-feedback-error/24 dark:hover:text-feedback-error",
            "dark:bg-[rgba(248,113,113,0.14)] dark:text-[#ef4444] dark:hover:bg-[rgba(248,113,113,0.24)] dark:hover:text-[#ef4444]")
    revert = run("restore-main-dark-colors", False)
    assert any(x["appearance"] == "dark" and x["ratio"] < x["threshold"] for x in revert)
    badge.write_bytes(originals[badge])
    toggle.write_bytes(originals[toggle])

    replace(badge, "dark:bg-feedback-error/4", "dark:bg-feedback-error")
    opaque = run("opaque-dark-badge", False)
    assert any(x["sample"] == "manual-only text" and x["ratio"] == 1 for x in opaque)
    badge.write_bytes(originals[badge])
    assert len(run("restored", True)) == 72
finally:
    for file, original in originals.items():
        file.write_bytes(original)
