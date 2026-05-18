#!/usr/bin/env python3
"""
check_toc.py — Verify that the Table of Contents in each RFC document matches its headings.

Reuses the TOC-generation logic from update_toc.py to compute the expected TOC for each file
and compares it against the actual TOC block in the file. Exits 0 if every file is consistent,
1 if any file is stale.

Usage:
    python3 scripts/check_toc.py                    # check all docs/*.md with a TOC section
    python3 scripts/check_toc.py docs/API.md ...    # check specific files
"""

import os
import re
import sys
import glob

# Reuse the existing helpers from update_toc.py without invoking its CLI.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from update_toc import generate_toc, DOCS_DIR, SKIP_FILES  # noqa: E402


def expected_and_actual(filepath):
    """Return (expected_block, actual_block) or (None, None) if no TOC section in file."""
    with open(filepath) as f:
        content = f.read()

    if '## Table of Contents' not in content:
        return None, None

    lines = content.splitlines()
    entries = generate_toc(lines)
    if not entries:
        return None, None

    expected_block = '## Table of Contents\n\n' + '\n'.join(entries) + '\n'

    m = re.search(
        r'## Table of Contents\n.*?(?=\n## |\Z)',
        content,
        flags=re.DOTALL,
    )
    if not m:
        return expected_block, ''

    actual_block = m.group(0)
    # Normalise trailing newline so comparison is whitespace-stable.
    if not actual_block.endswith('\n'):
        actual_block += '\n'

    return expected_block, actual_block


def check_file(filepath):
    expected, actual = expected_and_actual(filepath)
    if expected is None:
        return 'SKIP', 'no TOC section'
    if expected == actual:
        return 'OK', f'{expected.count(chr(10)) - 2} entries'
    return 'STALE', 'TOC does not match headings'


def main():
    if len(sys.argv) > 1:
        files = sys.argv[1:]
    else:
        files = sorted(glob.glob(os.path.join(DOCS_DIR, '*.md')))
        files = [f for f in files if os.path.basename(f) not in SKIP_FILES]

    stale = []
    for filepath in files:
        name = os.path.basename(filepath)
        status, detail = check_file(filepath)
        marker = {'OK': '✓', 'SKIP': '-', 'STALE': '✗'}[status]
        print(f'{marker} {status:5} {name} ({detail})')
        if status == 'STALE':
            stale.append(filepath)

    if stale:
        print()
        print(f'{len(stale)} file(s) have stale TOC.')
        print('Run: python3 scripts/update_toc.py ' + ' '.join(stale))
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
