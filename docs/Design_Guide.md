# Specification Design Guide

## Status of this document

This document is a Working Draft of the Beckn Protocol Specification, published by the Networks for Humanity Foundation. It is subject to change without notice. Feedback may be submitted via the issue tracker linked in the Document Details section.

## Copyright Notice

Copyright © 2026 Networks for Humanity Foundation. Licensed under [CC-BY-NC-SA 4.0 International](https://creativecommons.org/licenses/by-nc-sa/4.0/).

## Document Details

- **ID:** NFH-009
- **Publication Status:** Draft.
- **Authors:**
  - [Ravi Prakash](https://github.com/ravi-prakash-v), [Networks for Humanity](https://networksforhumanity.org)
- **Created:** 2026-05-11
- **Updated:** 2026-05-11
- **Version history:** Draft-01 (2026-04-10): Initial publication as RFC-005. Restructured from `05_Specification_Authoring_Style_Guide.md` into RFC form. Draft-02 (2026-05-11): Mandated path parameters for stateful resource identifiers; replaced `on_*` callback convention for stateful async APIs with REST callback convention; added RFC Approval Gate section; added CON-005-16, CON-005-17, CON-005-18, and CON-005-19.
- **Latest editor's draft:** Click [here](https://github.com/beckn/protocol-specifications-v2/blob/release-v2.0.0-lts/docs/Design_Guide.md).
- **Implementation report:** Not available. This document is at Initial Draft status; report will be linked in the next formal release of this RFC, following merge to main.
- **Stress test report:** Not available. This document is at Initial Draft status; report will be linked in the next formal release of this RFC, following merge to main.
- **Conformance impact:** Not determined. This document is at Initial Draft status; impact will be classified in the next formal release of this RFC, following merge to main.
- **Security/privacy implications:** Reduces semantic ambiguity that can cause unsafe processing or misinterpretation.
- **Replaces / Relates to:** Replaces non-RFC-form content in `05_Specification_Authoring_Style_Guide.md`.
- **Feedback:** Issues Click [here](https://github.com/beckn/protocol-specifications-v2/issues?q=is%3Aissue+label%3A%22RFC-005%22), Discussions Click [here](https://github.com/beckn/protocol-specifications-v2/discussions?discussions_q=label%3A%22RFC-005%22), Pull Requests Click [here](https://github.com/beckn/protocol-specifications-v2/pulls?q=is%3Apr+label%3A%22RFC-005%22).
- **Errata:** To be published.

## Abstract

This RFC defines authoring rules for Beckn API Specifications, Fabric-aware schema, JSON-LD artifacts, and supporting documentation so that naming, semantics, validation, and backward-compatible evolution remain consistent across repositories and teams.

## Disclaimer

This design guide is a recent addition to the Beckn Protocol Specification. As a result, a number of schemas, API endpoints, and artifacts that are currently live or in active use by the community may not fully conform to the rules defined here. Such artifacts SHOULD be treated as **legacy exceptions** and do not invalidate this guide.

Legacy exceptions will be progressively evaluated for migration toward conformant design. The timing and scope of each migration will be determined by careful assessment of ecosystem impact, implementer readiness, and backward-compatibility constraints. Until formally migrated, legacy artifacts MUST be explicitly identified as exceptions wherever they are referenced in this or any related specification.

## Table of Contents

- [Status of this document](#status-of-this-document)
- [Copyright Notice](#copyright-notice)
- [Document Details](#document-details)
- [Abstract](#abstract)
- [Disclaimer](#disclaimer)
- [Introduction](#introduction)
- [Specification](#specification)
  - [Definitions](#definitions)
- [Scope and Audience](#scope-and-audience)
- [Core Principles](#core-principles)
  - [Naming](#naming)
- [Designing API Endpoints](#designing-api-endpoints)
  - [Naming Convention](#naming-convention)
    - [For Stateless APIs](#for-stateless-apis)
    - [For Stateful APIs](#for-stateful-apis)
      - [Path Parameters](#path-parameters)
      - [Async Callbacks](#async-callbacks)
    - [Casing Rules](#casing-rules)
  - [Writing Descriptions](#writing-descriptions)
  - [Examples](#examples)
    - [✓ Preferred — `/confirm`](#preferred-confirm)
    - [✓ Preferred — `GET /catalog/subscription/{subscriptionId}` (stateful REST async)](#preferred-get-catalogsubscriptionsubscriptionid-stateful-rest-async)
    - [✗ Avoid — `/confirm`](#avoid-confirm)
- [Designing Schema](#designing-schema)
  - [Design Principles](#design-principles)
  - [Naming the Schema](#naming-the-schema)
    - [Naming Rules](#naming-rules)
    - [Casing Rules](#casing-rules-1)
  - [Describing a Schema](#describing-a-schema)
  - [Examples](#examples-1)
    - [✓ Preferred — `Contract` schema](#preferred-contract-schema)
    - [✗ Avoid — `Contract` schema](#avoid-contract-schema)
  - [Managing Exceptions and Offending Schemas](#managing-exceptions-and-offending-schemas)
- [Schema Organization](#schema-organization)
  - [Schema Source Directory](#schema-source-directory)
  - [Schema Directory Structure](#schema-directory-structure)
- [JSON-LD Conventions](#json-ld-conventions)
- [RFC Approval Gate](#rfc-approval-gate)
  - [Gate Conditions](#gate-conditions)
  - [Handling a Failed Gate](#handling-a-failed-gate)
  - [Scope Alignment](#scope-alignment)
  - [Why This Gate Exists](#why-this-gate-exists)
- [Schema Authoring and Validation Gates](#schema-authoring-and-validation-gates)
  - [Artifact Precedence](#artifact-precedence)
- [Change Management and Compatibility](#change-management-and-compatibility)
- [Cross-Artifact Checklist](#cross-artifact-checklist)
- [Examples and Normalization Patterns](#examples-and-normalization-patterns)
- [Conformance Requirements](#conformance-requirements)
- [Security and Interoperability Considerations](#security-and-interoperability-considerations)
- [Conclusion](#conclusion)
- [Acknowledgements](#acknowledgements)
- [References](#references)

## Introduction

Beckn Protocol specifications are authored across multiple repositories, and small inconsistencies in naming, schema semantics, endpoint tokenization, and documentation-example alignment can accumulate into interoperability debt. This guide establishes a common authoring baseline so artifacts evolve predictably, remain validation-aligned, and reduce the risk of unsafe parsing or inconsistent policy enforcement.

## Specification

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described [here](./Keyword_Definitions.md). These definitions aim to ensure that the terms are understood precisely and consistently to avoid confusion in the interpretation of standards, specifications, and protocols.

### Definitions

- **Machine contract:** Authoritative artifacts such as `attributes.yaml` and `schema.json` that define enforceable structure.
- **Semantic artifacts:** `context.jsonld` and `vocab.jsonld` files that define linked-data meaning and term mapping.
- **Schema pack:** A versioned bundle of required and optional schema, context, vocab, and documentation assets.
- **Cross-artifact consistency:** The requirement that contracts, semantic files, examples, and prose stay aligned.
- **Backward-compatible evolution:** An additive, mapped, deprecated-first change strategy for renames or replacements.
- **Canonical naming:** Governed, consistent naming for types, properties, enums, and endpoint actions.

> Note: Henceforth, all references to "fabric" will refer to the Universal Value-exchange Fabric operated by the Networks for Humanity Foundation, unless explicitly mentioned otherwise. 

## Scope and Audience

This RFC applies to architects and maintainers of:

- Beckn Protocol APIs
- Fabric APIs
- Fabric-aware schema 
- Domain, regional, and network-specific schema

## Core Principles

Good protocol specifications must be precise enough to eliminate implementation ambiguity, yet accessible enough for developers across different linguistic and technical backgrounds to understand and act on without confusion. The Beckn Protocol is adopted across diverse regions, domains, and languages — design decisions that create unnecessary cognitive load or assume cultural familiarity will slow adoption and increase the risk of misinterpretation.

These principles apply to all design decisions in a Beckn specification: naming a keyword, describing an endpoint, structuring a schema, or organizing an artifact bundle.

### Naming

The challenge in naming any keyword — an endpoint, schema, property, or enumeration value — is to convey maximum meaning using the fewest tokens, with the fewest syllables, while achieving high recall across a global developer audience. The simplicity of HTTP method names such as `GET`, `POST`, `PUT`, `PATCH`, and `DELETE` is an example of this principle applied well.

The following SHOULD be considered by any architect coining the name of a keyword:

1. **Semantic clarity:** The name SHOULD convey its semantics purely by its structure, without requiring the reader to consult its description.
2. **Minimum token count:** The number of words in any keyword SHOULD be minimized. Prefer one word over two, two over three.
3. **Minimum syllables:** When verbally expressed, a keyword SHOULD involve the fewest syllables necessary to remain unambiguous.
4. **Retention and recall:** Keywords SHOULD be easy to remember and reproduce across language barriers.

## Designing API Endpoints

All Beckn Protocol transaction endpoints use **HTTP POST**, regardless of the semantic nature of the action. The action is expressed in the URL path (e.g. `/confirm`) and in the `context.action` field of the request envelope. This is a deliberate design choice that keeps transport mechanics uniform and places all protocol semantics in the application layer.

Every Beckn API call follows an **asynchronous request/callback split**: the implementer returns a synchronous `Ack` or `Nack` immediately upon receiving the request, and delivers the business outcome asynchronously via the corresponding `on_*` callback endpoint on the caller's registered URI. Endpoint descriptions MUST account for both legs of this exchange.

Every request body MUST carry a `context` object — identifying the transaction, participants, and protocol version — and a `message` object carrying the action-specific payload. Endpoint descriptions MUST address the semantics of both.

### Naming Convention
Naming protocol endpoints is a crucial step in long-term protocol stability. The design challenge is to convey maximum meaning using the least amount of tokens/words with the least number of syllables while creating high recall value.

An example for such an endpoint name in Beckn is `track`. It uses only one syllable, conveys its purpose unambiguously, and has high recall.

For an action name, the ideal number of syllables is *one* but the recommended limit is *two*, although exceptions MAY be considered and accepted by the protocol working group, albeit begrudgingly. 

> Exception: The `discover` endpoint is an example of a three syllable action, which is an exception to the least syllables rule. 

#### For Stateless APIs
- The last path parameter of the request endpoint MUST be a **verb** describing the action requested by the caller. The `discover`, `select`, `init` (short for initialize), `confirm`, `update`, `cancel`, `track`, `rate`, `support` are all verbs.
- The last path parameter of the callback endpoint MUST be the verb used in the request endpoint preceded by an `on_`. For example, the callback endpoint for `discover` endpoint MUST be `on_discover`. 
  
> NOTE: The ONLY exception to the verb rule is the `status` endpoint, which has been preserved as a legacy endpoint name due to its meaning being consistent across the globe. An endpoint with the name `/status` typically means *"get the status"*, hence the deviation from the "verb-like" naming. However, all future endpoints MUST ALWAYS be in a verb form. 

#### For Stateful APIs

Stateful Fabric service APIs MUST follow REST conventions uniformly — for both synchronous and asynchronous interactions. Resources MUST be identified by noun-based URL paths, and HTTP methods MUST convey the nature of the operation:

| HTTP Method | Semantic | Example |
|---|---|---|
| `POST` | Create a new resource instance | `POST /catalog/subscription` |
| `GET` | Retrieve a resource or its current state | `GET /catalog/subscription/{subscriptionId}` |
| `PUT` | Replace a resource in full | `PUT /catalog/subscription/{subscriptionId}` |
| `PATCH` | Partially update a resource | `PATCH /catalog/subscription/{subscriptionId}` |
| `DELETE` | Remove a resource | `DELETE /catalog/subscription/{subscriptionId}` |

##### Path Parameters

Resource identifiers MUST be expressed as **path parameters**. Query parameters MUST only be used for optional, non-identifying modifiers such as pagination controls (`limit`, `offset`) or sort order. A resource whose identity is known at call time MUST appear in the URL path, not the query string.

```text
✓  GET /catalog/subscription/{subscriptionId}
✗  GET /catalog/subscription?subscriptionId={subscriptionId}

✓  DELETE /catalog/subscription/{subscriptionId}
✗  DELETE /catalog/subscription?subscriptionId={subscriptionId}
```

Query parameter names, where used for optional modifiers, MUST follow `lowerCamelCase` per CON-005-01.

##### Async Callbacks

Stateful async operations follow the same REST path conventions as their initiating requests. **The `on_*` callback convention applies exclusively to stateless P2P transaction endpoints** (e.g., `/confirm` → `/on_confirm`). It MUST NOT be used for stateful Fabric service API callbacks.

Where a stateful operation initiates an asynchronous outcome, the implementer MUST:

1. Return a synchronous `Ack` immediately upon receiving the request.
2. Deliver the async result by calling the requester's registered callback URI at the **same resource path** as the initiating request, using the HTTP POST method appropriate to the delivery semantics as the implementer is delivering new content to the caller.

```text
Initiating request:   GET  /catalog/subscription/{subscriptionId}   →  Ack
Async callback:       POST /catalog/subscription/{subscriptionId}
                      (called by CS on the BAP's registered callback URI,
                       carrying the assembled catalog as the request body)

Initiating request:   POST /catalog                                  →  Ack
Async callback:       POST /catalog/{catalogId}
                      (called by CS on the BPP's registered callback URI,
                       confirming acceptance and carrying the assigned catalogId)
```

The same resource path in the callback preserves the REST resource identity across both legs of the exchange. The caller correlates the callback to the initiating request via the resource path and any resource identifier present in both.

Legacy endpoint exceptions MUST be explicitly documented and MUST NOT become new precedent.

> **Legacy Exception — Catalog APIs:** The catalog service endpoints (`/catalog/publish`, `/catalog/on_publish`, `/catalog/subscription`, `/catalog/pull`, `/catalog/on_pull`) were designed before this style guide. They use an RPC-style `resource/action` naming pattern, the `on_*` callback convention, and query parameters for resource identification — all of which are inconsistent with the REST conventions required for stateful APIs. These endpoints are recognized as legacy exceptions and MUST NOT be used as a model for new stateful API design. They will be evaluated for migration to REST-conformant design in a future release, subject to ecosystem impact assessment.

#### Casing Rules
- Endpoints MUST use `snake_case` path tokens.

### Writing Descriptions
An endpoint description MUST precisely state what the endpoint does in terms of the fabric-aware value-exchange model. It MUST NOT use informal language or leave any aspect of the endpoint's behavior implicit or assumed.

Each endpoint description MUST include the following:

**1. Action statement.** A single sentence beginning with a verb that states what the caller requests and what the implementer performs. Both actor names MUST be stated explicitly. For example: *"The BAP invokes this endpoint to request the BPP to confirm a previously initialized order contract."*

**2. Preconditions.** Any state or prior API call that must have occurred before this endpoint may be invoked MUST be stated. For example: *"This endpoint MUST only be invoked after a successful `on_confirm` response has been received by the BAP."*

**3. Fabric context.** Where the endpoint interacts with or depends on a Fabric service (such as the Discovery Service, Registry, or catalog infrastructure), the relationship MUST be stated and the relevant Fabric component MUST be named. If a canonical document describes that component, a hyperlink to that document MUST be embedded inline within the description text.

**4. Message envelope.** The description MUST state the required envelope fields and their significance for this endpoint. All properties of the `context` and `message` objects that carry endpoint-specific semantics MUST be individually described.

**5. Response semantics.** Every response family (`Ack`, `AckNoCallback`, `NackBadRequest`, `NackUnauthorized`, `ServerError`) that the implementer may return MUST be described. The description MUST state what each response means in the context of this specific endpoint's behavior — it MUST NOT merely restate the HTTP status code.

**6. Callback relationship.** For stateless P2P request endpoints that have an `on_*` callback counterpart, the description MUST state when and by whom the callback is triggered, what it carries, and how the caller MUST interpret it. For stateful REST endpoints with an async outcome, the description MUST state that the implementer delivers the result by calling the same resource path on the caller's registered callback URI, what the delivery payload carries, and what the caller MUST do upon receipt.

**Tone and grammar.** Descriptions MUST be written in formal technical prose. The passive voice SHOULD be used only when the active actor is genuinely indeterminate. Descriptions MUST NOT contain colloquial phrasing, unexplained abbreviations, or normative requirements expressed in informal language. Every normative statement MUST use the keywords `MUST`, `SHOULD`, or `MAY` as defined in [Keyword Definitions](./Keyword_Definitions.md).

**Conformance to the fabric-first narrative.** Endpoint descriptions MUST reflect the fabric-first positioning of the Beckn Protocol. Endpoints that operate through Fabric services — such as catalog publishing, catalog-driven discovery, and registry lookup — MUST be described in terms of the Fabric infrastructure, not solely in terms of peer-to-peer exchange. The role of the NFH Fabric as the central coordination layer MUST be acknowledged wherever it is relevant to the endpoint's behavior.

### Examples

#### ✓ Preferred — `/confirm`

> The BAP invokes this endpoint to request the BPP to confirm a previously initialized order contract. This endpoint MUST only be invoked after a successful `on_init` response has been received by the BAP, establishing an active initialized transaction identified by `context.transactionId`. The BPP MUST validate the signature on the request as described in [Authentication and Trust](./Authentication_and_Trust.md) before processing. Upon successful validation and processing, the BPP MUST return an `Ack` synchronously and subsequently invoke the `/on_confirm` callback on the BAP's registered callback URI, carrying the confirmed `Contract` object in the `message` field. If signature validation fails, the BPP MUST return a `NackUnauthorized` response and MUST NOT invoke the callback. If the request body is structurally invalid or the `transactionId` does not correspond to an active initialized transaction, the BPP MUST return a `NackBadRequest` response. For the role of a confirmed contract within the NFH Fabric's value-exchange lifecycle, refer to [Value Exchange Lifecycle](./Value_Exchange_Lifecycle.md).

Both actor names are present, the precondition is explicit, every response family is described with business semantics, the callback relationship is fully stated, and two canonical documents are linked inline.

#### ✓ Preferred — `GET /catalog/subscription/{subscriptionId}` (stateful REST async)

> The BAP invokes this endpoint to request the CS to assemble and deliver the catalog snapshot scoped to the specified subscription. The `{subscriptionId}` path parameter MUST reference a `CatalogSubscription` record in `ACTIVE` status owned by the calling BAP, as identified by the signing key in the Authorization header. The CS MUST validate the signature as described in [Authentication and Trust](./Authentication_and_Trust.md) before processing. Upon successful validation, the CS MUST return an `Ack` synchronously and subsequently deliver the assembled catalog by invoking `POST /catalog/subscription/{subscriptionId}` on the BAP's registered callback URI, carrying the catalog payload in the request body. If the `subscriptionId` does NOT exist, the CS MUST return `NackNotFound`. If the subscription exists but is owned by a different BAP, the CS MUST return `NackForbidden`. If the subscription is in `INACTIVE` status, the CS MUST return `NackBadRequest`.

The resource identifier appears in the path, NOT the query string. The callback uses the same resource path on the BAP's registered URI. No `on_*` verb pattern is used.

#### ✗ Avoid — `/confirm`

**Variant A — Incomplete: real pre-guide description**

> "BAP accepts all terms and provides payment proof/reference, then requests the BPP to confirm the contract into a binding commitment."

*This is the actual `/confirm` description in `beckn.yaml` prior to adoption of this guide.* It names the caller (BAP) and implementer (BPP), which is correct. However, it assumes the contract always involves a payment — not all contract types do. It omits the precondition (`on_init` must have been received), all response families, the callback relationship, and any Fabric context. A reader cannot determine from this description what the BPP must do if signature validation fails, or what the `/on_confirm` callback carries.

---

**Variant B — Domain assumption without authority**

> "Sends the order confirmation to the seller. The seller processes it and sends back a confirmation."

Uses domain-specific language ("order", "seller") that assumes a commerce context. The Beckn Protocol is domain-neutral — the same endpoint is used for hiring contracts, mobility reservations, and energy exchanges. No response families described, no callback semantics, no preconditions.

---

**Variant C — Conflates request and callback**

> "Called by the buyer app after the seller acknowledges the terms. Returns a confirmed contract object."

"Returns a confirmed contract object" describes the `/on_confirm` callback, not the `/confirm` request, which returns only a synchronous `Ack`. This description conflates two distinct legs of the exchange, making it impossible to implement either correctly.

---

**Variant D — Query parameter used for resource identifier (stateful API anti-pattern)**

> `DELETE /catalog/subscription?subscriptionId={subscriptionId}`

The subscription is a known, identified resource. Its identifier MUST appear in the path: `DELETE /catalog/subscription/{subscriptionId}`. Using a query parameter for a resource identifier makes the endpoint semantically indistinguishable from a filtered collection operation and prevents REST-idiomatic client behaviour such as caching and addressability.

## Designing Schema

### Design Principles

When designing schema terms and IRIs, the following principles SHOULD be applied in addition to the general Core Principles:

1. **Semantic stability:** Names and IRIs SHOULD preserve stable meaning across versions.
2. **Composable evolution:** New terms SHOULD extend, not duplicate or redefine, existing semantics.
3. **Backward-safe change:** Renames and removals MUST carry migration and ontology mapping.

### Naming the Schema
Naming a schema is a practiced skill for a protocol architect. It requires thorough industry research, strong communication skills, and developer empathy. Like endpoints, the design challenge is to convey maximum semantics with the least amount of tokens or words using the least number of syllables, while creating high recall value. 

Schema authors MUST assume that the schema user (typically a developer) will NOT read and understand the canonical description of the schema in detail. The name of the schema should be extremely intuitive and self-describing. Schema authors are strongly advised to include a language refinement step in their design process. In today's AI-powered world, a simple prompt like this should work. 

> Prompt: "Generate an intuitive name for (describe concept). Widely adopted, industry-defined name for this concept take precedence over coining your own. Multi-word names are allowed"

#### Naming Rules

These rules apply to all schemas defined across the Beckn Protocol ecosystem — including those in `api/v2.0.0/beckn.yaml`, the [beckn/schemas](https://github.com/beckn/schemas) repository, and domain-specific extensions such as those in [beckn/DEG](https://github.com/beckn/DEG).

**Part of speech.** Schemas MUST always be nouns or the noun forms of verbs (especially when describing the state of an action).

**Domain-agnostic naming.** Domain-agnostic schema names should be abstract but meaningful and unambiguous. Any schema user reading the name should get a fairly good idea of its meaning without referring to its canonical description.

**Multi-word schemas.** Multi-word, industry-agnostic names like `FulfillmentAgent` or `PaymentMethod` are allowed. However, it is RECOMMENDED to restrict a multi-word schema to **two** components. Anything more than two is strongly discouraged unless there is no other way to convey the meaning. Extremely long, verbose schema names are also discouraged.

**Industry-specific schema naming.** Authors coining domain or industry-specific schema names MUST use the most widely adopted industry-standard terms instead of coining their own. For example, a business offering EV charging services should use `ChargingPointOperator` instead of `ChargingServiceProvider` — which, although clear, is not the industry-standard term.

**Action schema naming.** When naming a schema that describes an action, it is REQUIRED to append the word `Action` as a suffix. For example, when describing an act of payment, the preferred name is `PaymentAction` instead of just `Payment`, which creates ambiguity about whether the term describes the act of payment or its resulting state.

#### Casing Rules
- Types and classes MUST use `TitleCase`.
- Properties MUST use `lowerCamelCase`.
- Enum values MUST use `SCREAMING_SNAKE_CASE`.
- Reserved or ambiguous property names such as `type` SHOULD be avoided, except for JSON-LD `@type`.

### Describing a Schema

A schema description MUST precisely state what real-world concept, entity, or state the schema represents. It MUST NOT describe the schema in terms of its structural composition (e.g., *"an object containing X and Y"*) but exclusively in terms of its semantic meaning within the value-exchange model.

**Describing the schema itself.** The top-level description of a schema MUST include:

**1. Concept statement.** A single sentence identifying the real-world concept the schema models. The sentence MUST be unambiguous — a reader with no prior context MUST be able to identify the concept from the description alone, without reading the property definitions.

**2. Scope and lifecycle position.** The description MUST state in which part of the value-exchange lifecycle this schema appears, and which actors produce or consume it.

**3. Fabric context.** Where the schema models a resource managed by or exchanged through a Fabric service, that relationship MUST be named, and a hyperlink to the relevant canonical document MUST be embedded inline in the description. The same document IRI MUST also appear as a `seeAlso` triple in the schema's `vocab.jsonld` file.

**4. Relationship to other schemas.** If the schema extends, composes, or constrains another schema, that relationship MUST be stated explicitly.

**Describing properties.** Every property of a schema MUST have a description. Property descriptions MUST:

- State what the property represents, not merely restate its name.
- State whether the value is assigned by the caller, the implementer, or a Fabric service.
- State any constraints on the value that are not already captured by the JSON Schema type declaration (e.g., business-rule constraints, lifecycle invariants, or ordering requirements).
- For properties whose value is drawn from an enumeration, describe what each enumeration value means in the context of this specific schema.
- For properties that reference another schema by type, state the semantics of that reference rather than merely naming the referenced type.

**Tone and grammar.** Schema and property descriptions MUST be written in formal technical prose. They MUST NOT be written as imperative instructions or in the first or second person. Normative constraints on values MUST use `MUST`, `SHOULD`, or `MAY` as defined in [Keyword Definitions](./Keyword_Definitions.md). Descriptions MUST NOT assume domain-specific knowledge on the part of the reader unless that knowledge is defined elsewhere in this specification, in which case a hyperlink to that definition MUST be embedded inline.

**Conformance to the fabric-first narrative.** Schema descriptions MUST reflect the fabric-first positioning of the Beckn Protocol. Schemas that model Fabric-managed resources — such as catalogs, contracts, or registry entries — MUST be described in terms of their role within the NFH Fabric, not merely as data transfer objects.

### Examples

#### ✓ Preferred — `Contract` schema

**Schema-level description:**

> A `Contract` represents a digitally agreed commitment between two or more participants governing the exchange of economic or non-economic value, mediated by the NFH Fabric. It is produced by the BPP and transmitted to the BAP in the `on_confirm` callback. The schema is domain-neutral: the same `Contract` serves commerce, mobility, healthcare, and energy use cases through JSON-LD context mapping — for example, `retail:Order`, `mobility:Reservation`, and `healthcare:Appointment` are all sub-types of `beckn:Contract`. Once confirmed, it serves as the reference object for all subsequent lifecycle operations including `status`, `update`, `cancel`, and `track`. For the lifecycle in which a `Contract` transitions through states, refer to [Value Exchange Lifecycle](./Value_Exchange_Lifecycle.md).

**Property — `id`:**

> A globally unique identifier for this contract instance, assigned by the BPP before the `/on_confirm` callback and carried in all subsequent `status`, `update`, `cancel`, and `track` requests to identify the transaction. This value MUST remain stable for the entire lifetime of the contract and MUST NOT be reassigned or reused across distinct transactions. It is RECOMMENDED to combine `bppId`, `providerId`, and `id` to guarantee global uniqueness.

**Property — `status`:**

> The current lifecycle state of the contract, expressed as a `Descriptor` whose `code` MUST be one of the standard contract state values. The BPP is responsible for setting and updating this value. `ACTIVE` indicates the contract is in force and execution is ongoing. `CANCELLED` indicates the contract was terminated before fulfillment completion and MUST only appear after a successful `on_cancel` exchange. `COMPLETED` indicates all performance and settlement obligations have been met.

The concept statement is domain-neutral and names the real-world commitment — not the data structure. The lifecycle position (produced at `on_confirm`, referenced through `track`) is explicit. The property descriptions name who sets each value, when, and what each state means in business terms.

#### ✗ Avoid — `Contract` schema

The following examples are drawn from real descriptions in `beckn.yaml` and the [beckn/schemas](https://github.com/beckn/schemas) repository, written before this guide was adopted.

**Variant A — Structural opening, not a concept statement**

Schema-level: `"This is a JSON-LD compliant, linked-data schema that specifies a generic multi-party, digitally signed Contract between a set of participants."`

*This is the actual opening sentence of the `Contract` description in `beckn.yaml` prior to this guide.* It leads with how the schema is encoded ("JSON-LD compliant, linked-data") rather than what real-world concept it represents. A reader learns nothing about what a Contract means in a value-exchange context, who the participants are, or where it appears in the transaction lifecycle.

---

**Variant B — Name restatement**

Schema-level: `"Catalog schema for Beckn Protocol v2.0.0"`

*Actual description of the `Catalog` schema in `beckn.yaml`.* Restates the schema name and protocol version. Conveys no semantic meaning — what is a Catalog? Who produces it? When does it appear? Which actors interact with it?

---

**Variant C — Role description with no context**

Schema-level: `"Catalog publish request payload."`

*Actual description of `CatalogPublishAction` in `beckn.yaml`.* Describes the structural role ("request payload") rather than the real-world concept. No lifecycle position, no actors, no relationship to other schemas, no Fabric context.

### Managing Exceptions and Offending Schemas
Sometimes due to timeline constraints, and implementer demand, some schema names tend to violate the above rules. Such schemas are called **offending schemas**. While such practices are not recommended, the protocol does allow for their temporary existence. Schema authors are REQUIRED to eventually deprecate these names and provide clean machine-readable migration paths using `owl` syntax describing the deprecation of the offending schema name to the compliant schema name. This is also an opportunity for external contributors to flag such offending schemas as issues and keep such deviations in check. 

## Schema Organization

The reference schema pack structure used by the Beckn Protocol is maintained in the [beckn/schemas](https://github.com/beckn/schemas) repository. Every schema defined in the scope of the fabric MUST conform to the following organizational pattern.

### Schema Source Directory
All schemas defined in a specific context must be grouped inside a single directory. While the name of the directory is irrelevant, it is RECOMMENDED to have an intuitive name like `schema`, `schemas`, or `models`. A typical schema catalog directory looks like this.

```text
schemas/ 
├── Context/ 
│   ├── v2.0/
│   │   └── ...
│   └── README.md
│
├── Catalog/
│   ├── v2.0/ (LTS)
│   │   └── ...
│   ├── v2.1/
│   │   └── ...
│   └── README.md
│
├── Item/
│   ├── v2.0/
│   │   └── ...
│   ├── v2.1/
│   │   └── ...
│   └── README.md
│
├── Contract/
│   ├── v2.0/
│   │   └── ...
│   └── README.md
│
├── ... (220+ schemas in beckn/schemas)
│
├── context.jsonld (Master context for all schemas)
├── vocab.jsonld (Master vocabulary for all schemas)
└── README.md
```

### Schema Directory Structure
Every schema MUST reside in a schema directory whose name is the same as the schema with matching case. For example, a schema called `Catalog` MUST be defined in a directory called `Catalog`.

```text
├── Catalog/
│   ├── v2.0/
│   │   ├── attributes.yaml
│   │   ├── attributes.jsonschema.yaml
│   │   ├── context.jsonld
│   │   ├── vocab.jsonld
│   │   └── README.md
│   ├── v2.1/
│   │   ├── attributes.yaml
│   │   ├── attributes.jsonschema.yaml
│   │   ├── context.jsonld
│   │   ├── vocab.jsonld
│   │   └── README.md
│   └── README.md (Canonical, version-agnostic description)
├── .../
```

Expected schema pack structure:

- Required: `attributes.yaml`, `attributes.jsonschema.yaml`, `context.jsonld`, `vocab.jsonld`, `README.md`
- Optional: `renderer.json`, `profile.json`, `examples/**`

## JSON-LD Conventions

Every schema published within the Beckn Protocol ecosystem MUST include a `context.jsonld` file that maps all schema terms to IRIs in the `beckn:` namespace. This linked-data layer enables schema-neutral semantic interoperability: a `Contract` used in a retail transaction and one used in a healthcare appointment share the same base IRI (`beckn:Contract`) while carrying domain-specific properties through extension context files.

**Authoring rules:**

- Composition and extension objects MUST include `@context` and `@type`.
- Every schema term MUST map to an IRI in the `beckn:` namespace or a recognized external vocabulary (e.g., `xsd:`, `schema:`).
- `context.jsonld` and `vocab.jsonld` MUST remain aligned with the corresponding `attributes.yaml` and `attributes.jsonschema.yaml` contracts.
- Renamed terms SHOULD carry explicit ontology relations (e.g., `owl:sameAs`, `owl:deprecated`) and migration mapping in `vocab.jsonld`.

**Example — `Context` schema (`/schema/Context/v2.0/context.jsonld`):**

```json
{
  "@context": {
    "@version": 1.1,
    "@protected": true,
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "beckn": "https://schema.beckn.io/LinkedData/v2.1/context.jsonld",
    "Context": "beckn:Context",
    "action": "beckn:action",
    "bapId": "beckn:bapId",
    "bapUri": "beckn:bapUri",
    "bppId": "beckn:bppId",
    "bppUri": "beckn:bppUri",
    "messageId": "beckn:messageId",
    "transactionId": "beckn:transactionId",
    "version": "beckn:version",
    "domain": "beckn:domain",
    "timestamp": "beckn:timestamp",
    "ttl": "beckn:ttl"
  }
}
```

Each term in `@context` maps a human-readable property name to its canonical IRI under the `beckn:` namespace. The `@version: 1.1` declaration enables JSON-LD 1.1 features including `@protected`, which prevents downstream context files from overriding these mappings and guarantees stable semantic grounding across all implementations.

## RFC Approval Gate

An approved RFC is a **mandatory prerequisite** for any Pull Request that introduces or modifies schema, API endpoints, JSON-LD artifacts, or behavioral specification in any Beckn Protocol repository. This gate is enforced before any technical review of the Pull Request begins.

### Gate Conditions

A Pull Request MUST NOT be reviewed until all three gate conditions are satisfied:

| # | Condition | Enforcement |
|---|---|---|
| G-1 | The PR links to a specific RFC by ID | PR description MUST contain a direct link to the RFC document |
| G-2 | The linked RFC has reached **Proposed Standard** status or higher | RFC status MUST be declared in the RFC's Document Details block |
| G-3 | The PR diff scope aligns precisely with what the approved RFC specifies | Verified by the reviewer as Step 0 before any other review activity |

A Pull Request that fails any gate condition MUST be returned to the author immediately. No further review steps apply.

### Handling a Failed Gate

| Failure | Required action |
|---|---|
| No RFC linked | Author MUST draft and obtain RFC approval before resubmitting |
| RFC is `Draft` status | PR MUST be converted to Draft status; resubmit after RFC reaches Proposed Standard |
| PR scope exceeds the RFC | Author MUST either remove the excess changes from the PR, or update the RFC to cover them and obtain re-approval before resubmitting |
| PR scope is narrower than the RFC | Acceptable — a PR may implement a subset of an approved RFC |

### Scope Alignment

Once the gate conditions are satisfied, the reviewer MUST verify that the diff aligns with the RFC before conducting any technical review. Specifically:

- Every endpoint, schema, property, enum value, or behavioral rule introduced in the diff MUST be explicitly described in the approved RFC.
- No endpoint, schema, property, enum value, or behavioral rule may appear in the diff that is NOT described in the RFC.
- If the diff contains changes that are NOT covered by the approved RFC, the Pull Request MUST be rejected without further review. The reviewer MUST cite the specific diff elements that lack RFC coverage.

Reviewers are NOT responsible for evaluating the merit of changes that were NOT covered by an approved RFC. Scope introduced at the PR stage bypasses the working group's design authority. Such changes MUST be rejected without prejudice to the underlying idea — the idea belongs in a new or updated RFC.

### Why This Gate Exists

The RFC process exists to separate design decisions from implementation. A reviewer who encounters unexpected schema elements at diff-review time is being asked to perform a design review inside an implementation review — two distinct activities with different audiences, different criteria, and different working-group members. This gate keeps those activities separate and preserves the integrity of both.

An RFC that passes working-group review but whose implementation diverges from the approved design defeats the purpose of the RFC process entirely.

## Schema Authoring and Validation Gates

Each schema bundle MUST pass:

- OpenAPI validation for `attributes.yaml`
- JSON Schema validation for `attributes.jsonschema.yaml`
- JSON-LD validation for `context.jsonld` and `vocab.jsonld`

Core schemas SHOULD default to `additionalProperties: false`; extension containers SHOULD remain open and carry explicit semantic metadata.

### Artifact Precedence

When artifacts conflict, the following precedence MUST be applied:

1. `attributes.yaml`
2. `schema.json`
3. `context.jsonld`
4. `vocab.jsonld`
5. `examples`
6. `docs`
7. `README.md`

## Change Management and Compatibility

Breaking changes include:

- renaming properties, types, or enums
- adding required fields
- changing term meaning without introducing new terms

The preferred migration path is:

1. Add the new term while retaining the old term.
2. Mark the old term as deprecated.
3. Publish migration notes and semantic mapping.
4. Remove the old term only in a planned major release.

## Cross-Artifact Checklist

Before merge, authors SHOULD verify:

- canonical naming and casing consistency
- action and callback pairing: stateless P2P endpoints use `on_*` callback pattern; stateful REST endpoints use the same resource path on the caller's registered URI
- resource identifiers expressed as path parameters, NOT query parameters
- alignment across `attributes.yaml`, `schema.json`, `context.jsonld`, and `vocab.jsonld`
- examples validate against canonical contracts
- migration notes exist for renames and deprecations
- attribution and upstream traceability exist for derived specifications

## Examples and Normalization Patterns

Example naming normalization:

```text
transaction_id -> transactionId
expires_at -> expiresAt
http/get -> HTTP_GET
filters.type -> filters.expressionType
```

Example action and callback pairing — stateless P2P:

```text
/select              ->  /on_select
/catalog/publish     ->  /catalog/on_publish   (legacy exception — do not model)
```

Example resource and callback pairing — stateful REST async:

```text
GET  /catalog/subscription/{subscriptionId}   →  Ack
POST /catalog/subscription/{subscriptionId}       (CS calls BAP's registered URI — delivers catalog)

POST /catalog                                 →  Ack
POST /catalog/{catalogId}                         (CS calls BPP's registered URI — confirms acceptance)
```

Example path parameter vs query parameter:

```text
✓  GET    /catalog/subscription/{subscriptionId}   — resource identifier in path
✓  GET    /catalog/subscription?limit=20&offset=0  — pagination modifiers in query
✗  GET    /catalog/subscription?subscriptionId=xyz — identifier in query (MUST NOT)
✗  DELETE /catalog/subscription?subscriptionId=xyz — identifier in query (MUST NOT)
```

## Conformance Requirements

| ID | Requirement | Level |
|---|---|---|
| CON-005-01 | New schema properties MUST use `lowerCamelCase` and MUST NOT introduce `snake_case`. | MUST |
| CON-005-02 | Enum values MUST use `SCREAMING_SNAKE_CASE` for canonical representation. | MUST |
| CON-005-03 | Authors MUST keep `attributes.yaml`, `attributes.jsonschema.yaml`, `context.jsonld`, and `vocab.jsonld` semantically aligned. | MUST |
| CON-005-04 | Breaking renames and removals MUST include deprecation and migration guidance. | MUST |
| CON-005-05 | Examples and documentation SHOULD validate against canonical machine contracts. | SHOULD |
| CON-005-06 | Endpoint descriptions MUST explicitly name both the caller and the implementer actor. | MUST |
| CON-005-07 | Endpoint descriptions MUST describe every applicable response family using business semantics, not HTTP status codes. | MUST |
| CON-005-08 | Schema descriptions MUST be written as concept statements and MUST NOT describe structural composition. | MUST |
| CON-005-09 | Every property of a schema MUST have a description stating what it represents and who assigns its value. | MUST |
| CON-005-10 | All endpoint and schema descriptions MUST be written in formal technical prose using normative keywords as defined in [Keyword Definitions](./Keyword_Definitions.md). | MUST |
| CON-005-11 | Schema names that describe an action MUST append the suffix `Action` (e.g. `PaymentAction`, not `Payment`). | MUST |
| CON-005-12 | Stateful Fabric service APIs MUST use noun-based URL paths with standard HTTP verbs (GET, POST, PUT, PATCH, DELETE) following REST conventions, for both synchronous and asynchronous interactions. | MUST |
| CON-005-13 | Each schema's directory name MUST exactly match the schema name, including case (e.g. the `Catalog` schema MUST reside in a directory named `Catalog`). | MUST |
| CON-005-14 | Each versioned schema pack MUST include `attributes.yaml`, `attributes.jsonschema.yaml`, `context.jsonld`, `vocab.jsonld`, and `README.md`. | MUST |
| CON-005-15 | Every schema term MUST map to an IRI in the `beckn:` namespace or a recognized external vocabulary declared in the schema's `context.jsonld`. | MUST |
| CON-005-16 | Resource identifiers in stateful API endpoints MUST be expressed as path parameters. Query parameters MUST only be used for optional, non-identifying modifiers such as pagination or sort order. | MUST |
| CON-005-17 | Stateful async callbacks MUST use the same resource path as the initiating request on the caller's registered callback URI. The `on_*` callback pattern MUST NOT be used for stateful Fabric service API callbacks. | MUST |
| CON-005-18 | A Pull Request introducing schema, API, or artifact changes MUST link to an RFC at Proposed Standard status or higher before it may be reviewed. Pull Requests without an approved RFC MUST be rejected without review. | MUST |
| CON-005-19 | The scope of changes in a Pull Request MUST correspond precisely to the approved RFC. Changes NOT covered by the RFC MUST be removed from the PR or the RFC MUST be updated and re-approved before review proceeds. | MUST |

> Contributors SHOULD read [CONTRIBUTING.md](https://github.com/beckn/protocol-specifications-v2/blob/main/CONTRIBUTING.md), [CODE_OF_CONDUCT.md](https://github.com/beckn/protocol-specifications-v2/blob/main/CODE_OF_CONDUCT.md), and [GOVERNANCE.md](https://github.com/beckn/protocol-specifications/blob/master/GOVERNANCE.md) before making any contributions to this repository. Repeated violations of the conformance requirements in this document or of the broader governance model may result in the suspension of a contributor's Pull Request submission privileges, followed by their ability to submit Issues and participate in Discussions, and ultimately in their removal from the organization. A contributor who has been removed and wishes to be reinstated MUST submit a formal written request to the Working Group Administrator identifying the root cause of the violation and the remediation taken. The Core Working Group reserves the right to accept or deny such a request.

## Security and Interoperability Considerations

Ambiguous naming, schema and documentation drift, and untracked semantic changes can cause unsafe parsing and inconsistent policy enforcement. Strict cross-artifact validation, deterministic action naming, and explicit semantic mapping reduce these risks.

## Conclusion

This RFC consolidates the style guide into a single ordered structure while preserving the original normative guidance for naming, artifact precedence, validation, compatibility, and semantic alignment. Draft-01 records this RFC-form restructuring. Draft-02 refines the stateful API design rules: resource identifiers are now mandated as path parameters (CON-005-16); the async callback convention for stateful APIs is aligned with REST — the `on_*` verb pattern is now explicitly restricted to stateless P2P transaction endpoints only (CON-005-17); the RFC Approval Gate is introduced as a mandatory prerequisite for all Pull Request reviews, with scope alignment enforced before any technical review begins (CON-005-18, CON-005-19). Future governance work may standardize JSON-LD extension patterns and automated pull-request gates for minimum cross-artifact checks.

## Acknowledgements

This document reflects input from Beckn Protocol contributors maintaining protocol contracts, schema packs, semantic artifacts, and governance processes.

## References
- **Keyword definitions:** [Keyword Definitions](./Keyword_Definitions.md)
- **Schema.org style guide:** Click [here](https://schema.org/docs/styleguide.html)
- **Related pull request 67:** Click [here](https://github.com/beckn/protocol-specifications-v2/pull/67)
- **Related pull request 68:** Click [here](https://github.com/beckn/protocol-specifications-v2/pull/68)
