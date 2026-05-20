---
name: Beckn Protocol v2 Network Actors
description: Canonical actor names in Beckn Protocol v2 — no Gateway, no CDS
type: project
---

There is NO Gateway (BG) and NO CDS (Catalogue Discovery Service) in Beckn Protocol v2.0.

**Why:** These actors were split/removed as part of the v2 architecture redesign. Gateway existed in v1 only.

**v2 replacements:**
- CDS → split into two separate actors:
  - **CS** (Cataloging Service): handles catalog publish/index on the Fabric layer
  - **DS** (Discovery Service): handles catalog subscribe and query on the network layer
- **Gateway (BG):** removed entirely from v2. Only mention "Gateway" when explicitly discussing the old Beckn Protocol v1.x standard for backward-compatibility context.

**How to apply:**
- Never introduce "Gateway" or "CDS" into v2 specification documents.
- When referencing intermediary routing in v2, refer to the specific actor (CS, DS, Registry) or describe the flow directly.
- If editing a doc that mentions Gateway or CDS in a v2 context, replace with the appropriate CS/DS actor or remove the reference.
- BECKN-005 and other v1 artifacts may legitimately mention Gateway; do not alter those external references.
