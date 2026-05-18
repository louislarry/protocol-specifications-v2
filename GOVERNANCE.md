# Beckn Protocol Governance

**Status:** Active  
**Scope:** All repositories governed by the Beckn Core Working Group — `protocol-specifications-v2`, `schemas`, `DEG`, and any derivative protocol repositories.

---

## Introduction

Beckn Protocol is a peer-to-peer, stateless communication protocol for open, decentralized value exchange. It defines how independent systems — built by different teams, in different languages, on different infrastructure, across different domains and regions — can transact with each other without prior arrangement, shared platforms, or centralized intermediaries. The protocol is the only shared contract between these systems. When it is stable, the ecosystem can grow in any direction. When it changes carelessly, it breaks things that were not broken and were not expecting to be.

Most people who encounter Beckn Protocol for the first time think of it as an API specification with some associated schemas. That is understandable — those are the most visible artifacts. But a protocol is not an API. An API describes how a client interacts with a specific service. A protocol describes how any two independently implemented systems can interact with each other in a way that is correct, secure, and semantically consistent — without either system knowing anything about the other's implementation. This distinction is not academic. It determines what kinds of changes are safe, what kinds are dangerous, and why the bar for changing a protocol is fundamentally different from the bar for updating an API.

The Beckn ecosystem is also unusually susceptible to a specific failure mode: domain creep. Beckn Protocol is intentionally domain-agnostic — the same protocol governs commerce, mobility, healthcare, energy, and any other value-exchange domain. This is its primary strength. But contributors typically arrive from a specific domain, with a specific use case, and a natural tendency to solve the immediate problem in front of them. Domain-specific concepts, terminology, and assumptions find their way into proposals for core protocol changes. A field name that makes perfect sense in e-commerce creates ambiguity in healthcare. An endpoint pattern that works for logistics is wrong for financial services. The governance process exists in part to catch and prevent this drift before it becomes permanent.

There is a further compounding factor: stateless P2P protocol design is a specialized discipline that most software engineers have not practiced. The mental model for designing a web API — where you control both the server and the client contract, where you can deploy a fix in minutes, and where a breaking change affects only your own users — does not transfer to protocol design. In a protocol, you do NOT control the implementations on either side. A change you make today will be interpreted by systems that were written before the change and will be written long after it. Ambiguity in a protocol does not produce an error — it produces silent divergence between implementations that each believe they are conformant.

### The Beckn ecosystem stack and its evolution speeds

Not everything in the Beckn ecosystem evolves at the same rate. The stack below is ordered from the slowest-evolving layer at the foundation to the fastest-evolving layer at the periphery. Contributors MUST understand exactly which layer the artifact they are proposing to change sits in — because that determines which governance process applies and how much ecosystem-wide scrutiny is required.

| Layer | Examples | Appropriate evolution speed |
|---|---|---|
| **Core P2P stateless protocol** | `beckn.yaml`, `context.version`, transport semantics, request/response envelope structure, the `on_*` callback pattern | Slowest — changes here affect every implementation in every domain, every region, and every version of the ecosystem globally |
| **In-Fabric stateful protocols** | Catalog Service APIs, Discovery Service APIs, Registry APIs — the Fabric service layer | Slow — changes affect all network participants who depend on Fabric infrastructure |
| **Schemas** | Schema packs in `beckn/schemas`, domain-specific schemas, JSON-LD vocabulary | Moderate — changes propagate across domain extensions but are isolated from transport semantics |
| **Adapter specs** | ONIX and similar translation or bridge layer specifications | Faster — changes are scoped to integration boundaries and do NOT require ecosystem-wide coordination |
| **On-Fabric implementations** | Network-specific policies, domain configurations, application-layer behavior, operator-level rules | Fastest — changes are fully scoped to a specific network or operator context |

