---
name: beckn-proposal-review
description: Use this skill whenever the user wants to review a Discussion posted to Beckn Protocol repositories (protocol-specifications-v2, schemas, DEG). Triggers on any mention of a Beckn discussion URL, proposal review, design-guide readiness check, or requests to assess whether a Beckn proposal is ready to proceed to a Pull Request. Performs an RFC lifecycle check first, then a design-principle gate, then a full NFH-005 conformance review. Always use this skill when a beckn.org or beckn GitHub Discussion is mentioned.
---

# SKILL: Beckn Protocol — Proposal Review

## Purpose
Use this skill when asked to **review a Discussion** posted to any of the following repositories:

- https://github.com/beckn/protocol-specifications-v2/discussions
- https://github.com/beckn/schemas/discussions
- https://github.com/beckn/DEG/discussions

This skill evaluates whether a Proposal Discussion is conformant with the RFC writing standard, the seven design principles, and the NFH-005 Design Guide, and whether it is ready for the working group to approve for a Protocol Draft PR.

**Authority documents:**
- NFH-001: https://raw.githubusercontent.com/beckn/protocol-specifications-v2/refs/heads/draft/docs/Introduction.md
- NFH-005: https://github.com/beckn/protocol-specifications-v2/blob/draft/docs/Design_Guide.md
- NFH-006: https://github.com/beckn/protocol-specifications-v2/blob/draft/docs/NFH-006_RFC_Writing_Guide.md
- GOVERNANCE.md: https://github.com/beckn/protocol-specifications-v2/blob/draft/GOVERNANCE.md

---

## Pre-flight — SKILL_beckn_legacy_check

Before any other step, run the legacy drift check on all content in the Discussion:

| Check | Flag as blocking if |
|---|---|
| BG / Beckn Gateway in v2.0 context | Any mention of BG or Beckn Gateway not explicitly scoped to v1.0 |
| Domain vocabulary in core protocol proposals | "order", "seller", "buyer", "product", "item" in normative text targeting core repos |
| Internal infra terms | Internal service names, hardcoded hostnames, config thresholds, queue names |
| `not`/`Not` where `NOT` is required | Any normative constraint using lowercase "not" |
| `catalogue` vs `catalog` | British spelling in any artifact |
| Polling where async callback is the v2.0 pattern | Any synchronous polling mechanism proposed for a flow that should use async callback |
| Underscore action values where slash is v2.0 convention | `resource_action` where `resource/action` is required (except documented exceptions) |
| Registry protocol in scope | Any proposal touching registry protocols that should be directed to Linux Foundation Decentralized Trust |

Report all findings before proceeding. Blocking findings MUST be resolved before the proposal can advance.

---

## Step 0 — RFC Lifecycle Check

Before reviewing content quality, verify that the Discussion is in the correct place in the RFC lifecycle.

| Check | Pass condition |
|---|---|
| **Discussion category** | MUST be in the `Proposals` category. If it is in `Ideas` or `General`, it is NOT a reviewable Proposal — it is an earlier lifecycle stage. |
| **Linked Idea Discussion** | MUST link to a prior Discussion in the `Ideas` category. A Proposal with no linked Idea has bypassed the first lifecycle stage. |
| **RFC template used** | The Discussion body MUST use the NFH-006 RFC template structure. A free-form Discussion is not a Proposal. |
| **Stack layer justified** | The Motivation section MUST demonstrate why the change cannot be addressed at a higher layer (On-Fabric → Adapter → Schema → In-Fabric → Core P2P). |

**If any check fails:**

```
## Proposal Review — [Title] (#[number])

### RFC Lifecycle: FAIL

This Discussion is not ready for proposal review.

**Reason:** [specific failure]

**Required action:** [one of]
- Move to the `Proposals` category and restructure using the NFH-006 RFC template.
- Link the prior `Ideas` Discussion before this can be reviewed as a Proposal.
- Demonstrate in the Motivation section why a higher layer cannot address this requirement.

No content review has been conducted.
```

---

## Step 1 — Fetch and Parse the Discussion

Extract:
- **Discussion title** and number
- **Proposal type** — classify as: `new-endpoint`, `endpoint-change`, `new-schema`, `schema-rename`, `schema-deprecation`, `schema-property-change`, `directory-structure`, `json-ld-change`, `other`
- **Target layer** — which layer in the ecosystem stack this proposal targets
- **Proposed artifact(s)** — names of endpoints, schemas, or properties
- **Author's stated rationale**
- **Any draft spec text, YAML, JSON, or examples** in the Discussion body

---

## Step 2 — Design Principles Gate (NFH-001)

Evaluate the proposal against all seven design principles. A proposal that fails any principle is NOT ready for working group approval regardless of technical quality.

