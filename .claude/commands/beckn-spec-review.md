---
name: beckn-spec-review
description: Use this skill whenever the user wants to review a Pull Request against the Beckn Protocol repositories (protocol-specifications-v2, schemas, DEG). Triggers on any mention of a Beckn PR URL, Beckn spec review, design-guide conformance check, or requests to review YAML/JSON-LD/schema changes for Beckn. Performs an RFC gate check first — if no approved RFC is linked, the review stops immediately. Otherwise performs a full NFH-005 design-guide conformance review of the PR diff and produces a structured review with a merge recommendation. Always use this skill when a beckn.org or beckn GitHub PR is mentioned.
---

# SKILL: Beckn Protocol — Spec Review (Pull Request)

## Purpose
Use this skill when asked to **review a Pull Request** submitted to any of the following repositories:

- https://github.com/beckn/protocol-specifications-v2/pulls
- https://github.com/beckn/schemas/pulls
- https://github.com/beckn/DEG/pulls

A PR in these repositories typically adds or modifies API endpoint definitions, schema files (`attributes.yaml`, `attributes.jsonschema.yaml`), JSON-LD artifacts (`context.jsonld`, `vocab.jsonld`), examples, or documentation. This skill performs a full design-guide conformance review of the diff and produces a structured PR review with a merge recommendation.

**Design guide authority:** NFH-005, Networks for Humanity Foundation  
**Canonical URL:** https://github.com/beckn/protocol-specifications-v2/blob/draft/docs/Design_Guide.md  
**Normative keywords:** MUST = enforceable blocker, SHOULD = strong recommendation, MAY = optional

---

## Step 0 — RFC Gate Check (runs before everything else)

**This step is mandatory and non-skippable.** No other step runs until all applicable gate conditions pass.

### RFC Lifecycle Stages

Every Beckn Protocol change MUST progress through the following stages in order. Each stage is a prerequisite for the next.

| Stage | Location | Description |
|---|---|---|
| **Idea** | GitHub Discussion — `Ideas` category | The problem or opportunity is posted for community awareness. No RFC structure required. |
| **Proposal** | GitHub Discussion — `Proposals` category | A formal RFC authored using the NFH-006 template, linked to the Idea Discussion. Subject to working group review and vote. |
| **Protocol Draft** | Merged into `draft` branch via PR | The Proposal has been approved by the working group and merged. RFC content is normative but not yet a standard. |
| **Protocol Standard** | Merged into `main` branch via PR | Final standard. Auto-assigned RFC ID on merge. Three sub-types: `REQUIRED`, `RECOMMENDED`, `NOT RECOMMENDED`. MUST have at least one linked Issue (Bug or Enhancement). |

### Gate Conditions by Target Branch

**PR targeting `draft` branch — minimum RFC stage: Proposal**

| # | Check | Pass condition |
|---|---|---|
| G-0 | Idea Discussion exists | A Discussion in the `Ideas` category MUST exist and be linked from the PR description or the RFC document |
| G-1 | Proposal Discussion exists | A Discussion in the `Proposals` category MUST exist, MUST be linked to the G-0 Idea Discussion, and MUST use the NFH-006 RFC template |
| G-2 | RFC stage matches branch | RFC MUST be at Proposal stage or higher — i.e., an approved Proposal Discussion exists |
| G-3 | Scope alignment | PR diff scope MUST correspond precisely to the approved Proposal content (CON-005-19) |

**PR targeting `main` branch — minimum RFC stage: Protocol Draft**

All of G-0 through G-3 above, plus:

| # | Check | Pass condition |
|---|---|---|
| G-4 | RFC in `draft` branch | The RFC document MUST already exist in the `draft` branch, merged via a prior PR |
| G-5 | Linked Issues | The PR MUST link at least one Issue of type Bug or Enhancement |
| G-6 | Protocol Standard type declared | The RFC Document Details MUST declare one of: `Protocol Standard - REQUIRED`, `Protocol Standard - RECOMMENDED`, or `Protocol Standard - NOT RECOMMENDED` |
| G-7 | RFC ID present | The RFC ID field MUST be `NFH-TBD` — the actual ID is auto-assigned on merge to `main`; if a hardcoded ID is present, flag it |

### Gate Outcomes

