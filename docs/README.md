# Beckn Protocol 2.0 Specifications

## Specification

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described [here](./Keyword_Definitions.md). These definitions aim to ensure that the terms are understood precisely and consistently to avoid confusion in the interpretation of standards, specifications, and protocols.

## Before Proposing Changes

Any contributor proposing amendments, additions, or revisions to this specification MUST read and demonstrate understanding of the following documents before opening an issue, pull request, or discussion:

- [Code of Conduct](../CODE_OF_CONDUCT.md) — Governs the standards of conduct expected of all participants in the Beckn protocol community.
- [Governance Model](../GOVERNANCE.md) — Defines the decision-making structure, working group responsibilities, and RFC lifecycle by which this specification evolves.
- [Contributing Guide](../CONTRIBUTING.md) — Specifies the contribution workflow, branch conventions, review process, and acceptance criteria for proposed changes.

Proposals that do not comply with these documents are subject to immediate closure without review.

## Suggested Order of Reading

The documents in this specification are best read in the following sequence. Each document builds on the concepts established by those before it.

### 1. [NFH-001 — Specification: Architecture, Design Philosophy and Principles](./Specification.md)
Start here. Establishes the *why* behind Beckn Protocol v2 — the architectural philosophy, design constraints, and derived principles that govern every decision in the specification. Reading this first ensures the remainder of the specification is understood in the correct context.

### 2. [NFH-002 — Keyword Definitions](./Keyword_Definitions.md)
Defines the normative interpretation of requirement-level keywords (`MUST`, `SHOULD`, `MAY`, etc.) used throughout all documents. Read before proceeding to any normative specification content.

### 3. [NFH-003 — The Beckn Protocol Stack](./The_Beckn_Protocol_Stack.md)
Describes the six-layer structure of the protocol — networking, trust, data, semantics, policy, and application. Provides the structural map needed to understand where each subsequent document fits.

### 4. [NFH-004 — Core Data Schema](./Core_Data_Schema.md)
Defines how implementers navigate Beckn schema assets across OpenAPI contracts and core schema objects. Read before the API document, since the API operates on these data structures.

### 5. [NFH-005 — Linked Data Schema](./Linked_Data_Schema.md)
Covers the JSON-LD semantic layer built on top of the core schema. Explains how Beckn achieves semantic interoperability across domains and regions through linked data artifacts.

### 6. [NFH-006 — Beckn API Endpoints](./API.md)
Defines the full endpoint surface for Beckn v2.0.0 — action and callback lifecycle semantics, common envelopes, and implementation constraints derived from the canonical OpenAPI contract.

### 7. [NFH-007 — Authentication and Trust](./Authentication_and_Trust.md)
Specifies the Ed25519-based authentication and non-repudiation model that secures every message leg between network participants. Read after the API document to understand what is being secured and how.

### 8. [NFH-008 — Handling Exceptions and Errors](./Error_Codes.md)
Defines the canonical error taxonomy, ACK/NACK semantics, and error propagation model. Read after understanding the API and authentication layers that produce these errors.

### 9. [NFH-009 — Specification Design Guide](./Design_Guide.md)
Normative authoring rules for Beckn API specifications, schemas, and artifacts. Required reading for anyone contributing to or extending the specification.

### 10. [NFH-010 — RFC Authoring Guide](./RFC_Authoring_Guide.md)
Process and governance guide for authoring, reviewing, and publishing RFC submissions. Read this before opening any Proposal Discussion or Pull Request.

### 11. [NFH-011 — RFC Template](./RFC_Template.md)
The canonical template to be used when authoring a new RFC. Use in conjunction with NFH-010.

---

For a full publication summary including authors, dates, and status, see [RFC_Publication_Summary.md](./RFC_Publication_Summary.md).