| Principle | What to check |
|---|---|
| **1. Decentralization** | Does the change increase, not reduce, agency at the network edges? Flag if it introduces a required central coordinator. |
| **2. Fabric-driven** | Is there a traceable Fabric capability requirement in the Motivation section? Flag if the change is driven by implementation convenience. |
| **3. Agent-first** | Can every proposed flow be exercised by an AI Agent without human intervention? Flag any flow requiring real-time human input with no machine-executable alternative. |
| **4. Pragmatism** | Does the Motivation acknowledge implications for non-AI-native systems? |
| **5. Semantic interoperability** | Are all new terms defined, unambiguous, and interpretable consistently across domains and regions? |
| **6. Reusability via abstraction** | Does the Motivation demonstrate that existing schemas at schema.beckn.io were surveyed and found insufficient? Flag proposals for new schemas without this evidence. |
| **7. Trust by design** | Does the proposal preserve signature and acknowledgement requirements as baseline behavior? Flag any relaxation of these. |

**Stack layer validation:**
The Motivation MUST demonstrate that the change cannot be addressed at a faster-moving layer:
1. On-Fabric implementations
2. Adapter specs (ONIX etc.)
3. Schemas (`beckn/schemas`)
4. In-Fabric stateful protocols
5. Core P2P stateless protocol — only if all above are insufficient

Flag as a MUST violation if the Motivation does not address this.

---

## Step 3 — RFC Structure Review (NFH-006)

Check that the Proposal contains all mandatory RFC sections:

| Section | Pass condition |
|---|---|
| Abstract | 100–200 words; self-contained; states problem, mechanism, and out-of-scope |
| Motivation | Four subsections: Current State, Identified Problems, Why Current Design Cannot Be Extended, numbered Requirements |
| Design Goals and Non-Goals | Goals numbered and verifiable; Non-Goals state why excluded |
| Roles and Actors | Table with protocol identity, endpoints invoked/implemented; BG MUST NOT appear |
| Protocol Flows | Async flows have sequence diagrams; lifecycle resources have state machines; error flows documented |
| Schema Changes | New schemas justified; property descriptions include assignee; cross-artifact alignment plan linked |
| Security Considerations | Drafted before Protocol Flows; conforms to Authentication and Trust doc |
| Privacy Considerations | PII fields identified or explicitly stated as absent |
| Prior Art | At least three specific prior works named with adoption/rejection rationale |

---

## Step 4 — Content Review by Proposal Type

### §A — Endpoint Naming

| Rule | Check |
|---|---|
| Stateless: last path token is a verb | Flag nouns, adjectives, gerunds |
| Syllable target 1, hard limit 2 | Flag >2 syllables — requires working-group approval |
| Callback is `on_{verb}` | Flag any deviation |
| Path tokens use `snake_case` | Flag other casing |
| Stateful: URL path is a noun | Flag verb-based paths (CON-005-12) |
| Stateful: HTTP method matches operation | POST=create, GET=retrieve, PUT=replace, PATCH=update, DELETE=remove |
| Stateful async callback: same resource path, HTTP POST | Flag `on_*` pattern on stateful APIs (CON-005-17) |
| Resource identifiers in path parameters | Flag query parameters used as resource identifiers (CON-005-16) |
| NOT modelled on legacy exception | Flag new RPC-style endpoints copying `catalog/publish` pattern |

### §B — Endpoint Description

Six mandatory elements — check each:

| Element | Pass condition |
|---|---|
| 1. Action statement | Verb-first; names BOTH caller and implementer explicitly |
| 2. Preconditions | Prior API call or state stated with MUST |
| 3. Fabric context | If Fabric involved: service named and linked to canonical doc |
| 4. Message envelope | `context` and `message` semantics described |
| 5. Response semantics | All families (Ack, NackBadRequest, NackUnauthorized, ServerError) in business terms |
| 6. Callback relationship | For P2P stateless: states when/by whom/what/how. For stateful: states same-resource-path delivery. |

### §C — Schema Naming

- MUST be a noun or noun form of a verb
- Self-describing without the description
- Maximum 2 components recommended; flag 3+
- Industry-specific: MUST use widest-adopted industry-standard term
- Action schemas MUST carry `Action` suffix (CON-005-11)

Casing:

| Construct | Required | ID |
|---|---|---|
| Type/Class | `TitleCase` | CON-005-01 |
| Property | `lowerCamelCase` | CON-005-01 |
| Enum value | `SCREAMING_SNAKE_CASE` | CON-005-02 |

### §D — Schema Description

Top-level description — four required elements:
1. Concept statement — real-world concept, no structural language
2. Lifecycle position — where in value-exchange lifecycle; which actors produce/consume
3. Fabric context — if Fabric-managed: service named, canonical doc linked, `seeAlso` in `vocab.jsonld`
4. Schema relationships — extends/composes/constrains stated explicitly

Property descriptions — five requirements each:
1. States what the property represents (not a name restatement)
2. Names who assigns the value
3. States constraints beyond JSON Schema type
4. For enums: each value described in this schema's context
5. For references: semantics of the reference stated

### §E — Backward Compatibility

Flag any proposal that renames, removes, or changes meaning without all four migration steps:
1. New term added while old retained
2. Old term marked `owl:deprecated` in `vocab.jsonld`
3. Migration notes and semantic mapping described
4. Old term removal scoped to a named major release

