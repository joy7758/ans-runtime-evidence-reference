# Alignment with NIST Evaluation-Probe Research

## Current NIST research focus

NIST's public project describes automated adversarial verifiers that can run
inside an agentic workflow or post hoc and accumulate structured verdicts into
a machine-readable audit trail. Its current demonstrator evaluates factual
grounding through:

- faithfulness;
- completeness; and
- sufficiency.

Those probes ask whether claims are supported and appropriately represented by
trusted source material.

## Additional measurement target

This reference does not replace or criticize those probes. It isolates a
different target: whether a claimed runtime action is supported by a bounded,
integrity-checked execution record.

Issue #1 in the NIST repository already asks whether operational context,
admissibility conditions, and execution trace should become first-class
measurement inputs. This package takes the next question:

> How can a probe independently verify that the claimed execution actually
> occurred, was authorized, and produced untampered evidence?

The distinction is:

```text
raw trace
  != evidence presence
  != authorization-to-execution binding
  != evidence integrity
  != outcome consistency
  != independent verification
```

## Bounded crosswalk

| Measurement concern | Checked material | Failure result |
|---|---|---|
| Authorization-to-execution binding | allowed tools and authorization reference | `FAIL_UNAUTHORIZED_TOOL_CALL` |
| Tool invocation evidence | ordered observed and evidenced calls | `FAIL_UNAUTHORIZED_TOOL_CALL` or `FAIL_TRACE_MISMATCH` |
| Required evidence presence | evidence status and local artifact | `FAIL_MISSING_EVIDENCE` |
| Evidence integrity | computed SHA-256 over exact bytes | `FAIL_EVIDENCE_TAMPERING` |
| Outcome-to-evidence consistency | expected, observed, and evidenced outcome | `FAIL_OUTCOME_MISMATCH` |
| Independent result | recomputed verdict and reasons | input verdict cannot override computation |

## Non-claims

```text
NIST_STYLE=true
DEVELOPMENT_STAGE=true
OFFICIAL_NIST_IMPLEMENTATION=false
NIST_ENDORSED=false
NIST_CERTIFIED=false
NIST_FORMALLY_EVALUATED=false
FORMAL_COMPATIBILITY_DETERMINED=false
PRODUCTION_READY=false
```

The reference is a technical discussion artifact and reproducible negative-test
sample. Only NIST can characterize its own project scope or determine whether
this additional measurement target is useful to that work.