> **Note — Registry protocols.** Registry protocols used within the Beckn ecosystem follow the **DeDi (Decentralized Identity) protocol specifications**, hosted under the **Linux Foundation Decentralized Trust** initiative. These protocols operate under Linux Foundation Decentralized Trust governance, NOT this governance model. Changes to registry protocols MUST be proposed and managed through the Linux Foundation Decentralized Trust process. This document has no authority over those specifications.

### Change management by layer

The ordering of this stack is also the ordering of last resort. Every proposed change MUST first be attempted at the outermost layer where it can be fully addressed, and escalated inward only when that layer is genuinely insufficient. The direction of escalation is always from periphery toward core — never the reverse.

When a problem arises in the Beckn ecosystem, contributors MUST ask, in order:

1. **Can this be resolved as an on-Fabric implementation change?** Network policies, operator configurations, and application-layer behavior can almost always absorb use-case-specific requirements without touching any shared artifact. If yes, stop here.
2. **If not, can this be resolved as an adapter spec change?** ONIX and similar adapter layers exist precisely to translate between domain-specific or system-specific requirements and the core protocol. If yes, stop here.
3. **If not, can this be resolved as a schema change?** A new schema, an extended schema, or a domain-specific vocabulary addition in `beckn/schemas` can address most semantic requirements without modifying the transport layer. If yes, stop here.
4. **If not, can this be resolved as an in-Fabric stateful protocol change?** A new Fabric service API or modification to an existing Fabric service can address infrastructure-level requirements without touching the core P2P protocol. If yes, stop here.
5. **Only if none of the above are sufficient:** propose a change to the core P2P stateless protocol. This is the last resort, not the first. A proposal that arrives at this step without demonstrating why each of the four layers above cannot address the requirement will be rejected.

This escalation sequence is the Optimal Ignorance principle applied to the full stack. The core P2P protocol does NOT change because a new platform, domain, use case, or Fabric service was added to the ecosystem. It changes only when no other layer can absorb the requirement — and even then, only after the working group has satisfied itself that this is genuinely true.

This governance model exists to make that principle enforceable.

---

## Why this process is intentionally difficult

The governance model for Beckn Protocol is deliberately designed to make changes hard. This is not a bureaucratic accident — it is a core design decision, and it reflects the same philosophy that governs every stable protocol infrastructure layer in existence.

HTTP does NOT add a new method because a new social media platform was launched. TCP/IP did NOT change because video streaming became popular. The HDMI protocol does NOT introduce a new connector because a new television manufacturer ships a product. In each case, the protocol serves as stable infrastructure on which a diverse, independently developed ecosystem evolves. The protocol's stability is precisely what makes that ecosystem possible.

Beckn Protocol is the same. Downstream network operators, platform builders, and implementers across dozens of domains and regions depend on the protocol's stability for their own systems to function. Every change to the core protocol has the potential to break something, somewhere, at a scale the contributor may not be able to see from their vantage point. A new endpoint added for one network's convenience may silently invalidate a contract relied on by a network on the other side of the world.

The process is hard because the cost of getting it wrong is high, the cost is borne by people other than the person proposing the change, and the cost is often invisible until it is too late.

**Before proposing any change, every contributor MUST ask:** does this protocol need to change, or does my implementation need to change? In most cases, the answer is the latter. The protocol exists to serve the ecosystem. The ecosystem does NOT exist to serve the protocol.

---

## When these rules apply

The requirements in this document are formally binding from the moment this document is merged to the `main` branch of `protocol-specifications-v2`. Until that merge occurs, these rules exist on the `draft` branch as a work in progress and do NOT carry the same binding force as a merged standard.

This creates an unavoidable reality: the process by which this governance model is being authored is itself non-conformant to the process it describes. The Idea → Proposal → Protocol Draft → Protocol Standard lifecycle had not yet been formally established when the initial drafting of this document began. That non-conformance is acknowledged, and it creates no precedent.

No contributor may cite the drafting-period state of this document — or any other governance, conduct, or contributing document currently on the `draft` branch — as justification for violations after these documents are merged to `main`. The fact that these rules were not formally enforceable during their own creation does NOT mean they were not in effect as an intention. It means they were not yet in effect as a standard. Those are different things, and conflating them is itself a bad-faith argument.

