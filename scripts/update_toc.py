#!/usr/bin/env python3
"""
update_toc.py — Regenerates the Table of Contents in Beckn Protocol RFC documents.

Usage:
    python3 scripts/update_toc.py              # update all docs/*.md with a TOC section
    python3 scripts/update_toc.py docs/API.md  # update a specific file
"""

import re
import sys
import os
import glob

DOCS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'docs')
SKIP_FILES = {'README.md', 'RFC_Publication_Summary.md'}


def make_anchor(text):
    """Convert heading text to a GitHub-style anchor slug.

    Matches GitHub's actual heading-id algorithm:
      1. Strip inline markdown (keep inner text of bold/italic/code/links).
      2. Lowercase.
      3. Replace each whitespace character with a hyphen (NOT collapsed —
         consecutive whitespace becomes consecutive hyphens, which preserves
         the double-hyphen GitHub emits for headings with em-dashes etc.).
      4. Strip anything that is not a letter, digit, hyphen, or underscore.

    Leading and trailing hyphens are NOT stripped — GitHub keeps them when a
    heading begins or ends with a non-letter character (e.g. emoji, em-dash).
    """
    # 1. Strip inline markdown.
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'\*(.+?)\*', r'\1', text)
    text = re.sub(r'`(.+?)`', r'\1', text)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    # 2. Lowercase.
    text = text.lower()
    # 3. Replace each whitespace character with a hyphen (no collapsing).
    text = re.sub(r'\s', '-', text)
    # 4. Strip anything that is not a letter, digit, hyphen, or underscore.
    text = re.sub(r'[^\w\-]', '', text)
    return text


def generate_toc(lines):
    """Return a list of TOC entry strings from document heading lines."""
    entries = []
    anchor_counts = {}

    for line in lines:
        m = re.match(r'^(#{1,6})\s+(.+)', line)
        if not m:
            continue
        level = len(m.group(1))
        text = m.group(2).strip()

        anchor = make_anchor(text)

        # Deduplicate anchors (GitHub appends -1, -2, ...)
        if anchor in anchor_counts:
            anchor_counts[anchor] += 1
            unique_anchor = f'{anchor}-{anchor_counts[anchor]}'
        else:
            anchor_counts[anchor] = 0
            unique_anchor = anchor

        indent = '  ' * (level - 1)  # #=0, ##=2sp, ###=4sp, ...
        entries.append(f'{indent}- [{text}](#{unique_anchor})')

    return entries


def update_toc(filepath):
    with open(filepath) as f:
        content = f.read()

    if '## Table of Contents' not in content:
        return False, 'no TOC section found'

    lines = content.splitlines()
    toc_entries = generate_toc(lines)

    if not toc_entries:
        return False, 'no headings to list'

    new_toc_block = '## Table of Contents\n\n' + '\n'.join(toc_entries) + '\n'

    # Replace content from ## Table of Contents up to (not including) the next ## heading
    new_content = re.sub(
        r'## Table of Contents\n.*?(?=\n## |\Z)',
        new_toc_block,
        content,
        count=1,
        flags=re.DOTALL,
    )

    if new_content == content:
        return False, 'no change'

    with open(filepath, 'w') as f:
        f.write(new_content)

    return True, f'{len(toc_entries)} entries'


def main():
    if len(sys.argv) > 1:
        files = sys.argv[1:]
    else:
        files = sorted(glob.glob(os.path.join(DOCS_DIR, '*.md')))
        files = [f for f in files if os.path.basename(f) not in SKIP_FILES]

    for filepath in files:
        name = os.path.basename(filepath)
        changed, detail = update_toc(filepath)
        status = 'UPDATED  ' if changed else 'NO CHANGE'
        print(f'{status} {name} ({detail})')


if __name__ == '__main__':
    main()
