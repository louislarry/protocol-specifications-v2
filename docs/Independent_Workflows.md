# Independent Workflows

## Document Details

- **ID:** NFH-TBD
- **Status:** Stub — under draft.
- **Authors:**
  - [Ravi Prakash](https://github.com/ravi-prakash-v), [Networks for Humanity](https://networksforhumanity.org)
- **Created:** 2026-05-16
- **Updated:** 2026-05-16
- **Version history:** Stub (2026-05-16): Placeholder registered; content under draft.
- **Latest editor's draft:** Click [here](https://github.com/beckn/protocol-specifications-v2/blob/draft/docs/Independent_Workflows.md).
- **Implementation report:** Not available.
- **Stress test report:** Not available.
- **Conformance impact:** Not determined.
- **Security/privacy implications:** To be determined.
- **Replaces / Relates to:** Extends [NFH-013 Beckn Communication Model](./Communication_Protocol.md); relates to [NFH-001 Architecture, Design Philosophy and Principles](./Introduction.md).
- **Feedback:**
  - Issues: Click [here](https://github.com/beckn/protocol-specifications-v2/issues?q=is%3Aissue+label%3A%22NFH-TBD%22)
  - Discussions: Click [here](https://github.com/beckn/protocol-specifications-v2/discussions?discussions_q=label%3A%22NFH-TBD%22)
  - Pull Requests: Click [here](https://github.com/beckn/protocol-specifications-v2/pulls?q=is%3Apr+label%3A%22NFH-TBD%22)
- **Errata:** To be published.

## Abstract

> To be written.

This RFC specifies how Consumer Nodes and Provider Nodes maintain independent internal workflows in a stateless Beckn protocol interaction. Because Beckn Protocol declares state rather than synchronising it, each node is responsible for managing its own workflow independently of the other. This RFC will cover: recommended state-machine patterns for CNs and PNs, how to handle arriving callbacks as asynchronous events rather than blocking responses, anti-patterns arising from tight coupling to the other node's state, and guidance for AI Agent-operated nodes that process callback events as tool-call responses in an agentic loop.

## Table of Contents

- [Independent Workflows](#independent-workflows)
  - [Document Details](#document-details)
  - [Abstract](#abstract)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Specification](#specification)
    - [Definitions](#definitions)
    - [Normative Requirements](#normative-requirements)
    - [Conformance Requirements](#conformance-requirements)
    - [Cross-cutting Considerations](#cross-cutting-considerations)
    - [Migration Notes](#migration-notes)
    - [Examples](#examples)
  - [Conclusion](#conclusion)
    - [Open Questions](#open-questions)
  - [Acknowledgements](#acknowledgements)
  - [References](#references)

## Introduction

> To be written.

## Specification

> To be written.

### Definitions

> To be written.

### Normative Requirements

> To be written.

### Conformance Requirements

> To be written.

### Cross-cutting Considerations

> To be written.

### Migration Notes

> To be written.

### Examples

> To be written.

## Conclusion

> To be written.

### Open Questions

1. Should this RFC define normative state-machine schemas that nodes MUST implement, or leave state-machine design to implementers while only mandating observable behaviour?
2. How should a CN handle the case where a PN's callback contradicts the CN's own internally committed state (e.g., PN sends `on_cancel` after CN has already marked the order as confirmed)?
3. Should timeout and retry policies for pending `messageId` resolution be normative or informative?

## Acknowledgements

> To be written.

## References

- **NFH-013 Beckn Communication Model:** Click [here](./Communication_Protocol.md).
- **NFH-001 Architecture, Design Philosophy and Principles:** Click [here](./Introduction.md).
- **Keyword Definitions:** Click [here](./Keyword_Definitions.md).
- **Governance:** Click [here](../GOVERNANCE.md).
