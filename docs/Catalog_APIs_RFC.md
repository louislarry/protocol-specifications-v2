# RFC-08: Catalog APIs

## 1. Document Details

- **Status:** Draft.
- **Authors:** Beckn Protocol contributors.
- **Created:** 2026-04-22.
- **Updated:** 2026-05-18.
- **Version history:** To be published.
- **Latest editor's draft:** Click [here](https://github.com/beckn/protocol-specifications-v2/blob/draft/docs/Catalog_APIs_RFC.md).
- **Implementation report:** To be published by implementation working group.
- **Stress test report:** To be published by testing and certification working group.
- **Conformance impact:** Major (introduces catalog lifecycle management APIs for Beckn v2 networks).
- **Security/privacy implications:** Catalog data is published and distributed across Network Participants. Authentication via Beckn HTTP Signature is required on all endpoints. Subscription callbacks must be secured to prevent unauthorized catalog injection.
- **Replaces / Relates to:** Supersedes 15_Catalog_Publishing_Service.md and 16_Catalog_Discovery_Service.md.
- **Feedback:** Issues: Click [here](https://github.com/beckn/protocol-specifications-v2/issues?q=is%3Aissue+label%3A%22RFC-08%22); Discussions: Click [here](https://github.com/beckn/protocol-specifications-v2/discussions?discussions_q=label%3A%22RFC-08%22); Pull Requests: Click [here](https://github.com/beckn/protocol-specifications-v2/pulls?q=is%3Apr+label%3A%22RFC-08%22).
- **Errata:** To be published.

## 2. Abstract

This RFC defines the normative specification for all Catalog APIs in Beckn Protocol v2. It covers the full catalog lifecycle: publishing catalogs to the network, pushing catalogs to Discovery Services, subscribing to catalog update streams, pulling catalogs on demand, and searching catalog resources. All APIs follow the standard Beckn asynchronous request-callback pattern and use Network Participant terminology throughout.

## 3. Table of Contents

- [Introduction](#4-introduction)
- [4.1 Terminology](#41-terminology)
- [4.2 Design Principles](#42-design-principles)
- [Specification](#5-specification)
- [5.1 Normative Requirements](#51-normative-requirements)
- [5.2 Conformance Requirements](#52-conformance-requirements)
- [5.3 Security and Privacy Considerations](#53-security-and-privacy-considerations)
- [5.4 Migration Notes](#54-migration-notes)
- [5.5 Examples](#55-examples)
- [Conclusion](#6-conclusion)
- [6.1 Changelog](#61-changelog)
- [Acknowledgements](#7-acknowledgements)
- [References](#8-references)

## 4. Introduction

In Beckn v2 networks, catalog data must flow efficiently from providers to Discovery Services. Network Participants need standardized APIs to publish, distribute, subscribe to, and query catalog data across networks. Without a unified, normative specification for catalog lifecycle management, Network Participants cannot interoperably exchange catalog data, Discovery Services have no standard interface for receiving catalog updates, and catalog resources cannot be consistently queried across networks. This RFC formalizes those APIs to ensure consistent interoperability across all network implementations, enabling decoupled catalog synchronization, efficient incremental updates, and reusable master resource definitions.

### 4.1 Terminology

- **Normative:** Requirements that define conformance and interoperability behavior.
- **Informative:** Explanatory guidance that does not by itself define conformance.
- **Network Participant:** Any entity registered on a Beckn network that implements one or more Beckn protocol APIs.
- **Catalog system (CS):** The server-side Fabric service responsible for ingesting, storing, and distributing catalog data across the network.
- **Discovery Service (DS):** A discovery service owned and operated by a Network Participant that maintains a local catalog index by receiving updates via `/catalog/push`.
- **Subscription:** A persistent registration by a Network Participant to receive catalog updates for specified networks and/or schema types.
- **Conformance impact:** Classification of expected compatibility effect (Patch, Minor, Major, Informative).
- **Migration notes:** Operational guidance required to adopt the change safely.
- **Errata:** Post-publication corrections and clarifications.

### 4.2 Design Principles

_Refer to [GOVERNANCE.md](../GOVERNANCE.md) for the current governance source._

- **Interoperability-first:** All catalog APIs use the standard Beckn context and message envelope, ensuring any conformant Network Participant can exchange catalog data.
- **Abstraction over specificity:** APIs are domain-neutral and support any schema type, not tied to any specific vertical or catalog structure.
- **Optimal ignorance:** Each API exposes only the information necessary for its function. Publishing does not require knowledge of downstream subscribers.
- **Security by design:** All endpoints require Beckn HTTP Signature authentication. The subscriber identity is derived from the signing key in the Authorization header. Only the Network Participant that created a subscription can deactivate it.
- **Reusability before novelty:** Master resource definitions enable resource reuse across catalogs, avoiding duplication of canonical data.

## 5. Specification

_Use MUST / SHOULD / MAY as defined in [Keyword Definitions](https://github.com/beckn/protocol-specifications-v2/blob/main/docs/2_Keyword_Definitions.md)._

### 5.1 Normative Requirements

#### 5.1.1 Catalog Publish

**`POST /catalog/publish`**

A Network Participant publishes catalogs to the network. The CS returns an immediate `ACK` and processes catalogs asynchronously, delivering per-catalog results via `/catalog/on_publish`.

- The Network Participant MUST include a valid Beckn HTTP Signature on every publish request.
- The CS MUST return an `ACK` immediately on receipt.
- The CS MUST validate catalog payloads against the declared schema type.
- The CS MUST deliver per-catalog processing results to `/catalog/on_publish` asynchronously.

**Publish directives and catalog type:**

Publish directives define per-catalog processing instructions, matched by `catalogId`. The `catalogType` field MUST be one of `MASTER` or `REGULAR`. When publish directives are not provided, the CS infers the type from content — catalogs with offers are treated as `REGULAR`; catalogs with only resources are treated as `MASTER`. Default update mode is `MERGE`.

**Network visibility (`visibleTo`):**

Each publish directive may include a `visibleTo` array to restrict the catalog's delivery to specific network participant identifiers. Values MUST be registry-registered network participant identifiers. The CS enforces this restriction at delivery time. The resolution order is:

1. `publishDirectives[].visibleTo` — catalog is delivered only to the listed network participants.
2. `context.networkId` — fallback when `visibleTo` is omitted.
3. The CS's configured default network — fallback when neither is provided.

**`POST /catalog/on_publish`**

Callback endpoint implemented by the Network Participant. The CS delivers the publish status of each catalog once processing is complete.

- The Network Participant MUST implement `POST /catalog/on_publish` to receive processing results.
- The Network Participant MUST respond with `ACK` on receipt of the callback.

#### 5.1.2 Catalog Push

**`POST /catalog/push`**

Endpoint implemented by the Discovery Service run by a Network Participant. The CS pushes catalog updates matching the Network Participant's subscribed `networkIds` and schema types.

- The Discovery Service MUST implement `POST /catalog/push`.
- The CS MUST authenticate via Beckn HTTP Signature on every push request.
- The Discovery Service MUST return an `ACK` immediately on receipt.
- The Discovery Service MUST apply received catalogs to its local index.

#### 5.1.3 Catalog Subscription

**`POST /catalog/subscription`** (create)

A Network Participant creates a subscription to receive catalog updates for specified networks and/or schema types. The identity of the subscriber is derived by the CS from the signing key in the Beckn HTTP Signature Authorization header.

- At least one of `networkIds` or `schemaTypes` MUST be provided.
- The CS MUST reject the request with 409 when an identical `networkIds` + `schemaTypes` combination is already active for the caller.
- The CS MUST generate and return a unique `subscriptionId` UUID for each new subscription.

**`POST /catalog/subscription?subscriptionId={subscriptionId}`** (update)

A Network Participant updates an existing subscription by passing the `subscriptionId` as a query parameter.

- The caller MUST be the original creator of the subscription.
- The CS MUST return 403 when the `subscriptionId` belongs to a different subscriber.
- The CS MUST return 404 when the `subscriptionId` does not exist.

**`DELETE /catalog/subscription?subscriptionId={subscriptionId}`**

Deactivates an active subscription. Only the Network Participant that created the subscription can deactivate it.

- The `subscriptionId` MUST be provided as a query parameter.
- The CS MUST verify that the requesting Network Participant is the creator of the subscription before deactivating it.
- Subscription status after deactivation MUST be `INACTIVE`.

**`GET /catalog/subscriptions`**

Returns all subscriptions for the calling Network Participant. Use the `?subscriptionId=<uuid>` query parameter to retrieve a specific subscription.

- The CS MUST scope results to the calling Network Participant's identity, derived from the Authorization header.
- The caller MAY filter by subscription ID using the `?subscriptionId=<uuid>` query parameter.

#### 5.1.4 Catalog Pull

**`POST /catalog/pull`**

A Network Participant requests catalogs scoped by an active subscription. The caller passes a `subscriptionId` — the CS uses the subscription's network and schema-type filters to determine which catalogs to return. Returns an immediate `ACK`; results are delivered asynchronously via `/catalog/on_pull`. The BAP MUST use `context.messageId` to correlate the `/catalog/on_pull` callback with the originating request.

Two modes are supported:

- **FULL** — returns the latest version of each matching catalog.
- **INCREMENTAL** — returns all catalog versions published between `fromDate` and `toDate`, useful for syncing changes since the last pull. When `fromDate` is omitted, defaults to 7 days before the current time. The date range MUST NOT exceed 7 days per request.

Requirements:

- A valid `subscriptionId` referencing an active subscription MUST be provided.
- The CS MUST return 403 when the `subscriptionId` belongs to a different subscriber.
- The CS MUST return 404 when the `subscriptionId` does not exist.
- The `context.transactionId` MUST be provided and MUST persist through to the `/catalog/on_pull` callback.
- The CS MUST return an `ACK` immediately on receipt.
- The CS MUST deliver results to `/catalog/on_pull` asynchronously.

**`POST /catalog/on_pull`**

Callback endpoint implemented by the Network Participant to receive the results of a `/catalog/pull` request. The BAP MUST use `context.messageId` to correlate this callback with the originating `/catalog/pull` request.

- The Network Participant MUST implement `POST /catalog/on_pull` to receive pull results.
- The callback MUST carry terminal status only: `COMPLETED` or `FAILED`.
- The callback is delivered with at-least-once semantics; the receiving Network Participant MUST deduplicate on `context.transactionId`.
- On `COMPLETED` status, exactly one of `catalogs` (inline) or `downloadManifest` (pre-signed download descriptor) MUST be present.
- When `downloadManifest` is present, the Network Participant MUST verify the `checksum` against the downloaded content before processing. If verification fails, the Network Participant MUST discard the content and treat the pull as failed.
- On `FAILED` status, the `error` field MUST carry the failure reason.
- The Network Participant MUST respond with `ACK` on receipt of the callback.

#### 5.1.5 Catalog Search

**`POST /catalog/search`**

A Network Participant searches for catalogs indexed by the CS, filtered by catalog type, network identifiers, and schema type URIs.

- All filters are optional. When `filters.type` is omitted, the CS MUST default to `MASTER`.
- Omitting `filters.networkIds` or providing an empty array MUST match all networks.
- Omitting `filters.schemaTypes` or providing an empty array MUST match all schema types.
- Search results MUST be paginated.

**`GET /catalog/master/schemaTypes`**

A Network Participant retrieves the schema types available across all master resources in all networks.

**`GET /catalog/master/{masterResourceId}`**

A Network Participant retrieves a master resource by its identifier.

Requirements:

- The CS MUST support filtering by `filters.type`, `filters.networkIds`, and/or `filters.schemaTypes`.
- Omitting a filter dimension MUST match all values for that dimension, subject to the `filters.type` default above.
- Catalog search results MUST be paginated.
- The CS MUST return the full catalog envelope (including provider and descriptor metadata) for individual master resource lookups.

---

### 5.2 Conformance Requirements

| ID | Requirement | Level |
|---|---|---|
| CON-08-01 | Network Participants MUST authenticate all catalog API requests via Beckn HTTP Signature | MUST |
| CON-08-02 | The CS MUST return an `ACK` immediately on receipt of `/catalog/publish` | MUST |
| CON-08-03 | The CS MUST deliver per-catalog results to `/catalog/on_publish` asynchronously | MUST |
| CON-08-04 | Discovery Services MUST implement `POST /catalog/push` | MUST |
| CON-08-05 | At least one of `networkIds` or `schemaTypes` MUST be provided when creating a subscription | MUST |
| CON-08-06 | Subscription status MUST be either `ACTIVE` or `INACTIVE` | MUST |
| CON-08-07 | Only the Network Participant that created a subscription MUST be permitted to deactivate it | MUST |
| CON-08-08 | The CS MUST return an `ACK` immediately on receipt of `/catalog/pull` | MUST |
| CON-08-09 | A valid `subscriptionId` referencing an active subscription MUST be provided in `/catalog/pull` | MUST |
| CON-08-10 | The `context.transactionId` MUST be provided in `/catalog/pull` and MUST persist through to the `/catalog/on_pull` callback | MUST |
| CON-08-11 | Pull callbacks MUST carry terminal status only: `COMPLETED` or `FAILED` | MUST |
| CON-08-12 | The receiving Network Participant MUST deduplicate `/catalog/on_pull` callbacks on `context.transactionId` | MUST |
| CON-08-13 | On `COMPLETED` pull status, exactly one of `catalogs` or `downloadManifest` MUST be present | MUST |
| CON-08-14 | The `fromDate` to `toDate` range in INCREMENTAL pull requests MUST NOT exceed 7 days | MUST |
| CON-08-15 | Catalog search results MUST be paginated | MUST |
| CON-08-16 | Omitting a filter dimension in catalog search MUST match all values for that dimension, subject to the `filters.type` default of `MASTER` | MUST |
| CON-08-17 | The `catalogType` field in publish directives MUST be one of `MASTER` or `REGULAR` | MUST |
| CON-08-18 | When `downloadManifest` is present in a pull callback, the Network Participant MUST verify the checksum before processing the downloaded content | MUST |

---

### 5.3 Security and Privacy Considerations

- All catalog API endpoints MUST enforce Beckn HTTP Signature authentication. Unauthenticated requests MUST be rejected with HTTP 401.
- The identity of a subscriber is derived by the CS from the signing key in the Beckn HTTP Signature Authorization header. Network Participants do not supply subscriber identity in the request body.
- Only the Network Participant that created a subscription MAY deactivate it, enforced via the Authorization header identity.
- Catalog data at rest and in transit SHOULD be protected per the Network Policy Profile.
- Rate limiting SHOULD be applied per Network Participant on all catalog endpoints to prevent abuse.
- Pre-signed download URLs returned in `downloadManifest` within `/catalog/on_pull` responses are short-lived and MUST NOT be used beyond their `expiresAt` timestamp. The Network Participant MUST verify the `checksum` field after downloading and before processing.

---

### 5.4 Migration Notes

These catalog lifecycle APIs are new in Beckn v2 and have no direct equivalent in v1.x. Network Participants implementing v2.0 MUST implement the relevant catalog endpoints based on their role in the network. No backward-compatible migration path from v1.x is required.

The `filters.type` field in `POST /catalog/search` defaults to `MASTER`, preserving backward-compatible behavior for existing implementations that do not supply the field.

---

### 5.5 Examples

#### Example 1 — Publish a catalog

```json
{
  "context": {
    "version": "2.0.0",
    "action": "catalog/publish",
    "messageId": "550e8400-e29b-41d4-a716-446655440000",
    "transactionId": "550e8400-e29b-41d4-a716-446655440001",
    "timestamp": "2026-04-22T10:00:00.000Z",
    "bppId": "np.example.com",
    "bppUri": "https://np.example.com",
    "networkId": "retail-network"
  },
  "message": {
    "catalogs": [
      {
        "id": "CAT-001",
        "descriptor": { "name": "Example Catalog" },
        "provider": {
          "id": "provider-001",
          "descriptor": { "name": "Example Provider" }
        },
        "resources": [
          {
            "id": "ITEM-001",
            "descriptor": { "name": "Example Item" },
            "resourceAttributes": {
              "@context": "https://schema.beckn.org/retail/schema/1.1.0/context.jsonld",
              "@type": "RetailItem"
            }
          }
        ]
      }
    ]
  }
}
```

#### Example 2 — Publish with publishDirectives and visibleTo

```json
{
  "context": {
    "version": "2.0.0",
    "action": "catalog/publish",
    "messageId": "550e8400-e29b-41d4-a716-446655440010",
    "transactionId": "550e8400-e29b-41d4-a716-446655440011",
    "timestamp": "2026-04-22T10:00:00.000Z",
    "bppId": "np.example.com",
    "bppUri": "https://np.example.com",
    "networkId": "retail-network"
  },
  "message": {
    "publishDirectives": [
      {
        "catalogId": "CAT-001",
        "visibleTo": ["retail-network", "mobility-network"],
        "catalogType": "REGULAR",
        "updateMode": "MERGE"
      }
    ],
    "catalogs": [
      {
        "id": "CAT-001",
        "descriptor": { "name": "Example Catalog" },
        "provider": {
          "id": "provider-001",
          "descriptor": { "name": "Example Provider" }
        },
        "resources": [
          {
            "id": "ITEM-001",
            "descriptor": { "name": "Example Item" },
            "resourceAttributes": {
              "@context": "https://schema.beckn.org/retail/schema/1.1.0/context.jsonld",
              "@type": "RetailItem"
            }
          }
        ]
      }
    ]
  }
}
```

#### Example 3 — Subscribe to catalog updates

```json
{
  "context": {
    "version": "2.0.0",
    "action": "catalog/subscription",
    "messageId": "770e8400-e29b-41d4-a716-446655440020",
    "transactionId": "770e8400-e29b-41d4-a716-446655440021",
    "timestamp": "2026-04-22T10:05:00.000Z",
    "bapId": "np.example.com",
    "bapUri": "https://np.example.com"
  },
  "message": {
    "subscription": {
      "networkIds": ["retail"],
      "schemaTypes": [
        "https://schema.beckn.org/retail/schema/1.1.0/item.json#ItemType"
      ]
    }
  }
}
```

#### Example 4 — Pull catalogs (INCREMENTAL mode)

```json
{
  "context": {
    "version": "2.0.0",
    "action": "catalog/pull",
    "messageId": "660e8400-e29b-41d4-a716-446655440002",
    "transactionId": "660e8400-e29b-41d4-a716-446655440003",
    "timestamp": "2026-04-22T10:00:00.000Z",
    "bapId": "np.example.com",
    "bapUri": "https://np.example.com"
  },
  "message": {
    "subscriptionId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "mode": "INCREMENTAL",
    "fromDate": "2026-04-01T00:00:00.000Z",
    "toDate": "2026-04-06T00:00:00.000Z"
  }
}
```

#### Example 5 — on_pull callback (success, inline)

The BAP correlates this callback to the originating `/catalog/pull` request using `context.messageId`.

```json
{
  "context": {
    "version": "2.0.0",
    "action": "catalog/on_pull",
    "messageId": "660e8400-e29b-41d4-a716-446655440002",
    "transactionId": "660e8400-e29b-41d4-a716-446655440003",
    "timestamp": "2026-04-22T10:00:05.000Z"
  },
  "message": {
    "status": "COMPLETED",
    "catalogs": [
      {
        "id": "CAT-001",
        "descriptor": { "name": "Example Catalog" }
      }
    ]
  }
}
```

#### Example 6 — on_pull callback (success, downloadManifest)

Used when the result payload is too large to return inline.

```json
{
  "context": {
    "version": "2.0.0",
    "action": "catalog/on_pull",
    "messageId": "660e8400-e29b-41d4-a716-446655440002",
    "transactionId": "660e8400-e29b-41d4-a716-446655440003",
    "timestamp": "2026-04-22T10:00:05.000Z"
  },
  "message": {
    "status": "COMPLETED",
    "downloadManifest": {
      "url": "https://storage.example.com/catalog-result.json.gz?token=xyz",
      "expiresAt": "2026-04-22T11:00:05.000Z",
      "format": "json.gz",
      "sizeBytes": 5242880,
      "checksum": "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    }
  }
}
```

#### Example 7 — Deactivate a subscription

```
DELETE /catalog/subscription?subscriptionId=f47ac10b-58cc-4372-a567-0e02b2c3d479
Authorization: Signature ...
```

#### Example 8 — Search catalogs (default MASTER type)

```json
{
  "context": {
    "version": "2.0.0",
    "action": "catalog/search",
    "messageId": "770e8400-e29b-41d4-a716-446655440004",
    "transactionId": "770e8400-e29b-41d4-a716-446655440005",
    "timestamp": "2026-04-22T10:00:00.000Z"
  },
  "message": {
    "filters": {
      "networkIds": ["retail"],
      "schemaTypes": [
        "https://schema.beckn.org/retail/schema/1.1.0/item.json#ItemType"
      ]
    },
    "limit": 20,
    "offset": 0
  }
}
```

#### Example 9 — Search REGULAR catalogs explicitly

```json
{
  "context": {
    "version": "2.0.0",
    "action": "catalog/search",
    "messageId": "770e8400-e29b-41d4-a716-446655440006",
    "transactionId": "770e8400-e29b-41d4-a716-446655440007",
    "timestamp": "2026-04-22T10:00:00.000Z"
  },
  "message": {
    "filters": {
      "type": "REGULAR",
      "networkIds": ["retail"]
    },
    "limit": 20,
    "offset": 0
  }
}
```

## 6. Conclusion

This RFC defines the full catalog lifecycle API surface for Beckn Protocol v2, covering catalog publishing, Discovery Service sync, subscription management, on-demand pull, and catalog resource search. Conformant implementations of these APIs will enable consistent, interoperable catalog data exchange across all Beckn v2 networks. The RFC advances to Candidate status when at least one reference implementation has been validated against the conformance requirements in Section 5.2.

### 6.1 Changelog

| Version | Date | Author | Summary |
|---|---|---|---|
| Draft-01 | 2026-04-22 | | Initial draft |
| Draft-02 | 2026-05-07 | | Refactored catalog APIs |
| Draft-03 | 2026-05-18 | | `catalogType` enum values changed to `MASTER` and `REGULAR`; pull callback download descriptor renamed from `objectUrl` to `downloadManifest`; pull correlation uses `context.messageId` rather than a dedicated `requestId`; catalog search endpoint unified to `POST /catalog/search` with a `filters.type` filter defaulting to `MASTER`; `subscriberId` removed from `CatalogSubscription` — subscriber identity is derived from the Authorization header; terminology updated to Discovery Service throughout |

## 7. Acknowledgements

Beckn Protocol contributors and the implementation working group whose feedback shaped the catalog API design.

## 8. References

- **Governance:** [GOVERNANCE.md](../GOVERNANCE.md).
- **Keyword definitions:** [2_Keyword_Definitions.md](https://github.com/beckn/protocol-specifications-v2/blob/main/docs/2_Keyword_Definitions.md).
- **API specification:** [beckn.yaml](../api/v2.0.0/beckn.yaml).
- **Prior art:** Supersedes 15_Catalog_Publishing_Service.md and 16_Catalog_Discovery_Service.md.
