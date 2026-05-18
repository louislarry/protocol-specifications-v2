# Specification : Architecture, Design Philosophy and Principles
> Request for Comments
## Document Details

- **ID:** NFH-001
- **Status:** Draft.
- **Authors:**
  - [Ravi Prakash](https://github.com/ravi-prakash-v), [Networks for Humanity](https://networksforhumanity.org)
- **Created:** 2026-05-11
- **Updated:** 2026-05-11
- **Version history:** No commits found on `main` for `docs/02_Design_Philosophy.md`.
- **Latest editor's draft:** Click [here](https://github.com/beckn/protocol-specifications-v2/blob/draft/docs/02_Design_Philosophy.md).
- **Implementation report:** Not available. This document is at Initial Draft status; report will be linked in the next formal release of this RFC, following merge to main.
- **Stress test report:** Not available. This document is at Initial Draft status; report will be linked in the next formal release of this RFC, following merge to main.
- **Conformance impact:** Not determined. This document is at Initial Draft status; impact will be classified in the next formal release of this RFC, following merge to main.
- **Security/privacy implications:** Defines security-by-design architecture constraints, including signature and receipt semantics.
- **Replaces / Relates to:** Supersedes the prior non-template version of `02_Design_Philosophy.md`; aligned with `api/v2.0.0/beckn.yaml` and Beckn architecture documentation.
- **Feedback - Issues:** Click [here](https://github.com/beckn/protocol-specifications-v2/issues?q=is%3Aissue+label%3A%22RFC-002%22).
- **Feedback - Discussions:** Click [here](https://github.com/beckn/protocol-specifications-v2/discussions?discussions_q=label%3A%22RFC-002%22).
- **Feedback - Pull Requests:** Click [here](https://github.com/beckn/protocol-specifications-v2/pulls?q=is%3Apr+label%3A%22RFC-002%22).
- **Errata:** To be published.

## Abstract

This RFC defines the architectural philosophy and derived principles that guide Beckn Protocol v2 decisions, aligning transport contracts, asynchronous interaction patterns, catalog-first discovery, and contract-centric modeling with the canonical v2 artifacts and documentation.

## Table of Contents

- [Specification : Architecture, Design Philosophy and Principles](#specification--architecture-design-philosophy-and-principles)
  - [Document Details](#document-details)
  - [Abstract](#abstract)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Specification](#specification)
    - [Design Principles](#design-principles)
    - [Network Actors](#network-actors)
    - [API Surface and Interaction Model](#api-surface-and-interaction-model)
    - [Conformance Requirements and Alignment Notes](#conformance-requirements-and-alignment-notes)
    - [Security, Migration, and Evolution Notes](#security-migration-and-evolution-notes)
    - [Examples](#examples)
  - [Conclusion](#conclusion)
  - [Acknowledgements](#acknowledgements)
  - [References](#references)

## Introduction

Beckn has evolved into a multi-service value-exchange fabric spanning discovery, transaction, fulfillment, post-fulfillment, and infrastructure APIs. Without a formal architectural baseline, changes to API surface, actor roles, transport behavior, and schema semantics can drift across implementations. This RFC provides that baseline so protocol evolution remains coherent and aligned with the canonical v2 artifacts.

The architectural intent is to keep transport behavior explicit, preserve semantic interoperability across domains and regions, and allow new actor roles and value-exchange patterns to emerge without redesigning the core structure. This motivates a catalog-first discovery model, asynchronous business workflows with synchronous acknowledgements, and generalized contract abstractions that remain reusable across use cases.

## Specification

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described [here](./Keyword_Definitions.md). These definitions aim to ensure that the terms are understood precisely and consistently to avoid confusion in the interpretation of standards, specifications, and protocols.

### Design Principles

1. **Decentralization**: Any evolution in the protocol MUST enable decentralization of the associated ecosystem. In the context of value-exchange, the further we move towards the edges of a value-exchange transaction, the more choice, optionality, and agency MUST emerge as a consequence. 
2. **Fabric-driven:** Any evolution in the protocol MUST emerge as a consequence of evolution in the NFH Fabric. That means, any feature request MUST be a fabric feature request and not a protocol feature request. Based on the discussions following the feature request, a decision whether to support that feature as a run-time fabric feature, or a protocol feature will be taken. 
3. **Agent-first:** The protocol MUST first leverage AI for its evolution _and_ also empower AI Agents to participate in trusted, value-exchange transactions via unstructure. Any evolution in the protocol MUST primarily be enabled for AI Agents while keeping the human-enablement secondary. However this principle does NOT mean that all features are ONLY usable by AI. It should first be usable by AI, and then be usable by humans. But BOTH are required for the time being.  
4. **Pragmatism:** Not ALL systems today are AI-native. While Beckn requires an AI-first approach to its evolution, it does NOT eliminate the need for humans altogether. Therefore, architecture decisions SHOULD also keep in mind the practical implications on non-AI-native systems, current ecosystem tooling, and developer friendliness.
5. **Semantic interoperability:** Protocol concepts MUST be interpreted consistently across domains, regions, and implementations. 
6. **Reusability via abstraction:** Core concepts MUST remain abstract enough to be reused across diverse domains and regional deployments.
7. **Trust by design:** Mandatory signatures and `CounterSignature` acknowledgements MUST remain baseline transport behavior.

### Network Actors

Beckn Protocol v2 specification is designed to run as a layered stack built on a Universal Value Exchange Fabric:

1. Communication Protocol
2. API Specification
3. Composable Linked-Data Schema
4. Workflows

Core roles in v2 include CN, PN, Discovery Service (DS), and Registry.

High-level interaction shape:

```text
PN -> CP -> DS -> CN discovery
CN <-> PN transaction lifecycle
All actors <-> Registry for trust resolution
```

This topology preserves separation of concerns: infrastructure actors resolve discovery and trust, while transaction participants execute the lifecycle using shared transport and schema rules.

### API Surface and Interaction Model

`api/v2.0.0/beckn.yaml` MUST be treated as the canonical v2.0.x interoperability artifact.

The v2.0.0 OpenAPI contract currently defines 30 paths grouped as:

- Discovery
- Transaction
- Fulfillment
- Post-Fulfillment
- Catalog Publishing
- Catalog Subscription
- Catalog Pull
- Master Resource Search

Beckn APIs SHOULD remain action-addressable through named paths per action to preserve implementability and observability. Discovery SHOULD remain catalog-first rather than relying on runtime multicast fan-out. Forward requests SHOULD be acknowledged synchronously, and business outcomes MAY be returned asynchronously through `on_*` callbacks.

The request envelope MUST include `context` and `message`. Implementations MUST enforce `Authorization` signature validation and MUST support standard response families: `Ack`, `AckNoCallback`, `NackBadRequest`, `NackUnauthorized`, and `ServerError`. The transaction model SHOULD remain centered on generalized `Contract` entities and related abstractions for cross-domain compatibility. Schema semantics SHOULD remain composable through JSON-LD-compatible extension containers.

### Conformance Requirements and Alignment Notes

Architecture-level protocol changes to envelope, security, or acknowledgement semantics MUST be reviewed as interoperability-impacting changes. Implementations MUST treat `api/v2.0.0/beckn.yaml` as the source contract for v2.0.x endpoint and envelope behavior. Beckn deployments SHOULD preserve asynchronous request and callback semantics for lifecycle actions. Infrastructure capabilities such as publish, subscribe, pull, and search SHOULD be implemented as protocol-visible APIs where applicable.

### Security, Migration, and Evolution Notes

This RFC reinforces security-by-design through mandatory request signatures and signed acknowledgements. No new cryptographic primitive is introduced by this document. The main security risk addressed is trust ambiguity caused by inconsistent transport semantics across implementations.

No protocol wire migration is introduced by this RFC. This update is editorial and structural: it aligns architecture philosophy with the standard RFC structure and with existing v2.0.0 behavior.

The following evolution questions remain open and inform future work:

1. Slash and underscore action aliasing may need formal deprecation over a defined release window.
2. Actor capability profiles for Fabric Nodes, PN, CS, and DS may need publication as a separate normative RFC.

### Examples

Example layered architecture view:

```text
Network Architecture
  -> API Specification
    -> Composable Linked-Data Schema
      -> Communication Protocol
        -> Workflows
```

Example protocol path grouping from `beckn.yaml`:

```text
Discovery: /discover, /on_discover
Transaction: /select, /on_select, /init, /on_init, /confirm, /on_confirm
Fulfillment: /status, /on_status, /track, /on_track, /update, /on_update, /cancel, /on_cancel
Post-Fulfillment: /rate, /on_rate, /support, /on_support
Catalog Infra: /catalog/publish, /catalog/on_publish, /catalog/subscription, /catalog/pull, /catalog/master/*
```

## Conclusion

This RFC establishes a durable architectural baseline for Beckn Protocol v2 by consolidating the philosophy, topology, interaction model, and conformance expectations into a single structure. It does not introduce wire-level migration; relative to the initial draft, this revision primarily restructures the RFC and aligns its wording with the canonical v2.0.0 architecture artifacts.

## Acknowledgements

This RFC builds on the Beckn v2 OpenAPI contract, Beckn architecture documentation, and the broader Beckn community effort that shaped the protocol's transport, discovery, and trust model.

## References

- Keyword definitions: Click [here](./00_Keyword_Definitions.md)
- Canonical OpenAPI artifact: `api/v2.0.0/beckn.yaml`
- Beckn protocol overview: Click [here](https://docs.beckn.io/introduction-to-beckn/beckn-protocol)
- Universal Value-Exchange Fabric overview: Click [here](https://docs.beckn.io/introduction-to-beckn/fabric-the-value-exchange-infrastructure)
- Catalog publishing reference: Click [here](https://docs.beckn.io/introduction-to-beckn/fabric-the-value-exchange-infrastructure/publish-catalogs-using-catalg)
- Trusted networks and registry reference: Click [here](https://docs.beckn.io/introduction-to-beckn/fabric-the-value-exchange-infrastructure/build-trusted-networks-using-registr)