| Finding | Outcome |
|---|---|
| No Idea Discussion linked (G-0 fails) | **STOP — auto-reject. Lifecycle bypass.** |
| No Proposal Discussion linked (G-1 fails) | **STOP — auto-reject. Lifecycle bypass.** |
| RFC committed directly in PR without Proposal Discussion | **STOP — auto-reject. Lifecycle bypass.** |
| Proposal Discussion exists but not yet approved by working group | **STOP — auto-reject. Awaiting working group consensus.** |
| RFC at correct stage but diff scope exceeds Proposal (G-3 fails) | **STOP — auto-reject. List out-of-scope elements.** |
| PR to `main` but RFC not yet in `draft` branch (G-4 fails) | **STOP — auto-reject. Submit PR to `draft` first.** |
| PR to `main` with no linked Issues (G-5 fails) | **STOP — auto-reject.** |
| All applicable gate conditions pass | **PASS — proceed to Step 1.** |

### Auto-reject output format

When Step 0 fails, produce ONLY this output and stop:

```
## PR Review — [PR Title] (#[number]) — RFC GATE FAILED

**Gate result:** ✗ AUTO-REJECTED — no technical review conducted.

---

## TL;DR

### Recommended Action — Reviewers

**Close this Pull Request. [State specific next step for author based on failure type]:**
- Lifecycle bypass: request author post an Idea Discussion and follow the RFC process from the beginning.
- Proposal not yet approved: request author await working group consensus before resubmitting.
- Scope exceeds Proposal: request author remove out-of-scope changes or update the Proposal.

Reason summary:
- [Gate failure type and which checks failed (G-0 through G-7)]
- [RFC structural deficiency summary if RFC document is readable — 2–4 bullets]
- [Diff-level design violations visible without full review — RPC-style endpoints,
  on_* callbacks on stateful APIs, query params for resource identifiers]

Close the PR. Post a comment linking this review document.

---

### Recommended Action — Contributors

**[Specific instruction based on failure type]**

For lifecycle bypass (G-0 or G-1 failed):
1. Withdraw this Pull Request.
2. Post an Idea Discussion in the `Ideas` category.
3. Open a Proposal Discussion in the `Proposals` category using the NFH-006 template, linked to the Idea.
4. Address all RFC structural deficiencies in the Proposal Discussion.
5. Await working group approval of the Proposal.
6. Submit a new PR to `draft` only after the Proposal is approved (CON-005-19).
7. [For main branch: add linked Issues and declare Protocol Standard type before PR to `main`.]

For scope violation (G-3 failed):
1. Remove the following out-of-scope elements from the PR diff: [list]
2. OR update the Proposal Discussion to cover these elements and obtain re-approval.
3. Resubmit after resolution.

> **Notice.** [State specific violations — lifecycle bypass, design violations found,
> any repeated violation history.] Repeated submission of non-conformant Pull
> Requests carries the risk of suspension of PR submission privileges, followed
> by Issue and Discussion access, per the governance provisions in NFH-005.
> Reviewers are required to report repeated violations to the Working Group
> Administrator. Contributors SHOULD read CONTRIBUTING.md, CODE_OF_CONDUCT.md,
> and GOVERNANCE.md before making further contributions.

---

**Gate check results:**
| # | Check | Result |
|---|---|---|
| G-0 | Idea Discussion | ✓ / ✗ |
| G-1 | Proposal Discussion | ✓ / ✗ |
| G-2 | RFC stage vs target branch | ✓ / ✗ |
| G-3 | Scope alignment | ✓ / ✗ / N/A |
[Add G-4 through G-7 if PR targets `main`]

No review comments on the diff are provided.
```

---

## Step 1 — Fetch and Parse the Pull Request

When given a PR URL, fetch it and extract:
- **PR title**, number, and target branch
- **Files changed** — list all modified/added/deleted files
- **Diff summary** — what artifacts are being added, changed, or removed
- **PR description** — the author's stated intent and scope

Classify the PR scope:

| Changed File Type | Review Sections to Activate |
|---|---|
| `*.yaml` (OpenAPI / attributes) | §A Endpoint Naming, §B Endpoint Descriptions, §C Schema Naming, §D Schema Descriptions |
| `*.jsonschema.yaml` | §C Schema Naming, §D Schema Descriptions, §F Cross-Artifact Alignment |
| `context.jsonld` | §E JSON-LD, §F Cross-Artifact Alignment |
| `vocab.jsonld` | §E JSON-LD, §F Cross-Artifact Alignment |
| `README.md` / docs | §D Schema Descriptions, §G Prose Quality |
| Directory additions | §H Organization |
| Any rename or removal | §I Backward Compatibility |

---

## Step 2 — Diff-Level Review

For every changed artifact, apply the relevant sections below. Evaluate only what is in the diff — do not penalise for pre-existing violations in unchanged lines unless they are directly relevant to the change.

---

## §A — Endpoint Naming Review

Apply to every endpoint added or renamed in the diff.

**Core naming principle (apply to all names):**
> A global developer reading only the name, with zero context, must be able to infer its meaning. If not — flag.

**Stateless endpoints:**
- Last path token MUST be a **verb**. Flag nouns, adjectives, and gerunds. (CON-005-12)
- Syllable target: 1. Hard limit: 2. Flag anything over 2 as requiring working-group approval.
- Callback MUST be `on_{verb}` matching the request verb exactly.
- All path tokens MUST use `snake_case`. Flag other casing.

**Stateful (Fabric service) endpoints:**
- URL path MUST be a **noun**. Flag verb-based resource names. (CON-005-12)
- Resource identifiers MUST be **path parameters**. Flag query parameters used as resource identifiers. (CON-005-16)
- HTTP method MUST match intended operation:

| HTTP Method | Correct Use |
|---|---|
| POST | Create a new resource instance |
| GET | Retrieve a resource or its current state |
| PUT | Full replacement of a resource |
| PATCH | Partial update |
| DELETE | Remove a resource |

- **Async callback for stateful APIs:** the implementer delivers the async result by calling the **same resource path** on the caller's registered callback URI using `POST`. The `on_*` pattern MUST NOT appear on stateful API callbacks. (CON-005-17)
  - ✓ `GET /catalog/subscription/{subscriptionId}` — callback: `POST /catalog/subscription/{subscriptionId}` on caller's URI
  - ✗ `GET /catalog/subscription/{subscriptionId}` — callback: `POST /catalog/on_get` — VIOLATION

**Normalization check — flag these property name patterns:**
```
transaction_id  → must be transactionId
expires_at      → must be expiresAt
http/get        → must be HTTP_GET
filters.type    → must be filters.expressionType
```

---

## §B — Endpoint Description Review

Apply to every new or modified endpoint description in the diff.

**Six mandatory elements — check each in the diff text:**

| # | Element | Pass Condition |
|---|---|---|
| 1 | Action statement | Single sentence; verb-first; names BOTH caller and implementer |
| 2 | Preconditions | Prior state or API call stated explicitly with MUST |
| 3 | Fabric context | If Fabric service involved: named + hyperlinked to canonical doc |
| 4 | Message envelope | `context` and `message` fields with endpoint-specific semantics described |
| 5 | Response semantics | All applicable families (Ack, NackBadRequest, NackUnauthorized, ServerError) described in business terms |
| 6 | Callback relationship | When fired, by whom, what it carries, how caller interprets it |

**Tone and grammar:**
- All normative statements use `MUST` / `SHOULD` / `MAY` (CON-005-10)
- No domain-assuming language ("order", "seller") unless this is a domain-specific extension repo (DEG)
- No informal language or unexplained abbreviations
- Fabric-first: if Fabric mediates, it is named and linked

**Immediate blockers:**
- Description conflates `/x` request semantics with `/on_x` callback semantics
- Either actor (caller or implementer) is unnamed (CON-005-06)
- Response families missing or described only as HTTP codes (CON-005-07)

---

## §C — Schema Naming Review

Apply to every schema type, property, and enum value added or renamed in the diff.

**Schema name:**
- MUST be a noun or noun form of a verb (CON-005-08)
- MUST be self-describing without reading the description
- Multi-word: maximum 2 components recommended; flag 3+
- Industry-specific schemas MUST use the widest-adopted industry-standard term
- Action schemas MUST carry `Action` suffix (CON-005-11)
  - Flag: `Payment`, `Cancellation`, `Fulfillment` if they describe acts
  - Correct: `PaymentAction`, `CancellationAction`, `FulfillmentAction`

