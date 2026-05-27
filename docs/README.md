## Beckn Protocol v2.0 Documentation

This folder contains the normative RFC documents that constitute the Beckn Protocol v2.0 specification. Each document is authored using the RFC template ([NFH-011](./RFC_Template.md)), reviewed by the Core Working Group, and published under the governance model defined in [GOVERNANCE.md](../GOVERNANCE.md). Documents progress through the RFC lifecycle — Idea, Proposal, Protocol Draft, Protocol Standard — before becoming normative. All documents in this folder are at Protocol Standard status unless their metadata indicates otherwise.

#### Specification

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described [here](./Keyword_Definitions.md). These definitions aim to ensure that the terms are understood precisely and consistently to avoid confusion in the interpretation of standards, specifications, and protocols.

**Required reading before opening any issue, pull request, or discussion:**

 - [Code of Conduct](../CODE_OF_CONDUCT.md)
 - [Governance Model](../GOVERNANCE.md)
 - [Contributing Guide](../CONTRIBUTING.md)

#### Suggested Order of Reading

The documents in this specification are best read in the following sequence. Each document builds on the concepts established by those before it.

**1. [NFH-001 — Specification: Architecture, Design Philosophy and Principles](./Introduction.md)**
Start here. Establishes the *why* behind Beckn Protocol v2 — the architectural philosophy, design constraints, and derived principles that govern every decision in the specification. Reading this first ensures the remainder of the specification is understood in the correct context.

**2. [NFH-002 — Keyword Definitions](./Keyword_Definitions.md)**
Defines the normative interpretation of requirement-level keywords (`MUST`, `SHOULD`, `MAY`, etc.) used throughout all documents. Read before proceeding to any normative specification content.

**3. [NFH-006 — Beckn API Endpoints](./API.md)**
Defines the full endpoint surface for Beckn v2.0.0 — action and callback lifecycle semantics, common envelopes, and implementation constraints derived from the canonical OpenAPI contract.

**4. [NFH-013 — Beckn Communication Model](./Communication_Protocol.md)**
Defines how two Beckn nodes exchange messages: the asynchronous request–callback pattern, Ack/Nack semantics, how `context.messageId` correlates a callback to its originating request, how `context.transactionId` groups all messages in a business transaction, and how Provider Nodes may push unsolicited or repeated callbacks without the Consumer Node polling.

**5. [NFH-007 — Authentication and Trust](./Authentication_and_Trust.md)**
Specifies the Ed25519-based authentication and non-repudiation model that secures every message leg between network participants. Read after the API document to understand what is being secured and how.

**6. [NFH-012 — Schema Design Guide](./Schema_Design_Guide.md)**
Governs how Beckn schemas are designed, authored, published, and consumed. Establishes Agent-First Design — schemas authored *with* AI for AI agents — alongside Semantic Invariance, Unification over Standardization, and the abstraction → composition → extension → creation precedence.

**7. [NFH-010 — RFC Authoring Guide](./RFC_Authoring_Guide.md)**
Process and governance guide for authoring, reviewing, and publishing RFC submissions. Read this before opening any Proposal Discussion or Pull Request.

**8. [NFH-011 — RFC Template](./RFC_Template.md)**
The canonical template to be used when authoring a new RFC. Use in conjunction with NFH-010.

---

For a full publication summary including authors, dates, and status, see [RFC_Publication_Summary.md](./RFC_Publication_Summary.md).
