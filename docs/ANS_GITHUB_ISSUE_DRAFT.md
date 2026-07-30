# Proposal: Linking Agent Identity with Runtime Execution Evidence

Draft status: `FINAL_REVIEW_READY_NOT_SUBMITTED`

All reference links below are pinned to the public, human-DCO-signed commit
`0188da00cba8cc43c1257cd7e6126974a92a1ef1`. This draft has not been posted as
an official ANS Issue, and no Pull Request has been created.

## Summary

Would ANS maintainers consider a small interoperability point for external
runtime execution evidence?

Current ANS concepts answer an identity-state question: **Who is the agent, and
what identity or lifecycle state has ANS recorded?** Runtime execution evidence
answers a separate question: **What did that agent actually do in a particular
observed execution?**

The current implementation combines a registry, an append-only transparency
log, SCITT COSE receipts, and offline verification. This proposal asks first
whether maintainers consider an external evidence reference to be within
discussion scope. Only if maintainers accept that scope would a later Pull
Request be prepared.

The proposal does not ask ANS to store complete runtime logs, become an
execution-evidence system, or become an execution fact center. For a first
discussion, it suggests an independent companion profile that references an
existing ANS identity event and keeps the evidence body outside ANS.

## Motivation

An ANS `ansId`, versioned `ansName`, lifecycle event, transparency-log
inclusion, or SCITT receipt can establish verifiable identity-state context.
Those objects do not by themselves prove that the agent invoked a tool, used
particular inputs, produced an output, or completed a task.

Conversely, an execution evidence object can describe a bounded observed
operation and bind it to an `ansId`, but it should not issue an identity, change
ANS lifecycle state, or grant authority.

```text
ANS proves identity state.
Runtime evidence proves an observed execution claim.
Evidence is not authorization or truth.
```

Keeping these responsibilities separate lets relying parties compose identity
verification with runtime evidence verification without making the ANS registry
the owner of prompts, traces, outputs, retention policy, or domain-specific
execution claims.

## Current ANS Contract Considerations

This draft was checked against `agentnameservice/ans` commit
`d8ed4bb6b105863710a07dfce9ceb1c3145de486`.

The current agent producer event carries `ansId`, `ansName`, `eventType`,
`timestamp`, `raId`, and agent data. It is JCS-canonicalized and signed. The
transparency log computes the Merkle leaf from those canonical bytes, and the
SCITT COSE_Sign1 receipt carries the same event bytes.

The current agent-event tokens are a closed set:

- `AGENT_REGISTERED`
- `AGENT_RENEWED`
- `AGENT_DEPRECATED`
- `AGENT_REVOKED`

These properties make byte compatibility and log semantics important. A new
member in an existing event is not merely descriptive metadata: it changes the
signed bytes, leaf hash, and receipt payload.

## Minimal Proposal

The reference implementation therefore starts with a separate companion
object:

```json
{
  "agent_identity_reference": {
    "ansId": "0198f000-0000-7000-8000-000000000001",
    "ansName": "ans://v1.0.0.build-agent.example.test",
    "eventLogId": "0198f000-0000-7000-8000-000000000002",
    "eventType": "AGENT_REGISTERED",
    "lifecycle_status": "ACTIVE",
    "scitt_receipt_uri": "https://tl.example.test/v1/agents/0198f000-0000-7000-8000-000000000001/receipt",
    "scitt_receipt_sha256": "sha256:<64-lowercase-hex>"
  },
  "execution_evidence_reference": {
    "execution_evidence_id": "urn:example:execution-evidence:operation-001",
    "ansId": "0198f000-0000-7000-8000-000000000001",
    "evidence_uri": "https://evidence.example.test/operation-001.json",
    "digest_algorithm": "sha-256",
    "canonicalization": "reference-json-v0.1",
    "evidence_sha256": "sha256:<64-lowercase-hex>",
    "availability_status": "AVAILABLE"
  }
}
```

The names outside `ansId`, `ansName`, `eventLogId`, and `eventType` are
illustrative and non-normative. The object records a relationship; the external
evidence and an independent verifier remain responsible for the execution
claim.

