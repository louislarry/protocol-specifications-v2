#!/usr/bin/env python3
"""
update_readme.py — Regenerate docs/README.md "Suggested Order of Reading" from
scripts/reading_order.env.

Source of truth:
    scripts/reading_order.env — ordered list of filenames (relative to docs/).

For each filename in the order file, the script:
    1. Reads the document's NFH-ID and Title from its Document Details.
    2. Looks up the existing description in docs/README.md (matched by filename).
       If no description exists, inserts a TODO placeholder.
    3. Emits the entry as `**N. [NFH-NNN — Title](./Filename.md)**\\n<description>`.

The script does NOT generate or rewrite descriptions — those are human-curated
prose. It only enforces order, numbering, title freshness, and completeness.

Exit codes:
    0 — README regenerated successfully (no TODO placeholders remain).
    1 — README regenerated, but one or more entries still carry a TODO
        placeholder (a human must write the description before committing).
    2 — Hard error (missing files, malformed input).

Usage:
    python3 scripts/update_readme.py
"""

import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
DOCS_DIR = os.path.join(REPO_ROOT, 'docs')
ORDER_FILE = os.path.join(SCRIPT_DIR, 'reading_order.env')
README = os.path.join(DOCS_DIR, 'README.md')

ID_RE = re.compile(r'\*\*ID:?\*\*\s*\|?\s*(NFH-\d+)')
TODO_MARKER = 'TODO: add a one- or two-sentence description placing this document in the reading order.'


def read_order():
    """Return list of (filename, title) tuples from the env file."""
    if not os.path.exists(ORDER_FILE):
        print(f'ERROR: order file not found: {ORDER_FILE}', file=sys.stderr)
        sys.exit(2)
    entries = []
    with open(ORDER_FILE) as f:
        for lineno, line in enumerate(f, start=1):
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue
            if '|' not in stripped:
                print(f'ERROR: scripts/reading_order.env:{lineno}: '
                      f'line missing `|` separator: {stripped!r}', file=sys.stderr)
                sys.exit(2)
            filename, title = stripped.split('|', 1)
            entries.append((filename.strip(), title.strip()))
    return entries


def doc_nfh_id(filename):
    """Return the NFH-NNN ID extracted from the doc's Document Details, or raise."""
    path = os.path.join(DOCS_DIR, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f'docs/{filename} listed in reading_order.env but does not exist')
    with open(path) as f:
        content = f.read()
    id_match = ID_RE.search(content)
    if not id_match:
        raise ValueError(f'docs/{filename} has no **ID:** NFH-NNN line in Document Details')
    return id_match.group(1)


def parse_existing_descriptions(readme_content):
    """Map filename -> description text from the existing README.

    Matches the existing format: `**N. [NFH-NNN — Title](./Filename.md)**\\n<description>`
    The description runs to the next blank line.
    """
    descriptions = {}
    # Pattern: capture filename and the following description block (until blank line).
    pattern = re.compile(
        r'\*\*\d+\.\s*\[NFH-\d+[^\]]*?\]\(\./(?P<filename>[^)]+)\)\*\*\n(?P<desc>.+?)(?=\n\s*\n|\Z)',
        re.DOTALL,
    )
    for m in pattern.finditer(readme_content):
        descriptions[m.group('filename')] = m.group('desc').strip()
    return descriptions


def render_section(order, existing_descriptions):
    """Return (new_section_text, todo_filenames)."""
    lines = []
    todo_filenames = []
    for idx, (filename, title) in enumerate(order, start=1):
        nfh_id = doc_nfh_id(filename)
        description = existing_descriptions.get(filename)
        if not description or TODO_MARKER in description:
            description = TODO_MARKER
            todo_filenames.append(filename)
        lines.append(f'**{idx}. [{nfh_id} — {title}](./{filename})**')
        lines.append(description)
        lines.append('')
    # Strip trailing blank.
    while lines and lines[-1] == '':
        lines.pop()
    return '\n'.join(lines), todo_filenames


def update_readme(new_section):
    if not os.path.exists(README):
        print(f'ERROR: {README} not found', file=sys.stderr)
        sys.exit(2)
    with open(README) as f:
        content = f.read()

    # Replace from the "#### Suggested Order of Reading" heading up to the
    # next horizontal rule or end of file.
    header = '#### Suggested Order of Reading'
    if header not in content:
        print(f'ERROR: "{header}" heading not found in docs/README.md', file=sys.stderr)
        sys.exit(2)

    # Capture intro paragraph(s) between the header and the first entry, so we
    # don't lose them on regeneration.
    section_re = re.compile(
        r'(####\s+Suggested Order of Reading\n\n)'
        r'(?P<intro>.*?)(?=\*\*\d+\.)'
        r'(?P<body>\*\*\d+\..*?)(?=\n---|\Z)',
        re.DOTALL,
    )
    m = section_re.search(content)
    if not m:
        # No existing numbered body — just append after the header.
        intro = ''
        replacement = f'{header}\n\n{new_section}\n\n'
        new_content = content.replace(f'{header}\n', replacement, 1)
    else:
        intro = m.group('intro')
        replacement = f"{m.group(1)}{intro}{new_section}\n"
        new_content = content[:m.start()] + replacement + content[m.end():]

    if new_content != content:
        with open(README, 'w') as f:
            f.write(new_content)
        return True
    return False


def main():
    order = read_order()
    if not order:
        print('ERROR: scripts/reading_order.env is empty', file=sys.stderr)
        return 2

    try:
        with open(README) as f:
            existing_descriptions = parse_existing_descriptions(f.read())
    except OSError:
        existing_descriptions = {}

    try:
        new_section, todo_filenames = render_section(order, existing_descriptions)
    except (FileNotFoundError, ValueError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 2

    changed = update_readme(new_section)
    status = 'UPDATED' if changed else 'NO CHANGE'
    print(f'{status} docs/README.md ({len(order)} entries)')

    if todo_filenames:
        print()
        print('The following entries have placeholder descriptions and MUST be filled in:')
        for fn in todo_filenames:
            print(f'  - {fn}')
        print()
        print('Edit docs/README.md to replace each TODO line with a curated 1–2 sentence description.')
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