At the same time, the draft status of this document does NOT license intentional violations during the drafting period. Submitting a PR without an RFC, bypassing the design-principle gate, or pressuring the working group during a period when these rules are still being written is not technically a violation of a merged standard. It is, however, a violation of the ethical standard that every participant in this community is expected to hold regardless of what the current document status says. The absence of a formal rule does not create permission. It creates an expectation that people in good faith do not need rules to tell them what good faith looks like.

---

## Governance intent

This model governs the evolution of Beckn API contracts and schema contracts across all governed repositories. It applies equally to:

- API surface evolution (endpoints, transport behavior, request/response contracts)
- Schema evolution (core and extension schema behavior, conformance semantics)
- JSON-LD artifact evolution (`context.jsonld`, `vocab.jsonld`)
- RFC authorship, review, and lifecycle progression
- Release cadence and merge discipline

Every protocol change — without exception — MUST be proposed, reasoned, and approved through an RFC before any implementation artifact is submitted. An RFC is not a formality that accompanies a Pull Request. It is the primary artifact of the change. The Pull Request is what an approved RFC looks like in machine-readable form. If the RFC is not approved, the Pull Request does not exist.

The single governing principle is:

> Beckn evolves through logical, testable, ecosystem-conscious improvements to API and schema contracts that are first justified through the RFC process, then approved by the Core Working Group, and only then implemented as normative artifacts.

---

## Design principles gate

All contributions MUST be evaluated against the design principles stated in [NFH-001](./docs/Introduction.md) before formal review begins. A contribution that cannot pass this gate is not review-ready, regardless of its technical quality.

Every proposed change MUST:

1. Enable or preserve decentralization — it MUST increase, NOT reduce, agency at the edges of the network.
2. Emerge from a Fabric requirement — changes driven purely by implementation convenience or platform preference are NOT eligible.
3. Be exercisable by an AI Agent without human intervention at any protocol step.
4. Respect pragmatism — acknowledge the practical impact on non-AI-native implementations.
5. Preserve semantic interoperability — concepts MUST be interpreted consistently across all domains, regions, and implementations.
6. Reuse before adding — existing schemas and endpoints MUST be surveyed and found insufficient before new ones are proposed.
7. Preserve trust by design — signature and acknowledgement requirements MUST remain baseline transport behavior.

A contribution that cannot affirmatively satisfy all seven principles MUST NOT proceed to the RFC stage.

---

## RFC Lifecycle

Every protocol change follows this lifecycle. Each stage is a prerequisite for the next. No stage may be skipped.

### Stage 1 — Idea

**Location:** GitHub Discussions → `Ideas` category  
**Requirement:** None beyond clear articulation of the problem.  
**Purpose:** Establish that the problem is real, understood by the community, and worth the cost of a protocol change. The working group and community respond, ask questions, and signal whether they see the same problem.

An Idea that does NOT generate working group engagement is a signal that the problem may not require a protocol change. Contributors SHOULD take this signal seriously before proceeding.

### Stage 2 — Proposal

**Location:** GitHub Discussions → `Proposals` category  
**Requirement:** A formal RFC authored using the [NFH-006 RFC template](./docs/NFH-006_RFC_Writing_Guide.md), linked to the Idea Discussion.  
**Purpose:** The working group formally evaluates the proposed design against the design principles, the RFC writing standard, and the ecosystem impact. Working group consensus is required to advance.

A Proposal that does NOT reach consensus does NOT proceed. Contributors may revise and resubmit.

### Stage 3 — Protocol Draft

**Location:** `draft` branch (merged via PR after Proposal approval)  
**Requirement:** A PR to the `draft` branch whose diff corresponds precisely to the approved Proposal content. The PR MUST link to the approved Proposal Discussion. The PR MUST pass the RFC Approval Gate defined in [NFH-005](./docs/Design_Guide.md).  
**Purpose:** The approved design is implemented in normative artifacts (`beckn.yaml`, schema packs, JSON-LD files). The PR is subject to technical review against NFH-005.

