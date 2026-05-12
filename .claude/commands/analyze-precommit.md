---
name: analyze-precommit
description: Run the pre-commit hook against the current staged changes, capture its output, and write a structured analysis with recommended fixes to an uncommitted, untracked file at `.claude/scratch/precommit-report.md`. Use this when a commit was just blocked by the pre-commit hook, or proactively before committing to surface issues without aborting a commit.
---

# Analyze the Pre-Commit Hook Output

This skill captures the output of `scripts/hooks/pre-commit` against the currently staged changes, parses what failed, and writes a structured report with actionable next steps to a gitignored scratch file. The report is for **the user's local diagnosis only** — it MUST NOT be committed.

## Procedure

### 1. Ensure the scratch directory exists and is gitignored

```bash
mkdir -p .claude/scratch
grep -qxF '.claude/scratch/' .gitignore 2>/dev/null || echo '.claude/scratch/' >> .gitignore
```

The `.claude/scratch/` path is already gitignored at the repo level; this step is idempotent and safe.

### 2. Run the hook in capture mode

Run the canonical hook script directly so the output is captured without affecting the user's working tree:

```bash
scripts/hooks/pre-commit 2>&1 | tee .claude/scratch/precommit-raw.log
HOOK_EXIT_CODE=${PIPESTATUS[0]}
```

The `--no-verify` shortcut is NOT used — the point of this skill is to surface what the hook says, not to bypass it.

### 3. Parse the output

The hook reports two distinct check phases:

- **TOC check** — emitted by `scripts/check_toc.py`. Lines starting with `✗ STALE <filename>` indicate TOC drift. The hook will have already auto-fixed and re-staged these; no user action needed for them.
- **Docs index check** — emitted by `scripts/check_docs_index.py`. Lines `MISS` next to either `README` or `Summary` indicate missing index entries. These require manual edits via the `/update-readme` skill before the commit will succeed.

### 4. Write the structured report

Write the report to `.claude/scratch/precommit-report.md` with sections:

```markdown
# Pre-commit hook report — <ISO timestamp>

## Hook exit code
<0 = clean, 1 = blocked>

## Auto-fixed (no action required)
- List the files whose TOC the hook regenerated, if any.

## Action required
- For each docs index miss, name the file and the index(es) it is missing from.
- For each unexpected failure, summarise the error.

## Recommended next steps
- Numbered list of concrete commands to run (e.g. `Invoke /update-readme`, `Edit docs/README.md to insert entry for ...`).
- End with: re-run `git commit` to retry.

## Raw hook output
<verbatim contents of .claude/scratch/precommit-raw.log>
```

Keep the report scannable — the user reads this to decide what to do next, not to digest the entire hook output.

### 5. Hand back to the user

Print the path to the report (`.claude/scratch/precommit-report.md`) so the user can open it. Do NOT stage, add, or commit the report — it lives only as a working note.
