# Proposal: Linking ANS Identity State with Runtime Execution Evidence

提案：连接 ANS 身份状态与运行时执行证据

Status: `DEVELOPMENT_LOCAL_DRAFT_NOT_SUBMITTED`

This document is an independent discussion artifact. It is not an official ANS
implementation, protocol change, or claim of Linux Foundation or ANS maintainer
endorsement.

Upstream terminology was checked against
[`agentnameservice/ans`](https://github.com/agentnameservice/ans) commit
`d8ed4bb6b105863710a07dfce9ceb1c3145de486` on 2026-07-30.

## 1. Problem

Current ANS concepts answer an identity-state question:

> Who is the agent, and what identity or lifecycle state has ANS recorded?

The current public contract includes:

- immutable `ansId` values and versioned `ansName` values;
- signed, JCS-canonicalized agent event payloads;
- an append-only Merkle transparency log;
- SCITT COSE_Sign1 receipts over the same event bytes used for the leaf hash;
- lifecycle events and computed agent status;
- offline receipt and status-token verification.

A relying party may still need a separate answer:

> What did this agent actually do in a particular observed execution?

An ANS identity event or receipt does not by itself prove that a tool call,
input, output, or task execution occurred. Runtime evidence does not issue an
ANS identity, change lifecycle state, or grant authority.

```text
ANS proves identity state.
Runtime evidence proves an observed execution claim.
Neither object alone is authorization or truth.
```

## 2. Minimal Reference Model

The reference model is deliberately external:

```text
ANS ansId + ansName
  -> referenced ANS event logId + SCITT receipt pin
  -> external execution evidence reference
  -> evidence digest + canonicalization profile
  -> independent verifier
  -> fail-closed verification result
```

The companion object carries only references and verification metadata. It does
not ask ANS to store prompts, full arguments, complete traces, outputs, customer
data, or the evidence body.

The example schema preserves current ANS spellings for `ansId`, `ansName`,
`eventLogId`, and `eventType`. These uses are descriptive mappings, not proposed
new ANS fields.

## 3. Candidate Extension Points

### Option A — add a reference to existing agent event metadata

This is compact, but the current producer event is JCS-canonicalized and signed.
Adding a member changes the canonical event bytes, producer signature, Merkle
leaf hash, and SCITT receipt payload. It also requires a versioned schema and
compatibility decision.

### Option B — define an execution-evidence reference event

A dedicated event avoids changing bytes of existing events, but the current
agent event type is a closed set. A new type changes the accepted event
contract, appends additional leaves to the shared transparency log, and needs
defined status, audit, retention, authorization, and receipt semantics.

### Option C — publish an external interoperability companion profile

The companion profile references an existing ANS `ansId`, `ansName`,
`eventLogId`, and optionally a pinned SCITT receipt while storing the runtime
evidence elsewhere. Existing ANS event bytes, signatures, leaf hashes, receipts,
status computation, and log volume remain unchanged.

## 4. Comparison

| Criterion | A: event metadata | B: new event | C: companion profile |
| --- | --- | --- | --- |
| Existing wire contract | Changes an existing signed shape | Adds a new accepted shape and type | No ANS wire change |
| SCITT receipt | Existing event and receipt bytes change | New event receives a new receipt | Existing receipt is only referenced |
| Byte-for-byte compatibility | Not preserved for extended events | Existing events preserved; accepted contract expands | Preserved |
| Transparency-log load | Larger existing leaves | Additional leaves | None |
| New fact center | Risk of ANS appearing to own execution claims | Stronger risk because log carries a new event family | Evidence remains externally governed |
| Offline verification | Possible after versioning | Possible after defining new semantics | Possible with pinned ANS receipt and evidence object |
| Revoked/unavailable evidence | Needs new metadata semantics | Needs new lifecycle semantics | Explicit external availability status; verifier fails closed |
| First-discussion cost | Medium/high | High | Low |

For a first maintainer discussion, this proposal recommends **Option C** as the
least invasive reference. It does not decide a future upstream implementation.
Options A and B remain questions for maintainers if a standardized reference is
considered in scope.

## 5. Verification and Failure Semantics

The independent verifier checks:

- JSON Schema validity;
- equality of the ANS `ansId` across identity and evidence objects;
- evidence presence and `AVAILABLE` status;
- evidence-object identifier and operation-reference linkage;
- SHA-256 content integrity under the declared `reference-json-v0.1` profile;
- audit-pointer linkage;
- consistency of the declared verification result.

Verification fails closed for missing, unavailable, mismatched, malformed, or
tampered evidence. The availability values `UNAVAILABLE` and `REVOKED` are not
converted to `PASS`.

The reference verifier does **not** cryptographically verify ANS SCITT receipts,
resolve `ansName`, or query an ANS service. It records an ANS receipt URI and
digest pin so a real ANS verifier can be composed separately. It also does not
implement replay protection; a production profile would need an operation ID,
nonce, time window, or equivalent context.

The local `reference-json-v0.1` serialization is deterministic but is not a
claim of RFC 8785 JCS conformance. Any cross-language standardization should
select an explicit canonicalization standard and publish test vectors.

## 6. Revocation and Historical Evidence

ANS lifecycle state and evidence availability are independent dimensions.

- An ANS identity may later become `DEPRECATED`, `REVOKED`, or `EXPIRED` while
  historical execution evidence remains inspectable.
- Evidence may become unavailable or revoked while the ANS identity remains
  active.
- A verifier should report the ANS event and lifecycle state observed for the
  execution context, plus current state when available.
- Missing current state, an unavailable receipt, or unavailable evidence must
  remain explicit and must not inherit an earlier `PASS`.

The companion profile does not revoke ANS identities and does not ask ANS to
become an evidence-retention service.

## 7. Scope and Open Questions

This development-stage reference supplies a schema, synthetic example, offline
verifier, tests, and an implementation report. It makes no production,
conformance, legal non-repudiation, certification, or adoption claim.

Questions for ANS maintainers:

1. Is an external runtime-evidence reference within ANS discussion scope?
2. Is a companion profile preferable to changing the signed event contract?
3. If ANS eventually carries a reference, which event versioning and
   byte-compatibility guarantees must apply?
4. Should ANS specify only a pointer and digest, or also minimum failure,
   availability, replay, and historical-state semantics?
5. Should the ANS SCITT receipt be referenced by URL, digest, leaf identity, or
   another stable locator?

No upstream code change is requested before Issue-level discussion and an
explicit maintainer decision.

If ANS later adopts an event-level design, this companion profile should keep
its published version immutable, mark the superseding ANS version explicitly,
provide a field-by-field migration mapping, and retain historical verification
behavior. An upstream decision must not silently reinterpret existing companion
objects.