Upon merge, the RFC reaches Protocol Draft status. It is normative on the `draft` branch but has NOT yet reached standard status.

### Stage 4 — Protocol Standard

**Location:** `main` branch (merged via PR after Protocol Draft review)  
**Requirement:** A PR to the `main` branch. The RFC MUST already exist in the `draft` branch. The PR MUST link at least one Issue of type Bug or Enhancement. The RFC Document Details MUST declare a Protocol Standard type. The RFC `ID` field MUST remain `NFH-TBD` — the actual `NFH-NNN` identifier is assigned automatically on merge by a GitHub Action that scans all NFH-governed repositories for existing IDs and assigns the next available number. See the Branch and release management section for the full ID assignment process.

**Protocol Standard types:**

| Type | Meaning |
|---|---|
| `Protocol Standard - REQUIRED` | All conformant implementations MUST support this feature. |
| `Protocol Standard - RECOMMENDED` | Implementations SHOULD support this feature. |
| `Protocol Standard - NOT RECOMMENDED` | Feature is deprecated, or has failed security or compliance review after publication. Implementations SHOULD NOT implement it in new systems. |

**Purpose:** The change is promoted to a published standard. This is the terminal stage. Changes at this stage affect every conformant implementation in the ecosystem.

---

## Branch and release management

### Branch model

| Branch | Purpose | Who writes |
|---|---|---|
| `draft` | Active development. All Protocol Draft PRs target this branch. | Core Committers via approved PRs |
| `core-v2.x.y-lts-rcX` | Release candidate staging. Cut from `main`. | WG Administrator and designated Core Committers |
| `main` | Published standards. Contains only released, working-group-approved content. | WG Administrator only, via release branch PR |

No contributor may push directly to `main` or to a release branch. All work on `draft` follows the RFC lifecycle described in this document. The release process is the only mechanism by which content moves from `draft` to `main`.

### Release branch naming

Release branches MUST follow this format exactly:

```
core-v2.x.y-lts-rcX
```

Where:
- `x` is the minor version number
- `y` is the patch version number
- `X` is the release candidate number, starting at 1 and incrementing with each candidate for the same version

Examples: `core-v2.1.0-lts-rc1`, `core-v2.1.0-lts-rc2`, `core-v2.2.0-lts-rc1`.

A release branch is cut from the HEAD of `main`, NOT from `draft`. It represents a clean baseline of the current published standard onto which specific approved changes from `draft` are applied.

### Release tag format

Release tags on `main` MUST follow this format:

```
core-v2.x.y-lts
```

The `2` and `lts` components are constant for the foreseeable future. `x` (minor) and `y` (patch) may change at the working group's discretion.

**A merge to `main` does NOT automatically indicate a version number change.** The working group determines whether `x` or `y` increments, whether the tag is moved to the new HEAD, or whether a new tag is created. These are deliberate decisions, not mechanical consequences of merging. The Working Group reserves the right to update version numbers as it deems fit, independently of merge frequency.

**Release version is NOT the same as protocol version.** The release tag (`core-v2.x.y-lts`) is a governance and release management label. It identifies a specific published state of the specification. It is NOT the value of `context.version` in `beckn.yaml`. The `context.version` field is the protocol version string used by all conformant implementations at runtime, and it remains `2.0.0` until explicitly changed in `beckn.yaml` by the working group. A release tag of `core-v2.3.0-lts` does NOT mean `context.version` has changed — it may still be `2.0.0`. The authoritative source for the current `context.version` is always `api/v2.0.0/beckn.yaml`, not the release tag.

### Stage 1 — Cut the release branch

The Working Group Administrator creates the release branch from `main` HEAD once the CWG has determined which Protocol Draft changes are scheduled for the release. The scheduled changes MUST be documented in a release planning Discussion before the branch is cut.

### Stage 2 — Populate the release branch