**Casing — flag any violation in the diff:**

| Construct | Required Casing | Conformance ID |
|---|---|---|
| Type / Class name | `TitleCase` | CON-005-01 |
| Property name | `lowerCamelCase` | CON-005-01 |
| Enum value | `SCREAMING_SNAKE_CASE` | CON-005-02 |
| `snake_case` property | ✗ VIOLATION | CON-005-01 |
| `type` as a property name | ✗ AVOID | CON-005-01 note |

---

## §D — Schema Description Review

Apply to every new or modified schema/property description in the diff.

**Top-level schema description — all four elements must be present:**

| # | Element | Pass Condition |
|---|---|---|
| 1 | Concept statement | Opens with real-world concept; no structural language |
| 2 | Lifecycle position | States where in value-exchange lifecycle; names producing/consuming actors |
| 3 | Fabric context | If Fabric-managed: service named + canonical doc linked; `seeAlso` in `vocab.jsonld` |
| 4 | Schema relationships | Extends / composes / constrains relationships stated |

**Property descriptions (CON-005-09) — all five must be present for each property:**
1. States what the property represents (not a name restatement)
2. Names who assigns the value: caller, implementer, or Fabric service
3. States constraints beyond JSON Schema type
4. For enums: describes each value in this schema's context
5. For references: states semantics of the reference

**Blocker anti-patterns (CON-005-08):**
- Opens with: "A JSON-LD object containing…" / "An object with fields…"
- Is only: "[Schema name] schema for Beckn Protocol vX.Y"
- Is only: "[Schema name] request/response payload"

---

## §E — JSON-LD Review

Apply to every `context.jsonld` or `vocab.jsonld` change in the diff.

**Check:**
- Every term in `@context` maps to an IRI in `beckn:` namespace or recognised external vocab (`xsd:`, `schema:`) (CON-005-15)
- `@version: 1.1` declared
- `@protected: true` set
- `context.jsonld` and `vocab.jsonld` remain aligned with `attributes.yaml` (CON-005-03)
- Renamed terms carry `owl:sameAs` or `owl:deprecated` + migration mapping (CON-005-04)
- No term is removed without a deprecation step

**Pattern to verify for all new terms:**
```json
{
  "@context": {
    "@version": 1.1,
    "@protected": true,
    "beckn": "https://schema.beckn.io/LinkedData/v2.1/context.jsonld",
    "NewTerm": "beckn:NewTerm",
    "newProperty": "beckn:newProperty"
  }
}
```

---

## §F — Cross-Artifact Alignment Check

Apply whenever the PR touches more than one artifact type.

Verify the same terms, types, and properties appear consistently across:

| Pair to check | What to verify |
|---|---|
| `attributes.yaml` ↔ `attributes.jsonschema.yaml` | Same property names, types, and required fields |
| `attributes.yaml` ↔ `context.jsonld` | Every property in YAML has a mapping in `@context` |
| `context.jsonld` ↔ `vocab.jsonld` | Term IRIs are consistent |
| Any of the above ↔ `examples/**` | Examples validate against schema (CON-005-05) |

Flag any term that appears in one artifact but not the corresponding one (CON-005-03).

**Artifact precedence (when artifacts conflict):**
1. `attributes.yaml`
2. `schema.json`
3. `context.jsonld`
4. `vocab.jsonld`
5. `examples`
6. `docs`
7. `README.md`

If a conflict exists, the higher-precedence artifact governs. Flag which artifact is out of sync.

---

## §G — Prose Quality Review

Apply to description text in `README.md` files and inline YAML descriptions.

- Formal technical prose only (CON-005-10)
- All normative statements use `MUST` / `SHOULD` / `MAY`
- No colloquialisms, domain-assuming language, or unexplained abbreviations
- Passive voice only when the actor is genuinely indeterminate
- Hyperlinks to canonical documents embedded inline where referenced

---

## §H — Schema Organization Review

Apply when the PR adds a new schema directory or moves files.

**Directory structure (CON-005-13):**
- Directory name MUST exactly match schema name (case-sensitive)
- Versioned subdirectory (e.g. `v2.0/`) MUST contain all five required files

**Required files per versioned pack (CON-005-14):**

