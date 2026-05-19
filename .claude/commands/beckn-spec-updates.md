---
name: beckn-spec-updates
description: Use this skill whenever the user wants to review a GitHub Issue from Beckn Protocol repositories (protocol-specifications-v2, schemas, DEG) and draft the corresponding specification artifacts. Triggers on any mention of a Beckn issue URL, spec drafting, issue-to-draft workflow, or requests to produce conformant YAML/JSON-LD/schema artifacts from a Beckn issue. Covers new endpoints, new schemas, offending schema reports, missing descriptions, cross-artifact drift, breaking changes, and legacy migrations. Always use this skill when a beckn.org or beckn GitHub Issue is mentioned alongside spec work.
---

# SKILL: Beckn Protocol — Spec Updates (Issue → Draft)

## Purpose
Use this skill when asked to review a GitHub Issue and draft corresponding specification artifacts in full conformance with the design guide and governance model.

**Repositories in scope:**
- https://github.com/beckn/protocol-specifications-v2/issues
- https://github.com/beckn/schemas/issues
- https://github.com/beckn/DEG/issues

**Authority documents:**
- NFH-001: https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/draft/docs/Introduction.md
- NFH-005: https://github.com/beckn/protocol-specifications-v2/blob/draft/docs/Design_Guide.md
- GOVERNANCE.md: https://github.com/beckn/protocol-specifications-v2/blob/draft/GOVERNANCE.md
- CONTRIBUTING.md: https://github.com/beckn/protocol-specifications-v2/blob/draft/CONTRIBUTING.md

---

## Pre-flight — SKILL_beckn_legacy_check

Before drafting anything, run the legacy drift check on all Issue content:

| Check | Flag as blocking if |
|---|---|
| BG / Beckn Gateway in v2.0 context | Any mention of BG not scoped to v1.0 |
| Domain vocabulary in core normative text | "order", "seller", "buyer", "product", "item" in proposals targeting core repos |
| Internal infra terms | Internal service names, hardcoded hostnames, config values, queue names |
| `not`/`Not` where `NOT` is required | Normative constraints using lowercase "not" |
| `catalogue` vs `catalog` | British spelling |
| Polling where async callback is the v2.0 pattern | Synchronous polling for async flows |
| Underscore action values where slash is v2.0 convention | `resource_action` where `resource/action` is required |
| Registry protocol in scope | Redirect to Linux Foundation Decentralized Trust |

Report all findings before drafting. Blocking findings MUST be noted in the draft output.

---

## Step 0 — Issue Validity Check

Before any spec work, verify the Issue is valid:

| Check | Pass condition |
|---|---|
| **Issue type** | MUST be `Bug` or `Enhancement`. Issues that are feature requests, design discussions, or questions without a linked Proposal Discussion will be noted as invalid. |
| **Linked Proposal Discussion** | MUST link to an approved Proposal Discussion in the `Proposals` category. An Issue without this link is NOT implementation-ready. |
| **Affected layer stated** | MUST identify which layer in the ecosystem stack the Issue targets. |

If the Issue is not valid, state this clearly before proceeding:

```
## Issue Validity: FAIL

This Issue is not implementation-ready.

**Reason:** [missing Proposal Discussion link / wrong type / no affected layer]

**Required action:** [specific fix]

Spec drafting cannot proceed until the Issue is valid.
```

---

## Step 1 — Parse the Issue

Extract:
- **Issue title**, number, and type (`Bug` or `Enhancement`)
- **Issue type** — classify as: `new-endpoint-request`, `new-schema-request`, `offending-schema-report`, `missing-description`, `cross-artifact-drift`, `breaking-change-request`, `legacy-migration`, `directory-structure`, `other`
- **Target layer** — which ecosystem stack layer this Issue targets
- **Artifact(s) implicated** — schemas, endpoints, or files named
- **Linked Proposal Discussion** — URL and approval status
- **Stated problem or requirement**
- **Any draft content** in the Issue body

---

## Step 2 — Stack Layer Validation

Before drafting, confirm the Issue is targeting the correct layer. Apply the escalation sequence:

1. **On-Fabric implementations** — can this be resolved there? If yes, note it and flag the Issue as misrouted.
2. **Adapter specs** — can ONIX or a similar layer handle this? If yes, flag.
3. **Schemas** — does this require only a schema change, not a core protocol change? Note the correct repository.
4. **In-Fabric stateful protocols** — does this require a Fabric service API change only?
5. **Core P2P stateless protocol** — only proceed here if all above are genuinely insufficient.

