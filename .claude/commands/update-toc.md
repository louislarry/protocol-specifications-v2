---
name: update-toc
description: Regenerates the Table of Contents in all Beckn Protocol RFC documents in the docs/ folder. Run this after adding, removing, or renaming any headings in an RFC doc. Invokes scripts/update_toc.py.
---

# Update Table of Contents

Run the TOC update script, show what changed, then stage and commit.

```bash
cd /home/ravi/www/spec_work/protocol-specifications-v2
python3 scripts/update_toc.py
```

To update a single file only:
```bash
python3 scripts/update_toc.py docs/API.md
```

After running, review the diff, then stage and commit the updated files.
