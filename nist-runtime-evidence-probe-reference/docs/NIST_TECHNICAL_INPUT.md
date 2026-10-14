# Technical Input: Independently Verifiable Runtime Execution Evidence

> Independent, development-stage technical input. This document is not an
> official NIST specification, implementation, endorsement, certification,
> formal evaluation, or compatibility determination.

## Measurement gap

An agent's output can be factually grounded while the runtime action described
by that output remains unverified. A statement such as “I used the approved
tool and completed the operation” contains several distinct claims:

1. a tool invocation occurred;
2. the invocation was authorized;
3. the retained execution record belongs to the relevant actor and trace;
4. required evidence is present;
5. the evidence has not changed since its digest was recorded; and
6. the reported outcome agrees with the evidence.

A raw trace may contain useful events without independently establishing all
six claims. Conversely, a final answer may be correct even when the action was
unauthorized or the execution record is missing.

## Relationship to current NIST probes and Issue #1

NIST's current demonstrator evaluates whether claims are faithful, complete,
and sufficient relative to trusted source material. The project also uses
structured audit trails and supports active or post-hoc probes.

NIST repository Issue #1 asks whether operational context, admissibility
conditions, and execution trace should be first-class measurement inputs. That
is the starting point for this input, not a question to repeat.

The narrower follow-on question is:

> Would it be useful to treat independently verifiable runtime execution
> evidence as an additional probe dimension, distinct from both output quality
> and raw execution traces?

## Proposed measurement dimension

The proposed measurement target is **Runtime Execution Evidence Consistency**.
It compares the expected policy and outcome, the observed execution, and a
referenced evidence artifact.

### Authorization-to-execution binding

The expected behavior declares an allowed-tool set and an authorization
reference. Each observed and evidenced invocation must use an allowed tool and
carry the expected binding. A tool's technical availability does not establish
authorization.

### Tool invocation evidence

Observed and evidenced invocation sequences are compared by sequence number,
tool identifier, and authorization reference. A claimed call that is absent
from the evidence, or an evidenced call omitted from the observation, fails the
trace-consistency check.

### Evidence presence and expected-evidence absence

When a test case requires evidence, missing status or a missing local artifact
fails closed. The verifier does not substitute the agent's narrative, an
expected verdict, or another passing field for the absent evidence.

### Evidence integrity

The verifier calculates SHA-256 over the exact referenced bytes. A mismatch
fails before evidence contents are trusted. This detects byte changes only; it
does not establish signer identity, trusted time, custody, or non-repudiation.

### Outcome-to-evidence consistency

Expected, observed, and evidenced outcome objects must match. A successful
expected outcome cannot mask an observed failure or different result digest.

### Independent verification result

The fixture's `verification_result` is an expected test assertion, not an
authority-bearing self-attestation. The verifier returns a newly computed
result, checked dimensions, and reasons.

## Machine-readable contract

The JSON Schema requires:

```text
probe_id
agent_id
test_case
expected_behavior
observed_behavior
evidence_reference
verification_result
```

Stable probe, case, nonce, actor, and trace identifiers bind the supplied
records. The validator rejects unknown top-level fields, non-local evidence
URIs, absolute paths, and fixture-root traversal.

The principal results are:

```text
PASS
FAIL_UNAUTHORIZED_TOOL_CALL
FAIL_MISSING_EVIDENCE
FAIL_EVIDENCE_TAMPERING
FAIL_IDENTITY_MISMATCH
FAIL_TRACE_MISMATCH
FAIL_OUTCOME_MISMATCH
ERROR_INVALID_PROBE
```

## Reproducible failure vectors

The standalone reference retains five synthetic fixtures:

| Vector | Intended observation |
|---|---|
| successful execution | authorized call, evidence digest, trace, and outcome agree |
| unauthorized tool call | actual tool is outside the allowlist |
| missing evidence | required execution evidence is unavailable |
| evidence tampering | current evidence bytes differ from the recorded digest |
| outcome mismatch | expected, observed, and evidenced outcomes disagree |

The tests also show that recomputing a hash after introducing an unauthorized
evidence-only call does not turn the case into `PASS`, and that a forged input
verdict cannot override the computed result.

## Domain relevance

- **Industrial workflows:** separate a recommendation from an actually issued,
  authorized tool action without replacing plant safety authority.
- **Medical device and imaging workflows:** test synthetic retrieval, analysis,
  or export traces without using patient data or claiming clinical validation.
- **Software engineering agents:** compare claimed build, test, repository, or
  deployment calls with retained evidence without authorizing a merge or
  deployment.
- **Compliance and audit:** route human review toward missing, unauthorized,
  changed, or inconsistent evidence without turning the probe into a legal
  conclusion or certification.

## Current limits

- Evidence-capture completeness and unobserved activity are not proven.
- The authorization issuer and policy decision process are not verified.
- SHA-256 is not a signature or trusted timestamp.
- No remote evidence retrieval, custody validation, replay registry, hardware
  attestation, or confidential-computing integration is included.
- All examples are synthetic and local.
- No official NIST harness interoperability or formal conformance has been
  tested.
- A local `PASS` is not a system trust score, production-safety decision,
  certification, adoption claim, or permission to execute.

The intended contribution is a reproducible measurement example and a narrow
scope question, not a request to merge code or define a NIST standard.