If the Issue is targeting a layer above what it needs, note this in the output and draft for the correct layer.

---

## Step 3 — Design Principles Check (NFH-001)

Verify the Issue's requirements are consistent with all seven design principles:

| Principle | Check |
|---|---|
| Decentralization | Does the required change increase edge agency? |
| Fabric-driven | Is there a Fabric requirement traceable to the linked Proposal Discussion? |
| Agent-first | Can the proposed artifact be used by an AI Agent without human intervention? |
| Pragmatism | Are implications for non-AI-native systems acknowledged? |
| Semantic interoperability | Are all new terms unambiguous across domains and regions? |
| Reusability via abstraction | Have existing schemas at schema.beckn.io been surveyed? |
| Trust by design | Are signature requirements preserved? |

---

## Step 4 — Determine Drafting Scope

| Issue Type | Artifacts to Draft |
|---|---|
| `new-endpoint-request` | Endpoint entry in `beckn.yaml`; endpoint description (6-element template); callback entry; `context.jsonld` update |
| `new-schema-request` | Full schema pack: `attributes.yaml`, `attributes.jsonschema.yaml`, `context.jsonld`, `vocab.jsonld`, `README.md` |
| `offending-schema-report` | Renamed entry in `beckn.yaml`; `owl:deprecated` + `owl:sameAs` in `vocab.jsonld`; migration notes |
| `missing-description` | Conformant descriptions for all flagged endpoints or properties using the 6-element template |
| `cross-artifact-drift` | Corrected `context.jsonld` and/or `vocab.jsonld` aligned to `attributes.yaml` as ground truth |
| `breaking-change-request` | New term + deprecated old term; migration mapping in `vocab.jsonld`; migration notes |
| `legacy-migration` | Conformant REST artifact + deprecation + mapping + migration notes |
| `directory-structure` | Correct pack layout with all five required files |

State the full drafting scope before producing any output.

---

## Step 5 — Apply Design Guide Rules

### 5A — Naming Decisions

**Endpoint naming:**
- Stateless: last token MUST be a **verb**. Syllable target: 1, hard limit: 2.
- Callback: `on_{verb}` exactly.
- Stateful: URL MUST be a **noun**. HTTP method matches operation.
- Stateful async callback: same resource path on caller's registered URI using POST. NO `on_*` pattern (CON-005-17).
- Resource identifiers: path parameters ONLY. NO query parameters for identifiers (CON-005-16).
- All path tokens: `snake_case`.
- Do NOT model on legacy exceptions (`catalog/publish`, `catalog/pull` etc.).

**Schema naming:**
- MUST be a noun or noun form of a verb.
- Maximum 2 components recommended.
- Industry schemas: use widest-adopted standard term.
- Action schemas: append `Action` suffix (CON-005-11).

**Casing — apply strictly:**

| Construct | Required | ID |
|---|---|---|
| Type/Class | `TitleCase` | CON-005-01 |
| Property | `lowerCamelCase` | CON-005-01 |
| Enum value | `SCREAMING_SNAKE_CASE` | CON-005-02 |
| Path token | `snake_case` | CON-005-12 |

**Normalization patterns:**
```
transaction_id  → transactionId
expires_at      → expiresAt
http/get        → HTTP_GET
filters.type    → filters.expressionType
```

### 5B — Endpoint Description Template

```
[Caller] invokes this endpoint to request [implementer] to [action in business terms].
This endpoint MUST only be invoked after [precondition].
[If stateful async: "Upon successful validation, [implementer] MUST return an `Ack` synchronously
and subsequently deliver the result by invoking POST [same resource path] on [caller]'s registered
callback URI, carrying [payload description]."]
[If stateless P2P async: "Upon successful validation, [implementer] MUST return an `Ack` and
subsequently invoke `/on_[verb]` on [caller]'s registered callback URI, carrying [payload]."]
If [failure condition], [implementer] MUST return [NackUnauthorized / NackBadRequest / NackForbidden /
NackNotFound] and MUST NOT invoke the callback.
```

Six-element checklist:
- [ ] Both actor names present (CON-005-06)
- [ ] Precondition stated with MUST
- [ ] Fabric service named and linked if relevant
- [ ] All response families in business terms (CON-005-07)
- [ ] Callback relationship fully stated (P2P: `on_*`; stateful: same resource path)
- [ ] All normative statements use MUST / SHOULD / MAY (CON-005-10)

