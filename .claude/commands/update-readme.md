---
name: update-readme
description: Update the docs/README.md "Suggested Order of Reading" and docs/RFC_Publication_Summary.md when a new RFC is added (or when the reading order changes). The reading order is data-driven via scripts/reading_order.env — this skill edits that file, runs the deterministic regenerator script, and walks you through filling in the new entry's description. No LLM call is required for the README rendering itself.
---

# Update README + Publication Summary

This skill is the canonical workflow for keeping the two indexes consistent with the actual set of RFC documents under `docs/`.

The source of truth for reading order is `scripts/reading_order.env`. It is a simple list of entries in the form `Filename.md|Display Title`, one per line. The companion script `scripts/update_readme.py` is a deterministic regenerator: it reads the env file, looks up each doc's NFH-ID from its Document Details block, preserves any existing curated description in `docs/README.md`, and writes a fresh "Suggested Order of Reading" section. Curated descriptions are NEVER overwritten by the script — only their placement and the entry's NFH-ID/title are updated.

## When to invoke this skill

- A new RFC document was just added under `docs/`.
- The reading order needs to change (e.g. a new doc fits between two existing ones).
- The pre-commit hook reported a docs-index failure or a `TODO` placeholder in README.

## Procedure

### 1. Identify what's missing

```bash
python3 scripts/check_docs_index.py
```

It reports any:
- RFC document on disk that is not yet in `scripts/reading_order.env`.
- env entry that doesn't exist on disk.
- env entry that is missing from `docs/README.md` or `docs/RFC_Publication_Summary.md`.
- `TODO` placeholder description left in `docs/README.md`.

### 2. Edit `scripts/reading_order.env`

For each new doc, insert a line `Filename.md|Display Title` at the correct position in the reading order. The display title is the curated, human-friendly title that should appear in README — it does NOT have to match the document's H1.

When inserting in the middle, no renumbering is needed — the regenerator script computes `**N.**` prefixes from the order in the env file.

### 3. Regenerate `docs/README.md`

```bash
python3 scripts/update_readme.py
```

The script:
- Renders each entry as `**N. [NFH-NNN — Title](./Filename.md)**` followed by its description.
- Preserves existing descriptions that are matched by filename.
- Inserts a `TODO` placeholder line for any new filename that doesn't yet have a description.
- Exits 1 if any TODO placeholder remains, so the pre-commit hook can fail loudly.

### 4. Fill in any TODO descriptions

Open `docs/README.md` and replace each TODO placeholder with a curated 1–2 sentence description that situates the document in the reading order — what it covers and what to read before it.

Do NOT auto-generate this with an LLM in production: write it consciously so the reading order is comprehensible and accurate.

### 5. Update `docs/RFC_Publication_Summary.md`

Append a row to the Index table for the new RFC. Existing rows follow this shape:

```markdown
| [NFH-NNN](./Filename.md) | Title | [Author](https://github.com/handle) | YYYY-MM-DD | Status |
```

Keep the table ordered by NFH-NNN. The status column should reflect the doc's current Document Details status (`Draft` until it reaches Protocol Standard).

### 6. Verify

```bash
python3 scripts/check_docs_index.py
```

It MUST exit 0 (every entry marked `✓`, no failures) before you proceed to commit.

### 7. Hand back to the user

Print the diff for the four touched files (`scripts/reading_order.env`, `docs/README.md`, `docs/RFC_Publication_Summary.md`, and any new RFC under `docs/`). Do NOT commit — the user will stage and commit themselves.