Verification fails closed when evidence is missing, unavailable, malformed,
linked to another `ansId` or operation, or changed relative to its digest.
Historical evidence may remain inspectable after ANS deprecation or revocation,
but the relevant lifecycle state must stay explicit.

## Alternatives

### A. Add a reference to existing agent event metadata

This is compact, but it changes the JCS event bytes, producer signature, Merkle
leaf hash, receipt payload, and schema/version compatibility surface.

### B. Define a new execution-evidence reference event

Existing event bytes remain unchanged, but the accepted event-type contract
expands. New leaves increase transparency-log load, and status, authorization,
retention, audit, and receipt semantics would need to be defined.

### C. Publish an interoperability companion profile

`OPTION_C_EXTERNAL_INTEROPERABILITY_COMPANION_PROFILE`

Existing ANS event bytes, signatures, receipts, status behavior, and log load
remain unchanged. The profile can support offline composition when the ANS
receipt, external evidence, digest rules, and verifier inputs are available.

For a first discussion, I prefer **C** because it has the smallest impact. This
preference is not a request to decide an upstream implementation before
maintainer feedback.

## Reference Implementation

An independent, development-stage reference package is prepared at:

- [Repository](https://github.com/joy7758/ans-runtime-evidence-reference)
- [README](https://github.com/joy7758/ans-runtime-evidence-reference/blob/0188da00cba8cc43c1257cd7e6126974a92a1ef1/README.md)
- [Schema](https://github.com/joy7758/ans-runtime-evidence-reference/blob/0188da00cba8cc43c1257cd7e6126974a92a1ef1/schema/ans-evidence-extension.schema.json)
- [Synthetic example](https://github.com/joy7758/ans-runtime-evidence-reference/blob/0188da00cba8cc43c1257cd7e6126974a92a1ef1/examples/agent_identity_with_execution_evidence.json)
- [Offline verifier](https://github.com/joy7758/ans-runtime-evidence-reference/blob/0188da00cba8cc43c1257cd7e6126974a92a1ef1/verify_extension.py)
- [Tests](https://github.com/joy7758/ans-runtime-evidence-reference/blob/0188da00cba8cc43c1257cd7e6126974a92a1ef1/tests/test_ans_extension.py)
- [Technical proposal](https://github.com/joy7758/ans-runtime-evidence-reference/blob/0188da00cba8cc43c1257cd7e6126974a92a1ef1/docs/ANS_RUNTIME_EVIDENCE_PROPOSAL.md)
- [Implementation report](https://github.com/joy7758/ans-runtime-evidence-reference/blob/0188da00cba8cc43c1257cd7e6126974a92a1ef1/IMPLEMENTATION_REPORT.md)

The verifier checks the external profile only. It does not resolve `ansName`,
query ANS, or cryptographically verify SCITT receipts; those capabilities must
be supplied by an ANS verifier. The local JSON canonicalization profile is also
not a claim of RFC 8785 conformance.

Option C does not modify the existing ANS wire contract.

## Non-goals

This proposal does not:

- replace ANS or redefine ANS identity;
- claim official ANS implementation, compatibility, or conformance;
- claim Linux Foundation or maintainer endorsement;
- require ANS to store full execution logs or sensitive runtime payloads;
- turn a digest, evidence object, or verifier result into authorization;
- define legal non-repudiation, certification, or production readiness;
- request an upstream code change before Issue-level discussion.

## Questions for Maintainers

1. Is an external runtime-evidence reference in scope for ANS discussion?
2. Is a companion profile preferable to changing signed agent event bytes?
3. If ANS eventually carries a reference, should it use an existing event
   version, a new event type, or a separately versioned object?
4. Which stable identity-event locator should be referenced: `logId`, receipt
   digest, leaf identity, or another value?
5. Should ANS define minimum behavior for unavailable or revoked evidence, or
   leave all such semantics to the external profile?
6. Which canonicalization and replay-context fields would be necessary for
   cross-language offline verification?

## AI Assistance Disclosure

The reference implementation and submission materials were prepared with assistance from OpenAI Codex and reviewed by Bin Zhang, who remains responsible for the technical content and licensing.

No maintainer opinion, acceptance, or endorsement is implied by this draft.
