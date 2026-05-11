# Beckn Protocol 2.0 Specifications — Document Index

## Specification

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described [here](./Keyword_Definitions.md). These definitions aim to ensure that the terms are understood precisely and consistently to avoid confusion in the interpretation of standards, specifications, and protocols.

## Before Proposing Changes

Any contributor proposing amendments, additions, or revisions to this specification MUST read and demonstrate understanding of the following documents before opening an issue, pull request, or discussion:

- [Code of Conduct](../CODE_OF_CONDUCT.md) — Governs the standards of conduct expected of all participants in the Beckn protocol community.
- [Governance Model](../GOVERNANCE.md) — Defines the decision-making structure, working group responsibilities, and RFC lifecycle by which this specification evolves.
- [Contributing Guide](../CONTRIBUTING.md) — Specifies the contribution workflow, branch conventions, review process, and acceptance criteria for proposed changes.

Proposals that do not comply with these documents are subject to immediate closure without review.

## Table of Contents

| RFC ID | Title | Description | Authors | Last Updated | Type |
|--------|-------|-------------|---------|--------------|------|
| [NFH-001](./Specification.md) | Specification: Architecture, Design Philosophy and Principles | Defines the architectural philosophy and derived principles that govern Beckn Protocol v2 design decisions. | [Ravi Prakash](https://github.com/ravi-prakash-v) | 2026-05-11 | Protocol Standard — REQUIRED |
| [NFH-002](./Keyword_Definitions.md) | Keyword Definitions | Defines normative interpretations of requirement-level keywords used across all Beckn protocol documents. | [Ravi Prakash](https://github.com/ravi-prakash-v) | 2026-05-11 | Protocol Standard — REQUIRED |
| [NFH-003](./The_Beckn_Protocol_Stack.md) | The Beckn Protocol Stack | Defines the Beckn v2 protocol stack as six layers and specifies how networking, trust, data, semantics, policy, and application concerns interact. | [Ravi Prakash](https://github.com/ravi-prakash-v) | 2026-05-11 | Protocol Standard — REQUIRED |
| [NFH-004](./Core_Data_Schema.md) | Core Data Schema | Defines how implementers navigate Beckn schema assets across OpenAPI contracts, core schema objects, and registry-published versioned artifacts. | [Ravi Prakash](https://github.com/ravi-prakash-v) | 2026-05-11 | Protocol Standard — REQUIRED |
| [NFH-005](./Linked_Data_Schema.md) | Linked Data Schema | Defines how implementers navigate JSON-LD extension containers and linked data artifacts for semantic interoperability. | [Ravi Prakash](https://github.com/ravi-prakash-v) | 2026-05-11 | Protocol Standard — REQUIRED |
| [NFH-006](./API.md) | Beckn API Endpoints | Defines the Beckn v2.0.0 endpoint surface, action and callback lifecycle semantics, and implementation constraints derived from the canonical OpenAPI contract. | [Ravi Prakash](https://github.com/ravi-prakash-v) | 2026-05-11 | Protocol Standard — REQUIRED |
| [NFH-007](./Authentication_and_Trust.md) | Authentication and Trust | Specifies the Ed25519-based authentication and non-repudiation model governing all message legs between Beckn network participants. | [Ravi Prakash](https://github.com/ravi-prakash-v) | 2026-05-11 | Protocol Standard — REQUIRED |
| [NFH-008](./Error_Codes.md) | Handling Exceptions and Errors | Defines the canonical error taxonomy, ACK/NACK semantics, and error propagation model replacing BECKN-005 numeric codes. | [Abhishek Jain](https://github.com/abhimail), [Ravi Prakash](https://github.com/ravi-prakash-v) | 2026-05-11 | Protocol Standard — REQUIRED |
| [NFH-009](./Design_Guide.md) | Specification Design Guide | Defines authoring rules for Beckn API specifications, schemas, and artifacts to ensure naming, semantic, and evolution consistency. | [Ravi Prakash](https://github.com/ravi-prakash-v) | 2026-05-11 | Protocol Standard — REQUIRED |
| [NFH-010](./RFC_Authoring_Guide.md) | RFC Authoring Guide | Process and governance guide for authoring, reviewing, and publishing Beckn RFC submissions to the protocol-specifications-v2 repository. | [Ravi Prakash](https://github.com/ravi-prakash-v) | 2026-05-11 | Protocol Standard — REQUIRED |
| [NFH-011](./RFC_Template.md) | RFC Template | Canonical template for authoring new Beckn Protocol RFC submissions. | [Ravi Prakash](https://github.com/ravi-prakash-v) | 2026-05-11 | Protocol Standard — REQUIRED |