Approved changes from `draft` that are scheduled for the release are applied to the release branch. The Working Group Administrator or a designated Core Committer applies each change using one of the following methods: manual editing, patch file, or `git cherry-pick`. Each applied change MUST be traceable to a specific merged PR on the `draft` branch.

The population step is submitted as a single PR to the release branch. This PR is a staging review — it is NOT a design review. At this stage, the only permitted activities are:

- Document sanity check — confirm no formatting errors, broken links, or structural inconsistencies were introduced during cherry-pick or patch application.
- Acknowledgements — verify contributor attributions are present and accurate.
- `README.md` updates — version history entries and any other version-specific documentation.
- RFC date fields — update the `Updated` field in the Document Details block of any RFC whose content has changed in this release.

Design changes, scope additions, and schema modifications are NOT permitted at this stage. If a reviewer identifies a design issue, it MUST be returned to `draft` for the standard RFC process and deferred to a future release.

**Contributor License Agreement.** Before the population PR is merged to the release branch, the contributor who opened the PR MUST explicitly confirm their agreement to the Contributor License Agreement (CLA). This confirmation MUST appear as a comment in the PR thread from the contributor's GitHub account. A PR whose CLA agreement is not on record MUST NOT be merged.

### Stage 3 — Release candidate review

Once the release branch is populated, the Working Group Administrator opens a PR from the release branch to `main`. This PR MUST:

- Be reviewed by at least three Core Working Group members.
- Include the Chief Architect of the Protocol Working Group as one of the three required reviewers. The Chief Architect's approval is mandatory — the PR MUST NOT be merged without it.
- Trigger the conformance regression test GitHub Action automatically on opening. The Action performs a comprehensive regression test across ALL NFH-005 conformance checks. The test report MUST be available to reviewers before any approvals are recorded. A PR whose conformance regression report has not passed MUST NOT be approved.

During the release candidate review period, changes MUST be made directly on the release branch. No further cherry-picks or patches from `draft` SHOULD be accepted at this stage. If a defect is discovered during review that requires a fix from `draft`, the Working Group Administrator MUST assess whether:

1. The fix is minor enough to be made directly on the release branch (preferred for release-blocking issues), or
2. The release should be deferred to allow the fix to go through `draft` via the standard RFC process.

### Stage 4 — Merge to `main`

Once the PR has received the required approvals — including the Chief Architect — and the conformance regression report is clean, the Working Group Administrator merges the release branch PR to `main`.

**RFC ID assignment.** On merge to `main`, a GitHub Action is triggered that automatically assigns RFC IDs to all RFCs in the release whose `ID` field is still `NFH-TBD`. The Action:

1. Scans all NFH-governed repositories across the organization to collect all currently assigned `NFH-NNN` IDs.
2. Determines the next available ID(s) sequentially.
3. Updates the `ID` field in the Document Details block of each qualifying RFC in the merged content.
4. Commits the ID assignments directly to `main` as a single automated commit, recorded against the WG Administrator account.

No human intervention is required for ID assignment. If the Action fails, the merge is NOT rolled back, but the WG Administrator MUST resolve the ID conflict manually before the release announcement is published.

**Release tagging.** After merge, the Working Group Administrator determines the release tag action. A merge to `main` does NOT automatically trigger a version number change — the tag decision is a deliberate working group call, NOT a mechanical consequence of merging:

| Condition | Tag action |
|---|---|
| No breaking changes; existing implementations remain conformant | The existing release tag MAY be moved to the HEAD of `main`. No version number change is required. |
| Breaking changes introduced; implementations must update | A new release tag MUST be created at the HEAD of `main`. `x` or `y` is incremented at working group discretion. |
| Minor administrative or editorial changes only | The existing tag MAY be retained at its current position with no movement. |

Regardless of which tag action is taken, an announcement MUST be published in the repository Discussions within 24 hours of the merge. The announcement MUST state: the release tag name, whether the tag was moved, created, or left unchanged, the RFC IDs assigned during this release, and a summary of the changes included. The announcement MUST link to the release PR and the conformance regression report.