| File | Required |
|---|---|
| `attributes.yaml` | ✓ |
| `attributes.jsonschema.yaml` | ✓ |
| `context.jsonld` | ✓ |
| `vocab.jsonld` | ✓ |
| `README.md` | ✓ |

Flag any PR that adds a versioned directory without all five files.

**Validation gates** — confirm the PR description or CI results show:
- OpenAPI validation passed for `attributes.yaml`
- JSON Schema validation passed for `attributes.jsonschema.yaml`
- JSON-LD validation passed for `context.jsonld` and `vocab.jsonld`

---

## §I — Backward Compatibility Review

Apply to any PR that renames, removes, or changes the meaning of an existing artifact.

**Breaking change flags:**
- Property, type, or enum renamed — MUST violation if no deprecation path (CON-005-04)
- Required field added to existing schema — MUST violation if no migration notes
- Term meaning changed without new term introduced — MUST violation

**Required migration evidence in the PR diff:**
1. New term present in diff while old term still exists (not deleted)
2. Old term carries `owl:deprecated` in `vocab.jsonld`
3. `owl:sameAs` or equivalent mapping from old to new term in `vocab.jsonld`
4. PR description or linked issue names the target major version for old-term removal

Flag each missing step as a MUST violation.

---

## Step 3 — Full Conformance Table

Run all 19 checks against the diff:

| ID | Requirement | Result |
|---|---|---|
| CON-005-01 | New properties use `lowerCamelCase` | ✓ / ✗ / N/A |
| CON-005-02 | Enum values use `SCREAMING_SNAKE_CASE` | ✓ / ✗ / N/A |
| CON-005-03 | Artifacts semantically aligned | ✓ / ✗ / N/A |
| CON-005-04 | Renames/removals include deprecation + migration | ✓ / ✗ / N/A |
| CON-005-05 | Examples validate against canonical contracts | ✓ / ✗ / N/A |
| CON-005-06 | Endpoint descriptions name both actors | ✓ / ✗ / N/A |
| CON-005-07 | Response families described in business terms | ✓ / ✗ / N/A |
| CON-005-08 | Schema descriptions are concept statements | ✓ / ✗ / N/A |
| CON-005-09 | Every property has a description + value assignee | ✓ / ✗ / N/A |
| CON-005-10 | Formal prose + normative keywords used | ✓ / ✗ / N/A |
| CON-005-11 | Action schemas carry `Action` suffix | ✓ / ✗ / N/A |
| CON-005-12 | Stateful APIs use noun paths + REST verbs (sync and async) | ✓ / ✗ / N/A |
| CON-005-13 | Directory name matches schema name (case-sensitive) | ✓ / ✗ / N/A |
| CON-005-14 | Schema pack has all 5 required files | ✓ / ✗ / N/A |
| CON-005-15 | Schema terms map to `beckn:` IRI or external vocab | ✓ / ✗ / N/A |
| CON-005-16 | Stateful resource identifiers expressed as path parameters, not query parameters | ✓ / ✗ / N/A |
| CON-005-17 | Stateful async callbacks use same resource path; no `on_*` pattern | ✓ / ✗ / N/A |
| CON-005-18 | PR links to an approved RFC at the correct lifecycle stage for the target branch *(checked in Step 0 — G-0 through G-7)* | ✓ / ✗ |
| CON-005-19 | PR diff scope matches approved Proposal; no out-of-scope changes *(checked in Step 0 — G-3)* | ✓ / ✗ |

---

## Step 4 — Produce the PR Review

Structure the output as follows:

