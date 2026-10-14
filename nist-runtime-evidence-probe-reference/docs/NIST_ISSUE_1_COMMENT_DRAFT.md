# Draft reply to NIST repository Issue #1

Thank you for raising the distinction between output-focused evaluation and
measurement architectures in which operational context, admissibility
conditions, and execution trace are first-class elements. I agree that a trace
can expose important execution conditions that are not recoverable from the
final output alone.

I would like to add a narrower follow-on question: how should an evaluator
distinguish a raw execution trace from independently verifiable execution
evidence?

More specifically: how can a probe independently verify that a claimed
execution actually occurred, was authorized, and produced untampered evidence?

A trace may state that an agent called a tool, but an evaluation may still need
to test whether the call was within an explicit authorization envelope,
whether required evidence is present, whether the retained evidence bytes have
changed, and whether the reported outcome agrees with that evidence. These
checks address a different measurement target from both output quality and the
mere availability of trace events.

I prepared a small reference with six measurement dimensions:

1. **Authorization-to-execution binding:** every observed and evidenced tool
   call must be permitted by the test case and bound to its authorization
   reference.
2. **Tool invocation evidence:** ordered observed calls must match the calls
   retained in the evidence artifact.
3. **Expected-evidence absence:** a case that requires execution evidence fails
   closed when that evidence is missing.
4. **Evidence integrity:** SHA-256 is recomputed over the referenced bytes, so
   a changed artifact is rejected rather than trusted.
5. **Outcome-to-evidence consistency:** expected, observed, and evidenced
   outcomes must agree.
6. **Independent verification:** the verifier computes its own result and
   failure reasons instead of trusting a fixture's self-declared verdict.

The examples are entirely synthetic and cover a successful authorized
execution, an unauthorized call, missing evidence, tampering, and an outcome
mismatch. This does not prove evidence-capture completeness,
authorization-issuer legitimacy, signer identity, trusted time, or production
safety.

The machine-readable record binds a probe ID, test-case ID, nonce, agent ID,
trace ID, authorization reference, ordered invocations, outcome, and evidence
digest. The output retains the dimensions checked and concrete failure reasons.
That makes each negative result reproducible without asking a model judge to
infer whether an execution probably occurred. It also keeps `UNKNOWN` and
missing-evidence states visible rather than treating a plausible final answer
as proof of execution.

This is an independent, development-stage, NIST-style reference implementation.
It is not endorsed, certified, or formally evaluated by NIST, and no formal
compatibility determination is claimed.

The [public repository](https://github.com/joy7758/nist-runtime-evidence-probe-reference)
and its immutable reference include the
[README](https://github.com/joy7758/nist-runtime-evidence-probe-reference/blob/38db7676d481454386f31435fd7845718f9ae358/README.md),
[Schema](https://github.com/joy7758/nist-runtime-evidence-probe-reference/blob/38db7676d481454386f31435fd7845718f9ae358/schema/nist-evaluation-probe.schema.json),
[synthetic examples](https://github.com/joy7758/nist-runtime-evidence-probe-reference/tree/38db7676d481454386f31435fd7845718f9ae358/examples),
[tests](https://github.com/joy7758/nist-runtime-evidence-probe-reference/blob/38db7676d481454386f31435fd7845718f9ae358/tests/test_nist_probe.py),
[technical input](https://github.com/joy7758/nist-runtime-evidence-probe-reference/blob/38db7676d481454386f31435fd7845718f9ae358/docs/NIST_TECHNICAL_INPUT.md),
and [implementation report](https://github.com/joy7758/nist-runtime-evidence-probe-reference/blob/38db7676d481454386f31435fd7845718f9ae358/IMPLEMENTATION_REPORT.md).

Would it be useful to treat independently verifiable runtime execution evidence
as an additional probe dimension, distinct from both output quality and raw
execution traces?

This is offered as a scope question and reproducible negative-test sample, not
as a proposed NIST standard, compatibility claim, certification request, or
request to merge code.

**AI Assistance Disclosure:** This reference implementation and comment were
prepared with assistance from OpenAI Codex and reviewed by Bin Zhang, who
remains responsible for the technical content and licensing.
