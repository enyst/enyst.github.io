# Codex instructions

This repository is Engel's Notebook (`enyst.github.io`). The user gives Codex standing authorization to commit and push changes directly to `main` for work in this repository without asking again. Follow any task-specific instruction that overrides this permission.

Before pushing, check the working tree for unrelated changes, incorporate newer `origin/main` commits, verify the relevant changes, and confirm the push result.

## Agent attribution in page source

Whenever an agent creates or edits an HTML page, include one machine-readable
attribution comment near the beginning of the page, using this exact marker
and valid JSON (no trailing commas):

```html
<!-- notebook-attribution: {"version":1,"contributions":[{"agent":"<agent name>","llm":"<verified model name or ID>","date":"YYYY-MM-DD","role":"author"}]} -->
```

- Keep the marker `notebook-attribution:` and field names stable for importers.
  `version` is the schema version; `contributions` is an array of contributions.
- Every contribution includes `agent`, `llm`, `date` and `role`. Use the agent's
  name and the actual LLM name/version or model ID. If the LLM cannot be
  verified, use JSON `null`; never guess from the agent or product name.
- Use an ISO `YYYY-MM-DD` date and role `author` for original writing or
  `editor` for revisions. Importing or formatting another author's work does
  not make the agent its original author.
- Preserve existing author/source credits and earlier contribution entries.
  Add new contributions to the existing array rather than replacing its history
  or adding a second attribution block. Do not invent attribution for older work.
- Generated pages must emit and preserve the same comment through their owning
  generator, so regeneration does not erase provenance.

Keep this data in the HTML comment. This rule adds no visible byline or label;
Liberty Labs and other consumers decide how to present the attribution.
