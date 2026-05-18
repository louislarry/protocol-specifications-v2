#!/usr/bin/env python3
"""
check_docs_index.py — Verify the RFC docs index across three sources of truth:

  1. scripts/reading_order.env       (ordered list of RFC filenames + display titles)
  2. docs/README.md                  (rendered Suggested Order of Reading section)
  3. docs/RFC_Publication_Summary.md (Index table)

The script enforces:
  - Every RFC document on disk (docs/*.md with a `**ID:** NFH-NNN` line) appears
    in scripts/reading_order.env.
  - Every filename in reading_order.env exists on disk.
  - Every filename in reading_order.env is linked in docs/README.md and in
    docs/RFC_Publication_Summary.md.
  - The "Suggested Order of Reading" section in docs/README.md is in sync with
    reading_order.env (no TODO placeholders, ordering matches). The script does
    NOT regenerate README — it only reports drift. Run scripts/update_readme.py
    to regenerate.

When called with file path arguments (e.g. from the pre-commit hook), only the
listed files are enforced against the indexes. This keeps the hook focused on
staged changes and avoids surfacing pre-existing un-indexed files. The
reading_order.env coverage check, however, always runs against the whole
docs/ tree because that file is the single source of truth.

Exit codes:
    0 — All checks passed.
    1 — One or more checks failed; the script prints a report on what to fix.
"""

import os
import re
import sys
import glob

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
DOCS_DIR = os.path.join(REPO_ROOT, 'docs')
ORDER_FILE = os.path.join(SCRIPT_DIR, 'reading_order.env')
README = os.path.join(DOCS_DIR, 'README.md')
SUMMARY = os.path.join(DOCS_DIR, 'RFC_Publication_Summary.md')

INDEX_FILES = {'README.md', 'RFC_Publication_Summary.md'}
ID_RE = re.compile(r'\*\*ID:?\*\*\s*\|?\s*(NFH-\d+)')
TODO_MARKER = 'TODO: add a one- or two-sentence description'


def read_order():
    """Return a list of (filename, title) tuples from reading_order.env."""
    if not os.path.exists(ORDER_FILE):
        return []
    entries = []
    with open(ORDER_FILE) as f:
        for line in f:
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue
            if '|' not in stripped:
                continue  # malformed; the writer script catches this case
            filename, title = stripped.split('|', 1)
            entries.append((filename.strip(), title.strip()))
    return entries


def is_rfc_doc(filepath):
    name = os.path.basename(filepath)
    if name in INDEX_FILES:
        return False
    try:
        with open(filepath) as f:
            head = f.read(4000)
    except OSError:
        return False
    return bool(ID_RE.search(head))


def linked_in(index_path, doc_name):
    try:
        with open(index_path) as f:
            content = f.read()
    except OSError:
        return False
    return any(p in content for p in (f'(./{doc_name})', f'({doc_name})', f'(docs/{doc_name})'))


def main():
    failures = []

    order_entries = read_order()
    order_filenames = [fn for fn, _ in order_entries]
    order_set = set(order_filenames)

    # 1. Coverage: every RFC doc on disk is in reading_order.env.
    disk_rfcs = sorted(
        os.path.basename(p)
        for p in glob.glob(os.path.join(DOCS_DIR, '*.md'))
        if is_rfc_doc(p)
    )
    missing_from_env = [n for n in disk_rfcs if n not in order_set]
    if missing_from_env:
        failures.append(
            'The following RFC documents exist on disk but are NOT listed in '
            'scripts/reading_order.env:\n  - ' + '\n  - '.join(missing_from_env)
        )

    # 2. Every entry in reading_order.env must exist on disk.
    missing_on_disk = [n for n in order_filenames if not os.path.exists(os.path.join(DOCS_DIR, n))]
    if missing_on_disk:
        failures.append(
            'The following entries in scripts/reading_order.env do not exist on disk:\n'
            '  - ' + '\n  - '.join(missing_on_disk)
        )

    # Decide which subset of order_entries to enforce indexes for:
    if len(sys.argv) > 1:
        target_basenames = {os.path.basename(p) for p in sys.argv[1:]}
        target_entries = [(fn, t) for fn, t in order_entries if fn in target_basenames]
    else:
        target_entries = order_entries

    # 3. Index link check (README + Publication Summary).
    missing_in_readme = []
    missing_in_summary = []
    for filename, _title in target_entries:
        if not os.path.exists(os.path.join(DOCS_DIR, filename)):
            continue  # already reported above
        ok_readme = linked_in(README, filename)
        ok_summary = linked_in(SUMMARY, filename)
        marker = '✓' if ok_readme and ok_summary else '✗'
        print(f'{marker} {filename:40} README:{"OK " if ok_readme else "MISS"} '
              f'Summary:{"OK " if ok_summary else "MISS"}')
        if not ok_readme:
            missing_in_readme.append(filename)
        if not ok_summary:
            missing_in_summary.append(filename)

    if missing_in_readme:
        failures.append(
            'Missing from docs/README.md "Suggested Order of Reading":\n'
            '  - ' + '\n  - '.join(missing_in_readme) + '\n'
            'Run: python3 scripts/update_readme.py'
        )
    if missing_in_summary:
        failures.append(
            'Missing from docs/RFC_Publication_Summary.md "Index" table:\n'
            '  - ' + '\n  - '.join(missing_in_summary) + '\n'
            'Edit the table manually to add the missing rows.'
        )

    # 4. README TODO-placeholder check.
    try:
        with open(README) as f:
            readme_content = f.read()
        if TODO_MARKER in readme_content:
            failures.append(
                'docs/README.md still contains TODO placeholder description(s) '
                'inserted by scripts/update_readme.py. Replace each TODO line '
                'with a curated 1–2 sentence description before committing.'
            )
    except OSError:
        pass

    if failures:
        print()
        for f in failures:
            print(f)
            print()
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
