# ANS Runtime Execution Evidence Reference

This is an independent, development-stage reference implementation.

It is not an official ANS implementation.

It is not endorsed by the Linux Foundation or the ANS maintainers.

中文：这是一个独立的、开发阶段的参考实现；它不是官方 ANS 实现，也未获得 Linux
基金会或 ANS 维护者背书。

## 1. Problem

[Agent Name Service (ANS)](https://github.com/agentnameservice/ans) provides
identity, discovery, lifecycle, transparency-log, receipt, and offline
verification concepts for agents.

ANS identity state answers:

> Who is the agent?

Runtime execution evidence answers:

> What did the agent actually do in a particular observed execution?

Identity state is not proof of tool execution. Execution evidence does not issue
identity, change ANS lifecycle state, grant permission, or become truth.

## 2. Identity versus execution evidence

```text
ANS identity state
  != runtime execution evidence
  != authorization
  != truth
```

This repository demonstrates a small external link between the two layers. ANS
continues to govern its `ansId`, `ansName`, lifecycle events, transparency log,
and SCITT receipts. An external evidence producer stores an observed operation,
and an independent verifier checks its reference and digest.

## 3. Minimal reference model

```text
ANS ansId / ansName
  -> referenced eventLogId and SCITT receipt pin
  -> execution evidence reference
  -> evidence digest
  -> independent verifier
  -> verification result
```

The schema defines:

- `AgentIdentityReference`
- `ExecutionEvidenceReference`
- `VerificationResult`
- `AuditPointer`

The included example is synthetic. Its `example.test` hosts, UUIDs, URNs,
receipt digest, audit digest, task, and tool call are not real identities,
services, people, customer data, or ANS records.

## 4. Quick verification

Python 3.11 or newer is recommended.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install "jsonschema>=4.23" "pytest>=8"
.venv/bin/python verify_extension.py \
  examples/agent_identity_with_execution_evidence.json
.venv/bin/python -m pytest -q
```

Expected result:

```text
verification_status: PASS
8 passed
```

The verifier fails closed when evidence is missing, unavailable, malformed,
linked to another `ansId` or operation, or changed relative to its digest.

## 5. Repository structure

```text
.
├── README.md
├── LICENSE
├── .pre-commit-config.yaml
├── IMPLEMENTATION_REPORT.md
├── PUBLIC_RELEASE_READINESS_REPORT.md
├── schema/
│   └── ans-evidence-extension.schema.json
├── examples/
│   └── agent_identity_with_execution_evidence.json
├── verify_extension.py
├── tests/
│   └── test_ans_extension.py
└── docs/
    ├── ANS_RUNTIME_EVIDENCE_PROPOSAL.md
    ├── ANS_GITHUB_ISSUE_DRAFT.md
    └── ANS_SUBMISSION_CHECKLIST.md
```

## 6. Tests

The tests cover:

- identity-to-evidence linkage;
- evidence SHA-256 verification;
- tamper rejection;
- missing evidence fail-closed behavior;
- unavailable evidence fail-closed behavior;
- invalid ANS identity-reference rejection;
- invalid declared failure results;
- mismatched audit and operation references.

Ruff, JSON parsing, link checks, a private-path and secret scan, and
`pre-commit run --all-files` are recorded in
[`PUBLIC_RELEASE_READINESS_REPORT.md`](PUBLIC_RELEASE_READINESS_REPORT.md).

## 7. Relationship to current ANS

The terminology was checked against
[`agentnameservice/ans`](https://github.com/agentnameservice/ans) commit
`d8ed4bb6b105863710a07dfce9ceb1c3145de486` on 2026-07-30.

The current ANS public wire contract uses:

- UUID `ansId` and versioned `ansName`;
- JCS-canonicalized signed producer events;
- one append-only Merkle transparency log;
- SCITT COSE_Sign1 receipts whose payload contains the same event bytes used
  for the leaf hash;
- lifecycle events and computed status;
- offline receipt and status-token verification.

This repository does not add a field or event to that contract. It recommends a
companion interoperability profile for the first discussion because it leaves
existing event bytes, signatures, leaf hashes, receipts, status behavior, and
log load unchanged.

The design proposal compares three possible directions:

1. add an external evidence reference to existing event metadata;
2. define a new execution-evidence reference event;
3. publish a separate interoperability extension.

Only the third is implemented here, and only as an independent reference. No
field in this repository has been accepted into ANS.

## 8. Scope and limitations

The verifier validates this repository's JSON Schema, cross-object identifiers,
availability state, deterministic evidence serialization, SHA-256 digest, audit
link, and declared result.

It does not:

- resolve `ansName` or query a Registration Authority;
- cryptographically verify an ANS SCITT receipt or status token;
- modify or append to an ANS transparency log;
- prove that the synthetic tool call occurred in a real runtime;
- implement replay protection, authorization, retention, or key management;
- provide legal non-repudiation, certification, production readiness, or
  official ANS conformance.

The `reference-json-v0.1` digest profile is deterministic local JSON
serialization, not an RFC 8785 JCS conformance claim. A cross-language standard
would need a separately reviewed canonicalization decision and test vectors.

## 9. Contribution and AI assistance disclosure

This package was extracted and adapted from the private, Apache-2.0-licensed
`joy7758/agent-evidence` reference work at implementation commit
`88bb3269b4689b0bf01d23aa8206222717005afd` and submission-material commit
`9ad88f39261a9fd6f30c9c98fac09bd5d5293085`. The same Apache-2.0
[`LICENSE`](LICENSE) is included. No source code from the upstream ANS
repository is copied into this package. The private source repository is
identified for provenance but is not claimed to be anonymously accessible.

The reference implementation and submission materials were prepared with
assistance from OpenAI Codex and Alibaba Cloud Qwen, and reviewed by Bin Zhang,
who remains responsible for the technical content and licensing.

Any future contribution to ANS must follow the upstream contribution guide,
including Issue linkage, human DCO sign-off, review, and AI-assistance
disclosure. AI tools must not add `Signed-off-by:` trailers.

## Agent-readable status

```text
project_name=ANS Runtime Execution Evidence Reference
repository_role=independent_companion_reference
development_stage=Development
official_ans_implementation=false
ans_wire_contract_modified=false
full_runtime_logs_stored_by_ans=false
offline_external_evidence_verifier=true
ans_scitt_cryptographic_verification=false
production_ready=false
official_conformance=false
endorsement=false
human_review_required=true
```
