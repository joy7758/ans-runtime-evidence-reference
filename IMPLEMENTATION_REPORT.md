# ANS Runtime Evidence Reference Implementation Report

Date: 2026-07-30

Status: `LOCAL_PACKAGE_VALIDATED_HUMAN_COMMIT_REQUIRED`

## Outcome

A minimal, independent companion reference links:

```text
ANS ansId + ansName
  -> ANS event and SCITT receipt reference
  -> external execution evidence object
  -> content digest
  -> independent fail-closed verifier
  -> verification result and audit pointer
```

The package does not implement or replace ANS identity, modify the ANS wire
contract, store full runtime logs in ANS, or create a new source of truth.

## Source and License

The implementation was extracted and adapted from the Apache-2.0-licensed
`joy7758/agent-evidence` repository:

- implementation commit:
  `88bb3269b4689b0bf01d23aa8206222717005afd`;
- external-material commit:
  `9ad88f39261a9fd6f30c9c98fac09bd5d5293085`.

The source LICENSE was copied without modification. The package contains no
source code copied from the upstream ANS repository.

## Upstream ANS Review

The following upstream source was reviewed read-only:

- repository: <https://github.com/agentnameservice/ans>;
- commit: `d8ed4bb6b105863710a07dfce9ceb1c3145de486`;
- observed date: 2026-07-30;
- files: `README.md`, `CONTRIBUTING.md`, `spec/api-spec-v2.yaml`,
  `spec/api-spec-tl-v2.yaml`, and the agent event, identity, status,
  certificate, and name-related files under `internal/domain`.

Observed contract facts used by the proposal:

- `ansId` is an immutable agent UUID and `ansName` is a separate versioned
  DNS-style name;
- producer events are JCS-canonicalized and signed;
- event bytes determine the Merkle leaf and are carried by the SCITT
  COSE_Sign1 receipt;
- the agent producer-event enum is `AGENT_REGISTERED`, `AGENT_RENEWED`,
  `AGENT_DEPRECATED`, and `AGENT_REVOKED`;
- identity events share the transparency log but remain a separate keyed
  stream;
- offline receipt and status-token verification are current ANS concepts.

## Extension-Point Decision

Three options were compared.

| Option | Result for first discussion |
| --- | --- |
| Add evidence metadata to an existing signed event | Not preferred: changes canonical bytes, signature, leaf hash, receipt payload, and compatibility surface |
| Add a new execution-evidence event | Not preferred: expands the closed event contract and transparency-log load, and requires new semantics |
| External companion interoperability profile | Preferred: leaves all current ANS bytes, receipts, status behavior, and log load unchanged |

The preferred option is a discussion recommendation, not an upstream ANS
decision.

## Public Artifacts

| Artifact | Purpose |
| --- | --- |
| `README.md` | Five-minute entry, quick verification, actual ANS mapping, scope, attribution, and AI disclosure |
| `.pre-commit-config.yaml` | Reproducible merge-conflict, whitespace, JSON, and Ruff gates |
| `schema/ans-evidence-extension.schema.json` | Draft 2020-12 schema with the four reference definitions |
| `examples/agent_identity_with_execution_evidence.json` | Fully synthetic ANS identity/evidence lifecycle |
| `verify_extension.py` | Offline schema, linkage, availability, digest, and audit verifier |
| `tests/test_ans_extension.py` | Positive and fail-closed regression cases |
| `docs/ANS_RUNTIME_EVIDENCE_PROPOSAL.md` | Technical proposal and three-option comparison |
| `docs/ANS_GITHUB_ISSUE_DRAFT.md` | Do-not-post Issue draft with immutable-link placeholders |
| `docs/ANS_SUBMISSION_CHECKLIST.md` | Publication, license, DCO, and external-action gates |
| `PUBLIC_RELEASE_READINESS_REPORT.md` | Reproducible check results and limitations |

## Verification Boundary

The verifier performs strict Draft 2020-12 JSON Schema validation and then
checks:

- `ansId` linkage;
- evidence presence and `AVAILABLE` state;
- evidence object and operation identifiers;
- `reference-json-v0.1` SHA-256 integrity;
- audit-pointer linkage;
- declared result consistency.

The deterministic JSON profile is not an RFC 8785 conformance claim. The
verifier does not resolve `ansName`, query ANS, cryptographically verify a
SCITT receipt, establish that a real execution occurred, or grant authority.

## Independent Agent Recommendation Gate

The highest configured model, `qwen3.8-max-preview`, was attempted twice with
reduced context, but both calls timed out before returning a result.
`qwen3.7-max` was then used as the highest responsive review model.

```text
CUSTOMER_RECOMMENDATION=CONDITIONALLY_RECOMMENDED
TECHNICAL_VERDICT=APPROVE
BLOCKING_FINDINGS=0
```

The remaining conditions are:

- no live ANS resolution;
- no cryptographic SCITT receipt verification in this repository;
- external evidence URI availability is outside this repository;
- no upstream acceptance, production use, or legal reliance.

The reviewer agreed that Option C is appropriately isolated for a
development-stage reference.

## Claims and Authority Boundary

```text
INDEPENDENT_REFERENCE_IMPLEMENTED=true
IDENTITY_SYSTEM_CREATED=false
ANS_WIRE_CONTRACT_MODIFIED=false
ANS_EVENT_TYPE_ADDED=false
ANS_TRANSPARENCY_LOG_WRITTEN=false
ANS_SCITT_RECEIPT_VERIFIED=false
FULL_RUNTIME_LOGS_STORED_BY_ANS=false
OFFICIAL_ANS_IMPLEMENTATION=false
OFFICIAL_ANS_CONFORMANCE=false
LINUX_FOUNDATION_ENDORSEMENT=false
PRODUCTION_READY=false
EXTERNALLY_VALIDATED=false
LEGAL_NON_REPUDIATION=false
FINAL_COMMIT_CREATED=false
PUSH_EXECUTED=false
OFFICIAL_ISSUE_CREATED=false
OFFICIAL_PULL_REQUEST_CREATED=false
HUMAN_DCO_SIGNOFF_REQUIRED=true
```

Conclusion: `READY_FOR_HUMAN_DCO_NOT_COMMITTED_NOT_PUBLISHED`