### 5C — Schema Description Template

**Top-level:**
```
A [SchemaName] represents [real-world concept — what it IS, not its structure].
It is [produced by / consumed by] [actor names] [at / during] [lifecycle position].
[If Fabric-managed: "This schema models a resource managed by [Fabric service]; refer to [hyperlink]."]
[If extends another: "This schema [extends / composes / constrains] [OtherSchema] by [description]."]
```

**Per-property:**
```
[propertyName]: [What this property represents in business terms].
[Assigned by the [caller / implementer / Fabric service] at [lifecycle point].]
[Constraints beyond type: business rules, lifecycle invariants, ordering.]
[For enums: MUST be one of: VALUE_ONE ([meaning]), VALUE_TWO ([meaning]).]
[For references: References [ReferencedSchema], identifying [semantics of the reference].]
```

Schema description checklist:
- [ ] Opens with concept statement, NOT structural description (CON-005-08)
- [ ] Lifecycle position and producing/consuming actors named
- [ ] Fabric context present if applicable, with `seeAlso` noted for `vocab.jsonld`
- [ ] Schema relationships stated
- [ ] Every property has description naming what it is AND who assigns it (CON-005-09)
- [ ] MUST / SHOULD / MAY throughout (CON-005-10)

### 5D — JSON-LD Template

**New `context.jsonld`:**
```json
{
  "@context": {
    "@version": 1.1,
    "@protected": true,
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "beckn": "https://schema.beckn.io/LinkedData/v2.1/context.jsonld",
    "SchemaName": "beckn:SchemaName",
    "propertyOne": "beckn:propertyOne"
  }
}
```

**`vocab.jsonld` deprecation entry:**
```json
{
  "@id": "beckn:OldName",
  "@type": "owl:Class",
  "owl:deprecated": true,
  "owl:sameAs": { "@id": "beckn:NewName" },
  "rdfs:comment": "Deprecated. Use NewName. Migration: [notes]. Removal: [target version]."
}
```

JSON-LD checklist:
- [ ] All terms map to `beckn:` or recognised external vocab (CON-005-15)
- [ ] `@version: 1.1` and `@protected: true` declared
- [ ] Aligned with `attributes.yaml` (CON-005-03)
- [ ] Deprecations carry `owl:deprecated` + `owl:sameAs` (CON-005-04)

### 5E — Breaking Changes

Four-step migration in every draft:

1. Add new term while retaining old:
```yaml
newTermName:
  description: "[Conformant description]"
oldTermName:
  description: "DEPRECATED. Use newTermName. Removal target: [version]."
  deprecated: true
```

2. `vocab.jsonld` deprecation:
```json
{ "@id": "beckn:oldTermName", "owl:deprecated": true, "owl:sameAs": { "@id": "beckn:newTermName" } }
```

3. Migration notes in `README.md`.

4. Removal scoped to a named major release. Never remove without a named version.

---

## Step 6 — Schema Pack Directory Structure

```
{SchemaName}/                      — MUST match schema name exactly (CON-005-13)
└── v2.0/
    ├── attributes.yaml            — REQUIRED
    ├── attributes.jsonschema.yaml — REQUIRED
    ├── context.jsonld             — REQUIRED
    ├── vocab.jsonld               — REQUIRED
    └── README.md                  — REQUIRED
└── README.md                      — canonical version-agnostic description
```

Validation gates before PR:
- OpenAPI validation on `attributes.yaml`
- JSON Schema validation on `attributes.jsonschema.yaml`
- JSON-LD validation on `context.jsonld` and `vocab.jsonld`
- `npx @redocly/cli lint` for all examples

---

## Step 7 — Produce the Draft Output