### §F — JSON-LD

- All terms map to `beckn:` namespace or recognised external vocab (CON-005-15)
- `@version: 1.1` and `@protected: true` declared
- Aligned with `attributes.yaml` (CON-005-03)
- Renamed terms carry `owl:sameAs` + `owl:deprecated` (CON-005-04)

---

## Step 5 — Conformance Table

| ID | Requirement | Result |
|---|---|---|
| CON-005-01 | New properties use `lowerCamelCase` | ✓ / ✗ / ⚠️ |
| CON-005-02 | Enum values use `SCREAMING_SNAKE_CASE` | ✓ / ✗ / ⚠️ |
| CON-005-03 | Artifacts semantically aligned | ✓ / ✗ / ⚠️ |
| CON-005-04 | Renames/removals include deprecation + migration | ✓ / ✗ / N/A |
| CON-005-05 | Examples validate against canonical contracts | ✓ / ✗ / ⚠️ |
| CON-005-06 | Endpoint descriptions name both actors | ✓ / ✗ / N/A |
| CON-005-07 | Response families described in business terms | ✓ / ✗ / N/A |
| CON-005-08 | Schema descriptions are concept statements | ✓ / ✗ / N/A |
| CON-005-09 | Every property has description + assignee | ✓ / ✗ / N/A |
| CON-005-10 | Formal prose + normative keywords | ✓ / ✗ / ⚠️ |
| CON-005-11 | Action schemas carry `Action` suffix | ✓ / ✗ / N/A |
| CON-005-12 | Stateful APIs use noun paths + REST verbs | ✓ / ✗ / N/A |
| CON-005-13 | Directory name matches schema name | ✓ / ✗ / N/A |
| CON-005-14 | Schema pack has all 5 required files | ✓ / ✗ / N/A |
| CON-005-15 | Terms map to `beckn:` IRI or external vocab | ✓ / ✗ / N/A |
| CON-005-16 | Resource identifiers in path parameters | ✓ / ✗ / N/A |
| CON-005-17 | Stateful async callbacks use same resource path; no `on_*` | ✓ / ✗ / N/A |
| CON-005-18 | N/A at proposal stage — applies to PR | N/A |
| CON-005-19 | N/A at proposal stage — applies to PR | N/A |

Mark ⚠️ where the Discussion does not provide enough detail to assess.

---

## Step 6 — Produce the Review

```
## Proposal Review — [Discussion Title] (#[number])
**Repository:** [repo]
**Discussion category:** [Proposals / Ideas / other]
**Proposal type:** [type]
**Target layer:** [Core P2P / In-Fabric stateful / Schemas / Adapter specs / On-Fabric implementations]
**Proposed artifact(s):** [list]

---

## TL;DR

### Recommended Action — Working Group

**[One crisp instruction: Approve for Protocol Draft PR / Request revisions / Reject]**

[2–4 bullets: the most important findings. For rejections: what must change.
For approvals: any SHOULD items to note.]

---

### Recommended Action — Proposal Author

**[Numbered action list]**

---

### RFC Lifecycle
[PASS / FAIL — reason if fail]

### Design Principles Gate (NFH-001)
[PASS / FAIL per principle — reason for any fail]

### Stack Layer Assessment
[PASS / FAIL — evidence from Motivation section that higher layers were considered]

### Findings

#### MUST Violations (block approval)
- **[CON-005-xx or rule]:** [Found] → [Required]

#### SHOULD Violations (address before approval)
- **[Rule]:** [Found] → [Recommended]

#### Cannot Assess (insufficient detail)
- **[CON-005-xx]:** [What is missing]

---

### Conformance Table
[Full table from Step 5]

---

### Verdict
[One of:]
- ✅ READY FOR WORKING GROUP APPROVAL — No MUST violations. Lifecycle checks pass.
- ⚠️ CONDITIONALLY READY — SHOULD violations noted; author should address before WG vote.
- 🚫 NOT READY — [N] MUST violation(s). Proposal must be revised before WG consideration.
- ✗ WRONG LIFECYCLE STAGE — See RFC Lifecycle section above.

### Required Actions Before Working Group Approval
[Numbered list of concrete changes]
```

---

## Legacy Exception Handling

Known legacy exceptions — do NOT apply new rules retroactively to these, but DO flag if a new proposal models itself on them:

- `/catalog/publish`, `/catalog/on_publish`, `/catalog/subscription`, `/catalog/pull`, `/catalog/on_pull` — RPC-style, `on_*` callbacks on stateful APIs, query parameters for resource IDs. MUST NOT be used as design precedent.
- `status` endpoint — noun exception; preserved but not a model.
- `discover` — 3-syllable exception; preserved but not a model.

Registry protocols are out of scope. Any proposal touching registry protocols MUST be redirected to Linux Foundation Decentralized Trust governance.

---

*Skill based on NFH-001, NFH-005, NFH-006, GOVERNANCE.md. Canonical sources: protocol-specifications-v2/draft branch.*