```
## PR Review — [PR Title] (#[number])
**Repository:** [repo name]
**Target branch:** [branch]
**Files reviewed:** [count and list]
**Sections applied:** [list of §]

---

## TL;DR

### Recommended Action — Reviewers

**[One crisp instruction: Approve / Request changes / Close PR]**

[2–4 bullets summarising the most important findings. For gate failures:
close + move to discussion + reason. For blocking issues: what must change
before merge. For approvals: what SHOULD items the author should be aware of.]

---

### Recommended Action — Contributors

**[One crisp instruction matching the reviewer action]**

[Numbered action list. For lifecycle bypass gate failures: post Idea Discussion,
then Proposal Discussion (NFH-006 template, linked to Idea), await working group
approval, then submit PR. For scope violations: remove out-of-scope elements or
update and re-approve the Proposal. For `main` branch failures: add Issues, declare
Protocol Standard type. For blocking technical issues: numbered list of required
fixes. For approvals: SHOULD items to address.]

[Include the privilege warning blockquote when: this is a repeated violation, the
PR contains a lifecycle bypass, or multiple gate conditions failed simultaneously:]

> **Notice.** [State the specific violations.] Repeated submission of
> non-conformant Pull Requests carries the risk of suspension of PR submission
> privileges, followed by Issue and Discussion access, per the governance
> provisions in NFH-005. Reviewers are required to report repeated violations
> to the Working Group Administrator. Contributors SHOULD read CONTRIBUTING.md,
> CODE_OF_CONDUCT.md, and GOVERNANCE.md before making further contributions.

---

### RFC Gate (CON-005-18, CON-005-19)

| # | Check | Result |
|---|---|---|
| G-0 | Idea Discussion exists and linked | ✓ / ✗ |
| G-1 | Proposal Discussion exists, linked to Idea, uses NFH-006 template | ✓ / ✗ |
| G-2 | RFC stage matches target branch minimum | ✓ / ✗ |
| G-3 | Scope alignment — diff within Proposal scope | ✓ / ✗ / N/A |
| G-4 | RFC in `draft` branch *(only if PR targets `main`)* | ✓ / ✗ / N/A |
| G-5 | Linked Issues — Bug or Enhancement *(only if PR targets `main`)* | ✓ / ✗ / N/A |
| G-6 | Protocol Standard type declared *(only if PR targets `main`)* | ✓ / ✗ / N/A |
| G-7 | RFC ID is `NFH-TBD` *(only if PR targets `main`)* | ✓ / ✗ / N/A |

**Gate result:** PASS / FAIL — [failure type if applicable: Lifecycle Bypass / Stage Mismatch / Scope Violation]

*(If gate failed, the TL;DR above is the operative output.
 Schema findings below are reference only.)*

---

### Summary
[2–3 sentences: what the PR does, overall design-guide compliance assessment.
Omit for gate failures — executive summary is in TL;DR.]

---

### Blocking Issues (MUST violations — PR cannot merge)
For each:
- **File:** `path/to/file.yaml` (line N if known)
- **Rule:** [CON-005-xx or rule name]
- **Found:** [what is in the diff]
- **Required:** [what it must be changed to]

### Recommendations (SHOULD violations — address before merge)
For each:
- **File:** [path]
- **Rule:** [rule name]
- **Found:** [current state]
- **Recommended:** [suggested improvement]

### Inline Suggested Corrections
[Where appropriate, provide corrected text for descriptions, names, or JSON-LD entries]

---

### Conformance Table
[Full 19-row table with ✓ / ✗ / N/A per row]

---

### Merge Recommendation
[One of:]
- ✅ APPROVE — RFC gate passed; no MUST violations. Merge when SHOULD items are addressed or accepted.
- ⚠️ REQUEST CHANGES (minor) — RFC gate passed; SHOULD violations only. Author should address before merge.
- 🚫 REQUEST CHANGES (blocking) — RFC gate passed; [N] MUST violation(s). Must be resolved before merge.
- ✗ AUTO-REJECTED — RFC gate failed. No technical review conducted. See TL;DR above.

### Required Changes
[Numbered list of concrete diffs the author must make. Omit for gate failures —
required actions are in the TL;DR.]
```

---

## Legacy Exception Handling in PRs

If the PR modifies a known legacy exception artifact (`/catalog/publish`, `/catalog/pull`, `/catalog/on_publish`, `/catalog/on_pull`, `status` endpoint, etc.):
- Do NOT apply new endpoint naming rules or REST callback rules retroactively to the legacy artifact itself.
- DO flag if the PR is modelling NEW artifacts on the legacy exception pattern — new RPC-style endpoints or `on_*` callbacks for stateful APIs are blocking violations (CON-005-12, CON-005-17).
- If the PR is migrating a legacy exception to REST-conformant design, verify all four migration steps are present in the diff and that the new design uses path parameters (CON-005-16) and the REST callback pattern (CON-005-17).

---

*Skill based on NFH-005 Beckn Protocol Specification Design Guide, Draft-02. Source: https://github.com/beckn/protocol-specifications-v2/blob/draft/docs/Design_Guide.md*