### Stage 5 — Back-merge and cleanup

After the release branch is merged to `main`, all changes that were made directly on the release branch during the release candidate review period MUST be merged back to `draft`. This ensures `draft` reflects any release-stage corrections and does NOT diverge from the published standard.

The back-merge to `draft` is submitted as a PR by the Working Group Administrator and requires a single Core Committer approval.

Once the back-merge is confirmed, the release branch MUST be deleted. Retaining stale release branches is NOT permitted.

### Release branch lifecycle summary

```
main (HEAD)
  │
  ├── cut release branch ──► core-v2.x.y-lts-rc1
  │                              │
  │                              ├── cherry-pick from draft
  │                              ├── sanity check + CLA PR
  │                              ├── [rc2, rc3 if needed]
  │                              └── conformance regression passes
  │
  ◄── PR reviewed by ≥3 CWG members (incl. Chief Architect) ──────────┘
  │
  ├── merged to main
  ├── GitHub Action assigns NFH-xxx IDs to all NFH-TBD RFCs
  ├── release tag moved, created, or unchanged (WG decision)
  ├── announcement published (incl. assigned RFC IDs)
  ├── back-merge to draft
  └── release branch deleted
```

---

## Review cadence

The Core Working Group reviews Protocol Draft PRs on a scheduled cycle. Schedule is published in the repository Discussions.

Review cadence reflects the principle that stability is a feature. Frequent releases are NOT a goal.

---

## Never Push the Red Button

The rule is: never push the red button. This section exists because, in the rarest of circumstances, someone has to.

### When the exception applies

A direct, process-bypassing merge to `main` is permitted only when ALL of the following conditions are simultaneously true:

1. A feature or change that was previously merged to `main` has introduced a **Severity 3 bug** in one or more production systems — meaning a live, deployed implementation that is actively serving real transactions is materially broken, degraded, or producing incorrect protocol behavior as a direct consequence of the merged change.
2. The bug cannot be mitigated at the implementation layer without a corresponding spec change.
3. Every hour of delay in applying the fix causes measurable, documented harm to the ecosystem.

A Severity 3 bug is a production-breaking regression traceable to a specific merged commit. Performance degradation, suboptimal behavior, or theoretical security concerns that have not manifested in production do NOT qualify. If there is debate about whether the severity threshold is met, it is NOT met.

### Who has authority

In a qualifying emergency, the **Chief Architect of the Networks for Humanity Foundation** MAY adopt a Benevolent Dictator (BD) governance posture for the duration of the emergency. In this posture, the Chief Architect has the authority to:

- Override the RFC lifecycle requirement for the hotfix.
- Override the working group approval requirement.
- Merge the hotfix directly to `main` without a prior Proposal Discussion or Protocol Draft stage.
- Delegate merge approval rights to one or more named organization administrators by explicitly recording that delegation in the emergency PR thread before the merge is executed.

The BD posture is temporary. It expires the moment the hotfix is merged. No other governance authority is affected. The Chief Architect does NOT acquire ongoing authority over any other decision by virtue of invoking this mechanism.

The Chief Architect's decision to invoke this mechanism is final and is NOT subject to working group override during the emergency. It IS subject to retrospective review at the next working group meeting.

### Emergency process

When the Chief Architect determines the exception is warranted:

1. An emergency meeting of the Core Working Group MUST be convened as soon as possible. The Chief Architect MUST notify all CWG members immediately via the designated emergency channel. If a quorum cannot be assembled, the Chief Architect MAY proceed without it, with the emergency meeting held within 48 hours.
2. The hotfix PR MUST be opened against `main`. The PR description MUST document: the Severity 3 bug being addressed, the specific merged commit responsible, the scope of the fix, and — if authority is being delegated — the names of the delegated approvers.
3. The hotfix MUST be merged by the Chief Architect or an explicitly delegated organization administrator.
4. Immediately upon merge to `main`, the change MUST be propagated to the `draft` branch. The Working Group Administrator MUST post an announcement to all contributors in the repository Discussions requesting that they rebase, pull, or otherwise update their working branches against the new `main` state. The announcement MUST clearly state the nature of the emergency change and the commits affected.