```
## Spec Draft — Issue #[number]: [Title]
**Repository:** [repo]
**Issue type:** [Bug / Enhancement]
**Spec work type:** [new-endpoint-request / new-schema-request / etc.]
**Target layer:** [which ecosystem stack layer]
**Artifacts produced:** [list all files drafted]
**RFC ID field:** NFH-TBD (auto-assigned by GitHub Action on merge to `main`)

---

### Legacy Drift Check
[Results of SKILL_beckn_legacy_check — any blocking findings]

### Design Decisions
[For each naming or structural decision: the rule applied and why the choice was made]

---

### Draft Artifacts

#### [File path 1]
[Full draft content — YAML, JSON, or Markdown]

#### [File path 2]
[Full draft content]

---

### Migration Notes (if applicable)
[What is deprecated, its replacement, owl mappings, target removal version]

---

### Pre-PR Conformance Checklist

| ID | Requirement | Status |
|---|---|---|
| CON-005-01 | Properties use `lowerCamelCase` | ✓ / N/A |
| CON-005-02 | Enum values use `SCREAMING_SNAKE_CASE` | ✓ / N/A |
| CON-005-03 | Artifacts aligned | ✓ / N/A |
| CON-005-04 | Deprecation + migration present | ✓ / N/A |
| CON-005-05 | Examples validate | ✓ / Pending |
| CON-005-06 | Endpoint descriptions name both actors | ✓ / N/A |
| CON-005-07 | Response families in business terms | ✓ / N/A |
| CON-005-08 | Schema descriptions are concept statements | ✓ / N/A |
| CON-005-09 | All properties described + assignee named | ✓ / N/A |
| CON-005-10 | Formal prose + normative keywords | ✓ |
| CON-005-11 | Action schemas carry Action suffix | ✓ / N/A |
| CON-005-12 | Stateful APIs use noun paths + REST verbs | ✓ / N/A |
| CON-005-13 | Directory name matches schema name | ✓ / N/A |
| CON-005-14 | Schema pack has all 5 required files | ✓ / N/A |
| CON-005-15 | Terms map to `beckn:` IRI | ✓ / N/A |
| CON-005-16 | Resource identifiers in path parameters | ✓ / N/A |
| CON-005-17 | Stateful async callbacks use same resource path | ✓ / N/A |
| CON-005-18 | Linked Proposal Discussion is approved | ✓ / ✗ |
| CON-005-19 | Draft scope matches Proposal scope | ✓ / ✗  |

---

### Suggested PR Title
[Concise, accurate — e.g. "feat(schema): add CatalogSubscription schema pack"]

### PR Checklist Reminder
Before submitting the PR:
- [ ] RFC `ID` field is `NFH-TBD`
- [ ] PR targets `draft`, NOT `main`
- [ ] PR links to the approved Proposal Discussion
- [ ] PR diff is fully within the Proposal scope
- [ ] Companion PR opened in `schemas` repo if new terms were added to `beckn.yaml`
- [ ] `context.version` in `beckn.yaml` NOT changed unless explicitly required by the working group
```

---

## Special Cases

### Offending Schema Reports
1. Identify the specific violation (naming rule, casing, missing suffix)
2. Propose a conformant replacement using the naming rules
3. Draft full migration: new entry + `owl:deprecated` + `owl:sameAs` + migration notes + target removal version
4. Retain old name with deprecated flag — never delete without migration

### Cross-Artifact Drift
1. Treat `attributes.yaml` as ground truth (highest precedence per NFH-005)
2. Build term inventory from YAML
3. Flag every term in YAML absent from `context.jsonld` / `vocab.jsonld`
4. Flag every term in `context.jsonld` / `vocab.jsonld` with no YAML counterpart
5. Draft corrected JSON-LD entries for each gap

### Legacy Migration Requests
Known legacy exceptions requiring migration to conformant REST design:

| Legacy | Conformant replacement |
|---|---|
| `POST /catalog/publish` → `POST /catalog/on_publish` | `POST /catalog/{catalogId}` → callback: `POST /catalog/{catalogId}` on BPP URI |
| `POST /catalog/subscription` (RPC-style) | `POST /catalog/subscription` (create) + `GET /catalog/subscription/{subscriptionId}` + `DELETE /catalog/subscription/{subscriptionId}` |
| `POST /catalog/pull` + `POST /catalog/on_pull` | `GET /catalog/subscription/{subscriptionId}` → callback: `POST /catalog/subscription/{subscriptionId}` on BAP URI |

For each legacy migration draft:
1. Define new conformant artifact fully
2. Add `owl:deprecated` + `owl:sameAs` from old to new in `vocab.jsonld`
3. Write migration notes with explicit target version for old artifact removal
4. Label old artifact as legacy exception until removal

### Registry Protocol Issues
Any Issue touching registry protocols MUST be redirected:
```
This Issue involves registry protocols that are governed by Linux Foundation Decentralized Trust,
not by this governance model. Please redirect to the appropriate Linux Foundation Decentralized
Trust process. No spec work will be drafted here.
```

---

*Skill based on NFH-001, NFH-005, GOVERNANCE.md, CONTRIBUTING.md. Canonical sources: protocol-specifications-v2/draft branch.*