### Obligations after the emergency

The emergency is not over when the hotfix is merged. The following MUST occur:

- The emergency change MUST be the first agenda item at the next scheduled Core Working Group meeting, with no exceptions.
- A Root Cause Analysis (RCA) MUST be completed and documented in a GitHub Discussion before that meeting. The RCA MUST identify: what was merged that caused the regression, why the regression was not caught during review, and what process, tooling, or conformance gap allowed it to reach production.
- Mitigation strategies MUST be proposed, documented, and assigned to owners in that same meeting.
- The hotfix itself MUST be retroactively documented as a post-hoc RFC — authored using the NFH-006 template, submitted to the `Proposals` Discussion category, and formally approved by the working group so that the change appears in the RFC record. The post-hoc RFC MUST be linked from the emergency PR.

The failure to complete the RCA and retroactive RFC within 30 days of the emergency merge is itself a governance violation subject to the enforcement provisions of this document.

---

## Governance health reporting

The Working Group Administrator MUST publish a governance health report to the repository Discussions once per calendar month. The report MUST include:

- The number of PRs closed at the RFC gate (CON-005-18) during the reporting period, categorized by failure type (lifecycle bypass, stage mismatch, scope violation).
- The number of PRs closed for CON-005-01 through CON-005-19 violations by conformance ID.
- The number of Code of Conduct notices, suspensions, restrictions, and removals issued during the period.
- Any emergency hotfix invocations during the period and their RCA status.

This report serves a purpose beyond accountability. A consistently high rate of RFC gate failures may indicate that the RFC template (NFH-006) is unclear, that the Design Guide (NFH-005) requirements are not well understood, or that the onboarding process is inadequate. A high rate of the same conformance violation across multiple contributors is a signal that the requirement needs clarification, not just enforcement.

A sustained pattern of violations across multiple reporting periods MUST trigger a formal working group agenda item to evaluate whether the design principles (NFH-001), the Design Guide (NFH-005), or the governance model itself have become too idealistic or too detached from the practical realities of the ecosystem. The governance model is not exempt from the same scrutiny it demands of protocol changes. If it is not working, it MUST be changed through the RFC process.

The report is informational and does NOT require working group approval before publication. It MUST be factual, anonymized at the individual contributor level unless a CWG enforcement action is being specifically noted, and linked to the relevant threads where applicable.

---

## Enforcement and contributor access

Contributions that bypass the RFC lifecycle, skip the design-principle gate, or violate the Code of Conduct are closed without merge.

Repeated violations result in escalating access restrictions:

1. First violation — PR closed with documented reason. Contributor notified.
2. Repeated violations — PR submission privileges suspended.
3. Continued violations — Issue submission and Discussion participation restricted.
4. Severe or persistent violations — Contributor removed from the organization.

A contributor who has been removed and wishes to be reinstated MUST submit a formal written request to the Working Group Administrator identifying the root cause of the violation and the remediation taken. The Core Working Group reserves the right to accept or deny such requests.

---

## Working group membership

### Roles

The Core Working Group (CWG) consists of the following roles:

| Role | Authority |
|---|---|
| **Chief Architect** | Held by the designated NFH Chief Architect. Final authority on design decisions, Benevolent Dictator (BD) emergency powers, membership decisions, and cross-repository governance. |
| **Working Group Administrator** | Manages meeting cadence, publishes governance health reports, maintains the RFC registry, and executes administrative actions delegated by the Chief Architect. |
| **Core Committer** | Reviews and merges PRs to the `draft` branch. Participates in Protocol Draft and Protocol Standard review cycles. Has write access to governed repositories. |
| **Working Group Member** | Participates in RFC review, design discussions, and working group votes. Does NOT have merge authority. |

### Adding a working group member

Working group membership is by invitation, not by application. The process is:

1. **Nomination.** Any existing Core Committer or the Chief Architect may nominate a contributor for working group membership. The nominee MUST have a demonstrated record of conformant contributions to at least one governed repository — meaning at least one RFC that has successfully reached Protocol Draft status through the standard process. A contributor who has not yet submitted a conformant RFC is NOT eligible for nomination.

2. **Working group vote.** The nomination is posted to the working group's private channel with a seven-day comment period. Existing Core Committers vote. A simple majority of active Core Committers is required. The Chief Architect may appoint directly without a vote for the initial working group formation or in cases where the nominee's contribution record clearly satisfies the eligibility criteria and no objections are received.

3. **Acceptance conditions.** Before accepting, the nominee MUST confirm in writing that they have read and understood: [NFH-001](./docs/Introduction.md), [NFH-005](./docs/Design_Guide.md), [NFH-006](./docs/NFH-006_RFC_Writing_Guide.md), [GOVERNANCE.md](./GOVERNANCE.md), [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md), and [CONTRIBUTING.md](./CONTRIBUTING.md). Acceptance without this confirmation is NOT valid.

4. **Role assignment.** The Working Group Administrator adds the new member to the relevant GitHub team and announces the addition in the repository Discussions with the member's role and the effective date.

### When a working group member leaves

A working group member who chooses to leave MUST:

1. Post a formal departure announcement in the repository Discussions. The announcement MUST name their successor or explicitly acknowledge that maintenance responsibilities are being returned to the Chief Architect, and MUST state an effective date.
2. Complete any open review assignments or formally hand them off to another Core Committer before the effective date.
3. Transfer any relevant context, decisions-in-progress, or unresolved review threads to the Working Group Administrator.

Upon receiving the departure announcement, the Chief Architect reviews the departing member's role and access, and takes one of the following actions:

| Action | When appropriate |
|---|---|
| **Convert to external collaborator** | The member remains a valued community participant and may continue contributing via the standard governance process. GitHub access is reduced to read-only or per-repository collaboration where relevant. |
| **Remove from GitHub teams only** | The member's organizational membership is retained but their team-based write access is revoked. Suitable when the departure is temporary or the member may return. |
| **Remove from the organization** | The member's departure is complete and they have no ongoing role. They remain welcome to contribute as an open-source community contributor via the standard governance process — Idea → Proposal → Protocol Draft — with no special access. |

The Chief Architect MUST post the access decision to the repository Discussions within 14 days of the effective departure date. The decision is the Chief Architect's alone and is NOT subject to working group vote.

### Departure due to Code of Conduct violation

When a working group member is removed for a Code of Conduct violation — whether the violation occurred during their tenure or was discovered after — the departure does NOT follow the standard process above. The Chief Architect MAY:

- Remove the member from all GitHub teams and the organization immediately and without prior notice.
- Ban the former member from the organization, preventing future contributions in any capacity, including as an open-source community contributor.
- Blacklist the former member, which prohibits participation across all governed repositories and any other spaces associated with the Beckn Core Working Group.

In cases of ban or blacklist, the former member may submit a reinstatement request to the Working Group Administrator after a minimum of twelve months. The request MUST follow the reinstatement process defined in [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md). Reinstatement from a ban or blacklist requires explicit approval from the Chief Architect and is NOT subject to working group vote.

---

## Cross-repository applicability

This governance model applies uniformly across all repositories governed by the Beckn Core Working Group. A contributor who is removed from one repository for governance violations may have those restrictions applied across all governed repositories at the CWG's discretion.

Governed repositories include but are not limited to: `protocol-specifications-v2`, `schemas`, `DEG`.

---

## Related documents

- [NFH-001 — Architecture and Design Principles](./docs/Introduction.md)
- [NFH-005 — Specification Design Guide](./docs/Design_Guide.md)
- [NFH-006 — RFC Writing Guide](./docs/NFH-006_RFC_Writing_Guide.md)
- [CONTRIBUTING.md](./CONTRIBUTING.md)
- [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md)
